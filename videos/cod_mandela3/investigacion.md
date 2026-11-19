# Investigación: «20 EFECTOS MANDELA de Call of Duty, parte 3» (Expediente 141)

Fecha: 19-nov-2026 · Formato: cuenta regresiva de 20, ~15 min · Base: `videos/cod_mandela/investigacion.md` (parte 1), `videos/cod_mandela2/investigacion.md` (parte 2) y los `p..` de `videos/cod_misterios/guion.py`. No repite nada de lo usado allí: Shepherd y el cuchillo, Zakhaev, Ghost/Roach y Bravo Six ya salieron en la parte 1. La AUG, Weaver, «Frank, soy yo, Mason», la perk de Moon, Hoover, el armario, «Lullaby» y la Wunderwaffe salieron en la parte 2.

**Cómo verifiqué:** wiki de CoD por su API (`callofduty.fandom.com/api.php?action=parse&prop=wikitext`), con transcripciones de misiones. Reddit, con el archivo **arctic-shift**: búsquedas por título, el post completo y sus comentarios con votos. Ojo: la búsqueda de texto en comentarios de los subs grandes da *timeout*, así que donde no había hilo busqué testimonios en los **comentarios de YouTube** con `yt-dlp --write-comments`. Las frases las confirmé con **faster-whisper `small` en CPU** y con subtítulos automáticos. Los cuadros los miré en hojas de contacto a 320 px (ffmpeg) sobre tramos bajados con `yt-dlp --download-sections`.
**Confianza:** **ALTA** = fuente primaria (wiki o transcripción, o un cuadro o audio del juego que revisé) · **MEDIA** = varios testimonios o una fuente secundaria fiable, sin fuente primaria del recuerdo · **BAJA** = un solo testimonio o sin comprobar.
**Clips:** «✔ cuadro» = miré el fotograma · «✔ audio» = segundo confirmado con Whisper o subtítulos · «≈» = video candidato con el segundo aproximado: confirmarlo en `bajar`.
**TCRF:** no lo usé.
**Violencia:** el n.º 1 (disparo a Menéndez), el n.º 4 («No Russian») y el clip de Ghost (Shepherd dispara en 0:53) se cortan ANTES del disparo. En «No Russian», solo el ascensor y la frase, nunca la terminal.

---

## A. LOS 2 EFECTOS DE LOS ESPECTADORES (van sí o sí)

### A1. @gxlfredo07: «un solo zombi me seguía por todo el Nuketown colorido de BO1»
- **Lo que recuerda:** de niño, jugar Nuketown con zombis. No en el mapa de zombis de BO2, sino en el Nuketown normal y colorido de Black Ops 1, y con UN solo zombi que lo seguía por todo el mapa.
- **En realidad:** el Nuketown de **Black Ops 1 (2010) nunca tuvo zombis.** Su Easter egg de maniquíes es otro: si les vuelas la cabeza a todos en los primeros 15 segundos, suena «Sympathy for the Devil» (Rolling Stones). Nuketown Zombies (BO2) usa el Nuketown de los años 60, pero quemado y apocalíptico.
- **De dónde viene la confusión (hay DOS candidatos reales, y uno encaja casi palabra por palabra):**
  1. **Alpha Omega (Black Ops 4, julio de 2019):** es Nuketown ANTES de la bomba, con las casas de colores de los años 50. Si le quitas la cabeza **con el cuchillo** a los 30 A.D.A.M. (los maniquíes robot), **aparece UN A.D.A.M. detrás del letrero de Nuketown que actúa como zombi y te sigue por el mapa, pero se congela cuando lo miras** («Weeping Angel», como los ángeles de *Doctor Who*). Es inmune. Solo se va si lo llevas con la A.D.A.M. mujer de la sala de generadores, y entonces te dan un Self-Revive. Además hay **un zombi solitario en el desierto detrás de la casa verde que imita tu aspecto**.
  2. **Nuk3town (Black Ops 3, 2015):** si les quitas la cabeza a todos los maniquíes en los 2 primeros minutos, **cobran vida y te persiguen como zombis** (suena la campana del cambio de ronda). Si les quitas los BRAZOS, te siguen solo cuando no los miras, otra vez como los ángeles llorosos. El mapa es la versión 2065, pero brillante y llena de color.
  - Conclusión para el guion: no lo soñaste. Viste un Nuketown soleado con un maniquí-zombi que te seguía. Solo que no era BO1: era BO3 o, sobre todo, BO4.
- **Prueba:** Mannequin https://callofduty.fandom.com/wiki/Mannequin («Knifing the heads off them all will cause a male A.D.A.M. unit to follow the player in a fashion similar to Weeping Angels»; BO1: «Sympathy for the Devil») · Alpha Omega https://callofduty.fandom.com/wiki/Alpha_Omega (estreno 9-jul-2019; «will spawn an A.D.A.M. behind the Nuketown sign, who will act as a zombie, but will freeze in place when looked at»; «a lone zombie… that mimics the player's appearance») · Nuk3town https://callofduty.fandom.com/wiki/Nuk3town · Nuketown Zombies https://callofduty.fandom.com/wiki/Nuketown_Zombies · **Confianza: ALTA** (los dos Easter eggs y que BO1 no tiene zombis). Que esto sea lo que él vio es deducción nuestra: decirlo como «lo más probable».
- **Clip:** Alpha Omega, `HiyklPTA7QE` (Laggin24x, «What's Really In This Shed??») **0:45** ✔ cuadro: un A.D.A.M. de traje de pie junto a una casa de colores bajo el sol. **1:25** ✔ cuadro: los dos A.D.A.M. juntos en el cobertizo. Guía con todos los Easter eggs: `ltRbTs8Hi8M` (MrRoflWaffles, 153 k) ≈ · Nuk3town, `fcWwAgqO0kg` (It's Just Nico, 1,9 M, los 3 Easter eggs) **5:10-5:50** ✔ cuadro: maniquí-zombi de frente al jugador. Respaldo: `H_9wFkKg0tY` (5 M) ≈.
- **Pegatinas:** Nuketown de BO1 (las dos casas, verde y amarilla), un maniquí, un A.D.A.M. de Alpha Omega, el ángel lloroso (silueta genérica, sin la marca de *Doctor Who*), el letrero «Nuketown», el comentario de @gxlfredo07.

### A2. @rafaeltroconis6615: «Mason perdonó a Menéndez y el final de BO2 era encerrándolo en prisión»
- **Lo que recuerda:** antes de BO7 juraba que Mason perdonó a Menéndez y que Black Ops II terminaba con Menéndez en la cárcel.
- **En realidad:** **ese final EXISTE.** En «Judgment Day» el jugador, como **David «Section» Mason** (no Alex), decide si mata a Menéndez o lo captura. Si lo perdona, se lo llevan detenido y le dice a David que estudie el *Ulises* y que lo espere, que se escapará en un año. Lo que pasa después depende de Chloe (Karma):
  - **Chloe viva:** bloquea el plan de fuga. Un año después, Menéndez la ve en un programa de televisión y **se golpea la cabeza contra la tele de su celda** hasta que se ríe.
  - **Chloe muerta:** escapa, mata a Woods en la residencia (The Vault) y se quema en la tumba de su hermana.
  - **Canon:** Treyarch, en su línea de tiempo oficial, dice que **David lo mata** el 19-jun-2025 cuando intentaba huir disfrazado de soldado. Y **Black Ops 7** lo confirma: David «había acabado con su vida diez años antes». El Menéndez de 2035 es un ***deepfake* de IA** encargado por Emma Kagan (The Guild) y una alucinación del gas Cradle. En BO6 ya salía en las teles de Verdansk diciendo que estaba «vivo y bien».
  - Conclusión para el guion: tu recuerdo es un final real, pero no el oficial. Y BO7 jugó contigo: lo «revivió»… y era mentira.
- **Prueba:** https://callofduty.fandom.com/wiki/Raul_Menendez (estado: «K.I.A. (canon)… Incarcerated (non-canon)»; «If the player spares Menendez… put into U.S. custody… study Ulysses»; «If Chloe is alive… bash his head against the T.V.»; BO7: «David Mason, who had personally put an end to Menendez's life ten years before»; «Menendez was a highly advanced AI deepfake commissioned by… Emma Kagan»; BO6 Verdansk: «alive and well») · línea de tiempo de Treyarch `bVEbYbYd2ZE` · reacción a Fellow `D7fGnfBK2Yw` ~3:40 («Menéndez is somehow resurrected from the dead» en BO7) · **Confianza: ALTA.**
- **Clip:** final con captura `EMHd0VYb2pg` (A Fernandez, «Black Ops 2 Ending (Capture Menendez)») **3:05** ✔ cuadro: la tele en la pared de la celda. **3:15-3:35** ✔ cuadro: Menéndez con uniforme naranja dentro de la celda, con guardia. Antes, **2:00** ✔ cuadro: Menéndez capturado, en primer plano junto a un soldado. · Línea de tiempo oficial `bVEbYbYd2ZE` (Treyarch, 339 k) **10:25-10:28** ✔ cuadro: el texto «JUNE 19, 2025 — RAUL MENENDEZ IS KILLED BY U.S. SPECIAL FORCES WHILE TRYING TO ESCAPE…». · Final matándolo `38ALMyxA48A` (calloftreyarch, 460 k) ≈: **cortar antes del disparo**. · BO7, Menéndez amenaza: `lIKETU6q9rA` ≈ · en español latino `myE8i4s-e1w` («Raúl Menéndez's last message (Black Ops 7)») ≈: **OÍRLO** si dice algo de «volver».
- **Pegatinas:** Raúl Menéndez (BO2, traje blanco), Menéndez de BO7 (traje negro), David «Section» Mason, Chloe «Karma» Lynch, la celda, el *Ulises* (libro), Emma Kagan, el letrero «DEEPFAKE», el comentario de @rafaeltroconis6615.

---

## B. RANKING RECOMENDADO DE 20 (n.º 1 = el más impactante y demostrable)

### 20. Gaz SÍ sale en Modern Warfare 2 (2009)… 3 segundos
- **Recuerdan (dos bandos):** que Gaz está en el 141 de MW2 (es el Gaz del reinicio de 2022), o que Gaz no sale para nada en el MW2 original.
- **En realidad:** en MW2 (2009) Gaz está muerto (lo mata Zakhaev en «Game Over», CoD 4). Pero **aparece en la cinemática de introducción de MW2**, que repasa lo de CoD 4. En la campaña no está.
- **Prueba:** https://callofduty.fandom.com/wiki/Gaz (juegos: «Call of Duty: Modern Warfare 2 (intro cutscene)»; «killed by Imran Zakhaev with a Desert Eagle») · **Confianza: ALTA** (el hecho), **BAJA** como Mandela (no encontré ningún hilo que lo discuta). Usarlo como pregunta al público.
- **Clip:** intro de MW2 (2009) ≈ (no buscado) · Gaz de 2022 `acDGnS0u7TE` ≈.
- **Pegatinas:** Gaz de CoD 4 (gorra), Gaz de 2022, logo del 141.

### 19. Max Ammo no te llenaba el cargador (hasta 2018)
- **Recuerdan:** que Max Ammo siempre rellenó también el cargador que llevabas puesto. Los veteranos recuerdan lo contrario y todavía recargan antes de agarrarlo.
- **En realidad:** en WaW, BO1, BO2 y BO3 **solo rellenaba la reserva, no el cargador puesto.** El cambio llegó con **Black Ops 4**. Los dos bandos tienen razón según el juego que jugaron.
- **Prueba:** https://callofduty.fandom.com/wiki/Max_Ammo («Prior to Call of Duty: Black Ops 4, the player's current magazine will not be replenished») · r/CODZombies «Anyone still have the habit of reloading before picking up a max ammo despite no longer being necessary since BO4?» (**1819 votos**, 96 comentarios) https://www.reddit.com/r/CODZombies/comments/1h4itfx/ · **Confianza: ALTA** (el hecho), MEDIA (el «recuerdo»: es más una costumbre que un efecto Mandela).
- **Clip:** Max Ammo en BO1 con el cargador a medias ≈ (no buscado).
- **Pegatinas:** el icono de Max Ammo, un cargador medio vacío, el logo de BO4.

### 18. El tercer camión de Nacht der Untoten
- **Recuerda:** un camión volcado frente a una ventana de Nacht (WaW) que «ahora ya no está».
- **En realidad:** nunca hubo un camión en ese sitio. Quien juega dice que en esa ventana solo hay barriles, y que el **remake de BO3 (Zombies Chronicles) tiene tanques**: de ahí la mezcla.
- **Prueba:** r/CallOfDuty «[WAW] Possible new mandela effect? Truck its side on nacht now missing?» (14 votos, 13 comentarios) https://www.reddit.com/r/CallOfDuty/comments/16i7vds/ · r/CODZombies «Third truck on nacht gone?» https://www.reddit.com/r/CODZombies/comments/1ae4reu/ · **Confianza: MEDIA-BAJA** (solo comentarios; no lo comprobé en el mapa).
- **Clip:** Nacht en WaW, vista desde la ventana ≈ · Nacht de BO3 con tanques ≈.
- **Pegatinas:** camión Opel Blitz, tanque, la ventana tablada.

### 17. Speed Cola en el balcón de la Granja (TranZit)
- **Recuerdan:** Speed Cola en el balcón de la casa de la Granja de TranZit, con su jingle sonando arriba, y Double Tap en el restaurante.
- **En realidad:** en TranZit, en la Granja está **Double Tap** (piso de arriba del granero). **Speed Cola sí está en la Granja, pero en los modos Supervivencia/Grief** (la versión pequeña del mapa), y abajo, en la casa (según la parte 2; no revisé qué hay en el restaurante).
- **Prueba:** https://callofduty.fandom.com/wiki/Farm · r/CODZombies (comentario: «I always thought Speed Cola was on the farm house balcony in TranZit… I even vividly remember hearing its jingle for the first time on the balcony») https://www.reddit.com/r/CODZombies/comments/wa1urm/ · Drrpy `g8n6YhAzlRs` 11:17 · **Confianza: MEDIA** (dos fuentes; viene de los suplentes de la parte 2).
- **Clip:** TranZit, granja, piso de arriba del granero ≈ · Farm Supervivencia, Speed Cola en la casa ≈.
- **Pegatinas:** máquina de Speed Cola, máquina de Double Tap, el autobús de TranZit.

### 16. El zombi que se come al hombre del menú de BO1
- **Recuerdan:** que al entrar en Zombis desde el menú de Black Ops, un zombi entraba y se comía al hombre de la ventana. Otro, que en 4 teles se formaba un video de un hombre devorado por zombis.
- **En realidad (lo más citado):** al elegir «ZOMBIES», **Hudson (el de detrás del cristal) sale de la sala y vuelve golpeando la ventana**: el ataque pasa fuera de cámara.
- **Prueba:** r/CODZombies (varios comentarios: «there was a zombie that would come and eat the guy»; «4 of the TVs would make one video together showing a guy on the floor being eaten»; respuesta: «Hudson… leaves the room and then comes back, banging on the window») https://www.reddit.com/r/CODZombies/comments/wa1urm/ · **Confianza: MEDIA** (hay versiones opuestas; no lo vi en un video limpio).
- **Clip:** menú de BO1 (teles) `apBWd1FLK9s` (JackyZ, 3,2 M) **0:10-2:55** ✔ cuadro: solo las teles del cuarto de interrogatorio, sin el momento del zombi · menú en modo zombi `tc_O7NlHmZE` (294 k) ≈. Hay que encontrar el momento en `bajar` antes de usarlo como «prueba».
- **Pegatinas:** las teles del menú de BO1, la silla de interrogatorio, Hudson.

### 15. La «carne» que atraía a los zombis sí existió
- **Recuerda:** un *power-up* de BO2 en los mapas de TranZit: un trozo de carne cruda que lanzabas y atraía a los zombis como el mono, pero sin explotar. «¿Me lo inventé?».
- **En realidad:** existe. Es la **Zombie Flesh**, exclusiva del modo **Grief** de BO2. Se la tiras a un rival y los zombis lo persiguen 30 segundos (15 si cae al suelo). Si la atrapas de un golpe, «catching the meat», te frena a la mitad.
- **Prueba:** https://callofduty.fandom.com/wiki/Zombie_Flesh · r/CODZombies «Meat powerup mandela effect» https://www.reddit.com/r/CODZombies/comments/12jxq7r/ · **Confianza: ALTA** (que existe), BAJA (un solo hilo).
- **Clip:** `KgaSo84nZLc` («Grief New Power-Up (Zombie Flesh)», 65 s) ≈ · `aZj37c7ZJMM` («Black Ops II meat power-up Grief», 40 s) ≈.
- **Pegatinas:** la Zombie Flesh, el mono, el logo de Grief (CDC vs CIA).

### 14. Extinction nunca fue de Battlefield 4
- **Recuerda:** que *Extinction*, el modo de aliens, era la respuesta de Battlefield 4 a los zombis de CoD.
- **En realidad:** es un modo de **Call of Duty: Ghosts (2013)**, de Infinity Ward: cuatro jugadores contra los Cryptids. (La confusión viene, según él, de un juego prestado por un amigo de su hermano.)
- **Prueba:** https://callofduty.fandom.com/wiki/Extinction · r/CallOfDuty (comentario con **104 votos**: «I used to believe Extinction was actually a Battlefield 4 game mode and not a Ghosts gamemode») https://www.reddit.com/r/CallOfDuty/comments/1va89h3/ · **Confianza: ALTA** (el hecho), MEDIA (un testimonio muy votado).
- **Clip:** `YSSDG-Cyyi8` (NoAnnoyingCommentary Z, 232 k, sin comentario) ≈.
- **Pegatinas:** un Cryptid, portada de Ghosts, logo de BF4.

### 13. Reznov nunca dijo «pronto será su tierra»: son dos frases de dos misiones
- **Recuerda:** a Reznov en *World at War* diciendo «Soon it will be their land…».
- **En realidad:** son **dos frases distintas**. En «Vendetta» (Stalingrado): ***«…we will take the fight to their land… to their people… to their blood.»*** En «Their Land, Their Blood» (Alemania): ***«See how things have changed, my friend? Now it is their land… Their people… Their blood.»*** La memoria las fundió.
- **Prueba:** https://callofduty.fandom.com/wiki/Vendetta/Transcript · https://callofduty.fandom.com/wiki/Their_Land,_Their_Blood/Transcript · r/CallOfDuty «COD 5 Mandela Effect has me shook» (con encuesta) https://www.reddit.com/r/CallOfDuty/comments/1f2kqnj/ · **Confianza: ALTA** (las frases), BAJA (un hilo).
- **Clip (OÍRLO):** «Vendetta» `2UAvWQgRRXQ` (fabi, 16 k) **0:24-0:33** ✔ audio (subtítulos: «one day things would change, we would take the fight to their land, to their people, to their blood») · «Their Land, Their Blood» `cnpYaxw8Q9A` (DraKulis, 8K) **2:41-2:48** ✔ audio con Whisper («See how things have changed, my friend? Now it is their land. Their people…»).
- **Pegatinas:** Viktor Reznov (WaW), Dimitri Petrenko, bandera roja sobre el Reichstag.

### 12. One in the Chamber siempre tuvo 3 vidas
- **Recuerdan:** que One in the Chamber era un todos contra todos a 30 bajas, sin vidas.
- **En realidad:** desde que nació (Black Ops, 2010, apuestas): pistola, una bala, cuchillo y **tres vidas**. Lo que mezclan es *Sticks and Stones* o que, en MW2 (2022), la partida sigue con gente que entra.
- **Prueba:** https://callofduty.fandom.com/wiki/One_in_the_Chamber («Each player is given three lives») · r/ModernWarfareII «Mandela effect for one in the chamber» (9 comentarios, varios «THIS IS EXACTLY HOW I REMEMBER IT») https://www.reddit.com/r/ModernWarfareII/comments/1237j54/ · **Confianza: ALTA** (el hecho), MEDIA (varios testimonios en un hilo pequeño).
- **Clip:** One in the Chamber de BO1 con el contador de vidas ≈ (no buscado).
- **Pegatinas:** M1911 con una bala, el corazón de las vidas «x3», el *tomahawk* de Sticks and Stones.

### 11. Ghost nunca llevó la bufanda
- **Recuerdan:** a Ghost (MW2, 2009) con la bufanda o *shemagh* blanca y negra de los disfraces y *cosplays*. Uno lo descubrió en una foto suya disfrazado de niño.
- **En realidad:** el Ghost original **nunca la llevó en ninguna misión**: pasamontañas de calavera, gafas y auriculares. La bufanda viene de una sesión de fotos o *cosplay* muy famosa (y de que el *shemagh* estaba de moda en el airsoft). El Ghost moderno sí tiene aspectos con algo parecido.
- **Prueba:** r/modernwarfare «Ghost wearing a scarf?» (**57 votos**, 17 comentarios: «OG Ghost never wore one»; «he never wore one in a single mission. In my mind he always wore one») https://www.reddit.com/r/modernwarfare/comments/18644rn/ · **Confianza: MEDIA** (comunidad, sin fuente primaria; lo visual se puede comprobar).
- **Clip:** Ghost de 2009 en «Loose Ends» `mv88YFoq2rc` **0:40** ✔ cuadro: Ghost de frente, pasamontañas de calavera, sin bufanda visible a 320 px (confirmarlo a 720p). **Cortar antes de 0:53** (Shepherd dispara).
- **Pegatinas:** Ghost (2009), un *shemagh* tachado, un disfraz de Halloween (Flow, genérico, sin persona real).

### 10. El Capitán Price de la Segunda Guerra Mundial no es el de Modern Warfare
- **Recuerdan o creen:** que el Price de CoD 1 y CoD 2 (bigote, boina) es el mismo Price de CoD 4. En los comentarios hay teorías de que «los alemanes experimentaron con él y lo hicieron inmortal».
- **En realidad:** son dos personajes. El Price de la Segunda Guerra **muere el 27-oct-1944** saboteando el acorazado **Tirpitz** (última misión británica de CoD 1). El sargento Waters dice que fue «a very fine man». El John Price de CoD 4 es otro. Que sean familia (abuelo y nieto) **nunca se confirmó**: es teoría de fans. Guiños reales: un emblema y una carta de MW2 (2009) con el Price de la Segunda Guerra, el aspecto «Old School Price» de MW2 (2022), y que en el pre-alfa de CoD 4 a Price lo doblaba Michael Gough, la voz del Price de la Segunda Guerra.
- **Prueba:** https://callofduty.fandom.com/wiki/Price_(World_War_II) (estado: K.I.A.; Tirpitz) · https://callofduty.fandom.com/wiki/John_Price (Michael Gough en el pre-alfa) · Inkslasher «The Price Family Legacy» (`U6bq7GkHtOA`, 995 k; comentario de @DizzBeans, 461 likes, con la teoría del Price inmortal) · **Confianza: ALTA** (los hechos), MEDIA (la creencia).
- **Clip:** CoD 1, Tirpitz `ZvfhyaBxoiY` (JoshuaPare, «Did You Know Captain Price Dies In Call of Duty 1», 18 k) **0:00-0:23** ✔ audio (el control de papeles: «May I have a look at your papers?»), la muerte ≈ al final · `-uptI7C5Zhw` («Battleship Tirpitz (Captain Price Dies)», sin comentario) ≈ final.
- **Pegatinas:** Price de la Segunda Guerra (boina y bigote), Price de CoD 4 (gorro *boonie*), el acorazado Tirpitz, «1944».

### 9. El poste de Piccadilly: el «letrero de Standoff» de Modern Warfare (2019)
- **Recuerdan:** en abril de 2020, medio CoD (incluido el profesional Clayster) juró que el semáforo entre los autobuses de Piccadilly era nuevo: «nunca tuve que esquivarlo al disparar».
- **En realidad:** estaba desde el principio. Sale en el tráiler de seis meses antes y en partidas de diciembre de 2019.
- **Prueba:** r/Retconned «Any Call of Duty fans?» (16 votos, 20 comentarios; cita los tuits de @matthecodkingg y de Clayster; «The pole is literally in the game trailer from 6 months ago») https://www.reddit.com/r/Retconned/comments/g4msz9/ · mapa https://callofduty.fandom.com/wiki/Piccadilly_(map) · **Confianza: MEDIA** (no encontré el cuadro).
- **Clip:** tráiler multijugador `J7Ivdq5E-fs` (tiene restricción de edad; yt-dlp no lo baja sin *cookies*) → alternativa `bSO0CWrmWpg` (PlayStation Europe) ≈ · partida en Piccadilly sin comentario `lv90arMX8KU` ≈ buscar los autobuses.
- **Pegatinas:** el semáforo, autobús rojo de dos pisos, logo de MW (2019), «abril de 2020».

### 8. Mule Kick en Nacht der Untoten: depende de si estabas conectado
- **Recuerdan (dos bandos):** unos juran que Nacht no tiene perks; otros, que tenía Mule Kick.
- **En realidad:** **los dos tienen razón.** En WaW, Nacht no tiene ninguna perk. En Black Ops, el parche del 27-sep-2011 (PC, 11-oct, parche 1.15) puso Mule Kick en TODOS los mapas, a la izquierda de la M1 Carbine en la sala inicial de Nacht, **pero solo si estabas conectado** a PSN, Xbox Live o Steam. Sin conexión, Mule Kick solo salía en Moon. En BO3 (Zombies Chronicles) hay Mule Kick y Der Wunderfizz.
- **Prueba:** https://callofduty.fandom.com/wiki/Mule_Kick («the player must be connected to PlayStation Network, Steam or Xbox LIVE for Mule Kick to appear on other maps than Moon») · https://callofduty.fandom.com/wiki/Nacht_der_Untoten · r/CallOfDuty (comentarios: «Is there a Mule Kick in Nacht Der Untoten, or is there no perks?» / «If you Local/Offline. There's no Perks. If you play Online… Mule kick will be present on Nacht») https://www.reddit.com/r/CallOfDuty/comments/1va89h3/ · **Confianza: ALTA.**
- **Clip:** `3Frj5cEjhrw` (MrDalekJD, «Nacht Der Untoten - MULE KICK PERK ADDED INTO MAP!», 13 k) **0:29-0:36** ✔ cuadro: la máquina verde de Mule Kick en la sala inicial y «Hold to buy Mule Kick [Cost: 4000]».
- **Pegatinas:** máquina de Mule Kick, Nacht der Untoten, icono de «conectado/desconectado», Der Wunderfizz.

### 7. «Cincuenta mil personas vivían aquí»: la frase famosa es del menú, no de la misión
- **Recuerdan:** a MacMillan en «All Ghillied Up» diciendo «Forty-five thousand people used to live here…», o «…now it's a f\*\*\*ing ghost town».
- **En realidad:** son 50 000 y sin palabrota. Y hay un detalle que casi nadie nota: la versión que todos citan, ***«Fifty thousand people used to live here… now it's a ghost town»***, es la del **video del menú principal** de CoD 4, el que sale antes del título (en Reddit: «#SKIP! Main menu»). En la misión dice: ***«Look at this place… Fifty thousand people used to live in this city. Now it's a ghost town… I've never seen anything like it.»*** La palabrota viene de Shepherd en MW2 (*«…and the world just f\*\*\*ing watched»*).
- **Prueba:** https://callofduty.fandom.com/wiki/All_Ghillied_Up/Transcript · r/MandelaEffect «50k or 45k in Call of Duty 4» (sus primos también lo recuerdan como 45 000) https://www.reddit.com/r/MandelaEffect/comments/fkq6fx/ · r/MandelaEffect «…now it's a fucking ghost town» (6 comentarios, la explicación de Shepherd con 8 votos) https://www.reddit.com/r/MandelaEffect/comments/i93lgv/ · **Confianza: ALTA** (las frases), MEDIA (los testimonios).
- **Clip (OÍRLO):** versión del menú o intro `RRYmVb33VU0` (7 s) **0:00-0:05** ✔ audio con Whisper («50,000 people used to live here. Now it's a ghost town.»; el origen del clip es dudoso: buscar el video del menú original en `bajar`) · misión, versión remasterizada `XxemwEJDFi0` (15 s) **0:00-0:07** ✔ audio («Look at this place. 50,000 people used to live in this city.») · CoD 4 original: `pESIUgBES4Y` (11 s) **0:00-0:10** ✔ audio (la misma frase de la misión).
- **Pegatinas:** MacMillan con traje *ghillie*, la noria de Prípiat de fondo, «50 000» contra «45 000».

### 6. El mapa de zombis soleado de BO2 que «no existe»
- **Recuerda:** un mapa de zombis de BO2 o BO3 de día, soleado, con campos de hierba, bosques y pueblitos con casas, desde el que después te teletransportabas a otro sitio. Su amigo no tenía ni idea, y no lo encontraba en internet.
- **En realidad:** es **Outbreak, de Black Ops Cold War (2021)**: zombis en mapas abiertos de multijugador (Golova, Ruka, Alpine, Duga…), y un portal que te lleva a la siguiente región. Él ni siquiera tenía Cold War: lo jugó un fin de semana de acceso gratis. Lo confirmó él mismo: «I'm definitely thinking of Outbreak».
- **Prueba:** r/CODZombies «Mandela Effect about a nonexistent map?» (**378 votos**, 52 comentarios; respuesta principal «Outbreak mode, from black ops cold war», 525 votos) https://www.reddit.com/r/CODZombies/comments/1vqgx0j/ · **Confianza: ALTA.**
- **Clip:** Golova Outbreak `MP_KSkShPuk` (MichaelXboxEvolved, PS5) **2:00** ✔ cuadro (pueblo soleado de otoño con el cartel «GOLOVA OUTBREAK») · **5:00** ✔ cuadro (mismo pueblo, a pleno día).
- **Pegatinas:** mapa de Golova, el portal del Éter Oscuro, portada de Cold War, «fin de semana gratis».

### 5. La Ray Gun Mark II no estaba el día del lanzamiento de BO2
- **Recuerda:** la Ray Gun Mark II anunciada antes del lanzamiento de BO2 (nov-2012) y sacarla de la caja desde el primer día con sus amigos.
- **En realidad:** llegó **8 meses después**, con el DLC **Vengeance** (mapa Buried; Xbox 360 el 2-jul-2013, PS3/PC el 1-ago-2013), y luego se añadió a todos los mapas. El detalle que explica a los que «la vieron antes»: **en el parche 1.12 la Mark II se coló por error en todos los mapas unos días antes de Vengeance**, y la quitaron enseguida.
- **Prueba:** https://callofduty.fandom.com/wiki/Ray_Gun_Mark_II («In patch 1.12, the Ray Gun Mark II was unintentionally added to all maps prior to its official launch… but was later removed swiftly via a hotfix») · https://callofduty.fandom.com/wiki/Vengeance · r/MandelaEffect «Ray Gun Mark 2 was available from the start of Black Ops 2» (**42 votos**, 23 comentarios; «I remember it as dlc tbh.. but have a weird feeling that it came out earlier») https://www.reddit.com/r/MandelaEffect/comments/k27zwq/ · **Confianza: ALTA.**
- **Clip:** tráiler de Buried y Vengeance `SDfcmo0hlqE` **0:52** ✔ cuadro («BONUS ZOMBIES — RAY GUN MARK II») · juego temprano `IFyQe5HhMYM` («EARLY GAMEPLAY», 3 k) ≈.
- **Pegatinas:** Ray Gun Mark II, la Ray Gun original, portada de Vengeance, calendario «nov-2012 → jul-2013», «parche 1.12».

### 4. «Remember, no Russian» no significa «no dejen ningún ruso vivo»
- **Recuerdan o entendieron:** que Makárov ordena «que no quede ningún ruso».
- **En realidad:** significa **«nada de ruso»: no hablen ruso**, para que la masacre parezca obra de estadounidenses (falsa bandera; por eso deja el cadáver de Allen). Y el giro: **en Japón la frase se tradujo como 「殺せ、ロシア人だ」 («Korose, Roshia-jin da»: «Mátenlos, son rusos»)**, lo que confundió la trama. Se corrigió en *Modern Warfare 2 Campaign Remastered*. Además, la misión **no obliga a disparar**: el único objetivo es «Follow Makarov's lead», no hay ningún aviso que te pida disparar, y se puede saltar sin perder logros. En las versiones alemana y japonesa, matar a un civil te devuelve al último punto de control con el aviso «You killed a civilian!».
- **Prueba:** https://callofduty.fandom.com/wiki/No_Russian («Makarov's line… is mistranslated as "Kill them, they are Russians"… fixed in Campaign Remastered»; «the player can go through the mission without shooting any civilians») · r/CallOfDuty «How do you interpret Makarov's "No Russian" speech?» (**804 votos**, 89 comentarios: «I too thought he meant "leave no Russian alive" when I was younger») https://www.reddit.com/r/CallOfDuty/comments/1liu91i/ · **Confianza: ALTA.**
- **Clip (OÍRLO):** inglés `G7vBol8wud0` **1:33-1:38** ✔ audio (parte 1) · japonés `x7vvJm9jRVU` («○せ、ロシア人だ / No Russian», 43 s) **0:11-0:13** ✔ audio con Whisper («…ロシア人だ», con ruido), y en 0:00 «S nami Bog» · respaldo: `s0XWyxhH_KQ` («The worst mistranslated game ever», 204 k) ≈.
- **Ojo (tono y YouTube):** solo el ascensor y la frase. Ni la terminal ni civiles. Fundido en negro al abrirse las puertas.
- **Pegatinas:** Makárov, el ascensor, la bandera rusa con «sin hablar», el subtítulo japonés, Allen.

### 3. Jackson nunca le agarró la mano a Volker… en el CoD 4 original
- **Recuerdan:** que en «Shock and Awe», con la onda de la bomba, Jackson estira el brazo para salvar a un compañero que sale volando del helicóptero. Otros, verlo en primera persona agarrado y cayendo.
- **En realidad:** en **CoD 4 (2007)** el teniente **Volker** cae del Sea Knight y Jackson no hace nada. **El gesto del brazo lo añadió Modern Warfare Remastered (2016)**. Los dos bandos tienen razón, según cuál jugaron.
- **Prueba:** https://callofduty.fandom.com/wiki/Volker («In Modern Warfare Remastered… Jackson attempts to save Volker by reaching out his arm, but the centripetal forces still hurl him from the helicopter») · r/CallOfDuty (comentarios: «Didn't they add a scene of Jackson trying to save a fellow soldier… in COD 4 Remastered?» / «Yup, Lt. Volker…») https://www.reddit.com/r/CallOfDuty/comments/1va89h3/ · r/CallOfDuty «they made Sgt. Jackson value his fellow marines more by trying to save Lt Volker… unlike the OG version» https://www.reddit.com/r/CallOfDuty/comments/1nwclcl/ · **Confianza: ALTA.**
- **Clip (comparación lado a lado):** original `jB-n_8zq9Qo` (TryLink, 640 k) **0:56-1:05** ✔ cuadro (Volker en la rampa, el hongo, el helicóptero que se ladea, sin brazo) · remasterizado `4r-YtrYGAIQ` (Generic Gaming, 6,7 M) **2:36-2:48** ✔ cuadro (la rampa, el destello y «Everyone hang on!»; el brazo estirado ≈ 2:46: afinarlo).
- **Pegatinas:** Paul Jackson, Volker, el CH-46 Sea Knight, el hongo nuclear, «2007 / 2016».

### 2. El zombi que te perseguía en el Nuketown de colores
→ **A1.** Alpha Omega `HiyklPTA7QE` 0:45 y 1:25 ✔ cuadro · Nuk3town `fcWwAgqO0kg` 5:10-5:50 ✔ cuadro. **ALTA.** Enseñar el comentario de @gxlfredo07.

### 1. «Mason perdonó a Menéndez»: ese final existe… y BO7 lo enterró
→ **A2.** Celda `EMHd0VYb2pg` 3:15-3:35 ✔ cuadro · línea de tiempo de Treyarch `bVEbYbYd2ZE` 10:25-10:28 ✔ cuadro · BO7 *deepfake* ≈. **ALTA.**
- **Por qué es el n.º 1:** es de un espectador, mete a Black Ops 7 (lo más reciente), y tiene tres giros que se ven en pantalla: (1) el final que recuerda es real (la celda); (2) el oficial es el contrario (texto de Treyarch); (3) BO7 lo «resucita»… y es un *deepfake*. Remate: «Tú no te lo inventaste. Lo que te inventaron fue a Menéndez».

---

### Suplentes (por si alguno no cuaja en el montaje)
- **Makárov ahorcado** (MW3, «Dust to Dust»): hecho ALTA, Mandela BAJA. Clip `sS_wS5uhynk` (parte 1).
- **La Remington 870 en el banco de Town:** «The Bank contains no weapons, only Speed Cola» (wiki Town). Mismo comentario de `wa1urm`. MEDIA-BAJA.
- **Quick Revive comprado varias veces en solitario (BO1):** un comentario lo recuerda «como si fuera un truco», pero en solitario sí se compra hasta 3 veces. BAJA (sin comprobar la cifra en la wiki).
- **«Ghosts en Wii en 2010»:** r/MandelaEffect (16 comentarios) https://www.reddit.com/r/MandelaEffect/comments/1cnmxev/. Ghosts es de 2013 (lo dice el propio post). Lo más probable es que fuera el Black Ops de Wii, de 2010, pero no lo comprobé. BAJA.
- **DeFalco sobrevive a BO2:** comentarios (6 votos) dicen que muere siempre en «Judgment Day». No lo comprobé en la wiki. BAJA.

### Descartados (con motivo)
- **La Tactical Nuke en CoD 4:** el hecho es seguro (CoD 4 tenía UAV a 3 bajas, ataque aéreo a 5 y helicóptero a 7; la Nuke es de MW2, a 25; wiki Tactical Nuke), pero no encontré a nadie que lo recordara mal (búsquedas en r/CallOfDuty y YouTube).
- **El disparo a Zakhaev desde la noria:** el disparo es desde el Hotel Polissya; la noria es la extracción (transcripción de One Shot, One Kill). Ni un testimonio en Reddit ni en 700 comentarios de los dos videos más vistos de la misión.
- **Quién mata a Shepherd** y **el brazo de Zakhaev:** ya salieron en la parte 1 (p17 y p14).
- **El ataque químico de Londres (MW3), con la niña y la furgoneta:** hilo con 13 comentarios, pero es la muerte de una niña. Excluido por tono.
- **El hijo de Zakhaev capturado vivo:** en el juego se suicida. Excluido por tono, igual que en la parte 2.
- **Esvásticas de Kino y Verrückt cambiadas por cruces:** imagen sensible para YouTube.
- **Carta de jugador «Samurai» de BO1** (23 votos): nadie la encuentra en ninguna lista. No verificable.
- **Soap cantando «Scots Wha Hae» al final de MW3:** un comentario, sin rastro en la wiki.
- **Jumpscare de la niña en la versión de lanzamiento de Mob of the Dead:** rumor sin pruebas.
- **Stamin-Up o «Stamina-Up»:** la parte 1 ya lo nombra («lo que había era Stamin-Up»), y no hay debate documentado.
- **Dobladores (Gary Oldman/Reznov, Ed Harris/Hudson, Ice Cube/Bowman):** no encontré a nadie recordándolos mal. No entra.

---

## C. IDEAS PARA EL GANCHO (~25 s)
1. **«El zombi que se congela»** (de los espectadores + imagen): el Nuketown soleado de Alpha Omega (`HiyklPTA7QE` 0:45). Un A.D.A.M. de pie que solo se mueve cuando la cámara se aparta (corte seco: está más cerca). La voz: «Uno de ustedes me escribió que de niño un zombi lo perseguía por el Nuketown de colores… y que nadie le cree». Corte a la celda de Menéndez (`EMHd0VYb2pg` 3:20): «Otro jura que Mason perdonó a Menéndez. Spoiler: los dos tienen razón… a medias». Remate: «y en el número uno, Black Ops 7 te mintió en la cara».
2. **«Antes y después»** (comparación sin voz): pantalla partida, CoD 4 de 2007 (`jB-n_8zq9Qo` 0:56) contra el Remastered (`4r-YtrYGAIQ` 2:44). La voz calla 3 s y se ve el brazo de Jackson solo en un lado. La voz: «Si tú recuerdas esto… y tu amigo no, no está loco ninguno de los dos». Luego, rápido, el «Korose, Roshia-jin da» japonés (`x7vvJm9jRVU` 0:11) con subtítulo: «y en Japón, Makárov dijo otra cosa».

## D. SONIDOS QUE HAY QUE OÍR CON LA VOZ CALLADA
| N.º | Qué se oye | Video | Segundo |
|---|---|---|---|
| 4 | «Remember… no Russian.» (inglés) | `G7vBol8wud0` | 1:33-1:38 ✔ audio |
| 4 | «殺せ、ロシア人だ» (doblaje japonés, «mátenlos, son rusos») | `x7vvJm9jRVU` | 0:11-0:13 ✔ audio |
| 7 | «Fifty thousand people used to live here… now it's a ghost town» (versión del menú) | `RRYmVb33VU0` | 0:00-0:05 ✔ audio |
| 7 | «Look at this place. Fifty thousand people used to live in this city» (misión) | `XxemwEJDFi0` / `pESIUgBES4Y` | 0:00-0:07 / 0:00-0:10 ✔ audio |
| 13 | «…we will take the fight to their land, to their people, to their blood» (Vendetta) | `2UAvWQgRRXQ` | 0:24-0:33 ✔ audio |
| 13 | «See how things have changed, my friend? Now it is their land…» | `cnpYaxw8Q9A` | 2:41-2:48 ✔ audio |
| 3 | «Everyone hang on!» + la onda (Remastered) | `4r-YtrYGAIQ` | 2:41-2:48 ✔ cuadro (subtítulo visible) |
| 1 | Menéndez de BO7 en español latino (el mensaje de amenaza) | `myE8i4s-e1w` | ≈ (escucharlo entero; 191 s) |
| A1 | La campana de «ronda» cuando los maniquíes cobran vida (Nuk3town) | `fcWwAgqO0kg` | ≈ (antes de 5:10) |

## E. Notas para producción
- **Comentarios en pantalla:** @gxlfredo07 y @rafaeltroconis6615 (con `yt comentario`; recordar el límite de 10 días y que un comentario ya usado no se repite).
- **Clips con el segundo confirmado:** A1 (los dos), A2 (celda y línea de tiempo), n.º 3 (los dos), n.º 4 (los dos audios), n.º 5, 6, 7 (tres audios), 8, 11 (cuadro a 320 px) y 13 (los dos audios). El resto lleva «≈».
- **Violencia:** n.º 1 (disparo a Menéndez), n.º 4 («No Russian») y n.º 11 (Shepherd en 0:53): cortar antes.
- **Todo es de Call of Duty.** La silueta del ángel lloroso de *Doctor Who* va genérica, sin marca.
- **Temporales de esta investigación** (subtítulos, Whisper, comentarios, hojas de cuadros, Reddit): `C:\Users\jaire\AppData\Local\Temp\claude\6e3f4a8ffe67810a\e4b37e63-4f08-4c83-b2f0-0d0e14b642ea\scratchpad\inv\` (carpetas `frames\`, `reddit\`, `subs\`, `wiki\`).
