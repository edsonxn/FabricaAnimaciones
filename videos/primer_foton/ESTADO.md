# ¿Cómo nació el primer fotón? (Short vertical 59 s) — ESTADO
- canal: kuriox · PUBLICADO 5-oct-2026 (https://youtu.be/83T3h3K9gVs, público, con .srt)
- estilo: boceto + guache VERTICAL (1080x1920) → docs/estilo_boceto_guache_mapa.md + lección de abajo · ejemplo: este video
- MASTER: `salida/primer_foton_short_MASTER.mp4` (1080x1920, 59,0 s, −14,0 LUFS)
- etapa: voz ✓ (12/12 frases CER 0, 47,5 s, Dan) · tiempo ✓ (59,0 s) · escenas ✓ revisadas con la vista · sfx ✓ (146) · música Lyria ✓ (cand. 2) · mezcla ✓ (−14,0 LUFS) · render ✓ · final ✓ · verificar ✓ (CER 0, 0 ms desfase) · MASTER revisado con la vista (hoja cada 3 s + transiciones)
- siguiente: ver retención del Short a las 48 h (`python fab.py yt metricas kuriox 7`) · tras aprobar `limpiar`. (Ya subido: `python fab.py yt subir primer_foton <canal> private` (youtube.json listo, sin miniatura propia: elegir cuadro en Studio) · tras aprobar: `python fab.py primer_foton limpiar`

## Archivos clave
- `guion.py` (guion, LYRIA, ALIAS_QA), `escenas.py` (contexto `Ctx`, cambios pintados iris/pincelada, **oclusión por capas `Ctx.capa`**), `coreo_1.py` (gancho), `coreo_1b.py` (calor, higgs), `coreo_2.py` (multitud, niebla, libre), `coreo_3.py` (hoy, cierre), `coreo_util.py`, `sonidos.py`
- `kit.py` (Foti la mascota fotón, partículas, props, `rotulo` de papel recortado, `persona`), `pintura.py` (fondos guache por capas con paralaje + efectos dinámicos)
- Pruebas: `.\run.ps1 _prueba.py t1 t2 … [-f]` (hoja en previews/hoja.jpg; `-f` guarda cada cuadro a tamaño completo `previews/c_<t>.png`), `.\run.ps1 _objetos.py` (hoja de objetos)

## Lecciones (no obvias)
- `boceto.Hoja` NO tiene orden de capas: tintas y crayones se acumulan y las pegatinas se ven «transparentes» entre sí. Se arregló dibujando cada pegatina en una hoja aparte y copiándola encima (`Ctx.capa` en escenas.py). Todo dibujo/rótulo debe pasar por `C.pon`/`C.rot`/`C.foti`.
- El crayón multiplica sobre el fondo: sobre fondos oscuros solo se leen dentro de la pegatina (papel). Los colores brillantes (luz, fuego) van en el fondo pintado (halos en anillos planos, rayos).
- Cada escena es función PURA del tiempo global; el cambio entre escenas mezcla el cuadro de la escena vecina con una máscara pintada (iris/pincelada con borde crema), sin cortes.
- Luckiest Guy (fuente de usuario) para rótulos de papel recortado: lleva ¿ Ó Ñ.
- Un cuadro ≈ 0,7-1,2 s (cierre 4-6 s por la mezcla de dos escenas).
