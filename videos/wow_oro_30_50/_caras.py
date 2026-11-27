# -*- coding: utf-8 -*-
"""Caras de «15 FARMEOS de ORO del 30 al 50» (regla del 25-nov-2026: toda tarjeta de personaje enseña la CARA; RGC §R44).
caras/<slug>.png = recorte de pegatinas/<slug>.png (modelo 3D de Wowhead Forever) a cara + hombros, DESDE ARRIBA.
- Humanoides de pie (centauros, ogros, gnomos, goblins, PNJ, múrlocs): franja superior, alto = máx(0,75 x ancho, 36 % del alto).
- Bestias de lado o de frente: caja a mano (fracciones x0, y0, x1, y1 de la pegatina) medida en una rejilla del 10 % (25-nov).
python _caras.py [slug…] → caras/*.png + previews/caras_check.jpg (pegatina | cara, para mirarla)."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
PEG, CAR = os.path.join(D, "pegatinas"), os.path.join(D, "caras")
os.makedirs(CAR, exist_ok=True)
CAJA = {
    "aguijonero_scorpok": (0.0, 0.35, 0.75, 1.0),
    "arana_niebla_negra": (0.2, 0.0, 0.85, 0.65), "ermitana_niebla_negra": (0.2, 0.0, 0.85, 0.65),
    "cavapozos_fangorroca": (0.0, 0.38, 0.55, 1.0), "mordedor_brillavalva": (0.0, 0.38, 0.55, 1.0),
    "tortuga_brillavalva": (0.0, 0.38, 0.55, 1.0),
    "cazadora_llanagreste": (0.0, 0.25, 0.55, 0.85), "coyote_llanuras": (0.0, 0.25, 0.55, 0.85),
    "merodeador_coyote": (0.0, 0.25, 0.55, 0.85), "jaguar_pantano": (0.0, 0.25, 0.55, 0.85),
    "hiena_llagapata": (0.0, 0.3, 0.55, 0.95), "hiena_risitas": (0.0, 0.3, 0.55, 0.95), "zarposea_magram": (0.0, 0.3, 0.55, 0.95),
    "oso_cueracero": (0.0, 0.4, 0.6, 1.0), "patriarca_cueracero": (0.0, 0.4, 0.6, 1.0),
    "gorila_velo_bruma": (0.1, 0.05, 0.75, 0.65), "gorila_velo_bruma_anciano": (0.1, 0.05, 0.75, 0.65),
    "simio_groddoc": (0.05, 0.05, 0.7, 0.65), "tronador_groddoc": (0.05, 0.05, 0.7, 0.65),
    "destripador_negro": (0.1, 0.45, 0.75, 0.95), "roc": (0.1, 0.45, 0.75, 0.95), "roc_fuego": (0.1, 0.45, 0.75, 0.95),
    "cria_lethlor": (0.0, 0.25, 1.0, 0.75),
    "reptador_arena": (0.15, 0.0, 0.85, 0.85), "reptador_arenas_sur": (0.1, 0.1, 0.85, 0.85),
    "sootfur": (0.1, 0.1, 0.9, 0.7),
    "elemental_roca": (0.2, 0.0, 0.8, 0.5), "elemental_roca_inferior": (0.2, 0.0, 0.8, 0.5),
    "elemental_roca_superior": (0.2, 0.0, 0.8, 0.5),
    "murloc_marisma": (0.1, 0.0, 0.9, 0.55), "comecarnes_marisma": (0.1, 0.0, 0.9, 0.55),
    "oraculo_marisma": (0.1, 0.0, 0.9, 0.55), "vomitatintas_marisma": (0.1, 0.0, 0.9, 0.55),
}


def cara(slug):
    im = Image.open(os.path.join(PEG, slug + ".png")).convert("RGBA")
    W, H = im.size
    if slug in CAJA:
        x0, y0, x1, y1 = CAJA[slug]
        c = im.crop((round(x0 * W), round(y0 * H), round(x1 * W), round(y1 * H)))
    else:
        c = im.crop((0, 0, W, min(H, round(max(0.75 * W, 0.36 * H)))))
    b = c.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if b:
        c = c.crop(b)
    c.save(os.path.join(CAR, slug + ".png"))
    return c


def main(solo=None):
    cred = json.load(open(os.path.join(PEG, "_creditos.json"), encoding="utf-8"))
    slugs = [k for k, v in cred.items() if v.get("tipo") == "criatura" and (not solo or k in solo)]
    pares = [(s, Image.open(os.path.join(PEG, s + ".png")).convert("RGBA"), cara(s)) for s in slugs]
    cols, cw, ch = 4, 420, 230
    h = Image.new("RGB", (cols * cw, ((len(pares) + cols - 1) // cols) * ch), (40, 40, 40))
    d = ImageDraw.Draw(h)
    fnt = ImageFont.truetype("arialbd.ttf", 16)
    for n, (s, p, c) in enumerate(pares):
        x, y = (n % cols) * cw + 5, (n // cols) * ch + 5
        for k, im in enumerate((p, c)):
            im = im.copy()
            im.thumbnail((195, 195))
            bg = Image.new("RGBA", im.size, (90, 90, 90, 255))
            bg.alpha_composite(im)
            h.paste(bg.convert("RGB"), (x + k * 205, y))
        d.text((x, y + 200), s, fill=(255, 220, 80), font=fnt)
    h.save(os.path.join(D, "previews", "caras_check.jpg"), quality=85)
    print(len(pares), "caras")


if __name__ == "__main__":
    main(set(sys.argv[1:]) or None)
