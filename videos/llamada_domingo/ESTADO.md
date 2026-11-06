# Llamada de domingo (LogIA presenta) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia (LogIA, ATRASADO desde el 30-oct → hueco inmediato de `canales --actualizar`) · 16:9 · ~14 min
- estilo: DRAMA DE ANTOLOGÍA REALISTA (nuevo, 6-nov): clips de Flow con diálogo y lipsync (personajes de Flow con voz fija) + interfaz/keynote/noticiero por código (ui.py, voces ElevenLabs) → docs/formato_novela_ia.md
- etapa: ✅ MASTER 14:00 min subido a LogIA (be1zS17rxxI), privado, se publica sáb 7-nov 10:00 CDMX
- siguiente: visto bueno del usuario (si pide cambios: `video --rehacer t0-t1` + mezcla + final + `yt aplicar`); medir a 7 días

## Sesiones (UNA sesión, directo al MASTER — regla 5-nov)
- alias: llamada de domingo, black mirror, el capítulo de los clones, llamada_domingo
- leer al empezar: este ESTADO + guion.py (docstring = biblia) + docs/formato_novela_ia.md § «NOVELA, NO TRÁILER»
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion, Flow (personajes, imágenes, 48 clips), ui.py, voces Eleven, música, mezcla, MASTER, subir | ◐ parcial | 6-nov: guion listo |
| 2 | Flow (17 esc, 38 img, 48 clips), ui.py, música biblioteca, efectos, MASTER, subida | ✅ 6-nov | MASTER 840 s, diálogo/música 19,4 dB, -15,3 LUFS; be1zS17rxxI sáb 7-nov 10:00 |

## Decisiones (el usuario, 6-nov-2026)
- «como un capítulo de Black Mirror, mismo formato»; Claude decide estilo, personajes y guion; ~16 min; una sesión
- el estilo noir de LogIA «no funciona para el público»: buscar otro, con PERSONAJES con su personalidad y su voz
- presupuesto Flow: 357 pts (se restablece 22-nov) + 50 diarios → 48 clips = 316 pts; resto imagen (0 pts) y código

## En curso (checkpoint 6-nov ~14:00, sesión 1 cortada por contexto a 180k)
- Proyecto Flow: https://flow.google.com/project/5ccd1e3d-d989-48db-9b64-58e40811b4e4 (navegador integrado, 357 pts sin gastar)
- ✅ 7 PERSONAJES de Flow con retrato + cuerpo + voz fija (ids = /character/<id>):
  Ramón 011338c3-afd0-4506-a76f-f00ac55bd898 (Algenib) · Daniel aaafd8fb-73ac-47fe-a4dd-09222a607522 (Achird) ·
  Lucía 0baa0590-1907-4d62-b679-ee44f12cc761 (Kore) · Inés abfacf5c-3b94-4a85-9ccc-3eac0849cf4e (Sulafat) ·
  Carmen 7ca35696-00cc-49a6-af79-36696d383ae8 (Gacrux) · Chuy 7743c1ed-405e-49e8-9c01-12c83229ba01 (Orus) ·
  Mariana 2ee7d1cb-6df1-48e4-b099-9c32fdac556a (Leda)
- ✅ NOMBRES de los 7 en Flow (sesión 2, 6-nov).
- ✅ sesión 2: `flow_lote.py` (todo lo de Flow → flow/lote.json) + `flow_bundle.py` (paquete compacto que se inyecta por JS;
  el navegador integrado NO comparte portapapeles). 17 escenarios bajados a flow/esc/ (hoja previews/esc_hoja.jpg; nombres de
  Flow en `__ESCN` del paquete). Ingredientes por JS: abrir con button[aria-label=«Añadir ingredientes…»].click(), buscar con
  setter de value + evento input, clic en [role=option], clic en «Añadir a petición»; envío = clic real por ref. flow/_bajar.py
  baja URLs firmadas (añade el «=»). ✅ 33 imágenes bajadas: medios/scene-{001,007,011,023,026,030,031,040,045,050,059,064,068,074,080}.jpg (001/026/040/059/068
  = copia del escenario) + 23 fondos flow/bg/*.jpg para ui.py (keynote, anuncio, montaje de Ramón, noticiero, fiesta, oficina_dia,
  telefono_puerta, dos_telefonos, mesa_junta, laptop_noche). Hoja previews/img_hoja.jpg: todo bien; mirar a tamaño real
  scene-080 (¿se lee «Para el que viene»?) y bg/dos_telefonos (¿se ven los 2 teléfonos?).
- ✅ APERTURA en medios/: scene-002, 003, 004, 006, 008 (.mp4 720p, Whisper exacto; hoja previews/apertura_hoja.jpg, calidad muy
  buena). Originales en previews/originales/c0..c5. scene-005 actual TIENE una mujer detrás de Ramón al inicio y repite «el Paco
  ya no canta» → repetido (ver abajo); si el nuevo sale bien, sustituir medios/scene-005.mp4.
- ◐ ~15:20 LANZADOS 11 clips, en este orden: 005 (repetición «completely alone… says the line only once»), 014, 015, 017, 019,
  021, 027, 028, 029, 032, 033 (≈ 74 pts) y ~15:35 otros 16: 034, 035, 036, 038, 039, 041, 042, 043, 044, 046, 047, 048, 049,
  051, 052, 053 (≈ 107 pts) y ~15:45 los 16 últimos: 055, 056, 057, 060, 061, 062, 067, 069, 070, 071, 073, 076, 077, 078, 079,
  081 (≈ 106 pts; Lucía de luto «NOT her nurse scrubs» y Inés sin embarazo en __D[39]/[40]; quedan ≈ 30 pts para repetir).
  TODOS LOS CLIPS LANZADOS. Falta: bajar los 43 (720p) + Whisper para identificarlos y revisar. En la página: `__uno()` (JS) + clic real = un clip. Bajar: abrir cada clip (editor /edit/<id>), `__dl()` = botón «Descargar
  contenido multimedia» + «720p» por JS; las URL `…_720p_upsampled?…` llegan a `window.__urls` (gancho de fetch, ancla anulada) en
  ~30-40 s → flow/_bajar.py «previews/originales/{}.mp4» → IDENTIFICAR CADA CLIP POR SU DIÁLOGO con `python flow/_whisper.py
  <mp4…>` (faster-whisper medium, cuda) → copiar a medios/scene-NNN.mp4. Pendientes de lanzar: 034-039, 041-053, 055-062, 067-081
  (`flow/_clips_b.txt` y `_clips_c.txt` = prompts en \uXXXX para `Object.assign(window.__P, …)`; _clips_a ya inyectado).
- ✅ ~16:10 los 43 clips bajados, identificados por Whisper (flow/_asignar.py) y en medios/ (hoja previews/clips_hoja.jpg);
  076 repetido tras error de política; 071: 0-2,4 s silenciados (frase inventada «Daniel, tienes que ver esto»).
- ✅ música: Lyria dio 402 y Flow Music pide iniciar sesión con Google (OAuth: no sin permiso del usuario) → 7 piezas de la
  BIBLIOTECA por acto (la_sena, christa_pike ×4, duelo_cuerpo; otros canales) → audio/musica.wav 840 s. `tiempo` y `beats` hechos.
- ✅ efectos.py generado por flow/_efectos_gen.py (30 tramos de ambiente + radio/bolero/canario) y `fx` hecho (audio/fx.wav).
- ✅ miniatura Flow: salida/miniatura.jpg (1280x720, «NO ES TU HIJO»).
- ✅ ui.py (subagente): 22 piezas ui + 8 videollamadas (originales en previews/originales/scene-NNN_crudo.mp4), 23 voces
  Eleven (422 cr), hoja previews/ui_hoja.jpg. ~17:30 lanzado `video`.
- SIGUE: tras ui.py → fx → video → mezcla → final → verificar → tele → avisar → subir.
- ui.py: delegado a un subagente (sesión 2, ~15:25): 30 piezas por código + voces ElevenLabs + interfaz de videollamada para los
  clips `llamada` (004, 006, 042, 044, 052, 061, 076, 078).
- CÓMO LANZAR (todo probado en la sesión 2, en la página del proyecto; si la página se recargó, reinyectar):
  `python flow_bundle.py clip,llamada` escribe flow/_bundle_clip_llamada.js (diccionario común `window.__D` + `window.__P`
  {id: [prompt con ~N~, ingredientes, duración]} → `window.__get(id)`); los acentos pásalos como \uXXXX (json ensure_ascii).
  Duración: botón «8 s»/«10 s» por JS (abrir antes button[aria-label="Activador de ajustes"]) + tecla Escape REAL.
  Ingredientes: abrir button[aria-label="Añadir ingredientes a ventana para peticiones"] por JS, buscar con el setter nativo de
  value + evento input en input[placeholder="Buscar recursos"], .click() en el [role=option] («Don Ramón | Personaje» o el nombre
  de la imagen), .click() en el botón «Añadir a petición». Prompt: `.ProseMirror` + execCommand insertText. Envío: clic REAL por ref
  en «Iniciar generación». Los ingredientes se quitan solos tras cada envío.
  Galería VIRTUAL: para mapear resultados, recorrer `.cdk-virtual-scrollable` (scrollTop de 200 en 200), juntar los tiles y ordenar
  por posición (más nuevo arriba-izquierda) y casar con el orden de envío (las `Expires` de las URL firmadas crecen con él).
  flow/_bajar.py «plantilla» < «nombre uuid?query» baja URLs firmadas (añade el «=» que falta a la firma).
  Nombres de escenario en Flow: taller «Empty watch repair workshop inte…», taller_perfecto «Watch repair workshop interior»,
  oficina «Empty startup office at night», depto «Modern apartment interior at night», plaza «Empty plaza in Guadalajara neigh…»,
  cocina «Empty kitchen at night», porche «Porch of colorful house dusk», auto_lucia «Hatchback parked on Guadalajara…», taxi
  «Taxi interior at night in rain…», pasillo «Empty hospital corridor at night», hospital «Empty hospital room at night»,
  carretera «Modern car driving to Guadalajara», puerta «Closed watch-repair shop facade», puerta_dia «Don Ramón watch-repair
  shop stor…», hospital_ext «Hospital exterior at night», perfecto «Minimalist living room interior…», auditorio «Crowd in
  modern dark auditorium».
- Trucos Flow que funcionaron: texto en `.ProseMirror` con execCommand('insertText'); envío = clic REAL por ref en
  «Iniciar generación»; voz: botón «Selecciona una voz» (JS click) → clic real en «Buscar recursos» + escribir el nombre →
  `[role=option]` con .click() por JS (la voz queda puesta sola); «Crear cuerpo» con JS click. Pantalla del panel 1024x768,
  capturas a 800x600: usar refs (find), no coordenadas.
- SIGUIENTE: bajar la apertura 720p + Whisper + verla → clips 14-81 por actos → ui.py → voces ElevenLabs (ids abajo) → música → fx/mezcla/video/final → subir a LogIA
- ElevenLabs (cuenta 2, 29 685 cr): Valeria Roca = Gabriela hHjbwzYZW17oh0p05AKv · asistente = Ana María m7yTemJqdIqrcNleANfX ·
  locutor = Enrique Mondragón iDEmt5MnqUotdwCIVplo · anuncio = Eric tGjegxe7yxhGMzd3SOmH

## Hecho
- `guion.py`: 85 PLANOS (clip 48 · img 22 · ui 30 piezas por código), 839 s

## Falta
- [ ] Flow: proyecto, personajes, escenarios, imágenes, clips → medios/scene-NNN
- [ ] ui.py (piezas por código con su audio) · voces ElevenLabs
- [ ] música (biblioteca/Lyria/Flow Music), SFX, mezcla, video, final, verificar, miniatura Flow, subir

## Lecciones de este video (solo lo no obvio)
- 48 clips de Flow con personajes de voz fija: 47 de 48 a la primera (repetidos: 005 metió a una mujer que no existe; 076 error de
  política aleatorio). Whisper identifica cada clip por su diálogo: así no importa el orden en que lleguen las descargas.
- La galería de Flow es VIRTUAL (`.cdk-virtual-scrollable`): para mapear resultados hay que recorrerla por scrollTop.
- Un ajuste de vestuario que contradice la ficha del personaje (Lucía de luto vs. «nurse scrubs») hay que cambiarlo EN la ficha del
  prompt, no solo en la acción. Funcionó con una variante de la ficha para esos clips.
- Lyria sin saldo + Flow Music con OAuth pendiente → la biblioteca tenía piano/cuerdas de otros canales que funcionaron por acto.
- Delegar ui.py (30 piezas por código + voces) a un subagente ahorró la mitad del contexto de la sesión.
