# -*- coding: utf-8 -*-
"""AGENTE DE TOMAS del Estudio («modo creativo»): la IA escribe el código de cada toma, la prueba, la MIRA y la corrige.

Aprendido del generador de clips Remotion de C:\\googleimagenes\\holavideo (director -> programador -> render -> arreglo),
con dos mejoras: aquí un cuadro suelto se dibuja en < 1 s, así que se prueba ANTES del render, y la revisión con
visión es automática (allá era un botón).

Flujo por cada parte intermedia del guion (la intro y el cierre siguen con su plantilla):
  1. DIRECTOR (1 llamada para todo el video): un mundo visual distinto por parte, capas, actos amarrados a palabras.
  2. PROGRAMADOR: escribe `class Toma_pN(TomaBase)` usando solo kit_tomas.py + plano.py (manual con ejemplos verificados).
  3. REVISIÓN DE CÓDIGO (sin IA): AST — nada de imports, archivos, eval, while, dunders.
  4. PRUEBA: probar_toma.py en otro proceso (tiempo límite) dibuja 5 cuadros + mide cobertura y movimiento.
     Si truena: traceback + pista -> la IA lo arregla.
  5. JUEZ CON VISIÓN: la IA mira los cuadros con la lista de defectos de la Fábrica y pone nota 1-10.
     Si < 7: corrige con los cuadros delante (hasta 2 vueltas). Se queda la mejor versión que funcionó.
  6. RESPALDO: si ninguna versión funciona, esa parte usa la plantilla LibrePlano. Nunca queda un cuadro negro.
Salida: <proyecto>/tomas_ia.py (lo importa escenas.py) + <proyecto>/tomas_ia/ (borradores, cuadros, informe.json, hoja.jpg).

A mano:  python estudio/agente_tomas.py <carpeta_o_id_de_proyecto> [--solo p2,p3] [--modelo gemini-3.8-flash]
         (la key: variable GEMINI_API_KEY o --clave-archivo ruta.txt)
"""
import ast
import concurrent.futures as cf
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
NUCLEO = os.path.join(RAIZ, "nucleo")
sys.path.insert(0, AQUI)
import cerebro_gemini as G  # noqa: E402

ESTILOS_CREATIVOS = ("pro_kz_plano", "pro_kz_vertical", "pro_kz_iso", "pro_guache")
MODELO_CODIGO = "gemini-3.8-flash"        # escribir código pide más que el guion: Flash, no Flash-Lite
MAX_LLAMADAS_CODIGO = 6                   # por parte (primera versión + arreglos + correcciones visuales)
MAX_VUELTAS_VISUALES = 2
NOTA_OK = 7
TIEMPO_PRUEBA = 240                       # s por prueba (5 cuadros + pares de movimiento)
_PRUEBAS = threading.Semaphore(1)         # una prueba a la vez: 3 en paralelo agotaron la memoria (MemoryError, 5-oct)

PROHIBIDOS = {"open", "exec", "eval", "compile", "__import__", "getattr", "setattr", "delattr", "globals", "locals",
              "vars", "input", "breakpoint", "help", "exit", "quit", "os", "sys", "subprocess", "shutil", "pathlib",
              "socket", "importlib", "builtins", "memoryview", "type", "super_", "print"}


# ====================================================================== manual (prompt de sistema del programador)
def _firma(fn, quitar_self=True):
    try:
        s = str(inspect.signature(fn))
    except (TypeError, ValueError):
        return "(...)"
    if quitar_self:
        s = re.sub(r"^\(self,?\s*", "(", s)
    return s


def manual():
    """Prompt de sistema del programador (correr con el PYTHONPATH de un proyecto: el formato sale de su guion.py)."""
    import kit_tomas as kit
    vertical = kit.VERT
    P = kit.P
    W, H = (1080, 1920) if vertical else (1920, 1080)
    banda = 330 if vertical else 175
    metodos = []
    for nombre in ("cuando", "frase", "k", "u", "par", "ev", "cifra", "etiqueta", "contador", "montes", "suelo", "agua",
                   "ciudad", "arboles", "nubes", "aves", "particulas", "resplandor", "persona", "multitud", "busto",
                   "flecha", "barra"):
        fn = getattr(kit.TomaBase, nombre)
        doc = (inspect.getdoc(fn) or "").strip()
        metodos.append(f"self.{nombre}{_firma(fn)}" + (f"\n    {doc.replace(chr(10), chr(10) + '    ')}" if doc else ""))
    objetos = []
    for nombre in ("esfera", "sol", "tierra", "luna", "pajaro", "kuri", "microbio", "arbol", "hojas_cayendo", "termometro",
                   "fumarola", "onda", "discontinua", "linea_llamada", "planeta", "sol_corte", "galaxia",
                   "estrella_neutrones", "casa", "planta", "conejo", "zorro", "gusano_tubo", "panel_solar",
                   "central_nuclear", "interruptor", "molecula", "rotulo", "pastilla", "mezcla", "aclarar", "oscurecer"):
        fn = getattr(P, nombre, None)
        if fn:
            doc = (inspect.getdoc(fn) or "").split("\n")[0]
            objetos.append(f"P.{nombre}{_firma(fn, False)}" + (f"  # {doc}" if doc else ""))
    with open(os.path.join(AQUI, "ejemplos_tomas.py"), encoding="utf-8") as f:
        ejemplos = f.read().split('from kit_tomas import *  # noqa: F401,F403', 1)[-1].split("TOMAS = {")[0].strip()
    return f"""Eres animador y programador de motion graphics estilo KURZGESAGT (In a Nutshell): ilustración vectorial plana con
degradados suaves, sombras de 2 tonos, luces con halo, colores saturados, mucho detalle y TODO en movimiento.
Escribes UNA toma de un video en Python, para un motor propio que dibuja cuadro a cuadro.

FORMATO DE RESPUESTA: solo el código Python de UNA clase `class <Nombre>(TomaBase):` (con docstring que resuma mundo y actos).
Sin imports (todo ya está importado), sin ``` y sin texto fuera del código.

CÓMO FUNCIONA UNA TOMA
- `preparar_toma(self)`: se llama una vez. Calcula aquí los segundos de cada acto con self.cuando("palabra") (palabra que
  se dice LITERALMENTE en las frases de la parte) y pon efectos de sonido con self.ev(t, nombre, vol).
  Efectos válidos: {", ".join(kit.SFX_OK)}.
- `escena(self, lz, t)`: se llama en CADA cuadro con el segundo t (absoluto; la toma va de self.t0 a self.t1, dura self.dur).
  Dibuja de atrás hacia delante. Nada de estado entre cuadros: todo es función de t.
- Atributos de clase: CIELO (fondo: {", ".join(["espacio", "espacio2"] + list(kit.CIELOS))}), ZOOM (acercamiento de cámara a
  lo largo de la toma, 0.03-0.10; negativo = se aleja), DERIVA (1 = deriva suave; 0 = fija).
- El rótulo (arriba), las etiquetas de las claves (abajo) y la cifra se dibujan SOLOS. Si quieres poner la cifra en un sitio
  concreto de tu composición llama self.cifra(lz, t, x, y, px). No escribas otros textos salvo, como mucho, UNA etiqueta
  corta (self.etiqueta) que nombre algo del dibujo.
- Lienzo de {W}x{H} px ({"VERTICAL 9:16" if vertical else "horizontal 16:9"}), origen arriba-izquierda, y hacia abajo.
  Franjas reservadas: y < {banda} (rótulo/cifra) y y > {H - banda} (etiquetas). Lo importante va entre ellas
  (Y_ACCION0={banda}, Y_ACCION1={H - banda}). Constantes: W, H, CX, CY, VERT.

API DE LA TOMA (métodos de TomaBase)
{chr(10).join(metodos)}

DIBUJO DE BAJO NIVEL (lz)
lz.relleno(pts, color, alfa=1.0)                 polígono relleno; pts = lista de (x, y) o array Nx2
lz.degradado(pts, c0, c1, p0, p1, alfa=1.0)      polígono con degradado lineal de c0 (en el punto p0) a c1 (en p1)
lz.halo(x, y, r, color, alfa=1.0)               luz/resplandor radial suave
lz.trazo(pts, color, ancho=6, temblor=0.0)       línea (usa temblor=0.0; NUNCA color negro puro)
with lz.grupo(x, y, s, rot):                     transforma lo de dentro (trasladar, escalar, rotar en radianes)
with lz.capa(i):                                 0 = fondo dibujado, 1 = objetos, 2 = encima de todo
Formas (devuelven puntos): circulo(cx, cy, r, n=64), elipse(cx, cy, rx, ry, rot=0), rect_red(x, y, w, h, radio),
  estrella(cx, cy, r1, r2, puntas=5), blob(cx, cy, r, seed=0, irr=0.18), bezier(p0, p1, p2, p3, n=40), catmull(pts, n=12)
Animación: prog(t, a, b) -> 0..1 lineal; e_in, e_out, e_inout, e_back, e_elastic (curvas 0..1); pop(t, t0, dur) aparición
  con rebote; sale(t, t0, dur) 1->0; lerp(a, b, u); h01(i, j=0, k=0) -> número pseudoaleatorio fijo 0..1 (NO uses random);
  ruido1(array, seed) ruido suave -1..1; math y np disponibles. Colores = tuplas RGB 0-255.

OBJETOS ILUSTRADOS YA HECHOS (plano.py, prefijo P.)
{chr(10).join(objetos)}
Personajes (TIPOS para self.persona/multitud/busto): {", ".join(kit.K.TIPOS)}

REGLAS DE CALIDAD (obligatorias; un juez va a mirar los cuadros)
1. Cada toma es SU PROPIO MUNDO concreto (lugar y época de lo que se narra), nada de fondo vacío ni íconos sueltos flotando.
2. Al menos 3 planos de profundidad con paralaje (self.par / prof en los ayudantes): lejano, medio y primer plano.
3. Animación ambiente continua SIEMPRE (nubes, aves, partículas, agua, humo, hojas, luces que titilan...).
4. La acción narrada OCURRE: personajes u objetos hacen lo que dice la frase justo cuando se dice (self.cuando).
   Algo visible cambia al menos cada 2 segundos. Usa anticipación y rebote (pop, e_back) en las apariciones.
5. El protagonista se ve GRANDE: al menos 1/3 de la altura útil (personas protagonistas con s = 40-55 en horizontal,
   55-75 en vertical; de fondo, 18-28). Mejor pocas cosas grandes y detalladas que muchas diminutas.
   El protagonista se ve grande y nada importante queda cortado por los bordes ni
   tapado por textos. Las personas pisan el suelo (pies sobre la línea de suelo), sin flotar ni encimarse.
6. Rendimiento: menos de ~250 figuras por cuadro; bucles de hasta 150 vueltas; nada de while.
7. Prohibido: import, open, eval, exec, archivos, atributos con doble guion bajo, print, variables globales.

EJEMPLOS VERIFICADOS (cópiales el nivel de detalle y la forma de organizar el código):
{ejemplos}
"""


# ====================================================================== utilidades
def limpiar_codigo(txt):
    txt = re.sub(r"^```(?:python|py)?\s*\n?", "", txt.strip(), flags=re.M)
    txt = re.sub(r"\n?```\s*$", "", txt, flags=re.M).strip()
    i = txt.find("class ")
    return txt[i:] if i > 0 else txt


def revisar_codigo(codigo, nombre):
    """Problemas de seguridad/forma (lista vacía = bien)."""
    try:
        arbol = ast.parse(codigo)
    except SyntaxError as ex:
        return [f"SyntaxError línea {ex.lineno}: {ex.msg}"]
    prob = []
    clases = [n for n in arbol.body if isinstance(n, ast.ClassDef)]
    if not any(c.name == nombre for c in clases):
        prob.append(f"Falta la clase `{nombre}` (debe llamarse exactamente así y heredar de TomaBase)")
    for n in arbol.body:
        if not isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.Assign, ast.Expr)):
            prob.append(f"Línea {n.lineno}: a nivel de módulo solo se permiten la clase, funciones y constantes")
    for n in ast.walk(arbol):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            prob.append(f"Línea {n.lineno}: no se permiten imports (todo ya está importado)")
        elif isinstance(n, (ast.While, ast.Global, ast.Nonlocal, ast.AsyncFunctionDef, ast.Await)):
            prob.append(f"Línea {n.lineno}: no se permite {type(n).__name__}")
        elif isinstance(n, ast.Name) and (n.id in PROHIBIDOS or n.id.startswith("__")):
            prob.append(f"Línea {n.lineno}: nombre prohibido `{n.id}`")
        elif isinstance(n, ast.Attribute) and n.attr.startswith("__"):
            prob.append(f"Línea {n.lineno}: atributo prohibido `{n.attr}`")
    return prob[:8]


def _firma_parte(frases):
    import hashlib
    return hashlib.md5("|".join(frases).encode("utf-8")).hexdigest()[:10]


def _modulo(codigos):
    """codigos: {id: (nombre_clase, codigo, firma)} -> texto de un módulo importable."""
    partes = ["# -*- coding: utf-8 -*-", "# Generado por el agente de tomas del Estudio (modo creativo). Se reescribe solo.",
              "from kit_tomas import *  # noqa: F401,F403", ""]
    for _, (nombre, codigo, _) in codigos.items():
        partes += [codigo, "", ""]
    partes.append("TOMAS = {" + ", ".join(f"{eid!r}: segura({nombre}, {firma!r})" for eid, (nombre, _, firma) in codigos.items()) + "}")
    return "\n".join(partes) + "\n"


class Agente:
    def __init__(self, carpeta, p, clave, modelo_guion, modelo_codigo=None, avisar=None, procs=3):
        self.carpeta, self.p, self.clave = carpeta, p, clave
        self.modelo_guion = modelo_guion or G.DEFECTO
        self.modelo_codigo = modelo_codigo or MODELO_CODIGO
        self.avisar = avisar or (lambda msg: print(msg, flush=True))
        self.procs = procs
        self.vert = p.get("formato") == "vertical"
        self.dir = os.path.join(carpeta, "tomas_ia")
        self.uso = dict(entrada=0, salida=0, llamadas=0)
        self._manual = None

    # ------------------------------------------------------------------ IA
    def _ia(self, texto, sistema=None, imagenes=(), esquema=None, temperatura=0.7, modelo=None):
        modelo = modelo or self.modelo_codigo
        try:
            r, uso = G.generar(self.clave, modelo, texto, sistema=sistema, imagenes=imagenes, esquema=esquema,
                               temperatura=temperatura)
        except RuntimeError as ex:
            if "no existe" in str(ex) and modelo != self.modelo_guion:   # el modelo de código no está en esa key
                self.avisar(f"El modelo {modelo} no está disponible; uso {self.modelo_guion}")
                self.modelo_codigo = self.modelo_guion
                r, uso = G.generar(self.clave, self.modelo_guion, texto, sistema=sistema, imagenes=imagenes,
                                   esquema=esquema, temperatura=temperatura)
            else:
                raise
        self.uso["entrada"] += uso["entrada"]
        self.uso["salida"] += uso["salida"]
        self.uso["llamadas"] += 1
        return r

    @property
    def sistema(self):
        """El manual se arma en un proceso con el PYTHONPATH del proyecto (el kit importa config -> guion.py)."""
        if self._manual is None:
            import trabajos as T
            r = subprocess.run([sys.executable, os.path.abspath(__file__), "--manual"], cwd=self.carpeta,
                               env=T.entorno(self.carpeta), capture_output=True, timeout=120,
                               creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
            txt = r.stdout.decode("utf-8", "replace")
            if r.returncode != 0 or len(txt) < 2000:
                raise RuntimeError("No se pudo armar el manual de tomas: " + r.stderr.decode("utf-8", "replace")[-400:])
            self._manual = txt
        return self._manual

    # ------------------------------------------------------------------ 1. director
    def dirigir(self, partes):
        esquema = {"type": "OBJECT", "properties": {"tomas": {"type": "ARRAY", "items": {
            "type": "OBJECT", "properties": {
                "id": {"type": "STRING"},
                "mundo": {"type": "STRING", "description": "Lugar concreto que se ve (qué hay, época, luz), 1-2 frases"},
                "cielo": {"type": "STRING", "enum": ["espacio", "espacio2", "dia", "atardecer", "amanecer", "noche", "oceano",
                                                     "abismo", "interior", "laboratorio", "bosque", "desierto", "volcan", "hielo"]},
                "capas": {"type": "ARRAY", "items": {"type": "STRING"}, "description": "lejano, medio, primer plano"},
                "protagonista": {"type": "STRING"},
                "actos": {"type": "ARRAY", "items": {"type": "OBJECT", "properties": {
                    "palabra": {"type": "STRING", "description": "UNA palabra dicha literalmente en la parte"},
                    "accion": {"type": "STRING"}}, "required": ["palabra", "accion"]}},
                "ambiente": {"type": "STRING", "description": "animación continua (partículas, nubes, agua...)"},
                "camara": {"type": "STRING"}},
            "required": ["id", "mundo", "cielo", "capas", "protagonista", "actos", "ambiente", "camara"]}}},
            "required": ["tomas"]}
        guion = "\n".join(f"[{e['id']}] " + " ".join(e["frases"]) for e in self.p["escenas"])
        pedidas = "\n".join(f"- {e['id']}: «{' '.join(e['frases'])}»" + (f" (cifra {e['cifra']})" if e.get("cifra") else "")
                            for e in partes)
        texto = f"""Eres director de arte de un video corto estilo Kurzgesagt ({'vertical 9:16' if self.vert else 'horizontal 16:9'}).
Título: «{self.p.get('titulo', '')}». Guion completo:
{guion}

Diseña la puesta en escena de estas partes:
{pedidas}

Para cada una: un MUNDO VISUAL concreto y distinto de las demás (lugar, época y luz que corresponden a lo narrado; si es
abstracto, una metáfora física dibujable), 3 capas de profundidad, un protagonista grande, 2-3 actos amarrados a palabras
que se dicen literalmente (en orden), animación ambiente y movimiento de cámara. Que se pueda dibujar con: paisajes
(montes, suelo, agua, ciudad, árboles, nubes, aves), personas de cuerpo entero o en primer plano, cuerpos celestes,
microbios, moléculas, casas, plantas, animales sencillos, partículas, flechas, contadores y formas vectoriales."""
        r = self._ia(texto, esquema=esquema, temperatura=0.9, modelo=self.modelo_guion)
        return {t["id"]: t for t in r.get("tomas", [])}

    # ------------------------------------------------------------------ 2. programador
    def _datos_parte(self, e, plan, nombre, otros):
        datos = dict(frases=e["frases"], titulo=e.get("titulo"), claves=e.get("claves"), cifra=e.get("cifra"),
                     cifra_palabra=e.get("cifra_palabra"))
        palabras = sorted({w.strip(".,;:¿?¡!«»\"'").lower() for f in e["frases"] for w in f.split()} - {""})
        return f"""Escribe la clase `{nombre}(TomaBase)` para la parte «{e['id']}» (dura ~{max(4, round(len(' '.join(e['frases']).split()) / 2.6))} s).
DATOS DE LA PARTE: {json.dumps(datos, ensure_ascii=False)}
Palabras que se dicen (para self.cuando): {", ".join(palabras)}
PLAN DEL DIRECTOR: {json.dumps(plan, ensure_ascii=False)}
Mundos de las otras partes (NO los repitas): {otros}"""

    def programar(self, e, plan, nombre, otros):
        return limpiar_codigo(self._ia(self._datos_parte(e, plan, nombre, otros), sistema=self.sistema, temperatura=0.8))

    def arreglar(self, e, plan, nombre, codigo, error):
        pista = ""
        if "unexpected keyword" in error or "positional argument" in error:
            pista = "\nPista: revisa la firma exacta de esa función en el manual; usa solo los parámetros listados."
        elif "KeyError" in error:
            pista = "\nPista: usa self.cuando('palabra', defecto) en vez de self.w(...); nunca indexes diccionarios inciertos."
        elif "not defined" in error:
            pista = "\nPista: usa solo nombres del manual (los de plano.py llevan prefijo P.)."
        texto = (f"Este código de toma tiene un error y no se puede dibujar.\nERROR:\n{error}{pista}\n\nCÓDIGO:\n{codigo}\n\n"
                 f"Devuelve la clase `{nombre}` COMPLETA y corregida (solo el código). Contexto de la parte:\n"
                 + self._datos_parte(e, plan, nombre, "-"))
        return limpiar_codigo(self._ia(texto, sistema=self.sistema, temperatura=0.4))

    def corregir(self, e, plan, nombre, codigo, problemas, cuadros):
        texto = (f"Este es el código de una toma y {len(cuadros)} cuadros de cómo se ve AHORA (en orden de tiempo).\n"
                 f"PROBLEMAS A CORREGIR:\n- " + "\n- ".join(problemas) +
                 f"\n\nCÓDIGO ACTUAL:\n{codigo}\n\nMejora la toma para resolver TODOS los problemas sin perder lo que ya está "
                 f"bien. Devuelve la clase `{nombre}` COMPLETA (solo el código). Contexto de la parte:\n"
                 + self._datos_parte(e, plan, nombre, "-"))
        return limpiar_codigo(self._ia(texto, sistema=self.sistema, imagenes=cuadros, temperatura=0.5))

    # ------------------------------------------------------------------ 4. prueba
    def probar(self, eid, nombre, codigo, version):
        borr = os.path.join(self.dir, f"borr_{eid}_v{version}.py")
        with open(borr, "w", encoding="utf-8") as f:
            f.write(_modulo({eid: (nombre, codigo, None)}))
        sal = os.path.join(self.dir, f"prueba_{eid}_v{version}")
        shutil.rmtree(sal, ignore_errors=True)
        import trabajos as T
        try:
            with _PRUEBAS:
                subprocess.run([sys.executable, os.path.join(AQUI, "probar_toma.py"), borr, sal, eid, "5"],
                               cwd=self.carpeta, env=T.entorno(self.carpeta), capture_output=True, timeout=TIEMPO_PRUEBA,
                               creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        except subprocess.TimeoutExpired:
            return dict(error=f"La toma tarda demasiado en dibujarse (más de {TIEMPO_PRUEBA} s para 10 cuadros): "
                              "reduce figuras y bucles."), sal
        try:
            with open(os.path.join(sal, "resultado.json"), encoding="utf-8") as f:
                res = json.load(f)
        except (OSError, json.JSONDecodeError):
            return dict(error="La prueba no produjo resultado (el proceso se cayó)."), sal
        if "_general" in res:
            return dict(error=res["_general"]["error"]), sal
        return res.get(eid, dict(error="sin resultado")), sal

    @staticmethod
    def problemas_medidos(r):
        cs = r.get("cuadros", [])
        prob = []
        if cs and sum(c["cobertura"] for c in cs) / len(cs) < 0.15:
            prob.append("La escena se ve casi vacía: llena el cuadro con capas de paisaje/objetos (cobertura < 15 %).")
        quietos = [i + 1 for i, c in enumerate(cs) if c["movimiento"] < 0.35]
        if len(quietos) >= 2:
            prob.append(f"Hay momentos casi quietos (cuadros {quietos}): añade animación ambiente y acción continua.")
        lentos = [c["ms"] for c in cs if c["ms"] > 2500]
        if lentos:
            prob.append(f"Algunos cuadros tardan {max(lentos)} ms en dibujarse: simplifica (menos figuras por cuadro).")
        return prob

    # ------------------------------------------------------------------ 5. juez con visión
    def juzgar(self, e, plan, cuadros):
        esquema = {"type": "OBJECT", "properties": {
            "nota": {"type": "INTEGER", "description": "1-10"},
            "problemas": {"type": "ARRAY", "items": {"type": "STRING"}},
            "bien": {"type": "STRING"}}, "required": ["nota", "problemas"]}
        texto = f"""Eres el supervisor de calidad de un estudio que imita a Kurzgesagt con MUY buena calidad.
Estos son {len(cuadros)} cuadros (en orden) de una toma de ~{len(' '.join(e['frases']).split()) / 2.6:.0f} s.
Narración: «{' '.join(e['frases'])}»
Plan pedido: {json.dumps(plan, ensure_ascii=False)}

Evalúa con dureza y pon nota 1-10 (7 = se puede publicar). Defectos que BAJAN la nota:
escenario vacío o fondo liso con cosas sueltas; no se entiende qué lugar es o no tiene que ver con la narración; la acción
narrada no ocurre; figuras deformes, sin cara, flotando o encimadas; algo importante cortado por el borde o tapado por
textos; textos que chocan; elementos diminutos; colores apagados o feos; nada cambia entre cuadros; falta profundidad.
NO CUENTAN (los pone el sistema y no se pueden cambiar): el rótulo de arriba, las etiquetas en cápsula de abajo y la cifra
grande; tampoco opines de la cámara (tiene deriva y zoom que no se ven en cuadros sueltos).
En "problemas" da instrucciones CONCRETAS para el programador (qué mover, agrandar, añadir o quitar, citando el cuadro)."""
        r = self._ia(texto, imagenes=cuadros, esquema=esquema, temperatura=0.2)
        return int(r.get("nota", 0)), [str(x) for x in r.get("problemas", [])][:8], r.get("bien", "")

    # ------------------------------------------------------------------ una parte completa
    def parte(self, e, plan, otros):
        eid = e["id"]
        nombre = "Toma_" + re.sub(r"\W", "_", eid)
        hist, mejor = [], None
        codigo = None
        vueltas_visuales = 0
        for llamada in range(1, MAX_LLAMADAS_CODIGO + 1):
            try:
                if codigo is None:
                    self.avisar(f"{eid}: escribiendo la toma")
                    codigo = self.programar(e, plan, nombre, otros)
                prob = revisar_codigo(codigo, nombre)
                if prob:
                    hist.append(dict(v=llamada, fase="codigo", problemas=prob))
                    self.avisar(f"{eid}: el código no pasa la revisión, corrigiendo")
                    codigo = self.arreglar(e, plan, nombre, codigo, "\n".join(prob))
                    continue
                self.avisar(f"{eid}: probando la versión {llamada}")
                r, sal = self.probar(eid, nombre, codigo, llamada)
                if r.get("error"):
                    hist.append(dict(v=llamada, fase="prueba", error=r["error"][:600]))
                    self.avisar(f"{eid}: falló al dibujar, corrigiendo")
                    codigo = self.arreglar(e, plan, nombre, codigo, r["error"])
                    continue
                cuadros = [os.path.join(sal, c["archivo"]) for c in r["cuadros"]]
                medidos = self.problemas_medidos(r)
                self.avisar(f"{eid}: revisando los cuadros con visión")
                nota, vistos, bien = self.juzgar(e, plan, cuadros)
                puntaje = nota - (1 if medidos else 0)
                hist.append(dict(v=llamada, fase="juez", nota=nota, problemas=medidos + vistos, bien=bien))
                if mejor is None or puntaje > mejor["puntaje"]:
                    mejor = dict(puntaje=puntaje, nota=nota, codigo=codigo, cuadros=cuadros, version=llamada)
                if puntaje >= NOTA_OK or vueltas_visuales >= MAX_VUELTAS_VISUALES:
                    break
                vueltas_visuales += 1
                self.avisar(f"{eid}: nota {nota}/10, mejorando lo que se ve mal")
                codigo = self.corregir(e, plan, nombre, codigo, medidos + vistos, cuadros)
            except Exception as ex:                     # un fallo de la IA no tumba las demás partes
                hist.append(dict(v=llamada, fase="ia", error=str(ex)[:300]))
                if codigo is None or "cuota" in str(ex) or "API key" in str(ex):
                    break
        return dict(id=eid, nombre=nombre, mejor=mejor, historial=hist)

    # ------------------------------------------------------------------ todo
    def correr(self, solo=None):
        t_ini = time.time()
        os.makedirs(self.dir, exist_ok=True)
        escenas = self.p["escenas"]
        partes = [e for k, e in enumerate(escenas) if 0 < k < len(escenas) - 1 and (not solo or e["id"] in solo)]
        if not partes:
            return dict(ok=False, motivo="no hay partes intermedias")
        ruta_tl = os.path.join(self.carpeta, "timeline.json")
        tl_temporal = not os.path.exists(ruta_tl)
        if tl_temporal:                                # timeline estimado compartido por todas las pruebas
            import trabajos as T
            codigo_tl = ("import json, muestra_estilo as M; json.dump(M.timeline_provisional(), "
                         "open('timeline.json', 'w', encoding='utf-8'), ensure_ascii=False)")
            subprocess.run([sys.executable, "-c", codigo_tl], cwd=self.carpeta, env=T.entorno(self.carpeta),
                           capture_output=True, timeout=60, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            _ = self.sistema                           # el manual, una vez (antes de los hilos)
            self.avisar("Director: diseñando un mundo visual para cada parte")
            planes = self.dirigir(partes)
            otros = {e["id"]: planes.get(e["id"], {}).get("mundo", "") for e in partes}
            with cf.ThreadPoolExecutor(max_workers=self.procs) as ex:
                futs = [ex.submit(self.parte, e, planes.get(e["id"], {}),
                                  "; ".join(v for k, v in otros.items() if k != e["id"])) for e in partes]
                resultados = [f.result() for f in futs]
        finally:
            if tl_temporal and os.path.exists(ruta_tl):
                os.remove(ruta_tl)
        aceptadas = {}
        for r, e in zip(resultados, partes):
            if r["mejor"]:
                aceptadas[e["id"]] = (r["nombre"], r["mejor"]["codigo"], _firma_parte(e["frases"]))
        destino = os.path.join(self.carpeta, "tomas_ia.py")
        if aceptadas:
            with open(destino, "w", encoding="utf-8") as f:
                f.write(_modulo(aceptadas))
        elif os.path.exists(destino):
            os.remove(destino)
        informe = dict(fecha=time.strftime("%Y-%m-%d %H:%M"), segundos=round(time.time() - t_ini),
                       modelo_codigo=self.modelo_codigo, modelo_guion=self.modelo_guion, uso=self.uso, planes=planes,
                       partes=[dict(id=r["id"], nota=(r["mejor"] or {}).get("nota"), version=(r["mejor"] or {}).get("version"),
                                    plantilla=not r["mejor"], historial=r["historial"],
                                    cuadros=[os.path.relpath(c, self.carpeta) for c in (r["mejor"] or {}).get("cuadros", [])])
                               for r in resultados])
        with open(os.path.join(self.dir, "informe.json"), "w", encoding="utf-8") as f:
            json.dump(informe, f, ensure_ascii=False, indent=1)
        self._hoja(resultados)
        n_ok = len(aceptadas)
        self.avisar(f"Tomas creativas: {n_ok} de {len(partes)} listas ({informe['segundos']} s, {self.uso['llamadas']} llamadas)")
        return dict(ok=n_ok > 0, informe=informe)

    def _hoja(self, resultados):
        """Hoja de contacto: una fila por parte con los cuadros de la versión elegida."""
        try:
            import cv2
            import numpy as np
            filas = []
            for r in resultados:
                cs = (r["mejor"] or {}).get("cuadros", [])
                ims = [cv2.imread(c) for c in cs if os.path.exists(c)]
                ims = [cv2.resize(i, (384, int(i.shape[0] * 384 / i.shape[1]))) for i in ims if i is not None]
                if not ims:
                    continue
                while len(ims) < 5:
                    ims.append(np.zeros_like(ims[0]))
                fila = np.hstack(ims[:5])
                cv2.putText(fila, f"{r['id']}  nota {(r['mejor'] or {}).get('nota')}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.9, (255, 255, 255), 2, cv2.LINE_AA)
                filas.append(fila)
            if filas:
                ancho = max(f.shape[1] for f in filas)
                filas = [np.pad(f, ((0, 0), (0, ancho - f.shape[1]), (0, 0))) for f in filas]
                cv2.imwrite(os.path.join(self.dir, "hoja.jpg"), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 85])
        except Exception:
            pass


def crear_tomas(carpeta, p, a, avisar=None):
    """Punto de entrada del Estudio. a = ajustes de la petición (clave, modelo, modelo_creativo opcional)."""
    if p.get("estilo") not in ESTILOS_CREATIVOS:
        return dict(ok=False, motivo="el estilo no admite tomas creativas")
    ag = Agente(carpeta, p, a["clave"], a.get("modelo"), a.get("modelo_creativo"), avisar)
    return ag.correr()


# ====================================================================== línea de comandos
def _principal():
    if sys.argv[1:] == ["--manual"]:
        sys.stdout.reconfigure(encoding="utf-8")
        temporal = not os.path.exists("timeline.json")
        if temporal:
            import muestra_estilo as M
            with open("timeline.json", "w", encoding="utf-8") as f:
                json.dump(M.timeline_provisional(), f, ensure_ascii=False)
        try:
            sys.stdout.write(manual())
        finally:
            if temporal:
                os.remove("timeline.json")
        return
    import argparse
    ap = argparse.ArgumentParser(description="Agente de tomas creativas del Estudio")
    ap.add_argument("proyecto", help="carpeta del proyecto o id dentro de la carpeta de proyectos del Estudio")
    ap.add_argument("--solo", default="", help="ids separados por comas (p2,p3)")
    ap.add_argument("--modelo", default=None, help=f"modelo para escribir código (por defecto {MODELO_CODIGO})")
    ap.add_argument("--modelo-guion", default=None)
    ap.add_argument("--clave-archivo", default=None)
    args = ap.parse_args()
    import proyecto as PR
    carpeta = args.proyecto if os.path.isdir(args.proyecto) else os.path.join(PR.PROYECTOS, args.proyecto)
    ruta_p = os.path.join(carpeta, "proyecto.json")
    if os.path.exists(ruta_p):
        with open(ruta_p, encoding="utf-8") as f:
            p = json.load(f)
    else:                                           # carpeta suelta con guion.py (pruebas)
        sys.path.insert(0, carpeta)
        import guion as g
        p = dict(titulo=g.TITULO, formato=getattr(g, "FORMATO", "horizontal"), estilo="pro_kz_plano",
                 escenas=[{k: v for k, v in e.items()} for e in g.ESCENAS])
    clave = os.environ.get("GEMINI_API_KEY", "")
    if args.clave_archivo:
        with open(args.clave_archivo, encoding="utf-8") as f:
            clave = f.read().strip()
    if not clave:
        sys.exit("Falta la key de Gemini (GEMINI_API_KEY o --clave-archivo)")
    ag = Agente(carpeta, p, clave, args.modelo_guion, args.modelo)
    r = ag.correr(solo=[s for s in args.solo.split(",") if s] or None)
    print(json.dumps(dict(ok=r.get("ok"), uso=ag.uso, partes=[(x["id"], x["nota"], x["plantilla"])
                                                              for x in r.get("informe", {}).get("partes", [])]),
                     ensure_ascii=False))


if __name__ == "__main__":
    _principal()
