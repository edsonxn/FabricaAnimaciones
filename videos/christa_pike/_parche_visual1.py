# -*- coding: utf-8 -*-
"""Parche: puntos de entrada/salida de clips (según cortes detectados), retrato de Colleen limpio, sombra inferior y mapa con nombres."""


def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:90]
    return s.replace(old, new, 1)


a = open('tomas_a.py', encoding='utf-8').read()
a = rep(a, 'ini=187.8, fin=191.0,', 'ini=187.95, fin=190.7,')
a = rep(a, 'ini=191.0, fin=193.6,', 'ini=191.0, fin=192.6,')
a = rep(a, 'ini=10.4, fin=16.8,', 'ini=10.4, fin=16.4,')
a = rep(a, 'A(G, 4, "nadie") - 0.1, W / 2, 560, 96)', 'A(G, 4, "nadie") - 0.1, 500, 560, 96)')
a = rep(a, 'sp = pola("pike_ficha_usuario", 900, 0.78, (0.5, 0.45), lado=1200)', 'sp = pola("pike_ficha_usuario", 780, 0.78, (0.5, 0.45), lado=1200)')
a = rep(a, 'lerp(420, 500, u)', 'lerp(340, 450, u)')
a = rep(a, 'W / 2, 935, 82)', 'W / 2, 960, 82)')
a = rep(a, 'F_arch("wbir_asesinato_1995", ini=22.0, fin=26.0, tono=SEP, sat=0.7, alto=880)', 'F_clip("wbir_2020", ini=66.8, fin=70.3, z0=1.0, z1=1.1, tono=SEP, sat=0.7)')
a = rep(a, 'F_arch("wbir_asesinato_1995", ini=24.9, fin=27.0, tono=SEP, sat=0.8, alto=900)', 'F_clip("wbir_2020", ini=63.6, fin=66.5, z0=1.0, z1=1.08, tono=SEP, sat=0.8)')
a = rep(a, 'F_arch("wbir_asesinato_1995", ini=0.2, fin=6.6, tono=(1.0, 0.95, 0.9), alto=920)', 'F_clip("wbir_2020", ini=70.7, fin=72.9, z0=1.0, z1=1.1, c0=(0.5, 0.45), c1=(0.5, 0.45), tono=(1.0, 0.95, 0.9))')
a = rep(a, 'F_clip("france24", ini=42.0, fin=45.8, z0=1.0, z1=1.1, c0=(0.42, 0.5), c1=(0.46, 0.5))', 'F_clip("wbir_cronologia", ini=301.3, fin=304.7, z0=1.0, z1=1.1, c0=(0.5, 0.45), c1=(0.5, 0.45))')
a = rep(a, 'ini=27.0, fin=28.95,', 'ini=26.2, fin=27.9,')
a = rep(a, 'F_arch("wbir_asesinato_1995", ini=29.0, fin=32.0, tono=(0.95, 0.9, 0.9), alto=920),\n     [], [TAG("Tadaryl Shipp · 17 años"',
         'F_arch("wbir_asesinato_1995", ini=28.1, fin=32.3, tono=(0.95, 0.9, 0.9), alto=920),\n     [], [TAG("Tadaryl Shipp · 17 años"')
a = rep(a, 'ini=60.0, fin=68.0,', 'ini=59.5, fin=72.5,')
a = rep(a, 'ini=74.0, fin=75.9,', 'ini=73.5, fin=77.1,')
a = rep(a, 'F_clip("france24", ini=42.0, fin=45.8, z0=1.05, z1=1.0, c0=(0.44, 0.5), c1=(0.42, 0.5), tono=(0.8, 0.8, 0.86), sat=0.12)',
         'F_clip("wbir_cronologia", ini=301.3, fin=304.7, z0=1.08, z1=1.0, c0=(0.5, 0.46), c1=(0.5, 0.46), tono=(0.8, 0.8, 0.86), sat=0.12)')
a = rep(a, 'ini=48.0, fin=50.8,', 'ini=47.95, fin=50.5,')
a = rep(a, 'ini=51.0, fin=53.6,', 'ini=50.8, fin=53.1,')
a = rep(a, 'ini=63.0, fin=70.0,', 'ini=60.0, fin=72.0,')
a = rep(a, 'ini=50.0, fin=55.9,', 'ini=50.0, fin=55.7,')
a = rep(a, 'F_arch("wbir_asesinato_1995", ini=29.0, fin=32.0, tono=(0.95, 0.9, 0.9), alto=920),\n     [], [TAG("Tadaryl Shipp · cadena perpetua"',
         'F_arch("wbir_asesinato_1995", ini=28.1, fin=32.3, tono=(0.95, 0.9, 0.9), alto=920),\n     [], [TAG("Tadaryl Shipp · cadena perpetua"')
a = rep(a, 'ini=35.0, fin=41.5,', 'ini=34.0, fin=41.2,')
a = rep(a, 'ini=69.0, fin=73.6,', 'ini=68.4, fin=73.4,')
a = rep(a, 'ini=46.0, fin=49.9,', 'ini=46.1, fin=49.8,')
open('tomas_a.py', 'w', encoding='utf-8').write(a)

b = open('tomas_b.py', encoding='utf-8').read()
b = rep(b, '700, 27.0, INI(Dd, 1) + 0.15, rot=-2, x_cont=(0.125, 0.875), fin=28.95)', '700, 26.2, INI(Dd, 1) + 0.15, rot=-2, x_cont=(0.125, 0.875), fin=27.9)')
b = rep(b, 'ini=14.0, fin=20.6,', 'ini=13.9, fin=20.4,')
b = rep(b, 'F_clip("wbir_cronologia", ini=303.6, fin=307.5, z0=1.0, z1=1.08, tono=(0.85, 0.85, 0.9), sat=0.7)',
         'F_clip("france24", ini=42.0, fin=45.8, z0=1.3, z1=1.22, c0=(0.56, 0.5), c1=(0.56, 0.5), tono=(0.85, 0.85, 0.9), sat=0.7)')
b = rep(b, '[], [CRED(C_W, INI(Dd, 4) + 0.3, FIN(Dd, 4))], ent=("fundido", 0.8)', '[], [CRED(C_F, INI(Dd, 4) + 0.3, FIN(Dd, 4))], ent=("fundido", 0.8)')
b = rep(b, 'ini=286.0, fin=289.5,', 'ini=285.2, fin=288.4,')
b = rep(b, 'ini=73.8, fin=75.7,', 'ini=73.7, fin=74.9,')
b = rep(b, 'ini=15.4, fin=16.9,', 'ini=15.4, fin=16.4,')
b = rep(b, 'ini=45.0, fin=49.7,', 'ini=45.0, fin=49.4,')
b = rep(b, 'ini=73.0, fin=80.6,', 'ini=72.9, fin=80.4,')
b = rep(b, 'FRAME_CLIP("france24", 600, 520, 700, 43.0, INI(Ci, 3) + 0.3, rot=-2, fin=45.8), CRED(C_F,',
         'FRAME_CLIP("wbir_cronologia", 600, 520, 700, 301.3, INI(Ci, 3) + 0.3, rot=-2, fin=304.7), CRED(C_W,')
open('tomas_b.py', 'w', encoding='utf-8').write(b)

k = open('kit_cp.py', encoding='utf-8').read()
k = rep(k, '''def dibujar(d, lz, t):
    tl = t - d["t0"]
    dur = d["t1"] - d["t0"] + 0.5
    d["fondo"](lz, tl, t, dur, 1.0)
''', '''_SH = {}


def _sombra_inf():
    if "s" not in _SH:
        y = (np.arange(H, dtype=np.float32) / H - 0.56) / 0.44
        _SH["s"] = (1.0 - 0.52 * np.clip(y, 0, 1) ** 1.25)[:, None, None].astype(np.float32)
    return _SH["s"]


def dibujar(d, lz, t):
    tl = t - d["t0"]
    dur = d["t1"] - d["t0"] + 0.5
    d["fondo"](lz, tl, t, dur, 1.0)
    if d["textos"]:
        lz *= _sombra_inf()                      # sombra suave abajo: el texto principal se lee sobre cualquier imagen
''')
k = rep(k, '''        im = cv2.cvtColor(cv2.imread(os.path.join(os.getcwd(), "mapas", "mapa_sureste.png")), cv2.COLOR_BGR2RGB)
        _MAPA["m"] = im
        _MAPA["meta"] = json.load(open(os.path.join(os.getcwd(), "mapas", "meta.json")))
    return _MAPA["m"], _MAPA["meta"]''', '''        im = cv2.cvtColor(cv2.imread(os.path.join(os.getcwd(), "mapas", "mapa_sureste.png")), cv2.COLOR_BGR2RGB)
        im = np.clip((im.astype(np.float32) / 255.0 - 0.42) * 1.55 + 0.46, 0, 1)
        _MAPA["meta"] = json.load(open(os.path.join(os.getcwd(), "mapas", "meta.json")))
        pil = Image.fromarray((im * 255).astype(np.uint8)).convert("RGBA")
        ov = Image.new("RGBA", pil.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for txt, lon, lat, px in (("TENNESSEE", -86.3, 35.78, 74), ("KENTUCKY", -85.9, 37.4, 54), ("VIRGINIA", -78.9, 37.35, 54),
                                  ("VIRGINIA OCCIDENTAL", -80.9, 38.7, 44), ("CAROLINA DEL NORTE", -79.7, 35.55, 50),
                                  ("GEORGIA", -83.4, 33.2, 54), ("ALABAMA", -86.8, 33.0, 54), ("MISISIPI", -89.6, 33.6, 50)):
            x, y = _proy_meta(lon, lat)
            f = D.fuente("sans_l", px)
            sep = int(px * 0.28)
            w = sum(d.textlength(c, font=f) + sep for c in txt)
            xx = x - w / 2
            for c in txt:
                d.text((xx, y), c, font=f, fill=(255, 255, 255, 120), anchor="lm", stroke_width=2, stroke_fill=(0, 0, 0, 90))
                xx += d.textlength(c, font=f) + sep
        pil = Image.alpha_composite(pil, ov).convert("RGB")
        _MAPA["m"] = np.asarray(pil)
    return _MAPA["m"], _MAPA["meta"]


def _proy_meta(lon, lat):
    m = _MAPA["meta"]
    n = 2 ** m["z"]
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return (x - m["tx0"]) * 256 - m["x_off"], (y - m["ty0"]) * 256 - m["y_off"]''')
open('kit_cp.py', 'w', encoding='utf-8').write(k)
print("parche ok")
