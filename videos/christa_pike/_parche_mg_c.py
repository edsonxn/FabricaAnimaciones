# -*- coding: utf-8 -*-
"""Ajustes de maquetación tras revisar las hojas de cuadros con las escenas dibujadas."""


def rep(s, old, new, todos=False):
    assert old in s, "NO ENCONTRADO: " + old[:100]
    return s.replace(old, new) if todos else s.replace(old, new, 1)


b = open('tomas_b.py', encoding='utf-8').read()
# relojes de la noche: fuera de la ventana de observación
b = rep(b, 'RELOJ("7:26 p. m.", 1620, 330, 190, A(N_, 1, "siete"))', 'RELOJ("7:26 p. m.", 1700, 200, 150, A(N_, 1, "siete"))')
b = rep(b, 'RELOJ("7:46 p. m.", 1620, 330, 190, INI(N_, 5))', 'RELOJ("7:46 p. m.", 1700, 200, 150, INI(N_, 5))')
b = rep(b, 'RELOJ("7:34 p. m.", 1560, 960, 160, A(N_, 3, "treinta"))', 'RELOJ("7:34 p. m.", 1640, 1000, 130, A(N_, 3, "treinta"))')
b = rep(b, 'RELOJ("8:05 p. m.", 1500, 300, 190, INI(N_, 7))', 'RELOJ("8:05 p. m.", 1620, 330, 170, INI(N_, 7))')
# cuenta atrás de 5 minutos: encima de la jeringa, no sobre el reloj
b = rep(b, 'TEMPORIZADOR(A(N_, 6, "cinco", -0.1), A(N_, 6, "viva", 0.2), 560, 560, 130)', 'TEMPORIZADOR(A(N_, 6, "cinco", -0.1), A(N_, 6, "viva", 0.2), 1380, 250, 150)')
# etiquetas que chocaban con textos de la escena
b = rep(b, 'TAG("Abogados de Christa Pike", 1500, 960, A(De, 6, "falla"), 46)', 'TAG("Abogados de Christa Pike", 1560, 760, A(De, 6, "falla"), 46)')
b = rep(b, 'R(pk(Ca, 1, "mas", "hora"), W / 2, 960, 74)', 'R(pk(Ca, 1, "mas", "hora"), W / 2, 1010, 70)')
b = rep(b, 'TAG("Frank Strada · desde enero de 2023", 1300, 960, A(Hs, 5, "frank"), 46)', 'TAG("Frank Strada · desde enero de 2023", 1330, 790, A(Hs, 5, "frank"), 46)')
open('tomas_b.py', 'w', encoding='utf-8').write(b)

e3 = open('mg_esc3.py', encoding='utf-8').read()
e3 = rep(e3, '    p.texto("2.ª DOSIS", 1380, 820, 60, CREMA, "sans_b", smooth(pr(t, tu + 0.3, tu + 0.9)))\n', '')
open('mg_esc3.py', 'w', encoding='utf-8').write(e3)

e2 = open('mg_esc2.py', encoding='utf-8').read()
e2 = rep(e2, 'cruz(p, x + 10, 935, 36, pr(t, tk + per * 0.3, tk + per * 0.55), ROJO, 14)', 'cruz(p, x + 10, 905, 34, pr(t, tk + per * 0.3, tk + per * 0.55), ROJO, 14)')
open('mg_esc2.py', 'w', encoding='utf-8').write(e2)

e4 = open('mg_esc4.py', encoding='utf-8').read()
e4 = rep(e4, 'p.texto("desde 2024 · único fármaco", 1100, 900, 40,', 'p.texto("desde 2024 · único fármaco", 1100, 960, 40,')
open('mg_esc4.py', 'w', encoding='utf-8').write(e4)
print("ok")
