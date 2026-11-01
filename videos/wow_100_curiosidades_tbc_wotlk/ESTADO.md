# 100 curiosidades, secretos y easter eggs de Burning Crusade y Wrath que puedes ir a ver — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · 51:12 + pantalla final (3 071,9 s; el usuario pidió ≥ 45) · PROGRAMADO sáb 31-oct-2026 09:00 CDMX (15:00 UTC), privado hasta entonces
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + pantallas + MAPAS CON RUTA por zona + MG nuevos; música = OST del juego) → doc: docs/estilo_secuencia_yt.md
- etapa: guion ✅ · voz ✅ · 357 clips ✅ · efectos ✅ (Terrallende + Rasganorte, 18 hojas `fx` revisadas) · OST por zona + sonido original + mezcla ✅ · MASTER ✅ (51:32 con pantalla final) · subido y programado ✅ (27-oct)
- siguiente: que el usuario lo vea antes del sáb 31-oct; Studio (video relacionado de Shorts + monetización, memoria «studio-navegador»); resultado a 7 días en `canales/formula/cronicas_warcraft.md` (las partes `parte1_hasta1722.mp4` y `tramo_1706_3071.mp4` se borraron el 29-oct para liberar C:; si hay que corregir un tramo, re-render con `--tramo`)

## Sesiones (plan de tramos · «continúa el video 100 curiosidades» retoma aquí · protocolo docs/sesiones.md)
- alias: 100 curiosidades, cien curiosidades, tbc wotlk, terrallende y rasganorte, curiosidades de burning crusade, video de 45 minutos
- vista previa: NO (el usuario, 23-oct: «hazlo entero»); revisión con el rigor de siempre y aviso al subir
- leer al empezar: este ESTADO.md + `docs/estilo_secuencia_yt.md` §§ PEGATINAS, MG NUEVOS y MAPAS REALES CON RUTA · de modelo `videos/wow_curiosidades_reinos_este/` (31 min, 216 beats) y `videos/wow_curiosidades_kalimdor/` (`musica_wow.py`)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación + guion (100 curiosidades, ≥ 45 min) | ✅ 23-oct | 8 877 palabras ≈ 53 min; 14 datos verificados en la web (docstring de `guion.py`); FONETICA 231 entradas; orden geográfico 100→1 (Terrallende → Quel'Thalas/islas/Karazhan/Cavernas → Rasganorte), n.º 1 = Bridenbrad |
| 2 | nombres es-MX → voz Applio → seleccionar → tiempo → beats → busquedas.json | ✅ 24-oct | es-MX con la AreaTable esMX de wago.tools (25 nombres corregidos: Lodo Muerto, Bajo Arrabal, Gelidar, Nafsavar, Fauceparda, Puerta de Cólera…) + tooltips de Wowhead (Rondador de abajo, Caminante del Destino, Melenablanca, Manacapón); 411/411 tomas (113 con CER_MAX propio por cifras/nombres; 2 frases reescritas); voz 2 783 s; video 3 071,9 s; 357 beats; busquedas.json generado por `_busquedas_gen.py` (tabla por curiosidad + respaldo de zona). `LYRIA.tramos` pendiente para el tramo 8 |
| 3-5 | `bajar` 357 beats + 18 hojas `medios` revisadas + 2 vueltas de rehechos | ✅ 24-oct | 109 rehechos en la 1.ª vuelta (31 %: webcams, paneles de misión, mapas abiertos, marcas, Hearthstone, WC3, cinemáticas de otras expansiones) y 29 en la 2.ª con «<zona> Meisio»; incidente del `--rehacer` sin ids (ver Lecciones) resuelto restaurando desde `_respaldo`; `salida/creditos.txt` con 282 videos |
| 6 | efectos de Terrallende: MAPAS CON RUTA (un mapa de Wowhead por bloque de zona, con FOTO real en cada parada: `mapa()`, `ZONA_DE`), pegatinas, pantallas, 2-4 MG nuevos (p. ej. «los 5 héroes de la expedición», «las 3 sucursales de Gurgthock», «los dioses sacrificados de Zul'Drak», «las 3 apariciones de Harrison») | ✅ 24-oct | 84 pegatinas de Wowpedia (mosaico revisado, 18 cambiadas: Illidan era Cenarius, Medivh un cuervo…); mapa general de Terrallende a pantalla en la intro + 42 ventanas por parada con foto + la Cicatriz Muerta a pantalla; MG nuevos `paradero` (c100), `simon` (c073), `franquicia` (c079) en mg_wow; `traza` nuevo en mg_mapa; 9 hojas `fx` revisadas y clips 23 (título de YouTube) y 169 (webcam) rehechos |
| 7 | efectos de Rasganorte + hojas `fx` revisadas (choques de pegatinas/tarjetas) | ✅ 27-oct | efectos.py escrito el 26-oct (mapa general + 40 paradas + ~85 pegatinas + 30 tarjetas + MG altares/apariciones/paradero Barbabronce/cadena Bridenbrad); `apoyos` + `fx hoja` (18 hojas) revisadas el 27-oct sin bloqueos (solo rótulos de mapa cortados en el borde izquierdo: «oblado Taunka'le», «uerto del Embate», menor) |
| 8 | OST original por zona (yt-dlp «- Topic», ~21 temas → `musica_wow.py` por `ZONA_DE`) → mezcla → render (53 min: horas; `avisar`) → final → rigor MASTER (hojas + blackdetect) → miniatura → subir privado y PROGRAMAR sáb 31-oct 09:00 CDMX → registrar → `biblioteca catalogar` → commit | ✅ 27-oct | `LYRIA.tramos` = 30 tramos por zona (21 temas); SONIDO ORIGINAL en 10 beats (`ambiente_por`; E.T.C. 059-061, Garrosh 181, Gymer 257, Algalon 302, HoR 348-349, Fel Reaver 014, Caminante 132) con `_sonido_original.py alinear` (misma imagen aprobada + su audio); OST −14 dB ahí (`musica_wow.py aparta`); mezcla −14,1 LUFS / −1,46 dBTP / voz 14,6 dB; `audio/`, `segmentos/`, `salida/` pasados a C: (E: con Ntfs 55 el 26-oct 20:23); 1.er render cortado al 56 % por E: (USB desconectado 15:27) → `medios/` a C:, `--tramo 1706.834-3071.875` (19 min) y unión por cuadros (92 156, PSNR ok); `verificar` CER 1,5 %; rigor: 2 fundidos a negro de 0,7 s en portales (31:16, 43:33, del propio clip) y 4 «congelados» = mapas con ruta (no bloquean); clips 134/137 ya de WoW; miniatura Flow (Rey Exánime del tráiler); subido privado programado sáb 31-oct 09:00 CDMX |

## Decisiones del episodio (el usuario, 23-oct-2026: «sin overgear está bien, 53 minutos, hazlo entero»)
- tema (el usuario): 100 curiosidades de TBC + WotLK visitables/comprobables en el mapa, ≥ 45 min; «agrégale Easter eggs y secretos»
- orden (Claude): cuenta regresiva recorriendo las zonas en orden geográfico, para que los mapas con ruta cuenten un viaje; el usuario puede pedir el orden rarísimas/populares de Reinos del Este
- **SIN Overgear** (escena borrada antes de la voz) · **53 min aceptados** · **sin vista previa**
- **Música: OST ORIGINAL de WoW** por zona (regla del canal 23-oct), NUNCA Lyria · **Mapas reales con ruta** en cada bloque de zona (regla 23-oct) con foto real de lo que la voz nombra

## Hecho
- `nuevo --yt` (23-oct) · `canales --actualizar` (23-oct): antes que Warcraft (31-oct) se quedan sin video Crónicas del gaming (27), Sapiens (28), Cuerpo en Neón (29) y LogIA (30)
- guion.py completo: intro + c100…c001 + cierre; `ZONA_DE` (zona de cada curiosidad: música y mapas) y `_BLOQUES`
- adelantado para los tramos 6-8: `mapas/` (25 mapas de Wowhead es-ES, 1022x668; Dalaran no existe en Wowhead), `audio/wow/` (21 temas OST por zona, `_temas.json`) y `musica_wow.py` (tema por zona según `ZONA_DE`)
- `nucleo/secuencia_yt.py`: `--rehacer` sin ids exige `--todos`; carpeta temporal alternativa si un ffmpeg colgado retiene la anterior
- `nucleo/limpiar_publicados.py`: salta entradas NTFS rotas (E: con errores 55 el 23-oct)
- `nucleo/mezcla.py` en float32 + pico verdadero por trozos (51 min no cabían en RAM) · `_sonido_original.py` (alinear, creditos, habla, nivel) · `youtube_gen.py` (23 capítulos por zona)

## Cómo retomar (comandos)
```
python fab.py estado wow_100_curiosidades_tbc_wotlk
python fab.py wow_100_curiosidades_tbc_wotlk voz | seleccionar | tiempo | beats | busquedas
python fab.py wow_100_curiosidades_tbc_wotlk bajar           (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py wow_100_curiosidades_tbc_wotlk medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py` (docstring: datos verificados y ⚠ nombres es-MX por confirmar), luego `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `mapas/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- **NUNCA un bucle `while read … | python …` sin `< /dev/null`**: el primer python se comió el heredoc y el siguiente `bajar --rehacer` corrió SIN ids → rehizo los 357 beats 1,5 h hasta llenar el disco y dejó fuentes.json con 7 entradas. Arreglo: `bajar --rehacer` sin ids ahora exige `--todos`; los clips aprobados se restauraron desde `medios/_respaldo` (sufijo = hora de la vuelta) y fuentes.json se reconstruyó con las líneas «ok» de los logs (`_reparar_fuentes.py`).
- Un ffmpeg colgado de `bajar` retiene `medios/_tmp_scene-NNN/c.mp4` y tira la vuelta siguiente (PermissionError): `_bajar_tramo` ahora usa otra carpeta temporal; matar ffmpeg viejos con PowerShell `Stop-Process` (taskkill /PID se rompe en Git Bash por el `/`).
- Mosaico propio de los rehechos (`_mosaico.py`, 5 columnas, un cuadro a los 3 s) en vez de regenerar las 18 hojas: 108 clips en 2 imágenes.
- `mapas/terrallende.jpg` y `rasganorte.jpg` eran Tierras Inhóspitas y Las Tierras Devastadas (ids 3 y 4 de Wowhead = zonas): cambiados por `-2` y `-5` el 24-oct.
- Al leer coordenadas en Wowpedia salieron 4 dudas de GUION (la voz ya está hecha; no se tocó, los mapas evitan contradecirla): Haris Pilton está en el Bajo Arrabal (75.6, 31.6) y la voz la pone en la Taberna del Fin del Mundo (en el mapa, «Taberna» en esas coords); Zephyr figura en la Taberna, no «junto a A'dal» (c083 sin mapa de Shattrath); Culuthas figura en las Ruinas de Farahlon, no en el cráter de Ultris (c068: el mapa marca solo la forja); la Encrucijada de Kessel está en Bruma de Sangre y la voz dice Bruma Azur (c055 sin mapa).
- **Sonido original sin cambiar la imagen aprobada**: `bajar --rehacer` con `+ba` mueve el keyframe y el clip cambia (salieron clips de 1 cuadro); `_sonido_original.py alinear` busca por imagen el instante del aprobado y le pega su audio (12/12). 4 descartados: 2 con narrador (080, 247) y 2 mudos (155, 261).
- **Clips de Heroes of the Storm** colados (134, 137: «Maiev HoTS») que no vio la revisión de hojas: en Warcraft, mirar el TÍTULO de `fuentes.json` de los clips con nombres de héroe (HoTS/Hearthstone) además de la imagen.
- **Render cortado por E:** (USB desconectado 27-oct 15:27, «Clip vacío o ilegible»): `medios/` a C: antes de un render largo; se retomó por `--tramo` + unión por cuadros (receta en `docs/estilo_secuencia_yt.md` § «Render cortado a mitad»).
- Navegador integrado: bloquea `http://127.0.0.1` (ERR_BLOCKED_BY_CLIENT) → el ingrediente de la miniatura se tomó de `i.ytimg.com` (CORS abierto; `prompt_miniatura.md`).
- Revisión de choques sin render: `_choques.py` (cajas por FX, tiempo × posición) antes de `fx hoja`; cazó Thrall bajo Garrosh grande, Mogor bajo el MG y el mapa de Maiev bajo su tarjeta.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA) — 27-oct
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (`docs/estilo_secuencia_yt.md`: sonido original con `alinear`, render cortado; `docs/publicacion.md` 8b: ingredientes desde el navegador integrado)
- [ ] `canales/formula/cronicas_warcraft.md` con el resultado a 7 días (≈ 7-nov)
