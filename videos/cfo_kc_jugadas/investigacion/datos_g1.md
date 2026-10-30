# CTBC Flying Oyster vs Karmine Corp — PARTIDA 1 (Worlds 2026, fase suiza R4, Bo3 a muerte) — datos verificados
gameId 115660540726095074 · KC lado AZUL · ganó KC 19-3 en 27:39. Investigado el 29-oct-2026 (15:00-15:50 CDMX).
Fuentes: feed oficial `feed.lolesports.com/livestats/v1/window|details/<gid>` (caché `feed_115660540726095074.json`, resumen
`g1_feed.txt`, asesinatos con asistencias `g1_asist.txt`); **VOD de Twitch del directo LATAM en ESPAÑOL**
https://www.twitch.tv/videos/2914166111 (el de YouTube aún no salía); `vod_g1_480.mp4` = VOD 3300-5500 s en 480p; narración con
Whisper large-v3 (`vod_g1_480_narr.txt`); relojes del HUD leídos a mano en cuadros. Scripts: `g1_feed.py`, `g1_asist.py`,
`g1_narrar.py`, `hojas.py`, `cortar_twitch.py`.
Contexto (previa `videos/cfo_kc_worlds/guion.py`): los dos llegaban 1-2; **el que pierde la serie queda eliminado**, el que gana
queda 2-2 y juega la ronda 5 el sábado 31. Bo3 Fearless. Narrador (archivo 1813-1817): si gana KC, «mandar a casa a toda la
LCP» (SIN VERIFICAR que CFO sea el último equipo de la LCP vivo: no decirlo en la voz sin comprobar).

## Reloj y desfases (MEDIDOS)
- **Archivo `vod_g1_480` = HUD + 145** · **VOD Twitch = HUD + 3445** (1.ª sangre en el kill feed: archivo 498 = HUD 05:53).
- **Feed = HUD + 3** (el feed va en ventanas de ~10 s: ±2 s; donde hay cuadro leído manda el cuadro).
- Draft en el VOD ≈ 3300-3440 (archivo 0-140); juego desde archivo 145. Fin: nexo HUD **27:39** (feed `finished` 20:39:41Z).
- Parche 26.20 (rótulo del HUD, cuadro j1 t 30).

## Alineaciones y campeones (feed oficial)
| Pos. | KC (azul) | CFO (rojo) |
|---|---|---|
| Top | Canna — Galio | Rest — **Rumble** (su campeón insignia: gastado en la G1 por el Fearless) |
| Jungla | Yike — Wukong (NO Lee Sin: lo guarda) | Shad0w — Jarvan IV (con la skin homenaje «Cyanide», narrador archivo 151) |
| Mid | kyeahoo — Cassiopeia | POUT — Syndra |
| ADC | Caliste — Tristana | Doggo — Kai'Sa |
| Support | Busio — Nautilus | Kino — Alistar |
Draft (narración archivo 0-140): CFO cierra con Kai'Sa («para no dejársela»); KC muestra Tristana como última; los narradores
DUDAN de Tristana: «no sé si era la más efectiva, considerando lo que hay al otro lado» (archivo 119-126) y «cuando te marca con
el ulti [Syndra], te van a llegar todas las esferas. Así que veremos si puede aguantar ese embate» (126-140). Bans: SIN LEER.

## Marcador final (feed)
| | KC | CFO |
|---|---|---|
| Asesinatos | **19** | **3** (los 3 de POUT) |
| Oro | 59 300 | 43 822 (**+15 478** KC) |
| Torres | 10 | **0** |
| Inhibidores | 2 | 0 |
| Barones | 1 (HUD 24:56) | 0 |
| Dragones | 3: Químico (11:31), Infernal (17:56), Infernal (23:20) | 1: Nube (05:35) |
K/D/A (feed): Canna 2/0/10 · Yike 4/0/11 · kyeahoo 6/1/8 (31 % del daño de KC) · **Caliste 7/0/5** (cs 314, 15.3K oro) · Busio 0/2/12 —
Rest 0/2/1 · Shad0w 0/6/3 · POUT 3/3/0 (37 % del daño de CFO; los 3 asesinatos de CFO son suyos) · **Doggo 0/3/0, participación
0 %** · Kino 0/5/2. KC: 3 muertes en total (kyeahoo 1, Busio 2); Canna, Yike y Caliste sin morir.

## Curva de oro (KC − CFO, feed por minuto; HUD = feed − 3)
| min | dif | kills | nota |
|---|---|---|---|
| 5 | +302 | 0-0 | CFO toma el dragón de Nube (05:35) |
| 6 | +938 | 1-0 | 1.ª sangre Yike a POUT (05:53) |
| 8 | +567 | 1-1 | POUT a Busio (07:50) |
| 10 | +1 093 | 2-1 | Caliste a Kino (09:46) |
| 12 | +2 280 | 5-1 | dragón Químico + 3 por 0 (11:31-11:46) |
| 15 | +1 434 | 5-2 | POUT a kyeahoo bajo torre (14:48); el mejor momento de CFO |
| 17 | +2 893 | 5-2 | 2 torres con el Heraldo (16:32-16:35) |
| 18 | +4 542 | 8-2 | pelea 3 por 0 (17:19-17:28) + Infernal |
| 19 | +6 479 | 11-2 | pelea 3 por 0 (18:31-18:36) |
| 22 | +8 065 | 12-2 | |
| 25 | +9 112 | 13-3 | pick a Shad0w + Barón (24:32-24:56) |
| 27 | +12 050 | 14-3 | inhibidores |
| fin | **+15 478** | 19-3 | ace 27:21-27:28, nexo 27:39 |
CFO nunca estuvo arriba en oro después del minuto 1 (01:00 −20).

## LAS JUGADAS (reloj HUD; «t» = segundo de la fuente `medios/_fuente/g1_j*.mp4`; archivo = vod_g1_480)
### J1 · 05:35-05:53 — CFO cambia el dragón de Nube por la primera sangre de POUT — fuente `g1_j1` (K 296)
- 05:35 CFO toma el dragón de Nube (t 39). 05:53 **Yike (Wukong) mata a POUT (Syndra)**, asisten kyeahoo y Busio (t 57).
- Narración (archivo 440-540): KC buscaba agresividad temprana; «el Rumble va a estar completamente controlado por parte del
  Galio» (455); «aprovecha todo el caos CFO para hacer este dragón» (477); «Gran lectura por parte de Busio, junto con Yike…
  sabíamos que no tenía Destello POUT, ya lo habían castigado en la primera emboscada, la segunda alcanza a salir libre, pero esta
  tercera… ya no» (505-522); «una vez que revisan que no hay visión cerca de ese arbusto, saben también que Shad0w junto con Kino
  retrocedieron porque acaban de hacer el dragón» (524-530). (Whisper: «Jake»=Yike, «Bucio»=Busio, «Pouta»=POUT, «Kana»=Canna.)
- Predicción de los narradores (546-551): «lo importante para KC es no dejar que esa Kai'Sa crezca, porque puede ser la gran
  clave para CFO» → **se cumplió para KC**: Doggo terminó 0/3/0 sin participar en ningún asesinato.
### J2 · 07:50 — La respuesta de CFO: POUT y Shad0w cazan a Busio en el río — fuente `g1_j2` (K 436)
- **POUT mata a Busio**, asiste Shad0w (t ≈ 34). Busio quema Destello, «doble definitiva en su contra» (610-620).
- Narración: «venían con muy malas intenciones Shad0w y Kino… funciona la emboscada de CFO» (626-644); «qué jugador es Shad0w,
  porque en el momento en el que no está Busio en el carril inferior, saben que puede estar en el río, porque no hay un
  centinela» (644-656). KC tenía la iniciativa: «está presionado el carril central, está presionado el carril superior» (600-603).
### J3 · 09:46 — Caliste castiga a Kino, que va un nivel abajo — fuente `g1_j3` (K 556)
- **Caliste (Tristana) mata a Kino (Alistar)**, asiste Busio (t ≈ 30). Narración: «se va a lanzar con todo lo que tienen…
  pero demasiado tarde, ya lo habían castigado muchísimo a Kino, y eso se paga con sangre» (729-736); «el gran problema es que
  Kino es nivel 5… y en el momento en que ya es nivel 6, el Nautilus, Busio, van hacia adelante, porque no te van a responder»
  (744-756); «tiene medio objeto esa Kai'Sa» (756).
- Predicción (716-728): «si [Caliste] se fidea, hay seguridad de que en juego medio y tardío se gane la partida» → **se cumplió**.
### J4 · 11:31-11:46 — El dragón Químico: Galio cae del cielo y 3 por 0 — fuente `g1_j4` (K 656) ★ candidata a 3D
- Antes (feed 11:00): +1 076 KC, 2-1. KC con visión: «hay centinelas cubriendo dicha área» (795-802). Yike empieza el dragón
  (813); CFO lo ve y entra: Kino usa su definitiva (818-821), Shad0w «quiere saltar por el risco» (822), Rest con Teleportación
  «queda en una posición medio comprometida» (835-836).
- 11:31 **Yike asegura el dragón Químico** (cuadro archivo 836, «The Inferno blazes»: el mapa pasa a infernal). 11:41 **Canna
  (Galio) mata a Shad0w** (asiste Yike); 11:43 **kyeahoo mata a Kino** y 11:46 **kyeahoo mata a Doggo** (cuadros archivo 846-852;
  feed 11:42/11:46/11:49). → 5-1, oro feed 12:00 +2 280.
- Narración: «Canna logra ponerse en pie y hace impacto fuertísimo en la entrada del dragón, dominando completamente la escena, y
  como si fuera poco, doble asesinato… desastre en el dragón en contra de CFO» (846-856); repetición (862-900): «Busio junto con
  Caliste van directamente por este Rumble… cae Canna completamente a ayudar a Yike»; «había ya activado Kino esa definitiva y por
  lo tanto no puede hacer nada; esa Kai'Sa no había regresado [a base]… no tiene el primer objeto, no pega lo suficiente Doggo… una
  jugada perfecta por parte de KC; si bien CFO propone bien, no tiene los recursos para impactar» (884-903).
  ERRORES de CFO: pelear el dragón con Doggo sin su primer objeto y con la definitiva de Kino ya gastada; TP de Rest mal colocado.
### J5 · 14:48 — Lo mejor de CFO: zambullida 3 contra 1 sobre kyeahoo — fuente `g1_j5` (K 856)
- **POUT mata a kyeahoo**, asisten Shad0w y Kino (t ≈ 33). La ÚNICA muerte de kyeahoo en la partida.
- Narración (1022-1048): «ojo Kino, quiere lanzarse bajo torreta, tiene la definitiva, podría tanquearla sin problema… buena
  mirada petrificante, pero no sé si con eso baste… [Destello] lo tiene en enfriamiento… aguanta lo que no está escrito, pero aún
  así es demasiado el castigo, tres contra uno»; crítica: «el ulti de POUT no le hizo ni cariño… no tiene nada de daño POUT»
  (1042-1046); «todavía no tiene la antorcha, todavía no tiene ese primer objeto» (1049-1052).
- Antes (archivo 996-1009, HUD ~14:10): KC frena una entrada del Rumble y «aparece Canna, sin siquiera tener que utilizar la
  teletransportación… esto es lo que estaba buscando KC». Oro: +2.9K (13:00) → +1.4K (15:00): el único tramo en que CFO recorta.
### J6 · 16:32-19:47 — El Heraldo, dos peleas 3 por 0 y el Infernal — fuente `g1_j6` (K 986, 220 s)
- 16:32 y 16:35 **dos torres de KC** con el Heraldo (t 46/49; «Heraldo golpea, segunda del carril central», 1150-1152).
- **17:19 Caliste mata a Kino** (asisten los 4), **17:20 Caliste mata a Rest**, **17:28 kyeahoo mata a Shad0w** (t 53/54/62).
  Rest entra con TP y la definitiva del Rumble (1167-1170, «aparecer esa Rumble con ulti»); «buena provocación [taunt de Galio]…
  la mirada petrificante, buen combo, espectacular» (1190-1196); «una pelea muy mala para CFO, consigue absolutamente todo lo que
  quiere KC» (1220-1226).
- 17:56 **dragón Infernal KC** (t 90). 18:25 torre (t 119).
- **18:31 Caliste mata a Doggo**, **18:34 Yike mata a Kino**, **18:36 kyeahoo mata a Shad0w** (t 125/128/130): «se lanzaba hacia
  adelante con todo Yike… mira quién aparece, kyeahoo, a cerrar el paso… salta el risco, caído uno, el segundo, tercero también…
  tres a cero de nuevo» (1253-1272); «la partida ahora sí se complicó, CFO no encuentra la manera de tener impacto» (1276-1280).
- 19:46 **Caliste mata a POUT** (t 200), tras «la iniciación por parte de Busio, él entra, agarra tres» (1288-1291); «pésimamente
  posicionados los chicos de CFO» (1312-1315); «no he visto una sola vez que haya hecho el combo CFO» (1323-1332).
  (Whisper muy entrecortado en este tramo: citar solo frases completas.)
### J7 · 24:32-24:56 — El pick a Shad0w y el Barón — fuente `g1_j7` (K 1436)
- **24:32 Yike mata a Shad0w** (asisten Canna, Caliste, Busio; t 36) · **24:35 POUT mata a Busio** (t 39) · **24:56 Barón KC**
  (archivo 1641; t 60). Repetición en la transmisión desde archivo 1647 (t ≈ 66).
- Narración: «provocación perfecta, el momento perfecto de Canna» (1609-1611); «se ha muerto el jungla… Barón» (1619-1621);
  repetición: «si bien se llevan a Busio, lo importante es que Shad0w cae» (1659-1664).
### J8 · 26:31-27:39 — El cierre: ace y nexo — fuente `g1_j8` (K 1566)
- 26:31 Caliste a Shad0w (t 25); inhibidores 26:53 y 27:00; **27:21-27:28 ace**: kyeahoo a Shad0w, Canna a Kino, kyeahoo a Rest,
  Yike a Doggo, Caliste a POUT (t 75-82); **nexo 27:39** (t 93); t 104 = pantalla de victoria.
- Narración: «victoria apabullante por parte de KC» (1763-1766); «no pudieron frenar a uno solo de los jugadores de KC» (1773-1775);
  «uno a cero» (1805).

### ★ La más importante: **J4 (11:31-11:46)**
Es la jugada donde CFO SÍ propone pelea (Kino con definitiva, Shad0w por el risco, TP de Rest) y aun así sale 3 por 0: se explica
con 3D (visión de KC en el foso, entrada de Canna desde arriba, ventana sin objeto de Doggo). Alternativa: J6 (las dos peleas 3 por 0).

## Fuentes cortadas (`medios/_fuente/`, 1080p30 + audio, VOD Twitch) — HUD = t + K (medido en 3 cuadros por fuente; constante)
| Archivo | desde (s VOD) | dur | K (s) | HUD inicio → fin | Contenido |
|---|---|---|---|---|---|
| g1_j1.mp4 | 3735 | 90 | 296 | 04:56 → 06:26 | dragón Nube 05:35 (t 39), 1.ª sangre 05:53 (t 57) |
| g1_j2.mp4 | 3875 | 70 | 436 | 07:16 → 08:26 | POUT a Busio 07:50 (t 34) |
| g1_j3.mp4 | 3995 | 60 | 556 | 09:16 → 10:16 | Caliste a Kino 09:46 (t 30) |
| g1_j4.mp4 | 4095 | 80 | 656 | 10:56 → 12:16 | dragón 11:31 (t 35), 3 por 0 11:41-11:46 (t 45-50); t 74 = repetición |
| g1_j5.mp4 | 4300 | 60 | 856 | 14:16 → 15:16 | POUT a kyeahoo 14:48 (t 32) |
| g1_j6.mp4 | 4425 | 220 | 986 | 16:26 → 20:06 | torres t 46/49; pelea t 53-62; Infernal t 90; pelea t 125-130; POUT t 200 |
| g1_j7.mp4 | 4875 | 90 | 1436 | 23:56 → 25:26 | Shad0w t 36, Busio t 39, Barón t 60; repetición ≈ t 66 |
| g1_j8.mp4 | 5005 | 110 | 1566 | 26:06 → 27:56 | Shad0w t 25; ace t 75-82; nexo t 93 |
K = desde − 3439 en las ocho (yt-dlp sobre Twitch arranca ~6 s después de lo pedido). Lecturas: j1 t5 05:01, t45 05:41, t84 06:20;
j4 t5 11:01, t40 11:36; j6 t5 16:31, t110 18:16, t214 20:00; j8 t5 26:11, t55 27:01.

## Dudas / sin verificar
- Bans (sin leer). Tipo de dragón «Químico»: feed `chemtech`. Que Canna «cae» con su definitiva en J4: narración, ver cuadro.
- Horas de J2/J3/J5 por feed − 3 (±2 s): confirmar en el cuadro al medir la pizarra.
- «Mandar a casa a toda la LCP»: sin verificar.
