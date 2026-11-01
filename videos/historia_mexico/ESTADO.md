# Estado: historia_mexico

- **Canal**: `cronopapel` (Cronopapel)
- **Título**: Historia de México en 5 minutos
- **Formato**: `historia_pais_5m`
- **Prueba**: `pais_audiencia_mx`
- **Estado**: PROGRAMADO lun 26-oct-2026 14:00 CDMX (publishAt 2026-10-26T20:00:00Z, privado hasta la fecha; programado el 17-oct) — https://youtu.be/BZd71Z5BIrk
- **YouTube ID**: `BZd71Z5BIrk`
- **Duración**: 409.83 s (6:50) · 1920×1080 · 30 fps · 500.5 MB
- **Audio**: LUFS -14.00 · True Peak -1.03 dBTP · Relación voz/(música+sfx): 14.1 dB · CER final: 0.0015 · Desfase MP4 vs WAV: 0.00 ms
- **Miniatura**: `salida/historia_mexico_5min_mini.jpg` (aplicada en YouTube)
- **Subtítulos**: `salida/historia_mexico_5min.srt` (cargados en YouTube)

## Etapas completadas
- [x] `guion` (55 frases, 14 escenas + cierre, 13 eras desde Olmecas 1200 a. C. hasta México moderno 2026)
- [x] `mapa` (`datos/campos_mx.npz`: relieve real ETOPO1 120°W–85°W / 13°N–33°N + SDF costero y fronteras históricas)
- [x] `dibujos` (78 dibujos originales en `obj_mx1.py`, `obj_mx2.py`, `obj_mx3.py` inspeccionados en `previews/hoja_dibujos_*.png`)
- [x] `voz` + `seleccionar` + `tiempo` (55/55 tomas limpias, 409.82 s @ 112 BPM)
- [x] `comprobar` + `_qa_choques.py` (`0 tramos con avisos`) + `_hojas.py 3` (`rev_00.jpg`..`rev_11.jpg`)
- [x] `sfx` (134 eventos, 58 sonidos distintos)
- [x] `musica` (Lyria 3 Pro en 3 partes unidas en `audio/musica.wav`, 409.82 s)
- [x] `mezcla` (-14.00 LUFS, -1.03 dBTP, +14.1 dB voz sobre fondo)
- [x] `miniatura` (`salida/historia_mexico_5min_mini.jpg`) y `youtube.json`
- [x] `video` (137/137 segmentos en `salida/video_sin_audio.mp4`)
- [x] `final` (`salida/historia_mexico_5min_MASTER.mp4` + `salida/historia_mexico_5min.srt`)
- [x] `verificar` + `_revisar_master.py` (`previews/final_hoja.jpg` + `previews/master_00.jpg`..`master_22.jpg`)
- [x] `yt subir` (`private`: https://youtu.be/BZd71Z5BIrk)
