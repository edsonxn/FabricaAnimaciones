# Lista las frases rechazadas por `seleccionar` con su CER, cola y lo que oyó Whisper (para fijar umbrales por frase).
import json, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "voz")
e = json.load(open(os.path.join(D, "eval.json"), encoding="utf-8"))
r = json.load(open(os.path.join(D, "regenerar.json"), encoding="utf-8"))
sys.stdout.reconfigure(encoding="utf-8")
for k in r:
    v = e.get(k + "_s1.wav", {})
    print(f"{k:14s} cer={v.get('cer', -1):.3f} cola={v.get('tail_ratio', -1):.2f} gap={v.get('gap_max', -1):.2f} | {v.get('hyp', '')[:150]}")
