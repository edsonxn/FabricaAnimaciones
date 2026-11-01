# BEN Drowned: el cartucho maldito que nunca existió — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · meta: ~mié 21-oct-2026 18:00 CDMX (el canal se queda sin video el lun 19-oct 18:00; atraso aceptado por el usuario el 17-oct) · hipótesis 2 de `canales/formula/cronicas_gaming.md`: misma fórmula que `sonic_exe`, cambia SOLO la leyenda
- estilo: terror CRT (`ESTILO_VISUAL = "documental"`) → docs/estilo_terror_crt.md · ejemplo a copiar: `videos/sonic_exe/` (fórmula) + `videos/terror_ben_drowned/` (tele CRT + N64) · kit `nucleo/terror_*.py`
- etapa: guion ✓ · voz ✓ (30/30, CER ≤ 0,053, 273,4 s) · tiempo ✓ (302,6 s = 5:03, 9 escenas) · comprobar ✓ → tramo 2
- siguiente: tramo 2 → clips yt-dlp con hoja de contacto (`clips/`, `creditos_clips.json`) + `anclas.py` + `escenas.py` (cartucho 0-37,7 · falla 37,7-65,1 · ahogo 65,1-82,3 · estatua 82,3-109,7 · ben 109,7-147,4 · final 147,4-168,0)

## Sesiones (plan de tramos · «continúa el video ben drowned» retoma aquí · protocolo docs/sesiones.md)
- alias: ben drowned, ben drowned completo, ben largo, cartucho maldito de zelda
- vista previa: **el usuario (18-oct) quiere ver el PRIMER MINUTO en el tramo 2, antes de seguir**, con audio completo: Lyria + `fx_audio.py` + `mezcla` ANTES de `python fab.py ben_drowned video --hasta 60`
- leer al empezar: este ESTADO.md + `docs/estilo_terror_crt.md` (+ `videos/sonic_exe/escenas.py` solo para ver `pantalla(t)`/`cuadro(t)`)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz David + tiempo | ✅ 18-oct | fuentes: Wikipedia «Ben Drowned» + ARGN (docstring de `guion.py`). `voz` 1 623 créditos (saldo ≈ 24 968); `seleccionar` 30/30 a la 1.ª toma; `tiempo` 302,6 s; `comprobar` OK. Escenas aún de plantilla |
| 2 | clips yt-dlp (hoja de contacto) + anclas + escenas 1.ª mitad (cartucho → final) + Lyria (2 tramos) + SFX del 1.er minuto + mezcla + **vista previa `video --hasta 60` con audio completo** → el usuario la revisa | ⏳ siguiente | vista previa pedida por el usuario el 18-oct |
| 3 | escenas 2.ª mitad + SFX completos + mezcla + render + final + verificar + miniatura Flow + youtube.json + subir privado | pendiente | |

## Hecho
- `nuevo` + `canales --actualizar` (18-oct). Guion de 9 escenas: cartucho, falla, ahogo, estatua, ben, final | autor, legado, cierre (giro «nada de esto ocurrió» al final de `final`)

## Falta
- [x] voz, tiempo, comprobar · [ ] el usuario lee el guion · [ ] clips + anclas · [ ] escenas · [ ] audio · [ ] render · [ ] miniatura, youtube.json, subida

## Archivos clave
- `guion.py` (hechos verificados en el docstring, LYRIA de 2 tramos) · `ref_david.mp3`

## Lecciones de este video (solo lo no obvio)
- es.wikipedia no tiene artículo «Ben_Drowned» (404); Fanlore y Boing Boing dan 403 a WebFetch: bastaron en.wikipedia + ARGN.

## Cierre (regla del 12-oct-2026)
- [ ] subido, miniatura, programado y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [ ] HALLAZGOS documentados en docs/estilo_terror_crt.md
