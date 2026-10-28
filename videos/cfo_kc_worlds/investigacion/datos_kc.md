# KARMINE CORP (KC) — Worlds 2026, previa de CFO vs KC (jue 29-oct-2026) — datos verificados

Investigación hecha el 28-oct-2026. Solo Karmine Corp (el partido y CFO los investiga otro agente). Cada dato lleva su fuente. Leyenda:
- **[API]** = API oficial de LoL Esports (esports-api.lolesports.com, cabecera `x-api-key: 0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z`) o feed oficial (`feed.lolesports.com/livestats/v1/window|details/<gameId>`), descargados directamente.
- **[LP]** = Liquipedia (wikitexto o página renderizada por su API). **[WP]** / **[WPfr]** = Wikipedia en inglés / en francés (wikitexto descargado).
- **[VOD]** = comprobado mirando un cuadro del VOD oficial de YouTube (yt-dlp -g + ffmpeg, un cuadro; recortes en `cuadros_kc/`).
- **[BUSQ]** = solo titular (no pude leer el artículo). Ninguno de los datos de abajo depende de un [BUSQ] salvo donde se indica.

Fuentes base:
- Liquipedia KC: https://liquipedia.net/leagueoflegends/Karmine_Corp · Play-In: https://liquipedia.net/leagueoflegends/World_Championship/2026/Play-In · Suiza: https://liquipedia.net/leagueoflegends/World_Championship/2026/Swiss_Stage
- Wikipedia: https://en.wikipedia.org/wiki/Karmine_Corp · https://fr.wikipedia.org/wiki/Karmine_Corp · https://fr.wikipedia.org/wiki/Kameto · https://en.wikipedia.org/wiki/2026_League_of_Legends_World_Championship · https://en.wikipedia.org/wiki/2026_LEC_season · https://en.wikipedia.org/wiki/2026_Mid-Season_Invitational · https://en.wikipedia.org/wiki/2026_Esports_World_Cup_–_League_of_Legends · https://en.wikipedia.org/wiki/2025_First_Stand_Tournament · https://fr.wikipedia.org/wiki/Caliste_(esport) · https://en.wikipedia.org/wiki/Canna_(gamer)
- API: `getEventDetails?hl=en-US&id=<matchId>` (copias en `ev_*.json`), `getTeams?hl=en-US&id=karmine-corp` (`teams_kc.json`).
- Marcadores por jugador: `stats_<gameId>.json` (script `stats.py`), muertes: `m_<gameId>.txt` (script `muertes.py`), agregados: `agrega.py`.

---

## 0. EL PARTIDO DE MAÑANA, VISTO DESDE KC (solo lo que toca a KC)
- API: match **115660540726095073**, CFO vs KC, Bo3, `2026-10-29T20:00:00Z` = **15:00 CDT (Texas) = 14:00 centro de México**. Juegos 115660540726095074/075/076 (la API pone a CFO en azul en los juegos 1-2 y a KC en el 3; provisional). [API]
- Liquipedia: «Worlds 2026 - Low (1-2)-Low (1-2)», es decir **ambos 1-2: el que pierde se va eliminado (1-3) y el que gana sigue vivo (2-2) para la ronda 5 del 31-oct**. «As the higher seed, CTBC Flying Oyster earned the Right of First Selection for game 1». [LP Swiss_Stage]
- **Ya se enfrentaron**: First Stand 2025 (Seúl, LoL Park): CFO ganó **2-0** en grupos (11-mar-2025) y KC se vengó **3-2** en la semifinal (15-mar-2025): KC se puso 2-0, CFO empató 2-2 y KC ganó el quinto (39:28). Después KC perdió la final 1-3 con Hanwha Life. [WP 2025 First Stand; WPfr KC]. De aquel KC siguen **Canna, Yike y Caliste** (Vladi y Targamas ya no están). [LP KC, timeline]

## 1. HISTORIA DE KARMINE CORP

### Fundación y dueños
- Fundada el **30-mar-2020** como **Kameto Corp** por los streamers **Kamel «Kameto» Kebir** (francés, n. 27-jun-1995 en Corbeil-Essonnes) y **Zouhair «Kotei» Darji** (belga en LP). [WP; WPfr; LP organización «Kotei — Belgium — Co-Owner & COO»]
- **16-nov-2020**: entra **Amine «Prime» Mekri** (youtuber, rapero y empresario) como cofundador y la estructura pasa a llamarse **Karmine Corp** (anunciado en directo en el Twitch de Kameto, 17-nov-2020). [WP; WPfr]
- Prime ya no está: LP lo da fuera como copropietario el 7-nov-2025; WPfr dice que el club anunció su dimisión el 9-feb-2026; WP en inglés añade que se fue tras acusaciones de «comportamiento inapropiado» de ex-empleados (investigación de «Revue 21»). **Fechas contradictorias: mejor no usarlo en el video.** (Ojo: el soporte «Prime» de Karmine Corp Blue, Olivier Payet, es OTRA persona.) [LP; WPfr; WP]
- Propiedad actual: Kameto vía la sociedad Zoldyck (37 %). [WPfr infobox]
- El apodo «Kameto» lo tomó en StarCraft 2 en homenaje a un tío que murió de cáncer. [WPfr Kameto]
- **Zidane: NO encontré nada** que lo relacione con KC en LP, WP ni WPfr. No lo uses.

### Su afición: el «Blue Wall» y los KCX
- Apodo de la afición/del club: **Blue Wall**; sus ultras, organizados en la asociación «Le Blue Wall», son famosos por animar «como hinchas de fútbol». Himno: «KELAWIN»; color: azul. [WP infobox; WPfr]
- Eventos propios «Karmine Corp Xperience» (KCX) y otros, con asistencia: [WPfr «Évènements physiques»]

| Fecha | Lugar | Evento | Asistencia |
|---|---|---|---|
| 26-jul-2021 | Palais des congrès de París | KCX (1.º) | 3 500 |
| 15-dic-2021 | Palau Sant Jordi (Barcelona) | Showmatch KC vs KOI (equipo de Ibai y Piqué) | 12 000 |
| 21-jun-2022 | Accor Arena (Bercy, París) | KCX2 (partido de liga vs Misfits Premier) | 12 000 |
| 16-sep-2023 | Paris La Défense Arena | KCX3 «Karmine Corp vs The World» | 28 000 |
| 9-nov-2024 | Paris La Défense Arena | KCX4 «Forever Rivals» | 28 000 (texto) / 30 000 (tabla) |
| 24-26 jul-2026 | Adidas Arena (París) | LEC Roadtrip organizado por KC | 8 500 |

- Desde mayo de 2024 tienen su propio recinto, **Les Arènes (Évry-Courcouronnes, Grand Paris Sud), 3 000 asientos**; «una primera para el esport occidental». [WP; WPfr]
- **Récord de audiencia**: la final del EU Masters Spring 2021 (KC 3-1 BT Excel) tuvo un pico de **377 531 espectadores**, récord para una final de EU Masters (fuente: Esports Charts). [LP KC § History]
- Kameto batió récords de audiencia en Twitch; en abril de 2022 coordinó a Francia en r/place (Reddit) ante **420 000 espectadores** para pintar el logo de KC. [WPfr Kameto]
- Tras ganar el primer EU Masters (2021), **Emmanuel Macron los felicitó** por mensaje privado en Twitter. [WPfr KC; WPfr Kameto]
- 2026: la Esports World Cup se mudó de Riad a **París** (Paris Expo Porte de Versailles) por la guerra en Oriente Medio; ahí KC llegó a la final. [WP 2026 Esports World Cup]

### Títulos (LoL) y trayectoria
- **LFL** (liga francesa): campeón Spring 2021 (en su primera temporada en primera división) y Summer 2023. [LP KC § History; WPfr]
- **EU Masters / EMEA Masters** (2.ª división europea): campeón **Spring 2021** (3-1 BT Excel), **Summer 2021** (3-2 Fnatic Rising), **Spring 2022** (3-1 LDLC; con **Rekkles** en la plantilla) y **Summer 2023** (3-2 Movistar Riders, en la Sud de France Arena de Montpellier). **Primer equipo en ganarlo 2 y 3 veces seguidas; récord de títulos.** Con la academia (KC Blue) suman un 5.º (Summer 2025). [LP KC Achievements; WP; WPfr «Records»]
- **18-oct-2023**: compra la plaza de **Astralis** en la LEC. [LP; WP]
- **LEC 2024**: debut durísimo (último en Winter y Spring, 2-7 en ambos); en Summer fichan a **Canna** (ex-T1) y a Vladi, y llegan a semifinales de la llave baja. [WPfr]
- **LEC Winter 2025: CAMPEÓN, 3-0 a G2 en la final (2-mar-2025)** → **primer club francés que gana la LEC**. [LP; WPfr]
- **First Stand 2025: subcampeón** (1-3 vs Hanwha Life; antes 3-2 a CFO en semis). [LP; WP]
- 2025: se quedaron sin Mundial (cayeron 1-3 con G2 y 1-3 con Fnatic en los partidos de clasificación del Summer). [WPfr]
- Ganancias totales aprox. (LoL): **917 471 USD**. [LP]
- **Worlds 2026 es el PRIMER Mundial de Karmine Corp.** «This is the first World Championship appearance for the LEC's Karmine Corp». [WP Worlds 2026]. Kameto, al entrar en la LEC (2023), lo presentó como un paso hacia su sueño de ganar el Mundial. [WPfr Kameto]

## 2. PLANTILLA 2026 (LP «Active», API getTeams, WP)

| Rol | Jugador | Nombre | País | Nacimiento (edad el 29-oct) | En KC desde | Trayectoria clave |
|---|---|---|---|---|---|---|
| Top | **Canna** | Kim Chang-dong | Corea del Sur | 11-feb-2000 (26) | 2-may-2024 | **T1 2019-21**: campeón **LCK Spring 2020 en su año de novato** («Royal Roader»), semifinal del **Mundial 2021** con T1 (2-3 vs DK); luego Nongshim y Dplus. Su nombre viene de Kanna Kamui, personaje de *Miss Kobayashi's Dragon Maid*. T1 lo fichó siendo Diamante 1 «atascado». |
| Jungla | **Yike** | Martin Sundelin | Suecia (también Perú) | 11-nov-2000 (25) | 14-dic-2024 | **G2 2023-24**: 4 títulos de LEC (Winter/Summer 2023, Winter/Spring/Summer 2024 + Season Finals); pentakill con Lillia en playoffs LEC 2024. Ex-Team Oplon y LDLC. |
| Medio | **kyeahoo** | Kang Yea-hoo | Corea del Sur | 13-ago-2005 (21) | 7-ene-2026 | DRX (LCK) y DRX Challengers; subcampeón Asia Masters 2025. Primer año en Europa. |
| Tirador | **Caliste** ⭐ | Caliste Henry-Hennebert | **Francia** (Béziers) | 28-ago-2006 (**20**) | 30-oct-2024 (en KC desde may-2023) | La estrella. Apodos «Le prodige», «Le Petit Prince». Campeón EMEA Masters 2023 a los 16 años; récord de kills de la LFL; no pudo subir a la LEC en 2024 por la nueva edad mínima (18); **el campeón más joven de un split de la LEC** (Winter 2025). **MVP del LEC Summer 2026.** Contrato hasta 2028. |
| Soporte | **Busio** | Alan Cwalina | EE. UU./Polonia (LP: bandera polaca y estadounidense; WP: EE. UU.) | 23-oct-2003 (23) | 7-ene-2026 | **FlyQuest** (NA): MSI 2024, Worlds 2024 y 2025, First Stand 2025. 1.er equipo All-Pro LEC Spring y Summer 2026. |
| Entrenador | **Reapered** | Bok Han-gyu | Corea del Sur | 30-ene-1992 (34) | 7-ene-2026 | Exjugador de **SK Telecom T1** (IEM Colonia 2012); entrenador de **Cloud9** (foto LP 2018) y de **100 Thieves** (Worlds 2022). |
| Asistente | Zeph | Quentin Viguié | Francia | — | 7-ene-2026 | — |

Fuentes: LP https://liquipedia.net/leagueoflegends/Canna , /Yike , /Kyeahoo , /Caliste , /Busio , /Reapered ; WP Canna_(gamer); WPfr Caliste_(esport); API getTeams. (Las páginas renderizadas de Busio, Caliste y Reapered en LP dieron 429; de ellas solo leí el wikitexto: fechas, banderas y galería.)
- Edad media del quinteto ≈ 23 años; **el único francés es Caliste**.
- Frase (titular de entrevista, LP Media): Caliste, rft.gg, 24-sep-2026: «I Won't Stop Until I've Won Worlds». [LP; titular]

### Temporada 2026 de KC
| Torneo | Resultado | Fuente |
|---|---|---|
| LEC Versus (ene-mar) | Fase regular **1.º (8-3)**; playoffs: 2-0 GIANTX, 0-2 G2, 2-1 Vitality, 3-0 GIANTX, 3-2 KOI; **final 2-3 vs G2** (1-mar, Badalona) → **subcampeón** | WP 2026 LEC; LP |
| LEC Spring (mar-jun) | Fase regular 2.º (7-2); 1-3 G2, 3-1 NAVI, 3-0 GIANTX, 3-0 KOI; **final 2-3 vs G2** (7-jun) → subcampeón y plaza en el MSI. All-Pro: Caliste y Busio (1.º), Canna y Yike (2.º), kyeahoo (3.º) | WP; LP |
| MSI 2026 (Daejeon, Corea, 28 jun-12 jul) | Play-in: 3-0 Deep Cross Gaming, **0-3 T1**, 0-3 Team Liquid → **10.º, eliminado** | WP MSI 2026 |
| Esports World Cup 2026 (París, 15-19 jul) | Grupos (0-1 vs Gen.G y luego clasificado); cuartos **2-0 AG.AL (Anyone's Legend)**; semis **2-1 T1**; **final 0-3 Dplus KIA** → **subcampeón, 340 000 USD** | WP EWC 2026 LoL; LP KC |
| LEC Summer (jul-sep) | **Fase regular PERFECTA 9-0**. Playoffs: 3-1 GIANTX, **1-3 G2**, **0-3 Movistar KOI** → **3.º = LEC n.º 3** (al play-in del Mundial). **MVP del split: Caliste**; el **1.er equipo All-Pro entero fue de KC** (Canna, Yike, kyeahoo, Caliste, Busio) | WP 2026 LEC |

- Patrón 2026: **tres finales o casi y ningún título** (dos finales perdidas 2-3 con G2 y la de la EWC 0-3). G2 ganó los tres splits. [WP]
- KC fue de los primeros clasificados de la LEC al Mundial (5-sep). [WP Worlds 2026]

## 3. KC EN ESTA WORLDS

### Play-in (Riot Games Arena, Los Ángeles; 4 equipos, doble eliminación, todo Bo5 Fearless; solo el ganador pasa a la suiza) [WP; LP Play-In]
| Fecha | Serie | Resultado | Partidas (KC primero en asesinatos; duración) | gameId |
|---|---|---|---|---|
| 15-oct | KC vs **Cloud9 KIA** (LCS n.º 3), ronda 1 | **3-2** | J1 **1-20** derrota (35:02) · J2 14-16 victoria (35:10) · J3 **5-22** derrota (37:44) · J4 **15-6** victoria (38:08; con Elder) · J5 **17-8** victoria (31:21) | 115660588583171787 / …788 / …789 / 116299649500204436 / …437 |
| 16-oct | KC vs **MVK Esports** (LCP n.º 3), final de la llave alta | **3-0** | 9-4 (30:14) · 21-11 (33:03) · 14-7 (36:13) | 115660588583171791 / …792 / …793 |
| 18-oct | KC vs MVK, partido de clasificación (MVK: 3-0 a FURIA en la ronda 1, 0-3 con KC y 3-1 a FURIA en la final de la llave baja) | **3-0** | 13-2 (28:28) · 17-6 (27:26) · 25-12 (26:51) | 116299649498303885 / …886 / …887 |

- Contra C9 **estuvo dos veces a una derrota de quedarse fuera** (C9 iba 1-0 y 2-1) y perdió dos partidas por 1-20 y 5-22; aun así ganó la serie. Después, **6-0 en partidas contra MVK**. Play-in: **9-2 en partidas**. [WP; API]
- MVP de la partida 3 de la clasificación (la que dio el pase): **kyeahoo** (Viktor 4/0/11). [LP Play-In]

### Fase suiza (Credit Union of Texas Event Center, Allen, Texas) — KC entró en el bombo 4 [WP]
| Ronda | Partido | Resultado | Duración | Asesinatos | gameId | Nota |
|---|---|---|---|---|---|---|
| 1 (23-oct) | KC vs **Anyone's Legend** (LPL n.º 1) | **KC 1-0** | 33:16 | 12-4; KC 2 barones, 64,8k vs 56,7k de oro | 115660540726095010 | MVP: **Canna** (Jax) [LP]. AL acabó 0-3. |
| 2 (24-oct) | KC vs **LYON** (LCS n.º 2) | LYON 1-0 | 37:32 | 15-15 | 115660540726095024 | KC iba **+4,7k de oro a los 22 min** y lo perdió (ver § 4) |
| 3 (26-oct) | KC vs **Bilibili Gaming** (LPL n.º 2) (1-1 vs 1-1, Bo1) | BLG 1-0 | 36:20 | 11-14 | 115660540726095052 | MVP: Viper [LP] |

Fuentes: WP Worlds 2026 (marcadores y duraciones); API (gameId); feed (asesinatos). Lados: KC eligió azul vs AL y vs LYON; vs BLG eligió primera selección (BLG azul). [LP Swiss_Stage]

### VOD oficiales (YouTube) y desfase VOD = reloj de la partida + N s
Canal «LoL Esports» (inglés) y «LoL Esports Latinoamérica» (español, un video por partida). IDs de la API (`vods`, locale en-US / es-MX). Desfases medidos leyendo el reloj del marcador en cuadros del VOD ([VOD], ±1-2 s).

| Partida | VOD inglés | Desfase inglés | VOD español (LATAM) | Desfase español |
|---|---|---|---|---|
| Play-in C9 (serie entera, 3:38:10) | **MzoFIu6m4AU** | J4: reloj + 8254 hasta ~15:00 y **reloj + 8457 después** (pausa de ~200 s hacia el min 15); J5: **reloj + 11198** (API: J4 empieza en 7913 s, J5 en 10741 s del VOD) | J4 **2xC2Jpk_duM** (46:50) · J5 **yT6HBEteZuw** (39:36) · J1 vRj_7F_dkBU · J2 FQzLwM276rA · J3 LbM_9rbDUoo | J4: reloj + 307 hasta ~15:00, **reloj + 509 después**; J5: **reloj + 449** |
| Play-in MVK 16-oct (serie) | ftCQbsVYrpk (2:00:39) | sin medir (API: J1 1 s, J2 2250 s, J3 4639 s) | LVoj-fv5M90 · K1aYI54_yK0 · o2wK6JD7ZMg | sin medir |
| Play-in MVK 18-oct (serie) | 4uxGpP2TG38 (1:44:14) | J3: reloj + 4642 (1 punto) (API: J3 empieza en 4212 s) | J1 Wl0t7oyZHQI · J2 ekcAcfji1f4 · **J3 b6rqLH90mtI** | J3: **reloj + 406** |
| Suiza vs AL | **8txB9yg9FNc** (39:39) | **reloj + 328** | QEh3z4aQJ8g (40:22) | reloj + 332 (1 punto) |
| Suiza vs LYON | jToExBjYenQ (44:41) | reloj + 430 (1 punto) | sd4LsYCStnc | sin medir |
| Suiza vs BLG | Lo6V52lXc94 (44:49) | **reloj + 510** | P1kX8LN9UeM | sin medir |

- **Feed vs reloj**: en AL el feed va ~5 s por detrás del reloj del juego; en C9 J4 el feed incluye la pausa (feed ≈ reloj + ~205 s al final); en C9 J5 el feed ≈ reloj; en MVK J3 ±20 s. Para cortar, usa siempre el reloj del VOD.

### Estadísticas por jugador en el torneo (marcadores finales del feed oficial; KDA = (K+A)/M; KP = participación en asesinatos; daño = % del daño a campeones del equipo, media por partida)

**Total Worlds 2026 (14 partidas, 10-4)** — coincide con LP («Worlds 2026: 14 GP, 10 W, 4 L» en la ficha de Canna)
| Jugador | K/D/A | KDA | KP | Daño | Campeones |
|---|---|---|---|---|---|
| Canna | 35/34/66 | 2,97 | 53 % | 25 % | Jayce ×3, Rumble ×3, Galio ×2, Kled, Renekton, Ambessa, Kennen, Zaahen, Jax |
| Yike | 46/30/78 | 4,13 | 66 % | 16 % | **Lee Sin ×5**, Vi ×2, Naafiri ×2, Qiyana ×2, Jarvan IV ×2, Trundle |
| kyeahoo | 39/33/72 | 3,36 | 59 % | 26 % | Viktor ×3, Cassiopeia ×3, Syndra ×2, Ahri ×2, Orianna ×2, Anivia, Ryze |
| **Caliste** | **60**/23/68 | **5,57** | 68 % | 25 % | Xayah ×2, Kalista ×2, Miss Fortune, Varus, Lucian, Kai'Sa, Draven, Ashe, Zeri, Yunara, Ezreal, Jhin |
| Busio | 9/27/124 | 4,93 | **70 %** | 8 % | Nautilus ×2, Rakan ×2, Renata ×2, Vel'Koz, Nami, Rell, Seraphine, Yuumi, Lulu, Leona, Alistar |

**Solo la suiza (3 partidas, 1-2)**: Canna 11/6/13 (KDA 4,0) · Yike 10/9/18 (3,1) · kyeahoo 3/8/26 (3,6) · **Caliste 13/5/18 (6,2; KP 82 %)** · Busio 1/5/34 (7,0; KP 92 %). KC: 38 asesinatos en 3 partidas.

- Caliste es el máximo anotador (60 asesinatos en 14 partidas, 4,3 por partida) y tiene el mejor KDA. Partidas clave: **Xayah 11/1/3 en el J4 de eliminación vs C9** (38 % del daño), Ezreal 9/1/3 en la partida del pase.
- **Fearless**: Yike ha jugado Lee Sin 5 veces y Canna Rumble 3 y Jayce 3; en un Bo3 Fearless, en cuanto salga uno, no se repite.

## 4. JUGADAS CANDIDATAS (cómo juega KC)

**Estilo de KC en este torneo (de los datos):** gana peleas a 5 alrededor de objetivos tardíos (Elder, Barón) con Caliste como carry de daño (≈25-38 %), Yike entrando primero (Lee Sin/Jarvan) y Busio en enganche (Nautilus, Rakan, Renata). **Pero** en sus dos derrotas suizas llegó con ventaja a media partida y perdió la pelea grande: vs LYON iba +4,7k a los 22:33 y, en la pelea del 28:51-29:11 (triple de Berserker), perdió 5 por 2; vs BLG perdió un 3 por 5 (28:14-28:21) y el 5 por 1 final (35:36-35:46). [feed, `m_*.txt`]

### Jugada A — **El cuádruple de Canna (Jax) contra el n.º 1 de China** (la mejor pelea ganada; ronda 1 de la suiza)
- gameId **115660540726095010** (KC azul vs AL rojo). MVP: Canna. [LP]
- Antes: minuto 24, asesinatos 2-2, oro casi igual (KC −0,3k), dragones 2-2, barones 0-0; AL tenía las 3 larvas. [feed]
- Orden (reloj del VOD; el feed va ~5 s después): ~24:44 cae Yike (Jarvan IV) a manos de Hope (Miss Fortune) → **Canna mata a Tarzan (Nocturne) y a Kael (Neeko)**, ~24:47-24:49 **Canna mata a Shanks (Akali)** (TRIPLE KILL en pantalla a las 24:52), kyeahoo (Orianna) mata a Breathe (Olaf), **Canna mata a Hope** → **QUADRA KILL (24:54) y ACE (~24:56)**. 5 por 1. [feed + VOD: carteles «TRIPLE KILL!», «QUADRA KILL!» y «ACE!» vistos en cuadros, `cuadros_kc/al_quadra.jpg`]
- Después: KC +2,0k, primer barón (~27:10) y segundo (~33:20); final 12-4 en 33:16. [feed; WP]
- VOD inglés **8txB9yg9FNc**: pelea en **1812-1824 s (30:12-30:24)**; con contexto desde ~1790 s. Español **QEh3z4aQJ8g**: 1816-1828 s.
- Por qué sirve: es la victoria más grande de KC en la suiza (AL acabó 0-3) y enseña al top que «entra» en medio de los 5.

### Jugada B — **Caliste, Xayah 11/1/3: Elder y ACE para no quedar eliminados** (la estrella; C9 J4, C9 iba 2-1)
- gameId **116299649500204436** (C9 azul vs KC rojo).
- Antes (reloj ~36:10): KC 7-4 en asesinatos, **+7,8k de oro, 4 dragones contra 1, 1 barón** (tomado hacia el 31:30). Hubo una **pausa de ~3:20** hacia el minuto 15 (el feed la cuenta; el reloj no). [feed; VOD]
- Orden (reloj): ~36:25-36:41 C9 caza a **kyeahoo (Orianna) y a Busio (Rakan)** (Tactical, Yunara) → 6-7. ~36:45-37:05 KC contesta: **Caliste mata a Tactical y a Vulcan (Lulu)**, Yike (Qiyana) a Loki (Sylas), Caliste a Blaber (Sejuani) → 6-11. **~37:29 «Red team has slain the Elder Dragon!»** (KC). ~37:45-37:52, ya en la base de C9: **Caliste mata a Thanatos (Zaahen), Tactical y Vulcan en ~3 s (triple)** y Canna (Renekton) a Loki → **ACE**, 6-15; nexo a las 38:08. **Caliste: 6 asesinatos en ese último minuto y cuarto.** [feed `m_116299649500204436.txt`; VOD: relojes `cuadros_kc/g4_final.jpg`, cartel del Elder en `g4_pelea_hoja.jpg`]
- VOD español **2xC2Jpk_duM** (reloj + 509): **2694-2790 s (44:54-46:30)**; Elder en ~2758. VOD inglés **MzoFIu6m4AU** (reloj + 8457): **10642-10738 s (2:57:22-2:58:58)**.
- Por qué sirve: partida a muerte (como la de mañana), la estrella decide, y enseña cómo cierra KC: objetivo (Elder) + pelea a 5 con el tirador limpiando.

### Jugada C — **La pelea que completó la remontada ante Cloud9** (C9 J5, el quinto)
- gameId **116299649500204437** (KC azul vs C9 rojo). Feed ≈ reloj aquí.
- Antes (30:01): KC 12-7, **+4,8k, 2 barones** (C9 3 dragones, KC 2). Antes hubo una pelea que volteó la partida: 20:44-21:03, KC gana 4 por 2 (de 4-4 a 8-5). [feed]
- Orden final: 30:41 kyeahoo (Ahri) mata a Tactical (Ziggs); 31:09 **Caliste (Kai'Sa)** a Blaber (Lillia); 31:13 Canna (Ambessa) a Vulcan (Shen); 31:16 Thanatos (K'Sante) mata a kyeahoo y kyeahoo a Loki (Yone) a la vez; 31:18 Caliste a Thanatos → nexo a las 31:21, con el «Barón powerplay» en pantalla. 6 por 1 dentro de la base de C9. [feed `m_116299649500204437.txt`; VOD `cuadros_kc/g5_pelea_hoja.jpg`]
- VOD español **yT6HBEteZuw** (reloj + 449): final **2290-2330 s (38:10-38:50)**; pelea del 20:44: 1693-1712 s. VOD inglés **MzoFIu6m4AU** (reloj + 11198): final **13039-13079 s (3:37:19-3:37:59)**; pelea del 20:44: 12442-12461 s.
- Por qué sirve: el «momento Karmine» del torneo; tras perder 1-20 y 5-22, cierra el 3-2.

### Extra — la partida que dio el pase a la suiza (MVK, clasificación, J3)
- gameId **116299649498303887** (MVK azul vs KC rojo), 25-12 en 26:51. MVK ganó la primera sangre (Canna muerto a los 3:17), pero KC lo volteó a los 5 min (5:13-5:21, Canna doble). Cierre: 26:09-26:30 (feed) KC mata 4 sin bajas; Caliste remata a Gury y Harky. MVP: kyeahoo. VOD español **b6rqLH90mtI** (reloj + 406): cierre ≈ 1975-2060 s. Inglés 4uxGpP2TG38 (reloj + 4642, 1 punto). [feed; LP; VOD]

### Narradores (subtítulos automáticos): **NO OBTENIDOS**
- `yt-dlp --write-auto-subs --sub-langs en --skip-download` devolvió **HTTP 429 (Too Many Requests)** en todos los intentos (8txB9yg9FNc, MzoFIu6m4AU, QEh3z4aQJ8g, 2xC2Jpk_duM, yT6HBEteZuw), aunque YouTube sí los ofrece («en-orig», «en»). Repetir más tarde con el mismo comando y resumir con `vtt.py <archivo>.vtt <desde> <hasta>` usando los segundos de arriba. Lo que SÍ se vio en los cuadros: carteles TRIPLE/QUADRA KILL y ACE (AL), «Red team has slain the Elder Dragon!» (C9 J4), «Barón powerplay» (C9 J5).

## 5. IMÁGENES OFICIALES (API getTeams `karmine-corp`, todas responden 200)
- Logo KC: https://static.lolesports.com/teams/1704714951336_KC.png (y alternativo …1704714951337_KC.png, mismo archivo)
- Canna: https://static.lolesports.com/players/1774651372836_canna.png
- Yike: https://static.lolesports.com/players/1768550195190_Yike-01.png
- kyeahoo: https://static.lolesports.com/players/1774652002153_kyeahoo.png
- Caliste: https://static.lolesports.com/players/1774651348279_caliste.png
- Busio: https://static.lolesports.com/players/1774651329556_busio.png
- (Usar https; con http hay redirección 301.) No hay foto de Reapered en la API.

## 6. DATOS DE COLOR (con fuente)
- Un club que nació de **dos streamers en 2020** y en 6 años llegó al Mundial, con estadios de 28 000 personas para partidos de exhibición. [WP; WPfr]
- **Primer Mundial de su historia** y llegó por la puerta más estrecha: play-in en Los Ángeles, donde perdió 1-20 la primera partida. [WP; API]
- En 2026 **ganó la fase regular del Summer 9-0** y metió a sus 5 jugadores en el 1.er equipo All-Pro… y aun así fue 3.º. [WP 2026 LEC]
- **Le ganó a T1 en París** (semis EWC, 2-1) y al n.º 1 de China dos veces (AG.AL en la EWC, AL en la suiza). [WP EWC; WP Worlds]
- **Canna fue compañero de Faker** en T1 y campeón de Corea como novato (2020). [WP Canna; LP]
- **Caliste**, 20 años, francés: a los 14 jugaba torneos que pedían 16; la LEC subió la edad mínima a 18 justo cuando le tocaba subir y tuvo que esperar un año. [WPfr Caliste]

---

## DUDAS / NO VERIFICADO
1. **Zidane**: ninguna fuente consultada lo vincula a KC. No usarlo sin otra fuente.
2. **Prime**: fechas de salida contradictorias (LP 7-nov-2025, WPfr 9-feb-2026, WP «enero de 2026») y motivo delicado; mejor omitirlo.
3. **«LEC 2025 Winter»**: confirmado (3-0 G2). El «LEC Versus 2026» no es lo mismo (lo ganó G2 3-2).
4. **Subtítulos de los narradores**: bloqueados por YouTube (429); falta el resumen de lo que dicen en cada jugada.
5. **Desfases con 1 solo punto** (LYON inglés, AL español, MVK J3 inglés) y feed ±20 s en MVK J3: comprobar con un cuadro antes de cortar.
6. **Busio, Caliste y Reapered**: Liquipedia renderizado dio 429; trayectoria sacada del wikitexto (fechas, banderas, galería) y de WPfr (Caliste). Nacionalidad de Busio: LP pone Polonia + EE. UU., WP solo EE. UU.; decir «estadounidense de origen polaco» solo si se confirma.
7. **KCX4**: 28 000 (texto WPfr) o 30 000 (tabla WPfr).
8. **Récords de audiencia**: solo verificado el de la final del EU Masters 2021 (377 531 de pico, Esports Charts vía LP). Los de Twitch de Kameto, sin cifra concreta (salvo los 420 000 de r/place).
9. **Clasificación a la ronda 5 / eliminación**: KC 1-2 y CFO 1-2 según LP y WP; si la ronda 5 se juega el 31-oct, el ganador de mañana la juega (2-2).
