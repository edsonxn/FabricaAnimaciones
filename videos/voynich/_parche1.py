# -*- coding: utf-8 -*-
"""Parche 1 de escenas.py: guion ampliado (fecha/duenos/intentos)."""
p = "escenas.py"
s = open(p, encoding="utf-8").read()

# ---------- anclas
a = s.index('f_med, f_falsif, f_moderna')
b = s.index('t_codigo, t_inventado')
anclas = '''f_med, f_falsif, f_moderna = T("fecha", "medieval", frase=2), T("fecha", "falsificacion", frase=2), T("fecha", "moderna", frase=2)
f_eamon, f_menos, f_ternero = T("fecha", "eamon", frase=3), T("fecha", "menos", frase=3), T("fecha", "ternero", frase=3)

d_rastro, d_pasado = T("duenos", "rastro", frase=0), T("duenos", "pasado", frase=0)
d_1639, d_georg, d_ayuda, d_sabio, d_kircher = (T("duenos", w, frase=1) for w in ("nueve", "georg", "ayuda", "sabio", "athanasius"))
d_respondio, d_quiso = T("duenos", "respondio", frase=2), T("duenos", "quiso", frase=2)
d_carta, d_emperador, d_rodolfo = T("duenos", "carta", frase=3), T("duenos", "emperador", frase=3), T("duenos", "rodolfo", frase=3)
d_600, d_ducados, d_oro = T("duenos", "seiscientos", frase=3), T("duenos", "ducados", frase=3), T("duenos", "oro", frase=3)

i_william, i_purpura, i_anos = T("intentos", "william", frase=0), T("intentos", "purpura", frase=0), T("intentos", "anos", frase=0)
i_copio, i_linea, i_tarjetas = T("intentos", "copio", frase=1), T("intentos", "linea", frase=1), T("intentos", "tarjetas", frase=1)
i_pudo, i_desc, i_lenguaje = T("intentos", "pudo", frase=2), T("intentos", "descifrarlo", frase=2), T("intentos", "lenguaje", frase=2)
i_artificial = T("intentos", "artificial", frase=2)
i_ruido, i_azar = T("intentos", "ruido", frase=3), T("intentos", "azar", frase=3)
i_patrones, i_idioma, i_real = T("intentos", "patrones", frase=4), T("intentos", "idioma", frase=4), T("intentos", "real", frase=4)
i_treinta, i_palabras, i_veinte, i_simbolos = (T("intentos", w, frase=5) for w in ("treinta", "palabras", "veinte", "simbolos"))

'''
s = s[:a] + anclas + s[b:]

s = s.replace('F0, F1, F2 = INI("fecha", 0), INI("fecha", 1), INI("fecha", 2)', 'F0, F1, F2, F3 = (INI("fecha", k) for k in range(4))')
s = s.replace('D0, D1 = INI("duenos", 0), INI("duenos", 1)', 'D0, D1, D2, D3 = (INI("duenos", k) for k in range(4))')
s = s.replace('I0, I1, I2, I3_ = INI("intentos", 0), INI("intentos", 1), INI("intentos", 2), INI("intentos", 3)',
              'I0, I1, I2, I3_, I4, I5 = (INI("intentos", k) for k in range(6))')

# ---------- tomas: desde 'fecha_medieval' hasta el tablero de teorías
a = s.index('@toma(F2 - PAD, D0 - 0.1')
b = s.index('# ================================================================== TEORÍAS')
tomas = open("_tomas_nuevas.py", encoding="utf-8").read()
s = s[:a] + tomas + s[b:]
s = s.replace('"f110", "Fraude", 500, -80, -3, t_fraude, "¿Falsificación?"', '"f110", "Fraude", 500, -80, -3, t_fraude, "¿Fraude medieval?"')
open(p, "w", encoding="utf-8").write(s)
print("ok")
