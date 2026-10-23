# Los 12 objetos más RAROS de WoW Vanilla que podrían volver en WoW Forever — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · ~14 min · hueco mié 28-oct-2026 09:00 CDMX (15:00 UTC; `canales --actualizar` del 22-oct)
- estilo: secuencia_yt (gameplay por beat + apoyos + pegatinas + pantallas + MG nuevos con MAPAS REALES; SIN Overgear) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ SUBIDO y PROGRAMADO mié 28-oct-2026 09:00 CDMX (2xO3Wf1B4XQ) · miniatura + .srt
- siguiente: Studio > Monetización (anuncios + cuestionario) cuando procese la SD; medir a los 7 días (4-nov, día de Forever) contra Kalimdor; luego `limpiar`

## Sesiones (plan de tramos · «continúa el video objetos raros» retoma aquí · protocolo docs/sesiones.md)
- alias: objetos raros, armas raras, objetos raros vanilla
- vista previa: NO (el usuario, 22-oct: todo de corrido); aviso por voz al subir
- leer al empezar: este ESTADO.md + `docs/estilo_secuencia_yt.md` (sin § Overgear) + de modelo `videos/wow_curiosidades_kalimdor/`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación + guion (12 objetos, ~2 300 palabras) | ✅ 22-oct | 2 470 palabras; investigación con fuentes en `videos/_investigacion_wow_raros.md`; docstring de guion.py |
| 2 | voz Applio + seleccionar + tiempo + beats + busquedas.json | ✅ 22-oct | voz 108/108 (48 con CER_MAX por nombres/cifras; «doce» se oía «dos» → «una docena»); video 818 s + 20,6 |
| 3 | bajar clips + revisar hojas `medios` | ✅ 23-oct | 95/95; 42 rehechos en 4 vueltas (webcams, logos TOSAN/Twitch/«Crusades fed», «1% Drop chance», guías con mapa, retail, fan-art, Conquista del Invierno por Cuna); 25 canales vetados |
| 4 | apoyos + pegatinas + pantallas + MAPAS con ruta (`mg_wow.ruta`) + MG nuevos (`fx hoja`) | ✅ 23-oct | 90 FX: 9 mapas con FOTO en cada paso (pedido del usuario), forja ×2, sorteo, contadores, 31 apoyos, 3 pantallas |
| 5 | música original de WoW → mezcla → render → final → rigor MASTER → miniatura → subir y programar | ✅ 23-oct | -14,08 LUFS; MASTER 13:59 (0 negros); v1 con recuadro de streamer en 0:24 → clip 004 rehecho; subido 2xO3Wf1B4XQ |

## Decisiones del episodio (preguntadas al usuario el 22-oct-2026)
- tema (pedido por el usuario): armas/objetos RAROS de Vanilla que tal vez veamos en WoW Forever (4-nov-2026); ≥ 12 → 12
- orden: cuenta regresiva de menos a más raro; la n.º 1 la más rara
- **MAPAS REALES del juego** (el usuario): dónde se obtiene y rutas de las cadenas de misiones → MG nuevo `mg_wow.ruta`
- SIN Overgear · música ORIGINAL de WoW (no Lyria) · sin vista previa, todo de corrido
- referencia de fuera: Kadrath ×4,0 «8 Ítems de WoW con EFECTOS SECRETOS» (eje «oculto/raro»)

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada en curso)

## Hecho
- `nuevo --yt` (22-oct) · `canales --actualizar` (22-oct, cuota de la API agotada: datos del registro): antes que Warcraft se quedan sin video Cuerpo en Neón (dom 25) y Tamriel (lun 26)

## Cómo retomar (comandos)
```
python fab.py estado wow_objetos_raros
python fab.py wow_objetos_raros voz | seleccionar | tiempo | beats | busquedas
python fab.py wow_objetos_raros bajar           (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py wow_objetos_raros medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `mapas/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- **Fotos en el mapa** (el usuario, 23-oct): en cada paso de la ruta, la foto real de lo que se nombra → regla global (CLAUDE.md, mg_mapa y mg_wow.ruta).
- Un ancla repetida en el guion («con Anacronos» sale en Atiesh y en el cetro) dispara el pin antes de tiempo: usar `#2`.
- Applio dice «doce» y Whisper oye «dos»: «una docena» lo evita; nombres ingleses en FONETICA siguen dando CER 0,02-0,16 (aceptar por hyp).
- `yt-dlp` puede colgarse (timeout 300 s) y tumbar `bajar`: relanzar `bajar` completa lo que falta.
- La rejilla de `sorteo` con casillas del color del panel no se ve: las vacías tienen que contrastar.
- El último tramo del Montaje (`fx`) falló al regenerar; no afecta al MASTER (repetir `fx montaje` si el panel lo pide).

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO mié 28-oct 09:00 CDMX (2xO3Wf1B4XQ), miniatura y .srt; registrado en `canales/cronicas_warcraft.json` y BITACORA
- [x] HALLAZGOS documentados: docs/estilo_secuencia_yt.md (fotos en el mapa, mg_wow.ruta/forja/sorteo), reglas_globales_completas, CLAUDE.md, docs de Kurzgesagt y Cronopapel
- [ ] Monetización en Studio
