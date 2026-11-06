# Los jefes de Banjo-Tooie, del PEOR al MEJOR — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco jue 26-nov-2026 18:00 CDMX (canales --actualizar del 5-nov; confirmar antes de subir)
- estilo: secuencia_yt (Crónicas del gaming, kit `nucleo/mg_banjo.py`, voz Hope, OST del juego) → doc: docs/estilo_secuencia_yt.md § «Crónicas del gaming» + § REGLA DE ORO
- etapa: SUBIDO privado y programado jue 26-nov-2026 18:00 CDMX (https://youtu.be/yL1D3oGvTJQ), miniatura Flow aplicada
- siguiente: revisión del usuario del MASTER; medir a 7 días (~3-dic); `limpiar` al aprobar

## Sesiones (UNA sesión hasta el MASTER, regla del 5-nov-2026 · «continúa el video bt_jefes_ranking» retoma aquí)
- alias: banjo jefes, jefes de banjo tooie, banjo tooie 25 minutos (el 5.º de Banjo), bt_jefes_ranking
- vista previa: NO (directo al MASTER). Si salta el corte de 180k: checkpoint aquí y sesión nueva sola.
- leer al empezar: este ESTADO, docs/estilo_secuencia_yt.md § Crónicas del gaming (lecciones bt_mundos_ranking, bt_50_secretos) y § REGLA DE ORO; investigacion_jefes.md por grep
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + tiempo + beats + OST | ✅ 5-nov | 3 654 palabras, 169 beats |
| 2 | plan de clips · bajar · medios · brillo · pegatinas · efectos · Flow · promesas · fx · sfx · mezcla · chequeo · video · final · verificar · tele · miniatura Flow · subir · registrar · commit | ✅ 6-nov | MASTER 24:10, yL1D3oGvTJQ |

## En curso (checkpoint 5-nov, relevo a sesión nueva por contexto)
- HECHO: voz · tiempo · beats (169, 24:10) · `efectos.py` (319 FX) · `plan_clips.py` → busquedas.json + ambiente_por/recorte_por en guion.SECUENCIA · `bajar` (169/169) · `dl_amb.py` de los 12 de ambiente (duración exacta) · `medios` (hojas previews/medios_01-09.jpg, sin mirar a mano: el agente verificó 3 cuadros por beat) · `armar_musica_ost.py` (correr OTRA VEZ ahora que hay ambiente_por).
- `medir_brillo.py` HECHO: duraciones bien (ninguno corto); 5 clips con negro → corregir `desde` en plan_clips.py y `bajar N --rehacer`: scene-027 (0-1,2 s), 029 (1,5-2,7 y 5,4-6+), 037 (6,6-7,2), 060 (final 8,4), 085 (casi entero: es el Klungo sin texturas, oscuro → mejor imagen Flow o pant()).
- Dudosos del plan (catalogo_clips.md): 054, 085, 117, 126, 160, 165/166 → muchos se arreglan con la regla nueva de Flow (abajo).
- **REGLA NUEVA (el usuario, 5-nov): lo que no existe se genera en FLOW como captura real del juego** (docs/estilo_secuencia_yt.md § «Lo que no existe: Flow con ingredientes del juego»). En este video, generar en Flow (N64, ingredientes = capturas de Prosafia/Ninbanyan del mismo sitio + renders de pegatinas/) y meter como `pant()`/pegatina con marca «RECREACIÓN» en el momento en que la voz lo nombra: (1) Boss Boulder, la roca jefe de la mina (p09 «Una roca»); (2) Old King Coal formándose con trozos de carbón (p09, opción A); (3) The Kogs, engranajes jefe de la fábrica (intro y p01b); (4) la avispa gigante de Mushroomland (intro y «fuera»); (5) Terry volando bajo el borde del nido (p10, documento de 1999); (6) Mr. Patch con globos teledirigidos (p04); (7) Mingy Jongo con ojos rojos y látigo eléctrico (p03); (8) Mingella y Blobbelda peleando una por una en la torre de Cauldron Keep (p02); (9) el caldero mecánico volador de las hermanas (p02); (10) Weldar's Breath y Targitzan dorado en Banjoland (buscar antes en YouTube de Nuts & Bolts; si no, Flow). Después: `_huecos.py`, `_bordes.py` (ya libera memoria por FX).
- 6-nov: HECHO promesas.md (147 promesas; 121 ya se veían, 18 arregladas; pendientes menores: #77 Klungo sin texturas, #132 huellas de la Hag 1, #114 antorchas, #108 portada del álbum) · fx --sin-montaje · ambiente · sfx · mezcla · chequeo (pegatinas 5,8/min). LANZADO render: `video` + `final` (log video_log.txt). Después: verificar → `tele video bt_jefes_ranking master` → miniatura Flow → yt subir → registrar → commit.
- 6-nov: HECHO Flow (10 `pegatinas/flow_*.jpg` metidas en efectos.py con `recre()` + marca RECREACIÓN; 348 FX) y los 5 clips con negro corregidos (recorte 085 ajustado; música rehecha con ambiente). EN CURSO (agente, 6-nov): `promesas.md` + hojas previews/promesas_NN.jpg + arreglos en efectos.py. Mapas ilustrados de Flow (Terry, Klungo, Hag 1): NO hechos (el reinicio cortó al agente).
- (viejo) EN CURSO (agentes, 5-nov noche): imágenes Flow + mapas ilustrados + `promesas.md` (regla nueva: PROMESAS VISUALES) en efectos.py; arreglo de los 5 clips con negro.
- Falta en orden: Flow (lista de arriba) → efectos.py con esas imágenes → promesas.md + hoja previews/promesas_NN.jpg → brillo → armar_musica_ost.py → fx --sin-montaje → sfx → mezcla → chequeo → video (salida/ y segmentos/ en E:, 63 GB libres) → final → verificar → `tele video bt_jefes_ranking master` (segundo plano) → miniatura Flow → `yt subir bt_jefes_ranking cronicas_gaming private --publicar 2026-11-27T00:00:00Z` (jue 26-nov 18:00 CDMX; confirmar con `canales --actualizar`) → registrar en canales/cronicas_gaming.json (formato `ranking_jefes_secuencia_yt`, prueba «sujeto: jefes en vez de mundos») + fila en canales/formula/cronicas_gaming.md → lecciones al doc → commit.
- Ojo memoria: procesos de otra tarea (Applio, transcripción) llenaron la memoria virtual el 5-nov; si hay MemoryError, esperar, no matarlos.

## Decisiones del episodio (el usuario, 5-nov-2026)
- Pedido: «otro video para Crónicas del gaming de Banjo-Tooie, un top largo de 25 minutos». Elegido entre 3 con datos (jefes / 40 cambios vs Kazooie / transformaciones): **todos los JEFES, del peor al mejor**.
- Variable que cambia respecto a bt_mundos_ranking (ranking de 25 min): SOLO el sujeto (jefes en vez de mundos). Formato a anotar: `ranking_jefes_secuencia_yt`.
- Referencias: Easy Geek «Tier list de todos los JEFES de BANJO TOOIE» (25 k), Super Joe Bros «Boss Fights Tier List» (35 k), «All Bosses» de ProsafiaGaming (2,3 M).
- Comentarios (5-nov): 2 nuevos, 0 quejas, 0 sugerencias. @riuma77 (UgxKny5pWsQET7upHe94AaABAg, 6-nov, Rare: «es una pena que Nintendo se desligara…») = agradecimiento/contexto; @JaVik0 «Y los secretos?» (UgynJhE1FK8jNyNruil4AaABAg, 3-nov, en Majora: el video tenía 12) = crítica para burla disfrazada; además @riuma77 (Ugw_CCIkctKMyqDDO9l4AaABAg, 28-oct) y @antilopezmexicanos (Ugw2j_5-7ktR9uVpcxl4AaABAg, 31-oct). Todos ≤ 10 días al 5-nov (ojo: el del 28-oct caduca el 7-nov; para el render vale la fecha de hoy).
- NO repetir lo contado en banjo_tooie, bt_jiggies_crueles, bt_mundos_ranking y bt_50_secretos (lista «YA USADO» de bt_50_secretos/investigacion_secretos.md).

## Hecho
- `investigacion_jefes.md` (agente, 5-nov): ranking de consenso de 7 listas (10 puestos), fichas con sellos, clips (Prosafia `7RlB7mXcqlU` + Ninbanyan por jefe), OST oficial (títulos Fangamer).
- `guion.py`: 10 puestos + método + gracias (4 comentarios) + crítica JaVik0 + cierre; sonidos nombrados con `post`: p06 (saludo de Klungo, clip), p04 (tema Mr. Patch, SUBE_DB), p03 (tema Mingy, SUBE_DB), p01 (electricidad, clip).
- MG nuevos en `nucleo/mg_banjo.py`: `vida_jefe`, `escalera`, `mira` (probados, previews/_mg_nuevos.jpg).
- Base: mapas/sfx/pegatinas copiados de bt_50_secretos; `audio/ost` = junction a bt_mundos_ranking; `audio/ost_extra` + vs_coal, vs_woo, vs_weldar (Video-Game OST HQ). Pegatinas `com_UgxKny5p…` y `com_UgynJhE1…` hechas.
- `cache360/PROS.mp4` = compilación de jefes de ProsafiaGaming a 360p (para el plan de clips).
- `canales --actualizar` (5-nov): Crónicas del gaming BIEN, 6 programados, sin video desde jue 26-nov 18:00.

## Falta
- [ ] todo lo del tramo 1 y 2

## Cómo retomar (comandos)
```
python fab.py estado bt_jefes_ranking
python fab.py bt_jefes_ranking voz | seleccionar | tiempo | beats
```

## Lecciones (6-nov-2026)
- Corte de contexto a 180k a mitad: con Remote Control la app NO deja abrir la sesión de relevo (ni en turno del usuario). Funcionó repartir lo pesado en agentes (investigación, efectos, plan de clips, negros, Flow, promesas, miniatura) y dejar en el hilo solo los comandos.
- 3 430 palabras de Hope = 22:40 de voz: para 25 min hacen falta ~3 650 (159 palabras/min con pausas y `post`).
- `_bordes.py` con 300+ FX daba MemoryError (cachés de mapas de 4000 px en los cierres): ya suelta `fn` y hace `gc.collect()` por FX.
- Regla nueva del 5-nov en acción: 10 recreaciones Flow (`recre()` en efectos.py, marca «RECREACIÓN · Así pudo verse»); promesas.md con 147 promesas (121 ya se veían, 18 arregladas). Imágenes de otro tema (Caballero Negro, pingüino de dibujos) → ficha de texto, no imagen.
- Pendientes menores no bloqueantes: Klungo sin texturas (#77) solo como escena real aclarada; huellas de la Hag 1 en paredes (#132) sin imagen; tele cortó la conexión al mandar el MASTER (aviso por `avisar`).
