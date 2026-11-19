# Dossier: «Las 5 peores atrocidades de Godfrey QUE IGNORASTE»

Canal Runa Caída. Investigación del 19-nov-2026. Todo lo de abajo sale de las fuentes enlazadas, leídas hoy por API o descarga directa. Lo que no pude comprobar va marcado **NO VERIFICADO**. Cuando una afirmación es interpretación de la wiki (no texto del juego), lo digo.

## 0. Fuentes y cómo leerlas

| Clave | Fuente | Para qué sirve |
|---|---|---|
| **[ES-wiki]** | Wiki en español de Fandom, `https://eldenring.fandom.com/es/wiki/<Página>` (leída por su API) | Nombres oficiales en español, descripciones `{{Descripción\|ES=…}}`, ecos de Márika en español, 1 línea de Godfrey en español. **Es una wiki pequeña**: no tiene páginas de la mitad de los objetos (Hacha de Godfrey, Corona…) |
| **[EN-wiki]** | Wiki inglesa de Fandom, `https://eldenring.fandom.com/wiki/<Page>` (API) | Descripciones en inglés y japonés (`EN_line`/`JP_line`), diálogos completos (`Godfrey, First Elden Lord/dialogue`), ubicaciones. **Ojo**: la parte «Background/Notes» mezcla texto del juego con interpretación; aquí solo cito como hecho lo que viene entre comillas de un objeto o diálogo |
| **[EG]** | Eliteguias, `https://www.eliteguias.com/guias/e/er/…` (descarga directa, responde bien) | Descripciones de objetos en español transcritas del juego. **Tiene erratas** (ver cada cita): «Tanaño», «aguruios», «sinque madie», «Mogh», «sseguir», «pro ello». Antes de rotular, cotejar con captura |
| **[FX]** | Fextralife, `https://eldenring.wiki.fextralife.com/Godfrey,+First+Elden+Lord` | Respondió (HTTP 200). Lo usé solo para **confirmar** las líneas clave del combate: «good service, Serosh.», «courtesy enough.», «befits a crown.» aparecen en la página |
| **[YT]** | Subtítulos automáticos (inglés) y capítulos de videos de YouTube, leídos con `yt-dlp` sin descargar video | Para fechar al segundo las escenas y confirmar el texto hablado de la intro |

### Nombres oficiales en español (verificados) — inglés → español

| Inglés | Español oficial | Fuente / nota |
|---|---|---|
| Godfrey, First Elden Lord | **Godfrey, primer Señor del Círculo** | [ES-wiki], [EG]. LatAm: «Godfrey, Primer Señor de Elden» ([ES-wiki]) |
| Hoarah Loux, Warrior | **Hoarah Loux, guerrero** | [ES-wiki] alias; [EG] jefazos-p109 (con errata «Hoarah Lux») |
| Lord of the Battlefield | **Señor de la Batalla** / «el señor de la Batalla» | [ES-wiki] alias; [EG] Corona de Señor del Círculo |
| Serosh, Lord of Beasts / Beast Regent | **Serosh, Señor de las Bestias** / **bestia regente Serosh** | [EG] Gran martillo de garras bestiales; [EG]/[ES-wiki] Icono de Godfrey |
| Badlands | **Tierra Baldía** (singular) | [EG] Cinta de campeón, Gran hacha, Carne excelsa; [ES-wiki]. **«Tierras Baldías» es incorrecto** |
| Long March | **Larga Marcha** («la Larga Marcha de los Sinluz») | [EG]/[ES-wiki] Recuerdo de Hoarah Loux |
| Tarnished | **Sinluz** | LatAm: **Tiznados** ([ES-wiki] Sinluz) |
| Omen | **Augurio(s)** | LatAm: **Aojos** ([ES-wiki] Augurio) |
| Golden Lineage | **linaje dorado** / Linaje Dorado | [EG] Hacha de Godfrey («linaje dorado»), [ES-wiki] («Linaje Dorado») |
| Elden Throne | **Trono de Elden** | [ES-wiki], [EG] gracia |
| Erdtree Sanctuary | **Santuario del Árbol Áureo** | [EG] gracia; [ES-wiki] |
| Leyndell, Royal Capital | **Leyndell, capital del Reino** | [ES-wiki], [EG] |
| Leyndell, Ashen Capital | **Leyndell, capital cinérea** (región) · el Lugar de Gracia se llama **«Leyndell, Capital de la Ceniza»** | [ES-wiki], [EG] gracia |
| Stormveil Castle | **Castillo de Velo Tormentoso** | LatAm: **Castillo Velobrumo** ([ES-wiki]) |
| Stormhill | **Colina Tormentosa** | [ES-wiki], [EG]. **«Colina de la Tormenta» es incorrecto** |
| Storm Lord | **señor de la Tormenta** | [EG] Corona de Señor del Círculo («Se enfrentó solo al señor de la Tormenta») |
| Castle Morne / Weeping Peninsula | **Castillo de Morne** / **Península del Llanto** | [ES-wiki], [EG] |
| Mountaintops of the Giants | **Picos de los gigantes** | [ES-wiki], [EG] |
| Forge of the Giants / Flame Peak | **Forja de los gigantes** / **Pico de la llama** | [ES-wiki] Gigante de fuego, [EG] gracia |
| Giant-Conquering Hero's Grave | **Tumba del héroe matagigantes** | [ES-wiki], [EG] |
| War against the Giants | **guerra contra los gigantes** | [EG] Corona; [ES-wiki] |
| Fire Giant | **Gigante de fuego** | [ES-wiki], [EG] |
| Subterranean Shunning-Grounds | **Subsuelo de los marginados** | [ES-wiki], [EG] |
| Lands Between | **Tierras Intermedias** | [EG]/[ES-wiki] |
| Elden Ring | **Círculo de Elden** | [ES-wiki] |
| First / Third Church of Marika | **Primera iglesia de Márika** / **Tercera iglesia de Márika** | [EG] gracia; [ES-wiki] Reina Márika |
| Church of Pilgrimage | **Iglesia de la peregrinación** ([EG]) / «Iglesia de peregrinación» ([ES-wiki]) | Las dos fuentes difieren en el artículo |
| Smoldering Church | **Iglesia en llamas** | [EG] gracia (Caelid noroeste) |
| Shadow Keep (DLC) | **Fortaleza sombría** | [EG] Shadow of the Erdtree |
| Remembrance of Hoarah Loux | **Recuerdo de Hoarah Loux** | [ES-wiki], [EG] |
| Axe of Godfrey / Regal Roar | **Hacha de Godfrey** / habilidad **Rugido majestuoso** | [EG] armas-p298 |
| Ash of War: Hoarah Loux's Earthshaker | **Ceniza de Guerra: Sacudida de Hoarah Loux** | [EG], [ES-wiki] |
| Elden Lord Crown / Armor | **Corona de Señor del Círculo** / **Armadura de Señor del Círculo** | [EG] |
| Godfrey Icon | **Icono de Godfrey** | [EG], [ES-wiki] |
| Talisman of Lord's Bestowal (DLC) | **Talismán de la dádiva del señor** | [EG] talismanes-p104 |
| Axe Talisman | **Talismán con hacha** | [EG] |
| Champion Headband | **Cinta de campeón** | [EG] |
| Beastclaw Greathammer | **Gran martillo de garras bestiales** | [EG] |
| Golden / Beast Crest Heater Shield | **Escudo dorado con blasón de bestia** / **Escudo apuntado con blasón de bestia** | [EG] |
| Tree-and-Beast Surcoat | **Sobretodo con árbol y bestia** | [EG] |
| Grafted Blade Greatsword | **Espadón de hoja injertada** | [EG] |
| Rusted Anchor | **Ancla oxidada** | [EG] |
| Regal Omen Bairn / Omen Bairn | **Párvulo maldito de la realeza** / **Párvulo maldito** | [EG] |
| Mohg's Shackle | **Grillete de Mohg** | [EG] |
| Troll's Golden Sword | **Espada dorada de trol** | [EG] |
| Talisman Pouch | **Bolsa para talismán** | [ES-wiki], [EG] |

> **Lo que NO existe con el nombre del encargo:** «Talismán del Señor del Círculo» (lo más cercano es el **Talismán de la dádiva del señor**, DLC) y «Hacha de Hoarah Loux» (el arma es el **Hacha de Godfrey**; lo de Hoarah Loux es la **Ceniza de Guerra: Sacudida de Hoarah Loux**). «Vestigio» tampoco: es **Recuerdo**.

---

## 1. Quién es Godfrey ✅ CONFIRMADO

**(a) Los dos nombres**
- **Hoarah Loux** es su nombre de guerrero de Tierra Baldía. **Recuerdo de Hoarah Loux** ([EG] objetos-p556, igual en [ES-wiki]): «Recuerdo del guerrero Hoarah Loux, tallado en el Árbol Áureo. […] Cuando Godfrey, primer Señor del Círculo, fue despojado de su Gracia y se transformó en un Sinluz, abandonó las Tierras Intermedias en compañía de los suyos. / Cuando la Larga Marcha de los Sinluz tocó a su fin, Godfrey renunció a la corona para ser de nuevo un simple guerrero.»
  - EN ([EN-wiki]): «…Godfrey divested himself of kingship, becoming a simple warrior once more.» — «de nuevo / once more»: ya había sido guerrero antes de ser rey.
- **Cinta de campeón** ([EG] armaduras-p11): «Cinta reservada para los más valientes de Tierra Baldía. Prueba de que el portador ha asesinado a innumerables enemigos. Siguiendo el ejemplo de su líder, Hoarah Loux, los valientes guerreros de Tierra Baldía evitan cualquier adorno adicional.»
- **Gran hacha** ([EG] armas-p31): «Reconocida como el arma predilecta de los líderes de Tierra Baldía.»
- **Carne excelsa** ([EG] objetos-p76): «Esta comida estimulante, que se consideraba un manjar en Tierra Baldía, estaba destinada exclusivamente para aquellos a los que consideraban héroes.»
- Su pueblo son los **guerreros de los altiplanos**. **Hacha de los altiplanos** ([EG] armas-p90): «Los combatientes valerosos comienzan la batalla gritando su nombre.» (Eso explica el «¡…Hoarah Loux! ¡Guerrero!»). Que Hoarah Loux sea «highlander» es deducción de [EN-wiki] (Notes), no texto del juego.

**(b) Señor del Círculo y Serosh**
- **Icono de Godfrey** ([EG] talismanes-p58 = [ES-wiki]): «Godfrey era un feroz guerrero. Cuando juró sus votos para convertirse en Señor, comenzó a llevar a la bestia regente Serosh a sus espaldas, con el fin de calmar el incesante deseo de batalla que ardía en su interior.» Se obtiene al derrotar a **Godefroy, el Injertado** (Meseta Altus, [EG] jefazos-p73).
  - EN: «…to suppress the ceaseless lust for battle that raged within.»
- **Gran martillo de garras bestiales** ([EG] armas-p52): «Dicen que las uñas negras que sobresalen de la piel dorada representan a Serosh, Señor de las Bestias, que se convertiría en regente del rey Godfrey.» (Lo da **Gurranq** a la 7.ª Raíz mortuoria.)
- **Escudo dorado con blasón de bestia**: la versión de [EG] (escudos-p10) **corta** la segunda frase; el inglés ([EN-wiki]) dice: «The beast depicted is Serosh, aged counselor who guides the golden lineage.» → español **NO VERIFICADO** («consejero» lo usa [ES-wiki] en su trasfondo, no como cita).
- **Escudo apuntado con blasón de bestia** ([EG] escudos-p24): «En su blasón presenta una bestia, la cual recuerda a los guerreros que no han de sucumbir a la agitación del combate. Lucha con pasión, pero no seas su prisionero.»
- **Sobretodo con árbol y bestia** ([EG] armaduras-p42): «El sobretodo detalla el lejano Árbol Áureo y la bestia regente, un emblema del linaje dorado. Ambos son símbolos de una gloria ya pasada.»
- **Armadura leonina de Radahn** ([EG] armaduras-p217): «Se dice que el león dorado simboliza a Godfrey, el primer Señor del Círculo, y a su bestia regente, Serosh. Desde su juventud, Radahn quedó naturalmente fascinado por el Señor de la Batalla.»
- **Hacha de Godfrey** ([EG] armas-p298; errata «Tanaño» = «Antaño»): «Arma de Godfrey, Señor del Círculo. Se rompió en el curso de la batalla que libró como líder de los Sinluz durante la Larga Marcha. Esta arma simboliza la promesa de Godfrey de actuar como un señor y, más adelante, se convirtió en el emblema del linaje dorado. [Antaño], la corona se afianzaba mediante la fuerza.» EN: «In the days of the past, a crown was warranted with strength.»
- **Casco de hacha del crisol** ([EG] armaduras-p354): «Casco de los caballeros del crisol que servían a Godfrey, primer Señor del Círculo. La decoración en forma de hacha es el emblema del guerrero Ordovis…»
- Primer Señor del Círculo: [ES-wiki] cita a Miyazaki (EDGE, 2021): «En el apogeo de la Orden Dorada […] había dos Señores del Círculo, y Godfrey fue el primero de ellos.» (Matiz: [EN-wiki] «Elden Lord» lista también a **Placidusax** como Señor anterior; no lo uses salvo como dato curioso.)
- Tras su destierro, Márika se casó con Radagon. **Miriel, pastor de los Juramentos** (inglés, [EN-wiki]; español NO VERIFICADO): «However, when Godfrey, first Elden Lord, was hounded from the Lands Between, Radagon left Rennala to return to the Erdtree Capital, becoming Queen Marika's second husband and King Consort.»

**(c) Hijos y descendencia**
- **Gran Runa de Godrick** ([EG] objetos-p201; errata «fueron del Señor»): «Los primeros semidioses fueron [el] Señor del Círculo Godfrey y sus descendientes, el linaje dorado.»
- **Gran Runa de Mohg** ([EG] objetos-p536): «Mohg y Morgott eran gemelos, por lo que sus grandes runas son similares. No obstante, la runa de Mohg está empapada en sangre maldita, desde su devoción por el condenado lodazal en el que nació hasta las profundidades de la tierra.»
- Que Godwyn, Morgott y Mohg sean hijos de Godfrey y Márika lo afirman [ES-wiki] (infobox «hijos») y [EN-wiki]; **una frase del juego que diga «Morgott, hijo de Godfrey» con esas palabras: NO VERIFICADO**. Lo más cercano es la escena: Godfrey llora a Morgott («It's been a long while, Morgott.»).
- Godrick: **Kenneth Haight** (EN, [EN-wiki]): «And to think, he's the blood of Godfrey! Last of the golden lineage, though you almost wouldn't know it to look at him.» **Gideon** (EN): «Despite being the blood of Godfrey, first Elden Lord, he's a grotesque old fool, grasping for power.» **Godrick**, si te mata en la fase 2 (EN): «Great Godfrey, didst thou witness?»
- **Nepheli Loux** comparte apellido; [ES-wiki]: «Se desconoce la naturaleza de su relación». → **NO decir que es su hija.**

**(d) Lo que añade Shadow of the Erdtree** (poco, pero sirve)
- **Talismán de la dádiva del señor** ([EG] talismanes-p104; [EN-wiki] lo marca como objeto de SotE): «Talismán que muestra a Godfrey, primer Señor del Círculo, mientras recibe la preciada savia. […] El Señor del Árbol Áureo aceptó la savia estoicamente, sin atisbo de vacilación. ¡No debe sorprender que proyecte una larga sombra sobre las tierras!» Ubicación: **Fortaleza sombría**, junto al árbol dorado (tercera visita según [EG]; [EN-wiki]: «beside the large golden tree»).
- Ropa de los altiplanos en el DLC: **Atuendo de los altiplanos** ([EG] armaduras-p543, en el **Altiplano Sombrío**): «Los guerreros de los altiplanos son famosos como cazadores de osos; para ellos, no hay acto más glorioso que subyugar a una bestia salvaje.» **Atuendo glorioso** ([EG] armaduras-p553, Base de Rauh): «Los patrones rojos solo se permitían a los que cazaban osos. A los más grandes y gloriosos.» → La lectura de [EN-wiki] («Lord Godfrey is draped in blue, while Hoarah Loux is soaked in red beast blood») es **interpretación de la wiki**: dila como observación del narrador, no como lore.
- Nada más del DLC sobre Godfrey en lo que revisé (búsqueda de «Godfrey / Hoarah Loux / Serosh» en [EN-wiki], 200 páginas). La teoría de que Serosh se unió a él en la **Puerta de la Divinidad** ([EN-wiki] Serosh, Notes) es **especulación** de la wiki.

**(e) URLs**
- https://eldenring.fandom.com/es/wiki/Godfrey,_primer_Señor_del_Círculo · …/Serosh · …/Recuerdo_de_Hoarah_Loux · …/Icono_de_Godfrey · …/Sinluz · …/Reina_Márika_la_Eterna
- https://eldenring.fandom.com/wiki/Godfrey,_First_Elden_Lord · …/Godfrey,_First_Elden_Lord/dialogue · …/Serosh · …/Talisman_of_Lord%27s_Bestowal · …/Godrick_the_Grafted/dialogue
- https://www.eliteguias.com/guias/e/er/elden-ring_objetos-p556.php · …armaduras-p11.php · …talismanes-p58.php · …armas-p298.php · …armas-p52.php · …talismanes-p104.php · …objetos-p201.php · …objetos-p536.php

---

## 2. CANDIDATAS (10), cada una con veredicto

### C1. Exterminio de los gigantes de fuego ✅ CONFIRMADO (material muy fuerte)
**Qué dicen las fuentes**
- **Corona / Armadura de Señor del Círculo** ([EG] armaduras-p477/478): «La era del Árbol Áureo empezó en mitad de un enfrentamiento, cuando Godfrey era el señor de la Batalla. Lideró la guerra contra los gigantes. Se enfrentó solo al señor de la Tormenta. Y al fin llegó el momento en el que cayó su último enemigo. Fue en ese instante, según dice la historia, cuando se desvaneció el color de los ojos del señor Godfrey.»
- **La orden de Márika**, eco en la **Primera iglesia de Márika** (Picos de los gigantes), español de [ES-wiki]: «Recordadlo, valientes guerreros. Recuérdalo, mi señor Godfrey. Elogiamos tus actos. / La guía te ha llevado a superar cada prueba hasta llegar al lugar donde estás. / **Acaba con los gigantes con tu espada y confina la llama en lo alto de la montaña.** / Permite que empiece una nueva era. Una era rebosante de vida. / Blande el Círculo de Elden, ¡por la era del Árbol Áureo!» EN ([EN-wiki] Melina/dialogue): «Put the Giants to the sword, and confine the flame atop the mount.»
- **Recuerdo del gigante de fuego** ([EG] objetos-p520): «El gigante de fuego es un superviviente de la guerra contra los gigantes. Al constatar que las llamas de su forja jamás podrían extinguirse, la Reina Márika lo maldijo. "Oh, insignificante gigante, deberás custodiar tu llama por toda la eternidad".» → **un superviviente**: los demás, no.
- **Aplastagigantes** ([EG] armas-p241): «Gran martillo fabricado a partir de un pedrusco y usado en la guerra contra los gigantes. […] Después de que los gigantes desaparecieran para dar paso a las guerras de los hombres, esta arma cayó en el olvido.»
- **Medallón de rugido** ([EG] talismanes-p5): «En la antigüedad, los gigantes eran enemigos mortales del Árbol Áureo. Sus bramidos desolaban la naturaleza, provocaban avalanchas y azuzaban tormentas de fuego.»
- **Escudo de rostro** ([EG] escudos-p43): «El espantoso rostro y las llamas ardientes tienen como objetivo recordar el horror que supone enfrentarse a un gigante de fuego. De cierta forma, este escudo tiene una función instructiva.»
- **Los troles que se cambiaron de bando.** Monumento de espada junto a la Tumba del héroe matagigantes (EN, [EN-wiki] Sword Monuments; español NO VERIFICADO): «The War against the Giants / Champions battle, trolls betray / Fire vanquished, the era of the Erdtree begins». **Espada dorada de trol** ([EG] armas-p201): «Espada entregada a los gigantes menores que lucharon por el Árbol Áureo durante la guerra contra los gigantes, hace ya mucho tiempo. Aunque hayan perdido la cordura, en ningún momento se separan de sus espadas, cuyo estado actual es lamentable al haberse desconchado su chapado en oro.» Que los troles desciendan de los gigantes: *Troll's Hammer* (EN, [EN-wiki]; nombre español NO VERIFICADO): «Trolls are descended from the giants».
- Aliados: **Armadura de Zamor** ([EG] armaduras-p411): caballeros «aclamados como héroes en la guerra contra los gigantes […] enemigos jurados de los gigantes de fuego».
- **Piedra de forja [8]** ([EG] objetos-p375; errata «Se cre»): «…se utilizaban para poner a punto las armas de los campeones de la guerra contra los gigantes en el momento del nacimiento del Árbol Áureo.»
- **Cadáveres empalados**: [EN-wiki] (War Against the Giants) dice que los gigantes fueron «massacred in the fields before their Forge, leaving the battlefield littered with their impaled corpses» y pone una captura («The corpses of the Fire Giants, impaled by thorny stakes»). **Es escenario, no texto**: mostrarlo con clip/captura de los Picos, sin decir quién los empaló (**NO VERIFICADO**).
- **Quién mató al dios caído**: [ES-wiki] dice «Márika se encargó de derrotar al dios caído personalmente»; [EN-wiki] lo apoya en el Escudo tuerto con «believed». **Ningún texto se lo atribuye a Godfrey.**

**Lo que ignoraste:** el genocidio tiene orden firmada (Márika) y ejecutor con corona (Godfrey). Al último gigante lo dejaron vivo **para que trabajara de vigilante eterno**, y a los troles traidores les pagaron con una espada chapada en oro que hoy se descascara en manos de gigantes que «han perdido la cordura».

**URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_armaduras-p477.php · …objetos-p520.php · …armas-p241.php · …armas-p201.php · …talismanes-p5.php · …escudos-p43.php · https://eldenring.fandom.com/es/wiki/Reina_Márika_la_Eterna · https://eldenring.fandom.com/wiki/War_Against_the_Giants · https://eldenring.fandom.com/wiki/Sword_Monuments

### C2. Conquistas: Velo Tormentoso y Morne («un país desaparecido») ✅ CONFIRMADO
- Señor de la Tormenta: «Se enfrentó solo al señor de la Tormenta» (Corona, arriba). Su identidad es desconocida ([EN-wiki] Storm Lord: «The identity of the Storm Lord is unknown»).
- ***The Stormhawk King*** (cenizas; EN, [EN-wiki]; nombre español **NO VERIFICADO**): «Ashes of a hawk revered by all others as sovereign back in the days when Stormveil's winds still raged like no other.» → la tormenta de Velo Tormentoso **ya no ruge**. Que eso lo causara Godfrey: **NO VERIFICADO** (relación sugerida por [EN-wiki]).
- En el castillo: retrato grande de Godfrey y Serosh en el salón principal (lo patrulla el **Vástago injertado**) y estatua de ambos en la sala del trono ([EN-wiki] Storm Lord / Godfrey, Notes; verificar con captura).
- **Monumento junto a la entrada del Castillo de Morne** ([ES-wiki], español): «El asedio al castillo de Morne: / Un héroe solitario lucha en busca de venganza, / solo para terminar en manos del señor Godfrey.»
- **Espadón de hoja injertada** ([EG] armas-p62; errata «sseguir», «atributs»): «La famosa espada del Castillo de Morne. Arma de vengador que carga con océanos de ira y arrepentimiento. […] Un solitario campeón, superviviente de un país desaparecido, mostró tal determinación a la hora de seguir luchando que reclamó las espadas de todo un clan de guerreros.» Habilidad: **Juramento de venganza** («Haz un juramento sobre el espadón para vengar al clan»). Hoy la tiene el **Bastardo leonino** (jefe de Morne).
- **Lo que ignoraste:** la espada legendaria de Morne está hecha con las espadas de **todo un clan** al que Godfrey dejó sin país; el único superviviente las soldó para vengarse… y también cayó. Y en Velo Tormentoso, el retrato de quien les quitó el castillo sigue colgado en el salón.
- **URLs:** https://eldenring.fandom.com/es/wiki/Godfrey,_primer_Señor_del_Círculo (cita del monumento) · https://www.eliteguias.com/guias/e/er/elden-ring_armas-p62.php · https://eldenring.fandom.com/wiki/Castle_Morne · https://eldenring.fandom.com/wiki/Storm_Lord · https://eldenring.fandom.com/wiki/The_Stormhawk_King

### C3. Pelear hasta quedarse sin gracia ✅ CONFIRMADO (mejor como sub-hecho que como puesto)
- **Monumento junto a la Iglesia en llamas** (Caelid noroeste; [ES-wiki] lo llama «Monumento en Caelid»; [EN-wiki] Sword Monuments: «Near the Smoldering Church in Limgrave, on the border of Caelid»; [EN-wiki] Smoldering Church: región Caelid), español de [ES-wiki]: «El señor Godfrey finalmente termina su campaña: / Sus ejércitos dorados permanecen invencibles e incólumes. / Pero encuentra la Gracia perdida deteriorada y marchita.»
- Corona: el color de sus ojos se desvanece **cuando cayó su último enemigo**. JP ([EN-wiki]): 好敵手がいなくなった時 («cuando ya no quedaban rivales dignos»; el inglés oficial dice «his last worthy enemy»).
- **Cinta de campeón**: «Prueba de que el portador ha asesinado a innumerables enemigos» y los guerreros siguen «el ejemplo de su líder, Hoarah Loux».
- **Lo que ignoraste:** según el propio juego, Godfrey no pierde la gracia por perder una guerra. La pierde **cuando ya no queda nadie a quien matar**.

### C4. El exilio: se llevó a los suyos a «vivir y morir» lejos ✅ CONFIRMADO
- **Eco de Márika, Tercera iglesia de Márika** (Necrolimbo), español [ES-wiki]: «Mi señor. Os despojo a ti y a tus hombres de la Gracia. / Con la mirada teñida de oscuro, seréis expulsados de las Tierras Intermedias. / Guerrearéis en una tierra lejana, donde viviréis y moriréis.» EN: «My Lord, and thy warriors. I divest each of thee of thy grace. […] Ye will wage war in a land afar, where ye will live, and die.»
- **Eco, Iglesia de la peregrinación** (Península del Llanto), español [ES-wiki]: «Entonces, tras vuestra muerte, os devolveré lo que un día quise para mí. / Regresaréis a las Tierras Intermedias, guerrearéis y blandiréis el Círculo de Elden. / Fortaleceos ante la amenaza de la muerte, guerreros de mi señor Godfrey.» (EN: «I will give back what I once claimed.»)
- **Recuerdo de Hoarah Loux**: «abandonó las Tierras Intermedias en compañía de los suyos».
- **Talismán con hacha** ([EG] talismanes-p6): «El señor que lideró la Larga Marcha portaba un hacha y sus leales guerreros le rindieron homenaje portando una ellos también…» (Ruinas del bosque neblinoso, Necrolimbo este.)
- **Ancla oxidada** ([EG] armas-p67): «Cuando los Sinluz salieron de las Tierras Intermedias con su señor, dicen que solo quedó un único barco.» **Ojo, la traducción cambia el sentido**: EN «one boat alone was said to have been left behind» (un barco **se quedó atrás**). Usa la idea del inglés o di la frase española tal cual sin interpretarla.
- **Brave's Battlewear** es **contenido recortado** ([EN-wiki], {{cut}}): no citarlo.
- **La intro del juego** ([YT] subtítulos de _uydEN9Fu7M y 7BnZhJg91RQ + [EN-wiki] Tarnished): «Arise now, ye Tarnished. Ye dead, who yet live. The call of long-lost grace speaks to us all.» y luego «Hoarah Loux, chieftain of the badlands». Español de la primera frase ([ES-wiki] Sinluz): «Alzaos, Sinluz, es el momento. Vosotros que habéis muerto, pero vivís. La llamada de la Gracia perdida nos habla a todos.» «Hoarah Loux, líder de Tierra Baldía» aparece en [ES-wiki] solo como pie de imagen → texto de la intro en español: **NO VERIFICADO**.
- **Lo que ignoraste:** los Sinluz —tú incluido— existen porque Godfrey aceptó llevarse a su gente a morir en otra tierra con la promesa de resucitar algún día para seguir guerreando. Cada vez que mueres y vuelves, estás cobrando esa promesa.

### C5. Los hijos augurio bajo la capital ✅ CONFIRMADO con matiz importante
- **Párvulo maldito de la realeza** ([EG] objetos-p489; erratas «aguruios», «sinque madie»): «Muñeco de un párvulo expiatorio del linaje real del Árbol Áureo. […] A los hijos de [augurios] nacidos en la realeza no se les extirpan los cuernos, sino que se los oculta bajo tierra [sin que nadie] lo sepa, encarcelados para toda la eternidad. Estos amuletos de recuerdo se confeccionan en secreto.» (Se obtiene con el Recuerdo del rey de los Augurios.)
- **Párvulo maldito** ([EG] objetos-p496): «A los hijos de los augurios se les extirpan los cuernos, por lo que la mayoría perecen. Estos amuletos se confeccionan en su recuerdo. "Por favor, te ruego que no me odies ni me maldigas".» (Lo suelta un enemigo en el Subsuelo de los marginados.)
- **Grillete de Mohg** ([EG] objetos-p492; errata «Mogh»): «Un amuleto bañado en magia dorada. Antaño, se usaban grilletes para atar a esa gente maldita a la que se conoce como augurios; estos, en concreto, fueron creados para mantener a uno en particular bajo un confinamiento muy estricto.»
- **Recuerdo del rey de los Augurios** ([EG] objetos-p488; errata «pro ello»): «Pese a haber nacido como un augurio más sin la Gracia, Morgott decidió convertirse en el protector del Árbol Áureo. Jamás recibió ninguna muestra de afecto [por] ello, pero aún así, él amó.»
- Godfrey vuelve **cuando Morgott ya está muerto**: primera línea de la escena «It's been a long while, Morgott.» ([EN-wiki] dialogue; [YT] LhXGJMZ1kpY 0:17). [ES-wiki]: lo encuentra «lamentando la muerte de Morgott».
- **Matiz que hay que decir:** el juego **no dice quién ordenó encerrarlos**. Ni Godfrey ni Márika aparecen firmando. Lo que sí es comprobable: eran hijos de la realeza, los encerraron «para toda la eternidad», y el padre estaba de campaña (ver C3) y luego en el exilio (C4). Que **Godfrey hiciera el muñeco** es especulación de [EN-wiki] («He likely made…») → **NO VERIFICADO**.
- **Línea recortada** (no está en el juego, no citar como si lo estuviera): «Forgive me, Morgott.»

### C6. Serosh: el regente al que mata él mismo ✅ CONFIRMADO (material muy fuerte; es la escena más famosa)
- Serosh lo acompañó en el exilio: [ES-wiki] Serosh: «Cuando Godfrey abandonó las Tierras Intermedias como un Sinluz, Serosh permaneció con él y pareció perecer junto a su Señor» (apoyado en la intro). En la intro se ve a Hoarah Loux con Serosh ([EN-wiki] galería: «Godfrey and Serosh as depicted in the game's intro cutscene»).
- **Diálogo exacto de la transición** ([EN-wiki] Godfrey/dialogue, confirmado por [FX] y por [YT] LhXGJMZ1kpY): «Nngh! / **That will be all.** / **Thou didst me good service, Serosh.** / **I've given thee courtesy enough.** / Rrraaargh! / **Now I fight as Hoarah Loux! / Warrior!**»
  - JP ([EN-wiki]): «もう、よい / ずっと、世話をかけたな、セローシュよ / 行儀のよい振りは、もうやめだ / 今より、俺はホーラ・ルー！ / 戦士よ！» (en japonés la tercera línea habla de dejar de **fingir buenos modales**; el inglés oficial es «courtesy enough»).
  - Español del juego: **NO VERIFICADO** (ver §6, transcribir de un clip con subtítulos en español).
- **Cómo lo mata** — [ES-wiki] Serosh: «En el transcurso de la pelea, Serosh comienza a adoptar una forma más tangible, aparentemente preparándose para asumir un papel activo en la batalla. Sin embargo, Godfrey sostiene la cabeza de Serosh y **le rompe el cuello**, después de agradecerle por su servicio. Cubierto con la sangre de su antiguo regente, Godfrey se deshace de su hacha y continúa la lucha como Hoarah Loux.» [EN-wiki] Serosh: «When pushed to their limit, Serosh transitions from a spirit to a tangible, corporeal form, preparing to play an active role in the duel. However, Godfrey interrupts the process; he thanks Serosh for his service and violently kills him, drenching himself in the blood of his Beast Regent.»
- Detalle de modelo ([EN-wiki] Serosh, descripción visual; comprobar en captura): Serosh tiene los ojos cerrados y cicatrices («indicating his blindness» es lectura de la wiki), y en la espalda de Godfrey es translúcido. [ES-wiki] Notas: Serosh muerde el hombro de Godfrey cuando este ataca.
- **Muere** ([EN-wiki], [FX], [YT]): «Brave Tarnished... / Thy strength befits a crown.» Si te mata en la fase 2: «A crown is warranted with strength!»
- **Lo que ignoraste:** Serosh no se le cae: **se estaba volviendo de carne para pelear a su lado** y Godfrey lo interrumpe para matarlo. El león que llevó a cuestas desde que juró ser rey, que lo siguió al exilio y a la muerte, dura exactamente hasta que Godfrey va perdiendo. Su «gracias por los servicios» es el finiquito más rápido de las Tierras Intermedias.

### C7. Volvió por el trono cuando todo ardía ✅ CONFIRMADO (débil como puesto; bueno como gancho/cierre)
- Escena de entrada ([EN-wiki], [YT] LhXGJMZ1kpY 0:17–1:44): «Long and hard didst thou fight. Tarnished Warrior. Spurned by the grace of gold. Be assured, the Elden Ring resteth close at hand. Alas, I am returned. To be granted audience once more. Upon my name as Godfrey, the first Elden Lord!»
  - **Español verificado** ([ES-wiki], cita en la ficha): «Por desgracia, aquí estoy de nuevo para reclamarlo una vez más. Yo, Godfrey, ¡El primer Señor del Círculo!»
- Llega después de que **tú** quemaste el Árbol y mataste a Maliketh ([EN-wiki] Serosh; [ES-wiki] Godfrey).
- **Recortado, NO está en el juego** ([EN-wiki] {{cut}}): «True strength indeed, is precisely what I must take back. Do not fear, dear Erdtree. Do not fear, dear Marika. […] Thy rescue is near.» y «Dearest Marika... I am returned. O Marika! I will take thee in mine arms once more!» → solo como dato curioso, diciendo que es material cortado.

### C8. El legado: el linaje dorado ✅ CONFIRMADO (cameo)
- Godrick (su descendiente) injerta miembros y, si te mata, pregunta: «Great Godfrey, didst thou witness?» ([EN-wiki] Godrick/dialogue). Gideon: «grotesque old fool, grasping for power». **Sobretodo con árbol y bestia**: «símbolos de una gloria ya pasada».
- Godefroy, el Injertado guarda el **Icono de Godfrey** (Meseta Altus).
- Sirve para cerrar: «el emblema del linaje dorado» (Hacha de Godfrey) termina en un castillo de injertos.

### C9. Guerra contra los dragones / Farum Azula ❌ DESCARTAR
- El monumento junto a la *Stormcaller Church* (Meseta Altus; nombre español **NO VERIFICADO**) dice ([EN-wiki] Sword Monuments): «The Routing of the Ancient Dragons / Godwyn the Golden fought to the last, / Earning the friendship of dread Fortissax». **Es de Godwyn, no de Godfrey.** No encontré ningún texto que ponga a Godfrey en esa guerra. Tampoco una «tribu Azula» vencida por él: el parecido del Hacha de Godfrey con el **Machete de hombre bestia** es observación de [EN-wiki] (Notes), no lore.

### C10. Otros que no dan para puesto
| Tema | Veredicto | Dato |
|---|---|---|
| Halcones de guerra con las garras cortadas | ❌ No es de Godfrey | **Cenizas de halcón de guerra** (EN): «the talons of which have been sliced off so that razor-fine swords could be grafted» = injertos (época de Godrick), «With its lord vanquished…» |
| Cuernos cortados a los leones / halcones por el linaje dorado | ❌ Especulación de [EN-wiki] (Castle Morne, Trivia) | Sin texto del juego |
| Comer carne de bestia, cazar osos | ⚠ Cameo | Carne excelsa, Atuendo glorioso (arriba) |
| Caballeros del crisol | ⚠ Contexto | Servían a Godfrey; sin atrocidad atribuida |

---

## 3. Citas listas para usar (estado de verificación)

| Cita | Idioma | Estado |
|---|---|---|
| «Por desgracia, aquí estoy de nuevo para reclamarlo una vez más. Yo, Godfrey, ¡El primer Señor del Círculo!» | ES | ✅ textual [ES-wiki] |
| «It's been a long while, Morgott.» | EN | ✅ [EN-wiki] + [YT] |
| «That will be all. Thou didst me good service, Serosh. I've given thee courtesy enough.» | EN | ✅ [EN-wiki] + [FX] + [YT] |
| «Now I fight as Hoarah Loux! Warrior!» | EN | ✅ [EN-wiki] + [YT] (el encargo decía «¡Soy Hoarah Loux, guerrero!»: **esa versión española NO VERIFICADA**) |
| «Brave Tarnished... Thy strength befits a crown.» / «A crown is warranted with strength!» | EN | ✅ [EN-wiki] + [FX] |
| «Acaba con los gigantes con tu espada y confina la llama en lo alto de la montaña.» | ES | ✅ [ES-wiki] (eco de Márika) |
| «Mi señor. Os despojo a ti y a tus hombres de la Gracia. […] Guerrearéis en una tierra lejana, donde viviréis y moriréis.» | ES | ✅ [ES-wiki] |
| «Fortaleceos ante la amenaza de la muerte, guerreros de mi señor Godfrey.» | ES | ✅ [ES-wiki] |
| «…solo para terminar en manos del señor Godfrey.» (monumento de Morne) | ES | ✅ [ES-wiki] |
| «Sus ejércitos dorados permanecen invencibles e incólumes. Pero encuentra la Gracia perdida deteriorada y marchita.» | ES | ✅ [ES-wiki] |
| «Champions battle, trolls betray» (monumento de los gigantes) | EN | ✅ [EN-wiki]; español NO VERIFICADO |
| Corona, Icono, Recuerdo, Cinta, Hacha, Espadón de hoja injertada, Párvulos, Grillete, Espada dorada de trol, Recuerdo del gigante de fuego, Talismán de la dádiva del señor | ES | ✅ [EG] (cotejar erratas antes de rotular) |
| «Alzaos, Sinluz, es el momento. Vosotros que habéis muerto, pero vivís.» | ES | ✅ [ES-wiki] |
| Resto de líneas de Godfrey en español | ES | **NO VERIFICADO** |

---

## 4. Lugares para MAPAS (región del mapa del mundo)

| Lugar | Región | Ligado a | Fuente |
|---|---|---|---|
| **Santuario del Árbol Áureo** (sombra dorada de Godfrey) | Leyndell, capital del Reino (este de la Meseta Altus). Acceso: desde el Lugar de Gracia «Muralla oeste de la capital», hacia el sur por la muralla, subir por la rama al balcón y al norte, a la niebla | Sombra dorada (jefe obligatorio, suelta Bolsa para talismán) | [ES-wiki] Godfrey (sombra dorada); [ES-wiki] Leyndell |
| **Trono de Elden** (combate final) | Leyndell, capital cinérea (la misma capital, en ruinas tras quemar el Árbol) | C6, C7 | [ES-wiki], [EN-wiki] Elden Throne |
| **Subsuelo de los marginados** | Bajo Leyndell | C5 | [ES-wiki], [EG] |
| **Castillo de Velo Tormentoso** | Colina Tormentosa (Necrolimbo, noroeste) | C2 | [ES-wiki] |
| **Castillo de Morne** + monumento a la izquierda de la entrada | Sur de la Península del Llanto | C2 | [ES-wiki], [EN-wiki] Sword Monuments |
| **Iglesia en llamas** + monumento de «fin de la campaña» | Caelid noroeste, en la frontera con Necrolimbo | C3 | [EG] gracia, [EN-wiki] |
| **Tercera iglesia de Márika** (eco del destierro) | Necrolimbo (este, junto al bosque neblinoso) | C4 | [EG] gracia, [EN-wiki] |
| **Iglesia de la peregrinación** (eco de la promesa) | Península del Llanto | C4 | [EG] gracia, [EN-wiki] |
| **Primera iglesia de Márika** (eco «acaba con los gigantes») | Picos de los gigantes | C1 | [EG] gracia, [EN-wiki] |
| **Tumba del héroe matagigantes** + monumento «trolls betray» | Picos de los gigantes | C1 | [ES-wiki], [EN-wiki] |
| **Forja de los gigantes** / **Pico de la llama** (Gigante de fuego) | Picos de los gigantes (noreste del mapa) | C1 | [ES-wiki] Gigante de fuego |
| **Ruinas de Zamor** (aliados en la guerra) | Picos de los gigantes | C1 | [ES-wiki] Picos |
| Prisión eterna de Godefroy (Icono de Godfrey) | Sur de la Meseta Altus | C8 | [EN-wiki] Golden Lineage Evergaol; nombre español **NO VERIFICADO** |
| **Fortaleza sombría** (Talismán de la dádiva del señor) | DLC, región *Scadu Altus* ([EN-wiki]); que su nombre español sea «Altiplano Sombrío» ([EG] lo usa para el mapa del DLC): **NO VERIFICADO** | DLC | [EG], [EN-wiki] Shadow Keep |
| Tierra Baldía | **Fuera del mapa** (lugar mencionado, no visitable) | C4 | [EN-wiki] Badlands («a mentioned location») — en el mapa, flecha saliendo del borde, no marcador |

---

## 5. ESCENAS IMPORTANTES y clips (solo ids y segundos; nada descargado)

Canales evitados: Fextralife, IGN, PowerPyx, Gamerpillar, VaatiVidya, **Shirrako** (salió en todas las búsquedas: GRc2rqDDBGk, p8DoLcas1o0 — no usar). Los segundos con «[YT]» salen de subtítulos automáticos o capítulos; **revisar marca de agua y rótulos de cada canal antes de usarlo**.

| Escena | Video (id · canal · duración) | Momento |
|---|---|---|
| **Intro del juego** («The fallen leaves tell a story», «Hoarah Loux, chieftain of the badlands») | **_uydEN9Fu7M** · RajmanGaming HD · 266 s | 0:05 «The fallen leaves…»; 0:20 «The great Elden Ring was shattered»; 2:05 «Arise now, ye Tarnished»; **~2:26–2:32 «Hoarah Loux, chieftain of the badlands»**; 3:23 «A Tarnished of no renown» [YT] |
| Intro (alternativa) | **7BnZhJg91RQ** · BonfireVN · 244 s | 2:06 «Arise now»; **~2:29–2:34 Hoarah Loux**; 2:38 Gold Mask [YT] |
| Intro (alternativa larga) | tySAeZrYxok · Gamer's Little Playground · «All Cutscenes» 5894 s | No fechado |
| **Entrada de Godfrey en el Trono + transformación (Serosh)** | **LhXGJMZ1kpY** · Draknalor186 · 201 s | 0:17–0:20 «It's been a long while, Morgott»; 0:35 «Long and hard didst thou fight»; 1:11 «Alas, I am returned»; 1:36–1:44 «Upon my name as Godfrey…»; **~2:00 «That will be all»; 2:04–2:09 «Thou didst me good service, Serosh»; 2:44 «I've given thee courtesy enough»; ~2:54 muerte de Serosh (grito); 3:10–3:17 «Now I fight as Hoarah Loux! Warrior!»** [YT] |
| Mismo combate, **sin HUD 4K** | **XMCh2vAi_Yc** · JustGamesBruh · 382 s | Capítulos: Cinemática 1 **0:25–2:16**; Fase 1 2:16–2:57; Cinemática 2 (Serosh) **2:57–4:33**; Fase 2 4:33–6:22 [YT] |
| Mismo combate, sin HUD | **4doIpyiGKgQ** · ONGBAL · 386 s | Capítulos: Intro **0:00–1:51**; Fase 1 1:51–3:16; Cinemática fase 2 **3:16–4:49**; Fase 2 4:49–6:26 [YT] |
| Muerte de Hoarah Loux («Thy strength befits a crown») | **rTz4PyJYphw** · SourceSpy91 · Part 50, 1278 s | Capítulo «LEGEND FELLED» en 20:22 → la línea, justo antes (~20:05–20:22, **segundo exacto NO VERIFICADO**) |
| **Sombra dorada** (Santuario del Árbol Áureo) | **XEIlOcx6VwQ** · Ripper371 · 105 s (no commentary) · WXSNYQbtxbo · BOSS FIGHT · 91 s | Combate completo. **Que tenga cinemática de entrada: NO VERIFICADO** (las wikis no transcriben ninguna) |
| Longplay sin comentarios (respaldo para todo) | **HJ6EIysyst8** · SourceSpy91 · 81 h | Capítulos: Castillo de Morne **11:03:07**; Velo Tormentoso **12:22:37**; Godfrey (sombra) **62:18:17**; Morgott **62:48:35**; Picos de los gigantes **63:30:29**; Gigante de fuego **67:12:44**; Subsuelo de los marginados **75:43:38**; Godfrey/Hoarah Loux **80:52:51** [YT] |
| **Ecos de Márika** (Melina habla sobre jugabilidad) | **GRH4LNXKQt8** · Games from Mars · 1424 s | Tercera iglesia **6:22–7:16** («divest each of thee» ~6:50); Iglesia de la peregrinación **7:16–8:01**; Primera iglesia **14:23–15:10** [YT] |
| Monumento de Morne | eQurI1KRErE · (canal sin dato) · 62 s · «Lone Hero Falls To Lord Godfrey» | Completo; o longplay 11:03:07 |
| Subsuelo de los marginados | **QjakOuLJlpw** · SourceSpy91 · Part 49 | Exploración |
| Morgott (el hijo que defendía el trono) | **L4zVRGHc1yQ** · SourceSpy91 · Part 35 | Combate |
| Gigante de fuego | SUiP6yXW_x8 (351 s) · DekVMypUQDY · mnJsvwqYXR4 (canal sin dato en la búsqueda) | Combate; o longplay 67:12:44 |
| Para **transcribir el español** del juego | n-qv82v9rAw · Mr.Mumbru · «GODFREY, PRIMER SEÑOR DEL CÍRCULO… Cinemática #5» · 111 s · nsaXevM7yso · GameTrusTv · «Todas las cinemáticas» · 204 s · RuXbpe2KeKU · RZerø · «Intro [subtitulos Español]» · 243 s | Mirar si los subtítulos son del juego (no de fan). **uOJZQ-5d6Jk es un doblaje de fan: NO usar** |

**Escenas que hay que mostrar y no son cinemática** (clip de juego o captura): cadáveres de gigantes empalados en los Picos (C1), retrato y estatua de Godfrey en Velo Tormentoso (C2), monumento de Morne y de la Iglesia en llamas (C2/C3), el Bastardo leonino con el Espadón de hoja injertada (C2), Subsuelo de los marginados (C5).

---

## 6. PUESTOS PROPUESTOS (del 5 al 1)

Lógica de escala: de los **enemigos** (5) a **su gente** (4), **sus hijos** (3), **una especie entera** (2)… y el n.º 1 rompe la escala: no es el más grande, es el más personal. Duración orientativa: gancho 1:30 · cinco puestos de 3:45–4:15 · suscripción ≈ 0:10 antes del n.º 1 · cierre 1:00 ≈ 25 min.

### N.º 5 — «Coleccionista de reinos» (Velo Tormentoso y Morne)
**Gancho:** «Todo el mundo recuerda a Godrick en Velo Tormentoso. Nadie se pregunta de quién era el castillo antes.»
1. «Se enfrentó solo al señor de la Tormenta» (Corona) y el retrato de Godfrey y Serosh sigue en el salón principal (captura). Las cenizas de *The Stormhawk King* hablan de los días en que los vientos de Velo Tormentoso «still raged like no other» (EN): ya no rugen. (Que fuera culpa de Godfrey: NO VERIFICADO, dilo como pregunta).
2. Monumento de Morne: «…solo para terminar en manos del señor Godfrey.»
3. Espadón de hoja injertada: un superviviente «de un país desaparecido» soldó las espadas «de todo un clan» para vengarse. Hoy la usa el Bastardo leonino.
4. Remate (C3): perdió la gracia «cuando cayó su último enemigo», y sus guerreros llevan una cinta que es «prueba de que el portador ha asesinado a innumerables enemigos».
**Clips:** longplay HJ6EIysyst8 11:03:07 (Morne) y 12:22:37 (Velo Tormentoso); eQurI1KRErE (monumento).

### N.º 4 — «Llevó a su pueblo a morir lejos» (la Larga Marcha)
**Gancho:** «¿Quieres saber por qué eres un Sinluz? Pregúntale a Godfrey.»
1. Márika (Tercera iglesia): «Os despojo a ti y a tus hombres de la Gracia… donde viviréis y moriréis.» Y Godfrey «abandonó las Tierras Intermedias en compañía de los suyos» (Recuerdo).
2. La promesa (Iglesia de la peregrinación): «tras vuestra muerte, os devolveré lo que un día quise para mí». Sus guerreros lo seguían con hachas (Talismán con hacha); un barco se quedó atrás (Ancla oxidada, matiz EN).
3. Se quita la corona y vuelve a ser Hoarah Loux, «líder de Tierra Baldía»; la intro lo nombra entre los muertos que «aún viven»: «Alzaos, Sinluz…».
**Giro de puesto:** cada vez que mueres y vuelves, estás cobrando el trato que él aceptó.
**Clips:** GRH4LNXKQt8 6:22–8:01 (ecos); _uydEN9Fu7M 2:05–2:32 (intro).

### N.º 3 — «Padre del año» (los gemelos augurio)
**Gancho:** «Su primera frase al volver no es para Márika. Es para un hijo muerto.»
1. Párvulo maldito de la realeza: a los augurios de la realeza no les cortan los cuernos, los ocultan «bajo tierra sin que nadie lo sepa, encarcelados para toda la eternidad». Grillete de Mohg: «magia dorada».
2. A los plebeyos sí les cortan los cuernos «y la mayoría perecen» (Párvulo maldito: «Por favor, te ruego que no me odies ni me maldigas»).
3. Morgott defendió el trono de su padre sin que nadie lo quisiera («Jamás recibió ninguna muestra de afecto por ello, pero aún así, él amó»), y Godfrey llega cuando ya está muerto: «It's been a long while, Morgott.»
**Advertencia de guion:** decir que el juego **no dice quién los encerró**; la atrocidad es la ausencia (estaba de campaña y luego en el exilio). Ironía: los Sinluz que Morgott mataba en la capital eran la gente de su padre.
**Clips:** LhXGJMZ1kpY 0:17–0:20; QjakOuLJlpw (subsuelo); L4zVRGHc1yQ (Morgott).

### N.º 2 — «Acaba con los gigantes con tu espada» (guerra contra los gigantes)
**Gancho:** «Hay una especie entera que ya no existe. Su asesino lleva corona.»
1. La orden (Primera iglesia de Márika): «Acaba con los gigantes con tu espada y confina la llama en lo alto de la montaña». La ejecuta él: «Lideró la guerra contra los gigantes» (Corona).
2. Queda **un** superviviente, maldito a cuidar la llama «por toda la eternidad» (Recuerdo del gigante de fuego). «Después de que los gigantes desaparecieran…» (Aplastagigantes). Cadáveres empalados en el campo (escenario).
3. Los troles, descendientes de los gigantes, «traicionan» a los suyos (monumento) y reciben una espada dorada que hoy se desconcha en manos de troles que «han perdido la cordura» (Espada dorada de trol).
**Clips:** GRH4LNXKQt8 14:23–15:10 (eco); longplay 63:30:29 (Picos) y 67:12:44 (Gigante de fuego); SUiP6yXW_x8.

### N.º 1 — «El finiquito de Serosh»
**Giro:** «Las otras cuatro fueron contra enemigos, contra su pueblo, contra sus hijos, contra una especie. Esta fue contra el único que lo aguantó todas esas eras. Y la hizo delante de ti, porque ibas ganando.»
1. Serosh es el freno: Godfrey «comenzó a llevar a la bestia regente Serosh a sus espaldas, con el fin de calmar el incesante deseo de batalla» (Icono); «Lucha con pasión, pero no seas su prisionero» (Escudo apuntado). Fue «regente del rey Godfrey» (Gran martillo) y emblema del linaje (Sobretodo).
2. Lo siguió al exilio y a la muerte (intro; [ES-wiki] Serosh).
3. **Lo que ignoraste:** cuando Godfrey va perdiendo, Serosh **empieza a volverse de carne para pelear por él**, y Godfrey lo interrumpe y le rompe el cuello: «That will be all. Thou didst me good service, Serosh. I've given thee courtesy enough.» Y se baña en su sangre: «Now I fight as Hoarah Loux! Warrior!»
4. Cierre: muere diciéndote «Thy strength befits a crown» — «[Antaño], la corona se afianzaba mediante la fuerza» (Hacha de Godfrey). Y la postdata del DLC: el Talismán de la dádiva del señor dice que «proyecta una larga sombra sobre las tierras». Pues sí.
**Clips:** LhXGJMZ1kpY 2:00–3:17; XMCh2vAi_Yc 2:57–4:33 (sin HUD); 4doIpyiGKgQ 3:16–4:49; muerte en rTz4PyJYphw ~20:05–20:22.

**Reservas / cameos:** C7 (vuelve «para reclamarlo una vez más», con la cita española verificada, como gancho inicial) · C8 (Godrick: «Great Godfrey, didst thou witness?» como remate del n.º 1 o del cierre) · Carne excelsa y cazadores de osos (color para el n.º 4).

---

## 7. Datos falsos comunes que NO hay que decir

1. **«And one day, the Elden Ring was shattered…»** — la intro dice «The fallen leaves tell a story. The great Elden Ring was shattered.» ([YT] _uydEN9Fu7M 0:05–0:23).
2. **«A Morgott y Mohg les cortaron los cuernos.»** — Falso: a los augurios **de la realeza no** se los extirpan; los encierran bajo tierra (Párvulo maldito de la realeza). Los que pierden los cuernos son los plebeyos.
3. **«Godfrey encerró a sus hijos.»** — NO VERIFICADO: ningún texto dice quién lo ordenó.
4. **«Godfrey luchó contra los dragones / Farum Azula / la tribu Azula.»** — El monumento de los dragones es de **Godwyn**. No hay texto que meta a Godfrey ahí.
5. **«Godfrey mató al dios caído de los gigantes.»** — Ningún texto se lo atribuye; la wiki se lo atribuye a Márika, y aun así con «se cree».
6. **«Perdió la gracia por perder una batalla / por traición.»** — El juego dice lo contrario: sus ejércitos estaban «invencibles e incólumes»; los ojos se le apagan cuando «cayó su último enemigo».
7. **«Tierras Baldías»** → es **Tierra Baldía**. **«Colina de la Tormenta»** → **Colina Tormentosa**. **«Vestigio de Hoarah Loux»** → **Recuerdo**. **«Talismán del Señor del Círculo»** y **«Hacha de Hoarah Loux»** no existen con esos nombres.
8. **«¡Soy Hoarah Loux, guerrero!»** como cita del juego — el inglés es «Now I fight as Hoarah Loux! Warrior!»; la versión española no está verificada.
9. **«La sombra dorada aparece en el Trono de Elden.»** — Está en el **Santuario del Árbol Áureo** (capital del Reino). La del Trono es la de verdad, en la capital cinérea.
10. **«Nepheli es hija de Godfrey.»** — Relación desconocida ([ES-wiki]).
11. **«Godfrey dice "Forgive me, Morgott" / "Dearest Marika, I will take thee in mine arms" / "Thy rescue is near".»** — Son líneas **recortadas**, no están en el juego.
12. **«Hoarah Loux narra la intro.»** — La voz es el narrador; a Hoarah Loux solo lo **nombra** («chieftain of the badlands»).
13. **«Serosh era una mascota / un león cualquiera.»** — Es «Serosh, Señor de las Bestias» y «bestia regente», que «se convertiría en regente del rey Godfrey».
14. **«Los halcones de Velo Tormentoso perdieron las garras por Godfrey.»** — Las Cenizas de halcón de guerra hablan de injertos (época de Godrick).

---

## 8. Pendientes para la sesión de guion
- **Español de los diálogos de Godfrey:** solo está verificada la línea «Por desgracia, aquí estoy de nuevo…». Transcribir el resto (Morgott, Serosh, Hoarah Loux, muerte) de un clip con subtítulos **del juego** en español (candidatos en §5) o parafrasear sin comillas.
- Español del monumento de los gigantes («Champions battle, trolls betray») y de la línea de la intro «Hoarah Loux, chieftain of the badlands»: **NO VERIFICADO**.
- Citas de [EG]: cotejar con captura (erratas señaladas en cada una).
- Comprobar con captura: retrato y estatua en Velo Tormentoso, cadáveres empalados en los Picos, ojos cerrados de Serosh.
- Revisar marca de agua y rótulos de: RajmanGaming HD, BonfireVN, Draknalor186, JustGamesBruh, ONGBAL, Games from Mars, Ripper371, y de los videos con canal «sin dato».
- **NO VERIFICADO:** quién encerró a los augurios · quién empaló a los gigantes · si la tormenta de Velo Tormentoso acabó por Godfrey · nombre español de *The Stormhawk King*, de la prisión eterna de Godefroy, de la *Stormcaller Church* y del *Troll's Hammer* · si la sombra dorada tiene cinemática.
