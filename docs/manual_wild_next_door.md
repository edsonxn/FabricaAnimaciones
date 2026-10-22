# Manual rápido: un video de Wild Next Door de principio a fin

_Creado el 11-oct-2026 (video `arana_techo`) a pedido del usuario: para que un agente en una conversación nueva sepa en
minutos qué hacer, sin repetir la exploración. Léelo entero (≈ 5 min); el detalle técnico vive en
`docs/estilo_secuencia_flow.md` (consúltalo por sección, no entero)._

## SIGUIENTE VIDEO: propuesta y receta rápida (actualizado el 11-oct-2026 tras `cinco_bichos`)
**Estado del calendario:** `bichos_invierno` 15-oct, `arana_techo` 18-oct, `cinco_bichos` 21-oct (todos 16:00 UTC). El siguiente
hueco es el **24-oct**. Confirma con `python fab.py yt videos wild_next_door` y BITACORA.

**Antes de elegir tema, mira los 7 días de `ciempies_casa` (hecho: 440 vistas en 2,5 días) y `arana_techo` (medir el 25-oct):**
si la lista de `cinco_bichos` rinde parecido a un solo bicho, repite la lista con otro grupo; si un solo bicho gana, vuelve a
«Never Kill a X». Candidatos con evidencia en `canales/metricas/ideas/wild_next_door.md`:
- «5 Spiders You Should Never Kill in Your House» (las arañas son lo que más rompe la media: ×382, ×32, ×30; araña lobo y
  saltarina YA salieron en `cinco_bichos`, así que usa tejedora de jardín, araña de rincón, araña de patas largas… o cambia a
  «Every Spider in Your House Explained»).
- Hipótesis 3 de `canales/formula/wild_next_door.md`: «Every Bug in Your Garage/Bathroom/Attic Explained» (NATURE ARCHIVE DOCS,
  ×5 a ×20 en 6 videos).
- Bichos sin video propio: ladybug vs. asian lady beetle, tijereta (ya en lista), crisopa, escarabajo de suelo, mosca sírfida.

**Qué hizo `cinco_bichos` y conviene copiar** (`videos/cinco_bichos/`: `guion.py`, `hacer_prompts.py`, `_ronda.py`, `_dl.py`):
| Paso | Lo que funcionó | Tiempo / tokens |
|---|---|---|
| Datos | `ideas --actualizar` + formula + 6 búsquedas rápidas de hechos con fuentes de extensión | ~15 min |
| Guion | lista en cuenta regresiva (5→1) + «la que sí» + cierre circular; ficha de hechos en el docstring; 1 458 palabras = **8:38** reales | recortar ~300 palabras tras contar |
| Voz | `_ronda.py` (copiar, cambiar `V`): 75 frases × 4 tomas = **~45 min** de GPU; 8 frases acabaron con `CER_MAX_POR_FRASE` (cifras) y `TAIL_MAX_POR_FRASE` (cola alta con transcripción completa) | segundo plano |
| Prompts | 1 por beat con constantes de FICHA; tarjetas con numeral (5,4,3,2,1) dieron el dígito bien las 5 veces | 96 prompts ≈ 20 k tokens |
| Imágenes | **navegador integrado + `nucleo/flow_integrado.py`** (sección de abajo); 96 imágenes en ~25 min, 8 rehechas | ≈ 4,5 k tokens por lote de 12 |
| Música | `lyria_tramos.py` con 4 tramos (≤ 170 s cada uno): 0 problemas | 3 min |
| Armado | `video; mezcla; final; verificar` en UN comando de fondo | ~10 min |

**Hueco de la ruta con extensión (flowscrap):** necesita Claude in Chrome conectado. Si se desconecta (pasó el 11-oct a media
sesión, sin causa visible), no insistas: usa la ruta del navegador integrado de abajo.

## Imágenes SIN extensión de Chrome y con 0 puntos (probado el 11-oct-2026, `cinco_bichos`)
- **Con 0 puntos de Flow las IMÁGENES siguen gratis** (Nano Banana 2 Lite; el panel dice «La generación consumirá 0 puntos»).
  Solo los clips de video piden puntos. Sin saldo: video todo imagen (`SECUENCIA["video_s"] = 0`), como `ciempies_casa`.
- El **navegador integrado** del app (`mcp__Claude_Browser__*`) ya tiene sesión de Flow con la misma cuenta; no necesita Chrome ni
  la extensión. Pasos (≈ 25 min para 96 imágenes):
  1. `python nucleo/flow_integrado.py paquete <v>` escribe `videos/<v>/_bundle.js` (prompts.json comprimido con la FICHA y los
     ayudantes `__ins`, `__col`). Léelo con Read y pégalo UNA vez en `javascript_tool` (≈ 6 k tokens).
  2. `navigate https://flow.google.com/` → «Nuevo proyecto» (un proyecto nuevo por episodio) → `resize_window` 1500x800
     (si no, el panel sale diminuto) → chip del prompt: **Imagen · 16:9 · Nano Banana 2 Lite · x1** (el defecto es «2.1» y x2).
  3. Lotes de 12 con `browser_batch`: por cada prompt `javascript_tool` → `await window.__ins(i)` y `computer` → `key Return`
     (el botón de enviar ignora el clic sintético; Return real sí). Al final `await window.__col(12)` devuelve, en orden de
     envío, «uuid expires firma» de las imágenes nuevas.
  4. Bajarlas: `python nucleo/flow_integrado.py bajar <v>` con las líneas «N uuid expires firma» por stdin → `medios/scene-NNN.jpg`
     (las URLs firmadas se bajan con curl sin cookies; el navegador integrado NO puede hablar con `127.0.0.1`).
  5. `python fab.py <v> medios` y revisar las hojas; rehacer con `window.__R` + `__insR` (ver `cinco_bichos`) o con
     `__ins(i)` tras corregir el prompt; guardar las viejas en `medios/_ronda1/`.
  6. Al terminar: `resize_window preset desktop`.
- Cuidado: el pase del 11-oct generó ~12 imágenes cada ~45 s sin ningún aviso de «actividad inusual». Si aparece, bajar el ritmo.
- **Hallazgos de `doce_animales` (19-oct-2026, 191 imágenes + 7 clips, ~2 h):**
  - Al empezar, el navegador integrado había perdido la sesión de Flow: el usuario la inició en el panel (pedirlo al principio).
    El saldo está en el menú de la cuenta (avatar → «N puntos de Google Flow»).
  - El portapapeles NO llega al panel (Ctrl+V pega vacío y `clipboard.readText` da permiso denegado): el paquete se pega en
    `javascript_tool`. `paquete` ya no repite el cierre en cada prompt (arreglado: 75 k → 38 k caracteres). Antes de enviar,
    comparar un hash por prompt (JS frente a Python).
  - `browser_batch` admite 25 acciones como máximo: lotes de 12 = 12 × (`__ins(i)` + `key Return`) + `__col(12)`, con las
    esperas DENTRO de `__ins` (1,5 s antes y 2 s después de escribir). 0 envíos perdidos en 191.
  - **Clips desde el panel:** Vídeo · 360p · 10 s · x1 = 7 puntos (modelo «Omni 1.1 Flash»; 6 s = 5). Salen en ~1 min.
  - **DESCARGAS QUE ABREN «GUARDAR COMO» = EN EL CHROME DEL USUARIO (regla del usuario, 22-oct-2026; igual que las fotos 2K
    de `docs/estilo_pegatina_flow.md`):** el 720p «Resolución mejorada» de los clips (y cualquier descarga de Flow que en el
    navegador integrado abra la ventana «Guardar como» de Windows) se baja con **Claude in Chrome**, que tiene la autodescarga
    puesta: abrir la URL del editor del clip (`flow.google.com/project/<p>/edit/<id>`, la da el integrado al abrir el clip) →
    icono de descarga → 720p → cae en `E:\Downloads_jaire\<Titulo>_720p_<fecha>.mp4` → copiar a `medios/scene-00N.mp4` y
    verificar con ffprobe (1280x720). El integrado sigue sirviendo para GENERAR (imágenes y clips) y para las imágenes 1K, que
    se bajan con curl. En `arana_amarilla` el integrado dejó ventanas «Guardar como» abiertas que el usuario tuvo que cerrar
    a mano (una la guardó como `manu.mp4`) y un clip nunca llegó.
  - **Imágenes con «Nano Banana 2.1 · x1» = 0 puntos (22-oct-2026, `arana_amarilla`)**: mejor dibujo que el 2 Lite y el
    mismo `flow_integrado.py` (paquete + `__ins` + Return + `__col`) funciona igual: 104 imágenes en ~20 min, 1 rehecha.
  - **Hueco = 72 h EXACTAS** desde la hora real de publicación del anterior (`yt subir` lo comprueba): si el anterior salió a
    16:01:10, programar a 16:05, no a 16:00 (`arana_amarilla`, 22-oct-2026).
  - Identificar cada clip por el TÍTULO del editor (Flow lo pone en inglés: «Spider in web», «Grandmother telling story…») y
    comprobar un cuadro antes de renombrar: la tira de miniaturas del editor va del más nuevo al más viejo.
  - Revisar los clips: marco blanco + línea negra en 2 de 7 (medir filas > 215 desde el borde → `recorte_por` 0.03) y voz o
    risa en 2 de 7 (Whisper `base.en` en CPU sobre el mp4, ~1 min → `ambiente_por` 0 o FX sin audio).
  - **Negro de transición:** el clip combinado «escena uno → escena dos» puede pasar ~1 s por negro TOTAL (en `doce_animales`
    el zoom dentro de la boca de la zarigüeya, a los 12 s del gancho). Medirlo antes de armar (% de píxeles < 25 cada 0,1 s;
    > 85 % = negro) y saltarlo con el mismo clip encima: `dict(clip("scene-002", ("scene-002", t_corte), "scene-002:fin"),
    desde=fin_del_negro, vel=…, entra=0, sale=0)` (ejemplo en `videos/doce_animales/efectos.py`).
  - **Clips de clímax a mitad del video:** FX `video` a cuadro entero (`clip()` en `efectos.py`, `recorte=` si traen marco);
    su audio no entra en la mezcla. Cuadrar el rango con la duración real del clip (`fx --seco`): un clip de 6 s puesto en
    3 beats de 14 s congela 8 s.
  - Defectos en las imágenes (10 de 191): marco (2), onomatopeyas «BONK!» y «zzz», «OFF» en un interruptor, «CHAMPION» en un
    trofeo, boca dibujada como un «3», carteles con garabatos y un secundario que cambia de cara. Pedir «no sound effect
    words / no snoring letters / plate completely blank» desde el primer prompt.
- Defectos que salieron en 96 imágenes (8 rehechas): marco en una (detectar con esquinas blancas + línea oscura; las noches dan
  falsos positivos), conteo de ojos equivocado cuando la frase pide contar (pedir «exactly six… three pairs, no more»), humano
  realista en vez del monigote (si el prompt dice «a person», cámbialo por la ficha `human`), número en el rosetón, caras
  humanas dentro de una lupa y la escena central ausente (nido de barro). Revisar SIEMPRE las hojas completas.

## FOTO REAL de cada animal como pegatina (regla del usuario, 18-oct-2026; SIEMPRE, todo video del canal)
Al **presentar** cada animal o bicho (cuando la voz dice su nombre por primera vez, p. ej. «Number seven. The opossum.»),
encima del dibujo de Flow entra una **foto REAL** del animal como **pegatina animada** durante **~4-5 s**, para que el
espectador sepa cómo es en la vida real. Vale para listas y para videos de un solo bicho (en ese caso, una vez al
presentarlo y otra en «cómo distinguirlo»).
- **Mecánica:** la misma pegatina del motor SECUENCIA YT (`mg_tes.pegatina`: entra con rebote girando, se balancea y flota;
  foto opaca → rectángulo de esquinas redondeadas con marco blanco y sombra; píldora con el nombre debajo). Se declara en
  `videos/<v>/efectos.py` con `peg(en, slug, titulo)` (copiar `peg()` de `videos/_plantilla_yt/efectos.py`), `en` = las
  palabras exactas de la voz que lo nombran. Píldora: «REAL LIFE: <NOMBRE COMÚN>» o solo el nombre.
- **Tamaño y sitio:** grande, ~1/3 del alto (`tam` 480-560), en la esquina donde el dibujo deja aire (x=.20 o .80, y=.58);
  alternar lados entre animales. Nunca tapar la mascota de la ficha.
- **Fotos:** Wikimedia Commons (licencia libre; API `commons.wikimedia.org/w/api.php`, `prop=imageinfo&iiprop=url|extmetadata`),
  una foto nítida del animal entero, de cuerpo completo, fondo natural, sin marcas de agua. Guardar en
  `videos/<v>/pegatinas/<slug>.jpg` y anotar autor + licencia en `pegatinas/CREDITOS.md`; los créditos van en la descripción
  de `youtube.json` («Real-life photos: Wikimedia Commons, <autor> (CC BY-SA 4.0)…»).
- **Revisión:** `python fab.py <v> fx hoja` → `previews/fx_NN.jpg`; comprobar que cada foto es la especie correcta (no la
  parecida: reclusa vs. araña lobo, culebra rayada vs. cabeza de cobre).
- **Lo aprendido en `doce_animales` (19-oct-2026, 14 fotos):** en las tarjetas de numeral («11» a la izquierda, mascota a la
  derecha) la foto va SOBRE EL NÚMERO (x=.20): 3 de 14 tapaban a la mascota en la primera hoja (milpiés, sapo, murciélago).
  Si el bicho ocupa la parte baja, súbela (`y=.24`). Plantilla lista: `videos/doce_animales/efectos.py` (`peg()` con «REAL
  LIFE: …»). Fotos con defecto: bicho chico en su foto → recortar; ejemplar de museo con alfiler → tapar la cabeza del
  alfiler con `cv2.seamlessClone` de un trozo espejado del mismo élitro (el parche simple deja un halo). Originales en
  `pegatinas/_orig/`. Créditos de todas en la descripción (`youtube.json`, «REAL-LIFE PHOTOS»).

## IMÁGENES VIVAS: parallax y personaje que se mueve (pedido del usuario, 19-oct-2026; desde `doce_animales`)
Las imágenes de Flow ya no van quietas: en el armado, `python fab.py <v> vivo` propone las candidatas (personaje claro,
8-55 % del cuadro, 1-3 piezas) con su línea FX y la hoja `previews/vivo_NN.jpg`. Se pegan en `efectos.py` las que lo
merecen: primeros planos del animal (`respira`), dos personajes frente a frente (`baile`), un bicho en el aire (`flota`),
el bicho sobre un dedo (`balanceo` con `capa` = solo el bicho). Y `VIVO_AUTO = 12` da parallax suave a todas las demás.
Receta completa, parámetros y trampas: `docs/estilo_secuencia_flow.md` § «Imágenes vivas». Va antes de `video`, después de
que estén todas las imágenes; revisar la hoja y 3 s de las animadas a tamaño completo (halos, huecos, líneas dobladas).
Dónde va en el flujo y cuánto cuesta (tokens y tiempo): paso **7b** de «Paso a paso».

## El canal en 6 líneas
- Alias `wild_next_door`, canal **en INGLÉS** (audiencia de EE. UU.). Tema: bichos y animales de tu casa y jardín, con el
  giro «no es lo que crees / no lo mates».
- Estilo: **secuencia Flow**, una **ilustración de dibujo animado** (tinta negra gruesa y colores planos sobre fondo claro)
  por beat, generada en Google Flow. Motor `secuencia`: **NO se dibuja por código**. No es plastilina (eso es Plastitube).
- Voz: **Chatterbox con `EnglishComic.mp3`** (no ElevenLabs, así que no lleva corchetes). Música: **Lyria** (`LYRIA` en
  guion.py), nunca la procedural.
- Ciclo: **un video cada 3 días a las 16:00 UTC**, nunca dos el mismo día. Lote = privado y programado.
- Duración: de 4 a 10 min. El usuario suele pedir 9 min, que son **~1 380 palabras** (EnglishComic lee ~2,54 palabras/s
  con GAP 0.26).
- Miniatura: dibujo sobre fondo claro, frase manuscrita de 2-4 palabras y flecha curva al bicho (se genera en Flow).

## Qué funciona (resumen del 11-oct-2026)
**La versión al día, con evidencia, registro e hipótesis, está en `canales/formula/wild_next_door.md`.** Procedimiento
para revisarla antes de cada video (vale para todos los canales): `docs/que_funciona.md`.
- **Formato ganador: «Never Kill a X. Here's Why».** `ciempies_casa` sacó 440 vistas en 2,5 días, contra 2-3 vistas de
  arañas y avispas con el mismo estilo y la misma voz. Las preguntas de temporada («¿qué pasa con X en invierno?») no
  funcionan.
- Fuera, **la araña patona del techo que caza viudas negras** rompió la media en 3 canales chicos (×382, ×32, ×30). Las
  listas «5 animals you shouldn't kill around your house» (×72) y «Every bug in your <cuarto> explained» (×5 a ×20 en un
  mismo canal) también rompen la media.
- Por qué funciona: (1) **contraste**, algo frágil o feo vence a lo que da miedo; (2) **gancho en segunda persona y en
  una escena concreta** («It is two in the morning… you grab the broom… Don't.») con el giro en < 20 s; (3) **consejos
  prácticos alternados con datos raros**; (4) la miniatura dibujada con frase corta y flecha; (5) el tráfico llega sobre
  todo por **videos sugeridos**: un tema que ya es viral fuera se cuela junto a ese video.
- **Mascota con un accesorio fijo en la FICHA** para reconocerla entre imágenes: el ciempiés con sombrerito azul de
  detective, la araña macho con moñito rojo, la araña patona con gorra azul de vigilante nocturno.

## Paso a paso (comandos desde `C:\FabricaAnimaciones`)
1. **Hueco y tema.** `python fab.py yt videos wild_next_door` y BITACORA: el hueco es el último programado o publicado
   + 3 días, a las 16:00 UTC. Llena el registro de los videos que ya cumplieron 7 días y revisa qué funciona y por qué
   (`docs/que_funciona.md` → `canales/formula/wild_next_door.md`). Luego propón 3 temas que repitan la fórmula y cambien
   UNA variable, cada uno con su video de referencia y su ×. Comprueba que el tema no esté hecho:
   `grep -ri "<bicho>" videos/*/guion.py`.
2. **Pregunta al usuario** (AskUserQuestion): tema, duración y **saldo de puntos de Flow**. Precios en 360p con descarga
   «720p mejorada» gratis: **10 s = 7 puntos, 8 s = 6, 6 s = 5**. El de 10 s rinde más (1,43 s por punto): gasta todo el
   saldo con clips de 10 s y cubre el resto con uno de 8 s o de 6 s. Ejemplo: 55 puntos = `clips_s=[10]*7+[8]` = 78 s.
3. `python fab.py nuevo <v> --secuencia` y reescribe `guion.py` copiando `videos/arana_techo/guion.py`, que es la
   plantilla buena: voz EnglishComic, `clips_s`, `combinar=True`, FICHA de dibujo animado y LYRIA por escena con 4 tramos
   de ≤ 170 s. La plantilla del motor viene en español, con plastilina y Dan: cámbialo todo. Reglas del guion:
   - Números SIEMPRE en letras.
   - Frases de < 200 caracteres.
   - Una ficha de hechos con fuentes en el docstring (extensiones universitarias).
   - Mito del bicho anunciado en el gancho y resuelto a mitad del video (cliffhanger).
   - Escena de «cómo distinguirlo» y de «qué hacer si lo encuentras».
   - Cierre circular que vuelve a la escena del gancho.
   - Valida palabras y cifras: `python -c "import guion,re; ..."` (ver ESTADO de `arana_techo`).
4. **Voz** en segundo plano: copia `videos/arana_techo/_ronda.py` (cambia `V`) y córrelo. Hace `voz` → `seleccionar` con
   2 rondas de reintentos → `tiempo` → `beats`, con el log en `_ronda.log`. Antes mira la GPU
   (`nvidia-smi --query-gpu=memory.used --format=csv`, < 4 GB). Las frases con cifras ≥ 10 o palabras raras pueden fallar
   por Whisper: oye la toma y acéptala con `CER_MAX_POR_FRASE`.
5. **Prompts:** escribe `hacer_prompts.py` (modelo: `videos/ciempies_casa/hacer_prompts.py`). Lleva un prompt por beat,
   escrito desde el `texto` exacto de `beats.json`, con la FICHA palabra por palabra, encuadres variados y «full-bleed».
   Los beats de video llevan «Scene one… Then <transición>… Scene two…» (lista de transiciones en el doc de estilo).
   Luego `python fab.py <v> prompts`.
6. **Flow** (el usuario debe tener Chrome con la extensión `flowscrap` Y la pestaña de Flow VISIBLE; lee antes § «Hallazgos de sin_medicina» al final de este manual): sigue `docs/estilo_secuencia_flow.md`
   § «Generar en Flow» y § «Clips de video».
   - **Clips e imágenes van en proyectos de Flow distintos.**
   - **Una sola pestaña de Flow.**
   - Modelo de imagen «Nano Banana 2 Lite · x1».
   - Lanza un clip de prueba primero.
   - Puente: `python fab.py <v> servir` en segundo plano, con el log en ruta absoluta.
7. `python fab.py <v> medios` → MIRA todas las hojas `previews/medios_NN.jpg`. Rehaz las que tengan marco, texto, el
   personaje cambiado o no ilustren su frase.
7b. **Imágenes vivas** (desde `doce_animales`, 19-oct-2026; § «IMÁGENES VIVAS» arriba): con TODAS las imágenes ya
   aprobadas, lanza `python fab.py <v> vivo` en segundo plano, sin vigilarlo (~10-15 min para ~190 imágenes: rembg en la
   CPU, profundidad en la GPU; antes mira que la GPU esté < 4 GB y que no haya voz ni render). Mira las hojas
   `previews/vivo_NN.jpg`: de las recomendadas, quita las que arrastran media escena y pon `capa` donde la pieza 0 es una
   cabeza cortada o el suelo. Pega las líneas en `efectos.py` + `VIVO_AUTO = 12`. **Coste:** 0 tokens de API (todo
   local); lo único que gasta es revisar ~8 hojas, como las de medios. Render MEDIDO (19-oct, `doce_animales`): 8 → 30 min con 23 vivos + `VIVO_AUTO` en 14:25 (antes se estimaba ~+6 min por ~30 beats animados y ~+15 min
   por el parallax en todas), así que si hay prisa se quita `VIVO_AUTO`.
8. Desde la carpeta del video, `python ../../nucleo/lyria_tramos.py` (8 tramos ≈ 4 min por API) → `python fab.py <v>
   ambiente` → `mezcla` → **vista previa** `video --hasta 60` (`salida/<v>_AVANCE.mp4`, ~40 s) → `video` → `mezcla` →
   `final` → `verificar`, los cuatro últimos en UN comando de fondo. Revisa el MASTER con la vista (un cuadro cada ~3 s).
   **Miniatura** (19-oct-2026): en el navegador integrado, proyecto nuevo de Flow, Imagen · 16:9 · **Nano Banana 2.1 · x2
   = 0 puntos**; los prompts de `videos/doce_animales/_miniatura.py` se escriben con `computer type` en el cuadro y Return
   (no hace falta el paquete JS). Las 6 imágenes deletrearon bien el texto. Bajar los `<img>` de `flow-content.google`
   (1376x768) con curl, recortar a 16:9 y reducir a 1280x720.
9. **Publicación:** `youtube.json` (modelo: `videos/ciempies_casa/youtube.json`, con fuentes y aviso de IA en la
   descripción) y la miniatura de Flow en `salida/miniatura.jpg`. Luego
   `python fab.py yt subir <v> wild_next_door private --publicar <ISO del hueco>` y anótalo en `canales/wild_next_door.json`
   (`publicados`, con `"formato": "never_kill"` o el que toque) y en BITACORA. Si el video ya fue público, no se puede
   programar por API: hay que resubirlo.
10. Actualiza el `ESTADO.md` del video y, si aprendiste algo, este manual.

## Errores que ya costaron caro (no repetir)
- **Tres videos públicos el mismo día** (7-oct): hubo que retirarlos y resubirlos. Siempre privado + programado.
- `ciempies_casa` salió público el 9-oct (01:32 UTC) aunque estaba programado para el 12-oct, el mismo día que arañas.
  Antes de programar, compara `yt videos` con BITACORA.
- Imágenes en el mismo proyecto de Flow que los clips = llegaron corridas una posición. Usa un proyecto nuevo y revisa
  las 8 primeras.
- Flow dejó «Nano Banana 2.1» por defecto y la extensión no lo reconoce: elige a mano «2 Lite».
- Prompt sin «full-bleed… no border» = Flow dibuja la escena como viñeta con margen. Si un clip trae marco, usa
  `SECUENCIA["recorte_por"]`.
- Clips sin «Sin diálogo» = Flow mete voces (el motor lo añade solo). Comprobar con Whisper sobre `audio/ambiente.wav`.
- **(11-oct, `arana_techo`) flowscrap salta a 720p a mitad del lote** (15 puntos por clip). Su control lo detiene sin gastar;
  los clips que queden se mandan A MANO: selector en Vídeo · 360p · 10 s, pegar el prompt, enviar, y luego ··· → Descargar →
  720p · Resolución mejorada (cae en Descargas con el nombre del clip; se mueve a `medios/scene-XXX.mp4`).
- **No reiniciar `servir` durante un lote de clips**: los clips quedaron corridos una posición (ya corregido en el código:
  ahora toma `Descargas/<carpeta>/<scene>.mp4` por nombre). Verifica SIEMPRE por huella MD5 contra Descargas.
- El modelo de VIDEO dibuja la telaraña en espiral aunque se pida «no spiral»; el de imagen sí obedece.
- Flow cuela rótulos en cajas, máquinas y globos («STORAGE», «CARGO», «FURNACE», «COUGH!», «whistle»): poner
  «every box, crate, jar and machine is plain and unlabeled» y «no speech bubbles» en los prompts con utilería u onomatopeyas.
  Un personaje secundario que sale en varias imágenes (el conductor de TV) necesita su propia ficha o cambia de cara.
- Marcos de tarjeta en los clips: detectarlos midiendo las 4 esquinas (blancas frente al interior) en t = 0,3, 2, 4, 6 y 8 s,
  y ponerles `recorte_por` 0.035. En `arana_techo` los tenían 5 de 8 clips.

## Hallazgos de `sin_medicina` (12-oct-2026, Sapiens con Wifi, primer video Flow del canal) — LEER ANTES DE GENERAR EN FLOW
Origen: se tardó ~4 h de reloj en el tramo de Flow por problemas que no eran del guion. Todo lo de abajo ya costó tiempo o puntos.

### Regla de cierre (el usuario, 12-oct-2026; vale para TODOS los videos y canales)
Al cerrar un video (subido, miniatura puesta y programado) se documentan EN LA MISMA SESIÓN los hallazgos y mejoras: aquí (si es de
secuencia Flow) o en el `docs/estilo_*.md` del estilo, + la línea correspondiente en `ESTADO.md`. Entra: qué falló, cómo se arregló,
y qué mejora de código/proceso evitaría repetirlo. Sin esto el video no está cerrado.

### Saldo de Flow y clips
- **El saldo real puede ser menor que el dicho.** Aquí el usuario dijo «50 puntos» y el 7.º clip de 10 s falló con «Has alcanzado tu
  límite de uso» (el banner «Te quedan pocos puntos» ya lo avisaba). Planear `clips_s` con un clip de margen o abrir Flow y leer el
  banner/saldo ANTES de fijar `clips_s`. Los clips que fallan por saldo no cobran.
- **Si falta un clip NO corras `python fab.py <v> beats` otra vez:** vuelve a trocear TODO el tramo de imágenes con otros cortes y los
  ~100 prompts ya escritos dejan de corresponder. Se resolvió así: restaurar el `beats.json` anterior, partir SOLO el beat del clip
  perdido en dos imágenes (`texto_a`/`texto_b`, cortando en `t_medio`), renumerar ids y desplazar +1 las claves de `I` en
  `hacer_prompts.py` (ver el final de `videos/sin_medicina/hacer_prompts.py`). Mejora pendiente: escribir `hacer_prompts.py` con
  claves por TEXTO del beat (no por número) para que sobreviva a cualquier recorte.
- **flowscrap dice «Flow no mostró la pestaña Video en sus ajustes» y a pesar de eso SÍ genera el clip.** No relances: duplica el gasto.
  Mira primero la cuadrícula de Flow. Si los clips ya están generados y no bajan, descarga a mano: ⋮ de la tarjeta → Descargar →
  **720p Resolución mejorada** (una a la vez; tarda 1-4 min; cae en Descargas con el título del prompt; copiar a
  `Descargas/flow-<v>/scene-00N.mp4` y a `medios/`).
- **Verifica SIEMPRE con ffprobe que cada `medios/scene-00N.mp4` mida 1280x720.** El colector viejo posteaba el 360p por `/medio` y
  pisaba al 720p; el colector nuevo (en `docs/estilo_secuencia_flow.md`) solo usa `/video_listo` para los clips.
- **Marcos/viñetas en los clips: 3 de 6** (margen blanco fino, esquinas redondeadas oscuras). Medirlos con una hoja de las esquinas de
  cada clip a 2x (recorte 260x150 ampliado, en `previews/_esquinas.jpg`) y fijar `SECUENCIA["recorte_por"]` (aquí 0.035-0.04).
  Cambiar `guion.py` invalida la firma: `video --rehacer` re-renderizó todo (5 min), no solo el tramo.

### Chrome, pestañas y extensión (lo que más tiempo costó)
- **Si la pestaña de Flow no está visible, Flow no avanza:** `document.visibilityState === "hidden"` congela los temporizadores
  (`setTimeout` no vuelve y el CDP da timeout de 45 s), no carga los `<img>` de la cuadrícula y los envíos no se registran. Pasa cuando
  el grupo de pestañas de Claude queda colapsado/tapado en la ventana del usuario. Desde las herramientas NO se puede activar una
  pestaña (ni con `tabs_create`, ni cerrando pestañas, ni con Ctrl+Tab desde PowerShell). **Pedir al usuario que haga clic en la
  pestaña «Google Flow»** y comprobar `visibilityState` antes de cada lote largo. No mandar JS con `await setTimeout` largos:
  hacer las esperas con `computer wait` dentro del `browser_batch`.
- **El navegador integrado del app perdió la sesión de Flow** (el 11-oct la tenía) y no se puede iniciar sesión por el usuario:
  la ruta de imágenes «sin extensión» (`flow_integrado.py`) depende de que el usuario inicie sesión ahí. Confirmarlo al principio.
- **La extensión para IMÁGENES es lenta y desordena:** ~1 imagen/min, y con `count` x2 saca 2-3 variantes por prompt que se
  descargan como `<uuid>.jpg` (no `scene-NNN`) y fuera de orden. Para 100 imágenes es mejor el LOTE POR PEGADO desde `browser_batch`:
  1. Cargar `escenas.json` desde el puente en la página (`fetch http://127.0.0.1:8791/escenas.json`) y definir `__ins(sid)` SIN
     temporizadores: `execCommand('selectAll'/'delete'/'insertText')` en `.ProseMirror`, y comprobar que el editor quedó VACÍO tras
     el envío anterior (si no, el `Return` no se registró: reenviar).
  2. Por prompt: `javascript_tool __ins('scene-NNN')` → `computer wait 2` → `computer key Return` → `computer wait 3`. Lotes de 12-16
     por `browser_batch` (~80 imágenes en ~25 min). El `wait 2` antes del `Return` evita envíos que no se registran.
  3. La cuadrícula de Flow está virtualizada: NO contar tarjetas para saber si se envió (sirve el editor vacío).
  4. Recoger: recorrer la cuadrícula con scroll y juntar `img[src*=flow-content]`; el orden del DOM es de la más nueva a la más
     vieja, así que invertirlo da el orden de envío. Subirlas desde la propia página al puente con `fetch(src).blob()` →
     `POST /medio/scene-NNN` (más simple que bajar URLs firmadas). El puente `servir` se apaga a los 20 min sin novedad y al llegar
     a COMPLETO: reiniciarlo antes de recoger.
  5. Proyecto NUEVO de Flow por tanda para que el orden de la cuadrícula sea exacto (el chip de modelo se conserva: Nano Banana 2 Lite x1).
- Si ya hay archivos `<uuid>.jpg` en Descargas, el nombre ES el uuid de la imagen en Flow: se pueden cruzar con el orden de la cuadrícula.

### Calidad de las imágenes (Nano Banana 2 Lite)
- Se cuelan **dígitos** en escenas con muchos niños (la anciana con niños salió con 4-9 sueltos) y **etiquetas** en diagramas médicos
  (la rodilla trajo «ACL/MCL/PCL»). Añadir al cierre de TODOS los prompts: «Absolutely no numbers, digits or numerals anywhere in the
  picture» y, en diagramas, «no labels, no letters». Rehacer con la instrucción más estricta NO mejoró (011 y 045 salieron peor): mejor retocar.
- Retoque rápido sin regenerar: borrar etiquetas con `cv2.inpaint` (máscara de píxeles oscuros en las cajas de las letras) y una línea
  de borde de panel; quitar un marco blanco fino recortando ~22 px por lado y reescalando (`scene-056`). Guardar el original en
  `medios/_variantes/`.
- Flow no cuenta bien («seis de color y cuatro fantasmas», «siete de diez»): salen 3 fantasmas o 5 de 7. Evitar prompts que
  dependan de contar, o aceptar la aproximación si la frase solo dice «cuatro de cada diez».
- Beats de 7-8 s con una sola imagen se ven quietos (la deriva de cámara lo disimula): si el guion trae beats largos, partirlos.
- Miniatura en Flow: generar siempre ≥ 2 variantes. La B colaba una palabra suelta («waldo»); la A («SIN PASTILLAS» entre comillas y
  deletreada, Sapi + cráneo con agujero + flecha) salió limpia. Texto de 2 palabras, sin tildes.

### Fuentes y datos
- **Nunca escribir DOIs de memoria:** de 8 DOIs, 3 estaban mal y 1 apuntaba a un artículo de inmunoterapia. Verificar cada uno con
  `curl https://api.crossref.org/works/<doi>` (leer el título) o buscarlo con `query.bibliographic=` antes de pegarlo en la descripción.
  Correctos aquí: Rakus `10.1038/s41598-024-58988-7`, trepanación `10.1016/j.wneu.2018.03.143`, Dmanisi `10.1038/434717b`,
  Villabruna `10.1038/srep12150`.
- Voz Dan: ~3,3 pal/s; para 8:52 hicieron falta 1.505 palabras; Whisper deforma nombres propios («Shanidar», «Ötzi»): quitarlos de la narración.

### Tiempos de esta producción (para planear sesiones)
Clips ≈ 1 h con los problemas de arriba; imágenes 106 ≈ 25 min por lotes bien hechos; Lyria 4 tramos 2 min; render 5 min con 12
procesos aunque estuvieran abiertos `chatterbox_server.py` y `app.py` (no hizo falta cerrarlos); mezcla + final + verificar 3 min;
subida 3 min.

### Mejoras que se pueden implementar en el siguiente video
1. `nucleo/flow_lote.py`: generar desde `escenas.json` el JSON de `browser_batch` por lotes (ins + wait + Return + wait) y el
   recolector por POST, para no teclear los lotes a mano.
2. `hacer_prompts.py` por TEXTO de beat (no por número) y cierre «no numbers/labels» por defecto en la plantilla.
3. `fab.py <v> medios --medir`: ffprobe de la altura de cada clip y detección de marcos/esquinas (sugerir `recorte_por`).
4. `fab.py <v> doi`: verificar con Crossref todos los DOI de `youtube.json` antes de subir.
5. Al inicio de la sesión de Flow comprobar: saldo (banner), `visibilityState`, sesión del navegador integrado, y avisar al usuario.
