# ¿Qué pasaría si la GRAVEDAD desapareciera 5 segundos? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: kuriox · meta: vie 23-oct-2026 14:00 CDMX (hueco del canal tras oxigeno_5s del lun 19-oct; ciclo 4 d) · video horizontal 16:9, 2:30 (150,0 s)
- estilo: kurzgesagt con la mascota Kuri → doc de estilo: docs/estilo_kurzgesagt.md · ejemplo a copiar: videos/oxigeno_5s/ y videos/dos_lunas/
- etapa: PROGRAMADO vie 23-oct-2026 14:00 CDMX (publishAt 2026-10-23T20:00:00Z); subido 17-oct (https://youtu.be/q1ye9-nJPlM, miniatura de Flow con texto + .srt)
- siguiente: ver retención a las 48 h de publicado; cierre de video (hallazgos al doc de estilo)

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: gravedad, gravedad 5 segundos, qué pasaría si la gravedad, kuriox gravedad
- vista previa: SÍ, primeros 25 s con audio completo (`salida/gravedad_5s_AVANCE.mp4` completado)
- leer al empezar: `docs/estilo_kurzgesagt.md`, `videos/gravedad_5s/escenas.py`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | 1 sesión completa: guion (~2 min) + voz + tiempo + Lyria + escenas plano secuencia + SFX/mezcla + vista previa `--hasta 25` + MASTER | ✓ hecho | `salida/gravedad_5_segundos_MASTER.mp4` (150,0 s, 126,3 MB), CER mezcla 0,0011, desfase 0,00 ms, 9 hojas 2×3 revisadas |

## Hecho
- Creado `videos/gravedad_5s` y actualizado el panel (`python fab.py canales --actualizar`: Crónicas de Tamriel se queda primero sin video el dom 18-oct 12:05).
- `guion.py` (6 escenas, 29 frases, 150,0 s total a 110 BPM) + `voz` (29/29 CER 0 con Dan) + `tiempo`.
- Plano secuencia continuo: `mundo_comun.py`, `anclas.py`, `estado.py`, `camara.py`, `kit_grav.py`, `mundo_paisaje.py`, `gente.py`, `mundo_espacio.py`, `ui_base.py`, `ui.py`, `sonido.py`, `escenas.py`, `miniaturas.py`.
- Audio completo: `musica` (Lyria 3 Pro, 150,0 s), `sfx` (65 eventos), `mezcla` (-14,00 LUFS, -1,18 dBTP, relación voz/fondo 13,0 dB).
- Vista previa con audio completo: `salida/gravedad_5s_AVANCE.mp4` (0..24 s).
- MASTER final verificado y revisado en 9 hojas 2×3 (`previews/master_00.jpg` .. `master_08.jpg`): `salida/gravedad_5_segundos_MASTER.mp4`, `salida/gravedad_5_segundos.srt`, `salida/gravedad_5_segundos_mini_tierra.jpg` y `youtube.json`.

## Falta
- Nada; programado.

## Archivos clave
- `guion.py`, `escenas.py`, `kit_grav.py`, `mundo_paisaje.py`, `mundo_espacio.py`, `gente.py`, `ui.py`, `sonido.py`, `miniaturas.py`, `youtube.json`
