# Corta tramos del VOD de Twitch en 1080p30 + AAC: python cortar_twitch.py <destino_dir> <vod_id> nombre:desde:dur ...
# (yt-dlp --download-sections funciona aunque el VOD siga en vivo; luego ffmpeg a 30 fps como las fuentes de t1_koi_worlds)
import subprocess, sys, os
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
dest, vod = sys.argv[1], sys.argv[2]
os.makedirs(dest, exist_ok=True)
for spec in sys.argv[3:]:
    nom, desde, dur = spec.split(":")
    a, b = float(desde), float(desde) + float(dur)
    tmp = os.path.join(dest, f"_{nom}_crudo.mp4")
    out = os.path.join(dest, nom + ".mp4")
    if os.path.exists(out):
        print("ya", out); continue
    subprocess.run(["yt-dlp", "-q", "--force-overwrites", "--download-sections", f"*{a}-{b}", "-f", "1080p60/best",
                    "--ffmpeg-location", r"C:\ffmpeg\bin", "-o", tmp, f"https://www.twitch.tv/videos/{vod}"], check=True)
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", tmp, "-t", dur, "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "18", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out], check=True)
    os.remove(tmp)
    print("ok", out, subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration",
                                     "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
