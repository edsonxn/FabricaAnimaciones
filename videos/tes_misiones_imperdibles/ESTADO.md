# Las 25 misiones de Skyrim que NUNCA debes saltarte — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · PROGRAMADO sáb 07-nov-2026 12:08 CDMX (2026-11-07T18:08:00Z) · https://youtu.be/C16mqQHbK08 (privado)
- estilo: secuencia_yt (gameplay Skyrim por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · voz Chatterbox Sarcastica · música OST oficial de Skyrim → doc: docs/estilo_secuencia_yt.md § Tamriel
- etapa: subido y programado (29-oct-2026, 2.ª versión) · FALTA: monetización en Studio; borrar en Studio la versión vieja xnOdTqaZWrM (privada, sin programar)
- siguiente: revisión del usuario; monetización en https://studio.youtube.com/video/C16mqQHbK08/monetization ; al publicarse, `canales --actualizar`

## Sesiones (plan de tramos · «continúa el video tes_misiones_imperdibles» retoma aquí · protocolo docs/sesiones.md)
- alias: misiones imperdibles, 25 misiones, no saltarte · vista previa: ninguna (el usuario: directo al MASTER, aviso al tenerlo)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 28-oct): UESP + guion + voz + beats + clips + pegatinas + MG + mapas + OST + mezcla + render + rigor + miniatura + subida | ✅ 29-oct | 23:14; subido xnOdTqaZWrM |
| 2 | Correcciones del usuario (29-oct): faltaba la imagen de la pantalla final + mapas con ruta en ≥ la mitad de las misiones | ✅ 29-oct | 15 mapas; resubido C16mqQHbK08 en el mismo hueco |

## Decisiones del episodio (28/29-oct-2026)
- tema elegido por el usuario entre 3 con datos; repite misiones_nunca (×10) cambiando la polaridad. 22 min pedidos (22:55 + 20 s).
- Comentarios: gancho @sebastiannarvaez6185 (♥11) + @EnriqueJVidal-ei1nk; «Oblivión» (♥7) → FONETICA + tarjeta en el n.º 23;
  5 de agradecimiento. Voz IA / «habla más calmada» / acento mezclado → reportado al usuario, no se cambia.
- formato: `lista_25_misiones_imperdibles_secuencia_yt` · fecha: 96 h tras cosas_nunca (03-11) → sáb 07-11 18:08Z.
- 29-oct, el usuario: mapas con ruta en ≥ la mitad de misiones (regla nueva en el manual, también SFX del mismo juego).
  Mapas en 25, 23, 22, 21, 20, 18, 17, 16, 8, 7, 6, 5, 4, 3 y 2, con coordenadas reales de UESP (`_coords_uesp.py`).
- disco: C: se llenó a mitad de `bajar` (otra sesión) → carpetas pesadas en E: con junctions.

## Hecho
- 25 misiones verificadas en UESP (3 subagentes) · guion 188 frases · voz 188/188 · 160 beats · 160 clips (~100 rehechos)
- 3 MG nuevos en mg_tes (inversion, versiones, fragmentos) + 15 mapas con ruta y fotos · 85 pegatinas + 8 comentarios
- OST: 18 pistas nuevas + 6 reutilizadas · sonido original en 4 beats · mezcla −14 LUFS, voz 13 dB sobre música
- MASTER 1394 s (imagen y audio, pantalla final incluida) · blackdetect limpio salvo 3 parpadeos < 0,7 s · miniatura Flow · .srt
- subido + programado, BITACORA, publicados, panel · lecciones en docs/estilo_secuencia_yt.md

## Cómo retomar (comandos)
```
python fab.py continuar tes_misiones_imperdibles
```

## Lecciones de este video (detalle en docs/estilo_secuencia_yt.md § Tamriel)
- Investigar con subagentes en paralelo; `ambiente_por` + `+ba` = clips cortos; `_chequeo_clips.py` los caza.
- `final` borra video_sin_audio.mp4: SIEMPRE `FAB_CONSERVAR=1`; el empalme sobre el MASTER se comió la imagen de la pantalla final.
- Coordenadas de mapa reales: base de datos de UESP calibrada con ciudades (`_coords_uesp.py`).
- En Studio, el filtro de permisos frenó un clic por JavaScript: la monetización queda para el usuario.
