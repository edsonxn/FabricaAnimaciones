# -*- coding: utf-8 -*-
"""timeline.json para videos con AUDIO EXTERNO (guion.py: AUDIO_EXTERNO = "ruta al audio o video ya grabado").
No hay voz que generar: el audio dado ES la pista de voz. Lo llama `tiempo` (linea_tiempo.py).

  1. Convierte la fuente a audio/externo.wav (48 kHz).
  2. La transcribe palabra por palabra con Whisper -> voz/transcripcion.json (se hace UNA vez: si el archivo existe se
     reutiliza; corrige ahí a mano los nombres que Whisper oyó mal y vuelve a correr `tiempo`).
  3. Escribe timeline.json con una sola escena («audio») y una frase por segmento hablado, con sus palabras: así `beats`
     corta en las pausas reales y las anclas de efectos.py («cuando dice X») encuentran su segundo.
`mezcla` usa audio/externo.wav tal cual (sin la cadena de la voz sintética); `voz`, `seleccionar` y `verificar` no aplican.
"""
import json
import os
import subprocess

import config
import guion

FUENTE = guion.AUDIO_EXTERNO
WAV, TRANS = "audio/externo.wav", "voz/transcripcion.json"
os.makedirs("audio", exist_ok=True)
os.makedirs("voz", exist_ok=True)
if not os.path.exists(WAV) or os.path.getmtime(WAV) < os.path.getmtime(FUENTE):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", FUENTE, "-vn", "-ac", "2", "-ar", "48000", WAV], check=True)
total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", WAV],
                             capture_output=True, text=True).stdout.strip())

if not os.path.exists(TRANS):
    from faster_whisper import WhisperModel
    m = WhisperModel("large-v3", device="cuda", compute_type="float16")
    segs, _ = m.transcribe(WAV, language=config.VOZ.get("idioma", "es"), word_timestamps=True, vad_filter=True, beam_size=5)
    json.dump([dict(t0=round(s.start, 2), t1=round(s.end, 2), texto=s.text.strip(),
                    words=[dict(w=w.word.strip(), s=round(w.start, 3), e=round(w.end, 3)) for w in s.words]) for s in segs],
              open(TRANS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
segs = json.load(open(TRANS, encoding="utf-8"))

frases = [dict(key=f"audio_{i}", texto=s["texto"], t0=s["t0"], t1=s["t1"], words=s["words"]) for i, s in enumerate(segs) if s["words"]]
bpm = float(config.BPM)
tl = dict(bpm=bpm, beat=60 / bpm, unidad=4, total=round(total, 3), titulo=config.TITULO, estilo=config.ESTILO_VISUAL,
          audio_externo=WAV, transiciones=[],
          escenas=[dict(id=config.IDS[0], pre=0.0, t0=0.0, t1=round(total, 3), compases=0, beats=0, frases=frases,
                        fin_voz=frases[-1]["t1"] if frases else 0.0)])
json.dump(tl, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"timeline.json: audio externo de {total:.1f} s, {len(frases)} frases, {sum(len(f['words']) for f in frases)} palabras")
for f in frases:
    print(f"  {f['t0']:6.1f}-{f['t1']:6.1f}  {f['texto']}")
