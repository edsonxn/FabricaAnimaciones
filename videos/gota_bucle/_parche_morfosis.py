# -*- coding: utf-8 -*-
s = open('escenas.py', encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)


# ---- registro de transformaciones
rep('''def construir_actores():
    R = []''', '''MORFS = []


def M(sa, sb, t0, dur=0.55, sfx=True):
    """Transformación del actor `sa` en el actor `sb` (técnica de la referencia): sa se corta al empezar y sb aparece al terminar;
    entre medias `Mundo.morf` dibuja la metamorfosis (contorno que se deforma, crayón que se disuelve y vuelve a aparecer)."""
    sa["t_out"], sa["sale"], sa["d_out"] = t0, "cortar", 0.01
    sb["t_in"], sb["entra"], sb["d_in"] = t0 + dur, "fija", 0.01
    MORFS.append(dict(a=sa, b=sb, t0=t0, dur=dur))
    if sfx:
        sb["snd"] += [(t0, "morph", 0.8, {}), (t0 + 0.05, "garabato", 0.5, {"dur": 0.45}), (t0 + dur, "pop", 0.45, {"tono": 1.2})]
    return sb


def construir_actores():
    MORFS.clear()
    R = []''')

# ---- planeta -> nube
rep('''    A(R, O.planeta(), (540, 1060, 1.35), t_planeta, 0.4, "pop", t_out=t_out_pl, d_out=0.35, sem=43,
      sfx=[("pop", 0, 0.9), ("golpe_suave", 0.18, 0.7)], sfx_out=[("puf", 0, 0.5)])''',
    '''    sp_planeta = A(R, O.planeta(), (540, 1060, 1.35), t_planeta, 0.4, "pop", t_out=t_out_pl, d_out=0.35, sem=43,
                   sfx=[("pop", 0, 0.9), ("golpe_suave", 0.18, 0.7)])''')
rep('''    A(R, O.nube_din, C0_NUBE, t_hoy - 0.35, 0.5, "lt", t_out=INI("hielo") - 0.05, d_out=0.5, sale="sube_fuera", sem=2,
      sfx=[("garabato", 0, 0.6, {"dur": 0.5}), ("pop", 0.45, 0.6, {"tono": 0.9})], sfx_out=[("whoosh", 0, 0.5, {"dur": 0.5})])''',
    '''    sp_nube2 = A(R, O.nube_din, C0_NUBE, t_hoy - 0.35, 0.5, "lt", t_out=INI("hielo") - 0.05, d_out=0.5, sale="sube_fuera", sem=2,
                 sfx_out=[("whoosh", 0, 0.5, {"dur": 0.5})])
    M(sp_planeta, sp_nube2, INI("montana") - 0.7, 0.5)''')

# ---- montaña -> hielo
rep('''    A(R, O.montana(), (540, 1440, 0.95), t_cae + 0.45, 0.7, "sube", dy=700, t_out=INI("hielo") + 0.15, d_out=0.4, sale="borrar",
      sem=3, sfx=[("crece", 0, 0.7, {"dur": 0.8})], sfx_out=[("borrar", 0, 0.5, {"dur": 0.4})])''',
    '''    sp_mont = A(R, O.montana(), (540, 1440, 0.95), t_cae + 0.45, 0.7, "sube", dy=700, t_out=INI("hielo") + 0.15, d_out=0.4,
                sale="borrar", sem=3, sfx=[("crece", 0, 0.7, {"dur": 0.8})])''')
rep('''    A(R, O.bloque_hielo(), (lambda t: (540, 905, 1.5 * (1 + 0.07 * math.sin(math.pi * prog(t, t_glaciar, t_glaciar + 0.5))))),
      t_congela + 0.02, 0.4, "lt", t_out=t_derrite + 0.05, d_out=1.0, sale="encoger", sem=4,
      sfx=[("hielo", 0, 0.9), ("tick", 0.4, 0.5)])''',
    '''    sp_hielo = A(R, O.bloque_hielo(), (lambda t: (540, 905, 1.5 * (1 + 0.07 * math.sin(math.pi * prog(t, t_glaciar, t_glaciar + 0.5))))),
                 t_congela + 0.02, 0.4, "lt", t_out=t_derrite + 0.05, d_out=1.0, sale="encoger", sem=4,
                 sfx=[("hielo", 0.5, 0.9), ("tick", 0.9, 0.5)])
    M(sp_mont, sp_hielo, INI("hielo") + 0.1, 0.55)''')

# ---- hielo -> charco
rep('''    A(R, O.charco(), (lambda t: (540, 1225, 0.4 + 1.1 * smooth(prog(t, t_derrite + 0.3, t_derrite + 1.4)))), t_derrite + 0.3, 0.3,
      "pop", t_out=t_baja + 0.6, d_out=0.4, sem=9, sfx=[("plop", 0, 0.7)])''',
    '''    sp_charco = A(R, O.charco(), (lambda t: (540, 1225, 0.4 + 1.1 * smooth(prog(t, t_derrite + 0.3, t_derrite + 1.4)))),
                  t_derrite + 0.3, 0.3, "pop", t_out=t_baja + 0.6, d_out=0.4, sem=9, sfx=[("plop", 0.6, 0.7)])
    M(sp_hielo, sp_charco, t_derrite + 0.02, 0.6)''')

# ---- vaso -> aliento
rep('''    A(R, O.vaso(), vaso_tf, t_vaso_p - 0.25, 0.3, "pop", t_out=t_bebe + 0.6, d_out=0.3, sem=13,
      sfx=[("clink", 0.05, 0.8, {"tono": 1.2}), ("pop", 0.1, 0.5)])''',
    '''    sp_vaso = A(R, O.vaso(), vaso_tf, t_vaso_p - 0.25, 0.3, "pop", t_out=t_bebe + 0.6, d_out=0.3, sem=13,
                sfx=[("clink", 0.05, 0.8, {"tono": 1.2}), ("pop", 0.1, 0.5)])''')
rep('''    A(R, O.soplo(), (MOUTH[0] + 200, MOUTH[1] - 195, 0.9), t_devuelves, 0.4, "lt", t_out=t_sigue + 0.1, d_out=0.3, sem=15,
      sfx=[("puf", 0.05, 0.9), ("garabato", 0, 0.4, {"dur": 0.3})])''',
    '''    sp_soplo = A(R, O.soplo(), (MOUTH[0] + 200, MOUTH[1] - 195, 0.9), t_devuelves, 0.4, "lt", t_out=t_sigue + 0.1, d_out=0.3,
                 sem=15, sfx=[("puf", 0.5, 0.9)])
    M(sp_vaso, sp_soplo, t_devuelves - 0.08, 0.55)''')

# ---- sol <-> luna (los años pasan): cada cambio es una transformación
a = s.index("    # sol y luna que se alternan (pasan los años)")
b = s.index("    # ---- sol grande y vapor")
s = s[:a] + '''    # sol <-> luna: pasan los años (cada cambio es una transformación rápida)
    POS_SL = (880, 560, 1.0)
    ts0 = t_tres + 0.7
    forma = [O.sol(46), O.luna(), O.sol(46), O.luna()]
    prev = A(R, forma[0], POS_SL, ts0, 0.22, "pop", sem=50, sfx=[("tick", 0, 0.5)])
    for i in range(1, 4):
        nxt = A(R, forma[i], POS_SL, ts0 + 9, 0.1, "fija", sem=50 + i)
        M(prev, nxt, ts0 + 0.3 + 0.5 * (i - 1), 0.24, sfx=False)
        nxt["snd"] += [(ts0 + 0.3 + 0.5 * (i - 1), "morph", 0.45, {}), (ts0 + 0.54 + 0.5 * (i - 1), "tick", 0.5, {"tono": 1.0 + 0.15 * i})]
        prev = nxt
    prev["t_out"], prev["d_out"], prev["sale"] = ts0 + 0.3 + 0.5 * 2 + 0.24 + 0.45, 0.3, "encoger"
''' + s[b:]

# ---- actor(): salida instantánea
rep('''            uo = prog(t, a["t_out"], a["t_out"] + a["d_out"])
            if uo >= 1:
                return
            m = a["sale"]''', '''            if a["sale"] == "cortar":
                return
            uo = prog(t, a["t_out"], a["t_out"] + a["d_out"])
            if uo >= 1:
                return
            m = a["sale"]''')

# ---- dibujo de las transformaciones
rep('''        self.dinamicos(t, te)
        self.dibujar_gota(t, te)''', '''        for m in MORFS:
            if m["t0"] <= t < m["t0"] + m["dur"]:
                self.morf(m, t)
        self.dinamicos(t, te)
        self.dibujar_gota(t, te)''')
rep('''    def gota_dib(self, x, y, s, rot, ojos, boca, sq=0.0):''', '''    def morf(self, m, t):
        """Cuadro de la transformación m['a'] -> m['b'] (ver `M`)."""
        def estado(sp):
            pos = sp["pos"](t) if callable(sp["pos"]) else sp["pos"]
            return dict(x=pos[0], y=pos[1], s=pos[2], rot=pos[3] if len(pos) > 3 else sp["rot"], flip=sp["flip"])

        def dib(sp):
            return sp["d"](self.te) if callable(sp["d"]) else sp["d"]
        k = (t - m["t0"]) / m["dur"]
        B.morfosis(self.h, dib(m["a"]), estado(m["a"]), dib(m["b"]), estado(m["b"]), k, self.fs, m["b"]["sem"], tv=self.te,
                   vida=m["b"]["vida"])

    def gota_dib(self, x, y, s, rot, ojos, boca, sq=0.0):''')
open('escenas.py', 'w', encoding='utf-8').write(s)
print("ok")
