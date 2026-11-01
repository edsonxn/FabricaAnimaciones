# Tu nervio vago: el freno que apaga la ansiedad — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cuerpo_en_neon (Cuerpo en Neón, @cuerpoenneon) · PROGRAMADO vie 23-oct-2026 14:02 CDMX (publishAt 2026-10-23T20:02:00Z)
- estilo: secuencia Flow + efectos (línea blanca sobre negro + un elemento en neón amarillo) → doc: docs/estilo_linea_neon.md
- etapa: SUBIDO y PROGRAMADO https://youtu.be/NzMhKv8pl6w (privado; miniatura + .srt)
- siguiente: métricas a 7 días (30-oct) en canales/formula/cuerpo_en_neon.md · Short derivado (una técnica) · `limpiar` al aprobar

## Sesiones (plan de tramos · «continúa el video nervio_vago» retoma aquí · protocolo docs/sesiones.md)
- alias: nervio vago, video del vago, 4.º largo de Cuerpo en Neón
- vista previa: no (el usuario, 21-oct-2026: «1 sesión, directo al MASTER»)
- leer al empezar: docs/estilo_linea_neon.md (§ «Hallazgos») · modelo de archivos: videos/estres_cuerpo/
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion → voz → beats → prompts → Flow → efectos → SFX → Lyria → mezcla → render → final → rigor → subir y programar | ✅ 21-oct-2026 | todo en 1 sesión; render 1 h 41 min |

## Decisiones del episodio (21-oct-2026)
- tema elegido por el usuario entre 3 con datos: nervio vago (ref. Rebelde-Mente ×4,43, 1 M vistas) · ~9 min horizontal
- «tenemos 50 puntos en Flow, aprovéchalos para las primeras escenas» → 7 clips x 10 s (49 puntos) en 0-69 s; luego imágenes
- protagonista nuevo: «la chica» (bufanda y cárdigan) + Otto Loewi en grabado realista; el vago = la línea de neón
- técnicas distintas de estres_cuerpo: exhalación larga/resonancia, frío en el cuello, cantar, moverse, la gente
- título corto «¿Qué Es el NERVIO VAGO y Cómo Activarlo?» (prueba de título corto del canal) · miniatura «TU FRENO SECRETO» (m1 de 4)

## Hecho
- guion.py: 81 frases, 1533 palabras; 7 DOI verificados en Crossref + PubMed; aprobación FDA 2025 del SetPoint System verificada
- voz ElevenLabs 552,8 s (3235 créditos; la cuenta 1 quedó en 0, la 2 con ~12 400) · tiempo 593 s · 120 beats
- Flow 120/120: 7 clips Omni 1.1 Flash 360p→1080 (49 puntos, 0 rechazos; originales en medios/_360p) + 113 Nano Banana 2 Lite
  (076 «cirujano» falló 1 vez → «implante en la palma»; 045 con rótulo «airflow in» borrado por inpaint, original en _ronda1)
- efectos.py: 31 rótulos, 17 FX, 27 sonidos (17 SFX, 550 créditos) · Lyria 6 tramos (1 bloqueo de política en el 6.º, salió al 2.º)
- mezcla −14,0 LUFS, voz/(música+sfx) 13,4 dB · render 6082 s · MASTER 1080p 9:53, desfase 0, CER 0,021 (solo «Uno:/Dos:» → cifras)
- rigor: previews/rigor_1-6.jpg (198 cuadros, uno cada 3 s), sin quietos > 2 s; negros solo en apertura/cierre y ≤ 0,5 s
  dentro de las transiciones de los clips 4 (0:35) y 5 (0:43), aceptados como en agotado/estres
- youtube.json (13 capítulos, 8 fuentes) · subido y programado · registrado en canales/cuerpo_en_neon.json, BITACORA y fórmula

## Falta
- [ ] medir a 7 días (30-oct) · [ ] Short derivado (p. ej. «canta / tararea» o «frío en el cuello») · [ ] `limpiar` al aprobar

## Lecciones de este video (solo lo no obvio)
- Clips con anatomía: en un BUSTO de mármol o un MANIQUÍ de vidrio (no una persona) pasan la política de Flow a la primera (6 y 7).
- Tras bajar los clips con `mouseover` sintético, los pósters `<img>` desaparecen (quedan `<video>`): añadir a `__seen` las
  URLs `/image/<uuid>` de los clips y filtrar `__col` por `/image/` para que no cuenten como imágenes nuevas.
- `fx hoja` ANTES del render pilló 8 rótulos mal puestos (sobre el neón, cortados por el borde, y «→» sin glifo en Poppins:
  sale un cuadro; usar «·»). Rótulos de 2 palabras largas a x ≥ .8 se salen: partirlos en 2 líneas.
- Whisper: «Uno:/Dos:/Tres:/Cuatro:» → «1./2./…», «Loewi» → «Lowy», «Tracey» → «Tracy»: CER_MAX_POR_FRASE (falsos positivos).
  «¿Qué la baja?» lo oyó «¿Qué es la baja?»: reescrito a «¿Y qué es lo que la baja?».
- Un render de otra sesión estaba corriendo: el nuestro se encoló con un bucle que espera a que muera su PID (no dos a la vez).

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [x] HALLAZGOS documentados en docs/estilo_linea_neon.md § «Hallazgos de nervio_vago»
