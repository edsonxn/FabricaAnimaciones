# -*- coding: utf-8 -*-
"""Arma «Un segundo» (video de ~2 min): imágenes de Flow con cámara viva + motion graphics + voz y SFX de ElevenLabs.
Uso: python armar.py            -> un_segundo.mp4
     python armar.py hoja       -> hoja.jpg (un cuadro por segmento, para revisar)"""
import glob, json, math, os, subprocess, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30
F = r"C:\Users\jaire\AppData\Local\Microsoft\Windows\Fonts"
BLACK, XBOLD, SEMI = f"{F}\\Poppins-Black.ttf", f"{F}\\Poppins-ExtraBold.ttf", f"{F}\\Poppins-SemiBold.ttf"
AMARILLO, CREMA, ROSA, TINTA = (63, 210, 255), (224, 244, 255), (109, 77, 255), (51, 12, 20)   # BGR

lineas = json.load(open(f"{AQUI}/voz/lineas.json", encoding="utf-8"))
D = [l["dur"] for l in lineas]
PAUSA = [.6, .55, .5, .7, .9, .9, 1.3, .7, .8, 1.5, 1.0, .7, 1.8, .8, .9, 1.2, .6, 1.7, 1.4]
INICIO, TARJETA = 1.2, 7.0
T0 = []
t = INICIO
for d, p in zip(D, PAUSA):
    T0.append(t); t += d + p
T_FIN = t
TOTAL = T_FIN + TARJETA


def img(n):
    p = sorted(glob.glob(f"{AQUI}/img/p{n:02d}_*.png"))
    im = cv2.imread(p[0]) if p else np.full((768, 1376, 3), 40, np.uint8)
    h, w = im.shape[:2]
    k = max(2560 / w, 1440 / h)
    im = cv2.resize(im, (round(w * k), round(h * k)), interpolation=cv2.INTER_LANCZOS4)
    y, x = (im.shape[0] - 1440) // 2, (im.shape[1] - 2560) // 2
    return im[y:y + 1440, x:x + 2560]


IMG = {n: img(n) for n in range(1, 17)}
ease = lambda u: u * u * (3 - 2 * u)
clamp = lambda u: max(0.0, min(1.0, u))


def camara(im, u, a, b, sx=0, sy=0):
    """a, b = (zoom, cx, cy) con cx, cy en -1..1; u en 0..1."""
    e = ease(clamp(u))
    z = a[0] + (b[0] - a[0]) * e
    cx = (a[1] + (b[1] - a[1]) * e) * 2560 * .12
    cy = (a[2] + (b[2] - a[2]) * e) * 1440 * .12
    s = z * W / 2560
    M = np.float32([[s, 0, W / 2 - s * (1280 + cx) + sx], [0, s, H / 2 - s * (720 + cy) + sy]])
    return cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
RAD = np.clip((np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) - .45) / .75, 0, 1)[..., None]
LINEAS_TV = ((yy.astype(int) // 4) % 2)[..., None].astype(np.float32)


def vineta(f, color, fuerza):
    return (f * (1 - RAD * fuerza) + np.float32(color) * RAD * fuerza).astype(np.uint8)


def desaturar(f, k):
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)[..., None]
    return (f * (1 - k) + g * k).astype(np.uint8)


def tinte(f, color, k):
    return (f * (1 - k) + (f.astype(np.float32) * np.float32(color) / 255) * k).astype(np.uint8)


def oscurecer(f, k):
    return (f * (1 - k)).astype(np.uint8)


_cache = {}


def rotulo(texto, tam, color, fuente=BLACK, caja=None, pad=(46, 22)):
    key = (texto, tam, color, fuente, caja)
    if key in _cache:
        return _cache[key]
    fnt = ImageFont.truetype(fuente, tam)
    x0, y0, x1, y1 = fnt.getbbox(texto)
    w, h = x1 - x0, y1 - y0
    px, py = pad if caja else (16, 16)
    im = Image.new("RGBA", (w + 2 * px + 24, h + 2 * py + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rgb = lambda c: (c[2], c[1], c[0])
    if caja:
        d.rounded_rectangle((0, 0, w + 2 * px, h + 2 * py), radius=(h + 2 * py) // 2, fill=rgb(caja) + (255,))
    else:
        d.text((px - x0 + 6, py - y0 + 8), texto, font=fnt, fill=(8, 4, 24, 190))
    d.text((px - x0, py - y0), texto, font=fnt, fill=rgb(color) + (255,))
    a = np.array(im)
    _cache[key] = a[..., [2, 1, 0, 3]].copy()
    return _cache[key]


def pegar(f, r, cx, cy, escala=1.0, alfa=1.0):
    if alfa <= 0 or escala <= 0.02:
        return
    if abs(escala - 1) > .005:
        r = cv2.resize(r, None, fx=escala, fy=escala, interpolation=cv2.INTER_LINEAR)
    h, w = r.shape[:2]
    x, y = int(cx - w / 2), int(cy - h / 2)
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    rr = r[y0 - y:y1 - y, x0 - x:x1 - x]
    a = rr[..., 3:4].astype(np.float32) / 255 * alfa
    f[y0:y1, x0:x1] = (f[y0:y1, x0:x1] * (1 - a) + rr[..., :3] * a).astype(np.uint8)


def pop(dt, dur=.35):
    """Escala con rebote (anticipación y asentado), estilo Fábrica."""
    if dt <= 0:
        return 0
    u = dt / dur
    return 1.0 if u >= 1.6 else 1 - math.exp(-6 * u) * math.cos(9 * u)


def temblor(dt, amp=26, dur=.45):
    if dt < 0 or dt > dur:
        return 0, 0
    k = amp * (1 - dt / dur)
    return k * math.sin(dt * 95), k * math.cos(dt * 71)


def seg(n):
    return T0[n - 1], D[n - 1] + PAUSA[n - 1]


# momento del golpe (fin de la línea 6) y del empujón (línea 3)
T_EMPUJON = T0[2] + 1.0
T_GOLPE = T0[5] + D[5] - .35
T_NADIE = T0[15] + D[15] * .64           # «Porque nadie se salva…»
T_SUYO = T0[9] + D[9] * .52              # «Pero el golpe fue suyo»


def cuadro(t):
    # ---- qué segmento ----
    if t >= T_FIN:
        return tarjeta(t - T_FIN)
    n = 1
    for i in range(19):
        if t >= T0[i]:
            n = i + 1
    t0, dur = seg(n)
    if n == 1:
        t0, dur = 0, T0[1]
    u = (t - t0) / dur
    dt = t - t0

    if n == 1:
        f = camara(IMG[1], u, (1.0, 0, .3), (1.22, 0, -.1))
        s = pop(t - 1.5)
        pegar(f, rotulo("JALPA, ZACATECAS", 64, TINTA, BLACK, caja=AMARILLO), 390, 880, s)
        pegar(f, rotulo("Martes · 10:42 a.m. · Recreo", 40, CREMA, SEMI, caja=TINTA), 400, 975, pop(t - 1.9))
        f = oscurecer(f, 1 - clamp(t / .8))
    elif n == 2:
        f = camara(IMG[2], u, (1.08, -.4, 0), (1.25, .3, -.1))
    elif n == 3:
        sx, sy = temblor(t - T_EMPUJON, 34, .5)
        z = 1.05 if t < T_EMPUJON else 1.05 + .28 * ease(clamp((t - T_EMPUJON) / .25))
        f = camara(IMG[3], u, (z, 0, 0), (z + .06, 0, .1), sx, sy)
        fl = clamp(1 - (t - T_EMPUJON) / .18) if t >= T_EMPUJON else 0
        f = cv2.addWeighted(f, 1 - fl * .7, np.full_like(f, 255), fl * .7, 0)
    elif n == 4:
        f = camara(IMG[4], u, (1.25, 0, .2), (1.05, 0, 0))
        if int(t * 2) % 2 == 0:
            cv2.circle(f, (150, 120), 26, (60, 40, 255), -1, cv2.LINE_AA)
        pegar(f, rotulo("REC", 60, CREMA, BLACK), 260, 122)
    elif n == 5:
        lat = max(0, math.sin(t * 2 * math.pi * 2.3)) ** 6
        f = camara(IMG[5], u, (1.1 + .035 * lat, 0, -.2), (1.4 + .035 * lat, 0, .1))
        f = vineta(f, (60, 20, 255), .35 + .4 * lat)
    elif n == 6:
        sx, sy = temblor(t - T_GOLPE, 46, .6)
        f = camara(IMG[6], u, (1.3, .2, 0), (1.06, 0, 0), sx, sy)
        if dt < 1.25:
            f = oscurecer(f, .6 * clamp((1.25 - dt) / .3))
            pegar(f, rotulo("PRIMER FINAL", 200, CREMA, BLACK), W / 2, H / 2, pop(dt, .4), clamp((1.25 - dt) / .2))
        fl = clamp(1 - (t - T_GOLPE) / .22) if t >= T_GOLPE else 0
        f = cv2.addWeighted(f, 1 - fl, np.full_like(f, 255), fl, 0)
        f = vineta(f, (60, 20, 255), .3)
    elif n == 7:
        f = desaturar(camara(IMG[7], u, (1.35, .1, .3), (1.05, 0, 0)), .55 * clamp(dt / 1.2))
        f = vineta(f, (30, 10, 20), .55)
    elif n == 8:
        f = camara(IMG[8], u, (1.05, 0, 0), (1.3, 0, 0))
        f = vineta(f, (30, 10, 20), .4)
    elif n == 9:
        sir = .5 + .5 * math.sin(t * 7)
        f = camara(IMG[9], u, (1.08, .3, 0), (1.2, -.2, 0))
        f = vineta(f, (255 * (1 - sir), 30, 255 * sir), .28)
    elif n == 10:
        f = desaturar(camara(IMG[10], u, (1.04, 0, 0), (1.34, 0, .15)), .35)
        f = vineta(f, (30, 10, 20), .6)
        if t >= T_SUYO:
            d2 = t - T_SUYO
            pegar(f, rotulo("EL GOLPE FUE SUYO", 120, AMARILLO, BLACK), W / 2, 900, pop(d2, .4), clamp((t0 + dur - .15 - t) / .3))
    elif n == 11:
        orden = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        k = min(int(u * len(orden) * 1.0), len(orden) - 1)
        f = camara(IMG[orden[k]], u, (1.15, 0, 0), (1.15, 0, 0))
        dx = int(60 * math.sin(t * 50))
        f = np.roll(f, dx, axis=1)
        f[::, :, :] = (f * (.72 + .28 * LINEAS_TV)).astype(np.uint8)
        y = int((t * 900) % H)
        f[y:y + 40] = np.clip(f[y:y + 40].astype(np.int16) + 70, 0, 255).astype(np.uint8)
        f = desaturar(f, .5)
        if int(t * 5) % 2 == 0:
            pegar(f, rotulo("«« REBOBINAR", 110, AMARILLO, BLACK), W / 2, H / 2)
    elif n == 12:
        partes = [(1, (1.1, 0, 0)), (3, (1.3, 0, 0)), (3, (1.75, .1, .75)), (5, (1.3, 0, -.2))]
        k = min(int(u * 1.12 * 4), 3)
        uu = u * 1.12 * 4 - k
        im, (z, cx, cy) = partes[k]
        f = camara(IMG[im], uu, (z, cx, cy), (z + .08, cx, cy))
        fl = clamp(1 - uu / .12)
        f = cv2.addWeighted(f, 1 - fl * .5, np.full_like(f, 255), fl * .5, 0)
        if k == 3:
            f = vineta(f, (60, 20, 255), .45)
    elif n == 13:
        f = camara(IMG[11], u, (1.3, 0, .1), (1.04, 0, 0))
        f = tinte(f, (255, 225, 190), .25)
        tn = t0 + D[12] * .62
        if t >= tn:
            pegar(f, rotulo("UN SEGUNDO", 150, CREMA, BLACK), W / 2, 170, pop(t - tn, .5), clamp((t0 + dur - .1 - t) / .4))
    elif n == 14:
        f = camara(IMG[12], u, (1.05, -.2, 0), (1.25, .1, -.1))
    elif n == 15:
        f = camara(IMG[13], u, (1.25, .2, -.1), (1.06, 0, 0))
    elif n == 16:
        f = camara(IMG[14], u, (1.05, .2, 0), (1.3, -.1, -.1))
        if t >= T_NADIE:
            d2 = t - T_NADIE
            f = oscurecer(f, .55 * clamp(d2 / .4))
            pegar(f, rotulo("NADIE SE SALVA", 150, CREMA, BLACK), W / 2, 440, pop(d2, .4))
            pegar(f, rotulo("DE LAS CONSECUENCIAS", 118, AMARILLO, BLACK), W / 2, 610, pop(d2 - .45, .4))
            pegar(f, rotulo("de lo que hace", 80, CREMA, XBOLD), W / 2, 750, pop(d2 - 1.5, .4))
    elif n == 17:
        a = vineta(desaturar(camara(IMG[9], u, (1.2, .1, 0), (1.3, .1, 0)), .5), (60, 20, 200), .5)
        b = camara(IMG[15], u, (1.2, 0, 0), (1.3, 0, 0))
        corte = W * (1.25 - .75 * ease(clamp(dt / .7)))
        m = np.clip((xx - (corte - (yy - H / 2) * .22)) / 3 + .5, 0, 1)[..., None]
        f = (a * (1 - m) + b * m).astype(np.uint8)
        borde = (np.abs(xx - (corte - (yy - H / 2) * .22)) < 7)[..., None]
        f = np.where(borde, np.uint8(CREMA), f).astype(np.uint8)
    elif n == 18:
        f = camara(IMG[15], u, (1.3, 0, 0), (1.12, 0, 0))
        pegar(f, rotulo("UN SEGUNDO.", 200, AMARILLO, BLACK), W / 2, 165, pop(dt - .25, .5))
    else:
        f = camara(IMG[16], u, (1.04, 0, 0), (1.26, 0, -.1))
        f = oscurecer(f, clamp((t - (T_FIN - .6)) / .6))
    return f


FONDO = None
_lg = cv2.imread(f"{AQUI}/logos.png", cv2.IMREAD_UNCHANGED)
LOGOS = cv2.resize(_lg, (1400, round(1400 * _lg.shape[0] / _lg.shape[1])), interpolation=cv2.INTER_AREA)


def tarjeta(dt):
    global FONDO
    if FONDO is None:
        g = np.zeros((H, W, 3), np.float32)
        r = np.clip(1 - np.hypot((xx - W * .5) / W, (yy - H * .2) / H) * 1.5, 0, 1)[..., None]
        FONDO = (np.float32((51, 12, 20)) * (1 - r) + np.float32((156, 42, 74)) * r)
    f = FONDO.astype(np.uint8).copy()
    pegar(f, rotulo("UN SEGUNDO", 250, AMARILLO, BLACK), W / 2, 300, pop(dt - .3, .5))
    pegar(f, rotulo("puede cambiar toda la historia.", 70, CREMA, XBOLD), W / 2, 490, pop(dt - .9, .4))
    pegar(f, rotulo("HABLEMOS PARA ENTENDERNOS", 58, TINTA, BLACK, caja=CREMA), W / 2, 690, pop(dt - 1.6, .4))
    pegar(f, LOGOS, W / 2, 900, 1, clamp((dt - 2.2) / .6))
    return oscurecer(oscurecer(f, 1 - clamp(dt / .5)), clamp((dt - (TARJETA - .8)) / .8))


def audio(salida, video):
    ent, filt, mix = [], [], []

    def pon(ruta, en, vol=1.0, extra=""):
        i = len(ent) // 2 + 1; ent.extend(["-i", ruta])
        filt.append(f"[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo{extra},volume={vol},adelay={int(max(en, 0) * 1000)}:all=1[a{i}]")
        mix.append(f"[a{i}]")

    def bucle(ruta, en, hasta, vol):
        d = hasta - en
        pon(ruta, en, vol, f",aloop=loop=-1:size=2000000,atrim=0:{d:.2f},afade=t=in:d=1.2,afade=t=out:st={max(d - 1.8, 0):.2f}:d=1.8")

    for i in range(19):
        pon(f"{AQUI}/voz/l{i + 1:02d}.mp3", T0[i], 1.55)
    s = lambda k: f"{AQUI}/sfx/{k}.mp3"
    bucle(s("inicio"), 0, T_EMPUJON + .2, .30)
    bucle(s("patio"), 0, T_EMPUJON + .4, .35)
    pon(s("empujon"), T_EMPUJON - .15, .9)
    bucle(s("latido"), T0[4] - .2, T_GOLPE, .85)
    pon(s("boom"), T0[5], .55)
    pon(s("golpe"), T_GOLPE - .25, 1.0)
    pon(s("asombro"), T_GOLPE + .5, .55)
    bucle(s("oscuro"), T_GOLPE + .3, T0[10] + .2, .50)
    pon(s("notif"), T0[7] + 1.4, .35)
    pon(s("sirena"), T0[8] - .3, .30, ",afade=t=out:st=4.5:d=1.5")
    pon(s("boom"), T_SUYO - .1, .7)
    pon(s("rebobinar"), T0[10] + .5, .7)
    pon(s("empujon"), T0[11] + D[11] * .28, .5)
    bucle(s("latido"), T0[11] + D[11] * .7, T0[12] + D[12] * .45, .7)
    pon(s("respiro"), T0[12] + D[12] * .62, .9)
    bucle(s("luz"), T0[13] - .4, TOTAL - .2, .42)
    pon(s("boom"), T_NADIE - .1, .6)
    pon(s("boom"), T0[17] + .15, .8)
    pon(s("boom"), T_FIN + .3, .6)
    fc = ";".join(filt) + ";" + "".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,alimiter=limit=0.95,atrim=0:{TOTAL:.2f}[m]"
    open(f"{AQUI}/_fc.txt", "w", encoding="utf-8").write(fc)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, *ent, "-filter_complex_script", f"{AQUI}/_fc.txt",
                    "-map", "0:v", "-map", "[m]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", salida], check=True)


if __name__ == "__main__":
    print("duración total", round(TOTAL, 1), "s")
    if "audio" in sys.argv:
        audio(f"{AQUI}/un_segundo.mp4", f"{AQUI}/_mudo.mp4"); sys.exit()
    if "hoja" in sys.argv:
        ts = [T0[i] + (D[i] + PAUSA[i]) * (.75 if i not in (0,) else .6) for i in range(19)] + [T_GOLPE + .05, T_FIN + 4]
        mini = [cv2.resize(cuadro(x), (480, 270)) for x in ts]
        while len(mini) % 4:
            mini.append(np.zeros_like(mini[0]))
        cv2.imwrite(f"{AQUI}/hoja.jpg", np.vstack([np.hstack(mini[i:i + 4]) for i in range(0, len(mini), 4)]))
        sys.exit()
    mudo = f"{AQUI}/_mudo.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", mudo], stdin=subprocess.PIPE)
    N = int(TOTAL * FPS)
    for i in range(N):
        p.stdin.write(np.ascontiguousarray(cuadro(i / FPS)).tobytes())
        if i % 300 == 0:
            print(i, "/", N, flush=True)
    p.stdin.close(); p.wait()
    audio(f"{AQUI}/un_segundo.mp4", mudo)
    print("listo:", f"{AQUI}/un_segundo.mp4")
