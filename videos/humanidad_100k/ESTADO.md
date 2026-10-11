# La Tierra hace cien mil años: Cuando no estábamos solos — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: sin canal (video divulgativo independiente) · sin fecha fija
- estilo: secuencia_flow (ilustración estilo Wild Next Door: tinta wobbly, color plano, imágenes fijas con cámara dirigida) → docs/estilo_secuencia_flow.md
- etapa: MASTER borrador listo (2:42 min, 162.5 s) · tramo inicial 44 s 100% ilustrado y renderizado · 11/41 medios
- siguiente: generar escenas 12-41 en Google Flow para sustituir las tarjetas del borrador

## Decisiones del episodio
- Duración: 2:42 min (162.5 s, 32 frases, 420 palabras)
- Formato visual: Ilustración dibujada en 16:9 con cámara dirigida procedural (`video_s = 0`)
- Narrador: Dan (Chatterbox en español, referencia C:/chatterbox_voices/Dan.mp3)
- FICHA: triple anclaje adaptado a prehistoria (Homo sapiens, Neandertales, Denisovanos, fauna del Pleistoceno y campamentos)

## Hecho
- Proyecto creado en disco E: con estructura completa
- Guion, voz (32/32 frases CER 0.000) y timeline (162.5 s a 96 BPM)
- 41 beats calculados y 41 prompts exportados para Flow
- 11 primeras escenas generadas directamente en alta resolución (1080p, estilo Wild Next Door)
- Música procedural compuesta por escenas y masterizada con ducking a -14.00 LUFS (-1.33 dBTP)
- Clip terminado de 44 s con audio y cámara: `salida/humanidad_100k_preview_44s.mp4`
- Video MASTER completo (162.5 s) con subtítulos: `salida/humanidad_100k_MASTER.mp4`
- Verificación técnica: CER 0.0015, desfase 0 ms

## Falta
- [ ] Generar escenas 12 a 41 en Google Flow (vía script `servir` o web)
- [ ] Renderizar el MASTER final sustituyendo las tarjetas temporales (`python fab.py humanidad_100k video` y `final`)

## Cómo retomar (comandos)
```
python fab.py estado humanidad_100k
python fab.py humanidad_100k servir
python fab.py humanidad_100k video
python fab.py humanidad_100k final
```

## Archivos clave
- `salida/humanidad_100k_preview_44s.mp4` (video final de los primeros 44 s con ilustraciones terminadas)
- `salida/humanidad_100k_MASTER.mp4` (master completo de 2:42 min)
- `previews/medios_01.jpg` (hoja de contacto de las escenas)
