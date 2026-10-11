# -*- coding: utf-8 -*-
s = open('objetos.py', encoding='utf-8').read()
s = s.replace("def mar_capa(y, alt, col, semilla=0, ph=0.0, hilos=True):",
              "@lru_cache(maxsize=None)\ndef mar_capa(y, alt, col, semilla=0, ph=0.0, hilos=True):")
s = s.replace("def vapor(n=3):", "def vapor(n=3, sep=120):").replace("x = (i - (n - 1) / 2) * 120", "x = (i - (n - 1) / 2) * sep")
open('objetos.py', 'w', encoding='utf-8').write(s)

e = open('escenas.py', encoding='utf-8').read()
a = e.index("# ------------------------------------------------------------------ pases de la gota")
b = e.index("# ------------------------------------------------------------------ subtítulos manuscritos")
nuevo = open('_pases_nuevo.txt', encoding='utf-8').read()
e = e[:a] + nuevo + e[b:]
e = e.replace("GLASS_A = (740, 1040, 1.0, 0.0)", "GLASS_A = (713, 1040, 1.0, 0.0)")
a = e.index("    def mascota(self, t):")
b = e.index("    def expr(self, t):")
e = e[:a] + '''    def mascota(self, t):
        ps = self.pases
        if t < ps[0][0]:
            return ps[0][2](ps[0][0])
        k = max(i for i, p in enumerate(ps) if p[0] <= t)
        t0, t1, fn = ps[k]
        return fn(min(t, t1))

''' + e[b:]
a = e.index("    def dibujar_gota(self, t, te):")
b = e.index("    def lluvia(self, t, te):")
e = e[:a] + '''    def dibujar_gota(self, t, te):
        x, y, s, rot = self.mascota(t)
        ojos, boca = self.expr(t)
        if ojos == "abiertos" and ((te + 1.0) % 3.1) < 0.13:          # parpadeo cada 3,1 s
            ojos = "cerrados"
        y += 3.0 * math.sin(te * 2 * math.pi / 1.7)                    # balanceo de reposo
        if t_congela + 0.3 < t < t_rio:                                # tiembla de frío dentro del hielo
            x += (1 if self.fs == 1 else -1) * 3.0
        self.gota_dib(x, y, s, rot, t, ojos, boca)
        u_b = min(prog(t, t_tres, t_tres + 2.3), 1 - prog(t, INI("sol") + 0.1, INI("sol") + 0.9))
        if u_b > 0:
            O.barba().dibujar(self.h, x, y, s, rot, False, u_b, self.fs, 21)

''' + e[b:]
e = e.replace('e(t_hielo, "borrar" if False else "whoosh", 0.4, dur=0.6)', 'e(t_hielo, "whoosh", 0.4, dur=0.6)')
e = e.replace("""        self.act(O.pez(), lerp(-150, 1230, ((te * 0.02 + 0.2) % 1.0)) if False else 300 + 35 * math.sin(t * 0.8), 1360, 0.8, t,
                 t_mar + 1.2, 0.8, t_out=t_out, d_out=0.7, sem=17)""",
              """        self.act(O.pez(), 300 + 35 * math.sin(t * 0.8), 1360, 0.8, t, t_mar + 1.2, 0.8, t_out=t_out, d_out=0.7, sem=17)""")
e += "\n\nCLASES = {e[\"id\"]: Mundo for e in TL[\"escenas\"]}\n"
open('escenas.py', 'w', encoding='utf-8').write(e)
