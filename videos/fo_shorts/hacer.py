"""Shorts verticales de Radio Yermo recortados de los largos (26-nov-2026).

Cada Short = un puesto completo del largo (voz + música + imagen del MASTER, sin rehacer nada), en 1080x1920:
fondo = el mismo video ampliado, desenfocado y oscurecido; arriba el gancho en verde Pip-Boy; en medio el video 16:9 entero;
abajo «video completo en Radio Yermo» con el título del largo. Sin subtítulos quemados (R13).

    python videos/fo_shorts/hacer.py            # los 3
    python videos/fo_shorts/hacer.py gary       # uno
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"

VERDE = (40, 255, 70)
VERDE_T = (120, 235, 120)
BLANCO = (238, 244, 232)
FONDO = (6, 28, 10)
FB = "C:/Windows/Fonts/bahnschrift.ttf"
FM = "C:/Windows/Fonts/consolab.ttf"

W, H = 1080, 1920
VY = 680            # y del video 16:9 (1080x608)

SHORTS = {
    "gary": dict(
        largo="fo_refugios_25", t0=869.48, t1=941.10,   # sin «Número quince» ni la cola del Refugio 81 (FO4)
        juego="FALLOUT 3 · REFUGIO 108",
        gancho=["EL REFUGIO DONDE", "TODOS SE LLAMAN", "GARY"],
        completo="Los 25 refugios más MALVADOS de Fallout", id_largo="XU_OkLlxV7o",
        titulo="Fallout 3: el refugio de puros GARY #Shorts",
        desc="El Refugio 108 de Fallout 3: un supervisor con cáncer terminal, un generador programado para fallar y alguien "
             "clonando en serie a un hombre llamado Gary. Hoy solo quedan Garys, y solo dicen una palabra.",
        tags=["refugio 108", "gary fallout", "fallout 3", "vault 108", "refugios fallout"]),
    "ruzka": dict(
        largo="fo_enemigos_ocultos", t0=209.45, t1=261.80,   # sin «Número doce» ni la cola del Red Death
        juego="FALLOUT 3 · POINT LOOKOUT",
        gancho=["LA OSA DEL CIRCO", "QUE SIGUE JUGANDO", "200 AÑOS DESPUÉS"],
        completo="15 ENEMIGOS ocultos de Fallout que casi nadie vio", id_largo="f2zKynItV6U",
        titulo="Fallout 3: la osa de circo OLVIDADA #Shorts",
        desc="Ruzka, la osa maravilla del circo de Point Lookout, sigue en su guarida sin marcador doscientos años después: "
             "más grande que un yao guai normal y jugando con su pelota roja.",
        tags=["ruzka", "point lookout", "fallout 3", "yao guai", "enemigos ocultos fallout"]),
    "cura81": dict(
        largo="fo_nunca_f4", t0=517.05, t1=562.35,   # sin «Número cinco» ni la cola del Instituto
        juego="FALLOUT 4 · REFUGIO 81",
        gancho=["SI TE QUEDAS", "ESTA CURA,", "UN NIÑO MUERE"],
        completo="Las 15 cosas que NUNCA debes hacer en Fallout 4", id_largo="z_YrsxSbIFg",
        titulo="Fallout 4: NUNCA te quedes esta cura #Shorts",
        desc="En la sección secreta del Refugio 81, Curie solo puede hacer UNA dosis de la cura. Si te la quedas, Austin muere… "
             "¿y qué ganas? Diez puntos de vida máxima.",
        tags=["refugio 81", "austin fallout 4", "curie fallout 4", "fallout 4", "fallout 4 en español"]),
}


def f(ruta, tam):
    return ImageFont.truetype(ruta, tam)


def ancho(d, txt, fnt):
    b = d.textbbox((0, 0), txt, font=fnt)
    return b[2] - b[0]


def capa(s, ruta):
    """PNG transparente 1080x1920 con gancho arriba y «video completo» abajo."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # --- arriba: placa del juego + gancho en 3 renglones
    fj = f(FM, 40)
    txt = s["juego"]
    w = ancho(d, txt, fj)
    x0, y0 = (W - w) // 2 - 28, 150
    d.rounded_rectangle((x0, y0, x0 + w + 56, y0 + 66), 10, fill=FONDO + (225,), outline=VERDE + (255,), width=3)
    d.text((W // 2, y0 + 33), txt, font=fj, fill=VERDE, anchor="mm")
    y = 262
    for i, linea in enumerate(s["gancho"]):
        tam = 112
        fg = f(FB, tam)
        while ancho(d, linea, fg) > W - 90:
            tam -= 4
            fg = f(FB, tam)
        color = VERDE if i == len(s["gancho"]) - 1 else BLANCO
        d.text((W // 2, y), linea, font=fg, fill=color, anchor="mt", stroke_width=7, stroke_fill=(0, 0, 0))
        y += int(tam * 1.08)
    # --- marco del video
    d.rectangle((0, VY - 6, W, VY - 1), fill=VERDE + (255,))
    d.rectangle((0, VY + 608, W, VY + 613), fill=VERDE + (255,))
    # --- abajo: video completo
    fy = VY + 608 + 90
    fc = f(FM, 42)
    txt = "VIDEO COMPLETO EN EL CANAL"
    w = ancho(d, txt, fc)
    x = (W - w) // 2 + 22
    d.polygon([(x - 44, fy + 4), (x - 44, fy + 36), (x - 16, fy + 20)], fill=VERDE)      # ▶ dibujado (Consolas no lo trae)
    d.text((x, fy), txt, font=fc, fill=VERDE, anchor="lt")
    tam = 50
    ft = f(FB, tam)
    while ancho(d, s["completo"], ft) > W - 110:
        tam -= 2
        ft = f(FB, tam)
    d.text((W // 2, fy + 70), s["completo"], font=ft, fill=BLANCO, anchor="mt", stroke_width=4, stroke_fill=(0, 0, 0))
    fr = f(FB, 64)
    d.text((W // 2, fy + 170), "@RadioYermo", font=fr, fill=VERDE, anchor="mt", stroke_width=5, stroke_fill=(0, 0, 0))
    im.save(ruta)


def srt(s, ruta_srt, ruta_out):
    """Corta el .srt del largo al tramo y lo corre a 0."""
    def t(x):
        h, m, r = x.split(":"); sec, ms = r.split(","); return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000

    def fmt(x):
        x = max(0.0, x); h = int(x // 3600); m = int(x % 3600 // 60); sec = x % 60
        return f"{h:02d}:{m:02d}:{int(sec):02d},{int(round((sec - int(sec)) * 1000)):03d}"
    out, n = [], 0
    for blk in open(ruta_srt, encoding="utf-8").read().strip().split("\n\n"):
        l = blk.splitlines()
        if len(l) < 3:
            continue
        a, b = [t(x.strip()) for x in l[1].split("-->")]
        if a >= s["t0"] - 0.2 and a < s["t1"]:
            n += 1
            out.append(f"{n}\n{fmt(a - s['t0'])} --> {fmt(min(b, s['t1']) - s['t0'])}\n" + "\n".join(l[2:]))
    open(ruta_out, "w", encoding="utf-8").write("\n\n".join(out) + "\n")


def hacer(nombre):
    s = SHORTS[nombre]
    carpeta = os.path.join(RAIZ, "videos", "fo_short_" + nombre)
    os.makedirs(os.path.join(carpeta, "salida"), exist_ok=True)
    master = os.path.join(RAIZ, "videos", s["largo"], "salida", s["largo"] + "_MASTER.mp4")
    png = os.path.join(carpeta, "capa.png")
    capa(s, png)
    dur = s["t1"] - s["t0"]
    out = os.path.join(carpeta, "salida", f"fo_short_{nombre}_MASTER.mp4")
    fil = (f"[0:v]split=2[a][b];"
           f"[a]scale=-2:{H},crop={W}:{H},boxblur=28:2,eq=brightness=-0.22:saturation=0.8[bg];"
           f"[b]scale={W}:608[fg];"
           f"[bg][fg]overlay=0:{VY}[v1];[v1][1:v]overlay=0:0,format=yuv420p[v];"
           f"[0:a]afade=t=in:d=0.06,afade=t=out:st={dur - 0.7:.2f}:d=0.7[aout]")
    cmd = [FF, "-y", "-v", "error", "-ss", f"{s['t0']:.2f}", "-t", f"{dur:.2f}", "-i", master, "-i", png,
           "-filter_complex", fil, "-map", "[v]", "-map", "[aout]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    srt(s, os.path.join(RAIZ, "videos", s["largo"], "salida", s["largo"] + ".srt"),
        os.path.join(carpeta, "salida", f"fo_short_{nombre}.srt"))
    meta = dict(titulo=s["titulo"],
                descripcion=s["desc"] + f"\n\nEl video completo, «{s['completo']}»: https://youtu.be/{s['id_largo']}\n\n"
                            "Esto es Radio Yermo: listas, secretos y lore de Fallout en español. Suscríbete y sintoniza.\n\n"
                            "#shorts #fallout #radioyermo",
                etiquetas=s["tags"] + ["fallout", "fallout en español", "radio yermo", "shorts"],
                categoria=20, idioma="es", idioma_audio="es", subtitulos=f"salida/fo_short_{nombre}.srt",
                largo=s["largo"], tramo=[s["t0"], s["t1"]])
    json.dump(meta, open(os.path.join(carpeta, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK", nombre, f"{dur:.1f}s", out)


if __name__ == "__main__":
    for n in (sys.argv[1:] or list(SHORTS)):
        hacer(n)
