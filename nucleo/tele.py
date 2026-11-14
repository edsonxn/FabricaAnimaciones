# -*- coding: utf-8 -*-
"""LA TELE: la fábrica le manda al Google TV de la casa avisos con voz, avances, montajes, el tablero de videos en curso y
PREGUNTAS CON BOTONES que el usuario contesta con el control remoto (pedido del usuario, 4-nov-2026). La tele corre la app
«Puente TV» (D:\\PuenteTV, servidor HTTP en el puerto 8730; la PC la encuentra por UDP en 8731). Aquí no hace falta que
PuenteTV.exe esté abierto: se le habla a la tele directo y la voz sale de ElevenLabs con las cuentas de la fábrica.

  python fab.py tele                              ¿está la tele? (nombre, IP, qué se ve, permisos)
  python fab.py tele disponible                   imprime sí/no (código 0/4): la tele contesta y tiene la pantalla prendida
  python fab.py tele aviso "texto" [--titulo T] [--estilo info|importante|urgente|listo] [--no-pausar] [--sin-voz]
        [--nivel urgente|importante|info] [--origen fabrica|cnb|claude]   la tele decide según su modo (completo, banner o bandeja)
  python fab.py tele revisar <v> [avance|master|montaje] | --archivo x.mp4 [--esperar 3600]
        sala de revisión: el usuario marca momentos con el control (▼) y da el veredicto; deja REVISION_*.md con un cuadro por marca
  python fab.py tele modo [todo|normal|urgentes|silencio] [--minutos 120 | --hasta manana]   qué tanto puede interrumpir la tele
  python fab.py tele bandeja                      lo que llegó a la tele sin interrumpir
  python fab.py tele video <v> [avance|master|montaje|escena <id>|<ruta.mp4>]   lo más nuevo del video si no se dice qué
        [--pregunta "¿Lo subo?" --opciones "Sí, súbelo|Rehacer el gancho|Después" --momento final|durante|siempre]
        [--esperar 900]                         con --pregunta: botones en la tele; --esperar bloquea hasta la respuesta
  python fab.py tele preguntar "¿Qué tema sigue?" --opciones "A|B|C" [--mensaje M] [--video <v>|<ruta.mp4>] [--esperar 900]
  python fab.py tele imagen <ruta.jpg> [--segundos 15] [--titulo T]
  python fab.py tele tablero [--segundos 25]      foto del estado de los videos en curso (canal, etapa, qué sigue)
  python fab.py tele tablero --vivo               el tablero en vivo (el del protector de pantalla: fábrica + edificio de CNB)
  python fab.py tele respuestas                   lo que el usuario ha contestado en la tele (también nucleo/datos/tele_respuestas.jsonl)
  python fab.py tele cerrar                       quita lo que esté mostrando
Al contestar con --video <v> la decisión se apunta también al final de videos/<v>/ESTADO.md («- tele: …»).
Desde cualquier proyecto (skill global «avisar-y-decidir»): `python C:\FabricaAnimaciones\fab.py tele …`; las rutas
relativas se leen desde la carpeta de quien llama (FAB_CWD) y los textos de respaldo por voz son genéricos.
`fab.py avisar` copia el aviso a la tele si está prendida (nucleo/datos/tele.json → "espejo_avisar"). Doc: docs/tele.md.
NIVELES (4-nov-2026, tarde): cada aviso lleva `nivel` y `origen`; la tele contesta `entrega` = completo | banner | bandeja según el modo
que el usuario eligió en ella. «bandeja» = pidió silencio: NO se repite por las bocinas."""
import argparse
import base64
import glob
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
import urllib.parse

import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
VIDEOS = os.path.join(RAIZ, "videos")
DATOS = os.path.join(AQUI, "datos")
CONF = os.path.join(DATOS, "tele.json")
RESPUESTAS = os.path.join(DATOS, "tele_respuestas.jsonl")
CACHE_VOZ = os.path.join(RAIZ, "panel_avisos")
PUENTE_CONF = os.path.join(os.environ.get("APPDATA", ""), "PuenteTV", "config.json")
PUERTO, PUERTO_UDP = 8730, 8731
VOZ = "l1zE9xgNpUTaQCZzpNJa"            # Alberto Rodríguez, la misma de `fab.py avisar`
MODELO = "eleven_v4_turbo"
DEFECTO = {"espejo_avisar": True, "pausar_avisos": True, "ip": None, "nombre": None}


# ====================================================================== configuración y búsqueda de la tele
def conf():
    try:
        with open(CONF, encoding="utf-8") as f:
            return {**DEFECTO, **json.load(f)}
    except (OSError, ValueError):
        return dict(DEFECTO)


def _guardar_conf(c):
    os.makedirs(DATOS, exist_ok=True)
    tmp = CONF + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=1)
    os.replace(tmp, CONF)


def _estado_en(ip, espera=2.5):
    try:
        r = requests.get(f"http://{ip}:{PUERTO}/estado", params={"pc": "fabrica"}, timeout=espera)
        return r.json() if r.ok else None
    except (requests.RequestException, ValueError):
        return None


def _buscar_udp():
    """Pregunta «PUENTE?» por broadcast; la tele contesta «PUENTE1|nombre|8730»."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.settimeout(1.5)
    try:
        s.sendto(b"PUENTE?", ("255.255.255.255", PUERTO_UDP))
        while True:
            datos, (ip, _) = s.recvfrom(256)
            p = datos.decode("utf-8", "replace").split("|")
            if p[0] == "PUENTE1":
                return ip, (p[1] if len(p) > 1 else "Google TV")
    except OSError:
        return None
    finally:
        s.close()


_tele = None


def tele(obligatoria=True):
    """(ip, estado) de la tele; la IP se recuerda en tele.json y se vuelve a buscar si deja de contestar."""
    global _tele
    if _tele:
        return _tele
    c = conf()
    candidatas = [c.get("ip")]
    try:
        with open(PUENTE_CONF, encoding="utf-8-sig") as f:
            candidatas.append(json.load(f).get("TvIp"))
    except (OSError, ValueError):
        pass
    for ip in dict.fromkeys(x for x in candidatas if x):
        st = _estado_en(ip)
        if st:
            break
    else:
        hallada = _buscar_udp()
        ip, st = (hallada[0], _estado_en(hallada[0])) if hallada else (None, None)
    if not st:
        if obligatoria:
            raise SystemExit("La tele no contesta: ¿está prendida y con Puente TV? (D:\\PuenteTV, puerto 8730)")
        return None
    if ip != c.get("ip") or st.get("nombre") != c.get("nombre"):
        c.update(ip=ip, nombre=st.get("nombre"))
        _guardar_conf(c)
    _tele = (ip, st)
    return _tele


def _url(ruta, **q):
    ip, _ = tele()
    q["pc"] = "fabrica"
    return f"http://{ip}:{PUERTO}{ruta}?{urllib.parse.urlencode(q)}"


def _post_json(ruta, cuerpo, **q):
    r = requests.post(_url(ruta, **q), data=json.dumps(cuerpo, ensure_ascii=False).encode("utf-8"),
                      headers={"Content-Type": "application/json; charset=utf-8"}, timeout=60)
    try:
        d = r.json()
    except ValueError:
        d = {"ok": False, "error": r.text[:200]}
    if not r.ok or not d.get("ok", True):
        raise SystemExit(f"La tele rechazó {ruta}: {d.get('error') or r.status_code}"
                         + (" (¿falta actualizar Puente TV en la tele?)" if r.status_code == 404 else ""))
    return d


def _subir(ruta_archivo, ruta, **q):
    """Sube un archivo grande por flujo (no se carga en memoria) e imprime el avance."""
    total = os.path.getsize(ruta_archivo)

    def trozos():
        hecho, ultimo = 0, 0
        with open(ruta_archivo, "rb") as f:
            while True:
                b = f.read(1 << 20)
                if not b:
                    break
                hecho += len(b)
                if hecho - ultimo > total / 10 or hecho == total:
                    ultimo = hecho
                    print(f"  subiendo a la tele… {hecho * 100 // max(total, 1)} %", flush=True)
                yield b
    r = requests.post(_url(ruta, nombre=os.path.basename(ruta_archivo), **q), data=trozos(),
                      headers={"Content-Type": "application/octet-stream", "Content-Length": str(total)}, timeout=(10, 900))
    try:
        d = r.json()
    except ValueError:
        d = {}
    if not r.ok:
        raise SystemExit(f"La tele rechazó {ruta}: {d.get('error') or r.status_code}")
    return d


# ====================================================================== voz (ElevenLabs, como `fab.py avisar`)
def voz_mp3(texto):
    """MP3 de ElevenLabs (caché por texto en panel_avisos/); None si no hay red o saldo: entonces habla la voz de la tele."""
    import avisar
    hablado = avisar.texto_hablado(texto)
    if not hablado:
        return None
    os.makedirs(CACHE_VOZ, exist_ok=True)
    ruta = os.path.join(CACHE_VOZ, "tele_" + hashlib.sha1((hablado + VOZ).encode("utf-8")).hexdigest()[:16] + ".mp3")
    if os.path.isfile(ruta) and os.path.getsize(ruta) > 1000:
        return open(ruta, "rb").read()
    try:
        import tts_eleven
        body = dict(text=hablado, model_id=MODELO, language_code="es", voice_settings=dict(stability=0.5))
        r = tts_eleven.post(f"text-to-speech/{VOZ}?output_format=mp3_44100_128", json=body, timeout=60)
        if r.status_code != 200 or len(r.content) < 1000:
            return None
    except (Exception, SystemExit):
        return None
    with open(ruta + ".tmp", "wb") as f:
        f.write(r.content)
    os.replace(ruta + ".tmp", ruta)
    return r.content


def _con_voz(cuerpo, texto, voz=True):
    mp3 = voz_mp3(texto) if voz else None
    if mp3:
        cuerpo["audio_b64"] = base64.b64encode(mp3).decode("ascii")
    else:
        cuerpo["voz_tv"] = bool(voz)
    return cuerpo


# ====================================================================== acciones
def aviso(mensaje, titulo="", estilo="info", pausar=None, voz=True, duracion=0, nivel=None, origen="fabrica"):
    """Devuelve la respuesta de la tele; `entrega` dice cómo llegó (completo, banner o bandeja). Una tele vieja no la trae."""
    pausar = conf()["pausar_avisos"] if pausar is None else pausar
    cuerpo = dict(titulo=titulo, mensaje=mensaje, estilo=estilo, pausar=pausar, duracion=duracion, origen=origen)
    if nivel:
        cuerpo["nivel"] = nivel
    # La voz de ElevenLabs solo hace falta a pantalla completa: si la tele lo va a mandar a la esquinita o a la bandeja, no se gasta
    if voz and _entrega_probable(nivel or {"urgente": "urgente", "importante": "importante"}.get(estilo, "info"), origen) != "completo":
        voz = False
    return _post_json("/aviso", _con_voz(cuerpo, ". ".join(x for x in (titulo, mensaje) if x), voz))


def modo_tele():
    """Lo que eligió el usuario en la tele ({modo, no_molestar_hasta, dejar_urgentes, origenes}); None con una app vieja."""
    try:
        ip, _ = tele()
        r = requests.get(f"http://{ip}:{PUERTO}/modo", params={"pc": "fabrica"}, timeout=4)
        return r.json() if r.ok else None
    except (requests.RequestException, ValueError, SystemExit):
        return None


def _entrega_probable(nivel, origen):
    """La misma tabla que la tele (Ajustes.kt), para no pedir voz a ElevenLabs si no va a sonar."""
    m = modo_tele()
    if not m:
        return "completo"
    o = (m.get("origenes") or {}).get(origen, "normal")
    if o == "silencio":
        return "bandeja"
    n = {"urgente": 2, "importante": 1}.get(nivel, 0) - (1 if o == "menos" else 0)
    if n < 0:
        return "bandeja"
    modo = m.get("modo", "normal")
    if modo == "todo":
        return "completo" if n >= 1 else "banner"
    if modo == "urgentes":
        return "banner" if n == 2 else "bandeja"
    if modo == "silencio":
        return "banner" if n == 2 and m.get("dejar_urgentes", True) else "bandeja"
    return {2: "completo", 1: "banner"}.get(n, "bandeja")


def disponible():
    """La tele contesta Y tiene la pantalla prendida (en reposo el Chromecast sigue en la red, pero nadie lo vería).
    FAB_SIN_TELE=1 hace como si no estuviera (pruebas, o avisos solo en la PC)."""
    if os.environ.get("FAB_SIN_TELE") == "1":
        return False
    t = tele(obligatoria=False)
    return bool(t) and t[1].get("pantalla", True) is not False


def espejo_avisar(texto):
    """Lo llama `fab.py avisar`: REGLA (el usuario, 4-nov-2026) = primero la tele si está disponible. True si la tele
    lo recibió (entonces la PC ya no lo dice por las bocinas). Nunca falla."""
    try:
        if not conf()["espejo_avisar"] or not disponible():
            return False
        aviso(texto, titulo="Fábrica de Animaciones", estilo="listo", nivel="importante", origen="fabrica")
        return True                 # también si quedó en la bandeja: el usuario pidió silencio, no se repite en las bocinas
    except (Exception, SystemExit):
        return False


def por_voz(texto):
    """Respaldo de la regla: la tele no está → el aviso de siempre por las bocinas de la PC (ElevenLabs / voz de Windows)."""
    import avisar
    avisar.decir(texto)
    print(f"La tele no está disponible: avisé por voz en la PC («{texto}»).")


def imagen(ruta, segundos=15, titulo=None):
    q = {"segundos": segundos, "pausar": 1, "origen": "fabrica"}
    if titulo:
        q["titulo"] = titulo
    return _subir(ruta, "/imagen", **q)


def video(ruta, pausar=True):
    return _subir(ruta, "/video", pausar=int(pausar), origen="fabrica")


def web(url):
    """Una página viva a pantalla completa en la tele (el EN VIVO: `fab.py envivo --tele`); Atrás en el control la cierra."""
    return _post_json("/web", {"url": url})


def cerrar_web():
    return _post_json("/web/cerrar", {})


def ip_hacia_tele():
    """La IP de esta PC en la red de la tele (para darle direcciones que pueda abrir)."""
    import socket
    ip, _ = tele()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect((ip, PUERTO))
        return s.getsockname()[0]
    finally:
        s.close()


ULTIMA_ENTREGA = None


def _pospuesta():
    """¿La tele está en un modo que pospone las preguntas? (Solo urgentes / No molestar): entonces ni se sube el video."""
    m = modo_tele()
    return bool(m) and m.get("modo") in ("urgentes", "silencio")


def preguntar(titulo, opciones, mensaje="", archivo=None, momento="final", v=None, estilo="importante", modo=None, origen="fabrica"):
    """Pone la pregunta en la tele (con el video si se da `archivo`) y devuelve su id. Si la tele la pospone por su modo,
    ULTIMA_ENTREGA = "bandeja" (hay que preguntar en el chat)."""
    global ULTIMA_ENTREGA
    pid = time.strftime(("r" if modo == "revision" else "p") + "%m%d%H%M%S")
    pospuesta = _pospuesta()
    if pospuesta:
        subido = None                       # no vale la pena subir cientos de MB que no se van a ver
    else:
        subido = _subir(archivo, "/archivo")["archivo"] if archivo else None
    cuerpo = dict(id=pid, titulo=titulo, mensaje=mensaje, opciones=opciones, estilo=estilo, momento=momento,
                  video=v or "", pausar=True, origen=origen)
    if modo:
        cuerpo["modo"] = modo
    if subido:
        cuerpo["archivo"] = subido
    hablar = ". ".join(x for x in (titulo, mensaje) if x) if (not archivo or momento != "durante") and modo != "revision" else ""
    d = _post_json("/pregunta", _con_voz(cuerpo, hablar, bool(hablar) and not pospuesta and (subido is not None or not archivo)))
    ULTIMA_ENTREGA = d.get("entrega", "completo")
    _apuntar(dict(id=pid, video=v, pregunta=titulo, opciones=opciones,
                  estado="pospuesta (no molestar)" if ULTIMA_ENTREGA == "bandeja" else "enviada"))
    return pid


def respuesta(pid):
    ip, _ = tele()
    r = requests.get(f"http://{ip}:{PUERTO}/respuesta", params={"id": pid, "pc": "fabrica"}, timeout=5)
    return r.json() if r.ok else {"estado": "desconocida"}


def esperar(pid, segundos, v=None, pregunta=""):
    """Bloquea hasta que el usuario conteste en la tele (o pase el tiempo). Devuelve el texto elegido o None."""
    fin = time.time() + segundos
    while time.time() < fin:
        try:
            r = respuesta(pid)
        except requests.RequestException:
            r = {}
        if r.get("estado") == "respondida":
            elegido = r.get("opcion")
            _apuntar(dict(id=pid, video=v, pregunta=pregunta, respuesta=elegido, estado="respondida"))
            if v:
                _al_estado(v, pregunta, elegido)
            return elegido
        if r.get("estado") == "cerrada":
            _apuntar(dict(id=pid, video=v, pregunta=pregunta, estado="cerrada sin respuesta"))
            return None
        time.sleep(2)
    return None


def _apuntar(d):
    os.makedirs(DATOS, exist_ok=True)
    d = {"hora": time.strftime("%Y-%m-%d %H:%M:%S"), **d}
    with open(RESPUESTAS, "a", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False) + "\n")


def _al_estado(v, pregunta, elegido):
    ruta = os.path.join(VIDEOS, v, "ESTADO.md")
    if os.path.isfile(ruta):
        with open(ruta, "a", encoding="utf-8") as f:
            f.write(f"\n- tele: {time.strftime('%d-%b %H:%M')} «{pregunta}» → **{elegido}** (contestado en la tele)\n")


# ====================================================================== sala de revisión
def esperar_revision(pid, segundos):
    """Espera a que termine la revisión (veredicto o Atrás). Devuelve el JSON de la tele (con `marcas`) o None."""
    fin = time.time() + segundos
    while time.time() < fin:
        try:
            r = respuesta(pid)
        except requests.RequestException:
            r = {}
        if r.get("estado") in ("respondida", "cerrada"):
            return r
        time.sleep(3)
    try:
        r = respuesta(pid)                 # se acabó la espera: lo que se haya marcado hasta ahora
        return r if r.get("marcas") else None
    except requests.RequestException:
        return None


def _seg(hora):
    """«2:14» o «1:02:14» → segundos."""
    s = 0
    for x in str(hora).split(":"):
        s = s * 60 + int(x)
    return s


def guardar_revision(r, archivo, v=None, titulo=""):
    """REVISION_<fecha>.md + un cuadro por marca (para que Claude vea qué señaló el usuario). Devuelve la ruta del .md."""
    marcas = r.get("marcas") or []
    base = os.path.join(VIDEOS, v, "revision") if v else os.path.join(
        os.path.dirname(os.path.abspath(archivo)), "revision_" + os.path.splitext(os.path.basename(archivo))[0])
    os.makedirs(base, exist_ok=True)
    sello = time.strftime("%Y%m%d_%H%M")
    filas = []
    for m in marcas:
        t = float(m.get("t", 0))
        hora = m.get("hora") or f"{int(t) // 60}:{int(t) % 60:02d}"
        jpg = os.path.join(base, f"marca_{sello}_{hora.replace(':', 'm')}s_{m.get('tipo', 'nota').lower().replace(' ', '_')}.jpg")
        try:
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", archivo, "-frames:v", "1",
                            "-vf", "scale=960:-2", "-q:v", "3", jpg], check=True, timeout=60)
        except (subprocess.SubprocessError, OSError):
            jpg = None
        filas.append((hora, m.get("tipo", "nota"), jpg))
    veredicto = r.get("opcion") or ("(sin veredicto: salió con Atrás)" if r.get("estado") == "cerrada" else "(sin veredicto)")
    md = os.path.join(base, f"REVISION_{sello}.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(f"# Revisión en la tele · {time.strftime('%d-%m-%Y %H:%M')}\n\n")
        f.write(f"- video: `{os.path.relpath(archivo, RAIZ) if v else archivo}`\n- veredicto: **{veredicto}**\n- marcas: {len(marcas)}\n\n")
        if filas:
            f.write("| momento | qué | cuadro |\n|---|---|---|\n")
            for hora, tipo, jpg in filas:
                f.write(f"| {hora} | {tipo} | {os.path.basename(jpg) if jpg else '—'} |\n")
        else:
            f.write("Sin marcas.\n")
    if v:
        _al_estado(v, f"Revisión en la tele ({len(marcas)} marcas, {os.path.relpath(md, os.path.join(VIDEOS, v))})", veredicto)
    _apuntar(dict(id=r.get("id"), video=v, pregunta=titulo or "revisión", respuesta=veredicto, marcas=marcas, estado="revisada"))
    return md, filas, veredicto


# ====================================================================== qué video mandar
def _mas_nuevo(patrones):
    hay = [p for pat in patrones for p in glob.glob(pat) if not p.endswith(".tmp.mp4")]
    return max(hay, key=os.path.getmtime) if hay else None


def elegir(v, que=None, escena=None):
    """Ruta del MP4 a mandar: avance (ligero si hay), master, montaje (armado con audio), escena <id> o lo más nuevo."""
    c = os.path.join(VIDEOS, v)
    if not os.path.isdir(c):
        if os.path.isfile(v):
            return v
        raise SystemExit(f"No existe videos/{v}")
    pv, sa = os.path.join(c, "previews"), os.path.join(c, "salida")
    if que == "escena":
        r = os.path.join(pv, f"escena_{escena}.mp4")
        if not os.path.isfile(r):
            r = os.path.join(pv, "montaje", f"{escena}.mp4")
        return r if os.path.isfile(r) else None
    if que == "montaje":
        return armar_montaje(v)
    if que == "master":
        return _mas_nuevo([os.path.join(sa, "*MASTER*.mp4")])
    if que == "avance":
        return _mas_nuevo([os.path.join(pv, "*AVANCE_ligero*.mp4")]) or _mas_nuevo([os.path.join(sa, "*AVANCE*.mp4")])
    return (_mas_nuevo([os.path.join(sa, "*MASTER*.mp4"), os.path.join(pv, "*AVANCE_ligero*.mp4")])
            or _mas_nuevo([os.path.join(sa, "*AVANCE*.mp4")]) or armar_montaje(v, obligatorio=False)
            or _mas_nuevo([os.path.join(pv, "escena_*.mp4")]))


def armar_montaje(v, obligatorio=True):
    """El montaje del panel hecho video para la tele: cada escena de timeline.json (escena fluida o borrador del montaje;
    hueco negro si aún no está) a su duración, en orden, con la mezcla (o la voz) encima. previews/montaje/_tele.mp4, 720p."""
    c = os.path.join(VIDEOS, v)
    try:
        with open(os.path.join(c, "timeline.json"), encoding="utf-8") as f:
            escenas = json.load(f)["escenas"]
    except (OSError, ValueError, KeyError):
        if obligatorio:
            raise SystemExit(f"{v}: sin timeline.json, no hay montaje que armar")
        return None
    pv = os.path.join(c, "previews")
    fuentes = []
    for e in escenas:
        dur = max(0.1, e["t1"] - e["t0"])
        f = next((p for p in (os.path.join(pv, f"escena_{e['id']}.mp4"), os.path.join(pv, "montaje", f"{e['id']}.mp4"))
                  if os.path.isfile(p)), None)
        fuentes.append((f, dur))
    if not any(f for f, _ in fuentes):
        if obligatorio:
            raise SystemExit(f"{v}: ninguna escena tiene escena fluida ni borrador (python fab.py {v} montaje)")
        return None
    audio = next((p for p in (os.path.join(c, "audio", "final.wav"), *glob.glob(os.path.join(c, "voz", "final", "*.wav")))
                  if os.path.isfile(p)), None)
    salida = os.path.join(pv, "montaje", "_tele.mp4")
    piezas = [f for f, _ in fuentes if f] + ([audio] if audio else []) + [os.path.join(c, "timeline.json")]
    if os.path.isfile(salida) and os.path.getmtime(salida) > max(os.path.getmtime(p) for p in piezas):
        return salida                                          # ya armado con lo más nuevo
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    args, filtros, n = ["ffmpeg", "-y", "-loglevel", "error"], [], 0
    norm = "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=24,setsar=1,format=yuv420p"
    for i, (f, dur) in enumerate(fuentes):
        if f:
            args += ["-i", f]
            filtros.append(f"[{n}:v]{norm},tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},setpts=PTS-STARTPTS[v{i}]")
            n += 1
        else:
            filtros.append(f"color=c=0x101018:s=1280x720:r=24:d={dur:.3f},format=yuv420p[v{i}]")
    filtros.append("".join(f"[v{i}]" for i in range(len(fuentes))) + f"concat=n={len(fuentes)}:v=1:a=0[v]")
    args += (["-i", audio] if audio else []) + ["-filter_complex", ";".join(filtros), "-map", "[v]"]
    if audio:
        args += ["-map", f"{n}:a", "-c:a", "aac", "-b:a", "160k", "-shortest"]
    args += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-movflags", "+faststart", salida + ".tmp.mp4"]
    print(f"  armando el montaje de {v} ({sum(1 for f, _ in fuentes if f)}/{len(fuentes)} escenas)…", flush=True)
    subprocess.run(args, check=True)
    os.replace(salida + ".tmp.mp4", salida)
    return salida


# ====================================================================== tablero (foto del estado de los videos)
def tablero_png(dias=3, maximo=6):
    from PIL import Image, ImageDraw, ImageFont
    import estado as E
    filas = []
    for v in os.listdir(VIDEOS):
        ruta = os.path.join(VIDEOS, v, "ESTADO.md")
        if v.startswith("_") or not os.path.isfile(ruta) or time.time() - os.path.getmtime(ruta) > dias * 86400:
            continue
        f = {k: x.replace("`", "").replace("**", "") for k, x in E.campos(E._leer(ruta)).items()}
        e = E.etapas(os.path.join(VIDEOS, v))
        filas.append((e["yt"] != "ok", os.path.getmtime(ruta), v, f, e))     # primero lo que aún no se sube
    filas.sort(reverse=True)
    filas = [x[2:] for x in filas]

    def cabe(texto, fnt, ancho):
        while texto and d.textlength(texto, font=fnt) > ancho:
            texto = texto[:-2].rstrip() + "…"
        return texto
    W, H = 1920, 1080
    img = Image.new("RGB", (W, H), (12, 11, 20))
    d = ImageDraw.Draw(img)
    fuente = lambda n, negrita=False: ImageFont.truetype(  # noqa: E731
        os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "seguisb.ttf" if negrita else "segoeui.ttf"), n)
    d.text((90, 60), "Fábrica de Animaciones", font=fuente(64, True), fill=(251, 146, 60))
    d.text((90, 140), f"Videos en curso · {time.strftime('%d-%m-%Y %H:%M')}", font=fuente(34), fill=(170, 170, 190))
    y = 230
    if not filas:
        d.text((90, y), "No hay videos movidos en los últimos días.", font=fuente(40), fill=(230, 230, 240))
    for v, f, e in filas[:maximo]:
        d.rounded_rectangle((70, y, W - 70, y + 108), 22, fill=(24, 23, 38))
        d.text((100, y + 12), v, font=fuente(40, True), fill=(240, 240, 250))
        d.text((100, y + 62), cabe(" · ".join(x for x in (f.get("canal", ""), f.get("etapa", "")) if x), fuente(28), 880),
               font=fuente(28), fill=(160, 160, 185))
        x = 1020
        for nombre, clave in (("voz", "voz"), ("mezcla", "mezcla"), ("MASTER", "master"), ("YouTube", "yt")):
            listo = e[clave] == "ok"
            ancho = d.textlength(nombre, font=fuente(26, True)) + 36
            d.rounded_rectangle((x, y + 16, x + ancho, y + 58), 20, fill=(34, 120, 74) if listo else (52, 50, 70))
            d.text((x + 18, y + 20), nombre, font=fuente(26, True), fill=(240, 255, 245) if listo else (150, 150, 170))
            x += ancho + 14
        d.text((1020, y + 66), cabe("Sigue: " + f.get("siguiente", "—"), fuente(26), W - 1120), font=fuente(26), fill=(200, 200, 215))
        y += 124
    if len(filas) > maximo:
        d.text((90, y + 10), f"y {len(filas) - maximo} más · python fab.py estado", font=fuente(28), fill=(130, 130, 150))
    ruta = os.path.join(CACHE_VOZ, "tele_tablero.png")
    os.makedirs(CACHE_VOZ, exist_ok=True)
    img.save(ruta)
    return ruta, len(filas)


# ====================================================================== línea de comandos
def _ruta(r):
    """Ruta de archivo tal como la escribió quien llamó: `fab.py` corre esto con cwd en la fábrica, pero el skill global
    «avisar-y-decidir» lo llama desde cualquier proyecto (FAB_CWD = carpeta de origen)."""
    if not r or os.path.isabs(r):
        return r
    origen = os.path.join(os.environ.get("FAB_CWD", os.getcwd()), r)
    return origen if os.path.exists(origen) else r


def _opcion(resto, nombre):
    return next((resto[i + 1] for i, x in enumerate(resto[:-1]) if x == nombre), "")


def _texto_respaldo(cmd, resto):
    """Lo que dice la PC cuando la tele no está. Videos de la fábrica → «míralo en el panel»; cualquier otro proyecto →
    genérico («en la computadora»)."""
    texto = next((x for x in resto if not x.startswith("--")), "")
    pregunta = texto if cmd == "preguntar" else _opcion(resto, "--pregunta")
    opciones = [o.strip() for o in _opcion(resto, "--opciones").split("|") if o.strip()]
    if cmd == "aviso":
        sueltos, saltar = [], False
        for x in resto:
            if saltar:
                saltar = False
            elif x in ("--titulo", "--estilo"):
                saltar = True
            elif not x.startswith("--"):
                sueltos.append(x)
        return ". ".join(t for t in (_opcion(resto, "--titulo"), " ".join(sueltos)) if t)
    if cmd == "tablero":
        return "Te quería enseñar el tablero de la fábrica en la tele, pero no está prendida. Está en el panel."
    if cmd == "revisar":
        cual = texto if os.path.isdir(os.path.join(VIDEOS, texto)) else ""
        return (f"Hay un video{' de ' + cual if cual else ''} para que lo revises en la tele, pero no está prendida. "
                "Cuando la prendas, avísame y te lo mando.")
    if cmd == "video" and os.path.isdir(os.path.join(VIDEOS, texto)):
        dicho = f"Hay algo de {texto} para que lo revises. La tele no está prendida: míralo en el panel de la fábrica."
    elif cmd in ("video", "imagen"):
        cosa, lo = ("un video", "lo") if cmd == "video" else ("una imagen", "la")
        dicho = f"Te quería enseñar {cosa} en la tele, pero no está prendida. Te {lo} dejo en la computadora."
    else:
        dicho = ""
    if pregunta:
        p = pregunta.rstrip(" .")
        dicho += f" Tengo una pregunta para ti: {p}{'' if p.endswith('?') else '.'}"
        if opciones:
            dicho += " Las opciones son: " + ", ".join(opciones[:-1]) + (" o " if len(opciones) > 1 else "") + opciones[-1] + "."
        dicho += " Contéstame en la computadora."
    return dicho.strip()


def _origen_defecto():
    """«fabrica» si lo llama la fábrica; «claude» si viene de otro proyecto (skill avisar-y-decidir). La tele los separa."""
    cwd = os.path.abspath(os.environ.get("FAB_CWD", os.getcwd())).lower()
    return "fabrica" if cwd.startswith(RAIZ.lower()) else "claude"


def _modo_txt(m):
    nombre = {"todo": "🔔 Todo", "normal": "⭐ Normal", "urgentes": "🚨 Solo urgentes", "silencio": "🌙 No molestar"}.get(m.get("modo"), m.get("modo"))
    h = m.get("no_molestar_hasta") or 0
    return nombre + (f" (hasta las {time.strftime('%H:%M', time.localtime(h / 1000))})" if h else "")


def main(argv):
    if not argv:
        ip, st = tele()
        print(f"Tele: {st.get('nombre')} ({ip}) · Puente TV {st.get('version')}")
        print(f"  mostrando algo: {'sí' if st.get('mostrando') else 'no'} · en pantalla: {st.get('app') or '—'} {st.get('info') or ''}")
        print(f"  permisos: dibujar encima={'sí' if st.get('overlay') else 'NO'} · pausar lo que se ve={'sí' if st.get('control') else 'NO'}")
        print(f"  espejo de `fab.py avisar`: {'activo' if conf()['espejo_avisar'] else 'apagado'} (nucleo/datos/tele.json)")
        if st.get("modo"):
            print(f"  modo: {_modo_txt(st)} · bandeja: {st.get('bandeja', 0)} sin ver · tablero: {'sí' if st.get('tablero') else 'no'}")
        return
    cmd, resto = argv[0], argv[1:]
    if cmd == "disponible":
        # para el skill global «avisar-y-decidir»: ¿la tele está prendida y con pantalla? (código 0 = sí, 4 = no)
        si = disponible()
        print("sí" if si else "no")
        sys.exit(0 if si else 4)
    if cmd in ("aviso", "video", "preguntar", "imagen", "tablero", "revisar") and not disponible():
        # REGLA (4-nov-2026): primero la tele; si no está (apagada, en reposo, sin red), la voz de la PC como antes
        por_voz(_texto_respaldo(cmd, resto))
        sys.exit(4)
    ap = argparse.ArgumentParser(prog=f"fab.py tele {cmd}")
    if cmd == "aviso":
        ap.add_argument("texto", nargs="+")
        ap.add_argument("--titulo", default="")
        ap.add_argument("--estilo", default="info", choices=["info", "importante", "urgente", "listo"])
        ap.add_argument("--no-pausar", action="store_true")
        ap.add_argument("--sin-voz", action="store_true")
        ap.add_argument("--nivel", choices=["urgente", "importante", "info"])
        ap.add_argument("--origen", default=None, choices=["fabrica", "cnb", "claude", "puente"])
        a = ap.parse_args(resto)
        d = aviso(" ".join(a.texto), a.titulo, a.estilo, pausar=False if a.no_pausar else None, voz=not a.sin_voz,
                  nivel=a.nivel, origen=a.origen or _origen_defecto())
        print({"banner": "Aviso en la tele (en la esquinita, sin pausar).",
               "bandeja": "Quedó en la bandeja de la tele por el modo que eligió el usuario (no se repite por las bocinas)."
               }.get(d.get("entrega"), "Aviso en la tele."))
    elif cmd in ("video", "preguntar"):
        if cmd == "video":
            ap.add_argument("v")
            ap.add_argument("que", nargs="*", help="avance | master | montaje | escena <id>")
            ap.add_argument("--pregunta")
        else:
            ap.add_argument("pregunta")
            ap.add_argument("--video", dest="v")
        ap.add_argument("--opciones", default="", help='separadas con «|»: "Sí|No|Después"')
        ap.add_argument("--mensaje", default="")
        ap.add_argument("--momento", default="final", choices=["final", "durante", "siempre"])
        ap.add_argument("--esperar", type=int, default=0, help="segundos esperando la respuesta (0 = no esperar)")
        a = ap.parse_args(resto)
        opciones = [o.strip() for o in a.opciones.split("|") if o.strip()]
        archivo = None
        if cmd == "preguntar" and a.v and not os.path.isdir(os.path.join(VIDEOS, a.v)):
            archivo = _ruta(a.v)            # --video con un archivo suelto (otro proyecto), no un video de la fábrica
            if not os.path.isfile(archivo):
                raise SystemExit(f"--video: no existe videos/{a.v} ni el archivo {archivo}")
        if cmd == "video":
            que = a.que[0] if a.que else None
            if not os.path.isdir(os.path.join(VIDEOS, a.v)):
                a.v = _ruta(a.v)
            archivo = elegir(a.v, que, a.que[1] if len(a.que) > 1 else None)
            if not archivo:
                raise SystemExit(f"{a.v}: no encontré qué mandar ({que or 'nada renderizado todavía'})")
            print(f"  → {os.path.relpath(archivo, RAIZ)} ({os.path.getsize(archivo) / 2**20:.0f} MB)")
        if cmd == "video" and not a.pregunta:
            video(archivo)
            print("Reproduciendo en la tele.")
            return
        if not opciones:
            opciones = ["Sí", "No"]
        v = a.v if a.v and os.path.isdir(os.path.join(VIDEOS, a.v)) else None
        pid = preguntar(a.pregunta, opciones, a.mensaje, archivo, a.momento, v, origen="fabrica" if v else _origen_defecto())
        if ULTIMA_ENTREGA == "bandeja":
            print("POSPUESTA: la tele está en «no molestar» o «solo urgentes»; quedó en su bandeja. Pregunta en el chat.")
            sys.exit(5)
        print(f"Pregunta {pid} en la tele: {a.pregunta} [{' | '.join(opciones)}]")
        if a.esperar:
            elegido = esperar(pid, a.esperar, v, a.pregunta)
            print(f"RESPUESTA: {elegido}" if elegido else "Sin respuesta (se acabó la espera o se cerró).")
            sys.exit(0 if elegido else 3)
        print(f"  ver después: python fab.py tele respuestas   (id {pid})")
    elif cmd == "revisar":
        ap.add_argument("v", nargs="?", help="video de la fábrica (o una ruta .mp4)")
        ap.add_argument("que", nargs="*", help="avance | master | montaje | escena <id>")
        ap.add_argument("--archivo", help="cualquier video, de cualquier proyecto")
        ap.add_argument("--titulo", default="")
        ap.add_argument("--opciones", default="Aprobado|Hay que corregir", help='veredictos separados con «|»')
        ap.add_argument("--esperar", type=int, default=0, help="segundos esperando a que termine (0 = no esperar)")
        a = ap.parse_args(resto)
        v = a.v if a.v and os.path.isdir(os.path.join(VIDEOS, a.v)) else None
        if a.archivo or (a.v and not v):
            archivo = _ruta(a.archivo or a.v)
            if not os.path.isfile(archivo):
                raise SystemExit(f"No existe el archivo {archivo}")
        elif v:
            que = a.que[0] if a.que else None
            archivo = elegir(v, que, a.que[1] if len(a.que) > 1 else None)
            if not archivo:
                raise SystemExit(f"{v}: no encontré qué revisar ({que or 'nada renderizado todavía'})")
        else:
            raise SystemExit("Dime qué revisar: un video de la fábrica o --archivo ruta.mp4")
        print(f"  → {os.path.relpath(archivo, RAIZ) if v else archivo} ({os.path.getsize(archivo) / 2**20:.0f} MB)")
        titulo = a.titulo or (v or os.path.splitext(os.path.basename(archivo))[0])
        opciones = [o.strip() for o in a.opciones.split("|") if o.strip()] or ["Aprobado", "Hay que corregir"]
        pid = preguntar(titulo, opciones, "", archivo, "final", v, estilo="info", modo="revision",
                        origen="fabrica" if v else _origen_defecto())
        if ULTIMA_ENTREGA == "bandeja":
            print("POSPUESTA: la tele está en «no molestar» o «solo urgentes»; quedó en su bandeja. Pregunta en el chat.")
            sys.exit(5)
        print(f"Revisión {pid} en la tele: OK pausa · ◀ ▶ 10 s · ▼ marcar · ▲ marcas · Atrás: veredicto")
        if not a.esperar:
            print(f"  luego: python fab.py tele revisar-resultado {pid} {v or archivo}")
            return
        r = esperar_revision(pid, a.esperar)
        if not r:
            print("Sin revisión (se acabó la espera sin marcas ni veredicto).")
            sys.exit(3)
        md, filas, veredicto = guardar_revision(r, archivo, v, titulo)
        for hora, tipo, jpg in filas:
            print(f"MARCA {hora} · {tipo}" + (f" → {jpg}" if jpg else ""))
        print(f"VEREDICTO: {veredicto}")
        print(f"Revisión guardada: {md}")
    elif cmd == "revisar-resultado":
        ap.add_argument("pid")
        ap.add_argument("v", help="video de la fábrica o ruta del archivo que se revisó")
        a = ap.parse_args(resto)
        v = a.v if os.path.isdir(os.path.join(VIDEOS, a.v)) else None
        archivo = elegir(v) if v else _ruta(a.v)
        r = respuesta(a.pid)
        if r.get("estado") not in ("respondida", "cerrada") and not r.get("marcas"):
            print(f"Todavía no termina (estado: {r.get('estado')}).")
            sys.exit(3)
        md, filas, veredicto = guardar_revision(r, archivo, v)
        for hora, tipo, jpg in filas:
            print(f"MARCA {hora} · {tipo}" + (f" → {jpg}" if jpg else ""))
        print(f"VEREDICTO: {veredicto}\nRevisión guardada: {md}")
    elif cmd == "modo":
        ap.add_argument("modo", nargs="?", choices=["todo", "normal", "urgentes", "silencio", "no-molestar"])
        ap.add_argument("--minutos", type=int, default=0)
        ap.add_argument("--hasta", choices=["manana"])
        a = ap.parse_args(resto)
        if a.modo:
            cuerpo = {"modo": "silencio" if a.modo == "no-molestar" else a.modo}
            if a.minutos:
                cuerpo["minutos"] = a.minutos
            if a.hasta:
                cuerpo["hasta"] = a.hasta
            _post_json("/modo", cuerpo)
        m = modo_tele()
        print(f"Modo de la tele: {_modo_txt(m)}" if m else "La tele no tiene modos (¿falta actualizar Puente TV?).")
    elif cmd == "bandeja":
        ip, _ = tele()
        d = requests.get(f"http://{ip}:{PUERTO}/bandeja", params={"pc": "fabrica"}, timeout=5).json()
        for j in d.get("lista", [])[:30]:
            print(f"  {time.strftime('%d-%b %H:%M', time.localtime(j.get('hora', 0) / 1000))}  "
                  f"{'•' if not j.get('visto') else ' '} [{j.get('origen')}/{j.get('nivel')}] {j.get('titulo')} — {j.get('mensaje', '')[:80]}")
        print(f"Sin ver: {d.get('sin_ver', 0)}")
    elif cmd == "imagen":
        ap.add_argument("ruta")
        ap.add_argument("--segundos", type=int, default=15)
        ap.add_argument("--titulo")
        a = ap.parse_args(resto)
        imagen(_ruta(a.ruta), a.segundos, a.titulo)
        print("Imagen en la tele.")
    elif cmd == "tablero":
        ap.add_argument("--segundos", type=int, default=25)
        ap.add_argument("--dias", type=int, default=3)
        ap.add_argument("--vivo", action="store_true", help="el tablero en vivo de la PC (fábrica + CNB) en lugar de la foto")
        a = ap.parse_args(resto)
        if a.vivo:
            _post_json("/tablero/ver", {})
            print("Tablero en vivo en la tele (el mismo del protector de pantalla; Atrás para salir).")
            return
        ruta, n = tablero_png(a.dias)
        imagen(ruta, a.segundos, None)
        print(f"Tablero en la tele ({n} videos en curso). Imagen: {ruta}")
    elif cmd == "respuestas":
        try:
            ip, _ = tele()
            lista = requests.get(f"http://{ip}:{PUERTO}/respuestas", params={"pc": "fabrica"}, timeout=5).json().get("lista", [])
        except (SystemExit, requests.RequestException, ValueError):
            lista = []
        for r in lista:
            print(f"  {r.get('hora', '')}  {r.get('id')}  «{r.get('titulo')}» → {r.get('opcion') or r.get('estado')}")
        if not lista:
            print("  (la tele no tiene respuestas guardadas)")
        print(f"Registro de la fábrica: {RESPUESTAS}")
    elif cmd == "cerrar":
        requests.post(_url("/cerrar", todo=1), timeout=10)
        print("Listo: la tele dejó de mostrar.")
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
