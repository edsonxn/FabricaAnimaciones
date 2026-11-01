"""Ajuste de audio/musica.wav tras `lyria_tramos.py armar` (desde la carpeta del video, 21-oct-2026).
Lyria dio el tramo 1 en 58 s para 68,6 s (dos intentos: el 2.º, 62,6 s, con 8 s mudos y sin bajar en la tensión). El 1.º casa con el
guion SIN estirarlo (vals de feria → cajita en la cocina → tensión desde 34 s, justo «silencio» → cuna bajita): va tal cual, y el final
de «debajo de la mesa» (los niños dormidos) lo cubre la cajita de música de la biblioteca (wow_darrowshire__lyria_tramo7, otro
público), que entra en fundido a los 55 s y se va bajo el arranque del tramo 2."""
import librosa
import numpy as np
import soundfile as sf

SR = 48000
CAJITA = r"E:\FabricaAnimaciones\musica_biblioteca\wow_darrowshire__lyria_tramo7.mp3"
T_CAJ, DUR_CAJ, NIVEL_CAJ = 55.0, 16.0, 0.32       # entra a los 55 s, dura 16 s, nivel relativo a la mezcla de Lyria
X0, X1 = 67.1, 70.1                                # fundido cruzado hacia lo que dejó `armar` (el tramo 2)

m, _ = sf.read("audio/musica.wav", dtype="float32")
m = m.T
N = m.shape[1]
t1, _ = librosa.load("audio/lyria_tramo1.mp3", sr=SR, mono=False)
t1 = np.vstack([t1, t1]) if t1.ndim == 1 else t1[:2]
pico = np.abs(m).max()
t1 = t1 / (np.abs(t1).max() + 1e-9) * pico
mio = np.zeros((2, int(X1 * SR) + SR), np.float32)
mio[:, :t1.shape[1]] = t1[:, :mio.shape[1]]
c, _ = librosa.load(CAJITA, sr=SR, mono=False, duration=DUR_CAJ)
c = np.vstack([c, c]) if c.ndim == 1 else c[:2]
c = c / (np.abs(c).max() + 1e-9) * pico * NIVEL_CAJ
f_in, f_out = int(3.0 * SR), int(3.5 * SR)
c[:, :f_in] *= np.linspace(0, 1, f_in, dtype=np.float32)
c[:, -f_out:] *= np.linspace(1, 0, f_out, dtype=np.float32)
i = int(T_CAJ * SR)
n = min(c.shape[1], mio.shape[1] - i)
mio[:, i:i + n] += c[:, :n]
a, b = int(X0 * SR), int(X1 * SR)
w = np.ones(N, np.float32)
w[a:b] = np.linspace(1, 0, b - a, dtype=np.float32)
w[b:] = 0
L = min(mio.shape[1], N)
out = m * (1 - w)
out[:, :L] += mio[:, :L] * w[:L]
sf.write("audio/musica.wav", out.T, SR, subtype="FLOAT")
print(f"audio/musica.wav ajustada: tramo 1 sin estirar + cajita {T_CAJ}-{T_CAJ + DUR_CAJ} s; pico {np.abs(out).max():.2f}")
