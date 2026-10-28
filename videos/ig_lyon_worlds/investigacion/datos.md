# IG vs LYON — Worlds 2026, Suiza ronda 4 (28-oct-2026) — datos verificados

Investigación hecha el 27-oct-2026. Cada dato lleva su fuente. Leyenda de fiabilidad:
- **[API]** = API oficial de Riot/LoL Esports (esports-api.lolesports.com o feed.lolesports.com), descargada directamente.
- **[LP]** = Liquipedia (wikitexto o página renderizada por su API, descargada directamente).
- **[WP]** = Wikipedia en inglés (wikitexto descargado directamente).
- **[BUSQ]** = solo vi el titular o el resumen del buscador; el artículo devolvió 403 (Cloudflare) y no pude leerlo entero. Úsalo con cuidado y, si va a la voz, cítalo como «según Sheep Esports», etc.

Fuentes base:
- API calendario Worlds: `https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-US&leagueId=98767975604431411` (cabecera `x-api-key: 0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z`)
- API detalle del partido IG–LYON: `https://esports-api.lolesports.com/persisted/gw/getEventDetails?hl=en-US&id=115660540726095065`
- Liquipedia Worlds 2026: https://liquipedia.net/leagueoflegends/World_Championship/2026
- Liquipedia Suiza: https://liquipedia.net/leagueoflegends/World_Championship/2026/Swiss_Stage
- Wikipedia Worlds 2026: https://en.wikipedia.org/wiki/2026_League_of_Legends_World_Championship

---

## 1. HORARIO del 28-oct-2026 (Credit Union of Texas Event Center, Allen, Texas)

| Partido | Formato | UTC | Texas (CDT, UTC−5) | Centro de México (UTC−6) |
|---|---|---|---|---|
| Movistar KOI vs T1 | Bo3, ronda 4 (2-1 vs 2-1) | 20:00 | **15:00** | **14:00** |
| LYON vs Invictus Gaming | Bo3, ronda 4 (2-1 vs 2-1) | 23:00 | **18:00** | **17:00** |

- API: `startTime` = `2026-10-28T20:00:00Z` (MKOI–T1, match 115660540726095061) y `2026-10-28T23:00:00Z` (LYON–IG, match 115660540726095065), ambos `bestOf 3`, estado `unstarted`. [API]
- Liquipedia: «Oct 28 - 15:00 CDT High (2-1) MKOI…» y «Oct 28 - 18:00 CDT High (2-1) IG / LYON». [LP Swiss_Stage y página LYON «Upcoming Matches»]
- Wikipedia: ronda 4, Match 31 MKOI–T1 15:00 (UTC−5); Match 32 IG–LYON 18:00 (UTC−5); «28–30 October: 15:00 CDT (20:00 UTC)». [WP]
- Conversión: el 28-oct Texas sigue en horario de verano (CDT = UTC−5; EE. UU. lo quita el domingo 1-nov-2026). El centro de México no tiene horario de verano desde 2022 (UTC−6). Por eso hay **1 hora de diferencia**: 18:00 en Texas = 17:00 en CDMX.
- **OJO, la hora real puede ADELANTARSE**: el 25-oct, LYON–GEN estaba programado a las 17:00 CDT (API: 22:00 UTC; Wikipedia: 17:00) pero el partido arrancó a las **15:52 CDT** según Liquipedia (el feed oficial muestra la partida 1 empezando ~20:59 UTC), justo después del Bo3 anterior. Lo prudente en el video: «a partir de las 5 de la tarde, hora del centro de México, o en cuanto termine T1 contra KOI».
- Mismo día: KOI vs T1 (confirmado). Los otros 2-1 juegan el 29-oct (TES vs BLG, 18:00 CDT). [API, LP]
- Lado y elección: LYON (sembrado n.º 2 del LCS) tiene el **Derecho de Primera Selección** para el juego 1 por ser «higher seed» frente a IG (n.º 4 del LPL): «As the higher seed, LYON earned the Right of First Selection for game 1». [LP Swiss_Stage] La API lista provisionalmente a LYON en lado azul en los juegos 1 y 2 e IG en azul en el 3 [API getEventDetails], pero con la regla de primera selección LYON puede elegir lado O primera elección; no lo afirmes hasta verlo en el VOD.

## 2. QUÉ ESTÁ EN JUEGO (confirmado)

- Formato suizo: 16 equipos, 5 rondas; **3 victorias = pasa a la fase de eliminación (cuartos de final); 3 derrotas = eliminado**. Los partidos de eliminación y de clasificación son **Bo3 con Fearless Draft** (un campeón usado por cualquiera de los dos equipos ya no se puede volver a elegir en esa serie); el resto, Bo1. [LP Worlds_2026 «Format»; WP «Format»]
- IG y LYON van 2-1 → **el ganador llega a 3-1 y se clasifica a cuartos; el perdedor queda 2-2 y juega la ronda 5 el 31-oct** (Bo3, «12:00 CDT» de inicio de jornada; los cruces 2-2 aún sin definir). [LP Swiss_Stage: round5 = October 31; API: tres Bo3 TBD el 31-oct a 17:00, 20:00 y 23:00 UTC]
- Ronda 5 = 2-2 vs 2-2: el ganador pasa (3-2), el perdedor queda fuera (2-3). [LP, WP «3–2, advance / 2–3, eliminated»]
- Cuartos de final: 3, 4, 5 y 6 de noviembre (22:00 UTC = 17:00 CDT), Bo5; semifinales 7 y 8-nov en Allen; **final el 14-nov en el Barclays Center de Nueva York**. [API calendario; LP infobox venue3 = Barclays Center]
- Sorteo de cuartos: los 3-0 contra los 3-2; los 3-1 entre sí. Si gana, IG o LYON (3-1) enfrentaría a otro equipo 3-1. [LP «Draw Shows»]
- Tabla antes de la ronda 4: 3-0 = Dplus KIA y Gen.G (ya clasificados). 2-1 = BLG, IG, LYON, TES, MKOI, T1. 1-2 = KC, CFO, TL, LOS, G2, HLE. 0-3 eliminados = Anyone's Legend (n.º 1 del LPL) y Team Secret Whales. [API récords; LP Prize Pool «15-16: al, tsw»]

## 3. LYON

### Historia de la organización
- Organización **mexicana**, fundada (en LoL) el **2-abr-2013** por Karzek, FraGio y Nikez; antes se llamó **Lyon Gaming** y luego **Rainbow7**. [LP LYON: https://liquipedia.net/leagueoflegends/LYON]
- **Nov-2017**: Riot dictaminó que el nombre y logo de Lyon Gaming no pertenecían al dueño; multa de **12 500 USD** y cambio de nombre forzado; desde dic-2017 compitió como **Rainbow7** (2018-2024), con patrocinio «Movistar R7». [LP LYON § «Forced to rebrand», cita a esportsinsider.com]
- La Worlds 2024 la jugó como «Movistar R7»; nombre oficial Rainbow7, propiedad de Just Toys International. [WP 2024 Worlds, nota del equipo: https://en.wikipedia.org/wiki/2024_League_of_Legends_World_Championship]
- **31-oct-2024**: Rainbow7 se fusiona con **Six Karma** (otra organización mexicana) y vuelve a llamarse **LYON**, como representante de la LLA en la nueva LTA (liga de las Américas). [LP LYON y LP Six_Karma]
- 2025: jugó la **LTA Norte** (la LTA unió LCS, CBLOL y LLA en una liga). Al disolverse la LTA, el LCS volvió en 2026 y **LYON confirmó su plaza en el LCS 2026** como equipo socio. [WP 2026 LCS season: https://en.wikipedia.org/wiki/2026_LCS_season]
- **29-30 ago-2026**: LYON fue anfitrión del primer «Team Homegrounds» del LCS en la **Ciudad de México** (Arena Esports Stadium, Artz Pedregal). [WP 2026 LCS season] Ese fin de semana (semana 6) ganó **2-0 a Cloud9 y 2-0 a Team Liquid**. [API calendario LCS, 29 y 30-ago]
- Títulos regionales (LP «Achievements»): LAT Regional Finals 2013; LAN Apertura y Clausura 2015; LLA Clausura 2020; LLA Apertura 2023; LLA Clausura 2023 (invicto en la fase regular de ese split); LLA Clausura 2024; **LCS Lock-In 2026; LCS Spring 2026**. Ganancias aproximadas totales: 746 900 USD. [LP LYON]
- Mundiales anteriores de la organización: **2017** (como Lyon Gaming, Play-In; eliminado por Cloud9 3-0 según el titular de Dot Esports listado en LP) [LP LYON § Media; WP 2017 Worlds]; **2023** (Movistar R7, Play-In) [WP 2023 Worlds]; **2024** (Movistar R7, Play-In: le ganó 2-1 a **100 Thieves** de Norteamérica, luego perdió 0-2 y 1-2 contra paiN y quedó fuera) [API calendario Worlds 2024; WP 2024 Worlds]. **2026 es su primer Mundial como equipo del LCS y la primera vez que llega a la fase suiza.** [WP Worlds 2026 § Qualified teams]
- MSI 2018 como Rainbow7 (entrevistas listadas en LP LYON § Media).

### Su temporada 2026 (todo con fuente)
| Torneo | Resultado | Fuente |
|---|---|---|
| LCS Lock-In 2026 (24-ene a 1-mar) | **Campeón**: final 3-1 a Cloud9 (1-mar) | API LCS; LP; WP 2026 LCS |
| First Stand 2026 (São Paulo, 16-22 mar) | Fase de grupos: 3-2 a LOUD, 0-3 vs Gen.G, 1-3 vs JD Gaming (eliminado) | WP https://en.wikipedia.org/wiki/2026_First_Stand_Tournament |
| LCS Spring 2026 | Fase regular 2.º (5-2); **Campeón**: final 3-0 a Team Liquid (14-jun, Tempe, Arizona). Primer título de LCS de la org. Finals MVP: Saint | API; LP; WP; [BUSQ] Sheep «LYON captures the LCS championship by beating Team Liquid 3-0» |
| MSI 2026 (Daejeon, Corea) | **3.er lugar**: 3-0 FURIA, 0-3 BLG, 3-0 TSW, 3-0 G2, 2-3 HLE (final de la llave baja, 11-jul). HLE fue campeón (3-2 a BLG) | API MSI; LP LYON «2026-07-11 3rd»; WP MSI 2026 |
| LCS Summer 2026 | Fase regular **1.º (6-1)**; playoffs: 1-3 vs C9, 3-1 vs Shopify Rebellion (26-sep, le dio la plaza mundialista), 3-1 vs C9; **final 1-3 vs Team Liquid** (4-oct, Gas South Arena, Duluth/Atlanta) → **subcampeón = LCS n.º 2** | API; LP LCS/2026/Summer; WP Worlds 2026 tabla de clasificados («Summer Runner-up: LYON») |

- Dato fuerte: el MSI 2026 fue «el primer top 3 internacional de un equipo del LCS desde 2019». [BUSQ GosuGamers: https://www.gosugamers.net/lol/news/78769-lyon-sweep-g2-3-0-to-secure-first-lcs-top-three-international-finish-since-2019]
- LYON fue uno de cuatro equipos de las seis ligas principales que se clasificó a los tres torneos internacionales del año (First Stand, MSI y Worlds). [WP 2026 LCS season]
- Premios del Summer 2026: **Berserker = MVP del split** y 1.er equipo All-Pro; **Saint** = 1.er All-Pro; **Dhokla e Isles** = 2.º All-Pro. Saint fue «Player of the Series» en LYON–SR y C9–LYON. [LP LCS/2026/Summer]
- Inspired se perdió las primeras semanas del Summer (asuntos personales en Polonia; «nada malo», según él); lo sustituyó Armao (récord de 3-1), que se fue el 17-ago. [LP LCS/2026/Summer notas, con tuit de @LyonLATAM 22-jul-2026; BUSQ Sheep Esports]

### Plantilla 2026 (Liquipedia, Worlds 2026 y página LYON)
| Rol | Jugador | Nombre | Nacionalidad | Nac. | En LYON desde | Trayectoria clave |
|---|---|---|---|---|---|---|
| Top | **Dhokla** | Niship Doshi | EE. UU. (también India) | 17-jul-1997 | 13-ene-2026 | NRG (Worlds 2023), 100 Thieves (Worlds 2025); también fue entrenador |
| Jungla | **Inspired** (capitán) | Kacper Słoma | **Polonia** | 24-ene-2002 | 3-dic-2025 | Rogue (LEC, subcampeón LEC Spring 2021), Evil Geniuses (campeón LCS Spring 2022; 3-4.º MSI 2022), FlyQuest (campeón LCS Summer 2024, LTA Norte Split 2 y 3 2025 y LTA Championship 2025) |
| Medio | **Saint** | Kang Seong-in | Corea del Sur | 1-ene-2005 | 23-dic-2024 | Dplus KIA Challengers (LCK CL 2024); el más veterano en LYON |
| Tirador (ADC) | **Berserker** | Kim Min-cheol | Corea del Sur | 25-may-2003 | 8-dic-2025 | Cloud9 (Worlds 2022 y 2023); MVP del LCS Summer 2026 |
| Soporte | **Isles** | Jonah Rosario | Australia | 7-mar-2001 | 8-dic-2025 | Legacy Esports (Worlds 2020), Dignitas (2025) |
| Entrenador principal | **Reignover** | Kim Yeu-jin | Corea del Sur | 4-jul-1995 | — | Ex-jungla de Fnatic (2015), Immortals, Team Liquid, CLG |
| Asistente | **Rigby** | Han Earl | Corea del Sur | 5-dic-1995 | — | Ex-coach de Freecs y Evil Geniuses |

Fuentes: LP https://liquipedia.net/leagueoflegends/Inspired , /Saint , /Berserker_(Korean_player) , /Dhokla , /Isles , /Reignover , /Rigby ; plantilla también en API getTeams (`lyon-gaming`, home league «LCS / NORTH AMERICA»).
- Inspired es «capitán» (tuit de Biblos citado en LP: «temporarily taking the place of our captain»); Reignover lo describió como su principal *shotcaller* y líder dentro del juego. [LP notas; BUSQ Sheep «LYON Reignover: It's really hard for a new jungler to come in and fill Inspired's role»]
- **Ninguno de los cinco titulares es mexicano** (EE. UU., Polonia, 2 coreanos, Australia); la academia (LYON Academy, liga regional) tiene venezolanos y un colombiano. [LP LYON]
- Curiosidad Inspired: fue el primero en jugar el Nunu rediseñado en un Mundial (FlyQuest vs HLE, Worlds 2024); top 50 de Challenger a los 15 años. [LP Inspired § Trivia]
- Inspired en Worlds 2024 con FlyQuest: cuartos de final, perdieron **2-3 contra Gen.G**. [BUSQ GosuGamers «Gen.G avoid near upset by FlyQuest…»]

### Qué significa para Norteamérica
- LYON = LCS n.º 2 (bombo 3 del sorteo). [LP «Pool 3: LCS#2 (LYON)»]
- Su victoria 1-0 sobre Secret Whales (23-oct) fue la primera de Norteamérica en este Mundial (dato del usuario por VOD). Un LYON 3-1 lo metería en cuartos en un Mundial que se juega en EE. UU.
- Contexto: TL eliminó 2-0 al n.º 1 de China (Anyone's Legend, 26-oct), que se fue **0-3**. [API; WP ronda 3 match 30]
- Frases útiles (≤15 palabras, con atribución):
  - Inspired (DPM.LOL, pre-Mundial): «I don't dream, because I've never been in a Worlds final». [BUSQ https://dpm.lol/news/worlds-2026-lyon-inspired-interview]
  - Berserker (Sheep, MSI 2026): «I think I am just as good as Gumayusi». [BUSQ https://www.sheepesports.com/articles/lyon-berserker-i-think-i-am-just-as-good-as-gumayusi-before-his-series-against-hle/en]
  - Berserker (Sheep, ene-2026): «I didn't want to return. But with Inspired, I thought it could work». [LP LYON § Interviews]
  - Dhokla (Sheep, mar-2026): «I really like playing League and winning, that's what drives me». [LP LYON § Interviews]

## 4. INVICTUS GAMING (IG)

### Historia
- Fundada el **2-ago-2011** por **Wang Sicong** (hijo de Wang Jianlin, del grupo Dalian Wanda), que compró el equipo CCM por unos **6 millones de USD**. El nombre viene del poema «Invictus» de W. E. Henley. Su equipo de Dota 2 ganó **The International 2012**. [WP https://en.wikipedia.org/wiki/Invictus_Gaming ; LP https://liquipedia.net/leagueoflegends/Invictus_Gaming]
- Dic-2014: Rookie llega de KT Rolster (junto a KaKAO) durante el «éxodo coreano». [WP IG; LP Rookie]
- 2017: fichan a TheShy y JackeyLove; pierden 2-3 con Team WE la clasificación al Mundial. [LP Rookie § Biography; LP IG Results]
- **Campeón del mundo 2018**: final el **3-nov-2018** en el **Incheon Munhak Stadium** (Corea): **IG 3-0 Fnatic**. Plantilla: **TheShy, Ning, Rookie, JackeyLove, Baolan** (coach Kim). **MVP de la final: Ning**. Primer título mundial de China (LPL) y primer campeón no coreano tras cinco años seguidos de Corea; **la final más rápida de la historia: 85 minutos de juego en total**. En cuartos ganaron 3-2 a KT Rolster (ex-equipo de Rookie) y en semis 3-0 a G2. Premio: 2 418 750 USD. [WP https://en.wikipedia.org/wiki/2018_League_of_Legends_World_Championship ; WP IG; LP Rookie; LP IG Results]
- 2019: campeón LPL Spring (3-1 JDG); MSI 2019 semifinal (1-3 TL); Worlds 2019 semifinal (1-3 FPX). En el MSI 2019 venció a SKT T1 en **15:57**, récord de la victoria internacional más rápida (WP dice que sigue vigente en 2026; ref. Dexerto). [WP IG]
- 2020-2024: sin Mundial (2020 cayó en el Regional Finals 1-3 ante LGD; 2021-2024 fuera de playoffs casi siempre). [LP IG Results]
- **8-dic-2024**: reúnen a **TheShy y Rookie** (TheShy volvía tras un año sin competir). [BUSQ Sheep «TheShy, JieJie, Rookie, GALA and Meiko join Invictus Gaming»] Reestructuración de la org. con Oxygen Sports y HUYA como accionistas (30-nov-2024). [LP IG timeline]
- **Worlds 2025**: n.º 4 del LPL, cayó en el Play-In 1-3 contra T1 (17.º). [API Worlds 2025; LP IG Results]
- Ene-2026: campeón de la **Demacia Cup 2025** (3-0 JDG). [LP IG Results]

### Su temporada 2026 y clasificación
| Torneo | Resultado | Fuente |
|---|---|---|
| LPL Split 1 | 5-6.º (1-3 AL) | LP IG Results; API |
| LPL Split 2 | 9-12.º: cayó 0-3 contra TT en el Play-In | LP; API |
| LPL Split 3 | **3.º**: grupo Nirvana 4-2; playoffs 3-2 TES, 3-1 WE, 3-0 LGD, 2-3 AL | API standings y calendario; LP IG Results |
| LPL Regional Finals (Shanghái, 17-19 sep) | 1-3 vs Top Esports (llave alta; TES = n.º 3) y luego **3-1 vs JD Gaming** (final de la llave baja, 19-sep) → **LPL n.º 4** | API; LP LPL/2026/Regional_Finals; WP Worlds 2026 («Regional Qualifiers 4th Seed Playoff Winner») |

- El LPL tuvo 4 plazas porque BLG fue subcampeón del MSI 2026 (región n.º 2). [LP Worlds 2026 nota IG]
- IG = bombo 4 del sorteo (LPL#4). [LP Draw]
- Sheep Esports: Rookie vuelve a la fase principal de un Mundial **siete años después** (su última fue 2019). [BUSQ Sheep «Invictus Gaming qualify for Worlds 2026 with a 3-1 win over JD Gaming»]

### Plantilla 2026 (Liquipedia Worlds 2026 y LPL Regional Finals; coincide con API getTeams `invictus-gaming`)
| Rol | Jugador | Nombre | Nacionalidad | Nac. | Notas |
|---|---|---|---|---|---|
| Top | **TheShy** | Kang Seung-lok | Corea del Sur | 11-nov-1999 | Campeón del mundo 2018 con IG; subcampeón 2023 con Weibo Gaming (WP 2023 Worlds: final T1 3-0 WBG) |
| Jungla | **Wei** | Yan Yangwei | China | 9-nov-2002 | Ex-RNG y BLG; **MVP del MSI 2022** con RNG (WP 2022 MSI) |
| Medio | **Rookie** | Song Eui-jin | Corea del Sur | 11-mar-1997 (Busan) | Campeón del mundo 2018; en IG desde dic-2014 (con pausas); contrato hasta 2027 [BUSQ Sheep] |
| Tirador | **JiaQi** | Zi Jiaqi | China | 31-may-2004 | — |
| Soporte | **Meiko** (capitán) | Tian Ye | China | 6-jun-1998 | **Campeón del mundo 2021 con EDG**; campeón del primer MSI (2015); récord LPL de 3112 días seguidos en un club (EDG); **primer jugador en llegar a 1000 partidas en el LPL** (12-abr-2025) |
| Suplente | Assum | — | — | — | Tirador, no ha jugado |
| Entrenador principal | **Helper** | Kwon Young-jae | Corea del Sur | 24-mar-1995 | Ex-top; coaches: Fury, chengz; supervisor Kezman |

Fuentes: LP https://liquipedia.net/leagueoflegends/TheShy , /Rookie , /Wei , /JiaQi , /Meiko , /Helper_(Korean_player) ; LP LPL/2026/Regional_Finals.
- ¿Volvió Rookie? Sí, está desde la reunión de dic-2024. ¿TheShy? Sí, desde la misma fecha.
- De la plantilla campeona de 2018 siguen **TheShy y Rookie**; Meiko aporta otro anillo mundial (2021). **Tres campeones del mundo** en el once inicial de IG.
- Ojo: la Wikipedia de IG lista a «Daeny» como entrenador (desactualizado; Daeny entrena a BLG en este Mundial según LP). Usa Helper.

## 5. ENFRENTAMIENTOS PREVIOS Y RENDIMIENTO EN WORLDS 2026

### IG vs LYON
- **No encontré ningún enfrentamiento oficial previo entre IG y LYON/Rainbow7/Lyon Gaming.** Revisé con la API oficial todos los partidos de Worlds (2023-2026) y MSI (2024-2026): el único IG–LYON es el del 28-oct. Por las fechas, tampoco coincidieron en Mundiales anteriores: IG no fue a Worlds 2017 ni 2020-2024, y Lyon/R7 no fue a 2018-2019 ni 2025. Lo más probable: **primer enfrentamiento de la historia** (ver DUDAS).

### Resultados de la suiza (todo Bo1 salvo GEN–LYON)
| Ronda | Partido | Resultado | Duración | Fuente |
|---|---|---|---|---|
| 1 (23-oct) | Gen.G vs IG | GEN 1-0 | 26:01 | WP; API |
| 1 (23-oct) | Secret Whales vs LYON | LYON 1-0 | 26:49 | WP; LP |
| 2 (24-oct) | LYON vs Karmine Corp | LYON 1-0 | 37:32 | WP; LP |
| 2 (24-oct) | IG vs Secret Whales | IG 1-0 | 30:20 | WP; LP |
| 3 (25-oct) | Hanwha Life vs IG | IG 1-0 | 28:36 | WP; LP |
| 3 (25-oct) | Gen.G vs LYON (Bo3) | GEN 2-1 (LYON ganó el 1.º en 35:45; GEN el 2.º en 26:32 y el 3.º en 31:57). MVP de la serie: Kiin | WP; LP |

- Juego 1 LYON–GEN: LYON 10/4/29, 9 torres, 2 barones, 66,7k de oro vs 59,8k; win.gg lo llamó uno de los juegos más limpios del torneo. [WP; BUSQ win.gg https://win.gg/invictus-gaming-vs-lyon-worlds-2026-predictions/]
- IG–HLE: IG 29 asesinatos contra 9, 4 dragones. [WP]

### Estadísticas por jugador (de los marcadores finales del feed oficial de LoL Esports, `https://feed.lolesports.com/livestats/v1/window/<gameId>`; idénticos a los de Liquipedia)
KDA = (asesinatos + asistencias) / muertes; KP = participación en los asesinatos del equipo.

**IG (3 partidas, 2-1)**
| Jugador | K/D/A total | KDA | KP | Campeones |
|---|---|---|---|---|
| TheShy | 11/12/28 | 3,25 | 65 % | Rumble, K'Sante, Kled |
| Wei | 8/5/39 | 9,40 | 78 % | Jarvan IV, Nocturne, Nocturne |
| Rookie | 17/9/27 | 4,89 | 73 % | Aurora, Orianna, **Annie** (7/1/13 vs HLE) |
| JiaQi | 20/9/18 | 4,22 | 63 % | Jhin, Ashe, Yunara (12/4/6 vs HLE) |
| Meiko | 4/8/45 | 6,12 | 82 % | Alistar, Seraphine, Lulu (3/0/22 vs HLE) |

**LYON (5 partidas, 3-2 en juegos)**
| Jugador | K/D/A total | KDA | KP | Campeones |
|---|---|---|---|---|
| Dhokla | 8/11/30 | 3,45 | 60 % | K'Sante ×2, Galio, Olaf, Shen |
| Inspired | 6/13/41 | 3,62 | 75 % | Nocturne, Wukong, Xin Zhao, Vi, Maokai |
| Saint | 20/7/26 | **6,57** | 73 % | Anivia, Syndra, Ahri, Akali, Tristana |
| Berserker | **25**/12/22 | 3,92 | 75 % | Ezreal (**13/1/5** vs TSW), Yunara ×2, Kalista, Lucian |
| Isles | 4/13/53 | 4,38 | **90 %** | Alistar, Lulu ×2, Renata, Milio |

Partidas (gameId → gol.gg): LYON–TSW 115660540726095018 (https://gol.gg/game/stats/83644/page-summary/), LYON–KC …024 (83649), IG–TSW …034 (83650), IG–HLE …046 (83654), IG–GEN …006, LYON–GEN …042/…043/…044.
- Notas: los marcadores de cada partida están en Liquipedia Swiss_Stage («Game details»). Berserker es el jugador de LYON con más asesinatos y Saint el de mejor KDA; en IG destaca Wei (solo 5 muertes en 3 partidas).
- Ojo con el Fearless: en el Bo3 no se repite campeón. Wei jugó Nocturne dos veces y LYON lo jugó (Inspired) contra TSW: si sale en el juego 1, desaparece para el resto.

## 6. DATOS DE COLOR (con fuente)
- **Tres campeones del mundo en IG** (TheShy y Rookie 2018; Meiko 2021) contra un LYON **sin ningún título mundial**; el mejor resultado internacional de Inspired es el 3.º del MSI 2026 y la semifinal (3-4.º) del MSI 2022. [LP]
- **Rookie tiene 29 años** (nació el 11-mar-1997) y está en IG desde dic-2014. [LP Rookie]
- **Meiko: 1000 partidas en el LPL**, el primero en lograrlo. [LP Meiko, cita Weibo del LPL]
- IG 2018: la final más corta de la historia (85 min de juego en total). [WP 2018]
- LYON: de multa y cambio de nombre forzado en 2017 a jugar un Mundial en Texas como LCS n.º 2. [LP LYON]
- LYON jugó en casa en CDMX (Artz Pedregal, 29-30 ago) y ganó 2-0 a C9 y a TL. [WP 2026 LCS; API]
- LYON en 2026: 2 títulos de LCS, 3.º en el MSI, subcampeón del Summer. Hay un hilo narrativo: LYON perdió por poco con los gigantes (2-3 con HLE en el MSI, 2-1 con GEN aquí). [API; WP; BUSQ win.gg]
- El LPL lo está pasando mal: su n.º 1 (Anyone's Legend) se fue 0-3. IG ganó a HLE, el campeón del MSI. [API; WP]
- Homenaje: antes del día 4 de la suiza (26-oct) hubo un minuto de silencio por **Lauri «Cyanide» Happonen**, jungla de Fnatic campeón del Mundial de 2011. [WP Worlds 2026 ronda 3]
- La final será en el **Barclays Center de Nueva York (14-nov)**; el lema del torneo es «THIS IS OUR MOMENT». [LP infobox]

---

## DUDAS (sin confirmar o con matices)
1. **Hora real de inicio de IG–LYON**: la oficial es 18:00 CDT / 17:00 CDMX, pero el 25-oct un Bo3 empezó más de 1 h antes de su hora porque el anterior acabó rápido. Puede pasar lo mismo si T1–KOI termina 2-0.
2. **Lado o primera elección en el juego 1**: LYON tiene el derecho de primera selección (LP), pero no se sabe aún si elegirá lado azul o primera elección; la API muestra a LYON en azul, pero puede ser provisional.
3. **Primer enfrentamiento IG–LYON**: no encontré ninguno (API oficial: Worlds 2023-2026 y MSI 2024-2026; cruce de años en Liquipedia y Wikipedia). La API no cubre antes de 2023 y no revisé torneos menores (IEM, etc.), así que dilo como «hasta donde sabemos» o «no hay registro oficial».
4. **Cuádruple de Rookie con Annie vs HLE**: no la encontré en ningún medio escrito (el feed solo da 7/1/13); vale el VOD que ya tienes.
5. **Citas de entrevistas** (Inspired en DPM.LOL, Berserker y Reignover en Sheep, Dhokla): solo vi titulares o resúmenes del buscador; las páginas devolvieron 403. El texto exacto del titular es fiable, el contexto no lo he leído.
6. **Récord del MSI 2019 (15:57 vs SKT)**: Wikipedia dice que sigue vigente «en 2026», sin fuente actual; dilo con prudencia («fue récord»).
7. **Worlds 2017 de Lyon Gaming**: solo confirmado que jugó el Play-In y que Cloud9 la eliminó (titular de Dot Esports listado en Liquipedia); el marcador exacto no lo verifiqué en el bracket.
8. **Dhokla «Estados Unidos / India»**: Liquipedia da las dos banderas (country y country2); probablemente es estadounidense de origen indio, no lo confirmé.
9. **Entrenador de IG**: Liquipedia dice Helper; la Wikipedia de IG (desactualizada, con aviso «Update») dice Daeny. Me quedo con Liquipedia.
10. **Stats agregadas (KDA, KP)**: las calculé yo a partir de los marcadores oficiales de cada partida; la página de estadísticas de Liquipedia y gol.gg (resumen del torneo) no se pudieron descargar (vacía/403). Las cifras por partida sí coinciden con Liquipedia.
11. **LYON en la EWC 2026**: Liquipedia (estadísticas de Inspired) muestra 3 partidas y 0 victorias de LYON en la Esports World Cup 2026; no verifiqué el bracket. Mejor no usarlo.
12. **Primera victoria de Norteamérica en Worlds 2026 (LYON>TSW)**: dato del usuario por VOD; no lo encontré redactado así en un medio.
