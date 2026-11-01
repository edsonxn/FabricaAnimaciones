# Sonic.exe: el CD maldito que nunca existió — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · primer video largo del canal de terror; ciclo 4 días, 18:00 CDMX (hueco: el primero libre; todos los videos viejos están en privado)
- estilo: terror CRT (`ESTILO_VISUAL = "documental"`) → docs/estilo_terror_crt.md · ejemplo a copiar: `videos/terror_ben_drowned/` · aquí la pantalla es un MONITOR CRT de PC (el relato es un CD-R en PC)
- etapa: CERRADO · aprobado por el usuario y PROGRAMADO mié 14-oct-2026 18:00 CDMX (15-oct 00:00 UTC) · https://youtu.be/RrucyrC_1e8 · 3:45, miniatura Flow, .srt · feedback «aprobado» anotado · `limpiar` hecho
- siguiente: nada en este video; tras publicarse, `actualizar-canales` y anotar métricas. Siguiente hueco del canal: lun 19-oct 18:00 CDMX (ciclo 5 días) → video nuevo con `python fab.py ideas cronicas_gaming`

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: sonic exe, sonic.exe, cartucho maldito de sonic, primer video terror
- vista previa: renderizada el 13-oct (`salida/sonic_exe_AVANCE.mp4`, 60 s, MUDA); el usuario la vio: «se ve bien». Pidió que las próximas vistas previas lleven audio completo (voz+música+SFX+mezcla)
- leer al empezar: este ESTADO.md + `docs/estilo_terror_crt.md` (+ `videos/terror_ben_drowned/escenas.py` solo para ver `pantalla(t)`/`cuadro(t)`)
- DECISIÓN (duración, 13-oct): el usuario eligió DEJARLO en 3:45 (nada inventado); no se añade escena de secuelas.
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | **Guion + voz + tiempo + clips + anclas** | ✅ 13-oct-2026 | fuentes: Wikipedia, KYM, Daily Dot, Dictionary.com (docstring de `guion.py`). `voz` 1 119 créditos; `comprobar` OK (7/7 escenas, 100 anclas en `anclas.py`). Promoción del kit a `nucleo/terror_*.py` MOVIDA al cierre del tramo 2 (cuando el kit ya tenga monitor PC y las pantallas nuevas) |
| 2 | **Escenas** (`escenas.py`, `pantalla(t)`, `cuadro(t)`), revisar cada ~3 s a tamaño completo; vista previa del primer minuto; **promover el kit a `nucleo/terror_*.py`** (doc + galería) | ✅ 13-oct-2026 (sin vista previa renderizada) | `escenas.py` completo, revisado cada ~3 s (2 pasadas de hoja). Arreglos: cierre 199-222 s con eventos por palabra, ruido tras «start» con 2 cuadros del demonio, sellos en la wiki «ELIMINADO», cursor en la ventana .exe. Kit en `nucleo/terror_pix.py`+`terror_crt.py`+`terror_pc.py` (cuadros idénticos antes/después). `fx_audio.py` sigue siendo la copia de Ben: reescribir en tramo 3 |
| 3 | **Cierre:** `fx_audio.py` → Lyria → `mezcla` → `video` → `final` → `verificar` → miniatura → `youtube.json`; subir en PRIVADO y proponer el hueco | ✅ 13-oct-2026 | 43 golpes/27 SFX, Lyria 2 tramos, mezcla −14,2 LUFS (pico −1,05 dBTP, voz +12 dB). Render 75 segmentos en 29 min (12 procesos). `verificar`: CER 1,4 % (solo nombres propios), desfase 0 ms. MASTER: sin negros salvo el corte final (222,2 s) ni congelados > 2 s. Miniatura Flow (`prompt_miniatura.md`). Subido privado RrucyrC_1e8; registrado en `canales/cronicas_gaming.json` y BITACORA. NO programado. Aviso de derechos de los extractos en la descripción |

## Plan de tomas (cada escena su propio mundo; plano secuencia; el gameplay SIEMPRE dentro del monitor)
- **cd** 0-30,9: cuarto de 2011, escritorio con torre beige + monitor CRT; sobre amarillo, CD-R sin carátula con «SONIC.EXE» a rotulador y la nota arrugada; `T_DISCO0/1` el disco viaja al lector. Pantalla nueva `pant_escritorio` (Windows 2000, carpeta, «Ejecutar»).
- **titulo** 30,9-58,3: `clips/titulo_real.mp4` (Sonic 1 nativo 320x224, ©SEGA 1991) y se corrompe con dibujo encima: cielo oscuro (a_cielo), emblema oxidado (a_oxid), «1991»→«666» (a_666), agua roja (a_roja). Pantalla nueva `pant_titulo(prog)`.
- **niveles** 58,3-85,7: `fuego` («cacería») → `demonio` (a_ojos, cara de ojos rojos) → `tails` (a_tails) → `knuckles` (a_knuc) → `eggman` (a_vill) → `hola` (niveles_2, «DO YOU WANT TO PLAY WITH ME?»); la corrupción sale del monitor al cuarto.
- **final** 85,7-106,3: monitor se apaga, el jugador se gira, peluche de Sonic (silueta nueva) sobre la cama con ojos que sangran (el rojo solo ahí); en «nada de esto ocurrió» (a_ocurrio) el monitor vuelve al escritorio normal.
- **autor** 106,3-150,9: pantallas dibujadas `pant_wiki` (Creepypasta Wiki, «9 AGO 2011», JC-the-Hyena), captura retocada (antes/después con ventana de editor), ejecutable «.exe» (a_corres), rótulo amateur/tópicos.
- **legado** 150,9-195,4: tarjetas con fecha: GameJolt 2012 (MY5TCrimson), reproductor de YouTube sin logos (PewDiePie, solo texto), wiki «ELIMINADO · 14 ENE 2014» en rojo, blog furioso → «broma de internet».
- **cierre** 195,4-224,6: Ben Drowned (cartucho dibujado), pantalla de título esperando; en `a_start2` (221,5) algo entra detrás del jugador; corte a negro en `T_FIN` 222,2.
- Clips ya cortados (8 s, `clips/*.mp4`, créditos en `creditos_clips.json`): tails, fuego, knuckles, eggman, demonio, hola (KEVINUTX 4.0, juego de MY5TCrimson) y titulo_real (TheNawaf258). Los 6 primeros son 4:3 con marca de agua abajo: recortar ~3 % inferior.

## Hecho
- Guion verificado (ficción declarada en `autor_0`), voz ElevenLabs David, `tiempo`, clips con hoja de contacto, `anclas.py`, fórmula `canales/formula/cronicas_gaming.md`.

## Falta
- [x] revisado y aprobado (13-oct), programado, `limpiar`

## Cómo retomar (comandos)
```
python fab.py continuar sonic exe
python fab.py sonic_exe escena <id> t1 t2 ...        (hoja de prueba; MÍRALA)
```

## Archivos clave
- `guion.py`, `anclas.py`, `escenas.py` (hechos) · `fx_audio.py` (por reescribir, copia de Ben) · `_hoja.py` (hoja de cuadros: `python _hoja.py 0:224:6 --out g`) · `clips/` · kit en `nucleo/terror_*.py`

## Lecciones de este video (solo lo no obvio)
- Voz: ElevenLabs David (`0hh7H4ZVAtaGpm1VZyEN`, `eleven_v4`), `ref_david.mp3` copiado de Ben. «Sonic punto exe» en el texto sale bien y Whisper lo transcribe tal cual.
- **Es un CD-R en PC, no un cartucho.** El Short de referencia (×8,7) y el alias «cartucho maldito» son imprecisos: el título nuestro es «el CD maldito que nunca existió».
- WebFetch no abre Fandom (402): para el relato original se usó Wikipedia + KYM + Daily Dot + Dictionary.com; «I AM GOD» y métodos de muerte NO se usan (una sola fuente o fuente no fiable).
- Gameplay real: `yt-dlp -f 18/bv*[height<=480]` con `--extractor-args "youtube:player_client=android,web"` evitó un 403; mirar SIEMPRE la hoja de contacto: el primer intento de «Sonic.exe» tenía 2 s de ruido al inicio de `demonio` y el texto «HELLO…» solo aparece a ~2 s de `hola`.
- Escenas: el cierre (27 s en el mismo cuarto) pedía un evento por frase; páginas fijas > 6 s (wiki, .exe) llevan sellos/cursor; tras «start» el ruido NO cae a negro. Detalle en `docs/estilo_terror_crt.md` § «Variante monitor de PC».
- Sesión cortada por tokens: `continuar` avisó «trabajo sin registrar»; bastó py_compile + ffprobe de `audio/*.wav` para conciliar (SFX, Lyria y youtube.json ya estaban completos).
- Miniatura: el cuadro del video subido de niveles se quema; en Flow, Nano Banana 2.1 pinta el título con tilde a la primera (deletrearlo en el prompt). El navegador integrado puede no tener sesión de Google: pedirla al usuario.
- Referencia del nicho: «Sonic.exe: El Cartucho Maldito…» Short ×8,7 (Expedientes del Internet, 51 subs); «historia de terror de un juego» (Monblu ×123) y «leyendas de videojuegos» (×1,6).

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado (14-oct 18:00 CDMX) y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [x] HALLAZGOS documentados: `docs/estilo_terror_crt.md` § «Miniatura» y § «Variante monitor de PC»; `docs/publicacion.md` 8b
