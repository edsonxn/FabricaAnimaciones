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
from qa import SpeakerSim, artefactos, cer, normaliza, silenciar_arranque

SR_OUT = 48000
CER_MAX = 0.012
GAP_MAX = 0.65
TAIL_MAX = 0.35
PEAK_MAX = 1.25
# Umbral de cola por frase (guion.py: TAIL_MAX_POR_FRASE = {"escena_i": 0.40}) para frases que terminan hablando hasta el final
# (CER 0 en todas las tomas, pero el último 8 % tiene voz). Úsalo solo tras comprobar que la transcripción termina bien.
try:
    import guion as _g
    _TAIL_POR_FRASE = dict(getattr(_g, "TAIL_MAX_POR_FRASE", {}))
    _CER_POR_FRASE = dict(getattr(_g, "CER_MAX_POR_FRASE", {}))   # nombres propios que Whisper escribe distinto (Geoffrey -> Jeffrey)
    _IDIOMA_LIBRE = set(getattr(_g, "IDIOMA_LIBRE", []))           # frases oídas y aceptadas aunque Whisper dude del idioma
    _GAP_POR_FRASE = dict(getattr(_g, "GAP_MAX_POR_FRASE", {}))    # pausa larga a propósito tras un punto («…nada. La era…»)
except Exception:
    _TAIL_POR_FRASE, _CER_POR_FRASE, _IDIOMA_LIBRE, _GAP_POR_FRASE = {}, {}, set(), {}
# Applio (Edge TTS multilingüe) puede leer una frase entera con acento de otro idioma (13-oct-2026: «Oficialmente.» en
# portugués, «Guarda ese dato.» en italiano): Whisper sin idioma forzado; p(idioma del guion) < P_IDIOMA_MIN = se reescribe
P_IDIOMA_MIN = 0.90
MIRAR_IDIOMA = config.VOZ.get("motor") == "applio"
# ElevenLabs entrega la toma recortada justo al acabar la voz y no alucina colas: el filtro de cola (pensado para Chatterbox) no aplica
if config.VOZ.get("motor") == "elevenlabs":
    TAIL_MAX = 1.0
    if config.FRASES_TTS:   # etiquetas [pause], [sighs]… meten silencios a propósito dentro de la frase
        GAP_MAX = 2.5
elif config.VOZ.get("motor") == "applio":   # Edge TTS + RVC tampoco alucina colas
    TAIL_MAX = 1.0

os.makedirs("voz/final", exist_ok=True)
evals = json.load(open("voz/eval.json", encoding="utf-8")) if os.path.exists("voz/eval.json") else {}

# FAB_WHISPER_CPU=1: evaluar en CPU cuando otra sesión ocupa la GPU con Chatterbox (voz de ElevenLabs/Applio, 19-oct-2026)
_CPU = bool(os.environ.get("FAB_WHISPER_CPU"))
wm = WhisperModel("large-v3", device="cpu" if _CPU else "cuda", compute_type="int8" if _CPU else "float16")
spk = SpeakerSim(config.VOZ["referencia"], device="cpu" if _CPU else "cuda")
IDIOMA = config.VOZ["idioma"]
textos = {f"{e['id']}_{i}": t for e in config.ESCENAS for i, t in enumerate(e["frases"])}
# con FONETICA (Applio) Whisper puede escribir la grafía real o la fonética: vale la que menos errores dé
_fon = {k: re.sub(r"\s*\[[A-Za-z][A-Za-z' -]*\]\s*", " ", t).strip() for k, t in config.FRASES_TTS.items()}
def cer_frase(key, hyp):
    return min(cer(textos[key], hyp), cer(_fon[key], hyp)) if key in _fon else cer(textos[key], hyp)

# ---------- 1) evaluar candidatos ----------
for path in sorted(glob.glob("voz/cands/*.wav")):
    name = os.path.basename(path)
    if name in evals:
        continue
    key = re.sub(r"_s\d+\.wav$", "", name)
    y, sr = librosa.load(path, sr=None)
    segs, _ = wm.transcribe(path, language=IDIOMA, beam_size=5, vad_filter=False)
    hyp = " ".join(s.text for s in segs).strip()
    evals[name] = dict(key=key, hyp=hyp, cer=cer_frase(key, hyp), sim=spk.sim(y, sr),
                       dur=len(y) / sr, **artefactos(y, sr))
    if MIRAR_IDIOMA:   # solo la detección de idioma (los segmentos no se decodifican)
        _, info = wm.transcribe(path, language=None, beam_size=1)
        evals[name]["p_idioma"] = round(dict(info.all_language_probs or []).get(IDIOMA, 0.0), 3)
    json.dump(evals, open("voz/eval.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# la CER se recalcula desde la transcripción guardada (así una mejora de qa.normaliza aplica a tomas viejas)
for m in evals.values():
    if m["key"] in textos:
        m["cer"] = cer_frase(m["key"], m["hyp"])

# ---------- 2) elegir ----------
elegidas, fallan = {}, []
for key in textos:
    cands = [(n, m) for n, m in evals.items() if m["key"] == key]
    if not cands:
        fallan.append(key)
        continue
    med = float(np.median([m["dur"] for _, m in cands]))
    tmax = _TAIL_POR_FRASE.get(key, TAIL_MAX)
    cmax = _CER_POR_FRASE.get(key, CER_MAX)
    gmax = _GAP_POR_FRASE.get(key, GAP_MAX)
    ok = [(n, m) for n, m in cands
          if m["cer"] <= cmax and m["gap_max"] <= gmax and m["tail_ratio"] <= tmax
          and m["peak"] <= PEAK_MAX
          and (key in _IDIOMA_LIBRE or m.get("p_idioma", 1.0) >= P_IDIOMA_MIN)]
    if not ok:
        fallan.append(key)
        otro = [m for _, m in cands if m.get("p_idioma", 1.0) < P_IDIOMA_MIN]
        if otro and key not in _IDIOMA_LIBRE:
            print(f"{key}: suena a OTRO IDIOMA (p({IDIOMA}) = {otro[0]['p_idioma']:.2f}): reescribe la frase (más larga, sin "
                  f"palabras en inglés: FONETICA) o, si al oírla está bien, IDIOMA_LIBRE = [\"{key}\"] en guion.py")
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
# misma toma ya limpiada y alineada en una pasada anterior: se reutiliza (19-oct-2026: realinear 86 frases en CPU eran ~40 min)
_prev = json.load(open("voz/palabras.json", encoding="utf-8")) if os.path.exists("voz/palabras.json") else {}
for key, (n, m) in elegidas.items():
    _fin = f"voz/final/{key}.wav"
    if (_prev.get(key, {}).get("take") == n and os.path.exists(_fin)
            and os.path.getmtime(_fin) >= os.path.getmtime(f"voz/cands/{n}")):
        palabras[key] = _prev[key]
        continue
    y, sr = librosa.load(f"voz/cands/{n}", sr=None)
    y = librosa.resample(y, orig_sr=sr, target_sr=SR_OUT, res_type="soxr_vhq")
    # recorte de silencios: 40 ms antes, 120 ms después
    iv = librosa.effects.split(y, top_db=45, frame_length=2048, hop_length=256)
    a = max(0, iv[0][0] - int(0.04 * SR_OUT))
    b = min(len(y), iv[-1][1] + int(0.12 * SR_OUT))
    y = y[a:b].astype(np.float64)
    y_entera = y.copy()
    y, mudo = silenciar_arranque(y, SR_OUT)           # sonido suelto antes de la 1.ª palabra (Whisper no lo ve)
    if mudo:
        # una 1.ª palabra corta seguida de pausa («Hoy, Jalisco…», historia_jalisco 22-oct-2026) parece un sonido suelto:
        # si sin ese bloque Whisper ya no oye la primera palabra del guion, no se silencia
        _p0 = normaliza(textos[key]).split()[:1]
        _tmp = f"voz/final/_{key}_prueba.wav"
        sf.write(_tmp, y.astype(np.float32), SR_OUT, subtype="FLOAT")
        _s, _ = wm.transcribe(_tmp, language=IDIOMA, beam_size=5)
        _h = normaliza(" ".join(s_.text for s_ in _s)).split()[:1]
        os.remove(_tmp)
        if _p0 and _h != _p0:
            y, mudo = y_entera, 0.0
            print(f"{key}: el bloque inicial era la primera palabra («{_p0[0]}»): no se silencia")
    if mudo:
        print(f"{key}: silenciado un sonido de {mudo:.2f} s antes de la primera palabra")
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
