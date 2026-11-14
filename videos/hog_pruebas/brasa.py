# -*- coding: utf-8 -*-
"""ESTILO 1 · BRASA: todo está hecho de fuego. Él recortado con luz de hoguera, imágenes reales en paleta de brasa
que se encienden como papel quemándose, palabras marcadas con hierro candente, llamas y chispas continuas."""
import functools, math
import cv2, numpy as np
from comun import *

XS = np.array([0.0, 0.30, 0.55, 0.80, 1.0], np.float32)
CAL = [np.array(c, np.float32) for c in ([0.02, 0.45, 1.0, 1.0, 1.0], [0.01, 0.05, 0.36, 0.76, 0.96], [0.01, 0.02, 0.04, 0.30, 0.82])]


def calor(x):
    """0..1 → negro, rojo brasa, naranja, amarillo, blanco."""
    return np.dstack([np.interp(x, XS, c) for c in CAL]).astype(np.float32)


def teja(tex):
    """Hace la textura envolvente en vertical."""
    h = tex.shape[0]
    w = np.abs(np.linspace(-1, 1, h, dtype=np.float32))[:, None]
    return tex * (1 - w) + np.roll(tex, h // 2, 0) * w


def lum(rgb):
    return rgb[..., 0] * 0.3 + rgb[..., 1] * 0.59 + rgb[..., 2] * 0.11


class Lamina:
    """Imagen real en paleta de brasa, con borde quemado; entra y sale ardiendo."""

    def __init__(s, rgb, ancho, semilla, alfa=None, redonda=False, gamma=1.0):
        h = int(rgb.shape[0] * ancho / rgb.shape[1])
        rgb = cv2.resize(rgb, (ancho, h), interpolation=cv2.INTER_AREA)
        l = lum(rgb)
        l = cv2.createCLAHE(2.2, (6, 6)).apply((l * 255).astype(np.uint8)).astype(np.float32) / 255
        s.l = (l ** gamma) * 0.92 + 0.04
        yy, xx = np.mgrid[0:h, 0:ancho].astype(np.float32)
        n = ruido(h, ancho, 90, semilla)
        if alfa is not None:
            s.forma = cv2.resize(alfa, (ancho, h), interpolation=cv2.INTER_AREA)
        elif redonda:
            d = np.hypot((xx - ancho / 2) / (ancho / 2), (yy - h / 2) / (h / 2))
            s.forma = np.clip((0.97 - d + (n - .5) * .07) / 0.03, 0, 1)
        else:
            d = np.minimum(np.minimum(xx, ancho - 1 - xx), np.minimum(yy, h - 1 - yy)) / 46.0
            s.forma = np.clip((d - 0.15 - n * 0.75) / 0.12, 0, 1)
        dc = np.hypot((xx - ancho * .5) / ancho, (yy - h * .5) / h)
        r = 0.55 * ruido(h, ancho, 150, semilla + 7) + 0.45 * dc / dc.max()
        s.r = (r - r.min()) / (r.max() - r.min())
        r2 = ruido(h, ancho, 120, semilla + 13)
        s.r2 = r2
        s.bri = teja(ruido(h, ancho, 60, semilla + 3))
        s.h, s.w = h, ancho

    def sprite(s, t, t0, t1, din=0.55, dout=0.45):
        p, q = rampa(t, t0, din), rampa(t, t1 - dout, dout)
        if p <= 0 or q >= 1:
            return None
        fr = p * 1.2 - s.r
        vis = np.clip(fr / 0.05, 0, 1)
        glow = np.exp(-(fr / 0.06) ** 2) * (1 if p < 1 else 0)
        if q > 0:
            fq = q * 1.2 - s.r2
            vis = vis * (1 - np.clip(fq / 0.05, 0, 1))
            glow = glow + np.exp(-(fq / 0.07) ** 2)
        a = s.forma * vis
        x = s.l * (0.86 + 0.30 * desplaza(s.bri, 0, -t * 34))
        rgb = calor(np.clip(x, 0, 1)) * a[..., None]
        rgb += (glow * s.forma)[..., None] * np.array([1.6, 0.75, 0.18], np.float32)
        return np.dstack([rgb, a]).astype(np.float32)


@functools.lru_cache(maxsize=64)
def _marca(txt, tam, fuente, esp):
    a = np.pad(texto(txt, fuente, tam, (1, 1, 1), esp=esp)[..., 3], 50)
    return a, cv2.GaussianBlur(a, (0, 0), 17), cv2.GaussianBlur(a, (0, 0), 7), ruido(a.shape[0], a.shape[1], 26, len(txt))


def marca(L, txt, tam, cx, cy, t, t0, t1, fuente=F_IMPACT, esp=5):
    """Palabra marcada con hierro candente: entra al rojo blanco y se enfría a brasa."""
    if t < t0 or t > t1 + 0.35:
        return 0.0
    a, g, sm, n = _marca(txt, tam, fuente, esp)
    hot = golpe(t, t0, 1.1)
    op = 1 - rampa(t, t1, 0.35)
    k = 1.32 - 0.32 * sale(rampa(t, t0, 0.14))
    fill = calor(np.clip(0.60 + 0.38 * hot + (n - .5) * 0.28, 0, 1))
    sp = np.dstack([fill * a[..., None], a])
    sh = np.dstack([np.zeros(a.shape + (3,), np.float32), np.clip(sm * 1.5, 0, 1) * 0.85])
    gl = np.dstack([g[..., None] * np.array([1.0, 0.42, 0.08], np.float32) * (0.45 + 1.2 * hot), g])
    for q, kw in ((sh, {}), (gl, dict(suma=True)), (sp, {})):
        pegar(L, transf(q, k), cx, cy, op, **kw)
    return golpe(t, t0, 0.22)


class Brasa:
    def __init__(s):
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        base = np.dstack([0.030 + 0.07 * (yy / H) ** 2, 0.016 + 0.02 * (yy / H) ** 2, 0.012 + 0.006 * yy / H])
        d = np.hypot((xx - 540) / 760, (yy - 1560) / 900)
        s.resplandor = np.clip(1 - d, 0, 1)[..., None] ** 2 * np.array([0.55, 0.16, 0.03], np.float32)
        s.fondo = base.astype(np.float32)
        s.humo = teja(ruido(H // 4, W // 4, 70, 5))
        s.vin = (1 - 0.55 * np.clip(np.hypot((xx - 540) / 800, (yy - 960) / 1250) - 0.45, 0, 1) ** 1.5)[..., None].astype(np.float32)
        s.f1 = teja(teja(ruido(690, 540, 60, 21, 3)).T).T.copy(); s.f2 = teja(teja(ruido(690, 540, 26, 22, 3)).T).T.copy()
        gy = np.linspace(0, 1, 230, dtype=np.float32)[:, None]
        s.falt = gy ** 1.25
        rng = np.random.default_rng(4)
        s.ch = rng.random((90, 6)).astype(np.float32)          # chispas: x, velocidad, fase, tamaño, vaivén, capa
        k = np.exp(-((np.mgrid[-8:9, -8:9] ** 2).sum(0)) / 9.0).astype(np.float32)
        s.kch = np.dstack([k[..., None] * np.array([1.0, 0.55, 0.12], np.float32), k])
        # ---- láminas ----
        fr, fa = recorte_fugu(860)
        s.fugu = Lamina(fr, 860, 1, alfa=fa, gamma=0.8)
        tt = cargar("ttx", 900)
        s.ttx = Lamina(tt, 900, 2, alfa=np.clip(tt.max(2) * 4, 0, 1), gamma=0.7)
        s.sharaku = Lamina(cargar("sharaku", 640)[20:-20, 16:-16], 520, 3, gamma=0.9)
        b = cargar("bando", 600)
        s.bando = Lamina(b[30:780], 590, 4, gamma=0.85)
        p = cargar("sashimi", 1100)
        s.plato = Lamina(p[10:730, 0:735], 640, 5, redonda=True, gamma=0.8)
        cil = m_cilindro(560)
        s.cil = np.dstack([calor(0.30 + 0.22 * ruido(560, 560, 40, 9)) * cil[..., None], cil])
        s.cil_g = brillo(s.cil, 14, (1.0, 0.4, 0.08))
        cal = cv2.resize(m_glifo("☠", 300), None, fx=0.42, fy=0.42, interpolation=cv2.INTER_AREA)
        s.cal = np.dstack([calor(np.full(cal.shape, 0.93, np.float32)) * cal[..., None], cal])
        cg = m_glifo("☠", 520)
        s.calG = Lamina(np.dstack([cg] * 3), cg.shape[1], 6, alfa=cg, gamma=0.5)
        hg = m_higado(250)
        sh = 0.42 + 0.25 * ruido(250, 250, 50, 31) + 0.2 * cv2.GaussianBlur(hg, (0, 0), 18)
        s.hig = np.dstack([calor(np.clip(sh, 0, 1)) * hg[..., None], hg])
        s.hig_v = np.dstack([calor(np.clip(sh + 0.42, 0, 1)) * hg[..., None], hg])
        s.hig_g = brillo(s.hig, 16, (1.0, 0.35, 0.05))
        sol = forma(700, lambda d, T: d.ellipse([T * .03, T * .03, T * .97, T * .97], fill=255))
        s.sol = np.dstack([calor(0.36 + 0.14 * ruido(700, 700, 80, 41)) * sol[..., None], sol])
        s.sol_g = brillo(s.sol, 40, (0.9, 0.22, 0.04))

    # ---------------- capas ----------------
    def chispas(s, L, t, capa):
        for x0, v, ph, tam, vai, cp in s.ch:
            if (cp > 0.45) != capa:
                continue
            e = (t * (0.10 + 0.16 * v) + ph) % 1.0
            y = H - 150 - e * (900 + 900 * v)
            x = x0 * W + math.sin(e * 9 + ph * 20) * (30 + 70 * vai) + e * 60 * (vai - .5)
            b = (1 - e) ** 1.6 * (0.6 + 0.4 * math.sin(t * 23 + ph * 50))
            pegar(L, s.kch if tam > 0.5 else s.kch[3:-3, 3:-3], x, y, b * (0.9 if capa else 0.55), suma=True)

    def llamas(s, L, t):
        a = desplaza(s.f1, t * 37, t * 420)[:230] * 0.62 + desplaza(s.f2, -t * 23, t * 700)[:230] * 0.38
        x = np.clip((a * 1.25 - 0.30) * s.falt * 2.1 + s.falt ** 3 * (0.35 + 0.5 * a), 0, 0.93)
        f = cv2.resize(calor(x), (W, 460), interpolation=cv2.INTER_LINEAR)
        al = cv2.resize(np.clip(x * 2.4, 0, 1), (W, 460))[..., None]
        z = L[H - 460:]
        z *= 1 - al * 0.92
        z += f * al

    def barras(s, L, t):
        """Mil veces más potente que el cianuro: dos columnas de fuego."""
        op = ventana(t, 7.05, 9.6, 0.3, 0.3)
        if op <= 0:
            return 0.0
        p = suave(rampa(t, 7.62, 1.25))
        for cx, alto, etq, t0 in ((300, 70, "CIANURO", 7.1), (760, 70 + 640 * p ** 1.6, "FUGU", 7.3)):
            alto = int(alto * sale(rampa(t, t0, 0.3)))
            if alto < 4:
                continue
            x0, y0 = cx - 120, 900 - alto
            n = desplaza(s.f1, cx, t * 300)[:alto, :240]
            g = np.linspace(1, 0.25, alto, dtype=np.float32)[:, None]
            col = calor(np.clip(0.30 + 0.5 * g * (0.55 + 0.9 * n), 0, 1))
            m = np.ones((alto, 240), np.float32); m[:, :5] = m[:, -5:] = 0.4
            L[y0:900, x0:x0 + 240] = L[y0:900, x0:x0 + 240] * (1 - op * m[..., None]) + col * m[..., None] * op
            e = texto(etq, F_BAHN, 50, (1.0, 0.82, 0.55), esp=6)
            pegar(L, e, cx, 948, op)
        n = int(round(1000 ** p)) if p < 1 else 1000
        hot = max(golpe(t, 8.87, 0.9), 0.25 * (1 - p))
        c = texto(f"×{n}", F_IMPACT, 190, tuple(float(v) for v in calor(np.array([[0.70 + 0.28 * hot]], np.float32))[0, 0]), esp=4)
        g = brillo(c, 18, (1.0, 0.4, 0.08))
        k = 1 + 0.25 * golpe(t, 8.87, 0.3)
        pegar(L, transf(g, k), 540, 190, op * (0.5 + hot), suma=True); pegar(L, transf(c, k), 540, 190, op)
        return golpe(t, 8.87, 0.25)

    def cuadro(s, i):
        t = i / FPS
        par = 0.82 + 0.18 * math.sin(t * 11.3) * math.sin(t * 7.1 + 1) + 0.06 * math.sin(t * 31)
        L = s.fondo + s.resplandor * par
        hm = cv2.resize(desplaza(s.humo, t * 9, t * 55), (W, H), interpolation=cv2.INTER_LINEAR)[..., None]
        L = L + hm * np.array([0.085, 0.045, 0.03], np.float32) * (0.4 + s.resplandor[..., :1] * 2)
        s.chispas(L, t, False)
        sac = 0.0

        def lam(l, cx, cy, t0, t1, esc=1.0, rot=0.0, **kw):
            sp = l.sprite(t, t0, t1, **kw)
            if sp is not None:
                z = esc * (1 + 0.035 * (t - t0) / max(0.5, t1 - t0))
                pegar(L, transf(sp, z, rot), cx, cy)

        # --- 0-4,2 fugu, Japón, ruleta rusa ---
        if t < 2.6:
            k = rebote(rampa(t, 1.0, 0.4)) * (1 - rampa(t, 2.25, 0.3))
            if k > 0:
                pegar(L, transf(s.sol_g, k), 540, 470, 0.8 * par, suma=True); pegar(L, transf(s.sol, k), 540, 470, 0.92)
        lam(s.fugu, 540 + 14 * math.sin(t * 1.3), 480 + 10 * math.sin(t * 2.1), -0.15, 2.55, din=0.5)
        if 2.25 < t < 4.3:
            u = rampa(t, 2.3, 1.28)
            ang = -1500 * (1 - u) ** 3
            k = rebote(rampa(t, 2.25, 0.3)) * (1 - rampa(t, 4.0, 0.25))
            fl = golpe(t, 3.58, 0.5)
            pegar(L, transf(s.cil_g, k), 540, 500, 0.7 + fl, suma=True)
            pegar(L, transf(s.cil, k, ang), 540, 500)
            a = math.radians(270 + ang)
            pegar(L, transf(s.cal, k * (1 + 0.5 * fl)), 540 + 160 * k * math.cos(a), 500 + 160 * k * math.sin(a))
            sac += golpe(t, 3.58, 0.25)
        # --- 4,3-6,9 tetrodotoxina ---
        lam(s.ttx, 540, 560 + 12 * math.sin(t * 2), 4.45, 6.85, esc=1.0, rot=6 * math.sin(t * 1.1))
        # --- 6,9-9,6 ×1000 ---
        sac += s.barras(L, t)
        # --- 9,7-11,7 sin antídoto ---
        lam(s.calG, 540, 430, 9.75, 11.75, din=0.45)
        # --- 11,8-15 años 70 · kabuki ---
        lam(s.sharaku, 540 + 10 * math.sin(t), 490, 13.1, 15.0, rot=-2.0)
        # --- 15-16,4 Bandō ---
        lam(s.bando, 540, 505, 14.9, 16.4, din=0.4, dout=0.3)
        # --- 16,4-20,6 cuatro hígados ---
        lam(s.plato, 540, 400, 16.3, 20.9, din=0.5)
        ven = suave(rampa(t, 19.1, 0.7))
        for k, th in enumerate((17.68, 17.94, 18.2, 18.46)):
            e = rebote(rampa(t, th, 0.28))
            if e > 0:
                x, y = 180 + 240 * k, 800 + 8 * math.sin(t * 3 + k)
                pegar(L, transf(s.hig_g, e), x, y, 0.6 + 0.9 * ven + golpe(t, th, 0.3), suma=True)
                pegar(L, transf(s.hig, e, -8 + 5 * k), x, y)
                if ven > 0:
                    pegar(L, transf(s.hig_v, e, -8 + 5 * k), x, y, ven * (0.75 + 0.25 * math.sin(t * 14 + k)))
                sac += golpe(t, th, 0.18) * 0.6
        # --- él ---
        rgb, a, _ = persona(i, 540, 1085)
        ab = cv2.resize(cv2.GaussianBlur(cv2.resize(a, (W // 4, H // 4), interpolation=cv2.INTER_AREA), (0, 0), 9), (W, H))
        L += ((ab * (1 - a))[..., None] * np.array([0.95, 0.33, 0.06], np.float32)) * (0.75 * par)
        borde = np.clip(a - ab, 0, 1) * 2.2
        rgb = np.clip((rgb - 0.015) * 1.9, 0, 1) ** 0.78 * np.array([1.0, 0.95, 0.90], np.float32)
        rgb += borde[..., None] * np.array([1.0, 0.46, 0.10], np.float32) * (0.75 * par)
        a3 = a[..., None]
        L = L * (1 - a3) + rgb * a3
        s.llamas(L, t)
        s.chispas(L, t, True)
        # --- palabras al rojo vivo ---
        Y = 985
        for txt, tam, t0, t1 in (("JAPÓN", 150, 1.06, 2.35), ("RULETA RUSA", 150, 2.7, 4.05), ("TETRODOTOXINA", 122, 5.56, 6.8),
                                 ("NO EXISTE", 96, 10.2, 11.65), ("1975", 330, 12.06, 13.05), ("TEATRO KABUKI", 124, 14.04, 14.9),
                                 ("4 HÍGADOS", 150, 17.68, 19.0), ("LA PARTE MÁS VENENOSA", 96, 19.48, 21)):
            cy = 520 if txt == "1975" else 835 if txt == "NO EXISTE" else Y
            sac += marca(L, txt, tam, 540, cy, t, t0, t1)
        sac += marca(L, "ANTÍDOTO", 170, 540, 975, t, 10.88, 11.65)
        if 10.88 < t < 12.0:                                   # tachadura que arde sobre ANTÍDOTO
            u = sale(rampa(t, 11.0, 0.22)); op = 1 - rampa(t, 11.65, 0.35)
            x1 = int(170 + 740 * u)
            m = np.zeros((130, W), np.float32)
            cv2.line(m, (170, 100), (x1, 35), 1.0, 16, cv2.LINE_AA)
            m = (m * op)[..., None]
            L[915:1045] = L[915:1045] * (1 - m) + m * np.array([1.0, 0.86, 0.5], np.float32)
        marca(L, "KIOTO, JAPÓN", 70, 540, 760, t, 12.3, 13.05, fuente=F_BAHN, esp=10)
        sac += marca(L, "BANDŌ MITSUGORŌ", 118, 540, 955, t, 14.98, 16.35, fuente=F_BAHN, esp=3)
        marca(L, "TESORO NACIONAL VIVIENTE", 50, 540, 1050, t, 15.35, 16.35, fuente=F_BAHN, esp=8)
        L *= s.vin
        if sac > 0.02:
            L = np.roll(L, (int(math.sin(t * 90) * 13 * min(sac, 1.2)), int(math.cos(t * 70) * 9 * min(sac, 1.2))), (0, 1))
        L += (np.random.default_rng(i).random((H // 2, W // 2, 1), np.float32).repeat(2, 0).repeat(2, 1) - 0.5) * 0.035
        return L


if __name__ == "__main__":
    principal(Brasa, "brasa")
