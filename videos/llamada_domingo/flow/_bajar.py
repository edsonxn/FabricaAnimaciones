# baja URLs firmadas de Flow. Uso: python flow/_bajar.py <carpeta_o_plantilla> < lineas («nombre uuid?query»)
import sys, subprocess, os
plant = sys.argv[1]            # p. ej. flow/esc/{}.jpg
txt = sys.stdin.read().replace("\n", "\n")
for ln in txt.strip().splitlines():
    nom, q = ln.split(" ", 1)
    q = q.strip().strip('"')
    sig = q.split("Signature=")[1]
    if len(sig) % 4:
        q += "=" * (4 - len(sig) % 4)
    tipo = "video" if plant.endswith(".mp4") else "image"
    url = f"https://flow-content.google/{tipo}/{q}"
    dst = plant.format(nom)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    r = subprocess.run(["curl", "-s", "-f", "-o", dst, url])
    print(nom, "OK" if r.returncode == 0 and os.path.getsize(dst) > 5000 else f"FALLO {r.returncode}", os.path.getsize(dst) if os.path.exists(dst) else 0)
