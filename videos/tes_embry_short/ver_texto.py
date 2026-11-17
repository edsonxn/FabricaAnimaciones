"""Imprime la transcripción Whisper de los clips (segmentos con tiempo dentro del clip).
Uso: python ver_texto.py [clave ...]"""
import glob, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "segmentos", "clips")
claves = sys.argv[1:] or sorted(os.path.basename(p)[:-11] for p in glob.glob(os.path.join(D, "*.words.json")))
for c in claves:
    print("=====", c)
    for s in json.load(open(os.path.join(D, c + ".words.json"), encoding="utf-8")):
        print("  %5.1f-%5.1f  %s" % (s["a"], s["b"], s["t"]))
