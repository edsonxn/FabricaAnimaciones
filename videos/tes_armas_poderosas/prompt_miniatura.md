# Miniatura de «Las 15 armas más PODEROSAS de Skyrim» (Flow, Nano Banana 2.1, 23-oct-2026)

Estilo PROPIO del canal (receta en `videos/tes_misiones_daedricas/prompt_miniatura.md`): pergamino de fondo, título blanco
enorme con contorno negro, píldora amarilla, píldora negra «SKYRIM» y el personaje como RENDER del juego a la derecha.
Variable del video: Mercer Frey (dueño del n.º 3) con la Daga de hueso de dragón (n.º 1) y la Desgarradora gélida (n.º 3).
Resultado: `salida/miniatura_flow_v1.png` → `salida/miniatura.jpg` (1280x720), a la primera.

Ingredientes (pegados en el navegador INTEGRADO desde sus URL públicas, ver abajo): 1 miniatura del canal «8 dragones»
(i.ytimg.com/vi/fKPDEaOYMxQ/maxresdefault.jpg) · 2 Mercer Frey (wiki, Mercer_Frey.png) · 3 Dragondagger.png · 4 Glassswordchillrend.png.
Copia local en `miniatura_ing/`.

**Pegar ingredientes en el navegador integrado (23-oct-2026):** la página de Flow NO puede pedir nada a 127.0.0.1
(`ERR_BLOCKED_BY_CLIENT`, el navegador del app lo bloquea), pero sí a URL públicas con CORS (static.wikia.nocookie.net,
i.ytimg.com): `fetch(url) → createImageBitmap → canvas → toBlob('image/png') → File → ClipboardEvent('paste')` sobre el
`[contenteditable]`, UNO cada ~6 s (si se pegan seguidos solo entra el primero). La imagen final: `currentSrc` del `<img>` de
1376x768 y `curl` desde PowerShell.

## Prompt
YouTube thumbnail, 16:9, exactly the same layout, style and typography as image 1: an old aged parchment map of a fantasy land
as the background, warm brown and gold tones. On the left, huge bold white sans-serif text with a thick black outline in two
lines: "15 ARMAS". Under it, a rounded bright yellow pill label with bold black text: "MÁS PODEROSAS". Under that, a smaller
rounded black pill label with bold white text: "SKYRIM". On the right: the hooded man from image 2, keep him exactly as the
in-game 3D character render, not painted (same face, same dark hood and leather thief armor), menacing smirk, holding up in his
right hand the pale bone dagger from image 3 (same shape, same bone color), and in his left hand the glowing icy blue crystal
sword from image 4 (same blade), both weapons glowing, cold blue frost mist and warm golden light. High contrast, crisp, readable
at small size. Spell the text exactly: "15 ARMAS", "MÁS PODEROSAS", "SKYRIM". No other text, no watermark, no border.
