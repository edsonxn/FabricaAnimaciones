# La historia de Tequisquiapan (Short vertical, 2:58) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronopapel · **PROGRAMADO sáb 24-oct-2026 10:00 CDMX** (https://youtu.be/OfGVLuL490w, publishAt 2026-10-24T16:00:00Z, #Shorts) · Facebook «Historias Perdidas de México» PUBLICADO 22-oct (fb 1587120085964812)
- estilo: boceto → doc de estilo: docs/estilo_boceto_guache_mapa.md § «Variante VERTICAL con mapa (tequisquiapan)» · kit de videos/historia_aguascalientes/
- etapa: subido (privado programado) + Facebook publicado · falta el .srt en YouTube (cuota agotada el 22-oct)
- siguiente: `python fab.py yt aplicar tequisquiapan cronopapel OfGVLuL490w` (sube el .srt) · cuando salga un largo de Cronopapel público, «Vídeo relacionado» del Short en Studio · a los 7 días medir y anotar en canales/formula/cronopapel.md · al aprobar: `fab.py tequisquiapan limpiar`

## Sesiones (plan de tramos · «continúa el video tequisquiapan» retoma aquí · protocolo docs/sesiones.md)
- alias: tequisquiapan, Tequis, pueblo del Bajío, Short de 3 min de Cronopapel
- vista previa: no; el usuario eligió TODO DE CORRIDO en una sesión (22-oct-2026)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + mapa + guion + voz + Flow + coreo + sonido + render + subida + Facebook | ✅ 22-oct | una sesión; 2 subagentes (hechos+fotos, mapa) |

## Decisiones del episodio (22-oct-2026)
- pedido: «video similar [a Aguascalientes] pero vertical de 3 minutos de algún pueblo aleatorio del Bajío» → sorteo: Tequisquiapan
- reglas nuevas aplicadas: Google Maps de cada lugar en la descripción (8) + frase «te dejo en la descripción cómo llegar» + 19 fotos reales (1 cada ~9 s)
- quité «la foto aquí es obligatoria» para no pasar de 180 s (DURACION = 178,5 fija)
- NO se afirma: el decreto de Carranza (solo la placa de 1978), la cruz bajo el mezquite (tradición), «tercer monolito del mundo»

## Hecho
- `_hechos.md` + 43 fotos de Commons (`fotos/<clave>.jpg` vía `fotos/_claves.py`; `creditos.json` por clave; originales en `creditos_commons.json`)
- mapa vertical de Querétaro (700 px/°, `_mapa_notas.md`) · voz ElevenLabs Alberto 943 créditos, CER 0 · timeline 178,5 s (BPM 131,9)
- Flow: 8 prompts x2 (6 hojas + ciclos turista y jinete), variantes «a», 2K en `hd/`, piezas en `piezas/` · `coreo_1.py`, `coreo_2.py`
- SFX 44 nuevos (684 créditos) + 3 biblioteca · música de la biblioteca (Lyria API sin saldo) · mezcla −14,2 LUFS
- MASTER 1080x1920 178,5 s, CER 0,05 %, desfase 0 · rigor previews/rigorB_1-2.jpg (cuadro cada 3 s) sin bloqueos
- `youtube.json` (vía `_youtube.py`) · Facebook con `_fb_texto.txt`

## Lecciones (solo lo no obvio)
- `fab.py <v> video` tras editar la coreografía REUTILIZA `segmentos/seg_*.mp4` («listo 4s»): borrar los seg_*.mp4 (o `--rehacer`) antes.
  Y si `video` falla a medias, `final` arma el MASTER VIEJO sin avisar: mirar la fecha del MASTER.
- Kit de mapa en vertical a 700 px/°: (1) la deriva de `CamPath` de país (0,30/0,20) movía ~200 px el encuadre → 0,055/0,035;
  (2) la clave de cámara final de una escena (fin + 0,4) caía DESPUÉS de la primera de la siguiente (i0 − 0,2) y la cámara se iba
  antes de tiempo → cerrar en fin − 0,25; (3) cada frase debe arrancar con pegatina (el rigor halló 1-2 s de mapa solo en 5 sitios).
- Flow en Chrome: Ctrl+V pegó una captura vieja del portapapeles del usuario (SetImage sin persistir); usar «+» → Subir archivo
  (gancho a `input.click` + `file_upload`) y buscar el ingrediente por nombre en el selector antes de cada prompt.
- Lyria por API sin saldo (402, 22-oct) → piezas de la biblioteca NUNCA publicadas (`no_vuelve`, `la_sena`) para no repetir ante el público.
- La cuota diaria de la API de YouTube se agotó en la subida: el .srt queda para `yt aplicar` al día siguiente.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO, registrado en canales/cronopapel.json (`short: true`) y BITACORA; Facebook publicado
- [x] hallazgos en docs/estilo_boceto_guache_mapa.md · [x] biblioteca catalogar · [ ] .srt en YouTube
