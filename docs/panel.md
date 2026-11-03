# Panel de avance y vista previa

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Panel de avance
`python fab.py panel [--puerto 8765] [--abrir] [--lienzo]` → http://127.0.0.1:8765 (clásico) · http://127.0.0.1:8765/v2 (lienzo, ver abajo). Muestra en vivo las 14 etapas de cada
proyecto de `videos/` (los nuevos aparecen solos; deduce el estado de los archivos y de los procesos en marcha),
disco libre, GPU y logs. **Avisos por voz**: un vigilante detecta etapas terminadas, hitos del render (25/50/75 %),
etapas que piden atención o se detienen, y un locutor los dice por las bocinas de la PC con **ElevenLabs** (desde el
27-oct-2026, el usuario: «para no gastar CPU ni GPU siempre ElevenLabs»; `nucleo/avisos.py` → `avisar.eleven`, voz
Alberto Rodríguez, caché por texto; respaldo: voz de Windows). Chatterbox (`avisos_voz.py`, Faraon) solo con
`"motor": "chatterbox"` en `panel_config.json`. Se controla desde el panel (activar/silencio, destino, probar) y `panel_config.json`. Lee archivos y procesos; lo único que lanza es la **vista previa**. Código en `nucleo/panel.py` + `nucleo/panel.html`.
**Render parcial (12-oct-2026)**: `python fab.py <v> video --hasta <s>` (`nucleo/render_parcial.py`) dibuja solo el principio; con `segmentos/parcial.json` el bloque «Render en vivo» mide el avance solo sobre ese tramo (requiere reiniciar el panel tras el cambio de `panel.py`). Protocolo y regla de preguntar al usuario: `docs/sesiones.md` § 2b.

**Bitácora de uso y rediseño (12-oct-2026)**: el panel registra cómo lo usas (clics y clics muertos, filtros, buscador, scroll, pestañas, atención real, inventario de controles; nunca letras tecleadas) con `nucleo/panel_uso.js` (servido en `/uso.js`, incluye el iframe «Canales») → `POST /api/uso` → `nucleo/datos/uso_panel/AAAA-MM-DD.jsonl` (privado, fuera de git; lógica en `nucleo/uso_panel.py`). `python nucleo/uso_panel.py estado | resumen [--dias 14] [--ui v2] [--json] | borrar --antes AAAA-MM-DD`. Cada evento lleva la versión de la interfaz (`<meta name="ui-version">` de `panel.html`). **Cada cierto tiempo di «analiza mi uso del panel»**: el skill `analizar-uso-panel` lee la bitácora, diagnostica y escribe una propuesta en `nucleo/propuestas_panel/panel_vN.html` (se prueba en `http://127.0.0.1:8765/propuesta/panel_vN.html`, con datos reales y su uso registrado como `vN`); si la adoptas, sustituye `panel.html` y se anota en `docs/panel_ui_versiones.md`. Requiere reiniciar el panel una vez (cambió `panel.py`).
**Render en vivo (4-oct-2026)**: mientras corre el render de un video, su tarjeta muestra un bloque «Render en vivo»: barra real (segmentos
terminados + los que se dibujan, rayados), video listo/total, transcurrido, ritmo («1 s de video cada 3,7 s»), segundos por segmento y procesos a la vez,
y **una fila por escena** con un cuadrito por segmento de 3 s (verde = listo, tenue = ya existía, parpadea = dibujándose, gris = pendiente), su estado y
la hora estimada en que quedará lista. Cuando una escena está completa aparece **«▶ Ver fluida»**: abre la vista previa en esa escena y pulsa solo
«Renderizar esta escena» (segundos: monta el mp4 con los segmentos ya dibujados, sin dibujar nada; el worker lo permite durante un render completo
solo si la escena no necesita dibujar nada). **Prearmado (6-oct-2026)**: montar ese mp4 tardaba ~15 s (recodifica 1080p con grano mientras el render
ocupa la CPU y el disco E:), así que el panel lo hace solo en segundo plano (`panel.prearmar`: ffmpeg en prioridad baja, 2 hilos, una escena a la vez)
en cuanto el render termina cada escena; «Ver fluida» la reproduce al instante. `cache_escenas.listar` acepta segmentos del render aún sin anotar si son
adoptables (misma regla que `sin_dibujar`) y el mp4 es más nuevo que ellos; el empaquetado vive en `cache_escenas.empaquetar_escena` (lo usa también
el motor). Mientras renderiza, la etapa «Render» sale en curso con «k/n segmentos · restantes · termina HH:MM» aunque exista un MASTER previo, y
«Ahora:» es la etapa que corre (no la primera incompleta). Si la escena está dibujada pero la vista previa no podría reutilizarla (se empezó a dibujar antes de
«última edición del código + 15 min», ver `cache_escenas.limite_adopcion`, o con otro código) sale «⚠ lista · no reutilizable» con la hora límite.
Desde el 6-oct-2026 el render completo anota **cada segmento en cuanto lo termina** (`cache_escenas.anotar_segmento`, enganchado en
`render._repartir` dentro de un bloque `# cache_escenas`, que no cuenta en la firma): si el código no cambió desde que arrancó, la escena
sale «Ver fluida» al momento, sin esperar al final ni a la regla de los 15 min.
Todo se deduce de `segmentos/` (no depende de cómo se lanzó el render): `st_ctime` = inicio de cada segmento y `st_mtime` = fin (el `os.replace`
del `.tmp.mp4` conserva la creación); el arranque sale del proceso `-m render` hijo de `fab.py <v> video|todo` (`inicio_render`). Estimación
(`calcular_render` en `panel.py`, función pura): procesos = máximo de segmentos solapados, costo = promedio de los últimos terminados, y
faltan = (segmentos pendientes + lo que resta de los que se escriben) × costo / procesos; probado reproduciendo el render de `historia_espana`
(error de la hora de término 10-40 s con ~7 min por delante; por escena, ≤ 15 s). Lo que cambia a cada segundo (`render.vivo`) no repinta la tarjeta:
`tickRender()` lo actualiza en el sitio. **El panel se reinicia para tomar cambios de `panel.py`** (el HTML se relee solo): cierra su ventana de consola y
`python fab.py panel --abrir`.

**Voz y Selección en vivo (11-oct-2026)**: mientras corre `voz` o `seleccionar` (sueltos o dentro de `todo`), la tarjeta muestra un recuadro
como el del render: barra, frase/toma en curso con su texto, tomas hechas/total, semillas, ritmo, audio generado, última toma, transcurrido y
hora de término, y una fila por escena con un cuadrito por frase (o, si se regeneran ≤ 14 frases con `--solo`, una fila por frase con un
cuadrito por toma). En la selección: fase 1/3 (Whisper escucha cada toma; cuadrito verde = CER ≤ 1,2 %, rojo = con errores), 2/3 (elige) y
3/3 (limpia y alinea palabras, `voz/final/`), con las frases a regenerar en rojo. Si `fab.py` espera la GPU de voz, dice quién la tiene
(`voz_gpu.lock`). Todo sale de disco + la línea de comandos del hijo `-m tts_gen|tts_select`: `info_voz`, `info_seleccion`, `proceso_hijo`
en `panel.py`; `vozVivoHTML`/`tickVoz` en `panel.html`.
**Fondo por canal**: cada tarjeta lleva como fondo una ilustración del canal (`nucleo/panel_fondos/<alias>.svg`, servida en `/fondo/`) y una etiqueta con su nombre. El canal sale de `panel.json` (`"canal": "<alias>"`) > canal donde se publicó > «Canal X» en el docstring del guion > tabla `CANAL_POR_VIDEO` de `panel.py` > «experimento». Canal nuevo: añadirlo a `CANALES_PANEL`, crear su SVG y una regla `.card[data-canal="<alias>"]` en `panel.html`.
**Pestaña «Estilos»**: galería con un video terminado por estilo (4 cuadros sacados con ffmpeg a `videos/<v>/previews/galeria_N.jpg` + reproductor con Range). El catálogo es `nucleo/datos/galeria.json` (campos `id`, `nombre`, `estilo`, `canal`, `video`, `archivos` de `salida/`, `desc`, `uso`, `extra`; más `sin_ejemplo` = estilos sin video terminado): **se relee en cada petición, editarlo NO exige reiniciar el panel** y las entradas cuyo video no existe se omiten solas. Al crear o mejorar un estilo, o cambiar el video de referencia, actualízalo en la misma sesión (una entrada por estilo; si hay versión nueva del estilo, el ejemplo pasa al video nuevo y el anterior se rotula «versión anterior»). Orden = el de la lista (primero los estándares vigentes por canal). Los cuadros salen solos la primera vez que se abre la pestaña.
**Vista previa en el panel** (botón «▶ Vista previa» en cada proyecto con `timeline.json`): el panel lanza bajo demanda un
`nucleo/preview_worker.py` por video (proceso aparte, solo CPU, puerto libre + token; se cierra tras 10 min sin uso y se reinicia solo si cambia
código o `timeline.json`). Dibuja con el MISMO `render.Renderizador.cuadro` del render final (lo que ves es lo que sale). Modo cuadros: barra con
forma de onda + escenas + transiciones, scrub, ←/→ cuadro, espacio reproduce con audio (`audio/final.wav`, unos 1-2 fps según la escena: el motor
cuesta 0,6-1,2 s/cuadro) y «Clip fluido»: renderiza 5-40 s en paralelo (12 procesos) con audio y lo reproduce (≈ 7 s de espera por cada segundo
de video; no lo uses a la vez que un render largo). Workers y clips viven en `videos/<v>/previews/` (ignorado por git). Al lanzar producciones
largas, ofrece abrirlo.
**«Escena fluida» (4-oct-2026)**: botón «Renderizar esta escena» (la escena bajo la línea de tiempo). El worker dibuja la escena con el
MISMO codificador del render final (`render._trozo`: 1080p, x264 crf 18, piezas de 30 cuadros repartidas entre los procesos) y deja
(1) sus **segmentos** en `videos/<v>/segmentos/seg_NNNN.mp4` (tramos de 90 cuadros que cubren la escena; los de las orillas se
completan hasta la rejilla de 3 s y los comparte la escena vecina) anotados en `segmentos/preview_origen.json`, y (2) un mp4 liviano con
audio, `previews/escena_<id>.mp4` (ancho = «Calidad»), registrado en `previews/escenas.json`. La barra de tiempo marca esas zonas (verde =
vigente, ámbar = el código cambió) y al reproducir o mover la línea dentro de ellas se usa el mp4 (fluido, con audio, también al
reabrir la ventana); fuera de ellas siguen los cuadros del motor. **El render completo las reutiliza**: `render.video` llama a
`cache_escenas.depurar()`, que conserva los segmentos cuya firma coincide con el código actual y borra los hechos con código distinto.
- **Tiempo restante (4-oct-2026)**: mientras dibuja, «Escena fluida» y «Clip fluido» muestran `faltan ≈ X (termina ≈ HH:MM)` =
  transcurrido × (1 − avance) / avance, suavizado (`etaTexto` en `panel.html`). El motor informa `transcurrido` (`t_ini` del job) para
  que no se reinicie al reabrir la ventana; con un motor anterior a este cambio usa el reloj de la ventana («Recargar motor»).
- **Firma** = contenido de los módulos que importa `render.py` (cierre de imports por `ast`: nucleo + carpeta del video, no scripts
  sueltos `_*.py`), `timeline.json`, `guion.py` y `FAB_ESTILO`. No incluye imágenes/datos sueltos: si cambias uno, «Volver a renderizar».
  `cache_escenas.py` no cuenta, y el bloque entre `# cache_escenas: inicio` y `# cache_escenas: fin` de `render.py` tampoco (ese enganche
  no cambia píxeles). **Ojo:** cualquier otra edición de un módulo del render (aunque sea un comentario) pone las escenas en ámbar y el
  render completo borra sus segmentos al arrancar; si fue neutra para los píxeles, pulsa «conservar» ANTES de renderizar el video.
- El mp4 de la escena es solo para mirar: ancho máx. 1440, x264 crf 27 con tope de bitrate (2/5/9 Mb/s según el ancho) para no llenar el
  disco; los segmentos 1080p (los que usa el render final) se guardan aparte. Si falta el mp4 de una escena vigente, «Renderizar» solo lo
  rehace desde los segmentos (segundos, sin dibujar).
- Cambiar código de UNA escena deja todas las guardadas en ámbar (la firma es global). Si no tocaste las demás, botón «No toqué esas
  escenas: conservar» (`/escenas/conservar`) las da por vigentes; la editada se renderiza de nuevo.
- **Render completo → escenas en verde (4-oct-2026)**: `render.video` anota al terminar los segmentos que dibujó con la firma del código
  al arrancar (`cache_escenas.anotar_render`; si el código cambió durante el render no anota nada) y el motor de la vista previa, al abrir
  la ventana (`/escenas`), arma sin dibujar el mp4 de las escenas con todos sus segmentos «vigentes» pero sin mp4 (`autocompletar`,
  segundos, solo con ≥ 0,4 GB libres y sin render ni clip en curso). Hace falta «Recargar motor» si el motor arrancó con código anterior.
  Antes el verde solo lo daba «Renderizar esta escena»; el render completo dejaba `segmentos/` y el MASTER pero no las marcas.
  **Ámbar ≠ error**: la firma es global, así que cualquier edición posterior de un módulo del render (de OTRA sesión, p. ej. `estilos.py`,
  o un parche a `coreo_*.py`) pone todas en ámbar aunque el MASTER esté bien.
- **Antes de `video --rehacer …` tras editar código**: `render.video` → `depurar()` BORRA todos los segmentos anotados con una firma
  distinta a la actual (no solo los tramos a rehacer). Pulsa «No toqué esas escenas: conservar» ANTES (o `cache_escenas.conservar_escenas`)
  si los cambios solo afectan a los tramos que vas a rehacer; si no, se vuelve a dibujar todo lo guardado.
- Un render completo anterior a este cambio (sin anotar) no se toca. Sus segmentos se **adoptan** al pulsar «Renderizar» si su archivo se
  empezó a escribir >15 min después de la última edición del código (`cache_escenas.adoptar`): la escena queda lista en segundos.
- No arranca si hay un render completo escribiendo `segmentos/` o queda < 1,5 GB de disco (excepción: una escena que ese render ya dejó completa y reutilizable solo se monta, no dibuja nada: `cache_escenas.sin_dibujar`); usa `procesos_seguros` (memoria virtual).
- Endpoints del worker: `/escenas`, `/escena` (POST id,w,procs,forzar), `/escena/estado`, `/escena.mp4`, `/escenas/conservar` (POST). Solo lo detienes con su propio proceso (línea de comandos con `panel.py`), no con todos los python.

**Filtro por canal y por estilo (11-oct-2026)**: dos desplegables junto a los filtros de etapa («Todos los canales» / «Todos los estilos») muestran solo los videos de un canal (`canal` de cada proyecto, misma regla que el fondo) o de un `ESTILO_VISUAL` (vacío = «(sin estilo)»); se combinan entre sí y con En curso/Terminados/Ocultos, acotan también los contadores de arriba, y cada opción lleva cuántos videos visibles tiene. Se recuerdan en el navegador (`localStorage` `fc`/`fe`). Solo `panel.html`: no hace falta reiniciar el panel.

**Ocultos (7-oct-2026)**: todo video que ya está en YouTube (registrado en `publicados` de `canales/<alias>.json`: público, programado o privado) sale OCULTO por defecto; solo aparece con el filtro «Ocultos». El botón «👁 mostrar» lo vuelve a enseñar (guarda `"oculto": false` en `videos/<v>/panel.json`); «🙈 ocultar» guarda `"oculto": true` en cualquier proyecto. No borra nada.

## Panel v2 «Lienzo» (21-oct-2026, idea del usuario a partir de MiniMax Design)
**http://127.0.0.1:8765/v2** (o `python fab.py panel --abrir --lienzo`). El mismo servidor y las mismas funciones que el clásico, pero
en un lienzo infinito: **cada video es un tablero** y cada canal un carril de color (los carriles se empacan lado a lado como un
muro; lo que está en curso va primero). Código: `nucleo/panel_v2.py` (backend) + `nucleo/panel_v2.html` (página).
- **Arriba, el sistema en vivo**: estado de la lectura, CPU (con historial), RAM, GPU (uso, VRAM, temperatura), GB libres de cada
  unidad (C:, D:, E:), E/S de disco y red, y procesos (python/ffmpeg). Clic en CPU/RAM/GPU/Procesos → núcleos de la CPU, **trabajos de
  la fábrica agrupados** (un render = `fab.py <v> video` + sus 12 procesos + ffmpeg, con su video, etapa, CPU, RAM y cuánto lleva; clic
  en la fila = sus procesos), quién usa la GPU y lo que más memoria gasta del resto del equipo. Por debajo de ~1900 px de ancho, las
  métricas van en una segunda fila. Botones: ▶ En curso (producciones en marcha), 🔔 avisos por voz (los mismos: activar, destino,
  probar, repetir), 🎨 Estilos, 📅 Canales (la pestaña de siempre en un cajón), ▤ Clásico, tema (misma clave `localStorage.t`).
- **Tablero cerrado**: arriba, al inicio de la cabecera, el botón destacado **⤢ Abrir / ⤡ Contraer** (en un tablero abierto muy ancho
  la esquina derecha queda fuera de vista); portada (miniatura de YouTube > fotograma del MASTER > hoja > última prueba > primer medio),
  barra de las 17 etapas, anillo de avance, recuadro «en vivo» si algo corre, y abajo: ▶ Video (se reproduce ahí mismo), 🎞 Montaje,
  🔍 Vista previa, 👁 Ver estilo, 📂 carpeta (abre el Explorador), 🙈/👁 ocultar.
- **Proceso en marcha** (el usuario, 21-oct): borde azul que gira alrededor de la tarjeta (`@property --giro`), insignia arriba
  «● RENDER · 41 %» (de cerca) o pastilla de avance encima (de lejos, ver zoom semántico) y marco azul en el minimapa; el grosor
  del borde crece al alejar (`--inv` = 1/zoom).
- **Tablero abierto** (⤢ Abrir o doble clic): TODO lo producido en columnas que siguen el pipeline, unidas con flechas:
  ① Guion y voz (escenas y frases con ▶ por frase = la toma elegida de `voz/final/`; las etiquetas de actuación `[sighs]` resaltadas;
  ESTADO.md legible) → ② Imágenes y clips (cada subcarpeta: `medios/`, `imagenes/`, `pegatinas/`, `hojas/`, `piezas/*`…; al pasar el
  ratón por un clip se reproduce en silencio) → ③ Música y efectos (`audio/`, `sfx/`: un solo reproductor abajo que sigue sonando
  mientras te mueves; los `.wav` de > 25 MB se convierten una vez a `.m4a` en `previews/_v2/`) → ④ Pruebas y vistas (`previews/`, lo
  último primero) → ⑤ Entrega (MASTER y otros mp4 reproducibles, miniatura, `.srt`, metadatos de `youtube.json`). Se refresca solo cada
  8 s mientras está a la vista (sirve para ver llegar los medios de Flow). Fuera: `segmentos/`, `voz/cands`, código y cachés.
- **Contraer secciones** (el usuario, 21-oct): ▾/▸ en la cabecera de cada sección (Guion, ESTADO.md, `medios`, `audio`, `previews`,
  el video…) y de cada columna. **La regla vale para esa sección en TODOS los tableros**, también en los que se abran después
  (clave por tipo o carpeta: `guion`, `g:medios`, `col:guion`…; `localStorage` `v2pleg`). Se aplica en el sitio, sin redibujar
  (un video que suena no se corta).
- **Zoom semántico** (el usuario, 21-oct: «de lejos se ve raro: menos texto, más visual»): **cerca** (≥ 70 %) todo; **medio** (40-70 %)
  sin letra menuda ni botones salvo ⤢; **lejos** (< 40 %) solo lo visual: portadas, miniaturas, etapas en color, el borde azul de lo que
  corre y los carriles; las secciones de texto se vuelven un bloque con icono (📝 guion · 📋 ESTADO · 🎵 audio · 📺 YouTube). En medio y
  lejos **el título sale al pasar el ratón** (`#tip`; probé pastillas de título fijas y al usuario le gustó más así) y **solo lo que
  está en marcha** lleva ENCIMA de su tarjeta una pastilla de avance a tamaño fijo de pantalla (capa `#etiquetas`): título, barra
  gruesa y «RENDER · 49 % · termina 15:07» (la hora sale del `detalle` de la etapa), legible hasta el 16 %. Los tableros no cambian
  de tamaño entre niveles (no se reacomoda nada al hacer zoom).
- **Nitidez**: `will-change: transform` solo mientras te mueves; con él fijo Chrome estiraba una imagen del lienzo al hacer zoom
  (texto borroso). Al detenerse (~160 ms) se quita, la posición se redondea a píxel y las miniaturas a la vista piden una versión
  mayor si se muestran más grandes que su archivo (de 160 en 160 px, hasta 960).
- **Arrastrar nunca selecciona texto** (`user-select:none` en el lienzo + `preventDefault` en `pointerdown`); para copiar, el inspector
  y el visor. Arrastrar mueve desde cualquier parte salvo botones, reproductores y la barra de las listas.
- **Imágenes por turnos**: máx. 6 a la vez, lo último que entró a la vista primero, con un reintento. El servidor del panel solo
  encolaba 5 conexiones (valor de Python) y con la CPU al 100 % Windows rechazaba el resto: `panel.py` ahora usa 128.
- **Clic** en cualquier archivo → inspector a la derecha (vista grande, medidas reales, tamaño, fecha, ⤢ Ver grande, ↗ Abrir aparte,
  📂 Mostrar en carpeta, ⧉ Copiar ruta). **Doble clic** → visor a pantalla completa con ← → por toda la carpeta. Clic en la cabecera
  de un tablero → inspector del proyecto (etapas con detalle, «Siguiente: comando + copiar», último log, botones).
- **Montaje, Vista previa y Muestra son los del clásico**, incrustados: el lienzo abre `/?embed=montaje|previa|muestra&v=<video>` (modo
  «embebido» de `panel.html`: solo ese diálogo, fondo transparente; al cerrarlo avisa con `postMessage` y el lienzo lo quita). Cualquier
  mejora a esos diálogos en `panel.html` sale en los dos paneles.
- **Moverse**: arrastrar, rueda = zoom (botón 🖱 para que la rueda mueva), Ctrl+rueda/pellizco, minimapa (clic para ir), F = todo,
  1 = 100 %, + −, flechas, / = buscar, Esc. La lista de la izquierda (filtros En curso/Sin terminar/Terminados/Ocultos, canal, estilo,
  buscador que atenúa el resto) vuela al tablero. Se recuerdan vista, tableros abiertos y filtros (`localStorage` `v2*`). `/v2#v=<video>`
  abre ese tablero.
- **Backend** (`panel_v2.py`; panel.py lo **recarga solo si cambia**, así que editarlo NO exige reiniciar el panel; `panel.html`/
  `panel_v2.html` se releen en cada carga): `/api/v2/estado` (el estado de `/api/estado` **al instante**: devuelve el último calculado y
  calcula el siguiente en segundo plano; el 21-oct, con un render a CPU 100 %, `/api/estado` tardó 250 s), `/api/v2/sistema` (lo mide
  un hilo cada 2 s mientras alguien mira; los procesos salen de UNA llamada a Windows, `NtQuerySystemInformation`, porque psutil tardaba
  segundos por proceso protegido y `tasklist` 5 minutos), `/api/v2/portadas`, `/api/v2/recursos?video=`, `/api/v2/guion?video=`,
  `/v2/archivo/<v>/<ruta>` (con Range; solo extensiones de medios/texto y dentro del video, también a través de junctions),
  `/v2/mini/<v>/<ruta>?w=` (miniaturas en `previews/_v2/`, máx. 3 a la vez para no estorbar a un render), `/v2/oir/<v>/<ruta>`,
  `POST /api/v2/revelar`. Solo lee, salvo esas cachés y el Explorador.
- **Videos cuya CARPETA ENTERA es un junction** (los 28 movidos a `E:\FabricaAnimaciones\videos_desde_C` el 24-oct): hasta el
  26-oct-2026 `_car_video` exigía que la ruta real colgara de `videos/`, así que el ▶ Video, el Montaje y los recursos del lienzo
  daban 404 (el reproductor se quedaba en 0:00, `wow_pistas_futuro`). Ahora se valida el NOMBRE (una carpeta, sin `/ \ :`) y se
  sigue el enlace: `panel_v2._car` (vale sin reiniciar, el módulo se recarga solo) y `panel._car_video` (vale al reiniciar el panel).
- Registra el uso como `v2-lienzo` en la bitácora (`/uso.js`). Cambios en `panel.py` (rutas `/v2`, `--lienzo`, Estilos robusto, cola de 128):
  el panel en marcha los toma **cuando el usuario lo reinicie** (nunca lo reinicia Claude).

## Panel remoto: el lienzo en el celular fuera de casa (21-oct-2026, pedido del usuario)
`python fab.py panel --remoto` → levanta (si no corren) una **puerta con clave** (`nucleo/panel_remoto.py`, 127.0.0.1:8770) y un
**túnel ngrok**, e imprime el enlace `https://<algo>.ngrok-free.app/entrar?k=<clave>`: se abre una vez en el celular (cookie de
30 días) y luego basta `<url>/v2`. `--tunel cloudflared` (sin cuenta ni límites; URL nueva cada vez) · `--nueva-clave` · `estado` · `parar`.
- **El panel no se toca ni se reinicia**: la puerta reenvía a 127.0.0.1:8765, o a 8766 si el de 8765 es anterior al lienzo (el
  21-oct el de 8765 seguía sin `/v2`; el de 8766, `--sin-voz`, sí lo tiene). Se revisa cada minuto.
- Puerta y túnel se lanzan desacoplados (siguen vivos al cerrar la terminal); clave y PIDs en `panel_remoto.json` (raíz, fuera de
  git), registros `panel_remoto.log` / `panel_remoto_tunel.log`. Sin cookie todo da 401 (página «Entrar»); 8 claves malas = 10 min fuera.
- La puerta **comprime** JSON/HTML/JS y lleva la Vista previa del clásico a su trabajador por `/_pv/<puerto>/…` (solo puertos que
  el panel anunció en `/api/preview`; `panel.html` usa esa ruta cuando no está en 127.0.0.1). `/` lleva al lienzo; el clásico,
  `/?clasico`.
- **Peso**: `/api/v2/estado` ya no manda `secuencia.beats` (era el 72 % de ~800 KB) y con `?si=<huella>` sin cambios devuelve
  solo avisos/voz/sistema (~300 B). Por el túnel el lienzo pregunta cada 8 s (no 3/2) y nada con la pestaña de fondo.
- **Lienzo en el celular** (`panel_v2.html`, clases `html.remoto` / `html.tactil`): un dedo mueve, pellizco acerca, **doble toque**
  abre un tablero (el toque sencillo espera 340 ms por si es doble); el detalle sube como **hoja desde abajo**; la lista ☰ con velo
  (tocar un video la cierra); botones de 36-40 px; sin «📂 carpeta» por el túnel (abriría el Explorador en casa); horizontal = una
  sola fila arriba. Probado con Chrome emulando iPhone por la URL pública: lienzo, lista, hoja, tablero, Montaje, Canales, Procesos.
- **Dirección fija en el dominio** (21-oct, el usuario ofreció su dominio): `--dominio clicknbusiness.com.mx/fabrica` (queda en la
  config). El hosting (HostGator compartido, solo FTP) no puede correr el panel, así que `fabrica/` es solo una página que reenvía
  al túnel de hoy; se resube sola cuando cambia la URL de ngrok (con el módulo FTP de `C:\CNB`, cuyas credenciales nunca se leen
  aquí; solo toca esa carpeta, marcada con `fab_puerta.txt`; `noindex` + `no-store`). La clave no va al servidor: el primer
  enlace `…/fabrica/#k=<clave>` la deja en el `localStorage` de ESE celular y de ahí en adelante `clicknbusiness.com.mx/fabrica`
  entra solo (`#olvidar` la borra). Un subdominio con el panel «de verdad» exigiría DNS en Cloudflare o ngrok de pago.
- **ngrok gratis**: aviso «You are about to visit…» la primera vez (tocar *Visit Site*), URL nueva si ngrok se reinicia (volver a
  correr el comando) y cupo mensual de datos y peticiones; si se agota, `--tunel cloudflared`.

## App del teléfono: panel móvil, Fábrica 3D y APK (28-oct-2026, pedido del usuario)
Todo en `nucleo/app_movil/`, servido por `panel_v2.py` (se recarga solo: **no hay que reiniciar el panel**):
- **Panel móvil** `panel.html` → `/v2/movil` (por la puerta: `/m` o `/movil`; dominio: **`clicknbusiness.com.mx/panel/`**).
  Pestañas Ahora / En curso / Listos / Todos (+ deslizar), chips por canal, anillos CPU/RAM/GPU/C:, tarjeta por video con
  portada, barra, pista de etapas y caja «en vivo» (render, voz/selección, Flow o el proceso de `fab.py` que trabaja en ese
  video, con reloj de término); hoja de detalle (etapas, procesos, registro, ESTADO.md); **🎞 Montaje** a pantalla completa
  (`/?embed=montaje&v=`) y ▶ MASTER. Avisa con toast + SFX (WebAudio sintetizado, 🔇 por defecto) + vibración + confeti
  cuando una etapa termina. Lee `/api/v2/estado?si=` cada 6 s y `/api/v2/sistema` cada 10 s; solo lee.
- **Fábrica 3D** `juego.html` → `/v2/juego` (puerta `/juego`; dominio `clicknbusiness.com.mx/juego/`), three.js r160 de
  `tactica3d/vendor` (alias `/v2/app/three.module.min.js`). Nave industrial sin techo: hasta 18 **celdas** (lo que trabaja,
  lo que está a medias y lo último subido) con pantalla = portada, torre de etapas (un bloque por etapa; azul late = en curso,
  «pop» al terminar), brazo robot + banda + baliza + chispas cuando trabaja, trofeo ▶ si ya está en YouTube. Al entrar, el
  **estudio** del video: holograma de etapas y 7 estaciones (Guion + ESTADO.md, Cabina de voz = cada frase con su toma,
  Rocola = audio vía `/v2/oir`, Galería, Sala de clips, Cine = Montaje, Muelle = MASTER/miniaturas) y cuadros con sus imágenes.
  Recepción: Reactor (CPU/GPU de la PC), Trivia («¿de qué video es esta imagen?»), tablero de órdenes y Taquilla.
  Progresión en el `localStorage` del teléfono (`fab3d`): XP y rangos (Becario→Leyenda), créditos 🪙, bobinas 🎞 que sueltan
  las celdas que trabajan, 3 órdenes al día (+ bono), racha, 15 medallas, tienda de pintura/sombreros/estelas por nivel,
  «guion roto» (completar la palabra) y +60 XP por **presenciar** una etapa que termina. `window.FAB` = ganchos de depuración.
- **La Aldea** `aldea.html` → `/v2/aldea` (puerta `/juego` y `/aldea`; dominio `clicknbusiness.com.mx/juego/`; la Fábrica 3D
  pasó a `/fabrica3d`). Pedido del usuario: «tipo Age of Empires», «escenario bonito como Foundation», «NPC que van por los
  recursos», «destinar NPC a cada proyecto y pausar uno». Valle con relieve, lago, bosques instanciados (pinos, robles,
  abedules), 5 000 hojas de pasto, flores, caminos curvos, cielo con degradado, sol con sombras que siguen a la cámara y
  «siempre de día» u «hora real». Cada video = **obra** en un lote (anillos de 8 y 12) con un plano de ~17 secciones según el
  canal (casa · castillo para Warcraft/Gaming · torre para Runa/LogIA/Neón/sin canal); las secciones se reparten entre las
  etapas: 🟦 plano = la PC aún no llega, 🟨 lista para construir, sube con andamio mientras la levantan, sólida = hecha.
  **La PC manda el tope y los aldeanos el ritmo**: leñadores, canteros y mineros llevan 🪵🪨🪙 al almacén; los constructores
  de cada obra (−/+, ⏸ Pausar, 🎯 Enfocar = pausa las demás) acarrean el material y gastan 1 unidad por golpe. Todo vive en
  el teléfono (`localStorage` «aldea»; al volver, «mientras no estabas» simula hasta 4 h).
  **Ciudadela (29-oct, pedido del usuario):** en el valle solo quedan las obras SIN terminar; las terminadas (todas sus secciones
  + video subido o al 100 %; los subidos que nunca pasaron por el juego cuentan como terminados) se mudan a otro valle
  (botón 🏯, `x = CIU_X`): anillos de 62 lotes con los más recientes, trofeo, calles y alameda; todos sus edificios se funden
  en ~45 mallas por material (`fusiona()`) y el valle no se dibuja estando allí. Al terminar la última sección: fuegos y a los
  8 s se muda. **Cámara RTS:** mira a un punto suavizado (`CAM.sx/sz/sy`) y se coloca siempre a la misma distancia y ángulo
  de él → al arrastrar se desliza sin girar; el giro con dos dedos va hacia donde giran los dedos.
  **Etiquetas vivas y elementos del video (29-oct, pedido del usuario: «aburridos sin animación»; «que cada edificio sea
  diferente y tenga sus elementos del video»):** sobre cada obra una tarjeta HTML (`#etqs`, `hazEtiqueta/pintaEtiqueta`) que
  sigue al edificio en pantalla, con miniatura, barras 🎬/🏗 con rayas en movimiento, % que cuenta, chip animado (🔨 trabajando,
  🧱 lista, ⚠ falta material, ⏳ espera, ⚙️ la PC en vivo) y 👷 por constructor; de lejos se encoge a un anillo con el %. Los
  videos sin subir que el juego ve por primera vez arrancan en los cimientos. Cada obra pide `/api/v2/recursos` y toma hasta 10
  fotos (clips/imágenes) y 8 pegatinas: esperan en el **acopio** junto al solar y se **pegan en las paredes** (anclas halladas
  por rayos contra los muros, `calculaAnclas`) al construirse la sección; **cartel de obra** con la portada; los constructores
  a veces cargan un cuadro; matiz de color propio por video; al acercarse se ve más de cerca (la isométrica no se inclina). En la
  Ciudadela cada edificio lleva su portada en un cartel.
  **Vista isométrica low poly (29-oct, el usuario con 3 referencias «cute low poly»):** la vista de estratega es una cámara
  ORTOGRÁFICA fija (yaw 45°, 35,26°, `CAM_O`, sin giro; zoom = tamaño del encuadre `CAM.d` 22-130, `distCam()` para escalar
  etiquetas/sonidos) y el capataz usa la de perspectiva (`CAM_P`). Estilo: `flatShading` en todos los materiales, terreno con un
  color por triángulo (`facetas()`), verdes vivos, sin briznas de pasto, árboles en cono de 6 caras y copas icosaedro,
  rocas marrones, caminos como cintas (`cintas()`), sin tone mapping, sol alto (13 h). **Solo isométrica (29-oct, el usuario: «más plano como
  las referencias, todo se tiene que poder apreciar desde la vista satelital»):** sin tercera persona (`#modo/#joy/#accion`
  ocultos; el capataz se manda tocando), relieve ×0,28, sin flores, vallas ni nubes; fotos y pegatinas solo en paredes que miran
  a la cámara (`VISTA`), cartel de obra y acopio colocados de su lado (`ponEnVista`); zoom hasta 150.
  **Casillas (29-oct, referencias del usuario de islas isométricas de bloques):** el terreno es una ISLA de casillas de 4×4
  (`construyeCasillas`: tres InstancedMesh = tapa del color de la casilla, borde casi del mismo tono para una rejilla sutil y
  cuerpo de tierra hasta y=-8) sobre fondo pastel `#7fd6e0`; `altura()` devuelve la altura de la casilla (escalones de 1,2;
  el relieve suave queda en `alturaSuave`), agua = casillas azules más bajas, calles rectas por casillas (`trazaCalles`),
  lotes y obras alineados a la rejilla, pinos de dos pisos; la Ciudadela igual (`infoCiu`). HUD «cute»: fichas de recursos
  de crema con burbuja de color y botones gorditos con canto de color que se hunden al tocarlos (`.rb.madera`). Capataz en tercera persona (🧍,
  joystick + arrastrar para girar) o mandado desde la vista RTS tocando suelo/árbol/roca; monedas sobre las obras con la PC
  trabajando; Ayuntamiento con monumentos (renta de oro, +aldeanos), mejoras y edades por nivel. **No toca la PC**: pausar
  una obra no pausa el video real. `window.ALDEA` = ganchos de depuración.
- **Aviso de actualización** (`actualiza.js`, en las tres páginas): lee `version.json` (público). Si cambió `web.version`
  desde la última visita en ese teléfono → «🆕 ¡Actualización!» con `web.notas` (**al cambiar algo para el usuario, subir
  `web.version` y escribir las notas**). Si la app Android trae un `v=<versionCode>` menor que `apk.codigo` (o ninguno: la
  primera APK) → «📲 Hay una app nueva» con descarga pública `clicknbusiness.com.mx/panel/fabrica.apk`.
- **Rendimiento en el teléfono** (28-oct, el usuario notó lag al deslizar): nada de `backdrop-filter` en elementos fijos,
  ni bordes animados con `mask`/`@property`, ni fondos de pantalla completa animados; latidos solo con `opacity`.
- **APK Android** `android/construir_apk.py` (sin Gradle: aapt2 + javac + d8 + zipalign + apksigner del SDK de la PC; ~10 s):
  WebView `mx.clicknbusiness.fabrica` que abre `clicknbusiness.com.mx/panel/`; agente `FabricaApp/1.0` = **ngrok no muestra
  su aviso**; video a pantalla completa, atrás = historial, pantalla siempre encendida. Sale `nucleo/app_movil/fabrica.apk`
  (fuera de git; se baja desde el panel: **📲 → Descargar APK**, o sin clave en `clicknbusiness.com.mx/panel/fabrica.apk`; `--nota "…"` = novedades del aviso; sube sola al dominio; `versionCode` = minutos desde 1970). La llave `android/fabrica.keystore` (fuera de
  git) se reutiliza: si se pierde, hay que desinstalar la app vieja. Tras tocar `MainActivity.java`, volver a correr el script.
- **Puerta** (`panel_remoto.py`): atajos `/m`, `/movil`, `/juego`; sin clave solo pasan `/v2/app/*.png|webmanifest|js`
  (instalar la app web). El dominio publica `fabrica/`, `panel/` y `juego/` (`DOMINIO_EXTRAS`; la página lleva `&ir=` al
  túnel). `--republicar` las sube aunque la URL del túnel no haya cambiado. Cambios en la puerta = relanzarla (no el panel).

## Pestaña «Canales» (8-oct-2026)
El panel de estadísticas (`nucleo/estadisticas.py` + plantilla `nucleo/estadisticas.html`) vive dentro del panel como tercera pestaña: un `<iframe>` a `/canales`, que arma la misma plantilla con los datos de `canales/metricas/panel/<alias>.json` y los proyectos en producción. `python fab.py estadisticas` sigue generando la copia suelta (`canales/metricas/panel_canales.html`), sin botones que escriban.
- **¿Qué canal se queda sin video?** (arriba): una fila por canal con sus videos programados sobre una línea de tiempo (14/30/60 días) y la fecha del primer hueco del ciclo sin video = último programado (o último público) + ciclo. Urgente ≤ 3 días, pronto ≤ 7. Filtros por urgencia y por canal (las fichas de arriba), orden, y clic en la fila para el detalle: programados, último publicado, siguientes huecos libres, privados sin fecha y proyectos en producción. Cálculo: `estadisticas.calendario()`; en consola, `python fab.py canales`. Además de la lectura de YouTube, cuenta lo
  registrado en `canales/<alias>.json` → `publicados` con `programado`/`publicado` (13-oct-2026: con la cuota agotada tras una
  subida, el video recién programado no salía). Se actualiza al empezar y al terminar cada video (regla global del 13-oct).
- **Ciclo editable** (− / +): `POST /api/canales/ciclo` guarda `horario.ciclo_dias` en `canales/<alias>.json`. Solo mueve el pronóstico; el freno de publicación sigue siendo `separacion_min_horas` (`youtube.comprobar_separacion`).
- **«↻ Actualizar datos»**: `POST /api/canales/actualizar` lanza `estadisticas.actualizar_seguro` de todos los canales en un hilo (4 a la vez, solo lectura); la página consulta `/api/canales/progreso` y se recarga sola. Un canal que falle sale en rojo junto al botón y conserva sus datos anteriores.
- El marco copia el tema del panel (`localStorage.t`) y su paleta (`html.emb` en la plantilla) y ajusta su alto solo. Tras tocar `panel.py` o `estadisticas.py` hay que reiniciar el panel; la plantilla `.html` se lee en cada carga.
- **Canal suspendido (21-oct-2026, Edsonxn):** `"suspendido": {"desde", "nota"}` en `canales/<alias>.json` lo saca de esta pestaña, de `python fab.py canales [--actualizar]` y del «buenos días» (`estadisticas.alias_conocidos()`; con `con_suspendidos=True` sale igual, y el color de los demás no cambia). En la pestaña de proyectos, sus videos nacen ocultos (`panel.canales_suspendidos()`; «👁 mostrar» guarda `"oculto": false`) y el canal desaparece del desplegable salvo con el filtro «Ocultos». Reactivar = borrar la clave y reiniciar el panel.

## Motor SECUENCIA en el panel (6-oct-2026)
Los videos con `MOTOR = "secuencia"` (clips e imágenes de Google Flow; `docs/estilo_secuencia_flow.md`) no tienen etapa
«Escenas» ni vista previa del motor; en su lugar muestran **Beats**, **Prompts** y **Flow**, y un bloque con el avance de Flow:
recibidos/total, cuántos clips e imágenes faltan, ritmo por minuto y hora estimada de término (calculada con las horas de
llegada de los archivos de `medios/` en los últimos 15 min; «en pausa» si no llega nada en 4 min). Al abrir la tarjeta sale
un recuadro por beat con su miniatura (`/api/medio_mini`, guardadas en `previews/_minis/`), su segundo y su frase; borde ámbar
= beat de video. Código: `secuencia_info` y `medio_mini` en `panel.py`, `secHTML` en `panel.html`. Canal de un video nuevo:
`videos/<v>/panel.json` con `{"canal": "<alias>"}` (alias dados de alta en `CANALES_PANEL`).

**Render en vivo del motor SECUENCIA (17-oct-2026).** `secuencia.video` dibuja de una sola pasada en `salida/video_sin_audio.mp4`
(o `salida/tramo_A_B.mp4` con `--tramo`) y no escribe `segmentos/`, así que el avance sale de **`salida/progreso_render.json`**,
que reescribe cada ~2 s (atómico): `pid`, `inicio`, `ahora`, `fps`, `f0`/`f1`/`frame` (cuadros), `tramo`, `beat`/`beat_i`/`nbeats`
y `estado` = `dibujando` → `codificando` (cierra el mp4) → `ambiente` (solo el video completo) → `listo`, o `error` (+ `error`)
si se corta. Las vistas previas con `--salida` no lo tocan. El panel lo toma por vivo si su `pid` sigue entre los python o se
reescribió hace < 15 s (sirve también lanzado sin `fab.py`) y pinta la misma tarjeta «Render en vivo»: barra «m:ss/m:ss de video ·
%», faltan/hora de término (cuadros por segundo de reloj medidos desde el arranque), ritmo, beat en curso, tramo, MB en disco y una fila
por escena del timeline (sin «▶ Ver fluida»: cada cuadrito son 3 s de video). La etapa «Render» pasa a «en curso» con ese detalle
aunque exista un MASTER previo. Código: `progreso_secuencia` e `info_render_secuencia` en `panel.py`, `renderHTML` (rama `sec`) en
`panel.html`. Probado con `agotado_cortisol --tramo 0-10` y `0-40` (ETA estable a ±5 s).
**«Efectos» del motor SECUENCIA** = `audio/fx.wav` (`fab.py <v> fx`, SFX de `PISTAS` de `efectos.py`): listo si existe (con el nº
de `sfx/*.mp3`), «atención» si `efectos.py` es más nuevo que `fx.wav` y que el MASTER, pendiente si `efectos.py` tiene `PISTAS` y
no hay `fx.wav`, y «no aplica» si sus `PISTAS` están vacías (los ejemplos comentados no cuentan). Los Plastitube viejos con
`audio/sfx.wav` siguen como antes. `fab.py <v> fx` corriendo marca «Efectos» en curso. Cambió `panel.py`: el panel lo toma
cuando el usuario lo reinicie (nunca lo reinicia Claude).

## Vista «Montaje» (motor SECUENCIA YT, 13-oct-2026)
Los videos con `ESTILO_VISUAL = "secuencia_yt"` (clips de gameplay con yt-dlp) no muestran «Prompts» y la etapa `flow` se
llama **Clips** («clips de yt-dlp bajados»). Botón **🎞 Montaje** en la tarjeta: monitor + línea de tiempo con un bloque por
beat (ancho = duración, miniatura del clip, rayado = aún no baja). Reproduce cada clip de `medios/` en su beat (misma
velocidad que `secuencia.vel_clip`) con la voz de `voz/final/<key>.wav` encima, y se refresca cada 5 s: los huecos se llenan
solos mientras corre `bajar`. Clic en un bloque = saltar; espacio = play/pausa; ← → = beat; «saltar huecos». Es un borrador
del navegador (sin transiciones ni música). Solo lectura. Código: `montaje`, `servir_montaje`, `_servir_rango` en
`panel.py` (`/api/montaje?video=`, `/montaje/<v>/clip/<scene-id>`, `/montaje/<v>/voz/<key>.wav`, `/montaje/<v>/fx/<archivo>`);
`mj*` en `panel.html`.
**REGLA (el usuario, 20-oct-2026): el Montaje vale para TODO video del motor SECUENCIA (también Flow: imágenes `.jpg` y clips `.mp4`),
no solo SECUENCIA YT.** Mientras se generan las imágenes, cada lote se baja a `medios/` en cuanto sale para que el usuario vea el
montaje actual, y los clips se generan en la misma tanda (no al final). El botón dice «medios» en los videos Flow.
**Clic en las casillas Voz / Selección (19-oct-2026):** despliega las mismas barritas por escena que el «en vivo» aunque la etapa no esté
corriendo (`/api/detalle_voz?video=&etapa=voz|seleccion`, `detalle_voz` en `panel.py`; ✕ cerrar; se refresca cada 4 s). El «en vivo»
solo aparece si la etapa se lanzó con `fab.py <v> <etapa>` (un `python -m tts_gen` suelto no lo ve el panel).
**Música en el Montaje (19-oct-2026):** casilla «música»: `audio/musica.wav` en una pista sincronizada con la línea de tiempo, a
volumen 0,45 bajo la voz; el panel la sirve como `previews/montaje_musica.m4a` (`/montaje/<v>/musica/musica.m4a`, se rehace sola si
cambia la música). `parsear_guion` entiende ya `VOZ = dict(...)` (antes suponía 4 tomas por frase con ElevenLabs).
**Capa de efectos (13-oct-2026):** `python fab.py <v> fx montaje` exporta `previews/montaje_fx.json` y un mp4 de 960 px por
tramo con motion graphics o videos encima (`previews/montaje_fx/`, con el audio de efectos, p. ej. el código del patrocinio).
El monitor pone los apoyos PNG encima del clip en su momento (marcas doradas arriba en la línea de tiempo) y, dentro de un
tramo (marca morada abajo), el mp4 compuesto. Casillas **«efectos»** y **«subtítulos»** (esta se recuerda en el navegador).
Un beat cuyo medio es imagen (captura de la web del patrocinador) se muestra fijo. Si `efectos.py` cambió después de
exportar, la cabecera lo avisa. Pendiente: «cambiar clip» desde el bloque (= `bajar N --q`).
**REGLA (el usuario, 19-oct-2026): en TODO video SECUENCIA YT (Warcraft, Tamriel, Runa Caída, Crónicas del gaming) el Montaje
enseña SIEMPRE los motion graphics, pegatinas, fichas, imágenes y pantallas, como en Warcraft.** Desde ese día `python fab.py <v> fx`
exporta también la capa del Montaje (antes había que acordarse de `fx montaje`, y en Runa Caída y `tes_misiones_daedricas` nunca se
hizo: su Montaje solo enseñaba clips). Solo rehace los tramos que cambiaron; la firma incluye TODOS los kits `nucleo/mg_*.py`
(antes solo mg_wow/mg_tes: cambiar mg_er no rehacía nada). Tras editar `efectos.py`, volver a correr `fx` (o `fx montaje`).
`fx --sin-montaje` se lo salta. Necesita los clips de `medios/` (va después de `bajar`).
**Montaje por partes (el usuario, 26-oct-2026: «no veo los efectos» con la exportación de 50 min a medias):** `fx montaje` reescribe
`montaje_fx.json` tras CADA tramo pintado (el panel enseña lo que ya está; cerrar y abrir el 🎞 Montaje para recargar) y cada tramo
lleva una firma de SU contenido en `previews/montaje_fx/_firmas.json` (los FX que pisa con los parámetros de sus fn y sus clips;
`secuencia_fx._sig`), no la fecha de `efectos.py`/kits: antes, tocar una pegatina rehacía los ~200 tramos de un video largo.
Un cambio en una función auxiliar de un kit (p. ej. `_base` de mg_wow) NO se detecta: `fx montaje --forzar` si hace falta.

## Montaje de los videos dibujados por código (20-oct-2026)
El usuario: «la vista previa muchas veces tarda mucho en cargar y no se ve bien; la del montaje de Warcraft y Tamriel sí me gusta:
aplícalo a videos como el de Jalpa». Todo video que NO es motor secuencia y tiene `timeline.json` muestra **🎞 Montaje (n/m
escenas)** en la tarjeta (la vista previa queda como «🔍 Vista previa cuadro a cuadro»: es la que guarda escenas fluidas para el
render). Cada escena de `timeline.json` es un bloque que se reproduce fluido con, por orden: su escena fluida
(`previews/escena_<id>.mp4`, borde verde) o el borrador de **`python fab.py <v> montaje`** (`nucleo/montaje_codigo.py`:
`previews/montaje/<id>.mp4` 640x360 a 12 fps, mudo, `FAB_SS=1`, + `<id>.jpg` y `info.json` con la firma de `cache_escenas`); si
ambos existen gana el más nuevo. Borde ámbar = el código cambió desde que se dibujó (se sigue viendo lo viejo); rayado = sin dibujar;
punteado gris = escena de `ESCENAS` del guion sin voz todavía (duración estimada a 2,7 palabras/s). Audio: `audio/final.wav` (la
mezcla real) si es posterior a `timeline.json` (`previews/montaje_mezcla.m4a`), si no voz por frase + música. Botón **🖌 Dibujar lo
que falta** = lanza `fab.py <v> montaje` con prioridad baja (log en `previews/montaje/_montaje.log`, avance en `progreso.json`);
no a la vez que la voz o el render. Opciones: `montaje <ids…>`, `--todo`, `--fps`, `--ancho`, `--procs`. Código: `montaje_codigo`,
`_escenas_montaje`, `montaje_resumen`, `montaje_dibujar` en `panel.py` (`/montaje/<v>/esc/<archivo>`, `/montaje/<v>/fl/<archivo>`).

## Vista «En vivo» del agente (`/v2/vivo`, 30-oct-2026)

Lo que el agente hace, animado: `http://127.0.0.1:8765/v2/vivo` (la sesión más reciente con video), `/v2/vivo?video=<v>` (la sesión que produjo ese video más recientemente, aunque el corte a 180 mil abra otra) o `/v2/vivo?sesion=<id>`. Se entra con **🤖 En vivo** en la barra del lienzo o en la tarjeta de cada video. Funciona igual por el panel remoto y en el celular (el atajo `/vivo` entra en vigor al reiniciar la puerta; `/v2/vivo` ya sirve).

- **Datos:** `nucleo/agente_vivo.py` lee solo los bytes nuevos de `~/.claude/projects/C--FabricaAnimaciones/<sesion>.jsonl`: no gasta tokens ni toca al agente. Se ven las acciones, no el razonamiento. Los ayudantes se leen de `<sesion>/subagents/agent-*.jsonl`, igual de incremental (los 12 más recientes de las últimas 6 h, solo sus últimos 8 MB). Editar `agente_vivo.py` o `panel_vivo.html` no exige reiniciar el panel.
- **Qué enseña:** barra de etapas y render real (del estado del panel), taller con robot que camina a la estación (Guion, Voz, Sonido, Imágenes, Clips, Animación, Render, Revisión, Subida) y un monitor: imagen con lupa, código tecleándose con +/−, terminal, navegador con captura, burbujas, plan. El título de cada comando es su `description`: escribirla en español.
- **Repetición:** al abrir reproduce solo las últimas 3 acciones y se queda en la última esperando lo nuevo. La casilla **🔁 Repetir** (apagada por defecto, el usuario, 30-oct; se recuerda en ese navegador) la vuelve bucle: sin novedades en 9 s las repite. Al llegar una acción nueva corta y salta a lo de ahora (salvo 20 s después de elegir un momento en la línea de tiempo). Pestaña oculta = no pide datos.
- **Robot (30-oct):** cada acción tiene su pose y utilería (`POSES` en `panel_vivo.html`; `accionDe()` elige por tipo y estación): pinta con boina en caballete (imágenes), graba con cascos y micrófono (voz), hace de DJ (sonido), da la claqueta (clips), programa en laptop, escribe el guion con pluma, corre en una rueda de hámster (render), revisa con lupa y gorro de detective, lanza el video en un cohete a la nube (subida), lee, busca con linterna, surfea (navegador), se tapa los ojos (privado), festeja (cierre), se pone triste si un comando falla y se duerme con gorro si no hay nada. Al estar al día sigue en el proceso que corra (`etapa_actual`). Cada acción dura al menos 1,5 s para que no solo camine. Tocarlo hace una gracia al azar.
- **Solo la estación real (30-oct):** el robot pisa una estación únicamente si la acción trabaja ahí (`estacionDe()`); sin estación o en reposo vuelve al **Descanso** (rincón a la izquierda) y ninguna se ilumina. `agente_vivo.py` juzga lo que el comando EJECUTA, no las palabras que nombra (ignora heredocs y `python -c`), más la `description` si empieza por bajar/buscar audio o clips; Animación es solo código de animación (`_ANIMACION`), los scripts auxiliares no tienen estación. Los 1,5 s de cada acción cuentan ya en su sitio (tope de 3 s si camina lento). Subida solo con subidas reales: `yt subir/aplicar/publicar`, `pagina.py programar`, y Studio solo en `/videos/upload` o con una acción de edición (`_estacion_navegador`); las consultas de YouTube no tienen estación.
- **Investigación en vivo (30-oct):** `WebSearch` y `WebFetch` son eventos `busqueda` (texto, resultados) y `pagina` (sitio, título, extracto), todo por `tapar()`. La API añade `ayudantes` (id, tipo, descripción, activo, última acción, `accion`, contadores; activo = archivo escrito hace menos de `ACTIVA_S`), `equipo` (todos los ayudantes con acciones, para el selector) y `web`. Si lo hace el principal, pose `libros`; si lo hace un ayudante, lo enseña su mini. Las cifras dicen «N búsquedas · N páginas · N ayudantes trabajando». Hay líneas `api-request-blob` sin hora: se ignoran.
- **Mini robots (30-oct):** cada mini existe solo si hay trabajo real detrás; lo que hacen entre ellos es teatro y el rótulo dice lo real («Esperando la investigación»). Tipos (`TM` en `panel_vivo.html`): investigador, explorador, obrero, inspector (por las herramientas y la descripción del ayudante, `_Ayudante.tipo`), rodador, cantor, pintor (por `etapa_actual`) y cargador (comandos `run_in_background`, también render/voz/Flow). Máximo 4, 2 en celular, y «+N». Escenas (`pasaEscena`): preguntar, discutir y pelea (máx. una por minuto, nunca con trabajo real pendiente), avión de papel por página, entrega y choque de manos al terminar, rollo revisado con lupa, prisa ante el Rodador, susto al fallar, porra al cerrar tramo, pisotón y siesta. Un ayudante ya terminado solo reaparece en la repetición, mientras suenan sus eventos. Sonido en `M`: bajo y cada uno con su tono; si suena el principal, baja más. Probar: `Taller.sync(lista,etapa)`, `Taller.escena(tipo,mini)` y `Taller.pinta(t,dt)`. Límite: un comando de fondo sin aviso de fin se da por muerto a las 3 h o si la sesión lleva 30 min sin escribir.
- **Sonido:** casilla **🔊 Sonido**, apagada por defecto y recordada en cada navegador. Todo se sintetiza con Web Audio (`Son`, recetas en `R`): sin archivos ni APIs. `Son.medir("pintar")` da pico y duración sin que suene. Si la casilla ya venía marcada, el navegador exige un toque antes de sonar.
- **Seguridad:** todo texto pasa por `tapar()` (claves, tokens, correos, URL firmadas) y los archivos de `SENSIBLE` (`canales/tokens`, `client_secret`, `.env`, `panel_remoto.json`…) salen como «🔒 privado», sin contenido. Las capturas del navegador NO se tapan: pueden enseñar lo que había en pantalla (Studio, correo); por el remoto siguen detrás de la clave.
- **Caché:** imágenes reducidas a 960 px en `%TEMP%ab_vivo\<sesion>` (máx. 200 por sesión; se borran a los 3 días).
- **Prueba:** `python nucleo/agente_vivo.py [sesion]`.
- **De quién es una sesión (30-oct):** solo cuenta lo que produce (`_videos_producidos`, `Sesion.video`): Write/Edit dentro de `videos/<v>/`, también de sus ayudantes, y `fab.py <v> <etapa>` de producción, `fab.py nuevo` y `yt subir`; si aún no produjo nada, el título que nombra al video. Leer, buscar, mencionarlo, `estado`, `continuar`, `verificar` y `comprobar` no cuentan. Sin video propio (panel, núcleo) la sesión sale como chip con su título. Con varias del mismo video se sigue a la que lo produjo más recientemente, sin mezclar; el subtítulo de la cabecera dice de qué sesión viene lo que se ve. Las sesiones aparte que lanza un video no son minis: tienen su propio transcrito y su propio chip.
- **Trabajo de los minis en vivo (30-oct):** cada acción de un ayudante va a su propia línea (`_Ayudante.eventos`, `MAX_EV_AYUD`), aparte de la del principal: uno que hace cientos no echa a nadie. Al abrir se mandan las últimas `PRIMERA` del principal y `PRIMERA_AYUD` de cada uno, intercaladas por `seq`; la página también poda por origen (`podar()`). Salen en el monitor con las mismas pantallas (búsqueda, página, código, comando, imagen, navegador), su color, un distintivo con su nombre y una flecha sobre su mini. En vivo manda el principal; si espera, `proximoVivo()` enseña solo a los ayudantes activos. Selector **Todos / Principal / cada mini** sobre el historial: filtra historial, línea, cifras y monitor; el principal sigue moviéndose en el taller aunque el monitor no lo enseñe.
- **Kit de variantes por acción (1-nov-2026, el usuario: «se repite mucho lo mismo… un kit muy amplio de animaciones para cada acción, que den risa»):** `nucleo/panel_vivo_poses.js` (servido en `/v2/vivo/poses.js`, se carga antes de `extras.js`) añade 84 poses a 24 acciones de trabajo con `pon("<acción>", {nombre(T,s){…}})` → `POSES["<acción>_<nombre>"]`. Ejemplos: correr comando = palanca, rueda de hámster, patada a la máquina expendedora, detonador, microondas, manivela con cinta perforada; leer = pergamino que se va rodando, periódico para espiar, «no veo», tableta, libro al revés; programar = modo hacker, pulpo con 4 brazos más, un solo dedo, concertista, torre de bloques que se cae; fallo = cáscara de plátano, nube de lluvia propia, berrinche, cortocircuito; también buscar, investigar, navegar, revisar imagen, pintar, grabar, mezclar, clips, render, esperar render, subir, explicar, te escucha, paso listo, tramo listo, privado, ayudante, pensar y dormir. `variaDe()` en `panel_vivo.html` las baraja sin repetir hasta agotar la bolsa de cada acción (la pose original entra en la bolsa) y, si la acción dura, cambia cada 9 s (`ROTA_MS`, con su propio reloj `A.vT`); los robots de otras sesiones también barajan (`R.v`). **El letrero y el sonido siguen siendo los de la acción real**: solo cambia el teatro. La tabla se llama `KIT_V` porque `VARIAS` ya era la lista de gracias al tocar al robot. Probar una: en la consola, `Taller.prueba("boton_hamster")` (fija esa pose; `Taller.prueba()` la suelta); `Taller.estado().pose` dice cuál se ve. Reglas al añadir: utilería entre x −60 y +84, nada por encima de y −72 salvo lo que vuela (ahí va el letrero), texto con `em()` (sale derecho aunque el robot mire a la izquierda; `letra()` dentro de la pose se refleja), colores claros para lo que va sobre el muro oscuro, y nada de `gorro` salvo que el chiste lo pida (tapa el uniforme del canal).
- **Avance de tareas largas (3-nov-2026, el usuario: «que se vea bien cuánto lleva y cuánto le falta»):** `nucleo/panel_vivo_avance.js` (servido en `/v2/vivo/avance.js`, después de `extras.js`) pinta una tarjeta arriba a la derecha del lienzo (en el edificio, junto a la columna de zoom) cuando la etapa en curso del video trae avance real (`r.proyecto.etapas`: render, voz, selección…): % que lleva, % que falta, barra y el tiempo restante del detalle. Cada tarea toma al azar UNA de 15 animaciones (torre, pared, tren, tanque, pizza, puente, cohete, carrera, planta, rompecabezas, cerca, montaña, dominó, camión, reloj de arena; nunca la misma dos veces seguidas, la misma al recargar): lo hecho construido, lo que falta como hueco punteado. Al acabar, «¡Listo!» con destellos; si se corta, «Se detuvo». El % se suaviza porque el panel lo recalcula cada ~20 s. Probar: `Avance.prueba(i|"nombre", p)` en la consola; sin `p` recorre 0→100 % en 14 s.
- **Actividades siempre que esté libre (30-oct, el usuario: «nunca se esté quieto mucho tiempo»):** basta con que el principal no tenga acción real (`principalAlDia`): no exige ayudante. En 3-4 s va al Descanso (`LIBRE_MS` + `quieto` de 1-2 s) y rota 27 actividades cada 10-12 s sin repetir hasta agotar la bolsa (`ACTIVIDADES`, `sigueActividad`): tortita, café, tele, amigos, planta, pescar, tejer, yoga, guitarra, patineta, burbujas, malabares, barrer, aceitarse, antena, gato, papalote, castillo, ping-pong, bailar, hamaca, pesas, picnic, ajedrez, selfie, dormir (corta, 5-6 s) y preguntar (con pelea; como mucho una vez por minuto y solo con un mini activo en escena). Con un proceso corriendo, cada 45 s va 6 s a su pose real. Cada una es una pose en `POSES` con su sonido del mismo nombre en `R`, que suena solo al empezar, bajo y corto (`Son.actividad`), con la casilla de Sonido. El letrero dice lo real: la espera del mini o del proceso, «Al día» si la sesión no escribe y no hay nadie, nunca un «Esperando…» de algo que no existe. Solo se queda dormido de seguido con la sesión terminada hace más de 20 min (`TERMINADA_S`), sin ayudantes ni procesos. El trabajo real del principal corta la actividad en ese cuadro, y un ayudante que termina corta para entregar. Lo que no escribió el usuario (encargo de la sesión que la lanzó, mensaje de otra sesión, resumen tras compactar) es tipo `encargo`, no «Tú» (`_AJENOS`). Los amigos son juguetes de cuerda (`juguete()`), utilería, no minis. En lo angosto el robot se separa del borde (`xAct`), un velo aparta las estaciones y los minis dejan sitio (`finZona`).
- **Variantes de los minis (30-oct):** `VM` en `panel_vivo.html`, 4-5 por tipo: rotan cada 7-10 s y `a` dice con qué acciones reales encaja; si la acción cambia y ya no encaja, cambia enseguida. Investigador: libros, laptop, pergamino, corcho, telescopio. Explorador: linterna, brújula, mapa, prismáticos, pala. Obrero: martillo, soldar, sierra, llave, ladrillos. Inspector: lupa, tabla, regla, sello, escáner. Rodador: rueda, bici, cinta, manivela. Cantor: micro, partitura, filtro, diapasón. Pintor: lienzo, rodillo, paleta, aerosol. Cargador: carro, hombro, banda, apilar. Probar una: `m.fija=Taller.VM[tipo][i]`.
- **La PC por piezas (30-oct):** franja de gabinete abierto arriba del lienzo (`PCH`, `gabinete()`; `K` y `sue` se miden en lo que queda debajo), con `/api/v2/sistema` cada 3 s (`pedirPC`, nunca con la pestaña oculta; una muestra con `edad` ≥ 20 s no cuenta, y sin datos 15 s todo sale apagado). CPU con ventilador y un LED por núcleo, GPU con ventiladores, temperatura y barritas de VRAM, RAM como líquido, C: y E: con plato y anillo de ocupación, y Red con paquetes (100 % de ánimo = 12,5 MB/s, referencia fija porque la API no da el enlace). **Discos (30-oct, el usuario):** el número es el espacio ocupado, pero ánimo, calor y luz salen de su lectura y escritura (`io_discos`: `tasas_discos` en `agente_vivo.py`, tiempo ocupado de `IOCTL_DISK_PERFORMANCE`, porque aquí `psutil` da `read_time` en segundos enteros; unidad → PhysicalDrive con `IOCTL_VOLUME_GET_VOLUME_DISK_EXTENTS`, y si no hay certeza la unidad sale apagada con su número). Lleno solo engorda: 18 % más ancho al 100 %. Escala igual en todas, interpolada (`animo`): 0-20 dormida, 20-60 contenta, 60-85 sudor, 85-95 roja con vapor y temblor, 95-100 alarma con ojos en espiral, humo y llamas. Tocar una pieza da su detalle; abajo sigue la gracia del robot. Con una pieza ≥ 95 % el principal va con abanico o extintor cada 2 min como actividad más (`urge`).
- **Torre, la PC hecha personaje (30-oct):** torre con patas, cara en la pantalla, cable de cola y ventiladores que giran con el uso. Vive en una columna a la derecha del taller (`AN()`, ancho > 900 px) o en un carril abajo (`TH`, en lo angosto). `tarea_pc` (`agente_vivo.py`) clasifica en el servidor el trabajo de mayor CPU o GPU en `tarea` {tipo, nombre, video, cpu, gpu}: `_NO_TAREA` deja fuera panel y vigilancia, y por debajo de `TAREA_MIN_CPU` (2,5 %) no es tarea. `/api/v2/sistema` ya no da `cmd` y `rol` pasa por `tapar()` (`proceso_publico`). 35 animaciones en `TAREAS`, rotan cada 9-12 s: render (amasar, carretilla, yunque, horno), revisar (contraluz, comparar, lupa), voz (partitura, gárgaras, espejo), mezcla (consola, espagueti, perillas), transcribir (máquina, dictado, tira), descargas (pesca nube, cinta, cesta), ia (pesas, carrera, cerebro), subida (empaqueta, estiba, cohete), comprimir (uvas, exprimir, prensa), libre (café, salvapantallas, siesta, estira) y genérica (manivela, engranes, palanca). Lo desconocido es `generica`. Cambiar de oficio exige dos muestras iguales; intensidad, sudor y ánimo siguen el uso real; su letrero dice «nombre · CPU n %». Si trabaja y el principal está libre, cada 50 s va a mirarla, echarle porras o aire. Probar: `Taller.datosPC({...muestra,tarea})`, `Taller.torre.fija`.
- **Reacciones (30-oct):** teatro disparado por datos reales (`datosPC`, `RX`, `lanzaRx`); el letrero dice solo la cifra, las reacciones no crean minis y el principal entra solo si está libre. Mínimo 45 s por tipo y 5 min si la causa sigue igual. Disparadores: `susto` GPU/CPU ≥ 95; `calor` GPU sube ≥ 8 °C en 30 s (la API no da temperatura de CPU); `ram` ≥ 90; `disco` C: ≥ 90; `apagon` comando del principal con error en vivo; `red` menos de 0,01 MB/s durante 60 s (dice «Sin tráfico», la API no distingue caída); `rendfin` la etapa deja `video`/`final`; `normal` CPU, GPU o RAM ≥ 85 vuelve a < 60. Sin minis las hace el principal solo; si tampoco está libre, se descartan a los 20 s. Probar: `Taller.datosPC(muestra)`, `Taller.limpiaRx()`.
- **Texto limpio (30-oct):** `sin_markdown()` quita enlaces `[texto](#local_…)`, `**`, `*`, backticks, vallas y títulos de lo que dice el agente, los cierres, los extractos de página y los mensajes. El letrero y la etiqueta de los minis guardan `margen()` (22 px o 1,2 % del ancho): la captura del usuario perdía 17 px por lado a 1920 y la página no tiene desborde.

### El mundo del taller (`nucleo/panel_vivo_extras.js`, 30-oct-2026)

Las 12 ideas que eligió el usuario, en un módulo aparte: entran por `Taller.Cap` (capas `fondo`, `medio`, `encima`; `atras`, `cuerpo`, `cabeza` del robot; `clic`) y `/v2/vivo/extras.js`. Editarlo no exige reiniciar el panel. Datos en `/api/v2/vivo/mundo?video=&canal=` (`agente_vivo.mundo`, solo archivos locales, caché de 30 s) y en `/api/v2/agente` (`contexto`, `pregunta`). Probar: `Extras.prueba("bug"|"jefe"|"relevo"|"usuario"|"pregunta"|"carta"|"loteria"|"logro"|"estreno"|"resumen"|"lluvia"|"tormenta"|"canal:<alias>")`, `?canal=<alias>`, `?fiesta=muertos|navidad`, `?dorado=1`.

- **Taller por canal (`TEMAS`):** paleta, pared y lo que lleva el robot, para los 13 canales; LogIA y Cronopapel añaden filtro CSS al lienzo. Un tema nuevo es una fila.
- **Fiestas:** Día de Muertos del 28-oct al 3-nov (papel picado, cempasúchil, catrina y ofrenda con los `retirados` reales de todos los canales) y Navidad del 12-dic al 6-ene.
- **Ventana:** hora real; las nubes y la lluvia salen de los fallos en las últimas 15 acciones del principal (5 o más: relámpago).
- **Bugs y Jefe Render:** un fallo en vivo suelta un bicho que crece si se repite y muere con el siguiente comando bueno. El jefe sale en las etapas `video` y `final`; su vida es el progreso real de la etapa.
- **Relevo:** batería con los tokens de trabajo contra el corte (el mismo cálculo de `hook_contexto.py`; base de 100 mil si la sesión pesa más que `COLA_BYTES`). La escena sale con `start_session` que dice «continúa», con `hand_off_to_session` o cuando la página salta a otra sesión.
- **El Jefe y «Te espero»:** cada mensaje del usuario baja en una pantalla. «Te espero» sale con `wrap_up` con `ask`, `AskUserQuestion` o `ExitPlanMode`, y pone 🔔 en la pestaña. Los permisos pendientes no quedan en el transcrito: no se detectan.
- **Estreno:** MASTER de hace menos de 30 min y aún no visto (solo pantalla ≥ 900 px) o botón 🎬: telón y sus primeros 15 s. Con sonido si la casilla está marcada.
- **Material real:** la banda lleva imágenes de `medios`, `pegatinas` y `miniatura_flow`. La radio pone un trozo de `voz/final` al terminar un comando de voz (con la casilla de Sonido) o al tocarla.
- **Pared:** trofeos con miniatura local y vistas de las últimas métricas, noticiero con estrenos y cifras, buzón con `canales/comentarios/<alias>.json` (cada 75-105 s si está libre, o al tocarlo). Solo hay comentarios en los cuatro canales de videojuegos.
- **Lotería:** 9 de 18 cartas, fijas por sesión y marcadas con eventos reales.
- **Experiencia:** `nucleo/datos/uso_panel/vivo_progreso.json`, por sesión y con `max`. No es retroactiva: cuenta las sesiones que el panel lee desde el 30-oct. Trajes: bufanda Nv. 3, capa 6, corona 10, aura 15; robot dorado en 1 de cada 64 sesiones.
- **Resumen:** botón 🎞, ~1 min de momentos de la sesión en un lienzo propio, exportable a `.webm` sin audio. No usa capturas del navegador, porque pueden enseñar Studio o el correo.

**Edificio (31-oct-2026; pedido del usuario: «no se ve todo amontonado»):** el taller es un edificio de 6 pisos (`PISOS`/`LUGAR` en `panel_vivo.html`): sótano con gabinete y Torre, planta baja de descanso, Guion y voz, Arte, Montaje y azotea con Subida. Cada piso es la franja de antes apilada: las x llevan el piso (`piso*10 + fracción`; `pisoDe`, `fr`, `enP`), `avanza()` lleva a robots y minis por escalera (un piso) o elevador (dos o más, si está libre). Cámara con rueda, arrastre, doble clic y dos dedos; botones de piso, 🎯 seguir y 🏢 todo, dibujados en el lienzo. `Cap.encima` se dibuja sobre el vidrio (`dim()` fuera de un piso da medidas de pantalla). Con `EN_VIDEO` (robotaller.py, canal Edsonxn) o `?clasico` sigue la franja única. **Comprobado el 31-oct:** viajes con cambio de destino (el elevador se desvía), minis por la puerta, escenas entre pisos, cámara, clics, reacciones en la sala, 13 temas, 390x844, 360x640, 844x390, 1920x1080, `?clasico` y `robotaller.py prueba` (franja única). Trampas: `m.v` ya era la variante de animación de los minis, por eso el viaje se llama `via`; en una pestaña de fondo no corre `requestAnimationFrame` y `ahora` vale 0, así que nada que cuente tiempo puede arrancar con ese 0. Para probar con el panel oculto: `resize_window` y una captura lo despiertan. **Tres columnas (31-oct, pedido del usuario):** en escritorio (`body.edif`, más de 900 × 500 px) el lienzo va al centro con todo el alto, `#monitor` a la izquierda (`--izq`), `#lado` a la derecha (`--der`) con su propio scroll y la línea de tiempo abajo; `#cuerpo` usa `display:contents`, así el HTML y el teléfono no cambian. `#ses` ocupa una sola franja; `#etapas` y `#etaInfo` van sobre `#lado`. Un `ResizeObserver` vuelve a medir el lienzo, `zSigue` deja al menos 800 de ancho a la vista y un clic en la imagen del monitor la enseña grande (`#imgGrande`), porque la columna es angosta. Con 🏢 todo el edificio cabe entero a 1920x1080. **Modo director (31-oct, pedido del usuario: «como una película en tiempo real»):** botón 🎬 del lienzo; `Dir` en `panel_vivo.html`. `director()` vigila hechos reales cada cuadro y `hecho()` pide un plano con prioridad (9 error, 8 emergencia de la PC, 7 bicho y pelea, 6 entrega, Jefe, relevo y reacción normal, 5 elevador, subida y pregunta, 4 anuncio, 3 llegar a una estación); cada plano dura al menos 3,5 s salvo emergencias, con enfriamiento por tipo. Sin hechos, `recorrido()` alterna Token, minis, Torre y plano general. `camaraDir()` mueve con curva de entrada y salida, se abre en viajes largos e inclina o sacude en emergencias; `cinta()` pone barras, viñeta y rótulo. Tocar, arrastrar o usar la rueda lo aparta 12 s (`TREGUA`); 🎯 y 🏢 lo apagan. Se recuerda por visor en `localStorage` (`vivo_director`) y `prefers-reduced-motion` quita inclinación y sacudida. Los extras le pasan bichos, Jefe, relevo y anuncios por `Cap.drama`. Con `EN_VIDEO` y `?clasico` no corre. **Pantalla completa, TV y narrador (31-oct, pedido del usuario):** botón ⛶ del lienzo (`ponCine`): `body.cine` pone `#taller` fijo sobre todo y pide la Fullscreen API; sin ella (iPhone) se queda a toda la ventana con el CSS. Esc o ⛶ salen. Enciende el director y al salir deja el modo que había. **TV** en la azotea (`TV`, `tvGrande`, `tvPinta`), solo en pantalla completa: como el lienzo tapa la página sin ocultarla, `#mcuerpo` sigue maquetado y la TV lee de ahí título, imagen, líneas de código o texto, en un canvas aparte cada 450 ms; no pide nada nuevo al servidor ni abre nada en el túnel. El director corta a la TV con imágenes, mensajes del usuario y cierres. **Narrador** (casilla 🎙, apagada por defecto, `vivo_narrador`; también botón 🎙 en pantalla completa): `VOCES` son plantillas por tipo de plano, `narra()` lo llama `arranca()`, habla con `speechSynthesis` y prefiere voz es-MX, es-419 o es-US; cero tokens y cero créditos. Una frase a la vez, lo urgente (prioridad 7 o más) corta lo demás, 6 s de pausa, `Son.baja` baja los sonidos y `cinta()` dibuja la frase como subtítulo. Solo usa piso, estación, tipo de mini y cifras tipo «GPU al 99 %»: nunca rutas, títulos ni texto del monitor. Sin voz en español, lo dice el aviso de la casilla. **Toda la fábrica (31-oct, pedido del usuario):** pestaña 🏢 al inicio de `#ses` (`Flo`, `vivo_fabrica`). Todas las sesiones, también la elegida, son robots con estado propio y la elegida solo es el foco (`Flo.foco`): cambiar de sesión mueve la cámara y cambia TV, monitor, Plan e Historial, sin tocar a ningún robot (usuario, 31-oct: «el edificio debe continuar igual»). Token no se dibuja y copia al robot enfocado, así cámara, director y HUD lo siguen sin más código; no recibe minis ni escenas, y mientras dura el modo no cambian el tema de canal, trofeos ni buzón, y no hay relevo, Jefe, bichos ni lotería. Quien estuvo en foco se queda 20 min. Cada sesión de los últimos 20 min es un robot con estado propio (`fabrica()`, `pasaFlota()`, `dibujaFlota()`), con color y letrero, hasta 12 y el resto como «+N». Cada robot lee solo su fila de `/api/v2/agente/sesiones` (`accion` y `minis`, de `_resumen()` en `agente_vivo.py`: lo que ya está en memoria, cacheado 4 s y solo tipo de acción, sin texto), así no se mezclan eventos. Sin escribir 150 s va al descanso, a los 20 min sale por la puerta; una sesión nueva entra por la calle. Varios en una estación se acomodan al lado; si el elevador está ocupado, usan la escalera. Un toque enseña qué hace y otro lo enfoca. **Uniformes (31-oct, pedido del usuario):** `UNI` en `panel_vivo_extras.js`, uno por canal más `fabrica` para sesiones sin canal: `c` color del cuerpo, `t` torso, `k` cabeza y, opcionales, `manga`, `mano`, `pierna` y `zapato`, todo dibujado por código. Cada robot lleva su clave en `P.uni` y `figura()` no depende del canal global; el canal de cada sesión lo añade `panel_v2.py` a `/api/v2/agente/sesiones` y sale de `canal_de` en `panel.py` (panel.json > canal publicado > línea `- canal:` del `ESTADO.md` > docstring del guion). `n64_secretos` salía como Warcraft, con casco de cuernos, porque heredó ese docstring de `_plantilla_yt`; por eso la plantilla ya no nombra canal. Los minis conservan su gorro de oficio y visten el torso. Gaming es un fontanero retro (31-oct, pedido del usuario): gorra roja con «G», bigote, camisa roja, overol azul con botones amarillos, guantes blancos y zapatos cafés, sin logos ni arte de terceros. Ligoleyen (31-oct, pedido del usuario) lleva saco azul marino, camisa blanca, corbata dorada y zapatos negros, sin sombrero, como comentarista de deportes; Edsonxn es el del traje negro, corbata roja y sombrero. Crónicas de ligoleyen no tiene `canales/<alias>.json`, así que en el panel sus videos siguen como «experimento»: solo En vivo la reconoce, en `_canal_vivo` de `panel_v2.py`, por la línea `- canal:` del `ESTADO.md`. Sirve en el modo de una sesión (`Cap.uniSesion`) y en la fábrica, con leyenda abajo y el nombre del canal al tocar al robot. La corona de la fiesta va encima y los trajes de nivel siguen siendo de Token. Con `EN_VIDEO` y `?clasico` no se usa, y ahí siguen los trajes de `TEMAS`. El director salta a errores, cierres y llegadas de cualquier robot, y su recorrido los alterna con Token. Sondeo cada 3 s, por el túnel cada 15 s, nada con la pestaña oculta. `Yo` indica quién hace la pose, para que lo que suelta no salga de Token.

**Cambiar de sesión (31-oct-2026; pedido del usuario):** elegir una sesión, nueva o ya vista, en cualquiera de los dos modos, salta de golpe a la antepenúltima acción (`irTramo()`, `TRAMO=3`) y reproduce solo las últimas hasta quedar al día, sin recorrer la historia; el monitor conserva lo anterior hasta que llegan los datos y `S.gen` descarta las respuestas pedidas antes del cambio. La línea de tiempo sigue yendo atrás a mano y «Repetir» actúa igual que antes.

**De quién es cada video (31-oct-2026):** una pestaña de video enseña solo la sesión que lo produce (`Sesion.video` en `nucleo/agente_vivo.py`): cuentan los `fab.py <v> <etapa>` y las ediciones en `videos/<v>/`, pero no `panel.json` ni `ESTADO.md` (`_PAPELEO`), y una sesión que toca más el panel que el video (`_SISTEMA`) sale con su propio nombre. Los kits de `nucleo/` (`mg_*`, `peg_estilos`) no cuentan como sistema: se editan produciendo. `agente_vivo.py` se recarga solo al cambiar.

**Quién está en «Toda la fábrica» (31-oct-2026; pedido del usuario):** solo entran la sesión elegida, las que tuvieron actividad hace menos de 5 min (`GRACIA_S`), las `ocupada` (piensa, espera un comando, comando de fondo o ayudante activo; cada aviso caduca a los 15 min, `ESPERA_S`) y las que tienen un proceso de su video en la PC; a los 150 s sin actividad van al café y a los 5 min salen a la calle. Cada robot conserva su sitio y los letreros se escalonan. Las pestañas de `#ses` siguen mostrando las sesiones recientes.

**En el teléfono (30-oct-2026):** dirección fija **`clicknbusiness.com.mx/vivo/`** (carpeta de `DOMINIO_EXTRAS`, mismo reenvío al túnel que `/panel/`), botón 🤖 en la cabecera del panel móvil y otro en la ficha de cada video.
`nucleo/panel_vivo_movil.js` (+ el CSS `max-width:900px, max-height:500px` de `panel_vivo.html`): una sola pantalla sin desplazar: taller arriba y pestañas Ahora / Historial / Plan; pausa y línea de tiempo al pie, Sonido, Repetir y velocidad en «⋯»; acostado, taller a la izquierda.
Por el túnel (`REMOTO`) pregunta cada 5/8/30 s en vez de 2,2/3/8: unas 1 300 peticiones por hora abierta, ~1 KB cada una sin novedades, y nada con la pestaña oculta. La vuelta `←` lleva a `/v2/movil`.
