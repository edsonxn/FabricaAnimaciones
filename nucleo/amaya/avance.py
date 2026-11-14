# -*- coding: utf-8 -*-
"""Avance de un trabajo del Estudio de Amaya: le llega a ella como MENSAJE en el chat de su app (10-nov-2026).

    python nucleo/amaya/avance.py <trabajo> "🎙️ Grabando la voz de Hope"
    python nucleo/amaya/avance.py <trabajo> "🎨 ¡Mira tus escenas!" --imagen videos/amaya_x/previews/esc_1.jpg
    python nucleo/amaya/avance.py <trabajo> "🧸 Tus personajes" --imagen a.png b.png c.png      (2-9 → una HOJA)
    python nucleo/amaya/avance.py <trabajo> "🎬 ¡Ya quedó!" --voz "¡Amaya, tu video ya está listo! Corre a verlo."
    python nucleo/amaya/avance.py <trabajo> --listo

Lo corre el Claude que produce el video (nucleo/amaya/produccion.md, regla 7). Escribe una línea en
amaya_estudio/trabajos/<trabajo>.avances.jsonl; el servidor (nucleo/amaya/servidor.py) la convierte en mensaje del chat.
- --imagen: solo archivos de videos/ o amaya_estudio/ (nada más de la PC sale al teléfono). Varias = hoja con cuadrícula.
- --voz: nota de voz CORTA (≤ 160 letras) con la voz de SU video (ElevenLabs turbo, ≈ 80 créditos). Tope por video:
  limites.audios_por_video de amaya_estudio/config.json (5 si no dice). Si se pasa o falla, el avance sale sin audio.
"""
import json
import os
import re
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.dirname(AQUI)
RAIZ = os.path.dirname(NUCLEO)
DATOS = os.path.join(RAIZ, "amaya_estudio")
TRABAJOS = os.path.join(DATOS, "trabajos")
MEDIA = os.path.join(TRABAJOS, "media")
PERMITIDAS = [os.path.normcase(os.path.abspath(b)) for b in (os.path.join(RAIZ, "videos"), DATOS)]   # cada video es junction a E: → abspath, no realpath
MAX_VOZ = 160
FONDO = (26, 16, 51)          # el morado de la app


def leer_json(p, defecto=None):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defecto


def lineas(tid):
    out = []
    try:
        with open(os.path.join(TRABAJOS, f"{tid}.avances.jsonl"), encoding="utf-8") as f:
            for ln in f:
                try:
                    out.append(json.loads(ln))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


def ruta_valida(p):
    a = os.path.normcase(os.path.abspath(os.path.join(RAIZ, p)))      # abspath resuelve los «..»
    return a if any(a.startswith(b + os.sep) for b in PERMITIDAS) and os.path.isfile(a) else None


def hoja(imgs):
    """1 imagen → tal cual (≤ 1280); 2-9 → cuadrícula sobre el morado de la app, con esquinas redondeadas."""
    from PIL import Image, ImageDraw
    ims = []
    for p in imgs:
        try:
            im = Image.open(p)
            im.load()
            ims.append(im.convert("RGB"))
        except Exception as e:
            print("no es imagen:", os.path.basename(p), repr(e)[:80])
    if not ims:
        return None
    if len(ims) == 1:
        im = ims[0]
        im.thumbnail((1280, 1280))
        return im
    ims = ims[:9]
    n = len(ims)
    cols = 2 if n <= 4 else 3
    filas = (n + cols - 1) // cols
    vertical = sum(i.height > i.width for i in ims) > n / 2
    cw, ch = (360, 640) if vertical else (640, 360)
    if cols == 3:
        cw, ch = int(cw * 0.8), int(ch * 0.8)
    m = 14
    lienzo = Image.new("RGB", (cols * cw + (cols + 1) * m, filas * ch + (filas + 1) * m), FONDO)
    masc = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(masc).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=18, fill=255)
    for k, im in enumerate(ims):
        esc = max(cw / im.width, ch / im.height)          # llenar la celda y recortar al centro
        im = im.resize((max(cw, round(im.width * esc)), max(ch, round(im.height * esc))), Image.LANCZOS)
        x0, y0 = (im.width - cw) // 2, (im.height - ch) // 2
        im = im.crop((x0, y0, x0 + cw, y0 + ch))
        f, c = divmod(k, cols)
        lienzo.paste(im, (m + c * (cw + m), m + f * (ch + m)), masc)
    return lienzo


def voz_de(tid):
    t = leer_json(os.path.join(TRABAJOS, f"{tid}.json"), {}) or {}
    cfg = leer_json(os.path.join(DATOS, "config.json"), {}) or {}
    return (t.get("ficha") or {}).get("voz") or cfg.get("voz_avances") or ""


def tope_audios():
    cfg = leer_json(os.path.join(DATOS, "config.json"), {}) or {}
    return int((cfg.get("limites") or {}).get("audios_por_video", 5))


def hablar(tid, texto, base):
    texto = re.sub(r"\s+", " ", re.sub(r"\[(?:whispers?|excited|shouts?)[^\]]*\]|[<>{}]", "", texto)).strip()[:MAX_VOZ]
    if not texto:
        return None, None
    usados = sum(1 for a in lineas(tid) if a.get("audio"))
    if usados >= tope_audios():
        print(f"sin audio: ya van {usados} notas de voz en este video (tope {tope_audios()})")
        return None, None
    vid = voz_de(tid)
    if not vid:
        print("sin audio: este trabajo no tiene voz elegida")
        return None, None
    sys.modules.setdefault("config", None)              # tts_eleven sin video activo
    sys.path.insert(0, NUCLEO)
    try:
        import tts_eleven as T
        r = T.post(f"text-to-speech/{vid}?output_format=mp3_44100_64",
                   json={"text": texto, "model_id": "eleven_v4_turbo",
                         "voice_settings": {"stability": 0.45, "similarity_boost": 0.8}}, timeout=60)
    except Exception as e:
        print("sin audio: ElevenLabs falló", repr(e)[:120])
        return None, None
    if r.status_code != 200:
        print("sin audio: ElevenLabs", r.status_code, r.text[:160])
        return None, None
    nombre = base + ".mp3"
    with open(os.path.join(MEDIA, nombre), "wb") as f:
        f.write(r.content)
    return nombre, texto


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    tid = args.pop(0)
    if not re.match(r"^[A-Za-z0-9_-]{1,40}$", tid):
        sys.exit("trabajo inválido")
    os.makedirs(MEDIA, exist_ok=True)
    if args == ["--listo"]:
        linea = {"t": time.time(), "listo": True}
    else:
        texto, imgs, dice, modo = [], [], "", None
        for a in args:
            if a in ("--imagen", "--imagenes"):
                modo = "img"
            elif a == "--voz":
                modo = "voz"
            elif modo == "img":
                imgs.append(a)
            elif modo == "voz":
                dice = (dice + " " + a).strip()
            else:
                texto.append(a)
        linea = {"t": time.time(), "txt": " ".join(texto).strip()[:200]}
        base = f"{tid}_{int(time.time() * 1000) % 10 ** 9}"
        if imgs:
            buenas = [p for p in (ruta_valida(x) for x in imgs) if p]
            for x in imgs:
                if not ruta_valida(x):
                    print("imagen rechazada (solo de videos/ o amaya_estudio/):", x)
            im = hoja(buenas) if buenas else None
            if im:
                im.save(os.path.join(MEDIA, base + ".jpg"), "JPEG", quality=86)
                mini = im.copy()
                mini.thumbnail((720, 720))
                mini.save(os.path.join(MEDIA, base + "_mini.jpg"), "JPEG", quality=80)
                linea.update(img=base + ".jpg", mini=base + "_mini.jpg", n_img=len(buenas))
        if dice:
            nombre, dicho = hablar(tid, dice, base)
            if nombre:
                linea.update(audio=nombre, dice=dicho)
        if not (linea["txt"] or linea.get("img") or linea.get("audio")):
            sys.exit("avance vacío: nada que mandar")
    with open(os.path.join(TRABAJOS, f"{tid}.avances.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    print("avance anotado:", linea.get("txt", "listo"), "· imagen" if linea.get("img") else "", "· audio" if linea.get("audio") else "")


if __name__ == "__main__":
    main()
