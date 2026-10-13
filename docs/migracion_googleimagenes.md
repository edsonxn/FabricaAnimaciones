# Mudanza de canales desde `C:\googleimagenes` (iniciada 13-oct-2026)

El usuario pidió (13-oct-2026) traer a la Fábrica tres canales que hoy se producen con el sistema viejo
(Node/Express, `C:\googleimagenes`, salidas en `D:\videosnuevos\<canal_slug>\<video>\`):

| Canal | channelId | Tema | Voz en el sistema viejo | Prioridad |
|---|---|---|---|---|
| **Crónicas de Warcraft** | `UCjzJdQdD2vCpw1jHCqiQeFw` | WoW (hoy: WoW Forever / Classic+), listas «Las N … de peor a mejor» | **Applio** (Edge TTS `fr-FR-RemyMultilingualNeural` → RVC `RemyOriginal.pth`) | **1 — el canal más importante** |
| Crónicas de Tamriel | `UCWeCfdm8py6dYKHq7HwUIXw` | Skyrim / Elder Scrolls, listas | Chatterbox | 2 |
| Runa Caída | `UCQi_vcDu2EBmWy0U2I6pUDg` | Elden Ring, secretos/lore | Chatterbox | 3 |

Lectura de los canales: **con yt-dlp** (petición del usuario). Ojo: yt-dlp devuelve títulos auto-traducidos al inglés;
usar `--extractor-args "youtube:lang=es"` o leer el título original.

## Cómo se hace hoy un video de Warcraft (estudiado en `tauren_carrera_prohibida` = «Las 9 razas de WoW Forever», `qNuXfB386qc`, 972 s)
- Guion por secciones (30 secciones), estilo «gema» (chistes secos, cita ficticia dramática por sección, fonética con acentos
  para el TTS). Memoria vieja: `C:\Users\jaire\.claude\projects\C--googleimagenes\memory\tamriel-warcraft-gema-script-style.md`.
- Voz por sección con Applio → WAV + `whisper_segments.json`.
- **Secuencia de clips de YouTube (yt-dlp)**: 101 clips de ~8,6 s; cada clip = `sourcePath` (`seccion_N/broll/yt_<id>_<a>-<b>.mp4`),
  `cutFrom`, `duration`, `phraseText` (frase de Whisper que cubre), transición `slideleft`, etc. Archivo: `broll_preview.json`.
- **Apoyos** (~30-34 por video): `overlayImage` encima del clip (tooltips Wowhead, tarjetas, capturas). Receta en
  `C:\googleimagenes\CLAUDE.md` § «Apoyos».
- **3 motion graphics Remotion** encima de clips (`mgOriginal`), base `C:\googleimagenes\holavideo\src\Composition_mg_wow.tsx`.
- Regla de canal (11-oct): todo video lleva apoyos + 3 MG sin pedirlo.

## Applio desde Python (sin el servidor Node)
`C:\applio2\Applio\core.py tts ...` (CLI propio; python del entorno `C:\applio2\Applio\env`). Parámetros que usaba el
sistema viejo: pitch 0, index_rate 0.75, protect 0.5, f0 `rmvpe`. Voces RVC en `C:\applio2\Applio\logs\VOCES\*.pth`
(RemyOriginal, Faraon, Horacio, Kurz, Edson, …).

## Patrocinio Overgear (campaña activa, 13-oct-2026)
- Hoy: se pega un comercial prefabricado de 40 s entre las secciones 2 y 12:
  `C:\Users\jaire\Downloads\overgear_promo_ES_remy_preview_720p.mp4`.
- **Lo único intocable: el tramo del código** (≈ 33,0–40,0 s: «Usa el código CRONICAS10, 10 % de descuento» + packshot
  «-10% WITH PROMO CODE CRONICAS10» + «LINK IN THE DESCRIPTION»). El brief exige usar el creativo personalizado tal cual.
- Lo demás se rehace: segmento propio de 20-30 s, narrado con la voz del canal, que nazca del tema del video.
- Assets de Overgear: `D:\Cronicas de Warcraft\Overgear\` (Background.mp4, cards-carousel/cards-2 en pantalla verde,
  logo dark/light, packshot logo/texto en verde, pastillas pros/support/top-coaches/tos-friendly/trust/zero-ban, 4 «pair_green»).
- Brief (resumen): parche 12.1.5 (semana del 13-oct), raid de un jefe «The Unbinding of Kith'ix», logro M+ «Keystone Myth»,
  WoW Forever sale el 4-nov (primeras raids 9-dic) y Overgear ya se prepara para él. **Decir «self-play», nunca «jugamos
  por ti» ni compartir cuenta.** Mostrar captura de overgear.com/games/wow; código visible y sin recortar; tono neutro o
  positivo 30 días. Escoger UNA vía concreta (M+, raids, PvP o powerleveling).

## Decisiones del usuario (13-oct-2026)
- Orden: **Warcraft primero y completo**; Tamriel y Runa después reutilizando el motor.
- **El próximo video de Warcraft sale ya de la Fábrica** (no del sistema viejo), aunque tarde unos días.
- Comercial: la vía de Overgear (raids/M+/PvP/leveling) se elige **según el tema de cada video**, enlazada con WoW Forever.
- Quiere un **preview tipo «Estudio»** (el de `http://localhost:3000/estudio.html?p=<canal>/<slug>`: timeline de clips,
  monitor, cambiar clip, apoyos) **dentro del panel actual de la Fábrica, sin romper lo que ya funciona** en los otros canales.
  Claude decide la forma: pestaña/vista nueva del panel que solo se activa en videos con motor de secuencia yt-dlp.
  Ojo: `docs/estudio.md` ya es el «Estudio comercial»; el nuevo necesita otro nombre (p. ej. «Montaje»).

## Hecho
- Voz Applio: `VOZ = dict(motor="applio", tts_voice="fr-FR-RemyMultilingualNeural", rvc="RemyOriginal", pitch=0, rate=0,
  idioma="es", referencia=r"C:\chatterbox_voices\RemyOriginal_applio.wav")` en guion.py → `fab.py <v> voz` llama a
  `nucleo/tts_applio.py`. Edge TTS corre con el python de la Fábrica (**edge-tts 7.3.0**; el 7.2.8 del entorno de Applio
  da 403 de Microsoft) y RVC con el python de Applio (`nucleo/applio_lote.py`, modelo cargado una vez). Probado 13-oct:
  ~1 min de arranque + ~6 s por frase. `tts_select` no recorta colas para Applio (TAIL_MAX 1.0).
- Tokens: `nucleo/youtube.py` ya lee los de `C:\googleimagenes` → `fab.py yt …` funciona con los 3 canales.
- **S2a (13-oct) motor SECUENCIA YT** ✅: `nucleo/secuencia_yt.py` (`busquedas`, `bajar`, `fuentes`) sobre
  `nucleo/secuencia.py` (+ transición `slideleft`), plantilla `fab.py nuevo <v> --yt`, filtros oscuro/quieto/webcam.
  Probado con 4 beats reales (37 s, 1080p). Doc: `docs/estilo_secuencia_yt.md`.
- Fichas: `canales/cronicas_warcraft.json` (cada 2 días 09:00 CDMX, heredado), `cronicas_tamriel.json`, `runa_caida.json`
  (provisionales).

## Pendiente (por sesiones)
- [ ] S2b: apoyos (tooltips Wowhead/tarjetas como capa en `efectos.py`) + 3 MG (Remotion de `holavideo` o por código);
  receta en `C:\googleimagenes\CLAUDE.md` § «Apoyos» y `estudio_apoyos.js` (grep).
- [ ] S2c: vista «Montaje» en el panel (timeline de `beats.json`+`fuentes.json`, monitor, «cambiar clip» = `bajar N --q`).
- [ ] S3: comercial Overgear (20-30 s propios + tramo intacto 33,0-40,0 s del creativo con CRONICAS10) + primer video.
- [ ] `docs/estilo_broll_wow.md`, tabla de CLAUDE.md, memoria; luego Tamriel y Runa (Chatterbox).
