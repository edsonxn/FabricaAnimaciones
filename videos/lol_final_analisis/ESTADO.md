# Gen.G vs BLG: la GRAN FINAL de la Worlds 2026 analizada pausa por pausa (~22-25 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Crónicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; subida por Studio en el navegador, NO está en la API) · final sáb 14-nov 19:00 UTC, Bo5; publicar en cuanto esté (dom 15-nov)
- estilo: análisis táctico (secuencia_yt + VOD + `mg_tactica` + `mg_lol` + `mg_lol_pelea` + 3D `nucleo/tactica3d`) → docs/estilo_analisis_tactico.md § GUÍA RÁPIDA y § «partido YA JUGADO» · copiar de `videos/lol_final_previa/` (lo más nuevo) y `videos/lol_semana2/`
- etapa: ARCHIVADO 20-nov-2026 (decisión del usuario en «buenos días»: no se termina) · ✅ MASTER 14:09 (salida/lol_final_analisis_MASTER.mp4, 856 MB, desfase 0, −14,26 LUFS) mandado a la tele 14-nov 22:55
- siguiente: visto bueno del usuario → miniatura Flow (LETRAS ROJAS sin spoiler) → Studio PROGRAMADO (youtube_texto.md) → BITACORA → catalogar → commit

## Sesiones (protocolo docs/sesiones.md · «continúa el video lol_final_analisis»)
- alias: análisis de la final, final Worlds, Gen.G vs BLG final
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + montaje (agentes) | ✅ archivado 20-nov (no se termina) | corte por contexto: serie investigada (BLG 3-1), guion y voz completos, montaje en agentes |

## Decisiones (Claude, 14-nov; el usuario solo dijo «video de ligoleyen de la final análisis»)
- Formato: análisis de TODA la final partida por partida, 2 jugadas por partida, la decisiva de cada partida en 3D o mesa; formas de la previa
  (4 marcador NFL + 5 oro en vivo en todas; 1, 2, 3, 6, 8 repartidas). Duración ~22-25 min (lo que mejor funciona en el canal).
- SIN SPOILER en título, miniatura y gancho (regla del canal): cada resultado se descubre al final de su partida. Miniatura de LETRAS ROJAS
  (§ «Previa de una FINAL» del doc de estilo).
- Voz JC (`4XUsiqPDK4UACIM2BILe`), FONETICA de `investigacion/fonetica_lista.json` (de la previa).

## Datos verificados (feed oficial)
- G1 (115660540726095134): GEN azul gana 19-4 (~39 min). BLG 4 dragones al 22; GEN 3-0 al 22:23-32, Barón 25:33, ace 29:01-09, cierre 38:48-56.
- G2 (…135): BLG rojo gana 19-14 (~53 min). Barón BLG 29:45; 47:25-48:09 BLG 3-0; 53:00-14 cierre con 3.er Barón de BLG.

## En curso
- (14-nov 16:50) herramientas copiadas de lol_final_previa (raíz e investigacion/). Agentes: g1 (VOD QZCHpYleJnc) y g2 → datos_g1/g2.md,
  medios/_fuente/g<p>_j<k>.mp4, oro_g<p>.json, pistas_g<p>_j1.json. OJO: los .py copiados dicen «lol_final_previa» dentro: cambiar rutas.
- (14-nov 16:55) ✅ comentarios: investigacion/comentarios.json + 11 tarjetas pegatinas/com_*.png (investigacion/hacer_coms.py). Gracias: joaco_qz4746, ismaellopez632, flazhmarco, aqua_axis, ricardoordonez…, DanielTejerina. Críticas: JuanCarlosFuentesPando (T1 vende humo), leonardochamorro440 (IA), rolnesc2459 (Banderas). Justas: voz se cruza al inglés (idioma_voz), música/formato. Pronósticos con likes (sin tarjeta): thesonicring808 «Gen.G 3-1» (8), NicoBelikk/vilgaxiuz «BLG 3-2», masteronKick «BLG 3-1» → usar DESPUÉS de revelar el resultado. Queja voz IA → reportar al usuario.
- (14-nov 17:03) G3: BLG gana 20-8 (~38 min) → serie BLG 2-1. feed_g3.txt; agente g3 en marcha. Esperando G4 (esperar_partida.py 4).
- (14-nov ~17:30) ✅ G1 investigada: datos_g1.md (K 524; j1 alma 22:10-22:30 K_fuente 1280,0 [3D, pistas_g1_j1.json]; j2 ancestral robado 28:33-29:08 K_fuente 1663,2; relleno g1_r1 draft, r2 ancestral GEN, r3 nexo 1-0). cortar.py da 403 → investigacion/cortar2.py.
- (14-nov ~17:55) ✅ G2 investigada: datos_g2.md (VOD Ck_nt1V-Jvw, K 538; j1 Ancestral 47:05-48:08 K_fuente 2785 [3D, pistas_g2_j1.json]; j2 2.º Nube 25:12-25:34 K_fuente 1460, GEN 4-2, repetición t 85,7-126,4; relleno r1 draft, r2 Barón robado por GEN 42:50, r3 nexo 1-1).
- (14-nov 17:40) guion.py: intro + comentarios + G1 + G2 escritos (gancho PENDIENTE sin spoiler; G3+ y cierre pendientes). Voz generada de 40 frases (todas menos gancho) con `voz --solo`; ElevenLabs saldo ≈ 4 330 (OJO: justo para el resto). Fonética añadida: Corki, Locke, Cho'Gath, Ziggs, Rolnesc, Bryan.
- (14-nov 18:10) ✅ SERIE TERMINADA: BLG CAMPEÓN 3-1. G4 BLG (azul) 21-11 (~43 min); feed_g4.txt; agente g4 en marcha (+ nexo/celebración g4_r_nexo y ceremonia/MVP g4_r_copa). Saldo ElevenLabs total ≈ 4 337 (c2 4 111, c3 226). Falta: datos_g3/g4 → guion G3, G4, gancho sin spoiler, cierre → voz.
- (14-nov ~18:30) ✅ G3 investigada (datos_g3.md, VOD mUcFCIYGZ6Y K 536,4; j1 30:13-30:35 [3D] K_fuente 1750,1; j2 24:54-25:14 K_fuente 1447,4) y escrita en guion.py (g3_draft, g3_j2, g3_j1, g3_fin). Gancho escrito. Falta G4 (agente) + cierre.
- (14-nov ~19:00) ✅ voz 56/56 (gancho, intro, G1-G3) aceptada + idioma_voz OK; tiempo + beats: 9:10 sin vivos. efectos.py = helpers de la previa
  (exec de fx_escenas.py, fx_g1g2.py, fx_g3g4.py); guion.py une espacios_*.json y ajustes_*.json de cada agente. BRIEF_MONTAJE.md.
  ▶ 3 agentes de montaje: fx_escenas (escenas sin jugada), fx_g1g2 (g1_j1 3D, g1_j2, g2_j2, g2_j1 3D), fx_g3g4 (g3_j2, g3_j1 3D; luego G4).
  ▶ agente g4 investigando (datos_g4.md, g4_r_nexo, g4_r_copa/MVP). Saldo ElevenLabs ≈ 1 890 (c2 1 666, c3 226): G4 + cierre ≤ 600 palabras.
  Falta: guion G4 + cierre → voz → montaje G4/cierre → fx (SFX) → música biblioteca → vivos_audio → mezcla → render_par → final → tele → Flow → Studio.
- (14-nov ~19:40) ✅ G4 investigada (datos_g4.md, VOD AkGN278JAI8 K 533; j1 Barón 26:13-26:51 [3D] K_fuente 1513,2; j2 Barón robado por Xun 41:54 +
  nexo 42:57 K_fuente 2447,15; g4_r1 draft, g4_r_nexo, g4_r_copa, g4_r_copa2, g4_r_mvp: MVP KNIGHT 13/6/41, 84,4 % KP). Guion G4 + cierre
  (campeon, mvp, pronosticos, cierre) escrito; voz generada (21 frases, saldo ≈ 1 450). ▶ seleccionar en 2.º plano (espera esperar_libre).
- (14-nov ~20:05) ✅ fx_escenas.py (gancho…g3_fin) hecho por agente; hojas previews/esc_*. g1_ctx_0 cambiada a «tres dragones» (era inexacto): REGENERAR su voz tras el seleccionar en curso.

## En curso (checkpoint 14-nov ~20:45 — corte por contexto; relevo en sesión nueva)
- HECHO: serie investigada (datos_g1..g4.md, oro_g*.json, pistas_g*_j1.json, fuentes medios/_fuente/g<p>_j<k>/r*.mp4, g4_r_nexo/copa/copa2/mvp);
  guion.py COMPLETO (28 escenas: gancho sin spoiler, comentarios, G1-G4, campeon, mvp, pronosticos, cierre); voz 77/77 aceptada (voz_aceptada.json),
  idioma_voz OK; espaciar_voz + tiempo + beats corridos (812 s = 13:32 sin todos los espacios). LYRIA.tramos (10) definidos en guion.py.
- MONTAJE (3 agentes de la sesión anterior, siguen en segundo plano y escriben solos sus archivos; NO dupliques su trabajo):
  · fx_escenas.py (todas las escenas sin jugada; G4/cierre escritos, revisando hojas previews/esc_*.jpg) · fx_g1g2.py (+ g1_3d.py, g2_3d.py, mesa g1_j2a;
  espacios_fx_g1g2.json: g1_j1_4 cambió → «sin pausa real antes de Y», re-medir) · fx_g3g4.py (+ g3_3d.py, g4_3d.py; G4 recién habilitado).
  Saber si terminaron: sus resúmenes se añaden abajo en «## Relevos de agentes»; si no hay nada en ~1 h, revisa fecha de sus archivos y `fx --seco`.
- FALTA en orden: (1) cuando los 3 terminen: `python videos/lol_final_analisis/espaciar_voz.py` → `fab.py lol_final_analisis tiempo` → `beats` →
  `fx --seco` → `FAB_FX_FINAL=1 … fx hoja` y mirar TODAS las previews/fx_NN.jpg (regla 8) → `chequeo` (promesas visuales).
  (2) MÚSICA: `biblioteca sugerir lol_final_analisis` → `usar <id> lol_final_analisis <tramo>` ×10 evitando lo de la previa (ig_lyon 3, cfo_kc 3,
  lol_worlds 1/4/7/3/8, t1_koi 2/5, cfo_kc 4, lol_final_previa_*) → `alargar_musica.py` → `musica`. (3) `fx` (SFX + audio/fx.wav) →
  `vivos_audio.py` → `mezcla`. (4) `esperar_libre.py && render_par.py` (SIMULTANEOS 1, N 10) → `final` → `verificar` → `tele video lol_final_analisis master`
  en 2.º plano → avisar. (5) Miniatura Flow de LETRAS ROJAS sin spoiler (doc § «Previa de una FINAL»; p. ej. «GEN vs BLG / LA FINAL» o «PAUSA POR PAUSA»)
  (6) youtube_texto.md (título sin spoiler, capítulos, descripción con fuentes) → Studio PROGRAMADO (canal sin API; hueco: el siguiente tras el 12-nov,
  publicar dom 15-nov) → BITACORA → biblioteca catalogar → commit.
- Reportar al usuario: quejas de la voz IA en comentarios (5 más); saldo ElevenLabs ≈ 1 360 (c2 ~1 130, c3 226): sin margen para más voz.
## Relevos de agentes
- (14-nov ~21:00) ✅ fx_escenas.py TERMINADO (agente): todas las escenas sin jugada + G4/cierre revisadas (hojas previews/esc_*.jpg, esc_g4_01-09, esc_g4b_01-03).
- (14-nov ~21:00) ✅ MÚSICA elegida (biblioteca usar, nada de la previa): 1 lol_worlds_2026 t10 · 2 lol_semana2 t2 · 3 cfo_kc_worlds t5 · 4 ig_lyon t2 ·
  5 t1_koi t3 · 6 lol_worlds_2026 t9 · 7 lol_semana2 t6 · 8 cfo_kc_worlds t6 · 9 lol_worlds_2026 t6 · 10 lol_semana2 t10 → audio/lyria_tramoN.mp3.
  Tras el timeline FINAL: `alargar_musica.py` + `musica` (las piezas se ajustan al tramo).
- La sesión de relevo NO se pudo abrir (la app la rechaza en turnos de aviso automático): se reintenta en el siguiente mensaje del usuario.
- (14-nov ~21:10) ✅ fx_g3g4.py TERMINADO (agente): g3_j2, g3_j1 (3D g3_3d.mp4 + g3_3d_b.mp4), g4_j1 (3D g4_3d.mp4), g4_j2 (mesa g4_j2b); velocidades 0 > x1,
  cortes_voz OK. PENDIENTES que dejó: (a) `espaciar_voz.py` se para en g1_j1_4 (espacio de fx_g1g2: re-medir) → aplicó solo los suyos;
  (b) DATO MAL en g3_j2_1: «Y Chovy, solo, cae también» pero a las 25:08 Kiin está a su lado (datos_g3.md) → quitar «solo» (regenerar g3_j2_1,
  ~25 créditos, re-medir su espacio ["cae", 1, 4.2, 7.83] y revisar anclas de fx_g3g4.py en esa frase); (c) falta arte de Annie en splash/.
  esperar_libre.py se queda esperando a 2 procesos COLGADOS de starship_sin_patas (3592, 21056, 0 % CPU desde 18:34): no matarlos; comprobar CPU y seguir.
- Falta solo el agente de fx_g1g2.py (3D g1/g2 + mesa g1_j2a).
- (14-nov ~21:25) g3_j2_1 corregida («Y Chovy cae también», sin «solo») + espacio [Y,1,4.2,6.14]; todos los espacios aplicados (g1_j1_4 ya pasa); tiempo + beats = 847 s (14:07). Agente g34 revisando anclas de g3_j2.
- (14-nov ~21:35) ✅ g3_j2 re-anclado por el agente (espacio g3_j2_1 = [Y,1,5.65,6.14]); espaciar+tiempo+beats = 849,3 s; mesa_g3_j2b re-renderizada. Solo falta fx_g1g2.
- (14-nov ~22:10) ✅ MONTAJE COMPLETO (fx_g1g2 terminado: g1_3d.mp4, g2_3d.mp4, mesa_g1_j2a; hojas previews/fx_g12_*). esperar_libre.py ignora ya procesos
  colgados (0 % CPU). fx --seco OK (409 efectos). chequeo OK (idioma OK; avisos aceptados: pegatinas bajas como la previa, «Banderas» falso sonido).
  ✅ musica.wav (849,3 s) · ✅ `fx` → audio/fx.wav. Revisión mía de hojas: 2 arreglos pedidos a los agentes (pegatina de Xun cortada en el gancho
  10,2 s → fx_escenas; etiqueta Kiin tapa a Chovy en g3_j1 30:10 → fx_g3g4). Cuando respondan: `fx --seco` → `fx` (SFX otra vez si cambian
  tiempos) → `python videos/lol_final_analisis/vivos_audio.py` → `fab.py lol_final_analisis mezcla` → `esperar_libre.py && render_par.py` → final → verificar → tele master.
- (14-nov ~22:30) ✅ arreglos de hojas (Xun y Ruler x=0,12; etiquetas g3_j1 ya bien) · medios_locales (relleno g4_r1) · vivos_audio · mezcla −14,26 LUFS. ▶ render_par → final → verificar → tele master (2.º plano, log render_par.log).
- (14-nov ~22:40) ✅ youtube_texto.md (título/descr./capítulos SIN spoiler, etiquetas). FALTA tras el MASTER: tele master, miniatura Flow (LETRAS ROJAS, ingrediente = la última del canal, p. ej. https://i.ytimg.com/vi/ukbNE_8zGwk/maxresdefault.jpg; texto «GEN vs BLG» blanco + «PAUSA POR PAUSA» rojo, píldora WORLDS 2026, copa), Studio PROGRAMADO, BITACORA, catalogar, commit.
- (14-nov 22:55) ✅ MASTER 14:09 + .srt; final_hoja.jpg revisada (ojo: 6:26 tarjeta «LOS 4 BARONES» vacía en ese cuadro, ¿entrando? mirar en la tele). Tele + aviso por voz.
