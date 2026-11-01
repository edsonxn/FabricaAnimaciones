# -*- coding: utf-8 -*-
"""Estado del mundo en función del tiempo global: qué hay encendido, qué ha desaparecido y cuánto se ha destruido.
Versión A (solo O2) entre el comienzo de «aire» y el final de «regreso_a»; versión B (todos los átomos) desde B0.
El cierre vuelve al mundo normal (nada de esto ha pasado de verdad)."""
from motor import prog, e_in, e_out, e_inout, smooth, clamp01
from anclas import A, B0, Z3, Z4

T_O2_FUERA = A.esfuma - 0.05            # versión A: el O2 del aire se esfuma
T_O2_VUELVE = A.vuelve_ra - 0.1         # ... y vuelve
T_FUEGO = A.apagan - 0.05               # los fuegos se apagan (escalonado por objeto)
T_PLANTA = A.llama + 0.1                # la central pierde la llama
T_RED = A.seguridad + 0.2               # se dispara: apagón en cascada
T_B = A.cero_s - 0.1                    # versión B: desaparecen todos los átomos de O
T_B_VUELVE = A.vuelve_rb - 0.2


def estado(t):
    """Diccionario de parámetros 0..1 del paisaje."""
    if t >= Z4[0]:                      # cierre: mundo normal y sano
        return dict(o2=1.0, fuego=1.0, motores=1.0, red=1.0, b=0.0, polvo=0.0, hundir=0.0, hidro=0.0, vida=1.0,
                    cielo_b=0.0, choques=0.0, vuelta_b=0.0, oxido=1.0, fuego_vuelve=0.0, vida_resto=1.0, normal=True,
                    tunel=0.0, mareo=0.0)
    o2 = 1.0
    if t > T_O2_FUERA:
        o2 = 1 - e_out(prog(t, T_O2_FUERA, T_O2_FUERA + 0.35))
    if t > T_O2_VUELVE:
        o2 = e_out(prog(t, T_O2_VUELVE, T_O2_VUELVE + 0.5))
    if t > T_B:
        o2 = 1 - e_out(prog(t, T_B, T_B + 0.3))
    if t > T_B_VUELVE:
        o2 = e_out(prog(t, T_B_VUELVE, T_B_VUELVE + 0.8))
    fuego = 1 - prog(t, T_FUEGO, T_FUEGO + 0.6)
    fuego_vuelve = e_out(prog(t, A.brasas + 0.4, A.brasas + 1.4))          # algunas brasas vuelven a prender
    motores = 1 - prog(t, A.coches - 0.6, A.coches + 0.2)
    if t > A.pilotos:
        motores = e_out(prog(t, A.motores_ra - 0.2, A.motores_ra + 0.8))
    red = 1 - e_in(prog(t, T_RED, A.apagones + 1.2))
    b = e_inout(prog(t, B0, B0 + 2.5))
    polvo = e_inout(prog(t, A.edificios - 0.2, A.hunde + 1.6))
    hundir = e_inout(prog(t, A.hunde - 0.6, A.hunde + 1.8))
    hidro = e_inout(prog(t, A.deja_ag - 0.2, A.convierte + 1.2))
    vida = 1 - e_inout(prog(t, A.terceras_n - 0.3, A.terceras_n + 1.4))
    vida_resto = 1 - e_inout(prog(t, A.segundo_n - 0.4, A.ser_vivo + 0.8))
    oxido = 1 - prog(t, A.oxido - 0.4, A.oxido + 0.8)
    cielo_b = e_inout(prog(t, A.polvo - 0.5, A.hunde + 2.5))
    vuelta_b = e_inout(prog(t, T_B_VUELVE, T_B_VUELVE + 1.0))
    choques = e_out(prog(t, A.choques - 0.3, A.choques + 0.3)) * (1 - prog(t, B0 - 1.0, B0))
    tunel = e_inout(prog(t, A.tunel - 0.5, A.tunel + 0.6)) * (1 - e_out(prog(t, A.vuelve_ra - 0.1, A.vuelve_ra + 0.7)))
    mareo = e_inout(prog(t, A.mareo - 0.3, A.mareo + 0.8)) * (1 - e_out(prog(t, A.vuelve_ra, A.vuelve_ra + 1.0)))
    return dict(o2=o2, fuego=fuego, motores=motores, red=red, b=b, polvo=polvo, hundir=hundir, hidro=hidro,
                vida=vida, vida_resto=vida_resto, cielo_b=cielo_b, choques=choques, vuelta_b=vuelta_b, oxido=oxido,
                fuego_vuelve=fuego_vuelve, normal=False, tunel=tunel, mareo=mareo)
