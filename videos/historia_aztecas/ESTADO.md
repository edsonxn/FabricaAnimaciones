# Toda la historia de los AZTECAS — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronopapel · PROGRAMADO jue 26-nov-2026 14:00 CDMX (2026-11-26T20:00:00Z) · https://youtu.be/K_k3xRVcjao
- estilo: boceto → doc de estilo: docs/estilo_boceto_guache_mapa.md § «Dibujos en Flow» + § «historia_aguascalientes» · ejemplo a copiar: videos/historia_aguascalientes/
- etapa: ✅ SUBIDO y PROGRAMADO 25-nov 21:50 (K_k3xRVcjao, privado hasta la fecha; miniatura Flow + .srt) · MASTER 18:20 verificado (CER 0,0033, desfase 0 ms)
- siguiente: medir a 7 días (≈ 3-dic) y anotar en canales/formula/cronopapel.md → al aprobar: `fab.py historia_aztecas limpiar`

## Sesiones (plan de tramos · «continúa el video aztecas» retoma aquí · protocolo docs/sesiones.md)
- alias: aztecas, historia de los aztecas, mexicas
- origen: el usuario (23-nov) pidió aplicar la fórmula de «Menuda Historia» (historia COMPLETA larga con dibujitos, personaje fijo, miniatura limpia) a Cronopapel, ~16 min; análisis en `canales/formula/cronopapel.md` § «Revisión 23-nov-2026». Eligió en la tele: «Todo hoy aunque se acabe la semana» (cuenta semanal al 88 %).
- PERSONAJE FIJO del canal (nuevo): **Xolo**, un xoloitzcuintle que acompaña toda la historia; chiste que se repite: «siempre a un paso de terminar en el menú»; remate: guía de las almas al Mictlán.
- vista previa: NO; directo al MASTER (regla 5-nov) y aviso.
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + hechos + fotos + mapa (subagentes) + voz + tiempo | ✅ 23-nov | |
| 2 | Flow (hojas por época + hoja de Xolo) + recorte | ✅ 23-nov | |
| 3 | coreografía en paralelo (coreo_1..4) + revisión | ✅ 23-nov | |
| 4 | sfx → música → mezcla → render → chequeos → miniatura Flow → subir y programar | ✅ 25-nov | render en 2 tandas (24-nov cancelado; 25-nov --procs 4 tras Warcraft, 20:06-21:35) |

## Registro de producción (cerrado 25-nov)
- 23-nov ~09:15: kit copiado de historia_aguascalientes (core, reg, mapa, escenas, pegflow, foto_peg, sellos, obj_*, trans, _prueba, _hojas, _qa_choques, flow/ref_cronopapel.jpg).
  Subagentes lanzados: investigación (`_hechos.md` + `fotos/` con creditos.json e `_indice.jpg`) y mapa (`mapa.py`, `_mapa_notas.md`: Valle de México con lagos de 1519 + centro de México + imperio).

- 23-nov ~10:15: guion ✅ (17 escenas, 138 frases, 2 416 palabras) · voz ✅ ElevenLabs Alberto cuenta 4 (3 136 créditos; saldo ≈ 68 700) · `seleccionar` + `idioma_voz` en marcha.
- Flow ✅: proyecto «Nov 23 - 08:54» en Chrome; 1K (1376x768) en `flow/k1/NN.jpg` (mosaicos bajados por un botón en la página: el 2K del menú no respondía a clics automáticos → 1K, excepción a la regla de 2K).
  Hojas elegidas en `hojas/*_a.jpg` y recortadas en `piezas/<hoja>/` (mira `_indice.jpg` de cada una): 01/01b/01c_xolo_hoja (Xolo 24 poses), 02_migracion, 03_chapultepec,
  04_fundacion, 05_chinampas, 06_alianza, 07_moctezuma1, 08_vida, 09_mercado, 10_tributo, 11_axayacatl, 12_ahuizotl, 13_moctezuma2, 14_cortes, 15_caida,
  16_legado, 17_ruta, 18_mictlan (Xolo guía de almas), 24_xolo_salta; ciclos 19_xolo_corre (8), 20_mexica_camina (8), 21_canoa_ciclo (6), 22_caballo_galope (6), 23_guerrero_corre (8).
  Prompts en `flow/prompts.py`; `flow/_clip.py <hoja>` copia un prompt al portapapeles (Ctrl+V en Flow, re-añadir ingrediente antes de cada envío).

- 23-nov ~09:45: guion corregido con `_hechos.md` (17 frases) · voz 138/138 (CER_MAX_POR_FRASE 0,08 en 13 frases con nombres nahuas; idioma OK) · timeline 1 099,8 s (18:20)
  · música ✅ `audio/musica.wav` con 8 piezas de la BIBLIOTECA (Lyria API sin saldo, 402) · mapa ✅ (`_mapa_notas.md`; faltan tepanecas/acolhuas/imperio_1428 por 429 de Commons)
  · miniatura ✅ `salida/miniatura.jpg` (Flow, perfil jairedson5, «200 AÑOS / AZTECAS», variante 38bbe0cf) · `youtube.json` ✅ (falta __FOTOS__ = créditos de las fotos usadas)
  · comentarios: 0 en 21 d → sin agradecimientos/críticas. · COREOGRAFÍA: 4 subagentes con `_brief_coreo.md` (coreo_1..4) EN MARCHA.
- ~10:10: coreo_1..4 ✅ (74 fotos, ~4/min; revisiones `previews/rev_c1..c4_*`) · SFX ✅ 551 eventos (70 nuevos, 1 340 créditos) · mezcla ✅ −14,5 LUFS, voz +13,8 dB
  · chequeo ✅ (idioma OK; aviso «sonido nombrado» = falso positivo por «la voz de Cortés») · RENDER en marcha (`fab.py video` → `final` → `verificar`, logs `_render_log.txt`, `_verif_log.txt`).
  · youtube.json completo (maps + créditos de 66 fotos). Hueco: **mié 25-nov-2026 14:00 CDMX = 2026-11-25T20:00:00Z** (horario mié-vie 14:00; último publicado 7-nov).
- 24-nov: render CANCELADO por el usuario (había DOS renders a la vez tras reiniciar la sesión → memoria agotada). 104/367 segmentos guardados en `segmentos/`;
  `python fab.py historia_aztecas video` retoma desde ahí (un solo render; cada proceso ~2-3 GB por la rejilla «cuenca» de 2000 px/°).
- 25-nov 11:05: retomado. 118/367 segmentos en disco. Esperando a que termine el Whisper (`idioma_voz`) de la sesión de wow_ruta_profesiones (regla «un render a la vez»). ◐ 11:06 RENDER relanzado (log `_render_log2.txt`); a las 11:20 se TRABÓ (SystemError en `cv2.GaussianBlur`, foto_peg.py:268 = memoria agotada: la sesión de wow_ruta_profesiones lanzó `apoyos` con 10 GB de RAM). 12:53 CANCELADO por el usuario. **140/367 segmentos completos**; los `*.tmp.mp4` son restos. Relanzar con menos procesos y solo con ≥ 12 GB de RAM libre (OJO: `render.py` usa **12 procesos por defecto**). 12:58: el usuario decidió esperar a que termine Warcraft; hay una espera automática que lanza `fab.py historia_aztecas video --procs 4` (log `_render_log3.txt`) cuando existe el MASTER de wow_ruta_profesiones, ya no corre nada de esa sesión y hay ≥ 12 GB libres. Si la sesión se perdió, lanzarlo a mano con esas condiciones. Hueco movido a **jue 26-nov 14:00 CDMX = 2026-11-26T20:00:00Z** (el del 25 ya no se alcanza).
- Después del MASTER: avisar → `yt subir historia_aztecas cronopapel private --publicar 2026-11-26T20:00:00Z` → miniatura → canales/cronopapel.json + BITACORA → Facebook «Historias Perdidas de México».

- 25-nov ~22:20: una prueba del supervisor nuevo dentro de `render.py` cambió la firma de `cache_escenas` y **borró 359 de 367 segmentos** (quedan 8). El MASTER y la subida no se tocaron. Si algún día hay que arreglar un tramo, toca render completo (~1,5 h con `fab.py historia_aztecas video`, que ya usa `render_seguro`).

## Lecciones de este video (solo lo no obvio)
- Flow: el botón «Descargar lote» (icono ⬇ junto al prompt en la vista de lista) baja TODAS las variantes de ese prompt en un .zip a Descargas (E:\Downloads_jaire): mejor que el menú por imagen.
- Flow en Chrome (23-nov): pegar el prompt con el PORTAPAPELES (`flow/_clip.py`) sale gratis en tokens; el `fetch` a un servidor local desde Flow se cuelga (permiso de red local) y las descargas por `<a download>` se bloquean tras la primera hasta que el usuario permite «descargas múltiples» en flow.google.com → un MOSAICO de todas las imágenes en UNA descarga, cortado luego en Python.
- Flow «high demand»: ~1 de cada 3 hojas falla en ráfaga; reenviar las que falten tras ver el mosaico. Dos prompts de ciclo seguidos se MEZCLAN en una imagen (caballo + guerrero, peregrino + canoa): se parten por filas.
- Render (25-nov): cuando se acaba la RAM, el render no truena: los procesos que dibujan mueren con `SystemError ... GaussianBlur` y el principal se queda colgado SIN escribir nada en el log. Si `segmentos/` no cambia en 5 min, está trabado. Cada proceso usa 2-3 GB por la rejilla «cuenca».
- ElevenLabs 23-nov: cuenta 1 sin créditos, cuentas 2 y 3 con pago pendiente (401 payment_issue); la 4 funciona.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO, miniatura Flow, registrado (`canales/cronopapel.json`, BITACORA), Google Maps en la descripción (25-nov)
- [x] Facebook «Historias Perdidas de México»: PUBLICADO 25-nov 22:00, fb_id 1476982281050051 (copia H.264 CRF 23, 689 MB; post `E:\PaginaFace\paginas\historias_mx\posts\2026-11-26_1900_historia-aztecas`, con 📍 CÓMO LLEGAR)
- [ ] medir a 7 días y anotar en `canales/formula/cronopapel.md`
