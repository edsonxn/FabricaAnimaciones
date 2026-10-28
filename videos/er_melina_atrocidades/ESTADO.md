# Las 5 peores atrocidades de Melina QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · PROGRAMADO dom 01-11-2026 10:00 CDMX (2026-11-01T16:00:00Z) · https://youtu.be/U4reFaDG6Vg
- estilo: secuencia_yt (gameplay de Elden Ring por beat + PEGATINAS + imágenes a pantalla + MG NUEVOS `nucleo/mg_er.py` + mapas; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md § Runa Caída
- etapa: programado (subido private el 28-oct con miniatura; .srt sin cargar)
- siguiente: ✅ APROBADO por el usuario (28-oct) · .srt a mano en Studio (o `yt conectar`) · a los 7 días (8-nov) métricas vs Ranni/Miquella/Malenia

## Sesiones (plan de tramos · «continúa el video melina» retoma aquí · protocolo docs/sesiones.md)
- alias: melina, atrocidades de melina
- vista previa: MASTER directo (el usuario, 27-oct), revisado con hojas + barrido de negros/quietos, y aviso
- el usuario eligió hacerlo TODO EN UNA sesión (27-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz Faraon + seleccionar + tiempo | ✅ 27-oct | 117 frases, 3 495 palabras, voz 1 160 s, video 20:11 (+ pantalla final = 20:31) |
| 2 | beats, plan de clips, pegatinas, pant(), mapas, fichas/MG mg_er NUEVOS | ✅ 27-oct | 141 clips (12 rehechos), 150 efectos |
| 3 | música OST, SFX, mezcla, render, revisión, miniatura, subida private + programar | ✅ 28-oct | MASTER 3 sin negros ni quietos; CER 0,25 % |

## Decisiones del episodio (27-oct-2026, elegidas por el usuario)
- tema: Melina (mismo gancho «la favorita es la peor» que Ranni, 8 437 vistas en 2 días); descartados Mésmer y la Voluntad Mayor
- duración: al menos 18 min (copia del ganador Miquella ~20 min, ×18, 46 % visto)
- comentarios: `yt comentarios runa_caida` dio 403 (falta permiso en el token: `yt conectar` lo hace el usuario); el guion no cita comentarios
- puestos: 5 te eligió por estar solo · 4 la hija secreta (MaricaOfDaughter, Yesca de Mésmer) · 3 el pecado capital · 2 muerte para
  todos · 1 la promesa de matarte (escena tras los créditos, ojo violeta, teoría de la Reina del Ojo Velado dicha como teoría)

## En curso
- (nada: video cerrado el 28-oct)

## Hecho
- guion.py con citas verificadas (wikitexto de eldenring.fandom.com en inglés y japonés; nombres oficiales de la wiki es)
- voz: 234 tomas + 12 regeneradas; errores reales arreglados reescribiendo (DLC → «la expansión», «…a Maliketh, su guardián»,
  «esa llama», «Márika y Radagon… la de Ranni»); umbrales por frase para las falsas alarmas (comentario en guion.py)
- clips: plan_frases.json (subagente) → asignar_clips.py → busquedas.json; recorte .09 en los 17 de Shirrako
- efectos.py: ~60 pegatinas, ~40 fichas, 18 pantallas, MG nuevos `acuerdo` (x2), `ecos` (x3), `arbol_arde` (x2), `muerte_suelta`
  (x2), 2 mapas del mundo (acuerdo; ventana de la Hoja de la invocación), 6 SFX nuevos
- música: armar_musica_ost.py (OST oficial: tema, Mesa Redonda, Leyndell, Mésmer, Morgott, Gigante de fuego, Maliketh, Señor de la
  Llama Frenética), cortes por escena desde timeline.json
- miniatura Flow (miniatura_ing/flow/melina_v1.png, receta prompt_miniatura.md) · youtube.json con capítulos y créditos
- MASTER 1 → 3: 8,2 s quietos bajo el MG «acuerdo 2» (clip de Melina de pie) → clip de Torrentera galopando

## Lecciones de este video (solo lo no obvio)
- Fextralife cierra la conexión a scripts: el wikitexto de eldenring.fandom.com trae los diálogos completos (`Melina/dialogue`)
- TheFinalEpic (d2FRpV9KrkY) juega con el personaje casi desnudo: revisar al jugador en las tomas de diálogo
- MG grande + clip quieto = congelado; `CAMARA` no movió el clip: cambiar el clip
- E: quedó con 4,7 GB libres tras el render (antes 11): liberar antes del siguiente video largo

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/runa_caida.json`, BITACORA)
- [x] HALLAZGOS documentados → docs/estilo_secuencia_yt.md § Runa Caída (Melina), mg_er (4 MG), canales/formula/runa_caida.md
