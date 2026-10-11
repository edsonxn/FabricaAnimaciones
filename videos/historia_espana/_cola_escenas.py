# -*- coding: utf-8 -*-
"""Renderiza escenas fluidas en el motor de vista previa del panel, una tras otra (el motor solo admite un trabajo a la vez).
Uso: python _cola_escenas.py id1 id2 ...   -> el resultado queda en el panel (Escena fluida) y en _cola_escenas_log.txt."""
import json
import sys
import time
import urllib.error
import urllib.request

PANEL = "http://127.0.0.1:8765"
V = "historia_espana"
LOG = open(r"C:\FabricaAnimaciones\videos\historia_espana\_cola_escenas_log.txt", "a", encoding="utf-8")


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, file=LOG, flush=True)


def get(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def motor():
    for _ in range(60):
        d = get(f"{PANEL}/api/preview?video={V}")
        if d.get("estado") == "listo":
            return f"http://127.0.0.1:{d['puerto']}", f"token={d['token']}"
        time.sleep(3)
    raise RuntimeError("el motor no arrancó")


for esc in sys.argv[1:]:
    t0 = time.time()
    base, q = motor()
    while True:
        req = urllib.request.Request(f"{base}/escena?id={esc}&w=960&procs=12&forzar=1&{q}", method="POST")
        try:
            job = json.loads(urllib.request.urlopen(req, timeout=30).read().decode("utf-8"))["job"]
            break
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code == 409:                       # hay otro render en marcha: espera
                log(esc, "esperando:", msg[:80])
                time.sleep(20)
                base, q = motor()
                continue
            log(esc, "ERROR al lanzar:", e.code, msg[:200])
            sys.exit(1)
    log(esc, "lanzada, job", job)
    while True:
        time.sleep(5)
        try:
            s = get(f"{base}/escena/estado?job={job}&{q}")
        except Exception as e:                      # noqa: BLE001
            log(esc, "sin respuesta del motor:", e)
            continue
        if s.get("estado") != "trabajando":
            break
    log(esc, s.get("estado"), s.get("error", ""), f"{time.time() - t0:.0f} s")
    if s.get("estado") != "listo":
        sys.exit(1)
log("COLA TERMINADA")
