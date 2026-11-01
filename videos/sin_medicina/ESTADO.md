# ¿Cómo sobrevivían los humanos antiguos SIN medicina? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: sapiens_con_wifi · meta: dom 18-oct-2026 14:00 CDMX (20:00 UTC; ciclo 4 d tras `un_dia_30mil` 14-oct; antes mié 21-oct, movido el 12-oct desde el panel) · confirmar con `python fab.py yt videos sapiens_con_wifi`
- estilo: secuencia_flow EN ESPAÑOL (dibujo animado tinta + color plano, como Wild Next Door; mascota «Sapi» con diadema de wifi) → docs/estilo_secuencia_flow.md + docs/manual_wild_next_door.md
- etapa: CERRADO 12-oct-2026: subido en privado y programado dom 18-oct 14:00 CDMX (https://youtu.be/d53XquSO440; movido desde mié 21-oct el 12-oct, verificado en YouTube el 13-oct) · MASTER 8:52 verificado (CER 0,0011)
- siguiente: medir el 25-oct (`yt videos`/`yt metricas`) y llenar el registro de `canales/formula/sapiens_con_wifi.md`; lecciones del cierre en docs/manual_wild_next_door.md § «Hallazgos de sin_medicina»

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: sin medicina, sobrevivir sin medicina, humanos antiguos sin medicina
- leer al empezar: docs/manual_wild_next_door.md (§ «Imágenes SIN extensión» y «Paso a paso» 6-10), canales/formula/sapiens_con_wifi.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | datos, guion, voz, tiempo, beats, prompts | ✅ 12-oct-2026 | guion 1 505 pal., voz 8:06 (CER 0, 1 frase reescrita), beats 111, prompts 111 |
| 2 | Flow (6 clips + 106 imágenes), medios, Lyria, video, mezcla, final, verificar, miniatura, youtube.json, subir PRIVADO + programar | ✅ 12-oct-2026 | d53XquSO440; ver «Lecciones» y el manual |

## Decisiones del episodio (preguntadas al usuario)
- tema: «¿Cómo sobrevivían sin medicina?» (ref. Mango Explica SP ×11) · duración 8-9 min · voz Dan · música Lyria
- Flow: 50 puntos → `clips_s=[10]*7` (49 puntos, 70 s de video al inicio), el resto IMAGEN (Nano Banana 2 Lite, gratis)
- subir en PRIVADO; fijar fecha de publicación solo si el usuario lo pide (hueco sugerido arriba)

## Hecho
- Datos: `ideas sapiens_con_wifi` (12-oct), transcripción de Mango (gancho: Lister 1865 → «tú eres descendiente de supervivientes»),
  hechos verificados con fuentes (docstring de guion.py). Fórmula del canal: canales/formula/sapiens_con_wifi.md
- Guion final: 10 escenas (hook, mito, plantas, otzi, dientes, trepanacion, cuidado, amputacion, botiquin, outro), 94 frases.
- Voz Dan: `_ronda.py` + `_ronda2.py` (solo `cuidado_2`, sin el nombre «Shanidar»). 531,6 s de video (8:52).
- `hacer_prompts.py` → `prompts.json` + `flow/escenas.json` (111). Pictogramas sin cifras; Sapi es el «tú» (también en escenas modernas).

## Falta
- [ ] Flow: clip de prueba primero; proyecto de CLIPS aparte del de IMÁGENES; 360p + «720p mejorada»; imágenes con Nano Banana 2 Lite x1
- [ ] `medios` y revisar TODAS las hojas (marcos de tarjeta en clips → `recorte_por`; texto colado; Sapi con diadema de wifi; pierna del niño en 91-93, 109)
- [ ] Lyria (`cd videos/sin_medicina; python ../../nucleo/lyria_tramos.py`), `video`, `mezcla`, `final`, `verificar`, revisar MASTER cada ~3 s
- [ ] miniatura (Flow; sugerencia: Sapi con la diadema de wifi, fondo claro, frase manuscrita corta tipo «SIN PASTILLAS» y flecha al cráneo/pierna), youtube.json (fuentes + aviso de IA)
- [ ] subir PRIVADO: `python fab.py yt subir sin_medicina sapiens_con_wifi private` (programar solo si el usuario lo pide); `publicados` con `"formato": "pregunta_supervivencia"`

## Cómo retomar (comandos)
```
python fab.py continuar sin medicina
python fab.py estado sin_medicina
python fab.py sin_medicina medios
```

## Archivos clave
- `guion.py` (narración, hechos, FICHA, LYRIA), `hacer_prompts.py`, `beats.json`, `prompts.json`, `flow/escenas.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- Dan lee ~3,3 pal/s: 1 394 palabras habrían dado ~7:30; se añadió una escena (Hombre de Hielo) ANTES de la voz para llegar a 8-9 min.
- Whisper no reconoce «Shanidar» ni «Ötzi»: se quitaron los nombres de la narración (la frase falló 12 tomas).
- Prompts con cifras («ten», «thirty») pueden colar números: se usaron pictogramas con siluetas llenas y pálidas, sin dígitos.
- Flow dio saldo para 6 clips (no 7): `clips_s=[10]*6`. El beat 7 se partió en DOS imágenes (beats.json editado a mano desde `_beats_7clips.json`; `beats` automático rehace TODO el tramo de imágenes y desalinea los prompts: NO volver a correrlo). `hacer_prompts.py` ya desplaza +1.
- flowscrap: «Flow no mostró la pestaña Video» salía como error pero SÍ generaba el clip (no relanzar: duplica gasto). Sus descargas 720p a veces no llegan; la manual (⋮ → Descargar → 720p) tarda 1-4 min y cae en Descargas con nombre del prompt: copiar a `Descargas/flow-sin_medicina/scene-00N.mp4` y a `medios/`.
- El colector viejo posteaba el 360p por /medio y pisaba al 720p: verificar con ffprobe que cada `medios/scene-00N.mp4` mida 1280x720.
- Chrome oculto = Flow no avanza: si la pestaña del grupo de Claude no es la activa/visible, los timers se congelan, no cargan <img> y los envíos no se registran. Antes de lanzar lotes, comprobar `document.visibilityState === 'visible'`.
- Imágenes por lotes (sin extensión, que va a 1/min): `execCommand('insertText')` en `.ProseMirror` + `key Return` real (con `wait 2` antes) y control por conteo de tarjetas; el prompt de cada imagen lleva añadido «no numbers, digits or numerals» (la 007 coló dígitos: rehacerla). Bajar con `nucleo/flow_integrado.py bajar` (líneas «N uuid expires firma»). La 008 salió dos veces (se bajó la primera).
