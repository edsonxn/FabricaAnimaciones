# Transcribe la narración (español, LoL Esports Latinoamérica) de medios/_fuente/g2_j*.mp4 con faster-whisper large-v3
# -> investigacion/g2_jN_narr.txt  (segundos = t de la fuente; reloj HUD = t + K, ver datos_g2.md)
# Ejecutar desde videos/t1_koi_worlds: python investigacion/narrar_g2.py g2_j1 g2_j2 g2_j3
import sys, time
from faster_whisper import WhisperModel
P = ("Worlds, T1, Movistar KOI, KOI, MKOI, Doran, Oner, Faker, Peyz, Keria, Myrwn, Elyoya, Jojopyun, Supa, Alvaro, "
     "Gwen, Jarvan, Orianna, Jhin, Karma, Ornn, Xin Zhao, Viktor, Ezreal, Seraphine, Barón, Heraldo, dragón, inhibidor, nexo")
for intento in range(5):
    try:
        m = WhisperModel("large-v3", device="cuda", compute_type="float16"); break
    except Exception as e:
        print("reintento carga", e); time.sleep(30)
for n in sys.argv[1:]:
    for intento in range(5):
        try:
            seg, info = m.transcribe(f"medios/_fuente/{n}.mp4", language="es", initial_prompt=P, vad_filter=True)
            lineas = [f"{s.start:6.1f}-{s.end:6.1f} {s.text.strip()}" for s in seg]
            break
        except Exception as e:
            print("reintento", n, e); time.sleep(30)
    with open(f"investigacion/{n}_narr.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print("ok", n, len(lineas))
