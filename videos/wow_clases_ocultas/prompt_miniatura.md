# Miniatura de «Las 9 clases y profesiones OCULTAS de WoW Forever» (Flow + ingredientes reales, 13-oct-2026)

REGLA del canal (el usuario, 13-oct-2026): la miniatura se hace en Flow COMBINANDO capturas y elementos REALES del juego como
ingredientes (UI, personajes, fondos), nunca una imagen inventada. La primera versión solo con prompt (mago y panel de iconos
inventados, `salida/miniatura_a.jpg`/`_b.jpg`) fue rechazada.

Ingredientes (`miniatura_ing/`, sacados de `medios/`):
1. `1_creacion_personaje_mago.jpg` — pantalla real de creación de personaje (scene-043, t=1 s): mago y barra de clases.
2. `2_tooltip_coldflame_saber.jpg` — tooltip real del Coldflame Saber (scene-071, Farmerfarms).
3. `3_castillo_shadowfang.jpg` — patio real del Castillo de Colmillo Oscuro (scene-069). De reserva.
Logo real de Forever: se compone con PIL después (`C:\googleimagenes\thumbnails\forever_inmersivas\refs\forever_logo.png`).

Herramienta: `python C:\googleimagenes\scripts\flow_thumb.py "<prompt>" --ingredientes a,b --variantes 2 --exacto` (Chrome con
perfil `%LOCALAPPDATA%\ChromeFlowProfile` en el puerto 9222).

## Prompt

YouTube thumbnail, 16:9. Use image 1 as the base and keep it looking exactly like a real in-game screenshot: the real character
creation screen, its real interface and the real character model must stay faithful to image 1, do not redraw them in another
style. Zoom in so the mage character fills the left-center of the frame, larger and more heroic. The mage now grips a one-handed
sword whose blade glows icy blue frost with orange fire along its edge, the brightest element in the image. In the class icon
bar at the bottom of the screen, add one extra class slot at the end that glows intensely gold and purple with a white question
mark inside it, light rays bursting from it. Place image 2, the real item tooltip, unchanged and perfectly legible, large on the
right side of the frame with a soft glow around its border. Dramatic cinematic contrast, slightly darker vignette, keep the
bottom-left corner fairly dark and empty for a logo, nothing important in the bottom-right corner. No added text, no watermark,
no border.
