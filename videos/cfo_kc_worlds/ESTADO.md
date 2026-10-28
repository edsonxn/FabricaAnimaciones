# CFO vs KC: todo lo que debes saber antes del partido (Worlds 2026, ~15 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Crónicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; subida por Studio en el navegador, NO está en la API) · publicar jue 29-oct-2026 por la mañana (partido 14:00 CDMX)
- estilo: análisis táctico como `ig_lyon_worlds` (secuencia_yt + VOD + telestrador `mg_tactica` + `mg_lol` + 3D) → doc: docs/estilo_analisis_tactico.md
- etapa: ✅ SUBIDO por Studio y PROGRAMADO jue 29-oct-2026 10:00 CDMX · https://youtu.be/NO9hRcIKTQw (MASTER v2 corregido, 15:01) con miniatura «¿QUIÉN SE VA?», 14 etiquetas, «no para niños», anuncios + mid-roll, idoneidad «Nada de lo anterior», .srt español PUBLICADO
- siguiente: al aprobarlo: `python fab.py cfo_kc_worlds limpiar` y `biblioteca catalogar` (Lyria nueva)

## Sesiones (plan de tramos · «continúa el video cfo_kc_worlds» retoma aquí · protocolo docs/sesiones.md)
- alias: CFO vs KC, previa de CFO-KC, ligoleyen de CFO
- vista previa: NO (como IG-LYON: directo al completo); voz JC y Lyria/biblioteca «igual que Worlds»
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + jugadas + render + subida | ✅ 28-oct | MASTER v1 → revisión del usuario (anillos, rutas, saltos tras pausas, narradores lentos) → v2 corregida → subida https://youtu.be/NO9hRcIKTQw programada jue 29-oct 10:00 |

## Decisiones (el usuario, 28-oct-2026)
- previa de CFO vs KC «similar al de IG vs LYON», 15 min; se sube el MISMO día del partido → la voz dice «hoy a las 2 de la tarde».
- jugadas: MÁS flechas, la estrategia de CADA jugador, pausas, REPETICIONES para ver la intención, y la RUTA que hizo cada
  jugador en la jugada con su intención (rastreador nuevo del minimapa: `nucleo/tactica3d/rastrear.py`).

## En curso (checkpoint 28-oct)
- `nucleo/tactica3d/rastrear.py` (nuevo): detecta los iconos del minimapa con HoughCircles (×3), reparte con Data Dragon
  (Hungarian) y sigue con parecido propio + búsqueda local. Borrador: revisar la hoja y limpiar a mano.
- Datos: investigacion/datos_cfo.md + datos_kc.md (agentes, 28-oct). Narración de las jugadas: Whisper large-v3
  (investigacion/narrar.py → j*_narr.txt; YouTube da 429 a los subtítulos). j5 (VOD en español) alucina tras 49 s.
- Fuentes de jugada en medios/_fuente/: j1 TL-CFO (FATvv4Lk7IU desde 2470; reloj = t + 2000), j2 triple de Rest (desde 2630),
  j3 T1-CFO (cmct78Iytg8 desde 2010; + 1412), j3b Doggo-Doran (desde 1075; + 477), j4 KC-AL (8txB9yg9FNc desde 1750; + 1422),
  j5 C9-KC J4 (2xC2Jpk_duM desde 2640; + 2131).
- Rutas: `nucleo/tactica3d/fichas_inicio.py` (hoja con cada icono del minimapa numerado + iconos de Data Dragon) → posiciones a
  mano en 5-6 momentos por jugada; el rastreo automático confunde iconos en las peleas.
- MG nuevo `mg_lol.duelo` (cara a cara por posición).
- Repeticiones: cada jugada tiene escena «<jugada>_rep» (pre 8,5 s sin voz) con cámara lenta/zoom o la repetición oficial.
- Rutas: `RUTA()/ruta()` en efectos.py y `RUTA()` en mesas_3d.py llevan posiciones medidas en cuadros anteriores al cuadro de la
  pausa con la cámara compensada (investigacion/cam_j*.json, `rastros_vod.camara_clip`). Intención = flecha discontinua.
- ver.py = cuadros sueltos del video con su capa de efectos (python ver.py salida.jpg t1 t2 …), mucho más barato que `fx hoja`.
- youtube_texto.md listo (título, descripción con capítulos, etiquetas).
- 28-oct (revisión del usuario, 1.er MASTER): anillos mal puestos (medidos en hojas 2×2 / pies = placa + 0,07), rutas con puntos
  estimados y cruzando cortes, saltos de tiempo tras pausas/mesas, y 3 tramos en vivo estirados (narradores lentos). Corregido:
  todo medido de nuevo con rejilla2.py (UN cuadro), rutas solo medidas en la misma toma, VOD continuo (comprobado con ver.py en las
  uniones), scene-041/066/080 recortados de medios/_fuente. E: lleno: borrados intermedios par/fix/hoy de ig_lyon y lol_worlds.
  Re-render completo en curso (trozos en %TEMP%/cfo_kc_par).
