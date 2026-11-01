# Guía de estudio entrevista IEEZ (Consejos Distritales y Municipales) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: ninguno (video personal de estudio del usuario, NO va a YouTube) · entrevista el 21-oct-2026 por la tarde
- estilo: fichas y diagramas por código (PIL, `escenas.py` propio, 16:9, 24 fps) · sin doc de estilo propio
- etapa: entregado (MASTER 14:20 + MP3 en salida/)
- siguiente: nada; tras la entrevista, `python fab.py guia_ieez limpiar`

## Sesiones
- alias: «guía IEEZ», «video de estudio», «entrevista del Instituto Electoral»
- vista previa: no (entrevista hoy: entregar completo en esta sesión)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz + escenas + música + render + entrega | ✅ 21-oct | un solo video de ~12-13 min pedido por el usuario |

## En curso
- (nada en curso)

## Hecho
- Guía leída (`Descargas/GUIA DE ESTUDIO PAG WEB.pdf`): 3 preguntas (10/5/0, 30 % + 10 % curso) + 5 competencias STAR (20 %).
- Leyes oficiales descargadas de los enlaces de la guía y artículos citados extraídos (scratchpad de la sesión): CPEUM, Const. Zacatecas,
  LGIPE, Reglamento de Elecciones, Ley Electoral de Zacatecas, Ley Orgánica del IEEZ. Todo dato del guion sale de ese texto.
- Técnicas: pregunta → reloj (pausa 5 s / 3,2 s) → respuesta con fundamento; casos hipotéticos; mnemotecnias; bloques con barra de
  avance; tarjeta sincronizada con la palabra; simulacro final de 10 preguntas; tic-tac y campana (`fx_audio.py`) para estudiar solo escuchando.

- Entrega 21-oct 12:11: MASTER 1080p 24 fps 859,75 s, -14 LUFS, voz/música 23 dB; Lyria 6 tramos (el 6.º salió largo: recortado con fundido).
  `verificar` (Whisper del video entero) NO se corrió por tiempo; cada frase ya pasó Whisper en `seleccionar`. Hoja: previews/rev/hoja_master.jpg.

## Archivos clave
- `guion.py` (ESCENAS con `bloque` y `vis`), `escenas.py` (dibujo), `fx_audio.py` (tic-tac/campana → audio/fx.wav)

## Lecciones de este video (solo lo no obvio)
- `BPM = 480` en un video sin música procedural deja las escenas a 0,5 s en vez de 2 s (ahorró ~45 s aquí).
- 13 400 caracteres ≈ 16 min con ElevenLabs v4: para 12 min de guía con pausas, ~10 500 caracteres.
- Guía del IEEZ: los cómputos municipales los atribuye por error a la LGIPE (arts. 265-270); son de la Ley Electoral de Zacatecas.
