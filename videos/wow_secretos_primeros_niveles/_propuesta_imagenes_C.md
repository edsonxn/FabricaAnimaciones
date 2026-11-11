# Propuesta de imágenes — grupo C (s10, s08, s07, s06) · 10-nov-2026

Imágenes nuevas, todas miradas a 640 px y comprobadas por identidad (fuentes en `pegatinas/_fuentes.txt`, bloque «grupo C»).
Clips propuestos: ningún youtuber, webcam ni mascota en el tramo indicado (sí la interfaz normal del juego).

## Errores de lo que ya hay (corregir sí o sí)
- `pegatinas/thandol.png` y `pantallas/thandol.jpg` son un **mapa de Warcraft II** (otro juego, regla 3). Se usan en `pv("está el Puente de Thandol…")` (línea ~335) y como foto `"thandol"` en los dos `mapa("humedales")` (s10 y s09) → cambiar por **`s10_puente_thandol`**.
- `pv("Número siete. La estatua", "ruinas_lordaeron", "El Abandonado · la estatua de ojos rojos")` enseña la **entrada de las ruinas**, no la estatua ni al jefe → cambiar por **`s07_abandonado`** (y el rótulo a «El Abandonado · jefe secreto»).
- `o_carta` (320 px, borrosa) en `rel("Número diez…")`, el legajo y la cadena → mejor **`s10_carta_mision`** (ventana real de la misión, 620×784).
- Clips de otro jefe o con rótulos del youtuber: scene-125 y scene-132 (ficha «ALLIANCE» de Mudbucket con mascota), **scene-127 (Bjork, otro jefe, mientras la voz dice Viktor)**, scene-129 (webcam de tygarlily), scene-133/134 (fichas de botín de Uncas), scene-141 y 146 (subtítulos en inglés quemados), scene-145 y 148 (texto/infografía del youtuber), scene-142 (web de Twincruiser mientras la voz describe «M K» y la estatua).

## s10 · Sully Balloo
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s10_0 | «Número diez. Una carta» | «fondo del río» | pegatina (rel, en vez de o_carta) | `s10_carta_mision` | la ventana de misión «Sully Balloo's Letter» |
| s10_1 | «está el Puente de Thandol, un puente enano» | «gigantesco» | pegatina grande (tam ≥ 600) | `s10_puente_thandol` | el Puente de Thandol (tramo colgante entre pilares enanos) |
| s10_2 | «encuentras un cadáver» | «un cadáver» | pant | `s10_cadaver` | el enano muerto en el fondo, bajo el puente |
| s10_2 | «Y con él, un sobre empapado» | «sobre empapado» | pant | `s10_sobre_empapado` | el sobre flotando junto al cadáver |
| s10_3 | «Y empieza una misión: llevársela» | «llevársela» | pegatina grande | `s10_carta_mision` | texto real: «The letter is addressed to a Mrs. Sara Balloo of Ironforge… "My dear Sara…"» |
| s10_9 | «En Forever sigue ahí» | «alguien se moje» | clip nuevo para scene-114 | `https://www.youtube.com/watch?v=bjY79b050l8` desde 181 | Sara Balloo tras su mostrador en Forjaz diciendo «This isn't fair! My dearest Sully!» (sale el nombre del personaje del youtuber, «Focusta», dentro del bocadillo) |

Ya bien: s10_4 (legajo con el texto), s10_5-s10_7 (silueta de Sullivan Ballou + cadena), s10_8 (tarjeta de las dos guerras civiles). `sara` ya es Sara Balloo.

## s08 · La chimenea de Viktor (el secreto paso a paso)
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s08_2 | «hay dos jefes que no aparecen» | «si no los buscas» | carr de 2 | `s08_viktor`, `s07_abandonado` | los dos jefes ocultos (modelos) |
| s08_3 | «El primero está en una casa abandonada» | «después del Barón» | clip nuevo para scene-125 | `https://www.youtube.com/watch?v=Uh7ZrzUUdbk` desde 119 | llegada a la casa en ruinas con la chimenea encendida (4K, sin webcam; oscuro: subir gamma ~1,35) |
| s08_3 | «en una casa abandonada» | «después del Barón» | pant | `s08_casa_chimenea` | la casa en ruinas y su chimenea, en la plaga |
| s08_4 | «Dentro, en la chimenea, hay leña tibia» | «empiezan las oleadas» | clip nuevo para scene-126 | `Uh7ZrzUUdbk` desde 124 | la chimenea encendida dentro de las ruinas; el jugador la activa |
| s08_4 | «Le haces clic» | «empiezan las oleadas» | pant | `s08_lena_tibia` | la chimenea de cerca con el cursor de interactuar (engranaje) |
| s08_5 | «Son cinco oleadas» | «al terminar» | clip nuevo para scene-127 (sustituye a Bjork) | `Uh7ZrzUUdbk` desde 152 | la pelea contra las oleadas junto a la casa |
| s08_5 | «aparece Viktor el Vil» | «jefes secretos de la mazmorra» | pant | `s08_viktor_aparece` | Viktor the Vile con su placa (nivel 19) entre esqueletos |
| s08_5 | «uno de los jefes secretos» | «de la mazmorra» | pegatina grande | `s08_viktor` | el modelo de Viktor de cuerpo entero |
| s08_6 | «Cuántas oleadas son exactamente» | «a explorar» | clip nuevo para scene-128 | `Uh7ZrzUUdbk` desde 23 | Viktor the Vile en combate (placa visible) |
| s08_7 | «la pista es la chimenea» | «ya la encontraste» | clip nuevo para scene-129 | `Uh7ZrzUUdbk` desde 8 | la chimenea encendida de cerca (8-12 s; sale «XP: 88», texto del juego). No empezar antes de 4 s: hay un título del youtuber en 0-3 s |

Ya bien: s08_0 (reliquia), s08_1 (mapa de Tirisfal + `ruinas_lordaeron`), MG «ocultos» y «tiempos» (que se queden debajo de las pant). Ojo: la ficha `tiempos` aún dice «según una guía» → el guion ya no dice «una guía»: cambiar el subtítulo (p. ej. «jefe secreto»).

## s07 · La estatua que te mira
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s07_0 | «Número siete. La estatua» | «te mira» | pegatina (en vez de ruinas_lordaeron) | `s07_abandonado` | el modelo de El Abandonado |
| s07_3 | «hay una estatua con los ojos rojos» | «brillando» | **FALTA** | Flow | no encontré ni una toma de la estatua (12 videos revisados: Bue, Atten, Kasum, RoboNanners, Mudbucket, Uncas, Dlonem, tygarlily…; todos muestran la plaza y al jefe, ninguno la estatua de cerca). Flow con ingredientes: `s07_abandonado_juego` (la plaza Market Street) + `s07_abandonado` (el modelo) → estatua de piedra encapuchada con dos ojos rojos encendidos en una esquina de esa plaza, estilo WoW Classic, rótulo «RECREACIÓN» |
| s07_4 | «Si te acercas, llegan tres oleadas» | «enemigos» | clip nuevo para scene-132 | `https://www.youtube.com/watch?v=bGQ5w2BcYH4` desde 1541 | la plaza Market Street llena de necrófagos de la plaga (las oleadas), sin webcam |
| s07_4 | «aparece el jefe secreto: El Abandonado» | «El Abandonado» | clip nuevo para scene-133 | `bGQ5w2BcYH4` desde 1597 | el letrero «Market Street» y El Abandonado apareciendo con su placa de nombre |
| s07_4 | «el jefe secreto: El Abandonado» | «le queda perfecto» | pant | `s07_abandonado_juego` | El Abandonado en combate (placa) |
| s07_5 | «abandonado por todos los grupos» | «con prisa» | pegatina grande | `s07_abandonado` | el modelo del fantasma de cuerpo entero |
| s07_6 | «La mayoría de grupos pasan de largo» | «no es decoración» | clip nuevo para scene-134 | `bGQ5w2BcYH4` desde 1606 | sigue la pelea con El Abandonado (en vez de las fichas de botín de Uncas) |
| s07_7 | «Dos jefes ocultos en una mazmorra» | «nivel quince» | carr de 2 | `s08_viktor`, `s07_abandonado` | los dos jefes juntos |

Ya bien: s07_1, s07_2 (clips de las ruinas; Entrañas no sale, pero lo cubre el mapa del s08). MG «oleadas abandonado» encaja con las tres oleadas.

## s06 · Michel Koiter
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s06_1 | «En Los Baldíos, en una loma» | «que te lleve» | clip nuevo para scene-141 (tiene subtítulos quemados) | `https://www.youtube.com/watch?v=VGW9QAWNkyE` desde 183 | paisaje de Los Baldíos, limpio |
| s06_2/3 | «En su base, dos letras grabadas» | «con un mandoble» | clip nuevo para scene-142 (ahora enseña una web) | `VGW9QAWNkyE` desde 4 | primer plano del obelisco con «MK» y el orco con su mandoble encima (4-9 s, limpio) |
| s06_3 | «hay una estatua de un orco con un mandoble» | «con un mandoble» | pant | `s06_estatua_orco` | la estatua del orco con el mandoble sobre «MK» |
| s06_3 | «un sanador espiritual, que se llama Koiter» | «se llama Koiter» | pant | `s06_koiter_sanador` | el sanador espiritual (ángel azul) junto al santuario |
| s06_4 | «Michel Koiter era uno de los artistas» | «de Blizzard» | pegatina (camafeo/silueta) | `s06_michel_koiter` | foto real de Michel Koiter (la misma de warcraft.wiki.gg) |
| s06_4 | «firmaban juntos como Twincruiser» | «Twincruiser» | clip nuevo para scene-144 | `VGW9QAWNkyE` desde 48 | la web «TWINCRUISER» de los gemelos en un monitor CRT |
| s06_6 | «La estatua de ese orco es una copia exacta» | «Twincruiser» | clip nuevo para scene-145 (tiene el rótulo «Michel's life ended at 19») | `VGW9QAWNkyE` desde 216 | el camino de Los Baldíos hacia el obelisco al atardecer; encima, pant `s06_estatua_orco` desde «es una copia exacta» |
| s06_7 | «quien te devuelve a la vida es Koiter» | «es Koiter» | pant | `s06_koiter_sanador` | el sanador Koiter (sustituye al pv `santuario`, que es la estatua, no el sanador) |
| s06_8 | «Raynor recoge la placa de un marine caído» | «Dice M. Koiter» | pegatina grande (tam ≥ 600) | `s06_placa_koiter` | la placa «M. KOITER · MAR SARA» de StarCraft II |
| s06_8 | «Blizzard lo volvió a recordar en StarCraft dos» | «M. Koiter» | clip nuevo para scene-147 | `VGW9QAWNkyE` desde 278 | partida de StarCraft II con el retrato de Raynor (la voz nombra el juego, así que vale) |
| s06_9 | «La próxima vez que cruces Los Baldíos» | «de todo el juego» | clip nuevo para scene-148 (tiene una infografía del youtuber) | `VGW9QAWNkyE` desde 361 | el santuario en lo alto de la loma, plano general limpio |

Ya bien: s06_0 (reliquia `santuario` = la estatua), s06_1/2 (mapa de Los Baldíos), s06_5 (MG «vida koiter» + rótulo «19 AÑOS»), tarjeta de StarCraft II.

## Archivos nuevos
`pantallas/`: s10_cadaver, s10_sobre_empapado, s08_casa_chimenea, s08_lena_tibia, s08_viktor_aparece, s07_abandonado_juego, s06_estatua_orco, s06_koiter_sanador (todas .jpg, 1920×1080).
`pegatinas/`: s10_carta_mision (620×784), s10_puente_thandol (1000×750), s08_viktor (540×850), s07_abandonado (535×840), s06_michel_koiter (766×990), s06_placa_koiter (840×500).
Descargas temporales: `_dl/img_C/`.
