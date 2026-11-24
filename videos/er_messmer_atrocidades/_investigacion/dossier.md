# Dossier: «Las 5 peores atrocidades de Messmer QUE IGNORASTE»

Canal Runa Caída. Investigación del 24-nov-2026. Todo lo de abajo sale de las fuentes enlazadas, leídas hoy por API, descarga directa, `yt-dlp` (solo subtítulos, capítulos, metadatos y cuadros sueltos) o Whisper `medium` sobre la pista de audio de clips cortos y de 4 tramos cortos del longplay (para fechar líneas; audio borrado después). Lo que no pude comprobar va marcado **NO VERIFICADO**. Cuando una afirmación es interpretación de la wiki (no texto del juego), lo digo.

## 0. Fuentes y cómo leerlas

| Clave | Fuente | Para qué sirve |
|---|---|---|
| **[ES-wiki]** | Wiki en español de Fandom, `https://eldenring.fandom.com/es/wiki/<Página>` (API `action=parse&prop=wikitext`) | Nombres oficiales; descripciones `{{Descripción\|ES=…}}` de 4 objetos de Messmer; **todas las líneas de Messmer en español** (página «Messmer el Empalador», sección Diálogo); texto oficial español de la expansión (Bandai Namco ES). **Wiki pequeña**: no tiene páginas de Insignia de cruzada, Mayal de serpiente, Armadura de Messmer, Bendición de Márika, etc., ni diálogos en español de Leda, el Cornamentado o la Anciana |
| **[EN-wiki]** | Wiki inglesa, `https://eldenring.fandom.com/wiki/<Page>` (API) | Descripciones EN y JP (`EN_line`/`JP_line`); diálogos completos: `Messmer the Impaler/dialogue`, `Hornsent/dialogue` (= el NPC Cornamentado), `Hornsent Grandam/dialogue`, `Needle Knight Leda/dialogue`, `Fire Knight Queelign/dialogue`, `Stranded Souls`. **Ojo**: «Background» mezcla texto con interpretación; solo cito como hecho lo que va entre comillas de un objeto o diálogo |
| **[EG]** | Eliteguías, `https://www.eliteguias.com/guias/e/er/elden-ring_<sección>-pNNN.php` (descarga directa; ISO-8859-1) | Descripciones en español transcritas del juego. **Tiene erratas** (marcadas con [sic] o corchetes). Índice del DLC: `elden-ring_shadow-of-the-erdtree.php`. **Sus páginas de personajes del DLC NO transcriben diálogos** |
| **[TR-ES]** | Subtítulos **manuales** en español (es y es-MX) del tráiler oficial *Story Trailer* de **BANDAI NAMCO Europe**, `6uT8wGtB3yQ` (bajados con `yt-dlp --write-subs`) | La única fuente oficial en español de las frases de Leda sobre la cruzada («Una purga sin Gracia ni honor. La tiranía de la llama de Messmer») |
| **[FX]** | Fextralife | No hizo falta: las líneas clave quedaron confirmadas por [EN-wiki] + subtítulos/Whisper de los clips |
| **[YT]** | Subtítulos automáticos (inglés) y capítulos con `yt-dlp` (sin video). **[WH]** = segundo medido con Whisper `medium` (palabra a palabra en los clips de voz sola: ±0,3 s; en tramos con música: ±2 s) | Fechar escenas y líneas |

### Nombres oficiales en español (verificados) — inglés → español

| Inglés | Español oficial | Fuente / nota |
|---|---|---|
| Messmer the Impaler | **Messmer el Empalador** | [ES-wiki], [EG] jefazos-p140 |
| Base Serpent Messmer (fase 2) | **Messmer serpiente primitiva** | [ES-wiki] (alias y título de la 2.ª fase) |
| Base serpent / wicked serpent | «serpiente primitiva» ([EG] Casco de serpiente alada) · «serpiente básica» ([EG] Casco de Messmer) · «serpiente malvada» ([EG] Yesca) · «serpiente malévola» ([EG] Recuerdo) | **El español no es uniforme**; en diálogo Messmer dice «la oscura serpiente del abismo» ([ES-wiki]). Para la voz: «la serpiente del abismo» o «la serpiente que llevaba dentro» |
| Winged serpents | **serpientes aladas** | [EG] Casco de Messmer / de serpiente alada |
| Realm of Shadow / Land of Shadow | **Reino de las Sombras** (objetos: Recuerdo del Empalador, Runa del Reino de las Sombras) | [EG], [ES-wiki]. El texto de marketing usa «la Tierra Sombría» ([ES-wiki] descripción oficial). **No** «Tierra de las Sombras» (lo dijo el video de Miquella) |
| Scadutree | **Árbol Umbrío** | [EG], [ES-wiki] |
| Erdtree / Golden Order | Árbol Áureo / Orden Dorada | [EG] |
| Crusade | **cruzada** («cruzada purificadora», «cruzada sagrada») | [EG] Armadura de Messmer, Insignia de cruzada |
| Hornsent | **cornamentados** (pueblo) · el NPC: **Cornamentado** | [EG] personajes-p59, Mayal de serpiente; [ES-wiki] «Cornamentado (personaje)». **No «Cornudo»** (lo dijo el video de Miquella) |
| Hornsent Grandam | **Anciana cornamentada** | [EG] personajes-p66, [ES-wiki] |
| Needle Knight Leda | **Caballera de la aguja Leda** / «Leda» | [ES-wiki], [EG] |
| Fire Knight(s) | **Caballero(s) de Fuego** | [EG] armaduras-p556/557 |
| Fire Knight Queelign | **Caballero de Fuego Queelign** | [EG] personajes-p70, [ES-wiki] (EG escribe también «Queeling» [sic]) |
| Fire Knight Hilde / Salza | **Caballera de Fuego Hilde** / **Salza, sabio de los Caballeros de Fuego** | [EG] cenizas-espiritus-p73, armaduras-p596 |
| Black Knights / Andreas / Huw | **Caballeros Negros** / **Andreas, comandante de los Caballeros Negros** / **Huw, capitán de los Caballeros Negros** | [EG] cenizas-espiritus-p71/p69 |
| Messmer Soldier | **soldado de Messmer** | [EG] |
| Commander Gaius / Rellana | **Comandante Gaius** / **Rellana, Caballera de Luna Gemela** | [EG], [ES-wiki] |
| Shadow Keep | **Fortaleza sombría** (en un mapa: «Fortaleza Sombría») | [EG], [ES-wiki] |
| Specimen Storehouse | **Almacén de especímenes** | [ES-wiki] |
| Shadow Keep, Church District | **Fortaleza sombría, distrito de la iglesia** | [ES-wiki] |
| Scadu Altus | **Altiplano Sombrío** | [EG], [ES-wiki] |
| Gravesite Plain | **Llanura de las Tumbas** | [EG], [ES-wiki] |
| Belurat, Tower Settlement | **Belurat, asentamiento de la torre** | [EG], [ES-wiki] |
| Scorched Ruins | **Ruinas calcinadas** | [ES-wiki] Llanura de las Tumbas |
| Castle Ensis | **Castillo de Ensis** | [EG], [ES-wiki] |
| Rauh Base / Ancient Ruins of Rauh | **Base de Rauh** / **Antiguas ruinas de Rauh** | [EG], [ES-wiki] |
| Village of Flies / Recluses' River | **Aldea de las moscas** / **Río de los ermitaños** | [EG] cenizas-espiritus-p79 |
| Bonny Village | **Aldea ósea** | [EG] (gesto «Oh, Madre» «en un cadáver… de la Aldea ósea»; [EN-wiki] lo sitúa junto a Bonny Village) |
| Church of the Crusade | **Iglesia de la Cruzada** | [ES-wiki] |
| Church of the Bud / Romina | **Iglesia del Brote** / **Romina, la santa del brote** | [EG] Mapa: Ruinas de Rauh, jefazos-p141 |
| Fort of Reprimand / Fog Rift Fort | **Fuerte de la reprimenda** / **Fuerte Grieta Neblinosa** | [EG] |
| Gaols (Belurat/Bonny/Lamenter's) | **Prisión de Belurat** / **Prisión de Bonny** / **Prisión de Doliente** | [EG] |
| Divine Beast Dancing Lion | **Bestia divina León Danzante** | [EG], [ES-wiki] |
| Sculpted keepers | **guardianes esculpidos** | [EG] Cabeza de bestia divina |
| Enir-Ilim | **Enir-Ilim** | [ES-wiki] |
| Messmer's Kindling | **Yesca de Messmer** | [EG] objetos-p859 = [ES-wiki] |
| Remembrance of the Impaler | **Recuerdo del Empalador** | [EG] objetos-p858 = [ES-wiki] |
| Spear of the Impaler / Messmer's Assault | **Lanza del Empalador** / habilidad **Asalto de Messmer** | [EG] armas-p376 = [ES-wiki] |
| Messmer's Orb | **Orbe de Messmer** | [EG] encantamientos-p120 = [ES-wiki] |
| Messmer's Helm / Armor / Gauntlets / Greaves | **Casco / Armadura / Guanteletes / Grebas de Messmer** | [EG] armaduras-p592–595 |
| Crusade Insignia | **Insignia de cruzada** | [EG] talismanes-p92 |
| Serpent Flail | **Mayal de serpiente** | [EG] armas-p331 |
| Serpent Crest Shield | **Escudo con blasón de serpiente** | [EG] escudos-p70 |
| Divine Beast Tornado | **Tornado de bestia divina** | [EG] encantamientos-p122 |
| Remembrance of the Dancing Lion | **Recuerdo del León Danzante** | [EG] objetos-p720 |
| Divine Beast Head | **Cabeza de bestia divina** | [EG] armaduras-p527 |
| Scorpion Stew / Gourmet | **Potaje de escorpión** / **Potaje de escorpión gourmet** ([EG]) · «Estofado de escorpión» ([ES-wiki]) | **Fuentes discrepan**: usar «potaje» (lo transcribe [EG] del objeto) |
| Watchful Spirit / Braided Cord Robe | **Espíritu vigilante** / **Túnica de cordón trenzado** | [ES-wiki] Anciana; [EG] armaduras-p588 |
| Marika's Rune | **Runa de Márika** | [EG] objetos-p744 |
| Shadow Realm Rune | **Runa del Reino de las Sombras** | [EG] objetos-p663 |
| Blessing of Marika | **Bendición de Márika** | [EG] objetos-p742 |
| Revered Spirit Ash | **Cenizas de espíritu venerado** | [EG] objetos-p648 |
| Messmerfire grease | **Grasa de fuego de Messmer** | [EG] objetos-p715 |
| Fire Knight Armor / Helm / Seal | **Armadura / Casco / Sello de Caballero de Fuego** | [EG] |
| Rain of Fire / Fire Serpent | **Lluvia de fuego** / **Serpiente de fuego** | [EG] encantamientos-p121/p112 |
| Queelign's Greatsword | **Espadón de Queelign** | [EG] armas-p348 |
| Iris of Grace / of Occultation | **Iris de la Gracia** / **Iris de la Ocultación** | [EG] (Queelign) |
| Hefty Furnace Pot / Furnace Visage / Furnace Golem | **Frasco de fragua grande** / **Rostro de fragua** / **Gólem de la fragua** | [EG] objetos-p673/p656; [ES-wiki] |
| Firespark Perfume Bottle | **Botella de perfume ígneo** | [EG] armas-p315 |
| Golden Vow (DLC, consumible) | **Juramento dorado** | [EG] objetos-p760 |
| Marika's Scarseal / Soreseal | **Marca cicatrizada de Márika** / **Marca ulcerada de Márika** | [EG] talismanes-p41/p79 |
| Miquella's Great Rune | **Gran Runa de Miquella** | [EG] objetos-p783. Mensaje en pantalla: «En algún lugar se ha roto una Gran Runa» ([ES-wiki]) — [EG] lo cita como «Una Gran Runa se ha roto...»: **fuentes discrepan** |
| Gesture "O Mother" | **Oh, Madre** | [EG] gestos |
| Stranded Soul | (alma estancada) | Nombre usado en el dossier de Rykard; no lo volví a comprobar hoy |

> **Lo que NO existe con el nombre del encargo:** **«Gran Runa de Messmer»**: no hay ningún objeto así (la wiki EN no tiene página; Messmer suelta Recuerdo y Yesca, [ES-wiki]); la Gran Runa que «rompe» la historia es **la de Miquella** (y ya se contó en el video de Miquella). **«Fuerte Gael»** es del juego base (Caelid), no del DLC; en el DLC hay **Fuerte de la reprimenda** y **Fuerte Grieta Neblinosa**. **«Gaol» = cárcel de Messmer**: falso, las prisiones del DLC son **de los cornamentados** (ver C9). **«Aldea de las Moscas» purgada por Messmer**: falso, es una **enfermedad** (ver C9). **Igon y Freyja**: no tienen texto que los ligue a la cruzada (Igon caza dragones; Freyja sirvió a Radahn y solo comenta que el Cornamentado «es de los cornamentados de la torre» [EN-wiki]) → ❌.

---

## 1. Quién es Messmer ✅ CONFIRMADO

**(a) Hijo de Márika, con una serpiente dentro**
- **Recuerdo del Empalador** ([EG] objetos-p858; errata «los sutituyó» = lo sustituyó; = [ES-wiki] primera línea): «Una serpiente malévola se retorcía dentro de Messmer, por lo que su madre le arrancó el ojo y [lo sustituyó] por un sello de Gracia. Sin embargo, su miedo la obligó luego a esconder a su hijo en el Reino de las Sombras. / Oculto junto al pecado original, su odio fue creciendo.»
  - EN: «…her fear compelled her to secret away her child within the realm of shadow. Hidden away—keeping company with the original sin, and a hatred that would not be confined.» JP: はじまりの罪と、忘れ得ぬ憎しみと共に («con el pecado original y un odio que no se puede olvidar»).
- **Casco de Messmer** ([EG] armaduras-p592): «Las serpientes aladas eran las eternas compañeras de Messmer. / Estuvieron ahí cuando la serpiente básica fue sellada tras su ojo. Estuvieron ahí durante toda su eternidad de sufrimiento. Y le seguirán acompañando en esta grotesca forma nueva, que nació tras destruir la Gracia otorgada por su madre. Las serpientes han aceptado su destino.»
- **Casco de serpiente alada** (de Kood, capitán de los Caballeros de Fuego; [EG] armaduras-p591): «La serpiente alada es el animal simbólico de las tropas militares de Messmer. Es una sabia amiga que mantiene a la serpiente primitiva a raya y controla su poder.»
- **Yesca de Messmer** ([EG] objetos-p859 = [ES-wiki]): «La llama que arde en el interior de Messmer. / Una cosa oscura consumida por una serpiente malvada. / Quema el árbol sellado que se dice que se encuentra en las antiguas ruinas de Rauh. / Messmer, al igual que su hermana menor, carga con la visión de fuego.» (**La última frase ya la usó el video de Melina.**)
- **Orbe de Messmer** ([EG] encantamientos-p120 = [ES-wiki]): «Messmer odiaba su propio fuego. Una y otra vez deseaba librarse de él, pero este seguía ardiendo.» (**Ya usado en el video de Melina.**)
- Padre: la [EN-wiki] dice «Radagon (potential father)» y que es «strongly implied» empíreo: **interpretación, NO decirlo como hecho**.

**(b) La cruzada fue encargo de su madre**
- **Armadura de Messmer** ([EG] armaduras-p593; igual en Guanteletes p594 y Grebas p595): «Por deseo de su madre, Messmer se convirtió en un símbolo aterrador para llevar a cabo la cruzada purificadora que ella ansiaba. / "**Centra en mí, y solo en mí, tus maldiciones, tu ira y tu pesar**".» (EN: «Direct thy maledictions, thine ire, and thy grief towards me alone.» Quién dice la frase entre comillas: el juego no lo indica.)
- **Escudo con blasón de serpiente** ([EG] escudos-p70; errata «otr»): «Se dice que se forjó para conmemorar los inicios de la cruzada iniciada por Messmer, hijo de Márika.»
- Texto oficial de la expansión (Bandai Namco ES, en [ES-wiki] «Descripción oficial»): «La Tierra Sombría. Un lugar ensombrecido por el Árbol Áureo. / Donde se produjo la primera venida de la diosa Márika. / **Un reino purgado en una batalla olvidada. / Y calcinado por la llama de Messmer.**»
- Leda en el tráiler oficial ([TR-ES] España, 6uT8wGtB3yQ 0:48–1:16): «Lo que vino después fue una guerra secreta. / Una sobre la que nunca podrían escribirse canciones. / **Una purga sin Gracia ni honor. / La tiranía de la llama de Messmer.**» (es-MX: «Después vino una guerra oculta. / Una guerra que no inspiró canción alguna. / Una purga sin Gracia ni honor. / La tiranía de las llamas de Messmer.») Antes: «Miquella el Gentil habló de los inicios. / De la traición y la felonía. / De cómo de este amor emergió el oro. / Pero también surgió la sombra.» **Es subtítulo de tráiler, no texto del juego**: decirlo como «Leda lo cuenta así».
- Leda en el juego ([EN-wiki] dialogue; [YT] longplay 5:42:00, en pantalla «Wondering about the hornsent, are you?»): «Long ago, Queen Marika commanded Sir Messmer to purge the tower folk. A cleansing by fire. It's no wonder the hornsent holds the Erdtree in contempt. That aside, man is by nature a creature of conquest. And in this regard, the tower folk are no different. They were never saints. They just happened to be on the losing side of a war. But it's still a wretched shame.» → **PARAFRASEAR** (español NO VERIFICADO).

**(c) Sus líneas: las únicas verificadas en español** ([ES-wiki] «Messmer el Empalador», Diálogo)
- Introducción: «*Intruso sarnoso.* / *Eres un Sinluz, según parece.* / *Madre, ¿acaso tu verdadero señorío sanciona / a alguien tan despojado de luz?* / *Aun así..., mi propósito no ha cambiado.* / ***Quienes se ven despojados del don del oro deberán hacer frente a la muerte... En el abrazo de la llama de Messmer.***»
- Entrando en la 2.ª fase: «*No pienso sufrir... / Frente a un señor desprovisto de luz. / Oh, madre, perdóname.* […] *Muy pronto, Sinluz... / Perecerás entre las fauces... / De la oscura serpiente del abismo.*»
- Si te mata en la 2.ª fase: «*Oh, criatura desprovista de luz... / Déjate caer en el olvido, al igual que haré yo.*»
- Al morir: «***Madre... Márika... / Una maldición... caerá sobre ti...***»
- EN ([EN-wiki] dialogue; [WH] qSRYSmEx0z0): «Mongrel intruder. Thou'rt... Tarnished, it seemeth. Mother, wouldst thou truly Lordship sanction, in one so bereft of light? Yet... My purpose standeth unchanged. Those stripped of the Grace of Gold shall all meet death. In the embrace of Messmer's flame.» / «I will not suffer... A lord devoid of light. O mother, forgive me.» / «Soon, Tarnished. Wilt thou be taken in the jaws... Of the abyssal serpent, shorn of light.» / «O lightless creature... Embrace thine oblivion, as shall I.» / «Mother... Marika... A curse...upon thee...»
- JP de la frase famosa ([EN-wiki]): 黄金の祝福無き全てに、死を («muerte a todos los que no tengan la bendición del oro») / メスメルの火を.
- [EN-wiki] nota: es **la única vez que llama a su madre por su nombre**. (Comprobable en el propio diálogo: en las demás líneas dice «Madre».)
- **Recortado, NO está en el juego** ([EN-wiki] {{cut}}): «Miquella spoke of thee...» (inicio alternativo), «The Erdtree wilt not sanction, ones as you, or I.» y una muerte alternativa: «Mother... Marika... For what purpose... did I...». Solo como dato curioso, diciendo que es material cortado.

**(d) URLs**
- https://eldenring.fandom.com/es/wiki/Messmer_el_Empalador · …/Yesca_de_Messmer · …/Recuerdo_del_Empalador · …/Orbe_de_Messmer · …/Lanza_del_Empalador · …/Reino_de_las_Sombras · …/Elden_Ring:_Shadow_of_the_Erdtree · …/Anciana_cornamentada · …/Cornamentado_(personaje)
- https://eldenring.fandom.com/wiki/Messmer_the_Impaler · …/Messmer_the_Impaler/dialogue · …/Crusade · …/Base_Serpent · …/Hornsent/dialogue · …/Hornsent_Grandam/dialogue · …/Needle_Knight_Leda/dialogue · …/Fire_Knight_Queelign/dialogue · …/Stranded_Souls
- https://www.eliteguias.com/guias/e/er/elden-ring_objetos-p858.php · …objetos-p859.php · …armaduras-p592.php · …armaduras-p593.php · …escudos-p70.php · …encantamientos-p120.php
- Tráiler: https://www.youtube.com/watch?v=6uT8wGtB3yQ (subtítulos es / es-MX)

---

## 2. CANDIDATAS (12), cada una con veredicto

### C1. La medalla de la cruzada: empalar, quemar y disfrutarlo ✅ CONFIRMADO (material nuevo)
- **Insignia de cruzada** ([EG] talismanes-p92): «Talismán con una lanza alzada sobre un fondo llameante, en recuerdo de los caídos en la cruzada sagrada liderada por Messmer. / **Aumenta la potencia de ataque tras derrotar a un enemigo.** / Los cruzados olvidaron el honor y la piedad para **empalar y quemar sin misericordia a quienes consideraban impuros**. / **Quienes se sentían estimulados por los gritos de muerte eran los mismos que abogaban por la santidad de la campaña.**»
  - EN: «…to wantonly impale and scorch those deemed impure. Those who felt invigorated by each cry of death were the same men who were certain of the sanctity of the campaign.» JP: ただ、それを聖戦と信じる者だけが / 絶命の声に高揚を見出すのだ («solo quienes creen que es una guerra santa encuentran euforia en los gritos de muerte»).
  - **Lo que ignoraste:** el efecto del talismán **es** la frase: te sube el ataque cada vez que matas. Llevabas colgada la medalla de los que se excitaban con los gritos.
  - Quién te la da: el **Caballero de Fuego Queelign** al vencerlo cuando te invade en **Belurat** ([EG] talismanes-p92: «Lo suelta el espíritu rojo Caball[er]o de Fuego Queelign al derrotarlo en Belurat, asentamiento de la torre»; [ES-wiki] Queelign). Errata [EG]: «Caballeo».
- **Queelign** ([EN-wiki] dialogue; [YT] 3wQCfgdGfec 0:03–0:11): al matarte grita «Queen Marika, behold! I have excised another. Another cancer to thy joy.» Al invadir: «Those stripped of the Grace of Gold shall all meet death. In the embrace of Messmer's flame.» / «All ye spurned by Grace. Kneel evermore. Before the flame of Messmer.» Al caer: «Ahh, how could this be... Forsake me not... Queen Marika, my grace...» → **PARAFRASEAR**.
  - **Espadón de Queelign** ([EG] armas-p348): «Queelign se volcó en su cruzada y reforjó este espadón con la forma de la lanza de su soberano, con la esperanza de ser un segundo empalador» [sic, sin punto].
  - Ceniza **Caballero de Fuego Queelign** ([EG] cenizas-espiritus-p72): «Blande un espadón en forma de lanza que **empala al enemigo en fuego para alejar a la bella madre Márika de la impureza**. / Esa Gracia, aunque efímera, fue su salvación. / Y una vez salvado, lo único que le quedaba era la guerra.» (Se la da si le pones el **Iris de la Gracia**; con el **Iris de la Ocultación** te da el espadón. [EN-wiki] Iris: los sacerdotes del Árbol Áureo los usaban en el Reino de las Sombras para «calmar» o «avivar» el miedo de sus fieles.)
- **Lo que dice Messmer que lo une a ti:** «Quienes se ven despojados del don del oro deberán hacer frente a la muerte» [ES-wiki]. Tú eres un **Sinluz**, «despojado» de la gracia: él mismo te lo dice al verte («Eres un Sinluz… alguien tan despojado de luz»). El objetivo de la cruzada no eran solo los cornamentados: era **cualquiera sin la gracia del oro**. Lectura del narrador, apoyada en el texto literal.
- **URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_talismanes-p92.php · …armas-p348.php · …cenizas-espiritus-p72.php · https://eldenring.fandom.com/wiki/Fire_Knight_Queelign/dialogue · https://eldenring.fandom.com/wiki/Crusade_Insignia

### C2. Los dioses colgados de sus lanzas: de ahí sale «el Empalador» ✅ CONFIRMADO
- **Tornado de bestia divina** ([EG] encantamientos-p122; lo suelta el León Danzante de las Antiguas ruinas de Rauh): «**La mayoría de las bestias divinas fueron destripadas y colgadas en las lanzas de Messmer, antes de ser calcinadas en sus llamas.** / Quienes lo vieron lo comparan con una **pira funeraria para la propia torre**.»
  - JP: 神獣の多くは、串刺しの槍に晒され («la mayoría de las bestias divinas fueron expuestas en las lanzas de empalar»). **串刺し (kushizashi, empalar) es la misma palabra de su título**, 串刺し公 («el señor del empalamiento»). Que el apodo venga de aquí lo dice la [EN-wiki] (Crusade): **interpretación**; el dato del kanji es comprobable.
- **Bestia divina furiosa** ([EG] talismanes-p94; errata «Lasbestias»): «Las bestias divinas son mensajeras de los cielos y su furia refleja el tumulto de las alturas…»
- **Recuerdo del León Danzante** ([EG] objetos-p720; errata «Emparador»): «Al asaltar la torre el ejército del [Empalador], el ritual de la danza del león tomó tintes marciales con su divinidad, furia y belleza liviana.»
- **Cabeza de bestia divina** ([EG] armaduras-p527): «Máscara ritual con forma de la cabeza de una bestia divina capaz de llevar a cabo la danza del león. Usada por los mejores guardianes esculpidos. **Ya no responde a las sinceras plegarias de la anciana.**»
- La cinemática del León Danzante en Belurat lleva **el canto de la Anciana** ([EN-wiki] Hornsent Grandam/dialogue, «Theatre of the Divine Beast cutscene»): «O Horn-deck'd beast, from higher sphere deliver'd. Take root inside the tower's sculpted keepers. […] Dance and cavort, cleanse all that thou wilt. Cruelty, woe, and those who plague the tower. Cleanse away the strumpet's vile progeny.» → **PARAFRASEAR**. Es decir: la bestia que matas es **la plegaria de una anciana contra los hijos de Márika**.
- Escena del tráiler (no juego): criatura atravesada por varias lanzas entre soldados en una escalinata ardiendo ([TR] 6uT8wGtB3yQ ~1:04; captura `pantallas/trailer_criatura_atravesada_lanzas.jpg`). Que sea una bestia divina: **NO VERIFICADO** (parece cuadrúpeda con cuernos/ramas; decir «una criatura atravesada»).
- **URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_encantamientos-p122.php · …talismanes-p94.php · …objetos-p720.php · …armaduras-p527.php · https://eldenring.fandom.com/wiki/Divine_Beast_Tornado

### C3. La aldea de la abuela: el genocidio en primera persona ✅ CONFIRMADO
- **La Anciana cornamentada**, encerrada en un almacén de Belurat (necesitas la Llave del almacén, [EG] objetos-p716), te toma por soldado de Messmer ([EN-wiki] dialogue; [YT] p3JX1YVDYc0 0:19–0:52): «…by the look of thee, another of Messmer's peons, methinks. Tell me, dost thy kind never weary grow? How do these old bones fascinate thee yet? **Our lands were by thy kind set aflame, our tower by thy kind veiled in shadow. Thou cam'st, robbing us of all, spoiling all. Have ye not basked in these deeds long enough?** Listen, progeny of the wanton strumpet. For thy sins thou shalt have thy recompense—the sacred beast shall unleash its ire.» Si la atacas: «Didst thou imagine I would beg thee cease? […] Heaven shall judge thee all for thy deeds!» → **PARAFRASEAR**. («strumpet» = ramera: así llama a **Márika**; el español oficial **NO VERIFICADO**, decir «la ramera» solo como paráfrasis.)
- **Potaje de escorpión** ([EG] objetos-p722; errata «negociación» = negación): «Escorpión cocido en una sopa negra. / Receta típica de los cornamentados. […] **Antaño la preparaban con mimo las abuelas de la familia. / Al haberse enfriado hace tiempo, esta sopa desprende un olor rancio y agrio.**» (EN: «Once made with love by a certain elderly woman for the family table.» — **el español generaliza** a «las abuelas»).
- **Potaje de escorpión gourmet** ([EG] objetos-p869; errata «ene el»), tras matar a Messmer: «Los pensamientos y sentimientos del cocinero se funden y mezclan en el guiso, aunque **pocos saben distinguir el sabor del amor**. / Come, come hasta saciarte.»
- **Espíritu vigilante** ([EN-wiki]; se lo da la Anciana si llevas la Cabeza de bestia divina): «"Take vengeance upon Messmer and his lot. They who betrayed us, aye, they who burned us... Let them face in thy wrath their just deserts."» (Español del objeto **NO VERIFICADO**: no está en [EG] ni [ES-wiki].) En el longplay se ve con subtítulo: 3:37:02 «Have my son accompany thee to war.» / 3:37:12 «Take vengeance upon Messmer and his lot.»
- **El Cornamentado** (su hijo, según la propia Anciana: «Have my son accompany thee to war», [EN-wiki]): «**O mother, O most cherished wife and child.** It seems vengeance was not mine to enact.» (si no consigue vengarse) y al morir: «Apologies... O Mother, wife, and...chil...» ([YT] INoq5UMCr-o 5:54–6:02). Contra Messmer ([WH] 6m4rlHbjecA): «Messmer, foe of my beloved people. In vengeance for the flames, my blade I wield. […] My clan's suffering. Their pain. All that they felt. Do you understand now? Your ugliness.» Después ([YT] Sfo5u4vWJ-4 0:06–0:27): «Upon his end, did you see Messmer's face? Twas sublime—a very tangle of snakes! **To think he dared to call us savages. When he himself was most base of all.**» JP: よくも、我らを汚物と呼んだものだ («¡cómo se atrevió a llamarnos **inmundicia**!»). → **PARAFRASEAR**. Que su madre, esposa e hijo murieran **en la cruzada**: el juego no lo dice con esas palabras; se deduce de su venganza «por las llamas» → decirlo como pregunta.
- **Almas estancadas** de la Llanura de las Tumbas ([EN-wiki] Stranded Souls): junto a las **Ruinas calcinadas**: «Ev'ryone...burned to cinders...burned away. **Put to the torch...by Messmer...and his lot. What did we do to deserve such a fate? We merely lived our lives... We lived in peace...**» Al pie de un árbol al noreste de las Ruinas calcinadas: «I know... All your resentment lingers yet... The raw stuff from which I shall surely forge a curse. Upon the dastard Messmer's head. Upon Marika's children each and all.» → **PARAFRASEAR**; segundo en video **NO VERIFICADO**.
- **Mayal de serpiente** ([EG] armas-p331; está en un cofre del Fuerte Grieta Neblinosa): «El fuego ruge en el interior de los cuerpos de las serpientes, infligiendo terribles quemaduras. / Algunos del ejército de Messmer usaron estos mayales para **quemar a los cornamentados y marcarlos con agonía y miedo**.»
- **Mapa: Llanura de las Tumbas** ([EG] objetos-p639; erratas «llnaura», «estaá»; = [ES-wiki]): «Una sombría llanura cubierta de sepulcros espirituales. La torre espiral de los cornamentados se encuentra al noroeste, y toda la zona está dañada por los horripilantes estragos de la guerra.»
- **Túnica de cordón trenzado** ([EG] armaduras-p588): «Atavío de los cornamentados en busca de venganza. / El cordón trenzado une el juramento del vengador al rencor de las víctimas. Jamás debe deshacerse.»
- **Matiz obligatorio (ver C9):** Leda: «nunca fueron santos». Los cornamentados metían a gente en jarras.
- **URLs:** https://eldenring.fandom.com/wiki/Hornsent_Grandam/dialogue · https://eldenring.fandom.com/wiki/Hornsent/dialogue · https://eldenring.fandom.com/wiki/Stranded_Souls · https://www.eliteguias.com/guias/e/er/elden-ring_objetos-p722.php · …objetos-p869.php · …armas-p331.php · …armaduras-p588.php · …objetos-p639.php

### C4. Lo que le hizo a los suyos: caballeros presos, presidiarios al frente ✅ CONFIRMADO
- **Andreas, comandante de los Caballeros Negros** ([EG] cenizas-espiritus-p71; ataúd en las Catacumbas de Grieta Neblinosa): «Los Caballeros Negros eran la fuerza principal del ejército de Messmer. […] Aunque tras su huida del Árbol Áureo siguió siendo un devoto seguidor de Messmer, **se rebeló tras conocer la naturaleza reptiliana de su señor. Por ello, fue encarcelado en una tumba subterránea.**» (EN: «His righteous stand was rewarded with imprisonment…» — el español quita «justa».)
- **Huw, capitán de los Caballeros Negros** ([EG] cenizas-espiritus-p69; altar en las Catacumbas del río Escorpión): «Pese a dominar la caza de la bestia divina, **siguió a su padre, Andreas, en la rebelión contra Messmer, y al igual que él, fue encarcelado en una tumba subterránea.** / **Messmer lloró la pérdida de un hermano de armas.**»
  - **Lo que ignoraste:** dos cenizas que puedes invocar son **un padre y un hijo enterrados vivos** (encarcelados en una tumba) por enterarse de que su señor era una serpiente. Y él «lloró» al hijo.
- **Cenizas de soldado de Messmer** ([EG] cenizas-espiritus-p68; junto a unas lápidas del Fuerte de la reprimenda): «Estos soldados pertenecían al **vil batallón penitenciario** y fueron enterrados **fuera de la vista del Árbol Umbrío**.»
- **Armadura de soldado de Messmer** ([EG] armaduras-p493): «Aunque la pechera luce un motivo del Árbol Umbrío, se ha usado oro para su grabado. **Una pequeña consolación para quienes están obligados a combatir sin gracia ni honor.**» (Igual en Casco de soldado p492 y Armadura de Caballero Negro p497.)
- **Hacha de soldado de Messmer** ([EG] armas-p306; errata «la la»): «La favorita de quienes se perdieron a si mismos en la guerra de su señor.»
- **Casco de Caballero Negro** ([EG] armaduras-p496; errata «oramentos»): «…desprende un persistente hedor a podrido. / El olor podría proceder de la sangre contaminada que lo salpicó. O quien sabe si la causante es la propia alma ennegrecida del portador **tras una matanza sin fin**.»
- **Casco de Caballero de Fuego** ([EG] armaduras-p556; errata «jugar lealtad» = jurar): «Todos los caballeros provenían de alguna importante familia de los niveles superiores del Árbol Áureo, pero **fueron marginados, perseguidos y expulsados de sus hogares tras [jurar] lealtad a Messmer** como su señor.»
- **Armadura de Caballero de Fuego** ([EG] armaduras-p557): «Solo ellos llegaron a conocer de verdad a Messmer. Sus llamas son como serpientes. Tal es el destino que acompañaba a su forma maldita.»
- **Botella de perfume ígneo** ([EG] armas-p315): «La cruzada fue una purga violenta en la que participaron como guerreros.» (EN: «…the perfumers were not called there to heal.»)
- **Grasa de fuego de Messmer** ([EG] objetos-p715): «El fuego era un símbolo de la cruzada, e incluso los soldados rasos de Messmer lo usaban.» + **Chispa aromática** ([EG] objetos-p574): «Aunque el fuego estaba prohibido entre aquellos que servían al Árbol Áureo, con el avance de la guerra esta regla fue dejándose de lado.»
- **Almas estancadas** de soldados ([EN-wiki] Stranded Souls, ubicación sin dato): «O Marika... I beg...embrace your child... And give us a sign. How long must this holy war stretch on?» / «We have not been abandoned. Messmer is the son of Queen Marika... Her Grace would never abandon her own flesh and blood...» → **PARAFRASEAR**; ubicación **NO VERIFICADA**.
- **URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_cenizas-espiritus-p71.php · …cenizas-espiritus-p69.php · …cenizas-espiritus-p68.php · …armaduras-p493.php · …armaduras-p496.php · …armaduras-p556.php · …armaduras-p557.php · …armas-p306.php · …armas-p315.php

### C5. Quemar la biblioteca: Rauh, los especímenes y la iglesia de Romina ✅ CONFIRMADO con matiz
- **Capucha de Salza** ([EG] armaduras-p596): «Discípulo del sabio Wego, **se negó a quemar unas ruinas antiguas, incluso a pesar de jugarse la vida**.»
- **Lluvia de fuego** (encantamiento de Salza; [EG] encantamientos-p121): «Salza siempre mantuvo su desdén al barbarismo, **incluso a pesar de quemar más aldeas y calcinar más tierras que nadie**.» (Lo suelta el Caballero de Fuego del puente que va a las Antiguas ruinas de Rauh.)
- **Caballera de Fuego Hilde** ([EG] cenizas-espiritus-p73): «Hilde era una gran amiga del sabio Salza y **se unió a quienes insistieron en preservar los especímenes**. Las cenizas de Hilde se consagraron como amuleto para proteger el almacén.»
- **Matiz obligatorio:** ningún texto dice «Messmer ordenó quemar Rauh». Se deduce: Salza «se negó» arriesgando la vida (alguien lo ordenó) y Hilde «insistió en preservar» (alguien quería destruir). Decirlo así: «hubo que jugarse la vida para que **no** lo quemaran».
- **Recuerdo de la santa del brote** ([EG] objetos-p870): «**Después de que la iglesia se quemara**, Romina descubrió un retorcido elemento divino que entretejió en la torva putrefacción roja.» + **Hoja enastada del Brote** ([EG] armas-p379): «Una vez, en una iglesia en llamas, Romina alzó el brote en silencio.» → **el texto no dice quién quemó la iglesia**; la [EN-wiki] (Crusade) lo atribuye a los cruzados: **interpretación**.
- **Mapa: Ruinas de Rauh** ([EG] objetos-p765; erratas «aibsmo», «AL»): «Estas gigantescas ruinas están inundadas, arrasadas por la naturaleza y divididas en dos por un abismo. Al suroeste se encuentra la Iglesia del Brote, que supervisa la Torre de la Sombra.»
- **Lo que ignoraste:** el «sabio» de sus caballeros, el que despreciaba la barbarie, es el que **más aldeas quemó** de toda la cruzada.
- **URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_armaduras-p596.php · …encantamientos-p121.php · …cenizas-espiritus-p73.php · …objetos-p870.php · …armas-p379.php · …objetos-p765.php

### C6. El hijo escondido: el ojo arrancado y la medicina que nunca más hubo ✅ CONFIRMADO (víctima, no verdugo → cierre)
- Recuerdo del Empalador (§1a): «su madre le arrancó el ojo […] su miedo la obligó luego a esconder a su hijo».
- **Bendición de Márika** ([EN-wiki] Blessing of Marika; está en un cadáver a las afueras del Fuerte de la reprimenda y la sueltan los dos Centinelas del interior de Vista Sombría, [EG] objetos-p742): EN «A special physick blessed by Marika, the queen of the Erdtree. Completely restores HP and heals all ailments. **Marika once created several of these physicks for Messmer's sake. But never again.**» JP: 彼女は、メスメルのために、この霊薬を幾つか作った / その後、二度とそうすることはなかった (= EN).
  - ⚠ **[EG] transcribe distinto**: «Creada por Márika para Messmer. Fue la única que preparó.» — contradice EN y JP («varias… nunca más»). **Español oficial NO VERIFICADO** → PARAFRASEAR con EN/JP: «Márika hizo unas cuantas para Messmer. Y nunca más volvió a hacerlo».
  - **Lo que ignoraste:** la poción que te curó todo de golpe era **la medicina que una madre hizo para su hijo… antes de abandonarlo**. Y te la bebiste tú.
- **Runa de Márika** ([EG] objetos-p744): «Restos dorados de la Gracia concedida personalmente por la reina Márika a los héroes que se unieron a la cruzada por ella. / Úsalos para obtener 80.000 runas.» → **los cambiaste por runas**.
- **Runa del Reino de las Sombras** ([EG] objetos-p663): «Restos dorados de la Gracia concedida a quienes cayeron en el Reino de las Sombras.»
- **Juramento dorado** ([EG] objetos-p760): «El encantamiento sirve como rito para honrar a los camaradas fieles al lejano Árbol Áureo que cayeron en la cruzada.»
- **Gesto «Oh, Madre»** ([EG] gestos: «En un cadáver en el punto indicado de la Aldea ósea»): según [EN-wiki] (O Mother; Hinterland) se usa **delante de la estatua de Márika bajo la sala de Messmer** para abrir la zona secreta de la Tierra interior (Hinterland), donde está la aldea natal de Márika. Que la estatua sea «Márika con Messmer bebé» lo dice la [EN-wiki] (galería: «Marika and baby Messmer statue render»): **NO VERIFICADO** en texto del juego.
- Para la voz: su muerte «Madre... Márika... Una maldición... caerá sobre ti...» [ES-wiki] ✅.

### C7. La serpiente: la naturaleza que escondía ⚠ MARCO (no atrocidad)
- Casco de Messmer, Casco de serpiente alada, Yesca (§1a). Fase 2: rompe la Gracia de su madre y se transforma ([EG] Casco de Messmer: «grotesca forma nueva, que nació tras destruir la Gracia otorgada por su madre»).
- Sirve de bisagra para C4 (los Caballeros Negros se rebelaron al descubrirla) y para el gancho del n.º 1.
- Lo de que la serpiente fuera la misma de Rykard o de los hombres serpiente: **sin texto** → no decirlo. ([EN-wiki] Base Serpent, «See also» enlaza a God-Devouring Serpent, pero sin afirmación.)

### C8. Sus amigos y su espada ⚠ CAMEO
- **Recuerdo del Jinete del Jabalí** ([EG] objetos-p785): «Ambos eran como hermanos mayores del león y estaban malditos de nacimiento. Pese a ello, o tal vez a causa de ello, Gaius fue tanto amigo de Messmer como líder de sus hombres.»
- **Recuerdo de la Cab. de la Luna Gemela** ([EG] objetos-p729): «Rellana, antigua princesa cariana, renegó de su derecho de nacimiento y permaneció junto a Messmer, sabiendo que ni siquiera el brillo de la luna podría socorrerlo. / Pronto se convirtió en la Espada de Messmer.»
- **Mapa: Altiplano Sombrío** ([EG] objetos-p733; errata «ansía»): «La meseta ocupada por el ejército de Messmer que observa con ansia al Árbol Umbrío al noreste, recibe su nombre de su equivalente en el reino del Árbol Áureo. En su centro se encuentra la Fortaleza Sombría.»

### C9. Los cornamentados tampoco eran santos ⚠ MATIZ OBLIGATORIO (para no vender víctimas puras)
- Leda (§1b): «They were never saints. They just happened to be on the losing side of a war.»
- **Prisiones (Gaols)**: son de los cornamentados, no de Messmer. **Cuchillo carnicero de Bonny** ([EN-wiki] Bonny Butchering Knife): «An outsize butcher's cleaver used to dismember human bodies in the making of the great jars stored in the gaols.» **Gran tinaja** ([EN-wiki] Greatjar): «They offer their prayers to the innards of the greatjars, such that they might be reborn one day into sainthood. This is the cycle of death and rebirth, taken into the hands of mortal men.» Alma estancada de la **Prisión de Belurat** ([EN-wiki] Stranded Souls): «Oh please. Not the jar... Anything but that! I promise. I won't ever do it again!» Otra: «For pity's sake, your place is in the jar. Nigh-sainthood itself awaits you within. For shamans like you, this is your lot.» → **PARAFRASEAR** (nombres españoles de esos objetos **NO VERIFICADOS**).
- **Aldea de las moscas** ([EG] cenizas-espiritus-p79, Cenizas de hombre mosca): «Los cornamentados afectados acaban adoptando una forma parecida a la de una mosca. Se creía que al experimentar tal transformación, se liberaban de todo sufrimiento.» → **una enfermedad, no una purga** ([EN-wiki] Village of Flies: «succumbed to the fly sickness»).
- **Cenizas de espíritu venerado** ([EG] objetos-p648): «Se consiguen a partir de **cadáveres de cornamentados** y otros objetos que decoran ciudades y aldeas por todo el Reino de las Sombras. […] Los cadáveres marchitos eran deidades tutelares…» → **son sus propios muertos rituales**, no víctimas de Messmer. Cameo: «tus invocaciones las subiste con cenizas de cadáveres de cornamentados».
- Uso en guion: **una frase** de abogado del diablo antes del n.º 2 o 3; no un puesto.

### C10. Belurat y el resto del mapa arrasado ⚠ APOYO DE ESCENARIO
- Que el ejército de Messmer arrasara Belurat, la Ciudad de posibilidades, la Aldea ósea, las Ruinas de Unte, etc., **lo dicen la [EN-wiki] (Crusade) y la [ES-wiki] (Anciana: «Su pueblo fue reducido a cenizas por Messmer el Empalador y su ejército»)**, no un texto concreto del juego. Lo que sí es texto: la Anciana («nuestras tierras fueron incendiadas por los tuyos») y el alma de las Ruinas calcinadas («quemados… por Messmer y los suyos»). Usar esas dos.
- Queelign invade **en Belurat** y en la **Iglesia de la Cruzada** (estatua de Márika sin cabeza, [EN-wiki]).

### C11. La Gran Runa rota ❌ YA CONTADO (video de Miquella) + no es de Messmer
- `videos/er_miquella_atrocidades/guion.py` (escena p5b): «Cuando te acercas a la fortaleza de Messmer, una luz dorada estalla en el cielo: Miquella ha roto su Gran Runa.» + Freyja, Thiollier, Leda.
- Messmer **no tiene Gran Runa** (§0). Como mucho, una frase de transición.

### C12. Otros que no dan para puesto
| Tema | Veredicto | Dato |
|---|---|---|
| Messmer y los gigantes | ❌ Ya corregido en el video de Rykard (intro, comentario de @m0h4xd_727) | dossier de Rykard §9 |
| Messmer, hermano de Melina | ❌ Ya contado (video de Melina, p4/p4b: Yesca y Orbe con sus descripciones) | — |
| Igon / Freyja | ❌ Sin texto sobre la cruzada | §0 |
| «Marca ulcerada/cicatrizada de Márika» = el sello del ojo de Messmer | ⚠ **Interpretación**: el talismán es «un ojo grabado con una Runa de Elden. Se dice que se trata del sello de la Reina Márika» ([EG] talismanes-p41/p79) y la [EN-wiki] enlaza el sello de Messmer a esa página, pero **ningún texto del juego dice que sea el mismo**. Si se usa: «¿te suena…?» como pregunta, nunca como hecho | Muy popular en builds → tentador para el gancho; marcar como teoría |
| Messmer hijo de Radagon | ❌ Interpretación ([EN-wiki] «potential father») | — |
| Frasco de fragua grande | ⚠ cameo: «Las llamas de la fragua consumen el cuerpo y el alma. Cuando esa eliminación de la impureza se produce, se conoce como purificación» ([EG] objetos-p673; errata «peude»). **No dice Messmer** | — |
| Comandante de los «cruzados» que quemaron la iglesia de Romina | ❌ Sin texto (C5) | — |

### LO YA CONTADO EN EL CANAL (grep de `Messmer|cornamentad|Hornsent|Belurat|Reino de las Sombras` en `videos/er_*/guion.py`)
- `er_melina_atrocidades/guion.py` p4 y p4b: Yesca de Messmer («al igual que su hermana menor… visión del fuego»), Orbe de Messmer («despreciaba su propio fuego»), la frase «todos los despojados de la gracia del oro hallarán la muerte, en el abrazo de la llama de Mésmer» (**ojo: la dijo con otra traducción**, no la de [ES-wiki]). Y dice: «**Ya hicimos un video entero de lo que Mésmer hizo con ese fuego en el Reino de las Sombras**» → en `canales/runa_caida.json` **no hay ningún video de Messmer publicado**: o se refiere a otra cosa o es un error del guion de Melina; este video puede presentarse como «el que os prometimos». (NO VERIFICADO a qué se refería.)
- `er_miquella_atrocidades/guion.py` p5/p5b: el grupo de Miquella con «**un Cornudo que odia a Márika**» (nombre mal: es **Cornamentado**), la Gran Runa rota al acercarte a la fortaleza de Messmer, Leda que «va por el Cornudo… la venganza cambia a un hombre», Ansbach, Freyja. Usa «Tierra de las Sombras» (mal: **Reino de las Sombras**).
- `er_rykard_atrocidades/guion.py` intro: «Messmer… su cruzada purificadora quemó a los cornamentados en el Reino de las Sombras» (respuesta a los gigantes).
- `er_godfrey_atrocidades`, `er_godrick_atrocidades`, `er_radahn_atrocidades`: solo «Messmer está apuntado» en los comentarios y la pronunciación «Mésmer».
- **Ángulo nuevo para lo que se toca otra vez:** la Yesca solo para «la llama que arde dentro»; el Orbe no se relee; el Cornamentado se presenta con su nombre correcto y se dice en una frase «el que en el video de Miquella llamamos, mal, Cornudo».

---

## 3. Citas listas para usar (estado de verificación)

| Cita | Idioma | Estado |
|---|---|---|
| «Quienes se ven despojados del don del oro deberán hacer frente a la muerte... En el abrazo de la llama de Messmer.» | ES | ✅ [ES-wiki] (diálogo y cita de cabecera) |
| «Intruso sarnoso. Eres un Sinluz, según parece. Madre, ¿acaso tu verdadero señorío sanciona a alguien tan despojado de luz? Aun así..., mi propósito no ha cambiado.» | ES | ✅ [ES-wiki] |
| «No pienso sufrir... Frente a un señor desprovisto de luz. Oh, madre, perdóname.» | ES | ✅ [ES-wiki] |
| «Muy pronto, Sinluz... Perecerás entre las fauces... De la oscura serpiente del abismo.» | ES | ✅ [ES-wiki] |
| «Madre... Márika... Una maldición... caerá sobre ti...» | ES | ✅ [ES-wiki] |
| Mismas líneas en inglés (para que se OIGAN) | EN | ✅ [EN-wiki] + [WH] qSRYSmEx0z0 (ver §5) |
| Insignia de cruzada: «…empalar y quemar sin misericordia a quienes consideraban impuros. Quienes se sentían estimulados por los gritos de muerte eran los mismos que abogaban por la santidad de la campaña.» | ES | ✅ [EG] (una fuente española; EN/JP coinciden) |
| Tornado de bestia divina: «La mayoría de las bestias divinas fueron destripadas y colgadas en las lanzas de Messmer, antes de ser calcinadas en sus llamas. Quienes lo vieron lo comparan con una pira funeraria para la propia torre.» | ES | ✅ [EG] |
| Armadura de Messmer: «Por deseo de su madre, Messmer se convirtió en un símbolo aterrador para llevar a cabo la cruzada purificadora que ella ansiaba. "Centra en mí, y solo en mí, tus maldiciones, tu ira y tu pesar".» | ES | ✅ [EG] (×3 piezas) |
| Recuerdo del Empalador: «…su madre le arrancó el ojo y [lo] sustituyó por un sello de Gracia. Sin embargo, su miedo la obligó luego a esconder a su hijo en el Reino de las Sombras. Oculto junto al pecado original, su odio fue creciendo.» | ES | ✅ [EG] (errata «los sutituyó»); 1.ª línea = [ES-wiki] |
| Casco de Messmer: «…Estuvieron ahí cuando la serpiente básica fue sellada tras su ojo… grotesca forma nueva, que nació tras destruir la Gracia otorgada por su madre.» | ES | ✅ [EG] |
| Yesca de Messmer: «La llama que arde en el interior de Messmer. Una cosa oscura consumida por una serpiente malvada.» | ES | ✅ [EG] = [ES-wiki] (la frase de la hermana ya usada) |
| Escudo con blasón de serpiente: «…conmemorar los inicios de la cruzada iniciada por Messmer, hijo de Márika.» | ES | ✅ [EG] |
| Mayal de serpiente: «…usaron estos mayales para quemar a los cornamentados y marcarlos con agonía y miedo.» | ES | ✅ [EG] |
| Recuerdo del León Danzante / Cabeza de bestia divina («Ya no responde a las sinceras plegarias de la anciana») | ES | ✅ [EG] (errata «Emparador») |
| Potaje de escorpión: «Antaño la preparaban con mimo las abuelas de la familia. Al haberse enfriado hace tiempo, esta sopa desprende un olor rancio y agrio.» | ES | ✅ [EG] (errata «negociación») |
| Potaje gourmet: «…pocos saben distinguir el sabor del amor. Come, come hasta saciarte.» | ES | ✅ [EG] (errata «ene el») |
| Túnica de cordón trenzado: «…une el juramento del vengador al rencor de las víctimas. Jamás debe deshacerse.» | ES | ✅ [EG] |
| Mapa: Llanura de las Tumbas: «…toda la zona está dañada por los horripilantes estragos de la guerra.» | ES | ✅ [EG] = [ES-wiki] |
| Andreas: «…se rebeló tras conocer la naturaleza reptiliana de su señor. Por ello, fue encarcelado en una tumba subterránea.» | ES | ✅ [EG] |
| Huw: «…fue encarcelado en una tumba subterránea. Messmer lloró la pérdida de un hermano de armas.» | ES | ✅ [EG] |
| Cenizas de soldado de Messmer: «…vil batallón penitenciario… enterrados fuera de la vista del Árbol Umbrío.» | ES | ✅ [EG] |
| Armadura/Casco de soldado y de Caballero Negro: «…pequeño consuelo para quienes se ven obligados a librar una guerra sin gracia ni honor.» | ES | ✅ [EG] |
| Casco de Caballero Negro: «…alma ennegrecida del portador tras una matanza sin fin.» | ES | ✅ [EG] (errata «oramentos») |
| Casco / Armadura de Caballero de Fuego | ES | ✅ [EG] (errata «jugar lealtad») |
| Capucha de Salza: «…se negó a quemar unas ruinas antiguas, incluso a pesar de jugarse la vida.» | ES | ✅ [EG] |
| Lluvia de fuego: «Salza siempre mantuvo su desdén al barbarismo, incluso a pesar de quemar más aldeas y calcinar más tierras que nadie.» | ES | ✅ [EG] |
| Caballera de Fuego Hilde: «…insistieron en preservar los especímenes…» | ES | ✅ [EG] |
| Espadón de Queelign / Ceniza de Queelign («empala al enemigo en fuego para alejar a la bella madre Márika de la impureza») | ES | ✅ [EG] |
| Grasa de fuego de Messmer / Chispa aromática / Botella de perfume ígneo | ES | ✅ [EG] |
| Runa de Márika: «Restos dorados de la Gracia concedida personalmente por la reina Márika a los héroes que se unieron a la cruzada por ella.» | ES | ✅ [EG] |
| Runa del Reino de las Sombras / Juramento dorado | ES | ✅ [EG] |
| Recuerdo del Jinete del Jabalí / de la Cab. de la Luna Gemela / Mapa: Altiplano Sombrío | ES | ✅ [EG] |
| Recuerdo de la santa del brote / Hoja enastada del Brote («iglesia en llamas») | ES | ✅ [EG] — **no dice quién la quemó** |
| Texto oficial: «Un reino purgado en una batalla olvidada. Y calcinado por la llama de Messmer.» | ES | ✅ [ES-wiki] (Bandai Namco ES) |
| Tráiler: «Una purga sin Gracia ni honor. La tiranía de la llama de Messmer.» | ES | ✅ [TR-ES] (subtítulo oficial del tráiler, no del juego) |
| Bendición de Márika: «Márika hizo varias de estas medicinas para Messmer. Pero nunca más.» | EN/JP | ✅ [EN-wiki] EN+JP; **español NO VERIFICADO** ([EG] da otro texto) → PARAFRASEAR |
| Anciana: «Our lands were by thy kind set aflame… Thou cam'st, robbing us of all…» / «Take vengeance upon Messmer and his lot…» | EN | ✅ [EN-wiki] + [YT]; **PARAFRASEAR** |
| Cornamentado: «Messmer, foe of my beloved people. In vengeance for the flames, my blade I wield.» / «…dared to call us savages…» / «O mother, O most cherished wife and child.» | EN | ✅ [EN-wiki] + [WH]/[YT]; **PARAFRASEAR** |
| Leda: «Queen Marika commanded Sir Messmer to purge the tower folk. A cleansing by fire… They were never saints.» | EN | ✅ [EN-wiki] + [YT] (pantalla del longplay 5:42:00); **PARAFRASEAR** |
| Queelign: «Queen Marika, behold! I have excised another. Another cancer to thy joy.» | EN | ✅ [EN-wiki] + [YT]; **PARAFRASEAR** |
| Almas estancadas: «Put to the torch...by Messmer...and his lot. What did we do to deserve such a fate?» / «How long must this holy war stretch on?» | EN | ✅ [EN-wiki]; **PARAFRASEAR**; segundo en video NO VERIFICADO |
| Resto de diálogos en español (Leda, Cornamentado, Anciana, Queelign, almas, Espíritu vigilante) | ES | **NO VERIFICADO** (el juego no tiene doblaje al español; los subtítulos no están transcritos en ninguna fuente que encontrara) |

---

## 4. Lugares para MAPAS (x,y en `mapas/sombras_rejilla.jpg`, rejilla 0-1)

Mapa: `mapas/sombras.jpg` = **File:ER SotE Full Map v.1.10.jpg** (Fandom EN, 9472×11530, sin marcadores; fuente en `mapas/_fuentes.txt`). **Calibración ✅**: el mapa interactivo de la wiki «Map:Enemy Location - Furnace Golem» usa **este mismo archivo** (mapBounds 9472×11530, origen abajo-izquierda) → x = X/9472, y = 1 − Y/11530. Los puntos marcados «gólem» salen de ahí (exactos); el resto, medidos a ojo sobre recortes con rejilla de 0,02 e identificados **por forma** (las fortalezas vienen dibujadas en el arte del mapa).

| Lugar | x, y (rejilla) | Ligado a | Fiabilidad |
|---|---|---|---|
| **Fortaleza sombría** (fortaleza oscura con foso) | **0,49 , 0,43** (caja x 0,46–0,535 · y 0,40–0,46) | C4, C5, n.º 1 | ✅ por forma + Mapa: Altiplano Sombrío («en su centro») y gólem de Unte justo al sureste |
| Almacén de especímenes | dentro de la Fortaleza sombría (mismo punto) | C5 | ⚠ es parte de la fortaleza |
| **Ruinas calcinadas** (almas «quemados por Messmer») | **0,390 , 0,693** | C3 | ✅ gólem («tejados del edificio NE, donde está la Hoja de la piedad») |
| **Llanura de las Tumbas** (rótulo de región) | 0,40 , 0,68 (gólem de la llanura: 0,385 , 0,661) | C3 | ✅ gólem / ⚠ región |
| Lugar de gracia de entrada «Llanura de las Tumbas» / cruz de Miquella de entrada | ≈ 0,37 , 0,72 | Gancho | ⚠ **NO MEDIDO con precisión**: solo sé que las Ruinas calcinadas están «al noreste» de esa gracia ([EN-wiki] Scorched Ruins) |
| **Belurat, asentamiento de la torre** (ciudad amurallada con cúpulas) | **0,245 , 0,60** (caja x 0,21–0,28 · y 0,58–0,63) | C2, C3 | ⚠ por forma + Mapa: Llanura de las Tumbas («la torre espiral… al noroeste») |
| **Torre de los cornamentados / Enir-Ilim** (anillo oscuro con espinas encima de Belurat) | **0,225 , 0,555** | C2 | ⚠ por forma (Enir-Ilim está en la cima de esa torre; en el mapa es un círculo, no se ve la altura) |
| **Antiguas ruinas de Rauh** (zona verde dividida por un abismo) | **0,283 , 0,490** (zona x 0,20–0,38 · y 0,40–0,55) | C5 | ✅ gólem («Rauh Ancient Ruins») + Mapa: Ruinas de Rauh |
| **Castillo de Ensis** (castillo sobre agua entre la Llanura y el Altiplano) | **0,425 , 0,565** (caja x 0,40–0,45 · y 0,55–0,585) | C8 (Rellana) | ⚠ por forma |
| Altiplano Sombrío (gólem) | 0,454 , 0,487 | C8 | ✅ gólem / ⚠ región |
| Ruinas de Unte (gólem en la entrada) | 0,544 , 0,463 | C10 | ✅ gólem |
| Río de los ermitaños, tramo alto (gólem) | 0,527 , 0,477 | C9 (Aldea de las moscas, aguas abajo) | ✅ gólem |
| **Aldea de las moscas** | **NO VERIFICADO** (está «aguas abajo» del Río de los ermitaños, [EN-wiki]; no la identifiqué en el mapa) | C9 | ❌ |
| Fortaleza sombría, distrito de la iglesia (iglesia en cruz dentro de un lago) | ≈ 0,585 , 0,515 (gólem «Church District Highroad»: 0,634 , 0,512) | C10 | ⚠ por forma; gólem ✅ |
| **Árbol Umbrío** (dibujo del mapa, arriba) | tronco **0,545 , 0,17** · pie 0,555 , 0,24 | §1 | ✅ (es el dibujo) |
| Aldea ósea (gesto «Oh, Madre») / Fuerte de la reprimenda (Runa de Márika, soldados penitenciarios) / Fuerte Grieta Neblinosa (Mayal) / Iglesia de la Cruzada (Queelign) / Catacumbas de Grieta Neblinosa (Andreas) / Catacumbas del río Escorpión (Huw) | **NO MEDIDOS** | C1, C4, C6 | ❌ (solo sé su región: Altiplano Sombrío / Llanura) |
| Aldea con tejados rojos al este del Castillo de Ensis | 0,50 , 0,555 | — | ❌ identidad NO VERIFICADA (¿Aldea ósea? ¿Ciudad de posibilidades?) |
| «Fuerte Gael» | No existe en el DLC (juego base, Caelid) | — | — |
| Fuera del Reino: **mundo.jpg / mundo_rejilla.jpg** (copiados del video de Rykard) | Palacio de Mohg (entrada al DLC) — medir en `mundo_rejilla.jpg` si hace falta | Gancho | — |

---

## 5. ESCENAS IMPORTANTES y clips (solo ids y segundos; nada de video descargado)

Canales evitados: Fextralife, Lance McDonald, IGN, ConCon, PowerPyx, FP Good Game, Erudur, Gamerpillar, **Shirrako** (zHWvIF6_rl8 salió en las búsquedas: no usar), VaatiVidya, Zullie, Mage Infa, cad5150 (AodjN3dQyBk). **[CAP]** = capítulo; **[YT]** = subtítulos automáticos; **[WH]** = Whisper; **[FR]** = cuadro bajado y mirado.

**Fuente principal: SourceSpy91, longplay 4K 60 fps sin comentarios `-7P1VNhon6E` (23:34:56, «Shadow Of The Erdtree | 4K 60FPS | Full Game - 100% Walkthrough - No Commentary Longplay»)**. Comprobado con cuadros: **sin marca de agua**, HUD del juego visible en combate (barra y brújula), **subtítulos del juego en inglés activados** en diálogos y cinemáticas. Capítulos [CAP] útiles: Gravesite Plain 0:00:00 · Belurat Gaol 1:19:29 · Belurat, Tower Settlement **2:29:09** · Divine Beast Dancing Lion **3:36:40** · Castle Ensis 5:03:42 · Rellana 5:35:40 · Scadu Altus **5:41:07** · Fort Of Reprimand 7:23:56 · Bonny Village 8:02:53 · Bonny Gaol 8:12:23 · Rauh Base 9:12:19 · Fog Rift Catacombs 9:35:59 · Scorpion River Catacombs 10:39:45 · Shadow Keep (Church District) 11:36:29 · Shadow Keep Storehouse 12:19:32 · Commander Gaius 15:51:03 · Hinterlands 16:00:11 · Shadow Keep **17:18:37** · Golden Hippopotamus 17:20:32 · **Helping Hornsent 17:42:31** · Recluse River 17:48:41 · Shadow Keep 19:52:09 · **Messmer The Impaler 20:47:37** · Ancient Ruins Of Rauh 20:55:28 · Romina 22:27:24 · Enir Ilim 22:30:15 · Leda's Tag Team 23:16:38 · Radahn 23:23:19.

| Escena | Video (id · canal · duración) | Momento |
|---|---|---|
| **Presentación de Messmer (cinemática)** | **-7P1VNhon6E** · SourceSpy91 | ≈ **20:47:45–20:49:25** [FR] (ver [WH-L1] abajo); subtítulos del juego en inglés en pantalla |
| Misma cinemática, video corto | l7tuXNGLnuo · pgp · 97 s | **Tiene logo «pgp» y subtítulos quemados** [FR]: solo para referencia. [WH]: «Mongrel intruder» 0:15–0:18 · «Mother, wouldst thou truly Lordship sanction in one so bereft of light?» 0:27–0:40 · «Yet, my purpose standeth unchanged» 0:46–0:53 · «Those stripped of the Grace of Gold shall all meet death» 0:56–1:03 · «In the embrace of Messmer's flame» 1:08–1:13 |
| **2.ª fase (arranca el sello y sale la serpiente)** | -7P1VNhon6E · SourceSpy91 | [FR] **20:50:00** Messmer con serpientes y lanza (limpio) · **20:50:10** se cubre el rostro (limpio) · 20:50:20 «O mother, forgive me» (subtítulo) · **20:51:00** mano roja (limpio). Ver [WH-L1] |
| 2.ª fase, video corto | io3iYNzgz7k · pgp · 133 s | Logo pgp [FR]. [WH]: «I will not suffer» 0:10–0:13 · «A lord devoid of light» 0:16–0:18 · «O mother, forgive me» 0:27–0:34 · «Soon, Tarnished» 1:28–1:31 · «Wilt thou be taken in the jaws of the abyssal serpent, shorn of light» 1:37–1:50 |
| Combate completo 4K sin comentarios (alternativas) | jlNOo6j6enY · burgerarcade · 485 s · c0xHgQqPG20 · KMB GAMING · 446 s | Segundos **NO VERIFICADOS**; marca de agua **NO comprobada** |
| **Muerte de Messmer + el Cornamentado tras la pelea** | -7P1VNhon6E · SourceSpy91 | [FR] 20:54:00 Cornamentado: «Twas sublime—a very tangle of snakes!» · 20:54:30 «Now comes the piper to collect from Marika, her offspring…» · 20:54:50 «Then I wish not to be by him redeemed.» (subtítulos en pantalla). Ver [WH-L1] para «Mother... Marika...» |
| **El Cornamentado contra Messmer** («Messmer, foe of my beloved people…») | **6m4rlHbjecA** · Stratek · 26 s | [WH] 0:00–0:08 · «My clan's suffering… your ugliness» 0:08–0:21 |
| Cornamentado: todas sus líneas | INoq5UMCr-o · Stratek · 390 s | [YT] «The impaler, Messmer, must pay his due» 2:53–3:01 · «Messmer, foe of my beloved people» 4:14–4:29 · «dared call us savages» 4:43–4:56 · «O mother, O most cherished wife and child» **5:54–6:02** |
| Cornamentado tras matar a Messmer (alternativa) | Sfo5u4vWJ-4 · Lorebringer · 72 s | [YT] 0:06–0:27 «…did you see Messmer's face… dared call us savages…» · 0:31–1:06 «…the death of Messmer was merely the start…» |
| **Anciana cornamentada** | **p3JX1YVDYc0** · Stratek · 767 s (compilación) | [YT] «another of Messmer's peons» 0:19 · **«Our lands were by thy kind set aflame…» 0:34–0:52** · «Messmer's peon come to plague me» 1:42 · «A curse upon thee… strumpet's progeny» 2:22–2:39 · canto «Cleanse away the strumpet's vile progeny» 3:19, 3:56 · «Take vengeance upon Messmer and his lot» 5:13 · «Messmer and his sordid lot are elsewhere» 8:11 · «A sacrifice thou'dst make of me» 8:48 |
| Anciana (en el longplay, con imagen buena) | -7P1VNhon6E · SourceSpy91 | [FR] **3:36:44** «As evinced by thy gracious arrival.» · **3:37:02** «Have my son accompany thee to war.» · **3:37:12** «Take vengeance upon Messmer and his lot.» (subtítulos en pantalla). Ver [WH-L2] |
| Canto de la Anciana + baile del León (cinemática) | EWx5ndStb1I · Smoothy · 58 s | [YT] 0:26–0:54 «O Horn-deck'd beast… cleanse away the strumpet's vile progeny». Marca de agua NO comprobada |
| **Bestia divina León Danzante** (Belurat) | -7P1VNhon6E | [CAP] 3:36:40 (el capítulo empieza ya con la Anciana: la pelea está **antes**; segundo exacto **NO VERIFICADO**) |
| **Belurat** (asentamiento arrasado) | -7P1VNhon6E | [CAP] 2:29:09–3:36:40 · [FR] **2:34:00** plaza con fuente (limpio, solo brújula) · 2:29:40 relieves · 2:36:00 túnel · 2:38:00 calles |
| **Queelign** (invade en Belurat; «I have excised another…») | **3wQCfgdGfec** · Stratek · 123 s | [YT] **0:03–0:11** «Queen Marika, behold! I have excised another. Another cancer to thy joy.» · 0:25–0:28 «…in the embrace of Messmer's flame» · 0:41 «Queen Marika, mother to us all…» |
| Queelign en el longplay | -7P1VNhon6E | [FR] 5:48:00 cae: «Queen Marika, my grace...» y suelta la Ceniza de Guerra (Iglesia de la Cruzada) |
| **Leda: «Marika commanded Sir Messmer to purge the tower folk»** | -7P1VNhon6E | [FR] **5:42:00** «Wondering about the hornsent, are you?» → la línea sigue. Ver [WH-L3] |
| **Tráiler oficial (fuego de Messmer quemando, cruzada)** | **6uT8wGtB3yQ** · BANDAI NAMCO Europe · 195 s (subtítulos ES oficiales) | Leda: 0:48–0:52 «guerra secreta» · 0:59–1:02 · **1:06–1:10 «Una purga sin Gracia ni honor»** · **1:13–1:16 «La tiranía de la llama de Messmer»**. Imágenes [FR]: 0:56 jaulas ardiendo · 1:04 soldados con lanzas y una criatura atravesada · 1:08–1:12 Messmer con la lanza entre llamas · 1:15 incendio · 1:19 Messmer de cerca. Formato panorámico con franjas negras |
| Tráiler EE. UU. (igual) | J9Bm5U-MJZw · Bandai Namco America · 194 s | Solo subtítulos EN |
| **Fortaleza sombría por fuera** | -7P1VNhon6E | [FR] **17:18:20** (limpio, solo brújula) · 17:18:30 llanura del Altiplano |
| **Almacén de especímenes** | -7P1VNhon6E | [CAP] 12:19:32 · [FR] **20:00:00** rótulo «Specimen Storehouse» con la gran figura cornuda · **20:00:06** interior (limpio) |
| Caballeros de Fuego en la fortaleza | -7P1VNhon6E | [FR] 12:20:00 caballero de rojo con fuego (con HUD) |
| Antiguas ruinas de Rauh | -7P1VNhon6E | [CAP] 20:55:28 · [FR] 20:56:00 |
| Llanura de las Tumbas / Ruinas calcinadas (almas «quemados por Messmer») | -7P1VNhon6E | [CAP] 0:00:00–0:25:15; Ruinas calcinadas: segundo **NO VERIFICADO** |
| Andreas (Catacumbas de Grieta Neblinosa) / Huw (Catacumbas del río Escorpión) | -7P1VNhon6E | [CAP] 9:35:59 / 10:39:45 (segundo del ataúd/altar **NO VERIFICADO**) |
| Fuerte de la reprimenda (Runa de Márika, Bendición de Márika, cenizas de soldados) | -7P1VNhon6E | [CAP] 7:23:56 (segundo **NO VERIFICADO**) |
| Gesto «Oh, Madre» ante la estatua de Márika / Tierra interior | -7P1VNhon6E | [CAP] Hinterlands 16:00:11 (el gesto, justo antes: **NO VERIFICADO**) |
| **Cuerpos empalados en el juego** | — | **NO ENCONTRADO** hoy un segundo con empalados in-game; lo único verificado es el tráiler (1:04). Buscar en el longplay en el campamento ante la Fortaleza (17:18:37) o el Fuerte de la reprimenda |
| **Cornamentados presos** | — | ❌ No existe como tal (las prisiones son de los cornamentados, C9). Para jarras: Belurat Gaol [CAP] 1:19:29 |
| Messmer «voz sola» (para cortar sonidos) | **qSRYSmEx0z0** · Sin · 129 s · «Messmer the Impaler - Boss Voice Only» | ver tabla de SONIDOS |

**Tramos del longplay medidos con Whisper** (audio de `-7P1VNhon6E` cortado con `--download-sections`, borrado después). **Ojo: el corte empieza en un fotograma clave y Whisper sale ~5-6 s TARDE** respecto a los cuadros (comprobado: el subtítulo «Wondering about the hornsent» está en pantalla en 5:42:00 y Whisper lo pone en 5:42:01–09; «Twas sublime» en pantalla 20:54:00, Whisper 20:54:05; «Take vengeance upon Messmer» en pantalla 3:37:12, Whisper 3:37:18). Abajo ya van **corregidos restando 5 s** (±3 s):
- **[WH-L2] Anciana (3:35:30–3:40:00):** «As I felt the sacred beast's essence fade…» **3:36:22** · «…our voices have at last reached the heavens, as evinced by thy gracious arrival» 3:36:40–3:36:52 · «I implore, vessel of the sacred beast… Have my son accompany thee to war» **3:36:55–3:37:08** · «and dance thy dance of beauteous choler» 3:37:08–3:37:13 · **«Take vengeance upon Messmer and his lot. They who betrayed us, aye, they who burned us… Let them face in thy wrath their just deserts.» 3:37:13–3:37:27** · «My song will I sing… in service to thee» 3:37:27–3:37:32.
- **[WH-L3] Leda (5:41:00–5:45:30):** «Did you meet my compatriots?… Were it not for the charm Kindly Miquella put upon us…» 5:40:57–5:42:00 · «Wondering about the hornsent, are you? True enough. In any other circumstance, he'd be at our throats.» 5:42:00–5:42:10 · **«Long ago, Queen Marika commanded Sir Messmer to purge the tower folk. A cleansing by fire.» 5:42:10–5:42:17** · «It's no wonder the hornsent holds the Erdtree in contempt.» 5:42:17–5:42:21 · «…man is by nature a creature of conquest… They were never saints. They just happened to be on the losing side of a war, but it's still a wretched shame.» **5:42:21–5:42:35** · después habla el Cornamentado («You have a knack for timing… Miquella has said as much himself… sear clean the Erdtree's wanton sin») 5:42:35–5:44:01.
- **[WH-L1] Messmer (20:47:00–20:55:30):** con la música encima Whisper **no** sacó las líneas de la cinemática ni de la muerte (solo un fragmento: «…purpose standeth… stripped of the grace of gold…» hacia **20:48:43–20:49:20**). Lo comprobado con cuadros: cinemática de entrada ≈ **20:47:45–20:49:25** (pasillo 20:47:45, sala 20:48:30; a las 20:49:30 ya hay combate con barra «Messmer the Impaler») · cinemática de la 2.ª fase **20:50:00–20:51:00** (20:50:20 subtítulo «O mother, forgive me») · combate fase 2 20:52:00–20:53:00 · **el Cornamentado tras la muerte: «We meet again, I see, comrade-in-arms…» 20:53:55 · «…did you see Messmer's face?… a very tangle of snakes!… he dared call us savages, when he himself was most base of all» 20:54:00–20:54:13 · «…the death of Messmer was merely the start. Now comes the piper to collect from Marika, her offspring, and all the Erdtree's denizens. In vengeance for the flames, my blade I wield» 20:54:28–20:54:44**. **Segundo de «Mother... Marika... A curse upon thee» en el longplay: NO VERIFICADO** (entre 20:53:00 y 20:53:55; usar S5 de qSRYSmEx0z0).

### SONIDOS para que la voz los mande escuchar (cortar como sfx)

| # | Línea (EN) | Video | Inicio–fin | Comprobado |
|---|---|---|---|---|
| S1 | «Those stripped of the Grace of Gold shall all meet death. In the embrace of Messmer's flame.» | **qSRYSmEx0z0** (voz sola) | **29,3 s – 40,2 s** (0:29.3–0:40.2) | [WH] palabra a palabra (±0,3 s) |
| S1b | (repetición, la de cuando te mata en la fase 1; más seca) | qSRYSmEx0z0 | 43,3 s – 50,1 s | [WH] |
| S2 | «Mother, wouldst thou truly Lordship sanction, in one so bereft of light?» | qSRYSmEx0z0 | **10,7 s – 18,8 s** | [WH] |
| S3 | «I will not suffer... a lord devoid of light. O mother, forgive me.» | qSRYSmEx0z0 | **57,0 s – 76,8 s** (hay pausas largas: «I will not suffer» 57,0–59,4 · «a lord devoid of light» 62,6–65,2 · «O mother, forgive me» 69,5–76,8) | [WH] |
| S4 | «Soon, Tarnished. Wilt thou be taken in the jaws of the abyssal serpent, shorn of light.» | qSRYSmEx0z0 | **90,4 s – 106,3 s** | [WH] |
| S5 | **«Mother... Marika... A curse upon thee.»** | qSRYSmEx0z0 | **116,8 s – 124,0 s** (va pegado a «O lightless creature, embrace thine oblivion, as shall I» 108,9–116,0: cortar en 116,5) | [WH] |
| S6 | Cornamentado: «Messmer, foe of my beloved people. In vengeance for the flames, my blade I wield.» | **6m4rlHbjecA** | **0,0 s – 7,6 s** | [WH] |
| S7 | Cornamentado: «My clan's suffering. Their pain. All that they felt. Do you understand now? Your ugliness.» | 6m4rlHbjecA | **11,9 s – 21,0 s** | [WH] |

«Voz sola» = la pista del canal «Sin» no tiene imagen útil (solo sirve el audio). **Comprobar en la mezcla FINAL con Whisper** (regla de oro 10). Si se prefiere la versión con música de la cinemática: S1 en l7tuXNGLnuo 0:56,5–1:13,1.

### Capturas en `pantallas/` (1920×1080)

| Archivo | Sale de | Notas |
|---|---|---|
| `messmer_cinematica_serpientes_lanza.jpg` | -7P1VNhon6E 20:50:00 | Limpia (cinemática de la 2.ª fase, sin texto) |
| `messmer_fase2_cubre_rostro.jpg` | -7P1VNhon6E 20:50:10 | Limpia |
| `messmer_fase2_mano.jpg` | -7P1VNhon6E 20:51:00 | Limpia (mano roja en la arena) |
| `fortaleza_sombria_exterior.jpg` | -7P1VNhon6E 17:18:20 | Solo la brújula del juego arriba |
| `belurat_plaza_fuente.jpg` | -7P1VNhon6E 2:34:00 | Solo la brújula del juego |
| `almacen_especimenes_interior.jpg` | -7P1VNhon6E 20:00:06 | Solo la brújula |
| `anciana_cornamentada_almacen_CONSUBTITULO.jpg` | -7P1VNhon6E 3:37:02 | **Lleva subtítulo del juego** («Have my son accompany thee to war.»): recortar la franja baja o buscar un cuadro entre frases |
| `trailer_jaulas_ardiendo.jpg` | 6uT8wGtB3yQ 0:56 | Tráiler oficial, franjas negras |
| `trailer_criatura_atravesada_lanzas.jpg` | 6uT8wGtB3yQ 1:04 | Tráiler oficial; identidad de la criatura NO VERIFICADA |
| `trailer_messmer_lanza_llamas.jpg` | 6uT8wGtB3yQ 1:08 | Tráiler oficial |

**Escenas que hay que mostrar y no son cinemática** (clip o icono): Insignia de cruzada (icono + el efecto «aumenta la potencia de ataque tras derrotar a un enemigo»); Tornado de bestia divina; Mayal de serpiente; Potaje de escorpión; Cabeza de bestia divina; cenizas de Andreas y Huw; Bendición de Márika; Runa de Márika; Capucha de Salza / Lluvia de fuego; la Anciana en su almacén; el Cornamentado en la Cruz de Altasenda.

---

## 6. PUESTOS PROPUESTOS (del 5 al 1)

Lógica de escala: **sus propios hombres** (5) → **el saber de otros** (4) → **los dioses de otros** (3) → **una familia concreta** (2) → **tú** (1). Duración orientativa: gancho 1:30 · cinco puestos de 4:00–4:30 · suscripción ≈ 0:10 antes del n.º 1 · cierre 1:00 ≈ 25 min.

**Gancho propuesto:** que se OIGA S1 («Those stripped of the Grace of Gold…») y luego la voz en español: «Quienes se ven despojados del don del oro deberán hacer frente a la muerte... En el abrazo de la llama de Messmer.» → «Casi todo el mundo cree que lo peor de Messmer es que quemó a los cornamentados. Lo peor es que **tú** también estabas en esa frase.» + el texto oficial «Un reino purgado en una batalla olvidada. Y calcinado por la llama de Messmer.» + una línea: «en el video de Melina dijimos que haríamos este; aquí está» (ver §2, lo ya contado).

### N.º 5 — «Presos, presidiarios y una matanza sin fin» (C4)
**Gancho:** «Antes de quemar a nadie, Messmer ya se había quemado a los suyos.»
1. Los Caballeros de Fuego: hijos de la alta sociedad del Árbol Áureo, «marginados, perseguidos y expulsados de sus hogares» por jurarle lealtad (Casco de Caballero de Fuego). «Solo ellos llegaron a conocer de verdad a Messmer» (Armadura).
2. Andreas y Huw: se rebelaron «tras conocer la naturaleza reptiliana de su señor» y acabaron «encarcelados en una tumba subterránea»; «Messmer lloró la pérdida de un hermano de armas». Sus cenizas las invocaste tú.
3. La tropa: «vil batallón penitenciario… enterrados fuera de la vista del Árbol Umbrío»; «un pequeño consuelo para quienes se ven obligados a librar una guerra sin gracia ni honor»; el casco que apesta a «alma ennegrecida… tras una matanza sin fin». Un alma pregunta a Márika «¿cuánto más va a durar esta guerra santa?» (parafrasear).
**Remate:** y a esos mismos les pidieron que quemaran una biblioteca… → n.º 4.
**Clips:** longplay 9:35:59 (Grieta Neblinosa), 10:39:45 (río Escorpión), 7:23:56 (Fuerte de la reprimenda), 12:20:00 (Caballeros de Fuego).

### N.º 4 — «Quemar la biblioteca» (C5)
**Gancho:** «El sabio de sus caballeros odiaba la barbarie. Y quemó más aldeas que nadie.»
1. Lluvia de fuego: «Salza siempre mantuvo su desdén al barbarismo, incluso a pesar de quemar más aldeas y calcinar más tierras que nadie.»
2. Capucha de Salza: «se negó a quemar unas ruinas antiguas, incluso a pesar de jugarse la vida». Hilde: «insistieron en preservar los especímenes»; sus cenizas, «amuleto para proteger el almacén».
3. Lo que hay en ese almacén (captura `almacen_especimenes_interior.jpg`) y Rauh, «divididas en dos por un abismo». La iglesia de Romina «se quemó» (el juego **no** dice quién: preguntarlo).
**Advertencia:** ningún texto dice «Messmer mandó quemar Rauh»; decir «hubo que jugarse la vida para que no ardiera».
**Clips:** 12:19:32 y 20:00:06 (almacén), 20:55:28 (Rauh), 22:27:24 (Romina).

### N.º 3 — «Los dioses colgados de sus lanzas» (C2)
**Gancho:** «¿Sabes de dónde le viene el apodo? De lo que hizo con los dioses de otros.»
1. Tornado de bestia divina: «destripadas y colgadas en las lanzas de Messmer, antes de ser calcinadas en sus llamas… una pira funeraria para la propia torre». En japonés, la misma palabra de su título: **empalar**.
2. Recuerdo del León Danzante: al asaltar la torre «el ritual de la danza del león tomó tintes marciales». La bestia que matas en Belurat **es la plegaria de una anciana** contra los hijos de Márika (canto, parafrasear).
3. Y su máscara, cuando se la quitas: «Ya no responde a las sinceras plegarias de la anciana.»
**Clips:** tráiler 6uT8wGtB3yQ 1:04 (criatura atravesada) y 1:08–1:15; EWx5ndStb1I 0:26–0:54 (canto); longplay 3:36:40 (León).

### N.º 2 — «La sopa fría de la abuela» (C3)
**Gancho:** «De todo el genocidio, el juego solo te deja hablar con una víctima. Y te hace sopa.»
1. La Anciana encerrada en Belurat: te toma por «otro peón de Messmer»; «nuestras tierras fueron incendiadas por los tuyos… viniste a robarlo todo» (parafrasear; que se oiga en inglés si hace falta: p3JX1YVDYc0 0:34–0:52).
2. Potaje de escorpión: «Antaño la preparaban con mimo las abuelas de la familia. Al haberse enfriado hace tiempo, esta sopa desprende un olor rancio y agrio.» Gourmet: «pocos saben distinguir el sabor del amor».
3. Su hijo, el Cornamentado (que en el video de Miquella llamamos mal «Cornudo»): «Messmer, enemigo de mi amado pueblo» (S6); «se atrevió a llamarnos salvajes» (JP: «inmundicia»); y si no se venga, «oh madre, oh amada esposa e hijo». El alma de las Ruinas calcinadas: «quemados… por Messmer y los suyos. ¿Qué hicimos para merecer esto? Vivíamos en paz» (parafrasear). Mayal: «para quemar a los cornamentados y marcarlos con agonía y miedo».
**Matiz (C9) en una frase:** Leda: «nunca fueron santos» (y metían gente en jarras); «solo estaban en el bando perdedor».
**Clips:** longplay 3:36:44–3:37:12 (Anciana con imagen); 6m4rlHbjecA (S6/S7); INoq5UMCr-o 5:54–6:02; longplay 20:54:00.

### N.º 1 — «La medalla que llevaste colgada» (C1) — la que ignoraste
**Giro:** «Las otras cuatro las hizo él. Esta la llevaste tú.»
1. Insignia de cruzada, la que te suelta Queelign en Belurat: «Aumenta la potencia de ataque tras derrotar a un enemigo. Los cruzados olvidaron el honor y la piedad para empalar y quemar sin misericordia a quienes consideraban impuros. Quienes se sentían estimulados por los gritos de muerte eran los mismos que abogaban por la santidad de la campaña.» **El efecto es la frase**: más fuerte cada vez que matas.
2. Quién te la da: Queelign, que al matarte celebra «¡Reina Márika, mira! He extirpado otro cáncer de tu alegría» (parafrasear) y que quería «ser un segundo empalador» (Espadón). Su ceniza «empala al enemigo en fuego para alejar a la bella madre Márika de la impureza».
3. Y el impuro eras tú: Messmer al verte, «Eres un Sinluz… alguien tan despojado de luz» → «Quienes se ven despojados del don del oro deberán hacer frente a la muerte». La cruzada no era contra un pueblo: era contra todo el que no tuviera la gracia. Tú eres la definición. (Que se OIGA S2 y S1.)
4. Cierre del puesto: por deseo de su madre se hizo «un símbolo aterrador»; «Centra en mí, y solo en mí, tus maldiciones…» (Armadura). Y la Runa de Márika que rompiste por 80 000 runas: «la Gracia concedida personalmente por la reina Márika a los héroes que se unieron a la cruzada por ella».
**Clips:** 3wQCfgdGfec 0:03–0:11 (Queelign); longplay 5:48:00 (Queelign cae) y cinemática [WH-L1]; qSRYSmEx0z0 S1/S2.

**Cierre propuesto (C6):** la Bendición de Márika: «Márika hizo varias de estas medicinas para Messmer. Y nunca más» (parafrasear EN/JP; el texto de [EG] dice otra cosa) → la bebiste tú. Que se OIGA S5: «Mother... Marika... A curse upon thee» = «Madre... Márika... Una maldición... caerá sobre ti...».

**Reservas / cameos:** Gesto «Oh, Madre» ante la estatua de Márika (abre su aldea natal) · Cenizas de espíritu venerado («cadáveres de cornamentados») · Juramento dorado · Escudo con blasón de serpiente · Gaius y Rellana · Marca ulcerada de Márika (solo como pregunta, C12).

---

## 7. Datos falsos comunes que NO hay que decir

1. **«Messmer tiene Gran Runa / Miquella rompió la Gran Runa de Messmer.»** — Es la **Gran Runa de Miquella**; Messmer suelta Recuerdo y Yesca.
2. **«Las prisiones (Gaols) eran las cárceles de Messmer para los cornamentados.»** — Son de los cornamentados (jarras, «Not the jar…»).
3. **«Messmer quemó la Aldea de las moscas.»** — Es la enfermedad de las moscas.
4. **«Messmer ordenó quemar Rauh y el almacén.»** — Ningún texto lo dice así (C5).
5. **«Messmer quemó la iglesia de Romina.»** — El texto dice que la iglesia se quemó; no quién.
6. **«El Cornudo.»** — Es **el Cornamentado** (el video de Miquella lo dijo mal).
7. **«Tierra de las Sombras.»** — **Reino de las Sombras** en los objetos («la Tierra Sombría» solo en marketing).
8. **«Messmer es hijo de Radagon.»** — Interpretación de la wiki.
9. **«La Marca ulcerada de Márika es el ojo de Messmer.»** — Teoría; el juego no lo dice.
10. **«Messmer luchó contra los gigantes.»** — Godfrey (ya corregido en el video de Rykard).
11. **«La familia del Cornamentado murió en la cruzada»** como hecho — se deduce, no se dice.
12. **«La Bendición de Márika fue la única que hizo»** — Así lo transcribe [EG], pero EN y JP dicen «varias… y nunca más». Usar la versión EN/JP parafraseada.
13. **«Fuerte Gael»** en el Reino de las Sombras — es de Caelid.
14. **«Los cornamentados eran víctimas inocentes»** — Leda: «nunca fueron santos». Dar el matiz en una frase.
15. **Citas en español de Leda, la Anciana, el Cornamentado o Queelign con comillas** — NO VERIFICADO: parafrasear. Las únicas líneas habladas verificadas en español son **las de Messmer** ([ES-wiki]) y **las del tráiler** ([TR-ES]).
16. **Pronunciación**: el canal usa «Mésmer» (FONETICA en los guiones de Melina/Miquella/Radahn).

---

## 8. Pendientes para la sesión de guion

- Español de las líneas de Leda, Cornamentado, Anciana, Queelign, almas estancadas y del objeto Espíritu vigilante: **NO VERIFICADO** → parafrasear o transcribir de un clip con subtítulos del juego en español.
- **Bendición de Márika**: cotejar con captura el texto español real (EG contradice EN/JP).
- Cotejar con captura las descripciones de [EG] con erratas: Recuerdo del Empalador («los sutituyó»), Recuerdo del León Danzante («Emparador»), Potaje («negociación»), Casco de Caballero de Fuego («jugar lealtad»), Casco de Caballero Negro («oramentos»), Insignia («Caballeo»), Espadón de Queelign («Queeling»), Mapas (Llanura, Rauh, Altiplano).
- Nombres con fuentes que discrepan: Potaje/Estofado de escorpión; «serpiente primitiva/básica»; mensaje de la Gran Runa; «Cruz de tres sendas» ([ES-wiki]) / «Cruce de tres sendas» ([EG]).
- Medir en el mapa: Aldea de las moscas, Aldea ósea, Fuerte de la reprimenda, Fuerte Grieta Neblinosa, Iglesia de la Cruzada, gracia de entrada (**NO MEDIDOS**). Confirmar Belurat/Enir-Ilim/Castillo de Ensis (por forma).
- Segundos **NO VERIFICADOS**: pelea del León Danzante, Ruinas calcinadas (almas), Andreas/Huw, Fuerte de la reprimenda, gesto «Oh, Madre», cuerpos empalados in-game.
- Revisar marca de agua/rótulos de: Stratek, Lorebringer, Smoothy, Sin (solo audio), burgerarcade, KMB GAMING. **pgp tiene logo**: no usar su imagen. SourceSpy91 y el tráiler oficial: comprobados sin marca.
- **NO VERIFICADO**: a qué video se refería el guion de Melina («ya hicimos un video entero…»); identidad de la criatura del tráiler (1:04); que la estatua del gesto sea «Márika con Messmer bebé»; ubicación de las almas de soldados.
