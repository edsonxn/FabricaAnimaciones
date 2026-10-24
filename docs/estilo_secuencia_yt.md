# Estilo SECUENCIA YT — gameplay de YouTube por beat (Crónicas de Warcraft; luego Tamriel y Runa Caída)

Creado el 13-oct-2026 en la mudanza desde `C:\googleimagenes` (`docs/migracion_googleimagenes.md`).
Motor: `nucleo/secuencia_yt.py` (fuente de medios) + `nucleo/secuencia.py` (beats y armado de siempre).

## Flujo
```
python fab.py nuevo <v> --yt          plantilla videos/_plantilla_yt (VOZ Applio Remy, SECUENCIA fuente="yt", LYRIA épica)
python fab.py <v> voz | seleccionar | tiempo
python fab.py <v> beats               cortes en pausas reales, ~8,6 s (clip_s)
python fab.py <v> busquedas           crea busquedas.json vacío y lista los beats; Claude escribe una búsqueda por beat; repetir valida
python fab.py <v> bajar [-j 4]        busca (ytsearch), elige tramo, baja SOLO ese tramo (≤1080p, ≥720p) y lo corta a medios/scene-NNN.mp4
python fab.py <v> medios              hojas previews/medios_NN.jpg — MIRARLAS
python fab.py <v> bajar 12,15-17 --rehacer        otro tramo/candidato
python fab.py <v> bajar 12 --q "Thunder Bluff"    otra búsqueda solo para ese beat
python fab.py <v> bajar 12 --url https://youtu.be/ID --desde 312   video y segundo exactos
python fab.py <v> fuentes             beat → video/canal/segundo; salida/creditos.txt para la descripción
python fab.py <v> video [--tramo a-b]  arma con transición slideleft (0,35 s)
```
Velocidad medida: 4 clips en 37 s con `-j 4` (≈ 100 clips de un video de 15 min ≈ 15 min).

## Cómo escribir busquedas.json (lecciones heredadas del sistema viejo)
- **2-4 palabras, en INGLÉS, nombre propio primero**: «Thunder Bluff», «Thrall Orgrimmar», «Kith'ix raid».
- **Nunca varios nombres propios juntos**: YouTube devuelve CERO (probado: «Ratchet centaur chase Barrens»).
- Lista = respaldos en orden: `["Kith'ix raid", "Unbinding of Kithix", "WoW raid boss fight"]`. Lo recién salido
  (parche de esta semana) tiene pocos videos: pon siempre un respaldo genérico.
- El sufijo `World of Warcraft` se añade solo (salvo que la búsqueda ya diga WoW).
- `{"url", "desde"}` para lo que hay que enseñar sí o sí (la captura del tema, un jefe concreto).
- **«no commentary» / «gameplay» mejor que «guide» / «farming»** (wow_clases_ocultas, 13-oct): las guías traen rótulos
  gigantes, tablas y webcam (35 de 80 clips rechazados en la primera pasada); «Westfall no commentary» sale limpio.
- `--rehacer` recuerda los videos rechazados por beat (`fuentes.json` → `_rechazados`) y no los vuelve a elegir.
- **Listas largas de lugares/PNJ de Classic (`wow_curiosidades_reinos_este`, 216 beats, 18-oct-2026): 89 rechazados (41 %)** en 6
  vueltas: guías con fichas/mapas (Thraex, Platinum WoW, WoWAholics101), webcams, marcas (DRDEEPWOUND, MACHINIMA, THELTCOLONEL),
  «like & subscribe», Warcraft II/III, cinemáticas de BfA. Lo más limpio por zona: **Meisio** («<zona> - Music & Ambience» / «Gameplay,
  No Commentary, ASMR», 1 h, 4K) → para la 2.ª vuelta, «<zona> no commentary» o `--url` de un video de Meisio con otro `--desde`.
  Revisar los rehechos en un mosaico propio (ffmpeg, un cuadro por clip) es más barato que regenerar todas las hojas.
- Búsquedas iguales en beats seguidos: el motor toma otro tramo, pero mejor variar el plano.

- **`wow_curiosidades_kalimdor` (108 beats, 21-oct-2026): 54 rechazados (50 %) en 6 vueltas.** Fuentes nuevas que ensucian: Warcraft III
  («Frozen Throne bonus campaign», RTS), retail («Midnight Falls», «Mechagon», Frondavil moderno con franjas), Turtle WoW (servidor
  privado), «Then and Now» con rótulos de zona, videos de lore/guía con su propio gráfico encima (texto del libro + portada de EverQuest
  + marca), webcams y carteles (DCARR GAMING, Noob2Boss, «Join on twitch»), mapas abiertos o pantallas de carga. Una búsqueda de zona
  puede devolver OTRA zona («Desolace Meisio» → Feralas, «Un'Goro Crater Meisio» → Crestagrana): leer el TÍTULO en la salida de `bajar`
  antes del mosaico. Planos de ambiente casi fijos (Meisio parado) se salvan con `CAMARA = {"scene-NNN": dict(a=(1,0,0), b=(1.15,0,-.1))}`
  en efectos.py (acercamiento lento) en vez de rehacer.

## Filtros automáticos (`_apto`, `_juzgar`)
- Duración del video 90 s – 240 min; fuera títulos con reaction/podcast/tier list/news/shorts; `evitar_canales`.
- Tramo dentro del 12 %–88 % del video (sin intros ni outros), sin repetir tramo del mismo video (±L+20 s) y los
  videos de beats cercanos pasan al final de la cola.
- Rechaza clip **oscuro** (luz media < 0,07), **quieto** (menús, pantallas de carga) y **webcam de streamer**: cara
  Haar que se queda fija (±12 px) en ≥ 3 de 4 cuadros fuera del centro. El tono de piel NO sirve (la madera tauren da
  94 % «piel», probado 13-oct); lo que distingue la webcam es que no se mueve con la cámara del juego.
- Sin audio: se baja solo la imagen (`ambiente=0`).

## Voz Applio: fonética (el usuario, 13-oct-2026)
La voz base (`fr-FR-RemyMultilingualNeural`) es multilingüe: una palabra en inglés le hace cambiar de idioma/acento
(«Overgear» como se escribe, frases en otro idioma). Regla: **todo nombre en inglés sin traducción oficial va en
`FONETICA`** de guion.py (`"Overgear": "Óverguir"`, `"Forever": "Foréver"`, `"Blizzard": "Blízard"`, `"self-play": "sélf pléi"`,
`"Coldflame Saber": "Cóldfleim Séiber"`…; grafías del canal en `C:\googleimagenes\FONETICA_CHECKLIST.md`). El TTS lee la
fonética y el guion queda con la grafía real (.srt, Montaje, apoyos, YouTube); `seleccionar` acepta la que dé menos CER.
Con traducción oficial (Wowhead es), se usa la traducción. «WoW» se escribe «World of Warcraft» (así lo dice la voz).
**Nada de frases sueltas de 1-3 palabras**: «Oficialmente.» salió en portugués y «Guarda ese dato.» en italiano; se alargan
(«Al menos, eso es lo oficial.»). Comprobación: Whisper sin idioma forzado por frase (`language=None`) → toda frase con
idioma ≠ es o p(es) < 0,95 se reescribe. Palabra que acaba frase y RVC emborrona («la Horda.» → «la orba»): moverla al medio.

## Lo que la revisión de la hoja tiene que cazar (los filtros no lo ven)
Otro juego u otra expansión que no toca, texto/logos de otro canal encima, fan-art estático de videos de lore,
interfaz recargada que tape el sujeto, el sujeto equivocado (otra raza/zona). Se rehace con `--rehacer` o `--q`.

## Apoyos, motion graphics y patrocinio (S2b/S3, 13-oct-2026; primer uso `wow_clases_ocultas`)
Todo vive en `videos/<v>/efectos.py` (capa de `nucleo/secuencia_fx.py`), anclado a palabras de la voz:
```
python fab.py <v> apoyos            APOYOS -> apoyos/<hash>.png (Chrome headless vía Playwright) + hoja previews/fx_NN.jpg (MÍRALA)
python fab.py <v> fx                audio/fx.wav (sin SFX nuevos no gasta créditos)
python fab.py <v> fx montaje        tramos con MG/videos pre-renderizados a 960 px para la vista «Montaje» del panel
                                    (desde el 19-oct-2026 `fx` lo hace SOLO: regla del usuario, el Montaje enseña siempre MG,
                                    pegatinas, fichas y pantallas en Warcraft, Tamriel, Runa Caída y Crónicas del gaming)
```
- **Apoyos** (`nucleo/apoyos.py`, ~30 en 11-12 min, regla de canal): `wowhead="classic/929"` = tooltip REAL en es-MX (también
  `classic/npc/3887`, `classic/spell/N`); `tarjeta=dict(titulo, calidad, icono, lineas, pie, ancha)` SOLO con datos del guion;
  `web=URL` (captura 1920x1080, oculta avisos de cookies sin aceptarlos); `img=ruta|URL` con marco dorado y `titulo` debajo.
  Centro `size` .56-.62 (el objeto es el protagonista); a un lado `x≈.72, size .40-.50` (más chico no se lee: < 30 px de letra).
  Si el clip de debajo trae su propio tooltip grande, tarjeta al centro + FX `oscurecer` en el mismo rango. Una lista que
  crece (p. ej. los 11 conceptos) = varias tarjetas seguidas con `anim="fade"`.
  Íconos: nombres de Wowhead (`wow.zamimg.com/images/wow/icons/large/<n>.jpg`, comprobar con HEAD). warcraft.wiki.gg BLOQUEA
  scripts (403 «Blocked»): para jefes/PNJ usar el tooltip de PNJ de Wowhead.
- **Motion graphics** (`nucleo/mg_wow.py`, por código; sustituye a Remotion): `filas` (casillas que se llenan: 3/5/10),
  `grupos` (19 libros = 9 + 9 + «?») y `contadores` (119 pergaminos, 12 reinicios + remate verde). FX `mg` con `marcas`
  = anclas de la voz; `y=.76`. Cero cifras inventadas.
- **Patrocinio Overgear** (corregido por el usuario el 13-oct-2026): narración propia en el guion (texto aprobado por el
  usuario) **y el código también con nuestra voz** (frase propia «Usa el código CRONICAS10 y te llevas un diez por ciento de
  descuento.»). Del creativo (33,0-39,97 s) se usa **solo la imagen**, nunca su audio: el cambio de voz se notaba. Va como
  FX `video` (`desde=33.0`, `de=("scene-0NN", -6.97)`, `a="scene-0NN"`) con `FUNDIDO` 0 en ese beat y `PISTAS = []`;
  el `"post"` de la escena `overgear` estira la escena para que la imagen del código entre con «CRONICAS10» y acabe en el
  puesto siguiente. Assets de `D:\Cronicas de Warcraft\Overgear\` copiados a
  `medios/_overgear/` (pantalla verde → `croma=True`); captura de overgear.com/games/wow como medio de un beat (el brief la exige).
- **Cambiar la voz con los clips ya bajados**: `voz` → `seleccionar` → `tiempo` → **`reajustar`** (mueve los cortes de
  beats.json a los tiempos nuevos SIN renumerar; base: `timeline_beats.json`, que `beats` guarda) → `fx`. NUNCA `beats` de
  nuevo (renumeraría los clips). Los efectos se anclan a palabras y se mueven solos.
  Los clips se bajan con solo 0,3 s de margen: si la voz nueva crece, casi TODOS los beats quedan cortos → `bajar <ids> --rehacer -j 2`
  con la misma url/desde (antes, sincroniza `busquedas.json` con `fuentes.json`: los beats bajados con `--url` a mano no quedan en
  busquedas) y revisa el FINAL de cada clip (negro/menú en el tramo nuevo). Lyria: `armar` solo estira ±12 %; si la duración cambia
  más, respalda los tramos y `lyria_tramos.py generar` los pide a la medida (~35 s cada uno). `fx` rehace ya los tramos del
  Montaje cuyos clips cambiaron (antes la firma no miraba `medios/`). Caso: banjo_tooie con voz Hope, 19-oct-2026.
- **Pantalla final**: `final` anexa el clip de salida del canal («Gracias por ver / Video anterior / Recomendado», 20,6 s,
  con su audio) de `canales/<alias>.json` → `pantalla_final` (`E:\FabricaAnimaciones\pantallas_finales\`). Los elementos
  de la pantalla final (video anterior, recomendado) se colocan en YouTube Studio sobre esos últimos 20 s.
  Los clips sustituidos van a `medios/_respaldo/` y su crédito a `fuentes.json` → `_reemplazados` (con `bajar --rehacer`,
  desde el 14-oct-2026, también; antes se borraban).
- Revisión: la hoja `fx` caza también clips malos que se colaron en `medios` (wow_clases_ocultas: un tramo de RuneScape
  dentro de un video «WoW Forever» y un rótulo «Hellfire Peninsula» de otro canal → `bajar N --rehacer --q "..."`).

## Música, render y miniatura (primer cierre: `wow_clases_ocultas`, 13-oct-2026)
- **MÚSICA = BANDA SONORA OFICIAL DEL JUEGO (el usuario, 23-oct-2026; Warcraft, Tamriel, Runa Caída y Crónicas del gaming): nada de
  Lyria.** Una pista por puesto elegida por lo que cuenta (tema del jefe/personaje del que se habla, la zona, el tema principal en gancho y
  cierre), de los canales oficiales «<compositor> - Topic» (Elden Ring: Yuka Kitamura, Shoi Miyazawa, Tai Tomisawa, Tsukasa Saitoh),
  `yt-dlp -x --audio-format wav` a `audio/ost/`, cada tramo igualado a la misma sonoridad, fundidos cruzados de 2 s y escrito en
  `audio/musica.wav` (lo que lee `mezcla`; ducking bajo la voz como siempre). Primer uso: `er_malenia_atrocidades` (lista en su ESTADO).
  Lo de abajo sobre Lyria queda para videos viejos. Riesgo: Content ID del OST (reclamo de monetización): anotarlo si llega.
- **Lyria**: `LYRIA` con `tramos` (cada uno <= 175 s) y `fab.py <v> musica` llama a `lyria_tramos.py`. En `estilo` NO pongas el
  nombre del juego («in the style of World of Warcraft»): el filtro rechaza nombres propios. Usa «classic high-fantasy MMORPG soundtrack».
- **Música del patrocinio (el usuario, 13-oct-2026): durante el anuncio de Overgear suena la «musica promo» del canal**
  (`D:\Cronicas de Warcraft\musica promo.mp3`, copiada a `medios/_overgear/musica_promo.mp3`), no la Lyria:
  `LYRIA["reemplazos"] = {"overgear": dict(archivo=..., desde=0.3, db=0, cruce=1.5)}`. `lyria_tramos.armar` la iguala al RMS de
  la Lyria de ese tramo (la mezcla no cambia) con fundidos cruzados de 1,5 s en los bordes de la escena.
- Applio: una frase corta suelta dentro de la línea («Después mostraba once conceptos.») también cambia de idioma, aunque la
  línea completa sea larga: unir con coma en UNA frase.
- **`video --hasta N` no funciona con el motor secuencia** (lo ignora y renderiza todo). Por suerte es rápido (~7,5 min para 11:39),
  así que la vista previa se corta del MASTER: `ffmpeg -i salida/<v>_MASTER.mp4 -t 60 -c copy salida/vista_previa_60s.mp4`.
- **Barras negras dentro del clip** (4:3 o letterbox de origen): la descarga ya escala a 16:9, así que las barras quedan
  incrustadas. Se arreglan con `SECUENCIA["recorte_por"] = {"scene-001": 0.05, "scene-023": 0.13}` (fracción por lado) sin rebajar.
- **Revisión del MASTER**: un cuadro cada 6 s en hojas 8x6 (3 hojas para 12 min). Cazó lo que no vieron las hojas de medios:
  barras en el clip del gancho y un mod con cara humana realista en un video de hardcore («close calls»).
  **Y además `ffmpeg -i MASTER -vf blackdetect=d=0.15:pix_th=0.06 -an -f null -`** (18-oct-2026, `wow_curiosidades_reinos_este`):
  los videos de origen traen cortes y fundidos a negro, mapas con media pantalla negra y RECTÁNGULOS negros que tapan algo;
  las hojas de medios (un cuadro a mitad del clip) no los ven. Hubo 4 negros + 2 rectángulos + 2 letterbox en 31 min: se
  arreglan con `bajar N --rehacer --q "..."` (mirar 6 cuadros del clip nuevo y pasarle blackdetect) o `recorte_por`.
  `video --rehacer` no sirve en este motor: se vuelve a renderizar todo (~29 min para 31 min).
- **Miniatura (el usuario, 13-oct-2026): Flow COMBINANDO ingredientes REALES del juego**, nunca una imagen inventada: cuadros de
  `medios/` (pantalla de creación de personaje, tooltip real, personaje, fondo) subidos como ingredientes con
  `python C:\googleimagenes\scripts\flow_thumb.py "<prompt>" --ingredientes a.jpg,b.jpg --variantes 2 --exacto` (Chrome con
  perfil `%LOCALAPPDATA%\ChromeFlowProfile` en el puerto 9222; 0 tokens de capturas). El prompt dice «image 1 as the base, keep
  the real interface faithful, do not redraw» y lo que se añade. Luego, con PIL, el logo real de Forever abajo a la izquierda. Receta y
  prompt: `videos/wow_clases_ocultas/prompt_miniatura.md`.

## Lecciones de `wow_pistas_futuro` (13-oct-2026)
- **Búsquedas de un animal/objeto suelto traen basura**: «WoW shark» devolvió *Baby Shark* (Pinkfong) y «Deadwind Pass
  Karazhan» una cinemática hecha con IA. `evitar_palabras` ya filtra «ai cine/ai movie/ai generated/pinkfong/baby shark/
  nursery/infantiles», pero la hoja `medios` sigue siendo obligatoria: 25 de 77 clips se rehicieron tras mirarla (webcams de
  streamer pequeñas que el filtro Haar no caza, logos de otros canales, una pantalla de Wowhead).
- **Lo de la beta con nombre propio = `{"url", "desde"}`** de un video buscado antes con
  `yt-dlp --flat-playlist "ytsearch5:WoW Forever Gilneas"`: salió limpio en Gilneas, Grim Batol y Cavernas del Tiempo. Si el
  video tiene webcam fija, usa otro creador (Kaghoegaming la tenía en los 3 tramos).
- **Clip 4:3 con barras laterales** (Warcraft I, pillarbox): `recorte_por` 0.13 lo llena. Lo cazó la hoja del MASTER, no la de medios.
- **`img=` local en APOYOS**: ahora se incrusta como data URI (`nucleo/apoyos.py`); antes `file://` salía en blanco. Usa
  ruta absoluta con `/` (en `r"C:\...\videos"` el `\v` no se escapa si se edita con sed).
- `bajar` se cayó una vez con `WinError 32` (clip abierto por el Montaje del panel): repetir `bajar` completa lo que falte.

## Crónicas de Tamriel con este motor (primer video `tes_misiones_daedricas`, 13/14-oct-2026)
- **Misma fórmula que Warcraft, voz Chatterbox `Sarcastica.mp3`** (`VOZ = dict(referencia=".../Sarcastica.mp3", idioma="es",
  exaggeration=.6, cfg_weight=.35, temperature=.75)`), `FONETICA` para los nombres (Boethiah → Boétia, Hircine → Írsin,
  Skyrim → Eskáirim…), `sufijo="Skyrim"`, sin patrocinio. Guion con la «gema» (memoria de googleimagenes).
- **Voz:** 4 tomas × 82 frases iba a ~2,4 h (≈ 2,3 tomas/min): usar `voz --seeds 1 2` y una ronda `--seeds 3 4 --solo` para
  las que fallen. Whisper escribe distinto los nombres daédricos (Boecia, Ircine, Falcreaz, «Harvalgruf», Berulus) →
  `CER_MAX_POR_FRASE` 0,03-0,045 tras leer cada transcripción; frases > 10 s que hablan hasta el final → `TAIL_MAX_POR_FRASE` .46.
- **Motion graphics por código `nucleo/mg_tes.py`** (interfaz de Skyrim: humo negro difuminado, separadores hueso con
  rombo, Bahnschrift Condensed en mayúsculas espaciadas, rojo sangre): `mision` (aviso «Misión iniciada», uno por puesto),
  `objeto` (ficha del inventario con las cifras en *negrita*; sustituye a los tooltips de Wowhead), `rejilla` (2 de 100),
  `traiciones` (siluetas que caen y contador), `reloj` (anillo que se vacía), `contadores`. Fichas a `x=.76, y=.30`, 780 px.
- **Clips malos que cazó la hoja** (35 de 76 en tres rondas): inventarios/menús, mapa, pantalla negra, estatua real
  desempaquetada, comentario de YouTube con cara, marcas de agua (BLUxCHEESE «Tweakedculture1», TIMENG, Bandicam,
  NCHOANTHOMZ), arte de ESO, rótulos grandes de otro canal («THE QUEST»). `evitar_canales` para los reincidentes.
  En `--q` NO uses apóstrofos («Haemar's Shame» tumbó la descarga): «Haemars Shame».
- **`bajar --rehacer` ya no borra el clip viejo** (14-oct): lo mueve a `medios/_respaldo/` y lo devuelve si la descarga
  nueva falla. Antes, un HTTP 429 / «Sign in to confirm you're not a bot» de YouTube (tras ~150 descargas en la sesión)
  dejó 4 beats sin clip. Ante un 429: esperar 30-60 min; no insistir.
- **Miniatura de Tamriel = estilo PROPIO del canal** (no el de Warcraft): ver `videos/tes_misiones_daedricas/prompt_miniatura.md`.
  **El personaje debe verse como el PNJ REAL del juego (render 3D de la imagen de la wiki), no como ilustración pintada**
  (el usuario, 23-oct-2026, `tes_cosas_inutiles`: eligió la versión con Nazeem «real» sobre la pintada). En el prompt: «keep the
  man from image 2 exactly as the in-game 3D character render, not painted».
- **Lecciones de `tes_exploits_rotos` (17-oct-2026):**
  - **FONÉTICA: `"Skyrim": "Escairim"`** (el usuario, 23-oct-2026, `tes_cosas_inutiles`: «dice mal Skyrim, ponlo como escairim»;
    sustituye a «Eskaai rim» del 17-oct). Si en alguna frase Whisper oye «Skirim», reescribir esa frase, no volver a la grafía vieja.
  - **PEGATINAS (el usuario, 17-oct-2026: «cuando hables de objetos, ropa o personajes busca una imagen de esa cosa y ponla como pegatina
    con animación»)**: `mg_tes.pegatina(ruta, titulo, tam)` — imagen REAL recortada con borde blanco y sombra (las fotos opacas, p. ej.
    retratos de PNJ, salen como tarjeta redondeada), entra con rebote y giro, se balancea y flota; píldora negra con el nombre. Helper
    `peg(en, slug, titulo)` en `videos/tes_exploits_rotos/efectos.py`, abajo a la izquierda (`x=.17, y=.64`) para no chocar con las fichas
    (arriba a la derecha) ni con los avisos; varias seguidas en fila (`x` .12/.29/.46/.63) cuando la voz enumera. ~26 en 10,5 min.
    Imágenes de la wiki de Fandom: `elderscrolls.fandom.com/api.php?action=query&prop=pageimages&pithumbsize=600&titles=Bucket (Skyrim)`
    (renders con fondo transparente); pociones/venenos: `prop=images` de «Potions (Skyrim)» y `prop=imageinfo&iiprop=url` del archivo
    (los títulos de efecto, «Fortify Restoration», traen el ÍCONO del efecto, no el frasco). Reabrir y guardar como PNG RGBA con PIL.
  - **Búsquedas con «exploit/glitch/potion/enchanting» = MENÚS** (37 de 74 clips rechazados en la 1.ª hoja, 49 en total): usar
    «no commentary», «walk», «4k» y, para alquimia/encantamiento, escanear UN video limpio a 360p (hoja cada 10 s) y fijar `--url --desde`.
    Canales a evitar: The Glitch Report (rótulo «Flying»), Swezz Cheese (marco de transmisión PS4), Barrett Knives (forja real).
  - **El bloqueo «Sign in to confirm you're not a bot» llega a ~130 descargas** y vuelve a los pocos clips si se insiste: reintentar cada 5 min
    en segundo plano y mientras tanto avanzar miniatura/mezcla/metadatos.
  - Tras `reajustar`, los beats que crecen > 0,3 s se vuelven a bajar con la misma url/desde: el mismo segundo puede caer ahora en un menú
    (scene-021): MIRA también esos.
  - Barras negras de origen medidas por código (media de columnas/filas < 12) → `recorte_por` para 8 clips sin mirarlos uno a uno.
- **Lecciones de `tes_misiones_nunca` (19/20-oct-2026, 120 beats, 17:30):**
  - **MG nuevos con RETRATOS REALES dentro del humo** (`mg_tes`, helper `_retrato`: cabeza y torso de la imagen de la wiki, sube la luz
    de las fotos oscuras, los objetos con fondo transparente van enteros por su contorno): `rehenes` (la cabaña de Astrid: quien está
    sobre el armario arriba en rojo, «?» rojos sobre los 3 atados, aspa al que matas; vuelve en el n.º 2 con Astrid tachada),
    `sospechosos` (tablero con hilo rojo amuleto → Wuunferth, sello ARRESTADO, el hilo se corta y pasa a INOCENTE, hilo nuevo a
    Calixto con sello EL CARNICERO), `cadena` (boda → Emperador → sopa → doble → traición → santuario: eslabones en serpiente, el
    último se rompe y la casilla arde) y `balanza` (3 000 monedas contra Shadowmere, 20 000, maestros, armadura, Cicero; cada cosa cae al
    plato y lo inclina). Un MG largo puede repartirse en 2 apariciones (cadena: p4_7 con 2 pasos y p3_2-p3_6 con el resto) para no
    tapar el aviso del puesto siguiente ni quedarse quieto > 2 s.
  - **`mg_tes.objeto`: lo pegado a una negrita («*10*.») contaba como dos palabras y la última línea perdía el final** (arreglado
    20-oct). Probar siempre las fichas en `fx hoja`.
  - **La hoja de `medios` (1 cuadro a mitad del clip) no basta: la de `fx hoja` cazó 7 clips más** (mapa, inventario, menú de pociones,
    subtítulos enormes de otro canal «Head to Movarth's…» / «Quickly loot her…», marca «Spoiler Alert Theater», final en negro).
    Hoja propia de 2 cuadros por clip (1 s y 6 s) + `blackdetect` para revisar solo los rehechos.
  - Búsquedas: 33 de 120 rechazados en la primera hoja y 4 pasadas más; las guías de misión de Skyrim traen menús y mapas, y los
    videos de lore traen fan-art, *Legends* (cartas), Minecraft o UE5. Para nombres de misión, fijar `{url, desde}` de un video
    «no commentary» ya visto bueno. **Un `{url}` en busquedas.json gana a `--q`**: cambiar la entrada antes de buscar otra cosa.
  - Imágenes de la wiki: `pageimages` a veces trae otra cosa (Stones of Barenziah = un cofre, Gaius Maro = el hijo y no el comandante,
    Shiv = un PNJ): MIRAR el mosaico y buscar el archivo con `list=allimages&aiprefix=` (`Commander_Maro.png`, `Delphine_Riverwood.png`).
  - **Revisión del MASTER (21-oct): las hojas de medios y de `fx hoja` dejaron pasar 10 clips** que cazaron las hojas cada 6 s + el
    barrido: rótulo de otro canal sobre un mapa («13. SUNDERSTONE GORGE»), logo «KEIZAAL ONLINE» (mod multijugador), menú de
    inventario, subtítulos grandes en inglés de un youtuber, icono de streamer, marca «msi», negro de 0,7 s dentro del clip y dos
    quietos > 2 s (un mapa y un clip `{url}` más corto que su beat). **Rehacerlos con `--q «… 4k no commentary»` falló en 6 de 10**
    (Solstheim por ruina dwemer, Gabriella por Ventalia, una casa por un barco): lo que funcionó fue bajar a 360p la guía de la misión,
    hoja cada 6-11 s y `--url --desde` (5 de 5 a la primera). Guías limpias, sin mods: **LiveAfterLaundry** («Quest Guide»),
    **ScorbasGaming** (walkthrough por partes), **Shadow Rose** (no commentary). Evitar: Saika (personaje con mods + «INSCREVA-SE»),
    Max Modded, Ero-sama (marca), OrcCorp (logo «msi»; se quitó con `recorte_por` 0,09), canales de Keizaal Online.
  - Logo pequeño en una esquina: medirlo en un recorte a tamaño real y poner `recorte_por` = su distancia al borde + 1 %.
  - `ffmpeg -ss 3 -i MASTER -vf fps=1/6,…,tile=8x6` se saltó un tramo entero (867-1023 s) sin avisar: comprueba que las etiquetas
    de la última hoja lleguen al final del video; si hay hueco, saca ese tramo aparte.
  - `bajar --rehacer` truena con `PermissionError` si el 🎞 Montaje del panel tiene abierto el clip: reintentar basta.
- **Lecciones de `tes_cosas_inutiles` (23-oct-2026, 115 beats, 16:35, todo en 1 sesión):**
  - **6 MG nuevos en `mg_tes`** (cada uno para su idea, con retratos reales): `agenda` (reloj de 24 h con sectores por tramo del
    día y medallón del PNJ al centro; remate «Horas de trabajo: 0»), `lena` (troncos que se apilan y contador que se dispara hasta
    el precio de la casa, barra que se llena), `salud` (barras de salud rojas: 5 contra 25 y cinco bollos que igualan la poción),
    `receta` (ingredientes que entran uno por palabra y se funden en el resultado), `trato` (bifurcación del trato daédrico: camino
    A se apaga, camino B con aspa, datos y sello; en dos apariciones) y `compraventa` (línea de tiempo con +2 000/-4 000 y
    «TU BALANCE» que corre). Hojas de prueba con un script propio antes de `fx` (cuadros a varios dt sobre fondo gris).
  - **Clips: 30 + 13 + 4 + 2 rehechos en las hojas y 5 + 3 más en `fx hoja` y el MASTER.** Lo nuevo que ensucia: videos de COCINA
    con personas reales («sweetroll», «cooking»), un mando de Xbox real, teclado real, Elden Ring («mounted combat … vs Elden Ring»),
    «Unbreakable»/perks a pantalla completa, rótulos de listas de otros canales («#8 FRENZY RUNE», «Instant Kill again!!»),
    chat de stream a un lado, letreros de mods («JK's Dragonsreach», «BANDICAM» → `recorte_por`). Lo limpio: **Loopy Longplays**
    (longplays no commentary por facción), Kasaru (Gremio de Ladrones), Otaku Gamboa, guías de UESP-estilo sin rótulos.
  - Música: Lyria API sin saldo (402) → biblioteca de OTROS canales + OST original de Skyrim (el usuario lo autorizó); la OST se
    acredita en la descripción (Jeremy Soule / Bethesda) y puede traer Content ID. No catalogar esos tramos como Lyria.
- **Lecciones de `tes_armas_poderosas` (23-oct-2026, 113 beats, 16:33, todo en 1 sesión; tema elegido por Claude):**
  - **4 MG nuevos en `mg_tes`**: `ruleta` (rueda del Wabbajack que gira y frena en cada marca; giros seguidos se acortan solos para
    no pisarse; lista de resultados al lado), `niveles` (escalera del arma nivelada; `notas` enmarcan la trampa: «No se mejora en la
    forja», «Promete 30, hace 20»), `golpes` (¿cuántos golpes para tumbar a X? en dos fases: la barra de salud se vacía y el contador
    corre; en la fase B la mejor fila se pone en oro) y `barras` (barras comparadas + líneas de referencia punteadas, p. ej. la salud
    de los dragones). `_icono` tumba en horizontal las armas largas con fondo transparente (si no, quedan como astillas).
  - **Anclas y marcas = primera aparición en TODO el video**: «La Desgarradora gélida» (marca de un MG del n.º 1) casó con el aviso
    del n.º 3 y la barra salió antes de tiempo; «tiene un error» casó con «tiene un error precioso» de otro puesto. Usa un trozo que
    solo exista en esa frase. Revisar SIEMPRE en `fx hoja` que cada ficha sale en su puesto.
  - **Búsquedas «… no HUD»** (no HUD sword fight / dungeon / shout / ward spell…) salieron limpias 13 de 14 a la primera; «no
    commentary» seguía trayendo menús de forja, inventario, diario y árbol de ventajas. 56 de 113 clips rehechos en 5 vueltas. Canales a
    evitar añadidos: Spoiler Alert Theater, PIXEL STORYZ, Syzleaf, RGR29 (marcas de agua); contadores de FPS/GPU en una esquina →
    `recorte_por` .04-.09. Hoja propia de 2 cuadros por clip (1 s y 6 s, `videos/tes_armas_poderosas/_hoja_clips.py`) antes de `fx hoja`;
    los beats de más de 10 s, mirar también el final (uno acababa en el menú de la forja a los 12 s).
  - **Arreglar un tramo sin re-renderizar 20 min**: `video --tramo a-b` (sale `salida/tramo_a_b.mp4`) y empalmarlo por número de cuadro
    en `video_sin_audio.mp4` (trim start_frame/end_frame + concat, 30 fps) y repetir `final`. NO empalmar sobre el MASTER: el concat
    pierde la pantalla final. Si `final` truena con PermissionError, el panel tiene abierto el MASTER: renombrar el `.tmp.mp4` y repetir.
  - Rigor del MASTER con `_rigor.py` (un `-ss` por cuadro cada 6 s, hojas 8×6 con la hora + blackdetect/freezedetect): cazó 10 clips más.

## PEGATINAS en todo video de este motor (Tamriel 17-oct; Warcraft 18-oct-2026, `wow_curiosidades_reinos_este`)
El usuario: «cuando hables de objetos y personajes, ropa etc, busca imágenes de eso y ponlos como pegatinas **sin quitar los
elementos visuales que ya tienes**; son agregados para que el espectador vea mejor la curiosidad». Regla: cada personaje, criatura,
objeto o prenda que nombre la voz lleva su pegatina (`peg()` + `mg_tes.pegatina`, ~4 por minuto), ADEMÁS de clips, tarjetas y MG.
- Imágenes de Warcraft: **Wowpedia en Fandom** (warcraft.wiki.gg bloquea scripts): `wowpedia.fandom.com/api.php?action=query&prop=pageimages
  &piprop=original&redirects=1&titles=Hogger|Nat Pagle|…` (50 títulos por llamada); si la imagen de la página no sirve,
  `list=allimages&aiprefix=Hogger` y `prop=imageinfo&iiprop=url&titles=File:Hogger.jpg`. Guardar PNG RGBA ≤ 700 px en `pegatinas/<slug>.png`
  y MIRAR un mosaico antes de usarlas (la `Hogger.png` de Wowpedia era una escena bajo el agua; Ragnaros salía diminuto en una escena ancha).
  Objetos sin imagen: el ícono de Wowhead (`nether.wowhead.com/classic/tooltip/item/<id>` → `icon`) ampliado a 240 px.
- Tamaño 400 px (360 en fila), abajo a la izquierda (`x=.17, y=.62`); en fila (`x` .13/.30/.47) cuando la voz enumera. Las tarjetas y
  tooltips van a la derecha (`x=.72`) para no chocar. `fx montaje` las pre-renderiza para la vista Montaje del panel.
- **Más pegatinas y de tamaños distintos (el usuario, 18-oct-2026: «mete más pegatinas y de mayor tamaño… de diferentes tamaños y
  posiciones, incluso algunas que cubran la mitad de la pantalla»)**: además de las chicas abajo a la izquierda, ~1 de cada 5 va
  GRANDE (`x=.25` o `.75`, `y=.50`, `tam` 600-760 = media pantalla) para jefes y personajes icónicos, y algunas arriba (`y=.20-.36`)
  o abajo al centro. Una pegatina grande va del lado CONTRARIO a la tarjeta (`x=.72`); si la tarjeta está al centro, acórtala.
  Objetos sin imagen de Wowpedia: ícono de Wowhead ampliado (sirve a 250-320 px; los mapas de zona como pegatina NO sirven).
  Revisar con `fx hoja`: los choques típicos son grande + tarjeta del mismo lado y dos pegatinas apiladas en el mismo sitio.
- **PANTALLA COMPLETA (el usuario, 18-oct-2026)**: donde el clip no enseña lo que la curiosidad NECESITA ver (el Portal Oscuro
  apagado, la Muralla de Cringris, Naxxramas flotando, Katrana junto a Anduin), imagen REAL a cuadro entero con zoom/paneo lento:
  `pant(slug, de, a, zoom=(1.0, 1.10), pan=(x0, y0, x1, y1))` en efectos.py → FX `pantalla` (`mg_wow.pantalla`), que se dibuja
  DEBAJO de tarjetas y pegatinas. Solo en esos casos (~9 en 31 min): un clip que no encaja pero queda bien de fondo con pegatinas
  delante se queda. Imágenes de Wowpedia (`list=allimages&aiprefix=`, ≥ 1000 px), MIRAR un mosaico: descartar las que traen
  logos/rótulos, cómics con globos en inglés o algo distinto a lo que dice la voz (la «Naxxramas» oficial era Kel'Thuzad).
  Si la imagen no es apaisada va entera sobre su propio fondo desenfocado; si corta lo importante, `pan` hacia ese lado.
  Quita la pegatina de lo mismo que ya enseña la pantalla. Primer uso: `wow_curiosidades_reinos_este` (fuentes en `pantallas/_fuentes.txt`).
- **Nombres oficiales es-MX ANTES de la voz** (21-oct-2026, `wow_curiosidades_kalimdor`): `nether.wowhead.com/classic/mx/tooltip/npc/<id>`
  (ids en el `{{Elinks-NPC|id}}` de Wowpedia) da el nombre localizado: Anaya Dawnrunner = «Anaia Correalba», Cerellean Whiteclaw =
  «Cerellean Zarpablanca», Karna Remtravel = «Karna Tripirrem», A-Me 01 = «Memo 01», Kodo Kombobulator = «kombobulador kodo». Cambiarlos
  después de la voz regenera esas frases y obliga a revisar anclas de efectos.py.
- **Wowhead es-MX traduce nombres** que la voz dice en inglés (Postmaster Malown = «Jefe de correos Gassol», R.O.I.D.S. = «IFRDHR»,
  Lothos Riftwaker = «Lothos Levantagrietas»): en esos casos, tarjeta con el nombre que dice la voz y los datos reales del tooltip.

## MOTION GRAPHICS NUEVOS en cada video (el usuario, 19-oct-2026: Warcraft, Tamriel y Runa Caída)
El usuario, al ver `mg_er.hilos` en `er_miquella_atrocidades` («LOS SEGUIDORES DE MIQUELLA»: Miquella al centro y Leda, Ansbach,
Freyja, el Cornudo… atados con hilos dorados): «me gustó esa propuesta de motion; ese tipo de propuestas están bien, que no se quede
todo en pegatinas y cuadros de texto, los cuales también están perfectos». **Regla: en cada video el agente PROPONE y construye
motion graphics NUEVOS, diseñados para ese guion, donde la escena o el guion lo permitan**, ADEMÁS de pegatinas, fichas/tarjetas y
pantallas (no se quita nada de eso). **Aclaración del usuario (mismo día): «no digo que uses ese mismo motion, sino que cuando veas una
oportunidad propongas un motion nuevo, diferente, que encaje en el guion para mostrar mejor la idea o la escena».** O sea: NO es
repetir `hilos` ni ningún MG ya hecho; cada oportunidad pide un diseño propio que cuente ESA idea mejor que un clip o una ficha.
- **Dónde caben** (buscarlos al leer el guion, antes de escribir `efectos.py`; entre paréntesis, lo que se hizo en Runa como
  MUESTRA del tipo de idea, no como catálogo para repetir): una RELACIÓN entre personajes (quién sigue, sirve o
  traiciona a quién, árbol familiar, matrimonios, alianzas: `hilos`, `doble_vida`); una TRANSFORMACIÓN o fusión (`cosido`: alma +
  cuerpo = consorte; `gemelos`: un dios que se parte en dos); una SERIE con estructura (`cruces`: 13 cruces que se encienden con
  cada «Aquí abandono…»; `filas`, `grupos`, `contadores`); una COMPARACIÓN o tríada (`triada`: cuerpo / alma / voluntad, las
  anteriores se tachan); una cadena causa → efecto, una cronología, un antes/después, un engaño que se revela.
- **Cómo**: en el plan del video, 2-4 MG con su frase ancla y qué enseñan (decírselo al usuario al empezar); programarlos como
  función del kit del canal (`nucleo/mg_wow.py` Warcraft, `nucleo/mg_tes.py` Tamriel, `nucleo/mg_er.py` Runa Caída) con la interfaz
  del juego (tipografía, colores y paneles del canal), animados de verdad (entran por partes con las `marcas` de la voz; nada quieto
  más de ~2 s) y con un remate visual (algo que se corta, se tacha o se enciende en rojo). Pueden volver una segunda vez en el arco
  del MISMO video (los hilos al presentar a los seguidores y otra vez al romperse el encanto, ahora en rojo).
- Solo con datos del guion (cero cifras o nombres inventados); sin chocar con fichas ni pegatinas (mirarlo en `fx hoja`).
- **Transparencias en PIL: `ImageDraw` NO mezcla el alfa** (21-oct-2026): un `d.ellipse(..., fill=(r, g, b, 40))` sobre el panel
  REEMPLAZA esos píxeles por un 40 de opacidad y el clip de fondo se ve a través (halos de `runas` = agujeros verdosos). Halos,
  vapor y brillos se dibujan en una capa `Image.new("RGBA")` aparte y se pegan con `alpha_composite`. Cada
  función nueva se documenta en la sección de su canal en este doc, pero lo normal es **diseñar uno distinto en cada video**: un MG ya
  hecho solo se reutiliza si de verdad es lo que mejor cuenta esa escena (los contadores y casillas de Warcraft son la excepción
  natural).
- Referencias del NIVEL esperado (para inspirarse, no para copiar): Runa `mg_er.doble_vida/gemelos/hilos/cosido/cruces/triada`; Warcraft `mg_wow.filas/grupos/contadores` y (21-oct, `wow_curiosidades_kalimdor`) `runas` (cadena de suministro: 7 runas que se apagan con el agua de Azshara), `linaje` (pareja -> hijos que tachan al padre, con retratos reales en medallón), `cadena` (causa -> efecto en medallones que se tiñen de rojo) y `consola` (terminal titán que teclea «FALTAN» y estampa sellos); Tamriel
  `mg_tes.rejilla/traiciones/reloj/contadores/rehenes/sospechosos/cadena/balanza`.

## MAPAS REALES CON RUTA (el usuario, 23-oct-2026: Warcraft, Runa Caída, Tamriel y Crónicas del gaming)
El usuario: «en ocasiones hay que mostrar mapas reales del juego con rutas cuando hablemos de misiones o cosas que el espectador
quiera saber dónde es; tú decides en qué escenas y cómo… adaptados cada uno a su juego». Kit **`nucleo/mg_mapa.py`** (`mapa()`),
helper `mapa()` en `videos/_plantilla_yt/efectos.py` (en videos viejos, copiarlo de ahí con `_MAP` y `TEMA_MAPA`).
- **Cuándo (lo decide el agente al leer el guion, en el mismo plan que los MG nuevos; 1-4 por video, sin forzarlo):**
  1. **Ruta de misión**: la voz cuenta dónde empieza, por dónde se pasa y dónde acaba → **pantalla completa** 6-10 s, un lugar con
     nombre por cada sitio que la voz nombra (la ruta llega cuando lo dice).
  2. **«¿Dónde está?»**: un secreto, jefe, objeto o PNJ escondido que el espectador querría ir a buscar → **ventana** 3-5 s
     (`ventana=True`, sobre el clip, a la derecha) con 1-2 lugares; con un solo lugar no hay ruta: su marcador late.
  3. **Viajes del lore** (de dónde a dónde marchó un ejército, un exilio, una persecución) → pantalla completa.
  NO va si el guion no da geografía, ni cuando el clip de ese beat ya enseña el sitio con su nombre. Mientras hay mapa, nada de
  tarjetas a la derecha (`x=.72`) si es ventana; las pegatinas siguen (abajo a la izquierda) y se dibujan ENCIMA del mapa a pantalla.
- **Mapas = imagen REAL del juego** (nunca dibujada por código ni pintada en Flow; si no hay mapa real decente, no hay mapa).
  Guardar en `videos/<v>/mapas/<slug>.jpg|png` y la URL en `mapas/_fuentes.txt`. Fuentes probadas el 23-oct-2026:
  | Juego | Fuente | Notas |
  |---|---|---|
  | WoW | `wow.zamimg.com/images/wow/maps/enus/original/<id zona>.jpg` (id de `wowhead.com/classic/zone=<id>`; Elwynn = 12) | 1022x668 (la cámara amplía ≤ 1,6x de más: se ve bien, es pintura). Las coordenadas de Wowhead de PNJ/misiones (x, y en %) ≈ fracción /100 en esa imagen; confirmar en la rejilla |
  | Elden Ring | eldenring.fandom.com `File:ER Region Map <Región>.jpg` (4700 px) · mundo entero `ER Lands Between Map.jpg` (9644 px, con `recorte`) | Los `Map … MENU Knowledge` son el objeto «fragmento de mapa», NO el mapa |
  | Skyrim | UESP (`en.uesp.net/w/api.php?action=query&list=allimages&aiprefix=SR-map-`): `SR-map-Skyrim.jpg` (papel del juego, 2048) · `SR-map-<Comarca>_Hold.jpg` | `SR-map-All_Holds.jpg` es el político a colores (no el del juego) |
  | Gaming | la wiki del juego en Fandom (`list=search&srnamespace=6&srsearch=<juego> map`); Zelda OoT: `TheLegendOfZeldaOcarinaOfTime map.png` (1980x1440, ilustrado) | vgmaps.com tiene mapas cenitales hechos de capturas |
- **Coordenadas**: `python nucleo/mg_mapa.py rejilla videos/<v>/mapas/<slug>.jpg` → `<slug>_rejilla.jpg` con rejilla cada 0,05
  (MÍRALA y lee x, y de cada lugar). `puntos`: `(x, y)` = punto de paso sin nombre (hace que la ruta siga el camino del mapa:
  pon 1-3 entre lugares para no cortar montañas ni mar) y `(x, y, "Nombre"[, "inicio"|"paso"|"meta"|"peligro"])`. Nombres
  como los dice la voz (es-MX oficial: Villanorte, Villadorada, Páramos de Poniente, Necrolimbo, Carrera Blanca, Robledal…).
- **Temas** (`TEMA_MAPA` en efectos.py): `wow` = rayas amarillas que avanzan + «!» de misión al inicio y «?» de entrega en la meta,
  Georgia oro con contorno negro, título como el rótulo de zona · `er` = hilo dorado de la guía de gracia con chispas que corren,
  marcadores de Sitio de gracia, Garamond sobre banda negra difusa · `tes` = puntos hueso con sombra, marcador de misión de Skyrim
  (triángulo invertido que flota), Bahnschrift Condensed espaciada · `gaming` = bolitas miel que brotan con rebote y pines
  (plataformas de Rare) · `zelda` = puntos dorados, triángulo dorado en la meta, Engravers MT. **Juego nuevo de Crónicas del
  gaming = tema nuevo en `TEMAS`** con los colores/letra de la interfaz de ESE juego (marcadores en `_marcador`).
- **Animación**: la cámara empieza cerca del primer lugar y se abre a medida que la ruta avanza (`ajuste` .30 = cuánto enseña la
  ruta entera desde el principio), respira y deriva despacio (nada quieto); la ruta llega a cada lugar en su `marca`; el marcador
  rebota, su nombre busca un hueco libre (fuera del título y de otros nombres; si no hay, no se pone); la meta y los `peligro`
  emiten un anillo que late sin parar. Título arriba al centro (zona + `sub`, p. ej. «Misión: Desatado»); la ruta se encuadra
  DEBAJO de él. Rendimiento: 0,1-0,2 s por cuadro; la imagen se carga en el primer cuadro (perezoso).
- **Revisión**: `MP.hoja(fn, dur, marcas, "previews/mapa_<slug>.jpg")` antes de `fx`, y luego `fx hoja`. Cazar: lugar fuera del
  sitio real (coordenada mal leída), nombre pegado al título, ruta que cruza mar/montaña (faltan puntos de paso), ruta tan larga
  que no cabe (la cámara la sigue y los primeros lugares salen de cuadro: usar un mapa de región o partirla en dos).
- Prueba del kit (23-oct-2026): Elwynn (wow), Necrolimbo de la Iglesia de Elleh al Castillo Morne (er), Helgen → Robledal →
  Carrera Blanca (tes), Hyrule de OoT (zelda y gaming en ventana). Aún sin estrenar en un video.
- **FOTOS EN EL MAPA (el usuario, 23-oct-2026, al ver `wow_objetos_raros`; REGLA para TODO mapa de CUALQUIER canal):** «cuando
  salgan escenas de mapa, muestra también fotos del objeto, lugar o personaje del que se habla en el momento; por ejemplo, cuando
  dice que tienes que juntar ciertos ítems, al mencionarlos mostrar una foto de él, para que el mapa se sienta aún más dinámico».
  En cada lugar/paso con nombre va su foto como 5.º elemento del punto: `(x, y, "Nombre", tipo, foto)` en `mg_mapa.mapa` y
  `(x, y, rótulo, sub, foto)` en `mg_wow.ruta`. foto = imagen REAL (pegatina de la wiki, ruta .png/.jpg) o `"ico:<ícono>"` (ícono
  real de Wowhead para objetos: ingredientes, fragmentos, llaves). Sale junto al marcador con rebote cuando la voz lo nombra, en
  el primer hueco libre (esquiva título y nombres), y se va cuando la ruta llega al siguiente; la del premio se queda. El rótulo
  del paso dice el NOMBRE OFICIAL del objeto (tooltip es-MX: «Madera de roble de Piedrablanca», «Gema kor corrupta»). Sin imagen
  real de ese paso, `None` (nunca una inventada; p. ej. los objetos del ritual del Corcel nefasto no existen como ítem).
- **`mg_wow.ruta` (`wow_objetos_raros`, 23-oct-2026)**: variante de Warcraft hecha antes de `mg_mapa` — mapas de Wowhead con
  rótulos en español (`.../classic/maps/eses/original/<zona>.jpg`; `-1` mundo, `-3` Reinos del Este, `-6` Kalimdor sin `eses`),
  pines rojos numerados, línea punteada dorada con marcador que viaja, medallón del premio con halo (verde en la última marca),
  rótulos de los 2 últimos pasos. Rutas entre continentes en el mapa del mundo: centro de cada zona en su mapa de continente →
  mundo con `kal()`/`ek()` (ver `videos/wow_objetos_raros/efectos.py`). Mismo video: `forja` (receta de un legendario: los
  ingredientes vuelan al medallón, que estalla en naranja) y `sorteo` (5 000 casillas de intentos y UNA dorada: 0,02 %).

## Crónicas del gaming con este motor (Nintendo/retro; primer video `banjo_tooie`, 19-oct-2026)
- **El canal VUELVE a Nintendo/retro** (el usuario, 19-oct-2026; el terror CRT queda como especial) con la fórmula de Warcraft/Tamriel/
  Runa: historia + lore + lista de 10 secretos «QUE IGNORASTE», ~12-13 min, voz **Chatterbox `Sarcastica`** + `FONETICA` (Banjo →
  Bányo, Kazooie → Kazúi, Tooie → Túi, Jiggies → Yíguis, Jinjos → Yínyos, Gruntilda → Gruntílda…), `sufijo=""` y consultas completas.
- **Kit `nucleo/mg_gaming.py`** (estilo N64: Cooper Black, chocolate y miel, todo entra con REBOTE): `puesto(num, titulo)` (medallón con
  el número + cinta que se ajusta al título), `ficha(titulo, texto, tipo)` (cuadro de diálogo; *asteriscos* = miel), `linea_tiempo(hitos)`
  (un hito por marca; el último late en rojo), `swop()` (Stop 'n' Swop: memoria que se vacía, Nintendo lo tacha, «XBLA 2009» lo enciende),
  `jinjos()` (9 familias 1..9 = 45 + la gris «SHOULDN'T BE HERE»), `concurso()` (pesas de una tonelada que caen). Pegatinas con
  `mg_tes.pegatina` de `banjokazooie.fandom.com` (API `prop=pageimages` / `list=allimages`). Arial Rounded NO trae «·» (sale un cuadro):
  el kit lo cambia por «/».
- **Clips de N64 = serie Ninbanyan de Switch Online (1080p60, 44 partes nombradas por zona) con `{"url","desde"}`**. Para el segundo
  exacto: bajar la parte a 360p y hacer una hoja propia con OpenCV (un cuadro cada 6-25 s con el segundo impreso); 7 partes miradas
  bastaron para ~90 beats. Las escenas de video van en 4:3 dentro del MARCO de NSO (degradado gris + «P1», no negro): medirlo por
  columnas que no cambian en el tiempo (desviación < 4 en 3-4 cuadros) → `recorte_por` .145 (quita marco y franjas a la vez, 16:9).
- **El motor exige ≥ 720p** (`bv*[height>=720]`): los videos SD (KaiLightDark, ChrisPTY507, LerakoLanche, N64 Database) fallan con
  «Requested format is not available»; buscar otro en HD (illustrious rocket 720p tenía cartuchos vivos, llave de hielo, caja de hielo,
  Humba y dragón en un solo video).
- **Créditos del juego = tarjetas de ~7 s separadas por negro**: no caben en un beat de 8-10 s (el MASTER los cazó). Fundidos al final del
  clip: medir el brillo por segundo de cada clip rehecho (`cv2`, media < 20 = negro) además de `blackdetect` sobre el MASTER.
- YouTube: ~110 descargas en la sesión → 429 y luego «not a bot»; un reintento automático cada 5 min (script con los ids pendientes)
  lo resolvió en la primera vuelta ~40 min después.
- **MARCOS PINTADOS EN FLOW, no paneles dibujados por código (el usuario, 22-oct-2026, `zelda_oot`: «esos cuadros de texto se
  ven muy poco trabajados… puedes apoyarte de Flow para obtener mejor calidad»).** Los paneles de `mg_gaming` (rectángulo chocolate
  con borde miel) se veían planos. Receta nueva: `prompts.json` con piezas de interfaz SOBRE BLANCO (tablilla de piedra con marco
  de oro, pergamino con rodillos, medallón, cinta de terciopelo, tablero de templo con cresta, sello de cera, cartucho con etiqueta
  en blanco, letrero de madera, botones del mando) con una FICHA común («hand-painted video game interface asset… isolated on a
  plain flat pure white background… No text, no letters, no numbers, no runes») → `flow_integrado.py paquete` → Flow en el
  navegador integrado (Nano Banana 2.1, 16:9, x2 = 0 puntos; 9 prompts en ~2 min) → bajar con numeración 901+ → `ui/` →
  `python nucleo/recortar_ui.py pieza.jpg pieza.png [--partes N]` (quita el blanco CONECTADO al borde, conserva el interior
  claro de pergaminos/etiquetas). Kit **`nucleo/mg_zelda.py`**: `nueve()` escala sin deformar esquinas ni la cresta central
  (márgenes en `CORTES`), `brillo()` = destello que barre el oro al entrar, sombra suave, Engravers MT (títulos grabados) + Book
  Antiqua negrita; `puesto`, `ficha(piel="piedra"|"pergamino")`, `linea_tiempo`, `ocarina`, `paradoja`, `versiones`,
  `tres_lineas`. Para otro juego: mismas funciones, otras piezas (cambiar la FICHA de Flow a la estética de ese juego).
- **REGLA NUEVA (el usuario, 22-oct-2026, al ver la ficha «Carrera de obstáculos» de zelda_oot): FICHAS TRANSLÚCIDAS, nunca
  carteles opacos que cubran tanta pantalla y tapen el video.** Modelo: las de Crónicas de Tamriel (`mg_tes.objeto`/`mision`: humo
  negro difuminado, separadores finos, tipografía de la interfaz) — «los de Tamriel son los mejores» — pero ADAPTADAS a cada juego,
  no recicladas de Skyrim. Para el siguiente video: diseñar la versión translúcida con la interfaz de ese juego; las piezas de Flow
  solo como adorno pequeño (filigrana, icono, separador), y los MG grandes con panel translúcido. zelda_oot salió con las
  tablillas opacas (ya renderizado).
- **Lecciones de `zelda_oot` (22-oct-2026, 111 beats, 15:56):**
  - **Plan de clips por FRASE antes de los beats** (`videos/zelda_oot/plan_clips.py`): hojas de contacto propias a 360p de las partes
    de una serie limpia (ZeldaCentral NSO 1080p60), un cuadro cada 15 s con el segundo impreso → lista (id, segundo) por frase →
    `busquedas.json` sale solo al terminar `beats`. 111 clips con 21 rehechos en total (vs ~40-50 % en Warcraft/Tamriel).
  - **Medir el BRILLO de todos los clips (un cuadro cada 0,3 s, media < 14) ANTES del render**: `blackdetect` sobre el MASTER no
    caza negros de 0,3-0,6 s tapados por transiciones o efectos, y cada vuelta cuesta un render de ~35 min (aquí hubo 3 renders).
    Los fundidos están DENTRO del clip (fin de cinemática, cambio de zona), no solo en los bordes.
  - Fuentes que ensucian: videos con rótulo de título al principio (SoupyGhost «Gossip Stone behaviors…»), comparativas con texto
    gigante («And last but not least»), TV grabada con cámara, marca IGN en esquina, videos de UNA imagen fija (pentagrama del molino).
  - Clips cortos de fans (40-100 s) con `{url, desde}`: bajar `yt.min_s` a 30 en guion.py.
  - `medir_marco.py`: el marco NSO da 0,131; escenas casi quietas lo inflan (0,2-0,34) → fijar 0,131 para toda la serie NSO.

## Runa Caída con este motor (primer video `er_radagon_atrocidades`, 14-oct-2026)
- **Fórmula del ×24,6** (`canales/formula/runa_caida.md`): «Las 5 … QUE IGNORASTE», **~6-7 min** (el ganador de Márika duraba 5:54;
  el usuario descartó el piso viejo de 12 min del sistema anterior) · gema del canal · sin patrocinio · puente al video de Márika.
- **Voz Chatterbox `Faraon.mp3`** (`exaggeration=.55, cfg_weight=.3, temperature=.75`): lee a ~180 palabras/min (1 227 palabras =
  409 s de voz, video 7:22 con pausas). `voz --seeds 1 2` tarda ~25 min para 56 frases.
- **«Radagon» al INICIO de frase o tras pausa sale «Dradagón/Gradagón»** (la R inicial con FONETICA «Rádagon»): poner el nombre a
  media frase tras una vocal («Dice que Radagon…», «La forjó el propio Radagon…»). «Márika» en frase corta: Whisper escribe
  «Márica»/«marica» → CER_MAX_POR_FRASE .05 y elegir A MANO la toma con la tilde bien puesta (mover las otras a `voz/_descartes/` y
  quitarlas de `voz/eval.json`, o `seleccionar` revienta buscando el .wav).
- **Video largo (~20 min, `er_miquella_atrocidades`, 18-oct-2026):** 3 239 palabras = 1 120 s de voz = 19:55 a 80 BPM
  (≈ 2,9 palabras/s de voz; ~0,37 s de video por palabra). Cada puesto en DOS escenas (`p3`/`p3b`) para que Lyria no pase de
  175 s por escena. En la 1.ª ronda cayeron 51/141 frases y casi todas eran falsas alarmas (cola en frases largas, pausa
  larga tras punto, «Mohg» → «Moj/Mohawk» en Whisper): leer `voz/eval.json`, comprobar que la transcripción termina con las
  palabras del guion y fijar `CER_/GAP_/TAIL_MAX_POR_FRASE` a la mejor toma (`GAP_MAX_POR_FRASE` existe desde el 18-oct);
  regenerar solo los errores reales («restos» → «vestos», «rezaba» → «besaba»).
- **CORRECCIÓN (22-oct-2026, comentarios del Miquella publicado): «Moj/Mojé» y «Mikeya» NO eran falsas alarmas.** El público
  oyó «Miqueya y Mojé» y se burló («que la IA sea eterna», 3-4 comentarios de 32). **Causa:** Miquella se grabó el 18-oct y
  Chatterbox NO aplicaba `FONETICA` hasta el 20-oct (docs/voz.md): leyó la grafía real. Regla: si Whisper escribe un NOMBRE PROPIO
  distinto de la grafía del guion (`ll` → `y`, final `g` → `j/e`), es error real: regenerar o elegir la toma donde salga bien,
  nunca subir el CER. Grafías: «Miquella» → «Mikuéla» (en Ranni Whisper ya oye «Mikuela», sí funciona); «Mohg» con «Mog» suelta
  «Moj/Mojé» en Faraon: probar «Mog» a media frase seguido de vocal o «Móg» y comprobar en Whisper. «el Cornudo» es la traducción
  oficial de *Hornsent*: hace gracia pero es correcto.
- **Kit `nucleo/mg_er.py`** (interfaz de Elden Ring por código: Garamond `GARA.TTF`, dorado viejo, pergamino, paneles casi negros con
  filete dorado): `puesto` (banda negra a lo ancho estilo «ENEMIGO ABATIDO», `y=.80`), `descripcion` (ficha de objeto con icono real,
  *asteriscos* = dorado, el texto entra línea a línea; `x=.74, y=.30`), `mensaje` (mensaje del suelo en ámbar que se escribe solo),
  `doble_vida` (esquema de matrimonios que se funde en «RADAGON ES MÁRIKA») y `gemelos` (un solo dios que se parte en dos).
  Desde `er_miquella_atrocidades` (19-oct-2026): `hilos(centro, nombres, titulo)` (seguidores atados con hilos dorados; la
  última marca los corta y quedan enfrentados en rojo — úsalo dos veces: al presentarlos y al romperse el encanto, con todas
  las marcas en la misma ancla), `cosido(alma, cuerpo, resultado)` (dos círculos que se juntan con costura), `cruces(etiquetas,
  total=13)` (fila de cruces que se encienden con «Aquí abandono…»; `rojo_ultima` para el remate) y `triada(filas)` (columnas
  por marca; las anteriores se tachan y la última brilla). **Pegatinas en Runa Caída = misma regla que Warcraft**: imágenes de
  `eldenring.fandom.com/api.php?action=query&prop=pageimages&piprop=original&titles=…` y `list=allimages&aiprefix=…` (los
  íconos `ER_Icon_*` de 1024 px sirven a la vez de pegatina y de icono de la ficha; renders de PNJ `ER_NPC_<nombre>_2.png`
  con fondo transparente). Descartar el render de la Cruz de Miquella (una línea finísima) y las láminas de arte conceptual
  con varias figuras. Helpers `peg/grande/fila/pant/ficha/puesto` en `videos/er_miquella_atrocidades/efectos.py`.
- **Íconos reales**: API de la wiki de Fandom, `eldenring.fandom.com/api.php?action=query&prop=pageimages&pithumbsize=300&titles=…`
  (vienen en WebP aunque digan .png: reabrir y guardar con PIL). Fextralife carga las imágenes por JS (curl no las ve).
- Las citas de las fichas = descripciones de objeto/diálogos verificados en Fextralife, traducidas sin inventar.
- Búsquedas: el sufijo es «Elden Ring»; sin apóstrofos («Marikas Hammer», «Radagons Rings of Light»).
- **Miniatura**: la del ganador (pergamino + caja amarilla «ATROCIDADES DE X» + píldora negra «ELDEN RING» + personaje pintado a la
  derecha) cambiando solo el personaje; receta en `videos/er_radagon_atrocidades/prompt_miniatura.md`. Ingredientes: la miniatura
  ganadora + un cuadro real del personaje sacado de `medios/` (Radagon de espaldas con el martillo, scene-035). Salió a la primera.
- **Momento exacto de un video corto** (la estatua que cambia con la Ley de Regresión): bajarlo entero a 360p y hacer una hoja de
  contacto cada 4 s; luego `bajar N --rehacer --url … --desde S` (cazó el mensaje real «Radagon is Marika» a los 107 s).
- **Revisión del MASTER**: además de las hojas cada 6 s, barrido a 2 fps buscando media < 12 (negros) y diferencia < 0,4 durante
  > 2 s (quietos). Un clip de pelea fundía a negro a los 7,5 s de su tramo (el video de origen cortaba): `--desde` unos segundos antes.
- **Tras `reajustar`**, un beat que crece puede quedar más largo que su clip: volver a bajar ESE beat con la misma url/desde.
- **Búsquedas del DLC (`er_miquella_atrocidades`, 139 beats, 19-oct-2026): 54 clips rehechos en 4 rondas (39 %)**: mapas y menús
  de guías de PNJ (cad5150, ConCon, IGN, NeoJetty), marca de Fextralife, PowerPyx/FP Good Game/Erudur/«pgp», texto de Lance
  McDonald («DEBUGMENU.COM»), rótulos de lore (Zullie, Mage Infa), fan-art animado (Nate Sandhart), mando de Xbox en pantalla
  (vídeos «no hit»), «Thanks for watching… subscribe», «YOU DIED» y subtítulos de comentarista. Lo limpio: **«<zona> 4k» /
  «<jefe> 4k»** y los walkthroughs de **SourceSpy91** (4K60, sin comentarios) con `--url --desde`. Abyssal Woods y Stone Coffin
  Fissure devuelven casi siempre el MAPA (la zona se busca en el mapa): fijar `--url`. Para revisar rehechos, un mosaico de
  3 cuadros por clip (20/50/85 %) caza lo que un solo cuadro no ve (menú al final del clip, «YOU DIED» al 85 %).
- **`er_ranni_atrocidades` (21/22-oct-2026, ~12 min, 83 beats, 1 sola sesión de guion a MASTER):**
  - MG nuevos en `mg_er`: `marionetas(titiritero, munecos, dueno)` (cruceta con muñecos; la última marca da la vuelta y el titiritero
    cuelga de los hilos de `dueno` en azul luna), `sombra(ama, sombra_, amos)` (los Dos Dedos atan a la Empírea y a su sombra; ella
    corta su hilo y la sombra tiembla en rojo), `domino(fichas)` (fichas que caen una sobre otra, la última en rojo; causa → efecto) y
    `constelacion(nombres, centro, tu, remate)` (estrellas unidas a la Luna que se apagan una por marca; queda «Tú» y el remate).
    Repartidos en 2-3 apariciones del mismo MG con las marcas ya pasadas al inicio, para no tapar pegatinas ni quedarse quietos.
  - **Fijar url+segundo ANTES de bajar** con hojas de contacto a 240p de 3-4 videos limpios (SourceSpy91 Part 18 y Part 25 de la
    misión de Ranni, el final de 4KGameScape, la intro de BonfireVN): 17 de 83 rehechos (20 %) frente al 39-50 % de los videos anteriores.
  - **Marcas de agua nuevas**: Shirrako firma «SHIRRAKO» abajo a la derecha en TODOS sus clips (`recorte_por` .09; las hojas de 240 px no
    lo ven, solo un recorte a tamaño real de la esquina), «KGA», «Misternoobie», «DRAKULUS»; un cartel de texto de otro canal («I forgot
    to script this…»), un «tributo» con IA (Abyssal_Realms_) y una mujer de acción real hecha con IA en «Ranni the Witch 4k». Las
    búsquedas «Seluvis Rise», «Deathroot location», «Two Fingers Roundtable» devuelven MAPA o MENÚ.
  - Toma repetida: la misma escena de Ranni en la ventana salió 8 veces (P18 y otros videos que graban lo mismo): repartir planos.
  - Anclas: comprobar TODAS de una vez contra `timeline.json` con límites de palabra («el dragón» ≠ «del dragón») antes de `fx hoja`.
  - Voz Faraon: 31 de 33 «REGENERAR» eran falsas alarmas (Selubis, Blythe/Blyde, E.G./Ishi por Iji); reales: una toma que se comía
    las dos primeras palabras («Media comunidad») y «rito» → «grito» (cambiado a «ritual»).
- **`er_malenia_atrocidades` (23-oct-2026, ~19 min, 134 beats):** 37 rehechos en 3 rondas (28 %) con url+segundo fijados por CAPÍTULOS de
  YouTube (`yt-dlp --print "%(chapters)j"`: SourceSpy91 Part 20 Caelid de 4,5 h marca cada jefe/zona). **Gamerpillar** (guías de misión)
  lleva rótulos «STEP N» en todos sus clips: evitarlo. Mapas: un mapa de ruta se queda quieto en cuanto la ruta llega (la cámara apenas
  deriva): terminarlo ~1,5 s tras la última marca o `freezedetect` lo caza (3,9 s). Música = OST oficial (ver § Música).
- **NUNCA `bajar` dentro de `while read … <<EOF`**: los procesos hijos se comen el stdin y la siguiente vuelta lee basura como id;
  `bajar --q` sin ids rehízo los 51 beats (se recuperó todo de `medios/_respaldo/`). Desde el 14-oct el motor se niega a `--q`/`--url`
  sin ids; en bucles, `< /dev/null`.

## Pendiente del estilo
«Cambiar clip» desde el bloque del Montaje; dos apoyos a la vez en el mismo instante (hoy se pueden, pero se enciman).
