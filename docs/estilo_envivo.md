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

**Prueba REAL de 10 min (5-nov-2026, 08:11-08:20, sonnet, 2 guionistas, ElevenLabs el Profeta → Johnny, tele + app del teléfono):**
14 bloques + la despedida en 9,5 min. **ElevenLabs: 1 824 créditos** (15 372 → 13 548) ≈ **11 500 créditos/h**, dentro de lo
calculado. **Plan MAX: semanal 42 % → 42 %** (menos de 1 punto); **ventana de 5 h: 2 % → 9 %** en ~20 min de reloj, pero esa cifra
incluye la sesión de Claude Code que dirigía la prueba (Opus con ~190 mil tokens de contexto por turno), así que el directo solo gasta
bastante menos. Para aislarlo: medir otra vez sin ninguna sesión trabajando al mismo tiempo.
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

## Voces: ElevenLabs, relevo visible y discusión (4-nov-2026, noche; parte del pedido 1 de la cola)
- **Las 7 voces** (biblioteca compartida de ElevenLabs, ya usadas en `tes_dwemer_desaparicion`): Johnny (actual), Edoardo, Hope,
  José, Mario, MariCarmen y el Profeta, en `voz_eleven.VOCES`. «El Humano tras el Telón» es el clon del usuario (cuentas 2 y 3):
  no entra como narrador. Valen en la cuenta 2 o 3 (la 1 está en 0; `tts_eleven.post` salta sola).
- `voz_eleven.py`: misma firma que `voz.py`, `eleven_v4_turbo`, PCM 24 kHz → .wav, 4 frases en paralelo, sin
  `[whispers]`/`[excited]`/`[shouts]`; si falla o no hay saldo, esa frase sale con Windows. Gasto medido: **0,2 créditos por
  carácter**; un bloque de ~700 caracteres ≈ 140 créditos y **5,7-6 s** de síntesis.
- **Voz justo antes de sonar** (Windows y ElevenLabs): el bloque se escribe sin voz y se sintetiza al salir de la cola
  (`_voz_al_salir`): no se paga lo que se tira al cambiar de tema, y un cambio de voz alcanza también al búfer. Chatterbox
  (lento) sigue sintetizando al producir.
- **Relevo** (`cambiar_voz`; `/api/ajuste {"voz": "eleven:Hope"}`): bloque `v…` al frente de la cola, la vieja se despide y
  la nueva se presenta; la pantalla pone la placa «NARRA · NOMBRE» (abajo a la izquierda, sobre la barra del tema), la vieja
  sale, la nueva entra y late, con la cinta «RELEVO DE NARRADOR». Probado: **al aire a los 11 s** (al acabar la frase en curso).
- **Relevo automático** (`auto_relevo`, `auto_min` = 5): pasado ese tiempo entra otra voz al azar, sin repetir; con poco
  saldo (< 3 000) solo voces gratis. **Discusión** (`/api/ajuste {"discusion": ["eleven:Johnny", "eleven:Hope"]}`): el
  director escribe un intercambio con `"voz"` por frase; probado (bloque b006 con Hope y Johnny), pero entra ~3 min después
  porque el búfer ya estaba escrito. Selector, saldo, relevo automático y discusión en `/admin` y en la app del teléfono.
- Prueba del 4-nov (20:30): 736 créditos en total. Saldo de ElevenLabs a la vista en `/api/estado` (`eleven`).
- Falta: que el chat elija la voz (etiqueta «pedido de voz» en `chat.py`, contarla en el corte, la voz nueva nombra a quien la
  pidió, voz en la votación de vez en cuando, interruptor y tiempo mínimo entre cambios); que la discusión entre antes
  (rehacer el búfer al activarla); 3 voces; verlo en la tele (sigue sin abrir la página desde las 20:07).

## MODO SIN PÚBLICO: callado cuando no hay gente (el usuario, 5-nov-2026)
Palabras del usuario: «mientras no haya gente no se gasten tokens de elevenlabs, que esté callado y de vez en cuando solo se
genere un bloque real, y en cuanto llegue gente que el narrador los salude y les explique la dinámica de que deben comentar
sobre el tema que quieren escuchar».
- **Modos** (`Directo.publico`, en `/api/estado` → `publico`):
  - `despierto` = el directo normal.
  - `callado` = sin guionista continuo y sin voz. La pantalla sigue viva:
    - clips del tema cada 12 s y pegatinas del tema cada 8 s (`callado_media`);
    - la OST;
    - el rótulo «Comenta el tema que quieres escuchar» cada 30 s;
    - la cartela abajo «COMENTA EN EL CHAT EL TEMA QUE QUIERES ESCUCHAR · TEMA AHORA: …».

    Cada `callado_cada_min` (6 por defecto) entra UN bloque real con voz, para que quien llegue por un clip no encuentre
    algo muerto. Ese bloque usa la voz vigente o, con `voz_callado = windows`, la de Windows (gratis).
- **Quién hay**:
  - Espectadores concurrentes del directo de YouTube (`FuenteYouTube._espectadores`: `videos.list
    liveStreamingDetails.concurrentViewers`, 1 unidad por minuto). Se activa con `--chat-youtube <id>` o con el campo
    «enlace o ID del directo de YouTube» al INICIAR.
  - Cada comentario que entra (`Chat.recibir` → `Directo.actividad`).
  - Sin YouTube: «espectadores simulados» en `/admin`, o los botones de la app (🔇 No hay gente / 🔊 Hay gente).
- **Sin gente** = espectadores ≤ `umbral` (1 por defecto, para no contar al usuario).
  - Si se INICIA sin gente, arranca callado con un bloque al momento.
  - Despierto, pasa a callado cuando lleva `vuelve_min` (3) sin gente y sin comentarios; al callar se tira el búfer
    (salvo despedida o lo conservado).
- **Llega gente** (sube de `umbral` o alguien comenta): DESPIERTA.
  - El guionista escribe un bloque de BIENVENIDA (`_saludo`) que va al frente de la cola: saluda por su nombre a quien
    comentó y explica la dinámica (comentar el tema de Skyrim o Tamriel que quieren escuchar, el chat decide cada
    `cada_min` minutos, aquí se contesta a quien comenta) y enlaza con el tema actual. Si falla, va uno de respaldo.
  - Mientras se escribe, la pantalla dice «¡LLEGÓ GENTE! UN MOMENTO…».
  - **La voz del narrador por votación no se menciona**: todavía no existe (pedido 1 de la cola). Cuando exista, hay que
    añadirla al saludo.
- **Controles**:
  - `/admin`: segunda barra con el modo y los espectadores, 🔇 Callar, 🔊 Despertar + saludo, automático, espectadores
    simulados, umbral, minutos entre bloques, minutos para volver a callar, voz del modo callado, ID del directo de
    YouTube y el gasto por modo.
  - App: «No hay gente» y «Hay gente» en la tarjeta Directo.
  - API: `POST /api/publico {"forzar", "auto", "sim", "umbral", "cada_min", "vuelve_min", "voz_callado"}`.
- **Probado el 5-nov** con la voz de Windows, haiku y espectadores simulados en 0:
  - arranca callado con un bloque, y la pantalla callada se ve viva;
  - un comentario de «DovahPepe» lo despierta y el saludo lo nombra y explica la dinámica;
  - el saludo sale ANTES que los bloques normales (`siguiente` los retiene mientras `saludando`);
  - a los 30 s sin nadie vuelve a callar y tira lo que se escribía.

  **Falta**:
  - medir la latencia del saludo: en la segunda prueba tardó ~2 min con 3 llamadas a haiku a la vez;
  - probarlo con un directo real de YouTube (`concurrentViewers`) y con ElevenLabs.
- **Registro del gasto por modo** (`publico.gasto`): minutos, bloques escritos (= llamadas al guionista) y créditos de
  ElevenLabs en callado y en despierto.

## INICIAR y DETENER desde el panel (el usuario, 4-nov-2026, noche)
Palabras del usuario: «el panel siempre debe estar activo y desde ahí poder iniciar y detener todo; cuando detenga todo se
deja de escribir guion y generar voz, solo lanza una última de despedida… y deja reproduciendo lo que ya estaba generado».
Añadidos: «un botón para abrir la transmisión en una pestaña» y «un botón para enviar a la tv».
- **`fab.py envivo` arranca el servidor APAGADO**: panel, pantalla, app del teléfono y UDP encendidos y en `0.0.0.0` desde
  el principio. Sin guionista, sin voz y sin gasto; la pantalla enseña la portada «EL DIRECTO EMPIEZA PRONTO» con el primer
  tema. Con `--iniciar` arranca el directo como antes; las configuraciones `envivo-tele*` y `envivo-chatterbox` de
  `launch.json` ya lo llevan, y la `envivo` a secas es el panel apagado.
- Estados (`Directo.encendido`, en `/api/estado`):
  - `apagado`;
  - `arrancando`: carga la voz (Chatterbox, ~20-40 s);
  - `en_vivo`;
  - `cerrando`.
- `POST /api/directo {"accion": "iniciar", "tema", "voz", "modelo"}`. Cada INICIAR es una sesión nueva: carpeta
  `_sesiones/<fecha>`, cola y memoria limpias. Un cambio de tema mientras está apagado queda como el tema del próximo
  INICIAR.
- **DETENER** (`"detener"`):
  - El productor deja de despachar, y lo que se estaba escribiendo se cancela y se tira.
  - Suena lo que ya estaba en la cola (la voz se sintetiza al salir, así que solo se paga lo que se oye).
  - Al final va un bloque de **DESPEDIDA**: el director recibe `Directo.DESPEDIDA`, que levanta la regla de «nunca te
    despidas» y le pide cerrar el tema, dar las gracias, pedir la suscripción y el tema del próximo directo. Si falla, va
    `DESPEDIDA_RESPALDO`.
  - Cuando la despedida ya sonó y la pantalla pide más, el directo pasa a `apagado`. La pantalla pone la cartela «FIN DEL
    DIRECTO · GRACIAS POR ACOMPAÑARNOS · SUSCRÍBETE Y DEJA EN EL CHAT EL TEMA DEL PRÓXIMO» (12 s, kit de Tamriel) y luego la
    portada.
  - Mientras cierra, el chat no cambia el tema, no hay votación ni relevo automático, y los bloques de respuesta al chat se
    tiran.
- **DETENER YA** (`"detener_ya"`): corta en seco. La pantalla ve que `cortes` subió, calla la voz, quita pegatinas y placa
  y vuelve a la portada.
- **/admin**: barra arriba con el estado, tema, voz (las de ElevenLabs llevan «(gasta)» y piden confirmación), guionista,
  «y a la tele», ▶ INICIAR, ■ DETENER (con despedida), ✕ DETENER YA, ↗ Abrir transmisión, 📺 Mandar a la tele y ✕ Quitar
  de la tele, y cuántas pantallas hay al aire. **App del teléfono**: tarjeta «Directo» con Iniciar, Detener y Detener ya
  (arranca con la voz, el tema y el guionista actuales).
- **Dos pantallas se reparten los bloques**:
  - Cada pantalla `?auto=1` se identifica con un `pid` en `/api/siguiente` y `/api/estado`, y el panel lista las que
    avisaron en los últimos 8 s (avisan cada 1 s) (`pantallas`).
  - «Abrir transmisión» y «Mandar a la tele» avisan si ya hay una y ofrecen abrir la nueva como ESPEJO (`/?monitor=1`, no
    consume bloques).
  - `/api/tele {"accion": "poner", "modo": "espejo"}` manda el espejo a la tele.
- **Quitar de la tele**: Puente TV hace `finish()` de `TableroActivity` y su `onDestroy` destruye el WebView, lo que corta
  su JS. El servidor lo COMPRUEBA: si a los 4 s la IP de la tele sigue llamando a `/api/estado`, responde `sigue: true` y el
  panel pide cerrarla con Atrás.
- Probado el 4-nov con la voz de Windows y haiku:
  - portada apagado;
  - INICIAR («Los dwemer», b001 hecho en 23 s);
  - DETENER: se cancelaron las 2 escrituras en curso, la despedida se escribió y sonó, la cartela salió y quedó en
    `apagado`;
  - DETENER YA.

  **Falta probar**: en la tele, «Mandar» y «Quitar» con la comprobación, el aviso de dos pantallas y la despedida con
  ElevenLabs.
- La skill global `envivo` todavía no existe (pedido 3 de la cola): cuando se haga, que use `/api/directo`.

## Arreglos tras la prueba con ElevenLabs (el usuario, 4-nov-2026, noche)
1. **«Frases que debía decir el Profeta las dijo Johnny»**. Había dos causas:
   - La voz se buscaba por las 5 primeras letras del nombre, así que «Profeta» no coincidía con «el Profeta» y caía en la
     voz vigente.
   - La voz se resolvía al SALIR de la cola: si se apagaba la discusión o entraba otra voz antes, todas las frases pasaban
     a la voz nueva.

   Arreglo: `_clave_de_nombre` (sin acentos ni «el/la», acepta «Jose», «Mari Carmen», «Hope (ElevenLabs)») fija la `clave`
   de cada frase al ESCRIBIR el bloque. Un relevo o un cambio de discusión solo afecta a las frases que no llevan voz. Un
   nombre que no se reconoce queda apuntado en la bitácora. `voz_hecha` guarda la lista de claves para no volver a
   sintetizar lo ya hecho.
2. **«A veces se queda congelado el video de fondo»**: el **vigilante** de `pantalla.html` revisa cada 0,4 s si el
   `currentTime` del clip al aire avanza.
   - A los 0,8 s quieto: `play()` otra vez.
   - A los 2 s: cambia a un clip del DISCO distinto (el de la frase, el siguiente o uno de los 30 ya vistos). El enlace de
     YouTube trabado entra en `ytMalos` y no se vuelve a usar.
   - El servidor apunta «VIGILANTE: … → clip del disco (van N)».
3. **«Al cambiar de tema se corta la plática de tajo»**. Antes, a los `lat_max` (8 s) la frase en curso se cortaba con un
   fundido de 0,3 s. Ahora:
   - La frase en curso **siempre se termina** y luego entra la frase puente.
   - Solo una frase a la que, pasado el máximo, aún le queden más de 15 s se recorta, con un fundido de 1,5 s.
   - Las frases puente ya no son un «¡Cambio de rumbo!» seco: cierran el tema anterior por su nombre y enlazan con el
     nuevo («Bueno, y dejando {a} por aquí, que da para otro día…», «Un momento, que el chat manda. Dejamos {a}…»).
   - Falta un analizador de nivel para cortar en una pausa: se descartó porque, con el AudioContext suspendido, puede dejar
     la voz muda en la tele.
- Probado con piezas sueltas: reparto de voces en un bloque simulado y sintaxis del JS. **Falta probar** en un directo real
  con ElevenLabs y en la tele (vigilante con un enlace de YouTube que caduque, y oír que el cambio de tema ya no corta).

## Pedidos del usuario EN COLA (4-nov-2026, noche; en este orden, cada uno con su commit, doc y `fab.py tele aviso`)
1. **Voces de ElevenLabs desde el panel**: «poder elegir 1 de las 7 voces que hemos usado en el canal, y cuando cambie de voz
   que la antigua voz releve el mando y la nueva lo tome… e incluso puedan discutir entre ellas».
   - Juntar las 7 voces de Tamriel (Johnny = actual; `videos/tes_*/guion.py`, `docs/voz.md`, `canales/cronicas_tamriel.json`;
     cuenta de cada una, los clones solo en la cuenta 2). Si no son 7, enseñárselas y preguntar.
   - Selector (Windows / Chatterbox / cada voz Eleven) y saldo en `/admin` y la app; `voz_eleven.py` con la firma de
     `voz.sintetizar`; `eleven_v4_turbo`, corchetes sin `[whispers]`/`[excited]`/`[shouts]`; sintetizar solo el bloque que
     va a sonar; voz de Windows de respaldo si se acaba el saldo o falla.
   - **Relevo visible**: la vieja se despide y pasa el mando, la nueva se presenta; placa «NARRA» + nombre (`mg_tes.narrador`).
   - **Discusión** de 2-3 voces (cada frase con su voz y su placa), desde el panel/app o propuesta por el director.
   - **El público elige la voz**: en `chat.py`, etiqueta «pedido de voz» («que hable Johnny», «que discutan»), contada en el
     corte; al llegar al mínimo, relevo y la voz nueva nombra a quien la pidió; opción de voz en la votación de vez en
     cuando; interruptor y tiempo mínimo entre cambios en panel/app; con poco saldo, el chat solo elige voces gratis.
   - **Relevo automático**: si una voz lleva > 5 min (configurable, con interruptor), entra otra al azar (sin repetir) en el
     siguiente corte de bloque; un cambio del chat o manual reinicia el contador; con poco saldo, solo voces gratis.
   - Anotar el gasto (~2,2-3 US$/h) y avisar en el panel con poco saldo; medir latencia; prueba corta en la tele.
2. **Triplicar los estilos de pegatina** de `pantalla.html` (hoy 5: carta, silueta, camafeo, legajo, grande → 15 o más),
   cada uno con entrada, movimiento y salida propios. Ideas: los de `nucleo/peg_estilos.py` que faltan (reliquia sobre
   runas, banda de cine con los ojos, abanico al enumerar), libro de Skyrim que se abre, cartel «SE BUSCA», fragmento de
   mapa, vitrina con luz, pantalla de carga de Skyrim, lacre, polaroid que cae, tríptico, ventana de humo, papel que se
   rasga, foco en la oscuridad, comparación lado a lado, ficha de bestiario. Kit del canal y profundidad. Rotarlos sin
   repetir y según el tipo de imagen (el director puede sugerirlo). Que no tapen avisos, ficha, barra del tema ni votación.
   Hoja con todos en `previews/`, anotarlos aquí y preguntarle si quiere los mejores en `peg_estilos.py`.
3. **Controlar el directo desde cualquier conversación**: `POST /api/anuncio {texto, modo literal|redactar}` (en el
   siguiente cambio de frase, voz actual + aviso `mg_tes.mision`), `POST /api/mostrar {consulta|ruta|url, estilo?, dur?}`,
   `python fab.py envivo cmd <tema|anuncio|mostrar|comentar|pausa|voz|votacion|estado|parar>` (desde 127.0.0.1 sin código),
   **skill global** `~/.claude/skills/envivo/SKILL.md` (comprueba `/api/estado` antes; si no corre, lo dice), «Anuncio» y
   «Mostrar» en el panel y la app. Probar desde otra terminal con la tele y medir cuánto tardan.
4. **Donaciones de YouTube con prioridad** (**4-nov-2026: el usuario YA activó en Crónicas de Tamriel Super Chat, Super Stickers,
   Super Thanks y Regalos** en Studio > Ingresos > Supers y regalos; aún sin ninguno recibido; en `nucleo/envivo` todavía no hay
   código de donaciones): leer `superChatEvent`/`superStickerEvent`/`newSponsorEvent`/`memberMilestoneChatEvent`/
   `membershipGiftingEvent` de `liveChatMessages.list` (`amountDisplayString`, `userComment`) en `FuenteYouTube`, montos a MXN; un Super Chat con tema del juego cambia el tema en el bloque siguiente (gana el mayor
   monto; cuenta como varios votos con tope); tarjeta especial del color del nivel, el narrador lo lee y agradece; nada
   tóxico ni fuera de reglas, texto sin retocar; si se hace el cambio de voz por chat, quien dona también elige voz;
   «donación simulada» en `/admin`, app y `fab.py envivo cmd donar`; registro en `_sesiones/<fecha>/donaciones.jsonl` y
   total en el panel. Lo que no se pueda probar sin un directo real queda anotado como «falta probar».
5. Pendientes de lo anterior: afinar la búsqueda de YouTube y medir con 480p; ver por qué la tele dejó de abrir la página;
   candado de GPU por `seq` en Chatterbox.

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

## Clips de YouTube en vivo, sin descargar (el usuario, 4-nov-2026, noche)
«¿Se puede no bajar y solo reproducir y pasarlos al stream?» → `nucleo/envivo/yt_vivo.py` (`ClipsYT`):
- Al cambiar de tema (y cada 20 min con el mismo) en segundo plano: haiku traduce el tema a una búsqueda en inglés →
  `yt-dlp "ytsearch8:skyrim <búsqueda> gameplay no commentary" --flat-playlist -j` (solo metadatos, ~2 s) → filtro (≥ 2 min,
  fuera tráiler/reacción/review/top/#shorts) → haiku elige 3 por título → `yt-dlp -g -f "bv*[height<=480][vcodec^=avc1]/18"`
  (enlace directo de googlevideo, solo video, ~4 s cada uno; caduca en ~6 h y va atado a la IP pública de la casa: se renueva
  pasadas 3 h). Cada clip se usa en cuanto llega su enlace y se mete también en los bloques que ya esperan en el búfer.
- Tope de **12 llamadas a yt-dlp por minuto** y caché en memoria por tema; si YouTube frena (429 / «Sign in»), 2 min sin pedir.
- Pantalla: una de cada dos frases lleva `yt` además del clip del disco; `prepararYT` arranca en un punto al azar entre el 10 y
  el 85 % y, si no carga en 4 s o da error, entra el clip del disco sin que se note. `drawImage` de un video de otro dominio
  funciona (no se leen píxeles del canvas principal). La pantalla informa qué clip está al aire (`clip_al_aire`).
- Interruptor «Clips de YouTube en vivo» en `/admin` y «▶ YouTube en vivo» en la app (`/api/ajuste {"yt"}`), con la
  fuente del clip al aire (▶ YouTube título · canal / 💾 disco).
- **Probado en la tele (20:05-20:08):** clips de YouTube del tema («Skyrim | Part 31 | Stomping 2 Giants», «Giants and
  Mammoths!») intercalados con los del disco, sin pantalla negra. **Latencia del cambio al primer clip de YouTube: 76,6 s**
  (búsqueda 61 s por el tope de 6/min de entonces + esperar a la frase par del bloque siguiente). Con el tope a 12 y el clip
  usable en cuanto llega su enlace, la búsqueda bajó a 51 s (sin medir al aire: ver abajo).
- Problemas vistos: (1) con 720p la tele tardó ~28 s en enterarse del cambio de tema (el Chromecast se satura decodificando y
  dibujando en el canvas) → 480p; falta medirlo. (2) haiku eligió mal en una búsqueda («Los dragones y sus gritos» → hombre
  lobo en Riften, Skyrim VR): mejorar la búsqueda (sin traducir, o «<juego> <tema> gameplay» con palabras clave del tema) y
  exigir que el título nombre algo del tema. (3) Tras varios reinicios del servidor la tele dejó de abrir la página (Puente TV
  contestaba; ni cerrar y reabrir con `/api/tele` sirvió): quizá Android no deja abrir la ventana desde segundo plano si la
  tele está en otra app. Las páginas ahora se sirven con `no-store` y la dirección lleva `&v=` (la tele usaba un
  `pantalla.html` viejo en caché).
- **RIESGO:** en un directo REAL de YouTube, el gameplay de otros canales puede activar reclamos de derechos de autor
  (Content ID) y bloquear o cortar el directo. Para las pruebas en la tele no importa; para emitir, mejor clips propios
  del disco o gameplay grabado por nosotros.

## APK «En vivo»: control de las pruebas desde el teléfono, SOLO en la wifi (el usuario, 4-nov-2026, noche)
«No hace falta ngrok: voy a estar en la red local… es un control para manipular el stream en las pruebas.»
- `python nucleo/envivo/android/construir_apk.py` → `nucleo/envivo/android/envivo.apk` (57 KB, fuera de git; misma receta
  y llave que la app de la Fábrica). Se manda por **Rayo**: `"D:/Rayo/pc/publish/Rayo.exe" "<ruta del .apk>"`.
- La app (`MainActivity.java`, paquete `mx.clicknbusiness.envivo`) busca la PC por UDP (`ENVIVO?` → puerto **8792**,
  contesta `ENVIVO1|8790|<canal>`) o usa la última IP que sirvió (o se escribe a mano) y abre `http://PC:8790/movil` en un WebView.
- El servidor escucha SIEMPRE en la red de la casa (`0.0.0.0`). Desde la red solo se ve; **controla quien manda el código**
  de 4 cifras (cabecera `X-Codigo`): fijo en `nucleo/envivo/_cache/codigo_movil.txt`, lo imprime la consola y lo enseña la
  tele abajo a la izquierda los primeros 40 s. La página lo pide en cuanto un control da 403 y lo guarda en el teléfono.
- Botones nuevos: **📺 A la tele / ✕ Quitar de la tele** (`POST /api/tele`). Lanzar el servidor sigue siendo en la PC
  (`python fab.py envivo --tele`); la ruta `/envivo/` de la puerta remota queda como respaldo, pero no hace falta.
- Probado desde la PC por la red (no desde el POCO): UDP contesta; sin código 403; con código, tema y comentario 200.
  **Falta que el usuario la abra en el teléfono**: si no encuentra la PC, el firewall de Windows puede estar bloqueando el
  UDP 8792 (escribir la IP de la PC en la app, 192.168.0.237, y se recuerda).

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

## Directo de YouTube desde la PC: emisión + OBS por código (5-nov-2026)
`python nucleo/envivo/directo_yt.py preparar [canal]` crea la emisión **PRIVADA** del canal por la API (flujo reutilizable,
clave guardada en `_cache/directo_yt.json`, nunca impresa), abre OBS si está cerrado y por obs-websocket arma la escena
«EN VIVO» con la fuente de navegador `http://127.0.0.1:8790/?auto=1` (1920x1080, audio dentro de OBS), silencia el audio
del escritorio y el micrófono globales y pone la clave en el servicio. `salir [--publico]` arranca OBS, espera la señal y
pasa la emisión a «en vivo»; `publico` la hace pública ya al aire (con `containsSyntheticMedia`); `terminar` la cierra y
para OBS; `estado` lo resume. La fuente de OBS ES la pantalla del directo: la tele, solo en espejo (`/?monitor=1`). El chat
y los espectadores: INICIAR con `chat_youtube` = el `video_id` de ese json. Primera emisión: `gBR4XfioDsc` (Tamriel).
