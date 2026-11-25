# Corta del VOD completo 1080p H.264 (itag 299/137) + audio ORIGINAL en español (el VOD trae doblajes automáticos) a ../medios/_fuente: python los_cortar.py nombre:vid:desde:dur ...
import subprocess, sys, os
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dest = os.path.join(D, "medios", "_fuente")
os.makedirs(dest, exist_ok=True)
for spec in sys.argv[1:]:
    nom, vid, desde, dur = spec.split(":")
    urls = subprocess.run(["yt-dlp", "-g", "-f", "299+ba[ext=m4a][format_note*=original]/137+ba[ext=m4a][format_note*=original]", f"https://youtu.be/{vid}"],
                          capture_output=True, text=True).stdout.split()
    v, a = urls[0], urls[1]
    out = os.path.join(dest, nom + ".mp4")
    r = subprocess.run([FF, "-loglevel", "error", "-y", "-ss", desde, "-i", v, "-ss", desde, "-i", a, "-t", dur, "-map", "0:v:0",
                        "-map", "1:a:0", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "30", "-c:a", "aac",
                        "-b:a", "192k", out], capture_output=True, text=True)
    print(nom, "rc", r.returncode, r.stderr[-300:], os.path.getsize(out) if os.path.exists(out) else None)
