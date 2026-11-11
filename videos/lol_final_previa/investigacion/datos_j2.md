# J2 — Cuartos BLG vs DK, partida 1 (gameId 115660540726095098) — Xun y el Heraldo (investigado el 10-nov-2026)
Fuentes: feed oficial (`feed_098.txt` + `window` del feed para torres/dragones), metadatos del feed (campeones), subtítulos automáticos es (`subs/oXxOe-hbAtA.es.vtt`; escriben Akali = «la Cali», BLG = «Billy Billy», Career = «Carrier»), cuadros 1080p de `medios/_fuente/j2.mp4` y del VOD.

## Reloj (MEDIDO en cuadros) — en la voz SIEMPRE el HUD
| | Valor | Cuadros de control |
|---|---|---|
| VOD es-MX | **oXxOe-hbAtA** (2 445 s, «DK vs BLG … JUEGO 1») | |
| **K (VOD = HUD + K)** | **435** | VOD 1300 = 14:25 · VOD 1360 = 15:25 · VOD 1347 (j2 t=2) = 15:12 · VOD 1493 (t=148) = 17:38 |
| **K_fuente (HUD = t + K_fuente)** | **910** | t=2 → 15:12 · t=30 → 15:40 · t=60 → 16:10 · t=90 → 16:40 · t=148 → 17:38 |
| feed − HUD | **+4 a +6** | Lucid: HUD 16:09 ↔ feed 16:13 · Career: 16:13 ↔ 16:17 · ShowMaker: ≈16:27 ↔ 16:33 |
Fuente: `medios/_fuente/j2.mp4` = VOD 1345 + 150 s (HUD 15:10 → 17:40). Sin pausas técnicas en el tramo.

## Campeones (metadatos del feed) — BLG azul
BLG: Bin Ambessa · **Xun Naafiri** (comprobado: feed y rótulo «BLG Xun» sobre la Naafiri) · Knight Galio · Viper Cassiopeia · ON Nautilus.
DK: Siwoo Rumble · Lucid Qiyana · ShowMaker Akali · Smash Corki · Career Rell.

## Marcador en la jugada (leído en el HUD)
| HUD | Asesinatos BLG-DK | Oro BLG / DK (dif.) | Torres | Dragones |
|---|---|---|---|---|
| 15:12 | 4-3 | 26,3K / 26,8K (**−0,5K**) | 0-0 | BLG 2 (feed: infernal, montaña) · DK 0 |
| 16:04 | 4-3 | 27,7K / 28,0K (−0,3K) | 0-0 | igual |
| 16:13 | 6-4 | 28,8K / 28,7K (−0,1K) | 0-0 | igual |
| 16:28 | **7-4** | 29,7K / 29,0K (**+0,7K**) | 0-0 | igual |
| 16:37 | 7-4 | 30,0K / 29,2K (+0,8K) | 0-0 | igual |
Feed: −320 (16:13) → **+176** (16:33). La segunda fila del HUD marca 1 (BLG) y 2 (DK) con otro icono (probablemente larvas; sin confirmar). ⚠ El feed da 4 asesinatos a DK antes de la pelea (cuenta la muerte de Xun de 13:26 sin asesino); el HUD marca 3.

## Tomas sin corte (cortes detectados con `camaras.py` → `cam_j2.json`, revisados a mano donde importa)
- **40,6 → 71,4** (HUD 15:51 → 16:21): toda la pelea del río y el principio de la persecución. En 67,8 el detector marca un corte pero es un paneo rápido siguiendo a Xun (67,6 y 68,0 son la misma escena).
- 71,4 → 77,2: OTRA zona (ON, Knight y Siwoo junto al Heraldo invocado, lado superior). **La muerte de ShowMaker NO se ve en vivo.**
- 77,2 → 81,9: vuelta con Xun y Viper; ShowMaker ya muerto.
- 83,2 → 98,9: otras zonas / tabla de oro. 98,9-100,2 cortinilla.
- **100,2 → 124,8: REPETICIÓN** (rótulo «REPLAY»: la pelea del río hasta el DOUBLE KILL; no enseña la muerte de ShowMaker). No vale como acción en vivo.
- 125,5 → 136,1 y siguientes: en vivo (dragón químico, ≈17:20). Antes de 40,6 (cortes 19,0 / 22,4 / 39,8) no revisado a mano.

## Paso a paso (lado superior del mapa: río junto al foso del Heraldo; minimapa en t=50 y 65)
Narración, VOD 1393-1403 (t 48-58): «se logran llevar el heraldo de la grieta, están ahora buscando a Lucid, está demasiado adelante … les permite iniciar una pelea grupal, también está llegando Carrier [Career] … se llevan a Lucid».
| t | HUD | Qué se ve |
|---|---|---|
| 44 | 15:54 | BLG pegándole al Heraldo (4 354 de vida) en el foso: Xun, Knight, ON y Viper. Lucid y Career (DK) dentro del río, encima de ON |
| 47 | 15:57 | Heraldo 3 935. Siwoo llega por arriba; Smash abajo a la derecha |
| 50 | 16:00 | Rótulo **«Blue team has defeated the Rift Herald!»**. ShowMaker entra por la IZQUIERDA (flanco); Lucid y Career pegados a ON |
| 57 | 16:07 | **«Blue team has summoned the Rift Herald!»** (BLG lo invoca al momento). Un DK de nivel 11 «SUPPRESSED» (por la narración, Lucid) y Bin «UNSTOPPABLE» (la definitiva de Ambessa); Xun a la izquierda, junto a un DK de nivel 11 |
| 59 | 16:09 | Rótulo **«BLG Xun has slain DK Lucid!»** (5-3 en 16:10) |
| 62 | 16:12 | «SHUT DOWN!»: **cae Bin** (5-4; feed: lo mata ShowMaker) |
| 63,5 | 16:13 | 6-4: **cae Career** (feed: Xun) |
| 65 | 16:15 | Rótulo **«DOUBLE KILL!»** (Xun). Xun y Knight juntos, Viper debajo, Smash a la derecha; ShowMaker con poca vida, abajo a la izquierda |
| 67,5-71,2 | 16:17-16:21 | **Xun persigue a ShowMaker** (≈ un cuarto de vida) hacia la jungla superior de BLG (minimapa); Viper detrás |
| 71,4 | 16:21 | Corte a otra zona (ver tomas) |
| 77,25 | 16:27 | Vuelve la cámara: rótulo **«BLG Xun is on a killing spree!»**; ShowMaker ya no está (muerto). 16:28: **7-4, +0,7K** |
Resumen de la pelea en el HUD: BLG 4→7, DK 3→4; **los 3 asesinatos de BLG son de Xun** (Lucid 16:09, Career 16:13, ShowMaker ≈16:27); BLG pierde a Bin.

## Narración (segundo de VOD; citas cortas)
- VOD 1393-1403: «están ahora buscando a Lucid, está demasiado adelante … se llevan a Lucid».
- VOD 1414-1423: «Showmaker intenta escapar … está mal posicionado … quien no sobrevive es la Cali [Akali]».
- VOD 1441-1445: «Billy Billy [BLG] jugando mucho mejor en el tema de las peleas de equipo».
- VOD 1453-1477 (sobre la repetición): «Smash no se puede ni acercar porque Viper lo está [zoneando] … Viper es quien hace el gran trabajo para evitar que Smash se pueda acercar».
- VOD 1479-1482: «ahora recuperan la diferencia de oro».

## Por qué la gana BLG (solo lo visto y lo narrado)
BLG se queda el Heraldo (16:00) y lo invoca en el acto; DK entra a pelear con Lucid muy adelantado y los narradores lo señalan como el error. Bin le cae encima con la definitiva (SUPPRESSED/UNSTOPPABLE) y Xun remata a Lucid (16:09) y a Career (16:13): DOUBLE KILL. DK solo se cobra a Bin. ShowMaker, al que la narración ve mal colocado, huye con poca vida hacia la jungla de BLG y Xun lo persigue hasta matarlo (≈16:27, fuera de cámara). Según la narración, Viper mantiene a Smash fuera de la pelea. El oro pasa de −0,5K a +0,7K.

## Pausas: PIES medidos (fracción del cuadro completo, 1280×720; rejilla `previews/cuadros/r_j2_<t>.jpg`)
Coordenadas de pantalla (la cámara se mueve: compensar con `cam_j2.json`). «(media)» = pies tapados o deducidos del cuerpo bajo la barra; sin coordenada = bajo el HUD o sin identificar.
- **t=47 (15:57):** Xun .24,.39 (media, entre los efectos de las mascotas) · Siwoo .40,.19 · Lucid .49,.38 (media) · Career .45,.48 (media) · ON .43,.60 · Knight .30,.71 (media) · Heraldo (centro) .32,.36. Viper y Smash: bajo el HUD. Bin: sin identificar.
- **t=50 (16:00, Heraldo muerto, toma calmada):** Xun .30,.43 · ON .43,.43 · Knight .44,.57 · Lucid .51,.44 (media) · Career .555,.47 (media) · ShowMaker .125,.555 · Bin + Siwoo .41,.30 (encimados bajo el rótulo, media). Viper y Smash: bajo el HUD.
- **t=65 (16:15, tras el DOUBLE KILL; cámara quieta):** Xun + Knight .25,.64 (anillo común) · Viper .54,.66 (centro del anillo; la Cassiopeia no tiene pies) · Smash .75,.41. ShowMaker: en el borde izquierdo, bajo el HUD (barra en .03,.72).
- **t=69 (16:19, persecución):** Xun .51,.33 · ShowMaker .505,.65 · Viper .905,.25 (media).
- **t=71,2 (16:21):** Xun .415,.42 · ShowMaker .485,.70. Viper: fuera de los pies (barra en .77,.24).
- **Ruta Xun → ShowMaker (toma 40,6 → 71,4, la cámara se mueve: compensar):** Xun [(65, .25,.64), (69, .51,.33), (71.2, .415,.42)] · ShowMaker [(69, .505,.65), (71.2, .485,.70)].

## ⚠ Sin verificar / cuidado
- **«4 asesinatos de Xun»: NO.** En el feed la línea de 16:14 repite la de 16:13 (mismo marcador 5-4): es la misma muerte de Lucid. En el HUD BLG pasa de 4 a 7: **3 asesinatos de Xun** en la pelea (Lucid, Career, ShowMaker).
- La muerte de ShowMaker no sale en vivo ni en la repetición: el instante (≈16:27) es el del rótulo «killing spree» al volver la cámara y el marcador 7-4 de 16:28.
- Quién está «SUPPRESSED» en 16:07: la barra es de un DK de nivel 11 sin nombre legible; Lucid lo dice la narración. Que Ambessa lo suprime se deduce del «UNSTOPPABLE» de Bin, no lo dice nadie.
- Lo de Viper alejando a Smash es de la narración (sobre la repetición), no medido.
- «BLG ya no suelta la serie (3-0)»: dato del encargo, no comprobado en este tramo.
