# -*- coding: utf-8 -*-
def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:90]
    return s.replace(old, new, 1)


k = open('kit_cp.py', encoding='utf-8').read()
k = rep(k, 'def LINEA_ANOS(a_ini, a_fin, y, marcas, t_ini, t_fin_barra, r0, r1, x0=170, x1=1750, etiqueta="", sal=None):',
        'def LINEA_ANOS(a_ini, a_fin, y, marcas, t_ini, t_fin_barra, r0, r1, x0=170, x1=1750, etiqueta="", sal=None, paso=5, paso_lab=10):')
k = rep(k, '''        for yr in range(int(math.ceil(a_ini / 5) * 5), int(a_fin) + 1, 5):
            big = yr % 10 == 0''', '''        for yr in range(int(math.ceil(a_ini / paso) * paso), int(a_fin) + 1, paso):
            big = yr % paso_lab == 0''')
k = rep(k, '''            yr, txt, ta = m[:3]
            if t < ta:
                continue
            up, hh = m[3] if len(m) > 3 else (k_ % 2 == 0, 110)''', '''            yr, txt, ta = m[:3]
            if t < ta:
                continue
            up, hh = m[3] if len(m) > 3 else (k_ % 2 == 0, 110)
            lab = m[4] if len(m) > 4 else str(int(yr))''')
k = rep(k, 'd.text((px(yr), y1 - 10 if up else y1 + 10), str(yr), font=D.fuente("serif", 64),', 'd.text((px(yr), y1 - 10 if up else y1 + 10), lab, font=D.fuente("serif", 58),')
open('kit_cp.py', 'w', encoding='utf-8').write(k)

b = open('tomas_b.py', encoding='utf-8').read()
marca = '# ============================================================== PRECEDENTE'
assert marca in b
nuevo = '''# ============================================================== HISTORIAL (contexto: problemas previos de Tennessee con sus ejecuciones)
Hs = "historial"
_mh = [(2022.3, "Frena la ejecución de Oscar Smith", A(Hs, 1, "oscar"), (True, 120), "Abr. 2022"),
       (2025.0, "Se reanudan las ejecuciones", A(Hs, 2, "hasta"), (False, 120), "2025"),
       (2026.38, "Una ejecución se detiene: sin vía", A(Hs, 4, "segunda", -0.25), (True, 250), "May. 2026"),
       (2026.75, "Pike: dos dosis y sigue viva", A(Hs, 4, "fallida"), (False, 120), "30 sep. 2026")]
_lh = LINEA_ANOS(2021, 2027.2, 600, _mh, A(Hs, 1, "abril"), A(Hs, 2, "veinticinco", 0.2), 2022.3, 2025.0, x0=190, x1=1740,
                 etiqueta="Ejecuciones en Tennessee", paso=1, paso_lab=1)
shot(INI(Hs, 0), F_clip("newschannel5_hospital", ini=68.4, fin=73.4, z0=1.0, z1=1.12, banner=0.17, tono=(0.7, 0.72, 0.8)),
     [R([("Tennessee", A(Hs, 0, "tenesi")), ("ya", A(Hs, 0, "ya")), ("tenía", A(Hs, 0, "tenia"))], W / 2, 880, 80)],
     [CRED(C_5, INI(Hs, 0) + 0.3, FIN(Hs, 0))], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(INI(Hs, 1), F_clip("stock/alambre_1", ini=3.0, z0=1.0, z1=1.12, tono=(0.5, 0.52, 0.6)), [], [_lh], ent=("fundido", 0.7), grado=dict(vineta=0.9))
shot(INI(Hs, 3), F_clip("stock/pasillo_oscuro_3", ini=3.0, z0=1.0, z1=1.12, tono=(0.55, 0.57, 0.66)),
     [N("4", 330, 190, 220, A(Hs, 3, "cuatro")), R(pk(Hs, 3, "personas"), 330, 330, 54)], [_lh], ent=("fundido", 0.6), grado=dict(vineta=0.9))
shot(INI(Hs, 4), F_clip("stock/documento_1", ini=2.0, z0=1.0, z1=1.12, tono=(0.5, 0.5, 0.56), sat=0.6),
     [R(pk(Hs, 4, "segunda", "fallida"), W / 2, 170, 78, lineas=(2,))], [_lh],
     ent=("fundido", 0.6), grado=dict(vineta=0.9))
shot(INI(Hs, 5), F_clip("newschannel5_hospital", ini=288.8, fin=292.1, z0=1.0, z1=1.12, banner=0.17, tono=(0.8, 0.78, 0.78)),
     [S([("Pentobarbital", A(Hs, 5, "pentobarbital"))], W / 2, 250, 118)],
     [TAG("Frank Strada · desde enero de 2023", 560, 900, A(Hs, 5, "frank"), 46), CRED(C_5, INI(Hs, 5) + 0.3, FIN(Hs, 5))], ent=("fundido", 0.6), grado=dict(vineta=0.85))

'''
b = b.replace(marca, nuevo + marca, 1)
open('tomas_b.py', 'w', encoding='utf-8').write(b)
print('ok')
