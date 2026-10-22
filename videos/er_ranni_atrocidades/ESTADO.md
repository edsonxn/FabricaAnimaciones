# Las 5 peores atrocidades de Ranni QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · PROGRAMADO dom 25-10-2026 10:00 CDMX (2026-10-25T16:00:00Z) · https://youtu.be/ZamBFBDZ6OI
- estilo: secuencia_yt (gameplay de Elden Ring por beat + PEGATINAS + pantallas + MG `nucleo/mg_er.py`; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md § Runa Caída
- etapa: programado (subido private el 22-oct con miniatura; .srt sin cargar)
- siguiente: .srt a mano en Studio · a los 7 días (01-nov) `python fab.py yt metricas runa_caida 90` y comparar duraciones (6-7 / 12 / 20 min)

## Sesiones (plan de tramos · «continúa el video ranni» retoma aquí · protocolo docs/sesiones.md)
- alias: ranni, atrocidades de ranni, runa caída 12 min
- vista previa: NO (el usuario, 21-oct: «12 minutos hasta el final, 1 sesión»): MASTER directo + hojas + barrido de negros/quietos
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo: guion → voz → clips → pegatinas/MG → Lyria/SFX/mezcla → render → revisión → subida | ✅ 21/22-oct | una sola sesión (pedido del usuario); MASTER 2 de 12:16 |

## Decisiones del episodio (21-oct-2026)
- duración ~12 min (pedida por el usuario) · «Las 5 … QUE IGNORASTE», sujeto Ranni (la favorita = la peor)
- puestos: 5 Seluvis · 4 Blaidd · 3 las asesinas e Iji · 2 Godwyn (Noche de los Cuchillos Negros) · 1 la Era de las Estrellas
- MG nuevos: `marionetas`, `sombra`, `domino`, `constelacion` (docs/estilo_secuencia_yt.md § Runa Caída)
- Ranni a media frase («la bruja», «ella») para evitar la R inicial de Faraon

## Hecho
- guion.py: 82 frases, ~2 010 palabras, citas verificadas (fuentes en su docstring) · voz 82/82 (674 s) · video 11:56 + pantalla final
- 83 clips (17 rehechos; recorte_por 0,09 a los 9 de Shirrako por su firma; 0,06 al 064) · 110 efectos · 50 pegatinas + 9 pantallas
- Lyria: 6 tramos nuevos + 1 de la biblioteca (tes_misiones_nunca__lyria_tramo6) · SFX: 3 de la biblioteca + 2 nuevos · −14,0 LUFS
- miniatura Flow (ranni_v1) · youtube.json con capítulos y créditos (33 canales) · salida/creditos.txt
- registrado en canales/runa_caida.json y BITACORA · `canales --actualizar` (Runa BIEN hasta vie 30-oct) · biblioteca catalogada

## Revisión del MASTER (22-oct)
- MASTER 1: hojas cada 6 s (320 px) + blackdetect + quietos: firma «SHIRRAKO» en sus clips y la misma toma de Ranni en la ventana
  8 veces → recortes + 014/078 cambiados → MASTER 2: sin firmas, sin negros, quietos solo en la pantalla final (plantilla de tarjetas)

## Falta
- [ ] .srt a mano en Studio (token sin force-ssl) · [ ] resultado a 7 días en canales/formula/runa_caida.md · [ ] `limpiar` al aprobar

## Lecciones de este video (solo lo no obvio)
- hojas de contacto a 240p de 3-4 videos limpios ANTES de `bajar` y fijar url+segundo: 20 % rehechos (antes 39-50 %)
- las marcas de agua chicas (Shirrako) no se ven en hojas de 240 px: recortar la esquina a tamaño real del MASTER
- comprobar todas las anclas de efectos.py de golpe con límites de palabra («el dragón» ≠ «del dragón»)
- en Git Bash `sleep` no sigue el reloj real si el equipo reposa: esperar con PowerShell + `Get-Date`, o pedir keep-awake

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal (regla 20-oct), miniatura y registrado (`canales/runa_caida.json`, BITACORA)
- [x] HALLAZGOS documentados (ESTADO, docs/estilo_secuencia_yt.md § Runa Caída, canales/formula/runa_caida.md, memoria)
