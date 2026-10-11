# -*- coding: utf-8 -*-
import re
# ---- boceto.py: union_circulos con ymax por círculo, texto más grueso
b = open('../../nucleo/boceto.py', encoding='utf-8').read()
b = b.replace('''    for i, (cx, cy, r) in enumerate(circulos):
        a = np.linspace(0, 2 * math.pi, n, endpoint=False)
        x, y = cx + r * np.cos(a), cy + r * np.sin(a)
        ok = y <= base_y
        for j, (qx, qy, qr) in enumerate(circulos):''', '''    for i, c in enumerate(circulos):
        cx, cy, r = c[:3]
        a = np.linspace(0, 2 * math.pi, n, endpoint=False)
        x, y = cx + r * np.cos(a), cy + r * np.sin(a)
        ok = y <= (c[3] if len(c) > 3 else base_y)         # 4.º valor opcional: y máxima del arco de ese círculo
        for j, (qx, qy, qr) in enumerate(c_ for c_ in [cc[:3] for cc in circulos]):''')
b = b.replace('''    ImageDraw.Draw(im).text((4, 2), txt, font=f, fill=255)''', '''    ImageDraw.Draw(im).text((4, 2), txt, font=f, fill=255, stroke_width=1 if px < 120 else 2, stroke_fill=255)''')
open('../../nucleo/boceto.py', 'w', encoding='utf-8').write(b)

o = open('objetos.py', encoding='utf-8').read()
o = o.replace("circulos = [(-190, 30, 85), (-85, -35, 105), (45, -55, 120), (175, -5, 95), (250, 55, 55)]",
              "circulos = [(-190, 30, 85, 95), (-85, -35, 105, -8), (45, -55, 120, -8), (175, -5, 95, 62), (250, 55, 55, 98)]")
o = o.replace("circulos = [(-70, 10, 50), (0, -30, 62), (72, 0, 52)]", "circulos = [(-70, 10, 50, 40), (0, -30, 62, -8), (72, 0, 52, 40)]")
o = o.replace("return curva([(-60, -560), (110, -380), (-130, -180), (120, 30), (-140, 250), (100, 470), (-20, 640)], 14)",
              "return curva([(-30, -560), (125, -300), (-125, -20), (120, 260), (-30, 640)], 20)")
o = o.replace("ancho = 78 + 18 * np.sin(np.linspace(0, 9, len(C)))", "ancho = 64 + 10 * np.sin(np.linspace(0, 7, len(C)))")
open('objetos.py', 'w', encoding='utf-8').write(o)

e = open('escenas.py', encoding='utf-8').read()
e = e.replace("GLASS_B = (400, 1215, 0.66, -0.95)", "GLASS_B = (392, 1195, 0.62, -0.95)")
e = e.replace("PERSONA = (290, 1160, 0.85)\nMOUTH = (290, 1228)", "PERSONA = (270, 1170, 0.85)\nMOUTH = (270, 1238)")
# el vaso se retira tras beber (borrar) y el aliento sale por encima de la cabeza
e = e.replace("self.act(O.vaso(), gx, gy, gs, t, INI(\"vaso\") + 0.15, 0.9, t_out=t_out, d_out=0.8, rot=gr, sem=11)",
              "self.act(O.vaso(), gx, gy, gs, t, INI(\"vaso\") + 0.15, 0.9, t_out=t_bebe_fin, d_out=0.5, rot=gr, sem=11)")
e = e.replace("uo = prog(t, t_out, t_out + 0.8)\n                if uo < 1:", "uo = prog(t, t_bebe_fin, t_bebe_fin + 0.5)\n                if uo < 1:")
e = e.replace("t_camino = T(\"vaso\", \"camino\")", "t_camino = T(\"vaso\", \"camino\")\nt_bebe_fin = t_ti + 1.45")
e = e.replace("SOP = (MOUTH[0] + 120, MOUTH[1] - 60)", "SOP = (MOUTH[0] + 190, MOUTH[1] - 190)")
e = e.replace("self.act(O.soplo(), MOUTH[0] + 130, MOUTH[1] - 65, 0.9,", "self.act(O.soplo(), MOUTH[0] + 200, MOUTH[1] - 195, 0.9,")
e = e.replace("O.mar_capa(1010, 560, B.AZUL_CL, ph=0.5)", "O.mar_capa(1010, 530, B.AZUL_CL, ph=0.5)")
e = e.replace("O.mar_capa(1120, 460, B.AZUL, ph=2.0)", "O.mar_capa(1120, 420, B.AZUL, ph=2.0)")
e = e.replace("PX_SUB = 60", "PX_SUB = 64")
open('escenas.py', 'w', encoding='utf-8').write(e)
