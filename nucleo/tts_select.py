# -*- coding: utf-8 -*-
"""Evalúa todos los candidatos, elige la mejor toma por frase, la limpia y la alinea.

Salidas:
  voz/eval.json         métricas por candidato (caché)
  voz/final/<key>.wav   toma elegida, recortada, 48 kHz, -20 LUFS
  voz/palabras.json     {key: {"dur":..., "words":[{"w","s","e"}], "take":..., "cer":..., "sim":...}}
Imprime las frases que no pasan el umbral para regenerarlas.
"""
import difflib
import glob
import json
import os
import re

import librosa
import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from faster_whisper import WhisperModel

import config
from qa import SpeakerSim, artefactos, cer, normaliza

SR_OUT = 48000
CER_MAX = 0.012
GAP_MAX = 0.65
TAIL_MAX = 0.35

os.makedirs("voz/final", exist_ok=True)
evals = json.load(open("voz/eval.json", encoding="utf-8")) if os.path.exists("voz/eval.json") else {}

wm = WhisperModel("large-v3", device="cuda", compute_type="float16")
spk = SpeakerSim(config.VOZ["referencia"])
IDIOMA = config.VOZ["idioma"]
textos = {f"{e['id']}_{i}": t for e in config.ESCENAS for i, t in enumerate(e["frases"])}

# ---------- 1) evaluar candidatos ----------
for path in sorted(glob.glob("voz/cands/*.wav")):
    name = os.path.basename(path)
    if name in evals:
        continue
    key = re.sub(r"_s\d+\.wav$", "", name)
    y, sr = librosa.load(path, sr=None)
    segs, _ = wm.transcribe(path, language=IDIOMA, beam_size=5, vad_filter=False)
    hyp = " ".join(s.text for s in segs).strip()
    evals[name] = dict(key=key, hyp=hyp, cer=cer(textos[key], hyp), sim=spk.sim(y, sr),
                       dur=len(y) / sr, **artefactos(y, sr))
    json.dump(evals, open("voz/eval.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# la CER se recalcula desde la transcripción guardada (así una mejora de qa.normaliza aplica a tomas viejas)
for m in evals.values():
    if m["key"] in textos:
        m["cer"] = cer(textos[m["key"]], m["hyp"])

# ---------- 2) elegir ----------
elegidas, fallan = {}, []
for key in textos:
    cands = [(n, m) for n, m in evals.items() if m["key"] == key]
    if not cands:
        fallan.append(key)
        continue
    med = float(np.median([m["dur"] for _, m in cands]))
    ok = [(n, m) for n, m in cands
          if m["cer"] <= CER_MAX and m["gap_max"] <= GAP_MAX and m["tail_ratio"] <= TAIL_MAX
          and m["peak"] < 0.999]
    if not ok:
        fallan.append(key)
        continue

    def score(m):
        # similitud de voz manda; penaliza errores, pausas largas y duraciones atípicas
        return (m["sim"] - 3.0 * m["cer"] - 0.15 * max(0.0, m["gap_max"] - 0.45)
                - 0.05 * abs(m["dur"] - med) / med)
    n, m = max(ok, key=lambda nm: score(nm[1]))
    elegidas[key] = (n, m)

print(f"{len(elegidas)}/{len(textos)} frases con toma válida")
json.dump(fallan, open("voz/regenerar.json", "w", encoding="utf-8"))
if fallan:
    print("REGENERAR:", " ".join(fallan))


# ---------- 3) limpiar + alinear palabras ----------
def alinear(texto, words):
    """Asigna tiempos de Whisper a las palabras del guion (con puntuación original)."""
    guion = texto.split()
    g_norm = [normaliza(w) for w in guion]
    # tokens del guion normalizados (una palabra puede dar 0..n tokens)
    g_tok, g_own = [], []
    for gi, gn in enumerate(g_norm):
        for tk in gn.split():
            g_tok.append(tk)
            g_own.append(gi)
    # tokens de whisper con tiempo repartido (40.000 -> cuarenta mil)
    h_tok, h_t = [], []
    for w in words:
        toks = normaliza(w.word).split()
        for k, tk in enumerate(toks):
            a = w.start + (w.end - w.start) * k / len(toks)
            b = w.start + (w.end - w.start) * (k + 1) / len(toks)
            h_tok.append(tk)
            h_t.append((a, b))
    t_s = [None] * len(guion)
    t_e = [None] * len(guion)
    sm = difflib.SequenceMatcher(a=g_tok, b=h_tok, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            gi = g_own[blk.a + k]
            a, b = h_t[blk.b + k]
            t_s[gi] = a if t_s[gi] is None else min(t_s[gi], a)
            t_e[gi] = b if t_e[gi] is None else max(t_e[gi], b)
    # interpolar huecos
    known = [i for i in range(len(guion)) if t_s[i] is not None]
    for i in range(len(guion)):
        if t_s[i] is None:
            prev = max([k for k in known if k < i], default=None)
            nxt = min([k for k in known if k > i], default=None)
            a = t_e[prev] if prev is not None else 0.0
            b = t_s[nxt] if nxt is not None else a + 0.3
            t_s[i], t_e[i] = a, max(a + 0.05, b)
    return [dict(w=guion[i], s=round(float(t_s[i]), 3), e=round(float(t_e[i]), 3)) for i in range(len(guion))]


meter = pyln.Meter(SR_OUT)
palabras = {}
for key, (n, m) in elegidas.items():
    y, sr = librosa.load(f"voz/cands/{n}", sr=None)
    y = librosa.resample(y, orig_sr=sr, target_sr=SR_OUT, res_type="soxr_vhq")
    # recorte de silencios: 40 ms antes, 120 ms después
    iv = librosa.effects.split(y, top_db=45, frame_length=2048, hop_length=256)
    a = max(0, iv[0][0] - int(0.04 * SR_OUT))
    b = min(len(y), iv[-1][1] + int(0.12 * SR_OUT))
    y = y[a:b].astype(np.float64)
    fi, fo = int(0.006 * SR_OUT), int(0.05 * SR_OUT)
    y[:fi] *= np.linspace(0, 1, fi)
    y[-fo:] *= np.linspace(1, 0, fo) ** 2
    y = pyln.normalize.loudness(y, meter.integrated_loudness(y), -20.0)
    out = f"voz/final/{key}.wav"
    sf.write(out, y.astype(np.float32), SR_OUT, subtype="FLOAT")
    prompt = "Número uno: dejar tu huella. Número dos." if textos[key].startswith("Número") else None
    segs, _ = wm.transcribe(out, language=IDIOMA, beam_size=5, word_timestamps=True, initial_prompt=prompt)
    words = [w for s in segs for w in s.words]
    palabras[key] = dict(dur=round(len(y) / SR_OUT, 3), take=n, cer=round(m["cer"], 4),
                         sim=round(m["sim"], 4), words=alinear(textos[key], words))
    print(f"{key:14s} {n:22s} dur={len(y)/SR_OUT:5.2f}s cer={m['cer']:.3f} sim={m['sim']:.3f}")

json.dump(palabras, open("voz/palabras.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
tot = sum(p["dur"] for p in palabras.values())
print(f"Voz total: {tot:.1f} s")
