# -*- coding: utf-8 -*-
def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:90]
    return s.replace(old, new, 1)


k = open('kit_cp.py', encoding='utf-8').read()
i0 = k.index("        # marcas\n        pil = None")
i1 = k.index("        lz[:] = np.clip(out, 0, 1)\n    return f\n\n\n# ------------------------------------------------------------------ gráficos explicativos")
nuevo = '''        # marcas: primero los puntos, luego los nombres
        vis = []
        for (c, t0) in marcas:
            if t < t0:
                continue
            px_, py_ = np.array(proy(*CIUDADES[c])) * s + M[:, 2]
            if not (-80 < px_ < W + 80 and -80 < py_ < H + 80):
                continue
            u = e_back(prog(t, t0, t0 + 0.4))
            rad = int(20 * u * min(1.4, max(0.8, z ** 0.35)))
            cv2.circle(out, (int(px_), int(py_)), rad + 7, (0.02, 0.02, 0.02), -1, cv2.LINE_AA)
            cv2.circle(out, (int(px_), int(py_)), rad, tuple(v / 255.0 for v in CHART), -1, cv2.LINE_AA)
            vis.append((c, px_, py_, rad))
        if vis:
            pil = Image.fromarray((out * 255).clip(0, 255).astype(np.uint8))
            d = ImageDraw.Draw(pil)
            for c, px_, py_, rad in vis:
                d.text((px_, py_ - rad - 18), c, font=D.fuente("sans_l", 38), fill=(255, 255, 255), anchor="mb", stroke_width=4, stroke_fill=(0, 0, 0))
            out = np.asarray(pil).astype(np.float32) / 255.0
'''
k = k[:i0] + nuevo + k[i1:]
open('kit_cp.py', 'w', encoding='utf-8').write(k)

a = open('tomas_a.py', encoding='utf-8').read()
a = rep(a, '[N("15", 1480, 260, 250, A(Qn, 2, "quince")), R([("años", A(Qn, 2, "quince", 0.35))], 1480, 430, 70),',
        '[N("15", 1480, 260, 250, A(Qn, 2, "quince"), sal=A(Qn, 3, "mil", -0.2)), R([("años", A(Qn, 2, "quince", 0.35))], 1480, 430, 70, sal=A(Qn, 3, "mil", -0.2)),')
a = rep(a, 'TAG("Job Corps · Knoxville, Tennessee", 1500, 880,', 'TAG("Job Corps · Knoxville, Tennessee", 1330, 880,')
a = rep(a, 'F_clip("wbir_cronologia", ini=301.3, fin=304.7, z0=1.0, z1=1.1, c0=(0.5, 0.45), c1=(0.5, 0.45)),\n     [N("19", 1520, 420, 330, A(Co, 1, "diecinueve")), R([("años", A(Co, 1, "diecinueve", 0.3))], 1520, 600, 74)],',
        'F_arch("wbir_cronologia", ini=301.3, fin=304.7, x_cont=(0.0, 1.0), alto=800, z0=1.0, z1=1.07, dx=-230, bg=0.34),\n     [N("19", 1500, 420, 330, A(Co, 1, "diecinueve")), R([("años", A(Co, 1, "diecinueve", 0.3))], 1500, 610, 74)],')
a = rep(a, 'F_clip("wbir_cronologia", ini=301.3, fin=304.7, z0=1.08, z1=1.0, c0=(0.5, 0.46), c1=(0.5, 0.46), tono=(0.8, 0.8, 0.86), sat=0.12)',
        'F_arch("wbir_cronologia", ini=301.3, fin=304.7, x_cont=(0.0, 1.0), alto=820, z0=1.06, z1=1.0, tono=(0.82, 0.82, 0.88), sat=0.12, bg=0.28)')
open('tomas_a.py', 'w', encoding='utf-8').write(a)
print('ok')
