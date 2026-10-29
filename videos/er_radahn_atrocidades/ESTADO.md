# Las 5 peores atrocidades de Radahn QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · meta: hueco del canal tras Melina (dom 01-11) → jue 05-11-2026 10:00 CDMX (confirmar con `canales --actualizar`)
- estilo: secuencia_yt (gameplay de Elden Ring por beat + PEGATINAS + pant() + MG NUEVOS `nucleo/mg_er.py` + mapas; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md § Runa Caída
- etapa: programado (subido private el 29-oct con miniatura, publishAt 2026-11-05T16:00:00Z; .srt sin cargar)
- siguiente: nada; a los 7 días comparar con Miquella/Melina (canales/formula/runa_caida.md)

## Sesiones (plan de tramos · «continúa el video radahn» retoma aquí · protocolo docs/sesiones.md)
- alias: radahn, atrocidades de radahn
- vista previa: MASTER directo; el usuario lo revisa al avisar (regla 24-oct)
- el usuario eligió hacerlo TODO EN UNA sesión (28-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz Faraon + seleccionar + tiempo | ✅ 28-oct | 118/118; FONETICA Miquella «Mikéla», Mohg «Móg» |
| 2 | beats, plan de clips, pegatinas, pant(), mapas, fichas/MG mg_er NUEVOS | ✅ 28-oct | 170 beats, 30 rehechos; lanzas/cielo_sujeto/balanza/espejo |
| 3 | música OST, SFX, mezcla, render, revisión, miniatura, subida private + programar | ✅ 29-oct | MASTER 24:38 sin negros; https://youtu.be/Uuj8Bw45-fs |

## Decisiones del episodio (28-oct-2026, elegidas por el usuario)
- tema: Radahn (de 4 propuestos: Radahn, Mohg, Gideon, Godfrey); duración: AL MENOS 22 min (≈ 3 900-4 100 palabras)
- Comentarios: `yt comentarios` da 403 (token sin force-ssl) → leídos con yt-dlp (67, de Miquella/Ranni/Malenia/Radagon) y guardados en
  canales/comentarios/runa_caida.json. Quejas: ~10 de la voz IA / pronunciación («Mojé», «Miqueya», «Micuela»): cuidar FONETICA de Mohg
  y Miquella (se reporta al usuario, no se cambia la voz). Sugerencias: @ConkerLord22 pide Radahn y Morgott; @zoharysakiyamablue471 (♥4)
  bromea con «el día que publiques las atrocidades de Radahn…» → gancho. @dinobotstrafe7963 (♥8): no hay confirmación de si Radahn
  aceptó ser consorte → se dice como teoría. Agradecimientos (≥ 4): @Pipo12580, @hectoryee469, @barialfx, @jimmyrobinsongalan1665, @maknarth.
  Tarjetas ya en pegatinas/com_<id>.png (9).

## En curso
- (nada: video cerrado el 29-oct)

## Hecho
- MASTER 24:38 (3 renders: negro de 1,5 s en 021 tras volver a bajarlo con audio; «se curaron» por «se juraron» en p5b_3;
  diálogos estáticos 084/087/134 cambiados) · subido https://youtu.be/Uuj8Bw45-fs, programado jue 5-nov 10:00 CDMX
- voz 118/118 (24:18): FONETICA Miquella «Mikéla» (antes «Mikuéla» = «Micuela», la queja), Mohg «Móg»; p1_8 reescrita para que
  «Mohg» vaya ante vocal (ante consonante salía «mock»); umbrales por frase y tomas elegidas (voz/_descartes)
- 170 beats; clips del plan_frases (subagente) → asignar_clips.py → bajar; 27 rehechos tras mirar las hojas (diálogos estáticos de
  Stratek repetidos, menú, Seluvis donde va Ranni, negro en 155); recorte .09 en 23 de Shirrako; ambiente_por 021/024/095
- música OST (armar_musica_ost.py) · fx: 171 efectos + 6 SFX (ElevenLabs cuenta 2: la 1 tiene pago fallido) · mezcla −14,2 LUFS
- carpeta creada (`nuevo --yt`), comentarios leídos y 9 tarjetas
- investigacion.md (subagente, wikitexto fandom en/es) · OST oficial en audio/ost/ · guion.py (28-oct)

## Lecciones de este video (solo lo no obvio)
- «Mikuéla» suena «Micuela» (la queja): «Mikéla». Mohg ante consonante = «mock»: ponerlo ante vocal
- Stratek (diálogos): mismo plano estático por capítulo → máx. 1-2 por puesto
- Medir brillo tras CADA `bajar --rehacer` (el clip con audio empezaba en fundido a negro)
- Sin permiso force-ssl, `yt-dlp --write-comments --skip-download` lee los comentarios públicos (id, autor, avatar, ♥) sin API

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/runa_caida.json`, BITACORA)
- [x] HALLAZGOS documentados → docs/estilo_secuencia_yt.md § Runa Caída, canales/formula/runa_caida.md
