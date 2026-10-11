# -*- coding: utf-8 -*-
def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:100]
    return s.replace(old, new, 1)


b = open('tomas_b.py', encoding='utf-8').read()
b = rep(b, '[N("4", 330, 190, 220, A(Hs, 3, "cuatro")), R(pk(Hs, 3, "personas"), 330, 330, 54)]', '[N("4", 1560, 200, 230, A(Hs, 3, "cuatro")), R(pk(Hs, 3, "personas"), 1560, 380, 62)]')
b = rep(b, 'F_clip("stock/mazo_1", ini=1.0, z0=1.0, z1=1.15, tono=(0.7, 0.7, 0.75))', 'F_clip("stock/mazo_2", ini=1.0, z0=1.0, z1=1.15, tono=(1.5, 1.45, 1.4))')
b = rep(b, 'F_clip("stock/ciudad_noche_0", ini=1.0, z0=1.0, z1=1.15, tono=(0.7, 0.72, 0.85))', 'F_clip("stock/ciudad_noche_0", ini=1.0, z0=1.0, z1=1.15, tono=(1.5, 1.5, 1.8))')
b = rep(b, 'F_clip("stock/carretera_noche_0", ini=1.0, z0=1.0, z1=1.12, tono=(0.6, 0.62, 0.75))', 'F_clip("stock/carretera_noche_0", ini=1.0, z0=1.0, z1=1.12, tono=(1.3, 1.3, 1.5))')
b = rep(b, 'S([("Colleen", A(Ci, 3, "colin")), ("Slemmer", A(Ci, 3, "colin", 0.4))], 1330, 330, 96, lineas=(1,)),\n      N("1975 – 1995", 1330, 540, 130, A(Ci, 3, "diecinueve", -0.3), color=BL)]',
        'S([("Colleen", A(Ci, 3, "colin")), ("Slemmer", A(Ci, 3, "colin", 0.4))], 1610, 380, 96, lineas=(1,)),\n      N("1975 – 1995", 1610, 600, 110, A(Ci, 3, "diecinueve", -0.3), color=BL)]')
b = rep(b, '''                "Fotos: Wikimedia Commons — Kaldari, Cessna86, Jon698, Warren LeMay, Joe Ravi, Lynn Freeny, Quintin Soloviev, Bill Allen / AP",''',
        '''                "Fotos (Wikimedia Commons): Kaldari, Cessna86, Jon698, Warren LeMay, Joe Ravi,",
                "Lynn Freeny, Quintin Soloviev, Bill Allen / AP",''')
open('tomas_b.py', 'w', encoding='utf-8').write(b)
print('ok')
