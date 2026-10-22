# Estilo boceto + guache con mapa (Cronopapel)

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Estilo boceto + guache con mapa, plano secuencia y cambios de escena procedurales (ejemplo: `videos/historia_china/`, 16:9, 3:10)
- **Mapa** (`mapa.py`): campos de distancia con signo (SDF) sobre una rejilla lon/lat (Natural Earth en `datos/`, dominio público): `M.CAMPOS[época]`. Cada cuadro se interpolan
  dos campos (`core.Territorio`), se proyectan con `M.Cam` y se pintan con `M.pintar` (kernel numba, ~3 ms: relleno plano con grano, borde denso y media luna de sombra).
  `core.Fractura` parte el territorio en celdas de Voronoi (estados, reinos, caudillos) con separación/deriva y las reúne. La cámara es `core.CamPath` (PCHIP + deriva: nunca se queda quieta).
- **Dibujos**: `boceto.Dib(...).dibujar(..., peg=True)` los pone como **pegatinas** (recorte de papel con borde y sombra) sobre el fondo pintado (`Hoja.fondo`). Personajes con `obj_base.persona(...)`;
  objetos por épocas en `obj_a/b/c.py`. Sellos de dinastía con fuente CJK (`core.estampar`, `msyhbd.ttc`). Transformación personaje→personaje: `Reg.morf` (usa `boceto.morfosis`).
- **Coreografía**: `reg.Reg` (actores `Act`, rutas `rio`/`ruta`, `texto`, `contador`, `anio`, `sello`, `romper`, sonidos); una clase `Mundo` (escenas.py) lo dibuja todo en función de `t`.
  Anclas `T(escena, palabra, frase=i)` (OJO: coincide por PREFIJO: «seis» casa con «seiscientos»; usar `frase=`). Tras `from obj_base import *` importar `T` de core (el * trae el `T` de trazo).
- **Cambios de escena procedurales** (`trans.py`): barridos SDF pintados con el mismo pincel (tinta, pincel, papel, portal, puntos, rollo, ola, persianas) centrados en el hueco de silencio entre escenas;
  lo de la escena anterior desaparece en el pico de cobertura (`Reg.fin_de`). Debajo el mundo es continuo: no hay cortes. El usuario pidió exactamente esto: sin cortes duros, sí cambios de escena procedurales.
- **Duración**: `DURACION = N` en guion.py reparte la holgura entre escenas (BPM 108-132); falla si voz+márgenes > N. Voz con Dan ≈ 3,1 palabras/s en este guion (526 palabras ≈ 169 s).
- **Nombres propios** que Whisper escribe distinto (Zhou→Chou, Qin→King, Gengis Kan→Genghis Khan): `ALIAS_QA = {"variante": "canónico"}` en guion.py.
- **Lyria**: `nucleo/lyria.py --n 2`, elegir por correlación de energía con la intensidad pedida, `--usar k` (ahora alarga con atempo hasta un 12 % si es más corto que el video).
- Prueba rápida: `./run.sh _prueba.py t1 t2 ...` (hoja en `previews/hoja.jpg`). Render ≈ 7 min con 8 procesos (0,1-0,4 s/cuadro).

## Versión 2 (4-oct-2026, `videos/historia_espana/`) — EL EJEMPLO A COPIAR desde ahora
Mejoras del kit (copiar `mapa.py`, `core.py`, `reg.py`, `escenas.py`, `sellos.py`, `coreo_util.py`, `_prueba.py`, `_hojas.py`, `_qa_choques.py` de ese video):
- **Relieve real bajo el guache**: rejilla "eu" con NOAA ETOPO1 (`nucleo/datos/relieve_eu.npz`): sombreado del relieve, color por altitud, cumbres claras,
  mar con profundidad y ríos calculados del relieve (grosor por caudal). Los territorios dejan ver el relieve (`luz`).
- **Proyección de Mercator y dos rejillas** ("eu" detallada y "am" del Pacífico a Iberia, longitud desenvuelta): `R.rejilla(t, "am", dur)` funde una en otra
  mientras la cámara se aleja (Colón cruzando el Atlántico); con `dur=0` cambia bajo un barrido. Volver SIEMPRE a "eu" al acabar lo de América.
- **Capas de territorio simultáneas** (`R.terreno(t, campo, color, dur, capa=k, rej=...)`): reinos que conviven (Reconquista, Guerra Civil). Se pintan por número de capa.
- **Fronteras naturales**: los polígonos históricos se subdividen y ondulan con un ruido que depende solo de (lon, lat) (`_mano`), así los vecinos encajan.
- **Fractura por fronteras reales** (`CELDAS_PAISES`): el imperio se rompe en los países de Natural Earth; `fijas=` deja quietas las celdas que no se independizan;
  `colores` puede ser función (t, i) para recolorear (1898).
- **Sellos con emblema dibujado** (`sellos.py`) en vez de letras; se estampan abajo a la derecha (casi siempre mar) y vuelan a la fila superior.
- Campos en int16 y en px de pantalla (bordes y sombras iguales a cualquier zoom); contornos de tinta sin la raya recta del borde del cuadro.
- **Control de choques** `_qa_choques.py`: textos fuera de cuadro, texto/texto, texto/personaje, cosas bajo el contador o los sellos. Correrlo antes del render.
- Revisión: `_hojas.py 3` (todo el video cada 3 s) y luego cuadros a tamaño completo.
- **Fundido entre rejillas sin huecos (4-oct-2026, el usuario lo vio en gancho y en Colón):** "eu" solo abarca 43° de longitud; en cuanto la cámara sale de ella
  hay papel vacío. `escenas.cobertura(cam_e)` calcula qué parte de la pantalla cae dentro de "eu" y, fuera, manda "am" (`wp = max(w, 1 - cobertura)`; borde que
  se desvanece ~80 px). Además, empieza el fundido antes de que la cámara abandone Europa, y revisa con cuadros a tamaño completo CADA fundido (uno cada 0,3 s).
- **Grupos que marchan juntos = `coreo_util.formacion(k, n, ancho)` (4-oct-2026):** 3 `andar` con rutas separadas solo décimas de grado se encimaban al acercarse
  la cámara (montón de trazos negros: legionarios, carabelas, soldados franceses…). Pasa `off=formacion(k, 3, ancho_px)`: separación fija en pantalla, escalonada.
  Revisa los grupos con una tira de cuadros cada 0,5 s (se ven separados al salir y fundidos al llegar).
- **La fuente del boceto no tiene «→»** (sale un recuadro «▯»): dibuja la flecha (`obj_b.flecha()`) o escribe con palabras. Comprueba cada símbolo no alfabético.
- **Cuadros lisos de un solo color en las hojas** pueden ser el punto medio de una transición procedural (`portal`, `ola`, `rollo`…, `R.trans`): mira la tira de 0,5 s antes de darlo por defecto.
- **Revisión del MASTER:** `ffmpeg -vf fps=1/3,scale=960:540,tile=2x3` toma cada cuadro a mitad de cada tramo de 3 s (t = 1,5 + 3k), no en t = 3k: extrae el cuadro exacto con `-ss`.
- **Ríos en rejillas envueltas:** un río que cruza la costura de longitud (60° E en "am") se proyecta con salto de 360° y se dibuja como una recta a lo ancho del mundo
  (raya azul sobre España a 42,2° N). `mapa._cortar_costura` lo parte al cargar. Si cambias el recorte de longitud de una rejilla, vuelve a buscar saltos (`nat(lon)` con |Δ| > 180°).

## Versión 2.1 (11/12-oct-2026, `videos/historia_egipto/`) — Egipto rehecho: UNA rejilla, valle verde y DENSIDAD
El usuario devolvió la v1 de Egipto: «tiene errores… está muy pobre en elementos». Se rehízo con el kit v2 y estas reglas (copiar de Egipto
para países fuera de Europa; de España si hacen falta dos rejillas):
- **Una sola rejilla Mercator** (`REJ = {"eg": Rej("eg", 18, 50, 42, 8, 60.0)}`), `PXDEG_REF` = la suya, `core.ZREF = 2.5`. Relieve: NOAA ETOPO1
  por ERDDAP (`https://coastwatch.pfeg.noaa.gov/erddap/griddap/etopo180.nc?altitude[(lat0):1:(lat1)][(lon0):1:(lon1)]`, ~8 MB para 34°×32°).
- **Ríos de Natural Earth**, no del relieve: en el desierto el D8 inventa uadis. Los tramos del Nilo se encadenan con `coreo_util.nilo()` y
  `tramo(P, a, b)` para que barcos y caminantes vayan SOBRE el río real. Lagos = agua en la base; un lago moderno (Nasser) = capa de agua
  (`CAPAS_AGUA`) que se llena en su año.
- **Valle verde** (`M.CAMPOS["valle"]`: franja de 0,19° del río + Delta + El Fayum) pintado en la base: es la «franja verde rodeada de arena».
- **Territorios translúcidos y según el zoom**: alfa 0,86 de lejos → 0,36 de cerca (z > 8) y contornos que se atenúan igual; así los primeros
  planos muestran paisaje (valle, desierto, relieve) y el reino solo lo tiñe. Antes, de cerca, todo era una mancha de un color.
- **`core.BIG = 320`**: con 1600 (España) las franjas finas no «crecían», aparecían de golpe al final del fundido.
- **Rótulos de mapa girados** («RÍO NILO», «MAR ROJO»): `mapa._mascara_rot` agranda el lienzo antes de girar (si no, se recortan en letras sueltas).
- **Densidad mínima** (lo que pidió el usuario): en CADA frase entra al menos un dibujo nuevo y se mueve algo (carros por rutas, barcos por el
  río, ejércitos en formación, fracturas de reinos, contadores); ningún tramo > ~1,5 s con el mapa solo. Personajes en pantalla a izquierda
  (x≈330) y derecha (x≈1600) con su nombre encima; objetos al centro; lugares con punto + rótulo. ~150 dibujos para 5:40.
- **Dibujos**: `obj_eg1.py` (tocados para `persona`: nemes, coronas blanca/roja/doble, khepresh, Nefertiti, buitre… y `pers(…, barba=)`:
  la barba del kit tapaba la boca y el peinado «pelo» del kit tapaba los ojos como un antifaz), `obj_eg2.py` (monumentos, objetos, dioses con
  cabeza animal quitando la cabeza redonda con `_sin_cabeza`), `obj_eg3.py` (caballo de 4 poses, carro de guerra con conductor, camello, jinetes,
  barcos de cada época). Hoja de control: `./run.sh _hoja_dib.py obj_eg1`.
- **SFX**: `coreo_util.ga/pa/andar` ya NO suenan por defecto (regla «SFX repetidos, no»); cada sonido se pone a mano donde significa algo.
  **Desde el 22-oct-2026 los videos nuevos declaran `SFX_ELEVEN` en guion.py** (ElevenLabs/biblioteca, con variantes, sin
  repetir lo que el canal ya oyó): el sintetizado sonaba idéntico en los 8 videos del canal (`reloj_rapido`, `whoosh`, `pop`,
  `bling`, `campana`…). Receta: `docs/musica_biblioteca.md` § «SFX en los videos dibujados por código».
- **VOZ NUEVA (el usuario, 22-oct-2026): ElevenLabs «Alberto Rodríguez»** (latino neutro, serio y narrativo),
  `VOZ = dict(motor="elevenlabs", voice_id="l1zE9xgNpUTaQCZzpNJa", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)`,
  con corchetes de actuación y escritura normal (sin fonética; `docs/voz.md`). Dan (Chatterbox) queda para los videos viejos.
  Elegida entre 8 candidatas con la misma frase (casting en el artifact «Narrador de Cronopapel»).
- **Anclas por prefijo**: «corona» casa con «coronan», «cinco» con «ciento cinco» → `T(e, palabra, frase=i)` siempre que la palabra se repita.
- **Bordes de la rejilla**: la cámara no sale de la rejilla; un lugar a ~1° del borde (Pela, 40,8° N con la rejilla hasta 42° N) solo se ve acercando.
- Si la voz cambia en alguna frase, la música Lyria se conserva: **no correr `fab.py <v> musica`** (pisa `audio/musica.wav` con la procedural);
  basta `sfx` + `mezcla`.

## Versión 2.2 (22-oct-2026, `videos/historia_eeuu/`) — cámara con PARADAS y un video de 6 min en una sesión
Kit de México con rejilla "us" (Pacífico-Atlántico, 44 px/°: todo el país cabe a z ≈ 0,74). Lo nuevo (copiar de EE. UU.):
- **Cámara por paradas** (`coreo_util.para(R, ta, tb, lon, lat, z)` y `foco(R, ta, tb, CI[...], z)`): la cámara se DETIENE sobre el lugar mientras
  se habla de él y viaja entre paradas. Con claves sueltas (una por palabra) la cámara nunca llegaba: los dibujos anclados quedaban en el
  borde o fuera (Washington, Fort Sumter, Montgomery). `foco` deja el lugar ~140 px por DEBAJO del centro para que los monumentos que crecen
  hacia arriba no toquen el título.
- **Claves que se pisan entre escenas** (`escenas._sin_solapes`): la última parada de una escena (FIN + 0,6) caía después de la primera de la
  siguiente (INI − 1): PCHIP ordenaba las claves y la cámara iba y volvía por todo el país. Ahora la clave sobrante se adelanta o se quita.
- **Fractura por estados reales** (`R.romper("estados", ...)`): `core.Fractura` usa n = 49 (48 estados + 0 = fuera; `fijas=(0,)`).
  Sirve para «13 estados unidos», la Confederación (11), la Gran Depresión (país agrietado) y «50 estados».
- **Mosaico translúcido**: `pintar_celdas(..., alfa=)` recibe el alfa del zoom (antes las celdas iban opacas y de cerca tapaban el relieve).
- **Sello grande a (1720, 400)**, no a 760: abajo a la derecha vive el personaje de la derecha (x ≈ 1620) y chocaban.
- **Dibujos en paralelo**: tres subagentes (personajes / objetos hasta 1890 / objetos 1860-hoy) con una lista cerrada de nombres y firmas,
  mientras se escribe la coreografía; paleta común en `pal_us.py`. ~170 dibujos en ~10 min. Revisar la hoja `_hoja_dib.py` de cada uno.
- **Cuba y Florida en el borde sur** (lat 22,5): la cámara no baja más; con z ≈ 2 Cuba se ve abajo; nada de rótulos «abajo» allí.
- `_qa_choques.py` avisa de muchos «FUERA» de 0,25-0,5 s cuando la cámara viaja con rótulos de ciudad puestos: quitarlos o acortarlos
  si duran > 1 s; los cortos durante un viaje no se notan.

## Variante VERTICAL sin mapa: Short de ciencia «¿Cómo nació el primer fotón?» (5-oct-2026, `videos/primer_foton/`, 1080x1920, 59 s)
Boceto + guache para un Short: **pegatinas de boceto (tinta que hierve + crayón) sobre fondos pintados a guache**, sin mapa. EJEMPLO A COPIAR para Shorts de Cronopapel/ciencia.
- **Fondos** (`pintura.py`): capas RGBA con margen para cámara/paralaje (`cosmos`, `lienzo`, `mancha` con media luna de sombra, `textura` = vetas de pincel + grano) y efectos dinámicos en uint8 sobre el cuadro (`halo` en anillos planos, `rayos`, `mancha_din`, `ruido_tele`). La cámara (`Ctx.cam` = zoom, dx, dy) mueve cada capa con su factor de paralaje.
- **Kit** (`kit.py`): mascota **Foti** (fotón: sol de rayos + cola ondulada, ~10 caras, variante fría con bufanda), partículas con cara (quark/electrón/protón/neutrón), props (termómetro, olla, interruptor, tele de tubo, bombilla, persona…) y `rotulo()` = letras de papel recortado (Luckiest Guy) con crayón + contorno de tinta + pegatina. Usa `grueso`/`peso` de `T`/`R` de `boceto.py`; las caras se arman con `_cara(ojos, boca)`.
- **LIMITACIÓN de `boceto.Hoja`: no hay orden de capas** (tintas y crayones se acumulan; las pegatinas se ven a través unas de otras). Solución en `escenas.Ctx.capa`: cada dibujo se pinta en una hoja aparte y se copia encima de la principal tapando lo de abajo. Todo va por `C.pon` / `C.foti` / `C.rot`.
- **Estructura:** una función PURA del tiempo global por escena (`@escena("id")` en `coreo_*.py`), anclas `T("escena", "palabra")`; cambios entre escenas = mezcla con la escena vecina bajo una máscara pintada (iris/pincelada con borde crema) en `escenas.cuadro`. Cuadro ≈ 1 s; render 59 s ≈ 22 min con 12 procesos.
- Gancho de Short: en t = 0 ya hay imagen completa (persona + sol de rayos + rótulo «LUZ DEL BIG BANG»); la mascota entra en la 2.ª frase; el final repite el arranque (bucle) con CTA «¡SÍGUENOS!».
- Revisión: `.\run.ps1 _prueba.py t1 t2 … -f` (cuadros a tamaño completo) y, sobre el MASTER, `ffmpeg -vf fps=1/3,scale=360:640,tile=7x3`.

### Motor compartido para Shorts (5-oct-2026): `nucleo/sh_motor.py`, `sh_kit.py`, `sh_props.py`, `sh_pintura.py`, `sh_util.py`
Los 5 Shorts de ciencia de Kuriox (`platano_radiactivo`, `luna_se_aleja`, `peso_nube`, `dedos_arrugados`, `cielo_azul`) usan el motor de `primer_foton` MOVIDO a `nucleo/` (primer_foton conserva su copia):
- Cada video aporta: `guion.py`, `coreo.py` (una función `@escena("id")` por escena, anclas `T("escena", "palabra")`), `escenas.py` mínimo (`M.CAMBIOS.update({...})` + `import coreo`), `sonidos.py` (`return M.sonidos_auto()`), `_prueba.py` + `run.ps1`.
- `sh_props.py` = catálogo de dibujos de boceto reutilizable (plátano, trébol, detector, diente, Luna, Tierra, astronauta, elefante, nube, gotita, mano con yemas lisas/arrugadas, neumático, cerebro, ojo, prisma, Marte…); `sh_hoja.py` pinta la hoja de props.
- **SFX automáticos** (`sonidos_auto`): se recorre la coreografía sin dibujar (modo `REC`) y cada `t_in` de pegatina/rótulo genera su pop/bling/whoosh/plop; se cachea en `sfx_auto.json`.
- Obligatorio: `TRANSICIONES = [("continua", 0.1)] * N` en guion.py; sin eso `render` añade transiciones aleatorias (glitch, zoom).
- Pipeline por video: `_pipe_short.ps1 -v <video>` (sfx → Lyria 2 candidatos y `--usar 2` → mezcla → video → final → verificar); cola con `_cola.ps1`. Voz con `fab.py <v> voz --seeds 1 2` (2 tomas bastan si hay CPU/GPU compartidas).

## Dibujos en Flow en vez de por código — ESTÁNDAR DEL CANAL desde el 22-oct-2026 (el usuario vio `historia_jalisco`: «me gusta. Haz así los próximos Cronopapel»)
Todo video nuevo copia el kit de `videos/historia_jalisco/` (mapa del lugar + `pegflow.py` + `coreo_peg.py` + `flow/prompts.py` + `miniaturas.py`). Los `obj_*.py` dibujados por código quedan solo para primitivas (cronómetro, campana, espadas) y sellos.

### Prueba inicial (22-oct-2026, `videos/crono_flow_prueba/`; idea del usuario)
Pregunta del usuario: ¿barcos, personas, animales… se pueden pintar en Flow como hojas de pegatinas (§ `docs/estilo_pegatina_flow.md`)
para hacer Cronopapel más rápido? **Sí, con la referencia como INGREDIENTE.** Resultado: `previews/prueba_mapa.mp4` (8 s sobre un
cuadro real del mapa de Egipto: barco, barca de papiro por el Nilo, camello, carro, legión con ciclo de marcha, faraón).
- **Solo con texto NO se parece** (hojas `01-04_*`): Flow pinta «libro ilustrado» detallado aunque se le pida boceto ingenuo. El
  usuario: «no se parecen mucho al estilo».
- **Con ingrediente SÍ** (hojas `05-08_*_ref`): `ref/ref_cronopapel.jpg` = 12 dibujos reales del kit (`historia_egipto/previews/
  dib_obj_eg1/eg3`, `dib_kit_a`) en una lámina 16:9. Prompt: «Use the attached reference image ONLY as the art style guide… Do NOT copy
  the objects of the reference» + descripción del trazo (contorno negro grueso y temblón, formas geométricas, ojos de punto, sonrisa,
  mejillas rosas, patas de palito, relleno plano con rayitas blancas en diagonal) + «plain flat pure white background (no paper
  texture, no sticker border, no shadows)». El borde crema y la sombra de pegatina los pone el código (`_prueba_mapa.py: pegatina()`).
- Rinde: 4 prompts x2 = 32 dibujos en ~2 min (vs ~150 dibujos escritos a mano por código en Egipto). `pegaflow.py recortar … =8`
  los separó limpios. Hojas mixtas (barcos de cada época, personas de cada época, animales/vehículos) sirven a varios videos.
- Defectos: (1) ciclo de marcha de 7 con el escudo cambiando de lado entre cuadros = parpadeo → pedir «the shield always on his left
  arm, on the far side, identical in every drawing» o usar la variante consistente; (2) carro y carretas salen mirando a la izquierda
  (voltear); (3) el ingrediente se quita tras cada envío (re-añadir; Ctrl+V en el campo = lo más rápido).
- **ADOPTADO en `videos/historia_jalisco/` (22-oct-2026, pedido del usuario «quiero ver 1 video funcionando»).** Receta:
  1. Kit v2.1 copiado de `historia_mexico` (core, reg, mapa, escenas, trans, sellos, coreo_util, obj_a/b/c para cronómetro, espadas y
     campana). La rejilla conserva la llave `"mx"` (así no se toca el kit) pero es la región del video: `Rej("mx", -108.5, -98.5, 25, 17,
     260)` con ETOPO1 por ERDDAP y Natural Earth **10 m** (estados `adm0_a3 == MEX`, Lago de Chapala, ríos por SUBCADENA del nombre: NE
     10 m trae acentos). Con 260 px/° los territorios se aclaran desde z 1,8 (no 3,5) en `escenas.fondo` y en la tinta de fronteras.
  2. Flow en Chrome, 1 ingrediente `flow/ref_cronopapel.jpg` re-añadido antes de CADA prompt (`__addRef`), 9 hojas de 8 (una por época)
     + 4 ciclos (soldado, caxcán corriendo, insurgente, cristero a galope); `flow/prompts.py`. Un prompt de 13 no salió (sin error
     visible): contar las parejas de `Expires` y ver QUÉ hoja falta mirando las imágenes, no por el hueco de tiempos.
  3. 2K en Chrome: menú ⋮ → Descargar → 2K con PAUSAS de 1 s entre pasos (sin pausa el submenú no abre); las posiciones del menú dependen
     de la columna del mosaico (centrar con `scrollIntoView`). Emparejar cada 2K con su hoja 1K por parecido (diferencia media de
     grises a 172x96 ≈ 1 frente a > 20). Al recortar en 2K, el papel BLANCO se parte (periódico) y objetos cercanos se juntan (balón):
     tomar esas piezas del 1K y comprobar que la numeración de `_indice.jpg` no cambió.
  4. `pegflow.py`: `Peg` con la interfaz de `boceto.Dib.dibujar` (pies en (x, y), s = 1 → 400 px; silueta en `hoja.peg` = borde y
     sombra del kit; 3 variantes de temblor con la fase del boceto + respiración; destape en diagonal con u < 1) y parche de
     `Hoja.componer` que pinta las fotos sobre el fondo ANTES del crayón y la tinta (rótulos siempre encima). Ciclos: lienzo común
     sin recortar (si no, bailan). `coreo_peg.py`: atajos por hoja (`PU(7)` = Tenamaxtli…) y `andar_ciclo`/`grupo_ciclo` sobre rutas.
  5. Coreografía igual que siempre (`ga`/`pa`/`R.act`) con pegatinas en vez de `obj_*`. `_tl_provisional.py` permite armar y ver
     cuadros antes de la voz. Miniatura: `miniaturas.py` con las mismas pegatinas grandes sobre el mapa.
  6. Resultado: `historia_jalisco` (4:30, 13 hojas, ~110 pegatinas, en UNA sesión) programado el 3-nov-2026. Ajustes que hicieron falta:
     `core.ZREF = 1.7` (si no, las pegatinas sobre el mapa salen diminutas con la rejilla de 260 px/°); personas en el mapa s ≥ 0,5;
     cada escena empieza con una pegatina en `i0` (si no, 1-2 s de mapa solo tras el barrido); `T(e, "que")` encuentra el «que» de
     otra frase (usar `frase=`); `_qa_choques.py` mide `Peg` por su alto (parche en el video).


### `historia_aguascalientes` (22-oct-2026): primer Cronopapel LARGO (13:05) con voz ElevenLabs, fotos reales y lugares para visitar
Hecho en una sola sesión con subagentes (investigación, mapa, fotos, y la coreografía en 4 tramos en paralelo, uno por archivo).
- **Coreografía en paralelo:** `escenas.py` carga cada `coreo_N.py` con try/except (uno roto no tumba a los demás) y `_prueba.py
  --out=<nombre>` evita pisar la hoja de otro. Brief común en `videos/historia_aguascalientes/_brief_coreo.md` (reutilizable).
  `coreo_peg.py` ya NO carga hojas: cada coreo define sus atajos (si se copia del kit de Jalisco, quitar sus hojas o falla al importar).
- **Fotos reales** = `foto_peg.FotoPeg` (foto impresa con marco, cintas, sombra y crédito en pantalla; misma interfaz que `Peg`;
  `FP.s_para(0.46)`; ~4-5 s). Fuentes pequeñas de época ≤ 0,45 del alto. Copiar `foto_peg.py` + `fotos/` del video.
- **Mapa de un estado pequeño:** 640 px/° con relieve AWS Terrain Tiles (Terrarium z10) + SRTM15+ (ETOPO1 es muy grueso); ríos
  calculados del relieve; `escenas.fondo` con umbral `(cam.z - 2.2) / 3.3`; `core.ZREF = 1.7` se conserva.
- **ERRORES vistos:** (1) la fuente NO tiene «→ ←» ni «≈» (salen cuadros): escribir «A CIUDAD DE MÉXICO»; (2) `T(e, "nombre")` y
  `T(e, "vecinos")` anclaban a otra frase («en nombre de Felipe II»): usar `frase=` con palabras repetidas; (3) un rótulo solo
  ~3 s («una leyenda que se ve…») bloquea: siempre una pegatina; (4) CamPath añade un vaivén de ±190 px: claves de cámara cada
  ~2 s en escenas de capital; (5) la Presa Calles del mapa base se ve antes de 1927 (menor); (6) dato a verificar SIEMPRE con
  INEGI: Aguascalientes tiene 11 municipios, no 12 (la investigación lo traía mal; se regeneró una frase).
- Música: 3 tramos de la biblioteca (Bitácora: apozol/juchipila) + 3 Lyria; LYRIA en 6 tramos (máx. 175 s por tramo, también
  para los que salen de la biblioteca). SFX: 214/247 eventos con efectos propios (SFX_ELEVEN).
