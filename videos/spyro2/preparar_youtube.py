# -*- coding: utf-8 -*-
"""Escribe youtube.json con capítulos reales (timeline.json) y la miniatura PROVISIONAL por código de spyro2 (salida/miniatura.jpg).
La de Flow queda pendiente: Flow en el navegador integrado pide aceptar su política, y eso es del usuario.
    python preparar_youtube.py
"""
import json
import os
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
TIT = {"intro": "Una moneda con la cara de un hombre real", "h1": "De Spyro the Dragon a Spyro II", "h2": "Avalar, Ripto y los pilones", "h3": "La música de Stewart Copeland",
       "h4": "Un juego, cuatro nombres", "cierre": "Reignited y A Realm Beyond"}


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def capitulos():
    tl = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
    src = open(os.path.join(AQUI, "guion.py"), encoding="utf-8").read()
    sec = {m.group(1): m.group(2) for m in re.finditer(r'"id": "(s\d\d)", "frases": \[\s*"\[[^\]]*\] Número [^.]*\. ([^"]*?)"', src)}
    out = []
    for e in tl["escenas"]:
        i = e["id"]
        t = TIT.get(i) or f"#{int(i[1:])} {sec[i].rstrip('.')}"
        out.append(f"{mmss(0 if i == 'intro' else e['t0'])} {t}")
    return out


def miniatura():
    fondo = Image.open(os.path.join(AQUI, "pegatinas", "cap_shores.jpg")).convert("RGB")
    fondo = fondo.crop((0, int(fondo.height * .06), fondo.width, int(fondo.height * .94))).resize((W, H), Image.LANCZOS)
    im = Image.eval(fondo, lambda v: int(v * .55)).filter(ImageFilter.GaussianBlur(3)).convert("RGBA")
    moneda = Image.open(os.path.join(AQUI, "pegatinas", "cap_moneda.jpg")).convert("RGB")
    mw, mh = moneda.size
    moneda = moneda.crop((int(mw * .545), int(mh * .17), int(mw * .835), int(mh * .71))).resize((360, 330), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", moneda.size, 0)
    ImageDraw.Draw(m).ellipse((6, 6, 354, 324), fill=255)
    moneda.putalpha(m)
    im.alpha_composite(moneda, (70, 350))
    sp = Image.open(os.path.join(AQUI, "pegatinas", "spyro.png")).convert("RGBA")
    sp = sp.crop(sp.getbbox())
    e = 640 / sp.height
    sp = sp.resize((int(sp.width * e), 640), Image.LANCZOS)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x, y = W - sp.width - 10, 70
    s.paste((0, 0, 0, 170), (x + 10, y + 12), sp)
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    im.alpha_composite(sp, (x, y))
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype("C:/Windows/Fonts/COOPBL.TTF", 150)
    f2 = ImageFont.truetype("C:/Windows/Fonts/COOPBL.TTF", 64)
    d.text((46, 20), "30", font=f1, fill=(255, 214, 64), stroke_width=11, stroke_fill="black")
    d.text((46, 170), "SECRETOS", font=f1.font_variant(size=108), fill="white", stroke_width=9, stroke_fill="black")
    d.rounded_rectangle((42, 278, 620, 352), 22, fill=(214, 28, 28), outline="black", width=5)
    d.text((331, 315), "QUE IGNORASTE", font=f2, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
    im.convert("RGB").save(os.path.join(AQUI, "salida", "miniatura.jpg"), quality=92)


if __name__ == "__main__":
    cap = "\n".join(capitulos())
    desc = ("En Spyro 2 hay una moneda dorada con la cara de un hombre real. Un monje que le pide a un dragón matar a un yeti mientras el texto dice otra cosa. "
            "Un libro de monstruos que nunca llegaron al juego. Y otro juego escondido dentro del disco. Hoy te cuento cómo se hizo Spyro 2: Ripto's Rage "
            "(En busca de los talismanes), por qué tiene tres nombres distintos, y los 30 secretos que seguramente ignoraste.\n\nCAPÍTULOS\n" + cap)
    y = dict(titulo="Spyro 2: su historia y los 30 secretos QUE IGNORASTE",
             titulos_alternativos=["30 secretos de Spyro 2 que nadie te contó", "Spyro 2: la moneda con la cara de un hombre real y 29 secretos más"],
             descripcion=desc,
             etiquetas=["Spyro 2", "Spyro 2 Ripto's Rage", "En busca de los talismanes", "Gateway to Glimmer", "Spyro the Dragon", "Spyro", "secretos de Spyro 2",
                        "PlayStation 1", "PS1", "PSX", "Insomniac Games", "Stewart Copeland", "Ripto", "Moneybags", "A Realm Beyond", "Crónicas del gaming"],
             categoria="20", idioma="es", formato="historia_y_30_secretos_secuencia_yt", miniatura="salida/miniatura.jpg")
    json.dump(y, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    miniatura()
    print(cap[:400])
