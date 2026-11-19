# -*- coding: utf-8 -*-
"""Vigila el reel en Meta (sin imprimir el token): avisa cuando termina de procesar y cuando sale publicado (o si falla)."""
import json, subprocess, sys, time, datetime
import requests
VID = "1839179620463556"
env = dict(l.strip().split("=", 1) for l in open("E:/PaginaFace/paginas/noticias_jch/.env", encoding="utf-8") if "=" in l and not l.startswith("#"))
TOK = env["FB_PAGE_TOKEN"]
LIMITE = datetime.datetime(2026, 11, 19, 19, 40)
avisado_listo = False


def avisar(t):
    print(datetime.datetime.now().strftime("%H:%M"), t, flush=True)
    subprocess.run([sys.executable, "C:/FabricaAnimaciones/fab.py", "avisar", t], cwd="C:/FabricaAnimaciones")


while datetime.datetime.now() < LIMITE:
    try:
        d = requests.get(f"https://graph.facebook.com/v21.0/{VID}", params={"fields": "status,published,permalink_url",
                         "access_token": TOK}, timeout=30).json()
    except Exception as e:
        time.sleep(120)
        continue
    st = d.get("status", {})
    if "error" in d or st.get("video_status") == "error" or st.get("processing_phase", {}).get("status") == "error":
        avisar("Ojo: Meta marcó error en el reel del pino azul. Revisa la consola.")
        print(json.dumps(st)[:500])
        sys.exit(1)
    if not avisado_listo and st.get("processing_phase", {}).get("status") == "complete":
        avisado_listo = True
        print(datetime.datetime.now().strftime("%H:%M"), "procesado:", st.get("video_status"), flush=True)
    if d.get("published"):
        avisar("El reel del pino azul ya salió en Noticias de Juchipila.")
        print("permalink:", d.get("permalink_url"))
        sys.exit(0)
    time.sleep(300 if avisado_listo else 60)
avisar("Ojo: el reel del pino azul no aparece publicado a las siete cuarenta. Hay que revisarlo.")
sys.exit(2)
