import json, glob, os, sys, datetime as dt
sys.stdout.reconfigure(encoding="utf-8")
RAIZ = r"C:\FabricaAnimaciones"
sys.path.insert(0, os.path.join(RAIZ, "nucleo"))
import comentarios as C
SC = r"C:\Users\jaire\AppData\Local\Temp\claude\26726f8e7372f46b\2939ffe9-a907-4801-89d2-7bf6a1ae8f05\scratchpad\coms"
todos = {}
for f in glob.glob(os.path.join(SC, "*.info.json")):
    v = os.path.basename(f)[:-10]
    for c in (json.load(open(f, encoding="utf-8")).get("comments") or []):
        todos[c["id"]] = (v, c)
ELEGIDOS = [
    ("UgyfsqiFpG-ocppdEmN4AaABAg", "gracias"), ("Ugxm0BexIA_d7ty1HF54AaABAg", "gracias"),
    ("UgwKD0JApPpOgDfT78B4AaABAg", "gracias"), ("Ugz5rM7rve9QGhwUCfx4AaABAg", "gracias"),
    ("UgzWl9poevS3JGJCtC94AaABAg", "gracias"), ("Ugy-UKbNNHTtd2gvZoh4AaABAg", "gracias"),
    ("UgyRkfTi4B-tmyRUv2x4AaABAg", "critica"), ("UgyjsR8HwH1-pqeCJDx4AaABAg", "critica"),
    ("Ugw8yWeW4gGL5RV9cGd4AaABAg", "justa"), ("UgylfoAksU65kLRLMiZ4AaABAg", "justa"),
    ("UgysFDPHvpklcAUidy54AaABAg", "justa"),
]
usados = set()
for f in glob.glob(os.path.join(RAIZ, "videos", "*", "investigacion", "comentarios.json")):
    if "tl_josedeodo" not in f:
        usados |= {x["id"] for x in json.load(open(f, encoding="utf-8"))}
for p in glob.glob(os.path.join(RAIZ, "videos", "*", "pegatinas", "com_*.png")):
    if "tl_josedeodo" not in p:
        usados.add(os.path.basename(p)[4:-4])
out = []
for i, tipo in ELEGIDOS:
    assert i not in usados, i
    v, c = todos[i]
    fecha = str(dt.datetime.utcfromtimestamp(c["timestamp"]).date())
    assert fecha >= "2026-11-15", (i, fecha)
    out.append(dict(id=i, autor=c["author"], avatar=c.get("author_thumbnail"), fecha=fecha,
                    likes=c.get("like_count") or 0, texto=c["text"], tipo=tipo, video=v))
dst = os.path.join(RAIZ, "videos", "tl_josedeodo")
os.makedirs(os.path.join(dst, "investigacion"), exist_ok=True)
json.dump(out, open(os.path.join(dst, "investigacion", "comentarios.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for c in out:
    if c["tipo"] == "sugerencia":
        continue
    s = C.tarjeta(c, os.path.join(dst, "pegatinas", f"com_{c['id']}.png"))
    print(c["tipo"], c["autor"], c["fecha"], c["likes"], s)
