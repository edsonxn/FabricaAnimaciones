# Las 15 cosas más INÚTILES de Skyrim — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · meta: hueco lun 26-oct-2026 12:07 CDMX (≥ 96 h tras misiones_nunca, 22-oct 18:07Z) · ~15 min (el usuario)
- estilo: secuencia_yt (gameplay Skyrim por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · voz Chatterbox Sarcastica → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: ✅ SUBIDO y PROGRAMADO lun 26-oct-2026 12:08 CDMX (2026-10-26T18:08:00Z) · https://youtu.be/uz1kE1BI4w8 · MASTER v3 (16:35) con miniatura y .srt
- ✅ **PÚBLICO** desde el lun 26-oct 12:08 CDMX · https://youtu.be/uz1kE1BI4w8 (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
- siguiente: monetización en Studio (anuncios + cuestionario) PENDIENTE · `limpiar` cuando salga público

## Sesiones (plan de tramos · «continúa el video tes_cosas_inutiles» retoma aquí · protocolo docs/sesiones.md)
- alias: cosas inútiles, 15 inútiles, tamriel inútiles · vista previa: 🎞 Montaje del panel (el usuario, 23-oct), sin render parcial
- leer al empezar: este ESTADO + docs/estilo_secuencia_yt.md § «Crónicas de Tamriel», § PEGATINAS, § MOTION GRAPHICS NUEVOS y § MAPAS; copiar de videos/tes_misiones_nunca/
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 23-oct): guion UESP + voz + beats + clips + pegatinas + MG + mapas + música + mezcla + render + revisión + miniatura + subida | ✅ 23-oct | 131 frases, 115 clips, 47 pegatinas, 6 MG nuevos + rejilla, 3 mapas; subido uz1kE1BI4w8 programado 26-oct 12:08 CDMX |

## Decisiones del episodio (23-oct-2026)
- tema elegido por el usuario entre 3 con datos: lo más INÚTIL (ref. Choa «60 Useless Skyrim Facts» ×85,9). Variable que se prueba: el
  tema (de «no debes hacer» a «no sirve»); resto = fórmula de tes_misiones_nunca (15 puestos). Sin patrocinio. Puente final a exploits.
- lista (15→1): Nazeem · cortar leña · Piedra de la Torre · Llave de cera · Clarividencia · bollo dulce · Telequinesia · Reflejos
  rápidos · caballos · Voz del Emperador + Dominar animal · Cuchilla de Mehrunes · Hacha del arrepentimiento · hombre lobo sin
  Dawnguard · Proyectar voz · Pergamino antiguo (gema: la saga se llama así y lo mejor es vendérselo a Urag)
- formato a anotar al subir: `lista_15_inutiles_secuencia_yt`
- MG nuevos propuestos (frase ancla): (1) «LA AGENDA DE NAZEEM» p15: reloj de 24 h que se llena (posada 20-8, mercado 4 h, paseo,
  posada desde las 16) · (2) «LA CUENTA DE LA LEÑA» p14: troncos que caen a 5 monedas hasta 5 000 = Hogar de la Brisa (×1 000) ·
  (3) «LA PANADERÍA» p10: 5 ingredientes → 1 bollo = 5 de salud contra la poción = 25 · (4) «EL TRATO» p4: Barbas contra el hacha en
  una balanza de Clavicus, las cifras del hacha se tachan · (5) «COMPRA-VENTA» p1: pergamino → 2 000 → 4 000 con Urag.
- mapas (tema `tes`): ruta Lucero del Alba → Piedra de la Torre → Hibernalia (p13) · «¿dónde está?» Punta Mellada (p2) · ruta de
  Barbas Falkreath → santuario de Clavicus (p4).

## Hecho
- guion.py con datos verificados en UESP (fuentes en el docstring) y nombres es-ES de la wiki en español; FONETICA
- pegatinas/ (47 imágenes de la wiki, mosaico previews/pegatinas.jpg revisado; fuentes en pegatinas/_fuentes.txt)
- mapas/skyrim.jpg (UESP SR-map-Skyrim) + hojas previews/mapa_torre|clavicus|punta.jpg revisadas
- 6 MG nuevos en nucleo/mg_tes.py (agenda, lena, salud, receta, trato, compraventa) + hojas previews/mg_*.jpg revisadas
- efectos.py escrito (anclas sin comprobar hasta `tiempo`) · prompt_miniatura.md + miniatura_ing/ (Flow en marcha)
- voz 131/131 (26 aceptadas por CER/TAIL/GAP tras leer cada transcripción; cierre_0 con s3) · tiempo 986,7 s · 115 beats
- busquedas.json escrito · `bajar -j 4` y `musica` (Lyria nueva: la biblioteca solo tenía piezas de Tamriel) en marcha
- miniatura: salida/miniatura.jpg = v1 de Flow (elegida por el usuario)
- música (Lyria API sin saldo, 402; el usuario: «biblioteca y puedes usar música del juego original también»): tramos 1 kalimdor_t1,
  3 kalimdor_t8, 4 clases_ocultas_t4, 7 caxcan_mixton_t7, 8 clases_ocultas_t5 (biblioteca, otros canales) + OST de Skyrim (Jeremy
  Soule, yt-dlp en E:\…\ost\): 2 Far Horizons, 5 Out of the Cold, 6 Ancient Stones, 9 Sky Above, Voice Within → audio/musica.wav
  ⚠ la OST puede traer reclamaciones de Content ID: créditos en la descripción.

## Falta
- [x] monetización en Studio: anuncios Activada + mid-rolls, cuestionario «Nada de lo anterior» → «Adecuado para anuncios» (23-oct)
- [ ] `python fab.py tes_cosas_inutiles limpiar` cuando salga público
- cierre: registrado en canales/cronicas_tamriel.json (formato) y BITACORA ✅ · hallazgos en docs/estilo_secuencia_yt.md § Tamriel ✅
  · SFX catalogados ✅ · música NO catalogada (tramos 2/5/6/9 son OST de Skyrim, no Lyria)

## Cómo retomar (comandos)
```
python fab.py continuar tes_cosas_inutiles
```

- clips 115/115 tras 4 rondas (30 + 13 + 4 + 2 rehechos: menús, negro, webcam, Elden Ring, cocina real, rótulos de mods);
  recorte_por en 008 y 023
- voz: «Skyrim» = «Escairim» (el usuario); 15 frases regeneradas, tomas con la palabra más larga (≥ 0,46 s); `reajustar`
  → 975,3 s; scene-001 rebajada; música rearmada

- fx hoja revisada (5 hojas): rehechos 024, 051 (negro), 058 (negro), 074, 097; recorte 015 (BANDICAM); wilmuth adelantada
- blackdetect de los 115 clips limpio · youtube.json escrito (capítulos, créditos de 72 canales, OST) · render en marcha (23-oct)

- render v1 cortado 2 veces por el disco E: (USB TOSHIBA: eventos 153/50/51 de 13:12 a 14:36; el usuario lo arregló) → v2 ok
  (16:35 con pantalla final); revisión del MASTER (4 hojas cada 6 s + blackdetect): 066 (rótulo FRENZY RUNE), 075 (menús),
  107 (cadáver) rehechos → render v3 en marcha

## Lecciones de este video (solo lo no obvio)
- Un render que muere con BrokenPipe sin error de ffmpeg + `FileExistsError` en una junction = el disco externo E: se está cayendo:
  mirar el Visor de eventos (Ntfs 50/51/140, disk 153) antes de relanzar.
- FONÉTICA de Skyrim = «Escairim» (el usuario, 23-oct). Tras regenerar con `--solo`, `seleccionar` reevalúa solo; para forzar
  una toma, apartar la otra a voz/_descartes Y quitar su entrada de eval.json (si no, la sigue eligiendo).
- Miniatura: el usuario eligió la v1 (Nazeem con aspecto de PNJ real del juego) sobre la v2 (pintado): el personaje debe verse
  como el render del juego, no ilustración (anotado en docs/estilo_secuencia_yt.md § Tamriel).
