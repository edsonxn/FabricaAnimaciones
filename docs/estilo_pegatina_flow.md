# Estilo «pegatina Flow» — recortes animados con piezas de Flow (20-oct-2026)

**Idea del usuario (20-oct-2026, video `jalpa`, Bitácora Perdida):** «aprovechar Flow para crear los escenarios y una serie de personajes,
elementos, etc. y usarlos para la animación tipo pegatinas con movimiento… hojas de varios elementos con Nano Banana 2.1… incluso a
1 personaje hacerle una secuencia en la misma imagen (caminando o cualquier acción)». **Flow PINTA todo; el código lo MUEVE.**
Aprobado tras la prueba de 54 s: «me gusta mucho el estilo, continúa con todo el video».
Kit: `nucleo/pegaflow.py` · ESTILO_VISUAL = `"pegatina_flow"` (registrado en `nucleo/estilos.py`) · ejemplo completo: `videos/jalpa/`
(`guion.py` con FICHA, `prompts.json`, `escenas.py`, `_vivo.py`, `_tl_provisional.py`).

## 0. Receta en orden (lo que se hizo en `jalpa`, ~1 sesión para 1 min)
1. `python fab.py nuevo <v>` → guion.py con `ESTILO_VISUAL="pegatina_flow"`, `FICHA` (estilo común de Flow), `LYRIA`, `ALIAS_QA`, `FONETICA`.
2. `prompts.json` (escenarios + hojas) → `flow_integrado.py paquete` → Flow en el navegador integrado (§1) → `bajar` → `imagenes/`, `hojas/`.
3. `python nucleo/pegaflow.py recortar <v> hoja=N …` (§2) → mirar `piezas/*/_indice.jpg`.
4. `python ../../nucleo/preparar_profundidad.py canon_a senorio_a …` (desde la carpeta del video) → `imagenes/depth/`.
5. `python _tl_provisional.py` → `timeline.json` estimado para armar tomas SIN voz; `escenas.py` (§3); `_vivo.py hoja/video` (§4).
6. `voz` → `seleccionar` → `tiempo` (las tomas se reacomodan solas: todo se ancla con `T(escena, palabra, frase)`).
7. `lyria_tramos.py todo` → `sfx` → `mezcla` → `_vivo.py video` (montaje con audio) → revisar 1 cuadro/3 s → `video` → `final` → `verificar`.

## 1. Flow: qué pedir y cómo (Nano Banana 2.1 · 16:9 · x2 = 0 puntos el 20-oct)
- **FICHA común** al principio de TODOS los prompts (mismo trazo, paleta, época) → las pegatinas casan con los fondos. La de Jalpa:
  «Hand-painted 2D cut-out animation art, children's history picture book style: clean dark-brown ink outlines, flat gouache colors
  with soft painted shading and visible paper grain, warm earthy palette (…), southwestern Mexico, Caxcan people … 1540». Cierre:
  «No text, no letters, no watermark».
- **Escenario** (uno por lugar/hora: mañana, nublado, noche, atardecer): «Wide background of …», «Strong depth: foreground …, midground …,
  background …», «Open empty ground across the lower third», «No people, no animals». Los personajes los pone el código.
- **Hoja de personaje:** «Character model sheet on a plain flat pure white background: <ficha física> The SAME man drawn 5 times, full
  body, evenly spaced in one row with generous empty white space between them, never touching or overlapping: <pose 1>; <pose 2>…
  No ground, no cast shadows.» Poses útiles: calma, habla con la mano abierta, señala, furia (arma en alto), brazos cruzados, asustado,
  a caballo, con documento.
- **Ciclo en la MISMA imagen** (consistencia total): «Animation sprite sheet on a plain flat pure white background: walk|run|gallop
  cycle of <ficha>. The SAME character drawn 8 times in a single horizontal row, strict side view facing right, full body, same size and
  same height, evenly spaced and not touching, each drawing a consecutive phase of one walking step». Salieron bien: caminar 8, correr 8,
  galope 6 (caballo + jinete), aleteo de ave 6. SIEMPRE mirando a la DERECHA (el código voltea).
- **Utilería** (~16 objetos en rejilla «never touching») y **naturaleza** (árboles, nopal, maguey, rocas, nubes, «a row of 6 drawings of
  the same black bird showing a wing-flap cycle»): primer plano, objetos que «aparecen», cielo vivo.
- **Otras épocas con la misma FICHA** (video que cruza siglos): justo tras la ficha, «Same art style, but this picture is set in
  <año>: <qué>.» Funcionó en jalpa para 1800, 1811, 1858, 1864 y hoy sin perder trazo ni paleta (y `paquete` sigue validando que
  todos empiecen con la ficha). Para un lugar real de hoy, describir la foto de Commons (torres, material, reloj) en el prompt.
- **Mismo lugar en dos escenas** (mina de día / la misma tienda de raya al anochecer): dos prompts con hora y encuadre distintos =
  continuidad narrativa sin repetir fondo.
- **Lote grande** (28 prompts x2 en jalpa, tramo 2): `__ins` + Return en `browser_batch` de ≤ 25 acciones; a los ~3 min ya están
  todas; recolectar con el recorrido de scroll (§ abajo) → los `Expires` salen en pares crecientes = orden de envío (comprobación).
  Numerar la descarga desde 101 si `medios/` pudiera tener `scene-0NN` de antes.
- **Mosaico con «Error»** (la_sena, 20-oct: 1 de 72): no trae `<img>`, así que el recorrido junta 71. Se ve como un hueco doble en
  `y` entre mosaicos (con el panel angosto Flow pone 1 por fila, ~374 px) y como un `Expires` sin pareja; meter un `null` en ese hueco
  ANTES de invertir y el índice k da el prompt (k//2) y la variante (k%2). El resto de la numeración no se mueve.
- Defectos vistos: un ciclo de 8 salió en 2 filas de 8 (16 figuras) y otro con una línea de suelo: elegir la otra variante
  (renombrar a/b) ANTES de `recortar`, que solo lee `_a`.
- x2 = dos variantes por prompt: elegir la de fondo BLANCO puro (la de fondo crema o con marco recorta peor). Evitar objetos BLANCOS
  (la nube blanca se perdió al recortar).
- **Mecánica del navegador integrado** (sesión de Flow ya abierta): proyecto nuevo → chip «Imagen · 16:9 · Nano Banana 2.1 · x2» →
  pegar `_bundle.js` en `javascript_tool` → por prompt `await window.__ins(i)` + `key Return` real (13 en un `browser_batch`).
  **NO usar `__col` con espera larga**: pasa los 45 s del `javascript_tool` y marca las imágenes como vistas. En su lugar, recorrer el
  scroll y juntar todas las `img[src*=flow-content]` con su posición (`window.__all`), ordenar por (y, x), INVERTIR (lo nuevo sale arriba)
  → índice k = prompt k//2, variante k%2 → «N uuid expires firma» → `python nucleo/flow_integrado.py bajar <v>` (stdin; el BOM de la
  tubería de PowerShell ya se ignora) → renombrar `scene-NNN.jpg` a `<clave>_a|b.jpg`.
- **2K (2752x1536, gratis) NO**: menú → Descargar → 2K abre «Guardar como» de Windows POR imagen y el usuario no quiere aceptarlas.
  El 2K llega como base64 dentro de la respuesta `batchexecute` (rpc `SPrCad`) y la página fuerza la descarga de un blob: no hay URL
  para curl. Un gancho sobre `HTMLAnchorElement.prototype.click` (blob → no descargar) quita las ventanas, pero el archivo no sale del
  navegador. Decisión del usuario: 1K (1376x768); para hojas sobra; los fondos con zoom > 1,25 se ven algo blandos.
- Revisión: hojas de contacto de `imagenes/` y `hojas/` (400 px por imagen) antes de recortar; rejilla 10x10 sobre cada escenario
  (`previews/_rejilla.jpg`) para colocar puertas, chimeneas, fogatas y el suelo libre en coordenadas normalizadas.

## 2. Recorte (`python nucleo/pegaflow.py recortar <v> [hoja] [hoja=N] …`)
- Lee `hd/*_a.jpg` (si hay 2K) o `hojas/*_a.jpg` (las que también están en `imagenes/` son escenarios y se saltan). Escribe
  `piezas/<hoja>/NN.png` en ORDEN DE LECTURA (filas arriba→abajo, izquierda→derecha), `_indice.jpg` numerado (MÍRALO y nombra las piezas
  por su número en `escenas.py`; apunta el mapa número→pose en el ESTADO.md) y `meta.json`. Hojas con
  «camina|corre|galope|ciclo|aleteo|marcha|danza» en el nombre (marcha/danza desde el 20-oct) → además `ciclo_NN.png` en
  un lienzo común, pies abajo y eje de cabeza+torso (55 % superior) al centro: el ciclo no baila.
- **Alfa:** color del fondo = mediana del borde; fondo = zonas casi de ese color CONECTADAS AL BORDE (inundación) → el algodón blanco
  encerrado por la tinta se conserva. Huecos interiores (brazo en jarra, entre arco y cuerda) = color EXACTO del fondo (p90 < 0,22·tol) o
  zona plana que rembg `isnet-anime` (en caché) también da por fondo. Borde antialias con descontaminación del blanco.
- **Agrupar:** junta fina (lado/600 px); trozos chicos a < 4 juntas de una figura (plumas, flechas) se le pegan; chicos sueltos con área
  suficiente (aves) quedan como pieza propia; motas fuera.
- **`hoja=N`** fija cuántas figuras hay (se guarda en `piezas/cuantas.json`): si dos se tocan (los caballos del galope salían en 2 piezas
  en vez de 6) se parten por los valles de la suma de alfa por columnas. Jalpa: `caballo_galope=6 petacatl_hoja=5 proano_hoja=5
  petacatl_camina=8 guerrero_corre=8 caxcanes_hoja=6`.

## 3. Animación (`escenas.py`; API en el docstring de `nucleo/pegaflow.py`)
- **Toma** = función `dib(lz, t)` registrada con `@toma(t0, (transición, dur))`; `render_mundo(t)` elige la toma, mezcla con la anterior
  (`docu.mezcla_tomas`: latigo, desenfoque, destello, negro, fundido, corte), aplica `PF.acabado` y los fundidos de entrada/salida.
  `Mundo(Escena)` registra los SFX (`snd(t, nombre, vol, dur=…)` a nivel de módulo; nombres de `nucleo/sfx.py`: viento, fuego, galope,
  tambor, pasos, papel, pop, sello, golpe_grave, cuerno…).
- **Cámara:** `PF.Plano(fondo, t0, t1, z0, z1, c0, c1, par=(28, 6), tono=None)` = zoom/centro con easing + deriva de cámara en mano +
  parallax por profundidad (`par` = px que se desplaza lo cercano). Cada toma, su propio Plano (zoom 1,0-1,3; acercamientos de detalle
  1,5-1,95). Mismo escenario en dos tomas seguidas = encuadres MUY distintos (general / detalle).
- **Colocar:** `.en(t, x, y, frac)` → (X, Y, alto px) con los pies en (x, y) del escenario normalizado; `.P(t, x, y)` para puntos (humo,
  fogatas, río). **Tamaño por perspectiva:** `alto(y, horizonte, k)` = k·(y − hz) con k ≈ 0,62-0,68 (calibrar con una puerta: una persona
  ≈ 1,2 puertas). Protagonistas en primer plano ≥ 30 % del alto de pantalla.
- **Tercer plano de profundidad:** `.fg(t, x, y, frac, capa=1.3)` coloca plantas/rocas en coordenadas de PANTALLA (frac del alto de
  pantalla) que se desplazan `capa` veces lo que el suelo y crecen con el zoom^capa. (Con `.en(…, capa)` se salían del cuadro.)
- **Personajes:**
  - `anda(lz, pl, t, "<hoja ciclo>", ta, tb, x0, x1, y, frac, paso, flip, tono, pose=…)`: el cuadro del ciclo sale de la DISTANCIA
    recorrida (`paso` = distancia de un ciclo en altos: caminar 0,95 · correr 1,35 · galope 1,7) → los pies no patinan. Al llegar, cambia
    a una pose de la hoja (`pose="petacatl_hoja/01"`). `desde_antes=False` = no está antes de ta.
  - `paseo(…)`: títere de papel para piezas SIN ciclo (saltitos con |sen| y balanceo ±3°); sirve para aldeanos y para el caballo al paso.
  - `quieto(…, t_in=…)`: respira (escala vertical ±1,2 %) y, si `t_in`, se PEGA con rebote (escala 0,6→1, giro 8°→0, `PF.entra`).
  - `rot=4·sen(3t)` = trabajar (cavar, moler); `flip=True` voltea (los ciclos miran a la derecha).
  - **Rumbo (el usuario, 20-oct):** lo que se desplaza mira SIEMPRE hacia donde va. `MIRA = {pieza: +1 derecha / −1 izquierda}` en
    `escenas.py` (mirar la hoja de contacto de las piezas al recortar: Flow pinta caballos y caminantes hacia los dos lados) y
    `rumbo(pieza, x0, x1, flip)` dentro de `paseo`/`anda`/`desliza` voltea solo; las de frente no van en `MIRA` y su `flip` manda.
- **Pegatina:** borde de papel crema (`BORDE_PAPEL` = 0,65 % del lado mayor, en `_con_borde`), sombra de papel corta (off 4,6, 30 %) y
  **sombra de contacto** elíptica en los pies (`suelo=0.30`): sin ella la pegatina flota. `tono` tiñe la pieza con la luz de la escena —
  noche (0.60, 0.62, 0.92), nublado (0.93, 0.95, 1.02), contraluz de fogata (0.38, 0.30, 0.40)—: sin eso parece pegada encima.
- **Ambiente continuo** (nada quieto > 2 s): `aves` (ciclo de aleteo a 9 cuadros/s, vuelos en pantalla), `PF.humo` (chimeneas y peñol,
  color oscuro para el humo de guerra), `PF.brillo` + `PF.chispas` (fogatas pintadas del fondo y fogatas-pegatina que se encienden),
  `PF.destellos` sobre `PF.puntos_agua` (píxeles turquesa del río), `PF.arena_viento`, nubes-pegatina que derivan, plantas que se mecen.
- **Texto de énfasis** = `PF.rotulo(lz, txt, X, Y, px, t, t0, t1)`: tira de papel recortado con tinta serif que se pega con rebote; nombres
  («PETACATL · señor de Jalpa»), fechas («1540»), conceptos («ENCOMIENDA», «XALLI = ARENA»). Nunca subtítulos quemados.
- Rendimiento: ~0,6-0,8 s por cuadro a 1080p en un proceso; 54 s a 30 cuadros/s con 12 procesos ≈ 6 min.

## 4. Ver el avance (el usuario, 20-oct: «quiero ver el montaje mientras vas armando»)
- **Desde el 20-oct-2026 el 🎞 Montaje del panel también sirve aquí** (el usuario: «la vista previa tarda y no se ve bien; quiero el
  montaje como en Warcraft»): tras cada escena nueva de `escenas.py`, `python fab.py <v> montaje` (borradores 640x360 a 12 fps de las
  escenas que faltan o cambiaron; ~1 s por cuadro y proceso) y avisar al usuario de que abra 🎞 Montaje. Detalle: `docs/panel.md`.
- Para mandarlo al teléfono sigue valiendo `_vivo.py` (desde la carpeta del video, con
  `$env:PYTHONPATH="<video>;C:\FabricaAnimaciones\nucleo"`): `python _vivo.py hoja t1 t2 …` (cuadros 640x360) y
  `python _vivo.py video 12 8` → `previews/montaje_vivo.mp4` 960x540 con `audio/final.wav` si existe (crf 30: ~5 MB, llega al teléfono;
  > 30 MB no). Mandarlo con SendUserFile en cada avance real (1.º mudo con tiempos provisionales, 2.º con voz + Lyria + SFX).
- Antes de la voz: `python _tl_provisional.py` → `timeline.json` estimado (2,55 palabras/s; Dan habló más rápido: 62 → 54 s).

## 5. Voz y música (hallazgos de jalpa)
- **Chatterbox NO aplicaba `FONETICA` hasta el 20-oct-2026** (`tts_gen.py` usaba la grafía real): arreglado (lee `FRASES_TTS` sin
  etiquetas). Nombres nahuas con «tl» final: Chatterbox mete vocal de apoyo («Petacatel»): `ALIAS_QA` para esa variante; la toma que se
  come la ele («Petacati») es la mala. Whisper escribe «Halpa» por «Jalpa» (jota suave): `ALIAS_QA`.
- Lyria 3.5 por API: 0,08 US$ por pieza (crédito recargado el 20-oct). La web de AI Studio ya no da Lyria gratis (403, `key_off`).

## 5b. Miniatura y render (jalpa, 20-oct)
- Miniatura en Flow con la MISMA ficha de trazo del video + escena del gancho + texto pintado por Nano Banana: prompt en
  `videos/jalpa/prompt_miniatura.md` (2/2 bien a la primera; elegir la variante donde la acción tenga sentido: el que huye, alejándose).
- Render 1080p de 3:23 con 12 procesos ≈ 21 min (~0,6 s/cuadro y proceso). Arreglos: `cache_escenas.conservar(...)` de los 68
  segmentos y luego `video --rehacer t0-t1 …` (solo 5 segmentos, 2 min). Lanzar `fab.py` SIEMPRE desde `C:\FabricaAnimaciones`.

## 6. Errores a no repetir
- Primer plano con `.en(…, capa>1)` → fuera del cuadro con el zoom: usar `.fg` (pantalla).
- Rótulo encima de la nube-pegatina: texto y cielo en zonas distintas.
- Toma que empieza vacía hasta que entra el personaje (encomienda a los 29,5 s, adelanto nocturno a los 7 s): que el personaje entre
  con el arranque de la toma o ya esté. Cielo nocturno sin gente: guerreros a contraluz junto a cada fogata nueva.
- Personaje que avanza de espaldas a su rumbo (jalpa: Hidalgo y Mendoza a caballo, Santiago; `flip` puesto a mano «por variedad»
  sin mirar hacia dónde pintó Flow la pieza): se ve en el montaje → `MIRA` + `rumbo()` (§3).
- Orden de dibujo = profundidad: lo LEJANO (y menor) se dibuja ANTES que lo cercano. En jalpa (x3) la mula lejana se llamaba después
  del arriero y salía encima de su cabeza, flotando. Una pegatina grande en pantalla (`pega`, máscara) no va encima de un personaje.
- Dos personajes que se enciman (campesino detrás de Proaño): repartir x de destino; revisar cada toma en la hoja de 1 cuadro/3 s.
- (tramo 3 de jalpa) `T(…, "un")` casa con «uno» y `"san"` con «santuario»: anclar con n=1 o con otra palabra. Baskervville no
  tiene «→» (sale un cuadro). Los ciclos salen ~25 % más chicos que `frac` (lienzo común con margen): subir el factor. Retratos
  REALES de personajes históricos: `videos/jalpa/_retratos.py` (marco de madera) + `pega()` en pantalla con su rótulo.
- Lyria puede devolver una pieza con un hueco de SILENCIO dentro (144 s = 94 + 26 de silencio + 24): mirar el perfil de volumen
  antes de `armar` y quedarse con la parte buena.
- `python fab.py nuevo --help` crea un video llamado «--help» (no hay ayuda): quitar junctions con `cmd /c rmdir`, nunca Remove-Item -Recurse.
- (asteroide_invisible) Fondos guardados con su variante en el nombre (`espacio_tierra_a.jpg`, `depth/espacio_tierra_a.png`):
  `_fondo_depth` solo probaba `<fondo>_a.png` y el parallax no se aplicaba sin avisar. Desde el 20-oct prueba también `<fondo>.png`.
- La orientación de una pieza se mira en su PNG: la miniatura de `_indice.jpg` engaña (bólido con la cola al revés).

## 7. Fusión con Kurzgesagt (Kuriox, `videos/asteroide_invisible/`, 20-oct-2026)
- Flow pinta fondos y piezas con una FICHA «explicador espacial Kurzgesagt en clave de terror» (navy/índigo/teal + un acento rojo-naranja);
  el código pone los MOTION GRAPHICS de Kuriox encima: `trazo` (máscara cv2 + halo aditivo), `texto` Poppins con halo (en vez de
  `PF.rotulo` de papel), órbitas punteadas, enjambres, conos, retículas, cotas, barras, contadores. Todo en `escenas.py` del video.
- Pantallas dentro del escenario (monitores, pantalla de la sala de crisis): rectángulo del fondo → pantalla con `rect_P` y el MG
  dibujado dentro; al acercar la cámara la pantalla crece «hacia» el espectador (comparador AYER/HOY) con el cuarto y una figura
  en primer plano alrededor: profundidad, no «página web».
- Variantes b de Flow = segundo encuadre del mismo lugar (cheliabinsk_a/b, sala_crisis_a/b): dos tomas seguidas sin repetir fondo.
- Escala real de algo gigantesco (roca de 400 m sobre bloques de 30 m): dibujado por código a pantalla completa (`roca_gigante`),
  no una pieza ampliada. Planos de detalle: `fondo` desenfocado (GaussianBlur 2-3) = profundidad de campo detrás de la pegatina.
- (tramo 3, 20-oct) Luz que inunda un cuarto por el ventanal: NUNCA un rectángulo claro encima del vidrio (no casa con el marco y
  se lee como panel de «página web»); `quemar()` = sobreexposición ponderada por la luminancia × rampa hacia la ventana.
- Calima (aire que tiembla): remap senoidal de ~1 px y longitud de onda corta (`sin(Y·0,11)`); con 3 px los marcos ondulan como vidrio.
- Algo DETRÁS de las casas (el frente de la onda asomando sobre el horizonte): máscara de pantalla desde la profundidad del fondo
  (`lejos_pant`, 1 = lejos) multiplicada por el trazo.
- Texto sobre humo café o cielo claro: `sombra_txt()` (penumbra elíptica difusa) en vez de caja; el rojo sobre café no se lee.
- Gente que tumba la onda: giro alrededor de los pies hasta ~85° hacia donde sopla = queda tendida en el suelo y se lee bien;
  el momento del golpe de cada uno sale de su x (`t_frente + x / v`), igual que las ventanas que revientan.
- Un elemento raro pintado por Flow puede ser narrativo: el orbe oscuro con aro rojo del cielo de `calle_mediodia` hizo de la roca
  que viene casi de frente (se enciende, crece y estalla en el «segundo sol») sin tener que taparlo.
- (cierre, 20-oct) El objeto protagonista de una toma está en cuadro DESDE EL PRIMER FOTOGRAMA (aunque tenue/pequeño) y la frase
  solo lo «enciende»; si aparece cuando la voz lo nombra, el fondo se queda solo ~2,5 s (pasó en s3: la Tierra sin la roca).
- Segmentos de una vista previa vieja: un render completo tras editar el código los depura solo (la firma cambia), pero el
  `--rehacer` de seguridad no estorba. Render de 5:41 con 12 procesos ≈ 35 min + `final` 2 min.
- Miniatura de Kuriox SIN mascota (video de terror): receta de `gravedad_5s` cambiando la mascota por la escena del video (roca saliendo
  del resplandor del Sol hacia la Tierra) + 3 palabras «NADIE LO VIO» + cuenta atrás en píldora; 2/2 bien a la primera
  (`videos/asteroide_invisible/prompt_miniatura.md`). El texto complementa al título, no lo repite.
- Rigor del MASTER: los negros intencionales («Todavía» = corte a negro 1,9 s) se comprueban con `blackdetect` y deben durar < 2 s.

## 7b. Drama íntimo en un pueblo real (taller «La seña», `videos/la_sena/`, 20-oct-2026)
- FICHA «libro ilustrado mexicano contemporáneo» + detalles concretos del lugar en CADA fondo (block sin enjarre, varillas, tinacos,
  lámina, las dos torres del santuario, la carretera 54) = nada «gringo» al primer intento (32 fondos).
- Pieza que trae su mueble o a otro personaje: (1) recorte derivado (`_piezas_extra.py`: sin la mesa) + restaurar el fondo bajo la
  línea del corte para que el mueble PINTADO la tape; (2) primer plano con el corte fuera de cuadro + primer plano desenfocado
  (`desenfocado()`: pieza dibujada en una copia y mezclada con GaussianBlur) que tapa el corte lateral.
- Celular/anuncio/chat = PIL dentro del cuadro (`_cel()` con caché) sobre el fondo desenfocado; el texto «se escribe» por letras.
- Lyria: pedido de > ~100 s sale corto (98-100 s) → tramos ≤ 80 s; no respeta silencios → ajustar `audio/musica.wav` por código.

## 8. Lore oscuro de Warcraft (Crónicas de Warcraft, `videos/wow_darrowshire/`, 20-oct-2026)
- FICHA «cuento oscuro pintado a mano con proporciones de Warcraft» (gris ceniza + verde de peste + azul de luna, UN acento de vela)
  dio 24 fondos y 13 hojas coherentes al primer intento (`_prompts.py`). El pueblo «antes de la guerra» con «Same art style but warm
  and hopeful colours» sale dorado sin perder trazo.
- **Pegatinas REALES del juego** (regla del canal): Wowpedia por `prop=pageimages` / `list=allimages&aiprefix=` → `_reales.py` las
  enmarca como foto de papel (`piezas/reales/`) y hace MEDALLONES ovales de la cara (`piezas/medallon/`) para el árbol familiar.
  Capturas muy oscuras del juego (ruinas, necrófago, muñeca): gamma 0,55-0,8 antes del marco.
- **SFX DEL PROPIO JUEGO**: `https://www.wowhead.com/sounds/name:<texto>` responde a curl y trae en la página el JSON con
  `files[].url` (`wow.zamimg.com/sound-ids/live/enus/<n>/<id>/<nombre>.ogg`). Usados: iQuestActivate (misión aceptada),
  BellTollAlliance, AMB_ForestPlagued_Day/Night, GhostAggroA, mGhoulAggro2, MON_OrcSkeleton_Death01, m1hSwordHitMetalShieldCrit,
  VO_HumanMale_Battleshout_01, CampFireLargeLoop… `wow(t, nombre, vol, dur)` en escenas.py → `_sfx_juego.py` → `audio/fx.wav`
  (mezcla lo suma con MEZCLA["fx"]); los ambientes se repiten con fundido cruzado a ~-26 dBFS RMS.
- **Fantasma por código** = la MISMA pieza viva con `tono` azul-verde, opacidad ~0,6 que parpadea, eco desplazado, halo aditivo y
  temblor (`fantasma()`): misma cara viva y muerta sin pedir otra hoja a Flow.
- MG propios del guion: ventana de misión Classic en pergamino con «!» amarillo y aviso dorado «Misión aceptada» (+ el sonido real),
  árbol familiar con medallones reales y lazos de tinta que se trazan, mancha de la Plaga sobre el mapa pintado (ruido de baja
  frecuencia, borde verde, `hueco` = el pueblo que queda aislado), cuenta «I · II · III» de oleadas rechazadas.
- Ciclo de caminar con figuras que se TOCAN (espadas largas): `hoja=N` las parte por valles y salen cortes rectos que se ven como
  cajas. Mirar `_indice.jpg` antes de usarlo; si pasa, títeres de la hoja de poses (`paseo`) o pedir el ciclo «with wide gaps,
  weapons held close to the body».
- Pieza que trae su propio mueble (enfermo EN su cama): no ponerla encima del mueble pintado (sale una cama sobre otra); colocarla
  como un segundo mueble en primer plano.
- Voz incompleta por saldo: `PARCIAL_HASTA = "<escena>"` en guion.py trunca ESCENAS (y LYRIA.tramos) a lo que ya tiene voz, así
  `tiempo`, Lyria, SFX, mezcla y `video --hasta` funcionan; las escenas ya hechas conservan sus tiempos al completar.
- (tanda 2, 20-oct) **10 min de pegatina Flow en UNA sesión** (~85 tomas, 33 escenarios x2 + 11 hojas) caben, pero gastan ~60 % de
  la ventana de 5 h de una cuenta Pro (el contexto pasa de 500 k): mejor 2 sesiones (escenas 3-8 min / 8 min-fin + render).
- Tanda nueva de Flow: `prompts.json` temporal con SOLO las claves nuevas → `paquete` → `_bundle_t2.js` (índices 0..N, la mitad de
  largo para pegar) y luego regenerar el `prompts.json` completo. 1 de 44 prompts salió «Flow está recibiendo un gran número de
  solicitudes» (mosaico Error, sin cobro): se reenvía con `__ins(k)` al final y se baja aparte.
- **Iconos REALES de objetos de misión**: `https://nether.wowhead.com/classic/tooltip/item/<id>?locale=0` responde a curl con `icon`;
  la imagen es `https://wow.zamimg.com/images/wow/icons/large/<icon>.jpg` (56 px). Las páginas `wowhead.com/classic/quest=` NO
  responden a curl: los IDs se sondean por rango (Pamela's Doll 12885 y piezas 12886-12888, Joseph's Wedding Ring 12894, Annals of
  Darrowshire 12900). `_reales.py` los enmarca como icono de WoW (`piezas/iconos/`). Sonidos nuevos: `_bajar_sonidos.py`.
- **MG de interfaz de WoW para el lore** (todo en `videos/wow_darrowshire/escenas.py`, reutilizable): tooltip de objeto con icono
  real (`objeto`), rastreador de misión «- Cabeza: 0/1» (`rastreador`), marcos de unidad con medallón real y barra de vida
  (`marco_unidad`), barra de lanzamiento «Corrupción» (`barra_lanzar`), bolsa de 6 casillas que se llena de reliquias (`bolsa`),
  aviso dorado «Misión completada» (`aviso_oro`), ventana de misión con otro texto y tachada en rojo (Cataclysm), dos líneas del
  tiempo en tinta sobre un libro abierto que vuelven al mismo nudo, alma arrancada / contagio como cintas (`lazo`), escarcha.
- `sacude()` va ANTES de pintar la interfaz: si no, los marcos de unidad tiemblan con la cámara y se salen por arriba.
- Escarcha por código: ruido grueso con umbral duro sale en bloques/manchas; campo de borde + ruido suave (σ 9) y borde blando.
- Código nuevo solo DEBAJO de las tomas viejas → `cache_escenas.conservar(car, range(0, 60), firma_codigo(...))` reaprovecha los
  60 segmentos ya renderizados (0-180 s) aunque cambie la firma del archivo.
- **NOMBRES ÚNICOS por tanda en escenas.py** (bloqueó el MASTER, 21-oct): las tomas leen sus planos (`R4`) y tiempos (`t_lago`) del
  módulo AL DIBUJAR; la tanda 2 volvió a definir `R1…R6`, `t_lago`, `t_antes`, `t_asi` y la Plaga entera salió con los fondos de las
  reliquias (el lago en lugar del mapa). Prefijo propio por escena (`RQ1`, `t_lagoR`) y, antes de renderizar, la comprobación AST
  de nombres de módulo asignados dos veces (`ast.parse` → `Assign`/`FunctionDef` repetidos) debe dar 0. El rigor del MASTER
  incluye también los minutos «ya revisados» en el AVANCE: un render completo los vuelve a dibujar con el código nuevo.
  Prueba barata (21-oct): el render es determinista, así que el tramo del AVANCE aprobado debe salir IDÉNTICO en el MASTER.
  ffmpeg `-t 180 -vf fps=1,scale=160:90 -f rawvideo -pix_fmt rgb24` de los dos + diferencia media por cuadro (numpy): 0,0 = igual;
  entre dos instantes distintos sale ~40. Cualquier cuadro > 6 es un plano que cambió sin querer. 180 cuadros en ~1 min.
- Miniatura de este formato por código (`_miniatura.py`): escenario de Flow + la pieza fantasma + el modelo REAL del juego en foto
  de papel + «!» de misión + 2 palabras que complementan el título.
- (rigor del MASTER, 21-oct) **`paseo()` sigue dibujando la pose al llegar** (`hasta_despues=True` por defecto): si después entra
  `quieto()` con OTRA pose del mismo personaje salen DOS figuras encimadas (dos cabezas). Al cambiar de pose: `hasta_despues=False`
  o el `if t < tb: paseo… else: quieto…`. Grep rápido: `paseo(` del personaje X seguido de `quieto(` del mismo X.
- Interfaz de WoW contra el cuadro: el rastreador (W*0,60, H*0,10) choca con un rótulo centrado arriba (dale `t1` al rótulo antes
  de que entre) y la bolsa a W*0,70 tapa la cara de una pieza grande a la derecha. En las hojas de 640x360 se ve: mirar cada choque.
- Arreglo tras el render completo: editar escenas.py → `cache_escenas.conservar(car, range(0, N), firma_codigo(car, nucleo))` →
  `video --rehacer t0-t1 …` → `final`. Render cortado a medias: borrar los `seg_XXXX.mp4.tmp.mp4` y relanzar `video` (reutiliza
  los hechos). 13:30 de este formato = ~45 min de render con 12 procesos (~16 s por segmento de 3 s).
