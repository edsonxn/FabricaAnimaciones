# -*- coding: utf-8 -*-
"""Plan de clips de n64_secretos (31-oct-2026; estructura de spyro2/mario64_secretos): para cada beat (scene-001…170) un video de YouTube y el segundo
donde empieza su clip (el motor corta duración del beat + 0,3 s). Segundos elegidos MIRANDO hojas propias de medios/_escaneo (escanear.py: 360p por HTTP,
un cuadro cada N s con el segundo impreso). Escribe busquedas.json e imprime ambiente_por y recorte_por para pegar en SECUENCIA de guion.py.
    python plan_clips.py
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

F = {   # nombre: (id de YouTube, recorte por lado o 0, nota)
    "MPT": ("qXs0YeCdgrE", 0, "Mario Party 1 Tug o' War 29 s 720p24"),
    "MPP": ("vxXjicb2018", 0, "Mario Party 1 Pedal Power 45 s 4K"),
    "MP": ("5gwk2lA-muE", 0, "Mario Party 1 HD todos los minijuegos 4K"),
    "TETLP": ("BIXhf-QGue0", 0, "N64 Archive: Tetris 64 longplay 1080p60 (Bio Tetris desde 1103)"),
    "TET1": ("DQ4OvnVSQQM", 0, "Retro Ali: Bio Sensor (solo la foto del sensor 205-212)"),
    "IQ3": ("ceIRDAbbWTI", 0, "Zero64: iQue Player 4K"),
    "IQ5": ("6CD-6VKVR0Y", 0, "Console Technician: iQue 1080p"),
    "DKG": ("4hZ9i7tI1-Y", 0, "NotSoDevy: Dragon King prototype footage 1080p"),
    "OOT1": ("wuFfiTEr2yc", 0, "Nintendo of America: tráiler del remake de Ocarina of Time 4K"),
    "TANN": ("G28N5JqbGa8", 0, "Tanner's Game Museum: Silicon Graphics y la N64 1080p"),
    "SGI": ("gsIcKZnjjFg", 0, "pix ben: SGI Indy con Mario 64 1080p"),
    "SATURN": ("cyv6ZehQyTQ", 0, "Cyber Chaos Crew: comercial de lanzamiento de Sega Saturn 1080p"),
    "PSPRE": ("wWbfrx_uKYs", 0, "fenarinarsa: promo de prelanzamiento de PlayStation 1080p50"),
    "HW1": ("xROmt3g7NkY", 0, "Retro_VG_Repairs: desmontaje de la N64 1080p60"),
    "CART": ("x6_VsvoTe4Q", 0, "JRChadwick: disección de un cartucho de N64 720p"),
    "FV3": ("81yCq7Qfr7o", 0, "Retro Game Hunter Japan: caja y discos de Final Fantasy VII 4K"),
    "FV1": ("6CORYpK6_W8", 0, "Square Enix: Final Fantasy VII opening 1080p"),
    "SM64": ("CRzjAKE2Zns", .131, "Ninbanyan: Super Mario 64 Switch Online 1080p60"),
    "UNB": ("4g2EQwY0-jE", 0, "Crusherbad64: unboxing de la N64 1080p"),
    "SH": ("Ko_s0ij-z5o", 0, "N64 Archive: Saikyo Habu Shogi 1080p60"),
    "MK4": ("Kz-lI04yJ2c", 0, "arronmunroe: Mario Kart 64 a 4 jugadores 4K60"),
    "MK1": ("c2zG0FH8E9U", 0, "Matthew Reynolds: Yoshi Valley 1080p60"),
    "MEL": ("QNjqwueSvBY", 0, "LongplayArchive: Super Smash Bros. Melee (GameCube) 1080p60"),
    "RUM2": ("JWQ3kJYdf_0", 0, "Modern Vintage Gamer: Rumble Pak 4K (sin cara)"),
    "MT1": ("X-_P9onXHfA", 0, "Soap: Mario Tennis N64 intro 4K60"),
    "MT2": ("1XUiY4XgXj4", 0, "Power On: Mario Tennis N64 intro 4K60"),
    "MTC": ("m8Yyvw87PUg", 0, "NintenU: Mario Tennis 64 todos los personajes 4K"),
    "EX5": ("8TXuoLETX20", 0, "WatchmeplayNintendo: Excitebike 64 soccer 1080p60"),
    "EX3": ("1ABkIMlIEKk", 0, "Anthony Vo: Excitebike 64 Excite 3D 1080p"),
    "PW2": ("2HTVn5y3a9c", 0, "Yoshiller: Pilotwings 64 Mario/Wario 1080p60"),
    "PW1": ("sU0jNhzayiw", 0, "jdlmon64: Pilotwings 64 Rushmore Wario 1080p60"),
    "PWNSO": ("lmepP3ehkaM", 0, "Nintendo of America: Pilotwings 64 Switch Online"),
    "STK": ("3mYjgqrgtJY", 0, "Restore64: stick del mando N64 4K"),
    "STK2": ("HclgCNZvb5U", 0, "A Gizmo: reparación del stick N64 1080p"),
    "SF": ("1AKsOoOBhWw", 0, "Video Chums: Star Fox 64 Switch Online 1080p60"),
    "WB2": ("AqoXdap-c8s", 0, "Cyime: Wide-Boy 64 1080p"),
    "JP1": ("efi1czrC55E", 0, "RetoRetro64: Jumper Pak 1080p"),
    "JP3": ("FpiB0wxjOwc", 0, "Ryan Recommends: quitar el Jumper Pak 1080p"),
    "TX1": ("z4mrVbNh7X8", 0, "Don Allen: Super Mario 64 sin filtro de texturas 4K"),
    "PS3": ("P80oQ7q-l2A", 0, "BlueHedgehogMan17: Pokémon Stadium Game Boy Tower 1080p"),
    "CL1": ("yeEdKdF8eIQ", 0, "SicCooper: ClayFighter Sculptor's Cut 4K (solo manos y juego)"),
    "SU2": ("XdMNoRwlQJI", 0, "walker1984: Superman 64 anillos 1080p"),
    "CR2": ("x2OSOFWmCYM", 0, "Toxik Videos: Cruis'n USA arcade 1080p"),
    "KIULTRA": ("jkWBRCeJKvA", 0, "Quin Cukoo: comercial Nintendo ULTRA 64 Killer Instinct 1080p"),
    "KIG": ("ETCsqMjhKr8", 0, "LongplayArchive: Killer Instinct Gold 1440p60"),
    "SN1": ("lCnvpIEVpqo", 0, "Leonhart: Pokémon Snap Station 1080p60"),
    "HT2": ("125ltCbo7Ag", 0, "NRetroSpect: mando LodgeNet 720p"),
    "PD1": ("93qPlZR38yg", 0, "Matt Armour: Perfect Head, menús del E3 1999 720p59"),
    "DKT": ("Jpz4TZ7CAsQ", 0, "Nintendo of America: tráiler de Donkey Kong 64 en Switch Online"),
    "BH1": ("Q-Q_XgCleGI", 0, "Timmothy: Body Harvest nivel 1 1080p60"),
    "GT2": ("FQGllj4BjbA", 0, "BlaZe 92: camionetas de helados en los GTA (GTA III en 77-123) 1080p60"),
    "AF2": ("EFwQYCjgg7o", 0, "Video Game Intros: Doubutsu no Mori N64 1080p60"),
    "DD1": ("np0Cd_Iw7-w", 0, "The Famicast: disco Randnet del 64DD 1080p60"),
    "RE3": ("eQ68M1R-1hk", 0, "AKIR_4: Resident Evil 2 N64 1080p60"),
    "FF1": ("pZ0Pr8O6xnQ", 0, "Cyiatic: Final Fantasy VI Interactive CG Game 1080p15"),
    "DQ1": ("HSkxFrHNbgU", 0, "Joy Vision Studio: Dragon Warrior VII intro 720p"),
    "EB1": ("kFbl0S7G82o", 0, "Omni Productions: EarthBound 64 Spaceworld 1997 4K"),
    "EB2": ("gA-vvPKY5qw", 0, "SnowWood: EarthBound 64 Spaceworld 1999 720p"),
    "EB3": ("YLJ10_Rb-_4", 0, "BloxLogics: EarthBound 64 1080p60"),
    "M3": ("92bNvuPlfD8", 0, "LongPlaySonic: Mother 3 GBA"),
    "SB3": ("m3ZIYbkEPDQ", 0, "LongplayArchive: Mario Artist Polygon Studio 1440p60"),
    "SB2": ("hq2gPDU_eUE", 0, "ParallelSkawo: Sound Bomber 720p60"),
    "WW1": ("h_cQWl_drqg", 0, "LongplayArchive: WarioWare Inc. 1920p60"),
    "IW1": ("RMrj8gdUfCU", 0, "GDC: Satoru Iwata Heart of a Gamer 720p30"),
    "IW2": ("9YG9INjO91Y", 0, "GDC: homenaje animado a Satoru Iwata 1080p"),
    "SMASH": ("A6vORGHJWiM", 0, "ModernXP: Super Smash Bros. 64 100 % 1080p60"),
    "MT3": ("84T364Y9K-c", 0, "DarkCheee Gaming: Waluigi con el trofeo, Mario Tennis 64 1080p60"),
    "SHOS": ("ouybLlO0B1k", 0, "Ultra64 ARCHIVES: Super Mario 64 beta antes de Shoshinkai 1995 1080p"),
    "LIB": ("Hz8mW7DrOxY", 0, "Virtual Gaming Library: todos los juegos de N64 (VENTANA, ventanas.py)"),
    "NESV": ("Cy2PqdndtXE", 0, "Excitebike NES dentro de Excitebike 64 (VENTANA, ventanas.py)"),
    "KI1": ("vVE1d2gBcSM", 0, "Arcade Lounge: Killer Instinct arcade 3D lado a lado (VENTANA, ventanas.py)"),
    "MAJ": ("7xAeJ9DY1Fw", .131, "ZeldaCentral: Majora's Mask Switch Online 1080p60"),
}

PLAN = {
    1: ("MPT", 3), 2: ("TETLP", 1225), 3: ("IQ3", 62), 4: ("DKG", 0), 5: ("OOT1", 112), 6: ("UNB", 170),
    7: ("TANN", 20), 8: ("SGI", 130), 9: ("TANN", 152), 10: ("CR2", 40), 11: ("SHOS", 4), 12: ("SATURN", 234),
    13: ("SGI", 175), 14: ("HW1", 500), 15: ("FV3", 75), 16: ("CART", 14), 17: ("HW1", 800), 18: ("CART", 60),
    19: ("FV1", 80), 20: ("LIB", 1500), 21: ("LIB", 2400), 22: ("SM64", 185), 23: ("SH", 80), 24: ("UNB", 42),
    25: ("MK4", 90), 26: ("MK4", 245), 27: ("UNB", 640), 28: ("PSPRE", 54), 29: ("MEL", 827), 30: ("LIB", 3000),
    31: ("WB2", 8), 32: ("MT1", 84), 33: ("MT1", 112), 34: ("MT3", 0), 35: ("MTC", 40), 36: ("EX3", 5),
    37: ("EX3", 40), 38: ("EX5", 41), 39: ("NESV", 200), 40: ("PW2", 6.7), 41: ("PW2", 94), 42: ("PW2", 110),
    43: ("PW1", 105), 44: ("STK", 0), 45: ("STK", 109), 46: ("STK", 130), 47: ("STK2", 160), 48: ("HW1", 574),
    49: ("HW1", 597), 50: ("HW1", 640), 51: ("RUM2", 18), 52: ("SF", 106), 53: ("RUM2", 93), 54: ("RUM2", 205),
    55: ("WB2", 40), 56: ("WB2", 60), 57: ("WB2", 112), 58: ("WB2", 388), 59: ("JP1", 12), 60: ("JP1", 30),
    61: ("JP1", 60), 62: ("JP3", 90), 63: ("TX1", 32), 64: ("TX1", 60), 65: ("TX1", 100), 66: ("MK1", 6),
    67: ("MK1", 20), 68: ("MK1", 60), 69: ("MK1", 100), 70: ("PS3", 10), 71: ("PS3", 41), 72: ("PS3", 72),
    73: ("CL1", 190), 74: ("CL1", 62), 75: ("CL1", 439), 76: ("CL1", 585), 77: ("SU2", 35), 78: ("SU2", 56),
    79: ("SU2", 70), 80: ("SU2", 90), 81: ("SU2", 105), 82: ("KIULTRA", 10.5), 83: ("KI1", 24), 84: ("KIG", 100),
    85: ("SN1", 93), 86: ("SN1", 209), 87: ("SN1", 838), 88: ("SN1", 931), 89: ("HT2", 40), 90: ("HT2", 120),
    91: ("HT2", 60), 92: ("MK4", 400), 93: ("IQ3", 386), 94: ("IQ5", 170), 95: ("IQ3", 416), 96: ("IQ5", 300),
    97: ("IQ5", 400), 98: ("PD1", 12), 99: ("PD1", 60), 100: ("PD1", 114), 101: ("PD1", 125), 102: ("DKT", 5.5),
    103: ("DKT", 17.8), 104: ("DKT", 25), 105: ("DKT", 33.5), 106: ("BH1", 28), 107: ("BH1", 253), 108: ("BH1", 478),
    109: ("BH1", 619), 110: ("GT2", 77.2), 111: ("AF2", 5.9), 112: ("AF2", 30), 113: ("AF2", 60), 114: ("AF2", 80),
    115: ("DD1", 78), 116: ("DD1", 94), 117: ("DD1", 141), 118: ("DD1", 439), 119: ("DD1", 549), 120: ("RE3", 0),
    121: ("RE3", 172), 122: ("RE3", 183), 123: ("RE3", 217), 124: ("RE3", 332), 125: ("MPP", 0), 126: ("MPP", 20),
    127: ("MP", 1323), 128: ("STK", 349), 129: ("TETLP", 1103), 130: ("TET1", 205.5), 131: ("TETLP", 1143), 132: ("TETLP", 1388),
    133: ("TETLP", 1634), 134: ("FF1", 8), 135: ("FF1", 43), 136: ("FF1", 100), 137: ("TANN", 40), 138: ("FF1", 150),
    139: ("FV1", 93), 140: ("FV1", 105), 141: ("FV3", 41.7), 142: ("DQ1", 36), 143: ("DQ1", 100), 144: ("EB1", 0),
    145: ("EB1", 9), 146: ("EB2", 0), 147: ("M3", 300), 148: ("EB3", 0), 149: ("EB2", 30), 150: ("SB3", 1422),
    151: ("SB2", 130), 152: ("WW1", 426), 153: ("WW1", 213), 154: ("DKG", 12), 155: ("IW2", 23), 156: ("IW2", 7),
    157: ("DKG", 30), 158: ("SMASH", 3953), 159: ("SMASH", 416), 160: ("SMASH", 1248), 161: ("IW1", 154), 162: ("IW1", 83),
    163: ("IW1", 92), 164: ("IW2", 138), 165: ("OOT1", 6.6), 166: ("PWNSO", 4), 167: ("MAJ", 165), 168: ("OOT1", 160),
    169: ("UNB", 700), 170: ("MP", 1369),
}

# beats donde conviene OÍR el juego (audio del clip): música, SFX o voz de personaje, sin narrador de youtuber encima
AMBIENTE = {1: .6, 19: .8, 22: .7, 25: .6, 26: .6, 32: .7, 33: .7, 38: .5, 40: .6, 41: .6, 42: .6, 43: .6, 52: .7,
            66: .7, 67: .7, 68: .6, 69: .6, 77: .6, 78: .6, 79: .6, 80: .6, 84: .7, 112: .7, 113: .7, 114: .6, 125: .6,
            126: .6, 131: .5, 132: .5, 134: .7, 135: .7, 139: .7, 142: .6, 144: .7, 150: .6, 152: .8, 153: .8, 158: .7}


def sid(n):
    return f"scene-{n:03d}"


if __name__ == "__main__":
    beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
    assert len(beats) == len(PLAN) == 170, (len(beats), len(PLAN))
    out = {}
    for b in beats:
        n = int(b["id"].split("-")[1])
        nom, s = PLAN[n]
        out[b["id"]] = {"url": f"https://youtu.be/{F[nom][0]}", "desde": s}
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    recorte_por = {sid(n): F[nom][1] for n, (nom, s) in sorted(PLAN.items()) if F[nom][1]}
    ambiente_por = {sid(n): v for n, v in sorted(AMBIENTE.items())}
    print(f"busquedas.json: {len(out)} beats, {len({v[0] for v in PLAN.values()})} fuentes")
    print("recorte_por = " + repr(recorte_por))
    print("ambiente_por = " + repr(ambiente_por))
