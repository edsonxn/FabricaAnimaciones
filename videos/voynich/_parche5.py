# -*- coding: utf-8 -*-
"""Parche 5: versión de ~2 min (sin Duffy/pieles, Baresch/Kircher, tarjetas perforadas ni cifras). La versión larga queda en escenas_largo.py."""
import re

s = open("escenas.py", encoding="utf-8").read()


def corta(desde, hasta, nuevo=""):
    global s
    a = s.index(desde)
    b = s.index(hasta, a)
    s = s[:a] + nuevo + s[b:]


# ---------------- anclas
s = s.replace('f_eamon, f_menos, f_ternero = T("fecha", "eamon", frase=3), T("fecha", "menos", frase=3), T("fecha", "ternero", frase=3)\n', "")
corta('d_1639, d_georg, d_ayuda, d_sabio, d_kircher', 'i_william, i_purpura', '''d_carta, d_emperador, d_rodolfo = T("duenos", "carta", frase=1), T("duenos", "emperador", frase=1), T("duenos", "rodolfo", frase=1)
d_600, d_ducados, d_oro = T("duenos", "seiscientos", frase=1), T("duenos", "ducados", frase=1), T("duenos", "oro", frase=1)

''')
corta('i_copio, i_linea, i_tarjetas', 't_codigo, t_inventado', '''i_pudo, i_desc, i_lenguaje = T("intentos", "pudo", frase=1), T("intentos", "descifrarlo", frase=1), T("intentos", "lenguaje", frase=1)
i_artificial = T("intentos", "artificial", frase=1)
i_ruido, i_azar = T("intentos", "ruido", frase=2), T("intentos", "azar", frase=2)
i_patrones, i_idioma, i_real = T("intentos", "patrones", frase=3), T("intentos", "idioma", frase=3), T("intentos", "real", frase=3)

''')
s = s.replace('F0, F1, F2, F3 = (INI("fecha", k) for k in range(4))', 'F0, F1, F2 = (INI("fecha", k) for k in range(3))')
s = s.replace('D0, D1, D2, D3 = (INI("duenos", k) for k in range(4))', 'D0, D1 = (INI("duenos", k) for k in range(2))')
s = s.replace('I0, I1, I2, I3_, I4, I5 = (INI("intentos", k) for k in range(6))',
              'I0, I2, I3_, I4 = (INI("intentos", k) for k in range(4))     # Friedman, fracaso, ruido, Zipf\nI5 = INI("teorias", 0)')

# ---------------- tomas de fecha: la de 'medieval' termina en D0; se elimina la de pieles
s = s.replace('@toma(F2 - PAD, F3 - 0.1, ent=("desenfoque", 0.4), grado=dict(fuerza_vineta=0.7))', '@toma(F2 - PAD, D0 - 0.1, ent=("desenfoque", 0.4), grado=dict(fuerza_vineta=0.7))')
s = s.replace('D.foto_parallax(lz, HD("f001"), tl, F3 - F2 + 0.6, 1.5, 2.0,', 'D.foto_parallax(lz, HD("f001"), tl, D0 - F2 + 0.6, 1.5, 2.0,')
corta('def _piel(k):', '# ================================================================== DUEÑOS')

# ---------------- dueños
corta('@toma(D1 - PAD, d_sabio - 0.12', '# ================================================================== INTENTOS', '''@toma(D1 - PAD, d_emperador - 0.12, ent=("latigo", 0.35), grado=dict(calido=0.08))
def t_duenos_carta(lz, t):
    tl = t - (D1 - PAD)
    D.foto_parallax(lz, "kircher", tl, d_emperador - D1 + 0.5, 1.06, 1.28, (0.5, 0.35), (0.5, 0.3), par=(60, 10), tono=(0.85, 0.82, 0.75))
    D.tag_nombre(lz, "Carta a Athanasius Kircher", 1330, 900, t, d_carta - 0.05, 46)
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("duenos", 1, 1, 5), W / 2, 985, 84), t, "serif", 84)


@toma(d_emperador - PAD, I0 - 0.1, ent=("latigo", 0.35), grado=dict(calido=0.07))
def t_duenos_rodolfo(lz, t):
    tl = t - (d_emperador - PAD)
    D.foto_parallax(lz, "rodolfo_arcimboldo", tl, I0 - d_emperador + 0.6, 1.02, 1.22, (0.5, 0.42), (0.5, 0.36), par=(80, 10), tono=(0.9, 0.86, 0.8))
    sombra_lateral(lz, "izq", 0.5)
    D.tag_nombre(lz, "Rodolfo II", 500, 260, t, d_rodolfo - 0.05, 56)
    D.numero(lz, "600", 470, 520, 240, t, d_600 - 0.05, color=RJ, fnt="abril", salida=None)
    carta(lz, pola("ducado", 380, 0.8, (0.3, 0.5)), I3, t, d_ducados - 0.1, 1560, 690, 5, desde=(300, 300))
    D.dibujar_bloque(lz, bloque([("Ducados", d_ducados), ("De", T("duenos", "de", frase=1, n=1)), ("Oro", d_oro)], 470, 700, 92, lineas=(1,)), t, "serif", 92)


''')

# ---------------- intentos
s = s.replace('@toma(I0 - PAD, I1 - 0.1, ent=("desenfoque", 0.45), grado=dict(sat=0.7))', '@toma(I0 - PAD, I2 - 0.1, ent=("desenfoque", 0.45), grado=dict(sat=0.7))')
s = s.replace('D.foto_parallax(lz, "friedman", tl, I1 - I0 + 0.6,', 'D.foto_parallax(lz, "friedman", tl, I2 - I0 + 0.6,')
corta('def _linea_eva(k):', '@toma(I2 - PAD, I3_ - 0.1, ent=("latigo", 0.35))')
s = s.replace('kar("intentos", 2, 0, 3), 1400, 300, 90', 'kar("intentos", 1, 0, 3), 1400, 300, 90')
s = s.replace('kar("intentos", 3, 7, 12)', 'kar("intentos", 2, 7, 12)')
s = s.replace('kar("intentos", 4, 5, 12)', 'kar("intentos", 3, 5, 12)')
corta('@toma(I5 - PAD, T0 - 0.1, ent=("desenfoque", 0.4), grado=dict(fuerza_vineta=0.8))', '# ================================================================== TEORÍAS')

# ---------------- sonidos
corta('        n_p = 14', '        e(i_william, "papel", 0.5)', '        e(d_rastro, "viento", 0.35, dur=1.4)\n        e(d_carta - 0.05, "papel", 0.45)\n        e(d_rodolfo, "campana", 0.35)\n        e(d_600 - 0.05, "impacto", 0.55)\n        e(d_ducados, "clink", 0.5)\n')
corta('        for ti in (i_copio, i_linea, i_tarjetas):', '        for k in range(3):\n            e(i_pudo', "")
s = s.replace('        e(i_treinta - 0.1, "escribir", 0.4, dur=1.4)\n        e(i_veinte - 0.1, "impacto", 0.5)\n', "")
open("escenas.py", "w", encoding="utf-8").write(s)
print("ok")
