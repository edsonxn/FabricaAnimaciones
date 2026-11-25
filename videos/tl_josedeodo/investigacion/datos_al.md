# AL vs TLAW (Team Liquid) — Bo3 ronda 3 suiza, Worlds 2026, 26-oct-2026 — PARTIDA 1 — datos verificados
TLAW gana 16-5 (la serie la gana 2-0). gameId 115660540726095058 (match 115660540726095057). Inicio del feed 21:01:28 UTC.
VOD español (LoL Esports Latinoamérica) **ArfLpTbwAOw** «TLAW vs AL | WORLDS 2026 | DÍA 8 | FASE SUIZA | JUEGO 1» (2341 s). VOD inglés (LoL Esports) **Q28aQ_pETPE** «TLAW vs. AL | WORLDS 2026 | Swiss Stage | Day 04» (5787 s, serie completa; sin calibrar). Ambos de `getEventDetails` → `ev_al_tl.json`.
Investigado el 25-nov-2026. Feed: `al_g1_feed.txt` (muertes), `al_g1_asist.txt` (objetivos + asesino/asistentes + oro por minuto; `al_feed.py`, caché `feed_115660540726095058.json`). Narración (subtítulos automáticos es, seg = VOD): `al_g1_narr.txt` (`al_vtt.py` sobre `subs/al_es.es-orig.vtt`).
Los subtítulos cambian nombres; entre [ ] va el real: José de Oro/José de Odo/José Dodo/Joseo/Jose = Josedeodo · Jean/Jeon/Gion/John/Jhon = Yeon · Quick/Quinn/Quill = Quid · Corgy Jay/CorJJ = CoreJJ · Morgana = Morgan · Brith/Bridy/Brida/Braille/Brise/Breed = Breathe · Kobbe/Job = Hope · Cael = Kael · Tarson = Tarzan · Zambesa/Lambeza/Ayunara/Guinara = Ambessa/Yunara · Niwans Legends/Animals Legion/New One Slayers/Ninjas in Pyjamas = Anyone's Legend · Kiana = Qiyana.
Herramientas nuevas (en esta carpeta): `al_reloj.py` (franja del HUD desde la URL del VOD), `al_tira.py` (franja o cuadro con rejilla desde la fuente local), `al_zoom.py` (hoja 4×4 de recortes). Cuadros en `previews/cuadros/al_*.jpg`.

## Reloj (MEDIDO en cuadros; en la voz va SIEMPRE el HUD)
| Fuente | HUD = t − K (VOD) / t + K (clip) | Cuadros que lo fijan |
|---|---|---|
| VOD ArfLpTbwAOw | **VOD = HUD + 319** (sin pausas) | 400 = 01:21 · 700 = 06:21 · 725 = 06:46 FIRST BLOOD · 1200 = 14:41 · 1279 = 16:00 · 1385 = 17:46 · 2200 = 31:21 · 2306 = 33:06 |
| Feed | **feed ≈ banner + 4** (objetivos y muertes) · ≈ marcador + 3 | 1.ª sangre banner 06:46 / feed 06:50 · dragón 1 banner 05:36 / feed 05:40 · Barón 2 banner 31:09 / feed 31:13 |
| `al_j1.mp4` | **HUD = t + 1696** | t 1 = 28:17 · t 18 = 28:34 · t 30 = 28:46 · t 72 = 29:28 (alma) |
| `al_j2.mp4` | **HUD = t + 1009** | t 1 = 16:50 · t 10 = 16:59 · t 110 = 18:39 · t 119 = 18:48 |
OJO: el banner de muerte sale ~2 s ANTES de que cambie el marcador (Hope: banner 28:44, marcador 28:46). Duración: último HUD leído 33:06 (VOD 2306, torre); feed `finished` 33:18 → fin ≈ **33:14 ± 2** (el nexo no se ve con HUD: la realización pasa al escenario en VOD 2310).

## Resultado, lados y picks
| | Lado | Kills | Oro final | Torres | Barones | Dragones | Larvas | Heraldo |
|---|---|---|---|---|---|---|---|---|
| **AL** | azul | 5 | 55,5 K | 2 | 0 | 1 (nube, ROBADO 23:31) | **3** (HUD 0→3 entre 08:21 y 09:21; narrador VOD 836: «se quedan con las [vacío]larvas») | — |
| **TLAW** gana | rojo, **1.ª selección** (pantalla del draft: «BLUE SIDE» AL / «1ST PICK» TLAW) | 16 | 69,7 K (**+14,2 K**) | 9 + inhibidor | **2** | **4 = ALMA DE NUBE** (químico, hextech, nube, nube) | 0 | **1** (HUD 16:00, usado 16:50) |
| Jugador | Campeón | K/D/A | cs | Oro | % daño | KP | Guardianes |
|---|---|---|---|---|---|---|---|
| AL Breathe (top) | Ambessa | 2/5/1 | 305 | 11,5 K | 25,2 % | 60 % | 10 |
| AL Tarzan (jg) | Skarner | 0/3/5 | 207 | 10,5 K | 14,5 % | 100 % | 17 |
| AL Shanks (mid) | Orianna | 3/3/1 | 303 | 12,4 K | 30,5 % | 80 % | 17 |
| AL Hope (adc) | Yunara | 0/4/2 | 340 | 13,5 K | 22,9 % | 40 % | 19 |
| AL Kael (sup) | Lulu | 0/1/4 | 45 | 7,6 K | 6,9 % | 80 % | 65 |
| TLAW Morgan (top) | **Camille** | **7/1/6** | 319 | 16,3 K | 27,7 % | 81 % | 14 |
| TLAW Josedeodo (jg) | **Lee Sin** | **3/0/8** | 251 | 13,5 K | 11,8 % | 69 % | 22 |
| TLAW Quid (mid) | Galio | 2/0/11 | 290 | 13,6 K | 18,3 % | 81 % | 15 |
| TLAW Yeon (adc) | Lucian | 3/3/9 | 341 | 16,9 K | 33,4 % | 75 % | 14 |
| TLAW CoreJJ (sup) | Nami | 1/1/13 | 30 | 9,4 K | 8,9 % | 88 % | 58 |
(Fuente: `stats_115660540726095058.json`, feed final.)
- **Draft (VOD 49-262):** el primer bloqueo que nombra el narrador es Qiyana («de inmediato denegada», VOD 49). Lee Sin entra con ovación (VOD 56) y la tarjeta en pantalla dice **«77.6% FEARLESS PB% · 32.7% PICK · 7W-9L»** (cuadro `al_draft_58.jpg`; no dice el ámbito de la cifra: decir «según la transmisión»). Narrador sobre esa selección (VOD 60-89): «[Josedeodo] rompe el Worlds con un Lee Sin en donde lo invaden, lo acosan, lo hostigan… y fue justamente con Lee Sin. Veremos si acá se repite la historia». AL abre con Yunara + Lulu (narrador VOD 128-131), luego Orianna; TL Lucian + Nami (VOD 124), Camille contra Ambessa (VOD 218-225), Galio de cierre (VOD 229); AL último: Skarner (VOD 258). Narrador: «el buen combo entre el Lee Sin y la Camille» (VOD 231). Bloqueos completos: ⚠ no leídos (iconos de 36 px).

## Relato de la partida (HUD)
1. **05:36** TL dragón químico (banner VOD 655). **06:46 PRIMERA SANGRE: Josedeodo mata a Hope** en el carril inferior (asisten Quid, Yeon, CoreJJ), tras el cebo de CoreJJ que le quema el destello a Hope (narración VOD 584-606 y 794-796). Narrador: «Aquí viene [Josedeodo], este es el dive que estábamos esperando… se adelanta [Josedeodo], viene el combo… es primera sangre para Team Liquid» (VOD 696-726) · «no tiene que gastar [Josedeodo] la furia del dragón» (VOD 732).
2. 08:21-09:21 AL toma las 3 larvas. 08:57 Morgan mata a Hope (feed 09:01) · 09:16 Breathe mata a Yeon (feed 09:20). **11:29** TL dragón hextech. 13:54 TL primera torre (feed 13:58) · 13:58 Shanks mata a Morgan (feed 14:02) · 14:22 AL torre.
3. **≈16:00 TL toma el Heraldo** (banner ya en pantalla en VOD 1279 = 16:00), lo suelta a las **16:50**. Narrador (VOD 1296-1301): «declaraciones mismas de [Josedeodo] menciona que hoy en día el Heraldo no se utiliza por objetivos, sino que para pelear».
4. **17:09-17:16 = J2** (patada de Josedeodo a Breathe, Morgan lo remata 17:16) → **17:46 TL dragón nube** (3.º).
5. 19:04 TL torre · 19:28 Morgan mata otra vez a Breathe (feed 19:32).
6. **23:31 «Blue team has STOLEN the Cloud Drake!»**: Tarzan roba el dragón con castigo delante de Josedeodo (cuadro VOD 1731). Narrador: «el castigo, se lo termina robando en la cara a [Josedeodo]» (VOD 1729-1731). En la repetición culpan a Yeon: «[Yeon] le tira una luz lacerante y deja el dragón en 1360… si hay que apuntar a alguien, apunten a Lucian, que terminó pegando de más» (VOD 1795-1805). Acto seguido TL mata a 4 sin perder a nadie (feed 23:42-23:51 → HUD ~23:38-23:47: Quid a Hope, CoreJJ a Tarzan, Morgan a Shanks, **Josedeodo a Breathe**). Narrador: «terminan robándose el dragón, pero a lo mejor es la trampa… se llevan cuatro asesinatos y se ponen 5K de ventaja» (VOD 1746-1754).
7. **Barón 1 TL: HUD ~24:22** (sin cuadro: cae durante la repetición; feed 24:27 − 4, y el contador de reaparición del Barón marca 1:43 a las 28:39 → 24:22). 24:55 TL torre (feed 24:59). 25:08 Shanks mata a Yeon (feed 25:12).
8. **28:39-29:03 = J1**: pelea del ACE (5 por 2) → **29:28 TL dragón nube = ALMA DE NUBE** (cuadro VOD 2088; cartel «DRAGON SOUL» en J1 t 72).
9. **31:09 Barón 2 TL** (banner VOD 2188). 32:43-32:56 TL mata a Tarzan, Shanks y Breathe; inhibidor 32:53 (feed 32:57); torres 33:04-33:06; fin ≈ 33:14.
- Oro (feed, AL − TL): TL arriba desde el min 1 casi siempre; −2,3 K a los 14:00, −2,9 K a los 22, −6,6 K tras el Barón (25:12), −7,8 K a las 29:04 (cuadro), −13,6 K a las 33:01 (cuadro), **−14,2 K final**.
- Josedeodo: 3 asesinatos = 1.ª sangre a Hope (06:46), Breathe (~23:47), Breathe para el ACE (29:02). **0 muertes.** Asistió en la de Breathe 17:16, en los 3 primeros de la pelea del ACE y en las 3 últimas muertes de AL.

## Las 2 jugadas
Las fuentes: `medios/_fuente/al_j<n>.mp4`, 1920×1080, 30 fps, 120 s, con narración original en español. HUD = t + K.
| # | Título | Reloj HUD | Fuente | K | t clave |
|---|---|---|---|---|---|
| J1 | **La patada del ACE: Camille y Lee Sin por el flanco** | 28:39-29:03 | al_j1 (VOD 2015, 120 s) | **1696** | ver abajo |
| J2 | **La patada a Breathe antes del dragón** | 17:09-17:16 | al_j2 (VOD 1328, 120 s) | **1009** | ver abajo |

**J1 paso a paso (al_j1).** Marcador 3-8, TL +6,0 K, Barón de TL ya gastado (reaparece en 1:43), 3 dragones TL, el 4.º (alma) por salir.
t 10-13 (28:26-28:29): narrador «viene el TP… ahí va a aparecer [Morgan], viene de la base» (VOD 2025-2028). t 23,5 (28:39): **Morgan y Josedeodo juntos ARRIBA a la izquierda, por detrás del muro** (flanco), con los cinco de AL abajo frente a Yeon, CoreJJ y Quid. t 25 (28:41): Quid con «CHANNELING» (ulti de Galio) sobre Tarzan; Morgan ya encima de Hope dentro del círculo de su ulti. t 26,4 (**28:42**): **Hope con «AIRBORNE»** junto a Josedeodo; Morgan «POLYMORPHED» (Lulu de Kael); Quid «SUPPRESSED» (ulti de Skarner). t 28,5 (**28:44**): «TLAW Yeon has slain AL Hope!» (marcador 3-9 a las 28:46). t 32 (28:48): DOUBLE KILL de Yeon (Tarzan, marcador 3-10). t 35 (28:51): TRIPLE KILL de Yeon (Kael, 3-11). t 36-37 (28:52-53): «SHUT DOWN!»: Breathe mata a Yeon (4-11). t 39 (28:55): Shanks mata a CoreJJ (5-11). t 41 (28:57): «TLAW Morgan is on a rampage!» (Shanks, 5-12). t 45,4 (29:01): Breathe casi sin vida entre Josedeodo y Morgan, los otros 4 de AL muertos. t 46 (**29:02**): **«ACE!»** = Josedeodo mata a Breathe (feed 29:07: asesino Josedeodo); marcador 5-13 a las 29:04, +7,8 K. t 72 (29:28): «Red team has slain the Cloud Drake!» + «DRAGON SOUL».
Narración en vivo (VOD 2035-2071, t 20-56): «mira cómo entra [Morgan] por el flanco, se suma [Josedeodo], le va a pegar… en toda la boca, lo pateó… asesinato por primera vez en la partida [de Yeon], bien ahí, tiene el doble… llega [Breathe] y logra llevarse a [Yeon]… se va a sumar el quinto… ahí está el jovenzuelo, el adolescente, [Josedeodo] a patadas… lo clava al piso, cinco asesinatos, exterminio, dragón y alma para Team Liquid».
Narración de la repetición (VOD 2098-2122, t 83-107): «la jugada estaba completamente planeada, se lanza [Morgan], [Morgan] ultimátum hextech encima de [Hope] para que no se escape y luego entra [Josedeodo], furia del dragón, mucho control, mucho daño… [Hope] no puede jugar esta partida… desde que [Morgan] y [Josedeodo] sacaron la ventaja del oro para tener el daño suficiente para quemarlo en un combo». Elogio a Shanks (VOD 2123-2139): onda de choque a CoreJJ y Yeon, Zhonya, destello y mata a CoreJJ.
Repetición limpia «MOMENT OF THE GAME» (sin marcador): t ~78,8-111 (≈ en vivo t 15-47, desfase +62/+65: no constante, se mide por banners: DOUBLE KILL t 96, TRIPLE t 100, Breathe→Yeon t 104, Morgan→Shanks t 108). Público t ~111-114. Gráfico «Damage Dealt to Champions Last Teamfight» t ~115-120.

**J2 paso a paso (al_j2).** Marcador 2-2, TL +1,0 K, 2 dragones TL, el 3.º (nube) a punto; Heraldo de TL soltado a las 16:50 (t 1).
t 1 (16:50): «Red team has summoned the Rift Herald!». t 20,5 (**17:09**): Breathe (Ambessa, nivel 13) con «ROOTED» pegado a Josedeodo; Tarzan «STUNNED» atrás. t 21,5 (**17:10**): **Breathe con «AIRBORNE» ya del lado de Yeon, CoreJJ y Quid**: la patada lo manda dentro de TL (comparando t 20,5 → 21,5, sale del lado de Josedeodo hacia el norte, con la cámara casi quieta). t 22,5 (17:11): Breathe en medio de Yeon, CoreJJ y Quid; Morgan entra por abajo a la derecha. t 24,5 (17:13): Josedeodo (nivel 11) «SUPPRESSED» + «SILENCED» junto a Tarzan (ulti de Skarner); Quid «CHANNELING». t 27,5 (**17:16**): «TLAW Morgan has slain AL Breathe!» (marcador 2-3 a las 17:19; asisten los otros 4 de TL); Josedeodo sale con la vida muy baja. t 57 (17:46): «Red team has slain the Cloud Drake!» (3.º dragón TL).
Narración en vivo (VOD 1341-1385, t 13-57): «el dragón ya está en obras, por el momento [Josedeodo] sigue ahí en posición, [Tarzan] se quiere posicionar… Se cancela el dragón al menos por ahora. Cuidado, cadena control. Se lanzaba el abuelo. El octogenario lo patea perfecto, lo deja en una mala posición a [Breathe], tiene que caer. [Yeon] queda corto en daño… ahí está [Morgan]. Salta encima y termina el trato… cae el top laner de [Anyone's Legend]… van a ganar la posesión del dragón».
Narración del análisis (VOD 1386-1437, t 58-109): «la Ambessa no es el objetivo ideal… no es el mejor objetivo como para matar rápidamente después de una jugada de Insec. De hecho, sobrevive por bastante tiempo y después [Morgan] la termina sacrificando. Eso fuerza que [Josedeodo] tenga que salir muy herido… Team Liquid queda con una posición de tres contra cuatro… Se quedan con el objetivo, que es lo más crítico».
Repetición («REPLAY», sin marcador): t ~67,9-~98 (banner de Morgan a Breathe en t 84 ≈ en vivo 27,5 → desfase ≈ +56,5). Cámara de jugador ~98-104. En vivo otra vez desde t 104,2 (t 110 = 18:39).

**Alternativas (reloj y cuadro verificados, SIN fuente cortada):**
- **Primera sangre de Josedeodo, HUD 06:43-06:47, VOD ~700-730**: dive al carril inferior, FIRST BLOOD a 06:46 (cuadros `al_fb.jpg`). Narración arriba (punto 1).
- **El robo de Tarzan, HUD 23:31, VOD ~1715-1770**: «Blue team has stolen the Cloud Drake!» y la pelea de 4 por 0 de TL justo después; repetición del castigo VOD ~1772-1805 (cuadros `al_obj2.jpg`). Muy a cuento para «¿culpa de Josedeodo?»: le roban el dragón con su castigo y el narrador culpa a Lucian, no a él.

## Pausas (coordenadas de PIES, fracción del cuadro completo; `al_j*_r<t>.jpg` en previews/cuadros, rejilla 0,1)
Pies = punto bajo el campeón (≈ etiqueta + 0,09-0,10). Precisión MEDIA en general (medidos desde la etiqueta con rejilla, no con anillo). Sin coordenada = bajo el HUD (y > 0,76) o no identificado.
| Fuente | t | HUD | Toma | Pies |
|---|---|---|---|---|
| j1 | 23,5 | 28:39 | 0-25,3 | Morgan + Josedeodo .21,.24 (juntos, etiquetas encimadas) · Yeon .49,.26 · CoreJJ .70,.37 · Quid .69,.57 · Tarzan .51,.70 · Shanks .28,.68 · Hope .36,.76 (al límite) · Kael bajo HUD · Breathe fuera de cuadro |
| j1 | 26,4 | 28:42 | 25,6-38,3 | **Josedeodo .38,.47** · **Hope (AIRBORNE) .46,.58** · Morgan (POLYMORPHED) .48,.61 · Kael .48,.33 · Shanks .65,.52 · Tarzan .77,.48 · Quid (SUPPRESSED) .83,.35 · Yeon .56,.21 · CoreJJ .72,.22 · círculo de la ulti de Camille ≈ x .32-.56, y .45-.70 |
| j1 | 28,5 | 28:44 | 25,6-38,3 | Josedeodo .38,.61 · Tarzan .48,.56 · Morgan .53,.59 · Quid (CHANNELING) .55,.47 · Kael .18,.47 · Shanks .67,.47 · Yeon y CoreJJ (AIRBORNE, por nivel 15 y 12) .53,.33/.53,.39 (duda) · Hope ya muerta (banner) |
| j1 | 45,4 | 29:01 | 38,3-52,1 | **Breathe (casi sin vida) .58,.62** · **Josedeodo .42,.61** · Morgan .50,.60 · Quid (CHANNELING) .43,.47 (media) · los otros 4 de AL muertos (retratos con contador) |
| j2 | 20,5 | 17:09 | 0-39,7 | **Breathe (ROOTED) .42,.57** · **Josedeodo .45,.62** · Quid .47,.50 · Tarzan (STUNNED) .30,.40 · Hope .30,.25 · Kael .17,.27 · Shanks .24,.64 · Yeon .47,.27 · CoreJJ .52,.27 |
| j2 | 21,5 | 17:10 | 0-39,7 | **Breathe (AIRBORNE) .48,.36** · Josedeodo .43,.73 (al límite) · Yeon .53,.28 · CoreJJ .56,.30 · Quid .55,.50 · Tarzan .33,.47 · Hope .30,.33 · Kael .24,.33 · Shanks .22,.66 |
| j2 | 22,5 | 17:11 | 0-39,7 | Breathe .45,.42 · Yeon .52,.35 · CoreJJ .57,.44 · Quid .54,.53 · Josedeodo .45,.70 · Tarzan .29,.56 · Hope .28,.31 · Kael .18,.37 · Shanks .21,.74 · Morgan: etiqueta .66,.78, pies bajo HUD |
| j2 | 24,5 | 17:13 | 0-39,7 | Josedeodo (SUPPRESSED + SILENCED) .40,.52 (media) · Tarzan .33,.55 · Quid (CHANNELING) .52,.62 · Yeon .54,.38 · CoreJJ .59,.52 · Hope .27,.36 · Kael .21,.47 · Shanks .17,.70 |
| j2 | 27,5 | 17:16 | 0-39,7 | Josedeodo (vida muy baja) .63,.40 · Morgan .51,.54 · Tarzan .43,.56 · Hope .39,.42 · Kael .30,.27 · Shanks .35,.67 · Yeon .55,.34 · CoreJJ .69,.55 · Breathe ya muerto (banner) |
**Ruta medida (misma toma, j2):** Breathe t 20,5 (.42,.57) → t 21,5 (.48,.36) → t 22,5 (.45,.42) = la patada lo saca de su lado hacia TL. La cámara se mueve poco entre 20,5 y 22,5 (Shanks .24,.64 → .22,.66 → .21,.74): compensar con `cam_al_j2.json`. j1: Morgan y Josedeodo cambian de toma entre 23,5 y 26,4 (salto de cámara 25,3-25,6): sin ruta directa.
**Cortes de cámara** (`cam_al_j1.json`, `cam_al_j2.json`): j1 25,3-25,6 (salto rápido) · 38,3 · 52,1 · 57,4 · 68,7 · 77,6-78,8 (entra la repetición) · 98,5-98,9 · 101,2 · 103,3-103,5 · ~111-114 (público) · 114,8. j2 39,7 · 55,2 · 66,7-67,9 (entra la repetición) · 103,4 · 104,2 · 119,5.

## Candidatos
- **MVP de la partida: Morgan**, Camille 7/1/6, 16,3 K de oro, 27,7 % del daño de TL; abre J1 con la ulti sobre Hope y remata a Breathe en J2. Narrador al cierre (VOD 2324): «[Morgan] y [Josedeodo] sacan ventaja del juego temprano».
- **Josedeodo:** 3/0/8, primera sangre, el último asesinato del ACE y la patada de J2; solo 11,8 % del daño (su papel es control). Tarzan 0/3/5 con KP 100 %: estuvo en las 5 de AL sin matar a nadie.
- **Peor de AL: Hope**, Yunara 0/4/2, 40 % KP; narrador: «[Hope] no puede jugar esta partida» (VOD 2113).

## ⚠ Sin verificar o con matiz
- **«El abuelo / el octogenario lo patea»** (J2, VOD 1349-1351): el narrador no dice el nombre en esa frase; que la patada sea de Josedeodo lo dicen el análisis («después de una jugada de Insec… eso fuerza que [Josedeodo] tenga que salir muy herido») y el cuadro (AIRBORNE de Breathe a su lado). No repetir el apodo.
- **Dirección de la patada en J1:** el cuadro da a Hope «AIRBORNE» junto a Josedeodo a las 28:42 y el narrador dice «furia del dragón»; hacia dónde la manda no se ve con claridad. No decir «insec» en J1; sí en J2 (lo dice el narrador).
- **AIRBORNE de Yeon y CoreJJ (j1 t 28,5):** identificados por el nivel de la barra (15 y 12), no por el campeón.
- **Quién SUPPRIME a Josedeodo (j2 t 24,5):** se deduce que es la ulti de Skarner (Tarzan al lado); nadie lo dice.
- **Barón 1 (~24:22):** sin banner leído; sale del feed y del contador de reaparición. Antes de darlo en la voz, leerlo en otro cuadro o decir «minuto 24».
- **Muertes de 23:38-23:47 y del final:** relojes del feed − 4 (±2 s), sin cuadro.
- **Tarjeta «7W-9L» de Lee Sin:** cifra de la transmisión sin ámbito escrito; si va a la voz, atribuirla.
- **Bloqueos:** solo Qiyana (por el narrador). El resto no leído.
- **Desfase de las repeticiones:** aproximado; para pausar en la repetición, medir el cuadro.
- **VOD inglés Q28aQ_pETPE:** es la serie completa (5787 s); NO calibrado.
