# WARCRAFT (1983): El Guerrero y el Estofado de Poniente — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: sin canal — PRUEBA (el usuario, 18-oct-2026: «fue una prueba, no hay que considerarlo para ningún canal») · 16:9 · ~72 s · no se publica
- estilo: secuencia_flow «película de fantasía 1983» (35 mm, actores reales + plastilina/peluche/animatrónicos) → docs/estilo_secuencia_flow.md
- etapa: cerrado como prueba (MASTER 16-oct; sin miniatura, sin youtube.json, sin subida)
- siguiente: nada. Solo quedan los hallazgos de la receta «película 1983» para docs/estilo_secuencia_flow.md si se reutiliza

## Sesiones (plan de tramos · «continúa el video estofado» retoma aquí · protocolo docs/sesiones.md)
- alias: estofado, estofado de poniente, warcraft 1983, páramos de poniente
- vista previa: con audio completo (Lyria + SFX + mezcla) antes del render final
- leer al empezar: este ESTADO.md, `guion.py` (FICHA, PLANOS, ROTULOS, LYRIA) y docs/estilo_secuencia_flow.md § «Clips de video» y § «Generar en Flow»
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | idea, referencia, guion de 14 escenas | ✅ 15-oct | historia «Estofado de Poniente» elegida por el usuario; sin voz; 16:9 en Warcraft |
| 2 | SIN_VOZ en secuencia + prompts.json + 7 clips en Flow (49 pts) + Lyria | ✅ 16-oct (conciliado 17-oct) | 7 clips 720p × 10 s en `medios/` (a mano, saldo Flow agotado), Lyria por API → `audio/musica.wav` 72 s |
| 3 | rótulos, SFX, mezcla, armado, vista previa, final (miniatura/youtube.json/subida cancelados: era prueba) | ✅ 18-oct (cerrado como prueba) | hecho: rótulos, SFX ElevenLabs, mezcla, `final` → MASTER 1080p 92,6 s (72 s + 20 s pantalla final del canal), audio −16,8 dB medio / −1 dB pico, hoja cada 3 s revisada (sin cuadros negros salvo el fundido de 0 s). Falta: revisión del usuario, miniatura, youtube.json, subida lun 19-oct 11:00 |

## Decisiones del episodio (preguntadas al usuario el 15-oct-2026)
- duración total: ~72 s · todo en video: 7 clips × 10 s, 360p (descarga 720p mejorada gratis), combinar=True → 14 escenas
- voz: NINGUNA (montaje con música Lyria + foley, como la referencia) · rótulos de pergamino con serif amarilla (título, misión, «Continuará…»)
- referencia: https://youtu.be/3tNWWl7_NsI (endroxia, 416 mil vistas en 9 días). Héroe propio (chainmail + túnica roja), NO el de la referencia
- saldo Flow: 50 puntos (comprobar el saldo real antes de lanzar)

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- 17-oct (conciliación): el MASTER del 16-oct 08:43 existe y está completo; no rehacer nada. El `.srt` vacío es correcto (SIN_VOZ). Siguiente: revisión del usuario → miniatura → youtube.json → subida

## Hecho
- `guion.py`: FICHA en inglés (estilo 1983, 6 personajes/criaturas), 7 PLANOS combinados (A/transición/B), 3 ROTULOS, prompt LYRIA, 4 secciones (30 compases ≈ 72 s)
- `python fab.py canales --actualizar` al crear (15-oct)

## Falta
- [x] SIN_VOZ en `secuencia` · 7 clips · Lyria · SFX foley · rótulos · mezcla · MASTER (15/16-oct)
- [ ] Revisión del usuario del MASTER (+ encuesta corta y `--feedback`)
- [ ] Miniatura en Flow con ingredientes reales del juego (memoria «miniaturas Warcraft»)
- [ ] Título/descr. con datos (`python fab.py ideas cronicas_warcraft`); aclarar en la descripción «fan-made, no oficial de Blizzard»

## Archivos clave
- `guion.py` (FICHA, PLANOS, ROTULOS, LYRIA), luego `prompts.json`, `flow/escenas.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- Música de la referencia = OST de Blizzard; aquí SIEMPRE Lyria (regla 12-oct).
- La sesión del 16-oct avanzó hasta el MASTER sin anotarlo: el ESTADO decía «tramo 2 parcial». Registrar cada hito al momento (regla de checkpoints).
- `servir` (puente Flow) se apagó tras 20 min con 1/7: con el saldo agotado los clips 2-7 se bajaron a mano en el navegador integrado y se pusieron en `medios/scene-00N.mp4`.

## Cierre (regla del 12-oct-2026)
- [ ] subido, miniatura, programado y registrado (`canales/cronicas_warcraft.json`, BITACORA)
- [ ] HALLAZGOS y mejoras documentados en docs/estilo_secuencia_flow.md (receta «película 1983»)
