# -*- coding: utf-8 -*-
"""Lanzador de la Fábrica de Animaciones.

  python fab.py estado [<video>]                estado de todos los videos / ESTADO.md de uno (para retomar en una conversación nueva)
  python fab.py continuar [<texto>]             «continúa el video …»: qué TRAMO sigue (videos hechos en varias sesiones; docs/sesiones.md)
  python fab.py nuevo <video>                   crea videos/<video> desde videos/_plantilla
  python fab.py nuevo <video> --secuencia       igual, pero con el motor SECUENCIA (clips e imágenes de Google Flow; docs/estilo_secuencia_flow.md)
  python fab.py nuevo <video> --yt              motor SECUENCIA YT: gameplay de YouTube por beat (Warcraft; docs/estilo_secuencia_yt.md)
  python fab.py <video> busquedas | bajar | fuentes            motor SECUENCIA YT: una búsqueda por beat, bajar y cortar, créditos
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
  python fab.py limpiar --publicados [--borrar] libera disco: videos y mezclas .wav de los ya públicos en YouTube (conserva proyecto y voz)
  python fab.py panel [--puerto 8765] [--abrir] panel web con el avance de todos los proyectos (nucleo/panel.py)
  python fab.py panel --remoto [--tunel cloudflared] [estado|parar]  el lienzo desde el celular: puerta con clave + túnel (imprime el enlace)
  python fab.py estudio [--puerto 8790] [--abrir]  ESTUDIO: interfaz sencilla (comercial) para videos de 60 s (estudio/servidor.py)
  python fab.py estadisticas [--actualizar]     panel general de estadísticas de todos los canales (nucleo/estadisticas.py)
  python fab.py buenosdias [--actualizar]       «Buenos días»: tablero del día para el plan de acción (docs/buenos_dias.md)
  python fab.py canales [--actualizar]          inicio de día: qué canal se queda antes sin video programado
  python fab.py ideas [<canal>] [--actualizar]  siguiente video CON DATOS: lo tuyo vs. lo que rompió la media en el nicho (nucleo/ideas.py)
  python fab.py biblioteca buscar|sugerir|usar|ver|catalogar|sfx …   música de Lyria y SFX ya hechos, para reutilizar (docs/musica_biblioteca.md)
  python fab.py compartir [--destino D] [--subir <url .git>]   copia SIN tus canales (motor + estilos + ejemplos) para otra persona
  python fab.py api                       regenera API.md
"""
import json
import os
import shutil
import subprocess
import sys
import time

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
    "beats": ["-m", "secuencia", "beats"], "reajustar": ["-m", "secuencia", "reajustar"], "prompts": ["-m", "secuencia", "prompts"],
    "ingesta": ["-m", "secuencia", "ingesta"], "medios": ["-m", "secuencia", "medios"],
    "ambiente": ["-m", "secuencia", "ambiente"], "servir": ["-m", "secuencia", "servir"],
    # motor SECUENCIA YT (nucleo/secuencia_yt.py): gameplay de YouTube por beat (Crónicas de Warcraft)
    "busquedas": ["-m", "secuencia_yt", "busquedas"], "bajar": ["-m", "secuencia_yt", "bajar"],
    "fuentes": ["-m", "secuencia_yt", "fuentes"], "chequeo": ["-m", "chequeo_yt"],   # capas por minuto y narración ↔ imagen
    "fx": ["-m", "secuencia_fx"],   # capa de efectos del motor secuencia (efectos.py): SFX de ElevenLabs -> audio/fx.wav; `fx hoja`
    "montaje": ["-m", "montaje_codigo"],   # videos por código: borradores 640x360 por escena para el 🎞 Montaje del panel
    "vivo": ["-m", "vivo"],         # imágenes vivas (parallax + recorte animado): caché medios/capas/, candidatos y hoja vivo_NN
    "apoyos": ["-m", "apoyos"],     # efectos.py APOYOS -> apoyos/*.png (tooltips Wowhead, tarjetas, capturas) + hoja fx
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
    if etapa == "video":
        _parcial = os.path.join(carpeta, "segmentos", "parcial.json")
        if "--hasta" in extra:                 # render PARCIAL (el principio, para verlo antes de hacer el resto): nucleo/render_parcial.py
            cmd = [sys.executable, "-m", "render_parcial", "video"] + list(extra)
        elif os.path.exists(_parcial):         # render completo: ya no hay tope
            os.remove(_parcial)
    _g = open(os.path.join(carpeta, "guion.py"), encoding="utf-8").read()
    if etapa == "musica" and _re.search(r"^LYRIA\s*=", _g, _re.M) and "--procedural" not in extra:
        # la música es Lyria (regla 12-oct): `musica` NO debe pisar audio/musica.wav con la procedural
        if not _re.search(r"^\s*tramos\s*=", _g, _re.M):
            print(f"[{video}] musica: el guion tiene LYRIA sin `tramos`: genera con `python ../../nucleo/lyria.py --n 2` y "
                  f"`--usar N` desde la carpeta del video (la procedural solo con --procedural).")
            return
        cmd = [sys.executable, os.path.join(NUCLEO, "lyria_tramos.py"), "todo"]
    elif etapa == "musica":
        extra = [a for a in extra if a != "--procedural"]
        cmd = [sys.executable] + ETAPAS[etapa] + list(extra)
    if _re.search(r'^MOTOR\s*=\s*"secuencia"', open(os.path.join(carpeta, "guion.py"), encoding="utf-8").read(), _re.M):
        if etapa == "video":
            cmd = [sys.executable, "-m", "secuencia", "video"] + list(extra)
            if not extra and _re.search(r'fuente\s*=\s*"yt"', open(os.path.join(carpeta, "guion.py"), encoding="utf-8").read()):
                subprocess.run([sys.executable, "-m", "chequeo_yt"], cwd=carpeta, env=env)   # solo avisa (30-oct-2026)
        elif etapa in ("comprobar", "escena", "prueba", "montaje"):
            print(f"[{video}] {etapa}: no aplica al motor secuencia (revisa con `medios` y `video --tramo a-b`)")
            return
    print(f"\n=== [{video}] {etapa} ===", flush=True)
    # sin GPU no hay cola (19-oct-2026): la voz de ElevenLabs es una API, y `seleccionar` con FAB_WHISPER_CPU=1 evalúa en CPU
    sin_gpu = bool((etapa == "voz" and _re.search(r'motor\s*=\s*"elevenlabs"', _g))
                   or (etapa == "seleccionar" and os.environ.get("FAB_WHISPER_CPU")))
    if etapa in ETAPAS_GPU_VOZ and not sin_gpu:
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


TALLER = "http://127.0.0.1:8765"


def asegurar_taller():
    """El usuario (31-oct-2026): al empezar o continuar un video, el Robotaller (/v2/vivo) tiene que estar activo.
    Si el panel no responde lo arranca desacoplado (sobrevive a la sesión; nunca se detiene) y abre el taller."""
    from urllib.request import urlopen

    def vivo():
        try:
            urlopen(TALLER + "/v2/vivo", timeout=3).close()
            return True
        except Exception:
            return False

    if vivo():
        print(f"Robotaller activo: {TALLER}/v2/vivo", flush=True)
        return
    log = open(os.path.join(RAIZ, "panel_log_taller.txt"), "a", encoding="utf-8")
    subprocess.Popen([sys.executable, os.path.join(NUCLEO, "panel.py")], cwd=RAIZ, stdout=log, stderr=log, stdin=subprocess.DEVNULL,
                     env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                     creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)   # consola oculta: sus hijos la heredan, sin ventanas
    for _ in range(40):
        time.sleep(0.5)
        if vivo():
            import webbrowser
            webbrowser.open(TALLER + "/v2/vivo")
            print(f"Robotaller encendido: {TALLER}/v2/vivo", flush=True)
            return
    print("(aviso) el panel no respondió en 20 s; mira panel_log_taller.txt o lánzalo con: python fab.py panel --abrir")


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "ayuda"):
        print(__doc__)
        return
    if a[0] == "api":
        env = dict(os.environ, PYTHONPATH=NUCLEO, PYTHONIOENCODING="utf-8")
        subprocess.run([sys.executable, "-m", "api_doc"], cwd=RAIZ, env=env, check=True)
        return
    if a[0] in ("estado", "continuar"):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        args = a[1:] if a[0] == "estado" else ["continuar", *a[1:]]
        if a[0] == "continuar":
            asegurar_taller()
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "estado.py"), *args], cwd=RAIZ, env=env).returncode)
    if a[0] == "avisar":              # aviso por voz autónomo (Chatterbox + bocinas), sin servidor ni puerto 3000
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "avisar.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "panel":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        if "--remoto" in a:          # el lienzo desde el celular: puerta con clave + túnel (nucleo/panel_remoto.py)
            resto = [x for x in a[1:] if x != "--remoto"]
            sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "panel_remoto.py"), *resto], cwd=RAIZ, env=env).returncode)
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
    if a[0] == "buenosdias":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "buenosdias.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "ideas":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "ideas.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "biblioteca":          # música de Lyria y SFX ya pagados, con etiquetas, para reutilizar (docs/musica_biblioteca.md)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "musica_biblioteca.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "compartir":           # copia sin tus canales para otra persona (nucleo/compartir.py; compartir/ = su CLAUDE.md y LEEME)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "compartir.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "yt":
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "youtube.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "limpiar" and "--publicados" in a:   # disco: borra videos y mezclas de los ya públicos (nucleo/limpiar_publicados.py)
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        sys.exit(subprocess.run([sys.executable, os.path.join(NUCLEO, "limpiar_publicados.py"), *a[1:]], cwd=RAIZ, env=env).returncode)
    if a[0] == "nuevo":
        destino = os.path.join(VIDEOS, a[1])
        if os.path.exists(destino):
            sys.exit(f"Ya existe {destino}")
        shutil.copytree(os.path.join(VIDEOS, "_plantilla_yt" if "--yt" in a else "_plantilla_secuencia" if "--secuencia" in a else "_plantilla"), destino,
                        ignore=shutil.ignore_patterns("__pycache__"))
        pesados_a_e(a[1])
        asegurar_taller()
        print(f"Creado {destino}. Edita guion.py y ESTADO.md y luego: python fab.py {a[1]} todo")
        print("Regla (13-oct-2026): actualiza el panel de canales ahora y al terminar el video: python fab.py canales --actualizar")
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
