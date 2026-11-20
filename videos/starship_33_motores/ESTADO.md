# ¿Por qué Starship tiene 33 motores? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: T Menos Cero (`t_menos_cero`) · 3.er video · hueco sáb 21-nov-2026 (ciclo 5 d, hora del canal 13:00 CDMX) · una sesión directo al MASTER
- estilo: LÍNEA 3D + VIDEO REAL de cada suceso + fotos en marcos de alambre · copiar `videos/starship_sin_patas/` · doc `docs/estilo_linea3d.md`
- etapa: ✅ SUBIDO y PROGRAMADO sáb 21-nov-2026 13:00 CDMX: https://youtu.be/w7tACvGPLF0 (privado + publishAt, miniatura Flow + .srt) · MASTER 9:00, −14,33 LUFS, CER 0,0034, desfase 0; blackdetect: solo planos de líneas sobre negro (con contenido, comprobado)
- siguiente: visto bueno del usuario · medir a 7 días (≈ 28-nov) · al aprobar `python fab.py starship_33_motores limpiar`
- NO tocar el texto del guion: las anclas `ww` dependen de él

## En curso (20-nov-2026 ~08:30, sesión 1 cortada por contexto a los 180 mil)
- HECHO: datos.md (fuentes + lista de lo DUDOSO que no se dice) · guion.py 84 frases (corchetes sobrios) · voz ✅ · seleccionar ✅ · idioma ✅ · tiempo ✅ 540,5 s ·
  música ✅ (`audio/musica.wav`: biblioteca sin_patas t3/t2, vuelo15 t6/t1, sin_patas t5) · 22 clips en `clips/` (crédito y lista en `_clips.py`) ·
  fotos en `imagenes/` (f1_vonbraun, n1_pad, raptor_merlin, fh, fh2, musk; créditos en `imagenes/creditos.json`; musk = Commons «Elon Musk Colorado 2022 (cropped2)» copiada de sin_patas).
- Hojas de contacto: `python _contacto.py <clip> <paso> [t0 t1]` → `previews/c_<clip>.jpg` (lanzadas en 2.º plano para todos los clips 08:25).
- Segundos ya vistos: `b7` estática 20-36 s (amplia), cámara lenta 108-130, tarjeta del tuit de Musk «31 engines… still enough to reach orbit» 40-52 ·
  `f10mesa` motores desde abajo 6-24 (¡para «Mira la base»!) y 54-60, ascenso 66-72 · `f1` (vuelo 1, SpaceX) despegue 52-60, cohete girando 84 y 104, explosión 120 ·
  `f2sep` separación en caliente 0-15, se separan 45-60 · `a11` (Apolo 11, cámara E-8) motores F-1 encendiendo en cámara lenta 108-153 (antes humo/llamas 18-99).
- 20-nov ~09:30: ESCRITOS `comun.py` (CLIPS/CREDITO nuevos, `panel33`, `IDX`, `contador`), `planos1.py` (hoja `previews/h_p1.jpg` OK salvo: a_3d cámara lejos, n1 seg 0 = rótulo inglés, f1mot seg, mesa_desp=54 pantalla partida), `planos2.py`, `planos3.py`; `SEG` de cada planos = segundos de clip a AJUSTAR con el informe del subagente de hojas.
- Falta EN ORDEN (lo de abajo ya hecho hasta planos): ver el resto de hojas (n1, n1b, crs1, orbcomm, f15ap, s1c, f1mot, mcg, r3, r3b, fh, fabrica, f5 70-170, f15 330-470, f1b, f2b) →
  escribir `comun.py` (CLIPS/CREDITO de los clips nuevos; quitar geografía de Starbase si no se usa) + `planos1.py` (gancho, raptor, anillos, saturno),
  `planos2.py` (n1, falcon, fallas, fabrica), `planos3.py` (aterrizaje, vuelos, nave, contras, cierre) copiando el patrón de `_ref_planos1/2.py`
  (rp(), con_foto(), foto(), panel de 33 motores tipo `starship_vuelo15/comun.py:panel_sh`) → regla: video real en cada suceso, nunca > 30 s de 3D seguido →
  `promesas.md` + hojas `_hoja.py` → SFX (`SFX_ELEVEN` ya en guion.py; `sfx()` en cada planos) → `fab.py starship_33_motores sfx`, `mezcla`, `video`, `final`, `verificar`,
  `blackdetect` → `avisar` → miniatura Flow («33 MOTORES», base del Super Heavy encendida) → youtube.json (título 40-55 c.) → `yt subir … private --publicar` sáb 21-nov 13:00 CDMX (19:00 UTC) → BITACORA, canales json, commit.
- Tema elegido por el usuario en «buenos días» (20-nov): ref. The Space Race «The Real Reason Starship Has 33 Engines» (×2,04, ~2 M).
- `_ref_planos1.py`/`_ref_planos2.py` = planos del video anterior SOLO como referencia de código (no reciclar escenas); se borran al final.

- 20-nov ~10:15: RENDER en 2.º plano (mezcla→video→final→verificar, log `_render.log`); miniatura Flow encargada a un subagente (→ `miniatura/miniatura.jpg`, prompt en `prompt_miniatura.md`).
- Tras el render: `blackdetect` del MASTER (regla linea3d) → `avisar` → `yt subir starship_33_motores t_menos_cero private --publicar 2026-11-21T19:00:00Z` → `canales/t_menos_cero.json` publicados + BITACORA + ESTADO cerrado + `biblioteca sfx catalogar` + commit. Borrar `_ref_planos*.py` al cerrar.

## Sesiones
- alias: 33 motores, starship 33 motores, por qué 33 motores
- leer al empezar: este ESTADO + docs/estilo_linea3d.md

| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | datos + guion + voz + clips + fotos + planos + promesas + música/SFX + render + miniatura + subida | ✅ 20-nov | una sesión (pasó el corte de contexto; el relevo no se pudo abrir por Remote Control): todo hasta subido y programado |

## Lecciones
- Hojas de contacto de los clips por un subagente (`_contacto.py`): ahorra mucho contexto; los SEG de cada `planos*.py` se ajustan con su informe.
- blackdetect marca los planos de líneas sobre negro (≥ 97 % negro): comprobar brillo máximo antes de dar por malo un tramo.
- `_fotos.py` viejo llevaba datos personales en el User-Agent: usar `_commons.py` (UA genérico, pausa de 6 s: Commons da 429).
