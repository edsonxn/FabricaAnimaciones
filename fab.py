# -*- coding: utf-8 -*-
"""Lanzador de la Fábrica de Animaciones.

  python fab.py nuevo <video>                   crea videos/<video> desde videos/_plantilla
  python fab.py <video> voz [--seeds 1 2 3 4]   genera tomas de voz con Chatterbox
  python fab.py <video> seleccionar             elige la mejor toma por frase (Whisper + similitud), alinea palabras
  python fab.py <video> tiempo                  construye timeline.json (BPM, escenas, transiciones)
  python fab.py <video> escena <id> <t> [t...]  hoja de prueba de una escena  -> previews/esc_<id>.jpg
  python fab.py <video> comprobar               chequeo rápido previo al render (nombres, anclas, un cuadro por fase)
  python fab.py <video> prueba <t> [t...]       cuadros finales (transiciones + subtítulos) -> previews/hoja_render.jpg
  python fab.py <video> estilos <t>             el mismo cuadro en todos los estilos -> previews/estilos.jpg
  python fab.py <video> catalogo                todos los íconos en el estilo del video -> previews/catalogo_iconos.png
  python fab.py <video> musica | sfx | mezcla   audio (música procedural, efectos, mezcla y máster)
  python fab.py <video> video [--procs 13]      render completo sin audio (reanuda: salta segmentos ya hechos)
  python fab.py <video> final                   MASTER.mp4 + subtítulos .srt (FAB_WHATSAPP=1 añade versión 720p)
  python fab.py <video> verificar               QA final: Whisper sobre la mezcla, duración, desfase A/V, hoja de cuadros
  python fab.py <video> todo                    voz→seleccionar→tiempo→musica→sfx→mezcla→video→final
  python fab.py <video> limpiar                 borra segmentos/previews (regenerables)
  python fab.py api                             regenera API.md
"""
import json
import os
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.join(RAIZ, "nucleo")
VIDEOS = os.path.join(RAIZ, "videos")

ETAPAS = {
    "voz": ["-m", "tts_gen"], "seleccionar": ["-m", "tts_select"], "tiempo": ["-m", "linea_tiempo"],
    "escena": ["-m", "prueba_escena"], "prueba": ["-m", "render", "prueba"], "video": ["-m", "render", "video"],
    "musica": ["-m", "musica"], "sfx": ["-m", "sfx"], "mezcla": ["-m", "mezcla"], "final": ["-m", "final"],
    "estilos": ["-m", "muestra_estilos"], "catalogo": ["-m", "catalogo"], "verificar": ["-m", "verificar"],
    "comprobar": ["-m", "comprobar"], "miniatura": ["-m", "miniatura"],
}


def correr(video, etapa, extra):
    carpeta = os.path.join(VIDEOS, video)
    if not os.path.isfile(os.path.join(carpeta, "guion.py")):
        sys.exit(f"No existe {carpeta}\\guion.py  (usa: python fab.py nuevo {video})")
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([carpeta, NUCLEO])
    env["PYTHONIOENCODING"] = "utf-8"
    cmd = [sys.executable] + ETAPAS[etapa] + list(extra)
    print(f"\n=== [{video}] {etapa} ===", flush=True)
    r = subprocess.run(cmd, cwd=carpeta, env=env)
    if r.returncode != 0:
        sys.exit(f"La etapa '{etapa}' falló (código {r.returncode}).")


def todo(video):
    carpeta = os.path.join(VIDEOS, video)
    correr(video, "voz", [])
    for ronda, seeds in enumerate((["5", "6", "7", "8"], ["9", "10", "11", "12"])):
        correr(video, "seleccionar", [])
        reg = json.load(open(os.path.join(carpeta, "voz", "regenerar.json"), encoding="utf-8"))
        if not reg:
            break
        print(f"Frases a regenerar (ronda {ronda + 1}): {reg}")
        correr(video, "voz", ["--seeds", *seeds, "--solo", *reg])
    else:
        correr(video, "seleccionar", [])
        reg = json.load(open(os.path.join(carpeta, "voz", "regenerar.json"), encoding="utf-8"))
        if reg:
            sys.exit(f"Estas frases no pasan el control de calidad tras 12 tomas: {reg}. Reescríbelas en guion.py.")
    for etapa in ("tiempo", "comprobar", "musica", "sfx", "mezcla", "video", "final", "verificar"):
        correr(video, etapa, [])


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "ayuda"):
        print(__doc__)
        return
    if a[0] == "api":
        env = dict(os.environ, PYTHONPATH=NUCLEO, PYTHONIOENCODING="utf-8")
        subprocess.run([sys.executable, "-m", "api_doc"], cwd=RAIZ, env=env, check=True)
        return
    if a[0] == "yt":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "youtube.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "nuevo":
        destino = os.path.join(VIDEOS, a[1])
        if os.path.exists(destino):
            sys.exit(f"Ya existe {destino}")
        shutil.copytree(os.path.join(VIDEOS, "_plantilla"), destino)
        print(f"Creado {destino}. Edita guion.py y luego: python fab.py {a[1]} todo")
        return
    video, etapa, extra = a[0], a[1], a[2:]
    if etapa == "todo":
        todo(video)
    elif etapa == "limpiar":
        for d in ("segmentos", "previews"):
            shutil.rmtree(os.path.join(VIDEOS, video, d), ignore_errors=True)
        print("limpio")
    elif etapa in ETAPAS:
        correr(video, etapa, extra)
    else:
        sys.exit(f"Etapa desconocida '{etapa}'. Opciones: {', '.join(list(ETAPAS) + ['todo', 'limpiar'])}")


if __name__ == "__main__":
    main()
