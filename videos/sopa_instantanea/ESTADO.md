# Lo Perdió TODO y a los 48 Años Inventó la Sopa Instantánea en su Patio — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: pieza_oculta · lun 2-nov-2026 13:00 CDMX (hueco del canal)
- estilo: secuencia_flow (plastilina, clips e imágenes de Google Flow) → doc de estilo: docs/estilo_secuencia_flow.md
- etapa: subido y PROGRAMADO (lun 2-nov 13:00 CDMX) · https://youtu.be/iJ7QsuU1nUA
- siguiente: Short vertical de 40-60 s (fórmula: uno por largo, al día siguiente) · .srt a mano en Studio · registrar a 7 días en canales/formula/pieza_oculta.md

## Sesiones (plan de tramos · «continúa el video sopa_instantanea» retoma aquí · protocolo docs/sesiones.md)
- alias: sopa instantánea, Maruchan, Momofuku Ando, Cup Noodles, el 2 de la tanda de Plastitube
- vista previa: no; el usuario revisa en 🎞 Montaje del panel (como corn_flakes)
- leer al empezar: este ESTADO.md, `canales/formula/pieza_oculta.md` (fórmula de marcas, 23-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo en una sesión: guion → voz → beats → prompts → Flow → vivo → armado → Lyria → mezcla → final → subir | ✅ 23-oct | |

## Decisiones del episodio (23-oct-2026)
- tema elegido por el usuario entre 3 (sopa instantánea / LEGO / Tupperware), n.º 2 de la tanda
- duración total: 8-10 min (salió 8:13) · minutos iniciales en video: **2 min (el usuario)** = 12 clips combinados de 10 s, 360p + descarga 720p mejorada

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada)

## Hecho
- 23-oct: guion.py (17 escenas, 123 frases, 1 415 palabras; FONETICA japonesa; ficha verificada en la docstring), youtube.json con 16 capítulos
- 23-oct: voz 123/123 (8:13; 5 frases aceptadas con CER_MAX por errores de Whisper), 92 beats, 92 prompts
- 23-oct: 12 clips (84 puntos; proyecto Flow 6f6fcb85-…) bajados en 720p con Claude in Chrome; 80 imágenes Nano Banana 2.1 (proyecto fa1f0704-…), 7 rehechas (5 por la ficha de la esposa, 1 pendiente, 1 rechazada)
- 23-oct: 4 vivos + VIVO_AUTO, 6 rótulos; Lyria nueva 5 tramos (tramo 1 regenerado por corto); render 11 min; mezcla −14 LUFS, voz 12,9 dB sobre la música; verificar CER 0,0014; rigor 164 cuadros sin bloqueos
- 23-oct: subido iJ7QsuU1nUA privado programado 2-nov 19:00Z, miniatura aplicada (producto real de Commons como ingrediente); .srt NO (token sin permiso); registrado en canales/pieza_oculta.json, BITACORA y fórmula

## Falta
- [ ] Short vertical (40-60 s: la noche del tempura o los policías en la nieve) · [ ] .srt a mano en Studio · [ ] métricas a 7 días

## Archivos clave
- `guion.py`, `_imagenes.py` + `hacer_prompts.py` (prompts por tiempo), `efectos.py`, `prompt_miniatura.md`, `medios/`

## Lecciones de este video (solo lo no obvio)
- Detalle en docs/estilo_secuencia_flow.md § «Hallazgos de sopa_instantanea»: filtro de Flow con la ficha de la esposa, colector por mosaicos, clips en paralelo, tramo de Lyria corto.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/pieza_oculta.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
