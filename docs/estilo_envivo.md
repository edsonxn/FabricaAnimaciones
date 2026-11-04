# EN VIVO: directo generado y editado en tiempo real (idea del usuario, 4-nov-2026)

Formato nuevo para Crónicas de Tamriel (y luego Warcraft/Runa): un directo que no se acaba. El usuario da un tema y la
fábrica genera video en tiempo real (clips del canal, pegatinas reales, avisos y fichas del kit del canal, narrador) con un
búfer por delante; desde una ventanita se cambia el tema y el video gira hacia él. Meta: en un directo de YouTube el público
vota el tema de los minutos siguientes. **Regla del usuario: debe parecer lo más posible un video del propio canal** (letra,
avisos, fichas y pegatinas del kit de Tamriel, no un estilo genérico). Voz por ahora: **voz de Windows** (OneCore Raúl
es-MX), nada de ElevenLabs para no gastar créditos.

```
python fab.py envivo [canal] [--tema "…"] [--modelo sonnet|haiku] [--voz Raul] [--cada-min 3] [--chat-youtube <id>] [--abrir]
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

## En curso / pendiente
1. Probarlo con el usuario: `python fab.py envivo --abrir` (pantalla OBS `:8790/?auto=1` + panel `:8790/admin`).
2. Directo de YouTube real: la lectura del chat ya está escrita (`--chat-youtube <id>`) pero sin probar contra un directo.
3. Los subtemas en paralelo a veces se pisan (dos bloques sobre Numinex): el prompt ya pide personajes que no salgan en el
   bloque; vigilar.
4. Voz: OneCore Raúl por ahora; si el directo funciona, valorar una voz del canal.
