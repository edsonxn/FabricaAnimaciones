# 62 curiosidades de los Reinos del Este que casi nadie conoce (World of Warcraft Classic → Forever) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · 31:17 con pantalla final · PROGRAMADO Dv0Q-bh4Quw para lun 19-oct-2026 11:00 CDMX (17:00 UTC), orden del usuario 18-oct
- estilo: secuencia_yt (gameplay de YouTube por beat + apoyos + 3 MG; SIN Overgear) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ TERMINADO y subido en privado (MASTER v2 revisado: hojas cada 6 s + blackdetect sin negros) · miniatura + .srt cargados
- siguiente: nada de producción; al publicarse (19-oct), registrar en canales/cronicas_warcraft.json y BITACORA; luego `limpiar`

## Sesiones (plan de tramos · «continúa el video curiosidades» retoma aquí · protocolo docs/sesiones.md)
- alias: curiosidades, reinos del este, curiosidades de reinos del este, video de 30 minutos
- vista previa: SÍ, primeros 3 min con audio completo (voz + Lyria + mezcla) antes de bajar el resto de clips (el usuario, 17-oct)
- leer al empezar: este ESTADO.md + `docs/estilo_secuencia_yt.md` (no hace falta el § Overgear)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación + guion (62 curiosidades) | ✅ 17/18-oct | 18 datos verificados en la web (fuentes en el docstring de `guion.py`); 5 183 palabras ≈ 30,5 min a 170 ppm; 266 frases, ninguna > 200 caracteres ni de ≤ 4 palabras; FONETICA con 146 entradas |
| 2 | voz Applio + seleccionar + tiempo + beats + busquedas.json + `LYRIA.tramos` | ✅ 18-oct | 268/268 tomas (94 con CER_MAX por nombres/cifras, 3 frases reescritas: «once» se leía en inglés); voz 1 659,7 s; video 1 856 s (30:56); 216 beats; 12 tramos Lyria |
| 3 | bajar 0:00-8:30 + apoyos → VISTA PREVIA en el Montaje del panel (el usuario, 18-oct: «no hace falta renderizar», ≥ 3 min listos) | ✅ 18-oct | beats 1-60 bajados y REVISADOS (32 rehechos en 4 vueltas: guías con recuadros/mapas, webcams, marcas de agua, benchmark, retail); 27 apoyos (intro-c48; Malown/R.O.I.D.S./Lothos como tarjeta porque Wowhead es-MX los traduce); `evitar_canales` con 6 canales sucios. Falta: opinión del usuario |
| 4 | bajar 61-216 + revisar hojas `medios` | ✅ 18-oct | 216/216; 89 rehechos en 6 vueltas (guías con fichas/mapas, webcams, MACHINIMA, «like & subscribe», WC2/WC3, cinemáticas de BfA); 2 fijados con `--url --desde` |
| 5 | apoyos + pegatinas + 3 MG de TODO el video | ✅ 18-oct | 10 hojas `fx_NN.jpg` revisadas; 4 clips rehechos (70 marca «Ice_Lighting Presents», 106 no era Karazhan → Paso de la Muerte, 161 guía de botín → pelea con Kazzak, 188 gráfico de Top 10 → Tierras Fantasma); monturas de ZG en UNA tarjeta y CLUCK! acortada (tarjetas encimadas) |
| 6 | música original de WoW (3-4 temas de zona con yt-dlp, SIN Lyria) → mezcla → render → final → revisión MASTER → miniatura → youtube.json → subir privado | ✅ 18-oct | 4 temas originales (Elwynn, taberna humana, Bosque del Ocaso, Tirisfal; `musica_wow.py`); a petición del usuario, antes del render: 9 PANTALLAS completas con imagen real + 14 pegatinas nuevas y ~20 grandes (efectos.py 217 capas, aprobado en el Montaje); MASTER v1 con 8 defectos de origen → 6 clips rehechos + `recorte_por` → MASTER v2 limpio; subido privado Dv0Q-bh4Quw |

## Decisiones del episodio (preguntadas al usuario el 17-oct-2026)
- **PEGATINAS (el usuario, 18-oct)**: todo personaje/objeto/prenda que nombre la voz = imagen real como pegatina, ADEMÁS de clips y tarjetas (`peg()` en efectos.py, imágenes de Wowpedia en `pegatinas/`; receta docs/estilo_secuencia_yt.md § PEGATINAS)
- duración total: ~30 min · 62 curiosidades en cuenta regresiva (n.º 1 = la menos conocida y más curiosa) · 6 sesiones
- orden: 62-59 rarísimas (Malown, Gahz'ranka, R.O.I.D.S., Barov) · 58-7 alternando poco conocida / popular · 6-1 rarísimas (aeródromo de Forjaz, Quel'Thalas, Aldea Piroleña, Aurius, CLUCK!, la Ashbringer en el Monasterio)
- enfoque: Reinos del Este de CLASSIC (como llegan a WoW Forever, 4-nov), con gancho a Forever; Cataclysm/Wrath solo para contrastar
- **SIN Overgear** (el usuario, 17-oct: «va sin overgear»): sin segmento, sin código, sin música promo
- **MÚSICA = bandas sonoras ORIGINALES de WoW, NO Lyria** (el usuario, 18-oct: «no uses lyria, usa música original de World of Warcraft en ytdlp, descarga los audios de zona, unas 3 o 4»): música de fondo DEL PROPIO JUEGO (el usuario, 18-oct): Bosque de Elwynn, Páramos de Poniente, la de las TABERNAS, y similar (Bosque del Ocaso, Tirisfal) — nada de remixes, covers ni épica de cinemáticas; solo audio, en `audio/`; crédito en `salida/creditos.txt`. Excepción a la regla global de Lyria SOLO para este video

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada en curso)

## Hecho
- `nuevo --yt` (17-oct) · guion.py completo (ESCENAS intro + c62…c01 + cierre; `LYRIA.escenas` con un ánimo por curiosidad; `tramos` vacío hasta tener la línea de tiempo)

## Cómo retomar (comandos)
```
python fab.py estado wow_curiosidades_reinos_este
python fab.py wow_curiosidades_reinos_este voz | seleccionar | tiempo | beats | busquedas
python fab.py wow_curiosidades_reinos_este bajar           (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py wow_curiosidades_reinos_este medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json` (de dónde sale cada clip), `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- Error de datos cazado al buscar pegatinas: la garganta de Myzrael (Drywhisker) es de KOBOLDS, no de gnolls → c57_1 regrabada + `reajustar` (mismos 216 beats, misma duración).
- **Wowhead es-MX traduce nombres que la voz dice en inglés**: Postmaster Malown = «Jefe de correos Gassol», R.O.I.D.S. = «IFRDHR».
  Si el guion usa el nombre inglés, tarjeta con ese nombre y los datos reales del tooltip (no `wowhead=`).
- Búsquedas con «Classic» traen muchas GUÍAS de mazmorra (Thraex: recuadros «Abilities/Rewards» de otro canal) y videos de
  «Lore Deep Dive»/benchmarks con FPS: para el 2.º intento, «<zona> no commentary» o un lugar concreto («Refuge Pointe Classic»).
- Para listas largas, la voz Applio del canal va a ~170 palabras/min (medido en clases_ocultas, pistas_futuro y tes_misiones): 30 min ≈ 5 100-5 300 palabras ≈ 80 palabras por curiosidad. El primer borrador salió de 7 700 (43 min) y hubo que recortar dos veces.
- **Dos tarjetas `x=.72` con < 2 s entre sí se enciman en el fundido** (monturas de ZG, CLUCK!/pienso): revisar en la salida de `fx --seco` los pares «imagen» que se solapan; fusionar en una tarjeta o acortar `dur`.
- MASTER v1: `blackdetect` + hojas cazaron 8 defectos DE ORIGEN que la revisión de medios no vio (negros, rectángulos, letterbox,
  viñeta de cómic). Rehechos 035/051/105/122/187/212 (122 fijado con `--url` del video del 121, Turtle WoW = servidor privado, fuera).
- Datos quitados por no poder verificarlos: Chromie en Andorhal, nivel de Stitches, «barra de vida compartida» de Los Siete (eso es del BRD del 20.º aniversario). «Young Lovers» parodia a los Hatfield-McCoy, no a Romeo y Julieta.

## Cierre (regla del 12-oct-2026)
- [x] subido en privado, miniatura, .srt y registrado (`canales/<alias>.json`, BITACORA) · [x] programado lun 19-oct 11:00 CDMX
- [x] miniatura cambiada el 19-oct a `salida/miniatura_v3_gallina_sinlogo.jpg` (la v1 «mucha carga visual»; UN protagonista, sin logo; prompts en prompt_miniatura.md)
- [x] HALLAZGOS documentados: docs/estilo_secuencia_yt.md (pantalla completa, pegatinas grandes, blackdetect del MASTER), plantilla_yt `pant()`
