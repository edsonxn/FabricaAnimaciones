# Plan de cámara para toma.py (robotaller_n64) — copiar la estructura de videos/robotaller_mes1/toma.py

Copiar `videos/robotaller_mes1/toma.py`; quitar LLAVES_JS y las poses del piloto; `FIN_VOZ` = fin de `junta_2`; Jefe = `guion.JEFE`
(gancho_1, relevo_2, miniatura_2) con `m.jefe(...)` y `propios/jefe_limpio.png` (ya copiado). Token de streamer igual que el piloto.
`A(ini, clip, z0, c0, z1, c1, desde, vel, tr)`; nunca dos transiciones iguales seguidas (`m.revisar()`); nada quieto > 2-3 s.
Clips = capturas/<n>.mp4 (ver previews/cap_<n>.jpg). Coordenadas del mensaje en vivo como el piloto (mensaje ≈ (.5,.77), z 2.6).

| frase | plano |
|---|---|
| gancho_0 | tok full (0) → en «nueve»: mensaje z1.2→2.6 (.5,.77), vel .3 |
| gancho_1 (Jefe) | mensaje z2.6→3.4 sobre «croncias» |
| gancho_2 | m_intro z1→1.15 |
| gancho_3 | hojas_clips → «noventa» pegatinas → «mapas» m_yoshi desde 7 → «treinta» m_tetris |
| gancho_4 | investiga desde 3 z1→1.4 |
| contraste_0 | tok full (pensar) · contraste_1: investiga desde 8 vel 3 · contraste_2: tok → «real» fx_hojas |
| investiga_0 | investiga z1.2→1.7 vel 2 · _1: ayudante → «revisé» investiga desde 12 · _2: investigacion z1→1.5 (.4,.3) |
| investiga_3 | m_guantes desde 2 (rótulo «Los guantes de Mario Party») · _4: m_intro (pegatina Mario Party) |
| guion_0 | escribe_guion → «contados» m_yoshi desde 0 (contador 10/30) |
| guion_1 | guion_n64 z1→1.6 → «susurrando» z2.4 (.2,.12) donde se ve [whispers] · guion_2: guion_n64 desde 6 vel 3, z1→0.8 |
| voz_0..3 | voz_eleven → whisper desde 1 → whisper desde 6 → tok (fallo) → «Si la voz» whisper desde 11 |
| clips_0..4 | ayudantes_clips → hojas_clips z1→2.2 → hojas desde 6 → «treinta» fx_hojas desde 4 → m_guantes desde 2 → tok full (palomita) |
| capas_0..2 | m_intro (pegatina) → «noventa» pegatinas → m_yoshi desde 6 (ruta) → kit_mg desde 2 → «doscientos» mg_hojas / m_guantes desde 8 (MG del stick) |
| sonido_0..2 | mapas_sesion → m_tetris → **m_yoshi desde 0 mientras suena la OST (post 2,6 s, ver efectos)** |
| relevo_0..4 | relevo_a → tok → **cambio_cuenta z2.6 (.5,.77) en relevo_2 (Jefe)** → relevo_b → ayudantes_clips → tok (selfie) |
| revisa_0..4 | chequeo → fx_hojas desde 8 → render → m_cierre → tok (escuchar) |
| miniatura_0..3 | miniaturas z2.1 (.26,.3) código → flow → **si_flow z2.6 (.5,.77) (Jefe)** → miniaturas z1→2.1 (.74,.3) → «Desde» flow_imgs |
| cuenta_0..3 | cuenta z1.6 (.27,.45) → (.73,.45) → z1 → «decidir» mensaje desde 2 → investiga vel 6 z1→.8 |
| junta_0..2 | montaje → tok → **mensaje z3.4 sobre «croncias» (callback de la falta)** |

## efectos.py (copiar el del piloto y reanclar)
Rótulos en el piso (y=.885): 9 PALABRAS · 4 HORAS · 24:19 · 170 CLIPS · 1 106 ACCIONES · GRABACIÓN REAL · 1 · INVESTIGAR · 68 BÚSQUEDAS ·
FUENTE DE CADA DATO · 2 · GUION · 30 → 1 · 3 · VOZ · 8 RECHAZADAS · 3 REESCRITAS · 4 · IMÁGENES · 36 REHECHOS · VOZ = IMAGEN ·
90 PEGATINAS · MAPAS REALES · 18 ANIMACIONES NUEVAS · 220 EFECTOS · 5 · SONIDO · 36 PISTAS ORIGINALES · 180 000 TOKENS ·
6 SESIONES · 5 AYUDANTES · 6 · REVISAR · 27 ERRORES · 19:19 · 3 H 59 MIN · 17 NOV · CRÓNICAS DEL GAMING · TÚ DECIDES QUÉ SIGUE.
**Sonido nombrado (regla 31-oct):** en «Escucha.» (sonido_2) + post 2,6 s suena la OST real: copiar
`../n64_secretos/audio/ost/s21_mario_kart64_yoshi.wav` a `sfx/ost_yoshi.mp3` (ffmpeg, ~3,2 s desde un tramo con melodía) y
`PISTAS += dict(sfx="ost_yoshi", en="Escucha|fin", vol=.9)`; agachar música Lyria ahí (FX/mezcla) mientras suena.
SFX: los del piloto se generaron con ElevenLabs; NO repetir los mismos archivos (regla SFX repetidos): generar variantes nuevas
(prompts distintos) — saldo ElevenLabs: cuenta 1 = 10 000 (se renovó), cuenta 3 ≈ 1 550, cuenta 2 = 5.
