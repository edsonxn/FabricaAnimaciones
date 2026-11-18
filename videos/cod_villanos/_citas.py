"""Ubica citas en videos de YouTube: baja el audio y transcribe con faster-whisper (palabras con tiempo)."""
import os, re, subprocess, sys
from faster_whisper import WhisperModel

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "_citas")
os.makedirs(D, exist_ok=True)
TAREAS = [  # id, regex
    ("hIFud6Oeg-Y", r"martyr|cordis"),
    ("Gt1JeMK50us", r"phone|zakhaev|who|name"),
    ("9BNNOeWhN50", r"tried|kennedy"),
    ("wuEQmpxSD88", r"invad|nation|fire|attack"),
    ("xe4p8p4s56g", r"list|kate|where|war is coming|rules|die"),
    ("UnCOKMJvpfo", r"list|kate|where is he"),
]
if len(sys.argv) > 1:
    TAREAS = [t for t in TAREAS if t[0] in sys.argv[1:]]
m = WhisperModel("small", device="cuda", compute_type="float16")
for vid, pat in TAREAS:
    wav = os.path.join(D, vid + ".m4a")
    if not os.path.exists(wav):
        subprocess.run(["yt-dlp", "-q", "-f", "bestaudio[ext=m4a]/bestaudio", "-o", wav, "https://youtu.be/" + vid])
    if not os.path.exists(wav):
        print(vid, "SIN AUDIO"); continue
    segs, _ = m.transcribe(wav, language="en", word_timestamps=False, vad_filter=True)
    for s in segs:
        if re.search(pat, s.text, re.I):
            print(f"{vid} {s.start:7.1f}-{s.end:6.1f} {s.text.strip()[:120]}")
    sys.stdout.flush()
