# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «La heredera del rancho» cap. 1 (SIN voz: anclas en segundos; los clips traen su propio diálogo).
Beats: s1 0-8 cachetada · s2 8-18 testamento · s3 18-28 «a Guadalupe Ríos» · s4 28-36 Valeria/Rodrigo · s5 36-46 Leonor ·
s6 46-56 impugnar · s7 56-66 condición · s8 66-74 maleta · s9 74-84 flashback · s10 84-94 chimenea · s11 94-104 carta ·
s12 104-112 «ya lo sabe» · s13 112-126 «me quedo» + rótulo del capítulo 2.
  python fab.py heredera_rancho fx --seco   ·   python fab.py heredera_rancho fx   ·   python fab.py heredera_rancho fx hoja
"""

CAMARA = {}
FUNDIDO = {}
FX = [
    dict(tipo="abre", en=0, dur=.6),
    dict(tipo="oscurecer", de=121.6, a=126.0, k=.6),             # fondo para el rótulo del capítulo 2
]
ROTULOS = [
    dict(texto="LA HEREDERA", en=0.3, a=3.2, tam=112, color="crema", caja="tinta", y=.08),
    dict(texto="DEL RANCHO", en=0.3, a=3.2, tam=112, color="crema", caja="tinta", y=.15),
    dict(texto="Capítulo 1", en=0.6, a=3.2, tam=66, color="dorado", y=.22),
    dict(texto="Capítulo 2:", en=122.0, a=126.0, tam=86, color="dorado", y=.42),
    dict(texto="¿Qué le pasó a Carmen?", en=122.3, a=126.0, tam=80, color="crema", y=.50),
]
PALETA = {"dorado": (232, 178, 64)}
# Descripciones nuevas (no las de novela_altar): la página no debe oír los mismos efectos en cada capítulo.
SFX = {
    "campanas": ("Distant small-town church bell tolling slowly for a funeral, outdoors, melancholic", 6),
    "revelacion": ("Dramatic telenovela reveal hit: deep orchestral string stab with a low piano chord and cymbal swell", 3),
    "corazon": ("Muffled anxious heartbeat, slow and heavy, with a faint low room tone, suspense", 8),
    "golpe_final": ("Big cinematic soap opera cliffhanger hit: timpani and full strings, three descending notes", 4),
}
PISTAS = [
    dict(sfx="campanas", de=0.0, a=6.0, vol=.35),
    dict(sfx="revelacion", en=24.3, vol=.6),
    dict(sfx="revelacion", en=103.3, vol=.6),
    dict(sfx="corazon", de=104.2, a=111.8, vol=.5),
    dict(sfx="golpe_final", en=121.8, vol=.7),
]
