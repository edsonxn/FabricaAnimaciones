"""Hoja de prueba del kit mg_lol sobre un cuadro real del video (cada pieza en 3 instantes)."""
import sys, os
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import cv2, numpy as np
import mg_lol as L

V = r"C:\FabricaAnimaciones\videos\lol_worlds_2026"
E = os.path.join(V, "iconos", "equipos")
J = os.path.join(V, "pegatinas", "jugadores")
fondo = cv2.imread(os.path.join(V, "previews", "cuadros", "j1_77.0.png"))
fondo = cv2.cvtColor(fondo, cv2.COLOR_BGR2BGRA)

piezas = [
    ("tarjeta", L.tarjeta("Anyone's Legend", "Campeón de China · eliminado", "rojo", logo=os.path.join(E, "AL.png"), dato="0-3"), [.15, .35, 1.4], (.5, .82)),
    ("pegatina", L.pegatina(os.path.join(J, "Canna.png"), "Canna", "azul", logo=os.path.join(E, "KC.png"), sub="Jax · top", tam=430), [.1, .3, 1.5], (.25, .5)),
    ("resultados", L.resultados("Día 1 · ronda 1", [(os.path.join(E, "GEN.png"), "Gen.G", os.path.join(E, "IG.png"), "Invictus", 0),
                                                     (os.path.join(E, "KC.png"), "Karmine Corp", os.path.join(E, "AL.png"), "Anyone's Legend", 0)]), [.3, .8, 2.5], (.5, .5)),
    ("caida", L.caida("China en el día 1", [(os.path.join(E, x + ".png"), n) for x, n in (("AL", "AL"), ("BLG", "BLG"), ("TES", "TES"), ("IG", "IG"))], "0-4"), [.6, 2.3, 4.2], (.5, .5)),
    ("eliminado", L.eliminado(os.path.join(E, "AL.png"), "Anyone's Legend", "Campeón de China · 0-3"), [.6, 1.5, 2.6], (.5, .5)),
    ("apertura", L.apertura("WORLDS 2026", "Todo lo que ha pasado"), [.25, .6, 1.8], (.5, .5)),
    ("versus", L.versus((os.path.join(E, "DK.png"), "DK"), (os.path.join(E, "T1.png"), "T1"), "Dplus KIA vs T1", "Día 2", ganador=0), [.3, .5, 2.0], (.5, .5)),
    ("menu", L.menu([(os.path.join(V, "splash", "Kaisa.jpg"), "Las jugadas", "oro"), (os.path.join(J, "Smash.png"), "Los jugadores", "azul"),
                     (os.path.join(E, "GEN.png"), "Los equipos", "oro"), (os.path.join(E, "T1.png"), "Lo que viene", "rojo")]), [.5, 1.2, 3.0], (.5, .5)),
    ("suiza", L.suiza(), [.6, 2.5, 7.0], (.5, .5)),
]
marcas = {"caida": [.2, 1.0, 1.8, 2.6, 3.4], "eliminado": [1.2, 2.0], "versus": [1.5], "menu": [.3, .7, 1.1, 1.5],
          "suiza": [.3, 1.0, 1.8, 3.0, 4.0, 5.0], "resultados": [.3, 1.0]}
filas = []
for nom, fn, ts, (x, y) in piezas:
    celdas = []
    for t in ts:
        f = fondo.copy()
        im = fn(t, 6.0, marcas.get(nom, []))
        L._sobre(f, im, int(x * 1920 - im.shape[1] / 2), int(y * 1080 - im.shape[0] / 2))
        c = cv2.resize(f, (640, 360))
        cv2.putText(c, f"{nom} {t}s", (8, 22), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 255, 255), 2)
        celdas.append(c)
    filas.append(np.hstack(celdas))
hoja = np.vstack(filas)
cv2.imwrite(os.path.join(V, "previews", "mg_lol_hoja.jpg"), hoja[..., :3], [cv2.IMWRITE_JPEG_QUALITY, 85])
print(hoja.shape)
