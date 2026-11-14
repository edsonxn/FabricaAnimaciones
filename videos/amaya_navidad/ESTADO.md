# Las MEJORES y PEORES cosas que pedir en Navidad — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: canal_amaya (canal NUEVO de Amaya, alta 10-nov-2026; el YouTube lo crea el usuario; nombre del canal: «Amaya Vibes» (sale en los videos de referencia de ella))
- estilo: SCRAPBOOK COQUETTE (nuevo): vichy/rayas rosa, letras recortadas, stickers de productos dibujados (Flow) — kit `nucleo/coquette.py` ✅ (sin probar), doc `docs/estilo_scrapbook_coquette.md` ◻; referencias en `canales/referencias/amaya/`
- etapa: guion ✅ · voz ✅ (lista de Amaya integrada) · escenas ✅ · fotos reales ✅ · SFX ✅ · música biblioteca ✅ (Lyria 402) · MASTER ✅ 9:29 · Short ✅ · miniatura ◻
- siguiente: (1) MINIATURA en Flow (Chrome, proyecto «nov 10 - 15:27»: avatar de Amaya + stickers de la lista + «15 SÍ y 10 NO» escrito por Nano Banana, estilo scrapbook coquette); (2) si hay saldo de Lyria: música coquette nueva en 5 tramos (`lyria_tramos.py manual` para regenerar el PROMPTS_AI_STUDIO.md, desactualizado) → `armar` → mezcla → final; (3) que el usuario/Amaya revise el MASTER; (4) NO subir hasta que el usuario cree el canal «Amaya Vibes» y lo diga; al subir: créditos de fuentes.json en la descripción y Short con #Shorts.

## Sesiones
- alias: amaya_navidad, navidad de Amaya
- vista previa: SÍ, el usuario pidió (10-nov) un avance del primer minuto con la voz para enseñárselo a Amaya
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | referencias, competencia, guion, voz, tiempo, kit, stickers | ◐ 10-nov | cortada por contexto (180 mil) antes de escribir escenas.py |
| 2 | escenas del avance + fusión con el estilo de Amaya | ◐ 10-nov | AVANCE 0-96 s entregado y APROBADO por Amaya («Sí, sigue») |
| 3 | escenas m13…cierre, lista de Amaya, fotos reales, MASTER, Short | ◐ 10-nov | MASTER ✅ 9:29 (salida/amaya_navidad_MASTER.mp4, verificado, hoja final_hoja.jpg mirada) + Short ✅ (salida/amaya_navidad_SHORT.mp4, 38 s, p1+m1) + copia _MASTER_cel.mp4 enviada al chat; tele apagada → aviso por voz. FALTA: miniatura en Flow · Lyria nueva si hay saldo · NO subir sin el canal |

## En curso (checkpoint 10-nov noche, sesión 3)
- HECHO sesión 3: dibujos.py (22 stickers por código: aguacate fresa martillo celular jabon esponja gel bloqueador dados pulsera(_b/_c)
  nube copo nota_musical bateria_llena/vacia lata claqueta tienda burbuja pulgar); escenas.py con SEC (piezas secundarias ancladas a
  la palabra), NOTAS de todos los ítems, MOD de m11…m1, `suscribe` (play rojo genérico + SUSCRÍBETE→✓ SUSCRITO + campana + mano) y
  `cierre` (repaso de los 25, globo de comentarios, like, suscribe, «Soy Amaya», pantalla final con 2 cajas); stickers *_solo (sin
  contorno fantasma) para bálsamo, sérum y audífonos pirata; sonidos nuevos en sonidos_navidad.py (clic campana flash spray crujido
  lata claqueta cajita). Script de stickers por código = `stickers_codigo.py` (NO llamarlo dibujos.py: choca con nucleo/dibujos).
- HECHO al final de sesión 3: `python sfx_proc.py` → audio/fx.wav ✅ (548 eventos). LYRIA en guion.py partida en 4 tramos (≤175 s) con
  escenas por intensidad; `lyria_tramos.py todo` → HTTP 402 SIN SALDO (escribió audio/PROMPTS_AI_STUDIO.md). Provisional del avance
  movida a audio/_provisional/ (musica_biblioteca.wav = la recortada de 97 s; lyria_tramo1.mp3 = biblioteca duo_promo__lyria_2).
- FALTA, en orden: (1) MÚSICA: avisar al usuario del 402 (recargar crédito de AI Studio o hacer a mano los 4 prompts de
  PROMPTS_AI_STUDIO.md → audio/lyria_tramoN.mp3 → `lyria_tramos.py armar`); mientras tanto, para no parar: `fab.py biblioteca sugerir
  amaya_navidad` → pieza coquette/suave de 536 s (o varias) → audio/musica.wav de duración exacta 536,1 s; (2) `fab.py amaya_navidad
  mezcla`; (3) `fab.py amaya_navidad video` (completo, 2.º plano, avisar al acabar) → `final` → `verificar` → hoja del MASTER;
  (4) `tele video amaya_navidad master` en 2.º plano + SendUserFile copia < 30 MB; (5) Short + miniatura Flow (Chrome, proyecto
  «nov 10 - 15:27»); (6) canales/canal_amaya.json («Amaya Vibes»), docs/estilo_scrapbook_coquette.md, fila en CLAUDE.md;
  (7) NO subir sin preguntar (el canal lo crea el usuario).

## Checkpoint anterior (10-nov tarde, sesión 2)
- CAMBIOS DEL USUARIO (10-nov, vía la sesión madre): canal = «Amaya Vibes» (con S). La narradora ES Amaya: gancho_0 «Soy Amaya»,
  bienvenida_0 «¡Bienvenida a Amaya Vibes!», cierre_1 «Soy Amaya, ¡y nos vemos…!» (voz regenerada, total 536,1 s). Fusión con SU
  estilo (canales/referencias/amaya/ref3-5 + hoja_amaya_3refs.jpg): letras recortadas PASTEL variadas (kit ya cambiado), vichy
  rosa-rojo/crema, SU AVATAR (propios/amaya_avatar.png, recortado de ref4 a los 6 s) como presentadora que reacciona, sus stickers
  (Flow: perrito negro, mora, bola disco, latte, libros, bebida rosa, labios, hortensia, estrella, moño, mariposa, labial, ramo,
  mano cursor, campana), listón «HAPPY WATCHING!!», final de suscripción tipo ref5 (YouTube rojo + «✓ SUSCRITO» + campana + mano).
  Música: carácter de «Coquette playlist» (Valentine, music.youtube Q2UOijZ0_JQ) SOLO como referencia; nunca esa pista.
- HECHO en sesión 2: comun.py (ww + stk() que limpia restos del recorte), escenas.py REESCRITO con la fusión (gancho con «Soy Amaya»
  + avatar que parpadea/salta/niega (propios/amaya_avatar*.png), bienvenida «¡Bienvenida a / Amaya / Vibes» + listón HAPPY WATCHING!!
  + sus stickers; plantilla item() con adornos DECOS, avatar que se asoma al sello, MOD con pre/encima; m15 aplasta/estira, m14
  scrunchie vuela, p10 clip al candado + libreta), _hoja.py. Kit coquette: letras PASTEL (PAPELES nuevos) + fondo «vichy_amaya» +
  esquinas más visibles. Stickers nuevos de Amaya en stickers/ (Flow hojaH_2/I_1/J_1): perrito_negro mora bola_disco latte libros
  bebida labios hortensia estrella mono mariposa labial ramo mano campana taza_mono leche_fresa (brillos = mal recortado, no usar).
  Hoja del gancho mirada (previews/hoja_g.jpg): bien; «Soy»/«Amaya» chocaban → movidos (sin re-mirar). previews/hoja_b.jpg (bienvenida)
  y la de ítems SIN mirar todavía.
- HECHO también: hojas b e items miradas (sello movido a (560,770)); sonidos_navidad.py + sfx_proc.py → audio/fx.wav (281 eventos);
  música PROVISIONAL = biblioteca duo_promo__lyria_2 → audio/musica.wav (ffmpeg, recortada); LYRIA en guion.py (1 tramo: partirlo
  en ≤ 175 s para la Lyria nueva); mezcla ✅; render del avance lanzado 16:03 (`video --hasta 97.2`, log previews/_render_avance.log).
- FALTA (lo de abajo ya está hecho hasta el punto 3): (1) mirar previews/hoja_b.jpg y `python _hoja.py items 43.2 45.2 47.2 48.3 53.2 56.2 62.8 67.2 73.4 77.0 79.0 82.2
  85.2 89.1 89.7 91.7 94.7` (tiempos de sesión 1 + 1,2 s) y arreglar choques; (2) sonidos_navidad.py: copiar sfx_proc.py y
  sonidos_base.py de ../amaya_independencia y sintetizar los nombres de escenas.EV (pop, pop_avatar, cae, letras, sello, etiqueta,
  nota, acierto, bajon, tv, rasgado, whoosh, destello, megafono, boing_triste, cinta, misterio, ding, corazones) → audio/fx.wav;
  (3) música provisional: `python fab.py biblioteca sugerir amaya_navidad` (carácter coquette: piano, caja de música, pop suave);
  (4) avance 0-97,2 s (p10 termina en 97,2): `python fab.py amaya_navidad video --hasta 97` + mezcla → tele en 2.º plano
  `python fab.py tele video amaya_navidad avance --pregunta "¿Le gusta a Amaya?" --opciones "Sí, sigue|Cambiar algo" --esperar 900`
  + SendUserFile; (5) con su visto bueno: resto (suscribe = final tipo ref5 con mano/campana/«✓ SUSCRITO»; cierre), Short,
  miniatura Flow, canales/canal_amaya.json («Amaya Vibes»), docs/estilo_scrapbook_coquette.md, fila en CLAUDE.md.

## Checkpoint anterior (10-nov ~16:00)
- HECHO: guion.py (29 escenas; LISTA = id → (m/p, número, precio, nombre en pantalla)); voz/final + timeline.json; `nucleo/coquette.py`
  (fondo vichy/rayas, pegar() con sombra en recuadro, sticker(ruta, alto), texto, contorno_texto, rotulo_recorte (letras de
  revista que caen), esquinas (papel rasgado + periódico), golpe_sello/temblor, cuelga_etiqueta ($/$$/$$$), cinta (washi),
  pega_nota (notita Ink Free), destellos, corazon, cursor, tv (barras de color + glitch), rasgado (barrido de papel), acabado).
- Stickers (stickers/<nombre>.png, contorno blanco ya puesto por Flow): squishy pinzas scrunchies diario(_a) cuentas agenda tarjeta
  calcetines carta cajon cerezas megafono regalo baston arbolito gatito galleta chocolate esfera bodymist lampara paleta pantuflas
  sudadera bocina bolsa bebe balsamo canasta termo audifonos_pirata oso croissant perrito controles serum crema audifonos camara
  fotos rollo calcetin_nav1/2 calcetin_reno1/2 clip sello_goma (+ variantes _b/_a). Hojas originales en flow/, proyecto Flow «nov 10 - 15:27».
- FALTA, en orden: (1) escenas.py del video: `Mundo(Escena)`, `cuadro(t)` como `videos/amaya_independencia/escenas.py`, anclas
  con ww(esc, frase, palabra) de un comun.py igual al de amaya_independencia; plantilla genérica de ítem: «MEJOR/PEOR» + número
  en letras recortadas arriba a la izquierda, sticker grande que cae a (1180,560) alto ~560, cinta con el nombre abajo, etiqueta
  de precio al empezar la frase 1, sello al empezar la frase 2 (mejor=vichy rosa + «¡SÍ PÍDELO!»; peor=rayas_gris + «NI SE TE
  OCURRA», sticker que tiembla), notitas ancladas a palabras (dict NOTAS por ítem), esquinas(), destellos; transiciones: rasgado
  entre ítems, tv() al pasar a un peor y del gancho a la bienvenida. Ideas por escena: gancho = megáfono + «¡HOLA, HOLA!» en
  recortes, arbolito/regalo en «Navidad», calcetines con «¡OTRA VEZ NO!» en 6,4 s, «15 MEJORES» / «10 PEORES» en 9,7/12,4 s,
  carta en 16,4 s, cajón con cinta «SECRETO» en 19-21 s · bienvenida = «¡Bienvenida a mi canal!» en recortes (como ref1),
  sello verde 26,5 s, rojo 29,2 s, tres etiquetas $ $$ $$$ 32,4 s · m15 = el squishy se APLASTA en «aplastas» (45,7) y se
  ESTIRA en «estiras» (46,8) · m14 = un scrunchie sale volando en «vas a perder» (77,2) · p10 = el clip vuela al candado en «clip» (87,8).
  (2) hoja de prueba `python _hoja.py <x> t…` (copiar _hoja.py de amaya_independencia) y mirarla; (3) render del avance 0-96 s
  (`python fab.py amaya_navidad video --hasta 96` + mezcla provisional con música de la biblioteca: `fab.py biblioteca sugerir amaya_navidad`)
  y `python fab.py tele video amaya_navidad avance --pregunta "¿Le gusta a Amaya?" --opciones "Sí, sigue|Cambiar algo" --esperar 900` en segundo plano;
  (4) resto de escenas, SFX, música Lyria/biblioteca, MASTER, Short, miniatura en Flow; canal: `canales/canal_amaya.json` aún NO existe.
- Investigación: competencia MX (Sweetly Girl 846 mil, Alondra Tejeda 992/461 mil); guías de regalos 2026; humor: sin memes dudosos.

## Referencias de Amaya (10-nov, 15:45) — FUSIONAR con el kit
- `canales/referencias/amaya/ref3_amaya.mp4`, `ref4_amaya.mp4`, `ref5_amaya.mp4` (hoja `hoja_amaya_3refs.jpg`): «Amaya Vibe / Hello» y «WELCOME TO MY VLOG!» con letras recortadas PASTEL variadas, SU AVATAR (chica ilustrada de pelo largo oscuro y playera blanca, abajo a la izquierda), stickers (perrito negro, mora, bola disco, café latte, libros, bebida rosa, labios, flores azules, estrellas, moños, mariposa), cintilla «HAPPY WATCHING!!», final de suscripción (logo de YouTube + botón SUBSCRIBE + campana + mano que da clic).
- Música que le gusta: https://music.youtube.com/watch?v=Q2UOijZ0_JQ («Coquette playlist», Valentine). Solo de referencia; NO usarla en el video (derechos): Lyria o biblioteca con ese carácter.
- RENDER COMPLETO lanzado 17:08 (10-nov): música de biblioteca (chicle_dentro t3 · cinco_bichos t3 · duo_promo 2 · chicle_dentro t1) armada + mezcla ✅ (−14 LUFS); log previews/_render_full.log. Al acabar: final → verificar → tele master.
- 10-nov ~17:30 · CAMBIO DEL USUARIO (vía sesión madre): entra la LISTA ESCRITA A MANO POR AMAYA (canales/referencias/amaya/lista_amaya_1/_2.jpg).
  Render completo DETENIDO. guion.py cambiado (copia previa: guion_antes_lista_amaya.py): m12 → BLOQUEADOR + CREMA, m10 → PRODUCTOS PARA
  EL CABELLO, m8 → KIT DE EMERGENCIA, p9 → TINTES DE FANTASÍA (todas nuevas, «esta la puse yo»); crédito en p8 (maquillaje muy
  cargado), p2 (skincare de adultos), m7 (bolsa o mochila), m6, p7 (ropa de tu mayor gusto), p5 (higiene que tú escoges sí vale);
  cierre_1 con su «espero les guste… Byeee». Sérum de pestañas FUERA (prostaglandinas: irritan y pueden cambiar el color del ojo).
  FALTA: voz --solo de m12_0-2 p9_0-2 m10_0-2 m8_0-2 p8_0-1 m7_0 p7_2 m6_0 p5_2 p2_0 cierre_1 → seleccionar → tiempo → stickers por
  código nuevos (kit, cepillo, aceite, tinte, gis, mochila, insignia «elegido por Amaya») → escenas m12/m10/m8/p9 nuevas + anclas
  (CI.bye2 ya no existe) → sfx_proc → música armar (tiempos nuevos) → mezcla → video → final.
- 10-nov · LISTA DE AMAYA METIDA: voz de 20 frases ✅ (seleccionar ok; cierre_1 con tolerancia por su «Byeee»), tiempo ✅ (568,8 s = 9:29),
  stickers por código nuevos ✅ (kit cepillo aceite crema_peinar tinte gises mochila curita desodorante toallitas sol), escenas ✅
  (m12/m10/m8/p9 nuevas, insignia «elegido por Amaya ♡» = CREDITO en escenas.py, relleno del cierre; hojas miradas), SFX ✅ (575),
  música biblioteca en 5 tramos ✅ (tramo 2 partido) + mezcla ✅. RENDER COMPLETO relanzado (log previews/_render_full.log).
  Sigue: final → verificar → hoja MASTER → tele master → short.py → miniatura Flow → avisar.
- 10-nov · FOTOS REALES (pedido del usuario vía sesión madre): Commons con licencia libre (fotos_buscar.py → fotos/cand/, foto_prep.py →
  stickers/foto_*.png en polaroid/recorte/revista; créditos en fuentes.json). AMBOS (sticker y luego foto): m15 squishy, m5 termo, m4 oso,
  m2 audífonos, m1 cámara; SOLO FOTO: p8 maquillaje (principal), p4 pirata (principal) + original; m3 parchís real en «juego de mesa».
  Sin foto válida (solo personas reconocibles o logo grande): tintes, bloqueador, bolsa → sticker. Identidad comprobada en
  previews/pegatinas_check.jpg ✅. SFX 581 + mezcla ✅. RENDER COMPLETO relanzado (previews/_render_full.log). Lyria sigue en 402.
