# Lo que Nintendo AÑADIÓ en SECRETO al remake de Ocarina of Time — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco jue 12-nov-2026 18:00 CDMX (2026-11-13T00:00:00Z; cola recorrida el 11-nov para meterlo)
- estilo: secuencia_yt + kit translúcido de Zelda (copiar de `videos/oot_remake_eliminado/`) · voz ElevenLabs Hope turbo · OST oficial de Ocarina → doc: docs/estilo_secuencia_yt.md § Crónicas del gaming
- etapa: ✅ SUBIDO privado y programado jue 12-nov 18:01 CDMX — https://youtu.be/MKm8G-aiu7Y (MASTER 10:24, miniatura Flow)
- siguiente: medir a 7 días (~19-nov) contra oot_remake_eliminado (hipótesis ≥ ×3 la mediana) · Short derivado · `limpiar` al aprobar
- (viejo) siguiente: guion.py con fuentes → voz → seleccionar → idioma_voz → beats → plan_clips → bajar → medios → OST → efectos → chequeo → fx hoja → promesas → render → final → verificar → tele → miniatura Flow → subir

## Por qué este video (11-nov-2026, pedido del usuario: «seguir por Zelda y el remake»)
- `oot_remake_eliminado` (WjDK78u1ZO0) despegó: 1 088 vistas en ~2,5 días, 43 % visto, retención plana (×4-×15 frente al resto).
- Variable que cambia: SOLO el ángulo (lo eliminado → lo AÑADIDO sin avisar). Misma fórmula, ~10-12 min, título corto con verbo fuerte.
- Referencias de la semana: N Deluxe «30 nuevos secretos del remake» ×3 (95 k); Filosofía Nintendera «TODOS sus SECRETOS» ×2,7;
  Shorts de detalles ocultos 50-116 k (Link sonríe, 5.ª botella, ReDeads, jefe secreto de Skull Kid).
- Hipótesis: ≥ ×3 la mediana del canal a 7 días (≥ 600 vistas), sobre todo por búsqueda «ocarina of time remake secretos».
- Comentarios (11-nov): pegatinas ya bajadas en pegatinas/com_*.png. Críticas con contraburla: @omaryorke «usa Loquendo» (♥5),
  @isierra1595 «vete a TikTok», @PedrO-nf3lj «insufrible la voz». Pregunta: @mantequill4 «¿Master Quest saldrá?». Gracias:
  @frandeltin4387 «Muy buen video, ns pq no tiene likes y vistas» (en Mario 64). La voz IA se le reportó al usuario (no se cambia sola).

## Sesiones
- alias: remake añadido, oot añadido, lo que añadió el remake
- vista previa: ninguna; directo al MASTER (regla 5-nov)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión | ✅ 11-nov | cola recorrida + proyecto + comentarios + investigación + guion + voz + OST + scans; corte a 180 k |

## En curso
- ✅ investigacion.md (14 añadidos, agente) · ✅ guion.py (20 escenas, 12 puestos, 3 críticas, gracias, ~9,6 min) · ✅ voz Hope (76 frases)
- ✅ OST bajada (armar_musica_ost.py, SECCIONES nuevas; jabu puede faltar: revisar `bajar`) · hojas de candidatos en previews/_scan/
- Audio original (post): Ganondorf 8nSoklvmLkM 204,3-209,4 s (p4 post 5,6) · Darunia L45cq1H2d1s 12197,3-12205,6 s (p3 post 8,4)
- ◐ seleccionar + idioma_voz lanzados en 2.º plano (~20:30, 11-nov; esperan a que la sesión de Runa suelte la GPU; log en
  previews/_sel.log y previews/_idioma.log). p7_0 reescrita («ahora dan todavía más miedo»). Si _sel.log no dice «76/76» → repetir
  `fab.py oot_remake_anadido seleccionar` y luego `python nucleo/idioma_voz.py oot_remake_anadido`.
- ✅ 11-nov ~21:00: FONETICA (Master Quest, Skull Kid, Majora's Mask, ranking) + 2 frases reescritas por idioma_voz (5 X); voz
  regenerada; seleccionar + idioma_voz relanzados en 2.º plano (repetir si no dice 76/76 y 0 X). Pegatinas: 40 copiadas de
  zelda_oot/oot_remake_*/majora_mask + 12 nuevas (bajar_pegatinas.py; korok = TWW Koroks Artwork). beats tenía 72 (rehacer tras voz).
- ✅ 11-nov ~22:30: voz 76/76 + idioma_voz OK (0 X) · tiempo/beats = 73 beats, 10:25 · plan_clips.py + busquedas.json · bajar 73/73
  · medios mirados (rehechos 015 menú de canciones 9DkGKmx6NsQ, 038 revancha bXK2m6v52kw, 040 guardia N64, 059 MQ; recorte 016/042)
- ✅ música armada (audio/musica.wav 624,8 s) + ambiente. scene-048 y scene-055 CORTADOS A MANO (yt-dlp --download-sections
  --force-keyframes-at-cuts; 048 pedido 198.23 = empieza en 203,2 real, 055 = 12196,3; comprobado por correlación con
  previews/_scan/gan16.wav y dar.wav). NO hacer `bajar 48,55 --rehacer` (fuentes.json dice 199/12198, es solo el crédito).
- ✅ efectos.py (117 FX, 4 mapas de Hyrule mapas/hyrule_3ds.png, 5 comentarios con com() = mg_majora.pegatina) · chequeo OK
  (idioma OK; ocarina del 015 audible ambiente .8) · fx hoja FINAL mirada (fx_01-06) y arreglada (ventanas repetidas fuera,
  anclas Darunia/Link niño, 037/061 rehechos, comentarios legibles: previews/_chk_arreglos.jpg).
- ✅ 1.er MASTER 21:05 (10:24, sin desfase) · tele no prendida (avisó por voz) · ARREGLO: los 3,5 s iniciales salían negros (fundido del
  clip 001) → scene-001 desde 6 s; `video --rehacer 0-8 → final → verificar` en 2.º plano (previews/_render2.log).
- ✅ miniatura Flow A → salida/miniatura.jpg (prompt_miniatura.md) · ✅ youtube.json
- Falta: comprobar brillo del inicio del MASTER nuevo → tele master → `yt subir oot_remake_anadido cronicas_gaming private --publicar
  2026-11-13T00:00:00Z` → registrar en canales/cronicas_gaming.json + BITACORA + canales --actualizar → commit.
- (viejo) RENDER lanzado en 2.º plano (fx → mezcla → video → final → verificar; log previews/_render.log). Después: tele master,
  avisar, miniatura Flow, youtube.json, subir --publicar 2026-11-13T00:00:00Z, registrar, commit.
- SIGUIENTE (viejo): efectos.py (ver abajo), promesas.md, chequeo, fx hoja.
- Falta, en orden (lo de antes de «armar_musica» YA está): tiempo → beats → busquedas.json/plan_clips.py (copiar estructura de ../oot_remake_eliminado/plan_clips.py) → bajar
  → medios (MIRAR) → pegatinas (bajar_pegatinas.py) + ventanas N64 → `python armar_musica_ost.py` (comprobar jabu.wav) → ambiente
  → efectos.py (copiar ayudantes de ../oot_remake_eliminado/efectos.py: puesto «Añadido número N») + promesas.md → chequeo →
  `FAB_FX_FINAL=1 fab.py <v> fx hoja` (MIRAR) → fx → mezcla → video → final → verificar → tele master → miniatura Flow → youtube.json
  → `yt subir oot_remake_anadido cronicas_gaming private --publicar 2026-11-13T00:00:00Z` → registrar.
- Herramienta: `python _scan.py <id> previews/_scan/x.jpg a:b:paso` (cuadros de YouTube sin bajar; los primeros a veces salen negros).
- CLIPS YA MIRADOS (id, segundo):
  - botella: MOj6mCoK1sE 15 «Good sir!», 22 Link recibe botella, 30 «scoop up the bug», 38 atrapa, 52 tienda abierta, 60 poción roja
  - Ganondorf: 8nSoklvmLkM 172-206 espada y Link en blanco; 215-258 Ganondorf habla; 266-274 entra al Reino Sagrado (dorado)
  - sabios: L45cq1H2d1s Saria 10720-10775 (Cámara de los Sabios); Darunia 12198-12250; Volvagia/Montaña 12150-12162
  - Salón: opfv1K35uNE 540-900 (estatuas con fichas: Iron Knuckle 585, ReDead 630, Stalfos 720, Business Scrub 810, salón 900);
    SAHDCv3emzA 140 rótulo «Hall of Fallen Foes» (resto negro en el scan). Revanchas: bXK2m6v52kw. MUt7wPJIyaE = boss rush (HDR)
  - Mano Muerta: TTeIO1qeFGE (N64 vs 3DS vs Switch 2, 247 s) y Vh2jiWNbKIk; ReDead: XPvYWutj5ag (N64/3DS/Switch 2)
  - Máscara de la Verdad: niOLyw2vhCU / GzNjaJjivWM / CqAzG_093Uc (todos los pensamientos)
  - Semilla Deku: z8awcvmtphY NO sirve (facecam); probar K8K_iVdQx9U / WLQUuD_9j9s; si no, pegatina del objeto + Flow
  - Master Quest GameCube: EFhB23Z1OWw (ya usado en el video anterior); vacas: Rg8y2Pd1PgA 294
  - hojas sin mirar aún: previews/_scan/{kokiri,ocarinas,estuche,skullkid,dedos,hierba,redead,manomuerta,verdad,vacas,amiibo,manon64,mq,scrub}.jpg

## Lecciones (11-nov)
- `bajar` con +ba cortó Ganondorf 5 s tarde y Darunia truncado: para audio exacto usar yt-dlp --download-sections --force-keyframes-at-cuts y comprobar por correlación con el audio original.
- Clip 001 con fundido negro de 3,5 s: medir brillo del 1.er segundo de cada clip del gancho antes del render.
- Separación 48 h es estricta al segundo: un público que salió a 00:00:37 obliga a correr la cola unos minutos.
- Flow: fetch a 127.0.0.1 bloqueado; ingredientes por i.ytimg.com (miniatura del video fuente) funcionan.
