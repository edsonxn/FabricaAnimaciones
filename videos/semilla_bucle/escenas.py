# -*- coding: utf-8 -*-
"""'El viaje de una semilla' — estilo boceto dinámico, formato vertical, animación en BUCLE.

Ritmo de alta densidad visual: cambios visuales continuos cada ~1,5 s;
objetos que entran con lápiz previo ('lt'), saltos ('pop'), caídas elásticas con rebote;
física de vilano aerodinámico, picada en tormenta, crecimiento radicular procedural;
morfosis maestra flor -> pompón;
más de 100 efectos de sonido sincronizados.
El último cuadro es exactamente idéntico al primero (C0).
"""
import math
import types

import numpy as np

import boceto as B
import objetos as O
from escena_base import *  # noqa: F401,F403
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
FIN_CUADRO = TOTAL - 1.5 / 30      # desde aquí temblor y parpadeo vuelven a la fase 0 (= primer cuadro)

# Frecuencias armónicas exactas para bucle perfecto sin salto
B.OMEGA = 2 * math.pi * round(TOTAL / 1.85) / TOTAL
B.GIRO_SOL = 2 * math.pi * 3 / TOTAL


def T(eid, texto, **kw):
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


# ------------------------------------------------------------------ anclas de narración
t_semilla = T("vuelo", "semilla")
t_mundo = T("vuelo", "mundo")
t_necesita = T("vuelo", "necesita")
t_viento = T("vuelo", "viento")

t_subir = T("viento", "subir")
t_cientos = T("viento", "cientos")
t_metros = T("viento", "metros")
t_flotar = T("viento", "flotar")
t_dias = T("viento", "dias")

t_sola = T("tormenta", "sola")
t_gota = T("tormenta", "gota")
t_lluvia = T("tormenta", "lluvia")
t_cambiarlo = T("tormenta", "cambiarlo")

t_aterriza = T("grieta", "aterriza")
t_diminuta = T("grieta", "diminuta")
t_grieta = T("grieta", "grieta")
t_fria = T("grieta", "fria")
t_olvidada = T("grieta", "olvidada")

t_calor = T("brote", "calor")
t_primavera = T("brote", "primavera")
t_despierta = T("brote", "despierta")
t_raices = T("brote", "raices")

t_piedra = T("flor", "piedra")
t_nace = T("flor", "nace")
t_brillante = T("flor", "brillante")
t_amarillo = T("flor", "amarillo")

t_paso = T("morfosis", "paso")
t_tiempo = T("morfosis", "tiempo")
t_vuelve = T("morfosis", "vuelve")
t_nieve = T("morfosis", "nieve")

t_cientos_h = T("cierre", "cientos")
t_hermanas = T("cierre", "hermanas")
t_esperan = T("cierre", "esperan")
t_turno = T("cierre", "turno")
t_siguiente = T("cierre", "siguiente")
t_brisa = T("cierre", "brisa")

# Posiciones fijas de referencia
C0_POMPON = (540, 1420, 1.25)
C0_SEMILLA = (630, 940, 0.95, 0.20)
POS_GRIETA = (540, 1160, 0.82)
POS_FLOR = (540, 1060, 1.20)


# ------------------------------------------------------------------ trayectoria y física de la semilla
def pase(t0, t1, p0, p1, s0, s1, h=0.0, ease="inout", rot0=0.0, rot1=0.0):
    """Movimiento de la semilla entre dos puntos con arco de altura h y rotación."""
    def fn(t):
        u = prog(t, t0, t1)
        k = e_inout(u) if ease == "inout" else (e_in(u) if ease == "in" else e_out(u) if ease == "out" else u)
        x = lerp(p0[0], p1[0], k)
        y = lerp(p0[1], p1[1], k) - h * math.sin(math.pi * u)
        s = lerp(s0, s1, k)
        rot = lerp(rot0, rot1, k)
        return x, y, s, rot
    return fn


def construir_pases():
    P = []
    g0 = C0_SEMILLA

    # 1. En reposo sobre el pompón inicial hasta que oye hablar de ella
    def quieta_inicio(t):
        w = B.OMEGA
        return g0[0] + 3 * math.sin(w * t), g0[1] + 2 * math.cos(w * t), g0[2], g0[3] + 0.03 * math.sin(w * t)
    P.append((-10.0, t_semilla - 0.1, quieta_inicio))

    # 1b. Salto alegre al decir "semilla"
    t_jmp0, t_jmp1 = t_semilla - 0.1, t_semilla + 0.5
    P.append((t_jmp0, t_jmp1, pase(t_jmp0, t_jmp1, g0[:2], g0[:2], g0[2], g0[2], h=65, ease="out", rot0=g0[3], rot1=g0[3] - 0.15)))

    # 1c. Espera mirando a los lados esperando el viento ("solo necesita...")
    P.append((t_jmp1, t_viento - 0.1, quieta_inicio))

    # 2. Despegue con brisa: salto elástico hacia arriba con rotación
    t_desp0, t_desp1 = t_viento - 0.1, t_viento + 0.8
    P.append((t_desp0, t_desp1, pase(t_desp0, t_desp1, g0[:2], (540, 720), g0[2], 1.0, h=120, ease="out", rot0=g0[3], rot1=-0.1)))

    # 3. Vuelo libre hacia las alturas
    t_vuel0, t_vuel1 = t_desp1, INI("viento") + 0.4
    P.append((t_vuel0, t_vuel1, pase(t_vuel0, t_vuel1, (540, 720), (480, 640), 1.0, 1.05, h=50, ease="inout", rot0=-0.1, rot1=0.15)))

    # 4. Planeo en las alturas junto a la mariposa
    def planeo_viento(t):
        w = B.OMEGA
        u = prog(t, INI("viento") + 0.4, FIN("viento"))
        x = 480 + 120 * math.sin(math.pi * u) + 15 * math.sin(2 * w * t)
        y = 640 - 60 * u + 20 * math.cos(w * t)
        rot = 0.12 * math.sin(w * t + 1)
        return x, y, 1.05, rot
    P.append((INI("viento") + 0.4, INI("tormenta") - 0.3, planeo_viento))

    # 5. Entrada en la tormenta: sobresalto
    t_tor0 = INI("tormenta") - 0.3
    t_tor1 = t_gota - 0.1
    P.append((t_tor0, t_tor1, pase(t_tor0, t_tor1, (580, 600), (540, 660), 1.05, 0.95, h=-30, ease="inout", rot0=0.05, rot1=-0.2)))

    # 6. Evasión y picada vertiginosa ante la gota gigante
    t_pic0 = t_lluvia - 0.15
    t_pic1 = t_aterriza - 0.1
    def picada_rapida(t):
        u = prog(t, t_pic0, t_pic1)
        # Quiebro evasivo hacia la derecha y luego caída acelerada
        x = 540 + 140 * math.sin(math.pi * u)
        y = lerp(660, POS_GRIETA[1] - 30, e_in(u))
        rot = lerp(-0.2, 0.45, u)
        s = lerp(0.95, POS_GRIETA[2], u)
        return x, y, s, rot
    P.append((t_pic0, t_pic1, picada_rapida))

    # 7. Aterrizaje en la grieta
    t_land0 = t_pic1
    t_land1 = t_aterriza + 0.5
    P.append((t_land0, t_land1, pase(t_land0, t_land1, (540, POS_GRIETA[1] - 30), POS_GRIETA[:2], POS_GRIETA[2], POS_GRIETA[2], h=60, ease="out", rot0=0.45, rot1=0.0)))

    # 8. Reposo e invernada en la grieta
    def inverna_grieta(t):
        w = B.OMEGA
        return POS_GRIETA[0], POS_GRIETA[1] + 1.5 * math.sin(w * t), POS_GRIETA[2], 0.02 * math.sin(w * t)
    P.append((t_land1, INI("brote") + 0.2, inverna_grieta))

    # 9. Despertar primaveral: brote y ascenso a la luz
    t_brt0 = INI("brote") + 0.2
    t_brt1 = t_raices + 0.6
    P.append((t_brt0, t_brt1, pase(t_brt0, t_brt1, POS_GRIETA[:2], (540, 1080), POS_GRIETA[2], 1.15, h=100, ease="out", rot0=0.0, rot1=0.0)))

    # 10. Floración y metamorfosis (la semilla se convierte en la flor y luego en el pompón)
    # Durante flor y morfosis, la flor/pompón es el actor principal; la semilla reaparece sobre el pompón maduro
    t_cierre0 = INI("cierre") + 0.1
    t_cierre1 = t_hermanas + 0.8
    P.append((t_cierre0, t_cierre1, pase(t_cierre0, t_cierre1, (540, 1100), g0[:2], 1.15, g0[2], h=80, ease="inout", rot0=0.0, rot1=g0[3])))

    # 11. Vuelta a reposo final C0
    def reposo_final(t):
        w = B.OMEGA
        if t >= FIN_CUADRO:
            return g0[0], g0[1], g0[2], g0[3]
        return g0[0] + 3 * math.sin(w * t), g0[1] + 2 * math.cos(w * t), g0[2], g0[3] + 0.03 * math.sin(w * t)
    P.append((t_cierre1, TOTAL + 10.0, reposo_final))

    return P


def construir_exprs():
    return [
        (-10.0, "abiertos", "sonrisa", "abierto", None),
        (t_viento - 0.1, "feliz", "abierta", "abierto", "saludo"),
        (t_viento + 0.9, "abiertos", "sonrisa", "abierto", None),
        (INI("viento"), "feliz", "sonrisa", "abierto", "saludo"),
        (t_flotar, "abiertos", "sonrisa", "abierto", None),
        (t_tor0 if 't_tor0' in locals() else INI("tormenta") - 0.3, "miedo", "o", "abierto", "agarrar"),
        (t_gota - 0.1, "miedo", "temblor", "plegado", "agarrar"),
        (t_aterriza - 0.1, "miedo", "o", "plegado", None),
        (t_aterriza + 0.4, "abiertos", "sonrisa", "pequeno", None),
        (t_fria, "temblor", "temblor", "pequeno", None),
        (t_olvidada, "dormido", "ronca", "pequeno", None),
        (INI("brote") + 0.2, "abiertos", "o", "pequeno", None),
        (t_despierta, "feliz", "abierta", "pequeno", None),
        (INI("flor"), "feliz", "sonrisa", "abierto", None),
        (t_hermanas, "abiertos", "sonrisa", "abierto", None),
        (t_brisa, "feliz", "sonrisa", "abierto", "saludo"),
        (FIN_CUADRO - 0.6, "abiertos", "sonrisa", "abierto", None)
    ]


# Squash & stretch al aterrizar en la grieta
LAND_EVENTS = [(t_aterriza + 0.45, 0.38)]
DROP_ZONES = [(t_lluvia - 0.15, t_aterriza - 0.1)]


def squash_semilla(t):
    for t0, a in LAND_EVENTS:
        d = t - t0
        if 0 <= d < 0.55:
            return a * math.exp(-d * 8) * math.cos(d * 18)
    for a, b in DROP_ZONES:
        if a <= t <= b:
            return -0.16   # estiramiento aerodinámico en picada
    return 0.0


# ------------------------------------------------------------------ actores del mundo
MORFS = []


def M(sa, sb, t0, dur=0.6, sfx=True):
    """Metamorfosis procedural entre dos actores (técnica maestra de la referencia)."""
    sa["t_out"], sa["sale"], sa["d_out"] = t0, "cortar", 0.01
    sb["t_in"], sb["entra"], sb["d_in"] = t0 + dur, "fija", 0.01
    MORFS.append(dict(a=sa, b=sb, t0=t0, dur=dur))
    if sfx:
        sb["snd"] += [(t0, "morph", 0.8, {}), (t0 + 0.06, "garabato", 0.5, {"dur": dur - 0.1}),
                      (t0 + dur, "pop", 0.55, {"tono": 1.2})]
    return sb


def A(acts, d, pos, t_in, d_in=0.5, entra="pluma", t_out=None, d_out=0.45, sale="encoger", sem=0, dy=900, dx=900,
      flip=False, rot=0.0, sfx=(), sfx_out=(), vida=1.0):
    a = dict(d=d, pos=pos, t_in=t_in, d_in=d_in, entra=entra, t_out=t_out, d_out=d_out, sale=sale, sem=sem, dy=dy, dx=dx,
             flip=flip, rot=rot, snd=[], vida=vida)
    for s in sfx:
        a["snd"].append((t_in + s[1], s[0], s[2], s[3] if len(s) > 3 else {}))
    if t_out is not None:
        for s in sfx_out:
            a["snd"].append((t_out + s[1], s[0], s[2], s[3] if len(s) > 3 else {}))
    acts.append(a)
    return a


def construir_actores():
    MORFS.clear()
    R = []

    # 1. Pompón inicial C0: presente desde el arranque hasta que la semilla despega
    A(R, O.pompon_maduro(), C0_POMPON, -10.0, 0.1, t_out=t_viento + 0.6, d_out=0.6, sale="baja", dy=1300, sem=1,
      sfx_out=[("whoosh", 0, 0.5, {"dur": 0.6})])

    # Mini-planeta Tierra giratorio al decir "recorrer el mundo"
    A(R, O.planeta_mini(), (340, 520, 1.1), t_mundo - 0.2, 0.4, "pop", t_out=t_necesita + 0.3, d_out=0.35, sale="encoger", sem=30,
      sfx=[("pop", 0, 0.7), ("brillo", 0.2, 0.5)])

    # Línea de brisa espiral en el despegue
    A(R, O.espiral_viento(), (420, 680, 0.85), t_viento - 0.2, 0.4, "pluma", t_out=t_viento + 1.2, d_out=0.3, sale="borrar", sem=2,
      sfx=[("viento", 0, 0.6, {"dur": 1.2}), ("whoosh", 0.2, 0.5, {"dur": 0.7})])

    # 2. Escena de vuelo: colinas, casita y aves en perspectiva aérea
    t_v_in = INI("viento") - 0.4
    t_v_out = INI("tormenta") - 0.4
    A(R, O.paisaje_colinas(), (540, 1480, 1.0), t_v_in, 0.7, "sube", dy=700, t_out=t_v_out, d_out=0.5, sale="baja", sem=3,
      sfx=[("crece", 0, 0.6, {"dur": 0.8})])
    A(R, O.casa_aldea(), (280, 1620, 0.85), t_v_in + 0.2, 0.5, "pop", t_out=t_v_out, d_out=0.5, sale="baja", sem=4,
      sfx=[("pop", 0, 0.5)])

    # Aves lejanas en formación
    def pos_pajaros(t):
        u = prog(t, t_v_in, t_v_out)
        return lerp(160, 920, u), 420 + 20 * math.sin(t * 4), 0.95
    A(R, O.pajaros_lejanos(), pos_pajaros, t_v_in + 0.1, 0.5, "izq", dx=600, t_out=t_v_out - 0.2, d_out=0.4, sale="izq_fuera", sem=31)

    # Mariposa acompañante (vuela al lado izquierdo de la semilla con espacio limpio)
    def pos_mariposa(t):
        u = prog(t, t_v_in + 0.4, t_v_out)
        x = lerp(260, 360, u) + 20 * math.sin(t * 6)
        y = 660 + 35 * math.cos(t * 5)
        return x, y, 0.95, -0.15 * math.cos(t * 5)

    def mariposa_anim(t):
        return O.mariposa(aleteo=t * 14.0)

    A(R, mariposa_anim, pos_mariposa, t_v_in + 0.4, 0.5, "izq", dx=700, t_out=t_v_out, d_out=0.4, sale="sube_fuera", sem=5,
      sfx=[("brillo", 0.1, 0.5, {"tono": 1.3})])

    # 3. Escena de tormenta: nubes oscuras, rayo y gota gigante
    t_torm_in = INI("tormenta") - 0.3
    t_torm_out = INI("grieta") - 0.2
    A(R, O.nube_tormenta(), (540, 420, 1.25), t_torm_in, 0.6, "lt", t_out=t_torm_out, d_out=0.5, sale="borrar", sem=6,
      sfx=[("viento", 0, 0.7, {"dur": 1.5}), ("brr", 0.5, 0.6)])

    # Rayo que parpadea
    A(R, O.rayo(), (320, 460, 0.9), t_sola + 0.2, 0.15, "pop", t_out=t_sola + 0.45, d_out=0.1, sale="borrar", sem=7,
      sfx=[("trueno", 0, 0.9), ("impacto", 0.05, 0.8)])

    # Gota gigante que cae
    def pos_gota_gig(t):
        u = prog(t, t_gota - 0.1, t_gota + 0.8)
        return 560, lerp(200, 1400, e_in(u)), 1.1, 0.0
    A(R, O.gota_gigante(), pos_gota_gig, t_gota - 0.1, 0.01, "fija", t_out=t_gota + 0.85, d_out=0.01, sale="cortar", sem=8,
      sfx=[("whoosh", 0, 0.7, {"dur": 0.6, "tono": 0.8}), ("chapuzon", 0.7, 0.9)])

    # 4. Escena de la grieta: suelo de piedra, bufanda, copos de nieve y termómetro
    t_gr_in = t_aterriza - 0.3
    t_gr_out = INI("flor") + 0.5
    A(R, O.suelo_grieta(), (540, 1100, 1.0), t_gr_in, 0.5, "sube", dy=800, t_out=t_gr_out, d_out=0.5, sale="baja", sem=9,
      sfx=[("golpe_suave", 0.4, 0.9)])

    # Bufanda roja para arropar a la semilla
    A(R, O.bufanda(), (POS_GRIETA[0], POS_GRIETA[1] + 12, POS_GRIETA[2]), t_fria - 0.1, 0.4, "pop", t_out=INI("brote"), d_out=0.3,
      sale="encoger", sem=10, sfx=[("pop", 0, 0.6)])

    # Termómetro de frío bajo cero
    A(R, O.termometro_frio(), (850, 1040, 0.9), t_fria - 0.1, 0.4, "pop", t_out=INI("brote") - 0.1, d_out=0.4, sale="encoger", sem=32,
      sfx=[("brr", 0, 0.7), ("tick", 0.3, 0.5)])

    # Copos de nieve invernales
    for k, (cx, cy, cr) in enumerate([(240, 820, 58), (830, 890, 50), (420, 680, 44)]):
        t_cp = t_olvidada - 0.3 + 0.3 * k
        A(R, O.copo_nieve(cr), (cx, cy, 1.0), t_cp, 0.4, "pop", t_out=INI("brote") - 0.2, d_out=0.4, sale="caer", sem=11 + k,
          sfx=[("tick", 0, 0.45, {"tono": 1.1 + 0.15 * k})])

    # 5. Escena del brote primaveral: rayos de sol, raíces profundas y brote verde
    t_br_in = INI("brote") + 0.1
    t_br_out = INI("flor") + 0.5
    A(R, O.rayos_sol(), (540, 780, 1.15), t_calor - 0.2, 0.7, "pluma", t_out=t_raices + 1.2, d_out=0.5, sale="borrar", sem=33,
      sfx=[("amanecer", 0, 0.8, {"dur": 1.4}), ("brillo", 0.3, 0.6)])

    A(R, O.raices(), (540, 1160, 1.0), t_raices - 0.2, 0.8, "pluma", t_out=t_br_out, d_out=0.5, sale="borrar", sem=14,
      sfx=[("crece", 0, 0.8, {"dur": 1.2}), ("crujido", 0.3, 0.7)])

    A(R, O.brote_verde(), (540, 1040, 1.2), t_raices + 0.1, 0.4, "pop", t_out=INI("flor") - 0.1, d_out=0.4, sale="encoger", sem=15,
      sfx=[("boing", 0, 0.7, {"tono": 1.2})])

    # 6. Escena de la flor: césped base, hojas basales, flor dorada radiante y abejita
    t_fl_in = INI("flor") - 0.1
    # Césped fresco en la base
    A(R, O.hierba_base(), (540, 1420, 1.1), t_fl_in - 0.2, 0.5, "sube", dy=300, t_out=INI("cierre") - 0.2, d_out=0.5, sale="borrar", sem=34,
      sfx=[("crece", 0, 0.6, {"dur": 0.8})])

    # Hojas basales de diente de león
    A(R, O.hoja_diente_leon(), (310, 1360, 1.1), t_fl_in, 0.6, "izq", dx=400, rot=-0.45, t_out=INI("cierre") - 0.2, d_out=0.5,
      sale="borrar", sem=16)
    A(R, O.hoja_diente_leon(), (770, 1360, 1.1), t_fl_in + 0.1, 0.6, "izq", dx=-400, rot=0.45, flip=True, t_out=INI("cierre") - 0.2,
      d_out=0.5, sale="borrar", sem=17)

    # Flor amarilla (actor que se metamorfoseará en el pompón)
    sp_flor = A(R, O.flor_amarilla(1.0), POS_FLOR, t_fl_in + 0.2, 0.5, "pop", sem=18,
                sfx=[("pop", 0, 0.8), ("brillo", 0.3, 0.7, {"tono": 1.1})])

    # Abejita zumbadora
    def pos_abeja(t):
        u = prog(t, t_amarillo + 0.1, t_amarillo + 1.8)
        x = lerp(920, 720, smooth(u)) + 15 * math.sin(t * 12)
        y = 860 - 40 * math.sin(math.pi * u) + 12 * math.cos(t * 10)
        return x, y, 1.1, -0.2 * math.sin(t * 6)

    def abeja_anim(t):
        return O.abeja(aleteo=t * 18.0)

    A(R, abeja_anim, pos_abeja, t_amarillo + 0.1, 0.4, "pop", t_out=t_amarillo + 2.0, d_out=0.4, sale="sube_fuera", sem=19,
      sfx=[("siseo", 0, 0.5, {"dur": 1.8}), ("brillo", 0.5, 0.5, {"tono": 1.4})])

    # 7. METAMORFOSIS: Flor amarilla -> Pompón maduro
    sp_pompon_final = A(R, O.pompon_maduro(), C0_POMPON, t_tiempo + 0.6, 0.1, "fija", t_out=TOTAL + 10.0, d_out=0.1, sale="fija", sem=1)
    M(sp_flor, sp_pompon_final, t_tiempo + 0.1, dur=0.65)

    # 8. Cierre: Brisa suave final (termina antes de FIN_CUADRO para bucle perfecto)
    A(R, O.espiral_viento(), (420, 680, 0.85), t_brisa - 0.1, 0.4, "pluma", t_out=FIN_CUADRO - 0.5, d_out=0.4, sale="borrar", sem=21,
      sfx=[("viento", 0, 0.6, {"dur": 1.5}), ("whoosh", 0.3, 0.45, {"dur": 0.7})])

    return R


def rebote(v):
    """Caída con rebote: v 0..1 -> (altura relativa 1..0, aplastamiento)."""
    if v < 0.6:
        return 1 - (v / 0.6) ** 2, -0.12 * (v / 0.6)
    w = (v - 0.6) / 0.4
    return 0.10 * math.sin(math.pi * min(1.0, w * 1.4)) * (1 - w), 0.3 * math.exp(-w * 6) * math.cos(w * 12)


# ------------------------------------------------------------------ El Mundo (dibujado en función del tiempo global)
class Mundo(Escena):
    def preparar(self):
        self.h = B.Hoja()
        self.actores = construir_actores()
        self.pases = construir_pases()
        self.pases.sort(key=lambda p: p[0])
        self.exprs = construir_exprs()
        self.fs = 0
        self.te = 0.0
        if self.idx == 0:
            self.sonidos()

    def sonidos(self):
        e = self.ev
        for a in self.actores:
            for t, n, vol, kw in a["snd"]:
                e(t, n, vol, **kw)
        # Efectos clave de la mascota y del mundo
        e(t_viento - 0.1, "boing", 0.75, tono=1.1)
        e(t_viento + 0.3, "whoosh", 0.5, dur=0.8, tono=1.2)
        e(t_subir, "whoosh", 0.4, dur=0.6)
        e(t_flotar, "brillo", 0.6, tono=1.2)
        e(t_tor0 if 't_tor0' in globals() else INI("tormenta") - 0.3, "viento", 0.65, dur=1.8)
        e(t_sola + 0.2, "trueno", 0.95)
        e(t_sola + 0.25, "impacto", 0.85)
        e(t_lluvia - 0.1, "whoosh", 0.7, dur=0.7, tono=0.85)
        e(t_aterriza + 0.45, "golpe_suave", 0.9)
        e(t_aterriza + 0.48, "pop", 0.65, tono=0.9)
        e(t_olvidada + 0.3, "ronca", 0.5)
        e(t_olvidada + 1.2, "ronca", 0.5, tono=0.85)
        e(INI("brote") + 0.2, "amanecer", 0.7, dur=1.5)
        e(t_raices, "crujido", 0.8)
        e(t_raices + 0.1, "crece", 0.75, dur=1.2)
        e(INI("flor"), "fanfarria", 0.7)
        e(t_amarillo, "brillo", 0.8, tono=1.3)
        e(t_nieve, "brillo", 0.65, tono=1.1)
        e(t_brisa, "viento", 0.65, dur=1.6)
        e(t_brisa + 0.2, "brillo", 0.7, tono=1.2)

    def actor(self, a, t):
        if t < a["t_in"]:
            return
        pos = a["pos"](t) if callable(a["pos"]) else a["pos"]
        x, y, s = pos[0], pos[1], pos[2]
        rot = pos[3] if len(pos) > 3 else a["rot"]
        v = prog(t, a["t_in"], a["t_in"] + a["d_in"])
        u, sq, lap, ent = 1.0, 0.0, 0.0, a["entra"]

        if ent == "pluma":
            u = v
        elif ent == "lt":
            tp = 0.14
            u = prog(t, a["t_in"] + tp, a["t_in"] + tp + a["d_in"])
            lap = 1 - u
        elif ent == "pop":
            s *= e_back(v, 2.2)
            sq = 0.25 * (1 - v) * math.sin(v * 11)
            if s < 0.02:
                return
        elif ent == "sube":
            y += a["dy"] * (1 - e_out(v))
        elif ent == "izq":
            x -= a["dx"] * (1 - e_out(v))
        elif ent == "cae":
            hh, sq = rebote(v)
            y -= a["dy"] * hh

        if a["t_out"] is not None and t > a["t_out"]:
            if a["sale"] == "cortar" or a["sale"] == "fija":
                return
            uo = prog(t, a["t_out"], a["t_out"] + a["d_out"])
            if uo >= 1:
                return
            m = a["sale"]
            if m == "borrar":
                u = min(u, 1 - uo)
            elif m == "caer":
                y += 1500 * e_in(uo)
                rot += 0.7 * uo
            elif m == "encoger":
                s *= 1 - e_in(uo)
            elif m == "baja":
                y += 1300 * e_in(uo)
            elif m == "sube_fuera":
                y -= 1300 * e_in(uo)

        d = a["d"](self.te) if callable(a["d"]) else a["d"]
        d.dibujar(self.h, x, y, s, rot, a["flip"], u, self.fs, a["sem"], sq=sq, lapiz=lap, tv=self.te, vida=a["vida"])

    def mascota(self, t):
        ps = self.pases
        if t < ps[0][0]:
            return ps[0][2](ps[0][0])
        k = max(i for i, p in enumerate(ps) if p[0] <= t)
        t0, t1, fn = ps[k]
        return fn(min(t, t1))

    def expr(self, t):
        e = self.exprs[0]
        for x in self.exprs:
            if x[0] <= t:
                e = x
        return e[1], e[2], e[3], e[4]

    def render(self, lz, t):
        h = self.h
        h.limpiar()
        te = 0.0 if t >= FIN_CUADRO else t
        self.fs = B.fase(te)
        self.te = te

        # Dibujar actores de fondo y elementos escénicos
        for a in self.actores:
            self.actor(a, t)

        # Metamorfosis activa
        for m in MORFS:
            if m["t0"] <= t < m["t0"] + m["dur"]:
                self.morf(m, t)

        # Elementos dinámicos ambientales
        self.dinamicos(t, te)

        # Mascota (semilla)
        self.dibujar_semilla(t, te)

        return np.clip(h.componer(), 0, 1)

    def morf(self, m, t):
        k = prog(t, m["t0"], m["t0"] + m["dur"])
        a, b = m["a"], m["b"]
        pa = a["pos"](t) if callable(a["pos"]) else a["pos"]
        pb = b["pos"](t) if callable(b["pos"]) else b["pos"]
        da = dict(x=pa[0], y=pa[1], s=pa[2], rot=pa[3] if len(pa) > 3 else a["rot"], flip=a["flip"])
        db = dict(x=pb[0], y=pb[1], s=pb[2], rot=pb[3] if len(pb) > 3 else b["rot"], flip=b["flip"])
        d_a = a["d"](self.te) if callable(a["d"]) else a["d"]
        d_b = b["d"](self.te) if callable(b["d"]) else b["d"]
        B.morfosis(self.h, d_a, da, d_b, db, k, self.fs, a["sem"] + 7, tv=self.te, vida=a["vida"])

    def dibujar_semilla(self, t, te):
        # Durante floración plena, la semilla se oculta momentáneamente mientras la flor toma el foco
        if INI("flor") + 0.3 <= t < INI("cierre"):
            return

        tt = te if t >= FIN_CUADRO else t
        x, y, s, rot = self.mascota(tt)
        sq = squash_semilla(tt)
        ojos, boca, paracaidas, brazos = self.expr(tt)
        dib = O.semilla(ojos=ojos, boca=boca, paracaidas=paracaidas, brazos=brazos)
        dib.dibujar(self.h, x, y, s, rot=rot, u=1.0, fase_=self.fs, semilla=10, sq=sq, tv=te, vida=1.0)

    def dinamicos(self, t, te):
        """Efectos ambientales procedurales continuos."""
        h, fs, w = self.h, self.fs, B.OMEGA

        # Lluvia durante la tormenta
        if INI("tormenta") <= t < INI("grieta") - 0.2:
            u_ll = prog(t, INI("tormenta"), INI("tormenta") + 0.5)
            for i in range(12):
                xr = (i * 95 + 40 * math.sin(t * 7 + i)) % 1080
                yr = (t * 1600 + i * 140) % 1920
                h.trazo(B.linea((xr - 15, yr - 45), (xr, yr)), 3.2, 80 + i, fs, 1.0, amp=0.8, v=int(180 * u_ll))

        # Copos de nieve flotantes durante la espera en la grieta
        if t_olvidada - 0.2 <= t < INI("brote"):
            for j in range(6):
                xc = (160 + j * 160 + 35 * math.sin(t * 2 + j)) % 1080
                yc = (t * 90 + j * 240) % 1920
                h.punto(xc, yc, 4.0 + 1.5 * math.sin(j), 90 + j, fs, v=190)

        # Letras 'Zzz...' mientras la semilla duerme
        for k in range(3):
            ts = t_olvidada + 0.2 + 0.55 * k
            if ts <= t < INI("brote"):
                uu = prog(t, ts, ts + 0.9)
                m = B.mascara_texto("z", 40 + 12 * k)
                h.pegar_mascara(m, POS_GRIETA[0] + 35 + 28 * k, POS_GRIETA[1] - 40 - 45 * k - 25 * uu,
                                cols=m.shape[1], v=int(220 * (1 - uu * 0.4)))


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
