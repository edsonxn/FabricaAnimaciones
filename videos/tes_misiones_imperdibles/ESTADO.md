# Las 25 misiones de Skyrim que NUNCA debes saltarte — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · PROGRAMADO sáb 07-nov-2026 12:08 CDMX (2026-11-07T18:08:00Z) · https://youtu.be/xnOdTqaZWrM (privado)
- estilo: secuencia_yt (gameplay Skyrim por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · voz Chatterbox Sarcastica · música OST oficial de Skyrim → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: subido y programado (29-oct-2026) · FALTA: monetización en Studio (anuncios + mid-rolls + cuestionario «Nada de lo anterior»)
- siguiente: revisión del usuario; activar monetización en https://studio.youtube.com/video/xnOdTqaZWrM/monetization ; al publicarse, `canales --actualizar`

## Sesiones (plan de tramos · «continúa el video tes_misiones_imperdibles» retoma aquí · protocolo docs/sesiones.md)
- alias: misiones imperdibles, 25 misiones, no saltarte · vista previa: ninguna (el usuario: directo al MASTER, aviso al tenerlo)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 28-oct): UESP + guion + voz + beats + clips + pegatinas + MG + mapas + OST + mezcla + render + rigor + miniatura + subida | ✅ 29-oct | 23:14 con pantalla final; subido y programado sáb 07-11 |

## Decisiones del episodio (28-oct-2026)
- tema elegido por el usuario entre 3 con datos: «Las 25 misiones de Skyrim que NUNCA debes saltarte». Repite el ganador
  (tes_misiones_nunca: 22 117 vistas en < 7 días, ×10 la mediana de 2 220) y cambia UNA variable: la polaridad (las que SÍ hacer).
- duración: 22 min pedidos (salió 22:55 de voz + 20 s de pantalla final). Excluido lo ya salido en el canal.
- Comentarios: gancho = @sebastiannarvaez6185 (♥11) + @EnriqueJVidal-ei1nk; queja ♥7 «Oblivión» → FONETICA «Oblívion» y tarjeta
  en el n.º 23; agradecimientos @amadeoamaya7606, @marcocho_23, @franzindriago7950, @edupiles8494, @KRONOX-LEGEND (8 tarjetas reales).
  Voz IA / «habla más calmada» / acento mezclado → reportado al usuario, no se cambia.
- formato: `lista_25_misiones_imperdibles_secuencia_yt` · fecha: 96 h tras cosas_nunca (03-11) → sáb 07-11 18:08Z.
- disco: E: dio NTFS 55 el 28-oct 10:18; C: se llenó a mitad de `bajar` (otra sesión) → carpetas pesadas en E: con junctions.

## Hecho
- 25 misiones verificadas en UESP (3 subagentes) · guion 188 frases · voz 188/188 · 160 beats · 160 clips (~100 rehechos en 6 vueltas)
- 3 MG nuevos en mg_tes (inversion, versiones, fragmentos) + 2 mapas reales con fotos (Kyne, Gauldur) · 85 pegatinas + 8 comentarios
- OST: 18 pistas nuevas de Jeremy Soule + 6 reutilizadas (armar_musica_ost.py, 27 secciones) · sonido original en 4 beats
- mezcla −14 LUFS, voz 13 dB sobre música · MASTER 1394 s · blackdetect: 3 negros arreglados con `video --tramo` + `_empalme.py`
- miniatura Flow v1 · .srt · youtube.json (capítulos, créditos de 109 canales) · subido privado + programado · BITACORA, publicados, panel

## Cómo retomar (comandos)
```
python fab.py continuar tes_misiones_imperdibles
```

## Lecciones de este video (solo lo no obvio; detalle en docs/estilo_secuencia_yt.md § Tamriel)
- Investigar con subagentes en paralelo: 25 misiones verificadas en ~30 min; cazaron 2 errores del brief.
- `ambiente_por` + `+ba` = clips cortos: rebajar sin audio con la misma url/desde; `_chequeo_clips.py` los caza.
- `final` borra video_sin_audio.mp4: con `FAB_CONSERVAR=1` o empalmar sobre el MASTER (`_empalme.py`).
- La hoja de 2 cuadros no ve el final de beats largos: `fx hoja` + blackdetect del MASTER siguen siendo necesarios.
- En Studio, el filtro de permisos frenó un clic por JavaScript para activar los mid-rolls: la monetización queda para el usuario.
