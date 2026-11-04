# El Carpintero que lo Perdió Todo… e Inventó LEGO — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: pieza_oculta · SUBIDO y PROGRAMADO vie 6-nov-2026 13:00 CDMX (wCQ8VVbcbgk)
- estilo: secuencia_flow (plastilina, clips e imágenes de Google Flow) + capa de pegatinas/fotos/MG → doc: docs/estilo_secuencia_flow.md
- etapa: ✅ subido (MASTER 9:13, 1080p) · falta solo el .srt a mano en Studio y el visto bueno del usuario
- siguiente: si el usuario pide cambios → `video --rehacer t0-t1` + `final` + reemplazar en Studio antes del vie 13:00; al aprobar: `fab.py lego_carpintero limpiar`

## Sesiones (plan de tramos · «continúa el video lego_carpintero» retoma aquí · protocolo docs/sesiones.md)
- alias: LEGO, el carpintero, Ole Kirk, el 3 de la tanda de Plastitube
- vista previa: no; el usuario revisa en 🎞 Montaje del panel
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion → voz → beats → prompts | ✅ 4-nov | guion (18 escenas, 122 frases) con ficha verificada; voz 122/122 (Dan, Chatterbox) |
| 2 | Flow: 18 clips (3 min) + imágenes · pegatinas reales + MG | ✅ 4-nov | 18 clips 720p (letterbox en recorte_por, scene-016 sin ambiente), 76 imágenes, fx hoja y vivo revisados |
| 3 | vivo → armado → Lyria → mezcla → final → subir | ✅ 4-nov | Lyria nueva 5 tramos; render 21 min; −14 LUFS, voz +12,7 dB; CER 0,25 %; subido privado programado |

## Decisiones del episodio (3-nov-2026)
- tema: 3.º de la tanda (el usuario: «Short + LEGO»); ~9-10 min
- minutos iniciales en video: **3 min (el usuario)** = 18 clips combinados de 10 s, 360p + descarga 720p mejorada (126 de 433 puntos; se renuevan el 22-nov).
- **capa de pegatinas, fotos reales y animaciones encima (el usuario, 3-nov): en los 3 min de CLIPS, ligera (~1 cada 30-40 s, 1/3-1/2 de
  pantalla); en la parte de SOLO IMÁGENES, MÁS densa (pegatinas, fotos, MG, vivos) «para hacerlo dinámico»** → 41 efectos + 14 rótulos + 8 vivos.
- carpetas pesadas en C: (E: falló el 3-nov 16:39)

## Hecho
- 3-nov: guion.py con ficha histórica verificada (Wikipedia, lego.com, prensa de Nuevo León); 14 fotos reales de Commons en pegatinas/;
  kit NUEVO nucleo/mg_plasti.py (linea/contador/ladrillos) y tema "plasti" en peg_estilos; efectos.py.
- 4-nov: voz; 76 imágenes (Nano Banana 2.1, proyecto Flow 5420900a-…) + 18 clips (proyecto 60843ab2-…, Omni 1.1 Flash 360p → 720p);
  scene-055 bloqueada por el filtro (niños arrodillados) → rehecha sin niños; scene-060 rehecha.
- 4-nov: Lyria nueva (biblioteca solo daba Plastitube = mismo público); render, mezcla, final, verificar; miniatura Flow (Ole Kirk 1957 PD +
  ladrillo 2x4 CC0 de ingrediente); youtube.json con 17 capítulos y créditos; subido wCQ8VVbcbgk; registrado en canales/pieza_oculta.json y BITACORA.

## Lecciones
- **Dos sesiones sobre el mismo video a la vez** (sopa-short abrió una continuación mientras la sesión «lego» seguía viva): se repartieron
  sin pisarse por suerte. Antes de producir, `list_sessions {"linked": true}` y procesos `fab.py <v>`; si otra sesión lo lleva, retirarse.
- **`yt subir` marcaba «promoción pagada»** porque la descripción decía «no está patrocinado ni avalado» (aviso de marca): arreglado en
  nucleo/youtube.py (ignora «no (está/es) patrocinado») y desmarcado en el video. Revisar el aviso en cualquier video con marca registrada.
- C: se llenó a mitad (TEMP 12,5 GB): mirar espacio libre antes del render (~1,5 GB por cada 3 min).

## Falta
- [ ] .srt a mano en Studio (token sin force-ssl) · [ ] visto bueno del usuario · [ ] `limpiar` al aprobar
