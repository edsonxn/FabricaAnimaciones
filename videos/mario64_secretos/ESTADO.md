# Super Mario 64: su historia y los 20 secretos QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco dom 8-nov-2026 18:00 CDMX (ciclo 3 d) · gancho = 30 años + la placa «resuelta» (oct-2026)
- estilo: secuencia_yt + kit NUEVO `nucleo/mg_mario64.py` (diálogo translúcido, selección de estrella, HUD, 7 MG) + tema de mapa `mario64` + pegatinas + OST oficial + SFX del juego · voz ElevenLabs Hope (`eleven_v4_turbo`) → doc: docs/estilo_secuencia_yt.md § Crónicas del gaming
- etapa: ✅ SUBIDO en privado y PROGRAMADO dom 8-nov-2026 18:00 CDMX: https://youtu.be/-pXDdmgtvPQ · MASTER 21:24 · falta el visto bueno del usuario
- siguiente: revisión del usuario; si pide cambios, `video --rehacer t0-t1` + `final` + reemplazar la subida

## Sesiones (plan de tramos · «continúa el video mario 64» retoma aquí · protocolo docs/sesiones.md)
- alias: mario 64, super mario 64, video de mario, mario64_secretos
- vista previa: ninguna; directo al MASTER y aviso (el usuario, 29-oct)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 29-oct) | ✅ 30-oct | detenido a mitad el 29-oct y retomado en el tramo 2 |
| 2 | plan de clips → bajar → medios + brillo → fx hoja → ambiente → mezcla → video → final → verificar → subir | ✅ 30-oct | 22 clips rehechos, 133 efectos, 13 con sonido del juego; MASTER subido |

## Decisiones del episodio (29-oct-2026, el usuario)
- Tema elegido entre 3 con datos (Mario 64 historia + 20 secretos / Ocarina 15 misterios / historia de Smash): **Mario 64**.
  Variable que cambia: SOLO el juego (fórmula de zelda_oot/majora_mask). Ref.: Nachotaro ×3,5, TheNoob ×3,7.
- 22 min, una sesión, sin vista previa. Comentarios (29-oct): 0 nuevos, sin quejas (1 en 21 días): sin capturas de
  agradecimiento; la voz dice que se leen todos.

## Hecho
- fuentes_guion.md (agente + comprobación propia: TTC 12/3/6/9 en Super Mario Wiki; placa «Eternal Star» en 5 medios).
- Guion 156 frases; voz 156/156 (≈ 3 600 créditos, cuenta 2; CER_MAX_POR_FRASE para nombres); tiempo 21:24 + pantalla final.
- beats.json (149) + beats_texto.txt. efectos.py: 133 FX (20 rótulos de estrella, fichas, ~60 pegatinas, 9 mapas con ruta,
  MG mando/reloj_ttc/agua/boton_a/bit/estrellas/linea_tiempo), anclas validadas con `fx --seco`; 34 SFX del juego (sfx/m64_*).
- Mapas de VGMaps en mapas/ (castillo, JRB, CCM, HMC, TTC, WDW) con rejillas. Pegatinas: 67 en pegatinas/ (mosaico revisado).
- audio/musica.wav armado (armar_musica_ost.py, 21 secciones); REHACER tras fijar ambiente_por.
- Miniatura Flow variante B en salida/miniatura.jpg («¿LUIGI ERA REAL?», prompt_miniatura.md). youtube.json con capítulos
  (falta añadir los créditos de clips de salida/creditos.txt tras `fuentes`).

## Lecciones de este video (solo lo no obvio)
- `verificar`: los avisos de CER (Waiko Izumi, Swiggy, Panacook, TikTok Clock) son Whisper con nombres propios, no la voz. Negro 891,3-892,9 = crédito de Goddard, a propósito.
- 3D All-Stars NO trae Mario 64 en español: los nombres oficiales en español son los de Super Mario 64 DS.
- Super Mario Wiki (mariowiki.com) deja usar su API y mario.wiki.gallery tiene CORS abierto (collage en canvas dentro de Flow).
- Wikipedia «Giles Goddard» es OTRA persona (un sacerdote): mirar siempre el mosaico de pegatinas.
- Mapas de Mario 64: los del DS en la wiki son de 128-255 px; VGMaps (Atlas/N64) los tiene de 2-3 k px con rótulos.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
