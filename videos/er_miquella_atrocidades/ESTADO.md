# Las 5 peores atrocidades de Miquella QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · PROGRAMADO mar 20-10-2026 10:00 CDMX (2026-10-20T16:00:00Z) · https://youtu.be/vUaTbbI9yiM
- estilo: secuencia_yt (gameplay de Elden Ring por beat + PEGATINAS + imágenes a pantalla + MG `nucleo/mg_er.py`; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md § Runa Caída
- etapa: programado (subido private el 19-oct con miniatura; .srt sin cargar)
- siguiente: .srt a mano en Studio · a los 7 días (27-oct) `python fab.py yt metricas runa_caida 90` y comparar con Márika/Radagon (minutos por vista, % visto)

## Sesiones (plan de tramos · «continúa el video miquella» retoma aquí · protocolo docs/sesiones.md)
- alias: miquella, atrocidades de miquella, runa caída 20 min
- vista previa: NO (el usuario, 18-oct): MASTER directo, revisado con hojas de cuadros + barrido de negros/quietos
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz Faraon + seleccionar + tiempo | ✅ 18-oct | 141 frases, voz 1 120 s, video 19:55 (+ pantalla final) |
| 2 | beats, búsquedas, clips, pegatinas, pant(), fichas/MG mg_er | ✅ 19-oct | 139 clips (54 rehechos en 4 rondas), 147 efectos |
| 3 | Lyria, SFX, mezcla, render, revisión, miniatura, subida private | ✅ 19-oct | MASTER 2 (20:15) revisado: sin negros ni quietos; subido private |

## Revisión del MASTER 1 (19-oct-2026; 20:15, CER 0,87 %, hojas previews/master/master_01..17.jpg)
- negros: 076 pantalla de carga 4 s (10:43) → `--desde 354` · 049 y 123 fundían desde negro al empezar · 123 además menús de
  diálogo (IGN) → «Enir-Ilim 4k» · quietos 3 s: 025 (diálogo de Freyja) → «Shadow Keep 4k», 101 (Ambient Souls) → SourceSpy91
  Part 6 @1012 · 013 menú de tienda de Thiollier → «Scadu Altus 4k» · 098 rótulo «Source: Golden Seed» → SourceSpy91 @862
- pantallas fijas demasiado largas: seguidores 21,6 s → 9,1 · trina_final 18,5 → 8,3 · malenia_vs_radahn 12,9 → 6,0 ·
  la 2.ª «seguidores» (17:07) era repetida → `tierra_sombras`
- `fuentes.json`: los fijados a mano (`--url`) quedaban sin canal → completados; descripción sin VaatiVidya/IGN/Ambient Souls;
  capítulo #3 en 8:18 (decía 8:28)
- el usuario (19-oct) ELOGIÓ el MG `hilos` («Los seguidores de Miquella») → regla nueva: MG NUEVOS y distintos por guion en
  Warcraft/Tamriel/Runa (docs/estilo_secuencia_yt.md § MOTION GRAPHICS NUEVOS, plantilla yt, CLAUDE.md, memoria)

## Decisiones del episodio (18-oct-2026)
- duración ~20 min (lo pidió el usuario: PRUEBA de duración frente a los ~6-7 min de Márika/Radagon; anotar resultado en la fórmula)
- 5 puestos (~3,5 min cada uno) · «Las 5 … QUE IGNORASTE» cambiando el sujeto: Radagon → Miquella (lore del DLC)
- puente final a los videos de Radagon (L0HTszG4ycM) y Márika (KKxhcwon2kg)

## Hecho
- guion.py: 141 frases, 3 239 palabras, 12 escenas (pN/pNb para Lyria ≤ 175 s); citas verificadas en Fextralife
- voz 141/141 (umbrales por frase en guion.py) · Lyria 12 tramos · 5 SFX (180 créditos) · mezcla −14,1 LUFS
- 37 pegatinas (Fandom) + 24 pantallas · mg_er nuevos: `hilos`, `cosido`, `cruces`, `triada` · miniatura Flow (salida/miniatura.jpg)
- youtube.json (título, descripción con capítulos y créditos, etiquetas) · salida/creditos.txt (100 videos)

## Falta
- [x] render 2 (37 min) → final → revisión 2: barrido sin negros/quietos + mosaicos de cada tramo cambiado (previews/master2/)
- [x] subido private con miniatura (vUaTbbI9yiM) · registrado en canales/runa_caida.json y BITACORA · `canales --actualizar`
- [x] programado mar 20-oct 10:00 CDMX (orden del usuario) · [ ] .srt a mano en Studio (token sin force-ssl)
- [ ] a los 7 días: resultado de la prueba de 20 min en canales/formula/runa_caida.md · `limpiar` cuando ya no haga falta

## Lecciones de este video (solo lo no obvio)
- con 140+ frases de Faraon ~1/3 cae en la 1.ª ronda por cola y por nombres que Whisper no sabe escribir («Mohg» → Moj/Mohawk):
  NO regenerar; revisar eval.json y fijar umbrales por frase. Regenerar solo errores reales (vestos, Estrato, «con pasión»).
  **CORREGIDO el 22-oct tras publicarlo:** «Moj/Mojé» y «Mikeya» SÍ eran errores reales: los comentarios se burlan de «Miqueya y
  Mojé». Nombre propio mal escrito por Whisper = regenerar (detalle en `docs/estilo_secuencia_yt.md` § Runa Caída).
- «Ese uno eres tú» → Whisper «S1 eres tú»: frases de 3-4 palabras con «uno» = reescribir.
- `pant()` con ancla final lejana = imagen fija de 18-21 s: medir con `fx --seco` y dejar cada pantalla en ≤ ~10 s.
- `bajar --url --desde` deja `canal` vacío en fuentes.json → créditos incompletos: completarlo antes de `fuentes`.
- el barrido a 2 fps cazó los negros que las hojas cada 6 s no ven (pantalla de carga, fundidos al inicio de clip).

## Cierre (regla del 12-oct-2026)
- [x] subido (private), miniatura y registrado (`canales/runa_caida.json`, BITACORA) · panel `canales --actualizar` · [x] programado mar 20-oct 10:00 CDMX
- [x] HALLAZGOS documentados (ESTADO, docs/estilo_secuencia_yt.md § MG NUEVOS, memoria) · [ ] resultado de la prueba de 20 min a los 7 días
- Montaje con efectos exportado el 19-oct-2026 (`fab.py er_miquella_atrocidades fx montaje`: 64 tramos, 0 apoyos; panel 🎞 Montaje)
