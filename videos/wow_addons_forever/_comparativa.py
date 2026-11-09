# -*- coding: utf-8 -*-
"""9-nov (el usuario): comparativa Spoken vs WoW Forever Voces, cada ejemplo >= 5 s y AUDIBLE (voz callada: post de casa2b).
scene-051 se arma aquí a mano (dura 67 s y cruza casa2 → casa2b → casa2c → casa3_0), no con _obs.py:
  Kaltunk (g6) → Willem con Spoken → Willem con el nuestro → lobos con Spoken → lobos con el nuestro → Hermano Paxton (miaddon4).
El audio de cada ejemplo va como PISTA (sfx/cmp_*.mp3, voz=True) anclada a «Escucha la diferencia|fin» en efectos.py.
Grabaciones del 8-nov en E:\\videos grabados (revisadas: sin notificaciones). Tiempos de palabra con Whisper (_palabras_nuevas.py).
  python _comparativa.py
"""
import json
import os
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))
E = r"E:\videos grabados"
G6 = r"D:\wowForeverVoces\grabaciones_obs\2026-11-08 08-40-55.mp4"
# (archivo, desde, dur, pista)  pista = nombre del mp3 de sfx (None = solo imagen)
CMP = [("spoken1", 1.9, 6.3, "cmp_spoken_willem"),     # «Espero que te hayas preparado… aquí en Villanorte.»
       ("miaddon1", 1.2, 7.7, "cmp_mio_willem"),       # «Espero que vengas con ganas… a trabajar la tierra.»
       ("spoken3", 0.7, 6.0, "cmp_spoken_lobos"),      # «Detesto a esos asquerosos lobos grises… deliciosos.»
       ("miaddon3", 2.8, 5.8, "cmp_mio_lobos")]        # «¡Condenados lobos…! Pero me gustan los filetes…»
# el usuario (9-nov): comparar DIRECTO los archivos de audio de cada add-on (sin música ni ruido del juego), no la grabación.
# (archivo, retraso) = el archivo empieza a hablar en 0 s; en la grabación, la voz arranca `retraso` s después del corte.
SPK = os.path.join("D:/", "wowforever", "World of Warcraft", "_forever_", "Interface", "AddOns", "SpokenQuestsAudio_esMX", "generated", "sounds", "quests")
MIO = os.path.join("D:/", "wowForeverVoces", "addon", "WoWForeverVoces", "sonidos")
AUDIO = {"cmp_spoken_willem": (os.path.join(SPK, "783-accept.ogg"), .4), "cmp_mio_willem": (os.path.join(MIO, "783_desc_m.mp3"), .2),
         "cmp_spoken_lobos": (os.path.join(SPK, "33-accept.ogg"), .4), "cmp_mio_lobos": (os.path.join(MIO, "33_desc.mp3"), .3)}
OFFS = []          # segundo de cada ejemplo tras el fin de «Escucha la diferencia» (+.3)


def corte(src, desde, dur, out, audio=True):
    a = ["-c:a", "aac", "-b:a", "192k", "-ar", "48000"] if audio else ["-an"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{desde:.3f}", "-i", src, "-t", f"{dur:.3f}",
                    "-vf", "scale=1920:1080,fps=30,setsar=1", "-c:v", "libx264", "-preset", "fast", "-crf", "18", *a, out], check=True)


def main():
    beats = {b["id"]: b for b in json.load(open("beats.json", encoding="utf-8"))}
    tl = json.load(open("timeline.json", encoding="utf-8"))
    fr = {f["key"]: f for e in tl["escenas"] for f in e["frases"]}
    b = beats["scene-051"]
    t0, t1 = b["t0"], b["t1"]
    tk = fr["casa2_0"]["words"][-1]["e"] + .15            # Kaltunk habla desde 2,6 s de g6 (como OYE de _obs.py)
    tc = fr["casa2b_0"]["words"][-1]["e"] + .3            # empieza la comparativa
    tn = fr["casa2c_0"]["t0"] - .55           # empieza casa2c (inicio de su escena)
    tmp = "medios/_cmp"
    os.makedirs(tmp, exist_ok=True)
    partes = []
    corte(G6, 2.6 - (tk - t0), tc - t0, f"{tmp}/p0.mp4")
    partes.append(f"{tmp}/p0.mp4")
    t = tc
    for i, (f, d, dur, pista) in enumerate(CMP):
        OFFS.append(round(t - (tc - .3), 2))
        largo = dur if i < len(CMP) - 1 else tn - t      # el último llena hasta casa2c
        corte(os.path.join(E, f + ".mp4"), d, largo, f"{tmp}/p{i + 1}.mp4")
        partes.append(f"{tmp}/p{i + 1}.mp4")
        fa, ret = AUDIO[pista]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", fa, "-t", f"{dur:.3f}",
                        # loudnorm: Spoken sonaba 7-12 dB más bajo; mismo volumen para que la comparación sea justa
                        "-vn", "-af", f"adelay={int(ret * 1000)},afade=t=out:st={dur - .2:.2f}:d=0.2,loudnorm=I=-17:TP=-1.5:LRA=11",
                        "-ar", "48000", "-b:a", "192k",
                        f"sfx/{pista}.mp3"], check=True)
        t += largo
    corte(os.path.join(E, "miaddon4.mp4"), 0.0, t1 - t, f"{tmp}/p5.mp4")
    partes.append(f"{tmp}/p5.mp4")
    with open(f"{tmp}/lista.txt", "w", encoding="utf-8") as fh:
        fh.writelines(f"file '{os.path.abspath(p)}'\n" for p in partes)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/lista.txt", "-c", "copy",
                    "medios/scene-051.mp4"], check=True)
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "medios/scene-051.mp4"],
                       capture_output=True, text=True)
    print(f"scene-051 {t0:.2f}-{t1:.2f} ({t1 - t0:.2f} s) -> {float(r.stdout):.2f} s")
    print(f"comparativa desde {tc:.2f}; offsets tras «Escucha la diferencia|fin»: {OFFS}; casa2c {tn:.2f}")


if __name__ == "__main__":
    main()
