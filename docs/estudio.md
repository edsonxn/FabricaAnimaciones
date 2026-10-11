# Estudio — versión comercial (interfaz sencilla, videos de 60 s)

_Creado 5-oct-2026._ `python fab.py estudio --abrir` → http://127.0.0.1:8790 (puerto con `--puerto`).

Interfaz para público general, sin conceptos del pipeline: **idea → guion → estilo/voz/música → video**.
Cada proyecto es un video normal de la Fábrica (`guion.py` + `escenas.py`) en `estudio/proyectos/<id>/` y se produce
con las mismas etapas (`tts_gen → tts_select → linea_tiempo → comprobar → musica → sfx → mezcla → render video → final`).
**No toca `nucleo/`** (la firma de caché del panel y los videos de los canales no cambian).

## Archivos (`estudio/`)
| Archivo | Qué hace |
|---|---|
| `servidor.py` | HTTP (stdlib) + API JSON; sirve `estudio.html`, videos (Range), miniaturas de dibujos y voces |
| `estudio.html` | Interfaz: Crear video · Mis videos · Voces · Estilos · Ajustes (claro/oscuro, móvil) |
| `escenas_estudio.py` | Escenas genéricas adaptables a **horizontal y vertical** (`IntroEstudio`, `LibreEstudio`, `CierreEstudio`): halo + partículas + cámara en deriva, rótulo, etiquetas ancladas a palabras, cifra grande, 2º dibujo con flecha. Registra `ESTILO_PERSONAL` del guion como estilo «personal» |
| `proyecto.py` | Valida (≤ 125 palabras ≈ 60 s, frases ≤ 190 letras, ≤ 4 frases por parte, números → palabras en español, dibujos válidos) y escribe guion/escenas (literales Python con `pprint`, NO json) |
| `cerebro_gemini.py` | Gemini por REST (`x-goog-api-key`), lista de modelos, guion con `responseSchema` |
| `trabajos.py` | Cola (un trabajo pesado a la vez), producción con progreso, vista rápida (`nucleo/muestra_estilo.py`), prueba de voz, conversión de voces (ffmpeg) |
| `estilos_estudio.py` | Opciones amables (fondo, colores, trazo, letra, partículas) → diccionario de estilo del núcleo |
| `probar_voz.py`, `miniaturas_iconos.py` | Frase de prueba con Chatterbox; miniaturas PNG de los dibujos (`estudio/iconos/`) |

**Disco (5-oct-2026)**: proyectos y vistas previas en `E:\FabricaAnimaciones\estudio` (`proyecto.DATOS`; `FAB_ESTUDIO_DATOS` lo cambia;
si E: no está conectado se usa `estudio/` en C: y Ajustes lo avisa). En C: solo quedan código, ajustes, voces, estilos, iconos y portadas.

Datos del usuario (git los ignora): `ajustes.json` (API key + modelo + procesos), `voces/` (wav 24 kHz mono ≤ 20 s + `voces.json`),
`estilos.json`, `proyectos/`, `iconos/`. `_sistema` y `_muestra_estilo` son proyectos internos.

## Flujo de UN prompt (5-oct-2026, pedido del usuario: «el panel de guion es mucho que hacer»)
- **Crear video**: el usuario escribe una frase, elige formato, voz y estilo (o «Que elija la IA») y pulsa «Crear video».
  `/api/crear` → hilo `crear_video`: Gemini escribe el guion completo (partes, frases, dibujo por parte, 2º dibujo, etiquetas
  ancladas a palabras, cifra, rótulos, texto final, ánimo de la música) y, si el estilo es «auto», elige el estilo (`elegir_estilo`);
  si el guion queda largo, lo pide otra vez 30 palabras más corto; luego arranca la producción. El editor de guion queda
  escondido («Ver o editar el guion» / «o escribir yo el guion»).
- **Fábrica de estilos**: una frase → `/api/estilo/ia` → `disenar_estilo` (Gemini con `responseSchema` de las opciones del
  editor) → se guarda y se pinta su **portada**. El editor manual queda como «Ajuste fino».
- **Portadas** (`estudio/portadas/<id>.jpg`): un cuadro real del estilo (proyecto interno `_portada`, `muestra_estilo` 4 cuadros,
  el 2º recortado al 80 %), en una cola de fondo (`pedir_portada`). Al arrancar se pintan las que falten; al guardar un estilo
  se repinta. ~6-10 s cada una.

- **Vistas previas de 20 s por estilo** (`estudio/vistas.py` → `estudio/vistas/<id>.mp4` 720p + `.json` con su origen):
  se recortan solas los primeros 20 s de un video TERMINADO con ese estilo (proyectos del Estudio primero, luego
  `videos/*/salida/*_MASTER.mp4` de la Fábrica con ese `ESTILO_VISUAL`; revisa al arrancar y cada 90 s). Si no hay, en la
  galería de Estilos → tocar el estilo → «Generar vista previa de 20 s»: guion de muestra con timeline estimado, render +
  música + efectos SIN narración (no usa la GPU), audio mezclado con ffmpeg; va por la cola de trabajos pesados (~2 min con
  10 procesos). Si se ajusta a mano un estilo personal, su muestra generada se borra (ya no lo representa).

- **Estilos Premium** (antes «profesionales»; los de motor propio) (`vistas.CANALES`, ids `pro_*`): vitrina en Estilos con 20 s de un video real
  (`desde` = segundo de inicio elegido mirando la hoja de cuadros; `portada_t` = cuadro de la portada). Kurzgesagt isométrico,
  mapas con relieve, Kurzgesagt ilustrado, vertical Kuriox, mapa pintado Cronopapel, documental de misterio, crimen real y
  guache. **No se eligen** para crear con prompt: probado el 5-oct, las escenas genéricas con `kurzgesagt`/`documental`/`boceto`
  dan íconos sobre fondo liso o espacial, nada parecido (esos looks salen de `plano.py`, `kz_*`, `docu.py`, `boceto.py`).
  Para ofrecerlos en automático haría falta un generador de escenas propio por estilo.

## Modo creativo (beta, 5-oct-2026): agente de tomas
Aprendido de `C:\googleimagenes\holavideo` (clips Remotion: director → la IA escribe el `.tsx` → render → arreglo del
error → corrección con cuadros). Aquí la IA escribe **el código Python de cada toma** en vez de rellenar campos.
Casilla «Modo creativo» en Crear video (fuerza `pro_kz_plano`/`pro_kz_vertical`); `proyecto.json → creativo`.
- `estudio/kit_tomas.py` — `TomaBase(_BasePlano)`: fondo por preset (`CIELO`), cámara deriva+zoom, paralaje (`self.par`),
  franjas reservadas (rótulo/cifra arriba, claves abajo), ayudantes de mundo (montes, suelo, agua, ciudad, árboles, nubes,
  aves, partículas, personas `kz_pers2d`, multitudes, bustos, flechas, contadores). `segura(clase, firma)`: si el texto de
  la parte cambió o la toma truena → `LibrePlano` (con `ESTUDIO_TOMA_ESTRICTO=1` los errores se propagan).
- `estudio/ejemplos_tomas.py` — 2 tomas escritas a mano y **verificadas a la vista**; van íntegras al manual.
- `estudio/agente_tomas.py` — por cada parte intermedia (intro y cierre siguen con plantilla), en 3 hilos:
  director (1 llamada, mundos distintos) → programador (manual = docstrings del kit + catálogo de `plano.py` + ejemplos,
  se arma en un proceso con el PYTHONPATH del proyecto) → revisión AST (sin imports/archivos/eval/while/dunders) →
  `probar_toma.py` en otro proceso (5 cuadros + cobertura + movimiento, timeline provisional) → arreglo con traceback →
  **juez con visión** (nota 1-10, defectos de la Fábrica) → corrección con los cuadros (≤ 2 vueltas; ≤ 6 llamadas de
  código por parte). Se queda la mejor versión que funcionó. Modelo de código `gemini-3.8-flash` (si la key no lo tiene,
  usa el del guion). Salida: `<proyecto>/tomas_ia.py` (lo importa `escenas.py`) + `tomas_ia/` (borradores, pruebas,
  `informe.json`, `hoja.jpg`).
- A mano: `python estudio/agente_tomas.py <id|carpeta> [--solo p2,p3] [--modelo X] --clave-archivo <key.txt>`.
- Ampliar el estilo = añadir ayudantes con docstring a `TomaBase` (entran solos al manual) o un ejemplo verificado.

## Comportamiento
- **Voz**: biblioteca `C:\chatterbox_voices` o clonada (subir audio o grabar con el micrófono; casilla de permiso obligatoria).
  La producción graba 2 tomas por frase (no 4) y regraba hasta 2 rondas las que fallan; si aún fallan, pide cambiar esas frases.
  Usa el mismo candado de GPU que `fab.py` (`_CandadoVoz`).
- **60 s**: tope por palabras antes de producir y, tras `tiempo`, error si el timeline pasa de 66 s.
- **Render**: procesos desde Ajustes (12 por defecto; el render los baja solo si falta memoria). Al terminar borra `segmentos/` y
  `video_sin_audio.mp4`, deja `salida/*_MASTER.mp4` + `.srt` + `portada.jpg`. Exige ≥ 1,5 GB libres en C:.
- **Gemini**: modo económico (Flash/Flash-Lite), la interfaz avisa que **la calidad es inferior** a la producción hecha a mano.
  El guion queda editable; la IA elige dibujos del catálogo (`mascara` excluida: Spider-Man, derechos de autor).
- Medido (5-oct): vista rápida 6 cuadros ≈ 5-15 s; render de 40 s vertical con 6 procesos ≈ 4 min (con la PC cargada).

## Pendiente / ideas
- Probar en vivo la llamada a Gemini con una key real y una producción con voz cuando la GPU esté libre.
- Más dibujos en el catálogo y escenas genéricas con personajes (hoy son íconos sobre fondo con halo).
- Opción de cerebro de calidad alta (Claude API) junto al económico.
