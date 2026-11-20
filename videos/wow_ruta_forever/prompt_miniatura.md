# Miniatura — wow_ruta_forever (19-nov-2026, Flow Nano Banana 2.1, Imagen · 16:9 · Alto · x2, 0 puntos)

Título: «La RUTA del 1 al 60 en WoW Forever, zona por zona». La miniatura no repite el título: solo «1 → 60» + logo.
Proyecto de Flow: https://flow.google.com/project/e2c946ad-b54a-4f37-8403-e8782e2d0325 (los 4 ingredientes ya están subidos ahí:
para reintentar, «Añadir ingredientes» del cuadro del prompt → orden 1-2-3-4, sin volver a pegarlos).

Ingredientes (pegado sintético `ClipboardEvent('paste')` en `.ProseMirror` del navegador integrado, uno por llamada, en este orden):
1. `i.ytimg.com/vi/ju5Tc0pqtbg/maxresdefault.jpg` (miniatura aprobada «25 ERRORES» del canal): estilo de letras, logo WoW Forever y el orco in-game.
2. `mapas/mundo_forever_ancho.jpg` (mapa mundial real de Wowhead Forever: Kalimdor, Zephras, Reinos del Este) → `miniatura_ing/ing1_mapa.webp` 768x432, pegado en base64 y reescalado x2 por canvas.
3. `pegatinas/claros_rio.png` (Claros del Río, galería de Forever en warcraft.wiki.gg) → `miniatura_ing/ing2_claros_rio.webp` 400x225 (x2).
4. `pegatinas/monte_hyjal.png` (Monte Hyjal, galería de Forever) → `miniatura_ing/ing3_monte_hyjal.webp` 400x225 (x2).
(wiki.gg no tiene CORS y el integrado bloquea 127.0.0.1: por eso las locales van en base64 pequeñas.)

## Prompt

```
YouTube thumbnail 16:9 for a World of Warcraft Classic video about the leveling route from level 1 to 60. Keep the exact in-game World of Warcraft Classic graphics of the ingredients (game screenshot look, painted textures, in-game character models); NOT a 3D animated movie, NOT Pixar, NOT clay, NOT cinematic CGI, NOT modern retail WoW, do not redraw the faces. BACKGROUND = image 2: the real World of Warcraft world map (Kalimdor on the left, Eastern Kingdoms on the right, the small island in the middle) filling the whole frame, turned into an old in-game parchment map: warm aged paper edges, sepia sea, soft vignette, same continent shapes and zone colors as image 2. ROUTE: a thick glowing GOLDEN DOTTED LINE with small footprints that snakes across both continents, starting at a round golden map pin labeled "1" in the south of the Eastern Kingdoms (right), zig-zagging north and across the sea to Kalimdor, and ending at a big shining golden flag pin labeled "60" in the north of Kalimdor (left), with a bright sparkle. Along the route, two round gold-framed picture pins: one with the river landscape of image 3 (stone tower over a blue river) in the middle of the route, and one near the "60" end with the purple glowing forest of image 4. CHARACTER: the orc warrior from image 1, exact in-game model, big in the lower right corner seen from behind over the shoulder (three-quarter back view), looking left along the golden route toward the "60" flag, one hand shading his eyes. TEXT (bold, eye-catching YouTube thumbnail lettering, same style as image 1, thick black outline and drop shadow), in the upper left over the sea, exact, render perfectly, no extra words: huge yellow (#FFE21E) "1", a big white arrow "→", huge yellow (#FFE21E) "60" — read as "1 → 60". LOGO: the "World of Warcraft FOREVER" logo exactly as in image 1, small, bottom-left corner. Use nothing else from image 1 (no "25", no "ERRORES", no tooltip, no red sentence, no background). No watermark, no other text, no zone names, no spelling mistakes, sharp text.
```

## Resultado (19-nov-2026)
- A la primera, SIN bloqueo de «actividad inusual»: x2 en ~30 s, 1376x768, 0 puntos. Descarga: URL firmada `flow-content.google/image/…`
  de la respuesta del POST `batchexecute?rpcids=ogiZ0b` (`read_network_requests`) → curl, sin ventanas de guardado.
- `miniatura_ing/opciones/flow_a.jpg`: ruta punteada fina, «1→60» algo más chico, orco con la piel muy amarilla.
- `miniatura_ing/opciones/flow_b.jpg` ← **ELEGIDA**: «1 → 60» enorme (amarillo + flecha blanca, contorno negro), ruta dorada gruesa
  del pin «1» (sur de los Reinos del Este) a la bandera «60» (norte de Kalimdor), medallones de Claros del Río y Monte Hyjal, orco
  de espaldas mirando la ruta, logo WoW Forever abajo a la izquierda. Sin faltas ni texto extra. Se lee a tamaño celular (`miniatura_ing/_celular_ab.jpg`).
- `salida/miniatura.jpg` = B a 1280x720 (335 KB). Pendiente: subirla con el video (`yt subir` la toma sola) o `yt aplicar` si ya está subido.
