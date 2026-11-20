# Llamada de domingo — REMAKE ANIME (LogIA presenta) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: logia · APARTE del original (el usuario, 7-nov) · 16:9 · 14:00 · ✅ SUBIDO ZbgBSvK4bLw, programado vie 13-nov 10:00 CDMX
- estilo: ANIME VIVO (nuevo, 6-nov): imágenes de Flow (0 pts) en anime seinen de película + animación limitada por código
  (`nucleo/anime_vivo.py`: bocas por la voz, parpadeos, respiración, recorte con parallax, cámara, polvo/rayos/lluvia/fluor/bloom)
- etapa: ✅ Flow completo (A, B, E) · ✅ MASTER salida/llamada_de_domingo_anime_MASTER.mp4 (14:00, 1080p30, audio final del original intacto; 7-nov ~09:30)
- siguiente: ◐ V2 PEDIDA POR EL USUARIO (7-nov): TODO en anime (los 22 planos ui aún usan fotos realistas del original) y MÁS
  animación 2D en los planos estáticos → ver «## En curso — sesión 4». La v1 está subida (ZbgBSvK4bLw, programada 13-nov).

## Pedido (el usuario, 6-nov-2026)
- «Me gustó mucho el capítulo de Black Mirror de los clones… el guion está perfecto. Remake, lo mismo, pero como no hay puntos
  de Flow para video, cambia el estilo a algo con imágenes de Flow animadas, que se sienta animación real y no fotos. Tú define
  el estilo. Puedes usar las mismas voces, todo.»
- Decisión de Claude: ANIME de drama adulto. El anime ya ES animación limitada (dibujos sostenidos + bocas de 3 posiciones +
  parpadeos + paneos sobre fondos pintados), así que con imágenes + código se ve como anime de verdad, no como diapositivas.

## Plan técnico
- AUDIO = el del original SIN TOCAR: `../llamada_domingo/audio/final.wav` (voces Flow + Eleven, música, fx; 840 s). Labios: audio
  de cada plano en `../llamada_domingo/medios/scene-NNN.mp4`.
- Planos ui (22) = los del original (interfaz por código); si sobra tiempo, rehacer sus fondos de flow/bg en anime y `ui.py`.
- Planos clip/llamada/img (63) → `medios/scene-NNN.mp4` 1080p30 con anime_vivo; ensamblar 85 tramos + final.wav = MASTER.
- Flow: proyecto del original https://flow.google.com/project/5ccd1e3d-d989-48db-9b64-58e40811b4e4 (navegador integrado).
  `flow_anime.py A|B|E` = prompts; `flow/uuids.json` {clave: [uuid, nombre]}; descargas con `../llamada_domingo/flow/_bajar.py`.
  Inyección: helpers `__ing/__ingU/__txt/__prep` pegados por javascript_tool (fetch a localhost y popups NO funcionan en Flow);
  envío = clic REAL por ref en «Iniciar generación»; batch de 11 prompts (prep + clic) por browser_batch.
  Edición (boca/ojos): ingrediente = la base por uuid (opción del buscador con su miniatura), prompt «Edit this exact image…
  ONLY change: mouth open…» → x2 da DOS aperturas (media y abierta). Probado en flow/prueba (r1a + r1_boca1/2 + r1_ojos1/2).
- Prueba: previews/prueba_005.mp4 (10 s, Ramón) mandada a la tele con pregunta (6-nov ~16:45).

## En curso — sesión 4 (7-nov ~10:30-11:30, cortada por contexto) — V2
Pedido del usuario: «el video mantiene muchas imágenes del original; la idea era sustituir todo por el nuevo estilo y animar
todo en 2D; hay escenas MUY estáticas que hace falta animar más con 2D».
- ✅ Los planos ui (22: notif, keynote, anuncio, onboard, montaje, dashboard, noticiero, historial, timbre, final…) salen de
  `../llamada_domingo/ui.py` (`render_pieza(uid)`), que solo usa FOTOS FIJAS + interfaz por código: `foto("bg/x")` =
  ../llamada_domingo/flow/bg/*.jpg (23 fotorrealistas, hoja flow/_hojas/bg_original.jpg), `esc/x` = flow/esc/*.jpg,
  `medios/scene-045|050` (.jpg) y `cara(quien)` con cajas en píxeles de esas fotos.
- ✅ ENVIADAS a Flow (~11:00-11:25) las 23 ediciones anime (x2) de flow/bg: original como ingrediente (buscado en la galería
  por su prompt, variante elegida por firma 8x8) + retrato anime de Daniel (laptop_noche, fiesta, oficina_dia,
  telefono_puerta) o Ramón (mon_1..5). Prompt: «Redraw the first image as a hand-drawn 2D anime… Keep EXACTLY the same
  composition, framing… blank screens stay blank…». Helpers en flow/_helpers_ui.js. Una generación es BASURA (key_valeria +
  key_publico juntas con el prompt doble): descartarla. key_sala ya se vio bien.
- FALTA, en orden:
  1. Recoger las ~48 imágenes nuevas (las más recientes de la galería, src flow-content firmado → curl) y asignarlas POR
     CONTENIDO a su original (firma/diferencia contra flow/bg); elegir variante y guardar en flow/bg_anime/<nombre>.jpg AL
     TAMAÑO DEL ORIGINAL (ui.py usa coordenadas en píxeles: quads de teléfonos/pantallas y cajas de caras). Hoja para mirar.
  2. `ui_anime.py`: importar ../llamada_domingo/ui con `_ruta_img` redirigido (bg/x → flow/bg_anime/x.jpg; esc/x →
     flow/a/esc_x_a.jpg redimensionado; medios/scene-045|050 → cuadro de medios/scene-045|050.mp4), `cara()` → retratos
     flow/a/pj_*_a.jpg (como `envolver_llamada` en tomas.py), MEDIOS/PREV/CACHE → este video; render de los 22 planos ui a
     medios/scene-NNN.mp4. Revisar en hoja que teléfonos/pantallas sigan alineados.
  3. `tomas.ensamblar`: los planos ui desde medios/ (ya no recortes del MASTER original).
  4. MÁS ANIMACIÓN 2D en los planos estáticos (movimiento medio por plano, menor = más quieto): 021 1.4, 049 1.8, 017 1.8,
     081 2.0, 033 2.3, 052 2.6, 057 2.7, 077 2.7, 041 2.7, 061 2.7, 076 2.9, 073 2.9, 056 3.1, 070 3.1, 004 3.2, 036 3.3,
     023 3.3, 005 3.3, 044 3.4 (los mejores > 7: 026, 011, 031, 047, 032). Idea principal: POSES EXTRA con Flow (editar la
     misma imagen: baja la cabeza, gira, mueve la mano, se lleva el teléfono a la oreja…) y cambiarlas como cels en las
     pausas del audio (animación limitada de verdad), + movimiento secundario por código (pelo/ropa, manos, vapor, luces
     de autos, péndulos, gotas) y cámaras con dos tiempos. Ampliar `nucleo/anime_vivo.py` y doc.
  5. Re-render de lo cambiado (PROCS=4), hojas, `python tomas.py ensamblar` → MASTER v2 → `fab.py tele video llamada_anime
     master` en 2.º plano → `fab.py avisar`.
  6. YouTube: la v1 (ZbgBSvK4bLw) está programada vie 13-nov 10:00. PEDIR PERMISO para borrarla (o dejarla privada sin
     fecha) y subir la v2 en el mismo hueco (`yt subir llamada_anime logia private --publicar 2026-11-13T16:00:00Z`);
     actualizar canales/logia.json y BITACORA.
- Ojo: el primer `<input>` de Flow es el NOMBRE del proyecto (lo renombré sin querer y lo restauré a «nov 06 - 13:12»).

## En curso — sesión 3 (7-nov ~08:50) — ✅ MASTER
- 63/63 planos (hojas flow/_hojas/hoja_render1-3.jpg, hoja_master.jpg). Negros a 259, 641, 775 y 830 s = planos ui del
  original (rótulos y créditos), iguales que en el original. 071: Lucía en uniforme en vez de luto (sin corregir).
- El render de la noche murió en 7/63 (reinicio). Relanzado `PROCS=4 python tomas.py >> flow/_render.log` (14 GB libres;
  con 6 se quedó sin memoria). Los `medios/*.tmp.mp4` son restos rotos: se sobrescriben solos.

## En curso — sesión 2 (6-nov ~17:40, cortada por contexto a 180k)
- ✅ Fase B generada y BAJADA: 122 imágenes en flow/b/<scene>_<0|1>.jpg (lista firmada en flow/_listaB.txt; el orden se
  comprobó con los Expires crecientes por par). Hojas de revisión en flow/_hojas/hoja_B0..5.jpg (C:, no previews).
- ◐ Variantes elegidas: flow/_elegidasB.txt (002…050, 36 planos, mirando hojas B0-B2) y ya registradas en uuids.json
  (`flow_anime.py reg flow/_regB.txt`). FALTA mirar hoja_B3..B5 (051…069b, 25 planos), añadir sus líneas a
  _elegidasB.txt, regenerar _regB.txt (snippet: L de _listaB + elegidas) y volver a `reg`. Criterio: cara más grande
  en los planos con diálogo; personajes correctos.
- ✅ 61/61 variantes elegidas y registradas (`flow/_elegidasB.txt`, uuids.json 84 claves). ✅ Fase E ENVIADA (~18:45):
  97/100 ediciones (50 tomas × boca/ojos, orden = flow_anime.quien_habla()); NO salieron 019_boca, 029_ojos, 032_boca
  (tile no encontrado; 3 envíos sin ingrediente generaron basura con prompt «.» → ignorar). Reenvíos al final de la cola
  (029_ojos→ no; 032_ojos, 078_boca, 078_ojos sí, van DESPUÉS de 069b_ojos). ✅ RECOGIDO (~19:15): 210 bajadas a flow/e_raw/r###.jpg (lista flow/_listaE.txt) y
  asignadas POR CONTENIDO a flow/e/<scene>_<boca|ojos>_<0|1>.jpg (50 bases; 18 basura descartadas; 019 y 032 solo ojos,
  029 solo boca, 043 un solo par tomado como boca — si el render muestra ojos/boca cambiados en 041/043, revisar).
  ✅ `tomas.py` escrito y probado (014 con corte entre hablantes, 004 videollamada con interfaz de ui.py y miniatura
  anime). ~19:45 relanzado con `PROCS=3` (con 6 x264 se quedó sin memoria; planos img usan
  final.wav del tramo para la envolvente). ✅ docs/estilo_anime_vivo.md + línea en CLAUDE.md. Antes: `PROCS=6 python tomas.py` (log flow/_render.log; salta lo que ya esté en medios/). SIGUE:
  `python tomas.py ensamblar` → salida/llamada_de_domingo_anime_MASTER.mp4 → tele master → avisar. (Texto viejo:) recoger los tiles nuevos (más
  recientes que 069b de B) → identificar cada edición POR CONTENIDO (diferencia con su base de flow/b, no por orden) →
  bajar a flow/e/<scene>_boca_<0|1>.jpg y _ojos_<0|1>.jpg. Ingrediente de B = tile de la galería → «Más opciones» → «Añadir a la
  petición» (`__ingT(uuid)`: scroll a la y guardada en `__NEW`); el buscador de ingredientes NO sirve para B (miniaturas
  /asb/ sin uuid). Recoger E igual que B: tiles nuevos con src flow-content → lista → `_bajar.py` a flow/e/.
- ⚠ DISCO E: se colgó a las ~17:30 (ls de previews/ no responde; previews, audio, salida, segmentos y voz de este video y
  del original son junctions a E:). Revisar eventos del sistema antes de escribir ahí; si sigue mal, trabajar en C:
  (medios/ y flow/ están en C:). El audio final del original vive en E: (../llamada_domingo/audio/final.wav).
- NOTA ingredientes (fase E): las variantes nuevas SÍ tienen src flow-content firmado; las de la fase A y las imágenes
  viejas usan /asb/. `__ingU` por token asb sirve para A; para las de B, buscar la opción cuyo img src incluya el uuid
  (el helper viejo de _helpers.js). El `data-media-id` del tile = uuid.
- Videollamadas: los planos `llamada` (004, 006, 042, 044, 052, 061, 076, 078) del original llevan interfaz de
  `../llamada_domingo/ui.py llamada(scene)` sobre previews/originales/<scene>_crudo.mp4 → reutilizar con MEDIOS/PREV/
  CACHE apuntando a este video (la miniatura `cara(quien)` es foto realista: cambiarla por el retrato anime pj_*).
- Diálogo con 2 hablantes en un plano (014/014b, 032/032b, 069/069b): tiempos por frase en
  ../llamada_domingo/flow/_whisper.json → cortes de Toma.
- ✅ Fase B ENVIADA completa (61 prompts × 2, Nano Banana 2.1) en el proyecto (el dominio ahora es flow.google.com).
- ⚠ Flow CAMBIÓ: las imágenes ya no son URLs firmadas de flow-content (ahora `flow.google.com/asb/<token>`, piden sesión;
  curl no sirve). El uuid está en `img[data-media-id]`. Helpers nuevos en `flow/_helpers.js` (+ `__MAP` uuid→token de la
  galería, recorriendo `.cdk-virtual-scrollable` por scrollTop; `__ingU` busca la opción por el token asb).
- DESCARGA nueva: en la página `fetch(asb=s0)` → blob → `<a download>` → el navegador integrado deja el archivo COMPLETO como
  `~/Downloads/<uuid>.tmp` (no lo renombra). Se marca cada blob con `##FAB:<nombre>##` al final (JPEG lo ignora) y
  `flow/_recoger.py` lo saca de Descargas a flow/<carpeta>/<nombre>.jpg. fetch a 127.0.0.1 y el portapapeles NO funcionan.

## En curso (checkpoint 6-nov ~17:15, sesión 1 cortada por contexto a 180k)
- ✅ `nucleo/anime_vivo.py` (kit: Toma, render, cuadros; 0,31 s/cuadro en 1 proceso → paralelizar por plano).
- ✅ Fase A en flow/a/<clave>_a|b.jpg (hoja previews/hoja_A.jpg; elegidas las «_a»; escenarios algo pictóricos, personajes
  muy buenos). uuids en flow/uuids.json (clave → [uuid]).
- ✅ flow/_B.js (61 prompts, comprimido con diccionario `__D`): planos clip/llamada/img del original (sin las copias de
  escenario 001/026/040/059/068: usar flow/a/esc_*_a.jpg) + EXTRA 014b/032b/069b (segundo hablante).
- CÓMO LANZAR B: página del proyecto Flow → pegar helpers (bloque JS de abajo) + el contenido de flow/_B.js con
  javascript_tool (fetch a localhost y popups NO funcionan) → `await __prep(0)` → `find` «Iniciar generación» (ref) →
  browser_batch de 11 × [clic real por ref, `await __w(1500); (await __prep(k)).join(' ')`].
  Helpers: `__w`, `__ing(nombre,tipo)`, `__ingU(uuid)` (busca la opción por la miniatura y BAJA la lista con scroll hasta
  encontrarla), `__txt`, `__ningr`. Están en esta conversación; reescribirlos igual (ESTADO de llamada_domingo los describe).
- RECOGER: la galería solo pinta lo visible: scroll REAL (`computer scroll` 5 ticks en (400,400)) + `__col()` (junta
  img[src*=flow-content] con y+scrollTop) varias veces; ordenar por (y,x), INVERTIR → índice k = prompt k//2, variante k%2
  (los Expires salen en pares crecientes). Bajar con `python ../llamada_domingo/flow/_bajar.py "flow/b/{}.jpg" < lista`.
- DESPUÉS: registrar uuids de B (`python flow_anime.py reg flow/_regB.txt`, líneas «clave uuid»), elegir variante por hoja,
  `python flow_anime.py E` (2 ediciones por toma que habla: boca x2 = media+abierta, ojos x2) → lanzar igual → bajar a flow/e/.
- RENDER: escribir `tomas.py` (una Toma por plano: cam, fx, mov; audio de labios = ../llamada_domingo/medios/scene-NNN.mp4)
  → medios/scene-NNN.mp4 en paralelo → ensamblar 85 tramos (ui = recortes del MASTER original por beats.json) + audio
  ../llamada_domingo/audio/final.wav → salida/llamada_de_domingo_anime_MASTER.mp4 → tele master → avisar → preguntar si
  reemplaza al original programado (sáb 7-nov 10:00, be1zS17rxxI) o va aparte.

## Sesiones
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | estilo, kit anime_vivo, Flow A/B/E, render, MASTER | ✅ cerrado 20-nov (el video ya está subido) | 6-nov: estilo aprobado en la tele, kit, fase A bajada, _B.js listo |
| 2 | fase B en Flow | ✅ cerrado 20-nov (el video ya está subido) | 6-nov: 122 imágenes bajadas, 36/61 variantes elegidas; Flow cambió (asb), disco E: colgado |
| 4 | V2: ui en anime + más animación | ✅ cerrado 20-nov (el video ya está subido) | 7-nov: 23 ediciones anime de flow/bg enviadas a Flow; falta recoger, ui_anime.py, poses extra, MASTER v2 |
| 3 | render de planos, MASTER, subida | ✅ 7-nov | 56 planos en ~35 min con 4 procesos; MASTER 14:00; tele apagada → pregunta en chat; el usuario: «subirlo aparte en LogIA»; miniatura Flow (prompt_miniatura.md, 2/2 bien) |

## Lecciones
- Miniatura del remake: misma composición que la del original redibujada en anime con 2 ingredientes (tile de Ramón con
  «Añadir a la petición» + Daniel en base64 de 3 KB pegado): 2/2 bien a la primera. i.ytimg da 404 si el video aún es privado.
- Planos ui reciclados del original = fotorrealistas dentro del anime (miniatura de «Papá», calle del final): en un remake de
  estilo, la interfaz se re-renderiza con los retratos y fondos nuevos, no se recorta del MASTER viejo.
- Render en paralelo: 4 procesos con 32 GB (6 se quedó sin memoria); si el proceso muere quedan `medios/*.tmp.mp4` rotos
  que el relanzamiento sobrescribe. `print('✓')` a un log redirigido rompía en cp1252 → `sys.stdout.reconfigure(utf-8)`.
- Nano Banana edita la MISMA imagen con precisión (diferencia media 3/255): la cara entera se redibuja coherente → se cambia
  la cara completa con máscara suave, como un cel nuevo (cejas y mejillas se mueven con la boca: más vivo).
