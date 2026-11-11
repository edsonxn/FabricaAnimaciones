# J5 — Semifinal BLG vs T1, partida 3 (gameId 115660540726095124) — la pelea del alma infernal (investigado el 10-nov-2026)
Fuentes: feed oficial (`feed_124.txt` + `window` del feed para torres/dragones/barones), metadatos del feed (campeones), subtítulos automáticos es (`subs/Tq2FdhgReuI.es.vtt`; escriben Oner = «Honer», Peyz = «Pace», Knight = «K»/«Night», Xun = «Shun», Bin = «Vin», Mega Gnar = «Meganar»), cuadros 1080p de `medios/_fuente/j5.mp4` y del VOD.

## Reloj (MEDIDO en cuadros) — en la voz SIEMPRE el HUD
| | Valor | Cuadros de control |
|---|---|---|
| VOD es-MX | **Tq2FdhgReuI** (2 685 s, «BLG vs T1 … JUEGO 3») | |
| **K (VOD = HUD + K)** | **451** | VOD 2300 = 30:49 · VOD 2400 = 32:29 · VOD 2357 (j5 t=2) = 31:46 · VOD 2503 (t=148) = 34:12 |
| **K_fuente (HUD = t + K_fuente)** | **1904** | t=2 → 31:46 · t=30 → 32:14 · t=60 → 32:44 · t=90 → 33:14 · t=148 → 34:12 |
| feed − HUD | **+4 a +6** | Oner: HUD 32:43 ↔ feed 32:48 · Bin 32:46 ↔ 32:50 · Doran 32:49 ↔ 32:54 · Knight 33:00 ↔ 33:06 · Peyz/Keria 33:05-06 ↔ 33:10-11 |
Fuente: `medios/_fuente/j5.mp4` = VOD 2355 + 150 s (HUD 31:44 → 34:14). Sin pausas técnicas en el tramo.

## Campeones (metadatos del feed) — BLG azul
BLG: Bin Gnar · Xun Pantheon · Knight Taliyah · Viper Ezreal · ON Nami.
T1: Doran Ambessa · Oner Jarvan IV · Faker Ahri · Peyz Sivir · Keria Karma.

## Marcador en la jugada (leído en el HUD; torres/dragones/barones del feed)
| HUD | Asesinatos BLG-T1 | Oro (dif.) | Torres (feed) | Dragones | Barones |
|---|---|---|---|---|---|
| 31:46 | 12-8 | 62,1K / 58,2K (**+3,9K**) | 7-2 | BLG 3 (océano, 2 infernales) · T1 2 (nube, infernal) | BLG 1 |
| 32:44 | 13-8 | +4,5K | 7-2 | igual | |
| 32:46 | 13-9 | +3,5K | | | |
| 32:54 | 14-9 | +4,0K | | **BLG 4 = ALMA INFERNAL** | |
| 33:01 | 14-10 | +2,9K | | | |
| 33:06 | **16-10** | +3,9K | **7-3** (cae una torre de BLG, 33:03) | BLG 4 · T1 2 | BLG 1 |
| 34:12 | 16-10 | 68,2K / 63,8K (+4,4K) | | | |
Feed: +3 851 (32:48) → +2 626 (33:11). Contexto (solo feed, HUD ≈ feed − 5): T1 había remontado a **8-8** (feed 22:36, oro −151); BLG 2.º Barón ≈36:00 (feed 36:04); **nexo ≈36:52** (feed 36:57, 19-10, +8,6K). Ninguno de los tres medido en cuadro.

## Tomas sin corte (`camaras.py` → `cam_j5.json`, revisados a mano)
- 0,5 → 31,5 y 31,5 → 36,6: en vivo, lado inferior (Knight llega con teleport según la narración, t≈31).
- 37,1 → 48,8: en vivo, foso del dragón.
- **48,9 → 92,5** (HUD 32:33 → 33:16): **TODA la pelea, el dragón y el doble de Viper.** Entre 72 y 74,5 la cámara se desplaza (paneo) del foso hacia el carril central; los «cortes» que marca el detector en 74,7 y 75,6 son destellos (74,6 y 74,9 son la misma escena), no cortes.
- 92,5 → 93,8 cortinilla; **93,8 → 140,0: REPETICIÓN** («Moment of the game», sin HUD). No vale como acción en vivo.
- 141,4 → 150: en vivo (tabla de daño de la pelea).

## Paso a paso (foso del dragón, río inferior; minimapa abajo a la derecha)
Narración, VOD 2376-2381 (t 21-26): «no tienen visión alrededor del dragón». VOD 2398-2402 (t 43-47): BLG esperando «para utilizar el muro de la tejedora [Taliyah] y evitar que tengan posición los chicos de T1».
| t | HUD | Qué se ve |
|---|---|---|
| 40 | 32:24 | Rótulo **«Dragon has spawned!»** |
| 44-46 | 32:28-32:30 | Dragón 7 637. T1 en el borde del foso (Doran, Keria, Peyz, Oner junto al dragón; Faker a la izquierda). BLG en el río (Viper, Xun, ON, Bin; Knight arriba). +3,8K |
| 48,6 | 32:33 | Xun «STUNNED» entre Keria y Peyz; dragón 5 769 |
| 49-51 | 32:33-32:35 | Muro de Taliyah sobre el río. **«BLG Viper RESURRECTING»**: Viper muere y vuelve (el feed no lo cuenta como muerte) |
| 53-58 | 32:37-32:42 | Campo de rocas de Taliyah entre el foso y el río; dragón 5 302 → 4 195. Bin dentro del foso con Doran y Keria |
| 59 | 32:43 | Rótulo **«BLG Knight has slain T1 Oner!»** (13-8, +4,5K en 32:44); dragón 4 032 |
| 62 | 32:46 | «SHUT DOWN!»: **cae Bin** (13-9, +3,5K; feed: Doran). Knight encima de Doran |
| 65 | 32:49 | Rótulo **«BLG Xun has slain T1 Doran!»** (14-9 en 32:50); dragón 3 174 |
| 68,5 | 32:53 | Dragón 1 902; Xun y ON en el foso |
| 70-70,5 | 32:54-32:55 | **«Blue team has slain the Infernal Drake!»** + rótulo «INFERNAL DRAKE» y panel «DRAGON SOUL»: BLG 4.º dragón = **alma infernal** (HUD: 3 iconos en 32:52, 4 en 32:54) |
| 72-74,5 | 32:56-32:58 | La cámara sube al carril central: Keria y Peyz frente a Knight, Viper y ON |
| 76 | 33:00 | «SHUT DOWN!»: **cae Knight** (14-10 en 33:01, +2,9K; feed: Peyz) |
| 79 | 33:03 | **«Blue turret destroyed!»** (T1 tumba una torre de BLG en el centro; feed torres 7-3) |
| 81 | 33:05 | Xun encima de Keria; Viper al lado |
| 82 | 33:06 | **16-10, +3,9K**: Viper mata a Peyz y a Keria (feed 33:10 y 33:11) |
| 84 | 33:08 | Rótulo **«DOUBLE KILL!»** (Viper) |
Resumen: entre 32:43 y 33:06 BLG mata a **Oner, Doran, Peyz y Keria** y se lleva el **alma infernal**; pierde a **Bin y Knight** (y Viper se salva por la resurrección). T1 se lleva una torre central.

## Narración (segundo de VOD; citas cortas)
- VOD 2421-2426: «esto va a ser tanto dragón, alma del dragón infernal, como Barón».
- VOD 2428-2432: Faker usa la teleportación «para poder salir».
- VOD 2438-2440: «hizo tiempo para que llegara Viper, para que se llevara el doble asesinato».
- VOD 2452-2457 (repetición): «viene K[night] para cerrarlos y ahí atrapan completamente a Oner, que queda muy sobreextendido».
- VOD 2486-2490 (repetición): «te llevas … la torreta [central], por lo menos para compensar algo, pero no es la mejor jugada del mundo».
- VOD 2496-2500: «cómo se separan y cómo no se coordinan bien para esa iniciación es clave» (sobre T1).

## Por qué la gana BLG (solo lo visto y lo narrado)
BLG espera en el río con el muro de Taliyah mientras T1 se mete en el foso del dragón sin visión alrededor (narración). Oner queda sobreextendido y Knight lo caza (32:43); Bin cae, pero Xun mata a Doran (32:49) y BLG asegura el 4.º dragón: alma infernal (32:54). Faker se va con teleport. En el carril central T1 cobra a Knight y una torre, pero Viper (que ya había resucitado a las 32:35) mata a Peyz y Keria: 16-10. Según los narradores, T1 se separa y no coordina la iniciación.

## Pausas: PIES medidos (fracción del cuadro completo, 1280×720; rejilla `previews/cuadros/r_j5_<t>.jpg`)
Coordenadas de pantalla (la cámara se mueve: compensar con `cam_j5.json`). «(media)» = pies tapados o deducidos del cuerpo bajo la barra; sin coordenada = bajo el HUD o sin identificar.
- **t=46 (32:30, antes de la pelea; cámara quieta, los 10 visibles):** Doran .365,.21 · Keria .30,.28 · Peyz .31,.45 (media) · Oner .35,.50 (media, junto al dragón) · Faker .13,.64 · Knight .60,.15 · Viper .52,.40 · Xun .49,.49 · ON .59,.47 · Bin .57,.64 · dragón (centro del foso) .36,.47.
- **t=62 (32:46, Oner muerto, Bin cayendo; cámara quieta):** Knight + Doran .37,.34 (anillo común) · Viper + ON .485,.44 (encimados) · Xun .545,.51 · Keria .21,.65 · dragón .35,.60. Faker bajo el HUD (barra en .19,.725). Peyz: fuera de cuadro. Bin: muerto.
- **t=66,5 (32:50, tras matar a Doran; cámara quieta):** Keria .05,.49 · Viper .58,.28 · ON .53,.47 (media) · Xun .59,.61 · Knight .41,.29 (media, barra de nivel 17 sin nombre). Dos campeones de T1 sin nombre legible en .22,.49 y .405,.52 (Peyz/Faker: sin identificar).
- **t=81 (33:05, carril central, antes del doble de Viper):** Xun + Keria .40,.50 (encimados) · Viper .52,.48 · ON .68,.46 (media). Peyz: sin identificar.
- **Rutas (toma 48,9 → 92,5, con paneo: compensar):** Xun [(62, .545,.51), (66.5, .59,.61)] (t=46 es de la toma anterior, 37,1 → 48,8: no unir) · Viper [(62, .485,.44), (66.5, .58,.28)].

## ⚠ Sin verificar / cuidado
- **Viper «RESURRECTING» (32:35):** se ve el rótulo; quién lo mata antes no está medido. No es muerte en el feed: no contarla en el marcador.
- La muerte de Knight y la de Bin: el asesino sale del feed (Peyz, Doran); el cuadro solo enseña «SHUT DOWN!».
- «Faker se va con teleport» y «Oner sobreextendido» son de la narración (la segunda, sobre la repetición).
- Feed: «dr 4-2» aparece en 33:06, pero el HUD ya marca el 4.º dragón en 32:54: usar el HUD.
- El 8-8, el 2.º Barón y el cierre (≈36:52) son del feed − 5, sin cuadro. «La que pone a BLG 2-1»: dato del encargo, no comprobado aquí.
