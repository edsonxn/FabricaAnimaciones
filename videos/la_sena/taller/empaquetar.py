# -*- coding: utf-8 -*-
"""Empaqueta la presentación «Antes de decir que sí» en UN solo archivo (se abre sin internet en la compu del salón):
index.html + fonts + img + audio + el corto → Antes_de_decir_que_si.html
El corto sale de ../salida/La_sena_MASTER.mp4 (recomprimido a ~crf 25); si todavía no hay MASTER, la diapositiva 9 enseña el aviso.
    python taller/empaquetar.py      (desde videos/la_sena)"""
import base64
import os
import re
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
MASTER = os.path.join("..", "salida", "La_sena_MASTER.mp4")
MIME = {".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2", ".ttf": "font/ttf", ".mp3": "audio/mpeg"}


def uri(p):
    return f"data:{MIME[os.path.splitext(p)[1]]};base64,{base64.b64encode(open(p, 'rb').read()).decode()}"


s = open("index.html", encoding="utf-8").read()
s = re.sub(r'url\(((?:fonts|img)/[\w\-.]+)\)', lambda m: f"url({uri(m.group(1))})", s)
s = re.sub(r'src="((?:img|audio)/[\w\-.]+)"', lambda m: f'src="{uri(m.group(1))}"', s)
dinamicos = sorted(f for f in os.listdir("img") if f.startswith(("c_angel14_camina_", "p_zanate_vuelo_")))
s = s.replace("<script>\n(()=>{", "<script>window.IMG={%s};</script>\n<script>\n(()=>{"
              % ",".join(f'"{f}":"{uri(os.path.join("img", f))}"' for f in dinamicos), 1)

if os.path.exists(MASTER):
    # 720p a ~2 Mbps: con crf 25 a 1080p el grano del acabado daba 299 MB de HTML (21-oct); así queda ~80 MB y abre en una compu modesta
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", MASTER, "-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "slow",
                    "-b:v", "2000k", "-maxrate", "2800k", "-bufsize", "5600k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "video/_ligero.mp4"], check=True)
    assert 'src="video/la_sena.mp4" ' in s
    s = s.replace('src="video/la_sena.mp4" ', '')
    s = s.replace('</body>', '''<script id="cortodata" type="application/octet-stream">%s</script>
<script>
(()=>{const t=document.getElementById('cortodata').textContent,bin=atob(t),u=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)u[i]=bin.charCodeAt(i);
document.getElementById('corto').src=URL.createObjectURL(new Blob([u],{type:'video/mp4'}));document.getElementById('cortodata').remove()})();
</script>
</body>''' % base64.b64encode(open("video/_ligero.mp4", "rb").read()).decode())
    os.remove("video/_ligero.mp4")
else:
    s = s.replace(' src="video/la_sena.mp4"', '')
    print("AVISO: todavía no hay MASTER: la diapositiva 9 enseña «Aquí va el corto». Vuelve a correr esto cuando exista.")

open("Antes_de_decir_que_si.html", "w", encoding="utf-8").write(s)
print(round(os.path.getsize("Antes_de_decir_que_si.html") / 1e6, 1), "MB → taller/Antes_de_decir_que_si.html")
