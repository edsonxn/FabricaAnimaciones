# Las 10 cosas que DEBES hacer la primera semana de WoW Forever — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · PROGRAMADO dom 1-nov-2026 09:00 CDMX (abre la campaña Overgear de nov: 1, 4, 5, 7 y 9-nov) · https://youtu.be/zYCcRMQ_t2I
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + MG + mapas + Overgear kit Forever) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ subido y programado (14:56, miniatura + .srt) · falta la monetización en Studio (usuario)
- siguiente: revisión del usuario; si pide cambios → `video --rehacer t0-t1` + `final` (segmentos conservados) y re-subir

## Sesiones (plan de tramos · «continúa el video primera semana» retoma aquí · protocolo docs/sesiones.md)
- alias: primera semana, 10 cosas primera semana, video del 1 de noviembre, el que abre la promo
- vista previa: no (como jugadores_rompieron): MASTER y aviso
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | tema + investigación + guion + tarjetas de comentarios | ✅ 28-oct | 16 candidatos con fuente; 12 tarjetas `pegatinas/com_*.png` |
| 2 | voz Applio + tiempo + beats + busquedas.json + bajar + medios | ✅ 28-oct | 129 frases, 102 beats, 19 clips rehechos tras revisar hojas |
| 3 | efectos + OST + mezcla + render + final + verificar + subir | ✅ 28-oct | CER medio 0,007; zYCcRMQ_t2I programado con `--forzar` |

## Decisiones del episodio (el usuario, 28-oct-2026)
- tema: opción 3 de 3 («suena a algo que todo jugador de Forever tiene que ver») · mínimo 14 min · cuenta regresiva de 10
- Overgear campaña 2 (coaching de Forever, CRONICAS10, kit «WoW - Forever (nov)» + creativo `CRONICAS10_forever.mp4`) tras el n.º 8; sin «descuento mayor»
- FUERA «no compres oro» (Overgear vende oro): n.º 5 = recolectar y ahorrar para la montura (regla en docs/migracion_googleimagenes.md)
- DOBLE de mapas/MG/pegatinas: 7 mapas con ruta, 15 MG (4 nuevos en mg_wow: relojes, capas, botin, mudanza; + calendario, experiencia, reglas, nombre), ~46 pegatinas + 13 comentarios
- antes de la despedida: ANUNCIO de que las historias contadas (Darrowshire) se mudan a otro canal; video largo en preparación; sin nombrar canal
- Comentarios: queja repetida = voz IA (♥14), reportada al usuario, no se cambia

## Cómo retomar (comandos)
```
python fab.py wow_primera_semana video --rehacer 270-280   luego final + verificar
python fab.py yt subir wow_primera_semana cronicas_warcraft private --publicar 2026-11-01T15:00:00Z --forzar
```

## Archivos clave
- `guion.py`, `efectos.py`, `busquedas.json` (clips fijados), `musica_wow.py`, `youtube.json`, `prompt_miniatura.md`, `videos/_investigacion_wow_primera_semana.md`

## Lecciones de este video (solo lo no obvio)
- Fijar un clip va en `busquedas.json` (`url`/`desde`/`_archivo`), no en `beats.json`: `bajar` ignora lo de beats.
- Para quitar una idea del guion sin romper beats: reescribir las frases EN SU SITIO (mismo id) + `reajustar`, nunca borrar frases.
- Wowpedia da 520 y wiki.gg corta scripts: pegatinas con timeout corto, iconos de zamimg y páginas de wiki.gg una a una.
- Densidad que pidió el usuario en ~15 min: ≥ 6 mapas, ≥ 14 MG (contadores en vez de tarjetas sueltas), ~45 pegatinas + comentarios.
- Whisper marca CER alto en nombres ingleses (Lokmodan, Seipers Terrace): son de transcripción, no de voz; se aceptan con CER_MAX_POR_FRASE.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO dom 1-nov 09:00 CDMX, miniatura y registrado (`canales/cronicas_warcraft.json`, BITACORA)
- [x] HALLAZGOS documentados (docs/estilo_secuencia_yt.md §2b comentarios + MG nuevos; migracion_googleimagenes.md oro)
- [ ] monetización en Studio (usuario): https://studio.youtube.com/video/zYCcRMQ_t2I/edit
