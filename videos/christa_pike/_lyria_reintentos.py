# -*- coding: utf-8 -*-
"""Genera N candidatos de música con Lyria con un prompt NEUTRO (el filtro de entrada de Lyria bloquea palabras como «childhood», «dread»,
nombres propios o ids de escena como «crimen»/«juicio»). Etiquetas «Section k», descripciones solo musicales, con reintentos."""
import json
import os
import subprocess
import sys
import time
import urllib.error

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import lyria  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2
TL = json.load(open("timeline.json", encoding="utf-8"))
SEC = {
    "gancho": ("Opening: a sparse low drone, a slow heartbeat-like pulse, thin high string harmonics slowly rising, a held swell and a sudden silence at the end.", 4),
    "quien": ("Quiet and bleak: solitary felt piano, soft low strings, cold air.", 3),
    "colleen": ("Tender and sad: a gentle piano motif alone, warm sustained strings. Very soft.", 2),
    "crimen": ("Dark and tense but restrained: low pulsing bass, long dissonant strings, no melody, a heavy hit at the end.", 5),
    "juicio": ("Cold and procedural: steady low pulse, sparse piano notes like a ticking clock, sober.", 4),
    "corredor": ("Isolation and passing years: slow ambient drone, distant metallic textures, a single piano note echoing, bleak and still.", 3),
    "debate": ("Two alternating low string phrases in conversation, unresolved, serious, building slightly.", 4),
    "camino": ("Countdown tension: a quickening quiet pulse, ticking, rising strings, inevitability.", 6),
    "noche": ("Peak tension, restrained: very slow bass pulse, long cold string clusters rising, silences, a final unresolved cluster. No release.", 8),
    "despues": ("Aftermath: empty and stunned, soft low drone, sparse piano, slow and unsettled.", 5),
    "historial": ("Institutional unease: slow low strings, a ticking clock, sparse piano, cold and procedural.", 4),
    "precedente": ("Reflective: old-world solemn strings, slow piano, a feeling of history repeating.", 4),
    "cierre": ("Ethereal pads and a slow solitary piano, the question remains open, quiet, one final note, fades to silence.", 3),
}
total = TL["total"]
esc = TL["escenas"]
lineas = [f"Somber cinematic documentary score: slow low strings, sparse felt piano, a deep soft sub-bass pulse, distant ambient textures, subtle ticking clock, "
          f"occasional soft impacts. No drum kit, no big orchestral melody, never triumphant, never sentimental. Total length: exactly {lyria.mmss(total)} "
          f"({int(round(total))} seconds). Instrumental only, no vocals, no singing, no spoken words. It must leave room for a narrator: keep the middle "
          "frequencies calm, no lead melody competing with speech. End with a natural fade-out.", ""]
for k, e in enumerate(esc):
    d, inten = SEC[e["id"]]
    t1 = esc[k + 1]["t0"] if k + 1 < len(esc) else total
    lineas.append(f"[{lyria.mmss(e['t0'])} - {lyria.mmss(t1)}] Section {k + 1}: Intensity {inten}/10. {d}")
texto = "\n".join(lineas)
open("audio_prompt_lyria.txt", "w", encoding="utf-8").write(texto)
print(texto[:400], "...", flush=True)
os.makedirs("audio", exist_ok=True)
for k in range(1, N + 1):
    ruta_mp3 = f"audio/lyria_{k}.mp3"
    if os.path.exists(ruta_mp3) and os.path.getsize(ruta_mp3) > 100000:
        print("ya existe", ruta_mp3)
        continue
    for intento in range(1, 7):
        t = time.time()
        try:
            datos, mime, _ = lyria.generar(texto)
        except urllib.error.HTTPError as e:
            print(f"candidato {k} intento {intento}: HTTP {e.code} {e.read()[:140]}; reintento", flush=True)
            time.sleep(3)
            continue
        ext = ".mp3" if ("mpeg" in mime or "mp3" in mime) else ".wav"
        ruta = f"audio/lyria_{k}{ext}"
        open(ruta, "wb").write(datos)
        d = subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ruta], capture_output=True, text=True).stdout.strip()
        print(f"candidato {k}: {ruta} {float(d):.1f} s ({time.time() - t:.0f} s de generación, intento {intento})", flush=True)
        break
    else:
        print(f"candidato {k}: sin éxito")
