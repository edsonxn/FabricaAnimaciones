# Los 50 SECRETOS de Banjo-Tooie QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco lun 23-nov-2026 18:00 CDMX = 2026-11-24T00:00:00Z (pokemon_rojo_azul ya ocupa el 20-nov, aviso de su sesión 3-nov; confirmar con `canales --actualizar` antes de subir)
- estilo: secuencia_yt (Crónicas del gaming, kit `nucleo/mg_banjo.py`, voz Hope, OST del juego) → doc: docs/estilo_secuencia_yt.md § «Crónicas del gaming» + § REGLA DE ORO
- etapa: SUBIDO y programado lun 23-nov-2026 18:00 CDMX (https://youtu.be/waVn1g8VltA, privado)
- siguiente: revisión del usuario del MASTER; medir a 7 días; `limpiar` al aprobar


## Sesiones (plan de tramos · «continúa el video bt_50_secretos» retoma aquí · protocolo docs/sesiones.md)
- alias: banjo 50 secretos, banjo tooie 25 minutos (el 4.º de Banjo), bt_50_secretos
- vista previa: NO; el usuario pidió **una sola sesión** y ver solo el MASTER (3-nov-2026). Si salta el corte de 180k: checkpoint aquí y sesión nueva sola.
- leer al empezar: este ESTADO, docs/estilo_secuencia_yt.md § Crónicas del gaming (lecciones de bt_mundos_ranking, spyro2, n64_secretos) y § REGLA DE ORO; investigacion_secretos.md por grep
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + tiempo + beats + música OST + MG nuevos del kit | ✅ 3-nov | (cortes por contexto a 180k, retomado) |
| 2 | plan de clips por beat · bajar · medios · brillo/duración · dl_amb · pegatinas que faltan · efectos.py · fx hoja · ambiente_por + música otra vez · sfx · mezcla · chequeo · video · final · verificar · miniatura Flow · subir y programar · avisar | ✅ 3-nov | MASTER 24:49, subido waVn1g8VltA |

## Decisiones del episodio (el usuario, 3-nov-2026)
- Elegido entre 3 (historia completa / 50 secretos / lo que Rare cortó): **50 secretos**, ~25 min. Formato a anotar: `historia_y_50_secretos_secuencia_yt` → en realidad `lista_50_secretos_secuencia_yt`.
- Variable que cambia respecto a banjo_tooie (×2,46, el mejor largo): SOLO el número de secretos (10 → 50) y la duración. Mismo juego.
- Comentarios al empezar (3-nov): 0 nuevos, 0 quejas, 0 sugerencias (3 comentarios en 21 d, sin contestar).
- NO repetir lo ya contado en banjo_tooie, bt_jiggies_crueles y bt_mundos_ranking (lista «YA USADO» en investigacion_secretos.md).
- Base copiada de bt_mundos_ranking: mapas oficiales, pegatinas, sfx bt_*.mp3; `audio/ost` = junction a la OST de bt_mundos_ranking (34 pistas); `dl_amb.py` con AQ = esta carpeta.

## Pendiente para el usuario
- ⚠ s29 «el público… abuchea a Banjo» (beat 072): el audio del clip no se pudo confirmar de oído como abucheo (ambiente subido a 0,8).
- `chequeo` marca 8 frases que nombran música sin tramo con la voz callada (Atlantis, Isle O' Hags, Hag 1…): la OST de ese secreto suena debajo y con +9 dB en los silencios de s47/s35/s27.
- Densidad: pegatinas 4,6/min y MG 3,3/min (por encima del canal: 3,1 y 1,6; por debajo de la meta de 5/min); 0 tramos > 4 s sin gráfico.

## Hecho
- `investigacion_secretos.md` (50 + 10 reserva, sellos y fuentes). `guion.py`: 53 escenas, 118 frases, 3 444 palabras (~24 min).
- Pegatinas nuevas de la wiki (`bajar_pegatinas.py`) + Commons/Wikipedia (`bajar_pegatinas_wiki.py`). Faltan: portadas, Cockeye, Castle World, Gatehouse.
- OST extra en `audio/ost_extra/` (vs_hag1, cauldron, tower; Video-Game OST HQ / Gamesost). `armar_musica_ost.py`: una pista por secreto + `SUBE_DB` (+9 dB en el silencio de s47, s35, s27).

## Falta
- [ ] guion · voz · seleccionar · tiempo · beats · plan_clips · bajar · medios · brillo/duración · pegatinas · efectos · OST · SFX · ambiente · mezcla · chequeo · video · final · verificar · miniatura Flow · subir y programar · avisar

## Cómo retomar (comandos)
```
python fab.py estado bt_50_secretos
python fab.py bt_50_secretos bajar           baja lo que falte (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py bt_50_secretos medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Lecciones de este video (solo lo no obvio)
- En docs/estilo_secuencia_yt.md § «Lecciones de `bt_50_secretos`»: remapeo de beats tras regrabar, AJUSTE de negros, recorte en tupla para marcas de agua y subtítulos quemados, `_huecos.py`, `fx --sin-montaje`, y `video --rehacer` NO existe en secuencia (empalmar con `--tramo`).

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en docs/estilo_secuencia_yt.md
