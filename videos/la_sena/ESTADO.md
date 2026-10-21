# La seña (corto) + «Antes de decir que sí» (taller HTML, 3.º de secundaria, Jalpa) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: ninguno (taller presencial en una secundaria de bajos recursos de Jalpa, Zac.; no va a YouTube) · sin fecha
- estilo: pegatina_flow → doc: docs/estilo_pegatina_flow.md · ejemplo: videos/jalpa/ (+ asteroide_invisible para MG) · presentación como C:\googleimagenes\scratch\taller_hablemos
- etapa: TERMINADO (21-oct): `salida/La_sena_MASTER.mp4` 1080p 3:22 (CER 0, desfase 0, negro 1,6 s) + taller empaquetado con el
  corto: `taller/Antes_de_decir_que_si.html` (86 MB, corto a 720p, abre sin internet)
- siguiente: que el usuario confirme los datos de «Falta» (secundaria, uniforme, números) antes de dar el taller; al aprobar,
  `python fab.py la_sena limpiar` (segmentos/ = 874 MB). Si cambia un texto: editar `taller/index.html` y `python taller/empaquetar.py`

## Sesiones (plan de tramos · «continúa el video la_sena» retoma aquí · protocolo docs/sesiones.md)
- alias: la_sena, La seña, el taller de Jalpa, el del hermano mayor, Antes de decir que sí
- vista previa: con audio completo (voz + Lyria + SFX + mezcla), en el 🎞 Montaje del panel
- leer al empezar: este ESTADO.md, PLAN_TALLER.md y docs/estilo_pegatina_flow.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 0 | Ideas, investigación (llanto, contexto de Jalpa) y diseño | ✅ 20-oct | 5 ideas → la 1 (el hermano mayor y la «chamba») |
| 1 | guion.py (FICHA, LYRIA, voces) + voz ElevenLabs + Flow (36 prompts) + recorte + profundidad | ✅ 20-oct | Flow 71/72; 20 hojas recortadas; 16 profundidades; voz 29/29 CER 0 (568 créditos de la cuenta 2); duración natural 3:22 |
| 2 | Escenas cuesta→bendición (0:00-1:53) + Lyria + sfx + mezcla + montaje con audio | ✅ 20-oct | 24 tomas; Lyria 3 tramos (0,32 US$ con 2 repetidos); 11 efectos de ElevenLabs (950 créditos); montaje en el panel + previews/montaje_0-1m53.mp4 enviado |
| 3 | Escenas tenis→epílogo (1:53-3:22) + render + MASTER + rigor | ✅ 21-oct | 25 tomas; 4 efectos ElevenLabs (330 créditos, cuenta 2); render 27 min; rigor 30 cuadros: solo el negro (2,0 → 1,6 s, `--rehacer`) |
| 4 | Presentación HTML (18 diap. con pegatinas animadas) + empaquetado con el corto | ✅ 21-oct | 18 diapositivas revisadas en el navegador; corto dentro (720p, 2 Mbps) |

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (vacío: tramos 3 y 4 cerrados el 21-oct)

## Decisiones con el usuario (20-oct-2026)
- Mismo público que «Hablemos para entendernos» (3.º de secundaria) pero en barrio expuesto a violencia y drogas; tratarlo SUTIL.
- Objetivo: que lloren (kama muta: amor y sacrificio, no sangre ni miedo; Scared Straight empeora la delincuencia, Cochrane).
- Ambientado en Jalpa real, NO gringo (la 1.ª presentación tenía lockers, maestra de high school, hamburguesa…).
- «Estilo» = la técnica pegatina Flow (Flow pinta, el código mueve), NO la temática de Warcraft ni de videojuegos.
- Formato: presentación HTML de varias diapositivas, el corto a la mitad y la presentación con el mismo estilo del corto.

## Hecho
- Flow (20-oct, proyecto «oct 20 - 20:41», Nano Banana 2.1 · 16:9 · x2 = 0 puntos): 36 prompts → 71 imágenes. Nombres = clave de
  prompts.json sin el número + _a/_b. Hojas de contacto: previews/_contacto_imagenes.jpg y _contacto_hojas.jpg. Revisión: fondos de
  Jalpa sin rastro gringo (cuesta, azotea con varillas, cocina con cubeta, parada de la 54, secundaria con arcotecho, cancha de
  graduación, reja con troca, plaza con las torres); personajes coherentes entre hojas (Ángel 8/14/graduación, Toño 13/19/19b).

- Recorte (pegaflow, 20-oct): 20 hojas → piezas/; mapa número → pose en MAPA_PIEZAS.md.
- Fondos elegidos (con profundidad en imagenes/depth/): las variantes _a de todos, salvo azotea_noche_b (trae la escalera).
- Voz (20-oct): ElevenLabs eleven_v4, cuenta 2. Ángel = Sebastian «Lively Teenager»; Toño 13 = Alejandro; Toño 19 = Alexander-Clear;
  Rosa = Laura D; papá = Carlos Mestre (voice_id en guion.py). 29 frases, 92 s de voz, CER 0. ALIAS_QA porque Whisper «corrige»
  apá→papá, amá→mamá, pos→pues, secu→Seku. Márgenes de música: post 3 s en cuesta, post 8 s en azotea, post 3 s en tenis, pre 24 s
  en bendición (la gotera), pre 20 s + post 4 s en graduación. Pista de solo voz: previews/voz_la_sena.mp3.

## Falta
- [ ] Confirmar: nombre de la secundaria, color del uniforme (puse guinda), colonia
- [ ] Verificar: 089, Línea de la Vida 800 911 2000, nota de la Fiscalía de Jalisco (Crónica, 7-ago-2025), cita de «keepin' it REAL»
- [ ] Que el usuario apruebe las voces (cambiar una = otro voice_id en guion.py + `voz` solo regenera esas frases)

## Lecciones de este video (solo lo no obvio)
- Lyria no pasa de ~100 s con este pedido (pidió 113 s dos veces, salió 98-100): 3 tramos. Y NO respeta «casi silencio»: la gotera
  y el negro final los hace `_musica_ajuste.py` (correr tras `lyria_tramos.py armar`, antes de `mezcla`).
- Pieza que trae medio cuerpo de OTRO personaje (rosa_hoja/02, la bendición): primer plano con el corte de abajo fuera de cuadro y un
  poste desenfocado delante (`desenfocado()`) tapando el corte lateral; el muchacho de gris pasa por Toño.
- Pieza recortada sin su mueble (rosa_hoja/01c): copiar el fondo antes de dibujarla y RESTAURAR la mesa pintada bajo la línea del
  corte (`cocina()`): la mesa tapa los codos y no se ve el borde de papel del corte.
- ALIAS_QA con acentos no casa: Whisper normaliza sin acentos antes de comparar → claves y valores en ASCII («papa»: «apa»).
- Un mosaico de Flow con «Error» no tiene <img>: hueco doble en y + un Expires sin pareja → `null` en ese hueco antes de invertir
  (anotado en docs/estilo_pegatina_flow.md §1).
- angel8_hoja (a y b) trae el MARCO DE PUERTA en la pose de llorar: no ponerlo sobre la puerta pintada de puerta_noche (puerta sobre
  puerta); en la escena 2 usar la pose de pie sin marco o recortar el marco.

- (tramo 3) Los ciclos de ESTE video ya vienen a escala: el «×1,3» de `anda` (frio_extremo) los hacía más altos que la puerta.
- (tramo 4) Panel del navegador integrado OCULTO = animaciones CSS congeladas en 0 (pegatinas invisibles): para revisar,
  `document.getAnimations().forEach(a=>a.currentTime=4000)` antes de la captura. El corto embebido a 1080p crf 25 → HTML de
  299 MB (el grano del acabado no comprime): 720p a 2 Mbps → 86 MB.

## Archivos clave
- `PLAN_TALLER.md` (guion + diapositivas) · `_prompts.py` → `prompts.json` · `taller/` (index.html, _materiales.py, empaquetar.py)
