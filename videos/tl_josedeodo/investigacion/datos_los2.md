# LOS vs TLAW — G2 (Xin Zhao de Josedeodo) y G1 12:11 (Curse gana el 1 contra 1) — datos verificados
Serie Bo3 ronda 4 suiza, Worlds 2026, 30-oct-2026. G1 gameId 115660540726095078 (VOD español MBwou9RVw4w), G2 115660540726095079 (VOD BhZBuwW3Fhw).
Investigado el 25-nov-2026. Base: `datos_lotl.md` (resultado, picks, relato). Feed `lotl_g<p>_feed.txt`, asistencias `lotl_g<p>_asist.txt`, narración en vivo `lotl_g<p>_narr.txt` (subtítulos automáticos, seg = VOD).
Entre [ ] el nombre real: Ces/CS/Set/Sest/C = Zest, Fy/Face/Fist/Fight/FI = Feisty, Gion/Jon/Gon = Yeon, Kurs/Curs/Kur/Kurt = Curse, Dudu/Duo = Duduhh, Corj/JJ = CoreJJ, Akerman/Hackerman = Ackerman.
**Audio:** los VOD traen doblajes automáticos (inglés, portugués). Las fuentes se cortaron con la pista `format_note*=original` (140-2, es-US original) con `los_cortar.py`. ⚠ `lol_semana2/investigacion/lotl_cortar.py` pedía `140` a secas: comprobar que `lotl_j*.mp4` no salieran con el doblaje.

## Reloj (MEDIDO en cuadros; en la voz va SIEMPRE el HUD)
| Partida | VOD = HUD + | Feed = HUD + | Cuadros que lo fijan |
|---|---|---|---|
| G1 | **430** (confirmado) | +4 | VOD 1121,7 = 11:32 · 1146,7 = 11:57 · 1160,6 = 12:11 DOUBLE KILL |
| G2 | **480** (CONFIRMADO con objetivo) | +3 a +5 | VOD 1181 = 11:41 (dragón a 1 069) · **VOD 1182 = 11:42 «Red team has slain the Hextech Drake!»** (feed 11:47) · VOD 2649 = 36:09 «Red team has slain the Elder Dragon!» (feed 36:14) · VOD 2650 = 36:11 |
El reloj del HUD no es lineal al 100 %: dentro de un mismo clip el desfase se mueve hasta ±0,5 s (ver K de cada fuente). Leer el cuadro antes de dar un segundo exacto en la voz.

### Objetivos G2 con reloj (HUD leído en cuadro donde dice «cuadro»; el resto, feed − 3 a 5, ±2 s)
| HUD | Objetivo | Equipo | Fuente |
|---|---|---|---|
| ~05:57 | Dragón infernal | LOS | feed 06:00 |
| **11:42** | Dragón hextech; Josedeodo junto al dragón (1 069 de vida a 11:41) | TLAW | cuadro VOD 1181-1182 |
| **16:23** | Heraldo de la Grieta («Red team has defeated the Rift Herald!») | TLAW | cuadro los2_j1 t 27,5 |
| **17:38** | «Red team destroyed the first turret!» | TLAW | cuadro los2_j1 t 103 |
| **17:42** | Dragón químico (icono en el marcador a 17:42; banner «Red team has slain the Chemtech Drake!» en cola a 17:45) | TLAW | cuadro los2_j1 t 107-109,5 |
| ~23:36 | Dragón químico (2.º químico) | TLAW | feed 23:40 |
| ~29:09 | Dragón químico = ALMA | TLAW | feed 29:13 |
| ~29:49 | Barón | TLAW | feed 29:53 |
| **35:09-35:10** | «Dragon has spawned!» (Anciano) | — | cuadro los2_j2 t 3,5-4 |
| **36:09** | **Dragón Anciano** («Red team has slain the Elder Dragon!», 2 124 de vida a 36:08) | TLAW | cuadro los2_j2 t 64 |
| ~37:27-37:53 | 3 torres + inhibidor | TLAW | feed 37:31-37:57 |
Retrato del banner de heraldo, hextech y Anciano = el mismo retrato que en «TLAW Josedeodo has slain LOS Feisty!» (Xin Zhao); el de Yeon (Lucian) es otro. ⚠ Lectura de retrato, media-alta: decir «el castigo de Josedeodo» solo si se vuelve a mirar.

### Muertes G2 (feed − 4 = HUD ~, del asist)
07:13 Duduhh (Yeon) · 07:14 CoreJJ (Ackerman) · 07:17 Ackerman (**Josedeodo**) · 07:18 Yeon (Ackerman) · 10:24 Ackerman (Yeon; asiste Josedeodo) · 10:28 **Curse (Josedeodo)** · 16:27 Yeon (Duduhh) · 16:32 **Duduhh (Josedeodo)** · 16:32 Curse (Quid; asiste Josedeodo) · 16:45 **Feisty (Josedeodo)** · 19:14-19:20 triple de Duduhh (Yeon, **Josedeodo**, Morgan) — su ÚNICA muerte · 20:39 Yeon · 23:57 Curse (Quid) y Morgan (Duduhh) · 29:01 Curse (Quid) · **35:41 Curse (CoreJJ)** · **35:48 Feisty (Josedeodo)** · 37:03-37:50 Duduhh, Feisty, Zest, Ackerman.
Curse murió 5 veces en G2 y Josedeodo participa en las 5: la mata a 10:28 y asiste a 16:32, 23:57, 29:01 y 35:41. Josedeodo 5/1/10 = 5 asesinatos (07:17 Ackerman, 10:28 Curse, 16:32 Duduhh, 16:45 Feisty, 35:48 Feisty).
**¿«Su mejor partida»?** De las 7 (stats_*.json): G2 es la de más asesinatos (5), más daño de su equipo en %(23,2 %), kp 100 % y KDA 15. ⚠ La 115660540726095058 (Lee Sin 3/0/8) no tiene muertes: decir «la de más asesinatos y más daño», no «la de mejor KDA» sin matiz. El pick 4 de rojo en segunda ronda del draft: dato del encargo, NO leído aquí (bans/draft sin mirar).

## Las fuentes
1080p, 30 fps, AAC 192 k con narración original en español. HUD = t + K (en la repetición no hay reloj).
| Fuente | Partida | VOD desde | Dur. | K | Repetición |
|---|---|---|---|---|---|
| `medios/_fuente/los2_j1.mp4` | G2 | 1435 | 110 s | **955,8** (t 25 → 16:20, t 49,5 → 16:45; ±0,5) | t 57,7-94,4 (≈ HUD t + 918, por banners) |
| `medios/_fuente/los2_j2.mp4` | G2 | 2585 | 115 s | **2105,8** (t 35,5 → 35:41, t 64 → 36:09; ±0,3) | t 79,9-100,4 (≈ HUD t + 2052, por banners) |
| `medios/_fuente/los1_curse.mp4` | G1 | 1120 | 120 s | **690,5** (t 2 → 11:32, t 40,6 → 12:11; ±0,3) | bot t 63,3-83,5; top t ~84-102 (≈ HUD t + 630) |

## J1 (A, candidata principal) — G2, HUD 16:20-16:45: Josedeodo toma el heraldo y se lleva a Duduhh y a Feisty
Contexto: marcador 2-4, TLAW +1,9 K (16:20). LOS va a pelear el heraldo en el río de arriba con el teleport de Zest.
| t | HUD | Qué se ve | Marcador / oro |
|---|---|---|---|
| 0-24 | 15:55-16:19 | TLAW junta a los 5 en el río de arriba, junto al foso del heraldo | 2-4 |
| 27 | 16:22 | Josedeodo junto al heraldo (1 019 de vida); Curse y Morgan debajo, Duduhh y Ackerman llegando | 2-4 · +1,9 K |
| 27,5 | **16:23** | «Red team has defeated the Rift Herald!» | |
| 30 | 16:25 | Pelea en el foso: Curse encima de Yeon (Yeon con poca vida) | |
| 31-31,5 | **16:27** | Muere Yeon (Duduhh, asisten los 4): 2-4 → **3-4**, TLAW +2,0 K → +1,3 K. «SHUT DOWN!» en t 34,5-36,5 | 3-4 |
| 34 | 16:29 | Feisty AIRBORNE; Josedeodo en el centro; CoreJJ a la derecha | |
| 36-36,5 | **16:32** | Anillo de la definitiva de Xin Zhao alrededor de Josedeodo. Mueren **Duduhh (Josedeodo)** y Curse (Quid): 3-4 → **3-6**, +1,2 K → **+2,3 K** | 3-6 |
| 37-39,5 | 16:32-16:35 | «TLAW Josedeodo is on a killing spree!» | |
| 40-42 | 16:35-16:37 | «TLAW Quid has slain LOS Curse!» (en cola) | |
| 44-49 | 16:39-16:44 | TLAW persigue hacia la jungla de LOS; «Dragon has spawned!» a 16:44 | +2,4 K |
| 49,5-50 | **16:45** | Muere **Feisty (Josedeodo)**: **3-7**, «TLAW Josedeodo is on a rampage!» | 3-7 · +2,4 K → +3,0 K (16:46) |
| 56,4 | 16:52 | Corte a la repetición | |
| 57,7-94,4 | — | REPETICIÓN limpia (sin marcador de jugadores): heraldo a 4 254 de vida con Josedeodo (t 59), SHUT DOWN t 70, **«TLAW Josedeodo has slain LOS Duduhh!» t 76-77** (en directo ese banner no salió: lo tapó la cola), Quid-Curse t 78 | |
| 99,4-110 | 17:35-17:45 | Directo: primera torre (17:38), dragón químico (17:42) | 3-7 · +3,9 K |
Narración en vivo (VOD = t + 1435):
- VOD 1440-1453 (t 5-18): «llega todo el equipo de Team Liquid a la parte central y quieren quedarse con este heraldo… se van a quedar con él».
- VOD 1454-1464 (t 19-29): «Quieren buscar a [CoreJJ], le hacen daño… viene la teleportación por parte de… [Zest]. Quiere ingresar justamente con [Feisty]».
- VOD 1468-1476 (t 33-41): «Ese no tenía que morir. Ahora van a buscar también a Quid… José Deodo. Defensa creciente. Quiere buscar también el doble asesinato. Como lo acaba de hacer José de Odo. José de Odo lo está consiguiendo. Josecito. Dios mío, el de oro».
- VOD 1484-1494 (t 49-59): «Se lleva el asesinato también… José nuevamente demostrando por qué es el mejor jugador de su equipo».
- Repetición VOD 1502-1528 (t 67-93): «atrapan a [Yeon] que es lo más importante, conecta el Galio… José tiene mucho daño, ya tiene una hidra titánica y mira, sin miedo al éxito, se va hacia delante, están muy desgastados, termina llevándose a varios de los jugadores… [Zest] por lo menos sale con vida junto con Akerman, pero [Feisty] termina siendo sacrificado. Tres jugadores por parte de los terminan cayendo».
- VOD 1580-1587 (fuera del clip, HUD ~18:20): «la batalla para el equipo de los volvió a salvar José… 4/0/3 en el marcador» (cuadra con el feed: 4/0/3 a esa hora).
⚠ «doble asesinato» del narrador: el feed da a Josedeodo solo a Duduhh a 16:32; Curse es de Quid. Decir «dos asesinatos en la pelea (Duduhh y Feisty)».

## J2 (A, segunda candidata) — G2, HUD 35:09-36:09: Josedeodo contra Curse y el Anciano
Contexto: 8-9, TLAW con 4 dragones (alma química) y Barón tomado a ~29:49; TLAW +0,4 K a 35:05. El Anciano aparece a 35:09-35:10.
| t | HUD | Qué se ve | Marcador / oro |
|---|---|---|---|
| 3,5-4 | 35:09-35:10 | «Dragon has spawned!»; Anciano a 20 539 de vida, a la izquierda | 8-9 · TLAW +0,4 K |
| 6 | 35:12 | Josedeodo se lanza sobre Zest al sur del río (se ve el impacto); Curse y Ackerman abajo a la derecha | |
| 24-31,5 | 35:30-35:37 | Los 10 alrededor del río de abajo; Feisty arriba a la izquierda junto al pozo | 8-9 |
| 34 | **35:39** | Anillo del **Cataclismo** (definitiva de Jarvan IV) con Josedeodo y Curse DENTRO; Curse con «AIRBORNE» | |
| 35,5-36 | **35:41-35:42** | «TLAW CoreJJ has slain LOS Curse!»; marcador 8-9 → **8-10** a 35:42 | +0,7 K TLAW |
| 42,5-43 | **35:48** | «TLAW Josedeodo has slain LOS Feisty!»; **8-11** a 35:49 | +0,7 K → +1,4 K |
| 63 | 36:08 | Anciano a 2 124 de vida, CoreJJ, Yeon y Morgan encima | |
| 64 | **36:09** | «Red team has slain the Elder Dragon!» | 8-11 · +1,5 K → +2,4 K (36:13) |
| 66-70 | 36:11-36:15 | «ELDER DRAKE» y «True damage over time, 20% health execute» | |
| 79,9-100,4 | — | REPETICIÓN: CoreJJ-Curse t 89-90, Josedeodo-Feisty t 97-98 | |
| 104-115 | 36:49-37:00 | Directo | |
Narración en vivo (VOD = t + 2585):
- VOD 2589-2599 (t 4-14): «José de Odo en contra de [Zest] se avienta… mucho daño en contra de José de Odo también tiene que gastar el destello. No sé si eso fue un gran error por parte del equipo de Team Liquid».
- VOD 2600-2614 (t 15-29): «[Feisty] está esperando, tiene la caída heroica. [Curse] que no se quiere morir rápido, quiere buscar a [Yeon]… Son cuatro dragones para el equipo de Team Liquid».
- VOD 2616-2629 (t 31-44): «Igual se lanza José… Viene también el llamado del dios de la forja… pero [Curse] ya no está disponible… [Feisty]… No tiene destello, no tiene forma de escapar».
- VOD 2638-2649 (t 53-64): «y esto es dragón ancestral para Liquid. Dios mío, no pudieron bajar a nadie… sacando rapidísimo de acción a [Curse] y una vez que cae el junglero, ya no hay nada que hacer».
- Repetición VOD 2658-2686 (t 73-101): «**Ahora sí, Josecito ha superado pero con creces a [Curse]**… el destello lo gasta muy rápido José… porque José está anticipando que van a pelear. Ve cómo termina José entrando bastante bien. Mitiga bastante daño a [Curse]. Lo atrapan dentro de su propio cataclismo… [Zest] no puede entrar tampoco, es un Rumble».
⚠ «Hay dragón ancestral para Team Liquid» (VOD 2629) se dice 20 s ANTES de que caiga (HUD 36:09): no usar esa frase sobre el cuadro del dragón. «La ca de Roca» (VOD 2620): ininteligible. El destello de Josedeodo a t 4-6 lo dice el narrador; en cuadro se ve el lanzamiento, el icono del destello no lo leí.

## B — G1, HUD 11:30-12:11: Curse le gana el 1 contra 1 a Josedeodo (fuente los1_curse, K 690,5)
Contexto: 2-0 a LOS, LOS +1,3 K (11:31). Josedeodo nivel 8, Curse nivel 9 en el 1 contra 1 (barras t 37).
| t | HUD | Qué se ve | Marcador |
|---|---|---|---|
| 0-6 | 11:30-11:36 | Cámara sobre Quid; minimapa: Zest (Jayce) y Morgan en la línea de arriba, el icono de Nocturne (aro rojo) en la jungla de TLAW de arriba | 2-0 |
| 11-27 | 11:41-11:57 | Cámara abajo: pelea de bot. «TLAW Quid has slain LOS Ackerman!» a **11:56** (t 25) | 2-1 |
| 12-26 (minimapa) | 11:42-11:56 | Un icono de LOS (claro, compatible con Trundle) sube por el río de mitad hasta arriba (t 18 en el río central, t 24-26 ya en el río de arriba); el otro icono de LOS (Syndra) se queda en mitad. ⚠ Identidad del icono: media (color del icono + narrador «va llegando… [Curse]») | |
| 28 | 11:58 | Corte a arriba. t 28,5 (11:59): un LOS nivel 10 con «NEARSIGHTED» (definitiva de Nocturne), TLAW nivel 8 «UNSTOPPABLE», TLAW nivel 10 «AIRBORNE» | 2-1 |
| 31 | 12:01 | Los cuatro (Josedeodo, Morgan, Zest, Curse) en el río de arriba, dos LOS con «NEARSIGHTED» | |
| 32,5-33 | **12:03** | «TLAW Josedeodo has slain LOS Zest!» → 2-2 a 12:05 | 2-2 |
| 35,5-36 | **12:06** | «LOS Curse is on a killing spree!» (Curse mata a Morgan; feed: asiste Zest) → 3-2 a 12:07 | 3-2 |
| 37 | 12:07 | 1 contra 1: Curse (nivel 9) pegado a Josedeodo (nivel 8); pilar de Trundle a la izquierda | |
| 39 | 12:09 | Siguen pegados junto al muro del río | |
| 40,3-40,6 | **12:11** | **«DOUBLE KILL!»** de Curse (Morgan + Josedeodo); **4-2** a 12:12 | 4-2 |
| 44-57 | 12:14-12:27 | Directo (Curse sale del río; cámara a cubículos y jungla) | |
| 63,3-83,5 | — | REPETICIÓN del bot (Ackerman) | |
| ~84-102 | — | REPETICIÓN de arriba: Josedeodo-Zest t 95, Curse-Morgan t 96-98, DOUBLE KILL t 101-102. Corte bot → top entre t 83,5 y 84 (camara_clip no lo detectó) | |
| 109,6-120 | 12:40-12:50 | Directo | |
Feed (HUD ~): 12:04 Zest (Josedeodo, asiste Morgan) · 12:06 Morgan (Curse, asiste Zest) · 12:11 Josedeodo (Curse, asiste Zest).
Narración en vivo (VOD = t + 1120):
- VOD 1147-1159 (t 27-39): «en la parte superior va llegando José de Odo va llegando igualmente [Curse] el dos contra dos. Cuánto daño el mordisco por parte de [Curse] se quiere llevar un doble asesinato. Lo va a intentar solamente está José Deudo. Uno contra uno. Se quitan también la camiseta.»
- VOD 1159-1165 (t 39-45): «**José no tiene destello y ñam ñam ñam. Riquísimo… se lleva dos asesinados en la parte superior.**»
- Repetición VOD 1203-1236 (t 83-116): «es una gran iniciación por parte del Nocturne, por parte de José. Está cerca [Curse], es el gran problema. Castigan con todo a [Zest], pero está demasiado fuerte ese Trundle… el Trundle es un gran duelista uno contra uno… en el 1 a 1 el Nocturne no es rival en contra de él. Ya la diferencia es de 1100 entre los junglas.»
⚠ «Cómo lo encuentra»: no hay cuadro de cámara de Curse yendo arriba (la cámara está en bot hasta t 28); solo el minimapa. Lo seguro: fue un 2 contra 2 que INICIÓ Josedeodo (Nearsighted en Zest a 11:59; narrador: «gran iniciación… del Nocturne»), mató a Zest y luego Curse ganó el 1 contra 1. No decir «Curse lo invadió».

## Pies (fracción del cuadro completo; rejilla `z_<fuente>_<t>.jpg` en previews/cuadros; un cuadro)
Pie = bajo la barra, en el cuerpo. Sin coordenada = no identificado o bajo el HUD (y > 0,76).
| Fuente | t | HUD | Pies |
|---|---|---|---|
| los2_j1 | 27 | 16:22 | Josedeodo .33,.37 (media) · heraldo ~.33,.33 · Yeon .42,.35 (media) · Curse .45,.65 · Morgan .36,.58 (media) · Duduhh .58,.70 · Ackerman .55,.70 (duda) · Quid .27,.29 (duda) |
| los2_j1 | 36,5 | 16:32 | Josedeodo .47,.635 (media) · anillo de su definitiva: centro .47,.60, radio ~.12 en x · Morgan .55,.60 (media) · Feisty .30,.48 · CoreJJ .65,.55 · Quid .41,.34 (media) · Ackerman .25,.73 (al límite) · Zest: bajo HUD · Duduhh: muerto, sin coordenada |
| los2_j1 | 49,5 | 16:45 | Josedeodo .61,.31 (media) · Morgan .47,.55 · Ackerman .23,.51 · Feisty: muerto, sin coordenada |
| los2_j2 | 6 | 35:12 | Josedeodo .35,.60 · Zest .28,.68 (media) · Curse y Ackerman juntos ~.53,.72 (media) · Morgan .37,.35 · CoreJJ .47,.36 · Yeon .50,.45 (media) · Quid .56,.36 · Anciano ~.17,.27 · Duduhh: al límite |
| los2_j2 | 34 | 35:39 | Cataclismo: centro .41,.49, radio ~.10 en x · Curse .43,.48 (media, AIRBORNE) · Josedeodo .41,.52 (media) · Yeon .37,.44 (duda) · Morgan .44,.42 (duda) · CoreJJ .43,.30 · Ackerman .57,.60 · Quid .31,.15 (media) · Zest, Duduhh: bajo HUD · Feisty: fuera de cuadro |
| los2_j2 | 43,5 | 35:49 | Josedeodo .49,.33 (media) · Quid .42,.30 (media) · Morgan .49,.42 · CoreJJ .58,.31 · Zest .26,.60 · Duduhh .35,.60 · Ackerman: bajo HUD |
| los1_curse | 31 | 12:01 | Los cuatro dentro de x .46-.57, y .44-.56 (centro ~.51,.51): Josedeodo .47,.54 (duda) · Morgan .55,.47 (duda) · Zest y Curse con NEARSIGHTED, sin pie separable |
| los1_curse | 37 | 12:07 | Curse .45,.44 (duda) · Josedeodo .48,.44 (duda) — pegados · pilar de Trundle .41,.56 |
| los1_curse | 40,6 | 12:11 | Curse .43,.47 (media) · Josedeodo (cayendo) ~.47,.46 (duda) |
Cortes de cámara (`cam_<fuente>.json`): los2_j1 0,4-0,8 · 49,2 · 56,4-57,7 (→ repetición) · 80,2 · 83,0 · 94,4-95,2 (→ jugadores) · 99,2-99,4 (→ directo) · 105,2. los2_j2 21,3-21,9 · 49,3 · 52,1 · 63,7 · 74,6 · 78,6-79,9 (→ repetición) · 100,4-102,1 (→ directo). los1_curse 12,0-12,6 · 19,0 · 27,3-28,1 (bot → arriba) · 44,8 · 56,5 · 62,7-63,3 (→ repetición) · 73,0 · 77,7 · ~83,5-84 (bot → arriba, no detectado) · 90,5 · 108,9-109,6 (→ directo).

## Herramientas (en esta carpeta)
`los_cortar.py` (corte con audio original) · `vod_cuadros.py` (cuadros del VOD sin bajar) · `hud_fuente.py` / `hud_ff.py` (reloj; `_ff` = ffmpeg exacto, cv2 salta hasta 1 s) · `marcador_ff.py` · `banner_ff.py` · `cuadro_fuente.py` · `hoja_fuente.py` · `zoom_fuente.py` (rejilla) · `minimapa.py`.
