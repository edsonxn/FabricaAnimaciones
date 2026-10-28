# IG vs LYON: todo lo que debes saber antes del partido (Worlds 2026, ~12 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Crónicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; subida por Studio en el navegador, NO está en la API ni en canales/*.json)
- estilo: análisis táctico (secuencia_yt con clips del VOD + telestrador `nucleo/mg_tactica.py` + `mg_lol` + mesas 3D) → doc: docs/estilo_analisis_tactico.md
- etapa: ✅ SUBIDO por Studio y PROGRAMADO mié 28-oct-2026 10:00 CDMX · https://youtu.be/xP4IKYzFf5A (v2 «hoy»; 12:55, 737 MB, −14,2 LUFS) con miniatura, .srt, monetización (mid-roll, «Nada de lo anterior»), 14 etiquetas
- siguiente: nada (cerrado). Al aprobarlo: `python fab.py ig_lyon_worlds limpiar`

## Sesiones (plan de tramos · «continúa el video ig_lyon_worlds» retoma aquí · protocolo docs/sesiones.md)
- alias: IG vs LYON, previa de IG-LYON
- vista previa: NO (el usuario, 27-oct: «directo al completo»); voz y música «igual que Worlds»; publicar por Studio programado 10:00
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + jugadas + render + subida | ✅ 27/28-oct | MASTER 12:55 (2 arreglos: cierre y placas «sin Destello»); 28-oct: «mañana» → «hoy» (7 frases + 2 placas, render_par3.py solo de los tramos con voz nueva) y subida nueva: https://youtu.be/xP4IKYzFf5A (la v1 Who8udd68Rw decía «mañana»; la borró el usuario) |

## Decisiones (el usuario, 27-oct-2026)
- video de 12 min para gente que NO conoce a IG ni a LYON: historia, trayectoria, mejores jugadores, mejores jugadas, una razón para verlo.
- jugadas con MÁS pausas, líneas, rutas y flechas que en lol_worlds_2026, para entender posicionamiento y estrategia.
- avisar que ese mismo día a las 14:00 (centro de México) juegan T1 vs Movistar KOI. IG-LYON es DESPUÉS: 17:00 CDMX (API oficial),
  o antes si T1-KOI acaba pronto.

## En curso (checkpoint 27-oct 18:30)
- investigacion/datos.md = datos verificados con URL (agente). Jugadas: muertes y reloj del feed oficial
  (scratchpad muertes.py) + subtítulos de los VOD (investigacion/*.en.vtt) + cuadros con rejilla (rejilla.py → previews/cuadros/).
- Fuentes de jugada en medios/_fuente/ (¡medios/ está en C:, no es junction!): j1 = IG-HLE VOD rxkYf8BOHSQ desde 1840 (reloj = t + 1377),
  j2 = TSW-IG mva8OALSadc desde 1700 (reloj = t + 1254), j3 = LYON-TSW feWyEjzJmKc desde 1280 (reloj = t + 881),
  j4 = LYON-GEN G1 zNTyYcB20Mg desde 2360 (reloj = t + 1939).
- Momentos (t del clip): j1 Paranoia 86, Kanavi cae ~89, JiaQi cae ~95, Olaf «CC IMMUNE» 99, Guma cae ~102, Olaf STUNNED 107,
  doble 110, triple ~115, CUÁDRUPLE ~120, ace 124. j2 pausa 100 (22:34), Paranoia 104, pelea 110, ONDA DE CHOQUE ×4 113, Pun cae 116,
  Bie 124, Barón ~166. j3 Heraldo 70 (15:51), Paranoia 74, Bie cae 78, TP de Pun 84, Hizto 90, Dire 96, Pun 99 (doble).
  j4 contexto 104 (34:03, +3,0K), Saint entra 118, posiciones 128, Gen.G sobre el dragón 138, Inspired entra 141, Guardia 145,
  Chovy cae 149 (Dhokla), Ruler/Duro (Berserker) ~152, nexo ~205.
- recursos.py = fotos de jugadores/logos (API getTeams) + Data Dragon 16.21.1 → pegatinas/, iconos/, splash/.

## Render (27-oct 19:45)
- render_par.py (6 tramos, 13 min) → par_0..5; arreglos: render_par2.py (520-774.55 en 6 piezas fix_0..5) y fix_2 otra vez
  (606.67-650); salida/lista2.txt = par_0..3 + fix_0..5 → video_sin_audio.mp4 → final. Ojo: render_par2.py concatena mal
  (lista vieja): usar lista2.txt.
- Música: Lyria NUEVA (7 tramos; la biblioteca solo ofrecía la del video de la Worlds, mismo canal). Catalogar al cerrar.
- Menores sin arreglar: etiqueta «IG RETROCEDE» de la mesa j1 sale un poco por la derecha.

## Lecciones (28-oct)
- La voz decía «mañana» pero el video sale el MISMO día del partido: al escribir el guion, fechar desde el día de PUBLICACIÓN, no desde el de producción.
- Cambiar palabras en frases sueltas no mueve las escenas (van ancladas a compases): `voz` → `seleccionar` → `tiempo` → `reajustar` → `lyria armar` → `fx` → `ambiente` → `mezcla`, y re-render SOLO de los tramos con voz nueva (render_par3.py: 8 piezas, 7 min). Revisar clips de beats que crecen (`bajar N --url --desde` con la misma fuente).
- Studio: la descripción larga tecleada congeló la pestaña; con `execCommand('insertText')` por JS entra al instante. Escape en las etiquetas CIERRA el diálogo (el borrador queda; «Editar borrador»).
