# -*- coding: utf-8 -*-
"""Las grabaciones REALES de la fábrica (capturas/*.mp4), con la API tapada por robotaller.grabar_real. Revisar cuadro a cuadro: python capturas.py hoja [nombre]
  python capturas.py [nombre ...]"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, "../../nucleo")
import robotaller as R

SESION = "d1b5e1a2-cd88-4040-ad07-e359775c79b6"
VIVO = f"/v2/vivo?sesion={SESION}"


# el panel de trabajo solo, a letra grande: en el monitor del taller la página entera no se leería
SOLO_PANTALLA = """#cab,#ses,#etapas,#etaInfo,#lado,#pie{display:none!important}#taller{position:fixed!important;left:-4000px!important;width:1000px!important;height:300px!important}
body{display:block!important;overflow:hidden}#cuerpo{display:block!important;height:100vh!important;padding:0!important}#monitor{height:100vh!important;zoom:1.45;border:0!important}"""
RELOJ = "(()=>{const e=S.ev[S.idx];return e?[e.seq,e.tipo,e.titulo]:null})()"
JEFE = "setInterval(()=>document.querySelectorAll('#mcuerpo *').forEach(x=>{if(!x.children.length&&x.textContent.trim().toUpperCase()==='TÚ')x.textContent='EL JEFE';}),40);"   # el panel le dice «tú» a Edson
ENTRAR = "document.querySelector('#fabupd-ok')?.click();document.querySelector('#b-jugar')?.click();document.querySelector('#hoja-x')?.click()"
SIN_AVISO = "[id^=fabupd]{display:none!important}"
CIERRA = [dict(t=t, js=ENTRAR) for t in (0, .5, 1, 1.5, 2.5, 3.5)]
OCULTOS = "[...document.querySelectorAll('button')].find(b=>b.textContent.trim().startsWith('Ocultos'))?.click()"


def tecla(ev, k):
    return f"dispatchEvent(new KeyboardEvent('{ev}',{{key:'{k}'}}))"


INTERNO = re.compile(r"espectador|viewer|protagonista|adulaci|halag|superior|flatter|persuasi", re.I)    # la receta interna nunca sale en un video


def sin_interno(x):
    if isinstance(x, list):
        return [sin_interno(y) for y in x if not INTERNO.search(json.dumps(y, ensure_ascii=False))]
    if isinstance(x, dict):
        return {k: sin_interno(v) for k, v in x.items()}
    return x


def solo(de, a):
    """Solo esos eventos de la sesión: lo que el jefe escribió después no sale."""
    def filtra(u, datos):
        if "/api/v2/agente" in u and isinstance(datos, dict) and "eventos" in datos:
            datos["eventos"] = [e for e in datos["eventos"] if de <= e.get("seq", 0) <= a]
            datos = sin_interno(datos)
        return datos
    return filtra


def uno(seq, dur):
    """Un solo evento real, a velocidad normal, para que se pueda leer en el monitor."""
    return dict(url=VIVO, dur=dur, css=SOLO_PANTALLA, imagenes=True, cuadro=solo(seq, seq), espera=3, acciones=[dict(t=.1, js=JEFE + repaso(seq, .5))])


def repaso(seq, vel=1):
    """Salta a un evento real de la sesión y deja correr el repaso."""
    return f"(()=>{{S.vel={vel};irA({seq});}})()"


def _carta(nombre, cuerpo):
    os.makedirs("capturas", exist_ok=True)
    ruta = os.path.abspath(f"capturas/{nombre}.html")
    open(ruta, "w", encoding="utf-8").write(cuerpo)
    return "file:///" + ruta.replace("\\", "/")


def _codigo():
    """El código real que dibuja a Token, en una vista de editor (no se retoca: se lee del archivo)."""
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import JavascriptLexer
    lineas = open("../../nucleo/panel_vivo.html", encoding="utf-8").read().splitlines()
    i = next(n for n, x in enumerate(lineas) if "POSES={" in x)
    cuerpo = highlight("\n".join(lineas[i:i + 90]), JavascriptLexer(), HtmlFormatter(style="monokai", noclasses=True, nowrap=True))
    return _carta("codigo", f"""<!doctype html><meta charset=utf-8><style>html,body{{margin:0;background:#1b1e2b;overflow:hidden}}
    .bar{{position:fixed;top:0;left:0;right:0;height:44px;background:#141622;color:#cfd6f0;font:600 19px Consolas;line-height:44px;padding-left:20px;z-index:2}}
    pre{{margin:58px 0 0 0;padding:0 22px;font:21px/1.5 Consolas,monospace;white-space:pre;color:#e8e8e8}}</style>
    <div class=bar>panel_vivo.html</div><pre>{cuerpo}</pre>""")


ORGANIGRAMA = """<!doctype html><meta charset=utf-8><style>html,body{margin:0;height:100%;background:#10131f;color:#f5f7ff;font-family:'Segoe UI',sans-serif;overflow:hidden}
.h{position:absolute;top:36px;width:100%;text-align:center;font:800 44px 'Segoe UI';letter-spacing:6px;color:#7df3e1}
.c{position:absolute;left:50%;transform:translateX(-50%);padding:16px 44px;border-radius:18px;font:800 40px 'Segoe UI';white-space:nowrap}
.l{position:absolute;left:50%;width:6px;background:#4a5478;margin-left:-3px}</style>
<div class=h>ORGANIGRAMA</div>
<div class=c style="top:120px;background:#ffd166;color:#10131f">TÚ · junta directiva</div><div class=l style="top:206px;height:44px"></div>
<div class=c style="top:250px;background:#5bc0ff;color:#10131f">Edson · supervisa</div><div class=l style="top:336px;height:44px"></div>
<div class=c style="top:380px;background:#b388ff;color:#10131f">Token · hace todo</div><div class=l style="top:466px;height:44px"></div>
<div class=c style="top:510px;background:#ff5d73;color:#10131f;font-size:34px">Disco duro · agonizando</div>"""

TOMAS = {
    "vivo": lambda: dict(url=VIVO, dur=14, cuadro=solo(19, 111), reloj=RELOJ, espera=3, acciones=[dict(t=.2, js=JEFE + repaso(40, 2))]),
    "clasico": lambda: dict(url="/", dur=13, espera=5, acciones=[dict(t=.1, js=OCULTOS)] + [dict(t=2 + t / 10, js=f"scrollTo(0,{t * 9})") for t in range(110)]),
    "canales": lambda: dict(url="/", dur=12, espera=4, acciones=[dict(t=.1, js="pestana('can')")] + [dict(t=4 + t / 10, js=f"scrollTo(0,{t * 5})") for t in range(80)]),
    "lienzo": lambda: dict(url="/v2", dur=14, espera=6, css=SIN_AVISO, acciones=CIERRA + [dict(t=1, js=OCULTOS)] + [dict(t=2.5 + i * .2, js=f"encuadrar({{x:S.lim.x,y:S.lim.y+S.lim.h*{i * .0075:.4f},w:S.lim.w,h:S.lim.w*.56}},10,1)") for i in range(55)]),
    "montaje": lambda: dict(url="/?embed=montaje&v=majora_mask", dur=12, espera=7, acciones=[dict(t=.5, js="[...document.querySelectorAll('button')].find(b=>b.textContent.includes('Reproducir'))?.click()")]),
    "aldea": lambda: dict(url="/v2/aldea", dur=14, espera=6, css=SIN_AVISO, acciones=CIERRA),
    "fabrica3d": lambda: dict(url="/v2/juego", dur=12, espera=6, css=SIN_AVISO, acciones=CIERRA + [dict(t=4, js=tecla("keydown", "w")), dict(t=7, js=tecla("keyup", "w")), dict(t=7, js=tecla("keydown", "d")), dict(t=9, js=tecla("keyup", "d"))]),
    "movil": lambda: dict(url="/v2/movil", dur=9, w=390, h=844, escala=2, espera=4, css=SIN_AVISO, acciones=CIERRA + [dict(t=2, js="[...document.querySelectorAll('button,a,div')].find(x=>x.textContent.trim().startsWith('En curso')&&x.children.length<3)?.click()")]),
    # de «Sí, arma el piloto» (19) al código, las pruebas y los cuadros revisados: el repaso real de la sesión, rápido
    "como": lambda: dict(url=VIVO, dur=95, css=SOLO_PANTALLA, imagenes=True, cuadro=solo(19, 103), reloj=RELOJ, espera=3,
                        acciones=[dict(t=.2, js=JEFE + repaso(19, 4))]),
    "mensaje": lambda: uno(19, 5),
    "plan": lambda: uno(61, 6),
    "lee": lambda: uno(51, 8),
    "escribe": lambda: uno(40, 8),
    "mira": lambda: uno(96, 7),
    "relevo": lambda: dict(url=VIVO, dur=16, css=SOLO_PANTALLA, cuadro=solo(90, 111), reloj=RELOJ, espera=3, acciones=[dict(t=.2, js=repaso(104, 1))]),
    "codigo": lambda: dict(url=_codigo(), dur=12, acciones=[dict(t=t / 10, js=f"scrollTo(0,{t * 2})") for t in range(120)]),
    "organigrama": lambda: dict(url=_carta("organigrama", ORGANIGRAMA), dur=2, espera=.3),
}


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
    for n in pide:
        t = TOMAS[n]()
        R.grabar_real(f"capturas/{n}.mp4", t["url"], t["dur"], t.get("acciones", ()), w=t.get("w", 1600), h=t.get("h", 900), escala=t.get("escala", 1.5), sesion=SESION, espera=t.get("espera", 2.0),
                      imagenes=t.get("imagenes", False), css=t.get("css", ""), cuadro=t.get("cuadro"), reloj=t.get("reloj"))
        hoja(n)
