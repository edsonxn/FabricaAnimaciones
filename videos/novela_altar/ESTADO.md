# La muerta en el altar · Capítulo 1 — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: página de Facebook «Lágrimas y Venganza» (`novelas_ia`, creada el 23-oct-2026; arte y datos en canales/arte/novelas_ia/LEEME.md; token listo para publicar por API) · meta: publicar antes del 1-nov-2026 (Día de Muertos)
- estilo: novela con IA = secuencia Flow realista con diálogo y lipsync → docs: docs/formato_novela_ia.md + docs/estilo_secuencia_flow.md
- etapa: prompts 10/10 · hojas de personaje en Flow
- siguiente: en Flow (navegador integrado) mirar saldo, hacer hojas de los 5 personajes + sala con ofrenda (imágenes, 0 pts), luego clip de prueba 1

## Sesiones (plan de tramos · «continúa el video novela_altar» retoma aquí · protocolo docs/sesiones.md)
- alias: novela, la muerta en el altar, novela_altar, piloto de novela
- vista previa: con audio completo antes de cerrar (regla 13-oct)
- leer al empezar: este ESTADO + docs/formato_novela_ia.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion, PLANOS, prompts; hojas de personaje; clip de prueba | ◐ parcial | 23-oct: guion y prompts listos |
| 2 | 10 clips Veo/Omni 360p con diálogo → revisión → voces fijas (STS) | pendiente | |
| 3 | música (biblioteca/Lyria), SFX, rótulos, mezcla, render, final | pendiente | |

## Decisiones del episodio (el usuario, 23-oct-2026)
- duración ~92 s · TODO video (10 clips: 4 de 8 s + 6 de 10 s) · 360p + descarga «720p mejorada» · vertical 9:16
- estilo realista de telenovela (lo recomendé por datos: el viral de 2 M a 177× es realista)

## En curso (checkpoint)
- Flow (saldo 924 pts el 23-oct): proyecto https://flow.google.com/project/31c0c36e-98b3-485c-a710-ae9e3b2d31a5
  con 5 PERSONAJES de Flow («Caracteres»: retrato + cuerpo + VOZ fija): Ximena=Vindemiatrix, Doña Refugio=Gacrux,
  Mauricio=Alnilam, Daniela=Autonoe, Sofi=Leda. Imagen de la sala «Empty ofrenda altar with candles» (ingrediente).
  Clip 1 de prueba OK (medios/scene-001.mp4, 720x1280, Whisper exacto; defecto: vestido amarillo y venda alrededor).
  23-oct ~08:35: lanzados clips 2-10 + repetición del 1 con ingredientes. En medios/ (720p, Whisper EXACTO en todos):
  1-8 y 10. Buenos: 3,4,5,7,8,10. ~09:05 repeticiones lanzadas: 1 (vestido amarillo), 2 (Mauricio sin barba),
  6 (texto «ARRI ALEXA 350» quemado: NO poner «shot on ARRI Alexa» en el prompt), 9 (falló por política).
  Descargas SIEMPRE en el Chrome del usuario (autodescarga a E:\Downloads_jaire con el título del clip).
  ~09:15 ✅ LAS 10 TOMAS en medios/ (las elegidas; descartes en medios/_ronda1/). clips_s reales = 94 s, timeline 96 s.
  ~09:25 efectos.py (5 rótulos, 4 FX, 7 SFX ElevenLabs = 215 créditos, audio/fx.wav). Lyria API sin saldo (402) →
  música de biblioteca `la_sena__lyria_tramo3` (sin usar en ningún canal) → audio/musica.wav. Render `video` lanzado.
  ~09:50 ✅ MASTER salida/la_muerta_en_el_altar_cap1_MASTER.mp4 (1080x1920, 99 s, −14,3 LUFS) + .srt por Whisper
  (15 líneas). Revisado cada 3 s: sin negros, personajes consistentes. Arreglos: título en 2 renglones, sin destello,
  final alargado a 99 s (congela a Mauricio con «Capítulo 2»), `dialogo=True` ⇒ clips a 1,0× (nucleo/secuencia.py).
  ✅ 23-oct-2026 ~15:40: el usuario lo vio y aprobó → PUBLICADO en la página FB «Lágrimas y Venganza» (tipo video, 99 s,
  fb_id 4094617344177384): https://www.facebook.com/reel/4094617344177384/ (post en E:/PaginaFace/paginas/novelas_ia/posts/).

## Hecho
- `guion.py`: SIN_VOZ + `dialogo=True` (nuevo en `nucleo/secuencia.py`: no añade «sin diálogo»; PLANOS admiten `dialogo`,
  `objetos` y `escenario` propio). 10 PLANOS con diálogo en español, FICHA de 5 personajes + 4 objetos ancla, ROTULOS, LYRIA.
- `tiempo` (31 compases = 93 s) → `beats` (10 clips) → `prompts` (flow/escenas.json).

## Falta
- [ ] Hojas de personaje (frente/perfil/cuerpo) + sala con ofrenda en Flow, a `flow/hojas/`
- [ ] Clip de prueba (clip 1): ¿habla bien en español mexicano? ¿acepta ingredientes en video?
- [ ] Lote de 10 clips, revisión de consistencia (cara, ropa, anillo)
- [ ] Voz constante por personaje (ElevenLabs speech-to-speech, a probar)
- [ ] Rótulos en efectos.py, música, SFX, mezcla, render, verificar

## Archivos clave
- `guion.py` (FICHA + PLANOS con diálogo), `beats.json`, `prompts.json`, `flow/escenas.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- Flow (oct-2026) tiene **Caracteres**: personaje reutilizable con retrato, cuerpo y VOZ (voces Gemini: Achernar…Zubenelgenubi).
  Crear: /project/<id>/character → describir → Return; nombre con «Editar nombre»; voz: «Selecciona una voz» → buscar →
  clic en la voz (a veces la añade sola; si no, «Añadir al personaje»); «Crear cuerpo» → describir ropa → Return.
- Para un clip: «+» del cuadro de petición → el personaje es un `button[role=option]`: el clic del ratón NO lo añade, hay
  que `.click()` por JS. Ajustes (chip a la derecha): Vídeo · **Ingredientes** · 9:16 · Omni 1.1 Flash · 360p · 8 s = 6 pts
  (10 s = 7). Texto con `execCommand('insertText')` y `key Return` real. Capturas a escala 1 (con 0.6 las coordenadas fallan).
