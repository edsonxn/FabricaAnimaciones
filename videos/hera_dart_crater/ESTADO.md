# Hera ve el cráter de DART — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: T Menos Cero (`t_menos_cero`) · 4.º video · hueco vie 27-nov-2026 13:00 CDMX (19:00 UTC) · una sesión directo al MASTER
- estilo: LÍNEA 3D + VIDEO REAL de cada suceso + fotos en marcos de alambre · copiar `videos/starship_33_motores/` · doc `docs/estilo_linea3d.md` · kit nuevo `nucleo/linea3d_espacio.py` (asteroides, DART, Hera, estrellas, eyección)
- etapa: SUBIDO y PROGRAMADO · https://youtu.be/su3KWFK1xH0 · vie 27-nov-2026 13:00 CDMX (publishAt 2026-11-27T19:00:00Z)
- siguiente: nada (cerrado); tras 48 h mirar retención con `yt metricas t_menos_cero 90`; `fab.py hera_dart_crater limpiar` cuando se apruebe

## Cierre (27-nov-2026 07:45 CDMX)
- MASTER `salida/hera_dart_crater_MASTER.mp4` 9:37 1080p, Whisper CER medio 0.0024, desfase 0 ms; subido con miniatura y .srt; registrado en `canales/t_menos_cero.json` y BITACORA.
- Lecciones:
  - blackdetect (pix_th 0.06) en este estilo de fondo negro caza los planos 3D vacíos: 7,5 s de «¿SE MOVIÓ?» sin nada (barras ancladas a la palabra «setenta», 7 s después del inicio) y el punto de luz de «pregunta». Arreglo: el 3D del par girando + título grande desde T0, y cada texto sostenido hasta que entre el siguiente. Pasar blackdetect a la hoja de promesas ANTES del render.
  - La PC se durmió con el render a medias (8 h parado): el render retoma solo, pero en renders nocturnos pedir `request_keep_awake`.
  - Las fotos oficiales del día (esa.int, versión 1x; la @2x venía vacía) salvaron las promesas que los clips de la transmisión solo mostraban proyectadas.
  - ElevenLabs: cuentas 2 y 3 con pago fallido, la 1 sin cuota; los SFX salieron de la cuenta 4.

## Sesiones
- alias: hera, dart, cráter de dart, asteroide
- leer al empezar: este ESTADO + docs/estilo_linea3d.md

| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo hasta subido y programado | ✓ hecho | 26/27-nov · su3KWFK1xH0 |
