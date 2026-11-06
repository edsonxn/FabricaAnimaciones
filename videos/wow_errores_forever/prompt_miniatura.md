# Miniatura de «Los 25 ERRORES que estás cometiendo en WoW Forever» (Flow, Nano Banana, 6-nov-2026)

Ingrediente REAL: cuadro del tráiler cinemático oficial de WoW Forever (gnomo de bigote verde + humano de la Alianza con la cara roja
de vergüenza), sacado de `medios/scene-140.mp4` → `miniatura_ing/base_140.png`. Luego, con PIL, el logo real de Forever abajo a la izquierda.

## Prompt
YouTube thumbnail, 16:9. Use image 1 as the base and keep the real World of Warcraft Forever cinematic artwork faithful: the green-haired
gnome on the left and the embarrassed red-faced human soldier on the right, same faces, same style, do not redraw them. Make the human
cringe harder, eyes shut, as if he just made a huge mistake, and add a glowing red game-style error mark "X" floating between them with
red light on their faces. Darken the top area for text. Text in Spanish, exact, render perfectly, no extra words: first line "25 ERRORES"
in huge thick yellow #FFE21E condensed capitals with thick black outline across the top, second line "EN FOREVER" smaller in white with
black outline under it. Bottom-left dark and empty for a logo. No other text, no watermark, no border.

## RECHAZADA por el usuario (6-nov): la de arriba salió estilo Pixar/plastilina (cinemática). Versión vigente:
Base `miniatura_ing/base_067.png` (orco HD real de la pantalla de creación de Forever, scene-067) → Flow (orco_v1, «keep the exact in-game
WoW Forever graphics… NOT Pixar, NOT clay, NOT cinematic CGI», sin texto) → `miniatura_componer.py` (PIL): «25 ERRORES QUE ESTÁS
COMETIENDO» Impact amarillo con contorno, mensaje rojo real de error de la interfaz, logo real de Forever. Comparada con las antiguas
del usuario en `previews/miniatura_vs_antiguas.jpg`.

## VIGENTE (6-nov, 2.ª corrección del usuario: texto CON Nano Banana, no PIL; tooltip real; más fondo real)
Ingredientes: (1) `orco_v1.png` (orco HD in-game de Forever), (2) `tooltip_spare_part_bindings.png` (tooltip azul REAL del clip 075,
Ruinas de Lordaeron), (3) `fondo_146.png` (atardecer in-game de Los Baldíos). Prompt: «keep the exact in-game graphics… NOT Pixar, NOT
clay, NOT cinematic CGI… image 3 as more visible real game background… image 2 floating, keep its text… real red WoW interface error at
the top… "25 ERRORES" ultra-bold yellow #FFE21E thick black outline / "EN FOREVER" white». Elegida `texto_v1.png` + logo real de Forever
(PIL, solo el logo). Hoja comparativa: `previews/miniatura_vs_antiguas.jpg`. `miniatura_componer.py` queda obsoleto (texto en PIL).

## ELEGIDA POR EL USUARIO (6-nov): opción 6 de 8 (`miniatura_ing/opciones/op6.jpg` → `salida/miniatura.jpg`, tal cual)
Ingrediente: la miniatura aprobada (orco in-game + Los Baldíos + tooltip real + error rojo + logo); Nano Banana solo cambia el texto.
Prompt:
YouTube thumbnail, 16:9. Image 1 is the approved thumbnail: keep EVERYTHING exactly as it is, the same in-game HD orc, the same real Barrens background, the same blue item tooltip, the same red error message at the top and the same World of Warcraft Forever logo bottom-left, real game screenshot look, NOT Pixar, NOT clay, NOT cinematic CGI. Only erase the big white and yellow text on the left and replace it with new text, exact Spanish words, render perfectly, no extra words, same left area, not covering the orc, the tooltip or the logo: a gigantic yellow "25" with thick black outline taking most of the left side, and under it the word "ERRORES" smaller in white bold capitals with black outline, crossed by a big red hand-drawn X mark stroke over the corner of the 25.
Hoja de las 8: `previews/miniatura_opciones.jpg`. No se retocó el tooltip: el orco va delante de él a propósito, y moverlo lo encimaba con el «25».
