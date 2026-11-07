# -*- coding: utf-8 -*-
"""Plan de clips POR BEAT de oot_remake_eliminado (6-nov-2026): cada beat -> (id de YouTube, segundo) MIRADO en hojas de
contacto propias a 360p (un cuadro cada 1-16 s con el segundo impreso) o ya verificado en oot_remake_cambios / zelda_oot.
`python plan_clips.py` escribe busquedas.json e imprime recorte_por y ambiente_por para pegarlos en guion.py (SECUENCIA).

Fuentes (todas >= 720p):
  REMAKE  RM100 = oLHiQX2wxrE (100 % 4K sin comentario, capitulos), EUR = QaJbU5MrPw4 (Eurogamer Espana, 1080p: comparativa con
          clips N64 y menus del remake), KAE = 4dsfMqNJ_xI (Kaepora, 4K), B5 = b5Zg52U0aE4 (todas las escenas de Ganondorf),
          DEMO / OVR / DIR = material oficial de Nintendo (ya mirado en oot_remake_cambios/previews/_scan).
  N64     serie ZeldaCentral de Switch Online (P01 / P02 / P34 de videos/zelda_oot/mapa_clips.md, marco gris NSO = 0,131),
          MAU = MaUCTYb1VtI (patio con las ventanas, HD), J32 = J32wl9suIek (ZeldaIGN, 720p, 4:3), VGZ = VgZgYI0DUCY (puente,
          1080p), PMZ = pMzN9Y5LnW4 (sangre roja v1.0 / verde v1.2), LUPA = pm0S_b-nq-U (Lupa de la Verdad, 1440p),
          MQ = EFhB23Z1OWw (Master Quest de GameCube, 1080p), SEEDY = D-3oKJEERBM e irwOHH5nixw (glitches, 1080p limpios).
  3DS     ZorZelda SQUpOZGG8FQ (Rancho Lon Lon, 1080p), Chelone zK_Ju9Mt0fM (cuadro de Skyward Sword, 720p, grabado de la pantalla).
Clip = [desde, desde + duracion del beat + 0,3]; el motor reproduce a velocidad ~1, asi que el SONIDO original del clip cae en el
mismo segundo del beat que en el video fuente (ver ambiente_por). OJO (27-oct): con +ba el tramo puede salir con el audio
desfasado respecto a la imagen: tras `bajar --rehacer` de scene-026 y scene-057 comprobar el audio (Whisper / _sonido_original
alinear) antes de mezclar.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RM100, EUR, KAE, B5 = "oLHiQX2wxrE", "QaJbU5MrPw4", "4dsfMqNJ_xI", "b5Zg52U0aE4"
DEMO, OVR, DIR = "PQvD3p2yGwc", "8v8eDMh1o3g", "wuFfiTEr2yc"
P01, P02, P34 = "N6rM3KhqHIo", "MJxGJpBja_w", "m29XeXRn-2Y"
MAU, J32, VGZ, PMZ, LUPA, MQ = "MaUCTYb1VtI", "J32wl9suIek", "VgZgYI0DUCY", "pMzN9Y5LnW4", "pm0S_b-nq-U", "EFhB23Z1OWw"
GL1, GL2 = "D-3oKJEERBM", "irwOHH5nixw"
ZOR, CHE = "SQUpOZGG8FQ", "zK_Ju9Mt0fM"
NSO = 0.131

PLAN = {
    # --- gancho e intro ---
    1: (MAU, 11.3),      # N64: patio de Zelda, la resortera apunta a la ventana con los cuadros (recorte .125)
    2: (RM100, 6331),    # remake: Link sube al patio, Zelda en la ventana, sin cuadros de Mario
    3: (VGZ, 28),        # N64: Link junto a la cadena del puente (granja de rupias, contador 243)
    4: (DIR, 46),        # remake: Kokiri, ruinas, desierto (tema general)
    5: (DIR, 7),         # remake: campo de Hyrule al amanecer
    6: (OVR, 64),        # remake: lago Hylia, cucos, rancho
    7: (KAE, 4),         # remake 4K: vista del campo de Hyrule (antes del rotulo)
    8: (P01, 27),        # N64: luna llena y Link a caballo (el original, 99)
    9: (DIR, 31),        # remake: Epona al galope (viajar de un salto vs el camino)
    10: (DEMO, 548),     # remake: corriendo por el campo
    # --- 12: Skyward Sword del 3DS ---
    11: (ZOR, 112),      # 3DS: campo del Rancho Lon Lon (recorte .037)
    12: (CHE, 33.5),     # 3DS grabado de la pantalla: sala de Malon, cuadro de Skyward Sword a ~38-42 s (CALIDAD DUDOSA)
    13: (ZOR, 128),      # 3DS: Malon y Link hablando
    # --- 11: Lupa ---
    14: (OVR, 49),       # remake: Link y Navi de cerca
    15: (LUPA, 252.3),   # N64: cofre del Pozo y «You found the Lens of Truth!» a ~261 s (recorte .125)
    16: (EUR, 289.5),    # remake: menu «Gafas de la verdad» y el ojo morado a ~294
    17: (KAE, 40),       # remake 4K: Kaepora Gaebora aterriza en el tronco
    # --- 10: Kaepora ---
    18: (P02, 928.5),    # N64: el buho hablando
    19: (P02, 946),      # N64: «Did you get all that? No / Yes» a ~952
    20: (KAE, 84),       # remake: Kaepora, dialogo corto sin pregunta
    # --- 9: Piedra de la Agonia ---
    21: (EUR, 246),      # N64 «You obtained the Stone of Agony! ... Rumble Pak» a 246-251 y, al final, el broche del remake
    22: (EUR, 253.5),    # remake: menu «Broche resonante» y marcador verde
    23: (EUR, 271.5),    # remake: planta/flor en la roca y Cancion de la tormenta
    24: (EUR, 278.5),    # remake: la gruta se abre (luz azul, agujero)
    25: (RM100, 13318),  # remake: Bosque Perdido (DUDOSO: no se ve el tronco verde)
    # --- 8: Navi ---
    26: (P01, 1002.7),   # N64: Deku, Navi llama a Link (C-arriba «Navi» a ~1013); su «Hey!» a 1013,7 cae en el hueco de voz
    27: (DEMO, 325),     # remake: «Talk to Navi»
    28: (EUR, 117),      # remake: «¡Oooh, mira! ¡Los pensamientos de un hada!» (fairy thoughts)
    29: (KAE, 24),       # remake: Link y Navi en el bosque
    # --- 7: Grandes Hadas ---
    30: (RM100, 18323),  # remake: Link corre a la fuente («Beautiful fountain...»)
    31: (P34, 36),       # N64: «Welcome Link! I am the Great Fairy...» (recorte NSO)
    32: (RM100, 18386.5),  # remake: «Put rupees in the fountain»
    33: (RM100, 18396),  # remake: «Make an offering» y el contador baja 111 -> 86
    34: (RM100, 18413),  # remake: el vapor se abre y aparece la Gran Hada
    35: (RM100, 18424),  # remake: la Gran Hada de cerca (su vestido)
    # --- 6: una sola partida ---
    36: (P01, 49.6),     # N64: «Please select a file» con File 1/2/3
    37: (RM100, 13187),  # remake: Kokiri Forest con el indicador «Saving...»
    38: (RM100, 114),    # remake: Link despierta (nueva partida)
    # --- 5: glitches ---
    39: (GL1, 0.5),      # N64 limpio 1080p: carrera por la cueva (trucos)
    40: (GL2, 0.5),      # N64 limpio: salir del Bosque Kokiri antes de tiempo
    41: (GL2, 21),       # N64 limpio: atravesar el agua/los bloques (trucos de paredes; refuerzo: pegatina del cartucho)
    42: (DEMO, 183),     # remake: aviso «Jump» en el bosque
    43: (DEMO, 205),     # remake: avisos «Dash» y «Dive»
    # --- 4: granja de rupias ---
    44: (VGZ, 36),       # N64: Link salta al centro del puente
    45: (VGZ, 3.5),      # N64: trepa por la cadena
    46: (VGZ, 17),       # N64: recoge las rupias, contador 223 -> 243
    47: (DEMO, 630.5),   # remake: el puente levadizo
    48: (DEMO, 234),     # remake: tienda Kokiri, contador /200
    # --- 3: Master Quest ---
    49: (MQ, 52),        # GC: «Reading the Game Disc... Master Quest» (recorte .125)
    50: (MQ, 76),        # GC: titulo Master Quest con el caballo (recorte .125)
    51: (RM100, 135),    # remake: titulo sin Master Quest
    52: (RM100, 67212),  # remake: final del juego, los sabios
    # --- 2: Ganondorf ---
    53: (P34, 1150),     # N64: Ganondorf al organo
    54: (PMZ, 26.8),     # N64 v1.0: sangre roja, termina justo en la sangre (recorte arriba/abajo)
    55: (PMZ, 10.2),     # N64 v1.2: sangre verde (recorte arriba/abajo)
    56: (B5, 683),       # remake: el golpe final con la flecha
    57: (B5, 702.4),     # remake: Ganondorf de rodillas; «Impossible» a ~706 y «I, the mighty Ganondorf» a ~707,2
    58: (B5, 712.2),     # remake: sigue la escena («Losing to some pathetic child?!»), sin audio
    59: (B5, 732),       # remake: Link y Navi, el castillo se derrumba
    # --- 1: cuadros de Mario ---
    60: (J32, 12.5),     # N64 (ZeldaIGN 4:3): las ventanas con los cuadros (recorte 4:3)
    61: (MAU, 24),       # N64: la resortera, «Hey you! Don't cause any trouble!» a ~30 (recorte .125)
    62: (RM100, 9),      # remake: el tapiz «Threads of Time»
    63: (RM100, 6339),   # remake: el patio sin cuadros
    64: (RM100, 5927),   # remake: guardias de la puerta del castillo (DUDOSO: no es el guardia de la ventana)
    65: (RM100, 6128),   # remake: Talon despierta (DUDOSO: el broche de Bowser no se distingue)
    66: (EUR, 333),      # remake: sala de enemigos derrotados (coliseo)
    67: (KAE, 122.5),    # remake 4K: Link mirando el campo de Hyrule
    68: (DEMO, 845),     # remake: atardecer en el rancho
}

# recorte por clip: fraccion por lado o (izq, arriba, der, abajo)
REC_NSO = (1, 8, 18, 19, 26, 31, 36, 53)
RECORTE = {k: NSO for k in REC_NSO}
RECORTE.update({
    1: 0.125, 61: 0.125,                       # MAU: 4:3 con barras
    60: (0.14, 0, 0.145, 0),                   # J32: 4:3 con la marca IGN fuera
    15: 0.125,                                 # LUPA: marco decorativo de Emanu Korok
    49: 0.125, 50: 0.125,                      # MQ de GameCube: 4:3
    11: 0.037, 13: 0.037,                      # 3DS ZorZelda
    12: (0.03, 0, 0.02, 0),                    # Chelone: pantalla grabada
    54: (0, 0.14, 0, 0.14), 55: (0, 0.14, 0, 0.14),   # PMZ: barras de cine del juego
})
RECORTE[8] = NSO

# sonido original del clip (volumen 0,5-0,9)
AMBIENTE = {
    26: 0.9,   # «Hey!» de Navi (N64) en los 2,2 s de voz callada del final de p8
    57: 0.7,   # Ganondorf del remake: «Impossible... I, the mighty Ganondorf...» en los 6 s de voz callada de p2
    15: 0.6,   # N64: fanfarria del cofre / «Lens of Truth»
    19: 0.5,   # N64: el buho y su pregunta
    21: 0.6,   # N64: «You obtained the Stone of Agony!»
    31: 0.6,   # N64: la Gran Hada
    45: 0.6,   # N64: Link trepando por la cadena
    46: 0.6,   # N64: el sonido de las rupias al recogerlas
    49: 0.5,   # GC: musica del menu / disco Master Quest
    54: 0.6,   # N64 v1.0: grito de Ganondorf y la sangre roja
    55: 0.6,   # N64 v1.2: lo mismo con la sangre verde
    61: 0.5,   # N64: la resortera y el guardia «Hey you!»
}

if __name__ == "__main__":
    out = {}
    for n, (vid, s) in sorted(PLAN.items()):
        out[f"scene-{n:03d}"] = {"url": f"https://youtu.be/{vid}", "desde": s}
    assert len(out) == 68, len(out)
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats ->", "busquedas.json")
    print("recorte_por =", {f"scene-{k:03d}": v for k, v in sorted(RECORTE.items())})
    print("ambiente_por =", {f"scene-{k:03d}": v for k, v in sorted(AMBIENTE.items())})
