# -*- coding: utf-8 -*-
"""21-oct-2026: el guion pasó de 15 a 11 min quitando frases; las claves <escena>_<i> se corrieron. Renombra las tomas de
voz/cands y las entradas de voz/eval.json de la clave vieja a la nueva cuando el TEXTO es idéntico (voz/textos_15min.json)."""
import glob, json, os, shutil
import importlib.util as u
s = u.spec_from_file_location("g", "guion.py"); g = u.module_from_spec(s); s.loader.exec_module(g)
viejo = json.load(open("voz/textos_15min.json", encoding="utf-8"))
por_texto = {t: k for k, t in viejo.items()}
mapa = {}
for e in g.ESCENAS:
    for i, f in enumerate(e["frases"]):
        k = f"{e['id']}_{i}"
        if f in por_texto:
            mapa[por_texto[f]] = k
nuevas = [f"{e['id']}_{i}" for e in g.ESCENAS for i, f in enumerate(e["frases"]) if f not in por_texto]
print("reaprovechadas", len(mapa), "nuevas", nuevas)
tmp = "voz/_tmp"; os.makedirs(tmp, exist_ok=True)
for f in glob.glob("voz/cands/*.wav"):
    shutil.move(f, os.path.join(tmp, os.path.basename(f)))
ev = json.load(open("voz/eval.json", encoding="utf-8")); ev2 = {}
for f in glob.glob(tmp + "/*.wav"):
    n = os.path.basename(f); kv, sd = n.rsplit("_s", 1)
    if kv in mapa:
        nn = f"{mapa[kv]}_s{sd}"
        shutil.move(f, "voz/cands/" + nn)
        if n in ev:
            m = dict(ev[n]); m["key"] = mapa[kv]; ev2[nn] = m
    else:
        os.makedirs("voz/_descartadas", exist_ok=True); shutil.move(f, "voz/_descartadas/" + n)
os.rmdir(tmp)
json.dump(ev2, open("voz/eval.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({f"{e['id']}_{i}": f for e in g.ESCENAS for i, f in enumerate(e["frases"])},
          open("voz/textos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree("voz/final", ignore_errors=True)
for x in ("voz/palabras.json", "voz/regenerar.json"):
    if os.path.exists(x): os.remove(x)
