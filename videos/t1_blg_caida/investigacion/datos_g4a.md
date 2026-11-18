# G4 (A) — Semifinal BLG vs T1, partida 4: el draft de la Vayne y las tres peleas de 08:25, 10:50 y 17:30 — datos verificados (investigado el 17-nov-2026)
Partida: gameId 115660540726095125 (`feed_125.txt`, `stats_g4.json`). **T1 azul, BLG rojo.** BLG gana 21-9 y la serie 3-1.
Fuentes: cuadros 1080p del VOD es-MX **n616F3asGf0** (VOD = HUD + 481, comprobado otra vez: VOD 1556 = 17:55), subtítulos automáticos (`subs/n616F3asGf0.es.vtt`) y **Whisper medium** (GPU, solo en los tramos citados; large-v3 no cargó por falta de RAM: `mkl_malloc`). Las citas llevan el segundo del VOD de Whisper (±1 s).
Feed − HUD = **+5** también aquí: Viper→Oner feed 08:31 = rótulo FIRST BLOOD a las 08:26 del HUD; Bin→Keria 08:53 = 08:48; Viper→Peyz 09:01 = 08:56; Bin→Doran 10:57 = 10:52; Keria→ON 11:24 = 11:19; ON→Peyz 17:38 = 17:33; Xun→Oner 17:46 = 17:41. Los eventos de `stats_g4.json` también van en reloj del feed (Barón azul 1765 s = 29:25 feed = 29:20 HUD, igual que en `datos_j6.md`).

## Fuentes cortadas (`medios/_fuente/`)
| Archivo | VOD | Duración | **K_fuente** (HUD = t + K) | Qué cubre |
|---|---|---|---|---|
| `g4_draft.mp4` | 405 → 427 | 22 s | — (fase de selección) | t≈8 (VOD 413): la **Vayne entra como última selección de T1** en la 5.ª casilla; t≈9-12 «¡Ay, no puede ser, JJ!»; t≈17-22: las selecciones se reacomodan por rol y la Vayne queda en la casilla de Doran |
| `g4_j1.mp4` | 966 → 1026 | 60 s | **485** (t=0 → 08:05; t=21 → 08:26; t=57 → 09:02) | pelea por las larvas del vacío (08:15-08:31) y persecución hasta la torre exterior superior de T1 (08:48, 08:56) |
| `g4_j2.mp4` | 1118 → 1173 | 55 s | **637** (t=0 → 10:37; t=15 → 10:52; t=54 → 11:31) | Doran cae en su carril (10:52) y la pelea del carril inferior (11:05-11:19) |
| `g4_j3.mp4` | 1506 → 1550 | 44 s | **1025** (t=0 → 17:05; t=42,5 → 17:47) | pelea del foso del dragón: Oner mata a Knight (17:16) y BLG mata a 4 (17:33-17:41); BLG empieza el dragón |

K medido leyendo el reloj del HUD en cuadros (cada 2,5-3 s en toda la fuente; error ±1 s por el redondeo del reloj). **Las tres fuentes de juego son en vivo y sin pausas ni repeticiones**: el reloj corre seguido. En `g4_j3.mp4` aparece un recuadro con el público/banquillo de BLG abajo a la derecha (t≈34-37).

## 1. El draft: la Vayne de Doran (VOD 340-540)
**Rótulos del draft:** «BLUE SIDE» bajo T1 y «1ST PICK» bajo BLG (T1 elige lado, BLG la primera selección). Parche 26.20.
Orden en que se llenan las casillas (cuadros 1080p):
| VOD | T1 | BLG |
|---|---|---|
| ≤ 200 | 1.ª Lucian, 2.ª Milio | 1.ª Viktor, 2.ª Ashe, 3.ª Seraphine |
| ≤ 300 | 3.ª Akali | — |
| ≈ 350 | 4.ª **Wukong** | — |
| ≈ 380 | — | 4.ª **Renekton** (ficha: 19,4 % FEARLESS PB · 4,3 % PICK · 1W-3L) |
| ≈ 390 | — | 5.ª **Skarner** (29,0 % · 8,6 % · 5W-3L) |
| **≈ 413** | 5.ª y **última del draft: Vayne** (ficha: **14,0 % FEARLESS PB · 1,1 % PICK · 0W-1L**) | — |
| 418-426 | se reacomodan: Doran **Vayne**, Oner Wukong, Faker Akali, Peyz Lucian, Keria Milio | Bin Renekton, Xun Skarner, Knight Viktor, Viper Ashe, ON Seraphine |
→ La Vayne se elige **con el Renekton de Bin ya a la vista** (contraselección del último turno).

Narración (Whisper, VOD):
- 356-361: «Por ahora, T1, la única opción de iniciación que tiene es el Wukong… y le vas a dar la responsabilidad de iniciar».
- 364-372: «Le estás dando la responsabilidad de iniciación aquí a Doran. Un Ornn, por favor. Un Ornn sería la mejor opción, creo yo». (Los dos narradores esperaban un Ornn).
- 389-399: «Y el Renekton, ojito con esto… El Renekton destroza completamente los tanques en el juego temprano, con la Black Cleaver».
- **414: «¡Ay, no puede ser, JJ!»** (justo al bloquearse la Vayne, VOD ≈413).
- 424-446: «En el juego temprano pueden ganar por mucho los chicos de T1… pero esta composición, frente a lo que está ofreciendo BLG, veo que tiene muchas falencias y no tiene formas de iniciar. Si ellos no tienen la ventaja total en esta partida, no hay forma en la que puedan salir bien librados».
- 446-449: «Estoy en shock». — «Yo también, realmente en shock».
- 473-476: «Esto es matar o morir, matar o morir».
- 501-503: «Hay una Vayne en las manos de Doran, que es lo que estamos enfocando».
- Más tarde (VOD 1216-1226, vtt): Doran «está muy atrás… va a tener la activación muy lejos de su quest» (la misión del carril superior).

## 2. La pelea de las larvas del vacío (HUD 08:05-09:05, `g4_j1.mp4`, K = 485)
Lugar: **foso del río superior** (larvas del vacío, el foso del Barón) y la huida de T1 hacia **su torre exterior del carril superior** (minimapa).
| t | HUD | Qué se ve |
|---|---|---|
| 0-10 | 08:05-08:15 | Los dos equipos alrededor del foso. Tabla del HUD a las 08:15: Doran (niv. 7, 53 CS) **−265 de oro** contra Bin (niv. 8, 65 CS); Faker −160 contra Knight; Oner +51, Peyz +148; Keria −118 |
| 14 | 08:19 | Oner (Wukong) dentro del foso entre ON, Bin y Xun, **AIRBORNE** |
| 20 | 08:25 | Oner AIRBORNE entre Viper y ON; Keria **CHARMED** (definitiva de Seraphine) abajo |
| 21-22 | 08:26-08:27 | **«FIRST BLOOD!» — Viper mata a Oner** (0-1, BLG +1,0K) |
| 26-27 | 08:31 | Contador de larvas de BLG: 0 → **2** |
| 33-37 | 08:37-08:42 | Rótulo **«Red team has slain the Voidgrubs!»**; contador de T1: 0 → **1** (08:41) |
| 41 | 08:46 | Keria **STUNNED** entre Bin, Xun, Knight y Viper, ya hacia el carril superior de T1 |
| 44 | 08:48-08:49 | **«BLG Bin has slain T1 Keria!»** junto a la torre exterior superior de T1 (0-2) |
| 50 | 08:55 | Peyz huye bajo esa torre; Viper y Knight lo persiguen |
| 52 | 08:56-08:57 | **«BLG Viper has slain T1 Peyz!»** (0-3, BLG +1,8K) |
| 59 | 09:04 | Oner reaparece y vuelve al río; Doran −742 contra Bin en la tabla |
Quién inicia: en cuadro, Oner es el primero que queda dentro del foso rodeado (AIRBORNE a las 08:19 y 08:25); la narración lo confirma (abajo).

**Marcador del HUD**
| HUD | Asesinatos T1-BLG | Oro T1 / BLG | Torres | Dragones | Larvas |
|---|---|---|---|---|---|
| 08:05 | 0-0 | 13,0K / 13,1K (BLG +0,1K) | 0-0 | 1-0 (hextech, 06:31) | 0-0 |
| 09:02 | 0-3 | 13,9K / 15,8K (BLG **+1,9K**) | 0-0 | 1-0 | 1-2 |

Narración:
- 941-948: «Buena oleada que tiene también Doran, pero Bin le está ganando por 266 de oro» (≈07:43; en la tabla de las 08:15 se lee 265).
- 982-990 (≈08:21-08:29): «¿Qué pasó con Oner? Se metió solo contra el mundo. Lo van a derribar y responde excelentemente ON, utilizando bien su definitiva, mandándolos a todos a cantar».
- 1008-1025: «Uno más, dos para BLG… Y lo van a buscar a Peyz… pero no es suficiente contra el Viperino, la serpiente, la culebra campeona del mundo».
- Repetición, vtt 1064-1076: «Doran afuera, pues una Vayne no puede hacer nada… termina siendo Faker el que se lleva la vacu-larva y corren como puede todo T1. Es una catástrofe eso de juego temprano».
- vtt 1101-1108: «Ya se va a salir de control, sobre todo esta Ashe. 1 000 de oro en contra de un Lucian que necesitaba este juego temprano».

## 3. Doran cae y la pelea del carril inferior (HUD 10:37-11:32, `g4_j2.mp4`, K = 637)
| t | HUD | Qué se ve |
|---|---|---|
| 2 | 10:39 | Doran empujando en el carril superior; Xun (Skarner) sube por el río. Tabla: Doran 70 CS, Bin 81 CS, **−597 de oro** |
| 7 | 10:44 | Bin y Xun encima de Doran, que se refugia en su torre exterior superior |
| 11 | 10:48 | Bin con la definitiva encendida junto a la torre |
| 15 | 10:52 | **«BLG Bin has slain T1 Doran!»** bajo la torre exterior superior de T1 (0-4). Tabla: Doran 0/1/0, Bin 2/0/1, **−896** |
| 23 | 11:00 | Carril inferior: Viper y ON contra Peyz y Keria (Doran −1,2K en la tabla) |
| 28-33 | 11:05-11:10 | Llega Oner por la izquierda (su CLONE en pantalla); **Viper mata a Peyz** (0-5; el rótulo cae entre t=28 y t=33) |
| 36 | 11:13 | **«BLG ON has slain T1 Keria!»** (0-6, BLG +3,3K) |
| 37-41 | 11:14-11:18 | ON, con poca vida, se mete hasta la **torre exterior inferior de T1** |
| 41,5 | 11:19 | **«T1 Keria has slain BLG ON!»** bajo esa torre (1-6). Keria ya estaba muerta (11 s de reaparición en la tabla): asesinato póstumo; no se ve qué da el golpe final |

**Marcador del HUD**
| HUD | Asesinatos | Oro T1 / BLG | Torres | Dragones | Larvas |
|---|---|---|---|---|---|
| 10:37 | 0-3 | 16,5K / 18,6K (BLG +2,1K) | 0-0 | 1-0 | 1-2 |
| 11:31 | 1-6 | 18,0K / 21,3K (BLG **+3,3K**) | 0-0 | 1-0 | 1-2 |

Narración:
- 1114-1120: «La iniciación de Oner me dejó también con muchas dudas, porque es el único en el equipo que puede iniciar peleas».
- 1120-1136 (≈10:39-10:55): «Mira Xun, mira Xun. ¡Ay, Doran! No hay Flash, no hay Flash. Ay, mi Doran del alma… Le tiran una pedrada y se lo van a llevar. Secuestrado, muchacho. Lo intenta llevar Bin y le bajan la velocidad de movimiento, un asesinato más facilito para el señor Bin».
- 1148-1161: «Parecía que todo quedaba en las manos de T1, pero el Viper logra llevarlo y ON responde bien llevándose el segundo en el carril inferior… y se lo lleva Keria».
- 1167-1172: «El tema del Renekton se está saliendo de control, es fuerte, no hay quien lo va a poder controlar».
- vtt 1178-1193: «BLG está por encima simplemente por temas de composición… está sucediendo exactamente lo que BLG necesita para llevarse la partida».
- vtt 1250-1259: «Son 4 000 de oro… pero luce como que si BLG no se equivoca ya tiene el juego en sus manos».

## 4. La pelea del foso del dragón (HUD 17:05-17:49, `g4_j3.mp4`, K = 1025)
Lugar: **río inferior, en el foso del dragón** («Dragon has spawned!» a las 17:10). El primer choque (17:06-17:16) es un poco más al este, junto al carril inferior de BLG.
| t | HUD | Qué se ve |
|---|---|---|
| 1 | 17:06 | Faker contra Knight junto a una torre roja. Minimapa: un campeón de BLG arriba a la izquierda (carril superior) y el retrato de la Vayne junto a la base de T1 con un anillo verde (¿teletransporte? ver ⚠ 7) |
| 5 | 17:10 | **«Dragon has spawned!»**; Oner, Keria y Peyz encima de Knight |
| 8,5 | 17:13 | Varios AIRBORNE de los dos lados; T1 junta a 4 alrededor de Oner |
| 11,5 | 17:16 | **«T1 Oner has slain BLG Knight!»** (3-6, la ventaja baja a BLG +2,7K) |
| 15-19 | 17:20-17:24 | Ya en el río: Peyz ROOTED; Bin (la narración dice que llega con teletransporte), Viper, ON y Xun juntos; Doran llega por la izquierda |
| 26 | 17:31 | El dragón (7 873 de vida) en el foso; T1 (con el CLONE de Oner) se lanza sobre Bin, Xun y Viper |
| 28 | 17:33 | **«BLG ON has slain T1 Peyz!»** |
| 29,5 | 17:34 | Muere Keria (Bin; feed 17:39) → 3-8, BLG +3,6K |
| 32 | 17:37 | «BLG Bin is on a killing spree!» |
| 36 | 17:41 | **«BLG Xun has slain T1 Oner!»** y ON mata a Doran (feed 17:46) → **3-10** |
| 40 | 17:45 | Rótulo **«DOUBLE KILL!»** de ON (Seraphine); BLG empieza el dragón (5 251 de vida); en la franja, 4 retratos de T1 con temporizador: **solo Faker sigue vivo** |
| 43 | 17:48 | El dragón a 3 113; BLG lo toma ≈17:52 (`stats_g4.json`: dragón de montaña, feed 1077 s) |

**Marcador del HUD**
| HUD | Asesinatos | Oro T1 / BLG | Torres | Dragones | Larvas |
|---|---|---|---|---|---|
| 17:05 | 2-6 | 28,7K / 32,0K (BLG +3,3K) | 0-1 | 2-0 (hextech y océano) | 1-2 |
| 17:16 | 3-6 | 29,5K / 32,2K (BLG +2,7K) | 0-1 | 2-0 | 1-2 |
| 17:47 | 3-10 | 30,0K / 34,7K (BLG **+4,7K**) | 0-1 | 2-0 | 1-2 |
| 17:55 (VOD 1556) | 3-10 | 30,2K / 34,9K (BLG +4,7K) | 0-1 | **2-1** | 1-2 |
Tabla a las 17:06: Doran 0/1/0, 126 CS, **−1,1K** contra Bin (2/0/1, 150 CS).

Narración:
- 1480-1505 (≈16:39-17:04): «Doran sí o sí necesita hacer flanqueos… pero Bin simplemente hace las rotaciones, es mucho más rápido su teleportación. Y la tarea de Bin es justo evitar que Doran pueda empujar».
- 1516-1528 (≈17:15-17:27): «Oner atrapa a Knight, un asesinato importantísimo… esta es la pelea que necesitaba T1… atrapan a Bin, logran hacerle mucho daño, pero no pueden seguir con esta pelea».
- 1530-1547 (≈17:29-17:46): «Y Seraphine atrapa a cuatro, otros tres empalados. Hermosa pelea grupal generada por ON… va a caer Oner, va a caer Doran y este va a ser el dragón para BLG».
- Repetición (vtt 1589-1626): «La teleportación siempre hace una ventaja por parte de BLG. Llega Bin… Doran está cerca porque también tenía teleportación… logra separar a tres personajes de BLG, pero fíjate cómo está gastando recursos, y quienes no están gastando recursos, la Seraphine junto con el Skarner, porque están esperando el momento… le pega justamente al clon. El clon de Oner es el traidor».
- vtt 1667-1679: «Tan perdiendo todos los objetivos los chicos de T1… se terminan llevando el dragón, se llevan el heraldo».

## ⚠ Sin verificar / cuidado
1. **Larvas del vacío:** el contador junto al reloj (T1 1 · BLG 2) son las larvas (cambia en esta pelea; esto resuelve el ⚠ 6 de `datos_j6.md`). Pero el rótulo «Red team has slain the Voidgrubs!» (08:37-08:42) choca con el +1 de T1 a las 08:41 y con «Faker se lleva la vacu-larva» de la narración. Lo seguro: **BLG 2, T1 1**.
2. «Le tiran una pedrada» (Q de Skarner) y «secuestrado» (definitiva de Skarner) sobre Doran los dice la narración; en los cuadros solo se ven Xun y Bin encima de Doran y Bin con la definitiva encendida. Que Doran no tenía Flash («no hay Flash») también es solo de la narración.
3. Muerte de Peyz a las 11:05: el rótulo cae entre dos cuadros revisados (t=28 y t=33); el autor (Viper) sale del feed.
4. Que la Vayne sea contraselección del Renekton es una deducción del orden de las casillas (Renekton ≈VOD 380, Vayne ≈VOD 413), no lo dice un rótulo. El significado exacto de «FEARLESS PB%» (selección+bloqueo en el torneo) no se comprobó.
5. El orden de selección de BLG (Viktor, Ashe, Seraphine, Renekton, Skarner) sale del orden de las casillas antes del reacomodo.
6. Whisper large-v3 no cargó (RAM); usé medium. Escribe T1 = «Tijuana», BLG = «Vili Vili/Bilibili», Ornn = «Orn». Las citas de arriba ya van corregidas; las marcadas «vtt» vienen de los subtítulos automáticos (±2 s).
7. En el tramo 16:39-17:05 no corté fuente: el teletransporte de Bin al carril superior y su regreso solo están en la narración y en el minimapa de t=1.
