"""Baja los clips reales (1080p máx., mp4 sin audio no hace falta: se guarda con audio por si acaso). Uso: python _clips.py
Crédito de cada clip en CREDITO de comun.py."""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
CL = {
    # nombre: (id, sección o None)
    "b7": ("GV4Pc0ntO2Q", None),            # VideoFromSpace/SpaceX: 31 de 33 en la prueba estática (feb-2023)
    "f10mesa": ("wS_8WOQJUu8", None),       # VideoFromSpace/SpaceX: vista desde la mesa, vuelo 10
    "f1": ("_krgcofiM6M", None),            # SpaceX: vuelo 1
    "f1b": ("0PPCP0ZDdUI", None),           # VideoFromSpace/SpaceX: vuelo 1, más largo
    "f2sep": ("hcEHIePxHBk", None),         # VideoFromSpace/SpaceX: vuelo 2, separación
    "f2b": ("zA0hPG9AMOE", None),           # VideoFromSpace: vuelo 2, separación + explosión
    "f5": ("hI9HQfCAw64", None),            # SpaceX: vuelo 5 (regreso 1:16-2:20, captura 2:20-2:42)
    "mcg": ("TXYh4re0j8M", None),           # SpaceX: McGregor
    "r3": ("HJdu5ee_ohA", None),            # VideoFromSpace/SpaceX: Raptor 3 en prueba
    "r3b": ("PAqC94JmRKY", None),           # VideoFromSpace/SpaceX: Raptor 3 explicado
    "a11": ("DKtVpvzUF1Y", None),           # Spacecraft Films: cámara E-8 de Apolo 11, los 5 F-1
    "s1c": ("-rP6k18DVdg", None),           # NASA Marshall: prueba estática S-IC
    "f1mot": ("TtRpQKzVLaM", None),         # prueba de un F-1 (resubida)
    "n1": ("u2eAHvFprE8", None),            # Retro Space HD: N1 3-jul-1969 (material Roscosmos)
    "n1b": ("_iuo3J8L9b8", None),           # Space Clips: los 4 lanzamientos del N1
    "crs1": ("qJsEv1x-kIE", None),          # SpaceNewsNow: CRS-1, falla del motor 1
    "orbcomm": ("CQnR5fhCXkQ", None),       # SpaceX: aterrizaje ORBCOMM 2014
    "f15ap": ("VaeoXpx3Wsc", None),         # AP: explosión del B22, vuelo 15
    "f15": ("RHY66XujZ90", None),           # VideoFromSpace: vuelo 15 (propulsor 6:08-7:26)
    "fh": ("wbSwFU6tY1c", "*17:20-19:40"),  # SpaceX: Falcon Heavy, despegue en 17:41
    "fabrica": ("aFqjoCbZ4ik", "*41:00-44:30"),  # Everyday Astronaut: recorrido, Raptors
}

for nom, (vid, sec) in CL.items():
    dest = os.path.join(AQUI, "clips", nom + ".mp4")
    if os.path.exists(dest):
        continue
    cmd = ["yt-dlp", "-q", "--no-warnings", "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]",
           "--merge-output-format", "mp4", "-o", dest, f"https://www.youtube.com/watch?v={vid}"]
    if sec:
        cmd[1:1] = ["--download-sections", sec, "--force-keyframes-at-cuts"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(nom, "OK" if os.path.exists(dest) else "FALLÓ " + (r.stderr or "")[-200:], flush=True)
