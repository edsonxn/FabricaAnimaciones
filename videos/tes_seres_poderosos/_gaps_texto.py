import json, re, subprocess, sys
b = json.load(open("beats.json", encoding="utf-8"))
out = subprocess.run([sys.executable, "_huecos.py"], capture_output=True, text=True, encoding="utf-8", errors="ignore").stdout
for ln in out.splitlines()[1:]:
    m = re.match(r"\s*([\d.]+) -\s*([\d.]+)\s+\(\s*([\d.]+)", ln)
    if not m or float(m.group(3)) < 4.0: continue
    a, z = float(m.group(1)), float(m.group(2))
    print(f"--- {a:.1f}-{z:.1f} ({float(m.group(3)):.1f}s)")
    for x in b:
        if x["t1"] > a and x["t0"] < z:
            print(f"   {x['id']} {x['t0']:.1f}-{x['t1']:.1f}: {x['texto']}")
