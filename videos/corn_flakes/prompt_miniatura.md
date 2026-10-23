# Miniatura de corn_flakes (Flow, Nano Banana 2.1 · 16:9 · x2, 0 puntos; 23-oct-2026) — 2/2 bien, elegida la B

Fórmula nueva de Plastitube (`canales/formula/pieza_oculta.md`): retrato REAL en medallón + personajes de plastilina + el objeto + 2-4 palabras que lo nombran.

**Ingrediente:** los dos retratos de dominio público de Wikimedia (John Harvey Kellogg y W. K. Kellogg) unidos lado a lado.
En el navegador integrado el Ctrl+V del portapapeles de Windows NO llega; lo que sí funcionó: en `javascript_tool`, bajar las
imágenes de upload.wikimedia.org con `fetch` (CORS abierto), unirlas en un `<canvas>`, hacer un `File` y despachar en el
`.ProseMirror` un `new ClipboardEvent('paste', {clipboardData: dt})` con un `DataTransfer` que lleva ese `File`. Flow lo sube como ingrediente.

**Prompt:**
YouTube thumbnail, cinematic horizontal 16:9, handmade stop-motion plasticine clay diorama with visible fingerprints, warm dramatic
window light, high contrast. Use the two men in the reference photo as the likeness. In the center, a big white ceramic bowl
overflowing with golden crunchy corn flakes, a few flakes flying in the air. On the left, a plasticine clay caricature of the older
man from the reference (white mustache and white goatee, round glasses, all-white suit) turning his back, arms crossed, furious. On
the right, a plasticine clay caricature of the younger man from the reference (small round glasses, brown mustache, black bow tie,
charcoal gray suit) also turning his back, arms crossed, frowning. A jagged crack splits the wooden kitchen table between them.
Background: a dark warm 1900s sanitarium kitchen, softly blurred. In the top left and top right corners, two small round vintage
sepia photo medallions with thin gold frames showing the two real men exactly as in the reference photo. Big bold text at the top
center in thick yellow letters with a black outline: "CORN FLAKES". Under the bowl, smaller red letters with a white outline:
"POR UN ERROR". Only these words, spelled exactly like that. No other text, no logos, no brand names, no numbers.
