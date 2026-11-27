# Miniatura — «La NASA chocó contra un asteroide: este es el CRÁTER» (T Menos Cero)

Generada en Google Flow (navegador integrado), Nano Banana 2.1 · Imagen · 16:9 · razonamiento Alto · x2 · 0 puntos (26-nov-2026).

Ingredientes (pegado sintético con `ClipboardEvent('paste')`, sin rótulos ni logo de la ESA, recortados antes):
1. `miniatura/ref_dimorphos.jpg` — Dimorphos fotografiado por Hera, cuadro de la transmisión de la ESA (`clips/esa_hoy.mp4`, s 27; recorte 400×400 de 1080p, solo el asteroide con la cara aplanada). Ingrediente único; la nave DART va solo descrita en el prompt (la ilustración de la NASA trae un Dimorphos inventado y se descartó).

## Prompt

```
YouTube thumbnail, 16:9, ultra high contrast, readable at small size. Use the reference photo as the real look of asteroid Dimorphos photographed by the Hera space probe (photorealistic grey rubble-pile asteroid, loose boulders, hard sunlight from one side, deep black space).
LEFT 60% of the frame: the asteroid Dimorphos huge and close, photorealistic, exactly like the reference photo: grey rocky surface covered in loose boulders, one side clearly FLATTENED, and a very large obvious IMPACT CRATER almost as wide as the whole asteroid on that flattened face, with a sharp raised rim and deep shadow inside, hard side lighting from the left, black space behind. A faint spray of small rocks and dust drifting out of the crater.
RIGHT 40% of the frame: pure black background with a clean technical drawing made of thin glowing WHITE LINES only: the outline silhouette of the same asteroid with the crater marked by a white circle and a thin dimension line with small tick marks across the crater, and a tiny DART spacecraft drawn in white line art (a small box with two long thin rectangular solar panels) arriving along a dotted white trajectory line toward the crater. Minimal wireframe engineering style, white line art on black. The photo on the left blends into the line drawing on the right with a sharp diagonal split.
TEXT (exact, Spanish, render perfectly, no extra words): huge bold condensed sans-serif YouTube thumbnail lettering, upper right over the black area: first line "EL CRÁTER" in pure white with thick black outline and drop shadow, very large, spelled exactly C-R-Á-T-E-R with an acute accent on the Á; second line "DE DART" in bright yellow (#FFE21E) with thick black outline. Letters crisp and sharp, never cut by the frame edge.
NEGATIVE: no logos, no NASA logo, no ESA logo, no watermark, no people, no faces, no extra text, no numbers, no misspellings, no blurry letters, no planets, no Earth.
```

## Resultado (26-nov-2026, a la primera)

- **A (elegida)** → `miniatura/miniatura.jpg` (1280×720, 234 KB) y `propuestas/flow_A_elegida_1376x768.jpg`: Dimorphos fotorrealista con un cráter enorme y redondo en la cara de la luz, chorro de rocas saliendo; a la derecha el contorno del asteroide en línea blanca, círculo + cota sobre el cráter y la nave DART (caja + dos paneles) en línea punteada. «EL CRÁTER» blanco y «DE DART» amarillo, bien escritos (Á correcta). A 240 px el cráter y el texto se leen.
- **B** → `propuestas/flow_B_1376x768.jpg`: mejor dibujo técnico (silueta facetada del asteroide), texto también correcto, pero el cráter se confunde con la superficie a 240 px.
- Ojo: el cráter de A es más redondo y limpio que el real (el de Hera es una cara aplanada); es la exageración de miniatura pedida.
- Bajada: URL firmada `flow-content.google/image/<id>?Expires…&Signature…` de la respuesta del POST `batchexecute` `rpcids=ogiZ0b` (`read_network_requests` con su requestId) → curl.
- Lección: un base64 de ~9 KB copiado a mano en `javascript_tool` llegó corrupto (ingrediente con bloques grises). Lo que funcionó: WebP 288 px en gris (5,4 KB) partido en trozos de 1.200 caracteres en `window.__ch[]`, cada uno comprobado con CRC32 en la página contra el local antes de unir y pegar.
