# -*- coding: utf-8 -*-
"""Las 8 «MESAS» del acto A (modo "mesa" de nucleo/tactica3d): el cuadro congelado se proyecta sobre un suelo 3D, la cámara baja y gira,
cada jugador se levanta como ficha en sus PIES medidos (investigacion/datos_*.md, UN cuadro) y la cámara vuelve al encuadre del juego
para que el VOD siga desde ese cuadro. Lo que no tiene coordenada va como etiqueta, nunca como ficha. Rutas solo medidas y en la misma
toma (cam_<fuente>.json). Tiempos en tiempos_mesas.py (los escribe efectos.py). `lotl`: el MURO de Taliyah se levanta con sus puntos medidos.
uso: python videos/lol_semana2/mesas_3d.py [id …] [--json]   → tactica3d/mesa_<id>.json + medios/_fuente/mesa_<id>.mp4
OJO: `t1ko` lee su cuadro de t1_koi_worlds (E:) y `kccf` de cfo_kc_jugadas (C:).
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

_D = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(_D, "..", ".."))
WEB = "/videos/lol_semana2/"
ICO = WEB + "iconos/"
G = [0, 56.07, 62.73, .5, .5]          # pose de la cámara del juego: giro, inclinación, distancia, x, y
sys.path.insert(0, _D)
from tiempos_mesas import TIEMPOS  # noqa: E402  (de, a) de cada mesa en el video

EXT = {"t1_g2j2": ("t1_koi_worlds", "g2_j2"), "kc_g2j4": ("cfo_kc_jugadas", "g2_j4")}


def fuente(n):
    if n in EXT:
        return os.path.join(RAIZ, "videos", EXT[n][0], "medios", "_fuente", EXT[n][1] + ".mp4")
    return os.path.join(_D, "medios", "_fuente", f"{n}.mp4")


_TL = json.load(open(os.path.join(_D, "timeline.json"), encoding="utf-8"))
_FR = {f["key"]: f for e in _TL["escenas"] for f in e["frases"]}


def _n(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def W(k, palabra, mesa, n=0):
    """segundos desde el inicio de la mesa hasta que la voz dice `palabra`"""
    hits = [w for w in _FR[k]["words"] if _n(w["w"]).startswith(_n(palabra))]
    return round(max(.3, hits[n]["s"] - TIEMPOS[mesa][0]), 2)


def F(jug, camp, eq, x, y, d0=.4):
    return jug, dict(jugador=jug, campeon=camp, equipo=eq, icono=ICO + camp + ".png", puntos=[[0, x, y]], d0=d0)


def camara(de, a, giro=-18, incl=36, dist=50, x=.45, y=.45, giro2=14):
    d = a - de
    return [[de] + G, [de + .35] + G, [de + d * .32, giro, incl, dist, x, y], [de + d * .62, giro2, incl + 4, dist * .95, x, y],
            [a - .9] + G, [a] + G]


EQ = [dict(id="A", color="azul"), dict(id="R", color="rojo")]
sys.path.insert(0, os.path.join(RAIZ, "nucleo", "tactica3d"))
import rastros_vod as RV  # noqa: E402


def RUTA(n, t_ref, puntos):
    """ruta medida en cuadros anteriores (pies, fracción) llevada al cuadro t_ref con la cámara (investigacion/cam_<n>.json)"""
    cam = json.load(open(os.path.join(_D, "investigacion", f"cam_{n}.json")))
    return RV.ruta_en(cam, t_ref, puntos)


def ruta(id_, n, t_ref, puntos, color, en):
    pts = RUTA(n, t_ref, puntos)
    return [dict(id=id_, pts=pts, color=color, en=en, dur=.9, alto=1.5, grosor=1.2)] if len(pts) >= 2 else []


def tira(pts, ancho=.009):
    """franja fina alrededor de una polilínea medida: crearZona la levanta como un muro"""
    return [(u, v - ancho) for u, v in pts] + [(u, v + ancho) for u, v in reversed(pts)]


def elipse(u, v, ru, rv, n=20):
    import math
    return [(round(u + ru * math.cos(2 * math.pi * k / n), 4), round(v + rv * math.sin(2 * math.pi * k / n), 4)) for k in range(n)]


# lotl_j1 t 17,6: los puntos del dato van por la CRESTA de la roca; +.012 = línea central de la banda (.315-.345 en x .30, recorte 31-oct)
MURO = [(u, round(v + .012, 3)) for u, v in ((.206, .337), (.288, .320), (.369, .314), (.438, .303), (.531, .292), (.638, .253), (.744, .237))]

MESAS = {
    # ---- T1 vs KOI 19:16 (t1_g2j2 t 46): T1 azul. Solo Jojopyun y Elyoya tienen pies; Faker = su flecha, Oner sin coordenada en este cuadro
    "t1ko": dict(fondo=("t1_g2j2", 46.0), foco=(.47, .55), fichas=[
        F("Jojopyun", "Viktor", "R", .58, .64), F("Elyoya", "XinZhao", "R", .33, .41)],
        flechas=[dict(id="faker", pts=[(.505, .80), (.49, .66), (.46, .52)], color="azul", en=lambda: W("t1ko_j_2", "Faker", "t1ko"), dur=.9, alto=2.5, grosor=1.4)],
        etiquetas=[dict(en=lambda: W("t1ko_j_2", "Faker", "t1ko") + .4, flecha="faker", texto="FAKER · ORIANNA", sub="POR EL FLANCO", color="azul", dx=170, dy=-30),
                   dict(en=.8, u=.33, v=.41, alto=0, texto="KOI", sub="VAN TODOS POR ONER", color="rojo", dx=-170, dy=-60)]),
    # ---- LYON vs IG 28:01 (lyig_j1 t 22): IG azul, LYON rojo. Pies del dato J1-P1; Isles → JiaQi medido
    "lyig1": dict(fondo=("lyig_j1", 22.0), foco=(.42, .50), fichas=[
        F("Dhokla", "Olaf", "R", .30, .46), F("Meiko", "Nautilus", "A", .38, .475), F("JiaQi", "Jhin", "A", .365, .585),
        F("Rookie", "Annie", "A", .515, .635), F("Wei", "LeeSin", "A", .34, .745), F("Isles", "Alistar", "R", .53, .33),
        F("Saint", "Taliyah", "R", .77, .275)],
        flechas=[dict(id="isles", pts=[(.53, .33), (.4475, .4575), (.365, .585)], color="rojo", en=lambda: W("lyig_j1_1", "distancia", "lyig1"), dur=.8, guion=True, alto=2.5, grosor=1.4)],
        etiquetas=[dict(en=lambda: W("lyig_j1_1", "Dhokla", "lyig1"), u=.30, v=.46, alto=0, texto="DHOKLA", sub="POR LA IZQUIERDA", color="rojo", dx=-170, dy=-40),
                   dict(en=lambda: W("lyig_j1_1", "Isles", "lyig1"), u=.53, v=.33, alto=0, texto="ISLES", sub="ALISTAR", color="rojo", dx=170, dy=-50)]),
    # ---- LYON vs IG 02:34 (lyig_j2 t 24): LYON azul. Rutas medidas en la toma 13.9→28.9; círculo azul sin atribuirlo (⚠ datos)
    "lyig2": dict(fondo=("lyig_j2", 24.0), foco=(.38, .52), fichas=[
        F("Berserker", "Lucian", "A", .33, .48), F("Meiko", "Lux", "R", .375, .51), F("Inspired", "XinZhao", "A", .39, .39),
        F("Isles", "Milio", "A", .30, .65), F("JiaQi", "Caitlyn", "R", .51, .645)],
        zonas=[dict(pts=elipse(.305, .51, .10, .145), color="azul", en=1.0, alfa=.14)],
        flechas=ruta("r_meiko", "lyig_j2", 24, [(23.0, .40, .515), (24.0, .375, .51), (24.5, .30, .54), (25.0, .285, .55)], "rojo", 1.4)
        + ruta("r_insp", "lyig_j2", 24, [(22.0, .30, .275), (23.0, .37, .30), (24.0, .39, .39)], "azul", .9)
        + ruta("r_bers", "lyig_j2", 24, [(22.0, .25, .535), (23.0, .325, .455), (24.0, .33, .48)], "azul", .7),
        etiquetas=[dict(en=1.6, u=.375, v=.51, alto=0, texto="MEIKO", sub="SE PASA AL OTRO LADO", color="rojo", dx=190, dy=-50),
                   dict(en=.9, u=.33, v=.48, alto=0, texto="BERSERKER", sub="ATRAPADO", color="azul", dx=-180, dy=-40)]),
    # ---- KC vs CFO 19:57 (kc_g2j4 t 15): CFO azul, KC rojo. Canna = flecha desde el minimapa, sin anillo (⚠ datos)
    "kccf": dict(fondo=("kc_g2j4", 15.0), foco=(.50, .55), fichas=[
        F("Doggo", "Caitlyn", "A", .175, .56), F("Busio", "Lulu", "R", .43, .57), F("kyeahoo", "Viktor", "R", .43, .39)],
        flechas=[dict(id="canna", pts=[(.95, .70), (.80, .66), (.62, .60)], color="rojo", en=lambda: W("kccf_j_1", "Canna", "kccf"), dur=1.0, guion=True, alto=2.5, grosor=1.5)],
        etiquetas=[dict(en=.7, u=.43, v=.57, alto=0, texto="BUSIO", sub="SE ADELANTA", color="rojo", dx=-170, dy=40),
                   dict(en=lambda: W("kccf_j_1", "miran", "kccf"), u=.175, v=.56, alto=0, texto="CFO", sub="LO ESPERA", color="azul", dx=170, dy=-60),
                   dict(en=lambda: W("kccf_j_1", "Canna", "kccf") + .5, flecha="canna", texto="CANNA · CAMILLE", sub="POR LA RETAGUARDIA", color="rojo", dx=-30, dy=-70)]),
    # ---- BLG vs TES 28:49 (blte_j3 t 23): BLG azul. Los cuatro grupos se encienden con la voz
    "blte3": dict(fondo=("blte_j3", 23.0), foco=(.34, .45), fichas=[
        F("Xun", "MonkeyKing", "A", .107, .207), F("Knight", "Leblanc", "A", .209, .466), F("Bin", "KSante", "A", .346, .443),
        F("Viper", "Ashe", "A", .371, .686), F("ON", "Seraphine", "A", .532, .679), F("Tian", "JarvanIV", "R", .485, .44),
        F("369", "Aatrox", "R", .392, .48), F("JackeyLove", "Lucian", "R", .394, .207), F("Zhuo", "Milio", "R", .439, .20)],
        anillos=[dict(u=.107, v=.207, r=.05, color="azul", en=lambda: W("blte_peor_1", "Xun", "blte3")),
                 dict(u=.209, v=.466, r=.05, color="azul", en=lambda: W("blte_peor_1", "Knight", "blte3")),
                 dict(u=.346, v=.443, r=.05, color="azul", en=lambda: W("blte_peor_1", "Bin", "blte3")),
                 dict(u=.45, v=.68, r=.11, color="azul", en=lambda: W("blte_peor_1", "Viper", "blte3"))],
        etiquetas=[dict(en=.5, u=.30, v=.44, alto=0, texto="CUATRO GRUPOS", sub=None, color="amarillo", dx=0, dy=-150)]),
    # ---- BLG vs TES 36:23 (blte_j2 t 31): rutas 36:18 → 36:23 en la misma toma. Tian y Creme sin pies: etiqueta. Nunca decir «cebo»
    "blte2": dict(fondo=("blte_j2", 31.0), foco=(.42, .50), fichas=[
        F("Viper", "Ashe", "A", .50, .685), F("ON", "Seraphine", "A", .525, .55), F("Knight", "Leblanc", "A", .43, .415),
        F("Bin", "KSante", "A", .30, .46), F("369", "Aatrox", "R", .607, .568), F("JackeyLove", "Lucian", "R", .248, .443),
        F("Zhuo", "Milio", "R", .28, .27)],
        flechas=ruta("r_jl", "blte_j2", 31, [(26, .350, .330), (31, .248, .443)], "rojo", .8)
        + ruta("r_bin", "blte_j2", 31, [(26, .387, .411), (31, .300, .460)], "azul", 1.2)
        + ruta("r_vip", "blte_j2", 31, [(26, .608, .606), (31, .500, .685)], "azul", 3.0),
        etiquetas=[dict(en=1.4, u=.30, v=.46, alto=0, texto="BIN Y XUN", sub="TRAS JACKEYLOVE", color="azul", dx=-170, dy=60),
                   dict(en=lambda: W("blte_j_2", "369", "blte2"), u=.607, v=.568, alto=0, texto="369, TIAN Y CREME", sub="SOBRE VIPER Y ON", color="rojo", dx=-90, dy=130)]),
    # ---- LOS vs Liquid 34:40 (lotl_j1 t 17,6): Liquid azul, LOS rojo. El muro, con sus puntos medidos. Nunca «el muro frenó a Morgan»
    "lotl": dict(fondo=("lotl_j1", 17.6), foco=(.38, .47), fichas=[
        F("CoreJJ", "Lulu", "A", .297, .312), F("Yeon", "Yunara", "A", .241, .626), F("Ackerman", "Renata", "R", .322, .459),
        F("Duduhh", "Kalista", "R", .463, .609), F("Morgan", "Gnar", "A", .711, .426)],
        zonas=[dict(pts=tira(MURO, .005), color="amarillo", en=.2, alfa=.75, alto=1.8)],
        pilares=[dict(u=u, v=v, r=.012, color="amarillo", en=.25 + .1 * i, alto=3.2) for i, (u, v) in enumerate(MURO)],
        etiquetas=[dict(en=.5, u=.438, v=.315, alto=3.2, texto="EL MURO DE TALIYAH", sub=None, color="amarillo", dx=0, dy=-70),
                   dict(en=lambda: W("lotl_j_2", "CoreJJ", "lotl"), u=.297, v=.312, alto=0, texto="AL NORTE", sub="COREJJ Y QUID", color="azul", dx=-170, dy=-70),
                   dict(en=lambda: W("lotl_j_2", "Yeon", "lotl"), u=.241, v=.626, alto=0, texto="AL SUR, DENTRO", sub="YEON Y JOSEDEODO", color="azul", dx=-170, dy=60)]),
    # ---- G2 vs Hanwha 21:43 (g2hl_j1 t 23,7): HLE azul. BrokenBlade y Labrov no separables: sin ficha
    "g2hl": dict(fondo=("g2hl_j1", 23.7), foco=(.42, .47), fichas=[
        F("Kanavi", "JarvanIV", "A", .44, .285), F("Zeka", "Swain", "A", .345, .635), F("Zeus", "Ambessa", "A", .455, .665)],
        flechas=ruta("r_kan", "g2hl_j1", 23.7, [(17.0, .325, .285), (21.5, .41, .31), (23.7, .44, .285)], "azul", lambda: W("g2hl_j_1", "Kanavi", "g2hl")),
        etiquetas=[dict(en=lambda: W("g2hl_j_1", "Swain", "g2hl"), u=.345, v=.635, alto=0, texto="ZEKA", sub="SWAIN · DEFINITIVA", color="azul", dx=-170, dy=40),
                   dict(en=lambda: W("g2hl_j_1", "Kanavi", "g2hl"), u=.44, v=.285, alto=0, texto="KANAVI", sub="LLEGA POR ARRIBA", color="azul", dx=170, dy=-50)]),
    # ---- KC vs KOI 29:16 (kcmk_j3 t 12): KC azul. Caliste en duda: etiqueta, sin ficha. Ruta de Myrwn medida en la toma 1.8→22.1
    "kcmk3": dict(fondo=("kcmk_j3", 12.0), foco=(.45, .45), fichas=[
        F("Busio", "Seraphine", "A", .335, .31), F("Yike", "MonkeyKing", "A", .52, .27), F("Elyoya", "Sejuani", "R", .54, .58),
        F("Supa", "Zeri", "R", .65, .76)],
        flechas=ruta("r_myrwn", "kcmk_j3", 12, [(13.0, .40, .62), (15.0, .43, .38)], "rojo", lambda: W("kcmk_j3_1", "Myrwn", "kcmk3")),
        etiquetas=[dict(en=.6, u=.37, v=.43, alto=0, texto="CALISTE", sub="ATURDIDO", color="azul", dx=-180, dy=30),
                   dict(en=.9, u=.47, v=.33, alto=0, texto="EL ANCIANO", sub="14 366 DE VIDA", color="amarillo", dx=120, dy=-90),
                   dict(en=lambda: W("kcmk_j3_1", "Myrwn", "kcmk3"), u=.40, v=.62, alto=0, texto="MYRWN · CAMILLE", sub="POR LA IZQUIERDA", color="rojo", dx=-190, dy=50)]),
    # ---- KC vs KOI 37:16 (kcmk_j1 t 35): la pelea partida en dos. Caliste y kyeahoo bajo el HUD (y > .76) y Canna fuera de lectura: etiquetas
    "kcmk1": dict(fondo=("kcmk_j1", 35.0), foco=(.50, .50), fichas=[
        F("Supa", "Zeri", "R", .49, .41), F("Jojopyun", "Cassiopeia", "R", .38, .37)],
        zonas=[dict(pts=elipse(.45, .28, .15, .13), color="rojo", en=.6, alfa=.14), dict(pts=elipse(.58, .68, .15, .10), color="azul", en=1.0, alfa=.14)],
        etiquetas=[dict(en=.7, u=.45, v=.20, alto=0, texto="ARRIBA", sub="CANNA SOBRE SUPA", color="azul", dx=170, dy=-70),
                   dict(en=lambda: W("kcmk_j1_3", "por", "kcmk1"), u=.58, v=.70, alto=0, texto="ABAJO", sub="CALISTE Y KYEAHOO", color="azul", dx=190, dy=40)]),
    # ---- LOS vs LYON 40:14 (loly_j1 t 39): LOS azul, LYON rojo. Curse y Duduhh en duda: Curse etiqueta. Ruta de Berserker en la toma 35.1→53.5
    "loly1": dict(fondo=("loly_j1", 39.0), foco=(.60, .45), fichas=[
        F("Berserker", "Yunara", "R", .66, .40), F("Feisty", "Leblanc", "A", .645, .31), F("Ackerman", "Karma", "A", .535, .345),
        F("Inspired", "LeeSin", "R", .475, .57), F("Isles", "Lulu", "R", .63, .60)],
        flechas=ruta("r_bers1", "loly_j1", 39, [(36.0, .575, .60), (39.0, .66, .40)], "rojo", .8),
        etiquetas=[dict(en=.7, u=.745, v=.45, alto=0, texto="CURSE", sub="3 % DE VIDA", color="azul", dx=170, dy=30),
                   dict(en=lambda: W("loly_j1_1", "Isles", "loly1"), u=.63, v=.60, alto=0, texto="ISLES", sub="ATURDIDO", color="rojo", dx=170, dy=70),
                   dict(en=lambda: W("loly_j1_1", "Esta", "loly1", 1), u=.66, v=.40, alto=0, texto="BERSERKER", sub="SOLO CONTRA TODOS", color="rojo", dx=-200, dy=-90)]),
    # ---- LOS vs LYON 33:45 (loly_j3 t 31,5): LYON azul. Ackerman en duda: etiqueta. Su definitiva es narración, no se dibuja
    "loly3": dict(fondo=("loly_j3", 31.5), foco=(.34, .55), fichas=[
        F("Curse", "Chogath", "R", .46, .45), F("Feisty", "Ryze", "R", .31, .44), F("Berserker", "Lucian", "A", .27, .65),
        F("Isles", "Milio", "A", .135, .66), F("Dhokla", "KSante", "A", .36, .70)],
        etiquetas=[dict(en=.7, u=.45, v=.42, alto=0, texto="ACKERMAN", sub="SEGÚN LOS NARRADORES, YA A SALVO", color="rojo", dx=190, dy=-60),
                   dict(en=lambda: W("loly_j3_1", "definitiva", "loly3"), u=.36, v=.68, alto=0, texto="LYON", sub="LO ESTÁ ESPERANDO", color="azul", dx=-30, dy=80)]),
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
    for c in ("flechas", "anillos", "zonas", "pilares", "etiquetas"):
        if m.get(c):
            out = []
            for e in m[c]:
                e = dict(e)
                en = e.pop("en")
                en = min(en() if callable(en) else en, a - de - 1.6)      # que alcance a leerse antes de volver al juego
                e["en" if c != "etiquetas" else "de"] = round(de + en, 2)
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
