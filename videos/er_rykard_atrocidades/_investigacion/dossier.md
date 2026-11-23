# Dossier: «Las 5 peores atrocidades de Rykard QUE IGNORASTE»

Canal Runa Caída. Investigación del 22-nov-2026. Todo lo de abajo sale de las fuentes enlazadas, leídas hoy por API, descarga directa, `yt-dlp` (solo subtítulos/capítulos/metadatos) o Whisper sobre la pista de audio de 3 clips cortos (para fechar líneas habladas; audio borrado después). Lo que no pude comprobar va marcado **NO VERIFICADO**. Cuando una afirmación es interpretación de la wiki (no texto del juego), lo digo.

## 0. Fuentes y cómo leerlas

| Clave | Fuente | Para qué sirve |
|---|---|---|
| **[ES-wiki]** | Wiki en español de Fandom, `https://eldenring.fandom.com/es/wiki/<Página>` (API `action=parse&prop=wikitext`) | Nombres oficiales en español; descripciones `{{Descripción\|ES=…}}`; **la única línea de Rykard en español** («Únete a la familia del Rey Serpiente…»); el texto español del monumento del monte Gelmir. **Wiki pequeña**: no tiene páginas de Hoja blasfema, Rencor, Cazador de serpientes, Garra blasfema, Camafeo, Tónico, Daedicar, etc. |
| **[EN-wiki]** | Wiki inglesa, `https://eldenring.fandom.com/wiki/<Page>` (API) | Descripciones en inglés y japonés (`EN_line`/`JP`), diálogos completos (Rykard/dialogue, Tanith, Rya the Scout, Knight Bernahl, Patches, Sir Gideon Ofnir/dialogue, Volcano Manor Apparition, Stranded Souls). **Ojo**: «Background» mezcla texto con interpretación; solo cito como hecho lo que va entre comillas de un objeto o diálogo |
| **[EG]** | Eliteguias, `https://www.eliteguias.com/guias/e/er/elden-ring_<sección>-pNNN.php` (descarga directa; la página viene en ISO-8859-1) | Descripciones en español transcritas del juego. **Tiene erratas** (marcadas en cada cita con [sic] o corchetes). Índices útiles: `elden-ring_objetos.php`, `_armas.php`, `_armaduras.php`, `_talismanes.php`, `_hechizos.php`, `_gracia.php`, `_shadow-of-the-erdtree.php` |
| **[FX]** | Fextralife (`Rykard,+Lord+of+Blasphemy`, `Tanith`, `Rya`, `Patches`; HTTP 200 con `curl -L`) | Solo para **confirmar** líneas clave: «Join the Serpent King», «devour the very gods», «serpent never dies», «carcass is vast», «find purchase within me», «your serpent», «hideous ritual», «Kill me, please», «transposition», «like animals», «daddy ambition» → todas aparecen |
| **[YT]** | Subtítulos automáticos (inglés) y capítulos con `yt-dlp` (sin video) | Fechar escenas y líneas. **[WH]** = segundo medido con Whisper `medium` sobre la pista de audio (clips con música encima: **±2-3 s**, comprobar al cortar) |

### Nombres oficiales en español (verificados) — inglés → español

| Inglés | Español oficial | Fuente / nota |
|---|---|---|
| Rykard, Lord of Blasphemy | **Rykard, señor de la Blasfemia** | [ES-wiki], [EG] jefazos-p93 |
| Praetor Rykard | **pretor Rykard** (minúscula en los objetos) / «Pretor Rykard» | [EG] Camafeo, Garra blasfema, Casco de caballero de Gelmir; [ES-wiki] alias |
| The Serpent King | **Rey Serpiente** | [ES-wiki] (alias y cita de la intro) |
| God-Devouring Serpent | **Serpiente devoradioses** (fase 1) · LatAm: «Serpiente devoradora de dioses» | [ES-wiki], [EG] |
| Volcano Manor | **Mansión del Volcán** · LatAm: «Mansión Volcánica» | [ES-wiki], [EG] |
| Mt. Gelmir | **Monte Gelmir** (en los objetos a veces «monte Gelmir») | [ES-wiki], [EG] |
| Altus Plateau | **Meseta Altus** | [ES-wiki], [EG] gracia |
| Recusant(s) | **Recusante(s)** | [EG] Dedo Recusante; [ES-wiki] Tanith/Bernahl |
| Recusant Finger | **Dedo Recusante** | [EG] objetos-p456 |
| Remembrance of the Blasphemous | **Recuerdo del blasfemo** | [ES-wiki], [EG] objetos-p507 |
| Rykard's Great Rune | **Gran Runa de Rykard** | [ES-wiki], [EG] objetos-p506 |
| Blasphemous Blade / Taker's Flames | **Hoja blasfema** / habilidad **Llamas del megalómano** | [EG] armas-p268 |
| Rykard's Rancor | **Rencor de Rykard** | [EG] hechizos-p66 |
| Serpent-Hunter | **Cazador de serpientes** | [EG] armas-p267 |
| Devourer's Scepter | **Cetro de devorador** | [ES-wiki], [EG] armas-p76 |
| Blasphemous Claw | **Garra blasfema** | [EG] objetos-p550 |
| Taker's Cameo | **Camafeo del megalómano** | [EG] talismanes-p74 |
| Tonic of Forgetfulness | **Tónico del olvido** | [EG] objetos-p462 |
| Daedicar's Woe | **Pesar de Daedicar** | [EG] talismanes-p67 |
| Consort's Mask / Robe | **Máscara de consorte** / **Túnica de consorte** | [EG] armaduras-p397/398 |
| Serpent's Amnion | **Amnios de serpiente** | [EG] objetos-p461 |
| Man-Serpent Ashes | **Cenizas de hombre serpiente** | [EG] cenizas-espiritus-p53 |
| Man-serpent | **hombre serpiente** | [EG], [ES-wiki] |
| Serpent-God's Curved Sword | **Espada curva de dios serpiente** | [EG] armas-p119 |
| Magma Shot / Gelmir's Fury | **Disparo de magma** / **Ira de Gelmir** | [EG] hechizos-p62/63 |
| Serpentbone Blade | **Hoja de hueso de serpiente** | [EG] armas-p233 |
| Gelmir Knight Helm / Armor | **Casco / Armadura de caballero de Gelmir** | [EG] armaduras-p328/329 |
| Inquisitor's Girandole | **Candelabro de inquisidor** | [EG] armas-p200 |
| Ghiza's Wheel / Inquisitor Ghiza | **Rueda de Ghiza** / **inquisidor Ghiza** | [EG] armas-p232 |
| Bloodsoaked Mask / Official's Attire | **Máscara ensangrentada** / **Atuendo de oficial** | [EG] armaduras-p373/382 |
| Abductor Virgin(s) / Iron Virgin | **Virgen raptora / Vírgenes raptoras** (jefe y gracia) · en textos de objeto: **«vírgenes de hierro»** | [ES-wiki], [EG] jefazos-p72, gracia; [EG] Rueda de Ghiza |
| Subterranean Inquisition Chamber | **Cámara subterránea de la inquisición** | [EG] gracia, [ES-wiki] |
| Prison Town Church / Temple of Eiglay / Guest Hall / Audience Pathway | **Iglesia de la ciudad de los penados** / **Templo de Eiglay** / **Sala de invitados** / **Camino del auditorio** | [EG] gracia, [ES-wiki] |
| Gelmir Hero's Grave | **Tumba del héroe de Gelmir** | [EG] gracia, [ES-wiki]. (No existen «Ruinas de Gelmir» con ese nombre en lo que revisé) |
| Ninth Mt. Gelmir Campsite | **Noveno campamento del monte Gelmir** (junto al monumento) | [EG] gracia |
| Godskin Noble | **Noble sacrodermo** (jefe del Templo de Eiglay) | [ES-wiki], [EG] |
| Tanith, Volcano Manor Proprietress | **Tanith** (en objetos: «Lady Tanith», «dueña de la Mansión del Volcán») | [EG] Máscara/Túnica |
| Rya / Zorayas | **Rya** / **Zorayas** | [ES-wiki], [EG] Carta de Zorayas |
| Knight Bernahl | **Caballero Bernahl** (alias «Recusante Bernahl») | [ES-wiki] |
| Patches | **Parches** | [ES-wiki], [EG] personajes-p8 |
| Sir Gideon Ofnir, the All-Knowing | **Gideon Ofnir** · en un objeto: «Sir Gideon el Omnisciente» | [EG] personajes-p21, Sobretodo ocular |
| Finger Reader Enia | **Lectora de Dedos Enia** | [EG] |
| Old Knight Istvan | **Viejo caballero Istvan** ([EG] Carta) · [ES-wiki] dice «Vetusto caballero István» en otra página | Fuentes discrepan |
| Academy of Raya Lucaria / Caria Manor | **Academia de Raya Lucaria** / **Mansión de los Caria** | [EG] gracia |
| Liurnia of the Lakes | **Liurnia, tierra encharcada** | [EG] gracia, [ES-wiki] |
| Crumbling Farum Azula | **Farum Azula, la ciudad en ruinas** | [EG] gracia, [ES-wiki] |
| The Shattering | **la Devastación** | [EG] Mapa: Monte Gelmir; [ES-wiki]. **No «Fragmentación»** |
| Night of Black Knives | El juego, en la Garra blasfema, dice **«la noche del complot»**. [ES-wiki] titula el evento «Noche de los Puñales Negros»; las asesinas son «de los Cuchillos Negros» ([EG] Alecto). Nombre del evento en un texto del juego en español: **NO VERIFICADO** | — |
| Greater Will | **Voluntad Mayor** | [ES-wiki] |
| Erdtree / Golden Order | **Árbol Áureo** / **Orden Dorada** | [ES-wiki], [EG] |
| Rune of Death / Black Blade / Destined Death | **Runa de la Muerte** / **la Hoja Negra** / **la Muerte Escrita** | [EG] Garra blasfema |
| Messmer the Impaler | **Messmer el Empalador** | [ES-wiki], [EG] |
| Hornsent | **cornamentados** | [EG] Mayal de serpiente; [ES-wiki] |
| Realm/Land of Shadow | **Reino de las Sombras** (no «Tierra de las Sombras») | [ES-wiki], [EG] Recuerdo del Empalador |
| Crusade | **cruzada** («cruzada purificadora», «cruzada sagrada») | [EG] Armadura de Messmer, Insignia de cruzada |

> **Lo que NO existe con el nombre del encargo:** «Ruinas de Gelmir» (el lugar es **Tumba del héroe de Gelmir**); «Doncella de hierro» como nombre oficial (es **Virgen raptora**; en descripciones, «vírgenes de hierro»); «inquisidores del monte Gelmir» como facción con nombre (el texto es de Gideon: «a company of inquisitors»). «Eiglay» solo aparece como nombre del **Templo de Eiglay**; la wiki dice que es «probablemente» una referencia a Eglė (folclore lituano): **especulación**, no lore.

---

## 1. Quién es Rykard ✅ CONFIRMADO

**(a) Hijo de Rennala y Radagon, semidiós adoptivo**
- **Gran Runa de Rykard** ([EG] objetos-p506; errata «semidió sadoptivo»; = [ES-wiki]): «Rykard era uno de los hijos de Rennala y Radagon, y se convirtió en semidiós adoptivo tras la unión de Radagon con la Reina Márika. / Pero Rykard se ofreció como alimento a la serpiente blasfema, runa incluida.»
  - EN: «…who became demigod stepchildren after Radagon's union with Queen Marika. But Rykard fed himself to the blasphemous serpent, Great Rune and all.» JP: 外戚として («como parientes políticos»).
- **Disparo de magma** ([EG] hechizos-p62): «Tras descubrir los antiguos maleficios de Gelmir, Rykard, hijo de la Reina Rennala, los volvió a poner en práctica como nuevas formas de hechicería.»
- **Casco de caballero de Gelmir** ([EG] armaduras-p328): «Su penacho de plumas rojas es un símbolo del pedigrí de Rykard como hijo del señor Radagon.»
- Hermanos: Radahn y Ranni ([ES-wiki] infobox). Tía: Rellana ([ES-wiki], [EN-wiki]).

**(b) Pretor = juez, al mando de inquisidores** (texto de diálogo, no de objeto)
- **Gideon Ofnir**, «Sobre Rykard» ([EN-wiki] Sir Gideon Ofnir/dialogue; [YT] kZ4pC3lkIKU y fYz6wYgdZfw): «Praetor Rykard is the Lord of the Volcano Manor on Mt. Gelmir. He is a ruthless justiciar who commands a company of inquisitors, reviled for his serpentine demeanour. / The volcano, Mt. Gelmir, lies in the west of the Altus Plateau; the realm of the Erdtree. It was the stage of the most appalling battle in the entirety of the Shattering. / …Rykard has committed the grave sin of blasphemy. Marking himself as an enemy, never to be forgiven.» → español **NO VERIFICADO: parafrasear**.
  - JP: 法務官ライカード… 慈悲なき裁判官にして、責問吏たちの長。蛇のように忌み嫌われた男 («juez sin piedad y jefe de los inquisidores/interrogadores; un hombre aborrecido como una serpiente»). 法務官 = «magistrado/pretor».
- Que sus inquisidores torturaran **albinaúricos** (lo dicen [ES-wiki] y [EN-wiki] en el «Trasfondo») **no tiene cita**: **NO VERIFICADO**, no decirlo.

**(c) Tanith, la bailarina extranjera**
- **Máscara de consorte** ([EG] armaduras-p397; = Túnica de consorte p398): «Tiempo ha, cuando Rykard posó su mirada sobre Tanith, esta trabajaba como bailarina en un reino lejano. Rykard no tardó en hacerla su consorte. / Ella fue la única humana que permaneció a su lado cuando se transformó en la serpiente blasfema. / Fue entonces cuando Tanith realmente quedó cautivada por él.» (La máscara: «a imagen y semejanza de una reina extranjera».)
- **Castañuelas de bailarina** ([EG] objetos-p508; te las da Parches; Tanith las rechaza mientras come): «Su apasionado baile no oculta ningún arte de seducción, sino solo una digna belleza.» Que esa tierra sea **Ranah** es deducción de [EN-wiki] (página Ranah), no texto.

**(d) La blasfemia: se dejó devorar**
- **Recuerdo del blasfemo** ([EG] objetos-p507 = [ES-wiki]): «Rykard se transformó en una serpiente gigante capaz de devorar a sus presas para seguir creciendo y vivir eternamente "Lo entiendo. El camino de la blasfemia es largo y peligroso, por lo que no es posible recorrerlo si no se está listo para pecar".» (EN: «…that he might devour, grow, and live eternally. "I understand. The road of blasphemy is long and perilous. One cannot walk it unprepared to sin."» Quién dice la frase entre comillas: el juego no lo indica.)
- **Cetro de devorador** ([EG] armas-p76 = [ES-wiki]): «Cetro con forma de serpiente devorando el mundo. Esta arma se convertirá, algún día, en el símbolo del señor de la Blasfemia. […] Dicen que su diseño es una breve visión del futuro que tuvo Rykard en sus últimos momentos de vida, tras ser devorado por la gran serpiente.» (Lo suelta Bernahl.)
- **Camafeo del megalómano** ([EG] talismanes-p74): «Un talismán en el que aparece grabada la imagen severa del pretor Rykard, señor de la Mansión del Volcán. […] Cuando Rykard sucumbió a la herejía, tomar por la fuerza se convirtió en norma. Después de todo, los propios dioses lo hacían.» (**Ya usado en el video de los Sinluz**.)
- Por qué se rebela — **Tanith** tras el 2.º encargo ([EN-wiki], [FX]; [YT] jETSyfKxi20 3:18–4:18): «Our Lord, indignant, has refused. To scurry about, fighting over what miserly scraps they allow us. If the Erdtree, and indeed the very gods, would debase us so, then we are willing to raise the banner of resistance, even if it means heresy.» → parafrasear.

**(e) Su línea famosa (la única verificada en español)**
- Cinemática de la fase 2, **español [ES-wiki]** (cita en la ficha): «**Únete a la familia del Rey Serpiente. ¡Juntos devoraremos a los dioses!**»
- EN ([EN-wiki] dialogue, [FX]): «Hmm... / Very well. / You... / Join the Serpent King, as family... / Together, we will devour the very gods!» Si te mata: «Now, we can devour the gods together!» Al morir: «No one will hold me captive. / A serpent never dies. / Ha ha ha...» → las de muerte, **español NO VERIFICADO**.
- JP de la muerte: …何者も、我を律せられぬ / 蛇は、不滅よ («nadie puede someterme a la ley / la serpiente es inmortal»). Ironía para el guion: **律** es «ley/norma» — el antiguo juez dice que ya nadie puede juzgarlo (lectura del narrador, no de la wiki).
- **Recortado, NO está en el juego** ([EN-wiki] {{cut}}): «A fine sacrifice indeed… Now you are family.», «O shapers of gods, meddlers in fortune. I do not abide! By your suffocating Order.» y «Eveligne, show him the way... to devour the gods» (Eveligne sería el nombre de la serpiente en una versión descartada). Solo como dato curioso, diciendo que es material cortado.

**(f) URLs**
- https://eldenring.fandom.com/es/wiki/Rykard,_señor_de_la_Blasfemia · …/Gran_Runa_de_Rykard · …/Recuerdo_del_blasfemo · …/Serpiente_devoradioses · …/Cetro_de_devorador · …/Tanith · …/Rya · …/Mansión_del_Volcán · …/Monte_Gelmir · …/Caballero_Bernahl · …/Vírgenes_raptoras
- https://eldenring.fandom.com/wiki/Rykard,_Lord_of_Blasphemy · …/Rykard,_Lord_of_Blasphemy/dialogue · …/Tanith,_Volcano_Manor_Proprietress · …/Rya_the_Scout · …/Knight_Bernahl · …/Patches · …/Sir_Gideon_Ofnir,_the_All-Knowing/dialogue · …/Volcano_Manor_Apparition · …/Stranded_Souls · …/God-Devouring_Serpent · …/Assault_on_Volcano_Manor
- https://www.eliteguias.com/guias/e/er/elden-ring_objetos-p506.php · …objetos-p507.php · …armas-p76.php · …talismanes-p74.php · …armaduras-p397.php · …armaduras-p328.php · …hechizos-p62.php

---

## 2. CANDIDATAS (12), cada una con veredicto

### C1. El pretor y su inquisición: tortura antes de la blasfemia ✅ CONFIRMADO (material nuevo para el canal)
**Qué dicen las fuentes**
- Gideon (arriba, §1b): «ruthless justiciar who commands a company of inquisitors, reviled for his serpentine demeanour».
- **Candelabro de inquisidor** ([EG] armas-p200): «Instrumento de tortura utilizado en secreto contra nobles en la Mansión del Volcán del monte Gelmir. / Sus numerosas púas atraviesan la carne antes de hacerla arder con las llamas del arma. El olor a sangre quemada provocaba la desesperación de la víctima. Un candelabro concebido por una mente meticulosa.»
  - EN: «Instrument of torture used on nobles behind the curtain at the Volcano Manor…» · JP: ゲルミアの火山館、その隠された裏側で («en la cara oculta de la Mansión del Volcán»). Lo sueltan las **Vírgenes raptoras** (jefe doble) ([ES-wiki] Vírgenes raptoras: «suelta Candelabro de inquisidor»; [EG] jefazos-p72: recompensa «Candelabro de inquisidor»).
- **Rueda de Ghiza** ([EG] armas-p232; errata «adoptóñ»): «Gran rueda de hierro revestida de cuchillas que desgarran la carne. / Es un instrumento de tortura usado por el inquisidor Ghiza. El giro de la rueda provoca fuertes dolores y hemorragia. / Su diseño se adoptó para usarlo en las emblemáticas armas blandidas por las vírgenes de hierro.»
- El inquisidor Ghiza **te invade dentro de la Mansión del Volcán** ([EN-wiki] Inquisitor Ghiza: «Invades within the room upstairs near the Site of Grace»; [YT] wdGZrHkRv4M capítulo «INQUISITOR GHIZA» 22:54). Su ropa: **Máscara ensangrentada** ([EG] armaduras-p373): «Máscara hecha a partir de vendas muy ceñidas y empapadas en sangre. / Incluso la cobertura más macabra resulta más atractiva que la cara supurante que oculta debajo.» **Atuendo de oficial** ([EG] armaduras-p382; errata «Contro» = Control; EN «Surveillance»): «Túnica azul mugrienta que llevan los oficiales autorizados para desempeñar su macabro oficio. / [Control], ejecuciones, rituales truculentos... Las tareas más oscuras mueven los engranajes de la humanidad.»
- Dentro de la mansión hay una gracia llamada **Iglesia de la ciudad de los penados** y otra **Cámara subterránea de la inquisición** ([EG] gracia). Los nombres ya cuentan para qué servía la casa.
- **Dato curioso con aviso (versión 1.00, texto cambiado después)**: el Pesar de Daedicar decía originalmente ([EN-wiki] Daedicar's Woe, Trivia, marcado {{cut}}): «…This soft-featured man's name was Daedicar, and he was one of Captain Rykard's paramours, as well an attendant in his Inquisition. He would test new methods of torture first upon himself, making a gift of his pain and first-hand knowledge to the one he loved.» JP: 長官ライカードの妾の一人であり 拷問官としての彼の助手. **Solo lo afirma la wiki inglesa; no lo pude cotejar con otra fuente → NO VERIFICADO.** Si se usa, decir «según la wiki, en la primera versión del juego…».
- **Lo que ignoraste:** antes de ser el villano blasfemo, Rykard era **la ley**: el juez de las Tierras Intermedias tenía su propia compañía de torturadores, y la mansión elegante del volcán tenía «en secreto» un candelabro para quemar nobles y una iglesia para penados.
- **URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_armas-p200.php · …armas-p232.php · …armaduras-p373.php · …armaduras-p382.php · https://eldenring.fandom.com/wiki/Inquisitor%27s_Girandole · https://eldenring.fandom.com/wiki/Ghiza%27s_Wheel · https://eldenring.fandom.com/wiki/Inquisitor_Ghiza · https://eldenring.fandom.com/wiki/Daedicar%27s_Woe

### C2. Las vírgenes raptoras: secuestro a domicilio hasta la cámara de la inquisición ✅ CONFIRMADO con matiz
- **Parches** en la Academia ([EN-wiki] Patches; [FX]; [YT] 0U52CsjKPrY 0:10–0:42): «Have you ever seen an iron virgin? The clunky contraptions are whirlwinds of sickles and spiked wheels. ...but long ago, they were endowed with a spell of transposition. And get this. A surviving virgin sits at the bottom of the big waterwheel in the Academy of Raya Lucaria. Its transpositional powers fully intact. So, right, if you get caught in it on purpose... It'll chuck you out straight at the base of the Erdtree... Or so I'm told...» → parafrasear.
- Lo que pasa de verdad (jugabilidad, [ES-wiki] Vírgenes raptoras; [EN-wiki] Subterranean Inquisition Chamber): la virgen te agarra **hasta matarte** y apareces en un área cerrada de la Mansión del Volcán, la **Cámara subterránea de la inquisición**; no puedes teletransportarte fuera hasta vencer al jefe (**dos Vírgenes raptoras**, una con ruedas dentadas y otra con guadañas pendulares) y salir al monte Gelmir.
- Parches después ([EN-wiki]; [YT] 0U52CsjKPrY 0:53–1:23): «I spoke no lie, not a one. You were trapped inside a volcano, no mistake, but the Erdtree was right outside. You just had to spring yourself out.»
- Dónde hay vírgenes ([EN-wiki] Abductor Virgin, lista de ubicaciones): Liurnia, Mansión de los Caria, Academia de Raya Lucaria, monte Gelmir, Afueras de la capital, Leyndell, Mansión del Volcán. (En el DLC también hay un par en el **Fuerte de la reprimenda**, [EG] jefazos-p72; sin texto que lo relacione con Rykard.)
- Cómo atacan ([EN-wiki], descripción de jugabilidad): abren el pecho y te meten dentro con tentáculos con forma de serpiente; si sobrevives, te escupen.
- La pieza que conecta con Rykard: su arma **copia la rueda de tortura del inquisidor Ghiza** (Rueda de Ghiza, C1) y el jefe doble suelta el **Candelabro de inquisidor** de la mansión.
- **Matiz obligatorio:** el juego **no dice que Rykard construyera las vírgenes** (eso es interpretación de [EN-wiki]/[ES-wiki] en el trasfondo, apoyada solo en la cita de Parches). Tampoco dice textualmente «llevan gente a la mansión para interrogarla»: es lo que **ves** al dejarte atrapar. Decirlo así: «la máquina que te atrapa en la Academia te deja en la cámara de la inquisición de su mansión».
- Bonus de Parches en el monte Gelmir ([EN-wiki]; [YT] onpson1sZsI): te patea por un precipicio gritando «then stay away from the Volcano Manor!» y luego: «I heard the brutes there hunt Tarnished like animals.»
- **Lo que ignoraste:** el atajo «gratis» de Raya Lucaria es un **secuestro**: una máquina de tortura con «hechizo de transposición» que te mata y te deposita en la cámara de la inquisición de Rykard.
- **URLs:** https://eldenring.fandom.com/wiki/Abductor_Virgin · https://eldenring.fandom.com/wiki/Subterranean_Inquisition_Chamber · https://eldenring.fandom.com/es/wiki/Vírgenes_raptoras · https://www.eliteguias.com/guias/e/er/elden-ring_jefazos-p72.php

### C3. La guerra más espantosa de la Devastación… y el señor que se fue a la serpiente ✅ CONFIRMADO
- Gideon: «It was the stage of the most appalling battle in the entirety of the Shattering.» (§1b)
- **Monumento con espada** junto al Noveno campamento del monte Gelmir ([EN-wiki] Sword Monuments: «Near the Ninth Gelmir Campsite Site of Grace, in Mt. Gelmir»), **español [ES-wiki]** (nota del artículo de Rykard): «**El asalto a la Mansión del Volcán: / Lo sórdido, lo enfermizo, lo profano; / una guerra miserable interminable que no concede la gloria.**» EN: «The Assault on Volcano Manor / The squalid, the sick, the blasphemous; / a wretched, unending war with no glory». JP: 火山館攻略戦 / 穢れた者たち、疫病、冒涜 / 名誉なく、終わりもない惨戦. (Español con una sola fuente: cotejar con captura.)
- **Mapa: Monte Gelmir** ([EG] objetos-p435; errata «seencuentra»; = [ES-wiki]): «El monte Gelmir, en cuya cima se encuentra la Mansión del Volcán, se caracteriza por sus escarpados acantilados y su clima amenazador, peligros que se agudizan aún más tras la Devastación.»
- **Alma estancada** cerca de la entrada de la Mansión, Camino de la iniquidad ([EN-wiki] Stranded Souls): «Lord Rykard... If this putrid field of death is what your blasphemy would bring, then I can no longer abide. No one can.» JP: …誰も、お前には付いてゆかぬぞ («nadie te seguirá»). Otra, en el Fuerte Laiedd: «Eek...! The wretched fools... They'll never find me. […] I'll soon be back at the Volcano Manor.» → parafrasear.
- **Armadura de caballero de Gelmir** ([EG] armaduras-p329; **errata: empieza «Casco usado…»**, el EN dice «Armor worn…»): «[Armadura] usad[a] por los caballeros que antaño le eran leales al pretor Rykard. / Muestra un emblema que ya nadie usa, puesto que representa a un señor que empezó con nobles ambiciones pero acabó cayendo en una ávida depravación. / Al perder el señor su dignidad, estos caballeros también perdieron a su maestro.» (Se encuentra en la Tumba del héroe de Gelmir.)
- Se dejó devorar **runa incluida** (Gran Runa, §1a): en mitad de esa guerra, el semidiós le entregó su fragmento del Círculo a una serpiente.
- **Cazador de serpientes** ([EG] armas-p267): «Cuando las aspiraciones heroicas del señor degeneraron hasta convertirse en mera avaricia, sus hombres buscaron un arma con la que pudieran detenerlo.» Está **clavado en un montón de cadáveres** junto a la entrada de la arena ([EN-wiki] Rykard: «sticking out of a pile of corpses near the entrance to the arena»).
- **El fantasma de la mansión** (caballero de Gelmir, aparece tras recargar 3 veces; [EN-wiki] Volcano Manor Apparition; [YT] d7shRsbbjvI): «Someone, please, kill him... That horrendous serpent... Praetor Rykard...» / «Kill the great serpent. The one that devoured Praetor Rykard. I left the serpent-slaying spear in the Lord's Chamber.» / «Praetor Rykard's ambitions, though blasphemous, marked him a worthy sovereign. But they were reduced to gluttonous depravity, once he gave himself to the serpent. Whatever that thing is, it is no longer Praetor Rykard. Someone must kill him. To spare him, and his ambitions, from further dishonour.» Al vencer a Rykard, donde estaba arrodillado queda el gesto **«My Thanks»** ([EN-wiki]; nombre español **NO VERIFICADO**).
- Escenario que se puede mostrar (no texto): campamentos en ruinas por las laderas y soldados de Leyndell que siguen allí ([EN-wiki] Mt. Gelmir, descripción). Que **se volvieran caníbales o frenéticos «por los horrores»** es **interpretación de la wiki**: mostrar sin afirmar.
- Que el ejército atacante lo dirigiera **Morgott** es interpretación ([EN-wiki] Assault on Volcano Manor, infobox; [ES-wiki] Devastación «Rykard incluido»): **NO VERIFICADO** como texto.
- **Lo que ignoraste:** la batalla más espantosa de la guerra la sostuvo **su** ejército, y él la abandonó metiéndose en la boca de una serpiente con la Gran Runa puesta. Sus propios caballeros quitaron su emblema, buscaron un arma para matarlo, y uno se quedó como fantasma **pidiéndote a ti** que lo hicieras.
- **URLs:** https://eldenring.fandom.com/es/wiki/Rykard,_señor_de_la_Blasfemia (nota del monumento) · https://eldenring.fandom.com/wiki/Sword_Monuments · https://eldenring.fandom.com/wiki/Stranded_Souls · https://eldenring.fandom.com/wiki/Volcano_Manor_Apparition · https://www.eliteguias.com/guias/e/er/elden-ring_armaduras-p329.php · …armas-p267.php · …objetos-p435.php

### C4. Los hijos del ritual: los hombres serpiente y Zorayas ✅ CONFIRMADO (ángulo nuevo; el tónico ya se contó)
- **Cenizas de hombre serpiente** ([EG] cenizas-espiritus-p53): «Espíritu de un hombre serpiente deformado que empuña un látigo de magma. / Se dice que, hace mucho tiempo, la anciana serpiente que habitaba en el Monte Gelmir devoró a un semidiós, lo cual provocó el nacimiento de los hombres serpiente.»
- **Amnios de serpiente** ([EG] objetos-p461; está en el altar del **Templo de Eiglay**, tras el Noble sacrodermo, [ES-wiki] Rya): «Amnios del útero que albergó este pobre vástago no deseado fruto de un repulsivo ritual de parto. / Permanece siempre húmedo y jamás llegará a secarse.»
- **Espada curva de dios serpiente** ([EG] armas-p119; erratas «empelada», «olvidad»): «Espada curva que presenta la imagen de una antigua deidad con forma de serpiente. Herramienta [empleada] en una religión [olvidada] que se practicaba en el Monte Gelmir. / Aunque antes se usaba para ofrecer sacrificios, esta espada restaura PS al matar a un enemigo.» + Disparo de magma: Rykard **revivió** los maleficios de esa religión (§1a).
- **Ira de Gelmir** ([EG] hechizos-p63; errata «creador»; premio de Bernahl): «Este hechizo se lanza en representación de la furia del volcán, pero la arrogancia de intentar dominarlo es propio únicamente de hombres y víboras.»
- **Rya / Zorayas** ([EN-wiki] Rya the Scout; [FX]; [YT] 5IkIEt8YlW4):
  - Recluta Sinluz despiadados: «You are very brave yourself. Not only a steady hand, but a steady heart, merciless, even to your own kind. Such strength is precisely what my mistress seeks.» (1:56–2:25)
  - Oye ruidos: «Something beyond the walls, like breathing, or slithering scales...» (5:38–5:56)
  - Su forma real: «Goodness, am I still a serpent? […] This is my true form. My real name is Zorayas.» (6:06–6:53) · «Lady Tanith is my mother. I am told I was born by the grace of a glorious king.» (6:56)
  - Con el amnios: «I am certain of it. I was born inside this. It's a part of my birth mother.» (9:01–9:23)
  - El final: «I was an unwanted child. Born not of grace, but of a hideous ritual. Something that can never be accepted, not by men, nor serpents. Even Lady Tanith shouldn't accept me. […] Kill me, please. […] Free me from this accursed frame.» (9:52–10:36) · Si la matas: «Thank you... My champion... Mother...» (10:49)
  - **Carta de Zorayas** ([EG] objetos-p465; errata «nflexible»), si no la matas ni le das el tónico: «"Deseo emprender un viaje. / De ese modo, algún día, podré continuar el trabajo de mi madre. / Podré ser la orgullosa hija de Tanith de la Mansión del Volcán. / Adiós. / Siempre has sido tan amable, tan [inflexible]... / Mi adalid".»
- **Tanith** cuando Rya descubre la verdad ([EN-wiki]): «That some things are better left unknown. Besides, no-one should be blamed for their heritage.»
- **Pesar de Daedicar** (madre «de una infinidad de grotescos hijos») y el **Tónico del olvido**: **ya contados en el video de los Sinluz** (ver §8). Que Daedicar sea la madre de Rya lo «implica» la wiki: **interpretación**.
- Diseño (arte conceptual, [EN-wiki] God-Devouring Serpent, Trivia): la serpiente devorando a Rykard «poco después de salir del huevo», con dos huevos más en una bandeja de plata. **Es arte conceptual, no juego.**
- **Lo que ignoraste:** la blasfemia de Rykard no se quedó en él: de «un semidiós devorado» salió una **especie entera** de hombres serpiente, nacidos de «un repulsivo ritual de parto». Una de esas criaturas creció creyéndose hija «de un rey glorioso» y, cuando supo la verdad, su única petición fue que la mataras.
- **URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_cenizas-espiritus-p53.php · …objetos-p461.php · …armas-p119.php · …hechizos-p63.php · …objetos-p465.php · https://eldenring.fandom.com/wiki/Rya_the_Scout · https://eldenring.fandom.com/wiki/Temple_of_Eiglay

### C5. La noche del complot: le pagaron por la muerte de Godwyn ✅ CONFIRMADO (el texto existe; el papel exacto de Rykard no se dice)
- **Garra blasfema** ([EG] objetos-p550): «Una losa grabada con los restos de la Runa de la Muerte. / Puede desviar el poder de la hoja negra. / **En la noche del complot, Ranni recompensó con estos restos al pretor Rykard.** Si algún día se revela el allanamiento, servirán como último recurso y permitirán a Rykard desafiar a Maliketh, la Hoja Negra, la oscura bestia de la Muerte Escrita.»
  - EN ([EN-wiki]): «On the night of the dire plot, Ranni rewarded Praetor Rykard with these traces. Should the coming trespass one day transpire, they would serve as a last-resort foil, allowing Rykard to challenge Maliketh the Black Blade, the black beast of Destined Death.»
  - JP: 陰謀の夜、法務官ライカードはラニから**謝礼**として片鱗を貰い受けた — 謝礼 = «pago/remuneración en agradecimiento». / いつか来る**冒涜**の時 — donde el inglés dice «trespass» y el español «allanamiento», el japonés dice **«el día de la blasfemia»**.
- Quién la tiene: **Bernahl** te invade en Farum Azula, la ciudad en ruinas (al norte del Gran puente) y la suelta al morir ([ES-wiki] Caballero Bernahl; [EN-wiki] Blasphemous Claw: solo si completaste su misión en la Mansión y venciste a Rykard). La usas contra **Maliketh** para desviar su espada.
- Qué fue esa noche (contexto, ya usado en el video de Ranni): **Rogier** ([ES-wiki] Noche de los Puñales Negros, cita en español): «Ocurrió durante la época dorada del Árbol Áureo, mucho antes de la destrucción del Círculo de Elden. Alguien robó un fragmento de la Runa de la Muerte a Maliketh, la Hoja Negra. Y una noche funesta, asesinó a Godwyn, el Dorado.»
- **Bernahl**, tras la muerte de Rykard ([EN-wiki]; [YT] Ifw3P9rXaRY 0:03–0:56): «So. You killed Rykard? I harbour you no ill will. The strong take. Such is our code. Even he was prepared to meet a wretched end when he first took blasphemy unto his very flesh. […] O Greater Will, hear my voice. I am the recusant Bernahl, inheritor of my brother's will, and you will fall to my blade.» (De qué «hermano» habla: el juego no lo dice.)
- **Matiz obligatorio:** el texto dice que **Ranni le pagó esa noche**. No dice qué hizo Rykard (ni que empuñara un cuchillo). Formularlo como pregunta: «¿qué hizo para cobrar?».
- **Lo que ignoraste:** la herramienta que usaste para vencer a Maliketh es **la propina de Rykard por la noche en que murió Godwyn**, el primer semidiós en morir. El pretor ya conspiraba contra los dioses **antes** de la Devastación, y cobró en Runa de la Muerte para que, el día que la Muerte viniera a por él, pudiera pelearle.
- **URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_objetos-p550.php · https://eldenring.fandom.com/wiki/Blasphemous_Claw · https://eldenring.fandom.com/es/wiki/Noche_de_los_Puñales_Negros · https://eldenring.fandom.com/wiki/Knight_Bernahl

### C6. Devorar a sus campeones (la audiencia) ⚠ YA CONTADO (video de los Sinluz) — solo detalles nuevos como apoyo
- Nuevo para el canal: **Hoja blasfema** ([EG] armas-p268; errata «Aborberás»): «Arma sagrada de Rykard, señor de la Blasfemia. / Los restos de la infinidad de héroes a los que ha devorado se retuercen en la superficie de esta espada. / Ahora, comparten la misma sangre y están unidos como familia.» (Rykard la **saca de la boca de la serpiente** en la cinemática, [EN-wiki] Notes.)
- Tanith tras el 2.º encargo ([EN-wiki]; [YT] jETSyfKxi20 4:09–4:18): «If you follow this heroic path, one day the Lord will see you. The Lord's visits with our champions are always a spectacle.»
- En la arena: un cadáver con el **Sobretodo ocular** ([EG] armaduras-p396: «La insignia de la parte delantera designa a su portador como los ojos y oídos de Sir Gideon el Omnisciente»; ubicación: [EN-wiki] Gideon Notes / [ES-wiki] Gideon) → **el espía de Gideon también acabó en el menú**. Y el montón de cadáveres con el Cazador de serpientes (C3).
- Ya contado: Rencor de Rykard («El señor les concedió audiencia…»), Tanith comiéndose el cadáver, Camafeo, los 3 contratos.

### C7. Reclutar Sinluz para cazar a los suyos ⚠ ÁNGULO PARCIALMENTE CONTADO (contratos = video Sinluz)
- Nuevo: **Dedo Recusante** ([EG] objetos-p456; erratas «Manisón», «se ha convertido»): «Este dedo doblado está cubierto por escamas de serpiente. / Una reliquia del señor de la [Mansión] del Volcán llegada a los Sinluz que se [han] convertido en familia.» (EN: «An heirloom of the lord of the Volcano Manor, bequeathed to Tarnished who have become family.») → para invadir a otros jugadores **se usa un dedo con escamas de Rykard**.
- Bernahl ([EN-wiki]; [YT] s5GcSDwAokc 2:10–3:57): «The Volcano Manor is a pit of recusants who spit at grace and hunt our own kind.» / «To raise the flag of revolt against this sanctified pillaging, we recusants must become the most wretched of predators.»
- Tanith al empezar ([EN-wiki]; [YT] oFgdDACMA0M 0:10–0:14, sin invitación): «Fascinating. And not unlike another guest we had long ago…» (A quién se refiere: no se dice.)
- Uso: cameo para el gancho o para el n.º 4 (Parches: «hunt Tarnished like animals»).

### C8. Tanith se come el cadáver ❌ YA CONTADO (video Sinluz, p4b) — solo como guiño
- Tanith ([EN-wiki]; [FX]; [YT] sJ3hbEi9loA 0:09–0:32): «Our Lord's carcass is vast, and not easily consumed. Dear Rykard, please find purchase within me, I wish to be your serpent; your family.» Si le das las castañuelas: «I have no need of that. I must continue devouring my beloved lord...» ([YT] zC7c-DiAJPY 0:40–0:45) ← **este detalle no se usó**: cameo posible.
- Lo nuevo y útil para el cierre: Tanith tras tu victoria ([EN-wiki]; [YT] ClYjAC9k01g 0:04–0:32): «Our Lord was yet weak. You have taught us that. Defeat is not the end. Our Lord is immortal, and will one day rise again, stronger.» Y si vuelves a hablarle ([EN-wiki]; en los subtítulos de ese clip **no aparece**, segundo NO VERIFICADO): «Here is my thanks. For allowing our Lord to be revived, even stronger than before.»

### C9. La guerra contra los dioses / la Orden Dorada ⚠ MARCO, no atrocidad
- Tanith («heresy»), Bernahl («O Greater Will…»), Gideon («grave sin of blasphemy»), Camafeo. Sirve de hilo conductor y para el gancho; como puesto es abstracto.

### C10. Gigantes / Eiglay ❌ DESCARTAR
- **Gigantes**: no encontré ningún texto que ligue a Rykard con los gigantes; lo único es que el 3.er contrato (Juno Hoslow) está en los Picos de los gigantes (Carta roja, [EG] objetos-p458) — ya contado.
- **Eiglay**: solo el nombre del **Templo de Eiglay** (iglesia de la mansión dedicada a la serpiente, con una piel de serpiente mudada sobre el altar, según [EN-wiki]: «the shed skin of a great serpent suspended over its foul altar» — descripción de escenario). Nada más.

### C11. Patches, el estafador ⚠ CAMEO
- Te patea del acantilado (C2) y al final ([EN-wiki]; [FX]; [YT] ijNdEQdToEs 0:00–0:33): «The demigod beast is slain, and Tanith has lost her head. A fine mess, but how else could it end when daddy ambition is head over heels courting lady blasphemy.» → remate perfecto para un puesto.

### C12. Otros que no dan para puesto
| Tema | Veredicto | Dato |
|---|---|---|
| Rykard construyó las vírgenes de hierro | ❌ Interpretación de las wikis | Sin texto; ver C2 |
| Inquisidores torturaban albinaúricos | ❌ Sin cita | Ver §1b |
| Morgott dirigió el asalto | ❌ Interpretación | Ver C3 |
| *Ringed Finger* hecho del dedo de Rykard | ❌ Solo en la versión china 1.00 según [EN-wiki] ({{cut}}) | Nombre español: **Dedo anillado** ([EG]) — no usar |
| *Red Insignia* de Tanith | ❌ Contenido recortado | — |
| Jori, inquisidor anciano (DLC) | ❌ Es un cornamentado de Enir-Ilim, no de Rykard ([EN-wiki] Jori) | — |
| Daedicar varón e inquisidor | ⚠ Texto de la v1.00, solo [EN-wiki] | Ver C1 |

---

## 3. Citas listas para usar (estado de verificación)

| Cita | Idioma | Estado |
|---|---|---|
| «Únete a la familia del Rey Serpiente. ¡Juntos devoraremos a los dioses!» | ES | ✅ textual [ES-wiki] (única línea de Rykard en español verificada) |
| «Join the Serpent King, as family... Together, we will devour the very gods!» | EN | ✅ [EN-wiki] + [FX] + [WH] |
| «No one will hold me captive. A serpent never dies.» | EN | ✅ [EN-wiki] + [FX] + [WH]; español **NO VERIFICADO** |
| Gran Runa de Rykard: «…se ofreció como alimento a la serpiente blasfema, runa incluida.» | ES | ✅ [EG] = [ES-wiki] (errata «semidió sadoptivo» en [EG]) |
| Recuerdo del blasfemo: «…devorar a sus presas para seguir creciendo y vivir eternamente…» + «El camino de la blasfemia es largo y peligroso…» | ES | ✅ [EG] = [ES-wiki] |
| Cetro de devorador: «…una breve visión del futuro que tuvo Rykard en sus últimos momentos de vida, tras ser devorado por la gran serpiente.» | ES | ✅ [EG] = [ES-wiki] |
| Garra blasfema: «En la noche del complot, Ranni recompensó con estos restos al pretor Rykard…» | ES | ✅ [EG] (una fuente española; EN y JP coinciden) |
| Candelabro de inquisidor: «Instrumento de tortura utilizado en secreto contra nobles en la Mansión del Volcán…» | ES | ✅ [EG] |
| Rueda de Ghiza: «…instrumento de tortura usado por el inquisidor Ghiza… Su diseño se adoptó para… las vírgenes de hierro.» | ES | ✅ [EG] (errata «adoptóñ») |
| Máscara ensangrentada / Atuendo de oficial | ES | ✅ [EG] (errata «Contro») |
| Cazador de serpientes: «…sus hombres buscaron un arma con la que pudieran detenerlo.» | ES | ✅ [EG] |
| Armadura de caballero de Gelmir: «…un señor que empezó con nobles ambiciones pero acabó cayendo en una ávida depravación…» | ES | ✅ [EG] (errata: empieza «Casco usado») |
| Casco de caballero de Gelmir: «…símbolo del pedigrí de Rykard como hijo del señor Radagon.» | ES | ✅ [EG] |
| Monumento: «El asalto a la Mansión del Volcán: Lo sórdido, lo enfermizo, lo profano; una guerra miserable interminable que no concede la gloria.» | ES | ✅ [ES-wiki] (una fuente; cotejar con captura) |
| Mapa: Monte Gelmir «…peligros que se agudizan aún más tras la Devastación.» | ES | ✅ [EG] = [ES-wiki] |
| Cenizas de hombre serpiente: «…devoró a un semidiós, lo cual provocó el nacimiento de los hombres serpiente.» | ES | ✅ [EG] |
| Amnios de serpiente: «…pobre vástago no deseado fruto de un repulsivo ritual de parto.» | ES | ✅ [EG] |
| Espada curva de dios serpiente: «Aunque antes se usaba para ofrecer sacrificios…» | ES | ✅ [EG] (erratas «empelada», «olvidad») |
| Disparo de magma / Ira de Gelmir | ES | ✅ [EG] (errata «creador» en Ira) |
| Hoja blasfema: «Los restos de la infinidad de héroes a los que ha devorado se retuercen…» | ES | ✅ [EG] |
| Dedo Recusante: «…cubierto por escamas de serpiente. Una reliquia del señor de la Mansión del Volcán…» | ES | ✅ [EG] (erratas «Manisón», «se ha») |
| Carta de Zorayas | ES | ✅ [EG] (errata «nflexible») |
| Máscara/Túnica de consorte, Castañuelas de bailarina | ES | ✅ [EG] |
| Gideon: «ruthless justiciar who commands a company of inquisitors… most appalling battle… grave sin of blasphemy» | EN | ✅ [EN-wiki] + [YT]; **parafrasear** |
| Fantasma: «Someone, please, kill him…» / «Whatever that thing is, it is no longer Praetor Rykard…» | EN | ✅ [EN-wiki] + [YT]; **parafrasear** |
| Alma estancada: «If this putrid field of death is what your blasphemy would bring, then I can no longer abide. No one can.» | EN | ✅ [EN-wiki]; **parafrasear** |
| Rya: «I was an unwanted child. Born not of grace, but of a hideous ritual… Kill me, please.» | EN | ✅ [EN-wiki] + [FX] + [YT]; **parafrasear** |
| Parches: iron virgin «spell of transposition» / «trapped inside a volcano» / «hunt Tarnished like animals» / «daddy ambition… lady blasphemy» | EN | ✅ [EN-wiki] + [FX] + [YT]; **parafrasear** |
| Bernahl: «Even he was prepared to meet a wretched end when he first took blasphemy unto his very flesh.» | EN | ✅ [EN-wiki] + [YT] + [WH]; **parafrasear** |
| Tanith: «The Lord's visits with our champions are always a spectacle.» / «Our Lord is immortal…» | EN | ✅ [EN-wiki] + [YT]; **parafrasear** |
| Rogier: «…Alguien robó un fragmento de la Runa de la Muerte a Maliketh, la Hoja Negra. Y una noche funesta, asesinó a Godwyn, el Dorado.» | ES | ✅ [ES-wiki] |
| Pesar de Daedicar v1.00 (amante e inquisidor) | EN | ⚠ solo [EN-wiki] (texto retirado del juego) |
| Resto de diálogos en español (Tanith, Rya, Bernahl, Parches, Gideon, fantasma, muerte de Rykard) | ES | **NO VERIFICADO** (el juego no tiene doblaje en español; solo subtítulos en pantalla, no transcritos en ninguna fuente que encontrara) |

---

## 4. Lugares para MAPAS (coordenadas x,y medidas en `mapas/mundo_rejilla.jpg`, rejilla 0-1)

Medidas hoy sobre `mundo_rejilla.jpg` (1920×1815) y sobre un recorte ampliado de `mundo.jpg` con rejilla de 0,01. La Mansión del Volcán la identifiqué comparando la forma del cráter con el mapa oficial de la mazmorra (`File:ER Legacy Dungeon Map Volcano Manor.jpg`, [EN-wiki]): coincide con el complejo de edificios dentro de la lava.

| Lugar | x, y (rejilla) | Ligado a | Fiabilidad |
|---|---|---|---|
| **Mansión del Volcán** (complejo en la lava del cráter) | **0,228 , 0,325** (caja x 0,21–0,245 · y 0,31–0,34) | C1, C2, C3, C4, C6 | ✅ cotejada con el mapa de mazmorra |
| **Monte Gelmir** (zona del volcán) | centro **0,235 , 0,31** · caja aprox. x 0,19–0,27 · y 0,26–0,36 | C3 | ⚠ límites aproximados (el juego lo sitúa «en el oeste de la Meseta Altus», [EN-wiki]/[ES-wiki]) |
| Meseta Altus (rótulo de región) | 0,33 , 0,33 | Contexto | ⚠ aproximado |
| **Leyndell, capital del Reino** (el ejército que asedia) | 0,44 , 0,37 · Árbol Áureo 0,48 , 0,41 | C3 | ⚠ por forma (ciudad amurallada junto al Árbol) |
| **Academia de Raya Lucaria** (virgen raptora bajo la noria) | **0,195 , 0,540** (isla amurallada con puente al norte) | C2 | ✅ por forma |
| **Mansión de los Caria** (también hay vírgenes) | 0,19 , 0,405 | C2 (opcional) | ⚠ por forma; confirmar |
| Liurnia, tierra encharcada (Rya en el cenador) | 0,22 , 0,52 (lago) | C4 | ⚠ región |
| **Farum Azula, la ciudad en ruinas** (Bernahl suelta la Garra) | 0,87 , 0,48 (remolino al este) | C5 | ⚠ por forma |
| Castillo sombrío (contrato de Rileigh; ya contado) | 0,295 , 0,30 (castillo con foso verde) | — | ⚠ por forma; confirmar |
| Picos de los gigantes | 0,60 , 0,25 | §9 | ⚠ región |
| **Tumba del héroe de Gelmir** | **NO VERIFICADO** (sé que está en los acantilados del monte Gelmir, [EN-wiki]; no encontré su marcador en el mapa sin iconos) | C3 (armadura de los caballeros) | ❌ no medido |
| Monumento del asalto (Noveno campamento del monte Gelmir) | **NO VERIFICADO** dentro del Gelmir | C3 | ❌ no medido |
| Reino de las Sombras (DLC) | **Fuera del mapa** (flecha saliendo del borde) | §9 | — |

---

## 5. ESCENAS IMPORTANTES y clips (solo ids y segundos; nada de video descargado)

Canales evitados: Fextralife, IGN, PowerPyx, Gamerpillar, VaatiVidya, Zullie, cad5150, ConCon, **Shirrako** (salió en casi todas las búsquedas: NS6BWRTrrZU, 7Zw-yTeouLQ — no usar). Marcas de tiempo: **[CAP]** = capítulo del video; **[YT]** = subtítulos automáticos; **[WH]** = Whisper sobre el audio (±2-3 s). **Revisar marca de agua y rótulos de cada canal antes de usarlo** (no lo comprobé visualmente).

| Escena | Video (id · canal · duración) | Momento |
|---|---|---|
| **Cinemática fase 2: Rykard despierta y saca la espada de la boca de la serpiente** («Very well… Join the Serpent King, as family… Together, we will devour the very gods!») | **eljrH9jvANE** · pgp · 76 s · «Rykard Transformation Cinematic Cutscene (4K)» | **~0:31–0:34 «Very well»; ~1:02–1:06 «Join the Serpent King, as family»; ~1:06–1:12 «Together, we will devour the very gods!»** [WH]. El video entero es la cinemática |
| Misma cinemática + combate + muerte, 4K sin comentarios | **yjnnv3ib_t4** · VynPlays · 241 s | ~1:47 «Very well»; **~2:15–2:21 «Join the Serpent King…»; ~2:21–2:27 «…devour the very gods!»**; **~3:42–3:51 «No one will hold me captive. A serpent never dies.»** [WH] |
| Combate completo + diálogos posteriores (Tanith y Bernahl) | **bVWauAYPe60** · SourceSpy91 · Part 30 · 719 s | ~3:30–3:53 cinemática («Very well»); ~4:23 «Join…»; ~6:24–6:37 muerte de Rykard; **8:23–9:13 Tanith «It's true then… Our lord was yet weak… I always was an admirer»; 9:19–10:16 Bernahl «So, you killed Rykard… The strong take… Even he was prepared to meet a wretched end… rise against the Erdtree»** [WH] (en el tramo central Whisper repite frases: cotejar al oído) |
| Cinemáticas alternativas (Rykard) | RMgTDRMEoMA · wuh1 · 79 s · XQd7QcRsZYI · sirmicho · 79 s · UpyfTpUbH24 · GeordaneGaming · 72 s | Video entero = cinemática (segundos **NO VERIFICADOS**) |
| Muerte, línea suelta | rC573QqNaCo · (canal sin dato) · 6 s «Death Voice Line» | Completo (**NO VERIFICADO** contenido) |
| **Tanith comiéndose a Rykard** (guiño; ya contado) | **sJ3hbEi9loA** · Games from Mars · 65 s | 0:09 «Oh, you»; **0:11–0:19 «Our lord's carcass is vast and not easily consumed»; 0:20–0:32 «please find purchase within me… your serpent, your family… devour the gods together»** [YT] |
| Tanith rechaza las castañuelas mientras come | **zC7c-DiAJPY** · Zach CK · 84 s | **0:40–0:45 «I have no need of that. I must continue devouring my beloved lord»**; 0:52–1:13 diálogo de comer [YT] |
| Tanith tras tu victoria | **ClYjAC9k01g** · Terry Goodwin · 74 s | 0:04–0:32 «It's true then… Our lord was yet weak… Our lord is immortal, and will one day rise again, stronger»; 0:42–0:49 «The champion who walks the tainted path shines all the more. I always was an admirer» [YT] |
| Tanith te recibe / «otro invitado hace mucho» / «Rise with us, against the Erdtree» | **oFgdDACMA0M** · Terry Goodwin · 97 s | 0:10–0:14 «not unlike another guest we had long ago»; 0:30–0:32 «Rise with us, against the Erdtree» [YT] |
| Tanith: «no place for the meek» (ya usado) | JXeTD3mJEII · Terry Goodwin · 52 s | 0:13–0:24 [YT] |
| Tanith: la verdad sobre Rykard / «always a spectacle» / el tónico | **jETSyfKxi20** · Stratek · 586 s (compilación) | 3:18 «true ruler of this manor»; 3:35–3:58 «crumbs… indignant… miserly scraps… even if it means heresy»; **4:09–4:18 «heroic path… always a spectacle»**; 5:59–6:07 tónico; 6:37–6:46 «I will never be a good mother» [YT] |
| **Rya / Zorayas** (forma de serpiente, amnios, «Kill me, please») | **5IkIEt8YlW4** · Sunless_Solaire · 776 s · «Rya All Dialogue - HQ Audio» | 1:56–2:25 «merciless, even to your own kind»; 5:38–5:56 ruidos en las paredes; **6:06–6:53 «am I still a serpent?… My real name is Zorayas»**; 6:56–7:00 «born by the grace of a glorious king»; 9:01–9:23 amnios; **9:52–10:36 «unwanted child… hideous ritual… Kill me, please»**; 10:49–10:52 «Thank you… my champion… Mother» [YT]. **Es audio de diálogo: comprobar si hay imagen útil** |
| Rya (historia montada, alternativa) | tX0JFlnF6mQ · Lost Cinematics · 653 s | **NO VERIFICADO** (posible montaje con rótulos) |
| **Fantasma de la mansión** («Someone, please, kill him») | **d7shRsbbjvI** · Terry Goodwin · 140 s | **0:05–0:12 «Someone, please, kill him… that horrendous serpent… Praetor Rykard»**; 0:29–0:40 «Kill the great serpent… I left the serpent-slaying spear in the Lord's Chamber»; 0:58–1:11 «ambitions… worthy sovereign… gluttonous depravity»; **1:15–1:34 «Whatever that thing is, it is no longer Praetor Rykard. Someone must kill him…»** [YT] |
| Fantasma (alternativa) | RLTgn4G42qs · Gallvanos · 132 s | 0:07–0:14; 1:19–1:37 [YT] |
| **Gideon «Sobre Rykard»** | **kZ4pC3lkIKU** · Soul Cat · 36 s · fYz6wYgdZfw · Kevin B (Peace and Love) · 34 s | kZ4: **0:01–0:12 «Praetor Rykard… ruthless justiciar… company of inquisitors… serpentine demeanour»; 0:21–0:24 «most appalling battle»; 0:27–0:34 «grave sin of blasphemy… never to be forgiven»** [YT] |
| **Bernahl tras la muerte de Rykard** | **Ifw3P9rXaRY** · Terry Goodwin · 75 s | 0:03 «So, you killed Rykard»; 0:09–0:11 «The strong take. Such is our code»; **0:13–0:18 «Even he was prepared to meet a wretched end when he first took blasphemy unto his very flesh»**; 0:39–0:56 «O Greater Will… inheritor of my brother's will…» [YT] |
| Bernahl: «pit of recusants» / «wretched of predators» | s5GcSDwAokc · Stratek · 351 s | 2:10–2:13; 3:50–3:57 [YT] |
| Bernahl invade en Farum Azula (suelta la Garra blasfema) | zcj3vSb5KyM · Soul Cat · 229 s · 0ume4hyz0cE · Soul Cat · 210 s («Old Lord's Talisman and Blasphemous Claw…») | **NO VERIFICADO** el segundo |
| **Parches: la virgen de hierro de Raya Lucaria** (antes y después) | **0U52CsjKPrY** · Stratek · 87 s | **0:10–0:42 «Have you ever seen an iron virgin?… spell of transposition… bottom of the big waterwheel… chuck you out straight at the base of the Erdtree… or so I'm told»; 0:53–1:23 «I spoke no lie… You were trapped inside a volcano»** [YT] |
| **La virgen te atrapa y apareces en la Mansión** | lXRPwD_6s2w · IAmToastMan · 126 s · yWDl221XY8U · ShyKatana · 147 s · **TxnoanwFw4g** · Aethersong · 745 s | Aethersong [CAP]: Academia **0:00–2:09**, Mansión del Volcán 2:09, «ENEMY FELLED» (jefe doble) **10:26**, Monte Gelmir 11:12. Los otros dos: segundo **NO VERIFICADO** |
| Jefe doble de Vírgenes raptoras | iOk8MMMWPo4 · PANxWAR · 261 s | Completo (**NO VERIFICADO**) |
| **Parches te patea del acantilado** | **onpson1sZsI** · Zero Manga Hunter · 71 s | **~0:53–0:55 «…then stay away from the Volcano Manor!»; ~0:59 «Bye now!»; ~1:04 «Take care!»** [WH] |
| Parches tras matar a Rykard («daddy ambition… lady blasphemy») | **ijNdEQdToEs** · SBG · 58 s | 0:00 «Now you've gone and killed Rykard»; 0:17–0:21 «this Manor is finished… Tanith has lost her head»; **0:24–0:30 «how else could it end when daddy ambition is head over heels courting lady blasphemy»** [YT] |
| Inquisidor Ghiza (invasión en la Mansión) | **wdGZrHkRv4M** · Kelvyn Acevedo · 1969 s (sin comentarios, con capítulos) · d7Lg5R8Np-4 · Jaemekon · 53 s | wdGZ [CAP]: Mansión 0:00; Tanith 3:10; Rya 9:10; Bernahl 9:35; misiones de Tanith 10:31; **Inquisidor Ghiza 22:54–23:51** |
| Mansión del Volcán completa (respaldo) | **YS1P-_MROO0** · SourceSpy91 · Part 29 · 4944 s · 7C8zVzHL9D8 · Eagle Bearer · 2398 s | Sin capítulos (**NO VERIFICADO**) |
| Longplay de respaldo | **HJ6EIysyst8** · SourceSpy91 · 81 h | [CAP] Academia de Raya Lucaria **19:55:18**; Mansión de los Caria 27:27:25; Monte Gelmir **52:41:39**; Misiones de asesinato de Tanith **55:44:18**; **Rykard 57:44:51–57:57:18**; Picos de los gigantes 63:30:29; Gigante de fuego 67:12:44 |
| Ecos de Márika (para §9) | GRH4LNXKQt8 · Games from Mars · 1424 s | Primera iglesia de Márika **14:23–15:10** según el dossier de Godfrey (no lo volví a medir hoy: **NO VERIFICADO hoy**) |

**Escenas que hay que mostrar y no son cinemática** (clip de juego o captura): el monumento del asalto junto al Noveno campamento; las almas estancadas del Camino de la iniquidad; el montón de cadáveres con el Cazador de serpientes en la entrada de la arena; el altar del Templo de Eiglay con la piel de serpiente; el retrato de Rykard en la mansión ([ES-wiki] galería: «Retrato de Rykard en la Mansión del Volcán»); el Candelabro de inquisidor y la Rueda de Ghiza (iconos/armas); hombres serpiente con látigo de magma; la virgen bajo la noria de Raya Lucaria.

**Líneas para que se OIGAN en el video** (las mejores, con segundo): «Join the Serpent King, as family… Together, we will devour the very gods!» (eljrH9jvANE ~1:02–1:12 o yjnnv3ib_t4 ~2:15–2:27) · «A serpent never dies.» (yjnnv3ib_t4 ~3:42–3:51) · Tanith «Our lord's carcass is vast…» (sJ3hbEi9loA 0:11–0:19) · Rya «Kill me, please.» (5IkIEt8YlW4 ~10:27–10:30) · fantasma «Someone, please, kill him…» (d7shRsbbjvI 0:05–0:12) · Parches «…stay away from the Volcano Manor!» (onpson1sZsI ~0:53–0:55) · Parches «daddy ambition… lady blasphemy» (ijNdEQdToEs 0:24–0:30). **Todas en inglés**: comprobar en la mezcla final con Whisper (regla de oro 10).

---

## 6. PUESTOS PROPUESTOS (del 5 al 1)

Lógica de escala: de **unos nobles** en una sala secreta (5) a **cualquiera que pase cerca** de una máquina (4), **su propio ejército** (3), **una especie entera** nacida de su blasfemia (2)… y el n.º 1 rompe la escala hacia arriba y hacia atrás: **la muerte de un dios**, años antes, cobrada en una losa que tú mismo usaste. Duración orientativa: gancho 1:30 · cinco puestos de 4:00–4:30 (2-3 escenas cada uno) · suscripción ≈ 0:10 antes del n.º 1 · cierre 1:00 ≈ 25 min.

**Gancho propuesto:** la única línea verificada en español: «Únete a la familia del Rey Serpiente. ¡Juntos devoraremos a los dioses!» → «Casi todo el mundo cree que lo peor de Rykard es que se dejó comer por una serpiente. Eso es lo que **menos** daño hizo.» + recordar en una frase que la audiencia y los contratos ya se contaron en el video de los Sinluz (enlazar) y que hoy va todo lo demás.

### N.º 5 — «El juez con taller de tortura» (C1)
**Gancho:** «Antes de ser el señor de la Blasfemia, Rykard era la ley.»
1. Pretor = juez: Gideon lo llama juez despiadado al mando de una compañía de inquisidores, aborrecido «como una serpiente» (parafrasear). Casco de caballero de Gelmir: el penacho rojo, «pedigrí… hijo del señor Radagon».
2. La casa: Candelabro de inquisidor, «utilizado en secreto contra nobles en la Mansión del Volcán… El olor a sangre quemada provocaba la desesperación de la víctima. Un candelabro concebido por una mente meticulosa.» Gracias con nombre: **Iglesia de la ciudad de los penados**, **Cámara subterránea de la inquisición**.
3. El empleado: el inquisidor Ghiza, que te invade dentro de la mansión con su Rueda («cuchillas que desgarran la carne»), su Máscara ensangrentada y su Atuendo de oficial («…ejecuciones, rituales truculentos… Las tareas más oscuras mueven los engranajes de la humanidad»).
4. (Opcional, con aviso) Daedicar de la v1.00: amante y ayudante de la inquisición que probaba la tortura en sí mismo «por amor».
**Remate de puesto:** el diseño de esa rueda se copió para unas máquinas… → pasa al n.º 4.
**Clips:** kZ4pC3lkIKU 0:01–0:34 (Gideon); wdGZrHkRv4M 22:54–23:51 (Ghiza); longplay HJ6EIysyst8 52:41:39 (mansión).

### N.º 4 — «Secuestros a domicilio» (C2)
**Gancho:** «El atajo más famoso de Liurnia es un secuestro.»
1. Parches y su historia de la virgen de hierro con «hechizo de transposición» que te «saca al pie del Árbol Áureo»… según dicen (parafrasear).
2. Lo que pasa: te agarra hasta matarte y despiertas encerrado en la **Cámara subterránea de la inquisición** de la Mansión del Volcán; no puedes salir sin vencer a dos vírgenes raptoras, que sueltan… el **Candelabro de inquisidor**. La Rueda de Ghiza: «su diseño se adoptó para… las vírgenes de hierro».
3. Las hay en la Academia, en la Mansión de los Caria, en las Afueras de la capital, en Leyndell y en el monte Gelmir. Y Parches, que te empuja por un acantilado gritando que no vayas a la Mansión, y luego confiesa que «allí cazan Sinluz como animales».
**Advertencia de guion:** el juego **no dice que Rykard las construyera**; decir «máquinas de tortura que acaban en su cámara de la inquisición».
**Clips:** 0U52CsjKPrY 0:10–1:23; TxnoanwFw4g 0:00–2:09 y 10:26; onpson1sZsI ~0:53–1:04.

### N.º 3 — «La guerra que abandonó» (C3)
**Gancho:** «La batalla más espantosa de toda la Devastación fue la suya. Y se fue a mitad.»
1. Gideon: «el escenario de la batalla más espantosa de la Devastación» (parafrasear). Monumento: «Lo sórdido, lo enfermizo, lo profano; una guerra miserable interminable que no concede la gloria.» Mapa: «peligros que se agudizan aún más tras la Devastación».
2. En plena guerra, el semidiós se mete en la boca de una serpiente «runa incluida». Un alma en el camino: «si este campo de muerte pútrido es lo que traería tu blasfemia, no puedo seguir. Nadie puede» (parafrasear). Armadura de caballero de Gelmir: «un emblema que ya nadie usa».
3. Sus hombres buscan un arma para matarlo (Cazador de serpientes) y fallan; la lanza acaba clavada en un montón de cadáveres en la puerta de su sala. Y el fantasma de uno de sus caballeros te suplica: «que alguien lo mate… eso ya no es el pretor Rykard» (parafrasear). Si lo matas, te deja el gesto «Gracias» (**nombre español NO VERIFICADO**: decir «te da las gracias»).
**Remate de puesto (cameo C6):** la Hoja blasfema: «los restos de la infinidad de héroes a los que ha devorado se retuercen en la superficie», y en la arena hasta el espía de Gideon (Sobretodo ocular).
**Clips:** d7shRsbbjvI 0:05–1:34; longplay 52:41:39 (laderas, campamentos) y 57:44:51 (arena).

### N.º 2 — «Los hijos del ritual» (C4)
**Gancho:** «Rykard quería una familia. La consiguió. Nadie le preguntó a la familia.»
1. Cenizas de hombre serpiente: la serpiente «devoró a un semidiós, lo cual provocó el nacimiento de los hombres serpiente». La religión que Rykard revivió (Disparo de magma) usaba una espada «para ofrecer sacrificios» (Espada curva de dios serpiente).
2. Amnios de serpiente, en el altar del Templo de Eiglay: «pobre vástago no deseado fruto de un repulsivo ritual de parto. Permanece siempre húmedo».
3. Zorayas: la reclutadora que buscaba Sinluz «despiadados incluso con los suyos» resulta ser una de esas criaturas; le dijeron que nació «por la gracia de un rey glorioso». Cuando sabe la verdad: «fui una hija no deseada… nacida de un ritual horrible… Mátame, por favor» (parafrasear). Si la matas: «Gracias… mi adalid… madre».
**Advertencia:** el tónico del olvido y el Pesar de Daedicar **ya salieron** en el video de los Sinluz: mencionarlos en una frase, sin releer las descripciones.
**Clips:** 5IkIEt8YlW4 6:06–6:53 y 9:52–10:52; YS1P-_MROO0 (Templo de Eiglay, segundo NO VERIFICADO).

### N.º 1 — «La propina de la noche del complot» (C5) — la que ignoraste
**Giro:** «Las otras cuatro las hizo con el poder que ya tenía. Esta la hizo para conseguirlo. Y tú la llevaste en el inventario.»
1. La Garra blasfema, que te suelta Bernahl en Farum Azula y que usas contra Maliketh: «En la noche del complot, Ranni recompensó con estos restos al pretor Rykard.» En japonés: **un pago de agradecimiento**.
2. Qué noche era: «Alguien robó un fragmento de la Runa de la Muerte a Maliketh… y una noche funesta, asesinó a Godwyn, el Dorado» (Rogier, [ES-wiki]). El primer semidiós en morir; tras eso vino la Devastación (ya contado en el video de Ranni: solo recordarlo). **El juego no dice qué hizo Rykard para cobrar**: preguntarlo en voz alta.
3. Para qué quería el pago: «permitirán a Rykard desafiar a Maliketh, la Hoja Negra, la oscura bestia de la Muerte Escrita» — el que luego quiso «vivir eternamente» (Recuerdo del blasfemo) y murió diciendo «A serpent never dies» (que se OIGA). El pretor que juzgaba herejes ya planeaba el «día de la blasfemia» (JP) antes de la guerra.
4. Cierre del puesto: Bernahl, «heredero de la voluntad de mi hermano», carga la Garra hasta que se la quitas: «hasta él estaba preparado para un final miserable cuando abrazó la blasfemia en su propia carne» (parafrasear). Y Parches lo resume: «papá ambición cortejando a la señora blasfemia» (parafrasear).
**Clips:** Ifw3P9rXaRY 0:03–0:56; yjnnv3ib_t4 ~3:42–3:51 (muerte); zcj3vSb5KyM (invasión, segundo NO VERIFICADO); ijNdEQdToEs 0:24–0:30.

**Cierre propuesto:** Tanith tras tu victoria: «nuestro señor es inmortal y algún día volverá, más fuerte» (parafrasear) + el Cetro de devorador: «una serpiente devorando el mundo… se convertirá, algún día, en el símbolo del señor de la Blasfemia».

**Reservas / cameos:** Dedo Recusante («cubierto por escamas de serpiente… reliquia del señor de la Mansión del Volcán») para el gancho o el n.º 4 · Castañuelas que Tanith rechaza «I must continue devouring my beloved lord» · Tanith: «not unlike another guest we had long ago» · Ira de Gelmir: «la arrogancia de intentar dominarlo es propio únicamente de hombres y víboras».

---

## 7. Datos falsos comunes que NO hay que decir

1. **«Rykard construyó las vírgenes de hierro / raptoras.»** — Ningún texto lo dice. Lo comprobable: su arma copia la rueda de un inquisidor (Rueda de Ghiza) y la de Raya Lucaria te deja en la Cámara subterránea de la inquisición de la Mansión.
2. **«Rykard mató a Godwyn.»** — El texto dice que Ranni **lo recompensó** la noche del complot. Quién mató a Godwyn (las asesinas de los Cuchillos Negros) ya se contó en el video de Ranni.
3. **«La virgen de Raya Lucaria te lleva al Árbol Áureo.»** — Eso dice Parches; te lleva a la mansión. Él mismo admite que «podría haber sido más claro».
4. **«Tanith es la madre de Rya.»** — Es su **madre adoptiva** («as her adoptive mother»).
5. **«Daedicar es la madre de Rya.»** — Lo «implica» la wiki; el juego no lo dice.
6. **«Los inquisidores de Rykard torturaban albinaúricos.»** — Sin cita.
7. **«Morgott dirigió el asedio de la Mansión.»** — Interpretación de la wiki.
8. **«Rykard es hijo de Márika.»** — Es **hijastro**: «semidiós adoptivo tras la unión de Radagon con la Reina Márika».
9. **«La serpiente se llama Eiglay / Eveligne.»** — Eiglay es el nombre del **templo**; «Eveligne» sale solo en una línea **recortada**.
10. **«Rykard luchó en la guerra contra los gigantes.»** — Nada lo dice.
11. **«Una serpiente nunca muere»** como cita en español — el español no está verificado; usar el audio en inglés.
12. **Nombres:** «Fragmentación» → **Devastación** (el video de Ranni usó «Fragmentación»: no repetirlo) · «Tierra de las Sombras» → **Reino de las Sombras** · «Doncella de hierro» → **Virgen raptora** · «Ruinas de Gelmir» → **Tumba del héroe de Gelmir** · «Mansión Volcánica» es la versión latinoamericana · «Patches» → **Parches** · «Dedo del recusante» → **Dedo Recusante**.
13. **«La Garra blasfema era de Bernahl.»** — Era de Rykard (pago de Ranni); Bernahl la lleva cuando te invade.
14. **«Rykard se comió a Tanith / Tanith se convirtió en serpiente.»** — Ella intenta comérselo a él y **desea** ser su serpiente.
15. **«Los gigantes los exterminó Messmer.»** — Ver §9.

---

## 8. Pendientes para la sesión de guion

**LO YA CONTADO DE RYKARD EN EL CANAL (no repetir con el mismo ángulo)**
- `videos/er_sinluz_atrocidades/guion.py` (n.º 4 «Sicario de un caníbal», escenas p4/p4b/p4c, y p3f): la Mansión del Volcán y Tanith «te ofrece una familia»; las cartas y los 3 contratos (Istvan en la Colina Tormentosa, Rileigh en la Meseta Altus, Juno Hoslow en los Picos de los gigantes); los pagos (Disparo de magma, Hoja de hueso de serpiente, Camafeo del megalómano **con su descripción**); «no hay sitio para los débiles ni para los que quieren conservar las manos limpias»; la audiencia → **Rencor de Rykard con su descripción** (fauces de la serpiente, «se convirtieron en sus semejantes») y que los campeones eran «el siguiente menú»; Rykard «se ofreció como alimento a la serpiente, runa incluida»; **Tanith comiéndose el cadáver** y su frase; el **Tónico del olvido** (descripción y «Mi señor, no podría haber mayor angustia que olvidarte») y el recado de dárselo a Rya; el **Pesar de Daedicar** con su descripción («propina»); la **Máscara de consorte** con su descripción; Tanith muere de un golpe y te invade el Caballero de Tanith; el Rencor como arma que lanza a los campeones «para que vuelvan a morir»; Rennala y el Recuerdo (Lectora de Dedos Enia).
- `videos/er_morgott_atrocidades/guion.py`: Morgott nombra al «pretor Rykard» entre los «traidores deliberados».
- `videos/er_mohg_atrocidades/guion.py` y `er_godfrey_atrocidades/guion.py`: solo «Rykard está apuntado» en los comentarios (lo pedían Franko y Héctor).
- `videos/er_ranni_atrocidades/guion.py`: la Noche de los Cuchillos Negros, Tiche, Godwyn primer semidiós muerto (sin mencionar la Garra blasfema ni a Rykard) → el n.º 1 es **ángulo nuevo**, pero no volver a contar la noche: solo recordarla.
- `videos/er_radagon_atrocidades/guion.py`, `er_radahn_atrocidades/guion.py`: Rennala abandonada, los hijos de Radagon y Rennala (sin Rykard).
- **Ángulo nuevo para lo que se toca otra vez:** la serpiente/audiencia solo como apoyo (Hoja blasfema, Sobretodo ocular); Rya desde su origen (hombres serpiente, amnios), no desde el tónico; Tanith solo con las castañuelas y «nuestro señor es inmortal».

**Pendientes**
- Español de **todas** las líneas habladas salvo «Únete a la familia del Rey Serpiente…»: **NO VERIFICADO** → parafrasear sin comillas o transcribir de un clip con subtítulos del juego en español.
- Cotejar con captura: monumento del asalto (español de [ES-wiki]), descripciones de [EG] con erratas (Gran Runa, Tónico, Rueda de Ghiza, Armadura de caballero de Gelmir «Casco usado», Atuendo de oficial «Contro», Dedo Recusante, Carta de Zorayas).
- Medir en el mapa: Tumba del héroe de Gelmir, monumento del Noveno campamento, Mansión de los Caria, Castillo sombrío (**NO VERIFICADO**).
- Revisar marca de agua/rótulos de: pgp, VynPlays, SourceSpy91, Terry Goodwin, Stratek, Sunless_Solaire, Games from Mars, Zach CK, Soul Cat, Kevin B, SBG, Zero Manga Hunter, Aethersong, IAmToastMan, ShyKatana, Kelvyn Acevedo, Eagle Bearer, Gallvanos.
- Segundos con [WH] (±2-3 s): ajustar al cortar.
- **NO VERIFICADO:** nombre español del gesto «My Thanks»; del evento «Night of Black Knives» en un texto del juego; quién construyó las vírgenes; Daedicar v1.00 fuera de [EN-wiki]; Morgott al mando del asedio; tortura de albinaúricos; qué hizo Rykard la noche del complot; a qué «hermano» se refiere Bernahl; a qué «otro invitado» se refiere Tanith.

---

## 9. Comentario de los gigantes («lo de los gigantes creo que fue messmer», video de Godfrey)

**Veredicto: el comentario se equivoca. Según los textos del juego, la guerra contra los gigantes la dirigió Godfrey, por orden de Márika. Messmer dirigió otra guerra de exterminio, en el DLC: la cruzada contra los cornamentados del Reino de las Sombras. Ningún texto que encontrara pone a Messmer en la guerra contra los gigantes.**

**Godfrey y los gigantes (juego base)**
- **Corona de Señor del Círculo** ([EG] armaduras-p477; igual la **Armadura de Señor del Círculo**, p478): «Corona de Godfrey, el primer Señor del Círculo. / La era del Árbol Áureo empezó en mitad de un enfrentamiento, cuando Godfrey era el señor de la Batalla. / **Lideró la guerra contra los gigantes.** Se enfrentó solo al señor de la Tormenta. Y al fin llegó el momento en el que cayó su último enemigo…» EN ([EN-wiki] Elden Lord Crown): «He led the War against the Giants.»
- **Eco de Márika en la Primera iglesia de Márika** (Picos de los gigantes), español [ES-wiki] Reina Márika la Eterna (leído hoy): «Recordadlo, valientes guerreros. Recuérdalo, mi señor Godfrey. Elogiamos tus actos. / […] / **Acaba con los gigantes con tu espada y confina la llama en lo alto de la montaña.** / Permite que empiece una nueva era…»
- **Recuerdo del gigante de fuego** ([EG] objetos-p520): «El gigante de fuego es un superviviente de la guerra contra los gigantes. Al constatar que las llamas de su forja jamás podrían extinguirse, la Reina Márika lo maldijo…»
- La [EN-wiki] (War Against the Giants) pone como mandos a Márika y Godfrey; Messmer no aparece en esa página.

**Messmer y su cruzada (Shadow of the Erdtree)**
- **Armadura de Messmer** ([EG] armaduras-p593): «Por deseo de su madre, Messmer se convirtió en un símbolo aterrador para llevar a cabo la **cruzada purificadora** que ella ansiaba.»
- **Mayal de serpiente** ([EG] armas-p331): «Algunos del ejército de Messmer usaron estos mayales para **quemar a los cornamentados** y marcarlos con agonía y miedo.»
- **Escudo con blasón de serpiente** ([EG] escudos-p70): «Se dice que se forjó para conmemorar los inicios de la **cruzada iniciada por Messmer, hijo de Márika**.»
- **Insignia de cruzada** ([EG] talismanes-p92): «…en recuerdo de los caídos en la cruzada sagrada liderada por Messmer. […] Los cruzados olvidaron el honor y la piedad para **empalar y quemar** sin misericordia a quienes consideraban impuros.»
- **Tornado de bestia divina** ([EG] encantamientos-p122): «La mayoría de las bestias divinas fueron destripadas y colgadas en las lanzas de Messmer, antes de ser calcinadas en sus llamas.»
- **Recuerdo del Empalador** ([EG] objetos-p858; errata «los sutituyó»): «…su madre le arrancó el ojo y [lo] sustituyó por un sello de Gracia. Sin embargo, su miedo la obligó luego a esconder a su hijo en el **Reino de las Sombras**.»
- Línea de Messmer en español ([ES-wiki]): «Quienes se ven despojados del don del oro deberán hacer frente a la muerte... En el abrazo de la llama de Messmer.»
- [ES-wiki] Reino de las Sombras: «fue calcinado en una gran purga llevada a cabo por Messmer el Empalador por orden de la Reina Márika, con el objetivo de erradicar a los cornamentados» (resumen de la wiki, no texto del juego).

**De dónde puede venir la confusión** (lectura nuestra, no de las fuentes): las dos son guerras de exterminio **ordenadas por Márika**; en los Picos de los gigantes hay cadáveres de gigantes atravesados por estacas (escenario; el juego no dice quién los clavó) y a Messmer lo llaman «el Empalador»; y las dos tienen fuego de por medio (la llama de los gigantes / la llama de Messmer). Pero el fuego de Messmer es suyo («Messmer odiaba su propio fuego», **Orbe de Messmer**, [EG] encantamientos-p120), no el de la forja.

**Respuesta sugerida (contraburla del comentario, no de la persona):** «Casi: Messmer también empalaba por encargo de mamá, pero a otros. Los gigantes los liquidó Godfrey; lo dice su corona: "lideró la guerra contra los gigantes". Messmer tuvo su propia guerra, en el Reino de las Sombras, contra los cornamentados. Márika repartía genocidios por hijo, como quien reparte tareas de la casa.»

**URLs:** https://www.eliteguias.com/guias/e/er/elden-ring_armaduras-p477.php · …armaduras-p478.php · …objetos-p520.php · …armaduras-p593.php · …armas-p331.php · …escudos-p70.php · …talismanes-p92.php · …encantamientos-p122.php · …objetos-p858.php · …encantamientos-p120.php · https://eldenring.fandom.com/es/wiki/Reina_Márika_la_Eterna · https://eldenring.fandom.com/es/wiki/Messmer_el_Empalador · https://eldenring.fandom.com/es/wiki/Reino_de_las_Sombras · https://eldenring.fandom.com/wiki/War_Against_the_Giants · https://eldenring.fandom.com/wiki/Crusade

