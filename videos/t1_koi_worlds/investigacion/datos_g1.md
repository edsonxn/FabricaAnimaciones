# T1 vs Movistar KOI — PARTIDA 1 (Worlds 2026, fase suiza R4, Bo3) — datos verificados
gameId 115660540726095062 · T1 lado AZUL · ganó T1. Investigado el 28-oct-2026.
Fuentes: feed oficial `feed.lolesports.com/livestats/v1/window|details/<gid>` (caché `feed_115660540726095062.json`,
resumen `g1_feed.txt`, asesinatos con asistencias `g1_asist.txt`); VOD oficial https://youtu.be/rTVyiDIg-n8
(«MKOI vs T1 | WORLDS 2026 | DÍA 9 | FASE SUIZA | JUEGO 1», canal LoL Esports Latinoamérica, 47:17, **narración en ESPAÑOL**);
cuadros del HUD leídos a mano. Scripts: `g1_feed.py`, `g1_asist.py`, `g1_narrar.py`, `cortar.py`.

## Reloj y desfases (MEDIDOS)
- **Segundo del VOD = reloj HUD + 426** (constante): VOD 600 → HUD 02:54; VOD 1200 → 12:54; VOD 2800 → 39:34;
  y en las tiras de 1 s: VOD 766 → 05:40, VOD 1722 → 21:36, VOD 2450 → 33:44, VOD 2770 → 39:04. Las repeticiones NO meten
  hueco (el VOD tapa el directo mientras corren; el reloj sigue).
- **Reloj del feed = HUD + 4 s** (medido en 14 muertes: 1.ª sangre HUD 05:44 / feed 05:48; 21:42/21:46; 21:52/21:56;
  33:56/34:00; 34:01/34:05; 39:09/39:14; 39:41/39:45…). En este documento los relojes son del **HUD** salvo «feed».
- Duración: el HUD se congela en **39:55** al caer el nexo (VOD ≈ 2821 s). El feed marca `finished` en 40:05 (llega tarde).
  Duración oficial escrita: sin verificar (Leaguepedia con límite de peticiones); por el HUD, **≈ 39:55**.
- Draft en el VOD ≈ 290-400 s; el juego empieza en VOD 426. Rótulo del draft: «T1 BLUE SIDE ▶ MKOI 1ST PICK», PATCH 26.20.

## Alineaciones y campeones (feed oficial + draft del VOD)
| Pos. | T1 (azul) | MKOI (rojo) |
|---|---|---|
| Top | Doran — Ambessa | Myrwn — Gnar |
| Jungla | Oner — Lee Sin | Elyoya — Qiyana |
| Mid | Faker — Syndra | Jojopyun — Akali |
| ADC | Peyz — Xayah | Supa — Kai'Sa |
| Support | Keria — Nautilus | Alvaro — Alistar |
Entrenadores (rótulo del draft): T1 «Tom», MKOI «Melzhet».
**Bans: SIN VERIFICAR** (no están en la descripción ni en el feed; lectura del icono en el cuadro VOD 395 s):
T1 → 1.º Cassiopeia (dudoso), Vi, Ezreal, 2 sin identificar; MKOI → Camille, 4 sin identificar. Recorte: `cuadros_g1/` no lo
incluye; repetir con `ffmpeg -ss 395` y crop `430,570,1480x290` si hace falta.

## Marcador final (feed, último frame)
| | T1 | MKOI |
|---|---|---|
| Asesinatos | **20** | **10** |
| Oro | 82 899 (HUD 39:55: 82.7K) | 79 836 (79.8K) |
| Torres | 10 | 5 |
| Inhibidores | 1 | 0 |
| Barones | 1 (HUD ~22:29) | 1 (HUD ~34:42) |
| Dragones | 4: Nube (6:35), Océano (11:59), Infernal (23:19), Infernal (39:10) → 4.º = **alma** (mapa infernal) | 3: Infernal (17:41), Infernal (28:39), Infernal **robado** (33:51) |
(Horas de dragón = feed − 4 s. El alma: 4.º dragón de T1 + «Va a ser el alma» del narrador; el rótulo del alma no se vio en el cuadro → tipo «Infernal» deducido del mapa, sin rótulo visto.)

K/D/A (feed): Doran 6/0/6 (cs 383) · Oner 6/3/9 · Faker 5/2/8 · Peyz 2/3/9 (cs 478, 21.1K oro) · Keria 1/2/14 —
Myrwn 2/3/4 (37 % del daño de KOI) · Elyoya 3/6/5 · Jojopyun 2/5/2 · Supa 3/2/4 · Alvaro 0/4/9.
Doran sin morir en toda la partida (0 muertes). Anuncio «T1 Doran is unstoppable!» en HUD 39:10.

## Curva de oro (T1 − KOI, feed por minuto; HUD = feed − 4 s)
| min | dif | kills | nota |
|---|---|---|---|
| 3 | +22 | 0-0 | |
| 5 | +255 | 0-0 | |
| 6 | −344 | 0-1 | 1.ª sangre Jojopyun a Faker |
| 9 | **−1 714** | 0-3 | doble de Elyoya (8:17-8:23) |
| 12 | −216 | 3-3 | T1 remonta (Oner 9:40 y 11:18, Faker 11:53) |
| 15 | −274 | 3-3 | |
| 18 | −634 | 5-5 | pelea 17:17-17:21 pareja; dragón infernal KOI |
| 19 | −1 326 | 5-6 | |
| 21 | +56 | 7-6 | |
| **23** | **+3 306** | 13-7 | pelea + Barón de T1 |
| 26 | +5 217 | 14-7 | **máx. T1 +5 805 (feed 26:14)** |
| 28 | +5 418 | 14-7 | |
| 30 | +3 909 | 14-7 | |
| 33 | +4 220 | 14-7 | |
| 35 | +151 | 15-10 | KOI roba dragón, gana pelea y Barón |
| 37 | −1 827 | 15-10 | **máx. KOI −2 094 (feed 37:02)**; KOI tira 3 torres (feed 36:02-36:45) |
| 39 | −1 558 | 15-10 | |
| 40 (fin) | +2 972 → +3 063 | 20-10 | pelea final + nexo |

## Asesinatos con asistencias (feed, diferencia de K/D/A; HUD ≈ feed − 4) → `g1_asist.txt`

## LAS JUGADAS (reloj HUD)
### J1 · 05:44 — Primera sangre: Jojopyun (Akali) a Faker (Syndra) — fuente `g1_j1`
- Asiste Alvaro (Alistar). Cuadro HUD 05:42: Faker en el río con Alvaro encima y Jojopyun y Elyoya cerca.
- Narración (Whisper): Jojopyun ya le había quemado el Destello a Faker antes («termina quemando el destello en Faker», t 9-13);
  t 66-76: «¡Ah, que venía! … Venía Álvaro justamente del jardín inferior. Lo acosan por todas partes … y sin destello ya no
  hay nada que hacer. Termina cayendo la primera sangre para KOI».
- Oro: HUD 05:40 9.4K-9.3K → 05:55 9.7K-10.1K (−0.4K).
### J2 · 08:17-08:23 — Doble de Elyoya (Qiyana) en la jungla de T1 — fuente `g1_j2`
- 08:17 Elyoya mata a Oner (asisten Supa, Alvaro); 08:23 Elyoya mata a Peyz (asisten Myrwn, Supa, Alvaro). Marcador 0-3.
- Oro feed: 08:00 −610 → 09:00 −1 714 (el máximo de KOI en el juego temprano).
- Narración t 55-96: «qué buena entrada… se lleva rápidamente un asesinato… doble asesinato, está totalmente desatado el
  jungla de los chicos de KOI, ya va tres cero»; «cómo entran a la jungla, sin que hubiera visión por parte de T1, y los
  terminan agarrando, literalmente, por la espalda»; «entre el combo del Alistar y la [Qiyana], derritieron a Oner».
  (Whisper escribe «Sakiana/Kiana» = Qiyana, «Pace» = Peyz.)
### J3 · 21:42-22:33 — LA PELEA DE T1: 5 por 1 + Barón — fuente `g1_j3` ★ candidata a 3D
- Antes (HUD 21:36): 41.2K-41.4K (−0.2K), 7-6, T1 con 3 torres. Narrador: «21 minutos con 16 segundos … la ventaja en oro
  sigue siendo para KOI, pero mínima».
- Orden (HUD): 21:42 **Faker mata a Alvaro** (asisten los 4) — Doran había entrado sobre Alvaro; KOI responde con el TP de
  Jojopyun («va a aparecer Jojopyun, llega directo»). 21:47 **Myrwn mata a Faker** (asiste Jojopyun) y en el mismo segundo
  **Doran mata a Jojopyun** (asiste Faker). 21:52 **Oner mata a Elyoya** (asisten Doran, Peyz, Keria). 21:56 **Doran mata a
  Supa** (asisten Oner, Peyz, Keria). → 11-7.
- **22:29 Barón de T1** («Blue team has slain Baron Nashor!» en el cuadro HUD 22:30). 22:31 **Oner mata a Alvaro**, 22:33
  **Peyz mata a Myrwn** → 13-7.
- Oro: HUD 22:35 46.3K-43.1K (**+3.2K**); feed 23:00 +3 306. Después: dragón infernal T1 (23:19) y 4 torres en 4 min.
- Narración: t 50-67 «el [Jojopyun] ulti, le pega directo a Keria y [Peyz] … salta con destello, estaba [Myrwn] cerca, no se
  quiso plantar … y eso le termina costando 4 muertes a KOI»; t 67-90 «el único que murió fue Faker, porque recuerden la
  teletransportación de la [Akali] de Jojopyun»; t 91-97 «tiene 1400 de vida el [Barón], finalmente se los queda la
  escuadra»; t 97-103 «de postre, de regalo, en bandeja de plata, le entregan dos asesinatos más»; t 127-145 «[Supa] no puede
  pegar … el [Elyoya] llega un poco tarde a la teamfight … la teamfight es forzada».
  (Whisper repitió «se va a lanzar» ×12 en t 20-50: alucinación, no citar ese tramo.)
### J4 · 33:51-34:01 — KOI ROBA el dragón (el que podía ser alma de T1) y gana la pelea 3 por 1 → Barón — fuente `g1_j4`
- Antes (HUD 33:44): 67.5K-64.1K (**+3.4K** T1), 14-7, T1 con 3 dragones (alma en juego).
- 33:51 «Red team has stolen the Infernal Drake!» (cuadro HUD 33:51-33:52). Quien lo roba: **Myrwn (Gnar)** — icono del
  kill feed y narración t 79-84 «Primero aseguraron el dragón … Lo termina ganando el Gnar, de hecho».
- 33:56 **Supa mata a Oner** (asisten Myrwn, Elyoya, Alvaro); 33:58 **Doran mata a Elyoya** y **Supa mata a Peyz**;
  34:01 **Myrwn mata a Keria** → 15-10.
- **34:42 Barón de KOI** (cuadro HUD 34:42 «Red team has slain Baron Nashor!»). Con él KOI tira 3 torres (feed 36:02, 36:25,
  36:44) y pasa a **−2.1K** (feed 37:02).
- Oro: HUD 34:10 69.4K-67.3K (+2.1K) → feed 35:00 +151 → 37:00 −1 827.
- Narración: t 6-12 «El dragón que podría llegar a ser el alma si lo saca T1»; t 61-73 «Cuidado, se lo roban… Y mira, se la
  hace hacia delante [Myrwn]. Muy buena el Mega Gnar. Complica completamente la escuadra de T1»; t 91-98 «Primero con la
  entrada de Álvaro, que asegura un control en contra de [Faker]. Y luego también lo que hace Myrwn, que cuando se transforma
  en Mega Gnar, lo deja servido»; t 106-115 «la dejaron libre a Supa y se llevó un doble kill»; t 115-119 «los dos K de oro que
  tenía de ventaja… ya no existen. Están igualados». (Whisper escribe «FaZe» = Faker en t 91-106: por contexto, verificar.)
### J5 · 39:09-39:55 — Pelea del alma: Doran entra, T1 hace 5 por 0 y cierra — fuente `g1_j5`
- Antes (HUD 39:04): 77.7K-79.2K (**−1.5K**), 15-10, KOI con Barón ya gastado; dragón 4 de T1 en juego.
- 39:09 **Doran mata a Supa** (asisten Oner, Peyz, Keria); **39:10 T1 se lleva el dragón (4.º → alma)**, cuadro con «T1 Doran
  is unstoppable!»; 39:14-15 **Faker mata a Jojopyun** y **Peyz mata a Alvaro**; 39:19-20 **Doran mata a Elyoya**; 39:39 torre;
  39:40-41 **Oner mata a Myrwn** (el último, aguantaba solo) → 20-10; inhibidor, torres del nexo y **nexo HUD 39:55**.
  T1 no pierde a nadie en esta pelea (feed: 0 muertes de T1 después de 34:01).
- Oro: −1.5K (39:04) → +2.4K (39:44) → +2.9K (39:55).
- Narración: t 20-40 «Va a ser el alma, si termina en un exterminio, seguro que la partida se acaba ahí»; t 50-69 «ojo, que
  se lanza con todo Doran, que inicia la pelea antes de que se desate el caos … ¿quién se lo quedó? ¡Cómo no! Aparecía Doran y
  lograba llevarse el objetivo, T1 se impone en la pelea del dragón»; t 80-83 «Teletransportación por parte de [Faker] en la
  base, y van a ir a destruir directamente el Nexus»; t 84-105 «la última esperanza de KOI, que acaba de caer … para una
  partida, la verdad, bastante sufrida, que cometieron errores imperdonables».
  (Que Doran se lleve el dragón lo dice el narrador; el remate del dragón no lo comprobé en el kill feed: verificar en el cuadro.)

### ★ La más importante: **J3 (21:42-22:33)**
Es el vuelco: KOI iba por delante desde el minuto 6 (−1.7K al 9) y T1 pasa de −0.2K a +3.2K en 55 s con 5 por 1 + Barón,
camino de su máximo (+5.8K). Tiene una secuencia clara para 3D: Doran entra sobre Alvaro, TP de Jojopyun por detrás, Faker
cae pero Doran lo cambia por Jojopyun, Oner y Doran rematan a Elyoya y Supa, Barón y 2 asesinatos más. Alternativa
dramática: **J5**, la pelea del alma que decide el partido con Doran iniciando (5 por 0).

## Fuentes cortadas (`medios/_fuente/`, 1080p30 + audio AAC 192k) — HUD = t_fuente + K
| Archivo | vid | desde (s VOD) | dur | K (s) | HUD al inicio → fin | Contenido |
|---|---|---|---|---|---|---|
| g1_j1.mp4 | rTVyiDIg-n8 | 700 | 95 | 274 | 04:34 → 06:09 | 1.ª sangre a Faker (05:44 ↔ t 70) |
| g1_j2.mp4 | rTVyiDIg-n8 | 865 | 105 | 439 | 07:19 → 09:04 | doble de Elyoya (08:17 ↔ t 58; 08:23 ↔ t 64) |
| g1_j3.mp4 | rTVyiDIg-n8 | 1680 | 150 | 1254 | 20:54 → 23:24 | pelea 21:42 (t 48) → Barón 22:29 (t 95) → 22:33 (t 99); repetición después |
| g1_j4.mp4 | rTVyiDIg-n8 | 2396 | 150 | 1970 | 32:50 → 35:20 | robo 33:51 (t 61), pelea 33:56-34:01 (t 66-71), repetición desde ~34:12, Barón KOI 34:42 (t 112) |
| g1_j5.mp4 | rTVyiDIg-n8 | 2720 | 105 | 2294 | 38:14 → 39:59 | pelea 39:09 (t 55), dragón 39:10 (t 56), nexo 39:55 (t 101) |
(g1_j5: el audio se cortó al bajarlo por streaming; se rehízo con el audio completo del VOD, misma sincronía.)
Transcripciones Whisper large-v3 (es): `investigacion/g1_j1_narr.txt` … `g1_j5_narr.txt` (segundos = t de la fuente).

## Cuadros de referencia (`investigacion/cuadros_g1/`, 640 px)
01_j1_hud0542 · 02_j2_hud0815 · 03_j3_hud2140 · 04_j3_baron_hud2230 · 05_j4_hud3352 (rótulo del robo) ·
06_j4_baron_hud3442 · 07_j5_hud3908 · 08_j5_nexo_hud3955 (nombre = reloj HUD leído; VOD = HUD + 426).

## Dudas / sin verificar
- Bans (solo lectura parcial de iconos). Duración oficial escrita (HUD ≈ 39:55).
- Asistencias: por diferencia de K/D/A en frames de 10 s; si dos muertes caen en el mismo frame, las asistencias se mezclan
  (21:47 y 33:58: dos muertes casi simultáneas).
- Tipo del alma: deducido (mapa infernal desde el 3.er dragón), no visto el rótulo.
- Whisper deforma nombres (Pace=Peyz, Mewen/Mirwin=Myrwn, FaZe/Spaker=Faker, Sakiana=Qiyana, varón=Barón).
