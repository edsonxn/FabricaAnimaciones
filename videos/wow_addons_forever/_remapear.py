"""Reacomoda los clips ya bajados a los beats NUEVOS (tras mover la escena «voces», 6-nov-2026) por parecido de texto.
Uso: python _remapear.py <carpeta con beats/busquedas/fuentes viejos>  → escribe medios/scene-NNN.mp4 nuevos, fuentes.json,
busquedas.json y _pendientes.txt (beats sin clip suficiente: se bajan con `bajar <ids>` usando url+desde del clip viejo)."""
import json, os, re, shutil, subprocess, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
V = sys.argv[1]
nb = json.load(open("beats.json", encoding="utf-8"))
ob = json.load(open(os.path.join(V, "beats.json"), encoding="utf-8"))
obq = json.load(open(os.path.join(V, "busquedas.json"), encoding="utf-8"))
of = json.load(open(os.path.join(V, "fuentes.json"), encoding="utf-8"))
pal = lambda t: set(re.findall(r"\w+", t.lower()))
VIEJO = "medios/_viejo"
os.makedirs(VIEJO, exist_ok=True)
for b in ob:
    src = f"medios/{b['id']}.mp4"
    if os.path.exists(src):
        shutil.move(src, f"{VIEJO}/{b['id']}.mp4")


def dur(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


usados, mapa, pend = set(), {}, []
for b in nb:
    pw = pal(b["texto"])
    mejor, ms = None, 0.0
    for o in ob:
        if o["id"] in usados:
            continue
        ow = pal(o["texto"])
        s = len(pw & ow) / max(1, len(pw | ow))
        if s > ms:
            mejor, ms = o, s
    if mejor and ms >= 0.35:
        mapa[b["id"]] = (mejor["id"], round(ms, 2))
        usados.add(mejor["id"])
# beats sin pareja (la escena «voces» nueva): clips viejos que sobraron, en orden
sobran = [o["id"] for o in ob if o["id"] not in usados]
for b in nb:
    if b["id"] not in mapa and sobran:
        mapa[b["id"]] = (sobran.pop(0), 0.0)
nf = {k: v for k, v in of.items() if k.startswith("_") and k != "_rechazados"}
nf["_rechazados"] = {}
nq = {}
for b in nb:
    n = b["id"]
    o, s = mapa.get(n, (None, 0))
    if o is None:
        nq[n] = ["WoW Forever no commentary"]
        pend.append(n)
        continue
    nq[n] = obq.get(o, ["WoW Forever no commentary"])
    if o in of:
        nf[n] = of[o]
    if o in of.get("_rechazados", {}):
        nf["_rechazados"][n] = of["_rechazados"][o]
    f = f"{VIEJO}/{o}.mp4"
    nec = b["t1"] - b["t0"] + 0.3
    if os.path.exists(f) and dur(f) >= nec - 0.05:
        shutil.copy(f, f"medios/{n}.mp4")
    else:
        pend.append(n)
        if o in of and of[o].get("video"):
            nq[n] = {"url": "https://youtu.be/" + of[o]["video"], "desde": of[o].get("desde", 0)}
    print(n, "<-", o, s, "" if n not in pend else "PENDIENTE")
json.dump(nq, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(nf, open("fuentes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open("_pendientes.txt", "w").write(",".join(str(int(p[6:])) for p in pend))
print("pendientes:", ",".join(p[6:] for p in pend))
