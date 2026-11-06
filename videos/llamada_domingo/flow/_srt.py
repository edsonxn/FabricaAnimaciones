# .srt clip por clip (modo novela): Whisper a cada medios/scene-NNN.mp4 desplazado al t0 de su beat
import json, os
from faster_whisper import WhisperModel
b = json.load(open("beats.json", encoding="utf-8"))
m = WhisperModel("medium", device="cuda", compute_type="float16")
mute = {"scene-071": 2.4}
def ts(t):
    h, r = divmod(t, 3600); mi, s = divmod(r, 60); return f"{int(h):02}:{int(mi):02}:{int(s):02},{int((s % 1) * 1000):03}"
out = []
for x in b:
    f = f"medios/{x['id']}.mp4"
    if not os.path.exists(f):
        continue
    segs, _ = m.transcribe(f, language="es", vad_filter=True)
    for s in segs:
        if s.start < mute.get(x["id"], -1) or not s.text.strip():
            continue
        a, z = x["t0"] + s.start, min(x["t1"], x["t0"] + s.end)
        if a < x["t1"]:
            out.append((a, z, s.text.strip()))
with open("salida/llamada_de_domingo.srt", "w", encoding="utf-8") as fh:
    for i, (a, z, t) in enumerate(out, 1):
        fh.write(f"{i}\n{ts(a)} --> {ts(z)}\n{t}\n\n")
print(len(out), "líneas")
