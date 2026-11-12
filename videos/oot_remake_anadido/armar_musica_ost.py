# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Ocarina of Time (regla del usuario del 23-oct-2026: en Crónicas del gaming
va la música del juego, NUNCA Lyria). Pistas originales de N64 de «Nintendo Music Archive» (yt-dlp, una búsqueda por pista,
solo se aceptan resultados de ese canal con «Ocarina of Time OST - <pista>» en el título) en audio/ost/.
Receta de majora_mask/armar_musica_ost.py: cada sección a -23 LUFS, fundidos cruzados de 2 s, rampa final.
    python armar_musica_ost.py bajar   baja las pistas que falten (audio/ost/<slug>.wav)
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py oot_remake_anadido mezcla`)
"""
import json
import os
import subprocess
import sys

import numpy as np

SR = 48000
CRUCE = 2.0
LUFS = -23.0
APARTA_DB = -14.0       # la banda sonora baja esto donde suena el juego (beats con ambiente_por en guion.SECUENCIA)
CANAL = "Nintendo Music Archive"

# slug -> nombre de la pista en el título del video
PISTAS = {
    "titulo": "Title Theme", "leyenda": "Legend of Hyrule", "tienda": "Shop", "kakariko": "Kakariko Village",
    "templo_tiempo": "Temple of Time", "hada": "Great Fairy's Fountain", "kokiri": "Kokiri Forest", "agua": "Water Temple",
    "zora": "Zora's Domain", "mercado": "Market", "zelda": "Zelda's Theme", "bosque_perdido": "Lost Woods",
    "goron": "Goron City", "ocarina": "Ocarina of Time", "lon_lon": "LonLon Ranch", "gerudo": "Gerudo Valley",
    "campo": "Hyrule Field Main Theme", "arbol_deku": "Inside the Deku Tree", "final": "End Credits",
    "buho": "Kepora Gebora's Theme", "archivo": "Dodongo's Cavern", "torre": "Ganon's Castle Under Ground",
    # nuevas para este video (11-nov)
    "mascaras": "Happy Mask Shop", "saria": "Saria's Song", "pociones": "Potion Shop", "templo_bosque": "Forest Temple",
    "pozo": "Shadow Temple"  # el Fondo del Pozo usa este tema, "sabios": "Chamber of the Sages", "jabu": "Inside Jabu Jabu's Belly",
}

# escena del guion -> pistas que la llenan en orden: (slug, desde s). Distinto reparto que oot_remake_cambios.
SECCIONES = [
    ("intro", [("leyenda", 0)]),                      # la máscara sin amiibo
    ("contexto", [("titulo", 0)]),                    # ventas, la caja, el falso jefe de Skull Kid
    ("p12", [("kokiri", 0)]),                         # koroks en el Bosque Kokiri
    ("p11", [("campo", 0)]),                          # Link toca y corre por la hierba
    ("p10", [("ocarina", 0)]),                        # la ocarina de Saria y la del Tiempo (el tema de la entrega)
    ("p9", [("pociones", 0)]),                        # la quinta botella (tienda de pociones)
    ("p8", [("templo_bosque", 0)]),                   # semilla del mercader (Templo del Bosque)
    ("p7", [("pozo", 0)]),                            # ReDeads y Mano Muerta (Fondo del Pozo)
    ("com1", [("tienda", 0)]),                        # Loquendo
    ("p6", [("hada", 0)]),                            # el salón que se abre soñando
    ("p5", [("kakariko", 0)]),                        # la Máscara de la Verdad (guardia de Kakariko)
    ("com2", [("tienda", 30)]),                       # TikTok
    ("p4", [("templo_tiempo", 0)]),                   # Ganondorf en el Templo del Tiempo
    ("p4b", [("torre", 0)]),
    ("p3", [("sabios", 0)]),                          # los sabios
    ("p3b", [("sabios", 40)]),
    ("com3", [("buho", 0)]),                          # «su propio tema musical» = el tema de Kaepora (se oye)
    ("p2", [("jabu", 0)]),                            # Master Quest (vacas en la tripa de Jabu Jabu)
    ("p1", [("bosque_perdido", 0)]),                  # la máscara 103 / Skull Kid
    ("cierre", [("final", 0)]),
]


def bajar():
    os.makedirs(os.path.join("audio", "ost"), exist_ok=True)
    for slug, nombre in PISTAS.items():
        out = os.path.join("audio", "ost", slug + ".wav")
        if os.path.exists(out):
            continue
        q = f"ytsearch5:{CANAL} The Legend of Zelda Ocarina of Time OST - {nombre}"
        r = subprocess.run(["yt-dlp", q, "--flat-playlist", "--print", "%(id)s|%(channel)s|%(title)s"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        elegido = None
        for linea in r.stdout.splitlines():
            vid, canal, titulo = (linea.split("|", 2) + ["", ""])[:3]
            if canal == CANAL and "Ocarina of Time OST" in titulo and titulo.rsplit(" - ", 1)[-1].strip().lower() == nombre.lower():
                elegido = (vid, titulo)
                break
        if not elegido:
            print(f"  ✗ {slug}: no encontrada «{nombre}»")
            continue
        subprocess.run(["yt-dlp", "-q", "-x", "--audio-format", "wav", "-o", os.path.join("audio", "ost", slug + ".%(ext)s"),
                        f"https://youtu.be/{elegido[0]}"], check=False)
        print(f"  {slug:15s} {elegido[0]}  {elegido[1]}")


def cargar(n):
    import soundfile as sf
    from scipy.signal import resample_poly
    x, sr = sf.read(os.path.join("audio", "ost", n + ".wav"), always_2d=True)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g, axis=0)
    return x[:, :2] if x.shape[1] >= 2 else np.repeat(x, 2, axis=1)


def rampa(n, sube=True):
    r = np.linspace(0, 1, n) if sube else np.linspace(1, 0, n)
    return np.sin(r * np.pi / 2)[:, None]


def armar():
    import pyloudnorm as pyln
    import soundfile as sf
    tl = json.load(open("timeline.json", encoding="utf-8"))
    total = float(tl["total"])
    t0s = {e["id"]: float(e["t0"]) for e in tl["escenas"]}
    cortes = [(t0s[i], pistas) for i, pistas in SECCIONES]
    meter = pyln.Meter(SR)
    out = np.zeros((int(total * SR) + SR, 2))
    nc = int(CRUCE * SR)
    for k, (t0, pistas) in enumerate(cortes):
        t1 = cortes[k + 1][0] if k + 1 < len(cortes) else total
        largo = int((t1 - t0 + CRUCE) * SR)
        seg = np.zeros((0, 2))
        for n, desde in pistas:
            x = cargar(n)[int(desde * SR):]
            if len(seg):
                c = min(nc, len(seg), len(x))
                seg[-c:] = seg[-c:] * rampa(c, False) + x[:c] * rampa(c)
                seg = np.vstack([seg, x[c:]])
            else:
                seg = x
            if len(seg) >= largo:
                break
        while len(seg) < largo:                                  # si aún falta, repite la primera pista
            x = cargar(pistas[0][0])
            c = min(nc, len(seg), len(x))
            seg[-c:] = seg[-c:] * rampa(c, False) + x[:c] * rampa(c)
            seg = np.vstack([seg, x[c:]])
        seg = seg[:largo].copy()
        l = meter.integrated_loudness(seg)
        seg *= 10 ** ((LUFS - l) / 20)
        if t0 == 0:
            seg[:SR] *= rampa(SR)
        else:
            seg[:nc] *= rampa(nc)
        seg[-nc:] *= rampa(nc, False)
        i0 = int(max(0.0, t0 - CRUCE / 2) * SR) if t0 > 0 else 0
        out[i0:i0 + len(seg)] += seg[:len(out) - i0]
        print(f"{t0:7.1f}-{t1:7.1f}  {' + '.join(p for p, _ in pistas):30s}  {l:6.1f} LUFS -> {LUFS}")
    out = out[:int(total * SR)]
    # SONIDO ORIGINAL (el usuario, 26-oct-2026): en los beats con ambiente_por la banda sonora se aparta y se oye el juego
    import guion
    vols = guion.SECUENCIA.get("ambiente_por", {})
    gan = np.ones(len(out))
    r = int(.5 * SR)
    for b in json.load(open("beats.json", encoding="utf-8")):
        if vols.get(b["id"], 0) > 0:
            i0, i1 = int(b["t0"] * SR), min(len(out), int(b["t1"] * SR))
            g = 10 ** (APARTA_DB / 20)
            gan[i0:i1] = np.minimum(gan[i0:i1], g)
            gan[max(0, i0 - r):i0] = np.minimum(gan[max(0, i0 - r):i0], np.linspace(1, g, i0 - max(0, i0 - r)))
            gan[i1:i1 + r] = np.minimum(gan[i1:i1 + r], np.linspace(g, 1, len(gan[i1:i1 + r])))
    out *= gan[:, None]
    print(f"banda sonora apartada {APARTA_DB} dB en {sum(1 for v in vols.values() if v > 0)} beats con sonido original")
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join("audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s)")


if __name__ == "__main__":
    bajar() if sys.argv[1:] == ["bajar"] else armar()
