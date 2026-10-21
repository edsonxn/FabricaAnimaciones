# Panel de avance y vista previa

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Panel de avance
`python fab.py panel [--puerto 8765] [--abrir] [--lienzo]` → http://127.0.0.1:8765 (clásico) · http://127.0.0.1:8765/v2 (lienzo, ver abajo). Muestra en vivo las 14 etapas de cada
proyecto de `videos/` (los nuevos aparecen solos; deduce el estado de los archivos y de los procesos en marcha),
disco libre, GPU y logs. **Avisos por voz**: un vigilante detecta etapas terminadas, hitos del render (25/50/75 %),
etapas que piden atención o se detienen, y un locutor los dice con Chatterbox (`nucleo/avisos.py` + `avisos_voz.py`,
voz Faraon, por las bocinas de la PC; el modelo se carga al primer aviso y se descarga tras 5 min; respaldo: voz de
Windows). Se controla desde el panel (activar/silencio, destino, probar) y `panel_config.json`. Lee archivos y procesos; lo único que lanza es la **vista previa**. Código en `nucleo/panel.py` + `nucleo/panel.html`.
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
- Registra el uso como `v2-lienzo` en la bitácora (`/uso.js`). Cambios en `panel.py` (rutas `/v2`, `--lienzo`, Estilos robusto, cola de 128):
  el panel en marcha los toma **cuando el usuario lo reinicie** (nunca lo reinicia Claude).

## Pestaña «Canales» (8-oct-2026)
El panel de estadísticas (`nucleo/estadisticas.py` + plantilla `nucleo/estadisticas.html`) vive dentro del panel como tercera pestaña: un `<iframe>` a `/canales`, que arma la misma plantilla con los datos de `canales/metricas/panel/<alias>.json` y los proyectos en producción. `python fab.py estadisticas` sigue generando la copia suelta (`canales/metricas/panel_canales.html`), sin botones que escriban.
- **¿Qué canal se queda sin video?** (arriba): una fila por canal con sus videos programados sobre una línea de tiempo (14/30/60 días) y la fecha del primer hueco del ciclo sin video = último programado (o último público) + ciclo. Urgente ≤ 3 días, pronto ≤ 7. Filtros por urgencia y por canal (las fichas de arriba), orden, y clic en la fila para el detalle: programados, último publicado, siguientes huecos libres, privados sin fecha y proyectos en producción. Cálculo: `estadisticas.calendario()`; en consola, `python fab.py canales`.
- **Ciclo editable** (− / +): `POST /api/canales/ciclo` guarda `horario.ciclo_dias` en `canales/<alias>.json`. Solo mueve el pronóstico; el freno de publicación sigue siendo `separacion_min_horas` (`youtube.comprobar_separacion`).
- **«↻ Actualizar datos»**: `POST /api/canales/actualizar` lanza `estadisticas.actualizar_seguro` de todos los canales en un hilo (4 a la vez, solo lectura); la página consulta `/api/canales/progreso` y se recarga sola. Un canal que falle sale en rojo junto al botón y conserva sus datos anteriores.
- El marco copia el tema del panel (`localStorage.t`) y su paleta (`html.emb` en la plantilla) y ajusta su alto solo. Tras tocar `panel.py` o `estadisticas.py` hay que reiniciar el panel; la plantilla `.html` se lee en cada carga.

## Motor SECUENCIA en el panel (6-oct-2026)
Los videos con `MOTOR = "secuencia"` (clips e imágenes de Google Flow; `docs/estilo_secuencia_flow.md`) no tienen etapa
«Escenas» ni vista previa del motor; en su lugar muestran **Beats**, **Prompts** y **Flow**, y un bloque con el avance de Flow:
recibidos/total, cuántos clips e imágenes faltan, ritmo por minuto y hora estimada de término (calculada con las horas de
llegada de los archivos de `medios/` en los últimos 15 min; «en pausa» si no llega nada en 4 min). Al abrir la tarjeta sale
un recuadro por beat con su miniatura (`/api/medio_mini`, guardadas en `previews/_minis/`), su segundo y su frase; borde ámbar
= beat de video. Código: `secuencia_info` y `medio_mini` en `panel.py`, `secHTML` en `panel.html`. Canal de un video nuevo:
`videos/<v>/panel.json` con `{"canal": "<alias>"}` (alias dados de alta en `CANALES_PANEL`).
