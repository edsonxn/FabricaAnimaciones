# La historia de Roma en 5 minutos — ESTADO
- canal: cronopapel · video de prueba técnica terminado (boceto + guache con mapa)
- estilo: boceto + guache con mapa → docs/estilo_boceto_guache_mapa.md
- etapa: MASTER corregido y verificado (225.00 s, CER 0.0017, −14.00 LUFS, 212.0 MB)
- siguiente: video entregado y verificado sin cortes de mapa ni colisiones visuales
- locutor: Gaia (`C:/chatterbox_voices/Gaia.mp3`), idioma: es

## Archivos generados
- Master final: `salida/historia_roma_5min_MASTER.mp4` (1080p, 30 fps, 212.0 MB, 225.00 s).
- Subtítulos sincronizados: `salida/historia_roma_5min.srt` (sin subtítulos quemados en pantalla).
- Mezcla de audio: `audio/mezcla.wav` (−14.00 LUFS integrado, −1.11 dBTP de pico, 93 SFX).
- Verificación visual: `previews/final_hoja.jpg` y `previews/master_14s.jpg`.
- Metadatos optimizados: `youtube.json` y `prompt_miniatura.md`.

## Lecciones aprendidas
- La voz de Gaia en float32 desde Chatterbox tiene picos naturales de hasta 1.15; se ajustó `PEAK_MAX = 1.25` en `nucleo/tts_select.py` para admitirla sin descartar tomas fonéticamente perfectas.
- Normalización en `ALIAS_QA` de números ordinales («siglo tres» -> «siglo tercero») para igualar transcripciones de Whisper.
- Coreografía modular en 3 partes (`coreo_r1.py`, `coreo_r2.py`, `coreo_r3.py`) con 19 pegatinas vectoriales ilustradas, jinetes, barcos en movimiento con física senoidal, fracturas territoriales Voronoi, capas ambientales y 95 efectos de sonido colocados proceduralmente.
