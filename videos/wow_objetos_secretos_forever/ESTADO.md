# Los OBJETOS SECRETOS de WoW Forever que nadie te explica — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · jue 5-nov-2026 09:00 CDMX (hueco de la campaña Overgear; Forever sale el 4-nov)
- estilo: secuencia_yt (gameplay de YouTube por beat + apoyos + MG + pegatinas + mapas con ruta + Overgear) → doc: docs/estilo_secuencia_yt.md
- etapa: SUBIDO y PROGRAMADO jue 5-nov-2026 09:00 CDMX: https://youtu.be/_XPiWlcNjfE (17:38, promoción pagada marcada)
- siguiente: enlace s.gy de Alice → `yt aplicar`; anuncios + cuestionario de idoneidad en Studio; medir a 7 días

## Sesiones (plan de tramos · «continúa el video objetos secretos» retoma aquí · protocolo docs/sesiones.md)
- alias: objetos secretos, objetos secretos de Forever, el del 5-nov
- vista previa: NO (el usuario, 1-nov): 3 sesiones, solo el MASTER al final
- leer al empezar: este ESTADO.md · docs/estilo_secuencia_yt.md § REGLA DE ORO, § COMENTARIOS (2b y 2c), § MAPAS · copiar de `videos/wow_jugadores_rompieron/` (Overgear con fondo de marca) y `videos/wow_objetos_raros/` (misma fórmula en Vanilla)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz Applio + tiempo | ✅ 1-nov | 15 puestos con fuente; 161 frases; 26 tomas aceptadas por nombres ingleses (CER/TAIL_MAX_POR_FRASE) y 9 reescritas; OST por tramos escrita en LYRIA["tramos"] |
| 2 | beats + búsquedas + bajar clips + pegatinas + mapas + efectos.py + chequeo | ✅ 1-nov | 36 clips rehechos; 9 MG nuevos; 10 mapas |
| 3 | OST + SFX del juego + mezcla + render + final + verificar + miniatura Flow + subir/programar 5-nov | ✅ 1-nov | _XPiWlcNjfE programado con `--forzar` |

## Decisiones del episodio
- tema (el usuario, 1-nov): opción 1 de la conclusión del 1-nov en canales/formula/cronicas_warcraft.md (Kadrath ×4,0 / ×2,3; nuestros 12 objetos raros de Vanilla 6 587 en < 7 d). Una variable: Vanilla → Forever.
- duración total (el usuario, 1-nov): **~18 min** → ~15 puestos (propuesta) · Overgear: campaña 2, coaching Forever + CRONICAS10, **fondo de marca SIEMPRE**, enlace s.gy del 5-nov (pedir a Alice) y promoción pagada
- REGLA DE ORO: todas las capas suman; `fab.py <v> chequeo` antes de renderizar
- Fecha (el usuario, 1-nov, buenos días): **se mantiene jue 5-nov 09:00 CDMX con `--forzar`** aunque quede a 24 h del video del 4-nov (el canal pide 44 h). Terminar completo hasta dejarlo programado.
- Comentarios (1-nov, `yt comentarios`): 15 nuevos. Queja más repetida = voz IA (♥14, ♥4, ♥3) → reportada al usuario, no se cambia sola.
  - **Agradecimientos (≥ 4, repartidos):** @victorsoto2954 `UgxNUEuhQMM7b46ar-t4AaABAg` («casi 20 años después siguen habiendo cosas que descubrir»: encaja con el tema, va en el gancho o el cierre) · @rubenet5 `Ugz84d60LthINJhfjvt4AaABAg` («me ha encantado la temática y la voz») · @josejuanandrade4439 `Ugy28dO2Wp7-M9Wj3ax4AaABAg` («Gracias Tío Crónicas») · @cristianmandiola123 `Ugyw34VhbGJdf7yIB194AaABAg` · reserva @freddypazmino525 `UgyCTRdo285axs4NRa54AaABAg`
  - **Críticas con burla disfrazada: AL MENOS 3 en este video (el usuario, 1-nov; suma sobre el «1-2» del § 2c):** @diegoescobar6957 `UgyLra8yqW9zGb2baQ54AaABAg` («cuando la Ai te hace un video no deja nada bueno, todo el contenido es lo mas errado que puede ser», ♥14) · @fallensovich2780 `UgwFly67BE4afgM2Vy54AaABAg` («contenido ia zzzz») · @TheRealMelkorio `Ugzjp48cJ-IfVZwrBEd4AaABAg` («Asco las voces de IA», ♥4) · reserva @robertodominance547 `UgwxMEHIA3K3wujjxSN4AaABAg` (♥3). Repartidas en pausas (no seguidas). La guasa no puede negar que la voz es IA; se burla del comentario, no de la persona; en pausa natural, nunca en plena revelación.

  - **Dónde va cada uno (guion 1-nov):** gancho (intro_4) = @victorsoto2954 · `gracias1` (tras el 14) = @rubenet5 + @freddypazmino525 · `burla1` (tras el 13, babosa) = @TheRealMelkorio · `burla2` (tras el 11, banana) = @diegoescobar6957 · `gracias2` (antes del 8) = @josejuanandrade4439 + @cristianmandiola123 · `burla3` (tras el 8) = @fallensovich2780 (remata con la Bolsa de dormir del video del 1-nov). Tarjetas: `yt comentario wow_objetos_secretos_forever cronicas_warcraft <id>` → `peg(com_<id>)` 4-6 s.
- Sonido nombrado (regla 31-oct): c14 «las ranas te contestan cantando, y suena así» + `post` 3 s → clip con el canto de las ranas en `ambiente_por`.

## En curso
- 1-nov (corte a 180 mil, sesión de «buenos días»). El usuario pidió terminarlo COMPLETO hasta programarlo; cupo semanal al 91 % a las 10:20 (reinicio mar 3-nov 12:00 CDMX): si llega al 97 %, checkpoint y avisar.
- `bajar -j 4` lanzado ~10:33 con log en `_bajar.log` (79 de 121 clips a las ~10:44; va lento). Si se cortó: `python fab.py wow_objetos_secretos_forever bajar -j 4` retoma los que faltan.
- Hecho: `busquedas.json` (121), `_pegatinas.py` + `pegatinas/` (íconos Forever, renders PNJ de `nucleo/wow_png.py`, 8 `com_*`), `pantallas/` (claro, hyjal, nordrassil, thoradin, sátiro), `mapas/` (reinos_este_eses, azeroth_eses, kalimdor_enus, entranas, ventormenta, poniente), `efectos.py`, y en `nucleo/mg_wow.py` los MG `ocultos`, `chat`, `duplica`, `conjunto`, `reloj_oro`, `subasta`, `pizarra`, `censurado`, `tiempos` (compilan, NUNCA vistos en pantalla).
- 1-nov (siguió en esta sesión: la app no dejó abrir otra desde un aviso): anclas ✅, Overgear y screencast ✅, 36 clips rehechos ✅, ranas reales de `DYx4eMYrsxQ` en scene-015/016/018 con `ambiente_por` ✅, OST de 12 temas ✅, banco `nucleo/datos/sfx_juego/wow/` ✅, hoja y MG revisados ✅. `fx`, `ambiente`, `mezcla` ✅ (-14,09 LUFS; canto medido a -14 dB en 147-149,5 s con la voz callada; scene-018 cortada a mano). `video` + `final` + `verificar` lanzados en cadena (logs `_video.log`, `_final.log`, `_verificar.log`). Miniatura Flow ✅ (`salida/miniatura.jpg`, `prompt_miniatura.md`), `youtube.json` ✅ (con el enlace general de Overgear hasta que llegue el s.gy). Sigue: rigor del MASTER (blackdetect + hoja), subir con `--forzar`, registrar.
- Lista original: (1) `fab.py <v> fx --seco` y arreglar anclas que no casen. (2) Copiar `videos/wow_jugadores_rompieron/medios/_overgear/` a `medios/_overgear/`; `medios/scene-033.mp4` = el recorrido de overgear.com de `wow_jugadores_rompieron/medios/scene-031.mp4` estirado al beat (el brief exige screencast); anotar `_archivo` en busquedas. (3) `medios`: MIRAR hojas, rehacer malos (otro juego, webcams, rótulos). (4) Ranas: buscar clip con el canto real para scene-018 y `ambiente_por` (regla 31-oct); si no existe audio real, reescribir «y suena así». (5) `apoyos` (probar que `wowhead="forever/<id>"` responde), `fx hoja`, `chequeo` y ajustar densidad contra el canal. (6) Tramo 3.
- Decisiones: sin mapa de Zephras ni Riverglades (zonas nuevas sin mapa real descargable; si aparece uno, añadirlo). «Ocarina of Time» se cubre con tarjeta, sin imagen de otro juego. Pegatinas de Hearthstone descartadas (regla de oro 3): `graphed.png` es un goblin genérico; sustituir por cuadro real de Mister Graphed si un clip lo enseña.

## Hecho
- 1-nov: proyecto creado (`nuevo --yt`), canales actualizado (Warcraft BIEN, 4 programados).
- 1-nov: investigación `videos/_investigacion_wow_objetos_secretos_forever.md` (15 puestos, fuentes, nombres es-MX de Wowhead) · guion.py (161 frases) · voz Applio 161/161 válidas (945,9 s) · `tiempo` 1037,5 s · música OST por tramos (16) en guion.py.
- 1-nov: 8 tarjetas de comentario hechas (`yt comentario` → `com_<id>`, listas para `peg`).

## Falta
- [ ] enlace s.gy del 5-nov: lo pide el usuario a Alice; luego `yt aplicar` (por ahora va el enlace general con UTM)
- [x] tramo 2: mapas con ruta donde el guion lo permite (Zephras ranas 51,72; Entrañas canal; canales de Ventormenta; Minas de la Muerte; Riverglades mercado negro; ruta de la llave: Muralla de Thoradin → Entrañas → Roca Negra; ruta del legendario: Hyjal → Claro de la Luna → Un'Goro) con FOTO de cada objeto en su parada; pegatinas = icono/tooltip real de Wowhead de cada objeto; MG nuevos (p. ej. conjunto «Cómplices», contador 12 594 ocultos, tabla del mercado negro, mapa de pistas de la llave)
- [x] tramo 2: c14 post 3 s con el canto real de las ranas (`ambiente_por`)

## Lecciones de este video (solo lo no obvio)
- Un ancla que se repite en el guion fija el efecto en la PRIMERA aparición: el abanico del cierre quedó 16 min en pantalla («Un hacha que mina») y «Número ocho» casó con «antes del número ocho». Usar `#2` o más palabras y mirar `fx hoja` siempre.
- `bajar --url` puede dejar un clip más corto que el beat y el motor lo estira: el canto cayó 3 s tarde, encima de la voz. Tras fijar un sonido, medir `audio/ambiente.wav` y `audio/final.wav` en ese tramo; si hace falta, cortar a mano del video completo.
- `yt subir` solo marca la promoción pagada si la descripción dice PATROCINADO o youtube.json trae `promocion_pagada`. Se detectó tras subir y se corrigió con `yt aplicar`.
- `fps=1/15` + `tile` sobre el MASTER (con la pantalla final anexada) solo entrega la pantalla final: para la hoja de rigor, extraer cuadros con `-ss`.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO jue 5-nov 09:00 CDMX, miniatura Flow y registrado (`canales/cronicas_warcraft.json`, BITACORA)
- [x] HALLAZGOS documentados en manual/estilo
