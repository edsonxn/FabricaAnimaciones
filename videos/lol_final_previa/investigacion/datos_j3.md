# J3 (3D) — Semifinal Gen.G vs IG, partida 3 — Ruler: 4 asesinatos seguidos y Barón (investigado el 10-nov-2026)
Worlds 2026, semifinal, sáb 7-nov. **IG azul, Gen.G rojo.** gameId 115660540726095130 (`feed_130.txt`). VOD es-MX **WB7BeT33aWA**
(«IG vs GEN | WORLDS 2026 | DÍA 17 | FASE KNOCKOUT | JUEGO 3», 2 953 s). Subtítulos: `investigacion/subs/WB7BeT33aWA.es.vtt`
(los automáticos escriben Kiin = «King», Gen.G = «Jeygi/Jiejie», Barón = «varón»). Pistas del minimapa: `investigacion/pistas_j3.json`.

## Reloj (MEDIDO en cuadros) — en la voz SIEMPRE el HUD
| | Valor | Cuadros de control |
|---|---|---|
| **K (VOD = HUD + K)** | **507,8** (±0,3; sin pausas en toda la partida) | VOD 700 = 03:12 · 2300 = 29:52 · 2450 = 32:22 · 2900 = 39:52 · 2908 = 40:00 · 2912,6 = 40:04 |
| **K_fuente (HUD = t + K_fuente)** | **1760,3** (±0,3) | t 10,4 = 29:30 · t 11,8 = 29:32 · t 100,8 = 31:01 · t 101,8 = 31:02 |
| feed − HUD | **+4** | Meiko 30:22 ↔ 30:26 · JiaQi 30:27 ↔ 30:31 · Wei 30:35 ↔ 30:39 · TheShy 31:08 ↔ 31:12 |
- `medios/_fuente/j3.mp4`: 150 s, 1080p30 con audio, VOD ≈ 2268,1 → 2418 (HUD 29:20 → 31:50). ⚠ `cortar.py` falló dos veces con
  **403 Forbidden** en la URL directa (itag 399); el tramo se bajó con `yt-dlp --download-sections "*2268-2420"` del MISMO VOD es-MX
  y se recodificó igual que `cortar.py` (libx264 crf 18, 30 fps, AAC 192k). Por eso K_fuente no es redondo: medido, no supuesto.
- **Nexo final:** último HUD 40:04 en VOD 2912,6 (rótulo «GEN Ruler has slain IG Rookie!»); en VOD 2912,8 la realización corta a
  Ruler celebrando → nexo ≈ **40:05 (VOD ≈ 2913)**; feed 40:08.
- **Barón de Gen.G: HUD 31:11 (VOD ≈ 2379; t = 110,7)**, rótulo «Red team has slain Baron Nashor!». ⚠ NO es el minuto 33 del
  borrador: el feed solo muestrea en muertes (bar 0-1 aparece en su línea de 33:28). Lo dice también la narración (VOD 2383).

## Marcador (leído en el cuadro)
| HUD | Asesinatos IG-GEN | Oro IG / GEN | Torres IG-GEN | Dragones IG-GEN | Nota |
|---|---|---|---|---|---|
| 29:19 (t 0) | 13-6 | 53,9K / 51,0K (**IG +2,9K**) | 4-1 | 3-1 | «Dragon has spawned!» |
| 30:17 | 13-6 | 55,2K / 52,3K (IG +2,9K) | 4-1 | 3-1 | IG pegando al dragón de montaña (1 813) |
| 30:22 | 13-7 | 55,3K / 52,7K (IG +2,8K → +2,5K) | 4-1 | **3-2** | dragón robado + cae Meiko |
| 30:35 | 13-9 | 55,4K / 54,7K (IG +0,7K) | 4-1 | 3-2 | triple |
| 30:44 | 13-9 | 55,5K / 55,1K (IG +0,4K) | 4-1 | 3-2 | |
| 30:50 | 13-9 | 55,7K / 55,6K (sin insignia: empate) | **4-2** | 3-2 | «Blue turret destroyed!» |
| 31:09 | **13-10** | 56,0K / 56,6K (**GEN +0,6K**) | 4-2 | 3-2 | cae TheShy |
| 31:13 | 13-10 | 56,1K / 57,5K (**GEN +1,4K**) | 4-2 | 3-2 | BARON POWERPLAY +850 G (2:57) |
- La narración (VOD 2386-2388): Gen.G «empieza por primera vez en esta partida a ponerse arriba en oro». La narración (VOD 2417-2420):
  el dragón robado «era el alma, si es que lo sacaba Invictus» (IG tenía 3).

## Picks y K/D/A (feed; K/D/A leído en la tabla del HUD a las 30:45)
| Pos. | IG (azul) | GEN (rojo) |
|---|---|---|
| Top | TheShy **Gnar** 2/2/5 | Kiin **Camille** 2/3/2 |
| Jungla | Wei **Naafiri** 1/1/10 | Canyon **Wukong** 1/1/5 |
| Mid | Rookie **Locke** 9/1/3 | Chovy **Taliyah** 2/3/7 |
| ADC | JiaQi **Ezreal** 4/2/5 | Ruler **Yunara** **4**/2/5 |
| Sup. | Meiko **Alistar** 0/3/8 | Duro **Nautilus** 0/4/6 |

## Cortes de cámara y repeticiones (diferencia de cuadros + hojas)
- Salto de cámara del observador en t = 23,8 (HUD 29:43). Picture-in-picture de jugadores TAPANDO EL MINIMAPA: t 75-79 (30:35-30:39) y
  t 89-91 (30:49-30:51) (la vista principal sigue en vivo). Transición a **repetición** en t 136,3-137,7; de t 137,7 a 150 es repetición.
- **Tomas sin corte: 0 → 23,8 · 23,8 → 136,3** (en vivo) · 137,7 → 150 = repetición (no vale como acción en vivo).

## Paso a paso (t en j3.mp4; HUD medido en el mismo cuadro)
| t | HUD | Qué se ve |
|---|---|---|
| 0 | 29:19 | «Dragon has spawned!». IG 13-6 y +2,9K |
| 45 | 30:05 | Río central: Ruler, Duro y Canyon arriba a la izquierda; Meiko a la derecha; JiaQi abajo. Narración (VOD 2306-2312): Meiko «utiliza su voluntad inquebrantable», «entraba Canyon… salía con el señuelo» |
| 49 | 30:09 | Un campeón nivel 16 «CHANNELING» junto a una torre (narración VOD 2316-2321: no logran interrumpir la vuelta a base del top de Gen.G = Kiin) |
| 53 | 30:13 | Gen.G (Chovy, Ruler, Duro, Canyon) arriba; IG en el río: TheShy (Gnar grande, rosa), Meiko, JiaQi. Kiin: icono en la base de Gen.G |
| 56 | 30:16 | IG pega al dragón de montaña: 2 223 de vida; JiaQi y Wei en el foso |
| 57 | 30:17 | Dragón 1 813. Duro y Ruler bajan por arriba; muro blanco de piedra a la izquierda (como la definitiva de Taliyah). Kiin: icono con anillo brillante junto a su torre interior (≈ .86,.21) |
| 58 | **30:18** | **«Red team has stolen the Mountain Drake!»**: Canyon sobre el foso (CLONE + AIRBORNE junto a él) |
| 60 | 30:20 | Meiko «AIRBORNE» en el foso; Duro (Nautilus) encima; JiaQi y Wei debajo |
| 62 | **30:22** | **«GEN Ruler has slain IG Meiko!»** (13-7). Rótulo del dragón «5% Armor and Magic Resistance» |
| 63 | 30:23 | **IG partido en dos:** a la izquierda Rookie y TheShy con **Kiin** encima (Kiin ya está ahí: del icono en su torre a esta posición en 6 s = teletransporte; la narración, VOD 2340-2342: «Lo que hizo King fue legendario, aparecía…»); a la derecha Wei y JiaQi contra Chovy, Ruler, Duro y Canyon |
| 66 | 30:26 | JiaQi (vida casi vacía, efecto rosa encima) bajo Ruler, Duro y Chovy; Wei a su izquierda |
| 67 | **30:27** | **«DOUBLE KILL!»**: cae JiaQi (13-8, IG +1,8K) |
| 69 | 30:29 | Wei entra por la izquierda; TheShy y Rookie llegan tarde por abajo a la izquierda; Canyon «AIRBORNE» arriba a la derecha |
| 72 | 30:32 | Wei pegado a Kiin a la izquierda; Ruler/Duro/Chovy arriba; TheShy y Rookie abajo |
| 74 | 30:34 | Wei «STUNNED» junto a Kiin |
| 75 | **30:35** | **«TRIPLE KILL!»**: cae Wei (13-9, IG +0,7K); 30:37 rótulo «SHUT DOWN!» (la recompensa de Wei). Minimapa tapado 30:35-30:39 |
| 80 | 30:40 | Ruler, Chovy y Kiin se van arriba a la izquierda; Duro al centro; Rookie solo abajo |
| 85 | 30:45 | Tabla del HUD: Ruler 4/2/5. Chovy, Ruler y Kiin juntos hacia el Barón; Rookie a la derecha |
| 90 | **30:50** | «Blue turret destroyed!» (torres 4-2) |
| 92 | 30:52 | Canyon, Kiin, Ruler y Chovy en el foso del Barón; Rookie lejos, abajo a la derecha |
| 94 | 30:54 | Barra del Barón: 17 705 (30:56: 14 513; 31:00: 10 431; 31:02: 7 195; 31:03: 6 389; 31:06: 4 590) |
| 105 | 31:05 | TheShy «AIRBORNE» entre Kiin y Duro, dentro del foso; Rookie abajo; Barón ~4,6K |
| 108 | **31:08** | **«GEN Ruler is on a rampage!»**: cae TheShy (13-10, GEN +0,6K a las 31:09); Barón 3 089 |
| 111 | **31:11** | **«Red team has slain Baron Nashor!»**; 31:13 «BARON POWERPLAY» +850 G, GEN +1,4K |
| 113-136 | 31:13-31:36 | Gen.G sale del foso; Kiin a la línea de arriba; a las 31:21 IG solo tiene en el mapa a Rookie, Meiko (reapareció ~30:59) y JiaQi saliendo de base |

## Narración (subtítulos automáticos, segundo de VOD; ±2 s)
- VOD 2278-2290: «Rookie lo sabe perfectamente… necesita él matar a Ruler, aunque se tenga que sacrificar… si logra matar a Ruler… va a ganar la team fight Invictus Gaming».
- VOD 2323-2328: «se viene la pelea en el dragón… se lo termina robando, se lo roba Canyon».
- VOD 2330-2339: «acaba de caer Meiko, que quedó en una posición comprometida… ¿dónde está el resto de Invictus? Tenía que estar ahí peleando en el dragón».
- VOD 2340-2346: «Lo que hizo King [Kiin] fue legendario, aparecía y [sonaba/zoneaba] a dos de tal manera que no lo dejó jugar… triple asesinato para Ruler».
- VOD 2358-2367: Ruler «tiene 4K de oro de ventaja»… «van directamente por el Barón y quedan… dos jugadores vivos de Invictus».
- VOD 2377-2388: «se debió haber coordinado un poquito mejor con TheShy porque ni siquiera funcionó realmente el engage… Se termina quedando con Barón Gen.G y empieza por primera vez en esta partida a ponerse arriba en oro».

## Por qué gana Gen.G la pelea (solo lo visto y lo narrado)
IG pelea un dragón que le daba el alma y no llega junto: en el foso solo están Meiko, JiaQi y Wei. Canyon se lo roba (30:18) y Meiko,
que había entrado adelantado, cae primero (30:22). Mientras, Kiin aparece a la izquierda sobre Rookie y TheShy (del icono en su torre a
esa posición en 6 s) y los entretiene: IG queda partido en dos y Ruler limpia el lado del dragón, JiaQi a las 30:27 y Wei, que entra
solo, a las 30:35. Con tres de IG muertos, Gen.G va directo al Barón (30:52-31:11); TheShy entra solo al foso (31:05) y es el cuarto de
Ruler (31:08). De +2,9K para IG a +1,4K para Gen.G en 55 segundos.

## ⚠ Sin verificar / cuidado
- **TP de Kiin:** deducido (icono con anillo brillante junto a su torre a las 30:17 y en la pelea a las 30:23; nadie dice «teleport»; la narración dice «aparecía»). En la voz: «aparece por la espalda», no «teletransporte» a secas.
- El campeón «CHANNELING» de las 30:09 no se identificó en cuadro (la narración dice que es el top de Gen.G volviendo a base).
- El muro blanco de las 30:17-30:20 es compatible con la definitiva de Taliyah, pero nadie la nombra en este tramo.
- La torre caída a las 30:50 no se localizó en el minimapa. No decir cuál.
- «Soñaba» en los subtítulos es error del reconocimiento automático: no citar esa palabra.
- Pistas: precisión ~±0,04 (no ±0,03): la cámara de la vista principal se llevó al rectángulo del minimapa; ver `_meta` del JSON.
