# -*- coding: utf-8 -*-
def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:100]
    return s.replace(old, new, 1)


k = open('kit_cp.py', encoding='utf-8').read()
k = rep(k, 'wpx, hpx, yy = 1920, 640, 340', 'wpx, hpx, yy = 1920, 720, 420')
open('kit_cp.py', 'w', encoding='utf-8').write(k)

a = open('tomas_a.py', encoding='utf-8').read()
# 50 años: cifra roja + etiqueta
a = rep(a, '[S([("50", A(G, 1, "cincuenta")), ("Años", A(G, 1, "anos"))], 1500, 250, 150)]', '[N("50", 1480, 260, 230, A(G, 1, "cincuenta")), R([("años", A(G, 1, "anos"))], 1480, 440, 76)]')
# colleen_2: ordenador más claro + segundo plano
i0 = a.index('shot(INI(Co, 2), F_clip("stock/pc_antigua_1"')
i1 = a.index('# ============================================================== CRIMEN')
a = a[:i0] + '''shot(INI(Co, 2), F_clip("stock/pc_antigua_1", ini=1.0, z0=1.0, z1=1.2, c0=(0.55, 0.5), c1=(0.5, 0.5), tono=(1.45, 1.4, 1.3)),
     [R(pk(Co, 2, "computacion"), 1380, 830, 90)], [], ent=("fundido", 0.6), grado=dict(vineta=0.7))
shot(A(Co, 2, "abuelo", -0.3), F_clip("stock/pc_antigua_2", ini=1.0, z0=1.0, z1=1.15, tono=(1.15, 1.1, 1.0)),
     [], [], ent=("fundido", 0.6), grado=dict(vineta=0.75))

''' + a[i1:]
# bosque más claro
a = rep(a, 'F_clip("stock/bosque_niebla_0", ini=2.0, z0=1.0, z1=1.22, tono=(0.95, 1.0, 1.1)), [], [], ent=("fundido", 0.6), grado=dict(vineta=0.7))',
        'F_clip("stock/bosque_niebla_0", ini=2.0, z0=1.0, z1=1.22, tono=(1.5, 1.55, 1.7)), [], [], ent=("fundido", 0.6), grado=dict(vineta=0.65))')
a = rep(a, 'F_clip("stock/bosque_niebla_0", ini=12.0, z0=1.1, z1=1.3, tono=(0.62, 0.65, 0.75))', 'F_clip("stock/bosque_niebla_0", ini=12.0, z0=1.1, z1=1.3, tono=(1.1, 1.15, 1.3))')
# planta de vapor: abajo y más grande
a = rep(a, '("Abandonada", A(Cr, 1, "abandonada"))], W / 2, 120, 84)]', '("Abandonada", A(Cr, 1, "abandonada"))], W / 2, 975, 92)]')
# 30 min - 1 h con cifras lineales
i0 = a.index('[S([("30", A(Cr, 3, "media", -0.1))')
i1 = a.index('      R(pk(Cr, 3, "segun", "tribunal")')
a = a[:i0] + '[N("30 min", 1330, 400, 150, A(Cr, 3, "media", -0.1)), N("a 1 hora", 1330, 590, 150, A(Cr, 3, "hora", -0.1, 1)),\n' + a[i1:]
open('tomas_a.py', 'w', encoding='utf-8').write(a)

b = open('tomas_b.py', encoding='utf-8').read()
b = rep(b, 'TAG("Familia de Colleen Slemmer", 560, 230, A(Dd, 3, "familia"), 46)', 'TAG("Familia de Colleen Slemmer", 1450, 120, A(Dd, 3, "familia"), 46)')
b = rep(b, 'SELLO("Clemencia negada", 520, 540, A(Ca, 3, "nego"), 54, -9)', 'SELLO("Clemencia negada", 520, 720, A(Ca, 3, "nego"), 54, -9)')
b = rep(b, 'R(pk(Dd, 1, "nunca", "historia"), 1330, 190, 52, lineas=(3,))', 'R(pk(Dd, 1, "nunca", "historia"), 1330, 190, 62, lineas=(3,))')
open('tomas_b.py', 'w', encoding='utf-8').write(b)
print('ok')
