# Propuesta 18-nov-2026: CLAUDE.md y MEMORY.md más cortos (sin aplicar)

**APLICADA el 18-nov-2026 con el visto bueno del usuario.** Respaldo del índice de memoria anterior: `MEMORY_anterior_18nov.md`.

## Archivos
| Archivo | Qué es |
|---|---|
| `CLAUDE.md` | CLAUDE.md propuesto: una línea por regla, con fecha y puntero `RGC §Rnn` / `§Cnn` |
| `anexo_reglas_globales_completas.md` | Texto ÍNTEGRO del CLAUDE.md actual, partido en 43 secciones `### Rnn` + 19 `### Cnn`; se AÑADE al final de `docs/reglas_globales_completas.md` |
| `generar_anexo.py` | Genera el anexo y comprueba que cada línea del CLAUDE.md actual esté en él (solo faltan el título, la intro y 2 encabezados, que siguen en el corto) |
| `MEMORY.md` | Índice de memoria propuesto (va a `C:\Users\jaire\.claude\projects\C--FabricaAnimaciones\memory\MEMORY.md`, fuera del repo) |

## Conteo de tokens (tiktoken cl100k: aproximado; el tokenizador de Claude da algo más en español, la proporción es la misma)
| Archivo | Antes | Después | Ahorro |
|---|---:|---:|---:|
| CLAUDE.md | 17 013 tok (51 300 car.) | 4 860 tok (13 761 car.) | −71 % |
| MEMORY.md | 6 802 tok (20 392 car.) | 2 027 tok (5 864 car.) | −70 % |
| **Total al arrancar cada sesión** | **23 815** | **6 887** | **−71 % (≈ 17 000 tok menos)** |

El objetivo era ≥ 40 %. El contenido no se pierde: el anexo guarda el 100 % del texto, y los 156 archivos de memoria siguen en disco.

## Qué se movió y adónde (CLAUDE.md)
Todo el texto original va a `docs/reglas_globales_completas.md` → `### <id>`. En el CLAUDE.md corto queda la línea indicada.
| Id | Regla (fecha) | Queda en el corto como |
|---|---|---|
| R01 | Tokens, MAX, corte por cuenta, corte a 180 mil (12/13/21/29-oct, 5-nov) | 3 líneas en «Arranque y sesiones» |
| R02 | Buenos días (12-oct) | 1 línea |
| R03 | Retomar; robotaller (31-oct); una sesión hasta el MASTER (5-nov) | 2 líneas |
| R04 | REGLA DE ORO tes_secretos_40 y sus 9 puntos (30-oct; 5/11/12-nov) | 1 línea con los 9 puntos en pocas palabras |
| R05 | Mejora continua y corregir al usuario (18-nov) | 1 línea |
| R06 | Promo entre canales propios (18-nov) | 1 línea |
| R07 | Monetización en cada subida (17-nov) | 1 línea |
| R08 | Títulos (18-nov) | 1 línea con las cifras |
| R09-R12 | Qué canal toca (8-oct), panel de canales (13-oct), siguiente video con datos (8/11-oct), cierre de video (12-oct) | 3 líneas |
| R13 | Sin subtítulos quemados (30-sep) | media línea |
| R14 | Miniaturas con Flow (1-nov; juegos 6-nov) | 1 línea |
| R15 | APIs con un uso (21-oct) | 1 línea |
| R16-R17 | Sonido original (26-oct), si la voz nombra un sonido (31-oct) | 1 línea |
| R18 | Comentarios (27/28-oct; 3/5/11-nov) | 1 línea con mínimos y prohibiciones |
| R19-R20 | OST en juegos (23-oct), Lyria/biblioteca/SFX/escritura normal (12/21/22-oct, 12-nov) | 1 línea + media en ElevenLabs |
| R21-R23 | Voz en otro idioma (10-nov), no cita fuentes (12-nov), corchetes/turbo/sin susurros (7/26-oct, 2-nov) | 3 líneas |
| R24 | Un video por canal al día, ciclos, frecuencia (7/13-oct) | 1 línea (los ciclos por canal: en `canales/<alias>.json`, como dice la regla) |
| R25-R26 | Primero la tele (4/17-nov), avisar al renderizar (24-oct) | 2 líneas |
| R27-R28 | Rigor (30-sep), no reciclar escenas | 1,5 líneas |
| R29 | Campaña de suscripción (30-oct) | 1 línea |
| R30-R31 | Mapas con ruta + SFX del juego (29-oct), fotos en el mapa (23-oct) | 1 línea |
| R32-R36 | Identidad (6-nov), promesas (5-nov), todo lo nombrado (10-nov), escenas en movimiento (18-nov), Flow si no existe (5-nov) | 5 líneas en «Lo que se ve» |
| R37 | Estilo por canal fijo (30-sep) | media línea |
| C01-C19 | Filas de la tabla de estilos (voces con id, altas, cuentas, reglas de canal) | Tabla corta: canal, estilo en pocas palabras con fecha, ejemplo, doc |
| R38 | Reels de Juchipila | media línea |
| R39 | Video sin canal + catálogo de otros estilos; profundidad (14-oct) | 1 línea con los nombres de los estilos |
| R40 | Arranque rápido de video por código | puntero |
| R41 | Índice de docs | 1 línea con los 7 más usados |
| R42 | Comandos esenciales completos (envivo, tele, amaya, compartir, panel remoto, app del teléfono) | bloque de 6 líneas |
| R43 | Disco, git, entorno, entrega; render terminado = subir (20-oct); Facebook al instante (22-oct) | 4 líneas + 1 en «Canales y publicación» |

## Qué se quitó del índice de memoria (los archivos se quedan en disco)
Quitadas porque su regla ya está como línea en el CLAUDE.md corto:
- **Reglas de oro / lo que se ve:** regla-de-oro-tes-secretos-40, revisar-animaciones-cuadro-final, sin-prisas-bien-desde-inicio, mejora-continua-corregir-al-usuario, promesas-visuales-comprobar, todo-lo-nombrado-se-muestra, escenas-importantes-en-movimiento, imagen-correcta-por-identidad, flow-cuando-no-hay-material, mapas-reales-con-ruta-secuencia-yt, fotos-en-el-mapa, pegatinas-objetos-personajes-secuencia-yt, mg-nuevos-por-video-secuencia-yt, rigor-calidad-y-detalle, actualizar-docs-de-estilo, no-reciclar-escenas-entre-videos, sin-subtitulos-quemados, estilos-por-canal, profundidad-no-pagina-web, video-sin-canal-preguntar-camino, miniaturas-por-canal, miniaturas-warcraft-ingredientes-reales.
- **Voz y sonido:** voz-nunca-otro-idioma, voz-no-cita-fuentes, diccionario-pronunciacion-canal, voz-nombra-sonido-se-oye, sonido-original-del-juego, musica-del-juego-canales-gaming, biblioteca-de-musica-lyria, sfx-repetidos-no, imagenes-solo-en-flow-nunca-google-api.
- **Sesiones:** ahorro-de-tokens-revision-periodica, buenos-dias-claude-dirige, corte-por-tokens-cambio-de-cuenta, corte-automatico-contexto-180k, videos-en-tramos-por-sesiones, robotaller-activo-al-iniciar-video, aviso-por-voz-autonomo, panel-nunca-detener.
- **Publicación:** monetizacion-en-cada-subida, titulos-youtube-regla, nunca-varios-videos-mismo-dia, frecuencia-y-hora-las-decide-claude, render-terminado-subir-y-programar, facebook-bitacora-cronopapel-al-instante, panel-canales-al-empezar-y-terminar-video, siguiente-video-con-datos, cierre-de-video-documentar-hallazgos, comentarios-del-publico-gaming, campana-suscripcion-runa-tamriel, tele-google-tv-decisiones, avances-a-la-tv, avisar-al-renderizar-revision-del-usuario.
- **Canales (cubiertos por su fila de la tabla):** voz-johnny-warcraft-tamriel (además ya viejo: Tamriel pasó al Profeta el 12-nov), tamriel-profeta-narrador-principal, voz-gaming-carlos-aguilar, mudanza-canales-warcraft-tamriel-runa, canal-cuerpo-en-neon, canal-gaia-eterna, wild-next-door-foto-real-pegatina, cronopapel-pegatinas-flow, cronopapel-mapa-ubicacion, cronopapel-voz-alberto.

Se quedan (no están en CLAUDE.md): perfil y trayectoria de Edson, canales prioritarios, en vivo, producción, estilos sueltos, fórmulas de WND/Neón/Plastitube, Flow, panel, Overgear, análisis táctico, Gaia, Amaya, Facebook, disco E, etc. Las descripciones se acortaron a lo esencial; el detalle sigue en cada archivo.
**Arreglo de paso:** la línea 28 del índice actual tenía un enlace cortado («[Música Lyria…»); el propuesto enlaza `musica-lyria-adaptada-al-guion.md` y `google-ai-studio-lyria.md`.

## Riesgo y cómo se cubre
Con el corto, el detalle de cada regla (ids de voz, cifras exactas, ejemplos de fallos) ya no está en contexto desde el inicio. Para eso: el corto dice «antes de aplicar una regla en su paso, lee su sección» y cada línea lleva su `§Rnn`, que se lee con un grep de ~200-600 tokens solo cuando hace falta. Si prefiere menos riesgo, se pueden devolver al corto las 3-4 reglas que más se han roto (regla de oro, comentarios, todo lo nombrado) en versión media: el ahorro seguiría arriba del 60 %.

## Para aplicar (cuando el usuario diga que sí)
1. `git status` (hay muchos cambios ajenos: no se tocan).
2. `python docs/propuesta_claude_md/generar_anexo.py` otra vez si el CLAUDE.md cambió desde el 18-nov (el script avisa si falta alguna línea; los números de línea son los del CLAUDE.md del 18-nov).
3. Añadir `anexo_reglas_globales_completas.md` al final de `docs/reglas_globales_completas.md`.
4. Copiar `CLAUDE.md` a la raíz y `MEMORY.md` a la carpeta de memoria.
5. Commit solo de `CLAUDE.md`, `docs/reglas_globales_completas.md` y `docs/propuesta_claude_md/` (MEMORY.md está fuera del repo).
