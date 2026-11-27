# Dossier: «5 atrocidades de Maliketh que el juego te ESCONDIÓ»

Canal Runa Caída. Investigación del 27-nov-2026. Todo lo de abajo sale de las fuentes enlazadas, leídas hoy por API, descarga directa, `yt-dlp` (solo subtítulos, capítulos, metadatos y cuadros sueltos) o Whisper `medium` sobre la pista de audio de clips cortos (para fechar líneas; audio borrado después). Lo que no pude comprobar va marcado **NO VERIFICADO**. Si una afirmación es interpretación de la wiki o teoría de la comunidad (no texto del juego), lo digo y la marco **⚠ ESPECULACIÓN**.

## 0. Fuentes y cómo leerlas

| Clave | Fuente | Para qué sirve |
|---|---|---|
| **[ES-wiki]** | Wiki en español de Fandom, `https://eldenring.fandom.com/es/wiki/<Página>` (API `action=parse&prop=wikitext`). Páginas leídas: Maliketh, la Hoja Negra · Gurranq, el clérigo bestia · Clérigo bestia · Bestia ligada a la sombra · Runa de la Muerte · Noche de los Puñales Negros · Reina del Ojo Velado · Apóstol sacrodermo · Fiel de la Hoja Negra · Raíz mortuoria · Aquellos que viven en la muerte · D, cazador de los muertos · Godwyn el Dorado · Tiche · Alecto · Asesina de los Cuchillos Negros · Hechicero Rogier · Lectora de Dedos Enia · Santuario bestial · Farum Azula · Sello maldito de la Muerte · Recuerdo / Hoja negra de Maliketh | Nombres oficiales es-ES **y alias latinoamericano** (la wiki marca «versión latinoamericana»). **Solo UNA línea de Maliketh en español**: «Oh, Muerte. Conviértete en mi espada una vez más.» (cita de cabecera). No tiene sus otros diálogos en español ni los de Gurranq |
| **[EN-wiki]** | Wiki inglesa, `https://eldenring.fandom.com/wiki/<Page>` (API). ~170 páginas: Maliketh, the Black Blade · Gurranq, Beast Clergyman (+ /dialogue) · Beast Clergyman · D, Hunter of the Dead (+ /dialogue) · Black Blade Kindred · Corpse Wax · Gloam-Eyed Queen · Godskin Apostle · Night of the Black Knives · Rune of Death · Deathroot · Those Who Live in Death · Unused Content · objetos | Descripciones EN y JP (`EN_line`/`JP_line`), diálogos completos en inglés. **Ojo**: «Background/Lore» mezcla texto con interpretación; solo cito como hecho lo que va entre comillas de un objeto o diálogo |
| **[EG]** | Eliteguías, `https://www.eliteguias.com/guias/e/er/elden-ring_<sección>-pNNN.php` (descarga directa; ISO-8859-1) | Descripciones en español **transcritas del juego (es-ES)**. **Tiene erratas** (marcadas [sic]). Páginas: objetos-p553/p136/p137/p236/p394/p409/p429/p550 · armas-p296/p176/p177/p175/p178/p186/p244/p263/p264/p52/p51/p389/p212/p247/p132/p294 · armaduras-p465/p466/p425/p226/p224 · encantamientos-p8/p9/p10/p11/p12/p50/p60/p82/p91/p99 · talismanes-p15/p28/p76/p86 · cenizas-espiritus-p44/p63 · escudos-p67 · personajes-p12/p13 |
| **[TR]** | *Story Trailer* oficial de **BANDAI NAMCO Europe**, `K_03kFqWfqs` (230 s). Subtítulos en inglés **quemados** en la imagen; sin pista de subtítulos | La Noche de los Puñales Negros contada por Ranni con imagen oficial (Godwyn muerto) |
| **[YT]** | Subtítulos y capítulos con `yt-dlp` (sin video). **[WH]** = segundo medido con Whisper `medium` palabra a palabra (±0,3 s en voz sola; ±1 s con música). **[FR]** = cuadro bajado y mirado | Fechar escenas y líneas |
| **[CUT]** | Diálogo **recortado** (está en los archivos, no se oye en el juego): GczQrVgIUis (Stratek, subtítulos «en»), g7yotpJj89s (Sekiro Dubi «Gurranq Cut Dialogue», citado por [EN-wiki] Unused Content: «lines aren't used in Gurranq's ESD files»), Zocukkn7jv0 (SulkierPit7, «unused voice lines» desde 5:59) | Solo como «contenido recortado»: **nunca decir que ocurre en el juego** |

### Nombres oficiales en español (verificados) — inglés → español

| Inglés | Español oficial (es-ES) | Fuente / nota |
|---|---|---|
| Maliketh, the Black Blade | **Maliketh, la Hoja Negra** | [ES-wiki], [EG] (todas sus piezas). **LatAm: «Maliketh, la Espada Negra»** ([ES-wiki] alias «versión latinoamericana»). El video de Ranni dijo «la Espada Negra»; el de Melina, «la Hoja Negra». Pronunciación del canal: «Málikez» |
| Beast Clergyman | **Clérigo bestia** (LatAm «Clérigo Bestia») | [ES-wiki], [EG] |
| Gurranq, Beast Clergyman | **Gurranq, el clérigo bestia** («Gúrank») | [EG] personajes-p13, [ES-wiki] |
| Destined Death | **Muerte Escrita** | [EG] (Hoja negra, Casco, Recuerdo, Llama negra rastreadora, Runa reparadora). **LatAm: NO VERIFICADO**. El guion de Melina dijo «muerte destinada»: no es el término es-ES |
| Rune of Death | **Runa de la Muerte** | [EG], [ES-wiki] |
| Night of the Black Knives | **Noche de los Puñales Negros** | [EG] Aojo de puñal negro, [ES-wiki]. Los videos de Godrick, Ranni y Melina dijeron «de los Cuchillos Negros» (no es el oficial) |
| Black Knife Assassins | **asesinas de los Cuchillos Negros** | [EG] Armadura de Cuchillo Negro |
| Black Knifeprint | **Aojo de puñal negro** | [EG] objetos-p236 |
| Black Knife Tiche / Alecto | **Tiche, la Cuchillo Negro** / **Alecto, líder de los Cuchillos Negros** | [EG] cenizas-espiritus-p44 |
| Deathroot | **Raíz mortuoria** | [EG] objetos-p136 |
| Those Who Live in Death | **quienes viven en la muerte** / «aquellos que viven en la muerte» | [EG] Raíz mortuoria / [ES-wiki] |
| Bestial Sanctum | **Santuario de la bestia** (texto del juego: «el santuario de la bestia del lejano oriente») | [EG] Raíz mortuoria, Cinquedea. [ES-wiki] titula «Santuario bestial»: usar el del juego |
| Greyoll's Dragonbarrow | **Montedrago** | [EG] Cinquedea |
| Crumbling Farum Azula | **Farum Azula, la ciudad en ruinas** («Fárum Azúla») | [ES-wiki] |
| Remembrance of the Black Blade | **Recuerdo de la Hoja Negra** | [EG] objetos-p553 |
| Maliketh's Black Blade / su habilidad | **Hoja negra de Maliketh** / habilidad **Muerte Escrita** | [EG] armas-p296 |
| Black Blade (encantamiento) | **Hoja Negra** | [EG] encantamientos-p99 |
| Black Blade Kindred | **Fiel de la Hoja Negra** | [EG] armas-p176/p177/p263/p264, [ES-wiki] |
| Valiant Gargoyles | **gárgolas denodadas** | [EG] |
| Corpse wax | **adipocira** («el retal de los campeones») | [EG] armas-p186/p244 |
| Corpse Wax Cutter | **Corte de adipocira** | [EG] armas-p176 |
| Gloam-Eyed Queen | **Reina del Ojo Velado** | [EG] Espadón del exterminador de dioses, Ritual de la llama negra |
| Godskin Apostles | **apóstoles sacrodermos** (LatAm «Apóstol piel de dios») | [EG], [ES-wiki] |
| Godslayer's Greatsword | **Espadón del exterminador de dioses** | [EG] armas-p175 |
| Black Flame | **llama negra** | [EG] |
| Godskin Swaddling Cloth | **Empañadura sacroderma** | [EG] talismanes-p76 |
| Shadowbound Beast | **bestia ligada a la sombra** | [EG] Recuerdo, [ES-wiki] |
| Empyrean | **empírea** | [EG] Recuerdo, Ritual de la llama negra |
| Blasphemous Claw | **Garra blasfema** | [EG] objetos-p550 (ya usada en el video de Rykard) |
| Cursemark of Death | **Sello maldito de la Muerte** | [EG] objetos-p394 |
| Mending Rune of the Death-Prince | **Runa reparadora del Príncipe de la Muerte** | [EG] objetos-p409 |
| D, Hunter of the Dead | **D, cazador de los muertos** | [EG] personajes-p12 |
| Finger Reader Enia | **Lectora de Dedos Enia** | [EG] |
| Gurranq's incantations | **Piedra de Gurranq** · **Garra de la bestia Gurranq** · Garra de bestia · Lanzamiento de bestia · Vitalidad de bestia · Constitución de bestia | [EG] encantamientos-p8…p12, p50 |
| Clawmark Seal / Beast Eye | **Sello Marca de Garra** / **Ojo de bestia** | [EG] armas-p51, objetos-p137 |
| Beastclaw Greathammer | **Gran martillo de garras bestiales** (habla de **Serosh, Señor de las Bestias**) | [EG] armas-p52 (ya usado en Godfrey) |
| Cinquedea | **Cinquedea** («clérigos de alta jerarquía de Farum Azula») | [EG] armas-p178 |
| The Shattering | **la Devastación** | [ES-wiki] |
| Godwyn the Golden | **Godwyn, el Dorado** | [EG] Tiche |
| Divine Tower of Caelid | **Torre Sagrada de Caelid** | [EG] armas-p175 |
| Forbidden Lands | **Tierras prohibidas** | [EG] armas-p263 |

---

## 1. Quién es Maliketh ✅ CONFIRMADO

- **Hermanastro y sombra de Márika.** Casco y Armadura de Maliketh ([EG] armaduras-p465/p466): «Maliketh, **fiel hermanastro de la Reina Márika**, empuñaba un filo bañado en Muerte Escrita. **No había ni un solo semidiós que no lo temiese.** / Los campeones sabían lo que estaba en juego y, por eso mismo, eran campeones.»
- **Bestia ligada a la sombra de una empírea.** Recuerdo de la Hoja Negra ([EG] objetos-p553): «Maliketh era una bestia ligada a la sombra de su empírea. El ansia de Márika por disponer de su sombra actuaba como un baluarte contra la Muerte Escrita. **Aun así, ella lo traicionó.**»
  - EN: «Maliketh was the shadowbound beast of his Empyrean. Marika's sole need of her shadow was a vessel to lock away Destined Death. Even then, she betrayed him.» JP: マリカは影従に、運命の死の封印たるを望み 後にそれを裏切ったのだ («Márika quiso que su sombra fuera el sello de la Muerte Escrita, y luego traicionó eso»). **La traducción española se aleja**: el original dice que Márika **solo** lo quería como recipiente para encerrar la Muerte.
- **Guardián de la Runa de la Muerte** (= Muerte Escrita). Enia ([EN-wiki] dialogue): «The Rune of Death goes by two names; the other is Destined Death…». Runa reparadora ([EG] objetos-p409): «**La Orden Dorada se creó tras confinar a la Muerte Escrita**, por lo que esta nueva Orden equivaldrá a la restauración de la Muerte.»
- **La hoja en la carne.** Hoja negra de Maliketh ([EG] armas-p296): «Hoja negra de Maliketh que, antaño, abrazaba el poder de la Runa de la Muerte. Apenas es una sombra de su antigua gloria. / Después de que robase un fragmento de Muerte durante aquella fatídica noche, Maliketh vinculó la espada a su propia carne para que nadie pudiese volver a hurtar a la muerte.» **ERRATA de traducción**: en EN «After a fragment of Death **was stolen**…» (pasiva). En español parece que el ladrón fue Maliketh. **No leerlo literal en la voz**: «después de que le robaran un fragmento…».
- **Gurranq = Maliketh.** El clérigo bestia del Santuario de la bestia (Montedrago, norte de Caelid) es Maliketh disfrazado: en Farum Azula se arranca la túnica en la cinemática y se presenta: «Cower. Before Maliketh, the Black Blade.» ([EN-wiki] Gurranq). En el juego no se explica por qué se esconde.
- **Su nombre como bestia.** Piedra de Gurranq y Garra de la bestia Gurranq ([EG] encantamientos-p11/p12): «Antaño, Gurranq era una bestia tan terroríficamente feroz que su nombre significaba **"Muerte de los Semidioses"**.» ([ES-wiki] lo pone como epíteto.)
- **Se pelea en** Farum Azula, la ciudad en ruinas, después de que se queme el Árbol Áureo. Tras vencerlo, la Runa de la Muerte queda libre («The Rune of Death is unbound», Pqy93_M67Jg ≈ 444 s) y Leyndell queda en ceniza.

---

## 2. CANDIDATAS (13), cada una con veredicto

### C1. Los guardias remendados con grasa de cadáver ✅ CONFIRMADO (material nuevo)
- **Hoja negra de gárgola** ([EG] armas-p176): «Espadón de bronce que portaban las gárgolas denodadas, **arreglada con adipocira ennegrecida**. / Inflige daño sagrado. / **Esa es la marca de quienes sirven a Maliketh, la Hoja Negra.** / Habilidad única: Corte de adipocira / **Habilidad perdida de antiguos héroes.**» Igual en Alabarda negra (p177), Hojas negras (p263, errata «gárgols») y Hacha negra de gárgola (p264, errata «Infige»).
- **Qué es la adipocira, según el propio juego** (Espadón de gárgola [EG] armas-p186 y Gran hacha de gárgola p244): «Tal y como le pasaba a su portador, las piezas que faltan fueron arregladas con adipocira, **el retal de los campeones**.» (errata p244 «psaba»). EN: «mended with corpse wax; a patchwork of champions». En la vida real, *adipocere* = «cera de cadáver», grasa de cuerpos que se transforma bajo tierra ([EN-wiki] Corpse Wax lo enlaza a Wikipedia).
- **Dónde salen:** el **Fiel de la Hoja Negra** guarda la entrada del **Santuario de la bestia** (Montedrago) y aparece en las **Tierras prohibidas** ([EG] p263/p264; [EN-wiki] Bestial Sanctum: jefe «Black Blade Kindred»). Fuera del santuario hay **milicianos de la Hoja Negra** que lanzan encantamientos de bestia ([EN-wiki] Vulgar Militia).
- **Remate textual:** el casco de Maliketh dice «Los campeones sabían lo que estaba en juego y, por eso mismo, eran campeones».
- **Atrocidad (lo que permitió):** sus guardianes son estatuas parcheadas con lo que queda de campeones muertos, **ennegrecidas** para él. ⚠ Que la adipocira negra sea de campeones concretos al servicio de Maliketh es **interpretación**: el texto dice «retal de los campeones» de las gárgolas en general y «ennegrecida» en las suyas.
- **¿Lo sabía el jugador normal?** **No.** El jefe se mata en 2 minutos; lo de la adipocira solo está en el texto del arma que suelta (y en el de otras gárgolas). Casi nadie sabe qué es la adipocira.

### C2. «Muerte de los Semidioses»: el carcelero al que todos temían ✅ CONFIRMADO
- Piedra de Gurranq / Garra de la bestia Gurranq ([EG]): su nombre «significaba "Muerte de los Semidioses"». Las das al entregar la **6.ª** y **8.ª** Raíz mortuoria.
- Casco/Armadura ([EG]): «No había ni un solo semidiós que no lo temiese.»
- Runa reparadora ([EG]): la Orden Dorada **nació** de encerrar la Muerte → la «edad dorada» entera se construyó sobre su jaula.
- Hoja negra de Maliketh ([EG]): se cosió la espada **a su propia carne**.
- **Atrocidad:** fue el verdugo de la familia divina en potencia y el carcelero de la muerte del mundo; la Orden de Márika es literalmente la consecuencia de su encierro.
- **¿Lo sabía el jugador normal?** **A medias.** Que guarda la Runa de la Muerte lo dice la historia principal (Enia/Melina). «Muerte de los Semidioses» y «no había semidiós que no lo temiese» están **solo** en textos de encantamientos y armaduras que casi nadie lee.
- **YA CONTADO:** que selló la Runa en su espada (Melina p2; Ranni p2). **Ángulo nuevo:** el nombre de bestia y el miedo de los semidioses (no se ha dicho nunca en el canal).

### C3. La Reina del Ojo Velado y los apóstoles recién nacidos ✅ CONFIRMADO (con matiz)
- Espadón del exterminador de dioses ([EG] armas-p175): «Espada sagrada de la Reina del Ojo Velado, que controlaba a los apóstoles sacrodermos **antes de sucumbir ante Maliketh**.» (Se encuentra en la **Torre Sagrada de Caelid**, Montedrago, tras el Apóstol sacrodermo.)
- Ritual de la llama negra ([EG] encantamientos-p82): «La Reina del Ojo Velado dirigió a los apóstoles. **Se dice que era una empírea elegida por los Dedos.**»
- Túnica de apóstol sacrodermo ([EG] armaduras-p226): «Los apóstoles, que se dice que sirvieron a la Muerte Escrita, empuñan la llama negra exterminadora de dioses. Pero, **tras su derrota ante Maliketh, la Hoja Negra, la fuente de su poder fue sellada**.»
- Llama negra rastreadora ([EG] encantamientos-p60): «Hace un tiempo la llama negra era capaz de matar dioses. Sin embargo, **cuando Maliketh selló la Muerte Escrita, el verdadero poder de la llama negra se perdió**.»
- Empañadura sacroderma ([EG] talismanes-p76): «**La Reina del Ojo Velado acuna a los apóstoles recién nacidos envueltos en este paño.** Pronto crecerán y se convertirán en la fatalidad de los dioses.»
- **Atrocidad:** venció a una rival de Márika, otra candidata a diosa elegida por los mismos Dedos, y dejó a su pueblo de apóstoles sin el poder con el que nacían. **Matiz obligatorio:** los apóstoles **desollaban dioses** (su nombre: «sacrodermos», piel de dioses); no eran víctimas puras. El texto dice «sucumbir» y «derrota», **no** que la matara.
- **¿Lo sabía el jugador normal?** **No.** Todo está en textos de objetos opcionales (Torre Sagrada de Caelid, Cueva invocadora).
- **YA CONTADO:** Melina p4 (línea 205): «la Reina del Ojo Velado, una Empírea elegida por los Dedos que manejaba las llamas negras de la muerte de los dioses, hasta que Maliketh la derrotó» (como teoría sobre Melina). **Ángulo nuevo:** la guerra contada **desde Maliketh**: los recién nacidos en su paño, el poder sellado, y que era una rival elegida por los Dedos. Decir en una frase «en el video de Melina la nombramos de pasada».

### C4. La cacería de «quienes viven en la muerte» ✅ CONFIRMADO (ángulo nuevo)
- Raíz mortuoria ([EG] objetos-p136): «Una fuente que despierta a quienes viven en la muerte. / El clérigo bestia, que se encuentra en el santuario de la bestia del lejano oriente, recoge y devora estas raíces. / **En la noche del complot, la Runa de la Muerte robada permitió la primera muerte de un semidiós. Posteriormente, la Runa de la Muerte se extendió por las Tierras Intermedias a través de las raíces subterráneas del gran árbol, emergiendo en forma de raíz mortuoria.**» (errata «subteráneas»).
- D ([EN-wiki] D/dialogue): «I'm known as D. I hunt down Those Who Live in Death, and weed their Deathroot…» y, al pasarte el encargo: «…**the beast himself wishes for someone to take my place**.» → D era el cazador de Gurranq; **tú eres su sustituto**.
- Ojo de bestia ([EG] objetos-p137): «Se dice que tiembla cuando se encuentra cerca de la raíz mortuoria… "No estoy saciado... Aliméntame... con más Muerte..."».
- Gurranq con la **4.ª raíz** ([EN-wiki] dialogue): «Strange... There's something else... But the Death...yet quenches...» (JP おかしい、混ざっている = «qué raro, está mezclado»). Con la **5.ª**: «Death... My sin... **Should not be touched...by the hand of man**...»
- **Atrocidad:** la muerte que **él dejó escapar** se coló por las raíces y despertó a los muertos; su «solución» fue mandar cazadores (D, luego tú) a arrancarla y comérsela él. ⚠ Que la 4.ª raíz «mezclada» signifique algo concreto: **ESPECULACIÓN** (el juego no lo explica).
- **¿Lo sabía el jugador normal?** **No** lo del encargo de D (diálogo opcional de una misión secundaria) ni la frase «no debe tocarla la mano del hombre». La relación raíz → noche del complot está en la descripción de la raíz (la mayoría la entrega sin leer).
- **YA CONTADO:** Sinluz p3c (líneas 156-161) contó TODO el arco de dar de comer (ataque tras la 4.ª, «basta», 9.ª raíz, «pecar», «tú le rompiste la dieta»). **Ángulo nuevo:** **por qué** comía raíces (son su propio fallo) y **quién** le hacía el trabajo sucio (D). No repetir el ataque ni el «basta» salvo en una frase de enlace.

### C5. La noche que dejó robar la Muerte ✅ CONFIRMADO (base del n.º 1)
- Rogier ([EN-wiki] dialogue): «Someone stole a fragment of the Rune of Death from Maliketh, the Black Blade. And on a bitter night, murdered Godwyn the Golden.»
- Aojo de puñal negro ([EG] objetos-p236): «Durante la Noche de los Puñales Negros, alguien robó un fragmento de la Runa de la Muerte a Maliketh, la Hoja Negra, e imbuyó las dagas de los asesinos con su poder. / Esta marca es una prueba del ritual y **oculta la verdad de la conspiración**.» (errata «PUñales»).
- Tiche ([EG] cenizas-espiritus-p44): «…durante la noche del complot, imbuyó su puñal negro en la Runa de la Muerte para dar muerte a Godwyn, el Dorado…»
- Sello maldito de la Muerte ([EG] objetos-p394): «…dos semidioses murieron al mismo tiempo… Ranni fue la primera semidiosa en ver cómo su carne moría, mientras que, en el caso del Príncipe de la Muerte, tan solo su alma falleció.»
- [TR] K_03kFqWfqs: Ranni narra «On a night of wint'ry fog, the Rune of Death was stolen, and the demigods began to fall, starting with Godwyn the Golden… Queen Marika was driven to the brink. The Shattering ensued… The Elden Ring was broken, but by whom? And why?»
- **Atrocidad (lo que permitió):** el guardián de la muerte dejó que se la robaran → primera muerte de un semidiós → la Devastación.
- **¿Lo sabía el jugador normal?** El robo, **sí** (Rogier, Ranni). Lo de abajo (C6, C7) no.
- **YA CONTADO:** Ranni p2 (robo, Godwyn, espada sellada, Gurranq), Rykard (Rogier en la Mesa Redonda), Godrick. **No hacer de esto el puesto; es la puerta del n.º 1.**

### C6. «Aun así, ella lo traicionó» y las asesinas de Márika ✅ CONFIRMADO + ⚠ ESPECULACIÓN
- Recuerdo de la Hoja Negra ([EG]): «Aun así, ella lo traicionó.» (EN «Even then, she betrayed him.»)
- Armadura de Cuchillo Negro ([EG] armaduras-p425): «Las asesinas que llevaron a cabo las hazañas de la Noche de los Puñales Negros eran todas mujeres y, según los rumores, **eran númenes estrechamente vinculadas a la propia Márika**.»
- Aojo de puñal negro: «oculta la verdad de la conspiración».
- **⚠ ESPECULACIÓN:** que Márika estuviera detrás del robo de la Muerte a su propia sombra. El juego **no lo afirma**: solo junta «lo traicionó» + «asesinas vinculadas a Márika» + «oculta la verdad». **Decirlo como pregunta, nunca como hecho.**
- **¿Lo sabía el jugador normal?** **No.** Tres textos de objetos en tres sitios distintos.

### C7. Lo que dice Gurranq si lo matas ✅ CONFIRMADO (escondido)
- Solo si **matas a Gurranq en el Santuario** ([EN-wiki] dialogue): «**Marika...why...wouldst thou...gull me? Why...shatter...**» (JP なぜ、壊した = «¿por qué lo rompiste?»). «Gull» = engañar. → **El propio Maliketh, moribundo, acusa a Márika de engañarlo y de romper (el Círculo).**
- [WH] v-Csk29Jx50 127,3–142,5 s.
- **¿Lo sabía el jugador normal?** **No.** Casi nadie ataca a Gurranq (te da la misión); la línea solo sale si lo matas.

### C8. El diálogo RECORTADO: «¿Fui yo el necio, o tú me engañaste?» ⚠ CONTENIDO RECORTADO
- [CUT] (no está en el juego final): «No one will take the Rune of Death again. **Death to the thieves of Death. Death to the scavengers of Death.** A god falleth not so easily. This woman/man...a slayer of gods. Most impressive... **Armed with death, thou mayest choose the throne of thy desire.** … O Death! My fate! **O Marika... What...happened? Was I...myself the fool? Or was I tricked...by thee? O Marika... Why wouldst thou...relinquish... Why...**»
- Fuentes: GczQrVgIUis (Stratek), g7yotpJj89s (Sekiro Dubi; [EN-wiki] Unused Content lo cita: «lines aren't used in Gurranq's ESD files»), Zocukkn7jv0 (SulkierPit7 desde 5:59).
- **Regla:** decirlo como «FromSoftware grabó estas líneas y las **quitó** del juego». Marca en pantalla «DIÁLOGO RECORTADO».
- **¿Lo sabía el jugador normal?** **No** (solo en los archivos).

### C9. Las dos muertes de Maliketh ✅ CONFIRMADO (cierre)
- Muerte normal ([EN-wiki] dialogue): «Witless Tarnished... Why covet Destined Death? To kill what?»
- Si completaste la misión de Gurranq: «Forgive me, Marika... The Golden Order... cannot be restored.» (JP 黄金律は、もう、戻らぬ). Y la entrada cambia: «Tarnished, why wouldst thou... Why... Tis no matter. I hereby vow, that Destined Death shall not be stolen again.»
- **¿Lo sabía el jugador normal?** **No**: cada jugador oye **una** de las dos versiones.

### C10. Liberar la Muerte: la capital en ceniza ⚠ CONTEXTO (no es suya, es tuya)
- Tras vencerlo, la Runa de la Muerte queda suelta y Leyndell pasa a ser la capital de ceniza (Pqy93_M67Jg 414–504 s). Es consecuencia de **tu** victoria → cierre, no puesto.

### C11. La Garra blasfema ❌ YA CONTADO
- [EG] objetos-p550 «…la oscura bestia de la Muerte Escrita». Contada entera en el video de Rykard (162-171). Como mucho, una frase.

### C12. Otras afirmaciones de la comunidad ❌ SIN TEXTO
- Que Maliketh **destruyó Nokron/Nokstella**: **ningún texto** lo dice. El Fingerslayer Blade habla de la «alta traición» de la Ciudad Eterna sin nombrar a Maliketh.
- Que Maliketh y **Messmer** fueran «hermanos sombra»: sin texto.
- Maliketh en **Shadow of the Erdtree**: **ningún texto del DLC lo nombra** (las páginas del DLC salían en la búsqueda solo por las plantillas de navegación). Los **Caballeros de la Muerte** del DLC eran la guardia de **Godwyn**, no de Maliketh.
- Dragones / Placidusax ligados a Maliketh: sin texto.
- Que Maliketh **empalara** o hiriera a Márika: interpretación de la wiki, sin texto.

### C13. Farum Azula y las bestias ⚠ APOYO DE ESCENARIO
- Cinquedea ([EG] armas-p178): «Espada corta cedida a los clérigos de alta jerarquía de Farum Azula… El diseño rinde homenaje a los cinco dedos de una bestia, símbolo de la inteligencia que se otorgó antaño a los suyos.» (Está bajo el Santuario.)
- [EN-wiki] Bestial Sanctum: «The architecture matches that seen in Crumbling Farum Azula, and the corpses of many Beastmen can be found surrounding the sanctum.» (nota de la wiki, observación visual).
- Garra de bestia ([EG]): «la furia de Gurranq, una vez recuperada su naturaleza de bestia, tanto como su desasosiego»; Sello Marca de Garra: «la ira de Gurranq».
- Para planos, no para puesto.

### LO YA CONTADO EN EL CANAL (grep de `Maliketh|Gurranq|Raíz mortuoria|Reina del Ojo|Cuchillos Negros|Puñales Negros` en `videos/er_*/guion.py`)
- `er_ranni_atrocidades/guion.py` 145-158 (p2): robo del fragmento, Godwyn primer semidiós muerto, espada sellada en la carne, Gurranq comiendo raíces. Lo llama «**Maliketh, la Espada Negra**» (LatAm).
- `er_sinluz_atrocidades/guion.py` 156-161 (p3c): todo el arco de Gurranq (9 raíces, ataque tras la 4.ª, «basta», 9.ª «pecar»), cita de **KingInsect25** y el chiste «Márika le rompió el corazón. Tú le rompiste la dieta».
- `er_melina_atrocidades/guion.py` 168-174 (p2): Runa de la Muerte / «muerte destinada» (Enia), la sella en su espada, matar a su guardián; 205-206 (p4): **Reina del Ojo Velado** como teoría de Melina.
- `er_rykard_atrocidades/guion.py` 162-171: Garra blasfema, Bernahl, Rogier en la Mesa Redonda.
- `er_godrick_atrocidades` 178 · `er_godfrey_atrocidades` 54, 157 (Gran martillo de garras bestiales / Serosh, que da Gurranq): Noche de los Cuchillos Negros, Godwyn.
- `er_mohg` 197, `er_messmer` 189, `er_sinluz` 229: «Maliketh está apuntado».
- **Comentario ya respondido que vuelve:** @DarkShooter942 (Gurranq «nos suplicaba que guardáramos el arma») = el «Put it away… enough» que Sinluz ya contó → responderle con el ángulo nuevo (C4), no repetir la escena.
- **Ángulos nuevos obligados:** «Hoja Negra» y «Noche de los Puñales Negros» (nombres es-ES; decir una vez «en Latinoamérica, la Espada Negra»), «Muerte Escrita» (no «muerte destinada»).

---

## 3. Citas listas para usar (estado de verificación)

| Cita | Idioma | Estado |
|---|---|---|
| «Oh, Muerte. Conviértete en mi espada una vez más.» | ES | ✅ [ES-wiki] (única línea de Maliketh en español verificada) |
| Recuerdo: «Maliketh era una bestia ligada a la sombra de su empírea. El ansia de Márika por disponer de su sombra actuaba como un baluarte contra la Muerte Escrita. Aun así, ella lo traicionó.» | ES | ✅ [EG] (EN/JP: «solo lo quería como recipiente»; ver §1) |
| Casco/Armadura: «Maliketh, fiel hermanastro de la Reina Márika, empuñaba un filo bañado en Muerte Escrita. No había ni un solo semidiós que no lo temiese. Los campeones sabían lo que estaba en juego y, por eso mismo, eran campeones.» | ES | ✅ [EG] |
| Piedra de Gurranq: «Antaño, Gurranq era una bestia tan terroríficamente feroz que su nombre significaba "Muerte de los Semidioses".» | ES | ✅ [EG] |
| Hoja negra de Maliketh: «…Maliketh vinculó la espada a su propia carne para que nadie pudiese volver a hurtar a la muerte.» | ES | ✅ [EG] (**errata** «después de que robase»: parafrasear la 1.ª mitad) |
| Raíz mortuoria: «En la noche del complot, la Runa de la Muerte robada permitió la primera muerte de un semidiós. Posteriormente, la Runa de la Muerte se extendió por las Tierras Intermedias a través de las raíces subterráneas del gran árbol, emergiendo en forma de raíz mortuoria.» | ES | ✅ [EG] |
| Ojo de bestia: «"No estoy saciado... Aliméntame... con más Muerte..."» | ES | ✅ [EG] |
| Hoja negra de gárgola: «…arreglada con adipocira ennegrecida… Esa es la marca de quienes sirven a Maliketh, la Hoja Negra.» + Espadón de gárgola: «…adipocira, el retal de los campeones.» | ES | ✅ [EG] |
| Espadón del exterminador de dioses: «Espada sagrada de la Reina del Ojo Velado, que controlaba a los apóstoles sacrodermos antes de sucumbir ante Maliketh.» | ES | ✅ [EG] |
| Ritual de la llama negra: «La Reina del Ojo Velado dirigió a los apóstoles. Se dice que era una empírea elegida por los Dedos.» | ES | ✅ [EG] (ya dicho en Melina) |
| Empañadura sacroderma: «La Reina del Ojo Velado acuna a los apóstoles recién nacidos envueltos en este paño. Pronto crecerán y se convertirán en la fatalidad de los dioses.» | ES | ✅ [EG] |
| Llama negra rastreadora: «…cuando Maliketh selló la Muerte Escrita, el verdadero poder de la llama negra se perdió.» | ES | ✅ [EG] |
| Túnica de apóstol: «…tras su derrota ante Maliketh, la Hoja Negra, la fuente de su poder fue sellada.» | ES | ✅ [EG] |
| Aojo de puñal negro: «…alguien robó un fragmento de la Runa de la Muerte a Maliketh, la Hoja Negra… Esta marca es una prueba del ritual y oculta la verdad de la conspiración.» | ES | ✅ [EG] |
| Armadura de Cuchillo Negro: «…eran todas mujeres y, según los rumores, eran númenes estrechamente vinculadas a la propia Márika.» | ES | ✅ [EG] |
| Runa reparadora: «La Orden Dorada se creó tras confinar a la Muerte Escrita…» | ES | ✅ [EG] |
| Resto de líneas de Maliketh (entrada, muertes) y TODAS las de Gurranq | EN | ✅ [EN-wiki] + [WH]. **En español: NO VERIFICADO** → la voz las **parafrasea** y se OYEN en inglés (§5) |
| D: «the beast himself wishes for someone to take my place» | EN | ✅ [EN-wiki] D/dialogue. Español NO VERIFICADO → parafrasear |
| Diálogo recortado («Was I myself the fool? Or was I tricked by thee?») | EN | ⚠ [CUT] (3 fuentes coinciden). Siempre «recortado» |

---

## 4. Lugares para MAPAS (x,y en `mapas/mundo_rejilla.jpg`, rejilla 0-1)

Mapa: `mapas/mundo.jpg` (9644×9118) / `mundo_rejilla.jpg` (1920×1815), copiados del video de Rykard (mapa de superficie, **sin subterráneos**). Medido hoy a ojo sobre recortes de `mundo.jpg` e identificado **por forma** y por el texto de la wiki; cruzado con el dossier de Rykard (coinciden ±0,01). `sombras_rejilla.jpg` **no hace falta** (ningún texto del DLC nombra a Maliketh).

| Lugar | x, y (rejilla) | Ligado a | Fiabilidad |
|---|---|---|---|
| **Santuario de la bestia** (planta cuadrada con un círculo dentro, en la punta norte de la península de Montedrago) | **0,617 , 0,600** · puente largo hacia el sur 0,638 , 0,61→0,66 | C1, C4, n.º 4-5 | ✅ por forma + [EN-wiki] «on the northernmost tip of Caelid» |
| Montedrago (región) | ≈ 0,62–0,66 , 0,60–0,66 | C1 | ⚠ región |
| **Torre Sagrada de Caelid** (torre redonda en un islote al oeste de Montedrago, unida por un camino) | **0,518 , 0,637** | C3 | ⚠ por forma |
| **Farum Azula, la ciudad en ruinas** (remolino al este del mapa) | **0,886 , 0,493** (Rykard: 0,87 , 0,48) · plataforma circular grande al este del remolino 0,902 , 0,487 (¿arena de Maliketh? **NO VERIFICADO**) | n.º 1, cierre | ⚠ por forma (no es un lugar «real» del mapa: el juego lo dibuja como tormenta) |
| **Leyndell, capital del Reino** (ciudad amurallada con lago) | **0,45 , 0,39** (Rykard: 0,44 , 0,37) | C5, n.º 1, cierre | ⚠ por forma |
| **Árbol Áureo** (dibujo dorado) | **0,49 , 0,42** (Rykard 0,48 , 0,41) | C2, cierre | ✅ es el dibujo |
| **Academia de Raya Lucaria** (isla amurallada, Liurnia) | **0,196 , 0,540** (= Rykard ✅) | — (solo si se cita a Rennala/Ranni) | ✅ por forma |
| **Catacumbas de los Cuchillos Negros** (Aojo de puñal negro) | **≈ 0,275 , 0,45** | C5, C6 | ⚠ **NO MEDIDO con precisión**: [EN-wiki] «in the north-eastern area of Liurnia», al este de la Iglesia de los Votos; ese punto es la meseta NE de Liurnia |
| Tierras prohibidas (Fiel de la Hoja Negra n.º 2) | **NO MEDIDO** (entre Leyndell y las Cumbres de los gigantes, al NE de la capital) | C1 | ❌ |
| Aldea de Aguainvocante (D) / Necrolimbo (Este) | **NO MEDIDO** | C4 | ❌ |
| Nokron / Nokstella / Raíz profunda (cadáver de Godwyn) | **subterráneos: no están en este mapa** | C5 | ❌ usar las capturas de la wiki (`nokron_wiki`, `nokstella_wiki`) |
| Mesa Redonda | fuera del mapa | C5 | — (captura `mesa_redonda.jpg`) |

---

## 5. ESCENAS IMPORTANTES y clips (solo ids y segundos; nada de video descargado)

Canales evitados: Fextralife, **pgp** (logo en la imagen; rZ5Qssnpj8U), **Shirrako**, Lance McDonald, IGN, VaatiVidya, Zullie, PowerPyx y el resto de la lista del dossier de Messmer.

**Fuente principal: SourceSpy91, `Pqy93_M67Jg`** («Part 48 – Maliketh, The Black Blade», 4K, sin comentarios, 613 s). Comprobado con cuadros: **sin marca de agua**; HUD del juego en el combate.

| Escena | Video (id · canal) | Momento |
|---|---|---|
| Llegada / pelea fase 1 | **Pqy93_M67Jg** · SourceSpy91 | ≈ 37 s en adelante (con HUD) |
| **Cinemática: Gurranq se arranca la túnica, sale la hoja de su cuerpo y se presenta** | Pqy93_M67Jg | **≈ 170–242 s** [FR]: 172 Gurranq arrodillado · 186 su mano · **204 la hoja negra sale del cuerpo** · 212/224/236 Maliketh revelado (limpios) |
| Fase 2 («O, Death. Become my blade, once more.») | Pqy93_M67Jg | desde ≈ 244 s |
| LEGEND FELLED | Pqy93_M67Jg | ≈ 390 s |
| **La hoja de la Runa de la Muerte flotando / el jugador ante ella** | Pqy93_M67Jg | **414–432 s** [FR] |
| «The Rune of Death is unbound» | Pqy93_M67Jg | ≈ 444 s |
| Narración con imágenes (Árbol ardiendo, Muerte desatada) | Pqy93_M67Jg | 450–480 s [FR] **sin subtítulos** en 462 y 476 (comprobado) |
| Leyndell, capital de ceniza | Pqy93_M67Jg | ≈ 504 s |
| Pelea sin HUD (alternativas) | C7h854v6Ax8 · JustGamesBruh ([CAP] Intro 0 · Phase 1 15 · Cutscene 86 · Phase 2 160 · «Unleash the Destined Death cutscene» 245) · ijn3476GmKU ONGBAL · gYU5RwWaCDA 0bsidian | **Marca de agua NO comprobada** |
| Partida completa 720p con capítulos | HJ6EIysyst8 · SourceSpy91 | [CAP] Nokron 35:48:53 · Deeproot 37:22:12 · Dragonbarrow 44:06:02 · **Divine Tower of Caelid 46:48:36 · Godskin Apostle 47:03:01** · **D quest 52:32:21** · Forbidden Lands 63:17:03 · Farum Azula 77:28:44 · Godskin Duo 78:20:51 · Placidusax 79:52:24 · **Maliketh 80:01:34** · Capital de ceniza 80:36:40 |
| Partes 4K de SourceSpy91 | Farum Azula **9nmqal7jH9A** (6888 s) · Montedrago **nY_GWYSBz_Y** ([CAP] «Greyoll's Dragonbarrow» 0:45:26, cerca del Santuario) · Raíz profunda **KNOGSI89eQo** (0:26:50) · Torre Sagrada de Caelid **vXwBJr-fLM8** · Nokron **OC9bSeqZgYw** (0:03:54) | Segundo exacto del **Santuario / Gurranq / Fiel de la Hoja Negra: NO VERIFICADO** |
| Gurranq, las 9 raíces | c5mltemiLdA · ryurain (con capítulos) · FPay3pRpfY4 · Sen (incluye diálogo recortado) | NO VERIFICADO marca de agua |
| **Noche de los Puñales Negros (oficial)** | **K_03kFqWfqs** · BANDAI NAMCO Europe · 230 s | [FR] 20 manos de Ranni (subtítulo) · **31 bosque con niebla (limpio)** · 38 «The rune of death was stolen» (subtítulo) · 44–56 **Godwyn muerto** (49 limpio) · 62–68 ojo / «Queen Marika was driven to the brink» · 74–80 «The Shattering ensued» · 86 «The Elden Ring was broken, but by whom? And why?» (todos con subtítulo quemado salvo los marcados limpios) |
| Cinemática de apertura (Godwyn, Devastación) | _uydEN9Fu7M · RajmanGaming | NO VERIFICADO |
| Las dos variantes de diálogo de Maliketh | Pxrcjovrevc · Games from Mars (con capítulos) | referencia |

### SONIDOS para que la voz los mande escuchar (cortar como sfx)

| # | Línea (EN) | Video | Inicio–fin | Comprobado |
|---|---|---|---|---|
| S1 | **«O, Death. Become my blade, once more.»** | **xaXLX1UOl8A** (Sin, voz sola, 89 s) | **18,6 – 23,2 s** | [WH] palabra a palabra |
| S2 | «Thou, who approacheth Destined Death. I will not have it stolen from me again.» | xaXLX1UOl8A | **0,0 – 11,6 s** | [WH] |
| S3 | **«Witless Tarnished... Why covet Destined Death? To kill what?»** | xaXLX1UOl8A | **33,3 – 41,2 s** | [WH] |
| S4 | «Tarnished, why wouldst thou... Why... Tis no matter. I hereby vow, that Destined Death shall not be stolen again.» (variante con la misión hecha) | xaXLX1UOl8A | 42,8 – 62,8 s | [WH] |
| S5 | «Cower. Before Maliketh, the Black Blade.» | xaXLX1UOl8A | 69,8 – 75,0 s | [WH] (Whisper oye «Marika's»; el texto es el de [EN-wiki]) |
| S6 | **«Forgive me, Marika... The Golden Order... cannot be restored.»** | xaXLX1UOl8A | **75,9 – 87,2 s** | [WH] |
| S7 | Gurranq 4.ª raíz: «Strange... There's something else... But the Death... yet quenches...» | **v-Csk29Jx50** (Stratek, compilación de Gurranq, 389 s) | 72,8 – 85,2 s | [WH] |
| S8 | Gurranq: «Put it away... I won't forget... again... mine appetite... My sin... So please... enough...» | v-Csk29Jx50 | 101,4 – 125,2 s | [WH] (ya usado en Sinluz) |
| S9 | **Gurranq al morir: «Marika... why... wouldst thou... gull me? Why... shatter...»** | v-Csk29Jx50 | **127,3 – 142,5 s** | [WH] |
| S10 | Gurranq: «It is all consumed... still I am not sated» | v-Csk29Jx50 | 204,8 – 217,0 s | [WH] |
| S11 | Gurranq 9.ª raíz: «Marika... is this what it is to sin…» | v-Csk29Jx50 | 223,0 – 242,7 s | [WH] (ya usado en Sinluz) |
| S12 | [CUT] «Death to the thieves of Death. Death to the scavengers of Death.» | **GczQrVgIUis** (Stratek, 65 s) | 5,4 – 11,2 s | [WH] |
| S13 | [CUT] «Armed with death, thou mayest choose the throne of thy desire.» | GczQrVgIUis | 26,0 – 33,6 s | [WH] |
| S14 | **[CUT] «O Marika... What... happened? Was I... myself the fool? Or was I tricked... by thee?»** | GczQrVgIUis | **41,5 – 55,3 s** | [WH] |
| S15 | [CUT] «O Marika... Why wouldst thou... relinquish... Why...» | GczQrVgIUis | 55,3 – 63,5 s | [WH] |
| S16 | **Tráiler oficial, Ranni: «On a night of wint'ry fog, the Rune of Death was stolen… and the demigods began to fall, starting with Godwyn the Golden.»** | **K_03kFqWfqs** | **26,1 – 52,7 s** («On a night of wint'ry fog» 26,1–28,3 · «The rune of death was stolen» 35,5–39,5 · «And the demigods began to fall» 45,6–47,4 · «Starting with Godwyn the Golden» 50,4–52,7) | [WH] ±1 s (con música) |
| S17 | Tráiler: «The Elden Ring was broken. But by whom? And why?» | K_03kFqWfqs | 84,4 – 90,7 s | [WH] ±1 s |

«Voz sola» = las pistas de Sin y Stratek no tienen imagen útil (solo audio). Whisper oye «Malekith/Merika/America» donde dice Maliketh/Marika. **Comprobar en la mezcla FINAL con Whisper** (regla de oro 10).

### Capturas en `pantallas/` (1920×1080; anotadas en `pantallas/_fuentes.txt`)

| Archivo | Sale de | Notas |
|---|---|---|
| `gurranq_arrodillado_farum.jpg` | Pqy93_M67Jg 172 s | Limpia (cinemática) |
| `gurranq_mano_cinematica.jpg` | Pqy93_M67Jg 186 s | Limpia |
| `hoja_negra_sale_del_cuerpo.jpg` | Pqy93_M67Jg 204 s | Limpia (la hoja roja sale de su carne) |
| `maliketh_revelado_hoja.jpg` | Pqy93_M67Jg 212 s | Limpia |
| `maliketh_revelado_perfil.jpg` | Pqy93_M67Jg 224 s | Limpia (cara de perfil: útil para tarjeta) |
| `maliketh_revelado_cuerpo.jpg` | Pqy93_M67Jg 236 s | Limpia |
| `runa_muerte_hoja_flotando.jpg` | Pqy93_M67Jg 420 s | Limpia |
| `runa_muerte_altar.jpg` | Pqy93_M67Jg 432 s | Limpia (el jugador ante la hoja) |
| `narracion_muerte_desatada.jpg` | Pqy93_M67Jg 462 s | Sin subtítulo (comprobado la franja baja) |
| `arbol_aureo_ardiendo_runa_muerte.jpg` | Pqy93_M67Jg 476 s | Sin subtítulo (comprobado) |
| `trailer_noche_niebla.jpg` | K_03kFqWfqs 31 s | Tráiler oficial, limpio, franjas negras |
| `trailer_godwyn_cadaver.jpg` | K_03kFqWfqs 49 s | Tráiler oficial, limpio (Godwyn muerto) |
| `farum_wiki`, `nokron_wiki`, `nokstella_wiki`, `catacumbas_cuchillo`, `leyndell_wiki`, `caelid_wiki`, `mesa_redonda` | wiki EN (las puso otro proceso) | URLs en `_fuentes.txt` |

**Faltan capturas** (NO VERIFICADO el segundo): Santuario de la bestia por fuera y Gurranq comiendo (nY_GWYSBz_Y ≈ 0:45:26 en adelante), Fiel de la Hoja Negra, Torre Sagrada de Caelid / Apóstol sacrodermo (vXwBJr-fLM8), D (HJ6EIysyst8 52:32:21), cadáver de Godwyn en la Raíz profunda (KNOGSI89eQo).
**Escenas que no son cinemática** (icono de objeto): Recuerdo de la Hoja Negra, Hoja negra de Maliketh, Casco de Maliketh, Piedra de Gurranq, Raíz mortuoria, Ojo de bestia, Hoja negra de gárgola, Espadón del exterminador de dioses, Empañadura sacroderma, Aojo de puñal negro, Armadura de Cuchillo Negro, Sello maldito de la Muerte.

---

## 6. PUESTOS PROPUESTOS (del 5 al 1)

Lógica de escala: **sus guardias** (5) → **su cacería** (4) → **su nombre** (3) → **su guerra contra otra diosa** (2) → **la noche que lo cambió todo y lo que el juego te esconde** (1). Duración: gancho 1:30 · cinco puestos de 4:00–4:30 · suscripción ≈ 0:10 antes del n.º 1 · cierre 1:00 ≈ 25 min.

**Gancho propuesto:** que se OIGA S1 («O, Death. Become my blade, once more.») + la voz en español «Oh, Muerte. Conviértete en mi espada una vez más.» → «Casi todo el mundo cree que Maliketh es la víctima: el perro fiel de Márika al que le robaron la muerte. El juego esconde otra cosa.» + una línea a los que lo pidieron (bautivenier9997, AylanWar12, yoPisoPapas).

### N.º 5 — «Los guardias hechos de campeones muertos» (C1)
**Gancho:** «Antes de que veas a Gurranq, te para un guardia. Y ese guardia está remendado con grasa de muertos.»
1. El Fiel de la Hoja Negra en la puerta del Santuario (y en las Tierras prohibidas).
2. «Arreglada con adipocira ennegrecida. Esa es la marca de quienes sirven a Maliketh.» + qué es la adipocira: «el retal de los campeones».
3. El casco de Maliketh: «Los campeones sabían lo que estaba en juego…» (⚠ unir las dos frases es lectura nuestra).
**¿Lo sabía el jugador normal?** No: solo en el texto de las armas que suelta.

### N.º 4 — «D trabajaba para él» (C4)
**Gancho:** «Le diste nueve raíces a Gurranq. Ya lo contamos. Lo que no contamos es por qué existen esas raíces… y a quién usaba antes que a ti.»
1. Raíz mortuoria: la Runa robada «permitió la primera muerte de un semidiós» y luego «se extendió… por las raíces» → los muertos que caminan son **su** fallo.
2. D: «the beast himself wishes for someone to take my place» (parafrasear) → la bestia contrataba cazadores; tú eras el reemplazo.
3. S7 (4.ª raíz «there's something else») y la 5.ª: «no debe tocarla la mano del hombre».
4. Respuesta a @DarkShooter942 (lo de «guardar el arma»): ya en Sinluz; aquí el porqué.
**¿Lo sabía el jugador normal?** No (diálogo opcional de D + texto de la raíz).

### N.º 3 — «Muerte de los Semidioses» (C2)
**Gancho:** «Su nombre de bestia no era Gurranq. Significaba otra cosa.»
1. Piedra/Garra de la bestia Gurranq: «Muerte de los Semidioses» (te lo da él mismo, con la 6.ª y 8.ª raíz).
2. Casco/Armadura: «No había ni un solo semidiós que no lo temiese.»
3. Runa reparadora: la Orden Dorada se creó **tras** encerrar la Muerte → toda la edad dorada se levantó sobre su jaula. La hoja cosida a su carne.
**¿Lo sabía el jugador normal?** No: textos de encantamientos y armaduras.

### N.º 2 — «La reina que acunaba a los recién nacidos» (C3)
**Gancho:** «Antes de ser carcelero, fue verdugo de otra diosa.»
1. La Reina del Ojo Velado, «empírea elegida por los Dedos» (en el video de Melina, de pasada).
2. «…antes de sucumbir ante Maliketh» (su espada, Torre Sagrada de Caelid).
3. Empañadura: «acuna a los apóstoles recién nacidos… pronto crecerán y se convertirán en la fatalidad de los dioses» + Túnica: «la fuente de su poder fue sellada».
4. **Matiz:** los apóstoles desollaban dioses; el texto dice «derrota», no muerte.
**¿Lo sabía el jugador normal?** No.

### N.º 1 — «La noche que dejó robar la Muerte… y lo que dijo al morir» (C5 + C6 + C7 + C8) — la más escondida
**Gancho:** S16 (tráiler oficial: «On a night of wint'ry fog, the Rune of Death was stolen…»).
1. La puerta (ya conocida, una frase): Rogier/Ranni, Godwyn, la Devastación. **Su** fallo.
2. Lo escondido: Aojo «oculta la verdad de la conspiración»; Armadura de Cuchillo Negro: las asesinas, «númenes estrechamente vinculadas a la propia Márika»; Recuerdo: «Aun así, ella lo traicionó».
3. **⚠ ESPECULACIÓN como pregunta:** ¿le robaron la Muerte… o se la hizo robar su propia reina?
4. La prueba que casi nadie oyó: S9, Gurranq si lo matas: «¿Por qué… me engañaste? ¿Por qué… lo rompiste?»
5. Y lo que FromSoftware **quitó** (S14, «DIÁLOGO RECORTADO»): «¿Fui yo el necio, o tú me engañaste?»
**Cierre:** las dos muertes (C9): S3 «¿Para matar a quién?» / S6 «La Orden Dorada… no puede restaurarse» → cada jugador oyó una sola. Promo Crónicas de Tamriel al final.
**¿Lo sabía el jugador normal?** No: tres textos dispersos + una línea opcional + un diálogo recortado.

---

## 7. Datos falsos comunes que NO hay que decir

- «Maliketh **robó** la Muerte»: es la errata de la Hoja negra de Maliketh en español; el original dice que **se la robaron**.
- «Muerte destinada» como nombre oficial (dicho en Melina): en es-ES es **Muerte Escrita**; LatAm sin verificar.
- «Noche de los Cuchillos Negros» como oficial: es **Noche de los Puñales Negros** (las asesinas sí son «de los Cuchillos Negros»).
- «Márika ordenó robar la Muerte» como hecho: **⚠ ESPECULACIÓN**.
- «Maliketh mató a la Reina del Ojo Velado»: el texto dice «sucumbir» y «derrota».
- «Maliketh destruyó Nokron / Nokstella»: sin texto.
- «Maliketh y Messmer, hermanos sombra» / «Maliketh sale en Shadow of the Erdtree»: sin texto. Los Caballeros de la Muerte del DLC eran de Godwyn.
- Que el diálogo recortado ocurre en el juego: **no**; está en los archivos.
- «Gurranq ataca por comer la 4.ª raíz porque está envenenada»: el juego solo dice «there's something else» (⚠ ESPECULACIÓN la causa).
- «Maliketh es el gemelo/hijo de Márika»: el texto dice **hermanastro** y **sombra**.

---

## 8. Pendientes para la sesión de guion

1. **Diálogos en español** de Maliketh (salvo «Oh, Muerte…»), Gurranq y D: **NO VERIFICADOS** → parafrasear y que se oigan en inglés. Si se quiere el texto oficial: grabar/transcribir de un video en español (no encontrado hoy).
2. **«Destined Death» en LatAm**: NO VERIFICADO (es-ES = Muerte Escrita). Para @EdgarFelipe-d9y: solo afirmar el alias «Espada Negra» (fuente [ES-wiki]).
3. Capturas que faltan (§5): Santuario de la bestia, Gurranq comiendo, Fiel de la Hoja Negra, Torre Sagrada de Caelid, D, Godwyn en la Raíz profunda. Segundo exacto en los partes 4K NO VERIFICADO.
4. Marca de agua de las peleas sin HUD (C7h854v6Ax8, ijn3476GmKU, gYU5RwWaCDA) sin comprobar.
5. Coordenadas sin medir: Tierras prohibidas, Aldea de Aguainvocante, catacumbas (aprox.).
6. «Pigmeos»: referencia que salió en la investigación sin identificar → no usar.
7. Arena exacta de Maliketh en el dibujo de Farum Azula: NO VERIFICADA (usar el centro del remolino).
8. Regla de oro 10: S1, S3, S6, S9, S14 y S16 comprobadas con Whisper en la mezcla FINAL.
