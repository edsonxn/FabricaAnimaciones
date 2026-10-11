# -*- coding: utf-8 -*-
def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:90]
    return s.replace(old, new, 1)


k = open('kit_cp.py', encoding='utf-8').read()
i0 = k.index("def LINEA_ANOS(")
i1 = k.index("# ------------------------------------------------------------------ persianas")
nuevo = '''def LINEA_ANOS(a_ini, a_fin, y, marcas, t_ini, t_fin_barra, r0, r1, x0=170, x1=1750, etiqueta="", sal=None):
    """Eje de años con una barra que crece de r0 a r1 y marcas [(año, texto, t_aparece[, (arriba, alto)])]. `y` = y del eje en pantalla."""
    def f(lz, t):
        if t < t_ini:
            return
        o = smooth(prog(t, t_ini, t_ini + 0.4)) * (1 - (smooth(prog(t, sal, sal + 0.4)) if sal is not None else 0))
        wpx, hpx, yy = 1920, 640, 340
        im = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        px = lambda yr: x0 + (yr - a_ini) / (a_fin - a_ini) * (x1 - x0)
        d.line([x0, yy, x1, yy], fill=(235, 235, 230, 255), width=6)
        for yr in range(int(math.ceil(a_ini / 5) * 5), int(a_fin) + 1, 5):
            big = yr % 10 == 0
            d.line([px(yr), yy - (20 if big else 10), px(yr), yy + (20 if big else 10)], fill=(235, 235, 230, 255), width=4 if big else 2)
            if big:
                d.text((px(yr), yy + 34), str(yr), font=D.fuente("sans", 36), fill=(235, 235, 230, 255), anchor="mt", stroke_width=2, stroke_fill=(0, 0, 0, 255))
        u = e_inout(clamp01((t - t_ini - 0.2) / max(t_fin_barra - t_ini, 0.5)))
        xa, xb = px(r0), lerp(px(r0), px(r1), u)
        d.rectangle([xa, yy - 24, max(xb, xa + 2), yy + 24], fill=(232, 240, 40, 235))
        for k_, m in enumerate(marcas):
            yr, txt, ta = m[:3]
            if t < ta:
                continue
            up, hh = m[3] if len(m) > 3 else (k_ % 2 == 0, 110)
            q = e_out(prog(t, ta, ta + 0.35))
            y1 = yy - hh * q if up else yy + 44 + hh * q
            d.line([px(yr), yy - 16 if up else yy + 16, px(yr), y1], fill=(200, 200, 195, int(255 * q)), width=4)
            d.ellipse([px(yr) - 13, yy - 13, px(yr) + 13, yy + 13], fill=(190, 235, 30, 255))
            d.text((px(yr), y1 - 10 if up else y1 + 10), str(yr), font=D.fuente("serif", 64), fill=(232, 240, 40, int(255 * q)), anchor="mb" if up else "mt",
                   stroke_width=2, stroke_fill=(0, 0, 0, int(255 * q)))
            d.text((px(yr), y1 - 78 if up else y1 + 80), txt, font=D.fuente("sans_l", 35), fill=(238, 238, 232, int(255 * q)), anchor="mb" if up else "mt",
                   stroke_width=3, stroke_fill=(0, 0, 0, int(255 * q)))
        if etiqueta:
            d.text((wpx / 2, 24), etiqueta, font=D.fuente("sans_l", 38), fill=(228, 228, 222, 255), anchor="mt", stroke_width=3, stroke_fill=(0, 0, 0, 255))
        a = np.asarray(im, np.float32) / 255.0
        D.mezclar_pm(lz, a[..., :3] * a[..., 3:4], a[..., 3], 0, int(y - yy), o)
    return f


def CRONO(t0, t1, cx, cy, r=180, color=(0.86, 0.10, 0.10)):
    """Reloj circular que se llena (de 0 a una vuelta) entre t0 y t1; marcas cada cinco minutos de una hora."""
    def f(lz, t):
        if t < t0:
            return
        o = smooth(prog(t, t0, t0 + 0.5))
        u = e_inout(prog(t, t0 + 0.3, t1))
        buf = lz.copy()
        cv2.circle(buf, (cx, cy), r + 6, (0.03, 0.03, 0.03), 26, cv2.LINE_AA)
        cv2.circle(buf, (cx, cy), r, (0.35, 0.35, 0.35), 8, cv2.LINE_AA)
        for k_ in range(12):
            a = math.radians(k_ * 30 - 90)
            cv2.line(buf, (int(cx + math.cos(a) * (r - 22)), int(cy + math.sin(a) * (r - 22))), (int(cx + math.cos(a) * (r + 2)), int(cy + math.sin(a) * (r + 2))),
                     (0.9, 0.9, 0.88), 4, cv2.LINE_AA)
        if u > 0.003:
            cv2.ellipse(buf, (cx, cy), (r, r), 0, -90, -90 + 360 * u, color, 16, cv2.LINE_AA)
            a = math.radians(-90 + 360 * u)
            cv2.circle(buf, (int(cx + math.cos(a) * r), int(cy + math.sin(a) * r)), 15, (1.0, 0.95, 0.9), -1, cv2.LINE_AA)
        lz[:] = lz * (1 - o) + buf * o
    return f


'''
k = k[:i0] + nuevo + k[i1:]
open('kit_cp.py', 'w', encoding='utf-8').write(k)

a = open('tomas_a.py', encoding='utf-8').read()
a = rep(a, '''_marcas = [(2001, "Pide ser ejecutada", A(Cd, 1, "uno")), (2002, "Lo pide otra vez", ww(Cd, 1, "dos", 2)),
           (2004, "Condena por atacar a otra presa", A(Cd, 2, "cuatro")), (2022, "Demanda por igualdad", A(Cd, 3, "veintidos")),
           (2024, "Acuerdo con el estado", A(Cd, 3, "veinticuatro"))]''',
        '''_marcas = [(2001, "Pide ser ejecutada", A(Cd, 1, "uno"), (True, 120)), (2002, "Lo pide otra vez", ww(Cd, 1, "dos", 2), (False, 120)),
           (2004, "Condena por atacar a otra presa", A(Cd, 2, "cuatro"), (True, 230)), (2022, "Demanda por igualdad", A(Cd, 3, "veintidos"), (False, 120)),
           (2024, "Acuerdo con el estado", A(Cd, 3, "veinticuatro"), (True, 120))]''')
a = rep(a, 'LINEA_ANOS(1995, 2027, 560, _marcas,', 'LINEA_ANOS(1995, 2027, 600, _marcas,')
a = rep(a, 'TAG("Tadaryl Shipp · cadena perpetua", 1520, 880,', 'TAG("Tadaryl Shipp · cadena perpetua", 1320, 880,')
a = rep(a, 'F_clip("stock/bosque_niebla_0", ini=2.0, z0=1.0, z1=1.22, tono=(0.7, 0.74, 0.82)), [], [], ent=("fundido", 0.6), grado=dict(vineta=0.85))',
        'F_clip("stock/bosque_niebla_0", ini=2.0, z0=1.0, z1=1.22, tono=(0.95, 1.0, 1.1)), [], [], ent=("fundido", 0.6), grado=dict(vineta=0.7))')
i0 = a.index('shot(INI(Cr, 3), F_clip("stock/bosque_niebla_0", ini=12.0')
i1 = a.index('shot(INI(Cr, 4)')
a = a[:i0] + '''shot(INI(Cr, 3), F_clip("stock/bosque_niebla_0", ini=12.0, z0=1.1, z1=1.3, tono=(0.62, 0.65, 0.75)),
     [S([("30", A(Cr, 3, "media", -0.1)), ("Minutos", A(Cr, 3, "media", 0.2)), ("a", A(Cr, 3, "hora", 0.1, 1) - 0.4), ("1", A(Cr, 3, "hora", -0.1, 1)), ("Hora", A(Cr, 3, "hora", 0.2, 1))], 1330, 480, 112, lineas=(2,)),
      R(pk(Cr, 3, "segun", "tribunal"), W / 2, 900, 62)],
     [CRONO(A(Cr, 3, "media", -0.2), A(Cr, 3, "hora", 0.3, 1), 500, 500, 190)], ent=("fundido", 0.7), grado=dict(vineta=0.8))
''' + a[i1:]
open('tomas_a.py', 'w', encoding='utf-8').write(a)
print('ok')
