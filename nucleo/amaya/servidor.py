# -*- coding: utf-8 -*-
"""Estudio Amaya (10-nov-2026): el servidor local de la app de Amaya (la hija de Edson, 12 años).

    python fab.py amaya [--abrir]          levanta el servidor en 127.0.0.1:8795 (desacoplado) y, con --abrir, lo abre aquí
    python nucleo/amaya/servidor.py         lo mismo en primer plano

La app Android (nucleo/amaya/android, «Estudio Amaya») abre clicknbusiness.com.mx/amaya/ → túnel de hoy → puerta
(nucleo/panel_remoto.py, ruta /amaya/… con la LLAVE DE AMAYA, que solo abre esta ruta) → este servidor.

Qué hace:
  - Chat con la GUÍA: `claude -p` (sonnet, sin herramientas, sin CLAUDE.md) con el sistema nucleo/amaya/guia.md + el catálogo
    de estilos y voces. Ve sus fotos (van como imagen) y oye sus audios (Whisper «small» en CPU los transcribe).
    Contesta con marcas que la app pinta: [[estilo:ID]], [[voz:ID]], [[opciones: a | b]], [[ficha]]{…}[[/ficha]].
  - Producción: la ficha que ella confirma lanza un `claude -p` COMPLETO en C:\\FabricaAnimaciones (CLAUDE.md, herramientas)
    con nucleo/amaya/produccion.md añadido: hace videos/amaya_<algo>/ hasta el MASTER. Uno a la vez (cola), con tope diario.
    Su registro (stream-json) queda en amaya_estudio/trabajos/<id>.log y los avances para ella en <id>.avances.jsonl.
  - Voces de ElevenLabs (las de las cuentas con saldo, nunca las clonadas), muestras gratis + «dilo con mi frase» con tope.
  - Sus estilos propios, favoritos, fotos y audios subidos, «Mis videos» con versión ligera para el teléfono.
Todo lo de ella vive en amaya_estudio/ (fuera de git). Límites y carta de papá: amaya_estudio/config.json (papá lo edita).
"""
import base64
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import unicodedata
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.dirname(AQUI)
RAIZ = os.path.dirname(NUCLEO)
DATOS = os.path.join(RAIZ, "amaya_estudio")
VIDEOS = os.path.join(RAIZ, "videos")
PUERTO = 8795
FFMPEG = shutil.which("ffmpeg") or r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE = shutil.which("ffprobe") or r"C:\ffmpeg\bin\ffprobe.exe"
DESACOPLADO = 0x00000008 | 0x00000200 | 0x08000000
SIN_VENTANA = getattr(subprocess, "CREATE_NO_WINDOW", 0)

CONFIG_DEF = {
    "nombre": "Amaya",
    "firma": "Hecha con 💜 por papá Edson",
    "carta": ("Amaya: esta app la hice para ti. Aquí puedes inventar tus propios videos: tú pones la idea y la fábrica de "
              "la casa los dibuja con el estilo de tu canal y les pone tu voz y música. Pregúntale lo que quieras a Claude y "
              "diviértete creando. Estoy orgulloso de ti. — Papá"),
    "limites": {"mensajes_dia": 120, "videos_dia": 2, "pruebas_voz_dia": 12, "audios_por_video": 5},
    "avisar_a_papa": True,
    "modelo_guia": "sonnet",
    "modelo_produccion": "",
    # 10-nov-2026 (el usuario): un solo estilo y una sola voz, los del canal de Amaya; nada de pestañas Estilos/Voces
    "canal": {"alias": "canal_amaya", "nombre": "Amaya Vibes", "voz": "9Godp7dNohUvXk6qp0gS", "voz_nombre": "Regina"},
}
ESTILO_CANAL = {
    "id": "coquette", "nombre": "Scrapbook coquette", "emoji": "🎀", "auto": True,
    "desc": ("el estilo de su canal Amaya Vibes: vichy rosa y rayas pastel, letras recortadas que caen, stickers con borde "
             "blanco, notitas adhesivas, sellos ¡SÍ PÍDELO! / NI SE TE OCURRA, su avatar de presentadora y el final de suscripción"),
    "doc": "docs/estilo_scrapbook_coquette.md", "ejemplo": "videos/amaya_navidad/",
}
DENEGADOS = [   # reglas que la producción no puede saltarse (las de «deny» mandan aunque el modo sea bypass)
    "Bash(git push *)", "Bash(git commit *)", "Bash(git reset *)", "Bash(git checkout *)", "Bash(git rebase *)",
    "Bash(python fab.py yt *)", "Bash(python fab.py limpiar *)", "Bash(python fab.py compartir *)",
    "Bash(python fab.py panel *)", "Bash(python fab.py envivo *)", "Bash(*pagina.py*)", "Bash(*panel_remoto*)",
    "Bash(rm -rf *)", "Bash(*taskkill*)", "Bash(*Stop-Process*)",
    "PowerShell(git push *)", "PowerShell(git commit *)", "PowerShell(python fab.py yt *)", "PowerShell(*pagina.py*)",
    "PowerShell(*taskkill*)", "PowerShell(*Stop-Process*)", "PowerShell(Remove-Item -Recurse *)",
    "Edit(/CLAUDE.md)", "Write(/CLAUDE.md)", "Edit(/nucleo/**)", "Write(/nucleo/**)", "Edit(/canales/**)", "Write(/canales/**)",
    "Edit(/docs/**)", "Write(/docs/**)", "Edit(/fab.py)", "Write(/fab.py)",
]

_cand = threading.RLock()
CHAT_VIVO = {"pensando": False, "parcial": "", "desde": 0.0, "error": ""}


# ======================================================================== utilidades
def ruta(*p):
    return os.path.join(DATOS, *p)


def leer_json(path, defecto=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defecto


def guardar_json(path, datos):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def config():
    c = leer_json(ruta("config.json"))
    if c is None:
        c = json.loads(json.dumps(CONFIG_DEF))
        guardar_json(ruta("config.json"), c)
    for k, v in CONFIG_DEF.items():
        c.setdefault(k, v)
    for k, v in CONFIG_DEF["limites"].items():
        c["limites"].setdefault(k, v)
    return c


def hoy():
    return time.strftime("%Y-%m-%d")


def uso(sumar=None):
    with _cand:
        p = ruta("uso", hoy() + ".json")
        u = leer_json(p, {}) or {}
        if sumar:
            u[sumar] = u.get(sumar, 0) + 1
            guardar_json(p, u)
        return u


def restantes():
    lim, u = config()["limites"], uso()
    return {"mensajes": max(0, lim["mensajes_dia"] - u.get("mensajes", 0)),
            "videos": max(0, lim["videos_dia"] - u.get("videos", 0)),
            "pruebas_voz": max(0, lim["pruebas_voz_dia"] - u.get("pruebas_voz", 0))}


def slug(txt, n=28):
    t = unicodedata.normalize("NFKD", txt or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", "_", t).strip("_")
    return t[:n].strip("_") or "video"


def log(*a):
    try:
        os.makedirs(DATOS, exist_ok=True)
        with open(ruta("servidor.log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")
    except OSError:
        pass


def claude_exe():
    return shutil.which("claude") or shutil.which("claude.cmd") or "claude"


def pid_vivo(pid):
    if not pid:
        return False
    try:
        import psutil
        return psutil.pid_exists(int(pid)) and psutil.Process(int(pid)).status() != "zombie"
    except Exception:
        return False


# ======================================================================== catálogo: estilos y voces
def estilos_base():
    return (leer_json(os.path.join(AQUI, "estilos.json"), {}) or {}).get("estilos", [])


def estilos_mios():
    d = ruta("estilos")
    out = []
    if os.path.isdir(d):
        for n in sorted(os.listdir(d)):
            if n.endswith(".json"):
                e = leer_json(os.path.join(d, n))
                if e:
                    out.append(e)
    return out


def estilos_todos():
    favs = set((leer_json(ruta("favoritas.json"), {}) or {}).get("estilo", []))
    out = []
    for e in estilos_base() + estilos_mios():
        e = dict(e)
        e["favorito"] = e["id"] in favs
        e["img_url"] = f"img/estilo/{e['id']}.jpg"
        for k in ("doc", "ejemplo", "img"):
            e.pop(k, None)
        out.append(e)
    return out


def estilo(eid):
    if eid == ESTILO_CANAL["id"]:
        return ESTILO_CANAL
    return next((e for e in estilos_base() + estilos_mios() if e["id"] == eid), None)


_VOCES = {"t": 0, "datos": None}
ACENTOS_ES = ("latin", "mexican", "peninsular", "spanish", "colombian", "argentine", "peruvian", "chilean", "cuban",
              "dominican", "caribbean", "venezuelan")


def _eleven():
    sys.modules.setdefault("config", None)          # tts_eleven sin video activo (no carga config.py de un video)
    if NUCLEO not in sys.path:
        sys.path.insert(0, NUCLEO)
    import tts_eleven
    return tts_eleven


def voces():
    """Voces de las cuentas de ElevenLabs que tienen saldo (caché de 6 h). Nunca las clonadas ni las generadas."""
    if _VOCES["datos"] and time.time() - _VOCES["t"] < 6 * 3600:
        return _VOCES["datos"]
    cache = leer_json(ruta("voces_cache.json"))
    if cache and time.time() - cache.get("t", 0) < 6 * 3600:
        _VOCES.update(t=cache["t"], datos=cache["datos"])
        return cache["datos"]
    import requests
    T = _eleven()
    todas = {}
    for n, k in T.cuentas():
        try:
            if T.saldo(k) < 400:
                continue
            vs = requests.get(f"{T.URL}/voices", headers={"xi-api-key": k}, timeout=30).json().get("voices", [])
        except Exception as e:
            log("voces: cuenta", n, "falló", repr(e)[:120])
            continue
        for v in vs:
            if v.get("category") in ("cloned", "generated"):
                continue
            lab = v.get("labels") or {}
            nombre = v.get("name", "").split(" - ")[0].split(" – ")[0].split(" —")[0].strip()
            todas.setdefault(v["voice_id"], {
                "id": v["voice_id"], "nombre": nombre[:26], "largo": v.get("name", "")[:60],
                "genero": {"female": "chica", "male": "chico"}.get(lab.get("gender"), "neutra"),
                "acento": lab.get("accent") or "", "muestra": v.get("preview_url") or "",
                "es": any(a in (lab.get("accent") or "").lower() for a in ACENTOS_ES)})
    rec = (leer_json(os.path.join(AQUI, "voces.json"), {}) or {}).get("recomendadas", [])
    lista = []
    for r in rec:
        v = todas.get(r["id"])
        if v:
            lista.append(dict(v, nombre=r["nombre"], desc=r["desc"], grupo=r["grupo"], emoji=r.get("emoji", "🎙️"), recomendada=True))
    ids = {v["id"] for v in lista}
    otras = sorted((v for v in todas.values() if v["id"] not in ids), key=lambda v: (not v["es"], v["nombre"]))
    for v in otras:
        lista.append(dict(v, desc=f"{v['largo']}", grupo="mas", emoji="🎙️", recomendada=False))
    datos = {"t": time.time(), "datos": lista}
    if lista:
        guardar_json(ruta("voces_cache.json"), datos)
    _VOCES.update(t=time.time(), datos=lista)
    return lista


def voz(vid):
    return next((v for v in voces() if v["id"] == vid), None)


def probar_voz(vid, texto):
    texto = re.sub(r"\s+", " ", re.sub(r"[\[\]<>{}]", "", texto or "")).strip()[:140] or f"¡Hola {config()['nombre']}! Así sueno yo."
    h = hashlib.sha1(f"{vid}|{texto}".encode()).hexdigest()[:16]
    out = ruta("pruebas_voz", h + ".mp3")
    if os.path.exists(out):
        return h, None
    if restantes()["pruebas_voz"] <= 0:
        return None, "Ya usaste todas las pruebas de voz de hoy. ¡Mañana hay más!"
    T = _eleven()
    r = T.post(f"text-to-speech/{vid}?output_format=mp3_44100_128",
               json={"text": texto, "model_id": "eleven_v4_turbo", "voice_settings": {"stability": 0.45, "similarity_boost": 0.8}},
               timeout=60)
    if r.status_code != 200:
        log("probar voz", vid, r.status_code, r.text[:200])
        return None, "Esa voz no pudo hablar ahorita. Prueba otra 🙏"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as f:
        f.write(r.content)
    uso("pruebas_voz")
    return h, None


# ======================================================================== subidas: fotos y audios
_WHISPER = {"m": None}
_wh_cand = threading.Lock()


def transcribir(path):
    with _wh_cand:
        if _WHISPER["m"] is None:
            from faster_whisper import WhisperModel
            _WHISPER["m"] = WhisperModel("small", device="cpu", compute_type="int8")
        seg, _ = _WHISPER["m"].transcribe(path, language="es", vad_filter=True, beam_size=3)
        return " ".join(s.text.strip() for s in seg).strip()


def guardar_subida(datos, tipo, nombre=""):
    from PIL import Image, ImageOps
    sid = time.strftime("%m%d%H%M%S") + uuid.uuid4().hex[:4]
    d = ruta("subidos")
    os.makedirs(d, exist_ok=True)
    if tipo == "foto":
        try:
            im = ImageOps.exif_transpose(Image.open(io.BytesIO(datos))).convert("RGB")
        except Exception:
            return None, "No pude abrir esa foto. ¿Es JPG o PNG?"
        im.thumbnail((1600, 1600))
        im.save(os.path.join(d, f"f{sid}.jpg"), quality=88)
        im.thumbnail((420, 420))
        im.save(os.path.join(d, f"f{sid}_mini.jpg"), quality=80)
        return {"id": f"f{sid}", "tipo": "foto", "url": f"subidos/f{sid}.jpg", "mini": f"subidos/f{sid}_mini.jpg",
                "nombre": nombre[:60]}, None
    ext = ".webm"
    if datos[:4] == b"OggS":
        ext = ".ogg"
    elif datos[4:8] == b"ftyp":
        ext = ".m4a"
    p = os.path.join(d, f"a{sid}{ext}")
    with open(p, "wb") as f:
        f.write(datos)
    try:
        texto = transcribir(p)
    except Exception as e:
        log("whisper", repr(e)[:200])
        texto = ""
    return {"id": f"a{sid}", "tipo": "audio", "url": f"subidos/a{sid}{ext}", "texto": texto}, None


def adjunto_path(aid):
    if not re.match(r"^[fa][0-9a-f]{10,16}$", aid or ""):
        return None
    d = ruta("subidos")
    for n in os.listdir(d) if os.path.isdir(d) else []:
        if n.startswith(aid) and "_mini" not in n:
            return os.path.join(d, n)
    return None


# ======================================================================== chat con la guía
def chat():
    return leer_json(ruta("chat.json")) or {"sid": None, "turnos": 0, "mensajes": []}


def guardar_chat(c):
    guardar_json(ruta("chat.json"), c)


def nuevo_mensaje(de, texto, adjuntos=None, **extra):
    with _cand:
        c = chat()
        n = (c["mensajes"][-1]["n"] + 1) if c["mensajes"] else 1
        m = dict(n=n, de=de, texto=texto, adjuntos=adjuntos or [], t=time.time(), **extra)
        c["mensajes"].append(m)
        guardar_chat(c)
        return m


def sistema_guia():
    """guia.md + catálogo (cambia poco: así la caché del modelo sirve entre mensajes)."""
    txt = open(os.path.join(AQUI, "guia.md"), encoding="utf-8").read()
    k = config()["canal"]
    return (txt + f"\n\n## Su canal (fijo: no se pregunta ni se cambia)\n- Canal: {k['nombre']}.\n"
            f"- Estilo: {ESTILO_CANAL['emoji']} {ESTILO_CANAL['nombre']} — {ESTILO_CANAL['desc']}.\n"
            f"- Voz: {k['voz_nombre']} (la eligió ella; narra como si fuera Amaya: «Soy Amaya»).\n")


def estado_app():
    r = restantes()
    vids = videos()[:8]
    t = trabajo_activo()
    linea_v = "; ".join(f"{v['alias']} «{v['titulo']}» ({v['estado']})" for v in vids) or "ninguno todavía"
    return (f"[Nota de la app, no la menciones tal cual: hoy es {time.strftime('%d/%m/%Y %H:%M')}. Le quedan hoy "
            f"{r['videos']} videos por crear y {r['mensajes']} mensajes. "
            + (f"La fábrica está haciendo «{t['ficha'].get('titulo')}» ({t['estado']}); su último avance (ya se lo mandó al chat "
               f"con imagen o voz): «{(t.get('pasos') or [{}])[-1].get('txt', '-')}». " if t else "La fábrica está libre. ")
            + f"Sus videos: {linea_v}.]")


def correr_guia(m):
    """Manda el mensaje m de Amaya a la guía (en un hilo) y guarda la respuesta."""
    cfg = config()
    c = chat()
    carpeta = ruta("_claude")
    os.makedirs(carpeta, exist_ok=True)
    mcp = os.path.join(carpeta, "mcp_vacio.json")
    if not os.path.exists(mcp):
        open(mcp, "w").write('{"mcpServers":{}}')
    sp = os.path.join(carpeta, "sistema.md")
    with open(sp, "w", encoding="utf-8") as f:
        f.write(sistema_guia())
    sid = c.get("sid")
    if c.get("turnos", 0) >= 40:                      # conversación muy larga: sesión nueva con lo último como recuerdo
        sid = None
    texto = m["texto"] or ""
    for a in m.get("adjuntos", []):
        if a.get("tipo") == "audio":
            texto += f"\n(Mandó un audio; dice: «{a.get('texto') or '(no se entendió)'}»)"
        elif a.get("tipo") == "foto":
            texto += f"\n(Mandó una foto, id {a['id']}{': ' + a['nombre'] if a.get('nombre') else ''})"
    previo = ""
    if not sid:
        ult = [x for x in c["mensajes"][:-1] if x["de"] in ("amaya", "claude") and not x.get("avance")][-12:]
        if ult:
            previo = "Lo último que platicaron (de otra sesión):\n" + "\n".join(
                f"{'Amaya' if x['de'] == 'amaya' else 'Tú'}: {x['texto'][:400]}" for x in ult) + "\n\n"
    bloques = [{"type": "text", "text": estado_app() + "\n\n" + previo + "Amaya: " + texto.strip()}]
    from PIL import Image
    for a in m.get("adjuntos", []):
        if a.get("tipo") == "foto":
            p = adjunto_path(a["id"])
            if p:
                im = Image.open(p).convert("RGB")
                im.thumbnail((1024, 1024))
                b = io.BytesIO()
                im.save(b, "JPEG", quality=82)
                bloques.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                             "data": base64.b64encode(b.getvalue()).decode()}})
    entrada = json.dumps({"type": "user", "message": {"role": "user", "content": bloques}}, ensure_ascii=False) + "\n"
    cmd = [claude_exe(), "-p", "--model", cfg.get("modelo_guia") or "sonnet", "--system-prompt-file", sp,
           "--system-prompt-snapshot", "off", "--setting-sources", "", "--strict-mcp-config", "--mcp-config", mcp,
           "--tools", "", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
           "--include-partial-messages"]
    if sid:
        cmd += ["--resume", sid]
    CHAT_VIVO.update(pensando=True, parcial="", desde=time.time(), error="")
    final, nuevo_sid, err = "", sid, ""
    try:
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=carpeta,
                             env=dict(os.environ, MAX_THINKING_TOKENS="0"), creationflags=SIN_VENTANA)
        p.stdin.write(entrada.encode("utf-8"))
        p.stdin.close()
        inicio = time.time()
        for crudo in p.stdout:
            if time.time() - inicio > 240:
                p.kill()
                err = "tardó demasiado"
                break
            try:
                ev = json.loads(crudo.decode("utf-8", "replace"))
            except ValueError:
                continue
            tipo = ev.get("type")
            if tipo == "stream_event":
                e = ev.get("event") or {}
                if e.get("type") == "content_block_delta" and (e.get("delta") or {}).get("type") == "text_delta":
                    CHAT_VIVO["parcial"] += e["delta"].get("text", "")
            elif tipo == "system" and ev.get("session_id"):
                nuevo_sid = ev["session_id"]
            elif tipo == "result":
                nuevo_sid = ev.get("session_id") or nuevo_sid
                if ev.get("is_error"):
                    err = str(ev.get("result") or ev.get("subtype"))[:300]
                else:
                    final = ev.get("result") or CHAT_VIVO["parcial"]
        p.wait(timeout=30)
        if not final and not err:
            err = (p.stderr.read().decode("utf-8", "replace") or "sin respuesta")[-300:]
    except Exception as e:
        err = repr(e)[:300]
    with _cand:
        c = chat()
        if final:
            c["sid"] = nuevo_sid
            c["turnos"] = (c.get("turnos", 0) + 1) if nuevo_sid == sid else 1
            guardar_chat(c)
            nuevo_mensaje("claude", final.strip())
        else:
            log("guía falló", err)
            if sid and ("session" in err.lower() or "conversation" in err.lower()):
                c["sid"] = None
                guardar_chat(c)
            nuevo_mensaje("sistema", "Uy, no pude contestarte ahorita 😵‍💫 Vuelve a intentarlo en un momento "
                                     "(si sigue pasando, avísale a papá).")
        CHAT_VIVO.update(pensando=False, parcial="", error=err)


# ======================================================================== producción
def trabajos():
    d = ruta("trabajos")
    out = []
    if os.path.isdir(d):
        for n in os.listdir(d):
            if n.endswith(".json") and not n.endswith(".tmp"):
                t = leer_json(os.path.join(d, n))
                if t:
                    out.append(t)
    return sorted(out, key=lambda t: t.get("creado", 0), reverse=True)


_LECTURAS = {}


def leer_log(t):
    """Resume el registro stream-json de un trabajo: actividad actual, último texto, resultado (con caché por tamaño)."""
    p = ruta("trabajos", t["id"] + ".log")
    try:
        tam = os.path.getsize(p)
    except OSError:
        return {}
    c = _LECTURAS.get(t["id"])
    if c and c["tam"] == tam:
        return c["r"]
    r = {"actividad": "", "ultimo": "", "resultado": None, "error": False, "sid": None, "herramientas": 0, "t": os.path.getmtime(p)}
    with open(p, encoding="utf-8", errors="replace") as f:
        for ln in f:
            try:
                ev = json.loads(ln)
            except ValueError:
                continue
            if ev.get("session_id"):
                r["sid"] = ev["session_id"]
            if ev.get("type") == "assistant":
                for b in (ev.get("message") or {}).get("content", []):
                    if b.get("type") == "text" and b.get("text", "").strip():
                        r["ultimo"] = b["text"].strip()
                    elif b.get("type") == "tool_use":
                        r["herramientas"] += 1
                        r["actividad"] = actividad(b.get("name", ""), b.get("input") or {})
            elif ev.get("type") == "result":
                r["resultado"] = ev.get("result") or r["ultimo"]
                r["error"] = bool(ev.get("is_error"))
    _LECTURAS[t["id"]] = {"tam": tam, "r": r}
    return r


def actividad(nombre, inp):
    cmd = (inp.get("command") or "").lower()
    archivo = os.path.basename(inp.get("file_path") or "")
    pares = [(" voz", "🎙️ Grabando voces"), ("musica", "🎵 Buscando música"), ("biblioteca", "🎵 Buscando música"),
             ("lyria", "🎵 Componiendo música"), (" sfx", "🔊 Poniendo efectos de sonido"), (" fx", "🔊 Poniendo efectos"),
             (" mezcla", "🎚️ Mezclando el sonido"), (" video", "🎬 Animando cuadro por cuadro"), (" final", "✨ Uniendo todo"),
             ("verificar", "🔍 Revisando que todo esté bien"), (" escena", "🖼️ Probando una escena"), ("yt-dlp", "📥 Bajando clips"),
             (" bajar", "📥 Bajando clips"), ("nuevo ", "📁 Preparando tu proyecto"), ("tele ", "📺 Mandándolo a la tele de papá"),
             (" tiempo", "⏱️ Sincronizando la voz"), (" chequeo", "🔍 Revisando")]
    if nombre in ("Bash", "PowerShell"):
        for clave, txt in pares:
            if clave in cmd:
                return txt
        return "⚙️ Trabajando en la compu"
    if nombre in ("Write", "Edit"):
        if "guion" in archivo:
            return "✍️ Escribiendo el guion"
        if archivo.endswith(".py"):
            return "🎨 Diseñando las escenas"
        return "📝 Tomando notas"
    if nombre in ("Read", "Grep", "Glob"):
        return "📚 Leyendo cómo se hace"
    if nombre in ("WebSearch", "WebFetch"):
        return "🔎 Investigando el tema"
    return "⚙️ Trabajando"


def avances(t):
    out = []
    try:
        with open(ruta("trabajos", t["id"] + ".avances.jsonl"), encoding="utf-8") as f:
            for ln in f:
                try:
                    out.append(json.loads(ln))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


_AV_T = {"t": 0.0}


def avances_al_chat(forzar=False):
    """Cada avance nuevo de un trabajo (avance.py) se vuelve un mensaje de Claude en el chat de Amaya, con su imagen
    (cuadro, hoja de escenas o pegatinas) y/o su nota de voz. Recuerda cuántos vio de cada trabajo en chat.json."""
    if not forzar and time.time() - _AV_T["t"] < 2.5:
        return
    _AV_T["t"] = time.time()
    with _cand:
        c = chat()
        vistos = c.setdefault("avances_vistos", {})
        cambio = False
        for t in trabajos()[:8]:
            av = avances(t)
            if t["id"] not in vistos and t.get("creado", 0) < time.time() - 6 * 3600:
                vistos[t["id"]] = len(av)                # trabajos viejos: no inundar el chat
                cambio = True
                continue
            n0 = vistos.get(t["id"], 0)
            if len(av) <= n0:
                continue
            titulo = (t.get("ficha") or {}).get("titulo") or t["alias"]
            for a in av[n0:]:
                if not (a.get("txt") or a.get("img") or a.get("audio")):
                    continue
                adj = []
                if a.get("img"):
                    adj.append({"id": a["img"].rsplit(".", 1)[0], "tipo": "foto", "url": "media/" + a["img"],
                                "mini": "media/" + (a.get("mini") or a["img"]), "hoja": (a.get("n_img") or 1) > 1})
                if a.get("audio"):
                    adj.append({"id": a["audio"].rsplit(".", 1)[0], "tipo": "audio", "url": "media/" + a["audio"], "voz": True})
                n = (c["mensajes"][-1]["n"] + 1) if c["mensajes"] else 1
                c["mensajes"].append(dict(n=n, de="claude", texto=a.get("txt") or "", adjuntos=adj, t=a.get("t") or time.time(),
                                          avance=True, trabajo=t["id"], titulo=titulo))
            vistos[t["id"]] = len(av)
            cambio = True
        if cambio:
            guardar_chat(c)


def master_de(alias):
    d = os.path.join(VIDEOS, alias, "salida")
    if not os.path.isdir(d):
        return None
    ms = [os.path.join(d, n) for n in os.listdir(d) if n.endswith("_MASTER.mp4")]
    return max(ms, key=os.path.getmtime) if ms else None


def estado_trabajo(t):
    """en_cola | trabajando | listo | falta_papa | detenido | error, con lo que la app enseña."""
    lg = leer_log(t)
    av = avances(t)
    m = master_de(t["alias"])
    if t.get("estado") == "en_cola":
        e = "en_cola"
    elif lg.get("resultado") is not None:
        hecho = m and os.path.getmtime(m) >= t.get("inicio", 0) - 60
        e = "listo" if hecho else ("error" if lg.get("error") else "falta_papa")
    elif pid_vivo(t.get("pid")):
        e = "trabajando"
    else:
        e = "detenido" if t.get("pid") else "en_cola"
    pasos = [a for a in av if a.get("txt")]
    return dict(t, estado=e, pasos=pasos, actividad=lg.get("actividad", ""), mensaje=(lg.get("resultado") or "") if e != "trabajando" else "",
                sid=lg.get("sid") or t.get("sid"), master=bool(m), minutos=round(((lg.get("t") or time.time()) - t.get("inicio", time.time())) / 60) if t.get("inicio") else 0)


def trabajo_activo():
    for t in trabajos():
        e = estado_trabajo(t)
        if e["estado"] in ("trabajando", "en_cola"):
            return e
    return None


def prompt_produccion(t):
    f = t["ficha"]
    e = estilo(f.get("estilo")) or {}
    k = config()["canal"]
    v = {"nombre": k["voz_nombre"], "id": k["voz"]} if f.get("voz") == k["voz"] else (voz(f.get("voz")) or {"nombre": f.get("voz"), "id": f.get("voz")})
    fotos = [adjunto_path(x) for x in f.get("fotos", []) if adjunto_path(x)]
    base = estilo(e.get("base")) if e.get("id", "").startswith("mio_") else None
    lineas = [f"Trabajo `{t['id']}` del Estudio de Amaya (lee primero la sección «ESTUDIO AMAYA» de tus instrucciones).", ""]
    if t.get("cambios_de"):
        lineas += [f"Son CAMBIOS a su video ya hecho `videos/{t['alias']}/`: lee su ESTADO.md, haz SOLO los cambios que pide y "
                   "vuelve a sacar el MASTER (rehaz solo lo necesario).", ""]
    else:
        lineas += [f"Video NUEVO, alias `{t['alias']}` (créalo con `python fab.py nuevo {t['alias']}` y las opciones que pida el "
                   "estilo; no hace falta preguntar nada). En su ESTADO.md: «canal: " + k["nombre"] + " (`" + k["alias"] + "`) — video de Amaya "
                   "desde su app; lo sube PAPÁ desde su PC, tú NO lo subes».", ""]
    lineas += ["Lo que pidió Amaya (su ficha):", "```json", json.dumps(f, ensure_ascii=False, indent=1), "```", ""]
    if e:
        lineas.append(f"Estilo: {e.get('nombre')} — {e.get('desc', '')}")
        if e.get("doc"):
            lineas.append(f"  Doc del estilo: {e['doc']} · ejemplo a copiar: {e.get('ejemplo', '-')} · "
                          + ("se hace por código" if e.get("auto", True) else "necesita imágenes de Flow (regla 5)"))
        if e["id"].startswith("mio_"):
            lineas.append(f"  Es un ESTILO PROPIO de Amaya. Colores: {', '.join(e.get('colores', [])) or '-'}. "
                          f"Basado en: {(base or {}).get('nombre', 'libre')}"
                          + (f" (doc {base.get('doc')}, ejemplo {base.get('ejemplo')})" if base else "")
                          + (f". Foto de referencia: {adjunto_path(e['foto'])}" if e.get("foto") and adjunto_path(e["foto"]) else ""))
    lineas.append(f"Voz: ElevenLabs «{v.get('nombre')}» voice_id `{v.get('id')}` (modelo eleven_v4_turbo, corchetes de actuación "
                  "permitidos salvo susurros y excitado).")
    fmt = f.get("formato", "vertical")
    lineas.append(f"Duración: {f.get('duracion', '1 min')} · formato: {fmt}" + (" (FORMATO = \"vertical\", 1080x1920)" if fmt == "vertical" else " (1920x1080)"))
    if fotos:
        lineas.append("Fotos que mandó Amaya para el video (úsalas como pegatinas o planos): " + ", ".join(fotos))
    lineas += ["", f"Avances para ella (le llegan a su chat): `python nucleo/amaya/avance.py {t['id']} \"<emoji> <frase>\"` en cada "
               "etapa, con `--imagen` cuando haya algo que ver (escenas, pegatinas, montaje, cuadro final) y `--voz \"<frase corta>\"` "
               f"2-3 veces (regla 7); `python nucleo/amaya/avance.py {t['id']} --listo` al terminar."]
    return "\n".join(lineas)


def lanzar_trabajo(t):
    cfg = config()
    log_p = ruta("trabajos", t["id"] + ".log")
    pr_p = ruta("trabajos", t["id"] + ".prompt.txt")
    with open(pr_p, "w", encoding="utf-8") as f:
        f.write(prompt_produccion(t))
    cmd = [claude_exe(), "-p", "--output-format", "stream-json", "--verbose", "--permission-mode", "bypassPermissions",
           "--append-system-prompt-file", os.path.join(AQUI, "produccion.md"), "--disallowedTools", *DENEGADOS]
    if cfg.get("modelo_produccion"):
        cmd += ["--model", cfg["modelo_produccion"]]
    if t.get("resume_sid"):
        cmd += ["--resume", t["resume_sid"]]
    env = dict(os.environ, FAB_CORTE_CONTEXTO="0", FAB_AMAYA_TRABAJO=t["id"], PYTHONIOENCODING="utf-8")
    with open(pr_p, "rb") as entrada, open(log_p, "ab") as salida:
        try:
            p = subprocess.Popen(cmd, stdin=entrada, stdout=salida, stderr=subprocess.STDOUT, cwd=RAIZ, env=env,
                                 creationflags=DESACOPLADO | 0x01000000, close_fds=True)
        except OSError:
            p = subprocess.Popen(cmd, stdin=entrada, stdout=salida, stderr=subprocess.STDOUT, cwd=RAIZ, env=env,
                                 creationflags=DESACOPLADO, close_fds=True)
    t.update(estado="lanzado", pid=p.pid, inicio=time.time())
    guardar_json(ruta("trabajos", t["id"] + ".json"), t)
    log("producción", t["id"], t["alias"], "pid", p.pid)
    if cfg.get("avisar_a_papa"):
        avisar(f"Amaya empezó un video en su estudio: {t['ficha'].get('titulo', t['alias'])}.")


def avisar(texto):
    try:
        subprocess.Popen([sys.executable, os.path.join(RAIZ, "fab.py"), "avisar", texto], cwd=RAIZ,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=DESACOPLADO)
    except OSError:
        pass


def crear_trabajo(ficha):
    if restantes()["videos"] <= 0:
        return None, "Hoy ya creaste todos los videos que se pueden 🎬 ¡Mañana hacemos más!"
    if not isinstance(ficha, dict) or not ficha.get("idea") and not ficha.get("titulo"):
        return None, "A la ficha le falta la idea."
    k = config()["canal"]
    ficha = dict(ficha, estilo=ESTILO_CANAL["id"], voz=k["voz"], canal=k["alias"])
    cambios = ficha.get("cambios_de")
    if cambios:
        if not re.match(r"^amaya_[a-z0-9_]+$", cambios) or not os.path.isdir(os.path.join(VIDEOS, cambios)):
            return None, "No encontré ese video para cambiarlo."
        alias = cambios
    else:
        base = "amaya_" + slug(ficha.get("titulo") or ficha.get("idea"))
        alias, i = base, 2
        while os.path.exists(os.path.join(VIDEOS, alias)) or any(t["alias"] == alias for t in trabajos()):
            alias, i = f"{base}_{i}", i + 1
    tid = time.strftime("t%m%d_%H%M%S")
    t = {"id": tid, "alias": alias, "ficha": ficha, "creado": time.time(), "estado": "en_cola", "cambios_de": cambios}
    if cambios:
        prev = next((estado_trabajo(x) for x in trabajos() if x["alias"] == cambios and x.get("pid")), None)
        if prev and prev.get("sid"):
            t["resume_sid"] = prev["sid"]
    guardar_json(ruta("trabajos", tid + ".json"), t)
    uso("videos")
    with _cand:
        c = chat()
        for m in reversed(c["mensajes"]):
            if m["de"] == "claude" and "[[ficha]]" in m["texto"]:
                m["creado"] = tid
                break
        guardar_chat(c)
    nuevo_mensaje("sistema", f"🎬 ¡La fábrica recibió «{ficha.get('titulo') or alias}»! Puedes ver cómo va en «Mis videos».", trabajo=tid)
    despachar()
    return t, None


def reintentar(tid):
    t = leer_json(ruta("trabajos", tid + ".json"))
    if not t:
        return "No encontré ese trabajo."
    e = estado_trabajo(t)
    if e["estado"] not in ("detenido", "error", "falta_papa"):
        return "Ese video no necesita reintento."
    t2 = dict(t, estado="en_cola", resume_sid=e.get("sid"), reintento=t.get("reintento", 0) + 1, pid=None)
    t2["ficha"] = dict(t["ficha"], extra=(t["ficha"].get("extra") or "") + " · (Se cortó antes de terminar: sigue donde se quedó.)")
    guardar_json(ruta("trabajos", tid + ".json"), t2)
    despachar()
    return None


_desp = threading.Lock()


def despachar():
    """Lanza el siguiente trabajo en cola si no hay otro trabajando (y avisa a papá cuando uno termina)."""
    with _desp:
        ts = [estado_trabajo(t) for t in trabajos()]
        for t in ts:                                     # avisos de fin (una vez)
            if t["estado"] in ("listo", "falta_papa", "error") and not t.get("avisado"):
                crudo = leer_json(ruta("trabajos", t["id"] + ".json"))
                crudo["avisado"] = time.time()
                guardar_json(ruta("trabajos", t["id"] + ".json"), crudo)
                titulo = t["ficha"].get("titulo") or t["alias"]
                nuevo_mensaje("sistema", {"listo": f"✨ ¡Tu video «{titulo}» está listo! Míralo en «Mis videos».",
                                          "falta_papa": f"🧩 «{titulo}» va avanzado, pero falta que papá ayude con una parte.",
                                          "error": f"😵 «{titulo}» tuvo un problema. Papá puede revisarlo."}[t["estado"]], trabajo=t["id"])
                if config().get("avisar_a_papa"):
                    avisar(f"El video de Amaya «{titulo}» terminó: {t['estado'].replace('_', ' ')}.")
                if t["estado"] == "listo":
                    threading.Thread(target=version_movil, args=(t["alias"],), daemon=True).start()
        if any(t["estado"] == "trabajando" for t in ts):
            return
        cola = sorted((t for t in ts if t["estado"] == "en_cola"), key=lambda t: t.get("creado", 0))
        if cola:
            crudo = leer_json(ruta("trabajos", cola[0]["id"] + ".json"))
            lanzar_trabajo(crudo)


def vigilante():
    while True:
        try:
            despachar()
            avances_al_chat(True)
        except Exception as e:
            log("vigilante", repr(e)[:200])
        time.sleep(20)


# ======================================================================== mis videos
def videos():
    ts = {}
    for t in trabajos():
        ts.setdefault(t["alias"], t)
    out = []
    if not os.path.isdir(VIDEOS):
        return out
    for n in os.listdir(VIDEOS):
        if not n.startswith("amaya_") or not os.path.isdir(os.path.join(VIDEOS, n)):
            continue
        t = ts.get(n)
        m = master_de(n)
        titulo = (t or {}).get("ficha", {}).get("titulo") if t else None
        if not titulo:
            try:
                titulo = open(os.path.join(VIDEOS, n, "ESTADO.md"), encoding="utf-8").readline().lstrip("# ").split(" — ")[0].strip()
            except OSError:
                titulo = n
        e = estado_trabajo(t)["estado"] if t else ("listo" if m else "en_proceso")
        dur = None
        if m:
            info = leer_json(ruta("portadas", n + ".json")) or {}
            dur = info.get("dur")
        out.append({"alias": n, "titulo": titulo, "estado": e, "de": "amaya" if t else "papa", "master": bool(m),
                    "dur": dur, "t": os.path.getmtime(m) if m else os.path.getmtime(os.path.join(VIDEOS, n)),
                    "portada": f"v/{n}/portada.jpg", "trabajo": (t or {}).get("id"),
                    "vertical": (t or {}).get("ficha", {}).get("formato") == "vertical"})
    return sorted(out, key=lambda v: v["t"], reverse=True)


def portada(alias):
    out = ruta("portadas", alias + ".jpg")
    m = master_de(alias)
    if os.path.exists(out) and (not m or os.path.getmtime(out) >= os.path.getmtime(m)):
        return out
    if not m:
        return None
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:
        dur = float(subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", m],
                                   capture_output=True, text=True, timeout=30, creationflags=SIN_VENTANA).stdout.strip() or 0)
    except Exception:
        dur = 0
    subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{max(1, dur * 0.3):.1f}", "-i", m, "-frames:v", "1",
                    "-vf", "scale=640:640:force_original_aspect_ratio=decrease", "-q:v", "4", out],
                   capture_output=True, timeout=60, creationflags=SIN_VENTANA)
    guardar_json(ruta("portadas", alias + ".json"), {"dur": round(dur)})
    return out if os.path.exists(out) else None


_movil = threading.Lock()


def version_movil(alias):
    """Copia ligera (720p) para ver y guardar en el teléfono sin gastar tanto túnel."""
    m = master_de(alias)
    if not m:
        return None
    out = ruta("movil", alias + ".mp4")
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(m):
        return out
    with _movil:
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(m):
            return out
        os.makedirs(os.path.dirname(out), exist_ok=True)
        tmp = out + ".tmp.mp4"
        r = subprocess.run([FFMPEG, "-y", "-v", "error", "-i", m, "-vf", "scale='if(gt(iw,ih),-2,720)':'if(gt(iw,ih),720,-2)'",
                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-c:a", "aac", "-b:a", "128k",
                            "-movflags", "+faststart", "-threads", "2", tmp], capture_output=True, timeout=3600, creationflags=SIN_VENTANA)
        if r.returncode == 0:
            os.replace(tmp, out)
            return out
        log("versión móvil falló", alias, r.stderr[-300:])
        return None


# ======================================================================== imágenes de estilos
def tarjeta_sin_foto(e, out):
    from PIL import Image, ImageDraw, ImageFont
    cs = [c for c in (e.get("colores") or []) if re.match(r"^#[0-9a-fA-F]{6}$", c or "")] or ["#a98bff", "#ff6fb5", "#ffb38a"]
    cs = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in cs]
    if len(cs) == 1:
        cs = cs * 2
    w, h = 640, 400
    im = Image.new("RGB", (w, h))
    px = im.load()
    for x in range(w):
        t = x / (w - 1) * (len(cs) - 1)
        i = min(int(t), len(cs) - 2)
        u = t - i
        col = tuple(int(cs[i][k] + (cs[i + 1][k] - cs[i][k]) * u) for k in range(3))
        for y in range(h):
            px[x, y] = col
    g = ImageDraw.Draw(im)
    for j in range(18):                       # estrellitas suaves
        x, y = (j * 137) % w, (j * 89 + 40) % h
        g.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(255, 255, 255))
    try:
        f = ImageFont.truetype(r"C:\Windows\Fonts\seguiemj.ttf", 150)
        g.text((w / 2, h / 2), e.get("emoji") or "⭐", font=f, anchor="mm", embedded_color=True)
    except (OSError, ValueError):
        pass
    im.save(out, quality=86)
    return out


def img_estilo(eid):
    out = ruta("estilos_img", eid + ".jpg")
    if os.path.exists(out):
        return out
    e = estilo(eid)
    if not e:
        return None
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if eid.startswith("mio_"):
        p = adjunto_path(e.get("foto") or "")
        if p:
            from PIL import Image, ImageOps
            ImageOps.fit(Image.open(p).convert("RGB"), (640, 400)).save(out, quality=84)
            return out
        return tarjeta_sin_foto(e, out)          # sin foto: degradado con SUS colores y su emoji (nunca imagen rota)
    src = e.get("img") or ""
    seg = None
    if "@" in src:
        src, seg = src.rsplit("@", 1)
    p = os.path.join(RAIZ, src)
    if not os.path.exists(p):
        return None
    if seg is not None:
        subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", seg, "-i", p, "-frames:v", "1", "-vf",
                        "scale=640:400:force_original_aspect_ratio=increase,crop=640:400", "-q:v", "4", out],
                       capture_output=True, timeout=60, creationflags=SIN_VENTANA)
    else:
        from PIL import Image, ImageOps
        ImageOps.fit(Image.open(p).convert("RGB"), (640, 400)).save(out, quality=84)
    return out if os.path.exists(out) else None


def guardar_estilo_mio(d):
    nombre = (d.get("nombre") or "").strip()[:40]
    if not nombre:
        return None, "Ponle nombre a tu estilo."
    eid = d.get("id") if str(d.get("id", "")).startswith("mio_") else "mio_" + slug(nombre, 20)
    e = {"id": eid, "nombre": nombre, "emoji": (d.get("emoji") or "⭐")[:4], "desc": (d.get("desc") or "").strip()[:500],
         "ideal": (d.get("ideal") or "").strip()[:120], "colores": [c for c in d.get("colores", []) if re.match(r"^#[0-9a-fA-F]{6}$", c)][:5],
         "color": (d.get("colores") or ["#ff7eb6"])[0], "base": d.get("base") if estilo(d.get("base") or "") else None,
         "foto": d.get("foto") if adjunto_path(d.get("foto") or "") else None, "auto": True, "creado": time.time(),
         "pide": f"«Hazme un video de … en mi estilo {nombre}»"}
    if e["base"]:
        e["auto"] = (estilo(e["base"]) or {}).get("auto", True)
    guardar_json(ruta("estilos", eid + ".json"), e)
    try:
        os.remove(ruta("estilos_img", eid + ".jpg"))
    except OSError:
        pass
    return e, None


# ======================================================================== HTTP
TIPOS = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".json": "application/json", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".mp3": "audio/mpeg",
         ".mp4": "video/mp4", ".webm": "audio/webm", ".ogg": "audio/ogg", ".m4a": "audio/mp4", ".webmanifest": "application/manifest+json"}
PING_PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")


class Manejador(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, datos, codigo=200):
        b = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self._enviar(codigo, b, "application/json; charset=utf-8")

    def _enviar(self, codigo, cuerpo, tipo, cache="no-store"):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", cache)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(cuerpo)

    def _archivo(self, p, cache="max-age=3600"):
        if not p or not os.path.isfile(p):
            return self._enviar(404, b"no encontrado", "text/plain")
        tam = os.path.getsize(p)
        tipo = TIPOS.get(os.path.splitext(p)[1].lower(), "application/octet-stream")
        rng = self.headers.get("Range")
        ini, fin = 0, tam - 1
        m = re.match(r"bytes=(\d*)-(\d*)", rng or "")
        if m and (m.group(1) or m.group(2)):
            if m.group(1):
                ini = int(m.group(1))
                fin = int(m.group(2)) if m.group(2) else tam - 1
            else:
                ini = max(0, tam - int(m.group(2)))
            fin = min(fin, tam - 1)
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {ini}-{fin}/{tam}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(fin - ini + 1))
        self.send_header("Cache-Control", cache)
        q = parse_qs(urlparse(self.path).query)
        if q.get("bajar"):
            self.send_header("Content-Disposition", f'attachment; filename="{q["bajar"][0]}"')
        self.end_headers()
        if self.command == "HEAD":
            return
        with open(p, "rb") as f:
            f.seek(ini)
            falta = fin - ini + 1
            while falta > 0:
                trozo = f.read(min(256 * 1024, falta))
                if not trozo:
                    break
                self.wfile.write(trozo)
                falta -= len(trozo)

    def _cuerpo(self, maximo=30_000_000):
        n = int(self.headers.get("Content-Length") or 0)
        if n > maximo:
            raise ValueError("demasiado grande")
        return self.rfile.read(n) if n else b""

    def do_GET(self):
        self._seguro(self._get)

    def do_HEAD(self):
        self._seguro(self._get)

    def do_POST(self):
        self._seguro(self._post)

    def _seguro(self, f):
        try:
            f()
        except (ConnectionError, TimeoutError):
            pass
        except Exception as e:
            log("error", self.command, self.path, repr(e)[:300])
            try:
                self._json({"error": "algo falló en la fábrica"}, 500)
            except OSError:
                pass

    def _get(self):
        u = urlparse(self.path)
        r = unquote(u.path)
        q = parse_qs(u.query)
        if r in ("/", "/index.html"):
            return self._archivo(os.path.join(AQUI, "app.html"), cache="no-store")
        if r == "/ping.png":
            return self._enviar(200, PING_PNG, "image/png")
        if r in ("/manifest.webmanifest", "/icono-192.png", "/icono-512.png", "/sw.js"):
            return self._archivo(os.path.join(AQUI, "web", r.lstrip("/")), cache="max-age=600")
        if r == "/api/inicio":
            avances_al_chat(True)
            c = config()
            ch = chat()
            return self._json({"nombre": c["nombre"], "firma": c["firma"], "carta": c["carta"], "restantes": restantes(),
                               "limites": c["limites"], "estilos": [dict(ESTILO_CANAL, img_url="")], "canal": c["canal"], "mensajes": ch["mensajes"][-80:],
                               "vivo": CHAT_VIVO, "trabajo": trabajo_activo(), "videos": videos()})
        if r == "/api/chat":
            avances_al_chat()
            desde = int((q.get("desde") or ["0"])[0] or 0)
            ch = chat()
            return self._json({"mensajes": [m for m in ch["mensajes"] if m["n"] > desde], "vivo": CHAT_VIVO,
                               "restantes": restantes(), "trabajo": trabajo_activo()})
        if r == "/api/voces":
            try:
                vs = voces()
            except Exception as e:
                log("voces", repr(e)[:200])
                vs = []
            favs = set((leer_json(ruta("favoritas.json"), {}) or {}).get("voz", []))
            return self._json({"voces": [dict(v, favorita=v["id"] in favs) for v in vs], "restantes": restantes()})
        if r == "/api/estilos":
            return self._json({"estilos": estilos_todos()})
        if r == "/api/videos":
            return self._json({"videos": videos(), "trabajos": [estado_trabajo(t) for t in trabajos()[:12]]})
        m = re.match(r"^/img/estilo/([a-z0-9_]+)\.jpg$", r)
        if m:
            return self._archivo(img_estilo(m.group(1)), cache="max-age=300")
        m = re.match(r"^/subidos/([fa][0-9a-f]{10,16}(?:_mini)?\.(?:jpg|webm|ogg|m4a))$", r)
        if m:
            return self._archivo(ruta("subidos", m.group(1)), cache="max-age=86400")
        m = re.match(r"^/media/([A-Za-z0-9_-]{4,60}\.(?:jpg|mp3))$", r)
        if m:
            return self._archivo(ruta("trabajos", "media", m.group(1)), cache="max-age=86400")
        m = re.match(r"^/prueba_voz/([0-9a-f]{16})\.mp3$", r)
        if m:
            return self._archivo(ruta("pruebas_voz", m.group(1) + ".mp3"), cache="max-age=86400")
        m = re.match(r"^/v/(amaya_[a-z0-9_]+)/(portada\.jpg|video\.mp4|master\.mp4)$", r)
        if m:
            alias, que = m.groups()
            if que == "portada.jpg":
                return self._archivo(portada(alias), cache="max-age=120")
            if que == "master.mp4":
                return self._archivo(master_de(alias), cache="no-store")
            p = ruta("movil", alias + ".mp4")
            mm = master_de(alias)
            if mm and os.path.exists(p) and os.path.getmtime(p) >= os.path.getmtime(mm):
                return self._archivo(p, cache="no-store")
            if mm:
                threading.Thread(target=version_movil, args=(alias,), daemon=True).start()
            return self._archivo(mm, cache="no-store")
        return self._enviar(404, b"no encontrado", "text/plain")

    def _post(self):
        r = urlparse(self.path).path
        q = parse_qs(urlparse(self.path).query)
        if r == "/api/subir":
            tipo = (q.get("tipo") or ["foto"])[0]
            datos = self._cuerpo()
            a, err = guardar_subida(datos, "audio" if tipo == "audio" else "foto", unquote((q.get("nombre") or [""])[0]))
            return self._json({"error": err} if err else a, 400 if err else 200)
        d = json.loads(self._cuerpo(2_000_000) or b"{}")
        if r == "/api/chat":
            if CHAT_VIVO["pensando"]:
                return self._json({"error": "Claude todavía está contestando el mensaje anterior ✋"}, 409)
            if restantes()["mensajes"] <= 0:
                return self._json({"error": "Por hoy ya platicamos muchísimo 😅 ¡Mañana seguimos!"}, 429)
            texto = (d.get("texto") or "").strip()[:4000]
            adj = [a for a in d.get("adjuntos", []) if isinstance(a, dict) and adjunto_path(a.get("id"))][:6]
            if not texto and not adj:
                return self._json({"error": "mensaje vacío"}, 400)
            m = nuevo_mensaje("amaya", texto, adj)
            uso("mensajes")
            CHAT_VIVO.update(pensando=True, parcial="", desde=time.time())
            threading.Thread(target=correr_guia, args=(m,), daemon=True).start()
            return self._json({"ok": True, "mensaje": m})
        if r in ("/api/chat/nuevo", "/api/reiniciar"):
            # chat limpio y sesión nueva de la guía; el viejo se archiva. Se conservan los avances ya vistos (si no,
            # los de trabajos recientes volverían a llenar el chat) y NO se tocan videos, trabajos ni fotos.
            with _cand:
                c = chat()
                if c["mensajes"]:
                    guardar_json(ruta("chats_viejos", time.strftime("%Y%m%d_%H%M%S") + ".json"), c)
                guardar_chat({"sid": None, "turnos": 0, "mensajes": [], "avances_vistos": c.get("avances_vistos", {})})
                CHAT_VIVO.update(pensando=False, parcial="", error="")
            return self._json({"ok": True})
        if r == "/api/crear":
            t, err = crear_trabajo(d.get("ficha"))
            return self._json({"error": err} if err else {"ok": True, "trabajo": t}, 400 if err else 200)
        if r == "/api/reintentar":
            err = reintentar(d.get("id", ""))
            return self._json({"error": err} if err else {"ok": True}, 400 if err else 200)
        if r == "/api/voces/probar":
            h, err = probar_voz(d.get("id", ""), d.get("texto", ""))
            return self._json({"error": err} if err else {"url": f"prueba_voz/{h}.mp3", "restantes": restantes()}, 400 if err else 200)
        if r == "/api/favorita":
            tipo = "voz" if d.get("tipo") == "voz" else "estilo"
            with _cand:
                f = leer_json(ruta("favoritas.json"), {}) or {}
                xs = f.setdefault(tipo, [])
                if d.get("id") in xs:
                    xs.remove(d["id"])
                elif d.get("id"):
                    xs.append(d["id"])
                guardar_json(ruta("favoritas.json"), f)
            return self._json({"ok": True, "favoritas": f})
        if r in ("/api/estilos", "/api/estilos/borrar"):
            return self._json({"error": "Tu canal ya tiene su estilo 🎀"}, 400)
        if r == "/api/estilos":
            e, err = guardar_estilo_mio(d)
            return self._json({"error": err} if err else {"ok": True, "estilo": e}, 400 if err else 200)
        if r == "/api/estilos/borrar":
            eid = d.get("id", "")
            if eid.startswith("mio_") and re.match(r"^mio_[a-z0-9_]+$", eid):
                for p in (ruta("estilos", eid + ".json"), ruta("estilos_img", eid + ".jpg")):
                    try:
                        os.remove(p)
                    except OSError:
                        pass
            return self._json({"ok": True})
        return self._json({"error": "no existe"}, 404)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--puerto", type=int, default=PUERTO)
    a = ap.parse_args()
    os.makedirs(DATOS, exist_ok=True)
    config()
    threading.Thread(target=vigilante, daemon=True).start()
    threading.Thread(target=lambda: (time.sleep(3), voces()), daemon=True).start()   # calienta la caché de voces
    ThreadingHTTPServer.daemon_threads = True
    srv = ThreadingHTTPServer(("127.0.0.1", a.puerto), Manejador)
    log(f"Estudio Amaya en 127.0.0.1:{a.puerto}")
    print(f"Estudio Amaya en http://127.0.0.1:{a.puerto}/", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
