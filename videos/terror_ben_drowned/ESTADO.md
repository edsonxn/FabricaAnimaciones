# BEN Drowned: el cartucho maldito — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: sin canal (PRUEBA del estilo nuevo «terror CRT» para un canal de terror en videojuegos; el usuario decide el nombre/canal)
- estilo: terror CRT (`ESTILO_VISUAL = "documental"`, motion graphics por código) → doc: docs/estilo_terror_crt.md · ejemplo: este video
- etapa: render + revisión (12-oct-2026): voz ✓ (8/8, CER ≤ 0,015, David de LogIA) · tiempo ✓ (66,9 s) · escenas ✓ · fx ✓ · Lyria ✓ · mezcla ✓ (−14 LUFS, voz +13,1 dB)
- siguiente: ver el MASTER (`salida/terror_ben_drowned_MASTER.mp4`), pedir ajustes al usuario; si gusta: nombre/canal, promover el kit a `nucleo/` y hacer un video largo

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: ben drowned, terror ben, prueba terror, cartucho maldito
- vista previa: prueba de 1 minuto, una sola sesión
- leer al empezar: docs/estilo_terror_crt.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion, voz, kit, escenas, fx, Lyria, mezcla, render | ✅ 12-oct-2026 | prueba de 67 s |

## Hecho
- Tema: BEN Drowned (creepypasta/ARG de Alexander D. Hall «Jadusable», 2010; Wikipedia). Es FICCIÓN y el guion lo dice («Todo era ficción…»).
- Voz ElevenLabs David (`0hh7H4ZVAtaGpm1VZyEN`, eleven_v4, la de LogIA) con corchetes; `falla_0` hubo que regenerarla (`--seeds 4 --solo falla_0`).
- Gameplay real (yt-dlp, `clips/`, créditos en `clips/creditos_clips.json`): MojaveMyth (vendedor), ZeldaPowerVideos (estatua), 黒毛皮 (noche en Termina).
- Música Lyria `LYRIA` de 4 escenas; SFX ElevenLabs (15 sonidos, 34 golpes) en `audio/fx.wav`.

## Falta
- [ ] que el usuario vea el MASTER y decida: ¿se sigue con el estilo? ¿canal/nombre? ¿video largo?
- [ ] avisar del riesgo de derechos de los extractos de YouTube antes de publicar nada

## Cómo retomar (comandos)
```
python fab.py terror_ben_drowned video            (render completo, ~10 min)
python _hoja.py 8 28.6 34.6 -f --out h             (hoja de cuadros; desde videos/terror_ben_drowned)
python fx_audio.py ; python fab.py terror_ben_drowned mezcla
```

## Archivos clave
- `guion.py`, `anclas.py` (palabras → segundos), `escenas.py` (`pantalla` + `cuadro`), `terror.py` (kit), `pix.py`, `fx_audio.py`, `_hoja.py`

## Lecciones de este video (solo lo no obvio)
- Mirar el tramo de cada clip de yt-dlp ANTES de anclarlo: «elegía» era un logo fijo. La contact sheet cuesta segundos.
- Flash de pantalla completa > 0,15 lava el negro (el terror vive en el negro).
- Detalles en docs/estilo_terror_crt.md § «Errores a no repetir».

## Cierre (regla del 12-oct-2026)
- [ ] (prueba: sin subir) hallazgos en docs/estilo_terror_crt.md ✓ escritos; completar con lo que diga el usuario al ver el video
