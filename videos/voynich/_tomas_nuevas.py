@toma(F2 - PAD, F3 - 0.1, ent=("desenfoque", 0.4), grado=dict(fuerza_vineta=0.7))
def t_fecha_medieval(lz, t):
    tl = t - (F2 - PAD)
    D.foto_parallax(lz, "f001", tl, F3 - F2 + 0.6, 1.5, 2.0, (0.4, 0.35), (0.55, 0.55), par=(0, 0), tono=(0.7, 0.65, 0.55))
    D.dibujar_bloque(lz, bloque([("Pergamino", T("fecha", "pergamino", frase=2)), ("Medieval", f_med)], W / 2, 250, 110), t, "serif", 110)
    D.dibujar_bloque(lz, bloque([("Falsificación", f_falsif), ("Moderna", f_moderna)], W / 2, 900, 100, color=BL), t, "serif", 100)
    D.marcador_mano(lz, "tachado", W / 2, 905, 760, 12, prog(t, f_moderna + 0.35, f_moderna + 0.75), grosor=11)


def _piel(k):
    def mk():
        im = D.cargar(D.ruta_img("f001"), 2000)
        h, w = im.shape[:2]
        rng = np.random.default_rng(40 + k)
        cw, ch = int(w * 0.55), int(h * 0.36)
        x0, y0 = int(rng.integers(0, w - cw)), int(rng.integers(0, h - ch))
        return D.hoja_papel(np.ascontiguousarray(im[y0:y0 + ch, x0:x0 + cw]), 250, sr=12)
    return spr(("piel", k), mk)


@toma(F3 - PAD, D0 - 0.1, ent=("desenfoque", 0.4))
def t_fecha_pieles(lz, t):
    tl = t - (F3 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.48, 0.85, (0.20, 0.16, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.08, W / 2, H / 2 - 6, 0.0), D0 - F3 + 0.4, mano=0.7)(tl)
    n_ = 14
    t_ini = f_menos - 0.1
    paso = max(0.06, (f_ternero - t_ini - 0.2) / n_)
    for k in range(n_):
        col, fila = k % 7, k // 7
        x = 330 + col * 210 + (fila * 100)
        y = 470 + fila * 250
        carta(lz, _piel(k), cam, t, t_ini + k * paso, x, y, ((k * 37) % 9) - 4, desde=(0, -560), dur=0.35, fase=k)
    n = min(n_, max(0, int((t - t_ini) / paso) + 1)) if t >= t_ini else 0
    if n:
        pm, a, m = D.palabra_img(str(n), "abril", 250, tuple(RJ), stroke=0.04, glow=0.6)
        D.mezclar_pm(lz, pm, a, int(W / 2 - pm.shape[1] / 2), int(150 - pm.shape[0] / 2), smooth(prog(t, t_ini, t_ini + 0.2)))
    D.tag_nombre(lz, "Eamon Duffy · historiador", 480, 890, t, f_eamon - 0.05, 40)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("fecha", 3, 6, 11), W / 2 + 200, 985, 76), t, "serif", 76)


# ================================================================== DUEÑOS
@toma(D0 - PAD, D1 - 0.1, ent=("desenfoque", 0.5), grado=dict(polvo=0.5))
def t_duenos_rastro(lz, t):
    tl = t - (D0 - PAD)
    D.foto_parallax(lz, "escriba2", tl, D1 - D0 + 0.6, 1.02, 1.25, (0.5, 0.5), (0.45, 0.42), par=(50, 10),
                    tono=tuple(0.55 * (1 - 0.7 * prog(t, d_rastro, d_pasado + 0.6)) + 0.04 for _ in range(3)))
    D.dibujar_bloque(lz, bloque(kar("duenos", 0, 0, 7), W / 2, 900, 88, lineas=(4,)), t, "serif", 88)


@toma(D1 - PAD, d_sabio - 0.12, ent=("desenfoque", 0.45), grado=dict(calido=0.06))
def t_duenos_praga(lz, t):
    tl = t - (D1 - PAD)
    D.foto_parallax(lz, "praga", tl, d_sabio - D1 + 0.5, 1.04, 1.22, (0.5, 0.5), (0.58, 0.46), par=(70, 10), tono=(0.72, 0.68, 0.62))
    D.numero(lz, "1639", 1470, 210, 240, t, d_1639 - 0.05, color=BL, fnt="sans")
    D.tag_nombre(lz, "Georg Baresch · alquimista", 520, 820, t, d_georg - 0.05, 46)
    D.tag_nombre(lz, "Praga", 340, 720, t, T("duenos", "praga", frase=1) - 0.05, 40, rot=2.5)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 1, 12, 17), W / 2, 985, 76), t, "serif", 76)


@toma(d_sabio - PAD, D2 - 0.1, ent=("latigo", 0.35), grado=dict(calido=0.08))
def t_duenos_kircher(lz, t):
    tl = t - (d_sabio - PAD)
    D.foto_parallax(lz, "kircher", tl, D2 - d_sabio + 0.5, 1.06, 1.28, (0.5, 0.35), (0.5, 0.3), par=(60, 10), tono=(0.85, 0.82, 0.75))
    D.tag_nombre(lz, "Athanasius Kircher", 1450, 900, t, d_kircher - 0.05, 46)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 1, 18, 20), W / 2, 985, 84), t, "serif", 84)


@toma(D2 - PAD, d_quiso - 0.15, ent=("desenfoque", 0.35), grado=dict(calido=0.08))
def t_duenos_respondio(lz, t):
    tl = t - (D2 - PAD)
    D.foto_parallax(lz, "kircher", tl, d_quiso - D2 + 0.5, 1.7, 2.1, (0.5, 0.2), (0.5, 0.17), par=(80, 10), tono=(0.75, 0.72, 0.65))
    D.numero(lz, "¿?", 1450, 480, 420, t, d_respondio - 0.1, color=AM, fnt="serif")
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 2, 3, 6), W / 2, 985, 84), t, "serif", 84)


@toma(d_quiso - PAD, d_emperador - 0.1, ent=("latigo", 0.35))
def t_duenos_libro(lz, t):
    tl = t - (d_quiso - PAD)
    lz[:] = D.pozo_luz(0.5, 0.45, 0.8, (0.26, 0.19, 0.11))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.14, W / 2, H / 2 + 10, 0.0), d_emperador - d_quiso + 0.4, mano=0.8)(tl)
    sp = folio(1, 960)
    u = e_out(prog(t, d_quiso - PAD, d_quiso + 0.8))
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, lerp(1500, 620, u), 540, 1.0, lerp(14, -3, u), lerp(-40, -8, u)), smooth(prog(t, d_quiso - PAD, d_quiso + 0.2)))
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 2, 12, 17), W / 2, 985, 80), t, "serif", 80, salida=d_carta - 0.1)
    D.dibujar_bloque(lz, bloque(kar("duenos", 3, 2, 4), W / 2, 985, 84), t, "serif", 84)


@toma(d_emperador - PAD, I0 - 0.1, ent=("latigo", 0.35), grado=dict(calido=0.07))
def t_duenos_rodolfo(lz, t):
    tl = t - (d_emperador - PAD)
    D.foto_parallax(lz, "rodolfo_arcimboldo", tl, I0 - d_emperador + 0.6, 1.02, 1.22, (0.5, 0.42), (0.5, 0.36), par=(80, 10), tono=(0.9, 0.86, 0.8))
    sombra_lateral(lz, "izq", 0.5)
    D.tag_nombre(lz, "Rodolfo II", 500, 260, t, d_rodolfo - 0.05, 56)
    D.numero(lz, "600", 470, 520, 240, t, d_600 - 0.05, color=RJ, fnt="abril", salida=None)
    carta(lz, pola("ducado", 380, 0.8, (0.3, 0.5)), I3, t, d_ducados - 0.1, 1560, 690, 5, desde=(300, 300))
    D.dibujar_bloque(lz, bloque([("Ducados", d_ducados), ("De", T("duenos", "de", frase=3, n=1)), ("Oro", d_oro)], 470, 700, 92, lineas=(1,)), t, "serif", 92)


# ================================================================== INTENTOS
@toma(I0 - PAD, I1 - 0.1, ent=("desenfoque", 0.45), grado=dict(sat=0.7))
def t_int_friedman(lz, t):
    tl = t - (I0 - PAD)
    D.foto_parallax(lz, "friedman", tl, I1 - I0 + 0.6, 1.05, 1.28, (0.32, 0.42), (0.34, 0.36), par=(80, 18), tono=(0.9, 0.9, 0.9))
    sombra_lateral(lz, "der", 0.5)
    D.tag_nombre(lz, "William Friedman", 560, 820, t, i_william - 0.05, 52)
    carta(lz, pola("purple", 380, 1.05, (0.5, 0.42), "Máquina Púrpura"), I3, t, i_purpura - 0.3, 1560, 760, 4, desde=(300, 300))
    D.dibujar_bloque(lz, bloque(kar("intentos", 0, 10, 15), 1480, 330, 80, lineas=(2, 4)), t, "serif", 80)


def _linea_eva(k):
    ws = PALABRAS_VOY[200 + 17 * k: 200 + 17 * k + 14]
    return " ".join(ws)


@toma(I1 - PAD, I2 - 0.1, ent=("latigo", 0.35))
def t_int_tarjetas(lz, t):
    tl = t - (I1 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.5, 0.85, (0.20, 0.16, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.1, W / 2, H / 2 - 8, 0.0), I2 - I1 + 0.4, mano=0.7)(tl)
    for k, (ti, x, y, r) in enumerate(((i_copio - 0.1, 700, 300, -5), (i_linea - 0.1, 1100, 480, 3), (i_tarjetas - 0.1, 800, 690, -2))):
        sp = D.tarjeta_perforada(_linea_eva(k), k)
        carta(lz, sp, cam, t, ti, x, y, r, s=0.78, desde=(-900, 0), dur=0.55, fase=k)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("intentos", 1, 6, 9), W / 2, 985, 84), t, "serif", 84, salida=i_tarjetas - 0.15)
    D.dibujar_bloque(lz, bloque(kar("intentos", 1, 10, 12), W / 2, 985, 84), t, "serif", 84)


@toma(I2 - PAD, I3_ - 0.1, ent=("latigo", 0.35))
def t_int_fracaso(lz, t):
    tl = t - (I2 - PAD)
    lz[:] = D.pozo_luz(0.35, 0.45, 0.8, (0.24, 0.17, 0.10))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.1, W / 2 - 20, H / 2, 0.0), I3_ - I2 + 0.3, mano=0.8)(tl)
    sp = folio(190, 900)
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, 600, 520, 1.0, -3, -6), smooth(prog(t, I2 - PAD, I2 + 0.3)))
    for k, (x, y, w_, h_) in enumerate(((440, 300, 170, 70), (700, 480, 190, 70), (520, 690, 170, 70))):
        D.marcador_mano(lz, "circulo", x, y, w_, h_, prog(t, i_pudo + 0.15 * k, i_pudo + 0.4 + 0.3 * k), semilla=k)
    D.marcador_mano(lz, "tachado", 600, 520, 620, 700, prog(t, i_desc + 0.1, i_desc + 0.6), grosor=12)
    D.dibujar_bloque(lz, bloque(kar("intentos", 2, 0, 3), 1400, 300, 90, lineas=(1,)), t, "serif", 90, salida=i_lenguaje - 0.2)
    D.dibujar_bloque(lz, bloque([("Lenguaje", i_lenguaje), ("Artificial", i_artificial), ("¿?", i_artificial + 0.4)], 1400, 620, 96, lineas=(1,), color=BL), t, "serif", 96)


@toma(I3_ - PAD, I4 - 0.1, ent=("desenfoque", 0.35), grado=dict(fuerza_vineta=0.8))
def t_int_ruido(lz, t):
    tl = t - (I3_ - PAD)
    D.foto_parallax(lz, "f187", tl, I4 - I3_ + 0.6, 2.0, 2.9, (0.3, 0.3), (0.62, 0.62), par=(0, 0), tono=(0.62, 0.6, 0.55))
    franja_texto(lz, 0.6, 0.74)
    D.dibujar_bloque(lz, bloque(kar("intentos", 3, 7, 12), W / 2, 985, 92), t, "serif", 92)


@toma(I4 - PAD, I5 - 0.1, ent=("desenfoque", 0.4))
def t_int_zipf(lz, t):
    tl = t - (I4 - PAD)
    D.foto_parallax(lz, "f187", tl, I5 - I4 + 0.6, 1.6, 1.95, (0.5, 0.4), (0.5, 0.5), par=(0, 0), tono=(0.32, 0.31, 0.29))
    D.grafica_zipf(lz, ZIPF, t, i_patrones - 0.6, W / 2, 470, 1240, 660, dur=max(2.0, i_real - i_patrones + 0.4))
    D.dibujar_bloque(lz, bloque(kar("intentos", 4, 5, 12), W / 2, 930, 72), t, "serif", 72)
    tx = D.palabra_img("37 945 palabras cada una · Fuentes: transcripción de Takahashi y Project Gutenberg", "sans_l", 26, (0.85, 0.85, 0.82), stroke=0.05, glow=0.4)
    D.mezclar_pm(lz, tx[0], tx[1], int(W / 2 - tx[0].shape[1] / 2), 1012, smooth(prog(t, i_patrones + 0.6, i_patrones + 1.0)))


@toma(I5 - PAD, T0 - 0.1, ent=("desenfoque", 0.4), grado=dict(fuerza_vineta=0.8))
def t_int_cifras(lz, t):
    tl = t - (I5 - PAD)
    D.foto_parallax(lz, "f190", tl, T0 - I5 + 0.6, 1.7, 2.2, (0.3, 0.3), (0.6, 0.55), par=(0, 0), tono=(0.36, 0.34, 0.30))
    n = int(38000 * e_out(prog(t, i_treinta - 0.1, i_palabras)))
    if t >= i_treinta - 0.1:
        pm, a, m = D.palabra_img(f"{n:,}".replace(",", " "), "sans", 190, tuple(BL), stroke=0.03, glow=0.75)
        D.mezclar_pm(lz, pm, a, int(560 - pm.shape[1] / 2), int(430 - pm.shape[0] / 2), smooth(prog(t, i_treinta - 0.1, i_treinta + 0.1)))
    D.dibujar_bloque(lz, bloque([("Palabras", i_palabras)], 560, 600, 84), t, "serif", 84)
    D.numero(lz, "20–25", 1400, 430, 190, t, i_veinte - 0.1, color=RJ, fnt="abril")
    D.dibujar_bloque(lz, bloque([("Símbolos", i_simbolos)], 1400, 600, 84), t, "serif", 84)


