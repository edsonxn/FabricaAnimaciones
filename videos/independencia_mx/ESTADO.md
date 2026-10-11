# La Independencia de México, completa — ESTADO
- canal: bitacora_perdida · PROGRAMADO sáb 10-oct-2026 12:00 CDMX (dPk9bs6dX0Q; publishAt 2026-10-10T18:00:00Z, privado hasta la fecha, con miniatura IA y .srt)
- estilo: kurzgesagt ISOMÉTRICO (dioramas `kz_iso*`, mapa con relieve real `kz_mapa*`, retratos, UI de cápsulas) → docs/estilo_kurzgesagt.md · catálogo del kit: `docs/api_kz.md` (grep, no leer entero)
- etapa: v5 subida y programada (6-oct-2026)
- siguiente: nada; el 10-oct comprobar que salió público. Subidas viejas `f4Ipx5rLdmQ` (v2) y `1lq_vl0VTGQ` (v3): el usuario las borra en Studio. Tras publicarse: `python fab.py independencia_mx limpiar` (segmentos 803 MB)

## Qué es lo que existe
- Voz CER 0 (`voz/`), `timeline.json` (650,4 s, 18 escenas, BPM 112), `audio/` (música Lyria 5 partes + mezcla −14 LUFS). NO tocar los textos de `guion.py` (regenera voz).
- MASTER viejo de `salida/` = v2 con defectos (manchas verdes, desierto repetido, cuadro negro). Subido en privado https://youtu.be/f4Ipx5rLdmQ: NO publicar; se reemplaza al terminar con `yt aplicar`/nueva subida.
- Versión boceto anterior archivada en `boceto_v1/`; `v2_lateral/`, `figuras.py`, `mundo.py`, `mundos.py` son restos de v2 (Dolores de `mundos.py` se usa en t01 y t05 con `objetos(t, gente=0)` para pueblo dormido; RutaPlata en t01).
- Kit nuevo en `nucleo/`: `kz_iso*.py` (arquitectura, objetos, gente, interiores, deco), `kz_mapa*.py` (relieve ETOPO1 + países Natural Earth), `kz_retrato.py`, `kz_ui.py`. Mundos de video: `mundos_b.py` (RutaPlata, Hacienda, PuebloRuina), `mundos_c.py` (pirámide social), `mundos_d.py` (salones, trono, PlazaMayor), `mundos_e.py` (sala criolla, CalleQueretaro, PlazaPueblo, TalleresDolores, casa en corte), `mundos_f.py` (casa cural interior, CaminoMarcha, TierrasPueblo), `mundos_g.py` (GuanajuatoCiudad con Alhóndiga, Campamentos, cerros), `mundos_h.py` (MonteCruces, vista del valle, CampoRealista).

## Cómo se construye una escena (copiar de t03.py)
- `t0N.py` = `@shot(t0, bg=..., post=[GRAD], ent=(tipo, dur))` por cada toma; anclas con `T(escena, "palabra", frase=i)` (coincide por prefijo: usar `frase=`). `escenas.py` ordena todas las tomas; cada una dura hasta la siguiente.
- Toma de mapa: `bg=lambda t: MP.base(cam(t), t)` + `MD.*` (pais, ciudad, ruta, ejercito, etiqueta, mar_vivo, montes…). Toma isométrica: `Iso`, `Mundo`, `casa_colonial`, `Multitud`… (ver `mundos_d.PlazaMayor`, `mundos_b.Hacienda`).
- Pruebas: `./run.sh _prueba.py nombre t1 t2 ...` (hoja 3 columnas en `previews/nombre.jpg`); `./_esc.sh <escena> [n]` n cuadros repartidos; `./run.sh _cuadro.py t nombre` un cuadro completo; clip fluido: `./run.sh _clip.py t0 t1 previews/x.mp4 6`. Un cuadro cuesta ~0,3-1 s.
- Antes del render: `python fab.py independencia_mx comprobar`; render con `--procs 8`; luego `final`, `verificar`, revisar un cuadro cada ~3 s a tamaño completo.

## Escenas (t0–t1 en s)
| # | id | t0–t1 | estado |
|---|---|---|---|
| 1 | gancho | 0–17 | t01.py hecho (Dolores, repique en el mapa, título) |
| 2 | nueva_espana | 17–66 | t02.py hecho (plata, pirámide social, deudas, ruina) |
| 3 | napoleon | 66–105 | t03.py hecho; pulir última toma (etiquetas «Iturrigaray/Yermo» y «Garibay/Calleja» se encimaban en 98-104 s) |
| 4 | conspiracion | 105–148 | HECHO t04.py+t04b.py (tertulia, mapa Querétaro, calle, oficiales, plaza con sillón vacío, talleres de Dolores, calendario, delator, Josefa en pantalla dividida, jinete en el mapa). Mundos en `mundos_e.py` |
| 5 | grito | 148–193 | HECHO t05.py+t05b.py (Dolores de madrugada, casa cural, campana y multitud, Grito, estandarte, marcha, mapa que crece, tierras/tributos). Mundos en `mundos_f.py` |
| 6 | guanajuato | 193–229 | HECHO t06.py (mapa, ciudad minera con cerros, Alhóndiga, asedio, Pípila, saqueo, campamentos, mapa a la capital). Mundos en `mundos_g.py` (GuanajuatoCiudad, Campamentos, `cerros()` fondo con paralaje) |
| 7 | capital | 229–266 | HECHO t07.py (mapa, batalla en el monte, vista del valle con 80 000, flechas de retirada, burbujas de duda, campo realista, Aculco, discusión, ruptura). Mundos en `mundos_h.py` (MonteCruces, `vista_capital`/`multitud_espalda` 2D, CampoRealista) |
| 8 | guadalajara | 266–296 | HECHO t08.py (plaza de Guadalajara, decreto y cadenas rotas, imprenta y ministros, batalla de Calderón con 170+96 personas, explosión). Mundos en `mundos_i.py` (Guadalajara, imprenta/prensa, CampoCalderon) |
| 9 | captura | 296–332 | HECHO t09.py (huida al norte, emboscada en desierto, prisioneros, jefes con crespón, Hidalgo degradado y patio, jaulas en la Alhóndiga, semilla). Mundos en `mundos_j.py`. Tono sobrio: paleta gris/violeta, sin mostrar el momento de las ejecuciones |
| 10 | morelos | 332–377 | HECHO t10.py (mapa del sur, carpintería, mesa de guerra, victorias, sitio de Cuautla, salida de noche, aliados, Leona, conquistas). Mundos en `mundos_k.py` (carpinteria, Cuautla) |
| 11 | congreso | 377–409 | HECHO t11.py (mapa, salón del congreso, acta con mapa Atlántico z=0.18, Sentimientos, soberanía/cadena/castas en 2D, americanos, Apatzingán). Utilería 2D en `mundos_l.py` (cadena, escalera_castas) |
| 12 | fusilamiento | 409–444 | HECHO t12.py (cerco realista, círculo que cae, Congreso que huye, captura, juicio, patio sobrio, luces que se apagan). Reusa mundos de t09/t10 |
| 13 | guerrillas | 444–486 | HECHO t13.py (luces que se encienden en la sierra, Guerrero, Victoria en la selva, Mina, diez velas, cercos, 4 paneles del costo). Mundos en `mundos_m.py` (SierraSur, Selva) |
| 14 | giro | 486–519 | HECHO t14.py (mapa del Atlántico con tormenta y barco, rey Fernando VII y fusiles, barras recortadas con tijeras, La Profesa, separarse con soga cortada, independencia con asterisco y escudo). Casi todo 2D, interior propio en t14 |
| 15 | iturbide | 519–555 | HECHO t15.py (Iturbide elegido, campañas, encargo, Plan de Iguala y tres garantías, mensaje para todos, cartas, abrazo, Ejército Trigarante). Mundos en `mundos_n.py` (PlazaIguala, guirnaldas) |
| 16 | consumacion | 555–585 | HECHO t16.py (noticia como pólvora con ciudades que cambian a tricolor, O'Donojú en Veracruz, Tratados de Córdoba, entrada a la Plaza Mayor con Iturbide, Acta y fuegos artificiales, línea de 11 años) |
| 17 | despues | 585–621 | HECHO t17.py (nubes de problemas, Iturbide emperador con 12 meses, emblema 1824, Guerrero y cadena, traición, héroes con crespón, territorio, bolsa vacía e ideas distintas) |
| 18 | cierre | 621–650 | HECHO t18.py (tarjetas 16 y 27, plaza de noche, Díaz con la campana, ni un hombre ni un bando, muchos, pregunta final) |

## Reglas que aplican aquí (ver CLAUDE.md «Rigor»)
- Cada toma: ≥ 3 planos, detalle propio del lugar, animación ambiente, acción narrada por personajes; sin etiquetas encimadas; nada quieto > 2 s; mapas siempre con relieve real y ciudades en su coordenada.
- Cada escena con su mundo visual propio (no repetir el mismo diorama en escenas distintas).

## Lecciones técnicas (del rehacer)
- El relieve ETOPO1 se ve borroso por encima de zoom ~3,5 en `MP.base`: usa `exag=12, rios_umbral=0.7` (BASE en t04) y zoom ≤ 3,5; para acercarte, pasa a un diorama isométrico (`MD.ciudad` es de tamaño fijo, no depende del zoom).
- `U.salida(t, t1, dur)` vale 1 ANTES de t1 y baja a 0 después (no al revés): multiplica `U.pop(...) * U.salida(...)`.
- Cortes de casa de dos pisos: el piso de arriba tapa al de abajo; usa pantalla dividida con muesca (como `p_trono` en t03 y `q_josefa` en t04b).
- Personas en `G.persona`: tipos disponibles en `G.TIPOS` (no existe `criollo`: usa noble/regidor/comerciante/escribano/dama); retratos en `RT.QUIEN`.
- `T(escena, palabra, n=k)`: n es BASE 0 (n=1 = segunda aparición); coincide por prefijo y sin acentos.
- Etiquetas `U.llamada`: si dos van a coincidir en tiempo, pon `U.salida(t, t_siguiente - 0.15)` a la primera; cada etiqueta de una lista (machetes/palos/piedras) dura ~1 s y no hasta el final de la toma.
- Mapas: entre ciudades cercanas (Toluca–México ≈ 60 km) los íconos de ciudad/ejército (tamaño fijo en px) se encimaban; para movimientos locales usa flechas gruesas de pantalla (`_flecha` en t07.py) con ejércitos encima en vez de `MD.ruta`.

## Estado del render (2-oct-2026)
- El render v3 de 1-oct se cayó a las 12:33 por `ArrayMemoryError` (8 procesos; solo 9 de 217 segmentos hechos). Relanzado 2-oct ~16:50 con `bash _render_retry.sh` (6 procesos, reintenta solo y reanuda) → log `render_v3_log.txt`; termina con la línea `LISTO` y `salida/video_sin_audio.mp4`. ~1,5-2 h.
- Rótulos de t03 (98-104 s) ya revisados: sin choques (era una nota vieja).
- NO ejecutar voz/Chatterbox mientras renderiza.
- Pendiente tras el render: `python fab.py independencia_mx final`; `verificar`; contactos del MASTER (un cuadro cada 3 s: ffmpeg + hoja) y revisión a tamaño completo; subir con `yt subir` (privado) o `yt aplicar` sobre `f4Ipx5rLdmQ`; miniatura IA (`prompt_miniatura.md`); programar sáb 10-oct 12:00 CDMX = 2026-10-10T18:00:00Z (preguntar al usuario antes de publicar).
- Miniatura REHECHA (2-oct, el usuario dijo que el retrato del kit era feo): Hidalgo dibujado a medida en `mini_hidalgo.py` (cara, manos, sotana, estandarte; sin figuras encimadas) + `./run.sh _mini.py campana` → `salida/independencia_mexico_mini_final.jpg` (1280x720, «11 AÑOS / DE GUERRA», Hidalgo gritando, campana dorada, multitud con antorchas y estandarte). `youtube.json` ya apunta a ese archivo. Copia de respaldo en `previews/mini_final_respaldo.jpg`.
- Usuario pidió (2-oct): subir EN PRIVADO (no publicar ni programar). Cuando acabe el render: `bash _post_render.sh` (espera `LISTO`, hace `final` + `verificar`, log `post_render_log.txt`); luego revisar cuadros del MASTER a tamaño completo y `python fab.py yt subir independencia_mx bitacora_perdida private`; anotar el id nuevo en `canales/bitacora_perdida.json` y una línea en BITACORA.md.

## Revisión del MASTER v3 (2-oct-2026, un cuadro cada 3 s a tamaño completo, 217 cuadros)
- Render v3 terminado (5426 s), `final` + `verificar` OK: 650,37 s, 1080p, desfase 0 ms, CER 0,0009 (única frase >2 %: gancho_1 «Nadie imagina que ese repique va a desatar 11 años de heredra»: es el transcriptor, no la voz).
- NO quedan segmentos ni video_sin_audio: cualquier arreglo exige re-render completo UNA vez (desde 4-oct el render va ~2x más rápido por cuadro y admite 12 procesos si se cierran `chatterbox_server.py`/`app.py`; no deja dormir la PC). Ese render deja `segmentos/` (ya no los borra `final`), así que los arreglos siguientes son por tramos: `python fab.py independencia_mx video --rehacer 270-280 ...` + `final`.
- Calidad general: bien (mapas con relieve real, dioramas distintos por escena, retratos, sin escenas vacías). Subido en PRIVADO el 2-oct por pedido del usuario; NO publicar hasta arreglar lo de abajo si el usuario lo pide.
- Defectos menores vistos (candidatos a parche):
  1. Rótulo de lugar/fecha de esquina (`U.fecha_lugar`) tapado por la llamada superior en: Guadalajara «Noviembre de 1810» (~4:33), Ciudad de México «Diciembre de 1815» (~7:30), Temalaca «Noviembre de 1815» (~7:20), Iguala «24 de febrero de 1821» (~8:40), «1820» tapado por la etiqueta «Fernando VII» (~8:10).
  2. La Profesa (~8:25): etiquetas «obispos», «ricos», «oficiales conservadores» y «Ciudad de México» se encimaban.
  3. Destellos negros de 0,13-0,2 s en las transiciones de tinta (17,4 s; 80,9 s; 116,9 s; 139,1 s; 391,9 s): mancha de tinta que cubre todo el cuadro (`docu_fx.mezcla2`, `thr = ... * 1.12`; bajar a ≤ 0,9 para que nunca quede negro total).
  4. Toma final de t17 (~619-621 s): sin acción más de 2 s (solo bokeh/chispas) y el texto «cómo gobernar» se corta dentro de la caja.
  5. «Esa decisión cambió la historia» (~4:10): texto blanco con poco contraste sobre el edificio claro. Etiqueta «Veracruz» tapada por el barco (~9:00).

- **SUBIDO EN PRIVADO el 2-oct-2026: https://youtu.be/1lq_vl0VTGQ** (video + miniatura + .srt). Registrado en `canales/bitacora_perdida.json` y BITACORA.md. Siguiente: decidir con el usuario si se parchean los defectos de arriba y se re-sube, o se programa tal cual (sáb 10-oct 12:00 CDMX = 2026-10-10T18:00:00Z con `yt publicar bitacora_perdida <id> public --programar ...`; preguntar antes).

## v4 (2-oct-2026 noche): correcciones del usuario sobre la v3 (ver «Revisión del MASTER v3» arriba)
- Quejas: (1) olas/mar con «paralaje» raro al mover la cámara; (2) elementos o personas detrás de otros (muelle de Veracruz en t02, etc.); (3) usar RETRATOS REALES (pinturas/grabados de dominio público) integrados con marco, no los bustos dibujados.
- Hecho: `MD.mar_vivo` reescrito (rejillas lon/lat por nivel con fundido; olas = polígonos alfa); brillo del agua en coordenadas del mundo; íconos de ciudad achicados con el zoom y sin amontonarse; `Mundo.topo` (orden geométrico) activo en RutaPlata y PuebloRuina con muelle/barcos/estibadores reubicados; etiquetas sin cola diferidas y esquivando fecha de esquina/marcos/otras etiquetas (`lz.diferir`); tinta sin negro total; t14 «1820»/«un golpe militar» al lado del retrato; t17 final con movimiento; t13 «1817» registrado; t18 pares de retratos separados; ESPAÑA/PORTUGAL de t03 reubicadas.
- Retratos reales: `nucleo/kz_retrato_real.py`, recortes en `nucleo/datos/retratos/` (21 personajes, créditos en CREDITOS.md; `retratos/_config.py` + `nucleo/preparar_retratos.py`; búsqueda/descarga con `_buscar_retratos.py`, `_bajar_retratos.py`). `RT.retrato`/`MD.medallon` delegan solos. Los genéricos (campesino, criollo, peninsular, esclavo…) siguen dibujados.
- Miniatura: Hidalgo dibujado a medida (`mini_hidalgo.py`) + `_mini.py` (el usuario no volvió a quejarse de ella tras la 2.ª versión). Si quiere retrato real en la miniatura: usar `retratos/` también ahí.
- Docs actualizados: docs/estilo_kurzgesagt.md §A, CLAUDE.md (tabla de estilos), docs/api_kz.md.
- Render v4 lanzado 20:02 (6 procesos, `_render_retry.sh`) → luego `_post_render.sh` (final + verificar, log `post_render_log.txt`). El MASTER v3 quedó en `salida_v3_backup/`.
- Pendiente tras el render: revisar cuadros del MASTER v4 a tamaño completo (mar, puerto, retratos, rótulos), subir en PRIVADO (`yt subir independencia_mx bitacora_perdida private`; es un video NUEVO: el v3 `1lq_vl0VTGQ` y el v2 `f4Ipx5rLdmQ` quedan para borrar en Studio), anotar el id en `canales/bitacora_perdida.json` y BITACORA.md. NO publicar sin preguntar.

## v5 (6-oct-2026): revisión del MASTER v4 + 2 parches + render completo
- MASTER v4 (3-oct) revisado: 217 cuadros (uno cada 3 s) en hojas `previews/v4_rev/hojas/` + cuadros puntuales a tamaño completo; `blackdetect` sin destellos negros (90,7 s es un fundido a fondo vino, no un fallo). Rótulos de esquina, La Profesa y retratos reales: bien.
- Parches: `t15.py` la etiqueta «Iguala» de la ciudad sale cuando entra «lanza el Plan de Iguala» (quedaba tapada, ~8:52); `t18.py` la palomita del calendario 27 va a la esquina (cruzaba «la consumación», ~10:26). Probados en `previews/fix_palomita.png` y `previews/fix_iguala.jpg`.
- Render v5 lanzado 6-oct con 12 procesos + `final` + `verificar` → log `render_v5_log.txt` (deja `segmentos/`: arreglos siguientes por tramos con `video --rehacer`).
- Miniatura nueva con IA en Google Flow (Nano Banana 2.1, sesión de la cuenta Edsonxn en el navegador integrado): proyecto https://flow.google.com/project/81dab65c-b2cc-4863-b208-b0f09a84c880 , 2 opciones «11 AÑOS / DE GUERRA» (Hidalgo con la campana). Falta: que el usuario elija, descargarla, reducir a 1280x720 (<2 MB) → `salida/independencia_mexico_mini_final.jpg`.
- Siguiente: al terminar el render revisar los tramos parchados (8:50-8:56, 10:24-10:28) y una pasada general → `python fab.py yt subir independencia_mx bitacora_perdida private` (video NUEVO; v3 `1lq_vl0VTGQ` y v2 `f4Ipx5rLdmQ` quedan para borrar en Studio) → anotar id en `canales/bitacora_perdida.json` y BITACORA.md → programar sáb 10-oct 12:00 CDMX (2026-10-10T18:00:00Z) solo si el usuario lo confirma.
- **6-oct 13:20: render v5 OK** (650,37 s, CER 0,0009, desfase 0 ms; v5 idéntico al v4 salvo los 2 parches: comparación automática cuadro a cuadro + tramos parchados vistos). Miniatura: opción 2 de Flow → `salida/independencia_mexico_mini_final.jpg` (alternativa `_mini_alt.jpg`). Descripción de `youtube.json` corregida (retratos de dominio público). **Subido y programado: https://youtu.be/dPk9bs6dX0Q**.
- Lección: Flow (flow.google.com) en el navegador integrado tiene la sesión de la cuenta Edsonxn; las imágenes generadas se bajan con la URL `flow-content.google/image/...` del `<img>` (1376x768 → recortar a 16:9 y reducir a 1280x720).
