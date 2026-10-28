# Transcribe la narración de los tramos de jugada (medios/_fuente/j*.mp4) con faster-whisper large-v3 → investigacion/j*_narr.txt
import sys, os
from faster_whisper import WhisperModel
NOMBRES = {"j1": "CFO, CTBC Flying Oyster, Team Liquid, Rest, Shad0w, POUT, Doggo, Kino, Morgan, Josedeodo, Quid, Yeon, CoreJJ, Elder dragon, Baron, Qiyana, Rumble, Viktor, Aphelios, Alistar, Galio, Lee Sin, Syndra, Jhin, Rakan",
           "j2": "CFO, Team Liquid, Rest, Rumble, Doggo, Aphelios, triple kill, nexus, Baron",
           "j3": "T1, CFO, Peyz, Oner, Faker, Doran, Keria, Doggo, POUT, Rest, Kino, Shad0w, Kai'Sa, Ryze, Qiyana, Jhin, Vi, Galio, Ambessa, Rakan, Baron",
           "j3b": "T1, CFO, Doggo, Kai'Sa, Doran, Ambessa, Oner, Faker, Shad0w",
           "j4": "Karmine Corp, KC, Anyone's Legend, Canna, Jax, Yike, Jarvan, kyeahoo, Orianna, Caliste, Kalista, Busio, Renata, Hope, Shanks, Tarzan, Kael, Breathe, quadra kill",
           "j5": "Karmine Corp, Cloud9, Caliste, Xayah, Canna, Renekton, Yike, Qiyana, Busio, Rakan, kyeahoo, Orianna, Thanatos, Blaber, Loki, Tactical, Vulcan, Elder"}
m = WhisperModel("large-v3", device="cuda", compute_type="float16")
for n in sys.argv[1:]:
    seg, info = m.transcribe(f"medios/_fuente/{n}.mp4", language="es" if n == "j5" else "en", initial_prompt=NOMBRES.get(n, ""), vad_filter=True)
    with open(f"investigacion/{n}_narr.txt", "w", encoding="utf-8") as f:
        for s in seg:
            f.write(f"{s.start:6.1f}-{s.end:6.1f} {s.text.strip()}\n")
    print("ok", n)
