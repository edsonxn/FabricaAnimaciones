# Los 30 misterios y leyendas más raros de Call of Duty — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_cod = «Expediente 141» (3.er video) · meta: en cuanto esté (canal URGENTE el 9-nov; hueco de `canales --actualizar`)
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + MG + mapas + sonido original + OST oficial) → doc: docs/estilo_secuencia_yt.md
- etapa: SUBIDO privado y PROGRAMADO mar 11-nov 18:00 CDMX (2026-11-12T00:00Z): https://youtu.be/-4fHC9P5Hw0 · MASTER 2 (24:10) · ✅ miniatura FLOW aplicada el 10-nov («30 MISTERIOS / SIN RESOLVER», hombre de traje de MW3 + cara de Alcatraz; `prompt_miniatura.md`; la provisional en `salida/miniatura_provisional.jpg`) · publishAt comprobado en la API tras `yt aplicar`
- siguiente: visto bueno del usuario (10-nov: `tele video … master` = tele apagada (código 4), avisó por voz; el 1.er envío había fallado con ConnectionReset) · medir a 7 días (% visto ≥ 35) contra Mandela · `biblioteca sfx catalogar`; `limpiar` al aprobar; cierre de video (hallazgos al doc) · promesas.md NO se hizo antes del render (Private Eye sin imagen del cartel): revisarlo sobre el MASTER si el usuario lo pide
- antes: voz HECHA (10-nov, 24:10) · 169 clips bajados y revisados en mosaico (`_mosaico.py`; 22 rehechos) · efectos.py PROBADO (`fx --seco` sin errores: 330 efectos; chequeo: fichas 1,6 · MG 6,0 · pegatinas 5,7/min) · sonidos nombrados cortados
- historial (10-nov ~13:40): clips OK (128 = CoD3 de Xbox 360) · `armar_musica_ost.py` HECHO (audio/musica.wav, 32 secciones) · `sfx` hecho · `fx` + `mezcla` HECHOS (−14,1 LUFS, voz +13,4 dB) · `video` llegó al 69 % y falló (legajo de Spectre: `sello` va como (texto, i_marca); corregido) → render completo HECHO + MASTER 1 (1080p, 24:10, desfase 0) · tele no estaba (código 4, avisó por voz) · hoja `previews/final_hoja.jpg`: texto de youtuber en beats 93/123/124 → clips cambiados → `video --rehacer 789-799` y `1047-1067` + `final` + `verificar` LANZADOS (log `_video_log3.txt`) → al terminar: → `final` → `verificar` → `tele video cod_misterios master` → miniatura Flow → subir. promesas.md pendiente (revisar sobre el MASTER: Private Eye no tiene imagen del cartel)

## Sesiones (plan de tramos · «continúa el video cod_misterios» retoma aquí · protocolo docs/sesiones.md)
- alias: «el de los misterios de CoD», «cod misterios», «el 3.º de Expediente 141», «el de 25 minutos»
- vista previa: no (una sesión, directo al MASTER, regla del 5-nov); el MASTER a la tele sin preguntar
- leer al empezar: este ESTADO.md · `videos/cod_mandela/` (plantilla: guion.py, efectos.py, armar_musica_ost.py, bajar_pegatinas.py) · `canales/formula/cronicas_cod.md`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión: investigación → guion → voz → beats/clips → MG/pegatinas → sonido → render → miniatura → subir | ✅ (antes ◐ parcial) (9-nov: investigación, guion, pegatinas, OST, MG nuevos) · 10-nov: voz → clips → efectos → música → render → MASTER → subido y programado | ✅ 10-nov: miniatura de Flow aplicada; tramo CERRADO |

## Decisiones del episodio (el usuario, 9-nov-2026)
- tema: «Los 30 misterios y leyendas más raros de Call of Duty» (elegido entre 3; misma familia que Mandela, que ganó: 1 992 vistas vs 40 de MW4; ref. Fellow ×41,6)
- duración: ~25 min (la pidió el usuario) · puestos: 30 (cuenta regresiva) · Overgear: aún NO
- voz: Damián de ElevenLabs (`BPwS5yO6aXvwg8auqNwS`), eleven_v4_turbo. **Saldo 9-nov: 1 147 créditos (necesita ~4 300); el usuario recarga** → mirar `python nucleo/tts_eleven.py` antes de `voz`
- Comentarios (9-nov): 2 nuevos, 0 quejas, 0 sugerencias: @H.Hoster (Mandela 4:05, logro de Shadows of Evil) y @LDVader («0:19 esa es trampa jaja»)
- no repetir temas de `cod_mandela` ni de `cod_mw4_secretos`
- REGLA DE ORO: § REGLA DE ORO de docs/estilo_secuencia_yt.md (≥ 5 MG y ≥ 5 pegatinas/min, ningún tramo > 4 s con el clip solo); promesas.md; `fab.py cod_misterios chequeo` antes de renderizar

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- 9-nov (sesión 1 cortada a 180 mil): HECHO investigación (`investigacion.md`, 30 + 10 suplentes), guion (`guion.py`, 30 puestos, posts de sonido: intro chillido, p18 riff IX, p13 voz rusa, p11/p11b Samantha, p07 Sanctuary), 107 pegatinas (`bajar_pegatinas.py`, hoja `previews/pegatinas_hoja.jpg` revisada: NO usar `hesh`; faltan private_eye, richtofen, c_warzone, treyarch → captura/otro título), OST en `audio/ost/` (12 pistas, `_catalogo.txt`), clips candidatos por puesto en `clips_candidatos.md` (búsquedas ya hechas).
- FALTA en orden: voz (tras recarga; el usuario recarga 5 US$ = 25 000 créditos en la cuenta 2) → seleccionar (CER_MAX_POR_FRASE para frases con inglés) → tiempo → beats → busquedas.json (por escena, de clips_candidatos.md + investigacion.md) → bajar → medios (MIRAR) → `ambiente_por` + cortes de sonido `sfx/s_*.mp3` para los posts → efectos.py (copiado de Mandela: reescribir FX entero para este guion con pv/filav/pil + MG nuevos `C.caso`/`C.descifra` + comentarios `com_*` en p22 y cierre) → promesas.md → chequeo/_huecos/_bordes → armar_musica_ost.py (SECCIONES nuevas con las pistas de audio/ost) → sfx → mezcla → video → final → verificar → tele master → miniatura Flow → subir y programar (hueco de `canales --actualizar`).
- 9-nov: OST oficial bajando a `audio/ost/` (`_catalogo.txt`: Ghosts, BO2, MW2019, IW, Ascension; ninguna repetida de Mandela/MW4)
- 9-nov: plantilla copiada de cod_mandela (efectos.py, armar_musica_ost.py, bajar_pegatinas.py, _bordes.py); comentarios capturados (`pegatinas/com_*.png`)
- 10-nov (sesión 2): VOZ HECHA (154/154, 3 754 créditos, cuenta 2 queda ≈ 47 300; CER/TAIL por frase solo por nombres) · `tiempo` = 24:10 · pegatinas richtofen/treyarch bajadas (ARCHIVO en bajar_pegatinas.py); private_eye = captura del clip
- 10-nov: sonidos nombrados en `audio/cortes/_cortar.py` → `sfx/s_chillido|s_riff|s_ruso|s_sam1|s_sam2|s_sanct.mp3` (Samantha comprobada con Whisper; Sanctuary desde la pista de voz de Demucs) · mapa `mapas/verdansk.jpg` (wiki) + tema de mapa nuevo «cod» en `nucleo/mg_mapa.py`
- 10-nov 12:50 (sesión 2 cortada a 180 mil): `bajar -j 4` HECHO: 158/169 en medios/. FALLARON (cambiar búsqueda y repetir con `bajar N --q "…"` o `--url … --desde …`): scene-003 (Origins TS701bMxmSI dio 403 a yt-dlp; reintentar con `-f bestaudio` o `4BnV80YsWlw@26`), 004 y 134-136/138 (Vacant eW2lZ_G4gww: probar sin --download-sections o «Vacant ghost Call of Duty 4»), 028/029 (15yDXFYyWrI → «Kino der Toten portraits»), 039 (Zork SiqPRqYDj9A), 053/055 (Hangar 18 → «Hangar 18 Black Ops aliens»). Ojo: scene-159 bajó EpicsArchive (Dust to Dust, revisar marca).
- 10-nov: `efectos.py` REESCRITO entero para este guion (30 puestos: pv/sil/rel/cam/leg/aba/muro/vs/tabl + `C.caso` al cierre de cada puesto + `C.descifra` (Private Eye, oldman, Nyarlathotep, Morse, ADFGX, Warzone, shadowman) + mapa Verdansk con los 3 teléfonos (presa .17/.22, hospital .48/.66, cantera .74/.27; búnker sin marcar porque no confirmé su sitio) + comentarios `com_Ugx…` = @H.Hoster (p22) y `com_Ugy…` = @LDVader (cierre) + PISTAS de sonidos nombrados `s_*` + VIDEOS de cortes del gancho (102, 135, 116, 161: comprobar que existen tras rehacer 135). SIN PROBAR: correr `fx --seco`, corregir anclas que no encuentre y huecos > 4 s (2.ª pasada de relleno como en Mandela). Private Eye: no hay imagen del cartel → Flow «recreación» o captura del clip.
- LECCIÓN: nunca `Get-Content | Set-Content` en PowerShell 5.1 sobre un .md UTF-8 (lo lee como ANSI y lo deja doble UTF-8); usar Edit
- 9-nov: MG nuevos en `nucleo/mg_cod.py`: `caso(estado, titulo, sub)` (RESUELTO / SIN RESOLVER / FALSO / ERA VERDAD) y `descifra(cifrado, claro)`

## Hecho
- 9-nov: proyecto creado (`nuevo --yt`), tema y duración elegidos

## Falta
- [ ] investigación · [ ] guion · [ ] voz · [ ] beats/clips · [ ] MG/pegatinas · [ ] sonido/mezcla · [ ] render · [ ] miniatura · [ ] subida

## Archivos clave
- `guion.py`, `investigacion.md`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`
