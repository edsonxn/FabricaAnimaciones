# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «La heredera del rancho» cap. 2 (SIN voz: anclas en segundos; los clips traen su propio diálogo).
Beats: s1 0-8 mandil · s2 8-18 Chela · s3 18-28 el sobre · s4 28-36 Valeria · s5 36-46 candado · s6 46-56 maleta ·
s7 56-66 flashback de Carmen · s8 66-74 la ventana · s9 74-84 Rodrigo · s10 84-94 la llave · s11 94-104 la tumba ·
s12 104-112 Leonor en la puerta · s13 112-122 «¿Entonces quién?» + rótulo del capítulo 3 (122-126).
  python fab.py heredera_cap2 fx --seco   ·   python fab.py heredera_cap2 fx   ·   python fab.py heredera_cap2 fx hoja
"""

CAMARA = {}
FUNDIDO = {}
FX = [
    dict(tipo="abre", en=0, dur=.6),
    dict(tipo="oscurecer", de=121.6, a=126.0, k=.6),             # fondo para el rótulo del capítulo 3
]
ROTULOS = [
    dict(texto="LA HEREDERA", en=0.3, a=3.2, tam=112, color="crema", caja="tinta", y=.08),
    dict(texto="DEL RANCHO", en=0.3, a=3.2, tam=112, color="crema", caja="tinta", y=.15),
    dict(texto="Capítulo 2", en=0.6, a=3.2, tam=66, color="dorado", y=.22),
    dict(texto="Capítulo 3:", en=122.0, a=126.0, tam=86, color="dorado", y=.42),
    dict(texto="¿Quién está en la tumba?", en=122.3, a=126.0, tam=76, color="crema", y=.50),
]
PALETA = {"dorado": (232, 178, 64)}
# Descripciones nuevas (ni las del cap. 1 ni las de novela_altar): la página no debe oír los mismos efectos en cada capítulo.
SFX = {
    "gallo": ("A rooster crowing at dawn on a Mexican ranch, distant, with morning birds and a far dog bark", 5),
    "viento": ("Cold night wind whistling through old stone corridors and wooden shutters, eerie and hollow", 10),
    "trueno": ("A distant rolling thunder at night over the countryside, low and ominous", 5),
    "campana": ("A single slow church bell toll inside a small stone chapel at night, long reverberating tail", 6),
    "sting_final": ("Telenovela shock cliffhanger: a sharp rising violin tremolo that slams into a deep brass and "
                    "timpani hit, then a long low decay", 5),
}
PISTAS = [
    dict(sfx="gallo", de=0.0, a=5.0, vol=.3),
    dict(sfx="trueno", en=66.2, vol=.45),
    dict(sfx="viento", de=66.0, a=84.0, vol=.25),
    dict(sfx="campana", en=94.2, vol=.4),
    dict(sfx="sting_final", en=121.6, vol=.7),
]
