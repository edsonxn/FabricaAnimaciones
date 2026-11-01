# Lo más PERTURBADOR que pasó DE VERDAD en World of Warcraft — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · meta: jue 29 o vie 30-oct-2026 09:00 CDMX (especial de Halloween; el canal se queda sin video el 21-oct)
- estilo: «grabado de peste» (xilografía animada en espacio 3D, danza macabra) + clips yt-dlp · doc docs/estilo_grabado_peste.md · kit nucleo/grabado.py + grabado_3d.py
- etapa: CERRADO 16-oct: MASTER 9:11 + .srt + miniatura; PROGRAMADO hoy vie 16-oct 11:00 CDMX (_-M5FqPQmdg, 17:00 UTC), fecha del usuario
- siguiente: nada; al aprobarlo, `python fab.py wow_tres_noches limpiar` (segmentos/ 656 MB); revisar métricas a los 7 días

## Pedido del usuario (15-oct): más WoW REAL — hecho en 0:00-3:00, seguir igual en todos los tramos
- Grabado se queda; PEGATINAS reales (`comun.peg`: 1 de cada 3 + 1-2 cerca) y elementos reales (`png/`, `comun.relieve`).

## Decisión del usuario (14-oct-2026) — excepción al estilo del canal (Warcraft normal = SECUENCIA YT + Applio)
- Tema: 3 noches REALES, de menos a más: Sangre Corrupta (2005) → plaga zombi a propósito de Blizzard (oct-2008, «hace 18 años»)
  → el funeral emboscado (2006, Serenity Now, Illidan; con respeto, sin el nombre de la jugadora). Hechos y DOI en el docstring de guion.py.
- Narrador ÚNICO: el **Ángel de la Resurrección** (de «tú»); giro: tu personaje sigue en la pantalla de selección. Voz ElevenLabs
  **Lily** `pFZP5JQG7iQjIQuC4Bku`, `eleven_v4` con corchetes; en mezcla `REVERB_VOZ` etérea. Sin Overgear. Lyria de terror (4 tramos).
- **Jumpscares** (el usuario): 4 al CIERRE de su escena (silencio + golpe + 6-8 cuadros; SIN estrobo): **2:56 Hakkar** (`humanos`),
  **5:50 necrófago** (`portal`), **7:19 emboscada** (`fila`), **8:45 el Ángel** (`promesa`); detalle en `SUSTOS` de guion.py.
- Acento por acto: sangre / plaga / helado. Clips reales (≤ 8 s, crédito) SIEMPRE en «recuerdos»; nada quieto > 2 s.

## Línea de tiempo (14-oct, `tiempo`, 70 BPM) — 17 escenas, 8:50
Acto 1 Sangre Corrupta: gancho 0:00 · zulgurub 0:41 · mascotas 1:15 · ciudades 1:36 · humanos 2:14 · cdc 2:58 ·
Acto 2 Plaga: cajas 3:39 · reloj 4:10 · caen 4:41 · portal 5:19 · cura 5:50 · Acto 3 Funeral: funeral 6:17 · fila 6:58 ·
emboscada 7:19 · video 7:43 · Giro: promesa 8:07 · cierre 8:45-8:50.
Clips: 13 en `clips/_crudos/` con escena destino y crédito en `clips/creditos_clips.json`; el tramo se elige al montar.

## Sesiones (plan de tramos · «continúa el video tres noches» retoma aquí · protocolo docs/sesiones.md)
- alias: tres noches, video de terror de Warcraft, Halloween Warcraft, Ángel de la Resurrección
- vista previa: HECHA (tramo 4) y REHECHA con pegatinas (tramo 5, 15-oct, audio completo). 8 sesiones aprobadas.
- leer al empezar: este ESTADO.md; desde la sesión 3, docs/estilo_grabado_peste.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | decisión de tema/estilo/narrador + muestras de voz | ✅ 14-oct | elegido todo lo recomendado; voz de mujer y jumpscares por el usuario |
| 2 | guion + datos verificados + lista de clips yt-dlp + voz + tiempo | ✅ 14-oct | 1 025 palabras, 71 frases, CER ok; 8:50; 13 clips bajados |
| 3 | kit `nucleo/grabado.py` + `docs/estilo_grabado_peste.md` + cuadros de prueba del look (el usuario aprueba) | ✅ 14-oct | kit `grabado.py` + `grabado_3d.py`, `look.py` (3 láminas 3D), `previews/muestra_look.mp4`, doc, galería. **Look APROBADO por el usuario (14-oct, sin ajustes)** |
| 4 | escenas 0:00-2:58 (gancho → susto de Hakkar) + Lyria/SFX/mezcla de ese tramo + vista previa | ✅ 15-oct | `salida/wow_tres_noches_AVANCE.mp4` (3:00, audio completo); 60 segmentos; susto con silencio real + golpe al frente |
| 5 | pegatinas/PNG reales de WoW vanilla en el kit (`grabado_3d`) + hoja de prueba al usuario + aplicarlas a 0:00-3:00 + re-render del avance | ✅ 15-oct | `wow_png.py` (24 renders) + `G3.pegatina` + cobras/relieves del tráiler; look aprobado; AVANCE rehecho (1 h 53 min + 8 min) |
| 6 | escenas 2:58-5:50 (cdc + plaga zombi → susto del necrófago), ya con pegatinas | ✅ 15-oct | anclas 2:58-8:50; 18 PNJ nuevos; `decor_t6.py` (gabinete, Bahía del Botín, calle de Ventormenta, Villadorada, torre + susto2) + `fig2.py`; `escenas.py` con sustos generalizados (idéntico < 2:58,29) |
| 7 | escenas 5:50-8:50 (cura + funeral + giro, sustos 7:19 y 8:45), ya con pegatinas | ✅ 15-oct | `decor_t7.py` (amanecer Alba Argenta, aguas termales, cementerio video/promesa, plaza, selección, sustos 3-4) |
| 8 | cierre: SFX → mezcla → render → final → verificar → miniatura (Flow, ingredientes reales) → youtube.json | ✅ 16-oct | render 13 h 13 min (118 segmentos, MUCHO más lento que lo estimado); final + verificar (CER 0,27 %) ✔; subido privado _-M5FqPQmdg · 31 SFX nuevos (1 098 créditos) + mezcla −14,3 LUFS, 4 silencios de susto ≥ 0,83 s ✔; segmentos 6-58 conservados; RENDER COMPLETO lanzado 15-oct (`fab.py … video`); falta final, verificar, hoja del MASTER, miniatura, youtube.json, subir |

## Hecho
- 14-oct: guion + DOI (Crossref) + voz Lily + `tiempo` + 13 clips; escenas 0:00-3:00 (`escenas.py`, `decor_*.py`, `fig.py`,
  `comun.py`, `anclas.py`; hoja `python _prueba.py t1 t2`); música COMPLETA `audio/musica.wav` (Lyria a mano); 33 SFX.
- 15-oct: mezcla −14,3 LUFS, susto 2:56,4 (silencio 0,83 s + golpe). Tramo 5: pegatinas reales en las 6 partes y
  `salida/wow_tres_noches_AVANCE.mp4` rehecho (mismo `final.wav`); sin congelados; 2:57,5-3:00 negro = `cdc` (tramo 6).

## Falta
- [x] voz · [x] guion · [x] kit + doc de estilo + CLAUDE.md + galeria.json · [x] look aprobado · [ ] escenas (1/3) · [x] música + SFX tramo 1 · [ ] render
- [x] `final` anexó la pantalla final del canal Warcraft (530,6 s → 551,2 s)

## Lecciones de este video (solo lo no obvio)
- Lily pronuncia la z como «th»: es su acento, no la toma (CER_MAX_POR_FRASE).
- Los sustos se ponen al FINAL de una escena: el `post` de la escena da el silencio previo sin trucos en la voz.
- Golpe del susto en fx.wav = inaudible: va en `audio/fx_sustos.wav` + `sustos.json` y `mezcla` apaga todo entre apagón y
  golpe. Tramos 6-7: AÑADIR sus (apagón, golpe) a `SUSTOS_T` de fx_audio.py y su pista «susto».
- Tocar guion.py tras un render deja obsoletos los segmentos anotados (el siguiente `video` los borraría): `conservar`.
- Segmentos SIN anotar en la caché (0-13 del 14-oct) no se depuran al cambiar el código: borrarlos a mano.
- Tramos 6-7 (15-oct): el decorado nuevo arranca en 2:58,34 (`TR_ESTUDIO`) para que los segmentos 0-58 del avance sigan
  valiendo (`conservar`); los SFX de susto nuevos se llaman `susto_*` y van a `fx_sustos.wav`. Miniatura: Flow con 3
  ingredientes reales (`miniatura/refs/`), variante 1 (la 2 redibujó al Ángel con cuernos). Errores de montaje en el doc de estilo.

## Cierre (regla del 12-oct-2026)
- [x] subido + miniatura + registrado (`canales/cronicas_warcraft.json`, BITACORA) · [x] programado 16-oct 11:00 CDMX (el usuario) · [x] hallazgos al doc de estilo
