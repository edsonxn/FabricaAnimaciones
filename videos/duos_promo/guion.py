# -*- coding: utf-8 -*-
"""Anuncio vertical de Los Duos (grupo musical: tecladista y dos voces) para Facebook/Instagram Reels y estados de WhatsApp.

Estilo: VIDEOS REALES del grupo (4 clips de celular de fiestas, mejorados: escala 1080x1920, color cálido, grano fino) con
motion graphics propios dibujados por código en la identidad de su póster: negro + DORADO, logo «Los Duos» en cursiva dorada,
píldoras de colores por género, luces de escenario (bokeh) y destellos. Kit propio `duos.py`; escenas en `escenas.py`
(plano secuencia con tiempo global). Mapa de la zona con relieve real (ETOPO1). Música: popurrí de tramos de las 4 canciones
grabadas por el propio grupo (audio/musica.wav, `musica_popurri.py`), nada de Lyria. Sin subtítulos quemados.
"""

TITULO = "Los Duos — música en vivo para tu fiesta"
ARCHIVO = "los_duos_anuncio"
FORMATO = "vertical"     # 1080x1920
ESTILO_VISUAL = "documental"     # motion graphics propios por código sobre video real
DURACION = None          # natural: ~56 s de voz + 3 pausas de solo música (~85 s), pedido del usuario el 22-oct-2026
BPM = 480                # NO es el tempo real: cuantiza los cambios de escena a 0,5 s (la música no usa el BPM)
GAP = 0.14
SUBTITULOS = False
TRANSICIONES = [("continua", 0.04)] * 7    # plano secuencia: los cambios (empujón + destello) los dibuja escenas.py
MEZCLA = dict(musica=-18.0, fx=-15.0)    # la música del grupo se luce más que en un video normal
# Locutor elegido por el usuario el 22-oct-2026 entre 6 muestras: Zabra (radio comercial mexicana)
VOZ = dict(motor="elevenlabs", voice_id="9XaoraKgpXhItOQktYsV", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5,
           referencia="E:/FabricaAnimaciones/videos/duos_promo/material/muestras_voz/2_Zabra_radio_comercial_mexicano.mp3")
CER_MAX_POR_FRASE = {"contacto_0": 0.40}   # Whisper escribe el teléfono en cifras (449-306-5431): lectura correcta

# Datos del cliente (Facebook «Grupo Los Duos», 22-oct-2026): se vende como TECLADISTA Y DOS VOCES; 1 200 MXN la hora
# (no hay mínimo, pero el usuario pidió no decirlo);
# WhatsApp 449 306 5431; lema «Música que alegra tus momentos»; zona: Aguascalientes y sus municipios (Juchipila se quitó
# el 22-oct a pedido del usuario). ElevenLabs: escritura normal; el teléfono va en grupos
# como lo dice un locutor (en pantalla, en cifras).
# PAUSAS DE SOLO MÚSICA (el usuario, 22-oct-2026: «el narrador habla y deja huecos de 7-10 s de solo música para que el
# cliente la escuche»): al terminar la escena, una frase CANTADA completa de una pieza del grupo (pieza, desde, hasta en s;
# frases ubicadas con Whisper sobre la pista de voces de Demucs). Las usan musica_popurri.py y escenas.py.
PAUSA = {
    "grupo": ("A2", 101.40, 110.40),      # balada: «pues muy adentro se quedó como una luz que nunca se apagó»
    "generos": ("A1", 43.60, 54.00),      # La indita: «yo le di mi amor a cambio de su cariño, por eso los indios…»
    "eventos": ("A4", 30.30, 40.20),      # «Mis ojos me denuncian al saber que tu amor me está olvidando…»
}
ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "[excited] ¿Tienes boda, quince años o cumpleaños? [short pause] ¡Ponle música en vivo!",
    ]},
    {"id": "grupo", "post": PAUSA["grupo"][2] - PAUSA["grupo"][1] + 0.35, "frases": [
        "Llegan Los Duos: tecladista y dos voces, listos para que nadie se quede sentado.",
    ]},
    {"id": "generos", "post": PAUSA["generos"][2] - PAUSA["generos"][1] + 0.35, "frases": [
        "Cumbias, norteño, zapateado, banda... grupera, baladas, mariachi ¡y hasta rock!",
    ]},
    {"id": "eventos", "post": PAUSA["eventos"][2] - PAUSA["eventos"][1] + 0.35, "frases": [
        "Fiestas, reuniones familiares, eventos privados... [short pause] ellos ponen el ambiente.",
    ]},
    {"id": "zona", "frases": [
        "Tocan en todo Aguascalientes y sus municipios... [short pause] ¡llegan hasta tu fiesta!",
    ]},
    {"id": "precio", "frases": [
        "¿Y el precio? [short pause] [excited] ¡A solo mil doscientos pesos la hora!",
    ]},
    {"id": "contacto", "frases": [
        "Aparta tu fecha por WhatsApp: [short pause] cuatro, cuatro, nueve... tres, cero, seis... cincuenta y cuatro, treinta y uno.",
    ]},
    {"id": "cierre", "post": 5.0, "frases": [   # al final, 5 s del grupo cantando «Es tu amor…»
        "[warmly] Los Duos... [short pause] música que alegra tus momentos.",
    ]},
]
