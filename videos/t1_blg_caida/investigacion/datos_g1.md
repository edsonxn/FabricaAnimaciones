# G1 — Semifinal BLG vs T1, partida 1: los tres momentos que la deciden — datos verificados (investigado el 17-nov-2026)
Partida: gameId 115660540726095122 (`feed_122.txt`, `stats_g1.json`). **BLG azul (izquierda del HUD), T1 rojo.** BLG gana 18-6.
Campeones: BLG Bin K'Sante · Xun Naafiri · Knight Orianna · Viper Corki · ON Nautilus — T1 Doran Rumble · Oner Nocturne · Faker Locke · Peyz Xayah · Keria Rakan.
Fuentes: cuadros 1080p (marcador, rótulos centrales «X has slain Y», kill feed de la derecha, panel de inhibidores abajo a la izquierda), subtítulos automáticos es (`subs/bt2sO3ioJJ4.es.vtt`; escriben Knight = «Night/Nike», Xun = «Shun», Peyz = «Pace», Oner = «Honer/One», Keria = «Kia», T1 = «Tiwan/Tigan/TW One», BLG = «VLG/PLG/Billy Billy», Orianna = «Oliana/Lauriana», Naafiri = «Anafiri/la Nafiri»; corregidos al citar).

## Reloj (MEDIDO en cuadros) — en la voz SIEMPRE el HUD
| VOD es-MX | VOD = HUD + | Cuadros de control | feed − HUD |
|---|---|---|---|
| bt2sO3ioJJ4 | **509** (±1) | VOD 1425 = 15:17 · 1729 = 20:20 · 1924 = 23:36 · 2267 = 29:18 (ya medido en `datos_relleno.md`) | **+5/+6** (Peyz→Bin rótulo 15:37 ↔ feed 15:43 · Barón 21:00 ↔ 21:06 · Knight→Doran 21:17 ↔ 21:23 · Faker→ON 23:53 ↔ 23:59 · Faker→Xun 24:34 ↔ 24:40) |

Sin pausas entre 15:17 y 24:47 en los tramos cortados (el reloj corre seguido). El feed va **5-6 s adelantado**: todos los tiempos de abajo son del HUD.

## Fuentes cortadas (`medios/_fuente/`)
| Archivo | VOD | Duración | **K_fuente** (HUD = t + K) | Qué cubre |
|---|---|---|---|---|
| `g1_j1.mp4` | 1425 → 1480 | 55 s | **917** (t=0 → 15:17 · t=26 → 15:43 · t=41 → 15:58) | robo del Heraldo + pelea 1 (en vivo hasta t≈41; t≈42-43 transición; t≥44 REPETICIÓN del robo, sin HUD) |
| `g1_j2.mp4` | 1729 → 1809 | 80 s | **1220** (t=0 → 20:20 · t=39 → 21:00 · t=72 → 21:33; ±1) | Viper mata a Oner, Barón de BLG, muerte de Doran, torre superior de T1. Todo en vivo |
| `g1_j3.mp4` | 1924 → 2009 | 85 s | **1416** (t=0 → 23:36 · t=17 → 23:53 · t=58 → 24:34) | asedio con Barón en la base de T1, pelea 23:53-24:22, Faker cierra con el shutdown a Xun (24:34). Todo en vivo |

Cortadas con `yt-dlp --download-sections` (H.264 1080p + audio es-MX); `cortar.py` falló con este VOD (el formato `mp4` ≤1080 que elige es AV1).

---
## Momento 1 — El robo del Heraldo y la primera gran pelea (15:17-15:58)
**Contexto (narración, VOD 1396-1401 ≈ 14:47-14:52):** Faker acaba de matar a ON («la paranoia… lograrían atrapar al Nautilus, un asesinato para Locke»). BLG ya tiene la primera torre (carril superior).

### Marcador
| HUD | Asesinatos BLG-T1 | Oro BLG / T1 | Torres BLG-T1 | Dragones BLG-T1 | Larvas BLG-T1 |
|---|---|---|---|---|---|
| 15:17 | 1-2 | 27,2K / 26,7K (BLG +0,5K) | 1-0 | hextech – nube (1-1) | 3-0 |
| 15:58 | **4-3** | 29,9K / 28,2K (BLG **+1,7K**) | 1-0 | 1-1 | 3-0 |

### Paso a paso (t en `g1_j1.mp4`; HUD = t + 917)
| t | HUD | Qué se ve |
|---|---|---|
| 0-3 | 15:17-15:20 | Foso del Heraldo (río superior). **Faker** pegándole al Heraldo (vida 5128 → 1696); Xun asomado por la izquierda; Bin, Knight cerca; Keria, Doran, Peyz y Oner alrededor del foso |
| 4 | **15:21** | **«Blue team has stolen the Rift Herald!»**: Xun (Naafiri) se lo roba a T1. Bin en medio de T1 (Oner, Doran, Keria, Peyz), Faker arriba |
| 9-17 | 15:26-15:34 | Pelea alargada en la boca del foso: Bin «UNSTOPPABLE» se mete contra Faker; Doran, Keria, Oner y Peyz frente a Knight y Xun |
| 18 | 15:35 | Llegan **ON y Viper** por abajo; Bin muy bajo arriba junto a Doran, Peyz en medio, Keria al foso |
| 20 | **15:37** | **«T1 Peyz has slain BLG Bin!»** (1-3) |
| 22-23 | 15:39-15:40 | Xun «AIRBORNE» en el centro con Viper; **el marcador salta a 3-3 a las 15:40**: caen Peyz y Faker casi a la vez |
| 23 | 15:40 | **«BLG Viper has slain T1 Peyz!»** (Corki → Xayah) |
| 26 | 15:43 | **«BLG Knight has slain T1 Faker!»** (el rótulo va en cola: la muerte ya contaba en el 3-3 de 15:40) |
| 27-30 | 15:44-15:47 | BLG persigue a Doran hacia la torre exterior central de T1 (oleada roja y torre a la derecha) |
| 31 | **15:48** | **«DOUBLE KILL!» de Knight** (Orianna → Rumble = Doran), río superior hacia el lado de T1; 4-3 a las 15:49 (+1,6K) |
| 36-41 | 15:53-15:58 | BLG junto a la torre exterior central de T1; sigue 4-3 |
| 44-54 | — | REPETICIÓN del robo del Heraldo (sin HUD) |

**Muertes (HUD):** Bin 15:37 (Peyz) · Peyz ≈15:40 (Viper) · Faker ≈15:40 (Knight) · Doran 15:48 (Knight). Pelea 3 por 1 para BLG; Knight hace 2.
**Lo que NO se ve en los cortes:** la caída de la torre exterior central de T1 (la narración la anticipa; el feed la da como 2.ª torre de BLG a las 16:50 del feed ≈ 16:44-16:45 HUD).

### Narración (VOD = HUD + 509; subtítulos ±2 s)
- VOD 1418-1430 (≈15:09-15:21): «Xun está cerca para intentar llevarse a Keria… lo que quiere es el Heraldo de la Grieta… Son cuatro contra cinco… ¡Se lo roba! ¡Se lo roba! Está enfermo».
- VOD 1441-1456 (≈15:32-15:47): «Doran se pone caliente… entra la pelea grupal… alcanzada con la onda de choque… ahí está el doble asesinato».
- VOD 1460-1465: «Te lo adelantaba: es un pecado dejarle a Knight la Orianna, y vaya que la hace rendir al máximo».
- Repetición VOD 1470-1492: «T1 ve a Xun en todo momento… Aparece Bin para marcar esa zona, le da el espacio perfecto a Xun… Oner se emociona o se pone nervioso: smitea muy temprano y termina haciéndolo Xun».
- VOD 1497-1520: «Peyz… termina tirando el destello… ahí ya gastaste mucho, y es ahí donde BLG dice: “Listo, podemos ir hacia adelante”. Se combinan Xun con la onda de choque, ese es el combo… Orianna junto con Naafiri lo destrozan… y también Doran termina cayendo, y esta torreta del carril central también es historia».

---
## Momento 2 — Pick a Oner y el Barón de BLG (20:20-21:38)
### Marcador
| HUD | Asesinatos BLG-T1 | Oro BLG / T1 | Torres BLG-T1 | Dragones BLG-T1 | Nota |
|---|---|---|---|---|---|
| 20:20 | 4-3 | 37,9K / 34,6K (BLG +3,3K) | 3-1 | hextech + infernal – nube (2-1) | |
| 20:29 | 5-3 | 38,5K / 34,7K (+3,8K) | 3-1 | 2-1 | tras caer Oner |
| 21:02 | 5-3 | 39,8K / 35,2K (**+4,6K**) | 3-1 | 2-1 | tras el Barón |
| 21:18 | 6-3 | 40,6K / 35,5K (+5,1K) | 3-1 | 2-1 | tras caer Doran |
| 21:34 | 6-3 | 41,4K / 35,8K (**+5,6-5,8K**) | **4**-1 | 2-1 | cae una torre de T1 (carril superior) |

### Paso a paso (t en `g1_j2.mp4`; HUD = t + 1220)
| t | HUD | Qué se ve |
|---|---|---|
| 0-3 | 20:20-20:24 | Peyz y Keria en el carril superior, junto a la torre exterior superior de T1 (minimapa: arriba al centro) |
| 4 | 20:25 | **Oner** (Nocturne) se tira sobre un BLG «UNSTOPPABLE» de nivel 14 (Bin) en la jungla/río superior; Viper y ON debajo |
| 6-8 | 20:26-20:28 | **«BLG Viper is on a killing spree!»** (Corki → Nocturne): Viper mata a **Oner**; Bin en medio, Peyz y Keria se retiran bajo su torre. 5-3 a las 20:28 |
| 12 | 20:32 | «Objective Bounties are available soon» |
| 14 | **20:35** | **BLG empieza el Barón** con Xun, Viper, ON y Knight en el foso (vida 17 801 a las 20:36); un T1 de nivel 12 «CHANNELING» en el río, a la izquierda del foso |
| 22-29 | 20:42-20:50 | Doran y Keria entran por arriba del foso (lado del carril superior); **Bin** los frena delante del foso; Faker en el río a la izquierda; el Barón a 7 713 de vida (20:50) |
| 30-38 | 20:50-20:59 | Bin presiona a Doran y Keria, que se van hacia la torre superior de T1 (Doran gasta el destello según la narración) |
| 39 | **21:00** | **«Blue team has slain Baron Nashor!»** — nadie de T1 lo disputa; BLG +4,6K a las 21:02 |
| 44-50 | 21:04-21:10 | Con el Barón (BARON POWERPLAY desde ≈21:05; a las 21:14 lleva +878 de oro y le quedan 2:44), Bin y Knight empujan con la oleada hacia la torre superior de T1; Doran, Keria y Faker delante |
| 53-54 | 21:14 | Doran **«STUNNED»** (lo atrapa Bin), Keria al lado, Faker abajo |
| 56 | **21:17** | **«BLG Knight is on a killing spree!»** (Orianna → Rumble): cae **Doran**. 6-3 a las 21:18 |
| 72-74 | **21:33** | **«Red turret destroyed!»** — BLG tira la torre (carril superior) de T1: torres 4-1 |

**Muertes (HUD):** Oner 20:27 (Viper) · Doran 21:17 (Knight). **Barón: 20:35 → 21:00, sin disputa.**
**Cómo consigue BLG el Barón (visto + narrado):** BLG mata a Oner (el jungla, el único con castigo para disputarlo) a las 20:27 y a los 8 s ya está en el foso. Bin se queda delante del foso, frena a Doran y Keria cuando llegan por arriba y Doran gasta el destello; T1, con 4, sin jungla y sin destello de Doran, no entra. Barón limpio a las 21:00 y Doran muere 17 s después.

### Narración (VOD = HUD + 509)
- VOD 1712-1736 (≈20:23-20:27): «Peyz, ¿qué acaba de hacer?… Ahí está Oner, quiere atraparlo pero está bajo la torre… se adelanta demasiado… cuatro contra cinco… Oner se quiere salvar, pero Bin va corriendo como un bólido… lo derriban, y estos son 3000 de oro a favor de BLG».
- VOD 1738-1750: «Es el mismo T1 el que muerde el anzuelo… porque Xun tiene maneras de hacerse invulnerable por unos segundos, y eso le permite a Viper iniciar las hostilidades».
- VOD 1755-1763 (≈20:46-20:54): «Cuidado con Faker. Ahí está Faker, ahí está Doran. No lo han visto, no lo han visto… ¡tiene que utilizar el destello Doran! No puede ser».
- VOD 1764-1771 (≈20:55-21:02): «Se metieron en el lugar equivocado. Lo atraparon y no van a poder pelear sin destello de Doran. **Esto es un objetivo gratuito para los jugadores de BLG**».
- VOD 1780-1785 (≈21:11-21:16): «Ahora sí se le tiran, le echan los perros… tiene que escapar… Doran va a morir».
- VOD 1786-1798: «Esto ya me parece que está acabado a favor de BLG esta primera partida… era muy difícil la composición».

---
## Momento 3 — El inhibidor y la pelea en la base de T1 (23:02 → 24:47)
### El inhibidor (verificado en un corte de apoyo, VOD 1885-1925, no guardado en `_fuente`; HUD = t + 1377)
| HUD | Qué se ve | Marcador |
|---|---|---|
| 22:57 | BLG en la base de T1, lado del carril inferior; Oner, Keria y Doran defienden | 6-3 · 45,2K / 39,7K (+5,5K) · torres 6-2 |
| **23:02** | **«Red turret destroyed!»**: cae la torre del inhibidor inferior de T1 | torres 7-3 a las 23:03 (T1 tira a la vez una torre de BLG: rótulo «Blue turret destroyed!» en cola a las 23:09) |
| 23:06 | «An Objective Bounty has been claimed!» (lo cobra T1) | 6-3 · +4,8K |
| **23:15** | **«BLG ON has destroyed a red inhibitor!»** — el inhibidor inferior de T1 | 6-3 · 46,0K / 41,1K (+4,9K) · torres 7-3 |

Confirmación: a las 23:36 el panel de T1 (abajo a la izquierda) marca el inhibidor inferior con reaparición en 04:38 (5:00 − 0:21). Feed: 23:21 (+6 s).


### Marcador
| HUD | Asesinatos BLG-T1 | Oro BLG / T1 | Torres BLG-T1 | Dragones | Nota |
|---|---|---|---|---|---|
| 23:36 | 6-3 | 46,5K / 41,7K (BLG +4,8K) | 7-3 | 2-1 | BARON POWERPLAY de BLG, 0:23 restantes (+1071 de oro); inhibidor inferior de T1 caído |
| 23:49 | 8 torres | 47,0K / 42,0K (+5,0K) | **8**-3 | 2-1 | «Red turret destroyed!» a las 23:47 |
| 24:20 | **10-4** | 49,5K / 43,1K (+6,4K) | 8-3 | 2-1 | |
| 24:35 | **10-5** | 49,8K / 44,2K (+5,6K) | 8-3 | 2-1 | shutdown de Faker a Xun (+1K para T1) |
| 24:47 | 10-5 | 49,9K / 44,5K (+5,4K) | 8-3 | 2-1 | |

### Paso a paso (t en `g1_j3.mp4`; HUD = t + 1416)
| t | HUD | Qué se ve |
|---|---|---|
| 0 | 23:36 | Los 10 en la base de T1 (minimapa: esquina superior derecha, entre la entrada del carril central y el carril inferior). BLG en bloque a la izquierda (Knight, ON, Viper, Bin, Xun), T1 detrás de su muro (Peyz, Doran, Faker) |
| 0-10 | 23:36-23:46 | Oner, Peyz y Doran defienden bajo la torre; Keria a la izquierda |
| 11-13 | **23:47** | **«Red turret destroyed!»**: BLG tira otra torre de la base de T1 (8 torres a las 23:49) |
| 17 | **23:53** | **«T1 Faker has slain BLG ON!»** (6-4 a las 23:54): ON entra primero y cae; varios BLG «NEARSIGHTED» (paranoia de Nocturne) |
| 20 | **23:56** | **«BLG Xun has slain T1 Oner!»** (7-4 a las 23:57); Keria «CHARMED» |
| 24-38 | 24:00-24:14 | T1 (Faker, Keria, Peyz, Doran) se repliega hacia su base; BLG los persigue hacia la torre |
| 39 | **24:15** | **«BLG Knight is on a rampage!»** (Orianna → Rakan = **Keria**); 8-4 |
| 41 | 24:17 | Doran «STUNNED», Faker «UNSTOPPABLE» |
| 43 | **24:19** | **«BLG Bin has slain T1 Doran!»**; marcador **10-4 a las 24:20**: también cae **Peyz** |
| 46 | 24:22 | **«BLG Viper is on a rampage!»** (Corki → Xayah = Peyz) |
| 49-57 | 24:25-24:33 | Bin y Xun persiguen a **Faker** por la jungla hacia el río superior |
| 58 | **24:34** | **«SHUT DOWN!»** (Locke → Naafiri): **Faker mata a Xun** en el río superior; 10-5 a las 24:35 |
| 61-71 | 24:37-24:47 | Faker se escapa por el foso del Barón; Knight y Bin lo buscan; sigue 10-5 |

**Muertes (HUD):** ON 23:53 (Faker) · Oner 23:56 (Xun) · Keria 24:15 (Knight) · Doran 24:19 (Bin) · Peyz ≈24:20 (Viper) · Xun 24:34 (Faker). Pelea: **BLG 4 por 2**; T1 se queda sin 4 de sus 5 en 27 s.

### Narración (VOD = HUD + 509)
- VOD 1893-1906 (≈23:04-23:17): «En el carril inferior la torre va cayendo. El inhibidor es el próximo objetivo, y no hay nadie que pueda defender porque no hay limpieza de oleadas… La defensa es casi imposible».
- VOD 1910-1929: «Con el Barón, ve cómo les pega ese minion cañón… no se puede ni siquiera acercar… no puede hacer absolutamente nada T1, es cuestión de tiempo».
- VOD 1935-1952 (≈23:46-24:03): «Quieren atrapar a Peyz… Oner le pone el escudo antihechizos… llega una definitiva, atrapan a uno… Oner va a caer en las manos del mordisco de la Naafiri… Faker tiene que escapar… son cuatro contra cuatro».
- VOD 1955-1959: «Esta pelea beneficia a los chicos de T1 porque pueden defender…».
- VOD 1966-1973 (≈24:17-24:24): «¡Excelente definitiva! Le dan vuelta al marcador, le dan vuelta a la pelea. Los chicos de BLG están más enfocados que nunca».
- VOD 1977-1990 (≈24:28-24:41): «Cuidado con Xun… Lo van a atrapar… y se lo lleva. Shutdown en el uno contra uno. **Se confió demasiado la Naafiri**».
- VOD 2004-2010: «Se les fue Faker… es una gran jugada por lo menos para un poquito más de tiempo».
- Repetición VOD 2013-2040: «Inicia ON, que va hacia adelante, y T1 dice: “Bueno, listo, es el momento”… desaparecen a ON… el resto del equipo se queda con Xun y con Bin, y ahí es donde no se pueden dar vuelta… Knight y Viper están muy bajos y no tienen maná: es el momento indicado para Faker. Keria va a intentar entrar, pero no tiene aguante».
- VOD 2049-2056: «Intentan ir por Faker… sí podían acabar… y no lo podían atrapar».
- VOD 2062-2064: «Una ventaja grandísima… ¿cuántos son? 4700 de oro» (⚠ el HUD dice +5,4K a las 24:47; la cifra del narrador no cuadra con el marcador: no usarla).

---
## Pendiente / no verificado
- **Torre exterior central de T1 tras la pelea 1:** no está en `g1_j1.mp4` (el VOD pasa a la repetición a las 15:58); solo la narración y el feed (16:50 feed ≈ 16:44 HUD). Si el guion la nombra con hora, cortar VOD ≈1525-1545.
- **Quién gasta el destello en el Barón:** la narración dice que es Doran (20:50-20:54); en los cuadros a 1 fps no se distingue el destello. El resto (Bin delante del foso frenando a Doran y Keria, T1 sin disputar) sí se ve.
- **Faker en el Barón:** un T1 de nivel 12 «CHANNELING» en el río junto al foso (20:35 y 21:00); a las 20:50 ese punto lo ocupa «T1 Faker», pero no se ve qué canaliza.
- **Torre de las 23:47:** «Red turret destroyed!» en la base de T1 (8.ª de BLG), sin rótulo de qué carril; en el minimapa la pelea está entre la entrada central y el carril inferior de T1.
- **«4700 de oro»** (narrador, VOD 2064): el HUD marca +5,4K; no usar.
- Posiciones exactas de los 10 en el minimapa: no se extrajeron pistas (solo descripción por cuadros).
