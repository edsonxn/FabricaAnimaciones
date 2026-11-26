# Miniatura — wow_errores_60 (22-nov-2026, Flow Nano Banana 2.1, Imagen · 16:9 · x2, 0 puntos)

Título: «Los 25 ERRORES al llegar al nivel 60 en WoW Forever». La miniatura copia la composición de la aprobada «25 ERRORES»
(ju5Tc0pqtbg, 16 019 vistas) cambiando el fondo a Monte Hyjal de Forever, la insignia «NIVEL 60» y el error rojo.
Proyecto de Flow: https://flow.google.com/project/e2c946ad-b54a-4f37-8403-e8782e2d0325 (el de wow_ruta_forever).

Ingredientes, en este orden:
1. `i.ytimg.com/vi/ju5Tc0pqtbg/maxresdefault.jpg` (pegado sintético `ClipboardEvent('paste')` en `.ProseMirror`): orco in-game, letras, logo Forever.
2. `monte_hyjal_forever.jpg` (ya subido al proyecto; «Añadir ingredientes» → Añadir a petición): Monte Hyjal, galería oficial de Forever en warcraft.wiki.gg.
(Se intentó la Cima Hyjal de `pegatinas/cima_hyjal.png`: wiki.gg no tiene CORS y pegarla en base64 costaba 16 KB por llamada.)

## Prompt

```
YouTube thumbnail 16:9 for a World of Warcraft Classic video about the mistakes players make when they reach level 60. Keep the exact in-game World of Warcraft Classic graphics of the ingredients (game screenshot look, painted textures, in-game character models); NOT a 3D animated movie, NOT Pixar, NOT clay, NOT cinematic CGI, NOT modern retail WoW, do not redraw the faces. Same layout and lettering style as image 1. BACKGROUND = image 2: the real in-game Mount Hyjal landscape (giant purple trees, the night elf building, the glowing lake) filling the whole frame, slightly darkened behind the text, with a few small red dragons flying in the sky. CHARACTER: the orc warrior from image 1, exact same in-game model and armor, big on the right side, shocked face with open mouth, one hand raised, looking at the text. TEXT (bold, eye-catching YouTube thumbnail lettering, same style as image 1, thick black outline and drop shadow), exact, render perfectly, no extra words: on the left a huge yellow (#FFE21E) "25" with a big red X over its top right corner like in image 1, under it big white "ERRORES"; under that a black rounded badge with yellow text "NIVEL 60". At the top, one line of red World of Warcraft error-message text with black outline, exactly: "¡No puedes entrar a la banda!". LOGO: the "World of Warcraft FOREVER" logo exactly as in image 1, small, bottom-left corner. Remove the item tooltip of image 1 and its red sentence. No watermark, no other text, no spelling mistakes, sharp text, accents correct.
```

## Resultado
- A la primera, sin bloqueo: x2 en ~40 s, 1376x768, 0 puntos. Descarga: hook de fetch/XHR + `HTMLAnchorElement.prototype.click` anulado,
  clic en «Descargar lote» → la respuesta trae `flow-content.google/image/<id>?Expires…` con barras invertidas y `u003d`/`u0026`
  escapados (quitar todas las `\` y cambiar u003d→= y u0026→&) → curl.
- `miniatura_ing/opciones/flow_a.jpg`: «NIVEL 60» más chico.
- `miniatura_ing/opciones/flow_b.jpg` ← **ELEGIDA**: «25» amarillo con X roja, «ERRORES» blanco, insignia «NIVEL 60», error rojo
  «¡No puedes entrar a la banda!» arriba, orco de la aprobada con la boca abierta y la mano alzada, Monte Hyjal de fondo, logo Forever.
- `salida/miniatura.jpg` = B a 1280x720.

## Miniatura B para la prueba A/B (25-nov-2026, tras el arranque flojo: CTR 5,9 % a 11,6 h)
Cambio de concepto: fuera el orco con el número tachado (tercera miniatura igual en 18 días). Onyxia in-game echando fuego,
marcos de banda con «Muerto», «¿LISTO? NIVEL 60» y el error rojo «¡Necesitas resistencia al fuego!». Generada en Chrome (Claude in
Chrome): ingredientes pegados con `Clipboard.SetImage` + Ctrl+V; descarga con `fetch(src '=s0')` → blob → `<a download>` (sin diálogo).
Ingredientes: 1. `miniatura_ing/ing3_onyxia.jpg` (= pegatinas/onyxia.png, in-game) · 2. `miniatura_ing/ing3_raid_ui.jpg` (captura de banda con UI).

```
YouTube thumbnail 16:9 for a World of Warcraft Classic video about getting ready for the first raids at level 60. Keep the exact in-game World of Warcraft Classic graphics of the ingredients (game screenshot look, painted textures, in-game models); NOT a 3D animated movie, NOT Pixar, NOT clay, NOT cinematic CGI, NOT modern retail WoW. BACKGROUND and MAIN CHARACTER = image 1: the real in-game black dragon Onyxia in her lava lair, exact same in-game model, made HUGE and filling the right two thirds of the frame, head lowered toward the camera, jaws wide open, a big wave of orange fire breath coming out of her mouth toward the left, lava glow, dramatic contrast. INTERFACE from image 2: on the far left edge a small World of Warcraft raid frame panel with five player health bars, three of them empty and grey (dead), two red and almost empty. TEXT (bold, eye-catching YouTube thumbnail lettering, thick black outline and drop shadow), exact, render perfectly, no extra words: on the left, huge yellow (#FFE21E) "¿LISTO?" and right under it big white "NIVEL 60". At the top left, one line of red World of Warcraft error-message text with black outline, exactly: "¡Necesitas resistencia al fuego!". No logo, no watermark, no other text, no spelling mistakes, sharp text, Spanish accents and the inverted question mark correct.
```
- x2 a la primera, 1376x768. `opciones/flow_ony_0.jpg` ← ELEGIDA (texto inclinado, marcos «Muerto» legibles) · `flow_ony_1.jpg` (texto recto, marcos vacíos).
- `salida/miniatura_b_onyxia.jpg` (1280x720).

## Prueba A/B en Studio («Título y miniatura», EN CURSO desde el 25-nov-2026 ~20:55 CDMX)
1. Los 25 ERRORES al llegar al nivel 60 en WoW Forever + miniatura original (orco «25 ✗ ERRORES»)
2. BANDAS de WoW Forever: 25 ERRORES que te dejan fuera + miniatura Onyxia
3. Los 25 ERRORES al llegar al nivel 60 en WoW Forever + miniatura Onyxia (aísla el efecto de la miniatura)
YouTube elige la ganadora por tiempo de visualización y la aplica sola. Leer el informe a los 7 días y anotar en la fórmula.
