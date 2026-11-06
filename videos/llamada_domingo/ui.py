# -*- coding: utf-8 -*-
"""ui.py — piezas dibujadas por código de «Llamada de domingo» (LogIA presenta).

Cada plano U(d, ui, a) de guion.PLANOS sale como medios/scene-NNN.mp4 (NNN = índice en PLANOS + 1), 1920x1080, 30 fps,
H.264 yuv420p + AAC 48 kHz estéreo, con la duración EXACTA del plano. Interfaz de la app PRESENTE (crema/ámbar sobre oscuro),
teléfonos y laptops en perspectiva 3D con sombra y reflejo, fondos de Flow (flow/bg, flow/esc) con Ken Burns, grano y viñeta.
Voces de ElevenLabs (eleven_v4_turbo) cacheadas en voz/ui_<clave>.mp3 (nunca se regeneran si existen); SFX sintetizados.

Uso:
  python videos/llamada_domingo/ui.py                    todas las piezas ui + hoja previews/ui_hoja.jpg
  python videos/llamada_domingo/ui.py notif_1 titulo     solo esas
  python videos/llamada_domingo/ui.py voces              solo genera las locuciones que falten
  python videos/llamada_domingo/ui.py llamada scene-004  interfaz de videollamada sobre un clip de Flow (audio intacto)
  python videos/llamada_domingo/ui.py hoja               solo la hoja de revisión
"""
import io
import math
import os
import subprocess
import sys
import types
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.signal import butter, sosfilt, fftconvolve

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE = r"C:\ffmpeg\bin\ffprobe.exe"
W, H, FPS, SR = 1920, 1080, 30, 48000      # FPS = el del motor (nucleo/secuencia.py, FAB_FPS por defecto 30)
FONTS = r"C:\Windows\Fonts"
MEDIOS = os.path.join(AQUI, "medios")
VOZ_DIR = os.path.join(AQUI, "voz")
PREV = os.path.join(AQUI, "previews")

# ───────────────────────────── voces (ElevenLabs) ─────────────────────────────
VALERIA = "hHjbwzYZW17oh0p05AKv"
ASIST = "m7yTemJqdIqrcNleANfX"
NOTI = "iDEmt5MnqUotdwCIVplo"
ANUN = "tGjegxe7yxhGMzd3SOmH"
MODELO = "eleven_v4_turbo"

VOCES = {
    # keynote_1 — Valeria Roca presenta PRESENTE
    "keynote_1_1": (VALERIA, "[warmly] Buenas noches. [short pause] Les quiero hacer una pregunta. [short pause] ¿Cuándo fue "
                             "la última vez que le llamaron a su papá? [short pause] ¿A su mamá?"),
    "keynote_1_2": (VALERIA, "No es que no los quieran. [short pause] Es que la vida no deja. La junta, el tráfico, el "
                             "vuelo… [sighs] y otra vez es lunes."),
    "keynote_1_3": (VALERIA, "Por eso creamos Presente. [short pause] Tres horas de entrevista. Tus fotos, tus audios, tus "
                             "chats. [short pause] Y tu Presente llama por ti. Con tu cara. Con tu voz."),
    "keynote_1_4": (VALERIA, "Con el modo discreto, ellos nunca reciben un aviso. [short pause] Solo sienten que estás."),
    "keynote_1_5": (VALERIA, "En las pruebas, el noventa y cuatro por ciento de los padres nunca lo notó. [short pause] Lo "
                             "único que notaron… es que su hijo volvió."),
    "keynote_1_6": (VALERIA, "Presente. [short pause] Para los que no pueden estar."),
    # anuncio en la tele
    "anuncio_1": (ANUN, "Tu papá te espera cada domingo."),
    "anuncio_2": (ANUN, "Pero tú tienes una junta. Un vuelo. Una vida."),
    "anuncio_3": (ANUN, "Con Presente, tres horas de entrevista bastan. [short pause] Tu Presente llama por ti. Con tu cara. "
                        "Con tu voz."),
    "anuncio_4": (ANUN, "Modo discreto. [short pause] Ellos solo sienten que estás. Y tú, por fin, descansas."),
    "anuncio_5": (ANUN, "Presente. Para los que no pueden estar."),
    # noticiero
    "noticiero_1": (NOTI, "Presente ya supera los cuarenta millones de usuarios en el país."),
    "noticiero_2": (NOTI, "Con la nueva Ley de Compañía Digital, ninguna empresa está obligada a avisarle al familiar que "
                          "habla con una inteligencia artificial."),
    "noticiero_3": (NOTI, "Y según la propia empresa, el noventa y cuatro por ciento de los padres nunca lo nota."),
    # la asistente de la app
    "onboard_1": (ASIST, "[warmly] Hola, Daniel. Vamos a conocer a tu papá. [short pause] ¿Cómo te dice cuando está contento?"),
    "onboard_2": (ASIST, "¿Y cuando está enojado?"),
    "onboard_3": (ASIST, "Última pregunta. [short pause] ¿Qué es lo que más le duele a tu papá?"),
    "onboard_4_1": (ASIST, "Entrevista completada. [short pause] Estamos creando a tu Presente."),
    "onboard_4_2": (ASIST, "Tu Presente está listo. [short pause] ¿Activamos el modo discreto? Tu papá nunca recibirá un aviso."),
    "agregar_lucia": (ASIST, "Listo. Desde hoy, tu Presente también atiende las llamadas de Lucía. [short pause] Ella no "
                             "recibirá ningún aviso."),
    # keynote_2 — PRESENTE Legado
    "keynote_2_1": (VALERIA, "Hace un año eran cuarenta millones. [short pause] Hoy, trescientos doce millones de familias "
                             "vuelven a hablar cada domingo."),
    "keynote_2_2": (VALERIA, "Pero nos hicieron una pregunta muy difícil. [short pause] ¿Qué pasa cuando ya no está?"),
    "keynote_2_3": (VALERIA, "Les presento Presente Legado. [short pause] Porque una llamada de domingo… no tiene por qué "
                             "terminar."),
}
GASTO = []   # (clave, caracteres cobrados) de esta corrida


def _eleven():
    """tts_eleven sin video activo: se le da un config mínimo (su `import config` cargaría otro guion)."""
    sys.path.insert(0, os.path.join(RAIZ, "nucleo"))
    sys.modules.setdefault("config", types.SimpleNamespace(VOZ=dict(modelo=MODELO, idioma="es", stability=0.5)))
    import tts_eleven
    tts_eleven.config = sys.modules["config"]
    return tts_eleven


def ruta_voz(clave):
    return os.path.join(VOZ_DIR, f"ui_{clave}.mp3")


def asegurar_voz(clave):
    """Genera la locución si no existe (una sola toma; no se gasta dos veces)."""
    p = ruta_voz(clave)
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        return p
    te = _eleven()
    vid, texto = VOCES[clave]
    texto = te.sin_etiquetas(texto)
    audio, coste = te.tts(texto, seed=1234, voice_id=vid)
    os.makedirs(VOZ_DIR, exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(audio)
    GASTO.append((clave, coste))
    print(f"  voz {clave}: {coste} créditos", flush=True)
    return p


@lru_cache(None)
def leer_audio(ruta):
    """Cualquier audio → float32 (n, 2) a 48 kHz."""
    out = subprocess.run([FF, "-v", "error", "-i", ruta, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()


def dur_voz(clave):
    return len(leer_audio(asegurar_voz(clave))) / SR


@lru_cache(None)
def voz_lista(clave):
    """Locución recortada (silencios de las puntas) y a nivel parejo (RMS −20 dBFS)."""
    a = leer_audio(asegurar_voz(clave))
    m = np.abs(a).max(1)
    idx = np.where(m > 0.006)[0]
    if len(idx):
        a = a[max(0, idx[0] - int(.03 * SR)): idx[-1] + int(.15 * SR)]
    rms = float(np.sqrt((a ** 2).mean())) or 1e-6
    a = a * (0.1 / rms)
    pk = float(np.abs(a).max())
    if pk > 0.93:
        a *= 0.93 / pk
    return a.astype(np.float32)


def dur(clave):
    return len(voz_lista(clave)) / SR


# ───────────────────────────── tiempo y curvas ─────────────────────────────
def cl(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def seg(t, a, b):
    return cl((t - a) / (b - a)) if b > a else (1.0 if t >= a else 0.0)


def ss(x):
    x = cl(x)
    return x * x * (3 - 2 * x)


def eo(x):
    x = cl(x)
    return 1 - (1 - x) ** 3


def eio(x):
    x = cl(x)
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def lerp(a, b, x):
    return a + (b - a) * x


def ven(t, a, b, fi=.4, fo=.4):
    """1 dentro de [a, b] con entrada y salida suaves."""
    return ss(seg(t, a, a + fi)) * (1 - ss(seg(t, b - fo, b)))


def vaiven(t, s=0.0):
    """Pulso de cámara en mano (suave, sin repetir): −1..1."""
    return (math.sin(t * 1.31 + s) * .55 + math.sin(t * 2.63 + s * 2.1) * .3 + math.sin(t * 4.9 + s * .7) * .15)


# ───────────────────────────── color y tipografía ─────────────────────────────
CREMA = (244, 232, 210)
CREMA2 = (214, 200, 178)
AMBAR = (233, 170, 84)
AMBAR_C = (248, 206, 142)
TINTA = (22, 18, 15)
PANEL = (38, 32, 27)
GRIS = (160, 148, 132)
GRIS_O = (96, 88, 79)
TERRA = (190, 92, 70)

_FN = dict(l="segoeuil.ttf", sl="segoeuisl.ttf", r="segoeui.ttf", sb="seguisb.ttf", b="segoeuib.ttf", li="seguili.ttf",
           i="segoeuii.ttf", geo="georgia.ttf", geoi="georgiai.ttf", ico="SegoeIcons.ttf")


@lru_cache(None)
def F(k, tam):
    tam = max(4, int(round(tam)))
    if k.startswith("bahn"):
        f = ImageFont.truetype(os.path.join(FONTS, "bahnschrift.ttf"), tam)
        f.set_variation_by_name(k[5:] or "Regular")
        return f
    return ImageFont.truetype(os.path.join(FONTS, _FN[k]), tam)


def rgba(c, a=1.0):
    return (int(c[0]), int(c[1]), int(c[2]), int(cl(a) * 255))


class Lz:
    """Lienzo PIL con supermuestreo (ss=2): coordenadas en px finales. fondo=None → capa transparente (premultiplicada al
    salir); fondo=(r,g,b) → lienzo opaco donde las tintas con alfa se mezclan."""

    def __init__(s, w, h, fondo=None, k=2):
        s.w, s.h, s.k = int(w), int(h), k
        if fondo is None:
            s.im = Image.new("RGBA", (s.w * k, s.h * k), (0, 0, 0, 0))
            s.d = ImageDraw.Draw(s.im)
        else:
            s.im = Image.new("RGB", (s.w * k, s.h * k), tuple(int(v) for v in fondo[:3]))
            s.d = ImageDraw.Draw(s.im, "RGBA")
        s.opaco = fondo is not None

    def rect(s, x0, y0, x1, y1, r=0, fill=None, outline=None, width=1):
        k = s.k
        if x1 * k - 1 <= x0 * k or y1 * k - 1 <= y0 * k:
            return
        s.d.rounded_rectangle([x0 * k, y0 * k, x1 * k - 1, y1 * k - 1], radius=max(0, r * k), fill=fill, outline=outline,
                              width=max(1, int(width * k)))

    def circ(s, x, y, r, fill=None, outline=None, width=1):
        k = s.k
        s.d.ellipse([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], fill=fill, outline=outline,
                    width=max(1, int(width * k)))

    def arc(s, x, y, r, a0, a1, fill, width):
        k = s.k
        if a1 - a0 <= 0.2:
            return
        s.d.arc([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], a0, a1, fill=fill, width=max(1, int(width * k)))

    def line(s, pts, fill, width=1):
        k = s.k
        s.d.line([(x * k, y * k) for x, y in pts], fill=fill, width=max(1, int(width * k)), joint="curve")

    def poly(s, pts, fill):
        k = s.k
        s.d.polygon([(x * k, y * k) for x, y in pts], fill=fill)

    def ancho(s, txt, f, tam, track=0):
        fo = F(f, tam * s.k)
        if not track:
            return fo.getlength(txt) / s.k
        return (sum(fo.getlength(c) for c in txt) + track * s.k * (len(txt) - 1)) / s.k

    def text(s, x, y, txt, f, tam, fill, anchor="ls", track=0):
        k = s.k
        fo = F(f, tam * k)
        if len(fill) == 3:
            fill = tuple(fill) + (255,)
        if not track:
            s.d.text((x * k, y * k), txt, font=fo, fill=fill, anchor=anchor)
            return fo.getlength(txt) / k
        tot = s.ancho(txt, f, tam, track)
        xx = x - (tot / 2 if anchor[0] == "m" else tot if anchor[0] == "r" else 0)
        for c in txt:
            s.d.text((xx * k, y * k), c, font=fo, fill=fill, anchor="l" + anchor[1])
            xx += fo.getlength(c) / k + track
        return tot

    def wrap(s, txt, f, tam, maxw):
        out, cur = [], ""
        for p in txt.split(" "):
            prueba = (cur + " " + p).strip()
            if s.ancho(prueba, f, tam) <= maxw or not cur:
                cur = prueba
            else:
                out.append(cur)
                cur = p
        if cur:
            out.append(cur)
        return out

    def parrafo(s, x, y, txt, f, tam, fill, maxw, inter=1.32, anchor="ls"):
        ls_ = s.wrap(txt, f, tam, maxw)
        for i, l in enumerate(ls_):
            s.text(x, y + i * tam * inter, l, f, tam, fill, anchor=anchor)
        return len(ls_) * tam * inter

    def foto(s, im, x, y, w, h, r=0, circulo=False, op=1.0):
        """Pega una foto (PIL) recortada a w×h (cover) con esquinas redondeadas o en círculo."""
        k = s.k
        W2, H2 = int(w * k), int(h * k)
        iw, ih = im.size
        esc = max(W2 / iw, H2 / ih)
        im2 = im.resize((max(1, int(iw * esc + .5)), max(1, int(ih * esc + .5))), Image.LANCZOS)
        ox, oy = (im2.size[0] - W2) // 2, (im2.size[1] - H2) // 2
        im2 = im2.crop((ox, oy, ox + W2, oy + H2)).convert("RGB")
        m = Image.new("L", (W2, H2), 0)
        dm = ImageDraw.Draw(m)
        if circulo:
            dm.ellipse([0, 0, W2 - 1, H2 - 1], fill=int(255 * op))
        else:
            dm.rounded_rectangle([0, 0, W2 - 1, H2 - 1], radius=int(r * k), fill=int(255 * op))
        s.im.paste(im2, (int(x * k), int(y * k)), m)

    def logo(s, x, y, r, col=AMBAR, a=1.0, prog=1.0, txt=True, tam=None, tcol=CREMA, track=None):
        """Marca PRESENTE: anillo + punto (una presencia) y la palabra espaciada."""
        w = max(1.5, r * .16)
        s.arc(x, y, r, -90, -90 + 360 * cl(prog), rgba(col, a), w)
        if prog > .75:
            rd = r * .36 * eo(seg(prog, .75, 1))
            s.circ(x, y, rd, fill=rgba(col, a))
        if txt:
            tam = tam or r * 1.05
            s.text(x + r * 1.75, y, "PRESENTE", "l", tam, rgba(tcol, a), anchor="lm", track=track if track is not None else tam * .38)

    def out(s):
        """Capa premultiplicada float32 (h, w, 4)."""
        a = np.asarray(s.im, np.float32) / 255.0
        if s.k != 1:
            a = cv2.resize(a, (s.w, s.h), interpolation=cv2.INTER_AREA)
        if s.opaco:
            return np.dstack([a, np.ones(a.shape[:2] + (1,), np.float32)])
        a[..., :3] *= a[..., 3:4]
        return a

    def rgb(s):
        a = np.asarray(s.im.convert("RGB"), np.float32) / 255.0
        if s.k != 1:
            a = cv2.resize(a, (s.w, s.h), interpolation=cv2.INTER_AREA)
        return a


# ───────────────────────────── imágenes de Flow ─────────────────────────────
def _ruta_img(clave):
    if clave.startswith("medios/"):
        return os.path.join(MEDIOS, clave[7:] + ".jpg")
    if os.path.isabs(clave):
        return clave
    return os.path.join(AQUI, "flow", clave + ".jpg")


@lru_cache(None)
def foto(clave, sigma=0.0, k=1.0):
    """Imagen RGB float32 0..1 (flow/bg/x → "bg/x"); sigma = desenfoque en px de la fuente; k = exposición."""
    a = cv2.imread(_ruta_img(clave), cv2.IMREAD_COLOR)
    if a is None:
        raise SystemExit(f"falta la imagen {_ruta_img(clave)}")
    a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    if sigma:
        a = cv2.GaussianBlur(a, (0, 0), sigma)
    if k != 1.0:
        a = a * k
    return np.ascontiguousarray(a)


@lru_cache(None)
def pil(clave, caja=None, sigma=0):
    im = Image.open(_ruta_img(clave)).convert("RGB")
    if caja:
        im = im.crop(caja)
    if sigma:
        from PIL import ImageFilter
        im = im.filter(ImageFilter.GaussianBlur(sigma))
    return im


CACHE = os.path.join(PREV, "ui_cache")


def cara(quien):
    """Recortes de cara para avatares y miniaturas (flow/bg, medios/ y un cuadro del clip del Presente)."""
    cajas = {
        "ramon": ("bg/mon_1", (650, 105, 930, 385)),
        "ramon_taller": ("bg/mon_5", (665, 95, 945, 375)),
        "ramon_noche": ("medios/scene-050", (715, 105, 985, 375)),
        "ramon_cama": ("bg/mon_4", (770, 150, 1030, 410)),
        "carmen": ("medios/scene-045", (555, 175, 785, 405)),
        "daniel": ("bg/telefono_puerta", (900, 0, 1260, 360)),
    }
    if quien == "presente_daniel":
        os.makedirs(CACHE, exist_ok=True)
        p = os.path.join(CACHE, "cara_presente_daniel.png")
        if not os.path.exists(p):
            subprocess.run([FF, "-v", "error", "-y", "-ss", "1.0", "-i", os.path.join(MEDIOS, "scene-004.mp4"),
                            "-frames:v", "1", p], check=True)
        return Image.open(p).convert("RGB").crop((430, 60, 830, 460))
    c, caja = cajas[quien]
    return pil(c, caja)


# ───────────────────────────── cámara y composición ─────────────────────────────
def kb(a, x, z0=1.0, z1=1.08, c0=(.5, .5), c1=None):
    """Ken Burns: devuelve el cuadro 1920x1080 y la matriz afín fuente → pantalla."""
    ih, iw = a.shape[:2]
    c1 = c1 or c0
    z = lerp(z0, z1, x)
    s = max(W / iw, H / ih) * z
    cx, cy = lerp(c0[0], c1[0], x) * iw, lerp(c0[1], c1[1], x) * ih
    hw, hh = W / (2 * s), H / (2 * s)
    cx, cy = cl(cx, hw, iw - hw), cl(cy, hh, ih - hh)
    M = np.float32([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy]])
    return cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT), M


def mapa(M, pts):
    p = np.float32(pts)
    return p @ M[:, :2].T + M[:, 2]


def _caja(q, pad=0):
    x0 = max(0, int(math.floor(q[:, 0].min())) - pad)
    y0 = max(0, int(math.floor(q[:, 1].min())) - pad)
    x1 = min(W, int(math.ceil(q[:, 0].max())) + pad)
    y1 = min(H, int(math.ceil(q[:, 1].max())) + pad)
    return x0, y0, x1, y1


def pegar(fr, c, x, y, op=1.0):
    """Capa premultiplicada en (x, y)."""
    if op <= 0.003:
        return
    h, w = c.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    cc = c[y0 - y:y1 - y, x0 - x:x1 - x]
    a = cc[..., 3:4] * op
    fr[y0:y1, x0:x1] = fr[y0:y1, x0:x1] * (1 - a) + cc[..., :3] * op


def pegar_quad(fr, c, quad, op=1.0, vidrio=0.0, aditivo=False):
    """Capa premultiplicada deformada al cuadrilátero (TL, TR, BR, BL). vidrio = desenfoque del fondo bajo la capa."""
    if op <= 0.003:
        return
    q = np.float32(quad)
    h, w = c.shape[:2]
    qw = max(np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[2] - q[3]), 2)
    if w > qw * 1.3:
        k = qw * 1.15 / w
        c = cv2.resize(c, (max(2, int(w * k)), max(2, int(h * k))), interpolation=cv2.INTER_AREA)
        h, w = c.shape[:2]
    x0, y0, x1, y1 = _caja(q, 2)
    if x1 <= x0 or y1 <= y0:
        return
    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]), q - np.float32([x0, y0]))
    o = cv2.warpPerspective(c, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                            borderValue=(0, 0, 0, 0))
    reg = fr[y0:y1, x0:x1]
    if vidrio:
        forma = np.clip(o[..., 3:4] * 3.0, 0, 1) * op
        bl = cv2.GaussianBlur(reg, (0, 0), vidrio)
        reg = reg * (1 - forma) + bl * forma
    if aditivo:
        fr[y0:y1, x0:x1] = reg + o[..., :3] * op
    else:
        a = o[..., 3:4] * op
        fr[y0:y1, x0:x1] = reg * (1 - a) + o[..., :3] * op


def _mascara(q, blur, pad):
    x0, y0, x1, y1 = _caja(q, pad)
    if x1 <= x0 or y1 <= y0:
        return None
    m = np.zeros((y1 - y0, x1 - x0), np.float32)
    cv2.fillConvexPoly(m, np.int32(np.round((q - [x0, y0]) * 4)), 1.0, lineType=cv2.LINE_AA, shift=2)
    if blur:
        m = cv2.GaussianBlur(m, (0, 0), blur)
    return m[..., None], (x0, y0, x1, y1)


def sombra(fr, quad, dx=0, dy=24, blur=34, fuerza=.55, crece=1.0):
    q = np.float32(quad)
    if crece != 1.0:
        c = q.mean(0)
        q = c + (q - c) * crece
    q = q + [dx, dy]
    r = _mascara(q, blur, int(blur * 3))
    if r is None:
        return
    m, (x0, y0, x1, y1) = r
    fr[y0:y1, x0:x1] *= (1 - fuerza * m)


def luz(fr, quad, col, blur=70, fuerza=.3, crece=1.15):
    """Resplandor aditivo alrededor de una pantalla."""
    q = np.float32(quad)
    c = q.mean(0)
    q = c + (q - c) * crece
    r = _mascara(q, blur, int(blur * 3))
    if r is None:
        return
    m, (x0, y0, x1, y1) = r
    fr[y0:y1, x0:x1] += m * np.float32(col) * fuerza


def poli(fr, pts, col, op=1.0, col2=None):
    """Polígono relleno con antialias; col2 = degradado vertical."""
    q = np.float32(pts)
    r = _mascara(q, 0, 1)
    if r is None:
        return
    m, (x0, y0, x1, y1) = r
    c = np.float32(col)
    if col2 is not None:
        yy = np.linspace(0, 1, y1 - y0, dtype=np.float32)[:, None, None]
        c = c * (1 - yy) + np.float32(col2) * yy
    fr[y0:y1, x0:x1] = fr[y0:y1, x0:x1] * (1 - m * op) + c * m * op


def _R(yaw, pitch, roll):
    y, p, r = map(math.radians, (yaw, pitch, roll))
    Ry = np.array([[math.cos(y), 0, math.sin(y)], [0, 1, 0], [-math.sin(y), 0, math.cos(y)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(p), -math.sin(p)], [0, math.sin(p), math.cos(p)]])
    Rz = np.array([[math.cos(r), -math.sin(r), 0], [math.sin(r), math.cos(r), 0], [0, 0, 1]])
    return Rz @ Rx @ Ry


def quad3d(cx, cy, w, h, yaw=0.0, pitch=0.0, roll=0.0, f=2400.0):
    """Rectángulo w×h centrado en (cx, cy) girado en 3D y proyectado (pitch > 0 = la parte de arriba se aleja)."""
    pts = np.array([[-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], [w / 2, h / 2, 0], [-w / 2, h / 2, 0]], float)
    p = pts @ _R(yaw, -pitch, roll).T
    z = p[:, 2] + f
    return np.float32(np.stack([cx + p[:, 0] * f / z, cy + p[:, 1] * f / z], 1))


# ───────────────────────────── película ─────────────────────────────
_GR = None
_VIG = None


def pelicula(fr, f, grano=.026, vig=.34):
    global _GR, _VIG
    if _GR is None:
        rng = np.random.default_rng(11)
        _GR = [rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32) for _ in range(9)]
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
        _VIG = np.clip((r - .32) / .68, 0, 1) ** 1.7
    if vig:
        fr *= (1 - vig * _VIG)[..., None]
    if grano:
        g = cv2.resize(_GR[(f * 4) % 9], (W, H), interpolation=cv2.INTER_LINEAR)
        if (f // 9) % 2:
            g = g[::-1]
        fr += g[..., None] * grano
    np.clip(fr, 0, 1, out=fr)
    return fr


# ───────────────────────────── audio ─────────────────────────────
def _sos(tipo, f, orden=4):
    return butter(orden, f, btype=tipo, fs=SR, output="sos")


def bp(x, lo, hi, orden=4):
    return sosfilt(_sos("band", [lo, hi], orden), x, axis=0).astype(np.float32)


def lp(x, f, orden=4):
    return sosfilt(_sos("low", f, orden), x, axis=0).astype(np.float32)


def hp(x, f, orden=4):
    return sosfilt(_sos("high", f, orden), x, axis=0).astype(np.float32)


@lru_cache(None)
def _ir(rt, largo, seed=3):
    rng = np.random.default_rng(seed)
    n = int(largo * SR)
    t = np.arange(n) / SR
    x = rng.normal(0, 1, (n, 2)) * np.exp(-6.9 * t / rt)[:, None]
    x = lp(x, 5200, 2)
    x[:int(.022 * SR)] = 0
    return (x / np.sqrt((x ** 2).sum(0, keepdims=True))).astype(np.float32)


def reverb(a, rt=1.6, wet=.2, largo=None):
    ir = _ir(rt, largo or min(3.0, rt * 1.4))
    y = np.stack([fftconvolve(a[:, i], ir[:, i])[:len(a)] for i in range(2)], 1).astype(np.float32)
    return a * (1 - wet) + y * wet * 1.6


def st(x, pan=0.0):
    x = np.asarray(x, np.float32)
    return np.stack([x * min(1, 1 - pan), x * min(1, 1 + pan)], 1)


def _t(d):
    return np.arange(int(d * SR), dtype=np.float32) / SR


def s_tap(g=.16):
    t = _t(.06)
    rng = np.random.default_rng(5)
    x = np.sin(2 * np.pi * 1900 * t) * np.exp(-t / .007) * .5 + hp(rng.normal(0, 1, len(t)), 2500) * np.exp(-t / .003) * .5
    return st(x * g)


def s_click(g=.2):
    t = _t(.08)
    rng = np.random.default_rng(6)
    x = bp(rng.normal(0, 1, len(t)), 900, 5000) * np.exp(-t / .004) + np.sin(2 * np.pi * 420 * t) * np.exp(-t / .012) * .6
    return st(x * g)


def s_noti(g=.13):
    t = _t(1.2)
    x = np.zeros_like(t)
    for f0, t0 in ((1046.5, 0.0), (1567.98, .11)):
        tt = np.clip(t - t0, 0, None)
        on = (t >= t0).astype(np.float32)
        x += on * (np.sin(2 * np.pi * f0 * tt) + .25 * np.sin(2 * np.pi * 2 * f0 * tt) * np.exp(-tt / .08)) * np.exp(-tt / .32)
    x *= np.clip(t / .004, 0, 1)
    return reverb(st(x * g), .6, .18)


def s_vibra(pulsos=2, largo=.38, hueco=.16, g=.16):
    d = pulsos * (largo + hueco)
    t = _t(d)
    env = np.zeros_like(t)
    for i in range(pulsos):
        a = i * (largo + hueco)
        env += np.clip((t - a) / .015, 0, 1) * np.clip((a + largo - t) / .03, 0, 1)
    rng = np.random.default_rng(8)
    buzz = np.sign(np.sin(2 * np.pi * 152 * t)) * .5 + np.sin(2 * np.pi * 152 * t) + rng.normal(0, .3, len(t))
    x = lp(buzz, 650) + bp(buzz, 1800, 3200) * .15
    return st(x * env * g)


def s_swoosh(d=.42, g=.05, sube=True):
    t = _t(d)
    rng = np.random.default_rng(9)
    n = rng.normal(0, 1, len(t))
    x = bp(n, 700, 5500) * np.sin(np.pi * t / d) ** 2
    return st(x * g, .25 if sube else -.25)


def s_tick(tono=1.0, g=.06):
    t = _t(.05)
    rng = np.random.default_rng(int(tono * 100))
    x = hp(rng.normal(0, 1, len(t)), 2200) * np.exp(-t / .0018) + np.sin(2 * np.pi * 2600 * tono * t) * np.exp(-t / .004) * .7
    return st(x * g)


def s_ring(d, g=.11):
    """Tono de llamada original (marimba suave, motivo de 4 notas cada 2 s)."""
    t = _t(d)
    x = np.zeros_like(t)
    notas = [(659.25, 0), (987.77, .17), (880.0, .34), (1318.5, .51), (987.77, .68)]
    for c in np.arange(0, d, 2.0):
        for f0, dt in notas:
            t0 = c + dt
            tt = t - t0
            m = tt >= 0
            tt = np.where(m, tt, 0)
            x += m * (np.sin(2 * np.pi * f0 * tt) * np.exp(-tt / .28) + .3 * np.sin(2 * np.pi * 4 * f0 * tt) * np.exp(-tt / .03))
    return reverb(st(x * g), .5, .15)


def s_conecta(g=.1):
    t = _t(.5)
    x = np.zeros_like(t)
    for f0, t0 in ((659.25, 0), (880, .12)):
        tt = np.clip(t - t0, 0, None)
        x += (t >= t0) * np.sin(2 * np.pi * f0 * tt) * np.exp(-tt / .12)
    return st(x * g)


def s_grave(d, g=.09):
    t = _t(d)
    env = np.clip(t / (d * .45), 0, 1) ** 2 * np.clip((d - t) / (d * .4), 0, 1)
    x = (np.sin(2 * np.pi * 55 * t) + .5 * np.sin(2 * np.pi * 82.4 * t) + .25 * np.sin(2 * np.pi * 110 * t)) * env
    return reverb(st(x * g), 2.2, .3)


def s_ruido(d, lo, hi, g, seed=1, am=0.0):
    rng = np.random.default_rng(seed)
    n = int(d * SR)
    x = bp(rng.normal(0, 1, (n, 2)), lo, hi, 2)
    if am:
        e = lp(np.abs(rng.normal(0, 1, (n, 1))), am, 2)
        x = x * (e / (e.mean() + 1e-6))
    x /= (np.sqrt((x ** 2).mean()) + 1e-6)
    return (x * g).astype(np.float32)


def s_murmullo(d, g=.02, seed=4, voces=8):
    rng = np.random.default_rng(seed)
    n = int(d * SR)
    x = np.zeros((n, 2), np.float32)
    for v in range(voces):
        lo = 260 + rng.uniform(0, 160)
        b = bp(rng.normal(0, 1, n), lo, lo * 5, 2)
        e = lp(np.abs(rng.normal(0, 1, n)), 3.5 + rng.uniform(0, 3), 2)
        e = np.clip(e - e.mean() * .6, 0, None)
        p = rng.uniform(-.7, .7)
        x += st(b * e, p)
    x /= (np.sqrt((x ** 2).mean()) + 1e-6)
    return reverb(x * g, 1.2, .3)


def s_aplauso(d, g=.16, seed=2, sube=.5, baja=1.4):
    rng = np.random.default_rng(seed)
    n = int(d * SR)
    out = np.zeros((n, 2), np.float32)
    kern = []
    for i in range(20):
        L = int(rng.uniform(.006, .014) * SR)
        tt = np.arange(L) / SR
        kern.append(bp(rng.normal(0, 1, L), rng.uniform(700, 1300), rng.uniform(2800, 5200), 2) * np.exp(-tt / rng.uniform(.002, .005)))
    cant = int(d * 420)
    for _ in range(cant):
        t0 = rng.uniform(0, d)
        env = min(1, t0 / sube) * min(1, (d - t0) / baja)
        if rng.uniform() > env:
            continue
        k = kern[rng.integers(0, 20)]
        i = int(t0 * SR)
        m = min(len(k), n - i)
        p = rng.uniform(-.8, .8)
        a = rng.uniform(.3, 1)
        out[i:i + m, 0] += k[:m] * a * (1 - max(0, p))
        out[i:i + m, 1] += k[:m] * a * (1 + min(0, p))
    out /= (np.abs(out).max() + 1e-6)
    return reverb(out * g, 1.8, .35)


class Pista:
    def __init__(s, d):
        s.n = int(round(d * SR))
        s.a = np.zeros((s.n, 2), np.float32)

    def add(s, x, t0, g=1.0):
        x = st(x) if x.ndim == 1 else x
        i = int(round(t0 * SR))
        if i < 0:
            x, i = x[-i:], 0
        m = min(len(x), s.n - i)
        if m > 0:
            s.a[i:i + m] += x[:m] * g

    def voz(s, clave, t0, g=1.0, sala=0.0, tele=False):
        a = voz_lista(clave)
        if sala:
            a = reverb(np.concatenate([a, np.zeros((int(1.5 * SR), 2), np.float32)]), 1.7, sala)
        if tele:
            a = reverb(bp(a, 220, 5200, 2) * .8, .45, .25)
        s.add(a, t0, g)
        return t0 + dur(clave)

    def final(s):
        a = s.a
        pk = float(np.abs(a).max())
        if pk > .97:
            a = a * (.97 / pk)
        k = int(.012 * SR)   # sin clics en las puntas
        a[:k] *= np.linspace(0, 1, k)[:, None]
        a[-k:] *= np.linspace(1, 0, k)[:, None]
        return a


# ───────────────────────────── el teléfono (vidrio sin marco, en 3D) ─────────────────────────────
SW, SH = 500, 1084          # pantalla
TM, TP = 12, 6              # bisel y margen para los botones
_TB = {}


def _tel_base():
    if _TB:
        return _TB["b"], _TB["m"], _TB["i"]
    k = 4
    Wt, Ht = SW + 2 * (TM + TP), SH + 2 * (TM + TP)
    im = Image.new("RGBA", (Wt * k, Ht * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = TP * k
    for y0, y1 in ((250, 318), (338, 406)):
        d.rounded_rectangle([P - 4 * k, y0 * k, P + 6 * k, y1 * k], radius=2 * k, fill=(92, 90, 88, 255))
    d.rounded_rectangle([Wt * k - P - 6 * k, 300 * k, Wt * k - P + 4 * k, 410 * k], radius=2 * k, fill=(92, 90, 88, 255))
    R = 64
    d.rounded_rectangle([P, P, Wt * k - P, Ht * k - P], radius=R * k, fill=(168, 164, 158, 255))
    d.rounded_rectangle([P + 3 * k, P + 3 * k, Wt * k - P - 3 * k, Ht * k - P - 3 * k], radius=(R - 3) * k, fill=(10, 10, 12, 255))
    b = np.asarray(im.resize((Wt, Ht), Image.LANCZOS), np.float32) / 255
    b[..., :3] *= b[..., 3:4]
    m = Image.new("L", (SW * k, SH * k), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, SW * k - 1, SH * k - 1], radius=(R - TM) * k, fill=255)
    m = np.asarray(m.resize((SW, SH), Image.LANCZOS), np.float32)[..., None] / 255
    isla = Image.new("L", (SW * k, SH * k), 0)
    ImageDraw.Draw(isla).rounded_rectangle([(SW / 2 - 62) * k, 14 * k, (SW / 2 + 62) * k, 48 * k], radius=17 * k, fill=255)
    isla = np.asarray(isla.resize((SW, SH), Image.LANCZOS), np.float32)[..., None] / 255
    _TB.update(b=b, m=m, i=isla)
    return b, m, isla


@lru_cache(64)
def _reflejo(pos):
    yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
    u = xx / SW * .55 + yy / SH * .45
    c = .15 + pos * .6
    g = np.exp(-((u - c) / .07) ** 2) * .55 + np.exp(-((u - c - .16) / .03) ** 2) * .25 + (1 - yy / SH) * .12
    return g[..., None].astype(np.float32)


def tel_capa(pant, brillo=1.0, reflejo=.35, ref_k=.10):
    b, m, isla = _tel_base()
    c = b.copy()
    o = TM + TP
    scr = pant * brillo
    scr = scr * (1 - isla) + .012 * isla
    scr = np.clip(scr + _reflejo(round(cl(reflejo), 2)) * ref_k, 0, 1)
    reg = c[o:o + SH, o:o + SW]
    reg[..., :3] = reg[..., :3] * (1 - m) + scr * m
    return c


def poner_tel(fr, pant, cx, cy, alto, yaw=0.0, pitch=0.0, roll=0.0, brillo=1.0, reflejo=None,
              sombra_k=(18, 34, 38, .55), resplandor=0.0):
    c = tel_capa(pant, brillo, .35 + yaw * .025 + roll * .01 if reflejo is None else reflejo)
    h, w = c.shape[:2]
    k = alto / h
    q = quad3d(cx, cy, w * k, h * k, yaw, pitch, roll)
    if sombra_k:
        sombra(fr, q, *sombra_k)
    if resplandor:
        col = pant[::40, ::40].reshape(-1, 3).mean(0) * .6 + .4 * np.float32([1, .85, .62])
        luz(fr, q, col, blur=90, fuerza=resplandor * brillo, crece=1.25)
    pegar_quad(fr, c, q)
    return q


def en_mano(t, t_in=0.0, t_out=None, cx=1180, cy=700, alto=1320, seed=0.0, temblor=1.0, yaw=-7, pitch=4, roll=-3):
    """Teléfono sostenido (la mano queda fuera de cuadro): sube desde abajo, se mece, y baja al salir."""
    sube = eo(seg(t, t_in, t_in + .75))
    baja = ss(seg(t, t_out, t_out + .9)) if t_out is not None else 0.0
    dy = (1 - sube) * 900 + baja * 1000
    v = vaiven(t, seed) * temblor
    v2 = vaiven(t * 1.1, seed + 3.3) * temblor
    return dict(cx=cx + v * 7, cy=cy + dy + v2 * 6, alto=alto, yaw=yaw + v * .9, pitch=pitch + v2 * .7,
                roll=roll + v * .6 - (1 - sube) * 6)


# ───────────────────────────── pantallas del teléfono ─────────────────────────────
@lru_cache(None)
def fondo_bloqueo(clave="esc/carretera", k=.5):
    im = pil(clave)
    s = max(SW / im.size[0], SH / im.size[1])
    im = im.resize((int(im.size[0] * s) + 1, int(im.size[1] * s) + 1), Image.LANCZOS)
    ox = (im.size[0] - SW) // 2
    im = im.crop((ox, 0, ox + SW, SH))
    a = np.asarray(im, np.float32) / 255
    a = cv2.GaussianBlur(a, (0, 0), 26) * k
    return Image.fromarray(np.uint8(np.clip(a, 0, 1) * 255))


def icono_app(lz, x, y, s=40, a=1.0):
    lz.rect(x, y, x + s, y + s, r=s * .24, fill=rgba((30, 25, 21), a))
    lz.logo(x + s / 2, y + s / 2, s * .3, a=a, txt=False)


def bloqueo(hora, fecha, wall="esc/carretera", k=.5):
    lz = Lz(SW, SH, (0, 0, 0))
    lz.im.paste(fondo_bloqueo(wall, k).resize((SW * lz.k, SH * lz.k)), (0, 0))
    lz.text(SW / 2, 118, fecha, "sb", 22, rgba(CREMA, .9), anchor="ms")
    lz.text(SW / 2, 238, hora, "bahn_Light", 118, rgba(CREMA, .96), anchor="ms")
    lz.circ(84, 1010, 26, fill=(255, 255, 255, 40))
    lz.circ(SW - 84, 1010, 26, fill=(255, 255, 255, 40))
    lz.rect(SW / 2 - 70, 1062, SW / 2 + 70, 1067, r=3, fill=(255, 255, 255, 200))
    # barra de estado
    lz.text(SW - 40, 40, "", "sb", 16, CREMA, anchor="rs")
    for i in range(4):
        lz.rect(SW - 118 + i * 9, 34 - i * 4, SW - 112 + i * 9, 40, r=1, fill=(244, 232, 210, 230))
    lz.rect(SW - 72, 26, SW - 40, 42, r=4, outline=(244, 232, 210, 200), width=1.5)
    lz.rect(SW - 69, 29, SW - 50, 39, r=2, fill=(244, 232, 210, 230))
    return lz


def noti_alto(lz, w, titulo, lineas, tam=21):
    h = 22 + 38 + 8 + 30 + (len(lz.wrap(titulo, "sb", tam + 1, w - 44)) - 1) * (tam + 1) * 1.3
    for l in lineas:
        h += len(lz.wrap(l, "r", tam, w - 44)) * tam * 1.3 + 4
    return h + 16


def noti(lz, x, y, w, titulo, lineas, hora="ahora", a=1.0, tam=21, app="PRESENTE", resalta=None):
    """Tarjeta de notificación de PRESENTE (vidrio cálido)."""
    h = noti_alto(lz, w, titulo, lineas, tam)
    lz.rect(x, y, x + w, y + h, r=28, fill=rgba((52, 44, 38), .82 * a))
    lz.rect(x + 1, y + 1, x + w - 1, y + 3, r=2, fill=rgba((255, 240, 220), .10 * a))
    icono_app(lz, x + 20, y + 20, 38, a)
    lz.text(x + 70, y + 46, app, "sb", 15, rgba(CREMA2, a), anchor="ls", track=2.4)
    lz.text(x + w - 22, y + 46, hora, "r", 15, rgba(GRIS, a), anchor="rs")
    yy = y + 92
    for i, tl in enumerate(lz.wrap(titulo, "sb", tam + 1, w - 44)):
        if i:
            yy += (tam + 1) * 1.3
        lz.text(x + 22, yy, tl, "sb", tam + 1, rgba(CREMA, a), anchor="ls")
    yy += tam * 1.45
    for i, l in enumerate(lineas):
        col = AMBAR_C if resalta == i else CREMA
        for ll in lz.wrap(l, "r", tam, w - 44):
            lz.text(x + 22, yy, ll, "r", tam, rgba(col, .88 * a), anchor="ls")
            yy += tam * 1.3
        yy += 4
    return h


def toque(lz, x, y, p, a=1.0):
    """Huella de un dedo (círculo suave que se aprieta)."""
    r = 30 - 6 * p
    lz.circ(x, y, r + 10, fill=rgba((255, 250, 240), .10 * a))
    lz.circ(x, y, r, fill=rgba((255, 250, 240), .22 * a))


# ───────────────────────────── la laptop (en 3D) ─────────────────────────────
LW, LH = 1600, 1000      # pantalla de la app en la laptop


def _proy(P, f=1500.0):
    P = np.asarray(P, float)
    return np.float32(np.stack([W / 2 + f * P[:, 0] / P[:, 2], H / 2 + f * P[:, 1] / P[:, 2]], 1))


def poner_laptop(fr, pant, hx=0.0, hy=330.0, hz=1580.0, yaw=-12.0, tilt=14.0, brillo=1.0):
    """Laptop plateada: pantalla (pant = float RGB LH×LW) inclinada `tilt` grados hacia atrás, teclado hacia la cámara."""
    Ws, Hs, b = 1500.0, 937.0, 30.0
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    ct, st_ = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))

    def P(x, h=0.0, z=0.0):   # x a lo ancho, h hacia arriba en la tapa, z hacia la cámara sobre la base
        lx, ly, lz_ = x, -h * ct, h * st_ - z
        return [hx + lx * cy + lz_ * sy, hy + ly, hz - lx * sy + lz_ * cy]

    def Q(x0, x1, h0=None, h1=None, z0=None, z1=None):
        if h0 is not None:
            return _proy([P(x0, h1), P(x1, h1), P(x1, h0), P(x0, h0)])
        return _proy([P(x0, 0, z1), P(x1, 0, z1), P(x1, 0, z0), P(x0, 0, z0)])

    hw = Ws / 2 + b
    # base (teclado) hacia la cámara
    poli(fr, Q(-hw, hw, z0=-6, z1=1000), (.42, .42, .44), 1.0, (.20, .20, .22))
    poli(fr, Q(-hw * .9, hw * .9, z0=60, z1=430), (.07, .07, .075))
    for fila in range(5):
        z0 = 72 + fila * 70
        for col in range(14):
            x0 = -hw * .88 + col * (hw * 1.76 / 14)
            poli(fr, Q(x0 + 5, x0 + hw * 1.76 / 14 - 5, z0=z0 + 5, z1=z0 + 62), (.17, .17, .18))
    poli(fr, Q(-260, 260, z0=480, z1=820), (.36, .36, .38), 1.0, (.28, .28, .30))
    # tapa: canto de aluminio, bisel negro, pantalla
    poli(fr, Q(-hw - 4, hw + 4, h0=-4, h1=Hs + 2 * b + 4), (.55, .55, .57))
    qb = Q(-hw, hw, h0=0, h1=Hs + 2 * b)
    poli(fr, qb, (.03, .03, .035))
    qs = Q(-Ws / 2, Ws / 2, h0=b, h1=b + Hs)
    col = pant[::50, ::50].reshape(-1, 3).mean(0) * .5 + .5 * np.float32([1, .86, .66])
    luz(fr, Q(-hw, hw, z0=0, z1=520), col, blur=60, fuerza=.10 * brillo, crece=1.0)
    capa = np.dstack([np.clip(pant * brillo, 0, 1), np.ones(pant.shape[:2] + (1,), np.float32)])
    pegar_quad(fr, capa, qs)
    # reflejo del vidrio
    g = np.zeros((60, 100, 4), np.float32)
    g[..., :3] = np.linspace(0, 1, 100, dtype=np.float32)[None, :, None] ** 3 * .05
    g[..., 3] = 0
    pegar_quad(fr, g, qs, aditivo=True)
    return qs


def app_fondo(w, h, k=1.0):
    return _app_fondo(int(w), int(h), round(k, 2))


@lru_cache(None)
def _app_fondo(w, h, k):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w * .5) / w) ** 2 + ((yy - h * .1) / h) ** 2 * 1.6)
    g = np.clip(1 - r * 1.25, 0, 1) ** 2
    base = np.float32(TINTA) / 255
    calido = np.float32((70, 50, 32)) / 255
    a = (base[None, None] * (1 - g[..., None]) + calido[None, None] * g[..., None]) * k
    return Image.fromarray(np.uint8(np.clip(a, 0, 1) * 255))


def app_lz(w, h, k=1.0):
    lz = Lz(w, h, TINTA)
    lz.im.paste(app_fondo(w, h, k).resize((w * lz.k, h * lz.k)), (0, 0))
    return lz


def barra_app(lz, derecha="", centro=""):
    lz.logo(70, 64, 15, txt=True, tam=17)
    if centro:
        lz.text(lz.w / 2, 70, centro, "sl", 20, rgba(GRIS), anchor="ms", track=1)
    if derecha:
        lz.text(lz.w - 64, 70, derecha, "r", 19, rgba(GRIS), anchor="rs")
    lz.rect(56, 104, lz.w - 56, 105, fill=rgba(CREMA, .08))


def cursor(lz, x, y, aprieta=0.0, a=1.0):
    s = 1.0 - .12 * aprieta
    pts = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (27, 24)]
    pts = [(x + px * s * 1.15, y + py * s * 1.15) for px, py in pts]
    lz.poly([(px + 2, py + 3) for px, py in pts], fill=(0, 0, 0, int(90 * a)))
    lz.poly(pts, fill=rgba((250, 248, 244), a))
    lz.line(pts + [pts[0]], fill=rgba((20, 20, 20), a), width=1.4)


def interruptor(lz, x, y, on, a=1.0, w=96, h=52):
    """on = 0..1 (animable)."""
    c = tuple(int(lerp(GRIS_O[i], AMBAR[i], on)) for i in range(3))
    lz.rect(x, y, x + w, y + h, r=h / 2, fill=rgba(c, a))
    kx = lerp(x + h / 2, x + w - h / 2, eio(on))
    lz.circ(kx + 1, y + h / 2 + 2, h / 2 - 5, fill=(0, 0, 0, int(60 * a)))
    lz.circ(kx, y + h / 2, h / 2 - 5, fill=rgba((252, 246, 236), a))


def ondas(lz, x, y, w, h, t, activo=1.0, n=28, col=AMBAR, a=1.0, seed=0):
    """Barras de voz que escuchan."""
    paso = w / n
    for i in range(n):
        v = (math.sin(t * 7.1 + i * .9 + seed) * .5 + .5) * (math.sin(t * 3.3 + i * .37 + seed * 2) * .5 + .5)
        v = .08 + .92 * v * activo * (math.sin(math.pi * (i + .5) / n) ** .6)
        bh = max(4, h * v)
        cx = x + i * paso + paso / 2
        lz.rect(cx - paso * .28, y - bh / 2, cx + paso * .28, y + bh / 2, r=paso * .28, fill=rgba(col, a))


def escribe(txt, p):
    """Texto que se va escribiendo (p 0..1)."""
    n = int(round(len(txt) * cl(p)))
    return txt[:n]


# ───────────────────────────── salida ─────────────────────────────
class Pieza:
    def __init__(s, uid, d, fps=FPS):
        s.uid, s.d, s.fps = uid, d, fps
        s.n = int(round(d * fps))
        s.audio = Pista(d)
        s.grano, s.vig = .026, .34


def escribir(P, render, salida):
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    import soundfile as sf
    wav = os.path.join(CACHE, f"_{P.uid}.wav")
    sf.write(wav, P.audio.final(), SR, subtype="PCM_16")
    tmp = salida + ".tmp.mp4"
    cmd = [FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(P.fps), "-i", "-",
           "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
           "-t", f"{P.n / P.fps:.4f}", "-movflags", "+faststart", tmp]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(P.n):
        fr = render(f / P.fps, f)
        fr = pelicula(fr, f, P.grano, P.vig)
        pr.stdin.write((fr * 255 + .5).astype(np.uint8).tobytes())
    pr.stdin.close()
    if pr.wait() != 0:
        raise SystemExit(f"ffmpeg falló en {P.uid}")
    os.replace(tmp, salida)
    os.remove(wav)


# ═════════════════════════════════════ PIEZAS ═════════════════════════════════════
PIEZAS = {}


def pieza(f):
    PIEZAS[f.__name__[2:]] = f
    return f


def zumbido(t, tramos, amp=2.4):
    """Temblor del teléfono mientras vibra."""
    for a, b in tramos:
        if a <= t <= b:
            return math.sin(t * 940) * amp, math.cos(t * 770) * amp * .7
    return 0.0, 0.0


VIBRA2 = [(0, .38), (.54, .92)]


def _tramos(t0, base=VIBRA2):
    return [(t0 + a, t0 + b) for a, b in base]


# ─────────────── notif_1: la notificación que Daniel desliza sin leer ───────────────
@pieza
def f_notif_1(P):
    fondo = foto("bg/mesa_junta", 11, .74)
    A = P.audio
    A.add(s_ruido(P.d, 70, 700, .006, seed=21), 0)
    A.add(s_vibra(2), .45)
    A.add(s_swoosh(.4, .05), 5.2)
    tv = _tramos(.45)

    def r(t, f):
        fr, _ = kb(fondo, t / P.d, 1.12, 1.2, (.42, .4), (.46, .43))
        lz = bloqueo("22:47", "domingo, 26 de julio", "esc/carretera", .45)
        enc, sal = eo(seg(t, .6, 1.05)), eio(seg(t, 5.15, 5.6))
        y = lerp(-280, 300, enc)
        if sal < 1:
            noti(lz, 20 + sal * 560, y, SW - 40, "Llamada con Papá completada",
                 ["Hoy 11:05 · 18 min · Ánimo de Papá 92 %", "Resumen: le contaste del reloj del abuelo. Está contento."],
                 "ahora", a=1 - sal * .5)
        if 4.75 < t < 5.75:
            toque(lz, 150 + sal * 330, y + 150, seg(t, 4.75, 4.95), ven(t, 4.75, 5.75, .12, .25))
        br = ss(seg(t, .45, .75)) * (1 - .72 * ss(seg(t, 6.2, 6.85)))
        jx, jy = zumbido(t, tv)
        poner_tel(fr, lz.rgb(), 1010 + jx + t * 4, 585 + jy, lerp(1150, 1200, t / P.d), yaw=-6, pitch=38, roll=-13,
                  brillo=br, sombra_k=(10, 18, 22, .62), resplandor=.10)
        return fr
    return r


# ─────────────── titulo ───────────────
@pieza
def f_titulo(P):
    fondo = foto("esc/taller", 5, .15)
    rng = np.random.default_rng(3)
    motas = rng.uniform(0, 1, (46, 4))
    A = P.audio
    for i in range(9):
        A.add(s_tick(1.0 if i % 2 == 0 else .82, .03), .5 + i)
    A.add(s_grave(5.2), 3.9)

    def r(t, f):
        fr, _ = kb(fondo, t / P.d, 1.04, 1.12, (.5, .5), (.53, .47))
        fr *= ss(seg(t, 0, 1.2)) * (1 - ss(seg(t, 8.25, 9.0)))
        for x, y, v, s in motas:
            px = int((x * W + t * (6 + 14 * v)) % W)
            py = int((y * H - t * (4 + 9 * s)) % H)
            a = .025 + .05 * v
            cv2.circle(fr, (px, py), 1 + int(2 * s), (a * .9, a * .7, a * .45), -1, lineType=cv2.LINE_AA)
        lz = Lz(1700, 260)
        a1 = ven(t, 1.0, 3.8, .8, .7)
        if a1 > 0:
            lz.text(850, 140, "LogIA presenta", "sl", 34, rgba(CREMA2, a1), anchor="ms", track=12)
        a2 = ven(t, 4.3, 8.75, 1.3, .6)
        if a2 > 0:
            lz.text(850, 150, "LLAMADA DE DOMINGO", "l", 92, rgba(CREMA, a2), anchor="ms",
                    track=lerp(22, 33, seg(t, 4.3, 8.75)))
            w = 560 * eo(seg(t, 4.9, 6.6))
            lz.rect(850 - w / 2, 196, 850 + w / 2, 198, fill=rgba(AMBAR, a2 * .9))
        pegar(fr, lz.out(), W / 2 - 850, H / 2 - 150)
        return fr
    return r


# ─────────────── keynote (pantalla gigante de key_sala) ───────────────
QSALA = [(470, 50), (918, 49), (911, 257), (477, 256)]
SLW, SLH = 1600, 730


@lru_cache(None)
def _fondo_diapo():
    return app_fondo(SLW, SLH, 1.15)


def diapo():
    lz = Lz(SLW, SLH, TINTA, k=1)
    lz.im.paste(_fondo_diapo(), (0, 0))
    return lz


def logo_centrado(lz, cx, cy, r, prog=1.0, a=1.0, tam=None):
    tam = tam or r * 1.05
    ancho = 2 * r + .75 * r + lz.ancho("PRESENTE", "l", tam, tam * .38)
    lz.logo(cx - ancho / 2 + r, cy, r, a=1.0, prog=prog, txt=False)
    if a > 0:
        lz.text(cx - ancho / 2 + r + r * 1.75, cy, "PRESENTE", "l", tam, rgba(CREMA, a), anchor="lm", track=tam * .38)


def sala(t, x, z0, z1, c0, c1, lz_diapo, brillo=1.0):
    fr, M = kb(foto("bg/key_sala"), x, z0, z1, c0, c1)
    q = mapa(M, QSALA)
    s = np.clip(lz_diapo.rgb() * 1.04 * brillo + .035, 0, 1)
    luz(fr, q, s[::40, ::40].reshape(-1, 3).mean(0) + .1, blur=46, fuerza=.22, crece=1.06)
    pegar_quad(fr, np.dstack([s, np.ones(s.shape[:2] + (1,), np.float32)]), q)
    return fr


def aparece(lz, x, y, txt, f, tam, col, a, anchor="ms", track=0, sube=18):
    """Texto que entra subiendo y aclarándose (a = progreso 0..1)."""
    if a <= 0:
        return
    lz.text(x, y + (1 - eo(a)) * sube, txt, f, tam, rgba(col, ss(a)), anchor=anchor, track=track)


def chip(lz, x, y, w, h, txt, icono, a, t):
    if a <= 0:
        return
    dx = (1 - eo(a)) * 40
    lz.rect(x + dx, y, x + w + dx, y + h, r=h / 2, fill=rgba(PANEL, ss(a)))
    cx, cy = x + dx + h * .55, y + h / 2
    c = rgba(AMBAR, ss(a))
    if icono == "fotos":
        lz.rect(cx - 20, cy - 14, cx + 12, cy + 16, r=5, outline=c, width=3)
        lz.rect(cx - 12, cy - 22, cx + 20, cy + 8, r=5, fill=rgba(PANEL, ss(a)), outline=c, width=3)
    elif icono == "audios":
        for i in range(5):
            hh = 8 + 16 * abs(math.sin(t * 4 + i))
            lz.rect(cx - 22 + i * 10, cy - hh / 2, cx - 16 + i * 10, cy + hh / 2, r=3, fill=c)
    else:
        lz.rect(cx - 22, cy - 18, cx + 22, cy + 12, r=10, outline=c, width=3)
        lz.poly([(cx - 10, cy + 10), (cx - 16, cy + 22), (cx + 2, cy + 11)], fill=c)
    lz.text(x + dx + h * 1.15, cy, txt, "sl", 40, rgba(CREMA, ss(a)), anchor="lm")


@pieza
def f_keynote_1(P):
    L = [dur(f"keynote_1_{i}") for i in range(1, 7)]
    gaps = [.7, .7, .6, .6, .8]
    T = [1.0]
    for i in range(5):
        T.append(T[-1] + L[i] + gaps[i])
    fin = T[5] + L[5]
    assert fin < P.d - 2.0, f"keynote_1 no cabe: {fin:.1f}"
    A = P.audio
    for i in range(6):
        A.voz(f"keynote_1_{i + 1}", T[i], sala=.2)
    A.add(s_ruido(P.d, 50, 500, .007, seed=31), 0)
    A.add(s_murmullo(1.6, .018, seed=5), 0)
    A.add(s_aplauso(P.d - fin + .2, .2), fin - .15)
    c = [0, T[1] + .15, T[1] + L[1] * .55, T[2] + L[2] * .64, T[3] - .05, T[4] + L[4] * .45, T[5] - .1, P.d - 3.0, P.d]

    def lamina(t):
        lz = diapo()
        cx = SLW / 2
        if t < T[0] + 2.6:
            logo_centrado(lz, cx, SLH / 2 - 10, 72, eo(seg(t, .2, 1.6)), ss(seg(t, 1.0, 1.9)))
        elif t < T[1] + L[1] * .5:
            a = seg(t, T[0] + 2.6, T[0] + 3.3)
            aparece(lz, cx, 300, "¿Cuándo fue la última vez", "l", 80, CREMA, a)
            b = seg(t, T[0] + 3.3, T[0] + 4.0)
            if b > 0:
                w1 = lz.ancho("que le llamaste a tu ", "l", 80)
                w2 = lz.ancho("papá?", "l", 80)
                x0 = cx - (w1 + w2) / 2
                aparece(lz, x0, 405, "que le llamaste a tu ", "l", 80, CREMA, b, anchor="ls")
                aparece(lz, x0 + w1, 405, "papá?", "l", 80, AMBAR, b, anchor="ls")
            aparece(lz, cx, 530, "¿Y a tu mamá?", "sl", 54, GRIS, seg(t, T[0] + L[0] - 1.3, T[0] + L[0] - .6))
        elif t < T[2]:
            b0 = T[1]
            palabras = [("La junta.", .52), ("El tráfico.", .61), ("El vuelo.", .69)]
            fin_ = seg(t, b0 + L[1] * .82, b0 + L[1] * .9)
            xs = [cx - 470, cx, cx + 470]
            for (p, fr_), x in zip(palabras, xs):
                a = seg(t, b0 + L[1] * fr_, b0 + L[1] * fr_ + .5)
                col = tuple(int(lerp(CREMA[i], GRIS_O[i], fin_)) for i in range(3))
                aparece(lz, x, 330, p, "sl", 74, col, a)
            aparece(lz, cx, 480, "Y otra vez es lunes.", "l", 66, AMBAR, fin_ * 1.0)
        elif t < T[3]:
            b0 = T[2]
            p2 = seg(t, b0 + L[2] * .6, b0 + L[2] * .66)
            if p2 < 1:
                a0 = 1 - p2
                lz.logo(120, 90, 22, a=a0, tam=24)
                n = seg(t, b0 + L[2] * .17, b0 + L[2] * .27)
                if n > 0:
                    lz.text(430, 420, f"{int(round(3 * eo(n)))} h", "bahn_Light", 230, rgba(AMBAR, a0 * ss(n * 3)), anchor="ms")
                    lz.text(430, 500, "de entrevista", "sl", 40, rgba(CREMA, a0 * ss(n * 2)), anchor="ms")
                for i, (txt, ic, fr_) in enumerate((("tus fotos", "fotos", .33), ("tus audios", "audios", .40),
                                                    ("tus chats", "chats", .47))):
                    a = seg(t, b0 + L[2] * fr_, b0 + L[2] * fr_ + .5) * a0
                    chip(lz, 840, 190 + i * 130, 560, 96, txt, ic, a, t)
            if p2 > 0:
                aparece(lz, cx, 330, "Tu Presente llama por ti.", "l", 84, CREMA, p2)
                for k_ in range(3):
                    ph = (t * .9 + k_ / 3) % 1
                    lz.circ(cx, 175, 30 + ph * 60, outline=rgba(AMBAR, (1 - ph) * .7 * p2), width=3)
                lz.logo(cx, 175, 22, a=p2, txt=False)
                aparece(lz, cx, 460, "Con tu cara. Con tu voz.", "sl", 56, AMBAR, seg(t, b0 + L[2] * .8, b0 + L[2] * .88))
        elif t < T[4]:
            b0 = T[3]
            aparece(lz, 640, 330, "Modo discreto", "l", 72, CREMA, seg(t, b0, b0 + .5), anchor="rs")
            on = eio(seg(t, b0 + L[3] * .32, b0 + L[3] * .32 + .35))
            interruptor(lz, 740, 255, on, ss(seg(t, b0, b0 + .4)), w=230, h=118)
            aparece(lz, cx, 485, "Ellos nunca reciben un aviso.", "sl", 48, CREMA2, seg(t, b0 + .4, b0 + 1.0))
            aparece(lz, cx, 580, "Solo sienten que estás.", "l", 56, AMBAR, seg(t, b0 + L[3] * .6, b0 + L[3] * .68))
            lz.text(SLW - 60, SLH - 40, "Conforme a la Ley de Compañía Digital", "r", 22, rgba(GRIS, .8), anchor="rs")
        elif t < T[5]:
            b0 = T[4]
            n = eo(seg(t, b0 + L[4] * .15, b0 + L[4] * .42))
            aparece(lz, cx, 430, f"{int(round(94 * n))} %", "bahn_Light", 300, AMBAR, seg(t, b0, b0 + .4), sube=0)
            aparece(lz, cx, 545, "de los padres nunca lo notó", "sl", 54, CREMA, seg(t, b0 + L[4] * .4, b0 + L[4] * .5))
            lz.text(cx, SLH - 40, "Prueba piloto · 1 200 familias · Guadalajara y Ciudad de México", "r", 22,
                    rgba(GRIS, .8), anchor="ms")
        else:
            b0 = T[5]
            logo_centrado(lz, cx, 300, 64, 1.0, 1.0)
            aparece(lz, cx, 480, "Para los que no pueden estar.", "l", 60, CREMA, seg(t, b0 + .8, b0 + 1.6))
        return lz

    def r(t, f):
        k = max(i for i in range(8) if t >= c[i])
        x = seg(t, c[k], c[k + 1])
        if k == 0:
            return sala(t, x, 1.0, 1.07, (.5, .42), (.5, .4), lamina(t))
        if k == 1:
            fr, _ = kb(foto("bg/key_valeria"), x, 1.06, 1.14, (.56, .5), (.62, .48))
            return fr
        if k == 2:
            return sala(t, x, 1.72, 1.84, (.505, .25), (.505, .24), lamina(t))
        if k == 3:
            fr, _ = kb(foto("bg/key_publico"), x, 1.04, 1.12, (.42, .5), (.38, .5))
            return fr
        if k == 4:
            return sala(t, x, 1.36, 1.44, (.5, .3), (.5, .29), lamina(t))
        if k == 5:
            fr, _ = kb(foto("bg/key_publico"), x, 1.38, 1.48, (.56, .56), (.58, .55))
            return fr
        if k == 6:
            return sala(t, x, 1.14, 1.0, (.5, .4), (.5, .42), lamina(t))
        fr, _ = kb(foto("bg/key_valeria2"), x, 1.0, 1.08, (.5, .5), (.5, .46))
        fr *= 1 + .06 * math.sin(t * 9) * math.sin(t * 2.3)
        return fr
    return r


@pieza
def f_keynote_2(P):
    L = [dur(f"keynote_2_{i}") for i in range(1, 4)]
    T = [1.1, 1.1 + L[0] + .7]
    T.append(T[1] + L[1] + .7)
    fin = T[2] + L[2]
    assert fin < P.d - 1.4, f"keynote_2 no cabe: {fin:.1f}"
    A = P.audio
    for i in range(3):
        A.voz(f"keynote_2_{i + 1}", T[i], sala=.2)
    A.add(s_ruido(P.d, 50, 500, .007, seed=32), 0)
    A.add(s_aplauso(P.d - fin + .2, .2, seed=7), fin - .1)
    c = [0, T[0] + L[0] * .3, T[1], T[1] + L[1] * .5, T[2] + L[2] * .42, P.d - 2.4, P.d]

    def lamina(t):
        lz = diapo()
        cx = SLW / 2
        if t < T[1] + L[1] * .5:
            b0 = T[0]
            n = eio(seg(t, b0 + L[0] * .42, b0 + L[0] * .78))
            v = int(round(lerp(40, 312, n))) * 1_000_000
            s_ = f"{v:,}".replace(",", " ")
            col = tuple(int(lerp(CREMA[i], AMBAR[i], n)) for i in range(3))
            lz.text(cx, 400, s_, "bahn_Light", 200, rgba(col), anchor="ms")
            et = "usuarios" if n < .5 else "familias que vuelven a hablar cada domingo"
            lz.text(cx, 500, et, "sl", 46, rgba(CREMA2, abs(n - .5) * 2 if .3 < n < .7 else 1), anchor="ms")
            lz.logo(120, 90, 22, tam=24)
        elif t < T[2]:
            aparece(lz, cx, 390, "¿Y cuando ya no está?", "l", 96, CREMA, seg(t, T[1] + L[1] * .55, T[1] + L[1] * .7))
        else:
            b0 = T[2]
            p = eo(seg(t, b0 + .2, b0 + 1.6))
            logo_centrado(lz, cx, 250, 70, p, ss(seg(t, b0 + 1.0, b0 + 1.8)))
            aparece(lz, cx, 395, "Legado", "geoi", 96, AMBAR, seg(t, b0 + L[2] * .2, b0 + L[2] * .32))
            aparece(lz, cx, 560, "Porque una llamada de domingo no tiene por qué terminar.", "sl", 44, CREMA2,
                    seg(t, b0 + L[2] * .45, b0 + L[2] * .55))
        return lz

    def r(t, f):
        k = max(i for i in range(6) if t >= c[i])
        x = seg(t, c[k], c[k + 1])
        if k == 0:
            fr, _ = kb(foto("bg/key_valeria2"), x, 1.0, 1.1, (.5, .52), (.5, .48))
            fr *= 1 + .05 * math.sin(t * 7) * math.sin(t * 1.9)
            return fr
        if k == 1:
            return sala(t, x, 1.75, 1.86, (.505, .25), (.505, .24), lamina(t))
        if k == 2:
            fr, _ = kb(foto("bg/key_publico"), x, 1.3, 1.38, (.72, .45), (.7, .46))
            return fr
        if k == 3:
            return sala(t, x, 1.4, 1.5, (.5, .3), (.5, .28), lamina(t))
        if k == 4:
            return sala(t, x, 1.18, 1.02, (.5, .38), (.5, .42), lamina(t))
        fr, _ = kb(foto("bg/key_valeria2"), x, 1.25, 1.32, (.5, .5), (.5, .47))
        fr *= 1 + .07 * math.sin(t * 10) * math.sin(t * 2.7)
        return fr
    return r


# ─────────────── anuncio en la tele ───────────────
QTV = [(259, 141), (540, 175), (541, 379), (262, 385)]


def tarjeta_vidrio(fr, lz, cx, cy, yaw=0.0, pitch=0.0, roll=0.0, op=1.0, escala=1.0):
    c = lz.out()
    h, w = c.shape[:2]
    q = quad3d(cx, cy, w * escala, h * escala, yaw, pitch, roll)
    sombra(fr, q, 10, 22, 30, .35 * op)
    pegar_quad(fr, c, q, op, vidrio=16)
    return q


@lru_cache(None)
def _fondo_final():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * .45) / H) ** 2 * 1.4)
    g = np.clip(1 - r * 1.5, 0, 1) ** 2
    a = np.float32(TINTA) / 255 * (1 - g[..., None]) + np.float32((92, 64, 38)) / 255 * g[..., None]
    return a.astype(np.float32)


@lru_cache(None)
def _bokeh():
    """Campo de luces desenfocadas (aditivo) un poco más grande que el cuadro, para desplazarlo despacio."""
    rng = np.random.default_rng(12)
    b = np.zeros((H + 200, W + 300, 3), np.float32)
    for x, y, s in rng.uniform(0, 1, (18, 3)):
        a = .02 + .035 * s
        cv2.circle(b, (int(x * (W + 300)), int(y * (H + 200))), int(30 + 80 * s), (a, a * .72, a * .42), -1,
                   lineType=cv2.LINE_AA)
    return cv2.GaussianBlur(b, (0, 0), 6)


def cierre_marca(t, t0, tag="Para los que no pueden estar.", letra=True):
    """Placa final del anuncio (cuadro completo)."""
    fr = _fondo_final().copy()
    bk = _bokeh()
    ox, oy = int(80 + math.sin(t * .21) * 70), int(60 + math.cos(t * .17) * 50)
    fr += bk[oy:oy + H, ox:ox + W]
    lz = Lz(1600, 600)
    lt = t - t0
    lz.logo(0, 0, 1, txt=False, a=0)
    ancho = 2 * 70 + .75 * 70 + lz.ancho("PRESENTE", "l", 74, 74 * .38)
    lz.logo(800 - ancho / 2 + 70, 210, 70, prog=eo(seg(lt, 0, 1.0)), txt=False)
    lz.text(800 - ancho / 2 + 70 + 122, 210, "PRESENTE", "l", 74, rgba(CREMA, ss(seg(lt, .5, 1.2))), anchor="lm", track=28)
    aparece(lz, 800, 380, tag, "l", 54, CREMA2, seg(lt, .9, 1.6))
    if letra:
        lz.text(800, 560, "PRESENTE funciona conforme a la Ley de Compañía Digital. El familiar no recibe aviso. "
                          "Ánimo medido en pruebas internas.", "r", 17, rgba(GRIS, .7 * ss(seg(lt, 1.2, 1.8))), anchor="ms")
    pegar(fr, lz.out(), W / 2 - 800, H / 2 - 300)
    return fr


@pieza
def f_anuncio(P):
    L = [dur(f"anuncio_{i}") for i in range(1, 6)]
    gaps = [.5, .6, .6, .7]
    T = [.8]
    for i in range(4):
        T.append(T[-1] + L[i] + gaps[i])
    fin = T[4] + L[4]
    tv0 = min(fin + .35, P.d - 2.4)
    A = P.audio
    for i in range(5):
        A.voz(f"anuncio_{i + 1}", T[i])
    c = [0, T[1] - .25, T[2] - .25, T[3] - .25, T[4] - .35, tv0, P.d]
    for x in c[1:5]:
        A.add(s_swoosh(.5, .025), x - .2)
    A.add(s_ruido(P.d - tv0, 900, 7000, .012, seed=40, am=6), tv0)   # la lluvia del depto
    A.add(s_ruido(P.d - tv0, 60, 240, .006, seed=41), tv0)

    def anuncio(t):
        k = max(i for i in range(5) if t >= c[i])
        x = seg(t, c[k], c[k + 1])
        if k == 4:
            return cierre_marca(t, c[4])
        nom = ["anu_1", "anu_2", "anu_3", "anu_4"][k]
        zz = [(1.0, 1.08, (.45, .45), (.42, .45)), (1.06, 1.0, (.5, .45), (.5, .45)), (1.02, 1.12, (.4, .4), (.42, .38)),
              (1.1, 1.02, (.45, .5), (.5, .5))][k]
        fr, M = kb(foto("bg/" + nom), x, *zz)
        fr *= np.float32([1.05, 1.0, .93])
        lz = Lz(1500, 330)
        b0 = T[k]
        if k == 0:
            aparece(lz, 20, 250, "Cada domingo.", "l", 72, CREMA, seg(t, b0 + .5, b0 + 1.2), anchor="ls")
        elif k == 1:
            for i, (p, fr_) in enumerate((("Una junta.", .38), ("Un vuelo.", .58), ("Una vida.", .78))):
                aparece(lz, 20 + i * 400, 250, p, "l", 66, CREMA if i < 2 else AMBAR_C, seg(t, b0 + L[1] * fr_ - .2, b0 + L[1] * fr_ + .4),
                        anchor="ls")
        elif k == 2:
            aparece(lz, 20, 175, "Tres horas de entrevista.", "sl", 50, CREMA2, seg(t, b0 + .4, b0 + 1.0), anchor="ls")
            aparece(lz, 20, 260, "Con tu cara. Con tu voz.", "l", 72, CREMA, seg(t, b0 + L[2] * .62, b0 + L[2] * .72), anchor="ls")
        else:
            aparece(lz, 20, 260, "Ellos solo sienten que estás.", "l", 66, CREMA, seg(t, b0 + L[3] * .2, b0 + L[3] * .32),
                    anchor="ls")
        o = lz.out()
        sh = o.copy()
        sh[..., :3] = 0
        sh = cv2.GaussianBlur(sh, (0, 0), 6)
        pegar(fr, sh, 128, H - 410, .6)
        pegar(fr, o, 120, H - 420)
        if k == 2:   # la llamada que flota junto al teléfono del señor
            a = ven(t, c[2] + .8, c[3], .5, .3)
            if a > 0:
                card = Lz(380, 96)
                card.rect(0, 0, 380, 96, r=48, fill=rgba((48, 40, 34), .72))
                card.circ(48, 48, 10 + 2 * math.sin(t * 5), fill=rgba(AMBAR))
                card.text(78, 44, "En llamada con Daniel", "sb", 24, CREMA, anchor="ls")
                s_ = int(724 + t - c[2])
                card.text(78, 74, f"{s_ // 60:02d}:{s_ % 60:02d} · PRESENTE", "r", 18, rgba(GRIS), anchor="ls")
                p = mapa(M, [(530, 300)])[0]
                tarjeta_vidrio(fr, card, p[0] + 190, p[1], yaw=-8 + vaiven(t) * 1.5, op=a)
        if k == 3:
            a = ven(t, c[3] + .5, c[4], .5, .3)
            if a > 0:
                card = Lz(460, 120)
                card.rect(0, 0, 460, 120, r=30, fill=rgba((48, 40, 34), .72))
                card.logo(46, 60, 16, txt=False)
                card.text(84, 70, "Modo discreto", "sb", 30, CREMA, anchor="ls")
                interruptor(card, 340, 34, eio(seg(t, b0 + .8, b0 + 1.2)))
                tarjeta_vidrio(fr, card, 1440, 330, yaw=-10 + vaiven(t, 2) * 1.5, op=a)
        return fr

    def r(t, f):
        if t < c[5]:
            return anuncio(t)
        x = seg(t, c[5], P.d)
        fr, M = kb(foto("esc/depto", 0, .72), x, 1.45, 1.3, (.29, .33), (.3, .34))
        fr *= np.float32([.88, .97, 1.04])
        tvf = cv2.resize(cierre_marca(t, c[4]), (640, 360), interpolation=cv2.INTER_AREA)
        q = mapa(M, QTV)
        luz(fr, q, tvf[::20, ::20].reshape(-1, 3).mean(0) + .12, blur=70, fuerza=.3, crece=1.2)
        pegar_quad(fr, np.dstack([tvf * .92 + .02, np.ones((360, 640, 1), np.float32)]), q)
        return fr
    return r


# ─────────────── noticiero ───────────────
NAVY = (14, 26, 48)
ROJO = (196, 38, 46)
QMURO = [(792, 168), (1338, 124), (1338, 398), (792, 418)]
TICKER = ("TECNOLOGÍA  |  PRESENTE suma 40 millones de usuarios  |  Senado aprueba la Ley de Compañía Digital: sin aviso "
          "obligatorio al familiar  |  Guadalajara: 24 °C, cielo despejado  |  Las acciones de compañía digital suben 6 %  |  ")


@lru_cache(None)
def _ticker():
    lz = Lz(10, 10)
    w = int(lz.ancho(TICKER, "bahn_SemiBold", 28)) + 10
    lz = Lz(w, 46, NAVY, k=1)
    lz.text(0, 33, TICKER, "bahn_SemiBold", 28, (235, 238, 244), anchor="ls")
    return lz.rgb()


def zocalo(fr, t, titulo, sub, a, hora="21:34"):
    lz = Lz(W, 300, k=1)
    if a > 0:
        lz.rect(120, 16, 262, 52, fill=rgba(ROJO, a))
        lz.text(191, 43, "EN VIVO", "bahn_Bold", 24, rgba((255, 255, 255), a), anchor="ms")
        tw = lz.ancho(titulo, "bahn_Bold", 46) + 60
        lz.rect(120, 60, 120 + tw * eo(a), 136, fill=rgba((242, 242, 238), a))
        lz.text(150, 116, titulo, "bahn_Bold", 46, rgba(NAVY, a), anchor="ls")
        sw = lz.ancho(sub, "bahn", 28) + 60
        lz.rect(120, 136, 120 + max(tw, sw) * eo(a), 184, fill=rgba(NAVY, a * .94))
        lz.text(150, 170, sub, "bahn", 28, rgba((235, 238, 244), a), anchor="ls")
    lz.rect(0, 230, 270, 276, fill=rgba(ROJO))
    lz.text(135, 263, "ÚLTIMA HORA", "bahn_Bold", 26, (255, 255, 255, 255), anchor="ms")
    pegar(fr, lz.out(), 0, 780)
    tk = _ticker()
    off = int(t * 130) % tk.shape[1]
    tira = np.concatenate([tk, tk], 1)[:, off:off + W - 270]
    fr[1010:1056, 270:270 + tira.shape[1]] = tira
    bug = Lz(360, 90)
    bug.rect(0, 10, 18, 70, fill=rgba(ROJO))
    bug.text(32, 52, "MERIDIANO", "bahn_Bold", 38, (255, 255, 255, 235), anchor="ls")
    bug.text(34, 80, f"NOTICIAS · {hora}", "bahn", 20, (230, 232, 240, 210), anchor="ls")
    pegar(fr, bug.out(), W - 420, 50)


@pieza
def f_noticiero(P):
    L = [dur(f"noticiero_{i}") for i in range(1, 4)]
    gap = .25
    T = [.35, .35 + L[0] + gap]
    T.append(T[1] + L[1] + gap)
    if T[2] + L[2] > P.d - .1:
        gap = max(.05, (P.d - .1 - .35 - sum(L)) / 2)
        T = [.35, .35 + L[0] + gap]
        T.append(T[1] + L[1] + gap)
    A = P.audio
    for i in range(3):
        A.voz(f"noticiero_{i + 1}", T[i])
    c = [0, 2.6, T[1], T[2], P.d]
    A.add(s_swoosh(.5, .04), .3)
    A.add(s_ruido(T[1] - 2.6, 40, 300, .012, seed=50), 2.6)
    A.add(s_murmullo(T[2] - T[1], .012, seed=51), T[1])
    A.add(s_ruido(P.d - T[2], 80, 900, .005, seed=52), T[2])
    tit = [("PRESENTE SUPERA LOS 40 MILLONES DE USUARIOS", "La app que llama a tus papás por ti, con tu cara y con tu voz"),
           ("APRUEBAN LA LEY DE COMPAÑÍA DIGITAL", "Las empresas no tendrán que avisar al familiar que habla con una IA"),
           ("94 % DE LOS PADRES NUNCA LO NOTA", "Cifra de la propia empresa · no hay estudios independientes")]

    def r(t, f):
        k = max(i for i in range(4) if t >= c[i])
        x = seg(t, c[k], c[k + 1])
        if k == 0:
            fr, M = kb(foto("bg/noti_estudio", 0, .9), x, 1.0, 1.08, (.55, .45), (.58, .44))
            q = mapa(M, QMURO)
            lz = Lz(1100, 560, k=1)
            n = eo(seg(t, .3, 1.9))
            v = f"{int(40_000_000 * n):,}".replace(",", " ")
            lz.text(550, 290, v, "bahn_SemiBold", 170, rgba((236, 242, 250), .95), anchor="ms")
            lz.text(550, 380, "USUARIOS DE PRESENTE", "bahn", 46, rgba((200, 214, 236), .9), anchor="ms", track=6)
            lz.rect(330, 420, 770, 424, fill=rgba(ROJO, .9))
            luz(fr, q, (.08, .12, .2), blur=60, fuerza=.5, crece=1.0)
            pegar_quad(fr, lz.out(), q)
        else:
            nom = ["noti_1", "noti_3", "noti_2"][k - 1]
            zz = [(1.04, 1.12, (.5, .45), (.52, .45)), (1.1, 1.02, (.6, .4), (.55, .42)), (1.0, 1.08, (.45, .5), (.48, .48))][k - 1]
            fr, _ = kb(foto("bg/" + nom), x, *zz)
            if k == 3:
                card = Lz(420, 250)
                card.rect(0, 0, 420, 250, r=6, fill=rgba(NAVY, .78))
                card.text(210, 150, "94 %", "bahn_SemiBold", 130, rgba((242, 242, 238)), anchor="ms")
                card.text(210, 205, "de los padres no lo nota", "bahn", 28, rgba((210, 220, 236)), anchor="ms")
                card.rect(0, 0, 420, 8, fill=rgba(ROJO))
                tarjeta_vidrio(fr, card, 1540, 330, op=ven(t, c[3] + .6, P.d + 1, .5, .1))
        i = 0 if t < c[2] else 1 if t < c[3] else 2
        cambio = c[[0, 2, 3][i]]
        a = ss(seg(t, .5, 1.0)) if i == 0 else ss(seg(t, cambio + .05, cambio + .45))
        zocalo(fr, t, tit[i][0], tit[i][1], a)
        return fr
    return r


# ─────────────── la laptop: entrevista y altas ───────────────
QLAP = [(681, 439), (876, 455), (849, 604), (654, 573)]


def laptop_cerca(t, P, pant, yaw0, yaw1, hz0=1580, hz1=1500, hx0=-30, hx1=20, wide=None):
    x = t / P.d
    fondo = foto("bg/laptop_noche", 16, .4)
    fr, _ = kb(fondo, x, 1.15, 1.22, (.62, .42), (.58, .44))
    poner_laptop(fr, pant, hx=lerp(hx0, hx1, x), hy=300, hz=lerp(hz0, hz1, x) + 290, yaw=lerp(yaw0, yaw1, x))
    return fr


def laptop_lejos(x, pant):
    fr, M = kb(foto("bg/laptop_noche"), x, 1.0, 1.18, (.55, .55), (.57, .6))
    q = mapa(M, QLAP)
    s = np.clip(pant * 1.25 + .03, 0, 1)
    luz(fr, q, s[::50, ::50].reshape(-1, 3).mean(0) + .1, blur=40, fuerza=.18, crece=1.1)
    pegar_quad(fr, np.dstack([s, np.ones(s.shape[:2] + (1,), np.float32)]), q)
    return fr


def progreso(lz, n, total=212, y=905, a=1.0):
    lz.rect(260, y, LW - 260, y + 6, r=3, fill=rgba(PANEL, a))
    lz.rect(260, y, 260 + (LW - 520) * cl(n / total), y + 6, r=3, fill=rgba(AMBAR, a))


def pregunta(lz, t, t0, txt, a=1.0):
    p = seg(t, t0, t0 + .35)
    if p <= 0:
        return
    y = 540 + (1 - eo(p)) * 30
    lz.rect(260, y, LW - 260, y + 190, r=34, fill=rgba(PANEL, ss(p) * a))
    tt = escribe(txt, seg(t, t0 + .2, t0 + .2 + len(txt) * .035))
    lz.text(LW / 2, y + 112, tt, "sl", 52, rgba(CREMA, ss(p) * a), anchor="ms")
    if len(tt) < len(txt) or int(t * 2) % 2:
        w = lz.ancho(tt, "sl", 52)
        lz.rect(LW / 2 + w / 2 + 6, y + 70, LW / 2 + w / 2 + 9, y + 124, fill=rgba(AMBAR, ss(p) * a))


def escucha(lz, t, t0, a=1.0):
    p = ss(seg(t, t0, t0 + .5)) * a
    if p <= 0:
        return
    ondas(lz, LW / 2 - 200, 810, 400, 70, t, .5 + .5 * abs(math.sin(t * 1.7)), a=p)
    lz.text(LW / 2, 875, "Escuchando…", "r", 22, rgba(GRIS, p), anchor="ms")


@pieza
def f_onboard_1(P):
    V = 2.5
    P.audio.voz("onboard_1", V)
    P.audio.add(s_noti(.06), 2.3)
    P.audio.add(s_ruido(P.d, 60, 500, .006, seed=60), 0)
    Tq = V + dur("onboard_1") * .52

    def pant(t):
        lz = app_lz(LW, LH)
        barra_app(lz, "Entrevista · pregunta 1 de 212")
        aparece(lz, LW / 2, 300, "Hola, Daniel.", "sl", 46, GRIS, seg(t, .2, .8))
        aparece(lz, LW / 2, 410, "Vamos a conocer a tu papá.", "l", 86, CREMA, seg(t, .5, 1.2))
        lz.text(LW / 2, 960, "unas 3 horas · puedes pausar cuando quieras", "r", 22, rgba(GRIS, .8), anchor="ms")
        progreso(lz, 1, y=925)
        pregunta(lz, t, Tq, "¿Cómo te dice cuando está contento?")
        escucha(lz, t, Tq + 1.9)
        return lz.rgb()

    def r(t, f):
        if t < 2.3:
            return laptop_lejos(t / 2.3, pant(t))
        return laptop_cerca(t, P, pant(t), -13, -9)
    return r


@pieza
def f_onboard_2(P):
    V = .55
    P.audio.voz("onboard_2", V)
    P.audio.add(s_ruido(P.d, 60, 500, .006, seed=61), 0)

    def pant(t):
        lz = app_lz(LW, LH)
        barra_app(lz, "Entrevista · pregunta 2 de 212")
        a = seg(t, .05, .5)
        lz.rect(LW / 2 - 190, 250, LW / 2 + 190, 330, r=40, fill=rgba(PANEL, ss(a)))
        lz.text(LW / 2 - 40, 302, "«Chato»", "sl", 36, rgba(CREMA, ss(a)), anchor="ms")
        lz.line([(LW / 2 + 82, 290), (LW / 2 + 96, 304), (LW / 2 + 124, 274)], fill=rgba(AMBAR, ss(a)), width=4)
        lz.text(LW / 2, 380, "guardado · así te dice cuando está contento", "r", 22, rgba(GRIS, ss(a) * .9), anchor="ms")
        progreso(lz, 2, y=925)
        pregunta(lz, t, V + .1, "¿Y cuando está enojado?")
        escucha(lz, t, V + 1.9)
        return lz.rgb()

    return lambda t, f: laptop_cerca(t, P, pant(t), 10, 7, 1540, 1490, 30, -10)


@pieza
def f_onboard_3(P):
    V = 1.1
    P.audio.voz("onboard_3", V)
    P.audio.add(s_ruido(P.d, 60, 500, .006, seed=62), 0)
    Tq = V + dur("onboard_3") * .36

    def pant(t):
        lz = app_lz(LW, LH)
        p = eio(seg(t, .15, 1.5))
        n = int(round(lerp(2, 212, p)))
        mins = int(lerp(6, 178, p))
        barra_app(lz, f"Entrevista · pregunta {n} de 212")
        lz.text(LW / 2, 960, f"llevas {mins // 60} h {mins % 60:02d} min", "r", 22, rgba(GRIS, .85), anchor="ms")
        progreso(lz, n, y=925)
        aparece(lz, LW / 2, 400, "ÚLTIMA PREGUNTA", "sb", 26, AMBAR, seg(t, 1.2, 1.7), track=6)
        pregunta(lz, t, Tq, "¿Qué es lo que más le duele a tu papá?")
        escucha(lz, t, Tq + 2.1)
        return lz.rgb()

    return lambda t, f: laptop_cerca(t, P, pant(t), -16, -12, 1600, 1530, -60, -20)


@pieza
def f_onboard_4(P):
    V1, V2 = .4, 9.0
    P.audio.voz("onboard_4_1", V1)
    P.audio.voz("onboard_4_2", V2)
    P.audio.add(s_ruido(P.d, 60, 500, .006, seed=63), 0)
    P.audio.add(s_click(.22), 13.7)
    P.audio.add(s_noti(.05), 8.9)
    for k in range(5):
        P.audio.add(s_tap(.06), 2.2 + 1.2 * k)
    cara_im = cara("presente_daniel").resize((420, 420), Image.LANCZOS)
    carr = np.asarray(cara_im, np.float32) / 255
    rng = np.random.default_rng(14)
    N = 12
    ts = 420 // N
    tiles = [(i, j, rng.uniform(1.8, 6.6), rng.uniform(-1, 1), rng.uniform(-1, 1)) for i in range(N) for j in range(N)]
    FX, FY = 250, 300
    items = [("Su voz", 2.2), ("Sus gestos", 3.4), ("Su forma de hablar", 4.6), ("1 842 recuerdos", 5.8),
             ("Cómo le dice tu papá: «Chato»", 7.0)]

    def pant(t):
        lz = app_lz(LW, LH)
        barra_app(lz, "Tu Presente")
        a0 = 1 - ss(seg(t, 1.4, 1.9))
        if a0 > 0:
            aparece(lz, LW / 2, 470, "Entrevista completada", "l", 76, CREMA, seg(t, .1, .6))
            lz.text(LW / 2, 540, "3 h 02 min · 212 respuestas", "r", 26, rgba(GRIS, ss(seg(t, .4, .9)) * a0), anchor="ms")
        if t > 1.6:
            a1 = ss(seg(t, 1.6, 2.1))
            listo = seg(t, 8.6, 9.2)
            pr = eo(seg(t, 1.8, 8.4))
            if listo < 1:
                lz.text(FX, 230, f"Creando a tu Presente…  {int(pr * 100)} %", "sl", 30, rgba(CREMA2, a1 * (1 - listo)), anchor="ls")
            if listo > 0:
                aparece(lz, FX, 230, "Tu Presente está listo.", "l", 46, CREMA, listo, anchor="ls")
            lz.rect(FX - 8, FX + 42, FX + 428, FX + 478, r=34, outline=rgba(AMBAR, a1 * .5), width=2)
            if listo < 1:
                for i, (txt, ti) in enumerate(items):
                    a = seg(t, ti, ti + .4) * (1 - listo)
                    if a <= 0:
                        continue
                    y = 340 + i * 82
                    lz.circ(820, y - 10, 16, outline=rgba(AMBAR, ss(a)), width=3)
                    lz.line([(812, y - 10), (818, y - 3), (829, y - 18)], fill=rgba(AMBAR, ss(a)), width=3)
                    lz.text(856, y, txt, "sl", 34, rgba(CREMA, ss(a)), anchor="ls")
            if listo > 0:
                y0 = 330 + (1 - eo(listo)) * 30
                a = ss(listo)
                lz.rect(760, y0, 1380, y0 + 300, r=34, fill=rgba(PANEL, a))
                lz.text(800, y0 + 80, "Modo discreto", "sb", 40, rgba(CREMA, a), anchor="ls")
                on = eio(seg(t, 13.75, 14.05))
                interruptor(lz, 1230, y0 + 38, on, a, w=110, h=58)
                lz.parrafo(800, y0 + 140, "Papá nunca recibirá un aviso de que habla con tu Presente.", "r", 26,
                           rgba(CREMA2, a), 390)
                lz.text(800, y0 + 262, "Conforme a la Ley de Compañía Digital, art. 12", "r", 18, rgba(GRIS, a * .9), anchor="ls")
                if on > .5:
                    lz.text(1285, y0 + 130, "Activado", "sb", 22, rgba(AMBAR, ss(seg(t, 14.05, 14.4))), anchor="ms")
                if t > 11.4:
                    m = eio(seg(t, 11.6, 13.3))
                    cx_, cy_ = lerp(1470, 1268, m), lerp(930, y0 + 70, m)
                    cursor(lz, cx_, cy_, ven(t, 13.6, 13.95, .08, .12), ss(seg(t, 11.4, 11.7)))
        img = lz.rgb()
        if t > 1.6:   # el mosaico de la cara que se arma
            a1 = ss(seg(t, 1.6, 2.1))
            sc = int(lerp(0, 110, ss(seg(t, 4.0, 8.0))) * (1 - ss(seg(t, 8.3, 8.9))))
            for i, j, d0, dx, dy in tiles:
                p = eo(seg(t, d0, d0 + .8))
                if p <= 0:
                    continue
                gap = 2 * (1 - ss(seg(t, 7.6, 8.4)))
                x = int(FX + j * ts + dx * 120 * (1 - p))
                y = int(FY + i * ts + dy * 120 * (1 - p))
                tile = carr[i * ts:(i + 1) * ts, j * ts:(j + 1) * ts]
                g = int(gap)
                tile = tile[g:ts - g, g:ts - g] if g else tile
                hh, ww = tile.shape[:2]
                if 0 <= x and x + ww <= LW and 0 <= y and y + hh <= LH:
                    w8 = p * a1
                    img[y:y + hh, x:x + ww] = img[y:y + hh, x:x + ww] * (1 - w8) + tile * w8
            if 3.5 < t < 8.5:
                yy = int(FY + (t - 3.5) / 5.0 * 420)
                img[yy:yy + 3, FX:FX + 420] = img[yy:yy + 3, FX:FX + 420] * .4 + np.float32(AMBAR) / 255 * .6
        return img

    return lambda t, f: laptop_cerca(t, P, pant(t), -11, -6, 1560, 1480, -20, 30)


@pieza
def f_agregar_lucia(P):
    V = 2.1
    P.audio.voz("agregar_lucia", V)
    P.audio.add(s_ruido(P.d, 60, 500, .006, seed=64), 0)
    P.audio.add(s_click(.22), 1.5)
    P.audio.add(s_noti(.05), 1.7)
    filas = [("Mensajes", 2418), ("Audios", 96), ("Fotos", 312), ("Llamadas", 41)]

    def pant(t):
        lz = app_lz(LW, LH)
        barra_app(lz, "Contactos", centro="Agregar a tu Presente")
        lz.rect(220, 190, 760, 790, r=36, fill=rgba(PANEL))
        lz.circ(490, 340, 96, fill=rgba((30, 25, 21)), outline=rgba(AMBAR), width=3)
        lz.text(490, 372, "L", "bahn_Light", 100, rgba(AMBAR), anchor="ms")
        lz.text(490, 520, "Lucía Ortega", "sb", 42, rgba(CREMA), anchor="ms")
        lz.text(490, 565, "Hermana · Guadalajara", "r", 24, rgba(GRIS), anchor="ms")
        lz.text(300, 680, "Tu Presente atenderá sus llamadas", "r", 22, rgba(CREMA2), anchor="ls")
        interruptor(lz, 300, 700, 1.0, w=80, h=42)
        lz.text(400, 730, "Modo discreto", "sb", 22, rgba(AMBAR), anchor="ls")
        for i, (nom, v) in enumerate(filas):
            y = 230 + i * 110
            p = eo(seg(t, .1 + i * .15, 1.2 + i * .15))
            lz.text(860, y, nom, "r", 26, rgba(GRIS), anchor="ls")
            lz.text(1380, y, f"{int(v * p):,}".replace(",", " "), "bahn_SemiBold", 34, rgba(CREMA), anchor="rs")
            lz.rect(860, y + 22, 1380, y + 28, r=3, fill=rgba(TINTA))
            lz.rect(860, y + 22, 860 + 520 * p, y + 28, r=3, fill=rgba(AMBAR))
        hecho = seg(t, 1.6, 1.9)
        col = tuple(int(lerp(AMBAR[i], PANEL[i], hecho)) for i in range(3))
        lz.rect(860, 700, 1380, 780, r=40, fill=rgba(col))
        if hecho < .5:
            lz.text(1120, 752, "Agregar a Lucía", "sb", 30, rgba(TINTA), anchor="ms")
        else:
            lz.text(1140, 752, "Lucía agregada", "sb", 30, rgba(AMBAR), anchor="ms")
            lz.line([(990, 740), (1002, 752), (1024, 726)], fill=rgba(AMBAR), width=4)
        a = seg(t, 2.4, 3.0)
        if a > 0:
            y = 860 + (1 - eo(a)) * 30
            lz.rect(220, y, 1380, y + 80, r=40, fill=rgba((30, 25, 21), ss(a)))
            lz.circ(270, y + 40, 8, fill=rgba(AMBAR, ss(a)))
            lz.text(300, y + 50, "Tu Presente atiende a:  Papá  ·  Lucía", "r", 26, rgba(CREMA, ss(a)), anchor="ls")
            lz.text(1340, y + 50, "modo discreto", "r", 22, rgba(GRIS, ss(a)), anchor="rs")
        if t < 2.2:
            m = eio(seg(t, .2, 1.3))
            cursor(lz, lerp(1500, 1180, m), lerp(960, 745, m), ven(t, 1.4, 1.65, .06, .1), 1 - ss(seg(t, 1.9, 2.2)))
        return lz.rgb()

    return lambda t, f: laptop_cerca(t, P, pant(t), 9, 13, 1560, 1500, 20, -20)


# ─────────────── cartas ───────────────
def _carta(txt):
    def f(P):
        for i in range(8):
            P.audio.add(s_tick(1.0 if i % 2 == 0 else .82, .028), .25 + i * .5)

        def r(t, f_):
            fr = np.zeros((H, W, 3), np.float32) + .012
            lz = Lz(1500, 140)
            lz.text(750, 90, txt, "l", 46, rgba(CREMA, ven(t, .3, P.d - .25, .7, .55)), anchor="ms",
                    track=lerp(12, 19, t / P.d))
            pegar(fr, lz.out(), W / 2 - 750, H / 2 - 90)
            return fr
        return r
    return f


PIEZAS["carta_4meses"] = _carta("CUATRO MESES DESPUÉS")
PIEZAS["carta_3semanas"] = _carta("TRES SEMANAS DESPUÉS")
PIEZAS["carta_6meses"] = _carta("SEIS MESES DESPUÉS")


# ─────────────── montaje ───────────────
LLAMADAS = [("lun 27 jul", "14 min", 81, "Le contó de su rodilla."),
            ("mié 5 ago", "22 min", 84, "Volvió a poner boleros en las mañanas."),
            ("dom 16 ago", "31 min", 86, "Ganó dos partidas de dominó."),
            ("jue 27 ago", "18 min", 87, "Arregló un reloj de pared para una vecina."),
            ("lun 7 sep", "26 min", 88, "Se rió con la historia del avión."),
            ("sáb 19 sep", "12 min", 89, "Comió chilaquiles con don Chuy."),
            ("mié 30 sep", "40 min", 90, "Habló de tu mamá sin llorar."),
            ("dom 11 oct", "21 min", 91, "Preguntó por Inés y el bebé."),
            ("vie 23 oct", "17 min", 92, "Durmió bien toda la semana."),
            ("mar 3 nov", "28 min", 93, "Te leyó un poema de tu mamá."),
            ("dom 15 nov", "35 min", 94, "Dice que eres su orgullo.")]


@lru_cache(None)
def _tarjeta_llamada(i):
    fe, mi, an, re = LLAMADAS[i]
    lz = Lz(560, 150)
    lz.rect(0, 0, 560, 150, r=30, fill=rgba((40, 34, 29), .70))
    icono_app(lz, 22, 22, 42)
    lz.text(82, 50, f"Llamada con Papá · {fe}", "sb", 24, CREMA, anchor="ls")
    lz.text(82, 82, f"{mi} · Ánimo {an} %", "r", 20, rgba(AMBAR_C), anchor="ls")
    lz.text(82, 120, re, "i", 21, rgba(CREMA2), anchor="ls")
    return lz


@pieza
def f_montaje(P):
    imgs = ["mon_1", "mon_2", "mon_3", "mon_4", "mon_5"]
    movs = [(1.03, 1.12, (.5, .4), (.55, .36)), (1.12, 1.03, (.45, .5), (.5, .5)), (1.04, 1.13, (.62, .5), (.66, .45)),
            (1.12, 1.04, (.6, .45), (.56, .45)), (1.03, 1.11, (.6, .45), (.64, .42))]
    seg_d = P.d / 5
    tk = [1.6 + 3.4 * k for k in range(len(LLAMADAS))]
    for t0 in tk:
        P.audio.add(s_noti(.045), t0)
    P.audio.add(s_ruido(P.d, 70, 800, .005, seed=70), 0)
    for i in range(int(P.d)):
        P.audio.add(s_tick(1.0 if i % 2 == 0 else .82, .014), .3 + i)

    def r(t, f):
        fr = None
        for i in range(5):
            a0, a1 = i * seg_d - .45, (i + 1) * seg_d + .45
            if a0 <= t <= a1:
                x = seg(t, a0, a1)
                img, _ = kb(foto("bg/" + imgs[i]), x, *movs[i])
                w8 = ss(seg(t, a0, a0 + .9)) if i > 0 else 1.0
                fr = img if fr is None else fr * (1 - w8) + img * w8
        # contador
        n = int(1 + 117 * (t / P.d) ** 1.08)
        a = ss(seg(t, .5, 1.3))
        card = Lz(420, 220)
        card.rect(0, 0, 420, 220, r=30, fill=rgba((40, 34, 29), .66))
        card.logo(36, 38, 12, tam=14)
        card.text(30, 92, "Llamadas con Papá", "sb", 22, rgba(CREMA2), anchor="ls")
        card.text(30, 178, str(n), "bahn_Light", 92, rgba(CREMA), anchor="ls")
        card.text(390, 178, f"racha de {n} días", "r", 20, rgba(AMBAR_C), anchor="rs")
        pts = [(230 + k * 12, 130 - 40 * (k / 13) - 6 * math.sin(k * 1.7)) for k in range(14)]
        card.line(pts[:max(2, int(2 + 12 * t / P.d))], rgba(AMBAR, .9), 3)
        tarjeta_vidrio(fr, card, 1630, 190, yaw=-9 + vaiven(t, 1) * 1.2, pitch=2, op=a)
        # registro de llamadas que se apila
        lleg = sum(eo(seg(t, x0, x0 + .6)) for x0 in tk)
        for k in range(len(LLAMADAS)):
            slot = lleg - 1 - k
            if slot < -1 or slot > 3:
                continue
            op = ss(cl(slot + 1)) * (1 - ss(seg(slot, 2.0, 2.9)))
            if op <= 0:
                continue
            y = 930 - slot * 168
            tarjeta_vidrio(fr, _tarjeta_llamada(k), 400, y, yaw=9 + vaiven(t, k) * .8, op=op)
        return fr
    return r


# ─────────────── el tablero ───────────────
@pieza
def f_dashboard(P):
    fondo = foto("esc/oficina", 9, .6)
    P.audio.add(s_ruido(P.d, 60, 600, .007, seed=80), 0)
    P.audio.add(s_tap(.08), .9)
    av = cara("ramon")
    vals = [.58, .6, .63, .62, .67, .7, .72, .74, .78, .8, .83, .85, .88, .9, .92, .94]

    def pant(t):
        lz = app_lz(SW, SH, 1.2)
        lz.text(40, 40, "9:47", "sb", 17, CREMA, anchor="ls")
        lz.foto(av, 32, 76, 72, 72, circulo=True)
        lz.text(122, 108, "Papá", "sb", 32, CREMA, anchor="ls")
        lz.circ(129, 132, 5, fill=rgba(AMBAR))
        lz.text(142, 138, "Presente activo · modo discreto", "r", 16, rgba(AMBAR_C), anchor="ls")
        p = eo(seg(t, .6, 2.2))
        cx, cy, rr = SW / 2, 330, 118
        lz.arc(cx, cy, rr, 0, 360, rgba(GRIS_O, .5), 16)
        lz.arc(cx, cy, rr, -90, -90 + 360 * .94 * p, rgba(AMBAR), 16)
        lz.text(cx, cy + 22, f"{int(round(94 * p))} %", "bahn_Light", 76, CREMA, anchor="ms")
        lz.text(cx, cy + 60, "ánimo de Papá", "r", 18, rgba(GRIS), anchor="ms")
        n = eo(seg(t, .8, 2.6))
        for i, (v, et) in enumerate(((f"{int(121 * n)}", "llamadas"), (f"{int(118 * n)}", "días seguidos"),
                                     (f"{int(41 * n)} h", "juntos"))):
            x = 90 + i * 160
            lz.text(x, 530, v, "bahn_SemiBold", 42, CREMA, anchor="ms")
            lz.text(x, 560, et, "r", 16, rgba(GRIS), anchor="ms")
        lz.rect(24, 600, SW - 24, 790, r=24, fill=rgba(PANEL))
        lz.text(48, 640, "Ánimo por semana", "r", 18, rgba(GRIS), anchor="ls")
        q = eo(seg(t, 1.4, 3.6))
        pts = [(52 + i * (SW - 104) / 15, 775 - (v - .5) * 270) for i, v in enumerate(vals)]
        m = max(2, int(2 + 14 * q))
        lz.line(pts[:m], rgba(AMBAR), 3)
        for x, y in pts[:m]:
            lz.circ(x, y, 4, fill=rgba(AMBAR_C))
        a = ss(seg(t, 2.6, 3.2))
        lz.rect(24, 808, SW - 24, 940, r=24, fill=rgba(PANEL, a))
        lz.text(48, 848, "Hoy · 9:12 · 24 min", "sb", 20, rgba(CREMA, a), anchor="ls")
        lz.parrafo(48, 884, "«Le contó al Chato que ganó en el dominó.»", "i", 20, rgba(CREMA2, a), SW - 100)
        return lz.rgb()

    def r(t, f):
        fr, _ = kb(fondo, t / P.d, 1.08, 1.14, (.5, .45), (.54, .47))
        m = en_mano(t, 0.0, None, cx=1180, cy=620, alto=1180, seed=1.3, yaw=-8)
        poner_tel(fr, pant(t), **m, resplandor=.12)
        return fr
    return r


# ─────────────── notif_rutina: la fiesta ───────────────
@pieza
def f_notif_rutina(P):
    fondo = foto("bg/fiesta", 6, .78)
    A = P.audio
    A.add(s_murmullo(P.d, .035, seed=9, voces=14), 0)
    rng = np.random.default_rng(19)
    for t0 in rng.uniform(0, P.d - .2, 9):
        A.add(s_tick(rng.uniform(1.6, 2.2), .016), t0)
    A.add(s_vibra(2), 1.2)
    A.add(s_noti(.07), 1.25)
    tv = _tramos(1.2)

    def r(t, f):
        fr, _ = kb(fondo, t / P.d, 1.1, 1.18, (.45, .45), (.42, .44))
        lz = bloqueo("23:58", "jueves, 3 de diciembre", "esc/carretera", .45)
        enc = eo(seg(t, 1.3, 1.75))
        noti(lz, 20, lerp(-320, 300, enc), SW - 40, "Resumen de tu llamada con Papá",
             ["Hoy 23:51 · 2 min · Ánimo de Papá 90 %", "Papá tuvo una revisión médica de rutina. Todo en orden."],
             "ahora", resalta=1)
        m = en_mano(t, .1, 7.7, cx=1150, cy=700, alto=1320, seed=2.1, yaw=-9, roll=-4)
        jx, jy = zumbido(t, tv)
        m["cx"] += jx
        m["cy"] += jy
        poner_tel(fr, lz.rgb(), **m, resplandor=.08)
        return fr
    return r


# ─────────────── notif_lucia: el teléfono en el buró ───────────────
@pieza
def f_notif_lucia(P):
    fondo = foto("esc/depto", 7, .3)
    A = P.audio
    A.add(s_ruido(P.d, 900, 7000, .006, seed=90, am=5), 0)
    A.add(s_ruido(P.d, 40, 200, .005, seed=91), 0)
    A.add(s_vibra(2), .8)
    A.add(s_noti(.06), .85)
    tv = _tramos(.8)

    def r(t, f):
        x = t / P.d
        fr, _ = kb(fondo, x, 1.1, 1.16, (.6, .6), (.6, .62))
        fr *= np.float32([.85, .95, 1.08])
        lz = bloqueo("6:14", "viernes, 4 de diciembre", "esc/carretera", .4)
        noti(lz, 20, lerp(-340, 300, eo(seg(t, .9, 1.35))), SW - 40, "Llamada de Lucía atendida por tu Presente",
             ["Hoy 6:10 · 4 min", "Lucía está alterada: dale espacio.", "No es necesario que hagas nada."], "ahora", resalta=1)
        br = ss(seg(t, .8, 1.05)) * (1 - .8 * ss(seg(t, 6.9, 7.5)))
        jx, jy = zumbido(t, tv)
        poner_tel(fr, lz.rgb(), 960 + jx, 560 + jy - x * 10, lerp(1130, 1210, x), yaw=4, pitch=40, roll=9, brillo=br,
                  sombra_k=(8, 14, 20, .6), resplandor=.38 * br)
        return fr
    return r


# ─────────────── historial ───────────────
HIST = [
    ("sec", "JUEVES 3 DE DICIEMBRE"),
    ("cab", "23:48 · Llamada entrante de Papá", "2 min 14 s · la atendió tu Presente"),
    ("izq", "Papá", "Chato… estoy en el hospital. Me duele el pecho. ¿Vienes?", .9, 2.9),
    ("der", "Tu Presente", "Ya voy, papá. Aguántame. Tomo el primer vuelo.", 3.2, 4.8),
    ("res", "Resumen que recibiste", "«Papá tuvo una revisión médica de rutina. Todo en orden.»", 5.2, 5.9),
    ("sec", "VIERNES 4 DE DICIEMBRE"),
    ("cab", "06:10 · Llamada entrante de Lucía", "4 min 02 s · la atendió tu Presente"),
    ("izq", "Lucía", "Papá se nos fue, Daniel. ¿Dónde estás?", 7.8, 9.4),
    ("der", "Tu Presente", "No alcanzo vuelo, Lucía. Lo siento mucho.", 9.7, 11.0),
    ("res", "Resumen que recibiste", "«Lucía está alterada: dale espacio.»", 11.4, 12.0),
]


@lru_cache(None)
def _hist_layout():
    lz = Lz(SW, SH)
    y = 200
    out = []
    for e in HIST:
        if e[0] == "sec":
            y += 36
            out.append((e, y, 0))
            y += 22
        elif e[0] == "cab":
            out.append((e, y, 86))
            y += 96
        else:
            ancho = SW - 150
            ls_ = lz.wrap(e[2], "r" if e[0] != "res" else "i", 21, ancho - 36)
            h = 44 + len(ls_) * 28 + 18
            out.append((e, y, h, ls_))
            y += h + 14
    return out


@pieza
def f_historial(P):
    fondo = foto("esc/puerta", 7, .68)
    A = P.audio
    A.add(s_ruido(P.d, 100, 1600, .007, seed=100), 0)
    A.add(s_tap(.07), .55)
    A.add(s_swoosh(.6, .03), 6.3)
    lay = _hist_layout()
    y_card2 = [y for e, y, *_ in lay if e[0] == "sec"][1]

    def pant(t):
        lz = app_lz(SW, SH, 1.1)
        sc = (y_card2 - 150) * eio(seg(t, 6.3, 7.5))
        for item in lay:
            e, y = item[0], item[1] - sc
            if y > SH + 40 or y + 300 < 120:
                continue
            if e[0] == "sec":
                lz.text(32, y, e[1], "sb", 15, rgba(GRIS), anchor="ls", track=2)
            elif e[0] == "cab":
                lz.rect(20, y, SW - 20, y + item[2], r=22, fill=rgba(PANEL))
                lz.text(40, y + 38, e[1], "sb", 20, CREMA, anchor="ls")
                lz.text(40, y + 68, e[2], "r", 16, rgba(GRIS), anchor="ls")
            else:
                h, ls_ = item[2], item[3]
                a = ss(seg(t, e[3] - .3, e[3]))
                if a <= 0:
                    continue
                x0 = 24 if e[0] != "der" else 126
                fill = {"izq": (52, 46, 40), "der": (78, 58, 34), "res": (30, 25, 21)}[e[0]]
                lz.rect(x0, y, x0 + SW - 150, y + h, r=22, fill=rgba(fill, a),
                        outline=rgba(AMBAR, a * .7) if e[0] == "res" else None, width=1.5)
                lz.text(x0 + 18, y + 32, e[1], "sb", 15, rgba(AMBAR_C if e[0] != "izq" else GRIS, a), anchor="ls")
                pal = " ".join(ls_).split(" ")
                n = int(round(len(pal) * seg(t, e[3], e[4])))
                k = 0
                for li, l in enumerate(ls_):
                    ws = l.split(" ")
                    vis = ws[:max(0, n - k)]
                    k += len(ws)
                    if vis:
                        f_ = "i" if e[0] == "res" else "r"
                        col = AMBAR_C if e[0] == "res" else CREMA
                        lz.text(x0 + 18, y + 64 + li * 28, " ".join(vis), f_, 21, rgba(col, a), anchor="ls")
        lz.rect(0, 0, SW, 160, fill=rgba(TINTA, .96))
        lz.text(40, 40, "19:06", "sb", 17, CREMA, anchor="ls")
        lz.text(34, 118, "‹", "l", 44, rgba(AMBAR), anchor="ls")
        lz.text(70, 114, "Historial con Papá", "sb", 28, CREMA, anchor="ls")
        lz.rect(24, 150, SW - 24, 151, fill=rgba(CREMA, .1))
        return lz.rgb()

    def r(t, f):
        fr, _ = kb(fondo, t / P.d, 1.08, 1.16, (.5, .5), (.46, .5))
        m = en_mano(t, 0.0, None, cx=1160, cy=700, alto=1340, seed=4.0, temblor=1.7, yaw=-6)
        poner_tel(fr, pant(t), **m, resplandor=.10)
        return fr
    return r


# ─────────────── timbre_papa: PRESENTE Legado llama ───────────────
QVIDRIO = [(575, 340), (698, 325), (840, 590), (712, 600)]


@pieza
def f_timbre_papa(P):
    A = P.audio
    A.add(s_ring(P.d - .25), .25)
    A.add(s_vibra(5, .5, .5, .12), .3)
    A.add(s_ruido(P.d, 100, 1600, .006, seed=110), 0)
    av = cara("ramon")
    fondo_llamada = np.asarray(av.resize((SW, SW)).resize((SW // 8, SW // 8)).resize((SW, SH)), np.float32) / 255
    fondo_llamada = cv2.GaussianBlur(fondo_llamada, (0, 0), 18) * .42
    corte = 2.1

    def pant(t):
        lz = Lz(SW, SH, (0, 0, 0))
        lz.im.paste(Image.fromarray(np.uint8(fondo_llamada * 255)).resize((SW * lz.k, SH * lz.k)), (0, 0))
        y = lerp(-140, 70, eo(seg(t, .4, .9)))
        lz.rect(20, y, SW - 20, y + 96, r=26, fill=rgba((52, 44, 38), .85))
        icono_app(lz, 36, y + 24, 46)
        lz.text(96, y + 42, "PRESENTE Legado", "sb", 19, CREMA, anchor="ls")
        lz.text(96, y + 72, "Tu papá sigue contigo. 30 días gratis.", "r", 17, rgba(CREMA2), anchor="ls")
        lz.text(SW / 2, 330, "Papá", "bahn_Light", 76, CREMA, anchor="ms")
        lz.text(SW / 2, 372, "videollamada · PRESENTE Legado", "r", 19, rgba(CREMA2), anchor="ms")
        for k in range(3):
            ph = (t * .7 + k / 3) % 1
            lz.circ(SW / 2, 580, 118 + ph * 70, outline=rgba(AMBAR, (1 - ph) * .6), width=3)
        lz.foto(av, SW / 2 - 112, 468, 224, 224, circulo=True)
        for x, col, ic, et in ((130, TERRA, "", "Rechazar"), (370, AMBAR, "", "Contestar")):
            pul = 1 + .05 * math.sin(t * 6) if et == "Contestar" else 1
            lz.circ(x, 900, 42 * pul, fill=rgba(col))
            lz.text(x, 900, ic, "ico", 34, rgba((255, 255, 255)), anchor="mm")
            lz.text(x, 975, et, "r", 18, rgba(CREMA2), anchor="ms")
        return lz.rgb()

    def r(t, f):
        if t < corte:
            fr, M = kb(foto("bg/telefono_puerta"), t / corte, 1.04, 1.1, (.55, .45), (.53, .46))
            q = mapa(M, QVIDRIO)
            luz(fr, q, (1, .78, .5), blur=30, fuerza=.16 + .1 * abs(math.sin(t * 3.2)), crece=.9)
            return fr
        x = seg(t, corte, P.d)
        fr, _ = kb(foto("esc/puerta", 8, .62), x, 1.1, 1.16, (.45, .5), (.42, .5))
        m = en_mano(t, -2, None, cx=1120, cy=560, alto=1150, seed=6.0, temblor=1.3, yaw=-7)
        jx, jy = zumbido((t - .3) % 1.0, [(0, .5)], 2.0)
        m["cx"] += jx
        m["cy"] += jy
        poner_tel(fr, pant(t), **m, resplandor=.14)
        return fr
    return r


# ─────────────── notif_final: seis meses después ───────────────
@pieza
def f_notif_final(P):
    fondo = foto("bg/oficina_dia", 10, .9)
    A = P.audio
    A.add(s_ruido(P.d, 70, 900, .006, seed=120), 0)
    A.add(s_vibra(2), 1.0)
    A.add(s_swoosh(.4, .05), 8.6)
    tv = _tramos(1.0)

    def r(t, f):
        fr, _ = kb(fondo, t / P.d, 1.12, 1.2, (.42, .48), (.39, .46))
        lz = bloqueo("11:20", "domingo, 20 de junio", "esc/carretera", .45)
        enc, sal = eo(seg(t, 1.15, 1.6)), eio(seg(t, 8.6, 9.05))
        y = lerp(-320, 300, enc)
        if sal < 1:
            noti(lz, 20 + sal * 560, y, SW - 40, "Llamada con Papá completada",
                 ["Hoy 10:42 · 34 min", "Ánimo de Papá 97 % · Tu ánimo 91 %", "Resumen: hablaron del bebé y del reloj del abuelo."],
                 "ahora", a=1 - sal * .5, app="PRESENTE LEGADO", resalta=1)
        if 8.2 < t < 9.2:
            toque(lz, 150 + sal * 330, y + 160, seg(t, 8.2, 8.4), ven(t, 8.2, 9.2, .12, .25))
        br = ss(seg(t, 1.0, 1.3)) * (1 - .72 * ss(seg(t, 10.9, 11.6)))
        jx, jy = zumbido(t, tv)
        poner_tel(fr, lz.rgb(), 910 + jx - t * 3, 585 + jy, lerp(1150, 1210, t / P.d), yaw=6, pitch=38, roll=12,
                  brillo=br, sombra_k=(-10, 18, 22, .5), resplandor=.06)
        return fr
    return r


# ─────────────── final: los dos teléfonos siguen platicando ───────────────
QTEL = [[(440, 628), (585, 615), (598, 672), (452, 684)], [(538, 612), (690, 604), (696, 655), (548, 664)]]


@pieza
def f_final(P):
    A = P.audio
    for i in range(14):
        A.add(s_tick(1.0 if i % 2 == 0 else .82, .03), .4 + i)
    for i in range(7):
        A.add(s_tick(.62, .02), .9 + i * 2)
    for k in range(5):
        A.add(s_ruido(2.3, 300, 2600, .006, seed=130 + k, am=5) * np.float32([[1.3, .7] if k % 2 else [.7, 1.3]]),
              .4 + k * 2.6)
    fin_img = 14.0

    def r(t, f):
        fr = np.zeros((H, W, 3), np.float32)
        if t < fin_img:
            x = seg(t, 0, fin_img)
            fr, M = kb(foto("bg/dos_telefonos", 0, .95), x, 1.0, 1.36, (.5, .5), (.42, .76))
            habla = int(t / 2.6) % 2
            for i, qq in enumerate(QTEL):
                q = mapa(M, qq)
                act = .5 + .5 * abs(math.sin(t * 5 + i)) if i == habla else .25
                luz(fr, q, (.9, .75, .55), blur=26 * (M[0, 0] / 1.4), fuerza=.16 * act, crece=1.0)
            a = ven(t, 2.4, 12.4, .8, .8)
            if a > 0:
                for i, (qq, nom) in enumerate(zip(QTEL, ("Papá", "Chato"))):
                    q = mapa(M, qq)
                    cx_, cy_ = q.mean(0)
                    esc = M[0, 0] / 1.406
                    card = Lz(220, 64)
                    card.rect(0, 0, 220, 64, r=32, fill=rgba((40, 34, 29), .66))
                    card.circ(30, 32, 7, fill=rgba(AMBAR))
                    card.text(48, 41, nom, "sb", 22, CREMA, anchor="ls")
                    ondas(card, 128, 32, 72, 30, t + i, 1.0 if i == int(t / 2.6) % 2 else .15, n=9, a=.9, seed=i)
                    tarjeta_vidrio(fr, card, cx_ + (-80 if i == 0 else 80) * esc, cy_ - 120 * esc, op=a, escala=min(1.3, .8 * esc))
                s_ = int(11527 + t)
                lz = Lz(500, 50)
                lz.text(250, 34, f"en llamada · {s_ // 3600} h {s_ % 3600 // 60:02d} min {s_ % 60:02d} s", "r", 22,
                        rgba(CREMA2, a * .9), anchor="ms")
                p = mapa(M, [(565, 545)])[0]
                pegar(fr, lz.out(), p[0] - 250, p[1] - 150 * M[0, 0] / 1.406)
            fr *= 1 - ss(seg(t, 12.0, 13.8))
        lz = Lz(1700, 520)
        lz.text(850, 120, "LogIA presenta", "sl", 30, rgba(CREMA2, ven(t, 14.3, 21.6, .8, .7)), anchor="ms", track=10)
        a2 = ven(t, 14.8, 21.6, 1.0, .7)
        lz.text(850, 230, "LLAMADA DE DOMINGO", "l", 76, rgba(CREMA, a2), anchor="ms", track=26)
        lz.rect(850 - 230, 270, 850 + 230, 272, fill=rgba(AMBAR, a2 * .8))
        a3 = ven(t, 16.6, 21.6, .9, .7)
        lz.text(850, 380, "Una historia de ficción.", "r", 28, rgba(GRIS, a3), anchor="ms")
        lz.text(850, 424, "Video y voces hechos con inteligencia artificial.", "r", 28, rgba(GRIS, a3), anchor="ms")
        pegar(fr, lz.out(), W / 2 - 850, H / 2 - 260)
        return fr
    return r


# ═════════════════════════════ videollamada sobre los clips de Flow ═════════════════════════════
LLAMADA_CFG = {   # contacto que ve quien recibe, la cara de quien recibe (miniatura), segundo del contador al empezar
    "scene-004": ("Chato", "ramon_taller", 41, "PRESENTE"),
    "scene-006": ("Chato", "ramon_taller", 59, "PRESENTE"),
    "scene-042": ("Mariana", "carmen", 20, "PRESENTE"),
    "scene-044": ("Mariana", "carmen", 38, "PRESENTE"),
    "scene-052": ("Chato", "ramon_noche", 425, "PRESENTE"),
    "scene-061": ("Chato", "ramon_cama", 9, "PRESENTE"),
    "scene-076": ("Papá", "daniel", 4, "PRESENTE Legado"),
    "scene-078": ("Papá", "daniel", 22, "PRESENTE Legado"),
}


def _probe(ruta):
    out = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                          "stream=r_frame_rate,nb_read_packets", "-of", "csv=p=0", ruta], capture_output=True, text=True,
                         check=True).stdout.strip().split(",")
    num, den = out[0].split("/")
    return float(num) / float(den), int(out[1])


@lru_cache(None)
def _marco_llamada():
    """Capa fija: degradados arriba/abajo y esquinas redondeadas."""
    a = np.zeros((H, W, 4), np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None]
    g = np.clip(1 - yy / 230, 0, 1) ** 1.6 * .62 + np.clip((yy - (H - 260)) / 260, 0, 1) ** 1.6 * .55
    a[..., 3] = np.broadcast_to(g, (H, W))
    m = Image.new("L", (W * 2, H * 2), 255)
    ImageDraw.Draw(m).rounded_rectangle([14, 14, W * 2 - 15, H * 2 - 15], radius=84, fill=0)
    m = np.asarray(m.resize((W, H), Image.LANCZOS), np.float32) / 255
    a[..., 3] = np.maximum(a[..., 3], m)
    return a


def llamada(scene):
    if scene not in LLAMADA_CFG:
        raise SystemExit(f"{scene}: no es un plano de tipo llamada ({', '.join(LLAMADA_CFG)})")
    contacto, quien, s0, marca = LLAMADA_CFG[scene]
    src = os.path.join(MEDIOS, scene + ".mp4")
    crudo = os.path.join(PREV, "originales", scene + "_crudo.mp4")
    os.makedirs(os.path.dirname(crudo), exist_ok=True)
    if not os.path.exists(crudo):
        if not os.path.exists(src):
            raise SystemExit(f"falta {src}")
        import shutil
        shutil.copy2(src, crudo)
    fps, n = _probe(crudo)
    yo = cara(quien)
    yo_arr = np.asarray(yo.resize((350, 350), Image.LANCZOS), np.float32) / 255
    marco = _marco_llamada()
    dec = subprocess.Popen([FF, "-v", "error", "-i", crudo, "-f", "rawvideo", "-pix_fmt", "rgb24", "-vf",
                            f"scale={W}:{H}:flags=lanczos", "-"], stdout=subprocess.PIPE)
    tmp = os.path.join(CACHE, scene + "_llamada.mp4")
    os.makedirs(CACHE, exist_ok=True)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{fps}",
                            "-i", "-", "-i", crudo, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", tmp],
                           stdin=subprocess.PIPE)
    PW, PH = 330, 196
    f = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        t = f / fps
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        fr = fr * (1 - marco[..., 3:4])
        lz = Lz(W, 200, k=1)
        lz.text(86, 92, contacto, "sb", 44, CREMA, anchor="ls")
        lz.circ(96, 128, 6 + .8 * math.sin(t * 4), fill=rgba(AMBAR, .95))
        s_ = int(s0 + t)
        lz.text(112, 135, f"{marca} · videollamada · {s_ // 60:02d}:{s_ % 60:02d}", "r", 21, rgba(CREMA2, .92), anchor="ls")
        lz.logo(W - 250, 84, 13, a=.75, tam=15)
        pegar(fr, lz.out(), 0, 0)
        # botones (vidrio)
        bt = Lz(360, 100)
        for i, (ic, col) in enumerate((("", (60, 54, 48)), ("", TERRA), ("", (60, 54, 48)))):
            bt.circ(60 + i * 120, 50, 38, fill=rgba(col, .78))
            bt.text(60 + i * 120, 50, ic, "ico", 30, rgba((250, 246, 238), .95), anchor="mm")
        pegar_quad(fr, bt.out(), [(W / 2 - 180, H - 140), (W / 2 + 180, H - 140), (W / 2 + 180, H - 40), (W / 2 - 180, H - 40)],
                   vidrio=10)
        # miniatura de quien recibe
        ox = int(10 + 8 * math.sin(t * .35))
        oy = int(80 + 6 * math.cos(t * .3))
        mini = yo_arr[oy:oy + PH, ox:ox + PW]
        pz = Lz(PW + 8, PH + 8)
        pz.rect(0, 0, PW + 8, PH + 8, r=24, fill=rgba((250, 244, 232), .9))
        cap = pz.out()
        mm = Lz(PW, PH)
        mm.rect(0, 0, PW, PH, r=20, fill=(255, 255, 255, 255))
        mk = mm.out()[..., 3:4]
        x0, y0 = W - PW - 70, H - PH - 150
        sombra(fr, np.float32([(x0, y0), (x0 + PW, y0), (x0 + PW, y0 + PH), (x0, y0 + PH)]), 0, 14, 22, .45)
        pegar(fr, cap, x0 - 4, y0 - 4)
        reg = fr[y0:y0 + PH, x0:x0 + PW]
        fr[y0:y0 + PH, x0:x0 + PW] = reg * (1 - mk) + mini * mk
        np.clip(fr, 0, 1, out=fr)
        enc.stdin.write((fr * 255 + .5).astype(np.uint8).tobytes())
        f += 1
    dec.wait()
    enc.stdin.close()
    if enc.wait() != 0:
        raise SystemExit(f"ffmpeg falló en {scene}")
    import shutil
    shutil.move(tmp, src)
    print(f"  {scene}: {f} cuadros ({n} en el original) a {fps:g} fps → {src}", flush=True)


# ═════════════════════════════ orquestación ═════════════════════════════
def planos_ui():
    """{ui_id: (scene, d)} según guion.PLANOS."""
    sys.path.insert(0, AQUI)
    import importlib
    import guion
    importlib.reload(guion)
    return {p["ui"]: (f"scene-{i + 1:03d}", p["d"]) for i, p in enumerate(guion.PLANOS) if p["tipo"] == "ui"}


def render_pieza(uid):
    import time
    t0 = time.time()
    scene, d = planos_ui()[uid]
    P = Pieza(uid, d)
    r = PIEZAS[uid](P)
    escribir(P, r, os.path.join(MEDIOS, scene + ".mp4"))
    return uid, scene, time.time() - t0


def cuadro(uid, t):
    scene, d = planos_ui()[uid]
    P = Pieza(uid, d)
    r = PIEZAS[uid](P)
    fr = pelicula(r(t, int(t * FPS)), int(t * FPS), P.grano, P.vig)
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f"cuadro_{uid}_{t:g}.jpg")
    Image.fromarray((fr * 255 + .5).astype(np.uint8)).save(p, quality=90)
    print(p)


def duracion(ruta):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration:stream=codec_type,duration", "-of",
                          "json", ruta], capture_output=True, text=True).stdout
    import json
    j = json.loads(out)
    v = next((float(s["duration"]) for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((float(s["duration"]) for s in j["streams"] if s["codec_type"] == "audio"), None)
    return float(j["format"]["duration"]), v, a


def hoja(uids=None, llamadas=()):
    pl = planos_ui()
    uids = uids or list(pl)
    celdas = []
    for u in uids:
        scene, d = pl[u]
        for fr_ in (1 / 3, 2 / 3):
            celdas.append((f"{scene} {u} @{d * fr_:.1f}s", os.path.join(MEDIOS, scene + ".mp4"), d * fr_))
    for s in llamadas:
        p = os.path.join(MEDIOS, s + ".mp4")
        if os.path.exists(p):
            dd = duracion(p)[0]
            celdas.append((f"{s} llamada @{dd / 2:.1f}s", p, dd / 2))
    cw, ch, col = 384, 216, 6
    filas = (len(celdas) + col - 1) // col
    sheet = Image.new("RGB", (cw * col, (ch + 24) * filas), (12, 12, 12))
    d = ImageDraw.Draw(sheet)
    for i, (et, p, t) in enumerate(celdas):
        out = subprocess.run([FF, "-v", "error", "-ss", f"{t:.2f}", "-i", p, "-frames:v", "1", "-vf", f"scale={cw}:{ch}",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        x, y = (i % col) * cw, (i // col) * (ch + 24)
        if out:
            sheet.paste(Image.open(io.BytesIO(out)).convert("RGB"), (x, y))
        d.text((x + 4, y + ch + 4), et, fill=(255, 220, 120), font=F("r", 15))
    p = os.path.join(PREV, "ui_hoja.jpg")
    sheet.save(p, quality=88)
    print("hoja:", p)


def main(args):
    if args and args[0] == "voces":
        for k in VOCES:
            asegurar_voz(k)
        print("créditos gastados ahora:", sum(c for _, c in GASTO))
        return
    if args and args[0] == "llamada":
        for s in args[1:] or list(LLAMADA_CFG):
            llamada(s)
        return
    if args and args[0] == "hoja":
        hoja(None, list(LLAMADA_CFG))
        return
    if args and args[0] == "cuadro":
        for t in args[2:]:
            cuadro(args[1], float(t))
        return
    pl = planos_ui()
    uids = args or list(pl)
    falta = [u for u in uids if u not in PIEZAS or u not in pl]
    if falta:
        raise SystemExit(f"piezas desconocidas: {falta}")
    for k in VOCES:      # voces antes de abrir procesos (ninguna se genera dos veces)
        asegurar_voz(k)
    from multiprocessing import Pool
    with Pool(min(int(os.environ.get("UI_PROCESOS", "3")), len(uids))) as pool:
        for uid, scene, seg_ in pool.imap_unordered(render_pieza, sorted(uids, key=lambda u: -pl[u][1])):
            print(f"  ✓ {uid} → {scene}.mp4 ({seg_:.0f} s)", flush=True)
    print("\nduraciones (ffprobe):")
    for u in uids:
        scene, d = pl[u]
        fmt, v, a = duracion(os.path.join(MEDIOS, scene + ".mp4"))
        print(f"  {scene} {u:15s} d={d:>4}  video={v:.3f}  audio={a:.3f}  ok={abs(v - d) < 1e-3}")
    if not args:
        hoja(None, list(LLAMADA_CFG))


if __name__ == "__main__":
    for _s in (sys.stdout, sys.stderr):
        _s.reconfigure(encoding="utf-8", errors="replace")
    main(sys.argv[1:])
