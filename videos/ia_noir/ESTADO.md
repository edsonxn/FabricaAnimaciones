# El caso de la máquina — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia · PUBLICADO (público) 6-oct-2026 ~10:47 CDMX (eZlZRGf3VC0) — título «Por qué la IA podría DESTRUIR a la humanidad»
- estilo: noir (NUEVO: cine negro en tinta y aguada B/N) → kit nucleo/noir*.py · doc de estilo: docs/estilo_noir.md (pendiente)
- etapa: publicado (verificado en YouTube 6-oct-2026; a esa hora YouTube aún lo estaba PROCESANDO) · MASTER `salida/caso_maquina_MASTER.mp4` + .srt + miniatura
- siguiente: confirmar que terminó de procesar (`python fab.py yt videos logia` → «processed») y que cargaron miniatura y .srt; ver retención a las 48 h

## Hecho
- Guion 59 frases / 815 palabras (hechos verificados al 6-oct-2026 en el docstring de guion.py).
- Voz ElevenLabs «Edoardo» (voice_id YqZLNYWZm98oKaaLZkUA, multilingual v2): 59/59 frases CER ≤ 0,016; 1.928 créditos. Tiempo 358,6 s (84 BPM, GAP 0,55).
- Kit noir: Noir (claroscuro multiplicativo, capa emisiva, capa aditiva de lluvia/humo, niebla volumétrica, tinta, papel, grano, polvo),
  pieza() con tramado de plumilla y contraluz, Detective / Busto (primer plano) / Frontal (reparto), fondos pintados (ciudad, interiores),
  clip_noir (video real entintado), transiciones por planos (barrido, empuje, tinta, relámpago, humo).
- 34 clips de Pexels en clips/ (E:), créditos en clips/creditos_clips.json.

- 10 escenas (esc_*.py), comprobar ✓; SFX: 554 eventos / 134 sonidos (nucleo/sfx_noir.py); música Lyria 3 tramos (_lyria_segmentos.py);
  mezcla −14,06 LUFS, pico −1,05 dBTP, voz +12,7 dB; youtube.json; prompt_miniatura.md; docs/estilo_noir.md + fila LogIA en CLAUDE.md.

## Falta
- [ ] final → verificar → revisión del MASTER a tamaño completo
- [ ] pulido posible: manos (props.mano), piernas del detective de cuerpo entero
- [ ] miniatura (el usuario la genera con Nano Banana 2) → subir en privado a LogIA; el usuario decide fecha

## Cómo retomar (comandos)
```
python fab.py estado ia_noir
python videos/ia_noir/_prueba.py <escena> u1 u2 ...      (tiempos locales; hoja previews/p_<escena>.jpg)
python videos/ia_noir/_prueba_clips.py <clip> ...        (prueba del entintado de clips)
python videos/ia_noir/_hoja_global.py 3                  (un cuadro cada 3 s de todo el video -> previews/hoja_global_*.jpg)
python videos/ia_noir/_lyria_segmentos.py armar           (rehace audio/musica.wav desde los 3 tramos)
```

## Archivos clave
- `guion.py` (VOZ motor elevenlabs), `escenas.py`, `basen.py` (montaje por planos), `esc_*.py`, `mundos.py`, `props*.py`
- núcleo: `nucleo/noir.py`, `noir_pers.py`, `noir_fondos.py`, `tts_eleven.py` (clave en canales/tokens/elevenlabs_api_key.txt)

## Lecciones de este video (solo lo no obvio)
- ElevenLabs recorta la toma justo al acabar la voz: el filtro de «cola» de tts_select no aplica (TAIL_MAX=1.0 con motor elevenlabs).
- La luz MULTIPLICA el cuadro: ventanas, faroles y brasas van a la capa emisiva o quedan negras.
- Texto blanco sobre clips de papel claro no se lee: tinta oscura o doble pasada (sombra + blanco).
- El panel lee guion.py SIN ejecutarlo: ESCENAS deben ser {…} literales (con dict(...) cuenta 0 frases y el avance sale 450 %).
- Revisión del MASTER (6-oct): texto encimado en 3:04 (con zoom de cámara, `_encuadrar` empujó la 1.ª línea sobre la 2.ª → textos fijos en pantalla con `h.camara(1, W/2, H/2)`); apagón de 1:52 al 97 % = cuadro negro → 85 %. Las rayas verticales finas son el efecto de película (`_polvo`), no defecto.
- Miniatura dibujada con el kit (no IA): `_miniatura.py` → `salida/miniatura.jpg` (detective con persiana + caja negra con el ojo encendido, «¿NOS DESTRUIRÁ?»).
