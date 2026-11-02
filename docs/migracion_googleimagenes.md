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
- **Regla de canal (18-oct-2026, el usuario: «anota eso como constante en el canal»): todo video lleva PEGATINAS** — imagen real de
  cada personaje/objeto/prenda que nombre la voz, añadida a clips/apoyos/MG (`peg()` de la plantilla; docs/estilo_secuencia_yt.md § PEGATINAS).

## Applio desde Python (sin el servidor Node)
`C:\applio2\Applio\core.py tts ...` (CLI propio; python del entorno `C:\applio2\Applio\env`). Parámetros que usaba el
sistema viejo: pitch 0, index_rate 0.75, protect 0.5, f0 `rmvpe`. Voces RVC en `C:\applio2\Applio\logs\VOCES\*.pth`
(RemyOriginal, Faraon, Horacio, Kurz, Edson, …).

## Patrocinio Overgear (campaña activa, 13-oct-2026)
- Hoy: se pega un comercial prefabricado de 40 s entre las secciones 2 y 12:
  `C:\Users\jaire\Downloads\overgear_promo_ES_remy_preview_720p.mp4`.
- **Del creativo solo la IMAGEN del tramo del código** (≈ 33,0–40,0 s: «Usa el código CRONICAS10, 10 % de descuento» + packshot
  «-10% WITH PROMO CODE CRONICAS10» + «LINK IN THE DESCRIPTION»). **Su audio NO** (el usuario, 13-oct-2026: se notaba el
  cambio de voz): el código lo dice nuestra voz con una frase propia. El brief pedía el creativo tal cual; decisión del usuario.
- Lo demás se rehace: segmento propio de 20-30 s, narrado con la voz del canal, que nazca del tema del video.
- Assets de Overgear: `D:\Cronicas de Warcraft\Overgear\` (Background.mp4, cards-carousel/cards-2 en pantalla verde,
  logo dark/light, packshot logo/texto en verde, pastillas pros/support/top-coaches/tos-friendly/trust/zero-ban, 4 «pair_green»).
- Brief (resumen): parche 12.1.5 (semana del 13-oct), raid de un jefe «The Unbinding of Kith'ix», logro M+ «Keystone Myth»,
  WoW Forever sale el 4-nov (primeras raids 9-dic) y Overgear ya se prepara para él. **Decir «self-play», nunca «jugamos
  por ti» ni compartir cuenta.** Mostrar captura de overgear.com/games/wow; código visible y sin recortar; tono neutro o
  positivo 30 días. Escoger UNA vía concreta (M+, raids, PvP o powerleveling).

### Campaña 2: WoW Forever Coaching (brief recibido el 26-oct-2026; sustituye a la de 12.1.5)
- Brief: `C:\Users\jaire\Downloads\OVERGEAR — Integration Brief WoW Forever Coaching.pdf` (4 págs.). Contacto: Arseny Blokhin.
- Producto: **coaching self-play** de WoW Forever. Juegas tú tu personaje; un pro verificado (con ID, probado, incluso de
  guilds world-first) guía y corrige **por voz** (o texto). Sesiones 1 a 1 **por hora**, sin programa fijo. **PvE** (tácticas de
  jefes y mazmorras nuevas, plan de equipo pre-banda) o **PvP** (duelos, matchups de clase, campos de batalla); en ambos:
  talentos, build, addons, rotación y cooldowns **explicados**. EU y US; soporte ~2 min 24/7; inicio medio 30 min; 1,5 M pedidos.
- Idea central: «nadie se atasca por ser malo, sino porque nadie le dijo qué hacía mal»; las guías cubren el caso general,
  nunca TU personaje. En Forever el equipo no caduca (progresión en 60 por parches, sin expansiones): los vicios de las
  primeras semanas se quedan; corregir pronto sale más barato.
- Contexto: Forever sale el **4-nov**; bandas el **9-dic**: Barrow Deeps (10) y Hyjal Summit (20). Ventanas: fin de beta
  (22-oct) → lanzamiento = planear clase/build; 4-nov → 9-dic = llegar a 60, mazmorras, equiparse.
- **Obligatorio:** decir que el código da un descuento **MAYOR que el habitual, solo por un mes**, ligado al lanzamiento de
  Forever; **screencast de overgear.com/games/wow-forever/coaching** (en `nucleo/apoyos.py`: `web=` de esa URL); código bien
  visible y el creativo sin recortar; tono neutro o positivo 30 días. Si critican: «es coaching; juegas tú todo el tiempo».
- El % y el **creativo personalizado con el código** los manda el integration manager (correo de Warcraft); sin ellos no se
  cierra el segmento.
- Kit de marca (doc «How to Use Overgear Brand Assets»): Background en bucle de 20 s como capa de fondo; encima logo de
  esquina, offer cards (la de 2 tarjetas es la habitual), packshots para abrir/cerrar, reseñas reales y USPs **en pares**
  (.mov o .mp4 con croma). Primero la idea y el guion, luego elegir assets; nunca construir el guion alrededor de ellos.
  Para coaching ya hay `top-coaches.mp4` y `trust-coaching.mp4` en `D:\Cronicas de Warcraft\Overgear\`.
- 26-oct: el usuario quiere cambiar a esta campaña el segmento de los 2 privados de reserva (`wow_clases_ocultas`,
  `wow_pistas_futuro`), que llevan la campaña vieja.
- **28-oct: kit NUEVO de Forever sin aplicar.** El brief enlaza «How to Use Overgear Brand Assets»
  (docs.google.com/document/d/1b5ixAUfNWgLMLPRplZvldacGnN7UjPasZ7jAsfIpWEE) → carpeta de Drive
  `1yBNH0CeDzoNqRx4axic9enLJqsxiQqWr`, que tiene una subcarpeta nueva **«WoW - Forever (nov)»** (subida el 28-oct):
  `logo-light-bg-small_wow-forever.mp4`, `cards-1-coaching_green-screen_wow-forever.mp4` (tarjeta nueva de coaching),
  `cards-2_green-screen_wow-forever.mp4`, `packshot-logo(_greenscreen)_wow-forever.mp4`, `packshot-text(_greenscreen)_wow-forever.mp4`,
  `Reviews_v3_redscreen_march_wow-forever.mp4` (croma ROJO), `2 pair_green_wow-forever.mp4`; su carpeta Background está vacía
  (sigue el Background general). Los promos actuales usan solo los genéricos de dic-2025 (`Background`, pares 1-3,
  `cards-carousel`, `packshot-logo`), una CAPTURA fija de la página de coaching (el brief pide SCREENCAST en movimiento de
  overgear.com/games/wow-forever/coaching) y el creativo viejo con CRONICAS10. Nunca se han usado Reviews, logo de esquina,
  packshot-text ni cards-2. Falta que Alice mande el creativo personalizado con el código y el % de Forever.
  Listado recursivo de la carpeta pública: `embeddedfolderview?id=<carpeta>` (sin cuenta).
  **Descargados el 28-oct a `D:\Cronicas de Warcraft\Overgear\Forever\`** (9 archivos, 1920x1080 a 25 fps, sin alfa:
  croma verde salvo Reviews en ROJO). Packshot-text = eslogan nuevo «GET COACHED NOW · PLAY BETTER FOREVER» + Trustpilot
  4,9 + «overgear.com»; packshot-logo (7 s) con y sin fondo; logo de esquina (12 s, abajo a la izquierda); reseñas reales
  de 2 tarjetas + Trustpilot 4,9 (4 s); par de USP «Top coaches on the market» + «ToS-friendly» (4 s); tarjetas 1 y 2
  (4 s). Para usarlos en un video, copiarlos a `videos/<v>/medios/_overgear/` como los genéricos.
  **Aplicados el 28-oct** en los `efectos.py` de `wow_clases_ocultas` y `wow_pistas_futuro` (`medios/_overgear/forever/`):
  logo de esquina en bucle todo el anuncio (`bucle=True`), par Top coaches/ToS, tarjeta de coaching, reseñas con
  `croma="rojo"` y packshot-text en lugar del packshot-logo; los pares genéricos 1-3 fuera. El croma de `secuencia_fx` subió
  de umbral (el verde de Trustpilot se transparentaba). Falta re-renderizar los dos (privados de reserva) cuando llegue el
  código: cambiar `CREATIVO, CREATIVO_DESDE` en sus `efectos.py` y la voz de `overgear_5/6`, y un solo render con todo.
- **Promo en INGLÉS para Overgear (28-oct, petición del usuario):** `videos/overgear_promo_en/promo.py` (57,7 s, ElevenLabs
  George `JBFqnCBsd6RMkjVDRZzb`, eleven_v4_turbo; versión inglesa del texto aprobado de `wow_clases_ocultas` + kit Forever +
  música promo) → `salida/overgear_promo_EN.mp4`. Lleva CRONICAS10 y el creativo viejo hasta que llegue el código nuevo:
  cambiar `FRASES[6]` y `CREATIVO` y volver a correrlo (solo regenera las frases cambiadas). **Aprobado por el usuario
  (28-oct) pero NO se manda todavía:** se queda así hasta que llegue el código nuevo, se pone en el promo y en los videos.
- **28-oct, respuesta de Alice:** creativo del código `CRONICAS10_forever.mp4` (Drive de a.blokhin@overgear.com; copia en
  `D:\Cronicas de Warcraft\Overgear\Forever\` y en `medios/_overgear/` de los 2 privados): rótulo de 10 s en VERDE, 2000x1080
  sin audio — escudo → «overgear» → «-10% WITH PROMO CODE CRONICAS10» (2,5-6 s) → «LINK IN THE DESCRIPTION». **Mismo código y
  mismo 10 % que antes**, así que la voz en español no cambia («diez por ciento») y NO se dice «mayor que el habitual» (el
  creativo no lo respalda). Se usa con `croma=True` encima del clip, entrando 2,5 s antes de «CRONICAS10». **Fechas de
  noviembre: 1, 4, 5, 7 y 9-nov** (5 integraciones). Hecho el mismo día: re-render de los 2 privados (2hdnW7T5dl8,
  Hx0eAoY4szk; los anteriores siguen en privado) y promo en inglés con el creativo nuevo («special discount, for one month
  only» + «ten percent off»), listo para mandar a Overgear.
- **29-oct, corrección de Alice al promo en inglés:** «necesitamos usar otro fondo» → detrás del logo, tarjetas, reseñas,
  packshot y código va el **fondo de marca** `Background/Background.mp4` (Drive de recursos, 20 s, degradado morado con
  partículas; copia en `videos/wow_primera_semana/medios/_overgear/background/`; en bucle, cuadro entero, PRIMERO en la lista
  de FX para quedar debajo), nunca un clip de gameplay. Enlace de la descripción por integración: **`https://overgear.s.gy/CRONICAS/1`**
  para la del 1-nov (las demás fechas: pedirle el suyo si no llega). Tras este cambio no hace falta reenviar para aprobación.
- **2-nov, segunda corrección de Alice: logo de esquina BLANCO.** `logo-light-bg-small_wow-forever.mp4` ya no está en Drive;
  en su lugar va `white-og-small-logo.mp4` (subcarpeta «WoW - Forever (nov)/Logo», mismo formato: 1920x1080, 25 fps, 12 s,
  croma verde, misma posición; copia en `D:\Cronicas de Warcraft\Overgear\Forever\`). Aplicado a los 4 videos de noviembre
  (re-render del tramo og y resubida). Enlaces por integración: 1-nov `/CRONICAS/1`, 4-nov `/2`, 5-nov `/3`, 7-nov `/4`,
  9-nov `/5` (el enlace va con la FECHA, no con el video: si se intercambian fechas, se intercambian enlaces).
- **NUNCA decir «no compres oro» ni hablar mal de la compra de oro/boosts en un video con Overgear (el usuario, 28-oct-2026):** Overgear vende oro y servicios; en `wow_primera_semana` se cambió por datos de la montura. Tono neutro o positivo con el sector.
- **«Incluye promoción pagada» obligatorio (31-oct-2026):** los 4 videos de noviembre estaban sin marcar; `yt subir`/`yt aplicar` lo marcan solos si la descripción dice PATROCINADO (`promocion_pagada()` en `nucleo/youtube.py`; `"promocion_pagada": false` en youtube.json lo desactiva).
- Trato y pagos: Alice Garner (Ansvery, ag@ansvery.agency) en cronicas.warcraft@gmail.com; 75 US$/integración + 20 US$ por
  1 000 vistas (18-sep-2026); factura PayPal con los enlaces de los videos.

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
- [x] S2b (13-oct): apoyos (`nucleo/apoyos.py`, `fab.py <v> apoyos`) + 3 MG por código (`nucleo/mg_wow.py`) como capa de
  `efectos.py`; Overgear con croma + tramo intacto (FX `video`, PISTAS `voz=True`). Receta: `docs/estilo_secuencia_yt.md`.
- [x] Montaje con capa de efectos y casilla de subtítulos (`fab.py <v> fx montaje`, `docs/panel.md`).
- [◐] S2c (13-oct): vista «Montaje» en el panel ✅ timeline viva + monitor + voz (`docs/panel.md` § «Montaje»); falta «cambiar clip» = `bajar N --q` desde el bloque y ver los apoyos.
- [x] S3: comercial Overgear (narración propia + código con nuestra voz sobre la imagen 33,0-40,0 s del creativo) en
  `wow_clases_ocultas`; voz con `FONETICA` (docs/voz.md § Applio); `reajustar` para rehacer voz sin renumerar clips.
- [x] Pantalla final de cada canal mudado: `canales/<alias>.json` → `pantalla_final` (copias en
  `E:\FabricaAnimaciones\pantallas_finales\`, de `C:\googleimagenesutopilot.json` → `endScreenClipPath`); `final` la anexa.
- [ ] `docs/estilo_broll_wow.md`, tabla de CLAUDE.md, memoria; luego Tamriel y Runa (Chatterbox).
