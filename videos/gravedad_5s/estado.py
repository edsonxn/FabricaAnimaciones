# -*- coding: utf-8 -*-
"""Estado continuo del mundo en función del tiempo global t (parámetros 0..1):
  - salto_intro: pequeño salto al principio («Da un salto pequeño. Siempre vuelves al suelo.»)
  - grav_a: 1.0 con gravedad normal, 0.0 cuando se apaga en la versión A, regresa a 1.0 en «Segundo cinco»
  - alt_casa: flotación leve dentro de la casa (~28 u)
  - alt_parque: subida continua a ~1 m/s hasta 5 m (~290 u, copa del árbol) y caída brusca en caida_a
  - viento: expansión de la atmósfera hacia arriba + viento lateral
  - burbujas_mar: bolas de agua y olas levantadas en el aire
  - deriva: desplazamiento horizontal tangencial mientras no hay gravedad
  - impacto_a: sacudida/polvo al golpear el suelo en Segundo cinco
  - b: versión B activa (espacio: Tierra se hincha y agrieta con lava, órbitas rectas, Sol se expande y apaga, colapso final)
"""
from motor import prog, e_in, e_out, e_inout, clamp01
from mundo_comun import campana, ventana
from anclas import A, B0, Z3, Z4

T_GRAV_OFF = A.cero_a - 0.05
T_GRAV_ON = A.regresa - 0.05
T_IMPACTO = A.cae_ca + 0.35


def estado(t):
    """Diccionario de parámetros 0..1 del paisaje y del espacio."""
    if t >= Z4[0]:
        # Cierre en el parque: gravedad normal, con taza que cae en A.caiga
        caida_taza = e_in(prog(t, A.caiga - 0.15, A.piso_c + 0.05))
        return dict(
            salto_intro=0.0,
            grav_a=1.0,
            alt_casa=0.0,
            alt_parque=0.0,
            alt_cosas=0.0,
            viento=0.0,
            burbujas_mar=0.0,
            deriva=0.0,
            impacto_a=0.0,
            b=0.0,
            normal=True,
            caida_taza=caida_taza,
        )

    salto_intro = campana(t, A.salto - 0.05, A.vuelves + 0.25)

    # Gravedad en la superficie (Versión A)
    grav_a = 1.0
    if t > T_GRAV_OFF:
        grav_a = 1.0 - e_out(prog(t, T_GRAV_OFF, T_GRAV_OFF + 0.35))
    if t > T_GRAV_ON:
        grav_a = e_out(prog(t, T_GRAV_ON, T_GRAV_ON + 0.25))

    # Caída de vuelta al suelo en Segundo 5 (cae de lleno al mismo tiempo)
    caida = e_in(prog(t, T_GRAV_ON + 0.1, T_IMPACTO))
    rebote_suelo = 0.08 * campana(t, T_IMPACTO, T_IMPACTO + 0.38)

    # Flotación dentro de la casa (a ras del piso)
    sube_casa = e_inout(prog(t, A.flotas - 0.4, A.piso_a + 0.6))
    alt_casa = sube_casa * (1.0 - caida) + rebote_suelo * 0.4

    # Subida en el parque (caminando -> 1 m/s -> 5 m en 5 s)
    sube_parque = e_inout(prog(t, A.impulso - 0.2, A.parque + 0.8))
    if t > A.parque + 0.8 and t < T_GRAV_ON + 0.1:
        # Sigue derivando suavemente un poco más arriba durante viento_mar
        sube_parque = min(1.18, 1.0 + 0.18 * prog(t, A.parque + 0.8, T_GRAV_ON))
    alt_parque = max(0.0, sube_parque * (1.0 - caida) + rebote_suelo)

    # Perros, bicicletas, tazas y coches subiendo en cámara lenta
    sube_cosas = e_inout(prog(t, A.perros - 0.3, A.aire_a + 0.5))
    if t > A.aire_a + 0.5 and t < T_GRAV_ON + 0.1:
        sube_cosas = min(1.22, max(sube_cosas, e_inout(prog(t, A.perros - 0.3, T_GRAV_ON))))
    alt_cosas = max(0.0, sube_cosas * (1.0 - caida) + rebote_suelo)

    # Atmósfera que rebota hacia arriba y viento lateral
    viento = ventana(t, A.rebota_v - 0.2, T_GRAV_ON + 0.15, 0.4, 0.3)
    burbujas_mar = e_inout(prog(t, A.oidos, A.burbujas + 0.2)) * (1.0 - caida)
    deriva = e_inout(prog(t, A.viento - 0.3, A.recta_v + 0.4)) * (1.0 - 0.25 * caida)

    impacto_a = ventana(t, T_IMPACTO - 0.05, A.sobreviviria - 0.2, 0.08, 0.8)
    b = e_inout(prog(t, B0, B0 + 1.5))

    return dict(
        salto_intro=salto_intro,
        grav_a=grav_a,
        alt_casa=alt_casa,
        alt_parque=alt_parque,
        alt_cosas=alt_cosas,
        viento=viento,
        burbujas_mar=burbujas_mar,
        deriva=deriva,
        impacto_a=impacto_a,
        b=b,
        normal=False,
        caida_taza=0.0,
    )
