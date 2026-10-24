# 100 curiosidades, secretos y easter eggs de Burning Crusade y Wrath que puedes ir a ver — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · 51:12 + pantalla final (3 071,9 s; el usuario pidió ≥ 45) · hueco sáb 31-oct-2026 09:00 CDMX (15:00 UTC; `canales --actualizar` del 23-oct)
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + pantallas + MAPAS CON RUTA por zona + MG nuevos; música = OST del juego) → doc: docs/estilo_secuencia_yt.md
- etapa: guion ✅ · voz ✅ 411/411 · beats ✅ 357 · CLIPS ✅ 357/357 revisados (2 vueltas) · créditos ✅ · siguen los EFECTOS (tramo 6)
- siguiente: tramo 6 = efectos.py de Terrallende: mapas con ruta por bloque (`mapas/`, `ZONA_DE`, rejilla con `python nucleo/mg_mapa.py rejilla`), pegatinas, pantallas, 2-4 MG nuevos → `fx hoja`

## Sesiones (plan de tramos · «continúa el video 100 curiosidades» retoma aquí · protocolo docs/sesiones.md)
- alias: 100 curiosidades, cien curiosidades, tbc wotlk, terrallende y rasganorte, curiosidades de burning crusade, video de 45 minutos
- vista previa: NO (el usuario, 23-oct: «hazlo entero»); revisión con el rigor de siempre y aviso al subir
- leer al empezar: este ESTADO.md + `docs/estilo_secuencia_yt.md` §§ PEGATINAS, MG NUEVOS y MAPAS REALES CON RUTA · de modelo `videos/wow_curiosidades_reinos_este/` (31 min, 216 beats) y `videos/wow_curiosidades_kalimdor/` (`musica_wow.py`)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación + guion (100 curiosidades, ≥ 45 min) | ✅ 23-oct | 8 877 palabras ≈ 53 min; 14 datos verificados en la web (docstring de `guion.py`); FONETICA 231 entradas; orden geográfico 100→1 (Terrallende → Quel'Thalas/islas/Karazhan/Cavernas → Rasganorte), n.º 1 = Bridenbrad |
| 2 | nombres es-MX → voz Applio → seleccionar → tiempo → beats → busquedas.json | ✅ 24-oct | es-MX con la AreaTable esMX de wago.tools (25 nombres corregidos: Lodo Muerto, Bajo Arrabal, Gelidar, Nafsavar, Fauceparda, Puerta de Cólera…) + tooltips de Wowhead (Rondador de abajo, Caminante del Destino, Melenablanca, Manacapón); 411/411 tomas (113 con CER_MAX propio por cifras/nombres; 2 frases reescritas); voz 2 783 s; video 3 071,9 s; 357 beats; busquedas.json generado por `_busquedas_gen.py` (tabla por curiosidad + respaldo de zona). `LYRIA.tramos` pendiente para el tramo 8 |
| 3-5 | `bajar` 357 beats + 18 hojas `medios` revisadas + 2 vueltas de rehechos | ✅ 24-oct | 109 rehechos en la 1.ª vuelta (31 %: webcams, paneles de misión, mapas abiertos, marcas, Hearthstone, WC3, cinemáticas de otras expansiones) y 29 en la 2.ª con «<zona> Meisio»; incidente del `--rehacer` sin ids (ver Lecciones) resuelto restaurando desde `_respaldo`; `salida/creditos.txt` con 282 videos |
| 6 | efectos de Terrallende: MAPAS CON RUTA (un mapa de Wowhead por bloque de zona, con FOTO real en cada parada: `mapa()`, `ZONA_DE`), pegatinas, pantallas, 2-4 MG nuevos (p. ej. «los 5 héroes de la expedición», «las 3 sucursales de Gurgthock», «los dioses sacrificados de Zul'Drak», «las 3 apariciones de Harrison») | pendiente | |
| 7 | efectos de Rasganorte + hojas `fx` revisadas (choques de pegatinas/tarjetas) | pendiente | |
| 8 | OST original por zona (yt-dlp «- Topic», ~21 temas → `musica_wow.py` por `ZONA_DE`) → mezcla → render (53 min: horas; `avisar`) → final → rigor MASTER (hojas + blackdetect) → miniatura → subir privado y PROGRAMAR sáb 31-oct 09:00 CDMX → registrar → `biblioteca catalogar` → commit | pendiente | |

## Decisiones del episodio (el usuario, 23-oct-2026: «sin overgear está bien, 53 minutos, hazlo entero»)
- tema (el usuario): 100 curiosidades de TBC + WotLK visitables/comprobables en el mapa, ≥ 45 min; «agrégale Easter eggs y secretos»
- orden (Claude): cuenta regresiva recorriendo las zonas en orden geográfico, para que los mapas con ruta cuenten un viaje; el usuario puede pedir el orden rarísimas/populares de Reinos del Este
- **SIN Overgear** (escena borrada antes de la voz) · **53 min aceptados** · **sin vista previa**
- **Música: OST ORIGINAL de WoW** por zona (regla del canal 23-oct), NUNCA Lyria · **Mapas reales con ruta** en cada bloque de zona (regla 23-oct) con foto real de lo que la voz nombra

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada en curso) · ANTES del render: `python fab.py limpiar --publicados --borrar` (E: con 29 GB libres el 24-oct; libera ~15,8 GB) y revisar eventos NTFS de E:

## Hecho
- `nuevo --yt` (23-oct) · `canales --actualizar` (23-oct): antes que Warcraft (31-oct) se quedan sin video Crónicas del gaming (27), Sapiens (28), Cuerpo en Neón (29) y LogIA (30)
- guion.py completo: intro + c100…c001 + cierre; `ZONA_DE` (zona de cada curiosidad: música y mapas) y `_BLOQUES`
- adelantado para los tramos 6-8: `mapas/` (25 mapas de Wowhead es-ES, 1022x668; Dalaran no existe en Wowhead), `audio/wow/` (21 temas OST por zona, `_temas.json`) y `musica_wow.py` (tema por zona según `ZONA_DE`)
- `nucleo/secuencia_yt.py`: `--rehacer` sin ids exige `--todos`; carpeta temporal alternativa si un ffmpeg colgado retiene la anterior
- `nucleo/limpiar_publicados.py`: salta entradas NTFS rotas (E: con errores 55 el 23-oct); `limpiar --publicados --borrar` liberaría 15,8 GB: hacerlo ANTES del render (E: 59 GB libres)

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

## Cierre (regla del 12-oct-2026)
- [ ] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [ ] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»); `canales/formula/cronicas_warcraft.md` con el resultado a 7 días
