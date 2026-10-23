# Investigación: objetos más raros de WoW Vanilla que podríamos volver a ver en WoW Forever

Canal: Crónicas de Warcraft (`cronicas_warcraft`). Fecha de la investigación: 22-oct-2026.
Regla: solo datos verificados con fuente. Lo que no se pudo confirmar va marcado **(sin confirmar)**.

**Cómo se verificó**
- **Ficha de cada objeto** (ID, nivel de objeto, nivel requerido, calidad, icono, nombre en inglés y español): API XML de Wowhead Classic (`https://www.wowhead.com/classic/item=<ID>&xml`) y API de tooltips (`https://nether.wowhead.com/classic/tooltip/item/<ID>?locale=11` para **es-MX** y `locale=6` para **es-ES**). Wowhead.com/es usa es-ES; el es-MX sale del `locale=11` de la API de tooltips (los nombres coinciden con los del cliente latino).
- **Coordenadas Classic de NPC, objetos y entradas de mazmorra**: base de datos del addon Questie para Classic (versión v11.38.0, datos tomados de servidores Classic): <https://github.com/Questie/Questie/tree/v11.38.0/Database/Classic> y <https://github.com/Questie/Questie/blob/v11.38.0/Database/Zones/data/dungeons.lua>. **OJO:** las coordenadas de warcraft.wiki.gg suelen ser de retail y NO coinciden con Classic en algunas zonas (ej. Demitrian: wiki 29.6, 10.6 vs Classic 21.7, 8.6). Usar siempre las de este documento.
- **Hechos, historia y parches**: warcraft.wiki.gg (enlace en cada ficha) y prensa citada.
- Coordenadas comprobadas pintándolas sobre el mapa real de Silithus de Wowhead: caen exactamente en su sitio (Cenarion Hold, Demitrian, Gong).

---

## 0. Qué es WoW: Forever (no confundir con retail)

- **Qué es:** rama independiente de WoW, un «Classic+» permanente: mecánicas y estética de 2004 con historias y contenido nuevos; no está en la misma continuidad que retail. Ambientado en el primer año de WoW (25 ADP), **después de *Warcraft III Reforged: Forsaken Kingdom* y ANTES del Núcleo de Magma**. Fuente: <https://warcraft.wiki.gg/wiki/Forever>, <https://www.warcrafttavern.com/forever/news/warcraft-forever-classic-announced-at-blizzcon-2026/>
- **Fechas:** anunciado en la BlizzCon 2026. Beta del 17-sep al 22-oct-2026 (tope nivel 30); reserva de nombres 27-oct; **lanzamiento 4-nov-2026**. Fuente: <https://blizzardwatch.com/2026/09/13/world-warcraft-forevers-roadmap-gives-us-ann-idea-expect-rest-2026-summer-2027/>, <https://warcraft.wiki.gg/wiki/Forever>
- **Nivel máximo 60 para siempre** (nunca subirá). Nuevos: raza Skyborne (altos elfos exiliados), paladines Renegados, chamanes enanos, zonas nuevas (Riverlands, Monte Hyjal), 9 mazmorras nuevas, +1000 misiones, talentos rehechos, sistema Legacy (sustituye logros). Fuente: Warcraft Tavern y wiki (arriba).
- **Bandas:** el 9-dic-2026 se abren 3: **Barrow Deeps** (10, nueva), **Hyjal Summit** (20, nueva) y **Guarida de Onyxia** (40, la única clásica confirmada). Fuente: Blizzard Watch y wiki.
- **Hoja de ruta 2027:** primavera = 2 bandas nuevas, 2 mazmorras, zona y **una NUEVA cadena legendaria**; verano = **«una banda icónica rehecha»** (sin nombre), otra banda nueva, más mundo. Fuente: Blizzard Watch. Que la banda icónica sea el Núcleo de Magma, BWL, AQ o Naxx es **(rumor / sin confirmar)**; solo encaja con que el juego esté ambientado «antes del Núcleo de Magma».
- **NO confirmados:** Núcleo de Magma, Guarida Alanegra, Zul'Gurub, Ahn'Qiraj, Naxxramas, el evento de las puertas de AQ y los legendarios clásicos (Trueno Furioso, Sulfuras, Atiesh). La wiki no los menciona como contenido de Forever. Fuente: <https://warcraft.wiki.gg/wiki/Forever>
- **Mazmorras clásicas que SÍ están en la lista de Forever** (relevante para qué objetos podrían volver pronto): Profundidades de Roca Negra, Cumbre de Roca Negra inferior (LBRS), La Masacre (Este, Oeste y Norte), Scholomance, Stratholme, Castillo de Colmillo Oscuro, Minas de la Muerte, Cavernas de Brazanegra, Monasterio Escarlata, Uldaman, Zul'Farrak, Maraudon, Templo Sumergido, etc. (Cumbre de Roca Negra superior, UBRS, no aparece). Fuente: tabla de mazmorras en <https://warcraft.wiki.gg/wiki/Forever>
- **Dato gancho:** en el **evento de fin de beta (22-oct-2026, 10:00 PDT)** Kazzak destruyó Rémol (Brill), Azuregos atacaba Villadorada y había jefes fuera de las ciudades (Super Hogger, **Thunderaan**…); **los jefes soltaban Sulfuras y Trueno Furioso** y todos los bichos soltaban botín del Núcleo de Magma sin requisito de nivel. Fue un evento temporal de la beta, no contenido permanente. Fuente: <https://warcraft.wiki.gg/wiki/Forever> § «End of beta event»

**Lectura para el guion:** objetos de mazmorras que ya están en Forever (Ferromazo, Destrero de la muerte, Quel'Serrar con Onyxia el 9-dic, Corcel nefasto, Puño de Verigan, Hoja krol, Orbe de engaño, Sable de hielo) = «podrían volver pronto» **(sin confirmar que los objetos y misiones se mantengan iguales)**. Los que dependen del Núcleo, BWL, ZG, AQ o Naxx = **solo en fases tardías y si esas bandas vuelven**.

---

## 1. Mapas reales del juego (Wowhead Classic) — PATRÓN QUE FUNCIONA

Probado con `curl` el 22-oct-2026:

```
https://wow.zamimg.com/images/wow/classic/maps/enus/<tamaño>/<zoneId>.jpg
  original → 1022x668 (algunos 1024x683: Teldrassil 141, Stratholme 2017)  ~130-170 KB
  zoom     → 772x515
  normal   → 488x325
Versión con rótulos en español (es-ES): .../classic/maps/eses/original/<zoneId>.jpg  (200 OK; «esmx» da 404)
```

- **Coordenadas → píxel:** `px = x/100 * ancho`, `py = y/100 * alto` sobre la imagen `original` (comprobado en Silithus).
- **Mapas de continente / mundo:** `-1` = Azeroth (los dos continentes), `-3` = Reinos del Este, `-6` = Kalimdor. (`-4` es el mapa cósmico de TBC, no usar.)
  - <https://wow.zamimg.com/images/wow/classic/maps/enus/original/-1.jpg>
  - <https://wow.zamimg.com/images/wow/classic/maps/enus/original/-3.jpg>
  - <https://wow.zamimg.com/images/wow/classic/maps/enus/original/-6.jpg>
- **Mapas de instancia** (planta, fondo negro): Núcleo de Magma 2717, BWL 2677, Naxxramas 3456, Stratholme 2017, Scholomance 2057, La Masacre 2557, Prof. Roca Negra 1584, Zul'Gurub 1977, AQ40 3428, AQ20 3429, Colmillo Oscuro 209, Minas de la Muerte 1581, Brazanegra 719 → todos 200 OK. **Sin mapa (404): Guarida de Onyxia 2159 y Cumbre de Roca Negra 1583.**
- **Iconos:** `https://wow.zamimg.com/images/wow/icons/large/<icono>.jpg` (56x56, 200 OK). Tooltip: `https://www.wowhead.com/classic/item=<ID>`.

**IDs de zona (Wowhead/AreaTable) y nombre es-MX** (nombres de la traducción oficial que usa Questie; es-MX = es-ES en todas estas):

| Zona (en) | es-MX | ID | | Zona (en) | es-MX | ID |
|---|---|---|---|---|---|---|
| Silithus | Silithus | 1377 | | Burning Steppes | Las Estepas Ardientes | 46 |
| Tanaris | Tanaris | 440 | | Searing Gorge | La Garganta de Fuego | 51 |
| Felwood | Frondavil | 361 | | Eastern Plaguelands | Tierras de la Peste del Este | 139 |
| Winterspring | Cuna del Invierno | 618 | | Western Plaguelands | Tierras de la Peste del Oeste | 28 |
| Azshara | Azshara | 16 | | Elwynn Forest | Bosque de Elwynn | 12 |
| Moonglade | Claro de la Luna | 493 | | Westfall | Páramos de Poniente | 40 |
| Teldrassil | Teldrassil | 141 | | Dun Morogh | Dun Morogh | 1 |
| Darkshore | Costa Oscura | 148 | | Loch Modan | Loch Modan | 38 |
| Ashenvale | Vallefresno | 331 | | Stormwind City | Ciudad de Ventormenta | 1519 |
| Feralas | Feralas | 357 | | Ironforge | Forjaz | 1537 |
| Un'Goro Crater | Cráter de Un'Goro | 490 | | Stranglethorn Vale | Vega de Tuercespina | 33 |
| Dustwallow Marsh | Marjal Revolcafango | 15 | | The Hinterlands | Tierras del Interior | 47 |
| Blasted Lands | Las Tierras Devastadas | 4 | | Swamp of Sorrows | Pantano de las Penas | 8 |

Instancias: Núcleo de Magma 2717 · Guarida de Alanegra 2677 · Guarida de Onyxia 2159 · Naxxramas 3456 · Stratholme 2017 · Scholomance 2057 · La Masacre 2557 · Profundidades de Roca Negra 1584 · Cumbre de Roca Negra 1583 · Zul'Gurub 1977 · Templo de Ahn'Qiraj 3428 · Ruinas de Ahn'Qiraj 3429 · Castillo de Colmillo Oscuro 209 · Las Minas de la Muerte 1581 · Cavernas de Brazanegra 719 · Cavernas del Tiempo (dentro de Tanaris).

**Entradas de instancia en el mapa de zona (Classic, Questie `dungeons.lua`):**
Montaña Roca Negra (Núcleo, BWL, BRD, BRS): Garganta de Fuego (34.8, 85.3) / Estepas Ardientes (29.4, 38.3) · Guarida de Onyxia: Marjal Revolcafango (52.6, 76.8) · Naxxramas: Tierras de la Peste del Este (39.9, 25.8) · Stratholme: TdP del Este (31.3, 15.7) y entrada de servicio (47.9, 23.9) · Scholomance: TdP del Oeste (69.7, 73.2) · La Masacre: Feralas (59.2, 45.1) · Zul'Gurub: Vega de Tuercespina (53.9, 17.6) · Ahn'Qiraj: Silithus (28.6, 92.3) · Colmillo Oscuro: Bosque de Argénteos (44.8, 67.8) · Minas de la Muerte: Páramos de Poniente (42.5, 71.7) · Brazanegra: Vallefresno (14.5, 14.2).

---

## 2. Los 16 candidatos

Formato: nombre es-MX (es-ES si difiere) · inglés · ID Wowhead Classic · icono · nivel req. / nivel de objeto / calidad · fuente · datos raros con fuente · ruta (si aplica) · ¿cuándo podría estar en Forever?

### 1. Trueno Furioso, espada bendita del Hijo del Viento
- **EN:** Thunderfury, Blessed Blade of the Windseeker · **ID 19019** · icono `inv_sword_39` · req 60 / ilvl 80 / **Legendaria** · espada de una mano. es-ES: «Trueno furioso…». Tooltip: <https://www.wowhead.com/classic/item=19019>
- **Fuente:** cadena de misiones. Ingredientes: **Ataduras del Hijo del Viento** (izquierda ID 18563, de **Barón Geddon**; derecha ID 18564, de **Garr**; ambos en el Núcleo de Magma; ~3 % cada una, estimación de la comunidad), **Esencia del Señor del Fuego** (19017, Ragnaros, solo con la misión), **10 barras de elementium** (17771; mineral de elementium de la Guarida Alanegra), más 10 núcleos ígneos, 100 barras de arcanita y 30 flujos elementales (según la wiki). Fuentes: <https://warcraft.wiki.gg/wiki/Thunderfury,_Blessed_Blade_of_the_Windseeker>, <https://warcraft.wiki.gg/wiki/Bindings_of_the_Windseeker>, ~3 %: <https://warcrafttavern.com/wow-classic/guides/thunderfury>, <https://wowpedia.fandom.com/wiki/Bindings_of_the_Windseeker>
  - Nota: la página wiki de Trueno Furioso dice «izquierda de Garr»; la de las Ataduras y la base de datos Classic dicen **izquierda (18563) = Geddon, derecha (18564) = Garr**. Usar esta última.
- **Datos raros:**
  - Primer portador conocido: el enano guerrero **Wray**; su cadáver aún empuña la espada en la campaña del chamán de Legion. <https://warcraft.wiki.gg/wiki/Thunderfury,_Blessed_Blade_of_the_Windseeker>
  - Su nombre fue de los más largos del juego y se volvió meme del chat de Los Baldíos («Did someone say [Thunderfury]?»). Misma fuente.
  - Lore: Ragnaros derrotó a Thunderaan, Príncipe del Aire (hijo de Al'Akir); su esencia se encerró en un talismán partido en dos y entregado a Geddon y Garr. <https://warcraft.wiki.gg/wiki/Bindings_of_the_Windseeker>
  - Añadida en el parche 1.6.0 (12-jul-2005); en 1.9.0 le bajaron la ralentización y la frecuencia del efecto. Wiki (arriba).
  - En el fin de beta de Forever (22-oct-2026) Thunderaan apareció fuera de las ciudades y los jefes soltaban la espada. <https://warcraft.wiki.gg/wiki/Forever>
- **Ruta (misiones 7785 → 7786 → 7787):**
  1. Núcleo de Magma (2717): Garr y Barón Geddon sueltan las Ataduras.
  2. Silithus (1377), Campamento Crepuscular Arrasado: **Alto señor Demitrian (21.7, 8.6)** — «Examina el recipiente» (7785) y «Thunderaan el Hijo del Viento» (7786).
  3. Guarida Alanegra (2677): mineral de elementium. Núcleo de Magma: Esencia del Señor del Fuego (Ragnaros).
  4. Silithus, Demitrian (21.7, 8.6): invoca al **Príncipe Thunderaan** → la banda lo mata → «Hoja besada por el viento durmiente» (19018) → «¡Álzate, Trueno Furioso!» (7787).
- **En Forever:** fase tardía; necesita Núcleo de Magma + Guarida Alanegra, ninguno confirmado.

### 2. Sulfuras, Mano de Ragnaros
- **EN:** Sulfuras, Hand of Ragnaros · **ID 17182** · icono `inv_hammer_unique_sulfuras` · req 60 / ilvl 80 / **Legendaria** · maza de dos manos. Tooltip: <https://www.wowhead.com/classic/item=17182>
- **Fuente:** se fabrica: **Ojo de Sulfuras** (17204, Ragnaros; ~3 % según la wiki, 3,74 % según Mein-MMO) + **Martillo de Sulfuron** (17193, herrería 300). Los planos se obtienen entregando un **Lingote de sulfuron** (17203; según la base de datos, de Golemagg el Incinerador) a **Lokhtos Tratoscuro** (Lokhtos Darkbargainer) en el Bar Tragapenas de las Profundidades de Roca Negra (misión 7604 «Un contrato vinculante»). <https://warcraft.wiki.gg/wiki/Sulfuras,_Hand_of_Ragnaros>, <https://warcraft.wiki.gg/wiki/Eye_of_Sulfuras>, <https://warcraft.wiki.gg/wiki/Sulfuron_Hammer>
- **Datos raros:**
  - Hasta la Guarida Alanegra (1.6) fue el arma cuerpo a cuerpo con más DPS del juego, y hasta 1.11 la de más daño bruto. <https://warcraft.wiki.gg/wiki/Sulfuras,_Hand_of_Ragnaros>
  - El Ojo puede caer para cualquier clase, aunque no pueda usar mazas de dos manos. <https://warcraft.wiki.gg/wiki/Eye_of_Sulfuras>
  - Abril 2026: un jugador (SJBaerosols, Reddit) consiguió Sulfuras **tras unos 20 años**; el martillo pide 8 lingotes de sulfuron, 20 barras de hierro negro, 50 de arcanita y 10 Sangre de la Montaña. <https://mein-mmo.de/en/wow-sulfuras-nach-20-jahren,1564884/>
  - Se repartió en el fin de beta de Forever. <https://warcraft.wiki.gg/wiki/Forever>
- **Ruta:** Núcleo de Magma (lingote + Ojo) → Montaña Roca Negra / Profundidades de Roca Negra (1584), Lokhtos en el Bar Tragapenas (dentro de la instancia; entrada en la Garganta de Fuego 34.8, 85.3).
- **En Forever:** fase tardía (Núcleo de Magma no confirmado). BRD sí está.

### 3. Atiesh, gran báculo del Guardián
- **EN:** Atiesh, Greatstaff of the Guardian · **IDs 22589 (mago), 22630 (brujo), 22631 (sacerdote), 22632 (druida)** · icono `inv_staff_medivh` · req 60 / ilvl 90 / **Legendaria**. Tooltip: <https://www.wowhead.com/classic/item=22589>
- **Fuente:** **40 Astillas de Atiesh** (22726; caen de todos los jefes de Naxxramas salvo Sapphiron y Kel'Thuzad) → **Armazón de Atiesh** (22727) → Anacronos → **Cabeza del báculo** (22733, Kel'Thuzad) + **Base de Atiesh** (22734, C'Thun en AQ40) → purificarlo en Stratholme y matar al demonio Atiesh. <https://warcraft.wiki.gg/wiki/Atiesh,_Greatstaff_of_the_Guardian>, <https://warcraft.wiki.gg/wiki/Splinter_of_Atiesh>
- **Datos raros:**
  - Fue el **primer legendario de lanzador** de WoW. Abría un portal a la puerta de Karazhan **antes de que Karazhan existiera** (se abrió con TBC). <https://warcraft.wiki.gg/wiki/Atiesh,_Greatstaff_of_the_Guardian>
  - En Karazhan, el fantasma de Nielas Aran reacciona: «Where did you get that?! Did HE send you??». Misma fuente.
  - El demonio Atiesh tenía más de 200 000 PV y empuñaba dos **Andonisus, Segador de almas** (22736, ilvl 100); soltaba una solo si lo desarmaban. <https://warcraft.wiki.gg/wiki/Atiesh_(demon)>
  - Lore: al caer Dalaran el bastón se partió en 42 pedazos; Kel'Thuzad los buscaba. <https://warcraft.wiki.gg/wiki/Atiesh,_Greatstaff_of_the_Guardian>
  - Un PNJ de retail encontró 39 astillas en el almacén del vacío de un aventurero (le faltó una). <https://warcraft.wiki.gg/wiki/Splinter_of_Atiesh>
- **Ruta (9250 → 9251 → 9257/9269/9270/9271):** Naxxramas (3456; entrada TdP del Este 39.9, 25.8) → Tanaris (440), **Anacronos (65.3, 50.0)** a la entrada de las Cavernas del Tiempo → Naxxramas (Kel'Thuzad) + AQ40 (C'Thun; Silithus 28.6, 92.3) → Anacronos → Stratholme (2017), **Festival Lane** entre Elders' Square y King's Square: invocar y matar a Atiesh → Anacronos.
- **En Forever:** la más tardía de todas (Naxx + AQ40).

### 4. Quel'Serrar
- **EN/es:** Quel'Serrar · **ID 18348** · icono `inv_sword_01` · req 60 / ilvl 71 / **Épica** · solo guerreros y paladines · «La Hoja Alta». Tooltip: <https://www.wowhead.com/classic/item=18348>
- **Fuente:** el libro **Compendio de matar dragones de Nostro** (18401; antes «Foror's Compendium») cae de jefes de La Masacre con probabilidad tan baja que «se consideraba imposible de farmear»; era ligado a equipar y podía comprarse en la casa de subastas. <https://warcraft.wiki.gg/wiki/Quel%27Serrar>, <https://warcraft.wiki.gg/wiki/Foror%27s_Compendium_of_Dragon_Slaying>
- **Datos raros:**
  - La mecánica más única del Vanilla: dejas la **Hoja antigua sin templar** (18489) en el suelo de la Guarida de Onyxia, la **Respiración profunda** de Onyxia la calienta (Hoja antigua caliente, 18488, que se enfría con el tiempo), y al morir Onyxia la clavas en su cadáver → Espada antigua tratada (18492). <https://warcraft.wiki.gg/wiki/Quel%27Serrar> y texto de la misión 7509.
  - El texto del libro es un guiño a EverQuest (esconderse bajo un puente, rotación de «Complete Heal» de 5-15 clérigos). <https://warcraft.wiki.gg/wiki/Foror%27s_Compendium_of_Dragon_Slaying>
  - Renombrado de «Foror's» a «Nostro's» en un hotfix del 27-jul-2021 (wiki, misma fuente). El motivo concreto **(sin confirmar)**.
  - «Aún hoy es raro ver una Quel'Serrar original»; eliminada en 3.2.2. <https://warcraft.wiki.gg/wiki/Quel%27Serrar>
- **Ruta (7507 → 7508 → 7509):** La Masacre (2557; entrada Feralas 59.2, 45.1) → Ateneo de La Masacre Oeste: **Tradicionalista Lydros** (Lorekeeper Lydros) → Guarida de Onyxia (2159; entrada Marjal Revolcafango 52.6, 76.8) → Lydros.
- **En Forever:** **candidata temprana**: La Masacre está en la lista de mazmorras y Onyxia abre el 9-dic-2026. Que la cadena siga igual **(sin confirmar)**.

### 5. Rhok'delar, arco largo de los Guardianes ancianos / Lok'delar
- **EN:** Rhok'delar, Longbow of the Ancient Keepers · **ID 18713** · icono `inv_weapon_bow_01` · req 60 / ilvl 75 / Épica · arco solo de cazador. **Lok'delar** (ID 18715, `inv_staff_21`; es-MX «Lok'delar, báculo de los Guardianes ancianos», es-ES «bastón»). <https://www.wowhead.com/classic/item=18713>
- **Fuente:** la **Hoja petrificada vieja** (18703) cae del **Alijo del Señor del Fuego** (cofre de Mayordomo Executus, Núcleo de Magma) → los Ancianos de Frondavil → matar **4 demonios disfrazados, SOLO, sin mascota** + tendones de dragón (azul: Azuregos o dracos Cobalto de Cuna del Invierno; negro: Onyxia). <https://warcraft.wiki.gg/wiki/Rhok%27delar,_Longbow_of_the_Ancient_Keepers>
- **Datos raros:**
  - Los demonios se esconden «en las cuatro esquinas del mundo» con nombres de PNJ inocentes: **Simone la Discreta**, **Franklin el Amistoso**, **Nelson the Nice** (sin traducción en Wowhead es-MX) y **Artorius el Afable** (en: Simone the Inconspicuous, Franklin the Friendly, Nelson the Nice, Artorius the Amiable). Base de datos Classic (Questie).
  - Antes del parche 1.8.0 el arco y el bastón se podían transformar uno en otro como Benediction/Anathema. <https://warcraft.wiki.gg/wiki/Rhok%27delar,_Longbow_of_the_Ancient_Keepers>
  - Son «armas vivas»: Rhok'delar echa flores espontáneamente. Misma fuente.
- **Ruta (7632 → 7634 / 7635 / 7636):**
  1. Núcleo de Magma: Hoja petrificada vieja.
  2. Frondavil (361), Bosque de Hierroárbol (Irontree Woods): **Vartrus, Stoma y Hastat los Ancianos** — aprox. **(48, 24)** según la wiki (coordenada no verificada en Classic; Questie no la tiene porque los Ancianos aparecen al llevar la Hoja).
  3. Demonios (misión 7636): **Simone → Cráter de Un'Goro (34.3, 40.8)** · **Franklin → Estepas Ardientes (24.8, 65.9)** · **Nelson → Silithus (24.7, 76.0)** · **Artorius → Cuna del Invierno (60.3, 13.2)**.
  4. Tendón azul (7634): Azuregos, Azshara (53.3, 80.4) o dracos Cobalto de Cuna del Invierno (~57-61, 49-54). Tendón negro (7635): Onyxia.
  5. Vuelta a Frondavil.
  - **Ruta muy buena para animar:** 4 zonas de 2 continentes + 2 bandas.
- **En Forever:** fase tardía (la Hoja sale del Núcleo de Magma).

### 6. Oración / Anatema (Benediction / Anathema)
- **EN:** Benediction · **ID 18608** · icono `inv_staff_30` · req 60 / ilvl 75 / Épica · sacerdote. **es-MX «Oración», es-ES «Bendición»** (curioso: cambia según la región). **Anatema** (Anathema, ID 18609, `inv_staff_12`). <https://www.wowhead.com/classic/item=18608>
- **Fuente:** **El Ojo de divinidad** (18646; del Alijo del Señor del Fuego, Núcleo de Magma) + **El Ojo de la Sombra** (18665; botín de demonios: Iniciados/Asesinos Hederine de Cuna del Invierno, Señores del terror y Guardias viles de élite de las Tierras Devastadas) + **Astilla de Nordrassil** (premio de la misión del sacerdote). <https://warcraft.wiki.gg/wiki/Benediction>, <https://warcraft.wiki.gg/wiki/Splinter_of_Nordrassil>
- **Datos raros:**
  - Un solo bastón con dos caras: cada 30 min «invoca» a su gemelo (sanación ↔ sombras). <https://warcraft.wiki.gg/wiki/Anathema>
  - La misión: **con el Ojo de divinidad equipado** ves a **Eris Havenfire**, un fantasma en las Tierras de la Peste del Este; hay que **salvar 50 campesinos antes de que mueran 15**. <https://warcraft.wiki.gg/wiki/Splinter_of_Nordrassil> y texto de la misión 7622.
  - En el lore, Benediction es del arzobispo Alonsus Faol. En Hearthstone, Brann dice que Executus usaba una astilla para limpiarse los dientes. <https://warcraft.wiki.gg/wiki/Benediction>
- **Ruta:** Núcleo de Magma (Ojo de divinidad) → Tierras Devastadas / Cuna del Invierno (Ojo de la Sombra) → Tierras de la Peste del Este (139): **Eris Havenfire (21.0, 18.4)**, misión 7622 «El equilibrio de la Luz y la Sombra».
- **En Forever:** fase tardía (Núcleo de Magma).

### 7. Crematoria corrupta (y la leyenda de la Crematoria)
- **EN:** Corrupted Ashbringer · **ID 22691** · icono `inv_sword_2h_ashbringercorrupt` · req 60 / ilvl 86 / Épica · espada de dos manos. es-MX y es-ES: «Crematoria corrupta». <https://www.wowhead.com/classic/item=22691>
- **Fuente:** cofre de los **Cuatro Jinetes**, Naxxramas original (Alto señor Mograine la empuñaba). <https://warcraft.wiki.gg/wiki/Corrupted_Ashbringer>
- **Datos raros:**
  - Al equiparla, el espíritu de Mograine **te susurra** 12 frases («Yo... era... puro... una vez», «Mi... hijo... me vio... morir»…) y detrás se oye al Rey Exánime; la última la dicen los dos: «Kill... them... all!». También vuelve hostil al Alba Argenta y amistosa a la Cruzada Escarlata. Misma fuente.
  - **Evento secreto del Monasterio Escarlata:** al entrar a la Catedral con ella, los cruzados se arrodillan, aparece el fantasma de Alexandros y **mata a su hijo Renault**; luego libera a Fairbanks, que cuenta la traición. <https://warcraft.wiki.gg/wiki/Corrupted_Ashbringer/Scarlet_Monastery_Event>
  - **El gran rumor de Vanilla:** la Crematoria fue de los primeros legendarios **extraídos de los archivos del juego** y el Cuidador Alen la mencionaba: los jugadores buscaron una misión secreta que nunca existió; Blizzard lo desmintió y el legendario de lanzador del que hablaban era Atiesh (1.11). <https://warcraft.wiki.gg/wiki/Ashbringer>
  - Ya no se puede conseguir: en Wrath el jinete fue sustituido. <https://warcraft.wiki.gg/wiki/Corrupted_Ashbringer>
- **Ruta (narrativa, no misión):** Naxxramas (TdP del Este 39.9, 25.8) → Monasterio Escarlata (Claros de Tirisfal) para el evento. Mograine en la Capilla de la Esperanza de la Luz: **Tirion Vadín** (Tirion Fordring) en TdP del Este (7.6, 43.7) es la otra mitad de la historia.
- **En Forever:** la más tardía (Naxx). Nota: SM sí está en Forever.

### 8. El cetro del Mar de Dunas → Señor del Escarabajo + Cristal resonador negro qiraji
- **EN:** The Scepter of the Shifting Sands · **ID 21175** · icono `inv_hammer_25` · ilvl 60 / calidad común (objeto de misión). **Cristal resonador negro qiraji** (Black Qiraji Resonating Crystal) · **ID 21176** · icono `inv_misc_qirajicrystal_05` · req 60 / **Legendaria** (montura). <https://www.wowhead.com/classic/item=21176>
- **Fuente:** la cadena más larga del Vanilla; tocar el **Gong del Escarabajo** con el cetro abre las puertas de Ahn'Qiraj para todo el reino. <https://warcraft.wiki.gg/wiki/Scarab_Lord>
- **Datos raros:**
  - Quien tocaba el gong primero se llevaba título «Señor del Escarabajo» + el tanque negro; los que tuvieran cetro durante la **Guerra de las 10 Horas** también; después, nadie más en ese reino. <https://warcraft.wiki.gg/wiki/Black_Qiraji_Resonating_Crystal>, <https://warcraft.wiki.gg/wiki/Bang_a_Gong!>
  - Fue la **primera montura legendaria** y la única hasta Dragonflight. <https://warcraft.wiki.gg/wiki/Black_Qiraji_Resonating_Crystal>
  - Primer Señor del Escarabajo del mundo: **Kalahad**, reino **Medivh (EE. UU.)**; las puertas se abrieron allí el **22-ene-2006** (luego Mannoroth 27-ene, Zul'jin 31-ene; primera de Europa: Kael'thas 30-ene). <https://warcraft.wiki.gg/wiki/Scarab_Lord>, <https://warcraft.wiki.gg/wiki/Gates_of_Ahn%27Qiraj>
  - Desde el 6-feb-2009 los reinos nuevos nacían con las puertas abiertas → el tanque se volvió inalcanzable. <https://warcraft.wiki.gg/wiki/Black_Qiraji_Resonating_Crystal>
  - Bug de 2.2.0: quien estaba montado al salir el parche **aparecía transformado en avispa voladora**. Misma fuente.
  - En Classic 2019: **90 Señores del Escarabajo en Flamegor (RU)** y **49 en Fairbanks (US)**. <https://www.wowhead.com/classic/news/90-scarab-lords-on-the-flamegor-ru-server-317770>, <https://www.wowhead.com/classic/news/the-49-classic-scarab-lords-of-fairbanks-us-pvp-317687>
- **Ruta (base de datos Classic):**
  1. Silithus (1377), Fuerte Cenarion: **Baristolth del Mar de Dunas (49.5, 36.5)** — «Lo que traerá el mañana» (8286).
  2. Guarida Alanegra: cabeza del **Señor de linaje Capazote** (Broodlord Lashlayer) (8288). Silithus: fragmentos de caparazón silítido de Hive'Ashi (8301).
  3. Tanaris (440): **Anacronos (65.3, 50.0)**. Visión en Silithus: **Lágrima cristalina (28.7, 89.1)** (8305/8519).
  4. **Fragmento rojo** (21138): Vaelastrasz en la Guarida Alanegra → Nefarian.
  5. **Fragmento azul** (21137): Tanaris, **Narain Sabelotodo** (Narain Soothfancy) **(65.2, 18.6)** — el libro de Azuregos, «rAnS0m», «Draconic for Dummies»… → invocar al tiburón **Maws** con una boya de arcanita en la Vorágine de Azshara (Bahía de las Tormentas; coordenada Classic **(sin confirmar)**). Maws es un guiño a *Tiburón*. <https://warcraft.wiki.gg/wiki/Maws>
  6. **Fragmento verde** (21139): Teldrassil, **Fuego fatuo del bosque (37.5, 47.9)** → Claro de la Luna (493), **Guardián Remulos (36.2, 41.8)** → fragmentos de la corrupción de la Pesadilla en Vallefresno (~90, 39), Feralas (~48-54, 10), Tierras del Interior (~61-65, 16-25) y Cuna del Invierno → batalla contra Eranikus en Claro de la Luna.
  7. Anacronos (65.3, 50.0) → «El poderío de Kalimdor» (8742) → cetro.
  8. Silithus: **Gong del Escarabajo (25.7, 90.9)**, junto a la entrada de AQ (28.6, 92.3) — «¡Toca el gong!» (8743).
  - **La mejor ruta para animar del video:** Silithus ↔ Tanaris ↔ Azshara ↔ Teldrassil ↔ Claro de la Luna ↔ Vallefresno ↔ Feralas ↔ Tierras del Interior ↔ BWL.
- **En Forever:** fase tardía y depende de que vuelvan BWL y el evento de AQ **(sin confirmar)**.

### 9. Riendas de destrero de la muerte (es-ES: Riendas de Hemocargador)
- **EN:** Deathcharger's Reins · **ID 13335** · icono `ability_mount_undeadhorse` · req 60 / ilvl 60 / Rara (épica desde 1.12.1) · montura. <https://www.wowhead.com/classic/item=13335>
- **Fuente:** **Barón Osahendido** (Baron Rivendare), Stratholme. Probabilidad en Classic **0,02 %**; en el parche 3.0.2 se subió al 1 %. <https://warcraft.wiki.gg/wiki/Deathcharger%27s_Reins>, <https://www.invenglobal.com/articles/12340/top-10-rarest-items-in-world-of-warcraft-classic-and-how-to-get-them>
- **Datos raros:**
  - En Classic fue el **único caballo esquelético para la Alianza** y no pedía habilidad de montar (si pidiera Equitación no-muerta, la Alianza no podría usarlo). <https://warcraft.wiki.gg/wiki/Deathcharger%27s_Reins>
  - En 1.3.0 tuvieron que parchearlo para que los tauren pudieran usarlo. Misma fuente.
  - Lore: Rivendare condenó a su caballo favorito a la no-muerte con él. Misma fuente.
- **Ruta:** Tierras de la Peste del Este (139) → Stratholme, entrada de servicio (47.9, 23.9) → Barón.
- **En Forever:** **candidata temprana** (Stratholme está en la lista). Que el objeto y su probabilidad sigan iguales **(sin confirmar)**.

### 10. Riendas del sable de hielo de Cuna del Invierno (sustituye a Kruul)
- **Por qué sustituye a Kruul/Martillo del Vacío Abisal:** Kruul es del evento previo a TBC (parche 2.0.3) y su botín era el de Kazzak; el **Martillo del Vacío Abisal** (23056) en realidad cae de **Kel'Thuzad** en Naxxramas. Material débil y confuso para el video. <https://warcraft.wiki.gg/wiki/Highlord_Kruul>, <https://warcraft.wiki.gg/wiki/Hammer_of_the_Twisting_Nether>
- **EN:** Reins of the Winterspring Frostsaber · **ID 13086** · icono `ability_mount_pinktiger` · req 60 / ilvl 60 / Épica · montura. es-ES: «Riendas del Sable de Hielo de Cuna del Invierno». <https://www.wowhead.com/classic/item=13086>
- **Fuente:** en Classic se compraba por **100 de oro** a **Rivern Ventogélido** (Rivern Frostwind) al llegar a **Exaltado con los Entrenadores de Sableinvernal**, solo Alianza (y los no elfos necesitaban además Exaltado con Darnassus). <https://warcraft.wiki.gg/wiki/Reins_of_the_Winterspring_Frostsaber>, <https://warcraft.wiki.gg/wiki/Wintersaber_Trainers>
- **Datos raros:**
  - Facción de **solo dos PNJ**; fue motivo de quejas de la Horda por no tener equivalente hasta el parche 3.2. <https://warcraft.wiki.gg/wiki/Wintersaber_Trainers>
  - Desde 4.1.0 se cambió el farmeo de reputación por 20 días de misiones diarias con un cachorro. <https://warcraft.wiki.gg/wiki/Reins_of_the_Winterspring_Frostsaber>
  - Descripción: «Domar esta raza salvaje requiere paciencia, fuerza y un buen suministro de ratones falsos y cordel». Misma fuente.
  - Que fuera la reputación más larga del Vanilla **(sin confirmar como dato medido)**.
- **Ruta:** Cuna del Invierno (618), Roca Sableinvernal: **Rivern (49.9, 9.8)** — misiones «Provisiones de Sableinvernal» (osos Dientefilo, quimeras Viento Helado), gigantes y furbolgs Fuerte Invernal.
- **En Forever:** podría estar desde el principio (zona clásica de nivel 55-60) **(sin confirmar)**.

### 11. Hoja krol (y otros botines de mundo legendarios por su rareza)
- **EN:** Krol Blade · **ID 2244** · icono `inv_sword_18` · req 51 / ilvl 56 / Épica · espada de una mano, ligada al equipar. <https://www.wowhead.com/classic/item=2244>
- **Fuente:** botín de mundo de bichos nivel 50-58. Probabilidad: «una fracción de porcentaje» **(cifra sin confirmar)**. <https://warcraft.wiki.gg/wiki/Krol_Blade>, <https://wow.gg/guides/krol-blade-transmog-guide>
- **Datos raros:**
  - Se cree que su nombre homenajea a **Monte Krol**, programador jefe de herramientas y actor de voz de Blizzard. <https://warcraft.wiki.gg/wiki/Krol_Blade>
  - Meme de servidor: se spameaba «[Krol Blade]» al estilo Chuck Norris. Misma fuente.
- **Acompañantes:**
  - **Mano de Edward el Extraño** (Hand of Edward the Odd, **ID 2243**, `inv_mace_14`, req 57 / ilvl 62 / Épica): cae de bichos élite del Núcleo de Magma, BWL y AQ. En Vanilla **tu siguiente hechizo en 4 s era instantáneo**; en 1.7.0 tuvieron que impedir que sirviera para abrir cofres y capturar cementerios en el Valle de Alterac. <https://warcraft.wiki.gg/wiki/Hand_of_Edward_the_Odd>
  - **Canción de Mirah** (Mirah's Song, **ID 15806**, `inv_sword_34`, req 55 / ilvl 61 / Rara): premio de la cadena de Scholomance de **Eva Sarkhoff** (TdP del Oeste 70.2, 73.7): «Doctor Theolen Krastinov, el Carnicero» → «Bolsa de horrores de Krastinov» → «Kirtonos el Heraldo» (5382 → 5515 → 5384). <https://warcraft.wiki.gg/wiki/Mirah%27s_Song>
- **En Forever:** Hoja krol y Canción de Mirah podrían ser tempranas (mundo y Scholomance) **(sin confirmar)**; la Mano de Edward depende de bandas.

### 12. Orbe de engaño
- **EN:** Orb of Deception · **ID 1973** · icono `inv_misc_orb_02` · req 54 / ilvl 59 / Rara · abalorio ligado al equipar. <https://www.wowhead.com/classic/item=1973>
- **Fuente:** botín de mundo «extremadamente raro» de zonas e instancias de alto nivel anteriores a TBC; en la base de datos Classic aparece en cofres sólidos de Estepas Ardientes, TdP del Este y Oeste, Azshara y Cuna del Invierno. Probabilidad exacta **(sin confirmar)**. <https://warcraft.wiki.gg/wiki/Orb_of_Deception>
- **Datos raros:** te transforma 5 min en un miembro de la facción contraria (humano↔orco, enano↔trol, elfo de la noche↔no-muerto, gnomo↔tauren) con sus animaciones y gestos; 30 min de reutilización. Misma fuente.
- **En Forever:** temprana si los botines de mundo siguen iguales **(sin confirmar)**. Gancho flojo frente a los demás: candidata a recortar.

### 13. Corcel nefasto de Xoroth (brujo) — o Destrero (paladín)
- **Corcel nefasto:** hechizo «Invocar Corcel nefasto» (Summon Dreadsteed, **hechizo 23161**, icono `ability_mount_dreadsteed`); no es un objeto. <https://www.wowhead.com/classic/spell=23161>
- **Datos raros:**
  - Los corceles nefastos son de Xoroth, montura de los Señores del Terror; los mejores pertenecen a **Lord Hel'nurath**, «el caballerizo», a quien se invoca en La Masacre. <https://warcraft.wiki.gg/wiki/Dreadsteed>, <https://warcraft.wiki.gg/wiki/Xorothian_Dreadsteed>
  - Ritual en La Masacre con **Campana de Dethmoora, Rueda de la Marcha Negra y Vela del Juicio Final**; al matar al Corcel xorothiano aparece su espíritu y te lo da. Misiones 7626/7627/7628 y 7631 (Questie).
  - En 2.4.0 pasó al entrenador; la cadena se eliminó en 4.0.1. <https://warcraft.wiki.gg/wiki/Dreadsteed>
- **Ruta (7562 → 7631):** Ventormenta / Forjaz / Orgrimmar / Pantano de las Penas (inicio) → Estepas Ardientes (46): **Mor'zul Sangredoble (12.7, 31.6)** y **Gorzeeki Ojovago (12.4, 31.6)** → Cuna del Invierno (sangre de lechuzos) → Frondavil (361): **Lord Banehollow (35.9, 44.4)**, Ulathek (40.8, 48.4), Ur'dan (36.2, 44.5) en la Guarida de Jaedenar → Estepas Ardientes → **La Masacre** (Feralas 59.2, 45.1): ritual.
- **Alternativa paladín, Destrero:** Ventormenta, **Lord Grisillo Quiebrasombras** (Lord Grayson Shadowbreaker) **(37.2, 33.3)** → Forjaz, Alto sacerdote Rohan (24.7, 8.2) → espíritus de Terrordale (TdP del Oeste) → Grimand Elmore (Ventormenta 51.8, 12.1) → agua bendita de Stratholme → **Scholomance**, redimir al Corcel caído de Darkreaver (misión 7647 «Juicio y redención»). <https://warcraft.wiki.gg/wiki/Summon_Charger>
- **En Forever:** **temprana posible** (La Masacre, Scholomance y Stratholme están). Que vuelvan las cadenas de montura de clase **(sin confirmar)**.

### 14. Ferromazo (Ironfoe)
- **EN:** Ironfoe · **ID 11684** · icono `spell_frost_frostbrand` · req 55 / ilvl 60 / Épica · maza de mano principal. <https://www.wowhead.com/classic/item=11684>
- **Fuente:** **Emperador Dagran Thaurissan**, Profundidades de Roca Negra; probabilidad estimada **0,18 %–0,59 %**. <https://www.invenglobal.com/articles/12340/top-10-rarest-items-in-world-of-warcraft-classic-and-how-to-get-them>
- **Datos raros:**
  - Efecto: «al acertar, 2 ataques extra en tu siguiente golpe». <https://warcraft.wiki.gg/wiki/Ironfoe>
  - Lore: lo forjó **Franclorn Forjamaestro**; su gemelo es **Ferroviento (Ironfel)** **(nombre es sin confirmar)**. Ironfoe era la reliquia familiar del **Mariscal Windsor**: se lo quitaron los Hierro Negro al capturarlo, y Thaurissan lo usó hasta su muerte. Misma fuente.
  - En Battle for Azeroth reaparece en el MOTHERLODE!! Misma fuente.
- **Ruta:** Montaña Roca Negra (entrada Garganta de Fuego 34.8, 85.3 / Estepas 29.4, 38.3) → Profundidades de Roca Negra → Palacio Imperial. Narrativa extra: la escolta de Windsor.
- **En Forever:** **temprana** (BRD está en la lista) **(sin confirmar que el objeto siga igual)**.

### 15. Raptor Razzashi presto / Tigre Zulian presto (es-ES: «veloz»)
- **Raptor Razzashi presto** (Swift Razzashi Raptor) · **ID 19872** · `ability_mount_raptor` · req 60 / ilvl 60 / Épica. Cae de **Bloodlord Mandokir** (Wowhead es-MX no trae traducción), Zul'Gurub. <https://www.wowhead.com/classic/item=19872>
- **Tigre Zulian presto** (Swift Zulian Tiger) · **ID 19902** · `ability_mount_jungletiger` · cae de **High Priest Thekal** (sin traducción es-MX en Wowhead). <https://www.wowhead.com/classic/item=19902>
- **Probabilidad:** ~0,6 % el tigre según InvenGlobal; otras guías dan 1-2 %; **sin cifra oficial**. <https://www.invenglobal.com/articles/12340/top-10-rarest-items-in-world-of-warcraft-classic-and-how-to-get-them>
- **Datos raros:**
  - El raptor fue el **primer raptor para la Alianza** y la única forma de que un tauren montara uno. <https://warcraft.wiki.gg/wiki/Swift_Razzashi_Raptor>
  - El tigre fue el **primer sable para la Horda**. <https://warcraft.wiki.gg/wiki/Swift_Zulian_Tiger>
  - Ambos dejaron de caer en 4.0.3 (Cataclysm rehízo Zul'Gurub); hoy solo salen en la Subasta del Mercado Negro (puja inicial 20 000 de oro). Mismas fuentes.
- **Ruta:** Vega de Tuercespina (33): entrada de Zul'Gurub (53.9, 17.6).
- **En Forever:** fase tardía; Zul'Gurub no confirmado.

### 16. Puño de Verigan (paladín, nivel 20)
- **EN:** Verigan's Fist · **ID 6953** · icono `inv_hammer_05` · req 20 / ilvl 31 / Rara · maza de dos manos. <https://www.wowhead.com/classic/item=6953>
- **Fuente:** premio de «La prueba de rectitud» (1806), cadena «El tomo del valor», solo paladines (de la Alianza en Vanilla). <https://warcraft.wiki.gg/wiki/Verigan%27s_Fist>
- **Datos raros:**
  - Lo forja **Jordan Fontana** (Jordan Stilwell) y lo bautiza en honor de **Bosch Verigan**, un amigo paladín enano ya muerto. Misma fuente.
  - El equivalente de la Horda era la **Guja templada en sangre** (Blood-Tempered Ranseur). Eliminado en 4.0.3. Misma fuente.
- **Ruta (1649 → 1806, la mejor de nivel bajo para el mapa):**
  1. Ventormenta (1519): **Duthorian Rall (39.8, 29.8)**.
  2. Páramos de Poniente (40): **Daphne Fontana** (Daphne Stilwell) **(41.7, 89.2)** — defender su casa de los Defias.
  3. Dun Morogh (1), a las puertas de Forjaz: **Jordan Fontana (52.5, 36.9)**.
  4. Materiales: **Madera de roble blanco** (Leñadores goblins, Minas de la Muerte; entrada 42.5, 71.7) · **Envío de mineral** de **Bailor Petramano, Loch Modan (36.0, 44.9)** (ogros Mo'grosh ~67-70, 24-34) · **Martillo de Jordan** (Castillo de Colmillo Oscuro, entrada Bosque de Argénteos 44.8, 67.8) · **Gema Kor** (sacerdotisas de Brazanegra; purificada por **Thundris Tejevientos, Costa Oscura 37.4, 40.1**).
  5. Vuelta a Jordan.
  - Cruza **2 continentes, 6 zonas y 3 mazmorras** en nivel 20.
- **En Forever:** **temprana** (Minas, Colmillo Oscuro y Brazanegra están). Que la misión exista igual **(sin confirmar; Forever añade paladines Renegados en la Horda)**.

---

## 3. Resumen para elegir los 12

| # | Objeto (es-MX) | ID | Ruta de misión para el mapa | Forever |
|---|---|---|---|---|
| 1 | Trueno Furioso | 19019 | Media (MC → Silithus → BWL → Silithus) | Tardía |
| 2 | Sulfuras, Mano de Ragnaros | 17182 | Corta (MC → BRD) | Tardía |
| 3 | Atiesh | 22589 | Buena (Naxx → Tanaris → AQ → Stratholme) | La más tardía |
| 4 | Quel'Serrar | 18348 | Media (La Masacre → Onyxia) | **Temprana** (Ony 9-dic) |
| 5 | Rhok'delar | 18713 | **Muy buena** (Frondavil + 4 zonas + Azshara + Ony) | Tardía |
| 6 | Oración / Anatema | 18608 | Media (MC → T. Devastadas → TdP Este) | Tardía |
| 7 | Crematoria corrupta | 22691 | Narrativa (Naxx → Monasterio Escarlata) | La más tardía |
| 8 | Cetro del Mar de Dunas / Tanque negro | 21175 / 21176 | **La mejor** (9 zonas, 2 bandas) | Tardía, depende del evento |
| 9 | Riendas de destrero de la muerte | 13335 | Corta (Stratholme) | **Temprana** |
| 10 | Sable de hielo de Cuna del Invierno | 13086 | Una zona (Cuna del Invierno) | **Temprana** |
| 11 | Hoja krol (+ Mano de Edward, Canción de Mirah) | 2244 | Sin ruta (botín de mundo); Mirah tiene mini-ruta | Temprana |
| 12 | Orbe de engaño | 1973 | Sin ruta | Temprana (gancho flojo) |
| 13 | Corcel nefasto / Destrero | hechizo 23161 | **Muy buena** (Estepas → Cuna → Frondavil → La Masacre) | **Temprana** |
| 14 | Ferromazo | 11684 | Corta (BRD) + historia de Windsor | **Temprana** |
| 15 | Raptor Razzashi / Tigre Zulian presto | 19872 / 19902 | Corta (ZG) | Tardía |
| 16 | Puño de Verigan | 6953 | **Muy buena** (Ventormenta → Poniente → Dun Morogh → Loch Modan → Costa Oscura + 3 mazmorras) | **Temprana** |

**Recortables si hace falta:** Orbe de engaño (12) y Hoja krol (11) tienen menos datos verificados; Sulfuras (2) y Ferromazo (14) tienen rutas cortas.

## 4. Pendiente / sin confirmar
- Coordenadas Classic de los Ancianos de Frondavil (wiki 48, 24, posiblemente de retail) y de Maws en Azshara (el mapa de Azshara cambió en Cataclysm: no usar la coordenada de la wiki).
- Nombres es-MX de PNJ verificados con la API de tooltips de Wowhead (`nether.wowhead.com/classic/tooltip/npc/<ID>?locale=11`). Wowhead **no** trae traducción es-MX de: Prince Thunderaan, Anachronos, los Ancianos de Frondavil, Nelson the Nice, Eris Havenfire, Lord Banehollow, Maws, Baristolth, Bloodlord Mandokir, High Priest Thekal, Highlord Mograine (usar el nombre en inglés o el del doblaje). Ironfel (gemelo de Ferromazo) sin traducción confirmada.
- Probabilidades exactas de Hoja krol, Orbe de engaño y monturas de ZG (solo estimaciones de la comunidad).
- Si Forever mantendrá los objetos, misiones y probabilidades originales: Blizzard no lo ha dicho.
