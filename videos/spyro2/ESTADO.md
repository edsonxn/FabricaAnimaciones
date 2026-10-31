# Spyro 2: su historia y los 30 secretos QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco sáb 14-nov-2026 18:00 CDMX (ciclo 3 d; confirmar con `canales --actualizar`)
- estilo: secuencia_yt (Crónicas del gaming) → doc: docs/estilo_secuencia_yt.md § «Crónicas del gaming» y § SONIDO ORIGINAL
- etapa: SUBIDO y programado (https://youtu.be/BOELChGqqTg)
- siguiente: nada; medir a 7 días de publicarse


## Sesiones (plan de tramos · «continúa el video spyro2» retoma aquí · protocolo docs/sesiones.md)
- alias: spyro2, Spyro 2, Spyro 2 de PS1, Ripto's Rage, En busca de los talismanes
- vista previa: NO; el usuario eligió «todo de una vez» (encadenar tramos hasta el MASTER; aviso al terminar)
- leer al empezar: este ESTADO, docs/estilo_secuencia_yt.md § Crónicas del gaming, § SONIDO ORIGINAL y § MAPAS REALES; investigacion.md solo por grep
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación, mapas, OST, SFX, guion | ✅ 30-oct | guion cerrado y verificado: 174 frases, 3 489 palabras, 30 secretos |
| 2 | voz, tiempo, beats, plan de clips, bajar, medios | ✅ 31-oct | 174/174 clips; 39 con sonido original |
| 3 | efectos, música, sfx, ambiente, mezcla | ✅ 31-oct | 232 FX; -14,2 LUFS; voz 11,6 dB sobre el resto |
| 4 | render, final, verificar, miniatura, subir, programar, avisar, documentar | ✅ 31-oct | MASTER 24:52, 1,2 GB; programado sáb 14-nov 18:00 CDMX |

## Decisiones del episodio (el usuario, 30-oct-2026)
- 24 minutos. Elegido entre 3: **historia + secretos** (no ranking de niveles ni documental). Formato: `historia_y_30_secretos_secuencia_yt`.
- Variable que cambia: SOLO la consola/saga (PS1 en vez de Nintendo); misma fórmula que mario64_secretos con más duración.
- Gancho de actualidad: Spyro: A Realm Beyond (anunciado en el Xbox Games Showcase de junio de 2026; confirmar fecha en la investigación).
- Referencias: AtomiK.O. «107 Datos de Spyro» 104 k (25:58, es), The Leaderboard «107 Spyro Facts» 771 k (24:10), Jiggylookback «The Mysteries of Spyro 2» 17 k en 3 meses, Canadian Guy Eh «Spyro Iceberg» 130 k, Shanmania «Why is Spyro 2 so Cozy?» 790 k. En español no hay nada reciente y largo de Spyro 2.
- Comentarios (30-oct): 0 nuevos, 0 quejas, 0 sugerencias; el canal solo tiene 1 comentario en 21 días (ya usado en bt_mundos_ranking).
- Disco: `limpiar --publicados --borrar` el 30-oct liberó 10,5 GB (incluye majora_mask, público ese día a las 18:00). C: 10,1 GB, E: 11 GB. Render en C: (`salida/`, `segmentos/`, `audio/` reales) y copiar `medios/` a C: antes.

## En curso
- Nada: video cerrado el 31-oct-2026. Miniatura de Flow aplicada al subir.

## Hecho
- `python fab.py nuevo spyro2 --yt`, ideas, comentarios y panel de canales.

## Falta
- [x] Todo lo de la tabla de tramos.

## Cómo retomar (comandos)
```
python fab.py estado spyro2
python fab.py spyro2 voz
python fab.py spyro2 bajar           baja lo que falte (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py spyro2 medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `investigacion.md`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- Pausa de ~40 min por `chkdsk E:` (decisión del usuario); sin pérdidas en spyro2. Densidad de MG 1,2/min frente a 1,9 del canal; fichas 2,6 y pegatinas 2,9 por encima.
- `dl_amb.py` copiado con ruta fija tocó 33 clips de bt_mundos_ranking (anotado en su ESTADO). Lecciones en docs/estilo_secuencia_yt.md § Lecciones de `spyro2`.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
