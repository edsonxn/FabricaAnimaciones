# Estilo NOIR — cine negro en tinta y aguada (canal LogIA)

_Creado el 6-oct-2026 con `videos/ia_noir/` («El caso de la máquina», 5:58, 16:9). Referencia pedida por el usuario: ilustración 2D
hiperdetallada de cine negro, SOLO blanco y negro de alto contraste, claroscuro, lluvia, farola, gabardina y fedora, humo de cigarro,
sombras de persiana, textura de cómic vintage en tinta y aguada; muy dramático, existencialista, lleno de movimiento._

## Qué es
- `ESTILO_VISUAL = "noir"`. Cada escena (`esc_<id>.py`) es una `BaseNoir` (`videos/ia_noir/basen.py`) montada por **planos**:
  `self.plano(t0, fn, tr="barrido|empuje|tinta|relampago|humo|fundido", dur)`; `fn(h, t, u)` dibuja y devuelve `h.acabado(...)`.
  Entre escenas, **mancha de tinta** que cubre y se retira (0,5 s; el negro total dura un instante).
- **Híbrido**: el hilo es DIBUJADO (detective, ciudad, documentos, utilería) y los insertos son **video real de Pexels convertido en
  tinta** (`clip_noir`: suavizado que conserva bordes, aguada en 5 tonos, contorno de pluma, tramado en las sombras). ~35 % de planos.
  **Desde el 8-oct-2026 es regla** que los personajes reales salgan con su foto (ficha en tinta) y que el video real (Pexels, Pixabay,
  yt-dlp) se pinte siempre en este B/N: § «REGLA: MEDIOS REALES» más abajo, kit `nucleo/noir_real.py`.
- Narrador = el detective (primera persona, voz ElevenLabs «Edoardo»). Investigación como estructura: testigos, sospechoso, motivo,
  pruebas, carrera, desenlace, duda, caso abierto.

## Kit (núcleo)
| Archivo | Qué hace |
|---|---|
| `nucleo/noir.py` | `Noir(Toon)`: luz MULTIPLICATIVA (`luz_cono`, `luz_radial`, `luz_persiana` = rayas proyectadas), capa **emisiva** (`emitir`, ventanas, brasas: se suma tras la luz y se tapa con lo que se dibuja encima), capa **aditiva** (lluvia/humo/polvo que solo se ven donde hay luz), `pieza()` = forma con aguada + sombra con **tramado de plumilla** + **contraluz** (rim) + tinta; `acabado()` = luz, niebla volumétrica, tinta (bordes), curva S, papel, grano, polvo de película, viñeta. Atmósfera: `lluvia`, `salpicaduras`, `humo`, `motas`, `relampago`, `gotas_vidrio`, `reflejo` (suelo mojado). Texto: `texto_maquina` (letra a letra, nítido a cualquier zoom; `ang`, `ancho_max`), `soporte` (declara la hoja: el texto sale paralelo y cabe), `sello` (tampón). Transiciones: `transicion`, `tinta_cubre`, `iris`. Video real: `clip_noir`, `tinta_de_foto`. |
| `nucleo/noir_pers.py` | `Detective` (cuerpo entero 3/4: caminar, fumar, girar, viento en la gabardina), `Busto` (primer plano detallado: perfil, oreja, barba punteada, cigarro, mano que lo toma y lo lanza), `Frontal` (reparto de frente con luz cenital: rueda de reconocimiento, póker, marionetas), `Figura` (reparto simple) |
| `nucleo/noir_fondos.py` | `Lienzo` gris uint8 + alfa + emisión (poca memoria), `Capa.pegar(h, prof, bruma=…)` (perspectiva aérea), `edificio(tipo=ladrillo/deco/cristal/tienda)`, `ventana`, `escalera_incendio`, `tanque_agua`, `farola`, `letrero_vertical`, `bolsa`, `texto_lienzo` |
| `nucleo/noir_real.py` | **Medios reales en B/N de tinta** (regla § «Medios reales»): `retrato_noir` (FICHA con la foto real de un personaje: papel de foto, cinta/chincheta, sombra, deriva, rótulo a máquina paralelo al papel; devuelve su `quad` para poner un sello encima), `foto_noir` (foto de archivo a pantalla completa, Ken Burns), `clip_real` (como `clip_noir` + `recorte=` + `credito=`), `credito_fijo` (línea de crédito fija sobre franja negra), `cara_de` (comprueba la detección de cara) |
| `nucleo/imagenes_web.py` | `persona "Nombre" 3 --dir imagenes --descargar` = retratos REALES libres (foto principal de Wikipedia + Commons, cara detectada, sin NC/ND/fair use) con `creditos.json`; `creditos .` = bloque de créditos para la descripción |
| `nucleo/videos_stock.py` | video real: `buscar`/`miniaturas`/`bajar` (Pexels y Pixabay) y `ytbuscar`/`ytbajar <url> nombre --desde 1:10 --hasta 1:22` (yt-dlp, solo el tramo, ≤ 720p, sin audio) → `clips/<nombre>.mp4` + `creditos_clips.json` |
| `nucleo/sfx_noir.py` | ~95 efectos sintetizados (lluvia estéreo, multitud, máquina de escribir, tambor de revólver, servos, imprenta, aplanadora, sellos, atmósferas) |
| `nucleo/tts_eleven.py` | voz ElevenLabs (`VOZ = dict(motor="elevenlabs", voice_id=…)`); clave en `canales/tokens/elevenlabs_api_key.txt` |

## Voz y sonido del canal (el usuario, 7-oct-2026; segundo video `videos/videollamada_falsa/`)
- **Corchetes de actuación** en todo el guion (regla global, `docs/voz.md` § Corchetes) y modelo `eleven_v4_turbo` (por defecto desde el 26-oct-2026).
- **Opción: más voces de ElevenLabs para interpretar personajes** (el estafador, un testigo, la víctima): `VOZ_POR_FRASE` en guion.py.
  El detective sigue siendo el narrador; los personajes dicen frases cortas en su propia voz.
- **SFX de ElevenLabs para dar drama** (impactos, subidas, truenos, zumbidos, timbres) encima de los sintetizados de `sfx_noir.py`:
  `fx_audio.py` del video escribe `audio/fx.wav` con los golpes anclados a las mismas palabras que la animación.
- Kit nuevo en `videos/videollamada_falsa/comun.py`: Hong Kong de noche (`hk_*`), `oficina_hk`, `Llamada` (rejilla de videollamada con
  caras que se descomponen en máscaras), `espalda` (personaje de espaldas), `monitor`, `luz_rect`, `banda` (rótulo de énfasis sólido,
  legible sobre cualquier fondo; úsalo en vez de `N.sello` cuando el fondo es irregular).

## Kit del tercer video (`videos/informante_2027/`, 8-oct-2026) — PRIMITIVAS REUTILIZABLES
- `kit27.py` (primitivas base reutilizables): `calendario` (hoja de taco que cae), `carpeta` (el expediente con título de golpe), `hoja` (papel con renglones; devuelve
  T local→mundo), `billetes`, `casa`, `balanza`, `interruptor` (palanca ON/OFF), `reloj_arena`, `puerta` (rendija de luz, se abre),
  `mano_alzada` (votación), `multitud` (siluetas con ritmo propio y pancartas), `robot`, `pantalla_codigo`, `cajas`, `medidor`
  (aguja 0-100 %), `flecha`, `barra`, `taza_arriba` y **`caminante`** (personaje de perfil con ciclo de paso real: rodillas, braceo).
- `mundos27.py` y `comite.py`: ejemplos históricos específicos de ese video. NO se copian tal cual a videos nuevos.

## REGLAS DE VARIEDAD Y NO REPETICIÓN (el usuario, 8-oct-2026 y 10-oct-2026)
### 1. Dentro de un mismo video: cada escena, su propio mundo visual
- **Ningún fondo se repite en escenas distintas.** Si el guion vuelve al mismo lugar, se varía obligatoriamente con otra hora del día, otra luz y otra cámara.
- **La escena muestra lo que dice la frase:** la acción narrada la ejecutan los personajes, no un decorado genérico con texto encima.
- **Densidad mínima por toma:** al menos 3 planos de profundidad, detalle propio del lugar y la época, y animación de ambiente continua (lluvia, humo, polvo, gente).
- **Nada queda quieto más de ~2 s, y ningún plano arranca vacío.** Lo que cae o se escribe empieza con el plano; el remate se ancla a la palabra clave.
- **Ningún clip real se usa dos veces**, y no van dos fichas de retrato iguales a menos de ~30 s de separación.
- **Los efectos de sonido no se repiten:** no va el mismo SFX por cada pieza o elemento que aparece.

### 2. Entre videos: se reutilizan primitivas, no escenas
- **Sí se reutiliza el kit básico:** `K.caminante`, `K.hoja`, `K.puerta`, `N.texto_maquina`, `C.banda`, las capas de luz, lluvia, reflejos y humo.
- **NO se copian escenas (`esc_*.py`), mundos (`mundos27.py`) ni utilería (`props*.py`) de otro video.**
- Cada video nuevo lleva sus propios `mundos_<video>.py` y `props_<video>.py` diseñados para su temática específica.
- Un formato ganador se repite cambiando tema y gancho, pero siempre con escenas y utilería nuevas.

### 3. Comprobación y bloqueo de entrega
- **Hoja global con un cuadro cada 3 s de todo el video (`_hoja_global.py 3`),** vista a tamaño completo antes del render y otra vez sobre el MASTER.
- Se compara visualmente contra los videos previos: ninguna escena debe repetir un fondo, un objeto o una pose de ellos.
- **Fondo repetido o escenario vacío bloquea la entrega.** Si el tiempo no alcanza, se avisa al usuario en vez de entregar a medias.


## REGLA: MEDIOS REALES — caras y video de verdad, en blanco y negro de tinta (el usuario, 8-oct-2026)
Origen: el usuario pidió que los videos noir futuros no se queden solo en dibujo: **las personas de las que habla el guion salen con su
foto real** y **el video real (yt-dlp, Pexels, Pixabay) entra donde ayude, siempre con el efecto B/N**. Aplica a todo video nuevo de LogIA
(los ya publicados no se rehacen salvo que él lo pida). El hilo sigue siendo el dibujo; esto es la capa de realidad encima.

**1. Retratos reales de los personajes.** Al cerrar el guion, y antes de dibujar escenas, haz la lista de personas reales y públicas que
el narrador nombra (fundadores, investigadores, políticos, víctimas ya publicadas en prensa, figuras históricas) y consigue la foto de cada una:
```
python nucleo/imagenes_web.py persona "Nombre como en Wikipedia" 3 --dir videos/<v>/imagenes --descargar
```
Elige la que tenga cara frontal o de tres cuartos, buena luz y ≥ 600 px (la herramienta ya marca `caras=1` y ordena); si dos son buenas,
guarda ambas (`_2`: otro momento del video). **Míralas** (Read) antes de usarlas: que sea la persona correcta (homónimos) y la época
que toca. Cada foto se anota sola en `imagenes/creditos.json`.
- **Dónde ponerlas (criterio del realizador):** (a) en la **primera mención** del personaje, 2-4 s, con `R.retrato_noir(..., rotulo="NOMBRE",
  leyenda="cargo · año")` en cuanto el narrador dice el nombre (`t0` anclado a la palabra); (b) en el **expediente/tablero** cuando la
  investigación junta varios nombres (varias fichas, una por palabra, `R.retrato_noir` con `ang` y `x,y` distintos y `fijacion="chincheta"`);
  (c) como **foto a pantalla completa** (`R.foto_noir`) solo para lugares, edificios, documentos y archivo, no para caras; (d) al **volver**
  a un personaje clave en el desenlace (sello `N.sello` sobre la ficha con `info["quad"]`: «MINTIÓ», «RENUNCIÓ», «CASO ABIERTO»).
  No pongas dos fichas iguales a menos de ~30 s, ni más de 3 a la vez; la ficha se retira con `sale=(t, 0.4)`.
- Mejor foto real que busto dibujado (mismo criterio que `retratos-reales-integrados` en Bitácora Perdida); si el personaje **no tiene
  foto libre** o es un particular, queda como silueta/figura dibujada (`noir_pers`), nunca una cara inventada que sugiera ser él.
- **Límites obligatorios:** solo **figuras públicas o históricas**, y la foto real acompaña **hechos documentados**. En escenas
  hipotéticas o dramatizadas («qué pasaría si», reconstrucciones) y para particulares (víctimas anónimas, testigos, acusados sin condena)
  la persona va dibujada, sin su cara. Licencias: la herramienta descarta NC/ND/fair use; todo lo demás (dominio público, CC BY, CC BY-SA)
  exige crédito → al final, `python nucleo/imagenes_web.py creditos videos/<v>` y pegar el bloque en la descripción de `youtube.json`.

**2. Video real, siempre entintado.** Dos usos, los dos con `N.clip_noir` o `R.clip_real` (B/N de tinta y aguada, Ken Burns, luz del plano):
- **Ambiente / textura (Pexels y Pixabay, libres, sin crédito en pantalla):** `python nucleo/videos_stock.py buscar "server room lights" 6`
  → `miniaturas` para elegir a ojo → `bajar pexels <id> <nombre> --dir videos/<v>/clips`. Reglas de siempre (§ Receta 4): siluetas,
  contraluces y texturas; sin texto legible personal; medir parpadeos.
- **Lo concreto que el narrador menciona (yt-dlp):** la entrevista, la audiencia, la demo, la noticia, el testimonio.
  `python nucleo/videos_stock.py ytbuscar "Sam Altman Senate hearing 2023" 8` → elegir por título/duración/canal →
  `ytbajar <url> senado --desde 1:10 --hasta 1:18 --dir videos/<v>/clips` (solo ese tramo, ≤ 720p, sin audio; anota url/canal/tramo en
  `clips/creditos_clips.json`). Prefiere canales oficiales (gobierno, la propia empresa, agencias) a reuploads.
  **Reglas:** extractos de **≤ 6-8 s**, transformados (tinta) y con **crédito en pantalla** (`credito="ARCHIVO: <canal>"` en `R.clip_real`,
  sale solo a los 0,4 s); ningún clip se usa dos veces; `recorte=(x0, y0, x1, y1)` quita logos, rótulos de noticiero y barras negras de la
  fuente. **Avisar al usuario del riesgo de derechos** de ese material de terceros (igual que en `docs/estilo_documental.md`) y listar en
  la entrega qué clips son de YouTube. Si YouTube pide verificación anti-bot (bloqueo temporal de IP; pasó el 8-oct-2026), reintentar
  más tarde, cambiar a Pexels/Pixabay o, **solo si el usuario lo autoriza**, `--cookies chrome` (usa la sesión de su navegador).
- Proporción: el ~35 % de planos con video real que ya fija el estilo se reparte entre ambos; los clips de yt-dlp son pocos y con peso narrativo.

**3. Flujo y comprobación.**
1. `guion.py`: anotar `MEDIOS` (docstring o comentario: persona → archivo, tema → clip) para no perderlo entre sesiones.
2. Conseguir fotos y clips **antes** de escribir las escenas; hoja de contacto de fichas (`_prueba.py <escena>`) y de clips (`_prueba_clips.py`).
3. En la escena: `R.retrato_noir(h, "alan_turing", x, y, 480, t, self.t_nombre, rotulo="ALAN TURING", leyenda="1912 - 1954")` dentro de `fn(h, t, u)`
   antes de `h.acabado(...)`; sobre fondo oscuro, con luz de la escena (`k_luz=0.95` fija la luz del papel para que se lea).
4. **Revisar a tamaño completo** cada ficha y cada clip (regla de rigor): cara reconocible (si «se dibuja» de más, bajar `tinta`/`poster`
   o subir `local`), el rótulo dentro del papel, ningún texto encima de la cara, el clip sin logos ni parpadeos, el crédito legible.
5. Al entregar: créditos en la descripción + lista de clips de YouTube + aviso de derechos.

**Lecciones de la prueba (8-oct-2026):** los ajustes de `clip_noir` (poster 0,45, tinta 0,7) **deforman las caras** en foto fija: por eso
`retrato_noir` y `foto_noir` usan tinta 0,38-0,40, poster 0,15 y contraste local (CLAHE); la foto se comprime a un rango de grises que deja la
cara en ~0,46 (medio de la curva S) para que no queme; un crédito claro sobre el cuadro no se lee → franja negra y luz fija solo en el texto;
una cara a pantalla completa pierde resolución: para personas, la ficha.

## Receta
1. Guion con el detective como narrador; `ESCENAS` como **literales `{…}`** (el panel lee el guion sin ejecutarlo).
   **Lista de medios reales** (§ arriba): una foto por persona pública nombrada y los clips que pida lo que se cuenta.
2. Voz ElevenLabs (1 toma por frase; ~0,4 créditos/carácter con multilingual v2) → `seleccionar` → `tiempo` (GAP 0,55 para dramatismo).
3. Mundos pintados una vez por proceso (`mundos.py`: ciudad en 4 capas con bruma, interiores) + utilería (`props*.py`).
4. Insertos: `nucleo/videos_stock.py buscar/miniaturas/bajar` (Pexels/Pixabay) y `ytbuscar/ytbajar` (yt-dlp, lo concreto del relato; § «Medios
   reales») → `clips/` (en E:); las fotos de los personajes → `imagenes/`. Preferir siluetas, contraluces y primeros planos de
   textura (manos en máquina de escribir, multitud con paraguas, fichas, servidores); evitar clips con texto legible personal.
5. Música Lyria en 3 tramos (`_lyria_segmentos.py`: ~3 min por pieza, prompt solo musical, sin palabras sensibles) con intensidad que escala.
6. Revisión: `_prueba.py <escena> u…` por escena y `_hoja_global.py 3` (un cuadro cada 3 s de todo el video) antes del render.

## Lecciones
- La luz multiplica: pinta fondos con valores medios y deja el dramatismo a la luz; lo que emite va a la capa emisiva o queda negro.
- Curva S fuerte: tonos > 0,55 queman a blanco; caras ~118, gabardina ~78.
- Texto: rasterizar a la resolución del zoom y pegar SOLO su recuadro (pegar a pantalla completa costaba 8 s/cuadro con muchos textos).
- Texto claro sobre clips de papel no se lee: tinta oscura o sombra + blanco. Sellos con huecos no se leen en letras pequeñas: tinta sólida.
- Clips con parpadeos (un foco que se apaga): medir el brillo por cuarto de segundo y elegir el tramo estable.
- Una cabeza de perfil se reconoce; una de frente en rejilla parece un globo.
- **Texto sobre un papel/pantalla/cartel (el usuario, 8-oct-2026): SIEMPRE paralelo al soporte y dentro de él.** Quien dibuja el
  soporte lo declara con `N.soporte(h, cx, cy, w, hh, ang, s)` (`K.hoja` y `K.carpeta` ya lo hacen; un cristal o un cartel dibujado a
  mano: llamarlo antes de escribir) y todo `texto_maquina` anclado dentro toma su giro y se reduce para no pasar de su borde.
  Fuera de un soporte: `ang=` y `ancho_max=` a mano. Nunca colocar renglones con `T(...)` de una hoja girada sin girarlos también.
- **Caminar (el usuario, 8-oct-2026: «mueven los pies como si caminaran para atrás»):** la rodilla dobla SOLO con el pie en el aire
  y yendo hacia delante; el pie apoyado va estirado y pegado al suelo. No inventar ciclos con senos: `noir_pers.pierna_paso` +
  `cadera_paso` (los usan `Detective` y `K.caminante`). La fase sale de la distancia: `paso = dist / avance_paso(Detective.ZANCADA, s)`
  o `fase=K.fase_paso(dist, s)`; `fase=t * algo` hace patinar los pies. Comprobar con `python videos/informante_2027/_prueba_paso.py`.

## ERRORES A NO REPETIR — `secreto_ia` (hecho por Gemini, el usuario 21-oct-2026: «mal hecho, la animación está fea»)
Lo que lo separa de `informante_2027` (la vara del canal), visto en la hoja de cuadros cada 3 s:
- **Escenario como rectángulos grises sobre negro** (ventana = cuadro con lluvia, alfombra = caja, pasillo = marco con un cuadrito):
  sin muebles, sin personajes, sin 3 planos de profundidad. Cada mundo necesita utilería del lugar (mesas, cables, monitores, sillas).
- **Cero medios reales**: ni foto de los investigadores ni capturas de los papers/titulares (Anthropic, Apollo, Redwood). Viola § «MEDIOS REALES».
- **La IA como un rectángulo blanco en un tubo con una careta sonriente de garabato**: se lee infantil. Un personaje central necesita
  diseño con detalle (y moverse/reaccionar), no una primitiva brillante.
- **Mismo fondo 40 s** (columna en la tarima 1:06-1:45 y otra vez 1:48-2:33) y **tomas quietas** de 6-15 s.
- **Cuadro partido en dos** (mitad iluminada, mitad negra) que parece un fallo de render, no «dos cuartos».
- **Texto mecanografiado con letras perdidas** («¿P EDE UNA IA G ARDAR») y renglones tapados por el degradado del foco.
- Todo demasiado oscuro: la luz debe recortar figuras con detalle, no ocultar que no hay nada.
- Música procedural de respaldo: el canal va con Lyria siempre.
