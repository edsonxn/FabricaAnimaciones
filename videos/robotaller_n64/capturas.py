# -*- coding: utf-8 -*-
"""Grabaciones REALES de cómo se hizo n64_secretos (capturas/*.mp4), con la API tapada por robotaller.grabar_real.
Sesiones reales del Robotaller: A = la que lo empezó (mensaje, investigación, guion, voz), B = clips/efectos/render, M = miniatura en Flow.
  python capturas.py [nombre ...]      python capturas.py hoja [nombre ...]      python capturas.py master   (fragmentos del MASTER)"""
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, "../../nucleo")
import robotaller as R

N64 = os.path.abspath("../n64_secretos").replace("\\", "/")
A = "b7ac4dcb-94c2-4716-806b-7f30a251f2b2"
B = "9d043e2d-a59b-4989-b511-3052af41d785"
M = "5ab188b7-d446-4f1e-8136-bb20ad0798a8"


def vivo(s):
    return f"/v2/vivo?sesion={s}"


# el panel de trabajo solo, a letra grande
SOLO_PANTALLA = """#cab,#ses,#etapas,#etaInfo,#lado,#pie{display:none!important}#taller{position:fixed!important;left:-4000px!important;width:1000px!important;height:300px!important}
body{display:block!important;overflow:hidden}#cuerpo{display:block!important;height:100vh!important;padding:0!important}#monitor{height:100vh!important;zoom:1.45;border:0!important}"""
RELOJ = "(()=>{const e=S.ev[S.idx];return e?[e.seq,e.tipo,e.titulo]:null})()"
JEFE = "setInterval(()=>document.querySelectorAll('#mcuerpo *').forEach(x=>{if(!x.children.length&&x.textContent.trim().toUpperCase()==='TÚ')x.textContent='EL JEFE';}),40);"
ENTRAR = "document.querySelector('#fabupd-ok')?.click();document.querySelector('#b-jugar')?.click();document.querySelector('#hoja-x')?.click()"
SIN_AVISO = "[id^=fabupd]{display:none!important}"
CIERRA = [dict(t=t, js=ENTRAR) for t in (0, .5, 1, 1.5, 2.5, 3.5)]
INTERNO = re.compile(r"espectador|viewer|protagonista|adulaci|halag|superior|flatter|persuasi", re.I)    # la receta interna nunca sale


def sin_interno(x):
    if isinstance(x, list):
        return [sin_interno(y) for y in x if not INTERNO.search(json.dumps(y, ensure_ascii=False))]
    if isinstance(x, dict):
        return {k: sin_interno(v) for k, v in x.items()}
    return x


def solo(de, a):
    """Solo esos eventos de la sesión: lo de antes y lo de después no sale."""
    def filtra(u, datos):
        if "/api/v2/agente" in u and isinstance(datos, dict) and "eventos" in datos:
            datos["eventos"] = [e for e in datos["eventos"] if de <= e.get("seq", 0) <= a]
            datos = sin_interno(datos)
        return datos
    return filtra


def repaso(seq, vel=1):
    return f"(()=>{{S.vel={vel};irA({seq});}})()"


def uno(s, seq, dur, imagenes=False):
    """Un solo evento real, a velocidad normal, para que se lea en el monitor."""
    return dict(url=vivo(s), sesion=s, dur=dur, css=SOLO_PANTALLA, imagenes=imagenes, cuadro=solo(seq, seq), espera=8, acciones=[dict(t=.1, js=JEFE + repaso(seq, .5))])


def tramo(s, de, a, ir, vel, dur, pantalla=True, imagenes=False):
    """Repaso real de la sesión de `de` a `a`, empezando en `ir`."""
    return dict(url=vivo(s), sesion=s, dur=dur, css=SOLO_PANTALLA if pantalla else "", imagenes=imagenes, cuadro=solo(de, a), reloj=RELOJ, espera=8,
                acciones=[dict(t=.2, js=JEFE + repaso(ir, vel))])


# ---- páginas con los archivos reales del video (se leen del disco, no se retocan)
def _carta(nombre, cuerpo):
    os.makedirs("capturas", exist_ok=True)
    ruta = os.path.abspath(f"capturas/{nombre}.html")
    open(ruta, "w", encoding="utf-8").write(cuerpo)
    return "file:///" + ruta.replace("\\", "/")


ED = """<!doctype html><meta charset=utf-8><style>html,body{{margin:0;background:#1b1e2b;overflow:hidden}}
.bar{{position:fixed;top:0;left:0;right:0;height:44px;background:#141622;color:#cfd6f0;font:600 19px Consolas;line-height:44px;padding-left:20px;z-index:2}}
pre{{margin:58px 0 0 0;padding:0 22px;font:{tam}px/1.5 Consolas,monospace;white-space:pre-wrap;color:#e8e8e8}}</style>
<div class=bar>{titulo}</div><pre>{cuerpo}</pre>"""


def editor(nombre, ruta, de, a, lexer, titulo, tam=21):
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments import lexers
    lineas = open(ruta, encoding="utf-8").read().splitlines()[de:a]
    cuerpo = highlight("\n".join(lineas), lexers.get_lexer_by_name(lexer), HtmlFormatter(style="monokai", noclasses=True, nowrap=True))
    return _carta(nombre, ED.format(tam=tam, titulo=titulo, cuerpo=cuerpo))


def galeria(nombre, imgs, col, titulo, alto=None, fondo="#10131f"):
    celdas = "".join(f"<img src='file:///{N64}/{i}'>" for i in imgs)
    h = f"height:{alto}px;object-fit:contain;" if alto else ""
    return _carta(nombre, f"""<!doctype html><meta charset=utf-8><style>html,body{{margin:0;background:{fondo};overflow:hidden;font-family:'Segoe UI'}}
    .t{{position:fixed;top:0;left:0;right:0;height:46px;background:#141622;color:#cfd6f0;font:600 20px Consolas;line-height:46px;padding-left:20px;z-index:2}}
    .g{{display:grid;grid-template-columns:repeat({col},1fr);gap:8px;padding:56px 8px 8px}} img{{width:100%;{h}background:#222;border-radius:6px}}</style>
    <div class=t>{titulo}</div><div class=g>{celdas}</div>""")


def pegatinas():
    ps = sorted(f for f in os.listdir(f"{N64}/pegatinas") if f.lower().endswith((".png", ".jpg", ".webp")))
    return galeria("pegatinas", [f"pegatinas/{p}" for p in ps], 10, f"n64_secretos / pegatinas / {len(ps)} imágenes reales", alto=150, fondo="#2a2f45")


def miniaturas():
    return _carta("miniaturas", f"""<!doctype html><meta charset=utf-8><style>html,body{{margin:0;height:100%;background:#10131f;color:#f5f7ff;font-family:'Segoe UI';overflow:hidden}}
    .c{{position:absolute;top:120px;width:46%;text-align:center}} img{{width:100%;border-radius:14px;box-shadow:0 10px 40px #000}}
    .e{{font:800 38px 'Segoe UI';margin-bottom:22px;letter-spacing:3px}}</style>
    <div class=c style="left:2.5%"><div class=e style="color:#ff5d73">CON CÓDIGO</div><img src='file:///{N64}/salida/miniatura_codigo.jpg'></div>
    <div class=c style="right:2.5%"><div class=e style="color:#7df3e1">CON FLOW</div><img src='file:///{N64}/salida/miniatura.jpg'></div>""")


CUENTA = """<!doctype html><meta charset=utf-8><style>html,body{margin:0;height:100%;background:#10131f;color:#f5f7ff;font-family:'Segoe UI';overflow:hidden}
.c{position:absolute;top:170px;width:44%;text-align:center;border-radius:28px;padding:40px 0 50px}
.n{font:900 170px 'Segoe UI';line-height:1.05} .q{font:800 46px 'Segoe UI';letter-spacing:4px;margin-top:10px} .s{font:600 34px 'Segoe UI';opacity:.8;margin-top:14px}
.v{position:absolute;top:360px;left:50%;transform:translateX(-50%);font:900 64px 'Segoe UI';color:#4a5478}</style>
<div class=c style="left:3%;background:#1d2a44"><div class=q style="color:#5bc0ff">EL JEFE</div><div class=n style="color:#5bc0ff">34</div><div class=s>palabras · 6 mensajes</div></div>
<div class=v>VS</div>
<div class=c style="right:3%;background:#2b2142"><div class=q style="color:#b388ff">TOKEN</div><div class=n style="color:#b388ff">1 106</div><div class=s>acciones · 6 sesiones</div></div>"""


def scroll(dur, px, desde=0.0, paso=.1):
    n = int(dur / paso)
    return [dict(t=desde + i * paso, js=f"scrollTo(0,{i * px})") for i in range(n)]


TOMAS = {
    # sesión A: del mensaje al guion y la voz
    "mensaje": lambda: uno(A, 1, 6),
    "investiga": lambda: tramo(A, 1, 157, 94, 3, 22),
    "ayudante": lambda: uno(A, 24, 6),
    "cambio_cuenta": lambda: uno(A, 383, 6),
    "cierre_a": lambda: tramo(A, 383, 386, 384, .5, 9),
    "escribe_guion": lambda: uno(A, 163, 7),
    "voz_eleven": lambda: uno(A, 169, 6),
    "whisper": lambda: tramo(A, 169, 196, 180, 1, 16),
    "relevo_a": lambda: tramo(A, 165, 179, 173, .8, 12),
    "ayudantes_clips": lambda: tramo(A, 196, 203, 199, .6, 9),
    "kit_mg": lambda: tramo(A, 50, 71, 52, .8, 14, imagenes=True),
    "mapas_sesion": lambda: tramo(A, 214, 235, 216, 1.5, 14, imagenes=True),
    # sesión B: efectos, mapas, chequeo y render
    "fx_hojas": lambda: tramo(B, 60, 134, 72, 1.2, 18, imagenes=True),
    "relevo_b": lambda: tramo(B, 160, 170, 163, .8, 9),
    "render": lambda: tramo(B, 172, 182, 178, .8, 10),
    # sesión M: la miniatura en Flow
    "si_flow": lambda: uno(M, 75, 6),
    "flow": lambda: tramo(M, 75, 121, 84, 1.5, 16),
    "flow_imgs": lambda: tramo(M, 116, 119, 116, .5, 10, imagenes=True),
    # los archivos reales del video
    "investigacion": lambda: dict(url=editor("investigacion", f"{N64}/investigacion.md", 0, 140, "markdown", "n64_secretos / investigacion.md", 19), dur=14, acciones=scroll(14, 3)),
    "guion_n64": lambda: dict(url=editor("guion_n64", f"{N64}/guion.py", 45, 130, "python", "n64_secretos / guion.py"), dur=14, acciones=scroll(14, 2.4)),
    "chequeo": lambda: dict(url=editor("chequeo", f"{N64}/previews/chequeo_narracion.md", 0, 80, "markdown", "n64_secretos / chequeo de narración", 20), dur=10, acciones=scroll(10, 2)),
    "hojas_clips": lambda: dict(url=galeria("hojas_clips", [f"previews/medios_0{i}.jpg" for i in range(1, 10)], 3, "n64_secretos / 170 clips del juego que nombra la voz"),
                                dur=14, imagenes=True, espera=1.5, acciones=scroll(14, 4)),
    "pegatinas": lambda: dict(url=pegatinas(), dur=12, imagenes=True, espera=1.5, acciones=scroll(12, 3)),
    "mapas": lambda: dict(url=galeria("mapas", ["mapas/yoshi_valley.jpg", "mapas/MK64_SpecialCup_RainbowRoad.jpg", "mapas/MK64_StarCup_BowsersCastle.jpg",
                                                  "mapas/MK64_MushroomCup_MooMooFarm.jpg", "mapas/MK64_FlowerCup_ChocoMountain.jpg", "mapas/MK64_SpecialCup_DKsJungleParkway.jpg"], 3,
                                       "n64_secretos / mapas reales"), dur=8, imagenes=True, espera=1.5),
    "mg_hojas": lambda: dict(url=galeria("mg_hojas", [f"previews/fx_{i:02d}.jpg" for i in range(1, 12)], 2, "n64_secretos / animaciones y efectos encima del juego"),
                             dur=14, imagenes=True, espera=1.5, acciones=scroll(14, 5)),
    "miniaturas": lambda: dict(url=miniaturas(), dur=6, imagenes=True, espera=1.5),
    "cuenta": lambda: dict(url=_carta("cuenta", CUENTA), dur=3, espera=.3),
    # el panel
    "montaje": lambda: dict(url="/?embed=montaje&v=n64_secretos", dur=12, espera=7,
                            acciones=[dict(t=.5, js="[...document.querySelectorAll('button')].find(b=>b.textContent.includes('Reproducir'))?.click()")]),
}

# fragmentos del MASTER (aún programado: se cortan del archivo local). nombre: (desde, dur, con_audio)
MASTER = {"m_intro": (0.4, 9, False), "m_guantes": (1063.0, 10, False), "m_yoshi": (560.5, 12, True), "m_iwata": (1318.0, 8, False),
          "m_tetris": (1098.0, 8, False), "m_cierre": (1410.5, 8, False), "m_h1": (52.0, 8, False)}


def master():
    src = f"{N64}/salida/n64_secretos_MASTER.mp4"
    for n, (a, d, audio) in MASTER.items():
        subprocess.run([R.FFMPEG, "-y", "-loglevel", "error", "-ss", str(a), "-t", str(d), "-i", src, *([] if audio else ["-an"]), "-vf", "scale=1600:900,fps=30",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"capturas/{n}.mp4"], check=True)
        hoja(n)


def hoja(n):
    salida = f"previews/cap_{n}.jpg"
    dur = float(subprocess.run([R.FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"capturas/{n}.mp4"],
                               capture_output=True, text=True).stdout)
    subprocess.run([R.FFMPEG, "-y", "-loglevel", "error", "-i", f"capturas/{n}.mp4", "-vf", f"fps=6/{dur:.2f},scale=640:-1,tile=2x3", "-frames:v", "1", salida], check=True)
    print(salida)


if __name__ == "__main__":
    pide = sys.argv[1:] or list(TOMAS)
    if pide[0] == "hoja":
        for n in pide[1:] or TOMAS:
            hoja(n)
        sys.exit()
    if pide[0] == "master":
        os.makedirs("capturas", exist_ok=True)
        master()
        sys.exit()
    for n in pide:
        t = TOMAS[n]()
        R.grabar_real(f"capturas/{n}.mp4", t["url"], t["dur"], t.get("acciones", ()), w=t.get("w", 1600), h=t.get("h", 900), escala=t.get("escala", 1.5),
                      sesion=t.get("sesion"), espera=t.get("espera", 2.0), imagenes=t.get("imagenes", False), css=t.get("css", ""), cuadro=t.get("cuadro"), reloj=t.get("reloj"))
        hoja(n)
