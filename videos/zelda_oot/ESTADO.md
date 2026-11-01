# Zelda: Ocarina of Time — su historia y los 12 secretos QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · gancho = remake de Switch 2 del 5-nov-2026
- estilo: secuencia_yt + fichas/MG con marcos de Flow (`nucleo/mg_zelda.py`, ui/) · voz ElevenLabs Hope → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ SUBIDO en privado y PROGRAMADO sáb 24-oct 18:00 CDMX (2026-10-25T00:00Z): https://youtu.be/tHGhx72-OTs (15:56)
- ✅ **PÚBLICO** desde el sáb 24-oct 10:00 (antes de lo programado: estaba para las 18:00) CDMX · https://youtu.be/tHGhx72-OTs (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
- siguiente: registro a 7 días en canales/formula/cronicas_gaming.md (~1-nov) · al aprobar: `fab.py zelda_oot limpiar`

## Sesiones (plan de tramos · «continúa el video zelda_oot» retoma aquí · protocolo docs/sesiones.md)
- alias: zelda, ocarina, ocarina of time, video de zelda · vista previa: 🎞 Montaje + MASTER (el usuario, 22-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 22-oct) | ✅ 22-oct | guion 96 frases · voz · 111 beats · Lyria 8 tramos · 3 renders · subido y programado |

## Decisiones del episodio (22-oct-2026, el usuario)
- Ángulo «historia + 12 secretos QUE IGNORASTE» (fórmula de banjo_tooie; variable = el juego). Formato `historia_y_12_secretos_secuencia_yt`.
- Crítica 1: «cuadros de texto poco trabajados, apóyate de Flow» → marcos pintados en Flow + kit `mg_zelda`.
- Crítica 2: «texto que se sale de la caja y elementos mal acomodados» → cajas medidas (`INTERIOR`, `caja()`, `ajustar()`).
- Crítica 3 (para FUTUROS videos): nada de carteles opacos que tapen el video → fichas translúcidas tipo Tamriel, adaptadas a cada
  juego (regla en docs/estilo_secuencia_yt.md y memoria). Este video salió con las tablillas opacas.

## Hecho
- Datos verificados por agente (cabecera de guion.py). Voz Hope 5 672 créditos (saldo ≈ 33 270). 13 falsas alarmas de Whisper → tolerancias.
- Clips: plan por frase (`plan_clips.py`, `mapa_clips.md`) sobre la serie ZeldaCentral NSO 1080p60 + externos; 21 rehechos en total.
- MG nuevos: ocarina (5 botones + canciones), paradoja de la canción de la tormenta (sello NADIE), versiones del cartucho, tres
  líneas temporales, escalera de recompensas de Skulltulas. 118 efectos, 60 pegatinas (cinta de Flow).
- Lyria 8 tramos nuevos (la biblioteca solo tenía épica de Warcraft); SFX: sello de la biblioteca + 5 nuevos. Mezcla -14,3 LUFS.
- Miniatura Flow con ingredientes reales (prompt_miniatura.md). youtube.json con capítulos y créditos. Música y SFX catalogados.

## Fuentes de clips
- Ver `mapa_clips.md` (segundo exacto de cada parte de ZeldaCentral y de los videos externos) y `salida/creditos.txt`.

## Lecciones de este video (solo lo no obvio)
- Ctrl+V desde Claude no llega al navegador integrado: ingredientes de miniatura por Chrome (`file_upload`), ver prompt_miniatura.md.
- Whisper en CPU (FAB_WHISPER_CPU=1) ~1 frase/min cuando otra sesión tiene la GPU; eval.json es caché (se puede relanzar).
- 3 renders (~35-80 min c/u) por negros DENTRO de clips: medir el brillo de TODOS los clips antes del primer render.
- `nucleo/recortar_ui.py`: quita solo el blanco conectado al borde (sirve para cualquier pieza de interfaz de Flow).

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal, miniatura y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [x] HALLAZGOS documentados (docs/estilo_secuencia_yt.md § Crónicas del gaming; memoria)
- [ ] registro a 7 días en la fórmula del canal
