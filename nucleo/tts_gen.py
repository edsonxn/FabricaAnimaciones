# -*- coding: utf-8 -*-
"""Genera candidatos de voz (Chatterbox Multilingual v3 + voz de Dan).

Uso: python tts_gen.py --seeds 1 2 3 4 [--solo manos_1 ligar_2 ...]
Salta los archivos ya existentes, así se puede relanzar para regenerar faltantes.
"""
import argparse
import glob
import json
import os

import config

def todas_las_frases():
    return [(e["id"], i, f) for e in config.ESCENAS for i, f in enumerate(e["frases"])]
OUT = "voz/cands"

ap = argparse.ArgumentParser()
ap.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4])
ap.add_argument("--solo", nargs="*", default=None)
args = ap.parse_args()

os.makedirs(OUT, exist_ok=True)

# si el texto de una frase cambió en guion.py, sus tomas viejas ya no sirven: borrarlas
actuales = {f"{e}_{i}": config.FRASES_TTS.get(f"{e}_{i}", t) for e, i, t in todas_las_frases()}   # con corchetes: cambiar una etiqueta también regenera
prev = json.load(open("voz/textos.json", encoding="utf-8")) if os.path.exists("voz/textos.json") else {}
cambiadas = [k for k, t in actuales.items() if k in prev and prev[k] != t]
if cambiadas:
    print("texto cambiado, se regeneran:", cambiadas)
    ev = json.load(open("voz/eval.json", encoding="utf-8")) if os.path.exists("voz/eval.json") else {}
    for k in cambiadas:
        for f in glob.glob(f"{OUT}/{k}_s*.wav"):
            os.remove(f)
        ev = {n: m for n, m in ev.items() if m.get("key") != k}
    json.dump(ev, open("voz/eval.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(actuales, open("voz/textos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
if config.VOZ.get("motor") == "elevenlabs":
    import tts_eleven
    tts_eleven.generar(todas_las_frases(), args.seeds, args.solo, OUT)
    raise SystemExit
if config.VOZ.get("motor") == "applio":
    import tts_applio
    tts_applio.generar(todas_las_frases(), args.seeds, args.solo, OUT)
    raise SystemExit

REF = config.VOZ["referencia"]
IDIOMA = config.VOZ["idioma"]
CFG = {k: config.VOZ[k] for k in ("exaggeration", "cfg_weight", "temperature")}

import torch
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

model = ChatterboxMultilingualTTS.from_pretrained(device="cuda", t3_model="v3")
model.prepare_conditionals(REF, exaggeration=CFG["exaggeration"])

import re

for esc, idx, texto in todas_las_frases():
    key = f"{esc}_{idx}"
    if args.solo and key not in args.solo:
        continue
    # FONETICA de guion.py (config.FRASES_TTS): hasta el 20-oct-2026 Chatterbox leía SIEMPRE la grafía real y la fonética no le
    # llegaba (solo a Applio/ElevenLabs). Sin las etiquetas [..] de ElevenLabs, que Chatterbox leería en voz alta.
    texto_tts = re.sub(r"\s*\[[A-Za-z][A-Za-z' -]*\]\s*", " ", config.FRASES_TTS.get(key, texto)).strip()
    for seed in args.seeds:
        path = f"{OUT}/{key}_s{seed}.wav"
        if os.path.exists(path):
            continue
        torch.manual_seed(seed * 1000 + idx)
        wav = model.generate(texto_tts, language_id=IDIOMA, **CFG)
        ta.save(path, wav, model.sr)
        print(path, round(wav.shape[-1] / model.sr, 2), flush=True)
