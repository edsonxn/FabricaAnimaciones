# trailero_parada2 — edición TikTok de video REAL (sin canal)

- **Qué es:** edición vertical 1080x1920 de `clips/crudo.mp4` (trailero, 2.ª parada, 53 s → 44,7 s). Referencia de estilo: `Downloads/referencia.mp4` (título con palabra en color, rótulos de énfasis, memes).
- **Estilo/motor:** NO usa el núcleo. Todo en `editar.py` (OpenCV + PIL): tabla `SEG` (montaje con velocidades y congelados), `CAM` (zooms de corte), `rot(...)` (rótulos anclados al segundo del crudo), `CHECK` (checklist), `son(...)` (SFX). `T(seg, s)` convierte segundo del crudo → salida.
- **Hecho (7-oct-2026):** gancho en frío («¿no me descargaron nada?»), silencios cortados, 3 tramos en cámara rápida, 37 rótulos, checklist PARADA 2 DE 3, 14 SFX de ElevenLabs (171 créditos, `sonidos.py`), música Lyria (`audio/lyria.mp3`), máster a -14 LUFS, voz/fondo 11 dB.
- **Entrega:** `salida/trailero_parada2_MASTER.mp4`.
- **Pendiente:** que el usuario lo vea/oiga (la mezcla se revisó solo con medidores). Confirmar que la ciudad de la etiqueta es «ASSONET, MA» (Whisper oyó «Azonet»); se cambia en `etiqueta_tarima()`.

## Comandos (desde esta carpeta)
```
python editar.py tiempos          tabla del montaje
python editar.py hoja 1.3 12.5    cuadros de prueba -> previews/hoja.jpg
python editar.py audio            solo la mezcla
python editar.py                  mezcla + render (~4 min)
python sonidos.py                 regenera SFX/música que falten (borra el mp3 para rehacerlo)
```

## Lecciones
- Texto de énfasis: y≈1330-1420 si la cara va arriba; y≈490 si la cara va abajo (cabina). Si tapa la boca, mover `cy` de `CAM`, no el texto.
- Fuente 576x1024: no pasar de zoom ~1,4 (se ablanda).
- Sin subtítulos completos: solo palabras clave (regla global).
