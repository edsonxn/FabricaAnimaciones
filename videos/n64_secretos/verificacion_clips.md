# Verificación de clips — n64_secretos (31-oct-2026)

Revisión de las 9 hojas `previews/medios_01..09.jpg`, mosaicos propios de 6 cuadros por clip dudoso y medición de brillo/duración de los 170 clips (cv2, un cuadro cada 0,3 s; scripts en el scratchpad: `medir.py`, `mosaico.py`, `medidas.json`). No se tocó guion.py, plan_clips.py, busquedas.json ni se lanzó `bajar`.

Resumen: no hay caras de streamer ni webcams. No hay clips de otro juego (Final Fantasy, GTA III, Saturn, PlayStation, arcades y Smash Melee están nombrados por la voz). Sí hay 1 solapamiento de contenido, 31 clips truncados, 7 con negro o casi negro, 8 con rótulos o intros de video ajeno y 4 que no enseñan lo que dice la voz.

## A. CLIPS TRUNCADOS (duración real < beat − 0,5 s)

Los 31 son beats con audio original (`AMBIENTE`). Ningún clip sin audio quedó corto. `bajar` trunca los clips con audio: el mp4 trae menos de lo que pide el beat. En el motor el beat se queda sin imagen o se congela al final.

| Escena | mp4 / beat (s) | Fuente y `desde` | Sugerencia |
|---|---|---|---|
| 079 | 1,8 / 10,4 | SU2 70 | gravísimo; `bajar 79 --rehacer` y mirar por qué corta; si sigue corto, quitarla de `AMBIENTE` |
| 042 | 2,9 / 8,6 | PW2 110 | igual |
| 066 | 1,8 / 6,2 | MK1 6 | igual |
| 113 | 1,9 / 6,9 | AF2 60 | igual |
| 126 | 2,4 / 8,5 | MPP 20 | igual (además está casi negro, ver B) |
| 068 | 2,4 / 7,4 | MK1 60 | igual |
| 078 | 3,0 / 5,6 | SU2 56 | igual |
| 080 | 3,1 / 7,7 | SU2 90 | igual |
| 084 | 3,1 / 8,1 | KIG 100 | igual |
| 112 | 3,5 / 8,0 | AF2 30 | igual |
| 069 | 3,4 / 8,9 | MK1 100 | igual |
| 152 | 3,6 / 6,8 | WW1 426 | igual |
| 132 | 3,8 / 10,4 | TETLP 1388 | igual |
| 067 | 4,0 / 8,5 | MK1 20 | igual |
| 134 | 4,1 / 8,8 | FF1 8 | igual |
| 025 | 4,4 / 9,7 | MK4 90 | igual |
| 040 | 4,9 / 9,3 | PW2 6,7 | igual |
| 019 | 4,9 / 9,7 | FV1 80 | igual |
| 142 | 5,2 / 6,4 | DQ1 36 | igual |
| 026 | 5,6 / 8,1 | MK4 245 | igual |
| 139 | 5,7 / 7,9 | FV1 93 | igual |
| 022 | 6,0 / 7,7 | SM64 185 | igual |
| 032 | 6,1 / 8,9 | MT1 84 | igual |
| 114 | 6,3 / 11,5 | AF2 80 | igual |
| 033 | 7,1 / 8,2 | MT1 112 | igual |
| 052 | 7,2 / 7,8 | SF 106 | menor (0,6 s) |
| 150 | 7,7 / 8,4 | SB3 1422 | menor (0,7 s) |
| 135 | 8,8 / 10,8 | FF1 43 | 2 s cortos |
| 158 | 8,8 / 10,1 | SMASH 3953 | 1,3 s cortos |
| 043 | 9,9 / 10,5 | PW1 105 | menor (0,6 s) |
| 077 | 11,2 / 12,5 | SU2 35 | 1,2 s cortos |

Causa probable: el corte de `bajar` con audio, no el fin del video fuente (081 y 080 son del mismo video SU2 y 081 sí salió completo). Conviene revisar `nucleo/bajar` antes de rehacer; si el problema se repite, esas escenas se pasan a clip mudo con SFX del juego aparte.

## B. NEGRO, CASI NEGRO O FUNDIDO (media de gris < 14)

| Escena | Segundos | Qué es | Sugerencia |
|---|---|---|---|
| 028 | 0,0-3,3 | logo PlayStation y luego negro; la consola sale a los 4,5 s | PSPRE `desde` 54 → 57,5 (consola desde el segundo 0) |
| 092 | 1,2-2,9 | Map Select y negro antes del Mario Kart a 4 | MK4 `desde` 400 → 403 |
| 126 | 1,2-8,5 | minijuego de Mario Party a oscuras, casi negro todo el clip; la voz habla de girar el stick con la palma y no se ve | cambiar a MPT (Tug o' War) `desde` ≈ 12, o MP en otro minijuego de girar el stick |
| 011 / 082 | 5,7-7,2 | negro entre el ULTRA 64 y el título de Killer Instinct | ver F (011 repetido) |
| 083 | 6,0-6,3, 8,7, 9,3 | parpadeos del anuncio, aceptable | nada |
| 146 | varios | EarthBound 64 es oscuro por naturaleza (carro de mina) | aceptable; el logo Mother 3 de 7,6 s en adelante concuerda con la voz |
| 134 | todo | demo de Final Fantasy VI muy oscura con personajes diminutos (FF1 `desde` 8) | `desde` 8 → 18-30, donde los personajes se ven más grandes |
| 162 | 1,2-3,0 | Iwata con la sala a oscuras, se le ve | aceptable |
| 168 | 1,8 y 2,7 | parpadeos del tráiler del remake | aceptable |
| 034 | 5,5-7,5 | círculo gris vacío con una mota (cierre en iris del intro de Mario Tennis), no negro pero vacío | MT3 `desde` 0 sirve solo ~5 s; el resto del beat (10,4 s) mejor con MT2 o con el selector de MTC en Waluigi |
| 096 | 4,2-4,5 | pantalla blanca de carga, 0,3 s | aceptable |

## C. RÓTULOS, INTROS, MARCAS DE AGUA O PANTALLAS DE UN VIDEO AJENO

| Escena | Problema | Segundo | Sugerencia |
|---|---|---|---|
| 130 | aparece un dibujo de una chica con gafas (avatar o mascota del youtuber) sobre fondo rojo | desde ~3,6 s hasta el final | la foto del Bio Sensor dura solo ~3,7 s en TET1 (205,5-209); acortar el beat con otra fuente para el resto (Tetris 64 con la pinza en la oreja) o `desde` más temprano si hay más foto |
| 089 | intro del video fuente: fondo azul con silueta del mando y miniaturas con un presentador | 0-2,9 | HT2 `desde` 40 → 42,5 (el cuarto de hotel entra a los 2,9 s) |
| 054 | pantalla de una página web ("Rumble PAK The Circuit", tabla de direcciones); la voz habla de dos pilas AAA y del puerto de la tarjeta de memoria | 4,8-12 | RUM2 `desde` 205 → otro tramo del Rumble Pak (pilas y puerto), o dejar solo la foto dorada de 0-4 s y usar otro clip |
| 124 | logo "BIORAND" (paraguas de Umbrella) superpuesto | 3,7-5,5 | RE3 `desde` 332 → ~338 |
| 148 | marca "BLOXLOGICS" y rótulo japonés "MOTHER SERIES NEW WORK" en el cuadro | todo | EB3 `desde` 0: probar otro tramo sin rótulo, o EB1 / EB2 |
| 094 | marca de Instagram `@consoletechnician` pequeña abajo a la izquierda | todo | IQ5 `desde` 170: aceptable si se cubre con una pegatina; o `recorte` |
| 098-101 | captura de pantalla con reloj de cámara (10:45 AM) y baja calidad | todo | son la única fuente de Perfect Head; aceptable (sin alternativa) |
| 082, 083, 011 | logo "R" de Rare fijo abajo a la izquierda | todo | menor |
| 161-163 | logo "GDC" abajo a la derecha | todo | menor (es el discurso real que la voz menciona) |
| 052, 040-043, 166, 167 | avatar del jugador de Switch Online (esquina) y "Suspend Menu" (052) | todo | menor |
| 110 | marca "BLAZE92" abajo a la izquierda | todo | menor |

## D. NO ENSEÑAN LO QUE DICE LA VOZ

| Escena | Voz | Se ve | Sugerencia |
|---|---|---|---|
| 164 | «lo más grande que dejó la N64 empezó así, con un hombre programando en sus fines de semana» | dibujos en boceto de gente jugando con DS (homenaje a Iwata) | IW2 `desde` 138 → clip de Dragon King (DKG) o Smash 64 (SMASH) en otro segundo no usado |
| 126 | girar el stick con la palma | minijuego a oscuras | ver B |
| 034 | su nombre mezcla Luigi con warui y la L invertida en la gorra | Waluigi solo los primeros 2 s | ver B |
| 054 | pilas AAA y puerto | página web | ver C |
| 071 / 072 | pasar Pokémon al juego / Doduo y Dodrio | cartucho de Pokémon Azul en la Game Boy Tower | aceptable (la torre es lo que enseña) |
| 015 | «Nadie lo ha cerrado del todo. Y entonces llegó la decisión» | funda de plástico de PlayStation (0-3,5 s) y disco de Final Fantasy VII | débil pero válido (FF7 y PlayStation los nombra el guion); FV3 `desde` 75 → 78,5 para saltar la funda |
| 093 | «la consola dentro del mando» | manos tapando el mando 0-5 s, el iQue se ve a partir de 6 s | IQ3 `desde` 386 → ~392 |

## E. CASI QUIETOS (> 80 % de cuadros idénticos)

| Escena | Segundos | Qué es | Sugerencia |
|---|---|---|---|
| 118 | 8,9 | pantalla Randnet fija | DD1 `desde` 439 → tramo con movimiento, o dejar y cubrir con pegatina/MG |
| 119 | 8,1 | pantalla Randnet fija (teclado) | DD1 `desde` 549 → igual |
| 121 | 8,6 | logo Angel Studios fijo | RE3 `desde` 172 → ~178 |
| 130 | 5,2 | foto fija del Bio Sensor | ver C |

## F. CONTENIDO REPETIDO Y DUDOSO

- **011 repite el contenido de 082**: ambos muestran el anuncio de Ultra 64 y de Killer Instinct (011 viene de SHOS 4 y 082 de KIULTRA 10,5). Sugerencia: 011 → SHOS `desde` ≥ 30 (Super Mario 64 beta del Shoshinkai 95) y dejar el anuncio solo en 082.
- **122**: un cyborg sobre fondo hexagonal con «ACCESS DENIED» (RE3 `desde` 183). Parece una demo de Angel Studios y no Resident Evil 2; la voz habla de «nueve personas, doce meses, cinemáticas comprimidas». Verificar a ojo; sugerencia: RE3 `desde` 217-300 (juego real).
- **083**: el KI1 arcade viene lado a lado y repite cada cuadro en dos mitades; comprobar que `ventanas.py` lo recorta.
- **159**: Luigi con traje de equipo morado, no Waluigi; es Smash 64 normal. Sin problema.

## Lista resumida de escenas a rehacer

Prioridad alta (el clip no sirve):
- 126 (MPT ~12 s)
- 130 (acortar o cambiar de fuente)
- 034 (MT2/MTC)
- 054 (otro tramo de RUM2)
- 124 (RE3 ~338)
- 148 (otra fuente EB)
- 089 (HT2 42,5)
- 028 (PSPRE 57,5)
- 092 (MK4 403)
- 011 (SHOS ≥ 30)
- 122 (verificar)
- 164 (clip distinto)

Prioridad alta (truncados > 3 s): 079, 042, 066, 113, 068, 078, 080, 084, 112, 069, 152, 132, 067, 134, 025, 040, 019. Rehacer con `bajar N --rehacer` investigando primero el corte con audio.

Prioridad media (truncados 1-3 s): 142, 026, 139, 022, 032, 114, 033, 135, 158, 077.

Prioridad baja: 118, 119, 121 (quietos), 093, 015, 134, y marcas de agua en 094, 098-101, 082, 083, 161-163, 110.
