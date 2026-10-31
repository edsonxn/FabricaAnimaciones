# -*- coding: utf-8 -*-
"""Prueba de voz: Johnny (ElevenLabs, HMCmDsbKeaSZp5LMOYKR), la voz de la que salió Sarcastica.mp3, con corchetes (el usuario, 30-oct-2026).
Mismas frases que el video, para compararlas con las de Chatterbox. Uso: python _generar.py"""
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import tts_eleven as E

VOICE = "HMCmDsbKeaSZp5LMOYKR"
MODELO = "eleven_v4_turbo"
PRUEBAS = {
    "1_sarcasmo_burla": "[amused] Una pausa, que nos han descubierto. [short pause] Jhon Feddis Zabala nos escribió que se nota que "
                        "Kyrim no es lo nuestro. [sarcastic] Y tiene toda la razón. [short pause] De Kyrim no sabemos nada. "
                        "[laughs softly] Nosotros solo hablamos de Skyrim.",
    "2_serio_emotivo": "[serious] En el cinco, y aquí voy a hablar en serio. [short pause] Erik el Asesino existió. [sad] Le diagnosticaron "
                       "un sarcoma de Ewing en dos mil nueve. Make-A-Wish lo llevó a Bethesda, y crearon un personaje con su nombre. "
                       "[sighs] Murió el once de mayo de dos mil once, [short pause] seis meses antes de que saliera Skyrim. "
                       "[softly] Cada vez que convences a su padre de dejarlo marchar, le das a ese chico la aventura que quería.",
    "3_tension_epico": "[tense] Y lo más fuerte lo dice él. Que hacen bien en no fiarse. Que los dragones se crearon para dominar. "
                       "[whispers] Y que no pasa un día sin sentir la tentación de volver a su naturaleza. [long pause] "
                       "[dramatic] Por eso es el número uno. Los demás secretos están escondidos en libros y en cuevas. "
                       "[excited] Este te lo dijo a la cara, en la cima del mundo. [short pause] [sarcastic] Y tú le diste las gracias.",
}
AQUI = os.path.dirname(os.path.abspath(__file__))
E._activa = [n for n, _ in E.cuentas()].index(2)   # la 1 tiene 0 créditos; Johnny está en la 1 y la 2
total = 0
for nombre, texto in PRUEBAS.items():
    ruta = os.path.join(AQUI, f"eleven_{nombre}.mp3")
    if os.path.exists(ruta):
        continue
    r = E.post(f"text-to-speech/{VOICE}?output_format=mp3_44100_128", timeout=120,
               json=dict(text=texto, model_id=MODELO, seed=7, language_code="es", voice_settings=dict(stability=0.5)))
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    open(ruta, "wb").write(r.content)
    c = int(r.headers.get("character-cost") or 0)
    total += c
    print(nombre, len(texto), "caracteres, costo", c, flush=True)
print("créditos gastados", total, "· saldos", E.saldos())
