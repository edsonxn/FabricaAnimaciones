# El caso de las 1.200 (agentes de OpenAI que asaltaron Hugging Face) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia · meta: dom 18-oct-2026 14:00 CDMX (hueco siguiente a `informante_2027`, programado el 14-oct; ciclo 4 d). Confirmar con `python fab.py yt videos logia`
- estilo: noir → doc de estilo: docs/estilo_noir.md · ejemplo a copiar: videos/informante_2027/ (kit `kit27.py` + `mundos27.py` + `comite.py`)
- etapa: TERMINADO · MASTER 1080p generado (4,87 GB, 15:47 min) · QA verificado (CER 0,0003, desfase 0,00 ms) · miniaturas listas
- siguiente: subida a YouTube (privado/programado para dom 18-oct-2026 14:00 CDMX) con `python fab.py yt subir sociedad_1200`

## Hecho
- Guion en 5 actos ampliado a 15:47 min (28 escenas, 108 frases, 2.078 palabras).
- Voz ElevenLabs generada y validada (108/108 tomas limpias, CER medio < 0.016).
- Línea de tiempo construida (`timeline.json`, 947.14 s, 84 BPM).
- Fotos reales integradas (`sam_altman.jpg`, `clement_delangue.jpg`, `nick_bostrom.jpg`, `yann_lecun.jpg`, `mark_zuckerberg.jpg`).
- Las 28 escenas noir implementadas, con claroscuro, sombras de persiana, lluvia y grano de celuloide.
- Mezcla final de audio masterizada en broadcast standard (-14.00 LUFS, -1.11 dBTP, SNR 12.3 dB).
- Render completo de 316 segmentos (22.731 cuadros) completado con 12 procesos en paralelo.
- MASTER ensamblado: `salida/sociedad_1200_MASTER.mp4` (4.872 MB, 1080p, AAC 320k) y subtítulos `salida/sociedad_1200.srt`.
- Control de calidad (QA) verificado con `verificar`:
  - Inteligibilidad Whisper sobre mezcla final: CER medio 0.0003, 0 frases con CER > 2%.
  - Desfase A/V: 0 muestras (0.00 ms).
  - Duración audio y video: sincronía idéntica (947.14 s).
  - Hoja de contactos final del master: `previews/final_hoja.jpg`.
- Miniaturas generadas: 3 variantes de alto impacto («conspiracion», «altman», «rebelion») en `salida/` y hoja `previews/miniaturas.jpg`.
- Metadatos de YouTube (`youtube.json`) configurados con capítulos exactos al segundo, enlaces a fuentes y tags.

## Siguiente
- [ ] Subida a YouTube como video privado/programado para domingo 18-oct-2026 14:00 CDMX (ciclo de 4 días de LogIA).
- [ ] Limpiar segmentos temporales cuando el usuario lo apruebe (`python fab.py sociedad_1200 limpiar`).

## Archivos clave
- `salida/sociedad_1200_MASTER.mp4` (Video final exportado)
- `salida/sociedad_1200.srt` (Subtítulos en formato estándar)
- `salida/sociedad_1200_mini_altman.jpg` / `_mini_conspiracion.jpg` / `_mini_rebelion.jpg` (Miniaturas)
- `youtube.json` (Ficha completa para publicación en YouTube)
