# -*- coding: utf-8 -*-
"""Efectos de sonido del anuncio → audio/fx.wav (la mezcla lo baja MEZCLA["fx"] dB). Piezas de la biblioteca de SFX
(sfx/*.mp3, copiadas con `musica_biblioteca.py sfx usar`), ancladas a las mismas palabras que la animación de escenas.py.
Los frecuentes llevan variantes que rotan (pop_a..d, whoosh_a..d, brillo_a/b) para no repetir el mismo sonido.
    python sfx_duos.py         (--seco: solo lista)"""
import json
import subprocess
import sys

import numpy as np
import soundfile as sf

SR = 48000                 # el de la mezcla (nucleo/sinte.SR)
TL = json.load(open("timeline.json", encoding="utf-8"))
ESC = {e["id"]: e for e in TL["escenas"]}


def ww(esc, txt, n=0):
    hits = [w["s"] for f in ESC[esc]["frases"] for w in f["words"]
            if w["w"].lower().strip("¿¡!?.,:").startswith(txt)]
    return hits[n]


def leer(nombre):
    r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-i", f"sfx/{nombre}.mp3", "-f", "f32le", "-ac", "2",
                        "-ar", str(SR), "-"], capture_output=True, check=True)
    x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).T.copy()
    return x / max(1e-6, np.abs(x).max())


def eventos():
    ev = []
    pops = ["pop_a", "pop_b", "pop_c", "pop_d"]
    whs = ["whoosh_a", "whoosh_b", "whoosh_c", "whoosh_d"]
    n = [0]

    def pop(t, g=-9):
        ev.append((t, pops[n[0] % 4], g))
        n[0] += 1

    # cambios de bloque: whoosh que llega justo al corte
    for j, k in enumerate(["grupo", "generos", "eventos", "zona", "precio", "contacto", "cierre"]):
        ev.append((ESC[k]["t0"] - 0.30, whs[j % 4], -8))
    # gancho
    for w in ("boda", "quince", "cumplea"):
        pop(ww("gancho", w) - 0.05, -8)
    ev += [(ww("gancho", "ponle") - 0.1, "whoosh_d", -11), (ww("gancho", "en") - 0.04, "golpe_titulo", -5),
           (ww("gancho", "vivo") + 0.05, "brillo_a", -9)]
    # grupo
    tl = ww("grupo", "llegan") + 0.05
    ev += [(tl, "brillo_b", -7), (tl + 0.12, "golpe_titulo", -8)]
    pop(ww("grupo", "tecladista") - 0.05, -9)
    pop(ww("grupo", "dos") - 0.05, -9)
    ev += [(ww("grupo", "nadie") - 0.05, "brillo_a", -8)]
    # géneros: un pop por píldora; brillo en «¡y mucho más!»
    for w in ("cumbias", "norte", "zapateado", "banda", "grupera", "baladas", "mariachi"):
        pop(ww("generos", w) - 0.06, -10)
    ev += [(ww("generos", "rock") - 0.06, "golpe_titulo", -9), (ww("generos", "rock") + 0.55, "brillo_b", -10)]
    # eventos
    for w in ("fiestas", "reuniones", "eventos"):
        pop(ww("eventos", w) - 0.35, -10)
    ev += [(ww("eventos", "ellos") - 0.15, "whoosh_c", -10), (ww("eventos", "ponen") - 0.05, "brillo_a", -9)]
    # zona: pines
    pop(ww("zona", "aguascalientes") - 0.05, -7)
    ev += [(ww("zona", "municipios") - 0.2, "brillo_b", -12), (ww("zona", "llegan") - 0.05, "brillo_a", -10)]
    # pausas de solo música: un destello suave al entrar (guion.PAUSA; las mismas que escenas.T_PAUSA)
    for k in ("grupo", "generos", "eventos"):
        ev.append((ESC[k]["frases"][-1]["t1"] + 0.35, "brillo_b" if k == "generos" else "brillo_a", -14))
    # precio
    tm = ww("precio", "mil")
    ev += [(tm - 0.08, "golpe_precio", -3), (tm + 0.12, "brillo_b", -7), (ww("precio", "hora") - 0.35, "whoosh_b", -10)]
    # contacto: tiempos medidos de la voz (escenas.contacto)
    t0 = ESC["contacto"]["frases"][0]["t0"]
    ev += [(ww("contacto", "whatsapp") - 0.2, "whatsapp", -6)]
    for x in (2.52, 4.18, 5.60):
        pop(t0 + x - 0.04, -12)
    ev += [(t0 + 5.70, "ding", -10)]
    # cierre
    tc = ww("cierre", "los") - 0.1
    ev += [(tc, "brillo_a", -6), (tc + 0.15, "golpe_titulo", -8), (ESC["cierre"]["frases"][-1]["t1"] + 0.05, "brillo_b", -9)]
    return sorted(ev)


def main():
    ev = eventos()
    if "--seco" in sys.argv:
        from collections import Counter
        for t, nom, g in ev:
            print(f"{t:6.2f}  {nom:14s} {g:+d} dB")
        print(Counter(n for _, n, _ in ev))
        return
    out = np.zeros((2, int(TL["total"] * SR) + SR), np.float32)
    cache = {}
    for t, nom, g in ev:
        if nom not in cache:
            cache[nom] = leer(nom)
        x = cache[nom] * 10 ** (g / 20)
        i = max(0, int(t * SR))
        m = min(x.shape[1], out.shape[1] - i)
        out[:, i:i + m] += x[:, :m]
    out = out[:, :int(TL["total"] * SR)]
    out /= max(1.0, np.abs(out).max() / 0.98)
    sf.write("audio/fx.wav", out.T, SR, subtype="PCM_24")
    print(f"audio/fx.wav: {len(ev)} efectos, {len(cache)} piezas distintas")


if __name__ == "__main__":
    main()
