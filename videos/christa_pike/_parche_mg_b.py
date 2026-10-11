# -*- coding: utf-8 -*-
"""Parche: tomas_b.py usa las escenas dibujadas (mg_esc*.py) en lugar de metraje de stock/noticias reciclado."""


def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:100]
    return s.replace(old, new, 1)


b = open('tomas_b.py', encoding='utf-8').read()

b = rep(b, "from tomas_a import A, NEG, SEP, C_W, C_F, C_N, C_5, C_A\n",
        "from tomas_a import A, NEG, SEP, C_W, C_F, C_N, C_5, C_A\nfrom mg_esc import F_mg, OV  # noqa: F401\nfrom mg_esc2 import OV_calendario  # noqa: F401\nfrom mg_obj import cerebro, check  # noqa: F401\nfrom mg import pr as _pr  # noqa: F401\n")

# ---- DEBATE
b = rep(b, '''shot(INI(Dd, 0), F_clip("stock/balanza_0", ini=1.0, z0=1.0, z1=1.18, c0=(0.55, 0.55), c1=(0.5, 0.5), tono=(0.78, 0.78, 0.82)),
     [], [], ent=("tinta", 0.7), grado=dict(vineta=0.8))''', '''shot(INI(Dd, 0), F_mg("d_balanza"), [], [], ent=("tinta", 0.7))''')
b = rep(b, '''     [FRAME_CLIP("wbir_asesinato_1995", 560, 520, 700, 26.2, INI(Dd, 1) + 0.15, rot=-2, x_cont=(0.125, 0.875), fin=27.9),''',
        '''     [OV(lambda p, t: cerebro(p, 1700, 800, 110, grieta=_pr(t, A(Dd, 1, "cerebral"), A(Dd, 1, "congenito", 0.8)), t=t) if t > A(Dd, 1, "enfermedades") else None),
      FRAME_CLIP("wbir_asesinato_1995", 560, 520, 700, 26.2, INI(Dd, 1) + 0.15, rot=-2, x_cont=(0.125, 0.875), fin=27.9),''')

# ---- CAMINO
b = rep(b, '''     [N("30 · 09 · 2025", 560, 230, 120, A(Ca, 0, "treinta")), N("30 · 09 · 2026", 1360, 230, 120, A(Ca, 0, "ano"))],
     [TAG("Corte Suprema de Tennessee", 960, 900, A(Ca, 0, "corte"), 46), CRED(''', '''     [],
     [OV_calendario(A(Ca, 0, "fijo", 0.0), FIN(Ca, 0) - 0.4, 420, 560), TAG("Corte Suprema de Tennessee", 1300, 900, A(Ca, 0, "corte"), 46), CRED(''')
i0 = b.index('shot(INI(Ca, 1), F_clip("newschannel5_hospital"')
i1 = b.index("def _cartas_ca3(lz, t):")
b = b[:i0] + '''shot(INI(Ca, 1), F_mg("ca_intentos"),
     [S([("Mayo", A(Ca, 1, "mayo")), ("De", A(Ca, 1, "mayo", 0.3)), ("2026", A(Ca, 1, "mayo", 0.6))], 560, 230, 120),
      R(pk(Ca, 1, "mas", "hora"), W / 2, 960, 74)], [], ent=("fundido", 0.6))
shot(INI(Ca, 2), F_mg("ca_sangre"), [], [], ent=("fundido", 0.6))


''' + b[i1:]

# ---- NOCHE (todo dibujado)
i0 = b.index('shot(INI(N_, 0), F_clip("newschannel5_hospital"')
i1 = b.index("# ============================================================== DESPUES")
b = b[:i0] + '''shot(INI(N_, 0), F_mg("n_prision"),
     [], [RELOJ("6:41 p. m.", 1500, 300, 210, A(N_, 0, "seis")),
          TAG("Riverbend Maximum Security Institution", 700, 940, A(N_, 0, "prision"), 44)], ent=("tinta", 0.8), grado=G_)
shot(INI(N_, 1), F_mg("n_persianas"), [], [RELOJ("7:26 p. m.", 1620, 330, 190, A(N_, 1, "siete"))], ent=("fundido", 0.5), grado=G_)
snd(A(N_, 1, "persianas", -0.2), "persianas", 0.6)
shot(INI(N_, 2), F_mg("n_cancion"),
     [R([("«I'm", A(N_, 2, "amor", -0.6)), ("at", A(N_, 2, "amor", -0.45)), ("peace", A(N_, 2, "paz")), ("and", A(N_, 2, "paz", 0.3)),
         ("I'm", A(N_, 2, "paz", 0.45)), ("ready", A(N_, 2, "paz", 0.6)), ("to", A(N_, 2, "paz", 0.75)), ("go»", A(N_, 2, "paz", 0.9))], 600, 220, 66, lineas=(4,))],
     [TAG("Christa Pike · últimas palabras", 1400, 960, A(N_, 2, "amor", -0.6), 44)], ent=("fundido", 0.7), grado=G_)
shot(INI(N_, 3), F_mg("n_vena"),
     [R([("«The", A(N_, 3, "vena", -0.4)), ("vein", A(N_, 3, "vena")), ("in", A(N_, 3, "vena", 0.2)), ("my", A(N_, 3, "brazo", -0.3)), ("arm", A(N_, 3, "brazo")),
         ("feels", A(N_, 3, "brazo", 0.3)), ("like", A(N_, 3, "estaba", 0.0)), ("it's", A(N_, 3, "estaba", 0.3)), ("about", A(N_, 3, "punto", 0.0)),
         ("to", A(N_, 3, "punto", 0.3)), ("bust.»", A(N_, 3, "reventar"))], W / 2, 220, 62, lineas=(5,))],
     [RELOJ("7:34 p. m.", 1560, 960, 160, A(N_, 3, "treinta")), TAG("Christa Pike", 480, 700, A(N_, 3, "se", 0.0), 44)],
     ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 4), F_ventana_piedra(A(N_, 4, "piedra", 0.05)),
     [], [RELOJ("7:41 p. m.", 470, 330, 190, A(N_, 4, "siete")), CRED("Recreación gráfica del detalle que describieron los testigos · no es una imagen real", INI(N_, 4) + 0.5, A(N_, 4, "pentobarbital") - 0.6)],
     ent=("tinta", 0.7), grado=G_)
shot(A(N_, 4, "pentobarbital", -0.8), F_mg("n_jeringa"), [], [], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 5), F_mg("n_reabre"), [], [RELOJ("7:46 p. m.", 1620, 330, 190, INI(N_, 5))], ent=("fundido", 0.4), grado=G_)
snd(A(N_, 5, "cerraron"), "persianas", 0.55)
snd(A(N_, 5, "abrieron", 0.1), "persianas", 0.5)
shot(INI(N_, 6), F_mg("n_cuenta"),
     [R(pk(N_, 6, "segunda", "dosis"), 1380, 960, 70)],
     [TEMPORIZADOR(A(N_, 6, "cinco", -0.1), A(N_, 6, "viva", 0.2), 560, 560, 130)], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 7), F_mg("n_ronca"), [], [RELOJ("8:05 p. m.", 1500, 300, 190, INI(N_, 7))], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 8), F_mg("n_protocolo"), [], [], ent=("fundido", 0.6), grado=G_)
shot(INI(N_, 9), F_mg("n_ambulancia"), [], [], ent=("fundido", 0.5), grado=G_)

''' + b[i1:]

# ---- DESPUES
i0 = b.index('shot(INI(De, 0), F_clip("stock/hospital_1"')
i1 = b.index("shot(INI(De, 2), F_vena(")
b = b[:i0] + '''shot(INI(De, 0), F_mg("de_hospital"),
     [R(pk(De, 0, "estado", "critico"), W / 2, 960, 80)], [TAG("1 de octubre", 1560, 230, INI(De, 0) + 0.3, 48)], ent=("tinta", 0.7))
shot(INI(De, 1), F_mg("de_monitor"),
     [R([("Inconsciente", A(De, 1, "inconsciente"))], 560, 190, 80), R([("Respirador", A(De, 1, "respirador"))], 1400, 960, 80)],
     [TAG("2 de octubre · escrito judicial", 1470, 130, INI(De, 1) + 0.3, 42)], ent=("fundido", 0.6))
''' + b[i1:]
i0 = b.index('shot(INI(De, 5), F_clip("stock/documento_1"')
i1 = b.index('shot(INI(De, 7), F_clip("abc_ventilador"')
b = b[:i0] + '''shot(INI(De, 5), F_mg("de_protocolo"),
     [R([("«Actuó", A(De, 5, "actuo")), ("conforme", A(De, 5, "conforme")), ("al", A(De, 5, "al")), ("protocolo»", A(De, 5, "protocolo"))], 1300, 220, 66, lineas=(2,))],
     [TAG("Frank Strada", 1460, 900, A(De, 5, "actuo"), 46)], ent=("fundido", 0.5))
shot(INI(De, 6), F_mg("de_sistema"),
     [R([("«Una", A(De, 6, "falla")), ("falla", A(De, 6, "falla")), ("sistémica»", A(De, 6, "sistemica"))], W / 2, 140, 80)],
     [TAG("Abogados de Christa Pike", 1500, 960, A(De, 6, "falla"), 46)], ent=("fundido", 0.5))
''' + b[i1:]

# ---- HISTORIAL
i0 = b.index('shot(INI(Hs, 1), F_clip("stock/alambre_1"')
i1 = b.index("# ============================================================== PRECEDENTE")
b = b[:i0] + '''shot(INI(Hs, 1), F_mg("hs_prision"), [], [_lh], ent=("fundido", 0.7), grado=dict(vineta=0.9))
shot(INI(Hs, 3), F_mg("hs_cuatro"),
     [N("4", 1560, 200, 230, A(Hs, 3, "cuatro")), R(pk(Hs, 3, "personas"), 1560, 380, 62)], [_lh], ent=("fundido", 0.6), grado=dict(vineta=0.9))
shot(INI(Hs, 4), F_mg("hs_dos"), [R(pk(Hs, 4, "segunda", "fallida"), W / 2, 130, 78, lineas=(2,))], [], ent=("fundido", 0.6))
shot(INI(Hs, 5), F_mg("hs_vial"),
     [S([("Pentobarbital", A(Hs, 5, "pentobarbital"))], W / 2, 150, 118)],
     [TAG("Frank Strada · desde enero de 2023", 1300, 960, A(Hs, 5, "frank"), 46)], ent=("fundido", 0.6))

''' + b[i1:]

# ---- PRECEDENTE
b = rep(b, '''shot(INI(P, 0), F_clip("stock/documento_2", ini=3.0, z0=1.0, z1=1.15, tono=(0.62, 0.62, 0.66), sat=0.7),
     [R(pk(P, 0, "no", "igual"), W / 2, 860, 84, lineas=(3,))], [], ent=("tinta", 0.7), grado=dict(vineta=0.85))''', '''shot(INI(P, 0), F_mg("pr_busqueda"), [], [], ent=("tinta", 0.7))''')
b = rep(b, '''shot(INI(P, 1), F_borroso("willie1", 0.30),
     [N("1946", 1400, 440, 320, A(P, 1, "mil"))],
     [HERO("willie1", 600, 530, -3, alto=820, t_in=INI(P, 1) + 0.1, desde=(-800, 0)), TAG("Luisiana", 1400, 700, A(P, 1, "luisiana"), 54),''', '''shot(INI(P, 1), F_mg("pr_luisiana"),
     [N("1946", 420, 220, 260, A(P, 1, "mil"))],
     [lambda lz, t: carta(lz, pola("willie1", 520, 1.22, (0.5, 0.35), "Willie Francis"), I3, t, A(P, 1, "luisiana", 0.4), 1500, 560, 4, desde=(500, 0), dur=0.6),''')
b = rep(b, '''shot(INI(P, 5), F_clip("stock/mazo_2", ini=1.0, z0=1.0, z1=1.15, tono=(1.5, 1.45, 1.4)),
     [R([("Impugnarlo", A(P, 5, "impugnarlo"))], W / 2, 870, 100)], [], ent=("fundido", 0.5), grado=dict(vineta=0.85))''', '''shot(INI(P, 5), F_mg("pr_abogados"), [R([("Impugnarlo", A(P, 5, "impugnarlo"))], W / 2, 980, 90)], [], ent=("fundido", 0.5))''')

# ---- CIERRE
i0 = b.index('shot(INI(Ci, 0), F_clip("stock/ciudad_noche_0"')
i1 = b.index("_fin_voz = FIN(Ci, 3)")
b = b[:i0] + '''shot(INI(Ci, 0), F_mg("ci_ciudad"), [N("3 · 10 · 2026", 1300, 230, 170, A(Ci, 0, "tres"))], [], ent=("tinta", 0.8))
shot(INI(Ci, 1), F_mg("ci_sala"),
     [Q([[("Qué", A(Ci, 1, "que")), ("Falló", A(Ci, 1, "fallo"))], [("Esa", A(Ci, 1, "esa")), ("Noche", A(Ci, 1, "noche"))]], A(Ci, 1, "que") - 0.2, 1600, 520, 96)],
     [], ent=("fundido", 0.6))
shot(INI(Ci, 2), F_mg("ci_discuten"), [], [], ent=("fundido", 0.8))
''' + b[i1:]
b = rep(b, 'shot(INI(Ci, 3), F_clip("stock/vela_3", ini=1.0, z0=1.4, z1=1.4, c0=(0.40, 0.5), c1=(0.40, 0.5), tono=(0.9, 0.85, 0.8)),', 'shot(INI(Ci, 3), F_mg("ci_vela"),')
b = rep(b, '''                "Video de apoyo: Pexels · Música: Lyria",''', '''                "Animaciones y gráficos: producción propia · Música: Lyria",''')
open('tomas_b.py', 'w', encoding='utf-8').write(b)
print('B ok')
