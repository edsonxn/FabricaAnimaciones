# -*- coding: utf-8 -*-
"""Las «MESAS» de lol_final_previa (copia de videos/lol_semana2/mesas_3d.py). FORMAS NUEVAS (10-nov-2026): cam="bullet" = la cámara
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
WEB = "/videos/lol_final_previa/"
ICO = WEB + "iconos/"
G = [0, 56.07, 62.73, .5, .5]          # pose de la cámara del juego: giro, inclinación, distancia, x, y
sys.path.insert(0, _D)
from tiempos_mesas import TIEMPOS  # noqa: E402  (de, a) de cada mesa en el video

EXT = {}


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
    return [dict(id=id_, pts=pts, color=color, en=en, dur=.9, alto=1.5, grosor=1.2)] if len(pts) >= 2 else []


def tira(pts, ancho=.009):
    """franja fina alrededor de una polilínea medida: crearZona la levanta como un muro"""
    return [(u, v - ancho) for u, v in pts] + [(u, v + ancho) for u, v in reversed(pts)]


def elipse(u, v, ru, rv, n=20):
    import math
    return [(round(u + ru * math.cos(2 * math.pi * k / n), 4), round(v + rv * math.sin(2 * math.pi * k / n), 4)) for k in range(n)]


# lotl_j1 t 17,6: los puntos del dato van por la CRESTA de la roca; +.012 = línea central de la banda (.315-.345 en x .30, recorte 31-oct)
MESAS = {      # PIES medidos en investigacion/datos_jN.md (UN cuadro a 1280 px); lo que no tiene coordenada va como etiqueta
    # ---- FORMA 2 · BLG vs DK, cuartos P1, 16:19 (j2 t 69; BLG azul = "A"). Pies: datos_j2 § Pausas t=69. La ruta de Xun 65 → 69 cruza un
    #      hueco de cam_j2.json (67,8, paneo rápido que el detector pierde): no se dibuja; solo su INTENCIÓN hacia ShowMaker.
    "j2b": dict(fondo=("j2", 69.0), foco=(.51, .48), cam="bullet", fichas=[
        F("Xun", "Naafiri", "A", .51, .33), F("ShowMaker", "Akali", "R", .505, .65)],
        flechas=[dict(id="pers", pts=[(.51, .36), (.51, .50), (.505, .62)], color="azul", en=.9, dur=.9, guion=True, alto=2.5, grosor=1.4)],
        etiquetas=[dict(en=.7, u=.505, v=.65, alto=0, texto="SHOWMAKER", sub="ESCAPA CON POCA VIDA", color="rojo", dx=-190, dy=40),
                   dict(en=1.5, flecha="pers", texto="XUN · NAAFIRI", sub="LO PERSIGUE HASTA LA JUNGLA DE BLG", color="azul", dx=200, dy=-30),
                   dict(en=lambda: W("j2_3", "Tres", "j2b"), u=.51, v=.33, alto=0, texto="3 ASESINATOS DE XUN", sub="LUCID · CAREER · SHOWMAKER",
                        color="azul", dx=-230, dy=-70)]),
    # ---- FORMA 2 · BLG vs T1, semifinal P3, 32:30 (j5 t 46; BLG azul = "A"): los 10 medidos (datos_j5 § Pausas t=46) y el centro del foso
    "j5a": dict(fondo=("j5", 46.0), foco=(.43, .43), cam="bullet", fichas=[
        F("Doran", "Ambessa", "R", .365, .21), F("Keria", "Karma", "R", .30, .28), F("Peyz", "Sivir", "R", .31, .45),
        F("Oner", "JarvanIV", "R", .35, .50), F("Faker", "Ahri", "R", .13, .64), F("Knight", "Taliyah", "A", .60, .15),
        F("Viper", "Ezreal", "A", .52, .40), F("Xun", "Pantheon", "A", .49, .49), F("ON", "Nami", "A", .59, .47), F("Bin", "Gnar", "A", .57, .64)],
        anillos=[dict(u=.36, v=.47, r=.07, color="amarillo", en=.6)],
        zonas=[dict(pts=elipse(.55, .48, .07, .17), color="azul", en=lambda: W("j5_1", "Bilibili", "j5a"), alfa=.14)],
        etiquetas=[dict(en=.8, u=.33, v=.36, alto=0, texto="T1, EN EL FOSO DEL DRAGÓN", sub="SIN VISIÓN ALREDEDOR", color="rojo", dx=-210, dy=-50),
                   dict(en=lambda: W("j5_1", "Bilibili", "j5a"), u=.55, v=.48, alto=0, texto="BILIBILI LO ESPERA EN EL RÍO", color="azul",
                        dx=-40, dy=120),
                   dict(en=lambda: W("j5_1", "muro", "j5a"), u=.60, v=.15, alto=0, texto="KNIGHT · TALIYAH", sub="EL MURO", color="azul",
                        dx=190, dy=-20)]),
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
