"""python _t.py escena [f1 f2 ...] -> instantes absolutos: fracción 0..1 del tramo de la escena (por defecto 0.1 .. 0.9)."""
import sys, json
t = json.load(open('timeline.json', encoding='utf-8'))
e = {x['id']: x for x in t['escenas']}[sys.argv[1]]
fr = [float(a) for a in sys.argv[2:]] or [0.1, 0.25, 0.4, 0.55, 0.7, 0.9]
print(' '.join(f"{e['t0'] + f * (e['t1'] - e['t0']):.2f}" for f in fr))
