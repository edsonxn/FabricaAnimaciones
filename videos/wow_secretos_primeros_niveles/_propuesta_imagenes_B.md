# Propuesta de imágenes — grupo B (puestos 15 → 11), 10-nov-2026

Todo lo nuevo está en `pantallas/` y `pegatinas/` con prefijo `s1X_` (fuentes en `pegatinas/_fuentes.txt`, bloque «grupo B»), más 3 clips locales recortados sin webcam en `_dl/img_B/` (van en `busquedas.json` como `{"_local": ..., "desde": ...}`). Revisé cada imagen a 640 px y comprobé la identidad por la página de origen (nombre en la wiki o rótulo del PNJ en el juego).

**Aviso de montaje (afecta a 3 puestos):** tres mapas duran demasiado y taparían los clips nuevos si el mapa va a pantalla completa:
- s15: el mapa va de «La caja está en las coordenadas» a «…orilla del lago|fin» (~30 s, beats 063-066). Propuesta: `a=("Y no la vas a ver desde la orilla", .2)`. El punto de Khara se queda fuera; en su lugar entran el clip y la `pant` de Khara.
- s14: el mapa va hasta «…pasaba sin ver|fin». Propuesta: `a=("mirar frente a unas chozas|fin", .3)`, para que el cadáver se vea en el clip.
- s11: el mapa va hasta «…se encerró a sí mismo|fin» y tapa el clip 097, que ya enseña el muro y Gilneas detrás. Propuesta: `a=("el Muro de Cringris|fin", .3)`.

## s15 · Plata de las olas (caja de pesca hundida, Loch Modan)
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s15_1 | «En Loch Modan, en el fondo» | «de pesca abandonada» | clip nuevo scene-062 | `_local: _dl/img_B/clip_s15_lago.mp4`, desde 0 | el lago de Loch Modan con niebla: nada y se sumerge (WoW Forever) |
| s15_2 (2.ª mitad) | «hay que meterse al agua» | fin del beat | clip nuevo scene-063 | `_local: _dl/img_B/clip_s15_caja.mp4`, desde 0 | bajo el agua, frente a la caja (marca «!»); sale después del mapa recortado |
| s15_3 | «Para llegar hay que bucear» | «sal más rápido» | clip nuevo scene-064 | `_local: _dl/img_B/clip_s15_caja.mp4`, desde 18 | fondo del lago; abajo se lee la placa roja «Young Threshadon» (el trillón). Hoy sale una casa por dentro, que no tiene nada que ver |
| s15_3 | «Para llegar hay que bucear» | +3 s | pant (zoom lento) | `s15_caja_fondo` | la caja en el fondo turbio, con el trillón. Se distingue poco: úsala solo si el clip no basta |
| s15_4-5 | «con dos iniciales grabadas: K punto D» | «Así se esconde un secreto» | pegatina GRANDE (tam ≥ 650, `rel`/`legajo`) | `s15_mision_plata` | la ventana real de la misión «Silver of the Waves»: el pasador de plata con el monograma «K.D.» y el premio Repurposed Hair Band. Va después del legajo actual, o lo sustituye (el legajo lleva el icono de la muñequera, no del pasador) |
| s15_6 | «Esas iniciales son de Khara» | «misión oculta» | pant | `s15_khara_orilla` | Khara Deepwater con su rótulo <Fishing Supplies> en la orilla. Sustituye al `pv` pequeño de khara.png |
| s15_7 | «Es una misión que no aparece» | «del fondo del lago» | clip nuevo scene-067 | `_local: _dl/img_B/clip_s15_caja.mp4`, desde 8 | la ventana de la misión se abre desde la caja, bajo el agua: «la empieza un objeto» (quitar desde 16, donde abre el mapa) |
| s15_8 | «Se la devuelves» | «vale la pena el chapuzón» | clip nuevo scene-068 | `_local: _dl/img_B/clip_s15_lago.mp4`, desde 14 (o `clip_s15_khara.mp4`, desde 0) | sale del lago y le entrega la misión a Khara (+1 550 PX en pantalla); el `pv` de la muñequera queda encima |

Ya bien: s15_0 (pv o_munequera), el mapa de s15_2 recortado y el `pv` de la muñequera de s15_8.
Falta (opcional): la caja nítida. En todas las guías el agua está turbia. Si se quiere, Flow con ingredientes `s15_caja_fondo` + caja de pesca de WoW, rótulo «RECREACIÓN».

## s14 · ¿Dónde está la esposa de Mankrik?
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s14_1 | «En el Cruce, en Los Baldíos» | «hay un orco que no descansa» | pant | `s14_mankrik_choza` | Mankrik junto a su choza en el Cruce, de día (Classic). Sustituye a `pv(... "cruce")`: cruce.png es un Cruce de noche, en llamas, que no es el de Classic |
| s14_1-2 | «Mankrik. Los jabaespines» | «algo muy simple» | clip nuevo scene-073 | url `https://www.youtube.com/watch?v=ZnB6vJ00HWk`, desde 98 | llega a Mankrik en el Cruce, con el «?» y la ventana de «Lost in Battle» (Classic 2019, sin webcam). Hoy sale una selva con palmeras |
| s14_1 (alt.) | «hay un orco que no descansa: Mankrik» | +4 s | pegatina (camafeo) | `s14_mankrik_juego` | modelo de Mankrik en el juego; úsalo si se prefiere a la `pant` |
| s14_4 | «Y lo que encuentras no se llama Olgra» | «pasaba sin ver» | clip nuevo scene-075 | url `https://www.youtube.com/watch?v=agqWuSUXrbQ`, desde 46 | junto a las chozas: clic en «Beaten Corpse», ventana del cadáver y «Objective Complete: Find Mankrik's Wife» (Forever) |
| s14_5 | «Así nació el primer gran meme» | «todo el mundo preguntaba» | pegatina GRANDE | `s14_there` | el mapa-meme «THERE» de Wowhead que señala dónde está la esposa |
| s14_6-7 | «Y muchos la hacían solo para molestar» | «hasta hubo camisetas» | clip nuevo scene-078 | url `https://www.youtube.com/watch?v=Irqs2bSD4O4`, desde 15 | Los Baldíos de WoW Forever. El clip actual (qoA-h5j1Ed0 s60) tiene la WEBCAM del streamer abajo a la izquierda |
| s14_8 | «Mankrik acabó enterrando a su esposa» | «un monumento» | pegatina grande | `s14_olgra_tumba` | el cuerpo de Olgra amortajado con flores en Grol'dom (Cataclysm) |
| s14_9 | «Pero en Forever, la misión original» | «dónde buscar» | clip nuevo scene-080 | url `https://www.youtube.com/watch?v=Irqs2bSD4O4`, desde 60 | Cruce de Forever: entrega de «Lost in Battle» a Mankrik. El clip actual (qoA-h5j1Ed0 s200) también tiene WEBCAM |

Ya bien: rel olgra (título), el mapa recortado, el chat MG, la tarjeta «nivel 14», `pv` Olgra y Mankrik de Hearthstone en «Incluso salió en Hearthstone».
Falta: «hasta hubo camisetas». No encontré una foto real de la camiseta (Jinx, «Where's Mankrik's wife?»). Hay que buscar la foto del producto o cambiar la frase.

## s13 · Eitrigg
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s13_1-2 | «hay un orco viejo: Eitrigg» | «sin mirarlo» | clip nuevo scene-082 | url `https://www.youtube.com/watch?v=DC8Kh2eGJnw`, desde 143 | dentro del Bastión de Grommash (Classic 2020, cliente en español): Eitrigg con su rótulo y «?», la alfombra roja. Hoy sale Orgrimmar por fuera |
| s13_1 (alt.) | «hay un orco viejo: Eitrigg» | +4 s | pant | `s13_eitrigg_bastion` | cuadro fijo de Eitrigg en el Bastión (oscuro; mejor el clip) |
| s13_3 | «Ese paladín era Tirion» | +3,6 s | camafeo (cambio de slug) | `s13_tirion_paladin` | Tirion de paladín, modelo del juego (713x900). Sustituye a tirion.png, que mide 248 px y parece ilustración |
| s13_6 | «puede entrar al Bastión y quedarse» | fin | clip nuevo scene-086 | url `https://www.youtube.com/watch?v=DC8Kh2eGJnw`, desde 138 | cruza la puerta («Fuerte Grommash» en pantalla) y se planta frente a Eitrigg |

Ya bien: pv eitrigg (título), el mapa de Orgrimmar, los clips de Orgrimmar 081/083/084/085/087.
Falta: «junto a Thrall». Thrall no sale en ningún plano y la única imagen de la carpeta es arte de *Afterlives*, no del juego. Hace falta una captura de Thrall en su trono del Bastión (Classic).

## s12 · Aldea Piroleña
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s12_1 | «está la Aldea Piroleña, un pueblo» | «y su consejo» | pegatina GRANDE (tam ≈ 750, mide 799 px) | `s12_pirolena_dia` | la aldea de día, calle y casas (antes de Cataclysm). Hoy el clip es bosque oscuro |
| s12_1 (fin) | «con su herrero, su sastre y su consejo» | fin del beat | clip nuevo scene-088 | url `https://www.youtube.com/watch?v=Z6McskqeeYM`, desde 163 | el ayuntamiento con los rótulos «Lord Mayor Morrison» y «Pyrewood Council» (Classic) |
| s12_5 | «Desde el castillo que domina el pueblo» | «maldijo a sus vecinos» | pegatina grande sobre el mapa (o pant si el mapa se corta antes) | `s12_colmillo_castillo` | el castillo de Colmillo Oscuro sobre el acantilado. Debajo, el clip 092 es una viñeta de cómic: si el mapa no lo tapa entero, hay que cambiarlo |
| s12_8-9 | «Pero en Forever, la maldición sigue» | «A las nueve» | clip nuevo scene-095 | url `https://www.youtube.com/watch?v=sL7X7f8yYbQ`, desde 68 | Piroleña de noche en WoW Forever (puente y casas). El clip actual, ophzXhk_82M s180, es un video de lore: torre del reloj de Gilneas y arte de Arugal que no es del juego |

Ya bien: rel pyre_vigia, el reloj 21:00, el vs vigía/Moonrage, el mapa con Faerleia, Arugal y Morrison, el clip del ayuntamiento 090/093 (se ven Faerleia y el consejo) y la tarjeta de Cataclysm.
Falta: s12_7 «un pueblo lleno de huargen en lugar de humanos» (beat 094). El clip sL7X7f8yYbQ s120 son humanos (el chat dice «Pyrewood Elder… in fear»), no huargen, y no encontré ningún video con la aldea transformada. Propongo Flow con ingredientes `s12_pirolena_dia` + `moonrage.png` («Piroleña de noche llena de huargen Moonrage», estilo Classic, rótulo «RECREACIÓN»). Mínimo provisional: `pv` grande de moonrage, aunque mide 268 px.

## s11 · Gilneas / Muro de Cringris
| frase | empieza en | hasta | tipo | slug / url+desde | qué se ve |
|---|---|---|---|---|---|
| s11_5 | «encontraron una fila de campo de batalla» | «Todavía no se puede entrar» | pegatina grande | `s11_bg_gilneas` | la pantalla de carga real del campo de batalla de Gilneas (logo de Cataclysm), junto a la tarjeta «Gilneas en los archivos» |
| s11_6 | «a nivel quince ya puedes plantarte frente al muro» | «en lo que viene» | pant | `s11_muro_frente` | la puerta del muro cerrada, de frente. Hoy el beat 101 abre con arte de un huargen |

Ya bien: pv muro (título), el clip 097 (muro y Gilneas detrás; que se vea, ver el aviso de montaje), el camafeo de Genn (modelo del juego posterior, porque Genn no existe en Classic), el clip 099 y la tarjeta «Gilneas en los archivos». El arte de Cataclysm de s11_7 («sabemos lo que hay detrás») encaja.
