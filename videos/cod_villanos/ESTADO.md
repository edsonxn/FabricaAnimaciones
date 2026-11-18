# Cómo murió REALMENTE cada villano de Call of Duty — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_cod = «Expediente 141» (5.º largo) · meta: primer hueco tras el MASTER (canal URGENTE: hueco mar 17-nov 16:00, sin video programado)
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + MG `nucleo/mg_cod.py` + mapas + sonido original + OST oficial) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ SUBIDO y PROGRAMADO → https://youtu.be/d89Pw9AT4_o (privado, se publica mié 18-nov 13:00 CDMX = 19:00 UTC) · MASTER 17:31, 1127 MB, verificado (desfase 0 ms, CER 1 %) · miniatura Flow + .srt
- siguiente: medir a 7 días (25-nov) contra Mandela 1 y 2; contestar comentarios con borrador y visto bueno del usuario

## Sesiones (UNA sesión directo al MASTER, regla 5-nov)
- alias: «villanos de cod», «cómo murió cada villano», «cod villanos»
- leer al empezar: este ESTADO.md · plantilla `videos/cod_mandela2/` (guion.py, efectos.py, _escribir_busquedas.py, bajar_pegatinas.py, armar_musica_ost.py) · `canales/formula/cronicas_cod.md`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación → guion → voz (+ pegatinas, comentarios, OST bajada, citas localizadas) | ✅ 17-nov | cortada por contexto (180 mil) en `seleccionar` |
| 2 | seleccionar → idioma → tiempo → beats → busquedas → bajar → efectos → promesas → fx hoja → música → render → MASTER → miniatura → subir | ✅ 17-nov | subido y programado 18-nov 13:00; antes: MASTER 15:19 OK; 10 «--rehacer» para encimados: 7 cayeron por RAM (idioma_voz de otra sesión, 6,7 GB) y `final` pisó el MASTER con un video a medias → render completo |


## Notas de producción (sesión 1 cortada a 180 mil, 17-nov ~13:10)
- HECHO: `investigacion.md` (verificada, wiki CoD + clips MW4 confirmados) · `guion.py` · voz Damián en `voz/cands` (cuentas 2 y 3 de ElevenLabs AGOTADAS, va la 4 con ≈120 mil) · `bajar_pegatinas.py` + `pegatinas/` (≈75, hoja `previews/pegatinas_check.jpg` mirada: OK; «case» rehecha = Case de BO6; sin imagen: kevin_spacey, nikolai, farid, gideon, ethan, dempsey) · `_hoja_peg.py` · capturas de comentarios `pegatinas/com_*.png` (8: thefert, qtdrox, FABIANWOW, leukojb, Prophet9205, Daanw, almidon809, v5x777; H.Hoster YA usado → fuera) · OST en `audio/ost/` (11 pistas, `_catalogo.txt`) · MG nuevos `acta()` y `bajas()` al final de `nucleo/mg_cod.py` (falta hoja de prueba y añadirlos al docstring)
- Selección: CER_MAX_POR_FRASE puesto para 23 frases con nombres (textos revisados uno por uno: solo cambia cómo escribe Whisper los nombres). idioma_voz falló solo en p02_0 (toma vieja; ya regenerada como «El doctor Friedrich Steiner…») → repetir tras `seleccionar`
- CITAS AUDIBLES (post en guion; ambiente_por tras `beats`): Irons «I gave you that arm» 9KLWbfLfcgM@197 · Hassan «…your nation see fire… We're not attacking… invading» wuEQmpxSD88@26-46 · Mason «My name is Viktor Reznov… revenge» (vista de Hudson) RMSiCLsstS0@103-110 · Price «Where is he now? / Off the list» UnCOKMJvpfo@228.5-233.3 · Al-Asad: suena el teléfono, Gt1JeMK50us ~344-354 (mirar) · Menéndez «Martyr me» hIFud6Oeg-Y (128 s, segundo sin localizar) · Dragovich «Tried?» 9BNNOeWhN50 (sin localizar). Script de búsqueda con faster-whisper: `_citas.py` del video (descargar audio + transcribir + grep). CORTAR cada clip ANTES del disparo/golpe
- Clips útiles ya vistos: MW4 Out in the Cold S8Rg5StxRNc / fE_ubVHmKvk, pelea Price-Makarov xe4p8p4s56g, Graves Hired Gun ZZ7ZpkorfSI / yHAwUFuvIN4, Safehouse Gt1JeMK50us, Steiner ambas vistas 7p22Hx9w2l4, Irons 9KLWbfLfcgM, Dragovich 9BNNOeWhN50 (dWnWq1fr7Y8 alternativo; Yo1wQ_pvBgk pide edad)
- Suscritos (yt metricas 28 d): 53 de 8 901 vistas → «solo seis de cada mil» (ya en el guion). Mandela 2: 2 705 vistas, 51 % visto
- Hueco: el de hoy 17-nov 16:00 ya no da; usar el primer hueco de `canales --actualizar` al subir

## Lecciones (17-nov)
- En el motor SECUENCIA `video --rehacer` NO usa segmentos: re-renderiza el video entero (~25 min). Un arreglo = un render completo, no varios «tramos».
- Bucle de etapas en segundo plano: SIEMPRE cortar al primer error (`|| exit`); un `final` tras un `video` fallido pisó el MASTER bueno con un video de 73 s.
- `ambiente_por` va ANTES de `bajar`: si no, los clips de cita bajan sin audio (`bajar N --rehacer` + `ambiente`). Y `bajar` TRUNCA los clips con audio: 012/031/104/115 rehechos con `dl_amb.py` (duración = beat; cola revisada en `previews/citas_cola.jpg`, sin disparos)
- Memoria: Whisper de otra sesión (idioma_voz/tts_select, 6-8 GB) deja sin RAM al render; esperar con `esperar_libre.py` antes de lanzar.

- 17-nov: el usuario quitó la regla de mandar el MASTER a la tele solo (solo si lo pide). Un `ffmpeg` huérfano de otra sesión (0 CPU) dejó `esperar_libre` esperando 3 h: mirar la CPU del proceso, no solo si existe.
- Promesas comprobadas con el timeline sobre el render: 6 mal sincronizadas (silla, helicóptero, Barrett, cascada, cristal, puro) → clips al segundo exacto; render v2 ~18:35 (`_render_v2_log.txt`)

## Decisiones del episodio (17-nov-2026)
- tema: «Cómo murió REALMENTE cada villano de Call of Duty», elegido por el usuario en «buenos días» entre 3. Datos: OVERKILL no scope «Cada villano explicado» ×2,8 y la misma fórmula en GTA ×6,0. Variable cambiada respecto a Mandela: el EJE (de secretos a personajes)
- duración (la decide Claude): ~15 min, lista con cuenta regresiva (Mandela 1 = 14:20 con 35 %; Mandela 2 = 15:27)
- voz: Damián de ElevenLabs (`BPwS5yO6aXvwg8auqNwS`), eleven_v4_turbo; sin corchetes de emoción teatral ([deadpan], [serious], [short pause]); nombres alemanes/rusos con cuidado
- Comentarios (17-nov, `yt comentarios cronicas_cod`, 8 nuevos): críticas para contraburla: @thefert4229 «La voz es IA» (UgxMmZO1yx8ruCS7b_t4AaABAg, ♥2), @qtdrox «todo IA… ni voy a terminar de verlo» (UgxBZqOspRcF59gChr54AaABAg), @FABIANWOW «no me suena ninguno» (UgzNIv3Ae0b4WJKlGNJ4AaABAg). Agradecimientos: @Daanw-k6m (cartel de Standoff), @Prophet9205 (dato del hombre sombra de MW3), @leukojb6772 (Bell / Cold War → puesto de Perseus). Queja justa repetida de @v5x777cod_rdr_fan0 (voz frustrada/forzada) → se corrige con menos emoción, no se contesta con burla
- Violencia: cortar los clips ANTES del impacto (lección de mandela2 puesto 2)

## Falta
- [x] investigación · [x] guion · [x] voz · [x] beats/clips · [x] MG/pegatinas · [x] sonido/mezcla · [x] render · [x] miniatura Flow · [x] subida

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal, miniatura Flow y registrado (`canales/cronicas_cod.json`, BITACORA)
- [x] HALLAZGOS documentados (`docs/estilo_secuencia_yt.md`, `canales/formula/cronicas_cod.md`)
