"""Regla 10 (SFX): la voz nombra el «chasquido del gas» → el SFX destapar debe oírse en la mezcla FINAL.
Mide audio/fx.wav (dónde suena el SFX) contra el archivo final (MASTER o audio/final.wav) en esas ventanas
y junta los dos tramos del final en previews/citas_audio.mp3.
Uso: python videos/mpm_cocacola/_sfx_regla10.py [ruta_master_o_wav]"""
import os, sys, subprocess, numpy as np
V = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
fin = sys.argv[1] if len(sys.argv) > 1 else os.path.join(V, "audio", "final.wav")
# (nombre, ventana de la frase en la línea de tiempo)
TRAMOS = [("chasquido_gancho", 3.0, 9.5), ("tapa_cierre", 839.5, 848.5)]
SR = 16000


def leer(ruta, a, b, hp=0):
    af = ["-af", f"highpass=f={hp}"] if hp else []
    r = subprocess.run([FF, "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", ruta, "-vn", "-ac", "1",
                        "-ar", str(SR), *af, "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32)


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


prev = os.path.join(V, "previews"); os.makedirs(prev, exist_ok=True)
partes = []
for n, a, b in TRAMOS:
    fx = leer(os.path.join(V, "audio", "fx.wav"), a, b)
    mx = leer(fin, a, b)
    hop = SR // 10
    efx = np.array([db(fx[i:i + hop]) for i in range(0, len(fx) - hop, hop)])
    emx = np.array([db(mx[i:i + hop]) for i in range(0, len(mx) - hop, hop)])
    k = int(np.argmax(efx)); t_pico = a + k * .1
    on = np.where(efx > efx.max() - 20)[0]
    print(f"{n}: SFX en fx.wav de {a + on[0] * .1:.1f} a {a + on[-1] * .1:.1f} s, pico {efx.max():.1f} dBFS a {t_pico:.1f} s;"
          f" mezcla final en el pico {emx[k]:.1f} dBFS → SFX {efx.max() - emx[k]:+.1f} dB respecto al total")
    # brillo (>5 kHz: el siseo del gas) en el final, durante el SFX vs. 1 s antes
    hi = leer(fin, a, b, hp=5000)
    ehi = np.array([db(hi[i:i + hop]) for i in range(0, len(hi) - hop, hop)])
    dur = ehi[on[0]:on[-1] + 1].mean(); antes = ehi[max(0, on[0] - 10):on[0]].mean() if on[0] > 0 else float('nan')
    print(f"   >5 kHz en el final: {dur:.1f} dBFS durante el SFX vs {antes:.1f} dBFS justo antes")
    w = os.path.join(prev, f"_sfx_{n}.wav")
    subprocess.run([FF, "-y", "-v", "error", "-ss", str(a), "-t", str(b - a), "-i", fin, "-vn", "-ac", "2", "-ar", "48000", w], check=True)
    partes.append(w)
lst = os.path.join(prev, "_sfx.txt")
with open(lst, "w") as f:
    for p in partes:
        f.write(f"file '{p}'\n")
subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-b:a", "160k",
                os.path.join(prev, "citas_audio.mp3")], check=True)
print("→", os.path.join(prev, "citas_audio.mp3"))
