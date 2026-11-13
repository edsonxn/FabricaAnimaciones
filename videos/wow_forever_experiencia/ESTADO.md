# 30 cosas para vivir la experiencia REAL de WoW Forever — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · lun 23-nov-2026 09:00 CDMX (hueco de `canales --actualizar` del 12-nov) · **SIN Overgear (el usuario, 12-nov: «Sin Overgear, que sea así, sin promoción»)**
- estilo: secuencia_yt (gameplay por beat + pegatinas + MG + mapas con ruta + Overgear con fondo de marca) → doc: docs/estilo_secuencia_yt.md · copiar de `videos/wow_errores_30_60/` (lo más nuevo)
- etapa: SUBIDO y programado (https://youtu.be/CKBm0KBaM60, mar 17-nov 09:00 CDMX; versión con los 8 arreglos del usuario)
- siguiente: Studio (monetización + cuestionario de idoneidad); a los 7 días, métricas → `canales/formula/cronicas_warcraft.md`

## Sesiones (UNA sesión directo al MASTER, regla 5-nov; relevo si corta a 180 mil)
- alias: experiencia real de Forever, las 30 cosas, tómatelo con calma, el de Joseju
- vista previa: no; render a la tele solo (regla 5-nov)
- leer al empezar: este ESTADO.md · `videos/_investigacion_wow_forever_experiencia.md` · guion de referencia en el scratchpad (Joseju)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | referencia + canal + comentarios + investigación + guion v1 + voz lanzada + pegatinas/mapas + borrador de efectos | ◐ 12-nov (corte a 180 mil) | sigue en la sesión de relevo |
| 2 | correcciones + sin Overgear + voz + clips (60 rehechos) + chequeos + fx hoja + OST + render + miniatura Flow + subida | ✅ 12-nov | RSDta9FSn9c, lun 23-nov 09:00 |

## Decisiones del episodio (el usuario, 12-nov-2026)
- Idea del usuario: inspirado en «No salgo del WoW Forever ni a la calle» de **Joseju** (PGmkWXy9ANY, 10-nov, 370 mil vistas, 20 min):
  le gustó cómo narra y cómo presenta Forever como EXPERIENCIA (la fricción como virtud, lo social, el mundo grande, clases distintas).
  Nuestro video: **30 cosas que puedes hacer para vivir la experiencia real de WoW Forever** (como se jugaba Classic, no Retail):
  leveleo, rol, gente, mundo; «tómatelo con calma». Al revés de los videos de errores/consejos. **~30 min**, parte lista, parte análisis.
- Voz: Remy (Applio), la de siempre (ganó la votación). FONETICA de `wow_errores_30_60`.
- Overgear: NUNCA decir que correr/subir rápido/comprar boosts está mal: «hay muchas formas de jugar; esta es la otra».
- Comentarios (12-nov, 22 nuevos): críticas → @AlbertoHans-k7f8d («no puedo ni salir de Villa del Lago… este juego es imposible»),
  @Fetixe22 («addons de paga» → el nuestro es gratis), @arnoldhowardriberth8208 («quién paga para que le enseñen»); agradecimientos →
  @yorshnado8100, @AlexAnder-z1i7l, @pablisho6299, @sgto.sevilla6976, @PentaGRam8666; sugerencia @nicomedi93 (misiones tétricas del Bosque del Ocaso).
  Comprobar con `yt comentario` (≤ 10 días y no usados).

## En curso
- 12-nov ~13:30: investigación en un subagente → `videos/_investigacion_wow_forever_experiencia.md`.
- 12-nov ~14:10: `guion.py` v1 ✅ (39 escenas, 225 frases, ~4 970 palabras ≈ 30-31 min; borradores `_fijas.txt` + `_lista.txt`) · `voz` LANZADA → `_voz.log`.
  Al llegar la investigación: corregir datos (nombre es-MX de «The Great Outdoors», libros, naufragio, concurso de pesca) y regenerar solo esas frases.
  Música prevista (OST Wowmusicable): Elwynn 1yZNuUpTjTo · Posada Alianza rXdqWmp9FA4 (c17) · Bosque del Ocaso l8AlVcEvLEE (c13) · Baldíos Do5s0MQvF9s (c05) · Dun Morogh g2SZuqyjKtA · Teldrassil lXMguMnsyak · Durotar alWTyJr1Gro · Tirisfal IwlPgQtGguw · Ventormenta DUA1B3A1ZnY (c04, «escucha la música de la ciudad»).

- **12-nov ~15:00 CHECKPOINT (corte a 180 mil).** Hecho: investigación ✅ (`videos/_investigacion_wow_forever_experiencia.md`, 36 candidatos;
  léela por secciones con grep) · guion v1 ✅ (40 escenas, 225 frases; c27 se partió en c27/c27b con `post` 5,6 para oír el add-on;
  c04 con `post` 4,5 para oír la música de Ventormenta) · `voz` relanzada ~14:40 → `_voz2.log` (la 1.ª falló por un corte de Edge TTS;
  si vuelve a fallar, relanzar: reanuda) · 9 tarjetas `com_*` ✅ (en `pegatinas/`) · `_pegatinas.py` ✅ (personajes, íconos de objetos y
  hechizos; borradas las de lugares malas: lugares = `pant()` con capturas de los clips) · `mapas/` ✅ (Elwynn, Poniente, Ocaso, Baldíos,
  Trabalomas, Crestagrana, Claro de la Luna, Dun Morogh, Teldrassil, Azeroth…) · `sfx/` oye_willem + oye_kaltunk (add-on Voces) +
  mision_aceptada + subir_nivel · `medios/_overgear` copiado · `musica_wow.py` copiado (falta añadir las pistas tranquilas de arriba).
  Un SUBAGENTE escribe `_busquedas.py` (SRC por escena desde `_candidatos.txt`); si no quedó, hacerlo a mano copiando `_busquedas_ref.py`.
  **Añadir a SRC `"c27b": SRC["c27"]`** (escena nueva). Mirar las hojas de `medios` tras `bajar` (webcams, Retail, rótulos).
- **12-nov ~13:25 (relevo):** correcciones de la investigación APLICADAS a `guion.py` (24 cambios; c07 = Feria de la Luna Negra; respaldo v1 en el scratchpad) ·
  `efectos.py` ARMADO (helpers + cuerpo con anclas nuevas; c07 feria con mapa/calendario/Silas/boleto; c16 diablillo/tótems/oso/felina; c27b = grabación OBS g1
  sincronizada con `oye_willem`) · `_busquedas.py` ✅ (subagente; c07 con clips de la feria) · `voz` colgada en Edge TTS → matada, timeout de 90 s en
  `nucleo/tts_applio.py`, relanzada → `_voz3.log`. Pegatinas nuevas: silas, o_boleto, h_diablillo (Sayge solo hay arte de Hearthstone: NO usar).
- **12-nov (relevo) CHECKPOINT 2:** voz ✅ 219/219 (sin Overgear; frases reescritas por Applio: c09_0, c17_2, c17_4, c11_0, c03_3, c01_5, c01_6, c24_4, c25_2, c10_2, gracias2_3; `CER_MAX_POR_FRASE` con 28 transcripciones leídas) · idioma_voz ✅ 219 · tiempo ✅ 29:56 · beats ✅ 209 · busquedas.json ✅ · siguiente: `bajar -j 4` → hojas → promesas → chequeo → fx hoja → música → render.
  `nucleo/tts_applio.py`: Edge TTS con timeout 90 s, 4 en paralelo, caché persistente por texto en `voz/cands/_edge` (se borra al terminar), escritura atómica.
- **12-nov CHECKPOINT 3 (corte a 180 mil del relevo 1):** `bajar -j 4` LANZADO → `_bajar.log` (209 beats; si se cortó, relanzar: salta los medios que ya existen).
  Música OST ya bajada en `audio/wow/` (10 pistas Wowmusicable: Elwynn 1yZNuUpTjTo, Posada rXdqWmp9FA4, Ocaso l8AlVcEvLEE, Baldíos Do5s0MQvF9s,
  Dun Morogh g2SZuqyjKtA, Teldrassil lXMguMnsyak, Durotar alWTyJr1Gro, Tirisfal IwlPgQtGguw, Ventormenta DUA1B3A1ZnY, Claro de la Luna MwJ65pIfamE).
  Reparto decidido para `LYRIA["tramos"]` (≤ 175 s) + `TEMAS`/`_NOTA` de `musica_wow.py`: [intro,friccion] Elwynn · [c30,c29,c28] Dun Morogh ·
  [burla0,c27,c27b,burla1] Tirisfal · [c26,c25,c24] Elwynn · [c23,c22,c21] Durotar · [gracias1,c20,c19] Baldíos · [c18,c17] Posada ·
  [c16,c15] Claro de la Luna · [c14,c13] Ocaso · [c12,c11,gracias2] Teldrassil · [c10,c09,c08] Durotar · [c07,c06,burla2] Dun Morogh ·
  [c05] Baldíos · [c04] Ventormenta (post 4,5 s: «escucha la música de la ciudad») · [c03,c02] Elwynn · [c01,cierre] Ventormenta.
  Antes: comprobar canto (Ventormenta puede llevar coro) con `nucleo/ost_canto.py` o a oído; sin `reemplazos` (sin Overgear).
  `_promesas.py`/`promesas.md` ya reescritos para este guion (60 promesas). `youtube.json` borrador listo (sin Overgear, `__CAPITULOS__` por rellenar).
  Pendientes de material (aviso del hilo anterior): c29 menú de idiomas, c26 postes, c09 sacerdote resucitando, c20 tienda/venta, c21 muelles,
  c15 renombrar mascota, c04 Darnassus, c03 ventana de comercio, c07 Sayge (solo hay arte de Hearthstone: usar el clip de la feria).
- **12-nov ~15:05:** música ✅ (`LYRIA.tramos` 16 tramos + `musica_wow.py` → `fab.py musica` → `audio/musica.wav` 29:56); start_session rechazado (turno automático) → sigo en este hilo. `bajar` en curso (~scene-032).
- **12-nov ~15:40:** `bajar` ✅ 209/209 (10 fallos rehechos con --url) · hojas de medios 1-7 revisadas → `_rehacer.txt`; faltan hojas 8-11, luego rehacer con relleno PAL.
- **12-nov ~16:00:** las 11 hojas revisadas → 52 clips malos; rehaciéndolos con relleno sin comentarios (`_rehacer2.txt`, log `_rehacer2.log`). Después: `medios` y mirar SOLO esos, luego promesas/peg_check/chequeo/fx hoja.
- **12-nov ~16:30:** medios ✅ (60 clips rehechos y revisados; ojo: el canal Raf1994 5ArXTkfbt_0 trae recuadro de streamer) · `fx --seco` ✅ · apoyos ✅ · `_promesas.py` → `previews/promesas_01-05.jpg` (falta MIRARLAS) · `_peg_check.py` → `pegatinas_check_01-02.jpg` (falta MIRARLAS) · luego `chequeo`, `FAB_FX_FINAL=1 fx hoja`, sfx, mezcla, video.
- **12-nov ~17:00:** promesas 1-5 MIRADAS y arregladas (clips 71/120/186/194, MG reglas/calendario, sin APOYO bolsa, Mor'Ladim → pant colina_cuervo). Falta: mirar `pegatinas_check_01-02`, `chequeo`, `FAB_FX_FINAL=1 fx hoja`, sfx, mezcla, video.
- **12-nov ~17:20:** pegatinas_check mirado (súcubo boceto y Villadorada manga fuera; VS Retail fuera; +10 pegatinas) · `chequeo` ✅ (avisos de sonido c27b/c04 = falsos: OBS va por PISTA voz=True y la OST de Ventormenta suena en el post) · falta `FAB_FX_FINAL=1 fx hoja` y mirar, luego sfx/mezcla/video.
- **12-nov ~17:50:** `FAB_FX_FINAL=1 fx hoja` 6 hojas MIRADAS y arregladas (MG grupos/duplica/capas/bolsa/feria, comentarios encimados, clips 33/81) · LANZADO `fx` → `mezcla` → `video` → `final` (log `_render.log`). Después: tele master, verificar, miniatura, capítulos, subir.
- **12-nov ~18:10:** miniatura Flow ✅ `salida/miniatura.jpg` (op2: hoguera nocturna in-game, «30 COSAS / SIN CORRER AL 60», logo Forever; prompt en `prompt_miniatura.md`) · capítulos ✅ en `youtube.json` · render en curso (`_render.log`).
- **12-nov ~18:40:** MASTER ✅ `salida/wow_forever_experiencia_MASTER.mp4` (30:16 con pantalla final, 1,58 GB) · verificar ✅ (sin negros; hoja final mirada) · tele: falló (conexión cortada por la tele) · `yt subir … private --publicar 2026-11-23T15:00:00Z` LANZADO (`_subir.log`). Falta: registrar en `canales/cronicas_warcraft.json` → `canales --actualizar` → BITACORA → commit.
- **FALTA en orden:**
  1. **Correcciones de la investigación al guion** (luego regenerar SOLO esas frases con `voz`, que detecta texto cambiado):
     c22: Blizzard dice «hoguera» (no «fogata»), «hoguera básica» la crea Cocina, «tienda de campamento»; la misión NO tiene nombre es-MX
     → «con una misión sencilla hacia el nivel cinco»; 3 objetos, uno por jugador; beneficio al sentarse ≥ 1 min. ·
     c21: el concurso de pesca SÍ está en Forever: domingos 14-16 h, ahora lo completan los PRIMEROS 50, moneda exclusiva que se cambia con
     Jang en Bahía del Botín (quitar «en Classic»). · c13: es-MX = «La leyenda de Stalvan», **Stalvan Mantoniebla** (no Mistmantle; quitar
     su FONETICA), Lady Eva, Comandante Althea Cerranegro; Mor'Ladim es misión de grupo de 3. · c16: en Forever el brujo EMPIEZA SIN
     DEMONIO (diablillo por misión) y el druida aprende la FORMA FELINA al 20 por misión nueva (túmulo de espíritus de gato). ·
     c25: Hogger élite nivel 11 que NO se adapta; en Forever los objetos de misión se reparten por turnos en el grupo. · c18: «Caras
     conocidas»: quien agrupó contigo sale después con el nombre de otro color. · c24: legado «Explora todo el mapa del mundo con el mismo
     personaje»; en Elwynn no hay maestro de vuelo. · c08: el premio es la «Bolsa de dormir acogedora» (pasa por la presa de Loch Modan). ·
     **c07: cambiar libros por la FERIA DE LA LUNA NEGRA** (Elwynn 9-15-nov; vuelve el 7-dic a Mulgore, dos días antes de las bandas;
     Sayge da un beneficio de 2 h; el video sale el 23-nov → «la próxima, el siete de diciembre en Mulgore»). · c05: no está confirmado
     que el chat de Los Baldíos haya vuelto → «Los Baldíos vuelven a ser paso obligado de la Horda»; misión es-MX «Perdida en la batalla».
     · c06: Molino Tarren/Costasur sin confirmar en Forever → decirlo como leyenda de Classic. · intro_2: quitar «guías de nivel en tres
     días» como dato duro → «y gente que ya llegó al sesenta». · c02: añadir 1 frase de gráficos (iluminación secundaria en Bueno o más).
     · Opcional (análisis honesto): el 8-nov subió +50 % la XP de mazmorras; jugar solo es más rápido (sin tagueo compartido: Blizzard
     «hold the line»). Citas cortas de desarrolladores en la investigación (Greenfield, Zierhut) para `friccion`.
  2. Armar `efectos.py` = `_efectos_helpers.py.txt` (helpers copiados) + `_fx_cuerpo.py.txt` (FX ya escrito, anclado a las frases v1);
     ajustar anclas de las frases que cambien (c22 «Fogata», c07, c13 «Mistmantle», c16) y el MG `M.calendario` (firma: titulo, dia0,
     sem0, n, eventos, hoy). `python fab.py <v> fx --seco` y `FAB_FX_FINAL=1 fx hoja` (mirar TODAS las previews).
  3. seleccionar → `python nucleo/idioma_voz.py wow_forever_experiencia` → tiempo → beats → `_busquedas.py` → bajar (uno a la vez) →
     hojas de medios → promesas.md + `_promesas.py` → pegatinas_check → chequeo → música (tramos en guion.LYRIA + pistas nuevas en
     `musica_wow.py`: c17 posada, c13 Ocaso, c05 Baldíos, c04 Ventormenta) → sfx → mezcla → video → final → tele master → verificar →
     miniatura Flow (in-game real, texto de Nano Banana) → youtube.json (Overgear /CRONICAS/5, promoción pagada; crédito/inspiración no
     hace falta) → `yt subir … private --publicar 2026-11-23T15:00:00Z` → registrar → `canales --actualizar` → commit.

## En curso (12-nov, tras la subida)
- EL USUARIO MARCÓ UN ERROR: el mapa «AZEROTH · dónde empieza cada raza» (c28) pone Dun Morogh y Teldrassil en el mar. Las coordenadas de los mapas sobre `azeroth_eses` (c28, c23 ×2, c11, c10, c07 feria) se pusieron a ojo. Arreglo: medirlas en `videos/wow_errores_forever/mapas/azeroth_eses_rejilla.jpg` → `efectos.py` → `video` → `final` → `verificar` → subir en privado con la MISMA fecha (lun 23-nov 09:00 CDMX); RSDta9FSn9c queda en privado SIN fecha (no borrarlo) → registro → lección en docs/estilo_secuencia_yt.md § mapas.
- ~19:00: 17 coordenadas de `azeroth_eses` medidas en la rejilla y corregidas (comprobadas en `previews/_azeroth_puntos.jpg`) · re-render LANZADO (`_render2.log`).

- **~19:30: 7 ERRORES del usuario sobre el MASTER, TODO en una sola resubida (misma fecha; RSDta9FSn9c queda privado SIN fecha):**
  1. Mapas de Azeroth con puntos en el mar → ✅ 17 coordenadas medidas en la rejilla. 2. «Gratis» de Arnold en inglés + oraciones de 1-2 palabras → ✅ 9 frases reescritas y regeneradas (duraciones viejas en `_dur_viejas.json`, tomas viejas en `voz/_final_v1/`); falta seleccionar.
  3. Elwynn c26: «Mina de los Ecos» mal (es de kobolds, en Villanorte) → campamento gnoll Riverpaw real del Linde del Bosque. 4. Elwynn c24 «A PIE»: puente/granja/ruta falsos → ruta real Villadorada → Linde del Bosque → frontera de los Páramos (Granja Piedracampo, Viñedos Maclure, Guarnición de Arroyoeste), solo lugares reales.
  5. Revisar TODOS los mapas de zona con fuente (Three Corners 9.5,71 Marcy Baker; esposa de Mankrik ~49,50; naufragios; Colina del Cuervo; etc.). 6. Yorsh (gracias1_1, gracias1_2): Applio pasa al inglés → reescribir sin abrir con el nombre; revisar con Whisper por ventanas de ~3 s todas las frases con nombres.
  7. «Montes Crestagrana» → **Montañas Crestagrana** en voz, rótulos y youtube.json.
  Plan de audio: regenerar las frases y AJUSTARLAS a su duración vieja (atempo) sin rehacer `tiempo`/beats → `mezcla` → `video` (mapas) → `final` → `verificar` → subir.

- **13-nov ~00:30 CHECKPOINT de los 7 errores (+ c08 naufragio: en Forever NO hay naufragio, es una cadena Granja Alexston 37.1,50.1 → torre quemada de Los Baldíos 46.1,74.3 → … → presa de Loch Modan 49.5,12.9, según method.gg; c08_0/c08_1 reescritas):** voz ✅ (19 frases regeneradas, revisión de idioma por ventanas de 3 s ✅ con `_check_nombres.py`, idioma_voz ✅, ajustadas a su duración vieja con `_ajustar_duracion.py` sin rehacer `tiempo`/beats) · mapas ✅ (Azeroth medido en la rejilla; zonas con coordenadas con fuente de games.gg, warcraft.wiki.gg, method.gg y reinsofpain; revisados en `_hoja_mapas.py`) · Montañas Crestagrana ✅ · anclas de las frases cambiadas apuntan al texto VIEJO del timeline (a propósito) · LANZADO mezcla → video → final → verificar (`_render3.log`). Después: subir en privado con la misma fecha, dejar RSDta9FSn9c en privado SIN fecha, registro, commit.

- **13-nov:** MASTER v2 ✅ (mapas + voz + Crestagrana + c08), .srt corregido con el texto nuevo, subido CKBm0KBaM60 y reprogramado al mar 17-nov 09:00 CDMX por orden del usuario (después del último programado, «20 SECRETOS» del 14-nov). RSDta9FSn9c ya no existe. Pendiente: Studio (monetización + cuestionario).

## Hecho
- 12-nov: `nuevo --yt`, `canales --actualizar` (Warcraft BIEN, hueco 23-nov; canal que se queda antes sin video: Sapiens/Cuerpo en Neón atrasados), comentarios leídos.

## Lecciones de este video (solo lo no obvio)
- Edge TTS (Applio) se colgaba sin error y cortaba conexiones: `nucleo/tts_applio.py` ahora con timeout de 90 s, 4 en paralelo y caché persistente POR TEXTO con escritura atómica (una caché por nombre de frase reusó textos viejos y un mp3 a medias truncó 2 frases).
- Applio lee raro las frases cortas sueltas («Literalmente.», «Muere bien.», «Vívelo.»): unirlas con coma a la frase o alargarlas.
- Clips: 60 de 209 traían webcam, gráficos de otros canales (Raf1994 lleva un recuadro de streamer fijo) o Retail; el relleno sin comentarios de Forever (loJCGO2MTjc, 7sWSTsZu50c, UMh80-64QLc, dlGeYLM0RI8, I2waqOFv3JI puerto de Ventormenta) salva.
- Pegatinas de la wiki que NO son del juego: súcubo (boceto), Villadorada (manga), Mor'Ladim (figura) → fuera; Sayge solo tiene arte de Hearthstone.
