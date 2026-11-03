# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA ORIGINAL de Game Boy de Rojo/Azul a audio/ost/<nombre>.wav (regla del 23-oct-2026: en Crónicas del gaming
va la música del juego, nunca Lyria). Lista «Pokémon Red/Blue/Yellow Soundtrack» (Daintii Music, PL2uxd6YWj7PLbKlHSlTO7Lv4E6csDZhRc),
una pista por video.   python bajar_ost.py
"""
import os
import subprocess

PISTAS = {
    "titulo": "kJNuL_ebJMA", "pallet": "kO09V19wwlE", "oak": "PBGz9zkrPl8", "oak_lab": "mAZSdITC5fw", "rival": "XibSIEytjOo",
    "route1": "UCzsAM8myys", "wild": "LgK2f47q8cU", "capturado": "b3ay7CmkDr8", "pkcenter": "I_pRfIE6PgQ", "pewter": "nKEGjCgjDDc",
    "gymleader": "OMJLxfCWVb8", "victoria_lider": "Z2NRU83AxNg", "forest": "easI5Jcy3bE", "trainer": "fEWo5q_xy-Q",
    "route3_4": "dGad5zo197A", "cerulean": "7cNrqdPk0CA", "mtmoon": "3tjHIczAQE4", "route24": "ap4UpeatILU", "ssanne": "NEOV1OAv_QE",
    "vermilion": "6cWa4eNB5Jc", "route6": "ubFEqxrVWlk", "cycling": "Y1T8qWNWTB4", "lavender": "rfDPaCoH-Fs", "tower": "B-EQhnUYbFQ",
    "celadon": "9ENNKVoDmYg", "casino": "D3pDxLa9ElA", "silph": "QUK07P45m2A", "surf": "_2STgEDZXs4", "cinnabar": "ru_mtMDTFTw",
    "mansion": "WZb83GqAe-c", "indigo": "IGV3-vMsQiU", "champion": "erHsp-TrHNI", "hall_fame": "E3O-YUY2yQw", "credits": "ZLxd0Oq4NXA",
    "gym": "x6Nc4voDSak",
}

if __name__ == "__main__":
    aqui = os.path.dirname(os.path.abspath(__file__))
    od = os.path.join(aqui, "audio", "ost")
    os.makedirs(od, exist_ok=True)
    for n, vid in PISTAS.items():
        out = os.path.join(od, n + ".wav")
        if os.path.exists(out):
            continue
        r = subprocess.run(["yt-dlp", "-x", "--audio-format", "wav", "--no-playlist", "--quiet", "--no-warnings",
                            "-o", os.path.join(od, n + ".%(ext)s"), f"https://youtu.be/{vid}"], capture_output=True, text=True)
        print(n, "ok" if os.path.exists(out) else "FALLÓ " + r.stderr[-200:])
