# -*- coding: utf-8 -*-
"""APOYOS del motor SECUENCIA (Crónicas de Warcraft y luego Tamriel/Runa): una imagen ENCIMA del gameplay cuando la voz
nombra algo. Heredado del sistema viejo (`C:\\googleimagenes\\estudio_apoyos.js`, receta en su CLAUDE.md § «Apoyos»).
Se declaran en videos/<v>/efectos.py y la capa de efectos (secuencia_fx) los compone como FX `imagen` con entrada deslizada:

  APOYOS = [
    dict(en="Venenos y Ganzúa", wowhead="classic/5060"),          # tooltip REAL de Wowhead (es-MX; "classic/es/5060" = España;
                                                                  #   "classic/spell/1234" = hechizo)
    dict(en="Coldflame Saber", dur=7, tarjeta=dict(titulo="Coldflame Saber", calidad="oro", icono="inv_sword_17",
         lineas=["Sable", dict(t="Equipar: ...", c="verde")], pie="cita en cursiva")),   # SOLO datos verificados del guion
    dict(en="overgear", web="https://overgear.com/games/wow"),     # captura de una web (1920x1080)
    dict(en="el barón Filargenta", img="https://.../Baron.jpg", titulo="Barón Filargenta"),   # imagen suelta con marco dorado
  ]
  opcionales: dur (s, 4.5) · size (fracción del ancho: tarjeta .56, web .80, img .34) · x, y (centro, 0..1) · anim ("slide"|"fade")

  python fab.py <v> apoyos             genera lo que falte en apoyos/<hash>.png y hace la hoja previews/fx_NN.jpg (MÍRALA)
  python fab.py <v> apoyos --rehacer   vuelve a generar todos (p. ej. tras cambiar el CSS)

Estilo aprobado por el usuario (sistema viejo, 7-oct-2026): el objeto es el protagonista -> centro, 56-64 % del ancho; a un lado
(x=.80, size .26-.38) solo retratos o imágenes chicas. Tope ~30 apoyos en 11-12 min. Calidad desconocida = "oro".
Wowhead bloquea las páginas, pero el endpoint de tooltips nether.wowhead.com responde; los íconos salen de wow.zamimg.com.
"""
import hashlib
import html
import json
import os
import re
import sys

try:
    import guion as _g
    W, H = (1080, 1920) if getattr(_g, "FORMATO", "horizontal") == "vertical" else (1920, 1080)
except Exception:
    W, H = 1920, 1080
CARPETA = "apoyos"
TAM = dict(wowhead=.56, tarjeta=.56, web=.80, img=.34)      # ancho por defecto (fracción del cuadro)
CALIDAD = dict(gris="#9d9d9d", blanco="#ffffff", verde="#1eff00", azul="#0070dd", morado="#a335ee", naranja="#ff8000",
               oro="#e6cc80", amarillo="#ffd100")
CARD_CSS = """
*{box-sizing:border-box} html,body{margin:0;background:transparent}
#card{display:inline-flex;align-items:flex-start;gap:10px;padding:26px}
.ico{width:64px;height:64px;border-radius:8px;border:2px solid #b8b8b8;box-shadow:0 6px 18px rgba(0,0,0,.7);background:#111 center/cover;flex:none}
.tt{width:430px;background:rgba(6,10,28,.93);border:2px solid #b0b0b0;border-radius:9px;padding:14px 16px 15px;
    font:20px/1.36 'Segoe UI','Trebuchet MS',Verdana,sans-serif;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.75);text-shadow:0 1px 2px #000}
.tt.ancha{width:560px}
.tt b.t,.tt b[class^=q]{display:block;font-size:24px;line-height:1.2;margin-bottom:3px;font-weight:700}
.tt .l{display:flex;justify-content:space-between;gap:14px} .tt .pie{margin-top:8px;color:#ffd100;font-style:italic}
.tt table{border-collapse:collapse;width:100%} .tt td,.tt th{padding:0;font:inherit;font-weight:400;text-align:left;vertical-align:top} .tt th{text-align:right}
.tt a{color:inherit;text-decoration:none}
.q0{color:#9d9d9d}.q1{color:#fff}.q2{color:#1eff00}.q3{color:#0070dd}.q4{color:#a335ee}.q5{color:#ff8000}.q6,.q7{color:#e6cc80}.q{color:#ffd100}
.whtt-sellprice,.whtt-extra:not(.whtt-ilvl){display:none !important}
#card.foto{flex-direction:column;align-items:center}
.foto img{display:block;max-width:900px;max-height:900px;border:3px solid #c9a227;border-radius:10px;box-shadow:0 12px 34px rgba(0,0,0,.8)}
.foto .cap{max-width:900px;margin-top:10px;text-align:center;font:700 30px 'Georgia',serif;color:#ffd100;text-shadow:0 2px 4px #000,0 0 12px #000}
"""
_OCULTAR_BANNERS = ("() => { for (const e of document.querySelectorAll('[id*=cookie i],[class*=cookie i],[id*=consent i],"
                    "[class*=consent i],iframe[src*=chat i]')) e.remove(); }")


def tipo(a):
    return next(k for k in ("wowhead", "tarjeta", "web", "img") if k in a)


def ruta(a):
    """apoyos/<hash>.png: el nombre depende solo del CONTENIDO (no del momento), así reordenar no obliga a regenerar."""
    k = tipo(a)
    clave = json.dumps({k: a[k], "titulo": a.get("titulo")}, ensure_ascii=False, sort_keys=True)
    return os.path.join(CARPETA, f"{k}_{hashlib.md5(clave.encode('utf-8')).hexdigest()[:10]}.png")


def _icono(icono):
    if not icono:
        return None
    if re.match(r"^https?://", icono):
        return icono
    if os.path.exists(icono):
        return "file:///" + os.path.abspath(icono).replace("\\", "/")
    return f"https://wow.zamimg.com/images/wow/icons/large/{icono.lower()}.jpg"


def _tarjeta_html(t):
    col = lambda c: CALIDAD.get(c, c if (c or "").startswith("#") else "#ffffff")
    lineas = []
    for l in t.get("lineas", []):
        o = {"t": l} if isinstance(l, str) else l
        der = f"<span>{html.escape(o['der'])}</span>" if o.get("der") else ""
        lineas.append(f'<div class="l" style="color:{col(o.get("c"))}"><span>{html.escape(o["t"])}</span>{der}</div>')
    pie = f'<div class="pie">"{html.escape(t["pie"])}"</div>' if t.get("pie") else ""
    return (f'<b class="t" style="color:{col(t.get("calidad", "oro"))}">{html.escape(t["titulo"])}</b>' + "".join(lineas) + pie,
            _icono(t.get("icono")), bool(t.get("ancha")))


def _wowhead(ref):
    import requests
    m = re.fullmatch(r"(?:(.+?)/)?(?:(item|spell|npc|object)/)?(\d+)", str(ref))
    if not m:
        raise SystemExit(f"apoyos: wowhead inválido «{ref}» (usa 5060, \"classic/5060\" o \"classic/spell/1234\")")
    pre = m.group(1) or ""
    if not re.search(r"(^|/)(es|mx|en)$", pre):                 # español de Latinoamérica por defecto (nombres del guion)
        pre = (pre + "/mx").lstrip("/")
    pre = re.sub(r"(^|/)en$", "", pre)
    url = f"https://nether.wowhead.com/{pre + '/' if pre else ''}tooltip/{m.group(2) or 'item'}/{m.group(3)}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    if r.status_code != 200:
        raise SystemExit(f"apoyos: Wowhead respondió {r.status_code} para {url}")
    d = r.json()
    if not d.get("tooltip"):
        raise SystemExit(f"apoyos: Wowhead no trae tooltip para {ref}")
    # HTML de un tercero: fuera scripts y manejadores antes de pintarlo (la página no navega a ningún lado)
    seguro = re.sub(r"<script[\s\S]*?</script>", "", d["tooltip"], flags=re.I)
    seguro = re.sub(r"\son\w+=\"[^\"]*\"", "", seguro)
    return seguro, _icono(d.get("icon")), d.get("name")


def generar(lista, rehacer=False):
    """Genera los PNG que falten. Devuelve [(ruta, descripción)]."""
    pend = [a for a in lista if rehacer or not os.path.exists(ruta(a))]
    hechos = []
    if not pend:
        return hechos
    from playwright.sync_api import sync_playwright
    os.makedirs(CARPETA, exist_ok=True)
    with sync_playwright() as p:
        nav = None
        for canal in ("chrome", "msedge", None):
            try:
                nav = p.chromium.launch(channel=canal, headless=True) if canal else p.chromium.launch(headless=True)
                break
            except Exception:
                continue
        if nav is None:
            raise SystemExit("apoyos: no pude abrir Chrome/Edge headless con Playwright")
        for a in pend:
            k, dst = tipo(a), ruta(a)
            if k == "web":
                pg = nav.new_page(viewport={"width": 1600, "height": 900}, device_scale_factor=W / 1600)
                pg.goto(a["web"], wait_until="networkidle", timeout=60000)
                pg.wait_for_timeout(1500)
                pg.evaluate(_OCULTAR_BANNERS)            # oculta avisos de cookies/chat SIN aceptarlos
                pg.screenshot(path=dst)
                pg.close()
                hechos.append((dst, a["web"]))
                continue
            if k == "img":
                if re.match(r"^https?://", a["img"]):
                    src = a["img"]
                else:   # archivo local incrustado: la página (set_content) no puede cargar file://
                    import base64
                    ext = os.path.splitext(a["img"])[1].lower().strip(".").replace("jpg", "jpeg") or "png"
                    src = f"data:image/{ext};base64," + base64.b64encode(open(a["img"], "rb").read()).decode()
                cap = f'<div class="cap">{html.escape(a["titulo"])}</div>' if a.get("titulo") else ""
                cuerpo, desc = f'<div id="card" class="foto"><img src="{src}">{cap}</div>', a["img"]
            else:
                if k == "wowhead":
                    inner, ico, nombre = _wowhead(a["wowhead"])
                    ancha, desc = False, f"wowhead {a['wowhead']} = {nombre}"
                else:
                    inner, ico, ancha = _tarjeta_html(a["tarjeta"])
                    desc = f"tarjeta {a['tarjeta']['titulo']}"
                ic = f'<div class="ico" style="background-image:url(\'{ico}\')"></div>' if ico else ""
                cuerpo = f'<div id="card">{ic}<div class="tt{" ancha" if ancha else ""}">{inner}</div></div>'
            pg = nav.new_page(viewport={"width": 1000, "height": 1100}, device_scale_factor=2)
            pg.set_content(f'<!doctype html><meta charset="utf-8"><style>{CARD_CSS}</style>{cuerpo}', wait_until="networkidle",
                           timeout=30000)
            pg.locator("#card").screenshot(path=dst, omit_background=True)
            pg.close()
            hechos.append((dst, desc))
        nav.close()
    return hechos


def main(args):
    sys.path.insert(0, os.getcwd())
    if not os.path.exists("efectos.py"):
        raise SystemExit("Este video no tiene efectos.py")
    import importlib
    lista = list(getattr(importlib.import_module("efectos"), "APOYOS", []))
    if not lista:
        raise SystemExit("efectos.py no declara APOYOS")
    for dst, desc in generar(lista, "--rehacer" in args):
        print(f"  {dst}  <- {desc}")
    print(f"{len(lista)} apoyos listos en {CARPETA}/")
    import secuencia_fx
    secuencia_fx.hoja()


if __name__ == "__main__":
    main(sys.argv[1:])
