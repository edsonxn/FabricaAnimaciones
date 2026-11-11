# -*- coding: utf-8 -*-
"""Jugada 3 en 3D (semifinal Gen.G vs IG, partida 3: la remontada de Ruler): escribe tactica3d/j3.json para nucleo/tactica3d.

Datos (lo único que vale): investigacion/pistas_j3.json (posiciones de los 10 en el minimapa por segundo de juego del HUD,
±0,04) e investigacion/datos_j3.md (cronología y marcador leídos en el cuadro). IG = azul, Gen.G = rojo.
- 30:17 IG pega al dragón de montaña (2 223 → 1 813); era el del ALMA para IG (3-1). Kiin: icono con anillo junto a su torre.
- 30:18 «Red team has stolen the Mountain Drake!»: Canyon (Wukong) se lo roba → 3-2.
- 30:22 Ruler mata a Meiko (13-7) · 30:23 IG partido en dos: Rookie y TheShy a la izquierda con Kiin encima (su TP es
  DEDUCIDO: nunca se rotula «teletransporte»), Wei y JiaQi en el dragón · 30:27 DOUBLE (JiaQi, 13-8, IG +1,8K) ·
  30:35 TRIPLE (Wei, 13-9, IG +0,7K; SHUT DOWN). Minimapa tapado 30:35-30:39: ahí los rastros se cortan.
Formas del estilo: 1 (la cámara arranca y termina en la pose del juego sobre el foso del dragón: el VOD funde con la Grieta),
8 (niebla: lo que ve IG, APROXIMADO) y 2 (bullet time: reloj congelado en 30:23 y media vuelta de cámara).

TIEMPOS: DE, A y RELOJ ([[t_video, s_juego], …]) salen de tiempos_3d.py → TIEMPOS["j3"] = dict(de=…, a=…, reloj=[…]) si existe
(lo escribe efectos.py cuando haya voz); si no, provisional: x1 desde 30:06 (1806) hasta 30:40 (1840) con 3 s congelados en
30:23. Todo lo que depende del video (hud, etiquetas, carteles, cámara, niebla) está en SEGUNDOS DE JUEGO → tv(g) / tc(g, f).
Si el reloj de tiempos_3d.py no congela 30:23, la media vuelta se hace igual en el tiempo que dure ese segundo.
uso: python videos/lol_final_previa/j3_3d.py  →  python nucleo/tactica3d/render3d.py videos/lol_final_previa/tactica3d/j3.json …
"""
import importlib.util
import json
import os

_D = os.path.dirname(os.path.abspath(__file__))
WEB = "/videos/lol_final_previa/"
ICO = WEB + "iconos/"
PISTAS = os.path.join(_D, "investigacion", "pistas_j3.json")

CONGELA = 1823.0          # 30:23: IG partido en dos (bullet time)


def _tiempos():
    ruta = os.path.join(_D, "tiempos_3d.py")
    if os.path.exists(ruta):
        spec = importlib.util.spec_from_file_location("tiempos_3d", ruta)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        t = getattr(m, "TIEMPOS", {}).get("j3")
        if t:
            return float(t["de"]), float(t["a"]), [tuple(map(float, r)) for r in t["reloj"]], True
    # provisional: x1 desde 30:06; 3 s congelados en 30:23; x1 hasta 30:40
    rel = [(0.0, 1806.0), (17.0, CONGELA), (20.0, CONGELA), (37.0, 1840.0)]
    return rel[0][0], rel[-1][0], rel, False


DE, A, RELOJ, DE_ARCHIVO = _tiempos()


def tv(g):
    """segundo de juego → primer instante del video en que el reloj lo marca"""
    for (t0, g0), (t1, g1) in zip(RELOJ, RELOJ[1:]):
        if g0 <= g <= g1 and g1 > g0:
            return round(t0 + (t1 - t0) * (g - g0) / (g1 - g0), 3)
    return RELOJ[-1][0] if g > RELOJ[-1][1] else RELOJ[0][0]


def congelado(g):
    """(t0, t1) del tramo en que el reloj se queda en g (pausa); si no hay pausa, el tramo que dura ese segundo"""
    for (t0, g0), (t1, g1) in zip(RELOJ, RELOJ[1:]):
        if g0 == g1 == g and t1 > t0:
            return t0, t1
    return tv(g - .5), tv(g + .5)


def tc(g, f):
    """instante del video a la fracción f (0..1) del tramo congelado en g"""
    t0, t1 = congelado(g)
    return round(t0 + (t1 - t0) * f, 3)


# ------------------------------------------------------------------ pistas (medidas; nada inventado)
P = json.load(open(PISTAS, encoding="utf-8"))
JUG = {k: v for k, v in P.items() if not k.startswith("_")}
MUERTES = {m["muere"]: m for m in P["_muertes"]}
FOSO = tuple(P["_objetivos"]["foso_dragon"])          # (.66, .65)
DRAG = P["_objetivos"]["dragon_montana"]
EQ = {"azul": "IG", "rojo": "GEN"}
KIIN_TORRE = (.86, .21)                                 # icono con anillo junto a su torre interior (30:17)
IZQ, DER = (.43, .55), (.735, .65)                      # las dos mitades de IG a las 30:23 (medidas en pistas)


def fichas():
    out = {}
    for jug, d in JUG.items():
        pts = [list(p) for p in d["puntos"]]
        f = dict(jugador=jug, campeon=d["campeon"], equipo=EQ[d["equipo"]], icono=ICO + d["campeon"] + ".png", puntos=pts)
        g0 = pts[0][0]
        if g0 > RELOJ[0][1] + 1:            # sin dato antes: la ficha se levanta donde se la mide por primera vez
            f["de"] = tv(g0 - .5)
        if jug in MUERTES:                  # muere: la ficha se hunde en el segundo del rótulo
            f["sale"] = tv(MUERTES[jug]["hud"])
        out[jug] = f
    # Rookie: primer dato a las 30:23,3 en (.404, .522); se levanta 2,8 s antes en ese punto para que Kiin aparezca
    # «por la espalda» de alguien que ya está ahí (dentro de la precisión ±0,04 del minimapa).
    out["Rookie"]["de"] = tv(1820.5)
    # Kiin: dos fichas (la del TP deducido no se dibuja como TP): en su torre (30:17) se hunde; aparece en la pelea (30:23)
    k = out.pop("Kiin")
    torre = [p for p in k["puntos"] if p[0] < 1823]
    pelea = [p[:3] for p in k["puntos"] if p[0] >= 1823]
    out["Kiin_torre"] = dict(k, puntos=torre, de=tv(torre[0][0] - .5), sale=tv(1820.8))
    out["Kiin"] = dict(k, puntos=pelea, de=tv(1822.3))
    return out


def estructuras():
    return [
        dict(tipo="inhibidor", u=.075, v=.775, equipo="IG"), dict(tipo="inhibidor", u=.21, v=.795, equipo="IG"),
        dict(tipo="inhibidor", u=.235, v=.925, equipo="IG"), dict(tipo="nexo", u=.115, v=.885, equipo="IG"),
        dict(tipo="inhibidor", u=.765, v=.07, equipo="GEN"), dict(tipo="inhibidor", u=.79, v=.205, equipo="GEN"),
        dict(tipo="inhibidor", u=.925, v=.225, equipo="GEN"), dict(tipo="nexo", u=.885, v=.115, equipo="GEN"),
    ]


def hud():
    """columna del marcador (datos_j3.md § Marcador y § Paso a paso). Uno de cada tipo a la vez: el siguiente entra cuando
    el anterior se va (±0,15 s), así las píldoras no saltan de sitio."""
    fin = A + 1
    def serie(cortes, color_sub):
        out = []
        for i, (g, texto, sub, color) in enumerate(cortes):
            de = tv(g) + (.15 if i else 0)
            a = tv(cortes[i + 1][0]) - .15 if i + 1 < len(cortes) else fin
            out.append(dict(de=de, a=a, texto=texto, sub=sub, color=color, tam=32))
        return out
    g0 = RELOJ[0][1] + 1.6
    asesinatos = serie([(g0, "13 - 6 EN ASESINATOS", "IG VA ARRIBA", "azul"),
                        (1822, "13 - 7 EN ASESINATOS", "CAE MEIKO", "rojo"),
                        (1827, "13 - 8 EN ASESINATOS", "CAE JIAQI", "rojo"),
                        (1835, "13 - 9 EN ASESINATOS", "CAE WEI", "rojo")], None)
    oro = serie([(g0 + .8, "IG +2,9K DE ORO", "VENTAJA DE IG", "azul"),
                 (1822, "IG +2,5K DE ORO", "SE ACHICA", "azul"),
                 (1827, "IG +1,8K DE ORO", "SE ACHICA", "azul"),
                 (1835, "IG +0,7K DE ORO", "CASI EMPATE", "amarillo")], None)
    dragones = serie([(g0 + 1.6, "3 - 1 EN DRAGONES", "UNO MÁS Y IG TIENE EL ALMA", "azul"),
                      (DRAG["robado_por_GEN"], "3 - 2 EN DRAGONES", "GEN.G LE QUITA EL ALMA", "rojo")], None)
    return asesinatos + oro + dragones


def muerte(jug, rotulo, sub, dx, dy, hasta=None):
    m = MUERTES[jug]
    u, v = m["donde"]
    t = tv(m["hud"])
    return dict(de=t - .1, a=min(t + 2.0, hasta) if hasta else t + 2.0, u=u, v=v, alto=2.5, texto=rotulo, sub=sub, color="rojo",
                dx=dx, dy=dy, icono=ICO + JUG[jug]["campeon"] + ".png")


def escena():
    jg = [j for j in JUG]
    t_c0, t_c1 = congelado(CONGELA)
    # solo números leídos: el último (1 813) se mantiene hasta el robo (el golpe de Canyon lo deja en 0)
    drag_vida = []
    for g, hp in DRAG["vida"]:          # escalones: el número cambia de golpe, sin cifras intermedias que nadie leyó
        if drag_vida:
            drag_vida.append([tv(g) - .05, drag_vida[-1][1]])
        drag_vida.append([tv(g), hp])
    drag_vida += [[tv(DRAG["robado_por_GEN"]) - .08, DRAG["vida"][-1][1]], [tv(DRAG["robado_por_GEN"]), 0]]
    # cámara: [t, u, v, distancia, inclinación°, giro°, fov]. JUEGO = la pose de la cámara del juego sobre el foso del dragón
    # (56° como camG de grieta3d.js, de cerca) → forma 1 al principio y al final.
    JUEGO = [FOSO[0], FOSO[1], 30, 56, 0, 40]
    cam = [
        [DE] + JUEGO,
        [tv(1807.2), .63, .60, 52, 66, 0, 40],
        [tv(1809.0), .56, .52, 118, 80, 0, 38],          # vista alta (picada)
        [tv(1812.0), .57, .52, 118, 78, 0, 38],
        [tv(1815.0), .66, .47, 96, 62, -4, 37],          # el foso y la torre de Kiin a la vez
        [tv(1818.0), .68, .44, 96, 60, -12, 37],
        [tv(1820.4), .62, .56, 84, 62, -48, 37],         # niebla: lo que ve IG
        [t_c0, .59, .58, 78, 46, -90, 37],               # bullet time: media vuelta alrededor de la pelea
        [(t_c0 + t_c1) / 2, .59, .58, 74, 40, 0, 37],
        [t_c1, .59, .58, 78, 46, 90, 37],
        [tv(1825.0), .66, .61, 66, 54, 40, 37],
        [tv(1827.5), .68, .62, 58, 54, 18, 37],          # DOUBLE (JiaQi)
        [tv(1830.5), .62, .63, 58, 55, 8, 37],
        [tv(1833.5), .56, .63, 56, 55, 2, 37],           # Wei entra solo
        [tv(1835.6), .57, .61, 66, 58, 0, 37],           # TRIPLE (Wei)
        [tv(1837.6), .60, .60, 62, 57, 0, 38],
        [A] + JUEGO,                                     # vuelve a la pose del juego: el VOD sigue detrás
    ]
    # reloj anclado a la voz (tiempos_3d.py): las claves que caen fuera del reloj se apilan en DE o en A; se quitan para que la
    # subida desde la pose del juego (forma 1) y la vuelta a ella duren al menos ~1 s (fx_jugadas.py, 11-nov-2026)
    cam = [cam[0]] + [c for c in cam[1:-1] if DE + 1.2 < c[0] < A - .8] + [cam[-1]]
    cam = [c for i, c in enumerate(cam) if i == 0 or c[0] > cam[i - 1][0] + .05]
    return dict(
        de=DE, a=A, titulo="LA JUGADA EN 3D · DATOS DEL MINIMAPA", reloj=[list(r) for r in RELOJ], fundido=0,   # sin negro: el VOD funde encima (forma 1)
       
        equipos=[dict(id="IG", color="azul", logo=ICO + "equipos/IG.png"), dict(id="GEN", color="rojo", logo=ICO + "equipos/GEN.png")],
        fichas=fichas(),
        estructuras=estructuras(),
        objetivos=[
            dict(nombre="dragón de montaña", u=FOSO[0], v=FOSO[1], img=WEB + "tactica3d/j3_montana.png", color="#c99a5a", r=.035, muere=tv(DRAG["robado_por_GEN"]),
                 gana="rojo", vida=drag_vida, numeros_desde=drag_vida[0][0]),
        ],
        anillos=[
            dict(u=KIIN_TORRE[0], v=KIIN_TORRE[1], r=.03, color="amarillo", en=tv(1817.2), sale=tv(1820.8)),
            dict(u=FOSO[0], v=FOSO[1], r=.05, color="rojo", en=tv(1817.8), sale=tv(1820.2)),
            dict(u=IZQ[0], v=IZQ[1], r=.065, color="azul", en=t_c0 + .2, sale=t_c1 + .6),
            dict(u=DER[0], v=DER[1], r=.06, color="azul", en=t_c0 + .4, sale=t_c1 + .6),
        ],
        focos=[dict(quien="Canyon", de=tv(1817.4), a=tv(1820.4)), dict(quien="Kiin", de=tv(1822.4), a=t_c1),
               dict(quien="Ruler", de=tv(1821.4), a=tv(1822.3)), dict(quien="Ruler", de=t_c1 + .2, a=tv(1838.2))],
        rastros=[dict(quien=j, de=tv(1810.0), a=tv(MUERTES[j]["hud"]) if j in MUERTES else tv(1835.0), ventana=8)
                 for j in jg if j != "Kiin"] +
                [dict(quien="Kiin", de=tv(1823.4), a=tv(1835.0), ventana=8)],
        niebla=[dict(de=tv(1820.2), a=t_c0 - .05, ve="IG", oculta="GEN", radio=.075, fuerza=1.0, dur=.8)],
        hud=hud(),
        etiquetas=[
            dict(de=tv(1807.4), a=tv(1812.2), quien="JiaQi", texto="INVICTUS GAMING", color="azul", dx=110, dy=60, tam=28),
            dict(de=tv(1807.6), a=tv(1812.2), quien="Ruler", texto="GEN.G", color="rojo", dx=-110, dy=-50, tam=28),
            dict(de=tv(1812.6), a=tv(1817.6), u=FOSO[0], v=FOSO[1], alto=7, texto="DRAGÓN DE MONTAÑA",
                 sub="EL DEL ALMA PARA IG", color="amarillo", dx=170, dy=40),
            dict(de=tv(1817.4), a=tv(1820.6), quien="Kiin_torre", texto="KIIN, EN SU TORRE", sub="AL OTRO LADO DEL MAPA",
                 color="rojo", dx=150, dy=60, icono=ICO + "Camille.png"),
            dict(de=tv(1818.0), a=tv(1820.3), quien="Canyon", texto="CANYON ROBA EL DRAGÓN DEL ALMA", sub="3 - 2 EN DRAGONES",
                 color="rojo", dx=-160, dy=-40, icono=ICO + "MonkeyKing.png"),
            muerte("Meiko", "CAE MEIKO", "LA MATA RULER", 150, -60, hasta=t_c0 + .2),
            dict(de=tv(1822.4), a=tc(CONGELA, .3), quien="Kiin", texto="KIIN APARECE POR LA ESPALDA", sub="SOBRE ROOKIE Y THESHY",
                 color="rojo", dx=120, dy=-60, icono=ICO + "Camille.png"),
            dict(de=t_c0 + .3, a=t_c1 + .6, u=.58, v=.57, alto=3, texto="IG PARTIDO EN DOS",
                 sub="2 LEJOS · 2 EN EL DRAGÓN", color="azul", dx=0, dy=120, tam=34),
            muerte("JiaQi", "DOUBLE KILL", "RULER MATA A JIAQI", 150, -40),
            dict(de=tv(1828.8), a=tv(1831.8), quien="Wei", texto="WEI ENTRA SOLO", color="azul", dx=140, dy=-50),
            dict(de=tv(1831.0), a=tv(1834.0), quien="Rookie", texto="ROOKIE Y THESHY LLEGAN TARDE", color="azul",
                 dx=150, dy=60),
            muerte("Wei", "TRIPLE KILL", "RULER MATA A WEI · SHUT DOWN", -150, -40),
            dict(de=tv(1835.4), a=tv(1837.9), quien="Ruler", texto="RULER · YUNARA", sub="3 ASESINATOS EN 13 SEGUNDOS",
                 color="rojo", dx=150, dy=70, icono=ICO + "Yunara.png"),
        ],
        carteles=[
            dict(de=tv(1820.3), a=t_c0 - .1, texto="LA VISIÓN DE IG · APROXIMADA", sub="CALCULADA CON LAS POSICIONES",
                 color="azul", tam=46, y=170),
            dict(de=t_c0 + .1, a=t_c1 - .1, texto="30:23 · PAUSA", color="amarillo", tam=46, y=170),
        ],
        destellos=[tv(DRAG["robado_por_GEN"])],
        camara=cam,
    )


if __name__ == "__main__":
    os.makedirs(os.path.join(_D, "tactica3d"), exist_ok=True)
    ruta = os.path.join(_D, "tactica3d", "j3.json")
    E = escena()
    json.dump(E, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(ruta, "· tiempos:", "tiempos_3d.py" if DE_ARCHIVO else "PROVISIONALES (x1 desde 30:06)", f"· {DE}–{A}")
    print("SFX/eventos (t_video):", {"robo": tv(DRAG["robado_por_GEN"]), **{m: tv(MUERTES[m]["hud"]) for m in MUERTES
                                                                          if MUERTES[m]["hud"] <= RELOJ[-1][1]},
                                     "pausa": congelado(CONGELA)})
