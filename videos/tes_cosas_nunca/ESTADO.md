# Las 20 cosas que NUNCA debes hacer en Skyrim — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · PROGRAMADO mar 03-nov-2026 12:08 CDMX (2026-11-03T18:08:00Z) · https://youtu.be/GDT4s9U9kPs (privado)
- estilo: secuencia_yt (gameplay Skyrim por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · voz Chatterbox Sarcastica · música OST oficial de Skyrim → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: subido y programado (cerrado 27-oct-2026)
- siguiente: nada; al publicarse, `canales --actualizar` lo marca público. Respuestas a los 3 comentarios: borrador pendiente del visto bueno del usuario

## Sesiones (plan de tramos · «continúa el video tes_cosas_nunca» retoma aquí · protocolo docs/sesiones.md)
- alias: cosas nunca, 20 nunca, tamriel nunca · vista previa: 🎞 Montaje del panel, sin render parcial (aviso al tener el MASTER)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 27-oct): UESP + guion + voz + beats + clips + pegatinas + MG + mapas + OST + mezcla + render + rigor + miniatura + subida | ✅ 27-oct | 19:13 con pantalla final; subido y programado mar 03-11 |

## Decisiones del episodio (27-oct-2026)
- tema elegido por el usuario entre 3 con datos: «Las 20 cosas que NUNCA debes hacer en Skyrim». Repite el gancho ganador
  (tes_misiones_nunca: 19 781 vistas en 5 días, ×9 la mediana de 2 221) y cambia UNA variable: ACCIONES del jugador, no misiones.
  20 puestos para pasar de 16 min. Ref. de fuera: SmackerUnknown «Most Hated Quest» ×6,6, Arca do explorador ×425.
- excluido (ya salió en el canal): todo lo de misiones_daedricas, misiones_nunca, exploits_rotos, cosas_inutiles y armas_poderosas.
- comentarios reales enseñados: @DavidSanchez-nz2cb (gancho), @federicoherrera2105 («jarl» → «yarl»), @manuelulloa4748 (Fus Ro Dah a Delphine).
- formato anotado: `lista_20_nunca_hacer_secuencia_yt`
- disco: E: dio NTFS 55/130 el 27-oct 15:28-15:30 → audio/previews/salida/segmentos/voz son carpetas REALES en C: (no junctions)
- fecha: `canales` daba el lun 02-11, pero quedaba a 72 h de armas (separación 96 h): `yt subir` lo detuvo → mar 03-11, sin --forzar.

## Hecho
- guion 150 frases verificado en UESP · voz 150/150 (PNJ → «personajes») · 132 beats · 132 clips (45 rehechos)
- 4 MG nuevos en mg_tes (plazo, paciencia, escalado, reinicio) + mapa de la resaca de Sanguine con fotos · 55 pegatinas + 3 comentarios
- nucleo/comentarios.py: emojis a color en las tarjetas (antes salían cuadritos)
- OST: 20 pistas nuevas de Jeremy Soule (armar_musica_ost.py, 21 secciones); sonido original en 11 beats (4 con narrador fuera)
- mezcla −14 LUFS, voz 12 dB sobre música · MASTER 1153 s · rigor (_rigor.py) sin bloqueos · miniatura Flow v1 · .srt
- subido privado + programado, miniatura y .srt aplicados, monetización activada en Studio («Adecuado para anuncios», mid-rolls)
- BITACORA, canales/cronicas_tamriel.json (publicados), `canales --actualizar`, `biblioteca sfx catalogar`, lecciones en docs

## Cómo retomar (comandos)
```
python fab.py continuar tes_cosas_nunca
```

## Lecciones de este video (solo lo no obvio)
- Chatterbox lee las siglas («PNJ» → «puenche»): escribirlas enteras.
- Clips malos de tipos nuevos: cartoon de fans, sketches con actores, forja y maquetas reales, otro juego (Uncharted), pantallas
  de carga inventadas, temporizador de speedrun, clip más corto que el beat.
- 4 de 15 clips con sonido traían narrador: `_sonido_original.py habla` ANTES de la música.
- Un MG de lista que tape > 30 s el gameplay es demasiado: cortarlo por la frase clave.
- Con el panel del navegador oculto, Studio no responde a clics por coordenadas: clic por `ref` (read_page) o JS.
