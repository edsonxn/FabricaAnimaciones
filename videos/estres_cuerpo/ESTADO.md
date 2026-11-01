# 5 cosas que el estrés le hace a tu cuerpo sin que te des cuenta — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cuerpo_en_neon (Cuerpo en Neón, @cuerpoenneon) · meta: mié 21-oct-2026 14:00 CDMX (20:00 UTC; ciclo 2 d tras agotado_cortisol)
- estilo: secuencia Flow + efectos (línea blanca sobre negro + un elemento en neón amarillo) → doc: docs/estilo_linea_neon.md
- etapa: PUBLICADO (https://youtu.be/rdzUobc1UAM, 13:23; registrado en canales/cuerpo_en_neon.json y BITACORA). Conciliado el 26-oct: este ESTADO no se había cerrado
- siguiente: cierre pendiente → hallazgos a docs/estilo_linea_neon.md (si faltan), medir retención, `biblioteca catalogar`, `limpiar` al aprobar

## Sesiones (plan de tramos · «continúa el video estres_cuerpo» retoma aquí · protocolo docs/sesiones.md)
- alias: estrés en el cuerpo, 5 cosas del estrés, video de 12 min de Cuerpo en Neón, 3.º del canal
- vista previa: no (el usuario, 20-oct-2026: «directo al MASTER»)
- leer al empezar: docs/estilo_linea_neon.md (§ «Hallazgos») · modelo de archivos: videos/agotado_cortisol/ (hacer_prompts.py, efectos.py)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion → voz → beats → prompts → Flow → efectos → SFX → Lyria → mezcla → render lanzado | ✅ 20-oct (2 cuentas) | el render sobrevivió al corte de cuenta y acabó a las 10:46 |
| 2 | rigor del MASTER → miniatura → youtube.json → subida (preguntar) → cierre (hallazgos en docs/estilo_linea_neon.md) | ◐ parcial 20-oct | rigor + 12 rótulos movidos + miniatura + youtube.json hechos; falta subir y cerrar |

## Decisiones del episodio (20-oct-2026)
- el usuario pidió ~12 min cubriendo VARIOS temas (variable nueva frente a freno_enojo/agotado: duración + recopilatorio)
- 5 lugares del cuerpo (pecho, panza, quijada/hombros, fuera del cuerpo, defensas), cada uno con técnica y estudio
- clips: «tenemos 50 puntos de Flow, aprovéchalos al inicio» → 7 clips x 10 s (49 puntos) en 0-70 s; luego ~130 imágenes
- protagonista nuevo: «el chico» (freno_enojo = el hombre, agotado = la mujer); ciudad: camión, oficina, cocina, clínica
- vista previa: no; directo al MASTER
- miniatura «ES EL ESTRÉS» (A2 de 4; alternativas en salida/_mini/) · título «5 Cosas Que el ESTRÉS Le Hace a Tu Cuerpo…»

## Hecho
- guion.py: 110 frases, 2013 palabras (~12-13 min), Lyria en 6 tramos · junction medios/ → E: creada
- voz ElevenLabs 110 frases, 747,7 s, 4 610 créditos (saldo ≈ 12 336) · TAIL/CER por frase en 2 (Kiecolt-Glaser) · beats 152
- Flow: 152/152 (7 clips Omni 1.1 Flash 360p→1080 + 145 Nano Banana 2 Lite), 49 puntos; 2 rótulos borrados (009, 147)
- efectos.py: 38 rótulos, 17 FX, 32 sonidos (21 SFX, 600 créditos) · Lyria 7 tramos (tramo 4 bloqueado 1 vez por política, salió al 2.º) · mezcla −14,3 LUFS, voz/(música+sfx) 13,6 dB
- panel: el botón 🎞 Montaje ahora sale en TODO video secuencia (regla del usuario, 20-oct: ver el montaje mientras se generan los medios)
- render 3879 s · rigor: previews/rigor_1-8.jpg (268 cuadros, uno cada 3 s), rigor_fase_1-2.jpg, sin quietos > 2 s; negro 0,7 s en
  0:56 = transición dentro del clip 6 (aceptada, como en agotado) · 12 rótulos movidos (x/y) y re-render solo de 11 tramos
  (previews/rigor_rotulos_v2.jpg) · youtube.json (14 capítulos, 8 fuentes, 7 DOI vía Crossref) · miniatura (prompt_miniatura.md)

## Lecciones (solo lo no obvio)
- `__col` puede pasar del límite de 45 s del navegador: bajarlo a 38 s; si se corta, recuperar los nuevos del DOM (los más recientes arriba) y cuadrar por la hora de `Expires` (~3,6 s entre envíos; un salto de ~7 s = una imagen que falló).
- Los pósters de los clips aparecen como `<img>` nuevos: marcar todo como visto tras los clips o `__col` los cuenta como imágenes.
- Clips rechazados: «his chest… as he breathes fast» y la cabeza anatómica con la amígdala; reescritos pasaron. La imagen «blood flowing away from the belly» falló; «arrows of energy» pasó.
- Rótulo al centro (y=.5) + el chico de pie al centro = el texto tapa justo el neón que se presenta (o la cara). Títulos de sección y
  palabras que nombran el neón: x≈.2 en el hueco lateral, partidas en 2 rótulos (y .43/.57) si son largas.
- Arreglar rótulos sin re-render total (secuencia no tiene `--rehacer` ni segmentos, y `final` BORRA video_sin_audio.mp4):
  pista de video del MASTER con `-c:v copy` → `video --tramo a-b` → empalme cuadro exacto (trim/concat, crf 18) → `final`.
  El tramo debe EMPEZAR antes del fundido entre beats (si empieza dentro, no conoce el beat anterior y salta).
- Crossref lista a Sierra como primer autor de doi:10.1007/s00127-004-0701-4; el primer autor real es Hunter (PubMed).
- El 20-oct, tras cambiar de cuenta de Claude, Flow pidió iniciar sesión en el navegador integrado (lo hizo el usuario).
