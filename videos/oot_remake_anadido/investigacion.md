# Investigación: lo que Nintendo AÑADIÓ en SECRETO al remake de Ocarina of Time (Switch 2)

Investigado el 11-nov-2026, seis días después del lanzamiento (5-nov-2026). Solo con fuentes web y videos de YouTube de la semana. Cada punto se comprobó leyendo la nota, y cuando se pudo, con la transcripción del video (subtítulos automáticos vía yt-dlp, que recogen las voces del juego) o mirando cuadros (hojas de contacto de clips bajados a 360p a la carpeta temporal).

**Niveles de confianza**
- **Alto**: lo dice Nintendo (Aonuma, Fujibayashi, Ng) o lo dicen dos medios o más, y además se ve u oye en un video.
- **Medio**: una nota fiable más un video, o dos fuentes sin cita oficial.
- **Bajo**: una sola fuente, un datamine sin confirmar o un Short de fans.

**Sobre los segundos**
- **[transcr.]**: el segundo sale de los subtítulos del video, que transcriben las voces del juego.
- **[visión]**: lo comprobé mirando cuadros del clip.
- **[capítulo]**: el segundo sale de los capítulos de la descripción.
- **POR LOCALIZAR**: hay un video candidato, pero el segundo no está comprobado. Hay que mirarlo antes de usarlo.

**Sin narrador**: los clips de Gamer's Little Playground, Shirrako, Sirloin, BeardBear y LunarGaming son gameplay sin comentarios. Los de GameSpot, koadyokay y KnightPohtaytoe tienen narrador. Para usarlos hay que pasarlos por Demucs `no_vocals` (`videos/oot_remake_cambios/quitar_narrador.py`) o quitarles el audio.

**Clips N64**: vienen de la serie ZeldaCentral NSO que ya está catalogada en `videos/zelda_oot/mapa_clips.md` (marco 0,131).

---

## 0. Descartado porque YA LO CONTAMOS (no repetir)

**En `oot_remake_cambios`:**
- bolsa de 200 rupias
- amiibo de Link niño y Zelda niña con máscaras retro
- pantallas de carga a propósito
- app Zelda Notes
- ciclo de día y noche en los pueblos
- inventario con accesos en la cruceta
- giroscopio
- Ciudadela en 3D
- orquesta
- Threads of Time
- doblaje
- ocarina con el micrófono, ocarina física y la de HORI
- esprint
- barra de buceo
- cámara libre
- botón de salto

**En `oot_remake_eliminado`:**
- tapiz en lugar de los cuadros de Mario
- broche de Bowser de Talon
- guardia de la bomba
- Gafas de la Verdad
- Broche Resonante en lugar de la Piedra de la Agonía
- flores sobre las grutas
- tronco verde en el Bosque Perdido
- «fairy thoughts», las hadas con pistas
- nueva voz de Navi
- Grandes Hadas que cobran
- una sola ranura de guardado
- glitches
- puente levadizo
- Master Quest ausente
- sangre de Ganondorf
- teletransportes que Aonuma mandó quitar

**Mencionado de pasada:** el cierre de `oot_remake_eliminado` dice «un coliseo para pelear otra vez con los jefes». Aquí el Salón de los Enemigos Caídos (n.º 9) se cuenta a fondo, con lo que no se dijo.

**Pistas de la lista que no entran:**
- **«Secret Skull Kid Boss Fight» (Sirloin `Go0khcpjGEA`, BeardBear `Mh-ZKyaQcXE`): FALSO como añadido.** Lo comprobé con visión del video completo de Sirloin (vidIQ). No hay rótulo de jefe ni barra de vida.
  - Es el Skull Kid del tocón del Bosque Perdido, que ataca a Link adulto. Se teletransporta, dispara dardos con la flauta y suelta una Rupia Gigante de 200 que reaparece al salir y volver a entrar.
  - Eso ya existía en N64: misma Rupia Gigante, misma granja (Zelda Dungeon y GameWith, «Leaving the area and returning will respawn these Skull Kids»; clip N64 `g70dvKoI6I4`, 41 s).
  - Lo único nuevo es el bocadillo **«A grown-up!»** (`Go0khcpjGEA` 1:37 [visión]).
  - **Sirve como remate burlón:** «el jefe secreto que lleva 28 años ahí». También como contraste: la granja del puente desapareció, pero esta sigue.
  - Pelea en `Go0khcpjGEA` 0:10-0:26 y 1:40-2:18 [visión].
- **«Modo instrumento» (`d4PifU1Wd7o`): YA CONTADO en parte.** El p4 de `oot_remake_cambios` dice «tararear, o tocar». Lo comprobé con visión: en Opciones, «Change mic input» tiene tres valores, None, Instruments y Humming. El youtuber toca la Canción del Sol con una guitarra (0:00-0:24). Vale como detalle de 3 s si hace falta, no como puesto.
- **«Link sonríe fuera de cámara» (`ZDHZi-KFh6E`): BAJA, no entra.** En los cuadros [visión] se ve a Link con la boca entreabierta mientras Saria le enseña la canción. No se aprecia un antes y un después claro, y no hay segunda fuente.
- **«Navi despierta a Link» (`VFaIuyUMwUQ`): BAJA, no entra.** Es la misma escena con más kokiris en el camino. Saria saluda a Navi desde una roca (0:14-0:18 [visión]). En pantalla dice «Understood. I'll go get him!» (0:00). Es un cambio menor y solo lo enseña un Short.
- **«Lank y Lonk» (GameSpot `mVNCFPhM8Hw`, 9 s): NO es un añadido.** GameSpot lo explica así: «Using glitches to go into the dungeons of the opposite time era». Son modelos rotos que salen con un glitch. Como mucho sirve de chiste en el cierre.
- **«Hidden details» `zOcdNR_c61M` / `-QGLbyO5lis`:** es el estuche físico. Entra como n.º 1.

---

## 1. Lista de añadidos, del menos al más impactante

### 1. El estuche esconde un mapa de Hyrule y a Navi debajo del cartucho
- **Qué es:** la cara interior del estuche físico de Switch 2 lleva impreso un mapa de Hyrule en pergamino. Al sacar el cartucho, debajo del soporte aparece la silueta de Navi. Algunas ediciones traen además un póster desplegable con el mapa.
- **Fuentes:**
  - `zOcdNR_c61M` (Peanut jelly butter, 11-nov, 53 k vistas): 0:03 se abre el mapa; 0:07-0:09 aparece Navi bajo el soporte [visión].
  - `-QGLbyO5lis` (TheSatisfyingProcess, 11-nov, edición asiática): 0:10-0:13 el mapa desplegable [visión].
- **Confianza:** MEDIA. Hay dos videos y se ve claro, pero no lo recoge ningún medio.
- **Clip:** `zOcdNR_c61M` 0:03-0:10 (7 s). Vertical: hay que encuadrarlo o usarlo como pegatina.
- **N64:** no hay equivalente. El cartucho de 1998 era dorado, y se puede mencionar.
- **Mapa:** no aplica. Puede ir como captura del mapa del estuche.

### 2. Restos mágicos con forma de Korok flotando en el Bosque Kokiri
- **Qué es:** en el Bosque Kokiri y en el Bosque Perdido flotan restos mágicos, como polen o hojitas, que muchas veces tienen la silueta de un Korok de Wind Waker o Breath of the Wild. Es un guiño a que los kokiris se convierten en koroks tras la Gran Inundación.
- **Fuentes:**
  - Game Informer lo llama «potentially the only addition» que apunta al futuro de la saga: https://gameinformer.com/2026/11/03/the-zelda-ocarina-of-time-easter-eggs-that-did-and-did-not-make-it-into-the-2026-remake
  - GamingBolt, n.º 3, aclara que es solo visual: https://gamingbolt.com/the-legend-of-zelda-ocarina-of-time-remake-did-you-catch-these-15-hidden-details
- **Confianza:** ALTA.
- **Clip remake:** POR LOCALIZAR. Candidatos: Kokiri del 100 % de GLP `oLHiQX2wxrE` (capítulo «Kokiri Forest» 370 s → 1818 s) o BeardBear `0GARyN7TgzY`. Hay que buscar un plano quieto con partículas flotando. Si no se distingue la forma, enseñar la imagen de la nota de Game Informer, recortada como pegatina.
- **N64:** Bosque Kokiri en ZeldaCentral P01 `N6rM3KhqHIo` 228-243 s. Ahí no hay restos.
- **Mapa:** Bosque Kokiri y Bosque Perdido (esquina sureste de Hyrule).

### 3. Link ahora actúa: dedos en la ocarina y brazos en la hierba alta
- **Qué es:**
  - Al tocar una canción, Link mueve los dedos sobre los agujeros de la ocarina. En N64 la sostenía quieto.
  - El sonido es una ocarina real grabada, y resuena distinto según el sitio, según Nintendo UK citado por GamingBolt.
  - Al correr entre hierba alta, Link niño levanta los brazos para cubrirse la cara. El adulto no lo necesita porque es más alto (GameSpot).
  - Epona se monta como en Breath of the Wild, incluso a la carrera (GameSpot).
- **Fuentes:**
  - GamingBolt n.º 11 y 12 (enlace del n.º 2).
  - GameSpot «25 Things You STILL Didn't Know» `-0cwlyMdre8`: hierba en 2:30-2:46 y Epona en 1:02-1:15 [transcr.].
- **Confianza:** MEDIA. Los dedos y la grabación tienen una sola fuente escrita. Los brazos y Epona solo los cuenta GameSpot, pero se ven en su video.
- **Clip remake:**
  - dedos: `d4PifU1Wd7o` 0:18-0:21, Canción del Sol en primer plano [visión]. Tiene facecam encima, así que hay que recortar la mitad inferior. Mejor buscar el mismo plano en GLP `L45cq1H2d1s` (POR LOCALIZAR).
  - hierba: `-0cwlyMdre8` 2:38-2:46 (con narrador).
- **N64:** ocarina quieta en P01/P02 (Saria y el puente, `MJxGJpBja_w` 753-873 s).
- **Mapa:** no aplica. Si hace falta, el puente del Bosque Kokiri.

### 4. La Ocarina de las Hadas de Saria ya no se pierde
- **Qué es:** en N64, al recibir la Ocarina del Tiempo de Zelda en el foso del castillo, la Ocarina de las Hadas de Saria desaparecía del inventario porque la sustituía. En el remake se quedan las dos y puedes elegir cuál tocar. GamingBolt lo presenta como un recuerdo que Link conserva al salir del bosque.
- **Fuentes:**
  - Nintendo Everything: «Saria's Ocarina and the Ocarina of Time are both in Link's inventory, and you can choose which to play» (https://nintendoeverything.com/?p=927180, 24-oct).
  - GamingBolt n.º 4, «Links to the Past».
- **Confianza:** ALTA.
- **Clip remake:** POR LOCALIZAR. Es la pantalla de inventario con las dos ocarinas, en el 100 % `oLHiQX2wxrE` después del capítulo «Link Meets Princess Zelda» (6323 s). La entrega de la Ocarina del Tiempo está en el foso (cinemáticas `L45cq1H2d1s`, ~116:00-136:00 min, «Play this song at the altar» en 135:43 [transcr.]).
- **N64:** Zelda da la ocarina bajo el agua en P11 `FO9OG9QXGS4` 1188-1233 s. Saria da la suya en el puente, P02 `MJxGJpBja_w` 753-873 s.
- **Mapa:** Bosque Kokiri (puente de salida) → campo de Hyrule → foso del castillo de Hyrule. Es una ruta corta.

### 5. Una quinta botella, y llega antes
- **Qué es:** en la Ciudadela, la primera vez que llegas de niño:
  - Un anciano en la puerta de la tienda de pociones avisa del alboroto: «Y'hear that ruckus? The owner of the Potion Shop is making some sor…».
  - Dentro, el dueño grita «Ack! A bug escaped!» y te presta una botella para atrapar un escarabajo dorado que corre por la tienda: «I beg you—use this empty bottle».
  - Al atraparlo, te la llena con una poción roja: «As a token of gratitude for your legendary capture, I give you our shop's signature product!».
  - En N64 había 4 botellas y la primera llegaba más tarde.
- **Por qué:** Aonuma, en Game Informer, dijo que de joven quería una botella más: «Because bottles are so important to the way the player plays the game… one thing that I suggested was that the player could get their first bottle earlier». También: «It strengthens that whole sequence through the game by changing the order just a little bit there».
- **Fuentes:**
  - Nintendo Everything (enlace del n.º 4).
  - Guía de VGC: https://www.videogameschronicle.com/guide/zelda-oot-remake-all-empty-bottle-locations/
  - KeenGamer: https://www.keengamer.com/articles/guides/zelda-ocarina-of-time-remake-all-5-empty-bottle-locations/
  - Entrevista de Game Informer: https://www.gameinformer.com/interview/2026/11/03/zelda-ocarina-remake-producers-talk-changing-and-maintaining-the-game-easter
  - Short `eCtVmlcJrFw` (Rocket Da Boost, 11-nov, 54 k vistas).
- **Confianza:** ALTA.
- **Clip remake:**
  - 100 % sin comentarios `oLHiQX2wxrE`, capítulo «Bottle #1» 5511-5771 s [capítulo].
  - Los textos citados arriba se ven en `eCtVmlcJrFw` 0:32-1:16 [visión], pero es vertical y con rótulos.
- **N64:** no hay escena equivalente. Tienda de pociones N64 (la de Kakariko) en P22 `csFvvR08QFY` 333-378 s.
- **Mapa:** Ciudadela de Hyrule, tienda de pociones junto al bazar de la plaza.

### 6. La Semilla del Mercader Deku: una tienda donde la lances
- **Qué es:** un objeto nuevo, la «Business Scrub Seed». Al lanzarla, aparece un vendedor Deku justo donde cae, así que puedes reponer flechas, bombas o semillas sin salir de la mazmorra. Se consigue en cofres, por ejemplo en la cueva bajo las columnas del Río Zora o en el Camino del Viento del Templo de las Sombras, según Zelda Central. Ocupa el hueco del tedio de N64, cuando te quedabas sin flechas en mitad de un templo.
- **Fuentes:**
  - Nintendo Everything, lista de novedades: «Throwing it summons a Deku merchant wherever it lands» (https://nintendoeverything.com/list-of-everything-new-in-the-zelda-ocarina-of-time-remake-improvements-changes-and-additions/, 19-oct).
  - Nintendo Everything, «details you may have missed» (enlace del n.º 4).
  - Zelda Central, secretos n.º 4 y 11: https://zeldacentral.com/games/ocarina-of-time-remake/secrets-and-easter-eggs/
- **Confianza:** ALTA.
- **Clip remake:** POR LOCALIZAR. Candidato: `z8awcvmtphY` («Legend of Zelda does dungeon business..», 101 s; título prometedor, sin verificar). Si no sirve, hay que buscarlo en el Templo del Bosque del 100 % `oLHiQX2wxrE` (30231 s en adelante).
- **N64:** los Deku vendedores eran fijos, en P13 `M--gXMSdJxY` 183-198 s.
- **Mapa:** Río Zora (cueva bajo las columnas de baldosa azul) y Templo de las Sombras, debajo de Kakariko.

### 7. ReDeads y Mano Muerta, rehechos para dar más miedo
- **Qué es:**
  - El grito de los ReDeads sigue paralizando a Link en cualquier pose, incluso en el aire si saltas para atacarlos. Ahora además hay luz roja y unas bandas rojas brillantes que lo envuelven, y Link forcejea.
  - Corren hacia ti, y su cuerpo parece de materia vegetal en vez de carne: «made of plant material rather than flesh and blood».
  - La Mano Muerta del Fondo del Pozo es una masa pálida con la cabeza de dientes que sale entre la niebla verde. Las manos salen del suelo.
- **Fuentes:**
  - KnightPohtaytoe `z4Hs1jwCHBo` (11-nov, 118 k vistas): 0:36-1:23 [transcr.].
  - Beta Brawler `XPvYWutj5ag`, «ReDead: N64 vs 3DS vs Switch 2» (7-nov, 100 k vistas).
  - Mano Muerta en `scLpqjbkI-8` 0:03-0:27 [visión].
- **Confianza:** MEDIA. Hay varios videos y se ve, pero ningún medio escrito.
- **Clip remake:**
  - ReDeads: comparativa `XPvYWutj5ag` (115 s, sin narrador, con los tres juegos), POR LOCALIZAR el segundo de cada versión. También `z4Hs1jwCHBo` 1:00-1:20 (con narrador).
  - Mano Muerta: BeardBear `Vh2jiWNbKIk` (114 s) o el capítulo «Dead Hand Mini-Boss» del 100 % `oLHiQX2wxrE`, 49364 s [capítulo].
- **N64:** ReDead en `XPvYWutj5ag`. Fondo del Pozo en P25 `OLY3yMVtNLE` 528-1188 s.
- **Mapa:** Ciudadela en ruinas (ReDeads de adulto) y Kakariko → Fondo del Pozo (Mano Muerta, de niño).

### 8. El soldado del callejón ya no muere, y la Ciudadela habla de la huida
- **Qué es:**
  - **N64:** en el callejón trasero de la Ciudadela, entre la huida de Zelda e Impa y el momento de sacar la Espada Maestra, Link niño encuentra a un soldado herido. Le pregunta si es «el chico del bosque», le cuenta que Ganondorf traicionó al rey y le indica el Templo del Tiempo. Después se calla y Navi dice «He's not moving anymore…».
  - **Remake:** el soldado sobrevive. Parece agotado, no agonizante, y puedes hablarle todas las veces que quieras.
  - Esa misma tarde, casi todos los vecinos hablan del caos. Una mujer grita «Cowards—all of you! I'm not leaving this town no matter what! I love this place». Otra piensa huir a la Ciudad Goron hasta que cae en que no puede comer piedras. A una niña le advierten de un «old man chasing people».
- **Fuentes:**
  - Kotaku, 9-nov: https://kotaku.com/zelda-ocarina-of-time-remakes-castle-town-has-a-scene-that-will-haunt-me-forever-2000755088
  - Resumen del buscador de Zelda Wiki y Fandom «Back Alley», sobre el soldado de N64.
- **Confianza:** MEDIA. La única fuente del cambio es Kotaku y no encontré clip del remake con el soldado.
- **Clip remake:** POR LOCALIZAR. En `s1BElOIu8us` (Sirloin, Ciudadela antes y después del salto temporal) miré cuadros cada 18 s y NO aparece. Candidato: el 100 % `oLHiQX2wxrE`, justo antes del capítulo «Temple of Time» (26151 s).
- **N64:** `LWNGI87ptq4` (Nikra, 103 s, escena completa).
- **Mapa:** Ciudadela de Hyrule, callejón trasero → Templo del Tiempo.
- **Aviso:** si no aparece el clip del remake, contarlo con la cita de Kotaku y el clip de N64, o recrear el plano en Flow marcado como recreación.

### 9. El Salón de los Enemigos Caídos se abre soñando
- **Qué es:** es un área secreta que no sale en el mapa.
  - **Se abre** al terminar el Templo del Bosque y volver a ser niño. En Kakariko, Kaepora Gaebora explica que se llega «a través de los sueños». Cualquier cama con brillo verde te lleva: la casa de Link, el Gran Albergue de Kakariko, la alfombra de la cabaña del laboratorio del lago y el campamento de carpinteros del Valle Gerudo.
  - **Estatuas:** una por cada tipo de enemigo derrotado, 84 en total.
  - **Revanchas:** cada jefe tiene revancha cronometrada con equipo fijo.
  - **Tres pruebas en cadena:**
    - de las Piedras Espirituales: Gohma, King Dodongo y Barinade.
    - de los Cinco Sabios.
    - del Héroe del Tiempo: todos, más Ganondorf y Ganon.
  - **Premios:** medallas maestras, ránking mundial en Zelda Notes y un trofeo que aparece en el cuarto de Link en el Bosque Kokiri. No da corazones ni objetos.
  - **Origen:** sustituye al «Boss Challenge» del 3DS. Nintendo of America lo llamó «Hall of Fallen Heroes» en su nota de prensa, pero en el juego se llama «Hall of Fallen Foes».
- **Fuentes:**
  - KeenGamer, 7-nov: https://www.keengamer.com/articles/guides/zelda-ocarina-of-time-how-to-unlock-the-hall-of-fallen-foes/
  - GamesRadar, titular «adds boss rematches with built-in speedrun tracking»: https://www.gamesradar.com/games/the-legend-of-zelda/zelda-ocarina-of-time-remake-adds-boss-rematches-with-built-in-speedrun-tracking-and-it-all-reminds-me-of-one-of-my-favorite-wind-waker-quests/
  - Nintendo Everything: https://nintendoeverything.com/the-legend-of-zelda-ocarina-of-time-remake-reveals-hall-of-fallen-foes/
  - Zelda Central, secretos n.º 20 (cama verde de la casa en ruinas del lago).
  - Videos: «All 84 Enemies» `QwotGZbH-TA`, medallas `bXK2m6v52kw`.
- **Confianza:** ALTA.
- **Clip remake:**
  - entrada por la cama: Trophy Tom `SAHDCv3emzA` (148 s, sin comentarios), POR LOCALIZAR el segundo de la cama.
  - el salón con estatuas: BeardBear `opfv1K35uNE` (15:04).
  - revanchas: UTAGaming `bXK2m6v52kw` (33:44).
- **N64:** no existía. El antecedente es el Boss Challenge del 3DS.
- **Mapa:** Kakariko (Kaepora) → camas: casa de Link (Bosque Kokiri), Gran Albergue (sur de Kakariko), laboratorio del Lago Hylia y campamento del Valle Gerudo. Es una buena ruta de 4 puntos.

### 10. Ganondorf ahora le habla a Link niño en el Templo del Tiempo
- **Qué es:** la escena del salto a adulto se amplió. Al sacar la Espada Maestra, Ganondorf entra y se burla de Link, y después hay una escena nueva de Ganondorf entrando en el Reino Sagrado y tomando la Trifuerza. Sus líneas nuevas, con voz:
  - «You're entertaining, I'll give you that. For a child at most. Did you truly expect that such juvenile tricks would fool me? I've known all along that you would be my key to the Door of Time…»
  - «The royal fools and their little hero fighting so hard just to hand me the Sacred Realm. Now this world and the Triforce belong to me… Mourn your losses and choke on your bitter failures forever.»
  - Rauru también tiene texto nuevo («You may feel disoriented at the moment…»), y Navi, al ver a Link adulto, dice «Wow… you got really big. You grew so much».
- **Por qué:** Aonuma en Game Informer: la escena original «was very low on explanation», así que querían «something that explains his presence, that explains his reaction».
- **Fuentes:** entrevista de Game Informer (enlace del n.º 5) + transcripción del juego en dos videos.
- **Confianza:** ALTA.
- **Clip remake (sin comentarios):**
  - LunarGaming `8nSoklvmLkM`: espada 1:06, Ganondorf 2:37-4:30, Rauru 4:49-5:51, Navi 6:08 [transcr.]. Capítulos: 0 «Discovery of the Master Sword», 156 «Ganondorf's betrayal», 289 «Awakening in the future».
  - Gamer's Little Playground `ylu5K9T_T0w`, «Ganondorf Enters The Sacred Realm NEW Scene» (14:56).
  - Cinemáticas GLP `L45cq1H2d1s` 139:57-148:00 min, es decir 8397-8880 s [transcr.].
- **N64:** Espada Maestra y Ganondorf en blanco en P13 `M--gXMSdJxY` 618-708 s. Rauru y la Cámara de los Sabios en 753-918 s. En N64 Ganondorf solo tenía texto («I knew you held the key…»), sin escena en el Reino Sagrado.
- **Mapa:** Ciudadela → Templo del Tiempo (norte de la plaza) → Reino Sagrado. En el mapa: punto del Templo con un salto en blanco.

### 11. Los sabios no estaban muertos: Rauru los salvó
- **Qué es:** en N64 nunca quedaba claro qué pasaba con los sabios. Saria, Darunia, Ruto y Nabooru desaparecían en sus templos, y la comunidad debatió 28 años si habían muerto. En el remake, las escenas de la Cámara de los Sabios tienen líneas nuevas que lo aclaran: Rauru los sacó de allí.
  - Saria: «I was making my way through the Forest Temple when I was summoned to this place by Rauru the sage… I can never return to the world I knew.»
  - Darunia: «I hate to say it, but I'd be a pile of gravel right now if Rauru hadn't pulled me outta the fire back there.»
  - Ruto: «Surely that's why I was drawn into the temple.»
- **Fuentes:**
  - Boss Rush Banter, 9-nov: https://bossrush.net/2026/11/boss-rush-banter-the-ocarina-of-time-remake-finally-settles-a-long-debated-fan-theory-about-the-sages/
  - La transcripción del juego confirma las tres frases: `L45cq1H2d1s` 178:13 (Saria), 203:14 (Darunia) y 218:39 (Ruto).
  - Debate previo en el foro de Zelda Dungeon: https://www.zeldadungeon.net/forum/threads/sages-and-their-awakening.41392/
- **Confianza:** ALTA para las frases, porque se oyen en el juego. MEDIA para la lectura «los salvó», que es interpretación de Boss Rush, aunque las frases la apoyan.
- **Clip remake (sin comentarios):** cinemáticas GLP `L45cq1H2d1s`:
  - Saria: 10693-10760 s (178:13-179:20).
  - Darunia: 12194-12240 s (203:14).
  - Ruto: 13119-13160 s (218:39) [transcr.].
- **N64:** los sabios sellan a Ganondorf en P35 `F2Pp2qU3QWI` 603-633 s. La Cámara de los Sabios con Rauru, en P13 753-918 s.
- **Mapa:** Templo del Bosque (Bosque Sagrado), Templo del Fuego (cráter de la Montaña de la Muerte) y Templo del Agua (Lago Hylia), unidos al centro con la Cámara de los Sabios. Es una buena ruta.

### 12. La Máscara de la Verdad ahora lee pensamientos, y depende de por dónde te acerques
- **Qué es:** en N64, la Máscara de la Verdad servía para entender a las Piedras Chismosas, y la gente solo reaccionaba a tu cara. En el remake, Link lee lo que piensa cada personaje:
  - Si llegas de frente, el personaje ve la máscara y reacciona. Si llegas por detrás, sin que te vea, sale lo que piensa de verdad, con frases distintas y a veces con su historia.
  - El guardia de Kakariko que pedía la máscara Keaton «para su hijo» confiesa, por la espalda, que era para él. Si no se la vendes, cierra la verja hasta que se la des.
  - Un barbudo se pregunta si las barbas son tan sucias como un retrete. Un niño persigue un cuco con intención de comérselo.
  - En la pareja que baila (Honey y Darling), según a quién tengas más cerca, oyes la versión de ella o la de él, que es más oscura.
  - El Rey Zora revela preocupaciones que esconde (GamingBolt). Hasta las vacas tienen pensamientos.
- **Fuentes:**
  - GameSpot, «25 Things You STILL Didn't Know», `-0cwlyMdre8` (5:41-8:15 [transcr.]).
  - GamingBolt n.º 2, 11-nov.
  - Videos: Sirloin `niOLyw2vhCU` (12 min), YTSunny `GzNjaJjivWM` (18 min) y goodgamez `PH83O4Z90Q4` (52 min), todos «Mask of Truth Hidden Dialogues».
- **Confianza:** ALTA.
- **Clip remake:** `-0cwlyMdre8` 5:41-8:15 (con narrador; tiene el guardia Keaton en 7:03-7:52). Sin comentarios: Sirloin `niOLyw2vhCU`, POR LOCALIZAR el guardia Keaton.
- **N64:** Piedras Chismosas con la Máscara de la Verdad; Piedra Chismosa «cohete» en `x7uGxymMbSs` (87 s, del catálogo de `zelda_oot`). Guardia de Kakariko en P04 `Q53ffTZRmQk` 618-633 s.
- **Mapa:** Kakariko (guardia de la verja de la Montaña de la Muerte), plaza de la Ciudadela (pareja, niño del cuco) y Dominio Zora (Rey Zora).

### 13. Master Quest está escondido en el código, detrás de un DLC
- **Qué es:** el remake salió sin Master Quest (ya contado en `oot_remake_eliminado`). Pero el 6 y 7 de noviembre los dataminers encontraron en el ejecutable del juego todo lo necesario para activarlo:
  - **Lo que encontró MrCheeze:** cadenas como `HasMQ`, `IsMQModeExist`, `NewGameMQ` y `ReleaseMQ`, y la etiqueta «MQ» junto a «DodongoCavern».
  - **Lo que añadió OatmealDome:** se activa por poseer un DLC, no con una actualización, el mundo está en espejo y las mazmorras cambian. Su ejemplo: vacas dentro de la tripa de Jabu-Jabu.
  - **Lo que añadió Twisted Voxel:** los cambios parecen limitarse a las mazmorras, y el juego comprueba un solo paquete DLC.
  - Aonuma, cuando IGN le preguntó, no lo negó: «I don't think that we would announce anything specific at this time».
- **Fuentes:**
  - Nintendo Everything, 7-nov: https://nintendoeverything.com/?p=929206
  - VGC: https://www.videogameschronicle.com/news/zelda-ocarina-of-time-switch-2-could-be-getting-master-quest-dlc/
  - Kotaku: https://kotaku.com/zelda-ocarina-of-time-remake-master-quest-dlc-majoras-mask-2000755101
  - GamesRadar: https://www.gamesradar.com/games/the-legend-of-zelda/zelda-ocarina-of-time-remake-files-hint-at-master-quest-dlc-and-majoras-mask-remake-dataminers-claim/
- **Confianza:** ALTA de que el código existe. Nintendo no lo ha confirmado, así que se dice «según los dataminers».
- **Clip:**
  - koadyokay `Rg8y2Pd1PgA`, «Master Quest Isn't All They Found» (10-nov, 104 k vistas): capítulos 78 «What Dataminers Found», 294 «Ever Shot A Cow?» (vacas en la pared, 0:03 [transcr.]) y 408 «What Aonuma Said». Tiene narrador.
  - Video en español de HGuerrero `CXhA3KS9WKA`.
  - Para enseñarlo: captura del post de MrCheeze (citada en las notas) y Master Quest de GameCube `IFldCvi-4cY` o `nuTYYvrbksY`.
- **N64 y GameCube:** Master Quest de 2003 (GameCube) y 3DS 2011. Viene del «Ura Zelda» del 64DD (`ZbmIjimU9e0` en el catálogo).
- **Mapa:** Caverna de los Dodongos (Montaña de la Muerte) y la tripa de Jabu-Jabu (Fuente Zora). Vale un mapa en espejo como gag visual, marcado como ilustración.

### 14. Una máscara de amiibo que todavía no existe, con 173 líneas de diálogo
- **Qué es:**
  - En el código, las máscaras de los amiibo anunciados son `Mask_101` (Link niño) y `Mask_102` (Zelda niña). Hay una tercera, **`Mask_103`**, sin amiibo anunciado.
  - Tiene unas 173 líneas propias de reacción de los PNJ. Austin John Plays las contó; Nintendo Everything dice «close to 200».
  - Los personajes la llaman rara, de otro mundo, inquietante y «un monstruo». Uno dice que mirarla le hace sentirse raro, y el hijo del maestro carpintero pregunta si vienes a por él. Nadie la reconoce.
  - Algunos de los que reaccionan mal son personajes que no llegan vivos al salto de siete años.
  - La teoría es un amiibo de Skull Kid ligado a un remake de Majora's Mask. Nintendo no ha anunciado nada de eso.
- **Más pistas «Majora»** (todas BAJAS, de jugadores; citadas por koadyokay):
  - el Vendedor de Máscaras Felices lleva los brazaletes de oro que solo tenía en Majora's Mask.
  - la potrilla Epona tiene una animación de nadar, que encontró el usuario de X «YoungCamary».
  - Ingo dice «I think I'm going to cry», que recuerda al jefe de la compañía de circo de Majora.
- **Fuentes:**
  - Nintendo Everything, 9-nov: https://nintendoeverything.com/ocarina-of-time-datamine-suggests-unannounced-zelda-amiibo-coming-potential-majoras-mask-remake/
  - GameRant: https://gamerant.com/zelda-ocarina-of-time-skull-kid-amiibo-majoras-mask-remake/
  - Kotaku (enlace del n.º 13).
  - AllKeyShop: https://www.allkeyshop.com/blog/zelda-ocarina-of-time-remake-sales-datamine-news-r/
  - Video koadyokay `Rg8y2Pd1PgA`: capítulos 543, 612 «173 New Code Lines», 688 y 745 [transcr.].
- **Confianza:** MEDIA que el hallazgo existe (varios medios, con atribución a Austin John Plays). BAJA para la teoría de Skull Kid y Majora; decirlo como teoría de los fans.
- **Clip:** `Rg8y2Pd1PgA` 543-819 s (con narrador). Para la imagen: amiibo anunciados en el Direct de septiembre (`wuFfiTEr2yc`, del catálogo). Skull Kid en el Bosque Perdido del remake: `Go0khcpjGEA` 0:00-0:10 [visión], que conecta con la pista falsa del jefe secreto.
- **N64:** Skull Kid en el Bosque Perdido (`g70dvKoI6I4`). Majora's Mask N64 en `DZjrIHXIrIM` (del catálogo).
- **Mapa:** Bosque Perdido, tocón de Skull Kid. Sirve de cierre: «el último punto del mapa es uno que todavía no existe».

---

## 2. Reserva (si sobra tiempo o falta un puesto)
- **El guardia de la bomba duda si estás junto a Zelda:** no la tira para no ponerla en peligro. Solo lo cuenta GameSpot `-0cwlyMdre8` 3:44-3:59. Confianza BAJA-MEDIA. Es un remate del guardia que ya enseñamos en el video anterior.
- **Los dibujos de Malon en el segundo piso de Lon Lon:** la Ciudadela, Epona, la casa, y Talon, Malon e Ingo juntos. GameSpot 2:58-3:13. Confianza BAJA-MEDIA.
- **Mapa ilustrado con una niña gerudo**, cuando nunca hubo niñas gerudo en el juego. GameSpot 4:31-4:59. Confianza BAJA.
- **Kaepora Gaebora te tira al lago a propósito** en el vuelo al Lago Hylia. Solo GamingBolt n.º 13. Confianza BAJA.
- **Rutinas del mercado:** los vendedores pregonan de día, recogen al atardecer y se van a casa de noche. GamingBolt n.º 14. Choca en parte con el «día y noche en los pueblos» ya contado.
- **Fuego de Din en tiempo real:** el mundo ya no se congela al lanzarlo. Nintendo Everything. Un espantapájaros de entrenamiento en la tienda Kokiri y una mujer rubia nueva en la Ciudadela que te advierte que no gastes todo. Las dos solo en Nintendo Everything.
- **Escarabajos en la planta de judías** que sacan una Skulltula dorada, y **la Canción de las Tormentas junto a una judía** que cura. Lo cuenta GameSpot, pero no aclara si es nuevo; no usar como añadido sin comprobarlo.

---

## 3. Propuestas de gancho (1 frase)
1. «En el código del nuevo Ocarina of Time hay una máscara que todavía no puedes usar, con 173 frases escritas para ella, y nadie en Hyrule la reconoce.»
2. «28 años después, Nintendo por fin contestó la pregunta más oscura de Ocarina of Time: qué les pasó a los sabios. Y lo hizo sin anunciarlo.»
3. «El remake trae una pelea de jefe secreta con Skull Kid… o eso dicen 100 000 personas. La verdad es más rara, y hay otras 14 cosas que Nintendo metió sin avisar.»

---

## 4. Ventas y récords de la semana (verificado)
- **Ventas:** más de **5,2 millones** de copias en los primeros **cuatro días** en todo el mundo, físicas y digitales. Nintendo lo anunció el **11-nov-2026**. De ellas, **810 000 en Japón**.
- **Récord:** Nintendo dice que es el mejor lanzamiento de cuatro días de un juego editado por Nintendo en Switch 2, y el que más rápido ha vendido en todo el mundo y en EE. UU., Canadá y Latinoamérica.
  - Fuentes: https://www.dexerto.com/gaming/zelda-ocarina-of-time-remake-sells-5-2-million-copies-in-four-days-to-break-switch-2-record-3427243/ · https://www.notebookcheck.net/Zelda-Ocarina-of-Time-remake-sells-5-2-million-sets-Nintendo-Switch-2-record.1447824.0.html · https://www.vice.com/en/article/zelda-ocarina-of-time-remake-sales-worldwide/ · Variety (de pago, solo el titular): https://variety.com/2026/gaming/news/legend-of-zelda-ocarina-of-time-sales-remake-5-million-copies-1236945069/
- **Comparación:**
  - el N64 vendió **7,6 millones** en toda su vida, así que en 4 días el remake ya lleva cerca del 70 % (cálculo de Kotaku).
  - Ocarina of Time 3D: 6,44 millones (Dexerto).
  - Tears of the Kingdom: más de 10 millones en 3 días.
  - Fuente: https://kotaku.com/zelda-ocarina-of-time-remake-nintendo-64-sales-figures-switch-2-2000755871
- **Reino Unido:** número 1 en ventas físicas, con un lanzamiento físico ~35 % mayor que el de Breath of the Wild y el mejor del año en el país. Esto lo recoge el resumen del buscador de una sola fuente; hay que comprobarlo antes de decirlo.
- **Nota:** Metacritic 96, el más alto de 2026 (ya contado en `oot_remake_eliminado`; Dexerto lo repite).

---

## 5. Avisos para el guion
- **La pista del «jefe secreto de Skull Kid» es clickbait.** Si se usa, que sea como desmentido con burla: «lleva ahí desde 1998». No la presentes como añadido.
- **Datamines (n.º 13 y 14):** decir siempre «según los dataminers». En el n.º 14, la cifra es «173 líneas» según Austin John Plays y koadyokay, o «cerca de 200» según Nintendo Everything. Elegir una y decir de dónde sale.
- **El soldado (n.º 8)** depende solo de Kotaku y falta el clip del remake. Si no aparece, bajarlo a la reserva o contarlo con el clip de N64 y la cita.
- **POR LOCALIZAR:** Korok (n.º 2), las dos ocarinas en el inventario (n.º 4), la Semilla Deku en uso (n.º 6), el soldado (n.º 8), la cama del Salón (n.º 9) y el guardia Keaton sin narrador (n.º 12). Mirar el cuadro antes de meterlos en `beats`, como pide la regla de promesas visuales.
- **Herramientas que no funcionaron:**
  - `watch_youtube_video_and_ask` de Nexlev no está en el plan gratuito.
  - vidIQ se quedó con 5 créditos tras un solo `vidiq_video_watch`.
  - Zelda Wiki y Zelda Dungeon devuelven 403. Variety es de pago.
  - yt-dlp dio un 429 suelto con los subtítulos; al reintentar uno por uno funcionó.
- Los clips que bajé para mirar cuadros están solo en la carpeta temporal de la sesión, no en el proyecto.
