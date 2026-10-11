# -*- coding: utf-8 -*-
"""Capa de efectos de «Batman vs. el Guasón (animación fumada)». Formato y tipos: nucleo/secuencia_fx.py.
Las anclas de texto copian palabras del audio tal como quedaron en voz/transcripcion.json.
  python fab.py guason_fumado fx --seco    lista cada efecto con su segundo
  python fab.py guason_fumado fx           genera los SFX que falten (ElevenLabs) y arma audio/fx.wav
  python fab.py guason_fumado fx hoja      previews/fx_NN.jpg
"""

CAMARA = {
    "scene-006": dict(a=(1.0, 0, 0), b=(1.28, 0, -.2)),      # la cara furiosa se viene encima
    "scene-027": dict(a=(1.0, 0, 0), b=(1.3, 0, 0)),         # hipnosis
    "scene-042": dict(a=(1.05, 0, 0), b=(1.3, 0, -.3)),
    "scene-045": dict(a=(1.3, 0, -.4), b=(1.02, 0, 0)),      # se abre de golpe desde los ojos
    "scene-056": dict(a=(1.25, 0, .6), b=(1.0, 0, 0)),       # de Murci arrodillado al cielo
}

FX = [
    dict(tipo="abre", en=0, dur=.4),
    dict(tipo="temblor", en=.05, amp=20),
    dict(tipo="temblor", en="Dime", amp=16),
    dict(tipo="latido", beat="scene-006", bpm=150, fuerza=.25),
    dict(tipo="temblor", en="Guasón#2", amp=42, dur=.6),
    dict(tipo="destello", en="Guasón#2", fuerza=.6),
    dict(tipo="zoom", en="También secuestraste", cuanto=.22, entra=.18),
    dict(tipo="temblor", en="También secuestraste", amp=24),
    dict(tipo="desaturar", beat="scene-010", k=.6),
    dict(tipo="temblor", en=("regresar", .25), amp=38, dur=.5),
    dict(tipo="destello", en=("regresar", .25), fuerza=.5),
    dict(tipo="tinte", beat="scene-017", color="rojo", k=.3),
    dict(tipo="vineta", beat="scene-017", color="noche", fuerza=.5),
    dict(tipo="temblor", en="asesinarte", amp=48, dur=.6),
    dict(tipo="destello", en="asesinarte", fuerza=.8),
    dict(tipo="vineta", beat="scene-027", color=(120, 30, 200), fuerza=.45),
    dict(tipo="temblor", en="Una gran explosión", amp=70, dur=1.1),
    dict(tipo="destello", en="Una gran explosión", fuerza=1.0, dur=.35),
    dict(tipo="zoom", en="Una gran explosión", cuanto=.18, entra=.15),
    dict(tipo="temblor", en="Qué rayos", amp=22),
    dict(tipo="temblor", en="Controlaste", amp=30, dur=.5),
    dict(tipo="vineta", de="Controlaste", a="scene-036", color="rojo", fuerza=.35, entra=.3),
    dict(tipo="latido", beat="scene-042", bpm=160, fuerza=.3),
    dict(tipo="temblor", en="No le atravieses", amp=26),
    dict(tipo="oscurecer", beat="scene-044", k=.25, entra=.6),
    dict(tipo="destello", en="scene-045", fuerza=.9, dur=.3),
    dict(tipo="temblor", en="scene-045", amp=55, dur=.7),
    dict(tipo="desaturar", de="Eso no era", a="scene-046:fin", k=.7, entra=.15),
    dict(tipo="tinte", beat="scene-050", color=(255, 235, 170), k=.3),
    dict(tipo="temblor", en="mis ojos", amp=36, dur=.6),
    dict(tipo="tinte", beat="scene-054", color="rojo", k=.2),
    dict(tipo="temblor", en="levanta", amp=20),
    dict(tipo="cierra", en=178.9, dur=1.0),
]

ROTULOS = [
    dict(texto="¡BOOM!", en="Una gran explosión", a=("Una gran explosión", 1.6), tam=260, color="amarillo", y=.22),
    dict(texto="CENSURADO", en=("scene-045", .15), tam=120, color="amarillo", caja="tinta", y=.86),
    dict(texto="FIN (por suerte)", en=177.4, a=180.0, tam=90, color="amarillo", caja="tinta", y=.9),
]

SFX = {
    "musica_boba": ("Goofy sneaky cartoon comedy underscore, pizzicato strings, tuba and bassoon, silly and bouncy, loopable, no drums", 22),
    "musica_caos": ("Frantic silly cartoon chase music, fast xylophone and brass, chaotic and funny, loopable", 22),
    "dun_dun": ("Dramatic dun dun dun orchestral sting, exaggerated soap opera reveal", 3),
    "grillos": ("Awkward silence with crickets chirping at night", 3),
    "basura": ("Metal trash can lid clanging and garbage falling, comedic", 2),
    "pedorreta": ("Long wet cartoon raspberry tongue blowing sound, comedic", 1.5),
    "patada": ("Cartoon kick impact followed by a long slide whistle going up as something flies away", 2.5),
    "maligno": ("Short evil organ sting with thunder, cheesy horror movie", 3),
    "fanfarria": ("Short cheesy heroic brass fanfare, slightly out of tune, comedic", 3),
    "cuerda": ("Cartoon rope stretching and creaking then a boing spring", 2),
    "tada": ("Cheesy magician ta-da fanfare with cymbal", 2),
    "mazazo": ("Huge cartoon wooden mallet bonk on a head followed by tweeting birds", 3),
    "hipnosis": ("Wobbly spooky theremin hypnosis sound, cartoon", 4),
    "explosion": ("Massive cartoon explosion with debris falling and a long rumble", 5),
    "boing": ("Single cartoon boing spring jump", 1),
    "llegada": ("Powerful superhero landing whoosh and heavy impact with a low rumble", 3),
    "whoosh": ("Fast cartoon arm swing whoosh", 1),
    "pop": ("Loud comedic cork pop followed by a slide whistle going up fast", 1.5),
    "scratch": ("Vinyl record scratch, music stops abruptly", 1.5),
    "vomito": ("Cartoon retching and splashing into a metal bucket, comedic", 2.5),
    "coro": ("Angelic heavenly choir singing a single bright chord, shimmering", 4),
    "trombon": ("Sad trombone wah wah wah fail sound", 3),
    "frito": ("Sizzling frying sound with a short hiss of steam", 2),
}

PISTAS = [
    dict(sfx="musica_boba", de=0, a=("explosivo|fin", .2), vol=.16),
    dict(sfx="dun_dun", en="También secuestraste", vol=.45),
    dict(sfx="grillos", en=("secuestraste a Robin|fin", .3), a="Lo dices", vol=.5, bucle=False),
    dict(sfx="basura", en="basurero", vol=.5),
    dict(sfx="pedorreta", en=("convencer|fin", .1), vol=.7),
    dict(sfx="patada", en=("regresar", .15), vol=.6),
    dict(sfx="maligno", en="del inframundo", vol=.45),
    dict(sfx="fanfarria", en="Voy a tener", vol=.3),
    dict(sfx="cuerda", en="Aquí colgado", vol=.5),
    dict(sfx="tada", en=("desatarme|fin", .1), vol=.4),
    dict(sfx="mazazo", en=("asesinarte", -.1), vol=.7),
    dict(sfx="hipnosis", en="Yo solamente", vol=.3),
    dict(sfx="explosion", en=("Una gran explosión", -.1), vol=.9),
    dict(sfx="boing", en="Qué rayos", vol=.5),
    dict(sfx="musica_caos", de="Joker!", a=("scene-045", -.1), vol=.14),
    dict(sfx="llegada", en=("Controlaste", -.3), vol=.6),
    dict(sfx="dun_dun", en=("Superman", .4), vol=.4),
    dict(sfx="whoosh", en="No le atravieses", vol=.6),
    dict(sfx="pop", en=("scene-045", -.05), vol=.8),
    dict(sfx="scratch", en=("scene-045", -.15), vol=.6),
    dict(sfx="grillos", en=("guión|fin", .2), a="scene-047", vol=.5, bucle=False),
    dict(sfx="vomito", en="el ahorcado", vol=.5),
    dict(sfx="coro", en="Eras el caballero", vol=.4),
    dict(sfx="scratch", en="del homo", vol=.5),
    dict(sfx="frito", en="mis ojos", vol=.6),
    dict(sfx="musica_caos", de="mis ojos|fin", a=178.0, vol=.14),
    dict(sfx="trombon", en=177.2, vol=.6),
]
