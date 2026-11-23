# mpm_takis — «Así se FABRICAN los TAKIS por dentro» (Mil por Minuto, 1.er video del canal)

- **Canal:** Mil por Minuto (`mil_por_minuto`), fórmula `canales/formula/mil_por_minuto.md`.
- **Motor:** SECUENCIA YT (`docs/estilo_secuencia_yt.md`) + kit propio `nucleo/mg_planta.py` (creado 19-nov-2026).
- **Voz:** Brian C (ElevenLabs `Czw3Dn181ypdrCOnPfif`, eleven_v4_turbo), sin filtro. **Música:** Lyria (no es canal de juegos).
- **Duración objetivo:** ~15 min (fórmula 15-18; primer video: retención antes que largo).
- **Tema elegido por Claude (19-nov):** Takis = n.º 1 de la fórmula (mexicano, Barcel/Grupo Bimbo; ref. JPaniagua Docs ×6,8).

## Etapa
**PUBLICADO (22-nov-2026 ~13:45 CDMX): https://youtu.be/KwjDkJf79ME público.** Canal verificado por el usuario; miniatura `salida/miniatura.jpg` = mini_v2_2 ($1,100 MILLONES; elegida por el usuario el 22-nov ~18:25), título «Así se FABRICAN los Takis: un negocio de 1,100 millones» (55 c.); alternativa para A/B: «Cómo se HACEN los Takis dentro de la fábrica» + mini_v2_1 (río). SIGUE: métricas a 48 h y 7 días (`fab.py yt metricas mil_por_minuto`) y el 2.º video del canal (~26-nov).
Antes: **MASTER LISTO (19-nov-2026 23:32): `salida/mpm_takis_MASTER.mp4` (14:12, 1080p, −14.4 LUFS) + `.srt` + `salida/miniatura.jpg` (Flow) + `youtube.json`. FALTA SOLO SUBIR: el canal no tiene token de YouTube → el usuario corre `python fab.py yt conectar` con la cuenta de Mil por Minuto y luego `python fab.py yt subir mpm_takis mil_por_minuto private --publicar 2026-11-22T00:37:00Z` (sáb 21-nov 18:37 CDMX, hora del canal).**
Voz cerrada (89/89, 13:27 de voz, video 851.7 s = 14:12; idioma OK). `tiempo` + `beats` hechos (114 beats). busquedas.json escrito
con `_escribir_busquedas.py` (mayoría {url, desde} de metraje.md; FZRdk5QV1fg es 480p: si `bajar` lo rechaza por < 720p, ver
docs/estilo_secuencia_yt.md § METRAJE DE ARCHIVO < 720p). Corte de contexto de la sesión 1 aquí (19-nov ~17:40).

## En curso (siguiente, en orden)
0f. HECHO (19-nov 23:50): `video` (17 min) → `mezcla` (−14.38 LUFS, voz +13.8 dB) → `final` → `verificar` (CER 0.017; las 2 frases con CER alto se oyen bien con Whisper small; las demás = «taquis»/«Cerviche»/«Couple» de Whisper) · regla 10: el guion no manda escuchar nada · `avisar` hecho · miniatura Flow (`salida/_mini/flow_3.png`; flow_thumb.py NO detectó las imágenes del Flow nuevo en flow.google.com: se bajaron de la página) · `youtube.json` (título 55 c. validado, capítulos, fuentes). SUBIDA BLOQUEADA: sin token del canal (ver Etapa).
0e. (19-nov ~23:40) Lyria API = HTTP 402 SIN SALDO → música de la BIBLIOTECA por tramo (cohete_crs30 t1, historia_aguascalientes t3, doce_animales t8, guia_ieez_50 t3, lol_worlds_2026 t9, satoshi_nakamoto t2, cinco_bichos t4 desde 48) → audio/musica.wav armado. `musica_biblioteca._tl` también entiende `cortes`. `chequeo` OK (no bloquea). `fx` hecho (audio/fx.wav). `video` LANZADO ~23:40 (log _video.log). SIGUE: `mezcla` → `final` → `verificar` + citas → avisar → subir + miniatura Flow.
0d. HECHO (19-nov ~23:20, sesión 2, mismo hilo: la app no dejó abrir el relevo por Remote Control): arreglos a–e APLICADOS (sin «→», sin patente_texto, etiquetas movidas, Nielsen = etiqueta, sin pegatina Lorenzo en 110; clips 047=HIM@176 caen al aceite, 049=HIM@186 burbujas, 053=Shoplogix@199 recortado, 008 recortado). Hoja fx 01-09 REVISADA. `fx` lanzado (SFX + audio/fx.wav). promesas.md + previews/promesas_01.jpg HECHOS. Música: LYRIA con `tramos` (7) y `cortes={"proceso": [342.9]}` (opción NUEVA en nucleo/lyria_tramos.py para partir escenas > 175 s) → `fab.py mpm_takis musica` lanzado ~23:15 (log _musica.log). `chequeo` lanzado en segundo plano (log _chequeo.log; tarda > 8 min).
   SIGUE: leer _chequeo.log y _musica.log → `video` (render; nunca a la vez que otro render) → `mezcla` → `final` → `verificar` (regla 10: citas de audio) → `avisar` → `yt subir` (si no hay API, MASTER listo y decirlo) + miniatura Flow → «## Sesiones
- 22-nov-2026 (6): el usuario eligió la miniatura 2 → `salida/miniatura.jpg` = mini_v2_2 ($1,100 MILLONES) + título «Así se FABRICAN los Takis: un negocio de 1,100 millones» aplicados con `yt aplicar` (público). La 1 (río) queda para A/B. ✅
- 22-nov-2026 (5): canal verificado → miniatura mini_v2_1 + título nuevo aplicados (`yt aplicar`) y video PÚBLICO (`yt publicar … public`); registrado en canales/mil_por_minuto.json y BITACORA. ✅
- 20-nov-2026 (4): 5 MINIATURAS NUEVAS en Flow (investigación + prompts en `prompts_miniaturas_v2.md`): `salida/mini_v2_1..5.jpg` (río sin texto · $1,100 MILLONES · VS Doritos · ASÍ LOS ENROLLAN · ¿QUÉ ES ESTE POLVO?) con su título cada una; hoja `salida/miniaturas_v2_comparar.jpg`. ESPERA a que el usuario elija → copiar a `salida/miniatura.jpg` + título en `youtube.json`; se aplica al verificar el canal. Lección: flow_thumb.py ya no sirve (Flow = flow.google.com, perfil 9222 sin sesión): Chrome del usuario + Ctrl+V + fetch de los <img> a un receptor local (127.0.0.1:8799).
- 20-nov-2026 (3): SUBIDO KwjDkJf79ME (privado; DESPROGRAMADO a pedido del usuario: sin fecha hasta verificar el canal) + .srt + banner/idioma del canal. Miniatura `salida/miniatura.jpg` NO aplicada (canal sin verificar: HTTP 403). Al verificar: `python fab.py yt aplicar mpm_takis mil_por_minuto KwjDkJf79ME`.» y commit.
0c. HECHO (19-nov ~22:45, sesión 2): efectos.py ESCRITO (171 efectos: contador $ de esquina con `prefijo` nuevo en mg_planta.contador_produccion, plano + tarjeta en las 10 estaciones con `est()`, cifras, trivia pregunta/respuesta, 2 mapas + 2 ventanas, pantallas de patente/registro/Houston, pegatinas pv(), versus, etiquetas de mitos, placas «EQUIPO DE REFERENCIA» (_REF, automáticas por fuentes.json) y «PLANTA REAL DE BARCEL» (_REAL), SFX golpe_metal/maquina/freidora/caja/sello SIN generar aún). `fx --seco` OK, huecos > 4 s cerrados. `FAB_FX_FINAL=1 fx hoja` hecha (previews/fx_01..09); REVISADAS fx_01..06, FALTAN 07-09.
   ARREGLOS PENDIENTES de la hoja (hacer ANTES de `chequeo`):
   a) «→» no existe en Bahnschrift (sale «0»): cambiar «TAQUIS → TAKIS» por «DE TAQUIS A TAKIS», la cuenta «LA SALIDA» por «BOLSAS A CAJAS / CAJAS A TARIMAS / TARIMAS A LA RED DE BIMBO» y el porqué de est(10) por «Bolsas, cajas, tarimas y camiones».
   b) Quitar `pant("patente_texto", …)` (página de texto ilegible; el clip de Casa Herrera ya enseña la banda que separa).
   c) Etiquetas que chocan con texto del clip: «SOLO EN EE.UU.» (002) → y=.72 · «¿QUIÉN LOS HACE?» (010) → x=.62 y=.84 · «EL ARMA SECRETA» (063) → y=.80 · «EL NEGOCIO» (067) → y=.82.
   d) Clips: 047 (2-ed6djsAWk@71) termina en la placa «HEAT AND CONTROL / Convey» → `bajar 47 --url …2-ed6djsAWk --desde 64`; 053 (BHXtF1s_2x0) trae subtítulos en inglés → recortar como 045 (`crop=1536:864:192:0,scale=1920:1080`, respaldo en medios/_respaldo); 008 (mLUO_Zq3HeI, AMX) trae cintillo/QR/logo de TV → recortar arriba-izquierda (p. ej. crop=1350:760:0:0) y mirar.
   e) Mirar fx_07..09 (negocio desde 071, mitos, mapas 101-105, cierre). Luego `fx` (genera 5 SFX, ElevenLabs) y sigue el paso 3.
0b. HECHO (19-nov ~22:30, sesión 2): clips CERRADOS. Rehechos 048 (HIM aceite@200) 049 (HIM freidora@182) 058 (embolsado@272 + pegatina corte_manhattan) 061 (archivo@49.5) 063 (QWWc1kq0LmI@71 camión Bimbo) 065 (VZ_tD2kYGrc@5) 075 (rpQGaWkeG8U lockers) 100 (ZEKHR6jB2d0 Londres; el anterior traía subtítulo de nota policiaca). OJO: CAMARA de efectos.py SOLO actúa sobre imágenes, no sobre clips → 019 (bumerán del plato), 030, 045 y 106 recortados con ffmpeg EN EL ARCHIVO (originales en medios/_respaldo/*_orig_crop.mp4). texto_clips corrido: lo que queda es empaque/anuncio/cintillo de noticia (aceptado) y 101/104 tapados por mapa.
0. HECHO (19-nov ~18:10): `bajar` 114/114 (15 clips < 720p armados como VENTANA DE ARCHIVO con `_archivo.py`, marco naranja) y
   hojas `medios_01..06` REVISADAS. Rehacer (comandos en `_rehacer1.sh`): 019 tacos dorados · 034 (texto «Consumo de gas») ·
   047/048/049 freidora (049 texto «TWO-STAGE…») · 058 (logos Reuters/TDG) · 061 (rueda de prensa en vez de cajas) · 063 (subtítulos
   en inglés) · 065 y 106 (youtubers JOLLY) · 075 (sketch de TV) · 079 (trigo) · 086 (texto del anuncio) · 108 (rótulo «Comercial 2015»)
   · 109 (texto «Patented Odyssey Ovens»). CAMARA (recorte con zoom) en 030 (logo Tortilladoras Lenin) y 045 (subtítulos Shoplogix).
   Aceptados: noticias con cintillo (cita de noticia), anuncios con «COME BIEN», logos chicos de Heat and Control/Casa Herrera
   (llevarán rótulo EQUIPO DE REFERENCIA), 101/104 tapados por el mapa. OJO: signo de cx/cy de CAMARA 030/045 sin comprobar.
   `_rehacer1.sh` corrido (~18:20): 12 ok. PENDIENTE: 061 falló (ffmpeg; probar otro --desde u otra fuente de camiones/cajas) ·
   048 y 063 quedaron con la MISMA fuente (busquedas.json tiene {url} fijo: cambiar la entrada o usar --url distinto) · mirar en un
   mosaico los rehechos 019 034 049 058 (Thrasher, skate) 065 075 («Locker Rooms Be Like» = sketch: probable fuera) 106.
1. `python fab.py mpm_takis bajar -j 4` → `medios` (mirar hojas) → `python nucleo/texto_clips.py mpm_takis -j 4` (las noticias
   traen cintillo: son cita de noticia; BHXtF1s_2x0 trae subtítulos en inglés quemados → CAMARA con zoom que recorte abajo o rehacer).
   Rehacer con `bajar N --rehacer` / `--q` / `--url --desde` lo que no enseñe lo que dice la voz (regla de oro 2).
2. efectos.py: contador de esquina `mg(P.contador_produccion(34.88, "USD", "VENDIDOS EN EE.UU. DESDE QUE EMPEZÓ ESTE VIDEO",
   nota="1,100 M USD/año ÷ segundos del año · Circana 2024"), 0, ("fin"…), x=.86, y=.09)` (ojo: el formato debe mostrar $),
   `plano(k, de, a)` en cada «Estación N» (10), `P.estacion`, `P.cifra` (1,100 M; 400 M → 1,100 M; 3,900/1,600; 2,000 M),
   `P.cuenta`, `P.etiqueta` («REVISADAS» no; usar «EQUIPO DE REFERENCIA» sobre Casa Herrera/Heat and Control/How It's Made,
   «ARE YOU TAKIS ENOUGH?» escrito en negocio_8), `P.trivia` (A Rojo 40 · B pimentón y cúrcuma · C betabel; correcta=1 solo en el
   cierre), `P.ingredientes` (US, resalta Rojo 40/Amarillo 6), `P.sellos` (EXCESO CALORÍAS, EXCESO SODIO) si cabe con la voz,
   `P.barras` (Doritos 3.9 / Tostitos 1.6 / Takis 1.1 mil M USD), `P.linea_tiempo` (1999 Takis · 2001 TAQUIS · 2006 Fuego/EE.UU. ·
   2011 Mexicali · 2012 Coppell · 2024 1,100 M), pantallas patente_fig1/portada (beats 41-47), registro TAQUIS (21-22), Houston
   Press (74-75), Rotherham (105); mapas con `_mapa_base.ll()` (norteamerica: Lerma, Hermosillo, Mexicali, Guadalajara, Coppell;
   atlantico: Rotherham), pegatinas pv() de cada nombre (Servitje ×2, Bimbo, Barcel, Sabritas, PepsiCo, Nielsen, Doritos Dinamita,
   Tostitos, Flamin' Hot, Paqui, bolsas Takis). Pantalla con bolsa MX con sellos al decir «En la de México, además, Amarillo 5».
3. `fx --seco` (huecos > 4 s) → `FAB_FX_FINAL=1 python fab.py mpm_takis fx hoja` (mirar todas) → promesas.md → `chequeo` →
   `video` → `biblioteca sugerir` / Lyria + SFX de máquinas → `mezcla` → `final` → `verificar` → avisar → `yt subir` (canal sin API
   conectada todavía: si falla, dejar el MASTER listo y decirlo). Miniatura en Flow (producto + máquina + palabra en MAYÚSCULAS).

## Hecho
- `investigacion.md` (datos con fuente; NC = no decir como hecho) · `metraje.md` (clips reales: FZRdk5QV1fg Bimbo Mexicali = único
  metraje limpio de la línea Takis; Casa Herrera y Heat and Control para el proceso, con rótulo «EQUIPO DE REFERENCIA»).
- guion.py (2,026 palabras, ~14 min). Contador de esquina = dólares de Takis vendidos en EE.UU. desde que empezó el video
  (1,100 M USD/año ÷ 31,536,000 s = 34.88 USD/s, Circana abr-2024). Ajustar la cifra de la frase del cierre a la duración real.
- pegatinas/ (31, `_creditos.md`, hoja `previews/pegatinas_check.jpg` revisada) · pantallas/ (patente fig1 + portada, registro TAQUIS
  USPTO, Houston Press 2013 (archive.org), Rotherham aérea, Bimbo 1945 ilustración). Faltan: rollitos Fuego sueltos, cal, fotos de
  plantas Coppell/Mexicali/Lerma (usar cuadros del clip FZRdk5QV1fg para Mexicali).
- Bolsa MX: sellos EXCESO CALORÍAS + EXCESO SODIO (no hay de grasas).
- mapas/norteamerica.jpg y atlantico.jpg (Natural Earth, Mercator; `_mapa_base.ll(slug, lat, lon)` da x, y). Coordenadas (fuente):
  Lerma 19.28986,-99.51236 · Hermosillo 29.075,-110.95833 · Mexicali 32.636,-115.4759 · Guadalajara 20.67639,-103.34222 ·
  Coppell 32.96306,-96.99722 · Rotherham/Swinton 53.4877,-1.3149 · CDMX Santa Fe 19.37295,-99.26184.
- efectos.py adaptado (tema planta, `mg()`, `plano()`, ESTACIONES de 10).

## Siguiente
guion.py (estructura de la fórmula) → `voz` → `seleccionar` → `python nucleo/idioma_voz.py mpm_takis` → `tiempo` → `beats` →
`busquedas` → `bajar -j 4` → `medios` (mirar hojas) → `texto_clips` → pegatinas/pantallas/mapa → efectos.py → `fx --seco` →
`FAB_FX_FINAL=1 fx hoja` → promesas.md → `chequeo` → `video` → música Lyria + SFX → `mezcla`/`final` → `verificar` → avisar → subir.

## Sesiones
- 19-nov-2026 (1): video creado, kit `nucleo/mg_planta.py` (contador de producción, plano de línea, estación, cifra, cuenta,
  etiqueta, trivia, sellos NOM-051, barras, ingredientes, línea de tiempo) probado en hojas. ◐ parcial: investigación, guion, voz (2,690 créditos en total), pegatinas, mapas,
  tiempo, beats y búsquedas; corte de contexto antes de `bajar`.
- 19-nov-2026 (2): ✔ MASTER — clips cerrados (rehechos + recortes ffmpeg), efectos.py (169 efectos), hoja fx revisada, promesas, chequeo, música de la biblioteca (Lyria API sin saldo), render, mezcla, final, verificar, miniatura Flow y youtube.json. Falta subir (canal sin token). Lecciones: CAMARA no mueve clips de video; «→» no existe en Bahnschrift; `cortes` en LYRIA para escenas > 175 s.
