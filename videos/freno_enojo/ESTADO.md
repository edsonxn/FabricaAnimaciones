# Lo que pasa dentro de tu cuerpo cuando te callas el coraje — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cuerpo_en_neon (Cuerpo en Neón, @cuerpoenneon; aprobado por el usuario el 17-oct-2026) · sin fecha
- estilo: secuencia Flow + efectos (línea blanca sobre negro + un elemento en neón amarillo) → doc: docs/estilo_linea_neon.md
- etapa: PROGRAMADO sáb 17-oct-2026 14:00 CDMX (20:00 UTC) https://youtu.be/-zNE22UIjko
- siguiente: tras publicarse, revisar métricas a las 48 h y `python fab.py freno_enojo limpiar`

## Sesiones (plan de tramos · «continúa el video freno_enojo» retoma aquí · protocolo docs/sesiones.md)
- alias: freno del enojo, video del coraje, prueba de estilo neón
- vista previa: no (el usuario pidió el video completo, 1 sesión, sin supervisión: 16-oct-2026)
- leer al empezar: docs/estilo_secuencia_fx.md, docs/estilo_secuencia_flow.md § «Generar en Flow»
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo: guion → voz → beats → prompts → Flow → efectos → Lyria → render → final | ✅ 16-oct-2026 | todo en 1 sesión sin supervisión; MASTER + .srt en salida/ |

## Decisiones del episodio (preguntadas al usuario al empezar, 16-oct-2026)
- duración ~4 min horizontal · voz ElevenLabs NUEVA elegida por Claude: Alejandro Durán (sKgg4MPUDBy69X7iv3fA, eleven_v4)
- palabras gigantes SOLO en palabras clave (no karaoke) · 50 puntos de Flow → 7 clips de 10 s combinados al inicio (49 pts)
- Flow con sesión iniciada en el navegador integrado del app

## Hecho
- guion.py (627 palabras; hechos corregidos respecto al texto del usuario: ver docstring) · voz 237 s (1461 créditos ElevenLabs)
- 57 beats: 7 clips de Flow (6 de Omni Flash 360p reescalados a 1080; scene-002 = 2 imágenes + mp4 propio, el clip se rechazó
  2 veces por política) + 50 imágenes Nano Banana 2 Lite (029 y 036 rehechas; 036 con inpaint de rótulos V1-V3)
- efectos.py: FX `neon` nuevo en el núcleo (todo el video), 17 palabras clave, 13 SFX (490 créditos), Lyria 2 tramos
- render 20 min (4,5x tiempo real por el FX neon a cada cuadro) · mezcla -14,3 LUFS, voz/(música+sfx) 11,9 dB · verificar OK

## Falta
- [x] programado (pedido del usuario) · [ ] `python fab.py freno_enojo limpiar` tras publicarse
- [x] aprobado por el usuario; canal cuerpo_en_neon; youtube.json + miniatura Flow (Nano Banana 2.1, «LLORAS DE CORAJE»)

## Lecciones de este video (solo lo no obvio)
- Whisper escribe «Uno.» como «1.»: `CER_MAX_POR_FRASE` en las 5 frases que empiezan con número (falso positivo).
- Flow en el navegador integrado sirve también para CLIPS (sin extensión): todo el detalle en docs/estilo_linea_neon.md.
- El FX `neon` a cada cuadro hace el render ~2x más lento; si molesta, aplicarlo solo a beats con neón.
