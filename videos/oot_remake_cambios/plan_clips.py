# -*- coding: utf-8 -*-
"""Plan de clips POR BEAT de oot_remake_cambios (26-oct-2026): cada beat -> (id de YouTube, segundo) ya MIRADO en las hojas
propias (previews/_scan/*.jpg de escanear.py: DEMO, OVR, DIR, JUN) o en videos/zelda_oot/mapa_clips.md (serie ZeldaCentral
de N64 en Switch Online, marco NSO 0,131). `python plan_clips.py` escribe busquedas.json e imprime recorte_por para guion.py.
Remake = material OFICIAL de Nintendo of America; N64 = ZeldaCentral; 3DS = ZorZelda; mod de fans = Reonu.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
DEMO, OVR, DIR, JUN = "PQvD3p2yGwc", "8v8eDMh1o3g", "wuFfiTEr2yc", "r8eMoxo4ipE"
P = {1: "N6rM3KhqHIo", 2: "MJxGJpBja_w", 3: "BAnsTh2fHmU", 4: "Q53ffTZRmQk", 11: "FO9OG9QXGS4", 13: "M--gXMSdJxY",
     22: "csFvvR08QFY", 24: "quu9fmNlsGk"}
DS3, MOD = "m3ucPjOjDtk", "yAb8oPhAr4o"
NSO = 0.131


def p(n, s):
    return (P[n], s)


PLAN = {
    1: (DIR, 7),      # campo de Hyrule al amanecer, la Montaña de la Muerte
    2: (DIR, 46),     # Kokiri, ruinas, desierto: el remake en movimiento
    3: p(2, 895),     # N64: campo de Hyrule
    4: (DEMO, 56),    # Aonuma habla
    5: p(1, 38),     # N64: Link a caballo bajo la luna (sin el negro del título)
    6: p(22, 70),    # N64: Epona en el campo
    7: p(13, 980),   # N64: Link adulto despierta
    8: (DS3, 120),    # 3DS (2011): Templo del Agua
    9: (OVR, 28),    # remake: Link de cerca, el Árbol Deku
    10: (JUN, 60),    # anuncio de junio: Link dormido, luciérnagas
    11: (DEMO, 85),   # remake: Bosque Kokiri con detalle
    12: (DIR, 31),    # Epona al galope
    13: (DEMO, 862),  # Aonuma, segunda parte
    14: (OVR, 64),    # lago Hylia, cuco, rancho
    15: p(1, 380),    # N64: aldea Kokiri (contador de rupias)
    16: p(13, 465),   # N64: mercado (niño)
    17: p(4, 815),    # N64: Casa Skulltula
    18: (DEMO, 234),  # remake: tienda Kokiri (contador /200)
    19: (OVR, 262),   # amiibo Link niño y Zelda niña, 2027
    20: (OVR, 270),   # amiibo + colección
    21: p(11, 1340),  # N64: tienda de máscaras felices
    22: (OVR, 49),    # remake: Link y Navi de cerca
    23: (DEMO, 639.5),  # puente del castillo, justo antes de la carga
    24: (DEMO, 653),  # cartel «Hyrule Castle Town»
    25: (DEMO, 311),  # cartel «Deku Tree» tras la carga
    26: p(2, 1012),   # N64: campo -> mercado
    27: (OVR, 246),   # ZELDA NOTES: logo y teléfono
    28: (OVR, 252),   # ZELDA NOTES: registros, 2 000 preguntas, lugar de la imagen
    29: (OVR, 159),   # Sala de enemigos derrotados
    30: (DEMO, 760),  # remake: la ocarina con la partitura (de noche)
    31: (OVR, 167),   # Sala de enemigos, ficha del Stalchild
    32: p(3, 1010),   # N64: noche en el rancho y el campo
    33: p(2, 1030),   # N64: mercado de la Ciudadela (fondo prerrenderizado)
    34: (DEMO, 770),  # remake: de la noche al amanecer
    35: (DEMO, 721),  # remake: la plaza con luz de tarde
    36: p(4, 150),    # N64: Kakariko de día (HUD con botones C)
    37: p(24, 210),   # N64: menú de equipo (botas)
    38: p(24, 675),   # N64: menú de equipo otra vez
    39: (DEMO, 108),  # remake: inventario nuevo (16/200)
    40: (DEMO, 475),  # remake: tirachinas de las hadas
    41: p(11, 450),   # N64: Skulltula dorada
    42: (DEMO, 487),  # remake: apuntando en el Árbol Deku
    43: p(4, 710),    # N64: Kakariko de noche, Skulltula dorada
    44: (DEMO, 664),  # remake: la plaza con gente
    45: p(13, 410),   # N64: mercado
    46: p(13, 425),   # N64: mercado (fondo prerrenderizado)
    47: (DEMO, 680),  # remake: la plaza, la cámara gira
    48: (MOD, 40),    # mod de fans (Reonu): fondos en 3D
    49: (DEMO, 709),  # remake: callejón
    50: p(2, 755),    # N64: Saria en el puente, la ocarina
    51: (OVR, 37),    # remake: la Trifuerza, Ganondorf
    52: (DIR, 104),   # remake: Sheik con el arpa, Saria con la ocarina
    53: (DEMO, 325),  # remake: «Talk to Navi»
    54: p(1, 170),    # N64: el Árbol Deku habla, Navi
    55: (JUN, 22),    # anuncio de junio: el tapiz del Árbol Deku
    56: (DEMO, 594),  # remake: Threads of Time (siguiente objetivo)
    57: (DEMO, 581),  # remake: el tapiz
    58: p(3, 100),    # N64: Zelda en el patio (diálogo de texto)
    59: (DEMO, 151),  # remake: Saria con voz
    60: (OVR, 76),    # remake: Zelda, Mido
    61: (OVR, 228),   # remake: Link de cerca, su casa, el búho
    62: p(3, 835),    # N64: la Canción de Epona con los botones
    63: (DEMO, 795),  # remake: «Inputting audio…» (micrófono)
    64: (DEMO, 815),  # Aonuma toca la ocarina física
    65: (OVR, 144),   # «Play a song on an instrument» -> Canción de Epona
    66: p(2, 990),    # N64: campo de Hyrule
    67: p(11, 20),    # N64: campo (volteretas)
    68: (DEMO, 205),  # remake: avisos «Dash» y «Dive»
    69: (DEMO, 548),  # remake: corriendo por el campo
    70: (OVR, 113),   # remake: templo, agua, buceo
    71: p(13, 40),    # N64: campo (niño), cámara detrás
    72: (DEMO, 133),  # remake: la cámara gira en el bosque
    73: (DEMO, 289),  # remake: el Gran Árbol Deku
    74: (DEMO, 605),  # remake: del campo al castillo
    75: (DEMO, 263),  # remake: «Jump» en las piedras
    76: p(2, 100),    # N64: dentro del Árbol Deku (saltos automáticos)
    77: (DEMO, 183),  # remake: aviso «Jump» en el bosque
    78: (DEMO, 403),  # remake: enredaderas de la mazmorra
    79: (OVR, 101),   # remake: escalera, Templo
    80: (DEMO, 899),  # cartel del título con 11.5.2026
    81: (DIR, 58),    # remake: desierto Gerudo
    82: (DIR, 89),    # Epona y la Montaña de la Muerte
    83: (DEMO, 845),  # atardecer en el rancho con el potro
    84: (DIR, 171),   # la Espada Maestra (sin el destello)
}

if __name__ == "__main__":
    out, rec = {}, {}
    for n, (vid, s) in PLAN.items():
        k = f"scene-{n:03d}"
        out[k] = {"url": f"https://youtu.be/{vid}", "desde": s}
        if vid in P.values():
            rec[k] = NSO
        elif vid == DS3:
            rec[k] = 0.037
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats ->", "busquedas.json")
    print("recorte_por =", rec)
