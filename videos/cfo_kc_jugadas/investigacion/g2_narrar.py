# Transcribe la narración (español, LoL Esports Latinoamérica) de medios/_fuente/g2.mp4 con faster-whisper large-v3
# Uso (desde videos/cfo_kc_jugadas): python investigacion/g2_narrar.py investigacion/vod_g2_480.mp4 -> investigacion/vod_g2_480_narr.txt
# Reintenta en CPU int8 si la GPU da OOM (la comparte otro agente).
import sys, time
from faster_whisper import WhisperModel
BASE = ("Narración en español de League of Legends, Worlds 2026, Karmine Corp (KC) contra CTBC Flying Oyster (CFO). "
        "KC: Canna, Yike, kyeahoo, Caliste, Busio. CFO: Rest, Shad0w, POUT, Doggo, Kino. "
        "Campeones: Ambessa, Lee Sin, Ryze, Caitlyn, Karma, Camille, Pantheon, Viktor, Yunara, Lulu. "
        "Barón, dragón hextech, dragón del océano, alma del océano, dragón ancestral, Heraldo, inhibidor, nexo, ace, Flash, teamfight.")
def modelo():
    for _ in range(6):
        try: return WhisperModel("large-v3", device="cuda", compute_type="float16")
        except Exception as e: print("GPU ocupada:", e); time.sleep(30)
    return WhisperModel("large-v3", device="cpu", compute_type="int8")
m = modelo()
for n in sys.argv[1:]:
    for intento in range(4):
        try:
            seg, info = m.transcribe(n if n.endswith(".mp4") else f"medios/_fuente/{n}.mp4", language="es", initial_prompt=BASE, vad_filter=True)
            lineas = [f"{s.start:6.1f}-{s.end:6.1f} {s.text.strip()}" for s in seg]
            break
        except Exception as e:
            print("reintento", n, e); time.sleep(30)
    with open(f"investigacion/{__import__('os').path.basename(n).replace('.mp4','')}_narr.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print("ok", n, len(lineas))
