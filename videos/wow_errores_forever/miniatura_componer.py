"""Miniatura final: base de Flow (orco real de Forever, in-game) + interfaz REAL de WoW por código + título + logo de Forever."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H = 1280, 720
im = Image.open("miniatura_ing/orco_v1.png").convert("RGB").resize((W, H), Image.LANCZOS)
# oscurecer la mitad izquierda para el texto
som = Image.new("L", (W, H), 0)
ds = ImageDraw.Draw(som)
for x in range(W):
    ds.line([(x, 0), (x, H)], fill=int(max(0, 150 * (1 - x / (W * .62)))))
im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, som)
d = ImageDraw.Draw(im)


def texto(xy, s, f, relleno, borde=10, sombra=True):
    x, y = xy
    if sombra:
        capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(capa).text((x + 8, y + 10), s, font=f, fill=(0, 0, 0, 190), stroke_width=borde, stroke_fill=(0, 0, 0, 190))
        im.paste(capa.filter(ImageFilter.GaussianBlur(8)), (0, 0), capa.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).text((x, y), s, font=f, fill=relleno, stroke_width=borde, stroke_fill=(0, 0, 0))


IMPACT = "C:/Windows/Fonts/impact.ttf"
texto((46, 40), "25", ImageFont.truetype(IMPACT, 250), (255, 226, 30), 12)
texto((46, 300), "ERRORES", ImageFont.truetype(IMPACT, 150), (255, 226, 30), 10)
texto((52, 470), "QUE ESTÁS COMETIENDO", ImageFont.truetype(IMPACT, 52), (255, 255, 255), 6)

# mensaje rojo de error de la interfaz real de WoW (UIErrorsFrame: rojo con sombra, centrado arriba)
fe = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", 42)
msg = "No puedes hacer eso ahora."
w = d.textlength(msg, font=fe)
texto((int(W * .66 - w / 2), 22), msg, fe, (255, 32, 32), 3, sombra=False)

# logo real de Forever abajo a la izquierda
logo = Image.open(r"C:\googleimagenes\thumbnails\forever_inmersivas\refs\forever_logo.png").convert("RGBA")
logo.thumbnail((300, 170))
im.paste(logo, (40, H - logo.height - 26), logo)
im.save("salida/miniatura.jpg", quality=92)
print("salida/miniatura.jpg", im.size)
