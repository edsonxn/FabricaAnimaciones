# -*- coding: utf-8 -*-
"""Personas y animales diminutos del mundo isométrico (estilo Kurzgesagt): carteles en pantalla con 3/4 de frente o de espalda, caminata con balanceo y rebote,
gestos (saludar, trabajar, cargar, rezar, pelear, vitorear) y multitudes con desfase aleatorio. Todo original; tipos de la época (México 1808-1821).

Tamaño: `h` = altura en unidades de mundo (a zoom 1 = px). Una persona normal mide ~34. Con menos de ~26 px en pantalla se dibuja una versión mínima (LOD).
"""
import math

import numpy as np

from motor import circulo, elipse, rect_red, h01, catmull
import plano as P
from kz_iso import tint, sombra_elipse, C30, S30

PIELES = [(246, 204, 164), (230, 176, 128), (200, 140, 98), (168, 112, 80), (132, 86, 62)]
PELOS = [(44, 32, 40), (58, 40, 38), (30, 24, 34), (92, 62, 44), (210, 206, 214)]
ROPAS = [(236, 232, 220), (232, 92, 82), (70, 160, 200), (244, 190, 70), (110, 170, 110), (170, 110, 190), (240, 140, 60), (60, 120, 170)]
PALMA = (236, 198, 120)
BLANCO = (246, 242, 232)

# tipos de la época: torso, pantalón, sombrero, extras
TIPOS = {
    "campesino": dict(torso=(246, 240, 226), pierna=(240, 236, 224), sombrero="palma", faja=(214, 70, 70)),
    "campesina": dict(torso=(232, 120, 120), pierna=(120, 70, 100), sombrero=None, rebozo=(70, 120, 180), falda=True),
    "indigena": dict(torso=(250, 244, 228), pierna=(250, 244, 228), sombrero="palma", faja=(60, 150, 160)),
    "indigena_f": dict(torso=(250, 244, 228), pierna=(214, 90, 120), sombrero=None, rebozo=(240, 180, 70), falda=True),
    "insurgente": dict(torso=(246, 242, 232), pierna=(240, 236, 224), sombrero="palma", faja=(204, 52, 52), arma="machete"),
    "insurgente_lanza": dict(torso=(246, 242, 232), pierna=(240, 236, 224), sombrero="palma", faja=(204, 52, 52), arma="lanza"),
    "honda": dict(torso=(246, 242, 232), pierna=(240, 236, 224), sombrero="palma", faja=(204, 52, 52), arma="honda"),
    "minero": dict(torso=(176, 138, 100), pierna=(110, 90, 80), sombrero="casco", faja=(92, 64, 56), arma="pico"),
    "realista": dict(torso=(246, 244, 240), pierna=(54, 78, 140), sombrero="shako", cruz=True, arma="mosquete"),
    "dragon": dict(torso=(206, 56, 64), pierna=(246, 244, 240), sombrero="bicornio", cruz=True, arma="sable"),
    "oficial": dict(torso=(52, 86, 160), pierna=(246, 244, 240), sombrero="bicornio", cruz=True, arma="sable", charreteras=True),
    "virrey": dict(torso=(150, 44, 66), pierna=(246, 244, 240), sombrero="peluca", charreteras=True),
    "cura": dict(torso=(46, 42, 62), pierna=(46, 42, 62), sombrero=None, falda=True, cuello=BLANCO, pelo_blanco=True),
    "noble": dict(torso=(52, 46, 66), pierna=(70, 60, 80), sombrero="copa", cuello=BLANCO),
    "dama": dict(torso=(220, 110, 150), pierna=(220, 110, 150), sombrero="peinado", falda=True),
    "comerciante": dict(torso=(90, 150, 120), pierna=(120, 100, 90), sombrero="palma", delantal=(240, 232, 214)),
    "arriero": dict(torso=(200, 160, 110), pierna=(236, 230, 214), sombrero="palma", faja=(60, 110, 140), sarape=(222, 100, 70)),
    "nino": dict(torso=(246, 240, 226), pierna=(240, 236, 224), sombrero=None),
    "esclavo": dict(torso=(226, 212, 186), pierna=(196, 176, 146), sombrero=None, faja=(140, 100, 70)),
    "mestizo": dict(torso=(204, 154, 112), pierna=(96, 76, 70), sombrero="palma", faja=(60, 110, 140)),
    "peninsular": dict(torso=(170, 50, 72), pierna=(246, 244, 240), sombrero="peluca", charreteras=True),
    "regidor": dict(torso=(70, 52, 96), pierna=(60, 52, 72), sombrero="copa", cuello=BLANCO),
    "granadero": dict(torso=(40, 66, 140), pierna=(246, 244, 240), sombrero="gorro_piel", cruz=True, arma="mosquete", charreteras=True),
    "yermo": dict(torso=(60, 52, 70), pierna=(150, 120, 90), sombrero="copa", cuello=BLANCO, arma="sable"),
    "pijama": dict(torso=(236, 232, 246), pierna=(236, 232, 246), sombrero="gorro_noche", faja=(180, 160, 220)),
    "escribano": dict(torso=(70, 56, 90), pierna=(60, 50, 70), sombrero=None, cuello=BLANCO),
    "monarca": dict(torso=(150, 44, 66), pierna=(246, 244, 240), sombrero="corona", charreteras=True),
    "napoleon": dict(torso=(112, 118, 126), pierna=(246, 244, 240), sombrero="bicornio_lado", cuello=(250, 250, 248), faja=(250, 206, 90)),
}


def _px(iso, x, y, z=0.0):
    sx, sy = iso.P(x, y, z)
    return float(sx), float(sy)


def persona(lz, iso, x, y, t=0.0, tipo="campesino", dir=(1.0, 0.0), vel=0.0, seed=0, piel=None, h=34.0, accion=None, z=0.0, tp=0.0, rop=None, sombra=True, alfa=1.0, carga=None, cara=None):
    """Persona de h unidades de mundo en (x, y). dir = hacia dónde mira/camina (mundo); vel = ritmo de la caminata (0 = parada). accion: None|'saluda'|'vitorea'|'trabaja'|'reza'|'pelea'|'habla'|'carga'|'cae'.
    tp = tiempo propio (desfase por persona se suma con seed)."""
    k = iso.z
    hp = h * k
    if hp < 4.0:
        return
    sx, sy = _px(iso, x, y, z)
    if sx < -80 or sx > 2000 or sy < -80 or sy > 1180:
        return
    d = np.array(dir, float)
    pdx, pdy = (d[0] - d[1]) * C30, (d[0] + d[1]) * S30            # dirección proyectada
    lado = 1 if pdx >= 0 else -1
    frente = pdy >= -0.02                                             # mira hacia abajo de la pantalla = de frente
    spec = TIPOS[tipo]
    pc = piel if piel is not None else PIELES[int(h01(seed, 1) * len(PIELES)) % len(PIELES)]
    pelo = (210, 206, 214) if spec.get("pelo_blanco") else PELOS[int(h01(seed, 2) * len(PELOS) * 0.8) % (len(PELOS) - 1)]
    u = hp / 34.0
    ph = (t + tp) * vel * 7.0 + h01(seed, 3) * 6.28
    sw = math.sin(ph) if vel > 0 else 0.0
    bob = abs(math.sin(ph)) * 1.4 * u if vel > 0 else 0.45 * u * math.sin((t + tp) * 2.0 + h01(seed, 4) * 6.28)
    tor = rop if rop is not None else spec["torso"]
    pie = spec["pierna"]
    if sombra:
        sombra_elipse(lz, iso, x + 1.5, y + 0.6, 5.2 * h / 34, 3.0 * h / 34, 0.22 * alfa)
    lod = hp < 30
    A = alfa
    # --- piernas / falda
    by = sy - bob
    if spec.get("falda"):
        lz.relleno(np.array([[sx - 4.6 * u, by - 14 * u], [sx + 4.6 * u, by - 14 * u], [sx + (6.2 + 1.2 * sw) * u * lado * 0 + 6.4 * u, by - 1.5 * u], [sx - 6.4 * u, by - 1.5 * u]]), tint(pie), alfa=A)
        lz.relleno(np.array([[sx - 4.6 * u, by - 14 * u], [sx, by - 14 * u], [sx - 1.0 * u, by - 1.5 * u], [sx - 6.4 * u, by - 1.5 * u]]), tint(P.aclarar(pie, 0.12)), alfa=A)
        lz.relleno(rect_red(sx - 3.2 * u, by - 2.0 * u, 2.2 * u, 2.4 * u, 0.6 * u), tint((60, 40, 50)), alfa=A)
        lz.relleno(rect_red(sx + 1.0 * u, by - 2.0 * u, 2.2 * u, 2.4 * u, 0.6 * u), tint((60, 40, 50)), alfa=A)
    else:
        for s_, col in ((-1, P.oscurecer(pie, 0.24)), (1, pie)):
            ox = s_ * 2.0 * u + (sw * s_ * 4.0 * u * lado if vel > 0 else 0)
            lz.relleno(np.array([[sx + s_ * 1.0 * u - 1.9 * u, by - 14 * u], [sx + s_ * 1.0 * u + 1.9 * u, by - 14 * u], [sx + ox + 2.0 * u, by - 1.0 * u], [sx + ox - 2.0 * u, by - 1.0 * u]]), tint(col), alfa=A)
            lz.relleno(rect_red(sx + ox - 2.8 * u + (1.0 * u * lado), by - 2.0 * u + (1.0 * u * 0 if vel == 0 else -abs(sw) * 0.0), 5.2 * u, 2.6 * u, 1.0 * u), tint((56, 44, 50)), alfa=A)
    # --- brazos (detrás) y torso
    bz = by - 14 * u
    if not lod:
        ang_b = 0.35 * sw * lado
        _brazo(lz, sx - 5.2 * u, bz - 11 * u, 10 * u, -0.25 - ang_b, tor, pc, u, A, oscuro=True)
    th = 12.4 * u
    lz.relleno(rect_red(sx - 5.0 * u, bz - th, 10.0 * u, th + 0.6 * u, 2.4 * u), tint(tor), alfa=A)
    lz.relleno(rect_red(sx + 0.8 * u, bz - th, 4.2 * u, th + 0.6 * u, 2.0 * u), tint(P.oscurecer(tor, 0.20)), alfa=A)
    if spec.get("faja") and not lod:
        lz.relleno(rect_red(sx - 5.0 * u, bz - 3.6 * u, 10 * u, 2.4 * u, 0.6 * u), tint(spec["faja"]), alfa=A)
    if spec.get("cruz") and not lod:
        lz.relleno(np.array([[sx - 4.8 * u, bz - th + 1 * u], [sx - 3.2 * u, bz - th + 1 * u], [sx + 4.8 * u, bz - 1.0 * u], [sx + 3.2 * u, bz - 1.0 * u]]), tint((252, 250, 244)), alfa=A)
        lz.relleno(np.array([[sx + 4.8 * u, bz - th + 1 * u], [sx + 3.2 * u, bz - th + 1 * u], [sx - 4.8 * u, bz - 1.0 * u], [sx - 3.2 * u, bz - 1.0 * u]]), tint((252, 250, 244)), alfa=A)
    if spec.get("delantal") and not lod:
        lz.relleno(rect_red(sx - 3.6 * u, bz - 8 * u, 7.2 * u, 8.5 * u, 1.2 * u), tint(spec["delantal"]), alfa=A)
    if spec.get("sarape") and not lod:
        lz.relleno(np.array([[sx - 5.4 * u, bz - th + 0.5 * u], [sx + 5.4 * u, bz - th + 0.5 * u], [sx + 6.2 * u, bz - 4 * u], [sx - 6.2 * u, bz - 4 * u]]), tint(spec["sarape"]), alfa=A)
        for i in range(3):
            lz.relleno(rect_red(sx - 6.0 * u, bz - (5 + i * 2.6) * u, 12 * u, 1.0 * u, 0.3 * u), tint((250, 220, 120)), alfa=A)
    if spec.get("cuello") and not lod:
        lz.relleno(np.array([[sx - 2.4 * u, bz - th], [sx + 2.4 * u, bz - th], [sx, bz - th + 3.0 * u]]), tint(spec["cuello"]), alfa=A)
    if spec.get("rebozo"):
        lz.relleno(np.array([[sx - 5.6 * u, bz - th + 0.5 * u], [sx + 5.6 * u, bz - th + 0.5 * u], [sx + 4.6 * u, bz - 4.5 * u], [sx - 4.6 * u, bz - 4.5 * u]]), tint(spec["rebozo"]), alfa=A)
        lz.relleno(np.array([[sx - 5.6 * u, bz - th + 0.5 * u], [sx - 0.5 * u, bz - th + 0.5 * u], [sx - 0.5 * u, bz - 4.5 * u], [sx - 4.6 * u, bz - 4.5 * u]]), tint(P.aclarar(spec["rebozo"], 0.18)), alfa=A)
    if spec.get("charreteras") and not lod:
        for s_ in (-1, 1):
            lz.relleno(rect_red(sx + s_ * 5.0 * u - 2.4 * u, bz - th - 0.6 * u, 4.8 * u, 2.2 * u, 0.8 * u), tint((250, 206, 90)), alfa=A)
    # --- brazo delantero y arma
    ang_f = -0.35 * sw * lado
    mano = _brazo_accion(lz, sx, bz, u, tor, pc, A, accion, ang_f, t + tp, seed, lado, lod)
    _arma(lz, spec.get("arma"), mano, u, lado, A, t + tp, seed, accion, vel)
    if carga is not None and not lod:
        carga(lz, sx, bz, u)
    # --- cabeza
    hy = bz - th - 5.0 * u
    lz.relleno(rect_red(sx - 1.6 * u, bz - th - 2.0 * u, 3.2 * u, 3.0 * u, 0.8 * u), tint(P.oscurecer(pc, 0.12)), alfa=A)
    if not lod:
        for s_ in (-1, 1):
            lz.relleno(circulo(sx + s_ * 4.6 * u, bz - th + 1.4 * u, 2.5 * u, 8), tint(P.oscurecer(tor, 0.20) if s_ > 0 else tor), alfa=A)
    lz.relleno(circulo(sx + 0.4 * u * lado, hy, 5.3 * u, 16), tint(pc), alfa=A)
    lz.relleno(np.array([[sx - 3.5 * u, hy + 3 * u], [sx + 4.5 * u, hy + 2.5 * u], [sx + 4.2 * u, hy + 4.8 * u], [sx - 3.0 * u, hy + 4.8 * u]]), tint(P.oscurecer(pc, 0.10)), alfa=A * 0.0)
    if not frente:
        lz.relleno(circulo(sx + 0.4 * u * lado, hy - 0.4 * u, 5.5 * u, 16), tint(pelo), alfa=A)
    else:
        lz.relleno(np.array([[sx - 5.0 * u + 0.4 * u * lado, hy - 1.2 * u], [sx + 0.4 * u * lado, hy - 6.2 * u], [sx + 5.4 * u + 0.4 * u * lado, hy - 1.2 * u], [sx + 3.6 * u + 0.4 * u * lado, hy - 3.0 * u],
                             [sx + 0.4 * u * lado, hy - 4.0 * u], [sx - 3.4 * u + 0.4 * u * lado, hy - 3.0 * u]]), tint(pelo), alfa=A)
        if not lod:
            _rasgos(lz, sx + 0.4 * u * lado, hy, u, A, lado, hp, accion, cara, t + tp, seed, pc)
    _sombrero(lz, spec.get("sombrero"), sx + 0.4 * u * lado, hy, u, A, lado, pelo, spec, frente)


def _rasgos(lz, hx, hy, u, A, lado, hp, accion, cara, t, seed, pc):
    """Cara según el tamaño en pantalla: lejos, dos puntos; media, ojos y boca; cerca, ojos con esclerótica, cejas, nariz y boca expresiva."""
    emo = cara or ("alegre" if accion in ("vitorea", "saluda") else "habla" if accion == "habla" else "normal")
    oscuro = (40, 26, 36)
    cierre = 1.0 - 0.9 * (1.0 if ((t + seed * 1.7) % 3.6) > 3.45 else 0.0)          # parpadeo
    big = hp > 105
    mid = hp > 62
    for sg in (-1, 1):
        ex = hx + sg * 1.95 * u + 0.5 * u * lado
        ey = hy + 0.2 * u
        if big:
            lz.relleno(elipse(ex, ey, 1.15 * u, 1.18 * u * cierre, 0, 10), tint((252, 250, 246)), alfa=A)
            lz.relleno(circulo(ex + 0.3 * u * lado, ey + 0.1 * u, 0.62 * u, 8), tint(oscuro), alfa=A)
            ang = {"enojo": 0.45, "miedo": -0.35, "triste": -0.4, "alegre": -0.1}.get(emo, 0.0) * sg * -1
            lz.relleno(np.array([[ex - 1.5 * u, ey - 2.0 * u + ang * 1.5 * u], [ex + 1.5 * u, ey - 2.0 * u - ang * 1.5 * u], [ex + 1.5 * u, ey - 1.4 * u - ang * 1.5 * u], [ex - 1.5 * u, ey - 1.4 * u + ang * 1.5 * u]]), tint(P.oscurecer(pc, 0.55)), alfa=A)
        else:
            lz.relleno(circulo(ex, ey, 0.75 * u, 6), tint(oscuro), alfa=A)
    if big:        # nariz
        lz.relleno(np.array([[hx + 0.6 * u * lado, hy + 0.7 * u], [hx + 1.5 * u * lado, hy + 2.0 * u], [hx - 0.1 * u * lado, hy + 2.1 * u]]), tint(P.oscurecer(pc, 0.18)), alfa=A)
    my = hy + 3.1 * u
    if mid:
        if emo == "habla":
            ap = 0.5 + 0.9 * abs(math.sin(t * 10 + seed))
            lz.relleno(elipse(hx + 0.4 * u * lado, my, 1.5 * u, ap * u, 0, 10), tint((110, 36, 56)), alfa=A)
        elif emo == "alegre":
            lz.relleno(np.array([[hx - 1.9 * u, my - 0.6 * u], [hx + 2.7 * u, my - 0.6 * u], [hx + 0.4 * u, my + 1.7 * u]]), tint((120, 40, 60)), alfa=A)
        elif emo == "enojo":
            lz.relleno(np.array([[hx - 1.5 * u, my + 0.8 * u], [hx + 0.4 * u, my - 0.2 * u], [hx + 2.3 * u, my + 0.8 * u], [hx + 0.4 * u, my + 0.3 * u]]), tint((96, 40, 54)), alfa=A)
        elif emo == "miedo":
            lz.relleno(elipse(hx + 0.4 * u * lado, my + 0.3 * u, 1.0 * u, 1.2 * u, 0, 8), tint((110, 36, 56)), alfa=A)
        elif emo == "triste":
            lz.relleno(np.array([[hx - 1.5 * u, my + 1.0 * u], [hx + 0.4 * u, my - 0.2 * u], [hx + 2.3 * u, my + 1.0 * u], [hx + 0.4 * u, my + 0.4 * u]]), tint((96, 40, 54)), alfa=A)
        else:
            lz.relleno(rect_red(hx - 1.2 * u + 0.4 * u * lado, my, 3.2 * u, 0.55 * u, 0.2 * u), tint((120, 60, 66)), alfa=A)


def _brazo(lz, x0, y0, L, ang, torso, piel, u, A, oscuro=False):
    x1, y1 = x0 + math.sin(ang) * L, y0 + math.cos(ang) * L
    col = P.oscurecer(torso, 0.28) if oscuro else torso
    n = np.array([math.cos(ang), -math.sin(ang)]) * 1.9 * u
    lz.relleno(np.array([[x0 - n[0], y0 - n[1]], [x0 + n[0], y0 + n[1]], [x1 + n[0] * 0.8, y1 + n[1] * 0.8], [x1 - n[0] * 0.8, y1 - n[1] * 0.8]]), tint(col), alfa=A)
    lz.relleno(circulo(x1, y1 + 0.6 * u, 1.9 * u, 8), tint(piel), alfa=A)
    return x1, y1


def _brazo_accion(lz, sx, bz, u, tor, pc, A, accion, ang_f, t, seed, lado, lod):
    sh_x, sh_y = sx + 5.2 * u, bz - 11 * u
    if lod:
        return (sx + 6 * u, bz - 5 * u)
    if accion in ("vitorea", "saluda"):
        ang = math.pi - 0.45 + 0.5 * math.sin(t * 6.5 + seed) if accion == "vitorea" else math.pi - 0.2 + 0.35 * math.sin(t * 8.0 + seed)
        return _brazo(lz, sh_x, sh_y, 11 * u, ang, tor, pc, u, A)
    if accion == "pelea":
        ang = 2.4 + 0.9 * math.sin(t * 7.0 + seed)
        return _brazo(lz, sh_x, sh_y, 11 * u, ang * lado * 0 + ang, tor, pc, u, A)
    if accion == "trabaja":
        ang = 1.2 + 0.9 * math.sin(t * 5.0 + seed)
        return _brazo(lz, sh_x, sh_y, 11 * u, ang, tor, pc, u, A)
    if accion == "reza":
        return _brazo(lz, sh_x - 2 * u, sh_y, 8 * u, 0.5 * lado, tor, pc, u, A)
    if accion == "chaleco":
        return _brazo(lz, sh_x - 1 * u, sh_y, 7 * u, 2.5 * lado * 0 + 2.6, tor, pc, u, A)
    if accion == "habla":
        ang = 0.9 + 0.6 * math.sin(t * 3.2 + seed)
        return _brazo(lz, sh_x, sh_y, 11 * u, ang, tor, pc, u, A)
    if accion == "carga":
        return _brazo(lz, sh_x, sh_y, 9 * u, 0.9, tor, pc, u, A)
    return _brazo(lz, sh_x, sh_y, 11 * u, 0.25 + ang_f, tor, pc, u, A)


def _arma(lz, arma, mano, u, lado, A, t, seed, accion, vel):
    if arma is None:
        return
    mx, my = mano
    if arma == "machete":
        a = -0.9 + 0.5 * math.sin(t * 6 + seed) if accion == "pelea" else -0.5
        _tira(lz, (mx, my), a, 12 * u, 1.8 * u, (220, 228, 240), A)
    elif arma == "mosquete":
        _tira(lz, (mx, my + 18 * u), 3.14, 22 * u, 1.9 * u, (110, 78, 56), A)
        _tira(lz, (mx, my - 3 * u), 3.14, 24 * u, 1.0 * u, (214, 220, 232), A)
        lz.relleno(rect_red(mx - 1.6 * u, my - 6 * u, 3.2 * u, 2.4 * u, 0.5 * u), tint((140, 100, 70)), alfa=A)
    elif arma == "lanza":
        _tira(lz, (mx, my + 8 * u), 0.05, 44 * u, 1.3 * u, (140, 100, 70), A)
        lz.relleno(np.array([[mx - 1.6 * u, my - 34 * u], [mx, my - 42 * u], [mx + 1.6 * u, my - 34 * u]]), tint((226, 232, 244)), alfa=A)
    elif arma == "sable":
        a = -0.8 + 0.6 * math.sin(t * 6 + seed) if accion == "pelea" else -0.4
        _tira(lz, (mx, my), a, 16 * u, 1.4 * u, (226, 232, 244), A)
    elif arma == "pico":
        a = 2.4 + 0.9 * math.sin(t * 5 + seed) if accion == "trabaja" else 2.6
        _tira(lz, (mx, my), a, 12 * u, 1.4 * u, (140, 100, 70), A)
        _tira(lz, (mx + math.sin(a) * 12 * u, my + math.cos(a) * 12 * u), a + 1.57, 6 * u, 1.4 * u, (170, 170, 190), A)
    elif arma == "honda":
        r = 8 * u
        a = t * 14 + seed
        lz.relleno(circulo(mx + math.cos(a) * r, my - 12 * u + math.sin(a) * r * 0.5, 1.1 * u, 6), tint((150, 140, 130)), alfa=A)


def _tira(lz, p0, ang, L, w, color, A):
    x0, y0 = p0
    x1, y1 = x0 + math.sin(ang) * L, y0 + math.cos(ang) * L
    n = np.array([math.cos(ang), -math.sin(ang)]) * w / 2
    lz.relleno(np.array([[x0 - n[0], y0 - n[1]], [x0 + n[0], y0 + n[1]], [x1 + n[0], y1 + n[1]], [x1 - n[0], y1 - n[1]]]), tint(color), alfa=A)


def _sombrero(lz, tipo, hx, hy, u, A, lado, pelo, spec, frente):
    if tipo is None:
        if spec.get("rebozo"):
            lz.relleno(np.array([[hx - 5.2 * u, hy + 2 * u], [hx - 4.4 * u, hy - 4.8 * u], [hx, hy - 6.2 * u], [hx + 4.4 * u, hy - 4.8 * u], [hx + 5.2 * u, hy + 2 * u], [hx + 3.4 * u, hy - 1.4 * u],
                                 [hx, hy - 2.6 * u], [hx - 3.4 * u, hy - 1.4 * u]]), tint(spec["rebozo"]), alfa=A)
        return
    if tipo == "palma":
        lz.relleno(elipse(hx, hy - 3.6 * u, 9.6 * u, 2.6 * u, 0, 16), tint(P.oscurecer(PALMA, 0.12)), alfa=A)
        lz.relleno(np.array([[hx - 4.4 * u, hy - 3.8 * u], [hx - 3.6 * u, hy - 8.6 * u], [hx + 3.6 * u, hy - 8.6 * u], [hx + 4.4 * u, hy - 3.8 * u]]), tint(PALMA), alfa=A)
        lz.relleno(rect_red(hx - 4.4 * u, hy - 5.4 * u, 8.8 * u, 1.3 * u, 0.4 * u), tint((190, 66, 56)), alfa=A)
    elif tipo == "casco":
        lz.relleno(np.array([[hx - 5 * u, hy - 2.4 * u], [hx - 4.2 * u, hy - 7 * u], [hx + 4.2 * u, hy - 7 * u], [hx + 5 * u, hy - 2.4 * u]]), tint((240, 196, 70)), alfa=A)
        lz.relleno(circulo(hx + 2.6 * u * lado, hy - 5.4 * u, 1.3 * u, 6), tint((255, 250, 200)), alfa=A)
    elif tipo == "shako":
        lz.relleno(rect_red(hx - 3.9 * u, hy - 12 * u, 7.8 * u, 9.6 * u, 0.8 * u), tint((46, 56, 112)), alfa=A)
        lz.relleno(rect_red(hx - 3.9 * u, hy - 3.8 * u, 7.8 * u, 1.6 * u, 0.4 * u), tint((30, 30, 50)), alfa=A)
        lz.relleno(circulo(hx, hy - 8.0 * u, 1.3 * u, 6), tint((250, 206, 90)), alfa=A)
        lz.relleno(np.array([[hx - 0.8 * u, hy - 12 * u], [hx, hy - 15.5 * u], [hx + 0.8 * u, hy - 12 * u]]), tint((214, 52, 56)), alfa=A)
    elif tipo in ("bicornio", "bicornio_lado"):
        lz.relleno(np.array([[hx - 8 * u, hy - 3.4 * u], [hx - 5 * u, hy - 8.6 * u], [hx + 5 * u, hy - 8.6 * u], [hx + 8 * u, hy - 3.4 * u], [hx + 3 * u, hy - 5 * u], [hx - 3 * u, hy - 5 * u]]), tint((40, 36, 56)), alfa=A)
        lz.relleno(np.array([[hx - 8 * u, hy - 3.4 * u], [hx - 3 * u, hy - 5 * u], [hx + 3 * u, hy - 5 * u], [hx + 8 * u, hy - 3.4 * u], [hx + 6 * u, hy - 3.8 * u], [hx - 6 * u, hy - 3.8 * u]]), tint((250, 206, 90)), alfa=A)
    elif tipo == "peluca":
        lz.relleno(np.array([[hx - 5.4 * u, hy + 3 * u], [hx - 5 * u, hy - 5 * u], [hx, hy - 7 * u], [hx + 5 * u, hy - 5 * u], [hx + 5.4 * u, hy + 3 * u], [hx + 3.4 * u, hy - 1 * u], [hx - 3.4 * u, hy - 1 * u]]), tint((246, 244, 250)), alfa=A)
    elif tipo == "copa":
        lz.relleno(rect_red(hx - 3.6 * u, hy - 12 * u, 7.2 * u, 9.6 * u, 0.6 * u), tint((38, 34, 52)), alfa=A)
        lz.relleno(elipse(hx, hy - 3.4 * u, 7 * u, 1.9 * u, 0, 14), tint((38, 34, 52)), alfa=A)
    elif tipo == "peinado":
        lz.relleno(circulo(hx, hy - 6.2 * u, 3.0 * u, 10), tint((58, 40, 44)), alfa=A)
        lz.relleno(np.array([[hx - 4.6 * u, hy - 1 * u], [hx - 4.2 * u, hy - 5 * u], [hx, hy - 6 * u], [hx + 4.2 * u, hy - 5 * u], [hx + 4.6 * u, hy - 1 * u]]), tint((58, 40, 44)), alfa=A)
    elif tipo == "gorro_piel":
        lz.relleno(np.array([[hx - 5.4 * u, hy - 2 * u], [hx - 5.0 * u, hy - 12 * u], [hx - 2 * u, hy - 15 * u], [hx + 2 * u, hy - 15 * u], [hx + 5.0 * u, hy - 12 * u], [hx + 5.4 * u, hy - 2 * u]]), tint((36, 30, 40)), alfa=A)
        lz.relleno(np.array([[hx - 4 * u, hy - 4 * u], [hx - 3.4 * u, hy - 11 * u], [hx - 1 * u, hy - 13 * u], [hx - 1 * u, hy - 4 * u]]), tint((70, 60, 74)), alfa=A)
        lz.relleno(circulo(hx, hy - 8 * u, 1.4 * u, 6), tint((250, 206, 90)), alfa=A)
    elif tipo == "gorro_noche":
        lz.relleno(np.array([[hx - 5.2 * u, hy - 2.4 * u], [hx - 4.0 * u, hy - 8 * u], [hx + 1 * u, hy - 11 * u], [hx + 8 * u * lado, hy - 8 * u], [hx + 5.2 * u, hy - 2.4 * u]]), tint((240, 236, 250)), alfa=A)
        lz.relleno(circulo(hx + 8.4 * u * lado, hy - 7.6 * u, 1.8 * u, 8), tint((200, 180, 230)), alfa=A)
    elif tipo == "corona":
        lz.relleno(np.array([[hx - 3.4 * u, hy - 4 * u], [hx - 3.4 * u, hy - 8 * u], [hx - 1.6 * u, hy - 6 * u], [hx, hy - 9 * u], [hx + 1.6 * u, hy - 6 * u], [hx + 3.4 * u, hy - 8 * u], [hx + 3.4 * u, hy - 4 * u]]), tint((250, 208, 80)), alfa=A)


# ------------------------------------------------------------------------------------------------ animales
def oveja(lz, iso, x, y, t=0.0, dir=1, seed=0, s=1.0):
    sx, sy = _px(iso, x, y)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 1, y + 0.5, 6 * s, 3.4 * s, 0.2)
    bob = 0.5 * math.sin(t * 2 + seed)
    lz.relleno(rect_red(sx - 4 * k, sy - 3 * k, 1.4 * k, 3 * k, 0.5 * k), tint((70, 60, 70)))
    lz.relleno(rect_red(sx + 2 * k, sy - 3 * k, 1.4 * k, 3 * k, 0.5 * k), tint((70, 60, 70)))
    for (dx, dy, r, c) in ((-3, -7, 4.6, (232, 230, 240)), (2, -7.4, 4.6, (232, 230, 240)), (-0.5, -9, 4.2, (250, 250, 255)), (3.4, -5.4, 3.2, (214, 212, 226))):
        lz.relleno(circulo(sx + dx * k, sy + (dy + bob * 0.2) * k, r * k, 10), tint(c))
    hd = 5.2 * dir
    lz.relleno(elipse(sx + hd * k, sy - 6.2 * k, 2.2 * k, 2.8 * k, 0.2 * dir, 10), tint((86, 74, 84)))


def gallina(lz, iso, x, y, t=0.0, dir=1, seed=0, color=(178, 74, 138)):
    sx, sy = _px(iso, x, y)
    k = iso.z
    pico = 0.8 * math.sin(t * 9 + seed * 3)
    lz.relleno(elipse(sx, sy - 3.4 * k, 3.2 * k, 2.6 * k, 0, 10), tint(color))
    lz.relleno(circulo(sx + 2.6 * dir * k, sy - (5.4 + max(0, pico)) * k, 1.4 * k, 6), tint(P.aclarar(color, 0.12)))
    lz.relleno(np.array([[sx + 3.6 * dir * k, sy - 5.4 * k], [sx + 5.0 * dir * k, sy - 5.0 * k], [sx + 3.6 * dir * k, sy - 4.6 * k]]), tint((250, 190, 70)))
    lz.relleno(rect_red(sx - 0.6 * k, sy - 1.6 * k, 0.7 * k, 1.6 * k, 0.2 * k), tint((250, 190, 70)))


def cerdo(lz, iso, x, y, t=0.0, dir=1, seed=0):
    sx, sy = _px(iso, x, y)
    k = iso.z
    sombra_elipse(lz, iso, x + 1, y + 0.6, 7, 3.6, 0.2)
    lz.relleno(elipse(sx, sy - 5.2 * k, 6.6 * k, 4.4 * k, 0, 14), tint((246, 160, 170)))
    lz.relleno(elipse(sx - 1.2 * k, sy - 6.4 * k, 4.6 * k, 2.6 * k, 0, 12), tint((252, 190, 196)))
    lz.relleno(circulo(sx + 6.2 * dir * k, sy - 5.6 * k, 3.0 * k, 10), tint((246, 160, 170)))
    lz.relleno(elipse(sx + 8.8 * dir * k, sy - 5.2 * k, 1.4 * k, 1.2 * k, 0, 8), tint((226, 120, 140)))


def burro(lz, iso, x, y, t=0.0, dir=1, seed=0, carga=True, s=1.0, color=(150, 140, 134)):
    sx, sy = _px(iso, x, y)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 2, y + 1, 11 * s, 5 * s, 0.2)
    ph = t * 5 + seed
    for (dx, f) in ((-7, 0.0), (-3, math.pi), (4, math.pi), (8, 0.0)):
        lz.relleno(rect_red(sx + dx * k - 1.1 * k + math.sin(ph + f) * 1.4 * k, sy - 8 * k, 2.2 * k, 8 * k, 0.6 * k), tint(P.oscurecer(color, 0.25)))
    lz.relleno(elipse(sx, sy - 11 * k, 10 * k, 5.4 * k, 0, 16), tint(color))
    lz.relleno(elipse(sx - 1 * k, sy - 12.4 * k, 8 * k, 3 * k, 0, 14), tint(P.aclarar(color, 0.14)))
    lz.relleno(np.array([[sx + 7 * dir * k, sy - 13 * k], [sx + 12 * dir * k, sy - 19 * k], [sx + 15 * dir * k, sy - 17 * k], [sx + 11 * dir * k, sy - 9 * k]]), tint(color))
    lz.relleno(elipse(sx + 14 * dir * k, sy - 15.4 * k, 3.4 * k, 2.4 * k, 0.4 * dir, 10), tint(P.aclarar(color, 0.2)))
    lz.relleno(np.array([[sx + 11.6 * dir * k, sy - 18 * k], [sx + 12.4 * dir * k, sy - 23 * k], [sx + 14 * dir * k, sy - 18.4 * k]]), tint(color))
    if carga:
        lz.relleno(rect_red(sx - 7 * k, sy - 19 * k, 13 * k, 8 * k, 1.6 * k), tint((214, 100, 74)))
        lz.relleno(rect_red(sx - 7 * k, sy - 19 * k, 5 * k, 8 * k, 1.6 * k), tint((236, 150, 100)))
        lz.relleno(rect_red(sx - 5 * k, sy - 22 * k, 9 * k, 3.4 * k, 1.2 * k), tint((246, 220, 130)))


def caballo(lz, iso, x, y, t=0.0, dir=1, seed=0, color=(150, 98, 68), vel=0.0, jinete=None, s=1.0):
    """Caballo en 3/4 (pequeño). jinete = tipo de persona montada o None."""
    sx, sy = _px(iso, x, y)
    k = iso.z * s
    sombra_elipse(lz, iso, x + 3, y + 1, 14 * s, 6 * s, 0.22)
    ph = t * vel * 9 + seed
    osc = abs(math.sin(ph)) * 2.0 * k if vel > 0 else 0.0
    sy -= osc
    for (dx, f, c) in ((-9, 0.0, P.oscurecer(color, 0.28)), (6, math.pi, P.oscurecer(color, 0.28)), (-6, math.pi, color), (10, 0.0, color)):
        sw = math.sin(ph + f) * 3.2 * k if vel > 0 else 0
        lz.relleno(np.array([[sx + (dx - 1.4) * k, sy - 9 * k], [sx + (dx + 1.4) * k, sy - 9 * k], [sx + dx * k + sw + 1.0 * k, sy], [sx + dx * k + sw - 1.0 * k, sy]]), tint(c))
    lz.relleno(elipse(sx, sy - 14 * k, 13 * k, 6.4 * k, 0, 18), tint(color))
    lz.relleno(elipse(sx - 1.4 * k, sy - 15.6 * k, 10 * k, 3.4 * k, 0, 14), tint(P.aclarar(color, 0.14)))
    ncx, ncy = sx + 11 * dir * k, sy - 19 * k
    lz.relleno(np.array([[sx + 8 * dir * k, sy - 16 * k], [ncx + 4 * dir * k, ncy - 7 * k], [ncx + 8 * dir * k, ncy - 4 * k], [sx + 12 * dir * k, sy - 12 * k]]), tint(color))
    lz.relleno(elipse(ncx + 8 * dir * k, ncy - 3.4 * k, 4.4 * k, 2.6 * k, 0.5 * dir, 10), tint(P.aclarar(color, 0.16)))
    lz.relleno(np.array([[ncx + 3 * dir * k, ncy - 7 * k], [ncx + 3.4 * dir * k, ncy - 12 * k], [ncx + 6 * dir * k, ncy - 7 * k]]), tint(color))
    lz.relleno(np.array([[sx + 6.6 * dir * k, sy - 19 * k], [sx + 10 * dir * k, sy - 25 * k], [sx + 12 * dir * k, sy - 19 * k], [sx + 9 * dir * k, sy - 14 * k]]), tint((60, 42, 44)))
    lz.relleno(np.array([[sx - 12 * dir * k, sy - 15 * k], [sx - 17 * dir * k, sy - 10 * k + math.sin(ph) * 2 * k], [sx - 14 * dir * k, sy - 6 * k], [sx - 11 * dir * k, sy - 11 * k]]), tint((60, 42, 44)))
    lz.relleno(rect_red(sx - 6 * k, sy - 21 * k, 11 * k, 3.6 * k, 1.2 * k), tint((196, 70, 70)))
    if jinete:
        persona(lz, iso, x, y, t, jinete, dir=(dir, 0), h=34, z=10 * s, sombra=False, seed=seed + 5, accion=None)


# ------------------------------------------------------------------------------------------------ multitudes
class Multitud:
    """Agentes que siguen trayectos (o rondan un punto) con fases propias. Todo es función de t (cada cuadro es independiente).
    agregar(...) crea un agente; dibujar(mundo, t) los registra en el Mundo como objetos dinámicos."""

    def __init__(self):
        self.ag = []

    def camina(self, trayecto, tipo="campesino", vel=18.0, fase=0.0, seed=0, h=34.0, bucle=True, accion=None, t0=0.0, t1=None, **kw):
        """Agente que recorre una polilínea del suelo a `vel` unidades/s (rebota o repite)."""
        p = np.asarray(trayecto, float)
        d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]
        self.ag.append(dict(modo="camina", p=p, d=d, tipo=tipo, vel=vel, fase=fase, seed=seed, h=h, bucle=bucle, accion=accion, t0=t0, t1=t1, kw=kw))

    def ronda(self, centro, radio, tipo="campesino", n=1, vel=6.0, seed=0, h=34.0, accion=None, **kw):
        """n agentes que deambulan cerca de un punto."""
        for i in range(n):
            self.ag.append(dict(modo="ronda", c=np.asarray(centro, float), r=radio, tipo=tipo, vel=vel, seed=seed + i * 17, h=h, accion=accion, kw=kw))

    def quieto(self, pos, tipo="campesino", dir=(1.0, 0.0), seed=0, h=34.0, accion=None, **kw):
        self.ag.append(dict(modo="quieto", pos=np.asarray(pos, float), tipo=tipo, dir=dir, seed=seed, h=h, accion=accion, kw=kw))

    def estado(self, a, t):
        if a["modo"] == "camina":
            if t < a["t0"] or (a["t1"] is not None and t > a["t1"]):
                return None
            L = a["d"][-1]
            s = (t - a["t0"]) * a["vel"] + a["fase"] * L
            if a["bucle"] == "ida_vuelta":
                m = s % (2 * L)
                s = m if m <= L else 2 * L - m
                sentido = 1 if m <= L else -1
            else:
                s = s % L if a["bucle"] else min(s, L)
                sentido = 1
            i = int(np.clip(np.searchsorted(a["d"], s, side="right") - 1, 0, len(a["p"]) - 2))
            seg = a["p"][i + 1] - a["p"][i]
            f = (s - a["d"][i]) / max(a["d"][i + 1] - a["d"][i], 1e-6)
            pos = a["p"][i] + seg * f
            dr = seg / max(np.hypot(*seg), 1e-6) * sentido
            return pos, dr, a["vel"] / 18.0
        if a["modo"] == "ronda":
            s = a["seed"]
            tt = t * a["vel"] * 0.02 + h01(s, 1) * 50
            ang = tt * (0.6 + h01(s, 2)) + h01(s, 3) * 6.28
            pos = a["c"] + a["r"] * np.array([math.cos(ang) * (0.4 + 0.6 * h01(s, 4)), math.sin(ang * 0.8 + 1.0) * (0.4 + 0.6 * h01(s, 5))])
            v = a["c"] * 0 + a["r"] * np.array([-math.sin(ang), math.cos(ang * 0.8 + 1.0) * 0.8])
            dr = v / max(np.hypot(*v), 1e-6)
            return pos, dr, 0.6
        return a["pos"], np.array(a["dir"], float), 0.0

    def dibujar(self, mundo, t, iso=None):
        for a in self.ag:
            e = self.estado(a, t)
            if e is None:
                continue
            pos, dr, v = e
            kw = dict(a["kw"])
            mundo.add(pos[0] - 4, pos[1] - 4, pos[0] + 4, pos[1] + 4, a["h"], (lambda pos, dr, v, a, kw: (lambda lz, iso: persona(lz, iso, pos[0], pos[1], t, a["tipo"], dir=tuple(dr), vel=v, seed=a["seed"], h=a["h"], accion=a["accion"], **kw)))(pos, dr, v, a, kw),
                      fijo=False, clave=pos[0] + pos[1])


# ================================================================================ Juchipila (4-oct-2026): tipos, tocados y armas del siglo XVI y de la Revolución
TIPOS.update({
    "caxcan": dict(torso=(214, 84, 70), pierna=(172, 120, 84), sombrero="plumas", faja=(250, 200, 84), arma="arco"),
    "caxcan_lanza": dict(torso=(214, 84, 70), pierna=(172, 120, 84), sombrero="plumas", faja=(250, 200, 84), arma="lanza"),
    "caxcan_mazo": dict(torso=(72, 150, 190), pierna=(172, 120, 84), sombrero="plumas", faja=(250, 200, 84), arma="macuahuitl"),
    "caxcan_jefe": dict(torso=(72, 150, 190), pierna=(172, 120, 84), sombrero="plumas_grande", faja=(250, 200, 84), arma="macuahuitl"),
    "caxcana": dict(torso=(238, 234, 216), pierna=(222, 70, 120), sombrero="cinta", falda=True, faja=(250, 200, 84)),
    "caxcan_sacerdote": dict(torso=(120, 70, 190), pierna=(80, 200, 190), sombrero="plumas_grande", faja=(250, 200, 84)),
    "caxcan_anciano": dict(torso=(190, 150, 110), pierna=(190, 150, 110), sombrero="cinta", falda=True, pelo_blanco=True),
    "conquistador": dict(torso=(168, 178, 204), pierna=(150, 60, 64), sombrero="morrion", arma="sable", cruz=False),
    "conquistador_lanza": dict(torso=(168, 178, 204), pierna=(150, 60, 64), sombrero="morrion", arma="lanza"),
    "capitan_esp": dict(torso=(196, 196, 220), pierna=(150, 40, 56), sombrero="morrion_plumas", arma="sable", charreteras=True),
    "fraile": dict(torso=(150, 118, 96), pierna=(150, 118, 96), sombrero="capucha", falda=True, faja=(240, 232, 214)),
    "aliado": dict(torso=(244, 238, 222), pierna=(244, 238, 222), sombrero="plumas", faja=(214, 70, 70), arma="macuahuitl"),
    "revolucionario": dict(torso=(240, 232, 208), pierna=(240, 232, 208), sombrero="palma", faja=(150, 90, 60), arma="mosquete"),
    "tastoan": dict(torso=(214, 84, 70), pierna=(250, 244, 230), sombrero="mascara", faja=(250, 200, 84)),
})

_sombrero_base = _sombrero
_arma_base = _arma


def _sombrero(lz, tipo, hx, hy, u, A, lado, pelo, spec, frente):
    if tipo in ("plumas", "plumas_grande"):
        g = 1.45 if tipo == "plumas_grande" else 1.0
        lz.relleno(rect_red(hx - 5.2 * u, hy - 4.4 * u, 10.4 * u, 1.6 * u, 0.5 * u), tint((250, 200, 84)), alfa=A)
        cols = ((222, 70, 120), (250, 200, 84), (80, 200, 190), (120, 90, 220), (222, 70, 120))
        for k in range(5):
            ang = -0.8 + 0.4 * k
            ox, oy = math.sin(ang) * 8.0 * u * g, -math.cos(ang) * 8.5 * u * g
            bx = hx + (k - 2) * 2.0 * u
            lz.relleno(np.array([[bx - 1.2 * u, hy - 4.2 * u], [bx + ox * 0.5 - 2.0 * u, hy - 4.2 * u + oy * 0.5], [bx + ox, hy - 4.2 * u + oy], [bx + ox * 0.5 + 2.0 * u, hy - 4.2 * u + oy * 0.5], [bx + 1.2 * u, hy - 4.2 * u]]), tint(cols[k]), alfa=A)
    elif tipo == "cinta":
        lz.relleno(np.array([[hx - 5.2 * u, hy - 1.8 * u], [hx - 4.4 * u, hy - 5.2 * u], [hx, hy - 6.2 * u], [hx + 4.4 * u, hy - 5.2 * u], [hx + 5.2 * u, hy - 1.8 * u], [hx, hy - 3.4 * u]]), tint((40, 28, 44)), alfa=A)
        lz.relleno(rect_red(hx - 5.0 * u, hy - 4.6 * u, 10.0 * u, 1.3 * u, 0.4 * u), tint((222, 70, 120)), alfa=A)
    elif tipo in ("morrion", "morrion_plumas"):
        lz.relleno(np.array([[hx - 5.2 * u, hy - 2.6 * u], [hx - 4.4 * u, hy - 7.6 * u], [hx, hy - 9.2 * u], [hx + 4.4 * u, hy - 7.6 * u], [hx + 5.2 * u, hy - 2.6 * u]]), tint((176, 186, 214)), alfa=A)
        lz.relleno(rect_red(hx - 0.6 * u, hy - 9.4 * u, 1.2 * u, 7.0 * u, 0.3 * u), tint((214, 220, 238)), alfa=A)
        lz.relleno(elipse(hx, hy - 2.8 * u, 8.4 * u, 1.5 * u, 0, 14), tint((150, 160, 190)), alfa=A)
        if tipo == "morrion_plumas":
            for k in range(3):
                lz.relleno(np.array([[hx - 0.6 * u, hy - 9 * u], [hx + (2 + 2.4 * k) * u, hy - (13 + k) * u], [hx + (4 + 2.4 * k) * u, hy - (10 + k) * u]]), tint((214, 56, 66) if k % 2 == 0 else (250, 244, 230)), alfa=A)
    elif tipo == "capucha":
        lz.relleno(np.array([[hx - 5.4 * u, hy + 2.5 * u], [hx - 5.0 * u, hy - 5.0 * u], [hx, hy - 7.0 * u], [hx + 5.0 * u, hy - 5.0 * u], [hx + 5.4 * u, hy + 2.5 * u], [hx + 3.6 * u, hy - 1.0 * u], [hx, hy - 2.2 * u], [hx - 3.6 * u, hy - 1.0 * u]]), tint((120, 92, 72)), alfa=A)
    elif tipo == "mascara":
        lz.relleno(circulo(hx, hy, 6.0 * u, 14), tint((232, 190, 120)), alfa=A)
        for s_ in (-1, 1):
            lz.relleno(circulo(hx + s_ * 2.2 * u, hy - 0.6 * u, 1.3 * u, 8), tint((250, 244, 230)), alfa=A)
            lz.relleno(circulo(hx + s_ * 2.2 * u, hy - 0.6 * u, 0.6 * u, 6), tint((40, 20, 40)), alfa=A)
        lz.relleno(np.array([[hx - 2.4 * u, hy + 2.4 * u], [hx, hy + 1.4 * u], [hx + 2.4 * u, hy + 2.4 * u], [hx, hy + 3.4 * u]]), tint((200, 40, 50)), alfa=A)
        for k in range(3):
            lz.relleno(np.array([[hx + (k - 1) * 2.6 * u - 1.0 * u, hy - 5.4 * u], [hx + (k - 1) * 2.6 * u, hy - 9.0 * u], [hx + (k - 1) * 2.6 * u + 1.0 * u, hy - 5.4 * u]]), tint((250, 200, 84)), alfa=A)
    else:
        _sombrero_base(lz, tipo, hx, hy, u, A, lado, pelo, spec, frente)


def _arma(lz, arma, mano, u, lado, A, t, seed, accion, vel):
    if arma == "arco":
        mx, my = mano
        lz.trazo(np.array([[mx, my - 12 * u], [mx + 5 * u * lado, my], [mx, my + 12 * u]]), (140, 100, 70), 1.6 * u * iso_k(), afinar=False, temblor=0.0, capa=2) if False else None
        _tira(lz, (mx, my - 12 * u), 0.0, 24 * u, 1.3 * u, (140, 100, 70), A)
        _tira(lz, (mx - 0.4 * u, my - 12 * u), 0.0, 24 * u, 0.4 * u, (240, 232, 214), A)
        _tira(lz, (mx, my), 1.57 * lado, 16 * u, 0.7 * u, (190, 150, 100), A)
        lz.relleno(np.array([[mx + 16 * u * lado, my - 1.2 * u], [mx + 19 * u * lado, my], [mx + 16 * u * lado, my + 1.2 * u]]), tint((226, 232, 244)), alfa=A)
    elif arma == "macuahuitl":
        mx, my = mano
        a = 2.4 + 0.9 * math.sin(t * 6 + seed) if accion == "pelea" else 2.9
        _tira(lz, (mx, my), a, 17 * u, 3.2 * u, (170, 120, 80), A)
        for k in range(5):
            px_, py_ = mx + math.sin(a) * (4 + k * 2.6) * u, my + math.cos(a) * (4 + k * 2.6) * u
            lz.relleno(np.array([[px_ - 2.0 * u, py_ - 0.6 * u], [px_ - 3.3 * u, py_ + 0.6 * u], [px_ - 2.0 * u, py_ + 1.4 * u]]), tint((40, 36, 52)), alfa=A)
            lz.relleno(np.array([[px_ + 2.0 * u, py_ - 0.6 * u], [px_ + 3.3 * u, py_ + 0.6 * u], [px_ + 2.0 * u, py_ + 1.4 * u]]), tint((40, 36, 52)), alfa=A)
    else:
        _arma_base(lz, arma, mano, u, lado, A, t, seed, accion, vel)


def iso_k():
    return 1.0
