# Cómo acabó REALMENTE cada protagonista de Call of Duty — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_cod · «Expediente 141», 8.º largo · SUBIDO https://youtu.be/MR77GouPeDo, privado y programado vie 27-nov-2026 13:03 CDMX = 2026-11-27T19:03:00Z (candado de 72 h: mandela_zombies salió 19:02:18)
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + MG `nucleo/mg_cod.py` + sonido original + OST oficial) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ CERRADO 24-nov — MASTER 1080p 16:27 (962 MB) + .srt + miniatura Flow subidos; `verificar` CER 0,74 %, desfase 0 ms; citas oídas en la mezcla final (Whisper)
- siguiente: medir a 7 días (≈ 4-dic) contra «Cómo murió cada villano»; borrar `segmentos/` con `limpiar` si no hay arreglos

## Sesiones (UNA sesión directo al MASTER, regla 5-nov) — «continúa el video cod_protagonistas»
- alias: «protagonistas de cod», «qué pasó con cada protagonista», «cod protagonistas»
- leer al empezar: este ESTADO.md · plantilla `videos/cod_mandela_zombies/` (guion.py, efectos.py, _escribir_busquedas.py, _citas.py, _promesas.py, armar_musica_ost.py) y `videos/cod_villanos/` (acta, bajas) · `canales/formula/cronicas_cod.md`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación → guion → voz → pegatinas → OST → efectos → render → subir | ✅ 24-nov | en paralelo con Runa (Messmer) en otra sesión: UN render a la vez |

## Decisiones del episodio (24-nov-2026; tema elegido por el usuario entre 3 en el «buenos días»)
- tema: «Qué pasó REALMENTE con cada protagonista de Call of Duty». Datos (`yt metricas` 24-nov): «Cómo murió cada villano» ya va en 5 195 vistas en 6 días (2.º del canal, mejor tasa de likes 2,3 %); Mandela 1 11 802, Mandela 2 5 043, Mandela 3 1 849 en 3 d. Referencia: OVERKILL no scope «qué pasó con cada protagonista» ×3,2 (301 mil). Variable cambiada respecto a villanos: villanos → protagonistas (mismo eje personajes, mismo formato).
- duración (Claude): ~15-16 min, cuenta regresiva de 20.
- voz: Damián (`BPwS5yO6aXvwg8auqNwS`), eleven_v4_turbo, PLANA: solo [serious], [deadpan], [short pause]. Sin Turbo (H1): su decisión espera los comentarios ≈ 28-nov.
- Comentarios (24-nov, `yt comentarios cronicas_cod 10`, ninguno usado antes; ids comprobados con grep en videos/cod_*): agradecimientos @TMPLR5 (saga de Ghosts, Ghost vivo, Ugzo4vO15C-dMfGwhM14AaABAg) · @Keengan12239 (Rorke olvidado, UgzSoYq5kEbcJO6x-Sh4AaABAg) · @itsmaibel7486 (Watcher 2 en DMZ, Ugx7rVqdGXavX78a8qJ4AaABAg) · @andreshico1220 (Riley el perro en MW2, UgyOXQ2qm9ubc342COF4AaABAg). Críticas con contraburla: @andreshico1220 «Lo único que rescato» · @HdadDelJubileoensuEsperanza «Y Archer?» (faltó en villanos; The Archer de MW4 muere a manos de Price, Greater Good, tubo roto al cuello → va en el puesto de Price, Ugzlg2I1GWc_pZ9Y_R94AaABAg). @v5x777 «Que se quede el intruso»: solo como voto, en el cierre (la decisión de Turbo sigue pendiente ≈ 28-nov); su «japonés = censura» NO (dudoso).
- REGLA DE ORO: ≥ 5 MG y ≥ 5 pegatinas/min; promesas.md + escenas.md; `chequeo`; `FAB_FX_FINAL=1 fx hoja`; citas con Whisper en la mezcla final; violencia: clip cortado antes del impacto.
- no repetir escenas/clips de `cod_villanos` donde se pueda (otra parte de la misión).

## En curso (checkpoint 24-nov)
- HECHO: investigacion.md (20 + 5) · guion.py (32 escenas, 107 frases, 2 234 palabras; título «Cómo acabó REALMENTE cada protagonista de Call of Duty», 54 car.) · voz Damián (2 719 créditos, cuenta 4, saldo ≈ 64 mil) · pegatinas (121, hoja mirada; allen = nota «WHO IS ALEXEI BORODIN?», sin cara en el juego) · 5 tarjetas com_* · OST 11 pistas nuevas en audio/ost · citas medidas con Whisper medium (`_citas_log.txt`) y recortadas a sfx/s_*.mp3 (−18 LUFS): loose, reznov, soap, bell, gaz, soap23, price; CITAS en `_escribir_busquedas.py` · efectos.py escrito (MG nuevos `C.placa` y `C.servicio` en mg_cod, probados) · mapas/mundo.jpg (Yuri, Price)
- 24-nov tarde: 16:27 (987,5 s), 115 beats; 30 clips rehechos (créditos, webcams de streamers, LIKE/SUBSCRIBE, marcas grandes, negros, violencia); `vid(49)` tapa el disparo de Shepherd; chequeo: MG 6,0/min, pegatinas 6,2/min, fichas 1,5/min; hoja fx 1.ª mirada → 15 arreglos de encimados (`fix_fx.py` en scratchpad, ya aplicado)
- Confirmado MW4 con títulos de clips: Price muere en Greater Good (I-UWtfhJuYs), Archer ejecuta a Gaz (tzhfsgRFMLw), Laswell borra la 141 (4Xpc98CnSZI)

## Falta
- [x] investigación · [x] guion · [x] voz · [x] beats/clips · [x] MG/pegatinas · [x] sonido/mezcla · [x] render · [x] miniatura Flow · [x] subida (canal no monetizado: sin paso de anuncios)

## Lecciones de este video (solo lo no obvio)
- Recorte de citas con ffmpeg: `-ss` DESPUÉS de `-i` + `afade=t=out:st=…` = el fundido corre sobre la línea de tiempo del original y deja el recorte EN SILENCIO (las 7 citas salieron mudas; la regla 10 lo cazó en la mezcla con Whisper). Siempre `ffmpeg -ss A -t D -i entrada …` y medir el pico del recorte antes de `fx`.
- `seleccionar` reutiliza `voz/eval.json` por NOMBRE de archivo: tras regenerar una frase (misma `_s1.wav`) hay que borrar su entrada para que la mida de nuevo; y el rechazo puede ser `tail_ratio` (frase que acaba en voz alta), no el idioma.
- Fuentes que ensucian en CoD: mv7Y5T2oq-Q (webcam), gAN7QecQa9g (marca DALEK + pistola en la cabeza), yq9mHSyJJ5Q (logo PHOENIX), 9SRL__ZJgsg (rótulo SUBSCRIBE al inicio), iF-p-BaQBY4 (logo GAME DETOUR), 1p18qB5xIh0 (GELIPAT GAMING), finales de videos = créditos (VpB_6nTB4qA, P2qgZ-ZUkco, I-UWtfhJuYs > 1000 s). Limpias: Shirrako (lhMs3HBHqsA, fl0DKIJV030), A_mZFP4484k, ovN5k_l_MLA, tzhfsgRFMLw.
- Candado de 72 h: cuenta desde la hora REAL de salida del anterior (19:02:18), no desde la programada redonda → programar al minuto siguiente (19:03).
- 24-nov sesión única: render a las 17:01 tras esperar a Messmer (`_esperar_y_render.py` mira los progreso_render.json de otros videos: GPU compartida sin choques).
