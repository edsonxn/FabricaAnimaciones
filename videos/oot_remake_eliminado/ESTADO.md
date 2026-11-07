# Lo que Nintendo ELIMINÓ del REMAKE de Ocarina of Time — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco dom 8-nov-2026 18:00 CDMX (2026-11-09T00:00:00Z) · gancho = el remake salió el 5-nov
- estilo: secuencia_yt + kit translúcido de Zelda (copiar de `videos/oot_remake_cambios/`) · voz ElevenLabs Hope turbo · OST oficial de Ocarina → doc: docs/estilo_secuencia_yt.md § Crónicas del gaming
- etapa: ✅ SUBIDO privado y programado dom 8-nov 18:00 CDMX — https://youtu.be/WjDK78u1ZO0 (MASTER 9:46, miniatura Flow)
- siguiente: medir a 7 días (~16-nov) contra la mediana del canal (hipótesis > ×3) · Short P2 (cuadros de Mario) pendiente · `limpiar` al aprobar

## Por qué este video (Claude dirige el canal desde el 6-nov-2026; plan completo en canales/formula/cronicas_gaming.md)
- PRUEBA P1 «actualidad en su pico»: el remake salió el 5-nov y domina el nicho (Mundo N ×14,5; Short de Vandal «2 SECRETOS
  ELIMINADOS del remake» 289 k en 1,5 días). Nuestro `oot_remake_cambios` tuvo el mejor arranque del canal (215 en 3 d).
- Variable que cambia respecto a oot_remake_cambios: SOLO el ángulo (lo QUITADO tras el lanzamiento, con fuentes) + título corto
  con verbo fuerte (P3). Se coló en la cola: mario64 pasó al 10-nov (BITACORA 6-nov).
- Hipótesis: > ×3 la mediana del canal a 7 días, sobre todo por búsqueda. Registro a 7 días: (pendiente, ~15-nov).
- Comentarios al empezar (6-nov): 0 nuevos, sin quejas ni sugerencias. Los 5 de ≤ 10 días ya salieron en otros videos
  (`yt comentario` los rechaza): este video NO lleva capturas; en su lugar, pregunta fuerte para comentarios (el canal tiene
  5 comentarios en 21 días: subir eso también es meta de la prueba).
- Duración: ~10 min (los de 11-15 min retienen 40-50 %; el de 15 min de Banjo, 26 %).
- Short derivado (P2): la curiosidad más fuerte, vertical, 1 día antes del largo.

## Sesiones
- alias: remake eliminado, oot eliminado, lo que eliminó el remake
- vista previa: ninguna; directo al MASTER (regla 5-nov)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión | ◐ 6-nov | estrategia del canal + cola reordenada + investigación + guion + voz + beats + OST; corte a 180 k |
| 2 | clips, medios, OST, MG, efectos, chequeo | ◐ 7-nov | 68/68 clips, 4 MG nuevos, efectos.py, promesas.md; corte a 180 k antes de fx hoja/render |
| 3 | fx hoja, promesas, render, miniatura, subida | ✅ 7-nov | promesas 21/21; arreglos: corte 046/047 y blanco del clip 038; MASTER a la tele; subido WjDK78u1ZO0 |

## Historial de la producción (cerrado el 7-nov)
- ✅ 7-nov: clips 68/68 (011 reintentado; 025 = aura verde del Bosque Perdido de Eurogamer QaJbU5MrPw4@439; 047 = puente
  levadizo del remake con cadenas, cinemáticas L45cq1H2d1s@2251; 062 = tapiz sin negro, oLHiQX2wxrE@18; 027 rebajado CON
  audio, `ambiente_por` scene-027 0,5) · `medios` (hojas medios_01-04 miradas) · 8 ventanas N64 en medios/n64/ ·
  `armar_musica_ost.py` → audio/musica.wav ✅ · `ambiente` ✅ (13 clips con sonido).
- ✅ MG NUEVOS en nucleo/mg_oot.py: lista_negra, ranuras, sangre, ofrendas + balance(titulos=, cruz=) (hoja previews/mg_nuevos.jpg).
- ✅ efectos.py escrito (102 efectos: puestos «Eliminado número N», fichas N64, ventanas con sw2=False si el cuadro grande es N64,
  pv/sil/rel/cam/leg/aba, 8 MG) · `fx --seco` OK · `chequeo` OK (fichas 2,6 · mg 3,1 · pegatinas 4,1/min, 30 entradas distintas;
  avisos de sonido = falsas alarmas: «vas a oír en el 1», Saria suena en la OST de p9, Hey! en el post de p8).
- ✅ promesas.md escrito (21 promesas). Hojas fx_01-06 revisadas ANTES de las correcciones de ventanas/legajos.
- ✅ 7-nov (sesión 3): fx hoja mirada OK · promesas 21/21 ✅ (promesas_01-02) · ARREGLO: corte 046/047 a 393,6 s (el remake
  entraba 2,8 s tarde tras «En el remake, Link resbala»; respaldo previews/_beats_antes_corte047.json) → ambiente rehecho.
  fx + mezcla ✅ (−14,25 LUFS, voz/fondo 13,9 dB) · miniatura Flow ✅ salida/miniatura.jpg (A; prompt_miniatura.md) · youtube.json ✅
  (capítulos por anclas) · render `video → final → verificar` EN MARCHA (previews/_render.log).
- Falta (antes), en orden: `fab.py oot_remake_eliminado fx hoja` y MIRAR (ventanas lupa/kaepora movidas, legajos con título corto, sin
  ventana hadas) → `previews/promesas_NN.jpg` (cuadro real de cada promesa de promesas.md) → `fx` (audio/fx.wav) → `mezcla` →
  `video` → `final` → `verificar` → `tele video oot_remake_eliminado master` (2.º plano) → `avisar` → miniatura Flow («que parezca
  el juego»: patio del remake + cuadros de Mario tachados, texto «LO BORRARON» escrito por Nano Banana) → `yt subir
  oot_remake_eliminado cronicas_gaming private --publicar 2026-11-09T00:00:00Z` → registrar en canales/cronicas_gaming.json +
  BITACORA → Short P2 (cuadros de Mario) si da tiempo.

## Lecciones (7-nov)
- Beats cortados A MITAD de frase: «En el remake, Link resbala…» caía en el beat N64 (046) y el remake entraba 2,8 s tarde. Con
  promesas que dicen «en el remake/en N64», comprobar que el corte del beat coincide con ESA palabra (`_cuadros.py` en ±2 s).
- Clips que arrancan con fundido a blanco/negro (038 = 3 s blancos, el inicio de partida nueva): la hoja `fx` no lo delata si el
  cuadro cae después; mirar el primer segundo de cada clip o medir brillo (YAVG) antes del render. Arreglo: recortar el clip
  (respaldo en medios/_respaldo/) y re-render; `--rehacer` re-renderiza TODO si `segmentos/` está vacío (~12 min).
- Flow sin Chrome: el navegador integrado sirve; ingredientes locales por base64 + canvas (cuesta ~18 k caracteres por imagen de 480 px)
  y los públicos por `fetch` de i.ytimg.com. Los cuadros de Mario los dibujó Nano Banana desde el prompt, bien a la 1.ª.

## Falta
- [ ] guion · voz · seleccionar · tiempo · beats · plan de clips · bajar · medios · pegatinas · OST · fx · promesas · chequeo
- [x] video · final · verificar · tele · miniatura Flow · subir 9-nov 00:00Z
- [ ] Short P2 · registro a 7 días
