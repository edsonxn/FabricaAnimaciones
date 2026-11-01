# -*- coding: utf-8 -*-
"""Capa de EFECTOS del piloto «La muerta en el altar» (SIN voz: anclas en segundos; los clips traen su propio diálogo).
Beats: s1 0-8 foto · s2 8-18 rezo · s3 18-26 patio · s4 26-36 seguro · s5 36-44 anillo · s6 44-54 frenos ·
s7 54-64 Sofi · s8 64-74 dibujo · s9 74-84 la muerta vuelve · s10 84-96 «me voy a quedar» + celular.
  python fab.py novela_altar fx --seco   ·   python fab.py novela_altar fx   ·   python fab.py novela_altar fx hoja
"""

CAMARA = {}
FUNDIDO = {}
FX = [
    dict(tipo="abre", en=0, dur=.6),
    dict(tipo="temblor", en=77.1, amp=16),                       # ráfaga: las velas se apagan
    dict(tipo="oscurecer", de=94.0, a=99.0, k=.55),              # fondo para el rótulo del capítulo 2
]
ROTULOS = [
    dict(texto="LA MUERTA", en=0.4, a=3.4, tam=118, color="crema", caja="tinta", y=.08),
    dict(texto="EN EL ALTAR", en=0.4, a=3.4, tam=118, color="crema", caja="tinta", y=.15),
    dict(texto="Capítulo 1", en=0.7, a=3.4, tam=66, color="naranja", y=.22),
    dict(texto="«¿Ya confirmaste que no sobrevivió?»", en=91.6, a=94.0, tam=54, color="blanco", caja="tinta", y=.80),
    dict(texto="Capítulo 2:", en=94.2, a=99.0, tam=86, color="naranja", y=.42),
    dict(texto="¿Quién cortó los frenos?", en=94.5, a=99.0, tam=84, color="crema", y=.50),
]
PALETA = {"naranja": (255, 140, 26)}
SFX = {
    "latido": ("Slow heavy human heartbeat, low and muffled, tense, cinematic", 8),
    "sting": ("Classic Mexican telenovela dramatic reveal sting: short orchestral hit with timpani and strings, dun dun dun", 3),
    "frenos": ("Car brake pedal pumping uselessly then tires screeching on a mountain curve at night", 4),
    "papel": ("A sheet of paper being crumpled angrily in a fist, close", 1.5),
    "viento_velas": ("Sudden strong gust of wind whooshing through a room and blowing out many candles at once", 2.5),
    "copa": ("A wine glass falling and shattering on a tile floor", 1.5),
    "ding": ("Smartphone text message notification sound, single soft ding in a silent room", 1),
}
PISTAS = [
    dict(sfx="latido", de=0.3, a=8.0, vol=.55),
    dict(sfx="sting", en=7.2, vol=.6),
    dict(sfx="frenos", en=49.3, vol=.55),
    dict(sfx="papel", en=65.6, vol=.7),
    dict(sfx="viento_velas", en=76.9, vol=.75),
    dict(sfx="copa", en=78.8, vol=.6),
    dict(sfx="sting", en=79.6, vol=.7),
    dict(sfx="ding", en=91.4, vol=.8),
    dict(sfx="sting", en=94.1, vol=.75),
]
