# Los 20 EFECTOS MANDELA de Call of Duty que TÚ recordaste (parte 2) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_cod = «Expediente 141» (4.º video) · meta: sáb 14-nov-2026 13:00 CDMX (canal URGENTE: sin video desde el 14-nov; hora nueva 13:00 desde el 11-nov) o el primer hueco tras el MASTER
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + MG `nucleo/mg_cod.py` + mapas + sonido original + OST oficial) → doc: docs/estilo_secuencia_yt.md
- etapa: voz OK · beats (108, 15:27) · clips 108/108 con mosaico REVISADO · efectos.py ESCRITO (anclas OK) · promesas.md escrito
- siguiente: CERRADO. Subido https://youtu.be/8xOoO4YwA2c, programado sáb 14-nov 16:00 CDMX. Medir a 7 días contra la parte 1 (XL3MZ4Oj7Ko); si aguanta, parte 3

## Sesiones (UNA sesión directo al MASTER, regla 5-nov; MASTER a la tele sin preguntar)
- alias: «mandela 2», «el de los mandela de la gente», «cod mandela parte 2»
- leer al empezar: este ESTADO.md · plantilla `videos/cod_mandela/` (guion.py, efectos.py, armar_musica_ost.py, bajar_pegatinas.py) y `videos/cod_misterios/` (lo más nuevo: _mosaico.py, _escribir_busquedas.py, efectos.py) · `canales/formula/cronicas_cod.md`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación → guion → voz → pegatinas → OST → sonidos nombrados → MG nuevos | ✅ cerrado 20-nov (el video ya está subido) | cortada por contexto (180 mil) tras la voz |
| 2 | tiempo → beats → busquedas → bajar → efectos → promesas → fx hoja → música → render → MASTER → miniatura → subir | ✅ 14-nov | MASTER 15:27 revisado (promesas 33/33, ◐ 7 y 8), miniatura Flow (Gaz + M1911 + «2»), subido y programado |

## Decisiones del episodio (13-nov-2026)
- tema: «Mandela PARTE 2» elegido por el usuario entre 3 (Mandela parte 2 / Mandela de Zombies / villanos). Datos: Mandela 6 780 vistas, 35,2 % visto; MW4 334 (46 %); misterios 177 (2 días). Solo cambia UNA variable: la fuente (efectos que contó la gente + suplentes de la parte 1 + nuevos)
- duración (la decide Claude): ~15-16 min, 20 puestos en cuenta regresiva (Mandela 1 = 14:20 con 35 %; el de 24 min aún sin datos)
- voz: Damián de ElevenLabs (`BPwS5yO6aXvwg8auqNwS`), eleven_v4_turbo
- **CORRECCIÓN DE VOZ (queja justa, @v5x777cod_rdr_fan0, 12-nov):** Kino der Toten / Verrückt / Der Riese sonaban con acento francés; nombres en inglés forzados; el tono «frustrado» sonaba actuado → nombres alemanes con FONETICA comprobada al oído («Kíno der Tóten», «Ferrúkt», «Der Ríse»), menos corchetes de emoción (nada de [annoyed]/[sighs] teatrales; [deadpan] y [short pause] sí), y la voz le da las gracias en el video (queja justa = se corrige, no se burla)
- Comentarios (13-nov, `yt comentarios cronicas_cod`): 8 nuevos. Efectos de la gente → puestos: @brexxy7369 (AUG en la granja de BO2, Ugz7EOCl7eQvnRkWqVF4AaABAg), @Rafa-xe3pw (Mason a Woods «¿me recuerdas?», Ugy5ufFGlvSuVt3TAlZ4AaABAg), @metal9208 (duda del de Moon, UgwR4poiAMmxZRQHcyl4AaABAg). Contraburla: @AndrésRíos-v8y («Black Ops salió en 2007 y tenía 13 misiones», Ugz5_SxOl2jDb0wNjT14AaABAg) = efecto Mandela en vivo. Otros: @lycanroc8806 (Pawn takes Pawn, carta física), @mr_brigthside21 (chamba), @felixhd7436, queja de voz @v5x777cod_rdr_fan0 (UgzdPVWBh-q8W6o2CZx4AaABAg)
- REGLA DE ORO: § REGLA DE ORO de docs/estilo_secuencia_yt.md (≥ 5 MG y ≥ 5 pegatinas/min, ningún tramo > 4 s con el clip solo); promesas.md; `fab.py cod_mandela2 chequeo`; `FAB_FX_FINAL=1 fx hoja` revisada antes de `video`
- no repetir temas de `cod_mandela`, `cod_misterios` ni `cod_mw4_secretos`; OST que no se haya oído en el canal

## Falta
- [x] investigación · [x] guion · [x] voz · [x] beats/clips · [x] MG/pegatinas · [x] sonido/mezcla · [x] render · [x] miniatura Flow · [x] subida

## Archivos clave
- `guion.py`, `investigacion.md`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar, miniatura Flow y registrado (`canales/cronicas_cod.json`, BITACORA)
- [x] HALLAZGOS documentados (`docs/estilo_secuencia_yt.md`, `canales/formula/cronicas_cod.md`)

## Lecciones (14-nov-2026)
- `verificar` cayó por RAM y luego por CUDA OOM (otra sesión con Whisper en la GPU): el Whisper impreso vale; desfase (0 ms) y hoja se rehicieron en CPU leyendo solo un tramo del audio.
- Abiertos: promesa 7 (uniforme caqui) solo en el cómic sepia; promesa 8 (césped enrollado de Nuketown) no se distingue en el clip; marca «NXG» chica en la esquina de los clips de CoD 2 (b35-38).
- Lecciones de canal en `canales/formula/cronicas_cod.md` (14-nov).
