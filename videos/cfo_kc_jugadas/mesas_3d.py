# -*- coding: utf-8 -*-
"""Escenas «MESA» de CFO vs KC (2 mesas: j1 y j2) (modo "mesa" de nucleo/tactica3d, como videos/lol_worlds_2026/mesas_3d.py): el cuadro
congelado de la pausa se proyecta sobre un suelo 3D, la cámara baja y gira, cada jugador se levanta como ficha con su retrato
en su posición REAL del cuadro (placa de nombre + 0,06 = pies) y la cámara vuelve al encuadre del juego para que el VOD siga.
Posiciones: previews/cuadros/j*_<t>.jpg (rejilla.py, 27-oct). Tiempos del video en TIEMPOS (los pone efectos.py tras `tiempo`).
uso: python videos/cfo_kc_worlds/mesas_3d.py [id …]   → tactica3d/mesa_<id>.json + medios/_fuente/mesa_<id>.mp4
"""
import json
import os
import subprocess
import sys

_D = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(_D, "..", ".."))
WEB = "/videos/cfo_kc_worlds/"
ICO = WEB + "iconos/"
G = [0, 56.07, 62.73, .5, .5]          # pose de la cámara del juego: giro, inclinación, distancia, x, y
sys.path.insert(0, _D)
from tiempos_mesas import TIEMPOS  # noqa: E402  (de, a) de cada mesa en el video


def fuente(n):
    return os.path.join(_D, "medios", "_fuente", f"j{n}.mp4")


def F(jug, camp, eq, x, y, d0=.4):
    return jug, dict(jugador=jug, campeon=camp, equipo=eq, icono=ICO + camp + ".png", puntos=[[0, x, y]], d0=d0)


def camara(de, a, giro=-18, incl=36, dist=50, x=.45, y=.45, giro2=14):
    d = a - de
    return [[de] + G, [de + .35] + G, [de + d * .32, giro, incl, dist, x, y], [de + d * .62, giro2, incl + 4, dist * .95, x, y],
            [a - .9] + G, [a] + G]


EQ = [dict(id="A", color="azul"), dict(id="R", color="rojo")]

# en/sale de flechas, zonas y etiquetas: segundos DESDE el inicio de la mesa (se suman a `de`)
sys.path.insert(0, os.path.join(RAIZ, "nucleo", "tactica3d"))
import rastros_vod as RV  # noqa: E402


def RUTA(n, t_ref, puntos):
    """ruta medida en cuadros anteriores (pies, fracción) llevada al cuadro t_ref con la cámara (investigacion/cam_j<n>.json)"""
    cam = json.load(open(os.path.join(_D, "investigacion", f"cam_j{n}.json")))
    return RV.ruta_en(cam, t_ref, puntos)


MESAS = {
    # ---- J1 · TL vs CFO 34:16 (j1 t=56): pies medidos el 28-oct en previews/cuadros/r_j1_56.jpg (rejilla fina, UN cuadro)
    "j1": dict(fondo=(1, 56.0), foco=(.42, .55), fichas=[
        F("Rest", "Rumble", "R", .45, .63), F("Shad0w", "Qiyana", "R", .45, .72), F("Doggo", "Aphelios", "R", .54, .60),
        F("Kino", "Alistar", "R", .47, .49), F("POUT", "Viktor", "R", .635, .34),
        F("Yeon", "Jhin", "A", .25, .50), F("Josedeodo", "LeeSin", "A", .29, .42)],
        anillos=[dict(u=.39, v=.64, r=.07, color="amarillo", en=.4)],
        flechas=[dict(id="robo", pts=[(.29, .43), (.33, .53), (.37, .62)], color="azul", en=1.0, dur=.8, guion=True, alto=2.5,
                      grosor=1.3),
                 dict(id="tapa", pts=[(.47, .49), (.39, .46), (.31, .43)], color="rojo", en=2.0, dur=.8, alto=3, grosor=1.5)]
        # rutas: 34:04 → 34:16 en la MISMA toma (r_j1_44 y r_j1_56); si cruzan un corte, no se dibujan
        + [dict(id=i, pts=pts, color="rojo", en=e, dur=.9, alto=1.5, grosor=1.2)
           for i, pts, e in (("ruta_rest", RUTA(1, 56, [(44, .56, .62), (56, .45, .63)]), 3.0),
                             ("ruta_kino", RUTA(1, 56, [(44, .505, .58), (56, .47, .49)]), 3.2)) if len(pts) >= 2],
        etiquetas=[dict(en=.5, u=.39, v=.64, alto=0, texto="EL ANCESTRAL", sub="CFO LO ESTÁ HACIENDO", color="amarillo", dx=-170, dy=70),
                   dict(en=1.3, flecha="robo", texto="JOSEDEODO", sub="QUIERE ROBARLO", color="azul", dx=-170, dy=-40),
                   dict(en=2.3, flecha="tapa", texto="KINO", sub="LE TAPA EL PASO", color="rojo", dx=40, dy=-80)]),
    # ---- J2 · T1 vs CFO 24:20 (j3 t=48): pies medidos en r_j3_48.jpg; Rest y Peyz no se ven bien (fuera)
    "j2": dict(fondo=(3, 48.0), foco=(.48, .58), fichas=[
        F("Doggo", "Kaisa", "R", .44, .43), F("Kino", "Alistar", "R", .365, .52),
        F("Keria", "Rakan", "A", .42, .71), F("Oner", "Vi", "A", .67, .75)],
        anillos=[dict(u=.44, v=.43, r=.06, color="rojo", en=.4)],
        flechas=[dict(id="paso", pts=[(.365, .52), (.38, .58), (.40, .64)], color="rojo", en=1.0, dur=.7, alto=3, grosor=1.5),
                 dict(id="keria", pts=[(.42, .70), (.43, .56), (.44, .46)], color="azul", en=2.0, dur=.8, guion=True, alto=2.5,
                      grosor=1.3),
                 dict(id="oner", pts=[(.66, .74), (.55, .58), (.46, .46)], color="azul", en=2.4, dur=.8, guion=True, alto=2.5,
                      grosor=1.3)],
        etiquetas=[dict(en=.5, u=.44, v=.43, alto=0, texto="DOGGO", sub="EL QUE HAY QUE PROTEGER", color="rojo", dx=-190, dy=-50),
                   dict(en=1.3, flecha="paso", texto="KINO", sub="UN PASO AL FRENTE", color="rojo", dx=-180, dy=30),
                   dict(en=2.4, flecha="oner", texto="T1", sub="TODOS A POR DOGGO", color="azul", dx=150, dy=-30)]),
}


def escena(k):
    m = MESAS[k]
    de, a = TIEMPOS[k]
    n, s = m["fondo"]
    img = os.path.join(_D, "tactica3d", f"mesa_{k}_fondo.png")
    os.makedirs(os.path.dirname(img), exist_ok=True)
    if not os.path.exists(img):
        subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-y", "-ss", str(s), "-i", fuente(n), "-frames:v", "1", img],
                       check=True)
    fin = a - 1.0                      # todo sale antes de que la cámara vuelva al encuadre del juego
    fichas = {}
    for i, (j, f) in enumerate(m["fichas"]):
        f = dict(f)
        f["de"] = round(de + f.pop("d0") + .08 * i, 2)
        f["sale"] = round(fin, 2)
        fichas[j] = f
    E = dict(modo="mesa", de=de, a=a, fondo=WEB + f"tactica3d/mesa_{k}_fondo.png", equipos=EQ, fichas=fichas,
             camara=camara(de, a, x=m["foco"][0], y=m["foco"][1]))
    for c in ("flechas", "anillos", "zonas", "etiquetas"):
        if m.get(c):
            out = []
            for e in m[c]:
                e = dict(e)
                e["en" if c != "etiquetas" else "de"] = round(de + e.pop("en"), 2)
                if c == "etiquetas":
                    e["a"] = round(fin, 2)
                else:
                    e["sale"] = round(fin, 2)
                out.append(e)
            E[c] = out
    return E


if __name__ == "__main__":
    ks = [k for k in sys.argv[1:] if not k.startswith("--")] or list(MESAS)
    for k in ks:
        js = os.path.join(_D, "tactica3d", f"mesa_{k}.json")
        json.dump(escena(k), open(js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if "--json" not in sys.argv:
            subprocess.run([sys.executable, os.path.join(RAIZ, "nucleo", "tactica3d", "render3d.py"), js,
                            os.path.join(_D, "medios", "_fuente", f"mesa_{k}.mp4")], check=True)
