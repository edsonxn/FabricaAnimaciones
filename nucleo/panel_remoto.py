# -*- coding: utf-8 -*-
"""Panel remoto (21-oct-2026): el lienzo del panel desde el celular, fuera de la red de casa.

Una «puerta» con clave delante del panel (que sigue en 127.0.0.1 y NUNCA se reinicia) + un túnel público (ngrok por
defecto; cloudflared si se pide). La puerta:
  - pide la clave UNA vez (enlace /entrar?k=… o formulario) y la guarda en una cookie de 30 días; sin ella, nada pasa;
  - reenvía todo al panel (con Range para adelantar videos) y comprime JSON/HTML/JS (el estado pesa 7× menos);
  - lleva la «Vista previa» del clásico a su trabajador (/_pv/<puerto>/…, solo puertos que el propio panel anunció).

    python fab.py panel --remoto                     levanta puerta + túnel (si no corren) e imprime el enlace con la clave
    python fab.py panel --remoto --tunel cloudflared  sin cuenta ni límite de datos (URL nueva cada vez)
    python fab.py panel --remoto --nueva-clave        cambia la clave (las cookies viejas dejan de valer)
    python fab.py panel --remoto --dominio clicknbusiness.com.mx/fabrica   dirección fija en el dominio que reenvía al
                                                    túnel de hoy (FTP de C:\CNB; se reescribe sola si cambia la URL)
    python fab.py panel --remoto estado | parar

Estudio Amaya (10-nov-2026): /amaya/… -> nucleo/amaya/servidor.py (127.0.0.1:8795, se lanza solo si no corre) con su
PROPIA llave (`clave_amaya`, cookie fab_amaya) que SOLO abre /amaya/ (la de papá también entra); en el dominio,
clicknbusiness.com.mx/amaya/ (página propia con ping y pantalla «la fábrica está dormida»).

App del teléfono (28-oct-2026): /m (o /movil) = panel de estatus, /juego = la fábrica en 3D; en el dominio,
clicknbusiness.com.mx/panel/, /juego/ y /vivo/ (carpetas hermanas de /fabrica/, mismo reenvío).

Config y clave: panel_remoto.json (raíz, fuera de git). Registro: panel_remoto.log y panel_remoto_tunel.log.
"""
import argparse
import gzip
import http.client
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CFG = os.path.join(RAIZ, "panel_remoto.json")
LOG = os.path.join(RAIZ, "panel_remoto.log")
LOG_TUNEL = os.path.join(RAIZ, "panel_remoto_tunel.log")
PUERTO = 8770
PANELES = (8765, 8766)                 # el primero que sirva /v2 (el de 8765 puede ser anterior al lienzo)
COOKIE = "fab_llave"
ATAJOS = {"/m": "/v2/movil", "/movil": "/v2/movil", "/juego": "/v2/aldea", "/aldea": "/v2/aldea", "/fabrica3d": "/v2/juego", "/vivo": "/v2/vivo"}
# sin clave: lo que el navegador pide sin cookie para instalar la app (manifest, iconos, service worker, three.js)
PUBLICO = re.compile(r"^/v2/app/[A-Za-z0-9_.-]+\.(png|webmanifest|js|json)$")
DOMINIO_EXTRAS = {"panel": "/m", "juego": "/juego", "vivo": "/v2/vivo",    # carpetas del dominio además de la principal -> ruta del túnel
                  "envivo": "/envivo/movil"}
AMAYA = 8795                           # Estudio Amaya (nucleo/amaya/servidor.py): /amaya/… con la llave de Amaya o la de papá
COOKIE_AMAYA = "fab_amaya"
AMAYA_PUBLICO = {"/ping.png", "/manifest.webmanifest", "/icono-192.png", "/icono-512.png", "/sw.js"}
AMAYA_LOG = os.path.join(RAIZ, "amaya_estudio", "servidor_salida.log")
ENVIVO = 8790                          # el directo (`fab.py envivo`): su control remoto va por /envivo/… con la misma clave
SALTO = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "transfer-encoding",
         "upgrade", "host", "content-length", "accept-encoding", "cookie", "server", "date"}
COMPRIMIBLE = ("text/", "application/json", "application/javascript", "image/svg+xml")
# DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW: que sigan vivos al cerrar la terminal o la sesión
DESACOPLADO = 0x00000008 | 0x00000200 | 0x08000000
FUERA_DEL_JOB = 0x01000000             # CREATE_BREAKAWAY_FROM_JOB (si el job lo permite)


def leer_cfg():
    try:
        with open(CFG, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def guardar_cfg(c):
    tmp = CFG + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=1)
    os.replace(tmp, CFG)


def log(*a):
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(str(x) for x in a) + "\n")
    except OSError:
        pass


# ======================================================================== la puerta
CLAVE = ""
CLAVE_AMAYA = ""
_AMAYA_ARRANQUE = threading.Lock()
PV_PUERTOS = set()                     # trabajadores de vista previa que el panel anunció en /api/preview
FALLOS = {}                            # ip -> [instantes de claves equivocadas]
_PANEL = {"p": None, "t": 0.0}


def panel_puerto(forzar=False):
    """Puerto del panel que sirve el lienzo (se revisa cada minuto o si falla la conexión)."""
    if not forzar and _PANEL["p"] and time.time() - _PANEL["t"] < 60:
        return _PANEL["p"]
    for p in PANELES:
        try:
            c = http.client.HTTPConnection("127.0.0.1", p, timeout=4)
            c.request("GET", "/api/v2/sistema")
            if c.getresponse().status == 200:
                _PANEL.update(p=p, t=time.time())
                return p
        except OSError:
            pass
    _PANEL.update(p=_PANEL["p"] or PANELES[0], t=time.time())
    return _PANEL["p"]


def amaya_despierta(esperar=10.0):
    """Si el Estudio Amaya no escucha en 8795, lo lanza desacoplado (una sola vez a la vez) y espera hasta `esperar` s."""
    if escucha(AMAYA):
        return True
    with _AMAYA_ARRANQUE:
        if escucha(AMAYA):
            return True
        os.makedirs(os.path.dirname(AMAYA_LOG), exist_ok=True)
        log("lanzo el Estudio Amaya")
        lanzar([sys.executable, os.path.join(AQUI, "amaya", "servidor.py")], AMAYA_LOG)
        fin = time.time() + esperar
        while time.time() < fin:
            time.sleep(0.4)
            if escucha(AMAYA):
                return True
    return escucha(AMAYA)


PING_PNG = bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000"
                         "1f15c4890000000d49444154789c6360000002000154a24f5d0000000049454e44ae426082")


PAGINA_ENTRAR = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#0b0d13">
<title>Fábrica · entrar</title><style>
body{margin:0;min-height:100dvh;display:grid;place-items:center;background:#0b0d13;color:#e9ebf3;font:16px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif}
form{box-sizing:border-box;width:min(360px,calc(100vw - 40px));background:#151821;border:1px solid #272c39;border-radius:18px;padding:26px 22px;box-shadow:0 26px 64px rgba(0,0,0,.6)}
.logo{width:40px;height:40px;border-radius:12px;background:conic-gradient(from 210deg,#8b74ff,#ff5fa8,#ffb35c,#47d1a8,#8b74ff);box-shadow:inset 0 0 0 7px #151821;margin-bottom:14px}
h1{font-size:19px;margin:0 0 4px}p{color:#8d93a8;font-size:14px;margin:0 0 18px}
input{width:100%;box-sizing:border-box;height:48px;border-radius:12px;border:1px solid #363c4d;background:#1c202b;color:#e9ebf3;font:inherit;padding:0 14px}
button{margin-top:12px;width:100%;height:48px;border:0;border-radius:12px;background:#8b74ff;color:#fff;font:inherit;font-weight:650}
.err{color:#ff6b81;font-size:14px;margin:10px 0 0}</style></head><body>
<form method="post" action="/entrar"><div class="logo"></div><h1>Fábrica de Animaciones</h1><p>Panel remoto. Escribe la clave (o abre el enlace que te mandó Claude).</p>
<input name="k" type="password" autocomplete="current-password" placeholder="Clave" autofocus><input type="hidden" name="ir" value="{ir}">
<button>Entrar</button>{err}</form></body></html>"""


class Puerta(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _ip(self):
        return (self.headers.get("X-Forwarded-For") or self.client_address[0]).split(",")[0].strip()

    def _https(self):
        return self.headers.get("X-Forwarded-Proto", "").lower() == "https"

    def _enviar(self, codigo, cuerpo, tipo, extra=()):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        for k, v in extra:
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(cuerpo)

    def _con_llave(self):
        c = SimpleCookie()
        try:
            c.load(self.headers.get("Cookie") or "")
        except Exception:
            return False
        m = c.get(COOKIE)
        return bool(m and CLAVE and secrets.compare_digest(m.value.encode(), CLAVE.encode()))

    def _con_llave_amaya(self):
        if self._con_llave():
            return True
        c = SimpleCookie()
        try:
            c.load(self.headers.get("Cookie") or "")
        except Exception:
            return False
        m = c.get(COOKIE_AMAYA)
        return bool(m and CLAVE_AMAYA and secrets.compare_digest(m.value.encode(), CLAVE_AMAYA.encode()))

    def _pagina_entrar(self, codigo=401, err="", ir="/v2"):
        if ir.startswith("/amaya"):
            html = PAGINA_ENTRAR.replace("#8b74ff", "#ff5fa8").replace("#0b0d13", "#1a1033").replace("#151821", "#2a1650")                 .replace("#272c39", "#4a2f7d").replace("#1c202b", "#22123f").replace("#363c4d", "#5b3f8f").replace("<h1>Fábrica de Animaciones</h1>", "<h1>Estudio Amaya ✨</h1>") \
                .replace("Panel remoto. Escribe la clave (o abre el enlace que te mandó Claude).",
                         "Abre la app «Estudio Amaya» que te dio papá, o escribe tu clave.") \
                .replace("<title>Fábrica · entrar</title>", "<title>Estudio Amaya</title>")
            html = html.replace("{ir}", "/amaya/").replace("{err}", f'<p class="err">{err}</p>' if err else "")
            return self._enviar(codigo, html.encode("utf-8"), "text/html; charset=utf-8")
        html = PAGINA_ENTRAR.replace("{ir}", ir.replace('"', "")).replace("{err}", f'<p class="err">{err}</p>' if err else "")
        self._enviar(codigo, html.encode("utf-8"), "text/html; charset=utf-8")

    def _entrar(self, k, ir):
        ip, ahora = self._ip(), time.time()
        recientes = [t for t in FALLOS.get(ip, []) if ahora - t < 600]
        if len(recientes) >= 8:
            log("bloqueado", ip)
            return self._pagina_entrar(429, "Demasiados intentos. Espera 10 minutos.")
        if k and CLAVE_AMAYA and secrets.compare_digest(k.encode(), CLAVE_AMAYA.encode()):   # solo abre su estudio
            FALLOS.pop(ip, None)
            log("entró Amaya", ip, self.headers.get("User-Agent", "")[:80])
            self.send_response(303)
            self.send_header("Location", "/amaya/")
            self.send_header("Set-Cookie", f"{COOKIE_AMAYA}={CLAVE_AMAYA}; Max-Age=31536000; Path=/amaya; HttpOnly; SameSite=Lax"
                             + ("; Secure" if self._https() else ""))
            self.send_header("Content-Length", "0")
            return self.end_headers()
        if not (k and CLAVE and secrets.compare_digest(k.encode(), CLAVE.encode())):
            FALLOS[ip] = recientes + [ahora]
            log("clave equivocada", ip)
            return self._pagina_entrar(401, "Clave equivocada." if k else "", ir)
        FALLOS.pop(ip, None)
        if not ir.startswith("/") or ir.startswith("//"):
            ir = "/v2"
        cookie = f"{COOKIE}={CLAVE}; Max-Age=2592000; Path=/; HttpOnly; SameSite=Lax" + ("; Secure" if self._https() else "")
        log("entró", ip, self.headers.get("User-Agent", "")[:80])
        self.send_response(303)
        self.send_header("Location", ir)
        self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _atender(self):
        u = urlparse(self.path)
        ruta = u.path
        if ruta == "/_puerta/salud":
            return self._enviar(200, b'{"app":"fab-puerta"}', "application/json")
        if ruta == "/entrar":
            if self.command == "POST":
                n = int(self.headers.get("Content-Length") or 0)
                f = parse_qs(self.rfile.read(min(n, 4096)).decode("utf-8", "replace"))
            else:
                f = parse_qs(u.query)
            return self._entrar((f.get("k") or [""])[0].strip(), (f.get("ir") or ["/v2"])[0])
        if ruta == "/salir":
            self.send_response(303)
            self.send_header("Location", "/entrar")
            self.send_header("Set-Cookie", f"{COOKIE}=; Max-Age=0; Path=/")
            self.send_header("Content-Length", "0")
            return self.end_headers()
        if ruta == "/amaya":
            self.send_response(301)
            self.send_header("Location", "/amaya/" + (f"?{u.query}" if u.query else ""))
            self.send_header("Content-Length", "0")
            return self.end_headers()
        if ruta.startswith("/amaya/"):
            return self._amaya(ruta[len("/amaya"):], u.query)
        if PUBLICO.match(ruta) and self.command in ("GET", "HEAD"):
            return self._reenviar(panel_puerto(), self.path)
        if ruta.rstrip("/") in ATAJOS and self._con_llave():
            return self._reenviar(panel_puerto(), ATAJOS[ruta.rstrip("/")] + (f"?{u.query}" if u.query else ""))
        if not self._con_llave():
            if ruta.startswith(("/api/", "/v2/", "/_pv/", "/video/", "/media/", "/montaje/", "/audio/", "/envivo/")) or self.command != "GET":
                return self._enviar(401, b'{"error":"sin clave: abre /entrar"}', "application/json")
            return self._pagina_entrar(ir=self.path if ruta not in ("/", "/entrar") else "/v2")
        if ruta == "/envivo" or ruta.startswith("/envivo/"):     # control remoto del EN VIVO (nucleo/envivo/movil.html)
            resto = ruta[len("/envivo"):]
            if resto in ("", "/"):
                resto = "/movil"
            return self._reenviar(ENVIVO, resto + (f"?{u.query}" if u.query else ""))
        m = re.match(r"^/_pv/(\d{2,5})(/.*)$", ruta)
        if m:
            p = int(m.group(1))
            if p not in PV_PUERTOS:
                return self._enviar(404, b"trabajador desconocido", "text/plain")
            return self._reenviar(p, m.group(2) + (f"?{u.query}" if u.query else ""))
        if ruta == "/":                              # el celular entra directo al lienzo; el clásico sigue en /?clasico
            if not u.query:
                self.send_response(302)
                self.send_header("Location", "/v2")
                self.send_header("Content-Length", "0")
                return self.end_headers()
            if u.query == "clasico":
                return self._reenviar(panel_puerto(), "/")
        return self._reenviar(panel_puerto(), self.path)

    def _amaya(self, resto, query):
        """Estudio Amaya: /amaya/<resto> -> 127.0.0.1:8795/<resto>. El ping lo contesta la puerta (y despierta el estudio)."""
        if resto == "/ping.png" and self.command in ("GET", "HEAD"):
            threading.Thread(target=amaya_despierta, daemon=True).start()
            return self._enviar(200, PING_PNG, "image/png", [("Access-Control-Allow-Origin", "*")])
        if not (resto in AMAYA_PUBLICO and self.command in ("GET", "HEAD")) and not self._con_llave_amaya():
            if resto.startswith("/api/") or self.command != "GET":
                return self._enviar(401, b'{"error":"sin llave: abre la app Estudio Amaya"}', "application/json")
            return self._pagina_entrar(ir="/amaya/")
        if not amaya_despierta():
            return self._enviar(503, "El Estudio Amaya no arrancó. En la PC: python fab.py amaya".encode("utf-8"),
                                "text/plain; charset=utf-8")
        return self._reenviar(AMAYA, resto + (f"?{query}" if query else ""))

    def _reenviar(self, puerto, ruta, reintento=True):
        cuerpo = None
        if self.command == "POST":
            if not hasattr(self, "_cuerpo_leido"):           # se lee una vez: un reintento reusa el mismo cuerpo
                n = int(self.headers.get("Content-Length") or 0)
                self._cuerpo_leido = self.rfile.read(n) if n else b""
            cuerpo = self._cuerpo_leido
        cab = {k: v for k, v in self.headers.items() if k.lower() not in SALTO}
        cab["Host"] = f"127.0.0.1:{puerto}"
        try:
            c = http.client.HTTPConnection("127.0.0.1", puerto, timeout=600)
            c.request(self.command, ruta, body=cuerpo, headers=cab)
            r = c.getresponse()
        except ConnectionRefusedError:
            if puerto == AMAYA:
                if reintento and amaya_despierta():
                    return self._reenviar(AMAYA, ruta, False)
                return self._enviar(503, "El Estudio Amaya está dormido. En la PC: python fab.py amaya".encode("utf-8"),
                                    "text/plain; charset=utf-8")
            if puerto == ENVIVO:
                return self._enviar(502, "El directo no está corriendo. En la PC: python fab.py envivo".encode("utf-8"), "text/plain; charset=utf-8")
            if reintento and puerto in PANELES:
                return self._reenviar(panel_puerto(forzar=True), ruta, False) if cuerpo is None else \
                    self._enviar(502, "El panel no responde (¿se cerró?). En la PC: python fab.py panel".encode("utf-8"), "text/plain; charset=utf-8")
            return self._enviar(502, "El panel no responde (¿se cerró?). En la PC: python fab.py panel".encode("utf-8"), "text/plain; charset=utf-8")
        except OSError as e:
            return self._enviar(504, f"El panel tardó demasiado: {e}".encode("utf-8"), "text/plain; charset=utf-8")
        tipo = (r.getheader("Content-Type") or "").lower()
        largo = int(r.getheader("Content-Length") or -1)
        gz = "gzip" in (self.headers.get("Accept-Encoding") or "") and r.status == 200 and tipo.startswith(COMPRIMIBLE) \
            and not r.getheader("Content-Encoding") and 600 < largo < 30_000_000
        if gz or ruta.startswith("/api/preview"):
            datos = r.read()
            if ruta.startswith("/api/preview"):
                try:
                    pv = json.loads(datos)
                    if pv.get("puerto"):
                        PV_PUERTOS.add(int(pv["puerto"]))
                except (ValueError, TypeError, AttributeError):
                    pass
            if gz:
                datos = gzip.compress(datos, 5)
            self.send_response(r.status, r.reason)
            for k, v in r.getheaders():
                if k.lower() not in SALTO:
                    self.send_header(k, v)
            if gz:
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Vary", "Accept-Encoding")
            self.send_header("Content-Length", str(len(datos)))
            self.end_headers()
            self.wfile.write(datos)
            return
        self.send_response(r.status, r.reason)
        for k, v in r.getheaders():
            if k.lower() not in SALTO:
                self.send_header(k, v)
        if largo >= 0:
            self.send_header("Content-Length", str(largo))
        self.end_headers()
        while True:
            trozo = r.read(256 * 1024)
            if not trozo:
                break
            self.wfile.write(trozo)

    def _seguro(self):
        try:
            self._atender()
        except (ConnectionError, socket.timeout):
            pass
        except Exception as e:
            log("error", self.command, self.path, repr(e))
            try:
                self._enviar(500, str(e).encode("utf-8", "replace"), "text/plain; charset=utf-8")
            except OSError:
                pass

    def do_OPTIONS(self):                    # preflight del ping del dominio (lleva ngrok-skip-browser-warning)
        if urlparse(self.path).path == "/amaya/ping.png":
            return self._enviar(204, b"", "text/plain", [("Access-Control-Allow-Origin", "*"),
                                                         ("Access-Control-Allow-Methods", "GET"),
                                                         ("Access-Control-Allow-Headers", "ngrok-skip-browser-warning"),
                                                         ("Access-Control-Max-Age", "600")])
        self._enviar(405, b"", "text/plain")

    do_GET = do_POST = do_HEAD = _seguro


def servir(puerto):
    global CLAVE, CLAVE_AMAYA
    c = leer_cfg()
    if c.get("clave") and not c.get("clave_amaya"):
        c["clave_amaya"] = secrets.token_urlsafe(18)
        guardar_cfg(c)
    CLAVE = c.get("clave", "")
    CLAVE_AMAYA = c.get("clave_amaya", "")
    if not CLAVE:
        sys.exit("sin clave en panel_remoto.json")
    ThreadingHTTPServer.request_queue_size = 128
    ThreadingHTTPServer.daemon_threads = True
    srv = ThreadingHTTPServer(("127.0.0.1", puerto), Puerta)
    log(f"puerta en 127.0.0.1:{puerto} -> panel {panel_puerto()}")
    srv.serve_forever()


# ======================================================================== arrancar / parar
def escucha(puerto):
    try:
        with socket.create_connection(("127.0.0.1", puerto), timeout=1.5):
            return True
    except OSError:
        return False


def _tiene_lienzo(puerto):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{puerto}/api/v2/sistema", timeout=4) as r:
            return r.status == 200
    except (OSError, ValueError):
        return False


def es_puerta(puerto):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{puerto}/_puerta/salud", timeout=3) as r:
            return json.loads(r.read()).get("app") == "fab-puerta"
    except (OSError, ValueError):
        return False


def lanzar(cmd, salida):
    f = open(salida, "ab")
    try:
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=RAIZ,
                             creationflags=DESACOPLADO | FUERA_DEL_JOB, close_fds=True)
    except OSError:                                  # el job no deja salir: igual queda desacoplado
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=RAIZ,
                             creationflags=DESACOPLADO, close_fds=True)
    return p.pid


def vivo(pid, palabra):
    if not pid:
        return False
    try:
        import psutil
        pr = psutil.Process(pid)
        return palabra.lower() in " ".join(pr.cmdline()).lower()
    except Exception:
        return False


def binario(nombre, extra):
    for c in (shutil.which(nombre), *extra):
        if c and os.path.isfile(c):
            return c
    return None


def responde(url):
    """¿La URL pública llega a la puerta? (desde la propia PC, ida y vuelta por el túnel)"""
    try:
        q = urllib.request.Request(url.rstrip("/") + "/_puerta/salud", headers={"ngrok-skip-browser-warning": "1", "User-Agent": "fab-puerta"})
        with urllib.request.urlopen(q, timeout=12) as r:
            return json.loads(r.read()).get("app") == "fab-puerta"
    except (OSError, ValueError):
        return False


def abrir_tunel(tunel, puerto):
    open(LOG_TUNEL, "w").close()
    if tunel == "ngrok":
        exe = binario("ngrok", [r"C:\ngrok\ngrok.exe"])
        if not exe:
            sys.exit("No encuentro ngrok. Prueba con --tunel cloudflared.")
        pid = lanzar([exe, "http", f"127.0.0.1:{puerto}", "--log", "stdout", "--log-format", "logfmt"], LOG_TUNEL)
        patron = r'url=(https://[^\s"]+)'
    else:
        exe = binario("cloudflared", [r"C:\Program Files (x86)\cloudflared\cloudflared.exe", r"C:\Program Files\cloudflared\cloudflared.exe"])
        if not exe:
            sys.exit("No encuentro cloudflared.")
        pid = lanzar([exe, "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{puerto}"], LOG_TUNEL)
        patron = r"(https://[a-z0-9-]+\.trycloudflare\.com)"
    for _ in range(60):
        time.sleep(0.5)
        txt = open(LOG_TUNEL, encoding="utf-8", errors="replace").read()
        m = re.search(patron, txt)
        if m:
            return pid, m.group(1)
        e = re.search(r"(ERR_NGROK_\d+[^\n]*)", txt)
        if e or not vivo(pid, tunel):
            sys.exit(f"El túnel {tunel} no arrancó: {(e.group(1) if e else txt[-600:]).strip()}\n"
                     f"Registro: {LOG_TUNEL}" + ("\nAlternativa: python fab.py panel --remoto --tunel cloudflared" if tunel == "ngrok" else ""))
    sys.exit(f"El túnel {tunel} no dio URL en 30 s. Registro: {LOG_TUNEL}")


def iniciar(a):
    c = leer_cfg()
    if a.nueva_clave or not c.get("clave"):
        parar_pid(c.pop("puerta_pid", None))        # la puerta lee la clave al arrancar: hay que relanzarla
        c["clave"] = secrets.token_urlsafe(18)
    if not c.get("clave_amaya"):                    # llave de Amaya: solo abre /amaya/
        parar_pid(c.pop("puerta_pid", None))
        c["clave_amaya"] = secrets.token_urlsafe(18)
    puerto = a.puerto or c.get("puerto") or PUERTO
    c["puerto"] = puerto
    guardar_cfg(c)
    pp = panel_puerto(forzar=True)
    if not escucha(pp):
        print(f"El panel no está corriendo: lo lanzo (python fab.py panel --puerto {PANELES[0]})")
        lanzar([sys.executable, os.path.join(RAIZ, "fab.py"), "panel", "--puerto", str(PANELES[0])], os.path.join(RAIZ, "panel_salida.log"))
        for _ in range(40):
            time.sleep(0.5)
            if escucha(PANELES[0]):
                break
        pp = panel_puerto(forzar=True)
    if not _tiene_lienzo(pp):
        print(f"Ojo: el panel de 127.0.0.1:{pp} no tiene el lienzo (/v2): es anterior al 21-oct. Hay que reiniciarlo una vez.")
    # 1) la puerta
    if not es_puerta(puerto):
        if escucha(puerto):
            sys.exit(f"El puerto {puerto} lo usa otro programa: usa --puerto <otro>.")
        c["puerta_pid"] = lanzar([sys.executable, os.path.abspath(__file__), "servir", "--puerto", str(puerto)], LOG)
        for _ in range(30):
            time.sleep(0.3)
            if es_puerta(puerto):
                break
        else:
            sys.exit(f"La puerta no arrancó. Registro: {LOG}")
    # 2) el túnel (se reutiliza si sigue vivo y responde)
    tunel = a.tunel or c.get("tunel") or "ngrok"
    if a.tunel and a.tunel != c.get("tunel"):
        parar_pid(c.get("tunel_pid"))
        c.pop("url", None)
    if not (c.get("url") and vivo(c.get("tunel_pid"), tunel) and responde(c["url"])):
        parar_pid(c.get("tunel_pid"))
        c["tunel_pid"], c["url"] = abrir_tunel(tunel, puerto)
    c["tunel"] = tunel
    if a.dominio:
        dom = a.dominio.strip().rstrip("/").replace("https://", "").replace("http://", "")
        host, _, carpeta = dom.partition("/")
        if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", host, re.I) or not re.match(r"^[A-Za-z0-9_-]+$", carpeta or ""):
            sys.exit("--dominio va como dominio/carpeta, p. ej. clicknbusiness.com.mx/fabrica")
        c["dominio"] = dict(url=f"https://{host}/{carpeta}/", carpeta=carpeta, cnb=(c.get("dominio") or {}).get("cnb", r"C:\CNB"))
    if a.sin_dominio:
        c.pop("dominio", None)
    guardar_cfg(c)
    ok = any(responde(c["url"]) or time.sleep(2) for _ in range(4))   # el dominio nuevo tarda unos segundos en resolverse
    enlace = f"{c['url']}/entrar?k={quote(c['clave'])}"
    print(f"Panel remoto {'listo' if ok else 'levantado (la comprobación de ida y vuelta falló; prueba el enlace)'}"
          f" · túnel {tunel} · panel en 127.0.0.1:{pp}")
    if c.get("dominio") and publicar_dominio(c, forzar=bool(a.dominio) or a.republicar):
        d = c["dominio"]
        raiz = d["url"].rsplit("/", 2)[0]
        print(f"  Dirección fija (siempre lleva al túnel de hoy): {d['url']}")
        print(f"  En el teléfono: panel {raiz}/panel/  ·  juego {raiz}/juego/")
        print(f"  Primera vez en un celular (guarda la clave en ESE celular, nunca en el servidor): {d['url']}#k={quote(c['clave'])}")
    print(f"  Enlace directo con la clave (luego basta {c['url']}/v2):")
    print(f"  {enlace}")
    if tunel == "ngrok":
        print("  ngrok gratis muestra un aviso «You are about to visit…» con cada URL nueva: toca «Visit Site».")


# ======================================================================== dirección fija en el dominio (clicknbusiness.com.mx)
# La URL de ngrok gratis cambia cada vez que se reinicia; el hosting del dominio (HostGator compartido, solo FTP) no puede
# correr el panel, pero sí una página que reenvía al túnel de hoy. La clave NUNCA va al servidor: el primer enlace la lleva en
# el «#» (no viaja en la petición) y la página la guarda en el celular (localStorage) para entrar sola las veces siguientes.
MARCA = "fab_puerta.txt"
PAGINA_DOMINIO = """<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><title>Fábrica</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0b0d13;color:#8d93a8;font:15px system-ui,sans-serif}</style>
</head><body><p>Abriendo la Fábrica…</p><script>
const T=%s;let k="";
try{const h=new URLSearchParams(location.hash.slice(1));if(h.has("olvidar"))localStorage.removeItem("fab_k");else if(h.get("k"))localStorage.setItem("fab_k",h.get("k"));k=localStorage.getItem("fab_k")||"";}catch(e){}
history.replaceState(null,"",location.pathname);
const D=%s;location.replace(k?T+"/entrar?k="+encodeURIComponent(k)+"&ir="+encodeURIComponent(D):T+D);
</script><noscript><a href=%s>Abrir la Fábrica</a></noscript></body></html>
"""
HTACCESS_DOMINIO = """AddType application/vnd.android.package-archive .apk
<IfModule mod_headers.c>
Header set Cache-Control "no-store"
Header set X-Robots-Tag "noindex, nofollow"
</IfModule>
"""
# corre dentro de C:\\CNB con su propio módulo FTP (lee sus credenciales de su .env; aquí nunca se ven)
SUBIR_FTP = r'''
import sys
from pathlib import Path
from cnb import ftp as F
local, carpeta, marca = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
f = F.conectar()
try:
    hay = {n.rsplit("/", 1)[-1].lower() for n, d, _ in F.listar(f, ".")}
    if carpeta.lower() in hay and marca.lower() not in {n.rsplit("/", 1)[-1].lower() for n, _, _ in F.listar(f, carpeta)}:
        sys.exit(f"la carpeta {carpeta}/ ya existe en el servidor y no es de la Fábrica: no la toco")
    print("subidos", F.subir_carpeta(f, local, carpeta, log=lambda *a, **k: None))
finally:
    try:
        f.quit()
    except Exception:
        pass
'''


PAGINA_AMAYA = """<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#1a1033"><title>Estudio Amaya</title><style>
*{box-sizing:border-box}body{margin:0;min-height:100dvh;display:grid;place-items:center;background:radial-gradient(120% 80% at 50% 0%,#3a1d6e,#1a1033 60%);
color:#fff;font:17px/1.45 system-ui,-apple-system,"Segoe UI",sans-serif;text-align:center;padding:24px}
.c{width:min(360px,100%)}.e{font-size:72px;line-height:1;margin-bottom:10px;animation:f 3s ease-in-out infinite}
@keyframes f{50%{transform:translateY(-8px) rotate(-4deg)}}h1{font-size:24px;margin:6px 0}p{color:#d7c9ff;margin:6px 0 20px}
button{width:100%;height:52px;border:0;border-radius:16px;background:linear-gradient(90deg,#ff5fa8,#ffb35c);color:#2a0f3d;font:inherit;font-weight:800}
small{display:block;margin-top:16px;color:#a996e0;font-size:13px}#z{display:none}.pt{display:inline-block;animation:p 1.2s infinite}
@keyframes p{50%{opacity:.25}}</style></head><body><div class="c">
<div id="a"><div class="e">✨</div><h1>Estudio Amaya</h1><p>Abriendo tu estudio<span class="pt">…</span></p></div>
<div id="z"><div class="e">😴</div><h1>La fábrica está dormida</h1><p>La computadora de papá está apagada o descansando.<br>Pídele a papá que la despierte 💜</p>
<button onclick="probar()">Reintentar</button><small>Hecha con cariño por papá Edson</small></div></div><script>
const T=__T__;let k="";
try{const h=new URLSearchParams(location.hash.slice(1));if(h.has("olvidar"))localStorage.removeItem("amaya_k");else if(h.get("k"))localStorage.setItem("amaya_k",h.get("k"));k=localStorage.getItem("amaya_k")||"";}catch(e){}
history.replaceState(null,"",location.pathname);
function entrar(){location.replace(k?T+"/entrar?k="+encodeURIComponent(k)+"&ir=%2Famaya%2F":T+"/amaya/");}
function dormida(){document.getElementById("a").style.display="none";document.getElementById("z").style.display="block";}
function probar(){document.getElementById("z").style.display="none";document.getElementById("a").style.display="block";
 const c=new AbortController();const t=setTimeout(()=>c.abort(),12000);
 fetch(T+"/amaya/ping.png?t="+Date.now(),{headers:{"ngrok-skip-browser-warning":"1"},signal:c.signal,cache:"no-store"})
  .then(r=>{clearTimeout(t);(r.ok&&(r.headers.get("content-type")||"").startsWith("image/"))?entrar():dormida();})
  .catch(()=>{clearTimeout(t);dormida();});}
probar();
</script></body></html>
"""


def publicar_dominio(c, forzar=False):
    """Sube <dominio>/<carpeta>/ (index.html que reenvía al túnel de hoy) si la URL del túnel cambió. Solo esa carpeta."""
    d = c.get("dominio")
    if not d or not c.get("url") or (d.get("publicado") == c["url"] and not forzar):
        return True
    for carpeta, destino in [(d["carpeta"], "/v2")] + sorted(DOMINIO_EXTRAS.items()) + [("amaya", None)]:
        tmp = os.path.join(tempfile.gettempdir(), "fab_panel_remoto_dominio", carpeta)
        os.makedirs(tmp, exist_ok=True)
        u = json.dumps(c["url"])
        with open(os.path.join(tmp, "index.html"), "w", encoding="utf-8") as f:
            f.write(PAGINA_AMAYA.replace("__T__", u) if destino is None else PAGINA_DOMINIO % (u, json.dumps(destino), json.dumps(c["url"] + destino)))
        with open(os.path.join(tmp, ".htaccess"), "w", encoding="utf-8", newline="\n") as f:
            f.write(HTACCESS_DOMINIO)
        apk = os.path.join(AQUI, "app_movil", "fabrica.apk")
        if carpeta == "panel" and os.path.isfile(apk):          # la app Android se baja de aquí sin clave (no lleva secretos)
            shutil.copy2(apk, os.path.join(tmp, "fabrica.apk"))
        with open(os.path.join(tmp, MARCA), "w", encoding="utf-8") as f:
            f.write("Reenvío al panel remoto de la Fábrica de Animaciones (C:\\FabricaAnimaciones\\nucleo\\panel_remoto.py).\n"
                    "Lo reescribe `python fab.py panel --remoto` cada vez que cambia la URL del túnel. Sin claves.\n")
        r = subprocess.run([sys.executable, "-c", SUBIR_FTP, tmp, carpeta, MARCA], cwd=d.get("cnb", r"C:\CNB"),
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        if r.returncode != 0:
            print(f"  No pude actualizar {d['url'].rsplit('/', 2)[0]}/{carpeta}/: {(r.stderr or r.stdout).strip().splitlines()[-1:]}")
            return False
    d["publicado"] = c["url"]
    guardar_cfg(c)
    log("dominio", d["url"], "->", c["url"])
    return True


def parar_pid(pid):
    if pid and (vivo(pid, "ngrok") or vivo(pid, "cloudflared") or vivo(pid, "panel_remoto")):
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)


def parar():
    c = leer_cfg()
    parar_pid(c.get("tunel_pid"))
    parar_pid(c.get("puerta_pid"))
    for k in ("tunel_pid", "puerta_pid", "url"):
        c.pop(k, None)
    guardar_cfg(c)
    print("Panel remoto cerrado (puerta y túnel). El panel local sigue igual.")


def estado():
    c = leer_cfg()
    p = c.get("puerto") or PUERTO
    print(f"puerta 127.0.0.1:{p}: {'sí' if es_puerta(p) else 'no'} · túnel {c.get('tunel', '-')}: "
          f"{'vivo' if vivo(c.get('tunel_pid'), c.get('tunel', 'ngrok')) else 'no'} · URL: {c.get('url', '-')}")
    if c.get("url"):
        print(f"responde desde fuera: {'sí' if responde(c['url']) else 'no'}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Panel remoto: puerta con clave + túnel público")
    ap.add_argument("accion", nargs="?", default="iniciar", choices=["iniciar", "servir", "parar", "estado"])
    ap.add_argument("--puerto", type=int, default=0, help=f"puerto local de la puerta (por defecto {PUERTO})")
    ap.add_argument("--tunel", choices=["ngrok", "cloudflared"])
    ap.add_argument("--nueva-clave", action="store_true")
    ap.add_argument("--dominio", help="dirección fija dominio/carpeta que reenvía al túnel (p. ej. clicknbusiness.com.mx/fabrica; FTP de C:\\CNB)")
    ap.add_argument("--sin-dominio", action="store_true", help="deja de actualizar la dirección fija")
    ap.add_argument("--republicar", action="store_true", help="vuelve a subir las páginas del dominio aunque la URL no cambió")
    a = ap.parse_args()
    if a.accion == "servir":
        servir(a.puerto or leer_cfg().get("puerto") or PUERTO)
    elif a.accion == "parar":
        parar()
    elif a.accion == "estado":
        estado()
    else:
        iniciar(a)


if __name__ == "__main__":
    main()
