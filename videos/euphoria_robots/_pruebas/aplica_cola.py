s = open("escenas.py", encoding="utf-8").read()
i = s.index("MOMENTOS = dict(")
s = s[:i] + '''from esc_cola import MOMENTOS, PLAN, T, momento_en, pinta  # noqa: E402,F401


class Mundo(Escena):
    def render(self, lz, t):
        t0, nombre = momento_en(t)
        img = pinta(lz, nombre, t - t0, t)
        u = t - t0                                   # destello corto en cada cambio de momento
        if u < 0.12 and t > 0.5:
            img = np.clip(img + (0.12 - u) / 0.12 * 0.35, 0, 1)
        return img


from escena_base import TL  # noqa: E402

CLASES = {e["id"]: Mundo for e in TL["escenas"]}
'''
R = [
    ('''    sim = D.escenario("trapo", 6.0)
    tt = max(0.0, u - 5.0)
    P = sim.en(tt) if u > 5.0 else D.escenario("leve").en(0.0 + 0.0 * u)''',
     '''    t1, t2 = ctx["k"]("verlet_1"), ctx["k"]("verlet_2", "trapo") - 0.6
    sim = D.escenario("trapo", 6.0)
    tt = max(0.0, u - t2)
    P = sim.en(tt) if u > t2 else D.escenario("leve").en(0.0)'''),
    ("if u < 2.2 or u > 5.0:", "if u < t1 or u > t2:"),
    ("W / 2, 780, u, 2.3)", "W / 2, 780, u, t1 + 0.1)"),
    ("if u > 2.2:                                   # fantasma", "if t1 < u < t2:                               # fantasma"),
    ("alfa=0.25 * D.suave(D.pr(u, 2.2, 2.6)) * (u < 5.0), t=u)", "alfa=0.25 * D.suave(D.pr(u, t1, t1 + 0.4)), t=u)"),
    ("P = P + [[dx * 0.2, 0]] * 1 if u <= 5.0 else P", "P = P + [[dx * 0.2, 0]]"),
    ("etiquetas=D.pr(u, 0.6, 2.0) * (u < 4.8), t=u)", "etiquetas=D.pr(u, 0.6, 2.0) * (u < t2 - 0.2), t=u)"),
    ("    if 2.4 < u < 5.0:\n", "    if t1 + 0.2 < u < t2:\n"),
    ("D.suave(D.pr(u, 2.6, 3.1)))", "D.suave(D.pr(u, t1 + 0.4, t1 + 0.9)))"),
    ("W / 2, 1010, u, 2.8, fondo=D.PAPEL, px=30)", "W / 2, 1010, u, t1 + 0.6, fondo=D.PAPEL, px=30)"),
    ('''    D.titular(lz, "32 > 21", 1660, u, 0.3, px=150, col=D.CORAL)''',
     '''    if ctx.get("teaser"):
        D.titular(lz, "¿¿NADIE LO TOCÓ??", 1660, u, 0.9, px=96, col=D.CORAL)
        return
    D.titular(lz, "32 > 21", 1660, u, 0.3, px=150, col=D.CORAL)'''),
    ('''    D.kicker(lz, "ERROR REAL · 5-NOV", W / 2, 250, u, 0.0, fondo=D.CORAL)
    sim = D.escenario("vuela")''',
     '''    if not ctx.get("teaser"):
        D.kicker(lz, "ERROR REAL · 5-NOV", W / 2, 250, u, 0.0, fondo=D.CORAL)
    sim = D.escenario("vuela")'''),
]
for a, b in R:
    assert a in s, a[:60]
    s = s.replace(a, b)
open("escenas.py", "w", encoding="utf-8").write(s)
print("cola aplicada")
