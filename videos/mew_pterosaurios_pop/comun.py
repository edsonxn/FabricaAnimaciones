# -*- coding: utf-8 -*-
"""Base común (kit de La Hoguera / hog_pruebas + hog_nuevo) para el reel de los pterosaurios en RECETARIO.
Sprites = float32 RGBA PREMULTIPLICADO 0..1. Lienzo = float32 HxWx3 0..1.
Línea de tiempo: salida 0-13,5 = fuente 0-13,5 · 13,5-14,1 pase de hoja (fuente congelada en 22,87) ·
después fuente 22,87→90,57 (se quita su intro de banda 14,0-22,87) · cierre hasta DUR.
   python recetario.py hoja 1.0 5.9 ...  cuadros sueltos (tiempos de SALIDA) → previews/recetario_hoja.jpg
   python recetario.py video             render en partes → salida/recetario.mp4 (con audio/mezcla_recetario.wav)
"""
import functools, json, math, subprocess, sys
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

A = Path(__file__).parent
W, H, FPS = 1080, 1920, 30
CUT_A, GAP, SRC_B, SRC_FIN = 13.5, 0.6, 22.87, 90.567
FIN_EL = CUT_A + GAP + (SRC_FIN - SRC_B)       # 81,80 s: aquí se acaba su toma
DUR = FIN_EL + 2.6
NSRC = 2717
N = int(DUR * FPS)


def fuente(t):
    """Tiempo de salida → tiempo de la fuente (sigue de largo después del final, para el cierre)."""
    if t < CUT_A:
        return t
    if t < CUT_A + GAP:
        return SRC_B + 0.1                       # cuadro congelado (el primero limpio después de la intro)
    return SRC_B + t - CUT_A - GAP


def salida(ts):
    """Tiempo de la fuente → tiempo de salida."""
    return ts if ts < CUT_A + 0.001 else CUT_A + GAP + ts - SRC_B
FU = "C:/Windows/Fonts/"
F_IMPACT, F_BAHN, F_GEO, F_GEOB, F_GEOI = FU + "impact.ttf", FU + "bahnschrift.ttf", FU + "georgia.ttf", FU + "georgiab.ttf", FU + "georgiai.ttf"
F_COMIC, F_SCRIPT, F_INK, F_JP, F_POP = FU + "comicbd.ttf", FU + "segoeprb.ttf", FU + "Inkfree.ttf", FU + "YuGothB.ttc", str(A.parent.parent / "nucleo/tactica3d/fuentes/Poppins-Black.ttf")
F_SYM = FU + "seguisym.ttf"

PAL = json.load(open(A / "fuente/palabras.json", encoding="utf-8"))["palabras"]
try:
    SEG = json.load(open(A / "fuente/seguimiento.json", encoding="utf-8"))   # por cuadro de la fuente: [cx, top] suavizados
except FileNotFoundError:
    SEG = []


# ---------- tiempo ----------
def c01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else float(x)


def rampa(t, t0, d):
    return c01((t - t0) / d)


def suave(x):
    x = c01(x); return x * x * (3 - 2 * x)


def sale(x):                       # ease-out cúbico
    x = c01(x); return 1 - (1 - x) ** 3


def rebote(x, s=1.9):              # ease-out-back (se pasa y vuelve)
    x = c01(x) - 1; return 1 + (s + 1) * x ** 3 + s * x ** 2


def ventana(t, t0, t1, din=0.3, dout=0.3):
    """0→1 en t0, 1→0 al llegar a t1."""
    return min(rampa(t, t0, din), 1 - rampa(t, t1 - dout, dout))


def golpe(t, t0, d=0.35):          # 1 en t0 y cae a 0: para sacudidas y destellos
    return 0.0 if t < t0 else math.exp(-(t - t0) / d * 4)


# ---------- ruido ----------
@functools.lru_cache(maxsize=64)
def ruido(h, w, celda, semilla=0, octavas=4):
    """fbm 0..1 de h x w; celda = tamaño del grano mayor en px."""
    rng = np.random.default_rng(semilla)
    out = np.zeros((h, w), np.float32); amp, tot = 1.0, 0.0
    for o in range(octavas):
        c = max(2, int(celda / 2 ** o))
        g = rng.random((h // c + 3, w // c + 3)).astype(np.float32)
        out += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC); tot += amp; amp *= 0.5
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def desplaza(tex, dx, dy):
    """Textura envolvente desplazada (np.roll entero)."""
    return np.roll(np.roll(tex, int(dy) % tex.shape[0], 0), int(dx) % tex.shape[1], 1)


# ---------- sprites ----------
def pre(rgb, a):
    return np.dstack([rgb * a[..., None], a]).astype(np.float32)


def cargar(nombre, ancho=None):
    """img/<nombre>.* → RGB float 0..1."""
    f = next((A / "img").glob(nombre + ".*"))
    im = Image.open(f).convert("RGB")
    if ancho:
        im = im.resize((ancho, int(im.height * ancho / im.width)), Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 255.0


@functools.lru_cache(maxsize=256)
def texto(txt, fuente, tam, color=(1, 1, 1), borde=0, cborde=(0, 0, 0), esp=0, idx=0):
    """Texto → sprite premultiplicado. esp = espaciado extra entre letras."""
    f = ImageFont.truetype(fuente, tam, index=idx)
    m = borde + 6
    anchos = [f.getlength(ch) + esp for ch in txt]
    bb = f.getbbox(txt)
    w, h = int(sum(anchos) + 2 * m), int(bb[3] + tam * 0.25 + 2 * m)
    im = Image.new("L", (w, h), 0); bo = Image.new("L", (w, h), 0)
    d, db = ImageDraw.Draw(im), ImageDraw.Draw(bo)
    x = m
    for ch, an in zip(txt, anchos):
        d.text((x, m), ch, font=f, fill=255)
        if borde:
            db.text((x, m), ch, font=f, fill=255, stroke_width=borde, stroke_fill=255)
        x += an
    a = np.asarray(im).astype(np.float32) / 255
    if borde:
        b = np.asarray(bo).astype(np.float32) / 255
        rgb = np.array(color, np.float32) * a[..., None] + np.array(cborde, np.float32) * (b - a * b)[..., None]
        return np.dstack([rgb, b]).astype(np.float32)
    return pre(np.broadcast_to(np.array(color, np.float32), a.shape + (3,)), a)


def transf(sp, escala=1.0, rot=0.0, sx=None):
    """Escala (y rotación en grados) un sprite premultiplicado alrededor de su centro."""
    h, w = sp.shape[:2]
    ex = escala if sx is None else sx
    if rot == 0 and escala == 1 and sx is None:
        return sp
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    nw = int(abs(w * ex * c) + abs(h * escala * s)) + 2; nh = int(abs(w * ex * s) + abs(h * escala * c)) + 2
    M = np.array([[ex * c, -escala * s, nw / 2 - (ex * c * w / 2 - escala * s * h / 2)],
                  [ex * s, escala * c, nh / 2 - (ex * s * w / 2 + escala * c * h / 2)]], np.float32)
    return cv2.warpAffine(sp, M, (nw, nh), flags=cv2.INTER_LINEAR if escala > 0.6 else cv2.INTER_AREA, borderValue=0)


def pegar(L, sp, cx, cy, op=1.0, suma=False):
    """Pega el sprite centrado en (cx, cy). suma=True → aditivo (luz)."""
    if op <= 0.003:
        return
    h, w = sp.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    a0, b0, a1, b1 = max(0, x0), max(0, y0), min(L.shape[1], x0 + w), min(L.shape[0], y0 + h)
    if a1 <= a0 or b1 <= b0:
        return
    s = sp[b0 - y0:b1 - y0, a0 - x0:a1 - x0]
    d = L[b0:b1, a0:a1]
    if suma:
        d += s[..., :3] * op
    else:
        d *= 1 - s[..., 3:4] * op
        d += s[..., :3] * op


def sombra(sp, desen=14, op=0.55):
    """Sprite de sombra (negro) del alfa del sprite."""
    a = cv2.GaussianBlur(np.pad(sp[..., 3], desen * 2), (0, 0), desen) * op
    return np.dstack([np.zeros(a.shape + (3,), np.float32), a])


def brillo(sp, desen, color):
    """Halo aditivo del alfa del sprite."""
    a = cv2.GaussianBlur(np.pad(sp[..., 3], int(desen * 2.5)), (0, 0), desen)
    return np.dstack([a[..., None] * np.array(color, np.float32), a]).astype(np.float32)


def forma(tam, dibujar, ss=3):
    """Máscara 0..1 dibujada con PIL (dibujar(d, T) pinta en un lienzo de lado T=tam*ss)."""
    T = tam * ss
    im = Image.new("L", (T, T), 0)
    dibujar(ImageDraw.Draw(im), T)
    return np.asarray(im.resize((tam, tam), Image.LANCZOS)).astype(np.float32) / 255


@functools.lru_cache(maxsize=4)
def m_cilindro(tam=520):
    """Tambor de revólver: disco con 6 recámaras (1 = metal, 0 = hueco)."""
    def dib(d, T):
        c = T / 2
        d.ellipse([c - T * .47, c - T * .47, c + T * .47, c + T * .47], fill=255)
        for k in range(6):
            a = math.radians(60 * k + 30)
            x, y = c + T * .285 * math.cos(a), c + T * .285 * math.sin(a)
            d.ellipse([x - T * .105, y - T * .105, x + T * .105, y + T * .105], fill=0)
            x, y = c + T * .47 * math.cos(a + math.radians(30)), c + T * .47 * math.sin(a + math.radians(30))
            d.ellipse([x - T * .055, y - T * .055, x + T * .055, y + T * .055], fill=0)
        d.ellipse([c - T * .06, c - T * .06, c + T * .06, c + T * .06], fill=0)
    return forma(tam, dib)


@functools.lru_cache(maxsize=4)
def m_higado(tam=300):
    """Silueta de hígado (dos lóbulos)."""
    def dib(d, T):
        pts = []
        for k in range(160):
            a = 2 * math.pi * k / 160
            x = math.cos(a)
            ancho = 0.30 * (1 - 0.52 * (x + 1) / 2)                    # lóbulo grande a la izquierda, punta a la derecha
            y = math.sin(a) * ancho - 0.05 * x * x + (0.035 * math.exp(-((x - 0.05) / 0.10) ** 2) if math.sin(a) > 0 else 0) * -1
            pts.append((T * (.5 + 0.45 * x), T * (.52 + y)))
        d.polygon(pts, fill=255)
    return cv2.GaussianBlur(forma(tam, dib), (0, 0), 1.2)


@functools.lru_cache(maxsize=8)
def m_glifo(ch, tam=300, fuente=F_SYM):
    f = ImageFont.truetype(fuente, tam)
    bb = f.getbbox(ch)
    im = Image.new("L", (bb[2] - bb[0] + 8, bb[3] - bb[1] + 8), 0)
    ImageDraw.Draw(im).text((4 - bb[0], 4 - bb[1]), ch, font=f, fill=255)
    return np.asarray(im).astype(np.float32) / 255


@functools.lru_cache(maxsize=16)
def recorte(nombre, ancho=900):
    """img/<nombre>.* sin fondo → (rgb, alfa) recortado a su caja. PNG con alfa se usa tal cual;
    si no, rembg una vez (se guarda en img/_<nombre>.png)."""
    f = next(x for x in (A / "img").glob(nombre + ".*"))
    im = Image.open(f)
    if im.mode != "RGBA" or np.asarray(im)[..., 3].min() > 250:
        g = A / f"img/_{nombre}.png"
        if not g.exists():
            from rembg import new_session, remove
            remove(im.convert("RGB"), session=new_session("isnet-general-use")).save(g)
        im = Image.open(g)
        px = np.asarray(Image.open(f).convert("RGB").resize(im.size))
        al = np.asarray(im)[..., 3]
        im = Image.fromarray(np.dstack([px, al]))
    im = im.convert("RGBA"); im = im.crop(im.getbbox())
    im = im.resize((ancho, int(im.height * ancho / im.width)), Image.LANCZOS)
    x = np.asarray(im).astype(np.float32) / 255
    return x[..., :3], x[..., 3]


# ---------- la persona ----------


# ---------- la persona ----------
def persona(ts, x_dst=540, fondo=1800, s=0.72):
    """Él en el tiempo de fuente ts: cuadro volteado escalado s, con el borde de abajo del cuadro en y=fondo
    (queda bajo la cinta) y la cabeza centrada en x_dst (seguimiento suave). Devuelve (rgb, alfa)."""
    i = int(min(max(round(ts * FPS), 0), NSRC - 1))
    f = A / f"fuente/alfa_l/a_{i + 1:04d}.png"
    if not f.exists():
        return None, None
    rgb = cv2.imread(str(A / f"fuente/cuadros/c_{i + 1:04d}.jpg"))[..., ::-1].astype(np.float32) / 255
    a = cv2.imread(str(f), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    cx = SEG[i][0] if SEG else 880
    x0 = min(0.0, max(W - s * rgb.shape[1], x_dst - s * cx))
    M = np.array([[s, 0, x0], [0, s, fondo - s * rgb.shape[0]]], np.float32)
    return (cv2.warpAffine(rgb, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE),
            cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR))


def cuadro_fuente(ts, voltear=False):
    """Cuadro original (sin voltear = como lo publicó él, con sus textos legibles) en el tiempo ts → RGB float."""
    i = int(min(max(round(ts * FPS), 0), NSRC - 1))
    x = cv2.imread(str(A / f"fuente/cuadros/c_{i + 1:04d}.jpg"))[..., ::-1]
    return np.ascontiguousarray(x if voltear else x[:, ::-1]).astype(np.float32) / 255


# ---------- salida ----------
def _ffmpeg(sal):
    return subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(sal)], stdin=subprocess.PIPE)


def a8(L):
    return (np.clip(L, 0, 1) * 255 + 0.5).astype(np.uint8)


def principal(Clase, nombre, procesos=3):
    (A / "salida").mkdir(exist_ok=True); (A / "previews").mkdir(exist_ok=True)
    c = sys.argv[1] if len(sys.argv) > 1 else "hoja"
    if c == "hoja":
        ts = [float(x) for x in sys.argv[2:] if not x.startswith("-")] or [1, 5, 9, 13, 16, 20, 24, 30, 36, 42, 50, 56, 62, 68, 74, 80, 83]
        e = Clase()
        cols = min(len(ts), 6); filas = (len(ts) + cols - 1) // cols
        hoja = Image.new("RGB", (360 * cols, 640 * filas))
        for k, t in enumerate(ts):
            im = Image.fromarray(a8(e.cuadro(int(round(t * FPS)))))
            if len(ts) == 1:
                im.save(A / f"previews/{nombre}_{t:05.2f}.jpg", quality=90)
            d = ImageDraw.Draw(im)
            d.text((14, 10), f"{t:.2f}", fill=(255, 0, 0), font=ImageFont.truetype(F_GEOB, 40))
            hoja.paste(im.resize((360, 640), Image.LANCZOS), ((k % cols) * 360, (k // cols) * 640))
        hoja.save(A / f"previews/{nombre}_hoja.jpg", quality=86)
    elif c == "parte":
        k, n = int(sys.argv[2]), int(sys.argv[3])
        e = Clase()
        p = _ffmpeg(A / f"salida/_{nombre}_p{k}.mp4")
        for i in range(N * k // n, N * (k + 1) // n):
            p.stdin.write(a8(e.cuadro(i)).tobytes())
        p.stdin.close(); p.wait()
    elif c == "video":
        n = procesos
        ps = [subprocess.Popen([sys.executable, sys.argv[0], "parte", str(k), str(n)]) for k in range(n)]
        for p in ps:
            p.wait()
        malos = [k for k, p in enumerate(ps) if p.returncode != 0]
        if malos:
            sys.exit(f"partes fallidas: {malos} (rehacer con «parte k {n}» y concatenar)")
        lista = A / f"salida/_{nombre}.txt"
        lista.write_text("".join(f"file '_{nombre}_p{k}.mp4'\n" for k in range(n)))
        audio = A / f"audio/mezcla_{nombre}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista), "-i", str(audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                        "-shortest", "-movflags", "+faststart", str(A / f"salida/{nombre}.mp4")], check=True)
        for k in range(n):
            (A / f"salida/_{nombre}_p{k}.mp4").unlink()
        lista.unlink()
        print("listo", A / f"salida/{nombre}.mp4")
