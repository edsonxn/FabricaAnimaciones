# Estilo documental de misterio (calco de «Detrás del Enigma»)

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Estilo documental de misterio (ejemplo: `videos/voynich/`, 16:9, ~2 min) — referencia "Detrás del Enigma"
- `ESTILO_VISUAL = "documental"`, `SUBTITULOS = False`. Motor `nucleo/docu.py` (NO usa el Lienzo: todo es `np.float32` (H,W,3) RGB).
  Piezas: `foto_parallax` (foto a pantalla completa con cámara + parallax por mapa de profundidad), `Sprite`/`pegar`/`poner`/`Cam` (láminas 3D con
  sombra: polaroids `polaroid()`, folios `hoja_papel()`), `tablero()` + `pin()` + `hilo()` (corcho con hilo rojo), texto cinético
  (`bloque_texto` + `dibujar_bloque`: cada palabra aparece en su tiempo de voz; `karaoke(fr, i0, i1)` saca los tiempos de `timeline.json`),
  `tag_nombre` (rótulo blanco de nombre), `numero`, `estampa`, `marcador_mano` (círculo/tachado a rotulador), `linea_punteada`,
  `grafica_zipf`/`linea_tiempo` (infografías con datos REALES), `tarjeta_perforada`, `panel_analisis`, `acabado` (gradación, viñeta, polvo,
  grano) y `mezcla_tomas` (fundido/látigo/negro/desenfoque).
- Escenas: una sola clase `Mundo`; cada toma es `@toma(t0, t1, ent=(tipo, dur))` con `f(lz, t)`. Anclas: `T(escena, palabra, frase=i)` (OJO: coincide por
  PREFIJO, "ha" casa con "han"; para palabras ambiguas usar `kar(escena, frase, i0, i1)` por índice). `from escena_base import *` exporta un `D`
  (dibujos): importa `docu as D` DESPUÉS.
- Imágenes SIN clave: `nucleo/imagenes_web.py` (`commons`, `guardar_commons` con licencia y autor -> `creditos.json`; `bing` raspa Bing Images como
  `C:\googleimagenes\index.js`, sin control de licencia). Preferir material real y de dominio público (Commons, Yale IIIF: `collections.library.yale.edu/iiif/2/<id>/full/full/0/default.jpg`).
  Pollinations pide clave (401 sin ella; la clave está en `C:\googleimagenes\.env`, no usarla sin permiso).
- Profundidad: `python ../../nucleo/preparar_profundidad.py foto1 foto2` (Depth Anything V2 Small, ~1,5 s/foto) -> `imagenes/depth/`. Recortes: `rembg` (`imagenes/recortes/`).
- Acercamientos a escaneos: usar la versión completa (`imagenes/folios_hd/`), a 2600 px salen borrosos.
- Rigor: cada dato con fuente en el docstring de `guion.py`; nada de imágenes generadas que parezcan documentos reales; créditos en la tarjeta final y en la descripción.
- Voz: `qa.normaliza` ya convierte números romanos (Whisper escribe "siglo XX", "Rodolfo II"). Nombres raros que Whisper no reproduce ("Beinecke"): evitarlos en la narración
  y dejarlos solo en pantalla; "Athanasius" -> "Atanasio".
- Duración: cada escena se redondea a compases (BPM); ~140 s de voz = 2:40 de video. Para 2 min: ~105 s de voz, BPM 96, GAP 0,36.
- Prueba rápida de cuadros: `python _hoja.py t1 t2 ...` (en la carpeta del video; con `PYTHONPATH=<video>;nucleo`). Coste ~0,5-1 s por cuadro.

### Estilo documental v3 — CALCO del original (leer antes de tocar el texto o el ritmo)
Feedback del usuario (29-sep): la v1 (Baskervville amarillo abajo) "muy normal"; la v2 (Poppins Black Italic gigante amarillo, Impact, muchos golpes, glitches,
64 tomas de ~2 s) "muy rápida, letra muy grande y letras todo el tiempo". Lo que SÍ quiere: la tipografía y el efecto del min 1:00 del original.
Reglas (analizadas cuadro a cuadro del original `Rzkm2XKWRvc`):
- **Texto principal** (`R`): Poppins SemiBold Italic MAYÚSCULAS, blanco, ~88 px a 1080p, 2 líneas centradas, palabra a palabra con fundido (0,3 s), **líneas de escaneo a
  través de las letras**, sombra suave. Sin golpe de escala, sin contorno grueso.
- **Nombres/lugares/cifras** (`S`, `N`): serif condensado (Baskervville Bold x0,70 / Abril x0,72), **Título Con Mayúsculas**, amarillo limón ~98 px, cifras rojas. Preguntas (`Q`): serif
  blanco + "?" rojo grande.
- **Poco texto**: una idea por 5-6 s, solo lo importante; nada de subtítulos continuos.
- **Filtro de película en todo el cuadro** (`docu_fx.cine`): tilt-shift (arriba/abajo/bordes desenfocados), aberración cromática radial, bloom, viñeta fuerte, grano, polvo y
  **líneas de escaneo horizontales (periodo 4 px) sobre todo, texto incluido**.
- **Animaciones**: trazos rojos rectos gruesos que se dibujan y se borran sobre las líneas de la imagen (`trazo_recto`, el "nueve kilómetros" del min 1), línea de medida punteada
  con rótulo cursivo, óvalo luminoso, polaroid de mapa que cae con marcadores amarillo-verde y distancia (`hoja_mapa`: mapa de relieve real de Commons), sellos, fugas de luz de
  color (`mezcla2(..., "fuga")`), mancha de tinta negra, marco de película lateral.
- **Ritmo**: tomas de 2,5-6 s (media ~2,5 s), transiciones suaves (fundido 0,5-0,7 s; tinta/fuga en cambios de tema); nada de glitch/aberración constantes. Video de apoyo real
  (`nucleo/videos_stock.py`: Pexels/Pixabay con las claves de `C:\googleimagenes\.env`, que se leen al vuelo y no se copian) más folios/fotos con parallax.
- **Música**: Lyria (`nucleo/lyria.py`, modelo `lyria-3.5`, endpoint `interactions`): prompt por escenas con tiempos de `timeline.json` y `LYRIA = dict(...)` en guion.py;
  genera 2 candidatos, elegir el que siga la forma de energía pedida y `python lyria.py --usar N` -> `audio/musica.wav`. NO correr la etapa `musica` (procedural) después.
- Pruebas de calibración: `videos/voynich/_cmp.py` (compara lado a lado con cuadros del original), `_hoja.py` (hoja de cuadros).

## Documental de NOTICIA / crimen real (christa_pike, 3-oct-2026, 8 min) — qué se añadió al estilo
Ejemplo: `videos/christa_pike/` (kit propio `kit_cp.py`; tomas en `tomas_a.py`/`tomas_b.py`; `escenas.py` solo tiene `Mundo`). Lo reutilizable:
- **Anclas por PALABRA, no por índice:** `ww(escena, frase, "palabra", nth, sep)`, `pk(escena, frase, "desde", "hasta")`, `INI/FIN(escena, frase)`. Resisten cambios de voz/guion.
- **Material de terceros:** noticias/archivo con `yt-dlp` (`bajar_clips.py`, ≤720p) usados SOLO como extractos cortos con crédito en pantalla (`CRED`) y avisando al usuario del riesgo de derechos; fotos de Commons con `creditos.json`; b-roll libre Pexels/Pixabay (`bajar_stock.py`). `cortes.py` detecta cortes de plano para fijar `ini=`/`fin=` de cada extracto (`F_clip(..., fin=)` congela el cuadro en vez de dar la vuelta al inicio del archivo).
- **Fondos:** `F_clip(banner=0.17)` recorta con zoom el rótulo inferior de las noticias; `F_arch` pone archivo 4:3 sobre su propio fondo desenfocado; `MAPA([(t, zoom, lon, lat)], marcas, rutas)` = mapa de relieve REAL (`hacer_mapa.py`: teselas AWS Terrain + sombreado propio; `mapa_lugares.py`: Natural Earth) con cámara y rutas punteadas; nombres de estados en el propio mapa.
- **Infografías:** `LINEA_ANOS` (eje de años con barra y marcas arriba/abajo), `CRONO` (reloj que se llena), `RELOJ` (hora grande en serif rojo), `TEMPORIZADOR`, `PERSIANAS`, esquemas explicativos rotulados «NO ES UNA IMAGEN REAL» (`F_vena`, `F_ventana_piedra`).
- **Sombra inferior automática** en toda toma con texto (`dibujar` multiplica por `_sombra_inf`) para que el texto principal se lea sobre cualquier imagen.
- **Voz Faraon:** 2,37 palabras/s. Whisper no pasa «treinta y un años» (lo escribe 31 → «uno»): reescribir. Nombres ingleses en fonético (`PRON`) y alias para Whisper (`ALIAS_QA`).
- **Lyria:** el filtro de entrada bloquea al azar (HTTP 400 «content_blocked», incluso con el mismo prompt) y por palabras sensibles («childhood», «dread», nombres propios, ids de escena como «crimen»/«juicio»). Solución usada: prompt neutro («Section k», solo descripción musical) + reintentos + UNA pieza por tramo (Lyria da ~3 min máximo): `_lyria_segmentos.py` genera 3 tramos, los alarga con `atempo` (≤12 %) y los une con fundido cruzado de 3 s en `audio/musica.wav`.
- **Etiquetas (`TAG`) nunca sobre rostros;** comprobar en el cuadro. Estética de noticia: colores fríos y oscuros, tonos `tono=` por toma; si un stock sale casi negro, subir `tono` (1,3–1,6) o cambiar de clip.

### Motion graphics DIBUJADOS propios (feedback del usuario, 3-oct-2026: «faltan elementos, más dinámico, sin reciclar nada, dibuja siluetas, cosas»)
Regla para documentales de noticia/crimen real: **nada de b-roll de stock repetido ni de reciclar el mismo extracto de noticia**; cada frase evoca un motion graphic dibujado a medida. El stock solo sirve de apoyo puntual; lo real (fotos de Commons, archivo de noticias) va como extracto corto, una vez, con crédito.
Kit en `videos/christa_pike/` (copiar a un video nuevo):
- `mg.py`: pintor `P` a media resolución (4x más rápido; el filtro `cine` suaviza) con `poly/circ/elip/linea/polilinea/rrect/glow/haz/texto`; ambientes (`estrellas`, `luna`, `lluvia`, `polvo`, `niebla`, `colinas`, `bosque` (pinos/pelados), `ciudad` con ventanas que parpadean, `suelo`, `vineta_p`, `zoom_p`); **personas-silueta con esqueleto** (`persona(p, x, y_pies, h, pose, color, facing, ropa, pelo)` + poses `pose_caminar(fase)`, `estar`, `sentado`, `escribir`, `manos_cara`, `cartel`, `señalar`, `brazos_arriba`, `correr`; `multitud`, `acostada`, `silueta_sentada_vista_trasera`). Sombra de silueta sobre fondo oscuro: usar un tono un poco más claro (0.03-0.10) o luz de borde, si no desaparece.
- `mg_obj.py`: objetos animados (`reloj` con segundero, `hoja_cal` y `rodillo`, `balanza`, `mazo`+`onda_choque`, `silla_electrica`, `camilla`, `jeringa` que se vacía, `bolsa_iv` con goteo, `ecg`, `ambulancia` con luces, `persianas`/`cortina`/`ventana_obs`, `escritorio_pc`, `vela`, `documento`, `lupa`, `check`/`cruz`, `cerebro`, `engranaje`, `columnas`, `prision` con reflector, `pasillo` en perspectiva, `mapa_us` con estados de Natural Earth, `arco`, `pin`).
- `mg_esc*.py`: una función por escena `@esc("nombre", ini, fin)` con firma de fondo del motor `f(lz, tl, t, dur, ext)`; `F_mg("nombre")` la usa como fondo de un `shot`; `OV(fn)` la usa como extra aditivo. Anclas a la voz por palabra (`ww/pk/INI/FIN`).
- Pruebas: `python _hoja_mg.py nombre:tl,tl otra:tl --out previews/x.jpg` (3 cuadros por escena a 640x360, ~70 ms/cuadro) y `_hoja.py` para el cuadro final con filtro. Mirar SIEMPRE las hojas antes del render largo.
- Coste: cada escena dibujada 60-110 ms/cuadro + filtro `cine` ~0,5 s; el render de 8:15 tarda ~65 min con 8 procesos.

### Tablero de detective VIVO (satoshi_nakamoto, 3-oct-2026, ~14 min) — pedido: «más paneos de cámara, hilos, conectores diferentes, un tablero de detective en constante movimiento»
Ejemplo: `videos/satoshi_nakamoto/` (copiar `tablero.py`, `piezas.py`, `piezas2.py`, `portales.py`, `kit.py`, `coreo_comun.py`, `escenas.py`, `_hoja_rec.py`, `_hoja_portal.py`).
- **Un solo plano secuencia** sobre un corcho infinito (`tablero.py`): textura periódica con mipmaps (`BORDER_WRAP`), luz de lámpara que sigue a la cámara, polvo en primer plano.
  Cámara 3D (`CAM.clave(t, x, y, z, rz, rx, ry, modo)`): Hermite entre claves (nunca se para), `latigo` (barrido con desenfoque de movimiento), `suave` (frena); deriva de mano siempre.
- **Piezas** (`Pieza`): polaroid con foto real o silueta «SIN FOTO LIBRE», ficha a máquina, nota adhesiva, recorte genérico, impresiones REALES (código, hex, white paper),
  gráfica animada con datos propios. Entran volando desde la cámara, caen con sombra según la altura, rebotan y se clavan (`pin` + golpe de cámara). `teaser=(t0, t1)` las muestra antes (flash-forward).
- **Conectores distintos**: `Hilo` (lana roja/azul/amarilla/verde/blanca/negra con catenaria, vaivén al tenderse, `corte=` la parte y las mitades caen; `etiqueta=` ficha colgada),
  `Punteada` (línea de datos con paquetes de luz: correos, transacciones), `Marca` (rotulador: círculos, flechas, taches, subrayados, resaltador), `Cinta`, sellos (`sello_en`).
- **Portales** (fusión con los motion graphics): una polaroid con ventana transparente lleva una escena dibujada (`portales.py`, pintor `mg.P`); `DENTRO(pieza, t_a, t_b, t_c)` acerca la cámara
  hasta que la foto llena la pantalla (entonces solo se dibuja el portal) y luego sale al tablero. Así no hay cortes: corcho → escena → corcho.
- `Lupa` (aumento real del cuadro con distorsión), `Linterna` (tablero a oscuras con haz: gancho), `LUZ_FX` (apagones/silencio), `relleno()` (papeles de fondo oscurecidos: nunca corcho vacío).
- Coreografía por escena en `coreo_*.py` anclada a PALABRAS; textos del estilo v3 con ventana (`TX(fn, t0, t1)`, fundido de salida automático, corte de línea automático en `kit.R`/`kit.S`).
- Revisión: `_hoja_rec.py a..e` (cuadros clave del recorrido) y `_hoja_portal.py`. Coste: tablero 0,3-0,5 s/cuadro + `cine` 0,5 s.
- **Segundo video con el kit: `videos/polybius/` (7-oct-2026, 5:16).** Copiar de ahí si el tema no es Bitcoin: `piezas.py` ya no depende de datos de Satoshi
  (`anio_card`, `vacia_card` «NINGUNA», `icono_card` con pie, `revista` genérica, `hoja_vector`, `relleno` con notas del tema), `portal_base.py` (registro + utilidades,
  para repartir portales en varios archivos sin importaciones circulares) y `_hoja_rec.py t <tiempos>`. Kit temático `arcade.py`: cabinas de frente y de perfil,
  pantallas vectoriales propias, salón de 1981 con neones, jugadores con borde de luz. Lecciones (ESTADO.md del video): las siluetas necesitan fondo más claro + borde
  de luz; el portal se compensa ×1,22 porque `cine` oscurece; el «?» de `Q` necesita aire encima.
- **Sonido del tablero (el usuario, 7-oct-2026):** nada de un efecto por cada pieza. El clic de chincheta (`pin`) se quitó de `tablero.Pieza` y el papel va muy bajo; con 60-70 piezas el mismo sonido repetido cansa. Reservar los SFX para golpes con sentido (sello, látigo de cámara, corte de hilo).
