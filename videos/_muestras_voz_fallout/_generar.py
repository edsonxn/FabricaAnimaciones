# -*- coding: utf-8 -*-
"""Muestras de voz para Radio Yermo (canal de Fallout, 17-nov-2026): el narrador es «el Locutor» de una radio que transmite
desde el Yermo. Misma frase para todas (dato real: el Refugio 108 de Fallout 3, lleno de clones de Gary), turbo, cuenta 2.
Sin voces de otros canales (Damián, Alberto, Alejandro Durán, Carlos Aguilar, Johnny, JC, Hope...). Uso: python _generar.py"""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

MODELO = "eleven_v4_turbo"
TEXTO = ("Buenos días, Yermo. [short pause] Aquí Radio Yermo, transmitiendo desde lo que queda del mundo. [short pause] "
         "Hoy: el Refugio donde todos se llaman Gary. [short pause] Todos. [long pause] "
         "[sarcastic] Y tú pensabas que tu familia era rara.")
VOCES = {   # nombre: voice_id (biblioteca /v1/shared-voices?language=es&search=locutor|radio|announcer)
    "00_profeta_ref": "HNSF1CTQmub252yhXROX",      # el Profeta (Tamriel y Runa): referencia, NO candidata
    "01_jose": "y2ijeTfmnXjzheHO6zeN",             # Jose - Pleasant announcer's voice (México, grave)
    "02_zabra": "9XaoraKgpXhItOQktYsV",            # Zabra - Energetic and Engaging Announcer (México, radio comercial)
    "03_juan_pablo": "5kz7Te3c1BvAWyFfkfkW",       # Juan Pablo - locutor/narrador mexicano, acento norteño
    "04_brian": "Czw3Dn181ypdrCOnPfif",            # Brian C - Clean, professional, warm (Latinoamérica)
    "05_bardo": "AZnNufbTTeexeFdpIeLN",            # Bardo Limon - Sonorous and Sincere (Latinoamérica)
    "06_carlos_pro": "gBTPbHzRd0ZmV75Z5Zk4",       # Carlos Pro - Argentinian Documentary & Radio
}
AQUI = os.path.dirname(os.path.abspath(__file__))
E._activa = next(i for i, (n, _) in enumerate(E.cuentas()) if n == 2)
total = 0
for nombre, vid in VOCES.items():
    ruta = os.path.join(AQUI, f"{nombre}.mp3")
    if os.path.exists(ruta):
        continue
    r = E.post(f"text-to-speech/{vid}?output_format=mp3_44100_128", timeout=120,
               json=dict(text=TEXTO, model_id=MODELO, seed=7, language_code="es", voice_settings=dict(stability=0.5)))
    if r.status_code != 200:
        print(nombre, "ElevenLabs", r.status_code, r.text[:200], flush=True)
        continue
    open(ruta, "wb").write(r.content)
    c = int(r.headers.get("character-cost") or 0)
    total += c
    print(nombre, "costo", c, flush=True)
print("créditos gastados", total, "· saldos", E.saldos())
