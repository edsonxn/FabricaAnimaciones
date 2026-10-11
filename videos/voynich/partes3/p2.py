

# ---------------------------------------------------------------- CONTENIDO (32.5 - 50)
C = "contenido"
shot(32.55, F_borroso("f004", 0.30), [],
     [HERO(4, 620, 500, -4, t_in=32.6, desde=(-900, 0), alto=850), HERO(24, 1300, 500, 3, t_in=33.55, desde=(900, 0), alto=850)], ent=("tinta", 0.7))
shot(34.00, F_clip("microscopio2", z0=1.05, z1=1.25, c0=(0.6, 0.5), c1=(0.7, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [R(pal_(C, 0, 4, 11), W / 2, 780, 84, lineas=(3,))], ent=("fundido", 0.5))
shot(35.45, F_borroso("f110", 0.30), [R(pal_(C, 0, 4, 11), W / 2, 780, 84, lineas=(3,), sal=37.6)],
     [HERO(110, 640, 470, 2, t_in=35.5, desde=(0, -600), alto=860),
      lambda lz, t: D.estampa(lz, "SIN IDENTIFICAR", 1330, 500, t, w_(C, 0, 10) - 0.05, 90, rot=-8)], ent=("fundido", 0.4))
shot(37.85, F_borroso("f125", 0.30), [R(pal_(C, 1, 0, 3), W / 2, 960, 84, sal=39.1)],
     [HERO(125, 960, 470, -5, t_in=37.9, alto=860), lambda lz, t: X.elipse_luz(lz, 960, 470, 300, 300, prog(t, 38.4, 39.1), grosor=5)], ent=("fuga", 0.7))
shot(39.15, F_borroso("f141", 0.30), [R(pal_(C, 1, 3, 8), W / 2, 930, 78, lineas=(3,))],
     [HERO(141, 960, 460, 4, t_in=39.2, ry=(12, 4), desde=(900, 0), alto=850)], ent=("fundido", 0.5))

PAGS = (187, 190, 176, 175, 161, 153, 148, 144)


def _montaje(lz, t):
    k = int((t - 41.45) / 0.30) % len(PAGS)
    sp = folio(PAGS[k], 900)
    Mm = D.poner(sp.w, sp.h, 960 + 30 * math.sin(k * 2.1), 480, 1.0 + 0.05 * ((t - 41.45) % 0.30) / 0.30, (k % 5 - 2) * 2.0, (k % 3 - 1) * 6)
    D.pegar(lz, sp, Mm, 1.0)


shot(41.45, F_borroso("f190", 0.28), [], [_montaje], ent=("zoom", 0.3))


def _trazos2(lz, t):
    tt = t - 43.7
    for k, (y, x0, x1) in enumerate(((330, 260, 1500), (610, 300, 1560))):
        u1 = e_out(prog(tt, 0.45 * k, 0.45 * k + 1.1))
        u0 = e_inout(prog(tt, 1.6 + 0.3 * k, 2.4 + 0.3 * k))
        X.trazo_recto(lz, (x0, y), (x1, y + 4), u0, u1, 22)


shot(43.30, F_foto("folios_hd/f187", z0=1.7, z1=2.1, c0=(0.3, 0.3), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.72, 0.7, 0.66)),
     [R(pal_(C, 1, 13, 16), W / 2, 850, 88)], [_trazos2], ent=("fuga", 0.7))
shot(45.40, F_foto("escriba", z0=1.02, z1=1.2, c0=(0.5, 0.5), c1=(0.56, 0.45), par=(60, 12), tono=(0.72, 0.66, 0.58)),
     [Q([[("Nadie", w_(C, 2, 0)), ("sabe", w_(C, 2, 1))], [("quién", w_(C, 2, 2)), ("lo", w_(C, 2, 3)), ("escribió", w_(C, 2, 4))]], w_(C, 2, 2) - 0.1, 1350, 580, 84, sal=47.1)],
     ent=("tinta", 0.6))
shot(47.20, F_clip("escribir", inicio=2, z0=1.05, z1=1.25, c0=(0.55, 0.5), c1=(0.7, 0.5), tono=(0.9, 0.8, 0.7)),
     [Q([[("Ni", w_(C, 2, 5)), ("por", w_(C, 2, 6)), ("qué", w_(C, 2, 7))]], w_(C, 2, 5) - 0.1, 960, 560, 92)], ent=("fundido", 0.5))

# ---------------------------------------------------------------- FECHA (50 - 67.5)
Fh = "fecha"
shot(50.05, F_clip("reloj_oscuro", inicio=1, z0=1.05, z1=1.22, tono=(0.9, 0.8, 0.7)),
     [S([("2009", w_(Fh, 0, 3) - 0.1)], 960, 520, 230)], ent=("tinta", 0.7))
shot(51.75, F_clip("microscopio", z0=1.05, z1=1.2, c0=(0.55, 0.5), c1=(0.6, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [S([("Universidad", w_(Fh, 0, 5)), ("De", w_(Fh, 0, 6)), ("Arizona", w_(Fh, 0, 7))], 960, 860, 96)], ent=("fundido", 0.6))


def _muestras(lz, t):
    for k, (nom, ley) in enumerate((("f017", "folio 8"), ("f051", "folio 26"), ("f093", "folio 47"), ("f123", "folio 68"))):
        carta(lz, pola(nom, 400, 1.25, (0.5, 0.45), ley), I3, t, 54.22 + 0.3 * k, 330 + k * 420, 450 + (k % 2) * 60, (-4, 3, -2, 5)[k], desde=(0, -700), dur=0.5, fase=k)
        snd(54.22 + 0.3 * k, "obturador", 0.35)


shot(54.20, F_pozo(0.5, 0.5, 0.9, (0.20, 0.16, 0.10)),
     [S([("Carbono", w_(Fh, 0, 12)), ("14", w_(Fh, 0, 13))], 960, 920, 104)], [_muestras], ent=("fundido", 0.6))
shot(55.95, F_clip("pagina_cerca", inicio=5, z0=1.05, z1=1.18, tono=(0.30, 0.28, 0.26)),
     [N("1404", 640, 250, 210, w_(Fh, 1, 5) - 0.05), N("1438", 1280, 250, 210, w_(Fh, 1, 11) - 0.05)],
     [lambda lz, t: D.linea_tiempo(lz, t, 57.3, W / 2, 620, 1300, 1500, 1404, 1438, dur=max(0.8, w_(Fh, 1, 11) - 58.3), marcas=[(1455, "Biblia de Gutenberg")], etiqueta="Fecha del pergamino · carbono 14")], ent=("fuga", 0.7))
shot(61.45, F_foto("folios_hd/f001", z0=1.4, z1=1.75, c0=(0.6, 0.6), c1=(0.4, 0.3), par=(0, 0), lado=3800, tono=(0.7, 0.65, 0.55)),
     [R([("pergamino", w_(Fh, 2, 1)), ("medieval", w_(Fh, 2, 3))], W / 2, 500, 100)], ent=("fundido", 0.6))
shot(63.75, F_foto("f008", z0=1.35, z1=1.55, c0=(0.5, 0.35), c1=(0.5, 0.5), par=(0, 0), lado=2600, tono=(0.45, 0.43, 0.4)),
     [R(pal_(Fh, 2, 4, 9), W / 2, 480, 88, lineas=(3,))],
     [lambda lz, t: X.trazo_recto(lz, (420, 560), (1500, 560), 0.0, e_out(prog(t, w_(Fh, 2, 8) + 0.05, w_(Fh, 2, 8) + 0.5)), 16)], ent=("fundido", 0.6))
