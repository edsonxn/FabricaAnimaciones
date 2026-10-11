# -*- coding: utf-8 -*-
"""Base reutilizable de escenas: Escena (genérica), Item (título -> fase A -> fase B), utilidades
visuales (chip, flecha, palomita, icono_app...) y el catálogo ICONOS. Las escenas de cada video
heredan de aquí (videos/<nombre>/escenas.py). Todo se ancla a palabras de la narración con self.w()."""
import inspect
import json
import math
import re
import unicodedata

import numpy as np

import config
import estilos
import dibujos as D
import efectos as E
import fondos as F
from motor import (BLANCO, NEGRO, OCRE, W, H, Lienzo, ancho_texto, arco, blob, campana, catmull, circulo, clamp01,
                   componer, corazon, e_back, e_in, e_inout, e_out, elipse, espiral, bezier, estrella, h01, lerp, mat_r, mat_s,
                   mat_t, prog, r1, rect_red, remuestrear, smooth)
from ritmo import BEAT, env_bombo

TL = json.load(open("timeline.json", encoding="utf-8"))
estilos.activar(config.ESTILO_VISUAL)
AMARILLO, CIAN, MAGENTA, ROJO, VERDE = D.AMARILLO, D.CIAN, D.MAGENTA, D.ROJO, D.VERDE
OW = D.OW   # grosor de contorno estándar


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9ñ]+", "", s)


def pop(t, t0, dur=0.28):
    """Escala de aparición con rebote (0 antes de t0)."""
    return 0.0 if t < t0 else e_back(prog(t, t0, t0 + dur))


def sale(t, t0, dur=0.25):
    """1 → 0 a partir de t0."""
    return 1.0 - e_in(prog(t, t0, t0 + dur))


def color_arcoiris(u, s=0.75, v=1.0):
    rango = estilos.ACTUAL.get("hue_rango")      # estilos calmados: solo un rango de tonos (p. ej. cálidos)
    if rango:
        u = rango[0] + (rango[1] - rango[0]) * (0.5 + 0.5 * math.sin(u * 2 * math.pi))
    return tuple(int(255 * c) for c in D._hsv(u % 1.0, s, v))


# ============================================================ base
class Escena:
    PAL = "arcoiris"

    def __init__(self, d, idx):
        self.d = d
        self.idx = idx
        self.id = d["id"]
        self.t0, self.t1 = d["t0"], d["t1"]
        self.fr = d["frases"]
        self.sfx = []
        self.posts = []      # (ta, tb, fn(img, t, u)) con u = envolvente 0..1
        self.preparar()

    # ---- anclas de palabras
    def w(self, texto, frase=None, n=0, fin=False, desde=0):
        """Tiempo (s) en que se dice `texto` (inicio, o fin si fin=True). frase: índice exacto; desde: primera
        frase donde buscar; n: n-ésima aparición. Lanza KeyError si no está (así nada queda desincronizado)."""
        obj = [norm(x) for x in texto.split()]
        frases = [self.fr[frase]] if frase is not None else self.fr[desde:]
        hits = []
        for f in frases:
            ws = f["words"]
            nw = [norm(x["w"]) for x in ws]
            for i in range(len(ws) - len(obj) + 1):
                if all(nw[i + j].startswith(obj[j]) for j in range(len(obj))):
                    hits.append(ws[i + len(obj) - 1]["e"] if fin else ws[i]["s"])
        if len(hits) <= n:
            raise KeyError(f"[{self.id}] palabra no encontrada: '{texto}'")
        return hits[n]

    def ev(self, t, nombre, vol=1.0, pan=0.0, **kw):
        self.sfx.append(dict(t=round(float(t), 4), nombre=nombre, vol=vol, pan=pan, **kw))

    def post_fx(self, ta, tb, fn, rampa=0.15):
        self.posts.append((ta, tb, fn, rampa))

    # ---- a implementar
    def preparar(self):
        pass

    def fondo(self, t):
        return fondo_estilo("libre", t, self.PAL, env_bombo(t))

    def camara(self, t):
        return 1.0, 0.0, 0.0, 0.0

    def dibujar(self, lz, t):
        pass

    def ui(self, lz, t):
        return False

    def wob(self, t):
        return estilos.ACTUAL["wob"]

    # ---- render
    def matriz_camara(self, t):
        z, rot, dx, dy = self.camara(t)
        z *= 1 + 0.014 * env_bombo(t)
        return mat_t(W / 2 + dx, H / 2 + dy) @ mat_r(rot) @ mat_s(z) @ mat_t(-W / 2, -H / 2)

    def render(self, lz, t):
        lz.nuevo(t, wob=self.wob(t))
        bg = self.fondo(t)
        lz.M = self.matriz_camara(t)
        fps = estilos.ACTUAL.get("fps_mov")
        self.dibujar(lz, math.floor(t * fps) / fps if fps else t)
        img = componer(bg, lz.resolver(), boil=lz.boil)
        for ta, tb, fn, rampa in self.posts:
            if ta - rampa <= t <= tb + rampa:
                u = min(prog(t, ta - rampa, ta), 1 - prog(t, tb, tb + rampa)) if rampa > 0 else 1.0
                img = fn(img, t, smooth(u))
        lz.nuevo(t)
        if self.ui(lz, t):
            img = componer(img, lz.resolver(), boil=lz.boil)
        return np.clip(img, 0, 1)


def fondo_estilo(clave, t, pal=None, pulso=0.0):
    """Fondo por defecto del estilo activo. clave: titulo | antes | hoy | libre."""
    nombre, params = estilos.ACTUAL["fondos"][clave]
    fn = F.FONDOS[nombre]
    sig = inspect.signature(fn).parameters
    kw = dict(params)
    if "pal" in sig and "pal" not in kw and pal:
        kw["pal"] = pal
    if "pulso" in sig:
        kw["pulso"] = pulso
    return fn(t, **kw)


def mezcla_fondos(t, tc, fa, fb, dur=0.3):
    u = prog(t, tc, tc + dur)
    if u <= 0:
        return fa(t)
    if u >= 1:
        return fb(t)
    return fa(t) * (1 - u) + fb(t) * u


# ============================================================ escena de ítem
class Item(Escena):
    """Escena de ítem numerado. Requiere en guion.py: num, titulo y 3 frases:
    frase 0 = "<Número N>: <título>" (las primeras `palabras_previas` palabras no son el título),
    frase 1 = fase A (antes/contexto), frase 2 = fase B (hoy/remate).
    Opcionales: dato, fuente, sello (texto fase A; None = sin sello), sello_hoy, etiqueta_numero,
    fase_b (índice de la frase donde empieza la fase B; por defecto 2 -> permite ítems de 4+ frases)."""
    PAL = "arcoiris"
    SELLO = "HACE ~40.000 AÑOS"
    ANTES_PERSISTE = False

    def preparar(self):
        self.num = self.d["num"]
        self.A = self.t0
        self.B = self.fr[1]["t0"] - 0.3
        self.C = self.fr[self.d.get("fase_b", 2)]["t0"] - 0.25     # fase_b: índice de la frase que abre la fase B
        self.SELLO = self.d.get("sello", self.SELLO)
        previas = self.d.get("palabras_previas", 2)
        palabras = self.fr[0]["words"][previas:]
        titulo = self.d["titulo"].split()
        assert len(palabras) == len(titulo), (
            f"[{self.id}] el título ({len(titulo)} palabras) debe coincidir con lo narrado tras las primeras "
            f"{previas} palabras de la frase 0: {[w['w'] for w in palabras]}")
        self.t_tit = [w["s"] for w in palabras]
        self.ev(self.A, "impacto", 1.0)
        for k, tw in enumerate(self.t_tit):
            self.ev(tw, "pop", 0.55, pan=-0.3 + 0.6 * k / max(1, len(titulo) - 1), tono=1.0 + 0.12 * k)
        self.ev(self.B - 0.05, "whoosh", 0.7, dur=0.45)
        if self.SELLO:
            self.ev(self.B + 0.2, "sello", 0.6, pan=0.6)
            self.ev(self.C + 0.05, "sello", 0.6, pan=0.6, tono=1.25)
        self.escena()

    def escena(self):
        pass

    # --- fondos por fase
    def fondo_titulo(self, t):
        return fondo_estilo("titulo", t, self.PAL, env_bombo(t))

    def fondo_antes(self, t):
        return fondo_estilo("antes", t, self.PAL, env_bombo(t))

    def fondo_hoy(self, t):
        return fondo_estilo("hoy", t, self.PAL, env_bombo(t))

    def fondo(self, t):
        if t < self.B:
            return self.fondo_titulo(t)
        if t < self.C:
            return mezcla_fondos(t, self.B, self.fondo_titulo, self.fondo_antes)
        return mezcla_fondos(t, self.C, self.fondo_antes, self.fondo_hoy)

    # --- tarjeta de título
    def iconos_titulo(self, lz, t, x, y, s):
        pass

    def dibujar(self, lz, t):
        if t < self.B + 0.4:
            self.tarjeta(lz, t)
        if t >= self.B - 0.05:
            if t < self.C + 0.35 or self.ANTES_PERSISTE:
                self.antes(lz, t)
            if t >= self.C - 0.05:
                self.hoy(lz, t)

    def tarjeta(self, lz, t):
        salida = e_in(prog(t, self.B, self.B + 0.35))
        with lz.grupo(lerp(0, -620, salida), lerp(0, -420, salida), 1 - 0.75 * salida):
            k = pop(t, self.A, 0.4)
            if k <= 0:
                return
            giro = lerp(-0.5, 0, e_out(prog(t, self.A, self.A + 0.4))) + 0.05 * math.sin(t * 2.3)
            col = color_arcoiris(t * 0.25 + self.num * 0.1)
            lz.texto(self.d.get("etiqueta_numero", "NÚMERO"), 960, 175, 64, "print", color=BLANCO, borde=NEGRO, borde_px=9, k=k, rot=-0.06, seed=3)
            lz.texto(f"{self.num}", 960, 395, 330, "snap", color=col, borde=NEGRO, borde_px=16,
                     k=k * (1 + 0.05 * env_bombo(t)), rot=giro, seed=5)
            self.iconos_titulo(lz, t, 960, 395, k)
            # palabras del título, cada una al ser pronunciada
            pal = self.d["titulo"].split()
            px = 104
            anchos = [ancho_texto(p, "snap", px) for p in pal]
            esp = px * 0.35
            lineas = [[0]]
            ancho_lin = anchos[0]
            for i in range(1, len(pal)):
                if ancho_lin + esp + anchos[i] > 1700:
                    lineas.append([i])
                    ancho_lin = anchos[i]
                else:
                    lineas[-1].append(i)
                    ancho_lin += esp + anchos[i]
            y0 = 660 if len(lineas) == 1 else 620
            for li, lin in enumerate(lineas):
                tot = sum(anchos[i] for i in lin) + esp * (len(lin) - 1)
                x = 960 - tot / 2
                for i in lin:
                    kk = pop(t, self.t_tit[i] - 0.03, 0.25)
                    if kk > 0:
                        lz.texto(pal[i], x + anchos[i] / 2, y0 + li * 125, px, "snap",
                                 color=AMARILLO if i % 2 == 0 else CIAN, borde=NEGRO, borde_px=11, k=kk,
                                 rot=0.03 * math.sin(t * 3 + i), seed=10 + i)
                    x += anchos[i] + esp

    def antes(self, lz, t):
        pass

    def hoy(self, lz, t):
        pass

    # --- UI de escena: encabezado, sello de época, dato + fuente
    def ui(self, lz, t):
        if t < self.B + 0.15:
            return False
        k = pop(t, self.B + 0.15, 0.3)
        lz.texto(f"#{self.num} {self.d['titulo']}", 40, 62, 38, "snap", color=AMARILLO, borde=NEGRO, borde_px=7,
                 k=k, ancla=(0.0, 0.5), rot=-0.02, seed=1)
        # sello
        if not self.SELLO:
            pass
        elif t < self.C:
            ks = pop(t, self.B + 0.2, 0.3)
            self.sello(lz, t, self.SELLO, (255, 238, 205), (160, 50, 25), ks)
        else:
            ks = pop(t, self.C + 0.05, 0.3)
            self.sello(lz, t, self.d.get("sello_hoy", "HOY"), (25, 20, 50), CIAN, ks)
        # dato + fuente
        ta, tb = self.B + 0.5, self.C - 0.1
        if ta <= t <= tb + 0.3 and self.d.get("dato"):
            u = e_back(prog(t, ta, ta + 0.35)) * (1 - e_in(prog(t, tb, tb + 0.3)))
            if u > 0.01:
                with lz.grupo(960, 182, u):
                    D.etiqueta(lz, 0, 0, self.d["dato"], 34, fuente="semi", rot=-0.012, seed=7)
                    if self.d.get("fuente"):
                        txt = "Fuente: " + self.d["fuente"]
                        wf = ancho_texto(txt, "semi", 25) + 36
                        lz.relleno(rect_red(-wf / 2, 40, wf, 40, 20), (20, 16, 30), seed=9, alfa=0.78)
                        lz.texto(txt, 0, 60, 25, "semi", color=(235, 235, 240), borde=None, temblor=0.2, seed=8)
        return True

    def sello(self, lz, t, texto, fondo, tinta, k):
        if k <= 0:
            return
        with lz.grupo(1880, 70, k, -0.07):
            w = ancho_texto(texto, "print", 40) + 50
            lz.forma(rect_red(-w, -38, w, 76, 10), fondo, tinta, 6, seed=21)
            lz.trazo(rect_red(-w + 8, -30, w - 16, 60, 7), tinta, 3, cerrado=True, seed=22)
            lz.texto(texto, -w / 2, 2, 40, "print", color=tinta, borde=None, seed=23)


# ============================================================ utilidades visuales
def chip(lz, x, y, texto, k, px=40, rot=-0.03, seed=0, fondo=(255, 250, 235), color=NEGRO, fuente="print"):
    if k <= 0:
        return
    D.etiqueta(lz, x, y, texto, px, fondo=fondo, color=color, rot=rot, seed=seed, k=k, fuente=fuente, cinta=False)


def flecha(lz, p0, p1, frac, color=AMARILLO, ancho=12, seed=0, curva=0.25):
    if frac <= 0:
        return
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    n = np.array([-d[1], d[0]]) * curva
    pts = D.bezier(p0, p0 + d * 0.33 + n, p0 + d * 0.66 + n, p1, 20)
    D.trazo_parcial(lz, pts, frac, color, ancho, seed=seed)
    if frac >= 1:
        dirv = pts[-1] - pts[-3]
        dirv = dirv / (np.linalg.norm(dirv) + 1e-9)
        nv = np.array([-dirv[1], dirv[0]])
        cabeza = [pts[-1] + dirv * 18, pts[-1] - dirv * 16 + nv * 20, pts[-1] - dirv * 16 - nv * 20]
        lz.forma(np.array(cabeza), color, NEGRO, 4, seed + 1)


def palomita(lz, x, y, s, frac, color=VERDE, seed=0):
    D.trazo_parcial(lz, [(x - 22 * s, y), (x - 6 * s, y + 18 * s), (x + 26 * s, y - 22 * s)], frac, color, 12 * s, seed=seed)


def icono_app(lz, x, y, s, tipo, seed=0, t=0.0):
    cols = {"camara": (250, 90, 120), "musica": (80, 200, 120), "corazon": (255, 90, 90), "chat": (70, 170, 250),
            "mapa": (250, 190, 60), "juego": (170, 100, 240)}
    with lz.grupo(x, y, s):
        lz.forma(rect_red(-50, -50, 100, 100, 26), cols[tipo], NEGRO, 5, seed)
        if tipo == "camara":
            lz.forma(circulo(0, 4, 22, 20), BLANCO, NEGRO, 4, seed + 1)
            lz.relleno(circulo(0, 4, 10, 12), NEGRO, seed + 2, temblor=0.2)
        elif tipo == "musica":
            D.nota(lz, -8, 22, 0.55, BLANCO, seed=seed + 1)
        elif tipo == "corazon":
            lz.forma(corazon(0, 2, 30), BLANCO, NEGRO, 4, seed + 1)
        elif tipo == "chat":
            lz.forma(elipse(0, -4, 32, 24), BLANCO, NEGRO, 4, seed + 1)
            lz.relleno([(-14, 14), (-22, 32), (2, 18)], BLANCO, seed + 2)
        elif tipo == "mapa":
            lz.forma(catmull([(0, 30), (-22, -6), (0, -30), (22, -6)], 6, True), ROJO, NEGRO, 4, seed + 1)
        else:
            lz.forma(estrella(0, 0, 30, 13, 5, rot=t), AMARILLO, NEGRO, 4, seed + 1)


def remuestrear_n(P, n):
    P = np.vstack([P, P[:1]])
    seg = np.hypot(*np.diff(P, axis=0).T)
    d = np.concatenate([[0.0], np.cumsum(seg)])
    s = np.linspace(0, d[-1], n, endpoint=False)
    return np.stack([np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], 1)


def caminar(t, t0, dur, x0, x1):
    u = prog(t, t0, t0 + dur)
    return lerp(x0, x1, e_out(u)), (math.sin(t * 14) if 0 < u < 1 else 0.0)


# ============================================================ catálogo de íconos
# Cada ícono se dibuja centrado aprox. en (x, y) con tamaño ~ 400*s px. Firma: fn(lz, x, y, s, t)
def _personaje(tipo, **kw):
    return lambda lz, x, y, s, t: D.personaje(lz, x, y + 250 * s, 0.9 * s, t, tipo, seed=len(tipo) * 13, **kw)


def _sol(lz, x, y, s, t):
    lz.forma(estrella(x, y, 200 * s, 150 * s, 16, rot=t * 0.3), (255, 170, 40), NEGRO, 7, seed=329)
    lz.forma(circulo(x, y, 120 * s, 40), AMARILLO, NEGRO, 7, seed=330)


ICONOS = {
    "mano": lambda lz, x, y, s, t: D.mano(lz, x, y + 60 * s, 1.1 * s, seed=301),
    "estarcido": lambda lz, x, y, s, t: D.estarcido(lz, x, y + 80 * s, 1.0 * s, 1.0, capa=0),
    "cerdo": lambda lz, x, y, s, t: D.cerdo_rupestre(lz, x - 50 * s, y, 0.85 * s, 1.0, capa=1),
    "hamburguesa": lambda lz, x, y, s, t: D.hamburguesa(lz, x, y, 1.3 * s, seed=302),
    "flauta": lambda lz, x, y, s, t: D.flauta(lz, x, y, 1.5 * s, -0.08, seed=303),
    "nota": lambda lz, x, y, s, t: D.nota(lz, x - 60 * s, y + 90 * s, 2.2 * s, MAGENTA, seed=304, doble=True),
    "hombre_leon": lambda lz, x, y, s, t: D.hombre_leon(lz, x, y + 235 * s, 0.8 * s, 1.0, seed=305),
    "mascara": lambda lz, x, y, s, t: D.mascara_arana(lz, x, y, 1.4 * s, seed=306),
    "collar": lambda lz, x, y, s, t: D.collar(lz, x, y + 60 * s, 1.3 * s, seed=307, t=t),
    "aguja": lambda lz, x, y, s, t: D.aguja(lz, x, y, 2.0 * s, 0.1, seed=308),
    "hueso": lambda lz, x, y, s, t: D.hueso(lz, x, y, 1.1 * s, marcas=29, seed=309),
    "atun": lambda lz, x, y, s, t: D.atun(lz, x, y, 1.3 * s, t, seed=310),
    "sushi": lambda lz, x, y, s, t: D.sushi(lz, x, y, 1.9 * s, seed=311),
    "adn": lambda lz, x, y, s, t: D.adn(lz, x, y, 0.8 * s, t, largo=900, seed=312),
    "cerebro": lambda lz, x, y, s, t: D.cerebro(lz, x, y, 1.3 * s, t, seed=313, brillo=0.6),
    "telefono": lambda lz, x, y, s, t: D.telefono(lz, x, y, 0.95 * s, 0.05, t=t, seed=314,
                                                  pantalla=lambda lz: D.ui_camara(lz, t, 315)),
    "fuego": lambda lz, x, y, s, t: D.fuego(lz, x, y + 150 * s, 1.4 * s, t, seed=316),
    "flor": lambda lz, x, y, s, t: D.flor(lz, x, y - 80 * s, 1.4 * s, MAGENTA, seed=317, t=t),
    "vela": lambda lz, x, y, s, t: D.vela(lz, x, y + 110 * s, 1.5 * s, t, seed=318),
    "mamut": lambda lz, x, y, s, t: D.mamut(lz, x - 40 * s, y + 110 * s, 0.9 * s, t, seed=319),
    "wifi": lambda lz, x, y, s, t: D.wifi(lz, x, y + 90 * s, 2.0 * s, seed=320),
    "ciudad": lambda lz, x, y, s, t: D.ciudad(lz, x, y + 150 * s, 1.3 * s, seed=321),
    "trigo": lambda lz, x, y, s, t: D.trigo(lz, x, y + 60 * s, 1.8 * s, seed=322),
    "ojo": lambda lz, x, y, s, t: D.ojo_flotante(lz, x, y, 2.4 * s, t, seed=323,
                                                 mirar=(math.sin(t * 1.3), 0.3 * math.cos(t))),
    "corazon": lambda lz, x, y, s, t: lz.forma(corazon(x, y, 170 * s * (1 + 0.05 * env_bombo(t))), ROJO, NEGRO, 8, seed=324),
    "estrella": lambda lz, x, y, s, t: lz.forma(estrella(x, y, 190 * s, 85 * s, 5, rot=t * 0.5 - math.pi / 2),
                                                AMARILLO, NEGRO, 8, seed=325),
    "australia": lambda lz, x, y, s, t: D.australia(lz, x, y, 1.1 * s, pin=1.0, t=t, seed=326),
    "copo": lambda lz, x, y, s, t: D.copo(lz, x, y, 3.5 * s, t * 0.4, seed=327),
    "bebe": lambda lz, x, y, s, t: D.bebe(lz, x, y, 2.0 * s, t, seed=328),
    "sol": _sol,
    "pan": lambda lz, x, y, s, t: D.pan_plano(lz, x, y, 1.1 * s),
    "tostada": lambda lz, x, y, s, t: D.tostada(lz, x, y, 1.0 * s),
    "pegamento": lambda lz, x, y, s, t: D.tubo_pegamento(lz, x, y + 10 * s, 1.35 * s),
    "pastilla": lambda lz, x, y, s, t: D.pastilla(lz, x, y, 1.5 * s),
    "espejo_obsidiana": lambda lz, x, y, s, t: D.espejo_obsidiana(lz, x, y, 1.0 * s, t),
    "rueda_madera": lambda lz, x, y, s, t: D.rueda_madera(lz, x, y, 1.05 * s, t * 0.6),
    "bici": lambda lz, x, y, s, t: D.bici(lz, x, y - 20 * s, 0.9 * s, t),
    "auto": lambda lz, x, y, s, t: D.auto(lz, x, y, 1.15 * s, t),
    "maleta": lambda lz, x, y, s, t: D.maleta(lz, x, y + 20 * s, 1.0 * s),
    "silla": lambda lz, x, y, s, t: D.silla(lz, x, y + 60 * s, 1.1 * s),
    "tablilla": lambda lz, x, y, s, t: D.tablilla(lz, x, y, 0.95 * s),
    "tablilla_numeros": lambda lz, x, y, s, t: D.tablilla(lz, x, y, 0.95 * s, numeros=True, seed=585),
    "vasija": lambda lz, x, y, s, t: D.vasija(lz, x, y + 10 * s, 1.2 * s),
    "chat": lambda lz, x, y, s, t: D.chat(lz, x + 20 * s, y + 10 * s, 1.45 * s, t),
    "drenaje": lambda lz, x, y, s, t: D.drenaje(lz, x, y - 30 * s, 1.0 * s, t),
    "inodoro": lambda lz, x, y, s, t: D.inodoro(lz, x, y + 40 * s, 1.1 * s),
    "reloj": lambda lz, x, y, s, t: D.reloj(lz, x, y, 1.05 * s, t),
    "dia_noche": lambda lz, x, y, s, t: D.dia_noche(lz, x, y, 1.05 * s, t),
    "moneda_leon": lambda lz, x, y, s, t: D.moneda_leon(lz, x, y, 1.1 * s, 0.75 + 0.25 * math.cos(t * 1.2)),
    "piramides": lambda lz, x, y, s, t: D.piramides(lz, x - 70 * s, y + 120 * s, 0.9 * s),
    "carreta": lambda lz, x, y, s, t: D.carreta(lz, x - 60 * s, y + 130 * s, 0.75 * s, t),
    "balanza": lambda lz, x, y, s, t: D.balanza(lz, x, y + 170 * s, 1.0 * s, t, inclinacion=0.12 * math.sin(t * 2)),
    "cavernicola": _personaje("cave", mano_d=(150, -320)),
    "tu": _personaje("tu", accesorios=("auriculares",), mano_i=(-150, -320)),
    "neandertal": _personaje("neander"),
}


def dibujar_icono(lz, nombre, x, y, s, t):
    if nombre not in ICONOS:
        raise KeyError(f"Ícono '{nombre}' no existe. Opciones: {', '.join(sorted(ICONOS))}")
    ICONOS[nombre](lz, x, y, s, t)


# ============================================================ escenas genéricas (funcionan con cualquier guion)
_SLOTS = [(430, 360), (1490, 360), (430, 800), (1490, 800), (960, 830)]


class _ConClaves:
    """'claves' = [[palabra_ancla, texto_etiqueta], ...] -> la etiqueta aparece cuando se dice la palabra."""

    def preparar_claves(self):
        self.claves = []
        for i, (palabra, texto) in enumerate(self.d.get("claves", [])):
            tc = self.w(palabra, desde=1 if isinstance(self, Item) else 0)
            slot = _SLOTS[i % len(_SLOTS)]
            self.claves.append((tc, texto, slot))
            self.ev(tc, "pop", 0.5, pan=-0.5 if slot[0] < 960 else 0.5, tono=1.0 + 0.1 * i)

    def dibujar_claves(self, lz, t, desde=-1e9, hasta=1e9):
        for i, (tc, texto, (x, y)) in enumerate(self.claves):
            if desde <= tc < hasta:
                chip(lz, x, y + 8 * math.sin(t * 2 + i), texto, pop(t, tc, 0.3), 44, seed=400 + i,
                     rot=-0.03 + 0.02 * (i % 3))


def iconos_del_video(n=6):
    """Íconos únicos usados en el guion (icono + icono_hoy), repetidos en ciclo hasta n."""
    vistos = []
    for e in TL["escenas"]:
        for k in ("icono", "icono_hoy"):
            if e.get(k) and e[k] not in vistos:
                vistos.append(e[k])
    vistos = vistos or ["estrella"]
    return [vistos[i % len(vistos)] for i in range(max(n, len(vistos)))][:max(n, len(vistos))]


def partir_lineas(texto, n):
    out, cur = [], ""
    for p in texto.split():
        if len(cur) + len(p) + 1 > n and cur:
            out.append(cur)
            cur = p
        else:
            cur = (cur + " " + p).strip()
    return out + [cur] if cur else out


class IntroGenerica(_ConClaves, Escena):
    """Título del video (config.TITULO) con rebote + íconos de los ítems en órbita + claves."""

    def preparar(self):
        self.iconos = iconos_del_video(6)
        self.lineas = partir_lineas(config.TITULO.upper(), 22)
        for i in range(len(self.lineas)):
            self.ev(0.15 + 0.3 * i, "impacto" if i == 0 else "pop", 0.8, tono=0.9 + 0.1 * i)
        self.fin_titulo = self.fr[1]["t0"] - 0.2 if len(self.fr) > 1 else self.t1
        self.ev(self.fin_titulo, "whoosh", 0.5, dur=0.4)
        self.preparar_claves()

    def fondo(self, t):
        return mezcla_fondos(t, self.fin_titulo, lambda tt: fondo_estilo("titulo", tt, self.PAL, env_bombo(tt)),
                             lambda tt: fondo_estilo("libre", tt, self.PAL, env_bombo(tt)))

    def dibujar(self, lz, t):
        sube = e_inout(prog(t, self.fin_titulo - 0.1, self.fin_titulo + 0.4))
        esc = 1 - 0.55 * sube
        with lz.grupo(960, lerp(540, 185, sube), esc):
          with lz.grupo(-960, -540):
            n = len(self.lineas)
            px = 118 if n <= 3 else 92
            for i, lin in enumerate(self.lineas):
                k = pop(t, 0.15 + 0.3 * i, 0.35)
                if k > 0:
                    lz.texto(lin, 960, 540 - (n - 1) * px * 0.62 + i * px * 1.25, px, "snap",
                             color=color_arcoiris(t * 0.2 + i * 0.25), borde=NEGRO, borde_px=12, k=k,
                             rot=0.03 * math.sin(t * 2 + i), seed=10 + i)
        if sube > 0:
            m = len(self.iconos)
            for i, ic in enumerate(self.iconos):
                a = i / m * 2 * math.pi + t * 0.5
                dibujar_icono(lz, ic, 960 + 480 * math.cos(a), 650 + 170 * math.sin(a), 0.5 * sube, t)
        self.dibujar_claves(lz, t)


class ItemGenerico(_ConClaves, Item):
    """Ítem genérico: fase A = d['icono'] grande; fase B = d['icono'] a la izquierda -> d['icono_hoy'] a la derecha.
    Campos: icono, icono_hoy (opcional), claves (opcional), + los de Item (num, titulo, dato, fuente, sello...)."""
    ANTES_PERSISTE = True

    def escena(self):
        self.ic_a = self.d.get("icono", "estrella")
        self.ic_b = self.d.get("icono_hoy")
        self.ev(self.B + 0.15, "aparicion", 0.5)
        if self.ic_b:
            self.ev(self.C + 0.1, "boing", 0.6, pan=0.4)
        self.preparar_claves()

    def iconos_titulo(self, lz, t, x, y, s):
        for k in range(2):
            a = t * 1.4 + k * math.pi
            dibujar_icono(lz, self.ic_a, x + 340 * math.cos(a), y + 150 * math.sin(a), 0.28 * s, t)

    def antes(self, lz, t):
        k = pop(t, self.B + 0.15, 0.45)
        if k <= 0:
            return
        mov = e_inout(prog(t, self.C - 0.1, self.C + 0.4)) if self.ic_b else 0.0
        x, s = lerp(960, 520, mov), lerp(1.0, 0.7, mov)
        dibujar_icono(lz, self.ic_a, x, 560 + 14 * math.sin(t * 2), s * k * (1 + 0.03 * env_bombo(t)), t)
        self.dibujar_claves(lz, t, hasta=self.C)

    def hoy(self, lz, t):
        if self.ic_b:
            k = pop(t, self.C + 0.1, 0.4)
            if k > 0:
                flecha(lz, (820, 560), (1110, 560), prog(t, self.C + 0.1, self.C + 0.4), color=AMARILLO, ancho=16,
                       seed=77, curva=0.12)
                dibujar_icono(lz, self.ic_b, 1400, 560 + 14 * math.sin(t * 2 + 1), 0.7 * k, t)
        self.dibujar_claves(lz, t, desde=self.C)


class EscenaLibre(_ConClaves, Escena):
    """Escena sin número (para formatos que no son lista): d['icono'] al centro + claves."""

    def preparar(self):
        self.ic = self.d.get("icono", "estrella")
        self.ev(self.t0 + 0.1, "aparicion", 0.5)
        self.preparar_claves()

    def dibujar(self, lz, t):
        k = pop(t, self.t0 + 0.1, 0.45)
        if k > 0:
            dibujar_icono(lz, self.ic, 960, 560 + 14 * math.sin(t * 2), k, t)
        self.dibujar_claves(lz, t)


class OutroGenerico(_ConClaves, Escena):
    """Cierre: íconos de todos los ítems en órbita + tarjeta final (d['cierre']) + fundido a negro."""

    def preparar(self):
        self.iconos = iconos_del_video(6)
        self.fin = self.fr[-1]["t1"] + 0.12
        self.ev(self.fr[0]["t0"], "brillo", 0.6)
        self.ev(self.fin, "impacto", 0.9)
        self.preparar_claves()

    def fondo(self, t):
        return mezcla_fondos(t, self.fin, lambda tt: fondo_estilo("libre", tt, self.PAL, env_bombo(tt)),
                             lambda tt: fondo_estilo("titulo", tt, self.PAL, env_bombo(tt)))

    def dibujar(self, lz, t):
        if t < self.fin + 0.2:
            fuera = e_in(prog(t, self.fin - 0.1, self.fin + 0.2))
            m = len(self.iconos)
            for i, ic in enumerate(self.iconos):
                a = i / m * 2 * math.pi + t * 0.6
                k = pop(t, self.fr[0]["t0"] + 0.1 * i, 0.35) * (1 - fuera)
                if k > 0:
                    dibujar_icono(lz, ic, 960 + 500 * math.cos(a), 600 + 200 * math.sin(a), 0.5 * k, t)
            self.dibujar_claves(lz, t)
        if t >= self.fin:
            for i, lin in enumerate(partir_lineas(self.d.get("cierre", "¿CUÁL TE SORPRENDIÓ MÁS?"), 18)):
                lz.texto(lin, 960, 380 + i * 140, 110, "snap", color=AMARILLO if i == 0 else BLANCO, borde=NEGRO,
                         borde_px=12, k=pop(t, self.fin + 0.15 * i, 0.4), rot=-0.03, seed=150 + i)

    def render(self, lz, t):
        img = Escena.render(self, lz, t)
        neg = prog(t, self.t1 - 0.6, self.t1 - 0.05)
        return img * (1 - neg) if neg > 0 else img


def clases_automaticas(propias=None):
    """id -> clase: usa `propias` si la escena tiene clase a medida; si no, la genérica según posición/campos."""
    propias = propias or {}
    n = len(TL["escenas"])
    out = {}
    for k, e in enumerate(TL["escenas"]):
        if e["id"] in propias:
            out[e["id"]] = propias[e["id"]]
        elif k == 0:
            out[e["id"]] = IntroGenerica
        elif k == n - 1:
            out[e["id"]] = OutroGenerico
        elif "num" in e:
            out[e["id"]] = ItemGenerico
        else:
            out[e["id"]] = EscenaLibre
    return out
