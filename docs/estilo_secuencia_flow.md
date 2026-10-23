# Estilo SECUENCIA (Google Flow) — canal Plastitube (alias `pieza_oculta`; antes «La Pieza Oculta»)

_Creado el 6-oct-2026 al traer a la Fábrica el proyecto `C:\Users\jaire\OneDrive\Documents\Platitube` (Remotion + extensión
`flowscrap`), que queda jubilado. Sus reglas, aprendidas en 19 episodios, están resumidas aquí; el detalle histórico sigue
en `Platitube/docs/pipeline.md` y `Platitube/docs/bitacora.md`._

Departamento aparte de la Fábrica: el video NO se dibuja por código. Es una secuencia de **clips de video e imágenes
generados en Google Flow** (plan Pro del usuario), uno por «beat» de la narración, en **plastilina / claymation**.
Empieza con 1–2 minutos de clips de video y sigue con imágenes fijas con cámara lenta. Claude es el cerebro (guion,
beats, prompts, revisión, armado); la generación en Flow corre sola.

## Flujo (motor `nucleo/secuencia.py`)
```
python fab.py nuevo <v> --secuencia     plantilla videos/_plantilla_secuencia (guion.py con MOTOR, SECUENCIA y FICHA)
python fab.py <v> voz | seleccionar | tiempo      voz de siempre (Chatterbox Dan + Whisper large-v3) -> timeline.json
python fab.py <v> beats                 cortes en pausas reales de la voz -> beats.json
   (Claude escribe prompts.json: un prompt por beat)
python fab.py <v> prompts               valida y exporta flow/prompts.txt + flow/escenas.json
   (generación en Flow; ver «Generar en Flow»)
   (mientras salen: el usuario ve el avance en el panel, 🎞 Montaje; bajar cada lote al salir y los clips en la misma tanda,
    regla del usuario del 20-oct-2026; docs/panel.md § «Vista Montaje»)
python fab.py <v> servir                puente con Flow: entrega los prompts y recibe cada resultado en medios/ (cero tokens)
python fab.py <v> medios                hojas previews/medios_NN.jpg (20 por hoja, con la frase de cada beat): MIRARLAS
python fab.py <v> vivo                  imágenes vivas: candidatas + previews/vivo_NN.jpg -> líneas FX en efectos.py
                                        (local, 0 tokens de API, ~10-15 min en 2.º plano; § «Imágenes vivas»)
python fab.py <v> video [--borrador] [--tramo 100-140]   arma salida/video_sin_audio.mp4 (~8 min de video en ~4 min)
python fab.py <v> ambiente | mezcla | video --hasta 60  VISTA PREVIA con audio: salida/<v>_AVANCE.mp4 (60 s en ~40 s)
python fab.py <v> musica | sfx | mezcla | final | verificar      (mezcla después de video: usa audio/ambiente.wav)
```
**Vista previa (19-oct-2026, `doce_animales`):** antes `video --hasta` se IGNORABA en este motor y renderizaba el video
entero. Ahora `--hasta N` = `--tramo 0-N` + los primeros N s de `audio/final.wav` → `salida/<v>_AVANCE.mp4`. Orden: `fx`
(si hay SFX) → `ambiente` (el render parcial no lo genera) → Lyria → `mezcla` → `video --hasta 60`. Render real medido:
865 s con 23 imágenes vivas + `VIVO_AUTO` en ~30 min (un solo proceso; sin vivos, ~8 min).
`comprobar`, `escena` y `prueba` no aplican a este motor. `medios/` nace en E: (junction), igual que `salida/`.

## Formato vertical (reels 9:16; añadido el 8-oct-2026 para la página «Que pasa en Juchipila», `E:\PaginaFace`)
`FORMATO = "vertical"` en guion.py → el armado, los efectos (`efectos.py`) y las hojas `medios` salen en 1080x1920. Sin esa
línea todo sigue en 1920x1080. Lo que cambia al producir:
- En Flow pedir **9:16**: `FlowAutomation.setConfig({aspectRatio:'9:16', ...})` y chip de ajustes en 9:16. Un medio en 16:9
  no falla, pero se recorta al centro y pierde dos tercios de la imagen.
- En la `FICHA` y los prompts: «vertical nine by sixteen», no «horizontal dieciséis nueve»; sujeto centrado, aire arriba y abajo.
- Rótulos de `efectos.py`: el ancho útil es 1080; `tam` ≤ ~120 para una palabra larga, y frases en dos rótulos apilados.
- Ritmo de reel: `video_s=0` o pocos clips, `img_s≈3`, `GAP` corto, 30-60 s en total (Facebook acepta reels de 3 a 90 s).
- Probado con imágenes sintéticas (armado, cámara dirigida, viñeta, temblor, rótulo, hojas). **Sin probar aún con medios
  reales de Flow en 9:16 ni con clips verticales.** Respaldos del motor anterior: `nucleo/secuencia*.py.bak_horizontal`.

## Preguntar al usuario al empezar cada episodio (no asumir)
1. Duración total (→ palabras: minutos × 170).
2. Minutos iniciales en VIDEO (`video_s`; suele pedir 1–2 min; 0 = todo imagen).
3. Duración de cada clip (`clip_s`: 4, 6, 8 o 10 s) y resolución (360p con descarga «720p mejorada» ahorra puntos; 720p directo).
Anotar las respuestas en `ESTADO.md` («Decisiones del episodio») y el tema en el historial antes de escribir guion
(no repetir temas: lista de ocupados en `Platitube/docs/historial-videos.md`).

## Guion (lo que cambia respecto a otros canales)
- Formato «historia de un invento / un genio», 170 palabras por minuto con Dan. La duración aprobada es la del audio real.
- **Números, años y siglos en letras** (regex `\d` sobre las frases debe dar cero).
- Retención: gancho con contradicción en < 20 s (nada de biografía ni saludo) → promesa y coste antes de 1:30 →
  escalada problema/intento fallido/coste mayor → renovar la curiosidad cada 30–60 s → eureka como acción visible →
  **cliffhanger con pregunta real a mitad del video** → consecuencias en cascada (persona → oficio → industria → hoy) →
  cierre circular que vuelve al gancho; el CTA va después.
- Densidad visual: en la zona de imagen, cada 11–13 palabras traen un sujeto, acción o detalle ilustrable.
  La voz no describe la imagen: suman información distinta.
- Ficha histórica antes de escribir: persona, género, fechas, ciudad, oficio, objetos de la época y elementos prohibidos.
  Whisper nunca es fuente de datos.

## Beats
- `beats` reparte: zona de video en beats de ~`clip_s` (no de 4 s: se desperdicia el clip pagado), luego ~4 s por imagen
  hasta el minuto 5 (15 por minuto) y ~6 s después (10 por minuto). Cada corte cae en una pausa real (inicio de frase o
  tras puntuación); las fronteras de zona se mueven al inicio de frase más cercano.
- Nunca repartir por tiempo fijo ni por conteo de palabras: se desincroniza (pasó en Post-it y en Josephine Cochrane).
- Si se rehace la voz o cambia el guion: `tiempo` → `beats` otra vez y revisar `prompts.json` beat por beat.

## Prompts (`prompts.json`: `{"scene-001": "...", ...}`)
Un prompt autosuficiente por beat, escrito **a partir de la frase exacta de ese beat** (campo `texto` de beats.json).
Cada prompt lleva, en este orden: estilo fijo + iluminación → sujeto y acción → escenario → cierre de exclusiones.
- **Triple anclaje** (la `FICHA` de guion.py se copia palabra por palabra):
  1. *Personaje*: nunca solo el nombre; siempre su ficha física y de vestuario completa (edad, pelo, ropa, colores).
  2. *Objeto estrella*: descripción técnica exacta y sus exclusiones («sin caballos, sin vapor»); nunca «la máquina».
  3. *Escenario*: locación explícita («al aire libre en un camino de tierra rural…»); nada de «fondo de época».
- Época: nombrar materiales de entonces y prohibir lo moderno que el modelo suele colar. Palabras trampa:
  «montacargas» da una carretilla moderna, «carruaje» mete caballos.
- Pedir siempre «full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette»: sin eso Flow
  dibuja la escena como viñeta con margen de papel alrededor (visto el 6-oct-2026).
- Sin texto en la imagen: cerrar con «Sin texto, sin letras, sin logotipos, sin objetos modernos».
- Beats de VIDEO: el mismo criterio de redacción; `prompts` les añade solo
  «Sin diálogo, sin conversación entre personajes, sin voces audibles.» (Flow mete voces si no se prohíbe).
- Mismo prompt para imagen que para video: no existe un «prompt de video».
- Variar encuadre entre beats seguidos (plano general, detalle de manos, objeto, rostro): la cámara del armado ya alterna
  acercar/alejar/derivar, pero dos imágenes casi iguales seguidas se leen como una sola.

## Clips de video: baratos y combinados (pedido del usuario, 6-oct-2026; PROBADO el 7-oct-2026 en `videos/bichos_invierno`)
- **Resultado de la prueba**: Vídeo · Omni 1.1 Flash · 360p · 10 s · x1 = **7 puntos** por clip (4 s, 6 s y 8 s cuestan menos). La
  extensión genera, pide «720p · Resolución mejorada» (Flow tarda 1-2 min en reescalar) y el archivo queda en
  `Descargas/flow-<v>/scene-XXX.mp4` a 1280x720, 24 fps, con audio. Copiarlo a `medios/` (o usar `/video_listo`). La plantilla
  «Scene one… Then <transición>… Scene two…» sí produce las dos escenas con la transición dibujada en medio.
- **Clips e imágenes en proyectos de Flow distintos** (7-oct-2026): con clips en la cuadrícula, el lote de imágenes llegó corrido una posición y con duplicados (hubo que rehacer las 101). Lote de imágenes = proyecto nuevo y vacío; revisar las 8 primeras contra su texto antes de dejarlo correr. Una sola pestaña de Flow abierta (con dos, la extensión lee el chip de la otra).
- Si la extensión falla con el video («Flow no confirmó 360p»), enviar a mano: chip en Vídeo · 360p · 10 s · x1, pegar el prompt, y al terminar ··· → Descargar → 720p Resolución mejorada (una descarga a la vez).
- Lanzar SIEMPRE un clip de prueba antes del lote, y antes elegir a mano el modelo de imagen «Nano Banana 2 Lite» si después
  vienen imágenes (Flow dejó «Nano Banana 2.1» por defecto y la extensión no lo reconoce).
- **360p + descarga mejorada**: `SECUENCIA["video_calidad"] = "360p"` (por defecto). El clip se genera en 360p (menos puntos que
  los 12 de 720p) y se baja con el menú de Flow «··· → Descargar → 720p · Resolución mejorada», que es gratis. Como esa
  descarga la hace el propio Flow (no hay URL), el puente la toma de la carpeta Descargas: ver «lote de VIDEO» abajo.
- **Dos escenas por clip** (`combinar=True`, `clip_s=10`): cada clip de 10 s cubre DOS momentos del guion unidos por una
  transición dibujada. `beats` da para cada beat de video `texto_a`, `texto_b` y `t_medio`. Mitad de generaciones para el
  mismo tiempo de video, y el corte interno ya viene animado. Plantilla del prompt (en inglés):
  `<estilo>. Scene one, first five seconds: <escena A>. Then <TRANSICIÓN>. Scene two, last five seconds: <escena B>. <cierre>`
  (`prompts` avisa si un clip combinado no dice «scene two»; la frase de «Sin diálogo» se añade sola).
- **Transiciones en el estilo** (elegir una distinta por clip, que tenga que ver con lo que pasa):
  - *Se redibuja*: «the ink lines of the scene come loose, swirl like ribbons and redraw themselves into scene two».
  - *Mancha de tinta*: «a splash of black ink spreads across the frame and washes away to reveal scene two».
  - *Paso de página*: «the scene peels away like a turning sketchbook page, revealing scene two drawn underneath».
  - *Empalme por forma*: «the camera pushes into the round hole of the nest until it fills the frame, and that dark circle
    becomes the round attic window of scene two» (buscar una forma común: círculo, hexágono, hoja, copo).
  - *Arrastre de un elemento*: «a gust of falling leaves sweeps across the frame and when it passes we are in scene two».
  - *El personaje guía*: «the wasp flies toward the camera, covers the frame with its striped body, and flies away to reveal scene two».
  - *Borrado y dibujo*: «a giant eraser rubs out the scene and a pencil quickly sketches scene two in its place».
  Regla: la transición no lleva texto y dura ~1 s; las dos escenas mantienen la FICHA (mismos personajes y objeto).
- Mirar el saldo de Flow antes de planear minutos de video y decirle al usuario cuántos clips alcanzan.
- **Duraciones mezcladas para gastar todo el saldo** (11-oct-2026): `SECUENCIA["clips_s"] = [10]*7 + [8]` sustituye a
  `video_s`/`clip_s`. `beats` reparte cada grupo de clips iguales en su propio tramo y anota `clip_s` en cada beat de
  video; `prompts` pone ese `videoDuration` a cada escena. Precios en 360p: 10 s = 7 puntos, 8 s = 6, 6 s = 5 (el de 10 s
  rinde más por punto). Con 55 puntos, 7×10 + 1×8 = 78 s.

## Generar en Flow
> **Antes de lanzar nada lee `docs/manual_wild_next_door.md` § «Hallazgos de sin_medicina» (12-oct-2026):** pestaña de Flow VISIBLE, saldo real,
> el falso error «no mostró la pestaña Video», lote de imágenes por pegado (más rápido que la extensión) y no volver a correr `beats` a medias.
> **Sin extensión / sin Chrome / con 0 puntos (11-oct-2026):** las IMÁGENES salen gratis y se pueden lanzar desde el navegador
> integrado del app con `nucleo/flow_integrado.py`; receta en `docs/manual_wild_next_door.md` § «Imágenes SIN extensión».
Claude lanza el lote manejando la extensión `flowscrap` (`Documents\flowscrap`, instalada en el Chrome del usuario) con
Claude in Chrome, y los resultados vuelven por un **puente local** (no por las descargas de Chrome). Probado el 6-oct-2026
con imágenes (2 de 2 llegaron a `medios/`); **video aún sin probar**.
1. Abrir Flow, crear un **proyecto nuevo** (uno por episodio) y no tocar esa pestaña mientras corre.
2. En el panel de ajustes de Flow dejar a mano **Imagen · 16:9 · Nano Banana 2 Lite · x1** (clic en el chip de modelo junto a
   la flecha de enviar; esperar ~2 s entre clics). Si el chip ya dice «Nano Banana 2 Lite», la extensión no abre el panel.
3. `python fab.py <v> servir` en segundo plano = puente en `http://127.0.0.1:8791` (solo responde a flow.google.com):
   entrega `flow/escenas.json`, recibe cada resultado en `medios/scene-XXX.*`, termina solo con «COMPLETO» o tras 20 min sin novedad.
4. Una llamada de JavaScript en la pestaña de Flow lanza el lote (no pegar los prompts: gastan tokens):
   ```js
   const e = await (await fetch('http://127.0.0.1:8791/escenas.json')).json();
   await FlowAutomation.clear();     // borra la cola anterior de la extensión (preguntar si no es nuestra)
   await FlowAutomation.setConfig({aspectRatio:'16:9', videoQuality:'720p', videoDuration:'8', count:'x1', autoDownload:false, initialVideoCount:0});
   await FlowAutomation.addScenes(e); await FlowAutomation.start(); e.length
   ```
   Cada escena trae su `mediaType` y, si es video, su `videoDuration`. El `videoQuality:'720p'` de arriba es el camino ya
   probado (12 puntos por clip de 8 s); el barato en 360p va en lote aparte (abajo).
5. Otra llamada instala el **recolector** en la página (cada 6 s manda al puente lo que ya tenga resultado):
   ```js
   window.__fab = window.__fab || {env: {}, log: []}; clearInterval(window.__fab.t);
   window.__fab.paso = async () => { const s = await FlowAutomation.status(); for (const it of s.flowQueue) {
     const u = it.images && it.images[0]; if (!u || window.__fab.env[it.sceneId] === u) continue;
     try { const b = await (await fetch(u)).blob();
       const r = await fetch('http://127.0.0.1:8791/medio/' + it.sceneId, {method:'POST', headers:{'content-type': b.type}, body: b});
       if (r.ok) window.__fab.env[it.sceneId] = u; else window.__fab.log.push(it.sceneId + ' http ' + r.status);
     } catch (err) { window.__fab.log.push(it.sceneId + ' ' + err.message); } } };
   window.__fab.t = setInterval(() => window.__fab.paso().catch(() => {}), 6000); await window.__fab.paso();
   ```
   Si la pestaña se recarga, el recolector se pierde: reinstalarlo (la cola de la extensión sí sobrevive).
   **Lote de VIDEO en 360p (va aparte del de imágenes)**: lanzar solo las escenas de video con
   `setConfig({videoQuality:'360p', videoDuration:'<clip_s>', autoDownload:true, downloadFolder:'flow-<v>'})` (cada escena de
   `flow/escenas.json` ya trae su `videoDuration`). La extensión baja cada clip por el menú «720p · Resolución mejorada»; el
   recolector, para las escenas de video, llama primero a `POST /video_listo/<sceneId>` (el puente toma el .mp4 más nuevo de
   Descargas y anota su alto) y solo si eso falla manda el archivo de 360p por `/medio`. Cambiar en el recolector la línea del
   `fetch(u)` por: `if (it.mediaType==='video') { const v = await fetch('http://127.0.0.1:8791/video_listo/'+it.sceneId,{method:'POST'}); if (v.ok) { window.__fab.env[it.sceneId]=u; continue; } }`.
   Con `autoDownload:true` las imágenes también se bajarían a Descargas como basura: por eso el lote de imágenes va con `false`.
   Comprobar con ffprobe que los clips llegaron en 720 de alto.
6. Avance sin gastar: `FlowAutomation.status()` devolviendo SOLO conteos por `status` y textos de `error` recortados
   (si la respuesta incluye URLs la herramienta la bloquea), o `GET /estado` del puente.
7. Fallidas: corregir el prompt, `prompts`, y relanzar solo esas (filtrar `e` por `sceneId`).
   Para relanzar una que YA llegó (rechazada en la revisión), sacar antes su archivo de `medios/` y volver a `servir`.
   En el relanzado NO esperar con `await` a `FlowAutomation.start()` ni encadenar `clear()+addScenes()+start()` en una
   llamada larga: el 7-oct-2026 la pestaña se congeló (timeout de 45 s). Si pasa: recargar la pestaña, reinstalar el
   recolector y llamar `FlowAutomation.start()` sin `await` (la cola sobrevive).
8. **¿Faltó alguna imagen?** (pregunta del usuario, 7-oct-2026, al ver en Flow un mosaico «Error: Hemos detectado actividad
   inusual… You have not been charged»): ese mosaico es un intento fallido que la extensión reintenta sola. Se comprueba
   con tres cosas: `GET /estado` del puente con `faltan: []`; `FlowAutomation.status()` con todos en `done`, sin `error`
   y sin dos escenas con la misma URL de imagen; y las hojas `medios` sin ningún `FALTA` y con cada imagen acorde a su
   frase. El aviso de «actividad inusual» es el freno por ritmo de Google: si se repite, bajar el ritmo.
- Por qué no las descargas: el 6-oct-2026 Chrome guardó los resultados como `<uuid>.jpg` en la raíz de Descargas, sin carpeta
  ni `scene-XXX` (causa sin identificar; quizá otra extensión renombra). `ingesta` queda solo como respaldo.
- `flowscrap` 0.14.5 (6-oct-2026): Flow ahora rotula la pestaña «Vídeo» con acento y la extensión solo buscaba «Video», así
  que no encontraba el panel de ajustes («Flow no expuso el control accesible: Imagen / Image»). Parcheado en
  `content/content.js` (respaldo `content.js.bak_0144`); **requiere recargar la extensión en chrome://extensions y refrescar
  la pestaña de Flow**. Sin eso, la primera escena de un lote puede fallar y repetirse.
- El depurador de `flowscrap` y el de Claude in Chrome NO chocaron en la prueba.
- **Video probado el 6-oct-2026**: funciona con la extensión 0.14.5 (clips de 8 s, 720p, 1280x720 con audio, ~2-5 MB). Cada clip
  de 8 s en 720p cuesta **12 puntos**; mirar el saldo ANTES de planear minutos de video. Al acabarse los puntos Flow muestra
  «No tienes saldo suficiente para realizar esta acción» y la extensión NO lo detecta (se queda en `processing`): hay que
  `FlowAutomation.stop()` + `clear()`, cerrar el cuadro del prompt, pasar el chip a Imagen a mano, **refrescar la pestaña** y
  relanzar esos beats con `mediaType:'image'` (quitando la frase de «Sin diálogo»).
- Recargar la extensión a mitad de un lote lo corta: después hay que refrescar la pestaña de Flow y reinstalar el recolector;
  la escena que estaba en vuelo queda en `processing` para siempre y se relanza aparte.
- Marco de viñeta en un clip (no se puede regenerar sin puntos): `SECUENCIA["recorte_por"] = {"scene-003": 0.04}` recorta por lado.
  Sirve también para quitar un rótulo pegado al borde (en `arana_techo` el clip 6 traía números de estatura: 0.09). Para
  detectar marcos, mide las esquinas de cada clip en varios tiempos (receta en `docs/manual_wild_next_door.md`).
- flowscrap puede saltar a 720p a mitad de un lote de clips en 360p: los que falten se mandan a mano (ver el manual).
- **Ingrediente en el navegador INTEGRADO sin portapapeles (23-oct-2026, `corn_flakes`):** el Ctrl+V del portapapeles de Windows
  no llega al panel, pero un pegado SINTÉTICO sí: en `javascript_tool`, `fetch` de la imagen (upload.wikimedia.org tiene CORS
  abierto; también un blob de la propia página), opcionalmente unir varias en un `<canvas>` → `File` → `const dt = new
  DataTransfer(); dt.items.add(file); ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true,
  cancelable: true}))` sobre `.ProseMirror`. Flow lo sube como ingrediente («Subidas»). Prompt y receta: `videos/corn_flakes/prompt_miniatura.md`.
- Miniatura: mismo camino (escenas `scene-901/902` en un `flow/escenas.json` temporal, luego `prompts` lo restaura). Nano Banana 2
  Lite escribió bien frases cortas en inglés entre comillas. Receta que gana en el nicho de insectos: dibujo sobre fondo claro,
  frase manuscrita de 2-4 palabras y flecha curva al sujeto.
- Respaldo manual: pegar `flow/prompts.txt` en el panel de `flowscrap` con «Videos iniciales» = nº de beats de video.
Lo aprendido con `flowscrap` (vale también para el script propio; detalle en `flowscrap/ARQUITECTURA.md`):
- Flow ignora eventos sintéticos: hay que escribir y hacer clic con eventos «de confianza» (CDP `Input.*`).
- Modelos: imagen «Nano Banana 2 Lite»; video «Omni 1.1 Flash» texto-a-video, x1, 16:9.
- **Proyecto nuevo de Flow por episodio y no tocar la interfaz mientras corre**: con eso no se cruzan nombres y
  contenidos; una generación a la vez para que cada `scene-XXX` sea de su prompt.
- Descarga: imagen por URL directa; video en 360p se baja por el menú «··· → Descargar → 720p · Resolución mejorada».
- Sin puntos de video: seguir con las imágenes y retomar los videos otro día (no reintentar en bucle).
- Rechazo de política en un prompt: reescribirlo, no insistir con el mismo texto.
- Ir a ritmo humano: automatizar la interfaz puede ir contra los términos de Google y «ilimitado» tiene freno por ritmo.

## Revisión (regla global de rigor, adaptada)
- Antes de armar: mirar TODAS las hojas `medios_NN.jpg` y abrir a tamaño completo las dudosas. Se rehace el prompt si:
  la imagen no ilustra la frase de su beat; el personaje cambió de cara, edad o ropa; el objeto estrella no es el de la
  ficha; aparece texto, algo moderno o un borde negro; hay manos o caras deformes.
- Tras armar: un cuadro por beat en los primeros minutos y uno cada ~3 s en el MASTER; pregunta de control:
  «¿qué palabra suena aquí y qué se ve?».
- Antes de `final`: duración de video = duración del audio; ningún `FALTA` en las hojas.

## Armado (qué hace `video`)
- Imagen: recorte a 16:9 sin deformar, cámara lenta distinta por beat (acercar, alejar, cuatro derivas), más recorrido
  cuanto más dura el beat. Clip: se ajusta a la duración del beat entre 0,6x y 1,6x; si aún falta, congela el último cuadro.
- Fundido corto entre beats (`fundido`, 0,2 s; 0 = corte seco). 1080p, x264 crf 18.
- **Sin subtítulos quemados** (regla global de la Fábrica). Platitube sí los llevaba palabra por palabra; si el usuario
  los quiere en este canal hay que añadirlos al motor.
- **Sonido de los clips de Flow al 50 % como ambiente** (pedido del usuario, 6-oct-2026): `video` genera `audio/ambiente.wav`
  (también `fab.py <v> ambiente`) y `mezcla` lo suma bajo la voz, con todos los clips igualados de nivel. Volumen general en
  `SECUENCIA["ambiente"]` (0.5; 0 = mudo) y por clip en `ambiente_por={"scene-004": 0.0}` para callar uno que suene mal
  (voces, música rara). Por eso `mezcla` va DESPUÉS de `video`. Escuchar el primer minuto antes de `final`.

## Imágenes vivas (pedido del usuario, 19-oct-2026; kit `nucleo/vivo.py`, probado en `videos/doce_animales`)
Las imágenes fijas de Flow se sentían quietas. Ahora pueden **respirar**: el personaje se separa del fondo y se mueve un
poco encima («como un baile»), y el fondo lleva **parallax 2.5D**. No en todas: donde el personaje destaca (primer plano,
dos personajes frente a frente, un objeto en mano como una lupa o un matamoscas). Ayuda a la regla de «nada quieto > 2 s».
- **Preparar** (desde `C:\FabricaAnimaciones`): `python fab.py <v> vivo` prepara todas las imágenes (profundidad con Depth
  Anything V2 Small en la GPU + recorte con rembg en la CPU; ~2 s por imagen, caché en `medios/capas/<beat>/` que se rehace
  sola si la imagen cambia), imprime las **candidatas** con su línea FX lista para pegar y hace la hoja
  `previews/vivo_NN.jpg`: original | capas numeradas | fondo rellenado | cuadro vivo en su pico. **Mírala antes de pegar.**
  `vivo hoja scene-032 scene-037` = hoja de esas aunque no sean candidatas · `vivo preparar --solo-prof` = solo profundidad.
- **Candidata** = máscara entre el 8 y el 55 % del cuadro con 1-3 componentes. Animación propuesta: 2-3 componentes → `baile`;
  uno que no toca el borde de abajo y queda alto → `flota`; uno grande (> 30 %) → `respira`; si no → `balanceo`.
  En Flow casi todo es candidato (145 de 191 en `doce_animales`), así que el selector **recomienda** solo las que más
  destacan: puntos = tamaño de la pieza principal (hasta 40 %) + 0,12 si hay dos personajes + 0,08 si el beat dura ≥ 3,5 s
  − 0,15 si el recorte es de `isnet-anime`; pieza principal ≥ 12 %, ~20 % de las imágenes, nunca dos beats seguidos. Las
  demás salen comentadas. **Aun así hay que mirar la hoja:** en `doce_animales`, de 38 recomendadas, 20 iban tal cual, 8
  necesitaban `capa` (cabeza cortada, suelo, el sueño de un personaje dormido) y 10 se descartaron (el recorte arrastraba
  el mapa entero, la multitud, la cama, la telaraña). Un murciélago colgado se mece con `pivote=(.5, 0)` (arriba).
- **Declarar** en `efectos.py`: `FX = [dict(tipo="vivo", beat="scene-092", anim="baile"), dict(tipo="vivo",
  beat="scene-016", anim="balanceo", capa=1), ...]`. `capa` = qué recortes se mueven (los números de la hoja; None = todos;
  los que no se mueven siguen en el fondo con sus píxeles originales, sin rellenar). Con `en="palabras"` la animación entra
  suave en esa palabra. `amp` (1.0) escala todo el movimiento, `par` (16 px) el parallax, `escala` (1.04) el recorte,
  `pivote` (`"pies"`, `"centro"` o (fx, fy) relativo a la caja), `modelo` (`"isnet-anime"` si el general falla).
- **Parallax en TODAS** las imágenes: `VIVO_AUTO = 12` en `efectos.py` (px; requiere `vivo preparar --solo-prof`). Sin
  recorte: el fondo se desplaza por profundidad en la dirección en que ya va la cámara del beat (radial si solo hay zoom).
- **Animaciones** (`vivo.mov`): `respira` (squash vertical 1,8 % en 2,8 s, giro 0,7°) · `balanceo` (3° en 2,6 s) ·
  `baile` (vaivén 3,2° + rebote squash dos veces por vaivén, sin despegar los pies; los personajes en contrafase) ·
  `flota` (sube y baja 6 px, deriva 3 px, giro 1,6°; pivote al centro) · `parallax` (rígido, sale 1,8x más que el fondo).
- **Cómo se esconde el hueco:** el recorte va un **4 % más grande** con pivote en los pies (idea del usuario: tapa el borde
  del relleno); lo que mide > 300 px de alto **gira proporcionalmente menos** (la lupa de 980 px gira 0,8°, el sapo 3°); los
  lados que tocan el borde de la imagen se estiran por fuera del cuadro (al girar no asoma nada); el relleno es
  `cv2.inpaint` TELEA a media resolución con la máscara dilatada ~8 px, para que el contorno negro se vaya con el personaje.
- **Lo que costó (no repetir):** rembg en este dibujo de tinta y color plano marca el CONTORNO y deja fuera el relleno de color
  (camisa, pantalón, el vidrio de la lupa): sin rellenar los huecos interiores el recorte sale hueco y deja ver el fondo
  borroso (halo azul). El kit rellena huecos (sellando los lados que tocan el borde de la imagen), usa un alfa casi binario
  (lo semitransparente de rembg dejaba ver el relleno a través del brazo blanco) y **corta los puentes**: la mariquita, la
  uña y la cabeza venían unidas por el contorno del dedo; las líneas largas y delgadas (contorno de la mesa o del suelo) se
  quedan en el fondo, las patas, antenas y mangos vuelven a su pieza. `isnet-general-use` recorta mejor que `isnet-anime`
  en este estilo (el anime se comía el suelo o el dedo, y en el perro con el sapo no vio nada); el kit prueba el general
  y solo si no da candidata pasa al anime.
- **BUG que costó un render (19-oct-2026, arreglado):** `fab.py <v> video` lanza `python -m secuencia`, que corre como
  módulo `__main__`; `secuencia_fx` importaba OTRA copia de `secuencia` y `isinstance(act, S.Imagen)` fallaba, así que el
  MASTER salió SIN imágenes vivas ni parallax aunque `fx hoja` y las pruebas sí los mostraban (usan otra ruta). Arreglo:
  alias en `sys.modules` al principio de `nucleo/secuencia.py`. **Comprobar en el MASTER, no en la hoja:** medir el vaivén
  de un beat `baile` con `cv2.phaseCorrelate` sobre el personaje (≈ 6 px en 3 s; 0,3 px = no se aplicó) o comparar con
  `previews/vivo_prueba/`. Con vivos el render tarda ~3x (un beat de 3 s: 2 s → 11 s).
- **Cuidado al elegir:** una cabeza cortada por el cuello (la capa 0 de un primer plano de persona) NO se anima: se rompe en
  el cuello; mueve la otra capa (`capa=1`). Fondos sin personaje claro → solo parallax (`VIVO_AUTO`).
- **Coste de render:** 35-40 ms por cuadro con solo parallax, 55-140 ms con recortes grandes (1080p).
- **Lugar en el flujo y coste total** (el usuario, 19-oct-2026): va DESPUÉS de aprobar las hojas de medios y ANTES de
  `video`. La preparación es una vez por video (~10-15 min para ~190 imágenes, en segundo plano, sin vigilarla) y no
  gasta tokens de API: todo es local. Lo único que consume tokens es revisar las hojas `vivo_NN.jpg` (~8 en un video de
  14 min). Render MEDIDO: 8 → 30 min con 23 vivos + `VIVO_AUTO` en 14:25 (la estimación previa era ~+6 min por ~30 beats animados y ~+15 min si `VIVO_AUTO` da parallax a todas). Sin prisa, ambos.

## Hallazgos de `corn_flakes` (23-oct-2026, primer video de la fórmula de marcas; todo en una sesión)
- **Prompts por TIEMPO, no por número de beat** (resuelve la mejora pendiente de `sin_medicina`): `videos/corn_flakes/_imagenes.py`
  describe CADA FRASE del guion (`"escena_i": [variante, …]`) y `hacer_prompts.py` cruza `beats.json` con `timeline.json`: cada beat
  toma la frase que más suena dentro de él (siguiente variante si se repite; si no hay, otro encuadre) y cada clip combinado toma
  A = frase en [t0, t_medio] y B = [t_medio, t1]. Se puede escribir ANTES de tener la voz y sobrevive a cualquier `beats`. Copiarlo.
- **Clips 720p con Claude in Chrome: esperar a que llegue cada archivo** a `E:\Downloads_jaire` antes de navegar al siguiente clip;
  si se cambia de página justo después de pulsar «720p · Resolución mejorada», la descarga se cancela (de 6 llegó 1). Receta: abrir
  `flow.google.com/project/<p>/edit/<id>` → `find` «Descargar contenido multimedia» → clic → `find` «720p Resolución mejorada» →
  clic → esperar el archivo con un bucle `ls` → siguiente. Los `edit/<id>` se sacan en el integrado haciendo clic en cada mosaico
  (el más viejo es el último del DOM) y leyendo el título que pone Flow.
- **Letterbox negro en los primeros 2-3 s** de 2 de 6 clips combinados (filas negras arriba y abajo: 64 y 83 px de 720). Medir la
  primera fila con media > 20 cada 0,5 s y fijar `recorte_por` (0.09 y 0.12). Whisper `small` en CPU sobre los clips encontró una
  voz de conferencia y un «hmm» → `ambiente_por` 0.
- **Nano Banana 2.1 en el integrado: 94 imágenes + 3 rehechas en ~25 min, 0 envíos perdidos** (lotes de 12 con `__ins` + Return + `__col`).
  Fallos típicos: «both brothers» dibujó a otros dos personajes y una mancha de colores (nombrar SIEMPRE las fichas); «small figures
  of the two brothers» dio niños (pedir «figurines… one is <ficha> in miniature»); un ciclista que no era el doctor.
- **Imágenes vivas en interiores de plastilina:** el recorte arrastra mesas, máquinas y edificios en ~la mitad de las candidatas
  (9 de 19 descartadas); con dos personajes separados funciona `baile`, y `capa=` salva las que mezclan persona + mueble.
- **Chatterbox (Dan) con «Will»:** la fonética «Uíl» falló en 10 frases (Uiri, Gil, Wee) y «Güil» solo funcionó a mitad de frase;
  al principio o al final de la frase no hubo grafía que pasara → reescribir sin el nombre («el hermano menor»). La FONETICA por
  CONTEXTO («Will va»: «Güil va») cambia solo esas frases y no regenera las que ya pasaron. «Llegan» al inicio se oyó «Ya eran».
- Voz con 2 semillas por frase: 103/123 a la primera (≈ 30 min en vez de 65); las que fallan se regeneran aparte.
- **El disco E: falló a mitad del video** (reintentos de E/S, reinicio USB, NTFS 55): `lyria_tramos.py armar` y ffmpeg daban
  «Error closing file: Invalid argument». Se pasó el video a C: (robocopy leyendo de E: + `rmdir` del junction). Ver memoria del disco.
- Tiempos: guion + investigación 40 min; voz 45 min; Flow (94 imágenes + 6 clips + descargas) ≈ 1 h; vivo 10 min; render con 10
  vivos + parallax 11 min (8:10); mezcla + final + verificar 5 min; subida 4 min.

## Pendiente del departamento
- Probar con puntos: clip en 360p + descarga mejorada por el puente, y un clip combinado de 10 s con transición.
- `flowscrap` 0.14.6 ya reconoce «No tienes saldo suficiente» (requiere recargar la extensión).
- Miniaturas: manual vigente en `Platitube/docs/manual-miniaturas.md` (un solo plano de plastilina, 1–3 palabras).
- (hecho el 7-oct-2026, ver «Música» abajo) Música por tramo emocional con Lyria en vez de la procedural.

## Música: SIEMPRE Lyria adaptada al guion (pedido del usuario, 7-oct-2026; vale para Plastitube y Wild Next Door)
La música procedural (`fab.py <v> musica`) ya no se usa en este departamento. En `guion.py` va un diccionario `LYRIA` con el
`estilo` del canal, una descripción musical e intensidad por escena y los `tramos` (grupos de escenas seguidas de ≤ ~170 s,
porque Lyria da ~3 min por pieza). Desde la carpeta del video: `python ../../nucleo/lyria_tramos.py` genera cada tramo con los
tiempos reales de `timeline.json`, los ajusta (±12 %) y los une con fundido cruzado en `audio/musica.wav`; luego `mezcla` y
`final`. Solo descripción musical en inglés, sin nombres propios ni palabras sensibles (el filtro bloquea «war», «bomb»…).
Ejemplo: `videos/teflon_sarten/guion.py`. Los videos ya publicados no se tocan (YouTube no deja cambiar el audio).
- El panel ya muestra el avance de este motor (docs/panel.md «Motor SECUENCIA»); falta reproducir ahí el video armado antes del MASTER.
