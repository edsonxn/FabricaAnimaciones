# CTBC Flying Oyster vs Karmine Corp — PARTIDA 2 (Worlds 2026, fase suiza R4, Bo3 a muerte) — datos verificados
gameId 115660540726095075 · CFO lado AZUL · ganó KC 20-12 en 36:58 de juego (feed). Investigado el 29-oct-2026 (16:20-17:10 CDMX).
Fuentes: feed oficial (caché `feed_115660540726095075.json`; muertes/objetivos con RELOJ DE JUEGO sin pausas en `g2_asist.txt`
— generado por `g2_reloj.py` —; curva por minuto de juego `g2_curva.txt` — `g2_curva.py` —; marcador final por jugador en
`g2_feed.txt`, cuyo reloj es de pared: ignorarlo); **VOD de Twitch LATAM en español** https://www.twitch.tv/videos/2914166111;
`vod_g2_480.mp4` = VOD 5900-10899 s en 480p; narración con Whisper large-v3 (`vod_g2_480_narr.txt`, `g2_narrar.py`; Whisper:
«Jake/Jike/Yaik»=Yike, «Bucio»=Busio, «Kana»=Canna, «Pote/Pout»=POUT, «Dogo/Dobo»=Doggo, «Kiao Hu/Keahu/Yahoo»=kyeahoo,
«Kalista/Kaliste»=Caliste, «Rez»=Rest, «varón»=Barón, «Casey/Carmen Corp»=KC); relojes del HUD leídos a mano en cuadros.
Narradores: Corsario y JJ (se despiden en archivo ≈4990).

## Reloj y desfases (MEDIDOS) — el VOD incluye las pausas: el desfase cambia por tramo
| Tramo (HUD) | archivo `vod_g2_480` | VOD Twitch (≈) | Lecturas (archivo → HUD) |
|---|---|---|---|
| 00:00-17:03 | **HUD + 404** | HUD + 6309 | 500→01:36 · 534→02:10 · 600→03:16 · 900→08:16 · 1200→13:16 |
| 17:03-25:02 | **HUD + 826** | HUD + 6731 | 1966→19:01 · 2026→20:00 («Baron Nashor has spawned!») · 2146→22:00 |
| 25:29-fin | **HUD + 2553,5** | HUD + 8458 | 4174→27:00 · 4307→29:13 · 4534→33:01 · 4700→35:46 · 4711→35:58 · 4763→36:50 |
- VOD Twitch ≈ archivo + 5905 (±3 s: yt-dlp arranca unos segundos tarde y varía por corte; para cortar, pedir `desde` = HUD + 6303 /
  6721 / 8451 y MEDIR K en la fuente).
- **Feed = HUD + 4** (±2; el feed va en ventanas de ~10 s): 1.ª sangre feed 02:15 / HUD 02:11; dragón 05:37/05:33; Busio 09:52/09:48;
  1.ª torre 10:28/10:23-10:24; Doggo→Canna 23:48/23:44; Barón 24:21/24:17; alma 28:00/27:57; ancestral 36:01/35:58.
  En la G1 era +3. Abajo, donde hay cuadro leído manda el cuadro; si no, «≈ feed − 4».
- Pausas en la transmisión: **1.ª** HUD 17:03 (archivo 1427: «17 minutos y… uy, ¿qué pasó acá? Una pausa») → se reanuda archivo
  ≈1851 (7 min). **2.ª** HUD 25:02 (archivo 2328: pantalla en sepia) → vuelve en vivo archivo ≈4080 (≈29 min; el feed registra
  tres tramos: 25:06, 25:22 y 25:29 de juego, 7,8 + 17,3 + 3,7 min).
- Draft: archivo 0-405. Juego desde archivo 404. Parche 26.20 (rótulo del draft). Fin: pantalla «KC VICTORY» archivo ≈4770
  (HUD ≈36:56); feed `finished` 22:12:28Z = juego 36:58.

## POR QUÉ SE PARÓ LA PARTIDA (narración)
- **1.ª pausa (17:03, 7 min):** la pidió CFO («ahí vemos arriba que la pausa viene por CFO y que los oficiales están investigando»,
  1525-1530; Doggo «reclama», 1531-1534). Al volver: «por lo que tenía entendido fue un tema de hardware, nada más, de Doggo»
  (1852-1855); «lo bueno es que no ocurrió en ninguna situación comprometedora tipo una pelea en equipo» (1859-1863).
- **2.ª pausa (25:02, ≈29 min, justo después de la pelea del Barón):** otra vez Doggo. En pantalla: «referees investigating» (2422).
  «Mira, es un bug, es por parte de CFO de nueva cuenta… tiene un bug de no poder comprar un objeto» (2425-2446); «lo que reportaba
  Doggo es que no puede comprar un objeto… después de que murió» (2458-2470). Se reanudó y volvió a pararse: «hubo una pausa, la
  segunda casi consecutiva, porque Doggo no podía comprar o tenía un problema con un objeto… parecía que lo habían solucionado, pero
  nuevamente otra pausa segundos después» (3348-3367). Solución: «un problema de hardware con Doggo… estos continuos fallos… están
  cambiando el tema de la PC» (3474-3488); «recuerden que es una pausa técnica, particularmente en las manos de Doggo» (3575-3579).
  Los narradores hablan del Chronobreak (volver al instante previo a un bug) pero NO se usó: se siguió desde la pausa.

## Alineaciones, campeones y draft
| Pos. | CFO (azul) | KC (rojo) |
|---|---|---|
| Top | Rest — Ambessa (última elección de CFO) | Canna — Camille (última de KC, «responde agresivo… daño puro y duro», 341-348) |
| Jungla | Shad0w — **Lee Sin** (1.ª elección de CFO, 30-50) | Yike — Pantheon («para contrarrestar un poco a Lee Sin», 137-143) |
| Mid | POUT — Ryze (mostraron Hwei antes: «me gustaba más el Ryze que el Hwei», 292-305) | kyeahoo — Viktor (262-275) |
| ADC | Doggo — Caitlyn | Caliste — Yunara |
| Support | Kino — Karma | Busio — Lulu (KC aseguró Lulu + Yunara de inmediato, 62-85) |
- Lectura del draft (113-136): «Yunara, sobre todo al comienzo, tiene poco rango… entre el poke de Karma y el de Caitlyn no la va a
  pasar, o no debería pasar muy bien» → **se cumplió**: 1.ª sangre a Caliste (02:11) y dos niveles abajo a los 11 min (1150-1163).
  Sobre Ambessa (324-341): «una Ambessa que se fidee puede ser un dolor de cabeza» → **no se cumplió** (Rest 1/5/2).
  Ryze: «Casey lo dejó pasar y está teniendo el impacto» (1048-1056).
- Bans: en el cuadro (archivo 330-385) se ven 5 por equipo + «SERIES BAN» (los de la G1 por el Fearless), pero a 480p no se
  identifican con seguridad. Narración: CFO banea Jayce al final («del otro lado es Jayce, es lo que bloquea CFO», 50-60); KC banea
  Akali («la Kali ya termina siendo bloqueada por parte de KC», 165-172) y otro asesino («Locke», sin identificar, 203). Ver «Dudas».

## Marcador final (feed)
| | CFO | KC |
|---|---|---|
| Asesinatos | **12** | **20** |
| Oro | 67 954 | 75 038 (**+7 084** KC) |
| Torres | 7 | 7 |
| Inhibidores | 1 (HUD ≈29:07) | 1 (HUD ≈36:34) |
| Barones | 1 (HUD 24:17) | 1 (HUD ≈30:56) |
| Dragones | 4: Hextech (05:33), Océano (≈17:15), Océano (≈22:34), Océano (27:57) = **alma del océano** | 2: Nube (≈11:55), **Ancestral (35:58)** |
K/D/A (feed): Rest 1/5/2 · Shad0w 5/3/4 · POUT 3/3/3 · **Doggo 2/6/7 (40 % del daño de CFO, cs 372)** · Kino 1/3/9 — Canna 5/3/4 ·
Yike 4/2/12 · **kyeahoo 6/0/11 (31 % del daño de KC; 0 muertes)** · Caliste 4/4/12 (cs 388, 19.2K oro) · Busio 1/3/17.

## Curva de oro (CFO − KC, feed por MINUTO DE JUEGO; HUD ≈ feed − 4) — `g2_curva.txt`
| min | dif | kills | nota |
|---|---|---|---|
| 2 | −131 | 0-0 | KC arriba antes de la 1.ª sangre |
| 3 | +569 | 1-0 | 1.ª sangre Doggo a Caliste (02:11) |
| 6 | +635 | 1-0 | dragón Hextech CFO (05:33) |
| 7 | +1 287 | 3-1 | pelea de la línea inferior 2 por 1 (06:08-06:24) |
| 10 | +1 880 | 4-1 | Shad0w a Busio (09:48) |
| 11 | +3 066 | 4-1 | 1.ª torre CFO (10:23) |
| 13 | +3 355 | 4-1 | 2.ª torre (≈12:19); KC toma el dragón de Nube (≈11:55) |
| 16 | +3 209 | 4-2 | Canna mata a Rest (≈15:04); 3.ª torre (≈15:21) |
| 17 | +4 278 | 4-2 | 4.ª torre con el Heraldo (≈16:44) · PAUSA 17:03 |
| 18 | +4 416 | 4-2 | 2.º dragón (Océano) CFO |
| 19 | +3 995 | 4-2 | 1.ª torre de KC (≈18:10) |
| 20 | **+4 795** | 4-2 | **máximo de CFO** (feed 19:59; HUD 19:47 +4.5K) |
| 21 | +2 155 | 4-6 | pelea 4 por 0 de KC junto al Barón (20:04-20:44) |
| 23 | +2 062 | 4-6 | 3.er dragón (Océano) CFO |
| 24 | +2 977 | 5-6 | Doggo a Canna (23:44) |
| 25 | +2 310 | 8-10 | Barón CFO (24:17) + pelea 4 por 4 (24:20-24:53) · PAUSA 25:02 (≈29 min) |
| 27 | +1 679 | 8-10 | 2.ª torre de KC (≈26:41) |
| 28 | +1 497 | 8-10 | **alma del océano** (27:57) |
| 29 | +3 039 | 9-10 | torre (28:18) + POUT a Canna (28:34) |
| 30 | +2 935 | 9-10 | inhibidor CFO (≈29:07; HUD 29:13 = +3.7K) |
| 31 | +1 536 | 10-13 | pelea 3 por 1 de KC (30:20-30:22) |
| 32 | +289 | 10-13 | Barón KC (≈30:56); 7.ª torre de CFO (≈31:54) |
| 33 | **−143** | 10-13 | **KC arriba por primera vez desde el min 2** (cruce feed 32:53 ≈ HUD 32:49; un instante −4 en 31:38) |
| 34 | −236 | 10-13 | sale el dragón ANCESTRAL (HUD 33:55-33:56, «Dragon has spawned!», archivo 4589) |
| 35 | −146 | 11-14 | cambio 1 por 1 (34:06-34:07) |
| 36 | −2 554 | 11-17 | pelea del ancestral 5 por 1 (35:32-35:59) |
| fin | **−7 084** | 12-20 | inhibidor y torres 36:18-36:46, nexo ≈36:56 |
CFO estuvo arriba de forma continua del minuto 3 al 32.

## LAS JUGADAS (reloj HUD; «t» = segundo de la fuente `medios/_fuente/g2_j*.mp4`; «archivo» = vod_g2_480)
### J6 · 02:11-16:44 — El arranque de CFO: la línea inferior, el 2 por 1 y cuatro torres — fuentes `g2_j1`, `g2_j2`, `g2_j3`
- **02:11 1.ª sangre: Doggo (Caitlyn) mata a Caliste (Yunara)**, asiste Kino (cartel «FIRST BLOOD» archivo 534,5 / `g2_j1` t 24).
  Antes, Caliste y Busio aguantaron un primer choque gastando Barrera y Curación (489-520). Narración: «Lo hace muy bien, lo lee
  perfecto, se suelta hacia adelante… disparo en la cabeza y ¡zas! Se lleva la primera sangre CFO» (534-542); «Doggo es muy bueno
  con esta selección; lo que quieren hacer es estompear al máximo este carril inferior» (542-552). Repetición en la transmisión
  `g2_j1` t ≈ 67-85 («con el destello… y simplemente el crítico que le da gracias a la ralentización», 583-593).
- **05:33 dragón Hextech CFO** (mensaje «Blue team has slain the Hextech Drake!», archivo 737; Shad0w en el foso; `g2_j2` t 16):
  «aprovechan que el carril inferior tiene completo dominio, y eso complica demasiado que pueda llegar Yike» (734-744).
- **06:08 Busio (Lulu) mata a Doggo** (asisten Yike y Caliste; mensaje archivo 772, t 51) · **06:14 Shad0w (Lee Sin) mata a Busio**
  (asisten Doggo y Kino; archivo 778, t 57) · **06:24 POUT (Ryze) mata a Yike** (asisten Shad0w y Kino; archivo 788, t 67).
  Marcador de asesinatos 3-1. Narración: «Se paga con sangre [Doggo], debió haber estado más encima» (774-776); «venía Shad0w, viene
  POUT, que utiliza la definitiva, y ya con esto cierran completamente que pueda retroceder KC… termina siendo un dos por uno, nada
  favorable para ellos» (813-826); «Yike sabe que no fue la mejor jugada del mundo» (832-834). ERROR de KC: «la W [campo gravitatorio
  de Viktor] que puso ahí, paupérrima, en el borde; con suerte agarró a POUT, podría haber agarrado a los cuatro» (838-849) — «no hubo
  comunicación entre ellos» (852-854). Repetición en la transmisión `g2_j2` t ≈ 80-110 (sin HUD en t 100).
- **09:48 Shad0w mata a Busio** (asisten POUT y Doggo; mensaje archivo 992; `g2_j3` t 20): «no tiene ulti, explota de inmediato; lo
  siguen insistiendo en el carril inferior» (991-994); «deben castigarlo en otro lado» (994-1002).
- **Torres de CFO sin perder ninguna:** 10:23 la primera («Blue team destroyed the first turret!», archivo 1027, `g2_j3` t 55),
  ≈12:19, ≈15:21 y ≈16:44 (la 4.ª con el Heraldo: «le pega directo a la torreta cerca del inhibidor», 1417-1425). KC no toma su
  primera torre hasta ≈18:10. Diagnóstico de los narradores a los 10-11 min: «carril inferior totalmente superado… carril central,
  mucha ventaja de POUT con ese Ryze… en las junglas, mucho mejor Shad0w con Lee Sin… carril superior es el único lugar donde Canna
  está sacando la casta por el equipo» (1033-1064); «dos niveles completos de ventaja de Doggo contra Caliste» (1150-1163).
- Cuadros para pausa: `g2_j1` t 22 (02:09, Doggo y Kino contra Caliste y Busio en la línea inferior, un segundo antes del disparo);
  `g2_j2` t 49 (06:06, KC salta sobre Doggo junto a la torre inferior) y t 59 (06:16, Shad0w, POUT y Kino persiguen a Yike por el río).

### J7 · 19:56-20:44 — La pelea junto al Barón: 4 por 0 de KC — fuente `g2_j4` (K 1182) ★ candidata a 3D
- Antes: HUD 19:47 CFO +4.5K (t 5), 4-2. **El Barón aparece a las 20:00** («Baron Nashor has spawned!», t 18): la pelea es en el
  RÍO SUPERIOR, a la entrada del foso del Barón. Minimapa (t 2-14): los dos equipos amontonados alrededor del foso; un campeón de KC
  (icono rojo, pelo blanco = Camille) sube SOLO por el río desde el medio y entra por debajo a t 14.
- Quién inicia: **Busio se lanza de frente y CFO lo estaba esperando** («cuidado Busio, que se lanzaba de frente y lo estaban
  esperando», 2021-2024); **Canna aparece por la retaguardia** («opa Canna, cuidado, que aparecía por la retaguardia; Doggo con todo
  en contra de Canna», 2024-2030).
- **20:04 Canna (Camille) mata a Doggo** (asisten Yike, kyeahoo, Busio; mensaje t 22 / archivo 2030) · **20:10 Yike (Pantheon) mata a
  Rest** (asisten los 4; t 28) · **20:14 Canna mata a Kino** (doble asesinato, «DOUBLE KILL» t 32) · KC golpea el Barón (t 40-66;
  «le queda 4 mil de vida al Barón», 2064) con Shad0w y POUT afuera · **20:44 Yike mata a POUT** (cartel «SHUT DOWN», t 62).
  **KC NO se lleva el Barón**: lo suelta y se va (t 66-70; el feed no da Barón a nadie hasta el de CFO a las 24:17).
- Oro: +4.5K (19:47) → +2.9K (20:22, t 40) → +2.2K (20:57, t 75). Feed: +4 795 (19:59) → +2 955 (20:49) → +2 155 (21:00).
- Narración: «acaba de caer la sheriff de Piltover y parece que cae con eso toda la escuadra de CFO… además al lado del Barón, tres
  fuerzas han explotado en CFO» (2036-2046); «es cierto que no se lleva un Barón, pero le resulta la jugada a KC; ya lo habíamos
  adelantado, la gran esperanza era Canna» (2076-2084). Repetición en la transmisión **t 82-110** (archivo 2090-2118): «en ningún
  momento se da cuenta CFO de que allá aparece Canna; va directamente por Doggo; la Camille es el campeón perfecto para atrapar a
  alguien; la Caitlyn no puede hacer nada» (2094-2107). Después: «tenías un trabajo, no te pido que ganes la línea, solo que no se
  nos desbande la Camille» (2142-2152); «todos los jugadores de CFO tenían bounty [recompensa]… cuando empezaron a morir soltaron una
  cantidad de oro descomunal» (2179-2192).
- **Cuadros recomendados para la pausa:** **t 15** (19:57: Busio adelantado en el río superior, CFO agrupado esperándolo junto al
  foso, Camille llegando sola desde el río medio — ver minimapa t 12-14) · **t 21** (20:03: la definitiva de Camille sobre Doggo a la
  entrada del foso) · t 60 (20:42: KC dentro del foso pegándole al Barón, Shad0w y POUT afuera).
- Para el 3D: posiciones medibles en el minimapa de t 2-22 (el recorte del minimapa en 1080p queda a la derecha abajo; la parte de
  arriba del mapa se ve cortada en la esquina, medir con cuidado).

### J8 · 23:44-25:02 — El Barón de CFO, la pelea 4 por 4 y la pausa — fuente `g2_j5` (K 1412)
- Antes: KC se tiró sobre POUT: «cuatro se le cierran encima… casi cae… pero estaban todo el resto de jugadores de CFO y terminan
  aguantando» (2240-2260). **23:44 Doggo mata a Canna** (asisten Shad0w, POUT, Kino; mensaje t 12 / archivo 2250).
- «Van por el Barón» (2263): **24:17 Barón CFO** («Blue team has slain Baron Nashor!», t 45 / archivo 2283).
- Pelea a la salida del foso, ya con el Barón tomado: **24:20 POUT mata a Yike** (t 48) · ≈24:23 Shad0w a Busio · ≈24:23 kyeahoo a
  Doggo · ≈24:25 Caliste a POUT · ≈24:28 kyeahoo a Rest · ≈24:46 Shad0w a Caliste · **≈24:53 Canna mata a Shad0w** (t ≈ 81; horas
  ≈ = feed − 4). 7 muertes en 33 s; con Canna, 4 por lado. Narración: «Caliste, Caliste… adelante con destello, se lleva uno, se lleva
  dos… Caliste sale en persecución, Shad0w corre por su vida, y cuando cae esa Caitlyn se desmorona completamente todo CFO» (2287-2305);
  «Shad0w media vuelta, se confía… igual Canna sentencia la kill» (2313-2326).
- **25:02 pausa** (pantalla en sepia desde `g2_j5` t ≈ 90; la fuente termina en t 98 dentro de la pausa, sin cruzarla).
- Cuadros: t 44 (24:16, el Barón a punto de caer con los diez alrededor del foso) · t 57 (24:29, kyeahoo y Caliste rematando junto al
  foso, «DOUBLE KILL» archivo 2295).

### J9 · 27:57-31:00 — Alma, inhibidor… y la pelea 3 por 1 que la voltea — fuentes `g2_j6` (K 1659) y `g2_j7` (K 1799)
- **27:57 alma del océano CFO** (4.º dragón de CFO; cartel «Dragon Soul», archivo 4231, `g2_j6` t 18). KC estaba tirando una torre:
  «podría cambiar Barón por dragón… finalmente se van a quedar con este objetivo» (4220-4228). **28:18 torre CFO** («Red turret
  destroyed», t 39). **28:34 POUT mata a Canna** (asiste Shad0w; t 55): «se le complica el escape a Canna, no tiene destello… se confía
  demasiado, cree que tenía el daño suficiente y no es así» (4260-4271); repetición (4320-4356): «entró con destello Canna, un all-in en
  contra de Doggo, pero lo logran quitar… POUT no ve que detrás está Shad0w… venía en camino Yike, pero no cuenta».
- **≈29:07 Shad0w destruye un inhibidor de KC** («CFO Shad0w has destroyed a red inhibitor!», visible en t 94-95 = HUD 29:13; el
  contador de reaparición marca 4:52 a las 29:13 y «A red inhibitor has respawned!» sale a las 34:08-34:09 → destruido ≈29:06-29:09).
  HUD 29:13: **CFO +3.7K, 9-10, 6 torres a 2, alma**. «Ya están en la torre de inhibidor del carril inferior… no pueden defenderlo»
  (4283-4300). OJO: el Barón de CFO (24:17) ya había expirado (dura 3 min → 27:17).
- **30:17 reaparece el Barón** («Baron Nashor has spawned!», archivo 4370 / `g2_j7` t 18). **30:20 Rest mata a Caliste** (asisten
  Doggo, Kino; mensaje t 21) → **30:20-30:22 kyeahoo mata a Doggo, Yike a Kino, kyeahoo a Rest** (feed 30:24/30:25/30:26; «killing
  spree» t 23, «DOUBLE KILL» t 25). Quién inicia: **Caliste** («se enoja Caliste, con todo se lanza hacia adelante… se hace invulnerable
  en el último segundo… aparece Yike, se lleva el asesinato, son uno, podría ser ahora dos, y ahí viene el tercero», 4368-4381; en la
  repetición: «esa gran iniciación por parte de Caliste, no le estaban esperando; queda muy bajo pero hace su trabajo; Doggo gasta el
  guardabrazos y van hacia adelante», 4410-4418). «Ahora son ellos los que van a buscar ese Barón… Shad0w ni siquiera se acerca, van a
  ceder completamente este Barón» (4398-4403).
- **≈30:56 Barón KC** (feed 31:00): ocurre mientras la transmisión pasa la repetición de la pelea (`g2_j7` t 51-68, con el foso en
  ventana); vuelve en vivo con «BARON POWER PLAY» en t 70. «Ya con esto está a 1 400 [la ventaja de CFO]… el plan no ha salido» (4433-4440).
- Cuadros: `g2_j6` t 17 (27:56, CFO en el foso del dragón con el alma) · `g2_j6` t 50 (28:29, sin ver en cuadro: Canna entra con destello sobre Doggo en
  medio) · `g2_j7` t 19 (30:18, Caliste se lanza; los diez en el río junto al Barón recién aparecido) · `g2_j7` t 23 (30:22, kyeahoo
  rematando con la tormenta del Viktor).

### J10 · 34:06-36:56 — El dragón ANCESTRAL y el cierre — fuente `g2_j8` (K 2041) ★ candidata a 3D
- **El ancestral sale a las 33:55-33:56** («Dragon has spawned!», archivo 4589; 6 min después del alma). KC va arriba en oro desde
  ≈32:49 (HUD 33:01: 62.3K-62.4K; 34:07: 64.3K-64.4K, casi empatados).
- **34:06-34:07 Shad0w mata a Caliste** (asisten Doggo, Kino) **y Canna mata a Doggo** (asisten Yike, Caliste, Busio) (t 5-6): «cuidado
  que se viene la jugada aquí por la retaguardia… han caído ambos ADC» (4595-4610).
- ≈34:55: «pero mira Canna, se lanza, desorienta a tres, espectacular la entrada, pero nadie lo secunda… se resetea el dragón» (4652-4659,
  `g2_j8` t ≈ 55; sin verificar en cuadro).
- **35:32 Yike mata a Shad0w** (asisten kyeahoo, Busio; «SHUT DOWN» t 91): Shad0w va solo al río del ancestral (t 84, 35:25) y KC lo
  espera escondido. «KC sabe que ahí está Shad0w… por un sentinela; le terminó costando la vida; cayó en la trampa más vieja» (4680-4690);
  «al morir el jungla, el dragón queda más o menos expuesto» (4696-4700); «un sentinela básico es lo que lo revela… van por él, eliminan
  al junglero, y con eso parece que la partida podría estar sentenciada» (4724-4741); «cómo duele, Shad0w, en esa toma de decisiones de
  ir él, siendo el jungla» (4745-4750).
- **35:53-35:54 Caliste mata a Rest** (mensaje t 112-113) · **≈35:55 Caliste mata a POUT** («DOUBLE KILL» t 114,8) · ≈35:56 Kino mata a
  Canna (feed 36:00) · **35:57-35:58 ancestral KC** (cartel «ELDER DRAKE» t 116, «Red team has slain the Elder Dragon!» t 117) · ≈35:57
  kyeahoo mata a Doggo · ≈35:59 Caliste mata a Kino (feed 36:03; «TRIPLE KILL» y «ACE» en pantalla t 121-123). Narración: «Canna viene
  por la retaguardia, aparece de la nada, salta en contra de Doggo y no puede escapar… falta uno más que llegue y pueda secundar…
  efectivamente lo consigue, se lleva el dragón KC y da vuelta completamente esta partida» (4701-4715).
- **¿Quién remató el ancestral? SIN VERIFICAR.** El feed no lo registra, el cartel no lo nombra y la narración dice solo «se lleva el
  dragón KC». En t 115,6-116,4 junto al dragón están Busio (nivel 15, rotulado) y un jugador de KC nivel 17 sin rótulo (probablemente
  Yike: único jungla vivo, con Castigo; Shad0w llevaba 25 s muerto) — no se ve el golpe final.
- Cierre (feed − 4 salvo cuadro): torres ≈36:18 y ≈36:30; **inhibidor 36:34** («KC Caliste has destroyed a blue inhibitor», t 154);
  kyeahoo mata a Shad0w ≈36:39; torres ≈36:43 y ≈36:46; t 137-142 la transmisión muestra el gráfico «Win Expectancy» (de CFO casi toda
  la partida a KC al final); en t 169 (HUD 36:50) pasa a la cámara del escenario con el juego en ventana; «KC VICTORY» ≈ t 175.
- Narración final: «sella su pase al grupo del 2-2» (4771-4774); «**y oficialmente, Corsario, la LCP está fuera de Worlds 2026**»
  (4777-4783); «un 2 a 0 que podría haber sido 2 a 1 fácilmente, por cómo se estaba dando el comienzo» (4878-4882); «ninguno de los
  equipos de la LCP llegó al 2-2… Team Secret se va sin victorias, las Ostras se van 1-3» (4923-4934); «Rest va a tener pesadillas
  esta noche con esa Camille» (4820-4825); «una desconexión, o distraerte un poco, puede costarte una partida y la serie; eso le pasa a
  CFO, que hizo lo que tenía que hacer los primeros 20 minutos» (4848-4865); clave para el analista: «tenían muy claro que al que tenían
  que apagar era primeramente a Doggo» (4994-4999).
- **Cuadros recomendados para la pausa:** **t 84** (35:25: Shad0w solo en el río inferior junto al foso del ancestral; KC fuera de
  vista) · t 88 (35:29: KC le cae encima) · **t 108** (35:49: los diez alrededor del foso del ancestral) · t 116
  (35:57: el ancestral a punto de caer, Busio y un KC nivel 17 encima).

### ★ La mejor candidata a 3D: **J7 (19:56-20:44)**
Es LA pelea de mitad de partida: CFO, con +4,8K y el Barón recién aparecido, espera a Busio y no ve venir a Camille por el río medio;
tiene el «mientras» que el 3D explica (foso del Barón, río superior, flanco de Canna, la Caitlyn sin escape) y la repetición de la
transmisión (t 82-110) confirma el recorrido. Alternativa: **J10** (Shad0w pillado por el centinela y la pelea del ancestral), que tiene
la ventaja de decidir la serie pero el golpe final del dragón no se ve.

## Fuentes cortadas (`medios/_fuente/`, 1080p30 + audio, VOD Twitch) — HUD = t + K (medido en ≥ 2 cuadros por fuente; constante)
| Archivo | desde (s VOD) | dur | K (s) | HUD inicio → fin | Contenido |
|---|---|---|---|---|---|
| g2_j1.mp4 | 6412 | 95 | 107 | 01:47 → 03:22 | 1.ª sangre t 24 (02:11); repetición t ≈ 67-85 |
| g2_j2.mp4 | 6618 | 110 | 317 | 05:17 → 07:07 | dragón Hextech t 16; Busio→Doggo t 51; Shad0w→Busio t 57; POUT→Yike t 67; repetición t ≈ 80-110 |
| g2_j3.mp4 | 6872 | 75 | 568 | 09:28 → 10:43 | Shad0w→Busio t 20; 1.ª torre CFO t 55 |
| g2_j4.mp4 | 7905 | 120 | 1182 | 19:42 → 21:42 | Barón aparece t 18; Canna→Doggo t 22; Yike→Rest t 28; Canna→Kino t 32; KC al Barón t 40-66; Yike→POUT t 62; repetición t 82-110 |
| g2_j5.mp4 | 8130 | 98 | 1412 | 23:32 → 25:02 | Doggo→Canna t 12; Barón CFO t 45; pelea 4 por 4 t 48-81; pausa (sepia) desde t ≈ 90 |
| g2_j6.mp4 | 10112 | 100 | 1659 | 27:39 → 29:19 | alma t 18; torre t 39; POUT→Canna t 55; inhibidor ≈ t 88 (mensaje t 94) |
| g2_j7.mp4 | 10250 | 90 | 1799 | 29:59 → 31:29 | t 0-12 repetición (POUT→Canna); Barón aparece t 18; pelea 3 por 1 t 21-24; KC al Barón t 39-48; repetición t 51-68 (Barón KC ≈ t 57 en ventana); en vivo t 70 |
| g2_j8.mp4 | 10490 | 185 | 2041 | 34:01 → (36:50 en t 169) | cambio 1 por 1 t 5-6; Yike→Shad0w t 91; Caliste→Rest/POUT t 112-115; ancestral t 116-117; ace t ≈ 121; inhibidor t 154; escenario desde t 169; victoria ≈ t 175 |
K = desde − 6301…6305 (tramo 1), − 6718…6723 (tramo 2), − 8449…8453 (tramo 3): el arranque de yt-dlp varía ±3 s, por eso se midió
cada una. Lecturas: j1 t5 01:52, t40 02:27, t60 02:47 · j2 t5 05:22, t50 06:08 (K 317-318) · j3 t5 09:33, t40 10:08, t70 10:38 ·
j4 t5 19:47, t40 20:22, t75 20:57 · j5 t5 23:37, t50 24:22, t90 25:01 · j6 t5 27:45 (K 1660), t50 28:29, t95 29:14 · j7 t30 30:29,
t85 31:24 · j8 t0,5 34:02, t60 35:01, t150 36:31, t165 36:46. Ninguna cruza una pausa (j5 acaba dentro de la 2.ª, antes de reanudar).
Archivo `vod_g2_480` → t: j1 = archivo − 511; j2 − 721; j3 − 972; j4 − 2008; j5 − 2238; j6 − 4212,5; j7 − 4352,5; j8 − 4594,5.

## Correcciones al guion (escenas draft2 … curva2 de `guion.py`)
1. **draft2** · «Shad0w toma Lee Sin, el campeón favorito de Yike» → SIN RESPALDO en esta partida: la narración solo dice que el
   Pantheon de Yike era «para contrarrestar un poco a Lee Sin»; lo de «favorito» viene de la previa (datos_g1: «Yike — Wukong, NO Lee
   Sin: lo guarda»). Versión segura: «Shad0w abre el draft con Lee Sin, el campeón que Yike se estaba guardando».
2. **jugada6** · «Tres a uno para CFO, y con el primer dragón» → correcto como marcador (3-1), pero la pelea fue **2 por 1** (Busio mató
   a Doggo; Shad0w a Busio; POUT a Yike), como dicen los narradores. Si se dice «tres a uno», que quede claro que es el marcador.
3. **jugada7** · falta (no es error) lo esencial del contexto: la pelea es **junto al foso del Barón justo cuando aparece (20:00)**,
   Busio se adelanta y Canna entra **por la retaguardia** desde el río medio. Tras el 4 por 0, **KC empieza el Barón y lo suelta** (no se lo
   lleva). «Siete segundos después» (20:04 → 20:10 en cuadro = 6 s; feed 7 s): vale.
4. **jugada7_rep** · «en cuarenta segundos devolvió la mitad» → en 40 s (20:04-20:44) cae de +4,8K a +2,9K (−38 %); la mitad se alcanza
   al minuto 21 (+2,2K en HUD 20:57; +2 155 feed 21:00). Versión: «y en menos de un minuto devolvió la mitad». «Exactamente lo que le
   pasó a Karmine contra LYON»: no se puede verificar con estos datos (ver Dudas).
5. **jugada8** · «Pausa. Karmine no se rinde y pelea el Barón» → el Barón **ya era de CFO (24:17)**: KC pelea **a la salida del foso**,
   3 s después (POUT mata a Yike a las 24:20). Versión: «Karmine no se rinde y los espera a la salida del foso». Y «casi media hora de
   pausa» es correcto (≈29 min), pero falta el porqué: **problemas técnicos de Doggo** (no podía comprar un objeto; luego hardware y
   cambio de PC). En la 1.ª pausa (17:03, 7 min) también fue Doggo (hardware).
6. **jugada9** · «Con alma y con Barón» → el Barón de CFO había **expirado a las 27:17**; a las 29:11 CFO tenía alma, inhibidor y +3,7K,
   pero no la mejora del Barón. Versión: «Con el alma, un inhibidor y casi cuatro mil arriba». · «Rest mata a Caliste… pero dos segundos
   después la pelea se le voltea» → correcto; falta que **la inicia Caliste** (y que el Barón acababa de reaparecer, 30:17).
7. **jugada10** · «Minuto treinta y cinco. Por primera vez desde el minuto dos, Karmine va arriba en oro» → KC pasa arriba en el
   **minuto 33** (≈32:49; HUD 33:01 = +0,1K KC); en el 35 va +1,3K (HUD 35:41). Versión: «Minuto treinta y tres: por primera vez desde
   el minuto dos, Karmine va arriba en oro». · «Y aparece el dragón ancestral» → apareció a las **33:55-33:56** y ya se peleaba antes del
   35 (Canna «desorienta a tres… se resetea el dragón»). Versión: «Y el dragón ancestral ya está en el mapa». · «Antes de que el dragón
   sea de nadie, Karmine encuentra a Shad0w» → correcto; el detalle verificable: lo delata un centinela («cayó en la trampa más vieja»).
   · «Caliste remata a Rest y a POUT en un segundo» → en cuadro 35:53-35:55 (1-2 s; feed 35:58/35:59): aceptable, mejor «en dos
   segundos». · Orden real de las muertes según el feed: Caliste→Rest, Caliste→POUT, Kino→Canna, ancestral, kyeahoo→Doggo, Caliste→Kino:
   el guion lo respeta.
8. **jugada10_rep** · «CFO llegó a ir casi cinco mil arriba, tuvo el Barón, el alma y un inhibidor. Y perdió la partida en tres peleas»
   → correcto (máx. +4 795; las tres peleas: 20:04-20:44, 30:20-30:22, 35:32-35:59).
9. **curva2** · «casi cuatro mil con el alma» → con el alma (27:57) iba **+1,5K**; los +3,7K son a las 29:13, tras la torre y el
   inhibidor. Versión: «casi cuatro mil tras el alma y el inhibidor». · «desde el minuto treinta, todo de Karmine» → el oro no cambia de
   lado hasta el **33**; versión: «y desde la pelea del minuto treinta, todo de Karmine». · «Siete mil abajo al final» → correcto
   (−7 084).
Correctas sin cambios: draft2 (alineaciones, lado azul); jugada6 (1.ª sangre 02:11 Doggo a Caliste con Kino; dragón Hextech; Busio a
Doggo, Shad0w a Busio, POUT a Yike; Shad0w a Busio min 9; 4 torres sin perder ninguna; ~5K en el min 20); jugada7 (Canna a Doggo
primero; Yike a Rest; Canna a Kino; Yike a POUT ~30 s después; 4 por 0; de casi 5K a menos de 3K); jugada8 (tres dragones; Doggo a
Canna; Barón CFO; 7 muertes en 33-34 s; 4 por lado); jugada9 (alma 28:00; POUT a Canna; inhibidor; +3,7K; 3 por 1; Barón KC 34 s
después; oro empatado un minuto más tarde: −4 a las 31:38, +72 a las 31:58); jugada10 (Yike a Shad0w; 4 contra 5; Caliste a Rest y POUT;
Kino a Canna; ancestral KC; kyeahoo a Doggo; Caliste a Kino; 5 por 1; nexo).
Fuera de las escenas pedidas (por si sirve): «predicciones» · «Yike… respondió con Pantheon y doce asistencias» ✔ (4/2/12).
«boleta_kc» · «kyeahoo… cero muertes en la segunda partida» ✔ (6/0/11).

## Dudas / sin verificar
- **Quién remató el ancestral** (ver J10): no se ve; probablemente Yike, sin prueba.
- Bans de la G2 (solo Jayce de CFO y Akali de KC por narración; «Locke» sin identificar; Orianna y Renekton mencionados sin quedar claro
  quién los quitó). Para leerlos, cortar el draft en 1080p (VOD ≈ 6230-6300).
- Horas marcadas «≈» = feed − 4 (±2 s), sin cuadro propio: 2.ª-4.ª torre de CFO, dragones de Océano 2 y 3, dragón de Nube de KC, torres
  de KC, muertes intermedias de la pelea 24:20-24:53 y Kino→Canna / kyeahoo→Doggo / Caliste→Kino en el ancestral (los mensajes en
  pantalla salen en cola y con retraso).
- Carril de la 1.ª torre de CFO (10:23): sin confirmar (la narración menciona presión en el carril superior justo antes).
- Lo que hace Canna a las ≈34:55 («desorienta a tres… se resetea el dragón»): solo narración.
- «Exactamente lo que le pasó a Karmine contra LYON» (jugada7_rep): no está en estas fuentes.
- La previa decía que si ganaba KC mandaba «a casa a toda la LCP» (duda de datos_g1): **la narración lo confirma** («oficialmente, la LCP
  está fuera de Worlds 2026», archivo 4777-4783; «ninguno de los equipos de la LCP llegó al 2-2… las Ostras se van 1-3», 4923-4934).
