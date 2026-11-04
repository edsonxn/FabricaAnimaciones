# Banjo-Tooie «50 secretos»: verificación en cuadro, fuentes especiales y catálogo de tomas por frase

Fecha: 3-nov-2026. Serie principal: Ninbanyan «Banjo-Tooie Nintendo Switch Online - 100 % Walkthrough Part NN» (N64 vía NSO, 1080p60, sin narrador). Los ids de las 44 partes están en `tomas_frases.json` → `FUENTES` (P01…P44; las partes P43 `nYp4R7uiguw` y P44 `UhOTPmJTqq8` son nuevas respecto al catálogo de bt_mundos_ranking). Hojas de contacto propias a 360p con el segundo impreso (una cada 2-40 s según la zona) y, para leer texto, cuadros sueltos a 720p/1080p (`yt-dlp -g` + `ffmpeg -ss`). Las evidencias clave están en `previews/verif_secretos/`.

**Avisos de la serie (válidos para todas las tomas):**
- **P01 de 0 a 878 s es 4:3 con marco NSO** (la intro: póker, Hag 1, casa destruida): `recorte_por` ≈ 0,144 por lado. De 878 s en adelante es widescreen sin marco. El resto de las partes, widescreen sin marco (`recorte_por` vacío).
- **Cartel esporádico «Subscribe to my channel… thanks pals!»** arriba a la derecha (visto en P27 ~450 s y P44 a partir de 1978 s): comprobar cada clip con `medir_brillo` + hoja antes de renderizar.
- Menús de pausa/destinos a evitar (vistos): P01 25 s y 895-955 s; P03 190-205 y 225-235 s; P18 448 s; P10 685 s; P11 200 s; P21 177 s; P37 601 y 684 s; P43 575 y 700 s; P25 200 s.
- Las tomas son un cuadro visto en la hoja: **los ~8 s siguientes no están verificados cuadro a cuadro**. Un clip `desde` en cualquier zona con rótulo de zona puede traer un fundido a negro cerca.

## TAREA 1 — Verificaciones en cuadro

| # | Dato | Estado | Qué se ve en realidad (texto leído) | Fuente · segundo | Propuesta para la frase (no se editó guion.py) |
|---|---|---|---|---|---|
| a | S25 letrero «Cauldron Keep Secret Exit» a la derecha de la entrada | ✅ visto | Letrero de peligro amarillo-negro con el texto exacto **«CAULDRON KEEP / SECRET EXIT»**, a la DERECHA del hueco metálico de la entrada y pegado a un pilar dorado de Jiggy (leído a 1080p). Banjo cruza la plataforma verde y entra por ese hueco. | P43 `nYp4R7uiguw` · 636-642 s (nítido 639-641); rótulo de zona «Cauldron Keep» a los 648 s | Se puede mantener tal cual; añadir «un letrero de peligro» y empezar el clip en 636 s. |
| b | S29 placa «GB» detrás de la Hag 1 y «V10» en la pelea final | ✅ placa · ? V10 | Placa amarilla con **«HAG 1»** y un óvalo blanco **«GB»** a la derecha, entre dos luces rojas traseras (leída a 1080p). Sale en el rótulo-intro de la pelea final (zoom por detrás). «V10»: **no lo leí** (barrí 700-1790 s cada 40 s y 746-830 s cada 4 s: solo salen «After two years… revenge time!», «Answer correctly…», «How do I switch them all on?»). La pregunta de la matrícula no salió en las rondas del concurso que vi. | P44 `UhOTPmJTqq8` · placa 762-770 s (nítido 766-769); rótulo «Hag 1 – Monstrous Mechanical Mud-Muncher» 754 s | Dejar la matrícula (✅). Cambiar «V10» y «te pregunta qué pone en la matrícula» por «según la wiki, Grunty presume de motor V10, y una pregunta del concurso trata de la matrícula», o quitarlo. |
| c | S18 línea exacta de Kazooie a Loggo en N64 con «Mario» | ? no encontrado | Solo salió la PRIMERA conversación con Loggo (el váter parlante, Banjo lleva a Kazooie dragón en la mochila): «Hey there, Banjo» → «Well, Grunty ripped me ou[t]…» → «…someone thought it funny to fill me full of paper. I really need unblocking, if you wouldn't mind…» → al desatascarlo «Yep, I can feel a movement in my U-bend!» → «It's a Cheato book page!». **No apareció ninguna línea de fontanero ni de Mario** en 1150-1250 s ni en el resto de Workers' Quarters (1006-1150, 1250-1330). | P27 `-5xyL3uwvUM` · 1162-1216 s (Loggo); sin línea de Mario | Atribuir: «según la wiki, si le hablas otra vez, Kazooie le aconseja llamar a un fontanero; en N64 dice Mario, en Xbox ‘ese famoso italiano’» y enseñar a Loggo (1162-1197). No decir «lo ves». |
| d | S42 plano de las cartas de Banjo: papel tapiz de flores amarillas vs rombos | ❌ no es así | Mirado a 1080p en 281, 286, 376 y 396 s: las **cortinas** azules con dibujo amarillo (rombos / puntos) son las mismas en todos los planos de la mesa; detrás de Banjo la pared es de **madera lisa amarillenta** con cuadros y el reloj de cuco. No hay ningún plano en que cambie un papel de rombos por flores. El cambio, si existe en el modelo (solo lo da TCRF), no se aprecia. | P01 `ezvZQneGzTo` · 281, 286, 376, 396 s (hojas `m_s42b.jpg`) | Reescribir sin «se ve»: «según The Cutting Room Floor, el modelo de la casa esconde una copia de la del primer juego con papel de flores amarillas; en pantalla ni se nota». Imagen: planos de póker 286 y 376 s. |
| e | S38 sombra de pájaro de Dragon Kazooie | ? no confirmado | Kazooie dragón es **verde y va a la espalda de Banjo** (no vuela sola) y lanza fuego. A 1080p la sombra bajo Banjo+dragón es una mancha oscura sin forma de pájaro reconocible. No pude leer ni «retrato que no cambia» ni los colores invertidos en cuadro. | P21 `0Q1upbZH0vs` · 159-171 s (dragón con fuego en Isle O' Hags); sombra a 165 y 169 s | Atribuir a los fans / wiki («según la wiki, su sombra sigue siendo la de un pájaro») o quitar la frase de la sombra; el dragón se enseña a 159-171 s. |
| f | S27 frase de Jiggywiggy de «otra fuerza» | ? no hay clip | No aparece en Ninbanyan (la serie no usa el truco de abrir mundos con Cheato antes de hablar con Jiggywiggy). Búsquedas de YouTube sin resultado útil. Sí hay material del templo y del rompecabezas. | Sin fuente · templo: P11 50 s, P21 200 s; puzzles P21 220-300 s | Decirlo como «según la wiki» y poner el templo/rompecabezas; la frase exacta no se lee. |
| g | S36 «EEKUM BOKUM» en un Mumbo Pad | ✅ visto | En el borde biselado del disco morado octogonal (con la calavera de Mumbo) se lee **«…KUM · BOKUM»**; la «EE» inicial queda tapada por la perspectiva en 884 s y se ve «ЭRKUM» en 892 s. Detrás, la estatua dorada de Mumbo. | P03 `5PjYuSAZBJQ` · 884-900 s (1080p en `m_mp.jpg`) | Mantener; decir «en el borde del pad está escrito Eekum Bokum». |
| h | S21 abucheos cuando Banjo acierta | ? no verificable por imagen | No hay subtítulo de sonido. Whisper no transcribe nada del tramo 925-1010 s (voces de juego, sin letras). En el concurso salen: «Some loser bear» sobre Banjo (992 s) y Grunty «…ms, err… I mean contestant's, shall…» (972 s, confirma la frase «víctimas… concursantes»). Los abucheos solo los confirma el oído / la wiki. | P43 · 932-1000 s (intro y primeras rondas) | Comprobar a oído el tramo antes del render (marcado AUDIO); si no se oyen, decir «según la wiki, el público abuchea». |

Datos extra vistos que sirven al guion: Banjo-Threeie confirmado en texto («Just you wait until Banjo-Thr[eeie]», P44 1962-1964 s); la patada a la cabeza («Ooh, I think he[r eye…]», P44 1954 s); créditos del juego «The Banjo-Tooie Team… Grant ‘Old King Coal’ Kirkhope» (P43 1770-1790 s, solo si la voz nombra al equipo); la pregunta de las mochilas «Snack Pack / Sack Pack / Shack Pack» (P43 1620 s); Sabreman dormido «ZZZ… perhaps I'll ride on a do[lphin]» (P37 664 s ✅ para S47); «This is a warp pad» (P03 1256 s ✅ para S11).

## TAREA 2 — Fuentes especiales (YouTube)

Resolución = mayor `height` real que ofrece yt-dlp. Todos los segundos fueron vistos en cuadro (un agente aparte los buscó; los revisé).

| n.º | Fuente | Id · canal | Alto | Segundo(s) | Qué se ve | Avisos |
|---|---|---|---|---|---|---|
| 1 | Final JAPONÉS con el saco (clave `SACO`) | `feFsFAWJznY` · Censored Gaming (154 s) | 1080 | japonés: saco cae 68-69, Banjo lo sostiene 70-71, ojo en el suelo desde 71 (subtítulo JP 72); occidental: cabeza rueda 104-105, ojo 107, texto «OOOH, I THINK HER EYE JUST FELL OUT!» 108-110 | Final de Grunty, las dos versiones seguidas | Etiqueta fija arriba «Japanese/English Version» (cortar con crop), marca CENSORED GAMING abajo-der., anuncio VPN 0-9 s, cuadro blanco ~90 s, caja de Crash 2 a los 80 s. Sin cortes 69-79 y 105-112 s. Crédito al canal. |
| 2 | Trotty japonés sin tercer brazo | NO HALLADO | — | — | — | Ningún video con la versión japonesa en la piscina de JRL (Falcon 100 % japonés pasa por los Swimming Baths a 6300-6720 s sin que salga Trotty). Además, en NSO el cerdo rosa de la laguna se ve con DOS brazos a 1080p (P17 198 y 426 s): el tercer brazo no se puede enseñar. Decirlo «según VGFacts». |
| 3 | Demo SpaceWorld 2000 de GameCube (clave `SPACEWORLD`) | `zSLa5M8juyw` · Adam Doree (53 s) | 1440 falso (VHS) | 0 s Mumbo; 3-4 Kazooie corriendo; 5-6 enjambre; 7-11 multitud de enemigos en cueva; desde 12 s ya es Perfect Dark | Demo técnica de Rare de GameCube | Calidad ~480i borrosa, marca «Kikizo» abajo-der., © 2000 Nintendo/Rare. Gobi y Alphette NO se identifican. El autor aclara que NO es Banjo-Threeie y pide no reutilizar sus cintas sin contexto: dar crédito. Alternativa: su «Ultimate Video» `62O2vFfS_Ok` (3092 s, sin revisar). |
| 4 | Récord de Falcon (claves `FALCON100`, `FALCON_ANY`) | `vesydnvsHEo` (100 % 4:10:46) · `DCkUTe_LIDU` (any% 25:49) · Falcon | 1080 | 100 %: limpio a 4060, 5060, 5200, 6060 s; any%: 30, 140, 250, 470 s | Run en N64 japonés (texto JP en pantalla) | Panel de splits a la izquierda (25 %): `crop=1440:1080:480:0`. Sin webcam. Negros en cambios de zona. |
| 5 | Jamjars dándose con la tapa del silo (clave `JAMJARS_TAPA`) | `5YFszI5v-2k` · Steffu (Breegirl) (12 s) | 720 | «DISMISSED» 7 s; sale despedido 8 s; la tapa le golpea 10-10,5 s; tapa cerrada 11-12 s | Silo de Jamjars, Banjo de espaldas | El clip dura 12 s: desde 6 s quedan 6 s (menos que un beat de 8,6). Sin overlay ni narrador. Alternativa 1080p `G82v9syAEks` (Boinkity C., 11 s) pero con rótulo de NSO y marco 4:3. |
| 6 | Rare Revealed «A Rare Look at Dream» / dinosaurio (clave `DREAM`) | `XItTPJox9CU` · NeoGamer (352 s) | 2160 (ampliado de SNES) | pata gigante entra 50, protagonista aplastado 51; otra a 80-81; otra a 86; otras tomas 10-40, 110-140, 160-230, 240-260 | Dream: Land of Giants (SNES): niño pelirrojo con espada | En `w72kj20YNA0` (Rare Revealed, 1080p) el dinosaurio NO sale y hay entrevistas con CARA: no usarlo. NeoGamer tiene logos de canal desde 340 s. Alternativa limpia: Kawaii Games `POAcxSxauo4`. |
| 7 | Toma AÉREA de Terrydactyland junto al cráneo de Mumbo | NO HALLADA | — | — | — | Revisé Ninbanyan P22-P25 (cada 30 s, y P25 entera cada 40 s), Hawlo `SQuHBrGrjdQ`: solo interiores de cueva. El cráneo de Mumbo de Terrydactyland no sale; el que sale a 1232 s de P03 es el de MAYAHEM. Usar el dibujo de Mayles (Nintendo Life) como pegatina. |
| 8 | Demo acelerada de la pantalla de título en NSO | NO HALLADA | — | Sustituto: P01 `ezvZQneGzTo` pantalla de título 75-110 s | Título NSO limpio, SIN demo acelerada | La fuente (GamesRadar/Nintendo Life) es un video de Bluesky, no de YouTube. Hay que decirlo con MG, o grabar la pantalla de título de NSO a mano. |
| 9a | Dos Banjos (clave `DOS_BANJOS`) | `b7iGKxVuD9M` · Master Dimentio (123 s) | 720 | dos Banjo+Kazooie juntos 58-72 s en el iglú de Boggy; Mrs. Boggy detrás | Hailfire Peaks, lado hielo | Sin overlay ni narrador. El candidato `iAo6TJtvbq4` solo llega a 480p. |
| 9b | GI sin el tren (clave `GI_SIN_TREN`) | `TZCGRAAInmg` · The8bitbeast (9 s, TAS) | 720 | 1-3 s Banjo en plataforma industrial; 9 s ante la puerta de GI | Entrada a GI sin tren | Solo 9 s, con cortes negros/Jiggy a 4-8 s. Otras versiones solo 480p. No se ve el paso desde Hailfire. |
| 10 | Grunty's Lair de Banjo-Kazooie (clave `BK_LAIR`) | `XXnTS2hRWBY` · Ninbanyan (44132 s) | 1080 | entrada 3472-3480; sala de la puerta de 50 notas 3480-3530; sala principal con Brentilda 3544-3570; disco de salto 3668 | Interior de la guarida de BK, sin comentarista | Marco 4:3 con barras laterales (recorte ~0,145). Cartel esporádico «Smash that Like Button» (visto a 2880 s, no en la guarida). Marcar «BK». |
| 11 | Smash Ultimate: huevos de Banjo y Kazooie (claves `SMASH_HUEVOS`, `SMASH_FINAL`) | `bw6h7xAb0pw` · Master0fHyrule (352 s) · `sURaafANZ3o` · Nintendo Wire (14 s) | 1080 | huevos 77-92 s (ráfaga trasera con humo 92); Breegull Blaster 119-125; Final Smash 4-9 s | Smash Ultimate | bw6: etiqueta de texto arriba con el movimiento, HUD de daños abajo, marca MasterOfHyrule; 340 s+ pantalla de suscripción. sUR: subtítulos de descripción de 1 a 8 s. |
| 12 | Versión XBLA: concurso, refrigerador, peluche de DK (clave `XBLA_TOT`) | `HPvvSJ8gTaU` · packattack04082 (1897 s) | 1080 | refrigerador con pegatinas BK/BT/Rare 358-364 s (limpio 360-362); pregunta «Which fridge magnet was farthest right?» 366-370 | Tower of Tragedy XBLA | Sin comentarista. **NO hallé** la pregunta de los «13 botones del mando de Xbox 360», ni el peluche de DK cambiado, ni la casa de Bottles de XBLA. |

## TAREA 3 — Catálogo de tomas por frase (118 frases)

Formato: `(fuente, segundo, qué se ve) [marca]`. Cada frase lleva 2-4 candidatas en orden de preferencia; la **sugerida** es la primera que no choca (≥ 25 s de separación dentro de la misma fuente, ≥ 10 s dentro de la misma escena) con las sugeridas anteriores. Marcas: **AUDIO** = conviene oír el juego; **XBLA/BK/SMASH/DREAM/JP/GC** = material de otra versión o juego, decirlo en voz y rotular; **OJO** = riesgo; **HUECO** = sin toma buena.

### intro
- **intro_0** — «En Japón, Banjo-Tooie tiene otro final. La cabeza de la bruja Gruntilda desaparece, y la cambia…»  → sugerida: `SACO@68`
  - (SACO, 68, japonés: el saco azul/rosa cae y Banjo lo sostiene (70-71); recortar la etiqueta «Japanese Version» de arriba; NO usar 0-10 s (anuncio VPN)) **[JP]**
  - (SACO, 104, occidental: la cabeza de Grunty rueda (104-105) y el ojo cae (107); etiqueta «English Version») **[OJO]**
  - (P44, 1950, versión occidental NSO: Banjo patea la cabeza de Grunty en la azotea (1950-1956))
- **intro_1** — «Hay un cartucho que le pregunta a la consola doscientas sesenta y ocho veces si eres un pirata.…»  → sugerida: `P18@433`
  - (P18, 433, Lord Woo Fak Fak: pez abisal con linterna (jefe con huesos de más))
  - (P22, 750, Terrydactyland: rótulo de zona sobre el camino (el «accidente» de la montaña)) **[OJO]**
  - (P01, 75, título Banjo-Tooie de NSO limpio (para la frase del cartucho; el chip no sale en gameplay: MG))
- **intro_2** — «Ya te contamos su historia, sus Jiggies más crueles y sus ocho mundos. Creías que no quedaba na…»  → sugerida: `P10@1035`
  - (P10, 1035, vista aérea de Isle O' Hags (cielo verde) para «creías que no quedaba nada»)
  - (P02, 1110, Jinjo Village: «Blue Jinjo Family House» (el hub de los Jiggies crueles))
  - (P43, 650, rótulo «Cauldron Keep» al entrar (el mundo que casi no se ve))
- **intro_3** — «Estos son los cincuenta secretos de Banjo-Tooie que ignoraste. Del más curioso al que de verdad…»  → sugerida: `P01@100`
  - (P01, 100, título Banjo-Tooie con Klungo asomando (75-110, sin menús))
  - (P02, 230, rótulo «Isle O' Hags (Jinjo Village)» con Banjo corriendo)
  - (P10, 1335, las casas de colores de Jinjo Village en fila)
### s50
- **s50_0** — «Número cincuenta. Banjo-Tooie da por hecho que ya jugaste el primero. Empiezas en Spiral Mounta…»  → sugerida: `P01@985`
  - (P01, 985, Spiral Mountain: el fantasma de Bottles flota junto a Banjo («Can't you see I am decaying down there?»))
  - (P01, 1045, menú del fantasma de Bottles «Which ability would you like: Basic Movements» (1045-1055))
  - (P01, 1075, Banjo y Kazooie corriendo por Spiral Mountain (tocones, topera) tras el menú)
- **s50_1** — «Steve Malpass, uno de sus diseñadores, lo explicó así: ¿quién iba a empezar una saga por el seg…»  → sugerida: `P01@740`
  - (P01, 740, fantasma de Bottles brillando en el pueblo («It's worse than that…», 740-755))
  - (P01, 1165, vuelo de Kazooie sobre Spiral Mountain (cielo azul))
  - (P01, 1135, Banjo junto a tocones, aprendiendo movimientos)
### s49
- **s49_0** — «Cuarenta y nueve. Cuando llamas al tren Chuffy desde una estación, Old King Coal, el rey que vi…»  → sugerida: `P09@1000`
  - (P09, 1000, estación de Glitter Gulch Mine con vagones y farol (Banjo llegando))
  - (P09, 1120, rótulo «Inside Chuffy's Wagon» dentro del vagón de Chuffy)
  - (P34, 540, Chuffy en la estación de Hailfire Peaks con luz (catálogo anterior; sin ver 8 s)) **[OJO]**
  - (P09, 1380, Old King Coal en la sombra de la caldera («Hurrr»), cuando el tren responde) **[AUDIO]**
- **s49_1** — «Y si lo llamas desde la estación donde ya está, te contesta: ¿estás ciego? ¡Chuffy está justo d…»  → sugerida: `P09@1260`
  - (P09, 1260, Chuffy el tren iluminado de verde delante de Banjo (spell Levitate))
  - (P09, 1240, rótulo «Levitate / Chuffy the Train»)
  - (P34, 570, Chuffy visto de cerca en la estación de lava (catálogo anterior)) **[OJO]**
### s48
- **s48_0** — «Cuarenta y ocho. En los archivos del juego, la animación de disparar huevos hacia delante se ll…»  → sugerida: `P04@144`
  - (P04, 144, Kazooie en primera persona con huevos verdes y marcador (Breegull Blaster; 144-360))
  - (P04, 60, Jamjars y Kazooie en el silo, rótulo «Breegull Blaster» («Here's a move», 60-72))
  - (SMASH_HUEVOS, 77, Smash Ultimate: Banjo y Kazooie disparan huevos (77-92); etiqueta de texto arriba) **[SMASH]**
- **s48_1** — «O sea: huevo culo. Y Japón se lo tomó al pie de la letra: en Smash Ultimate, ese ataque de Banj…»  → sugerida: `SMASH_HUEVOS@92`
  - (SMASH_HUEVOS, 92, Smash Ultimate: ráfaga trasera de huevos con humo (el «huevo del trasero»)) **[SMASH]**
  - (SMASH_HUEVOS, 119, Smash Ultimate: Breegull Blaster mantenido (119-125)) **[SMASH]**
  - (SMASH_FINAL, 4, Smash Ultimate: Final Smash «The Mighty Jinjonator» (4-9)) **[SMASH]**
### s47
- **s47_0** — «Cuarenta y siete. De toda la banda sonora, la canción favorita de Grant Kirkhope, el compositor…»  → sugerida: `P18@40`
  - (P18, 40, Atlantis: columnas y ruinas verdes bajo el agua, Banjo nadando (40-60)) **[AUDIO]**
  - (P18, 10, Atlantis: pez erizo y ruinas (10-20)) **[AUDIO]**
  - (P18, 140, Atlantis: cofres con luz verde (140-150)) **[AUDIO]**
- **s47_1** — «Él mismo dice que resume lo que se siente al bajar ahí. Escúchala un momento.»  → sugerida: `P18@100`
  - (P18, 100, Atlantis: pasillos de ruinas con Banjo nadando (100-110), voz callada) **[AUDIO]**
  - (P18, 60, Atlantis: Banjo sobre la plataforma de ruinas (60)) **[AUDIO]**
  - (P18, 190, Atlantis: fondo marino con Kazooie (190), a punto del rótulo Sea Bottom) **[AUDIO]**
### s46
- **s46_0** — «Cuarenta y seis. Al llegar a Cauldron Keep, la guarida final de la bruja, a la derecha de la en…»  → sugerida: `P43@639`
  - (P43, 639, LETRERO LEÍDO: hazard amarillo-negro «CAULDRON KEEP / SECRET EXIT» a la derecha del hueco de entrada, junto al pilar de Jiggy (639-642))
  - (P43, 648, rótulo «Cauldron Keep» sobre el túnel de entrada)
  - (P43, 636, Banjo cruzando la plataforma verde hacia la entrada (636))
- **s46_1** — «O sea, Banjo y Kazooie asaltan el castillo de la villana entrando por la puerta de atrás. La en…»  → sugerida: `P43@657`
  - (P43, 642, Banjo entra por el hueco metálico (puerta trasera), pilar de Jiggy al lado)
  - (P43, 657, foso de ácido morado alrededor de la torre (657-678))
  - (P43, 666, Banjo en los pads de la plataforma verde con el foso detrás)
### s45
- **s45_0** — «Cuarenta y cinco. En casa de Bottles, en Jinjo Village, su hijo Speccy lleva una gorra con el s…»  → sugerida: `P02@1490`
  - (P02, 1490, Speccy (hijo de Bottles) con su gorra y un avión de juguete (1490-1500))
  - (P02, 1470, Kazooie saluda a Speccy en la casa de Bottles («Hi, Speccy»))
  - (XBLA, 310, XBLA (catálogo anterior): casa de Bottles/Isle en Xbox, para decir que la gorra siguió) **[XBLA]**
- **s45_1** — «Y en la casa cuelgan pósters de Juno y Vela, los héroes de Jet Force Gemini, otro juego de Rare…»  → sugerida: `P02@1525`
  - (P02, 1525, póster con piernas y logo de Rare en la casa de Bottles (primer plano, 1520-1535))
  - (P02, 1415, póster a la derecha del cuadro mientras Banjo habla con Bottles (1410-1420))
  - (P02, 1350, interior de la casa: cuadro de Mrs. Bottles y cama (1350))
- **s45_2** — «Una gorra de Pokémon en un juego de Rare, que siguió ahí incluso en la versión de Xbox, cuando …»  → sugerida: `P02@1430`
  - (P02, 1430, Goggles y el peluche en la misma casa (para no dejar la casa sin imagen))
  - (P02, 1290, Mrs. Bottles «Hello there, Ban…» (1290-1310))
  - (XBLA, 310, XBLA: la misma casa/Isle en la versión de Xbox) **[XBLA]**
### s44
- **s44_0** — «Cuarenta y cuatro. Cuando Banjo va solo y usa su mochila, como el Shack Pack o el Taxi Pack, ha…»  → sugerida: `P43@1620`
  - (P34, 180, Jamjars con Banjo de espaldas con mochila azul-verde (180-195); no es el Shack Pack) **[HUECO]**
  - (P43, 1620, pregunta del concurso «Holding… and pressing… Snack Pack / Sack Pack / Shack Pack» (1620)) **[OJO]**
  - (P07, 360, Jamjars en silo con Kazooie (para el viaje))
- **s44_1** — «Así que, en un cuadro concreto, esa mochila se apaga, y aparece otra idéntica en el mismo sitio…»  → sugerida: `P43@1620`
  - (P34, 195, Banjo con mochila (195): el cambio de mochila no se aprecia a 1080p; MG o cámara lenta propia) **[HUECO]**
  - (P43, 1620, mismo rótulo de pregunta de mochilas) **[OJO]**
### s43
- **s43_0** — «Cuarenta y tres. En el video de los Jiggies te contamos que el nombre de Chris P. Bacon salió d…»  → sugerida: `P07@240`
  - (P07, 240, Bullion Bill (zorro con sombrero) hablando en Prospector's Hut (240-260))
  - (P09, 1420, Old King Coal, cara de lava («Who dares enter Old King Coal's Bo…», 1420-1440))
  - (P01, 420, Grunty y Brentilda (para «la revista dejó bautizar personajes»: sin imagen mejor)) **[OJO]**
- **s43_1** — «Según VGFacts, de ahí salen también Old King Coal, el del tren, y Bullion Bill, el de la cabaña…»  → sugerida: `P09@1440`
  - (P09, 1440, Old King Coal en su caldera (1440))
  - (P07, 220, rótulo «Prospector's Hut» con Banjo (220))
  - (P07, 280, interior de la cabaña de Bullion Bill (280-300))
### s42
- **s42_0** — «Cuarenta y dos. Al entrar en el Gatehouse de Cauldron Keep, Banjo dice que ahí no hay nadie. Y …»  → sugerida: `P43@745`
  - (P43, 745, Banjo y Kazooie llegando al Gatehouse (rótulo «The Gatehouse» a los 755))
  - (P43, 755, rótulo «The Gatehouse» con la sala azul de luces) **[AUDIO]**
  - (P43, 725, Banjo con una hoja de Jiggy en el suelo antes del Gatehouse)
- **s42_1** — «Oh, sí que hay alguien. La música ha cambiado. Cada vez que pasa eso, acabamos peleando. Y en e…»  → sugerida: `P43@770`
  - (P43, 770, Klungo cae por el agujero del techo («Yarrrr», 770-780): cambio a música de jefe) **[AUDIO]**
  - (P43, 785, Klungo en primer plano «Lotsss hasss learnt new…»)
  - (P43, 815, pelea con Klungo en su burbuja (815-830))
### s41
- **s41_0** — «Cuarenta y uno. Una teoría de los fans: el contorno de Isle O' Hags imita el icono de vida de B…»  → sugerida: `P01@1165`
  - (P10, 1035, vista aérea de Isle O' Hags con sus cuevas (cielo verde))
  - (P01, 1165, Kazooie volando sobre la isla (cielo azul))
  - (P02, 230, rótulo «Isle O' Hags (Jinjo Village)»)
- **s41_1** — «Rare nunca lo confirmó. Te lo enseño encima del mapa, y tú decides si es diseño o casualidad.»  → sugerida: `P33@640`
  - (P33, 640, rótulo «Isle O' Hags (Wasteland)» (640))
  - (P43, 515, rótulo «Isle O' Hags (Wooded Hollow)» (515-530))
  - (P38, 1085, rótulo «Gruntilda's Lair (Entrance)» (1085))
### s40
- **s40_0** — «Cuarenta. Los huevos misteriosos del primer juego por fin se abren aquí, en el gallinero de Heg…»  → sugerida: `P03@120`
  - (P03, 120, rótulo «Heggy's Egg Shed» con Heggy la gallina azul (120-140))
  - (P03, 150, huevo amarillo en un nido del gallinero con Banjo (150-180))
  - (P04, 60, Breegull Blaster/Jamjars (para el huevo del Bash; no es el Bash)) **[OJO]**
- **s40_1** — «El azul, un truco de huevos que persiguen a los enemigos. Y el amarillo, un Jinjo jugable en el…»  → sugerida: `P03@250`
  - (P03, 250, Heggy «Cluck! Go find special e[ggs]» (250))
  - (P03, 215, huevo amarillo en el nido (210-240, evita el menú de 190-205 y 225-235)) **[OJO]**
  - (P03, 100, huevos azules en la entrada de Wooded Hollow («…table eggs may be found», 100-110))
### s39
- **s39_0** — «Treinta y nueve. La Hag 1, la perforadora gigante de las brujas, lleva detrás una matrícula con…»  → sugerida: `P44@766`
  - (P44, 766, PLACA LEÍDA: matrícula amarilla «HAG 1» con óvalo «GB», luces rojas (762-770, trasera de la Hag 1))
  - (P44, 754, rótulo «Hag 1 – Monstrous Mechanical Mud-Muncher»)
  - (P44, 758, Hag 1 de lado, luces y orugas)
- **s39_1** — «En la pelea final, Grunty presume de motor: siente la potencia de esa bestia V10. Y en el concu…»  → sugerida: `P44@786`
  - (P44, 786, Grunty en el podio «After two years… revenge time!» (782-790))
  - (P44, 818, Grunty con las tarjetas «Answer correctly and maybe I'll go a little slee[p]» (818-830))
  - (P44, 900, Hag 1 de frente «How do I switch them all on?» (900))
### s38
- **s38_0** — «Treinta y ocho. Todo el juego lo diseñaron solo dos personas: Gregg Mayles y Steve Malpass. Pri…»  → sugerida: `P15@625`
  - (P15, 625, rótulo «Witchyworld – Saucer of Peril Ride» (625) con la cabina del platillo)
  - (P15, 425, plataforma octogonal del platillo con Banjo (425))
  - (P43, 1770, créditos del juego «The Banjo-Tooie Team…» (1770-1790): solo si la voz nombra al equipo) **[OJO]**
- **s38_1** — «Para colocar notas, cámaras y disparadores usaban un editor dentro del propio juego, manejado c…»  → sugerida: `P15@505`
  - (P15, 505, dentro del platillo, vista en primera persona disparando a blancos (505-605))
  - (P15, 545, el parque de noche con luces desde el platillo (545))
  - (P15, 685, Kazooie junto al platillo rosa (685))
### s37
- **s37_0** — «Treinta y siete. Pawno, el usurero de Jolly Roger's Lagoon, viste la ropa del Capitán Cockeye, …»  → sugerida: `P17@805`
  - (P17, 805, Pawno de cerca, sombrero y chaleco «Greetings, frie[nd]» (805))
  - (P17, 745, fachada del «Pawno's Emporium» (745))
  - (P17, 985, Pawno tras el mostrador (985-1015))
- **s37_1** — «Lo contó Ed Bryan, el que diseñó a los personajes. Pawno no te presta nada gratis, pero el traj…»  → sugerida: `P17@820`
  - (P17, 820, Pawno tras el mostrador «…I reckon 20» (820))
  - (P17, 1015, Pawno cuenta monedas (1015))
  - (P17, 910, Jamjars/pedido de dinero en Jolly Roger's (910)) **[OJO]**
### s36
- **s36_0** — «Treinta y seis. En Xbox 360 hasta el examen de la bruja cambió. En Nintendo 64, el concurso pre…»  → sugerida: `P43@1012`
  - (P43, 1012, pregunta de la bruja N64 en pantalla («Which of these is an area in Grunty Industries?») como ejemplo del examen)
  - (P43, 1112, logo «Tower of Tragedy» (1112))
  - (XBLA_TOT, 366, XBLA: pregunta «Which fridge magnet was farthest right?» (366-370)) **[XBLA]**
- **s36_1** — «En Xbox, con Rare ya en Microsoft, la pregunta pasó a ser por el mando de Xbox 360, con trece. …»  → sugerida: `XBLA_TOT@360`
  - (XBLA_TOT, 360, XBLA: refrigerador con pegatinas BK/BT/Rare (358-364) del mismo concurso) **[XBLA]**
  - (P43, 1252, pregunta N64 con tres opciones (1252))
  - (P43, 1432, pregunta N64 «Canary Mary / The Prospector / Guffo» (1432))
### s35
- **s35_0** — «Treinta y cinco. La música de Isle O' Hags es la guarida de Grunty disfrazada. Kirkhope le dio …»  → sugerida: `P38@1085`
  - (P38, 1085, rótulo «Gruntilda's Lair (Entrance)»: entrada de la guarida en Isle O' Hags, con su música (1085-1100)) **[AUDIO]**
  - (P02, 1070, Banjo llegando a Jinjo Village (1070): música de la isla de fondo) **[AUDIO]**
  - (BK_LAIR, 3472, BK: entrada de Grunty's Lair del primer juego (3472-3480)) **[BK]**
- **s35_1** — «Y dice que en Banjo-Tooie no tuvo que rehacer nada: todas fueron sus primeras ideas. Escucha es…»  → sugerida: `BK_LAIR@3544`
  - (BK_LAIR, 3544, BK: sala principal de Grunty's Lair (3544-3570) con su música) **[BK AUDIO]**
  - (P10, 1285, Isle O' Hags: Banjo ante las casas de Jinjo Village (1285)) **[AUDIO]**
  - (P38, 1165, Isle O' Hags: camino hacia Jinjo Village (1165)) **[AUDIO]**
### s34
- **s34_0** — «Treinta y cuatro. En Hailfire Peaks descongelas a Sabreman, el explorador de los primeros juego…»  → sugerida: `P37@496`
  - (P37, 496, Sabreman descongelado en la nieve (496-526))
  - (P37, 631, Banjo y Sabreman en su tienda de lava (628-644))
  - (P37, 571, Sabreman caminando por la nieve (571))
- **s34_1** — «Dolphin, delfín, era el nombre en clave de la GameCube, la consola que Nintendo preparaba ese a…»  → sugerida: `P37@664`
  - (P37, 664, TEXTO LEÍDO: Sabreman dormido «ZZZ… perhaps I'll ride on a do[lphin?]» (664))
  - (P37, 652, su tienda verde sobre la plataforma de lava (652-672))
  - (SPACEWORLD, 0, demo GameCube (la consola «Dolphin»), si se quiere el guiño) **[GC OJO]**
### s33
- **s33_0** — «Treinta y tres. Lo que murmura Mumbo al hacer sus hechizos está escrito en el suelo. En los cos…»  → sugerida: `P03@884`
  - (P03, 884, LETRERO LEÍDO: borde del Mumbo Pad «…KUM · BOKUM» (Eekum Bokum, 884-900, la «E» inicial tapada por la perspectiva)) **[AUDIO]**
  - (P03, 860, estatua dorada de Mumbo sobre pedestal y el disco morado al lado (860))
  - (P09, 1240, rótulo del hechizo «Levitate»: Mumbo conjurando sobre Chuffy (1240-1260)) **[AUDIO]**
- **s33_1** — «Y esa voz no es de un actor: es del propio compositor, Grant Kirkhope.»  → sugerida: `P03@1328`
  - (P03, 1328, Mumbo habla desde su calavera «…so built new skull, Mumbo» (1328))
  - (P03, 1400, Mumbo de pie con su bastón (1400))
  - (P03, 1316, Mumbo en su trono de la calavera (1316))
### s32
- **s32_0** — «Treinta y dos. Rare es un estudio británico, pero Europa fue la última en jugarlo. Salió en Nor…»  → sugerida: `P01@75`
  - (P01, 75, título «Banjo-Tooie © 2000 Nintendo/Rare» limpio (75-110))
  - (P44, 2000, mismo título al final de la parte (2000-2030))
  - (P01, 125, tormenta sobre Spiral Mountain (125-160))
- **s32_1** — «En Japón, además, se llama La gran aventura de Banjo y Kazooie 2.»  → sugerida: `FALCON_ANY@30`
  - (FALCON_ANY, 30, juego en japonés (texto JP en pantalla), recortar el panel izq. con crop=1440:1080:480:0) **[JP]**
  - (P01, 100, título NSO con Klungo (100))
  - (P44, 2020, título con Klungo asomando (2020))
### s31
- **s31_0** — «Treinta y uno. Ya te contamos que el último mundo se recortó. Lo nuevo es cómo era. En los dibu…»  → sugerida: `P43@710`
  - (P43, 680, foso de ácido morado y torre verde de Cauldron Keep (680-700))
  - (P43, 710, Banjo en la cornisa de la torre sobre el foso (710))
  - (P43, 635, muros verdes de Cauldron Keep (635))
- **s31_1** — «Según la wiki del juego, había también una cripta con una fantasma, una armadura embrujada, y u…»  → sugerida: `P43@657`
  - (P43, 657, foso de ácido morado (657-678))
  - (P43, 740, torre con reja metálica sobre el foso (740))
  - (P43, 755, interior del Gatehouse (755): lo que queda del castillo grande)
### s30
- **s30_0** — «Treinta. Jamjars, el hermano militar de Bottles, enseña cada movimiento con una cadencia de mar…»  → sugerida: `P03@1100`
  - (P03, 1100, Jamjars en el silo: «So you'll be wanting t'learn…» (1080-1160)) **[AUDIO]**
  - (P04, 60, Jamjars y Kazooie: «Breegull Blaster – Here's a move» (60-72)) **[AUDIO]**
  - (P34, 180, Jamjars «That'll be all» con botón rojo (180-195)) **[AUDIO]**
- **s30_1** — «Según la wiki, en Xbox el botón de ataque dejó de ser la B, y varias de sus canciones se quedar…»  → sugerida: `P07@360`
  - (P07, 360, Jamjars con el botón verde y Kazooie (360))
  - (P11, 350, Jamjars en silo con luces de Witchyworld (350))
  - (P03, 1140, Jamjars «I see you've got enoug[h]» (1140))
### s29
- **s29_0** — «Veintinueve. En el concurso Tower of Tragedy, el público aplaude a las hermanas de Grunty, y ab…»  → sugerida: `P43@932`
  - (P43, 932, inicio del concurso: Grunty en el podio y Banjo en el pedestal (932-950)) **[AUDIO]**
  - (P43, 992, «Some loser bear» sobre Banjo con el marcador (992)) **[AUDIO]**
  - (P43, 1152, Banjo y una hermana de Grunty junto al podio (1152))
- **s29_1** — «Si nadie acierta, Grunty suelta: estoy rodeada de imbéciles, casi la frase de Scar en El rey le…»  → sugerida: `P43@972`
  - (P43, 972, TEXTO LEÍDO: «…ms, err… I mean contestant's, shall…» (972))
  - (P43, 952, Grunty presentando puntos «with 1 point being awarded if it was a…» (952))
  - (P43, 1192, las pesas de una tonelada del concurso (1192-1212))
### s28
- **s28_0** — «Veintiocho. Kirkhope tuvo que dejar Banjo-Tooie a medias dos veces. Empezó la música, pero le p…»  → sugerida: `P44@90`
  - (P01, 1060, Spiral Mountain (mientras la voz habla de la música): sin toma específica; DK64/Perfect Dark van como pegatina estática) **[HUECO]**
  - (P44, 90, fiesta de los Jinjos «Thanks, guys» (90))
  - (P02, 1070, Banjo entra en Jinjo Village (1070))
- **s28_1** — «Y a mitad del desarrollo, Rare se mudó a su nueva sede, una milla más abajo. Según Kirkhope, to…»  → sugerida: `P29@1050`
  - (P29, 1050, caja «Deliver to Twycross, England» (1050-1054, catálogo anterior, leída ✅))
  - (P27, 610, caja «Defective Goods» con Banjo (610))
  - (P27, 650, letrero «Waste Disposal Plant» (650))
### s27
- **s27_0** — «Veintisiete. La música del jefe final esconde otra canción. Según la wiki del juego, el tema de…»  → sugerida: `P44@1140`
  - (P44, 754, rótulo Hag 1 y primera fase del jefe (754-790) con su tema) **[AUDIO]**
  - (P44, 1140, la Hag 1 con faros azules en plena pelea (1140)) **[AUDIO]**
  - (P44, 1380, taladro de frente con faros azules (1380)) **[AUDIO]**
- **s27_1** — «Escúchala.»  → sugerida: `P44@1420`
  - (P44, 1420, pelea contra la Hag 1 (1420), tema sonando) **[AUDIO]**
  - (P44, 1460, taladro y faros (1460)) **[AUDIO]**
  - (P44, 1580, Kazooie contra la Hag 1 antes de la explosión (1580)) **[AUDIO]**
### s26
- **s26_0** — «Veintiséis. Mucha gente jura que la voz de sargento de Jamjars es de R. Lee Ermey, el de La cha…»  → sugerida: `P04@72`
  - (P03, 1080, Jamjars en el silo «My brother! How's the…» (1080))
  - (P07, 360, Jamjars con el botón verde (360))
  - (P04, 72, Jamjars lección (72))
- **s26_1** — «Es de Grant Kirkhope, el compositor, que también pone las voces de Mumbo, del rey Jingaling y d…»  → sugerida: `P02@600`
  - (P02, 600, rey Jingaling con corona y diálogo (catálogo anterior, P02 s600)) **[OJO]**
  - (P03, 1328, Mumbo habla (1328))
  - (P02, 1110, Jinjo Village: casas Jinjo (1110))
### mitad
- **mitad_0** — «Llevamos veinticinco. Antes de seguir: leemos todos sus comentarios, y los tomamos en cuenta pa…»  → sugerida: `P44@1810`
  - (P44, 90, fiesta de los Jinjos «Thanks, guys» (90))
  - (P44, 1810, banner «Well done Banjo & Kazooie» en la fiesta (1800-1820))
  - (P02, 1290, Mrs. Bottles saludando (1290))
- **mitad_1** — «O el de Antilope, que nos recordó lo triste que es la historia del héroe del tiempo. Gracias po…»  → sugerida: `P44@1840`
  - (P44, 1840, Jamjars y Banjo hablando en la fiesta (1840-1850))
  - (P44, 1860, Mumbo, Humba y Klungo dormido en la fiesta (1860-1870))
  - (P10, 1285, Isle O' Hags: Banjo ante las casas (1285))
### s25
- **s25_0** — «Veinticinco. Los warp pads, las baldosas que te teletransportan dentro de cada mundo, se metier…»  → sugerida: `P03@1256`
  - (P03, 1256, TEXTO LEÍDO: «This is a warp pad» con Banjo sobre el pad y destellos (1256-1268))
  - (P11, 25, Banjo sobre un pad azul circular (25))
  - (P43, 663, Banjo en los pads azul y rojo de la plataforma (663-666))
- **s25_1** — «Según Steve Malpass, ya era tarde para simplificar el juego. Y la gran inspiración para arregla…»  → sugerida: `P03@1268`
  - (P03, 1268, Banjo junto al warp pad (1268))
  - (P43, 654, dos pads sobre la plataforma verde (654))
  - (P11, 50, Templo de Jiggywiggy con la estatua (50): referencia de «inspiración de Zelda» sin otro juego) **[OJO]**
### s24
- **s24_0** — «Veinticuatro. Cuando Kazooie se convierte en dragón, en Hailfire Peaks, su sombra la delata. Si…»  → sugerida: `P21@159`
  - (P21, 159, Kazooie dragón verde (sobre Banjo) lanza fuego en Isle O' Hags (159-171))
  - (P21, 165, Banjo corre con el dragón a la espalda; sombra bajo ellos (165))
  - (P21, 140, diálogo «Dragon, burn many b…» con el retrato de Kazooie (140))
- **s24_1** — «Su retrato al hablar no cambia, y las escenas del final no se programaron para el dragón: ahí v…»  → sugerida: `P21@169`
  - (P21, 169, el dragón escupe fuego (169))
  - (P44, 1930, Banjo y la Kazooie normal en la azotea (1930): la escena final con la Kazooie de siempre)
  - (P21, 100, Humba/Wumba «You have the legendary Mega-G[lowbo]» (100)) **[OJO]**
### s23
- **s23_0** — «Veintitrés. El concurso de Grunty está lleno de trampas de Rare. Una pregunta: ¿en qué juego ap…»  → sugerida: `P43@1540`
  - (P43, 1540, pregunta «…in the name Banjo-Tooie?» con «Less than 10 / 11 / More than 9» (1540))
  - (P43, 1012, pregunta «Which of these is an area in Grunty Industries?» (1012))
  - (P43, 1550, pregunta «Who lives in Jinjo Village?» (1550))
- **s23_1** — «Es Diddy Kong Racing, de mil novecientos noventa y siete. La opción falsa es Super Banjo Land 6…»  → sugerida: `P43@1092`
  - (P43, 1092, pregunta con respuestas de broma «Superstash Deluxe / Booty Grabber Pro / Swagboy Supreme» (1092))
  - (P43, 1252, «Merry Maggie / Jamjars / Captain Blubber» (1252))
  - (P43, 1620, «Snack Pack / Sack Pack / Shack Pack» (1620))
### s22
- **s22_0** — «Veintidós. Del Stomponadon, el dinosaurio de Terrydactyland, solo ves el pie. Y ese pie viene d…»  → sugerida: `P33@461`
  - (P33, 461, pie gigante del Stomponadon con garras sobre el nido (461-470))
  - (P33, 541, polvo y garra de la pisada (541-548))
  - (P33, 490, nube de polvo del pie (490))
- **s22_1** — «En Dream, el proyecto de Rare que acabó siendo Banjo-Kazooie, al protagonista lo iba a persegui…»  → sugerida: `DREAM@50`
  - (DREAM, 50, Dream (SNES, ampliado): la pata gigante del dinosaurio aplasta al protagonista (50-51)) **[DREAM]**
  - (DREAM, 80, segunda pisada del dinosaurio (80-81)) **[DREAM]**
  - (DREAM, 86, tercera pisada (86)) **[DREAM]**
### s21
- **s21_0** — «Veintiuno. En casa de Bottles, su hija Goggles juega con un peluche de Donkey Kong. En la versi…»  → sugerida: `P02@1390`
  - (P02, 1390, Goggles con el peluche de Donkey Kong (1390-1430, 1430 a 720p limpio))
  - (P02, 1430, primer plano de Goggles y el peluche (1430))
  - (P02, 1350, interior de la casa de Bottles (1350))
- **s21_1** — «En el concurso, la respuesta Donkey Kong pasó a ser: un gorila adorable. Y en Nintendo Switch O…»  → sugerida: `P02@1410`
  - (P02, 1410, puerta y póster de la casa de Bottles con Banjo (1410))
  - (P43, 1092, opciones del concurso (para «un gorila adorable»: no es esa pregunta, ver HUECO)) **[HUECO]**
  - (P02, 1510, Kazooie «…already know that!» en la casa (1510))
### s20
- **s20_0** — «Veinte. Si abres un mundo con un código de Cheato, el maestro Jiggywiggy se da cuenta, y anunci…»  → sugerida: `P11@50`
  - (P11, 50, rótulo «Jiggywiggy's Temple» con la estatua (50))
  - (P10, 1085, Cheato «My first cheat is…» y menú de códigos (1085-1110))
  - (P21, 200, rótulo «Jiggywiggy's Temple» (200))
- **s20_1** — «Y si fallas muchas veces sus rompecabezas, empieza a dudar de que seas el elegido, y baja la di…»  → sugerida: `P21@220`
  - (P21, 220, rompecabezas de Jiggywiggy: cuadro rojo y mano (220-300))
  - (P11, 75, rompecabezas de Jiggywiggy (75-100))
  - (P38, 1225, rompecabezas con Banjo (1225-1285))
### s19
- **s19_0** — «Diecinueve. En Banjo-Tooie, Grunty deja de rimar en cuanto se lo piden. Gregg Mayles lo hizo pa…»  → sugerida: `P01@500`
  - (P01, 500, Grunty y su gato «Have… so back to our cas[tle]» (500-515))
  - (P01, 420, Grunty y Brentilda «Get you out your sisters» (420-432))
  - (P44, 786, Grunty en el podio, ya sin rimar (786))
- **s19_1** — «Años después admitió que no fue una de sus mejores ideas, y que probablemente debió mantener la…»  → sugerida: `P44@1721`
  - (P44, 1721, Grunty en su tanque «Okay, numbskulls, time for the biggest…» (1721-1739))
  - (P43, 1680, Grunty con las manos en la cintura tras el concurso (1680))
  - (P01, 530, Grunty junto a Mingella y Brentilda (530))
### s18
- **s18_0** — «Dieciocho. Los Minjos son Jinjos falsos que te atacan cuando te acercas. En los datos del juego…»  → sugerida: `P10@1360`
  - (P02, 1130, Jinjo Village: «Purple Jinjo Family House» (para los Jinjos): NO hay clip de Minjo) **[HUECO]**
  - (P10, 1360, casa Jinjo azul (1360))
  - (P02, 1150, casa Jinjo naranja (1150))
- **s18_1** — «Lo más probable es que fuera un primer diseño del Minjo, descartado porque se le veía venir de …»  → sugerida: `P02@1110`
  - (P10, 1335, casas Jinjo de colores (1335): el Jinjo musculoso solo existe como pegatina de TCRF/wiki) **[HUECO]**
  - (P02, 1110, «Blue Jinjo Family House» (1110))
- **s18_2** — «Un Minjo de gimnasio. Menos mal que no lo usaron: ya bastantes sustos dan los normales.»  → sugerida: `P10@1285`
  - (P02, 1070, Banjo en Jinjo Village (1070): sin Minjo en clip; MG/pegatina) **[HUECO]**
  - (P10, 1285, Banjo ante las casas Jinjo (1285))
### s17
- **s17_0** — «Diecisiete. Lord Woo Fak Fak, el pez abisal del fondo de Jolly Roger's Lagoon, le dio horas de …»  → sugerida: `P18@343`
  - (P18, 343, Lord Woo Fak Fak con su barra de vida (343))
  - (P18, 358, el pez «Pathetically around on…» (358))
  - (P18, 433, pez con la linterna y Kazooie (433))
- **s17_1** — «Steve Mayles descubrió que superaba el máximo de articulaciones del motor, un límite que ni sab…»  → sugerida: `P18@478`
  - (P18, 478, boca roja con dientes (478-493))
  - (P18, 568, explosión de huevo contra el pez (568))
  - (P18, 613, pez de lado con huevos (613-628))
- **s17_2** — «Así que, si alguna vez te pareció que ese pez se movía raro, no eras tú. Le faltaban huesos.»  → sugerida: `P18@688`
  - (P18, 688, TEXTO LEÍDO: «Time I opened my eyes to see what I'm doing!» (688))
  - (P18, 538, pez pasando por la cámara (538))
  - (P18, 628, el pez moviéndose (628))
### s16
- **s16_0** — «Dieciséis. En Grunty Industries, Loggo, el váter que habla, está atascado. Si le insistes, Kazo…»  → sugerida: `P27@1162`
  - (P27, 1162, Loggo, el váter parlante «Hey there, Banjo» (1162-1176))
  - (P27, 1180, Banjo (con el dragón) ante Loggo «I really need unblocking» (1180-1190))
  - (P27, 1204, Banjo desatasca a Loggo «Yep, I can feel a movement in my U-bend!» (1204))
- **s16_1** — «En Xbox, con Microsoft de por medio, a Mario no se le podía ni nombrar. Quedó como: ese italian…»  → sugerida: `P27@1216`
  - (P27, 1216, «It's a Cheato book page!» (1216))
  - (P27, 1038, puerta del baño con icono de persona en Workers' Quarters (1038))
  - (XBLA, 300, XBLA (catálogo): para la línea de «ese italiano famoso»: no hay clip de esa línea) **[XBLA HUECO]**
### s15
- **s15_0** — «Quince. Los cuarenta y cinco Jinjos siempre están en los mismos sitios, pero el color de cada u…»  → sugerida: `P02@1110`
  - (P02, 1110, «Blue Jinjo Family House» (1110))
  - (P02, 1130, «Purple Jinjo Family House» (1130))
  - (P10, 1285, las casas de Jinjo Village (1285))
- **s15_1** — «Los speedrunners lo saben bien: en speedrun punto com hay hasta una opción para las partidas qu…»  → sugerida: `FALCON100@5060`
  - (FALCON100, 5060, speedrun 100 % de Falcon, juego japonés (5060; recortar panel con crop=1440:1080:480:0)) **[JP]**
  - (P10, 1335, las casas Jinjo de colores (1335))
  - (P10, 1360, casa azul Jinjo (1360))
### s14
- **s14_0** — «Catorce. Kirkhope compuso la música de la intro al compás del video tal como corría en la Ninte…»  → sugerida: `P01@186`
  - (P01, 186, intro: Mumbo, Banjo, Kazooie y Bottles jugando al póker (186-232)) **[AUDIO]**
  - (P01, 296, la Hag 1 emerge entre las rocas (296-310)) **[AUDIO]**
  - (P01, 650, la Hag 1 por el portal verde (650-665)) **[AUDIO]**
- **s14_1** — «Y en Nintendo Switch Online, las demos de la pantalla de título van tan aceleradas que parece q…»  → sugerida: `P01@130`
  - (P01, 100, pantalla de título de NSO (100-110): no se ve la demo acelerada) **[HUECO]**
  - (P01, 75, título NSO (75))
  - (P01, 130, escena de tormenta tras el título (130))
### s13
- **s13_0** — «Trece. Esa intro dura diez minutos, y montarla fue un castigo. Ed Bryan, el encargado, tenía qu…»  → sugerida: `P01@420`
  - (P01, 420, Grunty y Brentilda en la intro (420-432))
  - (P01, 475, Brentilda y esqueleto de Mingella «No, no, no, this can…» (475))
  - (P01, 530, Grunty, Mingella y Brentilda «Hassle, I'll» (530))
- **s13_1** — «Para el E3 del dos mil tenía que funcionar sin desfasarse. Él y su hermano Will se quedaron has…»  → sugerida: `P01@560`
  - (P01, 560, Bottles y la mesa de póker otra vez (560))
  - (P01, 695, Banjo y los suyos ante la casa destruida «Well, at least everyone got out safely» (695-710))
  - (P01, 725, Banjo ante la cueva morada (725))
### s12
- **s12_0** — «Doce. A Klungo lo enfrentas tres veces, y el rótulo de su pelea cambia con su ánimo: esbirro co…»  → sugerida: `P02@50`
  - (P02, 50, RÓTULO LEÍDO: «Klungo – Minion with a Mission» (50))
  - (P21, 460, RÓTULO LEÍDO: «Klungo – Revenge-Seeking Minion» (460))
  - (P43, 875, rótulo «Cauldron Keep» y Klungo «Future prosss…» (875))
- **s12_1** — «En la última pelea renuncia: sin ascensos, sin días libres, sin sueldo. Dice que buscará un tra…»  → sugerida: `P43@860`
  - (P43, 860, Klungo «Ssniff! Klungo getsss lesss and…» (860))
  - (P43, 845, Klungo derrotado en el suelo (845))
  - (P43, 785, Klungo en primer plano (785))
- **s12_2** — «Y en Nuts & Bolts lo cumplió: tiene su propio juego, Hero Klungo Sssavesss Teh World. Es el úni…»  → sugerida: `P02@80`
  - (P43, 800, Klungo en el Gatehouse (800): Nuts & Bolts es otro juego: pegatina/MG, no clip) **[HUECO]**
  - (P02, 80, Klungo en su primera pelea (80))
  - (P21, 540, Klungo en su segunda pelea (540))
### s11
- **s11_0** — «Once. En la intro, mientras juegan al póker, la casa de Banjo cambia de papel tapiz en un solo …»  → sugerida: `P01@281`
  - (P01, 281, Mumbo ante cortinas azul-amarillo en la mesa de póker (280-284))
  - (P01, 286, Banjo ante la mesa, cuadro y reloj de cuco (286-290))
  - (P01, 376, Banjo con las cartas, cortinas y pez de colores (372-380))
- **s11_1** — «La razón: el modelo de la casa trae escondida una copia de la casa de Banjo-Kazooie, y ese plan…»  → sugerida: `P01@214`
  - (P01, 396, Banjo ante las pilas de fichas, cortinas al fondo (396))
  - (P01, 408, Mumbo se va hacia la ventana (408))
  - (P01, 214, Mumbo y Banjo con las fichas, papel azul a la derecha (214))
### s10
- **s10_0** — «Diez. Grunty Industries, la fábrica que casi todos odian, fue el primer mundo que diseñó Steve …»  → sugerida: `P27@370`
  - (P27, 370, exterior de ladrillo de Grunty Industries (370))
  - (P27, 530, interior de ladrillo con tuberías y cajas (530))
  - (P27, 610, caja «Defective Goods» con Banjo (610))
- **s10_1** — «Él mismo admite que quedó demasiado complicada. Su consuelo: muchos la odian, a algunos curiosa…»  → sugerida: `P27@570`
  - (P27, 570, pasarelas con cajas «Defective Goods» (570))
  - (P27, 770, puerta de metal con cartel (770))
  - (P27, 930, elevador con cartel y signos «?» (930))
- **s10_2** — «Por cierto, en nuestro ranking de los ocho mundos quedó en último lugar. Malpass, si nos ves: n…»  → sugerida: `P27@650`
  - (P27, 650, letrero «Waste Disposal Plant» (650))
  - (P27, 1038, puerta del baño en Workers' Quarters (1038))
  - (P27, 1126, refrigerador con el logo R de Rare (1126))
### s09
- **s09_0** — «Nueve. En Jolly Roger's Lagoon vive Trotty, un cerdo al que le salió un tercer brazo por bañars…»  → sugerida: `P17@198`
  - (P17, 198, cerdo rosa con pelota de playa y calzón azul, 1080p (198-205): TRES BRAZOS NO SE VEN, solo dos) **[OJO]**
  - (P17, 425, cerdo rosa con flotador de serpiente verde «Thanks, giant te…» (425-430)) **[OJO]**
  - (P17, 500, el cerdo en el flotador junto a Banjo (500)) **[OJO]**
- **s09_1** — «Según VGFacts, en la versión japonesa le quitaron el brazo, y ahora solo le preocupa que el agu…»  → sugerida: `P17@215`
  - (P17, 215, el cerdo habla «Well, I didn't w…» (215)) **[OJO]**
  - (P17, 275, camino de arena de la laguna (275))
  - (P17, 25, «Jolly's» y la laguna (25))
### s08
- **s08_0** — «Ocho. Muchos recuerdan que Banjo-Tooie necesitaba el Expansion Pak. Falso: funciona en una Nint…»  → sugerida: `P42@325`
  - (P42, 325, Bee Banjo vuela solo lejos de Cloud Cuckooland (325-350))
  - (P42, 75, islas flotantes de Cloud Cuckooland desde el aire (75))
  - (P42, 225, islas y plataformas de CCL (225))
- **s08_1** — «El precio: si te alejas volando de Cloud Cuckooland y te das la vuelta para verla entera, no ca…»  → sugerida: `P42@400`
  - (P42, 400, islas de CCL desde el aire con Bee Banjo (400))
  - (P42, 300, isla con tallo y Bee Banjo (300))
  - (P39, 30, isla de pasto verde de CCL con nubes (catálogo anterior)) **[OJO]**
### s07
- **s07_0** — «Siete. Un jugador normal tarda decenas de horas en completarlo al cien por cien. El récord mund…»  → sugerida: `FALCON100@5200`
  - (FALCON100, 5200, Falcon, récord 100 % 4:10:46 (5200; crop=1440:1080:480:0)) **[JP]**
  - (FALCON100, 6060, Falcon con la pistola de huevos (6060)) **[JP]**
  - (FALCON100, 4060, Falcon (4060)) **[JP]**
- **s07_1** — «Y llegar al final, sin buscarlo todo, le tomó veinticinco minutos y cuarenta y nueve segundos. …»  → sugerida: `FALCON_ANY@140`
  - (FALCON_ANY, 140, Falcon, any% 25:49 (140; crop)) **[JP]**
  - (FALCON_ANY, 250, Falcon any% (250)) **[JP]**
  - (FALCON_ANY, 470, Falcon any% (470)) **[JP]**
### s06
- **s06_0** — «Seis. El huevo Clockwork Kazooie, la bomba de cuerda que manejas a distancia, fue la mayor fábr…»  → sugerida: `P27@177`
  - (P04, 144, Kazooie en primera persona con huevos (para el huevo bomba; NO hay toma del Clockwork Kazooie)) **[HUECO]**
  - (P27, 177, entrada de Grunty Industries con la estación (177-210))
- **s06_1** — «Chris Sutherland cuenta que en las pruebas los fallos no se acababan nunca. En el código se lla…»  → sugerida: `GI_SIN_TREN@1`
  - (GI_SIN_TREN, 1, TAS: Banjo en plataforma de GI sin el tren (1-3; 9 s: ante la entrada; el clip dura 9 s con cortes 4-8)) **[OJO]**
  - (DOS_BANJOS, 58, los dos Banjos juntos en el iglú de Boggy (58-72))
  - (P27, 370, exterior de GI, por donde se entra normalmente (370))
### s05
- **s05_0** — «Cinco. Steve Mayles escondió una animación rara de Jamjars: en vez de meterse a tiempo en su si…»  → sugerida: `JAMJARS_TAPA@6`
  - (JAMJARS_TAPA, 6, Jamjars sale despedido y la tapa le golpea (golpe 10-10,5 s; el clip dura 12 s: solo 6 s desde el seg. 6)) **[OJO]**
  - (P03, 1080, silo normal de Jamjars (1080))
  - (P07, 360, silo de Jamjars en Glitter Gulch (360))
- **s05_1** — «Sale muy pocas veces. Años después, viendo un speedrun en el maratón Awesome Games Done Quick, …»  → sugerida: `P11@350`
  - (JAMJARS_TAPA, 7, «Dismissed», salida del silo y golpe (7-12)) **[OJO]**
  - (P03, 1100, Jamjars en el silo (1100))
  - (P11, 350, silo de Jamjars en Witchyworld (350))
- **s05_2** — «Su reacción: uno de sus momentos de mayor orgullo. Costarle unos segundos a ese speedrunner.»  → sugerida: `P34@195`
  - (JAMJARS_TAPA, 10, la tapa golpea la cabeza (10-10,5)) **[OJO]**
  - (P04, 72, Jamjars lección (72))
  - (P34, 195, Jamjars «That'll be all» (195))
### s04
- **s04_0** — «Cuatro. Al final del juego, Grunty promete venganza en Banjo-Threeie. Durante años se creyó que…»  → sugerida: `P44@1962`
  - (P44, 1962, TEXTO LEÍDO: Grunty (la cabeza) «Just you wait until Banjo-Thr[eeie]» (1962-1964))
  - (P44, 1960, «You'll be sorr[y]» (1960))
  - (P44, 1944, Jamjars antes de la patada (1944-1950))
- **s04_1** — «¿Y el video de Space World dos mil, con Banjo, Kazooie y Mumbo perseguidos por enemigos? Era un…»  → sugerida: `SPACEWORLD@0`
  - (SPACEWORLD, 0, demo de GameCube Spaceworld 2000: Mumbo (0), Kazooie (3), enemigos (5-11); calidad VHS; marca Kikizo abajo) **[GC OJO]**
  - (SPACEWORLD, 5, enjambre de bichos rodeando (5-6)) **[GC OJO]**
- **s04_2** — «Entre los perseguidores salen hasta Gobi y Alphette, dos personajes que no le harían daño a nad…»  → sugerida: `P20@71`
  - (SPACEWORLD, 7, multitud de enemigos en cueva (7-11); Gobi y Alphette NO se identifican en la cinta) **[GC OJO]**
  - (P20, 71, alienígenas «No. We're Alph[a]…» «Gammo. We're als[o]…» (58-106): sirven para presentar a Gobi y Alphette)
  - (P34, 1050, Gobi el camello (catálogo anterior, P34 s1050)) **[OJO]**
### s03
- **s03_0** — «Tres. Banjo-Tooie desconfía de ti. Si el chip de guardado del cartucho no es el correcto, el ju…»  → sugerida: `P01@100`
  - (P01, 75, título NSO limpio (75): el chip y el letrero «No controller» solo como MG) **[HUECO]**
  - (P01, 100, título con Klungo (100))
- **s03_1** — «Y eso no es todo. Durante la partida, le pregunta al chip de seguridad del cartucho doscientas …»  → sugerida: `P01@130`
  - (P01, 130, tormenta sobre Spiral Mountain (130): letrero «No controller» solo como MG) **[HUECO]**
- **s03_2** — «Ni el examen de la bruja era tan desconfiado.»  → sugerida: `P43@1012`
  - (P43, 1012, pregunta del examen de la bruja (1012))
  - (P43, 932, inicio del concurso (932))
### s02
- **s02_0** — «Dos. En Terrydactyland, junto al cráneo de Mumbo, hay una formación de rocas que, vista desde a…»  → sugerida: `P22@750`
  - (P03, 1232, cráneo de Mumbo con ojos naranjas de MAYAHEM (1232): NO es el de Terrydactyland) **[OJO]**
  - (P22, 750, rótulo «Terrydactyland» (750)) **[OJO]**
  - (P25, 880, rótulo «Terrydactyland» y cueva (880)) **[OJO]**
- **s02_1** — «Nintendo Life se lo preguntó al responsable de los escenarios, Steven Hurst. Su defensa: él sol…»  → sugerida: `P23@30`
  - (P25, 760, Banjo en cueva roja de Terrydactyland (760): NO hay toma aérea del cráneo; pegatina del dibujo de Mayles) **[HUECO]**
  - (P23, 30, entrada tipo concha en cueva de Terrydactyland (catálogo anterior)) **[OJO]**
- **s02_2** — «Por accidente. Juzga tú.»  → sugerida: `P22@60`
  - (P22, 60, roca agrietada con Banjo (catálogo anterior)) **[OJO]**
  - (P25, 360, pared de cueva con Banjo (360))
### s01
- **s01_0** — «Y el número uno. En el final, Banjo, Kazooie y sus amigos juegan con la cabeza de Gruntilda en …»  → sugerida: `SACO@104`
  - (P44, 1950, NSO: Banjo patea la cabeza de Grunty (1950-1956), versión de N64/NSO)
  - (SACO, 68, japonés: el saco cae (68-71), cortar etiqueta) **[JP]**
  - (SACO, 104, occidental: la cabeza rueda (104-107))
- **s01_1** — «Lo absurdo: el ojo de Grunty sigue saliéndose del saco, igual que en el original. No hay explic…»  → sugerida: `SACO@71`
  - (SACO, 71, japonés: el ojo en el suelo junto al saco (71-72)) **[JP]**
  - (SACO, 107, occidental: el ojo en el suelo (107-110))
  - (P44, 1954, NSO: texto «Ooh, I think he[r eye…]» (1954))
- **s01_2** — «En Xbox, por cierto, la cabeza volvió. Y tú, toda la vida pateándola, sin saber que en Japón er…»  → sugerida: `P44@1900`
  - (P44, 1954, versión N64/NSO: la cabeza patada (1954))
  - (P44, 1900, Banjo en casa de Bottles tras el final (1900))
  - (P44, 1930, Banjo y Kazooie en la azotea (1930))
### cierre
- **cierre_0** — «Esos son los cincuenta secretos de Banjo-Tooie que ignoraste. ¿Cuántos conocías? Dímelo en los …»  → sugerida: `P02@1070`
  - (P44, 1800, fiesta «Well done Banjo & Kazooie» (1800))
  - (P44, 1850, Jamjars, Mumbo y Banjo (1850))
  - (P02, 1070, Banjo en Jinjo Village (1070))
- **cierre_1** — «Si te gustó, suscríbete: este canal vive de clásicos como este. Y si te quedaste con ganas de m…»  → sugerida: `P02@230`
  - (P44, 1974, «The End» con fuegos artificiales (1972-1977; NO pasar de 1977: overlay «Subscribe to my channel»)) **[OJO]**
  - (P01, 75, título NSO (75))
  - (P02, 230, rótulo «Isle O' Hags» (230))

## Resumen de huecos y riesgos
- **Sin toma buena (HUECO):** s03_0, s03_1, s03_2 (cartucho/chip/«no hay mando»: solo MG; no hay gameplay), s02_x (no hay toma aérea del cráneo de Terrydactyland), s09_x (Trotty con tres brazos: no se ve), s18_x (Minjo y el Jinjo musculoso: solo pegatina), s06_0 (Clockwork Kazooie no localizado), s44_x (Shack/Taxi Pack y el cambio de mochila no se aprecian), s28_0 (DK64 y Perfect Dark: otros juegos, solo pegatina estática), s12_2 (Nuts & Bolts), s14_1 (demo acelerada de NSO), s16_1 (línea de Mario), s21_1 (pregunta «un gorila adorable» de Xbox).
- **Frases que repiten momento tras el algoritmo (sugerida con choque):** s44_1, s31_1, s21_1, s15_0, s03_0-s03_2, s01_1 (ver `tomas_frases.json` → `sugerida`).
- **Material de otro juego/versión que va marcado:** SACO (japonés), FALCON (japonés), SPACEWORLD (GameCube), DREAM, BK_LAIR (Banjo-Kazooie), SMASH_*, XBLA/XBLA_TOT.
- **AUDIO:** s47_0/1 (Atlantis, P18 10-60 y 100-110 s), s35_0/1 (isla → Grunty's Lair de BK: P38 1085-1100 + `BK_LAIR` 3544-3570), s42_0/1 (P43 755-780: cambio de música y Klungo), s33_0/1 (conjuro de Mumbo: P03 884-900 pad, P09 1240-1260 hechizo), s30_0 (cadencia de Jamjars: P03 1080-1140, P04 60-72), s29_0 (abucheos P43 932-1000), s27_0/1 (tema de la Hag 1: P44 754-790 y 1140-1580), s49_0 (Old King Coal «Hurrr» P09 1380), s14_0 (música de la intro P01 186-232, 296-310, 650-665).
