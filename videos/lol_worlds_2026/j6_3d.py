# -*- coding: utf-8 -*-
"""Jugada 6 en 3D (el Barón de Liquid, TLAW vs AL partida 2): escribe tactica3d/j6.json para nucleo/tactica3d.

VERIFICADO el 27-oct-2026 en el VOD (jugada.mp4 = wjoQ0ze5bJ4 desde 2833 s; reloj = s + 39:40), con la narración oficial
transcrita (Whisper, scratchpad) y el minimapa de la transmisión medido cada 2-6 s (rejilla de décimas):
- 40:16: 11-17 en asesinatos, 74,8K-71,8K (+3,0K), 6-2 en torres. Los 10 en el dragón Infernal.
- «it's Yeon that takes the drake… three for three»; «it would be soul for AL» (AL tenía 3) → 3-3 en dragones.
- «a wave pushing in the top side, taking the inhibitor tower» (torres 7-2 a las 40:32); «Morgan's gonna TP top to try and take
  the inhib» → a las 40:38 Morgan pega al inhibidor y Tarzan llega a defender («the Paranoia going down»).
- 40:39 «They're positioning on a flank, they want to cut off TL»; 40:46 «Team Liquid back away wisely».
- 40:59 «the inhib in the top side still remains for AL… you can see how dark the map is for the LPL number one».
- 41:35 Liquid empieza el Barón; 41:38 15 619 PV; 41:41 11 166; 41:44,8 Hope (al este del foso) dispara el cohete de Jinx
  (3 634 → 2 521 a las 41:45,7); 41:46 «Josedeodo will land the smite»; 41:46,4 «Blue team has slain Baron Nashor».
Posiciones: minimapa de la transmisión (u, v = fracción; mismo encuadre que mapas/grieta.png), precisión ~±0,03 del mapa.
Entre 41:05 y 41:35 hay un salto de tiempo (rótulo «30 segundos después»): ahí no se inventan rutas.
uso: python videos/lol_worlds_2026/j6_3d.py  →  python nucleo/tactica3d/render3d.py videos/lol_worlds_2026/tactica3d/j6.json …
"""
import json
import os

_D = os.path.dirname(os.path.abspath(__file__))
WEB = "/videos/lol_worlds_2026/"
ICO = WEB + "iconos/"

DE, A = 975.0, 1010.27          # tramo del video que cubre (frases jugada6_0 … jugada6_3; la 4 vuelve al VOD real)
# reloj: [t_video, segundo de juego]  (40:00 = 2400)
RELOJ = [(975.0, 2414.0), (983.3, 2420.6), (986.4, 2426.0), (987.6, 2426.0), (991.2, 2429.0),
         (993.8, 2432.5), (994.7, 2434.0), (998.0, 2440.0), (1000.1, 2448.0), (1002.0, 2457.0), (1004.5, 2465.0),
         (1005.6, 2495.0), (1007.35, 2504.9), (1009.1, 2505.7), (1009.9, 2506.0), (1010.27, 2506.15)]


def tv(g):
    """segundo de juego → primer instante del video en que el reloj lo marca"""
    for (t0, g0), (t1, g1) in zip(RELOJ, RELOJ[1:]):
        if g0 <= g <= g1 and g1 > g0:
            return round(t0 + (t1 - t0) * (g - g0) / (g1 - g0), 3)
    return RELOJ[-1][0] if g > RELOJ[-1][1] else RELOJ[0][0]


S = "salto"
# pistas en segundos de juego: (g, u, v[, "salto"])
TL = {
    "Morgan": ("Kled", [(2414, .63, .60), (2422, .64, .58), (2428.5, .64, .57), (2432, .695, .075, S), (2438, .735, .08),
                        (2446, .72, .08), (2452, .66, .075), (2458, .62, .08), (2465, .56, .10), (2495, .31, .27, S),
                        (2506, .305, .275)]),
    "Josedeodo": ("Pantheon", [(2414, .655, .665), (2423, .66, .66), (2428, .66, .56), (2434, .68, .44), (2440, .70, .37),
                               (2446, .71, .34), (2452, .65, .33), (2458, .56, .33), (2465, .47, .31), (2495, .30, .255, S),
                               (2506, .30, .25)]),
    "Quid": ("Akali", [(2414, .70, .60), (2423, .66, .58), (2430, .68, .47), (2436, .72, .38), (2442, .75, .33), (2448, .70, .31),
                       (2454, .62, .35), (2460, .55, .42), (2465, .53, .45), (2495, .43, .45, S), (2506, .42, .47)]),
    "Yeon": ("Xayah", [(2414, .66, .635), (2420.6, .665, .645), (2430, .66, .53), (2436, .69, .40), (2442, .70, .35),
                       (2448, .66, .32), (2454, .58, .32), (2460, .50, .31), (2465, .45, .33), (2495, .295, .31, S),
                       (2506, .29, .315)]),
    "CoreJJ": ("Rakan", [(2414, .60, .72), (2423, .62, .68), (2430, .64, .55), (2436, .67, .42), (2442, .68, .37),
                         (2448, .64, .35), (2454, .57, .36), (2460, .50, .36), (2465, .47, .36), (2495, .27, .355, S),
                         (2506, .27, .36)]),
}
AL = {
    "Breathe": ("Olaf", [(2414, .75, .755), (2423, .76, .72), (2430, .80, .62), (2436, .80, .48), (2442, .78, .33),
                         (2448, .74, .22), (2454, .70, .14), (2460, .66, .08), (2465, .60, .05), (2495, .55, .25, S),
                         (2500, .48, .30), (2504, .42, .39), (2506, .41, .40)]),
    "Tarzan": ("Nocturne", [(2414, .79, .66), (2423, .80, .64), (2428, .83, .62), (2433, .82, .58), (2435.5, .735, .085),
                            (2440, .74, .09), (2446, .70, .15), (2452, .64, .20), (2458, .62, .23), (2465, .64, .21),
                            (2495, .58, .17, S), (2498, .52, .19), (2501, .46, .27), (2504, .41, .37), (2506, .40, .39)]),
    "Shanks": ("Annie", [(2414, .84, .60), (2423, .85, .58), (2430, .89, .47), (2436, .86, .40), (2442, .82, .25),
                         (2448, .78, .20), (2454, .74, .21), (2460, .69, .24), (2465, .67, .26), (2495, .57, .33, S),
                         (2500, .56, .40), (2506, .54, .42)]),
    "Hope": ("Jinx", [(2414, .785, .70), (2423, .80, .66), (2430, .86, .55), (2436, .85, .42), (2442, .82, .27), (2448, .78, .22),
                      (2454, .72, .26), (2460, .66, .31), (2465, .64, .32), (2495, .58, .26, S), (2500, .53, .22),
                      (2504.8, .50, .27), (2506, .50, .27)]),
    "Kael": ("TahmKench", [(2414, .78, .735), (2423, .79, .70), (2430, .86, .55), (2436, .84, .42), (2442, .80, .30),
                           (2448, .74, .22), (2454, .70, .25), (2460, .67, .32), (2465, .67, .35), (2495, .62, .30, S),
                           (2500, .50, .38), (2504, .41, .44), (2506, .39, .45)]),
}
PIT_DRAGON, PIT_BARON = (.675, .705), (.325, .29)
INHIB_TORRE, INHIB = (.71, .07), (.765, .07)


def fichas():
    out = {}
    for eq, grupo in (("TL", TL), ("AL", AL)):
        for jug, (camp, pts) in grupo.items():
            out[jug] = dict(jugador=jug, campeon=camp, equipo=eq, icono=ICO + camp + ".png",
                            puntos=[list(p) for p in pts])
    return out


def escena():
    jg = list(TL) + list(AL)
    return dict(
        de=DE, a=A, titulo="LA JUGADA EN 3D · DATOS DEL MINIMAPA", reloj=[list(r) for r in RELOJ],
        equipos=[dict(id="TL", color="azul", logo=ICO + "equipos/TLAW.png"), dict(id="AL", color="rojo", logo=ICO + "equipos/AL.png")],
        fichas=fichas(),
        estructuras=[
            dict(tipo="torre", u=INHIB_TORRE[0], v=INHIB_TORRE[1], equipo="AL", cae=tv(2428.8)),
            dict(tipo="inhibidor", u=INHIB[0], v=INHIB[1], equipo="AL"),
            dict(tipo="inhibidor", u=.79, v=.205, equipo="AL"), dict(tipo="inhibidor", u=.925, v=.225, equipo="AL"),
            dict(tipo="torre", u=.755, v=.235, equipo="AL"), dict(tipo="torre", u=.93, v=.28, equipo="AL"),
            dict(tipo="nexo", u=.885, v=.115, equipo="AL"),
            dict(tipo="inhibidor", u=.075, v=.775, equipo="TL"), dict(tipo="inhibidor", u=.21, v=.795, equipo="TL"),
            dict(tipo="inhibidor", u=.235, v=.925, equipo="TL"), dict(tipo="nexo", u=.115, v=.885, equipo="TL"),
        ],
        objetivos=[
            dict(nombre="dragón", u=PIT_DRAGON[0], v=PIT_DRAGON[1], img=WEB + "tactica3d/dragon_infernal.png", color="#ff7a2e",
                 muere=tv(2420.6), gana="azul", r=.035),
            dict(nombre="Barón", u=PIT_BARON[0], v=PIT_BARON[1], img=WEB + "tactica3d/baron.png", color="morado", r=.04,
                 vida=[[tv(2495), 16900], [tv(2498), 15619], [tv(2501), 11166], [tv(2504.8), 3634], [tv(2505.3), 3304],
                       [tv(2505.7), 2521], [tv(2506.0), 1166], [A, 1166]],
                 vida_max=16900, numeros_desde=tv(2498)),
        ],
        oleadas=[dict(ruta=[(.47, .062), (.60, .062), (.70, .068), (.745, .072)], de=DE, a=tv(2431), color="azul", n=7,
                      sale=tv(2447))],
        tps=[dict(desde=(.64, .57), a=(.695, .075), en=tv(2428.5), llega=tv(2432), color="azul", alto=10)],
        flechas=[
            dict(id="flanco", pts=[(.80, .21), (.71, .27), (.61, .36)], color="rojo", en=998.25, dur=1.0, sale=1001.2, guion=True,
                 alto=2.5),
            dict(id="retira", pts=[(.70, .345), (.60, .33), (.48, .32)], color="azul", en=1000.2, dur=.9, sale=1002.4, alto=2.0),
        ],
        anillos=[
            dict(u=INHIB_TORRE[0], v=INHIB_TORRE[1], r=.03, color="rojo", en=988.9, sale=991.6),
            dict(u=PIT_BARON[0], v=PIT_BARON[1], r=.055, color="amarillo", en=1005.5, sale=A + 1),
        ],
        proyectiles=[dict(desde=(.50, .27), a=PIT_BARON, de=tv(2504.9), llega=tv(2505.7), color="#ff4fc3", alto=4)],
        focos=[dict(quien="Yeon", de=982.8, a=986.0), dict(quien="Morgan", de=991.7, a=995.2),
               dict(quien="Hope", de=1006.4, a=A + 1)],
        rastros=[dict(quien=j, de=994.6, a=1004.5, ventana=16) for j in jg if j != "Morgan"] +
                [dict(quien="Morgan", de=tv(2432) + .05, a=1004.5, ventana=12)] +
                [dict(quien=j, de=1005.65, a=A + 1, ventana=7) for j in AL],
        niebla=[dict(de=1002.0, a=1004.55, ve="AL", oculta="TL", radio=.06, fuerza=1.0, extra=[(.86, .14, .17)], dur=1.0)],
        hud=[
            dict(de=978.1, a=983.0, texto="11 - 17 EN ASESINATOS", sub="LIQUID VA ABAJO", color="rojo"),
            dict(de=980.6, a=983.0, texto="+3 000 DE ORO", sub="VENTAJA DE LIQUID", color="azul"),
            dict(de=981.5, a=983.0, texto="6 - 2 EN TORRES", sub="LIQUID PRESIONA", color="azul"),
            dict(de=984.7, a=987.4, texto="3 - 3 EN DRAGONES", sub="NADIE TIENE EL ALMA", color="amarillo"),
            dict(de=tv(2429.2), a=994.6, texto="7 - 2 EN TORRES", sub="CAE LA TORRE DEL INHIBIDOR", color="azul"),
        ],
        etiquetas=[
            dict(de=976.3, a=982.4, quien="Quid", texto="TEAM LIQUID", color="azul", dx=-120, dy=-60, tam=28),
            dict(de=976.5, a=982.4, quien="Shanks", texto="ANYONE'S LEGEND", color="rojo", dx=120, dy=-60, tam=28),
            dict(de=983.2, a=986.3, quien="Yeon", texto="YEON REMATA EL DRAGÓN", sub="EL 3.º DE LIQUID", color="azul",
                 dx=-140, dy=-50),
            dict(de=984.6, a=986.3, u=PIT_DRAGON[0], v=PIT_DRAGON[1], alto=7, texto="AL SE QUEDA SIN ALMA", color="rojo",
                 dx=150, dy=40),
            dict(de=988.4, a=991.4, u=.60, v=.062, alto=1, texto="OLEADA DE LIQUID", sub="EMPUJA SOLA", color="azul",
                 dx=-60, dy=110),
            dict(de=990.6, a=992.0, u=INHIB_TORRE[0], v=INHIB_TORRE[1], alto=4, texto="¡CAE LA TORRE!", color="rojo",
                 dx=120, dy=-40),
            dict(de=992.1, a=994.6, u=.695, v=.075, alto=2, texto="TP DE MORGAN", sub="A PRESIONAR EL INHIBIDOR",
                 color="azul", dx=-160, dy=110),
            dict(de=995.0, a=997.9, quien="Shanks", texto="AL SUELTA EL DRAGÓN", sub="Y VUELVE A SU BASE", color="rojo",
                 dx=120, dy=-50),
            dict(de=998.6, a=1001.1, flecha="flanco", texto="INTENTA ENCERRAR A LIQUID", color="rojo", dx=-30, dy=90),
            dict(de=1000.6, a=1002.3, flecha="retira", texto="LIQUID SE RETIRA A TIEMPO", color="azul", dx=-40, dy=-70),
            dict(de=1005.7, a=1007.4, u=PIT_BARON[0], v=PIT_BARON[1], alto=12, texto="LIQUID EMPIEZA EL BARÓN", color="azul",
                 dx=-170, dy=-30),
            dict(de=1006.4, a=A + 1, quien="Hope", texto="HOPE · JINX", sub="COHETE PARA ROBARLO", color="rojo", dx=140, dy=-40),
        ],
        carteles=[
            dict(de=986.45, a=987.55, texto="PAUSA", color="amarillo", tam=60, y=170),
            dict(de=1002.3, a=1004.5, texto="AL, A OSCURAS", sub="CASI SIN VISIÓN DEL MAPA", color="rojo", tam=54, y=170),
            dict(de=1004.6, a=1005.8, texto="30 SEGUNDOS DESPUÉS", sub="41:05 → 41:35", color="amarillo", tam=54, y=170),
        ],
        destellos=[1004.55],
        camara=[
            [975.0, .50, .50, 140, 64, -18, 36], [977.0, .60, .60, 105, 56, -12, 36], [979.5, .68, .66, 64, 50, -6, 36],
            [982.5, .69, .67, 47, 47, 2, 36], [984.2, .68, .66, 42, 50, 6, 36], [986.4, .68, .58, 58, 55, 4, 36],
            [987.6, .68, .40, 82, 60, 0, 36], [989.6, .64, .14, 58, 52, -8, 36], [991.3, .69, .12, 50, 50, -4, 36],
            [992.7, .68, .30, 88, 58, 0, 36], [994.4, .71, .18, 64, 54, 6, 36], [996.6, .76, .34, 94, 60, 10, 36],
            [999.0, .70, .28, 76, 56, 4, 36], [1001.5, .60, .31, 84, 58, -6, 36], [1003.8, .58, .36, 122, 64, -10, 36],
            [1004.6, .52, .38, 132, 66, -12, 36], [1005.6, .38, .27, 66, 53, -14, 36], [1007.0, .40, .27, 60, 50, -6, 36],
            [1008.5, .41, .25, 52, 47, 4, 36], [1010.27, .37, .24, 46, 46, 8, 36],
        ],
    )


if __name__ == "__main__":
    os.makedirs(os.path.join(_D, "tactica3d"), exist_ok=True)
    ruta = os.path.join(_D, "tactica3d", "j6.json")
    json.dump(escena(), open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(ruta)
