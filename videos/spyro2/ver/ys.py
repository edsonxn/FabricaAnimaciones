import subprocess, sys, json, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
q = sys.argv[1]; n = sys.argv[2] if len(sys.argv)>2 else "6"
r = subprocess.run(["yt-dlp","--flat-playlist","--dump-json",f"ytsearch{n}:{q}"],capture_output=True,text=True,encoding="utf-8")
for l in r.stdout.splitlines():
    try: d=json.loads(l)
    except: continue
    print(d.get("id"), d.get("duration"), d.get("channel"), "|", d.get("title"))
