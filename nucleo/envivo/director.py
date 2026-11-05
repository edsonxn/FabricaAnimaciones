# -*- coding: utf-8 -*-
"""Director del EN VIVO: escribe un bloque (4-6 frases, ~25-40 s) y elige qué se ve en cada frase.

Cada bloque propone 2 «proximos» subtemas: el servidor los reparte entre dos guionistas que escriben en paralelo
(cada llamada cuesta ~8 s de arranque + ~3 s por frase; con uno solo la producción iba por detrás de la voz).

Llama a Claude por la línea de comandos (`claude -p`, la suscripción del usuario, sin API de pago) desde una
carpeta vacía y sin configuración (sin MCP, hooks ni CLAUDE.md): sin «pensar»: ~8 s de arranque + ~2-3 s por frase
(sonnet, por defecto desde el 4-nov-2026: 12-17 s por bloque y mejor lore que haiku).
"""
import json
import os
import re
import shutil
import subprocess
import threading
import time

AQUI = os.path.dirname(os.path.abspath(__file__))

PROMPT = """Eres el guionista EN VIVO de un directo de YouTube del canal «{canal}» ({juego}). Estilo: {estilo}.
El directo no se acaba: cada vez escribes SOLO el siguiente bloque, que se narra justo después del anterior.

TEMA ACTUAL: {tema}
{transicion}{enfoque}{chat}
LO QUE YA SE DIJO EN EL DIRECTO (PROHIBIDO repetir datos, personajes u objetos de esta lista: cada bloque trae cosas NUEVAS
del tema; continúa el hilo con lo siguiente):
{historial}

{catalogo}

Escribe el bloque siguiente en español latino:
- {n_frases} frases, cada una de 10 a 24 palabras, frases habladas y naturales (es un narrador en directo, puede hablarle al chat).
- Datos de lore REALES; si no estás seguro de un dato, no lo inventes: dilo de forma general.
- Lo que dice la voz SE VE: cada frase nombra algo concreto (personaje, lugar, objeto, criatura, planta, libro…) y lleva SU imagen.
  Usa "pegatina" con un id EXACTO de la lista si hay una que sea justo eso; si no, "buscar" es OBLIGATORIO: el título EXACTO en
  INGLÉS de la página de la wiki de {juego} (p. ej. "Nightshade (Skyrim)", "Esbern", "Blackreach"). Nunca dejes una frase sin
  "pegatina" ni "buscar", salvo el saludo. "clip" = id EXACTO de un clip de la lista si encaja con la frase, si no null.
- "etiqueta": nombre corto EN ESPAÑOL de lo que enseña la imagen (2-4 palabras, p. ej. "Madre Noche" o "Goldar · misión cortada").
- "rotulo": aviso de pantalla al estilo del canal (título corto, 2-6 palabras, p. ej. "El dragón que no puedes absorber") solo en 1 o 2
  frases del bloque (en las demás null).
- "ficha": en 1 frase del bloque (las demás null), ficha de inventario del juego con un dato REAL que dice la voz:
  {{"arriba": "categoría corta", "nombre": "nombre del objeto/persona", "texto": "dato de 8-16 palabras con **negritas** en lo clave"}}.
- Nada de corchetes, emojis ni acotaciones. El directo NO se acaba: nunca te despidas ni cierres («eso es todo por hoy»,
  «nos vemos») y no vuelvas a saludar salvo en el arranque; la última frase deja enganchado lo que viene.
- "proximos": 2 subtemas concretos (máx. 8 palabras) que seguirían a este bloque dentro del MISMO tema, distintos entre sí, con
  personajes/objetos que NO salen en este bloque ni en lo ya dicho (otros guionistas los escribirán en paralelo).
- "opciones": 3 temas cortos (máx. 6 palabras) para que el chat vote qué viene después, relacionados pero distintos.

Responde SOLO con JSON válido, sin texto antes ni después (omite las claves que irían en null):
{{"titulo": "título corto del bloque", "frases": [{{"texto": "...", "pegatina": null, "buscar": null, "clip": null, "etiqueta": null, "rotulo": null, "ficha": null, "comentario": null}}],
 "resumen": "una línea con lo que se contó", "proximos": ["...", "..."], "opciones": ["...", "...", "..."]}}"""


CHAT = """
ESTE BLOQUE CONTESTA AL CHAT EN VIVO (comentarios reales de espectadores; nunca cambies ni inventes lo que dijeron):
{lista}
- Dedica UNA frase a cada comentario: nombra a la persona («Oye, Vane…» o «@Vane pregunta…», el nombre tal cual) y
  contéstale de verdad. En esa frase pon "comentario": "<su id>" (el comentario sale en pantalla mientras lo dices) y no
  pongas pegatina ni buscar en esa frase.
- Agradecimiento: agradece con calidez y recuerda que todos los comentarios se leen y se toman en cuenta.
- Pregunta: contéstala con un dato real de lore; si no lo sabes seguro, dilo de forma general.
- NUNCA inventes lugares, objetos ni secretos para rellenar: la última frase usa algo REAL y conocido del juego.
- Crítica exagerada o sin razón: contéstala con burla disfrazada, amable por fuera y con sarcasmo por debajo, para que el
  chat se ría; búrlate del comentario, NUNCA de la persona (sin insultos ni nada personal). Crítica justa: reconócela.
- Pedido de tema: di que se toma nota y que el chat decide cada pocos minutos.
- La última frase vuelve al tema actual con naturalidad, con su imagen.
"""


def _claude():
    return shutil.which("claude") or shutil.which("claude.cmd") or "claude"


def escribir(cfg, tema, historial, catalogo, transicion_de=None, modelo="sonnet", n_frases=6, carpeta=None, vigente=None,
             enfoque=None, paralelo=(), comentarios=(), formato=None):
    trans = ""
    pedido_por = ()
    if isinstance(transicion_de, tuple):
        transicion_de, pedido_por = transicion_de
    if transicion_de:
        trans = (f"¡CAMBIO DE TEMA EN VIVO! Veníamos hablando de «{transicion_de}» y ahora toca «{tema}». "
                 "La primera frase hace el puente con naturalidad (el chat / quien dirige pidió el cambio) y luego entra de lleno al tema nuevo.\n")
    if pedido_por:
        trans += ("Este tema lo PIDIÓ EL CHAT: " + ", ".join("@" + a for a in pedido_por)
                  + ". En la primera frase nómbralos (como mucho tres) y dales las gracias por pedirlo.\n")
    enf = ""
    if enfoque:
        enf = f"ESTE BLOQUE se centra en: {enfoque}. Enlázalo con naturalidad con lo anterior (sin anunciar «ahora toca»).\n"
    if paralelo:
        enf += "EN PARALELO otros guionistas escriben los bloques sobre: " + "; ".join(paralelo) + ". NO toques esos asuntos.\n"
    if formato:                                       # p. ej. la discusión entre voces (servidor.Directo.discusion)
        enf += formato + "\n"
    chat = ""
    if comentarios:
        chat = (CHAT.format(lista="\n".join(f'- id {c["id"]} · @{c["autor"]} ({c.get("tipo") or "comentario"}): «{c["texto"]}»'
                                              for c in comentarios), n=len(comentarios)))
    prompt = PROMPT.format(canal=cfg["nombre"], juego=cfg["juego"], estilo=cfg["estilo"], tema=tema, transicion=trans,
                           historial="\n".join(f"- {h}" for h in historial[-8:]) or "- (es el arranque del directo: saluda breve y entra al tema)",
                           catalogo=catalogo, n_frases=n_frases, enfoque=enf, chat=chat)
    carpeta = carpeta or os.path.join(AQUI, "_sesiones", "_claude")
    os.makedirs(carpeta, exist_ok=True)
    mcp = os.path.join(carpeta, "mcp_vacio.json")
    if not os.path.exists(mcp):
        with open(mcp, "w") as f:
            f.write('{"mcpServers":{}}')
    cmd = [_claude(), "-p", "--model", modelo, "--strict-mcp-config", "--mcp-config", mcp,
           "--setting-sources", "", "--tools", "", "--effort", "low"]
    env = dict(os.environ, MAX_THINKING_TOKENS="0")   # sin «pensar»: de ~24 s a ~13 s por bloque, y el guion sale igual de bien
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                         encoding="utf-8", cwd=carpeta, env=env, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    salida = {}
    hilo = threading.Thread(target=lambda: salida.setdefault("txt", p.communicate(prompt)[0]), daemon=True)
    hilo.start()
    fin = time.time() + 120
    while hilo.is_alive():                      # si cambian el tema a media escritura, se corta ya (no se espera a que acabe)
        hilo.join(0.3)
        if (vigente and not vigente()) or time.time() > fin:
            p.kill()
            return None, "cancelado"
    return _json(salida.get("txt")), salida.get("txt")


def _json(txt):
    m = re.search(r"\{.*\}", txt or "", re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:
        return None
    frases = [f for f in d.get("frases", []) if isinstance(f, dict) and f.get("texto")]
    if not frases:
        return None
    d["frases"] = frases
    return d
