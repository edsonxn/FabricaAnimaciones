# Voz: problemas ya vividos y cómo evitarlos

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## REGLA: voz de ElevenLabs = CORCHETES de actuación (el usuario, 7-oct-2026; vale para TODOS los canales)
Siempre que un video use ElevenLabs, el guion lleva **etiquetas entre corchetes** que le dan ánimo y sentimiento a la voz según lo que
se narra. Ejemplo que mandó el usuario: `[thoughtful] Anselmo llevaba quince años abriendo la puerta… [short pause] Nadie sabía su
apellido. [sighs] Para los vecinos…`. Primer video hecho así: `videos/videollamada_falsa/` (LogIA).
- **Cómo:** en `guion.py`, `VOZ = dict(motor="elevenlabs", voice_id=…, modelo="eleven_v4", idioma="es", referencia=…, tomas=1, stability=0.5)`
  y las etiquetas dentro de las frases: `"[sighs] Esa regla murió una tarde de enero. [short pause] En Hong Kong."`.
- **Etiquetas en inglés**, al inicio de la frase (tono) o en medio (pausa/gesto). Probadas: `[thoughtful]`, `[serious]`, `[curious]`,
  `[nervous]`, `[sighs]`, `[whispers]`, `[short pause]`; otras de ElevenLabs: `[long pause]`, `[excited]`, `[sad]`, `[angry]`,
  `[sarcastic]`, `[laughs]`, `[chuckles]`, `[exhales]`, `[shouts]`. Una o dos por frase y no en todas: que acompañen al guion
  (suspiro antes de la mala noticia, susurro en el remate, pausa antes del dato), no que lo adornen.
- **El núcleo las separa solo:** `config.py` guarda la frase con corchetes en `config.FRASES_TTS[clave]` y deja `ESCENAS` limpia, así
  Whisper (CER), `timeline.json`, el `.srt`, las anclas por palabra y el panel nunca ven las etiquetas. Cambiar una etiqueta regenera
  esa frase (`voz/textos.json` guarda el texto con corchetes). Con etiquetas, `tts_select` tolera silencios internos de hasta 2,5 s.
- **Modelos y costo real** (medido el 7-oct-2026 con la misma frase de 118 caracteres; `videos/videollamada_falsa/_modelos.py` lista
  los de la cuenta y `_prueba_voz.py <modelo>` compara): `eleven_v4` 13 créditos (≈ 0,11/carácter) · `eleven_v4_turbo` 6 ·
  `eleven_v3_conversational` 24 · `eleven_v3` 47 (≈ 0,40, igual que multilingual v2). **Por defecto `eleven_v4`**: un video de
  6:30 (53 frases) costó ~600 créditos. `eleven_multilingual_v2` y los flash/turbo v2 NO entienden corchetes (no los uses con etiquetas).
- Los modelos v3/v4 solo aceptan `stability` 0.0 (creativa) / 0.5 (natural) / 1.0 (robusta) y no reciben `previous_text/next_text`
  (`nucleo/tts_eleven.py` ya lo resuelve). Frases muy cortas («Caso abierto.») salen más inestables: revisar su transcripción.
- Una voz inglesa leyendo español (p. ej. «David») puede sesear raro una palabra (Whisper oyó «Quinze»): otra semilla
  (`tts_gen.py --seeds 3 --solo <clave>`; con `tomas=1` solo se usa la PRIMERA semilla de la lista, una por llamada).
- La voz ElevenLabs va ~2,5 palabras/s con estas etiquetas: para 6 min ≈ 800 palabras.
- **Varias voces = varios personajes (opción, el usuario, 7-oct-2026; pensada para LogIA/noir, vale en cualquier canal):** el narrador
  es `VOZ["voice_id"]`; para que otra voz interprete a un personaje (el estafador, un testigo, la víctima) se añade en `guion.py`
  `VOZ_POR_FRASE = {"llamada_4": "<voice_id>", …}` (clave `escena_índice`). Voces de la cuenta: `python videos/mods_ia_fusion/_voces.py`.
  Úsalo para frases dichas EN PERSONAJE (citas, diálogos cortos), con sus propios corchetes (`[whispers]`, `[nervous]`…); la similitud
  de voz de `tts_select` se mide contra la referencia del narrador, así que en esas frases saldrá baja (no bloquea: solo ordena tomas).
- **SFX de ElevenLabs para el drama (el usuario, 7-oct-2026):** además de los efectos sintetizados, golpes, subidas, truenos y texturas
  generados con ElevenLabs y anclados a las palabras (`fx_audio.py` del video → `audio/fx.wav`, que `mezcla` suma; ver CLAUDE.md
  «ARRANQUE RÁPIDO»).

## Voz: problemas ya vividos y cómo evitarlos (voynich, 29-sep: la voz tardó ~1 h en vez de ~10 min)
Antes de generar voz, revisa esta lista. Cada punto costó una ronda completa (~4 tomas x cada frase afectada).
1. **Escribe el guion FINAL antes de `voz`.** Ampliar y luego recortar obligó a generar 116 tomas y a rehacer 20 más. Fija la duración objetivo
   ANTES: ~2,4 palabras/s de voz; el video dura ~voz + 0,4 s por pausa + relleno hasta el compás (a 96 BPM ≈ +1,5 s por escena).
   Para N minutos de video: ~(N x 60 - 25) s de voz (2 min ≈ 105 s de voz ≈ 250 palabras). OJO: eso vale para la voz Enigma; **Dan lee a ~3,3-3,4 palabras/s** (`tesoro_moctezuma`: 918 palabras = 297 s de voz, video de 5:50): para 6 min con Dan ≈ 900 palabras. `python fab.py <v> tiempo` muestra la duración natural.
2. **Cambiar el texto de una frase borra sus tomas** (por clave `escena_i`); insertar o quitar frases DESPLAZA los índices y regenera todas las siguientes.
   Añade/quita frases al FINAL de la escena o acepta el coste.
3. **Whisper es el juez, no el oído:** el control exige CER 0. Lo que falla aunque el TTS lo diga bien:
   - números romanos ("siglo XX", "Rodolfo II") -> arreglado en `qa.normaliza`; cifras (1639, 600) ya se normalizan.
   - nombres raros: "Beinecke" (Whisper oye "Weinecke"), "Athanasius" (oye "Atanasius"), "Baresch" (a veces "Bares"). Solución: quitarlos de la narración
     ("biblioteca de libros raros de la Universidad de Yale", "Atanasio Kircher") y dejar el nombre exacto solo en pantalla.
   - siglas ("ADN" -> "Adán"), tildes de nombres ("Púrpura" sí pasa).
4. **Si una frase falla 4 tomas seguidas, no insistas con más semillas: reescríbela** (o quita el nombre propio). `todo` ya reintenta 2 rondas de 4 semillas.
5. **GPU compartida = voz 40x más lenta.** Chatterbox va a ~30 it/s; con la GPU llena (VRAM > 7,5 GB de 8) baja a ~1 it/s y una toma tarda 15 min. Los culpables vistos:
   el locutor del panel (`avisos_voz`, Chatterbox con voz Faraon, ~3 GB; se carga con cada aviso y se descarga a los 5 min) y otros programas del usuario.
   Antes de `voz`/`seleccionar` mira `nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv`: si hay > 4 GB usados sin que corra nada tuyo, espera a que baje
   (no mates el panel: ver memoria "panel-nunca-detener"). Regla: NO lances `voz` y `seleccionar` (Whisper) a la vez, ni depth/rembg mientras genera voz.
6. Los avisos por voz del panel se disparan al terminar cada etapa: lanzar muchas etapas seguidas mantiene el locutor cargado y frena la voz. Encadena las etapas en un script.
7. Comandos largos por consola (heredocs > ~8 KB, o con ``/comillas triples) se rompen: escribe los parches con Write y ejecútalos (`` se convierte en backspace: usa `chr(92)+"b"`).
8. Flujo eficiente: guion final -> `voz` -> `seleccionar` (una sola vez) -> mientras tanto trabaja SOLO en imágenes (CPU) -> `tiempo` -> resto. Usa `videos/voynich/_ronda2.py` como plantilla
   de "voz + seleccionar con reintentos" en segundo plano.
9. **CER 0 no garantiza que suene bien (historia_espana, 4-oct-2026):** Chatterbox a veces suelta un sonido ininteligible (0,1-0,4 s) ANTES de la primera
   palabra, separado de ella por un silencio; Whisper (GPU, beam 5) lo ignora y la toma sale con CER 0, pero el oído lo nota («oas, Fenicios…»). Whisper en CPU
   (`WhisperModel("large-v3", device="cpu", compute_type="int8")`, `word_timestamps=True`) sí lo transcribe: úsalo para diagnosticar. Desde esa fecha
   `qa.silenciar_arranque` (llamado por `tts_select`) silencia ese bloque si el primero es ≤ 0,35 s, el hueco ≥ 0,20 s y queda ≥ 1 s de voz; conserva la duración,
   así que los tiempos no cambian. Si el usuario dice que «al principio dice otra cosa», mira la envolvente (RMS cada 0,1 s) de `voz/final/<clave>.wav`: bloque corto, silencio, palabra.
