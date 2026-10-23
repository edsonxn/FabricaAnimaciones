# Los Corn Flakes Nacieron de un ERROR — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: pieza_oculta · jue 29-oct-2026 13:00 CDMX (hueco del canal)
- estilo: secuencia_flow (plastilina, clips e imágenes de Google Flow) → doc de estilo: docs/estilo_secuencia_flow.md
- etapa: subido y PROGRAMADO (jue 29-oct 13:00 CDMX) · https://youtu.be/4GLQgAKPQBg
- siguiente: Short vertical de 40-60 s (fórmula: uno por largo, al día siguiente) · registrar a 7 días en canales/formula/pieza_oculta.md

## Sesiones (plan de tramos · «continúa el video corn_flakes» retoma aquí · protocolo docs/sesiones.md)
- alias: corn flakes, Kellogg's, el de los hermanos Kellogg, el 1 de la tanda de Plastitube
- vista previa: no; el usuario revisa en 🎞 Montaje del panel (elegido el 23-oct)
- leer al empezar: este ESTADO.md, `canales/formula/pieza_oculta.md` (fórmula nueva de marcas, 23-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo en una sesión: guion → voz → beats → prompts → Flow → vivo → armado → Lyria → mezcla → final → subir | ✅ 23-oct | todo en una sesión; render en C: por fallo del disco E: |

## Decisiones del episodio (preguntadas al usuario al empezar, 23-oct-2026)
- duración total: 8-10 min (~1 500 palabras) · minutos iniciales en video: 1 min (clips combinados de 10 s, 360p) · resolución: 360p + descarga 720p mejorada
- primer video de la fórmula nueva (`canales/formula/pieza_oculta.md`): marca con giro humano, objeto en el título, miniatura con el producto real + nombre; lleva Short al día siguiente

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada)

## Hecho
- 23-oct: render 11 min (10 vivos + parallax), mezcla −14 LUFS, MASTER 8:10 1080p, verificar CER 0,005; rigor 167 cuadros sin bloqueos; subido 4GLQgAKPQBg privado programado 29-oct 19:00Z, miniatura aplicada; .srt NO (token sin permiso de subtítulos: subir a mano en Studio); registrado en canales/pieza_oculta.json, BITACORA y fórmula; música catalogada
- 23-oct: voz 123/123 (425 s; «Will» → «Güil» por contexto y 5 frases sin el nombre), `tiempo` 8:10, 100 beats; 94 imágenes Nano Banana 2.1 en el integrado (3 rehechas: 029, 038, 099) + 6 clips 360p→720p bajados con Claude in Chrome (esperar a que llegue cada archivo antes de cambiar de página); recorte_por 001/003 (letterbox) y ambiente 0 en 001/004 (voces)
- 23-oct: `nuevo corn_flakes --secuencia`; `canales --actualizar` (Plastitube: siguiente hueco jue 29-oct 13:00)
- 23-oct: guion.py (16 escenas, 123 frases, 1 397 palabras ≈ 8,2 min; FONETICA para Kellogg/Battle Creek/Will/John), youtube.json, LYRIA en 5 tramos

## Falta
- [ ] Short vertical (40-60 s, el día del guiño o el trigo olvidado) · [ ] .srt a mano en Studio · [ ] métricas a 7 días

## Cómo retomar (comandos)
```
python fab.py estado corn_flakes
python fab.py corn_flakes medios          hojas previews/medios_NN.jpg (qué llegó de Flow y qué falta)
python fab.py corn_flakes ingesta --espera 900
```

## Archivos clave
- `guion.py` (narración + FICHA visual), `beats.json`, `prompts.json`, `flow/escenas.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- Detalle en docs/estilo_secuencia_flow.md § «Hallazgos de corn_flakes»: prompts por tiempo, descargas 720p esperando cada archivo, letterbox en clips, «Will» en Chatterbox, disco E:.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/pieza_oculta.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
