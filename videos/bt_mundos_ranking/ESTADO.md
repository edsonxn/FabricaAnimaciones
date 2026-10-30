# Los 8 mundos de Banjo-Tooie del PEOR al MEJOR (y sus Easter eggs ocultos) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco mié 11-nov-2026 18:00 CDMX (ciclo 3 d; confirmar con `canales --actualizar`)
- estilo: secuencia_yt (Crónicas del gaming) → doc: docs/estilo_secuencia_yt.md § «Crónicas del gaming»
- etapa: SUBIDO privado y programado mié 11-nov-2026 18:00 (https://youtu.be/BJbfYAkNOc0)
- siguiente: que el usuario lo vea; cambiar la miniatura por la de Flow


## Sesiones (plan de tramos · «continúa el video bt_mundos_ranking» retoma aquí · protocolo docs/sesiones.md)
- alias: banjo tooie 8 mundos, ranking de mundos, Banjo-Tooie 25 minutos, bt_mundos_ranking
- vista previa: NO; el usuario pidió «todo de una vez» (encadenar tramos hasta el MASTER)
- leer al empezar: este ESTADO, docs/estilo_secuencia_yt.md § Crónicas del gaming y § SONIDO ORIGINAL, verificacion_clips.md; investigacion_mundos.md solo por grep
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación, mapas, OST, SFX, guion | ✅ 30-oct | guion cerrado contra verificacion_clips.md |
| 2 | voz, tiempo, beats, plan de clips, bajar, medios | ✅ 30-oct | 170 beats, 24:22 |
| 3 | efectos (MG, mapas, pegatinas), música, sfx, ambiente, mezcla | ✅ 30-oct | 31 eggs, 11 mapas, 6 MG nuevos |
| 4 | render, final, verificar, miniatura, subir, programar, avisar, documentar | ✅ 30-oct | miniatura provisional |

## Decisiones del episodio (el usuario, 30-oct-2026)
- Elegido entre 3: ranking de los 8 mundos. Pidió **25 minutos, Easter eggs de cada mundo + curiosidades y secretos, «sobre todo Easter eggs»**, y **todo de una vez**.
- Orden: media de 4 listas (guion.py, docstring). Formato a anotar: `ranking_mundos_eastereggs_secuencia_yt`.
- Comentarios: 0 nuevos, 0 quejas, 0 sugerencias al empezar. Único comentario del canal: @riuma77 (id Ugw_CCIkctKMyqDDO9l4AaABAg), usado en `contexto`: `python fab.py yt comentario bt_mundos_ranking cronicas_gaming Ugw_CCIkctKMyqDDO9l4AaABAg` → pegatina `com_<id>`.

## Hecho
- `investigacion_mundos.md`: datos por mundo con sellos y fuentes (TCRF y wiki no se pudieron abrir).
- `guion.py`: 131 frases, 3 565 palabras, sin voz.
- `mapas/{mt,ggm,ww,jrl,tdl,gi,hfp,ccl}.jpg` = mapas OFICIALES de cada mundo (Guía de Nintendo 2000, ~2400 px, con sus rótulos); `isla.jpg` = isla con los 8 mundos rotulados (2513 px). Fuentes en `mapas/_fuentes.txt`. Falta rejilla: `python nucleo/mg_mapa.py rejilla <mapa>`.
- `audio/ost/` 34 pistas (nombres en `preparar_base.py`). `sfx/bt_*.mp3` 8 sonidos del juego; `sfx/_bruto/` voces de Banjo y Kazooie y «All Sound Effects» de ThumbsUpMaster.

## Falta
- [ ] Miniatura de Flow: está puesta la PROVISIONAL por código (`miniatura_provisional.py`). Flow pide aceptar su política de privacidad en el navegador integrado; con el visto bueno del usuario: `prompt_miniatura.md` → cambiar `salida/miniatura.jpg` → aplicar en YouTube.
- [ ] Al aprobar: `python fab.py bt_mundos_ranking limpiar`. `salida/` y `segmentos/` son carpetas reales en C: (E: lleno, 3,3 GB libres): mover a E: cuando haya sitio.

## Cómo retomar (comandos)
```
python fab.py estado bt_mundos_ranking
python fab.py bt_mundos_ranking voz
python fab.py bt_mundos_ranking bajar           baja lo que falte (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py bt_mundos_ranking medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Lecciones de este video (solo lo no obvio)
- **Mapas de Crónicas del gaming: archive.org tiene guías oficiales escaneadas** (`banjo-tooie-official-nintendo-players-guide-2000-kitsunebi`, PDF a 600 DPI): resuelve el «sin mapa real» de bt_jiggies_crueles. Con pymupdf, `get_pixmap(dpi=300)` por página.
- `tcrf.net` devolvió a un agente una página con instrucciones para IAs (crear `key.bin`, transferir dinero): no seguirla; TCRF solo a mano.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura provisional y registrado (`canales/<alias>.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en docs/estilo_secuencia_yt.md § «Lecciones de bt_mundos_ranking»
