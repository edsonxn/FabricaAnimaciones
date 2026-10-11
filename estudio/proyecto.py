# -*- coding: utf-8 -*-
"""Proyectos del Estudio: validan el guion (60 s máx.), lo corrigen para la voz (números en palabras, frases cortas)
y escriben guion.py + escenas.py en estudio/proyectos/<id>/ para que el pipeline normal de la Fábrica los produzca."""
import json
import os
import pprint
import re
import time
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
# Lo pesado (proyectos: voz, audio, segmentos del render, videos finales; vistas previas) vive en el disco E: (HDD USB)
# para no llenar C:. FAB_ESTUDIO_DATOS cambia el destino; si E: no está conectado se usa la carpeta del Estudio en C:.
_DESTINO = os.environ.get("FAB_ESTUDIO_DATOS", r"E:\FabricaAnimaciones\estudio")
DATOS = _DESTINO if os.path.isdir(os.path.splitdrive(_DESTINO)[0] + os.sep) else AQUI
EN_E = DATOS != AQUI
PROYECTOS = os.path.join(DATOS, "proyectos")

PALABRAS_MAX = 125            # ~2,45 palabras/s con Chatterbox -> ~52 s de voz + intro y cierre ≈ 60 s
DURACION_MAX = 66.0           # tolerancia del timeline (música y márgenes)
FRASE_MAX = 190               # caracteres (la voz falla con frases largas)

# ánimo de la música -> sabor por escena (ver nucleo/config.SABORES)
ANIMOS = {
    "auto": None,
    "alegre": ["build", "funk", "disco", "brillo", "funk", "final"],
    "epico": ["build", "epico", "epico", "reloj", "epico", "final"],
    "misterio": ["tension", "vacio", "tension", "vacio", "tension", "ambiente"],
    "tranquilo": ["ambiente", "esperanza", "lounge", "esperanza", "ambiente", "esperanza"],
    "espacial": ["espacio", "espacio", "esperanza", "espacio", "vacio", "espacio"],
    "electronico": ["build", "acid", "dub", "reloj", "acid", "final"],
}

# estilos del núcleo que funcionan con las escenas del estudio (nombre amable para la interfaz)
ESTILOS_BASE = {
    "limpio": "Plano y limpio",
    "doodle": "Garabato divertido",
    "pizarra": "Pizarra con tiza",
    "cuaderno": "Cuaderno a bolígrafo",
    "neon": "Neón nocturno",
    "recortes": "Papel recortado",
    "doodle_psicodelico": "Psicodélico",
}


def slug(s, n=40):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")[:n] or "video"


# ------------------------------------------------------------------ números en palabras (la voz los lee mejor)
_U = "cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciséis diecisiete " \
     "dieciocho diecinueve veinte veintiuno veintidós veintitrés veinticuatro veinticinco veintiséis veintisiete " \
     "veintiocho veintinueve".split()
_D = {3: "treinta", 4: "cuarenta", 5: "cincuenta", 6: "sesenta", 7: "setenta", 8: "ochenta", 9: "noventa"}
_C = {1: "ciento", 2: "doscientos", 3: "trescientos", 4: "cuatrocientos", 5: "quinientos", 6: "seiscientos",
      7: "setecientos", 8: "ochocientos", 9: "novecientos"}


def _menor_mil(n):
    if n < 30:
        return _U[n]
    if n < 100:
        d, u = divmod(n, 10)
        return _D[d] + (f" y {_U[u]}" if u else "")
    if n == 100:
        return "cien"
    c, r = divmod(n, 100)
    return _C[c] + (f" {_menor_mil(r)}" if r else "")


def numero_a_palabras(n):
    n = int(n)
    if n < 0:
        return "menos " + numero_a_palabras(-n)
    if n < 1000:
        return _menor_mil(n)
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        pre = "mil" if m == 1 else _menor_mil(m).replace("uno", "un").replace("veintiun", "veintiún") + " mil"
        return pre + (f" {_menor_mil(r)}" if r else "")
    m, r = divmod(n, 1_000_000)
    pre = "un millón" if m == 1 else numero_a_palabras(m).replace("uno", "un") + " millones"
    return pre + (f" {numero_a_palabras(r)}" if r else "")


def numeros_en_palabras(texto):
    def rep(mo):
        s = mo.group(0)
        pct = s.endswith("%")
        s = s.rstrip("%")
        if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):        # 40.000 / 40,000
            s = re.sub(r"[.,]", "", s)
        if re.fullmatch(r"\d+[.,]\d+", s):                  # decimales: 3,5 -> tres coma cinco
            a, b = re.split(r"[.,]", s)
            out = f"{numero_a_palabras(a)} coma {' '.join(_U[int(c)] for c in b)}"
        else:
            out = numero_a_palabras(s)
        return out + (" por ciento" if pct else "")
    texto = texto.replace("%", "%")
    return re.sub(r"\d[\d.,]*\d%?|\d%?", rep, texto)


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]+", "", s)


def palabras(p):
    return sum(len(f.split()) for e in p["escenas"] for f in e.get("frases", []))


def validar(p, iconos):
    """Corrige lo que se pueda y devuelve (proyecto, avisos, errores). errores = no se puede producir así."""
    avisos, errores = [], []
    p["titulo"] = (p.get("titulo") or "Mi video").strip()[:70]
    p["formato"] = "vertical" if p.get("formato") == "vertical" else "horizontal"
    esc = [e for e in p.get("escenas", []) if any(f.strip() for f in e.get("frases", []))]
    if len(esc) < 2:
        errores.append("El guion necesita al menos 2 partes con texto (inicio y cierre).")
    for i, e in enumerate(esc):
        frases = []
        for f in e.get("frases", []):
            f = re.sub(r"\s+", " ", f).strip()
            if not f:
                continue
            nf = numeros_en_palabras(f)
            if nf != f:
                avisos.append(f"Escribí los números en palabras para la voz: «{nf[:60]}…»")
            if not re.search(r"[.!?…]$", nf):
                nf += "."
            if len(nf) > FRASE_MAX:
                errores.append(f"Parte {i + 1}: una frase es demasiado larga ({len(nf)} letras; máx. {FRASE_MAX}). Pártela en dos.")
            frases.append(nf)
        e["frases"] = frases[:4]
        if len(frases) > 4:
            avisos.append(f"Parte {i + 1}: solo se usan las primeras 4 frases.")
        for k in ("icono", "icono2"):
            if e.get(k) and e[k] not in iconos:
                avisos.append(f"Parte {i + 1}: el dibujo «{e[k]}» no existe; puse una estrella.")
                e[k] = "estrella" if k == "icono" else None
        texto_norm = [_norm(w) for f in frases for w in f.split()]
        claves = []
        for c in (e.get("claves") or [])[:3]:
            pal, et = (c.get("palabra"), c.get("etiqueta")) if isinstance(c, dict) else (c[0], c[1])
            if not pal or not et:
                continue
            pal = pal.split()[0]
            if not any(w.startswith(_norm(pal)) for w in texto_norm if _norm(pal)):
                avisos.append(f"Parte {i + 1}: la etiqueta «{et}» se ancló a una palabra que no se dice; aparecerá sola.")
            claves.append([pal, str(et)[:24]])
        e["claves"] = claves
        if e.get("cifra"):
            e["cifra"] = str(e["cifra"])[:12]
        e["titulo"] = (e.get("titulo") or "")[:28]
    p["escenas"] = esc
    n = palabras(p)
    if n > PALABRAS_MAX:
        errores.append(f"El guion tiene {n} palabras; para 60 segundos el máximo es {PALABRAS_MAX}. Recórtalo.")
    p["cierre"] = (p.get("cierre") or "¿LO SABÍAS?")[:40]
    if p.get("musica") not in ANIMOS:
        p["musica"] = "auto"
    return p, avisos, errores


def escribir(carpeta, p, voz_ref, estilo_personal=None):
    """guion.py + escenas.py del proyecto (el pipeline de la Fábrica los lee como cualquier video)."""
    os.makedirs(carpeta, exist_ok=True)
    escenas = []
    for i, e in enumerate(p["escenas"]):
        d = {"id": f"p{i + 1}", "frases": e["frases"]}
        for k in ("titulo", "icono", "icono2", "cifra", "cifra_palabra"):
            if e.get(k):
                d[k] = e[k]
        if e.get("claves"):
            d["claves"] = e["claves"]
        if i == len(p["escenas"]) - 1:
            d["cierre"] = p["cierre"]
        escenas.append(d)
    animo = ANIMOS.get(p.get("musica", "auto"))
    musica = {}
    if animo:
        for i, d in enumerate(escenas):
            musica[d["id"]] = {"sabor": animo[-1] if i == len(escenas) - 1 else animo[min(i, len(animo) - 2)]}
    estilo = p.get("estilo", "limpio")
    if estilo in ESTILOS_BASE:
        base = estilo
    elif estilo in ("pro_kz_plano", "pro_kz_vertical", "pro_kz_iso", "pro_mapas", "pro_mapa_guache"):
        base = "kurzgesagt"
    elif estilo in ("pro_documental", "pro_crimen"):
        base = "documental"
    elif estilo in ("pro_guache",):
        base = "guache"
    else:
        base = (estilo_personal or {}).get("base", "limpio")
    expr = float(p.get("expresividad", 0.7))
    lineas = [
        "# -*- coding: utf-8 -*-",
        '"""Proyecto del ESTUDIO (generado por la interfaz; se reescribe al guardar)."""',
        f"TITULO = {p['titulo']!r}",
        f"ARCHIVO = {slug(p['titulo'])!r}",
        f"ESTILO_VISUAL = {base!r}",
        f"FORMATO = {p['formato']!r}",
        "DURACION = None",
        "BPM = 120",
        "SUBTITULOS = False",
        f"VOZ = dict(referencia={voz_ref.replace(os.sep, '/')!r}, idioma='es', exaggeration={expr:.2f}, "
        f"cfg_weight=0.3, temperature=0.8)",
    ]
    if estilo_personal and estilo not in ESTILOS_BASE:
        lineas.append(f"ESTILO_PERSONAL = {pprint.pformat(estilo_personal, width=110, sort_dicts=False)}")
    if musica:
        lineas.append(f"MUSICA = {pprint.pformat(musica, sort_dicts=False)}")
    lineas.append("ESCENAS = " + pprint.pformat(escenas, width=110, sort_dicts=False))
    with open(os.path.join(carpeta, "guion.py"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    if estilo in ("pro_kz_plano", "pro_kz_vertical", "pro_kz_iso", "pro_guache"):
        esc_py = ("# -*- coding: utf-8 -*-\n# Generado por el Estudio (Kurzgesagt Plano).\n"
                  "from escenas_pro_plano import *  # noqa: F401,F403\n"
                  "from escenas_pro_plano import clases_plano\n\n"
                  "CLASES = clases_plano()\n"
                  "try:                       # modo creativo: tomas escritas por el agente (agente_tomas.py)\n"
                  "    from tomas_ia import TOMAS\n"
                  "    CLASES.update(TOMAS)\n"
                  "except ImportError:\n"
                  "    pass\n")
    elif estilo in ("pro_documental", "pro_crimen"):
        esc_py = ("# -*- coding: utf-8 -*-\n# Generado por el Estudio (Documental).\n"
                  "from escenas_pro_documental import *  # noqa: F401,F403\n"
                  "from escenas_pro_documental import clases_documental\n\n"
                  "CLASES = clases_documental()\n")
    elif estilo in ("pro_mapas", "pro_mapa_guache"):
        esc_py = ("# -*- coding: utf-8 -*-\n# Generado por el Estudio (Mapas con relieve).\n"
                  "from escenas_pro_mapas import *  # noqa: F401,F403\n"
                  "from escenas_pro_mapas import clases_mapas\n\n"
                  "CLASES = clases_mapas()\n")
    else:
        esc_py = ("# -*- coding: utf-8 -*-\n# Generado por el Estudio: todas las escenas son las del estudio.\n"
                  "from escenas_estudio import *  # noqa: F401,F403\n"
                  "from escenas_estudio import clases_estudio\n\n"
                  "CLASES = clases_estudio()\n")

    with open(os.path.join(carpeta, "escenas.py"), "w", encoding="utf-8") as f:
        f.write(esc_py)


def cargar(pid):
    with open(os.path.join(PROYECTOS, pid, "proyecto.json"), encoding="utf-8") as f:
        return json.load(f)


def guardar(p):
    carpeta = os.path.join(PROYECTOS, p["id"])
    os.makedirs(carpeta, exist_ok=True)
    p["modificado"] = time.time()
    tmp = os.path.join(carpeta, "proyecto.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=1)
    os.replace(tmp, os.path.join(carpeta, "proyecto.json"))
    return p


def nuevo_id(titulo):
    base = time.strftime("%Y%m%d_%H%M%S_") + slug(titulo, 24)
    return base
