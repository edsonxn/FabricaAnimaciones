# -*- coding: utf-8 -*-
"""Tomas de EJEMPLO escritas a mano y verificadas a la vista (manual del agente: se le pasan como referencia).
Si editas una, vuelve a mirar su hoja: python estudio/agente_tomas.py --ejemplos"""
from kit_tomas import *  # noqa: F401,F403


class TomaCampo(TomaBase):
    """«En las faldas del volcán, los campesinos siembran maíz y café en una tierra negra y muy fértil.»
    Mundo: valle al pie de un volcán humeante. 4 capas: volcán lejano, colinas, milpa, primer plano con campesinos.
    Actos: (1) panorama con humo y aves; (2) en «siembran» los campesinos trabajan; (3) en «maíz» brotan las plantas."""
    CIELO = "amanecer"
    ZOOM = 0.07

    def preparar_toma(self):
        self.t_siembra = self.cuando("siembran", self.t0 + 1.0)
        self.t_maiz = self.cuando("maíz", self.t_siembra + 1.0)
        self.ev(self.t_maiz, "pop", 0.5)

    def escena(self, lz, t):
        # capa lejana: sol, volcán y su humo
        self.resplandor(lz, W * 0.78, H * 0.3, 260, (255, 210, 150), alfa=0.55)
        ox, oy = self.par(t, 0.1)
        vx, vy = W * 0.36 + ox, H * 0.62 + oy
        cono = [(vx - 520, vy + 60), (vx - 90, vy - 330), (vx + 90, vy - 330), (vx + 540, vy + 60)]
        lz.degradado(cono, (120, 96, 120), (70, 56, 84), (vx, vy - 330), (vx, vy + 60))
        lz.relleno([(vx - 90, vy - 330), (vx - 40, vy - 300), (vx + 10, vy - 322), (vx + 60, vy - 296), (vx + 90, vy - 330)],
                   (210, 200, 214))
        for i in range(6):                                   # humo que sube y se abre
            u = ((t * 0.18 + i / 6) % 1.0)
            lz.relleno(circulo(vx + 30 * math.sin(i + t * 0.4) + 140 * u, vy - 360 - 260 * u, 40 + 90 * u, 40),
                       (236, 226, 236), alfa=0.75 * (1 - u))
        self.nubes(lz, t, n=3, y0=H * 0.12, y1=H * 0.3, prof=0.15, color=(255, 236, 226))
        self.aves(lz, t, n=5, zona=(0, H * 0.18, W, H * 0.36), color=(90, 70, 110), s=0.9)
        # capas medias: colinas y milpa en terrazas
        self.montes(lz, t, H * 0.66, (96, 150, 96), prof=0.35, amp=50, seed=3)
        self.montes(lz, t, H * 0.68, (70, 128, 80), prof=0.55, amp=30, seed=8)
        crece = e_out(prog(t, self.t_maiz, self.t_maiz + 1.4))
        ox2, oy2 = self.par(t, 0.7)
        for fila in range(3):
            y = H * 0.72 + fila * 38 + oy2
            for j in range(14):
                x = 80 + j * 130 + (fila % 2) * 65 + ox2
                P.planta(lz, x, y, s=(0.25 + 0.2 * fila) * (0.3 + 0.7 * crece), t=t + j, col=(96, 196, 110))
        # primer plano: tierra negra y campesinos trabajando
        self.suelo(lz, t, Y_ACCION1 - 20, (70, 52, 60), prof=0.95)   # pies sobre el suelo, encima de la franja de etiquetas
        trabaja = t >= self.t_siembra
        for i, (x, tipo) in enumerate(((W * 0.24, "hombre"), (W * 0.5, "senora"), (W * 0.74, "nino"))):
            self.persona(lz, t + i * 0.5, x, Y_ACCION1 + 5, s=44 if tipo != "nino" else 34, tipo=tipo, vista="perfil",
                         brazos="labra" if trabaja else "idle", mirar=1 if i != 1 else -1, seed=i)
        self.particulas(lz, t, "polvo", n=24, zona=(0, H * 0.55, W, H), s=0.8)


class TomaHuida(TomaBase):
    """«En una semana, la grieta creció hasta formar un cerro de cien metros. El pueblo entero tuvo que huir.»
    Mundo: noche roja; el volcán nuevo crece en la milpa mientras el pueblo huye en fila hacia la izquierda.
    Actos: (1) la grieta brilla y el cerro crece con «creció»; (2) en «huir» la gente camina cargando cosas."""
    CIELO = "volcan"
    ZOOM = -0.05            # la cámara se aleja para mostrar el tamaño del cerro

    def preparar_toma(self):
        self.t_crece = self.cuando("creció", self.t0 + 0.8)
        self.t_huir = self.cuando("huir", self.frase(-1)[0])
        self.ev(self.t_crece, "impacto", 0.6)
        self.ev(self.t_huir, "whoosh", 0.5, pan=-0.4)

    def escena(self, lz, t):
        self.montes(lz, t, H * 0.6, (70, 40, 60), prof=0.15, amp=60, seed=2)
        alto = 120 + 340 * e_inout(prog(t, self.t_crece, self.t_crece + 2.5))
        ox, oy = self.par(t, 0.4)
        cx, base = W * 0.62 + ox, H * 0.76 + oy
        self.resplandor(lz, cx, base - alto, 220 + alto * 0.5, (255, 120, 60), alfa=0.6)
        cono = [(cx - alto * 1.5, base), (cx - 50, base - alto), (cx + 50, base - alto), (cx + alto * 1.5, base)]
        lz.degradado(cono, (90, 50, 60), (40, 24, 36), (cx, base - alto), (cx, base))
        for i in range(3):                                   # ríos de lava que bajan
            frac = prog(t, self.t_crece + 0.6 * i, self.t_crece + 2.0 + 0.6 * i)
            if frac > 0:
                pts = [(cx - 20 + 20 * i, base - alto + 10), (cx - 60 + 70 * i, base - alto * 0.5),
                       (cx - 140 + 150 * i, base - 10)]
                lz.trazo(catmull(pts, 10)[: max(2, int(30 * frac))], (255, 150, 60), ancho=12, temblor=0.0)
        self.particulas(lz, t, "chispas", n=26, zona=(cx - 200, base - alto - 300, cx + 200, base - alto), s=1.2)
        self.particulas(lz, t, "polvo", n=30, zona=(0, 0, W, H * 0.8), color=(120, 100, 110))   # ceniza
        self.suelo(lz, t, Y_ACCION1 - 40, (54, 34, 46), prof=0.85)
        for i in range(4):
            P.casa(lz, W * (0.08 + 0.1 * i) + self.par(t, 0.85)[0], Y_ACCION1 - 30, s=0.8, calor=0.4)
        if t >= self.t_huir - 0.3:
            for i in range(6):                               # fila de gente que huye
                x = W * 0.55 - 190 * i - 110 * (t - self.t_huir)
                self.persona(lz, t + 0.3 * i, x, Y_ACCION1 + 5, s=34 if i % 4 != 2 else 26, tipo=("hombre", "mujer", "nino", "senora")[i % 4],
                             piernas="camina", brazos="carga" if i % 2 else "balanceo", vista="perfil", mirar=-1,
                             emocion="miedo", seed=i)


TOMAS = {"p2": segura(TomaCampo), "p4": segura(TomaHuida)}
