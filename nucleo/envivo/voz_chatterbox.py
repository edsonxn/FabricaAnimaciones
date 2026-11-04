# -*- coding: utf-8 -*-
"""Voz del EN VIVO con Chatterbox (local, GPU, gratis): la voz del canal en vez de la de Windows.

`--voz chatterbox:Sarcastica` (o `chatterbox:Faraon`, cualquier archivo de C:\\chatterbox_voices). El modelo se carga UNA vez
en el proceso del servidor (~3-4 GB de VRAM con t3 v3) y la GPU va con candado: los 2 guionistas en paralelo hacen cola aquí.
Tal cual, Chatterbox va a 1,07× el tiempo real en la RTX 4060 (más lento de lo que suena: el búfer se vacía); con el paso de
T3 en un CUDA Graph (`chatterbox_grafo.py`, mismo audio exacto) va a 0,74×.
Misma firma que `voz.sintetizar`: un .wav por frase y su duración. La FONETICA sale de los guiones de los videos del canal
(Chatterbox solo sabe español: «Skyrim» → «Escairim»). Ver docs/estilo_envivo.md § «Voz con Chatterbox».
"""
import ast
import glob
import os
import re
import threading
import time
import wave

VOCES = r"C:\chatterbox_voices"
REPO = r"C:\chatterbox\repo\src"
# los de docs/voz.md para Tamriel (tes_exploits_rotos y siguientes)
AJUSTES = dict(exaggeration=0.6, cfg_weight=0.35, temperature=0.75)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREFIJO_FONETICA = {"cronicas_tamriel": "tes_", "runa_caida": "er_"}

_modelo, _ref, _candado = None, None, threading.Lock()
_fonetica = {}
medidas = []          # (segundos de audio, segundos de síntesis) por frase: para la traza del factor de tiempo real


def cargar_fonetica(canal="cronicas_tamriel"):
    """Une las FONETICA de los videos del canal; la del video más reciente gana."""
    pref = PREFIJO_FONETICA.get(canal, "tes_")
    guiones = sorted(glob.glob(os.path.join(RAIZ, "videos", pref + "*", "guion.py")), key=os.path.getmtime)
    tabla = {}
    for g in guiones:
        try:
            s = open(g, encoding="utf-8").read()
        except OSError:
            continue
        m = re.search(r"^FONETICA\s*=\s*(\{.*?\n\})", s, re.S | re.M)
        if not m:
            continue
        try:
            tabla.update({k: v for k, v in ast.literal_eval(m.group(1)).items() if isinstance(v, str) and k != v})
        except Exception:
            pass
    _fonetica.clear()
    _fonetica.update(tabla)
    return len(tabla)


def fonetica(t):
    for k in sorted(_fonetica, key=len, reverse=True):
        t = re.sub(r"(?<![\wÁÉÍÓÚáéíóúñÑ])" + re.escape(k) + r"(?![\wÁÉÍÓÚáéíóúñÑ])", _fonetica[k], t)
    return t


def limpiar(t):
    t = re.sub(r"\[[^\]]*\]", "", t)
    t = t.replace("«", "").replace("»", "").replace("*", "").replace("“", "").replace("”", "")
    return re.sub(r"\s+", " ", t).strip()


def preparar(voz="Sarcastica", canal="cronicas_tamriel"):
    """Carga el modelo y la voz de referencia (tarda ~20-40 s la primera vez)."""
    global _modelo, _ref
    with _candado:
        if _modelo is None:
            import sys
            if REPO not in sys.path:
                sys.path.insert(0, REPO)
            from chatterbox.mtl_tts import ChatterboxMultilingualTTS
            _modelo = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
            cargar_fonetica(canal)
            try:
                from envivo import chatterbox_grafo
                chatterbox_grafo.instalar(_modelo)
            except Exception as e:                       # sin grafo va igual, solo más lento (~1,07×)
                print("chatterbox sin CUDA Graph:", e, flush=True)
        ref = voz if os.path.isabs(voz) else next(iter(glob.glob(os.path.join(VOCES, voz + ".*"))), None)
        if not ref:
            raise FileNotFoundError(f"no está la voz {voz} en {VOCES}")
        if ref != _ref:
            _modelo.prepare_conditionals(ref, exaggeration=AJUSTES["exaggeration"])
            _ref = ref
    return _modelo


def _guardar(ruta, wav, sr):
    import numpy as np
    a = wav.squeeze().detach().cpu().numpy()
    a = (np.clip(a, -1, 1) * 32767).astype("<i2")
    with wave.open(ruta, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(a.tobytes())
    return len(a) / float(sr)


def una(texto, ruta, voz="Sarcastica", semilla=None):
    """Una frase → (ruta, segundos). Sale con la GPU tomada solo mientras genera."""
    import torch
    m = preparar(voz)
    t = fonetica(limpiar(texto))
    with _candado:
        t0 = time.time()
        if semilla is not None:
            torch.manual_seed(semilla)
        try:
            wav = m.generate(t, language_id="es", **AJUSTES)
        except Exception as e:
            if not hasattr(m.t3, "_inference_original"):
                raise
            print("CUDA Graph falló, vuelvo al bucle normal:", e, flush=True)
            m.t3.inference = m.t3._inference_original
            del m.t3._inference_original
            wav = m.generate(t, language_id="es", **AJUSTES)
        dur = _guardar(ruta, wav, m.sr)
        medidas.append((dur, time.time() - t0))
        del medidas[:-200]
    return ruta, dur


def sintetizar(textos, carpeta, base, voz="Sarcastica", velocidad=None, al_terminar=None, vigente=None):
    """textos -> [(ruta_wav, segundos)], como voz.sintetizar. `al_terminar(i, ruta, dur)` avisa frase a frase.
    `vigente()` falso (cambió el tema) = deja de ocupar la GPU con un bloque que se va a tirar."""
    os.makedirs(carpeta, exist_ok=True)
    salida = []
    for i, t in enumerate(textos):
        ruta = os.path.join(carpeta, f"{base}_{i:02d}.wav")
        if vigente and not vigente():
            salida.append((None, max(1.5, len(limpiar(t)) / 15.0)))
            continue
        try:
            r = una(t, ruta, voz, semilla=1000 + i)
        except Exception:
            r = (None, max(1.5, len(limpiar(t)) / 15.0))
        salida.append(r)
        if al_terminar:
            al_terminar(i, *r)
    return salida


def factor():
    """Segundos de síntesis por segundo de audio de las últimas frases (< 1 = va por delante)."""
    if not medidas:
        return None
    a = sum(d for d, _ in medidas[-30:])
    s = sum(x for _, x in medidas[-30:])
    return s / a if a else None
