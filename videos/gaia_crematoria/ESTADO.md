# La Crematoria: dos padres, dos hijos y una espada — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: gaia_eterna (alta 29-oct-2026; falta `yt conectar` con la cuenta de la esposa) · sábado 10:00 CDMX, primer hueco tras el MASTER
- estilo: pegatina_flow (formato «Pamela») → docs/estilo_pegatina_flow.md § 8 · ejemplo: videos/wow_darrowshire/ · mapas: nucleo/mg_mapa.py tema "wow"
- etapa: voz ✅ · OST ✅ · Flow 192 imágenes ✅ · recorte ✅ · reales/mapas/SFX ✅ · escenas (plan.py, ~300 tomas) ✅ · mezcla ✅ · RENDER en marcha (10:14, 865 segmentos) · miniatura ✅ · youtube.json ✅
- siguiente: tramo 7a (revisión de los primeros ~10 min, ver «En curso») → visto bueno → render completo → `final` → `verificar` → aviso → `yt conectar` (cuenta de la esposa) → subir y programar

## Sesiones (plan de tramos · «continúa el video gaia_crematoria» retoma aquí · protocolo docs/sesiones.md)
- alias: gaia_crematoria, la Crematoria, el de Gaia Eterna, el de Tirion y los Mograine, el de la Ashbringer
- vista previa: 🎞 Montaje del panel con audio completo conforme salen las escenas (pendiente de confirmar con el usuario)
- leer al empezar: este ESTADO.md, `fuentes_lore.md`, docs/estilo_pegatina_flow.md § 8 y videos/wow_darrowshire/ESTADO.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Alta del canal + casting de voces + lore con fuentes + guion 40-50 min | ✅ 29-oct | canal ✅, voz narradora ✅, casting ✅ (elegido en casting.html), lore ✅, guion ✅ ~44 min |
| 2 | Voz (narradora + personajes) + seleccionar + tiempo + OST | ✅ 29-oct | 367 frases (~6 000 créditos); 1 bloqueada por el filtro (reescrita); 8 regeneradas; 43:14; OST 15 pistas |
| 3 | Flow (escenarios + hojas con ciclos + utilería) + recorte + profundidad + reales + mapas + SFX del juego | ✅ 29-oct | 96 prompts x2 (proyecto Flow «oct 29 - 09:33»), 30 hojas, 37 reales + 8 iconos + 8 medallones, 10 mapas, 93 SFX |
| 4-6 | Escenas por actos + sfx + mezcla | ✅ 29-oct | MOTOR POR DATOS: `escenas.py` dibuja y `plan.py` describe ~300 tomas; muestras cada 40 s revisadas (`_muestras.py`) |
| 7a | Revisión de los primeros ~10 min (mapas sin pixelar, fotos reales del juego, escena de la posada de Costasur) → avance → visto bueno | ◐ correcciones 7a (Eitrigg ✅, espada ✅, fotos reales pendiente) | 29-oct 14:05 render 0-798 s ✅ (sin errores; los 6 clips comprobados en el AVANCE); `salida/gaia_crematoria_AVANCE.mp4` + `AVANCE_ligero.mp4`; avisado |
| 7 | Render → MASTER → aviso al usuario → miniatura → youtube.json | ◐ 217/865 | render ≈ 2,5 h; detenido hasta el visto bueno del 7a |
| 8 | Subir (tras `yt conectar`) + registro + cierre | pendiente | |


- `audio/` pasado a carpeta REAL en C: (E: dio Ntfs 55 el 28-oct; ver memoria disco-e-fallando). `voz/` sigue en E:.

## En curso (29-oct, tramo 7)
- ⏸ 29-oct (noche) PAUSADO por el usuario: «pausemos lo de gaia hasta terminar lo de la worlds» (cfo_kc_jugadas). No lanzar nada de
  este video hasta que el usuario lo retome. Estado al pausar: avance del acto 1 corregido (16:03, `salida/AVANCE_ligero.mp4`)
  esperando su veredicto; render completo NO lanzado; 0 procesos de render.
- ✏ CORRECCIÓN 7a del usuario (29-oct, tras ver el avance): «en esa escena cambió al orco por humano, debe ser un orco también» =
  Tirion arrodillado curando con la Luz junto a Eitrigg herido en el campamento orco (`plan.py` juicio_11 y juicio_12, fondo
  e23_colina_horda). Causa: la pieza `TJ3` (`piezas/h08_tirion_joven/03.png`) trae DIBUJADA bajo sus manos una figura HUMANA
  blanca translúcida. Arreglo: copia `03.png` → `piezas/_respaldo/h08_03_orig.png`; borra de `03.png` esa figura (píxeles
  blanco-grises poco saturados del tercio inferior; la armadura dorada es saturada y se queda) y en juicio_11/12 pon bajo sus
  manos al orco `EI5` (Eitrigg tendido con el hacha) con `brillo` dorado (ORO) sobre él. Hoja de prueba con `_muestras.py`
  (tiempos: `python _tiempos_7a.py` + la toma juicio_11 en `escenas.TOMAS`), borra solo esos `segmentos/seg_NNNN.mp4`
  (NNNN = t // 3) y `python fab.py gaia_crematoria video --hasta 798` → copia ligera desde `salida/gaia_crematoria_AVANCE.mp4`
  (NO `_avance.py`: duplica 2 GB en E:) → `fab.py avisar` + mensaje. Juntar con lo demás que pida el usuario del avance.
  ◐ 29-oct (sesión hija): ✅ `03.png` sin la figura humana (respaldo `piezas/_respaldo/h08_03_orig.png`, script
  `piezas/_respaldo/h08_03_quitar_humano.py`; la luz que queda bajo las manos se desvanece por saturación, sin borde dentado).
  ✅ plan.py juicio_11: EI5 (0.70, 0.97, 0.34) bajo las manos, TJ3 subido a y=0.90, brillo (0.66, 0.76, 90); juicio_12: EI5
  (0.58, 0.99, 0.42) + TJ3 y=0.90 + brillo (0.55, 0.74, 170). Hoja revisada (640-653 s). Borrados seg_0213-0217 →
  `video --hasta 798` lanzado ~15:00 (log `render_7a_log.txt`; rehízo además 57 segmentos viejos de la vista previa).
  ✅ n.º 2 (sesión hija, 29-oct): la espada cortada y el borde recto venían de la pieza `DA4` (h05, hoja _a: la espada de DA3
  se le metía y la figura estaba cortada). `DA4` y `DA3` RECORTADOS DE LA HOJA _b (DA3 = Darion con la espada vertical, sin
  las piernas cortadas de DA4 abajo); originales en `piezas/_respaldo/h05_0{3,4}_orig.png`. ¡No relanzar `recortar` de h05!
  (meta.json de h05 sigue diciendo hoja _a). plan.py: alturas de DA4 reajustadas (pieza ahora solo el cuerpo tendido:
  0.26-0.29) y plaga_7 en (0.56, 0.86). Hojas revisadas 753-768 s.
  ◐ 29-oct ~15:50 (sesión nieta): ✅ render 15:00 acabado (AVANCE 15:45). ✅ (a) borrados seg_0250-0255. ✅ (b) n.º 3 barato:
  fotos reales nuevas en orbe_2 (tirion), forja_2 (agonia_escarcha), forja_9 (crematoria, 0.80/0.20/0.15), juicio_2 (tirion),
  juicio_14 (tirion), plaga_1 (alexandros_vivo), plaga_3 (kelthuzad); copia previa `previews/_plan_antes_n3.py`; hoja
  `previews/n3_reales.jpg` revisada; borrados sus 17 segmentos (65-66, 134-135, 151-152, 190-192, 221-222, 239-241, 244-246).
  Propuesta Flow (NO lanzada): regenerar con la foto real como ingrediente las hojas h01 h03 h08 h11 h13 h14 h15 h16 h17 (acto 1;
  + h02 h04 h06 h10 para el resto) = 9 (13) imágenes de Flow, ~55 (~78) piezas.
  ✅ (c) 16:02 `video --hasta 798` (36 seg., log `render_7b_log.txt`, sin Traceback) → AVANCE revisado con cuadros del mp4
  (`previews/avance_7b_hoja.jpg`) → `salida/AVANCE_ligero.mp4` (720p nvenc, 217 MB, 13:18) → avisado por voz.
  ◐ 16:20 el usuario: «Sí, regenera en Flow». Hecho en Chrome (Flow proyecto «oct 29 - 16:17», x2, 0 puntos; ingredientes =
  `hojas_reales/ingred/ref_*.jpg` subidos con file_upload): 18 imágenes en `hojas_reales/<clave>_a|b.jpg` (prompts en
  `_prompts_reales.py` → `prompts_reales.json`). Elegidas: h01 b, h03 b, h08 b (sin figura humana bajo las manos), h11 a, h13 b
  (orco gris con armadura roja, 7 figuras en 2 filas), h14 b, h15 a, h16 b (la a tiene fondo crema), h17 b (BORRAR la fila de
  texto de abajo antes de recortar). Comparativa `previews/hojas_reales_elegidas.jpg` enviada; hojas/ y piezas/ SIN TOCAR.
  ⚠ h14 nueva = Isillien JOVEN (Mano de Plata): IS se usa después como Gran Inquisidor (culpa_2, en_suenos 6-15) → meterla como
  hoja aparte (código nuevo, p. ej. IJ) solo para costasur. ⚠ h03 nueva = Renault pelirrojo (como el real); h04 (RS) sigue
  moreno → regenerar también h04 para que no cambie de cara. Al aprobar: copiar a hojas/<clave>_a.jpg (respaldar las viejas),
  `pegaflow.py recortar gaia_crematoria <hoja>` (hoja=N), MIRAR `_indice.jpg` y remapear códigos en plan.py; h08 ya no
  necesita el arreglo de 03.png; rehacer segmentos y avance.
  ▶ SIGUIENTE: el usuario ve el avance y decide (1) visto bueno → `fab.py gaia_crematoria video` COMPLETO; (2) si quiere la
  regeneración Flow con ingredientes reales, hacerla ANTES del render completo y rehacer los segmentos de esos actores.
  FALTA, en orden: (a) cuando acabe el render en curso, borrar `segmentos/seg_0250.mp4`…`seg_0255.mp4` (plaga 6-7,
  751-768 s: pudieron salir con la DA4 vieja) + cualquier segmento de la n.º 3 → `python fab.py gaia_crematoria video
  --hasta 798` (en segundo plano). (b) n.º 3 barato: añadir `real=[(slug, (frase, palabra))]` en tomas del acto 1 donde la
  voz nombra a un personaje con actor de Flow y aún sin foto real (p. ej. juicio_13/14 Eitrigg, juicio 1-5 Tirion); ver
  `python _tiempos_7a.py`; firmas `real(...)` en escenas.py:293. Contar las piezas de Flow que convendría regenerar con la
  imagen real como ingrediente y PROPONERLO al usuario (no lanzarlo). (c) copia ligera ffmpeg desde
  `salida/gaia_crematoria_AVANCE.mp4` → `AVANCE_ligero.mp4` (NO `_avance.py`) → `fab.py avisar` + mensaje. NO render completo
  sin el visto bueno final del usuario.
- ✏ CORRECCIÓN 7a n.º 2 del usuario (29-oct): «eso se ve raro, la espada arriba no pertenece» = toma con el caballero de pelo negro
  y armadura plateada con tabardo morado tendido/sentado entre ruinas, cielo verde de la Plaga: encima flota SOLA una pegatina de
  espada rúnica verde con calavera (la Agonía de Escarcha / espada del Rey Exánime, cortada en diagonal). Quitar esa pegatina de
  la toma (o, si el guion la nombra ahí, ponerla con sentido: en la mano o como objeto que cae, no flotando cortada). Revisar
  además el caballero: su pegatina trae un BORDE RECTO a la izquierda (mismo fallo de recorte que tuvo el hijo; rehacer el recorte).
  Localizar la toma con grep en `plan.py` de la pieza de la espada.
- ✏ PEDIDO n.º 3 del usuario (29-oct), «cuando se pueda»: si hay imagen REAL del personaje del juego, usar esa pegatina en lugar
  de la de Flow; las poses que falten, pedirlas a Flow con la imagen real como ingrediente; lo mismo con los lugares (la
  Crematoria real como ingrediente) y más elementos reales. Aplicarlo en el acto 1 donde salga barato (cambiar piezas de Flow por
  `piezas/reales/` en las tomas en las que el personaje está quieto o en primer plano); la regeneración en Flow con ingredientes,
  proponérsela al usuario con cuántas piezas son antes de lanzarla. Regla fija en docs/estilo_pegatina_flow.md § 8, puntos 8-9.
- ▶ 29-oct 14:05: acto 1 RENDERIZADO (266 seg., 0-798 s) y avisado. ⚠ E: LLENO (1,9 GB libres): `_avance.py` falló sin espacio; el AVANCE bueno es `salida/gaia_crematoria_AVANCE.mp4` (3,4 GB, de render_parcial) y `AVANCE_ligero.mp4` (124 MB) se sacó de él. 14:20: `fab.py limpiar --publicados --borrar` liberó 12 GB → E: con 14 GB libres (cabe el render completo). Siguiente: el usuario lo ve → lo que pida se cambia y se rehacen solo esos segmentos (`--hasta 798`) → con su visto bueno, `fab.py gaia_crematoria video` COMPLETO (los mapas posteriores se rehacen solos: mg_mapa cambió; revisar en_suenos_4, cuya marca «torre» cae fuera de la toma). — el usuario: «termina todo en esta sesión hasta tener el MASTER»
- ⛔ 29-oct 11:25: render completo DETENIDO a propósito (217/865 segmentos hechos, ~10,8 min; `seg_*.tmp.mp4` borrados). El usuario vio
  el AVANCE (7,9 min, `_avance.py`) y pidió, ANTES de seguir con el video completo, rehacer y enseñarle **los primeros ~10 min hasta
  el cierre de acto más cercano**:
  1. **Mapas pixelados** (p. ej. «Tierras de la Peste del Oeste / Vega del Amparo», ~7:50): alejar el zoom para no ampliar el mapa más
     que su resolución (o buscar una fuente del mapa a mayor resolución).
  2. **Fotos REALES del juego** donde el guion lo permita: lugares y MÁS personajes (pegatinas reales, no Flow).
  3. **Escenas que existen en el juego** (p. ej. la **posada de Costasur**): varias fotos/capturas de ese lugar y momento en el juego,
     junto a la animación, como pegatinas o como mejor quede (capturas de gameplay con yt-dlp + cuadros, o wowpedia/wowhead).
  4. **Pegatina de personaje CORTADA**: el hijo de pelo negro y brazos cruzados (¿Renault?), delante de las casas de entramado, sale
     cortado por un borde recto SIEMPRE, desde la primera vez que aparece (el usuario: solo ese, el niño de al lado está bien) →
     el fallo está en su pegatina/recorte de la hoja de Flow, no en una toma: rehacer ese recorte una vez y vale para todas sus tomas.
  → `video --rehacer <rango>` solo de ese tramo con audio completo → `_avance.py` → aviso → el usuario lo ve y decide qué más cambiar.
  Hasta su visto bueno NO relanzar el render completo (los cambios de mapas pueden tocar segmentos posteriores: revisarlos al reanudar).
- ◐ 7a en marcha (sesión hija, 29-oct ~12:10). Tramo = acto 1 entero (0 → 796 s, `complot` empieza el acto 2) = segmentos 0-265.
  ✅ (4) NI4 = `piezas/h07_darion_nino/04.png` recortado de la hoja **_b** (cuerpo entero; la _a lo pinta solo hasta los muslos: ese
  era el «borde recto»); original en `piezas/_respaldo/h07_04_orig.png`. ¡No relanzar `recortar` de h07 o se pierde!
  ✅ (1) `nucleo/mg_mapa.py`: nuevo `amp_max=2.0` (el zoom llegaba a 13,7x sobre mapas de 1024 px; Wowhead no tiene más resolución:
  `zoom/` = 772 px, `original/` = 1024). TODOS los mapas del video cambian → al reanudar el render completo, rehacer sus segmentos.
  Escalas viejas (máx.): elena/eitrigg/naxx/monasterio/ermitaño/capilla/epílogo 13,7x · costasur 7,9 · forja 6,2 · darion_busca 6,8.
  Ahora todos ≤ 2,0x (1,875x = llenar la pantalla con un mapa de 1024). ⚠ SIN verificar aún en cuadro: `fab.py gaia_crematoria
  escena eitrigg 470 474` y mirar que se vea el mapa entero, nítido, con la ruta y la foto.
  ⛔ Corte por contexto a las ~12:20 (hook 180 mil). FALTA, en orden:
  (2)+(3) Fotos reales nuevas. En warcraft.wiki.gg (API `api.php`, como `_bajar_reales.py`; añadir a `ARCHIVOS` y a `FOTOS` de
  `_reales.py`, luego `python _bajar_reales.py` + `python _reales.py`) hay: Costasur «Southshore.jpg», «Southshore Town Hall.jpg»,
  «Southshore battle.jpg», «Southshore Guard.jpg», «Southshore Crier.jpg» (no hay archivo «Southshore Inn»: para la POSADA, capturas
  de gameplay de la posada de Costasur con yt-dlp + cuadros, o Old Hillsbrad «Tarrenmill.jpg»); Rémol «Brill.jpg», «Brill Town
  Hall.jpg»; Vega del Amparo «Hearthglen Reforged.jpg», «Hearthglen in Cataclysm.jpg»; «Mardenholde Keep (original).jpg»; Forjaz
  «The Great Forge.jpg», «Ironforge - Classic cinematic.jpg»; Stratholme «Chronicle3 Arthas in Stratholme.jpg»; Kel'Thuzad humano
  «Kel'thuzadhuman.jpg» (mejor que el lich en mano_plata_6); Renault «Commander Mograine.jpg»; Dathrohan «Saidan Dathrohan
  comic.jpg»; Isillien «Isillien Past.jpg»; Gavinrad «Gavinrad the Dire.jpg»; Uther «Uther the Lightbringer.jpg».
  Dónde (plan.py, `real=`): gancho_3 darion · gancho_7 renault · gancho_8 taelan · elena_1 Rémol · mano_plata_5 Andorhal ·
  mano_plata_6 KT humano · costasur_1-6 VARIAS de Costasur/posada (idea: extender `real()` de escenas.py con un 4.º elemento
  dict {x, y, alto, dur} para poner 2-3 «polaroids» a la vez junto a la animación) · forja_1-3 Gran Forja · eitrigg_2-5 Vega del
  Amparo y Mardenholde · juicio_3 tirion/isillien · plaga Stratholme.
  ◐ Sesión 3 (29-oct): ✅ bajadas 19 fotos nuevas (`_bajar_reales.py`, slugs costasur*, remol*, andorhal, vega_amparo*, mardenholde,
  gran_forja, forjaz, cumbre_roca_negra, kelthuzad_humano, renault_comandante, dathrohan_comic, isillien_joven, uther_retrato;
  `vega_amparo_hoy` y `costasur_batalla` NO sirven) + POSADA: recorrido pre-Cata yt `2Ya2f-WKBr4` (480p) en `medios/costasur/`,
  cuadros 108 s (fachada), 117 y 120 s (interior con chimenea) → `pegatinas/_orig/posada_{fuera,dentro,chimenea}.jpg`.
  ✅ `_reales.py` (FOTOS nuevas + gamma de Roca Negra) ejecutado → `piezas/reales/<slug>.png`.
  ✅ `escenas.py`: `real()` acepta x, y, alto, rot; en el plan, `real=[(slug, (frase, palabra) | s desde t0 | None, lado, {x, y, alto, dur})]`
  + NOMBRE_REAL de los slugs nuevos.
  ✅ `plan.py` (copia previa en `previews/_plan_antes_7a.py`): fotos nuevas en gancho_7 (renault_comandante), gancho_8 (taelan),
  mapa elena (Rémol→remol), elena_8 (renault), orbe_0 (cumbre_roca_negra), mano_plata_2 (+dathrohan_comic), mano_plata_6
  (kelthuzad_humano), mano_plata_7 (andorhal), mapa costasur (costasur), costasur_1 (posada_fuera + isillien_joven), costasur_2
  (posada_chimenea), costasur_6 (posada_dentro), mapa forja (forjaz), forja_3 (gran_forja), forja_5 (vega_amparo), mapa eitrigg
  (Vega→tirion, Mardenholde→mardenholde; marcas eitrigg_0 «tirion» + eitrigg_1 «caballero»: la vieja caía FUERA de la toma),
  eitrigg_2 (+mardenholde). ⚠ SIN PROBAR: importar escenas falla fuera de fab.py (config importa `guion` del cwd); usar
  `python fab.py gaia_crematoria escena <id> t…` y comprobar que cada palabra clave (creció, martilló, fortaleza, saidan, cumbre,
  vega, caballero) exista en la frase (tk lanza error si no).
  Luego: `fab.py gaia_crematoria escena <id> t…` de cada toma tocada (MIRAR) → checkpoint → `video --rehacer 0-798` (con audio
  completo; mezcla ya hecha) → `python _avance.py` (une seg 0-265) → `fab.py avisar` + mensaje al usuario. NO render completo.
  ✅ Sesión 4 (29-oct ~12:45): hojas a 640x360 de las 13 fotos nuevas y los 5 mapas del acto 1 MIRADAS: todo bien salvo los mapas de
  las Tierras de la Peste (Vega del Amparo, Mardenholde y Stratholme están en el borde norte: su marcador quedaba bajo el título y sin
  nombre) → `nucleo/mg_mapa.py`: el título se desvanece justo antes del marcador que tapa y le cede el sitio al nombre (vale para
  todos los videos). PEGATINAS VIAJERAS (el usuario, 29-oct: «cuando se movilicen unidades o personajes en el mapa, pegatina pequeña
  en la ruta del o los personajes reales del juego») → `mg_mapa.mapa(..., viajeros=[png, ...])`: pegatina redonda con la imagen
  real en la punta del trazo (fila detrás si son varios), bajo marcadores; los nombres la esquivan. Puestas (7.º elemento del
  mapa en plan.py): costasur (alexandros_vivo), forja (alexandros_vivo + ribalimpia), darion_busca (darion), en_suenos (taelan),
  epilogo (tirion_highlord + darion); hojas miradas. ⚠ en_suenos_4: la marca «torre» (en_suenos_5) cae DESPUÉS del fin de la toma:
  la ruta no llega a dibujarse; revisar al reanudar. Segmentos 0-216 viejos BORRADOS; a las 12:46 lanzado `fab.py gaia_crematoria video
  --hasta 798` (render_parcial → `salida/gaia_crematoria_AVANCE.mp4`; log `render_7a_log.txt`). Al terminar: `python _avance.py`
  (copia ligera) + `fab.py avisar` + mensaje. Script de tiempos de prueba: `_tiempos_7a.py`.
  ◐ Sesión 5 (29-oct ~12:50-13:06): pedido nuevo del usuario: CLIPS DE VIDEO reales del juego (yt-dlp) donde el guion lo permita.
  ✅ Bajados a `medios/clips/` (créditos en `creditos.txt`) y recortados a `clips/<nombre>.mp4` (720p, sin audio, ≤ 8 s):
  posada_fuera (tour 106-112,8), posada_chimenea (115,5-121,5), posada_escalera (121,5-124,8) [Wowprecatarchive 2Ya2f-WKBr4] ·
  gran_forja (u4zjY06pcNU 358-364,5, Hazin221) · vega_amparo (asjxJXy3Hbw 14-22, TheWarcraftAtlas) · stratholme (tCwpCbnSWE4
  41,5-49, Thraex). Descartados: Andorhal y Capilla de la Luz (planos fijos).
  ✅ `escenas.py`: `CLIPS`, `_cuadro_clip`, `clip_real()` (polaroid de papel que REPRODUCE el clip + rótulo oro + «en el juego ·
  video: <canal> (YouTube)»); en el plan `clip=[(nombre, (frase, palabra) | s | None, {x, y, alto, rot, vel, dur})]`.
  ✅ `plan.py` (copia previa `previews/_plan_antes_clips.py`): costasur_1 posada_fuera (en lugar de la foto) · costasur_2
  posada_chimenea (quita fotos chimenea/salón) · costasur_6 posada_escalera en «escalera», vel 0,7 (quita foto posada_dentro) ·
  forja_3 gran_forja · forja_5 vega_amparo · plaga_5 stratholme. Ambos compilan. ⚠ SIN PROBAR EN CUADRO.
  ⚠ Editados a las 13:05:45 CON EL RENDER EN MARCHA (iba en 58/266): los obreros se reciclan cada 4 tareas y ya cargan el código
  nuevo. Segmentos de las tomas con clip: 108-113 (costasur_1/2), 120-122 (costasur_6), 135-138 (forja_3), 141-145 (forja_5),
  247-250 (plaga_5).
  FALTA, en orden: (1) YA: `python fab.py gaia_crematoria escena costasur 328 337 362` (y forja 410 428, plaga 746) → MIRAR a 640x360;
  si `clip_real` falla, arreglarlo enseguida (el render en marcha lo usa) y vigilar «Traceback» en `render_7a_log.txt`.
  (2) Esperar «listo: salida/gaia_crematoria_AVANCE.mp4» en el log (Bash en segundo plano con until-loop; ~14:15).
  (3) Borrar los `segmentos/seg_NNNN.mp4` de esas tomas con hora < la del último arreglo de código y relanzar
  `python fab.py gaia_crematoria video --hasta 798` (solo rehace los que faltan). (4) `python _avance.py` → 4-6 cuadros a 640x360
  (negros, mapas, viajeros 320-325 y 383-389 s, clips) → `python fab.py avisar "El acto uno de La Crematoria ya está listo para que
  lo veas"` + mensaje (mapas nítidos ≤ 2x con título que cede el sitio, 19 fotos reales + 3 capturas de la posada, niño de pelo negro
  de cuerpo entero, pegatinas viajeras, y los 6 CLIPS reales del juego). (5) Fila 7a → «◐ esperando visto bueno del usuario»; el
  render completo SOLO tras su visto bueno (mapas posteriores se rehacen: mg_mapa cambió).
  ✅ 14:06 render parcial LISTO (266/266, `salida/gaia_crematoria_AVANCE.mp4`, 3,4 GB, CON audio, 798 s). Hojas de los clips miradas
  (costasur 328, plaga 747: bien). Los 22 segmentos con clip son posteriores a la edición: NO hay que rehacer nada.
  ⛔ E: LLENO (0 bytes): `_avance.py` falla («No space left»); dos `_avance.py` a la vez (otra sesión, ffmpeg PID 7632 de las 14:07,
  atascado) dejaron `salida/AVANCE.mp4` truncado (2,1 GB, bloqueado). Arreglo: matar ese ffmpeg, borrar `salida/AVANCE.mp4` (es una
  copia sin recodificar de gaia_crematoria_AVANCE.mp4, sobra) y sacar SOLO la copia ligera desde `gaia_crematoria_AVANCE.mp4`
  (`ffmpeg -i salida/gaia_crematoria_AVANCE.mp4 -vf scale=1280:-2 -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 160k
  -movflags +faststart salida/AVANCE_ligero.mp4`). Liberar E: (p. ej. `fab.py limpiar --publicados`) antes del render completo.
- Hecho y listo para el cierre: `salida/miniatura.jpg` (`_miniatura.py`), `youtube.json` (título, capítulos, fuentes), eco de ultratumba
  (`_ultratumba.py`, 26 frases; originales en voz/final_orig), `audio/fx.wav` (`_sfx_juego.py`, 174 sonidos), `audio/final.wav`.

## Decisiones con el usuario (29-oct-2026)
- Canal: Gaia Eterna (de su esposa). Narradora = su voz clonada (probadas 19 emociones con corchetes: «suenan bien»).
- Tema elegido entre 3 propuestas con datos (`canales/formula/gaia_eterna.md`): La Crematoria, terror + heroísmo, 40 min MÍNIMO.
- Pedido: mapas reales con ruta en algunas escenas, VARIAS VOCES de ElevenLabs para los personajes con emociones, SFX DEL JUEGO.

## Voces
- Narradora: `BwV6RplmLHPGm7QVf6II` («Zyan gameplay 2», clonada, SOLO cuenta 2; `tts_eleven.post` ya salta de cuenta con
  `voice_not_found`). eleven_v4_turbo, stability 0,5. Pruebas: `videos/gaia_prueba_voz/`.
- Casting (`_prueba_personajes.py`, `muestras_personajes/todas.mp3`, 2 candidatos por personaje, 350 créditos):
  Alexandros salvatore/elder · Tirion arturo/elder · Renault enrique/antonio · Darion alejandro/david · Taelan david/antonio ·
  Isillien murdock/odran · Kel'Thuzad ivan/mordred · Rey Exánime miguel/final_boss · Eitrigg ragnar/ludovico (todas en español).
- ELEGIDAS por el usuario (29-oct, página `casting.html` en `localhost:8773`, launch «casting-crematoria»):
  Alexandros Salvatore `t3eeeqhBjrUqcrPvDqUn` (eligió Elder para los dos padres; el usuario dejó Elder a Tirion) · Tirion Elder
  `gSYqSbtMajxq5LUT0bNl` · Renault Enrique Mondragón
  `iDEmt5MnqUotdwCIVplo` · Darion Alejandro `byWOh4ohcovt7I8koF2I` · Taelan Antonio `htFfPSZGJwjBv1CL0aMD` · Isillien Murdock
  `OLmSqlYzB06EIKJRy5b0` · Kel'Thuzad Mordred `UFO0Yv86wqRxAt1DmXUu` · Rey Exánime Miguel `k8cFOyAg7B9qwBlDDNTC` · Eitrigg Ludovico
  `GTY55jD77hLBRrnQOhNk`.

## Guion (29-oct)
- `guion.py` aplana `actos_1/2/3.py` (cada frase str = narradora, tupla (personaje, texto) = VOZ_POR_FRASE con `VOCES`); `plan` de
  cada acto = imagen/mapa/SFX para el tramo de escenas. Lectura para el usuario: `guion_lectura.md` (regenerar si se edita).
- Canon = cómic «Ashbringer» + Chronicle 3 + misiones; lo de Classic desplazado se cuenta como «lo que vivieron los jugadores».
  Diálogos = adaptaciones (las líneas oficiales en español no se pudieron verificar). Voces con eco en la mezcla: Kel'Thuzad y el Rey.
- Música: BANDA SONORA OFICIAL de WoW (el usuario, 29-oct) → `armar_musica_ost.py` (secciones por escena; lista de pistas en su docstring).

## Tiempos (timeline.json, 29-oct)
- gancho 0 · bienvenida 80 · elena 109 · orbe 178 · mano_plata 233 · costasur 316 · forja 382 · eitrigg 466 · juicio 556 ·
  plaga 709 · complot 796 · traicion 873 · testigo 978 · naxxramas 1040 · susurros 1142 · culpa 1178 · cta_mitad 1240 ·
  darion_busca 1269 · monasterio 1356 · misterio 1436 · ermitano 1505 · taelan_hijo 1589 · recuerdos 1676 · en_suenos 1778 ·
  capilla_1 1909 · acherus 2044 · alba 2102 · epilogo 2389 · cierre 2542 → 2594,5
- `audio/` es carpeta REAL en C: (E: dio Ntfs 55 el 28-oct); `voz/` sigue en E: (pasarla a C: antes del render).

## Lecciones de este video (solo lo no obvio)
- 43 min de pegatina Flow en UNA sesión: en vez de escribir tomas a mano (Darrowshire: 3 200 líneas para 13 min), un MOTOR
  por datos (`escenas.py`) + `plan.py` (una línea por toma: escenario, cámara, luz, actores con códigos de 2 letras, ambiente, reales,
  iconos, rótulos, mapas, SFX). La PLACA de quien habla (medallón + nombre en oro) sale sola de PERSONAJE_POR_FRASE.
- El navegador integrado NO comparte el portapapeles de Windows: el paquete de Flow se inyecta directo en `javascript_tool`.
  Enviar con clic por código al botón «Iniciar generación» NO envía: hace falta la tecla Enter real.
- Columnas de luz recortadas de Flow se ven como papel: rayos procedurales aditivos (`columnas_luz`).
- `_muestras.py --rango` debe pasar `float` (np.float64 en `t` vuelve float64 los mapas de cv2.remap y truena).
- `fab.py nuevo --help` CREA un video llamado «--help» (borrado: junctions primero con rmdir).
- Whisper oye «Lord Dairon» por Lordaeron y «Mugrain/Mowgrain» por Mograine → ALIAS_QA.
- 1.ª `seleccionar`: 78 «fallos» y casi todos eran NOMBRES (Tyrion Badin, Eitrig, Renaud, Balnazar, Rivalimpia, Thailand…):
  ALIAS_QA con claves YA normalizadas (sin tildes ni apóstrofos) y `seleccionar` otra vez (reusa `voz/eval.json`, no gasta).
  Solo 8 eran tropiezos reales («caudeada», «abuelada», «volvieron a Vlad», «Uy» por «Hoy») → otra semilla (~170 créditos).
- Filtro de ElevenLabs (403 content_against_policy): «Si he de morir, quiero morir de pie, contigo» (Darion joven) → reescrita.

## Cierre (regla del 12-oct-2026)
- [ ] subido y PROGRAMADO en el hueco del canal, miniatura y registrado (`canales/gaia_eterna.json`, BITACORA)
- [ ] HALLAZGOS documentados (docs/estilo_pegatina_flow.md, canales/formula/gaia_eterna.md)
