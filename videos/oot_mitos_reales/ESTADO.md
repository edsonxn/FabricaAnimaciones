# Los MITOS de Ocarina of Time que eran REALES — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco lun 30-nov-2026 18:15 CDMX = 2026-12-01T00:15:00Z (cola: bt_50_secretos sale el 28-nov 00:12Z; ciclo 3 d)
- estilo: secuencia_yt + kit translúcido de Zelda (copiar de `videos/oot_remake_anadido/`) · voz NUEVA ElevenLabs Carlos Aguilar turbo (1.er video con ella) · OST oficial de Ocarina → doc: docs/estilo_secuencia_yt.md § Crónicas del gaming
- etapa: ✅ SUBIDO privado y PROGRAMADO lun 30-nov 18:15 CDMX (2026-12-01T00:15Z) — https://youtu.be/iXjyP-mUvH8 (MASTER 10:52, miniatura Flow B)
- siguiente: medir a 7 días (~8-dic) contra la mediana (hipótesis ≥ ×3 = 380 vistas) · Short derivado · `limpiar` al aprobar

## Por qué este video (26-nov-2026, RGC §R45; elegido por el usuario: «pon a producir la primera propuesta»)
- Investigación del 26-nov en `canales/formula/cronicas_gaming.md` § FÓRMULA VIGENTE: nuestro ganador `oot_remake_eliminado` ×15
  (1 942, 42 % visto, 9:47) + fuera Robe «DESMENTÍ los MITOS… de MARIO 64 que son Reales» ×4,1 (716 k) y ×2,6 (445 k).
- Variable que cambia respecto a oot_remake_eliminado: SOLO el ángulo (mito verificado). Mismo juego y ola del remake.
- Duración elegida por Claude: ~11 min (12 puestos; los de 10-12 min retienen 32-42 %, los de 21-25 min 14-30 %).
- Tono: misterio grave (la voz nueva) + sarcasmo seco del canal; cada mito cierra con sello REAL / A MEDIAS / FALSO.
- Hipótesis: ≥ ×3 la mediana del canal (≥ 380 vistas) a 7 días, por búsqueda «mitos ocarina of time».
- VOZ NUEVA (decisión del usuario del 12-nov, nunca estrenada): Carlos Aguilar `8MeTTgXVwMEhRVfblXOj`; tras 1-2 datos, placa
  «VOZ NUEVA» + un pedacito de Hope (~6-8 s) + «¿voz nueva o seguimos con Hope? vota en los comentarios»; se recuerda en el cierre.
  Contar votos a 7 días y decírselo al usuario. Saldo ElevenLabs: solo la cuenta 4 (53 292 créditos el 26-nov).
- Comentarios (26-nov): 4 nuevos; utilizables (≤ 10 días): @jhunoadguerrero-ilusionista «Buen trabajo, tienes mi apollo total»
  (gracias), @mau-azp (Banjo-Tooie, laguna y picos), @lindaclark6221 «Cuál granja del puente? No entendí nada» (queja justa:
  se explica el chiste, sin burla). Sin críticas nuevas (las de la voz ya salieron; se contestan con el cambio de voz).
  Pegatinas en pegatinas/com_*.png.

## Sesiones
- alias: mitos ocarina, mitos reales, oot mitos
- vista previa: ninguna; directo al MASTER (regla 5-nov)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión | ◐ 26-nov | investigación R45 + proyecto + comentarios + investigación de mitos |

## En curso
- ✅ proyecto creado (`nuevo --yt`), ayudantes, pegatinas y mapas copiados de oot_remake_anadido
- ✅ investigacion.md (agente: 18 mitos, fuentes, IDs con yt-dlp). OJO: tcrf.net Version_Differences traía texto para agentes de
  IA (pedía un pago y escribir key.bin): ignorado, no se cita. Fuera del guion: cuadros de Mario (ya en oot_remake_eliminado) y la
  «pelea secreta» de Skull Kid (oot_remake_anadido dijo que no es nueva).
- ✅ guion.py (19 escenas, 12 mitos: 10 REAL/A MEDIAS + 2 FALSO; ~1 550 palabras ≈ 11 min; `voz_2` = Hope; p1 post 7 s = el canto)
- ✅ MG nuevos en nucleo/mg_oot.py: `sello(veredicto, sub)` y `votacion()` (hoja previews/mg_nuevos.jpg, mg_votacion.jpg)
- ✅ OST: 25 pistas en audio/ost (faltan Happy Mask Shop y Saria's Song; no hacen falta)
- ✅ voz Carlos Aguilar 83/83 (5 rehechas con semilla 2: faltaban «Real.»/«Pausa rápida.» al inicio, «potos», «todo hay que»;
  lección: una palabra suelta tras el corchete al inicio de la frase se la come → no abrir frases con «Real.» solo) · idioma OK
  · tiempo + beats = 79 beats, 11:19 (lista en previews/_beats.txt; beat 71 = «Escucha» + 7 s del canto)
  · ElevenLabs: cuentas 2 y 3 con PAGO FALLIDO (401 payment_issue); solo la 4 (≈ 51 100 créditos) → avisar al usuario
- ✅ pegatinas nuevas (bajar_pegatinas.py) revisadas por identidad en previews/pegatinas_check.jpg (grog = hijo del maestro
  carpintero, el «Eyeball Frog» se borró; símbolo Gerudo viejo = media luna, nuevo = el de MM)
- ✅ clips_catalogo.md (agente, ~150 clips mirados en previews/_scan/) → plan_clips.py → busquedas.json → bajar 79/79 · medios
  mirados (medios_01-04): 061 cambiado a cementerio de Kakariko (P04 950), recortes en caja para GDQ (solo el juego) y
  SwankyBox (marco y logo) · brillo: 004 y 028 adelantados · 071 (canto) rehecho con dl_amb.py (bajar lo truncaba a 3,5 s)
- ✅ música armada (19 tramos OST; ganon/pesca bajadas a mano de Video Game Music / The Nintendo Music Channel; aparta −26 dB en
  071) · ambiente (071) · promesas.md (50) · efectos.py (126 FX, fx --seco OK)
- ✅ chequeo (densidad = canal; pegatinas subidas a ~4,4/min; avisos de sonido = falsas alarmas) · fx hoja mirada 2 veces y
  arreglada (072 terminaba en Cruis'n → RM100 37451 + pegatina voice_spectral; 004 sin diálogo; choques de fichas/siluetas;
  línea de la Trifuerza fuera porque tapaba «You got the Triforce»; Switch 2 rotulado «Nintendo Music» fuera; Rauru sin
  rótulo duplicado) · promesas 51/51 (promesas_01-05) · fx + mezcla (−14 LUFS, voz/fondo 14,4 dB)
- ✅ REGLA 10: el canto se oye en audio/final.wav 599,9-608,6 (−20 dBFS; Demucs: voz −25 dB contra −22 del resto de la música
  del juego, como en la mezcla original; Whisper es: nada de voz encima) → previews/citas_audio.mp3
- ✅ miniatura Flow B → salida/miniatura.jpg (prompt_miniatura.md) · youtube.json (título 43 car. «12 MITOS de Ocarina of Time
  que eran REALES», capítulos por timeline)
- ✅ 26-nov (tarde) el usuario vio el MASTER: (1) FUERA la votación de voz (escena «voz», «hasta este cambio de voz…», «¿voz nueva
  o la de antes?» y los 2 MG): Carlos Aguilar es la voz por defecto del canal; (2) REGLA R46 (secretos/mitos de verdad: los cucos
  vengadores son obvios, no mito; se quedan en este video, no se repite). Guion 80 frases, 76 beats, 10:52; plan_clips rehecho
  (42 clips reaprovechados, previews/_plan_clips_79.py = el de antes); hoja fx y promesas mirados de nuevo; recorte en caja de las
  franjas de Censored Gaming (13,3 %). El MASTER viejo lo bloqueaba el reproductor del usuario (os.replace «Acceso denegado»).
- ✅ render → final → verificar (CER 0,28 %, sin desfase, sin negros; canto audible 575-584 s, previews/citas_audio.mp3) → avisar
  → yt subir → registrado en canales/cronicas_gaming.json + BITACORA
- siguiente: video → final → verificar → tele master → avisar → yt subir oot_mitos_reales cronicas_gaming private --publicar
  2026-12-01T00:15:00Z → registrar en canales/cronicas_gaming.json + BITACORA + canales --actualizar → commit

## Falta
- [ ] guion · voz · seleccionar · idioma_voz · beats · plan de clips · bajar · medios · OST · fx · promesas · chequeo
- [ ] fx hoja · render · final · verificar · miniatura Flow · subir 1-dic 00:15Z · registrar · Short derivado
