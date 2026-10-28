# -*- coding: utf-8 -*-
"""PROMO EN INGLÉS de la integración de Overgear (coaching de WoW Forever) para mandársela a Overgear (el usuario, 28-oct-2026).
Es la versión inglesa del segmento de «wow_clases_ocultas» (texto aprobado) con el kit «WoW - Forever (nov)», narrada con
ElevenLabs (George, eleven_v4_turbo) y la «musica promo» del canal. No va a YouTube.
  python videos/overgear_promo_en/promo.py            voz (solo las frases que falten) + render → salida/overgear_promo_EN.mp4
  python videos/overgear_promo_en/promo.py --hoja     solo la hoja de revisión (previews/hoja.jpg)
Creativo del código: CRONICAS10_forever.mp4 (Alice, 28-oct): rótulo en verde «-10% WITH PROMO CODE CRONICAS10» → «LINK IN THE DESCRIPTION».
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "nucleo"))
import secuencia_fx as F          # _croma (verde/rojo) y _VideoFx (lector con bucle)
import tts_eleven as E

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
W, H, FPS = 1920, 1080, 30
CO = os.path.join(RAIZ, "videos", "wow_clases_ocultas", "medios") + "\\"
OGF = CO + "_overgear\\forever\\"
CREATIVO = CO + "_overgear\\CRONICAS10_forever.mp4"   # 10 s en verde; el código se lee de 2,5 a 6 s
MUSICA = CO + "_overgear\\musica_promo.mp3"

VOZ_ID, MODELO = "JBFqnCBsd6RMkjVDRZzb", "eleven_v4_turbo"     # George: narrador británico cálido
FRASES = [
    "[curious] Now that Forever is out, finding a hidden class is only half the job. The other half is knowing how to play it.",
    "Most players don't get stuck because they're bad. [short pause] They get stuck because nobody told them what they were "
    "doing wrong. And in Forever, the habits you pick up in the first weeks stay with you.",
    "[warmly] That's where Overgear comes in, the sponsor of today's video, with their coaching for World of Warcraft Forever.",
    "It's self-play: you play your own character, and a verified pro explains, by voice, what you're missing and why.",
    "Talents, rotation, addons, new dungeons or duels. You choose, and you only pay for the hours you need.",
    "The link is in the description, and for the Forever launch there's a special discount, for one month only.",
    "[excited] Use code CRONICAS10 and get ten percent off.",
]
HUECO, INICIO = 0.35, 0.5


def voz():
    os.makedirs(os.path.join(AQUI, "voz"), exist_ok=True)
    durs = []
    for i, t in enumerate(FRASES):
        mp3 = os.path.join(AQUI, "voz", f"l{i}.mp3")
        firma = mp3 + ".txt"
        if not (os.path.exists(mp3) and open(firma, encoding="utf-8").read() == t):
            r = E.post(f"text-to-speech/{VOZ_ID}?output_format=mp3_44100_128", timeout=120,
                       json=dict(text=t, model_id=MODELO, seed=7 + i, language_code="en", voice_settings=dict(stability=0.5)))
            if r.status_code != 200:
                raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
            open(mp3, "wb").write(r.content)
            open(firma, "w", encoding="utf-8").write(t)
            print(f"voz l{i}: {r.headers.get('character-cost')} créditos")
        d = float(subprocess.run([FF.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error", "-show_entries", "format=duration",
                                  "-of", "csv=p=0", mp3], capture_output=True, text=True).stdout)
        durs.append(d)
    t, tiempos = INICIO, []
    for d in durs:
        tiempos.append((t, t + d))
        t += d + HUECO
    return tiempos


def plan(T):
    """Capas por tramo: (de, a, ruta, desde, opciones). La primera de cada instante es la base (cuadro entero, sin croma)."""
    L = lambda i: T[i][0]
    cre = T[6][0] - 2.5                                          # el creativo entra 2,5 s antes: «CRONICAS10» se lee con la voz
    fin = cre + 9.7
    base = [(0, L(1) + 0.2, CO + "scene-025.mp4", 2.0, {}),
            (L(1) + 0.2, L(1) + 5.8, CO + "scene-034.mp4", 0.5, {}),   # banda en combate
            (L(1) + 5.8, L(2), CO + "scene-010.mp4", 0.0, {}),         # pelea en rojo
            (L(2), L(3), CO + "scene-026.mp4", 0.0, {}),       # recorrido por overgear.com/games/wow-forever/coaching
            (L(3), L(4), CO + "scene-022.mp4", 0.0, {}),       # tu personaje, jugando tú
            (L(4), fin, CO + "scene-028.mp4", 0.0, {})]        # Background de Overgear
    capas = [(L(2), L(5), OGF + "logo-light-bg-small_wow-forever.mp4", 0, dict(croma=True, bucle=True)),
             (L(3) + 2.0, L(3) + 6.0, OGF + "2 pair_green_wow-forever.mp4", 0, dict(croma=True)),
             (L(4), L(4) + 4.0, OGF + "cards-1-coaching_green-screen_wow-forever.mp4", 0, dict(croma=True)),
             (L(4) + 3.6, L(5), OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", 0, dict(croma="rojo")),
             (L(5), cre, OGF + "packshot-text_greenscreen_wow-forever.mp4", 0, dict(croma=True)),
             (cre, fin, CREATIVO, 0, dict(croma=True))]
    return base, capas, fin + 0.4


class Lector:
    def __init__(self):
        self.v = {}

    def cuadro(self, ruta, desde, dt, bucle=False):
        if (ruta, desde) not in self.v:
            self.v[(ruta, desde)] = F._VideoFx(ruta, desde, 1.0, bucle)
        f = self.v[(ruta, desde)].cuadro(dt)
        if f.shape[:2] == (H, W):
            return f
        h, w = f.shape[:2]                                      # más ancho que 16:9 (creativo de 2000x1080): recorte al centro
        f = cv2.resize(f, (max(W, round(w * H / h)), H), interpolation=cv2.INTER_LINEAR)
        x = (f.shape[1] - W) // 2
        return f[:, x:x + W]


def cuadro(t, base, capas, lec):
    fb = next((b for b in base if b[0] <= t < b[1]), base[-1])
    f = lec.cuadro(fb[2], fb[3], t - fb[0]).copy()
    for de, a, ruta, desde, op in capas:
        if de <= t < a:
            k = F._croma(lec.cuadro(ruta, desde, t - de, op.get("bucle", False)), op.get("croma", True))
            al = k[..., 3:4].astype(np.float32) / 255 * min(1.0, (t - de) / .25, (a - t) / .25)
            f = (k[..., :3] * al + f * (1 - al)).astype(np.uint8)
    for b0 in [b[0] for b in base[1:]]:                       # fundido corto entre bases
        if b0 - .2 <= t < b0 + .2:
            f = (f * (0.55 + 0.45 * abs(t - b0) / .2)).astype(np.uint8)
    return f


def audio(T, dur, sal):
    ent = sum([["-i", os.path.join(AQUI, "voz", f"l{i}.mp3")] for i in range(len(FRASES))], [])
    filt = "".join(f"[{i}:a]adelay={int(T[i][0] * 1000)}|{int(T[i][0] * 1000)}[v{i}];" for i in range(len(FRASES)))
    filt += "".join(f"[v{i}]" for i in range(len(FRASES))) + f"amix=inputs={len(FRASES)}:normalize=0,loudnorm=I=-16:TP=-1.5[voz];"
    filt += (f"[{len(FRASES)}:a]atrim=0.3:{dur + 0.3},asetpts=PTS-STARTPTS,volume=-17dB,"
             f"afade=t=out:st={dur - 1.2}:d=1.2[mus];[voz][mus]amix=inputs=2:normalize=0,alimiter=limit=0.95[out]")
    subprocess.run([FF, "-v", "error", "-y", *ent, "-i", MUSICA, "-filter_complex", filt, "-map", "[out]", "-t", f"{dur}",
                    "-ar", "48000", sal], check=True)


def main():
    T = voz()
    base, capas, dur = plan(T)
    json.dump(dict(frases=FRASES, tiempos=T, dur=dur), open(os.path.join(AQUI, "timeline.json"), "w", encoding="utf-8"), indent=1)
    lec = Lector()
    os.makedirs(os.path.join(AQUI, "previews"), exist_ok=True)
    if "--hoja" in sys.argv:
        ts = np.arange(0.5, dur, 1.6)
        ms = [cv2.resize(cuadro(t, base, capas, lec), (480, 270)) for t in ts]
        for m, t in zip(ms, ts):
            cv2.putText(m, f"{t:.1f}s", (6, 262), cv2.FONT_HERSHEY_SIMPLEX, .6, (90, 214, 255), 2, cv2.LINE_AA)
        ms += [np.zeros_like(ms[0])] * (-len(ms) % 5)
        cv2.imwrite(os.path.join(AQUI, "previews", "hoja.jpg"), np.vstack([np.hstack(ms[i:i + 5]) for i in range(0, len(ms), 5)]))
        print("previews/hoja.jpg", f"{dur:.1f} s")
        return
    os.makedirs(os.path.join(AQUI, "salida"), exist_ok=True)
    wav = os.path.join(AQUI, "salida", "audio.wav")
    audio(T, dur, wav)
    sal = os.path.join(AQUI, "salida", "overgear_promo_EN.mp4")
    p = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac",
                          "-b:a", "192k", "-shortest", "-movflags", "+faststart", sal], stdin=subprocess.PIPE)
    for n in range(int(dur * FPS)):
        p.stdin.write(cuadro(n / FPS, base, capas, lec).tobytes())
    p.stdin.close()
    p.wait()
    print(sal, f"{dur:.1f} s")


if __name__ == "__main__":
    main()
