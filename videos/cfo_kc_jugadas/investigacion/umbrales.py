# Escribe en guion.py CER_MAX_POR_FRASE / TAIL_MAX_POR_FRASE = lo medido + margen para las frases de regenerar.json
# (transcripciones leídas: solo nombres mal oídos por Whisper). python investigacion/umbrales.py
import json, os, re
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
e = json.load(open(os.path.join(V, "voz", "eval.json"), encoding="utf-8"))
r = json.load(open(os.path.join(V, "voz", "regenerar.json"), encoding="utf-8"))
cer = {k: round(e[k + "_s1.wav"]["cer"] + .02, 3) for k in r}
cola = {k: round(e[k + "_s1.wav"]["tail_ratio"] + .1, 2) for k in r}
p = os.path.join(V, "guion.py")
t = open(p, encoding="utf-8").read()
for nom, d in (("CER_MAX_POR_FRASE", cer), ("TAIL_MAX_POR_FRASE", cola)):    # se SUMAN a los que ya había
    viejo = json.loads(re.search(nom + r" = (\{.*?\})\n", t, re.S).group(1))
    d.update({k: v for k, v in viejo.items() if k not in d})
t = re.sub(r"CER_MAX_POR_FRASE = \{.*?\}\n", "CER_MAX_POR_FRASE = " + json.dumps(cer) + "\n", t, count=1, flags=re.S)
t = re.sub(r"TAIL_MAX_POR_FRASE = \{.*?\}\n", "TAIL_MAX_POR_FRASE = " + json.dumps(cola) + "\n", t, count=1, flags=re.S)
open(p, "w", encoding="utf-8").write(t)
print(len(cer), "umbrales")
