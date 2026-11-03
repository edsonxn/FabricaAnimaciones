# -*- coding: utf-8 -*-
"""SONIDOS DEL PROPIO JUEGO (regla del 29-oct-2026) -> sfx/pk_*.mp3, sin silencios de cola.
- Interfaz y mundo: canal «Matteo», un video por sonido de Rojo/Azul/Amarillo (etiquetados en el título).
- Gritos: «All Pokemon Red & Blue Cries» (Kvn3kHJFKuI), segundo del n.º n = 0,6 + (n - 1) × 1,23 (medido el 3-nov: Rhydon 138).
    python bajar_sfx.py
"""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
OD = os.path.join(AQUI, "sfx")
SUELTOS = {
    "pk_nivel": "OGXUoqSYscc", "pk_objeto": "RdxJ5c3MG1M", "pk_guardar": "59luvyf9SYI", "pk_pc": "fwEzOeeZxUE",
    "pk_pc_entra": "yKN3_WSMp7o", "pk_pc_sale": "PBOpSZja-1A", "pk_lanzar": "tXY4u4OM4w4", "pk_captura": "xgX0zPfAsv0",
    "pk_intento": "yOj2YtXAf4c", "pk_fallo": "T5DLcfFVsKY", "pk_huir": "1hcICWMIKTQ", "pk_error": "K4sgpVUOCZw",
    "pk_vuelo": "OUdD1Itsukc", "pk_choque": "TgOm3ewdXcc", "pk_puerta": "00rlTif_Kfg", "pk_a": "88qRmxhqoBA",
    "pk_start": "8Mla0CskjNw", "pk_pokedex": "rduVgdbO4B0", "pk_pokedex2": "q_uze6Jnv6M", "pk_curar": "Cd5vHQy30S8",
    "pk_fuerza": "dlzDe7zS3O8", "pk_barco": "BmnRb7L4cUw", "pk_compra": "WOLmd0ZIPBY", "pk_teleport": "wa6_3zkNGKI",
    "pk_veneno": "09nSUB3QhlM", "pk_corte": "2uhCrgM169A",
}
GRITOS = {"bulbasaur": 1, "charmander": 4, "squirtle": 7, "pikachu": 25, "raichu": 26, "clefairy": 35, "arcanine": 59,
          "alakazam": 65, "victreebel": 71, "gastly": 92, "gengar": 94, "exeggutor": 103, "rhydon": 112, "jynx": 124,
          "tauros": 128, "gyarados": 130, "ditto": 132, "dragonite": 149, "mewtwo": 150, "mew": 151}
RECORTE = "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse"


def bajar(vid, tmp, seccion=None):
    cmd = ["yt-dlp", "-x", "--audio-format", "wav", "--no-playlist", "--quiet", "--no-warnings", "-o", tmp + ".%(ext)s"]
    if seccion:
        cmd += ["--download-sections", seccion]
    subprocess.run(cmd + [f"https://youtu.be/{vid}"], capture_output=True)
    return tmp + ".wav"


def mp3(wav, out, extra=""):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-af", (extra + "," if extra else "") + RECORTE,
                    "-ar", "48000", "-ac", "2", "-b:a", "192k", out], check=True)
    os.remove(wav)


if __name__ == "__main__":
    os.makedirs(OD, exist_ok=True)
    for n, vid in SUELTOS.items():
        out = os.path.join(OD, n + ".mp3")
        if not os.path.exists(out):
            mp3(bajar(vid, os.path.join(OD, "_" + n)), out)
            print(n, "ok")
    todos = bajar("Kvn3kHJFKuI", os.path.join(OD, "_gritos"))
    for n, k in GRITOS.items():
        out = os.path.join(OD, f"pk_grito_{n}.mp3")
        if os.path.exists(out):
            continue
        t = 0.6 + (k - 1) * 1.23 - 0.15
        tmp = os.path.join(OD, f"_g_{n}.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-t", "1.15", "-i", todos, tmp], check=True)
        mp3(tmp, out, "afade=t=out:st=1.0:d=0.15")
        print("grito", n, "ok")
    os.remove(todos)
