# -*- coding: utf-8 -*-
"""Cerebro económico del Estudio: Google Gemini (API REST, sin dependencias) escribe el guion de 60 s y elige
dibujos, etiquetas y música. La calidad es INFERIOR a la producción hecha a mano en la Fábrica (coreografía a
medida, investigación verificada): aquí el modelo solo rellena una plantilla con escenas genéricas.

La API key la pone el usuario en la interfaz (se guarda en estudio/ajustes.json, que git ignora)."""
import json
import urllib.error
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta"
# Modelos de texto vigentes (ai.google.dev/gemini-api/docs/models, revisado el 5-oct-2026). Los 2.0 están apagados y los
# 2.5 solo funcionan en proyectos antiguos. «Ver modelos de mi cuenta» en Ajustes trae la lista real de la key.
DEFECTO = "gemini-3.5-flash-lite"
SUGERIDOS = [
    ("gemini-3.5-flash-lite", "Gemini 3.5 Flash-Lite · el más barato y rápido (recomendado)"),
    ("gemini-3.1-flash-lite", "Gemini 3.1 Flash-Lite · muy barato"),
    ("gemini-3.8-flash", "Gemini 3.8 Flash · el Flash más nuevo, mejor guion, algo más caro"),
    ("gemini-3.7-flash", "Gemini 3.7 Flash · barato"),
    ("gemini-3.6-flash", "Gemini 3.6 Flash · barato"),
    ("gemini-3.5-flash", "Gemini 3.5 Flash · barato"),
    ("gemini-3.1-pro-preview", "Gemini 3.1 Pro (vista previa) · mejor calidad, más caro"),
]
VIEJOS = ("gemini-2.0", "gemini-1.")      # apagados: si estaban guardados en ajustes, se cambia al de por defecto


def _pedir(url, clave, cuerpo=None, timeout=90):
    req = urllib.request.Request(url, data=json.dumps(cuerpo).encode("utf-8") if cuerpo is not None else None,
                                 headers={"x-goog-api-key": clave, "Content-Type": "application/json"},
                                 method="POST" if cuerpo is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        try:
            msg = json.loads(ex.read().decode("utf-8")).get("error", {}).get("message", "")
        except Exception:
            msg = ""
        if ex.code in (400, 401, 403) and ("API key" in msg or "PERMISSION" in msg.upper()):
            raise RuntimeError("La API key de Gemini no es válida o no tiene permiso. Revísala en Ajustes.")
        if ex.code == 429:
            raise RuntimeError("Gemini dice que se acabó la cuota por ahora (límite gratuito o de pago). Espera un "
                               "minuto o elige otro modelo.")
        if ex.code == 404:
            raise RuntimeError("Ese modelo de Gemini no existe o ya no está disponible. Elige otro en Ajustes.")
        raise RuntimeError(f"Gemini respondió con error {ex.code}: {msg[:200]}")
    except urllib.error.URLError as ex:
        raise RuntimeError(f"No hay conexión con Gemini ({ex.reason}). Revisa tu internet.")


def modelos(clave):
    """Modelos de texto disponibles para esa key: [{id, nombre, barato}] (los «flash/lite» primero)."""
    out, token = [], None
    for _ in range(5):
        url = f"{API}/models?pageSize=200" + (f"&pageToken={token}" if token else "")
        d = _pedir(url, clave, timeout=20)
        for m in d.get("models", []):
            if "generateContent" not in m.get("supportedGenerationMethods", []):
                continue
            mid = m["name"].split("/", 1)[-1]
            bajo = mid.lower()
            if not bajo.startswith("gemini") or bajo.startswith(VIEJOS) or any(x in bajo for x in ("embedding", "image", "tts", "audio", "live",
                                                                         "vision", "robotics", "computer-use")):
                continue
            out.append(dict(id=mid, nombre=m.get("displayName", mid),
                            barato=("lite" in bajo) or ("flash" in bajo)))
        token = d.get("nextPageToken")
        if not token:
            break

    def version(b):
        import re
        v = re.match(r"gemini-(\d+)(?:\.(\d+))?", b)
        return -(int(v.group(1)) * 100 + int(v.group(2) or 0)) if v else 0

    def orden(m):                          # baratos primero y, dentro de cada grupo, los más nuevos arriba
        b = m["id"].lower()
        return (0 if "lite" in b else 1 if "flash" in b else 2, "preview" in b or "exp" in b, version(b), b)
    return sorted(out, key=orden)


ESQUEMA = {
    "type": "OBJECT",
    "properties": {
        "titulo": {"type": "STRING", "description": "Título corto y llamativo del video (máx. 50 letras)"},
        "cierre": {"type": "STRING", "description": "Frase final en pantalla, 2-4 palabras (p. ej. ¿LO SABÍAS?)"},
        "musica": {"type": "STRING", "enum": ["alegre", "epico", "misterio", "tranquilo", "espacial", "electronico"]},
        "escenas": {
            "type": "ARRAY", "minItems": 4, "maxItems": 6,
            "items": {
                "type": "OBJECT",
                "properties": {
                    "frases": {"type": "ARRAY", "items": {"type": "STRING"}, "minItems": 1, "maxItems": 3},
                    "titulo": {"type": "STRING", "description": "Rótulo de 1-3 palabras para la parte (vacío en la primera y la última)"},
                    "icono": {"type": "STRING"},
                    "icono2": {"type": "STRING", "description": "Segundo dibujo que aparece a mitad de la parte, o vacío"},
                    "claves": {"type": "ARRAY", "maxItems": 2, "items": {
                        "type": "OBJECT", "properties": {
                            "palabra": {"type": "STRING", "description": "UNA palabra que se dice literalmente en las frases"},
                            "etiqueta": {"type": "STRING", "description": "Texto en pantalla, máx. 20 letras"}},
                        "required": ["palabra", "etiqueta"]}},
                    "estampa": {"type": "STRING", "description": "Sello de archivo si es documental (p. ej. CONFIDENCIAL, CLASIFICADO)"},
                    "lugar": {"type": "STRING", "description": "Ciudad o región si es estilo mapas (p. ej. Mexico, Dolores, Madrid)"},
                    "ruta": {"type": "STRING", "description": "Segunda ciudad para trazar ruta animada en el mapa"},
                    "cifra": {"type": "STRING", "description": "Número o fecha a destacar en grande (con dígitos), o vacío"},
                    "cifra_palabra": {"type": "STRING", "description": "Palabra que se dice justo cuando debe aparecer la cifra"},
                },
                "required": ["frases", "icono"],
            },
        },
    },
    "required": ["titulo", "cierre", "musica", "escenas"],
}


def instrucciones(tema, tono, iconos, palabras_max, estilo="limpio"):
    lista_iconos = list(iconos)
    guia_estilo = ""
    if estilo in ("pro_kz_plano", "pro_kz_vertical", "pro_kz_iso"):
        extras = ["tierra", "sol", "luna", "galaxia", "planeta", "pajaro", "kuri", "microbio", "arbol", "planta", "humano", "termometro", "fumarola", "onda", "atomo", "nuclear", "solar", "molecula", "esfera"]
        lista_iconos = extras + lista_iconos
        guia_estilo = ("\n- Estilo KURZGESAGT ILUSTRADO: animaciones vectoriales limpias, ciencia, cosmos, naturaleza y tecnología. Usa elementos como tierra, sol, galaxia, microbio, pajaro, atomo cuando encajen.")
    elif estilo in ("pro_documental", "pro_crimen"):
        guia_estilo = ("\n- Estilo DOCUMENTAL DE MISTERIO / ARCHIVO: atmósfera de investigación y enigmas. En 'estampa' usa sellos como CONFIDENCIAL, CLASIFICADO, EXPEDIENTE, EVIDENCIA. Resalta fechas en 'cifra'.")
    elif estilo in ("pro_mapas", "pro_mapa_guache"):
        guia_estilo = ("\n- Estilo MAPAS CON RELIEVE REAL: historia y geografía sobre mapa 3D. Pon en 'lugar' la ciudad o país central de cada escena, y en 'ruta' la ciudad destino si hay desplazamiento.")
    return f"""Eres guionista de videos cortos animados en español (formato YouTube Shorts / TikTok / video corto).
Escribe el guion de UN video de máximo 60 segundos sobre: «{tema}».
Tono: {tono or "cercano, curioso y entretenido"}.{guia_estilo}

REGLAS (obligatorias):
- Entre 4 y 6 partes. La primera engancha con una pregunta o dato sorprendente; la última cierra con una idea memorable.
- En TOTAL entre {palabras_max - 35} y {palabras_max - 10} palabras habladas (sumando todas las frases). Nunca más de {palabras_max}.
- Frases cortas (máximo 22 palabras cada una), naturales para leer en voz alta.
- TODOS los números escritos en palabras dentro de las frases ("mil novecientos sesenta y nueve", no "1969"). Nada de siglas raras, emojis ni paréntesis.
- Datos correctos y prudentes: si no estás seguro de una cifra, no la uses.
- "icono" e "icono2" deben ser EXACTAMENTE nombres de esta lista de dibujos disponibles: {", ".join(iconos)}.
  Elige el que mejor represente la idea; si ninguno encaja, usa "estrella" o "cerebro". Varía los dibujos entre partes.
- "claves": 1 o 2 por parte (salvo la primera), con una palabra que se diga LITERALMENTE en esa parte y una etiqueta corta en mayúsculas.
- "cifra" solo cuando haya un número clave (escrito con dígitos en ese campo, p. ej. "1969" o "×5"), y "cifra_palabra" una palabra de esa parte.
- "musica": el ánimo que mejor le va al tema."""


def escribir_guion(clave, modelo, tema, tono, iconos, palabras_max=125, estilo="limpio"):
    cuerpo = {
        "contents": [{"role": "user", "parts": [{"text": instrucciones(tema, tono, iconos, palabras_max, estilo=estilo)}]}],
        "generationConfig": {"temperature": 0.8, "responseMimeType": "application/json", "responseSchema": ESQUEMA},
    }
    d = _pedir(f"{API}/models/{modelo}:generateContent", clave, cuerpo)
    try:
        partes = d["candidates"][0]["content"]["parts"]
        texto = "".join(p.get("text", "") for p in partes)
        g = json.loads(texto)
    except (KeyError, IndexError, json.JSONDecodeError):
        motivo = (d.get("promptFeedback") or {}).get("blockReason") or (d.get("candidates") or [{}])[0].get("finishReason")
        raise RuntimeError(f"Gemini no devolvió un guion válido ({motivo or 'respuesta vacía'}). Prueba otra vez o con otro modelo.")
    uso = d.get("usageMetadata", {})
    return g, dict(entrada=uso.get("promptTokenCount", 0), salida=uso.get("candidatesTokenCount", 0))


def probar(clave, modelo):
    cuerpo = {"contents": [{"role": "user", "parts": [{"text": "Responde solo: OK"}]}],
              "generationConfig": {"maxOutputTokens": 5}}
    _pedir(f"{API}/models/{modelo}:generateContent", clave, cuerpo, timeout=30)
    return True


# ------------------------------------------------------------------ estilo visual desde un prompt
def esquema_estilo(bases, fondos, paletas, letras):
    num = lambda d: {"type": "NUMBER", "description": d}
    hexa = lambda d: {"type": "STRING", "description": d + " (hex #rrggbb)"}
    return {
        "type": "OBJECT",
        "properties": {
            "nombre": {"type": "STRING", "description": "Nombre corto y bonito del estilo (máx. 24 letras)"},
            "base": {"type": "STRING", "enum": list(bases)},
            "fondo": {"type": "STRING", "enum": list(fondos)},
            "color_fondo": hexa("Color del fondo (o de arriba si es degradado)"),
            "color_fondo2": hexa("Color de abajo del degradado"),
            "paleta": {"type": "STRING", "enum": list(paletas)},
            "colores": {"type": "STRING", "enum": ["vivos", "pastel", "acuarela", "mate", "oscuro"]},
            "tinta": hexa("Color de las líneas de contorno, o cadena vacía para el del estilo base"),
            "temblor": num("Temblor del trazo 0 (recto, vectorial) a 3 (muy tembloroso, a mano)"),
            "sombra": num("Sombra de los dibujos 0 a 0.6"),
            "textura": num("Grano/textura de papel 0 a 0.08"),
            "neon": num("Brillo neón 0 a 1 (solo para estilos nocturnos/brillantes)"),
            "pegatina": {"type": "BOOLEAN", "description": "Borde blanco de pegatina alrededor de los dibujos"},
            "vineta": {"type": "BOOLEAN", "description": "Bordes de la pantalla oscurecidos"},
            "letra": {"type": "STRING", "enum": list(letras)},
            "particulas": hexa("Color de las partículas y halos que flotan (debe contrastar con el fondo)"),
        },
        "required": ["nombre", "base", "fondo", "color_fondo", "color_fondo2", "paleta", "colores", "tinta", "temblor",
                     "sombra", "textura", "neon", "pegatina", "vineta", "letra", "particulas"],
    }


def disenar_estilo(clave, modelo, descripcion, bases, fondos, paletas, letras):
    """bases/fondos/letras: dict id -> descripción amable; paletas: lista."""
    texto = f"""Eres director de arte de videos animados 2D (dibujos tipo pegatina/ilustración plana sobre un fondo).
Diseña un ESTILO VISUAL que cumpla esta descripción del usuario: «{descripcion}».
Opciones:
- base (cómo se dibujan los trazos): {json.dumps(bases, ensure_ascii=False)}
- fondo: {json.dumps(fondos, ensure_ascii=False)} («liso» usa color_fondo; «degradado» usa color_fondo y color_fondo2;
  plano/rayos/plasma/ondas/cartulina/rejilla usan la paleta: {", ".join(paletas)})
- letra de los títulos: {json.dumps(letras, ensure_ascii=False)}
Reglas: los dibujos y textos deben LEERSE bien sobre el fondo (contraste); si el fondo es oscuro usa colores «oscuro» o «vivos»
con partículas claras; si es claro, partículas blancas o de un tono suave. Sé fiel a la descripción (época, ánimo, colores)."""
    cuerpo = {"contents": [{"role": "user", "parts": [{"text": texto}]}],
              "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json",
                                   "responseSchema": esquema_estilo(bases, fondos, paletas, letras)}}
    d = _pedir(f"{API}/models/{modelo}:generateContent", clave, cuerpo)
    try:
        return json.loads("".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"]))
    except (KeyError, IndexError, json.JSONDecodeError):
        raise RuntimeError("Gemini no devolvió un estilo válido. Prueba otra vez o con otras palabras.")


def elegir_estilo(clave, modelo, tema, estilos):
    """estilos: dict id -> descripción. Devuelve el id que mejor le va al tema."""
    cuerpo = {"contents": [{"role": "user", "parts": [{"text":
              f"Elige el estilo visual que mejor le va a un video corto sobre «{tema}». Opciones: "
              f"{json.dumps(estilos, ensure_ascii=False)}"}]}],
              "generationConfig": {"temperature": 0.3, "responseMimeType": "application/json",
                                   "responseSchema": {"type": "OBJECT", "properties": {
                                       "estilo": {"type": "STRING", "enum": list(estilos)}}, "required": ["estilo"]}}}
    try:
        d = _pedir(f"{API}/models/{modelo}:generateContent", clave, cuerpo, timeout=40)
        e = json.loads("".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"]))["estilo"]
        return e if e in estilos else None
    except Exception:
        return None


def generar(clave, modelo, texto, sistema=None, imagenes=(), esquema=None, temperatura=0.7, timeout=240):
    """Llamada general (la usa el agente de tomas): texto + imágenes JPG opcionales -> (texto, uso).
    Con `esquema` devuelve JSON ya decodificado."""
    import base64
    partes = [{"text": texto}]
    for ruta in imagenes or ():
        with open(ruta, "rb") as f:
            partes.append({"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(f.read()).decode("ascii")}})
    cfg = {"temperature": temperatura}
    if esquema:
        cfg.update(responseMimeType="application/json", responseSchema=esquema)
    cuerpo = {"contents": [{"role": "user", "parts": partes}], "generationConfig": cfg}
    if sistema:
        cuerpo["systemInstruction"] = {"parts": [{"text": sistema}]}
    d = _pedir(f"{API}/models/{modelo}:generateContent", clave, cuerpo, timeout=timeout)
    try:
        salida = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
    except (KeyError, IndexError):
        motivo = (d.get("promptFeedback") or {}).get("blockReason") or (d.get("candidates") or [{}])[0].get("finishReason")
        raise RuntimeError(f"Gemini no devolvió respuesta ({motivo or 'vacía'})")
    uso = d.get("usageMetadata", {})
    uso = dict(entrada=uso.get("promptTokenCount", 0), salida=uso.get("candidatesTokenCount", 0))
    if esquema:
        try:
            return json.loads(salida), uso
        except json.JSONDecodeError:
            raise RuntimeError("Gemini devolvió un JSON roto")
    return salida, uso
