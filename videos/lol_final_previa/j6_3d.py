# -*- coding: utf-8 -*-
"""Jugada 6 en 3D (semifinal BLG vs T1, partida 4: la pelea que elimina a T1): escribe tactica3d/j6.json para nucleo/tactica3d.

Datos (lo único que vale): investigacion/pistas_j6.json (posiciones de los 10 en el minimapa por segundo de juego del HUD,
±0,03-0,04 en la pelea) e investigacion/datos_j6.md (cronología y marcador leídos en el cuadro). T1 = azul, BLG = rojo.
- 29:20 T1 mata al Barón (POWERPLAY 3:00) → a las 32:16 le quedan 0:03 y a las 32:17 0:02 (datos_j6.md; el brief decía 0:02
  a las 32:14: gana datos_j6.md). La cuenta atrás del HUD sale de esas lecturas: acaba en 32:19.
- 32:16 marcador 8-12, oro 60,9K / 61,3K (BLG +0,4K), torres 4-4 · 32:14 «Red turret destroyed!» (exterior central de BLG,
  (.61, .42); T1 3→4 torres a las 32:17) · Oner encima de Viper (32:13-32:15) · 32:16 Viper «RESURRECTING» (Ángel de la Guarda,
  no es muerte) · 32:17 entran Bin por arriba y Xun por abajo; Faker se va al norte detrás de Knight y ON · 32:18 Knight mata a
  Oner (8-13 a las 32:19; fuera de cámara: su último punto medido es 32:17) · 32:23 Bin mata a Doran · 32:27 DOBLE de Knight:
  cae Faker (8-15, BLG +2,5K). BLG no pierde a nadie. (El feed oro_125.json va ≈5 s detrás del HUD; en pantalla, el HUD.)
Formas del estilo: 1 (la cámara arranca y termina en la pose del juego sobre la torre central roja: el VOD funde con la Grieta),
8 (niebla: lo que ve T1 mientras Bin y Xun llegan por los flancos, APROXIMADO) y 6 (LO QUE PODÍA HACER: ruta fantasma
discontinua de T1 reagrupando bajo su torre central, rotulada POSIBILIDAD, frente a las rutas reales de Oner y de Faker).

TIEMPOS: DE, A y RELOJ ([[t_video, s_juego], …]) salen de tiempos_3d.py → TIEMPOS["j6"] = dict(de=…, a=…, reloj=[…]) si existe
(lo escribe efectos.py cuando haya voz); si no, provisional: x1 desde 32:06 (1926) hasta 32:20 (1940). Todo lo que depende del
video (hud, etiquetas, carteles, cámara, niebla, flechas) está en SEGUNDOS DE JUEGO → tv(g). Lo que cae fuera del reloj
(Doran 32:23, Faker 32:27, +2,5K) solo entra si el reloj de tiempos_3d.py llega hasta ahí.
uso: python videos/lol_final_previa/j6_3d.py  →  python nucleo/tactica3d/render3d.py videos/lol_final_previa/tactica3d/j6.json …
"""
import importlib.util
import json
import os

_D = os.path.dirname(os.path.abspath(__file__))
WEB = "/videos/lol_final_previa/"
ICO = WEB + "iconos/"
PISTAS = os.path.join(_D, "investigacion", "pistas_j6.json")
ICONO = {"Wukong": "MonkeyKing"}         # nombre del campeón → archivo de iconos/


def _tiempos():
    ruta = os.path.join(_D, "tiempos_3d.py")
    if os.path.exists(ruta):
        spec = importlib.util.spec_from_file_location("tiempos_3d", ruta)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        t = getattr(m, "TIEMPOS", {}).get("j6")
        if t:
            return float(t["de"]), float(t["a"]), [tuple(map(float, r)) for r in t["reloj"]], True
    rel = [(0.0, 1926.0), (14.0, 1940.0)]          # provisional: x1 de 32:06 a 32:20
    return rel[0][0], rel[-1][0], rel, False


DE, A, RELOJ, DE_ARCHIVO = _tiempos()
G0, G1 = RELOJ[0][1], RELOJ[-1][1]                 # segundos de juego que cubre el clip


def tv(g):
    """segundo de juego → primer instante del video en que el reloj lo marca"""
    for (t0, g0), (t1, g1) in zip(RELOJ, RELOJ[1:]):
        if g0 <= g <= g1 and g1 > g0:
            return round(t0 + (t1 - t0) * (g - g0) / (g1 - g0), 3)
    return RELOJ[-1][0] if g > RELOJ[-1][1] else RELOJ[0][0]


def dentro(g):
    return G0 - .01 <= g <= G1 + .01


# ------------------------------------------------------------------ pistas (medidas; nada inventado)
P = json.load(open(PISTAS, encoding="utf-8"))
JUG = {k: v for k, v in P.items() if not k.startswith("_")}
MUERTES = {m["jugador"]: m for m in P["_muertes"] if m.get("por")}      # Viper (Ángel de la Guarda) no es muerte
ANGEL = next(m for m in P["_muertes"] if m["jugador"] == "Viper")
EQ = {"azul": "T1", "rojo": "BLG"}
T1, BLG = [j for j, d in JUG.items() if d["equipo"] == "azul"], [j for j, d in JUG.items() if d["equipo"] == "rojo"]
TORRE = tuple(P["_torres"][0]["lugar"])            # (.61, .42) exterior central de BLG, cae 32:14
TORRE_T1 = tuple(P["_torres"][1]["lugar"])         # (.35, .65) exterior central de T1, cae 32:42
G_TORRE, G_TORRE_T1 = 1934.0, 1962.0
G_ANGEL = 1936.0                                   # RESURRECTING 32:16 (32:16-32:17)
G_ENTRAN = 1937.0                                  # 32:17: Bin por arriba, Xun por abajo; Faker al norte
G_BARON_FIN = 1939.0                               # 0:03 a las 32:16 y 0:02 a las 32:17 → 0:00 a las 32:19


def ico(campeon):
    return ICO + ICONO.get(campeon, campeon) + ".png"


def donde(jug, g):
    """posición medida más cercana en el tiempo (sin interpolar más allá de los puntos)"""
    pts = JUG[jug]["puntos"]
    return tuple(min(pts, key=lambda p: abs(p[0] - g))[1:3])


def fichas():
    out = {}
    for jug, d in JUG.items():
        pts, ant = [], None
        for p in d["puntos"]:
            q = list(p)
            if ant and (abs(q[1] - ant[1]) + abs(q[2] - ant[2])) > .45:   # regreso a base (anillo de regreso en las notas)
                q.append("salto")
            pts.append(q)
            ant = q
        f = dict(jugador=jug, campeon=d["campeon"], equipo=EQ[d["equipo"]], icono=ico(d["campeon"]), puntos=pts)
        if pts[0][0] > G0 + 1:              # sin dato antes: la ficha se levanta donde se la mide por primera vez
            f["de"] = tv(pts[0][0] - .5)
        if jug in MUERTES and dentro(MUERTES[jug]["s"]):       # muere: la ficha se hunde en el segundo del rótulo
            f["sale"] = tv(MUERTES[jug]["s"])
        out[jug] = f
    return out


def estructuras():
    return [
        dict(tipo="torre", u=TORRE[0], v=TORRE[1], equipo="BLG", **({"cae": tv(G_TORRE)} if dentro(G_TORRE) else {})),
        dict(tipo="torre", u=TORRE_T1[0], v=TORRE_T1[1], equipo="T1",
             **({"cae": tv(G_TORRE_T1)} if dentro(G_TORRE_T1) else {})),
        dict(tipo="inhibidor", u=.075, v=.775, equipo="T1"), dict(tipo="inhibidor", u=.21, v=.795, equipo="T1"),
        dict(tipo="inhibidor", u=.235, v=.925, equipo="T1"), dict(tipo="nexo", u=.115, v=.885, equipo="T1"),
        dict(tipo="inhibidor", u=.765, v=.07, equipo="BLG"), dict(tipo="inhibidor", u=.79, v=.205, equipo="BLG"),
        dict(tipo="inhibidor", u=.925, v=.225, equipo="BLG"), dict(tipo="nexo", u=.885, v=.115, equipo="BLG"),
    ]


def hud():
    """columna del marcador (datos_j6.md § Marcador). Uno de cada tipo a la vez: el siguiente entra cuando el anterior se va
    (±0,15 s), así las píldoras no saltan de sitio. Solo los cortes que caen dentro del reloj."""
    fin = A + 1

    def serie(cortes):
        cortes = [c for c in cortes if c[0] <= G1 + .01]
        out = []
        for i, (g, texto, sub, color) in enumerate(cortes):
            de = max(DE, tv(g)) + (.15 if i else 0)
            a = tv(cortes[i + 1][0]) - .15 if i + 1 < len(cortes) else fin
            out.append(dict(de=de, a=a, texto=texto, sub=sub, color=color, tam=32))
        return out
    g0 = G0 + .6
    asesinatos = serie([(g0, "8 - 12 EN ASESINATOS", "BLG VA ARRIBA", "rojo"),
                        (1938.0, "8 - 13 EN ASESINATOS", "CAE ONER", "rojo"),
                        (1943.0, "8 - 14 EN ASESINATOS", "CAE DORAN", "rojo"),
                        (1947.0, "8 - 15 EN ASESINATOS", "CAE FAKER", "rojo")])
    oro = serie([(g0 + .6, "BLG +0,4K DE ORO", "T1, A MENOS DE 500", "amarillo"),
                 (1947.0, "BLG +2,5K DE ORO", "LA VENTAJA VUELVE", "rojo")])
    torres = serie([(g0 + 1.2, "3 - 4 EN TORRES", "T1 EMPUJA EL CENTRO", "azul"),
                    (G_TORRE, "4 - 4 EN TORRES", "CAE LA EXTERIOR CENTRAL DE BLG", "azul")])
    # Barón: cuenta atrás que cuadra con las dos lecturas del HUD (0:03 a las 32:16, 0:02 a las 32:17)
    baron = []
    g = float(int(G0 + 1.8) + 1)
    while g < G_BARON_FIN and g <= G1:
        baron.append((g, f"BARÓN DE T1 · QUEDAN 0:{int(G_BARON_FIN - g):02d}", "SE LE ACABA A T1", "morado"))
        g += 1
    baron.append((G_BARON_FIN, "BARÓN DE T1 · 0:00", "SE ACABÓ EL BARÓN", "morado"))
    return asesinatos + oro + torres + serie(baron)


def muerte(jug, rotulo, sub, dx, dy):
    m = MUERTES[jug]
    u, v = m.get("lugar") or m.get("lugar_aprox") or donde(jug, m["s"])
    t = tv(m["s"])
    return dict(de=t - .1, a=t + 2.0, u=u, v=v, alto=2.5, texto=rotulo, sub=sub, color="rojo", dx=dx, dy=dy,
                icono=ico(JUG[jug]["campeon"]))


def escena():
    # cámara: [t, u, v, distancia, inclinación°, giro°, fov]. JUEGO = la pose de la cámara del juego sobre la torre central
    # roja (56° como camG de grieta3d.js, de cerca) → forma 1 al principio y al final.
    JUEGO = [.61, .42, 30, 56, 0, 40]
    FIN = [.62, .375, 30, 56, 0, 40]
    cam = [
        [DE] + JUEGO,
        [tv(1927.2), .62, .43, 50, 64, 0, 40],
        [tv(1928.8), .66, .43, 104, 80, 0, 38],          # vista alta (picada): la pelea y los dos flancos
        [tv(1930.4), .67, .42, 100, 77, 0, 38],          # niebla: Bin llega por arriba, Xun por abajo
        [tv(1933.2), .64, .43, 92, 72, -4, 38],
        [tv(1934.8), .53, .49, 84, 64, -8, 38],          # LO QUE PODÍA HACER: la torre central de T1 entra en cuadro
        [tv(1936.6), .56, .46, 82, 64, -4, 38],
        [tv(1938.2), .62, .38, 62, 60, 0, 39],           # Faker, solo al norte
        [A] + FIN,                                       # vuelve a la pose del juego: el VOD sigue detrás
    ]
    if cam[-1][0] < A - .05:
        cam.append([A] + FIN)
    # reloj anclado a la voz (tiempos_3d.py): las claves que caen fuera del reloj se apilan en DE o en A; se quitan para que la
    # subida desde la pose del juego (forma 1) y la vuelta a ella duren al menos ~1 s (fx_jugadas.py, 11-nov-2026)
    cam = [cam[0]] + [c for c in cam[1:-1] if DE + 1.2 < c[0] < A - .8] + [cam[-1]]
    cam = [c for i, c in enumerate(cam) if i == 0 or c[0] > cam[i - 1][0] + .05]

    podia = [(.565, .455), (.49, .51), (.42, .565), (.37, .62)]          # T1 reagrupando bajo su torre central (POSIBILIDAD)
    oner = [tuple(p[1:3]) for p in JUG["Oner"]["puntos"] if 1930 <= p[0] <= 1934]      # medidos: 32:10 → 32:14
    faker = [tuple(p[1:3]) for p in JUG["Faker"]["puntos"] if 1934 <= p[0] <= 1939]    # medidos: 32:14 → 32:19

    etiquetas = [
        dict(de=tv(1926.4), a=tv(1929.4), quien="Peyz", texto="T1", color="azul", dx=-120, dy=70, tam=30),
        dict(de=tv(1926.6), a=tv(1929.4), quien="ON", texto="BILIBILI GAMING", color="rojo", dx=120, dy=-60, tam=28),
        dict(de=tv(1927.0), a=tv(1930.2), u=TORRE[0], v=TORRE[1], alto=4, texto="TORRE EXTERIOR CENTRAL",
             sub="DE BLG", color="rojo", dx=150, dy=60),
        dict(de=tv(1931.0), a=tv(1933.3), quien="Bin", texto="BIN, POR ARRIBA", color="rojo", dx=150, dy=40,
             icono=ico("Renekton"), tam=26),
        dict(de=tv(1931.2), a=tv(1933.3), quien="Xun", texto="XUN, POR ABAJO", color="rojo", dx=120, dy=60,
             icono=ico("Skarner"), tam=26),
        dict(de=tv(1933.35), a=tv(1935.0), flecha="oner", texto="ONER SE LANZA SOBRE VIPER", sub="LO QUE PASÓ",
             color="azul", dx=150, dy=-70, icono=ico("Wukong")),
        dict(de=tv(G_TORRE) - .05, a=tv(G_TORRE + 1.8), u=TORRE[0], v=TORRE[1], alto=4, texto="¡CAE LA TORRE!",
             color="rojo", dx=150, dy=40),
        dict(de=tv(1935.0), a=tv(1937.6), flecha="podia", texto="REAGRUPAR BAJO SU TORRE", sub="POSIBILIDAD",
             color="blanco", dx=70, dy=50),
        dict(de=tv(G_ANGEL), a=tv(1937.6), u=ANGEL_UV[0], v=ANGEL_UV[1], alto=3, texto="VIPER SE SALVA",
             sub="ÁNGEL DE LA GUARDA", color="rojo", dx=160, dy=70, icono=ico("Ashe"), tam=26),
        dict(de=tv(1936.8), a=A + 1, flecha="faker", texto="FAKER, SOLO AL NORTE", sub="DETRÁS DE KNIGHT Y ON",
             color="azul", dx=170, dy=30, icono=ico("Akali")),
    ]
    if dentro(MUERTES["Oner"]["s"]):
        etiquetas.append(muerte("Oner", "CAE ONER", "LO MATA KNIGHT", 150, 60))
    if dentro(MUERTES["Doran"]["s"]):
        etiquetas.append(muerte("Doran", "CAE DORAN", "LO MATA BIN", 150, 60))
    if dentro(MUERTES["Faker"]["s"]):
        etiquetas.append(muerte("Faker", "CAE FAKER", "DOBLE DE KNIGHT", -150, -40))

    return dict(
        de=DE, a=A, titulo="LA JUGADA EN 3D · DATOS DEL MINIMAPA", reloj=[list(r) for r in RELOJ], fundido=0,   # sin negro: el VOD funde encima (forma 1)
        equipos=[dict(id="T1", color="azul", logo=ICO + "equipos/T1.png"), dict(id="BLG", color="rojo", logo=ICO + "equipos/BLG.png")],
        fichas=fichas(),
        estructuras=estructuras(),
        anillos=[
            dict(u=TORRE[0], v=TORRE[1], r=.03, color="rojo", en=tv(1927.2), sale=tv(G_TORRE)),
            dict(u=TORRE_T1[0], v=TORRE_T1[1], r=.035, color="blanco", en=tv(1935.6), sale=tv(1937.8)),
            dict(u=ANGEL_UV[0], v=ANGEL_UV[1], r=.022, color="amarillo", en=tv(G_ANGEL), sale=tv(1937.6)),
        ],
        flechas=[
            dict(id="oner", pts=oner, color="azul", en=tv(1932.4), dur=1.0, sale=tv(1935.2), alto=1.6),
            dict(id="podia", pts=podia, color="blanco", en=tv(1934.9), dur=1.2, sale=tv(1937.8), guion=True, alto=2.6,
                 grosor=.85),
            dict(id="faker", pts=faker, color="azul", en=tv(1936.6), dur=1.2, sale=A + 1, alto=1.8),
        ],
        focos=[dict(quien="Oner", de=tv(1932.2), a=tv(1935.6)), dict(quien="Faker", de=tv(1936.4), a=A + 1)],
        rastros=[dict(quien=j, de=tv(1927.0), a=tv(MUERTES[j]["s"]) if j in MUERTES and dentro(MUERTES[j]["s"]) else A + 1,
                      ventana=8) for j in JUG],
        niebla=[dict(de=tv(1930.3), a=tv(1933.3), ve="T1", oculta="BLG", radio=.075, fuerza=1.0, dur=.7)],
        hud=hud(),
        etiquetas=etiquetas,
        carteles=[
            dict(de=tv(1930.5), a=tv(1933.3), texto="LA VISIÓN DE T1 · APROXIMADA", sub="CALCULADA CON LAS POSICIONES",
                 color="azul", tam=46, y=170),
            dict(de=tv(1935.0), a=tv(1937.7), texto="LO QUE PODÍA HACER", sub="POSIBILIDAD, NO LO QUE PASÓ",
                 color="blanco", tam=46, y=170),
        ],
        destellos=[],
        camara=cam,
    )


ANGEL_UV = (.62, .42)     # RESURRECTING 32:16-32:17 (notas de Viper en pistas_j6.json)

if __name__ == "__main__":
    os.makedirs(os.path.join(_D, "tactica3d"), exist_ok=True)
    ruta = os.path.join(_D, "tactica3d", "j6.json")
    E = escena()
    json.dump(E, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(ruta, "· tiempos:", "tiempos_3d.py" if DE_ARCHIVO else "PROVISIONALES (x1 de 32:06 a 32:20)", f"· {DE}–{A}")
    print("SFX/eventos (t_video):", {"torre": tv(G_TORRE), "angel": tv(G_ANGEL),
                                     **{m: tv(MUERTES[m]["s"]) for m in MUERTES if dentro(MUERTES[m]["s"])}})
