# ¿Por qué el cielo es azul? (Short vertical) — ESTADO
- canal: kuriox · PROGRAMADO 20-oct-2026 18:00 CDMX (https://youtu.be/kCqZ1Bep07s, privado hasta la fecha, con .srt)
- estilo: boceto + guache vertical con el MOTOR COMPARTIDO `nucleo/sh_*.py` → docs/estilo_boceto_guache_mapa.md (variante vertical) · ejemplo: videos/primer_foton/
- etapa: voz ✓ · tiempo ✓ · escenas ✓ revisadas · sfx automáticos ✓ · música Lyria ✓ · mezcla ✓ · render ✓ · verificar ✓ · subido y programado
- siguiente: ver retención a las 48 h de publicarse (`python fab.py yt metricas kuriox 7`); `python fab.py cielo_azul limpiar` al aprobar

## Archivos clave
- `guion.py`, `coreo.py` (escenas), `escenas.py` (CAMBIOS entre escenas), `sonidos.py` (automáticos: `sh_motor.sonidos_auto`), `_prueba.py` / `run.ps1` (hoja de pruebas), `youtube.json`

## Lecciones (no obvias)
- `TRANSICIONES = [("continua", 0.1)] * N` en guion.py es OBLIGATORIO: sin ello el render mete transiciones al azar (glitch, zoom) encima de las pintadas.
- `tiempo` falla si DURACION no cabe en el rango de BPM (voz ~38 s no llega a 58 s): usar DURACION = None y `post` en la última escena.
- Whisper escribe «500» y `normaliza` lo vuelve «quinientos» (masculino): alias en ALIAS_QA si la frase dice «quinientas».
