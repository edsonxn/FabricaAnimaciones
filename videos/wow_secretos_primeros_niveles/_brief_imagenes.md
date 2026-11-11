# Encargo: imagen REAL de todo lo que nombra la voz (10-nov-2026)

Video: `C:\FabricaAnimaciones\videos\wow_secretos_primeros_niveles\` — «20 secretos escondidos de los primeros niveles de WoW Forever»
(Crónicas de Warcraft, ~28 min, motor SECUENCIA YT: un clip de gameplay de YouTube por beat + capas de efectos encima).

## Qué pidió el usuario (regla nueva, leer `docs/estilo_secuencia_yt.md` § «TODO LO QUE SE NOMBRA SE MUESTRA»)
«Cuando hablas de objetos o personajes de misión o escenas, busca imágenes reales de lo que hablas. Por ejemplo la caja de pesca
hundida en Loch Modan: está bien el mapa, pero apóyate de imágenes que muestren el objeto real en la escena, o el personaje si habla.
Cuando hablas de los secretos de las Ruinas de Lordaeron, apóyate con imágenes para que se entienda el secreto. Mejor con videos;
si no hay videos, imágenes como pegatina grande o cubriendo toda la pantalla.» En secretos/huevos de pascua es OBLIGATORIO.

## Archivos (solo LEER; NO edites guion.py, efectos.py, beats.json ni busquedas.json: otro agente integra)
- `guion.py`: frases por escena (`{"id": 's09', "frases": [...]}`; la frase N de la escena sXX es `sXX_N`, desde 0).
- `efectos.py`: lo que ya se pone encima (pegatinas `pv/rel/sil/cam/ban`, `pant()` = imagen a pantalla completa, `mapa()`, `mg()`, tarjetas `dict(tarjeta=...)`), anclado por texto de la frase (`en=` / `de=`/`a=`).
- `beats.json`: 199 beats `{"id":"scene-NNN","t0","t1","texto"}` (texto = frase(s) que suenan en ese beat); `busquedas.json`: `{"scene-NNN": {"url","desde"}}` = de qué video y segundo sale el clip de ese beat. Clips bajados: `medios/scene-NNN.mp4`.
- `videos/_investigacion_wow_secretos_primeros_niveles.md`: fuentes y coordenadas de cada secreto (grep por nombre).
- `pegatinas/` (png ya hechos, `pegatinas/_fuentes.txt`), `pantallas/` (jpg a pantalla completa), `previews/_guias/` (guías ya bajadas).

## Qué hacer en TUS puestos
1. Para cada frase, apunta cada OBJETO, PERSONAJE (sobre todo el que habla o da la misión), LUGAR concreto (sala, casa, rincón) y PASO del secreto (clic, gesto, objeto que se usa, lo que aparece después).
2. Mira qué se ve en ese momento: el clip del beat (`ffmpeg -ss <s> -i medios/scene-NNN.mp4 -frames:v 1 -vf scale=640:-1`, hojas a 640x360 para ahorrar) + lo que ya pone efectos.py. Si ya se ve CLARO, no hagas nada.
3. Lo que no se ve o no se distingue: busca material REAL de World of Warcraft (Classic / Forever / la versión de la época; nunca otro juego, ni Hearthstone, ni fan art, ni retail moderno si se ve distinto):
   - Primero VIDEO: `yt-dlp "ytsearch10:<búsqueda en inglés>" --print "%(id)s | %(duration)s | %(height)s | %(title)s"`, luego mira una hoja de cuadros del tramo. Si un video enseña el secreto, propón ese clip para el beat (url + segundo exacto `desde`).
   - Si no, CAPTURA nítida: `yt-dlp -f "bv*[height<=2160]" --download-sections "*A-B" -o ...` a la mayor calidad + `ffmpeg -ss` a PNG, recorte limpio SIN rótulos/caras/webcams/texto del youtuber. También valen capturas de Wowhead/warcraft.wiki.gg (screenshots del objeto o PNJ in-game; comprueba identidad: mismo PNJ/objeto, misma zona).
   - Guarda: pantalla completa → `pantallas/<slug>.jpg` (16:9, ≥ 1280 de ancho); pegatina → `pegatinas/<slug>.png` (recorte del objeto/PNJ, ≥ 500 px). Slugs nuevos únicos, prefijo con el puesto: `s15_caja_pesca`, etc. Añade una línea por imagen a `pegatinas/_fuentes.txt` (archivo, fuente URL + segundo, qué es).
   - Descargas temporales en `_dl/img_<tu grupo>/`.
4. MIRA cada imagen que guardes (a 640 px) y comprueba que es lo que se nombra (identidad, no nombre: homónimos fuera).
5. No inventes: si de verdad no hay material, dilo («falta: Flow con ingredientes X»).

## Lo que devuelves (y escribes en `_propuesta_imagenes_<grupo>.md`)
Una fila por cambio: `frase id | texto exacto (4-8 palabras) donde empieza | hasta qué palabras | tipo (pant / pegatina grande / carr de 2-4 / clip nuevo para scene-NNN) | slug(s) o url+desde | qué se ve`. Más una línea de «ya bien» por lo que no necesita nada. Breve: sin volcar archivos.
Python 3.10, ffmpeg en PATH (C:\ffmpeg\bin), yt-dlp instalado. Windows (Git Bash). No lances renders ni `fab.py video`, no toques procesos.
