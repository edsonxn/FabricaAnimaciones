# -*- coding: utf-8 -*-
"""Short vertical de Crónicas de Tamriel: compilación de los momentos más graciosos de «Jugando Skyrim con IA»
(la serie de Embry, Mantella). Sin voz nueva: el audio es el de los episodios. El montaje vive en montar.py."""

TITULO = "Le di IA a los NPC de Skyrim y me humillaron 💀 #Shorts"
CANAL = "cronicas_tamriel"
FORMATO = "vertical"
ESTILO_VISUAL = "compilacion_vertical"

# SFX de edición meme (biblioteca primero, ElevenLabs si no hay); bip de censura sintetizado en montar.py
SFX_ELEVEN = {
    "boom": dict(prompt="Deep meme bass boom hit, single punchy cinematic thud with short reverb, comedic", seg=1.5, variantes=2, bib=False),
    "scratch": dict(prompt="Vinyl record scratch, music stops abruptly, comedic", seg=1.0),
    "whoosh": dict(prompt="Fast short swoosh transition, air whip, quick", seg=0.6, variantes=3),
    "ding": dict(prompt="Bright cartoon ding bell, single hit, comedic realization", seg=1.0, bib=False),
    "risas": dict(prompt="Small studio audience laughing for two seconds, sitcom laugh track, warm", seg=2.5),
    "bruh": dict(prompt="Comedic low cartoon trombone wah wah fail sound, sad short", seg=2.0),
}

ESCENAS = []   # sin voz ni escenas del motor: el montaje es montar.py
SIN_VOZ = True

