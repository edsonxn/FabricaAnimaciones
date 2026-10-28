# -*- coding: utf-8 -*-
"""Escenas «MESA» de las 4 jugadas (modo "mesa" de nucleo/tactica3d, como videos/lol_worlds_2026/mesas_3d.py): el cuadro
congelado de la pausa se proyecta sobre un suelo 3D, la cámara baja y gira, cada jugador se levanta como ficha con su retrato
en su posición REAL del cuadro (placa de nombre + 0,06 = pies) y la cámara vuelve al encuadre del juego para que el VOD siga.
Posiciones: previews/cuadros/j*_<t>.jpg (rejilla.py, 27-oct). Tiempos del video en TIEMPOS (los pone efectos.py tras `tiempo`).
uso: python videos/ig_lyon_worlds/mesas_3d.py [id …]   → tactica3d/mesa_<id>.json + medios/_fuente/mesa_<id>.mp4
"""
import json
import os
import subprocess
import sys

_D = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(_D, "..", ".."))
WEB = "/videos/ig_lyon_worlds/"
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
MESAS = {
    # ---- J1 · IG vs HLE 24:36 (j1 t=99): el Olaf de Zeus con su definitiva; IG retrocede y espera
    "j1": dict(fondo=(1, 99.0), foco=(.42, .42), fichas=[
        F("Zeus", "Olaf", "R", .344, .57), F("Zeka", "Lissandra", "R", .208, .495), F("Gumayusi", "Kalista", "R", .417, .36),
        F("Rookie", "Annie", "A", .609, .325), F("Wei", "Nocturne", "A", .5625, .23), F("Meiko", "Lulu", "A", .63, .556)],
        anillos=[dict(u=.344, v=.57, r=.07, color="rojo", en=.5)],
        flechas=[dict(id="atras", pts=[(.60, .33), (.66, .27), (.72, .22)], color="azul", en=1.4, dur=.8, alto=2.5, grosor=1.3),
                 dict(id="atras2", pts=[(.63, .55), (.69, .50), (.75, .46)], color="azul", en=1.6, dur=.8, alto=2.5, grosor=1.3)],
        etiquetas=[dict(en=.7, u=.344, v=.57, alto=0, texto="ZEUS · OLAF", sub="INMUNE AL CONTROL", color="rojo", dx=-150, dy=90),
                   dict(en=1.9, flecha="atras", texto="IG RETROCEDE", sub="Y ESPERA", color="azul", dx=90, dy=-60)]),
    # ---- J2 · TSW vs IG 22:47 (j2 t=112.6): cuatro de TSW juntos; la Orianna de Rookie detrás
    "j2": dict(fondo=(2, 112.6), foco=(.33, .36), fichas=[
        F("Dire", "Ryze", "R", .27, .22), F("Hizto", "Qiyana", "R", .23, .25), F("Pun", "Shen", "R", .22, .35),
        F("Bie", "Alistar", "R", .345, .36), F("Eddie", "Ezreal", "R", .135, .545),
        F("TheShy", "KSante", "A", .345, .45), F("Wei", "Nocturne", "A", .375, .43), F("JiaQi", "Ashe", "A", .51, .42),
        F("Meiko", "Seraphine", "A", .54, .40), F("Rookie", "Orianna", "A", .47, .60)],
        zonas=[dict(pts=[(.17, .17), (.38, .17), (.40, .40), (.17, .40)], color="rojo", en=.8, alfa=.18)],
        flechas=[dict(id="onda", pts=[(.47, .58), (.40, .45), (.30, .30)], color="azul", en=2.0, dur=.8, alto=4, grosor=1.5)],
        etiquetas=[dict(en=1.0, u=.27, v=.24, alto=0, texto="CUATRO JUNTOS", sub="TEAM SECRET WHALES", color="rojo", dx=-60, dy=-70),
                   dict(en=2.3, u=.47, v=.60, alto=0, texto="ROOKIE · ORIANNA", sub="LA ONDA DE CHOQUE, LISTA", color="azul",
                        dx=-300, dy=70)]),
    # ---- J3 · LYON vs TSW 15:51 (j3 t=70): LYON en el Heraldo; TSW llega por el río
    "j3": dict(fondo=(3, 70.0), foco=(.45, .4), fichas=[
        F("Dhokla", "KSante", "A", .26, .215), F("Inspired", "Nocturne", "A", .415, .405), F("Berserker", "Ezreal", "A", .55, .675),
        F("Isles", "Alistar", "A", .55, .75), F("Dire", "Ryze", "R", .85, .195)],
        anillos=[dict(u=.38, v=.30, r=.07, color="amarillo", en=.5)],
        flechas=[dict(id="llegan", pts=[(.95, .30), (.82, .32), (.70, .36)], color="rojo", en=1.3, dur=.8, guion=True, alto=1.5,
                      grosor=1.3)],
        etiquetas=[dict(en=.6, u=.38, v=.30, alto=0, texto="HERALDO", sub="LYON LO ESTÁ HACIENDO", color="amarillo", dx=-150, dy=-50),
                   dict(en=1.6, flecha="llegan", texto="TSW LLEGA", sub="A DISPUTARLO", color="rojo", dx=60, dy=-60)]),
    # ---- J4 · LYON vs Gen.G 34:37 (j4 t=138): Gen.G junto sobre el dragón; Dhokla en el flanco
    "j4": dict(fondo=(4, 138.0), foco=(.38, .4), fichas=[
        F("Ruler", "Jhin", "R", .406, .214), F("Duro", "Alistar", "R", .484, .25), F("Canyon", "Qiyana", "R", .375, .37),
        F("Chovy", "Anivia", "R", .443, .37), F("Kiin", "Rumble", "R", .1875, .33),
        F("Dhokla", "Olaf", "A", .068, .43), F("Inspired", "XinZhao", "A", .396, .60), F("Isles", "Renata", "A", .604, .59),
        F("Berserker", "Kalista", "A", .635, .74)],
        zonas=[dict(pts=[(.33, .16), (.53, .16), (.53, .42), (.33, .42)], color="rojo", en=.8, alfa=.15)],
        flechas=[dict(id="flanco", pts=[(.07, .43), (.17, .40), (.30, .36)], color="azul", en=1.6, dur=.8, guion=True, alto=2,
                      grosor=1.3),
                 dict(id="entra", pts=[(.40, .60), (.41, .50), (.42, .38)], color="azul", en=2.3, dur=.7, alto=4, grosor=1.6)],
        etiquetas=[dict(en=1.0, u=.43, v=.20, alto=0, texto="GEN.G", sub="LOS CINCO, SOBRE EL DRAGÓN", color="rojo", dx=120, dy=-60),
                   dict(en=1.8, flecha="flanco", texto="DHOKLA", sub="ESCONDIDO EN EL FLANCO", color="azul", dx=-40, dy=80),
                   dict(en=2.6, flecha="entra", texto="INSPIRED", sub="XIN ZHAO · AL CENTRO", color="azul", dx=150, dy=40)]),
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
