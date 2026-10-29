# Miniatura de «Las 5 peores atrocidades de Radahn QUE IGNORASTE» (Flow, 28-oct-2026)

Receta ganadora del canal (Márika ×24,6, KKxhcwon2kg) cambiando solo el personaje. Ingredientes en miniatura_ing/: 1 ref_marika.jpg
(composición y tipografía), 2 radahn_real.jpg (captura REAL de las Dunas, Elden Ring Wiki), 3 radahn_cuerpo.png (render oficial),
4 radahn_estrellas.jpg (cinemática de Aeonia). Elegida: flow/radahn_v1.png → salida/miniatura.jpg.

Prompt (miniatura_ing/prompt_linea.txt):
YouTube thumbnail, 16:9, exactly the same layout, style and typography as image 1: an old aged parchment map of a fantasy land as the background, warm brown and gold tones. On the left, a bright yellow rectangular box with a thin black border and huge bold black condensed sans-serif text in two lines: "ATROCIDADES" and "DE RADAHN". Under it, a smaller black box with a white outline and bold white text: "ELDEN RING". On the right, a dramatic painted fantasy character in the same epic illustrated style as image 1: the giant red-maned general from images 2 and 3, faithful to them (wild flaming red hair like a lion's mane, a golden lion-faced helm with horns, heavy dark armor and a tattered cape, two huge curved greatswords), towering and menacing, surrounded by swirling violet gravity magic, with broken spears stuck in his back, and behind him a night sky with a burning violet star falling like a meteor, as in image 4. High contrast, crisp, readable at small size. Spell the text exactly: "ATROCIDADES", "DE RADAHN", "ELDEN RING". No other text, no watermark, no border.

Comando (rutas ABSOLUTAS: el script resuelve desde C:\googleimagenes; el prompt por --file, las comillas rompen PowerShell):
python C:\googleimagenes\scripts\flow_thumb.py --file <abs>\prompt_linea.txt --ingredientes <abs>\ref_marika.jpg,... --variantes 2 --exacto --salida <abs>\flow --nombre radahn
