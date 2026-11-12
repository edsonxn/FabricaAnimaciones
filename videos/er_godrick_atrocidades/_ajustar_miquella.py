# -*- coding: utf-8 -*-
"""12-nov-2026: el Profeta decía «MÍ-que-lla»; se regeneraron las 4 frases con FONETICA «Miquéla» (acento en «que»).
Para NO volver a renderizar la imagen (el video ya estaba hecho y subido), cada toma nueva se estira/encoge con atempo
a la duración EXACTA de la vieja (voz/_descartes/miquella_acento/<k>_FINAL_viejo.wav), así timeline.json no cambia.
Uso (desde la carpeta del video, tras `seleccionar`): python _ajustar_miquella.py  → luego `mezcla` y `final`."""
import os
import shutil
import subprocess

import soundfile as sf

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
for k in ("p5b_3", "p4b_6", "p4b_7", "cierre_7"):
    viejo = f"voz/_descartes/miquella_acento/{k}_FINAL_viejo.wav"
    nuevo = f"voz/final/{k}.wav"
    crudo = f"voz/_descartes/miquella_acento/{k}_NUEVO_sin_ajustar.wav"
    if not os.path.exists(crudo):
        shutil.copy(nuevo, crudo)
    dv, dn = sf.info(viejo).duration, sf.info(crudo).duration
    tempo = dn / dv
    print(f"{k}: viejo {dv:.3f} s · nuevo {dn:.3f} s · atempo {tempo:.3f}" + ("  ⚠ más de 8 %" if abs(tempo - 1) > .08 else ""))
    sr = sf.info(viejo).samplerate
    n = int(round(dv * sr))
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", crudo, "-af", f"atempo={tempo:.6f},apad", "-ar", str(sr), "-ac", "1",
                    "-t", f"{n / sr:.6f}", nuevo], check=True)
    print(f"   → {nuevo} {sf.info(nuevo).duration:.3f} s")
