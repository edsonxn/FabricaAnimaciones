# Los 25 ERRORES que estás cometiendo en WoW Forever — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · sáb 7-nov-2026 09:00 CDMX (fecha Overgear, enlace `overgear.s.gy/CRONICAS/4`)
- estilo: secuencia_yt (gameplay por beat + pegatinas + MG + mapas con ruta + Overgear con fondo de marca) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ SUBIDO y PROGRAMADO sáb 7-nov 09:00 CDMX (ju5Tc0pqtbg) · MASTER 23:47
- siguiente: Studio por navegador (monetización + cuestionario, video relacionado de Shorts) · medir votos de voces y retención a 7 días

## Sesiones (UNA sesión directo al MASTER, regla 5-nov; relevo si corta a 180 mil)
- alias: errores de Forever, los 25 errores, el del 7-nov
- vista previa: no; render a la tele solo (regla 5-nov)
- leer al empezar: este ESTADO.md · docs/voz.md § «VARIAS VOCES QUE COMPITEN» · copiar de `videos/tes_dwemer_desaparicion/` (voces) y `videos/wow_objetos_secretos_forever/` (Overgear, mapas, MG)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + tiempo | ◐ parcial 5-nov | guion ✅; voz lanzada ~23:00 (corte a 180 mil) |
| 2 | beats + búsquedas + bajar + pegatinas + mapas + efectos + chequeo | ✅ 6-nov | 45 clips rehechos, promesas.md |
| 3 | OST + SFX + mezcla + render + final + verificar + miniatura Flow + subir 7-nov + mover clases_ocultas | ✅ 6-nov | MASTER, subido ju5Tc0pqtbg, clases_ocultas → 12-nov |

## Decisiones del episodio (el usuario, 5-nov-2026)
- Tema: «Los 25 ERRORES que estás cometiendo en WoW Forever (y cómo arreglarlos)», opción 1 de canales/formula/cronicas_warcraft.md (5-nov). **22 min.**
- Overgear: fecha 7-nov → enlace `/CRONICAS/4` (el enlace va con la FECHA), fondo de marca, logo blanco, promoción pagada; NUNCA hablar mal de comprar oro/boosts.
- `wow_clases_ocultas` (POmeaxw16n0, hoy sáb 7-nov 09:00) se MUEVE al **jue 12-nov 09:00 CDMX** (hacerlo justo antes de subir este).
- **VOCES (el usuario, 5-nov, sustituye a la discusión Johnny/Applio/Remy del 2-nov): competencia de voces como en Tamriel**, mismas voces
  (Edoardo, Hope, José, Mario, MariCarmen, el Profeta, el Humano tras el Telón) pero **SIN Johnny: en su lugar la de Applio** (la de siempre
  de Warcraft, presenta). El público vota en comentarios; papeleta + placa «NARRA · VOZ n DE N» (hay que hacer `mg_wow.narrador/votacion`).
- Saldo 5-nov: ElevenLabs cuenta 1 = 0, cuenta 2 = 3 316, cuenta 3 = 226 → Applio (gratis) lleva más reparto (gancho, Overgear, comentarios, ~4 puestos).
- Comentarios (5-nov): 44 nuevos. Ver `canales/comentarios/cronicas_warcraft.json`. Elegir ≥ 4 agradecimientos y 1-2 críticas (≤ 10 días, no usados).

## En curso
- **6-nov ~10:00 (relevo 2, corte a 180 mil):** HECHO: `bajar` 168/168; hojas `medios` revisadas → ~45 clips rehechos (webcams, rótulos de otros canales, webs, retail, «Blizzard presents»; fijados a mano 028 066 129 130 155 con `--url`); NO lanzar `bajar` en paralelo (pisa `fuentes.json`). Pegatinas `jabali.png` y `lich_king.png` sustituidas por capturas reales de los clips 155/127 (originales en el scratchpad). `efectos.py`: Kodo «6000 de favor» (decía «de oro») + pegatina `gnomeregan` (libro de Rumi). `promesas.md` (41) + `_promesas.py` → `previews/promesas_0N.jpg` revisadas ✅. `chequeo` ✅ (avisos de sonido = falsos positivos: las voces nombradas se oyen). `musica_wow.py` + `fab.py <v> musica` ✅ → `audio/musica.wav` 1440,6 s.
- 6-nov ~10:05: `fx` (fx.wav ✅ 09:20; el montaje del panel se cortó por timeout, da igual) · `mezcla` ✅ (−14,3 LUFS, voz +13,8 dB) · `youtube.json` ✅ (capítulos, Overgear `/CRONICAS/4`, promoción pagada) · miniatura RECHAZADA (Pixar) y rehecha con orco in-game + interfaz real (`miniatura_componer.py`, `salida/miniatura.jpg`) · `video` LANZADO ~10:05 → `_video.log`.
- **6-nov ~10:20 CAMBIO DEL USUARIO (vía la sesión que me lanzó):** render DETENIDO. (a) Voces más tarde: Remy (Applio) da gancho + c25 + c24; escena `voces` va DESPUÉS de c24, corta (9 frases, ~30 s); Edoardo = c23 + c20; cierre_2 y c23_5 reescritas; tramo 1 de música = intro,c25,c24,voces y tramo 2 = c23. Copia del guion anterior en el scratchpad (`guion_antes_voces.py`). 60 tomas borradas (c25, c24, c20, voces, cierre_2, c23_5) → `voz` LANZADO ~10:25 (`_voz3.log`). Después: seleccionar → tiempo → beats → REMAPEAR clips viejos a los beats nuevos por texto (no rebajar todo) → fx --seco → chequeo → mezcla → video. (b) Miniatura: texto con Nano Banana (no PIL) + tooltip real de ítem raro/épico + más fondo real; comparar con las antiguas.
- (b) HECHA 6-nov ~10:40: miniatura con texto de Nano Banana + tooltip real + fondo de Los Baldíos (`salida/miniatura.jpg`, receta en prompt_miniatura.md § VIGENTE).
- 6-nov ~11:30: voz ✅ 194/194 (247 créditos; saldo ≈ 30 097) · tiempo ✅ 23:26 · beats 164 · clips REMAPEADOS por texto (`_remapear.py`, viejos en `medios/_viejo/`, 36 rebajados con url+desde) · efectos reanclados (papeleta, com del Humano, voto de Edoardo) · cuadros del arranque ✅ · 8 opciones de miniatura (`previews/miniatura_opciones.jpg`, `miniatura_ing/opciones/op1-8.jpg`) ENVIADAS a la sesión madre: el usuario ELIGE; no subir otra · cadena musica→fx→mezcla→video LANZADA (`_cadena.log`).
- FALTA en orden (tras lo anterior): `video` (largo, en segundo plano) → `final` → `tele video wow_errores_forever master` (segundo plano) → `verificar` → miniatura Flow → mover clases_ocultas al 12-nov → `yt subir … --publicar 2026-11-07T15:00:00Z` → registrar → `canales --actualizar` → commit.
- 6-nov madrugada: voz ✅ (Applio se cayó a la frase 14 por la GPU compartida; relanzado; ElevenLabs 2 632 créditos, cuenta 2 queda ≈ 30 489), seleccionar ✅ (22 aceptadas por hipótesis en CER/TAIL_MAX; voces_5 reescrita), tiempo ✅ 24:00. La app no dejó abrir sesión de relevo (turno de aviso): se sigue en este hilo.
- Hecho: investigación `videos/_investigacion_wow_errores_forever.md` · `guion.py` (195 frases; reparto en `NARRA`/`VOCES`/`LEMAS`) · 10 tarjetas `com_*` en `pegatinas/` · `nucleo/mg_wow.py` + `narrador()` y `votacion()` (probadas) · `medios/_overgear/` y `musica_wow.py` copiados de `wow_objetos_secretos_forever`.
- Falta, en orden: (1) ✅. (2) ✅. (3) beats ✅ busquedas ✅; `bajar -j 4` lanzado 6-nov → `medios` (MIRAR hojas); beats 077-081 = Overgear (los tapa el fondo de marca). (4) ✅ 6-nov: `_pegatinas.py` (97: íconos zamimg + Wowpedia; NO usar hillsbrad/costasur/nerzhul/ritual/elwynn: son de WC2, bocetos o erróneos), `mapas/` copiados, `efectos.py` escrito (placas automáticas desde guion.NARRA, papeleta inicio y cierre, 7 mapas, 10 comentarios, Overgear, tarjetas). Original: pegatinas, mapas con ruta (≥ la mitad donde se pueda: Humedales/Auberdine, Trinquete, Ventormenta/Entrañas, Crestagrana/Baldíos campamentos, naufragio), `efectos.py` con placa `M.narrador(nombre, LEMAS[n], k, 8)` en cada cambio de voz y `M.votacion` en el cierre (cada voz marca su casilla), MG nuevos por guion, Overgear (copiar bloque de `wow_objetos_secretos_forever/efectos.py`). (5) `chequeo` → SFX del juego → `mezcla` → `video` → `final` → `tele video <v> master` → `verificar`. (6) Miniatura Flow. (7) Mover `wow_clases_ocultas` (POmeaxw16n0) al jue 12-nov 09:00 CDMX; `yt subir wow_errores_forever cronicas_warcraft private --publicar 2026-11-07T15:00:00Z`; youtube.json con `overgear.s.gy/CRONICAS/4` y PATROCINADO; registrar.

## Hecho
- 5-nov: proyecto creado (`nuevo --yt`), canales actualizado (Warcraft PRONTO, 2 programados), fórmula anotada.

## Falta
- [ ] todo lo de los tramos

## Lecciones de este video (solo lo no obvio)
- `bajar` en paralelo (varios procesos) pisa `fuentes.json`: uno a la vez.
- Script propio que importe `secuencia_fx`: poner la carpeta del video ANTES de `nucleo/` en sys.path (si no, «efectos» = nucleo/efectos.py y la capa sale vacía).
- Al reordenar escenas tras bajar clips: `_remapear.py` reasigna clips por texto y solo rebaja los cortos con url+desde (36 de 164).
- `CER_MAX_POR_FRASE` con claves repetidas: gana la última (la vieja) → borrar la antigua al aceptar una nueva.
- Miniaturas WoW: in-game real (nada de cinemática Pixar), texto de Nano Banana (no PIL), interfaz real; dar 6-8 opciones de texto.
- Voces de competencia: el narrador de siempre da 1-2 datos antes de presentar a las demás (presentación ≤ 30 s).

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO 7-nov (ju5Tc0pqtbg), miniatura Flow op6 elegida por el usuario, registrado (`canales/cronicas_warcraft.json`, BITACORA); clases_ocultas (8hNPy07Bu4A) movido al 12-nov
- [ ] Studio: monetización + cuestionario (https://studio.youtube.com/video/ju5Tc0pqtbg/edit)
- [ ] HALLAZGOS documentados
