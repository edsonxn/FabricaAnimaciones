# Las 15 cosas que NUNCA debes hacer en Fallout 4 — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: radio_yermo (1.er video del canal) · PROGRAMADO mié 18-nov-2026 17:00 CDMX (z_YrsxSbIFg, privado)
- estilo: secuencia_yt (receta de Tamriel; regla de oro `videos/tes_secretos_40/`) · kit NUEVO `nucleo/mg_fo.py` (Pip-Boy) · voz el Profeta + filtro radio modo B (`nucleo/fx_radio.py`) · OST oficial de Fallout 4 → doc: docs/estilo_secuencia_yt.md § Radio Yermo
- etapa: SUBIDO Y PROGRAMADO · MASTER `salida/fo_nunca_f4_MASTER.mp4` (14:02, 1080p) + .srt cargado · miniatura Flow `salida/miniatura.jpg` APLICADA el 18-nov (canal verificado)
- siguiente: medir a 7 días (25-nov) y empezar el 2.º video de Radio Yermo

## Sesiones («continúa el video fo_nunca_f4» retoma aquí · protocolo docs/sesiones.md)
- alias: nunca fallout 4, primer video de Radio Yermo · UNA sesión directo al MASTER (relevos por corte de 180k)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO hasta MASTER subido y programado | ✅ cerrado 20-nov (el video ya está subido) | tema elegido; investigación + kit mg_fo + filtro radio hechos; corte por contexto antes del guion |
| 2 | clips + mapa + efectos + OST + render + subida | ✅ 17-nov | MASTER subido y programado; miniatura sin aplicar (permiso del canal) |
| 3 | aplicar miniatura | ✅ 18-nov (canal verificado por el usuario; miniatura Flow aplicada) — antes ◐ 08:13 | `yt aplicar fo_nunca_f4 radio_yermo z_YrsxSbIFg`: metadatos OK, sigue programado 23:00Z; miniatura otra vez HTTP 403 (canal sin verificar) → falta que el usuario verifique y repetir el comando |

## En curso (checkpoint 17-nov, corte por contexto de la sesión 1)
- HECHO: investigación verificada en `_investigacion_A.md` (misiones) y `_investigacion_B.md` (mecánicas), con URL, nombres es, imágenes, búsquedas/clips.
- HECHO: kit `nucleo/mg_fo.py` (puesto, ficha, objetivo, special, terminal, vats, enemigo, rads, radio, botin, aviso, rejilla, contador, pegatina) probado en `previews/prueba_mg_fo.jpg` (`_prueba_mg.py`); refs reales en `nucleo/datos/ref_fo/`.
- HECHO: filtro de radio en el pipeline: `guion.VOZ_FX = {key: "radio" | "radio+sintonia" | "mezcla:<s>"}` + `VOZ_FX_DEFECTO = "tinte"` (`nucleo/voz_fx.py`, `nucleo/mezcla.py`; sintonía de 0,9 s antes de la frase). Falta documentarlo en docs/estilo_secuencia_yt.md § Radio Yermo y en docs/voz.md.
- LISTA ELEGIDA (cuenta atrás; datos en las investigaciones): 15 legendario a medias (muta y se cura, B6) · 14 Mar Resplandeciente sin protección (B3; cifras dudosas: decir «menos de dos minutos», Cráter del Átomo 300 rads/s) · 13 supermutante suicida (B10, 450 de daño, logro «¡Touchdown!») · 12 caer con servoarmadura junto a aliados (B10, se vuelven hostiles) · 11 contenedores fuera de tus asentamientos se vacían (B10) · 10 cabezón de atributo antes de tenerlo en 10 = pierdes el 11 (B10) · 9 Mamá Murphy: la 5.ª dosis, Psycho (A6) · 8 servoarmadura con el núcleo puesto (B1) · 7 matar a Sinjin de un tiro furtivo → muere Kent, pierdes las 3 mejoras del traje (A10, «Mortaja Plateada») · 6 «La opción nuclear» sin la orden de evacuación (A, reemplazo: Ferrocarril hostil) · 5 Refugio 81: quedarte la cura (Austin muere, el refugio te culpa, solo −10 vida máx.; A5) · 4 Gran líder de Nuka-World (Preston te odia aun con afinidad máx.; A3) · 3 Dunwich Borers con servoarmadura (se queda en el pozo inundado para siempre; B10) · 2 liberar a Lorenzo Cabot (A1) · 1 Far Harbor: código de apagado del parque eólico, la Niebla se traga el pueblo («Purificando la tierra»; A4 corregido).
- Nombres por confirmar con captura en español antes de la voz (los marca A y B: «Gran líder», parque eólico, «Psico/Psycho», mensaje de legendario…).
- HECHO guion.py; voz lanzada (`python fab.py fo_nunca_f4 voz > _voz.log`). FALTA en orden: (guion hecho: ~15 min ≈ 2 300 palabras a ritmo del Profeta; gancho con 1 cosa visible por frase; saludo/remates/suscripción/despedida marcados en VOZ_FX con radio; voz sin citar fuentes; promo hermano Tamriel opcional) → `chequeo_yt` antes de `voz` → voz (VOZ del Profeta como `videos/tes_builds_rotas/guion.py`) → seleccionar → idioma_voz → tiempo → beats → busquedas/bajar/medios → pegatinas + MG (`mg_fo`) + mapas (falta mapa de la Commonwealth: la wiki NO tiene el mapa oficial del Pip-Boy por API; buscar captura del mapa del mundo del juego, evitar «Commonwealth Cartography» que es un MOD; luego ajustar tema `fo` de mg_mapa) → OST oficial FO4 (Inon Zur) + SFX del juego → chequeo + fx hoja final + promesas → video → final → tele → miniatura Flow → subir y programar (hueco: canal URGENTE, 17:00 CDMX) → registrar.

## Decisiones (17-nov-2026)
- Tema elegido por el usuario: «15 NUNCA en Fallout 4» (Tamriel «15 misiones NUNCA» ×10,7; IGN «9 cosas que NO debes hacer en Fallout 4» 796 mil en español; SmackerUnknown «10 Mistakes ALL Fallout 4 Players Make» 99 mil/1 mes). Otros: «30 SECRETOS de FO4», «10 armas ROTAS de New Vegas» (reserva).
- Comentarios: canal sin videos → sin agradecimientos ni críticas en este (no hay comentarios propios). Suscripción: se pide (0 subs, sin cifra).
- Hueco: canal URGENTE desde hoy (ciclo 4 d, 17:00 CDMX).

## Hecho
- `nuevo --yt`, candado, `canales --actualizar`

## Falta
- [ ] guion · voz + filtro radio · beats/clips · pegatinas · MG · mapas · OST · SFX · chequeos · MASTER · miniatura · subida

## Checkpoint 17-nov (2)
- Pegatinas: 52 en `pegatinas/` (`_pegatinas.py`, fuentes en `pegatinas/_fuentes.txt`), hoja `previews/pegatinas_hoja.jpg` mirada: identidad OK. NO usar `enfermedad_rata.png` (Pip-Boy en inglés).
- MAPA: `mapas/_grid.png` (wiki «Commonwealth_map_grid.png», 2048²) = mapa REAL del Pip-Boy con rejilla roja de coordenadas del juego (origen 0,0 al centro-este; ±50 000 por línea gruesa). Plan: quitar la rejilla roja (inpaint de píxeles rojos) → `mapas/commonwealth.png`; ubicar cada lugar casando los recortes `FO4_map_<lugar>.jpg` de la wiki (marcador en el centro) contra el mapa (template matching), nunca de memoria. Lugares: Sanctuary Hills, Mar Resplandeciente/Cráter del Átomo, Medford Memorial Hospital, Mass Fusion, Goodneighbor, Milton General Hospital, Refugio 81, Dunwich Borers, Manicomio Parsons, Casa Cabot. Far Harbor es otro mapa (La Isla): mapa aparte o sin mapa.
- Clips: `bajar -j 4` corriendo en segundo plano (`_bajar.log`); luego `fab.py fo_nunca_f4 medios` y MIRAR las hojas.
- MAPA (17-nov, sesión 1): `mapas/commonwealth.png` ya LIMPIO (rejilla roja quitada con inpaint; es el mapa real del Pip-Boy). `_ubicar.py`
  (template matching de los recortes `FO4_map_<lugar>.jpg` de la wiki) NO es fiable: los recortes vienen a escalas distintas (774×531 y
  1354×994) y varios lugares caen en el mismo punto (Medford y Sanctuary con y=0,123; Casa Cabot = Instituto; Parsons cogió «Parsons_Creamery»).
  Solo parecen buenos: Dunwich (0,833, 0,122) NE, Cráter del Átomo (0,220, 0,869) SO, Borde del Mar (0,216, 0,708), Refugio 81 (0,277, 0,518).
  Hacerlo bien: las coordenadas del juego (rejilla de `_grid.png`: líneas cada 50 000 unidades, 0,0 marcado) + la posición en unidades del
  juego de cada lugar (wiki: plantilla del lugar / «cell» o mapa en el recorte con el marcador), o casar cada recorte a SU escala (medir la
  escala por par de iconos). Mirar `previews/_coords.jpg` antes de usar ninguna coordenada.

## Checkpoint 17-nov (sesión 2)
- Clips MIRADOS: rehechos con `--url --desde` (cuadros comprobados) 4, 6, 16, 32, 41, 50, 68, 75, 81, 82, 83, 85, 87 (terminal TURBINE_DATA real), 90, 96 (textos de youtubers, marcas de agua, streamer, tarjetas negras, mod). OJO: el bucle `while read` necesita `</dev/null` en `fab.py bajar` (se come el stdin).
- MAPA HECHO: `_ubicar3.py` (recortes del Pip-Boy de la wiki en `mapas/_recortes/`, ícono de cada lugar leído JUNTO A SU RÓTULO en el recorte, recorte registrado por template matching multiescala del recorte entero, punto proyectado) → `mapas/_coords.json` (sanctuary, crater_atomo, medford, milton, mass_fusion, goodneighbor, diamond_city, refugio81, dunwich, manicomio, casa_cabot, instituto = ruinas del C.I.T.). COMPROBADO en `previews/_coords_check.jpg` (recorte | mapa, mismo encuadre): todos casan ícono por ícono; Mass Fusion corregido a (1012,107) del recorte e instituto a las ruinas del C.I.T. (el Instituto no tiene ícono en el mapa grande) — mirar esas dos filas en la hoja nueva.
- Tema `fo` de `nucleo/mg_mapa.py` AJUSTADO: marcadores = cuatro escuadras de selección del Pip-Boy (como las capturas de la wiki) + cuadrito; meta con doble escuadra. Probar con `MP.hoja` antes de `fx`.
- FALTA en orden: (1) efectos.py según `_plan_efectos.md` (anclas contra timeline.json; mira `previews/pegatinas_hoja.jpg`); (2) imagen del MEMORIAL de Austin (promesa visual seg 536: wiki o Flow); (3) logo de Crónicas de Tamriel para el cierre; (4) banco SFX de Fallout 4 + OST oficial (Inon Zur, una pista por puesto, `armar_musica_ost.py`); (5) `texto_clips.py fo_nunca_f4 -j 4`, chequeo, `FAB_FX_FINAL=1 fx hoja` mirando TODO, promesas.md; (6) video → final → tele → miniatura Flow → subir 17:00 → registrar → commit (incluye nucleo/mg_mapa.py).
- efectos.py ESCRITO (sesión 2, tras el corte; la app no dejó abrir el relevo desde este turno): 162 FX según `_plan_efectos.md` + EXTRA de huecos; `fx --seco` resuelve todas las anclas; único hueco > 4 s: 543-550 (MEMORIAL de Austin: no hay imagen en la wiki ni nítida en `QNtCXe2BwvU` (aula a los ~56 s, 360p) → generarlo en Flow como `pantallas/memorial_austin.jpg` con ingredientes reales y meter `pant()` ahí). Logo del canal hermano: `pegatinas/tamriel_canal.png` (avatar real del canal). `PISTAS = []` hasta crear el banco SFX de Fallout 4.
- (sesión 2, 18:45) `fx hoja` MIRADA (8 hojas): corregidos textos encimados con el HUD de los clips (avisos a y=.86), «Sinjin»/«Longfellow» puestos sobre OTRO personaje (quitados: VATS/enemigo), muro con 5 fotos, suero/contador separados; clips 008 (mutación real), 039 (Sanctuary, antes negro) y 067 (antes menú de taller) rehechos. Mapas: `efectos._recorta()` recorta el Pip-Boy a la zona (sin eso, falta de memoria a 4200 px).
- OST HECHA: `_bajar_ost.py` (16 pistas de Inon Zur, álbum «Fallout 4» comprobado; Behemoth = FO3, fuera) + `ost_canto.py` + `armar_musica_ost.py` → `audio/musica.wav` (842,5 s, sin canto bajo la voz). SFX del juego: banco nuevo `nucleo/datos/sfx_juego/fallout4/` (`_bajar.py`, 8 sonidos; «geiger» es genérico) → `sfx/*.mp3` + PISTAS en efectos.py.
- (19:30) chequeo: MG 6,0/min, pegatinas 4,0/min (56, 28 entradas, 0 repetidas), mapas 0,9/min, idioma OK 97 frases; OCR = solo HUD del juego. Clip de New Vegas en scene-028 → rehecho con FO4 (sl6-kQgvAss). MEMORIAL: captura REAL del aula (QNtCXe2BwvU 57,6 s) → `pantallas/memorial_austin.jpg` + `pant()`. `promesas.md` escrito. `fx` (audio/fx.wav OK; borradores de Montaje parados en 11/51) → `mezcla` OK (−14 LUFS, voz +12,5 dB, filtro de radio en 19 frases).
- (19:45) MINIATURA de Flow HECHA: proyecto Flow «nov 17 - 19:29» (Chrome; en el navegador integrado no llega el pegado), ingredientes reales (calle de Boston de scene-094, servoarmaduras y Lorenzo de la wiki) pegados con ClipboardEvent sintético desde un servidor local, Nano Banana 2.1 16:9 ×4, texto «¡NUNCA HAGAS ESTO!» + «FALLOUT 4» escrito por Nano Banana → variante 3 → `salida/miniatura.jpg` (las 4 en `miniatura_ing/flow_v*.img`). `youtube.json` escrito (capítulos, fuentes, créditos de 46 canales, música Inon Zur). Esperando a que termine el render de `t1_blg_caida` para lanzar `video`.

## Lecciones (cierre 17-nov)
- Mapas del Pip-Boy: ubicar con el ícono JUNTO A SU RÓTULO en el recorte de la wiki (el corchete no siempre está al centro) y registrar el recorte entero; recortar el mapa a la zona en cada FX (`_recorta`), si no, falta de memoria a 4200 px.
- Clips de FO4 llenos de HUD en inglés: el OCR los marca todos; la revisión real es a ojo en las hojas `fx_NN` (etiquetas del kit encimadas con el nombre del enemigo del clip → poner `enemigo` en y=.22 y avisos abajo).
- Un clip «de baúles» resultó ser de New Vegas (HUD ámbar): `chequeo` lo detectó por el título.
- Etiquetas de identidad (VATS/enemigo «Sinjin», «Viejo Longfellow») cayeron sobre OTRO personaje del clip: no rotular personajes sobre un clip sin mirar quién sale.
- Flow desde Chrome: ingredientes por `ClipboardEvent('paste')` con archivos servidos en http://localhost (Chrome sí lo permite; el navegador integrado no), descarga por la URL firmada de `flow-content.google` con curl.
- Canal nuevo: YouTube no deja miniaturas personalizadas hasta verificar el canal (HTTP 403 en `thumbnails/set`).
