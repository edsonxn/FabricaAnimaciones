# La heredera del rancho · Capítulo 2 «¿Qué le pasó a Carmen?» — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: página de Facebook «Lágrimas y Venganza» (`novelas_ia`; E:\PaginaFace --pagina novelas_ia) · cap. 2 de la serie
- estilo: novela con IA = secuencia Flow realista con diálogo y lipsync → docs: docs/formato_novela_ia.md (+ videos/heredera_rancho/)
- etapa: ✅ CAP. 2 PUBLICADO en FB (23-oct, fb_id 1115639327878996, remezclado 23-oct) · siguiente: capítulo 3
- siguiente: capítulo 3 «¿Quién está en la tumba?» (nueva carpeta `heredera_cap3`; copiar guion.py; ver LA VERDAD en la biblia) CON LA
  RECETA «NOVELA, NO TRÁILER» de docs/formato_novela_ia.md (reprise + 3-4 escenas largas, plano/contraplano, música por momentos)

## Sesiones (plan de tramos · «continúa el video heredera_cap2» retoma aquí · protocolo docs/sesiones.md)
- alias: heredera cap 2, capítulo 2 de la heredera, heredera_cap2
- leer al empezar: este ESTADO + docs/formato_novela_ia.md § «Serie de muchos capítulos» + ESTADO de heredera_rancho § Lecciones
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion (13 planos, biblia ampliada), prompts; personajes nuevos; clips 1-13 | ✅ 23-oct | 1 repetición (política) |
| 2 | música (Flow Music / biblioteca), SFX, rótulos, mezcla, render, MASTER → revisión del usuario → FB | ✅ 23-oct | https://www.facebook.com/reel/1115639327878996/ (remezclado; el viejo 1485561113494147 queda para borrar a mano) |

## En curso (checkpoint)
- guion.py: 13 PLANOS (122 s de clips + rótulo final = 126 s); biblia ampliada en el docstring (LA VERDAD de Carmen y la
  tumba sin nombre, gancho del cap. 3 «¿Quién está en la tumba?»).
- `tiempo` → `beats` → `prompts` ✅ (flow/escenas.json, 13 videos).
- Flow: proyecto del cap. 1 https://flow.google.com/project/44a69a63-fd04-4493-9f93-fa2ab6d933d8 (mismos 7 personajes).
  Personajes NUEVOS: Doña Chela, Chuy, Carmen (Carmen = Lupe con 32 años). Escenarios nuevos: cocina, establo, balcón,
  puerta con candado, cuarto de Carmen (polvo) y su versión limpia (flashback), pasillo con lazos negros, capilla con tumba.
  Reusar del cap. 1: estudio, cuarto de Lupe.
- ✅ 23-oct: personajes Doña Chela=Sulafat, Chuy=Orus, Carmen=Despina (retrato + cuerpo + voz) y 7 escenarios nuevos (imágenes
  9:16 gratis: cocina, establo, balcón, puerta con candado, cuarto de Carmen con polvo y limpio, capilla con tumba). Siguiente: clips.
- Trucos: el selector de voz tiene BUSCADOR (clic en el campo, escribir el nombre, clic en la voz, «Añadir al personaje»); las capturas
  del panel van con retraso: comprobar el texto con JS antes de reescribir. En nombre: clic en el campo + Ctrl+A + escribir.
- ✅ ~23-oct: LOS 13 CLIPS LANZADOS (360p, 8/10 s, ingredientes = personajes + imagen del escenario; ≈ 87 pts). Automatizado por
  JS en la página: `__addIng` (busca en «Buscar recursos», clic en la opción «<nombre> Personaje/Imagen», «Añadir a petición»),
  `__dur(s)` (abre «Activador de ajustes» y elige 8/10 s; luego Escape REAL), prompt pegado con ClipboardEvent('paste') y
  envío con clic real en «Iniciar generación». Siguiente: descargar 720p en Chrome → medios/scene-001..013 → Whisper + hojas.
- ✅ 13 clips en medios/ (720p). Clip 6 falló por política («menores de edad», reembolsado) → repetido con «an adult woman».
  Gasto Flow ≈ 94 pts. Descarga en Chrome: abrir un clip (editor) → icono de descarga (1282,30) → «720p» (1302,152); la tira de
  miniaturas de arriba pasa al siguiente; vigilante scratchpad/esperar_clip.ps1 copia cada descarga a medios/scene-NNN.mp4.
- ✅ música: Flow Music «Ranch Mystery Score: Episode 2» (180 s) → audio/flowmusic_cap2.wav; audio/musica.wav = 0-100,5 s +
  fundido 3 s + 148,5-177,6 s (126 s). ✅ efectos.py + SFX (5, cuenta 3 de ElevenLabs, 310 créditos) → audio/fx.wav.

- ✅ ~13:10 MASTER salida/la_heredera_del_rancho_cap2_MASTER.mp4 (1080x1920, 126 s, −15,2 LUFS) + .srt por Whisper (30 líneas,
  diálogo completo). Hojas: previews/final_hoja.jpg y previews/cada3s.jpg (sin negros, caras consistentes).

## Lecciones de este video (solo lo no obvio)
- CRÍTICA DEL USUARIO (23-oct): música tapaba las voces (iba ~6 dB bajo el diálogo, sin ducking) y el capítulo parecía
  tráiler (13 momentos sueltos). Mezcla arreglada en el motor y cap. 1-2 remezclados (18,8 dB); estructura nueva para el cap. 3.
- Flow rechazó un clip por «menores de edad» con una adulta que saca ropa de una maleta: añadir «an adult woman» lo arregló.
- Un capítulo entero (13 clips) se lanza en ~10 min automatizando la página con JS (ver checkpoint) y se baja en ~12 min.
- Whisper sobre los clips: Flow a veces se salta parte de una línea larga (la fecha del clip 11); líneas de ≤ 12 palabras.
