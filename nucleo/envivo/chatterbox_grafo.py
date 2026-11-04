# -*- coding: utf-8 -*-
"""T3 de Chatterbox Multilingual con el paso de decodificación capturado en un CUDA Graph (EN VIVO, 4-nov-2026).

Por qué: en la RTX 4060 el bucle autorregresivo de T3 (Llama de 30 capas, 1 token = 40 ms de audio) va a ~26 pasos/s con la
GPU al 13 %: lo frena lanzar cientos de kernels pequeños por paso desde Python, no el cálculo (fp16/bf16 lo empeoran).
Un CUDA Graph lanza el paso entero de una vez. Caché estática fija (`LARGO`) para capturar UNA vez y reutilizar el grafo
en todas las frases; las posiciones viejas de la frase anterior quedan fuera por la máscara causal (cache_position).
Mismo muestreo que `T3.inference` (CFG, repetición, temperatura, min_p, top_p). Sin triton (no hay en Windows).

    import chatterbox_grafo; chatterbox_grafo.instalar(modelo)   # modelo = ChatterboxMultilingualTTS
"""
import types

import torch
from transformers import StaticCache
from transformers.generation.logits_process import (MinPLogitsWarper, RepetitionPenaltyLogitsProcessor,
                                                    TopPLogitsWarper)

LARGO = 1600        # prefijo (voz de referencia + texto, ~150-400) + hasta 1000 tokens de habla (40 s)


class _Grafo:
    def __init__(self, t3):
        self.t3, self.tf = t3, t3.tfmr
        dev = next(t3.parameters()).device
        self.dev = dev
        self.cache = StaticCache(config=self.tf.config, max_cache_len=LARGO)
        d = self.tf.config.hidden_size
        self.emb = torch.zeros(2, 1, d, device=dev)
        self.pos = torch.zeros(1, dtype=torch.long, device=dev)
        self.grafo, self.logits = None, None

    def _paso(self):
        o = self.tf(inputs_embeds=self.emb, past_key_values=self.cache, use_cache=True, cache_position=self.pos)
        return self.t3.speech_head(o.last_hidden_state)[:, -1, :]

    def prefill(self, inp):
        P = inp.shape[1]
        o = self.tf(inputs_embeds=inp, past_key_values=self.cache, use_cache=True,
                    cache_position=torch.arange(P, device=self.dev))
        logits = self.t3.speech_head(o.last_hidden_state)[:, -1, :]
        if self.grafo is None:                       # captura una vez, escribiendo basura en la posición P (se pisa luego)
            self.pos.fill_(P)
            s = torch.cuda.Stream()
            s.wait_stream(torch.cuda.current_stream())
            with torch.cuda.stream(s):
                for _ in range(3):
                    self._paso()
            torch.cuda.current_stream().wait_stream(s)
            self.grafo = torch.cuda.CUDAGraph()
            with torch.cuda.graph(self.grafo):
                self.logits = self._paso()
        return logits

    def paso(self, emb, pos):
        self.emb.copy_(emb)
        self.pos.fill_(pos)
        self.grafo.replay()
        return self.logits


def _inference(self, *, t3_cond, text_tokens, initial_speech_tokens=None, max_new_tokens=1000, temperature=0.8, top_p=0.95,
               min_p=0.05, repetition_penalty=1.2, cfg_weight=0.5, **_):
    g = self._grafo
    text_tokens = torch.atleast_2d(text_tokens).to(dtype=torch.long, device=g.dev)
    if initial_speech_tokens is None:
        initial_speech_tokens = self.hp.start_speech_token * torch.ones_like(text_tokens[:, :1])
    embeds, _ = self.prepare_input_embeds(t3_cond=t3_cond, text_tokens=text_tokens, speech_tokens=initial_speech_tokens,
                                          cfg_weight=cfg_weight)
    bos = torch.tensor([[self.hp.start_speech_token]], dtype=torch.long, device=g.dev)
    bos_emb = self.speech_emb(bos) + self.speech_pos_emb.get_fixed_embedding(0)
    inp = torch.cat([embeds, torch.cat([bos_emb, bos_emb])], dim=1)
    P = inp.shape[1]
    max_new_tokens = min(max_new_tokens, LARGO - P - 1)
    logits_step = g.prefill(inp)

    top_p_w, min_p_w = TopPLogitsWarper(top_p=top_p), MinPLogitsWarper(min_p=min_p)
    rep = RepetitionPenaltyLogitsProcessor(penalty=float(repetition_penalty))
    cfg = torch.as_tensor(cfg_weight, device=g.dev, dtype=logits_step.dtype)
    generated, predicted = bos.clone(), []
    for i in range(max_new_tokens):
        cond, uncond = logits_step[0:1, :], logits_step[1:2, :]
        logits = rep(generated, cond + cfg * (cond - uncond))
        if temperature != 1.0:
            logits = logits / temperature
        logits = top_p_w(generated, min_p_w(generated, logits))
        nxt = torch.multinomial(torch.softmax(logits, dim=-1), num_samples=1)
        predicted.append(nxt)
        generated = torch.cat([generated, nxt], dim=1)
        if nxt.item() == self.hp.stop_speech_token:
            break
        e = self.speech_emb(nxt) + self.speech_pos_emb.get_fixed_embedding(i + 1)
        logits_step = g.paso(torch.cat([e, e]), P + i)
    return torch.cat(predicted, dim=1)


def instalar(modelo):
    """Cambia `modelo.t3.inference` por la versión con grafo (se captura en la primera frase)."""
    t3 = modelo.t3
    t3._grafo = _Grafo(t3)
    t3._inference_original = t3.inference
    t3.inference = types.MethodType(_inference, t3)
    return modelo
