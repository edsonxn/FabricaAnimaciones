# -*- coding: utf-8 -*-
"""Diseño de sonido del plano secuencia: efectos sincronizados con las anclas de cada capítulo."""
import math

import cap_camino as CC
import cap_cerro as CE
import cap_ciudad as CD
import cap_cierre as CZ
import cap_local as CL
import cap_mapa as CM
import cap_mina as CMI
import cap_patio as CP
import cap_plata as CPL
from ctx import INI, FIN


def registrar(m, T_DIVE0, AÑO_HITOS):
    ev = m.ev
    # ---------------------------------------------------------------- mapa
    a = CM.A
    ev(a["mil"] - 0.1, "escribir", 0.5, dur=1.0)
    ev(a["nueva"], "pop", 0.6, tono=1.0)
    ev(a["nueva"] + 0.5, "ding", 0.35, pan=0.3)
    ev(a["ninguna"], "pincel", 0.5, dur=1.2)
    for i in range(0, 15, 2):
        ev(a["cerros"] + i * 0.04, "pop", 0.25, pan=-0.5 + i * 0.07, tono=0.8 + 0.03 * i)
    for i in range(0, 26, 3):
        ev(a["nopales"] + i * 0.05, "pop", 0.22, pan=0.5 - i * 0.04, tono=1.2 + 0.02 * i)
    ev(a["nomadas"] - 0.1, "spray", 0.45, dur=1.0)
    for k, nm in enumerate(("zacatecos", "huachi", "chichi")):
        ev(a[nm], "pop", 0.55, pan=-0.3 + 0.3 * k, tono=1.0 + 0.1 * k)
    ev(a["chichi"] + 0.4, "brillo", 0.45)
    ev(T_DIVE0, "zoom_whoosh", 0.7, dur=3.0)
    # ---------------------------------------------------------------- cerro
    c = CL.A
    ev(c["piedras"], "brillo", 0.5, pan=-0.3)
    ev(c["llega"], "pasos", 0.35, dur=5.0)
    ev(c["odre"], "pop", 0.5)
    ev(c["bufa"], "sello", 0.6, pan=0.3)
    for i in range(3):
        ev(c["arma"] + 0.15 * i, "pop", 0.55, tono=0.9 + 0.12 * i, pan=-0.2 + 0.2 * i)
    ev(c["arma"] + 0.6, "fuego", 0.35, dur=3.0)
    ev(c["ocho"] - 0.2, "sello", 0.55, pan=0.2)
    ev(c["veta"], "pincel", 0.45, dur=2.4)
    for i in range(4):
        ev(c["veta"] + 0.5 + 0.6 * i, "brillo", 0.3, pan=0.3, tono=1.0 + 0.1 * i)
    ev(c["fiebre"], "pasos", 0.5, dur=2.6)
    for i, nm in enumerate(("onate", "ibarra", "banuelos")):
        pass
    # ---------------------------------------------------------------- campamento
    ev(c["tres"] - 0.3, "reloj_rapido", 0.4, dur=1.6)
    ev(c["c49"] + 0.2, "escribir", 0.4, dur=0.8)
    for i in range(18):
        ev(c["casas"] - 0.4 + 0.30 * (i + 3) if i > 2 else c["casas"] - 0.4, "pop", 0.35, pan=-0.6 + 0.07 * i, tono=0.9 + 0.03 * (i % 6))
    ev(c["laderas"], "puf", 0.4)
    ev(c["caro"], "ding", 0.4)
    ev(c["maiz"], "pasos", 0.3, dur=3.0)
    for i in range(34):
        ev(c["t34"] - 0.2 + i * 0.094, "tick", 0.3, tono=1.0 + 0.02 * i)
    ev(c["hosp"], "campana", 0.35, tono=1.2)
    ev(c["c50"] - 0.3, "escribir", 0.4, dur=0.8)
    # ---------------------------------------------------------------- mina
    mi = CMI.A
    ev(mi["bajo"], "viento", 0.5, dur=1.6)
    ev(mi["brutal"], "latido", 0.55)
    t = mi["ini"] + 1.7
    while t < mi["carg"] - 0.5:
        ev(t + 0.4, "clink", 0.5, pan=-0.3, tono=0.9)
        ev(t + 0.4, "golpe_suave", 0.35)
        t += 0.8
    ev(mi["vela"], "brillo", 0.3, pan=0.2)
    ev(mi["carg"] - 0.5, "viento", 0.4, dur=1.6)
    t = CMI.T_CLIMB0
    while t < CMI.T_CLIMB1 - 1.5:
        ev(t, "pasos", 0.25, dur=2.0, pan=-0.1)
        t += 2.0
    for nm in ("pueblos", "llegan", "esclav"):
        ev(mi[nm] - 0.3, "sello", 0.5, pan=0.3)
    ev(mi["doscientos"] - 0.2, "reloj_rapido", 0.4, dur=1.6)
    # ---------------------------------------------------------------- patio
    p = CP.A
    ev(p["siete"] - 0.4, "escribir", 0.45, dur=1.0)
    ev(p["benef"] - 0.2, "sello", 0.5)
    ev(p["muele"] - 0.5, "arena", 0.45, dur=1.2)
    ev(p["mineral"], "pop", 0.4, tono=0.9)
    ev(p["sal"], "puf", 0.4)
    ev(p["sal"] + 0.05, "pop", 0.4, tono=1.1)
    ev(p["mercurio"], "burbuja", 0.5)
    ev(p["mercurio"] + 0.05, "pop", 0.4, tono=1.25)
    t = p["mulas"] - 0.6
    while t < p["semanas"] + 3.0:
        ev(t, "pasos", 0.3, dur=3.0)
        t += 3.0
    for i in range(21):
        ev(p["semanas"] - 0.1 + i * (2.0 / 21), "tick", 0.25, tono=0.9 + 0.01 * i)
    ev(p["atrapa"], "morph", 0.4)
    ev(p["atrapa"] + 1.0, "revelar", 0.45)
    ev(p["atrapa"] + 1.2, "brillo", 0.5, pan=0.2)
    ev(p["pobre"], "pop", 0.4)
    ev(p["espana"], "pop", 0.45)
    # ---------------------------------------------------------------- camino
    k = CC.A
    ev(k["ini"], "pasos", 0.35, dur=3.5)
    ev(k["camino"], "sello", 0.5)
    ev(k["guerra"], "impacto", 0.35, tono=0.9)
    ev(k["c50"] + 0.3, "escribir", 0.4, dur=0.9)
    for i in range(3):
        ev(k["atacan"] - 0.2 + 0.55 * i, "whoosh", 0.4, dur=0.4, pan=0.4 - 0.4 * i)
        ev(k["atacan"] + 0.35 + 0.55 * i, "golpe_suave", 0.5, pan=-0.3)
    for i in range(3):
        ev(k["carav"] + 0.7 * i, "whoosh", 0.35, dur=0.4, pan=0.3)
        ev(k["carav"] + 0.55 + 0.7 * i, "golpe_suave", 0.45)
    ev(k["conflicto"] - 0.2, "sello", 0.5)
    ev(k["presidios"], "impacto", 0.5, tono=1.1)
    ev(k["escolta"], "pasos", 0.4, dur=2.5)
    ev(k["final"], "hmm", 0.4)
    ev(k["n90"] + 0.3, "escribir", 0.45, dur=1.2)
    ev(k["paz"] - 0.1, "sello", 0.7, pan=0.1)
    ev(k["comida"], "bling", 0.35, pan=-0.3)
    ev(k["ropa"], "bling", 0.35)
    ev(k["ganado"], "bling", 0.35, pan=0.3)
    # ---------------------------------------------------------------- ciudad
    d = CD.A
    ev(d["aldea"] - 0.4, "escribir", 0.4, dur=1.5)
    for i in range(12):
        ev(d["aldea"] - 0.3 + 0.3 + 4.2 * i / 12, "puf", 0.3, pan=-0.6 + 0.1 * i)
    ev(d["francis"], "pop", 0.5)
    for i in range(4):
        ev(d["convento"] + 0.8 * i, "campana", 0.4 - 0.05 * i, tono=1.0)
    ev(d["c58"], "escribir", 0.4, dur=1.0)
    ev(d["rey"], "revelar", 0.5)
    ev(d["titulo"] + 0.3, "sello", 0.75)
    ev(d["escudo"], "revelar", 0.5)
    ev(d["escudo"] + 0.3, "brillo", 0.5)
    for nm in ("mercados", "matadero"):
        ev(d[nm], "pop", 0.45)
    # ---------------------------------------------------------------- plata
    pl = CPL.A
    ev(pl["ini"] - 0.4, "zoom_whoosh", 0.6, dur=2.0)
    ev(pl["ini"] + 0.5, "pincel", 0.4, dur=3.4)
    ev(pl["capital"], "pop", 0.45)
    ev(pl["mar"], "ola", 0.4, dur=0.85)
    ev(pl["mar"] + 0.5, "campana", 0.3, tono=0.8)
    ev(pl["sevilla"], "pop", 0.5)
    ev(pl["monedas"] - 0.3, "revelar", 0.4)
    for i in range(14):
        ev(pl["monedas"] + 0.15 * i, "clink", 0.4, pan=-0.6 + 0.09 * i, tono=1.0 + 0.04 * (i % 5))
    for nm in ("guerras", "imperios", "comercio"):
        ev(pl[nm], "pop", 0.5)
    # ---------------------------------------------------------------- cierre
    z = CZ.A
    ev(z["ini"] - 0.3, "zoom_whoosh", 0.7, dur=3.4)
    ev(z["oscuridad"] - 0.6, "apagon", 0.6, dur=1.8)
    t = z["ini"] + 3.6
    while t < z["hoy"] - 0.6:
        ev(t, "clink", 0.35, tono=0.85)
        t += 0.8
    ev(z["hoy"] - 0.4, "amanecer", 0.6, dur=2.5)
    ev(z["hoy"], "impacto", 0.4)
    for i in range(3):
        ev(z["patrimonio"] + 0.7 * i, "campana", 0.4, tono=1.0 + 0.12 * i)
    ev(z["bajo"], "viento", 0.4, dur=1.5)
    ev(z["fin"] + 0.8, "impacto", 0.5, tono=0.8)
    ev(z["fin"] + 1.1, "ding", 0.4)
