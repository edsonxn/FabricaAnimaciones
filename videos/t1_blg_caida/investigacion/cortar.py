# Corta tramos de los VOD completos en 1080p con audio: python cortar.py <destino_dir> nombre:vid:desde:dur ...
import subprocess, sys, os
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
dest = sys.argv[1]
os.makedirs(dest, exist_ok=True)
for spec in sys.argv[2:]:
    nom, vid, desde, dur = spec.split(":")
    urls = subprocess.run(["yt-dlp", "-g", "-f", "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/bv*[height<=1080]+ba",
                           f"https://youtu.be/{vid}"], capture_output=True, text=True).stdout.split()
    v, a = urls[0], urls[1]
    out = os.path.join(dest, nom + ".mp4")
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", desde, "-i", v, "-ss", desde, "-i", a, "-t", dur, "-map", "0:v:0",
                    "-map", "1:a:0", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "30", "-c:a", "aac",
                    "-b:a", "192k", out], check=True)
    print("ok", out)
