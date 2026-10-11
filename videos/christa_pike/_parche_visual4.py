# -*- coding: utf-8 -*-
def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:90]
    return s.replace(old, new, 1)


b = open('tomas_b.py', encoding='utf-8').read()
# d3: rueda de prensa con el retrato (NBC) en lugar del clip de la carpa
b = rep(b, '''shot(INI(Dd, 3), F_clip("wbir_carpa", ini=71.0, fin=79.0, z0=1.35, z1=1.5, c0=(0.2, 0.52), c1=(0.22, 0.5), tono=(0.9, 0.9, 0.92)),
     [R(pk(Dd, 3, "pagar"), 1380, 560, 70)], [TAG("Familia de Colleen Slemmer", 1480, 880, A(Dd, 3, "familia"), 46), CRED(C_W, INI(Dd, 3) + 0.3, FIN(Dd, 3))],
     ent=("fundido", 0.7))''', '''shot(INI(Dd, 3), F_clip("nbc_ventilador", ini=60.0, fin=64.4, z0=1.0, z1=1.1, banner=0.2, tono=(0.9, 0.9, 0.95)),
     [R(pk(Dd, 3, "pagar"), W / 2, 880, 70)], [TAG("Familia de Colleen Slemmer", 560, 230, A(Dd, 3, "familia"), 46), CRED(C_N, INI(Dd, 3) + 0.3, FIN(Dd, 3))],
     ent=("fundido", 0.7))''')
b = rep(b, '''shot(INI(De, 8), F_clip("wbir_carpa", ini=72.0, fin=79.0, z0=1.35, z1=1.5, c0=(0.2, 0.52), c1=(0.22, 0.5), tono=(0.8, 0.8, 0.84)),
     [R([("«Todo", A(De, 8, "queria", -0.5)), ("lo", A(De, 8, "queria", -0.35)), ("que", A(De, 8, "queria", -0.2)), ("quería", A(De, 8, "queria")),
         ("era", A(De, 8, "era")), ("justicia»", A(De, 8, "justicia"))], 1380, 560, 62, lineas=(3,))],
     [CRED(C_W, INI(De, 8) + 0.3, FIN(De, 8))], ent=("fundido", 0.7), grado=dict(vineta=0.85))''',
        '''shot(INI(De, 8), F_clip("abc_ventilador", ini=64.2, fin=68.1, z0=1.0, z1=1.1, banner=0.22, tono=(0.8, 0.8, 0.84)),
     [R([("«Todo", A(De, 8, "queria", -0.5)), ("lo", A(De, 8, "queria", -0.35)), ("que", A(De, 8, "queria", -0.2)), ("quería", A(De, 8, "queria")),
         ("era", A(De, 8, "era")), ("justicia»", A(De, 8, "justicia"))], W / 2, 860, 62, lineas=(3,))],
     [TAG("May Martinez", 560, 230, INI(De, 8) + 0.3, 46), CRED("Foto: AP · ABC News", INI(De, 8) + 0.3, FIN(De, 8))], ent=("fundido", 0.7), grado=dict(vineta=0.85))''')
# gobernador: foto sobria de dominio público
b = rep(b, 'pola("bill_lee", 520, 1.22, (0.5, 0.3), "Gobernador Bill Lee")', 'pola("bill_lee3", 520, 1.22, (0.5, 0.35), "Gobernador Bill Lee")')
b = rep(b, 'pola("scotus", 760, 0.74, (0.5, 0.5), "Corte Suprema de EE. UU.")', 'pola("scotus", 760, 0.74, (0.5, 0.5), "Corte Suprema")')
b = rep(b, 'CRED("Fotos: Maryland GovPics (CC BY 2.0) · Kjetil Ree (CC BY-SA 3.0) · Wikimedia Commons"', 'CRED("Fotos: Lynn Freeny (dominio público) · Kjetil Ree (CC BY-SA 3.0) · Wikimedia Commons"')
b = rep(b, 'shot(INI(De, 3), F_borroso("bill_lee", 0.28),', 'shot(INI(De, 3), F_borroso("bill_lee3", 0.28),')
b = rep(b, 'HERO("bill_lee", 600, 520, -3, alto=820,', 'HERO("bill_lee3", 600, 520, -3, alto=760,')
b = rep(b, 'CRED("Foto: Maryland GovPics · Wikimedia Commons (CC BY 2.0)"', 'CRED("Foto: Lynn Freeny · Wikimedia Commons (dominio público)"')
b = rep(b, 'Maryland GovPics, Quintin Soloviev', 'Lynn Freeny, Quintin Soloviev')
open('tomas_b.py', 'w', encoding='utf-8').write(b)
print('ok')
