# G3 (Doran temprano + remontada de T1) y G2 (jugada de Faker) — datos verificados (investigado el 17-nov-2026)
Fuentes: feed oficial (`feed_124.txt`, `feed_123.txt`), subtítulos automáticos es (`subs/Tq2FdhgReuI.es.vtt`, `subs/r9-avVeme5o.es.vtt`; escriben Oner = «Honer», Peyz = «P/Pace», Knight = «Night», Xun = «Shun», Bin = «Vin», T1 = «Tiwan»), cuadros 1080p de las fuentes cortadas.
**En la voz SIEMPRE el reloj del HUD** (el feed va ≈ +5 s).

---------------------------------------------------------------------------------------------------
# A) PARTIDA 3 — gameId 115660540726095124 — **BLG azul, T1 rojo**
BLG: Bin Gnar · Xun Pantheon · Knight Taliyah · Viper Ezreal · ON Nami — T1: Doran Ambessa · Oner Jarvan IV · Faker Ahri · Peyz Sivir · Keria Karma.

## Reloj (MEDIDO en cuadros)
| VOD es-MX | VOD = HUD + | Control |
|---|---|---|
| Tq2FdhgReuI | **451** (vale también al principio: sin pausas antes del min 3) | VOD 666 = **03:35** con el rótulo «BLG Xun has slain T1 Doran!» en pantalla; los tres K_fuente de abajo salen exactos con 451 |

## Fuentes cortadas (`medios/_fuente/`)
| Archivo | VOD | Dur. | **K_fuente** (HUD = t + K) | Cuadros de control | Qué cubre |
|---|---|---|---|---|---|
| `g3_j1.mp4` | 631 → 676 | 45 s | **180** | t=0 → 03:00 · t=16 → 03:16 · t=35 → 03:35 | 1.ª muerte de Doran (Xun + Bin, arriba) |
| `g3_j2.mp4` | 1028 → 1073 | 45 s | **577** | t=0 → 09:37 · t=20 → 09:57 · t=31 → 10:08 | 2.ª muerte de Doran (buceo de Bin, Viper y Xun bajo su torre) |
| `g3_j3.mp4` | 1771 → 1816 | 45 s | **1320** | t=0 → 22:00 · t=10 → 22:10 · t=30 → 22:30 | dragón robado por Oner y la pelea de la remontada (7-4 → 8-8) |
Ninguna tiene cortes de realización hasta t≈43 de `g3_j3` (ahí empieza la REPETICIÓN, rótulo «REPLAY»: no vale como en vivo).

## A1. Doran cae a las 03:35 (`g3_j1.mp4`, HUD = t + 180)
**Marcador:** 03:00 = asesinatos 1-1, oro BLG 5,9K / T1 5,9K · 03:30 = 1-1, T1 +0,4K (6,4K / 6,8K) · **03:36 = 2-1, BLG +0,1K (7,0K / 6,9K)**.
Fila Bin-Doran en el marcador: 03:00 Bin 19 de súbditos / Doran 17, Doran nivel 4 contra nivel 3 de Bin · 03:38 Doran 0/1/0 muerto (10 s para revivir), Bin 0/0/1, diferencia 170 a favor de Bin.

| t | HUD | Qué se ve |
|---|---|---|
| 0-16 | 03:00-03:16 | La cámara va del carril central (Faker) al de abajo; Doran en el carril superior |
| 22 | 03:22 | Carril superior: Doran solo frente a Bin y sus súbditos; un BLG de nivel 4 canaliza en el río superior (rótulo «CHANNELING») |
| 26 | 03:26 | Sigue la canalización en el río (rayo de luz vertical); Doran en el carril, Bin a la izquierda |
| 29 | 03:29 | **Xun sale del río** hacia Doran; Bin por el carril: 2 contra 1 |
| 30 | 03:30 | **Doran «STUNNED»** con Xun encima y Bin al lado (la W de Pantheon aturde; el rótulo no dice qué habilidad) |
| 31-34 | 03:31-03:34 | Doran retrocede hacia su torre con poca vida; Xun lo persigue, Bin detrás |
| 35 | **03:35** | **«BLG Xun has slain T1 Doran!»** (+300 oro) al pie de la torre exterior superior de T1 (se ve su base en el borde de arriba; minimapa: esquina superior izquierda, lado de T1) |
**Quién participa:** Xun (asesinato) y Bin (asistencia, 0/0/1). Nadie de T1 llega.

**Narración (VOD; subtítulos ±2 s):**
- VOD 660-672: «…mi amigo Doran, ay amigo Doran. Destello inmediato, lo van a atrapar. Está bajo la torre. Se lleva el asesinato. La línea que tenían que ganar, ahora la tienen en su contra los jugadores de T1».
- VOD 674-684: «Sí, muchísimos problemas en el carril superior… a Doran otra vez le van a empezar a hacer casita. Ya lo sabe Doran, es parte del trabajo».
- VOD 684-692: «Pero Bin puede salirse de control».

## A2. Doran cae a las 10:08 (`g3_j2.mp4`, HUD = t + 577)
**Marcador:** 09:37 = 2-1, BLG +0,5K (16,5K / 16,0K) · 09:57 = 2-1, BLG +0,4K · **10:08 = 3-1, BLG +0,8K (17,7K / 16,9K)** · 10:18 = 3-1, 18,0K / 17,1K.
Fila Bin-Doran: **09:37 Bin 93 súbditos, 0/0/1, nivel 9 · Doran 72 súbditos, 0/1/0, nivel 8 · diferencia 845 a favor de Bin** · **10:17 Bin 102, 0/0/2 · Doran 75, 0/2/0 (muerto, 16 s) · diferencia 1,1K**. (Los −942 a los 10:00 son del archivo de estadísticas, no los vi en el HUD; el HUD da 845 a las 09:37 y 1,1K a las 10:17.)

| t | HUD | Qué se ve |
|---|---|---|
| 0-17 | 09:37-09:54 | Carril central: Faker, Oner y Keria frente a Knight y ON; **Xun sale del carril central hacia arriba** (09:54) |
| 19,5 | 09:56 | Carril superior, bajo la torre exterior superior de T1: **Bin (transformado en Mega Gnar) y Viper** encima de Doran; Doran «AIRBORNE» |
| 21 | 09:58 | **Doran «STUNNED»**; la torre le dispara a Bin (rayo rojo) |
| 23-24 | 10:00-10:01 | Cae la **definitiva de Xun** (la «gran descarga celestial» de Pantheon: círculo naranja a la derecha); Doran «UNSTOPPABLE» (usa su definitiva) |
| 25-28 | 10:02-10:05 | Xun entra por la derecha; Doran se lanza hacia él y vuelve hacia su torre con muy poca vida; Bin y Viper siguen ahí |
| 31 | **10:08** | **«BLG Viper has slain T1 Doran!»** junto a la torre de T1 (3-1) |
| 33-44 | 10:10-10:21 | Oner y Keria llegan tarde (10:15); BLG sigue golpeando la torre con súbditos (10:21). No muere nadie de BLG |
**Quién participa:** Viper (asesinato), Bin y Xun (asistencias; Bin 0/0/2, Xun 1/0/1 a las 10:17). Buceo de tres de BLG bajo la torre de T1.

**Narración:**
- VOD 1047-1060: «Uy, cuidado acá con Viper… Ay, ahora sí, gran descarga celestial. Se le tiran encima bajo la torre. Excelente reacción. Y Viper, último golpe. Y ahí está, logra llevarse uno más».
- VOD 1063-1076: «Qué error por parte de Doran, porque ni cerca estuvo de poder atrapar a Xun… lo intenta atrapar… pero no posiciona bien esa definitiva y eso le cuesta la vida otra vez a Doran, que está 0-2 ya en estos momentos».
- VOD 1076-1087: «…de ventaja para Bin, que obviamente se está haciendo la Black Cleaver como su primer objeto… está haciendo pedazos».

## A3. La remontada de T1, 22:00-22:31 (`g3_j3.mp4`, HUD = t + 1320)
Lugar: el foso del dragón (río inferior) y la jungla de T1 al este de él.
**Marcador:** **22:00 = 7-4, BLG +1,0K (40,1K / 39,1K), dragones 2-1** · 22:04 = 7-5, BLG +0,5K · 22:10 = 7-6 · 22:12 = 7-7, T1 +0,7K · 22:16 = 8-7, 40,8K / 40,9K (igualados) · **22:33 = 8-8, T1 +1,0K (41,0K / 42,0K)**.
K/D/A a las 22:38 (HUD): Doran 0/4/3 · Oner 2/1/6 · Faker 3/1/1 · Peyz 2/1/6 · Keria 1/1/6 — Bin 1/1/4 · Xun 2/2/3 · Knight 2/1/3 · Viper 2/1/2 · ON 1/3/2.

| t | HUD | Qué se ve |
|---|---|---|
| 0 | 22:00 | BLG en el dragón infernal; **el muro de Taliyah (definitiva de Knight) cruza el río** junto al foso; T1 al otro lado (Oner, Doran, Keria, Faker) |
| 1-3 | **22:01-22:03** | **«Red team has slain the Infernal Drake!»**: T1 se queda el dragón (lo roba Oner, según la narración). Doran «UNSTOPPABLE» entrando |
| 3-4 | 22:03-22:04 | Marcador 7-4 → **7-5: cae ON** (asesino según el feed: Oner; su rótulo no se ve, lo tapa el del dragón) |
| 7 | 22:07 | **Bin «CHARMED»** (el hechizo de Ahri) junto a Faker, Peyz y Keria |
| 9 | **22:09** | **«T1 Faker has slain BLG Bin!»** (7-6) |
| 10-12 | 22:10-22:12 | **«T1 Peyz has slain BLG Xun!»** (7-7, T1 +0,7K) |
| 16 | **22:16** | **«BLG Viper has slain T1 Keria!»** (8-7) |
| 19-27 | 22:19-22:27 | Viper y Knight se retiran por el foso; Faker, Oner y Peyz los siguen por el río |
| 28-29 | 22:28-22:29 | **Knight «CHARMED»** por Faker en la jungla de T1, al este del foso del dragón |
| 30 | **22:30** | **«T1 Faker has slain BLG Knight!»** (+380) → 8-8 a las 22:33, T1 +1,0K |
| ≈43 | — | Empieza la REPETICIÓN (no vale como en vivo) |
**Quién inicia:** BLG estaba haciendo el dragón con el muro de Knight puesto; **Oner entra y lo roba**, y con eso empieza la pelea (narración, ver abajo). Muertes: ON (Oner, feed), Bin (Faker), Xun (Peyz), Keria (Viper), Knight (Faker). **Faker hace 2 de las 5 muertes.**

**Narración:**
- VOD 1758-1773: «Xun luego se mete un poco extraño, sin mucha razón aparente, pero esta es la pelea que les puede dar la partida a cualquiera de los dos equipos. Aquí está llegando muro de la tejedora. Xun recibe mucho castigo, quieren llevarse el dragón, pero llega y se lo roba Oner».
- VOD 1776-1793: «Se van a llevar la vida de la Nami… Doran intenta escapar. Utiliza bien el destello. Viper se lleva a Keria… se llevan el dragón y la diferencia de oro es nula».
- VOD 1800-1810 (≈22:29-22:39, la muerte de Knight): «¿Por qué? … Todo por un centinela. Todo por un centinela».
- Repetición, VOD 1813-1832: «Otra vez un buen muro de la tejedora para separar a T1. Entra con todo, lo termina robando… entra junto con Doran atrás, Bin intentándose hacer el tiempo. Es un 3 contra 2 porque están divididos los chicos de T1, pero se cierran bastante bien. No puede Bin aguantar… T1 perfectamente los empuja hacia atrás».

---------------------------------------------------------------------------------------------------
# B) PARTIDA 2 — gameId 115660540726095123 — **T1 azul, BLG rojo**: la E de Faker (Syndra)
T1: Doran Olaf · Oner Lee Sin · Faker Syndra · Peyz Jhin · Keria Poppy — BLG: Bin Camille · Xun Qiyana · Knight LeBlanc · Viper Kai'Sa · ON Alistar.

## Reloj y fuente
| Archivo | VOD | Dur. | **K_fuente** (HUD = t + K) | Cuadros de control |
|---|---|---|---|---|
| `g2_faker.mp4` | 1505 → 1555 | 50 s | **1057** (VOD = HUD + 448 confirmado: VOD 1471 = 17:03, 1505 = 17:37, 1519 = 17:51) | t=0 → 17:37 · t=13 → 17:50 · t=20 → 17:57 |
Tramos: **en vivo t=0 → ≈36** · cortinilla t≈36 · **REPETICIÓN t≈37,5 → 50** (repite la muerte de Knight de las 17:03-17:08 y luego la de Bin).

## Marcador
| HUD | Asesinatos T1-BLG | Oro T1 / BLG | Nota |
|---|---|---|---|
| 17:37 | 2-4 | 30,7K / 33,1K (BLG +2,4K) | «Blue team has slain the Ocean Drake!»: T1 se lleva el 3.er dragón |
| 17:50 | 3-4 | 31,0K / 33,5K (BLG +2,5K) | cae Bin |
| 17:57 | 3-4 | 31,8K / 33,7K (BLG +1,9K) | «Red turret destroyed!»: T1 tira la torre de BLG de esa zona |
| 18:05 | 3-4 | 32,2K / 33,8K (BLG +1,6K) | |
K/D/A: 17:37 Doran 1/3/0 · Oner 1/1/1 · **Faker 0/0/1** · Peyz 0/0/0 · Keria 0/0/0 — Bin 2/1/0 · Xun 1/0/3 · Knight 1/1/0 (muerto) · Viper 0/0/0 · ON 0/0/0.
17:56 Doran 1/3/1 · Oner 2/1/1 · **Faker 0/0/2** · Peyz 0/0/0 · Keria 0/0/1 — Bin 2/2/0 (muerto, 36 s).
→ En la muerte de Bin participan **Oner (asesinato), Faker, Doran y Keria (asistencias)**. Faker no tiene ningún asesinato todavía: sus dos jugadas son aturdimientos que rematan otros.

## Paso a paso (t en `g2_faker.mp4`; HUD = t + 1057)
| t | HUD | Qué se ve |
|---|---|---|
| 0 | 17:37 | T1 termina el dragón oceánico (3-0 en dragones); Bin ya había tirado la teleportación hacia abajo (narración, VOD 1502-1504) |
| 8,3 | 17:45 | **Bin (Camille, nivel 13)** solo y adelantado en el carril inferior, lado de BLG (minimapa); Faker todavía no sale en cuadro |
| 8,8 | **17:46** | Faker aparece por la izquierda y lanza **la E de Syndra (Dispersar a los Débiles)**: la onda morada empuja la esfera contra Bin → **Bin «STUNNED»** (único campeón de BLG en la zona, nivel 13) |
| 9,3 | 17:46 | Entra Doran (Olaf) por la izquierda, con Faker al lado |
| 9,7-10,8 | 17:47-17:48 | Keria (Poppy) entra con su definitiva (arco dorado); Doran «CC IMMUNE» (definitiva de Olaf); Oner encima de Bin |
| 11,3-12,3 | 17:48-17:49 | Bin usa su definitiva (hexágono amarillo de Camille); Keria queda «STUNNED» dentro, pero Bin está rodeado |
| 12,8-13 | **17:50** | **«T1 Oner has slain BLG Bin!»** (+370) → 3-4 |
| 20 | 17:57 | **«Red turret destroyed!»** |
| 37,5-42 | repetición | La E de Faker sobre **Knight** (LeBlanc): «AIRBORNE» → «STUNNED», luego la patada de Lee Sin; «Dragon has spawned!» (fue a las 17:03-17:05) |
| 47,8-48,4 | repetición | La misma E sobre Bin: «AIRBORNE» → «STUNNED» |
**La jugada anterior (fuera de la fuente, cuadros del VOD):** 17:03 un BLG «AIRBORNE» junto a Faker; 17:07 Oner +350 → Knight cae (feed 17:13 = HUD ≈17:08), con asistencia de Faker (0/0/1 a las 17:37). La repetición confirma que es la E de Syndra sobre Knight. Por eso la narración dice «la hace de nuevo».

**Narración:**
- VOD 1504-1516: «…está tirando la teleportación Bin ahí abajo… simplemente para defender, no dejar caer esta torreta exterior, pero hay cuatro jugadores de T1 en esa zona. Cuatro. Ay, otra vez Bin en problemas».
- VOD 1516-1523: «…tiene que tener definitiva, pero no lo vio llegar, no hay visión, no hay nada. **Dispersar a los Débiles y Faker la hace de nuevo**».
- VOD 1535-1541: «Se adelantó un poquitito… Dispersar a los Débiles por parte de Faker y lo atrapan absolutamente todos».
- VOD 1542-1547 (repetición): «Esto primero lo de Knight que está sobreextendido… **Faker espectacular, por cierto, Faker**».
- VOD 1565-1570: «…y el que no está para nada dormido es Faker… todavía con muy buenas mecánicas».

---------------------------------------------------------------------------------------------------
## ⚠ Sin verificar / cuidado
1. **A1:** el destello de Doran lo dice la narración («destello inmediato»); no lo aislé en cuadro. Qué habilidad aturde a Doran a las 03:30 no sale en pantalla (solo «STUNNED» con Xun encima). Quién canaliza en el río (03:22-03:28) se deduce: de ahí sale Xun a las 03:29.
2. **A2:** que la definitiva de Doran fallara sobre Xun es de la narración; en cuadro solo se ve «UNSTOPPABLE» y el salto hacia Xun. Los −942 de oro a los 10:00 no salen en el HUD (845 a las 09:37, 1,1K a las 10:17).
3. **A3:** el rótulo de la muerte de ON (22:03-22:04) no se ve (lo tapa el del dragón); el asesino (Oner) es del feed. Que Oner robe el dragón es de la narración (en cuadro: «Red team has slain the Infernal Drake!» a las 22:01). «Todo por un centinela»: no comprobé qué centinela fue a buscar Knight.
4. **A3, oro:** el feed da −151 a la hora del 8-8 (feed 22:36); el HUD a las 22:33 da T1 +1,0K. En la voz, usar el HUD.
5. **B:** la torre que cae a las 17:57 está en la zona de la pelea (minimapa: carril inferior, lado de BLG); que sea exactamente la que Bin bajó a defender se deduce de la narración y el minimapa, no de un rótulo con nombre.
