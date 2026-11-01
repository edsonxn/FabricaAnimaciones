# dl_sec.py <videoid> <nombre> <ini_s> <fin_s> [alto=1080]
import subprocess, sys, os, time
vid, nombre, ini, fin = sys.argv[1:5]
alto = sys.argv[5] if len(sys.argv)>5 else "1080"
os.makedirs("sec", exist_ok=True)
out = f"sec/{nombre}.%(ext)s"
fmt = f"bestvideo[height<={alto}][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[height<={alto}]+bestaudio/best[height<={alto}]"
cmd = ["yt-dlp","-f",fmt,"--download-sections",f"*{ini}-{fin}","--force-keyframes-at-cuts","--merge-output-format","mp4",
       "-o",out,"--no-part","--quiet","--no-progress",f"https://youtu.be/{vid}"]
r = subprocess.run(cmd,capture_output=True,text=True,encoding="utf-8",errors="replace")
print((r.stdout+r.stderr)[-600:])
time.sleep(3)
