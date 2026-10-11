# Batman vs. el Guasón (animación fumada) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: SIN CANAL (prueba del camino «secuencia con efectos») · sin fecha
- estilo: secuencia_fx, «animación fumada / sin presupuesto» (dibujos mal hechos a propósito, Flow) → docs/estilo_secuencia_fx.md
- etapa: MASTER listo (7-oct-2026), revisado cada 3 s; falta que el usuario lo vea y escuche
- siguiente: esperar comentarios del usuario; arreglos: editar efectos.py o rehacer un dibujo → `video` → `final`

## Decisiones del episodio
- Audio: el sketch de Sociedad Nokkoi tal cual (`fuente/sociedad_nokkoi.mp4`, 3:00, descargado por el usuario el 7-oct-2026). `AUDIO_EXTERNO`.
- Todo imagen (video_s=0), 16:9 (el motor es horizontal; el original era vertical), un dibujo cada ~3,2 s, corte seco.
- Personajes descritos con apodo (MURCI, PAYASO, SUPER, CHICO), sin nombres de marca. Chiste final sugerido, no dibujado.
- Es audio de terceros: antes de publicarlo en cualquier canal, preguntar al usuario (derechos / permiso de los autores).

## Hecho
- `tiempo`: 64 frases, 373 palabras (voz/transcripcion.json, Whisper large-v3). `beats`: 56 beats.
- `hacer_prompts.py` → prompts.json (56). Prueba de estilo en Flow: aprobada tras quitar «white paper look» (dibujaba marco blanco).
- `efectos.py`: 33 efectos, 3 rótulos (¡BOOM!, CENSURADO, FIN), 27 sonidos; 23 SFX de ElevenLabs en `sfx/` (975 créditos).
- `mezcla`: -14,9 LUFS, voz/fondo 10,7 dB (con `fx=-6 dB` por defecto).

## Falta
- [x] 56/56 dibujos de Flow (proyecto «oct 07 - 14:05», Nano Banana 2 Lite, ~1 por minuto, 0 puntos). `salida/guason_fumado_MASTER.mp4` (3:00, 1080p, 90 MB).
- [ ] El usuario no ha ESCUCHADO la mezcla: los niveles de SFX se fijaron por medición (voz/fondo 10,7 dB), no de oído.
- [ ] Detalle conocido: scene-008 trae la palabra «CHICO» escrita en el papel. Versión vertical: no existe (el motor es 16:9).

## Cómo retomar (comandos)
```
python fab.py estado guason_fumado
python fab.py guason_fumado medios
python fab.py guason_fumado fx --seco
python fab.py guason_fumado video
python fab.py guason_fumado final
```

## Archivos clave
- `guion.py` (FICHA de estilo y personajes), `hacer_prompts.py` (una escena por beat), `efectos.py`, `sfx/`, `voz/transcripcion.json`

## Lecciones de este video
- El puente `servir` lee `flow/escenas.json` al arrancar: si cambian los prompts hay que reiniciarlo.
- «sausage finger» lo dibuja como salchicha literal; «white paper look» mete marco blanco.
- ElevenLabs entrega los SFX muy fuertes: sin el recorte `fx=-6` la voz quedaba solo 4,7 dB arriba del fondo.
