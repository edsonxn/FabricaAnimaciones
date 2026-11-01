# 12 Animals You Should NEVER Kill Around Your House (And 2 You Should) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: wild_next_door · PROGRAMADO mié 21-oct-2026 16:01 UTC (10:01 CDMX; ciclo 3 d tras `arana_techo`)
- estilo: secuencia_flow (dibujo animado, tinta gruesa + colores planos, fondo claro) → docs/manual_wild_next_door.md (leer primero)
- etapa: PROGRAMADO 21-oct 16:01 UTC (https://youtu.be/fRiMIprIcM8, MASTER v2 con imágenes vivas, miniatura y .srt) · registrado
- siguiente: el usuario BORRA la v1 privada https://youtu.be/kDsjeEwoLMA (sin vivos) · medir el 28-oct contra `cinco_bichos` · `limpiar` al aprobar

## Sesiones (plan de tramos · «continúa el video doce_animales» retoma aquí · protocolo docs/sesiones.md)
- alias: doce animales, 12 animals, video de 14 minutos de Wild Next Door
- vista previa: SÍ, el primer minuto con audio completo (voz + Lyria + mezcla) antes del render entero: `python fab.py doce_animales video --hasta 60`
- leer al empezar: `docs/manual_wild_next_door.md` (§ «FOTO REAL» y § «Imágenes SIN extensión»), `canales/formula/wild_next_door.md`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | datos + guion + voz + tiempo + beats + fotos reales | ✅ 18-oct | 2 353 palabras → 14:25; 17 frases aceptadas por CER (cifras en dígitos de Whisper) |
| 2 | prompts (195 imágenes, gratis, navegador integrado) + 7 clips en Flow | ✅ 19-oct | 191 imágenes (10 rehechas) + 7 clips 1280x720 · 47 pts gastados, quedan 3 · ~2 h |
| 3 | efectos.py (pegatinas + 3 clips de clímax) → Lyria (8 tramos) → mezcla → vista previa 60 s → render → final → verificar → miniatura → subida | ✅ 19-oct | 14 pegatinas, 3 clímax, 23 vivos + VIVO_AUTO; 2 renders (el 1.º sin vivos por bug del motor); subido privado fRiMIprIcM8 · ~3 h |

## Decisiones del episodio (preguntadas al usuario al empezar, 18-oct-2026)
- duración total: **14 min** → 14:25 real (865 s)
- tema: lista «Never Kill» ampliada de bichos a ANIMALES del patio (variable probada). Ref: Curious Kids Discover ×70 (11 min, 210 k vistas), mismo formato ×47 y ×18
- lista: 12 mariquita · 11 milpiés · 10 mosca sírfida · 9 escarabajo de suelo · 8 araña amarilla de jardín · 7 libélula ·
  6 abejorro · 5 sapo (mito verrugas) · 4 culebra rayada · 3 murciélago · 2 lagartija de cerca (Lyme) · 1 zarigüeya (mito
  5 000 garrapatas); «los 2 que sí»: linterna moteada y garrapata de patas negras
- saldo Flow: el usuario dice **50 puntos** → 47 pts = 66 s (3 de margen)
- clips: **gancho + clímax**. El motor solo pone clips al inicio → `clips_s=[10]*4` (28 pts, primeros 40 s) y 3 más
  (10+10+6 s = 19 pts) como FX `video` a cuadro entero en `efectos.py`: n.º 1 (zarigüeya se desmaya), linterna moteada, cierre
- foto REAL de cada animal como pegatina al presentarlo (regla nueva del usuario, 18-oct)
- formato a anotar al subir: `never_kill_lista`

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada: tramo 3 cerrado el 19-oct)

## Hecho
- `nuevo doce_animales --secuencia` y `canales --actualizar` (18-oct): WND se queda sin video el mié 21-oct 10:00; humanidad_100k (77 %) está en producción para ese hueco
- guion.py: 17 escenas, 150 frases; ficha de hechos con fuentes en el docstring; FICHA con 14 mascotas + accesorio fijo
- voz (`_ronda.py`, espera GPU libre): 150 frases × hasta 12 tomas; voz total 798 s; `tiempo` 865 s; `beats` 195 escenas
- LYRIA en 8 tramos ≤ 170 s
- Fotos reales: 14 en `pegatinas/` + `CREDITOS.md` (autor y licencia), revisadas en `previews/_fotos.jpg`. Escarabajo =
  *Pterostichus melanarius* (ejemplar de museo con alfiler: recortar); mosca sírfida pequeña en su foto → recortar.
- Tramo 2 (19-oct): `hacer_prompts.py` (claves por TEXTO, 12 tarjetas con numeral, ronda 2 al final) + `clips_climax.json`;
  imágenes en el proyecto Flow «oct 19 - 08:08», clips en «oct 19 - 08:47» (cuenta Edsonxn, vídeo Omni 1.1 Flash 360p →
  descarga 720p mejorada). Rehechas 016 044 048 064 074 116 128 145 149 183 (originales en `medios/_ronda1/`).
  `guion.py`: `recorte_por` scene-001 0.03 (marco), `ambiente_por` scene-004 0 (voz «Whoa…»).

## Falta
- [x] tramo 2 · [x] tramo 3 · [x] programado 21-oct 16:01 UTC · [ ] borrar v1 kDsjeEwoLMA (usuario)

## Archivos clave: `guion.py`, `efectos.py`, `youtube.json`, `_miniatura.py`, `beats.json`, `hacer_prompts.py`, `prompts.json`, `clips_climax.json`, `flow/escenas.json`, `medios/`, `pegatinas/`, `_ronda.py`, `_fotos.py`
## Lecciones de este video (solo lo no obvio)
- Estimar duración con EnglishComic: **3,36 pal/s + 1,12 s por frase**; acertó: 14:28 estimado vs. 14:25 real.
- Con muchas cifras en letras Whisper falla por CER: revisar `voz/eval.json` (hyp) y aceptarlas en `CER_MAX_POR_FRASE`.
- Wikimedia da 429 en ráfagas: pausas de 5 s + reintentos con espera creciente.
- **Paquete del navegador:** el portapapeles NO llega al navegador integrado (Ctrl+V pega vacío): pegar el JS en `javascript_tool`.
  `flow_integrado.py paquete` repetía el cierre en cada prompt (arreglado el 19-oct: 75 k → 38 k caracteres). Verificar con
  un hash por prompt (JS vs. Python) antes de enviar. Lotes de 12 = 25 acciones de `browser_batch` (el máximo) con la espera
  DENTRO de `__ins`: 191 imágenes en ~35 min, 0 envíos perdidos.
- **Clips:** cada descarga abre «Guardar como» de Windows, pero el archivo ya queda completo en `E:\Downloads_jaire\<uuid>.tmp`
  (o con su nombre si el usuario pulsa Guardar): copiarlo de ahí. En el editor del clip, «Descargar contenido multimedia» →
  720p; la tira de miniaturas salta entre clips (el más nuevo primero). 2 de 7 con marco (~12 px) y 2 con voz/risa
  (Whisper base.en en CPU sobre el mp4).
- **El render NO aplicaba imágenes vivas ni parallax** (`python -m secuencia` = `__main__`, isinstance fallaba): arreglado en
  `nucleo/secuencia.py`. La hoja `fx hoja` sí los mostraba: comprobar el vaivén EN EL MASTER (`phaseCorrelate`, ≈ 6 px).
  Con vivos el render pasa de ~8 min a ~30 min (865 s).
- Flow metió ~1 s de negro TOTAL en la transición del clip scene-002 (dentro de la boca): saltado con el mismo clip encima
  (`desde`/`vel` en `efectos.py`). Medir el % de negro de cada clip antes de armar.
- YouTube rechaza etiquetas > 500 caracteres contando comillas de las que llevan espacio: dejar ~410.

## Cierre (regla del 12-oct-2026)
- [x] subido (privado), miniatura, registrado (`canales/wild_next_door.json`, BITACORA) · [x] programado 21-oct 16:01 UTC (orden del usuario)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
