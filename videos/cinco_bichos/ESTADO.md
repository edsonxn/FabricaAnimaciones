# 5 Bugs You Should NEVER Kill Around Your House (And 1 You Should) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: wild_next_door (EN INGLÉS) · PÚBLICO desde lun 12-oct-2026 21:42 UTC (adelantado por el usuario; estaba programado mié 21-oct 16:00 UTC)
- estilo: secuencia_flow (dibujo animado de Flow, TODO IMAGEN, 96 beats) → docs/manual_wild_next_door.md · ejemplo: videos/ciempies_casa/
- etapa: PÚBLICO desde lun 12-oct 21:42 UTC (https://youtu.be/8q2TyqEBRNg, con miniatura; adelantado por el usuario con `--forzar`: el canal llevaba 3 días sin video) · MASTER 8:38 verificado
- siguiente: nada con YouTube. A los 7 días (≈19-oct): `python fab.py yt videos wild_next_door`, llenar la fila en `canales/formula/wild_next_door.md` y luego `python fab.py cinco_bichos limpiar`

## Decisiones del episodio (el usuario, 11-oct-2026: «tú elige todo, orquesta todo, estaré ausente, súbelo en privado con su miniatura»)
- Tema elegido con datos (`ideas --actualizar` 11-oct): hipótesis 2 de `canales/formula/wild_next_door.md`, empaque «Never Kill» + estructura en
  LISTA (Curious Kids Discover ×70 «5 Animals You Shouldn't Kill Around Your House»; The-Wild-Discovery ×382 con araña que caza viudas).
- Lista en cuenta regresiva: 5 mantis · 4 araña lobo · 3 tijereta (mito del oído a mitad) · 2 araña saltarina (la de la ventana
  del gancho) · 1 avispa alfarera azul (caza viudas negras) · «la que sí»: cucaracha alemana. Cierre circular a la cocina del gancho.
- TODO IMAGEN: Flow marcaba **0 puntos** (se gastaron los 55 en `arana_techo`). Las imágenes de Nano Banana 2 Lite SIGUEN SALIENDO gratis.
- Mascotas con accesorio fijo (FICHA): mantis con moñito morado, araña lobo con pañuelo rojo, tijereta con orejeras rosas, saltarina con capa
  azul, alfarera con casco naranja, cucaracha con antifaz de ladrón.
- Miniatura elegida: «DON'T SQUISH THEM» (zapato sobre 3 bichos). Alternativas en `salida/`: `miniatura_alt_901.jpg` («NEVER KILL THESE»
  con matamoscas) y `miniatura_alt_903.jpg` (gran «5» + «NEVER KILL»).
- (histórico) Se subió sin programar a propósito: «súbelo en privado» no incluye fijar fecha. Después quedó programado mié 21-oct 16:00 UTC y el 12-oct el usuario lo adelantó: salió público ese día.

## Hecho
- Guion 75 frases / 1 458 palabras con ficha de hechos y fuentes en el docstring; voz EnglishComic 75/75 (aceptadas con cifras falsas
  positivas: `four_0`, `two_1`, `two_6`; colas altas pero transcripción completa: `four_2`, `four_6`, `four_7`, `three_9`, `two_5`).
- 96 imágenes por el navegador integrado (Claude in Chrome se desconectó): 8 rehechas en una 2.ª ronda (viejas en `medios/_ronda1/`).
- Música Lyria en 4 tramos (518,4 s). MASTER 1080p 8:38, −14,02 LUFS, pico −1,35 dBTP, voz/fondo 13,2 dB, CER medio 0,008
  (los 5 «>2 %» son cifras/«Ear Wig»), sin desfase. Revisado con la vista (hoja 1 cuadro/12 s + blackdetect sin cuadros negros).
- `youtube.json` con capítulos y fuentes; subido en privado con miniatura; anotado en `canales/wild_next_door.json` y BITACORA.

## Falta
- [x] Que el usuario vea el MASTER y decida la fecha: lo publicó el 12-oct 21:42 UTC
- [ ] A los 7 días de publicarse: llenar la fila en `canales/formula/wild_next_door.md`; `python fab.py cinco_bichos limpiar`

## Archivos clave
- `guion.py` (narración + FICHA + LYRIA + CER/TAIL por frase), `hacer_prompts.py`, `_miniatura.py`, `_ronda.py`, `_dl.py`, `beats.json`, `youtube.json`
- Ruta de imágenes sin extensión: `nucleo/flow_integrado.py` + manual § «Imágenes SIN extensión de Chrome y con 0 puntos»

## Lecciones de este video
- Con 0 puntos de Flow las IMÁGENES siguen gratis: un video de 8-9 min sale completo sin puntos (solo se pierden los clips).
- Para 1 458 palabras la voz dio 8:38 (no 9:50): EnglishComic lee ~2,8 palabras/s en frases cortas de lista.
- La ronda de voz tardó ~45 min con 4 tomas por frase: 17 frases necesitaron 2.ª ronda y 8 acabaron aceptadas por CER/cola
  (cifras «4», «6,000», «2022» y colas altas) → poner `CER_MAX_POR_FRASE`/`TAIL_MAX_POR_FRASE` desde el guion si hay cifras en letras.
- Claude in Chrome puede desconectarse a mitad; el navegador integrado ya tiene sesión de Flow y basta (ver manual).
- ffmpeg en Git Bash: salida a `/tmp/...` falla (ruta de Windows) y las imágenes sueltas piden `-update 1`; usar PIL para hojas.
