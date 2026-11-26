# -*- coding: utf-8 -*-
"""Las «MESAS» de tl_josedeodo (copia de videos/lol_semana2/mesas_3d.py). FORMAS NUEVAS (10-nov-2026): cam="bullet" = la cámara
da MEDIA VUELTA alrededor de la pelea congelada (bullet time, forma 2); cam="cenital" = la mesa sube en picada hasta la vista desde
arriba y ahí funde con la Grieta 3D (forma 1, VOD → 3D sin corte). Antes: las 8 «MESAS» del acto A (modo "mesa" de nucleo/tactica3d): el cuadro congelado se proyecta sobre un suelo 3D, la cámara baja y gira,
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
WEB = "/videos/tl_josedeodo/"
ICO = WEB + "iconos/"
G = [0, 56.07, 62.73, .5, .5]          # pose de la cámara del juego: giro, inclinación, distancia, x, y
sys.path.insert(0, _D)
from tiempos_mesas import TIEMPOS  # noqa: E402  (de, a) de cada mesa en el video

EXT = {"cfo_j1": ("cfo_kc_worlds", "j1")}          # lotl_j1 copiado a medios/_fuente (de lol_semana2)


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


def camara(de, a, giro=-18, incl=36, dist=50, x=.45, y=.45, giro2=14, modo="normal"):
    d = a - de
    if modo == "bullet":          # forma 2: media vuelta alrededor de la pelea (de -95° a +95°), baja y se acerca en el centro
        return [[de] + G, [de + .3] + G, [de + d * .2, -95, 30, 44, x, y], [de + d * .45, 0, 22, 38, x, y],
                [de + d * .7, 95, 30, 44, x, y], [a - .9] + G, [a] + G]
    if modo == "orbita":          # 25-nov (el usuario: «cámara 3D rotando»): VUELTA COMPLETA alrededor de la jugada congelada; 360° = la pose
        g2 = [360] + G[1:]        # del juego otra vez, así el VOD sigue desde el mismo cuadro sin corte
        return [[de] + G, [de + .3] + G, [de + d * .22, 90, 34, 46, x, y], [de + d * .44, 180, 26, 40, x, y],
                [de + d * .66, 270, 34, 46, x, y], [a - .9] + g2, [a] + g2]
    if modo == "cenital":         # forma 1: sube en picada hasta la vista desde arriba (ahí entra la Grieta 3D con un fundido)
        return [[de] + G, [de + .3] + G, [de + d * .55, 0, 80, 80, x, y], [a, 0, 89, 105, x, y]]
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
    return [dict(id=id_, pts=pts, color=color, en=en, dur=.9, alto=2.8, grosor=1.2)] if len(pts) >= 2 else []   # alto: flecha en ARCO (25-nov)


def tira(pts, ancho=.009):
    """franja fina alrededor de una polilínea medida: crearZona la levanta como un muro"""
    return [(u, v - ancho) for u, v in pts] + [(u, v + ancho) for u, v in reversed(pts)]


def elipse(u, v, ru, rv, n=20):
    import math
    return [(round(u + ru * math.cos(2 * math.pi * k / n), 4), round(v + rv * math.sin(2 * math.pi * k / n), 4)) for k in range(n)]


# lotl_j1 t 17,6: los puntos del dato van por la CRESTA de la roca; +.012 = línea central de la banda (.315-.345 en x .30, recorte 31-oct)
MESAS = {
    # ================= 2.ª versión (25-nov-2026): PLAN 3D + ÓRBITAS con flechas en arco (alto) y rutas MEDIDAS (barras de vida nombradas a
    # mano en cada cuadro con rastros_vod.barras → pies = barra + (55, 100) px; RUTA lleva los puntos de otros cuadros con cam_<n>.json)
    # ---- BLG · PLAN en 10:58 (blg_j1 t 15): Liquid en el foso; ON baja (Xun detrás, fuera de cámara). TLAW azul = "A"
    "blg_plan": dict(fondo=("blg_j1", 15.0), foco=(.42, .45), cam="normal", fichas=[
        F("Josedeodo", "JarvanIV", "A", .24, .46), F("Yeon", "Ezreal", "A", .34, .45), F("CoreJJ", "Karma", "A", .40, .55),
        F("ON", "Nautilus", "R", .76, .52)],
        anillos=[dict(u=.20, v=.36, r=.05, color="amarillo", en=.6)],
        zonas=[dict(pts=elipse(.25, .38, .09, .1), color="azul", en=.8, alfa=.18)],
        flechas=[dict(id="on", pts=[(.76, .52), (.60, .48), (.42, .44)], color="rojo", en=2.2, dur=1.0, alto=3.0, grosor=1.1)],
        etiquetas=[dict(en=1.0, u=.25, v=.38, alto=0, texto="LIQUID: HACER EL DRAGÓN", sub="JOSEDEODO, YEON Y COREJJ", color="azul", dx=60, dy=190),
                   dict(en=2.4, u=.76, v=.52, alto=0, texto="BILIBILI: VIENE A DISPUTARLO", sub="ON LLEGA · XUN DETRÁS", color="rojo",
                        dx=-470, dy=150)]),
    # ---- BLG · ÓRBITA en el robo, 11:06 (blg_j1 t 23): barras nombradas (Josedeodo 404,320 · Xun 724,320 · ON 997,437); ruta de Xun medida
    #      t 19,5-22,5 (tl_pres XUN_PANT, px) llevada al cuadro con cam_blg_j1
    "blg_orb": dict(fondo=("blg_j1", 23.0), foco=(.36, .42), cam="orbita", fichas=[
        F("Josedeodo", "JarvanIV", "A", .239, .389), F("Xun", "LeeSin", "R", .406, .389), F("ON", "Nautilus", "R", .548, .497)],
        anillos=[dict(u=.29, v=.35, r=.05, color="amarillo", en=.5)],
        flechas=lambda: ruta("xun", "blg_j1", 23.0, [(19.5, .62, .37), (21.0, .552, .386), (21.75, .538, .423), (22.5, .41, .41),
                                                     (23.0, .406, .389)], "rojo", .9),
        etiquetas=[dict(en=1.2, u=.406, v=.389, alto=0, texto="XUN · LEE SIN", sub="ENTRA Y LO ROBA CON EL CASTIGO", color="rojo", dx=120, dy=-90),
                   dict(en=2.0, u=.239, v=.389, alto=0, texto="JOSEDEODO · JARVAN IV", sub="SE QUEDA SIN EL DRAGÓN", color="azul", dx=-40, dy=150)]),
    # ---- AL G1 · ÓRBITA en 28:42 (al_j1 t 26,4): TLAW = ROJO en esta partida. Barras nombradas: Josedeodo 680,422 · Hope (AIRBORNE) 824,530 ·
    #      Morgan (POLYMORPHED) 894,578 · Yeon 1025,138 · CoreJJ 1308,158 · Quid (SUPPRESSED) 1530,296 · Kael 874,256 · Shanks 1194,452 ·
    #      Tarzan 1410,442. Ruta del flanco: Morgan y Josedeodo en t 23,5 (.21, .24) llevados con cam_al_j1
    "al1_orb": dict(fondo=("al_j1", 26.4), foco=(.5, .45), cam="orbita", fichas=[
        F("Josedeodo", "LeeSin", "R", .383, .483), F("Morgan", "Camille", "R", .494, .628), F("Yeon", "Lucian", "R", .5625, .22),
        F("CoreJJ", "Nami", "R", .71, .239), F("Quid", "Galio", "R", .826, .367),
        F("Hope", "Yunara", "A", .458, .583), F("Kael", "Lulu", "A", .484, .33), F("Shanks", "Orianna", "A", .65, .511),
        F("Tarzan", "Skarner", "A", .763, .502)],
        zonas=[dict(pts=elipse(.46, .60, .075, .065), color="rojo", en=.7, alfa=.16)],
        flechas=lambda: ruta("flanco", "al_j1", 26.4, [(23.5, .21, .24), (26.4, .383, .483)], "rojo", 1.0)
        + [dict(id="patada", pts=[(.383, .483), (.42, .53), (.458, .583)], color="rojo", en=1.8, dur=.7, alto=2.0, grosor=1.0)],
        etiquetas=[dict(en=1.1, u=.383, v=.483, alto=0, texto="JOSEDEODO · LEE SIN", sub="ENTRA POR DETRÁS, CON LA PATADA", color="rojo",
                        dx=-430, dy=-80),
                   dict(en=1.9, u=.458, v=.583, alto=0, texto="HOPE, ATRAPADA", sub="LA DEFINITIVA DE MORGAN (CAMILLE)", color="azul", dx=-60,
                        dy=150)]),
    # ---- CFO · PLAN en 34:16 (cfo_j1 t 56): barras nombradas: Josedeodo 510,368 · Yeon 453,472 · Morgan 698,127 · Kino 832,454 · Rest 800,610 ·
    #      Doggo 988,554 · Shadow 812,706 · POUT 1146,250 · ancestral (barra 9 349) 702,606. Narración: «Jose waiting off the side… Kino knows he
    #      has to bodyblock, get him out of the pit». Ruta de Kino medida (t 61,5: 534,360) llevada con cam_cfo_j1 (de rastros/cfo.json)
    "cfo_plan": dict(fondo=("cfo_j1", 56.0), foco=(.42, .5), cam="normal", fichas=[
        F("Josedeodo", "LeeSin", "A", .294, .433), F("Yeon", "Jhin", "A", .265, .530), F("Morgan", "Galio", "A", .392, .210),
        F("Kino", "Alistar", "R", .462, .513), F("Rest", "Rumble", "R", .445, .657), F("Doggo", "Aphelios", "R", .543, .606),
        F("Shadow", "Qiyana", "R", .452, .746), F("POUT", "Viktor", "R", .626, .324)],
        anillos=[dict(u=.395, v=.66, r=.055, color="amarillo", en=.5)],
        flechas=lambda: [dict(id="robo", pts=[(.294, .433), (.35, .55), (.39, .64)], color="azul", en=1.6, dur=.8, alto=2.5, grosor=.9)]
        + ruta("kino", "cfo_j1", 56.0, [(56.0, .462, .513), (61.5, .307, .426)], "rojo", 2.6),
        etiquetas=[dict(en=.9, u=.395, v=.66, alto=0, texto="DRAGÓN ANCESTRAL", sub="CTBC LO EMPIEZA · 5 CONTRA 4", color="amarillo", dx=120, dy=60),
                   dict(en=1.6, u=.294, v=.433, alto=0, texto="JOSEDEODO ESPERA AL LADO", sub="PARA ROBARLO CON EL CASTIGO", color="azul",
                        dx=40, dy=-150),
                   dict(en=2.8, u=.462, v=.513, alto=0, texto="KINO · ALISTAR", sub="SU TRABAJO: SACARLO DEL FOSO", color="rojo", dx=110, dy=-60)]),
    # ---- CFO · ÓRBITA en 34:24 (cfo_j1 t 64,3; «CFO Rest has slain TLAW Josedeodo»): puntos de t 56/61,5/63,4/64,4 llevados con cam_cfo_j1
    "cfo_orb": dict(fondo=("cfo_j1", 64.3), foco=(.45, .5), cam="orbita", fichas=[
        F("Josedeodo", "LeeSin", "A", .341, .515), F("Yeon", "Jhin", "A", .339, .370), F("Rest", "Rumble", "R", .394, .522),
        F("Kino", "Alistar", "R", .529, .437), F("Doggo", "Aphelios", "R", .458, .474), F("POUT", "Viktor", "R", .524, .310),
        F("Shadow", "Qiyana", "R", .568, .757)],
        anillos=[dict(u=.625, v=.73, r=.055, color="amarillo", en=.5)],
        flechas=lambda: [dict(id="kino", pts=[(.612, .577), (.50, .52), (.382, .467)], color="rojo", en=.9, dur=.9, alto=3.0, grosor=1.1),
                         dict(id="lanzado", pts=[(.437, .519), (.39, .52), (.341, .515)], color="azul", en=1.7, dur=.6, alto=2.2, grosor=.9),
                         dict(id="rest", pts=[(.5954, .7216), (.4434, .5947), (.394, .522)], color="rojo", en=2.3, dur=.9, alto=1.6, grosor=1.0)],
        etiquetas=[dict(en=1.0, u=.382, v=.467, alto=0, texto="KINO LO LEVANTA", sub="ALISTAR · LO SACA DEL FOSO", color="rojo", dx=110, dy=-120),
                   dict(en=2.0, u=.341, v=.515, alto=0, texto="JOSEDEODO CAE · 34:24", sub="REST LO REMATA", color="azul", dx=-470, dy=60)]),
    # ---- LOS G2 · ÓRBITA en 16:32 (los2_j1 t 36,5; cae Duduhh): TLAW = ROJO. Barras: Josedeodo 823,596 · Morgan 942,529 · CoreJJ 1157,472 ·
    #      Quid 696,231 · Feisty 512,394 · Ackerman 426,686 · Zest 890,747. Ruta: Josedeodo en 16:44 (t 48,5: 1021,396), llevada con cam_los2_j1
    "los2_orb": dict(fondo=("los2_j1", 36.5), foco=(.45, .55), cam="orbita", fichas=[
        F("Josedeodo", "XinZhao", "R", .457, .644), F("Morgan", "Ornn", "R", .519, .582), F("CoreJJ", "Nami", "R", .631, .53),
        F("Quid", "Orianna", "R", .391, .306), F("Feisty", "Galio", "A", .295, .457), F("Ackerman", "Karma", "A", .25, .728),
        F("Zest", "Rumble", "A", .492, .784)],
        zonas=[dict(pts=elipse(.46, .62, .1, .08), color="rojo", en=.6, alfa=.14)],
        flechas=lambda: ruta("caza", "los2_j1", 36.5, [(36.5, .457, .644), (48.5, .56, .459)], "rojo", 1.6),
        etiquetas=[dict(en=.9, u=.457, v=.644, alto=0, texto="DUDUHH, FUERA · 16:32", sub="LA DEFINITIVA DE XIN ZHAO", color="rojo", dx=110, dy=60),
                   dict(en=2.0, u=.295, v=.457, alto=0, texto="FEISTY · GALIO", sub="EL SIGUIENTE: LO PERSIGUE", color="azul", dx=-60, dy=-120)]),
    # ---- LOS G1 (gancho) · ÓRBITA en 12:08 (los1_curse t 37,5): Curse 804,269 · Josedeodo 797,330 (1 contra 1). Josedeodo en 12:03 (t 33,5:
    #      764,384, acaba de matar a Zest) llevado con cam_los1_curse. TLAW = ROJO
    "gancho_orb": dict(fondo=("los1_curse", 37.5), foco=(.45, .38), cam="orbita", fichas=[
        F("Josedeodo", "Nocturne", "R", .444, .398), F("Curse", "Trundle", "A", .447, .342)],
        flechas=lambda: ruta("jose", "los1_curse", 37.5, [(33.5, .427, .448), (37.5, .444, .398)], "rojo", 1.0),
        etiquetas=[dict(en=1.0, u=.447, v=.342, alto=0, texto="CURSE · NIVEL 9", sub="TRUNDLE", color="azul", dx=110, dy=-100),
                   dict(en=1.6, u=.444, v=.398, alto=0, texto="JOSEDEODO · NIVEL 8", sub="NOCTURNE · SIN DESTELLO", color="rojo", dx=-460, dy=60)]),
      # PIES medidos en UN cuadro a 1280 px (previews/cuadros/r_lotl_j1_96.jpg: etiqueta + ~0,09); lo dudoso va como etiqueta
    # ---- LOS vs TLAW, partida 3, 34:4x, REPETICIÓN limpia de la transmisión (lotl_j1 t 96; TLAW azul = "A"). lol_semana2 usó t 17,6 en vivo:
    #      esta es otra toma (la repetición) y otra cámara (bullet).
    "los3": dict(fondo=("lotl_j1", 96.0), foco=(.47, .48), cam="bullet", fichas=[
        F("Josedeodo", "Sejuani", "A", .43, .66), F("Yeon", "Yunara", "A", .34, .58), F("CoreJJ", "Lulu", "A", .38, .23),
        F("Quid", "Viktor", "A", .55, .26), F("Ackerman", "RenataGlasc", "R", .44, .49), F("Feisty", "Taliyah", "R", .59, .43),
        F("Zest", "Tristana", "R", .62, .52), F("Duduhh", "Kalista", "R", .62, .58)],
        zonas=[dict(pts=tira([(.06, .265), (.2, .255), (.32, .255), (.44, .25), (.56, .235), (.66, .22)], .012), color="rojo", en=.6, alfa=.5),
               dict(pts=elipse(.40, .62, .09, .07), color="azul", en=1.2, alfa=.14)],
        etiquetas=[dict(en=1.0, u=.47, v=.24, alto=0, texto="EL MURO DE FEISTY", sub="TALIYAH · CRUZA EL RÍO", color="rojo", dx=60, dy=-90),
                   dict(en=1.6, u=.46, v=.25, alto=0, texto="COREJJ Y QUID", sub="DEL OTRO LADO", color="azul", dx=-260, dy=-40),
                   dict(en=2.2, u=.40, v=.63, alto=0, texto="JOSEDEODO Y YEON", sub="DENTRO DEL FOSO, CON 4 ENCIMA", color="azul",
                        dx=-260, dy=90)]),
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
    modo = m.get("cam", "normal")
    fin = a - (1.0 if modo != "cenital" else .2)      # todo sale antes de que la cámara vuelva al encuadre del juego
    fichas = {}
    for i, (j, f) in enumerate(m["fichas"]):
        f = dict(f)
        f["de"] = round(de + f.pop("d0") + .08 * i, 2)
        f["sale"] = round(fin, 2)
        fichas[j] = f
    E = dict(modo="mesa", de=de, a=a, fondo=WEB + f"tactica3d/mesa_{k}_fondo.png", equipos=EQ, fichas=fichas,
             camara=camara(de, a, x=m["foco"][0], y=m["foco"][1], modo=modo))
    for c in ("flechas", "anillos", "zonas", "pilares", "etiquetas"):
        if m.get(c):
            out = []
            for e in (m[c]() if callable(m[c]) else m[c]):
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
