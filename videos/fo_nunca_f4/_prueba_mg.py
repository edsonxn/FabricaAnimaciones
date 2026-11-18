# Hoja de prueba del kit mg_fo: cada MG a 3 tiempos sobre un cuadro de gameplay real.
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import mg_fo as F  # noqa: E402

AQUI = Path(__file__).parent
fondo = Image.open(r"C:\FabricaAnimaciones\nucleo\datos\ref_fo\hud_rad_es.jpg").convert("RGB").resize((1920, 1080))
PEG = next(iter(sorted((AQUI / "pegatinas").glob("*.png"))), None) if (AQUI / "pegatinas").exists() else None

casos = [
    ("puesto", F.puesto(15, "Dejar la servoarmadura con el núcleo", "Retira el núcleo de fusión"), 4.0, [], (.5, .3)),
    ("ficha", F.ficha("Fat Man", [("Daño", 468), ("Peso", 30.5), ("Valor", 512)], "Lanza *minibombas*. A tus pies, también a ti.", "INV / ARMAS"), 4.0, [], (.75, .4)),
    ("objetivo", F.objetivo("Libera a Lorenzo Cabot", "Casa Cabot", hecho=True), 3.0, [1.5], (.3, .2)),
    ("special", F.special([5, 6, 5, 1, 1, 1, 1], cambios=[("Suerte", 10), ("Suerte", 11)]), 4.0, [1.0, 2.0], (.5, .5)),
    ("terminal", F.terminal(["> ENTRAR", "Acceso concedido.", "Sujeto: *Lorenzo Cabot*"]), 4.0, [], (.5, .5)),
    ("vats", F.vats([(.5, .2, 87), (.35, .45, 95), (.62, .55, 95), (.45, .85, 95)], crit=.8, titulo="Sanguinario"), 3.5, [], (.5, .5)),
    ("enemigo", F.enemigo("Sanguinario legendario", 1, .45, sub="Legendario"), 3.0, [1.2], (.5, .12)),
    ("rads", F.rads(300, 1.0, .6, titulo="Mar Resplandeciente"), 3.0, [], (.5, .8)),
    ("radio", F.radio(["Radio Diamond City", "Radio Yermo", "Freedom Radio"], 1, "Transmitiendo desde el Yermo..."), 4.0, [], (.5, .5)),
    ("botin", F.botin("Necrófago salvaje errante", ["Chapa (3)", "Bola ocho", "Núcleo de fusión"], 2), 3.0, [], (.7, .5)),
    ("aviso", F.aviso("Núcleo de fusión retirado", "Servoarmadura T-45", icono="ok"), 3.0, [], (.3, .12)),
    ("rejilla", F.rejilla("De cada 100 jugadores", 100, 7, "Solo 7 lo sabían"), 4.0, [1.0], (.5, .5)),
    ("contador", F.contador(450, "de daño", "Minibomba"), 3.0, [], (.5, .5)),
]
if PEG:
    casos.append(("pegatina", F.pegatina(str(PEG), "Prueba"), 3.0, [], (.2, .6)))

tiempos = lambda dur: (0.15, dur * .55, dur - .1)
W, H = 640, 360
hoja = Image.new("RGB", (W * 3, H * len(casos)), (0, 0, 0))
for r, (nom, fn, dur, mk, (cx, cy)) in enumerate(casos):
    for c, t in enumerate(tiempos(dur)):
        lien = fondo.copy().convert("RGBA")
        a = fn(t, dur, mk)
        if a.shape[0] > 2:
            im = Image.fromarray(a[..., [2, 1, 0, 3]], "RGBA")
            x, y = int(cx * 1920 - im.width / 2), int(cy * 1080 - im.height / 2)
            lien.alpha_composite(im, (max(0, x), max(0, y)))
        p = lien.convert("RGB").resize((W, H))
        ImageDraw.Draw(p).text((6, 6), f"{nom} t={t:.2f}", fill=(255, 255, 0))
        hoja.paste(p, (c * W, r * H))
sal = AQUI / "previews" / "prueba_mg_fo.jpg"
sal.parent.mkdir(exist_ok=True)
hoja.save(sal, quality=85)
print(sal)
