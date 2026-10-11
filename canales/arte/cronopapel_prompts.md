# Cronopapel — prompts para Nano Banana 2 (foto de perfil y banner)

Estilo de marca = el de los videos: **ilustración plana tipo boceto + guache sobre papel**, paleta cálida y apagada (crema, arena, verde azulado, terracota, mostaza), contornos de tinta negra que tiemblan un poco, relleno de crayón en trazos diagonales, grano de papel, sombra suave tipo recorte de papel pegado. Nada de 3D, nada de degradados brillantes.

Colores de marca: crema papel `#F7F4EB`, verde azulado mar `#BAD6D8`, arena `#EADEC0`, terracota/rojo sello `#C6423A`, mostaza `#EEB440`, tinta `#1E1B21`.

---

## 1) FOTO DE PERFIL (pedir 1:1, 2048x2048; YouTube la recorta en círculo y la muestra a ~98 px)

```
Square 1:1 channel avatar logo, flat vector illustration with a hand-drawn ink sketch style and gouache paper texture, like a modern animated history explainer.

SUBJECT: one big, simple, centered emblem that fills about 80% of the frame: a cream-colored stopwatch (clock) drawn with thick wobbly black ink outlines, whose round face is a painted miniature map of Asia: pale teal sea, sand-colored land, and ONE large terracotta-red territory shaped like China in the middle of the face. The map has a thin crack running through it, like a torn piece of paper that is being put back together. The stopwatch has a small golden crown button on top and a single black clock hand pointing to 12. Around the stopwatch edge, a thin white paper-cutout border (sticker style) with a soft drop shadow.

BACKGROUND: solid dark teal-blue #1F4E5A with very subtle paper grain, nothing else, no text, no letters.

STYLE DETAILS: crayon-style diagonal hatching inside the colored areas, slightly offset from the ink lines (like a child coloring), matte gouache look, warm muted palette (cream #F7F4EB, sand #EADEC0, sea teal #BAD6D8, terracotta red #C6423A, mustard #EEB440), black ink #1E1B21.

COMPOSITION: emblem perfectly centered with generous margin so nothing important is cut off by a circular crop; very readable when shrunk to 98 px; high contrast between the emblem and the dark background.

NEGATIVE: no text, no watermark, no 3D render, no glossy gradients, no photorealism, no tiny details, no faces, no extra objects.
```

**Variante B (alternativa, más "animal de papel" por el nombre anterior):** mismo prompt pero el emblema es un **cocodrilo/dragón de papel plegado en miniatura** (origami dorado) enroscado alrededor de un reloj de bolsillo. Usar solo si A no convence.

**Comprobar:** a 98 px debe leerse "reloj con mapa rojo" y nada más. Si se ve sobrecargado, pedir: *"simplify: remove the crack and the crown, keep only the red map on the clock face"*.

---

## 2) BANNER (pedir 16:9 y luego reescalar a **2560x1440**, < 6 MB)

Zona segura: todo lo importante (nombre + lema) dentro del **rectángulo central de 1546x423 px** (en la imagen de 2560x1440, centrado). El resto se ve solo en pantallas grandes/TV; en celular solo se ve esa franja.

```
Wide 16:9 YouTube channel banner, flat vector illustration with a hand-drawn ink sketch style and gouache paper texture, like a modern animated history explainer. Warm cream paper background with visible paper grain and soft blotchy watercolor-like variations.

SCENE: a huge vintage paper world map laid flat, seen from above, painted in muted gouache: pale teal oceans, sand-colored continents with slightly wobbly black ink coastlines. Several territories are painted in flat terracotta red, mustard yellow, sage green and steel blue, like historical empires, and some of them have thin cracks as if the paper map were torn into puzzle pieces that fit back together. Stuck on the map like white cut-out paper stickers with soft shadows, small cartoon figures and objects of world history: a Chinese emperor with a flat beaded crown on the far left, a pyramid, a Roman column, a viking ship with a striped sail, a samurai, a Mongol horseman, a caravel, a Great Wall segment, a tiny Eiffel-like tower, a steam train, a moai, a castle. A dotted black route with little arrows crosses the map. A few red square dynasty seal stamps are scattered on the map.

CENTER (most important): the middle third of the banner is calm and uncluttered (just map and paper texture, slightly lighter so text pops). In the exact center, hand-lettered in a thick, friendly, slightly wobbly brush-marker font, dark ink #1E1B21 with a white paper-cutout outline and soft shadow: the word "CRONOPAPEL" in large capital letters, and below it, smaller, the tagline "La historia del mundo, en minutos". Text exact, in Spanish, render perfectly, no extra words, no misspellings, correct accents.

STYLE DETAILS: crayon-like diagonal hatching inside colored shapes, slightly offset from the ink outlines; sticker figures with thin white borders and soft drop shadows; matte gouache finish. Palette: cream #F7F4EB, sand #EADEC0, sea teal #BAD6D8, terracotta red #C6423A, mustard #EEB440, sage green #7EA88A, steel blue #6086B8, ink #1E1B21.

COMPOSITION: symmetric, clutter only at the far left and far right edges, clean central band of about 60% of the width for the title, horizontal feel, no important element in the top 15% or bottom 15% of the image.

NEGATIVE: no watermark, no extra text, no logos of real companies, no real people or real faces, no spelling mistakes, no blurry text, no photorealism, no 3D render, no neon, no glossy gradients.
```

**Variante corta del lema (si el texto sale mal):** pedir *"change ONLY the tagline to: 'Historia en minutos'. Keep everything else identical."*

**Si el acento o una letra sale mal:** *"fix only the text, keep the rest identical: CRONOPAPEL / La historia del mundo, en minutos"*.

---

## Cómo lo aplico cuando los tengas
1. Me avisas y me pasas las imágenes (o las dejas en `canales/arte/`).
2. Yo reescalo el banner a 2560x1440 (< 6 MB) y el perfil a 800x800, y subo el banner con `python fab.py yt canal cronopapel` (campo `banner` del JSON).
3. **La foto de perfil y el nombre solo se cambian en Studio** (la API de YouTube no lo permite): Studio > Personalización > Perfil → Nombre «Cronopapel» y subir el perfil.
