# -*- coding: utf-8 -*-
"""Estilo NOIR COLOR (neo-noir apagado): la misma esencia del noir en tinta y aguada (claroscuro, persianas, lluvia que solo brilla
donde hay luz, niebla, humo, tramado de plumilla, papel, grano y polvo) pero con un POCO de color, siempre oscuro y desaturado:
sombras frías (azul acero / verde petróleo), luces de sodio ámbar y UN acento (neón rojo, lámpara verde) por plano.

Cómo se consigue sin perder el noir: todo se sigue pensando en VALORES (tono 0..255 como en noir.py); el color sale de
  1) RAMPAS por material (mapa de degradado: el valor elige el color, de lo oscuro-frío a lo claro-cálido) -> `h.pieza(..., rampa=)`,
     `pegar(capa, h, rampa=)` para los fondos pintados en gris con noir_fondos.Lienzo;
  2) LUCES DE COLOR (sodio, luna, neón) que multiplican el cuadro -> la lluvia, el humo y la niebla toman el color de la luz;
  3) un ETALONAJE final (`PALETAS`): curva S sobre la luminancia, saturación baja (~0,5), negro tintado, sombras frías y luces cálidas.

    h = NoirColor("sodio")                       # una por proceso; paletas: sodio · bourbon · medianoche
    h.nuevo(t)
    pegar(capa, h, 0.6, rampa="ladrillo", bruma=0.3)       # Capa de noir_fondos (gris) -> color por rampa
    h.pieza(P, 78, sem, rampa="gabardina")                 # o `with h.con_rampa("piel"):` alrededor de lo que dibuje un personaje
    h.luz_cono(x, y, ang, abre, largo, h.pal["sodio"], k=1.4); h.luz_persiana(quad, k=0.9, col=h.pal["luna"])
    h.emitir(P, 1.0, col=h.pal["neon"])                    # neón / bombilla / brasa con su color
    img = h.acabado(t, niebla=dict(dens=0.3))              # float32 HxWx3 en color apagado

Los personajes de noir_pers (Detective, Busto, Figura) funcionan tal cual: sin rampa usan `rampa_personaje` (valor -> gabardina
caqui, piel cálida, camisa crema, sombras azul tinta). Texto (`noir.texto_maquina`, `noir.sello`) acepta `tono=` RGB 0..1 para el
acento: `N.sello(h, "CASO ABIERTO", ..., tono=h.pal["sello"])`.
Doc: docs/estilo_noir_color.md. Prueba: videos/prueba_noir_color/.
"""
import contextlib
import math

import cv2
import numpy as np

from motor import H, W
import noir as N
import toon as TN
from noir import SW, SH, AW, AH, Noir, papel, niebla_tex, _vineta_noir, _trama, _polvo

# ================================================================ rampas (mapas de degradado por material)
# (valor 0..1, (r, g, b) 0..1). Lo oscuro va a tinta fría; lo claro, a cálido apagado. Nada muy saturado: el etalonaje baja más.
RAMPAS = {
    "neutro": [(0, (0, 0, 0)), (1, (1, 1, 1))],
    "personaje": [(0.00, (0.020, 0.028, 0.045)), (0.10, (0.060, 0.070, 0.090)), (0.22, (0.200, 0.180, 0.150)),
                  (0.32, (0.360, 0.300, 0.215)), (0.46, (0.600, 0.430, 0.330)), (0.62, (0.760, 0.600, 0.480)),
                  (0.78, (0.860, 0.820, 0.720)), (1.00, (0.980, 0.950, 0.880))],
    "gabardina": [(0.00, (0.020, 0.025, 0.040)), (0.15, (0.120, 0.110, 0.090)), (0.32, (0.400, 0.330, 0.220)),
                  (0.55, (0.620, 0.530, 0.380)), (1.00, (0.950, 0.900, 0.780))],
    "piel": [(0.00, (0.030, 0.025, 0.035)), (0.20, (0.250, 0.150, 0.120)), (0.46, (0.660, 0.460, 0.360)),
             (0.70, (0.840, 0.680, 0.560)), (1.00, (0.990, 0.930, 0.850))],
    "ladrillo": [(0.00, (0.020, 0.022, 0.040)), (0.12, (0.110, 0.070, 0.075)), (0.24, (0.300, 0.150, 0.110)),
                 (0.45, (0.520, 0.320, 0.230)), (0.75, (0.780, 0.640, 0.500)), (1.00, (0.980, 0.900, 0.760))],
    "piedra": [(0.00, (0.020, 0.030, 0.045)), (0.20, (0.150, 0.170, 0.190)), (0.45, (0.400, 0.410, 0.410)),
               (1.00, (0.920, 0.900, 0.850))],
    "lejos": [(0.00, (0.020, 0.035, 0.060)), (0.30, (0.170, 0.230, 0.290)), (0.60, (0.420, 0.500, 0.560)),
              (1.00, (0.900, 0.880, 0.800))],
    "cielo": [(0.00, (0.010, 0.020, 0.040)), (0.30, (0.090, 0.150, 0.200)), (0.60, (0.300, 0.380, 0.430)),
              (1.00, (0.800, 0.820, 0.800))],
    "asfalto": [(0.00, (0.015, 0.022, 0.035)), (0.15, (0.080, 0.100, 0.120)), (0.40, (0.280, 0.300, 0.300)),
                (1.00, (0.900, 0.870, 0.800))],
    "madera": [(0.00, (0.025, 0.020, 0.025)), (0.18, (0.180, 0.100, 0.060)), (0.40, (0.430, 0.260, 0.150)),
               (0.70, (0.700, 0.520, 0.340)), (1.00, (0.960, 0.860, 0.700))],
    "papel": [(0.00, (0.030, 0.030, 0.040)), (0.40, (0.420, 0.380, 0.300)), (0.75, (0.820, 0.760, 0.620)),
              (1.00, (0.980, 0.940, 0.820))],
    "laton": [(0.00, (0.030, 0.025, 0.020)), (0.30, (0.330, 0.220, 0.080)), (0.65, (0.760, 0.580, 0.280)),
              (1.00, (1.000, 0.920, 0.700))],
    "vidrio_verde": [(0.00, (0.010, 0.030, 0.025)), (0.30, (0.050, 0.220, 0.150)), (0.65, (0.250, 0.560, 0.380)),
                     (1.00, (0.800, 0.980, 0.820))],
    "vino": [(0.00, (0.030, 0.010, 0.020)), (0.30, (0.300, 0.050, 0.070)), (0.65, (0.620, 0.170, 0.150)),
             (1.00, (0.980, 0.700, 0.600))],
    "whisky": [(0.00, (0.040, 0.020, 0.010)), (0.30, (0.400, 0.180, 0.040)), (0.65, (0.820, 0.480, 0.150)),
               (1.00, (1.000, 0.880, 0.600))],
    "tela_verde": [(0.00, (0.015, 0.030, 0.025)), (0.30, (0.090, 0.200, 0.150)), (0.60, (0.260, 0.420, 0.320)),
                   (1.00, (0.800, 0.880, 0.780))],
}


def _lut(stops, n=256):
    xs = np.array([s[0] for s in stops], np.float32)
    cs = np.array([s[1] for s in stops], np.float32)
    u = np.linspace(0, 1, n, dtype=np.float32)
    return np.stack([np.interp(u, xs, cs[:, c]) for c in range(3)], 1).astype(np.float32)


_LUTS = {}


def lut(rampa):
    """LUT 256x3 (0..1) de una rampa (nombre de RAMPAS o lista de paradas)."""
    if isinstance(rampa, str):
        if rampa not in _LUTS:
            _LUTS[rampa] = _lut(RAMPAS[rampa])
        return _LUTS[rampa]
    return _lut(rampa)


def col(rampa, v):
    """Color 0..255 (r, g, b) del valor v (0..255) en la rampa."""
    c = lut(rampa)[int(max(0, min(255, v)))]
    return (float(c[0] * 255), float(c[1] * 255), float(c[2] * 255))


# ================================================================ paletas (etalonaje + colores de luz con nombre)
# sat: saturación global tras la curva S (0 = B/N, 1 = la del dibujo). sombra/luz: tinte multiplicativo por zonas (split toning).
PALETAS = {
    # Sodio y neón: calle de noche, farolas ámbar contra sombras azul acero; acento neón rojo. La de referencia.
    "sodio": dict(sat=0.62, negro=(0.016, 0.024, 0.034), blanco=(0.97, 0.93, 0.84), sombra=(0.84, 0.99, 1.14),
                  luz=(1.10, 0.99, 0.82), niebla=(0.06, 0.09, 0.115), aditivo=(0.55, 0.70, 0.85),
                  colores=dict(sodio=(1.55, 1.02, 0.52), luna=(0.62, 0.80, 1.0), neon=(1.0, 0.16, 0.14), lampara=(1.45, 1.05, 0.62),
                               verde=(0.45, 1.0, 0.62), relampago=(0.80, 0.90, 1.0), sello=(0.55, 0.06, 0.05),
                               tinta=(0.025, 0.03, 0.045), papel=(0.93, 0.88, 0.74))),
    # Bourbon: interiores de oficina, fluorescente verdoso en la sombra y whisky en las luces; acento vino.
    "bourbon": dict(sat=0.55, negro=(0.020, 0.026, 0.022), blanco=(0.96, 0.92, 0.80), sombra=(0.90, 1.06, 0.98),
                    luz=(1.12, 0.98, 0.76), niebla=(0.07, 0.085, 0.07), aditivo=(0.70, 0.80, 0.65),
                    colores=dict(sodio=(1.50, 1.05, 0.55), luna=(0.70, 0.90, 0.85), neon=(0.85, 0.12, 0.20), lampara=(1.40, 1.08, 0.66),
                                 verde=(0.50, 1.0, 0.58), relampago=(0.85, 0.95, 0.90), sello=(0.48, 0.05, 0.10),
                                 tinta=(0.03, 0.035, 0.03), papel=(0.92, 0.86, 0.70))),
    # Medianoche: azul profundo y violeta, neón magenta-rojo; la más fría.
    "medianoche": dict(sat=0.58, negro=(0.014, 0.018, 0.040), blanco=(0.94, 0.93, 0.96), sombra=(0.86, 0.92, 1.20),
                       luz=(1.04, 0.98, 0.92), niebla=(0.06, 0.07, 0.13), aditivo=(0.60, 0.68, 0.95),
                       colores=dict(sodio=(1.35, 1.0, 0.70), luna=(0.55, 0.70, 1.10), neon=(1.0, 0.14, 0.40), lampara=(1.30, 1.05, 0.80),
                                    verde=(0.40, 1.0, 0.75), relampago=(0.75, 0.85, 1.05), sello=(0.50, 0.05, 0.14),
                                    tinta=(0.02, 0.025, 0.05), papel=(0.90, 0.88, 0.84))),
}


# ================================================================ lienzo
class NoirColor(Noir):
    """Noir con color apagado. Mantiene la interfaz de Noir: lo que funciona con Noir (personajes, texto, lluvia, humo,
    transiciones) funciona aquí; los colores se piden por rampa o por nombre de la paleta (`h.pal["sodio"]`)."""

    def __init__(self, paleta="sodio"):
        super().__init__()
        self.usar_paleta(paleta)
        self.rampa_personaje = "personaje"
        self._rampa = None
        self._Ec = None

    def usar_paleta(self, paleta):
        self.paleta = paleta
        self.P = PALETAS[paleta] if isinstance(paleta, str) else paleta
        self.pal = dict(self.P["colores"])

    def nuevo(self, t, fondo=None, tinte=(1, 1, 1)):
        super().nuevo(t, fondo, tinte)
        self._Ec = None
        self._rim_col = None

    # -------------------------------------------------------- rampas
    @contextlib.contextmanager
    def con_rampa(self, rampa):
        """Todo lo que se dibuje con pieza() dentro del bloque usa esta rampa (un personaje entero, un coche...)."""
        prev = self._rampa
        self._rampa = rampa
        try:
            yield
        finally:
            self._rampa = prev

    def c(self, v, rampa=None):
        """Color 0..255 del valor v (0..255) en la rampa indicada o la activa."""
        return col(rampa or self._rampa or self.rampa_personaje, v)

    def rim_color(self, c):
        """Color del contraluz (rim) de las piezas: el de la luz principal del plano (None = crema neutro)."""
        self._rim_col = c

    # -------------------------------------------------------- emisión en color
    def emisivo(self):
        if self._E is None:
            self._E = np.zeros((H, W), np.float32)
        return self._E

    def _color_emision(self):
        if self._Ec is None:
            self._Ec = np.empty((H, W, 3), np.float32)
            self._Ec[:] = np.array(self.pal["lampara"], np.float32) / max(self.pal["lampara"])
        return self._Ec

    def teñir_emision(self, a, x0, y0, c):
        """Marca con el color c la emisión dentro de la máscara a (float 0..1) en (x0, y0)."""
        Ec = self._color_emision()
        c = np.asarray(c, np.float32)
        c = c / max(1e-6, float(c.max()))
        sl = Ec[y0:y0 + a.shape[0], x0:x0 + a.shape[1]]
        aa = a[:sl.shape[0], :sl.shape[1], None]
        sl += (c - sl) * aa

    def emitir(self, P, v, mundo=True, blur=1.0, col=None):
        """Polígono que emite luz con intensidad v y color col (por defecto la lámpara de la paleta)."""
        Q = self.tf(P) if mundo else np.asarray(P, float)
        r = self.mascara([Q], m=4 + int(3 * blur))
        if r is None:
            return
        mk, x0, y0 = r
        a = mk.astype(np.float32) / 255.0
        if blur > 0:
            a = cv2.GaussianBlur(a, (0, 0), blur)
        E = self.emisivo()
        sl = E[y0:y0 + a.shape[0], x0:x0 + a.shape[1]]
        np.maximum(sl, a * v, out=sl)
        self.teñir_emision(a, x0, y0, col if col is not None else self.pal["lampara"])

    def resplandor(self, x, y, r, v, col=None, mundo=True):
        """Halo emisivo suave (bombilla, neón) de radio r: ilumina el aire alrededor de la fuente."""
        if mundo:
            x, y = self.tf(np.array([[x, y]]))[0]
            r *= self.zoom
        x0, y0 = int(max(0, x - r)), int(max(0, y - r))
        x1, y1 = int(min(W, x + r + 1)), int(min(H, y + r + 1))
        if x1 <= x0 or y1 <= y0:
            return
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / max(1.0, r)
        a = np.clip(1 - d, 0, 1) ** 2.2
        E = self.emisivo()
        E[y0:y1, x0:x1] += a * v
        self.teñir_emision(np.clip(a * 3, 0, 1), x0, y0, col if col is not None else self.pal["lampara"])

    # -------------------------------------------------------- luces en color
    def luz_persiana(self, quad, k=1.0, tipo="persiana", n=16, abierto=0.55, suave=1.6, mundo=True, col=None):
        Q = self.tf(quad) if mundo else np.asarray(quad, float)
        src = np.float32([[0, 0], [255, 0], [255, 255], [0, 255]])
        M = cv2.getPerspectiveTransform(src, np.float32(Q / 3.0))
        pat = cv2.warpPerspective(N._patron(tipo, n, round(abierto, 2)), M, (SW, SH), flags=cv2.INTER_LINEAR)
        if suave > 0:
            pat = cv2.GaussianBlur(pat, (0, 0), suave)
        self._extra.append((pat * k, np.asarray(col if col is not None else (1, 1, 1), np.float32)))

    def luz_mascara(self, m, k=1.0, col=None):
        if m.shape[0] != SH:
            m = cv2.resize(m, (SW, SH), interpolation=cv2.INTER_AREA)
        self._extra.append((m * k, np.asarray(col if col is not None else (1, 1, 1), np.float32)))

    def mapa_rgb(self):
        yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
        xx *= 3
        yy *= 3
        L = np.empty((SH, SW, 3), np.float32)
        L[:] = self.ambiente
        for lz in self.luces:
            if lz[0] == "r":
                _, x, y, r, c, k = lz
                d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / max(1.0, r)
                L += (np.clip(1 - d, 0, 1) ** 2 * k)[..., None] * c
            else:
                _, x, y, ang, abre, largo, c, k, suave = lz
                dx, dy = xx - x, yy - y
                d = np.sqrt(dx * dx + dy * dy) + 1e-3
                th = np.arccos(np.clip((dx * math.cos(ang) + dy * math.sin(ang)) / d, -1, 1))
                lat = np.clip((abre - th) / (abre * suave + 1e-4), 0, 1)
                lat = lat * lat * (3 - 2 * lat)
                lon = np.clip(1 - d / largo, 0, 1) ** 0.8
                L += (lat * lon * k)[..., None] * c
        for e in self._extra:
            if isinstance(e, tuple):
                L += e[0][..., None] * e[1]
            else:
                L += e[..., None]
        for Q, v in self._fijas:                          # luz fija (rótulos): máscara, porque cv2 no escribe en un canal suelto
            m = np.zeros((SH, SW), np.uint8)
            cv2.fillConvexPoly(m, Q, 255, cv2.LINE_AA)
            a = (m.astype(np.float32) * (1 / 255.0))[..., None]
            L *= 1 - a
            L += a * float(v)
        return L

    def mapa_gris(self):                                  # compatibilidad (quien lo pida en gris)
        L = self.mapa_rgb()
        return L[..., 0] * 0.3 + L[..., 1] * 0.59 + L[..., 2] * 0.11

    # -------------------------------------------------------- piezas
    def pieza(self, P, tono, sem=0, w=7.0, luz=(0.25, -1.0), d=22.0, sombra=0.6, trama=0.75, rim=0.0, rim_tono=238,
              tex=0.06, linea=True, jit=2.0, alfa=1.0, sketch=0.25, grad=None, rampa=None):
        """Igual que Noir.pieza pero en color: el valor `tono` se lee en la rampa (la dada, la activa o la del personaje);
        la sombra es el mismo material más oscuro (más frío) y el rim toma el color de la luz principal (`rim_color`)."""
        rp = rampa or self._rampa or self.rampa_personaje
        Pw = self.tf(P)
        Pj = self._jit(TN._remu(Pw, 4.0, True)[:-1] if len(Pw) > 8 else Pw, jit * self.zoom, sem)
        o = (1.5 * math.sin(self.dib * 2.1 + sem), 1.5 * math.cos(self.dib * 1.7 + sem * 2))
        g = None if grad is None else (col(rp, grad[0]), grad[1], grad[2])
        r = self.relleno(Pj, col(rp, tono), grad=g, alfa=alfa, tex=tex, off=o)
        if r is not None and self.silueta is None:
            mk, x0, y0 = r
            ln = math.hypot(*luz) + 1e-9
            lx, ly = luz[0] / ln, luz[1] / ln
            dz = d * self.zoom
            if sombra > 0:
                b = self._banda(mk, -lx * dz, -ly * dz, 1.2)
                self._pintar(b, x0, y0, col(rp, tono * 0.42), alfa=sombra * alfa, tex=0.03)
                if trama > 0:
                    b2 = self._banda(mk, -lx * dz * 1.9, -ly * dz * 1.9, 1.0)
                    tr = _trama(self.dib % 3)[y0:y0 + mk.shape[0], x0:x0 + mk.shape[1]]
                    hb = (b2.astype(np.float32) * tr[:b2.shape[0], :b2.shape[1]]).astype(np.uint8)
                    self._pintar(hb, x0, y0, col(rp, 10), alfa=trama * alfa, tex=0.0)
            if rim > 0:
                rb = self._banda(mk, lx * dz * 0.32, ly * dz * 0.32, 0.8)
                if self._rim_col is not None:
                    c = np.asarray(self._rim_col, np.float32)
                    rc = tuple(float(v) for v in np.clip(c / max(1e-6, c.max()) * rim_tono, 0, 255))
                else:
                    rc = col(rp, rim_tono)
                self._pintar(rb, x0, y0, rc, alfa=rim * alfa, tex=0.0)
        if linea and w > 0:
            self.anillo(Pj, w, sem, color=tuple(v * 255 for v in self.pal["tinta"]), alfa=alfa, peso_luz=0.6, jit=0.0,
                        sketch=sketch)
        return r

    # -------------------------------------------------------- acabado en color
    def acabado(self, t, *, negro=None, blanco=None, contraste=5.2, medio=0.44, tinta=0.55, niebla=None, brillo_A=1.0,
                A_base=0.05, bloom=0.4, grano=0.065, polvo=1.0, vin=1.0, flash=0.0, parpadeo=0.02, oscuro=1.0, sat=None,
                col_A=None):
        """Luz de color, emisión, niebla, lluvia/humo, halo, tinta y curva S en LUMINANCIA; luego el color se devuelve con la
        saturación de la paleta (`sat`), negro y blanco tintados, sombras frías / luces cálidas, papel, grano, polvo y viñeta."""
        Pp = self.P
        rgb = self.img
        L3 = self.mapa_rgb()
        L = cv2.resize(L3, (W, H), interpolation=cv2.INTER_LINEAR)
        rgb = rgb * L
        if self._E is not None:
            Ec = self._Ec if self._Ec is not None else np.asarray(self.pal["lampara"], np.float32) / max(self.pal["lampara"])
            rgb += self._E[..., None] * Ec
        if niebla is not None:
            dens, vel, y0, y1 = niebla.get("dens", 0.3), niebla.get("vel", 30.0), niebla.get("y0", 0), niebla.get("y1", H)
            tx = niebla_tex(niebla.get("sem", 0))
            off = int(t * vel / 3) % SW
            n = tx[:, off:off + SW]
            yy = np.arange(SH, dtype=np.float32)[:, None] * 3
            g = np.clip((yy - y0) / max(1.0, (y1 - y0)), 0, 1)
            g = g * g * (3 - 2 * g) if niebla.get("sube", True) else 1 - g
            d3 = np.clip(dens * n * (0.35 + 0.65 * g) * 1.6, 0, 0.9)
            ncol = np.asarray(niebla.get("col", Pp["niebla"]), np.float32)
            f3 = d3[..., None] * (ncol + 0.75 * np.clip(L3 - 0.12, 0, None))
            d = cv2.resize(d3, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
            f = cv2.resize(f3, (W, H), interpolation=cv2.INTER_LINEAR)
            rgb = rgb * (1 - d) + f
        if self._A is not None:
            A = cv2.GaussianBlur(self._A, (0, 0), 0.7)
            A = cv2.resize(A, (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
            ca = np.asarray(col_A if col_A is not None else Pp["aditivo"], np.float32)
            rgb = rgb + A * brillo_A * (A_base * ca + 0.9 * np.clip(L - 0.1, 0, 1.6))
        if bloom > 0:                                       # halo de película: las luces fuertes sangran su color
            br = np.clip(rgb - 0.7, 0, None)
            g = cv2.GaussianBlur(cv2.resize(br, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 10)
            rgb = rgb + cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR) * bloom * 2.2
        Y = rgb[..., 0] * 0.3 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11
        if tinta > 0:                                       # tinta: bordes nítidos y oscuros (sobre la luminancia)
            b = cv2.GaussianBlur(Y, (0, 0), 2.4)
            Yt = Y + tinta * (Y - b)
            b2 = cv2.GaussianBlur(Yt, (0, 0), 9)
            Yt = Yt + 0.25 * tinta * (Yt - b2)
        else:
            Yt = Y
        x = np.clip(Yt, 0, 1.4)
        y = 1 / (1 + np.exp(-contraste * (x - medio)))
        ya, yb = 1 / (1 + math.exp(contraste * medio)), 1 / (1 + math.exp(-contraste * (1.4 - medio)))
        y = (y - ya) / (yb - ya)
        # crominancia: proporción de cada canal sobre la luminancia, apagada por la saturación de la paleta
        s = Pp["sat"] if sat is None else sat
        Ys = np.maximum(Y, 1e-3)[..., None]
        ratio = np.clip(rgb / Ys, 0, 3.5)
        fia = np.clip(Y / 0.03, 0, 1)[..., None]          # en el negro puro la proporción no significa nada
        ratio = 1 + (ratio - 1) * (s * fia)
        if flash > 0:
            y = y + flash * (1 - y) * 0.85
            fr = np.asarray(self.pal["relampago"], np.float32)
            ratio = ratio + (fr / fr.mean() - ratio) * min(1.0, flash)
        out = y[..., None] * ratio
        ng = np.asarray(negro if negro is not None else Pp["negro"], np.float32)
        bl = np.asarray(blanco if blanco is not None else Pp["blanco"], np.float32)
        out = ng + (bl - ng) * out
        w = np.clip(y, 0, 1)[..., None]                     # sombras frías, luces cálidas
        ts, tl = np.asarray(Pp["sombra"], np.float32), np.asarray(Pp["luz"], np.float32)
        out *= ts + (tl - ts) * (w * w * (3 - 2 * w))
        out *= papel()[..., None]
        if grano > 0:
            gr = TN._banco_grano()[int(t * 24) % 6]
            yy_ = np.clip(y, 0, 1)
            out += (grano * 0.55 * gr * (0.35 + 0.65 * yy_ * (1 - yy_) * 4))[..., None]
        if parpadeo > 0:
            out *= 1 + parpadeo * math.sin(t * 24 * 2.1) * math.sin(t * 7.3)
        if polvo > 0:
            yp = np.clip(y, 0, 1).astype(np.float32)
            base = yp.copy()
            _polvo(yp, t, polvo)
            out += (yp - base)[..., None]
        if vin > 0:
            out *= (1 - vin * (1 - _vineta_noir()))[..., None]
        if oscuro < 1:
            out *= oscuro
        np.clip(out, 0, 1, out=out)
        return out.astype(np.float32)


# ================================================================ fondos pintados (noir_fondos.Lienzo, gris) -> color
def pegar(capa, h, prof=1.0, rampa="piedra", oscuro=1.0, dx=0.0, dy=0.0, emis=1.0, bruma=0.0, col_bruma=None,
          col_emis=None):
    """Compone una Capa gris de noir_fondos con la cámara (paralaje prof), leyendo cada valor en la rampa del material.
    bruma: perspectiva aérea hacia el color de niebla de la paleta (o col_bruma). Las ventanas encendidas (emisión) van a la
    capa emisiva con col_emis (por defecto la lámpara: ventanas ámbar)."""
    M = h.matriz_capa(prof) @ np.array([[1, 0, capa.ox + dx], [0, 1, capa.oy + dy], [0, 0, 1]], float)
    g = cv2.warpAffine(capa.g, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    if oscuro != 1.0:
        g = np.clip(g.astype(np.float32) * oscuro, 0, 255).astype(np.uint8)
    v = lut(rampa)[g]                                     # (H, W, 3) 0..1
    if bruma > 0:
        cb = np.asarray(col_bruma if col_bruma is not None else np.asarray(h.P["niebla"]) * 4.0, np.float32)
        v = v * (1 - bruma) + cb * bruma
    if capa.a is None:
        h.img[:] = v
        af = None
    else:
        a = cv2.warpAffine(capa.a, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        af = a.astype(np.float32) * (1 / 255.0)
        h.img *= (1 - af)[..., None]
        h.img += v * af[..., None]
    if h._E is not None and af is not None:
        h._E *= 1 - af
    if capa.e is not None and emis > 0:
        e = cv2.warpAffine(capa.e, M[:2], (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        ef = e.astype(np.float32) * (emis / 255.0)
        E = h.emisivo()
        E += ef
        h.teñir_emision(np.clip(ef * 4, 0, 1), 0, 0, col_emis if col_emis is not None else h.pal["lampara"])
