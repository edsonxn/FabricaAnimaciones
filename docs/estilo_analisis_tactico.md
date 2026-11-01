# Estilo ANÁLISIS TÁCTICO — una jugada explicada «como en la NFL» (esports / deportes)

Creado el 26-oct-2026 como prueba sin canal (`videos/lol_worlds_tl_al/`: el Barón de Team Liquid en la Worlds 2026 de
League of Legends). Pedido del usuario: «analice jugadas, repeticiones, como esos análisis de la NFL con efectos 3D,
flechas… haciendo pausas, dibujando flechas, rutas, elementos, mapa, todo para entender la jugada».

## Receta
1. **Elegir la jugada con datos**: resumen de YouTube → hojas de contacto (1 cuadro/15 s) → la secuencia decisiva.
   Los resúmenes SE SALTAN tramos (40:28 → 41:42 en el ejemplo): la jugada se corta del **VOD completo**. Con el reloj
   del juego en pantalla se saca el desfase (segundo del VOD = reloj + N) y se baja UN tramo de 2-3 min en 1080p
   (`ffmpeg -ss` sobre la URL de `yt-dlp -g`, video + audio) a `medios/_fuente/jugada.mp4`.
2. **Entender la jugada**: transcripción de la transmisión (`get_video_transcript` del VOD) para lo que pasa fuera de
   cámara + marcador (oro, asesinatos, torres) + minimapa (`previews/minimapas.png`: recorte del minimapa en cada momento).
   Los picks, de la descripción del VOD. Cero datos inventados: todo dato del guion sale de la transmisión.
3. **Guion** ~2 min: gancho con el final de la jugada → «vamos a rebobinar» → contexto (marcador en el tablero) →
   pausas con telestrador → tablero con el «por qué» (rotaciones, oleadas, visión) → desenlace en cámara lenta →
   la lección + pregunta. Voz ElevenLabs con corchetes (ejemplo: JC «Energetic News Broadcaster»).
4. **Montaje con UN solo clip** (motor SECUENCIA YT): `beats` normal, `medios/scene-NNN.jpg` de relleno, y TODO el
   cuadro lo pone el FX `video` del clip fuente: `vel=1` juega, `vel=0` congela (pausa), `vel<0` rebobina, `vel<1`
   cámara lenta. Helper `J(de, a, desde, vel)` en `efectos.py`.
5. **Kit `nucleo/mg_tactica.py`** (tiempos ABSOLUTOS de la voz):
   - `pizarra(de, elementos, "PAUSA", "40:16")` sobre el cuadro congelado: `anillo` en el suelo bajo cada jugador (borde
     que se traza + onda + etiqueta con línea guía), `flecha` que se dibuja sola (Catmull-Rom, discontinua para
     «llega tarde»/intención), `zona`, `texto`, `foco` (oscurece todo menos los anillos). Chip «❚❚ PAUSA · reloj».
     Posiciones: cuadro con rejilla (`previews/cuadros/g<t>.jpg`), el anillo va a los PIES, no a la barra de vida.
   - `tablero(de, mapa, elementos, camara, titulo, reloj, hud, iconos)`: mapa oficial (Data Dragon `map11.png`) en un
     plano girado 40° con cámara (zoom/paneo por fases), `ficha` con el icono REAL del campeón que sigue una ruta
     con tiempos, `oleada`, `tp` (arco punteado + remolino), `ward` (ojo + visión), `niebla`, `num` (pasos 1-2-3),
     HUD de píldoras con fin opcional.
   - `chip(...)` (píldora suelta: «REPETICIÓN», «-2 DESTELLO» con icono del hechizo) y `rebobinar()` (rayas de cinta).
6. Sonido: música de la biblioteca (`biblioteca sugerir`), SFX de la biblioteca (`biblioteca sfx usar`): golpe + clic en
   cada pausa, rebobinado, swoosh al entrar al tablero, pop en cada etiqueta, subida antes del momento clave.

## Voz: pronunciación de nombres en inglés (el usuario, 26-oct-2026)
- En la prueba la voz dijo «Liquid» a la española; se pronuncia **«Lícuid»**. En TODO video de este estilo, `FONETICA` en
  `guion.py` con los nombres de equipos y jugadores en inglés: config.py la aplica también a ElevenLabs (`FRASES_TTS`) y el
  guion conserva la grafía real para el .srt. Punto de partida (revisar oyendo): `"Team Liquid": "Tim Lícuid"`,
  `"Liquid": "Lícuid"`, `"Anyone's Legend": "Éniuans Léyend"`, `"Gen.G": "Yen yi"`, `"Dplus KIA": "Di plus Kía"`,
  `"Bilibili Gaming": "Bilibili Guéiming"`, `"Top Esports": "Top I spórts"`, `"Movistar KOI": "Movistar Koi"`,
  `"Hanwha Life": "Janjua Laif"`, `"Karmine Corp": "Karmin Corp"`, `"Cloud9": "Claud náin"`, `"Worlds": "Uórlds"`.
  Whisper sigue comparando contra la grafía real: sube `CER_MAX_POR_FRASE` donde haga falta tras leer la transcripción.

## Velocidad de render (optimizado el 26-oct-2026)
- Primera versión: ~0,9 s/cuadro (pausas ~0,8 s, tableros ~1,2 s, niebla 2,5 s): 2 min de video ≈ 40 min en un proceso.
- Ahora: **~60 ms/cuadro de media** (tableros 50-100 ms, pausas 70-110 ms, clip solo 12 ms). Claves: `_sobre` y el `_pegar`
  del motor trabajan solo en el recuadro con alfa (`cv2.boundingRect`), copia directa si la capa es opaca y `cv2.blendLinear`
  en vez de numpy; el mapa se deforma sobre el fondo con `BORDER_TRANSPARENT` (sin máscara); niebla a 1/4 de resolución;
  centinelas en parche local; el foco es la capa de ABAJO de la pizarra (antes apagaba también las flechas).
- Regla: nada de capas de 1920×1080 por elemento; dibuja en un parche del tamaño del elemento.
- Videos largos (18 min ≈ 32 000 cuadros ≈ 30 min a 60 ms): además, render en tramos paralelos
  (`fab.py <v> video --tramo a-b --salida salida/par_k.mp4` ×6 + `ffmpeg -f concat -c copy` → `salida/video_sin_audio.mp4`
  → `final`). El script de la prueba: 6 procesos subieron la CPU de 23 % a 97 %.

## Errores a no repetir (primera prueba)
- `tv`, `zoom`, `oscurecer`, `desaturar` del motor se aplican ANTES del FX `video`: con el clip a cuadro entero NO se ven.
  Por eso el foco y el rebobinado viven en el kit.
- Tablero amontonado: con fichas grandes y 10 nombres no se lee nada. Fichas chicas, nombre SOLO de quien nombra la voz,
  zoom de cámara en cada fase, y todo elemento con `sale` cuando ya no se habla de él (también las píldoras del HUD).
- Etiquetas en capa aparte encima de las fichas (si no, las fichas las tapan).
- La flecha de una intención (flanco) se dibuja ANTES de que las fichas se muevan.
- Whisper rechaza tomas buenas por los nombres («varón» por Barón, «John» por Yeon): `CER_MAX_POR_FRASE` tras leer la transcripción.

## Gráficos de transmisión: `nucleo/mg_lol.py` (el usuario, 27-oct-2026, `lol_worlds_2026`)
- Las píldoras `mg_tactica.chip` sobre el gameplay «se ven muy básicas, poco impresionantes»: en este estilo NO se usan solas.
  Se edita como Warcraft/Tamriel/Runa (docs/estilo_secuencia_yt.md § PEGATINAS y § MOTION GRAPHICS NUEVOS): pegatina real casi en
  cada frase (fotos oficiales de jugadores y arte de campeones), MG propios del guion que entran por partes con la voz, nada
  quieto > 2 s, y el gancho (primeros 30-45 s) cargado de MG.
- Kit `mg_lol`: `tarjeta` (tercio inferior de vidrio con filo dorado, logo, barrido, giro 3D que respira), `pegatina`,
  `resultados`, `caida`, `eliminado`, `apertura`, `versus`, `menu`, `suiza`. Hoja de prueba: `videos/lol_worlds_2026/_prueba_mg_lol.py`.
- Recursos oficiales: logos y fotos de jugadores con la API pública de LoL Esports (`esports-api.lolesports.com/persisted/gw/
  getTeams`, clave pública de la web; las URL `http://static.lolesports.com` redirigen: bajarlas por HTTPS o salen HTML);
  arte de campeones de Data Dragon (`cdn/img/champion/splash/<C>_0.jpg` y `loading/<C>_0.jpg`).

- **Durante el análisis de una jugada (el usuario, 27-oct-2026):** flechas, rutas y zoom; tarjetas y pegatinas CHICAS y en los bordes
  (esquinas o sobre el marcador de abajo) para no tapar la jugada. Fuera del análisis (gancho, resúmenes) sí van grandes.

- **MG nuevos (27-oct-2026, tramo 3 de `lol_worlds_2026`)**: `ficha_jugador(foto, nombre, logo, n, stats)` (top de jugadores:
  foto que sube, «N.º k», barras de estadística que se llenan con la voz), `ranking(titulo, filas)` (puestos en rombo dorado),
  `tabla(titulo, columnas)` (equipos por récord: 2-0 | 0-2), `calendario(titulo, hitos)` (línea de fechas, la final con halo),
  `barras(titulo, items, total)` (picks: «12 de 29») y `resultados` con ganador None = cruce por jugar («VS» o la fecha).
  Hoja: `videos/lol_worlds_2026/_prueba_mg_nuevos.py` → previews/mg_lol_nuevos.jpg.

## Zoom en la pausa y en la cámara lenta (27-oct-2026)
- El FX `video` acepta `zoom=(z, cx, cy)` (centro en fracción del cuadro fuente), `zoom0` (inicio; por defecto sin zoom),
  `zoom_en` y `zoom_dur`: acercamiento animado, también con el clip congelado o en cámara lenta. Para mantenerlo en el
  siguiente tramo, `zoom0 = zoom`; para salir, `zoom0 = (z, cx, cy)` y `zoom = (1, .5, .5)`.
- La pizarra NO se transforma: si una pausa lleva zoom, mide anillos y flechas sobre el cuadro ya acercado (rejilla con el mismo
  recorte). En el resumen de la Worlds el zoom se usó en las cámaras lentas (1,28-1,45) y las pausas quedaron a cuadro entero.

## Verificar cada frase con el MARCADOR y el VOD, no con el resumen (27-oct-2026)
- Los resúmenes oficiales PEGAN momentos distintos y la narración se monta encima: en DK-T1 el «Goodbye Lucid» era del 37:08
  y la pelea del Anciano del 40:25 (Lucid vivo). El guion decía «con uno menos»: falso. Antes de analizar una jugada, lee el
  RELOJ del juego en cada cuadro de la hoja de contacto (un salto de reloj = corte del resumen) y los subtítulos del VOD completo.
- El marcador dice más que los narradores: la fila de dragones (de qué lado están) desmintió «Hanwha aseguró el alma»
  (eran los 4 dragones de IG); la diferencia de oro a lo largo de la partida desmintió «KOI acababa de ganar una pelea».
- Corregir una frase sin mover el resto: regenerar solo esa frase (`voz` detecta el texto cambiado), `seleccionar`, `tiempo`,
  y si la escena pierde/gana un compás, `"post": s` en esa escena del guion para que conserve sus compases.
- El FX `cierra` sin `a` deja el video en NEGRO hasta el final: entre secciones, `cierra` con `a` + `abre`.
- (27-oct, 2.ª ronda) Fuentes que NO mienten, en este orden: kill feed y banners del cuadro; los RETRATOS del HUD (se ponen
  grises con su temporizador: orden real de las muertes); la tabla de K/D/A (quién sumó la muerte); la narración del VOD
  transcrita con Whisper large-v3 (`initial_prompt` con los nombres) — los subtítulos automáticos cambian nombres («Cuzz» =
  Keria). Nunca escribir intenciones que nadie dijo («espera a que gasten todo», «busca a uno solo»): o lo dice la narración
  o se ve en los cuadros. Si dos momentos del resumen están separados (Barón 20:24 → pelea 34:41), la voz lo DICE.
- Al regenerar varias frases: compara las escenas con `timeline_beats.json` (o una copia previa de timeline.json) y añade
  `"post"` a las que pierdan un compás; así los ~300 efectos con tiempo absoluto no se mueven.

## Jugada clave en 3D: `nucleo/tactica3d` (el usuario, 27-oct-2026)
«En la más importante algún sistema 3D como three.js… que se aprecien las intenciones, movimientos y rutas». Primera: el Barón
de Liquid en `videos/lol_worlds_2026/` (`j6_3d.py` → `tactica3d/j6.json` → `medios/_fuente/j6_3d.mp4`, 35 s en 66 s).
- Motor: `nucleo/tactica3d/grieta3d.html` + `grieta3d.js` (three.js r160 en `vendor/`, sin CDN). Terreno de la Grieta con
  relieve real, río y árboles a partir del minimapa oficial (`preparar_grieta.py` → `assets/`), fichas con el retrato del
  campeón y el nombre del jugador, rastros (rutas) que se dibujan solos, flechas de INTENCIÓN (discontinuas) y de movimiento
  (continuas), anillos, oleadas de súbditos, TP con haz, proyectiles (cohete de Jinx), torres que caen, objetivos (dragón,
  Barón) con su imagen REAL recortada del VOD y barra de vida con los números leídos en pantalla, niebla de guerra (oscurece
  el mapa salvo la visión de un equipo y deja al otro como fantasma), reloj de juego, columna de datos y carteles (PAUSA,
  «30 segundos después»). Fuente Poppins en `fuentes/` (la del kit).
- Render: `python nucleo/tactica3d/render3d.py <escena.json> <salida.mp4>` (Edge sin ventana + GPU, ~2 cuadros por cuadro
  real); `… <carpeta> --cuadros 976 990 1004` para revisar; `--url` lo abre en vivo en el navegador (`&vivo=1`).
- Escena (JSON, la escribe un `.py` del video): `de`/`a` en segundos del VIDEO; `reloj` = [[t_video, s_juego]…] (permite
  pausas y saltos); `fichas` con `puntos` [[s_juego, u, v(, "salto")]] medidos en el minimapa (u, v = fracción, mismo
  encuadre que `mapas/grieta.png`); `estructuras`, `objetivos`, `oleadas`, `tps`, `flechas` (con `id` para colgarles
  rótulo), `anillos`, `proyectiles`, `focos`, `rastros` (`ventana` en s), `niebla`, `hud`, `etiquetas` (ancla `quien`,
  `flecha` o u/v), `carteles`, `destellos`, `camara` [[t, u, v, distancia, inclinación°, giro°, fov]] (Catmull-Rom).
- Medir posiciones: hojas del minimapa con rejilla de décimas cada 2-6 s (recorte 1640,800 de 276 px en las transmisiones de
  LoL Esports) + la vista principal para saber quién es quién en los grupos. El rastreo automático por plantillas FALLA
  cuando los iconos se enciman: medir a mano. Precisión ~±0,03 del mapa; donde no hay datos (regresos a base), salto de tiempo
  con cartel, no rutas inventadas.
- En efectos.py el 3D entra como FX `video` (`ruta=…j6_3d.mp4`, `desde = t − de`) tras el rebobinado, y al clímax vuelve el
  VOD real (el castigo). Los sonidos del 3D (TP, torre, cohete) van en PISTAS con los instantes que imprime el JSON.

### VOD real INTERCALADO con 3D (el usuario, 27-oct-2026: «no olvides mostrar la jugada con el video real y ahí también
### elementos 3D… una combinación de video real intercalando 3D»)
- Nunca 30 s seguidos de mapa 3D: alternar por frases. j6: 3D (contexto) → VOD (el dragón) → 3D (pausa, oleada, TP) → VOD
  congelado con elementos 3D (AL vuelve a defender) → 3D (flanco, oscuridad, Barón) → VOD con 3D (cohete) → VOD (castigo).
  `V3(de, a)` toma el tramo del clip 3D que corresponde (`desde = de − inicio del clip`).
- **Elementos 3D sobre el VOD** (`E.modo = "video"`, `nucleo/tactica3d/sobre_video.py`): `pizarra3d(nombre, de, a, els, reloj,
  (fuente, s))` convierte la pizarra 2D de una pausa (mismos x, y medidos en el cuadro) en capa transparente: anillos tumbados
  en perspectiva del suelo, columna de luz sobre cada jugador (anillos ≤ 80 px), flechas en arco con sombra, zonas con borde
  de luz, rótulos con retrato; `extra=dict(proyectiles=[…])` para el cohete, etc. Se renderiza con
  `python nucleo/tactica3d/sobre_video.py <video>` (solo las que cambian; dos MP4 color+alfa que lee `capa.py`).
  Revisar: `render3d.py <capa>.json <carpeta> --cuadros t` (pone el cuadro real debajo).
- **«Mesa»** (`E.modo = "mesa"`, `videos/lol_worlds_2026/mesas_3d.py`): el cuadro congelado se proyecta sobre un suelo 3D; la
  cámara parte del encuadre del juego (con el cuadro real encima fundiéndose: el corte no se ve), baja y gira, los jugadores se
  levantan como fichas con retrato en su sitio real (placa de nombre + 0,06 = pies) y vuelve al encuadre del juego para que el
  VOD siga desde ese cuadro. `MESA(k, de, a, reloj)` en efectos.py. Para PELEAS es mejor que el mapa: el minimapa encima los
  iconos y los resúmenes de LoL Esports no dan un rectángulo de cámara fiable (el Anciano no cae donde dice el rectángulo).
- Comprobar la alineación de las fichas con la cámara fija en la pose del juego (`camara = [[de]+G, [a]+G]`, fichas visibles)
  antes del render: cada disco debe caer bajo su campeón.

## Previa de un partido + jugadas con MÁS pausas (27-oct-2026, `videos/ig_lyon_worlds/`)
- Pedido del usuario: video de ~12 min para quien NO conoce a los equipos (historia, camino, jugadores, jugadas) y «más pausas
  durante los enfrentamientos… más líneas, rutas, flechas». Receta: 4 jugadas × 4-6 pausas, cada pausa con 2-5 elementos
  (anillos con etiqueta, flecha de la acción, zona, chips de «quién/qué»), una mesa 3D y una capa 3D por jugada; entre pausas el
  VOD corre estirado/acelerado para llenar la frase (`CLIP(n, de, a, t0, t1)`), con «▶▶ ACELERADO» si va rápido.
- **Hallar las peleas sin ver horas de VOD:** el feed oficial `feed.lolesports.com/livestats/v1/window/<gameId>?startingTime=…`
  (cada 10 s, sin clave) da muertes, oro, dragones y barones por jugador → lista de quién mató a quién y cuándo
  (`videos/ig_lyon_worlds/investigacion/muertes.py <gameId>…`; también `cortar.py` = tramo 1080p de un VOD y `vtt.py`). Los gameId salen de `getEventDetails`. El reloj del feed puede ir desfasado
  hasta ~100 s del reloj del HUD (TSW-IG): calibrar SIEMPRE con un cuadro del VOD y dar en la voz el reloj del HUD.
- **Narración del VOD:** los subtítulos automáticos de YouTube (`yt-dlp --write-auto-subs --sub-langs en`) salen en segundos y
  bastan para saber qué dijeron los narradores; Whisper large-v3 solo si hace falta precisión (con la GPU ocupada tarda > 20 min).
- **Efectos anclados a la VOZ, no a segundos:** `efectos.py` lee `timeline.json` y usa `T0(k)`, `T1(k)`, `W(k, "palabra")` y
  `NX(k)` (inicio de la siguiente frase): se escribe antes de tener la línea de tiempo y sobrevive a `tiempo` si cambia la voz.
  `W` falla con KeyError si la palabra no está (se ve en `fx --seco`).
- Con ElevenLabs, Whisper rechaza ~la mitad de las frases por los NOMBRES («Lion», «Yachi», «Genji», «Janjoa»): leer las
  transcripciones de eval.json y poner `CER_MAX_POR_FRASE`/`TAIL_MAX_POR_FRASE` = medido + margen (sin regenerar voz).
- Duración: 1 760 palabras + 4 tramos en vivo salieron 13:27; recortar los `pre` en vivo (16/12/12/18 s) y una frase final de
  escena (no del medio: desplaza índices) bajó a 12:55 sin regenerar nada.

## Pendiente
- Zoom con la pizarra transformada (hoy la pizarra se mide sobre el cuadro ya acercado).
- Audio de los comentaristas/estadio bajo la voz en los tramos que juegan (FX `video` no lleva audio a la mezcla).
- Tablero de otros juegos/deportes: solo cambia el mapa (cancha, campo) y los iconos.

- **Fecha relativa = día de PUBLICACIÓN (28-oct-2026, `ig_lyon_worlds`):** la previa se produjo la víspera y la voz decía «mañana»; sale el mismo día del partido → «hoy / esta tarde». Antes de `voz`, grep de «mañana|hoy|ayer» en guion y placas contra la fecha de publicación. Corregir después cuesta voz + re-render de los tramos (las escenas no se mueven: van a compás).

## Errores corregidos tras la revisión del usuario (28-oct-2026, `cfo_kc_worlds`) — revisar SIEMPRE antes de entregar
1. **Anillos fuera de sitio** («esos círculos mal posicionados», también en videos anteriores). Causas: (a) medir en hojas 2×2
   (`j1_comp.jpg`) y leer la altura de los cuadros de ABAJO respecto a la hoja entera; (b) poner los pies en «placa + 0,07»: en
   1080p los pies quedan entre +0,08 y +0,18 bajo el nombre según el zoom de la cámara. Regla: `rejilla2.py <n> <t>` = UN cuadro a
   1280 px con rejilla cada 0,05, y se miden directamente los PIES de cada campeón (nunca la placa). Lo que esté bajo el HUD
   (y > 0,76) o no se identifique con seguridad, no lleva anillo: texto suelto.
2. **Rutas con puntos inventados**: una ruta solo con puntos MEDIDOS y dentro de la MISMA toma de cámara
   (`investigacion/cam_j*.json` marca los cortes; `ruta()` avisa «AVISO ruta … cruza un corte» y no dibuja). Nada de puntos
   intermedios estimados ni rutas de reserva escritas a mano.
3. **Saltos de tiempo tras una pausa** («la pausa no está sincronizada con la continuación»): cada tramo del VOD arranca en el
   cuadro EXACTO donde quedó la pausa o la mesa anterior; si hay que avanzar, `CLIP(t_pausa → t_destino)` con «▶▶ ACELERADO»;
   las repeticiones con `desde = t_pausa_siguiente − vel·duración` para terminar en ese cuadro; nunca volver atrás salvo en un
   «REBOBINANDO» o una «REPETICIÓN» rotulados.
4. **Narradores lentos en los tramos en vivo**: con video+audio (`+ba`) yt-dlp entrega tramos más cortos (~10 s para un beat de
   17 s) y el motor los estira (0,6×), voz incluida. Tras `bajar`, comparar la duración de cada clip con su beat; los tramos en
   vivo se cortan de la fuente local de la jugada (`medios/_fuente/j*.mp4`, imagen y narración alineadas) con ffmpeg.

## Nunca cámara rápida en una jugada (el usuario, 31-oct-2026, `lol_semana2`)
Tras explicar, «les das play pero en cámara rápida y no se alcanzan a ver bien»: la acción va SIEMPRE a x1 o más lenta. `CLIP(n, de, a, t0, t1)` estira el video para llenar
la frase y por eso aceleraba (109 tramos > x1,05, hasta x10). Si la acción no cabe en la frase: `"post"` en la escena con la narración original, o saltar por corte entre momentos.
Los clips de contexto se recortan a x1; se quitan los «» ACELERADO». Sustituye al «ACELERADO» del § «Errores corregidos» punto 3: para llegar a otro momento, corte rotulado, no acelerar.
**Nunca cortar la voz dentro de una palabra (el usuario, 31-oct-2026: «hay sílabas que se cortan y se continúan después del clip»).** Los tiempos de `palabras.json` fallan hasta 0,9 s: un corte calculado con ellos cae en plena sílaba (17 de 51 en el primer intento). Cada silencio va en una pausa REAL medida en la señal, de ≥ 120 ms (60 ms de margen a cada lado, fundido de 12 ms): `investigacion/pausas_frase.py <frase>` da las pausas y el 4.º valor de `ESPACIOS_VOZ` fija el segundo. Donde no hay pausa natural («cuádruple y ace», «y nexo», «baja a setecientos») el silencio se mueve a la pausa anterior o al inicio de la frase, y el ancla del video se ajusta; regenerar es el último recurso. Chequeo: `investigacion/cortes_voz.py` (`--whisper` escucha 1,5 s a cada lado; las diferencias de escritura de nombres no son fallo, solo una palabra partida); `espaciar_voz.py` se niega a cortar sin pausa y `render_par.py` no arranca si un corte falla. Evitar saltos del VOD de menos de 1 s: se ven como tirón; mejor quitar anclas y dejar el tramo corrido a x1.
**Cómo se hace sin regenerar voz (`videos/lol_semana2/`):** `espaciar_voz.py` + `ESPACIOS_VOZ` en guion.py meten silencios DENTRO de las frases ya grabadas, entre palabras: la lista de muertes se vuelve relato en vivo, cada muerte cae a x1 cuando la voz la nombra y en el hueco entra la narración original sola (efectos.py la detecta y escribe `vivos.json`; `_VIVOS` lo lee, uniendo huecos a menos de 4 s para que la música no bombee). El hueco se calcula con `tramo de VOD − voz`. Más de ~6 s de hueco entre dos momentos o tiempo muerto (35 s hasta el nexo): corte a mitad de tramo (`TRAMO`/`SYNC`), lo que sigue al momento anterior + lo que lleva al siguiente. `REBX` rebobina justo hasta lo que cabe a x1 antes de la pausa. Control: `investigacion/velocidades.py --cortes` (x1, saltos y fuentes que se pasan). Coste: 15:19 → 19:16 (entender manda sobre la duración; se recorta contexto, no jugadas). Con más beats, `medios_locales.py` antes del render. `seleccionar` borra los silencios: tras él, `espaciar_voz.py` y `tiempo`. Las piezas de música se quedan cortas: `alargar_musica.py`.

## Análisis de un partido YA JUGADO, el mismo día (28-oct-2026, `videos/t1_koi_worlds/`, ~1 h 40 min de principio a subida)
- **Sin spoiler** (el usuario): ni miniatura, ni título, ni gancho, ni los clips del gancho dicen quién ganó; el resultado de cada
  partida se descubre en su última jugada. Miniatura neutra («T1 vs KOI · LA PELEA CLAVE»).
- **Investigación en paralelo**: un agente por partida (feed `window` + VOD + Whisper) deja `investigacion/datos_g<p>.md` con el
  desfase VOD = HUD + K, las jugadas con reloj del HUD y las fuentes `medios/_fuente/g<p>_j<k>.mp4` (HUD = t + K por fuente).
  Los VOD de la Worlds en el canal `UC-I8d_BjKP6MMsYjZhAtjIA` salen en ESPAÑOL a la hora de terminar cada partida.
- **Tramos EN VIVO con la narración original**: el FX `video` de la fuente local cubre de e0 a la primera frase y
  `vivos_audio.py` escribe `audio/ambiente.wav` (48 kHz) con el audio de esa misma fuente; la música baja 16 dB (`MEZCLA.musica_curva`).
  Se corre DESPUÉS de `video` (que borra ambiente.wav si ningún beat lleva `ambiente_por`) y antes de `mezcla`.
- **Pausas 3D**: en `sobre_video`, los `texto` de una pizarra 3D salen CENTRADOS en x (solo cuenta `y`): sacar a `tar(...)` los que
  choquen con anillos. Un `tar(...)` NO puede ir dentro de la lista de una pizarra (KeyError 'en').
- **Duración**: la voz JC habla ~2,4 palabras/s; 1 700 palabras + 7 vivos de 17-21 s + 6 repeticiones = 15:27.
