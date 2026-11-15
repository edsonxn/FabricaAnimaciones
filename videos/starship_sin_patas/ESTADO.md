# ¿Por qué Starship NO tiene patas? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: T Menos Cero (`t_menos_cero`) · 2.º video · hueco sáb 21-nov 17:37 CDMX (`canales --actualizar`) · una sesión directo al MASTER
- estilo: LÍNEA 3D + VIDEO REAL de cada suceso + fotos en marcos de alambre · copiar `videos/starship_vuelo15/` · doc `docs/estilo_linea3d.md` (§ REGLA: más video real)
- etapa: SUBIDO KinwPPlHKpg, programado sáb 21-nov 17:37 CDMX (2026-11-21T23:37:00Z) · MASTER 9:26 verificado (CER 0,19 %, desfase 0, sin cuadros negros) · en la tele
- siguiente: medir a 7 días (28-nov); el usuario puede cambiar la miniatura por A/C1/C2 de `miniatura/propuestas/` (`yt aplicar starship_sin_patas t_menos_cero KinwPPlHKpg`); al aprobar: `limpiar`
- NO tocar el texto del guion: las anclas `ww` dependen de él

## Hecho (14-nov-2026)
- Guion 83 frases (`datos.md` con fuentes) · voz ElevenLabs Alberto · 30 planos de video real de 12 clips + 8 fotos de Commons + 3D (planos1/2/3.py) · `promesas.md` · música de la biblioteca (dos_lunas t1/t2, t1_koi_worlds t2/t3, lol_semana2 t3) · SFX_ELEVEN · mezcla −14,35 LUFS.
- Miniatura Flow: B «NO TIENE PATAS» (subida); A, C1, C2 y `_hoja.jpg` en `miniatura/propuestas/`.

## Lecciones (ya en docs/estilo_linea3d.md § «Explicador con video real en cada suceso»)
- Fotos cargadas a resolución completa en float32 + muchos lectores de video abiertos = render sin memoria: fotos ≤ 1 400 px y máx. 2 `VideoCapture` por proceso.
- Lectura lenta de E: («Stream timeout» de OpenCV) deja cuadros NEGROS sin error: pasar `blackdetect` al MASTER siempre y rehacer el tramo.
- Un segmento cortado por memoria queda sin «moov atom» y la concatenación se para ahí (video de 81 s): revisar duraciones de `segmentos/` si `final` falla.

## Sesiones
- ✅ 14-nov-2026 (1, mismo hilo; la sesión de relevo no se pudo abrir por Remote Control): datos, guion, voz, clips, fotos, planos, música, SFX, render (2 cortes por memoria + 1 segmento negro por lectura lenta de E:, arreglados), miniatura Flow, subida programada.
