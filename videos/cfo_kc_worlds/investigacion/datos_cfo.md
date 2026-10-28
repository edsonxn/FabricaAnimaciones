# CFO vs KC — Worlds 2026, Suiza ronda 4 (29-oct-2026): EL PARTIDO + CTBC FLYING OYSTER — datos verificados

Investigación hecha el 28-oct-2026. Cada dato lleva su fuente. Leyenda de fiabilidad (la misma que `videos/ig_lyon_worlds/investigacion/datos.md`):
- **[API]** = API oficial de Riot/LoL Esports (esports-api.lolesports.com o feed.lolesports.com), descargada directamente.
- **[LP]** = Liquipedia (wikitexto por su API, o la página renderizada de la fase suiza que ya estaba en `investigacion/lp/swiss_render.txt`).
- **[WP]** = Wikipedia en inglés (wikitexto descargado directamente; copias en `investigacion/wp_cfo/`).
- **[VOD]** = cuadro sacado del VOD oficial de YouTube con `yt-dlp -g` + ffmpeg y mirado a ojo (`investigacion/cuadros/`).
- **[BUSQ]** = solo vi el titular/resumen del buscador; el artículo dio 403 o la página está bloqueada. Úsalo con cuidado y, si va a la voz, atribúyelo («según Sheep Esports…»).

**Bloqueos de esta sesión:** Liquipedia y Leaguepedia nos devolvieron «Rate Limited» casi toda la sesión (dos agentes consultando a la vez) y YouTube dio **HTTP 429 a los subtítulos automáticos** de los tres VOD (probado 5 veces con 2 clientes distintos). Por eso **no hay .vtt ni resumen de lo que dicen los narradores**; el desfase VOD/reloj se calibró con cuadros del VOD (método más fiable que los subtítulos). Ver DUDAS.

Fuentes base:
- API calendario Worlds: `https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US&leagueId=98767975604431411` (cabecera `x-api-key: 0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z`) → `sched_98767975604431411.json`
- API detalle del partido CFO–KC: `https://esports-api.lolesports.com/persisted/gw/getEventDetails?hl=en-US&id=115660540726095073` → `ev_cfo_kc.json`
- Feed de cada partida: `https://feed.lolesports.com/livestats/v1/window/<gameId>` (sin clave) → scripts `muertes.py`, `cfo_stats.py`, `cfo_objetivos.py`
- Liquipedia Worlds 2026: https://liquipedia.net/leagueoflegends/World_Championship/2026 · Suiza: https://liquipedia.net/leagueoflegends/World_Championship/2026/Swiss_Stage
- Wikipedia: https://en.wikipedia.org/wiki/2026_League_of_Legends_World_Championship · https://en.wikipedia.org/wiki/CTBC_Flying_Oyster

---

## 1. EL PARTIDO (jueves 29-oct-2026, Credit Union of Texas Event Center, Allen, Texas)

| Partido | Formato | UTC | Texas (CDT, UTC−5) | Centro de México (UTC−6) |
|---|---|---|---|---|
| **CTBC Flying Oyster vs Karmine Corp** | Bo3 Fearless, ronda 4 «Low» (1-2 vs 1-2) | 20:00 | **15:00** | **14:00** |
| Top Esports vs Bilibili Gaming | Bo3 Fearless, ronda 4 «High» (2-1 vs 2-1) | 23:00 | **18:00** | **17:00** |

- API: `startTime` = `2026-10-29T20:00:00Z`, match id **115660540726095073**, `bestOf 3`, estado `unstarted`, bloque «Swiss». gameIds reservados: juego 1 = **115660540726095074**, juego 2 = **…075**, juego 3 = **…076**. La API lista provisionalmente a **CFO en azul en los juegos 1 y 2 y a KC en azul en el 3** (provisional). [API getEventDetails]
- El otro partido del día: BLG vs TES, match 115660540726095069, `2026-10-29T23:00:00Z`, Bo3 (ambos 2-1: el ganador se clasifica a cuartos). [API] Liquipedia: «Oct 29 - 15:00 CDT Low (1-2) KC / CFO» y «Oct 29 - 18:00 CDT High (2-1) TES / BLG». [LP swiss_render] Wikipedia: Karmine Corp vs CTBC Flying Oyster, 29 October, 15:00 (UTC−5). [WP]
- Conversión: Texas sigue en horario de verano hasta el domingo 1-nov-2026 (CDT = UTC−5); el centro de México está en UTC−6 todo el año → **15:00 Texas = 14:00 CDMX**. Al ser el primer partido del día no debería adelantarse (el adelanto de 1 h del 25-oct fue en un segundo Bo3 del día; ver datos.md de IG–LYON).

### Récords y qué está en juego (CONFIRMADO)
- Récords en la API antes del partido: **CFO 1-2 y KC 1-2**. [API getSchedule, `record`]
- Camino de CFO: R1 **ganó** a Team Liquid Alienware (Bo1, 23-oct); R2 **perdió** con Movistar KOI (Bo1, 24-oct); R3 **perdió** con T1 (Bo1, 26-oct). [API; LP; WP]
- Camino de KC (para cruzar con el otro agente): R1 ganó a Anyone's Legend (Bo1, 23-oct); R2 perdió con LYON (24-oct); R3 perdió con BLG (26-oct). [API]
- Formato suizo: 3 victorias = cuartos; 3 derrotas = eliminado; los partidos de eliminación y clasificación son **Bo3 con Fearless Draft**. [LP Worlds_2026 «Format»; LP Swiss_Stage]
- **Es un partido a muerte**: el **perdedor queda 1-3 y se va del Mundial**; el **ganador queda 2-2 y juega la ronda 5 el sábado 31-oct** (Bo3, 2-2 contra 2-2: el que gana pasa a cuartos 3-2, el que pierde cae 2-3). La API ya tiene tres Bo3 «TBD» el 31-oct a las 17:00, 20:00 y 23:00 UTC (12:00, 15:00 y 18:00 CDT = 11:00, 14:00 y 17:00 CDMX), sin cruces definidos (sorteo tras la ronda 4). [API; LP «round5 = October 31»; LP: «The match order is yet to be announced»]
- Mismo bloque «Low (1-2)»: el 30-oct juegan **TLAW vs LOS** (15:00 CDT) y **G2 vs HLE** (18:00 CDT). Los 3-0 (DK, GEN) ya están en cuartos; los 0-3 (AL, TSW) ya fuera. [API; LP]

### Primera selección
- **CFO tiene el Derecho de Primera Selección para el juego 1**: «As the higher seed, CTBC Flying Oyster earned the Right of First Selection for game 1». [LP swiss_render, ronda 4 Low] Regla: en la suiza la tiene «the team with a higher regional seed». [LP Worlds_2026 «Format»] CFO es **LCP n.º 2**; KC entró como **LEC n.º 3** (ganador del Play-In). [LP Worlds_2026, Pool 4: «LCP#2 (CFO)… Play-In Winner (KC)»]
- Cómo la usó CFO antes en este Mundial: vs T1 (también tenía el derecho) **eligió segunda selección** y T1 tomó lado azul; vs MKOI (sorteo) **eligió segunda selección** y MKOI tomó azul. Contra TL no la tenía (TL eligió azul, CFO segunda selección). Es decir, **CFO siempre ha jugado en lado rojo con «second pick»** en esta Worlds. [LP swiss_render] Probable que repita, pero no lo afirmes hasta ver el draft.

### Enfrentamientos previos CFO–KC (oficiales, API + WP)
Revisé con la API Worlds 2023-2026, MSI 2024-2026, First Stand 2025-2026 y EWC 2026. **Solo se han cruzado en el First Stand 2025** (LoL Park, Seúl), y dos veces en la misma semana:
| Fecha | Fase | Resultado | Detalle |
|---|---|---|---|
| 11-mar-2025 | Grupos, Bo3 (match 113470740396478931) | **CFO 2-0 KC** | 29:54 (15-7 en asesinatos, 4 dragones, 10 torres) y 33:53 (22-9, 2 barones) [API; WP 2025 First Stand] |
| 15-mar-2025 | **Semifinal**, Bo5 (match 113470740396478953) | **KC 3-2 CFO** | KC ganó 1.º (35:07) y 2.º (28:26; 24-1 en asesinatos); **CFO empató 2-2** (31:32 y 30:13) y **KC ganó el 5.º en 39:28** (18-13). KC perdió la final 1-3 contra HLE. [API; WP] |
- Wikipedia: CFO quedó 3-4.º, su mejor resultado internacional, «knocked out by Europe's Karmine Corp in the semifinals». [WP CTBC Flying Oyster]
- **Narrativa: es una revancha.** CFO remontó de 0-2 a 2-2 y perdió el quinto juego. De aquel CFO siguen **Rest y Doggo**; de aquel KC probablemente siguen Canna, Yike y Caliste (NO verificado aquí: plantilla de KC 2026 según LP Worlds_2026: Canna, Yike, kyeahoo, Caliste, Busio; la plantilla de KC 2025 la confirma el otro agente). [LP; API alineaciones]
- No se cruzaron en Worlds 2025 ni en MSI 2025 (KC no fue a ninguno de los dos). [API]

---

## 2. CFO — HISTORIA

- **Nombre y origen:** «CTBC Flying Oyster» (中信飛牡蠣). En mandarín, «飛牡蠣» (*fēi mǔlì*, «ostra voladora») **suena como la palabra inglesa «family»**: el nombre chino se lee como «CTBC Family», guiño al lema del banco **CTBC: «We are family»**, que también es el lema del equipo. [WP CTBC Flying Oyster § Team identity; LP § Trivia]
- **Dueño:** CTBC Sports Entertainment, filial del **CTBC Bank** (Taiwán); el mismo grupo es dueño del equipo de béisbol **CTBC Brothers** y del de baloncesto **New Taipei CTBC DEA**. Sede: Taipéi. Colores azul y amarillo. [WP; LP]
- **Fundación:** 26-ene-2022, comprando una plaza del PCS. **Ojo, las fuentes no coinciden:** WP dice que compró la plaza de **Machi Esports**; LP dice la de **Hong Kong Attitude**. La plantilla fundadora eran ex-jugadores de **Machi Esports y J Team**: Rest (top), Gemini (jungla), Mission (medio), Atlen (tirador) y Koala (soporte). [WP; LP] → **No es linaje de PSG Talon**: Talon fue su gran rival (le ganó dos finales del PCS por 3-2, primavera 2022 y verano 2023).
- **Rest es el único que queda del equipo fundador de 2022** (top desde el primer día; contrato renovado el 15-dic-2025: «We are happy to announce Rest will be staying at CFO as our top laner»). [WP; LP timeline]
- **Títulos domésticos:** PCS Summer 2022 (3-0 a Beyond Gaming en la final); **LCP 2025 Kickoff** (3-1 a Talon, **primer título de la historia del LCP**), **LCP 2025 Mid-Season** (fase regular invicta, final 3-2 a GAM) y **LCP 2025 Season Finals** (3-0 a Team Secret Whales). **3 LCP + 1 PCS = 4 títulos.** CFO comparte con TSW el récord de títulos del LCP (3). [WP CTBC Flying Oyster y League_of_Legends_Championship_Pacific; API LCP: finales 23-feb, 8-jun y 21-sep-2025]
- **Mundiales previos:**
  - **2022** (fase de grupos): una sola victoria, **contra 100 Thieves**; empató último del grupo. [LP § History; WP]
  - **2023** (Play-In): eliminado por Team BDS (0-2), 19-20.º. [WP; LP]
  - **2024**: no se clasificó. [WP]
  - **2025** (Pekín/Shanghái): suiza 3-2 → **cuartos de final**, primer equipo del LCP en llegar y **el primero de Asia-Pacífico desde 2015** (Flash Wolves y ahq). Resultados: 1-0 a Fnatic (32:00), **1-0 a T1 (32:22; 25-11 en asesinatos)**, 1-2 con Anyone's Legend, 0-2 con HLE, 2-0 a FlyQuest; cuartos **0-3 contra KT Rolster** (29-oct-2025). [WP 2025 Worlds; API]
  - **Le ganó a T1 en la suiza de 2025 y ese T1 acabó campeón del mundo** (final 9-nov-2025: T1 3-2 KT). [WP; API] ← dato llamativo.
- **MSI 2025** (primera vez en un MSI): perdió **2-3 contra T1** tras ir **2-1 arriba** (el 2.º juego lo ganó 24-3 en asesinatos), ganó **3-1 a Movistar KOI** y cayó 1-3 con Anyone's Legend (5.º). [WP 2025 MSI; API]
- **First Stand 2025:** semifinalista (3-4.º), su mejor resultado internacional; en grupos solo perdió con HLE. [WP]
- **2025 fue histórico:** según WP, CFO fue el único equipo de las cinco ligas grandes que se clasificó a los **tres** torneos internacionales de 2025 (First Stand, MSI y Worlds). [WP CTBC Flying Oyster § 2025]
- Doggo hizo un **pentakill contra T1 en el MSI 2025** y otro en la final del LCP 2025 contra TSW. [BUSQ resumen de Leaguepedia https://lol.fandom.com/wiki/Doggo — no verificado en VOD]

### Hechos llamativos para quien no conoce a CFO
1. Su nombre chino es un **juego de palabras con «family»** (el lema del banco que los paga). [WP]
2. **Le ganó a T1 en el Mundial 2025** y T1 fue campeón; y en el MSI 2025 tuvo a T1 a un juego de caer (2-1 arriba, perdió 2-3). [WP; API]
3. En 2025 ganó **las tres ligas del año** y fue el **primer equipo de Asia-Pacífico en cuartos de un Mundial en 10 años**. [WP]
4. **Ya se cruzó con KC: le ganó 2-0 y luego perdió la semifinal 2-3** remontando de 0-2 (First Stand 2025). [API; WP]
5. 2026 fue lo contrario: **casi último del LCP medio año**, cambió medio y soporte en abril y **se metió al Mundial en el último split** (ver tabla). [API; WP 2026 LCP]

---

## 3. CFO — PLANTILLA 2026 Y TEMPORADA

### Plantilla (LP Worlds_2026 y WP CTBC Flying Oyster; coincide con API getTeams `ctbc-flying-oyster`, liga «LCP / PACIFIC»)
| Rol | Jugador | Nombre | Nacionalidad | En CFO | Trayectoria (fuente) |
|---|---|---|---|---|---|
| Top | **Rest** | Hsu Shih-chieh (API: SHI-JIE XU) | Taiwán | desde la fundación (ene-2022) | Ex-Machi/J Team; único fundador que queda; Mundiales 2022, 2023 y 2025 con CFO [WP; LP] |
| Jungla | **Shad0w** | Zhao Zhiqiang | **Italia** (WP: «nat = IT») | 15/16-dic-2025 | Empezó en Europa (Element Gaming, Outplayed), luego LEC y LPL: FunPlus Phoenix y Bilibili Gaming; sustituyó a JunJia; «tercera liga grande» de su carrera [BUSQ Sheep «lol-shad0w-joins-ctbc-flying-oyster-in-lcp», 16-dic-2025; BUSQ Leaguepedia] |
| Medio | **POUT** | Han In-woong (API: INUNG HAN) | Corea del Sur | debut oficial **18-abr-2026** (LCP Split 2, semana 3) | Venía de **Saigon Dino** (Vietnam); campeón LCK Academy Series 2021 Summer con Shadow EK; sustituyó a **Pungyeon**, que se fue «a petición propia» (anuncio del 4-may-2026) [API alineaciones; BUSQ Sheep «sources-pungyeon-set-to-join-ctbc-flying-oyster» y agregadores] |
| Tirador | **Doggo** (capitán) | Chiu Tzu-chuan | Taiwán | 2025 | Ex-LPL (Bilibili Gaming, Ultra Prime); suplente de emergencia de PSG Talon en el MSI 2021; pentakills en LPL 2023, final LCP 2025 y MSI 2025 vs T1; **1.er equipo All-Pro del LCP Split 3 2026** [LP Worlds_2026 «bot, captain»; WP 2026 LCP; BUSQ Leaguepedia/Sheep] |
| Soporte | **Kino** | Wu Hsin-jung (API: XIN-RONG JHU WU) | Taiwán | debut oficial **18-abr-2026** | Sustituyó a **2274** (bajado a la academia, anuncio 4-may-2026) [API alineaciones; BUSQ] |
| Entrenador | **Chawy** | Wong Xing Lei | — | — | «storied coach», siguió al frente en 2026 [LP; WP; BUSQ Sheep] |
| Asistente | **Wulala** | Liu Sheng-wei | Taiwán | — | — [LP; WP] |

- **Jugador estrella: Doggo.** Capitán, el único CFO en el 1.er equipo All-Pro del LCP (Split 3 2026), máximo daño de CFO en este Mundial (58,2k sumando las 3 partidas) y ya era «el carry principal» de CFO en Worlds 2025. [WP 2026 LCP; LP marcadores; BUSQ Sheep «lol-worlds-the-five-players-to-watch»] Premios Split 3 2026: Shad0w y POUT 2.º equipo All-Pro; Kino 3.º. [WP 2026 LCP § Awards]
- **Firma de Rest: Rumble.** Lo jugó en 11 de las 26 series del LCP 2026 (primer juego) y en 2 de las 3 partidas de este Mundial. [API alineaciones `alineaciones_cfo_2026.txt`; feed]
- Rareza: Doggo jugó **Syndra y Xerath de tirador** en el LCP Split 3 (31-jul y 2-ago-2026). [API alineaciones]
- **Edades: NO verificadas** (Liquipedia/Leaguepedia bloqueadas). Ver DUDAS.
- Fotos oficiales (API getTeams):
  - Logo: http://static.lolesports.com/teams/1656307849320_CFO_Logo.png (alternativo …849321_CFO_Logo.png)
  - Rest: http://static.lolesports.com/players/1769232185565_Rest.png
  - Shad0w: http://static.lolesports.com/players/1769232218550_Shad0w.png
  - POUT: http://static.lolesports.com/players/1785926070523_POUT.png
  - Doggo: http://static.lolesports.com/players/1769232306480_Doggo.png
  - Kino: http://static.lolesports.com/players/1785926061333_Kino.png
  - Foto de equipo en Worlds 2025 (cuartos): Liquipedia «CFO at Worlds 2025 Quarterfinals Features Day.jpg» (Driver, HongQ, Rest, JunJia, Kaiwing, Doggo). [LP]

### Temporada 2026 (todo de la API, contrastado con WP 2026 LCP season)
| Torneo | Resultado | Fuente |
|---|---|---|
| LCP Split 1 (ene-feb) | Fase regular 3-4 en series (5.º); playoffs: **1-3 vs Ground Zero** (13-feb) → fuera en 1.ª ronda. 3 puntos de campeonato | API; WP |
| First Stand 2026 | No se clasificó | API; WP |
| LCP Split 2 (abr-may) | Fase regular 2-5 (6.º); **cambio de medio y soporte (POUT y Kino) el 18-abr**; playoffs: **2-3 vs MVK** (23-may) → fuera en 1.ª ronda. 2 puntos | API; WP |
| MSI 2026 | No se clasificó (fueron TSW y DCG) | API; WP |
| EWC 2026 | No aparece en la API del EWC 2026 | API |
| LCP Split 3 (jul-ago) | Suiza: 2-0 DCG, 2-1 GAM, **0-3 TSW**, 3-1 GZ; desempates: 3-2 MVK y **3-2 TSW** → **1.er sembrado** a playoffs; playoffs: 3-0 MVK, 0-3 TSW, **3-1 MVK (29-ago, le dio el boleto al Mundial)**; **final 0-3 vs TSW** (30-ago, Taipei Heping Basketball Gymnasium) → **subcampeón = LCP n.º 2** | API; WP |

- TSW ganó los tres splits del LCP 2026 (y se fue 0-3 de este Mundial). [WP 2026 LCP; API]
- Wikipedia: «Between 22 and 29 August… MVK Esports and CTBC Flying Oyster qualifying». [WP 2026 Worlds]

---

## 4. CFO — CAMINO EN ESTA WORLDS (3 Bo1, 1-2)

| Ronda | Partido (match id) | gameId | Resultado | Duración | Lado CFO | VOD inglés (LoL Esports) | VOD español MX | Desfase VOD |
|---|---|---|---|---|---|---|---|---|
| 1 (23-oct, 17:10 CDT) | TLAW vs CFO (…095007) | **115660540726095008** | **CFO gana** 12-11 | 37:32 | rojo | **FATvv4Lk7IU** (45:20) | EYe_B57eTIo | **VOD = reloj + 470 s (7:50)** |
| 2 (24-oct, 12:59 CDT) | MKOI vs CFO (…095021) | **115660540726095022** | CFO pierde 7-19 | 33:08 | rojo | **sLoG6iB0L2Q** (40:25) | BsNSLY_6HsY | **VOD = reloj + 438 s (7:18)** |
| 3 (26-oct, 12:00 CDT) | T1 vs CFO (…095049) | **115660540726095050** | CFO pierde 6-14 | 27:23 | rojo | **cmct78Iytg8** (37:21) | yOOx_G_0t04 | **VOD = reloj + 598 s (9:58)** |

- Canal de los VOD: «LoL Esports» (inglés) y «LoL Esports Latinoamérica» (es-MX); títulos «TLAW vs. CFO | WORLDS 2026 | Swiss Stage | Day 01», etc. [yt-dlp; API `vods`] Transmisión completa (LP): https://youtu.be/uG9SCwcHA7k?t=24875 (TL–CFO), https://youtu.be/xa70p5u-mmw?t=9816 (MKOI–CFO), https://youtu.be/ECJoJ7ez7-4?t=6061 (T1–CFO). gol.gg: 83639, 83647, 83662. [LP]
- **Desfases calibrados con cuadros del VOD** [VOD]: FATvv4Lk7IU 600 s → reloj 02:10 y 1500 s → 17:10 (ambos +470); sLoG6iB0L2Q 600 s → 02:42 y 1500 s → 17:41 (+438/+439); cmct78Iytg8 1090 s → 08:12, 1140 s → 09:02, 1500 s → 15:02, 2073 s → 24:35 (todos +598). El reloj de `muertes.py` coincide con el del juego (±10 s; muestreo del feed cada 10 s).
- Narradores (LP): TL–CFO Drakos y Kobe; MKOI–CFO CaptainFlowers y Vedius; T1–CFO CaptainFlowers y Dagda.

### Drafts (LP swiss_render + feed)
| Partida | CFO (Rest / Shad0w / POUT / Doggo / Kino) | Rival | Bans (azul / rojo) |
|---|---|---|---|
| vs TL ✅ | Rumble / Qiyana / Viktor / Aphelios / Alistar | Galio, Lee Sin, Syndra, Jhin, Rakan | TL: Akali, Vi, Cassiopeia, Ashe, Draven · CFO: Orianna, Ezreal, Renata, Nautilus, Lulu |
| vs MKOI ❌ | Olaf / Lee Sin / Akali / Tristana / Lulu | Trundle, Qiyana, Cassiopeia, Kalista, Renata | MKOI: Lucian, Rumble, Nocturne, Aphelios, Caitlyn · CFO: Ezreal, Vi, Anivia, Skarner, K'Sante |
| vs T1 ❌ | Rumble / Qiyana / Ryze / Kai'Sa / Alistar | Ambessa, Vi, Galio, Jhin, Rakan | T1: K'Sante, Draven, Syndra, Poppy, Nautilus · CFO: Renata, Nocturne, Cassiopeia, Anivia, Ahri |
(La asignación de bans por lado sale del orden de LP; verifícalo en el VOD si va a pantalla.)
- **Rival que respeta Rumble:** MKOI le baneó Rumble a Rest; las dos veces que lo jugó, CFO fue a Rumble + Qiyana + Alistar. **Fearless:** si CFO saca Rumble en el juego 1, ya no lo tiene en el 2 ni el 3.

### Marcadores finales (feed oficial, `s_<gameId>.txt`; idénticos a LP)
| Partida | Rest | Shad0w | POUT | Doggo | Kino | Oro CFO–rival | Objetivos CFO |
|---|---|---|---|---|---|---|---|
| vs TL | 4/3/3 | 5/2/5 | 1/1/6 | 2/1/7 | 0/4/12 | 74,2k–65,4k | 8 torres, 1 inhib, **1 barón, 5 dragones (alma de montaña + Elder)** |
| vs MKOI | 3/5/0 | 0/4/5 | 2/4/1 | 1/4/1 | 1/2/3 | 57,7k–71,7k | 2 torres, 1 barón, 0 dragones |
| vs T1 | 0/3/1 | 2/2/3 | 0/2/2 | 4/3/2 | 0/4/6 | 50,5k–56,7k | 4 torres, 2 dragones |

### Estadísticas por jugador en el torneo (sumadas de los marcadores oficiales; KDA = (K+A)/M; KP sobre 25 asesinatos de CFO)
| Jugador | K/D/A total | KDA | KP | Daño a campeones (LP) | Campeones |
|---|---|---|---|---|---|
| Rest | 7/11/4 | 1,00 | 44 % | 36,2k | Rumble ×2, Olaf |
| Shad0w | 7/8/13 | 2,50 | 80 % | 42,4k | Qiyana ×2, Lee Sin |
| POUT | 3/7/9 | 1,71 | 48 % | 34,9k | Viktor, Akali, Ryze |
| **Doggo** | 7/8/10 | 2,13 | 68 % | **58,2k** | Aphelios, Tristana, Kai'Sa |
| Kino | 1/10/21 | 2,20 | **88 %** | 9,7k | Alistar ×2, Lulu |
- CFO: 25 asesinatos y 44 muertes en 3 partidas. Ganó la partida más larga (37:32) y perdió las otras dos antes del minuto 34. [feed; LP]

---

## 5. JUGADAS CANDIDATAS DE CFO (con `muertes.py` + `cfo_objetivos.py`; archivos `m_<gameId>.txt` y `o_<gameId>.txt`)

### JUGADA A — «La pelea del Elder» vs Team Liquid (la remontada) ★ recomendada
- gameId **115660540726095008**, VOD **FATvv4Lk7IU**, desfase +470 s.
- **Antes:** TL dominaba el marcador: **10-5 en asesinatos al 32:12** (Yeon, Jhin, 5/0 y sin morir) y había roto 3 torres antes que CFO; pero CFO tenía **4 dragones** (hextech 06:39, océano 12:01, montaña 17:17, **montaña 27:58 = alma de montaña**) contra 1 de TL. Oro casi parejo (TL +437 al 32:10, CFO +224 al 32:12). [feed]
- **La pelea (reloj 34:01–34:32, en el foso del dragón):**
  1. 34:01 Shad0w (Qiyana) mata a **CoreJJ** (Rakan) → 10-6
  2. 34:29 Rest (Rumble) mata a **Josedeodo** (Lee Sin) → 10-7
  3. 34:30 Quid (Syndra) mata a **Shad0w** → 11-7
  4. 34:32 **POUT (Viktor) mata a Quid** → 11-8 (cuadro del VOD a 42:20: «CFO POUT has slain TLAW Quid!» junto al foso, oro CFO +1,5k) [VOD]
  5. **34:41 CFO mata al Dragón Ancestral (Elder)** → 5.º dragón; **35:16 Barón** para CFO.
- **VOD:** pelea desde **41:51** (2511 s); Elder a **42:31** (2551 s); Barón a **43:06** (2586 s). Arranca el corte a ~41:35 para ver la preparación.
- **Por qué sirve:** explica CÓMO gana CFO: juego de objetivos (alma de dragón) aunque vaya perdiendo en asesinatos, y una pelea de 4 contra el reloj alrededor del foso. Es su única victoria del torneo.

### JUGADA B — El final con «TRIPLE KILL» de Rest (Rumble) vs Team Liquid
- Mismo gameId/VOD. Tras Elder + Barón, CFO tira 4 torres e inhibidor (36:10–37:07) y entra a la base de TL:
  - 37:17 **Rest mata a Morgan** (Galio) · 37:18 **Rest mata a CoreJJ** · 37:22 **Doggo (Aphelios) mata a Josedeodo** · 37:25 **Rest mata a Quid** → 4 muertes en 8 s; nexo a las 37:32. Oro final +7,8k para CFO. [feed]
- Cuadro del VOD a 45:11 (2711 s): rótulo **«TRIPLE KILL!»** de Rest con el «Baron Powerplay» activo, junto a la fuente de TL; marcador 11-11, reloj 37:21. [VOD]
- **VOD:** **44:59–45:20** (2699–2720 s; el VOD termina justo en el nexo). Para contexto, desde las torres: 44:00 (2640 s).
- **Por qué sirve:** la jugada del veterano (el único fundador de CFO) con su campeón firma, y cierra la remontada.

### JUGADA C — Doggo vs T1 (la estrella) y el «tiro» de CFO (su debilidad)
- gameId **115660540726095050**, VOD **cmct78Iytg8**, desfase +598 s.
- **Doggo (Kai'Sa) caza a Doran tres veces:** 08:12 Doggo mata a Doran (Ambessa) → 3-2; 09:02 otra vez → 4-3; 11:45 otra vez → 4-5 (CFO pasa delante en asesinatos). Además 11:36 Shad0w mata a Oner y **20:32 Shad0w (Qiyana) mata a Faker (Galio)**. VOD: 18:10 (1090 s), 19:00 (1140 s), 21:43 (1303 s); Faker a 30:30 (1830 s). Cuadros de 08:12 y 09:02 confirmados [VOD].
- **El giro:** al **24:33 CFO iba +2,1k de oro, 2 dragones a 1 y 4 torres a 3**. En 11 segundos T1 gana la pelea **5-0** en el río de arriba: 24:33 Peyz mata a Doggo · 24:38 Oner mata a POUT · 24:43 Peyz mata a Rest · 24:44 Peyz mata a Kino · 24:44 Faker mata a Shad0w. **25:24 Barón de T1**, 26:38–26:43 T1 hace *ace* otra vez (Oner 3 asesinatos) y gana a las 27:23. VOD: pelea en **34:31** (2071 s; cuadro a 34:33 «T1 Oner has slain CFO POUT!», marcador 7-6, CFO +0,8k) [VOD]; Barón a 35:22 (2122 s).
- **Por qué sirve:** enseña al jugador estrella ganando duelos contra un campeón del mundo y, en la misma partida, el problema de CFO: **pierde las peleas grandes de mitad de partida cuando va ganando** (también vs MKOI: tomó un Barón al 25:50 y perdió la pelea 4-0 entre 25:52 y 26:07, VOD sLoG6iB0L2Q 33:08–33:25).

---

## 6. DATOS DE COLOR (con fuente)
- Es **la revancha de la semifinal del First Stand 2025** (KC 3-2 tras remontada de CFO a 2-2). [API; WP]
- **Los dos llegan 1-2 y uno se va a casa**; el ganador jugará el sábado otra final de 2-2. [API; LP]
- CFO es el equipo que **le ganó a T1 en el Mundial 2025** y a quien T1 se lo devolvió en este (26-oct). [WP; API]
- CFO **perdió a 4 de 6 jugadores** del equipo que llegó a cuartos en 2025 (siguen Rest y Doggo; se fueron JunJia, HongQ, Kaiwing y Driver). [LP galería 2025; API alineaciones; BUSQ Sheep: Kaiwing a Vivo Keyd Stars]
- Medio año entre los últimos del LCP (2-5 en series en el Split 2) y aun así al Mundial: **los cambios de abril (POUT y Kino) le dieron la vuelta**; con ellos, final del Split 3. [API; WP]
- El LCP llega castigado: su n.º 1 (TSW) se fue 0-3; si CFO pierde, al LCP solo le quedaría… nadie (MVK cayó en el Play-In ante KC). [API]

---

## DUDAS (sin confirmar o con matices)
1. **Subtítulos / lo que dicen los narradores: NO conseguido.** YouTube respondió HTTP 429 a los subtítulos automáticos de los tres VOD durante toda la sesión. Reintentar más tarde: `yt-dlp --write-auto-subs --sub-langs en --skip-download -o "%(id)s" https://youtu.be/FATvv4Lk7IU` (y cmct78Iytg8, sLoG6iB0L2Q), luego `python vtt.py FATvv4Lk7IU.en.vtt 2500 2560` etc.
2. **Edades y fechas de nacimiento de la plantilla de CFO: NO verificadas** (Liquipedia y Leaguepedia en «rate limit»). Reintentar `https://liquipedia.net/leagueoflegends/api.php?action=parse&page=Doggo&prop=wikitext&format=json` (Rest, Shad0w_(Italian_player), POUT, Kino, Chawy).
3. **Trayectoria de Shad0w, POUT, Kino y Doggo**: solo de resúmenes del buscador (Sheep Esports 403, Leaguepedia, agregadores). La fecha de debut de POUT/Kino (18-abr-2026) y de quiénes sustituyeron (Pungyeon, 2274) sí está verificada en la API.
4. **Origen de la plaza de CFO**: WP dice Machi Esports, LP dice Hong Kong Attitude. Decir «compró una plaza del PCS en 2022» sin nombrarla.
5. **Pentakills de Doggo** (MSI 2025 vs T1, final LCP 2025): solo del resumen del buscador sobre Leaguepedia.
6. **Lado/elección del juego 1**: CFO tiene el derecho; en sus tres partidas eligió segunda selección (lado rojo). La API muestra a CFO en azul en los juegos 1 y 2, pero es provisional.
7. **H2H**: la API de Worlds solo llega a finales de 2023 y no revisé el EWC 2025 (KC no estuvo en MSI 2025, por lo que probablemente tampoco en el EWC 2025). Dilo como «su único cruce oficial fue en el First Stand 2025».
8. **Bans por lado**: asignados según el orden de LP; confirmar en el VOD si se muestran.
9. **Daño a campeones**: de LP (cifras entre paréntesis del marcador); el feed da `championDamageShare` coherente (Doggo 32 %, 36 %, 28 %).
10. **EWC 2026**: un resumen del buscador dice que Shad0w jugó el EWC 2026, pero la API del EWC 2026 no tiene ningún partido de CFO. Mejor no usarlo.

## Archivos en esta carpeta (míos)
`ev_cfo_kc.json`, `ev_11566054072609500{7,21,49}.json` (partidos y VOD), `sched_*.json` (calendarios), `partidos_cfo_kc.txt` (todos los cruces internacionales CFO/KC), `team_cfo.json`, `alineaciones_cfo_2026.txt` (+ `cfo_alineaciones.py`), `m_<gameId>.txt` (muertes), `s_<gameId>.txt` (marcador final, `cfo_stats.py`), `o_<gameId>.txt` (objetivos, `cfo_objetivos.py`), `cuadros/` (calibración), `lp_cfo/`, `wp_cfo/`, `url_*.txt` (URL directas temporales de YouTube, caducan).
