"""Lo que el agente hace, en vivo (el usuario, 30-oct-2026): lee los transcritos de Claude Code y los vuelve eventos.

Claude Code escribe cada sesión en ~/.claude/projects/C--FabricaAnimaciones/<id>.jsonl según ocurre: cada imagen que mira,
cada archivo que escribe, cada comando. Aquí se leen solo los bytes nuevos (no gasta tokens ni toca al agente) y salen
eventos que la página /v2/vivo anima. Se ve lo que el agente HACE; su razonamiento, no.

  sesiones()              sesiones de las últimas horas: título, video detectado, si está activa
  eventos(sesion, desde)  los eventos con seq > desde, más el plan y la estación actuales
  imagen(sesion, nombre)  ruta de la imagen guardada (reducida) de un evento

El panel remoto sale a internet: TODO texto pasa por tapar() y los archivos sensibles salen sin contenido.
Prueba: python nucleo/agente_vivo.py [sesion]
"""
import base64
import collections
import difflib
import glob
import hashlib
import io
import json
import os
import re
import shutil
import struct
import tempfile
import threading
import time
from datetime import datetime
from urllib.parse import unquote

CARPETA = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--FabricaAnimaciones")
VIDEOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos")
CACHE = os.path.join(tempfile.gettempdir(), "fab_vivo")
HORAS = 12                             # sesiones que se listan
ACTIVA_S = 120                         # sin escribir en este tiempo, la sesión ya no cuenta como «en vivo»
COLA_BYTES = 40_000_000                # al abrir una sesión se lee solo su final (con imágenes pesan decenas de MB)
MAX_EVENTOS = 500
PRIMERA = 160                          # eventos del principal que se mandan al abrir la página (la ventana de la repetición)
MAX_EV_AYUD = 200                      # cada ayudante guarda los suyos aparte: uno que hace cientos no echa al principal
PRIMERA_AYUD = 60                      # y de cada uno se mandan estos al abrir
MAX_IMAGENES = 200                     # imágenes por sesión en la caché (reducidas a ANCHO_IMG, ~50 KB cada una)
ANCHO_IMG = 960
MAX_LINEAS = 70                        # código o comando por evento
MAX_COL = 170
HORAS_AYUD = 6                         # ayudantes que se leen: su archivo se escribió en estas horas
MAX_AYUD = 12                          # y como mucho estos (los más recientes): hay transcritos de 300 MB
COLA_AYUD = 8_000_000                  # de cada ayudante se lee solo su final
LINEA_AYUD = 2_000_000                 # sus líneas más largas son imágenes: no se usan
AYUD_CADA = 2                          # segundos entre revisiones de la carpeta de ayudantes
FONDO_MAX_S = 3 * 3600                 # un comando en segundo plano sin aviso de fin se da por muerto
MAX_ULTIMOS_S = 600                    # ayudantes ya terminados que aún se mandan a la página

EXT_IMG = (".jpg", ".jpeg", ".png", ".webp", ".gif")

# ---------------------------------------------------------------- filtro de secretos
SENSIBLE = re.compile(r"canales[\\/]+tokens|client_secret|(^|[\\/])\.env\b|panel_remoto\.json|credentials|\.pem\b|"
                      r"\.pfx\b|cookies?\.(txt|json)|llaves?\.json|claves?\.json", re.I)
_SECRETOS = [
    (re.compile(r"\bsk[-_][A-Za-z0-9_-]{16,}"), "••••"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{30,}"), "••••"),
    (re.compile(r"\bya29\.[\w.-]+"), "••••"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "••••"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"), "••••"),
    (re.compile(r"\bxox[abprs]-[\w-]+"), "••••"),
    (re.compile(r"\bEAA[A-Za-z0-9]{30,}"), "••••"),
    (re.compile(r"\beyJ[\w-]{16,}\.[\w-]+\.[\w-]+"), "••••"),
    (re.compile(r"([?&](?:k|key|token|sig|signature|auth|access_token|expires|x-goog-[\w-]+)=)[^&\s\"'<>]+", re.I), r"\1••••"),
    (re.compile(r"(?i)\b([\w-]*(?:api[_-]?key|token|secret|password|passwd|contrase[nñ]a|clave|authorization)[\w-]*)"
                r"([\"'\s]*[:=][\"'\s]*)(?:bearer\s+)?([^\s\"',;)}\]]{6,})"), r"\1\2••••"),
    (re.compile(r"(?i)\bbearer\s+[\w.~+/-]{8,}=*"), "Bearer ••••"),
    (re.compile(r"\b[A-Fa-f0-9]{40,}\b"), "••••"),
    (re.compile(r"\b[A-Za-z0-9+_-]{48,}={0,2}"), "••••"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "••••@••••"),
]


def tapar(texto):
    """El texto sin claves, tokens ni correos: lo que pasa por aquí puede verse desde el celular."""
    if not texto:
        return ""
    for rx, por in _SECRETOS:
        texto = rx.sub(por, texto)
    return texto


def sensible(*textos):
    return any(t and SENSIBLE.search(t) for t in textos)


def _recortar(texto, lineas=MAX_LINEAS, col=MAX_COL):
    filas = (texto or "").replace("\r\n", "\n").split("\n")
    sobran = max(0, len(filas) - lineas)
    filas = [f[:col] + ("…" if len(f) > col else "") for f in filas[:lineas]]
    return "\n".join(filas), sobran


_MD_VALLA = re.compile(r"(?m)^[ \t]*```[\w-]*[ \t]*$\n?")
_MD_ENLACE = re.compile(r"!?\[([^\]\n]{0,300})\]\([^)\n]{0,600}\)")
_MD_NEGRITA = re.compile(r"(?<![\w*])(\*\*|__)(?=\S)([^\n]{1,300}?)(?<=\S)\1(?![\w*])")
_MD_CURSIVA = re.compile(r"(?<![\w*])\*(?=[^\s*])([^*\n]{1,300}?)(?<=[^\s*])\*(?![\w*])")
_MD_CODIGO = re.compile(r"`+([^`\n]{0,300})`+")
_MD_TITULO = re.compile(r"(?m)^[ \t]{0,3}#{1,6}[ \t]+")


def sin_markdown(texto):
    """Lo que dice el agente, sin marcas: enlaces `[texto](#local_…)` → texto; `**`, `*`, backticks, vallas y títulos fuera."""
    t = _MD_VALLA.sub("", texto or "")
    t = _MD_ENLACE.sub(r"\1", t)
    t = _MD_NEGRITA.sub(r"\2", t)
    t = _MD_CURSIVA.sub(r"\1", t)
    t = _MD_CODIGO.sub(r"\1", t)
    return _MD_TITULO.sub("", t)


def _corto(texto, n=240):
    t = " ".join((texto or "").split())
    return t[:n] + ("…" if len(t) > n else "")


# ---------------------------------------------------------------- de herramienta a evento
ESTACIONES = ["guion", "voz", "sonido", "imagenes", "clips", "animacion", "render", "revision", "subida"]
_FAB = re.compile(r"""fab\.py["']?\s+([a-z0-9_]+)\s+([a-z_]+)""")
_VIDEO = re.compile(r"videos[\\/]+([a-z0-9][a-z0-9_]*)[\\/]+")
_FAB_ESTACION = {"voz": "voz", "seleccionar": "voz", "tiempo": "voz", "musica": "sonido", "sfx": "sonido", "mezcla": "sonido",
                 "ambiente": "sonido", "reajustar": "sonido", "video": "render", "final": "render", "todo": "render", "verificar": "revision",
                 "escena": "animacion", "comprobar": "animacion", "fx": "animacion", "montaje": "animacion", "prueba": "animacion",
                 "beats": "guion", "prompts": "imagenes", "servir": "imagenes", "ingesta": "imagenes", "medios": "imagenes",
                 "busquedas": "imagenes", "fuentes": "imagenes", "bajar": "clips", "miniatura": "imagenes"}


# De quién es una sesión: solo cuenta lo que PRODUCE el video. Leer, buscar, mencionarlo o `fab.py <v> estado` no
_FAB_PRODUCE = set(_FAB_ESTACION) - {"verificar", "comprobar"}
_FAB_NUEVO = re.compile(r"""fab\.py["']?\s+(?:nuevo|yt\s+subir)\s+([a-z0-9_]+)""")


def _es_video(v):
    return bool(v) and not v.startswith("_") and os.path.isdir(os.path.join(VIDEOS, v))


# Solo cuenta lo que el comando EJECUTA: en un `grep`, un commit o un heredoc las palabras «lyria» o «render» no son trabajo en esa estación
_CORRE = re.compile(r"(?:^|[\s;&|(])(?:python3?|py)(?:\.exe)?\s+([^\n;|&]+)")
_HEREDOC = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?.*?^\s*\1\s*$", re.S | re.M)
_PY_C = re.compile(r"""-c\s+(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')""", re.S)
_TRAMOS = re.compile(r"[;|\n]|&&")
_SONIDO = re.compile(r"(?<![a-z])(ost|sfx|lyria|demucs|musica|mezcla|sonidos?)(?![a-z])")
_CLIPS = re.compile(r"(?<![a-z])clips?(?![a-z])")
_RENDER = re.compile(r"""(^|[\s"'\\/])render\w*\.py\b|-m\s+secuencia\s+video\b""")
_YTDLP = re.compile(r"""(^|[\s;&|("'\\/])yt[-_]dlp(\.exe)?["']?\s""")
_YTDLP_MIRA = re.compile(r"--print\b|--flat-playlist|--dump-json|\s-j\b|--simulate")
_YTDLP_AUDIO = re.compile(r"\s-x\b|--extract-audio|--audio-format|(?<!\+)bestaudio")
_FFMPEG = re.compile(r"""(^|[\s"'\\/])ffmpeg(\.exe)?["']?\s""")
_DEMUCS = re.compile(r"(^|\s)demucs\s")
_BAJA = re.compile(r"\s*(baj|descarg|busc|download)")      # la `description`: «Baja la banda sonora…» (el comando no siempre lo dice)
_BAJA_CLIPS = re.compile(r"\b(clips?|gameplay)\b")
_BAJA_SONIDO = re.compile(r"\b(ost|banda sonora|sfx|efectos? de sonido|m[úu]sica|audio|pistas?|tracks?)\b")
_STUDIO_EDITA = re.compile(r"\bsub[ei]|upload|public|programa|guard|save|miniatura|thumbnail|visibilidad|monetiz|relacionado|pantalla final|tarjeta", re.I)
_EXT_AUDIO = ("wav", "mp3", "m4a", "ogg", "flac", "opus")
_EXT_IMG = ("jpg", "jpeg", "png", "webp", "gif")
# Código de animación real; el resto (descargas, pruebas, parches) es auxiliar y no tiene estación
_ANIMACION = re.compile(r"^(efectos|escenas?|esc_\w+|escena_base|mundos?(_\w+)?|t\d+\w*|coreo\w*|props?\d*|obj_\w+|trans|look|mapa|sellos|\w+_3d"
                        r"|mg(_\w+)?|kz_\w+|noir\w*|toon\w*|terror_\w+|grabado\w*|sh_\w+|crono_\w+|docu\w*|motor|pegaflow|boceto|guache"
                        r"|dibujos|fondos|plano|secuencia\w*)\.py$")


def _lo_que_corre(cmd):
    """Los `python …` que el comando ejecuta de verdad, sin heredocs ni `python -c`."""
    return " ".join(_CORRE.findall(_PY_C.sub(" ", _HEREDOC.sub(" ", (cmd or "").lower()))))


def _videos_producidos(nombre, ent):
    """Los videos que esta herramienta produce: Write/Edit dentro de videos/<v>/, o `fab.py <v> <etapa>` de producción."""
    ent = ent if isinstance(ent, dict) else {}
    if nombre in ("Write", "Edit"):
        return [v for v in _VIDEO.findall(ent.get("file_path") or "")[:1] if _es_video(v)]
    if nombre in ("Bash", "PowerShell"):
        corre = _lo_que_corre(ent.get("command"))
        return [v for v in [m.group(1) for m in _FAB.finditer(corre) if m.group(2) in _FAB_PRODUCE] + _FAB_NUEVO.findall(corre) if _es_video(v)]
    return []


def _video_del_titulo(titulo):
    """El video que nombra el título de la sesión («Continúa bt_mundos_ranking — verificar y voz»), si nombra alguno."""
    t = (titulo or "").lower()
    try:
        nombres = os.listdir(VIDEOS)
    except OSError:
        return None
    for v in sorted(nombres, key=len, reverse=True):
        if len(v) >= 4 and not v.startswith("_") and v in t and re.search(rf"(?<![a-z0-9_]){re.escape(v)}(?![a-z0-9_])", t):
            return v
    return None


def _estacion_ffmpeg(limpio):
    tramo = next(s for s in _TRAMOS.split(limpio) if _FFMPEG.search(s))
    ext = (re.findall(r"\.([a-z0-9]{2,4})\b", tramo) or [""])[-1]    # la salida va al final
    return "sonido" if ext in _EXT_AUDIO else None if ext in _EXT_IMG else "render"


def _estacion_cmd(cmd, desc=""):
    limpio = _PY_C.sub(" ", _HEREDOC.sub(" ", cmd.lower()))
    corre = _lo_que_corre(cmd)
    m = _FAB.search(corre)
    if m and m.group(2) in _FAB_ESTACION:
        return _FAB_ESTACION[m.group(2)]
    if "fab.py" in corre:                                  # avisar, estado, yt comentarios…: no son ninguna estación
        return "subida" if re.search(r"fab\.py\s+yt\s+(subir|aplicar|publicar)", corre) else "sonido" if "fab.py biblioteca" in corre else None
    if re.search(r"pagina\.py\b.*\bprogramar\b", corre):   # el resto de pagina.py (calendario, aprobar…) no publica nada
        return "subida"
    if "pagina.py" in corre:
        return None
    d = (desc or "").lower()
    if _BAJA.match(d) and _BAJA_CLIPS.search(d):
        return "clips"
    if _BAJA.match(d) and _BAJA_SONIDO.search(d):
        return "sonido"
    if _YTDLP.search(limpio):
        return None if _YTDLP_MIRA.search(limpio) else "sonido" if _YTDLP_AUDIO.search(limpio) else "clips"
    if _FFMPEG.search(limpio):
        return _estacion_ffmpeg(limpio)
    if _SONIDO.search(corre) or _DEMUCS.search(limpio):
        return "sonido"
    if _CLIPS.search(corre):
        return "clips"
    return "render" if _RENDER.search(corre) else None


def _estacion_archivo(ruta):
    r = (ruta or "").replace("\\", "/").lower()
    base = r.rsplit("/", 1)[-1]
    if base == "guion.py" or base.endswith(".srt"):
        return "guion"
    if "/audio/" in r or base.endswith((".wav", ".mp3")):
        return "sonido"
    if "/flow/" in r or "/piezas/" in r or "prompts" in base:
        return "imagenes"
    if _ANIMACION.match(base) and ("/videos/" in r or "/nucleo/" in r):
        return "animacion"
    return None


def _diff(viejo, nuevo):
    """Líneas [[signo, texto]] del cambio, sin las cabeceras del diff."""
    salida = []
    for ln in difflib.unified_diff((viejo or "").split("\n"), (nuevo or "").split("\n"), lineterm="", n=2):
        if ln.startswith(("---", "+++", "@@")):
            continue
        salida.append([ln[0], tapar(ln[1:])[:MAX_COL]])
    return salida[:MAX_LINEAS], max(0, len(salida) - MAX_LINEAS)


_NAV = {"navigate": "Abre", "computer": "Usa", "find": "Busca en", "read_page": "Lee", "get_page_text": "Lee",
        "form_input": "Llena", "browser_batch": "Varios pasos en", "javascript_tool": "Revisa", "preview_start": "Abre"}


def _evento_herramienta(nombre, ent):
    """El evento de una llamada a herramienta (None si no se muestra). El resultado se le pega después."""
    ent = ent if isinstance(ent, dict) else {}
    if nombre in ("Read",):
        ruta = ent.get("file_path") or ""
        base = os.path.basename(ruta)
        if sensible(ruta):
            return dict(tipo="privado", titulo="Archivo privado", detalle="contenido oculto")
        if base.lower().endswith(EXT_IMG):
            return dict(tipo="imagen", titulo=f"Mira {base}", ruta=_ruta_corta(ruta), estacion="revision")
        return dict(tipo="leer", titulo=f"Lee {base}", ruta=_ruta_corta(ruta))
    if nombre == "Write":
        ruta = ent.get("file_path") or ""
        if sensible(ruta):
            return dict(tipo="privado", titulo="Archivo privado", detalle="contenido oculto")
        codigo, sobran = _recortar(tapar(ent.get("content") or ""))
        return dict(tipo="codigo", titulo=f"Escribe {os.path.basename(ruta)}", ruta=_ruta_corta(ruta),
                    estacion=_estacion_archivo(ruta), lineas=[["+", x] for x in codigo.split("\n")], sobran=sobran,
                    nuevas=(ent.get("content") or "").count("\n") + 1, quitadas=0)
    if nombre == "Edit":
        ruta = ent.get("file_path") or ""
        if sensible(ruta):
            return dict(tipo="privado", titulo="Archivo privado", detalle="contenido oculto")
        filas, sobran = _diff(ent.get("old_string"), ent.get("new_string"))
        return dict(tipo="codigo", titulo=f"Edita {os.path.basename(ruta)}", ruta=_ruta_corta(ruta),
                    estacion=_estacion_archivo(ruta), lineas=filas, sobran=sobran,
                    nuevas=sum(1 for s, _ in filas if s == "+"), quitadas=sum(1 for s, _ in filas if s == "-"))
    if nombre in ("Bash", "PowerShell"):
        cmd = ent.get("command") or ""
        if sensible(cmd):
            return dict(tipo="privado", titulo="Comando con datos privados", detalle=_corto(tapar(ent.get("description") or ""), 120))
        texto, sobran = _recortar(tapar(cmd), 24)
        return dict(tipo="comando", titulo=_corto(tapar(ent.get("description") or "") or tapar(cmd), 110), comando=texto,
                    sobran=sobran, estacion=_estacion_cmd(cmd, ent.get("description")))
    if nombre in ("Grep", "Glob"):
        return dict(tipo="buscar", titulo=f"Busca «{_corto(tapar(ent.get('pattern') or ''), 70)}»",
                    ruta=_ruta_corta(ent.get("path") or ""))
    if nombre == "Agent":
        return dict(tipo="ayudante", titulo=_corto(tapar(ent.get("description") or "Ayudante"), 90))
    if nombre == "Artifact":
        return dict(tipo="leer", titulo="Publica una página")
    if nombre == "WebSearch":
        q = tapar(ent.get("query") or "")
        return dict(tipo="busqueda", titulo=f"Busca en la web «{_corto(q, 80)}»", query=_corto(q, 160))
    if nombre == "WebFetch":
        url = tapar(ent.get("url") or "")
        return dict(tipo="pagina", titulo=f"Lee {_sitio(url)}", sitio=_sitio(url), url=url[:200])
    if "__Claude_Browser__" in nombre or "__claude-in-chrome__" in nombre:
        corto = nombre.rsplit("__", 1)[-1]
        if corto in ("tabs_context", "tabs_context_mcp", "read_console_messages", "read_network_requests", "resize_window")                 or ent.get("action") == "wait":
            return None
        url = ent.get("url") or ""
        if corto == "browser_batch":
            acc = [a.get("input", {}).get("action_summary") or a.get("name") for a in ent.get("actions") or [] if isinstance(a, dict)]
            detalle = _corto(tapar(" · ".join(x for x in acc if x)), 200)
            url = next((a.get("input", {}).get("url") for a in ent.get("actions") or [] if isinstance(a, dict) and a.get("input", {}).get("url")), "")
        else:
            detalle = _corto(tapar(ent.get("action_summary") or ent.get("text") or ent.get("query") or ""), 200)
        host = re.sub(r"^https?://", "", url).split("/")[0][:60]
        return dict(tipo="navegador", verbo=_NAV.get(corto, "Usa"), host=host, detalle=detalle, url=url)
    return None


def _estacion_navegador(host, ev):
    if "labs.google" in host:
        return "imagenes"
    if "studio.youtube" in host and ("/videos/upload" in ev["url"] or (ev["verbo"] != "Lee" and _STUDIO_EDITA.search(ev["detalle"]))):
        return "subida"                                    # mirar Studio no es subir
    return None


def _sitio(url):
    return re.sub(r"^https?://(www\.)?", "", url or "").split("/")[0][:60]


def _titulo_url(url):
    cola = unquote(re.sub(r"[?#].*$", "", url or "").rstrip("/").rsplit("/", 1)[-1])
    return re.sub(r"[-_]+", " ", cola)[:110]


def _enlaces(texto):
    """[(título, url)] de lo que devuelve WebSearch: «Links: [{title, url}…]», a veces en varios bloques."""
    filas = {}
    for m in re.finditer(r"Links: (\[.*?\])\s*(?:\n|$)", texto or ""):
        try:
            for x in json.loads(m.group(1)):
                filas.setdefault(x.get("url"), x.get("title") or "")
        except (ValueError, AttributeError):
            pass
    return [(t, u) for u, t in filas.items() if u]


def _ruta_corta(ruta):
    r = (ruta or "").replace("\\", "/")
    for marca in ("/FabricaAnimaciones/", "/fab_vivo/"):
        if marca in r:
            return tapar(r.split(marca, 1)[1])
    return tapar(r.rsplit("/", 2)[-1] if r.count("/") > 2 else r)


def _texto_resultado(cont):
    if isinstance(cont, str):
        return cont
    if isinstance(cont, list):
        return "\n".join(b.get("text", "") for b in cont if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _imagen_de(cont):
    if isinstance(cont, list):
        for b in cont:
            if isinstance(b, dict) and b.get("type") == "image" and (b.get("source") or {}).get("type") == "base64":
                return b["source"].get("data")
    return None


def _usuario_limpio(texto):
    """El mensaje del usuario, sin los bloques que añade la app."""
    t = re.sub(r"<(system-reminder|local-command[\w-]*|command-[\w-]+|ide_[\w-]+|side-sessions-event|ci-monitor-event|task-notification)\b.*?</\1>", "",
               texto or "", flags=re.S)
    t = re.sub(r"<pasted_content.*?</pasted_content>", "[texto pegado]", t, flags=re.S)
    return t.strip()


# Entran como mensaje de usuario, pero no los escribió él
_AJENOS = (("Background (from the session that started this one)", "Encargo de la sesión que la lanzó"),
           ("Another Claude session sent a message", "Mensaje de otra sesión"),
           ("This session is being continued from a previous conversation", "Resumen de la sesión anterior"))


def _epoch(iso):
    try:
        return datetime.fromisoformat((iso or "").replace("Z", "+00:00")).timestamp()
    except ValueError:
        return time.time()


# ---------------------------------------------------------------- lectura incremental de una sesión
class _Archivo:
    """Un .jsonl que crece: da solo las líneas completas nuevas (la última puede estar a medio escribir)."""

    def __init__(self, ruta, cola):
        self.ruta, self.cola = ruta, cola
        self.pos = 0
        self.resto = b""

    def nuevas(self):
        try:
            tam = os.path.getsize(self.ruta)
        except OSError:
            return []
        if tam == self.pos:
            return []
        with open(self.ruta, "rb") as f:
            if self.pos == 0 and tam > self.cola:
                f.seek(tam - self.cola)
                f.readline()               # la primera línea queda partida
            else:
                f.seek(self.pos)
            datos = f.read()
            self.pos = f.tell()
        lineas = (self.resto + datos).split(b"\n")
        self.resto = lineas.pop()
        return lineas


_CUENTA = {"WebSearch": "busquedas", "WebFetch": "paginas", "Read": "lecturas", "Grep": "lecturas", "Glob": "lecturas",
           "Write": "escrituras", "Edit": "escrituras", "Bash": "comandos", "PowerShell": "comandos"}
_REVISA = re.compile(r"verific|revis|comprob|audit|review|check", re.I)
_FONDO_ESTACION = {"render": "rodador", "voz": "cantor", "imagenes": "pintor", "clips": "cargador"}


class _Ayudante:
    """Un subagente: su propio archivo en <sesion>/subagents/. Sus tool_use_id quedan en su propio `abiertos`."""

    def __init__(self, id_, ruta):
        self.id = id_
        self.arch = _Archivo(ruta, COLA_AYUD)
        self.abiertos = {}
        self.cuenta = collections.Counter()
        self.eventos = collections.deque(maxlen=MAX_EV_AYUD)
        self.ultima = ""
        self.accion = ""                   # tipo del último evento: lo que su mini está haciendo de verdad
        self.host = ""
        self.t = 0.0
        self.desc = ""
        try:
            with open(ruta[:-6] + ".meta.json", encoding="utf-8") as f:
                self.desc = tapar(str(json.load(f).get("description") or ""))[:70]
        except (OSError, ValueError, AttributeError):
            pass

    @property
    def tipo(self):
        c = self.cuenta
        web = c["busquedas"] + c["paginas"]
        if web >= 3 and web >= c["lecturas"] + c["escrituras"]:
            return "investigador"
        if _REVISA.search(self.desc):
            return "inspector"
        if web:
            return "investigador"
        return "obrero" if c["escrituras"] >= 3 and c["escrituras"] * 3 >= c["lecturas"] else "explorador"


class Sesion:
    def __init__(self, id_, ruta):
        self.id, self.ruta = id_, ruta
        self.arch = _Archivo(ruta, COLA_BYTES)
        self.ayud = {}                     # id -> _Ayudante
        self.ayud_t = 0.0
        self.fondo = {}                    # tool_use_id -> comando en segundo plano sin aviso de fin
        self.titulos = {}                  # url -> título visto en una búsqueda
        self.cuenta = collections.Counter()
        self.seq = 0
        self.rev = 0                       # sube con cada evento nuevo o completado (la imagen llega después de la llamada)
        self.eventos = collections.deque(maxlen=MAX_EVENTOS)
        self.abiertos = {}                 # tool_use_id -> evento, para pegarle el resultado
        self.plan = []
        self.titulo = ""
        self.estacion = None
        self.produce = collections.Counter()    # video -> herramientas que lo produjeron (ver `_videos_producidos`)
        self.produce_t = {}                # video -> última vez que se produjo
        self.ultimo_t = 0.0
        self.pensando = False
        self.host = ""
        self.n_img = 0
        self.lock = threading.Lock()

    def actualizar(self):
        with self.lock:
            lote = []                          # el principal y sus ayudantes entran por hora en la misma línea de tiempo
            for ln in self.arch.nuevas():
                d = self._leer(ln)
                if d:
                    lote.append((_epoch(d.get("timestamp")), d, None))
            for a in self._ayudantes_al_dia():
                for ln in a.arch.nuevas():
                    d = self._leer_ayudante(ln)
                    if d:
                        lote.append((_epoch(d.get("timestamp")), d, a))
            lote.sort(key=lambda x: x[0])
            for t, d, a in lote:
                if a:
                    self._linea_ayudante(a, t, d)
                else:
                    self._linea(t, d)

    def _ayudantes_al_dia(self):
        ahora = time.time()
        if ahora - self.ayud_t < AYUD_CADA:
            return []
        self.ayud_t = ahora
        hallados = []
        try:
            for x in os.scandir(os.path.join(self.ruta[:-6], "subagents")):
                if x.name.startswith("agent-") and x.name.endswith(".jsonl"):
                    mt = x.stat().st_mtime
                    if ahora - mt < HORAS_AYUD * 3600:
                        hallados.append((mt, x.name[6:-6], x.path))
        except OSError:
            return []
        hallados.sort(reverse=True)
        for _, id_, ruta in hallados[:MAX_AYUD]:
            if id_ not in self.ayud:
                self.ayud[id_] = _Ayudante(id_, ruta)
        return [self.ayud[id_] for _, id_, _ in hallados[:MAX_AYUD]]

    def _leer(self, ln):
        # las líneas con imágenes pesan MB: se descartan rápido las que no interesan
        if b'"customTitle"' in ln[:300]:
            try:
                self.titulo = json.loads(ln).get("customTitle") or self.titulo
            except ValueError:
                pass
            return None
        if b'"type":"assistant"' not in ln and b'"type":"user"' not in ln:
            return None
        try:
            d = json.loads(ln)
        except ValueError:
            return None
        return d if d.get("type") in ("assistant", "user") and not d.get("isSidechain") else None

    def _leer_ayudante(self, ln):
        if len(ln) > LINEA_AYUD or (b'"tool_use"' not in ln and b'"tool_result"' not in ln):
            return None
        try:
            d = json.loads(ln)
        except ValueError:
            return None
        return d if d.get("type") in ("assistant", "user") else None   # hay líneas `api-request-blob`, sin hora

    def _evidencia(self, nombre, ent, t):
        for v in _videos_producidos(nombre, ent):
            self.produce[v] += 1
            self.produce_t[v] = t

    def _linea_ayudante(self, a, t, d):
        """Cada acción va a la línea del ayudante, aparte de la del principal (`a.eventos`): la página las intercala por `seq`."""
        a.t = max(a.t, t)
        cont = (d.get("message") or {}).get("content")
        for b in cont if isinstance(cont, list) else []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use":
                nombre, ent = b.get("name") or "", b.get("input")
                if nombre in _CUENTA:
                    a.cuenta[_CUENTA[nombre]] += 1
                self._evidencia(nombre, ent, t)
                ev = _evento_herramienta(nombre, ent)
                if not ev or ev["tipo"] == "ayudante":
                    continue
                if ev["tipo"] == "navegador":
                    a.host = ev.pop("host") or a.host
                    ev["titulo"] = f"{ev.pop('verbo')} {a.host or 'el navegador'}"
                    ev.pop("url")
                a.ultima = ev.get("titulo") or a.ultima
                a.accion = ev["tipo"]
                ev.update(de=a.id, quien=a.desc)
                self._poner(ev, t, a)
                a.abiertos[b.get("id")] = ev
                if len(a.abiertos) > 200:
                    a.abiertos.pop(next(iter(a.abiertos)))
            elif b.get("type") == "tool_result":
                ev = a.abiertos.pop(b.get("tool_use_id"), None)
                if ev is not None:
                    self._resultado(ev, b)

    def ayudantes(self):
        """Los ayudantes y comandos de fondo con trabajo real detrás, más los que acaban de terminar (la página los ve despedirse)."""
        ahora = time.time()
        filas = []
        for a in list(self.ayud.values()):
            try:
                mt = os.path.getmtime(a.arch.ruta)
            except OSError:
                continue
            if ahora - mt < MAX_ULTIMOS_S:
                filas.append(dict(id=a.id, tipo=a.tipo, desc=a.desc, activo=ahora - mt < ACTIVA_S, ultima=a.ultima, accion=a.accion, t=a.t, **a.cuenta))
        try:
            reciente = ahora - os.path.getmtime(self.ruta) < 1800  # sin la sesión viva nadie avisaría de su fin
        except OSError:
            reciente = False
        for k, f in list(self.fondo.items()):
            if ahora - f["t"] > FONDO_MAX_S:
                del self.fondo[k]
            elif reciente:
                filas.append(dict(id=k[-12:], tipo=f["tipo"], desc=f["desc"], activo=True, ultima=f["desc"], t=f["t"], fondo=True))
        return filas

    def equipo(self):
        """Todos los ayudantes con acciones en la línea, aunque ya hayan terminado: el selector del historial los necesita."""
        ahora = time.time()
        filas = []
        for a in list(self.ayud.values()):
            if a.eventos:
                try:
                    activo = ahora - os.path.getmtime(a.arch.ruta) < ACTIVA_S
                except OSError:
                    activo = False
                filas.append(dict(id=a.id, tipo=a.tipo, desc=a.desc, activo=activo, n=len(a.eventos), t=a.t))
        return sorted(filas, key=lambda x: -x["t"])

    def _fin_fondo(self, texto):
        for k in re.findall(r"<tool-use-id>([\w-]+)</tool-use-id>", texto or ""):
            self.fondo.pop(k, None)

    def _linea(self, t, d):
        self.ultimo_t = max(self.ultimo_t, t)
        cont = (d.get("message") or {}).get("content")
        if d["type"] == "user":
            self._usuario(cont, t, d)
        elif isinstance(cont, list):
            self.pensando = False
            for b in cont:
                if isinstance(b, dict):
                    self._asistente(b, t)

    def _usuario(self, cont, t, d):
        if isinstance(cont, str):
            self._fin_fondo(cont)
            texto = _usuario_limpio(cont)
            if texto and not d.get("isMeta"):
                self._mensaje(texto, t)
            return
        if not isinstance(cont, list):
            return
        for b in cont:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_result":
                ev = self.abiertos.pop(b.get("tool_use_id"), None)
                if ev is not None:
                    self._resultado(ev, b)
            elif b.get("type") == "text":
                self._fin_fondo(b.get("text"))
                texto = "" if d.get("isMeta") else _usuario_limpio(b.get("text"))
                if texto:
                    self._mensaje(texto, t)

    def _mensaje(self, texto, t):
        for marca, titulo in _AJENOS:
            if texto.startswith(marca):
                resto = texto[len(marca):].lstrip(":. \n")
                return self._poner(dict(tipo="encargo", titulo=titulo, detalle=_corto(tapar(sin_markdown(resto)), 400)), t)
        self._poner(dict(tipo="usuario", titulo="El usuario", detalle=_corto(tapar(sin_markdown(texto)), 400)), t)

    def _asistente(self, b, t):
        tipo = b.get("type")
        if tipo == "text":
            texto = (b.get("text") or "").strip()
            if texto:
                self._poner(dict(tipo="habla", titulo="Explica", detalle=_corto(tapar(sin_markdown(texto)), 420)), t)
        elif tipo == "thinking":
            self.pensando = True
        elif tipo == "tool_use":
            nombre, ent = b.get("name") or "", b.get("input")
            if nombre == "mcp__ccd_turn__update_plan":
                return self._plan(ent or {}, t)
            if nombre == "mcp__ccd_turn__wrap_up":
                return self._poner(dict(tipo="cierre", titulo="Cierra el tramo", detalle=_corto(tapar(sin_markdown((ent or {}).get("recap"))), 320)), t)
            self._evidencia(nombre, ent, t)
            ev = _evento_herramienta(nombre, ent)
            if ev and ev["tipo"] == "navegador":      # los clics no traen dirección: siguen en el último sitio abierto
                self.host = ev.pop("host") or self.host
                ev["estacion"] = _estacion_navegador(self.host, ev)
                ev["titulo"] = f"{ev.pop('verbo')} {self.host or 'el navegador'}"
                ev.pop("url")
            if ev:
                self._poner(ev, t)
                if ev["tipo"] == "comando" and (ent or {}).get("run_in_background"):
                    self._a_fondo(b.get("id"), ev, t)
                self.abiertos[b.get("id")] = ev
                if len(self.abiertos) > 200:
                    self.abiertos.pop(next(iter(self.abiertos)))

    def _a_fondo(self, id_, ev, t):
        est = ev.get("estacion")
        tipo = _FONDO_ESTACION.get(est) or ("cargador" if est == "sonido" and _BAJA.match(ev["titulo"].lower()) else None)
        if tipo:
            self.fondo[id_] = dict(tipo=tipo, desc=_corto(ev["titulo"], 70), t=t)

    def _plan(self, ent, t):
        if ent.get("items"):
            self.plan = [dict(texto=tapar(str(i.get("content") or ""))[:90], estado=i.get("status") or "pending")
                         for i in ent["items"] if isinstance(i, dict)]
        else:
            actual = next((i for i, p in enumerate(self.plan) if p["estado"] == "in_progress"), None)
            if ent.get("advance") and actual is not None:
                self.plan[actual]["estado"] = "completed"
                sig = next((p for p in self.plan[actual + 1:] if p["estado"] == "pending"), None)
                if sig:
                    sig["estado"] = "in_progress"
            for n in ent.get("done") or []:
                if 0 < n <= len(self.plan):
                    self.plan[n - 1]["estado"] = "completed"
            n = ent.get("start")
            if isinstance(n, int) and 0 < n <= len(self.plan):
                self.plan[n - 1]["estado"] = "in_progress"
        hecho = next((p["texto"] for p in self.plan if p["estado"] == "in_progress"), "")
        if hecho:
            self._poner(dict(tipo="paso", titulo=hecho, plan=[dict(p) for p in self.plan]), t)

    def _resultado(self, ev, b):
        cont = b.get("content")
        datos = _imagen_de(cont)
        self.rev += 1
        ev.update(rev=self.rev, listo=True)
        if ev["tipo"] in ("imagen", "navegador") and datos:
            ev["img"] = self._guardar(datos, ev["seq"])
        if ev["tipo"] == "privado":
            return
        texto = tapar(_texto_resultado(cont))
        if b.get("is_error"):
            ev["fallo"] = True
        if ev["tipo"] == "leer" and texto:
            texto = re.sub(r"(?m)^\s*\d+\t", "", texto)
            ev["extracto"] = _recortar(texto, 18, 120)[0]
        elif ev["tipo"] == "comando" and texto:
            filas = [x for x in texto.replace("\r\n", "\n").split("\n") if x.strip()]
            ev["salida"] = _recortar("\n".join(filas[-10:]), 10, 140)[0]
        elif ev["tipo"] == "buscar" and texto:
            ev["detalle"] = f"{sum(1 for x in texto.split(chr(10)) if x.strip())} resultados"
        elif ev["tipo"] == "busqueda":
            filas = _enlaces(_texto_resultado(cont))
            for titulo, url in filas:
                self.titulos[tapar(url)] = tapar(titulo)[:110]
            ev["detalle"] = f"{len(filas)} resultados"
            ev["resultados"] = [dict(titulo=tapar(ti)[:110], sitio=_sitio(tapar(u))) for ti, u in filas[:7]]
        elif ev["tipo"] == "pagina":
            if texto.startswith(("The server returned HTTP", "Error")):
                ev["fallo"] = True
            ev["pag_titulo"] = self.titulos.get(ev["url"]) or _titulo_url(ev["url"])
            ev["extracto"] = _corto(sin_markdown(texto), 420)
            ev["detalle"] = ev["pag_titulo"]

    def _guardar(self, datos, seq):
        """Guarda la imagen reducida en la caché; devuelve su nombre (None si no se pudo)."""
        nombre = f"{seq:06d}_{hashlib.sha1(datos[:4096].encode('ascii', 'ignore')).hexdigest()[:10]}.jpg"
        carpeta = os.path.join(CACHE, self.id)
        real = os.path.join(carpeta, nombre)
        try:
            if not os.path.exists(real):
                from PIL import Image
                os.makedirs(carpeta, exist_ok=True)
                im = Image.open(io.BytesIO(base64.b64decode(datos)))
                im.thumbnail((ANCHO_IMG, ANCHO_IMG))
                im.convert("RGB").save(real, "JPEG", quality=72)
                self._podar(carpeta)
        except Exception:                  # noqa: BLE001  (una imagen rara no debe tumbar la lectura)
            return None
        return nombre

    def _podar(self, carpeta):
        self.n_img += 1
        if self.n_img % 20 == 0:
            for viejo in sorted(os.listdir(carpeta))[:-MAX_IMAGENES]:
                try:
                    os.remove(os.path.join(carpeta, viejo))
                except OSError:
                    pass

    def _poner(self, ev, t, ayudante=None):
        self.seq += 1
        self.rev += 1
        ev.update(seq=self.seq, rev=self.rev, t=t)
        if not ayudante:                                   # el principal: sin estación no se arrastra la anterior
            self.estacion = ev.get("estacion")
        ev["en"] = self.estacion
        if ev["tipo"] in ("busqueda", "pagina"):
            self.cuenta[ev["tipo"]] += 1
        (ayudante.eventos if ayudante else self.eventos).append(ev)

    def lista(self, desde=0):
        """Lo que hay que mandar, por orden: lo nuevo desde la revisión `desde`, o al abrir el final de cada línea por separado.
        desde > rev: el panel se reinició y volvió a leer la sesión; se manda todo otra vez."""
        with self.lock:
            lineas = [self.eventos] + [a.eventos for a in self.ayud.values()]
            if 0 < desde <= self.rev:
                filas = [e for ln in lineas for e in ln if e["rev"] > desde]
            else:
                filas = list(self.eventos)[-PRIMERA:] + [e for a in self.ayud.values() for e in list(a.eventos)[-PRIMERA_AYUD:]]
        return sorted(filas, key=lambda e: e["seq"])

    @property
    def video(self):
        """El video de esta sesión: el que más produjo o, si aún no produjo nada, el que nombra su título. Si no, ninguno."""
        return self.produce.most_common(1)[0][0] if self.produce else _video_del_titulo(self.titulo)


# ---------------------------------------------------------- qué hace la PC: la tarea real, clasificada aquí para que `cmd` no salga por la API
TAREA_MIN_CPU = 2.5                    # % del total: por debajo es vigilancia, no tarea
_NO_TAREA = re.compile(r"Panel de la f[aá]brica|panel_remoto|monitor_server|esperar_respuestas|enviar_lote|baileys|server\.js|^node$", re.I)
_TIPOS_TAREA = (("subida", re.compile(r"fab\.py yt (subir|aplicar|publicar)|pagina\.py.*programar|\bupload", re.I)),
                ("comprimir", re.compile(r"comprim|compress|libx265|hevc", re.I)),
                ("revisar", re.compile(r"medir_brillo|verificar|comprobar|revis[ae]|hoja_", re.I)),
                ("voz", re.compile(r"chatterbox|applio|rvc|tts_|fab\.py (voz|seleccionar)", re.I)),
                ("transcribir", re.compile(r"whisper|transcrib|fab\.py tiempo", re.I)),
                ("mezcla", re.compile(r"mezcla|demucs|armar_musica|armar_ost|lyria|fab\.py (musica|sfx|ambiente)", re.I)),
                ("descargas", re.compile(r"yt[-_]dlp|fab\.py bajar|descarg", re.I)),
                ("ia", re.compile(r"tactica|\bwan\b|comfy|flux|torch", re.I)),
                ("render", re.compile(r"ffmpeg|secuencia|render|fab\.py (video|final|todo|fx|montaje|escena|prueba)", re.I)))


def tarea_pc(d):
    """{tipo, nombre, video, cpu, gpu} de lo que más carga la PC ahora, con solo lo que puede salir a internet.
    Un proceso que no se reconoce es `generica`, sin inventar qué hace; sin procesos con carga, `libre`."""
    try:
        gpu = d.get("gpu") or {}
        en_gpu = {g.get("pid") for g in gpu.get("procesos") or []}
        cpu_pc, gpu_pc = (d.get("cpu") or {}).get("uso") or 0, gpu.get("uso") or 0
        mejor, puntos = None, 0.0
        for tr in d.get("procesos") or []:
            texto = " ".join([tr.get("rol") or "", tr.get("cmd") or ""] + [h.get("rol") or "" for h in tr.get("hijos") or []])
            if _NO_TAREA.search(tr.get("rol") or ""):
                continue
            usa_gpu = bool(en_gpu & ({tr.get("pid")} | {h.get("pid") for h in tr.get("hijos") or []}))
            p = max(tr.get("cpu_total") or 0, gpu_pc if usa_gpu else 0)
            if p >= TAREA_MIN_CPU and p > puntos:
                mejor, puntos = (tr, texto, usa_gpu), p
        if not mejor:
            if max(cpu_pc, gpu_pc) >= 60:
                return dict(tipo="generica", nombre="Otros programas", video=None, cpu=cpu_pc, gpu=gpu_pc)
            return dict(tipo="libre", nombre="", video=None, cpu=cpu_pc, gpu=gpu_pc)
        tr, texto, usa_gpu = mejor
        tipo = next((k for k, rx in _TIPOS_TAREA if rx.search(texto)), "ia" if usa_gpu and gpu_pc >= 30 else "generica")
        nombre = _corto(tapar(tr.get("rol") or tr.get("nombre") or "proceso"), 34)
        return dict(tipo=tipo, nombre=nombre, video=tr.get("video"), cpu=cpu_pc, gpu=gpu_pc)
    except Exception:                      # noqa: BLE001  (una tarea mal leída no debe parar el muestreo)
        return None


def proceso_publico(tr):
    """Un trabajo tal como sale por /api/v2/sistema: sin `cmd`, que puede llevar claves, y con `rol` tapado."""
    d = {k: v for k, v in tr.items() if k != "cmd"}
    d["rol"] = tapar(d.get("rol") or "")
    d["hijos"] = [dict(h, rol=tapar(h.get("rol") or "")) for h in tr.get("hijos") or []]
    return d


# ---------------------------------------------------------- actividad por disco: el tiempo ocupado que da Windows, en 100 ns
def _ioctl(ruta, codigo, tam):
    import ctypes
    from ctypes import wintypes
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    k.CreateFileW.restype = wintypes.HANDLE
    k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    k.DeviceIoControl.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD,
                                  ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    h = k.CreateFileW(ruta, 0, 3, None, 3, 0, None)
    if h in (None, wintypes.HANDLE(-1).value):
        return None
    try:
        b = ctypes.create_string_buffer(tam)
        n = wintypes.DWORD()
        return b.raw if k.DeviceIoControl(h, codigo, None, 0, b, tam, ctypes.byref(n), None) else None
    finally:
        k.CloseHandle(h)


def _disco_de(unidad):
    """El PhysicalDrive de una unidad, o None si no se puede decir con certeza (varios discos, unidad virtual)."""
    b = _ioctl("\\\\.\\" + unidad, 0x00560000, 256)            # IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS
    if not b:
        return None
    return struct.unpack_from("<I", b, 8)[0] if struct.unpack_from("<I", b, 0)[0] == 1 else None


def tasas_discos(c):
    """{unidad: {lee, esc, act}} en MB/s y % de tiempo ocupado desde la lectura anterior. Lo que no se pueda medir no sale."""
    try:
        if os.name != "nt":
            return {}
        ahora = time.time()
        m = c.get("disco_mapa")
        if not m or ahora - m[0] > 600:
            m = c["disco_mapa"] = (ahora, {u: _disco_de(u) for u in ("C:", "E:")})
        antes, nuevo, out = c.get("disco_perf") or {}, {}, {}
        for u, n in m[1].items():
            b = None if n is None else _ioctl(f"\\\\.\\PhysicalDrive{n}", 0x00070020, 256)   # IOCTL_DISK_PERFORMANCE
            if not b:
                continue
            leidos, escritos, _, _, ocioso = struct.unpack_from("<qqqqq", b, 0)
            reloj = struct.unpack_from("<q", b, 56)[0]
            nuevo[n] = (leidos, escritos, ocioso, reloj)
            q = antes.get(n)
            if q and reloj > q[3]:
                dt = reloj - q[3]                              # 100 ns
                s = dt / 1e7
                out[u] = dict(lee=round((leidos - q[0]) / s / 1048576, 1), esc=round((escritos - q[1]) / s / 1048576, 1),
                              act=round(min(100.0, max(0.0, 100 * (1 - (ocioso - q[2]) / dt))), 1))
        c["disco_perf"] = nuevo
        return out
    except Exception:                      # noqa: BLE001  (sin esta cifra el disco sale apagado, no se inventa)
        return {}


_SES = {}
_LOCK = threading.Lock()


def _sesion(id_):
    if not re.match(r"^[A-Za-z0-9-]{8,64}$", id_ or ""):
        return None
    ruta = os.path.join(CARPETA, id_ + ".jsonl")
    if not os.path.isfile(ruta):
        return None
    with _LOCK:
        s = _SES.get(id_)
        if s is None:
            s = _SES[id_] = Sesion(id_, ruta)
    s.actualizar()
    return s


_LISTA = {"t": 0.0, "v": [], "limpio": 0.0}


def _limpiar_cache():
    """Una vez por hora borra las imágenes de sesiones de hace más de 3 días (C: va justo de espacio)."""
    if time.time() - _LISTA["limpio"] < 3600 or not os.path.isdir(CACHE):
        return
    _LISTA["limpio"] = time.time()
    for carpeta in os.scandir(CACHE):
        if carpeta.is_dir() and time.time() - carpeta.stat().st_mtime > 3 * 86400:
            shutil.rmtree(carpeta.path, ignore_errors=True)


def sesiones():
    """Las sesiones con actividad en las últimas horas, la más reciente primero."""
    if time.time() - _LISTA["t"] < 4:
        return _LISTA["v"]
    ahora = time.time()
    filas = []
    for ruta in glob.glob(os.path.join(CARPETA, "*.jsonl")):
        try:
            mt = os.path.getmtime(ruta)
        except OSError:
            continue
        if ahora - mt > HORAS * 3600:
            continue
        s = _sesion(os.path.basename(ruta)[:-6])
        if s and s.seq:
            v = s.video
            filas.append(dict(id=s.id, titulo=tapar(s.titulo)[:70], video=v, t=mt, prod=s.produce_t.get(v) or mt, activa=ahora - mt < ACTIVA_S, eventos=s.seq))
    filas.sort(key=lambda x: -x["t"])
    _LISTA.update(t=ahora, v=filas)
    _limpiar_cache()
    return filas


def eventos(sesion="", video="", desde=0):
    """{sesion, video, titulo, activa, pensando, plan, estacion, rev, eventos} con lo nuevo o cambiado desde la revisión `desde`.
    Sin sesión sigue a la que produjo ese video más recientemente (o a la más reciente con video): el corte a 180 mil abre otra
    y hay que pasar a ella. Una sesión que solo lo leyó o lo mencionó no es de ese video."""
    if not sesion:
        lista = sesiones()
        if video:
            elegida = max((x for x in lista if x["video"] == video), key=lambda x: x["prod"], default=None)
        else:
            elegida = next((x for x in lista if x["video"]), None) or (lista[0] if lista else None)
        sesion = elegida["id"] if elegida else ""
    s = _sesion(sesion)
    if not s:
        return dict(sesion="", eventos=[], rev=0, plan=[], activa=False)
    try:
        mt = os.path.getmtime(s.ruta)
    except OSError:
        mt = 0
    nuevos = s.lista(desde)
    return dict(sesion=s.id, video=s.video, titulo=tapar(s.titulo)[:70], activa=time.time() - mt < ACTIVA_S,
                pensando=s.pensando, plan=s.plan, estacion=s.estacion, rev=s.rev, ultimo=s.ultimo_t, eventos=nuevos,
                ayudantes=s.ayudantes(), equipo=s.equipo(), web=dict(busquedas=s.cuenta["busqueda"], paginas=s.cuenta["pagina"]))


def imagen(sesion, nombre):
    if not re.match(r"^[A-Za-z0-9-]{8,64}$", sesion or "") or not re.match(r"^\d{6}_[0-9a-f]{10}\.jpg$", nombre or ""):
        return None
    real = os.path.join(CACHE, sesion, nombre)
    return real if os.path.isfile(real) else None


if __name__ == "__main__":
    import sys
    t0 = time.time()
    if len(sys.argv) > 1:
        r = eventos(sesion=sys.argv[1])
    else:
        print(json.dumps(sesiones(), ensure_ascii=False, indent=1))
        r = eventos()
    print(f"{time.time() - t0:.2f} s · sesión {r['sesion']} · {r.get('video')} · {len(r['eventos'])} eventos · plan {len(r['plan'])}")
    for e in r["eventos"][-14:]:
        print(e["seq"], e["tipo"], e.get("en"), "|", e["titulo"][:80], "| img" if e.get("img") else "")
    assert tapar("key=sk-abcdefghijklmnop1234 AIzaSyA1234567890123456789012345678901234 pepe@gmail.com") .count("••••") >= 3
    assert sin_markdown("[La sesión](#local_05cc) deja **listo** `fab.py` y 2*3*4") == "La sesión deja listo fab.py y 2*3*4"
