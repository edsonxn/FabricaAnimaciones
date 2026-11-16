# 30 trucos para NUNCA quedarte sin ORO en WoW Forever — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · **vie 20-nov-2026 09:00 CDMX** (hueco de `canales` del 15-nov) · **SIN Overgear (el usuario, 15-nov)**; aun así NADA contra comprar oro (campaña 3 de Overgear arranca el 25-nov)
- estilo: secuencia_yt (gameplay por beat + pegatinas + MG + mapas con ruta) → doc: docs/estilo_secuencia_yt.md · copiar de `videos/wow_forever_experiencia/` (30 min, sin Overgear) y `videos/wow_errores_30_60/`
- etapa: ✅ SUBIDO y PROGRAMADO vie 20-nov-2026 09:00 CDMX → https://youtu.be/WZQBgTB3HNw (privado hasta entonces; MASTER 29:22, .srt, SIN Overgear)
- siguiente: (1) ✅ miniatura de Flow aplicada el 16-nov (`salida/miniatura.jpg`, opción B de `miniatura_ing/opciones/`) · (2) ✅ Studio 16-nov: monetización Activada (salió Desactivada) + mid-rolls + cuestionario (solo Violencia 1.ª → «Adecuado para anuncios») · (3) métricas a 7 días → formula · al aprobar: `fab.py wow_oro_forever limpiar`

## Sesiones (UNA sesión directo al MASTER, regla 5-nov; relevo si corta a 180 mil)
- alias: oro de Forever, los 30 trucos de oro, nunca sin oro
- leer al empezar: este ESTADO.md · `videos/_investigacion_wow_oro_forever.md` · docs/estilo_secuencia_yt.md (grep)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | canal + comentarios + investigación + guion + MG nuevos (`nucleo/mg_oro.py`) + voz + clips + efectos + revisión + render + subida | ✅ 15-nov | WZQBgTB3HNw, vie 20-nov 09:00 |
| 2 | miniatura de Flow (relevo) | ✅ 16-nov | reintento único sin bloqueo; B elegida (logo grande, más oro); `yt aplicar` conserva privado + publishAt · Studio: monetización + cuestionario |

## Decisiones del episodio (el usuario, 15-nov-2026)
- Tema: opción 1 de `canales/formula/cronicas_warcraft.md` (conclusión del 15-nov): una variable sobre «20 errores del 30 al 60» = el tema (oro). Referencia fuera: Vuxxy «never go broke» ×8,7.
- Duración ~30 min (la pidió el usuario). Fecha: vie 20-nov sin Overgear.
- Voz: Remy (Applio) entero, la de siempre (los comentarios la piden; la competencia de voces no gusta). FONETICA de `wow_forever_experiencia`.
- Comentarios (15-nov; tarjetas `pegatinas/com_*` hechas):
  - CORRECCIÓN justa: @Jorge_alvarez_ (UgzL7HlT…) «la doble especialización cuesta 50 g, no 10 g» (lo confirma también @jeimy88-j2k) → enseñarlo y darle la razón.
  - AYUDA: @rafaelmartinezsantana7055 (UgxCYAWA…) «inventario lleno de objetos de misión» → truco de bolsas.
  - Gracias: @Alan-kb5iz (UgzLV1m3…) @Leon89vlk (Ugy4zNo2…) @JONATHANTX111 (UgxBfWWi…) @JotaBerttuci (UgxeV-jR…).
  - Burla (amable por fuera): @Ehren-03 (UgxtHhlq…, «dejen jugar sin optimizar… sin pagar para aprender») · @vincent1785 (Ugx9MgSZ…, iceberg «ni una foto, acto de fe» → hoy cada moneda sale en pantalla) · @CaneAttack (Ugxmhp_a…, «no aprecio la info con estos tipos de voz» → hoy la voz de siempre).
  - Ya usados (no repetir): AlbertoHans, arnoldhoward, Fetixe22, PentaGRam8666, yorshnado, pablisho, AlexAnder, sgto.sevilla.

## En curso
- 15-nov: `nuevo` ✅ · tarjetas ✅ · investigación ✅ `videos/_investigacion_wow_oro_forever.md` (doble esp. = 50 g comprobado) · guion ✅ (`_alargar.py` ya aplicado: NO volver a correrlo) · voz LANZADA ~11:30 → `_voz.log` (ojo: hay un `starship_sin_patas video` colgado desde el 14-nov 18:34, PID 3592/21056; no es nuestro).

## Lecciones de este video (solo lo no obvio)
- Videos de ~30 min con 10 GB de commit libre: mezcla/verificar caían por RAM → arreglado en el núcleo (float32). Si vuelve: reiniciar la PC (≈45 GB comprometidos fuera de procesos visibles el 15-nov).
- Flow puede bloquear con «Hemos detectado actividad inusual» (filtro anti-bots): no se salta; miniatura provisional de un cuadro y reintentar otro rato.
- Applio: «Solo matar humanoides.» sonó a italiano; un nombre al inicio de la frase («Ehren, …») tumba el detector de idioma → reescribir sin el nombre delante.
- `mapa(objeto=)` = nombre de ícono de Wowhead, no ruta. ffmpeg de yt-dlp falla a veces con código 3436169992: reintentar con -j 2.
- 15-nov ~11:40: subagentes LANZADOS: clips → `_busquedas.py`; coordenadas → `_coords.md` + `_pegatinas.py`/pegatinas/ + previews/_hoja_peg.jpg (revisar hoja a mano).
- 15-nov ~12:10: `nucleo/mg_oro.py` NUEVO (factura, desplome, balanza, escalera, techo, dia_noche; prueba: `python nucleo/mg_oro.py` → %TEMP%/_mg_oro_prueba.jpg, revisada). intro_4 cambiada («más de mil quinientos»): repetir `voz` al acabar para regenerarla.
- ⏸ 15-nov ~12:20 PAUSA del usuario: detenidos la voz y los 2 subagentes. Quedó: `_candidatos.json`/`_candidatos.txt` (búsquedas de clips del subagente, a medio revisar; `_buscar_fuentes.py` con Q nuevo) · NO hay `_busquedas.py`, `_coords.md` ni pegatinas de objetos (solo `com_*`). Al retomar, relanzar esas dos tareas (coordenadas con fuente de Wowhead + pegatinas por identidad con hoja `previews/_hoja_peg.jpg`; SRC por escena → `_busquedas.py`).
- Fecha prevista vie 20-nov 09:00 CDMX: si la pausa se alarga, revisar el hueco con `canales --actualizar`.
- ▶ 15-nov RETOMADO: voz relanzada (`_voz.log`) + subagentes de clips (`_busquedas.py`) y de coordenadas/pegatinas (`_coords.md`, `pegatinas/`, `previews/_hoja_peg.jpg`) relanzados. El `starship_sin_patas video` (PID 3592) sigue colgado desde el 14-nov.
- voz ✅ (EXIT 0) · seleccionar LANZADO (`_sel.log`) · `_busquedas.py` ✅ (37 escenas; flojas c10 huevos, c11 almejas, c09 grifos, c16 páginas → reforzar con pegatinas/pant; ojo EoOuPZKl_Rs en portugués y guías con narrador: revisar webcams en hojas de medios).

## En curso (relevo 1, 15-nov tarde, corte a 180 mil)
- HECHO: voz ✅ 227 tomas Applio (`_voz.log`, EXIT 0) · seleccionar ✅ 198/227 (`_sel.log`, voz total 1431,9 s) · `_busquedas.py` ✅ (subagente; `python _busquedas.py` tras `beats`; `--check` OK).
- FALTA 1: las 29 de REGENERAR: c28_3 burla0_1 c26_5 c24_4 c23_0 c22_3 c19_0 c18_4 c17_3 c16_0 c16_1 c16_3 c14_4 c13_1 c11_0 c11_1 gracias2_1 c10_1 c10_2 c09_3 c08_5 c07_0 c07_6 c04_3 c04_4 c03_0 c03_2 c02_0 c02_4. Applio da SIEMPRE la misma toma: leer la `hyp` de Whisper en `voz/eval.json` (clave `<id>_s1.wav`) → si solo falla un nombre propio/cifra, `CER_MAX_POR_FRASE[id] = 0.08` en guion.py; si dice otra cosa o suena en otro idioma, REESCRIBIR la frase (o FONETICA) y `fab.py wow_oro_forever voz` (solo regenera las cambiadas) → seleccionar otra vez hasta 227/227.
- FALTA 2 (en orden): `python nucleo/idioma_voz.py wow_oro_forever` → tiempo → beats → `python _busquedas.py` → `bajar -j 4` (uno a la vez) → hojas `medios` (webcams, caras, rótulos, portugués `EoOuPZKl_Rs`) → `--rehacer` → LYRIA.tramos (OST de WoW, `musica_wow.py`: temas de Gadgetzan/Bahía del Botín/Tanaris/Feralas/Forjaz/Orgrimmar/Desolace/Arathi; ≤ 175 s; distintos de `wow_forever_experiencia`) → efectos.py (helpers de `../wow_forever_experiencia/efectos.py` + MG de `nucleo/mg_oro.py`: factura intro 207+100+1000+200, desplome huevos 1 o→67→49→31→18 p, balanza carne de tortuga 1 c/20 p, escalera respec 1/5/10 vs doble 50, techo Cristal Arcano 9/12,5 vs 50, dia_noche perla de oro 2 o 70 p → 5 o; 9 `com()` de las tarjetas; mapas con `_coords.md`; pegatinas reforzando c09/c10/c11/c16) → promesas.md + hojas → pegatinas_check → chequeo → `FAB_FX_FINAL=1 fx hoja` (mirar todo) → música → sfx → mezcla → video → final → `tele video wow_oro_forever master` → verificar → miniatura Flow (que parezca el juego: subasta/tooltip de oro, texto de Nano Banana) → youtube.json (SIN Overgear) → `yt subir wow_oro_forever cronicas_warcraft private --publicar 2026-11-20T15:00:00Z` → publicados + BITACORA + `canales --actualizar` → commit (incluye nucleo/mg_oro.py).
- SUBAGENTE AÚN CORRIENDO al cortar: coordenadas + pegatinas → `_coords.md` (+ nombres de ícono), `mapas/`, `pegatinas/`, `previews/_hoja_peg.jpg`. La sesión de relevo comprueba que esos archivos existan; si no, rehacer esa tarea (fuente Wowhead, identidad comprobada, mirar la hoja).
- 15-nov (tras el corte, el relevo con start_session lo rechazó la app por turno automático: REINTENTAR en el próximo mensaje del usuario; candado borrado): 7 frases reescritas (burla0_1, c24_4, c19_0, c17_3, c16_3, c14_4, c04_3) + CER_MAX para 22 de nombres → `voz` + `seleccionar` LANZADOS (`_voz2.log`, `_sel2.log`).
- subagente coords/pegatinas ✅: `_coords.md` (23 lugares con fuente Wowhead Forever + íconos), 16 mapas, 58 pegatinas (hoja `previews/_hoja_peg.jpg` revisada por él). Correcciones de nombres al guion PENDIENTES tras `_sel2`: Kildar → Valle del Honor; Frayfeather = hipogrifos; «El Arrecife Mortal»; venda de seda pesada; receta: chuleta de lobo magro; cardoveloz; tela de inferi; Bolsa de paño mágico roja.
- _sel2: 224/227; nombres oficiales corregidos (Valle del Honor, paño mágico, seda pesada, chuleta de lobo magro, Arrecife Mortal, hipogrifos, cardoveloz, tela de inferi) → voz+seleccionar otra vez (`_voz3.log`, `_sel3.log`).
- ✅ voz 227/227 (`_sel4.log`, 1640,4 s). Siguiente: idioma_voz → tiempo → beats.
- ✅ idioma_voz (c17_1 reescrita) · tiempo 29:22 (1762,5 s) · beats 205 · busquedas.json ✅ · `bajar -j 4` LANZADO → `_bajar.log`.
- ✅ efectos.py (83 efectos, 7 rótulos, 8 sonidos; `fx --seco` OK) · sfx/ copiados. Siguiente: al acabar `bajar` → hojas medios → rehacer → promesas → chequeo → fx hoja → música.
- ✅ OST: musica_wow.py (15 tramos, 14 temas) + `fab.py musica` · promesas.md + _promesas.py (58) escritos (falta correrlo tras bajar).

## CHECKPOINT 2 (15-nov ~17:40) — qué falta EN ORDEN
- HECHO además: voz 227/227 · idioma_voz OK · tiempo 29:22 · beats 205 · busquedas.json · efectos.py (83, `fx --seco` OK; MG de `nucleo/mg_oro.py`) · promesas.md/_promesas.py (58) · OST (`audio/musica.wav`) · sfx.
- `bajar -j 4` CORRIENDO (`_bajar.log`, ~17:05; algún FALLÓ, p. ej. scene-125 igHxERi6idE@570 → reintentar con `bajar <ids> --rehacer` o fuente nueva en busquedas.json).
- FALTA: al acabar bajar → `fab.py wow_oro_forever medios` (mirar TODAS las hojas: webcams, caras, rótulos de otro canal, portugués EoOuPZKl_Rs; `find medios -size -20k`) → rehacer malos → `python _promesas.py` (mirar previews/promesas_NN.jpg) → `_peg_check.py` adaptado (pegatinas_check) → `fab.py wow_oro_forever chequeo` → `FAB_FX_FINAL=1 python fab.py wow_oro_forever fx hoja` (mirar todas las fx_NN.jpg) → `fx` → `mezcla` → `video` → `final` → `tele video wow_oro_forever master` (2.º plano) → verificar → miniatura Flow → youtube.json (SIN Overgear, capítulos) → `yt subir wow_oro_forever cronicas_warcraft private --publicar 2026-11-20T15:00:00Z` → publicados + BITACORA + `canales --actualizar` → commit + push (con nucleo/mg_oro.py) → `biblioteca`/docs (mg_oro en estilo_secuencia_yt.md).
- ✅ bajar 203/205 (16 reintentados) · subagente revisando hojas `medios` y rehaciendo (177 y 187 sin fuente) → `_rehacer.txt`.
- ✅ medios revisados (62 rehechos, `_rehacer.txt`; FIJO en _busquedas.py).
- chequeo: densidad baja (mg 0,7 vs 1,1; pegatinas 1,2 vs 1,9) → `_fx_extra.txt` (7 MG + 19 pegatinas) LISTO PARA AÑADIR a efectos.py cuando acabe el subagente de revisión visual (está editando efectos.py) y volver a mirar fx hoja. Avisos de sonido (scene-068 «Suena absurdo», scene-167 «la voz de siempre») = falsos positivos.
- ✅ revisión visual 1 (subagente): promesas 58 OK tras arreglos, pegatinas OK, fx hoja arreglada (bandas con `pantallas/banda_*.jpg`). Añadido `_fx_extra.txt` → efectos.py (111 efectos, seco OK). Subagente 2 LANZADO: rehace clips 6:13/7:05/15:37/20:41/8:20 + texto quemado 069/090/201, y revisa en fx hoja los 28 efectos nuevos. Pendiente kit: la «lupa» de peg_anim tapa caras a ratos (no tocado).
- ✅ subagente 2: 12 clips rehechos (FIJO), efectos ajustados (100 FX), scene-099 → YFyyslnV8gw@120 (revisado). LANZADO fx → mezcla → video → final (`_render.log`).
- ✅ youtube.json (SIN Overgear, 32 capítulos) · miniatura Flow LANZADA (subagente → salida/miniatura.jpg + prompt_miniatura.md) · render corriendo.
- ⚠ miniatura Flow: Flow rechazó con «actividad inusual» (filtro anti-bots; NO se salta). Proyecto con ingredientes ya pegados: https://flow.google.com/project/e981dbe2-5221-41a4-97d5-d1c90730579d · receta en prompt_miniatura.md. Reintentar más tarde (o el usuario a mano) y aplicar con `yt aplicar` antes del 20-nov; mientras, miniatura de código de respaldo.
- ⚠ 1.er intento: `fx` ✅ pero `mezcla` cayó por RAM (ArrayMemoryError 645 MiB); RELANZADO mezcla → video → final (`_render2.log`).
- `nucleo/sinte.py` compresor optimizado (float32 en el sitio) por el fallo de RAM de la mezcla (commit libre 10 GB) → RELANZADO `_render3.log`.
- mezcla seguía cayendo en el limitador (commit total 55,9 GB, libres 10; ~45 GB comprometidos fuera de los procesos visibles) → `nucleo/mezcla.py`: pistas a float32 y soltar golpes/fx/fxv antes del compresor. RELANZADO `_render4.log`. (Cambios de núcleo: sinte.compresor y mezcla.py → incluir en el commit.)
- ✅ MASTER 29:22 1080p (-14,1 LUFS, -1,39 dBTP) + .srt · verificar ✅ (nucleo/verificar.py lee en float32) · final_hoja mirada · tele: falló la conexión (ConnectionReset; tele apagada?) · miniatura PROVISIONAL = cuadro de la banda (salida/miniatura.jpg; la de Flow pendiente) · `yt subir … private --publicar 2026-11-20T15:00:00Z` LANZADO (`_subir.log`).
