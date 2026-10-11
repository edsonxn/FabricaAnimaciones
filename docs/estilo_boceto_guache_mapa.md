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
