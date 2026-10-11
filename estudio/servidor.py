# -*- coding: utf-8 -*-
"""ESTUDIO de la Fábrica de Animaciones: interfaz sencilla (versión comercial) para crear videos animados de hasta
60 segundos sin conocer el pipeline: idea -> guion (Gemini o a mano) -> estilo, voz y música -> video.

    python fab.py estudio [--puerto 8790] [--abrir]   ->  http://127.0.0.1:8790

Proyectos en estudio/proyectos/<id>/ (cada uno es un video normal de la Fábrica: guion.py + escenas.py), voces
clonadas en estudio/voces/, estilos personales en estudio/estilos.json y la API key de Gemini en estudio/ajustes.json
(nada de eso se sube a git)."""
import argparse
import glob
import json
import mimetypes
import os
import re
import shutil
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import cerebro_gemini as G  # noqa: E402
import agente_tomas as AG  # noqa: E402
import estilos_estudio as EST  # noqa: E402
import proyecto as P  # noqa: E402
import trabajos as T  # noqa: E402
import vistas as V  # noqa: E402

HTML = os.path.join(AQUI, "estudio.html")
AJUSTES = os.path.join(AQUI, "ajustes.json")
VOCES = os.path.join(AQUI, "voces")
ICONOS_DIR = os.path.join(AQUI, "iconos")
PORTADAS = os.path.join(AQUI, "portadas")                # portada de cada estilo (un cuadro real dibujado con él)
SISTEMA = os.path.join(P.PROYECTOS, "_sistema")          # proyecto interno para miniaturas y muestras de estilo
BIBLIOTECA_VOCES = r"C:\chatterbox_voices"
VOCES_VISIBLES = {"dan", "faraon", "antonio", "charon", "gaia"}   # únicas voces de la biblioteca que muestra el Estudio
NO_COMERCIALES = {"mascara"}                             # dibujos con personajes con derechos de autor
TEXTO_PRUEBA_VOZ = "Hola, esta es mi voz en la Fábrica de Animaciones. ¿Qué te parece cómo suena?"

MUESTRA_GUION = dict(titulo="Así se ve tu estilo", formato="horizontal", musica="auto", escenas=[
    dict(frases=["Este es un video de muestra para ver tu estilo."], icono="cerebro"),
    dict(titulo="Ideas", frases=["Cada parte tiene sus dibujos y etiquetas.", "Y todo se mueve con la voz."],
         icono="sol", icono2="ciudad", claves=[["dibujos", "DIBUJOS"]]),
    dict(titulo="Datos", frases=["Las cifras aparecen en grande cuando las dices, como cien."], icono="reloj",
         cifra="100", cifra_palabra="cien"),
    dict(frases=["Y así termina."], icono="estrella"),
], cierre="¡Listo!")


# ------------------------------------------------------------------ ajustes
# La API key de Gemini y el modelo NO viven en el servidor: cada navegador los guarda en su localStorage y los manda en
# cada petición (cabeceras X-Gemini-Key / X-Gemini-Model). Así varias personas pueden usar el mismo Estudio (p. ej. por un
# túnel) cada una con su propia key. En ajustes.json solo queda lo del equipo (procs); cualquier "clave" vieja se ignora.
_PET = threading.local()


def ajustes():
    try:
        with open(AJUSTES, encoding="utf-8") as f:
            a = json.load(f)
    except Exception:
        a = {}
    a.pop("clave", None)                                   # nunca se usa la key guardada en disco
    modelo = (getattr(_PET, "modelo", "") or a.get("modelo") or "").strip()
    if not modelo or modelo.startswith(G.VIEJOS):
        modelo = G.DEFECTO
    a["modelo"] = modelo
    a["clave"] = getattr(_PET, "clave", "") or ""          # la de ESTA petición (navegador)
    a.setdefault("procs", 12)
    return a


def guardar_ajustes(a):
    a = {k: v for k, v in a.items() if k not in ("clave", "modelo")}   # la key y el modelo son del navegador
    tmp = AJUSTES + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(a, f, ensure_ascii=False, indent=1)
    os.replace(tmp, AJUSTES)


def ajustes_publicos():
    a = ajustes()
    clave = a.get("clave", "")
    return dict(modelo=a["modelo"], procs=a["procs"], tiene_clave=bool(clave), sugeridos=G.SUGERIDOS,
                clave_oculta=("•" * 8 + clave[-4:]) if clave else "")


# ------------------------------------------------------------------ catálogos
def iconos():
    import ast
    src = open(os.path.join(T.NUCLEO, "escena_base.py"), encoding="utf-8").read()
    m = re.search(r"^ICONOS = \{(.*?)^\}", src, re.M | re.S)
    nombres = re.findall(r'^\s+"([a-z_0-9]+)":', m.group(1), re.M) if m else []
    return [n for n in nombres if n not in NO_COMERCIALES]


def voces():
    out = []
    try:
        with open(os.path.join(VOCES, "voces.json"), encoding="utf-8") as f:
            propias = json.load(f)
    except Exception:
        propias = []
    for v in propias:
        if os.path.exists(os.path.join(VOCES, v["archivo"])):
            out.append(dict(id=v["id"], nombre=v["nombre"], tipo="propia", duracion=v.get("duracion"),
                            prueba=os.path.exists(os.path.join(VOCES, v["id"] + "_prueba.wav"))))
    for f in sorted(glob.glob(os.path.join(BIBLIOTECA_VOCES, "*.*"))):
        if f.lower().endswith((".mp3", ".wav")):
            n = os.path.splitext(os.path.basename(f))[0]
            if n.lower() not in VOCES_VISIBLES:
                continue
            vid = "lib_" + P.slug(n)
            out.append(dict(id=vid, nombre=n, tipo="biblioteca",
                            prueba=os.path.exists(os.path.join(VOCES, vid + "_prueba.wav"))))
    return out


def ruta_voz(vid):
    if vid.startswith("lib_"):
        for f in glob.glob(os.path.join(BIBLIOTECA_VOCES, "*.*")):
            if "lib_" + P.slug(os.path.splitext(os.path.basename(f))[0]) == vid:
                return f
        return None
    try:
        with open(os.path.join(VOCES, "voces.json"), encoding="utf-8") as f:
            for v in json.load(f):
                if v["id"] == vid:
                    return os.path.join(VOCES, v["archivo"])
    except Exception:
        pass
    return None


def lista_proyectos():
    out = []
    for f in glob.glob(os.path.join(P.PROYECTOS, "*", "proyecto.json")):
        carpeta = os.path.dirname(f)
        if os.path.basename(carpeta).startswith("_"):
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                p = json.load(fh)
        except Exception:
            continue
        est = T.leer_estado(carpeta)
        out.append(dict(id=p["id"], titulo=p.get("titulo"), formato=p.get("formato"), estilo=p.get("estilo"),
                        modificado=p.get("modificado", 0), estado=est.get("estado", "borrador"),
                        pct=est.get("pct", 0), mensaje=est.get("mensaje", ""),
                        portada=os.path.exists(os.path.join(carpeta, "portada.jpg")), duracion=est.get("duracion")))
    return sorted(out, key=lambda x: -x["modificado"])


def info_estilos():
    def portada(eid):
        f = os.path.join(PORTADAS, eid + ".jpg")
        return int(os.path.getmtime(f)) if os.path.exists(f) else None
    base = [dict(id=k, nombre=v, tipo="base", portada=portada(k), vista=V.info(k)) for k, v in P.ESTILOS_BASE.items()]
    pers = [dict(e, tipo="personal", portada=portada(e["id"]), vista=V.info(e["id"])) for e in EST.cargar()]
    pro = [dict(id=c["id"], nombre=c["nombre"], tipo="canal", canal=c["canal"], descripcion=c["descripcion"],
                portada=portada(c["id"]), vista=V.info(c["id"])) for c in V.CANALES]
    return base + pers + pro


# ------------------------------------------------------------------ portadas de estilo (en segundo plano, de una en una)
_cola_portadas, _pendientes = [], set()
_hay_portadas = threading.Condition()


def pedir_portada(eid, forzar=False):
    if not forzar and os.path.exists(os.path.join(PORTADAS, eid + ".jpg")):
        return
    with _hay_portadas:
        if eid not in _pendientes:
            _pendientes.add(eid)
            _cola_portadas.append(eid)
            _hay_portadas.notify()


def portadas_pendientes():
    return sorted(_pendientes)


def _hilo_portadas():
    while True:
        with _hay_portadas:
            while not _cola_portadas:
                _hay_portadas.wait()
            eid = _cola_portadas.pop(0)
        try:
            _dibujar_portada(eid)
        except Exception as ex:
            print(f"portada {eid}: {ex}", flush=True)
        finally:
            _pendientes.discard(eid)


def escribir_muestra(carpeta, eid, formato="horizontal"):
    """guion.py/escenas.py del video de muestra con el estilo eid. False si el estilo no existe."""
    personal = None
    if eid in P.ESTILOS_BASE:
        nombre = eid
    else:
        e = EST.buscar(eid)
        if not e:
            return False
        personal, nombre = EST.a_nucleo(e), "personal"
    p, _, _ = P.validar(dict(MUESTRA_GUION, estilo=nombre, formato=formato), iconos())
    P.escribir(carpeta, p, os.path.join(BIBLIOTECA_VOCES, "Dan.mp3"), personal)
    return True


def _hilo_vistas():
    """Saca vistas de 20 s de los videos ya terminados (al arrancar y cada 90 s, por si se terminó uno nuevo)."""
    while True:
        try:
            V.completar_canales(PORTADAS)
            V.completar_desde_videos([e["id"] for e in info_estilos() if e["tipo"] != "canal"])
        except Exception as ex:
            print("vistas:", ex, flush=True)
        time.sleep(90)


def _dibujar_portada(eid):
    import subprocess
    carpeta = os.path.join(P.PROYECTOS, "_portada")
    shutil.rmtree(carpeta, ignore_errors=True)
    if not escribir_muestra(carpeta, eid):
        return
    T._correr("portada", [sys.executable, os.path.join(T.NUCLEO, "muestra_estilo.py"), "4"], carpeta,
              os.path.join(carpeta, "log.txt"), descripcion="portada de estilo")
    origen = os.path.join(carpeta, "previews", "muestra", "m_02.jpg")
    if not os.path.exists(origen):
        raise RuntimeError("no salió el cuadro")
    os.makedirs(PORTADAS, exist_ok=True)
    subprocess.run([T.FFMPEG, "-y", "-loglevel", "error", "-i", origen, "-vf", "crop=iw*0.8:ih*0.8:iw*0.1:ih*0.12,scale=640:-2", "-q:v", "3",
                    os.path.join(PORTADAS, eid + ".jpg")], capture_output=True,
                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)


# ------------------------------------------------------------------ un solo prompt -> video
def guion_ia(tema, tono, a, palabras_max=P.PALABRAS_MAX, estilo="limpio"):
    g, uso = G.escribir_guion(a["clave"], a["modelo"], tema, tono, iconos(), palabras_max, estilo=estilo)
    for e in g.get("escenas", []):
        e["claves"] = [[c.get("palabra", ""), c.get("etiqueta", "")] for c in e.get("claves", [])]
        for k in ("icono2", "cifra", "cifra_palabra", "titulo", "estampa", "lugar", "ruta"):
            if not e.get(k):
                e.pop(k, None)
    return g


def crear_video(pid, d, a):
    """En segundo plano: Gemini escribe el guion (y elige estilo si es «auto») y arranca la producción.
    `a` = ajustes de la petición que lo pidió (con SU key de Gemini; este hilo no tiene la petición HTTP)."""
    carpeta = os.path.join(P.PROYECTOS, pid)
    try:
        T._escribir_estado(carpeta, estado="produciendo", paso="guion", pct=1, mensaje="Escribiendo el guion con IA",
                           error=None, detalle=None, inicio=time.time())
        tema = d["tema"]
        p = P.cargar(pid)
        estilo_solicitado = p.get("estilo") or d.get("estilo") or "auto"
        g = guion_ia(tema, d.get("tono"), a, estilo=estilo_solicitado)
        p.update(titulo=g.get("titulo") or tema[:60], cierre=g.get("cierre"), escenas=g.get("escenas", []),
                 cerebro=f"Gemini · {a['modelo']}")
        if p.get("musica", "auto") == "auto":
            p["musica"] = g.get("musica", "auto")
        if p.get("estilo") == "auto":
            T._escribir_estado(carpeta, mensaje="Eligiendo el estilo visual")
            opciones = dict(P.ESTILOS_BASE)
            opciones.update({e["id"]: e.get("descripcion") or e["nombre"] for e in EST.cargar()})
            opciones.update({"pro_kz_plano": "Kurzgesagt ilustrado (espacio, ciencia, tecnología)",
                             "pro_documental": "Documental de misterio (archivos, enigmas y evidencias)",
                             "pro_mapas": "Mapas con relieve real (historia, viajes y geografía)"})
            p["estilo"] = G.elegir_estilo(a["clave"], a["modelo"], tema, opciones) or "doodle"
        p, avisos, errores = materializar(p)
        if errores:                                    # casi siempre: guion largo -> otra vez, más corto
            T._escribir_estado(carpeta, mensaje="Acortando el guion para que quepa en 60 segundos")
            g = guion_ia(tema, d.get("tono"), a, P.PALABRAS_MAX - 30)
            p.update(titulo=g.get("titulo") or p["titulo"], cierre=g.get("cierre"), escenas=g.get("escenas", []))
            p, avisos, errores = materializar(p)
        if errores:
            raise RuntimeError("\n".join(errores))
        if p.get("creativo") and p.get("estilo") in AG.ESTILOS_CREATIVOS:
            tomas_creativas(carpeta, p, a)
        T.producir(pid, a["procs"])
    except Exception as ex:
        T._escribir_estado(carpeta, estado="error", paso=None, mensaje="Algo salió mal", error=str(ex))


def tomas_creativas(carpeta, p, a):
    """Modo creativo: el agente escribe, prueba y revisa con visión una toma a medida por parte. Si falla, el video
    sigue con las plantillas (nunca bloquea la producción)."""
    T._escribir_estado(carpeta, paso="tomas", pct=2, mensaje="Modo creativo: la IA está diseñando cada toma")
    try:
        r = AG.crear_tomas(carpeta, p, a, avisar=lambda m: T._escribir_estado(carpeta, mensaje="Modo creativo · " + m))
        inf = r.get("informe", {})
        hechas = [x for x in inf.get("partes", []) if not x.get("plantilla")]
        T._escribir_estado(carpeta, creativo=dict(hechas=len(hechas), total=len(inf.get("partes", [])),
                                                  notas={x["id"]: x.get("nota") for x in inf.get("partes", [])}))
    except Exception as ex:
        T._escribir_estado(carpeta, creativo=dict(error=str(ex)[:300]))


# ------------------------------------------------------------------ proyecto -> archivos del pipeline
def materializar(p):
    """Valida, y escribe guion.py/escenas.py. Devuelve (proyecto, avisos, errores)."""
    p, avisos, errores = P.validar(p, iconos())
    carpeta = os.path.join(P.PROYECTOS, p["id"])
    if not p.get("voz"):
        p["voz"] = "lib_dan"
    ref = ruta_voz(p["voz"]) or os.path.join(BIBLIOTECA_VOCES, "Dan.mp3")
    personal = None
    if p.get("estilo") not in P.ESTILOS_BASE:
        e = EST.buscar(p.get("estilo"))
        if e:
            personal = EST.a_nucleo(e)
        elif str(p.get("estilo", "")).startswith("pro_"):
            pass  # Estilo Premium con motor propio
        else:
            p["estilo"] = "limpio"
    if p["escenas"]:
        P.escribir(carpeta, p, ref, personal)
    tl = os.path.join(carpeta, "timeline.json")        # el guion cambió: la sincronización vieja ya no sirve
    if os.path.exists(tl) and T.leer_estado(carpeta).get("estado") not in ("produciendo", "en_cola"):
        os.remove(tl)
    P.guardar(p)
    return p, avisos, errores


def preparar_sistema():
    """Proyecto interno con un guion de muestra (para miniaturas de dibujos y muestras de estilo)."""
    if not os.path.exists(os.path.join(SISTEMA, "guion.py")):
        p, _, _ = P.validar(dict(MUESTRA_GUION, id="_sistema"), iconos())
        P.escribir(SISTEMA, p, os.path.join(BIBLIOTECA_VOCES, "Dan.mp3"))
    T.miniaturas_iconos(ICONOS_DIR, SISTEMA)
    threading.Thread(target=_hilo_portadas, daemon=True).start()
    threading.Thread(target=_hilo_vistas, daemon=True).start()
    for e in info_estilos():
        if not e["portada"] and e["tipo"] != "canal":
            pedir_portada(e["id"])


def muestra_estilo(estilo, formato):
    """Escribe el proyecto de muestra con ese estilo y lanza la vista previa (4 cuadros)."""
    carpeta = os.path.join(P.PROYECTOS, "_muestra_estilo")
    personal = None
    if isinstance(estilo, dict):
        personal = EST.a_nucleo(estilo)
        nombre = "personal"
    else:
        nombre = estilo if estilo in P.ESTILOS_BASE else "limpio"
        e = EST.buscar(estilo)
        if e:
            personal, nombre = EST.a_nucleo(e), "personal"
    p, _, _ = P.validar(dict(MUESTRA_GUION, formato=formato, estilo=nombre), iconos())
    P.escribir(carpeta, p, os.path.join(BIBLIOTECA_VOCES, "Dan.mp3"), personal)
    tl = os.path.join(carpeta, "timeline.json")
    if os.path.exists(tl):
        os.remove(tl)
    T.vista_previa(carpeta, 4)
    return carpeta


# ------------------------------------------------------------------ HTTP
class Manejador(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def _cuerpo(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    def _archivo(self, ruta, descargar=None):
        if not ruta or not os.path.isfile(ruta):
            return self._json(dict(error="no existe"), 404)
        tam = os.path.getsize(ruta)
        tipo = mimetypes.guess_type(ruta)[0] or "application/octet-stream"
        rango = self.headers.get("Range")
        ini, fin = 0, tam - 1
        if rango and (m := re.match(r"bytes=(\d*)-(\d*)", rango)):
            ini = int(m.group(1)) if m.group(1) else max(0, tam - int(m.group(2)))
            fin = int(m.group(2)) if m.group(1) and m.group(2) else tam - 1
            self.send_response(206)
            self.send_header("Content-Range", f"bytes {ini}-{fin}/{tam}")
        else:
            self.send_response(200)
        self.send_header("Content-Type", tipo)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(fin - ini + 1))
        self.send_header("Cache-Control", "no-cache")
        if descargar:
            self.send_header("Content-Disposition", f'attachment; filename="{descargar}"')
        self.end_headers()
        with open(ruta, "rb") as f:
            f.seek(ini)
            falta = fin - ini + 1
            try:
                while falta > 0:
                    b = f.read(min(1 << 20, falta))
                    if not b:
                        break
                    self.wfile.write(b)
                    falta -= len(b)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass

    @staticmethod
    def _seguro(base, rel):
        ruta = os.path.normpath(os.path.join(base, rel))
        return ruta if ruta.startswith(os.path.normpath(base) + os.sep) else None

    def _cargar_cabeceras(self):
        """La key y el modelo de Gemini vienen del navegador (localStorage), no del disco del servidor."""
        _PET.clave = (self.headers.get("X-Gemini-Key") or "").strip()
        _PET.modelo = (self.headers.get("X-Gemini-Model") or "").strip()

    # ---------------- GET
    def do_GET(self):
        self._cargar_cabeceras()
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        ruta = unquote(u.path)
        try:
            if ruta in ("/", "/index.html"):
                b = open(HTML, "rb").read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(b)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                return self.wfile.write(b)
            if ruta == "/api/inicio":
                libre = shutil.disk_usage(P.PROYECTOS if os.path.isdir(P.PROYECTOS) else AQUI).free / 2 ** 30
                return self._json(dict(ajustes=ajustes_publicos(), estilos=info_estilos(), iconos=iconos(),
                                       animos=list(P.ANIMOS), voces=voces(), pendientes=portadas_pendientes(), proyectos=lista_proyectos(),
                                       disco_gb=round(libre, 1), carpeta_trabajo=P.DATOS, en_e=P.EN_E,
                                       disco_c_gb=round(shutil.disk_usage(AQUI).free / 2 ** 30, 1), ocupado=T.ocupado(),
                                       palabras_max=P.PALABRAS_MAX, fondos=EST.FONDOS, paletas=EST.PALETAS,
                                       letras=EST.LETRAS, con_paleta=EST.CON_PALETA,
                                       iconos_listos=os.path.isdir(ICONOS_DIR) and len(os.listdir(ICONOS_DIR)) >= 50))
            if ruta == "/api/proyectos":
                return self._json(dict(proyectos=lista_proyectos(), ocupado=T.ocupado()))
            if ruta == "/api/proyecto":
                p = P.cargar(q["id"])
                carpeta = os.path.join(P.PROYECTOS, p["id"])
                return self._json(dict(proyecto=p, estado=T.leer_estado(carpeta), previa=T.estado_previa(carpeta)))
            if ruta == "/api/previa":
                carpeta = os.path.join(P.PROYECTOS, q["id"])
                return self._json(T.estado_previa(carpeta))
            if ruta == "/api/estilo/previa":
                return self._json(T.estado_previa(os.path.join(P.PROYECTOS, "_muestra_estilo")))
            if ruta == "/api/voz/prueba":
                return self._json(T.estado_prueba_voz(q["id"]))
            if ruta == "/api/estilos":
                return self._json(dict(estilos=info_estilos(), pendientes=portadas_pendientes()))
            if ruta.startswith("/vista/"):
                return self._archivo(self._seguro(V.DIR, ruta[len("/vista/"):]))
            if ruta.startswith("/portada/"):
                return self._archivo(self._seguro(PORTADAS, ruta[len("/portada/"):]))
            if ruta.startswith("/icono/"):
                return self._archivo(self._seguro(ICONOS_DIR, ruta[len("/icono/"):]))
            if ruta.startswith("/voz/"):
                return self._archivo(self._seguro(VOCES, ruta[len("/voz/"):]))
            if ruta.startswith("/archivo/"):            # /archivo/<id>/<ruta dentro del proyecto>
                pid, rel = ruta[len("/archivo/"):].split("/", 1)
                base = os.path.join(P.PROYECTOS, pid)
                f = self._seguro(base, rel)
                desc = None
                if q.get("descargar") and f:
                    desc = re.sub(r"[^\w.\-]+", "_", os.path.basename(f).replace("_MASTER", ""))
                return self._archivo(f, desc)
            self._json(dict(error="no encontrado"), 404)
        except KeyError as ex:
            self._json(dict(error=f"falta el dato {ex}"), 400)
        except FileNotFoundError:
            self._json(dict(error="ese proyecto no existe"), 404)
        except Exception as ex:
            self._json(dict(error=str(ex)), 500)

    # ---------------- POST
    def do_POST(self):
        self._cargar_cabeceras()
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        ruta = u.path
        try:
            if ruta == "/api/voz/subir":                 # cuerpo = audio crudo; ?nombre=…&ext=…
                datos = self._cuerpo()
                if len(datos) > 40 * 2 ** 20:
                    return self._json(dict(error="El audio pesa demasiado (máx. 40 MB)."), 400)
                if q.get("permiso") != "1":
                    return self._json(dict(error="Confirma que la voz es tuya o que tienes permiso para usarla."), 400)
                os.makedirs(VOCES, exist_ok=True)
                nombre = (q.get("nombre") or "Mi voz").strip()[:30]
                vid = "voz_" + time.strftime("%Y%m%d%H%M%S")
                ext = re.sub(r"[^a-z0-9]", "", (q.get("ext") or "bin").lower())[:5]
                crudo = os.path.join(VOCES, vid + "_original." + ext)
                with open(crudo, "wb") as f:
                    f.write(datos)
                try:
                    dur = T.preparar_voz(crudo, os.path.join(VOCES, vid + ".wav"))
                finally:
                    try:
                        os.remove(crudo)
                    except OSError:
                        pass
                lista = []
                try:
                    with open(os.path.join(VOCES, "voces.json"), encoding="utf-8") as f:
                        lista = json.load(f)
                except Exception:
                    pass
                lista.append(dict(id=vid, nombre=nombre, archivo=vid + ".wav", duracion=round(dur, 1), creada=time.time()))
                with open(os.path.join(VOCES, "voces.json"), "w", encoding="utf-8") as f:
                    json.dump(lista, f, ensure_ascii=False, indent=1)
                return self._json(dict(ok=True, id=vid, duracion=dur, voces=voces()))

            d = json.loads(self._cuerpo() or b"{}")
            if ruta == "/api/ajustes":                   # solo lo del equipo; la key y el modelo son del navegador
                a = ajustes()
                if d.get("procs"):
                    a["procs"] = max(2, min(16, int(d["procs"])))
                guardar_ajustes(a)
                return self._json(dict(ok=True, ajustes=ajustes_publicos()))
            if ruta == "/api/gemini/modelos":
                clave = (d.get("clave") or ajustes().get("clave") or "").strip()
                if not clave:
                    return self._json(dict(error="Primero pega tu API key de Gemini."), 400)
                return self._json(dict(modelos=G.modelos(clave)))
            if ruta == "/api/gemini/probar":
                a = ajustes()
                clave = (d.get("clave") or a.get("clave") or "").strip()
                G.probar(clave, d.get("modelo") or a["modelo"])
                return self._json(dict(ok=True))
            if ruta == "/api/crear":                       # UN prompt -> video
                a = ajustes()
                if not a.get("clave"):
                    return self._json(dict(error="Para crear con un prompt necesitas tu API key de Gemini (pestaña Ajustes)."), 400)
                tema = (d.get("tema") or "").strip()
                if len(tema) < 4:
                    return self._json(dict(error="Describe tu video en una frase."), 400)
                pid = P.nuevo_id(tema)
                p = dict(id=pid, titulo=tema[:60], tema=tema, tono=d.get("tono") or "",
                         formato="vertical" if d.get("formato") == "vertical" else "horizontal",
                         estilo=d.get("estilo") or "auto", voz=d.get("voz") or "lib_dan", musica=d.get("musica") or "auto",
                         expresividad=float(d.get("expresividad", 0.7)), escenas=[], cierre="",
                         creativo=bool(d.get("creativo")))
                P.guardar(p)
                T._escribir_estado(os.path.join(P.PROYECTOS, pid), estado="en_cola", paso=None, pct=0,
                                   mensaje="Preparando…", inicio=time.time())     # antes de responder: la interfaz lo ve ya
                threading.Thread(target=crear_video, args=(pid, d, a), daemon=True).start()
                return self._json(dict(ok=True, id=pid))
            if ruta == "/api/estilo/ia":                   # UN prompt -> estilo + portada
                a = ajustes()
                if not a.get("clave"):
                    return self._json(dict(error="Para crear estilos con un prompt necesitas tu API key de Gemini (Ajustes)."), 400)
                desc = (d.get("descripcion") or "").strip()
                if len(desc) < 3:
                    return self._json(dict(error="Describe cómo quieres que se vea."), 400)
                e = G.disenar_estilo(a["clave"], a["modelo"], desc, dict(P.ESTILOS_BASE), EST.FONDOS, EST.PALETAS, EST.LETRAS)
                e["descripcion"] = desc
                e.pop("id", None)
                e = EST.guardar_uno(e)
                pedir_portada(e["id"], forzar=True)
                return self._json(dict(ok=True, estilo=e, estilos=info_estilos()))
            if ruta == "/api/guion/ia":
                a = ajustes()
                if not a.get("clave"):
                    return self._json(dict(error="Para escribir con IA necesitas tu API key de Gemini (pestaña Ajustes)."), 400)
                tema = (d.get("tema") or "").strip()
                if len(tema) < 4:
                    return self._json(dict(error="Cuéntame de qué trata tu video (una frase basta)."), 400)
                g, uso = G.escribir_guion(a["clave"], a["modelo"], tema, d.get("tono"), iconos(), P.PALABRAS_MAX)
                for e in g.get("escenas", []):
                    e["claves"] = [[c.get("palabra", ""), c.get("etiqueta", "")] for c in e.get("claves", [])]
                    for k in ("icono2", "cifra", "cifra_palabra", "titulo"):
                        if not e.get(k):
                            e.pop(k, None)
                p = dict(d.get("base") or {})
                p.update(titulo=g.get("titulo"), cierre=g.get("cierre"), escenas=g.get("escenas", []),
                         tema=tema, tono=d.get("tono"), cerebro=f"Gemini · {a['modelo']}")
                if p.get("musica", "auto") == "auto":
                    p["musica"] = g.get("musica", "auto")
                p["id"] = p.get("id") or P.nuevo_id(p["titulo"] or tema)
                p, avisos, errores = materializar(p)
                return self._json(dict(proyecto=p, avisos=avisos, errores=errores, uso=uso))
            if ruta == "/api/proyecto/guardar":
                p = d["proyecto"]
                p["id"] = p.get("id") or P.nuevo_id(p.get("titulo") or "video")
                if T.leer_estado(os.path.join(P.PROYECTOS, p["id"])).get("estado") in ("produciendo", "en_cola"):
                    return self._json(dict(error="Este video se está creando; espera a que termine o cancélalo."), 409)
                p, avisos, errores = materializar(p)
                return self._json(dict(proyecto=p, avisos=avisos, errores=errores))
            if ruta == "/api/proyecto/previa":
                T.vista_previa(os.path.join(P.PROYECTOS, d["id"]), 6)
                return self._json(dict(ok=True))
            if ruta == "/api/proyecto/producir":
                p = P.cargar(d["id"])
                p, avisos, errores = materializar(p)
                if errores:
                    return self._json(dict(error="\n".join(errores)), 400)
                if T.leer_estado(os.path.join(P.PROYECTOS, p["id"])).get("estado") in ("produciendo", "en_cola"):
                    return self._json(dict(error="Ya se está creando."), 409)
                T.producir(p["id"], ajustes()["procs"])
                return self._json(dict(ok=True))
            if ruta == "/api/proyecto/cancelar":
                T.cancelar("producir:" + d["id"])
                carpeta = os.path.join(P.PROYECTOS, d["id"])
                if T.leer_estado(carpeta).get("estado") == "en_cola":     # aún esperando turno: se ve cancelado ya
                    T._escribir_estado(carpeta, estado="cancelado", paso=None, pct=0, mensaje="Cancelado")
                return self._json(dict(ok=True))
            if ruta == "/api/proyecto/borrar":
                carpeta = os.path.join(P.PROYECTOS, d["id"])
                if T.leer_estado(carpeta).get("estado") in ("produciendo", "en_cola"):
                    return self._json(dict(error="Cancela la creación antes de borrarlo."), 409)
                if os.path.basename(carpeta).startswith("_") or not os.path.isfile(os.path.join(carpeta, "proyecto.json")):
                    return self._json(dict(error="no existe"), 404)
                shutil.rmtree(carpeta, ignore_errors=True)
                return self._json(dict(ok=True))
            if ruta == "/api/proyecto/duplicar":
                p = P.cargar(d["id"])
                p["id"] = P.nuevo_id(p["titulo"])
                p["titulo"] = (p["titulo"] + " (copia)")[:70]
                p, _, _ = materializar(p)
                return self._json(dict(proyecto=p))
            if ruta == "/api/voz/probar":
                ref = ruta_voz(d["id"])
                if not ref:
                    return self._json(dict(error="Esa voz no existe."), 404)
                os.makedirs(VOCES, exist_ok=True)
                T.probar_voz(d["id"], ref, os.path.join(VOCES, d["id"] + "_prueba.wav"),
                             (d.get("texto") or TEXTO_PRUEBA_VOZ)[:200], float(d.get("expresividad", 0.7)))
                return self._json(dict(ok=True))
            if ruta == "/api/voz/borrar":
                lista = []
                with open(os.path.join(VOCES, "voces.json"), encoding="utf-8") as f:
                    lista = json.load(f)
                for v in lista:
                    if v["id"] == d["id"]:
                        for x in (v["archivo"], v["id"] + "_prueba.wav"):
                            try:
                                os.remove(os.path.join(VOCES, x))
                            except OSError:
                                pass
                with open(os.path.join(VOCES, "voces.json"), "w", encoding="utf-8") as f:
                    json.dump([v for v in lista if v["id"] != d["id"]], f, ensure_ascii=False, indent=1)
                return self._json(dict(ok=True, voces=voces()))
            if ruta == "/api/estilo/guardar":
                e = EST.guardar_uno(d["estilo"])
                pedir_portada(e["id"], forzar=True)
                if (V.info(e["id"]).get("origen") == "muestra"):
                    V.borrar(e["id"])                       # el estilo cambió: su muestra ya no lo representa
                return self._json(dict(ok=True, estilo=e, estilos=info_estilos()))
            if ruta == "/api/estilo/vista":            # generar (o rehacer) la vista de 20 s
                eid = d["id"]
                if eid.startswith("pro_"):
                    return self._json(dict(error="Los estilos Premium usan un fragmento de su video real."), 400)
                if eid not in P.ESTILOS_BASE and not EST.buscar(eid):
                    return self._json(dict(error="Ese estilo no existe."), 404)
                V.generar(eid, lambda carpeta: escribir_muestra(carpeta, eid), min(ajustes()["procs"], 10))
                return self._json(dict(ok=True))
            if ruta == "/api/estilo/borrar":
                EST.borrar(d["id"])
                V.borrar(d["id"])
                try:
                    os.remove(os.path.join(PORTADAS, d["id"] + ".jpg"))
                except OSError:
                    pass
                return self._json(dict(ok=True, estilos=info_estilos()))
            if ruta == "/api/estilo/previa":
                muestra_estilo(d.get("estilo"), "vertical" if d.get("formato") == "vertical" else "horizontal")
                return self._json(dict(ok=True))
            self._json(dict(error="no encontrado"), 404)
        except RuntimeError as ex:
            self._json(dict(error=str(ex)), 400)
        except KeyError as ex:
            self._json(dict(error=f"falta el dato {ex}"), 400)
        except Exception as ex:
            self._json(dict(error=f"{type(ex).__name__}: {ex}"), 500)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--puerto", type=int, default=8790)
    ap.add_argument("--abrir", action="store_true")
    a = ap.parse_args()
    os.makedirs(P.PROYECTOS, exist_ok=True)
    preparar_sistema()
    srv = ThreadingHTTPServer(("127.0.0.1", a.puerto), Manejador)
    url = f"http://127.0.0.1:{a.puerto}"
    print(f"Estudio en {url}  (Ctrl+C para cerrar)", flush=True)
    if a.abrir:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
