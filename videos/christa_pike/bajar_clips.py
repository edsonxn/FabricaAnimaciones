# -*- coding: utf-8 -*-
"""Descarga con yt-dlp (<=720p) los videos de noticias/archivo que se usarán en EXTRACTOS CORTOS con crédito en pantalla.
Todo es de licencia estándar de YouTube (no CC): se anota en clips/creditos_clips.json con canal, título y URL."""
import json, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "clips")
os.makedirs(OUT, exist_ok=True)

LISTA = {   # nombre -> id de YouTube
    "wbir_asesinato_1995": "Zo89WzCh07A",        # Jan. 12, 1995: The murder of Colleen Slemmer (WBIR, 1:50)
    "wbir_cronologia": "BOFtu15rCaw",             # Christa Gail Pike timeline: 30 years (WBIR, 5:40)
    "wbir_2020": "gQLjD37ir20",                   # The Knoxville Job Corps killing (WBIR, 6:22)
    "wbir_protesta": "OD-HNCMRlXc",               # Hundreds gather in Nashville to protest (WBIR, 1:32)
    "wbir_carpa": "n5-hTen5crc",                  # Inside the media tent at execution stay (WBIR, 2:52)
    "tdoc_riverbend": "-9enj1zevBs",              # TDOC: Riverbend Maximum Security Institution (2:03)
    "fox_nashville_familias": "UkaEYviAhwE",      # Grieving families ... (FOX Nashville, 2:49)
    "abc_ventilador": "M44uraWOnOA",              # ABC News (1:32)
    "nbc_ventilador": "x-O_CCf6IFg",              # NBC News (2:55)
    "inside_ultimo_deseo": "McRe8jtagNk",         # Inside Edition (1:50)
    "inside_que_fallo": "6ifK6aBXwuQ",            # Inside Edition (3:00)
    "cbs_suspension": "x8OluiQqVUk",              # CBS News (3:36)
    "cbs_sobrevivio": "a8hVGQbNHWY",              # CBS News (4:14)
    "france24": "00IREqoxi4A",                    # FRANCE 24 English (1:45)
    "newsx_strada": "Ft_sii7149o",                # NewsX World (2:10)
    "newschannel5_hospital": "vJ5IYZAMbU8",       # NewsChannel 5 (6:29)
}

if __name__ == "__main__":
    solo = sys.argv[1:] or list(LISTA)
    cr_path = os.path.join(OUT, "creditos_clips.json")
    cr = json.load(open(cr_path, encoding="utf-8")) if os.path.exists(cr_path) else {}
    for nom in solo:
        vid = LISTA[nom]
        destino = os.path.join(OUT, nom + ".mp4")
        if os.path.exists(destino):
            print("ya existe", nom)
            continue
        cmd = [sys.executable, "-m", "yt_dlp", f"https://www.youtube.com/watch?v={vid}",
               "-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/b[height<=720]",
               "--merge-output-format", "mp4", "-o", destino, "--no-playlist", "--no-warnings", "-q", "--progress",
               "--print-to-file", "%(channel)s|%(title)s|%(upload_date)s|%(duration_string)s", os.path.join(OUT, nom + ".info.txt"),
               "--ffmpeg-location", r"C:\ffmpeg\bin"]
        r = subprocess.run(cmd, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        if r.returncode == 0 and os.path.exists(destino):
            info = open(os.path.join(OUT, nom + ".info.txt"), encoding="utf-8").read().strip().split("|")
            cr[nom] = dict(canal=info[0], titulo=info[1], fecha=info[2], duracion=info[3], url=f"https://www.youtube.com/watch?v={vid}",
                           licencia="YouTube estándar (no CC): solo extractos cortos con crédito, uso informativo/comentario")
            json.dump(cr, open(cr_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("OK", nom, round(os.path.getsize(destino) / 1e6, 1), "MB")
        else:
            print("FALLÓ", nom)
