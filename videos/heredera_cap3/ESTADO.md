# La heredera del rancho · Capítulo 3 «¿Quién está en la tumba?» — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: página de Facebook «Lágrimas y Venganza» (`novelas_ia`; E:\PaginaFace --pagina novelas_ia) · cap. 3 de la serie
- estilo: novela con IA = secuencia Flow realista con diálogo y lipsync, PRIMER CAP. CON «NOVELA, NO TRÁILER» → docs/formato_novela_ia.md
- etapa: ✅ CAP. 3 PUBLICADO en FB (23-oct, fb_id 1781596886433014, https://www.facebook.com/reel/1781596886433014/)
- siguiente: capítulo 4 «¿Dónde está Carmen?» (nueva carpeta `heredera_cap4`; copiar guion.py con `_PUESTAn`; ver la biblia del
  docstring) con la receta «NOVELA, NO TRÁILER» + puntos 8-9 de docs/formato_novela_ia.md

## Sesiones (plan de tramos · «continúa el video heredera_cap3» retoma aquí · protocolo docs/sesiones.md)
- alias: heredera cap 3, capítulo 3 de la heredera, heredera_cap3
- leer al empezar: este ESTADO + docs/formato_novela_ia.md § «NOVELA, NO TRÁILER» y § «Serie de muchos capítulos» + ESTADO de heredera_cap2
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion con la receta nueva (reprise + 3 escenas + 2 cortinillas), prompts | ✅ 23-oct | v2 tras «que no parezca tráiler»: 19 clips, 186 s |
| 2 | escena 1 (clips 2-6) en Flow → prueba de continuidad con la reprise; luego clips 7-19 (total ≈ 122 pts) + descarga 720p | ✅ 23-oct | 19 clips; repetidos 5 (cuarto claro), 18-19 (política, escopeta) y 14 (monólogo inventado) ≈ 117 pts en total |
| 3 | Flow Music, efectos.py (ambiente por escena), SFX, fx → música → video → mezcla (≥ 15 dB) → final → revisión → FB | ✅ 23-oct | aprobado por el usuario y publicado al momento: https://www.facebook.com/reel/1781596886433014/ |

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- guion.py escrito (biblia actualizada en el docstring; gancho del cap. 4 «¿Dónde está Carmen?»). tiempo/beats/prompts ✅.
- medios/scene-001.mp4 = copia de heredera_cap2/medios/scene-013.mp4 (reprise, 0 pts). NO lanzar el clip 1 en Flow.
- El usuario (23-oct): «asegúrate que parezcan escenas de novela, no un tráiler o escenas aisladas casi sin conexión». Guion v2:
  escenas de 50-56 s (1 línea por clip + reacción + silencios), cada escena termina en la decisión que causa la siguiente
  («Hoy no, nos está mirando» → «mañana la tapan con cemento» → «Entonces es esta noche»), cortinilla 2 = Valeria vigilando
  desde el balcón (ata las escenas), puesta en escena fija `_PUESTAn` repetida en cada clip, todos los que la puesta nombra van
  de ingrediente (máx. 3 por clip).
- Escenas: 1 capilla misma noche (clips 2-6, 10-60 s) · cortinilla amanecer (7) · 2 cocina amanecer (8-13, 68-124 s) ·
  cortinilla Valeria en el balcón (14) · 3 capilla, abren la tumba (15-19, 132-182 s) · «Continuará…» 182-186.
- Ingredientes: misma imagen de escenario por escena (capilla y cocina del cap. 2), personajes de Flow. Cortinilla 7 sin
  personajes. Música por tramos en `MEZCLA["musica_curva"]`; ambiente de cuarto continuo por escena en efectos.py (`PISTAS`).
- ✅ 23-oct: clips 2-6 LANZADOS en Flow (navegador integrado, 9:16 · 360p · 10 s, Omni 1.1 Flash, 35 pts). OJO: el ajuste
  venía en 16:9: comprobar «crop_9_16» en «Activador de ajustes» antes de lanzar. Ingredientes por JS (`__addIng`: clic en la
  opción «<nombre> | Imagen/Personaje» basta, ya no hay botón «Añadir a petición»); clic real en «Iniciar generación».
  ✅ bajados 720p a medios/scene-002..006 SIN Chrome: en el editor del clip, menú «Descargar» → «720p» lanza el reescalado y
  la página pide `flow-content.google/video/<id>_720p_upsampled?Expires…&Signature…` (URL firmada pública) → gancho en
  `window.fetch` que la guarda (`__urls`) → curl. Whisper: las 5 líneas exactas.
  Revisión (previews/prueba_escena1_hoja.jpg): cobertura de novela OK (PP Leonor → contraplano Lupe con Emiliano detrás, OTS),
  pero el clip 5 salió en un cuarto CLARO de paredes amarillas → repetido con «same dark night chapel… NOT a bright room»
  (viejo en previews/scene-005_v1_cuarto_claro.mp4). Clip 3: el fondo de Lupe parece patio con arcos (leve, se deja).
- ✅ 23-oct clips 7-19 lanzados y bajados (720p). Flow RECHAZÓ por política el 18 y el 19 (Chuy apuntando la escopeta a la
  cara): repetidos con la escopeta «pointed at the floor» / «across his chest, NOT aiming it at anyone» y pasaron.
  Whisper: Flow INVENTA líneas en planos sin diálogo o al inicio: 7 voz en off («La tierra no olvida…») → audio silenciado;
  14 monólogo de Valeria en primer plano → repetido con «her lips stay closed… No dialogue, no voice-over»; 17 «Tenemos que
  abrirla ahora» (plano general) → 0-2,4 s silenciados; 11 «No podemos confiar en ellos» (encaja, se deja). Originales en
  previews/originales/. Final del 12 corta 2 s a un fogón con otras personas (revisar al montar; recortar si estorba).
  OJO usuario: las descargas del navegador integrado abrían VENTANAS DE GUARDADO → se bloquea `HTMLAnchorElement.click` en la
  página (la URL firmada ya llega por el gancho de fetch); no usar el menú de descarga sin ese bloqueo.
- ✅ efectos.py: ambiente de cuarto continuo por escena (capilla_noche, amanecer, cocina, patio_noche) + latido + golpe_final
  + rótulos («En el capítulo anterior…», título, «Continuará… Capítulo 4: ¿Dónde está Carmen?»); 6 SFX nuevos, 790 créditos
  (cuenta 3; las cuentas 1 y 2 ya en 0).
- ✅ música: Flow Music «Telenovela Ep 3 Score» (181,4 s; id 60799cc4…, wav público) → audio/flowmusic_cap3.wav (+ toma alt
  aaed571b… 149,7 s sin usar). audio/musica.wav = 0-143,1 s + fundido 3 s + 132,5-… de modo que el golpe final de la pieza
  (174,0 s) cae en 181,6 («Continuará…»); el golpe grande (168) cae en 175,6, justo tras «mi hermano fue por tu madre».
- ✅ render 148 s · mezcla −14 LUFS, −1,7 dBTP, diálogo/música 25,2 dB · final + verificar (desfase 0 ms).
  `final` NO genera el .srt en modo novela (salió vacío): hecho clip por clip con Whisper desplazado al inicio de cada beat
  (scratchpad srt_cap3.py; 25 líneas; sin el 7 ni la línea inventada del 17). Rótulos revisados a tamaño completo (previews/rotulos.jpg).
- Prueba de continuidad tras la escena 1: hoja de los 6 clips + verlos seguidos. Si saltan (sitio, luz, linterna): probar en
  Flow el modo «Fotogramas» con el último cuadro del clip anterior como primer cuadro (ver si conserva la voz del personaje).

## Lecciones de este video (solo lo no obvio)
- La receta anti-tráiler funcionó (el usuario aprobó escena 1, corte crudo y MASTER sin cambios): puesta fija `_PUESTAn` +
  todos los nombrados como ingrediente + cada escena termina en la decisión que lleva a la siguiente.
- Probar UNA escena antes de gastar el resto: cazó el clip 5 en un cuarto claro (7 pts) antes de lanzar los otros 13.
- Flow inventa líneas (voz en off en planos sin gente, monólogos, frases al inicio): Whisper a TODOS los clips antes de montar.
- Flow rechaza «apuntar un arma a la cara de alguien»: el arma hacia el piso o cruzada al pecho pasa y la escena no pierde fuerza.
- Descarga 720p sin Chrome y SIN ventanas: gancho en `fetch` para la URL firmada + `HTMLAnchorElement.prototype.click` anulado.
- `final` deja el .srt VACÍO en modo novela: hacerlo clip por clip con Whisper (scratchpad srt_cap3.py).

## Cierre (regla del 12-oct-2026)
- [x] publicado en FB «Lágrimas y Venganza» (tipo `video`) y registrado (BITACORA, fb_log.jsonl)
- [x] HALLAZGOS de la receta nueva documentados en docs/formato_novela_ia.md
