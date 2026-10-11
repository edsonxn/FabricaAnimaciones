# -*- coding: utf-8 -*-
"""Escenas del ESTUDIO (versión comercial): funcionan con cualquier guion generado por la interfaz y se adaptan solas
a horizontal (1920x1080) o vertical (1080x1920). No tocan el núcleo: viven fuera de nucleo/ y heredan de escena_base.

Campos por escena (guion.py del proyecto del estudio):
  frases            1-4 frases narradas
  titulo            rótulo corto arriba (opcional)
  icono / icono2    nombres del catálogo ICONOS; icono2 entra con flecha a mitad de la escena (opcional)
  claves            [[palabra_dicha, "ETIQUETA"], ...] -> chip que aparece cuando se dice la palabra
  cifra, cifra_palabra   número/fecha grande que aparece cuando se dice cifra_palabra (opcional)
Primera escena = intro con el TITULO del video; última = cierre con d["cierre"].
Estilo personal: guion.ESTILO_PERSONAL = dict(base="limpio", ...) se registra como estilo «personal».
Todo se mueve siempre: cámara en deriva, íconos que flotan, partículas de fondo (nada quieto > 2 s).
"""
import math

import config
import estilos
from escena_base import *  # noqa: F401,F403
from escena_base import (AMARILLO, CIAN, BLANCO, NEGRO, ICONOS, Escena, chip, dibujar_icono, e_in, e_inout, flecha,
                         fondo_estilo, lerp, mezcla_fondos, partir_lineas, pop, prog, sale, env_bombo, circulo,
                         estrella, color_arcoiris, TL)
from motor import W, H, ancho_texto

# ------------------------------------------------------------------ estilo personal (creado en la interfaz)
_PERSONAL = getattr(config._g, "ESTILO_PERSONAL", None)
if _PERSONAL:
    _base = dict(estilos.ESTILOS.get(_PERSONAL.get("base", "limpio"), estilos.ESTILOS["limpio"]))
    _base.update({k: (tuple(v) if isinstance(v, list) else v) for k, v in _PERSONAL.items() if k != "base"})
    if "fondos" in _PERSONAL:
        _base["fondos"] = {k: (v[0], {kk: (tuple(vv) if isinstance(vv, list) else vv) for kk, vv in v[1].items()})
                           for k, v in _PERSONAL["fondos"].items()}
    estilos.ESTILOS["personal"] = _base
    estilos.activar("personal")

VERT = H > W
CX = W / 2
CY = H * 0.53 if VERT else 560
FUENTE = estilos.ACTUAL.get("fuente_titulos", "snap")
ANCHO_LIN = 13 if VERT else 22                       # caracteres por línea en títulos grandes
Y_TITULO = 250 if VERT else 105                      # rótulo de escena (vertical: debajo de la zona de la app)
# huecos de etiquetas: lejos del centro (donde están los íconos) y dentro de la zona segura
SLOTS = ([(CX - 200, H * 0.20), (CX + 190, H * 0.77), (CX + 160, H * 0.235), (CX - 170, H * 0.80)] if VERT else
         [(430, 300), (1490, 830), (1490, 300), (430, 830)])


def _px_que_cabe(lineas, px, ancho_max):
    """Tamaño de letra para que la línea más ancha quepa en ancho_max."""
    mx = max((ancho_texto(l, FUENTE, 100) for l in lineas), default=1) or 1
    return min(px, ancho_max / mx * 100)


ESC_ICONO = 1.45 if VERT else 1.0                    # en vertical los dibujos crecen (pantalla de teléfono)


def halo(lz, x, y, r, t, k, seed=0):
    """Disco suave + anillo punteado que gira detrás del dibujo principal: ancla la composición."""
    if k <= 0:
        return
    col = estilos.ACTUAL.get("color_halo") or (255, 255, 255)
    with lz.capa(0):
        lz.relleno(circulo(x, y, r * k * (1 + 0.03 * math.sin(t * 2)), 64), col, seed=seed, alfa=0.18)
        lz.relleno(circulo(x, y, r * 0.78 * k, 64), col, seed=seed + 1, alfa=0.14)
        n = 18
        for i in range(n):
            a = i / n * 2 * math.pi + t * 0.35
            lz.relleno(circulo(x + r * 1.12 * k * math.cos(a), y + r * 1.12 * k * math.sin(a), 7 * k, 10), col,
                       seed=seed + 2 + i, alfa=0.35)


def _palabra(esc, palabra, defecto, desde=0):
    """Ancla segura: si la palabra no se encuentra (alineación rara), no tumba el render."""
    if not palabra:
        return defecto
    try:
        return esc.w(palabra.split()[0], desde=desde)
    except (KeyError, IndexError):
        return defecto


class _Base(Escena):
    """Cámara en deriva + partículas de ambiente + rótulo + etiquetas clave + cifra."""
    N_PART = 16

    def preparar_comun(self, solo_abajo=False):
        self.claves = []
        if solo_abajo:                              # arriba está el título del video: etiquetas solo abajo
            slots = [sl for sl in SLOTS if sl[1] > H * 0.5]
        else:
            slots = SLOTS[1:] + SLOTS[:1] if self.d.get("cifra") else SLOTS
        for i, (palabra, texto) in enumerate(self.d.get("claves", [])[:4]):
            tc = _palabra(self, palabra, self.t0 + 0.6 + 1.2 * i)
            self.claves.append((tc, texto.upper()[:24], slots[i % len(slots)]))
            self.ev(tc, "pop", 0.5, pan=-0.4 if slots[i % len(slots)][0] < CX else 0.4, tono=1.0 + 0.1 * i)
        self.t_cifra = None
        if self.d.get("cifra"):
            self.t_cifra = _palabra(self, self.d.get("cifra_palabra"), self.t0 + 1.0)
            self.ev(self.t_cifra, "impacto", 0.6)
        if self.d.get("titulo"):
            self.ev(self.t0 + 0.12, "whoosh", 0.35, dur=0.35)

    def camara(self, t):
        u = t - self.t0
        return (1.03 + 0.025 * math.sin(u * 0.45 + self.idx), 0.008 * math.sin(u * 0.31 + self.idx * 2),
                22 * math.sin(u * 0.27 + self.idx), 14 * math.cos(u * 0.33))

    def particulas(self, lz, t):
        col = estilos.ACTUAL.get("color_particulas") or (255, 255, 255)
        with lz.capa(0):
            for i in range(self.N_PART):
                fx = (i * 0.6180339 + self.idx * 0.13) % 1.0
                vel = 18 + 22 * ((i * 0.37) % 1.0)
                y = (H + 80) - ((t * vel + i * 211) % (H + 160))
                x = fx * W + 30 * math.sin(t * 0.6 + i)
                r = 5 + 7 * ((i * 0.71) % 1.0)
                if i % 3 == 0:
                    lz.relleno(estrella(x, y, r * 1.8, r * 0.8, 4, rot=t * 0.8 + i), col, seed=900 + i, alfa=0.35)
                else:
                    lz.relleno(circulo(x, y, r, 14), col, seed=900 + i, alfa=0.22)

    def rotulo(self, lz, t):
        tit = self.d.get("titulo")
        if not tit:
            return
        k = pop(t, self.t0 + 0.1, 0.35) * sale(t, self.t1 - 0.25, 0.25)
        if k > 0:
            chip(lz, CX, Y_TITULO, tit.upper()[:28], k, 50 if VERT else 46, seed=60 + self.idx, rot=-0.02)

    def dibujar_claves(self, lz, t):
        for i, (tc, texto, (x, y)) in enumerate(self.claves):
            k = pop(t, tc, 0.3) * sale(t, self.t1 - 0.2, 0.2)
            if k > 0:
                chip(lz, x, y + 8 * math.sin(t * 2 + i), texto, k, 46 if VERT else 44, seed=400 + i,
                     rot=-0.03 + 0.03 * (i % 3))

    def dibujar_cifra(self, lz, t):
        if self.t_cifra is None:
            return
        k = pop(t, self.t_cifra, 0.4) * sale(t, self.t1 - 0.25, 0.25)
        if k > 0:
            txt = str(self.d["cifra"])[:12]
            px = min(210, (W * 0.8) / max(1, ancho_texto(txt, FUENTE, 100)) * 100)
            y = H * 0.19 if VERT else 250
            lz.texto(txt, CX, y, px, FUENTE, color=color_arcoiris(t * 0.2 + self.idx * 0.3), borde=NEGRO,
                     borde_px=14, k=k * (1 + 0.04 * env_bombo(t)), rot=0.03 * math.sin(t * 1.7), seed=70)


class IntroEstudio(_Base):
    """Título del video que rebota y luego sube; íconos del video en órbita."""

    def preparar(self):
        self.iconos = [i for i in dict.fromkeys(e.get(k) for e in TL["escenas"] for k in ("icono", "icono2"))
                       if i in ICONOS][:6] or ["estrella"]
        self.lineas = partir_lineas(config.TITULO.upper(), ANCHO_LIN)[:4]
        for i in range(len(self.lineas)):
            self.ev(0.15 + 0.3 * i, "impacto" if i == 0 else "pop", 0.8, tono=0.9 + 0.1 * i)
        self.fin_titulo = self.fr[1]["t0"] - 0.2 if len(self.fr) > 1 else max(self.t0 + 2.0, self.fr[0]["t1"] - 0.4)
        self.ev(self.fin_titulo, "whoosh", 0.5, dur=0.4)
        self.preparar_comun(solo_abajo=True)

    def fondo(self, t):
        return mezcla_fondos(t, self.fin_titulo, lambda tt: fondo_estilo("titulo", tt, self.PAL, env_bombo(tt)),
                             lambda tt: fondo_estilo("libre", tt, self.PAL, env_bombo(tt)))

    def dibujar(self, lz, t):
        self.particulas(lz, t)
        sube = e_inout(prog(t, self.fin_titulo - 0.1, self.fin_titulo + 0.45))
        n = len(self.lineas)
        px = _px_que_cabe(self.lineas, (124 if n <= 2 else 104) if VERT else (118 if n <= 3 else 92), W * 0.78)
        y_fin = H * 0.17 if VERT else 175
        with lz.grupo(CX, lerp(CY, y_fin, sube), 1 - 0.5 * sube):
            for i, lin in enumerate(self.lineas):
                k = pop(t, 0.15 + 0.3 * i, 0.35)
                if k > 0:
                    lz.texto(lin, 0, -(n - 1) * px * 0.62 + i * px * 1.25, px, FUENTE,
                             color=color_arcoiris(t * 0.2 + i * 0.25), borde=NEGRO, borde_px=12, k=k,
                             rot=0.03 * math.sin(t * 2 + i), seed=10 + i)
        if sube > 0:
            m = len(self.iconos)
            rx, ry = (W * 0.32, H * 0.2) if VERT else (480, 170)
            for i, ic in enumerate(self.iconos):
                a = i / m * 2 * math.pi + t * 0.5
                dibujar_icono(lz, ic, CX + rx * math.cos(a), CY + 80 + ry * math.sin(a), 0.5 * ESC_ICONO * sube, t)
        self.dibujar_claves(lz, t)


class LibreEstudio(_Base):
    """Ícono principal grande; si hay icono2, el primero se aparta y entra el segundo con una flecha."""

    def preparar(self):
        self.ic = self.d.get("icono") if self.d.get("icono") in ICONOS else "estrella"
        self.ic2 = self.d.get("icono2") if self.d.get("icono2") in ICONOS else None
        self.ev(self.t0 + 0.12, "aparicion", 0.5)
        n = len(self.fr)
        self.tc = (self.fr[n // 2]["t0"] - 0.2 if n > 1 else self.t0 + (self.t1 - self.t0) * 0.5) if self.ic2 else 1e9
        if self.ic2:
            self.ev(self.tc + 0.1, "boing", 0.6, pan=0.4)
        self.preparar_comun()

    def dibujar(self, lz, t):
        self.particulas(lz, t)
        k = pop(t, self.t0 + 0.12, 0.45) * sale(t, self.t1 - 0.15, 0.2)
        mov = e_inout(prog(t, self.tc - 0.1, self.tc + 0.45))
        if VERT:
            p1, p2 = (CX, lerp(CY, H * 0.37, mov)), (CX, H * 0.66)
        else:
            p1, p2 = (lerp(CX, 520, mov), CY), (1400, CY)
        s1 = lerp(1.0, 0.72, mov) * ESC_ICONO
        if self.t_cifra is not None and not self.ic2:
            s1 *= lerp(1.0, 0.8, e_inout(prog(t, self.t_cifra, self.t_cifra + 0.4)))
        if k > 0:
            halo(lz, p1[0], p1[1], 260 * s1, t, k, seed=500)
            dibujar_icono(lz, self.ic, p1[0], p1[1] + 14 * math.sin(t * 2), s1 * k * (1 + 0.03 * env_bombo(t)), t)
        if self.ic2 and t >= self.tc:
            k2 = pop(t, self.tc + 0.1, 0.4) * sale(t, self.t1 - 0.15, 0.2)
            if k2 > 0:
                if VERT:
                    a, b = (CX, H * 0.47), (CX, H * 0.56)
                else:
                    a, b = (800, CY), (1110, CY)
                flecha(lz, a, b, prog(t, self.tc + 0.1, self.tc + 0.4), color=AMARILLO, ancho=16, seed=77, curva=0.12)
                halo(lz, p2[0], p2[1], 190 * ESC_ICONO, t + 1.3, k2, seed=540)
                dibujar_icono(lz, self.ic2, p2[0], p2[1] + 14 * math.sin(t * 2 + 1), 0.72 * ESC_ICONO * k2, t)
        self.dibujar_cifra(lz, t)
        self.dibujar_claves(lz, t)
        self.rotulo(lz, t)


class CierreEstudio(_Base):
    """Íconos en órbita + tarjeta final (d['cierre']) + fundido a negro."""

    def preparar(self):
        self.iconos = [i for i in dict.fromkeys(e.get(k) for e in TL["escenas"] for k in ("icono", "icono2"))
                       if i in ICONOS][:6] or ["estrella"]
        self.fin = self.fr[-1]["t1"] + 0.12 if self.fr else self.t0 + 1.0
        if self.fr:
            self.ev(self.fr[0]["t0"], "brillo", 0.6)
        self.ev(self.fin, "impacto", 0.9)
        self.preparar_comun()

    def fondo(self, t):
        return mezcla_fondos(t, self.fin, lambda tt: fondo_estilo("libre", tt, self.PAL, env_bombo(tt)),
                             lambda tt: fondo_estilo("titulo", tt, self.PAL, env_bombo(tt)))

    def dibujar(self, lz, t):
        self.particulas(lz, t)
        t_ini = self.fr[0]["t0"] if self.fr else self.t0
        if t < self.fin + 0.25:
            fuera = e_in(prog(t, self.fin - 0.1, self.fin + 0.25))
            m = len(self.iconos)
            rx, ry = (W * 0.3, H * 0.2) if VERT else (500, 200)
            for i, ic in enumerate(self.iconos):
                a = i / m * 2 * math.pi + t * 0.6
                kk = pop(t, t_ini + 0.1 * i, 0.35) * (1 - fuera)
                if kk > 0:
                    dibujar_icono(lz, ic, CX + rx * math.cos(a), CY + ry * math.sin(a), 0.5 * ESC_ICONO * kk, t)
            self.dibujar_claves(lz, t)
        if t >= self.fin:
            lineas = partir_lineas(self.d.get("cierre", "¿LO SABÍAS?").upper(), 12 if VERT else 18)[:4]
            px = _px_que_cabe(lineas, 112 if VERT else 110, W * 0.72)
            y0 = CY - (len(lineas) - 1) * px * 0.65
            for i, lin in enumerate(lineas):
                lz.texto(lin, CX, y0 + i * px * 1.3, px, FUENTE, color=AMARILLO if i == 0 else BLANCO, borde=NEGRO,
                         borde_px=12, k=pop(t, self.fin + 0.15 * i, 0.4) * (1 + 0.02 * math.sin(t * 3 + i)),
                         rot=-0.03 + 0.01 * math.sin(t * 1.5), seed=150 + i)
        self.rotulo(lz, t)

    def render(self, lz, t):
        img = Escena.render(self, lz, t)
        neg = prog(t, self.t1 - 0.6, self.t1 - 0.05)
        return img * (1 - neg) if neg > 0 else img


def clases_estudio():
    n = len(TL["escenas"])
    return {e["id"]: (IntroEstudio if k == 0 else CierreEstudio if k == n - 1 else LibreEstudio)
            for k, e in enumerate(TL["escenas"])}
