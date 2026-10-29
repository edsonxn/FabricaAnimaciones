# Videos en TRAMOS: varias conversaciones (sesiones) por video

_Regla del usuario (12-oct-2026), para TODOS los canales y estilos. Origen: «Las 1.200» (videos/sociedad_1200, 15:47 en noir a
color) se volvió una conversación enorme. Cada mensaje vuelve a cargar todo el contexto, así que una conversación larga cuesta
mucho más que varias cortas. Con el traspaso documentado, una conversación nueva arranca leyendo solo el `ESTADO.md` y su guía._

## 1. La frase del usuario: «continúa el video …»
Cuando el usuario diga «continúa el video de las 1200», «sigue con el video X», «continúa X» (o equivalente):
1. `python fab.py continuar <lo que dijo>` → encuentra el video por carpeta, título o `alias` y dice **qué tramo sigue**,
   qué leer y cómo cerrar. Sin texto, lista los videos con tramos pendientes. Si encajan varios, pregunta cuál.
2. Lee SOLO lo que indica (el `ESTADO.md` del video + su «leer al empezar»). El núcleo y los kits, solo con grep.
3. Haz **ese tramo** completo, con el rigor de siempre (revisar con la vista). Si el usuario pide «haz dos tramos», haz dos.
4. Al terminar (o si la conversación se alarga demasiado, con muchas imágenes o errores): **cierra el tramo** (punto 3).

## 2. Video NUEVO: proponer el plan de sesiones ANTES de producir
Después del protocolo de video nuevo (canal → métricas/ideas → tema, estilo y duración; `docs/publicacion.md`), estima las
sesiones y **pregúntale al usuario cuántas quiere** (AskUserQuestion, tu recomendación primero y una línea de por qué: cuántos
minutos y escenas lleva cada tramo). Luego escribe el plan en la sección «## Sesiones» de su `ESTADO.md`.

### Cómo estimarlo
`sesiones ≈ 1 (guion + voz + tiempo) + ⌈minutos dibujados ÷ ritmo⌉ + 1 (cierre)`, con estos ritmos por sesión:

| Tipo de video | Minutos por sesión de escenas | Notas |
|---|---|---|
| Short / ≤ 60-90 s (cualquier estilo) | — | **1 sesión** para todo |
| Secuencia Flow (Wild Next Door, Plastitube, reels) | — | **1-2 sesiones**: (1) guion, voz, prompts y generación en Flow; (2) ingesta, medios, efectos, render y subida |
| Dibujado DENSO (noir / noir_color con tomas cada 3-5 s, Kurzgesagt isométrico, mapas con relieve) | ~2-3 min (4-6 escenas) | el primer tramo de escenas incluye el kit del video (personaje, utilería, lugares) |
| Dibujado NORMAL (boceto/guache, doodle, cartoon90, documental con motion graphics) | ~3-4 min | |
| Documental de fotos y clips reales con poco dibujo | ~4-5 min | |
| Estilo NUEVO (primer video del estilo) | +1 sesión | para el kit y la prueba de estilo |

Videos de ≤ 3 min y estilo normal: juntar en 2 sesiones (guion+voz+escenas · cierre). Si la voz ya existe (rehacer escenas),
quita la primera. El cierre (sonido → mezcla → render → final → verificar → hoja del MASTER → miniatura → youtube.json → subida
en privado) va siempre en su propia sesión: el render corre solo y deja margen para corregir con `video --rehacer`.
Ejemplo real: «Las 1.200», 15:47 en noir_color denso, voz hecha → 6 tramos de escenas + 1 de cierre = 7.

## 2b. VER EL PRINCIPIO ANTES DE SEGUIR: render PARCIAL (regla del usuario, 12-oct-2026; videos dibujados por código)
Origen: en «Las 1.200» (15:47 en 7 tramos) el usuario quiso ver lo ya hecho (los primeros 9 min) antes de decidir si se hacían las
demás escenas. **Al proponer el plan de sesiones (punto 2) pregunta TAMBIÉN, en el mismo AskUserQuestion:** «¿Quieres ver el principio
del video antes de hacer el resto? ¿Después del primer minuto, de los 2 primeros, de cada tramo, o solo al final?». Anota la
respuesta en la sección «## Sesiones» del `ESTADO.md` (línea `- vista previa: ...`) y, en cada punto acordado, **cierra el tramo con
el render parcial ya lanzado** y espera a que el usuario lo vea y diga si se continúa. Si no se acordó, ofrécelo igual al cerrar un tramo.
- **SIEMPRE CON AUDIO COMPLETO (regla del usuario, 13-oct-2026, al ver el avance mudo de `sonic_exe`):** «los preview con audio, sonido,
  música, todo, porque es parte importante». Antes de lanzar el parcial deja hecho `voz`, `sfx`/`fx_audio`, `musica` (Lyria) y `mezcla`
  (`audio/final.wav`); el parcial lo recorta y lo une. Si el plan era ver el primer minuto en el tramo de escenas, el audio de ESE
  minuto (SFX + Lyria de la primera escena) va antes: ordena el tramo como escenas → sonido de lo que se verá → mezcla → parcial.
- Comando: `python fab.py <video> video --hasta <segundos> [--procs 12]` (`nucleo/render_parcial.py`). Redondea hacia abajo a
  múltiplos de 3 s. Deja `salida/<video>_AVANCE.mp4` (video + `audio/final.wav` recortado) y NO toca el MASTER. Es un render
  normal para el panel: **barritas por segmento y escena, ETA, «Ver fluida»** (el panel limita el avance a ese tramo con
  `segmentos/parcial.json`). Hay que lanzarlo con `fab.py` (no con scripts propios): el panel detecta el render por esa línea de comando.
- Los segmentos son los mismos del render completo: al terminar el video, `fab.py <v> video` reutiliza lo ya dibujado (borra `parcial.json`).
- Escenas aún sin hacer: el registro (`escenas.py`) debe dar a cada id una clase; las pendientes usan una clase de RELLENO negra
  (ver `videos/sociedad_1200/_reg.py`) para que el motor arranque. El último tramo parcial acaba con una transición a negro.
- Si había un `*_MASTER.mp4` viejo en `salida/`, el panel marca el video «listo» y no muestra el avance: apártalo (renómbralo
  a `*_viejo.mp4`) antes de renderizar de nuevo.
- Antes: pedir cerrar `chatterbox_server.py` y `app.py` (el render sube de procesos solo al liberarse memoria). Un video de 9 min
  noir denso tarda ~1,5 h con 8-12 procesos.

## 3. Cerrar un tramo (SIEMPRE, antes de despedirte)
- En la tabla de «## Sesiones»: la fila hecha → `✅ <fecha>` + nota corta (qué quedó, archivos nuevos). Si quedó a medias →
  `◐ parcial: hechas X, falta Y`. La siguiente → `⏳ siguiente`.
- Actualiza `- etapa:` y `- siguiente:` de la cabecera, las «Lecciones» no obvias y, si cambió el kit, su guía.
- Si diseñaste tomas o decisiones que sirven a tramos futuros, déjalas escritas (p. ej. `PLAN_TOMAS.md`): la próxima
  conversación no debe volver a diseñarlas.
- Si se acordó (o conviene) ver el avance: lanza el render parcial (§2b) antes de despedirte.
- Termina diciendo al usuario la frase exacta para la próxima conversación: **«continúa el video <alias>»**.
- Commits solo si el usuario lo pide (y nunca tokens, métricas ni audio/render).
- Si el tramo **empieza o termina el video** (creado, subido/programado o descartado): `python fab.py canales --actualizar` y una línea al usuario con el canal que se queda antes sin video (regla del 13-oct-2026, `docs/reglas_globales_completas.md` § «PANEL DE CANALES»).

## 4. Formato de la sección en ESTADO.md (la lee `fab.py continuar`)
```
## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: <frases con las que el usuario lo nombra, separadas por comas>
- leer al empezar: <archivos además del ESTADO.md: la guía del kit, el plan de tomas…>
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion, voz, tiempo + kit + escenas 1-4 | ✅ 12-oct | ... |
| 2 | escenas 5-9 | ⏳ siguiente | ... |
| 3 | cierre: sfx → mezcla → render → final → verificar → miniatura → youtube.json | pendiente | ... |
```
El número va al principio de cada fila; «✅» (o «hecho»/«listo») marca lo terminado; la primera fila sin ✅ es la que sigue.
Las plantillas `videos/_plantilla*/ESTADO.md` ya traen la sección.

## 5. Archivos de traspaso recomendados (videos dibujados por código)
- `ESTADO.md` (≤ 60 líneas) con la sección de sesiones: SIEMPRE.
- `GUIA_<algo>.md` o `GUIA_ESCENAS.md`: el kit del video en una página (firmas, convenciones, colores, reglas de ritmo) para no
  leer los kits enteros. Ejemplo: `videos/sociedad_1200/GUIA_ESCENAS.md`.
- `PLAN_TOMAS.md`: las tomas de cada escena ancladas a palabras del guion. Ejemplo: `videos/sociedad_1200/PLAN_TOMAS.md`.
- Una escena terminada y revisada como ejemplo a copiar (citada en la guía).
- `## En curso` en el `ESTADO.md` mientras haya un tramo abierto (§6): lo último que hiciste y lo que sigue, para el relevo de cuenta.

## 6. Corte por tokens y CAMBIO DE CUENTA (regla del usuario, 13-oct-2026; todos los canales y estilos)
Origen: en `dos_lunas` la sesión se quedó sin tokens a mitad del tramo 3 con cuatro módulos escritos y el `ESTADO.md` aún diciendo
«esperando visto bueno». El usuario tiene 3 cuentas Pro: cuando una se agota, abre OTRA cuenta y escribe «continúa el video X».
Esa conversación nueva **no sabe nada** de la anterior: solo existe lo que está en disco. Por eso:

**Mientras trabajas (para que un corte no pierda nada)**
- **El disco es la memoria.** No dejes decisiones, tiempos ni «lo que falta» solo en la conversación.
- **Checkpoint en `ESTADO.md` ANTES de cada pieza pesada y DESPUÉS de cada hito**, no al final del tramo: al terminar cada toma/escena
  probada, tras cada comando largo (voz, render, subida) y cada vez que el usuario decida algo. Una línea basta, en la sección
  `## En curso` (bórrala al cerrar el tramo): *qué estás haciendo · archivos que tocas · qué falta · comando lanzado y hora*.
- Antes de lanzar un render/voz largo, anota en `## En curso` el comando exacto y la hora: ese proceso sigue vivo aunque la sesión
  muera (lo lanzó `fab.py`), y la sesión siguiente debe mirar el panel / `tasklist` antes de relanzarlo.
- Pon la fila del tramo en `◐ parcial` en cuanto exista algo (qué hay, qué falta, qué se probó) y deja el plan de tomas / la guía al día.
- Vigila el margen: `get_usage` con la ventana de 5 h > 80 % (o semanal > 90 %) → **para de empezar piezas nuevas**, cierra el tramo
  (§3) y avisa al usuario de que puede seguir en otra cuenta. Anota el uso de la cuenta (`buenosdias --uso`, docs/buenos_dias.md §3).

**Al retomar tras un corte (o en otra cuenta)**
1. `python fab.py continuar <video>` ahora avisa **«⚠ TRABAJO SIN REGISTRAR»**: lista los archivos del video más nuevos que su
   `ESTADO.md`. Si aparece, la sesión anterior se cortó sin anotar.
2. **Concilia antes de producir:** `python -m py_compile` de los `.py` nuevos; abre las hojas de `previews/` más recientes (muestran qué
   se probó de verdad); grep de lo que registran `escenas.py`/`guion.py` (p. ej. `registrar_sfx`, anclas, `CLASES`); revisa `salida/`.
3. Anota en el `ESTADO.md` lo que **ya existe** (qué está escrito, qué probado, qué falta) y recién entonces continúa con lo que falte.
   No rehagas lo hecho y no confíes en `- etapa:`/`- siguiente:` si hay trabajo sin registrar: pueden estar viejos.
4. Nunca dos cuentas sobre el mismo video a la vez (comparten carpeta, GPU y RAM; `chatterbox_server.py` y los renders no se mezclan).

## 7. Corte AUTOMÁTICO por contexto: checkpoint + hilo nuevo a los 180 mil tokens (el usuario, 29-oct-2026; todo el proyecto)
Por qué: cada paso de Claude vuelve a leer TODO el hilo, así que un hilo largo cobra su tamaño en cada llamada. Simulación sobre
228 sesiones reales (21 días): la sesión típica llegaba a ~383 mil tokens (p90 714 mil) y cada hilo arranca ya con ~83 mil
(CLAUDE.md + MEMORY.md + herramientas). Reiniciar a 150-200 mil ahorra **~40 %** del gasto; al 30 % (300 mil) solo ~34 %; por debajo
de ~100 mil sale MÁS caro (se paga el arranque una y otra vez). Script: `nucleo/hook_contexto.py`.
- **Cómo funciona:** hook `PostToolUse` en `.claude/settings.json` → `nucleo/hook_contexto.py` lee del transcrito el uso de la última
  llamada del hilo principal. Al pasar 180 mil le inyecta a Claude la orden: terminar SOLO el paso en curso (lo ya lanzado sigue),
  checkpoint (§6: `## En curso` + fila `◐ parcial`), abrir sesión nueva con `start_session` (`user_asked`, `fresh`, sin worktree, brief
  «continúa el video <v>» + lo que falta) y cerrar el turno. Si la app no deja abrirla: tarjeta propuesta o «abre un chat nuevo y
  escribe: continúa el video <v>». Repite el aviso cada +40 mil si el hilo sigue; se rearma tras compactar; no salta en subagentes.
- **Cambio del 29-oct-2026 (el usuario: «cámbialo»), por qué:** en la práctica los hilos arrancaban ya con ~100-108 mil, así
  que a los 180 mil totales cada sesión trabajaba solo 70-80 mil y pedía otra a cada rato; además la sesión cortada y la que la
  lanzó abrían cada una su continuación (CFO vs KC: dos idénticas con 8 s de diferencia; la Crematoria: tres a la vez).
  1. **Cuenta solo el TRABAJO:** el umbral va por encima de la base de la sesión (el contexto de su primera llamada, medido una
     vez y guardado en la marca), así que corta hacia los ~280 mil totales.
  2. **Candado por video:** antes de abrir, `python nucleo/hook_contexto.py candado <v>` → «OK» (abre y queda apuntado en
     `videos/<v>/.continuacion.json`) o «YA» (otra sesión la abrió hace < 30 min: no abrir otra).
  3. **Si la app no deja abrir el hilo nuevo** (el turno lo despertó un aviso, un agente en segundo plano u otra sesión; la app
     solo abre sesiones desde un turno que empezó una persona): el hilo SIGUE TRABAJANDO donde está, sin preguntarle al usuario
     («no esperes mi mensaje, termínalo todo», 29-oct), y reintenta el relevo en el siguiente turno del usuario.
  4. **Quien recibe la nota de una sesión cortada NO abre su continuación:** la abre ella misma (y, si la app se lo impide, sigue
     trabajando ella, punto 3). La sesión principal solo avisa al usuario y detiene duplicados si los ve.
- **Ajustes:** variable de entorno `FAB_CORTE_CONTEXTO` (tokens de trabajo; `0` = apagado). Medir un hilo: `python nucleo/hook_contexto.py --medir <transcrito.jsonl>`.
- **La otra palanca:** los ~83 mil del arranque se pagan en cada llamada de cada sesión; recortar `CLAUDE.md`/`MEMORY.md` y los
  conectores que la Fábrica no usa ahorra en todo.
