# -*- coding: utf-8 -*-
"""Anuncio de Los Duos — vertical, plano secuencia con tiempo global (kit duos.py).
Cada bloque del guion es una función que dibuja el cuadro entero; en los cambios de bloque se mezclan los dos con un
empujón de zoom y un destello (los whooshes los pone sfx_duos.py en audio/fx.wav, anclados a los mismos tiempos).
    gancho   parejas bailando (video real) + BODA / XV AÑOS / CUMPLEAÑOS + «¡PONLE MÚSICA EN VIVO!»
    grupo    el logo nace dorado → tarjeta con el tecladista cantando + TECLADISTA / 2 VOCES → «nadie se queda sentado»
    generos  cortes de baile a cada género + píldoras de colores (como su póster)
    eventos  tres tarjetas con fiestas reales → «ponen el ambiente» con confeti
    zona     mapa con relieve real: Aguascalientes y sus municipios, unidos por líneas doradas
    pausas   tras grupo, géneros y eventos: 9-10 s de SOLO MÚSICA (canta el grupo) con video real, «EN VIVO» y ecualizador
    precio   escenario con haces de luz: «¿Y EL PRECIO?» → $1,200 que cae con destellos → POR HORA
    contacto WhatsApp: el número aparece cifra por cifra cuando el locutor lo dice
    cierre   logo grande, lema, número y zona; entran las voces del grupo"""
import math

from duos import (BLANCO, CREMA, ESC, FIN, GENEROS, H, INI, ORO, ORO_CLARO, TINTA, TOTAL, VERDE_WA, W, P, acabado, chispas,
                  cinta, clamp, clip_borroso, clip_lleno, confeti, destellos, e_back, e_out, emoji, escenario, geo_pant,
                  golpe, logo, mapa, ancho, ecualizador, nota, marca_agua, mix, notas, oscurecer, pildora, pin, polvo, pr, smooth, subrayado, tarjeta,
                  texto, texto_oro, velo, ww)
from escena_base import Escena

T = {k: ESC[k]["t0"] for k in ESC}
CORTES = [T[k] for k in ("grupo", "generos", "eventos", "zona", "precio", "contacto", "cierre")]
MEZCLA_S = 0.22


def aparece(t, t0, dur=0.32):
    return clamp((t - t0) / dur)


def rebote(t, t0, dur=0.42):
    u = clamp((t - t0) / dur)
    return e_back(u) if u < 1 else 1.0


# ------------------------------------------------------------------ gancho
def gancho(p, t):
    t0 = T["gancho"]
    u = (t - t0) / (T["grupo"] - t0)
    clip_lleno(p, "baile_globos", t - t0 + 0.3, z=1.14 - 0.10 * smooth(u), dy=-30 + 40 * u)
    velo(p, 820, 1920, 0.80)
    velo(p, 0, 420, 0.55, arriba=True)
    notas(p, t, 6, 0.8, semilla=31, y_min=200, y_max=1300)
    a_ti = ww("gancho", 0, "tienes")
    sale = aparece(t, ww("gancho", 0, "ponle") - 0.25, 0.3)
    texto(p, "¿TIENES...", W / 2, 900 - 40 * sale, 70, CREMA, "anton", aparece(t, a_ti, 0.25) * (1 - sale), esp=0.08)
    for j, (pal, txt) in enumerate((("boda", "BODA"), ("quince", "XV AÑOS"), ("cumplea", "CUMPLEAÑOS?"))):
        tw = ww("gancho", 0, pal)
        k = rebote(t, tw - 0.05)
        if k <= 0:
            continue
        y = 1040 + j * 165 - 120 * sale
        texto_oro(p, txt, W / 2, y, 150 if j < 2 else 140, "anton", (1 - sale), esp=0.03, brillo=clamp((t - tw) / 0.8),
                  contorno=0.07)
    # ¡PONLE MÚSICA EN VIVO!
    tp, tv = ww("gancho", 0, "ponle"), ww("gancho", 0, "en vivo")
    k1 = rebote(t, tp - 0.05)
    if k1 > 0:
        with p.pivote(W / 2, 1080, 0.6 + 0.4 * k1):
            texto(p, "¡PONLE MÚSICA", W / 2, 1040, 128, BLANCO, "anton", min(1, k1), esp=0.02)
    k2 = rebote(t, tv - 0.05, 0.5)
    if k2 > 0:
        with p.pivote(W / 2, 1240, 0.4 + 0.6 * k2):
            cinta(p, W / 2, 1240, 780, 190, min(1, k2), color=(0.80, 0.08, 0.10), inclina=-3)
            texto(p, "EN VIVO!", W / 2 + 40, 1234, 150, BLANCO, "anton", min(1, k2), esp=0.04, contorno=0.04)
            # punto rojo que late («grabando en vivo»)
            lat = 0.6 + 0.4 * math.sin(t * 9)
            p.glow(W / 2 - 250, 1234, 60, (1, 0.3, 0.3), 0.6 * lat)
            p.circ(W / 2 - 250, 1234, 24, BLANCO, min(1, k2) * (0.7 + 0.3 * lat))
        destellos(p, t, tv, W / 2, 1240, 16, 420)
    polvo(p, t, 20, 0.6)


# ------------------------------------------------------------------ grupo
def grupo(p, t):
    t0, t1 = T["grupo"], T["generos"]
    t_logo = ww("grupo", 0, "llegan") + 0.05
    t_tecla = ww("grupo", 0, "tecladista")
    t_voces = ww("grupo", 0, "dos voces")
    t_listos = ww("grupo", 0, "listos")
    t_nadie = ww("grupo", 0, "nadie")
    # fondo: escenario + el tecladista difuso
    escenario(p, t, fuerza=0.8)
    clip_borroso(p, "tecladista", t - t0 + 1.0, 0.42, op=0.8)
    oscurecer(p, 0.15)
    # el logo nace grande y sube a ser cabecera cuando entra la tarjeta
    sube = smooth(clamp((t - (t_tecla - 0.55)) / 0.55))
    crece_ = smooth(clamp((t - (t_listos + 0.55)) / 0.7))
    logo(p, W / 2, lerp_(880, 230, sube), lerp_(0.98, 0.62, sube), t, t_logo, 1.0 - clamp(crece_ * 3), lema=sube < 0.5,
         t_lema=t_logo + 0.6)
    destellos(p, t, t_logo + 0.2, W / 2, 880, 18, 480)
    # tarjeta con el tecladista; al «listos» se agranda y el contenido pasa a la pista de baile
    ent = rebote(t, t_tecla - 0.45, 0.5)
    if ent > 0:
        crece = smooth(clamp((t - (t_listos + 0.55)) / 0.7))
        cw, ch_ = lerp_(760, W + 40, crece), lerp_(1150, H + 40, crece)
        cy = lerp_(1010, H / 2, crece) + (1 - min(1, ent)) * 900
        ang = lerp_(-2.5, 0, crece) + (1 - min(1, ent)) * -8
        nombre, seg = ("tecladista", t - t_tecla + 3.2) if t < t_listos + 0.55 else ("baile_c", t - t_listos)
        marco = lerp_(14, 0, crece)
        tarjeta(p, nombre, seg, W / 2, cy, cw, ch_, ang, min(1, ent), marco=marco,
                enfoque=0.6 if nombre == "tecladista" else 0.5, enfoque_x=0.42 if nombre == "tecladista" else 0.5)
        if crece > 0:
            velo(p, 850, 1920, 0.78 * crece)
            velo(p, 0, 400, 0.5 * crece, arriba=True)
            marca_agua(p, t, clamp((crece - 0.5) * 2))
        # insignias
        sale = smooth(clamp((t - (t_listos + 0.35)) / 0.4))
        for j, (tw, txt, chs) in enumerate(((t_tecla, "TECLADISTA", "🎹"), (t_voces, "2 VOCES", "🎤"))):
            k = rebote(t, tw - 0.05)
            if k <= 0 or sale >= 1:
                continue
            x = W / 2 + (-40 if j == 0 else 40)
            y = 1420 + 140 * j - 300 * sale
            bw = 250
            with p.pivote(x, y, k):
                p.rrect(x - bw, y - 60, x + bw, y + 60, 60, TINTA, 0.88 * (1 - sale))
                p.rrect(x - bw, y - 60, x + bw, y + 60, 60, None, 1 - sale, borde=ORO, w=4)
                emoji(p, chs, x - bw + 70, y, 72, 1 - sale)
                if j == 1:
                    emoji(p, chs, x - bw + 115, y + 4, 64, 1 - sale)
                texto_oro(p, txt, x + 45, y + 2, 72, "anton", 1 - sale, esp=0.03, contorno=0.05, sombra=0.3)
        # «NADIE SE QUEDA SENTADO»
        kn = rebote(t, t_nadie - 0.05, 0.45)
        if kn > 0:
            texto(p, "¡NADIE SE QUEDA", W / 2, 1230, 112, BLANCO, "anton", min(1, kn), esp=0.02)
            texto_oro(p, "SENTADO!", W / 2, 1370, 170, "anton", min(1, kn), esp=0.04,
                      brillo=clamp((t - t_nadie - 0.2) / 0.9))
            confeti(p, t, t_nadie, 60, 2.6, semilla=17)
    notas(p, t, 5, 0.6, semilla=41)


def lerp_(a, b, u):
    return a + (b - a) * u


# ------------------------------------------------------------------ géneros
FONDOS_GEN = ["baile_a", "noche_a", "baile_b", "noche_b", "baile_globos", "tecladista", "baile_c", "manos"]


def generos(p, t):
    t0 = T["generos"]
    ts = [ww("generos", 0, w) for w in ("cumbias", "norte", "zapateado", "banda", "grupera", "baladas", "mariachi",
                                        "rock")]
    i = max([j for j, x in enumerate(ts) if t >= x - 0.12] or [0])
    seg = t - (ts[i] - 0.12 if i else t0) + 0.4
    z = 1.10 - 0.05 * clamp((t - (ts[i] - 0.12)) / 1.2)
    clip_lleno(p, FONDOS_GEN[i], seg + {"baile_globos": 2.5, "tecladista": 5.0}.get(FONDOS_GEN[i], 0.0), z=z)
    oscurecer(p, 0.42)
    velo(p, 0, 560, 0.6, arriba=True)
    # destello en cada corte
    p.im += 0.10 * golpe(t, ts[i] - 0.12, 0.25)
    marca_agua(p, t, aparece(t, t0, 0.3))
    k = rebote(t, t0 + 0.05, 0.5)
    texto(p, "MÚSICA", W / 2, 262, 92, BLANCO, "anton", min(1, k), esp=0.10)
    texto_oro(p, "VERSÁTIL", W / 2, 425, 150, "anton", min(1, k), esp=0.05, brillo=clamp((t - t0 - 0.3) / 1.0))
    for j, (txt, col, ch) in enumerate(GENEROS):
        kj = rebote(t, ts[j] - 0.06, 0.4)
        if kj <= 0:
            continue
        cx = 285 if j % 2 == 0 else 795
        cy = 640 + (j // 2) * 175
        if j == 7:                                    # ROCK: más grande y con sacudida
            kj *= 1.0 + 0.10 * golpe(t, ts[j] + 0.05, 0.4)
        pildora(p, cx, cy, txt, col, ch, kj, 1.0, w=470, t=t)
    km = rebote(t, ts[-1] + 0.55, 0.4)
    if km > 0:
        texto_oro(p, "¡Y MUCHO MÁS!", W / 2, 1420, 104, "anton", min(1, km), esp=0.03, brillo=clamp((t - ts[-1] - 0.7) / 0.9))
        chispas(p, t, W / 2, 1420, 700, 160, 8)
    notas(p, t, 6, 0.6, semilla=51, y_min=1450, y_max=H)


# ------------------------------------------------------------------ eventos
def eventos(p, t):
    t0 = T["eventos"]
    tf, tr, te = ww("eventos", 0, "fiestas"), ww("eventos", 0, "reuniones"), ww("eventos", 0, "eventos")
    ta = ww("eventos", 0, "ellos")
    final = smooth(clamp((t - (ta - 0.15)) / 0.55))
    escenario(p, t, fuerza=1.0)
    marca_agua(p, t, 1 - final)
    if final < 1:
        cards = [(tf, "manos", "FIESTAS", 390, 480, -4, 3.5, 0.55), (tr, "mesas", "REUNIONES FAMILIARES", 690, 930, 3, 0.0, 0.62),
                 (te, "salon", "EVENTOS PRIVADOS", 400, 1380, -3, 1.0, 0.5)]
        for j, (tw, nom, txt, cx, cy, ang, off, enf) in enumerate(cards):
            k = rebote(t, tw - 0.35, 0.5)
            if k <= 0:
                continue
            fuera = final * (1 if j % 2 == 0 else -1) * 1200
            x = cx + (1 - min(1, k)) * (-700 if j % 2 == 0 else 700) + fuera
            w_, h_ = 660, 380
            a_ = ang + (1 - min(1, k)) * 10
            tarjeta(p, nom, t - tw + off + 0.8, x, cy, w_, h_, a_, min(1, k), marco=12, enfoque=enf)
            # rótulo sobre el borde inferior de la tarjeta (sigue su giro)
            lx, ly = x - math.sin(math.radians(a_)) * (h_ / 2), cy + math.cos(math.radians(a_)) * (h_ / 2)
            lw = ancho(txt, 66) / 2 + 40
            cinta(p, lx, ly, 2 * lw, 96, min(1, k), color=TINTA, inclina=a_)
            texto_oro(p, txt, lx, ly - 2, 66, "anton", min(1, k), esp=0.03, brillo=clamp((t - tw) / 0.9), sombra=0.2)
    if final > 0:
        clip_lleno(p, "manos", t - ta + 3.6, z=1.18 - 0.10 * clamp((t - ta) / 3.0), op=final)
        velo(p, 850, 1920, 0.78 * final)
        kp = rebote(t, ww("eventos", 0, "ponen") - 0.1, 0.45)
        if kp > 0:
            texto(p, "ELLOS PONEN", W / 2, 1220, 110, BLANCO, "anton", min(1, kp) * final, esp=0.04)
            texto_oro(p, "EL AMBIENTE", W / 2, 1365, 160, "anton", min(1, kp) * final, esp=0.03,
                      brillo=clamp((t - ww("eventos", 0, "ambiente")) / 0.9))
        confeti(p, t, ta + 0.1, 80, 3.0, semilla=29)
    notas(p, t, 5, 0.5, semilla=61)


# ------------------------------------------------------------------ zona (mapa)
AGS = (-102.2916, 21.8818)
CENTRO_AGS = (-102.34, 22.06)
# municipios del estado (cabeceras); «i» = rótulo a la izquierda del punto
MUN_AGS = [("Jesús María", -102.343, 21.961, "i"), ("San José de Gracia", -102.416, 22.150, "i"),
           ("Calvillo", -102.718, 21.847, "d"), ("Rincón de Romos", -102.321, 22.229, "i"), ("Cosío", -102.300, 22.366, "i"),
           ("Pabellón de Arteaga", -102.276, 22.149, "d"), ("Tepezalá", -102.170, 22.224, "i"), ("Asientos", -102.089, 22.238, "d"),
           ("El Llano", -101.965, 21.919, "i"), ("San Fco. de los Romo", -102.270, 22.075, "d")]


def cam_zona(t):
    u = smooth(clamp((t - T["zona"]) / (T["precio"] - T["zona"])))
    return (lerp_(AGS[0], CENTRO_AGS[0], u), lerp_(AGS[1], CENTRO_AGS[1], u), lerp_(1.65, 1.35, u))


def zona(p, t):
    t0 = T["zona"]
    cam = cam_zona(t)
    mapa(p, *cam)
    velo(p, 0, 520, 0.7, arriba=True)
    velo(p, 1450, 1920, 0.6)
    polvo(p, t, 25, 0.6)
    marca_agua(p, t)
    k = rebote(t, t0 + 0.1, 0.5)
    texto(p, "TE LLEVAMOS LA FIESTA", W / 2, 300, 62, CREMA, "anton", min(1, k), esp=0.12)
    t_ags, t_mun = ww("zona", 0, "aguascalientes"), ww("zona", 0, "municipios")
    t_lle = ww("zona", 0, "llegan")
    ax, ay = geo_pant(*AGS, cam)
    # municipios: aparecen uno tras otro, unidos a la capital por una línea dorada
    for j, (nom, lo, la, lado) in enumerate(MUN_AGS):
        tj = t_mun - 0.25 + 0.09 * j
        v = rebote(t, tj, 0.35)
        if v <= 0:
            continue
        x, y = geo_pant(lo, la, cam)
        u = clamp((t - tj) / 0.4)
        p.linea((ax, ay), (lerp_(ax, x, u), lerp_(ay, y, u)), 3, ORO, 0.45)
        # «¡llegan hasta tu fiesta!»: una chispa viaja de la capital a cada municipio y deja una onda
        w_ = (t - t_lle - 0.05 * j) / 0.8
        if 0 < w_ < 1:
            p.glow(lerp_(ax, x, e_out(w_)), lerp_(ay, y, e_out(w_)), 40, ORO_CLARO, 0.9 * (1 - w_ * 0.5))
        if 0 < w_ - 0.6 < 0.8:
            q = (w_ - 0.6) / 0.8
            p.circ(x, y, 12 + 40 * q, ORO, 0.7 * (1 - q), w=3)
        p.circ(x, y, 13 * v, TINTA, 0.9)
        p.circ(x, y, 9 * v, ORO_CLARO, 1.0)
        izq = lado == "i"
        texto(p, nom, x + (-20 if izq else 20), y, 32, CREMA, "mont", min(1, v) * 0.95, "rm" if izq else "lm", sombra=0.9,
              contorno=0.08)
    pin(p, ax, ay, t, t_ags - 0.1, 1.0, 1.2)
    destellos(p, t, t_ags + 0.25, ax, ay - 80, 12, 220)
    ka = rebote(t, t_ags + 0.1, 0.4)
    if ka > 0:
        texto_oro(p, "AGUASCALIENTES", ax, ay + 72, 80, "anton", min(1, ka), esp=0.03)
    kz = rebote(t, t_lle - 0.05, 0.45)
    if kz > 0:
        texto(p, "¡LLEGAN HASTA", W / 2, 1390, 92, BLANCO, "anton", min(1, kz), esp=0.03)
        texto_oro(p, "TU FIESTA!", W / 2, 1510, 130, "anton", min(1, kz), esp=0.04, brillo=clamp((t - t_lle - 0.2) / 0.9))


# ------------------------------------------------------------------ precio
def precio(p, t):
    t0 = T["precio"]
    tq, tm, th = ww("precio", 0, "precio"), ww("precio", 0, "mil"), ww("precio", 0, "hora")
    ts = ww("precio", 0, "solo")
    escenario(p, t, fuerza=1.2)
    clip_borroso(p, "manos", t - t0 + 2.0, 0.30, op=0.5)
    marca_agua(p, t)
    # «¿Y EL PRECIO?»: tiembla un poco y se encoge cuando cae la cifra
    kq = rebote(t, tq - 0.25, 0.4)
    baja = smooth(clamp((t - (tm - 0.2)) / 0.35))
    if kq > 0:
        y = lerp_(900, 520, baja)
        s = lerp_(1.0, 0.62, baja)
        with p.pivote(W / 2, y, s * min(1, kq)):
            texto(p, "¿Y EL PRECIO?", W / 2 + math.sin(t * 30) * 4 * (1 - baja), y, 130, BLANCO, "anton", 1.0, esp=0.03)
    ks = rebote(t, ts - 0.05, 0.35)
    if ks > 0:
        texto(p, "A SOLO", W / 2, 700, 84, ORO_CLARO, "anton", min(1, ks) * (0.4 + 0.6 * baja), esp=0.15)
    # $1,200
    u = clamp((t - (tm - 0.08)) / 0.32)
    if u > 0:
        s = lerp_(2.6, 1.0, e_out(u)) * (1 + 0.04 * math.sin(t * 5) * clamp(t - tm - 0.5))
        p.glow(W / 2, 960, 620, ORO, 0.22 * u)
        with p.pivote(W / 2, 960, s):
            texto_oro(p, "$1,200", W / 2, 960, 330, "anton", min(1, u * 1.5), esp=0.01, brillo=clamp((t - tm - 0.3) / 1.0),
                      contorno=0.05)
        texto(p, "PESOS MEXICANOS", W / 2, 1165, 40, CREMA, "mont", u, esp=0.2)
        destellos(p, t, tm + 0.15, W / 2, 960, 22, 560)
        chispas(p, t, W / 2, 960, 900, 420, 10, fuerza=clamp(t - tm - 0.6))
    kh = rebote(t, th - 0.35, 0.45)
    if kh > 0:
        with p.pivote(W / 2, 1330, 0.5 + 0.5 * kh):
            cinta(p, W / 2, 1330, 720, 170, min(1, kh), inclina=-3)
            texto(p, "POR HORA", W / 2, 1326, 128, TINTA, "anton", min(1, kh), esp=0.06, sombra=0.0, contorno=0.0)
    notas(p, t, 6, 0.7, semilla=71, y_min=1450, y_max=H)


# ------------------------------------------------------------------ contacto
DIGITOS = "449 306 5431"


def contacto(p, t):
    t0 = INI("contacto")
    # tiempos medidos de la voz (Whisper con marcas por palabra sobre voz/final/contacto_0.wav)
    ti = [t0 + x for x in (2.52, 2.98, 3.38, 4.18, 4.42, 4.82, 5.60, 5.60, 6.64, 6.64)]
    clip_borroso(p, "baile_b", t - T["contacto"] + 1.0, 0.40)
    polvo(p, t, 30, 0.8)
    notas(p, t, 5, 0.5, semilla=81)
    marca_agua(p, t)
    ta = ww("contacto", 0, "aparta")
    k = rebote(t, ta - 0.05, 0.45)
    if k > 0:
        emoji(p, "📅", W / 2 - 330, 420, 110, min(1, k), ang=-8)
        texto(p, "APARTA", W / 2 + 60, 360, 100, BLANCO, "anton", min(1, k), esp=0.06)
        texto_oro(p, "TU FECHA", W / 2 + 60, 485, 130, "anton", min(1, k), esp=0.04, brillo=clamp((t - ta) / 0.9))
    # icono de WhatsApp
    tw = ww("contacto", 0, "whatsapp")
    kw = rebote(t, tw - 0.25, 0.5)
    if kw > 0:
        cx, cy = W / 2, 820
        lat = 1 + 0.04 * math.sin(t * 6)
        with p.pivote(cx, cy, kw * lat):
            p.glow(cx, cy, 300, VERDE_WA, 0.35)
            p.circ(cx + 8, cy + 14, 132, (0, 0, 0), 0.45)
            p.circ(cx, cy, 132, VERDE_WA, 1.0)
            p.circ(cx, cy, 84, BLANCO, 1.0, w=13)
            p.poly([(cx - 70, cy + 50), (cx - 92, cy + 100), (cx - 38, cy + 80)], BLANCO, 1.0)
            emoji(p, "📞", cx, cy, 80, 1.0, ang=-10)
        texto(p, "WhatsApp", W / 2, 1010, 70, BLANCO, "mont", min(1, kw), esp=0.02)
    # el número, cifra por cifra
    if t >= ti[0] - 0.1:
        tot_w = 0
        anchos = []
        for ch in DIGITOS:
            a = 38 if ch == " " else 72
            anchos.append(a)
            tot_w += a
        x = W / 2 - tot_w / 2
        idx = 0
        p.rrect(W / 2 - tot_w / 2 - 55, 1110, W / 2 + tot_w / 2 + 55, 1290, 40, TINTA, 0.75 * aparece(t, ti[0] - 0.1, 0.25))
        p.rrect(W / 2 - tot_w / 2 - 55, 1110, W / 2 + tot_w / 2 + 55, 1290, 40, None, aparece(t, ti[0] - 0.1, 0.25),
                borde=ORO, w=4)
        for ch, a in zip(DIGITOS, anchos):
            if ch != " ":
                tc = ti[idx]
                kd = rebote(t, tc - 0.06, 0.3)
                if kd > 0:
                    with p.pivote(x + a / 2, 1200, kd):
                        recien = golpe(t, tc, 0.5)
                        texto_oro(p, ch, x + a / 2, 1200, 140, "anton", 1.0, contorno=0.05)
                        if recien > 0.05:
                            p.glow(x + a / 2, 1200, 90, ORO_CLARO, 0.5 * recien)
                idx += 1
            x += a
    tc_ = ti[6] + 0.1
    kc = rebote(t, tc_, 0.45)
    if kc > 0:
        lat = 1 + 0.05 * max(0.0, math.sin((t - tc_) * 7))
        with p.pivote(W / 2, 1470, kc * lat):
            p.rrect(W / 2 - 330 + 8, 1395 + 14, W / 2 + 330 + 8, 1545 + 14, 75, (0, 0, 0), 0.4)
            p.rrect(W / 2 - 330, 1395, W / 2 + 330, 1545, 75, VERDE_WA, 1.0)
            p.rrect(W / 2 - 330, 1395, W / 2 + 330, 1470, 75, BLANCO, 0.12)
            texto(p, "¡CONTÁCTANOS!", W / 2, 1468, 92, BLANCO, "anton", 1.0, esp=0.04, sombra=0.3, contorno=0.03)
        # Facebook
        kf = aparece(t, tc_ + 0.3, 0.4)
        p.rrect(W / 2 - 300, 1600, W / 2 - 230, 1670, 16, (0.09, 0.47, 0.95), kf)
        texto(p, "f", W / 2 - 265, 1640, 64, BLANCO, "anton", kf, sombra=0.0, contorno=0.0)
        texto(p, "Grupo Los Duos", W / 2 - 205, 1635, 56, BLANCO, "mont", kf, "lm", sombra=0.6)
        chispas(p, t, W / 2, 1470, 760, 220, 8, fuerza=kc)


# ------------------------------------------------------------------ cierre
def cierre(p, t):
    t0 = T["cierre"]
    tl = ww("cierre", 0, "los duos") - 0.1
    escenario(p, t, fuerza=1.1)
    clip_borroso(p, "tecladista", t - t0 + 4.0, 0.30, op=0.55)
    logo(p, W / 2, 760, 1.0, t, tl, 1.0, lema=False)
    destellos(p, t, tl + 0.3, W / 2, 760, 22, 560)
    chispas(p, t, W / 2, 760, 900, 420, 10, fuerza=clamp(t - tl - 0.8))
    # lema palabra por palabra
    pals = [("Música", "musica"), ("que", "que"), ("alegra", "alegra"), ("tus", "tus"), ("momentos", "momentos")]
    xs, x = [], 0
    for txt, _ in pals:
        xs.append(x)
        x += ancho(txt, 50, "monti") + 16
    x0 = W / 2 - (x - 16) / 2
    for (txt, clave), dx in zip(pals, xs):
        tw = ww("cierre", 0, clave)
        k = rebote(t, tw - 0.05, 0.35)
        if k > 0:
            texto(p, txt, x0 + dx, 1010 + (1 - min(1, k)) * 30, 50, CREMA, "monti", min(1, k), "lm", sombra=0.7)
    # tira de datos
    kd = rebote(t, FIN("cierre") + 0.1, 0.5)
    if kd > 0:
        a = min(1, kd)
        with p.pivote(W / 2, 1390, kd):
            p.rrect(W / 2 - 420, 1250, W / 2 + 420, 1530, 46, TINTA, 0.80 * a)
            p.rrect(W / 2 - 420, 1250, W / 2 + 420, 1530, 46, None, a, borde=ORO, w=4)
            p.circ(W / 2 - 300, 1335, 50, VERDE_WA, a)
            emoji(p, "📞", W / 2 - 300, 1335, 52, a, ang=-10)
            texto_oro(p, "449 306 5431", W / 2 + 40, 1335, 100, "anton", a, esp=0.03, contorno=0.05)
            texto(p, "$1,200 POR HORA", W / 2, 1455, 62, BLANCO, "anton", a, esp=0.06)
        texto(p, "AGUASCALIENTES Y SUS MUNICIPIOS", W / 2, 1590, 44, CREMA, "mont", aparece(t, FIN("cierre") + 0.4, 0.4),
              esp=0.08)
    ecualizador(p, W / 2, 1180, 600, 90, t, aparece(t, FIN("cierre") + 0.2, 0.5), smooth(clamp((t - FIN("cierre") - 0.2) / 0.6)))
    notas(p, t, 10, 0.9, semilla=91)
    confeti(p, t, FIN("cierre") + 0.05, 70, 3.5, semilla=37, fuerza=0.9)
    confeti(p, t, FIN("cierre") + 3.0, 50, 3.5, semilla=43, fuerza=0.8)


# ------------------------------------------------------------------ pausas de solo música (el grupo canta)
PAUSAS = {   # escena tras la que va la pausa: rótulo y cortes [(s desde el inicio de la pausa, clip, segundo del clip)]
    "grupo": ("ASÍ SUENAN EN VIVO", [(0.0, "tecladista", 2.0), (4.3, "teclado", 0.6), (6.4, "tecladista", 6.4)]),
    "generos": ("¡A BAILAR!", [(0.0, "baile_globos", 0.0), (2.1, "noche_a", 0.5), (4.2, "baile_a", 0.5), (6.3, "noche_b", 0.3),
                               (8.4, "baile_b", 1.0)]),
    "eventos": ("¡PURO AMBIENTE!", [(0.0, "manos", 3.2), (2.6, "salon", 1.5), (5.0, "baile_c", 0.8), (7.4, "noche_b", 2.5)]),
}
T_PAUSA = {k: FIN(k) + 0.35 for k in PAUSAS}


def pausa(p, t, esc):
    tp = T_PAUSA[esc]
    rot, cortes = PAUSAS[esc]
    s = t - tp
    j = max([i for i, c in enumerate(cortes) if s >= c[0] - 1e-6] or [0])
    c0, nom, seg0 = cortes[j]
    clip_lleno(p, nom, seg0 + max(0.0, s - c0), z=1.12 - 0.07 * clamp((s - c0) / 2.5))
    if j:
        p.im += 0.12 * golpe(s, c0, 0.22)
    velo(p, 900, 1920, 0.80)
    velo(p, 0, 330, 0.5, arriba=True)
    marca_agua(p, t)
    notas(p, t, 8, 0.9, semilla=101, y_min=300, y_max=1150)
    k = rebote(t, tp + 0.15, 0.45)
    if k > 0:
        a = min(1, k)
        lat = 0.6 + 0.4 * math.sin(t * 8)                  # «● EN VIVO»
        p.rrect(W / 2 - 120, 1205, W / 2 + 120, 1265, 30, (0.80, 0.08, 0.10), 0.95 * a)
        p.circ(W / 2 - 80, 1235, 12, BLANCO, a * (0.6 + 0.4 * lat))
        texto(p, "EN VIVO", W / 2 + 18, 1236, 44, BLANCO, "anton", a, esp=0.10, sombra=0.0, contorno=0.0)
        with p.pivote(W / 2, 1335, 0.6 + 0.4 * k):
            texto_oro(p, rot, W / 2, 1335, 92, "anton", a, esp=0.03, brillo=clamp((t - tp - 0.3) / 1.0))
            mw = ancho(rot, 92, esp=0.03) / 2 + 60
            for sg in (-1, 1):
                nota(p, W / 2 + sg * mw, 1330 + math.sin(t * 4 + sg) * 6, 80, a, doble=sg > 0)
    ecualizador(p, W / 2, 1535, 820, 150, t, 1.0, smooth(clamp((t - tp) / 0.5)))


BLOQUES = [("gancho", gancho), ("grupo", grupo), ("generos", generos), ("eventos", eventos), ("zona", zona),
           ("precio", precio), ("contacto", contacto), ("cierre", cierre)]


def _bloque(t):
    i = 0
    for j, (k, _) in enumerate(BLOQUES):
        if t >= T[k]:
            i = j
    return i


def _lienzo(f, t, *a):
    p = P()
    f(p, t, *a)
    return p.im


def pintar(i, t):
    k, fn = BLOQUES[i]
    tp = T_PAUSA.get(k)
    if tp is None or t < tp:
        return _lienzo(fn, t)
    u = smooth(clamp((t - tp) / 0.35))
    b = _lienzo(pausa, t, k)
    return b if u >= 1 else _lienzo(fn, t) * (1 - u) + b * u


def cuadro(t):
    i = _bloque(t)
    tc = T[BLOQUES[i][0]]
    flash, sac = 0.0, 0.0
    if i > 0 and t - tc < MEZCLA_S:                           # entra el bloque nuevo con empujón de zoom
        u = smooth((t - tc) / MEZCLA_S)
        nuevo = pintar(i, t)
        viejo = pintar(i - 1, t)
        img = viejo * (1 - u) + nuevo * u
        flash = 0.22 * (1 - abs(u - 0.5) * 2)
    elif i < len(BLOQUES) - 1 and T[BLOQUES[i + 1][0]] - t < 0.12:
        img = pintar(i, t)
        flash = 0.10 * (1 - (T[BLOQUES[i + 1][0]] - t) / 0.12)
    else:
        img = pintar(i, t)
    # golpes con sacudida: el logo, «EN VIVO», el precio
    for tg, f in ((ww("gancho", 0, "en vivo"), 0.5), (ww("grupo", 0, "los duos") + 0.15, 0.35),
                  (ww("precio", 0, "mil") + 0.12, 0.9), (ww("cierre", 0, "los duos") + 0.15, 0.35)):
        g = golpe(t, tg, 0.35)
        sac += f * g
        flash += 0.12 * f * golpe(t, tg, 0.2)
    for tp in T_PAUSA.values():
        flash += 0.10 * golpe(t, tp + 0.1, 0.3)
    img = acabado(img, t, flash=flash, sacudida=sac)
    img *= smooth(pr(t, 0.0, 0.25))
    img *= 1.0 - smooth(pr(t, TOTAL - 0.6, TOTAL))
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


from escena_base import TL  # noqa: E402

CLASES = {e["id"]: Mundo for e in TL["escenas"]}
