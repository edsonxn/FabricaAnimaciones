# Bitácora general — Fábrica de Animaciones

Estado al **2026-09-29**. Se armó revisando archivos del proyecto, métricas guardadas, el estado en vivo de YouTube
(`yt videos`) y el cierre de cada sesión anterior. Actualízala al final de cada video o sesión (ver CLAUDE.md).

## 1. Decisiones que esperan respuesta tuya
1. **Git:** hay 17 archivos modificados + 5 rutas nuevas sin confirmar (ver §5). Tres sesiones distintas preguntaron lo mismo:
   ¿un commit con todo junto o separado? Recomendación: todo junto en un commit (los cambios están mezclados en los
   mismos archivos del núcleo) *después* de re-verificar que `40mil_anos` no cambia.
2. ~~Video del Sol~~ → **decidido (29-sep): va a Kuriox** (canal conectado, ver §5). En proceso.
3. ~~Ruta de la Plata~~ → **borrado el 29-sep** (confirmado en YouTube). También desaparecieron las 3 copias del Galeón de Manila.
4. **Cadencia Sapiens con Wifi:** después del 7-oct no hay nada programado. ¿Qué tema sigue para el miércoles 14-oct?

## 2. Calendario de publicaciones
| Fecha (CDMX) | Canal | Video | Estado |
|---|---|---|---|
| 28-sep | Sapiens con Wifi | Los Humanos Antiguos Hacían lo Mismo que Tú (`Uvg8hX78deo`) | **Público** |
| mié 30-sep 14:00 | Sapiens con Wifi | 7 Inventos Antiguos que Usas Todos los Días (`ni6FrdYvon0`) | Privado, programado |
| mié 7-oct 14:00 | Sapiens con Wifi | Neandertales: 7 Mitos que la Ciencia Derrumbó (`mlR8vD9ABuw`) | Privado, programado |
| ~29-sep | Bitácora Perdida | Zacatecas 1546: así se vivía en la fiebre de plata (`NwBYB1s0Q3w`) | **Público** (ver nota en §4) |
| 30-sep | Bitácora Perdida | El tesoro perdido de Moctezuma (`videos/tesoro_moctezuma`, 5:50, animación v2) (`EUXq7-n_i7E`) | **Público** (verificado en YouTube 30-sep) |
| mié 7-oct 14:00 | Cronopapel | Historia de Irán en 5 minutos (`CqSg_v6pFjQ`) | Privado, programado |
| mié 14-oct 14:00 | Cronopapel | Historia de Japón en 5 minutos (`EI0c27EY89E`) | Privado (subido con miniatura y .srt) |
| mié 21-oct 14:00 | Cronopapel | La historia de Egipto en 5 minutos (`3V_C7ZEj5is`) | Privado (subido con miniatura y .srt) |
| 28-oct en adelante | — | — | **Sin video asignado** |

## 3. Canal: Sapiens con Wifi (`sapiens_con_wifi`)
**Nicho:** prehistoria, inventos antiguos, evolución humana. Antes se llamaba «Just Homo Sapiens». Voz: Dan. Formato largo (~3 min).
**Horario:** miércoles a viernes 14:00 CDMX (20:00 UTC); 1-2 videos por semana.

**Números (métricas del 29-sep):** 10 suscriptores, 272 vistas históricas, 17 vistas en 90 días (todas por búsqueda de
YouTube), retención media 6,5 % en la ventana (18,3 % histórica). El video del 28-sep tiene 2 vistas: **no hay datos
suficientes para sacar conclusiones**; los temas salen de investigación del nicho, no de métricas propias.

| Video | Carpeta | Estado |
|---|---|---|
| 10 cosas de hace 40 000 años | `videos/40mil_anos` | Publicado. Miniatura «selfie». |
| 7 inventos antiguos | `videos/inventos_antiguos` | Subido y programado 30-sep. Miniatura «tostada». |
| Neandertales: 7 mitos | `videos/neandertales` | Subido y programado 7-oct. Miniatura «¿BRUTOS?»; quedan `mitos` y `collar` como alternativas. |

**Pendientes**
- [ ] **Subtítulos de `inventos_antiguos`:** al subirlo, el token no tenía permiso `youtube.force-ssl` y el `.srt` no se cargó
      (`subida_log.txt`). Neandertales sí los cargó, así que probablemente ya se reconectó: verificar en Studio o correr
      `python fab.py yt aplicar inventos_antiguos sapiens_con_wifi ni6FrdYvon0` **antes de mañana 14:00**.
- [ ] Revisar mañana tras la publicación de «inventos» (vistas, retención en las primeras horas).
- [ ] Correr `python fab.py yt metricas sapiens_con_wifi 28` hacia el 7-oct y comparar con `canales/metricas/`.
- [ ] Pedir a Studio la gráfica «Cuándo están conectados tus usuarios» y ajustar `horario` en el JSON.
- [ ] Confirmar en Studio que banner y foto de perfil de `canales/arte/` estén aplicados (foto y nombre no van por API).
- [ ] Definir el video del 14-oct (idea de Neandertales: ¿versión «sin cortes» / plano secuencia? la sesión lo ofreció).
- [ ] `canales/sapiens_con_wifi.json` tiene cambios sin commitear (lista `publicados`).

## 4. Canal: Bitácora Perdida (`bitacora_perdida`, `UCZeiiNb2XgM0kt2Ye3d8qbQ`)
**Nicho:** historia de México (Independencia, Guadalajara, San Blas, Galeón de Manila, Zacatecas). Conectado el 29-sep;
idioma cambiado de `en` a `es` (país MX). Además tiene 8 videos largos de prehistoria (1.5 a 4 h) de 2025, en no listado.

**Números (29-sep):** 19 suscriptores, 82 vistas en el contador, 2 060 vistas históricas, 137 en 90 días
(50 % por búsqueda de YouTube), retención media 17 %. Los videos de ~2:40 rinden mejor:

| Video | Duración | % visto medio |
|---|---|---|
| Por Qué la Independencia de México Duró 11 Años | 2:40 | **67,5 %** |
| Por Qué Guadalajara Tuvo que Morir 4 Veces | 2:40 | 58,1 % |
| El Puerto Secreto que Dominó el Pacífico: San Blas | 2:35 | 33,7 % |

**Estado de los videos**
- **Zacatecas 1546** (`videos/zacatecas_vox`): vertical 1080×1920, 3:01, estilo Vox, plano secuencia. Voz CER 0,0005, −14 LUFS, desfase 0 ms.
  YouTube lo muestra **público**, pero la sesión que lo subió lo dejó privado y sin programar: alguien lo publicó después
  (probablemente tú desde Studio). Miniatura `bufa`; quedan `mina` y `moneda`.
- **La Ruta de la Plata** y las 3 copias del Galeón de Manila: borrados por el usuario (29-sep). Ya no aparecen en el canal.

**Pendientes**
- [ ] Registrar Zacatecas en `publicados` de `canales/bitacora_perdida.json` (hoy está vacío).
- [ ] Ver cómo rinde el vertical de 3:00 frente a los de ~2:40 (retención y de dónde llegan las vistas) antes de repetir el formato.
- [ ] Decidir la serie: el guion es «los primeros 100 años»; ¿siguen más ciudades/épocas del mismo estilo?
- [ ] Defectos menores sin corregir en Zacatecas: etiquetas «SEVILLA» y «ESPAÑA» se pisan un poco en la ruta de la plata; los guachichiles
      de la escena de la paz (~2:08) se ven rígidos; tomas anchas del camino con personajes pequeños.
- [ ] Horario propio: aún es el del protocolo; ajustar cuando haya datos.
- [ ] Sin `descripcion` ni `palabras_clave` propias en el JSON del canal (las que tiene en YouTube no se tocaron).

## 5. Canal: Kuriox (`kuriox`, `UC7QhLbgQcdshoidlUzbaTgg`) — conectado el 29-sep
**Nicho:** datos curiosos y ciencia, mayormente **Shorts** verticales de ~50 s más algunos largos (2 a 14 min). 67 suscriptores, 54 videos,
26 271 vistas históricas, 17 140 en 90 días (67 % vienen de Shorts), retención media 36 %. Público: 10 842 vistas de MX, luego AR, ES, PE, CO;
sobre todo hombres de 25-34. Los Shorts rinden mucho (hasta 1 645 vistas; «El origen perturbador de la motosierra» 48 % visto, «La criatura
inmortal» 62 %); los largos venden poco (p. ej. «30 datos reales» 13:59 = 141 vistas, 24 % visto). Métricas: `canales/metricas/kuriox_2026-09-29.json`.
- [x] **PUBLICADO 29-sep** (https://youtu.be/l3JexzfS6-Y, público, miniatura ¿SIN SOL?, subtítulos cargados; CER 0,0004, desfase 0). Detalle previo: re-render con la corrección de Júpiter → `final` → `verificar` (log: `videos/sol_apagado_8min/render_log3.txt`),
      luego `yt subir sol_apagado_8min kuriox public` con `youtube.json` y miniatura «¿SIN SOL?» (`apagon`). **Autorizado por el usuario publicarlo.**
- [ ] Riesgo a vigilar: los largos de Kuriox rinden poco frente a sus Shorts; ver retención del video de 8 min en 48 h. Idea: cortar Shorts verticales de él.
- [ ] Versión de 1 min (`videos/sol_apagado`): sigue con el termómetro invertido; re-renderizar (~6 min) antes de usarla. Es 16:9, no es Short.
- [ ] Sin `idioma` en el JSON del canal ni descripción propia (`canales/kuriox.json` mínimo).

### Estilo y lecciones de Kuriox (LEER antes de hacer cualquier video para este canal)
**Estilo usado hasta ahora:** `ESTILO_VISUAL = "kurzgesagt"` (vector plano, espacio, bloom), plano secuencia sin cortes (`TRANSICIONES = [("continua", 0.1)] * n`,
un solo `Mundo` en escenas.py), voz Dan, música documental (`espacio`/`tension`/`vacio`/`esperanza`), `GAP = 0.75` s entre frases, BPM 110.
Ejemplo (con el pájaro, así se queda): `videos/sol_apagado_8min/` (publicado 29-sep, https://youtu.be/l3JexzfS6-Y).

**Opinión del usuario sobre «¿Qué pasaría si el Sol se apagara?» (8 min): le gustó, pero se le hizo LENTO.**
- Las pausas entre frases fueron demasiado grandes (`GAP` 0,75 s y `post` de 1,5 a 4 s por escena).
- Muy poco movimiento en pantalla: mucho tiempo con un objeto casi quieto.
- **Regla para el siguiente video de Kuriox: más dinámico.**
  - Pausas más cortas: `GAP` ≈ 0,3-0,4 s y `post` ≤ 1 s; ritmo de Short, no de documental contemplativo.
  - Más dibujos por escena y más cosas apareciendo, moviéndose y transformándose (personajes, objetos, rótulos, partículas) en cada frase.
  - Movimiento casi constante: cámara siempre en paneo/zoom, elementos que entran y salen, animación propia por frase, no solo la palabra clave.
  - Nada de más de ~2 s sin que algo nuevo cambie en pantalla.
  - Si el tema lo permite, formato de Short vertical o versión corta: los Shorts son el 67 % de las vistas del canal y los largos rinden poco.
- **Mascota: NUNCA el pájaro morado (`plano.pajaro`).** Es la mascota del canal original que nos inspira; de él solo queremos el estilo de animación.
  La mascota de Kuriox es **Kuri**, un robot explorador redondo (turquesa, pantalla de cara, antena amarilla): `P.kuri(lz, x, y, s, t, mirar=, aleteo=, feliz=, tiritar=, escarcha=, boca=, voltear=)`
  (misma firma que `pajaro`; alias `P.mascota`; ya está en `nucleo/plano.py` y en API.md). **Decisión del usuario: el video del Sol (publicado, l3JexzfS6-Y) se queda como está, con el pájaro; Kuri entra desde el siguiente video.**
  No copiar tampoco otros personajes reconocibles del canal original.
- Al proponer un video para Kuriox, decir cómo se va a cumplir esto (más elementos por frase, pausas cortas) antes de producir.

## 5d. Canal: Cronopapel (`cronopapel`, `UCqwn92RiGu4DbSlRSijj4ew`) — conectado el 30-sep
**Antes:** «Animales de Papel», canal viejo de *Historias Bíblicas* (13 videos cortos públicos, ~9,4 mil vistas, 44 suscriptores, retención media 80 %). **Ahora:** historia condensada y animada en boceto+guache («La historia de X en N minutos»).
Nombre elegido por mí (único en YouTube): **Cronopapel**. Aplicado por API el 30-sep: descripción, 15 palabras clave, idioma `es`, país `MX` (`canales/cronopapel.json`).
- [ ] **Nombre y foto de perfil: solo en Studio** (no van por API). Prompts de perfil y banner para Nano Banana 2 en `canales/arte/cronopapel_prompts.md`.
- [ ] Banner: cuando esté la imagen, reescalar a 2560x1440 (<6 MB), poner `banner` en el JSON y correr `python fab.py yt canal cronopapel`.
- [ ] Decidir qué hacer con los 13 videos bíblicos antiguos (siguen públicos y fuera de nicho; propuesta: dejarlos en *no listado* para conservar vistas y suscriptores sin confundir al nuevo público). No se ha tocado ninguno.
- [x] Nombre, perfil y banner puestos por el usuario en Studio; videos bíblicos viejos borrados por el usuario (30-sep).
- [x] **Subido en privado el 30-sep: https://youtu.be/4Hc-DNPgiRM** («Historia de China en 3 minutos»; metadatos, capítulos y .srt cargados). Miniatura IA (variante A, «CHINA EN 3 MINUTOS») aplicada el 30-sep; falta que el usuario lo publique desde Studio.
- [x] **2.º video: «La historia de Irán en 5 minutos»** (`videos/historia_iran/`, 30-sep): subido en privado https://youtu.be/CqSg_v6pFjQ (MASTER 270 MB, 5:00, CER medio 0,22 %, LUFS -14, desfase A/V 0). Tema elegido por la búsqueda «historia de Irán» (+2.100 %). Música Lyria en 2 mitades (`_lyria_partes.py`: Lyria solo da ~3 min por pieza; corte en sasánidas→islam). Render con 7 procesos (con 11 se agotó la memoria virtual). **[Actualización 30-sep: miniatura IA variante A aplicada y video PROGRAMADO para mié 7-oct 14:00 CDMX = 2026-10-07T20:00:00Z; solo queda que el usuario oiga «Carras» y «safávida»]** Antes era pendiente: miniatura IA (prompt en `prompt_miniatura.md`) → `yt aplicar historia_iran cronopapel CqSg_v6pFjQ`; programar mié 7-oct 14:00 CDMX = 2026-10-07T20:00:00Z con `yt publicar cronopapel CqSg_v6pFjQ public --programar`; el usuario debe OÍR dos nombres que Whisper dudó: «Carras» (~1:54) y «safávida» (~3:13).

## 5b. Video del Sol (astronomía, estilo Kurzgesagt)
| Video | Carpeta | Estado |
|---|---|---|
| ¿Qué pasaría si el Sol se apagara? — 1 min | `videos/sol_apagado` | Renderizado, **con un error**: el termómetro tenía los colores al revés. Código ya corregido; **falta re-renderizar** (~6 min). |
| Mismo tema — 8 min | `videos/sol_apagado_8min` | MASTER de 480 s verificado (CER 0,0004, −14 LUFS, −1,11 dBTP, desfase 0). **Corrección a medias:** el reloj «1 h 11 min» se encima ~2 s con «43 min» de Júpiter (~2:12). Se movió la órbita y se rehízo el tramo 126–159 s, pero al empalmar quedaron 14 402 cuadros en vez de 14 400; el `video_sin_audio.mp4` de `salida/` es ese intento fallido. El MASTER bueno no se tocó. Opciones: localizar el cuadro sobrante o re-renderizar completo (~40 min). |

Miniaturas del de 8 min: `apagon`, `congelada`, `ocho` (una sesión recomendó la que dice «¿SIN SOL?» por leerse mejor en celular).
- [ ] Decidir canal (§1.2), luego terminar el punto anterior y pasar `verificar`.
- Los MASTER pesan 405 MB (8 min) y 56 MB (1 min): no llegan al móvil (límite 30 MB).

## 5c. Historia de la humanidad en 60 s (`videos/historia_60`) — 29-sep
Vertical 1080x1920, sin voz, kurzgesagt, plano secuencia con 19 épocas (200 000 años -> hoy) y portales entre ellas. Música procedural
(flauta/épico/brillo/reloj/final, 128 BPM) + ~300 efectos. Con narración de Dan (lee el texto en pantalla de cada época, CER 0 sobre la mezcla, voz/fondo 11,5 dB, -14,5 LUFS, -1,05 dBTP), sin subtítulos encima.
MASTER: `videos/historia_60/salida/historia_humanidad_60s_MASTER.mp4` (44,7 MB). Sin canal asignado, miniatura ni publicación. Ver CLAUDE.md (estilo Kurzgesagt actualizado y videos sin voz/voz anclada).

## 6. Motor, repositorio y documentación
**Repositorio:** `github.com/edsonxn/FabricaAnimaciones` (privado). Solo hay 2 commits (`d0cf10d`, `f4c2b7c`); todo lo de
28-29 sep está sin confirmar:
- Modificados: `nucleo/` (config, dibujos, efectos, escena_base, estilos, fondos, linea_tiempo, miniatura, motor, plano, prueba_escena, qa, render, sfx, verificar),
  `videos/sol_apagado/escenas.py`, `canales/sapiens_con_wifi.json`.
- Nuevos: `nucleo/vox.py`, `canales/bitacora_perdida.json`, `videos/neandertales/`, `videos/sol_apagado_8min/`, `videos/zacatecas_vox/`.
- Antes de commitear: `git status` y confirmar que no entra ningún secreto (los tokens y `youtube_client_secrets.json` ya están ignorados).

**Pendientes de motor**
- [ ] Tras los cambios al núcleo, la regla del proyecto pide `python fab.py api` (API.md es del 28-sep 13:45, anterior a `vox.py` y al modo vertical)
      y **re-verificar `videos/40mil_anos`** (no debe cambiar). Nadie lo ha hecho.
- [ ] Documentar en `CLAUDE.md` el estilo **`vox`** (`nucleo/vox.py`, `FORMATO = "vertical"`) y la mejora de render paralelo/optimización.
- [ ] `videos/zacatecas_vox/` tiene archivos de trabajo (`_parche1-4.py`, `prueba_*.py`, logs): ordenar antes del commit.
- [ ] Disco C: 20,7 GB libres (suficiente). Los MASTER de 400-500 MB por video se acumulan: decidir cuáles conservar.

## 6d. «El tesoro perdido de Moctezuma» (Bitácora Perdida) — `videos/tesoro_moctezuma`, 30-sep
- **v2 (vigente): motion graphics animados cuadro a cuadro, estilo Kurzgesagt** (`ESTILO_VISUAL = "kurzgesagt"`, Lienzo). 16:9, **5:50**, voz Dan, 19 escenas distintas. Rehecho tras el comentario del
  usuario: «el estilo documental es aburrido, se reciclan fotos y videos, cada escena debe ser distinta, construir escenas cuadro a cuadro que muestren lo que se habla, el desenfoque afecta al texto».
  v1 documental (fotos con parallax + clips de stock) quedó archivada: `salida/*_v1_docu_*` y `escenas_docu.py`.
- Verificado v2: voz CER medio 0,0006 (1 frase en 2,4 % por un efecto de sonido: corregido en `audio/final.wav`), −14,0 LUFS, −1,30 dBTP, voz/fondo 12,4 dB, desfase A/V 0 ms. MASTER 255 MB.
  Si `final` falla con PermissionError, **VLC tiene el MASTER abierto**: el remux corregido se dejó en `salida/tesoro_moctezuma_MASTER_nuevo.mp4` (renombrarlo al cerrar VLC).
- Estructura: `s_a.py`..`s_e.py` (escenas por bloques), `figuras.py` (soldado, guerrero, tlatoani, caballo, canoa, bergantín, obrero, Durero, cañón, barra, discos, cofre, templo mayor, palacio),
  `mapa_local.py` (valle de México: lago, isla-ciudad, calzadas, ciudad moderna), `mapa.py`/`mundo.py` (copiados de Teotihuacán), `util.py` (tiempos de la voz, cámara, texto, agua, lluvia, tarjetas con imágenes),
  `reg.py` (tomas y sonidos), `escenas.py` (ensamblado y transiciones). Mapas reales con Natural Earth 50 m (`datos/tierra_atlantico.json`, dominio público).
  Fotos históricas usadas UNA vez cada una como «tarjeta»: Durero, suplicio de Cuauhtémoc (Izaguirre), portada de Bernal Díaz, placa del Monte de Piedad.
- Pruebas rápidas sin render: `_prueba.py <nombre> t1 t2 ...` (hoja en `previews/`). Coste: 0,2-0,6 s por cuadro; render 8 procesos ≈ 28 min.
- **Lecciones (importantes para todos los videos):** (1) el usuario prefiere ANIMACIÓN que muestre la acción narrada (soldados que huyen, canoas que atacan, pared que cae, horno que funde) sobre fotos con
  parallax; cada escena con un mundo visual distinto; casi ningún material reciclado. (2) El texto va dibujado en el Lienzo (nítido); nunca aplicar tilt-shift/desenfoque encima del texto.
  (3) En `docu_fx.titular`, `lineas` son CORTES acumulados. (4) Dan lee ~3,4 palabras/s: 918 palabras = 297 s. (5) Render con 13 procesos se queda sin memoria: `--procs 8`. (6) Evitar clips de stock con
  relojes de pulsera/croma; usar dibujo propio. (7) Whisper escribe «rayos X»/«México» por «rayos equis»/«mexica»: reescribir. (8) Comandos largos de consola fallan: escribir parches con Write.
- Archivos de entrega: `salida/tesoro_moctezuma_MASTER.mp4`, `.srt`, miniaturas `oro` (en `youtube.json`), `donde`, `hundido` (`hacer_miniaturas.py` ahora usa cuadros del propio video).
- Disco C: revisar (los MASTER v1 de 2,2 GB se pueden borrar si la v2 gusta).
- **Subido en privado el 30-sep-2026: https://youtu.be/EUXq7-n_i7E** («Tesoro de Moctezuma: la noche en que desapareció»). Miniatura: la generada por el usuario en Nano Banana 2 con el prompt de `prompt_miniatura.md` (`salida/tesoro_moctezuma_mini_final.jpg`). El usuario lo publica desde Studio. Registrado en `publicados`.
- Nota de calidad: Whisper marca `llegada_2` con 2,4 % («regalos» → «freralos») en la mezcla final aunque las tomas crudas dan CER 0; se bajó el efecto de pasos, sigue igual; no lo he podido escuchar: conviene oír ese tramo (0:31-0:37) antes de publicar.
- Lección: flujo de miniaturas con IA y de publicación documentado en CLAUDE.md §8b y §8c.

## 6a. Estilo `boceto` — prueba «El viaje de una gota» (`videos/gota_bucle`, 29-sep)
- Vertical 1080×1920, 44,4 s, en **bucle** (primer y último cuadro idénticos), voz CER 0,0017, −14 LUFS, −1,5 dBTP, desfase 0 ms,
  voz/fondo 11,5 dB. MASTER en `salida/viaje_de_una_gota_MASTER.mp4` (41,6 MB: no llega al móvil). Sin subir ni programar.
- v1 (8 escenas lentas) quedó en `escenas_v1.py`; v2 sigue el ritmo de la referencia de X (kevin_t_ngo): ~30 cambios, bocetos de lápiz,
  física, formas siempre en movimiento y ~130 efectos de sonido. El render tarda ~42 s (composición con numba).
- 29-sep (2.ª pasada): añadidas 6 **transformaciones de objeto a objeto** copiadas de la referencia (`morfosis`); MASTER re-renderizado y verificado (CER 0,0017, −14 LUFS, voz/fondo 11,6 dB, 145 efectos).
  Si `final` falla con PermissionError sobre el MASTER, es que hay un reproductor con el archivo abierto: cerrarlo y mover el `.tmp.mp4`.
- [ ] Si se quiere un video largo con este estilo: escribir frases cortas (1-2 s) y varias imágenes por frase.

## 6c. Estilo `guache` — prueba «Un hombre contra cinco criaturas» (`videos/pelea_meme`, 29-sep)
- Pedido del usuario: crear el estilo del post de X «Economía de la isla» (@e_page: ilustración de libro infantil en gouache, paleta apagada,
  personajes de cabeza redonda, grano de papel) y probarlo con un **video meme de ~1 min**: un hombre contra una criatura por ronda, con
  escenarios y armas distintos. Salió: **Don Beto** (hombre común, bigote, chanclas) vs escorpión gigante (desierto, chancla), tiranosaurio
  (selva, sartén), tiburón (océano, pez espada), extraterrestre (Luna, extintor-cohete) y dragón (volcán, tapa de olla + la chancla que regresa).
- 16:9, 64,8 s, voz Dan (23/23 frases CER 0), plano secuencia (carrera continua entre biomas), marcador de rondas, barras de vida, medallas
  tachadas, ¡PELEA!/¡NOCAUT!, ~134 efectos. Detalle técnico en CLAUDE.md («Estilo guache»). Sin canal asignado ni subido.
- [ ] Si gusta: versión vertical (Short) para Kuriox; ojo, la coreografía usa 1920 px de ancho por bioma.
- [ ] Ideas: más rondas (serie «1 hombre vs ...»), otros héroes/armas, miniatura con Don Beto y la chancla.

## 6b. Música con Lyria (Google AI Studio) — anotado el 29-sep
- El usuario tiene una API key de **Google AI Studio** y con ella se puede generar música con el modelo **Lyria 3 Pro Preview**
  (`lyria-3-pro-preview`: canción completa, control de estructura por secciones con tiempos e intensidad, instrumentos).
  En el Playground se ve el formato de prompt: `[0:00 - 0:20] Intro: Intensity 3/10. ...` / Verse / Chorus, con instrumentos concretos.
- **La key está guardada en `canales/tokens/google_ai_studio.txt`** (carpeta ignorada por git). NUNCA copiarla a BITACORA, CLAUDE.md,
  guiones ni commits.
- Hoy la música sale de `nucleo/musica.py` (procedural, sin voz). Lyria sería una alternativa por video: pedir un prompt por escena
  con la duración de `timeline.json`, guardar el audio en `videos/<nombre>/audio/` y saltar la etapa `musica` (falta integrar en `mezcla`).
- [ ] Probar una llamada real a Lyria (no se ha probado la key ni el formato de salida) y decidir si se integra como `fab.py <video> lyria`.


## 6c. Mini documental «El libro que nadie puede leer» (manuscrito Voynich) — `videos/voynich`, 29-sep
- Estilo nuevo `documental` (motor `nucleo/docu.py`, imágenes `nucleo/imagenes_web.py`), inspirado en «Detrás del Enigma» (Nazca). 16:9, 2:11, voz Enigma.
- Verificado: voz CER 0 (24/24 frases), −14,0 LUFS, −1,4 dBTP, voz/fondo 12,4 dB, desfase A/V 0 ms. Render ~10 min.
- Archivos: `salida/voynich_libro_ilegible_MASTER_v2.mp4` (706 MB, mezcla final; el `_MASTER.mp4` tiene la mezcla anterior y VLC lo tenía abierto),
  `salida/voynich_preview_720p.mp4` (vista ligera), `.srt`. Al cerrar VLC: borrar `_MASTER.mp4` y renombrar `_MASTER_v2.mp4`.
- Sin canal asignado ni subida. Créditos en `imagenes/creditos.json` y en la tarjeta final (CC BY-SA: Kastelic, ArnoldReinhold, Bjoertvedt).
- Versión larga (2:40, con Baresch/Kircher, tarjetas perforadas, 14 pieles, 38 000 palabras): `guion_largo.py` + `escenas_largo.py` (sin voz regenerada).
- Problemas de voz documentados en CLAUDE.md («Voz: problemas ya vividos y cómo evitarlos»).

## 6d. Vista previa dentro del panel — 30-sep
- Botón «▶ Vista previa» en cada proyecto con `timeline.json`: cuadros del motor real (`preview_worker.py`, un proceso por video lanzado por el panel),
  scrub sobre forma de onda + escenas, reproducción con audio (1-2 fps) y «Clip fluido» (5-40 s en paralelo con audio). Decisión: NO migrar a Remotion
  (se quiere conservar la calidad del motor propio). Detalle en CLAUDE.md, sección «Panel de avance».
- Pendiente: el panel del puerto 8765 se lanzó antes de este cambio; hay que reiniciarlo (una vez) para que aparezca el botón.
- Idea futura: pre-renderizar cuadros por delante con un pool persistente para que «reproducir» suba de 1-2 a ~8 fps.

## 6e. «La historia de China en 3 minutos» (canal NUEVO, aún sin crear) — `videos/historia_china`, 30-sep
- **Nicho elegido por investigación (Nexlev):** historia condensada y animada («X años de historia de [país] en N minutos»). Referencia: *Animated History* (84 mil suscriptores en 11 meses, ~550 mil vistas medias). En español hay poca oferta exacta. Serie posible: China, Japón, Rusia, Corea, México, Roma…
- **Video:** 16:9, **3:10** (190 s), voz Dan (42 frases, CER 0; Whisper oye «Gengis Kan» como «Hengish Khan» en la mezcla: CER 3,6 % en 1 frase, pronunciación correcta), música Lyria (candidato 2 alargado 4 % sin cambiar tono), 280 SFX propios (nuevos: explosion, canonazo, crujido, galope, tambor, pluck, trueno, cuerno, tren, monedas). −14,0 LUFS, −1,12 dBTP, voz/fondo 12,3 dB, desfase A/V 0 ms. MASTER 190 MB: `salida/historia_china_3min_MASTER.mp4` + `.srt`. Metadatos en `youtube.json` (título «Historia de China en 3 minutos», capítulos reales) y prompts de miniatura en `prompt_miniatura.md`. **Sin subir** (falta el canal).
- **Estilo nuevo «boceto + guache»:** mapa pintado a guache (campos de distancia con signo interpolados entre épocas: el imperio crece, se encoge y se **fractura** en celdas y se reúne) + personajes/objetos de boceto como **pegatinas** de papel con sombra + **cambios de escena procedurales** (barridos de pintura: tinta, pinceladas, papel rasgado, iris, media tinta, rollo, ola, persianas) + sellos rojos de dinastía (fuente CJK) que se acumulan arriba a la derecha + contador de años. Ver CLAUDE.md «Estilo boceto + guache con mapa».
- Decisión de guion: se recortaron Confucio, el papel y el Gran Canal para no pasar de 3:10 (`DURACION = 190`). Regla del QA: `ALIAS_QA` en guion.py y «a.C./d.C.» ya normalizados en `qa.normaliza`.
- [ ] Crear el canal y conectar (`yt conectar`), subir en privado, generar miniatura (Nano Banana) y publicar.
- [ ] Pendiente menor: algunos cuadros tienen pegatinas encima de los subtítulos (foso de barro ~0:52, multitud Tang ~1:19); personajes algo pequeños para el ancho del cuadro.

## 7. Fuera de este proyecto (no auditado)
Hay sesiones aparte en `C:\googleimagenes` (**Crónicas de Warcraft**, Gaia Eterna) y `Platitube`. Usan otros flujos y no las revisé;
si quieres que tengan su propio apartado, dime dónde guardan su estado.

## 8. Regla de mantenimiento
Al terminar cada video o cambio: actualizar §2 (calendario), la tabla del canal y sus pendientes, y `publicados` en `canales/<alias>.json`.


## Canal: Edsonxn (`edsonxn`, conectado el 30-sep-2026)
**Id:** `UCPiRBTFWvxEdqBlEY0os4PQ` · 1.660 suscriptores · 200 videos. Antes: tutoriales de Unity (2017-2023; un Short de 49 s = 79 mil vistas y 633 suscriptores).
Desde jun-2026: retro-gaming, hacks y misterios de internet (25 videos en 10 semanas, ~90 vistas por video, retención 30-43 %). Métricas: `canales/metricas/edsonxn_2026-09-30.json`.
**Decisión (30-sep):** nuevo enfoque = misterios y leyendas del internet y los videojuegos en estilo **documental de misterio**, voz **Faraon**, 1 largo (5-8 min) por semana + Short vertical.
**Primer video:** `videos/polybius` (Polybius, 52 frases / 718 palabras). Voz en cola (esperaba a `independencia_mx`); imágenes de Commons en `imagenes/`; falta `tiempo`, `escenas.py` a medida, música (Lyria), sfx, render, miniatura IA y `youtube.json`.

## 9. Producción del 30-sep-2026: plan semanal y tres videos nuevos (en curso)
Plan acordado con el usuario: **1 video por semana por canal, de 5 a 8 minutos**; prueba de un largo de 10-12 min en Bitácora Perdida; Kuriox con Shorts. No pasar a 15 min sin datos de retención.
Estado real de YouTube verificado por API (`publishAt`): Sapiens y Cronopapel tienen su último video programado el mié 7-oct (Neandertales / Irán) → sin video desde el 14-oct; Bitácora Perdida: Teotihuacán programado sáb 3-oct 12:00 CDMX; Kuriox sin calendario.
| Video | Canal | Estilo | Estado (30-sep, noche) |
|---|---|---|---|
| `independencia_mx` «La Independencia de México, completa» (10:50, voz 9:53) | Bitácora Perdida | **Kurzgesagt** (rehecho: la 1.ª versión salió en boceto+guache por error; archivada en `boceto_v1/`) | guion y voz listos (CER 0), 18 escenas, música Lyria en 5 partes, SFX y mezcla (−14 LUFS) hechos; **renderizado, MASTER 494 MB, CER 0,0008, −14 LUFS, desfase 0, SUBIDO EN PRIVADO el 30-sep: https://youtu.be/f4Ipx5rLdmQ** (subtítulos cargados); falta miniatura IA (`prompt_miniatura.md`, luego `yt aplicar`) y que el usuario oiga «once años de guerra» (~0:11: Whisper lo oye «heredra») antes de programar. Meta: sáb 10-oct 12:00 CDMX |
| `historia_japon` «La historia de Japón en 5 minutos» (330 s) | Cronopapel | boceto + guache con mapa | subido en privado: https://youtu.be/EI0c27EY89E con miniatura IA y .srt |
| `historia_egipto` «La historia de Egipto en 5 minutos» (340 s) | Cronopapel | boceto + guache con mapa | subido en privado: https://youtu.be/3V_C7ZEj5is con miniatura IA y .srt (QA: 0.0ms desync, CER 0.0015) |
| `un_dia_30mil` «Un día en la vida hace 30.000 años» | Sapiens con Wifi | doodle | guion y 9 escenas a medida listas; `comprobar` pasa; **falta la voz** (en cola; la voz se detuvo a medias para que cupiera el render). Meta: mié 14-oct 14:00 CDMX |
Prompts de miniatura IA de los tres: `prompt_miniatura.md` en cada carpeta; `youtube.json` de Independencia ya con capítulos reales.
**Lecciones nuevas:** (1) con voz (Chatterbox ≈ 8 GB de commit) y render a la vez se agota la memoria virtual (60 GB) y el render va 5× más lento o falla: no los corras juntos; (2) `fab.py <v> voz --seeds ...` SIN `--solo` regenera esas semillas para TODAS las frases (370 tomas de más); (3) una frase que falla con 4 semillas nuevas se reescribe (se quitó «hondas» y se acortó la última frase); (4) comandos de consola de >8 KB fallan: escribir archivos con Write; (5) `_tl_prov.py` + `_hoja.py`/`_esc.sh` permiten montar y revisar todas las escenas antes de tener la voz.
