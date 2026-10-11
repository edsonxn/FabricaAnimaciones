

# ---------------------------------------------------------------- DUEÑOS (67.5 - 77.5)
Dn = "duenos"
shot(67.50, F_foto("escriba2", z0=1.02, z1=1.25, c0=(0.5, 0.5), c1=(0.45, 0.42), par=(50, 10), tono=(0.5, 0.45, 0.4)),
     [TXT(pal_(Dn, 0, 0, 4), 960, 470, 150, lineas=(2,), sal=w_(Dn, 0, 6) + 0.25)], ent=("tinta", 0.55), grado=dict(polvo=0.5))
shot(70.28, F_clip("carta", inicio=3, z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.6, 0.55), tono=(0.85, 0.78, 0.68)),
     [TXT(pal_(Dn, 1, 0, 5), 960, 250, 110, lineas=(2,), clave=[1])],
     [lambda lz, t: carta(lz, X.estampilla("kircher", "1665", 300), I3, t, 70.75, 1560, 700, 6, desde=(500, 300), dur=0.45),
      lambda lz, t: D.tag_nombre(lz, "Carta a Athanasius Kircher", 1470, 920, t, 71.2, 40)], ent=("aberracion", 0.28))
shot(72.85, F_foto("rodolfo_arcimboldo", z0=1.02, z1=1.25, c0=(0.5, 0.42), c1=(0.5, 0.36), par=(80, 10), tono=(0.9, 0.86, 0.8)),
     [TXT([("el", w_(Dn, 1, 7)), ("emperador", w_(Dn, 1, 8))], 560, 800, 140, lineas=(1,), clave=[1]),
      TXT([("Rodolfo", w_(Dn, 1, 9)), ("II", w_(Dn, 1, 10))], 560, 560, 170, lineas=(1,), clave=[0, 1], sal=74.6)],
     [lambda lz, t: D.tag_nombre(lz, "Rodolfo II", 1500, 260, t, w_(Dn, 1, 9), 56)], ent=("glitch", 0.25))
shot(74.60, F_clip("monedas", inicio=2, z0=1.05, z1=1.3, c0=(0.5, 0.5), c1=(0.6, 0.5), tono=(0.75, 0.7, 0.65)),
     [NUM("600", 540, 360, 380, w_(Dn, 1, 14) - 0.05), TXT([("ducados", w_(Dn, 1, 15)), ("de", w_(Dn, 1, 16)), ("oro", w_(Dn, 1, 17))], 960, 880, 140, lineas=(1,), clave=[1, 2])],
     ent=("destello", 0.3))

# ---------------------------------------------------------------- INTENTOS (77.5 - 100)
It = "intentos"
shot(77.50, F_clip("maquina", inicio=1, z0=1.05, z1=1.3, tono=(0.75, 0.75, 0.7), sat=0.6),
     [TXT([("siglo", w_(It, 0, 3)), ("XX", w_(It, 0, 4))], 960, 540, 200, fnt="impact", clave=[1], mayus=False)], ent=("tinta", 0.5))


def _friedman_ext(lz, t):
    D.tag_nombre(lz, "William Friedman", 560, 860, t, w_(It, 0, 5), 52)


shot(79.05, F_foto("friedman", z0=1.05, z1=1.28, c0=(0.32, 0.42), c1=(0.34, 0.36), par=(80, 18), tono=(0.9, 0.9, 0.9)),
     [TXT([("William", w_(It, 0, 5)), ("Friedman", w_(It, 0, 6))], 1400, 330, 120, lineas=(1,), clave=[1])], [_friedman_ext], ent=("aberracion", 0.28), grado=dict(sat=0.7))
shot(80.45, F_clip("maquina2", inicio=3, z0=1.05, z1=1.3, tono=(0.7, 0.7, 0.68), sat=0.6),
     [TXT([("criptógrafo", w_(It, 0, 8))], 960, 540, 150, fnt="impact", clave=[0])], ent=("corte", 0.001))
shot(81.22, F_pozo(0.5, 0.45, 0.85, (0.26, 0.10, 0.28)),
     [TXT(pal_(It, 0, 12, 14), 960, 800, 110, clave=[]), TXT([("Púrpura", w_(It, 0, 14))], 960, 940, 170, fnt="impact", clave=[0])],
     [lambda lz, t: carta(lz, pola("purple", 640, 1.0, (0.5, 0.42), "Máquina Púrpura"), I3, t, 81.3, 960, 400, 3, desde=(0, -700), dur=0.45)], ent=("glitch", 0.25))
shot(82.90, F_clip("reloj_bolsillo", inicio=6, z0=1.05, z1=1.3, tono=(0.85, 0.75, 0.65)),
     [TXT([("le", w_(It, 0, 15)), ("dedicó", w_(It, 0, 16))], 960, 300, 110, lineas=(1,)), TXT([("años", w_(It, 0, 17))], 960, 640, 260, fnt="impact", clave=[0])], ent=("tinta", 0.45))
shot(84.98, F_borroso("f190", 0.28),
     [TXT(pal_(It, 1, 0, 3), 960, 900, 125, lineas=(1,), clave=[1, 2])],
     [HERO(190, 960, 470, -3, t_in=85.0, desde=(0, 700)),
      lambda lz, t: D.marcador_mano(lz, "tachado", 960, 470, 700, 800, prog(t, w_(It, 1, 2) + 0.1, w_(It, 1, 2) + 0.5), grosor=16),
      lambda lz, t: D.marcador_mano(lz, "tachado", 960, 470, -700, 800, prog(t, w_(It, 1, 2) + 0.25, w_(It, 1, 2) + 0.65), grosor=16)], ent=("corte", 0.001))
shot(86.22, F_clip("humo", inicio=8, z0=1.05, z1=1.25, tono=(0.85, 0.85, 0.9)),
     [NUM("1959", 700, 400, 300, 86.4, color=BL, fnt="pop_bi"), CAP(pal_(It, 1, 3, 6), 700, 620, 52)],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Anagrama", "1959", "Philological Quarterly"), D.poner(420, 420, 1420, 500, 1.0, -10), 0.92 * smooth(prog(t, w_(It, 1, 7), w_(It, 1, 7) + 0.15)))], ent=("destello", 0.3))
shot(88.30, F_foto("folios_hd/f187", z0=1.6, z1=2.0, c0=(0.45, 0.4), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.6, 0.58, 0.54)),
     [TXT([("lenguaje", w_(It, 1, 11)), ("artificial", w_(It, 1, 12))], 960, 540, 190, lineas=(1,), clave=[1])], ent=("aberracion", 0.28))
shot(90.20, F_clip("humo", inicio=1, z0=1.05, z1=1.3, tono=(0.75, 0.8, 0.9)),
     [TXT([("inquietante", w_(It, 2, 4))], 960, 540, 190, fnt="impact", clave=[0], scan=True)], ent=("glitch", 0.28), grado=dict(fuerza_vineta=0.8))
shot(91.72, F_foto("folios_hd/f190", z0=1.9, z1=2.4, c0=(0.25, 0.3), c1=(0.7, 0.6), par=(0, 0), lado=3800, tono=(0.55, 0.53, 0.5)),
     [TXT(pal_(It, 2, 7, 12), 960, 470, 150, lineas=(3,), clave=[2, 4])], ent=("corte", 0.001), grado=dict(fuerza_vineta=0.8))
shot(94.05, F_foto("folios_hd/f187", z0=1.6, z1=1.95, c0=(0.5, 0.4), c1=(0.5, 0.5), par=(0, 0), lado=3800, tono=(0.30, 0.29, 0.27)),
     [TXT([("patrones", w_(It, 3, 3)), ("estadísticos", w_(It, 3, 4))], 960, 130, 90, clave=[0, 1], lineas=()),
      TXT([("idioma", w_(It, 3, 10)), ("real", w_(It, 3, 11))], 960, 950, 150, lineas=(1,), clave=[1])],
     [lambda lz, t: D.grafica_zipf(lz, ZIPF, t, 94.15, W / 2, 500, 1240, 640, dur=3.4),
      lambda lz, t: X.elipse_luz(lz, 900, 560, 230, 150, prog(t, w_(It, 3, 10), w_(It, 3, 11) + 0.4), grosor=6)], ent=("desenfoque", 0.35))
