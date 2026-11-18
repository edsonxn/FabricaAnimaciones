# Top 25 refugios más malvados y raros de Fallout — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: radio_yermo (2.º video) · hueco sáb 21-nov-2026 09:15 CDMX (horario = el de Tamriel desde hoy: 3 d, 09:15)
- estilo: secuencia_yt (receta de Tamriel; regla de oro `videos/tes_secretos_40/`) · kit `nucleo/mg_fo.py` · voz el Profeta + filtro radio modo B (`VOZ_FX`, como `videos/fo_nunca_f4/guion.py`) · OST oficial de cada juego → doc: docs/estilo_secuencia_yt.md § Radio Yermo
- etapa: SUBIDO XU_OkLlxV7o (programado dom 22-nov 09:15 CDMX) = reemplazo con las 13 ESCENAS IMPORTANTES con su clip real (`escenas.md`, `previews/escenas_01/02.jpg`). El viejo iyLkHK3mpoI BORRADO de YouTube (OK del usuario, 18-nov).
- siguiente: nada pendiente; `fab.py fo_refugios_25 limpiar` cuando él apruebe el video.

## Sesiones («continúa el video fo_refugios_25» retoma aquí · protocolo docs/sesiones.md)
- alias: top 25 refugios, refugios malvados de Fallout · UNA sesión directo al MASTER (relevos por corte de 180k)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación, guion, voz (lanzada), Flow abierto | ◐ 17-nov parcial | corte por contexto 180k; relevo en sesión nueva |
| 2 | resto hasta MASTER subido y programado | ✅ 18-nov | render, subida, título cambiado por la regla nueva |
| 3 | escenas importantes con clip real (pedido del usuario 18-nov) | ✅ 18-nov | 13/13 con clip real (ninguno de Flow); video completo re-renderizado, final, resubido XU_OkLlxV7o |

## Decisiones (17-nov-2026, pedido del usuario)
- Top 25 «refugios más malvados / hardcore / raros» de Fallout, ≥ 30 min, el n.º 1 = el PEOR refugio (el más malvado), lore oficial.
- Gameplay real donde exista; lo que no tenga imagen ni video → RECREACIÓN en Flow con gráficos de Fallout 3/4 (rótulo «RECREACIÓN»), regla 5-nov.
- Misma voz y filtro de radio que `fo_nunca_f4`. Clips solo del juego que se nombra (regla 3). OST: del juego de cada refugio.
- Comentarios: 0 (el 1.er video sale el 18-nov) → sin agradecimientos ni críticas. Suscripción: se pide sin cifra.

## En curso
- 18-nov ~12:40 (corte por contexto) · ARREGLO DE ESCENAS IMPORTANTES (pedido del usuario: «cuando hables de algo interesante de ver, busca ese clip; última opción Flow video 4-6 s en 360p y reescalar»). Hecho: regla escrita (docs/estilo_secuencia_yt.md § «LAS ESCENAS IMPORTANTES SE VEN», CLAUDE.md, memoria); auditoría → `escenas.md` (13 beats; 10 con clip real localizado y comprobado con cuadros: url@seg en la tabla). Falta, en orden: (1) buscar 058 Jonas (4td2SqKyxmI 3700-4100), 118 cerebro (YPrEhhTmwjk 2400-2560), 166 cápsulas momificadas (3ZyBc6UfuVg); Flow video 4-6 s 360p → «720p mejorada» solo si no hay clip; (2) `python fab.py fo_refugios_25 bajar <N> --rehacer --url <url> --desde <s>` por beat; mirar un cuadro de cada medio; (3) `video --rehacer t0-t1` de cada tramo (tiempos en beats.json) → `final` → `verificar` (con ≥ 3 GB de RAM libres); (4) subir el MASTER nuevo `yt subir fo_refugios_25 radio_yermo private --publicar 2026-11-22T15:15:00Z` (FAB: el registro actual de iyLkHK3mpoI en canales/radio_yermo.json choca con la separación: quitarle la programación antes o usar `--forzar` solo para ese reemplazo) y pedirle al usuario el OK para BORRAR iyLkHK3mpoI; actualizar publicados/BITACORA; commit.
- 18-nov ~13:10 (sesión de relevo) · MEDIOS NUEVOS PUESTOS: 12 de 13 beats de `escenas.md` en `medios/` y mirados (`previews/escenas_medios.jpg`); 058 cortado a mano (keyframe desplazado), 117/118 a mano (Tactics solo 480p 4:3: relleno difuminado; 118 con acercamiento), 166 = PZlv9_eJfI8@1036 (inglés). scene-006 se pisó por error y se RESTAURÓ (respaldo + fuentes). Falta el 067: 7Ijy7vBzxzY era una mantis → buscando portador de esporas en 63NqNwe1H8Y. Luego: `video` COMPLETO (aquí `--rehacer` no sirve) → `final` → `verificar` → hoja de escenas → `yt publicar radio_yermo iyLkHK3mpoI private` (quitarle la programación) → `yt subir … --publicar 2026-11-22T15:15:00Z` → pedir OK para borrar iyLkHK3mpoI.
- LISTA (cuenta atrás): 25 R55+56 · 24 R21 · 23 R118 · 22 R43 · 21 R88 · 20 R101 · 19 R22 · 18 R106 · 17 R63 · 16 R81 · 15 R108 (Gary, post) · 14 R0 · 13 R77 · 12 R94 · 11 R68+69 · 10 R95 · 9 R111 · 8 R12 · 7 R92 (ruido blanco, post) · 6 R87 · subs · 5 R96 · 4 R51 · 3 R11 (4 disparos, post) · 2 R75 · 1 R112. Hilo Braun (88 → 75 → 112).
- Agentes en marcha (17-nov tarde): mapas (`mapas/`), pegatinas (`_pegatinas.py`, `pegatinas/_lista.md`), OST (`_bajar_ost.py`, `audio/ost/_ids.json`).
- Investigación en `_investigacion_A.md` (FO3/FNV), `_B.md` (FO4/FO76), `_C.md` (clásicos y lore); mapas en `mapas/` (`_coords.json`, hojas `previews/_coords_check_*.jpg`).

## Checkpoint 17-nov ~21:30 (corte de la sesión 1)
- HECHO: horario Radio Yermo = Tamriel (3 d, 09:15; json, BITACORA, fórmula, memoria). `nuevo --yt`, candado, `canales --actualizar` (hueco sáb 21-nov 09:15 CDMX).
- HECHO: `guion.py` (25 puestos, 5 089 palabras, VOZ_FX radio en saludo/remates/subs/cierre; `post` en p15a «Gary», p7a ruido blanco, p3a cuatro disparos → en `beats` poner `ambiente_por` del clip de Gary (audio «Gary») y SFX de ruido blanco y 4 disparos de FNV en esos huecos).
- VOZ lanzada ~21:05 en segundo plano (`python fab.py fo_refugios_25 voz > _voz.log`, cuenta 4 de ElevenLabs con 115 k créditos). Al terminar (232 frases; `FIN` al final del log): `seleccionar` → `python nucleo/idioma_voz.py fo_refugios_25` → `tiempo` → oír/Whisper «GECK», «ZAX», «Vault-Tec», «Mister House» (FONETICA solo si suena mal).
- AGENTES lanzados desde la sesión 1 (escriben a disco; la sesión 2 NO recibe su aviso: comprobar que existan): mapas → `mapas/<juego>.png` + `mapas/_coords.json` + `previews/_coords_check_<juego>.jpg` (MIRARLAS); pegatinas → `pegatinas/*.png`, `pegatinas/_lista.md`, `previews/pegatinas_check*.jpg` (MIRARLAS: identidad); OST → `audio/ost/*.wav` + `audio/ost/_ids.json` (FO3/FNV/FO76/FO1/Tactics + las 16 de FO4). Si algo falta a medias, rehacerlo.
- FLOW: proyecto abierto en Chrome «nov 17 - 21:25» (flow.google.com/project/3c6fdbb6-f116-40be-9949-8cdba353f7fc), Nano Banana 2.1, 16:9, x4, 0 puntos. Ingredientes = fetch de static.wikia.nocookie.net (CORS abierto) → canvas → File → `ClipboardEvent('paste')` en `.ProseMirror` (un ingrediente por llamada); texto con `execCommand('insertText')` y Return real. Se pegó ya el atrio del V81 (para r55_pared). Lista de 13 recreaciones en `flow_prompts.md` → `pantallas/<slug>.jpg` (rótulo «RECREACIÓN»). Descarga: URL firmada `flow-content.google/image/…` de la respuesta `batchexecute` (rpcids=ogiZ0b) con curl. Luego la miniatura (Flow, que parezca el juego, texto escrito por Nano Banana).
- Clips: IDs con segundos en las fichas «YouTube» de `_investigacion_A/B/C.md` (Star Marshal 4K sin comentario: 112 `gK4AlHIDd3A` 30:58/42:44, 92 `QHzbAZR1oU8`, 106 `6-j7LGWoeys`, 101 `4td2SqKyxmI`; Gary `q-U95qZzk9U`; 11 `Xa8Pq3k-BgU`; evitar `kumbpNWUGXk`, `zP0Fr8P2FmQ`, `LCeo6ZWUneE`). Tras `beats`, poner `url`+`desde` por beat en busquedas y mirar `medios`.

## Checkpoint 17-nov ~22:10 (sigue la sesión 1 tras el corte: la app no dejó abrir el relevo desde un turno automático)
- VOZ HECHA (232 frases, `voz/cands`). `seleccionar` falló 2 veces por CUDA out of memory (otro proceso usaba la GPU: probablemente rembg del agente de pegatinas) → reintentar cuando termine: `python fab.py fo_refugios_25 seleccionar`.
- FLOW HECHO: 13 recreaciones elegidas en `pantallas/` (r55_pared[_b], r56_comico[_b], r43_pantera[_b], r69_hombre[_b], r68_puerta, r77_caja[_b], r77_hormiga, r112_laguna[_b], r112_chalet, r12_puerta[_b], r118_islenos[_b], r95_alijo[_b], r11_cinco[_b]); las 72 en `pantallas/_flow/`, hoja `previews/flow_hoja.jpg`. Viñeta real del cómico del 77: `pantallas/_flow/r77_hormiga_v1..` NO; la viñeta = ingrediente `77_Vault_Boy_puppet.png` de la wiki. Receptor local `%TEMP%/recibe_flow.py` (puerto 8799) para bajar de Flow por POST desde la página. MINIATURA HECHA: `salida/miniatura.jpg` (Braun + tumbonas del 112 + «EL PEOR REFUGIO / TOP 25 FALLOUT», v2 de `pantallas/_flow/mini2_v*`; la versión con Betty la rechazó Flow).
- MAPAS HECHOS (5: commonwealth, la_isla, yermo_capital, mojave [1024 ampliado], apalaches) con 29 refugios en `mapas/_coords.json` por juego (el 21 no: usar `strip_puerta_norte`). PEGATINAS HECHAS: 138 + 26 `_rec` (`pegatinas/_lista.md`; NO usar `r77_puerta` (palabrota); sin imagen: Doc, Katherine, Rubin, Olivette, Baker, Nina → usar recreaciones/otros). OST: agente aún en marcha. `seleccionar` relanzado 21:40 (`_sel.log`).

## Checkpoint 17-nov ~22:50
- VOZ OK: 232/232, `idioma_voz` limpio (7 remates cortos reescritos más largos: p14_6, p16_5, p17_7, p18_2, p25_5, p5_8, p9_8; tomas viejas en `voz/_idioma1/`). CER/TAIL por frase en guion.py (Whisper: Voltec, Brown, Sachs). `tiempo` y `beats` hechos: 2 363,75 s, scene-001..275. OST: 40 pistas en `audio/ost/` (`_ids.json` con tipo); FO1/Tactics son ripeos de fans sin álbum (usar poco).
- OJO GPU: `seleccionar` falló 3 veces por CUDA OOM pasajero (otro proceso); reintentar basta.

## Checkpoint 18-nov ~00:30
- `p3a` post 8,6 s (grabación REAL del Refugio 11 con los 4 disparos: `sfx/r11_grabacion.mp3`, de Ihawkj4pD3c 42,5-51 s) → tiempo/beats rehechos (2 368,75 s). `sfx/ruido_blanco.mp3` (sintetizado) tras «Así sonaba.». «Gary»: scene-108 desde 141,4 de q-U95qZzk9U + `ambiente_por` .85 → tras `bajar`, `bajar scene-108 --rehacer` y comprobar DURACIÓN (bajar trunca clips con audio).
- `_clips.py` → busquedas.json (url+desde por beat, reparto a lo largo de cada video fuente). `bajar -j 4` en marcha (`_bajar.log`, termina con FIN).
- `efectos.py` ESCRITO: 226 FX + 32 SFX, `fx --seco` sin anclas rotas. Mapas por juego con `ref()`/`mapa(juego, …)`.
- FALTA: bajar → medios (MIRAR hojas: mods, facecam, texto de youtuber, HUD de otro juego) → `armar_musica_ost.py` (copiar de fo_nunca_f4; una pista del juego de cada refugio; `_ids.json` tiene tipo) → ambiente → chequeo → `FAB_FX_FINAL=1 fx hoja` (MIRAR todo) → promesas.md → fx → mezcla → video → final → tele master → youtube.json → subir privado `--publicar 2026-11-21T15:15:00Z` → registrar → avisar → commit.

## Checkpoint 18-nov ~01:30
- 275/275 clips; hojas `previews/medios_*.jpg` MIRADAS (14): rehechos 052 (cartel blanco), 102-104 y 257 (negros), 167 (Fallout Shelter), 190/196 (menú de pausa), 215 (botón SUBSCRIBED de youtuber), p8 entero 168-178 (FO1 en RUSO de EX8aqou8YHg → swVjVj1nAuE + Star Marshal). Overrides en `_clips.py` FIJOS. scene-108 con audio «Gary» (9,65 s OK).
- `armar_musica_ost.py` escrito (una pista del juego de cada refugio); `nucleo/ost_canto.py fo_refugios_25` + armar lanzados.

## Checkpoint 18-nov ~02:30
- MÚSICA HECHA: `audio/musica.wav` (2 368,75 s, una pista oficial del juego de cada refugio). CHEQUEO 1: OCR limpio, idioma OK; densidad baja → EXTRA en efectos.py (+31 pegatinas, +2 mapas con ruta: Reuben 51→76, 101→106) → 259 efectos, `fx --seco` OK.
- SIGUIENTE: `FAB_FX_FINAL=1 python fab.py fo_refugios_25 fx hoja` → mirar TODAS las `previews/fx_NN.jpg` → arreglar → promesas.md → `fx` → `ambiente` → `mezcla` → `video` → `final` → `tele video fo_refugios_25 master` → youtube.json → `yt subir fo_refugios_25 radio_yermo private --publicar 2026-11-21T15:15:00Z` → registrar → avisar → commit.

## Checkpoint 18-nov ~09:00
- `fx hoja` FINAL MIRADA (13 hojas): arreglados ancla de la pantera (cogía el intro y tapaba 42-320 s → «Y una pantera viva»), muro de Braun (4.ª foto en «?» → orden de la voz, 4 marcas, destaca=2), clips de la suscripción 201-203 (deslumbre blanco → 4td2SqKyxmI 4720-4790). Mapas recortados en disco (`mapas/_cache/`, `_recorte_disco`: sin eso la hoja se quedaba sin RAM). El «?» en los rótulos de la hoja es solo su fuente; en el video las tildes salen bien.
- `youtube.json` (`_youtube.py`), `promesas.md`, `salida/miniatura.jpg` HECHOS.
- En marcha (~09:00): bajar 201-203 → fx → ambiente → mezcla. Luego: comprobar que no corre otro render → `video` → `final` → `verificar` → `tele video fo_refugios_25 master` → subir.

## Checkpoint 18-nov ~15:00 (cierre de la sesión 3)
- HECHO: 067 = 63NqNwe1H8Y@734.8 (Spore Carrier Brute, corte HD a mano, gamma 1.15; la mantis en `medios/_respaldo/`). `video` completo (2011 s) → `final` → MASTER 1080p 30 fps 39:29, desfase 0 ms; hoja de las 13 escenas sacada del MASTER (`previews/escenas_01.jpg`, `_02.jpg`): todas muestran lo que dice la voz. `verificar`: Whisper sin memoria de GPU 2 veces (CUDA OOM con 1,2 GB usados); la voz y la mezcla no cambiaron, así que el CER del MASTER anterior sigue valiendo; duración y desfase comprobados aparte. `yt publicar radio_yermo iyLkHK3mpoI private` (sin programación) → `yt subir … --publicar 2026-11-22T15:15:00Z` = XU_OkLlxV7o con miniatura y .srt.
- LECCIÓN: `yt-dlp --download-sections` puede empezar en un keyframe anterior (058 salía la taquilla): si el cuadro no cuadra, bajar un tramo más largo en HD y cortar con `-ss` exacto. Tactics solo tiene 480p 4:3: relleno difuminado + acercamiento.

## Falta
- NOTA: `fx` normal se queda sin RAM con 259 efectos (los borradores de Montaje): usar `fx --sin-montaje`.
- [ ] guion · chequeo_yt · voz · seleccionar · idioma_voz · tiempo · beats · busquedas/bajar/medios · pegatinas · Flow (recreaciones + miniatura) · MG · mapas · OST · SFX · chequeo · fx hoja final · promesas · video · final · tele · subir 21-nov 09:15 · registrar · commit


## Lecciones (cierre 18-nov)
- Comprobar la duración del video fuente antes de pedir un tramo: un `desde` pasado del final deja un .mp4 de 261 bytes y `video` falla al final («Faltan 3 medios»).
- `fx --sin-montaje` con > 250 FX; mapas recortados a disco (`_recorte_disco`).
- Título: el primero (72 caracteres, con paréntesis) no le gustó al usuario → regla de títulos (docs/publicacion.md).
- `verificar` necesita ~3 GB de RAM libres (Whisper + audio de 40 min): no lanzarlo mientras otra sesión recorta con 3 procesos.