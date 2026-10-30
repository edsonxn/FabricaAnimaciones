# CFO vs KC: las jugadas clave analizadas (Worlds 2026, ~16 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Crónicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; subida por Studio en el navegador, NO está en la API) · publicar hoy jue 29-oct-2026 por la noche (serie CFO-KC, Bo3, empezó 14:00 CDMX)
- estilo: análisis táctico como `t1_koi_worlds` (secuencia_yt + VOD + telestrador `mg_tactica` + `mg_lol` + mesas/capas 3D) → doc: docs/estilo_analisis_tactico.md
- etapa: ✅ MASTER LISTO 29-oct 18:12 (17:30, salida/cfo_kc_jugadas_MASTER.mp4 + .srt); falta subir por Studio
- siguiente: guion.py (G1) → al terminar la serie: datos_g2/g3 → voz → jugadas/3D → render → subida (ver «En curso»)

## Sesiones (plan de tramos · «continúa el video cfo_kc_jugadas» retoma aquí · protocolo docs/sesiones.md)
- alias: CFO vs KC de hoy, análisis CFO KC, partido de KC
- vista previa: NO (el usuario, 29-oct: «todo seguido, sin vista previa»); ~16 min; canal Crónicas de ligoleyen
- leer al empezar: este ESTADO, docs/estilo_analisis_tactico.md (§ «Errores corregidos» y § «Análisis de un partido YA JUGADO»), guion.py (docstring = datos)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación G1 + guion de la G1 + estructura para G2/G3 | ◐ parcial | 29-oct 14:50-15:40 feed/VOD/desfase/Whisper/fuentes; 15:50 K medido + datos_g1.md; falta guion.py (corte por contexto) |
| 2 | G2 + guion + voz + tiempos | ◐ parcial | 29-oct 16:15-16:45 (sesión 3, cortada por contexto): guion, voz 85/85, tiempo 1039 s, beats 121 |
| 3 | efectos.py (jugadas con pausas/3D, boleta) → capas 3D → render_par → vivos_audio → mezcla → final → verificar → Studio | ◐ MASTER listo, falta Studio | 29-oct 17:00-18:05 (sesión 5, cortada por contexto): correcciones G2 + voz, medios, efectos.py, boleta, capas 3D, música 7/8 |

## Decisiones (el usuario, 29-oct-2026)
- «análisis de las mejores jugadas y los movimientos más inteligentes, las mejores predicciones… escenas 3D con pausas, flechas,
  rutas… varias jugadas de cada partido, no solo las mejores sino las inteligentes, predicciones, los errores y aciertos de cada jugador».
- SIN SPOILER: miniatura, título y gancho no dicen quién ganó; cada resultado se descubre en la última jugada de su partida.

## Datos (investigacion/)
- Serie: event 115660540726095073 (getEventDetails → event.json). G1 gameId 115660540726095074 (completada), G2 …075, G3 …076.
- G1: KC AZUL (Canna Galio, Yike Wukong, kyeahoo Cassiopeia, Caliste Tristana, Busio Nautilus) vs CFO ROJO (Rest Rumble,
  Shad0w Jarvan IV, POUT Syndra, Doggo Kai'Sa, Kino Alistar). Feed: g1_feed.txt (oro por minuto, objetivos), g1_asist.txt (muertes).
  Reloj feed ≠ HUD: calibrar con un cuadro del VOD (en T1-KOI era HUD + 4).

## En curso (checkpoint 29-oct 17:15 — sesión 5)
- ✅ datos_g2.md y pausas_g1.md listos; 8 fuentes g2_j1..j8 (K: j1 107, j2 317, j3 568, j4 1182, j5 1412, j6 1659, j7 1799, j8 2041).
  J6 = g2_j1/j2/j3 · J7 = g2_j4 · J8 = g2_j5 · J9 = g2_j6/j7 · J10 = g2_j8.
- ✅ 17:12 «Correcciones al guion» aplicadas en guion.py (draft2_2, jugada6_2, jugada7_0, jugada7_rep_0, jugada8_1/3, jugada9_1/2,
  jugada10_0/4, curva2_0; quitado «lo que le pasó a Karmine contra LYON», sin fuente). ✅ 17:25 voz 85/85 · tiempo 1050,0 s (17:30) · beats 122 · ▶ medios_locales.py (G2 ya con g2_j*) en marcha.
- ✅ 17:50 medios 122/122 con fuentes G2 · efectos.py ESCRITO (339 efectos; helpers de t1_koi + COLOR(eq) por partida; pausas G2
  medidas en previews/cuadros/r_g2_*; capas 3D j3a/j3b/j7a/j7b/j10a/j10b) · MG nuevo `mg_lol.boleta` · `fx --seco` OK.
  ✅ 18:05 capas 3D renderizadas (PYTHONIOENCODING=utf-8 python nucleo/tactica3d/sobre_video.py cfo_kc_jugadas) · vivos_audio.py
  con los VIVOS nuevos (fuente, segundo FINAL) · guion._VIVOS puesto · LYRIA.tramos (8) en guion.py; biblioteca `usar` hecho
  para los 8 (audio/lyria_tramo1..8.mp3; tramo 1 = ig_lyon t1, 2-8 = lol_worlds_2026 t3, t2, t1, t4, t8, t7, t5).
- ✅ 18:25 (sigue la sesión 5: la app no deja abrir sesiones desde un encargo de sesión) música armada (9 tramos; 1 = cfo_kc_worlds t4,
  7 = lol t5, 8 = ig_lyon t3, 9 = lol t10 desde 57 s) · sfx/ copiados de t1_koi (UI) · `fx` → audio/fx.wav · miniatura.py →
  miniatura/elegida.jpg (sin spoiler) · youtube_texto.md · render_par.py ajustado. ▶ 18:27 render_par.py lanzado (render_par/par_*.log).
- ✅ 17:55 render_par (18 min) → vivos_audio → mezcla (−14,3 LUFS) → final → verificar OK: salida/cfo_kc_jugadas_MASTER.mp4 17:30 + .srt.
  Revisión: boleta con ✓/✗ como «0» (fuente) y fila 1 encima del sub → arreglado en mg_lol.boleta; ▶ 18:00 re-render SOLO par_5
  (875-1050) en %TEMP%/cfo_kc_par, concat de par_0..5 → final → verificar. Luego: avisar → Studio (youtube_texto.md, miniatura/elegida.jpg).
- ✅ 18:12 par_5 re-renderizado + concat + final + verificar OK (MASTER 1097 MB, boleta bien) · `avisar` hecho.
  FALTA: subida por Studio (Crónicas de ligoleyen). 18:15 BLOQUEADO: el navegador integrado tiene la cuenta Google «Edson Iñiguez»
  (sin canales); Crónicas de ligoleyen no sale en el selector → el usuario debe iniciar sesión con la cuenta del canal (o subirlo él).
  Luego: Studio → archivo salida/cfo_kc_jugadas_MASTER.mp4 → textos de youtube_texto.md → miniatura/elegida.jpg → .srt → publicar hoy.
- (texto anterior) FALTA en orden (sesión 6): (1) `lyria_tramos.py armar` (desde videos/cfo_kc_jugadas) dijo «tramo curva2..cierre dura 179 s
  (> 175 s): pártelo en dos» → partir el tramo 8 en 2 en guion.py (curva2..boleta_cfo / numeros..cierre), `biblioteca sugerir`
  + `usar <id> cfo_kc_jugadas 9` (sin repetir piezas) y `armar`. (2) `fab.py cfo_kc_jugadas fx` (SFX + fx.wav) y una hoja de
  revisión rápida (`fab.py cfo_kc_jugadas fx hoja` o escena) de 2-3 pausas. (3) render_par.py: CORTES = [0,175,350,525,700,875,1050.0],
  TMP «cfo_kc_par» → luego `vivos_audio.py` → `mezcla` → `final` → `verificar`. (4) miniatura neutra sin spoiler + youtube.json,
  `fab.py avisar`, subida por Studio (Crónicas de ligoleyen, no está en la API) como t1_koi_worlds. (5) Cierre: lecciones, docs, commit.
## En curso (checkpoint 29-oct 16:45 — CORTE POR CONTEXTO; la sesión 4 sigue aquí)
- ✅ voz 85/85 (umbrales por nombres: investigacion/umbrales.py ya aplicado), `tiempo` = 1039,09 s (17:19), `beats` = 121 (timeline.json, beats.json).
- ✅ NO se usa busquedas/bajar de YouTube (VOD G2 aún no salía): `medios_locales.py` corta medios/scene-NNN.mp4 de las fuentes
  locales (✅ 16:47: 121/121 clips, los de secciones G2 con fuentes de la G1 de reserva → cuando existan g2_j*, borrar esos scene-NNN y re-correrlo; los beats sin fuente G2 quedan para después: re-correrlo cuando existan g2_j*).
  Ojo: sus listas usan g2_j1..g2_j6 — ajústalas a las fuentes que deje el agente de la G2.
- ✅ `investigacion/cam_g1_j*.json` (cámaras para rutas; investigacion/camaras.py <fuentes> para las de la G2).
- ✅ nucleo/mg_lol.py: falta escribir el MG nuevo `boleta(foto, nombre, logo, color, sub, filas=[(ok, texto)])` (aciertos ✓ / errores ✗
  por marca, estilo ficha_jugador) para boleta_kc/boleta_cfo.
- ▶ 16:35 AGENTES en segundo plano (lanzados por la sesión 3; NO relanzar, esperar a que estén sus archivos):
  · ✅ G2 TERMINADO 17:25: datos_g2.md + medios/_fuente/g2_j1..g2_j8 (K: j1 107, j2 317, j3 568, j4 1182, j5 1412, j6 1659, j7 1799, j8 2041;
    feed = HUD + 4). Pausas = Doggo (17:03 hardware; 25:02 bug de tienda → le cambiaron la PC). 3D: J7 = g2_j4 t15/t21 (rep t82-110).
    Ancestral: rematador NO verificable. CORREGIR guion (ver § «Correcciones al guion» de datos_g2.md): jugada8 (Barón ya de CFO, pelea a la
    salida; decir la pausa), jugada9 (Barón de CFO expiró 27:17; la pelea del 30 la inicia Caliste), jugada10 (KC arriba desde el min 33;
    ancestral salió 33:55), curva2 (+1,5K con el alma; +3,7K tras inhibidor), jugada7_rep (38 %, no la mitad), draft2 (quitar «favorito
    de Yike»), jugada6 (pelea 2 por 1). La LCP queda fuera (narrador). medios_locales.py: sus listas G2 deben usar g2_j1..j8 y re-cortar.
  · (antes) G2: escribe `investigacion/datos_g2.md` (K por tramo entre pausas, Whisper vod_g2_480_narr.txt, jugadas J6-J10, cuadros para pausas,
    curva de oro por minuto, «Correcciones al guion» = frases de draft2…curva2 a cambiar) y corta `medios/_fuente/g2_j*.mp4`.
  · ✅ G1 TERMINADO 17:12: `investigacion/pausas_g1.md` (pausas 1-5 y 7 bien medidas; 6, 8, 9, 10 parciales; Shad0w muere en g1_j7 t≈34, no 36) — G1: escribe `investigacion/pausas_g1.md` (posiciones medidas de los PIES en 10 pausas de la G1, rutas, zonas, cortes, repeticiones).
- FALTA en orden: (1) leer datos_g2.md y pausas_g1.md; aplicar «Correcciones al guion» (si cambian frases: borrar sus voz/cands y
  `voz` + `seleccionar` + `tiempo` + `beats` de nuevo). (2) efectos.py con el formato de videos/t1_koi_worlds/efectos.py (helpers J, CLIP,
  PZ, REB, VIVO, LENTA, gris, draft, tar, peg, mg; K de cada fuente; anillos de pausas_g1.md; G2 medir con rejilla2.py), 3D con
  pizarra3d en jugada3 (dragón Químico), jugada7 y jugada10; MG boleta; `fab.py cfo_kc_jugadas fx --seco`. (3) capas 3D
  (`python nucleo/tactica3d/sobre_video.py cfo_kc_jugadas`), vivos_audio.py (VIVOS = fuente+segundo de cada VIVO), MEZCLA._VIVOS en
  guion.py, música de la biblioteca (`fab.py biblioteca sugerir cfo_kc_jugadas`; Lyria dio 429 el 28-oct), sfx. (4) render_par.py
  (CORTES hasta 1039,09; nombre del video) → vivos_audio → mezcla → final → verificar → `fab.py avisar` → Studio (como t1_koi_worlds).
## En curso (checkpoint 29-oct 16:30, sesión «continúa cfo_kc_jugadas» 3)
- ✅ 16:28 guion.py COMPLETO (G1 + G2, 10 jugadas + reps, curva1/2, predicciones, boleta_kc/cfo, números, sigue, cierre; ~1 850 palabras).
  Frases de la G2 solo con datos del feed (posiciones → telestrador tras ver el VOD). ▶ 16:30 `voz` lanzada (voz.log).
- ✅ yt-dlp 2026.08.19 daba HTTP 500 en TODO VOD de Twitch → `pip install -U yt-dlp` (2026.10.21) lo arregló.
  ▶ investigacion/bajar_g2.sh baja vod_g2_480.mp4 (VOD Twitch 5900-10899 → archivo = VOD − 5900 − ~6).
- recursos.py con los 10 campeones de la G2 (iconos/, splash/).
- ✅ 16:20 G2 TERMINADA (API aún «inProgress»; feed «finished» 22:12:28Z): CFO azul (Rest Ambessa, Shad0w Lee Sin, POUT Ryze, Doggo Caitlyn,
  Kino Karma) vs KC rojo (Canna Camille, Yike Pantheon, kyeahoo Viktor 6/0/11, Caliste Yunara, Busio Lulu). NO hay G3.
  `investigacion/g2_reloj.py` (reloj de JUEGO sin pausas) → `g2_asist.txt`; g1_feed.py acepta NFR=480. Reloj VOD Twitch ≈ (pared − 19:15:34Z) + 54 s
  (medido con la G1: feed 20:12:02Z ↔ VOD 3442). G2 juego 0 = pared 20:59:40Z ≈ VOD 6300. Twitch m3u8 dio 500 a las 16:20 (recién cerrado): reintentar.
## En curso (checkpoint 29-oct 15:50)
- ✅ 15:50 Whisper G1 y las 8 fuentes g1_j1..j8 TERMINADAS; K medido (HUD = t + K, K = desde − 3439: j1 296, j2 436, j3 556,
  j4 656, j5 856, j6 986, j7 1436, j8 1566) → **`investigacion/datos_g1.md` ESCRITO** (jugadas, narración citada, predicciones, curva).
  15:47 API: KC 1-0, G2 inProgress (gameId …075).
- FALTA en orden: (1) guion.py con formato de `videos/t1_koi_worlds/guion.py` (VOZ JC ElevenLabs 4XUsiqPDK4UACIM2BILe, FONETICA de
  `cfo_kc_worlds/guion.py`): gancho SIN SPOILER («el que pierda se va a casa») → juego → draft1 (narradores dudan de Tristana) →
  jugadas G1 = J1 Nube por 1.ª sangre, J2 respuesta de Shad0w, J3/J4 dragón Químico ★3D, J5 lo mejor de CFO, J6 dos 3 por 0, J7 pick+Barón,
  J8 ace/nexo (todo en datos_g1.md con t de cada fuente) → curva1 → boleta por jugador (MG nuevo) → «¿se cumplieron las predicciones?»
  (previa: pelea de mitad de partida, dragón, Fearless Rest/Rumble y Yike sin Lee Sin; narradores: Kai'Sa no creció = Doggo 0/3/0 0 %)
  → escenas VACÍAS draft2/jugadas G2 (+G3) → claves/números/sigue/cierre. (2) G2/G3: un agente por partida → datos_g2.md (mismo
  método: VOD Twitch 2914166111, desfase, Whisper, fuentes g2_j*). (3) voz → efectos/3D → render → Studio.
## En curso (antes, 15:00)
- Copiados de t1_koi_worlds: ver.py, rejilla2.py, render_par.py, mesas_3d.py, hacer_busquedas.py, escenas.py, tiempos_mesas.py,
  vivos_audio.py, tiempos.py, hoja.py, recursos.py (ya corrido: jugadores, logos, Data Dragon 16.21.1), investigacion/{api,g1_feed,g1_asist,cortar}.py.
- **VOD de la G1 SIN esperar a YouTube: VOD de Twitch del directo LATAM en español `https://www.twitch.tv/videos/2914166111`**
  (empezó 19:15:34Z; yt-dlp `--download-sections "*a-b" -f 1080p60` SÍ funciona mientras sigue en vivo; el directo de YouTube
  gLo32IvM-Ro NO deja cortar trozos). Draft de la G1 en VOD ≈ 3420 s (cuadro con bans y alineaciones); el juego empieza después.
- ✅ 15:00 bajado `investigacion/vod_g1_480.mp4` (VOD Twitch 3300-5500 s en 480p; log vod_g1_480.log). Si quedó a medias, relanzar:
  `yt-dlp --download-sections "*3300-5500" -f 480p --ffmpeg-location C:/ffmpeg/bin -o "vod_g1_480.%(ext)s" https://www.twitch.tv/videos/2914166111`
  (en investigacion/). Segundo del archivo = segundo del VOD − 3300.
- Hecho para analizar: `investigacion/hojas.py <video> <desde> <hasta> <paso> <prefijo>` (hojas 4×4 rotuladas) y
  `investigacion/g1_narrar.py` adaptado a KC/CFO (acepta ruta .mp4; Whisper large-v3 en GPU, libre a las 15:00).
- ✅ 15:25 DESFASE G1 medido (reloj del HUD cuadro a cuadro): **archivo vod_g1_480 = HUD + 145 · VOD Twitch = HUD + 3445 · feed = HUD + 3/4**
  (1.ª sangre en el kill feed: archivo 498 = HUD 05:53). Fin de la G1 ≈ archivo 1804. Whisper de vod_g1_480 lanzado 15:20 → investigacion/vod_g1_480_narr.txt.
- ✅ 15:40 jugadas vistas en hojas (archivo vod_g1_480 = HUD+145): dragón químico KC HUD 11:31 (archivo 836, «The Inferno
  blazes» = mapa infernal), Canna→Shad0w 11:41 y doble de kyeahoo a Kino/Doggo 11:43-47 (archivo 846-852); 17:19 Caliste→Kino,
  doble 17:21, kyeahoo→Shad0w 17:29 (archivo 1184-1194); 18:31-18:36 rampage de Caliste→Doggo, Yike→Kino, kyeahoo→Shad0w
  (archivo 1258-1263); 24:32 Yike→Shad0w (killing spree), 24:35 POUT→Busio, **Barón KC HUD 24:56** (archivo 1641), repetición
  desde 1647. Feed = HUD + 3.
- LANZADOS 15:20-15:35 (en segundo plano, comprobar al retomar):
  · Whisper large-v3 de vod_g1_480 → `investigacion/vod_g1_480_narr.txt` (log narrar_g1.log; segundos = archivo = HUD+145).
    Si no existe el .txt y no hay python con > 1 GB: relanzar `python investigacion/g1_narrar.py investigacion/vod_g1_480.mp4` desde videos/cfo_kc_jugadas.
  · Fuentes 1080p30 `investigacion/cortar_twitch.py` (nuevo; log cortar_g1.log): g1_j1 VOD 3735+90 (1.ª sangre) · j2 3875+70 (POUT→Busio
    07:50) · j3 3995+60 (Caliste→Kino 09:46) · j4 4095+80 (dragón + 3×0 11:31-11:47) · j5 4300+60 (POUT→kyeahoo 14:48) · j6 4425+220
    (torres 16:35, peleas 17:19-17:29, 18:31-18:36, infernal 17:59, POUT 19:46) · j7 4875+90 (pick + Barón 24:56) · j8 5005+110 (final, nexo 27:39).
    Twitch corta por segmentos: **medir K de cada fuente** (HUD = t + K, esperado K ≈ VOD_desde − 3445) leyendo el reloj; reanudable (salta los ya hechos).
- G2 en curso a las 15:35 (API: KC 1-0). Previa cfo_kc_worlds § claves: (1) pelea de mitad de partida (2) objetivos/dragón (3) Fearless: Rest Rumble, Yike Lee Sin.
- Falta, en orden: (1) ~~hojas cada 15 s~~ → leer reloj del HUD → desfase VOD = HUD + K y feed = HUD + ? (2) Whisper de la G1 entera
  (narración LATAM: intenciones y predicciones de los narradores) (3) `investigacion/datos_g1.md` como el de t1_koi_worlds
  (4) cortar fuentes 1080p `medios/_fuente/g1_j*.mp4` con cortar.py adaptado a Twitch (5) guion.py con la G1 + escenas vacías para G2/G3.
- Idea de guion (G1 = paliza de KC 19-3, 27:39): jugadas 05:52 1.ª sangre Yike→POUT, 07:50 POUT→Busio (respuesta CFO), 09:46
  Caliste→Kino, 11:33-11:45 dragón químico + 3 por 0, 14:48 POUT→kyeahoo, 17:18-17:27 pelea 3 por 0 + torres, 18:31-18:36 3 por 0
  + infernal, 24:31-24:59 pick a Shad0w + Barón, 27:21-27:28 ace y nexo. Además: «boleta» de aciertos y errores de CADA jugador
  (MG nuevo), y «¿se cumplieron las predicciones?» = las 3 claves de la previa `cfo_kc_worlds` (pelea de mitad de partida,
  objetivos, Fearless: Rest gastó su Rumble en la G1; Yike no sacó Lee Sin) contra lo que pasó. SIN SPOILER en gancho/título.

## Lecciones de este video (solo lo no obvio)
- Fuentes Bold Condensed del kit sin ✓/✗/❚❚: dibujarlos con líneas (mg_lol.boleta, miniatura.py).
- En Windows, `sobre_video.py` y `biblioteca`/`lyria_tramos` fallan al imprimir «→» (cp1252): lanzarlos con PYTHONIOENCODING=utf-8.
- Re-render de un solo tramo: `video --tramo a-b --salida %TEMP%/cfo_kc_par/par_k.mp4` + concat de par_lista.txt (5 min, no 18).
- `python fab.py nuevo --help` CREA un video llamado «--help» (borrado a mano).

## Cierre (regla del 12-oct-2026)
- [ ] subido por Studio y PROGRAMADO, miniatura, .srt, monetización
- [ ] HALLAZGOS documentados en docs/estilo_analisis_tactico.md
