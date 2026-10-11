# -*- coding: utf-8 -*-
"""Escenas del ESTUDIO para el estilo Kurzgesagt Ilustrado (pro_kz_plano y pro_kz_vertical).
Utiliza el motor de vector plano de nucleo/plano.py (cuerpos celestes, microbios, personajes,
naturaleza, partículas y rótulos limpios estilo Poppins).
Se adapta automáticamente tanto a horizontal (1920x1080) como a vertical (1080x1920).
"""
import math

import config
import estilos
import fondos as F
import plano as P
from escena_base import (BLANCO, NEGRO, AMARILLO, CIAN, ICONOS, Escena, circulo, dibujar_icono,
                         e_in, e_inout, e_out, lerp, partir_lineas, pop, prog, sale, env_bombo, TL)
from motor import W, H, ancho_texto, rect_red

estilos.activar("kurzgesagt")

VERT = H > W
CX = W / 2
CY = H * 0.52 if VERT else 540
FUENTE = "geo"
ANCHO_LIN = 14 if VERT else 24
Y_TITULO = 240 if VERT else 110

SLOTS = ([(CX - 220, H * 0.22), (CX + 210, H * 0.76), (CX + 200, H * 0.25), (CX - 210, H * 0.79)] if VERT else
         [(420, 280), (1500, 800), (1500, 280), (420, 800)])

ESC_PLANO = 1.35 if VERT else 1.0


def _palabra(esc, palabra, defecto, desde=0):
    if not palabra:
        return defecto
    try:
        return esc.w(palabra.split()[0], desde=desde)
    except (KeyError, IndexError):
        return defecto


def _px_que_cabe(lineas, px, ancho_max):
    mx = max((ancho_texto(l, FUENTE, 100) for l in lineas), default=1) or 1
    return min(px, ancho_max / mx * 100)


def halo_kurz(lz, x, y, r, t, k):
    """Resplandor cósmico suave característico de Kurzgesagt."""
    if k <= 0:
        return
    with lz.capa(0):
        lz.relleno(circulo(x, y, r * 1.25 * k, 72), (40, 50, 110), alfa=0.22)
        lz.relleno(circulo(x, y, r * 0.95 * k, 64), (70, 90, 180), alfa=0.18)
        lz.relleno(circulo(x, y, r * 0.65 * k, 64), (110, 160, 255), alfa=0.12)


def dibujar_elemento_plano(lz, elemento, cx, cy, s, t, k):
    """Renderiza un objeto vectorial de plano.py con física e iluminación suave."""
    if k <= 0:
        return
    el = (elemento or "").lower().strip()
    r = int(140 * s * k)

    # 1. Cuerpos celestes y espacio
    if any(k in el for k in ("tierra", "planeta", "mundo", "globo")):
        P.tierra(lz, cx, cy, r, t, rot=t * 0.08, luz=1.0, ciudades=1.0)
    elif any(k in el for k in ("sol", "estrella", "luz", "calor", "energia")):
        P.sol(lz, cx, cy, int(r * 0.9), t, brillo=1.0)
    elif any(k in el for k in ("luna", "noche", "satelite")):
        P.luna(lz, cx, cy, r, ang_luz=math.pi * 1.2, luz=1.0)
    elif any(k in el for k in ("galaxia", "universo", "cosmos")):
        P.galaxia(lz, cx, cy, int(r * 1.5), t=t)
    elif "marte" in el:
        P.planeta(lz, cx, cy, r, "marte", t=t)
    elif "jupiter" in el:
        P.planeta(lz, cx, cy, int(r * 1.15), "jupiter", t=t)
    elif "saturno" in el:
        P.planeta(lz, cx, cy, int(r * 0.95), "saturno", t=t)

    # 2. Seres vivos y naturaleza
    elif any(k in el for k in ("pajaro", "ave", "pato", "kuri")):
        P.kuri(lz, cx, cy + 20 * s, s=s * 1.1 * k, t=t)
    elif any(k in el for k in ("microbio", "bacteria", "celula", "virus", "adn")):
        P.microbio(lz, cx, cy, s=s * 1.1 * k, t=t, color=(90, 240, 180))
    elif any(k in el for k in ("arbol", "bosque", "madera")):
        P.arbol(lz, cx, cy + 50 * s, s=s * 1.05 * k, t=t)
    elif any(k in el for k in ("planta", "hoja", "flor")):
        P.planta(lz, cx, cy + 30 * s, s=s * 1.1 * k, t=t)
    elif any(k in el for k in ("conejo", "mascota")):
        P.conejo(lz, cx, cy + 40 * s, s=s * 1.1 * k, t=t)
    elif any(k in el for k in ("zorro", "lobo")):
        P.zorro(lz, cx, cy + 30 * s, s=s * 1.05 * k, t=t)
    elif any(k in el for k in ("humano", "persona", "hombre", "mujer", "gente")):
        P.humano(lz, cx, cy + 40 * s, s=s * 1.0 * k, t=t)

    # 3. Ciencia, física y tecnología
    elif any(k in el for k in ("termometro", "temperatura", "clima", "frio")):
        P.termometro(lz, cx, cy, s=s * 1.1 * k, nivel=0.75 + 0.15 * math.sin(t * 2))
    elif any(k in el for k in ("fumarola", "volcan", "abismo", "fuego")):
        P.fumarola(lz, cx, cy + 60 * s, s=s * 1.1 * k, t=t)
    elif any(k in el for k in ("onda", "radio", "senal", "frecuencia")):
        P.onda(lz, cx, cy, r=int(r * 1.4), ancho=32, color=(90, 210, 255), alfa=k)
    elif any(k in el for k in ("nuclear", "atomo", "radiacion")):
        P.central_nuclear(lz, cx, cy + 40 * s, s=s * 1.0 * k, t=t)
    elif any(k in el for k in ("solar", "panel", "electricidad")):
        P.panel_solar(lz, cx, cy + 30 * s, s=s * 1.1 * k)
    elif any(k in el for k in ("molecula", "quimica")):
        P.molecula(lz, cx, cy, s=s * 1.1 * k, tipo="O2", rot=t * 0.4)
    elif any(k in el for k in ("esfera", "particula")):
        P.esfera(lz, cx, cy, r, (70, 150, 255))

    # 4. Iconos limpios de catálogo general
    elif el in ICONOS:
        halo_kurz(lz, cx, cy, r * 1.3, t, k)
        dibujar_icono(lz, el, cx, cy, s * 0.9 * k, t)
    else:
        # Fallback elegante: planeta Tierra Kurzgesagt
        P.tierra(lz, cx, cy, r, t, rot=t * 0.08, luz=1.0, ciudades=1.0)


class _BasePlano(Escena):
    """Base Kurzgesagt: fondo espacial / degradado, cámara lenta, etiquetas y cifras."""
    N_ESTRELLAS = 30

    def preparar_comun(self, solo_abajo=False):
        self.claves = []
        slots = [sl for sl in SLOTS if sl[1] > H * 0.5] if solo_abajo else SLOTS
        for i, (palabra, texto) in enumerate(self.d.get("claves", [])[:4]):
            tc = _palabra(self, palabra, self.t0 + 0.6 + 1.2 * i)
            self.claves.append((tc, texto.upper()[:24], slots[i % len(slots)]))
            self.ev(tc, "pop", 0.45, pan=-0.3 if slots[i % len(slots)][0] < CX else 0.3, tono=1.05 + 0.08 * i)
        self.t_cifra = None
        if self.d.get("cifra"):
            self.t_cifra = _palabra(self, self.d.get("cifra_palabra"), self.t0 + 1.0)
            self.ev(self.t_cifra, "impacto", 0.65)
        if self.d.get("titulo"):
            self.ev(self.t0 + 0.1, "whoosh", 0.35, dur=0.35)

    def fondo(self, t):
        return F.espacio(t, tono=1 if self.idx % 2 == 1 else 0)

    def camara(self, t):
        u = t - self.t0
        # Deriva suave cinematográfica (sin movimientos bruscos)
        return (1.02 + 0.02 * math.sin(u * 0.35 + self.idx), 0.004 * math.sin(u * 0.25 + self.idx),
                16 * math.sin(u * 0.22 + self.idx), 10 * math.cos(u * 0.28))

    def rotulo(self, lz, t):
        tit = self.d.get("titulo")
        if not tit:
            return
        k = pop(t, self.t0 + 0.1, 0.35) * sale(t, self.t1 - 0.22, 0.22)
        if k > 0:
            P.pastilla(lz, CX, Y_TITULO, tit.upper()[:28], px=42 if VERT else 40, k=k,
                       fondo=(255, 255, 255), color=(26, 22, 54), fuente=FUENTE)

    def dibujar_claves(self, lz, t):
        for i, (tc, texto, (x, y)) in enumerate(self.claves):
            k = pop(t, tc, 0.3) * sale(t, self.t1 - 0.2, 0.2)
            if k > 0:
                y_flota = y + 6 * math.sin(t * 1.8 + i)
                P.pastilla(lz, x, y_flota, texto, px=38 if VERT else 36, k=k,
                           fondo=(235, 240, 255), color=(30, 25, 60), fuente=FUENTE)

    def dibujar_cifra(self, lz, t):
        if self.t_cifra is None:
            return
        k = pop(t, self.t_cifra, 0.4) * sale(t, self.t1 - 0.25, 0.25)
        if k > 0:
            txt = str(self.d["cifra"])[:14]
            px = min(220, int((W * 0.8) / max(1, ancho_texto(txt, FUENTE, 100)) * 100))
            y = H * 0.22 if VERT else 240
            with lz.capa(2):
                P.rotulo(lz, CX, y, txt, px=px, k=k * (1 + 0.03 * env_bombo(t)),
                         color=(100, 230, 255), fuente=FUENTE, rot=0.01 * math.sin(t * 1.5))


class IntroPlano(_BasePlano):
    """Intro Kurzgesagt: Título con tipografía limpia + cuerpo celeste central que emerge."""

    def preparar(self):
        self.elemento = self.d.get("icono") or "tierra"
        self.lineas = partir_lineas(config.TITULO.upper(), ANCHO_LIN)[:4]
        for i in range(len(self.lineas)):
            self.ev(0.12 + 0.28 * i, "impacto" if i == 0 else "pop", 0.75, tono=0.95 + 0.1 * i)
        self.fin_titulo = self.fr[1]["t0"] - 0.2 if len(self.fr) > 1 else max(self.t0 + 2.0, self.fr[0]["t1"] - 0.4)
        self.ev(self.fin_titulo, "whoosh", 0.5, dur=0.4)
        self.preparar_comun(solo_abajo=True)

    def dibujar(self, lz, t):
        sube = e_inout(prog(t, self.fin_titulo - 0.1, self.fin_titulo + 0.45))
        n = len(self.lineas)
        px = _px_que_cabe(self.lineas, (126 if n <= 2 else 102) if VERT else (116 if n <= 3 else 90), W * 0.78)
        y_fin = H * 0.18 if VERT else 165

        with lz.grupo(CX, lerp(CY, y_fin, sube), 1 - 0.45 * sube):
            for i, lin in enumerate(self.lineas):
                k = pop(t, 0.12 + 0.28 * i, 0.35)
                if k > 0:
                    with lz.capa(2):
                        P.rotulo(lz, 0, -(n - 1) * px * 0.62 + i * px * 1.25, lin, px=px, k=k,
                                 color=BLANCO if i == 0 else (240, 245, 255), fuente=FUENTE)

        if sube > 0.05:
            k_elem = pop(t, self.fin_titulo + 0.1, 0.45)
            y_elem = CY + 80 if VERT else CY + 40
            dibujar_elemento_plano(lz, self.elemento, CX, y_elem, ESC_PLANO * 1.15, t, k_elem * sube)

        self.dibujar_claves(lz, t)


class LibrePlano(_BasePlano):
    """Escena vectorial Kurzgesagt: elemento visual principal + segundo elemento con flecha si existe."""

    def preparar(self):
        self.elem = self.d.get("icono") or "tierra"
        self.elem2 = self.d.get("icono2")
        self.ev(self.t0 + 0.1, "aparicion", 0.55)
        n = len(self.fr)
        self.tc = (self.fr[n // 2]["t0"] - 0.2 if n > 1 else self.t0 + (self.t1 - self.t0) * 0.5) if self.elem2 else 1e9
        if self.elem2:
            self.ev(self.tc + 0.1, "whoosh", 0.55, pan=0.3)
        self.preparar_comun()

    def dibujar(self, lz, t):
        k = pop(t, self.t0 + 0.1, 0.4) * sale(t, self.t1 - 0.15, 0.2)
        mov = e_inout(prog(t, self.tc - 0.1, self.tc + 0.45))

        if VERT:
            p1, p2 = (CX, lerp(CY, H * 0.38, mov)), (CX, H * 0.67)
        else:
            p1, p2 = (lerp(CX, 530, mov), CY), (1390, CY)

        s1 = lerp(1.0, 0.75, mov) * ESC_PLANO
        if self.t_cifra is not None and not self.elem2:
            s1 *= lerp(1.0, 0.82, e_inout(prog(t, self.t_cifra, self.t_cifra + 0.4)))

        if k > 0:
            dibujar_elemento_plano(lz, self.elem, p1[0], p1[1] + 10 * math.sin(t * 1.8), s1, t, k)

        if self.elem2 and t >= self.tc:
            k2 = pop(t, self.tc + 0.1, 0.4) * sale(t, self.t1 - 0.15, 0.2)
            if k2 > 0:
                # Flecha conectora discontinua limpia
                with lz.capa(2):
                    if VERT:
                        pts = [(CX, H * 0.48), (CX, H * 0.57)]
                    else:
                        pts = [(820, CY), (1100, CY)]
                    P.discontinua(lz, pts, (100, 220, 255), ancho=6, largo=24, hueco=14, fase=-t * 40)
                dibujar_elemento_plano(lz, self.elem2, p2[0], p2[1] + 10 * math.sin(t * 1.8 + 1),
                                       0.75 * ESC_PLANO, t, k2)

        self.dibujar_cifra(lz, t)
        self.dibujar_claves(lz, t)
        self.rotulo(lz, t)


class CierrePlano(_BasePlano):
    """Cierre Kurzgesagt: gran elemento final + mensaje inolvidable con resplandor."""

    def preparar(self):
        self.elem = self.d.get("icono") or "sol"
        self.fin = self.fr[-1]["t1"] + 0.12 if self.fr else self.t0 + 1.0
        if self.fr:
            self.ev(self.fr[0]["t0"], "brillo", 0.6)
        self.ev(self.fin, "impacto", 0.85)
        self.preparar_comun()

    def dibujar(self, lz, t):
        t_ini = self.fr[0]["t0"] if self.fr else self.t0

        if t < self.fin + 0.2:
            fuera = e_in(prog(t, self.fin - 0.1, self.fin + 0.2))
            k_elem = pop(t, t_ini + 0.1, 0.4) * (1 - fuera)
            if k_elem > 0:
                dibujar_elemento_plano(lz, self.elem, CX, CY + (40 if VERT else 0), ESC_PLANO * 1.1, t, k_elem)
            self.dibujar_claves(lz, t)

        if t >= self.fin:
            lineas = partir_lineas(self.d.get("cierre", "¿LO SABÍAS?").upper(), 13 if VERT else 20)[:4]
            px = _px_que_cabe(lineas, 108 if VERT else 102, W * 0.74)
            y0 = CY - (len(lineas) - 1) * px * 0.65
            with lz.capa(2):
                for i, lin in enumerate(lineas):
                    k = pop(t, self.fin + 0.14 * i, 0.38)
                    if k > 0:
                        P.rotulo(lz, CX, y0 + i * px * 1.3, lin, px=px, k=k,
                                 color=(255, 230, 80) if i == 0 else BLANCO, fuente=FUENTE)

        self.rotulo(lz, t)

    def render(self, lz, t):
        img = Escena.render(self, lz, t)
        neg = prog(t, self.t1 - 0.55, self.t1 - 0.05)
        return img * (1 - neg) if neg > 0 else img


def clases_plano():
    n = len(TL["escenas"])
    return {e["id"]: (IntroPlano if k == 0 else CierrePlano if k == n - 1 else LibrePlano)
            for k, e in enumerate(TL["escenas"])}
