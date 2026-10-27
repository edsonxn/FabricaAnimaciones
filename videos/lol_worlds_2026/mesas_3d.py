# -*- coding: utf-8 -*-
"""Escenas «MESA» de las jugadas 1-5 (27-oct-2026, el usuario: «combinación de video real intercalando 3D»).

El cuadro congelado de la pausa se proyecta sobre un suelo 3D (nucleo/tactica3d, modo "mesa"): la cámara parte del encuadre
del juego —el corte con el VOD no se nota—, se inclina y gira mientras cada jugador se levanta como ficha con su retrato en su
posición REAL del cuadro (placa de nombre + 0,06 = pies), se dibujan las rutas/intenciones que la narración confirma, y la
cámara vuelve al encuadre original para que el video real siga desde ese mismo cuadro.
Posiciones: placas de nombre de las hojas de medición (scratchpad medir.py, 27-oct). Jugadores fuera de cuadro: no salen.
uso: python videos/lol_worlds_2026/mesas_3d.py [id …]   → tactica3d/mesa_<id>.json + medios/_fuente/mesa_<id>.mp4
"""
import json
import os
import subprocess
import sys

_D = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(_D, "..", ".."))
WEB = "/videos/lol_worlds_2026/"
ICO = WEB + "iconos/"
G = [0, 56.07, 62.73, .5, .5]          # pose de la cámara del juego: giro, inclinación, distancia, x, y


def fuente(n):
    return os.path.join(_D, "medios", "_fuente", f"j{n}.mp4")


def F(jug, camp, eq, x, y, de, sale, **kw):
    return jug, dict(jugador=jug, campeon=camp, equipo=eq, icono=ICO + (camp + ".png" if camp else "equipos/" + kw.get("logo", "HLE") + ".png"),
                     puntos=[[0, x, y]] + kw.get("mueve", []), de=de, sale=sale)


def camara(de, a, giro=-18, incl=36, dist=50, x=.45, y=.45, giro2=14):
    """encuadre del juego → baja e inclina → gira → vuelve al encuadre del juego un segundo antes de `a`"""
    d = a - de
    return [[de] + G, [de + .35] + G, [de + d * .32, giro, incl, dist, x, y], [de + d * .62, giro2, incl + 4, dist * .95, x, y],
            [a - .9] + G, [a] + G]


EQ = [dict(id="A", color="azul"), dict(id="R", color="rojo")]

MESAS = {
    # ---- J1 · KC vs AL 24:36 (j1.mp4 75.0). «…y su definitiva hace algo cruel: los enemigos que toca… se atacan entre ellos»
    "j1": dict(fondo=(1, 75.0), de=277.4, a=282.27, foco=(.42, .42), fichas=[
        F("Busio", "Renata", "A", .38, .375, 277.8, 281.2), F("Yike", "JarvanIV", "A", .47, .365, 277.9, 281.2),
        F("Canna", "Jax", "A", .35, .555, 278.0, 281.2), F("Caliste", "Kalista", "A", .47, .565, 278.1, 281.2),
        F("kyeahoo", "Orianna", "A", .62, .715, 278.2, 281.2),
        F("Shanks", "Akali", "R", .20, .245, 277.9, 281.2), F("Kael", "Neeko", "R", .35, .255, 278.0, 281.2),
        F("Tarzan", "Nocturne", "R", .72, .325, 278.1, 281.2)],
        flechas=[dict(id="ola", pts=[(.38, .37), (.33, .31), (.27, .26)], color="azul", en=278.5, dur=.9, sale=281.2, alto=3.5,
                      grosor=1.6)],
        zonas=[dict(pts=[(.13, .17), (.42, .17), (.44, .33), (.15, .35)], color="rojo", en=279.0, sale=281.2, alfa=.18)],
        etiquetas=[dict(de=278.6, a=281.2, flecha="ola", texto="LA OLA DE RENATA", sub="BUSIO", color="azul", dx=40, dy=-60),
                   dict(de=279.6, a=281.2, u=.28, v=.22, alto=0, texto="SE ATACAN ENTRE ELLOS", color="rojo", dx=-40, dy=120)]),
    # ---- J2 · DK vs T1 40:25 (j2.mp4 74.6). «DK tiene una sola salida: pelear. Ya. Antes de que caiga el dragón.»
    "j2": dict(fondo=(2, 74.6), de=446.6, a=453.32, foco=(.6, .45), fichas=[
        F("ShowMaker", "Viktor", "A", .33, .44, 447.0, 452.3), F("Siwoo", "KSante", "A", .42, .425, 447.1, 452.3),
        F("Lucid", "JarvanIV", "A", .40, .595, 447.2, 452.3), F("Career", "Renata", "A", .45, .64, 447.3, 452.3),
        F("Smash", "Kalista", "A", .41, .665, 447.4, 452.3),
        F("Doran", "Jayce", "R", .67, .29, 447.2, 452.3), F("Peyz", "Caitlyn", "R", .74, .485, 447.3, 452.3),
        F("Keria", "Neeko", "R", .61, .745, 447.4, 452.3)],
        anillos=[dict(u=.84, v=.27, r=.06, color="amarillo", en=447.3, sale=452.3)],
        pilares=[dict(u=.84, v=.27, r=.03, color="morado", en=447.4, sale=452.3, alto=12)],
        flechas=[dict(id="pelear", pts=[(.42, .55), (.58, .44), (.78, .30)], color="azul", en=449.2, dur=.9, sale=452.3, alto=4,
                      grosor=1.5)],
        etiquetas=[dict(de=447.6, a=452.3, u=.84, v=.27, alto=3, texto="ANCIANO", sub="T1 LO ESTÁ TIRANDO", color="amarillo",
                        dx=-170, dy=40),
                   dict(de=449.6, a=452.3, flecha="pelear", texto="¡PELEAR YA!", sub="LA ÚNICA SALIDA DE DK", color="azul",
                        dx=-60, dy=60)]),
    # ---- J3 · KOI vs DK 38:23 (j3.mp4 59.5). «Jojopyun está adelantado, lejos de su equipo… y Career… tiene el ancla lista.»
    "j3": dict(fondo=(3, 59.5), de=617.3, a=622.32, foco=(.32, .32), fichas=[
        F("Jojopyun", "Anivia", "R", .33, .225, 617.6, 621.4), F("Alvaro", "Karma", "R", .14, .32, 617.7, 621.4),
        F("Elyoya", "Trundle", "R", .29, .38, 617.8, 621.4), F("Supa", "Ezreal", "R", .16, .415, 617.9, 621.4),
        F("Myrwn", "Jayce", "R", .19, .53, 618.0, 621.4),
        F("Career", "Nautilus", "A", .475, .16, 617.7, 621.4), F("ShowMaker", "Cassiopeia", "A", .49, .525, 617.9, 621.4),
        F("Smash", "Kaisa", "A", .555, .525, 618.0, 621.4)],
        zonas=[dict(pts=[(.08, .27), (.33, .27), (.33, .58), (.08, .58)], color="rojo", en=617.6, sale=621.4, alfa=.16)],
        flechas=[dict(id="lejos", pts=[(.27, .33), (.30, .28), (.33, .235)], color="rojo", en=617.6, dur=.6, sale=621.4,
                      guion=True, alto=1.5),
                 dict(id="ancla", pts=[(.47, .17), (.40, .19), (.345, .22)], color="azul", en=619.6, dur=.7, sale=621.4, alto=2.5,
                      grosor=1.3)],
        etiquetas=[dict(de=617.9, a=621.4, flecha="lejos", texto="LEJOS DE SU EQUIPO", sub="JOJOPYUN · ANIVIA", color="rojo",
                        dx=-90, dy=70),
                   dict(de=620.0, a=621.4, flecha="ancla", texto="EL ANCLA, LISTA", sub="CAREER · NAUTILUS", color="azul",
                        dx=60, dy=-70)]),
    # ---- J4 · LYON vs Gen.G 34:41 (j4.mp4 84.0). «Mira a Inspired, con Xin Zhao. Inspired se mete… al centro del equipo coreano»
    "j4": dict(fondo=(4, 84.0), de=723.9, a=729.3, foco=(.4, .35), fichas=[
        F("Inspired", "XinZhao", "A", .40, .40, 724.3, 728.4), F("Dhokla", "Olaf", "A", .10, .575, 724.5, 728.4),
        F("Berserker", "Kalista", "A", .65, .555, 724.5, 728.4),
        F("Ruler", "Jhin", "R", .43, .245, 724.4, 728.4), F("Kiin", "Rumble", "R", .32, .34, 724.4, 728.4),
        F("Chovy", "Anivia", "R", .41, .36, 724.5, 728.4), F("Duro", "Alistar", "R", .46, .40, 724.5, 728.4)],
        zonas=[dict(pts=[(.28, .20), (.52, .20), (.52, .45), (.28, .45)], color="rojo", en=725.2, sale=728.4, alfa=.14)],
        pilares=[dict(u=.40, v=.40, r=.02, color="azul", en=724.8, sale=728.4, alto=11)],
        etiquetas=[dict(de=724.8, a=728.4, u=.40, v=.40, alto=0, texto="INSPIRED", sub="XIN ZHAO · AL CENTRO DE GEN.G", color="azul",
                        dx=170, dy=60, icono=ICO + "XinZhao.png"),
                   dict(de=725.4, a=728.4, u=.30, v=.20, alto=0, texto="GEN.G", sub="LOS CINCO JUNTOS", color="rojo",
                        dx=-80, dy=-60)]),
    # ---- J5 · IG vs HLE 24:25 (j5.mp4 61.0). «Mira dónde está Rookie: con Annie, detrás de su equipo.»
    "j5": dict(fondo=(5, 61.0), de=823.03, a=827.82, foco=(.42, .5), fichas=[
        F("Rookie", "Annie", "A", .465, .67, 823.5, 826.9), F("Wei", "Nocturne", "A", .50, .56, 823.6, 826.9),
        F("Meiko", "Lulu", "A", .325, .67, 823.6, 826.9), F("JiaQi", "Yunara", "A", .235, .69, 823.7, 826.9),
        F("Delight", "Renata", "R", .27, .42, 823.7, 826.9), F("HLE", None, "R", .09, .235, 823.8, 826.9),
        F("HLE ", None, "R", .64, .24, 823.8, 826.9), F("HLE  ", None, "R", .545, .465, 823.8, 826.9)],
        pilares=[dict(u=.465, v=.67, r=.02, color="azul", en=824.8, sale=826.9, alto=11)],
        flechas=[dict(id="frente", pts=[(.465, .66), (.48, .60), (.50, .565)], color="azul", en=825.6, dur=.5, sale=826.9,
                      guion=True, alto=1.2)],
        etiquetas=[dict(de=824.9, a=826.9, u=.465, v=.67, alto=0, texto="ROOKIE", sub="ANNIE · DETRÁS DE SU EQUIPO", color="azul",
                        dx=170, dy=40, icono=ICO + "Annie.png")]),
}


def escena(k):
    m = MESAS[k]
    n, s = m["fondo"]
    img = os.path.join(_D, "tactica3d", f"mesa_{k}_fondo.png")
    if not os.path.exists(img):
        subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-y", "-ss", str(s), "-i", fuente(n), "-frames:v", "1", img],
                       check=True)
    E = dict(modo="mesa", de=m["de"], a=m["a"], fondo=WEB + f"tactica3d/mesa_{k}_fondo.png", equipos=EQ,
             fichas=dict(m["fichas"]), camara=camara(m["de"], m["a"], x=m["foco"][0], y=m["foco"][1]))
    for c in ("flechas", "anillos", "zonas", "pilares", "etiquetas"):
        if m.get(c):
            E[c] = m[c]
    return E


if __name__ == "__main__":
    ks = [k for k in sys.argv[1:] if not k.startswith("--")] or list(MESAS)
    for k in ks:
        js = os.path.join(_D, "tactica3d", f"mesa_{k}.json")
        json.dump(escena(k), open(js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if "--json" not in sys.argv:
            subprocess.run([sys.executable, os.path.join(RAIZ, "nucleo", "tactica3d", "render3d.py"), js,
                            os.path.join(_D, "medios", "_fuente", f"mesa_{k}.mp4")], check=True)
