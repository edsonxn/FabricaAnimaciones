# Los 15 enemigos ocultos de Fallout — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: radio_yermo (3.er video) · hueco mié 25-nov-2026 09:15 CDMX (ciclo 3 d, 09:15 = el de Tamriel)
- estilo: secuencia_yt (receta de Tamriel; regla de oro `videos/tes_secretos_40/`) · kit `nucleo/mg_fo.py` · voz el Profeta + filtro radio modo B (`VOZ_FX`, como `videos/fo_nunca_f4/guion.py`) · OST oficial de cada juego → doc: docs/estilo_secuencia_yt.md § Radio Yermo
- etapa: SUBIDO f2zKynItV6U (privado, programado mié 25-nov 09:16 CDMX = 15:16Z) · MASTER `salida/fo_enemigos_ocultos_MASTER.mp4` 15:23 1080p, −14 LUFS, desfase 0 ms; miniatura y .srt cargados
- siguiente: nada pendiente; `fab.py fo_enemigos_ocultos limpiar` cuando él apruebe el video. Medir ≈ 2-dic.

## Sesiones («continúa el video fo_enemigos_ocultos» retoma aquí · protocolo docs/sesiones.md)
- alias: enemigos ocultos de Fallout · UNA sesión directo al MASTER
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo hasta MASTER subido y programado | ✅ 23-nov | una sola sesión; 86 → 88 % semanal |

## Decisiones (23-nov-2026, Claude con datos; el usuario dio el OK en «buenos días»)
- Tema: 15 enemigos ocultos/raros de Fallout 3, New Vegas y 4 (5 por juego, cuenta atrás, el n.º 1 = el más bestia). Referencia: Wastelander «Hidden Fallout NV/3/4 Enemies» ×7,3 / ×6,5 / ×3,4 (canal de 13,8 mil); en español no existe la lista. Variable que cambia respecto a los anteriores: tema «secretos/ocultos» y tres juegos (vuelve a ~15 min como el 1.º).
- Duración ~15 min (≈ 2 300 palabras). Lista propia, sacada de la wiki (no copiar la de Wastelander). Clips solo del juego que se nombra.
- Comentarios: leer los NUEVOS de fo_nunca_f4 y fo_refugios_25 antes del guion (≤ 10 días).

## En curso
- 23-nov: carpeta creada (`nuevo --yt`). Investigación con 2 agentes → `_investigacion_A.md` (FO3+FNV), `_investigacion_B.md` (FO4).
- Comentarios (23-nov): radio_yermo 0 comentarios en 21 d → sin agradecimientos ni críticas; suscripción sin cifra.

## Checkpoint 23-nov ~13:50
- HECHO: investigación (`_investigacion_A.md` FO3+FNV, `_B.md` FO4; dudosos comprobados en la wiki: Gabe atómico, cigarrillo del mítico, 4 000 RF de Hundebarcos). `guion.py` (15 puestos: FO3 15/12/9/5 · FNV 14/11/8/6/3/1 · FO4 13/10/7/4/2; p7a con `post` 2,6 s para el silbido del OVNI → `ambiente_por` del clip del choque). OST (30 pistas FO3/FNV/FO4) y mapas (yermo_capital, mojave, commonwealth, la_isla + `_coords.json` de fo_refugios_25) COPIADOS; `armar_musica_ost.py` copiado (adaptar a puestos).
- VOZ lanzada ~13:50 (`_voz.log`, FIN al final). Luego `seleccionar` → `python nucleo/idioma_voz.py fo_enemigos_ocultos` → `tiempo` → `beats`.
- Descartados: Samuel (sin video), Keller y Nukalurk FO3 (video débil), geco de fuego, Grun, rey simiófago.

## Checkpoint 23-nov ~15:40
- VOZ: 102/102 (CER_MAX_POR_FRASE solo nombres; p13_5/p4_0/p5_5 seed 2; 6 frases reescritas por idioma: intro_4, p11_0, p12_0, p6_4, p8_0, p9_1). Silbido del OVNI QUITADO (p7a/p7_0 reescritas; sin sonidos nombrados).
- CLIPS: hojas de cuadros de las 44 fuentes (`previews/_ref_<id>.jpg`, `_refpNN.jpg`; 360p en E:\…\_ref) → tramos buenos en `_clips.py` → `busquedas.json` (107) → `bajar -j 4` (`_bajar.log`, FIN). Power armor HUD (9OKb, g7Bv, Vsu_) = juego, no mod. Evitar: 2KNS (marca de agua PS4Trophies), LIO9 (textos), E626 (panel de stream).
- PEGATINAS: 60 (`_pegatinas.py`, `pegatinas/_lista.md`, malas en `pegatinas/_malas/`).
- MAPAS: coords = marcadores del mapa interactivo de la wiki (`mapas/_wiki/marcadores.json`) en `mapas/_coords.json` (yermo_capital, mojave, commonwealth + DLC punto_lookout, big_mt, divisoria bajados de la wiki); hoja `previews/_coords_check.jpg` MIRADA. Sin mapa: Nuka-World e Isla (la base de la wiki no coincide).

## Checkpoint 23-nov ~17:30
- Medios: hojas `previews/medios_0N.jpg` MIRADAS; 17 clips rehechos (negro, subtítulos del juego en inglés, blanco, texto de youtuber «my voice sounds weird», pantalla de carga) → FIJOS en `_clips.py`.
- Chequeo: densidad MG 4,7/min (canal 4,2), mapas 0,7 (= canal), pegatinas subidas con EXTRA2 (+16). OCR restante = HUD del juego (nombres de enemigo, carteles de Ruzka, «Wheel up ZOOM», menús).
- fx hoja FINAL mirada 2 veces (8 hojas): arreglados anclas que caían en otro puesto («Cuatro mil#3», «Mil quinientos…#2», «Número uno#3»), pegatina encimada, foto pixelada → reliquia, logo de Tamriel (`tamriel_canal.png`, no Vault Boy).
- Miniatura: Flow (Nano Banana 2.1, proyecto «nov 23 - 08:06») v1 → `salida/miniatura.jpg`; v2 en `pantallas/_flow/`. `promesas.md`, `escenas.md`, `_youtube.py` escritos.

## Cierre 23-nov ~09:30 (hora del render)
- Render fx → ambiente → mezcla (−14 LUFS, pico −1,3 dBTP) → video → final: 1 050 MB. `verificar`: CER medio 0,52 %; 10 frases > 2 % = solo nombres (Rusca, Yaowai, BGMT, RAR, Dyson…). Promesas comprobadas en el MASTER (`previews/promesas_01/02.jpg`). Sin citas de audio (regla 10: ninguna frase manda escuchar).
- `yt subir … --publicar 2026-11-25T15:16:00Z` (a las 15:15:00 lo paró la separación de 72 h por 38 s). Registrado en `canales/radio_yermo.json` y BITACORA.

## Lecciones
- `_clips.py` reparte el `desde` sin mirar la duración del video fuente: dos clips salieron cortos (scene-034, 070-072). Recortar los tramos a `duración − clip` (o que `bajar` avise).
- Anclas de `efectos.py` con números («Cuatro mil», «Mil quinientos…», «número uno») casan en otros puestos («sesenta y cuatro, mil quinientos»; «el número uno» de la suscripción): usar `#N` y mirar la hoja FINAL.
- Los Let's Play de New Vegas/FO3 traen SUBTÍTULOS del juego en inglés en los diálogos (Think Tank, Megatón, Longfellow): el OCR solo caza los grandes; mirar la hoja de medios.
- Mapas: el mapa interactivo de la wiki (`Map:FO3 World Map`, `Map:FNVOWB World Map`…) da las coords de cada marcador sobre la MISMA textura → sin template matching (`mapas/_wiki/busca.py`); también trae los mapas de los DLC.

## Falta
- [x] TODO (23-nov). Antes: investigación · comentarios · guion · chequeo_yt · voz · seleccionar · idioma_voz · tiempo · beats · clips/medios · pegatinas · Flow (recreaciones + miniatura) · MG · mapas · OST · SFX · chequeo · fx hoja final · promesas · escenas · video · final · verificar · citas · subir 25-nov 09:15 · registrar · commit
