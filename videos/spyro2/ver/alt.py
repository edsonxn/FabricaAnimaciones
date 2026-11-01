import subprocess, json, sys, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
for v in sys.argv[1:]:
    r = subprocess.run(["yt-dlp","--skip-download","--dump-json",f"https://youtu.be/{v}"],capture_output=True,text=True,encoding="utf-8",errors="replace")
    try:
        d=json.loads(r.stdout)
        hs=sorted({f.get('height') for f in d['formats'] if f.get('height')})
        print(v, d.get('duration'), max(hs), d.get('uploader'), "|", d['title'][:80])
    except Exception as e:
        print(v, "ERR", r.stderr[-150:])
    time.sleep(2)
