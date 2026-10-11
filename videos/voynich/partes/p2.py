

# ---------------------------------------------------------------- CONTENIDO (32.5 - 50)
C = "contenido"


def HERO(nombre, x=960, y=500, rot=0.0, alto=880, t_in=0.0, ry=(-12, -3), desde=(0, 0), dur=0.5):
    """Folio grande con cámara propia (para 'héroes' de página)."""
    def f(lz, t):
        sp = folio(nombre, alto)
        u = e_out(prog(t, t_in, t_in + dur))
        cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.10, W / 2, H / 2 + 12, 0.0), 2.4, mano=0.9)(t - t_in)
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(x + desde[0], x, u), lerp(y + desde[1], y, u), lerp(0.88, 1.0, u), lerp(rot + 6, rot, u), lerp(ry[0], ry[1], u)), smooth(prog(t, t_in, t_in + 0.15)))
    return f


shot(32.55, F_borroso("f004", 0.30), [], [HERO(4, 960, 500, -4, t_in=32.6, desde=(-900, 0))], ent=("tinta", 0.5))
shot(33.05, F_borroso("f007", 0.30), [], [HERO(7, 960, 500, 3, t_in=33.07, desde=(900, 0))], ent=("corte", 0.001))
shot(33.48, F_borroso("f024", 0.30), [TXT([("plantas", w_(C, 0, 2))], 960, 900, 170, fnt="impact", clave=[0])],
     [HERO(24, 960, 500, -2, t_in=33.5, desde=(0, 700))], ent=("corte", 0.001))
shot(34.00, F_clip("microscopio2", z0=1.05, z1=1.3, c0=(0.6, 0.5), c1=(0.7, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [TXT([("ningún", w_(C, 0, 4)), ("botánico", w_(C, 0, 5))], 960, 850, 150, lineas=(1,), clave=[1])], ent=("aberracion", 0.28))
shot(35.05, F_borroso("f110", 0.30),
     [TXT([("identificar", w_(C, 0, 8))], 960, 930, 150, clave=[0])],
     [HERO(110, 960, 470, 2, t_in=35.07, desde=(0, -600)),
      lambda lz, t: D.estampa(lz, "SIN IDENTIFICAR", 1330, 620, t, w_(C, 0, 10) - 0.05, 90, rot=-8)], ent=("glitch", 0.25))
shot(37.85, F_borroso("f125", 0.30),
     [TXT([("estrellas", w_(C, 1, 2))], 960, 930, 160, fnt="impact", clave=[0])],
     [HERO(125, 960, 470, -6, t_in=37.87, alto=880), lambda lz, t: X.elipse_luz(lz, 960, 470, 300, 300, prog(t, 38.4, 39.1), grosor=6)], ent=("tinta", 0.45))
shot(39.15, F_borroso("f141", 0.30),
     [TXT([("mujeres", w_(C, 1, 3)), ("bañándose", w_(C, 1, 4))], 960, 930, 120, lineas=(), clave=[1])],
     [HERO(141, 960, 470, 4, t_in=39.17, ry=(12, 4), desde=(900, 0))], ent=("aberracion", 0.28))
shot(40.50, F_foto("f136", z0=1.6, z1=2.0, c0=(0.5, 0.75), c1=(0.5, 0.3), par=(0, 0), lado=2600, tono=(0.85, 0.85, 0.8)),
     [TXT([("tuberías", w_(C, 1, 6)), ("extrañas", w_(C, 1, 7))], 960, 930, 130, clave=[0, 1])], ent=("corte", 0.001))

PAGS = (187, 190, 176, 175, 161, 153, 148, 144)


def _montaje(lz, t):
    k = int((t - 41.45) / 0.21) % len(PAGS)
    sp = folio(PAGS[k], 900)
    Mm = D.poner(sp.w, sp.h, 960 + 40 * math.sin(k * 2.1), 480, 1.0 + 0.05 * ((t - 41.45) % 0.21) / 0.21, (k % 5 - 2) * 2.5, (k % 3 - 1) * 8)
    D.pegar(lz, sp, Mm, 1.0)


shot(41.45, F_borroso("f190", 0.28), [TXT(pal_(C, 1, 9, 12), 960, 940, 120, clave=[0, 2])], [_montaje], ent=("zoom", 0.28))
shot(43.30, F_foto("folios_hd/f187", z0=1.7, z1=2.2, c0=(0.3, 0.3), c1=(0.6, 0.55), par=(0, 0), lado=3800, tono=(0.72, 0.7, 0.66)),
     [TXT([("alfabeto", w_(C, 1, 14)), ("desconocido", w_(C, 1, 15))], 960, 880, 140, lineas=(1,), clave=[1])],
     [lambda lz, t: X.resaltador(lz, 300, 300, 1000, 365, prog(t, 43.4, 44.1)), lambda lz, t: X.resaltador(lz, 700, 560, 1500, 625, prog(t, 43.9, 44.7), semilla=3)], ent=("destello", 0.3))
shot(45.40, F_foto("escriba", z0=1.02, z1=1.22, c0=(0.5, 0.5), c1=(0.56, 0.45), par=(60, 12), tono=(0.72, 0.66, 0.58)),
     [TXT([("Nadie", w_(C, 2, 0)), ("sabe", w_(C, 2, 1))], 700, 200, 96, sal=w_(C, 2, 2) - 0.05), NUM("¿Quién?", 1300, 320, 230, w_(C, 2, 2) - 0.05, color=AM, fnt="impact")], ent=("tinta", 0.5), grado=dict(fuerza_vineta=0.75))
shot(47.20, F_clip("escribir", inicio=2, z0=1.05, z1=1.3, c0=(0.55, 0.5), c1=(0.7, 0.5), tono=(0.9, 0.8, 0.7)),
     [NUM("¿Por qué?", 960, 300, 240, w_(C, 2, 6) - 0.05, color=BL, fnt="impact")], ent=("aberracion", 0.28))

# ---------------------------------------------------------------- FECHA (50 - 67.5)
Fh = "fecha"
shot(50.05, F_clip("reloj_oscuro", inicio=1, z0=1.05, z1=1.3, tono=(0.9, 0.8, 0.7)),
     [NUM("2009", 960, 480, 420, w_(Fh, 0, 1) - 0.05, color=BL, fnt="pop_bi")], ent=("tinta", 0.55))
shot(51.75, F_clip("microscopio", z0=1.05, z1=1.25, c0=(0.55, 0.5), c1=(0.6, 0.5), tono=(0.62, 0.52, 0.42), sat=0.35),
     [TXT([("Arizona", w_(Fh, 0, 7))], 960, 880, 170, fnt="impact", clave=[0])],
     [lambda lz, t: D.tag_nombre(lz, "Universidad de Arizona", 560, 250, t, w_(Fh, 0, 5), 56)], ent=("aberracion", 0.28))
shot(53.05, F_foto("folios_hd/f001", z0=1.5, z1=2.0, c0=(0.4, 0.3), c1=(0.55, 0.55), par=(0, 0), lado=3800, tono=(0.7, 0.65, 0.55)),
     [TXT([("pergamino", w_(Fh, 0, 10))], 960, 880, 150, fnt="impact", clave=[0])], ent=("corte", 0.001))


def _muestras(lz, t):
    for k, (nom, ley) in enumerate((("f017", "folio 8"), ("f051", "folio 26"), ("f093", "folio 47"), ("f123", "folio 68"))):
        carta(lz, pola(nom, 400, 1.25, (0.5, 0.45), ley), I3, t, 54.22 + 0.22 * k, 330 + k * 420, 470 + (k % 2) * 60, (-4, 3, -2, 5)[k], desde=(0, -700), dur=0.4, fase=k)
        snd(54.22 + 0.22 * k, "obturador", 0.4)


shot(54.20, F_pozo(0.5, 0.5, 0.9, (0.20, 0.16, 0.10)),
     [TXT([("carbono", w_(Fh, 0, 12)), ("14", w_(Fh, 0, 13))], 960, 930, 130, clave=[0, 1])], [_muestras], ent=("desenfoque", 0.3))
shot(55.95, F_clip("humo", inicio=2, z0=1.05, z1=1.25, tono=(0.9, 0.85, 0.85)),
     [TXT([("el", w_(Fh, 1, 0)), ("resultado", w_(Fh, 1, 1))], 960, 540, 160, clave=[1])], ent=("tinta", 0.5))
shot(57.25, F_clip("pagina_cerca", inicio=5, z0=1.05, z1=1.2, tono=(0.30, 0.28, 0.26)),
     [NUM("1404", 640, 250, 210, w_(Fh, 1, 5) - 0.05, color=AM), NUM("1438", 1280, 250, 210, w_(Fh, 1, 11) - 0.05, color=AM)],
     [lambda lz, t: D.linea_tiempo(lz, t, 57.3, W / 2, 620, 1300, 1500, 1404, 1438, dur=max(0.8, w_(Fh, 1, 11) - 58.3), marcas=[(1455, "Biblia de Gutenberg")], etiqueta="Fecha del pergamino · carbono 14")], ent=("glitch", 0.25))
shot(61.45, F_foto("folios_hd/f001", z0=1.4, z1=1.8, c0=(0.6, 0.6), c1=(0.4, 0.3), par=(0, 0), lado=3800, tono=(0.7, 0.65, 0.55)),
     [TXT([("pergamino", w_(Fh, 2, 1)), ("medieval", w_(Fh, 2, 3))], 960, 480, 170, lineas=(1,), clave=[1])], ent=("destello", 0.3))
shot(63.75, F_foto("f008", z0=1.35, z1=1.6, c0=(0.5, 0.35), c1=(0.5, 0.5), par=(0, 0), lado=2600, tono=(0.45, 0.43, 0.4)),
     [TXT(pal_(Fh, 2, 4, 9), 960, 470, 130, lineas=(3,), clave=[3, 4])],
     [lambda lz, t: D.marcador_mano(lz, "tachado", 960, 530, 1080, 10, prog(t, w_(Fh, 2, 8) + 0.05, w_(Fh, 2, 8) + 0.4), grosor=14)], ent=("tinta", 0.45))
