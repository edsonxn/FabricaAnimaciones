# Worlds 2026: todo lo que ha pasado (resumen de ~22 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Cronicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; el usuario, 27-oct: subido por la pestaña de Studio, NO está en la API ni en canales/*.json)
- estilo: análisis táctico (secuencia_yt con clips del VOD + telestrador `nucleo/mg_tactica.py`) → doc: docs/estilo_analisis_tactico.md
- etapa: v2 SUBIDA EN PRIVADO por Studio el 27-oct (https://youtu.be/0eS1M_prcaQ): monetización activada (mid-roll), «Nada de lo anterior» → adecuado para anuncios, miniatura elegida.jpg, .srt español. La v1 (lcGGYgWwZEg) ya no existe. El usuario la publica a mano. Revisión tras subir (27-oct): Privado ✓, 22:02 reproducible ✓, monetización «Comprobando» con mid-roll ✓; el .srt había quedado como BORRADOR en el editor (se pulsó «Publicar»), y la tabla de Idiomas sigue generando los automáticos: comprobar ahí que salga Español publicado. OJO para otros videos: subir el .srt en el diálogo de subida lo deja en borrador.
- siguiente: nada de producción. Registrar el canal en canales/ si se va a usar más; ronda 4 (28-30 oct) deja viejos «queviene», «equipos» y «cierre»; al cerrar: `biblioteca catalogar` ya hecho (v1), `limpiar` cuando el usuario apruebe

## Sesiones (plan de tramos · «continúa el video lol_worlds_2026» retoma aquí · protocolo docs/sesiones.md)
- alias: Worlds 22 min, resumen de la Worlds, «el favorito cayó»
- vista previa: SÍ, los primeros ~2 min con audio completo (voz + música + SFX + mezcla) antes de seguir con el resto
- leer al empezar: este ESTADO, docs/estilo_analisis_tactico.md, guion.py (docstring = datos verificados)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | miniatura + investigación + guion + voz | ✅ 27-oct | miniatura «EL FAVORITO CAYÓ»; guion 109 frases; voz JC 2 703 créditos; tiempo 22:01 |
| 2 | clips 1-38 + jugada 1 analizada + música Lyria (10 tramos, todo el video) + vista previa 0-5:26 | ✅ 27-oct | render de 326 s en 205 s; vivo a −15 LUFS |
| 3 | clips 39-155 + jugadas 2-6 analizadas (+ rótulos de jugadores/equipos) | ✅ 27-oct | 154 clips; 3 frases corregidas con el VOD (j2, j3, j5); zoom en FX video; MG nuevos (ficha, ranking, tabla, calendario, barras) |
| 4 | fx → ambiente → mezcla → render completo (tramos paralelos) → final → verificar → aviso; catalogar música | ✅ 27-oct | −14,46 LUFS, voz +9,1 dB; render 6 tramos en 21 min; MASTER 22:01 (1,26 GB), desfase 0 ms, CER 0,020 (nombres); música catalogada; subido en privado por Studio con monetización. Montaje del panel a medias (montaje lo completa) |
| 5 | revisión de las 6 jugadas en cuadros (REVISION_JUGADAS.md) + j6 en 3D (nucleo/tactica3d) + capas/mesas 3D j1-j5 + voz 10 frases + re-render | ✅ 27-oct | MASTER v2 22:01, verificar OK (desfase 0 ms; CER alto solo en nombres). Tras revisarlo, 2 rótulos de las mesas j1/j2 corregidos: tramos 276-284 y 445-455 re-renderizados (salida/fix_a/b.mp4) y empalmados EN C: (scratchpad emp/) porque E: tuvo daño NTFS 55 a las 15:28 (reparado 15:30); MASTER copiado a E: con MD5 idéntico. El usuario lo vio y aprobó → subido en privado por Studio (0eS1M_prcaQ) con monetización, miniatura y .srt |

## Decisiones (el usuario, 27-oct-2026)
- duración ~22 min; las mejores jugadas analizadas + mejores jugadores, mejores equipos, panorama para ponerse al día.
- carpeta nueva (la prueba `lol_worlds_tl_al` = el Barón de Liquid, se reutiliza como una jugada). 4 sesiones. Sin canal.
- miniatura: «EL FAVORITO CAYÓ» (B2 de Flow). El guion debe sostenerlo: Anyone's Legend, campeón del LPL, fuera 0-3.

## En curso — tramo 5: corrección de jugadas + JUGADA 6 EN 3D (checkpoint 27-oct, sesión 5)
- El usuario (27-oct): «las jugadas deben analizarse bien sin errores» + en la más importante un sistema 3D (three.js) que
  enseñe intenciones, movimientos y rutas. Elegida la j6 (el Barón que elimina a AL = título del video).
- ✅ j6 VERIFICADA (narración oficial transcrita con Whisper + minimapa medido cada 2-6 s): el dragón lo remata Yeon; AL tenía
  3 (3-3, nadie con alma); cae la TORRE del inhibidor (7-2 a las 40:32), el inhibidor AGUANTA; Tarzan llega con Paranoia;
  AL intenta cortar por un flanco y Liquid se retira; «how dark the map is» para AL; Barón 41:35-41:46.4 (15 619 → 11 166 →
  3 634 → 1 166); el robo lo intenta HOPE con el cohete de Jinx (no el Nocturne). Frases jugada6_2 y _3 reescritas y
  regeneradas (44 créditos), `tiempo` sin mover escenas (total 1321,09). El tablero 2D viejo tenía posiciones inventadas.
- ✅ Kit nuevo `nucleo/tactica3d/` (grieta3d.html/js + three.js r160 en vendor/, preparar_grieta.py, render3d.py con Edge sin
  ventana y la GPU). Escena `j6_3d.py` → `tactica3d/j6.json` → `medios/_fuente/j6_3d.mp4` (35,3 s en 66 s). efectos.py: el 3D
  ocupa 975.7-1010.27 y vuelve al VOD en el castigo. `fx --seco` OK.
- ✅ Vista previa con audio completo: salida/VISTA_jugada6_3D.mp4 (+ _movil.mp4), 16:09-17:09; enseñada al usuario.
  OJO: `fab.py fx` también exporta la capa visual entera (secuencia_fx, >15 min); para solo el audio basta con que escriba
  audio/fx.wav (los primeros ~30 s) y luego `mezcla`.
- ✅ j1-j5 revisadas (REVISION_JUGADAS.md § «ESTADO 27-oct»); textos corregidos en guion.py (9 frases + FONETICA Myrwn/Jayce).
- ✅ voz (10 frases, 241 créditos) → seleccionar 109/109 (umbrales CER/cola por nombres) → tiempo con "post" 1.8 en jugada1 y
  2.6 en jugada5 (las escenas vuelven EXACTAS a timeline_beats.json, total 1321,09) → efectos.py j1-j5 ajustados (15 cambios)
  → fx --sin-montaje → mezcla (−14,45 LUFS, voz +9,0 dB) → `render_par.py` lanzado (6 tramos).
- El usuario vio la vista previa: «se ve bien» + intercalar VOD real con 3D y elementos 3D sobre el video, en TODAS las
  jugadas. ✅ Motor: modos «video» (capa transparente) y «mesa» (cuadro real proyectado en 3D). ✅ j6 intercalada (V3 + 4
  capas pizarra3d); j1-j5: pausa con capa 3D + escena mesa (mesas_3d.py → medios/_fuente/mesa_j1..j5.mp4); j4 Barón con capa.
  Capas en tactica3d/capas/ (8). 3D del dragón corregido a 40:20,6. Sonidos de transición. fx + mezcla −14,46 LUFS.
- ✅ render_par.py (6 tramos) → final (+ fix_a/fix_b empalmados) → verificar OK (27-oct, sesión 6) → avisado; falta subir de nuevo en privado por Studio. (Antes, plan original:) `voz` → … → ajustar
  efectos.py de j1-j5 (tarjetas/pegatinas: Keria+Neeko en j2, Myrwn/Jayce en j3, sin «Busca a uno solo» en j4, sin «espera
  atrás/que Hanwha gaste» en j5, sin «KC cierra el paso»/«por detrás» en j1) → fx → mezcla → render 6 tramos → final →
  verificar → subir en privado por Studio.

## Tramo 3 (checkpoint 27-oct, sesión 3)
- busquedas.json 39-154 escritas (partidas ubicadas en H1-H4 con investigacion/*.txt; vivo 108 = VOD wjoQ0ze5bJ4@2909).
  `bajar` lanzado (116 clips). ambiente_por con 045/065/078/090/108 → `bajar 45 65 78 90 108 --rehacer` para el audio.
- Fuentes de jugadas cortándose: j2 = H2@1960, j3 = H3@830, j4 = H3@1230, j5 = H3@215 (150 s c/u, script en scratchpad
  cortar_jugadas.py: yt-dlp -g + ffmpeg -ss). j6 = ../lol_worlds_tl_al/medios/_fuente/jugada.mp4 (no copiar: C: lleno).
- Narración oficial verificada (⚠ de abajo resueltos): j2 «Goodbye Lucid… Elder down to 12k… flash forward… Renata, Smash
  knock up… from nothing they put T1 to ashes» (H2 33:42-34:14); j3 «Jojo stepped too far forward, anchor onto the bird…
  Supa taken out, the exhaust means nothing… penta» (H3 14:49); j4 «they get the Baron, LYON! (rend)… Inspired jumped into
  the center… Chovy is killed» (H3 20:59-22:10); j5 «Infernal soul… Gumayusi needs a bailout… Rookie… polymorph… down goes
  the Olaf… triple… quadra» (H3 4:10-5:05).
- ✅ 154/154 clips en medios/. Vivos con audio: `bajar 45 65 78 90 108 --rehacer` lanzado.
- ✅ JUGADA 2 CORREGIDA (no era verdad «T1 atrapa a Lucid… con uno menos»: Lucid murió en el 37:08 y en la pelea del Anciano,
  40:25, está vivo). Frases jugada2_0/1/2/4 reescritas y regeneradas (75 créditos), `seleccionar` 109/109, `tiempo`: con
  "post": 1.6 la escena conserva 46 compases → nada se movió (total 1321.09). beats.json NO se regeneró (solo cambian los
  textos de los beats 046-056, tapados por el FX de j2).
- ✅ ZOOM programado en el FX `video` (nucleo/secuencia_fx.py `_zoom_video`): `zoom=(z, cx, cy)`, `zoom0`, `zoom_en`,
  `zoom_dur`. La pizarra se mide sobre el cuadro ya acercado (scratchpad rejilla.py n:t:z:cx:cy → previews/cuadros/).
- ✅ También CORREGIDAS jugada3_0 (KOI llegó a +0,8K en el 32:30, no «acababa de ganar una pelea») y jugada5_0 (el alma del
  Infernal es de IG: sus 4 dragones en el marcador 24:21). 44 créditos. Escenas sin moverse (total 1321.09).
- ✅ MG nuevos en mg_lol: ficha_jugador, ranking, tabla, calendario, barras; resultados acepta ganador None («VS»/fecha).
  Hoja: previews/mg_lol_nuevos.jpg (`_prueba_mg_nuevos.py`).
- Pausas medidas (previews/cuadros/j*_a/b.jpg): j2 pausa 74.6 (40:25; Anciano .84,.27; T1 Doran .665,.31, Peyz .71,.52,
  Keria/Oner .62,.76; DK grupo .385,.55); j3 pausa 59.5 (Jojo .385,.19; Career .47,.21; KOI .08-.34 × .25-.6), penta 79;
  j4 Barón 29.0 (20:24, «Blue team has slain Baron»), Inspired 84.0 (Inspired .36,.42; Chovy .40,.33), Chovy cae 90.5;
  j5 pausa 61.0 (Rookie .465,.70 detrás; JiaQi .235,.68; Meiko .325,.68; Wei .5,.55), cuádruple 92.
- ✅ efectos.py 323-1321 escrito (336 efectos, 351 sonidos; `fx --seco` OK). Revisado en previews/tramo3_a/b/c.jpg.
  OJO: el FX `cierra` sin `a` deja NEGRO hasta el final: el de 322 s (y el de 481 s) llevan ahora `a` + `abre`.

## Tramo 2 (checkpoint 27-oct ~15:50)
- El usuario APROBÓ la v2: «me gusta todo». REGLAS DEL ANÁLISIS (el usuario, 27-oct): en las jugadas analizadas usar FLECHAS,
  CAMINOS (rutas), ZOOM; las tarjetas/pegatinas durante la jugada CHICAS y en los BORDES (no tapar la acción): tarjetas tam 30-44
  en las esquinas (x .1/.87, y .13-.29) o abajo sobre el marcador (y .86); pegatinas tam 210-240 en x .07/.93. Ya aplicado a la
  jugada 1 (+ 2 flechas y una zona en la pausa 24:36); falta re-renderizar (`fx` → `mezcla` → `video --hasta 326`) si se quiere ver.
- ZOOM sobre el cuadro congelado aún NO existe en mg_tactica (pendiente del estilo): programarlo (zoom del FX video + pizarra
  transformada) en el tramo 3 o usar el `tablero` con cámara.
- efectos.py 0-323 REESCRITO con mg_lol (93 efectos: portada, AL eliminado, pegatinas, VS, caídas, menú, suiza, resultados,
  pegatinas de campeones en el análisis). fx + mezcla (−14,4 LUFS, voz +10,8 dB) + `video --hasta 326` ✔ (736 s: los MG nuevos
  hacen el render ~3,5× más lento → el video completo, en tramos paralelos). Hoja: previews/avance_hoja2.jpg (revisada, sin choques).
- Pendiente menor: placas de nombre de las pegatinas algo chicas (tam 40 en mg_lol.pegatina → subir a ~48).
- 27-oct tramo 2: beats (155) → busquedas.json 1-38 con {url, desde} de los RESÚMENES oficiales (H1-H4 abajo) → bajar 1-38 ✔
  (mosaico previews/mosaico_1_38.jpg revisado). Jugada 1 hecha: medios/_fuente/j1.mp4 (H1 desde 1000 s, 150 s), efectos.py con
  rebobinado, pausa con telestrador a 24:36, cámara lenta, cuádruple, Barón, nexo y lección. Rótulos de gancho, formato, play-in
  y día 1. Música: 10 tramos Lyria NUEVOS (audio/lyria_tramo1-10.mp3) armados; MEZCLA["musica_curva"] baja 16 dB en los
  6 tramos en vivo (_VIVOS en guion.py). sfx/ copiado de la prueba. fx, ambiente, mezcla (−14,4 LUFS) ✔.
  Lanzado `video --hasta 326` → salida/lol_worlds_2026_AVANCE.mp4 (log E:\...
ender_avance.txt).
- Resúmenes: H1 `_9iVitbeCio` (día 1) · H2 `Fbxau2uQc_E` · H3 `Oix7cBcGmgM` · H4 `ys6RaOaqCy0`; himno `mlFxxNsExJc`; sorteo
  `0E9gvrpiMzc`. Partidas dentro de cada resumen (m:s): ver investigacion/*.txt.
- Cada jugada tiene `pre` = 52 s: la jugada se ve PRIMERO en vivo con el audio de la transmisión (poner esos beats en
  `SECUENCIA["ambiente_por"]` y bajar con audio), luego `rebobinar()` y la voz la analiza con pausas/telestrador.
- ⚠ Frases a VERIFICAR con el VOD en el tramo 2 (si no cuadran, regenerar solo esa frase): jugada2_3 (cómo entra Career y el
  lanzamiento de Kalista), jugada4_1 (Barón de LYON con Kalista), jugada5_0/1/2 (oro, Lulu/Olaf), jugada3_0.
- Las 6 jugadas y sus VOD (EpicSkillshot; lista completa en investigacion/vods_epic.txt):
  1 KC vs AL (oL7SoVo7diQ, cuádruple de Canna) · 2 DK vs T1 (CH58ZuCC_lQ, Anciano) · 3 KOI vs DK G1 (5ncuDEGwbkg, penta de
  Smash) · 4 LYON vs GEN G1 (zNTyYcB20Mg, Inspired) · 5 IG vs HLE (rxkYf8BOHSQ, cuádruple de Rookie) · 6 AL vs TLAW G2
  (wjoQ0ze5bJ4, Barón; reutilizar el análisis de ../lol_worlds_tl_al/efectos.py). Momento exacto: resúmenes de LoL Esports
  en investigacion/*.txt (marca [mm:ss] del resumen) → ubicar con el reloj del juego en el VOD.
- Dónde está cada jugada en los RESÚMENES oficiales de LoL Esports (sacar ahí un cuadro, leer el reloj del juego y saltar al
  VOD): 1 `_9iVitbeCio` [17:26-18:00] · 2 `Fbxau2uQc_E` [33:11-34:14] · 3 `Oix7cBcGmgM` [14:19-15:21] · 4 `Oix7cBcGmgM`
  [20:28-22:32] (Barón de LYON ~20:59, Inspired ~22:00) · 5 `Oix7cBcGmgM` [3:40-5:11] · 6 ya cortada en la prueba (VOD 2833-3013 s).
- El video es una FOTO al 27-oct: si se publica tras la ronda 4 (28-30 oct), rehacer «queviene», «equipos» y «cierre».

## Hecho
- miniatura (4 de Flow, elegida B2) · carpeta creada con `nuevo --yt`
- investigación en `investigacion/`: resúmenes oficiales de los 4 días (txt), picks de 51 VOD (`picks.txt`), gol.gg (`gol_*.csv`)
- guion.py: 23 escenas, 109 frases, ~2 450 palabras, FONETICA de 70 nombres; voz JC (eleven_v4_turbo) 109/109 con umbrales
  por frase (Whisper oye «Carmen Corp», «Genji»); 15:26 de voz; `tiempo` → 22:01

## Falta
- [x] guion · [x] voz · [ ] clips · [ ] telestrador · [ ] sonido · [ ] render · [ ] verificar

## Lecciones de este video (solo lo no obvio)
- Wikipedia anotó «Bo3, 2-1» en partidas de la ronda 3 que fueron al mejor de 1: contrastar con la lista de VOD (uno por partida).
- gol.gg tarda en cargar el último día: al citar números, mira «Games» de cada equipo contra el calendario.
- 60 `yt-dlp` en paralelo (descripciones) → HTTP 429 «Sign in to confirm you're not a bot» un rato: lanzar en tandas de ≤ 8.
- Los RESÚMENES oficiales de LoL Esports sirven de fuente de clips Y de tramo en vivo: ya traen la jugada entera y la voz de los
  narradores; con sus subtítulos se ubica cada partida sin mirar el video.
- Las descripciones de EpicSkillshot traen los picks de cada partida: fuente rápida para no inventar campeones.
