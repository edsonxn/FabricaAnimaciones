# Miniatura — wow_ruta_profesiones (25-nov-2026, Flow Nano Banana 2.1, Imagen · 16:9 · Alto · x4, 0 puntos)

Título: «La RUTA de PROFESIONES del 1 al 300 en WoW Forever». La miniatura no repite el título: «1 → 300» + «PROFESIONES» + logo.
Proyecto de Flow: https://flow.google.com/project/e2c946ad-b54a-4f37-8403-e8782e2d0325 (el de wow_ruta_forever y wow_errores_60;
los 2 ingredientes ya están subidos ahí: para reintentar, «Añadir ingredientes» → orden 1-2, sin volver a pegarlos).
x4 también marcaba «La generación consumirá 0 puntos» (aunque sale el aviso «Te quedan pocos puntos»), así que se pidieron 4.

Ingredientes (pegado sintético `ClipboardEvent('paste')` en `.ProseMirror` del navegador integrado, uno por llamada, ~6 s entre ellos):
1. `i.ytimg.com/vi/Rcu_3ztFANk/maxresdefault.jpg` (miniatura aprobada «La RUTA del 1 al 60»): letras «1 → 60» y logo WoW Forever.
2. `i.ytimg.com/vi/ju5Tc0pqtbg/maxresdefault.jpg` (miniatura aprobada «25 ERRORES»): el orco in-game del canal (cara, barba trenzada, ropa morada).
El taller (yunque, alquimia, hierbas, menas, pico, piel, hilo y tela) lo describe el prompt; no hubo ingrediente de fondo.

## Prompt

```
YouTube thumbnail 16:9 for a World of Warcraft Classic video about leveling professions from skill 1 to 300. Keep the exact in-game World of Warcraft Classic graphics of the ingredients (game screenshot look, painted low-poly textures, in-game character models); NOT a 3D animated movie, NOT Pixar, NOT clay, NOT cinematic CGI, NOT modern retail WoW, do not redraw the faces. Same lettering style and logo as image 1. BACKGROUND: an in-game World of Warcraft Classic crafting workshop like the Orgrimmar forge, warm orange firelight, stone and wood walls, a glowing forge fire in the back. In the foreground, a wooden crafting table full of profession items, clear and readable: a black anvil with a hammer and a red-hot glowing metal ingot with sparks, an alchemist mortar and pestle with three potion flasks (red, blue, green), bundles of herbs (Peacebloom, Silverleaf), shiny chunks of copper and mithril ore glowing, a miner's pick, a rolled cured leather hide, spools of thread and folded cloth. CHARACTER: the orc from image 2, exact same in-game model, face, braided beard and armor, big on the right side, working as a blacksmith: raising a hammer over the anvil, determined face, sparks flying. TEXT (bold, eye-catching YouTube thumbnail lettering exactly like the "1 → 60" of image 1, thick black outline and drop shadow), in the upper left, exact, render perfectly, no extra words: huge yellow (#FFE21E) "1", a big white arrow "→", huge yellow (#FFE21E) "300" (three digits: 3-0-0) — read as "1 → 300". Directly under it, smaller bold white "PROFESIONES" with black outline (spelled exactly P-R-O-F-E-S-I-O-N-E-S). LOGO: the "World of Warcraft FOREVER" logo exactly as in image 1, small, bottom-left corner. Use nothing else from image 1 (no map, no route, no "60", no pins) and nothing else from image 2 (no "25", no "ERRORES", no tooltip, no red sentence). No watermark, no other text, no spelling mistakes, sharp text.
```
(El prompt también se pegó con `ClipboardEvent('paste')` + `DataTransfer.setData('text/plain', …)`; clic real en «Iniciar generación».)

## Resultado (25-nov-2026)
- A la primera, sin bloqueo: x4 en ~40 s, 1376x768, 0 puntos. Las 4 con el texto perfecto («1 → 300», «PROFESIONES»), logo Forever abajo a la izquierda.
- Descarga: hook de `fetch`/`XMLHttpRequest.send` instalado ANTES de generar; la respuesta trae `flow-content.google/image/<id>?Expires…`
  (quitar `\`, u003d→=, u0026→&) → curl sin cookies. Hoja a tamaño celular: `miniatura_ing/_celular_abcd.jpg`; vistas 640x360 `miniatura_ing/_v_*.jpg`.
- `miniatura_ing/opciones/flow_a.jpg`: orco con guantes (no es el de la aprobada) y cara seria; objetos más pequeños.
- `miniatura_ing/opciones/flow_b.jpg`: orco gruñendo, buena; taller más oscuro y objetos chicos.
- `miniatura_ing/opciones/flow_c.jpg`: muchos frascos, mesa algo recargada.
- `miniatura_ing/opciones/flow_d.jpg` ← **ELEGIDA**: orco más grande y fiel a la aprobada (manos desnudas, ropa morada), martillo en alto,
  lingote al rojo con chispas, fragua encendida detrás; frascos rojo/azul/verde, hierbas, menas, mortero, pico, piel y tela grandes y legibles.
- `salida/miniatura.jpg` = D a 1280x720 (255 KB). Pendiente: subirla con el video (`yt subir` la toma sola) o `yt aplicar` si ya está subido.
