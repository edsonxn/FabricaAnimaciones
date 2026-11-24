"""Regla 10: extrae del MASTER las citas de audio que la voz manda escuchar, Whisper + nivel, y las junta en previews/citas_audio.mp3.
Uso: python videos/er_messmer_atrocidades/_citas_master.py   (CPU, para no chocar con la GPU)"""
import subprocess, glob, os, re
V = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
import sys
master = sys.argv[1] if len(sys.argv) > 1 else glob.glob(os.path.join(V, "salida", "*_MASTER.mp4"))[0]
# (nombre, inicio, fin, lo que se espera oír) — segundos de la mezcla (audio/mezcla) = MASTER
CITAS = [("s_despojados", 26.9, 38.9, "Those stripped of the Grace of Gold shall all meet death, in the embrace of Messmer's flame"),
         ("s_cornamentado", 889.9, 898.1, "Messmer, foe of my beloved people. In vengeance for the flames, my blade I wield"),
         ("s_madre_sanciona", 1208.7, 1217.6, "Mother, wouldst thou truly Lordship sanction, in one so bereft of light?"),
         ("s_maldicion", 1389.5, 1397.6, "Mother... Marika... A curse upon thee")]
prev = os.path.join(V, "previews"); os.makedirs(prev, exist_ok=True)
from faster_whisper import WhisperModel
wm = WhisperModel("large-v3", device="cpu", compute_type="int8")
partes = []
for n, a, b, esp in CITAS:
    w = os.path.join(prev, f"_cita_{n}.wav")
    subprocess.run([FF, "-y", "-v", "error", "-ss", str(a), "-to", str(b), "-i", master, "-vn", "-ac", "1", "-ar", "16000", w], check=True)
    r = subprocess.run([FF, "-hide_banner", "-i", w, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    segs, _ = wm.transcribe(w, language="en", beam_size=5, vad_filter=False)
    txt = " ".join(s.text.strip() for s in segs)
    print(f"{n:12s} {a:7.1f}-{b:7.1f}  {lufs[-1] if lufs else '?'} LUFS  Whisper: «{txt}»  (esperado: {esp})")
    partes.append(w)
lst = os.path.join(prev, "_citas.txt")
with open(lst, "w") as f:
    for p in partes:
        f.write(f"file '{p}'\n")
subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-b:a", "160k", os.path.join(prev, "citas_audio.mp3")], check=True)
print("→", os.path.join(prev, "citas_audio.mp3"))
