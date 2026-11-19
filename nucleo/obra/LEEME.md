# «La obra»: vista RTS de lo que se está produciendo (pedido del usuario, 19-nov-2026)

Pedido: al hacer clic en una obra de la ruleta «En producción» (pestaña «Canales», `nucleo/estadisticas.html`, tarjetas
`.tl-p`) se abre un pop-up en la misma ventana con una escena tipo estrategia en tiempo real (vista 3/4 isométrica, bosque):
aldeanos llevan recursos (madera, silicio, componentes de computadora, rollos de película) al edificio en obra, otros
martillan, la cámara se mueve sola como en un RTS y arriba del edificio se ven vistazos de lo que se genera del video
(como el monitor del robotaller). La misma escena reemplaza al robotaller en la tele (tablero de Puente TV).
**Arte y sonidos ORIGINALES** «en el espíritu de» los RTS medievales de fines de los 90: nada copiado de Age of Empires
(ni sprites, ni sonidos, ni nombre en pantalla). Ya se le dijo al usuario.

## Hecho (19-nov)
- `flow/*.jpg`: 8 dibujos de Flow (Nano Banana 2.1, 0 puntos, fondo magenta). Proyecto Flow «nov 19 - 12:54».
- `preparar_arte.py` → `img/*.png` (sprites al doble de su tamaño en pantalla, transparencia limpia) + `img/pasto.jpg`,
  `img/tierra.jpg` (512 px, repetibles) + `img/hoja.jpg` (revisión). Piezas: cimientos, armazon, taller (edificio por
  etapas); madera, silicio, componentes, pelicula (montones de recursos); roca, piedras, arbusto, arbusto_flor, tocon,
  barril, cajas, carretilla, costal, cerca; roble, pino, abedul, castano, pino_chico, arce.
- Pantalla pintada en el techo de `img/taller.png` (758x800): paralelogramo TL (416,172), TR (599,81), BL (416,314),
  BR (600,218). Para pintar ahí: `ctx.transform(183/w, -91/w, 0, 142/h, 416, 172)` en coordenadas del sprite.
- `sonido/*.mp3` (ElevenLabs, 332 créditos; NO va a git): martillo_1-3, hacha_1-2, pico_1-2, deposito_1-2, sierra,
  ambiente (20 s, en bucle), listo (fanfarria).
- Datos ya listos en `estadisticas.py`: `datos_panel()` → cada canal trae `prod` (video, titulo, progreso, etapa_n, mini,
  mini_final, sale, atrasado) y `libres` (huecos por llenar), `logo`, `color`.

## Falta (en orden)
1. **`nucleo/panel_obra.html`** servida en `/v2/obra` (`?video=<v>` enfoca esa obra; `?tele=1` = sin sonido, media
   resolución, menos aldeanos). Rutas en `panel_v2.py` → `get()` (se recarga solo, sin reiniciar el panel): `/v2/obra`,
   `/v2/obra/img/<n>`, `/v2/obra/sonido/<n>` (lista blanca de nombres), `/api/v2/obra`. En `panel_v2.py` el panel es `P`
   (`P.estado_cache()`), NO `import panel` (el panel corre como `__main__`): `estadisticas.datos_panel(P.estado_cache(30)["proyectos"])`.
   La API: obras [{video, titulo, canal, canal_nombre, color, progreso, etapa_n, sale, atrasado, vistazos: [/media/<v>/previews/*.jpg …]}],
   libres [{canal_nombre, logo, sale}].
2. Motor (canvas 2D): mundo 3200x1800; suelo pre-dibujado una vez (patrón de pasto, manchas, claro de tierra con máscara
   de degradados alrededor de cada obra, caminos de tierra a cada recurso); árboles de la orilla «horneados» en el suelo,
   los cercanos a la acción se dibujan cada cuadro ordenados por y; sombras elípticas.
   Obras: 1 → (1600,950); 2 → (1150,900),(2100,1000); 3 → (1000,1000),(1700,800),(2350,1100); 0 → taller terminado y
   letrero «Sin obras». Etapa por progreso: <0,3 cimientos · <0,7 armazón · ≥0,7 taller (+ andamio dibujado si <0,97);
   al cambiar de etapa, nube de polvo. Barra de construcción verde encima (estilo RTS). Vistazos cada 4 s: en la pantalla
   del techo del taller (transform de arriba) o, en etapas 1-2, en un letrero de obra flotante con cuerdas.
   Recursos: madera (bosque oeste ~500,900, un leñador talando), silicio (afloramiento norte ~1500,330), componentes
   (este ~2750,600), película (carreta sureste ~2600,1500). Huecos «por llenar»: terreno con estacas y letrero del canal.
   Aldeanos dibujados por código (~34 px de alto): piernas alternas, túnica del color del canal, cabeza, sombrero de paja
   en algunos, herramienta; recolectores: ir → trabajar 3-5 s (hacha/pico/recoger, con sonido) → volver cargando el
   recurso (sprite chico) → descargar (sonido) → repetir; constructores alrededor de la obra martillando.
   Cámara RTS: recorrido (obra de cerca, seguir a un aldeano 6 s, zona de recurso, vista general) con resorte suave; en el
   pop-up arrastrar/rueda la mueven a mano y a los 10 s vuelve al recorrido. HUD en HTML: barra de recursos arriba
   (cuenta entregas), minimapa abajo a la izquierda (obras, aldeanos, rectángulo de cámara), panel de la obra abajo
   (título, canal, % y etapa, «sale <fecha>»). Sonido WebAudio: ambiente en bucle 0,35; golpes con volumen y paneo por
   distancia a la cámara; botón 🔊; si el AudioContext queda suspendido, «Toca para sonido». `window.__pausa(si)` para la tele.
3. **Pop-up** en `estadisticas.html`: clic en `.tl-p` (no `.libre`) → capa fija con `<iframe src="/v2/obra?video=<v>" allow="autoplay">`,
   ✕ y Esc cierran; `cursor:pointer` en las obras. Ojo: el arrastre de la ruleta ya cancela clics (`TL.mov`).
4. **Tele**: `D:\PuenteTV\tablero\tv.html` línea ~476 `$("fVivo").src=conK("/v2/vivo")` → `/v2/obra?tele=1`; en
   `D:\PuenteTV\tablero\servidor.py` agregar a la lista blanca del proxy `/v2/obra`, `/api/v2/obra`, `^/v2/obra/(img|sonido)/…`
   y `/media/<v>/previews|salida/*.jpg`; reiniciar SOLO ese servidor (pythonw en el 8741; LEEME de esa carpeta). Medir
   fluidez con `bash D:/PuenteTV/tablero/medir_fps.sh "tv?vista=1"` (robotaller daba ~32 fps). Título del chip de la vista 1.
5. Probar en el panel (navegador integrado, `http://127.0.0.1:8765/canales` → clic en una obra) y en la tele; commit
   (sin `sonido/` ni `flow/`, ya en .gitignore); documentar en `docs/panel.md` y `docs/tele.md`.

## Sesión 2 (19-nov) — hecho; la sesión 3 terminó los aldeanos (abajo)
Hecho y probado en el navegador integrado:
- `nucleo/panel_obra.html` (motor completo: suelo horneado, obras por etapa con pantalla en el techo / letrero flotante,
  barra RTS, recursos, huecos por llenar, aldeanos dibujados POR CÓDIGO, partículas, cámara RTS + mano, HUD, minimapa,
  sonido WebAudio, `?tele=1`, `__pausa`). Rutas en `panel_v2.py` (`_obra_get`, `obra_datos` con caché de 20 s,
  vistazos = `/v2/mini/<v>/previews/*.jpg?w=480`). `/v2/obra?video=cod_mandela3` se ve bien.
- Pop-up en `estadisticas.html` (`data-video` en `.tl-p`, `abrirObra`, ✕/Esc/clic fuera; Esc dentro del iframe llega por
  postMessage `obra:cerrar`). Probado: clic en la obra de la ruleta abre la escena.
- Tele: `D:\PuenteTV	ablero	v.html` → `/v2/obra?tele=1` (chip, pestaña y NOMBRES = «La obra»); `servidor.py` con
  `/v2/obra`, `/api/v2/obra`, `/v2/obra/(img|sonido)/…`, `/media/<v>/(previews|salida)/…` en la lista blanca; servidor 8741
  reiniciado y probado con curl (200 en todo). Respaldos: `servidor.py.bak_obra`, `tv.html.bak_obra`. FALTA medir fps.

PEDIDO NUEVO del usuario (19-nov): «los aldeanos hazlos con secuencia de imágenes de Flow para que parezca de age of
empire, en 1 imagen una hoja de varias imágenes para la animación» (arte ORIGINAL, estilo RTS de fines de los 90).
- Hojas de Flow ya bajadas en `flow/` (mismo aldeano, túnica azul pura #1f4fff para teñirla con el color del canal):
  `ald_caminar.jpg` (12 cuadros en 2 filas), `ald_cargar.jpg` (8, costal al hombro), `ald_hacha.jpg` (6: reposo, sube,
  arriba, baja, golpe abajo, recupera), `ald_martillo.jpg` (6), `ald_recoger.jpg` (6: se agacha por una caja y la levanta).
- FALTA `ald_pico.jpg`: existe en el proyecto Flow «nov 19 - 12:54» (media df06d431-aa1c-4b29-bff3-7c41dd215fcb, 2.ª fila
  de la lista), pero su URL `lh3.googleusercontent.com/asb/…` pide cookies; la regeneración dio PUBLIC_ERROR_UNUSUAL_ACTIVITY
  (no insistir en seguida). Bajarla con el botón Descargar desde Chrome o regenerarla más tarde; si no, el minero usa `hacha`.
  Truco que sí funcionó: gancho en `window.fetch` que saca `image/<uuid>?Expires…Signature…` de las respuestas
  `batchexecute` (ogiZ0b) y curl sin cookies a `https://flow-content.google/image/<uuid>?Expires=…&KeyName=labs-flow-prod-cdn-key&Signature=…`.
Siguiente, en orden:
1. `preparar_arte.py aldeanos`: segmentar cada hoja por las manchas de túnica (una por cuadro, en orden de filas), juntar a
   cada una sus pedazos (herramienta, caja, costal), escalar por la altura mediana de la túnica (aldeano ~40 px en
   pantalla → 80 px en el archivo), ancla = centro de la túnica y fila más baja de las botas; celdas iguales por animación
   → `img/ald_<anim>.png` + `img/aldeanos.json` {anim: {n, w, h, ax, ay}}; teñir la túnica (HSV: tono del canal, V/S
   escalados) para las 8 tintas de `COL` → `img/ald_<anim>_<0-7>.png`. Ampliar `OBRA_IMG` si hace falta (ya acepta `[a-z_0-9]`).
2. En `panel_obra.html` cambiar `dibAld` por los sprites (espejo con scale(-1,1) al ir a la izquierda): caminar por
   distancia (`a.paso`), `cargar` al volver, `hacha`/`martillo`/`pico` por `a.fase` con el golpe (sonido) en el cuadro del
   impacto, `recoger` en componentes/película y al descargar; la sierra usa `martillo`. Quitar la carga dibujada encima.
3. Medir fps en la tele: `bash D:/PuenteTV/tablero/medir_fps.sh "tv?vista=1"` (robotaller ~32).
4. Docs (`docs/panel.md`, `docs/tele.md`), commit en español sin `sonido/` ni `flow/` y push.

## Sesión 3 (19-nov): aldeanos con sprites de Flow ✔
- `preparar_arte.py aldeanos` → `img/ald_<anim>.png` + `img/ald_<anim>_<0-7>.png` (8 tintas) + `img/aldeanos.json` +
  `img/hoja_aldeanos.jpg`, y reescribe `ALD_META` en `panel_obra.html`. caminar 12 · cargar 8 · hacha 6 · martillo 6 · recoger 6.
- `panel_obra.html`: `dibAld` dibuja los sprites (`aldPose`, `aldTira`); se quitaron el aldeano por código y `herramienta`.
  Probado en el navegador integrado (`/v2/obra?video=cod_mandela3`, pop-up `abrirObra` de `/canales`, `?tele=1`), sin errores.
- Pendiente: (1) `flow/ald_pico.jpg` (6 cuadros, mismo aldeano con pico) → correr `preparar_arte.py aldeanos` y el minero
  la usa solo; (2) medir fps en la tele: ADB no conectaba (activar depuración inalámbrica y `adb connect`), luego
  `bash D:/PuenteTV/tablero/medir_fps.sh "tv?vista=1"`.

## Sesión 3b (19-nov): materiales reales ✔
Recursos = materiales del video (guion, voz, clips, efectos, música) con su contador, de `obra_materiales()` en
`panel_v2.py`; pilas frente a la obra, letreros en cada sitio, aldeanos solo por lo que falta y llegada al subir una cuenta
real. Detalle en `docs/panel.md` § «Vista «La obra»». Probado con `wow_ruta_forever` (y cuentas simuladas que suben y se completan).

## Sesión 4 (19-nov): animaciones de OCIO ✔ (abajo, el cierre)
Pedido (el usuario vía la sesión «App de Google TV para ver La obra»): «cuando un aldeano esté inactivo ponlo dormido o
sentado con alguna animación, genera las animaciones nuevas para que no se vean solo ahí congelados».
NO tocar `nucleo/panel_obra.html` (lo edita la sesión «Continúa La obra — capas», local_a6e54548-cb50-47c1-880b-8336c648d887).
Hecho:
- `flow/ald_pico.jpg` bajada (6 cuadros: listo, sube, medio, arriba, baja, GOLPE). Su golpe es el cuadro 5; para igualar
  el convenio del hacha (golpe = cuadro 4, recupera = 5) reordenar en `preparar_arte.py` a [0, 2, 3, 4, 5, 1].
  Al bajarla sin gancho se abrió una descarga del navegador integrado (`E:\Downloads_jaire98ff3b5-….tmp`): borrar ese .tmp.
Falta, en orden:
1. En Flow (navegador integrado, proyecto «nov 19 - 12:54», https://flow.google.com/project/a63ef11e-8d97-4e33-951b-7ad35eac75cb)
   generar con Nano Banana 2.1, 16:9, x1, una por una (Flow ya dio «actividad inusual» con prisas), con la MISMA plantilla
   de las otras hojas (leerla en el proyecto: «Game art sprite sheet in the style of classic late-1990s isometric medieval
   real-time strategy games… pure blue (#1f4fff) wool tunic… facing right. Animation frames: … All frames evenly spaced in
   ONE horizontal row… Solid flat pure magenta (#FF00FF) background…»), cambiando solo «Animation frames»:
   - dormir: 6 frames, lying asleep on his side on the ground, head to the right resting on his bent arm, eyes closed,
     chest and shoulder rising and falling slightly (bucle); la «z» la dibuja el motor (sin texto en la hoja).
   - sentado: 6 frames, sitting cross-legged on the ground eating a small loaf of bread (sube, muerde, mastica, baja).
   - estirarse: 6 frames, standing, big lazy stretch with both arms over the head and a yawn, then back to rest.
   - platicar: 6 frames, standing, talking and gesturing with the open right hand, small nods.
   Prompt: editor `.ProseMirror` → `focus()` + `document.execCommand('insertText', false, prompt)` + tecla Return REAL.
   Bajar SIN ventanas: antes de cualquier clic de descarga, gancho en `window.fetch`/XHR que junte
   `flow-content.google/image/<uuid>?Expires…` de las respuestas `batchexecute` y `HTMLAnchorElement.prototype.click`
   anulado; luego `curl` sin cookies a `flow/ald_<anim>.jpg`. (En JS no escribir «&»: usar «\u0026».)
2. `preparar_arte.py`: agregar dormir 6, sentado 6, estirarse 6, platicar 6 (y pico con el reorden) a `ALDEANOS`, y un
   modo que NO reescriba `panel_obra.html` (p. ej. `aldeanos --sin-html`). Para el acostado, el piso = fila más baja del cuerpo.
   Correr, mirar `img/hoja_aldeanos.jpg` y cada bucle (que el primer y el último cuadro empaten).
3. Mandar a la sesión de capas (SendMessage a local_a6e54548-…): nombres, n, w, h, ax, ay de `img/aldeanos.json`, que se
   cargan como las demás (`/v2/obra/img/ald_<anim>_<tinta>.png`, `ALD_META[anim]`), qué cuadros van en bucle y que pico
   ya existe con golpe en el cuadro 4.
4. Commit en español solo de `preparar_arte.py`, `img/ald_*` nuevos, `img/aldeanos.json`, `img/hoja_aldeanos.jpg`, este LEEME; push.

Cierre sesión 4: `flow/ald_dormir|sentado|estirarse|platicar.jpg` (Flow, Nano Banana 2.1) y `ald_pico.jpg` → recortadas con
`preparar_arte.py aldeanos --sin-html` (no toca `panel_obra.html`; el pico reordenado a golpe = cuadro 4; dormir y sentado
escalados por el ÁREA de la túnica, `POR_AREA`). Medidas en `img/aldeanos.json`; enviadas a la sesión de capas para el ocio.
Bajar de Flow sin ventanas: el gancho `__scan2` (quita las barras invertidas y luego cambia `u003d`/`u0026`) saca la URL
firmada de la respuesta `ogiZ0b` al terminar cada imagen; `curl` sin cookies.
