# -*- coding: utf-8 -*-
s = open('t03.py', encoding='utf-8').read()

# 1) arresto: soldados con antorchas, sin kwargs inexistentes
a = s.index("    ent = e_inout(prog(t, t_noche, t_arr - 0.3))")
b = s.index("    sal = e_inout(prog(t, t_arr, t_mand + 0.2))")
nuevo = '''    ent = e_inout(prog(t, t_noche, t_arr - 0.3))
    for i in range(7):
        x = lerp(520, 200 + 16 * i, ent)
        y = 120 + 12 * i - 6 * (i % 2)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: _soldado_antorcha(lz, iso, x, y, i, ent)))(x, y, i), fijo=False, clave=x + y)
'''
s = s[:a] + nuevo + s[b:]
s = s.replace("# ------------------------------------------------------------------------------------------------ 7. EL ARRESTO DE NOCHE",
'''# ------------------------------------------------------------------------------------------------ 7. EL ARRESTO DE NOCHE
def _soldado_antorcha(lz, iso, x, y, i, ent):
    G.persona(lz, iso, x, y, T_ACT[0], "granadero" if i % 2 else "yermo", dir=(-1, 0.3), vel=0.0 if ent > 0.98 else 1.0, seed=1300 + i, h=48)
    O.antorcha(lz, iso, x + 5, y + 3, T_ACT[0], h=30, seed=i)


T_ACT = [0.0]

''', 1)
s = s.replace("def p_arresto(lz, t):\n    cx, cy, cz, zm = cam_arr(t)", "def p_arresto(lz, t):\n    T_ACT[0] = t\n    cx, cy, cz, zm = cam_arr(t)")

# 2) golpe: lista de personajes válida
a = s.index("        pers = ((\"virrey\", 330")
b = s.index("            tt = [t_pod2, t_camb2 + 0.2, t_manos, t_fuerza]")
nuevo = '''        pers = (("virrey", 330, "serio"), ("yermo", 800, "enojo"), ("calleja", 1270, "enojo"), ("iturbide", 1740, "alegre"))
        kp = U.pop(t, t_pod2 - 0.3)
        if kp > 0.01:
            for i, (qn, px_, emo) in enumerate(pers):
                ki = U.pop(t, t_pod2 - 0.2 + 0.18 * i, 1.2)
                MD.medallon(lz, px_, 640, 118, qn, t, emocion=emo, k=ki, seed=i + 40)
'''
s = s[:a] + nuevo + s[b:]
open('t03.py', 'w', encoding='utf-8').write(s)

# 3) montes_lista en kz_mapa_dib
q = r'..\..\nucleo\kz_mapa_dib.py'
m = open(q, encoding='utf-8').read()
if "def montes_lista" not in m:
    m += '''

def montes_lista(lz, cam, picos, alfa=1.0):
    """Montañas en posiciones dadas [(lon, lat, altitud_m), ...] (para zonas sin datos de relieve: Pirineos, Alpes…)."""
    z = cam[2]
    for (lon, lat, alt) in picos:
        x, y = M.proy(cam, lon, lat)
        if -60 < x < W + 60 and -80 < y < H + 60:
            s = (0.55 + 0.9 * min(1.0, (alt - 2000) / 3400.0)) * max(0.7, min(2.2, z ** 0.45)) * 26
            _monte(lz, float(x), float(y), s, alt, alfa)
'''
    open(q, 'w', encoding='utf-8').write(m)
print('ok')
