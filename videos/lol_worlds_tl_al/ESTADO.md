# Cómo Team Liquid ganó el Barón SIN PELEAR (Worlds 2026, TLAW vs AL partida 2) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: SIN CANAL (prueba de formato «análisis táctico de esports» pedida el 26-oct-2026; no se sube)
- estilo: secuencia_yt con UN clip + telestrador por código (nucleo/mg_tactica.py) → doc: docs/estilo_secuencia_yt.md
- etapa: verificado (MASTER 2:09 listo, esperando la revisión del usuario; no se sube: sin canal)
- siguiente: prueba cerrada. El video largo (22 min) sigue en videos/lol_worlds_2026/ (27-oct-2026); la miniatura se hizo aquí y se copió allá.

## Sesiones (plan de tramos · «continúa el video lol_worlds_tl_al» retoma aquí · protocolo docs/sesiones.md)
- alias: análisis LoL, prueba Worlds, Barón de Liquid
- vista previa: el MASTER entero (es corto, ~90 s) con audio completo
- leer al empezar: guion.py (docstring con los datos verificados), efectos.py
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | jugada + clip + guion + voz + telestrador + sonido + render | ✅ 26-oct | MASTER verificado; render en 6 tramos paralelos (22 min) |

## Decisiones (el usuario, 26-oct-2026)
- «tú elige la jugada»: Barón de TL a 41:46 (dragón 3 → oleada + TP → Barón). Narrador ElevenLabs a elección: JC (4XUsiqPDK4UACIM2BILe).
- análisis corto con pausas, flechas, rutas, elementos y mapa.

## En curso (checkpoint)
- **27-oct-2026: el usuario pide el video LARGO (~22 min) de la Worlds 2026 hasta hoy** (mejores jugadas analizadas, mejores
  jugadores y equipos, panorama para ponerse al día). Empezó por la MINIATURA: 4 de Flow en `miniatura/` (prompt y
  resultado en `prompt_miniatura.md`), esperando que elija. Datos al 27-oct (Wikipedia): play-in LA lo ganó Karmine Corp;
  suiza tras ronda 3: Gen.G y Dplus KIA 3-0; KOI, LYON, IG, TES, T1, BLG 2-1; HLE, G2, CFO, KC, LOS, TLAW 1-2; TSW y AL 0-3.
  Ronda 4: 28-oct KOI-T1 e IG-LYON; 29-oct KC-CFO y TES-BLG; 30-oct TLAW-LOS y HLE-G2; ronda 5 el 31-oct.
  Pendiente decidir: carpeta propia del video largo, canal, sesiones y vista previa. `salida/video_sin_audio.mp4` de las 07:12
  del 27-oct es un resto del render de la prueba (no es trabajo nuevo).
- clip bajado: medios/_fuente/jugada.mp4 (1080p30, 180 s = VOD 2833-3013 s = reloj 39:40-42:40). Cuadros de pausa elegidos:
  36 s (dragón, 40:16), 121 s (Barón 11 166 PV, 41:41), 124,5-127 s cámara lenta del castigo. Mapa: mapas/grieta.png (Data Dragon 16.21.1).

## Hecho
- guion.py (7 escenas, 16 frases); voz JC ElevenLabs turbo (343 créditos, 129,3 s con pausas; 6 frases aceptadas con
  CER/TAIL por frase: Whisper oye «varón»/«John»); 15 beats con medios/scene-NNN.jpg de relleno (el FX `video` tapa todo).
- kit nuevo nucleo/mg_tactica.py (pizarra + tablero 3D + chip + rebobinar); efectos.py con 4 pausas, 3 tableros, chips.
- música: biblioteca mods_ia_fusion__lyria_1 → audio/musica.wav; SFX de la biblioteca (sfx/, 9 sonidos) en PISTAS.

## Falta
- [x] fx (audio/fx.wav) · el Montaje del panel se DETUVO (un solo tramo de 129 s a 960 px, >18 min): no hace falta en la prueba
- [x] mezcla: −14,0 LUFS, −1,2 dBTP, voz 9,7 dB sobre música+SFX
- [x] video en 6 tramos paralelos (`video --tramo a-b --salida salida/par_k.mp4` + concat -c copy; 1 proceso iba a ~40 min) → final → verificar (CER 0,012; 0 ms de desfase) → aviso

## Lecciones de este video (solo lo no obvio)
- El motor SECUENCIA dibuja en UN proceso: con capas pesadas, partir en tramos `--tramo` en paralelo (6 → CPU al 97 %).
- Los resúmenes de YouTube se saltan tramos (40:28 → 41:42): para analizar una jugada, baja el VOD completo y ubica con el reloj.
