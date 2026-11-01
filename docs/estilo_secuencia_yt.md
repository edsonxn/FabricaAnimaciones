# Estilo SECUENCIA YT — gameplay de YouTube por beat (Crónicas de Warcraft; luego Tamriel y Runa Caída)

Creado el 13-oct-2026 en la mudanza desde `C:\googleimagenes` (`docs/migracion_googleimagenes.md`).
Motor: `nucleo/secuencia_yt.py` (fuente de medios) + `nucleo/secuencia.py` (beats y armado de siempre).

## REGLA DE ORO Y LISTA DE CONTROL (el usuario, 30-oct-2026; leer ANTES de escribir `efectos.py`)
`videos/tes_secretos_40/` es el nivel mínimo: el usuario lo aprobó con «la edición quedó perfecta, el guion perfecto, la burla perfecta» y
pidió aplicarlo en todos los demás canales. Vale para Warcraft, Tamriel, Runa y Gaming con su kit y su interfaz; los canales con otro
motor aplican las mismas ideas con el suyo (`docs/reglas_globales_completas.md` § «REGLA DE ORO»).

**Las reglas SUMAN, nunca sustituyen.** Lo que perdió la primera versión de ese video fue justo eso: al añadir mapas bajaron las fichas
de ~28 a 11, el primer MG salió en 3:42 y no hubo otro hasta 13:12. Todo pedido nuevo se añade encima de esta lista:

| Capa | Mínimo | Cómo |
|---|---|---|
| Clip por beat | Enseña lo que dice la voz, del MISMO juego | `fuentes.json`, hojas `medios`; un clip de otro juego no se tolera ni 1 s |
| Lo que dice la voz se VE | Lugar, persona u objeto nombrado: imagen real en ese momento | Clip, `pant()` o pegatina; «se ve X» = X en pantalla (Torre Blanca, no un lago) |
| Fichas de interfaz | ≥ la mediana del canal (`chequeo`) | Translúcidas, con la interfaz del juego |
| MG | Desde el gancho y repartidos, sin huecos de minutos; nuevos para ESTE guion | Kit `mg_wow`/`mg_tes`/`mg_er`/`mg_gaming`; más si el guion lo permite |
| Mapas con ruta | ≥ mitad de los puestos en listas de misiones; siempre que se hable de dónde | § MAPAS REALES CON RUTA |
| Pegatinas | Cada nombre real; ≥ 1 de cada 3 en estilo no estándar | Abajo |
| Comentarios | ≥ 4 agradecimientos + 1-2 críticas con burla disfrazada | § COMENTARIOS, puntos 2b y 2c |
| Sonido del juego | OST oficial, `ambiente_por`, SFX del mismo juego | § Sonido original |
| Lo que la voz dice que SUENA se OYE | Cada «escucha…», música, voz o grito nombrado: su tramo audible con la voz callada | § Sonido original, «Si la voz nombra un sonido» |
| Campaña de suscripción (Runa, Tamriel) | 6-10 s hacia el 70-80 % | § CAMPAÑA DE SUSCRIPCIÓN |

**Medición de referencia** (`tes_secretos_40`, por minuto): fichas 1,7 · MG 1,4 · mapas 0,7 · pegatinas 3,1 · comentarios 0,5.

**Pegatinas variadas (`nucleo/peg_estilos.py`, temas `tes`, `wow`, `er`, `gaming`):** `silueta` = personaje SIN fondo a media pantalla con
la cara bien visible y el video corriendo detrás (colocar con `pos_silueta`); `reliquia` = objeto sobre círculo de runas; `banda` = tira
de cine con los ojos; `camafeo` = medallón para menciones rápidas; `legajo` = expediente; `abanico` = cartas al enumerar. Cambia también
tamaño, posición y giro de las normales, y diseña estilos nuevos: no debe sentirse que todas son iguales. Para silueta usa un fotograma
nítido ≥ 1000 px; si rembg arrastra a otro personaje, recorta antes. Código de ejemplo: `videos/tes_secretos_40/efectos.py`.

**Antes de renderizar:** `python fab.py <v> chequeo` (también corre solo antes de `video`; nunca bloquea). Da la densidad contra la
mediana del canal, lo que la voz nombra sin apoyo (`previews/chequeo_narracion.md`) y los clips de otro juego. Es una pista de texto: lo
que marca se mira a mano.

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
  **FONDO DE MARCA SIEMPRE (Alice 29-oct; el usuario 1-nov-2026: «es algo que quieren siempre»):** en TODO video con
  Overgear, `medios/_overgear/background/Background.mp4` (degradado morado con partículas) a cuadro entero, en bucle, DEBAJO
  de reseñas, packshot y código: FX `video` `nombre="og fondo marca"`, `de=` la frase de las reseñas, `a=` el mismo final que
  «og CODIGO», puesto ANTES que los demás «og …» en la lista. Las tarjetas de coaching y de los pros siguen sobre gameplay;
  nunca gameplay detrás del logo, reseñas, packshot ni código. Ejemplo: `videos/wow_primera_semana/efectos.py`.
  **Además:** «incluye promoción pagada» marcado (lo hace `yt subir`/`aplicar`) y en la descripción el enlace por
  integración que mande Alice (`overgear.s.gy/CRONICAS/N`), no el general.
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
  Lo de abajo sobre Lyria queda para videos viejos. Riesgo: Content ID del OST (reclamo de monetización): anotarlo si llega. **Reclamos vistos:** Viva Piñata «Oven-Fresh Day» (TEOSTO_TONO_STEF_CS, `rare_auge_caida`, 28-oct): no usar la OST de Viva Piñata. Si llega un reclamo antes de publicar: cambiar la pista en `armar_musica_ost.py` → `mezcla` → `final` (solo audio, la imagen se copia) → resubir al mismo hueco y borrar el viejo.
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
  - **Render cortado a mitad (27-oct-2026, `wow_100_curiosidades_tbc_wotlk`, E: USB desconectado al 56 %)**: el `video_sin_audio.mp4`
    a medias SÍ se lee (ffmpeg cierra el archivo al morir el pipe). No empezar de cero: (1) keyframe cercano al final del parcial
    (`ffprobe -skip_frame nokey -show_entries frame=pts_time -read_intervals 1650%1723`), (2) `video --tramo <kf+0,001>-<total>`,
    (3) parcial recortado POR CUADROS (`-map 0:v -frames:v <kf×30> -c copy`; con `-t` salen 2 cuadros de más por los B-frames y la
    imagen se desfasa del audio) + concat demuxer `-c copy`, (4) comprobar nb_read_packets = round(total×30) y PSNR de la unión
    contra el parcial (inf antes del corte, ~50 dB después), (5) `final`. Y antes de un render largo, `medios/` en C: (un clip ilegible
    en E: lo tumba; leyendo de C: el render fue ~3× más rápido: 23 min en 19 min).
- **Lecciones de `tes_cosas_nunca` (27-oct-2026, «Las 20 cosas que NUNCA…», 19:13, todo en una sesión):**
  - **Siglas en la voz**: Chatterbox lee «PNJ» como «puenche/pungo» (4 frases fallidas): escribir «personajes» en el guion (o
    FONETICA) y en el ancla de efectos. Nombres que Whisper escribe distinto (Boethiah→boecia, Sanguine→Sangin, Aranea→Arania):
    `CER_MAX_POR_FRASE` tras leer la transcripción; frases largas con CER 0 que acaban hablando: `TAIL_MAX_POR_FRASE` 0,55.
  - **4 MG nuevos en `mg_tes`**: `plazo` (barra de horas con avisos y curas: Lydia 72 h, Sanguinare Vampiris), `paciencia` (golpes
    que perdona hasta «hostil»), `escalado` (tu nivel contra el mundo, hitos de dragones), `reinicio` (cofre que se vacía, casa
    segura). Un MG de lista que tape > 30 s el gameplay es demasiado: cortarlo por la frase clave (escalado 42 s → 28 s).
  - **Clips**: 45 de 132 rehechos. Nuevos tipos a cazar en la hoja: animación/cartoon de fans («Skyrim chicken», «Skyrim Schmyrim»),
    gente real (sketch «Lydia carrying», forja real «Make N' Create», maquetas «Book Nook»), otro juego (Uncharted 4 con «jail
    cell»), pantallas de carga INVENTADAS por fans («Sarcastic Loading Screens»), collages blancos, temporizador de speedrun y
    clips más cortos que el beat (5,9 s para 9,3 s: cuadro negro en la hoja). `bajar N --rehacer --q "…"` dirigido los arregla.
  - **Sonido original**: 4 de 15 beats con `ambiente_por` traían narrador/streamer (`_sonido_original.py habla`): quitarlos antes
    de `armar_musica_ost.py` + `ambiente`. El de Uthgerd («Who taught you to fight…») es diálogo del juego: se queda.
  - **Programar**: `ciclo_dias` 3 (panel) y `separacion_min_horas` 96 chocan; `canales` dio el lun 02-11 pero `yt subir` lo
    detiene (72 h tras armas): se programó en el primer hueco con 96 h (mar 03-11 12:08 CDMX), sin `--forzar`.
- **Lecciones de `tes_misiones_imperdibles` (28/29-oct-2026, «Las 25 misiones que NUNCA debes saltarte», 22:55 de voz, 160 beats):**
  - **Investigación con 3 subagentes en paralelo** (8-9 misiones cada uno, fichas UESP + nombres es-ES + búsquedas de YouTube): 25
    misiones verificadas en ~30 min sin gastar contexto. Pedirles que avisen de lo que no casa (dieron con 2 errores del brief:
    «The Lost Expedition» es en Nchuand-Zel, no Alftand; Ildari es de «Old Friends», no de «The Gardener of Men»).
  - **3 MG nuevos en `mg_tes`**: `inversion` (pilas de monedas pago a pago + «INVERTIDO» + carta-sello + el que despierta en rojo:
    Ralis/Ahzidal), `versiones` (dos testimonios con «PRUEBAS: 0» y sello «SIN PRUEBAS»: Saadia/alik'r) y `fragmentos` (objeto que
    se parte entre sus portadores, vuelve y los tacha: Gauldur, en 2 apariciones alrededor del mapa). `_icono` TUMBA los objetos
    largos (un amuleto salía como astilla): para joyas, `_libre` (contorno sin giro). El sello no va sobre un retrato: abajo al centro.
  - **Clips: ~100 de 160 rehechos en 5 vueltas** (el peor ratio hasta ahora: misiones con nombre propio = guías con menús). Nuevos
    sucios: subtítulos en ruso, rótulo «MODDED», créditos de Patreon, «Added Actors» de un mod, cara de cartoon encima, «Tiny Tower
    - Playerhome», mods con ropa mínima. La hoja de 2 cuadros (1 s y 6 s) NO ve el final de los beats largos: `fx hoja` cazó 6 más
    con menú o negro a mitad. Lo que salvó la última vuelta: `{url, desde}` de un video ya limpio del mismo video (otro segundo).
  - **`ambiente_por` + `+ba` = clips cortos** (11 de 18 beats con sonido salieron de 1,2-8 s para beats de 7-11 s): rebajarlos SIN
    audio con la misma url/desde y dejar el sonido solo donde bajó entero (4 beats). `_chequeo_clips.py` (ffprobe: clip < beat)
    los caza en 1 s; `_hoja_clips.py` necesita `-pix_fmt yuvj420p -strict -1` para los clips con audio (si no, cuadro negro falso).
  - **C: se llenó a mitad de `bajar`** (otra sesión; 12 GB → 0,06): 4 clips truncados e ilegibles. Con E: sin errores en 12 h, se
    pasaron medios/audio/voz/previews/salida/segmentos/sfx a E: con junctions (`Move-Item` + `New-Item -ItemType Junction`).
  - Miniatura Flow a la primera (Sheogorath + Wabbajack + queso sobre la composición de la ganadora): `prompt_miniatura.md`.
  - **`final` BORRA `salida/video_sin_audio.mp4`** (y este motor no deja `segmentos/`): si el blackdetect del MASTER pide arreglos,
    no hay sobre qué empalmar. **Corre `final` SIEMPRE con `FAB_CONSERVAR=1`** y empalma los tramos sobre `video_sin_audio.mp4`
    (luego `final` otra vez). NO uses `videos/tes_misiones_imperdibles/_empalme.py` sobre el MASTER: el trim por cuadros SE COMIÓ
    LA IMAGEN DE LA PANTALLA FINAL (la imagen acabó en 1374,6 s y solo quedó su audio; el usuario lo vio, 29-oct) — comprueba
    siempre con ffprobe que la duración del stream de VIDEO del MASTER incluya la pantalla final. Aquí: 3 negros de 1-2,3 s al final/inicio de clips
    (013, 018, 065) que ni la hoja de clips ni `fx hoja` vieron; rehechos con la misma url y `desde` + 40 s.

- **Lecciones de `tes_secretos_40` (30-oct-2026, «Los 40 SECRETOS», 17:22 de voz, 121 beats):**
  - **Ritmo real de `Sarcastica`: 2,6-2,7 palabras/s.** 18 min ≈ 2 700 palabras; 40 puestos ≈ 60 palabras cada uno. El primer guion salió de 3 483 (21:40): contar palabras ANTES de la voz.
  - La voz fue mucho más rápida de lo calculado (292 tomas en ~45 min con la GPU libre).
  - **4 MG nuevos en `mg_tes`**: `nombre` (un nombre que se parte y confiesa su significado), `cordura` (diario que se desquicia, barra sin cifras y sello), `informe` (expediente con barras negras que se retiran en cada marca, sello) y `aguante` (barra al mínimo, ataques y cuenta atrás).
  - **Anclas: «Número treinta» casa con «Número treinta y ocho»**: el aviso del 30 salió en el 38. Usa un trozo que no sea prefijo de otro número.
  - **Clips: 44 + 11 + 5 + 3 rehechos.** Lo que cerró las últimas vueltas fue `{url, desde}` de un longplay limpio (Loopy Longplays `JV3tKszygTU`); aun así caen menús de forja, inventario y libros: mirar el rehecho. `fx hoja` se genera antes de los últimos rehechos: esos no salen en ella.
  - **YouTube limita la descripción a 5 000 BYTES**: 4 962 caracteres con acentos dan `invalidDescription`. Quédate en ~4 600.
  - **Banco de SFX reales en `nucleo/datos/sfx_juego/skyrim/`** (`_bajar.py`: misión, subir de nivel, lugar descubierto, monedas), en ~16 momentos clave y no en cada puesto, para no repetir.
  - **Flow pide aceptar «Rights to use this image» al pegar ingredientes en un proyecto nuevo: se acepta SIEMPRE con «I agree», sin preguntar (el usuario, 31-oct-2026: «siempre acepta eso de flow»; autorización permanente para todos los canales).** Solo cubre ese aviso: cualquier otra condición, política, cuenta o permiso nuevo de Flow se le sigue preguntando al usuario.
  - Disco: con E: dañado, `nuevo` igual crea junctions a E:; quitarlas al crear el video (`rmdir` y carpeta real en C:).

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
- Referencias del NIVEL esperado (para inspirarse, no para copiar): Runa `mg_er.doble_vida/gemelos/hilos/cosido/cruces/triada`; Warcraft `mg_wow.filas/grupos/contadores` y (21-oct, `wow_curiosidades_kalimdor`) `runas` (cadena de suministro: 7 runas que se apagan con el agua de Azshara), `linaje` (pareja -> hijos que tachan al padre, con retratos reales en medallón), `cadena` (causa -> efecto en medallones que se tiñen de rojo) y `consola` (terminal titán que teclea «FALTAN» y estampa sellos); (24-oct, `wow_100_curiosidades_tbc_wotlk`) `paradero` (¿dónde está cada uno?: medallones en fila con su lugar; los que faltan, grises con «?» y sello rojo), `simon` (el juego de 4 luces de Ogri'la: secuencias que crecen en bucle y el fallo con rayos) y `franquicia` (un personaje con «sucursales»: letreros de neón que prenden parpadeando y contador); (27-oct, `wow_jugadores_rompieron`) `reckoning` (un talento sin tope: contador de cargas que sube, el jefe con su barra de vida, lluvia de íconos que lo revienta y el parche que desploma el contador a 4), `inmortal` (jefe que se cura con cada muerte: la barra baja a golpes y cada calavera la rellena en verde; sello «INMORTAL» y un MJ que se lo lleva) y `expediente` (un caso judicial que se escribe año a año con golpe de mazo y veredicto en sello rojo); (28-oct, `wow_primera_semana`) `calendario` (días del mes con HOY que late, día clave con aro y franjas que se extienden), `experiencia` (dos barras de experiencia: sin nada / con bonos que la aceleran), `reglas` (tipos de servidor como puertas: se elige una, sello y facción tachada), `nombre` (campo de nombre y apellido que se teclea y sale ✔/✖ con motivo), `relojes` (la misma hora en varias ciudades, agujas que giran), `capas` (dos planos de capa, tu personaje cruza la frontera y el bicho desaparece), `botin` (un azul de mazmorra cuya apariencia vuela a los 5 del grupo) y `mudanza` (un formato que sale del canal hacia un canal nuevo en silueta, sello PRONTO); (1-nov, `wow_objetos_secretos_forever`) `ocultos` (bolsa con casillas tapadas que se destapan), `chat` (ventana de chat con comando tecleado), `duplica` (efecto según el sitio), `conjunto` (dos piezas unidas, bonos y totales), `reloj_oro` (barra que corre desconectado y oro), `subasta` (tabla de lotes con pujas), `pizarra` (frase en tiza traducida palabra a palabra), `censurado` (tooltip borrado y pistas alrededor) y `tiempos` (línea de tiempo por tramos); Tamriel
  `mg_tes.rejilla/traiciones/reloj/contadores/rehenes/sospechosos/cadena/balanza`.

## METRAJE DE ARCHIVO < 720p (27-oct-2026, `wow_jugadores_rompieron`)
Los videos originales de 2005-2006 (Kazzak en Ventormenta 240p, el gong de Medivh 480p, la exploración de Hyjal 256p, el récord de
Joana 360p, la «Reckoning Bomb» 480p) son lo más valioso de un video de jugadores REALES, pero `bajar` los rechaza («Requested
format is not available»: pide ≥ 720p). Receta: bajarlos enteros (`yt-dlp -f "bv*+ba/b"` a `medios/_archivo/<n>_raw.mp4`), hoja de
contacto 4x4 con la hora (ffmpeg `fps=16/dur,drawtext,tile`) para elegir tramos, y armar `medios/scene-NNN.mp4` a mano como VENTANA
DE ARCHIVO: el mismo clip escalado a 860 px de alto con marco dorado (`pad … color=0xC9A227`) sobre él mismo desenfocado y oscurecido
a cuadro entero. Se registran en `fuentes.json` (crédito) y en `busquedas.json` con `"_archivo"` para no pasarles `--rehacer`.
Un tramo puede salir negro (Kazzak a 203 s): mirar el clip armado. En la descripción, línea «METRAJE DE ARCHIVO» con sus canales.
- Animaciones de fans sobre audio real (Onyxia Wipe): revisar TODOS sus cuadros; la «YouTube Approved Edition» trae fotos ajenas
  (una sugerente, un faquir) y el audio original tiene tacos justo después del grito: cortar el beat antes (`ambiente_por`).
- Guion de jugadores: los nombres que Whisper escribe distinto (Kazzak → «Kazakh», Joana → «Johanna», Ahn'Qiraj → «Anquiraj») se
  aceptan con `CER_MAX_POR_FRASE` tras oírlos; «WoW» va en FONETICA como «uórld of uárcraft».

## MAPAS REALES CON RUTA (el usuario, 23-oct-2026: Warcraft, Runa Caída, Tamriel y Crónicas del gaming)
El usuario: «en ocasiones hay que mostrar mapas reales del juego con rutas cuando hablemos de misiones o cosas que el espectador
quiera saber dónde es; tú decides en qué escenas y cómo… adaptados cada uno a su juego». Kit **`nucleo/mg_mapa.py`** (`mapa()`),
helper `mapa()` en `videos/_plantilla_yt/efectos.py` (en videos viejos, copiarlo de ahí con `_MAP` y `TEMA_MAPA`).
- **MÁS MAPAS (el usuario, 29-oct-2026, al ver `tes_misiones_imperdibles` con solo 2): «siempre que se pueda y el guion lo
  permita, usar mapas con rutas»; en listas de misiones, AL MENOS LA MITAD de los puestos con mapa de dónde inicia y sus
  objetivos, con la ruta.** Sustituye al «1-4 por video» de abajo: el mapa va en todo puesto que tenga geografía (dónde empieza,
  adónde te manda, dónde está el jefe o el premio), aunque la voz solo nombre uno de los lugares (los demás van rotulados). Uno de
  cada puesto, 6-12 s, en la frase que cuenta el viaje; quita la pegatina de lo que ya sale como foto en un punto del mapa.
  **Coordenadas REALES**: base de datos del mapa de UESP (`gamemap.uesp.net/sr/db/gamemap.php?action=search&db=sr&search=<lugar>`,
  `worldId` 1 = Skyrim, 2 = Solstheim) calibrada con las ciudades del mapa de papel por mínimos cuadrados:
  `videos/tes_misiones_imperdibles/_coords_uesp.py` (error ≈ 3 % del mapa; los lugares de un DLC llevan sufijo: «Darkfall Cave (DG)»,
  «Last Vigil (DB)»). Revisión: `_prueba_mapas.py` (último cuadro de cada mapa en un mosaico). Primer uso: 15 de 25 misiones.
- **Cuándo (lo decide el agente al leer el guion, en el mismo plan que los MG nuevos; antes 1-4 por video, ver la regla de arriba):**
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
- **Mapas de continente de Wowhead (24-oct-2026)**: `.../maps/eses/original/-2.jpg` = Terrallende, `-5` = Rasganorte, `-4` = el cosmos
  (Azeroth/Draenor), `-7` = Pandaria. Los ids `3` y `4` son ZONAS (Tierras Inhóspitas y Las Tierras Devastadas): MIRAR cada mapa
  bajado antes de usarlo. **Video con 100 paradas** (`wow_100_curiosidades_tbc_wotlk`): un mapa general a pantalla en la intro
  (solo inicio y meta con nombre: el mapa ya pinta las zonas; con 8 rótulos se amontonaban) y una VENTANA de 4-6 s por parada
  (helper `parada()` en su efectos.py: zona + «N.º n» + foto), con ruta corta cuando la voz va de un sitio a otro. Coordenadas
  dudosas: `{{coords|x|y|zona}}` en el wikitexto de Wowpedia (`prop=revisions`) del PNJ. Un recorrido largo con solo inicio
  y meta necesita `traza=99` (si no, cada tramo se dibuja en 1,7 s y la ruta sale de golpe al final).
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
- **Video 3 `majora_mask` (23-oct-2026): FICHAS TRANSLÚCIDAS con la interfaz del propio juego (cumple la regla del 22-oct) —
  kit `nucleo/mg_majora.py`**: `ficha` = el cuadro de diálogo de N64 (negro translúcido con borde difuso, texto que se escribe
  letra a letra, *resaltado* rosa como los nombres, triángulo verde de «siguiente»); `puesto` = el cartel «Amanecer del primer
  día» (serifa blanca con tracking + «-título-»); `reloj` (el reloj de 3 días del HUD con sol/luna y «Quedan N horas»), `ciclo`
  (bucle Día 1 → … → Canción del Tiempo), `horario` (cuaderno de los Bombers), `rejilla` (las 24 máscaras con sus íconos reales →
  la especial), `almas` (retrato real que se funde en su máscara), `pegatina` con píldora translúcida. Para otro juego: misma
  receta, la interfaz de ESE juego (su caja de diálogo, su cartel de zona, su HUD). Tema de mapa nuevo `"majora"` en mg_mapa.
  - **Música OST** (regla del 23-oct): `armar_musica_ost.py` con las secciones por id de escena (lee los t0 de timeline.json);
    para Nintendo no hay canales «- Topic»: lista «Complete Soundtrack» de Nintendo Music Archive (audio original de N64).
  - Plan de clips por un AGENTE que mira las hojas propias (`escanear.py` = 360p + hoja cada 15 s con el segundo impreso) y
    escribe busquedas.json directamente: 107/107 a la primera (1 rehecho por ser una pantalla quieta). ZeldaCentral mete su
    animación del canal también A MITAD de algunas partes, y tras cada Canción del Tiempo hay ~20 s de espiral/blanco/negro.
  - Pegatinas: `bajar_pegatinas.py` (API imageinfo de zelda.fandom.com por nombre de archivo `MM_<X>_Artwork.png`); los íconos
    de máscara son de 32 px: para pegatinas usar `MM3D_<X>_Model/Render.png`, los íconos solo en la rejilla (NEAREST).
  - Miniatura Flow por Chrome: bajar con el menú «Más opciones → Descargar → 1K» (va a Descargas sin diálogo); el fetch a
    localhost desde Flow lo bloquea la CSP y el canvas queda «tainted».
- **`bt_jiggies_crueles` (23-oct-2026, 80 beats, 11:30): PRIMER kit TRANSLÚCIDO del canal, `nucleo/mg_banjo.py`** (la regla del
  22-oct aplicada): humo chocolate de bordes difuminados (no caja), filetes miel que se desvanecen con un panal al centro, Cooper
  Black miel con contorno + Arial Rounded crema. `puesto(num, titulo, jiggy)` = el Jiggy REAL de la wiki girando sobre su eje
  (ancho = |cos|) con el número; `crueldad(n)` = medidor en panales como la barra de vida del juego (sale al irse el puesto, arriba
  a la derecha); `ficha` translúcida. MG del guion: `marcador` (puntos con dos metas: página de Cheato / Jiggy + reloj),
  `contrarreloj` (n objetivos que caen con reloj; remate BOOM o gas tóxico; `hasta` < 1 = no te da tiempo), `carrera` (Canary
  Mary: acelera si te pegas, acelerón final, el truco), `recados` (problema → solución, ✓, premio y sello «NO»), `cadena`.
  Probar cada MG con marcas SIMULADAS en varios instantes (script propio sobre un cuadro de gameplay) antes de `fx hoja`: así
  salieron las etiquetas de metas encimadas (40/50 de 60) y los tamaños chicos (dinamita, carrera, cadena) sin gastar un render.
  - **Ninbanyan con widescreen (NSO, «Widescreen» en la Parte 1)**: sin marco gris → `recorte_por` vacío; las cinemáticas traen
    una franja negra arriba fina, aceptable. Los cuadros de la serie (360p, un cuadro cada 4-15 s) dieron el segundo exacto de los
    80 beats a la primera (`plan_clips.py` por BEAT, no por frase); solo 3 rehechos (2 con negro de túnel/fundido, 1 de lona).
  - **Brillo de TODOS los clips antes del render** (media < 14 cada 0,3 s): cazó el túnel del tren (P26 @150) y el fundido de la
    pantalla de totales (P26 @280).
  - **Música**: no hay álbum oficial de Banjo-Tooie en «Grant Kirkhope - Topic» (solo Re-Jiggyed de BK); se usó el ripeo del
    juego de «Video-Game OST HQ» (`armar_musica_ost.py`, una pista por puesto: «Racin' With Mary», «Ordinance Storage», «Vs. Mr. Patch»…).
  - **Sin mapa**: el único mapa real de Isle o' Hags es el pergamino del manual, sin nombres; no se ubican los sitios con certeza
    → `recados` con fotos reales en vez de un mapa con posiciones inventadas (regla: sin mapa real decente, no hay mapa).
  - **Miniatura**: la wiki de Banjo (static.wikia.nocookie.net) tiene CORS abierto → collage de los renders en un `<canvas>`
    dentro de la página de Flow y pegado sintético como ingrediente; salió bien a la primera (`prompt_miniatura.md`).
  - Voz Hope: Whisper escribe «Zubas/uvas», «Umba Umba», «Cheeto», «Scrooge» → tolerancias; la única mala real fue «Dentro, Banjo»
    leído «Ventro» (dos palabras que empiezan igual): reescribir la frase, no repetir la semilla.


### Lecciones de `mario64_secretos` (30-oct-2026)
- **Kit `nucleo/mg_mario64.py`:** diálogo translúcido, rótulo de selección de estrella, HUD y 7 MG (mando, reloj_ttc, agua, boton_a, bit, estrellas, linea_tiempo) + tema de mapa `mario64`. Mapas de VGMaps (2-3 k px con rótulos); los del DS en la wiki son de 128-255 px.
- **`medir_brillo.py` sobre el clip REAL, no sobre una copia:** `bajar` no fuerza keyframes, así que el tramo real empieza en otro punto que una bajada de 360p del mismo segundo (dos clips «limpios» en 360p salieron con negro de 0,3-1,5 s). Bucle que funciona: corregir `desde` → `bajar <id> --rehacer` → medir → repetir. De 20 marcados, 5 eran oscuros a propósito: mirar el cuadro exacto antes de rehacer.
- **Rótulos de secreto y ficha:** comprobar en `fx hoja` que no caen sobre un diálogo del juego (el rótulo arriba chocó con el de Bowser en el 081): se corrige moviendo el clip, no el rótulo.
- **Antes de cambiar la `url` de un beat, mirar `plan_clips.py`:** un longplay de 4,5 h tiene varias fuentes casi iguales; al rehacer con otra `url` el segundo apunta fuera del video y `bajar` dice `ok` sin dejar archivo (el aviso real es `148/149 clips`).
- **Render en segundo plano y PC suspendida:** el proceso sobrevive y sigue al despertar; el salto en los segundos del log no es un error.

### Lecciones de `bt_mundos_ranking` (30-oct-2026, 170 beats, 24:22, el más largo del canal)
- **`bajar` TRUNCA los clips con audio** (`ambiente_por` > 0): 29 de 36 salieron 2-8 s cortos y `medir_brillo` los vio como negro. Script del video `dl_amb.py` (baja video y audio por separado con corte exacto). Sin arreglar en `secuencia_yt._bajar_tramo`; si un clip con ambiente se rehace con `bajar --rehacer`, vuelve a truncarse. Comprobar DURACIÓN además de brillo.
- **Mapas de gaming = guías oficiales escaneadas de archive.org** (PDF 600 DPI + pymupdf `get_pixmap(dpi=300)`): 9 mapas con rótulos originales, mucho mejores que el manual. Traen flechas y páginas de la guía: se ven como «mapa de la guía oficial», con ese subtítulo. Los pergaminos de manual NO traen nombres: nada de ubicar mundos ahí; las conexiones del cierre van en `mg_banjo.conexiones`.
- **Kit `mg_banjo` ampliado:** `egg` (contador de Easter eggs en la esquina: da ritmo en un video largo; con mapa a pantalla bajarlo a y=.27 o choca con el título), `cuatro_listas`, `ruleta`, `codigos`, `conexiones`, `ficha_mundo`.
- **Verificar en imagen ANTES de grabar** (agente con hojas, tabla de datos con el texto exacto leído): salvó 4 datos falsos (rocas fálicas, letrero de trituradoras, Jiggy partido, «a Rare date») y mejoró varios («A BEAR STOLE ME GLORY…», errata «SLIGHTY»). Lo que solo se ve en otra versión se dice en voz y lleva rótulo (`xbox()`).
- **Whisper y nombres ingleses:** 41 de 130 frases rechazadas, todas falsas alarmas (Mr Doctor Boy, Cheeto, Hellfire). Comparar `textos.json` con `eval.json` por diferencias de palabras y fijar `CER_MAX_POR_FRASE` con la CER + .0015; `TAIL_MAX_POR_FRASE` para las que hablan hasta el final si la transcripción termina bien.
- **Plan de clips y corrección por AGENTE (sonnet):** ~260 mil tokens cada uno fuera del hilo principal; 170 beats a la primera y 17 clips arreglados.
- **Disco:** un video de 24 min no cabe en E: con 3 GB libres: cambiar `salida/` y `segmentos/` del video a carpetas reales en C: antes del render (quitar la junction con `cmd //c rmdir`).
- **Flow en el navegador integrado volvió a pedir bienvenida y política de privacidad el 30-oct** (dominio nuevo `flow.google.com`). Aceptarla es del usuario: no se acepta sola. Mientras tanto, miniatura provisional por código (`miniatura_provisional.py`).

### Lecciones de `spyro2` (31-oct-2026, 174 beats, 24:52, primer video de PS1 del canal)
- **Kit `nucleo/mg_spyro.py`** (cuadro de diálogo translúcido, gemas que giran, cifras doradas del HUD) con 22 MG; tema `spyro` en `mg_mapa` y en `peg_estilos`. `secreto()` = rótulo + contador `hud` de esquina «N/30» todo el secreto: da ritmo en 25 min y no cuenta como MG (nombre «aviso …»).
- **Capturas 1080p por URL directa** (`videos/spyro2/capturas.py`): `yt-dlp -g` + `ffmpeg -ss` da cualquier cuadro de un longplay sin bajarlo. El primer pedido a una URL recién firmada da 403: reintentar con 2 s de pausa. 33 capturas sirvieron para pegatinas, MG y personajes sin arte en la wiki (Brother Ned, Fisher, Murgen).
- **Solo existe un mapa real (la lámina de Avalar):** se reutiliza en ventana con la foto del nivel en cada mundo. Mapas de nivel no hay en ninguna fuente, así que no se inventan.
- **Cámara web de la única fuente de un dato** (prototipo, glitch): se tapa con una pegatina en esa esquina (`_tapa` en efectos.py) en vez de perder el dato. Mirar las hojas de los videos de fans antes: el agente no siempre lo descarta.
- **Copiar un script de otro video:** nunca dejar su ruta absoluta. `dl_amb.py` llevaba `AQ` fijo a bt_mundos_ranking y reescribió 33 clips de ese video; ya usa su propia carpeta. Además, en heredocs del Bash de esta PC `\\` se colapsa: para tocar rutas de Windows usar la herramienta Edit, no `sed` ni un heredoc. Comprobar con `grep` antes de lanzar.
- **`medios/` también es junction a E:** en videos nuevos, aunque no salga en `nuevo`; `du` da 0. Antes de un render largo mirar con `dir /AL` qué vive en cada disco.
- **Disco:** render de 24:52 = 1,1 GB + MASTER 1,2 GB + `salida/` y `segmentos/` en C:; bastan ~6 GB libres, no 12 como decía la cuenta vieja (47 min de render a 12 procesos).

### Lecciones de `n64_secretos` (31-oct-2026, 170 beats, 24:19, primer video de CONSOLA del canal)
- **Kit `nucleo/mg_n64.py`** (pizarra de grafito translúcida con la tira de cuatro colores, cubo del logo, Bahnschrift) con 18 MG propios; tema `n64` en `mg_mapa` (ruta plateada, cubos como marcadores) y en `peg_estilos`. Un tema nuevo de `mg_mapa` necesita entrar en la lista de `_etiqueta` (banda de humo) o pedirá `caja`/`filo` y fallará con `KeyError`.
- **Rutas de mapa a mano, nunca a ojo sobre la hoja:** las de Yoshi Valley salieron por encima de la roca. Receta: rejilla con coordenadas en fracción sobre el mapa entero y luego dos o tres zooms con rejilla fina de la zona; trazar el camino real (qué conecta con qué) y dibujar la polilínea sobre el mapa ANTES de `fx hoja`. Las listas de puntos van con nombre en `efectos.py` (`_VUELTA_LARGA`, `_ATAJO`, `_TRAMO_FINAL`, `_SALIDA`) para que dos rutas compartan tramos.
- **`bajar_pegatinas.py` con Wikipedia falla en accesorios y empresas absorbidas:** «Transfer Pak» y «Expansion Pak» redirigen a una página sin imagen y «DMA Design» a Rockstar North (sale el logo de Rockstar). Buscar en Commons (`list=search`, `srnamespace=6`) y en la wiki de fans (`gta.fandom.com` tenía el logo de DMA); los logos negros sobre alfa (CD, Digital Foundry) se ponen sobre blanco o desaparecen en el video. Mirar SIEMPRE la hoja de contacto de `pegatinas/`.
- **Clips con `ambiente_por`:** `bajar` los trunca; los 33 salieron cortos frente a su beat y se rehicieron todos con `dl_amb.py` (video y audio con el segundo exacto). Dos beats con el MISMO clip (011 y 082) delatan una descarga equivocada: compararlos en la hoja de brillo.
- **`ficha(a=("frase|fin", …))` puede resolverse a 0,03 s** si el ancla no se encuentra: en la lista de `fx` buscar FX de duración ~0 y pasarlos a `dur=`.
- **Un MG nuevo debe aguantar q≈0 y q≈1:** `mg_n64.calor` tiró la capa de `fx` al 70 % (barra con y1 < y0 al entrar). Antes de `fx`, llamar cada FX en sus instantes límite (inicio, inicio+1 cuadro, fin−1 cuadro, fin): 220 FX = 5 940 llamadas en segundos, frente a una hora de `fx` perdida.
- **`verificar` y cifras:** las frases con CER > 2 % eran todas cifras («300.000», «$199.99») o nombres en inglés escritos con `FONETICA` («Wide-Boy64» → «White Boy»). Antes de regrabar, oír la frase: si la voz está bien, no es error.

## SONIDO ORIGINAL del juego (el usuario, 26-oct-2026: Warcraft, Tamriel, Runa Caída y Crónicas del gaming)
«Cuando sea necesario mete sonidos de Zelda original y música… cuando salen partes donde conviene escuchar la música, o los gritos
de Link y SFX de Zelda; aplica esas reglas también en Tamriel, Warcraft o Runa Caída.» Primer uso: `videos/oot_remake_cambios/`.
- **SFX DEL MISMO JUEGO (el usuario, 29-oct-2026): «siempre que se pueda, SFX del mismo juego también».** Además del audio del
  clip, los efectos de sonido del video (aviso de misión, ficha, pegatina, mapa, sello, golpe de un MG) salen del JUEGO del que se
  habla, no de ElevenLabs ni sintetizados: los sonidos de interfaz y de mundo del juego (Skyrim: «Misión iniciada / completada»,
  subir de nivel, descubrir un lugar, gritos, abrir el diario, monedas; WoW: misión aceptada/completada, subir de nivel, botín;
  Elden Ring: gracia descubierta, objeto obtenido, «ENEMY FELLED»), bajados con yt-dlp de videos «<juego> sound effects / UI
  sounds» limpios (sin voz, se comprueba con Whisper) o recortados del audio de los propios clips, guardados en
  `nucleo/datos/sfx_juego/<juego>/` y catalogados en la biblioteca de SFX para reutilizarlos sin repetir el mismo en el canal.
  Solo si el juego no tiene ese sonido, ElevenLabs con `SFX_ELEVEN`.
- **Qué beats:** los que enseñan algo que SUENA y la voz lo nombra: la música del juego cuando se habla de ella, una canción que
  se toca (ocarina, laúd), gritos/voces del personaje, golpes y saltos, una maldición, el cartel de una zona. ~1 de cada 4 beats;
  el resto sigue mudo (dos músicas a la vez = ruido).
- **Cómo:** `SECUENCIA["ambiente_por"] = {"scene-050": .9, ...}` (0,5 ambiente, 0,8-0,9 cuando el sonido ES el punto) con
  `ambiente=0.0` general → `python fab.py <v> bajar 50,51 --rehacer` (con volumen > 0, `secuencia_yt._bajar_tramo` baja
  `bv+ba` y conserva el audio en AAC) → la OST se APARTA −14 dB en esos beats (`armar_musica_ost.py`, `APARTA_DB`, rampas de
  0,5 s) → `python fab.py <v> ambiente` (audio/ambiente.wav, nivelado) → `mezcla` lo pone bajo la voz con ducking de 5 dB.
- **Narrador encima** (demos de desarrolladores, tráileres «overview», guías): Whisper sobre cada clip con audio; si habla
  alguien, Demucs `--two-stems vocals` y el clip se queda con `no_vocals` (`videos/oot_remake_cambios/quitar_narrador.py`),
  y Whisper otra vez (debe salir «sin habla»). En oot_remake_cambios 10 de 21 clips traían la voz en inglés de la demo.
- **A un clip YA APROBADO no se le rebaja con `bajar --url --desde` (27-oct-2026, `wow_100_curiosidades_tbc_wotlk`):** con
  `+ba` yt-dlp corta el tramo en OTRO keyframe (video que empieza segundos después que el audio) y 11 de 12 clips salieron con
  otra imagen o de 1 cuadro. Para sumarle el sonido sin tocar la imagen: `_sonido_original.py alinear <carpeta de aprobados>`
  (baja el tramo con audio y margen, busca por imagen dónde empieza el aprobado y le pega el audio de ese instante; dif < 8 =
  mismo cuadro). Antes copia los aprobados de `medios/_respaldo` (el más nuevo de cada beat). Luego `creditos` (el `--url` deja
  «fijado a mano» en fuentes.json), `habla` (Whisper: 2 de 14 traían narrador → fuera) y `nivel` (−52 LUFS = mudo → fuera).
  Elegir por el TÍTULO del clip: «Music Video», «LIVE», «No Commentary», cinemáticas; las guías casi siempre llevan narrador.
- **Pausas para oírlo:** el guion solo admite `post` por ESCENA y añadirlo re-corta TODOS los beats (85 en vez de 84, otros
  límites): decidirlo ANTES de `beats`/plan de clips, nunca después.
- **SI LA VOZ NOMBRA UN SONIDO, EL ESPECTADOR LO OYE (el usuario, 31-oct-2026, TODOS los canales; visto en `spyro2` y antes):**
  «cuando el narrador hace referencia a un sonido o invita a escuchar, es imprescindible que pongas un tramo del sonido, música, lo
  que sea… no importa que el narrador se quede callado». Toda frase que hable de un sonido («escucha la diferencia», «cada nivel
  suena a…», «usan el mismo tema musical», «la voz de Ripto», «le grita…», «la música de las demos», una canción, un grito, un
  ruido) lleva ESE sonido audible en ese momento: no basta el clip con `ambiente_por` bajo la voz si la voz lo tapa.
  - **Cómo:** al escribir el guion se marca la frase y se le da su tramo **con la voz callada**: `post` de 2-6 s en esa escena (se
    decide ANTES de `beats`, ver arriba), con el audio del clip a 0,9-1,0 y la OST apartada; comparaciones («la versión americana /
    la europea») = los dos tramos seguidos, cada uno con su rótulo. Música de un nivel que se nombra = esa pista de la OST sube en
    ese beat (no la del puesto). Voz de un actor = una línea suya del juego. Si no existe audio real de ese sonido, se reescribe la
    frase para no prometerlo.
  - **Verbos para quien OYE el video:** «sí, oíste bien», nunca «sí, leíste bien» (el espectador escucha la narración; «lees» solo
    para un texto que de verdad está en pantalla y es el punto, como el cuadro de diálogo del monje en `spyro2`).
  - **Aviso automático (`nucleo/chequeo_yt.py`, `sonidos`):** corre solo antes de `voz` en TODO video (con el texto del guion:
    lista las frases para decidir `post` + `ambiente_por` y los «leíste») y dentro de `chequeo`/antes de `video` (con timeline:
    marca cada frase cuyo beat o el siguiente no llega a `ambiente_por` 0,8 o que no deja ≥ 1,5 s de voz callada). A mano:
    `python -m chequeo_yt sonidos` desde la carpeta del video. Es pista de texto: «escuchar una disculpa» (figurado) sale y se
    ignora. En `spyro2` marcó las 16 frases de su tramo 5. Antes de renderizar, se oye cada una en la mezcla.

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
- **`er_melina_atrocidades` (27-oct-2026, ~20 min, todo en UNA sesión por petición del usuario):** MG nuevos en `mg_er`:
  `acuerdo(da, pides, letra, remate)` (contrato de dos columnas «Ella te da / Tú la llevas»; vuelve en el n.º 1 con la letra
  pequeña que crece en rojo, los regalos se tiñen de carmín y cae el sello «Deber»), `ecos(lineas, firma, revela)` (las citas de
  Márika se escriben con el Círculo de Elden girando tenue; la firma «una desconocida» se tacha y sale «SU MADRE»),
  `arbol_arde(etapas)` (el Árbol Áureo dibujado por código: la llama llega al pie, trepa, la copa arde en brasas y llueve ceniza;
  primera versión con lenguas de fuego geométricas se veía de dibujo infantil: desenfoque 2,5 px antes del halo + brasas
  redondas) y `muerte_suelta(nombres, remate)` (la Runa de la Muerte presa en eslabones que saltan volando; ondas que tachan a
  todos los nombres). Fuentes de citas: el WIKITEXTO de eldenring.fandom.com (`api.php?action=parse&prop=wikitext`, p. ej.
  `Melina/dialogue` con el texto inglés y japonés completo) — Fextralife cierra la conexión a scripts; nombres oficiales en
  español con `eldenring.fandom.com/es/api.php` (Torrentera, Hoja de la invocación, doncella enyescada, Maliketh la Hoja Negra,
  Reino de las Sombras, Reina del Ojo Velado). `armar_musica_ost.py` de este video corta por escena leyendo `timeline.json`
  (no a mano) y `asignar_clips.py` pasa un plan POR FRASE (`plan_frases.json`) a `busquedas.json` por beat.
  `flow_thumb.py` en PowerShell 5.1: el prompt con comillas dobles se rompe al pasar a python → `--file` con RUTAS ABSOLUTAS
  (las relativas las resuelve contra C:\googleimagenes).
  Revisión: 12 de 141 clips rehechos (9 %) con el plan por frase de un subagente que miró hojas a 0/3/6/9/12 s. Lo que cazó mi
  mosaico de 3 cuadros por clip: menú de subir de nivel y menú «Hablar» al final del tramo, un destello BLANCO de 2 s, y el
  personaje del jugador CASI DESNUDO en los videos de diálogos de TheFinalEpic (d2FRpV9KrkY ~1213-1238, Maiko pecrcqqbrNE @42):
  revisar siempre al jugador en tomas de diálogo. **MG grande y casi opaco + clip quieto = 8 s congelados** en freezedetect
  (MASTER 1): `CAMARA` sobre ese beat NO movió el clip (el HUD salió en el mismo sitio); se arregló cambiando el clip por uno con
  movimiento (Torrentera galopando). Voz: «DLC» → «dieque» (escribir «la expansión») y un nombre a final de frase se come la
  cola («matar a Maliketh.» → «Malik»; arreglado con «…a Maliketh, su guardián.»).
- **`er_radahn_atrocidades` (28/29-oct-2026, 24:38, 170 beats, todo en UNA sesión, tema pedido en los comentarios):** MG nuevos en
  `mg_er`: `lanzas(bando, centro, tu)` (las lanzas del enemigo se clavan en el león rojo y salen como flechas de gravedad contra
  «Tú»), `cielo_sujeto(atados, quien, remate)` (cielo quieto con destinos atados a `quien` por hilos violetas; la última marca los
  rompe, el cielo gira y cae una estrella), `balanza(izq, der, pesos, remate)` (las dos posturas de un debate: cada prueba cae en su
  platillo y la balanza se inclina; al final vuelve al centro con «Nunca lo dice») y `espejo(padre, hijo, papel_padre, papel_hijo,
  idolo)` (padre e hijo acaban en el mismo papel; el ídolo de infancia se tacha). **FONÉTICA (queja de los comentarios): «Mikuéla»
  SUENA «Mi-cue-la» = «Micuela», la burla de la gente → «Mikéla» (Whisper: «Miquela»). Mohg «Móg»: ante consonante sale «mock/mok»
  («Mohg secuestró») → reescribir para que vaya ante vocal («Fue Mohg el que…», «a Mohg, y…»).** Comentarios en pantalla: tarjeta
  `com_<id>` con `peg(…, tam=700-760)` en el gancho, cuando la voz cita a quien pidió o corrigió, y 5 de agradecimiento en el cierre.
  Revisión: 30 de 170 clips rehechos (18 %). Lo que cazaron las hojas: las recopilaciones de diálogos de **Stratek** (Jerren, Iji,
  Sellen, Freyja, Ansbach) son el MISMO plano estático y oscuro en cada capítulo → 4-5 seguidos parecen congelados (máx. 1-2 por
  puesto, el resto pelea/cinemática); el «Summon this companion?» de una partida con HUD; Seluvis en un video de la misión de
  Ranni; un fundido a negro al EMPEZAR un clip vuelto a bajar con audio (`ambiente_por`): **medir el brillo después de CADA
  `--rehacer`**, no solo antes del render. Anclas: `efectos.py` sale de un `orden.py` que avisa si un ancla cae > 40 palabras ANTES
  que la anterior («Su hermana» enganchaba «Ranni es su hermana» del puesto anterior). `seleccionar` guarda en `voz/eval.json` las
  tomas que apartas a `_descartes/`: podarlo (solo las que existen en `cands/`) o truena con `FileNotFoundError`. Cambiar UNA toma
  tras el render sin rehacer tiempos: rellenar la toma nueva con silencio hasta la duración exacta de la vieja → `mezcla` → `final`.
  `video --rehacer` con 4 tramos volvió a renderizar TODO (32 min). Créditos: `yt-dlp --print "%(channel)s"` por id de `fuentes.json`.
- **NUNCA `bajar` dentro de `while read … <<EOF`**: los procesos hijos se comen el stdin y la siguiente vuelta lee basura como id;
  `bajar --q` sin ids rehízo los 51 beats (se recuperó todo de `medios/_respaldo/`). Desde el 14-oct el motor se niega a `--q`/`--url`
  sin ids; en bucles, `< /dev/null`.

## COMENTARIOS de la gente (el usuario, 27-oct-2026: Warcraft, Tamriel, Runa Caída y Crónicas del gaming)
Que el público se sienta tomado en cuenta. Tres momentos:
1. **ANTES DE CADA VIDEO (el usuario, 28-oct-2026), al proponer tema:** `python fab.py yt comentarios <canal> [dias]` →
   `canales/comentarios/<alias>.json` (fuera de git; recuerda qué ya se vio) y en pantalla tres listas por ♥:
   - **NUEVOS** desde la última lectura: léelos todos.
   - **QUEJAS** (voz/IA, errores de dato, pronunciación, «redondeas», duración, sin sonido…): lo que se repite o tiene ♥ se
     corrige en ESTE video (nombre bien pronunciado en `FONETICA`, dato verificado, ritmo, mezcla) y se anota como lección en
     `canales/formula/<alias>.md`. Quejas de la voz IA o del formato: se le reportan al usuario con cifras (cuántas, ♥), no se
     cambia de voz ni de motor sin preguntar.
   - **SUGERENCIAS** (temas, partes 2, «te faltó X»): las de muchos ♥ o repetidas son candidatas fuertes a tema; van a
     `docs/ideas_guardadas.md` con su @usuario y el id del comentario (para enseñarlo después, punto 2).
   Las pistas de QUEJA/SUGERENCIA (`QUEJA`, `SUGERENCIA` en `nucleo/comentarios.py`) solo ordenan la lectura: la conclusión sale de
   leerlos. Deja una línea «Comentarios: …» (quejas atendidas, sugerencia elegida) en el `ESTADO.md` del video.
2. **En el guion:** si el video nace de un comentario o corrige un error que alguien señaló, la voz lo dice («@silentsword nos
   pidió el corcel de Xoroth…») y en pantalla sale el comentario REAL: `python fab.py yt comentario <v> <canal> <id>` dibuja la
   tarjeta (modo oscuro de YouTube: avatar, @usuario, «hace N días», texto, 👍) en `videos/<v>/pegatinas/com_<id>.png`, y en
   `efectos.py`: `peg(en, "com_<id>", "", tam=760, x=.30, y=.30)`, 3-5 s. 1-3 por video, en el gancho o al abrir el puesto que pidió.
   Nunca inventar ni retocar el texto (solo cortar con «…», máx. 5 líneas); nada de datos personales más allá del @usuario y
   su avatar públicos. Lo único que se contesta con guasa son las críticas del punto 2c, con sus límites.
2b. **Comentarios de AGRADECIMIENTO (el usuario, 28-oct-2026; los 4 canales):** cuando el guion lo permita, enseñar capturas
   de los MEJORES comentarios que agradecen y valoran el trabajo del canal: **al menos 4 por video, repartidos** (en pausas
   naturales: antes de un puesto, tras el patrocinio, en el cierre), con la misma tarjeta `yt comentario` → `com_<id>`. Si un
   video tiene muchos buenos, juntar VARIOS en una sola escena (3-5 tarjetas escalonadas) y la voz agradece a todos. La voz
   recuerda que **todos los comentarios se leen y se toman en cuenta para seguir mejorando**. Elegir por ♥ y por lo concreto
   del elogio (no «buen video» a secas); no repetir el mismo comentario en dos videos del canal.
2c. **Comentarios que CRITICAN: contestar a su nivel, con burla disfrazada (el usuario, 30-oct-2026; los 4 canales):** además de
   los de agradecimiento, «uno que otro» crítico: **1 por video, 2 como mucho**, y no en todos si no hay uno bueno. La meta es que
   quien lo vea se ría y **se sienta de nuestro equipo**.
   - **Tono:** por fuera amable, agradecido, casi servicial; la burla va por debajo y nunca se declara. Sirven el elogio
     envenenado, el sarcasmo seco, darle la razón hasta el absurdo y agradecerle lo que no quiso decir. La voz lo suelta con
     calma, sin enojo: si suena a pleito, perdimos. Cada canal con su voz y su lenguaje (un chiste de Elden Ring en Runa, etc.).
   - **Cuáles:** críticas exageradas, sin razón, de sabelotodo o de «ya no es lo que era». **Una queja JUSTA no se contesta así:
     se corrige** (punto 1). Si el dato que señala es cierto, no se le puede dar guasa.
   - **Ejemplos de tono (inventados, solo para el registro):** a «esto lo sabe cualquiera» → «Felicidades. Para el resto de los
     mortales hicimos este video.»; a «este canal ya no es lo que era» → «Tiene razón. Antes éramos menos.»
   - **Cómo sale:** tarjeta real `yt comentario` → `com_<id>` (`peg(...)`, 4-6 s), la voz la lee (o la resume) y remata en una o dos
     frases; un silencio corto antes del remate ayuda. Va en una pausa natural, nunca en plena revelación de un puesto. Queda
     anotado en la línea «Comentarios» del `ESTADO.md` y se le menciona al usuario al avisar del MASTER, para que lo vea.
   - **Límites:** se burla del COMENTARIO, no de la persona: nada de insultos ni groserías, físico, familia, origen, religión,
     identidad ni inteligencia a secas. Nada contra quien parezca menor de edad. Sin pedir a la gente que vaya a contestarle
     (YouTube sanciona el acoso dirigido). No repetir a la misma persona. Si al leerlo da lástima el otro, se pasó: bajarlo. El
     texto del comentario sigue sin inventarse ni retocarse, y la guasa nunca puede mentir sobre si la voz es IA (punto 3).
3. **Contestar:** borrador de respuestas con el tono del canal (las críticas, con el tono de 2c) → el usuario lo aprueba → envío por la API espaciado 25-60 s
   (`comments.insert`, 50 unidades c/u). Permitido por las Developer Policies si el usuario aprueba cada respuesta (III.I.2,
   III.C.3); el riesgo es el filtro de spam: sin respuestas idénticas, sin enlaces ni «suscríbete». Las preguntas de «¿la voz es
   IA?» las decide el usuario: nunca mentir. Corazones y fijar comentario: solo en Studio (la API no lo hace).
Plastitube y Runa Caída necesitan reconectar el token (`yt conectar`) para leer comentarios (403 de permisos, 27-oct).

## CAMPAÑA DE SUSCRIPCIÓN (el usuario, 30-oct-2026: Runa Caída y Crónicas de Tamriel, todo video nuevo)
«Tenemos poquitos suscriptores, hay que subirlos». Hasta hoy NINGÚN guion lo pedía. Datos a 90 días (`yt metricas`):
| | Subs | Vistas de NO suscritos | Subs ganados por 1 000 vistas | Audiencia al 80 % / al final |
|---|---|---|---|---|
| Runa Caída | 305 | **97,4 %** (3 de cada 100 suscritos) | 8,8 | ~50 % / ~20 % |
| Crónicas de Tamriel | 6 420 | **86,3 %** (14 de cada 100 suscritos) | 2,7 | ~48 % / ~20 % |
Pista (muestra pequeña): los largos narrativos convierten más que las listas de 8: Miquella 20:15 = 10,2 por 1 000 frente a Ranni
3,6; «15 TEORÍAS» 25:47 = 8,1 frente a 0,4-2,5 de las listas de ~11 min.
Metas públicas (en `campana_subs` de `canales/<alias>.json`): Runa **500 → 1 000** (1 000 es el umbral de monetización, junto con
4 000 h; lleva 1 913 h en 90 días y no está monetizado), Tamriel **7 000 → 10 000**.
1. **Dónde:** antes del último puesto (Runa, 5 puestos) o de los 2-3 últimos (Tamriel), hacia el 70-80 %: ahí sigue el doble de
   audiencia que al final y la promesa del n.º 1 retiene. Nunca en el gancho. Segundo toque de UNA frase en el cierre, junto a la
   pregunta para comentarios.
2. **Qué dice la voz (6-10 s, 2-3 frases, en el tono del canal):** la cifra real del momento («de cada cien que ven este canal,
   solo tres están suscritos»), la meta y que todos los comentarios se leen (encaja con los de agradecimiento). Sacar la cifra de la
   línea `suscritos` de `yt metricas <alias> 90` el día del guion. Redacción distinta en cada video; nada de «dale like y
   suscríbete» genérico. Ejemplos: Runa: «Antes del número uno, un dato que duele: de cada cien que ven esto, tres están suscritos.
   Queremos llegar a quinientos. Si llevas cinco atrocidades aguantando, esta es la más pequeña del video.» Tamriel: «De cada cien
   que ven este canal, catorce están suscritos. Los otros ochenta y seis entran, se llevan todo y se van, como en una tienda de
   Carrera Blanca. Queremos llegar a siete mil.»
3. **Qué sale en pantalla (encima del gameplay, sin parar el video):** interfaz del juego, nunca un botón rojo de plantilla.
   Runa: `E.cien("De cada 100 que ven Runa Caída", 3, ("Solo 3 están suscritos", 2))` + `E.mensaje(["Intenta suscribirte."])` +
   `E.puesto("Siguiente objetivo", "500 suscriptores")`. Tamriel: `T.rejilla("De cada 100 que ven este canal", 100, 14, ("Solo 14
   están suscritos", 2))` + `T.mision("Misión nueva", "Suscríbete a Crónicas de Tamriel")` + `T.mision("Siguiente objetivo", "7 000
   suscriptores")`. Marcas de `cien`/`rejilla`: aparecer, encender, remate. Sin repetir el mismo montaje en dos videos seguidos.
4. **Descripción, automático:** `yt subir` y `yt aplicar` meten tras el primer párrafo la línea de `campana_subs` con el enlace
   `?sub_confirmation=1` (abre el aviso de suscribirse). No escribirla en `youtube.json`. Al cumplir la campaña se quita el campo.
5. **Medir a los 7 días y anotar en `canales/formula/<alias>.md`:** subs por 1 000 vistas frente a la base (8,8 y 2,7) y caída de
   retención en el tramo. Objetivo: Runa ≥ 12, Tamriel ≥ 5. Si la curva cae más de 3 puntos en el tramo, acortarlo; si tras 3 videos
   los subs por 1 000 no suben, cambiar UNA variable (lugar o texto).
6. **Límites:** cifras siempre reales, sin sub4sub, sin sorteos ni recompensas por suscribirse, sin prometer temas que el usuario no
   haya decidido. En las respuestas a comentarios sigue sin pedirse (filtro de spam, § COMENTARIOS).

## Lecciones de `wow_objetos_secretos_forever` (1-nov-2026)
- **Anclas repetidas:** un ancla casa con la PRIMERA aparición; un cierre que repite palabras del gancho deja el efecto minutos en pantalla. Usar `#2` y revisar `fx hoja`.
- **Sonido con `--url`:** el clip puede quedar más corto que el beat y estirarse, y el sonido se desplaza. Medir `audio/ambiente.wav` y `audio/final.wav` en ese tramo antes del render.
- **Patrocinio:** `yt subir` marca la promoción pagada solo con «PATROCINADO» en la descripción o `"promocion_pagada": true` en youtube.json; comprobar la línea «promoción pagada: marcada» en el log.
- **Hoja de rigor:** extraer cuadros con `-ss`; `fps` + `tile` sobre el MASTER con pantalla final anexada solo entrega esa pantalla.
- **SFX de WoW:** banco en `nucleo/datos/sfx_juego/wow/` (misión aceptada y completada, subir de nivel, subasta), copiado a `sfx/<n>.mp3`. La búsqueda automática trajo una moneda de Mario y otro audio ajeno: comprobar el título de cada fuente.

## Pendiente del estilo
«Cambiar clip» desde el bloque del Montaje; dos apoyos a la vez en el mismo instante (hoy se pueden, pero se enciman).
