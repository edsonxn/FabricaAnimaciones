# Fábrica de Animaciones — guía para Claude Code

Pipeline propio (Python, todo local) que produce videos animados 2D con narración, música y efectos sincronizados. El usuario habla español: responde en español. Usa `python fab.py ...` desde `C:\FabricaAnimaciones`.
**Este archivo = una línea por regla, con su fecha.** El texto íntegro de cada una está en `docs/reglas_globales_completas.md` (= **RGC**), sección `### Rnn` / `### Cnn`: `grep -n -A3 '### R18' docs/reglas_globales_completas.md`. Ninguna regla se borra: se resume aquí y el detalle se mueve allá (18-nov-2026). Antes de aplicar una regla en su paso (voz, comentarios, miniatura, subida…), lee su sección.

## Arranque y sesiones
- **Tokens (12-oct; plan MAX 21-oct):** el cuello es GPU/render y la revisión del usuario. Primer chat del día: `get_usage` + 3 líneas. Una tarea por sesión; solo el `ESTADO.md` del video; `API.md`/`BITACORA.md`/núcleo con grep; imágenes a 640x360; no vigilar renders: `python fab.py avisar "texto"` (siempre ElevenLabs, respaldo voz de Windows, nunca Chatterbox; 20/27-oct). → RGC §R01
- **Corte por cuenta (13-oct):** el disco es la memoria: checkpoint en `ESTADO.md` (`## En curso` + `◐ parcial`) antes de cada pieza pesada y tras cada hito; ventana 5 h > 80 % → cerrar tramo; «⚠ TRABAJO SIN REGISTRAR» → conciliar antes de producir. → RGC §R01 · `docs/sesiones.md` §6
- **Corte automático a 180 mil tokens de trabajo (29-oct; candado por video; 5-nov sigue en 180 mil):** al aviso del hook, termina el paso, checkpoint y `start_session` (`user_asked`, `fresh`, «continúa el video <v>» + lo que falta), autorizado; quien recibe la nota no abre otra; el relevo sigue solo hasta el MASTER. → RGC §R01 · `docs/sesiones.md` §7
- **«Buenos días» (12-oct):** `python fab.py buenosdias` → Claude propone el plan del día; tras cada revisión, encuesta corta y `--feedback`; anotar uso por cuenta (`--uso`). → RGC §R02 · `docs/buenos_dias.md`
- **«Buenos días Juchipila» (19-nov):** skill `buenos-dias-juchipila` → `python fab.py buenosdias juchipila` (tablero de la página Noticias de Juchipila en `E:\PaginaFace`), arreglar el vigía, tanda de piezas listas con su imagen, mejora del día aplicada. → skill · `E:\PaginaFace\CLAUDE.md` § `noticias_jch`
- **Retomar (12-oct; robotaller 31-oct):** `fab.py estado [v]` · «continúa el video X» → `fab.py continuar X`; leer solo su `ESTADO.md` y el doc de estilo que cite; `continuar`/`nuevo` encienden `/v2/vivo` solos. Al terminar: «## Sesiones» del `ESTADO.md` + «continúa el video <alias>»; calendario o subida → una línea en `BITACORA.md`. → RGC §R03
- **Video nuevo = UNA SESIÓN, DIRECTO AL MASTER (5-nov):** `fab.py nuevo <v>` (`--secuencia`, `--yt`); sin plan de sesiones ni vista previa salvo que él lo pida; duración la decide Claude por canal; preguntar solo lo que no esté claro. → RGC §R03 · `docs/publicacion.md`

## Reglas de oro
- **REGLA DE ORO `videos/tes_secretos_40/` = nivel mínimo, TODOS los canales (30-oct):** (1) las reglas SUMAN; (2) lo que dice la voz SE VE en ese momento + lista de PROMESAS VISUALES antes del render (5-nov); (3) ningún clip de otro juego/tema; (4) MG nuevos repartidos desde el gancho; (5) pegatinas variadas (`peg_estilos`, `peg_anim`, `presenta`, mapas con `entrada=`; 5-nov); (6) agradecimientos + críticas con burla; (7) `fab.py <v> chequeo` antes de renderizar; (8) cada animación revisada en su cuadro final con `FAB_FX_FINAL=1 fab.py <v> fx hoja` (11-nov); (9) SIN PRISAS: nada de memoria, todo dato visual de su fuente; cerca del corte, checkpoint y no improvisar (12-nov); (10) lo que la voz manda escuchar SE OYE: cada cita comprobada en la mezcla FINAL con Whisper + `previews/citas_audio.mp3` antes de subir (19-nov). → RGC §R04 · `docs/estilo_secuencia_yt.md` § «REGLA DE ORO Y LISTA DE CONTROL»
- **Mejora continua y corregir al usuario (18-nov):** ≥ 1 vez por sesión proponer en una línea qué optimizar; si una idea suya tiene un costo que no ve, decírselo ANTES con datos y una alternativa; decisiones de canales con fuente oficial. → RGC §R05
- **Monetización en cada subida (17-nov; canales `"monetizado": true`):** en la misma sesión, Studio → Anuncios + casilla MID-ROLL + cuestionario → Guardar y comprobar; `fab.py yt monetizado <id>`; no está «subido» mientras siga en `canales/monetizacion_pendiente.json`. → RGC §R07 · `docs/publicacion.md` § «Canales monetizados»
- **Títulos (18-nov):** 40-55 caracteres (tope 60; Shorts ≤ 40), sin paréntesis/corchetes/`|`/emoji, clave y número al inicio, 1-2 palabras en MAYÚSCULAS; `yt subir` los rechaza. → RGC §R08 · `docs/publicacion.md` § «TÍTULOS»

## Reglas globales (una línea cada una; detalle en RGC)
**Lo que se ve**
- **Todo lo que se nombra se muestra, con video de preferencia (10-nov):** clip; si no, `pant()` o pegatina GRANDE nítida; el mapa no basta; la voz habla como quien estuvo ahí; hechizos/efectos/escenas se ven FUNCIONANDO: clip → foto real → Flow con gráficos del juego (19-nov). → RGC §R34
- **Promesas visuales comprobadas (5-nov):** `promesas.md` + `previews/promesas_NN.jpg` antes del render. → RGC §R33
- **Escenas importantes en movimiento (18-nov):** suceso contado = clip real de ese momento; último recurso Flow video 4-6 s marcado RECREACIÓN; `escenas.md`. → RGC §R35
- **Cada imagen por IDENTIDAD, no por nombre (6-nov):** contra la infobox; hoja `previews/pegatinas_check.jpg` mirada a mano. → RGC §R32
- **Lo que no existe → Flow como captura real (5-nov):** ingredientes reales y estilo del juego; beta = «BETA / RECREACIÓN»; también para enriquecer. → RGC §R36
- **Mapas reales con ruta + SFX del mismo juego (23/29-oct):** ≥ mitad de puestos en listas de misiones; coordenadas UESP. → RGC §R30 · **Fotos en el mapa (23-oct):** foto real de lo nombrado junto a su marcador. → RGC §R31
- **Rigor (30-sep):** cuadro cada ~3 s; lista de bloqueos; densidad ≥ 3 planos; al crear un estilo, actualizar doc, esta tabla, `api_kz` y galería. → RGC §R27 · `docs/estilo_kurzgesagt.md` § «ERRORES»
- **No reciclar escenas entre videos.** → RGC §R28 · **Sin subtítulos quemados (30-sep).** → RGC §R13 · **Estilo por canal fijo (30-sep):** no cambiar de motor sin preguntar. → RGC §R37
- **Miniaturas SIEMPRE con Flow (1-nov):** juegos = que parezca el juego, texto escrito por Nano Banana, nunca PIL (6-nov). → RGC §R14 · `docs/publicacion.md` § «MINIATURAS = FLOW»

**Voz y sonido**
- **La voz nunca en otro idioma (10-nov):** `python nucleo/idioma_voz.py <v>` tras `seleccionar`; `IDIOMA_LIBRE` prohibido. → RGC §R21 · `docs/voz.md`
- **La voz no cita fuentes (12-nov).** → RGC §R22
- **ElevenLabs = corchetes de actuación (7-oct):** `eleven_v4_turbo` (26-oct); sin `[whispers]`/`[excited]`/`[shouts]` (2-nov); escritura normal, sin fonética (12-oct; A/B 12-nov). → RGC §R23 §R20 · `docs/voz.md`
- **Si la voz nombra un sonido, se oye (31-oct; comprobado en el MASTER, 19-nov).** → RGC §R17 · **Sonido original del juego (26-oct):** `ambiente_por`. → RGC §R16
- **Música (12-oct; biblioteca 21-oct; SFX 22-oct):** canales de juegos = OST oficial, nunca Lyria (23-oct); resto = Lyria apegada al guion, primero `fab.py biblioteca sugerir <v>`; SFX en `SFX_ELEVEN`. → RGC §R19 §R20 · `docs/musica_biblioteca.md`

**Canales y publicación**
- **Qué canal toca (8-oct) + panel SIEMPRE al día (13-oct; 22-nov):** cada publicación, programación o video que entra a producción se ve en el panel al momento: `yt subir/publicar/aplicar` lo refrescan solos, registrar en `publicados` con la hora real, `TITULO` provisional al crear, comprobar `/api/v2/obra`; Shorts no cuentan (21-oct). → RGC §R09 §R10
- **Siguiente video con datos (8/11-oct):** `fab.py ideas <alias>` + `docs/que_funciona.md` → 3 temas con referencia. → RGC §R11
- **Cierre de video (12-oct):** hallazgos a `docs/manual_*`/`estilo_*`, lecciones en `ESTADO.md`, DOI con Crossref. → RGC §R12
- **Comentarios (27-oct; 28-oct; 3/5/11-nov):** leer NUEVOS antes de cada video; ≥ 4 agradecimientos; MÍNIMO 2-3 críticas con contraburla (del comentario, no de la persona); solo ≤ 10 días; ninguno dos veces; nunca inventar. → RGC §R18 · `docs/estilo_secuencia_yt.md` § «COMENTARIOS»
- **Promo entre canales propios (18-nov):** siempre AL FINAL + pantalla final + descripción, destino con ≥ 2 videos públicos, públicos que se cruzan. → RGC §R06
- **Campaña de suscripción Runa/Tamriel (30-oct).** → RGC §R29
- **Nunca varios videos del mismo canal el mismo día (7-oct):** `horario` de `canales/<alias>.json`; frecuencia y hora las decide Claude con datos (13-oct). → RGC §R24 · `docs/publicacion.md` § «Frecuencia y hora»
- **Render terminado = SUBIR Y PROGRAMAR sin preguntar (20-oct):** `yt subir <v> <canal> private --publicar <ISO del hueco>`; Bitácora y Cronopapel también a Facebook al instante (22-oct). → RGC §R43 · `docs/publicacion.md`
- **APIs, cada una con UN uso (21-oct):** imágenes solo en Flow; AI Studio solo Lyria; nunca probar una API de pago ni abrir `canales/tokens/`. → RGC §R15 · `docs/apis.md`
- **Primero la tele (4-nov):** decisiones `fab.py tele preguntar … --esperar 900`; videos a la tele SOLO si él lo pide (17-nov). → RGC §R25 · `docs/tele.md`
- **Avisar al renderizar (24-oct):** MASTER + `verificar` + chequeos baratos → `avisar`; sin rondas largas antes de su visto bueno. → RGC §R26

## Estilo por canal (primer mensaje: anota estilo y ejemplo; detalle de cada fila en RGC §Cnn)
| Canal (alias) | Estilo | Copiar de | Doc |
|---|---|---|---|
| Bitácora Perdida (`bitacora_perdida`) §C01 | Kurzgesagt isométrico + relieve + retratos reales · docu antiguo (4-nov) | `independencia_mx/` · `ramses_ii/` | `estilo_kurzgesagt.md` §A · `estilo_docu_antiguo.md` |
| Cronopapel (`cronopapel`) §C02 | Boceto + guache, pegatinas Flow, mapa con ubicación, voz Alberto (22-oct) | `historia_jalisco/` | `estilo_boceto_guache_mapa.md` |
| Sapiens con Wifi (`sapiens_con_wifi`) §C03 | Doodle | `neandertales/` | `flujo_produccion.md` |
| Kuriox (`kuriox`) §C04 | Kurzgesagt + Kuri · acuarela (4-nov) | `sol_apagado_8min/` · `ballena_estomago/` | `estilo_kurzgesagt.md` · `estilo_acuarela_pincel.md` |
| Edsonxn (`edsonxn`) §C05 | Jefe de Robots (30-oct; protegidos y `filtro_canal.py`) · disección (5-nov) | `robotaller_mes1/` · `euphoria_robots/` | `estilo_jefe_robots.md` · `estilo_diseccion.md` |
| LogIA (`logia`) §C06 | Noir B/N con medios reales · pegatina Flow (21-oct) | `informante_2027/` · `secreto_ia/` | `estilo_noir.md` |
| Plastitube (`pieza_oculta`) §C07 | Secuencia Flow plastilina, voz Dan | `bichos_invierno/` | `estilo_secuencia_flow.md` |
| Wild Next Door (`wild_next_door`) §C08 | EN INGLÉS, Flow dibujo animado, foto real de cada animal (18-oct) | `arana_techo/` | `manual_wild_next_door.md` |
| Crónicas del gaming (`cronicas_gaming`) §C09 | SECUENCIA YT Nintendo/retro (19-oct), voz Carlos Aguilar (12-nov) | `majora_mask/` | `estilo_secuencia_yt.md` |
| **Crónicas de Warcraft** (`cronicas_warcraft`) N.º 1 §C10 | SECUENCIA YT, voz Johnny (2-nov), Overgear | `tauren_carrera_prohibida` (D:) | `migracion_googleimagenes.md` · `estilo_secuencia_yt.md` |
| Runa Caída (`runa_caida`) §C11 | SECUENCIA YT Elden Ring, Profeta PLANO (11-nov) | `er_radagon_atrocidades/` | `estilo_secuencia_yt.md` § Runa |
| Crónicas de Tamriel (`cronicas_tamriel`) §C12 | SECUENCIA YT Skyrim, Profeta 8 de 10 (12-nov) | `tes_misiones_daedricas/` | `estilo_secuencia_yt.md` § Tamriel |
| Gaia Eterna (`gaia_eterna`) §C13 | Historias de lore WoW, voz clonada de la narradora (29-oct) | `wow_darrowshire/` | `estilo_pegatina_flow.md` § 8 |
| Cuerpo en Neón (`cuerpo_en_neon`) §C14 | Línea blanca + neón (17-oct) | `freno_enojo/` | `estilo_linea_neon.md` |
| **Expediente 141** (`cronicas_cod`) §C15 | SECUENCIA YT CoD, voz Damián (2-nov) | `tes_secretos_40/` | `formula/cronicas_cod.md` |
| Crónicas de LoL (sin json, Studio) §C16 | Análisis táctico + 3D, voz JC; skill `cronicas-lol` | `lol_semana2/` · `lol_worlds_2026/` | `estilo_analisis_tactico.md` |
| T Menos Cero (`t_menos_cero`) §C17 | Línea 3D cohetes (14-nov) | `cohete_crs30/` | `estilo_linea3d.md` |
| Radio Yermo (`radio_yermo`) §C18 | Fallout = receta de Tamriel, Profeta con filtro de radio (17-nov) | `tes_secretos_40/` | `formula/radio_yermo.md` |
| Amaya Vibes (`canal_amaya`) §C19 | Scrapbook coquette, voz Regina (10-nov; no subir sin su OK) | `amaya_navidad/` | `estilo_scrapbook_coquette.md` |
| Mil por Minuto (`mil_por_minuto`) §C20 | Cómo se fabrican las marcas + el negocio, SECUENCIA YT + plano de la línea y contador, voz Brian C (19-nov) | `tes_secretos_40/` | `formula/mil_por_minuto.md` |

(Docs en `docs/`, ejemplos en `videos/`, fórmulas en `canales/formula/`.) **Reels «Que pasa en Juchipila»** = secuencia vertical `jch_<tema>`, no van a YouTube. → RGC §R38
**Video sin canal: preguntar antes** (AskUserQuestion): secuencia con efectos tipo Flow o animación por código; catálogo de otros estilos (noir color, rayos X, terror CRT, anuncio de app, grabado de peste, línea neón, anime vivo, pegatina Flow, línea 3D, análisis táctico…); toda lámina con profundidad, nunca «página web» (14-oct). → RGC §R39 · arranque rápido por código → RGC §R40

## Comandos esenciales (lista completa en RGC §R42)
```
python fab.py estado [v] | continuar [texto] | canales [--actualizar] | ideas [<canal>] | estadisticas [--actualizar]
python fab.py <v> voz | seleccionar | tiempo | comprobar | musica | sfx | mezcla | video | final | verificar | todo | chequeo
python fab.py <v> montaje | escena <id> t1 t2 | video --hasta <s> | --rehacer 270-280 | fx [--seco|hoja] | limpiar
python fab.py biblioteca sugerir <v> | usar <id> <v> <tramo> | sfx buscar <texto>
python fab.py yt canales | metricas <alias> 90 | videos <canal> | subir <v> <canal> private | aplicar | publicar | comentarios <canal>
python fab.py tele … · envivo · amaya · compartir · panel --abrir | --remoto | --lienzo   (detalle: RGC §R42, docs/panel.md, docs/tele.md)
```
Panel: NUNCA detenerlo ni matar los python; renders siempre con `fab.py`. Docs: `docs/flujo_produccion.md` · `voz.md` (ANTES de `voz`) · `apis.md` · `publicacion.md` · `sesiones.md` · `panel.md` · `estilo_*.md` (índice completo: RGC §R41).

## Disco, git y entorno (detalle RGC §R43)
- Lo pesado en `E:\FabricaAnimaciones` (junctions; E: conectado); C: casi lleno; `final` conserva `segmentos/`. Antes de un render largo: cerrar `chatterbox_server.py` y `app.py`; voz (Chatterbox) y render NO a la vez.
- Git: solo código/config; NUNCA `canales/youtube_client_secrets.json`, `canales/tokens/`, métricas, voz/audio/render; `git status` antes de commit; commit en español; `git push`.
- Comandos > ~8 KB fallan en Windows: Write/Edit. Python 3.10, ffmpeg `C:\ffmpeg\bin`, RTX 4060 8 GB; no borrar `~/.cache/huggingface/hub`.
- Entrega: `videos/<v>/salida/*_MASTER.mp4` (1080p) + `.srt`.
