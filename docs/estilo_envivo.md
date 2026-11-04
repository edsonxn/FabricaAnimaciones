# EN VIVO: directo generado y editado en tiempo real (idea del usuario, 4-nov-2026)

Formato nuevo para Crónicas de Tamriel (y luego Warcraft/Runa): un directo que no se acaba. El usuario da un tema y la
fábrica genera video en tiempo real (clips del canal, pegatinas reales, avisos y fichas del kit del canal, narrador) con un
búfer por delante; desde una ventanita se cambia el tema y el video gira hacia él. Meta: en un directo de YouTube el público
vota el tema de los minutos siguientes. **Regla del usuario: debe parecer lo más posible un video del propio canal** (letra,
avisos, fichas y pegatinas del kit de Tamriel, no un estilo genérico). Voz por ahora: **voz de Windows** (OneCore Raúl
es-MX), nada de ElevenLabs para no gastar créditos.

```
python fab.py envivo [canal] [--tele] [--tema "…"] [--modelo sonnet|haiku] [--voz Raul|chatterbox:Sarcastica] [--cada-min 3] [--chat-youtube <id>] [--abrir]
  pantalla (OBS: fuente de navegador): http://127.0.0.1:8790/?auto=1     panel: http://127.0.0.1:8790/admin   (simple: /control)
```
En el panel de vista previa: `.claude/launch.json` → «envivo».

## Cómo funciona (nucleo/envivo/)
- `servidor.py` Flask + despachador con **`GUIONISTAS = 2` llamadas a la vez** y búfer de `BUFER = 2` bloques (+1 en
  escritura). Cada bloque propone 2 `proximos` subtemas; cada guionista toma uno y sabe qué escriben los otros («EN
  PARALELO… no lo toques»). Los bloques entran a la cola en orden de despacho (`seq`). Cambio de tema desde el control =
  tira el búfer menos 1 bloque de **relleno** y corta las escrituras en curso; por votación = conserva 1 bloque marcado
  `conservado`. El primer bloque de un tema nuevo (o del arranque) es corto (4 frases) para que llegue antes. Todo lo
  dicho queda en `_sesiones/<fecha>/guion.jsonl` (para cortar después un video o Shorts del directo).
- `director.py` escribe cada bloque (6 frases, ~35-48 s de voz) con `claude -p` (suscripción, sin API de pago) desde carpeta
  vacía, sin MCP/hooks/CLAUDE.md, `MAX_THINKING_TOKENS=0` y `--effort low`; **sonnet por defecto** (ver «Medido»). Elige por
  frase: pegatina del disco o `buscar` en la wiki (Fandom), clip, etiqueta en español, aviso (`rotulo`) y 1 ficha de
  inventario con **negritas**. Opciones de votación. Nunca se despide ni vuelve a saludar (el directo no se acaba).
- `biblioteca.py` reutiliza lo que el canal ya tiene: `videos/tes_*/pegatinas` (+ `_rec` recortadas), `medios/scene-*.mp4`
  con el texto de `beats.json`, OST de `audio/ost`. Las pegatinas usadas salen del catálogo un rato (evita repetir).
- `voz.py` SAPI + voces OneCore (Raúl), un .wav por frase; su duración marca el cambio de imagen.
- `pantalla.html` canvas 1920×1080 con el kit de `mg_tes.py`: Bahnschrift Condensed (servida en `/fuente/`), humo negro
  difuminado, separadores con rombo, hueso/gris/sangre; avisos tipo «misión iniciada» arriba al centro; ficha de inventario
  arriba a la derecha; pegatinas carta / silueta / camafeo / legajo / grande (media pantalla; las fotos anchas se encierran
  dentro del cuadro); OST con ducking; votación abajo a la derecha. **Cambio de tema:** cada bloque lleva `ver`; lo precargado
  del tema viejo pasa a `relleno` (suena solo si el nuevo aún no está, nunca pantalla de espera) y en cuanto llega el
  bloque nuevo se salta a él en el siguiente cambio de frase. `control.html` = la ventanita (tema, sugerencias, votación
  simulada, pausa, guionista, registro).

## Probado (4-nov-2026)
Arranque, clips, pegatinas de los 5 estilos, fichas, votación (aviso «EL CHAT ELIGIÓ» → bloque conservado → «EL CHAT
DECIDIÓ», sin hueco). **Cambio manual verificado en pantalla** (traza de `seg/idx/siguiente` en el navegador): el bloque
precargado viejo pasa a relleno, el viejo sigue sonando sin hueco y el nuevo entra en el siguiente cambio de frase
(15:51:38 cambio → 15:52:05 listo → 15:52:06 al aire con haiku; desde la ventanita y con sonnet: 15 s). Acentos bien desde
`/control` y urllib (curl de Git Bash los manda mal).

## Medido (4-nov-2026)
- `claude -p` cuesta **~8 s solo de arranque**; con un guionista, 6 frases tardaban 23-35 s (haiku) para ~37 s de voz y el
  búfer se vaciaba (0 s). Con 2 guionistas en paralelo: **búfer 90-127 s** en régimen.
- **sonnet vs haiku** (mismo tema, sin «pensar»): sonnet 12-17 s por bloque (haiku 23-35 s) y **mucho mejor guion**: lore
  correcto y el sarcasmo del canal («un héroe nórdico con más fama que pruebas, como todo buen héroe»). Haiku metía errores
  (Paarthurnax en Alto Hrothgar; «en Skyrim no se pueden domar dragones», cuando Dragonborn deja montarlos; Numinex/Numidium)
  y se despedía a mitad del directo. → **sonnet por defecto**, haiku de respaldo. Ojo: gasta más plan (~1 llamada por bloque).

## Costos (medido el 4-nov-2026 con `claude -p --output-format json`)
Todo corre con la **suscripción MAX** (`claude -p`): no hay factura aparte, pero cada llamada gasta del límite semanal del
plan. La cifra en US$ es lo que costaría lo mismo pagado por API (sirve para comparar y para vigilar el plan).

| Pieza | Qué usa | Por llamada (medido) | Por hora de directo |
|---|---|---|---|
| Guion de bloque (6 frases, ~45 s de voz) | sonnet | 13-16 s · ~0,065 US$ (≈ 14 000 tokens de entrada fijos del CLI + ~2 000 del guion; ~1 000 de salida) | ~80-90 llamadas ≈ **5,2-5,9 US$** |
| Respuesta al chat (1-2 comentarios) | sonnet | 12-14 s · ~0,063 US$ | chat moderado ~15 ≈ **0,9 US$**; muy activo ~40 ≈ 2,5 US$ |
| Clasificar comentarios (tanda de hasta 25) | haiku | 6-10 s · ~0,0025 US$ | moderado ~60 tandas ≈ **0,15 US$**; muy activo ~360 ≈ 0,9 US$ |
| (alternativa) guion con haiku | haiku | 26-28 s · ~0,005 US$ | ≈ 0,45 US$, pero lore flojo (ver «Medido») |
| Voz | Windows OneCore Raúl | 0 | **0** |
| Imágenes y clips | disco del canal + wiki Fandom | 0 | **0** |
| Chat de YouTube (`--chat-youtube`) | API de YouTube (cuota gratis de 10 000 u./día) | 5 unidades por lectura | 0 US$ · ~1 200 u./h (≈ 8 h al día) |
| ElevenLabs, Flow, Lyria | no se usan | 0 | **0** |

| (alternativa) voz ElevenLabs `eleven_v4_turbo` | API de ElevenLabs (créditos) | ~0,2 créditos por carácter (cuentas Starter) · 0,04 US$ por 1 000 caracteres | **~54 000 caracteres ≈ 10 800 créditos ≈ 2,2 US$**; con cambios de tema cada 3 min (bloques ya hablados que se tiran) ≈ 13 000-15 000 créditos ≈ **2,6-3 US$** |

**ElevenLabs en el directo (calculado el 4-nov-2026, sin llamadas de pago):** los 117 bloques reales de `_sesiones/2026*/guion.jsonl`
= 71 266 caracteres en 4 248 s de voz de Windows = **16,8 caracteres por segundo** (≈ 60 000 por hora con Raúl). ElevenLabs habla
más despacio (narración real ≈ 900 caracteres/min, `docs/apis.md`), así que una hora de directo pide **~54 000 caracteres**. Con
turbo (0,2 créditos/carácter en las Starter) ≈ **10 800 créditos por hora**, + 20-40 % si el chat cambia el tema cada 3 min
(cada corte tira 1-2 bloques ya sintetizados): **~13 000-15 000 créditos/h**. Saldos de hoy (`python nucleo/tts_eleven.py`):
cuenta 1 = 0, cuenta 2 = 25 711, cuenta 3 = 1 195 → **~1,8-2,5 h de directo en total, y la cuenta 2 es la de los clones**
(narradora de Gaia, El Jefe, Remy Eleven) y de las voces de los videos: un directo de 2 h la dejaría vacía. En dinero (mismo
precio en pago por uso y planes: 0,04 US$ por 1 000 caracteres de turbo) ≈ **2,2-3 US$ por hora**; un plan Starter (6 US$,
150 000 caracteres) da **~2,5-3 h** al mes; Creator (22 US$, 550 000) ~**9-10 h**; 1 h diaria ≈ 1 600 000-1 800 000
caracteres/mes ≈ **65-90 US$/mes**. Si se hace: sintetizar con ElevenLabs solo el bloque que va a sonar (no el búfer entero)
para no pagar los que se tiran, y su caché por texto no sirve (nunca se repite una frase).

**Total equivalente:** con sonnet ≈ **6-8 US$ por hora** de directo (casi todo es el guion); con haiku ≈ 0,6-1,5 US$/h.
En dinero real: **0** extra; el gasto es límite del plan MAX. Medir en la primera prueba de 1 h con `get_usage` (antes y
después) cuánto % semanal se come una hora.
Para bajarlo: cada llamada cuesta casi lo mismo pase lo que pase (~14 000 tokens fijos del CLI; `--system-prompt` corto
apenas lo baja: 0,071 → 0,065), así que **bloques más largos = menos llamadas** (10 frases ≈ −40 % por minuto). Lo que
no conviene: más guionistas en paralelo de los necesarios ni subir el búfer (los cambios de tema tiran bloques ya pagados).

## Chat y panel de administración (el usuario, 4-nov-2026, tarde)
«Que la IA interactúe con los comentarios… cada pocos minutos vea lo que más se pide (del tema; lo que no, se descarta) y
cambie el tema; que muestre en pantalla los que considere buenos; un panel para ver los comentarios en tiempo real,
proponer tema y comentar como espectador.»
- **Panel `/admin`** (lo abre `--abrir`): chat en vivo con la etiqueta de la IA por comentario (pedido · pregunta ·
  agradecimiento · crítica · comentario · fuera · spam · tóxico, el tema normalizado y la nota), botones por comentario
  (mostrar · fijar · que lo conteste · ocultar), caja para **comentar como espectador** con votos rápidos 1/2/3 y una
  **ráfaga de prueba** (8 comentarios variados), pantalla espejo (`/?monitor=1`: sigue lo que está al aire sin pedir bloques
  ni sonar), tema (cambiar ya / proponer para el próximo corte), **cuenta atrás del corte**, ranking de lo más pedido,
  cada cuántos minutos y mínimo de pedidos, votación, pausa, guionista y registro.
- `chat.py`: los comentarios entran por `POST /api/comentario` (panel) o por `FuenteYouTube` (`--chat-youtube <id del
  video>`, APAGADA por defecto: `liveChatMessages.list` = 5 unidades, mínimo 15 s entre lecturas ≈ 1 200 u./h, tope 6 000).
  «1/2/3» con la votación activa = voto directo. Un hilo clasifica en tandas con **haiku** (~5-8 s por tanda). Cada
  `--cada-min` (3 por defecto) se cuenta la ventana: si un tema llega al mínimo de pedidos (2), cambia el tema
  (origen «chat», conserva 1 bloque) y **el puente nombra a quienes lo pidieron**; si no, manda la propuesta del panel o sigue.
- **Respuestas al chat:** un guionista extra escribe un bloque corto `r###` (1-2 comentarios + 1 frase de vuelta al tema,
  8-17 s) que se cuela al frente de la cola: suena justo después del bloque al aire. Reglas de CLAUDE.md § COMENTARIOS:
  agradecer y recordar que se leen todos; crítica exagerada = burla disfrazada (del comentario, nunca de la persona); los
  pedidos no se contestan uno a uno. Un cambio de tema NO tira las respuestas ya escritas.
- **Pantalla:** el comentario que contesta la voz sale como tarjeta tipo YouTube oscuro (como `comentarios.tarjeta`) con
  rótulo del kit («PREGUNTA DEL CHAT», «CRÍTICA DEL CHAT»…), a la izquierda; las pegatinas se van a la derecha. La IA enseña
  sola los comentarios buenos (uno cada ≥ 20 s, 8 s, nunca encima de una ficha). Fijado = tarjeta chica bajo «EN VIVO».
- **OBS:** fuente de navegador `http://127.0.0.1:8790/?auto=1`, 1920×1080, «Controlar audio vía OBS» activado. El panel va
  en otro monitor o en el teléfono (misma red: cambiar `127.0.0.1` por la IP de la PC requeriría `--host 0.0.0.0`, pendiente).
- Probado de punta a punta (4-nov): ráfaga → 5 contestados por su nombre en 8-17 s cada bloque → corte a los 1,5 min con 3
  pedidos → «Gracias a @Kiara_Lore y @Ulfric_Fan por pedir el cambio…». Spam y GTA 6 descartados.
  Lore: alguna respuesta mete un dato dudoso («nirnroot carmesí en cuevas de Cuarzo Rojo»; está en Blackreach): vigilar.

## Voz con Chatterbox (medido el 4-nov-2026, RTX 4060, voz `Sarcastica` = la de Tamriel antes de Johnny)
`python fab.py envivo --voz chatterbox:Sarcastica` (cualquier archivo de `C:\chatterbox_voices`; preview «envivo-chatterbox», puerto
8791). `nucleo/envivo/voz_chatterbox.py`: mismo contrato que `voz.py` (un .wav por frase + duración), modelo cargado UNA vez
en el servidor (~48 s, ~3-4 GB de VRAM), GPU con candado, FONETICA unida de los `videos/tes_*/guion.py` (323 palabras; la del
video más reciente gana), ajustes de Tamriel (exaggeration 0,6 · cfg 0,35 · temp 0,75). `/api/estado` da `voz_factor`.
- **Tal cual NO alcanza:** factor **1,065** (segundos de síntesis por segundo de audio; 24 frases reales, 1,01-1,19). Un
  bloque de 6 frases (~46 s) tarda ~49-55 s; con 2 guionistas a la vez la GPU hace cola: 101 s de audio en 106 s. El búfer
  se vaciaría ~4 min por hora. Trocear por frase NO lo arregla (solo adelanta la 1.ª frase, lista a ~9 s): es ritmo, no espera.
- **Dónde se va el tiempo:** T3 (el autorregresivo, Llama de 30 capas, 25 pasos = 1 s de audio) 85 %; s3gen 15 %; marca de
  agua ~0. T3 va a ~26 pasos/s con la GPU al 13 %: lo frena lanzar cientos de kernels pequeños por paso, no el cálculo.
  fp16/bf16 lo EMPEORAN (1,13-1,30); TF32 igual. Triton/torch.compile no hay en Windows.
- **Arreglo: `nucleo/envivo/chatterbox_grafo.py`** captura el paso de decodificación de T3 en un **CUDA Graph** con caché
  estática (1 600 posiciones, se captura una vez y vale para todas las frases). **Mismo audio exacto** (Whisper transcribe
  igual, mismas duraciones, misma semilla) y **factor 0,74** (0,72-0,79): 45 s de audio en ~33 s. Si el grafo falla, vuelve
  solo al bucle original. Medido también dentro del servidor con Flask y los guionistas: **0,75-0,78**.
- Con 0,75 la GPU da ~1,3 s de audio por segundo: alcanza para el directo con ~30 % de margen (incluidas las respuestas al
  chat), pero sin mucho más. Un bloque de un tema viejo deja de ocupar la GPU en cuanto cambia el tema (`vigente`); las
  respuestas al chat (`r###`) no se cortan.
- **Prueba en el navegador (17:13-17:15, cortada por pausa del usuario):** modelo listo, 1.er bloque (4 frases) al aire a
  los ~26 s de pedirlo. No llegó a verse el paso al 2.º bloque. **Riesgo visto en la traza:** el búfer siguió en 0 durante
  el 1.er bloque porque los 2 bloques siguientes se sintetizan A LA VEZ frase a frase (el candado los intercala) y ambos
  terminan tarde (~66 s de GPU) → probable hueco de ~30-40 s al arrancar. Pendiente: que el candado dé prioridad al bloque
  con `seq` más bajo (el que sale antes), y entonces repetir la traza 10 min con un cambio de tema y una ráfaga de chat.

## En curso / pendiente
**Pausado por el usuario (4-nov-2026, noche).** Comentarios + panel `/admin`: PROBADO de punta a punta en el navegador (ráfaga de 8 comentarios → clasificación con haiku, spam y GTA 6 descartados → 5 contestados por su nombre en bloques `r###` → corte a los 1,5 min con 3 pedidos y puente con los nombres; mostrar, fijar y espejo `/?monitor=1` verificados con capturas) y commiteado (`2107675`). Falta: probarlo con el usuario, el chat de un directo real de YouTube (`--chat-youtube`, sin probar), verlo a 1500 px de ancho (solo se vio el diseño de una columna) y la sesión «envivo-voces» (ElevenLabs/Chatterbox), también en pausa.
1. Probarlo con el usuario: `python fab.py envivo --abrir` (pantalla OBS `:8790/?auto=1` + panel `:8790/admin`).
2. (el usuario, 4-nov noche) ElevenLabs: calculado (fila en «Costos»: ~2,2-3 US$/h, los saldos dan ~2 h). Chatterbox: con
   CUDA Graph va a 0,75× (§ «Voz con Chatterbox»); **PAUSADO por el usuario a mitad de la prueba**: falta la prioridad del
   candado por `seq`, la traza de 10 min sin huecos y el commit (`voz_chatterbox.py`, `chatterbox_grafo.py`, `servidor.py`,
   este doc, preview «envivo-chatterbox» en `.claude/launch.json`).
3. Directo de YouTube real: la lectura del chat ya está escrita (`--chat-youtube <id>`) pero sin probar contra un directo.
4. Los subtemas en paralelo a veces se pisan (dos bloques sobre Numinex): el prompt ya pide personajes que no salgan en el
   bloque; vigilar.
5. Voz: OneCore Raúl por ahora; si el directo funciona, valorar una voz del canal.

## Tele, control remoto del teléfono y frase puente (4-nov-2026, noche; probado de punta a punta)
`python fab.py envivo --tele` (preview «envivo-tele») = el directo en el Google TV con audio + la app del teléfono. Lo que se hizo:
- `servidor.py`: frase puente inmediata (`_puente`, bloque `p###` `inmediato` al frente de la cola, voz del motor activo,
  sin Claude), `lat_min`/`lat_max`/`puente` en `/api/ajuste` y `/api/estado` (+ `latencias`, `bufer_det`, `peg_al_aire`,
  `en_curso`), latencia REAL medida al salir al aire (`al_aire_medir`, registro «LATENCIA puente/bloque»), `--tele` (0.0.0.0 +
  manda `http://<ip>:8790/?auto=1` a la tele), desde la red solo GET de pantalla + `POST /api/progreso` (403 al resto),
  ruta `/movil`. Arreglada la barra de `--voz` (`C:\\chatterbox_voices`).
- `pantalla.html`: no salta a lo nuevo antes de `lat_min`; a `lat_max` corta la frase vieja (fundido 0,3 s); el bloque
  completo no repite el aviso de la frase puente; estado cada 1 s.
- `movil.html` (NUEVO): control remoto del teléfono (al aire + pegatina, búfer en barras, tema ya / próximo corte, ranking,
  chat en vivo con acciones, comentar y 💡 sugerir como espectador, latencia mín/máx, frase puente sí/no, pausa, votación,
  guionista, corte del chat, registro). Rutas relativas: sirve en `:8790/movil` y por la puerta en `/envivo/movil`.
- `nucleo/panel_remoto.py` (la puerta): `/envivo/…` → 127.0.0.1:8790 con la misma clave; carpeta de dominio `envivo/`
  (`clicknbusiness.com.mx/envivo/`). FALTA relanzar la puerta (matar `puerta_pid` de `panel_remoto.json` y
  `python nucleo/panel_remoto.py iniciar --republicar`).
- `nucleo/tele.py`: `web(url)`, `cerrar_web()`, `ip_hacia_tele()`.
- **Puente TV** (`D:\PuenteTV\tv`, Tablero.kt + PuenteService.kt): `POST /web {"url"}` abre la página a pantalla completa en el
  WebView del tablero (sin tocar el tablero guardado), `POST /web/cerrar`. APK compilada y copiada; la tele ya tiene la
  1.261104.1730. (APK anterior en el scratchpad de la sesión.)
**Probado (4-nov, 17:33-17:39):** la tele abrió `http://192.168.0.237:8790/?auto=1` sola y fue avanzando frases y bloques
(búfer 86-133 s); desde la red, `POST /api/tema` = 403 y `GET /api/estado` = 200. **Latencia real** (registro «LATENCIA»,
`latencias` en `/api/estado` y en la app):

| Ajuste | Frase puente lista | Puente al aire | Bloque nuevo al aire |
|---|---|---|---|
| antes (sin puente) | — | — | 15-27 s |
| mín 3 s · máx 8 s | 0,8 s | **7,1 s** | **11,0 s** |
| mín 0 · máx 2 s | 0,7 s | 5,6 s (página vieja en caché) | 16,4 s |
| mín 0 · máx 2 s (repetido) | 0,8 s | **3,6 s** | **11,1 s** |

El puente sale ~1,5 s después del máximo (sondeo del estado cada 1 s + fundido de 0,3 s + cargar el audio en el Chromecast).
El bloque completo tarda lo que tarda sonnet (10-16 s); la frase puente dura 3-4 s, así que entre ella y el bloque puede
sonar el relleno del tema viejo unos segundos. **Por defecto: mín 3 s, máx 8 s** (no corta frases casi nunca); para
reaccionar rápido, mín 0 y máx 2-3 en la app.
- **App fuera de casa:** por la puerta con la misma clave del panel: `clicknbusiness.com.mx/envivo/` → túnel → `/envivo/movil`
  (probado por el túnel ngrok: sin clave 401; con clave, app + estado + comentario). En casa también `:8790/movil` en la PC.
- **Ojo:** `POST /web/cerrar` cerró la conexión sin respuesta (la tele siguió contestando): comprobar que cierre; si no, Atrás.
- No se vio la tele en persona: falta que el usuario confirme que se oye y que el WebView del Chromecast va fluido.
- Pendiente: mandarle la app «por rayo» (preguntar qué es) y, en la 1.ª prueba larga, medir el % del plan MAX en su chat.

## Pedido del usuario (4-nov-2026, noche) — pendiente
- **RECORDAR en la PRIMERA prueba:** medir el % de uso del plan MAX con el medidor de su chat (claude.ai, uso de la sesión de
  5 h y semanal): anotar antes y después de 15-30 min de directo y extrapolar a 1 h. Tomar como referencia la sesión de 5 h.
- El directo NO necesita una conversación abierta: `fab.py envivo` es un servidor de Python que llama solo a `claude -p` (la
  sesión iniciada de Claude Code en la PC, misma suscripción y mismos límites). Basta con la terminal abierta.
- **Tele:** que el directo se pueda ver para las pruebas en el Google TV con Puente TV (`fab.py tele`, `docs/tele.md`).
- **App del teléfono «control remoto»** (se la mandan «por rayo»: confirmar con él qué es «rayo» si no está claro): controles
  importantes (pausa, tema, votación, guionista, búfer), **comentar y sugerir temas como espectador en tiempo real**, y
  **latencia del cambio de tema regulable con mínimo y máximo** desde el teléfono.
- Latencia medida hoy: cambio de tema → bloque nuevo al aire en **15-27 s** (sonnet 15 s). Idea para bajarla: frase puente
  inmediata («¡el chat manda: ahora X!») con voz de Windows en ~2-3 s, mientras se escribe el bloque completo.
