# El pino azul de la Sierra de Morones — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: SIN CANAL · reel diario n.º 1 de la página de Facebook «Noticias de Juchipila» (noticias_jch, E:\PaginaFace) · sale hoy 19-nov-2026 19:00-20:00
- estilo: secuencia vertical con efectos (fotos reales de Commons + kit propio `kit_nj.py`) → docs/estilo_secuencia_fx.md + E:\PaginaFace\reel_diario.md
- etapa: PUBLICADO 19-nov 19:02 en Noticias de Juchipila (fb 1839179620463556, facebook.com/reel/1839179620463556; post 2026-11-19_1900_pino-azul-reel)
- siguiente: nada; revisar mañana vistas y compartidas (tablero de buenos días Juchipila)

## Sesiones
- alias: «el reel del pino azul», «el primer reel diario de Juchipila»
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | receta, fuentes, guion, voz, beats, medios, kit, efectos, SFX, hoja | ✅ | sesión 1 (19-nov 09:15-10:30) cortada a 180 mil tokens |
| 2 ✅ | render → mezcla → final → verificar → post → Rayo → su sí → publicar → verificar en Meta → § 5 receta + skill | ✅ hecho (19-nov 10:13-12:50) | |

## Decisiones (Edson, 19-nov-2026; anotadas en § 5 de reel_diario.md)
- Subtítulos grandes SÍ (excepción a R13 solo en esta página) · hora fija 19:00-20:00 · voz Carlos Corella `LnGOA2SxH2fX1e1iNzEp` (cuenta 4)
- PÁGINA ANÓNIMA: nada de voces, música, kits ni arte de los canales. Cama musical y SFX nuevos de ElevenLabs (`sfx/nj_*`), kit propio con colores del logo.

## En curso (checkpoint 19-nov ~10:30; MASTER 10:14, Rayo 10:23; § 5 de la receta y skill HECHOS 10:30)
- Hecho y revisado: voz (167 cr, 46,6 s, idioma OK), `tiempo` (56,7 s), `beats` (16), `_medios.py` → medios/ (recortes 9:16 de Commons), `kit_nj.py`, `efectos.py`, `fx` (10 SFX, 666 cr; audio/fx.wav), `FAB_FX_FINAL=1 fx hoja` mirada y corregida (previews/fx_0N.jpg).
- 10:35: cadena en segundo plano (espera a que acabe el render ajeno y lanza video → mezcla → final → verificar; log en el scratchpad de la sesión 1, render.log). Si la sesión se cortó, comprobar si existe salida/*_MASTER.mp4 antes de relanzar.
- Falta, en orden: (1) `python fab.py jchn_261119_pino_azul video` (en segundo plano) → `mezcla` (sin música aparte: la cama va en fx.wav; si `mezcla` pide MUSICA, revisar) → `final` → `verificar`; mirar 3-4 cuadros a tamaño real y escuchar el inicio. (2) texto del post (borrador abajo) (3) MASTER al celular por Rayo (skill `rayo`) y esperar su sí (4) con su sí: en E:\PaginaFace `python pagina.py --pagina noticias_jch nuevo <slug> --tipo reel --categoria cultura`, copiar MASTER a la carpeta del post, `medios` en post.json, `texto.txt`, `aprobar`, `programar --ya` (si es antes de las 19:00, programar a las 19:00); comprobar con GET `<video_id>?fields=status,published,length` (primer reel contra Meta). (5) añadir las fotos usadas a `vigia/fotos_usadas.json` (commons:File:… de Sierra 1-3, cono 2, Pinus_maximartinezii.jpg) y el tema a `vigia/reels.json`. (6) § 5 «Producción» de reel_diario.md con lo aprendido + paso del reel diario en `C:\Users\jaire\.claude\skills\buenos-dias-juchipila\SKILL.md`.

## Borrador del texto del post
Un pino que casi no existe en ningún otro lugar del mundo crece en la Sierra de Morones, en Juchipila. 🌲
Es el pino azul (Pinus maximartinezii): tiene las piñas y los piñones más grandes de todos los pinos piñoneros. Se calculan entre 2,000 y 2,500 árboles adultos en el Cerro de Piñones; en 2010 se encontró un segundo bosque en Durango, más chico. Hoy está en peligro de extinción por el fuego y el ganado suelto.
¿Usted ya lo conocía? Cuéntenos en los comentarios.
Fuentes: Acta Botánica Mexicana (2011) https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0187-71512011000300005 · Threatened Conifers of the World (RBGE) https://threatenedconifers.rbge.org.uk/conifers/pinus-maximartinezii
Fotos: pinidae, ferbio_dgo y Ruff tuff cream puff / Wikimedia Commons (CC BY-SA 4.0 y CC0). Mapas: © OpenStreetMap, OpenTopoMap.
#Juchipila #SierraDeMorones #PinoAzul

## Archivos clave
- `guion.py` (fuentes en el encabezado), `kit_nj.py`, `efectos.py`, `_medios.py`, `_mapa_base.py`, `fuente/fotos/creditos.json`, `arte/logo_esquina.png`
- Pieza 01 de `piezas_listas/` (misma especie, tarjeta con la foto 4): el reel NO usa la foto 4 (regla: ninguna foto se repite).

## Lecciones
- Commons: con UA genérico da 429/HTML; usar el UA de `E:\PaginaFace\fotos.py` (CommonsReuseBot) y `iiurlwidth=1600`.
- Mapa z8 se quedó corto en vertical (reflejos): base z9 grande + cámara limitada a la base (`_camara`).
- Las cifras de la voz salen en número en los subtítulos (`NUMEROS` en efectos.py).
- Rótulo con nombre propio: solo lo que dice la fuente («J. Rzedowski», no el nombre completo).
