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
import tempfile
import threading
import time
from datetime import datetime

CARPETA = os.path.join(os.path.expanduser("~"), ".claude", "projects", "C--FabricaAnimaciones")
VIDEOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos")
CACHE = os.path.join(tempfile.gettempdir(), "fab_vivo")
HORAS = 12                             # sesiones que se listan
ACTIVA_S = 120                         # sin escribir en este tiempo, la sesión ya no cuenta como «en vivo»
COLA_BYTES = 40_000_000                # al abrir una sesión se lee solo su final (con imágenes pesan decenas de MB)
MAX_EVENTOS = 500
PRIMERA = 160                          # eventos que se mandan al abrir la página (la ventana de la repetición)
MAX_IMAGENES = 200                     # imágenes por sesión en la caché (reducidas a ANCHO_IMG, ~50 KB cada una)
ANCHO_IMG = 960
MAX_LINEAS = 70                        # código o comando por evento
MAX_COL = 170

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


def _corto(texto, n=240):
    t = " ".join((texto or "").split())
    return t[:n] + ("…" if len(t) > n else "")


# ---------------------------------------------------------------- de herramienta a evento
ESTACIONES = ["guion", "voz", "sonido", "imagenes", "clips", "animacion", "render", "revision", "subida"]
_FAB = re.compile(r"fab\.py\s+([a-z0-9_]+)\s+([a-z_]+)")
_VIDEO = re.compile(r"videos[\\/]+([a-z0-9][a-z0-9_]*)[\\/]+")
_FAB_ESTACION = {"voz": "voz", "seleccionar": "voz", "tiempo": "voz", "musica": "sonido", "sfx": "sonido", "mezcla": "sonido",
                 "ambiente": "sonido", "video": "render", "final": "render", "todo": "render", "verificar": "revision",
                 "escena": "animacion", "comprobar": "animacion", "fx": "animacion", "montaje": "animacion", "prueba": "animacion",
                 "beats": "guion", "prompts": "imagenes", "servir": "imagenes", "ingesta": "imagenes", "medios": "imagenes",
                 "busquedas": "imagenes", "fuentes": "imagenes", "bajar": "clips", "miniatura": "imagenes"}


def _video_de(*textos):
    for t in textos:
        for v in _VIDEO.findall(t or ""):
            if not v.startswith("_"):
                return v
        m = _FAB.search(t or "")
        if m and os.path.isdir(os.path.join(VIDEOS, m.group(1))):
            return m.group(1)
    return None


def _estacion_cmd(cmd):
    m = _FAB.search(cmd)
    if m and m.group(2) in _FAB_ESTACION:
        return _FAB_ESTACION[m.group(2)]
    c = cmd.lower()
    if "yt subir" in c or "fab.py yt " in c or "pagina.py" in c:
        return "subida"
    if "yt-dlp" in c or "yt_dlp" in c:
        return "clips"
    if "lyria" in c or "demucs" in c or "armar_musica" in c:
        return "sonido"
    if "ffmpeg" in c or "render" in c:
        return "render"
    return None


def _estacion_archivo(ruta):
    r = (ruta or "").replace("\\", "/").lower()
    base = r.rsplit("/", 1)[-1]
    if base == "guion.py" or base.endswith(".srt"):
        return "guion"
    if "/audio/" in r or base.endswith((".wav", ".mp3")):
        return "sonido"
    if "/flow/" in r or "/piezas/" in r or "prompts" in base:
        return "imagenes"
    if base.endswith(".py") and ("/videos/" in r or "/nucleo/" in r):
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
            return dict(tipo="imagen", titulo=f"Mira {base}", ruta=_ruta_corta(ruta), video=_video_de(ruta), estacion="revision")
        return dict(tipo="leer", titulo=f"Lee {base}", ruta=_ruta_corta(ruta), video=_video_de(ruta))
    if nombre == "Write":
        ruta = ent.get("file_path") or ""
        if sensible(ruta):
            return dict(tipo="privado", titulo="Archivo privado", detalle="contenido oculto")
        codigo, sobran = _recortar(tapar(ent.get("content") or ""))
        return dict(tipo="codigo", titulo=f"Escribe {os.path.basename(ruta)}", ruta=_ruta_corta(ruta), video=_video_de(ruta),
                    estacion=_estacion_archivo(ruta), lineas=[["+", x] for x in codigo.split("\n")], sobran=sobran,
                    nuevas=(ent.get("content") or "").count("\n") + 1, quitadas=0)
    if nombre == "Edit":
        ruta = ent.get("file_path") or ""
        if sensible(ruta):
            return dict(tipo="privado", titulo="Archivo privado", detalle="contenido oculto")
        filas, sobran = _diff(ent.get("old_string"), ent.get("new_string"))
        return dict(tipo="codigo", titulo=f"Edita {os.path.basename(ruta)}", ruta=_ruta_corta(ruta), video=_video_de(ruta),
                    estacion=_estacion_archivo(ruta), lineas=filas, sobran=sobran,
                    nuevas=sum(1 for s, _ in filas if s == "+"), quitadas=sum(1 for s, _ in filas if s == "-"))
    if nombre in ("Bash", "PowerShell"):
        cmd = ent.get("command") or ""
        if sensible(cmd):
            return dict(tipo="privado", titulo="Comando con datos privados", detalle=_corto(tapar(ent.get("description") or ""), 120))
        texto, sobran = _recortar(tapar(cmd), 24)
        return dict(tipo="comando", titulo=_corto(tapar(ent.get("description") or "") or tapar(cmd), 110), comando=texto,
                    sobran=sobran, video=_video_de(cmd), estacion=_estacion_cmd(cmd))
    if nombre in ("Grep", "Glob"):
        return dict(tipo="buscar", titulo=f"Busca «{_corto(tapar(ent.get('pattern') or ''), 70)}»",
                    ruta=_ruta_corta(ent.get("path") or ""), video=_video_de(ent.get("path")))
    if nombre == "Agent":
        return dict(tipo="ayudante", titulo=_corto(tapar(ent.get("description") or "Ayudante"), 90))
    if nombre == "Artifact":
        return dict(tipo="leer", titulo="Publica una página")
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
        return dict(tipo="navegador", verbo=_NAV.get(corto, "Usa"), host=host, detalle=detalle)
    return None


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
    t = re.sub(r"<(system-reminder|local-command[\w-]*|command-[\w-]+|ide_[\w-]+|side-sessions-event|ci-monitor-event)\b.*?</\1>", "",
               texto or "", flags=re.S)
    t = re.sub(r"<pasted_content.*?</pasted_content>", "[texto pegado]", t, flags=re.S)
    return t.strip()


def _epoch(iso):
    try:
        return datetime.fromisoformat((iso or "").replace("Z", "+00:00")).timestamp()
    except ValueError:
        return time.time()


# ---------------------------------------------------------------- lectura incremental de una sesión
class Sesion:
    def __init__(self, id_, ruta):
        self.id, self.ruta = id_, ruta
        self.pos = 0
        self.seq = 0
        self.rev = 0                       # sube con cada evento nuevo o completado (la imagen llega después de la llamada)
        self.eventos = collections.deque(maxlen=MAX_EVENTOS)
        self.abiertos = {}                 # tool_use_id -> evento, para pegarle el resultado
        self.plan = []
        self.titulo = ""
        self.estacion = None
        self.conteo = collections.Counter()
        self.ultimo_t = 0.0
        self.pensando = False
        self.host = ""
        self.n_img = 0
        self.resto = b""
        self.lock = threading.Lock()

    def actualizar(self):
        with self.lock:
            try:
                tam = os.path.getsize(self.ruta)
            except OSError:
                return
            if tam == self.pos:
                return
            with open(self.ruta, "rb") as f:
                if self.pos == 0 and tam > COLA_BYTES:
                    f.seek(tam - COLA_BYTES)
                    f.readline()               # la primera línea queda partida
                else:
                    f.seek(self.pos)
                datos = f.read()
                self.pos = f.tell()
            lineas = (self.resto + datos).split(b"\n")
            self.resto = lineas.pop()          # lo último puede estar a medio escribir
            for ln in lineas:
                self._linea(ln)

    def _linea(self, ln):
        # las líneas con imágenes pesan MB: se descartan rápido las que no interesan
        if b'"customTitle"' in ln[:300]:
            try:
                self.titulo = json.loads(ln).get("customTitle") or self.titulo
            except ValueError:
                pass
            return
        if b'"type":"assistant"' not in ln and b'"type":"user"' not in ln:
            return
        try:
            d = json.loads(ln)
        except ValueError:
            return
        if d.get("type") not in ("assistant", "user") or d.get("isSidechain"):
            return
        t = _epoch(d.get("timestamp"))
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
            texto = _usuario_limpio(cont)
            if texto and not d.get("isMeta"):
                self._poner(dict(tipo="usuario", titulo="El usuario", detalle=_corto(tapar(texto), 400)), t)
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
            elif b.get("type") == "text" and not d.get("isMeta"):
                texto = _usuario_limpio(b.get("text"))
                if texto:
                    self._poner(dict(tipo="usuario", titulo="El usuario", detalle=_corto(tapar(texto), 400)), t)

    def _asistente(self, b, t):
        tipo = b.get("type")
        if tipo == "text":
            texto = (b.get("text") or "").strip()
            if texto:
                self._poner(dict(tipo="habla", titulo="Explica", detalle=_corto(tapar(texto), 420)), t)
        elif tipo == "thinking":
            self.pensando = True
        elif tipo == "tool_use":
            nombre, ent = b.get("name") or "", b.get("input")
            if nombre == "mcp__ccd_turn__update_plan":
                return self._plan(ent or {}, t)
            if nombre == "mcp__ccd_turn__wrap_up":
                return self._poner(dict(tipo="cierre", titulo="Cierra el tramo", detalle=_corto(tapar((ent or {}).get("recap") or ""), 320)), t)
            ev = _evento_herramienta(nombre, ent)
            if ev and ev["tipo"] == "navegador":      # los clics no traen dirección: siguen en el último sitio abierto
                self.host = ev.pop("host") or self.host
                ev["titulo"] = f"{ev.pop('verbo')} {self.host or 'el navegador'}"
                ev["estacion"] = "imagenes" if "labs.google" in self.host else "subida" if "studio.youtube" in self.host else None
            if ev:
                self._poner(ev, t)
                self.abiertos[b.get("id")] = ev
                if len(self.abiertos) > 200:
                    self.abiertos.pop(next(iter(self.abiertos)))

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

    def _poner(self, ev, t):
        self.seq += 1
        self.rev += 1
        ev.update(seq=self.seq, rev=self.rev, t=t)
        if ev.get("video"):
            self.conteo[ev["video"]] += 1
        if ev.get("estacion"):
            self.estacion = ev["estacion"]
        ev["en"] = self.estacion
        self.eventos.append(ev)

    @property
    def video(self):
        return self.conteo.most_common(1)[0][0] if self.conteo else None


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
            filas.append(dict(id=s.id, titulo=tapar(s.titulo)[:70], video=s.video, t=mt, activa=ahora - mt < ACTIVA_S, eventos=s.seq))
    filas.sort(key=lambda x: -x["t"])
    _LISTA.update(t=ahora, v=filas)
    _limpiar_cache()
    return filas


def eventos(sesion="", video="", desde=0):
    """{sesion, video, titulo, activa, pensando, plan, estacion, rev, eventos} con lo nuevo o cambiado desde la revisión `desde`.
    Sin sesión sigue la más reciente del video (o la más reciente con video): el corte a 180 mil abre otra y hay que pasar a ella."""
    if not sesion:
        lista = sesiones()
        elegida = next((x for x in lista if x["video"] == video), None) if video else None
        elegida = elegida or next((x for x in lista if x["video"] and not video), None) or (lista[0] if lista and not video else None)
        sesion = elegida["id"] if elegida else ""
    s = _sesion(sesion)
    if not s:
        return dict(sesion="", eventos=[], rev=0, plan=[], activa=False)
    try:
        mt = os.path.getmtime(s.ruta)
    except OSError:
        mt = 0
    # desde > rev: el panel se reinició y volvió a leer la sesión; se manda todo otra vez
    nuevos = [e for e in s.eventos if e["rev"] > desde] if 0 < desde <= s.rev else list(s.eventos)[-PRIMERA:]
    return dict(sesion=s.id, video=video or s.video, titulo=tapar(s.titulo)[:70], activa=time.time() - mt < ACTIVA_S,
                pensando=s.pensando, plan=s.plan, estacion=s.estacion, rev=s.rev, ultimo=s.ultimo_t, eventos=nuevos)


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
