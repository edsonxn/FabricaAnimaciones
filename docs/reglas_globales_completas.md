<!-- Copia íntegra del CLAUDE.md anterior a la poda del 13-oct-2026. CLAUDE.md es ahora la versión corta; aquí está el detalle completo de cada regla. Léelo solo si hace falta. -->

# Fábrica de Animaciones — guía para Claude Code

Pipeline propio (Python, todo local) que produce videos animados 2D procedurales con narración (Chatterbox), música y efectos
sintetizados y sincronizados. El usuario habla español: responde en español. Usa rutas absolutas o `python fab.py ...` desde `C:\FabricaAnimaciones`.

## RETOMAR UN VIDEO EN UNA CONVERSACIÓN NUEVA (hazlo así, ahorra contexto)
1. `python fab.py estado` → tabla de todos los videos (canal, estilo, etapa, qué falta). `python fab.py estado <video>` → su `ESTADO.md`.
   Si el usuario dice «continúa el video X»: `python fab.py continuar X` (videos en tramos, regla de abajo).
2. Lee **solo** `videos/<video>/ESTADO.md` (≤ 60 líneas: estilo, qué está hecho, qué falta, comandos, archivos clave, lecciones) y el doc de estilo que cite.
3. **No leas** `BITACORA.md`, `API.md` ni el núcleo completo: `API.md` solo con grep (`grep -n "def nombre" nucleo/*.py` y lees ese rango).
4. Antes de terminar la sesión (o si el usuario se va): **actualiza `ESTADO.md`** (qué quedó hecho, siguiente paso exacto, comando para retomar). Si cambió el calendario de publicación o un video se subió, una línea en `BITACORA.md`.
5. Video nuevo: `python fab.py nuevo <nombre>` crea el `ESTADO.md` desde la plantilla; protocolo completo en `docs/publicacion.md`.

## REGLA GLOBAL: VIDEOS EN TRAMOS, UNA CONVERSACIÓN POR TRAMO (el usuario, 12-oct-2026; todos los canales y estilos)
Para ahorrar tokens, un video largo o denso se hace en varias conversaciones. Protocolo completo: **`docs/sesiones.md`**.
- **«continúa el video <X>»** (o «sigue con el video X») → `python fab.py continuar <X>`: encuentra el video por carpeta, título
  o alias y dice qué TRAMO sigue y qué leer (solo eso). Haz ese tramo y al terminar CIÉRRALO en la sección «## Sesiones» de su
  `ESTADO.md` (✅ fecha + nota, o ◐ parcial), actualiza «etapa/siguiente» y despídete con la frase exacta para la próxima
  conversación: «continúa el video <alias>». Sin texto, `fab.py continuar` lista los videos con tramos pendientes.
- **Video nuevo:** antes de producir, estima cuántas sesiones conviene según duración y complejidad (tabla de
  `docs/sesiones.md`: Short = 1; Flow = 1-2; dibujado denso ≈ 2-3 min por sesión + 1 de guion/voz + 1 de cierre) y
  **pregunta al usuario cuántas quiere** (AskUserQuestion, tu recomendación primero). Escribe el plan en «## Sesiones» del
  `ESTADO.md` (las plantillas ya la traen) con `alias` y «leer al empezar». En videos dibujados, deja además una guía del kit en
  una página y el plan de tomas (ejemplo: `videos/sociedad_1200/GUIA_ESCENAS.md` y `PLAN_TOMAS.md`).

- **VER EL PRINCIPIO ANTES DE SEGUIR (el usuario, 12-oct-2026):** al proponer el plan de sesiones pregunta también si quiere ver el primer minuto / los 2 primeros / cada tramo renderizado antes de seguir con las demás escenas (anótalo en `- vista previa:` de «## Sesiones»). Render parcial: `python fab.py <v> video --hasta <s>` → `salida/<v>_AVANCE.mp4`, con barritas en el panel; detalle en `docs/sesiones.md` § 2b. Lánzalo SIEMPRE con `fab.py` (si no, el panel no ve el render).

## INICIO DE DÍA: ¿QUÉ CANAL SE QUEDA SIN VIDEO? (8-oct-2026)
Si el usuario pregunta qué toca hoy o qué canal urge: `python fab.py canales --actualizar` (lee YouTube, solo lectura, ~15 s) → tabla ordenada por el primer hueco del ciclo SIN video (último programado o publicado + ciclo del canal), con lo que hay en producción. Sin `--actualizar` usa los datos guardados. **Los Shorts NO cuentan para el hueco (el usuario, 12-oct-2026): solo videos largos.** Responde con el canal más urgente y propón el siguiente video. Lo mismo, interactivo, en la pestaña **«Canales»** del panel (`python fab.py panel --abrir`): filtros, detalle por canal, botón «Actualizar datos» y ciclo editable (`horario.ciclo_dias` de `canales/<alias>.json`; si falta: `separacion_min_horas`/24, y si no, 7).

## REGLA GLOBAL: PANEL DE CANALES AL EMPEZAR Y AL TERMINAR CADA VIDEO (el usuario, 13-oct-2026; todos los canales)
Para saber qué canales se quedan antes sin video, el calendario de la pestaña «Canales» del panel (y `python fab.py canales`)
se actualiza SIEMPRE en dos momentos:
1. **Al empezar un video** (`python fab.py nuevo <v>` o primera sesión de un tema): `python fab.py canales --actualizar`; el
   proyecto sale en «En producción» de su canal (si no, `videos/<v>/panel.json` con `{"canal": "<alias>"}`).
2. **Al terminarlo** (subido en privado/programado, publicado, o descartado): primero se registra en
   `canales/<alias>.json` → `publicados` (`id`, `titulo`, `visibilidad`, `programado`/`publicado`, `formato`) y la BITACORA;
   luego `python fab.py canales --actualizar`, y se le dice al usuario en una línea qué canal queda más cerca de
   quedarse sin video (ATRASADO/URGENTE primero).
Si la API de YouTube da 403 de cuota (la subida de un video gasta ~1 600 unidades de 10 000), `canales --actualizar`
conserva los datos anteriores y el calendario cuenta igualmente lo registrado en `publicados` (`estadisticas.calendario`,
13-oct-2026). La pestaña del panel toma ese cálculo tras reiniciar el panel (lo reinicia el usuario, nunca Claude).

## REGLA GLOBAL: EL SIGUIENTE VIDEO SE DECIDE CON DATOS (el usuario, 8-oct-2026)
Antes de proponer el tema de un video nuevo (cualquier canal): `python fab.py ideas <alias>` (`--actualizar` si el informe tiene más de ~1 semana; solo lectura, ~350 de cuota). Da (1) lo tuyo contra la mediana del propio canal, con % visto, y (2) los videos del nicho que rompieron la media DE SU PROPIO CANAL en los últimos 60 días (× mediana). Propón 3 temas, cada uno con su video de referencia y su ×; prefiere formatos que se repiten en varios canales chicos. Formato ganador = se repite cambiando tema y gancho (con escenas nuevas, nunca recicladas). Los canales son chicos: lo propio son pistas, la señal fuerte es la de fuera. **Y SIEMPRE revisar QUÉ funciona y POR QUÉ (el usuario, 11-oct-2026): `docs/que_funciona.md`** (miniaturas con `nucleo/hoja_miniaturas.py`, gancho del mejor atípico por transcripción, el porqué en 5 ejes: tema, empaque, gancho, estructura y distribución). La conclusión va a **`canales/formula/<alias>.md`** (fórmula vigente, qué evitar, UNA hipótesis por video y registro a 7 días); el siguiente video repite la fórmula y cambia una sola variable. Al subir, `"formato": "<nombre>"` en `publicados` de `canales/<alias>.json` para medir la apuesta. Configuración (`ideas.busquedas`, `competidores`, `filtro`) y detalle: cabecera de `nucleo/ideas.py`; `python fab.py ideas` lista los canales.

## REGLA GLOBAL: CIERRE DE VIDEO = DOCUMENTAR LO APRENDIDO (el usuario, 12-oct-2026; todos los canales y estilos)
Un video NO está cerrado cuando se sube: está cerrado cuando además quedó escrito lo que salió mal y cómo evitarlo. Al terminar CADA video
(subido, miniatura puesta, programado y registrado en `canales/<alias>.json` + BITACORA) y EN LA MISMA SESIÓN:
- Añade a `docs/manual_*.md` o `docs/estilo_*.md` del estilo una sección de **hallazgos** (qué falló, cómo se arregló, tiempos reales) y una lista
  de **mejoras implementables** (código/proceso) para el siguiente video. Ejemplo: `docs/manual_wild_next_door.md` § «Hallazgos de sin_medicina».
- Apunta en el `ESTADO.md` del video las lecciones no obvias y, si hay mejora de código, su siguiente paso. Y una línea de memoria si es una preferencia del usuario.
- Antes de empezar un video nuevo del mismo estilo, LEE esa sección de hallazgos (el manual del estilo la cita en el «Paso a paso»).
- Las fuentes citadas (DOI) se verifican con Crossref antes de publicar; nunca de memoria.

## REGLA GLOBAL: SIN SUBTÍTULOS QUEMADOS (todos los canales, 30-sep-2026)
Ningún video lleva subtítulos dibujados. Texto en pantalla solo para énfasis visual (título, cifra, nombre, etiqueta de mapa). `config.SUBTITULOS = False`; el `.srt` se genera igual (subtítulos opcionales de YouTube). Videos anteriores con subtítulos quemados solo se rehacen si el usuario lo pide.

## REGLAS GLOBALES (el usuario, 12-oct-2026): MÚSICA SIEMPRE LYRIA APEGADA AL GUION; ELEVENLABS = ESCRITURA NORMAL
- **Música:** en todos los canales y estilos es Lyria adaptada al guion (`LYRIA` en guion.py con el arco real de cada escena). Nunca la procedural (`fab.py <v> musica`).
- **Biblioteca primero (el usuario, 21-oct-2026):** toda la Lyria ya generada está catalogada con etiquetas en `nucleo/datos/musica_biblioteca.json`
  (audio en `E:\FabricaAnimaciones\musica_biblioteca\`). Antes de pedir Lyria nueva: `python fab.py biblioteca sugerir <v>` → `usar` → `armar`;
  Lyria nueva solo para lo que la biblioteca no cubra. No repetir música ante el mismo público. Al cerrar un video: `biblioteca catalogar`.
  Detalle: `docs/musica_biblioteca.md`.

## REGLA GLOBAL: CADA API CON UN SOLO USO (el usuario, 21-oct-2026)
- Imágenes SOLO en Flow (navegador integrado o Claude in Chrome). La clave de Google AI Studio es SOLO para Lyria: nunca imágenes por
  API (Nano Banana / gemini-*-image / Imagen), aunque el modelo aparezca en la lista. Origen: en `no_vuelve` se lanzó una imagen de prueba por
  la API (la rechazó el 402); el usuario: «nunca hagas fotos en Google AI, las fotos son en Flow; no se debe usar el saldo en imágenes».
- Sin navegador en la sesión → pedir al usuario que lo active; nunca una alternativa de pago. ElevenLabs: 2 cuentas en la API con saldo.
- Nunca probar una API de pago «a ver si funciona» sin preguntar; nunca abrir `canales/tokens/`. Tabla completa: `docs/apis.md`.
- **Voz ElevenLabs:** escritura normal, SIN reglas fonéticas (esas son solo de Chatterbox): números en cifras («11 de julio», «8 de la noche»), nombres bien escritos («Alice», no «Alis»). Origen: «Once de la noche» se leyó en inglés («uans»; `once` = *once*); con «11» sale bien.

## REGLA GLOBAL: VOZ DE ELEVENLABS = CORCHETES DE ACTUACIÓN (el usuario, 7-oct-2026)
Todo guion que se narre con ElevenLabs (cualquier canal) lleva etiquetas en inglés entre corchetes que le dan ánimo y sentimiento a la voz según lo narrado: `"[sighs] Esa regla murió en enero. [short pause] En Hong Kong."` (`[thoughtful]`, `[serious]`, `[curious]`, `[whispers]`, `[sighs]`, `[short pause]`…). Modelo `eleven_v4` (entiende corchetes y es el más barato de calidad completa, ≈ 0,11 créditos/carácter; `eleven_multilingual_v2` NO las entiende). El núcleo las quita solo para Whisper, timeline y .srt (`config.FRASES_TTS`). Detalle, lista de etiquetas y costos: `docs/voz.md` § «Corchetes». Ejemplo: `videos/videollamada_falsa/guion.py`.

## REGLA GLOBAL: NUNCA VARIOS VIDEOS DEL MISMO CANAL EL MISMO DÍA (el usuario, 7-oct-2026)
Origen: se hicieron públicos 3 videos de Wild Next Door el mismo día y hubo que retirarlos. **No se repite.**
- Un video por canal a la vez, espaciados según `horario.separacion_min_horas` de `canales/<alias>.json` (48 h por defecto). **Ciclos fijados por el usuario (7-oct-2026): Wild Next Door uno cada 3 días (16:00 UTC); LogIA uno cada 4-5 días desde el último publicado; Plastitube semanal, martes 19:00 UTC.**
- Lote de varios videos listos = todos en PRIVADO y programados en huecos sucesivos, enseñando antes el calendario al usuario. «Súbelos/publícalos» sobre un lote no significa «todos hoy».
- Antes de publicar o programar: `python fab.py yt videos <canal>` y BITACORA. El código se detiene si hay choque (`comprobar_separacion`); `--forzar` solo si el usuario pidió expresamente esa excepción. Detalle: `docs/publicacion.md`.

## REGLA GLOBAL: RIGOR CON LA CALIDAD Y EL DETALLE, SIEMPRE (el usuario, 30-sep-2026)
Origen: «La Independencia de México, completa» se subió con mapas que eran manchas verdes, el mismo desierto vacío en casi todas las escenas, figuras mal dibujadas, tomas sin nada y un cuadro negro. **No se repite.**
- Un video NO está terminado porque el render pasó y la voz tiene CER 0: está terminado cuando cada toma se ve a la altura del mejor ejemplo de su estilo. Si el tiempo no alcanza, se dice al usuario; no se entrega a medias.
- **Revisar con la vista, a tamaño completo (Read de la imagen), antes del render largo y otra vez sobre el MASTER:** un cuadro cada ~3 s y uno por fase de cada toma. No basta la hoja de miniaturas.
- **Defectos que bloquean la entrega:** escenario vacío; mismo fondo en escenas distintas; mapa sin geografía real (costa, relieve, ríos, límites, ciudades en su coordenada, con etiqueta) o con «manchas»; figuras mal proporcionadas, sin cara o manos, flotando o montadas unas sobre otras; texto que choca con personajes o se sale del cuadro; cuadros negros o saltos; algo quieto más de ~2 s; personajes demasiado pequeños.
- **Lista de errores ya vividos (Juchipila, 11-oct-2026; se subió con ellos por decisión del usuario): `docs/estilo_kurzgesagt.md` § «ERRORES A NO REPETIR»** — transición de manchas sucia, suelo plano/escena vacía, figuras clonadas, etiquetas diminutas o encimadas, bajo contraste, retratos oscuros/rayados, mapas borrosos, líneas de tiempo sin escala, pergaminos vacíos. Revisar el MASTER con hoja 2×3 (1 cuadro/3 s) ANTES de dar el video por bueno.
- **Densidad mínima por toma** (estilos ilustrados/Kurzgesagt): ≥ 3 planos de profundidad; detalle propio del lugar y la época; animación ambiente continua (nubes, aves, polvo, humo, agua, hierba); la acción narrada la hacen los personajes. Cada escena, su propio mundo visual.
- **«Estilo Kurzgesagt» = replicar al canal Kurzgesagt con MUY BUENA calidad, mucho detalle y buen movimiento** (no «vector plano minimalista»): texturas suaves, sombras de 2 tonos, luces, partículas, personajes expresivos (ojos, cejas, boca, manos, pliegues), anticipación/rebote/seguimiento, caminatas con ciclo creíble, multitudes con ritmo propio, cámara siempre en deriva/zoom/paneo con paralaje. «Muñecos quietos sobre un fondo» no está terminado.
- **Mapas:** geografía REAL de dominio público (Natural Earth, ETOPO) con relieve, ríos, litoral, límites y ciudades verdaderas; ejércitos y rutas animados.
- **FOTOS EN EL MAPA (el usuario, 23-oct-2026; TODOS los canales, todo mapa con lugares o rutas):** mientras se ve el mapa, cada vez
  que la voz nombra un personaje, un lugar o un objeto (los ítems que hay que juntar, la ciudad a la que se llega, el jefe), sale su
  FOTO REAL junto a su marcador (con rebote, sin tapar nombres ni título) y se va al pasar al siguiente: el mapa debe sentirse
  dinámico, no solo una línea que avanza. Imagen real siempre (retrato/pegatina de la wiki, foto de archivo, ícono oficial del
  objeto); si no existe, ese paso va sin foto, nunca inventada. Kits: `mg_mapa.mapa` y `mg_wow.ruta` (5.º elemento del punto)
  — receta en `docs/estilo_secuencia_yt.md` § «MAPAS REALES CON RUTA»; en Kurzgesagt/Cronopapel, retrato o pegatina junto a la
  ciudad/estado que se nombra (`docs/estilo_kurzgesagt.md` §A, `docs/estilo_boceto_guache_mapa.md` § «Ubicación en México»).
- Si el usuario critica la calidad: se arregla también el estilo (kit reutilizable + doc de estilo) y la lección va a `ESTADO.md`/`BITACORA.md`. Entre tardar más y entregar flojo: siempre lo primero.
- **Cuando un video crea o mejora un estilo/kit, actualiza EN LA MISMA SESIÓN `docs/estilo_*.md`, la tabla de estilos de este archivo, `docs/api_kz.md` (`python nucleo/api_kz.py`) y la galería de la pestaña «Estilos» del panel (`nucleo/datos/galeria.json`, se relee sola, sin reiniciar el panel), no solo el `ESTADO.md` del video.**

## ARRANQUE RÁPIDO de un video DIBUJADO POR CÓDIGO (no repitas la exploración; 7-oct-2026)
- **Vertical:** `FORMATO = "vertical"` en guion.py → `motor.W, H = 1080, 1920`. Ritmo de Short: `GAP = 0.16`.
- **Escena que dibuja el cuadro entero:** una clase `Mundo(Escena)` con `render(self, lz, t)` que devuelve float32 HxWx3 en 0..1, `CLASES = {id: Mundo}` y `TRANSICIONES = [("continua", 0.5)] * (n_escenas - 1)` en guion.py (si no, el núcleo mete sus propias transiciones). `ESTILO_VISUAL = "documental"` para motion graphics propios.
- **Voz ElevenLabs:** `VOZ = dict(motor="elevenlabs", voice_id=..., modelo="eleven_v4", referencia="<mp3>", tomas=1, stability=0.5)` + corchetes de actuación en las frases (regla global de arriba). Voces y saldo: `python videos/mods_ia_fusion/_voces.py`; la referencia sale gratis de la muestra pública: `python videos/mods_ia_fusion/_ref_voz.py <voice_id> ref.mp3`. Si `seleccionar` dice REGENERAR: `voz --seeds 5 --solo <key>`.
- **SFX de ElevenLabs fuera del motor secuencia:** copiar `videos/mods_ia_fusion/fx_audio.py` (escribe `audio/fx.wav`, que `mezcla` suma). Empezar con `MEZCLA["fx"] = -17`; revisar que la relación voz/fondo que imprime `mezcla` sea ≥ ~11 dB.
- **Música Lyria:** `LYRIA = dict(estilo=..., escenas={id: (descripción, intensidad)})` en guion.py; desde la carpeta del video, con `$env:PYTHONPATH = "<carpeta del video>;C:\FabricaAnimaciones\nucleo"`: `python ..\..\nucleo\lyria.py --n 1` y luego `--usar 1`.
- **Anclas por palabra sin instancia de escena:** `pix.ww(escena, frase, "palabra")` lee `timeline.json` directamente.
- **Video real:** `python -m yt_dlp -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" -o "videos/<v>/clips/<nombre>.%(ext)s" <url>`; hoja de contacto con ffmpeg (`fps=1/3,scale=320:-1,tile=7x4`) para elegir el tramo.
- Ejemplo completo de todo lo anterior: `videos/mods_ia_fusion/` (estilo «rayos X tecno», `docs/estilo_rayosx_tecno.md`).

## Ahorrar tokens
- `API.md` (catálogos + firmas) solo con grep. Para coreografías nuevas, copia patrones del video de referencia con `grep -n "class X" -A 60`, no el archivo entero.
- Comandos largos (> ~8 KB) fallan en este Windows: escribe archivos con Write/Edit, no heredocs enormes; los parches van a un `.py` y se ejecutan.
- Mira imágenes (hojas de prueba) a 640x360 para explorar y a tamaño completo solo para el rigor final.

## ESTILO POR CANAL (REGLA FIJA, 30-sep-2026): NO cambiar de motor por comodidad; si otro motor sería más rápido, PREGUNTAR
`ESTILO_VISUAL` de `guion.py` debe coincidir con el motor realmente usado. Al empezar: anota estilo y ejemplo en el primer mensaje.
| Canal (alias) | Estilo | Ejemplo a copiar | Doc de estilo |
|---|---|---|---|
| **Bitácora Perdida** (`bitacora_perdida`) | **Kurzgesagt siempre**, muy buena calidad, mucho detalle y movimiento. **Estándar actual: Kurzgesagt ISOMÉTRICO + mapas con relieve real** (dioramas, interiores en corte, **retratos REALES de dominio público en marco dorado** — `nucleo/kz_retrato_real.py`, no bustos dibujados —, rótulos de cápsula). Zacatecas (`vox` vertical) fue excepción | **`videos/independencia_mx/`** (`tNN.py`, `mundos_*.py`; kit `nucleo/kz_*.py`, catálogo `docs/api_kz.md`); antes `tesoro_moctezuma/`, `teotihuacan/` | `docs/estilo_kurzgesagt.md` §A (leer entera antes de empezar) |
| **Cronopapel** (`cronopapel`) | Boceto + guache con mapa pintado y pegatinas, cambios de escena procedurales. **Short vertical sin mapa: `videos/primer_foton/` (pegatinas sobre fondos guache, mascota Foti)**. **Estándar actual (v2): relieve real ETOPO1 bajo el guache, ríos, capas de reinos, fronteras reales; MUCHOS elementos (el usuario devolvió Egipto v1 «muy pobre en elementos»): un dibujo nuevo por frase, nada de mapa solo > 1,5 s** | **`videos/historia_egipto/`** (v2.1: una rejilla, valle verde, ~150 dibujos) y **`videos/historia_espana/`** (dos rejillas); antes `historia_china/`, `historia_iran/`, `historia_japon/` | `docs/estilo_boceto_guache_mapa.md` (§ Versión 2 y 2.1) |
| **Sapiens con Wifi** (`sapiens_con_wifi`) | Doodle (`doodle`, `doodle_psicodelico`, `recortes`), listas por ítems | `videos/neandertales/`, `un_dia_30mil/`, `40mil_anos/` | `docs/flujo_produccion.md` (estilos visuales) |
| **Kuriox** (`kuriox`) | Kurzgesagt con la mascota **Kuri** (nunca el pájaro morado); Shorts verticales; más dinámico (pausas cortas, mucho movimiento) | `videos/sol_apagado_8min/`, `historia_60/` | `docs/estilo_kurzgesagt.md` |
| **Edsonxn** (`edsonxn`) | **Documental de misterio / crimen real** (calco de «Detrás del Enigma»), voz **Faraon**, sin subtítulos; noticias de actualidad con extractos de video (yt-dlp) + fotos Commons + mapa de relieve real | `videos/voynich/`, `videos/polybius/`, `videos/christa_pike/` (kit `kit_cp.py`), **`videos/satoshi_nakamoto/` = TABLERO DE DETECTIVE VIVO** (kit `tablero.py` + portales); **`videos/polybius/`** = el mismo tablero ya desligado del tema Bitcoin (piezas genéricas, `portal_base.py`, kit `arcade.py`): copiar de aquí | `docs/estilo_documental.md` (§ «Documental de NOTICIA / crimen real», § «Motion graphics DIBUJADOS propios» y § «Tablero de detective VIVO») |
| **LogIA** (`logia`) | **Noir**: cine negro en tinta y aguada, SOLO B/N, claroscuro, lluvia, persianas; dibujo cuadro a cuadro + video real de Pexels entintado (`clip_noir`); detective narrador; voz ElevenLabs con corchetes de actuación (`eleven_v4`), opción de más voces para personajes (`VOZ_POR_FRASE`) y SFX de ElevenLabs para el drama. **REGLA (el usuario, 8-oct-2026): MEDIOS REALES** — cada persona pública que el guion nombre sale con su FOTO REAL (`python nucleo/imagenes_web.py persona "<Nombre>" 3 --dir imagenes --descargar` → ficha `nucleo/noir_real.retrato_noir`) y el video real (Pexels/Pixabay y **yt-dlp** `videos_stock.py ytbuscar/ytbajar`) entra donde ayude, SIEMPRE en B/N de tinta (`clip_real`/`clip_noir`), con créditos (`imagenes_web.py creditos`); solo figuras públicas con hechos documentados (particulares e hipótesis = dibujados), clips de YouTube ≤ 8 s con crédito en pantalla y aviso de derechos al usuario | **`videos/informante_2027/`** (10 min, 20 escenas; kit `kit27.py` + `mundos27.py` + `comite.py`) y `videos/ia_noir/` (kit `nucleo/noir*.py`, `sfx_noir.py`, `tts_eleven.py`) | `docs/estilo_noir.md` |
| **Plastitube** (alias `pieza_oculta`; antes «La Pieza Oculta») | **Secuencia Flow**: plastilina/claymation hecha con clips e imágenes de Google Flow (1–2 min de video al inicio, luego imagen por beat); motor `secuencia`, NO se dibuja por código; inventos y sus inventores; voz Dan | mismo sistema que Wild Next Door: copiar `videos/bichos_invierno/` (clips de Flow al inicio + imágenes) o `videos/aranas_otono/` (todo imagen); primer video propio (prueba, todo imagen): `videos/teflon_sarten/` en la Fábrica (antes: proyecto `Documents\Platitube`, jubilado) | `docs/estilo_secuencia_flow.md` (preguntar duración, minutos de video y clip antes de empezar); efectos y SFX opcionales: `docs/estilo_secuencia_fx.md` § «Ideas para Plastitube y Wild Next Door» |
| **Wild Next Door** (`wild_next_door`) | **EN INGLÉS.** Secuencia Flow en **dibujo animado** (tinta + color plano, fondo claro; no plastilina), voz Chatterbox **EnglishComic**, música Lyria; bichos de casa con giro «no lo mates». **Formato ganador: «Never Kill a X»** (ciempiés: 440 vistas en 2,5 días vs 2-3 de los demás) | **`videos/arana_techo/`** (guion plantilla con `clips_s`), `ciempies_casa/` (prompts), `bichos_invierno/` (clips) | **`docs/manual_wild_next_door.md` (LEER PRIMERO: paso a paso, qué funciona y errores)** |
**Reels de la página de Facebook «Que pasa en Juchipila» (8-oct-2026):** no son de ningún canal de YouTube y el camino ya está decidido: secuencia con efectos en VERTICAL (`FORMATO = "vertical"` en guion.py, `docs/estilo_secuencia_flow.md` § «Formato vertical»). Videos `jch_<tema>`; receta completa y publicación en `E:\PaginaFace\CLAUDE.md` § «hazme un reel». No se suben a YouTube.

**VIDEO SIN CANAL (regla del usuario, 7-oct-2026): si pide un video y no es para ningún canal, PREGUNTAR antes de empezar** (AskUserQuestion) cuál de los dos caminos quiere, salvo que ya lo haya dicho en el pedido:
1. **Secuencia con efectos** (tipo Flow): imágenes/clips de Google Flow, una por frase, con cámara dirigida, golpes, rótulos de énfasis y SFX/camas de ElevenLabs anclados a las palabras. Motor `secuencia` + `efectos.py` (`nucleo/secuencia_fx.py`). Doc: **`docs/estilo_secuencia_fx.md`**. Ejemplos: `docs/ejemplos/un_segundo/` (el corto que originó el estilo) y **`videos/guason_fumado/`** (audio externo + estilo «animación fumada / sin presupuesto»). También acepta un audio ya grabado (`AUDIO_EXTERNO` en guion.py).
2. **Animación tradicional** dibujada por código, como la de los otros canales (elegir entonces el estilo de la tabla).

Otros estilos de prueba: **noir a color** = la esencia del noir con un poco de color oscuro y apagado (sombras frías, sodio ámbar, UN acento; paletas sodio/bourbon/medianoche; kit `nucleo/noir_color.py`, prueba `videos/prueba_noir_color/`) y su **variante feudal** = pesquisidor encapuchado con farol que investiga casos y sucesos antiguos (castillos, antorchas, pergamino y lacre; para sagas medievales tipo GoT/HotD e historia antigua; kit `nucleo/noir_feudal.py` + reparto de corte `nucleo/noir_corte.py`, prueba `videos/prueba_noir_feudal/`, **primer video completo `videos/got_joffrey/`** = «¿Quién envenenó al rey?», 3:12; **tech-noir con «copias» de cabeza de monitor: `videos/sociedad_1200/`**, 15:47, 28 escenas, kit `reparto.py`/`props_s.py`/`mundos_1..6.py`), doc de ambos `docs/estilo_noir_color.md` (11-oct-2026); **rayos X tecno** = explicador de tecnología vertical, neón sobre oscuro, video real dentro de ventanas de programa y diagramas animados alrededor (`videos/mods_ia_fusion/`, kit `pix.py` + `comp.py`, `docs/estilo_rayosx_tecno.md`), boceto en bucle (`docs/estilo_boceto_gota.md`), guache/meme (`docs/estilo_guache_meme.md`), **cartoon90** = dibujo animado de los 90 tipo «Coraje el perro cobarde», tinta que se redibuja cada cuadro (`videos/gato_cobarde/`, kit `nucleo/toon*.py`, `docs/estilo_cartoon90.md`; lo entrega con la vista previa del panel lista y SIN renderizar: el usuario renderiza escena por escena).

## Índice de docs (léelos solo cuando haga falta)
- `docs/flujo_produccion.md` — estructura del núcleo, etapas del flujo, cómo se escribe una escena a medida, estilos visuales, velocidad de render, QA, modelos, disco, entorno.
- `docs/voz.md` — problemas de voz ya vividos (leer ANTES de `voz`; guion final primero, GPU compartida, nombres raros).
- `docs/publicacion.md` — protocolo de video nuevo (canal → métricas → preguntas → producir), horario, miniaturas con IA, subida a YouTube.
- `docs/estudio.md` — **Estudio** (versión comercial, `python fab.py estudio --abrir`, puerto 8790): videos de 60 s horizontal/vertical, voz clonada, estilos personales, guion con Gemini barato. Código en `estudio/` (no toca `nucleo/`).
- `docs/panel.md` — panel de avance y vista previa. `docs/estilo_*.md` — recetas por estilo.
- `BITACORA.md` — calendario de publicaciones y estado por canal (corto). Historial largo: `docs/historial.md`.

## Comandos esenciales
```
python fab.py estado [video]            estado de todos / de uno
python fab.py continuar [texto]         «continúa el video X»: qué tramo sigue (docs/sesiones.md)
python fab.py <v> voz | seleccionar | tiempo | comprobar | musica | sfx | mezcla | video | final | verificar | todo
python fab.py <v> escena <id> t1 t2 ... hoja de prueba de una escena (previews/esc_<id>.jpg; MÍRALA)
python fab.py <v> video --rehacer 270-280 [..]  re-renderiza solo esos tramos (s); luego `final`
python fab.py nuevo <v> --secuencia     video del motor SECUENCIA (Google Flow); luego beats | prompts | ingesta | medios | video
python fab.py <v> fx [--seco | hoja]    motor SECUENCIA con efectos.py: SFX de ElevenLabs -> audio/fx.wav (lo suma `mezcla`); --seco lista tiempos; hoja = previews/fx_NN.jpg
python fab.py <v> limpiar               borra segmentos/ cuando el video está aprobado
python fab.py yt canales | metricas <alias> 90 | subir <v> <canal> private | aplicar <v> <canal> <id> | publicar ...
python fab.py canales [--actualizar]      inicio de día: qué canal se queda antes sin video (misma vista en la pestaña «Canales» del panel)
python fab.py ideas [<canal>] [--actualizar]  siguiente video con datos: lo tuyo vs. lo que rompió la media en el nicho (canales/metricas/ideas/<canal>.md)
python fab.py estadisticas [--actualizar] panel general de estadísticas de TODOS los canales (HTML sin servidor: canales/metricas/panel_canales.html;
                                        `--actualizar` pide datos frescos a YouTube, solo lectura; código nucleo/estadisticas.py + .html;
                                        canal nuevo = agregarlo AL FINAL de ORDEN para no repintar los colores)
python fab.py panel --abrir             panel de avance (NUNCA detenerlo ni matarlo con los python)
                                        Bitácora de uso del panel (clics, filtros, scroll) + skill `analizar-uso-panel` («analiza mi uso del panel» → propuesta de interfaz nueva): docs/panel.md
                                        Vista previa → «Renderizar esta escena»: queda fluida en el panel y el render completo la REUTILIZA
                                        (segmentos/ + firma del código; ver docs/panel.md «Escena fluida»). Tras editar código, ámbar = obsoleta.
                                        El render completo también deja las escenas en verde (anota sus segmentos; el motor arma el mp4 al abrir).
                                        ANTES de `video --rehacer` tras editar código: «conservar» en el panel (si no, `depurar` borra todo lo guardado)
```

## Disco, git y entorno (resumen; detalle en docs/flujo_produccion.md)
- **Lo pesado vive en E:\FabricaAnimaciones** (junctions, 5-oct-2026, a pedido del usuario): `videos/*/{salida*,segmentos,audio,voz,previews,clips}` y los proyectos/vistas del Estudio (`E:\FabricaAnimaciones\estudio`). `fab.py nuevo` ya crea esas carpetas en E:. **E: (HDD USB) debe estar conectado** para producir, renderizar o subir. Herramienta: `python nucleo/mover_pesados.py` (ver docs/flujo_produccion.md «Disco»).
- C: suele estar casi lleno: antes de renderizar mira el espacio libre (un video de 3 min ≈ 1,5 GB temporales; con < 2 GB libres avisa). `final` CONSERVA `segmentos/` para arreglos por tramos (`python fab.py <v> video --rehacer 270-280` + `final`, minutos en vez de re-render completo); al aprobar/subir el video: `python fab.py <v> limpiar`.
- Render rápido (2026-10-04, ver docs/flujo_produccion.md «Optimización»): el límite es la memoria virtual de Windows, no el CPU. Antes de un render largo pide al usuario cerrar `chatterbox_server.py` y `app.py` (~8 GB cada uno) y usa 12 procesos (por defecto); el render ya no deja dormir la PC, dice qué cerrar si no caben y **sube solo de procesos cuando se libera memoria** (y si a uno le falta memoria, reintenta su segmento en vez de caerse).
- Git: repo privado `origin`; versionar solo código/config (ver `.gitignore`); NUNCA `canales/youtube_client_secrets.json`, `canales/tokens/`, métricas, voz/audio/render. `git status` antes de cada commit; commit en español; `git push`. Hay muchos cambios sin confirmar (ver BITACORA §6).
- Python 3.10 del sistema (torch cu124, numpy, opencv, numba, faster-whisper…); Chatterbox en `C:\chatterbox\repo`; voces en `C:\chatterbox_voices` (Dan = narrador por defecto); ffmpeg `C:\ffmpeg\bin`; GPU RTX 4060 8 GB. No borrar `~/.cache/huggingface/hub` (Chatterbox y Whisper, ~6 GB).
- Entrega: `videos/<v>/salida/*_MASTER.mp4` (1080p) + `.srt`. Nada de versiones para WhatsApp salvo que lo pida. **Render terminado = subir privado y PROGRAMAR en el hueco del canal sin preguntar, cualquier canal (el usuario, 20-oct-2026; `docs/publicacion.md` § «render terminado»).** Hacer público YA o `--forzar` = preguntar antes.
- Con voz (Chatterbox) y render a la vez se agota la memoria virtual: no los corras juntos; render con `--procs 12` (el render baja solo los procesos si no hay memoria).
