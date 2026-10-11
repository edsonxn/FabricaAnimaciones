# -*- coding: utf-8 -*-
"""Parche 2 de la escena 2: etiquetas laterales en el decreto, transición limpia, etiqueta del barco y ciudades de Europa."""
p = 't02.py'
s = open(p, encoding='utf-8').read()

# 1) etiquetas laterales (cada una a un lado del grupo, con cola lateral)
a = s.index("    qx, qy = iso.P(140, 184, 80)\n    k = U.pop(t, t_iglesia) * U.salida(t, T_DINERO)")
b = s.index("# ------------------------------------------------------------------------------------------------ 5b.")
nuevo = '''    qx, qy = iso.P(140, 184, 70)
    k = U.pop(t, t_iglesia) * U.salida(t, T_DINERO)
    if k > 0.01:
        U.llamada(lz, float(qx) + 70, float(qy) - 60, "La Iglesia", color=U.COL["morado"], px=46, k=k, cola="izq")
        _signo(lz, float(qx) + 20, float(qy) - 150, U.pop(t, t_iglesia + 0.3) * U.salida(t, T_DINERO))
    qx, qy = iso.P(118, 178, 70)
    k = U.pop(t, t_iglesia + 0.5) * U.salida(t, T_DINERO)
    if k > 0.01:
        U.llamada(lz, float(qx) - 70, float(qy) - 60, "Propietarios", color=U.COL["naranja"], px=46, k=k, cola="der")
        _signo(lz, float(qx) - 20, float(qy) - 150, U.pop(t, t_iglesia + 0.6) * U.salida(t, T_DINERO))


'''
s = s[:a] + nuevo + s[b:]

# 2) transición limpia hacia el mapa
s = s.replace('@shot(T_DINERO, bg=lambda t: MP.base(cam_dinero(t), t), post=[GRAD], ent=("zoom", 0.8))', '@shot(T_DINERO, bg=lambda t: MP.base(cam_dinero(t), t), post=[GRAD], ent=("fundido", 0.5))')

# 3) etiqueta del barco anclada a la cabeza de la ruta
s = s.replace('''    kk = U.pop(t, t_deudas - 0.2) * U.salida(t, t_guerras - 0.6)
    if kk > 0.01:
        sx, sy = MP.proy(cam, -52.0, 31.0)
        U.llamada(lz, float(sx), float(sy) - 60, "dinero para la Corona", color=U.COL["naranja"], px=44, k=kk, cola="abajo")''',
'''    kk = U.pop(t, t_deudas - 0.2) * U.salida(t, t_guerras - 0.6)
    if kk > 0.01 and cab is not None:
        U.llamada(lz, cab[0], cab[1] - 60, "dinero para la Corona", color=U.COL["naranja"], px=44, k=kk, cola="abajo")''')

# 4) ciudades de Europa con banderas de colores
s = s.replace('''    kk = U.pop(t, t_guerras - 0.6)
    if kk > 0.01:
        sx, sy = MP.proy(cam, -3.6, 40.4)
        MD.corona(lz, float(sx), float(sy) - 36, 1.5 * kk, t=t)''',
'''    for j, (lug, tipo, col) in enumerate((("madrid", "ciudad", (255, 206, 70)), ("cadiz", "puerto", (255, 206, 70)), ("lisboa", "puerto", (90, 190, 120)), ("paris", "ciudad", (80, 130, 230)),
                                          ("londres", "ciudad", (230, 90, 120)), ("roma", "ciudad", (150, 130, 230)), ("berlin", "ciudad", (240, 160, 70)))):
        MD.ciudad(lz, cam, lug, t, t_guerras - 0.9 + 0.1 * j, tam=1.5 if cam[2] > 0.6 else 1.1, tipo=tipo, bando=col, semilla=j + 40)
    kk = U.pop(t, t_guerras - 0.6)
    if kk > 0.01:
        sx, sy = MP.proy(cam, -3.7, 40.4)
        MD.corona(lz, float(sx), float(sy) - 80, 1.5 * kk, t=t)''')
open(p, 'w', encoding='utf-8').write(s)

# 5) coordenadas de las ciudades europeas en kz_mapa_dib
q = r'..\..\nucleo\kz_mapa_dib.py'
m = open(q, encoding='utf-8').read()
if '"madrid"' not in m:
    m = m.replace('"zitacuaro": (-100.36, 19.43),', '"zitacuaro": (-100.36, 19.43), "madrid": (-3.70, 40.42), "cadiz": (-6.29, 36.53), "lisboa": (-9.14, 38.72), "paris": (2.35, 48.86), "londres": (-0.12, 51.50), "roma": (12.50, 41.90), "berlin": (13.40, 52.52),')
open(q, 'w', encoding='utf-8').write(m)
print('ok')
