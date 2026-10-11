# -*- coding: utf-8 -*-
"""Lanzador de la Fábrica de Animaciones.

  python fab.py estado [<video>]                estado de todos los videos / ESTADO.md de uno (para retomar en una conversación nueva)
  python fab.py nuevo <video>                   crea videos/<video> desde videos/_plantilla
  python fab.py nuevo <video> --secuencia       igual, pero con el motor SECUENCIA (clips e imágenes de Google Flow; docs/estilo_secuencia_flow.md)
  python fab.py <video> beats | prompts | ingesta | medios     motor SECUENCIA: cortes por beat, prompts para Flow, traer descargas, hojas de revisión
  python fab.py <video> voz [--seeds 1 2 3 4]   genera tomas de voz con Chatterbox
  python fab.py <video> seleccionar             elige la mejor toma por frase (Whisper + similitud), alinea palabras
  python fab.py <video> tiempo                  construye timeline.json (BPM, escenas, transiciones)
  python fab.py <video> escena <id> <t> [t...]  hoja de prueba de una escena  -> previews/esc_<id>.jpg
  python fab.py <video> comprobar               chequeo rápido previo al render (nombres, anclas, un cuadro por fase)
  python fab.py <video> prueba <t> [t...]       cuadros finales (transiciones + subtítulos) -> previews/hoja_render.jpg
  python fab.py <video> estilos <t>             el mismo cuadro en todos los estilos -> previews/estilos.jpg
  python fab.py <video> catalogo                todos los íconos en el estilo del video -> previews/catalogo_iconos.png
  python fab.py <video> musica | sfx | mezcla   audio (música procedural, efectos, mezcla y máster)
  python fab.py <video> video [--procs 12]      render completo sin audio (reanuda: salta segmentos ya hechos)
  python fab.py <video> video --rehacer 270-280 [545-550 ...]   re-renderiza solo esos tramos (s) y reempalma
  python fab.py <video> final                   MASTER.mp4 + subtítulos .srt (conserva segmentos/; FAB_WHATSAPP=1 añade 720p)
  python fab.py <video> verificar               QA final: Whisper sobre la mezcla, duración, desfase A/V, hoja de cuadros
  python fab.py <video> todo                    voz→seleccionar→tiempo→musica→sfx→mezcla→video→final
  python fab.py <video> limpiar [--previews]    borra segmentos/ del render (y previews/ con --previews) al aprobar el video
  python fab.py panel [--puerto 8765] [--abrir] panel web con el avance de todos los proyectos (nucleo/panel.py)
  python fab.py estudio [--puerto 8790] [--abrir]  ESTUDIO: interfaz sencilla (comercial) para videos de 60 s (estudio/servidor.py)
  python fab.py estadisticas [--actualizar]     panel general de estadísticas de todos los canales (nucleo/estadisticas.py)
  python fab.py canales [--actualizar]          inicio de día: qué canal se queda antes sin video programado
  python fab.py ideas [<canal>] [--actualizar]  siguiente video CON DATOS: lo tuyo vs. lo que rompió la media en el nicho (nucleo/ideas.py)
  python fab.py api                       regenera API.md
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
    # motor SECUENCIA (nucleo/secuencia.py): su `video` también sale de ahí cuando guion.py dice MOTOR = "secuencia"
    "beats": ["-m", "secuencia", "beats"], "prompts": ["-m", "secuencia", "prompts"],
    "ingesta": ["-m", "secuencia", "ingesta"], "medios": ["-m", "secuencia", "medios"],
    "ambiente": ["-m", "secuencia", "ambiente"], "servir": ["-m", "secuencia", "servir"],
    "fx": ["-m", "secuencia_fx"],   # capa de efectos del motor secuencia (efectos.py): SFX de ElevenLabs -> audio/fx.wav; `fx hoja`
}


# Etapas que usan la GPU para voz (Chatterbox / Whisper): nunca dos a la vez, aunque sean de videos distintos.
# Con la GPU compartida cada toma pasa de ~4 s a ~15 min, así que las demás esperan su turno en cola.
ETAPAS_GPU_VOZ = ("voz", "seleccionar", "verificar")
LOCK_VOZ = os.path.join(RAIZ, "voz_gpu.lock")


class _CandadoVoz:
    """Candado exclusivo entre procesos (msvcrt). Lo suelta solo el sistema si el proceso muere."""

    def __init__(self, descripcion):
        self.descripcion = descripcion
        self.f = None

    def __enter__(self):
        import time
        avisado = False
        while True:
            f = open(LOCK_VOZ, "a+")
            try:
                if os.name == "nt":
                    import msvcrt
                    f.seek(1 << 20)  # byte lejos del texto: así los demás pueden leer quién lo tiene
                    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                f.seek(0)
                quien = "".join(c for c in f.read(200) if c.isprintable()).strip() or "otro proyecto"
                f.close()
                if not avisado:
                    print(f"[cola de voz] la GPU de voz la usa «{quien}»: espero mi turno ({self.descripcion})...", flush=True)
                    avisado = True
                time.sleep(5)
        self.f = f
        f.seek(0)
        f.truncate()
        f.write(self.descripcion)
        f.flush()
        if avisado:
            print("[cola de voz] mi turno, empiezo.", flush=True)
        return self

    def __exit__(self, *a):
        try:
            if os.name == "nt":
                import msvcrt
                self.f.seek(1 << 20)
                msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
        finally:
            self.f.close()


def correr(video, etapa, extra):
    carpeta = os.path.join(VIDEOS, video)
    if not os.path.isfile(os.path.join(carpeta, "guion.py")):
        sys.exit(f"No existe {carpeta}\\guion.py  (usa: python fab.py nuevo {video})")
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([carpeta, NUCLEO])
    env["PYTHONIOENCODING"] = "utf-8"
    import re as _re
    _m = _re.search(r"^FPS\s*=\s*(\d+)", open(os.path.join(carpeta, "guion.py"), encoding="utf-8").read(), _re.M)
    if _m:
        env["FAB_FPS"] = _m.group(1)          # fps del video (por defecto 30)
    cmd = [sys.executable] + ETAPAS[etapa] + list(extra)
    if _re.search(r'^MOTOR\s*=\s*"secuencia"', open(os.path.join(carpeta, "guion.py"), encoding="utf-8").read(), _re.M):
        if etapa == "video":
            cmd = [sys.executable, "-m", "secuencia", "video"] + list(extra)
        elif etapa in ("comprobar", "escena", "prueba"):
            print(f"[{video}] {etapa}: no aplica al motor secuencia (revisa con `medios` y `video --tramo a-b`)")
            return
    print(f"\n=== [{video}] {etapa} ===", flush=True)
    if etapa in ETAPAS_GPU_VOZ:
        with _CandadoVoz(f"{video} {etapa}"):
            r = subprocess.run(cmd, cwd=carpeta, env=env)
    else:
        r = subprocess.run(cmd, cwd=carpeta, env=env)
    if r.returncode != 0:
        sys.exit(f"La etapa '{etapa}' falló (código {r.returncode}).")


def todo(video):
    carpeta = os.path.join(VIDEOS, video)
    _g = open(os.path.join(carpeta, "guion.py"), encoding="utf-8").read()
    if "SIN_VOZ = True" in _g and "VOZ_ANCLADA = True" not in _g:
        for etapa in ("tiempo", "comprobar", "musica", "sfx", "mezcla", "video", "final", "verificar"):
            correr(video, etapa, [])
        return
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


PESADAS = ("salida", "segmentos", "audio", "voz", "previews")


def pesados_a_e(video):
    """Video nuevo: sus carpetas pesadas nacen en E: (junction en la ruta de siempre) para no llenar C:.
    FAB_PESADOS cambia el destino; si el disco no está conectado se quedan en C: y se avisa."""
    sys.path.insert(0, NUCLEO)
    import mover_pesados as MP
    if not os.path.isdir(os.path.splitdrive(MP.DESTINO)[0] + "\\"):
        print(f"(aviso) no está el disco {MP.DESTINO}: las carpetas pesadas quedan en C:. Luego: python nucleo/mover_pesados.py --aplicar --subs {','.join(PESADAS)} {video}")
        return
    for sub in PESADAS:
        local = os.path.join(VIDEOS, video, sub)
        if os.path.exists(local):
            continue
        destino = os.path.join(MP.DESTINO, "videos", video, sub)
        os.makedirs(destino, exist_ok=True)
        MP.crear_junction(local, destino)
    print(f"Carpetas pesadas ({', '.join(PESADAS)}) en {os.path.join(MP.DESTINO, 'videos', video)}")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "ayuda"):
        print(__doc__)
        return
    if a[0] == "api":
        env = dict(os.environ, PYTHONPATH=NUCLEO, PYTHONIOENCODING="utf-8")
        subprocess.run([sys.executable, "-m", "api_doc"], cwd=RAIZ, env=env, check=True)
        return
    if a[0] == "estado":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "estado.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "panel":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "panel.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "estudio":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(RAIZ, "estudio", "servidor.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "estadisticas":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "estadisticas.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "canales":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "estadisticas.py"), "calendario", *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "ideas":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "ideas.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "yt":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "youtube.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "nuevo":
        destino = os.path.join(VIDEOS, a[1])
        if os.path.exists(destino):
            sys.exit(f"Ya existe {destino}")
        shutil.copytree(os.path.join(VIDEOS, "_plantilla_secuencia" if "--secuencia" in a else "_plantilla"), destino,
                        ignore=shutil.ignore_patterns("__pycache__"))
        pesados_a_e(a[1])
        print(f"Creado {destino}. Edita guion.py y ESTADO.md y luego: python fab.py {a[1]} todo")
        return
    video, etapa, extra = a[0], a[1], a[2:]
    if etapa == "todo":
        todo(video)
    elif etapa == "limpiar":            # segmentos del render (y previews/ solo con --previews: guarda respaldos de miniaturas)
        carpeta = os.path.join(VIDEOS, video)
        for d in ("segmentos", "previews") if "--previews" in extra else ("segmentos",):
            shutil.rmtree(os.path.join(carpeta, d), ignore_errors=True)
        vsa = os.path.join(carpeta, "salida", "video_sin_audio.mp4")
        if os.path.exists(vsa):
            os.remove(vsa)
        print("limpio")
    elif etapa in ETAPAS:
        correr(video, etapa, extra)
    else:
        sys.exit(f"Etapa desconocida '{etapa}'. Opciones: {', '.join(list(ETAPAS) + ['todo', 'limpiar'])}")


if __name__ == "__main__":
    main()
