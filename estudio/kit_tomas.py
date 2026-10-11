# -*- coding: utf-8 -*-
"""Kit de TOMAS CREATIVAS del Estudio (estilo Kurzgesagt ilustrado, horizontal y vertical).

La IA (agente_tomas.py) escribe una clase `TomaXX(TomaBase)` por parte del guion usando SOLO lo que hay aquí,
`plano.py` (P), los personajes 2D de `kz_pers2d.py` (K) y las utilidades de animación de `motor`/`escena_base`.
TomaBase ya resuelve lo repetitivo para que el código generado se concentre en la composición y la acción:
  - fondo por preset (`CIELO = "atardecer"`), cámara con deriva + zoom lento, paralaje por profundidad (`prof`);
  - rótulo arriba, etiquetas (claves) abajo y la cifra (si no la coloca la toma) — franjas reservadas;
  - ayudantes de mundo: montes, suelo, agua, ciudad, árboles, nubes, aves, partículas, personas y multitudes;
  - `self.cuando("palabra", defecto)` = segundo en que se dice esa palabra (nunca lanza error).
`segura(clase, firma)` envuelve una toma: si el guion cambió o la toma truena al dibujar, se usa la plantilla
`LibrePlano` (nunca queda un cuadro negro). Con ESTUDIO_TOMA_ESTRICTO=1 los errores se propagan (para probar).
"""
import math
import os

import numpy as np

import fondos as F
import plano as P
import kz_pers2d as K
from escena_base import (BLANCO, Escena, circulo, e_in, e_inout, e_out, lerp, partir_lineas, pop, prog, sale,
                         env_bombo)
from motor import W, H, ancho_texto, rect_red, elipse, estrella, blob, bezier, catmull, e_back, e_elastic, h01, ruido1
from escenas_pro_plano import _BasePlano, LibrePlano, IntroPlano, CierrePlano, FUENTE, dibujar_elemento_plano

VERT = H > W
CX, CY = W / 2, H / 2
# Franjas reservadas: arriba rótulo/cifra, abajo etiquetas. La acción va entre Y_ACCION0 y Y_ACCION1.
BANDA = 330 if VERT else 175
Y_ACCION0, Y_ACCION1 = BANDA, H - BANDA
ESTRICTO = os.environ.get("ESTUDIO_TOMA_ESTRICTO") == "1"
SFX_OK = ("pop", "whoosh", "impacto", "brillo", "aparicion", "viento", "pasos", "latido", "fuego", "ola", "burbujas",
          "campana", "tick", "zap", "puf", "chapuzon", "eco", "revelar", "ding", "golpe_suave", "zoom_whoosh")

CIELOS = {
    "dia": ((0.36, 0.62, 0.96), (0.78, 0.90, 1.0)),
    "atardecer": ((0.30, 0.20, 0.52), (1.0, 0.62, 0.42)),
    "amanecer": ((0.42, 0.56, 0.92), (1.0, 0.80, 0.62)),
    "noche": ((0.04, 0.06, 0.20), (0.16, 0.18, 0.42)),
    "oceano": ((0.10, 0.42, 0.72), (0.02, 0.10, 0.30)),
    "abismo": ((0.03, 0.10, 0.26), (0.0, 0.02, 0.08)),
    "interior": ((0.95, 0.86, 0.72), (0.80, 0.62, 0.50)),
    "laboratorio": ((0.16, 0.22, 0.34), (0.30, 0.40, 0.55)),
    "bosque": ((0.50, 0.78, 0.86), (0.82, 0.94, 0.80)),
    "desierto": ((0.50, 0.70, 0.95), (1.0, 0.86, 0.62)),
    "volcan": ((0.18, 0.06, 0.10), (0.62, 0.20, 0.10)),
    "hielo": ((0.62, 0.80, 0.96), (0.92, 0.97, 1.0)),
}


def mezcla(c1, c2, u):
    return P.mezcla(c1, c2, max(0.0, min(1.0, u)))


class TomaBase(_BasePlano):
    """Base de las tomas creativas. La toma implementa `preparar_toma()` y `escena(lz, t)`."""
    CIELO = "espacio"          # espacio | espacio2 | dia | atardecer | amanecer | noche | oceano | abismo | interior |
                               # laboratorio | bosque | desierto | volcan | hielo
    ZOOM = 0.06                # cuánto se acerca la cámara a lo largo de la toma (0 = nada; negativo = se aleja)
    DERIVA = 1.0               # amplitud de la deriva lateral (0 = cámara fija)

    # ------------------------------------------------------------------ ciclo de vida
    def preparar(self):
        self._dibujo_cifra = False
        self.preparar_comun()
        self.preparar_toma()

    def preparar_toma(self):
        pass

    def escena(self, lz, t):
        pass

    def dibujar(self, lz, t):
        self._dibujo_cifra = False
        self.escena(lz, t)
        if not self._dibujo_cifra:
            self.cifra(lz, t, CX, BANDA + (120 if VERT else 90), px=170 if VERT else 150)
        self.dibujar_claves(lz, t)
        self.rotulo(lz, t)

    def ev(self, t, nombre, vol=1.0, pan=0.0, **kw):
        """Efecto de sonido en el segundo t (nombres de SFX_OK; otro nombre => «pop»)."""
        Escena.ev(self, t, nombre if nombre in SFX_OK else "pop", max(0.0, min(1.0, float(vol))),
                  max(-1.0, min(1.0, float(pan))), **{k: v for k, v in kw.items() if k in ("dur", "tono")})

    # ------------------------------------------------------------------ tiempo
    @property
    def dur(self):
        return self.t1 - self.t0

    def u(self, t):
        """Avance 0..1 de la toma."""
        return max(0.0, min(1.0, (t - self.t0) / max(0.01, self.dur)))

    def cuando(self, palabra, defecto=None, desde=0):
        """Segundo en que se dice `palabra` (la primera que coincida). Si no está, `defecto` (o t0 + 0.5)."""
        d = self.t0 + 0.5 if defecto is None else defecto
        if not palabra:
            return d
        try:
            return self.w(str(palabra).split()[0], desde=desde)
        except (KeyError, IndexError):
            return d

    def frase(self, i):
        """(t0, t1) de la frase i de esta parte (i negativo cuenta desde el final)."""
        if not self.fr:
            return self.t0, self.t1
        f = self.fr[max(-len(self.fr), min(len(self.fr) - 1, i))]
        return f["t0"], f["t1"]

    def k(self, t, ta, dur=0.4, salida=True):
        """Envolvente de aparición con rebote (0..1) desde ta; se apaga al final de la toma."""
        v = pop(t, ta, dur)
        return v * sale(t, self.t1 - 0.2, 0.2) if salida else v

    # ------------------------------------------------------------------ fondo y cámara
    def fondo(self, t):
        c = self.CIELO
        if c in ("espacio", "espacio2"):
            return F.espacio(t, tono=1 if c == "espacio2" else 0)
        arriba, abajo = CIELOS.get(c, CIELOS["dia"])
        return F.degradado(t, arriba=arriba, abajo=abajo)

    def camara(self, t):
        u = t - self.t0
        z = 1.02 + self.ZOOM * e_inout(self.u(t))
        a = self.DERIVA
        return (z, 0.003 * a * math.sin(u * 0.3 + self.idx),
                18 * a * math.sin(u * 0.22 + self.idx), 10 * a * math.cos(u * 0.27 + self.idx))

    def par(self, t, prof):
        """Desplazamiento de paralaje (ox, oy) para una capa a profundidad prof (0 = horizonte, 1 = primer plano)."""
        _, _, dx, dy = self.camara(t)
        f = 1.0 - max(0.0, min(1.0, prof))
        return -dx * f * 1.6, -dy * f * 1.6

    # ------------------------------------------------------------------ textos
    def cifra(self, lz, t, x, y, px=150, color=(110, 230, 255)):
        """La cifra del guion (si hay), en (x, y). Llamarla desde escena() para colocarla donde convenga."""
        self._dibujo_cifra = True
        if self.t_cifra is None:
            return
        k = pop(t, self.t_cifra, 0.4) * sale(t, self.t1 - 0.25, 0.25)
        if k > 0:
            txt = str(self.d["cifra"])[:14]
            px = min(px, int((W * 0.8) / max(1, ancho_texto(txt, FUENTE, 100)) * 100))
            with lz.capa(2):
                P.rotulo(lz, x, y, txt, px=px, k=k * (1 + 0.03 * env_bombo(t)), color=color, fuente=FUENTE)

    def etiqueta(self, lz, x, y, texto, k, px=34, fondo=(255, 255, 255), color=(30, 25, 60)):
        if k > 0:
            P.pastilla(lz, x, y, str(texto)[:26], px=px, k=k, fondo=fondo, color=color, fuente=FUENTE)

    def contador(self, lz, t, x, y, desde, hasta, ta, dur=1.2, px=90, sufijo="", color=BLANCO):
        """Número que cuenta de `desde` a `hasta` empezando en ta."""
        k = self.k(t, ta, 0.3)
        if k <= 0:
            return
        v = lerp(desde, hasta, e_out(prog(t, ta, ta + dur)))
        txt = f"{int(round(v)):,}".replace(",", ".") + sufijo
        P.rotulo(lz, x, y, txt, px=px, k=k, color=color, fuente=FUENTE)

    def dibujar_claves(self, lz, t):
        """Etiquetas de las claves en la franja de abajo, repartidas."""
        n = len(self.claves)
        for i, (tc, texto, _) in enumerate(self.claves):
            k = pop(t, tc, 0.3) * sale(t, self.t1 - 0.2, 0.2)
            if k <= 0:
                continue
            if VERT:
                x, y = CX, H - BANDA * 0.55 - 100 * (n - 1 - i)
            else:
                x, y = (CX if n == 1 else lerp(W * 0.3, W * 0.7, i / max(1, n - 1))), H - BANDA * 0.5
            P.pastilla(lz, x, y + 5 * math.sin(t * 1.8 + i), texto, px=38 if VERT else 34, k=k,
                       fondo=(235, 240, 255), color=(30, 25, 60), fuente=FUENTE)

    # ------------------------------------------------------------------ mundo (capas con paralaje)
    def montes(self, lz, t, y, color, prof=0.2, amp=70, seed=1, picos=False, capa=0):
        """Cordillera/colinas que llenan el ancho desde la altura y hacia abajo (prof = profundidad para paralaje)."""
        ox, oy = self.par(t, prof)
        xs = np.linspace(-260, W + 260, 90)
        fr = 0.004 if not picos else 0.009
        ys = y + amp * (0.6 * ruido1(xs * fr, seed) + 0.4 * ruido1(xs * fr * 2.3, seed + 7))
        if picos:
            ys = ys - amp * 0.5 * np.abs(np.sin(xs * 0.006 + seed))
        pts = np.concatenate([np.stack([xs + ox, ys + oy], 1), [[W + 260 + ox, H + 300], [-260 + ox, H + 300]]])
        with lz.capa(capa):
            lz.degradado(pts, P.aclarar(color, 0.12), P.oscurecer(color, 0.18), (0, y - amp), (0, y + 420))

    def suelo(self, lz, t, y, color, prof=0.8, amp=14, seed=4, capa=0):
        """Terreno del primer plano (casi plano) con borde de luz."""
        ox, oy = self.par(t, prof)
        xs = np.linspace(-260, W + 260, 70)
        ys = y + amp * ruido1(xs * 0.006, seed)
        top = np.stack([xs + ox, ys + oy], 1)
        pts = np.concatenate([top, [[W + 260 + ox, H + 300], [-260 + ox, H + 300]]])
        with lz.capa(capa):
            lz.degradado(pts, color, P.oscurecer(color, 0.25), (0, y), (0, H))
            borde = np.concatenate([top, (top + [0, 10])[::-1]])
            lz.relleno(borde, P.aclarar(color, 0.18), alfa=0.8)

    def agua(self, lz, t, y, color=(40, 120, 210), prof=0.7, olas=1.0, capa=0):
        """Mar/lago desde la altura y hacia abajo, con oleaje y reflejos."""
        ox, oy = self.par(t, prof)
        xs = np.linspace(-260, W + 260, 120)
        ys = y + 8 * olas * np.sin(xs * 0.012 + t * 1.6) + 5 * olas * np.sin(xs * 0.031 - t * 2.3)
        pts = np.concatenate([np.stack([xs + ox, ys + oy], 1), [[W + 260 + ox, H + 300], [-260 + ox, H + 300]]])
        with lz.capa(capa):
            lz.degradado(pts, P.aclarar(color, 0.15), P.oscurecer(color, 0.45), (0, y), (0, H))
            for i in range(7):
                yy = y + 40 + i * (H - y) / 8
                x0 = (h01(i, 3) * W + 30 * t * (1 + i * 0.2)) % (W + 400) - 200 + ox
                lz.relleno(rect_red(x0, yy + oy, 120 + 60 * h01(i, 5), 6, 3), P.aclarar(color, 0.35), alfa=0.5)

    def ciudad(self, lz, t, y, n=14, prof=0.5, color=(70, 80, 140), ventanas=(255, 214, 120), alto=(90, 300), seed=0,
               x0=-100, x1=None, capa=0):
        """Silueta de edificios con ventanas encendidas (base en y)."""
        ox, oy = self.par(t, prof)
        x1 = W + 100 if x1 is None else x1
        anchos = [(x1 - x0) / n] * n
        x = x0
        with lz.capa(capa):
            for i in range(n):
                w = anchos[i] * (0.75 + 0.25 * h01(i, seed))
                h = lerp(alto[0], alto[1], h01(i, seed + 1))
                lz.relleno(rect_red(x + ox, y - h + oy, w, h + 400, 6), mezcla(color, (255, 255, 255), 0.05 * (i % 3)))
                if ventanas:
                    for r in range(int(h // 44)):
                        for c in range(max(1, int(w // 34))):
                            if h01(i, r, c + seed) > 0.45:
                                on = 0.6 + 0.4 * math.sin(t * 0.7 + i + r * 1.3 + c)
                                lz.relleno(rect_red(x + 10 + c * 34 + ox, y - h + 18 + r * 44 + oy, 14, 20, 3),
                                           ventanas, alfa=0.5 + 0.5 * on)
                x += anchos[i]

    def arboles(self, lz, t, y, n=6, x0=0, x1=None, s=0.7, prof=0.6, hojas=(80, 176, 100), seed=0, capa=0):
        ox, oy = self.par(t, prof)
        x1 = W if x1 is None else x1
        with lz.capa(capa):
            for i in range(n):
                x = lerp(x0, x1, (i + 0.5) / n) + 40 * (h01(i, seed) - 0.5)
                P.arbol(lz, x + ox, y + oy, s=s * (0.8 + 0.4 * h01(i, seed + 2)), t=t + i, hojas=hojas, seed=i + seed)

    def nubes(self, lz, t, n=4, y0=None, y1=None, prof=0.25, color=(255, 255, 255), alfa=0.92, vel=16, s=1.0, seed=0,
              capa=0):
        """Nubes redondeadas que cruzan despacio."""
        ox, oy = self.par(t, prof)
        y0 = Y_ACCION0 * 0.6 if y0 is None else y0
        y1 = H * 0.4 if y1 is None else y1
        with lz.capa(capa):
            for i in range(n):
                sc = s * (0.7 + 0.6 * h01(i, seed))
                x = (h01(i, seed + 1) * (W + 600) + vel * (0.5 + prof) * t) % (W + 600) - 300 + ox
                y = lerp(y0, y1, h01(i, seed + 2)) + oy
                for j, (dx, dy, r) in enumerate(((0, 0, 60), (-70, 18, 44), (70, 16, 48), (30, -30, 46))):
                    lz.relleno(circulo(x + dx * sc, y + dy * sc, r * sc, 40), color, alfa=alfa)

    def aves(self, lz, t, n=4, zona=None, color=(40, 44, 80), s=1.0, vel=60, seed=0, capa=2):
        """Bandada lejana: pájaros en V que aletean y cruzan."""
        x0, y0, x1, y1 = zona or (0, Y_ACCION0, W, H * 0.4)
        with lz.capa(capa):
            for i in range(n):
                x = x0 + ((h01(i, seed) * (x1 - x0) + vel * t * (0.8 + 0.4 * h01(i, seed + 1))) % (x1 - x0 + 200)) - 100
                y = lerp(y0, y1, h01(i, seed + 2)) + 8 * math.sin(t * 1.3 + i)
                a = 0.5 * math.sin(t * 9 + i * 1.7)
                e = 18 * s
                pts = [(x - e, y - e * (0.4 + a)), (x - e * 0.3, y - e * 0.1), (x, y), (x + e * 0.3, y - e * 0.1),
                       (x + e, y - e * (0.4 + a))]
                lz.trazo(pts, color, ancho=4 * s, temblor=0.0)

    def particulas(self, lz, t, tipo="polvo", n=40, zona=None, color=None, s=1.0, seed=0, capa=2):
        """Ambiente continuo. tipo: polvo | burbujas | chispas | nieve | luciernagas | estrellas | lluvia | esporas."""
        x0, y0, x1, y1 = zona or (0, 0, W, H)
        ww, hh = max(1, x1 - x0), max(1, y1 - y0)
        col = color or dict(polvo=(255, 240, 210), burbujas=(200, 240, 255), chispas=(255, 170, 70),
                            nieve=(255, 255, 255), luciernagas=(255, 240, 120), estrellas=(255, 255, 230),
                            lluvia=(190, 210, 255), esporas=(180, 255, 200)).get(tipo, (255, 255, 255))
        vy = dict(polvo=-8, burbujas=-70, chispas=-90, nieve=45, luciernagas=-6, estrellas=0, lluvia=900, esporas=-15).get(tipo, 0)
        with lz.capa(capa):
            for i in range(n):
                a, b, c = h01(i, seed), h01(i, seed + 1), h01(i, seed + 2)
                x = x0 + (a * ww + 14 * math.sin(t * (0.6 + c) + i)) % ww
                y = y0 + (b * hh + vy * t * (0.6 + 0.8 * c)) % hh
                r = s * (2 + 4 * c) * (2.2 if tipo == "burbujas" else 1)
                if tipo == "lluvia":
                    lz.relleno(rect_red(x, y, 3 * s, 28 * s, 1.5), col, alfa=0.55)
                    continue
                if tipo in ("luciernagas", "chispas", "estrellas"):
                    tw = 0.5 + 0.5 * math.sin(t * (3 + 3 * c) + i * 2.1)
                    lz.halo(x, y, r * 5, col, alfa=0.35 * tw)
                    lz.relleno(circulo(x, y, r * (0.6 + 0.4 * tw), 12), col, alfa=0.9)
                elif tipo == "burbujas":
                    lz.relleno(circulo(x, y, r, 20), col, alfa=0.28)
                    lz.relleno(circulo(x - r * 0.35, y - r * 0.35, r * 0.28, 10), (255, 255, 255), alfa=0.8)
                else:
                    lz.relleno(circulo(x, y, r, 12), col, alfa=0.45 + 0.3 * c)

    def resplandor(self, lz, x, y, r, color=(255, 220, 140), alfa=0.6, capa=0):
        """Luz suave (sol tras montes, lámpara, brillo de un objeto)."""
        lz.halo(x, y, r, color, alfa=alfa, capa=capa)

    # ------------------------------------------------------------------ gente
    def persona(self, lz, t, x, y, s=30, tipo="hombre", piernas="idle", brazos="balanceo", mirar=1, vista="frente",
                emocion="neutro", objetivo=None, seed=0, alfa=1.0, lean=0.0):
        """Personaje de cuerpo entero con pies en (x, y). s ≈ 30 => ~ 300 px de alto (horizontal).
        tipo: hombre | mujer | nino | senora | comerciante | soldado | capitan | fraile | revolucionario | danzante | ...
        piernas: idle | camina | corre | baila | arrodillado | sentado.
        brazos: balanceo | idle | señala | arriba | saluda | carga | baila | defensa | pecho.
        vista: frente | perfil (para caminar) | tres. mirar: 1 derecha / -1 izquierda. objetivo=(x,y) si brazos='señala'.
        emocion: neutro | alegre | serio | sorpresa | miedo | enojo | triste | pensativo | grito."""
        K.cuerpo(lz, x, y, s, tipo if tipo in K.TIPOS else "hombre", t, piernas=piernas, brazos=brazos, mirar=mirar,
                 vista=vista, seed=seed, alfa=alfa, emocion=emocion, objetivo=objetivo, lean=lean)

    def multitud(self, lz, t, x0, x1, y, n=8, s=22, tipos=("hombre", "mujer", "nino", "senora"), piernas="idle",
                 brazos="idle", vista="frente", seed=0):
        """Fila de gente con ritmo propio (cada uno se mueve distinto)."""
        for i in range(n):
            x = lerp(x0, x1, (i + 0.5) / n) + 18 * (h01(i, seed) - 0.5)
            yy = y + 10 * h01(i, seed + 3)
            K.cuerpo(lz, x, yy, s * (0.9 + 0.2 * h01(i, seed + 1)), tipos[i % len(tipos)], t + 0.37 * i,
                     piernas=piernas, brazos=brazos, mirar=1 if h01(i, seed + 4) > 0.5 else -1, vista=vista,
                     seed=i + seed, cara="minima")

    def busto(self, lz, t, x, y, s=120, tipo="mujer", emocion="neutro", habla=0.0, yaw=-0.45, mirar=(0.0, 0.0)):
        """Primer plano de un personaje (cabeza y hombros); (x, y) = base del cuello; s ≈ 120 => cabeza ~290 px."""
        K.busto(lz, x, y, s, tipo if tipo in K.TIPOS else "mujer", t, yaw=yaw, emocion=emocion, habla=habla, mirar=mirar)

    # ------------------------------------------------------------------ gráficos
    def flecha(self, lz, p0, p1, frac=1.0, color=(255, 214, 90), ancho=10, curva=0.25, capa=2):
        """Flecha curva que se dibuja de p0 a p1 (frac 0..1)."""
        if frac <= 0.01:
            return
        (x0, y0), (x1, y1) = p0, p1
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        nx, ny = -(y1 - y0) * curva, (x1 - x0) * curva
        pts = bezier((x0, y0), (mx + nx * 0.6, my + ny * 0.6 - 0), (mx + nx * 0.6, my + ny * 0.6), (x1, y1), n=40)
        m = max(2, int(len(pts) * min(1.0, frac)))
        seg = pts[:m]
        with lz.capa(capa):
            lz.trazo(seg, color, ancho=ancho, temblor=0.0)
            (ax, ay), (bx, by) = seg[-2], seg[-1]
            ang = math.atan2(by - ay, bx - ax)
            L = ancho * 2.6
            cab = [(bx + math.cos(ang) * L * 0.5, by + math.sin(ang) * L * 0.5),
                   (bx + math.cos(ang + 2.5) * L, by + math.sin(ang + 2.5) * L),
                   (bx + math.cos(ang - 2.5) * L, by + math.sin(ang - 2.5) * L)]
            lz.relleno(cab, color)

    def barra(self, lz, x, y, w, h, frac, color=(110, 230, 255), fondo=(40, 40, 80), capa=2):
        """Barra de progreso/medidor (frac 0..1)."""
        with lz.capa(capa):
            lz.relleno(rect_red(x, y, w, h, h / 2), fondo, alfa=0.8)
            if frac > 0.01:
                lz.relleno(rect_red(x, y, max(h, w * min(1.0, frac)), h, h / 2), color)


def segura(clase, firma=None):
    """Fábrica para CLASES: crea la toma; si el guion cambió (firma distinta) o truena, usa LibrePlano."""
    def crear(d, idx):
        if firma and firma_parte(d) != firma:
            return LibrePlano(d, idx)
        try:
            esc = clase(d, idx)
        except Exception:
            if ESTRICTO:
                raise
            return LibrePlano(d, idx)
        if not ESTRICTO:
            _blindar(esc, d, idx)
        return esc
    crear.clase = clase
    return crear


def _blindar(esc, d, idx):
    estado = {"rota": False, "resp": None}

    def respaldo():
        if estado["resp"] is None:
            estado["resp"] = LibrePlano(d, idx)
        return estado["resp"]

    for nombre in ("dibujar", "fondo", "camara"):
        orig = getattr(esc, nombre)

        def envuelta(*a, _orig=orig, _n=nombre):
            if not estado["rota"]:
                try:
                    return _orig(*a)
                except Exception:
                    estado["rota"] = True
            return getattr(respaldo(), _n)(*a)
        setattr(esc, nombre, envuelta)


def firma_parte(d):
    """Huella del texto de una parte: si cambia, la toma generada ya no corresponde."""
    import hashlib
    txt = "|".join(f.get("texto", "") if isinstance(f, dict) else str(f) for f in (d.get("frases") or []))
    return hashlib.md5(txt.encode("utf-8")).hexdigest()[:10]
