# Short: los NPC con IA más groseros de Skyrim (serie de Embry) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · Short vertical (#Shorts, no cuenta para el hueco)
- estilo: COMPILACIÓN vertical de gameplay propio (Jugando Skyrim con IA / Mantella) + zoom a la cara del NPC + edición meme · sin voz nueva
- etapa: SUBIDO y programado (vie 20-nov 19:30 CDMX), aVWHrbiiXl4
- siguiente: cuando sea público, «Vídeo relacionado» = jG9LnSPKxPw en Studio; medir a 7 días (≈ 27-nov)

## Sesiones
- alias: short de Embry, short de los mejores momentos de Skyrim con IA
- pedido (17-nov-2026): ~90 s, vertical, muchos momentos («compilación grande, muy dinámico»), yo hablo y el NPC contesta algo gracioso, zoom a la cara de quien dice lo gracioso, edición chistosa encima.
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | fuentes → candidatos → clips → montaje (17-nov) | ✅ 17-nov | corte de contexto a 180 mil; siguió la sesión de relevo |
| 2 | revisar cuadros → render MASTER → tele → subir Short | ✅ 17-nov | MASTER 80,3 s, subido aVWHrbiiXl4 |

## Hecho (17-nov-2026)
- 13 momentos, 80,3 s, 1080x1920, −14,4 LUFS, bips sobre «chingada» (orca) y «madre» (tiktok) comprobados en el MASTER.
- Caras marcadas a mano (`MANO` en montar.py; el Haar de `caras.py` fallaba), franja esmerilada bajo nombre y remate, emoji del lado libre. «hijas» recortado a 40,8 s (la cámara del juego salta).
- Subido https://youtu.be/aVWHrbiiXl4 privado, se publica vie 20-nov 19:30 CDMX (2026-11-21T01:30Z), .srt cargado; registrado en `canales/cronicas_tamriel.json` (`"short": true`) y BITACORA. La tele no estaba prendida: aviso por voz.
- PENDIENTE en Studio: monetización (anuncios + cuestionario de idoneidad) y, cuando sea público, «Vídeo relacionado» = jG9LnSPKxPw (episodio 1 de la serie).

## Archivos clave
- `bajar_fuentes.py`, `candidatos.py`, `bajar_clips.py`, `montar.py`

## Lecciones de este video (solo lo no obvio)
- Las caras del juego no las detecta el Haar de OpenCV (cascos, perfiles, poca luz): marcarlas a mano cada 0,5 s sobre una hoja con rejilla y revisar 6 cuadros por momento antes del render. Detalle en `docs/estilo_secuencia_yt.md` § «Short de COMPILACIÓN vertical».
- En `audio()` un `for n, m in enumerate(MOM)` pisaba la `n` del largo del búfer (falló el 1.er render): nombres distintos.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO, registrado (`canales/cronicas_tamriel.json` con `"short": true`, BITACORA)
- [x] HALLAZGOS documentados
