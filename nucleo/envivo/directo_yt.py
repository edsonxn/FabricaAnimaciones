# -*- coding: utf-8 -*-
"""El directo de YouTube del EN VIVO, de punta a punta desde la PC (5-nov-2026).

    python nucleo/envivo/directo_yt.py preparar [canal] [--titulo "…"]   crea emisión PRIVADA + clave y configura OBS
    python nucleo/envivo/directo_yt.py obs                                solo (re)configura OBS
    python nucleo/envivo/directo_yt.py estado                             emisión, señal y OBS
    python nucleo/envivo/directo_yt.py salir [--publico]                  OBS transmite → la emisión pasa a «en vivo»
    python nucleo/envivo/directo_yt.py publico                            privado → público (con el directo ya al aire)
    python nucleo/envivo/directo_yt.py terminar                           cierra la emisión y para OBS

- YouTube por la API del canal (`nucleo/youtube.py`, permiso `youtube`). La emisión nace PRIVADA: hacerla pública es
  decisión del usuario (`salir --publico` o `publico`).
- OBS por obs-websocket (puerto y clave de su propia config; la clave no se imprime). Escena «EN VIVO» con la pantalla
  del directo como fuente de navegador 1920x1080 y su audio dentro de OBS; el micrófono y el audio del escritorio se
  silencian para que no salga nada de la casa.
- La pantalla de OBS es LA pantalla del directo (consume los bloques): la tele, en espejo (`/?monitor=1`).
- Lo creado se guarda en `_cache/directo_yt.json` (la clave de transmisión no sale de ahí; `_cache` no va a git). El
  servidor lo lee con `--chat-youtube auto`.
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import youtube as yt  # noqa: E402

CACHE = os.path.join(AQUI, "_cache", "directo_yt.json")
OBS_EXE = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
OBS_CFG = os.path.join(os.environ.get("APPDATA", ""), "obs-studio", "plugin_config", "obs-websocket", "config.json")
ESCENA, FUENTE = "EN VIVO", "Pantalla EN VIVO"
VENTANA, AUDIO, TITULO_VENTANA = "Ventana EN VIVO", "Audio EN VIVO", "En vivo"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PERFIL_EDGE = os.path.join(AQUI, "_cache", "edge_obs")


def abrir_ventana(url):
    """Edge en modo app con perfil propio, a pantalla completa en la 2.ª pantalla (x = -1920): 1920x1080 exactos, sin
    barra (Windows no deja una ventana con marco más alta que la pantalla). F11 la saca de pantalla completa."""
    if subprocess.run(["tasklist", "/v", "/fi", "imagename eq msedge.exe"], capture_output=True, text=True,
                      errors="ignore").stdout.count(TITULO_VENTANA) == 0:
        subprocess.Popen([EDGE, f"--user-data-dir={PERFIL_EDGE}", "--no-first-run", "--autoplay-policy=no-user-gesture-required",
                          "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
                          "--disable-backgrounding-occluded-windows", f"--app={url}",
                          "--window-position=-1920,0", "--window-size=1920,1080", "--start-fullscreen"])
        time.sleep(4)
INGESTA = "rtmp://a.rtmp.youtube.com/live2"

TITULOS = {
    "cronicas_tamriel": "EN VIVO: Lore de Skyrim y Tamriel | TÚ eliges el tema en el chat",
    "cronicas_warcraft": "EN VIVO: Lore de Warcraft | TÚ eliges el tema en el chat",
    "runa_caida": "EN VIVO: Lore de Elden Ring | TÚ eliges el tema en el chat",
}
DESCRIPCION = """Directo de lore que se escribe y se narra en tiempo real: comenta en el chat el tema que quieres escuchar
y cada pocos minutos el chat decide qué sigue. También puedes votar la voz del narrador.

La narración, el guion y el montaje se generan con IA en vivo; los datos de lore se revisan, pero si algo se nos escapa,
dínoslo en el chat y lo corregimos al aire.
"""


def guardado():
    try:
        return json.load(open(CACHE, encoding="utf-8"))
    except Exception:
        return {}


def guardar(d):
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(d, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- YouTube
def crear_emision(canal, titulo=None):
    cid = yt.resolver_canal(canal)
    d = guardado()
    if d.get("cid") != cid or not d.get("stream_id"):        # flujo (clave) reutilizable: uno por canal
        s = yt.api(cid, "POST", "/liveStreams", params={"part": "snippet,cdn,contentDetails"}, json={
            "snippet": {"title": "EN VIVO · fábrica"},
            "cdn": {"frameRate": "variable", "ingestionType": "rtmp", "resolution": "variable"},
            "contentDetails": {"isReusable": True}})
        d = {"cid": cid, "canal": canal, "stream_id": s["id"], "clave": s["cdn"]["ingestionInfo"]["streamName"]}
    ahora = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    b = yt.api(cid, "POST", "/liveBroadcasts", params={"part": "snippet,status,contentDetails"}, json={
        "snippet": {"title": titulo or TITULOS.get(canal, "EN VIVO"), "description": DESCRIPCION, "scheduledStartTime": ahora},
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False},
        "contentDetails": {"enableAutoStart": False, "enableAutoStop": True, "enableDvr": True, "latencyPreference": "normal",   # «low» acelera y corta el audio en el reproductor (prueba del 5-nov)
                           "monitorStream": {"enableMonitorStream": False}}})
    yt.api(cid, "POST", "/liveBroadcasts/bind", params={"id": b["id"], "part": "id,contentDetails", "streamId": d["stream_id"]})
    d.update({"video_id": b["id"], "titulo": b["snippet"]["title"], "creado": ahora, "privacidad": "private"})
    guardar(d)
    return d


def estado_yt(d):
    b = yt.api(d["cid"], "GET", "/liveBroadcasts", params={"part": "status", "id": d["video_id"]})
    s = yt.api(d["cid"], "GET", "/liveStreams", params={"part": "status", "id": d["stream_id"]})
    bs = (b.get("items") or [{}])[0].get("status", {})
    ss = (s.get("items") or [{}])[0].get("status", {})
    return {"emision": bs.get("lifeCycleStatus"), "privacidad": bs.get("privacyStatus"), "señal": ss.get("streamStatus"),
            "salud": (ss.get("healthStatus") or {}).get("status")}


def transicion(d, a):
    return yt.api(d["cid"], "POST", "/liveBroadcasts/transition", params={"broadcastStatus": a, "id": d["video_id"], "part": "status"})


def hacer_publico(d):
    yt.api(d["cid"], "PUT", "/videos", params={"part": "status"}, json={
        "id": d["video_id"], "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True}})
    d["privacidad"] = "public"
    guardar(d)


# ---------------------------------------------------------------- OBS
def obs(abrir=True):
    import obsws_python as ows
    cfg = json.load(open(OBS_CFG, encoding="utf-8"))
    for intento in range(30):
        try:
            return ows.ReqClient(host="127.0.0.1", port=cfg.get("server_port", 4455), password=cfg.get("server_password", ""), timeout=5)
        except Exception:
            if intento == 0 and abrir:
                subprocess.Popen([OBS_EXE, "--disable-shutdown-check"], cwd=os.path.dirname(OBS_EXE))
            time.sleep(1.5)
    raise SystemExit("OBS no contesta en el websocket (¿abierto? Herramientas → Ajustes del servidor WebSocket)")


def configurar_obs(d, puerto=8790):
    c = obs()
    for _ in range(40):                                       # recién abierto, OBS contesta 207 («not ready») unos segundos
        try:
            escenas = [s["sceneName"] for s in c.get_scene_list().scenes]
            break
        except Exception:
            time.sleep(1)
    else:
        raise SystemExit("OBS no termina de arrancar")
    if ESCENA not in escenas:
        c.create_scene(ESCENA)
    # La pantalla va en una VENTANA DE EDGE aparte, no en la fuente de navegador de OBS: el audio de esa fuente salía
    # cortado (~7 cortes por segundo, «como radio que pierde señal») aunque la página solo tocara la voz; capturado de la
    # ventana de Edge, 0 cortes (medido el 5-nov-2026). OBS toma la imagen (captura de ventana) y el audio (captura de
    # audio de aplicación) de esa ventana. Edge con perfil propio: no se mezcla con el navegador del usuario.
    url = f"http://127.0.0.1:{puerto}/?auto=1"
    abrir_ventana(url)
    entradas = [i["inputName"] for i in c.get_input_list().inputs]
    if FUENTE in entradas:                                    # la fuente de navegador vieja también consumía bloques
        c.remove_input(FUENTE)
    ventana = f"{TITULO_VENTANA}:Chrome_WidgetWin_1:msedge.exe"
    for nombre, tipo, aj in ((VENTANA, "window_capture", {"window": ventana, "priority": 0, "method": 2, "cursor": False, "client_area": True}),
                             (AUDIO, "wasapi_process_output_capture", {"window": ventana, "priority": 0})):
        if nombre in entradas:
            c.set_input_settings(nombre, aj, True)
        else:
            c.create_input(ESCENA, nombre, tipo, aj, True)
    time.sleep(1)
    for it in c.get_scene_item_list(ESCENA).scene_items:      # la ventana, al lienzo 1920x1080 (si quedara barra, se recorta)
        if it["sourceName"] == VENTANA:
            alto = c.get_scene_item_transform(ESCENA, it["sceneItemId"]).scene_item_transform.get("sourceHeight") or 1080
            c.set_scene_item_transform(ESCENA, it["sceneItemId"], {"positionX": 0, "positionY": 0, "cropTop": int(max(0, alto - 1080)), "boundsType": "OBS_BOUNDS_STRETCH",
                                                                    "boundsWidth": 1920, "boundsHeight": 1080, "boundsAlignment": 0})
    c.set_current_program_scene(ESCENA)
    especiales = c.get_special_inputs()                       # micrófono y audio del escritorio: callados
    for k in ("desktop1", "desktop2", "mic1", "mic2", "mic3", "mic4"):
        n = getattr(especiales, k, None)
        if n:
            c.set_input_mute(n, True)
    try:
        c.set_video_settings(30, 1, 1920, 1080, 1920, 1080)
    except Exception:
        pass                                                   # con la salida activa no se puede: se queda como estaba
    try:
        c.set_stream_service_settings("rtmp_custom", {"server": INGESTA, "key": d["clave"]})
    except Exception:
        pass                                                   # transmitiendo no se puede cambiar: ya está puesta
    return url


def obs_transmitiendo():
    try:
        return obs(abrir=False).get_stream_status().output_active
    except BaseException:
        return None


# ---------------------------------------------------------------- comandos
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("accion", choices=["preparar", "obs", "estado", "salir", "publico", "terminar"])
    ap.add_argument("canal", nargs="?", default="cronicas_tamriel")
    ap.add_argument("--titulo")
    ap.add_argument("--publico", action="store_true")
    ap.add_argument("--puerto", type=int, default=8790)
    a = ap.parse_args()
    d = guardado()
    if a.accion == "preparar":
        d = crear_emision(a.canal, a.titulo)
        print(f"emisión PRIVADA creada: https://youtu.be/{d['video_id']}  («{d['titulo']}»)")
        print(f"Studio: https://studio.youtube.com/video/{d['video_id']}/livestreaming")
        print("OBS: escena", ESCENA, "→", configurar_obs(d, a.puerto), "(micrófono y escritorio silenciados; clave puesta)")
        return
    if not d.get("video_id"):
        raise SystemExit("no hay emisión: primero `preparar`")
    if a.accion == "obs":
        print("OBS:", configurar_obs(d, a.puerto))
    elif a.accion == "estado":
        print(json.dumps({**estado_yt(d), "obs_transmitiendo": obs_transmitiendo(), "video": f"https://youtu.be/{d['video_id']}"},
                         ensure_ascii=False))
    elif a.accion == "salir":
        c = obs()
        if not c.get_stream_status().output_active:
            c.start_stream()
        for _ in range(60):                                   # YouTube tarda unos segundos en ver la señal
            e = estado_yt(d)
            if e["señal"] == "active":
                break
            time.sleep(2)
        else:
            raise SystemExit(f"YouTube no recibe la señal de OBS: {e}")
        if e["emision"] not in ("live", "liveStarting"):
            transicion(d, "live")
        if a.publico:
            hacer_publico(d)
        print("AL AIRE:", json.dumps(estado_yt(d), ensure_ascii=False), f"https://youtu.be/{d['video_id']}")
    elif a.accion == "publico":
        hacer_publico(d)
        print("público:", f"https://youtu.be/{d['video_id']}")
    elif a.accion == "terminar":
        try:
            transicion(d, "complete")
        except Exception as e:
            print("transición:", e)
        try:
            obs(abrir=False).stop_stream()
        except BaseException:
            pass
        print("emisión terminada", json.dumps(estado_yt(d), ensure_ascii=False))


if __name__ == "__main__":
    main()
