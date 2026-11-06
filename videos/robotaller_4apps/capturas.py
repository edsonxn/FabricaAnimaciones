# -*- coding: utf-8 -*-
"""Grabaciones REALES de las 4 apps (capturas/*.mp4) con la API tapada por robotaller.grabar_real. Base: videos/robotaller_n64/capturas.py.
Sesiones de D:\\Escaner (índice de eventos: `python eventos.py` → capturas/eventos_<n>.txt). La API del panel solo manda los 160 últimos
eventos, así que el filtro `solo()` pone los de la sesión completa leídos aquí con agente_vivo (enmascara se aplica después igual).
  python capturas.py [nombre ...]      python capturas.py hoja [nombre ...]"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, "../../nucleo")
import robotaller as R
from eventos import sid, todos

ALT, APPS, IDEAS, AUTO = sid("30a418d2-"), sid("fecd0d1d-"), sid("5023f72b-"), sid("bd7d4bbf-")
_EV = {}


def vivo(s):
    return f"/v2/vivo?sesion={s}"


SOLO_PANTALLA = """#cab,#ses,#etapas,#etaInfo,#lado,#pie{display:none!important}#taller{position:fixed!important;left:-4000px!important;width:1000px!important;height:300px!important}
body{display:block!important;overflow:hidden}#cuerpo{display:block!important;height:100vh!important;padding:0!important}#monitor{height:100vh!important;zoom:1.45;border:0!important}"""
RELOJ = "(()=>{const e=S.ev[S.idx];return e?[e.seq,e.tipo,e.titulo]:null})()"
JEFE = "setInterval(()=>document.querySelectorAll('#mcuerpo *').forEach(x=>{if(!x.children.length&&x.textContent.trim().toUpperCase()==='TÚ')x.textContent='EL JEFE';}),40);"
# privado de estas sesiones: nombre de la wifi, nombre de la tele, IPs, código y puerto de vinculación, dominio, modelo/año del carro y nombre de la app
PRIVADO = re.compile(r"Casa\s+I[nñ]iguez|Cuarto\s+Zyan[^\"]*|192\.168[\w.{}…]*|\b0\.18\d\b|\b44495\b|\b203330\b|clicknbusiness\.com\.mx[^\s\"]*|Zyan"
                     r"|altima\s*scan|altima|nissan|(?<!\d)2007(?!\d)|4\s*puertas|(?<![\d.])2[.,]5\s*L(?![a-z])|QR25\w*", re.I)   # 5-nov: ni modelo ni año del carro (pedido del usuario)


def tapa(x):
    if isinstance(x, str):
        return PRIVADO.sub("▒▒▒", x)
    if isinstance(x, list):
        return [tapa(y) for y in x]
    if isinstance(x, dict):
        return {k: tapa(v) for k, v in x.items()}
    return x


def solo(s, de, a):
    """Solo esos eventos de la sesión (completa, no los 160 de la API): lo de antes y lo de después no sale."""
    if s not in _EV:
        _EV[s] = todos(s)
    def filtra(u, datos):
        if "/api/v2/agente" in u and isinstance(datos, dict) and "eventos" in datos:
            datos["eventos"] = [_EV[s][k] for k in sorted(_EV[s]) if de <= k <= a]
        return tapa(datos)
    return filtra


def repaso(seq, vel=1):
    return f"(()=>{{S.vel={vel};irA({seq});}})()"


def uno(s, seq, dur, imagenes=False):
    return dict(url=vivo(s), sesion=s, dur=dur, css=SOLO_PANTALLA, imagenes=imagenes, cuadro=solo(s, seq, seq), espera=8, acciones=[dict(t=.1, js=JEFE + repaso(seq, .5))])


def tramo(s, de, a, ir, vel, dur, imagenes=False):
    return dict(url=vivo(s), sesion=s, dur=dur, css=SOLO_PANTALLA, imagenes=imagenes, cuadro=solo(s, de, a), reloj=RELOJ, espera=8,
                acciones=[dict(t=.2, js=JEFE + repaso(ir, vel))])


def ui(app):
    return "file:///" + os.path.abspath(f"capturas/ui/{app}/index.html").replace("\\", "/")


def tele(modo):
    return "file:///" + os.path.abspath("capturas/tele/tele.html").replace("\\", "/") + "#" + modo


TOMAS = {
    # Altima Scan (3-nov)
    "alt_pide": lambda: uno(ALT, 1, 7),
    "alt_codigo": lambda: tramo(ALT, 2, 47, 8, 2.5, 14),
    "alt_falla": lambda: uno(ALT, 84, 6),
    "alt_registro": lambda: uno(ALT, 119, 7),
    "alt_versiones": lambda: tramo(ALT, 109, 166, 110, 3, 14),
    "alt_funciona": lambda: uno(ALT, 167, 6),
    "alt_alertas": lambda: tramo(ALT, 169, 245, 172, 3, 12),
    # MicWiFi y Rayo (4-nov, mañana)
    "mic_pide": lambda: uno(APPS, 1, 7),
    "mic_codigo": lambda: tramo(APPS, 2, 50, 10, 2.5, 12),
    "mic_firewall": lambda: tramo(APPS, 68, 88, 69, 1.2, 10),
    "mic_jala": lambda: uno(APPS, 88, 5),
    "rayo_pide": lambda: uno(APPS, 91, 7),
    "rayo_codigo": lambda: tramo(APPS, 92, 165, 97, 3, 12),
    # Puente TV
    "tv_pide": lambda: uno(APPS, 187, 7),
    "tv_codigo": lambda: tramo(APPS, 188, 265, 195, 3, 12),
    "tv_prueba": lambda: tramo(APPS, 276, 340, 280, 2, 12),
    "ideas_pide": lambda: uno(IDEAS, 1, 6),
    "ideas_no": lambda: uno(IDEAS, 3, 8),
    "ideas_tele": lambda: tramo(IDEAS, 25, 136, 54, 3, 12),
    # la APK nueva del carro, por Rayo
    "auto_rayo": lambda: tramo(AUTO, 1, 47, 23, 1, 10),
    # la tele SIMULADA (tele.py): el aviso real de las 12:35 con el robot, la sala de revisión y el protector
    "tele_aviso": lambda: dict(url=tele("aviso"), dur=11, espera=.2, imagenes=True),
    "tele_revision": lambda: dict(url=tele("revision"), dur=9, espera=.6, imagenes=True),
    "tele_protector": lambda: dict(url=tele("protector"), dur=8, espera=.6, imagenes=True),
    # escritorio (interfaces reales con datos de demostración limpios)
    "rayo_pc": lambda: dict(url=ui("rayo"), dur=14, espera=1.0, w=1100, h=720, escala=2.0),
    "puente_pc": lambda: dict(url=ui("puente"), dur=10, espera=1.0, w=1280, h=800, escala=1.6,
                              acciones=[dict(t=2.5, js="(()=>{const t=document.querySelector('#titulo');if(t){t.value='';t.dispatchEvent(new Event('input'))}})()")]),
}


def hoja(n):
    salida = f"previews/cap_{n}.jpg"
    dur = float(subprocess.run([R.FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"capturas/{n}.mp4"],
                               capture_output=True, text=True).stdout)
    subprocess.run([R.FFMPEG, "-y", "-loglevel", "error", "-i", f"capturas/{n}.mp4", "-vf", f"fps=6/{dur:.2f},scale=640:-1,tile=2x3", "-frames:v", "1", salida], check=True)
    print(salida)


if __name__ == "__main__":
    pide = sys.argv[1:] or list(TOMAS)
    if pide[0] == "hoja":
        for n in pide[1:] or TOMAS:
            hoja(n)
        sys.exit()
    os.makedirs("previews", exist_ok=True)
    for n in pide:
        t = TOMAS[n]()
        R.grabar_real(f"capturas/{n}.mp4", t["url"], t["dur"], t.get("acciones", ()), w=t.get("w", 1600), h=t.get("h", 900), escala=t.get("escala", 1.5),
                      sesion=t.get("sesion"), espera=t.get("espera", 2.0), imagenes=t.get("imagenes", False), css=t.get("css", ""), cuadro=t.get("cuadro"), reloj=t.get("reloj"))
        hoja(n)
