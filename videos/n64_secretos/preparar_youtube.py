# -*- coding: utf-8 -*-
"""Escribe youtube.json con capítulos reales (timeline.json + títulos de los 30 secretos de efectos.py) y una miniatura PROVISIONAL
por código (salida/miniatura.jpg) con ingredientes reales: cuadro de Mario Kart 64 a cuatro jugadores, Mario y el logo de la N64.
    python preparar_youtube.py
"""
import json
import os
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H = 1280, 720
TIT = {"intro": "Un juego que repartía guantes", "h1": "Project Reality: cómo nació", "h2": "Cartucho contra CD", "h3": "El lanzamiento",
       "h4": "Por qué perdió la guerra", "cierre": "Treinta años después"}


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


def capitulos():
    tl = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
    src = open(os.path.join(AQUI, "efectos.py"), encoding="utf-8").read()
    sec = {int(n): t for n, t in re.findall(r'(\d+): \("([^"]+)", "[^"]+"\)', src[src.index("_SEC = {"):src.index("}", src.index("_SEC = {"))])}
    out = []
    for e in tl["escenas"]:
        i = e["id"]
        t = TIT.get(i) or f"#{int(i[1:])} {sec[int(i[1:])]}"
        out.append(f"{mmss(0 if i == 'intro' else e['t0'])} {t}")
    return out


def miniatura():
    fondo = Image.open(os.path.join(AQUI, "pegatinas", "cap_mk64_4j.jpg")).convert("RGB").resize((W, H), Image.LANCZOS)
    im = Image.eval(fondo, lambda v: int(v * .5)).filter(ImageFilter.GaussianBlur(2.5)).convert("RGBA")
    sp = Image.open(os.path.join(AQUI, "pegatinas", "mario.png")).convert("RGBA")
    sp = sp.crop(sp.getbbox())
    e = 660 / sp.height
    sp = sp.resize((int(sp.width * e), 660), Image.LANCZOS)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x, y = W - sp.width - 20, 60
    s.paste((0, 0, 0, 170), (x + 10, y + 12), sp)
    im.alpha_composite(s.filter(ImageFilter.GaussianBlur(10)))
    im.alpha_composite(sp, (x, y))
    logo = Image.open(os.path.join(AQUI, "pegatinas", "n64.png")).convert("RGBA")
    logo = logo.crop(logo.getbbox())
    e = 300 / logo.width
    logo = logo.resize((300, int(logo.height * e)), Image.LANCZOS)
    im.alpha_composite(logo, (60, H - logo.height - 40))
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 160)
    f2 = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 58)
    d.text((46, 10), "30", font=f1, fill=(255, 214, 64), stroke_width=11, stroke_fill="black")
    d.text((46, 180), "SECRETOS", font=f1.font_variant(size=104), fill="white", stroke_width=9, stroke_fill="black")
    d.rounded_rectangle((42, 318, 640, 396), 22, fill=(214, 28, 28), outline="black", width=5)
    d.text((341, 357), "QUE IGNORASTE", font=f2, fill="white", anchor="mm", stroke_width=3, stroke_fill="black")
    os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
    im.convert("RGB").save(os.path.join(AQUI, "salida", "miniatura.jpg"), quality=92)


if __name__ == "__main__":
    cap = "\n".join(capitulos())
    desc = ("Hubo un juego de Nintendo 64 que obligó a repartir guantes. Un Tetris que te medía el pulso con una pinza en la oreja. Una Nintendo 64 "
            "escondida dentro de un mando que solo se vendió en China. Y cuatro muñecos sin cara que acabaron siendo Super Smash Bros. "
            "La Nintendo 64 cumplió 30 años: hoy te cuento cómo nació como Project Reality, por qué perdió la guerra contra PlayStation "
            "y los 30 secretos que seguramente ignoraste.\n\nCAPÍTULOS\n" + cap)
    y = dict(titulo="Los 30 SECRETOS de la Nintendo 64 QUE IGNORASTE",
             titulos_alternativos=["30 secretos de la Nintendo 64 que nadie te contó", "La Nintendo 64 cumple 30 años: 30 secretos que ignoraste"],
             descripcion=desc,
             etiquetas=["Nintendo 64", "N64", "secretos de la Nintendo 64", "Nintendo 64 30 años", "Project Reality", "Ultra 64", "Mario Kart 64",
                        "Super Mario 64", "Super Smash Bros", "64DD", "iQue Player", "Rumble Pak", "Transfer Pak", "Satoru Iwata", "retro",
                        "Crónicas del gaming"],
             categoria="20", idioma="es", formato="historia_y_30_secretos_secuencia_yt", miniatura="salida/miniatura.jpg")
    json.dump(y, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    miniatura()
    print(cap)
