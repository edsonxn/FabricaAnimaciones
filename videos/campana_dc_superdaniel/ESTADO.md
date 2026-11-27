# campana_dc_superdaniel — «Súper Daniel arregla el alumbrado» (Campaña Daniel Cervantes, demo)

Pedido del usuario (27-nov-2026): video corto ~20 s, VERTICAL, todo en **Flow con puntos**, resolución mínima (360p) y luego
reescalar. Realista pero absurdo/cómico: Daniel sale a cámara en una calle real de Juchipila, se pone un traje de superhéroe
azul con el logo del PAN (armado tipo armadura high-tech), sale volando y va a reparar el alumbrado público.
Proyecto, no canal: nada se publica sin OK; entrega por Rayo. Ver `docs/campana_daniel_cervantes.md`.

## Decisiones
- Omni 1.2 Flash · 9:16 · 360p · x1 (1 punto/s). Guía aplicada: `docs/flow_prompts.md` (RGC §R47), hecha en esta sesión.
- Ingredientes renombrados y citados con @: `daniel_cervantes` (`../campana_dc_agua/img/daniel_limpia.png`), `daniel_traje`
  (`previews/c1_t7.png`, cuadro del clip 1), `plaza_xochipilli`, `juchipila_aerea` (Commons, `fuente/`), `logo_PAN` (`fuente/pan_2025.png`).
- Voz: la de Flow con lipsync → Demucs + ElevenLabs speech-to-speech al clon de Daniel (cuenta 4) con `sts.py`.
- Cierre por código: logo + «DANIEL CERVANTES» + «JUCHIPILA, CON LUZ» + rótulo chico «Hecho con IA».
- Proyecto Flow: https://flow.google.com/project/dac5e2ee-caa7-4e46-821c-dcabdf42ff8d
- Descarga sin ventanas: `recibe.py` (puerto 18792) + fetch desde la página de Flow.

## Guion (como quedó)
1. 0-10 s (clip 1, Ingredientes): plaza al anochecer, Daniel a cámara «¿Otra vez sin luz? Yo me encargo.», placas azules lo
   cubren (PAN en el pecho), despega.
2. 10-20 s (Ampliar 10 s del mismo clip): vuela sobre la torre rosa, baja a una calle con faroles, los arregla, vecinos; «¡Listo!».
3. 20-25 s (remate, Fotogramas desde un primer plano hecho con Nano Banana): pulgar arriba, «Juchipila, con luz.», guiño.
4. 25-26.7 s cartela.

## Avance
- ✔ MASTER `salida/superdaniel_MASTER.mp4` — 26.7 s, 1080×1920, 24 fps, −14.3 LUFS, pico −1.1 dBFS.
  Whisper en la mezcla final: «otra vez sin luz yo me encargo · listo · Juchipila con luz». Hoja: `previews/hoja_master.jpg`.
- Montaje: `python monta.py` (tramo A = c12 reescalado local lanczos+unsharp; B = c4 «720p mejorada»; cartela; audio
  `audio/c12_daniel.wav` + `audio/c4_daniel.wav`). `--solo-audio` rehace solo la mezcla.
- Puntos de Flow: ~35 (clip 1 10 + Ampliar 10 + remate fallido 5 + edición 5 + remate bueno 5; imágenes 0).
- Nada publicado. Pendiente: OK del usuario y entrega por Rayo.

## Lecciones
- Remate 1 (Fotogramas desde el último cuadro, cara chica) → la cara derivó en el primer plano (perilla, más pelo).
  La edición «Describe cómo editar» con @daniel_cervantes casi no la cambió. Solución: imagen inicial en primer plano con
  Nano Banana (@daniel_cervantes + @daniel_traje + cuadro de la calle) → Fotogramas. Pasado a `docs/flow_prompts.md` §3.
- Videos > 15 s no se editan/amplían/mejoran en Flow → el tramo de 20 s se reescaló en local.
- Salto de luz entre el plano abierto (atardecer) y el primer plano (noche): aceptable como corte; si se rehace, pedir
  «dusk sky» en la imagen inicial.
- Sonoridad: loudnorm de 1 pasada dejaba −17 LUFS (picos de los propulsores); se usa ganancia medida + limitador rápido.

## Sesiones
- 27-nov: arranque, clip 1, investigación de prompts de Flow (guía nueva), Ampliar, remate, montaje y MASTER.
  Para seguir: «continúa el video campana_dc_superdaniel».
