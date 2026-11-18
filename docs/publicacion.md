# Publicación y canales (protocolo de video nuevo, horario, miniaturas IA, subida a YouTube)

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Cuando el usuario pide un video nuevo (PROTOCOLO — hazlo siempre, en este orden)
1. **Canal.** `python fab.py yt canales` y pregunta para qué canal es (hoy solo hay uno conectado:
   **Sapiens con Wifi**, alias `sapiens_con_wifi`, `canales/sapiens_con_wifi.json`). Canal nuevo:
   `python fab.py yt conectar` (el usuario inicia sesión en el navegador) + crear `canales/<alias>.json`.
2. **Métricas primero.** `python fab.py yt metricas <alias> 90` y analiza ANTES de proponer nada:
   % visto medio y curva de retención de cada video (¿dónde cae? → intro/gancho/duración), fuentes de tráfico
   (búsqueda vs sugeridos vs navegación), términos de búsqueda, países/edades, qué títulos/miniaturas rinden.
   Compara con el último `canales/metricas/*.json`. Da al usuario 2-4 recomendaciones concretas para el
   proceso y el canal (tema, duración, gancho, estilo, miniatura, frecuencia). Canal con pocos datos
   (<1.000 vistas en 28 días): dilo y apóyate en investigación del nicho (vidIQ/Nexlev si hay créditos).
   **Y siempre `python fab.py ideas <alias>`** (8-oct-2026, `nucleo/ideas.py`): lo tuyo contra la mediana del canal
   + los videos del nicho que rompieron la media DE SU CANAL en los últimos 60 días (`--actualizar` si el informe
   tiene más de ~1 semana; ~350 de cuota). El tema sale de ahí: formato que se repite en varios canales chicos
   + lo que a ti te retuvo. Ajusta `ideas.busquedas`/`competidores`/`filtro` de `canales/<alias>.json` si sale ruido.
   **Después, el porqué:** `docs/que_funciona.md` → actualizar `canales/formula/<alias>.md` (fórmula, evitar,
   hipótesis, registro a 7 días) ANTES de proponer temas.
   Al subir el video, anota `"formato": "<nombre corto>"` en su entrada de `publicados`: el informe agrupa por formato
   y así se ve qué apuesta ganó.
3. **Preguntas** (AskUserQuestion, con tu recomendación primero): tema (3 ideas sacadas del informe de `ideas`,
   cada una con el video de referencia y su × mediana), estilo visual, duración, formato (largo o Short vertical), voz (Dan por defecto) y cuándo
   publicar (por defecto el siguiente hueco del horario del canal, abajo). Nunca versiones para WhatsApp.
3b. **Una sesión, directo al MASTER** (el usuario, 5-nov-2026; sustituye el plan de sesiones del 12-oct): si no dice otra
   cosa, se produce entero en esta sesión. La duración la decide Claude según el canal si él no la da; solo se pregunta lo que
   no esté claro (p. ej. el canal). Tramos solo si él los pide (`docs/sesiones.md`).
4. **Producir** (flujo de abajo) → miniatura (2-3 variantes) → `youtube.json` (título con la **REGLA DE TÍTULOS** de abajo:
   40-55 caracteres, palabra clave al inicio, SIN paréntesis; descripción con capítulos reales del timeline, fuentes, enlace a otro video
   del canal y 3 hashtags; 15-25 etiquetas ≤ 450 caracteres) → `yt subir <v> <canal> private --publicar <ISO del hueco>`.
   **Render terminado = subir y programar SIN preguntar (regla abajo, 20-oct-2026).** Hacer público YA sigue siendo del usuario.
5. **Cierre (regla del 12-oct-2026):** registrar en `canales/<alias>.json` (`publicados`, con `formato`), BITACORA y `ESTADO.md`, y DOCUMENTAR hallazgos y
   mejoras en el manual/estilo del video (CLAUDE.md «CIERRE DE VIDEO»). Verificar los DOI de las fuentes con Crossref antes de subir.

## REGLA IMPORTANTE: TÍTULOS (el usuario, 18-nov-2026, TODOS los canales y videos)
«Eso de poner entre paréntesis creo que no es una buena práctica… no solamente quedó muy largo, sino que se ve medio raro»
(`fo_refugios_25` salió con «Los 25 REFUGIOS más MALVADOS de Fallout (el n.º 1 es el peor de la saga)», 72 caracteres; se cambió
a «Los 25 refugios más MALVADOS de Fallout», 39). Investigado el mismo día. Los estudios externos son de blogs de herramientas, con
evidencia floja; lo sólido es lo que dice YouTube y lo que miden nuestros propios canales:
- **Nuestros datos (yt-dlp, 18-nov-2026):** los 6 videos más vistos de Warcraft miden **41-51 caracteres** y ninguno lleva
  paréntesis (Kungen 272 mil, Angwe 88 mil, «¿Realmente es TAN Mala la Película de Warcraft?» 76 mil). En Runa Caída, la fórmula
  «Las 5 peores atrocidades de X que IGNORASTE» rinde de 39 a 50 caracteres; la única con paréntesis y 62 caracteres («…TARNISHED (You)
  THAT YOU IGNORED») está entre las de menos vistas. En Tamriel, los títulos con emoji son los de menos vistas (310-355). Los títulos
  largos de tutorial de Tamriel (73-93 caracteres) funcionaron por BÚSQUEDA: no se copian para listas ni para lore.
- **Fuera:** YouTube permite 100 caracteres, pero en el celular se ve como mucho ~50-60 (depende del aparato y del ancho de las
  letras); la mayoría de las guías piden 50-60 y lo importante en los primeros ~40. Los paréntesis no muestran ninguna ventaja
  medible (solo ~8 % de los títulos con más de 1 M de vistas los usa). El empaque es título + miniatura juntos (Paddy Galloway):
  se complementan, no se repiten. El A/B de Studio («Probar y comparar», hasta 3 títulos) elige por TIEMPO DE VISUALIZACIÓN, no por CTR.

**Reglas (se cumplen siempre; `yt subir`/`yt aplicar` RECHAZAN el título que rompa las dos primeras):**
1. **Sin paréntesis ni corchetes** `( ) [ ]`. El dato extra («el n.º 1 es el peor») va en la MINIATURA o en la descripción.
2. **Largo: 40-55 caracteres; tope duro 60** (Shorts: ≤ 40 sin contar `#Shorts`). Leerlo como se ve en el celular: lo de después
   del carácter 50 casi nadie lo ve.
3. **Una sola frase limpia:** sin `|` ni guiones separadores, sin emoji. Los dos puntos SÍ valen tras un nombre propio
   («Angwe: el villano más temido de la historia de WoW», «Hydra: El Sacerdote Que Humilló a Todos en WoW», de los más vistos de
   Warcraft), nunca para colgar un segundo título detrás.
4. **Palabra clave del público al principio o muy cerca** (Fallout, Skyrim, WoW, el nombre del personaje) y el número si es lista
   («Los 25…», «Las 5…»): en las listas, el número va primero.
5. **UNA o DOS palabras en MAYÚSCULAS**, la que carga la emoción (MALVADOS, NUNCA, IGNORASTE), nunca medio título.
6. **Curiosidad sin mentira:** promete algo que el video cumple (lo dice la voz y se ve). Nada de «no creerás…» ni de clickbait
   que el video no paga. Mejor una palabra fuerte concreta (peor, prohibido, nunca, oculto, malvado) que tres adjetivos.
7. **Título y miniatura se reparten el trabajo:** la miniatura NO repite el título; añade lo que falta (en `fo_refugios_25`: el
   título dice «Los 25 refugios más MALVADOS de Fallout» y la miniatura «EL PEOR REFUGIO»).
8. **Repetir la fórmula que ya funciona en el canal** (`canales/formula/<alias>.md`) y cambiar UNA variable; anotar 2 alternativas
   en `titulos_alternativos` de `youtube.json`. Cuando se pase por Studio (monetización, video relacionado), montar el A/B
   «Probar y comparar» con el título y las 2 alternativas si el canal lo tiene; apuntar el ganador en la fórmula del canal.
9. **Idioma natural del canal:** español latino neutro (Wild Next Door, en inglés); tildes y signos ¿¡ bien puestos.
Cómo comprobar antes de subir: `python -c "import sys; sys.path.insert(0,'nucleo'); import youtube; print(youtube.revisar_titulo('<título>'))"`.
Saltarse el rechazo solo con el OK expreso del usuario: `FAB_TITULO_OK=1`.

## REGLA: render terminado = SUBIR Y PROGRAMAR en el hueco (el usuario, 20-oct-2026, CUALQUIER canal)
«Súbelo y prográmalo en el hueco que se necesite, y documéntalo para que así sea siempre: cuando rendericemos hay que subir y dejar
programado; lo mismo aplica para cualquier canal.» (dicho sobre `asteroide_invisible`, Kuriox). Es autorización permanente:
- Al terminar `final` + `verificar` y la revisión de rigor del MASTER (hoja 2×3 + 1 cuadro/3 s) **sin bloqueos**, Claude sube SIN
  preguntar: `python fab.py yt subir <v> <canal> private --publicar <ISO UTC>` (privado + `publishAt`; miniatura, `youtube.json` y .srt).
- **Hueco** = el que da `python fab.py canales --actualizar` para ese canal (el siguiente libre de su `horario`), comprobado con
  `yt videos <canal>` + BITACORA. Si choca (`comprobar_separacion`), el siguiente hueco libre; **nunca `--forzar`**.
- Después: registrar en `canales/<alias>.json` → `publicados` (`programado`, `formato`), BITACORA, `ESTADO.md`; `canales --actualizar`
  y decir al usuario fecha/hora programada (CDMX) y qué canal se queda antes sin video.
- Sigue requiriendo preguntar: hacer público YA (sin fecha), `--forzar`, y los videos que el usuario se reserva (p. ej. los privados de
  reserva de Warcraft). Si la revisión del MASTER encuentra un bloqueo, se arregla antes; no se sube flojo.
- Reels de Facebook (Juchipila) no van a YouTube: esta regla no les aplica.

## REGLA: lo que la API no hace, se hace en Studio con el navegador integrado (el usuario, 21-oct-2026, TODOS los canales)
«Lo que no puedas hacer entra en el navegador y hazlo» — la sesión principal de Google (jairedson5) ya está iniciada en el navegador
integrado y gestiona todos los canales. Tras cada `yt subir`, en Studio:
- **Cambiar primero al canal correcto** (avatar > Cambiar de cuenta > el canal): Studio abre por defecto **Edsonxn** y su buscador
  solo ve los videos del canal activo. Lo fiable: `studio.youtube.com/channel/<canal_id>/videos` y desde ahí abrir el video.
- **Short → «Vídeo relacionado» = su largo** (Detalles > columna derecha > lápiz > elegir > Guardar). Solo ofrece videos YA PÚBLICOS
  y el campo no aparece hasta que YouTube termina de procesar el Short: si el largo sale más tarde, se pone cuando salga (anotarlo en
  «siguiente» del `ESTADO.md`). La Data API no tiene este campo. **3-nov-2026 (`sopa_short`):** con el Short aún privado/programado
  Studio deja elegir el largo y «Guardar» se apaga, pero al recargar vuelve a «Ninguno»: ponerlo cuando el SHORT ya sea público.
- **Canales monetizados (`"monetizado": true` en `canales/<alias>.json`; al 17-nov-2026: Crónicas de Warcraft, Crónicas de Tamriel y Runa Caída):
  **REGLA DE ORO (el usuario, 17-nov-2026): CADA video subido se deja con la monetización ACTIVADA y la casilla de anuncios MID-ROLL marcada, en la
  misma sesión de la subida, sin que el usuario tenga que hacerlo** («a veces subes videos y no activas la monetización y luego yo la tengo que
  activar… activa la casilla de mostrar anuncios en mid-roll, que a veces no se ponen»). `yt subir` apunta el video en
  `canales/monetizacion_pendiente.json`; `canales --actualizar` y `yt monetizacion` lo listan; al terminar y comprobarlo (recargar la pestaña:
  «Activada» y mid-roll marcado) → `python fab.py yt monetizado <id>`. Si la versión SD aún no deja guardar, se espera y se vuelve en la misma sesión;
  si la sesión se acaba antes, queda en la lista y en «siguiente» del `ESTADO.md` (la siguiente sesión lo hace primero). Canal nuevo que entre al
  Programa de Socios → `"monetizado": true` en su json el mismo día.
  pestaña «Monetización» del video → Anuncios **Activado** + todos los tipos de anuncio (pre/mid/post-roll; mid-rolls automáticos
  en videos ≥ 8 min) y el **cuestionario de idoneidad para anunciantes** respondido con verdad → Guardar. La API no lo expone.
  Studio no deja guardarlo hasta que termina de procesar la versión SD. No hay interruptor de anuncios por canal (Configuración >
  Ajustes de subida > Monetización solo tiene la casilla de mid-rolls, marcada en Tamriel el 21-oct): se activa video por video. Lo
  subido por API a Warcraft solía salir «Activada», pero `wow_curiosidades_kalimdor` (21-oct) salió «Desactivada», igual que Tamriel
  (tes_misiones_nunca) → revisarlo SIEMPRE.
  Ruta directa: `studio.youtube.com/video/<id>/monetization` (abre en el canal del video). Cuestionario de un video de gameplay
  de Skyrim/WoW (21-oct, salió «Adecuado para anuncios»): Violencia = 1.ª opción (violencia de gameplay sin editar, sangre mínima),
  Contenido desagradable = 1.ª (con contexto), Temas delicados = 1.ª (mención breve/ficción); el resto sin marcar → Enviar →
  Guardar (sí deja guardar aunque avise de la versión SD; queda «Comprobando»).
  **Cuidado al marcar (23-oct-2026, `wow_objetos_raros`):** al desplegar una sección el diálogo se desplaza y el clic cae en OTRA
  (se marcó por error «Contenido para adultos»; se canceló sin enviar). Marcar por JS: cada `[role=radiogroup]` se identifica por el
  texto de su 1.ª opción (Violencia = «Se muestran intervenciones de la policía…», Desagradable = «Contenido ligera o moderadamente
  desagradable…»), `.click()` y comprobar `aria-checked` antes de Enviar; el resumen debe decir «Nada» en las demás.
  **Cada video se responde por SU contenido, no copiando el anterior** (21-oct): «Temas delicados» = violencia doméstica, autolesiones,
  suicidio, abuso o acoso sexual, aborto; un video de curiosidades sin nada de eso lo deja SIN marcar (`wow_curiosidades_kalimdor`:
  solo Violencia 1.ª —gameplay sin editar tras los 7 primeros segundos, violencia leve— y Contenido desagradable 1.ª). Los tipos de
  anuncio (pre/mid/post-roll) no aparecen hasta que termina la versión SD: se dejan para la siguiente visita.
- **Subtítulos (.srt): el navegador integrado NO abre el selector de archivos** («Subir manualmente» > Continuar no hace nada).
  Camino: el usuario reconecta el canal con `python fab.py yt conectar` (pide el permiso youtube.force-ssl) y luego
  `python fab.py yt aplicar <v> <canal> <id>` sube el .srt por API (conserva privado + `publishAt`). Tamriel ya reconectado con
  force-ssl el 21-oct; en `conectar` hay que elegir el canal correcto en la pantalla de Google (el token queda por canal).
- Listas de reproducción SÍ van por API (`playlists.insert` / `playlistItems.insert`, 50 de cuota cada una).

## REGLA: NUNCA varios videos del mismo canal el mismo día (el usuario, 7-oct-2026)
Origen: el 7-oct-2026 se hicieron públicos de golpe 3 videos de Wild Next Door (arañas, ciempiés, bichos en
invierno) un día después del de avispas. Hubo que retirarlos a privado. **No se repite.**
- **Un video por canal a la vez, espaciados.** Separación mínima entre dos videos públicos o programados del
  mismo canal: `horario.separacion_min_horas` de `canales/<alias>.json` (48 h por defecto). Wild Next Door:
  uno cada 2-3 días.
- **Si hay varios videos listos (lote):** todos se suben en PRIVADO y se programan (`--publicar <ISO UTC>`)
  en huecos sucesivos del calendario; antes se le enseña el calendario al usuario. «Súbelos» o «publícalos»
  dicho sobre un lote NO significa «todos hoy».
- **Antes de publicar o programar:** `python fab.py yt videos <canal>` + BITACORA para ver qué hay público o
  programado cerca de esa fecha.
- **El código lo impide:** `yt publicar ... public`, `yt publicar ... --programar` y `yt subir ... public /
  --publicar` se detienen (`comprobar_separacion` en `nucleo/youtube.py`) si chocan con otro video del canal.
  `--forzar` solo cuando el usuario pidió expresamente esa excepción para ese video, nunca por iniciativa propia.
- **Un video que ya fue público no se puede volver a programar por API** (HTTP 400): por eso hacer público es
  difícil de deshacer; ante la duda, privado + programado.

## Horario de publicación (investigado 2026-09-28; revisar con métricas propias)
- Audiencia objetivo: México/Latinoamérica (+ España). Videos largos: **miércoles a viernes 14:00 CDMX
  (20:00 UTC)** = 15:00 Bogotá/Lima, 17:00 Buenos Aires, 22:00 Madrid; alternativa sábado/domingo 10:00 CDMX
  (16:00 UTC). Regla: publicar 1-2 h antes del pico de la audiencia. Shorts: 18:00-21:00 locales.
- Constancia > hora exacta: 1-2 videos por semana el mismo día/hora. Programa con `--publicar` (UTC).
- Cuando el canal tenga datos, pide al usuario la gráfica "Cuándo están conectados tus usuarios" de
  YouTube Studio > Estadísticas > Audiencia (no está en la API) y ajusta `horario` en `canales/<alias>.json`.

### Frecuencia y hora de CADA canal: Claude las decide con datos y las cambia (el usuario, 13-oct-2026; vale para TODOS los canales)
El usuario autorizó que, **cada vez que analices un canal para hacer un video** (paso 2 del protocolo: `yt metricas`, `ideas`,
`canales --actualizar`, la gráfica «Cuándo están conectados tus usuarios» si el usuario la pasa), recojas esos datos y **cambies
la frecuencia y la hora** de ese canal según lo que decidas. Los ciclos y horas anteriores (Wild Next Door cada 3 días, LogIA 4-5,
Plastitube semanal martes 19:00 UTC, etc.) eran puntos de partida, no leyes: tú los ajustas.
- **Qué mirar:** vistas y % visto de los últimos videos según día/hora de salida, ritmo real de producción, cuánto tardan en arrancar
  los videos (vistas a 48 h vs. a 7 d), cola de videos listos, hueco actual del canal (`canales --actualizar`).
- **Cómo se cambia:** edita `horario` en `canales/<alias>.json` — `ciclo_dias` (lo lee el panel/«Canales»), `separacion_min_horas`
  (≈ ciclo × 24: es el freno de `youtube.py`; si no lo subes/bajas junto con el ciclo, el freno manda), `hora_local`, `utc`, `zona`.
  Añade una entrada a `horario.historial` (`fecha`, `ciclo_dias`, `hora_local`, `motivo` con el dato que lo justifica) y una línea
  en `BITACORA.md`.
- **Díselo al usuario** en la misma respuesta: «cambié X de A a B porque …». No pide permiso, pero no es silencioso.
- **Límites que NO cambian:** nunca dos videos del mismo canal el mismo día ni por debajo de `separacion_min_horas`; lotes en
  privado y programados en huecos sucesivos; un video renderizado se sube ya programado en su hueco (20-oct); hacer público YA sigue siendo del usuario.
- Con pocos datos (< 1.000 vistas/28 d) di que la decisión es por criterio, no por datos, y revisa cuando haya más.
- **Crónicas del gaming** (`cronicas_gaming`, terror CRT): arranca el 13-oct-2026 con un video cada 4 días a las 18:00 CDMX
  (00:00 UTC del día siguiente; terror = tráfico de noche), por pedido del usuario el ciclo y por criterio la hora.

**MINIATURAS = FLOW EN TODOS LOS CANALES (el usuario, 1-nov-2026: «las miniaturas siempre van con flow en todos los canales»).**
   Claude la genera en Flow (navegador integrado, Nano Banana 2.1, x2, texto dentro, ingredientes reales pegados) con el estilo
   de cada canal; prompt en `videos/<v>/prompt_miniatura.md`. La de código (punto 8) es SOLO respaldo provisional para no frenar
   una subida: antes de la fecha de publicación se cambia por la de Flow con `yt aplicar` (ej. `n64_secretos`).
   **Miniaturas de WoW = QUE PAREZCA EL JUEGO (el usuario, 6-nov-2026, al rechazar la de `wow_errores_forever`: «que sí parezca el
   juego, y no de una película de Pixar»; vale para todos los canales de videojuegos con su juego).** Cuatro capas, siempre:
   (1) **fondo real del juego**: captura in-game de una zona o ciudad sacada de `medios/` (nunca un cuadro de cinemática o tráiler);
   (2) **1-2 personajes reales**: modelo in-game (captura, pantalla de creación, render de Wowhead) o arte oficial de ese personaje
   (las antiguas del usuario: Arthas, Alamuerte, el huargen; `C:\googleimagenes\thumbnails\*_usuario.jpeg`);
   (3) **interfaz real**: ítems con su ícono y tooltip, un cuadro de misión, la barra de acciones, el error rojo, marcos de unidad, según
   el tema (buen ejemplo: `wow_clases_ocultas`); (4) logo real + 1-3 palabras amarillas y blancas con contorno negro.
   Flow combina el fondo y los personajes con el prompt «keep the exact in-game World of Warcraft graphics of the ingredients (game
   screenshot look, painted textures, in-game character models); NOT a 3D animated movie, NOT Pixar, NOT clay, NOT cinematic CGI, do not
   redraw the faces». Los cinemáticos/tráileres no sirven de base para los personajes: Flow los vuelve plastilina. La interfaz (un
   tooltip con las estadísticas de un ítem raro/épico del video, un cuadro de misión, el error rojo) va como ingrediente real en Flow o
   pegada encima; el logo puede pegarse con PIL. **EL TEXTO LO ESCRIBE NANO BANANA, NUNCA PIL (el usuario, 6-nov-2026, TODOS los
   canales: «los textos los tienes que hacer con Nano Banana… el font que tú usas no está tan adecuado a la miniatura»):** se pide en el
   prompt con «bold, eye-catching YouTube thumbnail lettering» y el texto exacto deletreado; solo se corrige por código si un acento sale
   mal tras dos intentos. Antes de subir, compárala
   en una hoja con las antiguas del usuario: si no parece el juego, se rehace.
   **«Hemos detectado actividad inusual» en Flow (15/16-nov-2026, `wow_oro_forever`):** es pasajero; no se salta ni se reintenta en
   bucle: miniatura provisional y UN reintento otro día (al día siguiente salió a la primera). Ingredientes ya subidos al proyecto se
   añaden con el botón «Añadir ingredientes» del cuadro del prompt (lista del proyecto → «Añadir a petición», en el orden del prompt),
   sin volver a pegarlos.
8. (Respaldo provisional) Miniatura por código: `videos/<nombre>/miniaturas.py` con `VARIANTES = {nombre: fn(lz) -> fondo}` (ejemplo en
   `videos/40mil_anos/miniaturas.py`) → `python fab.py <nombre> miniatura` → `salida/*_mini_<variante>.jpg`
   (1280x720) y `previews/miniaturas.jpg` (MÍRALA: incluye la vista a tamaño de celular). En el nicho funciona:
   personaje grande con cara de sorpresa, 1-3 palabras enormes amarillas con contorno negro, alto contraste.
   Usa `ojos="abiertos"` (a un T fijo el parpadeo automático puede cerrar los ojos).
   Metadatos de YouTube del video en `videos/<nombre>/youtube.json`; datos del canal en `canales/*.json`.
8b. **Miniaturas con IA (Nano Banana 2) — flujo vigente desde el 30-sep-2026.** El usuario genera la imagen en Nano Banana 2 (soporta texto) con un prompt que escribe Claude;
   luego avisa, y Claude la reduce a 1280x720 (<2 MB) y la sube. Ejemplo ganador con su prompt completo: `videos/tesoro_moctezuma/prompt_miniatura.md` («ORO PERDIDO», salió muy bien a la primera).
   Receta del prompt (en inglés, texto en español entre comillas): (1) primera línea = formato + estilo (*flat vector illustration like modern animated explainers* para que coincida con el video);
   (2) SCENE = UN solo momento dramático con sujeto grande y emoción extrema (pánico/sorpresa), el elemento valioso cayendo/brillando y fondo con contexto (ciudad en llamas, canoas);
   (3) LIGHTING AND COLOR: fondo muy oscuro y UN elemento brillante (oro) + luz de contraluz naranja/azul; (4) TEXT: «exact, Spanish, render perfectly, no extra words», 1-3 palabras en 2 líneas (blanco + amarillo #FFE21E),
   mayúsculas gruesas condensadas con contorno negro y sombra, en el tercio superior-izquierdo SIN tapar cara ni objeto clave; (5) COMPOSITION: regla de tercios, espacio oscuro limpio para el texto;
   (6) NEGATIVE: sin marca de agua, sin texto extra, sin faltas, sin rostros reales, sin desenfoque en el texto. Dar 2 variantes (misterio «¿DÓNDE ESTÁ?» y consecuencia «NUNCA APARECIÓ»).
   Si un acento sale mal: pedir corregir solo el texto conservando todo lo demás. Comprobar a tamaño de celular (~170 px de ancho): deben leerse el texto y la cara.
   Las miniaturas hechas por código (`miniaturas.py` / `hacer_miniaturas.py`) quedan como respaldo; la de IA es mucho más llamativa.
   **Texto dentro de la imagen (el usuario, 13-oct-2026): Nano Banana 2.1 en Flow escribe texto muy bien; aprovéchalo** y pide el título
   en el propio prompt en vez de sobreponerlo por código (deletrea la palabra con tilde: «spelled exactly E-X-I-S-T-I-Ó with an acute
   accent on the final O»). Claude la genera él mismo en Flow desde el navegador integrado (chip por defecto Imagen · 16:9 · 2.1 · x2,
   0 puntos). Receta y prompt probado: `docs/estilo_terror_crt.md` § «Miniatura» (`videos/sonic_exe/prompt_miniatura.md`).
   **Ingredientes en el navegador integrado (27-oct-2026):** bloquea `http://127.0.0.1` (ERR_BLOCKED_BY_CLIENT: no sirve un servidor
   local de imágenes), pero `i.ytimg.com/vi/<id>/maxresdefault.jpg` y upload.wikimedia.org tienen CORS abierto: `fetch` → `File` →
   `ClipboardEvent('paste')` en `.ProseMirror`. La miniatura oficial de un tráiler del juego es un ingrediente real de primera
   (`videos/wow_100_curiosidades_tbc_wotlk/prompt_miniatura.md`, 2/2 bien). **Un ingrediente por llamada (3-nov-2026):** varios
   `paste` en un mismo bucle solo adjuntan el primero; pegar uno, esperar ~5 s y pegar el siguiente. Las portadas y sprites
   «fair use» de en.wikipedia no salen en `pageimages`: usar `generator=images&prop=imageinfo` (`pokemon_rojo_azul`, 2/2 bien).
   La URL firmada `flow-content.google/image/…` también está en el `src` de los `<img>` del proyecto (curl sin cookies). Sin URL pública, una imagen de ~4 KB (256 px, WebP) cabe como
   base64 en `javascript_tool`; el canvas la reescala antes de pegarla (`robotaller_mes1`, 30-oct-2026).
   **Bajar la imagen (30-oct-2026):** los `<img>` de Flow ya son `flow.google.com/asb/…` y sin cookies devuelven HTML. La URL firmada
   `flow-content.google/image/<id>?Expires…&Signature…` viene en la respuesta del POST `batchexecute` con `rpcids=ogiZ0b`
   (`read_network_requests` con su `requestId`), y esa sí baja con curl sin cookies.
8c. **Publicación (flujo acordado con el usuario):** Claude sube el video con `python fab.py yt subir <video> <canal> private` (sube video, aplica `youtube.json`, miniatura `miniatura` y subtítulos .srt), anota el
   id en `canales/<canal>.json` (`publicados`) y en BITACORA.md. **Desde el 20-oct-2026 se sube YA PROGRAMADO en el hueco del canal
   (`private --publicar <ISO UTC>`) sin preguntar** (regla «render terminado = subir y programar» arriba); a uno ya subido sin fecha:
   `yt publicar <canal> <id> public --programar <ISO UTC>`.
   Antes de subir: cerrar VLC u otro reproductor que tenga el MASTER abierto (si no, `final` falla con PermissionError), correr `verificar` y abrir la hoja `previews/final_hoja.jpg`.
9. YouTube (`nucleo/youtube.py`, portado de RemoGravity; cliente OAuth en `canales/youtube_client_secrets.json`,
   tokens en `canales/tokens/`): `python fab.py yt ayuda`. Canal por alias = nombre de `canales/<alias>.json`
   (p. ej. `sapiens_con_wifi`). `yt videos <canal>`, `yt metricas <canal> [dias]`, `yt aplicar <video> <canal> <id>` (metadatos + miniatura +
   .srt a un video ya subido, sin cambiar su visibilidad), `yt subir <video> <canal> [private|unlisted|public]
   [--publicar ISO]`, `yt publicar <canal> <id> [public|unlisted|private] [--programar ISO]`, `yt canal <alias>` (descripción, palabras clave, idioma, país, banner). Nombre y foto de
   perfil del canal NO se pueden cambiar por API (Studio). Hacer público YA = preguntar antes; programar en el hueco = automático (20-oct).
   Arte del canal: `python canales/arte_canal.py "NOMBRE" "lema"` → `canales/arte/` (revisar `*_revision.jpg`).


## Facebook: Bitácora Perdida y Cronopapel también, publicados al instante (el usuario, 22-oct-2026)
«Ahora todos los videos que subamos a Bitácora y Cronopapel también se suben a Facebook y se publican al instante aunque en YouTube
estén programados.» Es la aprobación permanente del usuario para ESOS dos canales (para los demás no aplica).
- Página: «Historias Perdidas de México» = `historias_mx` en `E:\PaginaFace` (id de API 1388991384298203; token ya guardado).
- Tras subir y programar en YouTube: copia comprimida del MASTER (< 1 GB, la subida simple de `/videos` no admite más; H.264
  CRF 23, AAC 192k) → `python pagina.py --pagina historias_mx nuevo <slug> --tipo video --categoria historia` → copiar el mp4 a la
  carpeta, `medios` + `"titulo"` en post.json, `texto.txt` (descripción corta sacada de youtube.json: gancho, lugares, fuentes y
  créditos de fotos; sin capítulos ni enlaces a YouTube programados) → `aprobar <id>` → `programar <id> --ya`.
- Anotar el `fb_id` en el ESTADO.md del video y una línea en BITACORA.md.
