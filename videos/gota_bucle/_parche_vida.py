# -*- coding: utf-8 -*-
s = open('escenas.py', encoding='utf-8').read()


def rep(a, b, n=1):
    global s
    assert s.count(a) >= 1, a[:60]
    s = s.replace(a, b) if n == 0 else s.replace(a, b, n)


rep('FIN_CUADRO = TOTAL - 1.5 / 30      # desde aquí el temblor y el parpadeo vuelven a la fase 0 (= primer cuadro)',
    'FIN_CUADRO = TOTAL - 1.5 / 30      # desde aquí el temblor y el parpadeo vuelven a la fase 0 (= primer cuadro)\n'
    '# la "vida" (respiración, ondulación, giro del sol) usa ciclos ENTEROS en la duración total: el movimiento cierra el bucle\n'
    'B.OMEGA = 2 * math.pi * round(TOTAL / 1.85) / TOTAL\n'
    'B.GIRO_SOL = 2 * math.pi * 3 / TOTAL\n')
# A(): vida
rep('flip=False, rot=0.0, sfx=(), sfx_out=()):\n    """Registra un actor.', 'flip=False, rot=0.0, sfx=(), sfx_out=(), vida=1.0):\n    """Registra un actor.')
rep('flip=flip, rot=rot, snd=[])', 'flip=flip, rot=rot, snd=[], vida=vida)')
# nube y sol dinámicos
rep('A(R, O.sol(76), C0_SOL, -10, 0.1, t_out=t_nunca + 0.12', 'A(R, SOL, C0_SOL, -10, 0.1, t_out=t_nunca + 0.12')
rep('A(R, O.nube(), C0_NUBE, -10, 0.1, t_out=t_nunca', 'A(R, O.nube_din, C0_NUBE, -10, 0.1, t_out=t_nunca')
rep('A(R, O.nube(), C0_NUBE, t_hoy - 0.35', 'A(R, O.nube_din, C0_NUBE, t_hoy - 0.35')
rep('A(R, O.nube(), C0_NUBE, t_c, 0.55', 'A(R, O.nube_din, C0_NUBE, t_c, 0.55')
rep('A(R, O.sol(76), C0_SOL, t_c + 0.7', 'A(R, SOL, C0_SOL, t_c + 0.7')
rep('A(R, O.sol(76), (190, 700, 1.35), t_sol - 0.45', 'A(R, SOL, (190, 700, 1.35), t_sol - 0.45')
rep('def construir_actores():', 'def SOL(te):\n    return O.sol_din(76, te)\n\n\ndef construir_actores():')
rep('sfx=[("siseo", 0, 0.6, {"dur": 0.9})], sfx_out=[("borrar", 0, 0.4, {"dur": 0.3})])',
    'sfx=[("siseo", 0, 0.6, {"dur": 0.9})], sfx_out=[("borrar", 0, 0.4, {"dur": 0.3})], vida=2.6)')
rep('A(R, O.persona("sonrisa"), PERSONA, t_luego - 0.05, 0.4, "sube", dy=650, t_out=t_camino + 0.5, d_out=0.4, sale="baja", sem=14,\n      sfx=[("whoosh", 0, 0.4, {"dur": 0.4}), ("pop", 0.35, 0.7)])',
    'A(R, O.persona("sonrisa"), PERSONA, t_luego - 0.05, 0.4, "sube", dy=650, t_out=t_camino + 0.5, d_out=0.4, sale="baja", sem=14,\n      sfx=[("whoosh", 0, 0.4, {"dur": 0.4}), ("pop", 0.35, 0.7)], vida=1.5)')
# actor(): dibujo callable + vida
rep('        a["d"].dibujar(self.h, x, y, s, rot, a["flip"], u, self.fs, a["sem"], sq=sq, lapiz=lap)',
    '        d = a["d"](self.te) if callable(a["d"]) else a["d"]\n'
    '        d.dibujar(self.h, x, y, s, rot, a["flip"], u, self.fs, a["sem"], sq=sq, lapiz=lap, tv=self.te, vida=a["vida"])')
rep('        self.fs = B.fase(te)\n        for a in self.actores:', '        self.fs = B.fase(te)\n        self.te = te\n        for a in self.actores:')
rep('        self.fs = 0\n        if self.idx == 0:', '        self.fs = 0\n        self.te = 0.0\n        if self.idx == 0:')
# mascota: mira, respiración
rep('''    def gota_dib(self, x, y, s, rot, ojos, boca, sq=0.0):
        if s < 0.03:
            return
        O.gota(ojos, boca, True).dibujar(self.h, x, y, s, rot, False, 1.0, self.fs, 0, sq=sq)''',
    '''    def gota_dib(self, x, y, s, rot, ojos, boca, sq=0.0):
        if s < 0.03:
            return
        mira = int(round(1.2 * math.sin(B.OMEGA * self.te + 1.0)))          # mira a los lados
        O.gota(ojos, boca, True, False, mira).dibujar(self.h, x, y, s, rot, False, 1.0, self.fs, 0, sq=sq, tv=self.te, vida=0.8)''')
rep('        self.gota_dib(x, y, s, rot, ojos, boca, squash_gota(t))',
    '        self.gota_dib(x, y, s, rot, ojos, boca, squash_gota(t) + 0.045 * math.sin(2 * B.OMEGA * te + 0.6))')
rep('            O.barba().dibujar(self.h, x, y, s, rot, False, u_b, self.fs, 21)', '            O.barba().dibujar(self.h, x, y, s, rot, False, u_b, self.fs, 21, tv=te, vida=1.2)')
# rótulos que se mecen
rep('''def escribir(h, txt, x, y, px, u, fs, v=255):
    """Rotula `txt` centrado en (x, y), escribiéndose de izquierda a derecha (u 0..1)."""
    if u <= 0 or v <= 0:
        return
    m = B.mascara_texto(txt, px)
    h.pegar_mascara(m, x - m.shape[1] / 2 + (fs - 1) * 0.7, y - m.shape[0] / 2, cols=m.shape[1] * min(1.0, u), v=v)''',
    '''def escribir(h, txt, x, y, px, u, fs, v=255, tv=0.0):
    """Rotula `txt` centrado en (x, y), escribiéndose de izquierda a derecha (u 0..1); se mece siempre (nada queda quieto)."""
    if u <= 0 or v <= 0:
        return
    m = B.mascara_texto(txt, px)
    mx = 3.0 * math.sin(2 * B.OMEGA * tv + x * 0.01)
    my = 5.0 * math.sin(B.OMEGA * tv * 3 + y * 0.013)
    h.pegar_mascara(m, x - m.shape[1] / 2 + (fs - 1) * 0.7 + mx, y - m.shape[0] / 2 + my, cols=m.shape[1] * min(1.0, u), v=v)''')
s = s.replace('int(255 * (1 - prog(t, t_vueltas + 0.5, t_vueltas + 0.9))))', 'int(255 * (1 - prog(t, t_vueltas + 0.5, t_vueltas + 0.9))), te)')
s = s.replace('''                         int(255 * (1 - prog(t, t_meses + 0.4, t_meses + 0.7))))''', '''                         int(255 * (1 - prog(t, t_meses + 0.4, t_meses + 0.7))), te)''')
s = s.replace('escribir(h, "3000", 540, 430, 250, u, fs, int(255 * min(1.0, u * 4)))', 'escribir(h, "3000", 540, 430, 250, u, fs, int(255 * min(1.0, u * 4)), te)')
s = s.replace('''                         int(255 * (1 - uu * 0.4)))''', '''                         int(255 * (1 - uu * 0.4)), te)''')
# agua en movimiento
rep('        self.punteado(t)\n\n    def salpicadura', '        self.agua(t, te)\n        self.punteado(t)\n\n    def salpicadura')
rep('    def salpicadura(self, t, t0, x, y, n, dur, alt):', '''    def agua(self, t, te):
        """Agua que siempre corre: rayas que avanzan por el río y olas que viajan por el mar."""
        h, fs, w = self.h, self.fs, B.OMEGA
        u_r = _u_rio(t)
        if t_baja + 0.5 < t < t_meses + 0.6 and u_r > 0.3:
            k = 1 - prog(t, t_meses + 0.35, t_meses + 0.6)
            for i in range(9):
                uu = (te * 0.27 + i / 9.0) % 1.0
                if uu > u_r - 0.04:
                    continue
                p, q = O.punto_rio(uu), O.punto_rio(min(1.0, uu + 0.025))
                a = (RIO_TF[0] + p[0] * RIO_TF[2], RIO_TF[1] + p[1] * RIO_TF[2])
                b = (RIO_TF[0] + q[0] * RIO_TF[2], RIO_TF[1] + q[1] * RIO_TF[2])
                h.trazo(np.array([a, b]), 4.0, 400 + i, fs, 1.0, amp=1.0, v=int(200 * k))
        t_m = t_camino + 1.4
        uo = prog(t, t_levanta + 0.3, t_levanta + 1.0)
        if t_m + 0.7 < t and uo < 1:
            dy = 1300 * e_in(uo) + 700 * (1 - e_out(prog(t, t_m, t_m + 0.9)))
            for j, (yy, x0) in enumerate(((1075, 0), (1165, 90), (1260, 20), (1350, 140), (1440, 60))):
                for k in range(5):
                    x = (x0 + k * 230 + 60 * math.sin(w * te + j) + 45 * te * (1 if j % 2 else -1)) % 1200 - 60
                    xs = np.linspace(x, x + 110, 12)
                    ys = yy + dy + 9 * np.sin(xs / 58.0 + 2 * w * te + j * 1.3)
                    h.trazo(np.stack([xs, ys], 1), 3.6, 500 + j * 7 + k, fs, 1.0, amp=0.8, v=170)

    def salpicadura(self, t, t0, x, y, n, dur, alt):''')
open('escenas.py', 'w', encoding='utf-8').write(s)
print("ok")
