# Las 8 misiones daédricas PROHIBIDAS de Skyrim — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · PROGRAMADO jue 15-oct-2026 09:15 CDMX (2026-10-15T15:15:00Z) · https://youtu.be/O2ZsE2AFGYc
- estilo: secuencia_yt (gameplay Skyrim por beat + MG de interfaz de Skyrim `nucleo/mg_tes.py`) · voz Chatterbox Sarcastica → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: subido (private + programado)
- siguiente: subir el .srt a mano en Studio (el token no tiene youtube.force-ssl) o `python fab.py yt conectar`; métricas en unos días

## Sesiones (alias: tamriel daédricas, misiones daédricas)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo: guion, voz, clips, kit MG, Lyria, mezcla, render, revisión, miniatura, subida | ✅ 13/14-oct | el usuario pidió 1 sola sesión |

## Decisiones del episodio (13-oct-2026)
- tema: misiones daédricas (eje daédrico del canal + «no hagas esta misión» de fuera) · 8 puestos · SIN patrocinio
- voz Chatterbox `Sarcastica.mp3` · gema del canal · puente final a «Los 8 Príncipes Daédricos» (0TlESXgHxXM)
- miniatura: estilo PROPIO del canal (el usuario descartó la «copiando a Warcraft») → salida/miniatura.jpg (v1)
- título ≤ 50: «Las 8 misiones daédricas PROHIBIDAS de Skyrim» (el largo quedó de alternativo)
- MASTER: el usuario lo aprobó TAL CUAL el 14-oct («ya no hay que modificar»): se quedó con 4 detalles conocidos
  (menú de inventario a 0:06, mapa a 1:06, ~1 s negro hacia 1:30, rótulo «THE QUEST» a 4:48, el reloj de Namira
  arranca en 0:00). efectos.py ya trae el arreglo del reloj; los clips 001/008/011/035 se borraron de medios/
  (no re-renderizar sin bajarlos antes).

## Hecho
- guion 1 917 palabras · voz 82/82 (609,9 s) · 76 beats · 35 clips rehechos tras 3 hojas · 5 SFX (120 créditos) ·
  Lyria 5 tramos · mezcla -14,0 LUFS · MASTER 11:10 con pantalla final · verificar CER medio 0,77 %
- subido private con `--publicar 2026-10-15T15:15:00Z`, miniatura aplicada; registrado en canales/cronicas_tamriel.json
  (formato `lista_8_daedrico_secuencia_yt`) y BITACORA

## Falta
- [ ] subtítulos: subir salida/tes_misiones_daedricas.srt en Studio (o reconectar el token con force-ssl)
- [ ] a los 7 días: comparar con «objetos» 9 404 / «hechizos ROTOS» 8 570 (canales/formula/cronicas_tamriel.md)
- [ ] `python fab.py tes_misiones_daedricas limpiar` cuando ya no haga falta

## Lecciones de este video (detalle en docs/estilo_secuencia_yt.md § «Crónicas de Tamriel»)
- 2 tomas por frase con Chatterbox y reintento solo de las que fallan (4 tomas = ~2,4 h)
- `bajar --rehacer` borraba el clip antes de bajar el nuevo: con un 429 de YouTube quedaron 4 beats vacíos → motor arreglado
- tras ~150 descargas YouTube pide «confirma que no eres un bot»: espaciar las rondas de --rehacer
- en `--q` sin apóstrofos

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado y registrado (`canales/cronicas_tamriel.json`, BITACORA)
- [x] HALLAZGOS documentados (docs/estilo_secuencia_yt.md, CLAUDE.md tabla, memoria de miniaturas)
- Montaje con efectos exportado el 19-oct-2026 (`fab.py tes_misiones_daedricas fx montaje`: 32 tramos, 0 apoyos; panel 🎞 Montaje)
