# Voz: problemas ya vividos y cómo evitarlos

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Origen de `Sarcastica.mp3` (encontrado el 30-oct-2026)
Es **Johnny - Mocking, Sarcastic and Rich**, ElevenLabs `HMCmDsbKeaSZp5LMOYKR`, en las cuentas 1 y 2 (la 3 no la tiene). Similitud de timbre
0,958 entre 2 415 voces; la siguiente, 0,86. Prueba con corchetes: `videos/tes_secretos_40/prueba_voz_eleven/` (Eleven y Chatterbox con las
mismas frases). Así se identifica cualquier otra voz: `resemblyzer` contra las muestras gratis de `/v1/voices`, `/v1/history` y `/v1/shared-voices`.

## REGLA: voz de ElevenLabs = CORCHETES de actuación (el usuario, 7-oct-2026; vale para TODOS los canales)
Siempre que un video use ElevenLabs, el guion lleva **etiquetas entre corchetes** que le dan ánimo y sentimiento a la voz según lo que
se narra. Ejemplo que mandó el usuario: `[thoughtful] Anselmo llevaba quince años abriendo la puerta… [short pause] Nadie sabía su
apellido. [sighs] Para los vecinos…`. Primer video hecho así: `videos/videollamada_falsa/` (LogIA).
- **Cómo:** en `guion.py`, `VOZ = dict(motor="elevenlabs", voice_id=…, modelo="eleven_v4_turbo", idioma="es", referencia=…, tomas=1, stability=0.5)`
  y las etiquetas dentro de las frases: `"[sighs] Esa regla murió una tarde de enero. [short pause] En Hong Kong."`.
- **Escritura NORMAL (12-oct-2026):** con ElevenLabs no se aplican reglas fonéticas (son de Chatterbox): números en cifras («11 de julio»), nombres bien escritos («Alice»). «Once de la noche» se leyó en inglés («uans»); «11» sale bien.
- **Etiquetas en inglés**, al inicio de la frase (tono) o en medio (pausa/gesto). Probadas: `[thoughtful]`, `[serious]`, `[curious]`,
  `[nervous]`, `[sighs]`, `[whispers]`, `[short pause]`; otras de ElevenLabs: `[long pause]`, `[excited]`, `[sad]`, `[angry]`,
  `[sarcastic]`, `[laughs]`, `[chuckles]`, `[exhales]`, `[shouts]`. Una o dos por frase y no en todas: que acompañen al guion
  (suspiro antes de la mala noticia, susurro en el remate, pausa antes del dato), no que lo adornen.
- **El núcleo las separa solo:** `config.py` guarda la frase con corchetes en `config.FRASES_TTS[clave]` y deja `ESCENAS` limpia, así
  Whisper (CER), `timeline.json`, el `.srt`, las anclas por palabra y el panel nunca ven las etiquetas. Cambiar una etiqueta regenera
  esa frase (`voz/textos.json` guarda el texto con corchetes). Con etiquetas, `tts_select` tolera silencios internos de hasta 2,5 s.
- **Modelos y costo real** (medido el 7-oct-2026 con la misma frase de 118 caracteres; `videos/videollamada_falsa/_modelos.py` lista
  los de la cuenta y `_prueba_voz.py <modelo>` compara): `eleven_v4` 13 créditos (≈ 0,11/carácter) · `eleven_v4_turbo` 6 ·
  `eleven_v3_conversational` 24 · `eleven_v3` 47 (≈ 0,40, igual que multilingual v2). **POR DEFECTO `eleven_v4_turbo` desde el
  26-oct-2026 (el usuario, al oír a Hope: «suena perfecto… el default debe ser turbo»)**: entiende los corchetes igual (Whisper no
  oyó ninguna etiqueta leída) y cobra **0,20 créditos/carácter frente a 0,40 de `eleven_v4`** (medido con `character-cost`;
  muestras en `videos/oot_remake_cambios/muestras/`). `tts_eleven.modelo()` pasa a turbo todo guion NUEVO que diga `eleven_v4`
  (copiado de un video viejo); un video con tomas ya hechas en v4 sigue en v4 (no cambia la voz a media obra); `VOZ["modelo_fijo"]
  = True` lo fuerza. `voz/eleven_log.json` anota `modelo` en cada toma. Guion de 15 min ≈ 13 800 caracteres ≈ 2 800 créditos.
  Antes (hasta el 26-oct) el defecto era `eleven_v4`: un video de
  6:30 (53 frases) costó ~600 créditos. **OJO: desde el 13-oct-2026 `eleven_v4` cobra ≈ 0,40 créditos/carácter** (medido en
  `sonic_exe`, `duo_promo` y `wow_tres_noches` con `voz/eleven_log.json`): un guion de 8:50 (7 100 caracteres) costó ~2 850. `eleven_multilingual_v2` y los flash/turbo v2 NO entienden corchetes (no los uses con etiquetas).
- Las voces de la biblioteca pública de ElevenLabs se usan por API con su `voice_id` sin añadirlas a la cuenta (Lily en `wow_tres_noches`).
- **Cuentas de respaldo (el usuario, 20-oct-2026):** además de `canales/tokens/elevenlabs_api_key.txt` (cuenta 1), cada clave extra va
  sola en `canales/tokens/elevenlabs_api_key_2.txt`, `_3.txt`… (no versionadas). `tts_eleven.post()` (voz y SFX de `secuencia_fx`)
  empieza por la primera cuenta con saldo y, si la API responde 401/402 (cuota agotada, clave rechazada), sigue con la siguiente sin
  parar; `voz/eleven_log.json` anota `cuenta` en cada toma. Saldo de todas: `python nucleo/tts_eleven.py`. La misma `voice_id` y el
  mismo modelo suenan igual desde cualquier cuenta, así que un video puede mezclar frases de dos cuentas. Los `fx_audio.py` viejos de
  cada video siguen leyendo solo la cuenta 1.
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

## REGLA: mezcla de Applio = cadena «suave» (el usuario, 13-oct-2026)
El Montaje del panel reproduce la voz cruda (~-20 LUFS) y el MASTER la pasaba por la cadena de Chatterbox/ElevenLabs
(-2 dB 280 Hz, +2 dB 3,5 kHz, compresor 3:1 +3 dB, reverb 5 %, todo a -14 LUFS): «se escucha diferente, más fuerte». En el A/B
de `wow_pistas_futuro` el usuario eligió la **B**: con `VOZ motor="applio"` la mezcla usa HP 70 Hz + compresión 1,6:1, sin EQ de
timbre ni reverb (`config.CADENA_VOZ="suave"`, automático). `guion.CADENA_VOZ="completa"` fuerza la vieja (solo `wow_pistas_futuro`
se quedó con la A). El loudness final sigue a -14 LUFS.

## REGLA: voz Applio (Crónicas de Warcraft) = FONÉTICA para el inglés (el usuario, 13-oct-2026)
Applio = Edge TTS `fr-FR-RemyMultilingualNeural` + RVC. La voz base es **multilingüe**: una palabra en inglés la hace cambiar de
idioma («Overgear» leído como se escribe) y una frase suelta muy corta sale con acento de otro idioma («Oficialmente.» →
portugués, «Guarda ese dato.» → italiano). Al revés que ElevenLabs, aquí SÍ hay fonética:
- `FONETICA = {"Overgear": "Óverguir", "Forever": "Foréver", ...}` en guion.py: `config.py` la aplica solo al texto del TTS
  (`FRASES_TTS`); el guion conserva la grafía real (.srt, Montaje, apoyos, YouTube) y `seleccionar` acepta la CER más baja de
  las dos grafías. Cambiar la tabla regenera solo las frases afectadas. Lista y ejemplos: `docs/estilo_secuencia_yt.md` § «Voz Applio».
- **CHATTERBOX NO LEÍA LA FONETICA hasta el 20-oct-2026** (`jalpa`): `tts_gen.py` generaba con la grafía real y solo Applio/ElevenLabs
  usaban `FRASES_TTS`; al cambiar la tabla se borraban las tomas pero salían IDÉNTICAS (misma semilla, mismo texto). Arreglado: Chatterbox
  lee `FRASES_TTS` sin etiquetas `[..]`. Tamriel y Runa Caída (Chatterbox + FONETICA) nunca la tuvieron: el «Skirim» del punto 10 puede
  venir de ahí; en su próximo video, revisar si la fonética ya resuelve esos nombres.
- Nada de frases de 1-3 palabras sueltas; `seleccionar` (con Applio) mide el idioma de cada toma con Whisper sin idioma
  forzado y rechaza p(es) < 0,90 con el aviso «suena a OTRO IDIOMA» (si al oírla está bien: `IDIOMA_LIBRE = ["clave"]`).
- Edge TTS es determinista: regenerar no cambia nada; se reescribe la frase.

## Voz: problemas ya vividos y cómo evitarlos (voynich, 29-sep: la voz tardó ~1 h en vez de ~10 min)
Antes de generar voz, revisa esta lista. Cada punto costó una ronda completa (~4 tomas x cada frase afectada).
1. **Escribe el guion FINAL antes de `voz`.** Ampliar y luego recortar obligó a generar 116 tomas y a rehacer 20 más. Fija la duración objetivo
   ANTES: ~2,4 palabras/s de voz; el video dura ~voz + 0,4 s por pausa + relleno hasta el compás (a 96 BPM ≈ +1,5 s por escena).
   Para N minutos de video: ~(N x 60 - 25) s de voz (2 min ≈ 105 s de voz ≈ 250 palabras). OJO: eso vale para la voz Enigma; **Dan lee a ~3,3-3,4 palabras/s** (`tesoro_moctezuma`: 918 palabras = 297 s de voz, video de 5:50): para 6 min con Dan ≈ 900 palabras. (`oxigeno_5s`, 14-oct, GAP 0,35: 941 palabras = 303 s de voz → 5:52 de video; calcula ≈ N×60×2,7 palabras para N min con Dan y pausas cortas.) `python fab.py <v> tiempo` muestra la duración natural.
2. **Cambiar el texto de una frase borra sus tomas** (por clave `escena_i`); insertar o quitar frases DESPLAZA los índices y regenera todas las siguientes.
   Añade/quita frases al FINAL de la escena o acepta el coste.
3. **Whisper es el juez, no el oído:** el control exige CER 0. Lo que falla aunque el TTS lo diga bien:
   - números romanos ("siglo XX", "Rodolfo II") -> arreglado en `qa.normaliza`; cifras (1639, 600) ya se normalizan.
   - nombres raros: "Beinecke" (Whisper oye "Weinecke"), "Athanasius" (oye "Atanasius"), "Baresch" (a veces "Bares"). Solución: quitarlos de la narración
     ("biblioteca de libros raros de la Universidad de Yale", "Atanasio Kircher") y dejar el nombre exacto solo en pantalla.
   - siglas ("ADN" -> "Adán"), tildes de nombres ("Púrpura" sí pasa).
   - Umbrales por frase en guion.py (Chatterbox): `CER_MAX_POR_FRASE` (nombres que Whisper escribe distinto), `TAIL_MAX_POR_FRASE`
     (frases que hablan hasta el final) y `GAP_MAX_POR_FRASE` (pausa larga a propósito tras un punto; 18-oct-2026). Úsalos solo
     tras leer en `voz/eval.json` que la transcripción está completa y termina bien.
4. **Si una frase falla 4 tomas seguidas, no insistas con más semillas: reescríbela** (o quita el nombre propio). `todo` ya reintenta 2 rondas de 4 semillas.
5. **GPU compartida = voz 40x más lenta.** Chatterbox va a ~30 it/s; con la GPU llena (VRAM > 7,5 GB de 8) baja a ~1 it/s y una toma tarda 15 min. Los culpables vistos:
   el locutor del panel y `fab.py avisar` (hasta el 26-oct eran Chatterbox, ~3 GB; **desde el 27-oct-2026 los avisos van por ElevenLabs y no tocan la GPU**) y otros programas del usuario.
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
10. **Un nombre inglés con diptongo se COMPRIME en la frase aunque la FONETICA esté bien (tes_exploits_rotos, 17-oct-2026):** con Chatterbox
   `Sarcastica`, «Eskáirim» suena bien en una prueba aislada pero dentro de la frase sale «Skirim» en casi todas las tomas; Whisper escribe
   «Skyrim» de todas formas (CER 0) y nadie lo cazó hasta que el usuario lo oyó. Arreglo: grafía con la vocal alargada («Eskaai rim») y elegir
   la toma donde la palabra DURA más (word_timestamps de faster-whisper: buena ≥ 0,55 s, comprimida ≈ 0,32-0,45 s; Whisper aislado en la
   comprimida oye «Ski»/«Skidding»). Detector y generador en el scratch de esa sesión; método: generar 3 semillas con la grafía nueva, medir la
   palabra, mover las otras tomas a `voz/_descartes/` (y quitarlas de `eval.json`), `seleccionar`, `tiempo`, **`reajustar`** (nunca `beats`).
   Afecta a TODO video de Tamriel/Skyrim con esta voz. **Desde el 23-oct-2026 la grafía es `"Skyrim": "Escairim"`** (el usuario: «Eskaai
   rim» sonaba mal en `tes_cosas_inutiles`); el método de medir cuánto dura la palabra y quedarse con la toma más larga sigue valiendo.

## Voz sin GPU y selección en CPU (banjo_tooie, 19-oct-2026)
- `fab.py <v> voz` con `motor="elevenlabs"` ya NO hace cola de GPU (es una API). `seleccionar` con `$env:FAB_WHISPER_CPU = "1"` evalúa con
  Whisper en CPU (int8) y tampoco hace cola: sirve cuando otra sesión ocupa la GPU con Chatterbox (~30 s por frase en vez de ~3).
- `tts_select` reutiliza las frases cuya toma elegida ya estaba limpia y alineada (`palabras.json` + `voz/final`): rehacer 3 frases ya no
  realinea las 86.
- Cambiar de narrador en un video hecho: la voz nueva puede durar MUY distinto (Hope +14 % frente a Chatterbox Sarcastica). Medirlo
  (suma de `voz/cands`) y preguntar al usuario antes de seguir: velocidad natural (rebajar clips) o acelerar.

- **`silenciar_arranque` borraba una 1.ª palabra corta seguida de pausa** («Hoy, Jalisco…», historia_jalisco 22-oct-2026; `verificar` dio CER 3,9 % en la mezcla). Arreglado en `tts_select.py`: tras silenciar, Whisper vuelve a oír la toma y, si ya no aparece la primera palabra del guion, la toma se deja entera. Para rehacer una frase ya elegida: borra `voz/final/<clave>.wav` y corre `seleccionar` (la duración no cambia: basta `mezcla` + `final`).
