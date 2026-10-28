# Rare: el estudio que Nintendo DEJÓ IR (auge y caída) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · SUBIDO en privado y PROGRAMADO jue 5-nov-2026 18:00 CDMX: https://youtu.be/RwkNXgEnqsU (18:00)
- estilo: secuencia_yt + kit NUEVO `nucleo/mg_rare.py` (humo azul noche + oro de Rareware/Rare Replay) + pegatinas + OST oficial por época · voz ElevenLabs Hope (`eleven_v4_turbo`) → doc: docs/estilo_secuencia_yt.md § Crónicas del gaming
- etapa: subido y programado; esperando el visto bueno del usuario
- siguiente: visto bueno → `fab.py rare_auge_caida limpiar` · hallazgos al doc de estilo · registro a 7 días (~12-nov) en canales/formula

## Sesiones (plan de tramos · «continúa el video rare» retoma aquí · protocolo docs/sesiones.md)
- alias: rare, auge y caída de rare, video de rare, rare_auge_caida
- vista previa: ninguna; directo al MASTER y aviso (el usuario, 28-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 28-oct) | ✅ 28-oct | investigación con fuentes · guion 130 frases · voz turbo · 126 clips (42 fuentes) · OST · 118 FX · render 27 min · subido RwkNXgEnqsU |

## Decisiones del episodio (28-oct-2026, el usuario)
- Tema elegido entre 3 con datos (Rare / Mario 64 + 20 secretos / OoT 10 misterios): **auge y caída de Rare**. Variable que
  cambia: SOLO el formato (historia de un estudio por capítulos). Ref.: Kilobyte Chronicles ×9,1 (1 910 subs).
- 18 min, una sesión, sin vista previa. Comentarios (28-oct): 1 nuevo (@riuma77, ♥0), sin quejas ni sugerencias.

## Hecho
- Investigación por agente + comprobación propia (memorando de Matt Booty 22-sep-2026; «Edson» en Project Dream): fuentes_guion.md.
- Voz 130/130 (CER_MAX_POR_FRASE para nombres: Whisper oye «Rear» por Rare). Verificar: CER medio 0,99 %, desfase 0 ms.
- Clips: escanear.py (hojas propias de 52 fuentes, sin bajar los longplays: ffmpeg salta por HTTP) → agente → plan_clips.py →
  busquedas.json; 11 rehechos tras mirar medios_01-07 y medir el brillo cada 0,3 s.
- Kit mg_rare: ficha, puesto (capítulo), pegatina, eras, acciones (de quién es Rare), reparto (el divorcio de 2002), exodo (fuga
  de talento), torres (ventas), apuesta (balanza SGI). Hojas de prueba: `python nucleo/mg_rare.py prueba`.
- Música: armar_musica_ost.py con cortes por ESCENA y por BEAT (KI, Perfect Dark, Conker, Viva Piñata); apartada en 8 beats.
- Miniatura Flow en el navegador integrado (variante A de 2). youtube.json con capítulos, fuentes y créditos de los 41 videos.

## Lecciones de este video (solo lo no obvio)
- Hojas de contacto de longplays de 6-17 h SIN bajarlos: `ffmpeg -ss t -i <url 360p de yt-dlp -j>` por cuadro, 6 hilos (escanear.py).
- Los «Rare Revealed» (y documentales) cortan cada 2-5 s entre gameplay y entrevista: la hoja engaña; no usarlos para gameplay.
- Los tráileres traen tarjetas de citas/rótulos cada ~25 s («EXPLORE», «The best pirate game…»): elegir tramos entre tarjetas y
  revisar el FINAL del clip.
- Wikimedia: 429 con originales en ráfaga y 400 «use thumbnail sizes»: pedir `pithumbsize=960` / `iiurlwidth=960` y pausas.
- `armar_musica_ost.py`: una sección con varias pistas solo suena la primera si cabe; para cambiar de juego, corte por beat.
- E: casi lleno (1,9 GB): salida/ y segmentos/ de este video pasaron de junction a carpetas reales en C:.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal, miniatura y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [ ] visto bueno del usuario · limpiar · `biblioteca sfx catalogar` (sin SFX nuevos) · HALLAZGOS al doc de estilo
- [ ] registro a 7 días en canales/formula/cronicas_gaming.md
