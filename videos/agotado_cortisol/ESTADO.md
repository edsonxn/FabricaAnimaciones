# Por qué estás agotado pero tu mente no se apaga de noche — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cuerpo_en_neon (Cuerpo en Neón, @cuerpoenneon) · PROGRAMADO lun 19-oct-2026 14:00 CDMX (20:00 UTC)
- estilo: secuencia Flow + efectos (línea blanca sobre negro + un elemento en neón amarillo) → doc: docs/estilo_linea_neon.md
- etapa: PROGRAMADO https://youtu.be/fLmNcI235FU (privado hasta el 19-oct 20:00 UTC)
- siguiente: el 26-oct medir 7 días (`yt videos` + `yt metricas`) en canales/formula/cuerpo_en_neon.md; luego `python fab.py agotado_cortisol limpiar`

## Sesiones (plan de tramos · «continúa el video agotado_cortisol» retoma aquí · protocolo docs/sesiones.md)
- alias: agotado y no duermes, video del cortisol, 2.º de Cuerpo en Neón
- vista previa: no (el usuario eligió 1 sesión sin vista previa, 17-oct-2026)
- leer al empezar: docs/estilo_linea_neon.md (§ «Hallazgos de agotado_cortisol»)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo: guion → voz → beats → prompts → Flow → efectos → Lyria → render → final → subida | ✅ 17-oct-2026 | 1 sesión; MASTER + .srt en salida/; subido y programado a pedido del usuario |

## Decisiones del episodio (17-oct-2026)
- tema elegido por el usuario entre 3 con datos (canales/formula/cuerpo_en_neon.md): «agotado y no duermes» (cortisol),
  4 canales fuera con × alto. Misma fórmula que freno_enojo (fisiología + 5 técnicas, voz Alejandro Durán); variable = tema.
- 7 clips de 10 s combinados (0-70 s, 49 puntos; el usuario confirmó el saldo) + 59 imágenes Nano Banana 2 Lite
- protagonista: «la mujer» (freno_enojo usó al hombre); escenarios nuevos, nada reciclado
- el usuario prefiere el FX neon en todo el video aunque el render vaya a 5x tiempo real (17-oct): no optimizarlo

## Hecho
- guion.py 751 palabras con ficha de hechos y DOI · voz ElevenLabs 49 frases, 238 s (~1880 créditos)
- 66 beats; 66/66 medios a la primera (clips 360p reescalados a 1080, originales en medios/_360p/; uuids en flow/)
- efectos.py: neón en todo el video, 17 palabras clave, 17 SFX (550 créditos) · Lyria API 2 tramos
- render 1553 s · mezcla -14,0 LUFS, voz/(música+sfx) 12,5 dB · verificar OK (solo falsos positivos «Uno.» → «1.»)
- rigor: 104 cuadros (previews/rigor_1-3.jpg) revisados: sin escenas vacías, rótulos dentro; el fundido a negro de 0,6 s
  dentro del clip 6 (0:55) y el destello amarillo de 0,9 s del foco (0:13) son transiciones del clip, aceptadas
- youtube.json (4 DOI verificados en Crossref) · miniatura «AGOTADO Y DESPIERTO» (Nano Banana 2.1; alternativa en salida/_mini/)
- subido https://youtu.be/fLmNcI235FU privado con publicación programada 2026-10-19T20:00:00Z; registrado en
  canales/cuerpo_en_neon.json, BITACORA y fórmula · separacion_min_horas del canal 96 → 48 (ciclo de 2 días)

## Falta
- [ ] 26-oct: fila de 7 días en canales/formula/cuerpo_en_neon.md · [ ] `limpiar` tras publicarse

## Lecciones de este video (solo lo no obvio)
- El banner «Te quedan pocos puntos» de Flow no es el saldo: preguntar antes de pasar a todo imagen (el chip dice el costo).
- Con [tired], «Son las 11» perdía el «Son» en 3 semillas: «Las 11 de la noche.» lo arregla.
- El panel no ve el avance del render del motor secuencia (cuenta segmentos/ y este motor no los escribe).

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado y registrado (`canales/cuerpo_en_neon.json`, BITACORA)
- [x] HALLAZGOS documentados en docs/estilo_linea_neon.md § «Hallazgos de agotado_cortisol»
