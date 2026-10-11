# -*- coding: utf-8 -*-
"""Parche: caras con rasgos (ojos con esclerótica, cejas, nariz, boca con expresión) en `persona` cuando se ve grande; Napoleón con redingote gris y mano en el chaleco."""
p = 'kz_gente_iso.py'
s = open(p, encoding='utf-8').read()

# 1) firma: parámetro cara
s = s.replace("def persona(lz, iso, x, y, t=0.0, tipo=\"campesino\", dir=(1.0, 0.0), vel=0.0, seed=0, piel=None, h=34.0, accion=None, z=0.0, tp=0.0, rop=None, sombra=True, alfa=1.0, carga=None):",
              "def persona(lz, iso, x, y, t=0.0, tipo=\"campesino\", dir=(1.0, 0.0), vel=0.0, seed=0, piel=None, h=34.0, accion=None, z=0.0, tp=0.0, rop=None, sombra=True, alfa=1.0, carga=None, cara=None):")

# 2) rasgos faciales: reemplazar el bloque de ojos de puntos
a = s.index("        if not lod:\n            ex = sx + (1.6 * lado + 0.4 * lado) * u")
b = s.index("    _sombrero(lz, spec.get(\"sombrero\"), sx + 0.4 * u * lado, hy, u, A, lado, pelo, spec, frente)")
nuevo = '''        if not lod:
            _rasgos(lz, sx + 0.4 * u * lado, hy, u, A, lado, hp, accion, cara, t + tp, seed, pc)
'''
s = s[:a] + nuevo + s[b:]

# 3) función _rasgos
s = s.replace("def _brazo(lz, x0, y0, L, ang, torso, piel, u, A, oscuro=False):", '''def _rasgos(lz, hx, hy, u, A, lado, hp, accion, cara, t, seed, pc):
    """Cara según el tamaño en pantalla: lejos, dos puntos; media, ojos y boca; cerca, ojos con esclerótica, cejas, nariz y boca expresiva."""
    emo = cara or ("alegre" if accion in ("vitorea", "saluda") else "habla" if accion == "habla" else "normal")
    oscuro = (40, 26, 36)
    cierre = 1.0 - 0.9 * (1.0 if ((t + seed * 1.7) % 3.6) > 3.45 else 0.0)          # parpadeo
    big = hp > 105
    mid = hp > 62
    for sg in (-1, 1):
        ex = hx + sg * 1.95 * u + 0.5 * u * lado
        ey = hy + 0.2 * u
        if big:
            lz.relleno(elipse(ex, ey, 1.35 * u, 1.55 * u * cierre, 0, 10), tint((252, 250, 246)), alfa=A)
            lz.relleno(circulo(ex + 0.35 * u * lado, ey + 0.1 * u, 0.75 * u, 8), tint(oscuro), alfa=A)
            ang = {"enojo": 0.45, "miedo": -0.35, "triste": -0.4, "alegre": -0.1}.get(emo, 0.0) * sg * -1
            lz.relleno(np.array([[ex - 1.5 * u, ey - 2.0 * u + ang * 1.5 * u], [ex + 1.5 * u, ey - 2.0 * u - ang * 1.5 * u], [ex + 1.5 * u, ey - 1.4 * u - ang * 1.5 * u], [ex - 1.5 * u, ey - 1.4 * u + ang * 1.5 * u]]), tint(P.oscurecer(pc, 0.55)), alfa=A)
        else:
            lz.relleno(circulo(ex, ey, 0.75 * u, 6), tint(oscuro), alfa=A)
    if big:        # nariz
        lz.relleno(np.array([[hx + 0.6 * u * lado, hy + 0.7 * u], [hx + 1.5 * u * lado, hy + 2.0 * u], [hx - 0.1 * u * lado, hy + 2.1 * u]]), tint(P.oscurecer(pc, 0.18)), alfa=A)
    my = hy + 3.1 * u
    if mid:
        if emo == "habla":
            ap = 0.5 + 0.9 * abs(math.sin(t * 10 + seed))
            lz.relleno(elipse(hx + 0.4 * u * lado, my, 1.5 * u, ap * u, 0, 10), tint((110, 36, 56)), alfa=A)
        elif emo == "alegre":
            lz.relleno(np.array([[hx - 1.9 * u, my - 0.6 * u], [hx + 2.7 * u, my - 0.6 * u], [hx + 0.4 * u, my + 1.7 * u]]), tint((120, 40, 60)), alfa=A)
        elif emo == "enojo":
            lz.relleno(np.array([[hx - 1.5 * u, my + 0.8 * u], [hx + 0.4 * u, my - 0.2 * u], [hx + 2.3 * u, my + 0.8 * u], [hx + 0.4 * u, my + 0.3 * u]]), tint((96, 40, 54)), alfa=A)
        elif emo in ("miedo", "triste"):
            lz.relleno(elipse(hx + 0.4 * u * lado, my + 0.3 * u, 1.0 * u, 1.2 * u, 0, 8), tint((110, 36, 56)), alfa=A)
        else:
            lz.relleno(rect_red(hx - 1.2 * u + 0.4 * u * lado, my, 3.2 * u, 0.55 * u, 0.2 * u), tint((120, 60, 66)), alfa=A)


def _brazo(lz, x0, y0, L, ang, torso, piel, u, A, oscuro=False):''', 1)

# 4) acción «chaleco» (mano dentro de la casaca)
s = s.replace('''    if accion == "reza":
        return _brazo(lz, sh_x - 2 * u, sh_y, 8 * u, 0.5 * lado, tor, pc, u, A)''', '''    if accion == "reza":
        return _brazo(lz, sh_x - 2 * u, sh_y, 8 * u, 0.5 * lado, tor, pc, u, A)
    if accion == "chaleco":
        return _brazo(lz, sh_x - 1 * u, sh_y, 7 * u, 2.5 * lado * 0 + 2.6, tor, pc, u, A)''')

# 5) Napoleón: redingote gris
s = s.replace('"napoleon": dict(torso=(52, 86, 160), pierna=(246, 244, 240), sombrero="bicornio_lado", cruz=True),', '"napoleon": dict(torso=(112, 118, 126), pierna=(246, 244, 240), sombrero="bicornio_lado", cuello=(250, 250, 248), faja=(250, 206, 90)),')
open(p, 'w', encoding='utf-8').write(s)

# t03: Napoleón con la mano en el chaleco, corona más chica
q = r'..\videos\independencia_mx\t03.py'
t = open(q, encoding='utf-8').read()
t = t.replace('G.persona(lz, iso, 200, 112, t, "napoleon", dir=(-1, 0.6), seed=72, piel=G.PIELES[0], h=58, accion="habla" if t < t_abd else None)', 'G.persona(lz, iso, 200, 112, t, "napoleon", dir=(-1, 0.6), seed=72, piel=G.PIELES[0], h=58, accion="chaleco", cara="serio")')
t = t.replace("O2.corona(lz, iso, cx_, cy_, z_, 1.8, rot=u * 9.0)", "O2.corona(lz, iso, cx_, cy_, z_, 0.9, rot=u * 9.0)")
t = t.replace('G.persona(lz, iso, 82, 156, t, "monarca", dir=(1, -0.6), seed=71, piel=G.PIELES[0], h=58, accion="trabaja" if firma < 1 else None)', 'G.persona(lz, iso, 82, 156, t, "monarca", dir=(1, -0.6), seed=71, piel=G.PIELES[0], h=58, accion="trabaja" if firma < 1 else None, cara="triste")')
open(q, 'w', encoding='utf-8').write(t)
print('ok')
