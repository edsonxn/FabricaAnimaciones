

# ---------------------------------------------------------------- DUEÑOS (67.5 - 77.5)
Dn = "duenos"
shot(67.50, F_foto("escriba2", z0=1.02, z1=1.22, c0=(0.5, 0.5), c1=(0.45, 0.42), par=(50, 10), tono=(0.5, 0.45, 0.4)),
     [R(pal_(Dn, 0, 0, 7), W / 2, 520, 92, lineas=(4,), sal=w_(Dn, 0, 6) + 0.4)], ent=("tinta", 0.7), grado=dict(polvo=0.4))
shot(70.28, F_clip("carta", inicio=3, z0=1.05, z1=1.25, c0=(0.5, 0.5), c1=(0.6, 0.55), tono=(0.85, 0.78, 0.68)),
     [R(pal_(Dn, 1, 0, 5), 900, 250, 88, lineas=(3,))],
     [lambda lz, t: carta(lz, X.estampilla("kircher", "1665", 300), I3, t, 70.9, 1560, 700, 6, desde=(500, 300), dur=0.55),
      lambda lz, t: D.tag_nombre(lz, "Carta a Athanasius Kircher", 1470, 920, t, 71.4, 40)], ent=("fuga", 0.7))
shot(72.85, F_foto("rodolfo_arcimboldo", z0=1.02, z1=1.2, c0=(0.5, 0.42), c1=(0.5, 0.36), par=(80, 10), tono=(0.9, 0.86, 0.8)),
     [S([("Rodolfo", w_(Dn, 1, 9)), ("II", w_(Dn, 1, 10))], 560, 700, 130, lineas=(1,))],
     [lambda lz, t: D.tag_nombre(lz, "El emperador", 500, 300, t, w_(Dn, 1, 8), 52)], ent=("fundido", 0.6))
shot(74.60, F_clip("monedas", inicio=2, z0=1.05, z1=1.25, c0=(0.5, 0.5), c1=(0.6, 0.5), tono=(0.75, 0.7, 0.65)),
     [N("600", 540, 380, 340, w_(Dn, 1, 14) - 0.05), S([("Ducados", w_(Dn, 1, 15)), ("De", w_(Dn, 1, 16)), ("Oro", w_(Dn, 1, 17))], 960, 900, 100)], ent=("fundido", 0.6))

# ---------------------------------------------------------------- INTENTOS (77.5 - 100)
It = "intentos"
shot(77.50, F_clip("maquina", inicio=1, z0=1.05, z1=1.25, tono=(0.75, 0.75, 0.7), sat=0.6),
     [R(pal_(It, 0, 0, 5), W / 2, 820, 80, lineas=(3,))], ent=("tinta", 0.7))
shot(79.05, F_foto("friedman", z0=1.05, z1=1.25, c0=(0.32, 0.42), c1=(0.34, 0.36), par=(80, 18), tono=(0.9, 0.9, 0.9)),
     [S([("William", w_(It, 0, 5)), ("Friedman", w_(It, 0, 6))], 1420, 300, 104, lineas=(1,))],
     [lambda lz, t: D.tag_nombre(lz, "Criptógrafo", 560, 860, t, w_(It, 0, 8), 48)], ent=("fundido", 0.6), grado=dict(sat=0.7))
shot(81.22, F_pozo(0.5, 0.45, 0.85, (0.26, 0.10, 0.28)),
     [R(pal_(It, 0, 11, 15), W / 2, 880, 84, lineas=(2,))],
     [lambda lz, t: carta(lz, pola("purple", 640, 1.0, (0.5, 0.42), "Máquina Púrpura"), I3, t, 81.3, 960, 400, 3, desde=(0, -700), dur=0.55)], ent=("fuga", 0.7))
shot(82.90, F_clip("reloj_bolsillo", inicio=6, z0=1.05, z1=1.25, tono=(0.85, 0.75, 0.65)),
     [R(pal_(It, 0, 15, 18), W / 2, 500, 96, lineas=(1,))], ent=("fundido", 0.6))


def _equis(lz, t):
    t0 = w_(It, 1, 2) + 0.1
    for k, (a, b) in enumerate((((700, 250), (1220, 760)), ((1220, 250), (700, 760)))):
        X.trazo_recto(lz, a, b, 0.0, e_out(prog(t, t0 + 0.25 * k, t0 + 0.25 * k + 0.5)), 26)


shot(84.98, F_borroso("f190", 0.28), [R(pal_(It, 1, 0, 3), W / 2, 900, 88)], [HERO(190, 960, 470, -3, t_in=85.0, desde=(0, 700)), _equis], ent=("fundido", 0.5))
shot(86.22, F_clip("humo", inicio=8, z0=1.05, z1=1.22, tono=(0.85, 0.85, 0.9)),
     [S([("1959", 86.4)], 700, 470, 230)],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Anagrama", "1959", "Philological Quarterly"), D.poner(420, 420, 1400, 500, 1.0, -10), 0.92 * smooth(prog(t, w_(It, 1, 7), w_(It, 1, 7) + 0.2)))], ent=("fuga", 0.7))
shot(88.30, F_foto("folios_hd/f187", z0=1.6, z1=1.95, c0=(0.45, 0.4), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.6, 0.58, 0.54)),
     [R(pal_(It, 1, 10, 13), W / 2, 540, 96, lineas=(1,))], ent=("fundido", 0.6))
shot(90.20, F_clip("humo", inicio=1, z0=1.05, z1=1.25, tono=(0.75, 0.8, 0.9)),
     [R(pal_(It, 2, 2, 5), W / 2, 540, 96, lineas=(1,))], ent=("fundido", 0.6), grado=dict(vineta=0.85))


def _trazos3(lz, t):
    t0 = w_(It, 2, 9) - 0.2
    for k, y in enumerate((300, 430, 560, 690)):
        u1 = e_out(prog(t, t0 + 0.22 * k, t0 + 0.22 * k + 0.7))
        X.trazo_recto(lz, (250, y), (1670, y + 4), 0.0, u1, 16, op=0.85)


shot(91.72, F_foto("folios_hd/f190", z0=1.9, z1=2.3, c0=(0.25, 0.3), c1=(0.7, 0.6), par=(0, 0), lado=3800, tono=(0.55, 0.53, 0.5)),
     [R(pal_(It, 2, 5, 12), W / 2, 880, 84, lineas=(4,))], [_trazos3], ent=("fundido", 0.6), grado=dict(vineta=0.85))
shot(94.05, F_foto("folios_hd/f187", z0=1.6, z1=1.9, c0=(0.5, 0.4), c1=(0.5, 0.5), par=(0, 0), lado=3800, tono=(0.30, 0.29, 0.27)),
     [R(pal_(It, 3, 3, 12), W / 2, 950, 62, lineas=(5,))],
     [lambda lz, t: D.grafica_zipf(lz, ZIPF, t, 94.15, W / 2, 450, 1240, 640, dur=3.6),
      lambda lz, t: X.elipse_luz(lz, 900, 520, 230, 150, prog(t, w_(It, 3, 10), w_(It, 3, 11) + 0.5), grosor=5)], ent=("fuga", 0.7))
