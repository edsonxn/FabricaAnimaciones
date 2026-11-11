# Gen.G vs BLG: todo antes de la GRAN FINAL de la Worlds 2026 (~25 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Crónicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; subida por Studio en el navegador, NO está en la API) · publicar **jue 12-nov** (el usuario, 10-nov: deja respirar el resumen de semis del 10-nov); final sáb 14-nov 19:00 UTC (13:00 CDMX), Barclays Center, Bo5
- estilo: análisis táctico (secuencia_yt + VOD + `mg_tactica` + `mg_lol` + 3D `nucleo/tactica3d`) → doc: docs/estilo_analisis_tactico.md § GUÍA RÁPIDA · copiar de `videos/lol_semana2/` y `videos/lol_worlds_2026/j6_3d.py`
- etapa: ✅ SUBIDO por Studio y PROGRAMADO jue 12-nov-2026 10:00 CDMX · https://youtu.be/ukbNE_8zGwk (MASTER 23:11, 1 339 MB, desfase 0) · miniatura «GEN vs BLG · LA GRAN FINAL» (fórmula del canal), 22 etiquetas, no para niños, IA «No», sin promoción de pago, anuncios + mid-roll, idoneidad «Nada de lo anterior», .srt español PUBLICADO
- siguiente: nada de producción. Medir a 48 h (CTR, retención) en Studio; resumen de la final después del sáb 14-nov.

## Sesiones (protocolo docs/sesiones.md · «continúa el video lol_final_previa»)
- alias: previa de la final, Gen.G vs BLG, final Worlds
- vista previa: ninguna; directo al MASTER (regla 5-nov) y a la tele
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación feed + guion + recursos | ◐ 10-nov | feed_*.txt (13 partidas), guion.py borrador, recursos.py (fotos/logos/arte), 10 tarjetas de comentarios |
| 2 | (elige formas de presentación §) jugadas (agentes) → guion final → voz → efectos (2D + 3D) → música/SFX → render → final | ◐ 10-nov 23:22 | relevo: formas 1, 2, 4, 5, 10 (recomendadas; el usuario no eligió); voz de 46 frases fijas hecha y aceptada (voz_aceptada.json); `nucleo/mg_lol_pelea.py` (marcador NFL + oro en vivo); oro cada 10 s en investigacion/oro_125/130.json; subagente de RELLENO cortando r_*.mp4 → datos_relleno.md |

## Decisiones (el usuario, 10-nov-2026)
- ~25 min; VARIAS jugadas convertidas a 3D (Grieta 3D / mesa / capas 3D con flechas, rutas, intenciones).
- La caída de T1 YA NO es spoiler: gancho, título y miniatura pueden usarla.

## Datos verificados (API LoL Esports + feed livestats; `investigacion/`)
- Suiza: **Gen.G 3-0** (IG 1-0, HLE 1-0, LYON 2-1). **BLG 3-2** (pierde MKOI 0-1, gana TLAW, KC, pierde TES 1-2, gana HLE 2-0).
- Cuartos: GEN 3-0 LYON (mié 4-nov; 19-8, 22-6, 16-10) · BLG 3-0 DK (jue 5-nov; 24-10, 13-10, 25-9) · IG 3-1 TES · T1 3-1 KC.
- Semis: **GEN 3-0 IG** (sáb 7-nov; 29-9, 27-9, y G3 remontada 16-18 en asesinatos) · **BLG 3-1 T1** (dom 8-nov; G1 BLG 18-6, G2 T1 22-10, G3 BLG 19-10, G4 BLG 21-9).
- Plantillas (feed): GEN Kiin, Canyon, Chovy, Ruler, Duro · BLG Bin, Xun, Knight, Viper, ON · T1 Doran, Oner, Faker, Peyz, Keria · IG TheShy, Wei, Rookie, JiaQi, Meiko.
- Gen.G en eliminatorias: 6-0 en partidas. BLG: 6-1.
- **GEN-IG G3** (`feed_130`): IG 10-3 y +4,6K (18:22); Ruler (Yunara) 4 asesinatos seguidos 30:26-31:12 (Meiko, JiaQi, Wei, TheShy) → de +2,8K a +0,2K; Gen.G Barón ~33; IG gana 3-0 la pelea 33:28; cierre 39:16-40:08 (Gen.G 4-0 y fin). Tiempos = feed (HUD ≈ feed − 1..5 s; MEDIR en cuadro).
- **T1-BLG G4** (`feed_125`): BLG 10-3 al 17:46; T1 gana 28:02-28:27 (Faker 3 asesinatos, Doran 2) → de −6,3K a −3,3K; T1 Barón (~32); BLG gana 32:23-32:32 (Oner, Doran, Faker caen; Knight 2) → fin de T1; 37:10-37:42 cierre.
- POR VERIFICAR antes del guion: historial de finales (BLG perdió la final de 2024 contra T1 2-3; MSI de Gen.G); «ninguno ha ganado un Mundial» (Gen.G compró a Samsung Galaxy, campeón 2017: decirlo con cuidado).

## En curso (checkpoint 3, 10-nov 23:22 — corte por contexto; se sigue en la misma sesión)
- HECHO: formas: ver § Presentación ELEGIDA · `nucleo/mg_lol_pelea.py` NUEVO (`marcador_pelea` = forma 4,
  `oro_vivo` = forma 5; probados en previews/mg/) · `mesas_3d.py` con `cam="bullet"` (forma 2, media vuelta) y `cam="cenital"`
  (forma 1: sube a vista cenital y funde con la Grieta 3D); MESAS = {} por llenar · `efectos.py` = SOLO helpers copiados de
  lol_semana2 (EXT a hlbl_j1 K 2402.5 = cuádruple de Knight 41:05-41:10 en t≈62-67,5, blte_j1 K 1519, blte_j2 2152, blte_j3 1706,
  blte_g3 1392; K = {} por llenar) · copiados vivos_audio, render_par, espaciar_voz, alargar_musica, medios_locales e
  investigacion/{velocidades,voz_cuadra,pausas_frase,cortes_voz}.py (OJO: aún dicen «lol_semana2» dentro: cambiar rutas).
- VOZ: 46 frases fijas + gancho_0, duelo_jungla_0, j2_0-4, j5_0-4 generadas; aceptadas por nombres en `voz_aceptada.json`
  (`python aceptar_voz.py <claves>` tras leer voz/eval.json). Saldo ElevenLabs cuenta 2 ≈ 36 900.
- GUION reescrito con datos: j2 (Xun 3 asesinatos, NO 4: el feed duplica una línea; Heraldo 16:00; ShowMaker muere fuera de cámara
  ≈16:27) y j5 (BLG +3,9K antes; muro de Taliyah; alma infernal 32:54; Viper resucita). datos_j2.md y datos_j5.md completos (pies, tomas).
- FEED cada 10 s: investigacion/oro_130.json y oro_125.json [[s, dif azul-rojo, …]] (reloj ≈ el de feed_*.txt). IG = azul en la G3;
  T1 = azul en la G4. GEN-IG G3: Barón de Gen.G ~31:15 justo tras TheShy (31:12) → +1,4K para Gen.G. T1-BLG G4: Barón de T1 29:25.
- ✅ j1 y j3 reescritos con datos_j1/j3.md (j1: dragón infernal 25:46, muro de Taliyah de Chovy, Ruler ×3 sin bajas, Barón; K 494,3 / K_fuente 1490,7, pelea t 58-73 · j3: robo de Canyon 30:18 del dragón del alma, IG partido, Kiin «aparece por la espalda», Ruler ×4 30:22-31:08, Barón 31:11, IG +2,9K → GEN +1,4K; K 507,8 / K_fuente 1760,3; pistas_j3.json ±0,04, saltar claves `_meta/_objetivos/_muertes`, minimapa tapado 30:35-39 y 30:49-51); voz generada.
- (11-nov ~00:15) Relleno: 6 de 8 cortados (r_lyon2, r_ig1, r_ig2, r_ig3fin, r_dk2, r_t1g1 + datos_relleno.md); agente reanudado para r_dk3fin y
  r_escenario. Subagente escribiendo `j3_3d.py` (Grieta 3D con formas 1, 2 y 8; lee DE/A/RELOJ de `tiempos_3d.py` → TIEMPOS["j3"], que debe
  escribir efectos.py; provisional x1 desde 30:06) → medios/_fuente/j3_3d.mp4. `seleccionar` corriendo en CPU (FAB_WHISPER_CPU=1: la GPU no
  tiene memoria para large-v3 con Chrome abierto); al acabar: `python aceptar_voz.py` de las que solo fallen por nombres.
- (11-nov ~00:45) ✅ relleno 8/8 en medios/_fuente/r_*.mp4 + investigacion/datos_relleno.md (K y lo que se ve; r_dk2 desde t 38,9 es REPETICIÓN).
  ✅ voz 82/82 aceptada (j4/j6/j6_ctx/j6_fin = PROVISIONALES con el borrador viejo: rehacer con datos_j4/j6) · idioma_voz OK.
  `seleccionar` se usa con FAB_WHISPER_INT8=1 (opción nueva en nucleo/tts_select.py: Whisper int8_float16 en GPU). En marcha (bucle con
  reintentos): seleccionar → tiempo → beats (la alineación falló por memoria de GPU compartida con wow_errores_30_60). Luego `biblioteca sugerir`.
- (11-nov ~01:10) ✅ datos_j4/j6 (correcciones de la sesión principal aplicadas): gancho_0 («al Barón le quedan dos segundos»), j4 (Ancestral
  30:28, torres, ACE 32:11 22-10 +9,8K; K 448 / K_fuente 1802; pelea t 112-129, toma 28,7→129,5 sin cortes), j6_ctx_1 (Faker DOS), j6 (32:14
  torre, Oner→Viper, Ángel de la Guarda 32:16, Bin arriba/Xun abajo, Oner 32:18, Doran 32:23, Faker 32:27, 3-0 sin bajas, +0,4K→+2,5K;
  K 481 / K_fuente 1860; pelea t 64-87), j6_fin (nexo ≈37:45, VOD 2751 «Se rompió la dinastía…»; j6_fin.mp4 HUD = t + 2249; solo
  celebración de BLG, NO prometer la de T1; j6_baron.mp4 HUD = t + 1719, hasta t≈36,5 repetición). Voz regrabada (saldo ≈ 36 000).
  ✅ j3_3d.py + medios/_fuente/j3_3d.mp4 provisional (37 s: 30:06→30:40 con 3 s congelados en 30:23; formas 1, 2, 8; lee tiempos_3d.py).
  ▶ Subagente: j6_3d.py (formas 1, 6, 8). ▶ seleccionar en bucle (boua5offo). efectos.py = helpers + marcador()/oro() + exec de
  fx_escenas.py y fx_jugadas.py (separados para trabajar en paralelo) + PISTAS/SFX (sfx/ copiados de lol_semana2) + tiempos_3d.py.
- (11-nov ~01:40) ✅ voz 83/83 + idioma OK + tiempo + beats: **14:47** (887 s) → corto para ~25 min. ✅ j6_3d.py + j6_3d.mp4 provisional
  (32:06→32:20, formas 1, 6 «LO QUE PODÍA HACER», 8; Barón 0:00 a las 32:19 según datos_j6; ojo: la voz vuelve al VOD en «Viper se salva»
  (32:16): el 3D debe cortarse ~32:15 o el VOD retomar en 32:14). ▶ Subagente AMPLIANDO el guion con escenas NUEVAS (ids nuevos, sin tocar
  las grabadas) desde el relleno + j4b (Faker 23:10-23:50) → investigacion/AMPLIACION.md. Después: voz --solo de las nuevas → seleccionar
  (FAB_WHISPER_INT8=1) → aceptar_voz → idioma_voz → tiempo → beats → efectos en paralelo (fx_escenas.py / fx_jugadas.py).
- (11-nov ~02:30) ✅ guion AMPLIADO (+12 escenas, investigacion/AMPLIACION.md) · voz 132/132 · idioma_voz OK (lyon_p2_2 reescrita) ·
  tiempo + beats: **23:16** (1 395,8 s). j6_fin post 14 s (celebración audible tras «Escucha cómo se vivió»), final_publico post 5 s.
  ▶ 2 agentes de montaje en paralelo: fx_escenas.py (escenas sin jugada) y fx_jugadas.py (j1-j6, ctx/fin, mesas, 3D, 7 formas).
- ✅ MÚSICA: LYRIA.tramos (10, por acto) + biblioteca usar (ig_lyon 3, cfo_kc 3, lol_worlds 1/4/7/3/8, t1_koi 2/5, cfo_kc 4: piezas del
  canal, ninguna repetida en el video, como en lol_semana2) + alargar_musica.py + `musica` → audio/musica.wav 1 395,8 s. Si cambia el
  timeline: alargar_musica.py + musica otra vez.
- REGLA DEL USUARIO (11-nov): «Antes de lanzar, asegúrate que no hay otro. Si lo hay, pausa el tuyo hasta que terminen los otros.» →
  `python esperar_libre.py && <render/3D/Whisper>` (espera sin matar nada; lista los pesados con su cwd). Aplica a render_par, render3d,
  mesas_3d, seleccionar, idioma_voz, final.
- ✅ fx_escenas.py (agente, 11-nov): todas las escenas sin jugada; ~90 cuadros revisados; oro_116/117/128/129/099/100/122.json bajados.
  Sin VOD (fondo animado con escudos): suizas, lyon_p1, hora de la final, historia 2023-24. PENDIENTE: la captura com_UgyWEuyk… (Leonardo)
  corta el texto antes de «3/2 para BLG» (la tapa una tarjeta; regenerarla si da tiempo); tramos libres usados en escenas: j1 0-47,
  j2 0-40,6, j5 0-37, j6 2-40, j4 133-148 (comprobar que no choquen con fx_jugadas).
- ✅ fx_jugadas.py (agente, 11-nov): las 6 jugadas con las 7 formas (hoja previews/formas_jugadas.jpg revisada: 1, 2, 3, 4, 5, 6, 8 visibles);
  mesas j2b/j5a renderizadas, j3_3d/j6_3d re-renderizados con TIEMPOS_3D anclados a la voz; fx --seco OK (739 efectos), 0 tramos > x1.
  Dudas del agente: oro del feed en la pausa de j6 marca −1,0K y el HUD BLG +0,5K (muestreo de 10 s: revisar/quitar ahí); saltos < 1 s
  para que cada muerte caiga con la voz (SYNC). j6_fin_2 reescrita («Y estas son las reacciones de Bilibili cuando cae el nexo…»): el
  comentario de Historias de un Mundo Nuevo NO pidió reacciones. ▶ (11-nov ~04:00) seleccionar de j6_fin_2 esperando a esperar_libre
  (renders de otras sesiones). Luego: tiempo → beats → alargar_musica + musica → fx (SFX) → chequeo → vivos_audio → mezcla → render_par.
- (11-nov ~04:30) ✅ j6_fin_2 seleccionada · tiempo · beats · alargar_musica + musica (1 391,45 s = 23:11) · medios_locales.py reescrito (clip de
  cada beat = el FX video que lo cubre; 8 beats sobre fondo → r_escenario) · chequeo: idioma OK; avisos aceptados: variedad de pegatinas (el
  canal usa las de mg_lol), «sonido nombrado» de voz_1 (falso), final_publico y j6_fin (los oye vivos_audio: post a x1 con audio del clip).
  ▶ `fx` (SFX + audio/fx.wav) esperando a esperar_libre (falló por memoria con renders ajenos). Luego: vivos_audio.py → mezcla →
  esperar_libre && render_par.py → final → verificar → tele master → miniatura Flow → Studio jue 12-nov.
- (11-nov 11:50) ✅ audio/fx.wav (el borrador de montaje de `fx` se cayó al 78 %: no hace falta). ▶ render_par.py (3 simultáneos) lanzado tras
  esperar_libre → salida/video_sin_audio.mp4 (trozos en %TEMP%/lol_final_previa_par, se reanuda con par_k.ok). Después: vivos_audio.py →
  `mezcla` → `final` → `verificar` → tele master. Miniatura Flow: preguntado a la sesión principal si la hace ella.
- (11-nov 11:55) ✗ render_par 1.er intento: los 6 tramos MemoryError (3 a la vez + otras sesiones). Relanzado con N = 10 y SIMULTANEOS = 2
  (tras esperar_libre). ✅ youtube_texto.md (título, descripción, 20 capítulos del timeline de 23:11, etiquetas). Miniatura Flow: la hace
  ESTE hilo tras el render (la principal no puede); si no da, último paso de ESTADO + relevo.
- (11-nov 12:05, YA NO VALE: luz verde del usuario ~12:30 y render_par lanzado) ⏸ RENDER EN PAUSA por orden del usuario («Vamos a pausar el render hasta que termine el de Warcraft»). Encadenado en 2.º
  plano: `esperar_wow.py` (espera a que ARRANQUE y luego TERMINE el render de videos/wow_*) → esperar_libre → render_par.py (N 10, 2 a la vez).
  Si esta cadena se pierde, relanzarla igual; nada pesado mientras tanto.
- (11-nov 13:20) render_par: 6/10 tramos OK (0, 1, 5, 7, 8, 9: par_k.ok en %TEMP%/lol_final_previa_par); 2, 3, 4 y 6 MemoryError hacia los
  19 min (pagefile lleno). Relanzado con SIMULTANEOS = 1 (se reanuda solo con los que faltan).
- (11-nov 14:10) ✅ MASTER 1.ª versión (23:11, 1 339 MB, −14,3 LUFS, desfase 0) con vivos (vivos_audio.py arreglado: salta 3D/mesas sin audio) y
  mandado a la tele. Hoja final_hoja.jpg revisada: bien, salvo la cifra de la gráfica de oro cuando va arriba el rojo («-1,4K GEN» = se lee al
  revés) → corregido en nucleo/mg_lol_pelea.py (siempre «+X K <equipo que va arriba>»). ▶ RE-RENDER completo (10 tramos, 1 a la vez, tras
  esperar_libre) → final → verificar → tele master, encadenado en 2.º plano. Audio ya mezclado (audio/final.wav) no cambia.
  Luego: miniatura Flow (miniatura/prompt_flow.md) → Studio PROGRAMADO jue 12-nov (youtube_texto.md) → BITACORA → catalogar → commit.
- ✅ (11-nov 14:20) MINIATURA Flow: miniatura/elegida.jpg (de flow_a.png; collage de 4 fotos oficiales + 2 logos como ingrediente único;
  proyecto Flow «nov 11 - 14:07»). youtube_texto.md al día.
- ◐ (11-nov 15:30) RE-RENDER: tramos 0-8 OK; par_9 MemoryError (otra sesión con la RAM llena: tactica3d + ffmpeg vertical).
  Relanzado en 2.º plano tras esperar_libre (render_par se reanuda solo con par_9; log render_par2.log) → final → verificar → tele master.
  Si se pierde: relanzar igual. Luego Studio PROGRAMADO jue 12-nov.
- ✅ (11-nov 16:10) MASTER v2 (gráfica de oro «+1,4K GEN» comprobada en cuadro) → Studio: ukbNE_8zGwk PROGRAMADO jue 12-nov 10:00 CDMX.
  MINIATURA: el usuario rechazó la de caras (flow_a: «no me gustan… mejor como las últimas del canal, para que se reconozca»)
  → rehecha en Flow con la miniatura de IG-LYON (i.ytimg.com) como ingrediente: miniatura/canal_a.png → elegida.jpg; la rechazada
  queda en elegida_rechazada_t1.jpg. .srt cargado con el hook de HTMLInputElement.click (change en setTimeout) + SHA-256 = el local.
- FALTA (ya nada de investigación), pistas_j3/j6.json (ya están j6_baron.mp4 y j6_fin.mp4). Agente de
  RELLENO (de la sesión 23:20) cortando r_lyon2, r_ig1, r_ig2, r_ig3fin, r_dk2, r_dk3fin, r_t1g1, r_escenario → datos_relleno.md.
- SIGUIENTE en orden: afinar j1, j3 (+ Barón 31:15), j4, j6 (Barón 29:25: «se le acaba el Barón»), j3_ctx/j3_fin/j6_ctx/j6_fin con los
  datos → voz --solo → seleccionar → aceptar_voz → idioma_voz → tiempo → beats → efectos.py por escenas (plan por jugada abajo) →
  mesas_3d → j3_3d.py/j6_3d.py → fx --seco → chequeo → música/SFX → vivos → mezcla → render_par → final → verificar → tele → Flow → Studio.
- Plan j2: VIVO t40,6-48,6 · PZ t50 (Xun .30,.43 · Lucid .51,.44 · Career .555,.47 · ShowMaker .125,.555 · ON .43,.43 · Knight .44,.57)
  · SYNC 59 Lucid/62 Bin/63,5 Career/65 DOUBLE + marcador_pelea BLG–DK · mesa bullet en t69 (Xun .51,.33 · ShowMaker .505,.65 · Viper
  .905,.25; ruta Xun [(65,.25,.64),(69,.51,.33)]) · corte a 77,2 «killing spree». j5: VIVO 37,1-43 · PZ t46 (los 10 medidos) · 49-51
  muro · SYNC 59 Oner/62 Bin/65 Doran/70 alma/76 Knight/79 torre/82-84 doble de Viper + marcador · mesa bullet t62 · repetición 93,8+.
## En curso (checkpoint, 10-nov noche — corte por contexto)
- HECHO: video creado (`nuevo --yt`); feed oficial de las 13 partidas (`investigacion/feed_*.txt`, `muertes.py`), `datos_duelos.md` (K/D/A eliminatorias),
  `fonetica_lista.json`, `guion.py` COMPLETO en borrador (~1 850 palabras; faltan ~500 en las jugadas → ~25 min con vivos y pausas),
  `recursos.py` corrido (pegatinas/jugadores de GEN, BLG, T1, IG, LYON, DK; iconos y splash de 61 campeones), tarjetas
  `pegatinas/com_*.png` (10 comentarios del 8-10 nov, texto exacto en `investigacion/comentarios.json`; avatar gris: no hay URL).
- EN MARCHA (lanzados ~22:00 del 10-nov, 3 subagentes de ESTA sesión): cortan `medios/_fuente/j1..j6.mp4` (+ `j6_fin.mp4`) y escriben
  `investigacion/datos_jN.md` (K del VOD, tabla paso a paso, cortes de cámara, narración, posiciones de pies) y `pistas_j3.json` /
  `pistas_j6.json` (minimapa, para la Grieta 3D). Brief: `investigacion/BRIEF_JUGADAS.md`. Si al retomar falta alguno, avanza con
  lo demás y vuelve a mirar; si a la mañana sigue faltando, haz esa jugada a mano con el brief.
- Jugadas: j1 GEN-LYON G3 Ruler triple (2D) · j2 BLG-DK G1 Xun ×4 (2D + mesa) · j3 GEN-IG G3 remontada de Ruler (GRIETA 3D) ·
  j4 T1-BLG G2 T1 5-0 (2D) · j5 T1-BLG G3 BLG 4-2 (2D + mesa) · j6 T1-BLG G4 pelea tras el Barón de T1 (GRIETA 3D) + j6_fin nexo y reacciones.
- FALTA en orden: afinar frases j1-j6 con lo medido (quitar lo que no se vea) → voz (JC) → seleccionar → `python nucleo/idioma_voz.py lol_final_previa`
  → tiempo → beats → efectos.py (copiar helpers de `../lol_semana2/efectos.py` líneas 1-450: J, CLIP, P/PZ, REBX, LENTA, MESA, V3, VIVO,
  com, sil, peg, tar; 3D: `j3_3d.py`/`j6_3d.py` como `../lol_worlds_2026/j6_3d.py` → `nucleo/tactica3d/render3d.py`; mesas con
  `mesas_3d.py`) → MG del cara a cara (`L.duelo`/`ficha_jugador`), llave, calendario de la final → `fx --seco` → `chequeo` → música
  (`biblioteca sugerir`) + SFX → vivos_audio → mezcla → render_par → final → verificar → tele master → miniatura Flow
  («SIN T1, ¿QUIÉN GANA?» o similar, Gen.G vs BLG) → youtube_texto.md → subir por Studio PROGRAMADO jue 12-nov (hora: la de los
  anteriores, ~10:00-20:00 CDMX) → BITACORA.
- Reportar al usuario: la queja n.º 1 de los videos de cuartos/semis es la voz (no los hizo esta fábrica: voz distinta). Este vuelve a JC.

## Presentación ELEGIDA (el usuario, 10-nov, vía la sesión principal: «me gustan todas menos de la 7 a la 10, bueno la 8 si me gusta»)
- VAN: 1 VOD→Grieta 3D sin corte · 2 bullet time · 3 pantalla dividida · 4 marcador NFL · 5 oro en vivo · 6 «LO QUE PODÍA HACER» (solo
  rotulado como posibilidad y con apoyo de la narración) · 8 visión y niebla en la Grieta 3D. NO van: 7, 9, 10 (los VIVO normales del
  estilo siguen, y las reacciones de j6_fin también: las pidió un comentario). Se SUMAN al estilo de siempre.
- «para que las apliques TODAS» (el usuario, 10-nov): las 7 salen; 4 (marcador) y 5 (oro en vivo del feed) en LAS SEIS jugadas;
  j1 = 3 · j2 = 2 + 6 · j3 = 1 + 8 + 2 · j4 = 3 + 6 · j5 = 2 + 3 · j6 = 1 + 6 + 8 (además de 4 y 5 en todas). Antes del render, hoja de
  cuadros con las 7 marcadas (previews/formas_*.jpg).
## Presentación de jugadas: 10 formas nuevas (el usuario, 10-nov: «probemos nuevas formas y más dinámicas»; ELIGE él)
1. VOD → Grieta 3D sin corte: el cuadro congelado se despega del suelo y la cámara sube en picada hasta el mapa 3D (y vuelve al VOD en el mismo cuadro).
2. Bullet time 3D: congelado, la cámara da media vuelta alrededor de la pelea en la mesa 3D, con las fichas levantadas.
3. Pantalla dividida: VOD + mapa 3D a la vez, o 2-3 ventanas con zoom que siguen a cada protagonista (Ruler, Knight, Faker).
4. Marcador de pelea tipo NFL: una barra abajo donde cada muerte se enciende al caer (retrato que se agrieta y pasa a gris) + «3 por 0».
5. Gráfica de oro en vivo: la línea del feed cada 10 s se dibuja durante la pelea y se ve el desplome (j3 de +2,8K a +0,2K).
6. Camino que no tomó (rotulado «LO QUE PODÍA HACER»): ruta fantasma discontinua (T1 volviendo a base con el Barón) frente a la que hizo.
7. Cuenta atrás de la decisión: reloj gigante «9 SEGUNDOS» que corre mientras la jugada avanza en cámara lenta.
8. Visión y niebla: antes del Barón, la Grieta 3D oscura con la visión de cada equipo; quién veía a quién.
9. Espejo: dos jugadas parecidas lado a lado con el reloj sincronizado (la remontada de Gen.G contra la caída de T1).
10. Voz de la transmisión + cámara de los jugadores: tramos en vivo con la narración original, palabras clave gigantes y la reacción real (la pidió un comentario).
Recomendado si no contesta: 1, 2, 4, 5 y 10 (hay kit o se hacen sobre él); 6 solo rotulado como posibilidad, nunca como hecho.

## Plan de jugadas (borrador)
- 3D: GEN-IG G3 la remontada de Ruler (30:26-31:12) · T1-BLG G4 pelea tras el Barón (32:23-32:32) · + 1-2 más (BLG-DK, GEN-LYON).
- 2D (pausas + telestrador): T1 gana la G2 a BLG (Faker) · una de GEN-LYON · una de BLG-DK · T1-BLG G4 28:02.
