# El cilindro vacío que seguía pesando lo mismo (teflón) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: pieza_oculta (Plastitube) · PROGRAMADO mar 3-nov-2026 13:00 CDMX (https://youtu.be/bQj_Ip4dhEo; publishAt 2026-11-03T19:00:00Z; sigue el ciclo semanal de martes)
- estilo: secuencia_flow (plastilina, SOLO imágenes de Google Flow) → docs/estilo_secuencia_flow.md · ejemplo: videos/ciempies_casa/
- etapa: SUBIDO EN PRIVADO el 7-oct-2026 → https://youtu.be/bQj_Ip4dhEo (aprobado por el usuario; miniatura «¿Y EL GAS?» de Flow; alternativa en previews/mini_b.jpg); sin fecha de publicación
- ✅ **PÚBLICO** desde el dom 25-oct 13:00 (el registro de abajo que dice 3-nov está viejo) CDMX · https://youtu.be/bQj_Ip4dhEo (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
- siguiente: el usuario decide fecha (ocupados 13, 20 y 27-oct 19:00 UTC) → `python fab.py yt publicar pieza_oculta bQj_Ip4dhEo private --programar <fecha>Z`; subir el .srt a mano en Studio o reconectar el canal (`python fab.py yt conectar`: el token no tiene permiso de subtítulos)

## Decisiones del episodio
- Pedido del usuario (7-oct-2026): video de prueba de 6 minutos, solo imágenes (Flow sin puntos de video). `video_s=0`.
- Tema elegido por Claude (no estaba en `Platitube/docs/historial-videos.md`): Roy Plunkett y el teflón (1938) → sartén de Grégoire (1956).
- 1 052 palabras, 89 frases, voz Dan. Título de trabajo; el definitivo se decide con la miniatura.

## Hecho
- Guion con ficha histórica en el docstring de `guion.py` y FICHA visual (químico, ayudante, ingeniero, esposa, cilindro).
- Voz 89/89 (CER 0 en la selección), 370,6 s; 89 beats; `hacer_prompts.py` → `prompts.json` (español, personas por oficio).
- Flow: 89/89 en proyecto nuevo «oct 07 - 14:23» (Nano Banana 2 Lite x1, ~15-20 s por imagen). Rehechas 026 (tabla periódica con letras) y 080 (paciente abierto, demasiado gráfico).
- Armado 158 s, mezcla, MASTER 175 MB + .srt, `youtube.json` en borrador.
- Música: Lyria en 3 tramos adaptada al guion (`LYRIA` en guion.py + `python ../../nucleo/lyria_tramos.py`); los 3 salieron al primer intento y la energía por escena sigue la intensidad pedida (mínimos en gancho/polvo/problema, máximo en cascada). La procedural quedó en `audio/musica_procedural.wav`. NO correr `musica`.

## Falta
- [ ] visto bueno del usuario
- [ ] miniatura, título definitivo, subida en privado y programación (el canal tiene ocupados 13, 20 y 27-oct 19:00 UTC)
- [ ] anotar el tema en `Platitube/docs/historial-videos.md` si se publica

## Cómo retomar (comandos)
```
python fab.py estado teflon_sarten
python fab.py teflon_sarten medios          hojas previews/medios_NN.jpg
python videos/teflon_sarten/_armado.py      video → sfx → mezcla → final → verificar (log en _armado.log)
```

## Archivos clave
- `guion.py` (narración + FICHA), `hacer_prompts.py`, `_ronda.py`, `_armado.py`, `beats.json`, `prompts.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- El cilindro cambia de tamaño entre tomas (termo ↔ tanque mediano) aunque la FICHA diga «del tamaño de un termo»: para el próximo, dar la medida relativa a la mano en cada prompt.
- Pedir «garabatos ilegibles» en un cuaderno está bien, pero un laboratorio sin más indicación mete tablas periódicas con letras: añadir «pared sin carteles ni láminas».
- Escenas médicas: decir «sin paciente, sin sangre, sin órganos» o Flow modela una cirugía abierta.
- `verificar` marca 4 frases con CER 2-5 % («pegas»→«peras», «enrede»→«entrete»): es Whisper bajo la música; en la selección de voz dieron CER 0.
- El motor secuencia no genera SFX (0 eventos): la mezcla es voz + música.

- 23-oct-2026: título cambiado en YouTube (sigue programado dom 25-oct 13:00 CDMX) de «El cilindro vacío que seguía pesando lo mismo» a «El ACCIDENTE que Creó el Teflón: de la Bomba Atómica a Tu Sartén» — los títulos que esconden el objeto no reciben búsqueda (diagnóstico en canales/formula/pieza_oculta.md).
