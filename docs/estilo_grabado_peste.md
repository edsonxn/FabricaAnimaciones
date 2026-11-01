# Estilo «grabado de peste» — xilografía / grabado en cobre ANIMADO, en un espacio 3D (horizontal 16:9)

Creado el 14-oct-2026 para `videos/wow_tres_noches/` (especial de Halloween de Crónicas de Warcraft). Kit: `nucleo/grabado.py`
(pintor, trama, figuras, recuerdos, chat) + `nucleo/grabado_3d.py` (cámara 3D y profundidad). Láminas de prueba:
`videos/wow_tres_noches/look.py` (`python _look.py cementerio:1 danza:1 recuerdo:1.5 -f`), muestra en movimiento
`python _movimiento.py` → `previews/muestra_look.mp4`.

## Idea
Danza macabra (Holbein, Durero, hojas volantes de la peste): tinta casi negra sobre papel hueso envejecido. La luz es papel sin
tinta; la sombra es TRAMA de líneas (nunca degradado). Un color de acento por acto en una plancha aparte (multiplica, con mal
registro y densidad irregular, como estampa iluminada a mano): sangre `SANGRE`, plaga `PLAGA`, helado `HIELO`, espectro
`ESPECTRO`, fuego `ORO`. Las líneas HIERVEN 8 veces por segundo (`HERVOR`): nada está quieto aunque la cámara no se mueva.

## Regla de oro: PROFUNDIDAD (el usuario, 14-oct-2026: «no dejan de parecer página web»)
Las primeras láminas eran paneles planos sobre un fondo (marco + reloj + chat en fila) y el usuario las rechazó. Desde entonces
CADA lámina es un ESPACIO 3D con `grabado_3d`:
- `Camara(x, y, z, guinada, cabeceo, f, foco, apertura, bruma, lejos)` — mundo: x derecha, y ABAJO (suelo y = 0), z fondo.
  `kf_camara(t, kfs)` = cámara que se mueve (la cámara SIEMPRE viaja un poco: dolly + giro → paralaje).
- Suelos, muros y techos con `plano(...)`: trama en perspectiva (converge al punto de fuga, se afina con la distancia y se funde
  en tono antes del moiré), `patron=("losas", L)` / `("sillares", L, h)`, `luces=[(x, y, z, radio, fuerza)]` (charcos de luz 3D)
  y `quiebre` (trazo de buril cortado y afilado: piedra tallada).
- Figuras del kit colocadas en el mundo: `sx, sy, zc = cam.pt(X, 0, Z)` y tamaño `s_mundo * cam.k(zc)`; con los pies en el
  suelo y `sombra_contacto` (nada flota salvo lo que vuela: almas, el Ángel).
- `capa_prof(g, cam, zc)` agrupa figuras por bandas de profundidad: desenfoque de cámara + bruma de lejanía.
- PRIMER PLANO oscuro y desenfocado siempre (tumba, esqueleto, barrotes, hierba): enmarca y da escala.
- Objetos planos (el recuerdo, el pergamino del chat, un reloj, una cartela) se pintan en un lienzo `G(t, w, h, alfa=True)` y se
  CUELGAN en el espacio con `estampar(g, lienzo, quad_mundo(cam, centro, U, V, ancho, alto, giro))` (perspectiva + sombra
  arrojada). Una cartela de título cuelga del techo con cadenas (`trazo3d`), no se pega a la pantalla.
- Claroscuro con `iluminar(g, luces)` (lo que no toca la luz se hunde en líneas horizontales que engordan), `haz` (rayos de
  luna/fragua con polvo), `particulas` (polvo, ceniza, brasas, nieve, esporas), `humo`, `sombra_capa` (sombra proyectada de
  una figura por una luz, p. ej. los esqueletos ante la fragua).
- Three.js: el usuario lo ofreció (14-oct). Se prefirió el 3D dentro del mismo motor para que el grabado siga dibujado línea a
  línea; si un escenario necesita geometría 3D compleja (vuelo por una ciudad), entonces sí Three.js + shader de grabado.

## Pintor `G` (grabado.py) — lo esencial
`G(t)` lienzo de papel · `trama(pts, tono, tono2, luz, ang, per, modo, cruz, borde)` (modo `lineal` · `contorno` · `anillos` ·
`rayos`; `cruz=False` = una familia que engorda hasta cerrarse) · `papel` (tapa lo de atrás) · `figura` (papel + trama + contorno)
· `figura_union` (unión de piezas con un solo contorno) · `trazo(pts, w, w1, anchos)` (buril que tiembla) · `macizo` ·
`acento` / `acento_luz` (plancha de color) · `capa(g, desenfoque, bruma)` · `acabado(g, golpe, flash, negativo, oscuro)`.
Figuras genéricas: `cielo`, `luna`, `nube`, `colina`/`perfil_colina`, `pasto`, `niebla`, `lapida`, `reja`, `arbol_seco`,
`craneo`, `huesos`, `esqueleto` + `pose_danza`, `fantasma`, `ala`, `llama`, `cuervo`, `cartela` (filacteria), `marco`,
`rotulo` (se estampa como un sello), `salpicadura`, `recuerdo` (video real pasado a tinta dentro de un marco, con la tinta
comiéndose los bordes), `chat` (pergamino con líneas que se escriben y se corrompen). Lo propio del video (el Ángel, la utilería
de Forjaz) vive en el video, no en el kit.
Rendimiento (16-oct-2026): `GR.fondo` (fondo cacheado por tick) y `GR.sprite` / `GR.esqueleto_baila` (figuras estampadas):
ver § «Rendimiento» → «Cachés del kit». Úsalos desde el primer decorado.

## Video real (yt-dlp) — «recuerdos»
Siempre dentro de un marco grabado (`recuerdo`), nunca a pantalla completa. Los clips de 2005-2008 son 640x480: duotono sepia al
centro (`tinta` 0,2-0,3) y grabado de líneas hacia los bordes; el grabado puro de gameplay movido se vuelve ruido. Elegir
momentos con multitud o una figura grande, sin interfaz (`z`, `cx`, `cy` recortan). El cuadro necesita su PROPIA luz en
`iluminar`, o la oscuridad lo tapa. Crédito en la descripción.
**Más juego REAL (el usuario, 15-oct-2026, al aprobar el avance de `wow_tres_noches`):** además de los «recuerdos», armar
los escenarios con elementos PNG reales del juego (rocas, árboles, personajes de WoW vanilla) y, a veces, personajes reales
como PEGATINAS con borde de papel; tratados con tinta/duotono y colocados DENTRO del espacio 3D a su profundidad, con sombra.
El grabado se queda: es sumar, no reemplazar.
**Cómo (tramo 5 de `wow_tres_noches`, 15-oct-2026):**
- Renders OFICIALES de PNJ con fondo transparente: `python nucleo/wow_png.py "Hakkar" "Ironforge Guard" ...` (busca en
  Wowhead classic con Chrome fuera de pantalla porque CloudFront bloquea curl/headless; caché e índice en
  `nucleo/datos/wow_png/`, hoja `_hoja.jpg`). Son de 300 px: de cerca se ven algo blandos, pero la estampa lo disimula.
- Elementos del escenario: recortes de cuadros del tráiler/clips con `wow_png.recorte_clip(mp4, seg, caja)`
  (transparent_background en la GPU) → `videos/<v>/png/` (cobras de Zul'Gurub); relieves planos recortados a mano.
- `G3.pegatina(g, cam, png, X, Z, alto, t, ...)`: recorte de papel DE PIE en el mundo (mira a la cámara, se mece, sombra de
  contacto + sombra de cartón), pasado a la estampa (duotono + líneas hacia el contorno + buril) y con su TONO real en la
  plancha de color (`color` 0,8: se reconoce el rojo de Hakkar, la barba de un enano). `alza` 0..1 = se levanta como libro
  desplegable (entrada) o cae de espaldas (muerte: `alza = 1 - cae`, luego huesos). `borde=0` = elemento integrado (estatuas).
  En el video: `comun.peg(objs, cam, t, "PNJ" | "png:archivo", X, Z, alto, aura=...)` y `comun.relieve(...)` (imagen plana
  estampada en un muro). Alturas: persona dibujada ≈ 360, enano ≈ 280, gnomo ≈ 200, troll grande ≈ 500.
- Dosis: 1 de cada 3 de la multitud + 1-2 protagonistas reales CERCA por escena (a los lados, sin tapar la acción);
  lejos y detrás de la multitud no se ven (primera prueba: «pocas y chicas»). Cobra encima de otro personaje = amontonado.
Bajar tramos: `yt-dlp --download-sections` con el formato `[ext=mp4]+[ext=m4a]` falla en ffmpeg; con `bv*[height<=720]+ba/b` sí.

## Errores a no repetir (14-oct-2026)
- **MAREO en movimiento** (el usuario: «se ve raro con el movimiento, marea»): (1) una trama fija en pantalla (claroscuro con
  líneas) encima de superficies con trama en perspectiva hace moiré, vetas oscuras que «nadan» con la cámara → `iluminar` ya
  NO dibuja líneas: engorda la tinta existente y lava el tono (aguatinta); (2) tramas de relleno que hierven en superficies
  grandes → `HIERVE_TRAMA = False` (solo tiemblan los contornos, poco); (3) vaivén de la hoja → `vaiven=0`; (4) líneas
  de suelo más finas de ~3 px → se funden en tono antes (`plano`); (5) cámara lenta: ≤ ~40 unidades/s cerca del suelo.
  Comprobación: hoja del suelo en dos cuadros separados 1 s + diferencia media cuadro a cuadro.
- Panel plano sobre fondo tramado = «página web» → espacio 3D (arriba).
- Dos familias cruzadas del mismo periodo y grosor = malla mecánica → la 2.ª es más fina, de otro periodo y solo en sombra
  honda (`tramado` ya lo hace). El claroscuro en líneas HORIZONTALES (engorda las del cielo/suelo, no las cruza).
- Suelo con trazo quebrado horizontal = AGUA; quebrado en dos direcciones = CESTERÍA. La tierra va en líneas horizontales
  continuas (como en las láminas de época) y la escala la dan hierba, piedras y tumbas repartidas en profundidad.
- Anillos de `contorno` en todo un cráneo = huella digital → solo en el lado de la sombra (`tono` 0, `tono2` ~0,4).
- Huesos dibujados uno a uno = manchas negras en las articulaciones → `huesos(g, [(a, b, r), ...])` (tinta de todos, luego papel).
- Fantasma con el brazo a la altura de la capucha = pato → brazos al pecho, mangas caídas.
- Objetos fuera de cuadro: con f = 1500 se ve ±0,62·Z en x; repartir tumbas/figuras dentro de ese cono (`_tumbas()` en look.py).
- El Ángel con la cintura en y = -60 hundía la túnica en el suelo → flota a y ≈ -250.
- Las nubes por arcos encadenados se autocortan → unión de círculos (`figura_union`).

## Montaje de escenas (tramo 4 de `wow_tres_noches`, 14-oct-2026)
- Estructura: `escenas.py` (un `Mundo` que reparte cada segundo GLOBAL a su decorado) + `decor_*.py` (un decorado 3D por
  lugar, con su lista de fotogramas clave de cámara anclados a palabras) + `fig.py` (figuras propias) + `comun.py`
  (`figuras()` agrupa objetos por bandas de profundidad DE CÁMARA, `mancha()` = cambio de decorado con tinta que se derrama y
  se retira en un silencio, `cartela_colgada`, `recuerdo_colgado`) + `anclas.py` (lo usan escenas y `fx_audio.py`).
- Hoja de prueba propia: `python _prueba.py t1 t2 ...` (paralelo, 640x360 por cuadro) y `--grande t` (1920x1080).
- Cada frase tiene su dibujo: las tumbas brotan con su relieve a «salto/jefe/apuesta» y se hunden antes de lo siguiente;
  los candeleros se encienden a «tres» y crecen a «peor/anterior»; la cartela o el recuerdo real entran a su palabra.

## Errores a no repetir (montaje, 14-oct-2026)
- Funciones diferidas (`lambda c: ...`) en la lista de objetos que leen X, Z u `op` sin capturarlos: se dibujan con los
  valores del ÚLTIMO personaje → capturar SIEMPRE con argumentos por defecto (`lambda c, X=X, Z=Z, op=op: ...`).
- Palmeras cercanas: el penacho queda fuera de cuadro y solo se ven troncos («postes») → en plano medio, más bajas.
- Trazos finos (frondas, hierba) se borran con la apertura de cámara: en exteriores con vegetación, `apertura` 2-3.
- Suelo exterior con `quiebre` = textura de agua: la tierra va sin quiebre (ya estaba escrito; volvió a pasar).
- Sujeto cercano desenfocado (tumbas del relieve, cazador, mercader): poner `foco` en ESE fotograma clave (rack focus).
- Multitud a menos de ~1000 de la cámara tapa el cuadro con figuras enormes y borrosas: gente a ≥ 1000; protagonistas
  a 900-1300; un solo personaje desenfocado de primer plano para enmarcar.
- Recuerdos o estandartes pegados a un muro lateral se ven de canto: colgarlos de cadenas en el aire, girados hacia la
  cámara (`U = (0.9, 0, ±0.44)`).
- Muro o acantilado de fondo que tapa el cielo entero = pared de ruido: perfil quebrado con cielo y montañas encima.
- Banda de figuras delante del monstruo lo tapa: repartirla en dos flancos y dejar libre el centro.
- Cara de frente redonda con trama de anillos = simpática (parecía una morsa): para un susto, cráneo anguloso, ceño,
  ojos rasgados de rendija que arden, filas de dientes y colmillos, sombra desde arriba (`cara_hakkar` en fig.py).
- Las mangas claras sobre una capa oscura parecían carteles: manga del tono de la capa, estrecha.
- Render caído: un `plano` visto de canto (techo con la cámara alta mirando abajo) proyecta una tira de 1 px y
  `np.gradient` falla → arreglado en `grabado_3d.plano` (si la caja mide < 3 px, solo papel). Probar SIEMPRE los cuadros
  de los movimientos de cámara extremos antes del render largo.
- Jumpscare en audio (15-oct): el golpe dentro de `fx.wav` (que entra a `MEZCLA["fx"]` −17 dB) quedaba BAJO la música y
  la Lyria seguía sonando en el «silencio». Ahora `fx_audio.py` escribe los «susto» en `audio/fx_sustos.wav` +
  `audio/sustos.json` ([[apagón, golpe], ...] desde `anclas`) y `mezcla` (genérico) apaga todo entre ambos instantes, saca
  el golpe a `MEZCLA["susto"]` (−9 LUFS por defecto) y devuelve la cama en 1,2 s. Medir con `silencedetect` (≥ 0,8 s).
- Tocar `guion.py` (aunque sea audio: `REVERB_VOZ`) cambia la firma y deja «obsoletos» los segmentos anotados: el
  siguiente `video` los BORRA. Si el cambio no toca píxeles, `cache_escenas.conservar` (botón «conservar» del panel)
  antes de renderizar; para juntar audio nuevo con un avance ya dibujado, ffmpeg directo (concat + final.wav).
- Coste real: 3-5,7 s por cuadro en un proceso (Forjaz con multitud = el más caro); con 12 procesos ≈ 1 cuadro/s en total
  (CPU de 16 hilos) → 3 min de video ≈ 90 min. Lo más caro: `plano` (35 %), `_blend` de figuras, `componer` de las bandas.

## Errores a no repetir (tramos 6-7 de `wow_tres_noches`, 15-oct-2026)
- **Sillares pequeños con `quiebre`** (muros de 110-140 × 50-64) = punteado de «óvalos» que zumba en movimiento. Muros:
  `patron=("sillares", 230, 105)`, `quiebre=0`, `var=0.06`, tono 0.3. El zócalo de las casas igual.
- **Entramado de madera con diagonales y tejados en cuña** vistos de lado en una calle = bosque de rayas negras. Solo postes
  verticales + viga del piso + alero; revoque claro (0.1).
- **Cámara fuera de la sala**: en una sala circular (`plano` en anillo) la cámara debe quedar DENTRO del radio; si no, se ve el
  dorso del muro como mancha negra.
- **Lambdas sin capturar X/Z** volvió a pasar (la pescadora se dibujaba en la cresta de la colina): `lambda c, X=X, Z=Z: ...`
  SIEMPRE, también cuando la lambda está fuera de un bucle (los bucles posteriores reasignan X/Z).
- **Gente/necrófagos a < 1000 de la cámara** tapan el cuadro (muro de figuras borrosas): la acción de cada escena entre 1300 y
  2600; solo 1-2 pegatinas cerca, a los lados.
- **Ladera = `plano` inclinado de lados rectos** = cuña blanca contra el cielo. Una colina es un polígono 3D con la falda curva
  (`falda` con `s ** 1.6`) + cresta irregular + pinos ENCIMA siguiendo la pendiente.
- **El mar tapa lo que está «en» el agua** (el casco del galeón): dibujar barcos DESPUÉS del `plano` del mar.
- **Sustos dibujados a escala gigante con la figura del kit** (el Ángel con s = 11) engordan todas las líneas: caricatura. Los
  primeros planos de susto se dibujan a tamaño de pantalla (`susto4`: capucha, degradado de sombra en la frente, mejillas
  hundidas, pupilas diminutas con ojeras, boca larga). Un yelmo redondo parece champiñón: yelmo de cubo con rendija en T.
- Cráneo con `ojos=1` + rendijas propias = «!» (punto de la pupila del kit bajo la rendija): `ojos=0` si se dibujan aparte.
- Escribir el prompt en Flow con `Locator.type` se corta a los 30 s (prompts largos): `execCommand('insertText')` y `Enter`
  (script de una vez en el scratchpad conectado por CDP al Chrome de `flow_thumb.py`).
- Conservar segmentos de un avance al seguir el video: el decorado nuevo arranca DESPUÉS del último cuadro ya renderizado
  (aquí 2:58,29) y `escenas.py` queda idéntico antes; luego `cache_escenas.conservar(car, ks, firma)` antes del render.

## Rendimiento
**Render completo de `wow_tres_noches` (15/16-oct-2026, 118 segmentos, 12 procesos): 13 h 13 min de reloj, pero ~9,5 h fue la
PC DETENIDA** (ningún segmento terminó entre 21:53 y 07:59: suspensión; `SetThreadExecutionState` de render.py no impide la
tapa cerrada / el botón de suspender). Cómputo real ≈ 3,5 h = **~0,85 cuadros/s ≈ 25 min de render por minuto de video**.
Antes de un render de noche: plan de energía «no suspender» con la corriente conectada y la tapa sin efecto.
Medido 16-oct (1080p, un proceso solo): **~3 s por cuadro** (1-5 s según decorado: selva 5,2, Forjaz 4,0, selección 1,0).
Con 12 procesos cada cuadro tarda ~10,6 s (6 procesos: ~7 s): solo **3,4× de ganancia con 12 procesos**, porque todo son
pasadas de numpy sobre imágenes float32 de 1920×1080 y el cuello es la memoria, no los núcleos.
Dónde se va el cuadro (perfil de 12 cuadros, 16-oct; tiempo acumulado, los % se solapan): figuras de `comun.figuras` (esqueletos/PNJ de la danza) ~35 %,
`G3.plano` (trama en perspectiva por píxel de cada muro/suelo) ~24 %, mezclas `_blend` (~1 250 por cuadro) ~17 %,
`componer`/`capa` ~10 %, `iluminar` + `colina` + `acento_luz` + `acabado` ~20 %; pinos (~13 por cuadro) ~5 %.
Todo se redibuja desde cero en cada cuadro aunque la trama no hierva (`HIERVE_TRAMA = False`) y los contornos solo cambien
8 veces/s (`HERVOR`): ahí está el margen (fondo lejano cacheado, sprites de multitud y pinos). Ideas en § siguiente.

### Cachés del kit (16-oct-2026, APLICADAS en `grabado.py` / `grabado_3d.py`)
`GR.CACHE = False` vuelve a dibujar todo desde cero (comprobado: cuadros **idénticos bit a bit** al código anterior).
- **Fondo cacheado** — `g = GR.fondo(t, clave, [(dibujar(g, tt), firma(tt)), ...])` sustituye a `g = G(t)` + lo primero
  que se pinta. Cada etapa se pinta en el inicio del tick (`GR.t_tick(t)`, determinista) y se COPIA en los cuadros
  siguientes del tick si su firma (px de pantalla: `G3.firma_lejos(cam)` = horizonte, giro, paralaje; o la propia del
  decorado: x de la luna...) cambia < `FONDO_TOL` = 1,5 px; lo cercano firma con `G3.firma_cerca(cam)` (≈ 0,75 px: solo
  cámara quieta, los pies no resbalan). Se cachea el PREFIJO de etapas que cumplen; lo demás, en vivo encima.
  Reglas: (1) cada etapa recalcula su cámara con `C.camara(tt, ...)`; (2) lo que vuela (cuervos) se pinta DESPUÉS, fuera
  del fondo, solo si nunca tapa lo cacheado (en el ciclo del cementerio la Forjaz roja es alta: ahí solo se cachea el
  cielo); (3) mete en la firma todo lo que cambia con t (`100 * revela`, luces que se encienden); (4) **no «corras» el
  fondo cacheado para seguir al horizonte**: las rayas del cielo son fijas en pantalla y temblarían a 8 Hz (probado).
  Ejemplos: `decor_cem.cementerio`, `decor_zg.selva`, `decor_forjaz.forjaz`, `decor_t6.muelle`, `decor_t7._termales` y
  `cementerio_final`.
- **Sprites** — `GR.sprite(g, clave, x, y, s, dibujar(c, ax, ay, s_), caja)` estampa una figura desde un lienzo cacheado
  (uint8, máx. `SPRITE_MAX_MB` = 300 MB por proceso): escala en escalones de 4 % y reescalado exacto al estampar, hervor
  «en tres» (`g.k % 3`), lo fuera de cuadro no se dibuja y lo grande cortado por el borde va en vivo. La `clave` lleva
  todo lo que cambia el dibujo con la POSE CUANTIZADA (`GR.fase_cuant`). Ya lo usan: `GR.lapida` (sin tiempo),
  `GR.esqueleto_baila` (16 poses por ciclo, todos los bailarines comparten), y en el video `fig.persona` (8 poses por
  paso; el halo de contagio se pinta en vivo y el tinte del cuerpo va en la clave; lo que CAE, en vivo), `fig.pino` (el
  vaivén solo desfasa: todos los pinos comparten), `fig.palmera`, `fig.helecho` y `look.angel` (redibujado por tick: túnica
  y alas a 8 dibujos/s; vaivén y posición al cuadro exacto). Un acierto cuesta 0,3-9 ms frente a 8-32 ms en vivo; un
  fallo, ~1,3× lo vivo.
- **Medición** (16-oct-2026, 1080p, un proceso, 40 cuadros SEGUIDOS por tiempo ≈ un trozo de segmento; script en el
  scratchpad de la sesión, mismo método que `_prueba.py`):

  | t (decorado) | antes s/cuadro | con cachés | |
  |---|---|---|---|
  | 20 cementerio | 2,61 | 2,05 | −21 % |
  | 45 selva | 4,21 | 2,97 | −29 % |
  | 100 Forjaz | 4,45 | 4,21 | −5 % |
  | 250 muelle | 2,78 | 2,78 | 0 % |
  | 400 fila (termales) | 2,72 | 2,36 | −13 % |
  | 500 cementerio final | 2,78 | 2,43 | −13 % |
  | **media** | **3,26** | **2,80** | **−14 %** |

  Diferencia de imagen media 0,2-1,4 niveles de 255 (a 640x360); hoja `previews/cache_comparacion.jpg` (antes | con caché
  | diferencia ×4), hecha con `python _prueba.py --sin-cache --out cache_antes 20.1667 45.1667 100.1667 250.1667
  400.1667 500.1667` y lo mismo sin `--sin-cache`: iguales a simple vista; la diferencia es solo el temblor del contorno.
- **Por qué no más**: en este video la cámara NUNCA se para (empujes lentos): el fondo lejano se reutiliza en ~1/3 de los
  cuadros y el cercano casi nunca (aciertos de fondo 48 de 136 en la medición); el muelle y Forjaz son `G3.plano` con
  cámara en marcha (0,8-1,75 s/cuadro) y no ganan. Lo que queda caro: `plano` con cámara en marcha, `capa`/`componer`
  (desenfoque de profundidad, ~0,3-0,45 s), `iluminar` (0,2-0,47 s) y `acabado` (~0,17 s).

### Aligerar el próximo video (propuesta del 16-oct-2026; las dos primeras ya están en el kit, ver § anterior)
- **Planos con la cámara QUIETA** (o que solo gire) en los momentos de multitud: ahí el fondo entero (muros, suelos)
  cuesta una copia. Cámara en marcha = el plano completo cada cuadro.
- **Usar `GR.fondo` y `GR.sprite` desde el principio** (no reconvertir al final): pinos, tumbas, esqueletos y PNJ de fondo
  como sprites; solo 4-6 figuras cercanas con dibujo completo.
- **Menos decorados por minuto**: 19 decorados en 9 min (≈ 3 000 líneas de `decor_*.py`) = mucho código por video; mejor
  8-10 decorados más ricos con varios ángulos de cámara, y pasar las piezas repetidas (pino, tumba, esqueleto) al kit.
- **Fondos a media resolución** con la niebla de profundidad (lo lejano ya va suave) y reescalado.
