# La historia de Jalisco en 5 minutos — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: cronopapel · PROGRAMADO mar 3-nov-2026 14:00 CDMX (publishAt 2026-11-03T20:00:00Z) — https://youtu.be/SiA13ZlBK5A
- estilo: boceto + guache con mapa (kit v2.1 de historia_mexico) + PEGATINAS FLOW → docs/estilo_boceto_guache_mapa.md § «Dibujos en Flow» · ejemplo de este flujo: este video
- etapa: subido (privado, programado; miniatura y .srt cargados)
- siguiente: a los 7 días medir con `yt metricas cronopapel` y anotar en canales/formula/cronopapel.md (prueba `estado_mx_pegatinas_flow`); al aprobarlo, `python fab.py historia_jalisco limpiar`

## Sesiones
- alias: historia de Jalisco, Jalisco en 5 minutos
- vista previa: NO (el usuario, 22-oct: «el video entero»); hecho de corrido en una sesión
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz + pegatinas Flow + mapa + coreografía + render + subida | ✅ 22-oct-2026 | primer Cronopapel con pegatinas de Flow |

## Hecho
- guion.py (40 frases, 12 escenas), `_hechos.md` verificados por búsqueda web (correcciones: Juan de Oñate 1532, Calderón 6 000 vs decenas
  de miles, 3.er estado más poblado, Mundial 2026 México 1-0 Corea).
- Voz Chatterbox Dan 40/40 (243 s); timeline 270,0 s (4:30). CER final 0,26 %.
- Mapa: `mapa.py` rejilla "mx" = Jalisco (260 px/°), ETOPO1 + Natural Earth 10 m (estados, Chapala, Santiago/Lerma); 25 campos.
- Pegatinas: `flow/prompts.py` (13 hojas, ingrediente `flow/ref_cronopapel.jpg`); 10 en 2K (hd/), ciclos 10/11/13 en 1K; `pegflow.py`
  + `coreo_peg.py`; periódico y balón tomados del 1K (`_piezas_1k/`).
- Lyria 3 tramos (0,24 US$) catalogada; sfx 103 eventos; mezcla −14,00 LUFS / −1,44 dBTP / voz +13,6 dB.
- Render 90 segmentos (15 min, 12 procesos). MASTER revisado cada 3 s (previews/master_resumen_0/1.jpg): sin cuadros negros ni vacíos.

## Lecciones (aplicadas a docs)
- Ingrediente de estilo = clave para que Flow dibuje como el kit; re-añadirlo antes de cada prompt (o Ctrl+V).
- 2K: el papel blanco se parte al recortar y objetos cercanos se juntan → comprobar `_indice.jpg` y mezclar piezas del 1K.
- Con rejilla de 260 px/° los territorios se aclaran desde z 1,8 y `core.ZREF = 1.7`; si no, las pegatinas del mapa salen diminutas.
- `T(e, "que")` encuentra el «que» de la frase anterior: usar `frase=` en palabras comunes.
- `tts_select.silenciar_arranque` borraba un «Hoy,» inicial: arreglado en el núcleo (si Whisper deja de oír la 1.ª palabra, no silencia).
- El panel remoto (puerto 8766) puede tener abierto el MASTER: `final` falla al reemplazarlo → montar a otro nombre y `os.replace` en bucle.
