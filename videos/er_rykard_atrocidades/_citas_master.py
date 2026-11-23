"""Regla 10: extrae del MASTER las citas de audio que la voz manda escuchar, Whisper + nivel, y las junta en previews/citas_audio.mp3.
Uso: python videos/er_rykard_atrocidades/_citas_master.py   (CPU, para no chocar con la GPU)"""
import subprocess, glob, os, re
V = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
master = glob.glob(os.path.join(V, "salida", "*_MASTER.mp4"))[0]
# (nombre, inicio, fin, lo que se espera oír) — segundos de la mezcla (audio/mezcla) = MASTER
CITAS = [("s_rykard", 804.3, 813.7, "Join the Serpent King"),
         ("s_rya", 1052.8, 1055.3, "Kill me, please"),
         ("s_serpiente", 1405.4, 1415.1, "A serpent never dies")]
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
