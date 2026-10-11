# -*- coding: utf-8 -*-
"""Parche: anclar rótulos del pueblo, llenar el plano final y rehacer 1804 en dos tomas (decreto + dinero hacia Europa)."""
p = 't02.py'
s = open(p, encoding='utf-8').read()

# --- anclar rótulos del pueblo a sus grupos y llenar el plano final
a = s.index("    base_x, base_y = ibajo.P(OFF, OFF, 70)")
b = s.index("def _icono(lz, x, y, s, tip):")
nuevo = open('_parche_t02a_pueblo.txt', encoding='utf-8').read()
s = s[:a] + nuevo + s[b:]
s = s.replace("(t_minas2 + 0.9, (OFF, OFF, Z_BAJO + 330, 0.62)), (T_PREG, (OFF, OFF, Z_BAJO + 450, 0.56))", "(t_minas2 + 0.9, (OFF, OFF, Z_BAJO + 330, 0.80)), (T_PREG, (OFF, OFF, Z_BAJO + 450, 0.72))")

# --- 1804: dos tomas
a = s.index("# ------------------------------------------------------------------------------------------------ 5. 1804: EL DECRETO")
b = s.index("def _bolsa(lz, iso, x, y, z, i):")
nuevo = open('_parche_t02a_deudas.txt', encoding='utf-8').read()
s = s[:a] + nuevo + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('ok')
