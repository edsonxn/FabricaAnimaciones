# La heredera del rancho · Capítulo 1 — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: página de Facebook «Lágrimas y Venganza» (`novelas_ia`; E:\PaginaFace --pagina novelas_ia) · novela de MUCHOS capítulos
- estilo: novela con IA = secuencia Flow realista con diálogo y lipsync → docs: docs/formato_novela_ia.md (+ copiar videos/novela_altar/)
- etapa: ✅ CAP. 1 PUBLICADO en FB (23-oct) · el cap. 2 vive en `videos/heredera_cap2/` (publicado el 23-oct)
- siguiente: la serie sigue en `videos/heredera_cap2/ESTADO.md` → capítulo 3 «¿Quién está en la tumba?»

## Sesiones (plan de tramos · «continúa el video heredera_rancho» retoma aquí · protocolo docs/sesiones.md)
- alias: heredera, la heredera del rancho, heredera_rancho, novela 2
- vista previa: el usuario pidió ver los PRIMEROS CLIPS antes de hacer el capítulo entero (23-oct); al final, MASTER con audio completo
- leer al empezar: este ESTADO + docs/formato_novela_ia.md (y el ESTADO de novela_altar § Lecciones)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion (13 planos, biblia de la serie), prompts; personajes Flow; clips 1-4 → revisión del usuario | ✅ 23-oct | 7 personajes con voz, clips 1-4 aprobados |
| 2 | clips 5-13 + repeticiones | ✅ 23-oct | sin repeticiones |
| 3 | música (Flow Music), SFX, rótulos, mezcla, render, MASTER, publicar en FB | ✅ 23-oct | https://www.facebook.com/reel/1266763678961150/ (remezclado; el viejo 4105030019626908 queda para borrar a mano) |

## Decisiones (el usuario, 23-oct-2026)
- novela NUEVA de muchos capítulos (eligió «La heredera del rancho» de 3 premisas) · cap. 1 ≈ 2 min · vertical 9:16
- ver los primeros clips antes de gastar puntos en todo el capítulo

## En curso (checkpoint)
- guion.py: 13 PLANOS (122 s de clips + rótulo final = 126 s), FICHA de 7 personajes + 4 objetos, biblia de la serie en el docstring.
- `tiempo` (42 compases) → `beats` (13 clips) → `prompts` (flow/escenas.json) ✅
- Flow: proyecto https://flow.google.com/project/44a69a63-fd04-4493-9f93-fa2ab6d933d8 · PERSONAJES (retrato + cuerpo + voz):
  Lupe=Achernar, Doña Leonor=Kore, Licenciado Ibarra=Iapetus, Rodrigo=Rasalgethi, Valeria=Zephyr ✅. Faltan Emiliano
  (Algieba) y Don Aurelio (Algenib) para clips 8-9. Imágenes de escenario: «Study in traditional…» (estudio) y «Coffin in
  hacienda courtyard» (patio del velorio) ✅. ~10:20 clips 1-4 lanzados (ingredientes: personajes + escenario; 6/7 pts c/u).
  Siguiente: descargar 720p en Chrome → medios/scene-001..004.mp4 → enseñar al usuario (Montaje) → si aprueba, clips 5-13.
- Trucos de esta sesión: `window.__addIng([...])` (JS: botón «Añadir ingredientes…» → `[role=option]` → «Añadir a petición»,
  uno por uno), duración con el «Activador de ajustes», enviar = clic en la flecha (717,701) con el menú cerrado (Escape real).
  Voces: la lista es virtual, elegir por JS desplazando el contenedor hasta ver el nombre (un clic de ratón cae en otra voz).

- ~10:00 medios/scene-001..004.mp4 (720p, Whisper exacto salvo «senil»→«cenío» en el 4). Clip 2: Leonor salió con pelo
  oscuro (otra mujer) → repetición lanzada ~10:05 con «exactly the same woman as the Doña Leonor character reference».
  Emiliano (Algieba) y Don Aurelio (Algenib) creados ✅ (los 7 personajes listos).
- ~10:05 ✅ repetición del clip 2 OK (Leonor plateada; el malo en medios/_ronda1/). Vista previa sin música:
  previews/heredera_cap1_clips1-4.mp4 (36 s) enviada al usuario; ESPERA su visto bueno para los clips 5-13.
  Gasto en Flow hasta aquí: 33 puntos (4 clips + 1 repetición); personajes e imágenes gratis.
- 23-oct ~10:25 el usuario aprobó: «falta la música de novela, termina el primer capítulo completo y lo publicas en el face».
  Escenarios nuevos (gratis): «Servant bedroom…», «Fireplace lighting…», «Dark stone corridor…». Clips 5-13 LANZADOS.
  Siguiente: bajar 720p en Chrome (uno a uno) → medios/scene-005..013 → Whisper + hojas → música biblioteca → efectos →
  mezcla/video/final → publicar en FB (novelas_ia, tipo video porque > 90 s).
- ~11:00 ✅ LOS 13 CLIPS en medios/ (720p, Whisper exacto en todos; caras consistentes). Gasto Flow total ≈ 93 pts.
  ✅ efectos.py (5 rótulos, 2 FX, 4 SFX ElevenLabs cuenta 3 = 210 créditos; audio/fx.wav).
  ✅ MÚSICA: Lyria API 402 y biblioteca sin telenovela → el usuario eligió FLOW MUSIC (flowmusic.app, plan gratis; el usuario
  hizo el «Continuar con Google»). Pieza «Telenovela Drama» 177 s instrumental: audio/flowmusic_telenovela.wav (WAV público en
  storage.googleapis.com/producer-app-public/clips/<id>.wav, sacado de la respuesta POST /__api/clips). audio/musica.wav =
  0-103 s + fundido 3 s + 138-164 s (126 s). Siguiente: mezcla → video → final → revisión → publicar.

- ✅ ~11:20 MASTER salida/la_heredera_del_rancho_cap1_MASTER.mp4 (1080x1920, 126 s, −14,2 LUFS; diálogo completo por Whisper)
  → PUBLICADO en «Lágrimas y Venganza» (tipo video, fb_id 1266763678961150, remezclado 23-oct): https://www.facebook.com/reel/1266763678961150/

## Lecciones de este video (solo lo no obvio)
- **ORDEN en SIN_VOZ con diálogo: `video` ANTES de `mezcla`.** El render escribe audio/ambiente.wav (el sonido de los clips);
  una mezcla hecha antes sale solo con música + SFX (el usuario: «el video solo tiene música»). Orden: fx → música → video →
  mezcla → final. Comprobar con Whisper sobre el MASTER (no sobre los clips).
- Flow pone nombre a cada clip («Valeria and Rodrigo arguing…»): al elegir ingrediente por nombre, filtrar por la línea
  «Personaje»/«Imagen»; un VIDEO como ingrediente cambia a «duración según el ingrediente» y cobra 10 puntos.
- Con 4 personajes en un plano, Flow puede ignorar a uno (Leonor salió morena en el clip 2): revisar caras en la hoja.
