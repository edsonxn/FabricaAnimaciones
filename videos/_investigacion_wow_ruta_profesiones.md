# Investigación: «La RUTA de PROFESIONES del 1 al 300 en WoW Forever»

Hecha el **25-nov-2026** (21 días después del lanzamiento de WoW Forever, 4-nov-2026). Canal: Crónicas de Warcraft. ~27 min, formato «ruta»: 12 paradas (una por profesión) por tramos 1-75 / 75-150 / 150-225 / 225-300, Alianza y Horda. Patrocinador: Overgear.

## Cómo leer la confianza
- **OFICIAL** = notas de hotfix de Blizzard (página única que Blizzard amplía; leída hoy, cubre hasta el **23-nov**) o artículo/post azul.
- **DATOS** = datos del cliente de Forever leídos hoy en Wowhead Forever: mapa mundial (`nether.wowhead.com/forever/data/world-map`: entrenadores, PNJ, **vetas, hierbas, bancos de pesca y puntos de cuero con sus criaturas**) y tooltips de objetos/recetas (`nether.wowhead.com/forever/tooltip/...`, `locale=0` inglés y **`locale=11` = es-MX**, comprobado: «Mena de torio pesada»).
- **GUÍAS** = guías escritas para Forever (wow-professions.com/forever, Warcraft Tavern Forever, Conquest Capped…). wow-professions **no fecha** sus páginas; el autor dice en varias que lo probó «sin montura» o «en la beta»: es mezcla de beta y cliente en vivo.
- **BETA** = dato que solo consta de la beta.
- **CLASSIC-sin-confirmar** = vale en Classic; ninguna fuente de Forever lo confirma.

## Fuentes generales
- **[OFI-HF]** Blizzard, «WoW: Forever Hotfixes» (del 5 al 23-nov, publicada el 24-nov): https://worldofwarcraft.blizzard.com/news/24315281
- **[WHF-MAP]** Wowhead Forever, mapa mundial (datos `https://nether.wowhead.com/forever/data/world-map` y su versión `.../forever/mx/...` para nombres es-MX), leído el 25-nov. Coordenadas convertidas del lienzo a % de zona con la **rejilla de áreas del propio archivo** (campo `zones`: cada celda de 32 px dice a qué zona pertenece), no con el rectángulo más pequeño (eso fallaba: ponía El Cruce en Durotar y Theramore en Laderas). Comprobación: Snang (Orgrimmar) 62.8, 49.4 en [WHF-MAP] = 62.9, 49.4 en [WP-TR]; Vhan 44.0, 44.6 = 44.1, 44.5; Trianna 63.6, 21.4 = 63.6, 21.3. Error esperado ±0.2.
- **[WHF-TT]** Wowhead Forever, tooltips de objetos y recetas (inglés + es-MX), leídos el 25-nov para ~370 objetos y ~360 recetas de las guías: https://www.wowhead.com/forever/item=<id> (las páginas web de Wowhead devuelven 403/JS; la API de tooltips sí responde).
- **[WP-TR]** wow-professions.com, páginas de **entrenadores de Forever** por profesión (cada entrenador trae su `/way #uiMap x y`, o sea coordenada del mapa del juego): https://www.wow-professions.com/forever/mining-trainers (mismo patrón: herbalism-, skinning-, alchemy-, blacksmithing-, enchanting-, engineering-, leatherworking-, tailoring-, cooking-, fishing-, first-aid-trainers). Tabla de costes por rango incluida.
- **[WP-<prof>]** wow-professions.com, **guías de subida 1-300 de Forever**: https://www.wow-professions.com/forever/mining-leveling-guide (mismo patrón para cada profesión; Pesca y Cocina también tienen `fishing-and-cooking-leveling-guide`).
- **[WP-NEW-MIN] / [WP-NEW-HERB]** wow-professions, «New Ores, Bars and Camp Items» https://www.wow-professions.com/forever/mining-changes · «New Herbs, Seeds and Camp Items» https://www.wow-professions.com/forever/herbalism-changes
- **[WP-CAMP]** wow-professions, guía de campamento de Forever (los 3 objetos de cada profesión, sus planos y quién los suelta): https://www.wow-professions.com/forever/camping-guide
- **[WP-FAV]** wow-professions, Favor de comerciante (cajas, recompensas, reputación, todas las recetas por profesión con coste y reputación): https://www.wow-professions.com/forever/merchants-favor-durotar-supply-azeroth-commerce
- **[WT-PROF]** Warcraft Tavern (Luxrah), resumen de profesiones de Forever: https://www.warcrafttavern.com/forever/guides/professions/ · guías por profesión con «qué cambió»: `/forever/guides/alchemy/`, `blacksmithing/`, `enchanting/`, `engineering/`, `leatherworking/`, `tailoring/`, `skinning/`, `cooking/`, `fishing/`, `first-aid/` (sin fecha en la página).
- **[WT-LEG]** Warcraft Tavern, Legado (árbol de Profesiones): https://www.warcrafttavern.com/forever/guides/legacy/
- **Ya investigado en el canal (se cita, no se repite):** [ERR] `_investigacion_wow_errores_forever.md` (C3 bolsas, C4 Favor, C5 cajas, C11 Legado, C13 campamento) · [3060] `_investigacion_wow_errores_30_60.md` (#13 Primeros auxilios, #11 materiales) · [E60] `_investigacion_wow_errores_60.md` (C12 Esencia maleable, C13 profesiones a 300, C30 frascos) · [ORO] `_investigacion_wow_oro_forever.md` (#24 recolección, #20 encantador banco, #15/#14/#4 pesca, #13 Supervendedor, #6 recetas de Favor, #2 torio rico, precios) · [RUTA] `_investigacion_wow_ruta_forever.md` (método del mapa, pueblos y vuelos).
- **YouTube (encontrados por buscador; NO vistos, sin minuto):** «WoW Forever: Every Profession 1-300 Guide» https://www.youtube.com/watch?v=qoKCsubHt2Y · «WoW Forever First Aid Guide 1-300 - Fastest Route (Bandages + Healing Potions)» https://www.youtube.com/watch?v=hluNnUw8Ui4 · «WoW Forever First Aid 1–300 Guide» https://www.youtube.com/watch?v=MWWe9QpIR0M · «Mining + Herbalism 1-300 in WoW Forever: My Exact Route» https://www.youtube.com/watch?v=Ah5Qlo9c8pw · «WoW Forever Herbalism 1–300: Trainers, Skill Breakpoints & Route Limits» https://www.youtube.com/watch?v=T3miY_Kb2qY · «WoW Forever Alchemy Guide 1–300: Leveling, Herbs & Flasks» https://www.youtube.com/watch?v=7r0xt1AynMc · lista «WoW Forever Professions Guide» https://www.youtube.com/playlist?list=PLaNLoppjnTC4 — sirven para buscar gameplay; antes de usar un clip, mirar que sea del cliente de Forever (interfaz de profesiones con tecla K, ranura de bolsa de componentes).

---

## AVISO PARA EL GUION
- **Reglas del patrocinador (Overgear):** siempre «WoW Forever»; Forever **no** es una temporada ni un modo temporal (ni «temporada», ni «esta temporada»); nada de «la mejor profesión», tier lists, «mejor clase» ni «top DPS»; nada de Heroico/Mítico/M+/arenas/flex; no prometer botín de banda ni BiS; nada contra comprar oro, boosts o servicios; nunca «subir es aburrido» ni «sáltate el grind». Ojo con las guías: wow-professions dice de Desuello «easy but really boring» y propone «skip the first 105 points» fundiendo mena comprada: **en el guion se dice «la opción de fundir mena desde la subasta»**, nunca «saltarse».
- **Ojo con un objeto:** el material del Horno de hierro (Fishing Hut) se llama en es-MX con la palabra prohibida; decirlo en inglés («Seasonal Fish Steaks») o no nombrarlo.
- **Las guías de subida son de un autor** (wow-professions) que reconoce partes probadas en la beta; las rutas y cantidades son **estimaciones** («These numbers are estimates»). Decir «unos», «alrededor de».
- **Hotfix que envejece las guías:** el **10-nov** Blizzard bajó «the price vendors pay for some crafted armor items from Leatherworking, Tailoring, and Blacksmithing» [OFI-HF]. Cuando una guía dice «hazlas porque el vendedor paga más», puede estar desfasado.
- **Coordenadas de Ventormenta:** el mapa de ciudad de Forever **no** es el de Classic. Georgio Bolero sale en **53.3, 81.5** ([WP-TR] y [WHF-MAP] coinciden en una recta perfecta con 16 PNJ, error ≤0.2), no en el 43, 73 de las guías de Classic. Usar siempre las de este documento. En las otras 5 capitales el mapa coincide.
- **Nivel para aprender:** [WP-TR] dice que el rango Aprendiz de **todas** las profesiones no pide nivel en Forever y que la recolección no pide nivel en ningún rango; [WT-PROF] da nivel 1 (recolección) / 5 (fabricación y secundarias) para Aprendiz y 10/20/35 para Oficial/Experto/Artesano en todas. **Contradicción**: decir «Oficial pide nivel 10, Experto 20 y Artesano 35» (coinciden las dos para fabricación) y no dar nivel para Aprendiz.
- **Nombres es-MX** sacados hoy de [WHF-TT] `locale=11`. Novedades respecto a nuestros videos anteriores: las **Waylaid Crates** se llaman **«Cajón arrebatado»** (no «sin traducción»), los Craftsman's Writs son **«Libranza del artesano»**, Shipping Label = **«Etiqueta de envío»**, Mister Graphed = **«Señor Grafo»** (en [E60] pusimos «Maese Graphed»: manda Wowhead mx), Healing Potion = **«Poción de sanación»** (no «de curación»), Three Corners = **«Tres Caminos»**. Comprobar en el cliente antes del render.
- **Ya contado en otros videos (usar como dato de ruta, no como «error»):** Favor y cajas [ERR C4-C5], Legado y profesiones de fabricación [ERR C11-C12], campamento [ERR C13-C14], Primeros auxilios hace pociones y Atenciones médicas [3060 #13], tier de artesano y Esencia maleable [E60 C12-C13], frasco de poder supremo [E60 C30], recolección y precios [ORO].

---

## Contexto (sirve para todo el video)

### Cuántas profesiones y cuáles
- **9 principales** (Alquimia, Herrería, Encantamiento, Ingeniería, Herboristería, Peletería, Minería, Desuello, Sastrería) y **3 secundarias** (Cocina, Primeros auxilios, Pesca). **Límite: 2 principales por personaje; las 3 secundarias se suman a ellas.** Las secundarias **no se pueden desaprender**; las principales sí (X roja en la ventana de profesiones y confirmación escrita) y se vuelve a empezar de cero [WT-PROF]. → GUÍAS.
- **No hay Joyería** en Forever (comentario de un lector en [WT-PROF]; no está en ninguna lista de profesiones). Las 12 paradas del video son exactamente las 12 que existen. → GUÍAS.
- **Ninguna profesión da bonus pasivo** (ni vida por Minería ni crítico por Desuello): su valor viene de lo que fabricas y de los beneficios del campamento [WT-PROF]. Racial: el **tauren** con **Cultivo** recoge hierbas sin Herboristería (Blizzard lo arregló el 17 y 19-nov para Marregal y Loto cárdeno) [OFI-HF]; el **gnomo ya no recibe +15 de Ingeniería** ([WP-ENG]: «Gnomes don't get +15 Engineering skill in Forever»; [WT-ENG]: su pasiva ahora reduce la probabilidad de que los cacharros fallen). → OFICIAL / GUÍAS.
- **Ventana de profesiones nueva** (tecla **K**, separada del libro de hechizos), con buscador, filtros, seguimiento de recetas, botón «Crear todo» y **ranura de objetivo opcional** para encantar [WT-PROF, WT-BS]. Desencantar no está en el libro: está en la caja de Encantamiento de esa ventana [WP-ENCH]. → GUÍAS.

### Cuánto cuesta entrenar (y qué pide)
| Rango | Tope | Habilidad mínima | Nivel | Coste (principales) | Coste (secundarias) |
|---|---|---|---|---|---|
| Aprendiz | 75 | — | ver aviso | **10 c** | **1 p** |
| Oficial | 150 | 50 | 10 | **5 p** | **5 p** |
| Experto | 225 | 125 | 20 | **50 p** | **1 o** (es un libro: Cocina, Pesca, Primeros auxilios) |
| Artesano | 300 | 200 (secundarias 225) | 35 | **5 o** | misión (sin coste de entrenador) |
- Fuente: tablas de [WP-TR] (iconos de cobre/plata/oro leídos en el HTML) «sin descuento de reputación»; [ORO #24] ya daba 10 c / 5 p / 50 p / 5 o para recolección. **Total para llevar una principal al 300: 5 o 55 p 10 c** (más las recetas). El hotfix del **19-nov** arregla que los cielonatos no recibieran el 10 % de Honorable en equitación, lo que confirma que los entrenadores aplican descuento por reputación [OFI-HF]. → GUÍAS (cifras) / OFICIAL (descuento existe).
- **Artesano no lo enseña cualquiera:** en fabricación solo entrenadores especiales (ver cada parada); en secundarias, una misión [WT-PROF].

### Entrenadores en las 6 capitales (coordenadas del mapa de ciudad de Forever) [WP-TR; comprobadas con WHF-MAP]
Formato: Aprendiz / Oficial / (Experto). Los de recolección enseñan 1-300.

**Horda**
| Profesión | Orgrimmar | Cima del Trueno | Entrañas |
|---|---|---|---|
| Minería | Makaru 73.1, 26.3 | Brek Pezuña Pétrea 34.5, 57.7 | Brom Killian 56.0, 37.1 |
| Herboristería | Jandi 55.5, 39.7 | Komin Pezuña Invernal 50.0, 40.1 | Martha Alliestar 54.1, 49.7 |
| Desuello | Thuwd 63.2, 45.4 | Mooranta 44.5, 42.8 | Killian Hagey 70.2, 59.1 |
| Alquimia | Whuut 55.8, 33.1 / Yelmak 56.7, 33.0 | Kray 46.8, 34.4 / Bena Winterhoof 46.6, 33.2 | Doctor Martin Felben 46.7, 74.5 / Doctor Marsh 51.3, 74.1 / **Experto: Doctor Herbert Halsey 47.9, 73.1** |
| Herrería | Ug'thok 80.7, 23.6 / Snarl 79.6, 23.2 / **Experto: Saru Steelfury 82.3, 23.0** | Thrag Stonehoof 39.4, 56.9 / Karn Stonehoof 39.5, 55.3 | Basil Frye 60.0, 29.0 / James Van Brunt 61.2, 30.3 |
| Encantamiento | Jhag 53.5, 38.4 / Godan 53.9, 38.4 | Mot Dawnstrider 44.9, 39.0 / Teg Dawnstrider 44.9, 37.7 | Malcomb Wynn 62.3, 60.5 / Lavinia Crowe 62.4, 61.6 |
| Ingeniería | Thund 75.9, 24.4 / Nogg 75.8, 25.4 / **Experto: Roxxik 76.0, 25.1** | (no hay) | Graham Van Talen 75.3, 72.7 / Franklin Lloyd 76.3, 73.3 |
| Peletería | Kamari 63.2, 44.6 / Karolek 62.8, 44.3 | Mak 42.2, 43.3 / Tarn 42.1, 43.0 / **Experto: Una 41.7, 42.6** | Dan Golthas 70.8, 58.6 / Arthur Moore 70.2, 57.6 |
| Sastrería | Snang 62.9, 49.4 / Magar 63.5, 50.0 | Vhan 44.1, 44.5 / Tepa 44.5, 45.4 | Victor Ward 70.2, 29.7 / Rhiannon Davis 70.1, 30.1 / **Experto: Josef Gregorian 70.8, 30.6** |
| Cocina | Zamja 57.5, 53.9 | Aska Mistrunner 50.8, 52.9 | Eunice Burch 62.2, 44.6 |
| Pesca | Lumak 69.8, 29.2 | Kah Mistrunner 56.1, 46.9 | Armand Cromwell 80.7, 31.4 |
| Primeros auxilios | Arnok 34.1, 84.4 | Pand Stonebinder 29.2, 21.0 | Mary Edras 73.5, 55.5 |

**Alianza**
| Profesión | Ventormenta (mapa de Forever) | Forjaz | Darnassus |
|---|---|---|---|
| Minería | Gelman Stonehand 59.1, 37.8 | Geofram Bouldertoe 50.2, 26.1 | (no hay; Kurdram Stonehammer en Auberdine, Costa Oscura 38.2, 41.0) |
| Herboristería | Tannysa 54.4, 84.0 (Shylamiir 31.4, 63.0) | Reyna Ramapiedra 55.7, 59.0 | Firodren Llamaluna 47.9, 68.6 |
| Desuello | Maris Granger 72.1, 62.2 | Balthus Stoneflayer 39.7, 32.3 | Eladriel 64.2, 22.1 |
| Alquimia | Tel'Athir 55.6, 85.6 / Lilyssia Nightbreeze 55.7, 86.1 | Vosur Brakthel 66.5, 55.4 / Tally Berryfizz 66.6, 55.3 | Milla Fairancora 55.3, 22.8 / Sylvanna Forestmoon 56.1, 24.1 / **Experto: Ainethil 54.9, 24.0** |
| Herrería | Dane Lindgren 64.1, 36.9 / Therum Deepforge 63.6, 36.8 | Groum Stonebeard 52.1, 41.9 / Rotgath Stonebeard 51.9, 42.4 / **Experto: Bengus Deepforge 52.4, 41.2** | (no hay) |
| Encantamiento | Betty Quin 53.1, 73.8 / Lucan Cordell 53.1, 74.3 | Thonys Pillarstone 60.4, 44.9 / Gimble Thistlefuzz 59.8, 45.5 | Lalina Summermoon 58.9, 12.8 / Taladan 58.6, 13.2 |
| Ingeniería | Sprite Jumpsprocket 61.8, 30.7 / Lilliam Sparkspindle 62.2, 30.4 | Jemma Quikswitch 67.8, 44.2 / Trixie Quikswitch 67.6, 43.1 / **Experto: Springspindle Fizzlegear 68.5, 43.5** | (no hay) |
| Peletería | Randal Valor 72.2, 62.8 / Simon Peletero 71.7, 62.9 | Gretta Bueneje 39.0, 32.7 / Fimble Bueneje 40.2, 33.7 | Darianna 64.5, 21.0 / Faldron 64.9, 21.6 / **Experto: Telonis 64.4, 21.5** |
| Sastrería | Lawrence Schneider 53.4, 81.5 / Sellandus 52.3, 83.4 / **Experto: Georgio Bolero 53.3, 81.5** | Uthrar Threx 43.7, 28.2 / Jormund Petrocejas 43.3, 28.9 | Trianna 63.6, 21.3 / Me'lynn 63.2, 22.3 |
| Cocina | Stephen Ryback 78.2, 53.2 | Daryl Riknussun 60.0, 36.7 | Alegorn 48.9, 21.2 |
| Pesca | Arnold Leland 55.0, 69.6 | Grimnur Stonebrand 48.1, 6.5 | Astaia 47.8, 56.7 |
| Primeros auxilios | Shaina Fuller 52.9, 44.7 | Nissa Firestone 54.9, 58.5 | Dannelor 51.7, 12.5 |
- **Novedad de Forever para entrenar:** (1) **Dalaran vuelve y tiene entrenadores de la Alianza** que enseñan **del 1 al 225** en Alquimia (Linzy Blackbolt), Herrería (Alard Schmied), Encantamiento (Vanessa Sellers) y Sastrería (Charles Worth), más Cocina y Primeros auxilios: mapa de Montañas de Alterac 16.8-19.7, 60.4-63.4 [WP-TR; WHF-MAP]. (2) **Isla Zephras** tiene entrenadores de todas las profesiones en Valanaar y Aldea Shen'dar, para los dos bandos [WP-TR]. (3) **Shen'dralas** (zona casi de la Horda, ver [RUTA]) tiene a **Jarael** (Peletería 1-225, 42.6, 78.1) y **Melanori** (Sastrería 1-225, 43.7, 77.6; pide una cadena de 5 misiones; el autor duda si enseñar hasta Experto es un error) [WP-TR]. (4) **Claros del Río** tiene minero (Grungle 77.8, 52.0; Wowhead mx lo llama «Anodín»: comprobar), herreros (Gur'dok, Horda, 60.0, 46.3; Alphonse Dumas 64.5, 82.0), ingeniero goblin (Melbin Powderfuse 77.8, 50.9), cocinero (Gorg, Horda) y pescador (Krix 79.3, 54.8) [WP-TR; WHF-MAP]. (5) **Monte Hyjal**: Kaylaena Springwhisper enseña Ingeniería de Artesano (60.2, 61.4) [WP-ENG; WHF-MAP]. → GUÍAS + DATOS.
- **Entrenadores júnior (nuevos, solo 1-75 de recolección)** en cada zona inicial: Minería Norzsh (Durotar 40.5, 68.1), Vartha Rockmane (Mulgore 44.3, 78.4), Walter Mason (Tirisfal 32.2, 65.8), Sally Swiftwrench (Dun Morogh 28.8, 67.8), Kelsey Fargo (Elwynn 47.2, 32.2), Fanorran Stilloak (Teldrassil 58.2, 41.5); lo mismo en Herboristería y Desuello [WP-TR]. Varios tienen **ID de PNJ ≥ 247 000** en [WHF-MAP] (Emrys Flintbeard 267338, Zor'la 267329…): son PNJ nuevos de Forever. → DATOS.
- **Zephras sin entrenador al empezar:** la misión «Harvesting Windstones» (ID 93552) de Aldea Thendal te deja elegir un libro que **enseña la profesión**: «**Minería para torpes**» (Mining for Dummies, objeto 247840), «**Cosecha salvaje**» (Wild Harvest, 247841) o «**Recolección de pelambres para principiantes**» (Pelt Collecting for Beginners, 247846); cada uno da +2 de habilidad [WP-MIN; WT-PROF; WHF-TT]. → DATOS (nombres) / GUÍAS.

### Bolsas de componentes (5.ª ranura) [ERR C3]
- Hay una **ranura propia para bolsa de componentes** junto a las 5 normales; la Sastrería las fabrica: **Bolsa de componentes de lino 6 casillas** (6 madejas de lino + 6 hilo burdo), **de lana 8** (pide **Tinte cerúleo**, que hace la Alquimia), **de tejido mágico 12** y **de paño rúnico 14** (estas dos son recetas de Favor, 60 de Favor, Amistoso, habilidad 190 y 215) [WHF-TT spells 1257013/1257017/1257443/1257465; WP-FAV]. Hay versiones de recolección de 4 casillas y los vendedores de Zephras venden bolsas de profesión de aprendiz (hotfix 5-nov) [WT-PROF; OFI-HF]. → DATOS / OFICIAL.
- Bolsas normales tras el hotfix del **11-nov**: Bolsa de tejido mágico roja **14 casillas** (5 madejas), Mochila de seda verde y negra **12**, Bolsa de lana verde y roja **10** [OFI-HF]. Bolsa de lino roja 8 (era 6) [WT-TAIL].

### Legado (puntos por profesión) [ERR C11, C12]
- **1 punto por llegar a 150, 225 y 300** en cada una de las **6 de fabricación** (Alquimia, Herrería, Encantamiento, Ingeniería, Peletería, Sastrería) = 18 posibles; la recolección y las secundarias **no** dan [WT-LEG; ERR C11]. → OFICIAL (Blizzard es-MX, en [ERR]).
- **Árbol de Profesiones** [WT-LEG]: **Horas extra** (Working Overtime, 5 rangos, +4 % por rango de probabilidad de subir habilidad), **Cosecha abundante** (Bountiful Harvest, 5 rangos, +20 % por rango de materiales «escasos»), **Regateo** (2 rangos, −5 % en vendedores), Luremaster (2 rangos, 25 % de pescar uno extra con señuelo), Master Chef (5 rangos, 10 % de receta doble), Performance Bonus (3 rangos, 5 % de recibir el doble de Favor al entregar un cajón) y Dedicated Study (1 rango, +1 a tu profesión más baja; con todo a 300, 2-4 esencias elementales). Dos huecos «To be added in a future update». Luremaster, Master Chef, Performance Bonus y Dedicated Study: **sin traducción oficial comprobada** (decir en inglés). Primeros auxilios tiene además «Field Medicine» (acorta el Recently Bandaged en el mundo abierto) según [WT-FA]. → GUÍAS.

### Favor de comerciante (resumen para la ruta) [ERR C4-C5; WP-FAV]
- **Campamentos:** Horda = Logística y suministros de Durotar, **al oeste de El Cruce, Los Baldíos**: vendedores en **49.4-49.8, 28.8-30.0** ([WHF-MAP]: Boticaria Durelle 49.8, 29.4, Gor'mak 49.8, 29.6, Beneris 49.6, 29.8, Fundefusibles 49.8, 29.6, Patani 49.6, 29.6, Jim'bek 49.6, 29.4, Aza'bek 49.6, 29.4, Okamache 49.6, 28.8) y Dokimi (entrega) 50.0, 29.2 [ERR C4]. Alianza = Autoridad Comercial de Azeroth, **Tres Caminos, oeste de Montañas Crestagrana**: Marcy Baker 9.6, 71.0; Nina Fuegocertero 10.8, 72.4; Stondry Martilloscuro 10.4, 74.6; Alynsia 11.2, 71.4; Fritz Fizzle 10.4, 74.2; Daniel Hilvanante 10.0, 72.6; Mivin Tejesombra 10.0, 72.8; Kalsey Sanden 10.8, 72.6; Huey Vallesol 8.4, 72.0 [WHF-MAP]. Los dos venden **las mismas recetas**. → DATOS.
- **Cajón arrebatado** (Waylaid Crate): se llena con UNA de las pilas que pide y se entrega: Aprendiz 5 de Favor (crudo) / 10 (fabricado), Oficial 10/20, Experto 15/30, Artesano «Not known yet»; Aprendiz y Oficial piden nivel 10, Experto 20, Artesano 35 [WP-FAV; ERR C5]. **La reputación no sale de los cajones sino de las «Libranzas del artesano»** (Craftsman's Writs): Oficial 75, Experto 125, Artesano 200 de reputación, una vez al día cada una, y no hace falta tener la profesión [WP-FAV]. La primera vez: **Etiqueta de envío** → 2000 de reputación y 50 de Favor [WP-FAV; ERR C5]. Desde Amistoso, el **Recibo de entrega falsificado** (15 de Favor) convierte un cajón vacío en 50 de reputación [WP-FAV]. → GUÍAS.
- **Recetas por profesión (número):** Alquimia 28, Herrería 61, Cocina 6 (todas «smoothies» de Espíritu), Encantamiento 39, Ingeniería 26, Peletería 81, Sastrería 67 = **308 recetas de Favor** [WP-FAV] (dentro de las «más de 600» nuevas que dijeron los desarrolladores [WT-PROF]). Las armas y armaduras de Favor **se ligan al recogerlas**: solo para ti [WP-FAV]. → GUÍAS.
- **Recompensas finales:** Riendas del kodo de carga 6000 de Favor + Exaltado + nivel 60 + Equitación de oficial (Journeyman Riding) [WP-FAV; ERR C4 coincide]; **Certificado de alquimia/herrería/encantamiento/ingeniería/peletería/sastrería** → título de la profesión **para toda la cuenta**, visible con 300 de habilidad (1000 de Favor según [ERR C4]) [WP-FAV]; mascota (Comida de mula de carga, 1500, Reverenciado), tabardo 200 (Exaltado), Solicitud de licencia publicitaria 1200 (Honorable) → juguete del cartel de profesión. → GUÍAS.

### Campamento (lo que cambia la ruta de TODAS las profesiones) [ERR C13; WP-CAMP]
- Alguien enciende una hoguera y cada jugador alrededor pone **un objeto de su profesión** (1 h de reutilización); te sientas 1 minuto y recibes **Beneficios del campamento** durante 1 h, con todo lo que aporten los objetos. Hoguera básica 3 objetos, de oficial 5, de experto 10 [WP-CAMP]. La **Hoguera básica** viene con Cocina 1 y se fabrica con 1 Madera simple [WP-CAMP; WP-COOK]. **Hoguera de oficial**: plano de Lord Serpentis (Cuevas de los Lamentos), Cocina 90 (hotfix 10-nov: también 90 para colocarla) [WP-CAMP; OFI-HF]. **Hoguera de experto**: plano de Slavecrusher Grox en el Bastión de Krol'dok (Claros del Río); se aprende con 200 pero se usa con 220 («might be a bug») [WP-CAMP]. → GUÍAS / OFICIAL.
- **Cada profesión tiene 3 objetos** (Cocina 2): el 1.º lo enseña el entrenador (habilidad 20), el 2.º y el 3.º son **planos que sueltan jefes** (140 y 300). Lista completa con sus jefes en cada parada. Varios son **estaciones de fabricación obligatorias** (Expositor de curtido, Rueca, Telar, Yunque, Forja maestra, Laboratorio de alquimia, Forja arcana, Banco de trabajo de anarquista, Fundición de magma, Horno de hierro): el autor de [WP-CAMP] dice «I haven't found any of them out in the world. They only come from camps». Se pueden comprar ya hechas en la subasta o usar la de otro jugador del campamento sin tener la habilidad [WP-CAMP]. → GUÍAS.
- **Cifra de Blizzard:** en la semana 1 se usaron **28 696 386 objetos de campamento** (Warcraft Tavern, «by the numbers», 18-nov; ya en [E60]). → OFICIAL.

### Combinaciones de profesiones que tienen sentido en Forever (y por qué) — sin «la mejor»
1. **Minería + Herrería o Ingeniería:** la Herrería de Forever pide del orden de **500 a 1220 barras de torio** solo para el tramo 270-300 [WP-BS]; la mena se apila ahora de 20 en 20 [WP-NEW-MIN]; las barras nuevas (azerotio, torio pesado) salen de materiales que solo da la Minería. Da Legado (Herrería/Ingeniería) a 150/225/300. → GUÍAS.
2. **Herboristería + Alquimia:** la lista de compra de [WP-ALCH] pide ~1 000 hierbas del 1 al 300. Y en Forever la Alquimia fabrica **tintes** (cerúleo, magenta, esmeralda) que piden la Sastrería y la Peletería [WHF-TT; WT-ALCH]: el alquimista tiene clientes nuevos. → GUÍAS / DATOS.
3. **Desuello + Peletería:** el Expositor de curtido es estación obligatoria para muchas recetas, y la Tienda de campamento (objeto de Peletería) da **descanso**: es la profesión que más ayuda a subir de nivel [WP-CAMP; ERR C13]. → GUÍAS.
4. **Sastrería + Encantamiento:** ninguna necesita recolección y lo que coses lo desencantas [WP-ENCH]. En Forever además: las **bolsas de componentes** las hace la Sastrería y el **tier de artesano de banda** necesita **Esencia maleable de la Naturaleza**, que «se consigue al desencantar» objetos de Cima Hyjal o Cavernas del Túmulo [E60 C12; WHF item 274030]. → DATOS.
5. **Dos de recolección (Minería + Desuello o Herboristería):** para oro directo ([ORO #24], RageGaming) — **pero** no dan Legado [ERR C11]; si el personaje principal es recolector, que un alternativo suba fabricación. → GUÍAS.
6. **Tauren:** con Cultivo recoge hierbas sin Herboristería, así que puede llevar dos de fabricación y alimentar la Alquimia igual [OFI-HF 17/19-nov arreglan Cultivo]. → OFICIAL (Cultivo existe y funciona con hierbas que «tienes la habilidad»: ojo, el hotfix dice «on herbs you have the Herbalism skill for»; comprobar en el cliente si pide Herboristería para hierbas de alto nivel).
7. **Las 3 secundarias para todos:** no ocupan hueco; Primeros auxilios hace las **pociones de sanación** (antes de Alquimia), Cocina enciende el campamento y su comida da **+5 % de experiencia por muertes** [3060 #13; PS/WT, en E60 C29], Pesca da cofres en mar abierto sin habilidad [ORO #15]. → GUÍAS.

---

## LAS 12 PARADAS

### Parada 1 · MINERÍA (recolección; alimenta Herrería e Ingeniería)
- **Explicación por tramo** [WP-MIN, guía de Forever]:
  - **1-65 (Cobre):** cualquier zona inicial; la guía prefiere **Durotar (Horda)** y **Bosque de Elwynn (Alianza)**. En Mulgore, una cueva con 5 vetas de cobre de reaparición muy rápida («you can basically stay inside the cave»), con forja en la **Excavación de Bael'dun** (34.6, 53.2). En Teldrassil no hay vetas de cobre: hay **Fragmentos de ámbar** (nuevos) y la forja más cercana está en Darnassus. Fundir el cobre en Cerrotajo / Villadorada / Rémol / Kharanos / Aldea Shen'dar tras cada vuelta.
  - **Opción de fundir desde la subasta hasta 105:** ~140 Mena de cobre + 70 Mena de estaño → 1-65 cobre, 65-75 estaño, 75-105 bronce (70 barras); 105-120 plata (35-45 menas). Con +5 de bonus se pica hierro desde 120 (no 125).
  - **65-125 (Estaño y plata):** **Los Humedales** (Alianza; una cueva «llena de vetas de estaño y de incendicita»), **Bosque de Argénteos** (Horda; cueva con 3 vetas que reaparecen cada ~2 min) o **Laderas de Trabalomas**; alternativas: Páramos de Poniente, Los Baldíos, Vallefresno, Sierra Espolón. Estaño desde 65, plata desde 75. **En Forever los mobs reaparecen mucho más rápido** («you need to outlevel them by quite a few levels»).
  - **125-175 (Hierro y oro):** **Tierras Altas de Arathi** (con montura o nivel alto; 4 cuevas) o **Las Mil Agujas** (la más segura hacia nivel 30); Desolace. Hierro desde 125, oro desde 155. Opcional: fundir ~20 Mena de hierro hasta 135 y ~22 Mena de oro de 155 a 175.
  - **175-245 (Mitril y veraplata):** **Tierras del Interior** o **Tanaris**. Mitril desde 175, veraplata desde 230. Aprender Artesano (pide 200) antes de salir.
  - **245-275 (Torio pequeño):** **Cráter de Un'Goro**, **Las Tierras Devastadas** o **Frondavil** (2-3 vetas en dos cuevas; la Alianza no puede picar en la mina de la Armería de la Guarnición).
  - **275-300 (Torio rico):** **Un'Goro**, **Tierras de la Peste del Este**, **Cuna del Invierno** o **Las Estepas Ardientes** (élites 57-58 en una parte de la ruta).
- **Alianza vs Horda:** mismos minerales; cambian la cueva del tramo 65-125 (Humedales para la Alianza, Argénteos/Trabalomas para la Horda) y que **Darnassus no tiene entrenador de Minería** (el más cercano, Kurdram Stonehammer en Auberdine) [WP-MIN].
- **Lo nuevo de Forever** [WP-NEW-MIN; OFI-HF; WHF-MAP]:
  - **Entrenadores júnior** en cada zona inicial (1-75, sin fundición) y **Vetas de cobre pobres** en las zonas iniciales (294 puntos en [WHF-MAP]) + **Fragmentos de ámbar** en Teldrassil (19 puntos normales y 56 grandes): los elfos de la noche pueden picar en casa; dan Mena de cobre pero solo suben habilidad hasta 20.
  - **La mena se apila de 20** (era 10).
  - **Mena nueva:** **Mena de torio pesada** (Heavy Thorium Ore, 248815) de la **Veta de torio pesada**, aparición rara en **Monte Hyjal** «con humo verde vil» → **Barra de torio pesada** (251291) con «Fundir torio pesado» (habilidad 300) **solo en la Fundición de magma** del campamento. La Alquimia la transmuta en **Barra de legionita** (251290).
  - **Materiales escasos** (salen al picar): **Pirita** (cobre, estaño, hierro; 249391), **Bauxita** (mitril; 249425), **Pecblenda** (torio; 249426) → **Barra de azerotio** (249726) con «Fundir azerotio» (275, 2 Pecblenda + 1 Carbón, en forja). Cosecha abundante (Legado) da +20 % por rango de escasos [WT-LEG].
  - **Objetos de campamento:** **Magnetita** (Lodestone, 20: poder de ataque cuerpo a cuerpo, no se acumula con Bendición de poderío) → **Jardín rocoso** (140: hace aparecer una veta común con el tiempo; plano de los Relic Guardian del Sitio de Excavación: Los Humedales) → **Fundición de magma** (300; plano de Embajador Latifuego en Profundidades de Roca Negra).
  - **Hierro espectral** en Shen'dralas (29 puntos en [WHF-MAP]): mena de misión; el hotfix del **17-nov** permite rastrearla con Encontrar minerales y sube su aparición [OFI-HF].
  - **Bonus de habilidad nuevo:** **Luz de mina crepuscular** (+4; 275028), recompensa de «A Miner Problem», misión de la **Alianza en Claros del Río** [WP-MIN].
  - El 20-nov Blizzard reparó la forja y el yunque de **Toron Rockhoof en la Cima de la Eternidad** (Hyjal 69.0, 47.4) para fundir allí [OFI-HF].
- **Lugar/mapa** (densidad máxima de vetas por casilla de 10 % en [WHF-MAP]; n = vetas en esa casilla):
  - Cobre: Durotar 53.1, 25.5 (n=17) y 45.5, 35.1 · Elwynn 42.0, 76.8 (n=13) · Dun Morogh 72.7, 54.3 (n=23, junto a la Cantera de Gol'Bolar 68.7, 58.1) · Mulgore 56.7, 53.4 (n=33) · Tirisfal 53.7, 43.9 · Zephras 44.9, 54.8 (n=31; Zephras es la zona con más cobre: 299). Vetas pobres: Durotar 43.8, 64.7 (n=25, Valle de los Retos). Ámbar: Teldrassil 56.9, 27.6 (n=17) y grandes 53.0, 51.1.
  - Estaño: Los Humedales 47.5, 62.3 (n=9; ahí mismo 14 vetas de incendicita: 47.3, 62.2 = la cueva) · Argénteos 58.1, 72.8 (n=13) · Laderas 28.3, 55.7 · Baldíos 46.3, 84.0 · Páramos 31.9, 45.2.
  - Hierro/oro: Arathi hierro 54.4, 76.0 y 33.2, 44.7; oro 84.5, 32.8 · Mil Agujas hierro 12.7, 34.8 y 43.3, 35.5 · Claros del Río (zona nueva) tiene **la mayor cantidad de vetas de hierro del mapa: 133** (55.5, 44.7).
  - Mitril/veraplata: Tierras del Interior 56.7, 43.9 (n=11 de cada) · Tanaris 33.5, 44.6 y 55.1, 74.6.
  - Torio pequeño: Un'Goro 67.3, 15.9 (n=12) · Tierras Devastadas 65.9, 30.8 · Frondavil 36.2, 54.6.
  - Torio rico: Cuna del Invierno 55.9, 85.8 (n=9) · Peste del Este 47.1, 54.6 · Estepas 65.4, 35.8 · **Monte Hyjal 110 vetas de torio rico** (63.6, 86.7; 76.3, 75.4) y **119 puntos de torio pesado** (35.6, 83.3; 35.8, 47.6; 64.5, 86.0).
  - Hierro espectral: Shen'dralas 54.6, 76.1.
  - Entrenadores: ver Contexto + Claros del Río (Grungle 77.8, 52.0).
- **En pantalla:** Mena de cobre / Copper Ore (2770) · Mena de estaño / Tin Ore (2771) · Mena de hierro / Iron Ore (2772) · Mena de oro / Gold Ore (2776) · Mena de mitril / Mithril Ore (3858) · Mena de veraplata / Truesilver Ore (7911) · Mena de torio / Thorium Ore (10620) · **Mena de torio pesada / Heavy Thorium Ore (248815)** · Pirita / Pyrite (249391) · Bauxita / Bauxite (249425) · Pecblenda / Pitchblende (249426) · Barra de azerotio / Azerothium Bar (249726) · Barra de torio pesada / Heavy Thorium Bar (251291) · Pico de minero / Mining Pick (2901) · Minería para torpes / Mining for Dummies (247840) · Luz de mina crepuscular / Twilight Mine Light (275028) · Plano: fundición de magma / Blueprint: Molten Foundry (273122). YouTube: «WoW Forever Heavy Thorium Vein Mount Hyjal» · «WoW Forever Molten Foundry smelt heavy thorium» · «WoW Forever mining 1-300 route» · «WoW Forever Poor Copper Vein».
- **Curioso:** la **única mena nueva** de Forever no se puede fundir en ninguna forja de Azeroth: hace falta montar un campamento y poner encima una Fundición de magma, cuyo plano está en Profundidades de Roca Negra. Y Claros del Río, una zona que no existía, es la que más vetas de hierro tiene de todo el mapa (133).
- **Fuente:** [WP-MIN] · [WP-NEW-MIN] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [WHF-TT]
- **Confianza:** DATOS (vetas, objetos, nombres) · GUÍAS (ruta, cantidades) · OFICIAL (hierro espectral, forja de Toron). El «humo verde vil» de la veta pesada: GUÍA (solo lo dice wow-professions).

### Parada 2 · HERBORISTERÍA (recolección; alimenta Alquimia, Primeros auxilios y la cocina de hierbas)
- **Explicación por tramo** [WP-HERB]:
  - **1-70:** cualquier zona inicial (Flor de paz, Hojaplata; Raíz de tierra desde 15). «La reaparición es tan rápida que sin montura no terminas la vuelta».
  - **70-115:** **Bosque de Argénteos** (sur; vueltas cortas), **Loch Modan** o **Costa Oscura** (Marregal, Brezospina; Alga estranguladora desde 85). Aprender Oficial (50).
  - **115-170:** **Laderas de Trabalomas** o **Sierra Espolón** (tres zonas: mobs 14-15, 25 o más gente pero más Sangrerregia). Hierba cardenal, Acérita salvaje, Sangrerregia desde 125, Vidarraíz desde 150. Aprender Experto (125).
  - **170-205:** **Vega de Tuercespina** o **Tierras Altas de Arathi** (Pálida, Espina de oro, Mostacho de Khadgar desde 185).
  - **205-230:** **Tanaris** o **La Garganta de Fuego** (Loto cárdeno, Flor de fuego). **Aprender Artesano (200) antes de ir: allí no hay entrenador.**
  - **230-270:** **Tierras del Interior** (Solea, Loto cárdeno, Champiñón fantasma desde 245 en una cueva, Sansam dorado).
  - **270-300:** **Frondavil** (Solea, Gromsanguina, Sansam dorado, Hojasueño, Salviargenta de montaña, Flor de plaga).
  - Bonus: Té de espina de oro (+15, receta de Henry Stern en Zahúrda Rajacieno, Cocina 175), Guantes de herborista (+5), encantamiento de guantes (+2/+5), Guantes de boticario (+2, misión de la Horda).
- **Alianza vs Horda:** la ruta es neutral; cambian los entrenadores. Los **Claros del Río** son una alternativa nueva para 170-205 (77 Espina de oro y 64 Sangrerregia en [WHF-MAP]).
- **Lo nuevo de Forever** [WP-NEW-HERB; OFI-HF; WHF-TT]:
  - Entrenadores júnior 1-75 y **Flor de paz marchita** / **Hojaplata atrofiada** en las zonas iniciales (319 y 325 puntos en [WHF-MAP]).
  - **3 hierbas nuevas en Monte Hyjal:** **Hojapesadilla** (Marefoil, 248823; una Hojasueño rara y brillante, da también Hojasueño), **Salvia demoníaca** (Demonsage, 248821; una Salviargenta de montaña rara y brillante) y **Loto de la muerte** (Death Lotus, 248822; de cualquier hierba de Hyjal **solo con el encantamiento de guantes «Lotus Claw»**).
  - **Escasos:** Liquen con volantes (249399; de Raíz de tierra, Marregal, Brezospina, Alga), Rosínea (249424; de Sangrerregia, Pálida, Espina de oro…), Estranguladora (249274; «not known yet»).
  - **Semillas** en 4 rangos (comunes, poco comunes, inusuales, escasas) que se plantan en el **Invernadero** o se combinan en el **Injertador de semillas**. Hotfix **19-nov**: el Injertador vuelve, ahora puede fallar y ya no admite semillas escasas [OFI-HF].
  - **Objetos de campamento:** **Vela de incienso** (20; Intelecto, no se acumula con Intelecto Arcano) → **Invernadero** (140; plano de Shadetooth, Sitio de Excavación: Los Humedales) → **Injertador de semillas** (300; plano de Tendris Malatroncos, La Masacre).
- **Lugar/mapa** (densidad [WHF-MAP]):
  - Zonas iniciales: Flor de paz marchita Durotar 44.3, 65.2 (n=27) · Hojaplata atrofiada Elwynn 54.2, 44.5 (n=19) · Hojaplata Mulgore 55.2, 64.8 · Teldrassil 67.7, 54.7.
  - Argénteos: Brezospina 54.5, 76.6 (n=12); Marregal 54.6, 27.0 · Costa Oscura Marregal 36.1, 85.6 · Loch Modan Brezospina 65.5, 42.9.
  - Laderas: Sangrerregia 36.5, 56.1 · Sierra Espolón: Hierba cardenal 35.0, 64.2.
  - Tuercespina: Mostacho de Khadgar 35.1, 15.2 (n=14); Espina de oro 45.7, 35.9 · Arathi: Mostacho 56.6, 35.1.
  - Tanaris: Flor de fuego 44.9, 34.7; Loto cárdeno 46.9, 65.5 · Garganta de Fuego: Flor de fuego 44.9, 63.6.
  - Tierras del Interior: Champiñón fantasma 57.6, 42.6 (n=9) y 57.7, 81.8; Solea 65.4, 47.4.
  - Frondavil: Flor de plaga 42.9, 43.6; Gromsanguina 44.8, 85.0; Hojasueño 53.6, 14.9.
  - **Monte Hyjal:** Hojapesadilla 44.3, 75.2 (n=11); Salvia demoníaca 45.2, 86.8 (n=13) y 62.6, 33.8.
- **En pantalla:** Flor de paz / Peacebloom (2447) · Hojaplata / Silverleaf (765) · Marregal / Mageroyal (785) · Brezospina / Briarthorn (2450) · Sangrerregia / Kingsblood (3356) · Mostacho de Khadgar / Khadgar's Whisker (3358) · Loto cárdeno / Purple Lotus (8831) · Solea / Sungrass (8838) · Hojasueño / Dreamfoil (13463) · **Hojapesadilla / Marefoil (248823)** · **Salvia demoníaca / Demonsage (248821)** · **Loto de la muerte / Death Lotus (248822)** · Liquen con volantes / Frilled Lichen (249399) · Rosínea / Rosecap (249424) · Semillas de hierbas comunes / Commonplace Herb Seeds (268415) · Cosecha salvaje / Wild Harvest (247841) · Plano: invernadero (273106). YouTube: «WoW Forever Marefoil Demonsage Mount Hyjal» · «WoW Forever Greenhouse herb seeds camp» · «WoW Forever herbalism 1-300».
- **Curioso:** en Forever puedes **cultivar** hierbas: las semillas que salen al recoger se plantan en un invernadero de campamento. Y el Loto de la muerte de Hyjal no se ve en el mapa: sale de cualquier hierba, pero solo si llevas un encantamiento en los guantes.
- **Fuente:** [WP-HERB] · [WP-NEW-HERB] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [WHF-TT]
- **Confianza:** DATOS (nodos, objetos) · GUÍAS (ruta) · OFICIAL (Injertador). «Lotus Claw»: GUÍA (sin id del encantamiento).

### Parada 3 · DESUELLO (recolección; alimenta Peletería)
- **Explicación por tramo** [WP-SKIN; WT-SKIN]:
  - **Regla:** hace falta **5 × nivel del bicho** (nivel 30 → 150); por debajo del 20, menos (nivel 11 → 10; +10 por nivel). Encantar guantes – Desuello: un nivel más.
  - **1-75:** **en Forever los bichos de las zonas iniciales dan puntos hasta 75.** Horda: Jabalíes moteados del Valle de los Retos (Durotar, nv. 1-2). Alianza: Lobos jóvenes y Lobos del bosque de Villanorte (Elwynn, nv. 1-2).
  - **75-150:** Horda: **Los Baldíos**, campamento de raptores al oeste de **Fuerte del Norte** (61.2, 54.7; Sunscale Scytheclaw, Zhevra Charger, Ornery Plainstrider; nv. 16-18) hasta 150. Alianza: **Loch Modan** (Elder Mountain Boar, Black Bear Patriarch, Loch Crocolisk; 75-130) y **Los Humedales**, Excavación de Whelgar (34.5, 49.7; Mottled Scytheclaw/Razormaw nv. 25-27; 130-150).
  - **150-225:** **cueva de yetis de Laderas de Trabalomas** (delante: Vicious Gray Bear y Starving Mountain Lion hasta 160; dentro, Cueva de las Laderas: Cave Yeti y Ferocious Yeti nv. 30-32, «reaparecen tan rápido que puedes quedarte dentro»; llegan Horda desde Molino Tarren y Alianza desde Costasur) o **Bosque del Ocaso**, El Vergel Pútrido / Condena de Roland (worgens Nightbane nv. 26-29).
  - **225-280:** **Feralas, Vega Cicatriz Feral** (54.6, 56.5): Feral Scar Yeti, Enraged Feral Scar, Hulking Feral Scar (nv. 43-46; los de 46 desde 230). Horda desde Campamento Mojache, Alianza desde Bastión Plumaluna.
  - **280-300:** **Un'Goro**, oeste del cráter, desde el Refugio de Marshal: Diemetradon, Pterrordax, Elder Diemetradon, Frenzied Pterrordax (nv. 50-55).
  - Alternativas por rango ([WT-SKIN]): 150+ incluye **Claros del Río**; final: Tierras Devastadas, Frondavil, Peste del Oeste, Azshara, Cuna del Invierno, Silithus, Peste del Este.
- **Alianza vs Horda:** cambia el tramo 75-150 (Baldíos para la Horda; Loch Modan + Humedales para la Alianza). **La Horda tiene un cuchillo con bonus:** Cuchillo para desollar afilado (+3; 269716), recompensa de «Unwelcome Guests» en Los Baldíos [WP-SKIN].
- **Lo nuevo de Forever** [WT-SKIN; OFI-HF; CC-ORO en ORO #24; WHF-TT]:
  - Entrenadores júnior 1-75 y bichos iniciales que dan puntos hasta 75.
  - **Cada criatura se desuella una sola vez** (desde la beta) [ORO #24]; hotfix **17-nov**: «Skinners can no longer skin a few creatures that typically are not skinnable» [OFI-HF].
  - **Materiales nuevos:** escasos **Cuero prístino** (249427, nivel 25), **Pellejo prístino** (249428, nivel 45) y **Escama prístina** (249429, nivel 60); **Pellejo vil** (248824) y **Cuero vil** (248825) de nivel 60 [WHF-TT]. El Cuero prístino cayó de ~1 o 60 p (beta) a ~5 p el 13-nov [ORO #24].
  - **Objetos de campamento:** **Silla de campamento** (20; +2 % de crítico, no se acumula con el aura de lechúcico) → **Guía de campo** (140; cualquiera la lee y aprende Rastrear bestias; plano de Lady Anacondra, Cuevas de los Lamentos) → **Banco de trabajo de trampero** (300; una trampa; plano de La Bestia en Cumbre de Roca Negra o del Maestro de canes Loksey en el Monasterio Escarlata) [WP-CAMP].
  - Misión «Rough Wolf Pelts»: se cancela si desaprendes Desuello (hotfix 6-nov) [OFI-HF].
- **Lugar/mapa** ([WHF-MAP] trae «puntos de cuero» con la criatura y su % de botín):
  - 1-75: Durotar 42.9, 23.2 (Elder Mottled Boar 40 %) · Elwynn 44.1, 71.1 (Stonetusk Boar, Young Forest Bear).
  - 75-150: Baldíos 60.2, 33.8 (Zhevra Charger 73 %, Ornery Plainstrider 72 %) y 54.0, 44.0 · Loch Modan 63.2, 40.8 (Loch Crocolisk 59 %, Black Bear Patriarch 71 %, Elder Mountain Boar 73 %) · Humedales 29.8, 46.6 (Mottled Razormaw 72 %).
  - 150-225: Laderas 57.8, 27.4 y 41.7, 42.3 (osos y leones de montaña) · **cueva de yetis en el mapa de Montañas de Alterac 36.5, 85.9** (Cave Yeti 72 %; Wowhead la asigna a Alterac, en el borde con Laderas) · Bosque del Ocaso 62.8, 68.2 y 64.6, 35.6 (Nightbane 71-72 %).
  - 225-280: Feralas 51.6, 59.2 (Hulking/Enraged Feral Scar, Feral Scar Yeti; cuero grueso) y 57.4, 59.8.
  - 280-300: Un'Goro 36.0, 35.2 y 35.5, 46.0 (Frenzied Pterrordax 51 %, Elder Diemetradon 50 %; cuero basto).
  - Nuevo: **Claros del Río 65.2, 53.1 y 58.4, 55.6** (Mature Paletusk, Wildplains Patriarch, Roving Tallstrider ~76 % de cuero pesado) · **Monte Hyjal 74.3, 36.6** (Nightsaber Guardian, Wildbreath Chimaerok; cuero basto).
- **En pantalla:** Cuero ligero / Light Leather (2318) · Cuero medio / Medium Leather (2319) · Cuero pesado / Heavy Leather (4234) · Cuero grueso / Thick Leather (4304) · Cuero basto / Rugged Leather (8170) · **Cuero prístino / Pristine Leather (249427)** · **Pellejo prístino / Pristine Hide (249428)** · **Escama prístina / Pristine Scale (249429)** · Pellejo vil / Fel Hide (248824) · Cuchillo para desollar / Skinning Knife (7005) · **Cuchillo para desollar afilado / Keen Skinning Knife (269716)** · Recolección de pelambres para principiantes (247846). YouTube: «WoW Forever skinning 1-300» · «WoW Forever Feral Scar Vale yeti skinning» · «WoW Forever Pristine Leather skinning».
- **Curioso:** en Forever ya no hay «desollar el bicho que mató otro dos veces»: cada criatura se desuella una sola vez. Y el material «prístino» que en la beta valía 1 oro 60 bajó a 5 platas en la primera semana [ORO #24].
- **Fuente:** [WP-SKIN] · [WT-SKIN] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [WHF-TT] · [ORO #24]
- **Confianza:** DATOS (puntos de cuero, objetos) · GUÍAS (ruta) · OFICIAL (hotfixes). «Una vez por criatura»: BETA (Conquest Capped) sin desmentir.

### Parada 4 · ALQUIMIA
- **Explicación por tramo** [WP-ALCH; lista de compra total en la guía]:
  - **1-55 (Aprendiz):** 9 **Elixir de fuerza menor** (receta nueva de Forever; 9 Hojaplata) hasta 10; 45 Elixir de defensa menor (Hojaplata + Flor de paz) hasta 55.
  - **55-150 (Oficial):** 10 Poción de maná menor; 28 Elixir de entereza menor (56 Raíz de tierra) hasta 90; 30 Elixir de sabiduría hasta 120; 10 Poción de maná inferior; 20 Aceite de fuego (40 Pargo de fuego) de 130 a 150.
  - **150-225 (Experto, 50 p):** 15 Elixir de poder de fuego; 36 Poción de maná (Alga + Sangrerregia) hasta 195; 36 Poción de Protección contra la Naturaleza (receta ligada al recogerla: Bronk o Logannas en Feralas, Glyx Brewright en Tuercespina, Pestlezugg en Tanaris) hasta 225.
  - **225-300 (Artesano):** 26 Protección contra la Naturaleza; transmutaciones de hierro→oro y mitril→veraplata «de paso» (1 h de reutilización); Elixir de intelecto superior; 47 Aceite escama pétrea; 44 Elixir de defensa superior (la receta se vende como «Elixir de defensa excelente», «probably a bug») hasta 300. Alternativa: 55 Poción de maná excelente.
  - **Materiales aproximados:** 1-150 ≈ 83 Flor de paz, 54 Hojaplata, 50 Marregal, 56 Raíz de tierra, 60 Brezospina, 10 Alga, 40 Pargo de fuego, 152 viales; 150-225 ≈ 72 Alga, 51 Sangrerregia, 36 Vidarraíz; 225-300 ≈ 26 Vidarraíz, 26 Alga, 25 Mostacho, 44 Solea, 25 Carolina, 47 Anguila escama pétrea.
- **Alianza vs Horda:** Experto con **Doctor Herbert Halsey (Entrañas)** o **Ainethil (Darnassus)**; Artesano con **Rogvar** (Rocal, Pantano de las Penas 48.5, 55.8; Horda) o **Kylanna Windwhisper** (Bastión Plumaluna, Feralas 32.6, 43.8; Alianza). La Alianza tiene además a **Linzy Blackbolt en Dalaran** (1-225). **Los dos bandos:** **Maestro micólogo Shurome** en el **Santuario Esmeralda de Frondavil (51.5, 82.0)** enseña **del 1 al 300**, y deja aprender Artesano **sin pedir 200** («I'm not sure if this is an oversight by Blizzard») [WP-ALCH; WP-TR; WHF-MAP].
- **Lo nuevo de Forever** [WT-ALCH; WP-FAV; WP-CAMP; OFI-HF; WHF-TT]:
  - **Las pociones de sanación se fueron a Primeros auxilios** («everyone can craft them»): el alquimista ya no las hace.
  - Recetas nuevas: Elixir arcano menor (247754; su precio de venta bajó de 25 c a 5 c el 10-nov), Elixir del oso pardo (250351), Elixir de astucia (250328); la Poción de ira ahora la usan también los druidas. El 10-nov se renombró «Receta: Elixir de poder de fuego superior» a «Elixir de poder sagrado» [OFI-HF].
  - **Tintes de alquimista** («Crafted by alchemists»): Tinte cerúleo (249409), Tinte magenta (249430), Tinte verde esmeralda (249431), y Ácido sulfúrico (249410): los piden la Sastrería (bolsas de componentes) y otras recetas.
  - **28 recetas de Favor** (Boticaria Durelle / Nina Fuegocertero): pociones de 30 s (Poción de ensalmador, Spellblasting, Frenzy; 45 de Favor, habilidad 130-140) hasta Elixir del oso pardo (300, 240 de Favor, Honorable); Elixir de ferocidad 275 / 180 de Favor / Honorable [WP-FAV; ERR C4].
  - **Objetos de campamento:** **Pozo de maná** (20; regeneración de maná, no se acumula con Bendición de sabiduría) → **Fermentador** (140; necesario para algunas recetas; plano de Rath'mael en las Ruinas de Lordaeron, Tirisfal 61.6, 73.7) → **Laboratorio de alquimia** (300; **los frascos ya no exigen ir a Scholomance**; plano de **Ras Levescarcha** en Scholomance, el mismo que suelta la receta del Frasco de poder supremo [E60 C30]) [WP-CAMP; WT-ALCH].
  - Transmutación nueva: Barra de torio pesada → **Barra de legionita** [WP-NEW-MIN].
- **Lugar/mapa:** Shurome, Frondavil 51.5, 82.0 (Santuario Esmeralda 50.9, 81.3) · Rogvar, Pantano de las Penas 48.5, 55.8 · Kylanna Windwhisper, Feralas 32.6, 43.8 · Pestlezugg (Tanaris, Gadgetzan 51.2, 27.5) · Halsey Entrañas 47.9, 73.1 · Ainethil Darnassus 54.9, 24.0 · Linzy Blackbolt, Alterac 18.6, 62.4 · campamento de Favor (Baldíos 49.8, 29.4 / Crestagrana 10.8, 72.4).
- **En pantalla:** Elixir de fuerza menor (receta 1245250) · Elixir de defensa menor (7183) · **Elixir arcano menor / Minor Arcane Elixir (247754)** · **Elixir del oso pardo / Elixir of the Grizzly (250351)** · Elixir de astucia / Elixir of Cunning (250328) · Receta: poción de Protección contra la Naturaleza (6057) · Receta: elixir de defensa excelente (13478) · Tinte cerúleo / Cerulean Dye (249409) · Barra de legionita / Legionite Bar (251290) · Laboratorio de alquimia / Alchemy Laboratory (279990) · Pozo de maná (279956) · Fermentador (279970) · Vial vacío (3371) / emplomado (3372) / de cristal (8925). YouTube: «WoW Forever alchemy 1-300 Shurome Felwood» · «WoW Forever Alchemy Laboratory camp flask» · «WoW Forever alchemy healing potions removed first aid».
- **Curioso:** en Forever el alquimista **perdió las pociones de sanación** (ahora son de Primeros auxilios, o sea de todo el mundo)… pero ganó un laboratorio portátil: los frascos, que antes solo se hacían dentro de Scholomance, ahora se fabrican junto a una hoguera.
- **Fuente:** [WP-ALCH] · [WT-ALCH] · [WP-FAV] · [WP-CAMP] · [OFI-HF] · [WHF-TT] · [E60 C30]
- **Confianza:** OFICIAL (hotfixes) · DATOS (objetos, tintes) · GUÍAS (ruta, Shurome «sin 200» puede corregirse).

### Parada 5 · HERRERÍA
- **Explicación por tramo** [WP-BS]:
  - **1-75:** 30 Piedra de afilar tosca, 30 Piedra de pulir tosca (guardar 10), 36 Piedra de pulir burda (guardar todas). Martillo de herrero obligatorio. **Hotfix 10-nov: la Piedra de pulir burda da puntos hasta 90 (era 75)** [OFI-HF].
  - **75-140 (Oficial):** 5 Vara de plata; 15 Leotardos de bronce toscos; Brazales de bronce estampados; 20 Piedra de pulir pesada (guardarlas para el 180); Guanteletes de bronce plateados. ≈ 300 Barras de bronce en 1-150.
  - **140-210 (Experto, 50 p; Saru Steelfury en Orgrimmar o Bengus Deepforge en Forjaz):** 40 **Brazales de hierro verde** (240 Barras de hierro) hasta 175; Piedra de pulir sólida; 20 Brazales de escamas doradas (100 Barras de acero); 17 Pantalones de placas de mitril (204 Barras de mitril).
  - **210-300 (Artesano con Brikk Finoficio en Bahía del Botín, los dos bandos):** con el plano de Espuelas de mitril (botín del mundo) o con piezas de mitril pesado; 240-270 Cinturón y Brazales de placas imperiales (misiones de **Derotain Sorbelodo**, Tanaris 51.4, 28.6, nivel 50; 20 Barras de torio cada misión); 270-300 Botas/Leotardos radiantes o de torio, o piezas imperiales: **entre 508 y 1220 Barras de torio** según los planos que consigas.
  - Especialización (Forjador de armaduras / de armas) a 200 y nivel 40, opcional.
- **Alianza vs Horda:** Experto en Orgrimmar (Horda) / Forjaz (Alianza); la Alianza tiene además a **Alard Schmied en Dalaran (1-225)**; **Darnassus y Teldrassil no tienen herrero** (Delfrum Flintbeard en Auberdine). Especialistas: Forjador de armaduras Grumnus Steelshaper (Forjaz 50.2, 42.7) / Okothos Ironrager (Orgrimmar 79.9, 23.6); de armas Ironus Coldsteel (Forjaz 50.9, 43.2) / Borgosh Corebender (Orgrimmar 79.7, 23.4) [WP-TR].
- **Lo nuevo de Forever** [WP-BS; WT-BS; WP-FAV; WP-CAMP; OFI-HF; E60 C13]:
  - **Plan de Placas bendecidas (8 planos nuevos)** que suben 240-300 y caen con ~2 % de bichos del mundo; el peto, de las **arpías Wormwing de Monte Hyjal** [WP-BS].
  - **61 recetas de Favor** (Gor'mak / Stondry Martilloscuro): conjuntos de malla y placas por rol (Guard's, Veteran's, Acolyte's, Protector's, Crusader's → Sentinel's, Officer's, Prefect's, Warder's, Justicar's), Cestus de torio, Gran maza de torio, **Guja de legionita** (300) y **Coraza/Yelmo/Leotardos de torio enriquecido** (300) [WP-FAV].
  - Barras nuevas: **azerotio** y **torio pesado** «para recetas de final» [WP-NEW-MIN].
  - Las piedras de afilar y de peso **ahora se acumulan con venenos y Viento Furioso** [WT-BS].
  - **Objetos de campamento:** **Rueda de afilar** (20; Fuerza, no se acumula con Tótem de Fuerza de la tierra) → **Yunque** (140; plano de Gilnid en Las Minas de la Muerte) → **Forja maestra** (300; «needed for many Blacksmithing recipes»; plano del Señor gólem Argelmach en Profundidades de Roca Negra) [WP-CAMP].
  - Hotfix **17-nov**: «The Old Ways» da la receta de Leotardos de guerra orcos con un objeto; la Maza de bronce pasa a ligarse al equiparla [OFI-HF]. 20-nov: forja de Toron Rockhoof en Hyjal reparada.
  - El tier de artesano de banda pide **Herrería 300** [E60 C13] (no prometer botín).
- **Lugar/mapa:** Brikk Finoficio, Bahía del Botín 29.0, 75.4 [WHF-MAP] · Derotain Sorbelodo, Tanaris 51.4, 28.6 · Saru Steelfury Orgrimmar 82.3, 23.0 · Bengus Deepforge Forjaz 52.4, 41.2 · Alard Schmied, Alterac 19.7, 63.4 · Toron Rockhoof, Hyjal 69.0, 47.4 · arpías Wormwing (Monte Hyjal; sin coordenada del grupo).
- **En pantalla:** Barra de bronce (2841) · Barra de hierro (3575) · Barra de acero (3859) · Barra de mitril (3860) · Barra de torio (12359) · Martillo de herrero (5956) · Piedra de pulir burda (3478) · Diseño: espuelas de mitril (7989) · **Diseño: peto de placas bendecidas / Plans: Blessed Plate Chest (251446)** · Diseño: botas radiantes (12697) · Barra de azerotio (249726) · Plano: forja maestra (273113) · Plano: yunque (273086). YouTube: «WoW Forever blacksmithing 1-300» · «WoW Forever Blessed Plate plans drop» · «WoW Forever Master Forge camp».
- **Curioso:** para el último tramo de Herrería la guía calcula **entre 508 y 1 220 barras de torio** solo de 270 a 300: la diferencia depende de que encuentres o no un par de planos en la subasta.
- **Fuente:** [WP-BS] · [WT-BS] · [WP-FAV] · [WP-CAMP] · [OFI-HF] · [WHF-TT] · [E60 C13]
- **Confianza:** OFICIAL (hotfixes) · GUÍAS (ruta, cantidades, % de los planos ~2 %) · DATOS (planos y nombres).

### Parada 6 · ENCANTAMIENTO
- **Explicación por tramo** [WP-ENCH]:
  - **1-70 (Aprendiz):** 1 Vara de cobre rúnica (Vara de cobre + **Mota de magia**, reactivo nuevo de vendedor); 18 Encantar brazal: aguante inferior (Mota de magia) hasta 20; 50 Encantar pechera: aguante inferior (Polvo extraño) o Brazal: desvío menor (Esencia mágica inferior) hasta 70. **Desencantar también da puntos** (uno por cada uno hasta 20). «Forever added a few new low level recipes, so the first 70 points are cheaper».
  - **70-150 (Oficial):** dos caminos (Polvo extraño o Esencia mágica inferior): Absorción menor, Vara de plata rúnica, Varita mágica superior, Intelecto inferior de 2M o Capa/Botas.
  - **150-225 (Experto, 50 p):** **un solo entrenador por bando**: **Hgarth** (Horda; en un risco sobre el Refugio Roca del Sol, Sierra Espolón 49.2, 57.1) y **Kitta Vientofuego** (Alianza; lo alto de la **Torre de Azora**, Elwynn 64.9, 70.6); la Alianza también **Vanessa Sellers en Dalaran**. Vara dorada rúnica, Aceite de maná menor, 44 Encantar botas: agilidad inferior, Vara de veraplata rúnica, Aceite de zahorí inferior, Capa: defensa superior.
  - **225-300 (Artesano): solo Annora en Uldaman** (entrada trasera; Tierras Inhóspitas 44.2, 12.2 es el rótulo de Uldaman) — «aparece solo cuando matas todo lo de su zona» — ~12 o para aprender todo; recetas de 230+ solo las enseña ella. Guantes: agilidad (Polvo de visión) hasta 250; Aceite de maná inferior (Kania, Silithus); Escudo: aguante superior; Aceite de zahorí; **Vara rúnica de arcanita** (Lorelae Wintersong, Claro de la Luna) para el 300.
  - Materiales: 1-150 ≈ 19 Motas de magia + 257 Polvo extraño (o 293 Esencias mágicas inferiores); 150-225 ≈ 61 Polvo de alma + 31 Polvo de visión; 225-300 ≈ 34 Polvo de visión, 104 Polvo onírico, 88 Polvo de ilusión.
  - Macro que recomienda la guía para encantar en serie (usa la ranura de objetivo opcional).
- **Alianza vs Horda:** Experto en dos sitios distintos (Sierra Espolón / Elwynn, más Dalaran para la Alianza); Artesano igual para los dos (Uldaman).
- **Lo nuevo de Forever** [WT-ENCH; WP-FAV; WP-CAMP; OFI-HF; E60 C12; ORO #20]:
  - **Mota de magia** (247786) en el vendedor de encantamiento; en las zonas iniciales solo la venden los de Zephras y Tirisfal.
  - **Varita de práctica de novato** craftable con Encantamiento 1 [WT-ENCH]; las Varitas mágicas inferior/superior ahora dan poder con hechizos.
  - **39 recetas de Favor** (Beneris / Alynsia): **Encantar collar** (agilidad, desvío, poder de sanación, poder con hechizos, fuerza; habilidad 210, 120 de Favor, Amistoso), Encantar arma: Insight / Recovery / Revelation, **reliquias** (ídolos, tótems, libramientos) y **bastones, orbes y varita** para lanzadores [WP-FAV]. Un jugador: el primero con la fórmula de collar «cobra lo que quiera» [ORO #6].
  - **Objetos de campamento:** **Laúd encantado** (20; armadura, estadísticas y resistencias, no se acumula con Marca de lo Salvaje) → **Recuperador arcano** (140; **desencantado con bonus**, «Better disenchanting»; plano de la Sombra del archimago en la **Ciudad de Dalaran**; hotfix 10-nov: pide la Vara dorada rúnica y aplica su bonus a encantadores de nivel bajo) → **Forja arcana** (300; plano de Nanaya en **El Bancal del Creador**) [WP-CAMP; OFI-HF].
  - **Esencia maleable de la Naturaleza** (274030) **solo sale desencantando** objetos de Cima Hyjal o Cavernas del Túmulo y la piden las recetas del tier de artesano [E60 C12]. (Dato del objeto; no prometer botín).
- **Lugar/mapa:** Hgarth, Sierra Espolón 49.2, 57.2 [WHF-MAP] (Refugio Roca del Sol 47.8, 60.8) · Kitta Vientofuego, Elwynn 64.8, 70.6 (Torre de Azora 65.8, 68.1) · Vanessa Sellers, Alterac 16.8, 62.3 · Uldaman (rótulo), Tierras Inhóspitas 44.2, 12.2 · Kania (Silithus, posada de Fuerte Cenarion 52.2, 39.9) · Lorelae Wintersong (Claro de la Luna, Amparo de la Noche 48.1, 34.4).
- **En pantalla:** **Mota de magia / Mote of Magic (247786)** · Polvo extraño (10940) · Esencia mágica inferior (10938) · Polvo de alma (11083) · Polvo de visión (11137) · Polvo onírico (11176) · Polvo de ilusión (16204) · Vara de arcanita (16206) · Fórmula: vara rúnica de arcanita (16243) · Encantar collar: agilidad (receta 1249059) · Plano: recuperador arcano (273103) · Plano: forja arcana (273116). YouTube: «WoW Forever enchanting 1-300» · «WoW Forever Annora Uldaman artisan enchanting» · «WoW Forever enchant necklace».
- **Curioso:** en Forever los collares por fin se encantan… pero la fórmula no la enseña ningún entrenador: se compra con Favor en un campamento de mercaderes.
- **Fuente:** [WP-ENCH] · [WT-ENCH] · [WP-FAV] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [WHF-TT] · [E60 C12]
- **Confianza:** OFICIAL (hotfix del Recuperador) · DATOS · GUÍAS (ruta; «Annora única para Artesano» = como en Classic, confirmado por la guía de Forever).

### Parada 7 · INGENIERÍA
- **Explicación por tramo** [WP-ENG]:
  - **1-56:** 56 Polvo explosivo tosco; 28 Puñado de tornillos de cobre; 1 Llave inglesa de arco voltaico (herramienta). Empezar en Orgrimmar o Forjaz «porque allí también está el Experto».
  - **56-150 (Oficial):** 28 Bomba de cobre tosca; Polvo explosivo burdo + Dinamita burda; Contacto de plata; 25 Tubo de bronce; Mira estándar; Polvo explosivo pesado + Cacharros zumbones de bronce.
  - **150-200 (Experto, 50 p; Roxxik en Orgrimmar o Springspindle Fizzlegear en Forjaz):** Marco de bronce; 15 **Oveja explosiva**; Polvo explosivo sólido; Microajustador giromático; Granada de hierro; Tubo de mitril.
  - **200-300 (Artesano con Buzzek Giracorchete en Gadgetzan o con Kayleena Encantaflores en Monte Hyjal):** Activador inestable, Envoltura de mitril, Bomba de gran poder explosivo, Polvo explosivo denso, 20 **Trasto de torio** (Sovik en Orgrimmar / Gearcutter Cogspinner en Forjaz), 21 **Tubo de torio** (esquema ligado al recogerlo en Forever: Xizzer Fizzbolt en Cuna del Invierno o **Kor'gar en Claros del Río**).
  - Materiales: 1-150 ≈ 56 Piedra férrea, 62 Barra de cobre, 80 de bronce; 150-225 ≈ 75 Barra de mitril; 225-300 ≈ 84 de mitril, 88 Piedra densa, **186 Barras de torio**.
  - Especialización gnómica o goblin a 200 y nivel 30 (gnómica: Tinkmaster Overspark, Forjaz 69.8, 50.7 / Oglethorpe Obnoticus, Bahía del Botín 28.3, 76.3; goblin: Nixx Sprocketspring, Gadgetzan 52.5, 27.3 / Vazario Linkgrease, Trinquete 62.7, 36.3 / **Melbin Powderfuse, Claros del Río 77.8, 50.9**) [WP-TR].
- **Alianza vs Horda:** **Cima del Trueno y Darnassus no tienen ingeniero**; en Tirisfal tampoco (Graham Van Talen en Entrañas); Mulgore tiene a Twizwick Sprocketgrind en una meseta difícil sobre la Mina Ventura y Cía.; la Alianza tiene a Finbus Geargrind (Oficial) en el Bosque del Ocaso [WP-ENG].
- **Lo nuevo de Forever** [WT-ENG; WP-FAV; WP-CAMP; OFI-HF]:
  - **El gnomo ya no recibe +15** [WP-ENG]; su pasiva reduce los fallos de los cacharros [WT-ENG].
  - **26 recetas de Favor** (Fundefusibles / Fritz Fizzle): versiones **«SAF-T»** de explosivos que puede usar cualquiera (Dinamita SAF-T, Bomba de cobre SAF-T), **arma arrojadiza nueva** («Satchel of Copper/Bronze/Iron/Dark Iron Bombs», sin munición), cinturones y gafas por tipo de armadura, **Parapente goblin ultraliviano** (300, 360 de Favor, Honorable), «Stealthman 52», «Gnomish Poultryizer», «Compact Critter Carrier» [WP-FAV; WT-ENG].
  - **Lija** (Sandpaper, 249432) «Crafted by engineers», reactivo nuevo [WHF-TT].
  - **Objetos de campamento (los únicos que no dan beneficio):** **Robot de componentes** (20; vende reactivos de clase y suministros a todo el campamento) → **Robot de reparación** (140; repara a todos; plano de Sneed, Las Minas de la Muerte) → **Banco de trabajo de anarquista** (300; plano de Ezra Grimm, Stratholme) [WP-CAMP; WT-ENG].
  - Hotfixes: Granada de hierro al vendedor 1 p 25 c (era 5 p) y munición Swiftstrike/Swiftfeather ya no se liga (10-nov); arreglados los regalos de renovación goblin/gnomo y «The Mortar: Reloaded» (23-nov) [OFI-HF].
- **Lugar/mapa:** Buzzek Giracorchete, Tanaris 52.2, 27.6 · **Kayleena Encantaflores, Monte Hyjal 60.2, 61.4** · Kor'gar, Claros del Río 77.6, 50.8 · Roxxik Orgrimmar 76.0, 25.1 · Springspindle Forjaz 68.5, 43.5 · Strange Hermit (Zephras, Bosque Sombraviento 54.0, 39.0) [WHF-MAP; WP-TR].
- **En pantalla:** Piedra férrea (2835) · Puñado de tornillos de cobre (4359) · Tubo de bronce (4371) · Cacharros zumbones de bronce (4375) · Tubo de mitril (10559) · Activador inestable (10560) · Trasto de torio (15994) · Tubo de torio (16000) · Esquema: tubo de torio (16047) · **Lija / Sandpaper (249432)** · Robot de reparación (receta 1263034) · **Parapente goblin ultraliviano (receta 1266938)**. YouTube: «WoW Forever engineering 1-300» · «WoW Forever SAF-T Dynamite» · «WoW Forever Reagent Bot camp engineering» · «WoW Forever goblin glider».
- **Curioso:** la Ingeniería de Forever inventó la **seguridad infantil**: las bombas «SAF-T» están hechas para que las lance quien no es ingeniero. Y el gnomo, el ingeniero por excelencia, perdió sus 15 puntos gratis.
- **Fuente:** [WP-ENG] · [WT-ENG] · [WP-FAV] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [WHF-TT]
- **Confianza:** OFICIAL (hotfixes) · DATOS · GUÍAS (ruta; gnomo sin +15 = una guía; WT da el efecto nuevo).

### Parada 8 · PELETERÍA
- **Explicación por tramo** [WP-LW]:
  - **1-60:** 35 Cuero ligero (de Restos de cuero estropeado); 10 Pellejo ligero curtido; 20 Guantes de cuero repujado.
  - **60-130 (Oficial):** Guantes y Pantalones de cuero repujado; 20 Pellejo medio curtido; Cinturón de cuero fino; 20 Cinturón de cuero oscuro; Cuero pesado.
  - **130-205 (Experto, 50 p; Una en Cima del Trueno o Telonis en Darnassus; también Jarael en Shen'dralas):** Pellejo pesado curtido; Hombreras bárbaras (o Leotardos bárbaros); Guantes de guardián; Arnés bárbaro (Hebilla de hierro); 22 Cinta Nightscape.
  - **205-300 (Artesano; Hahrana Pielférrea en Campamento Mojache, Feralas — Horda — o Drakk Stonehand en Pico Nidal, Tierras del Interior — Alianza):** 36 Pantalones Nightscape (504 Cuero grueso) hasta 235; 36 Guanteletes de cuero maligno (Werg Thickblade en Tirisfal / Leonard Porter en Peste del Oeste) o **Zapatos de gamuza azul** (patrón nuevo) hasta 265; 49 Cinta de cuero rúnico (Jase Farlane, Capilla de la Esperanza de la Luz) hasta 300, o patrones nuevos: Brazales de cuero labrado, Brazales de gamuza azul, Brazales de escórpido cargados.
  - Materiales: 1-150 ≈ 247 Cuero ligero + 152 medio; 150-225 ≈ 292 Cuero pesado + 390 grueso; 225-265 ≈ 224 grueso + 288 basto; 265-300: 410-686 Cuero basto y 50-490 Paño rúnico.
  - Especialización (dracoescama, elemental, tribal) a 225 y nivel 40: Peter Galen (Azshara 37.6, 65.5) / Thorkaf Dragoneye (Tierras Inhóspitas 62.6, 57.5); Brumn Winterhoof (Arathi 28.2, 44.9) / Sarah Tanner (Garganta de Fuego 63.6, 75.9); Caryssia Moonhunter (Feralas 89.4, 46.5) / Se'Jib (Tuercespina 36.5, 34.1) [WP-TR].
- **Alianza vs Horda:** Experto en Cima del Trueno (Horda) / Darnassus (Alianza) / Shen'dralas (Jarael, sin bando: en la práctica de la Horda [RUTA]); Artesano en Feralas (Horda) / Tierras del Interior (Alianza); los patrones de Guanteletes malignos en Tirisfal (H) / Peste del Oeste (A).
- **Lo nuevo de Forever** [WT-LW; WP-LW; WP-FAV; WP-CAMP; OFI-HF; WHF-TT]:
  - **81 recetas de Favor** (Patani / Daniel Hilvanante): conjuntos de cuero y malla para cada rol (Brawler's, Defender's, Trapper's, Totemic, Stormrider's, Wisdom's → Prowler's, Skulker's, Warden's, Stalker's, Skirmisher's, Skycaller's, Mender's) y dos kits de armadura (Forceful Thick, Mystic Rugged) [WP-FAV].
  - **Patrones nuevos de gamuza azul**: Zapatos (252859), Brazales (252888) y Sombrero de gamuza azul (252890; necesita Máquina de coser) [WHF-TT].
  - **Estaciones:** el **Expositor de curtido** es obligatorio para muchas recetas; **hotfix 6-nov: baja de 140 a 125** y sus puntos de habilidad se bajaron 15 [OFI-HF]. La **Máquina de coser** solo se coloca con 300 «even if you buy one» (posible descuido) [WP-LW].
  - **Objetos de campamento:** **Tienda de campamento** (20; **experiencia de descanso hasta el 5 % de un nivel, una vez por hora**) → **Expositor de curtido** (125; plano de Razorclaw el Carnicero, Castillo de Colmillo Oscuro) → **Máquina de coser** (300; plano de Vectus, Scholomance) [WP-CAMP; ERR C13].
  - Especializaciones: **se quitaron las estadísticas de resistencia**; dracoescama reorganizada por rol (verde sanadores, azul lanzadores, negra físicos) [WT-LW]. Hotfix 23-nov: «Pattern: Centaur Hoofwarmers» ya se puede aprender [OFI-HF].
  - **Salero** (Salt Shaker): Sal de roca profunda → refinada cada 3 días, para Pellejo basto curtido [WT-LW].
- **Lugar/mapa:** Hahrana Pielférrea, Feralas 74.4, 43.1 · Drakk Stonehand, Tierras del Interior 13.4, 43.3 · Jarael, Shen'dralas 42.6, 78.1 · Una, Cima del Trueno 41.7, 42.6 · Telonis, Darnassus 64.4, 21.5 · Jase Farlane (Capilla de la Esperanza de la Luz, Peste del Este 71.9, 49.1) · campamento de Favor.
- **En pantalla:** Cuero ligero/medio/pesado/grueso/basto (2318/2319/4234/4304/8170) · Sal (4289) · Hilo rúnico (14341) · Patrón: guanteletes de cuero maligno (15725) · Patrón: cinta de cuero rúnico (15756) · **Patrón: zapatos de gamuza azul / Pattern: Blue Suede Shoes (252859)** · Patrón: sombrero de gamuza azul (252890) · **Tienda de campamento / Camp Tent (receta 1229432)** · Expositor de curtido (1263031) · Plano: máquina de coser (273121). YouTube: «WoW Forever leatherworking 1-300» · «WoW Forever Blue Suede Shoes pattern» · «WoW Forever Camp Tent rested xp».
- **Curioso:** en Forever existe el patrón **«Zapatos de gamuza azul»** (Blue Suede Shoes): unos zapatos con nombre de canción de Elvis que, según la guía, sirven para subir del 235 al 265 «y el vendedor paga más por ellos».
- **Fuente:** [WP-LW] · [WT-LW] · [WP-FAV] · [WP-CAMP] · [OFI-HF] · [WHF-TT] · [ERR C13]
- **Confianza:** OFICIAL (Expositor 125) · DATOS (patrones) · GUÍAS (ruta, cantidades; el argumento del precio de venta puede haber cambiado con el hotfix del 10-nov).

### Parada 9 · SASTRERÍA
- **Explicación por tramo** [WP-TAIL]:
  - **1-55:** 30 Madeja de paño de lino; 28 Cinturón de lino.
  - **55-140 (Oficial; Magar/Rhiannon Davis/Jormund Petrocejas/Me'lynn):** 37 Madeja de paño de lana; 22 Capa de lana; Sobrehombros de lana de doble costura; 54 Madeja de paño de seda (≈ 812 Paños de seda hasta 185); Capucha de seda celeste; 15 Mochila de seda pequeña.
  - **140-200 (Experto, 50 p; Josef Gregorian en Entrañas o Georgio Bolero en Ventormenta):** Madeja de tejido mágico; 20 Chaleco de seda carmesí; 17 Pantalones de seda carmesí; 22 Leotardos de tejido mágico negros.
  - **200-300 (Artesano; Daryl Stack en Molino Tarren — Horda — o Timothy Worthington / Timoteo Valián en Isla Theramore — Alianza):** Sobrehombros de tejido mágico negros; Madeja de paño rúnico; **17 Bolsa de tejido mágico roja** (14 casillas tras el hotfix) hasta 225; Cinturón de paño rúnico; Guantes de paño rúnico (Qia, Vista Eterna); 250-280 **Puños de paño rúnico** (patrón nuevo: **Pexmit** en Monte Hyjal, 10 o, o misión de la Horda «Threading a Solution» de Kal'tinzan en Flora Antigua); 280-300 Sobrehombros de paño rúnico o Turbante tejido de zahorí.
  - Materiales: 1-150 ≈ 60 lino, 111 lana, 220 seda, 115 tejido mágico; 150-225 ≈ 592 seda + 605 tejido mágico; 225-280 **≈ 1 440 Paños rúnicos**.
- **Alianza vs Horda:** Experto Entrañas (H) / Ventormenta (A) / Charles Worth en Dalaran (A) / Melanori en Shen'dralas; Artesano Laderas (H) / Marjal (A); el Hilo rúnico no se vende en Theramore («buy it before you go»); los Puños de paño rúnico: la Horda puede sacarlos por misión.
- **Lo nuevo de Forever** [WT-TAIL; WP-TAIL; WP-FAV; WP-CAMP; OFI-HF; WHF-TT]:
  - **Bolsas de componentes** (lino 6, lana 8, tejido mágico 12, paño rúnico 14) y bolsas más grandes (hotfix 11-nov) — ver Contexto.
  - **67 recetas de Favor** (Jim'bek / Mivin Tejesombra): conjuntos de tela por escuela (fuego, escarcha, arcano, sombras, sagrado, sanación) y las 2 bolsas de componentes.
  - Recetas cambiadas con poder con hechizos (Sobrehombros de lana reforzados, Capucha de seda celeste) y **Toga/Leotardos de sombras afiligranados** de mazmorras de nivel bajo [WT-TAIL].
  - **Objetos de campamento:** **Estandarte de facción** (20; Espíritu para tu bando, no se acumula con Espíritu divino) → **Rueca** (140; obligatoria para muchas recetas; plano del Unstable Sentinel en la **Ciudad de Dalaran**) → **Telar** (300; plano de la Baronesa Anastari, Stratholme) [WP-CAMP]. El Telar solo se fabrica con 300, así que **las recetas del Círculo Cenarion (Mishta, Silithus) que darían puntos de 285 a 300 piden un Telar que aún no puedes hacer**: «you would need a camp where another tailor already placed a Loom» [WP-TAIL].
- **Lugar/mapa:** Daryl Stack, Laderas 63.7, 20.8 (Molino Tarren 61.5, 20.0) · Timothy Worthington, Marjal 66.2, 51.8 · Qia, Cuna del Invierno 61.2, 37.2 · **Pexmit, Monte Hyjal 48.2, 33.6** (también marcado «raro» en [WHF-MAP]: «can be tricky to find») · Kal'tinzan, Hyjal 13.6, 53.0 (Flora Antigua 13.3, 49.9) · Mishta, Silithus 49.8, 36.4 · Josef Gregorian Entrañas 70.8, 30.6 · Georgio Bolero Ventormenta 53.3, 81.5 · Charles Worth, Alterac 17.7, 60.4 · Melanori, Shen'dralas 43.4, 77.8.
- **En pantalla:** Paño de lino / lana / seda / tejido mágico / rúnico (2589 / 2592 / 4306 / 4338 / 14047) · Madeja de paño rúnico (14048) · Seda de araña Tejehierro (14227) · **Patrón: puños de paño rúnico / Pattern: Runecloth Cuffs (254124)** · Patrón: guantes de paño rúnico (14481) · Bolsa de componentes de lino (receta 1257013) · Rueca (1263032) · Telar (1263080) · Plano: rueca (273099). YouTube: «WoW Forever tailoring 1-300» · «WoW Forever Pexmit Mount Hyjal» · «WoW Forever Red Mageweave Bag 14 slot» · «WoW Forever reagent bag tailoring».
- **Curioso:** el último tramo de Sastrería de Forever tiene una trampa: las recetas que te llevarían al 300 necesitan un Telar… y el Telar solo lo puede fabricar alguien que ya tenga 300. O encuentras a otro sastre con su telar puesto, o subes por otro camino.
- **Fuente:** [WP-TAIL] · [WT-TAIL] · [WP-FAV] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [WHF-TT]
- **Confianza:** OFICIAL (bolsas) · DATOS · GUÍAS (ruta; lo del Telar puede ser un descuido que Blizzard cambie).

### Parada 10 · COCINA (secundaria; enciende el campamento)
- **Explicación por tramo** [WP-COOK]:
  - **1-50:** 55 Pececito luminoso o Caballa de piel escurridiza.
  - **50-150 (Oficial, mismo entrenador):** 55 Pargo de lodo boquilargo o Atún blanco arco iris hasta 100; 53 Siluro mostacherizo hasta 150.
  - **150-225 (Experto = libro «Libro de cocina para expertos», 1 o):** **Wulan** en Aldea Cazasombras, Desolace (Horda) o **Shandrina** en Lago Mystral, Vallefresno (Alianza). 28 Almejas endiabladas goblin; 55 Raptor asado o Trucha cabeza de mitril.
  - **225-300 (Artesano = misión «Clamlette Surprise» de Dirge Hojágil en Gadgetzan, nivel 35, Cocina 225):** llevar 12 Huevos gigantes, 10 Carne de almeja sabrosa y 20 Queso curado de Alterac; luego 72 Serviola moteada o Branquirrojo (recetas de Gikkix, Puerto Bonvapor) hasta 285 y 18 Sopa de pargo nocturno hasta 300.
- **Alianza vs Horda:** solo cambia el libro de Experto (Desolace / Vallefresno) y los vendedores de recetas.
- **Lo nuevo de Forever** [WP-COOK; WT-COOK; WP-FAV; WP-CAMP; OFI-HF]:
  - **La hoguera es un objeto**: la **Hoguera básica** se aprende con Cocina 1 y se fabrica con 1 Madera simple (Sílex y yesca solo para fabricarla); hogueras de oficial (Cocina 90) y de experto (200/220) con planos de jefes.
  - **La comida cocinada da bonus de experiencia** (+5 % por muertes según [PS]/Warcraft Tavern, en [E60 C29]); muchas recetas cambiaron a una sola estadística principal; el Siluro mostacherizo ahora da bonus de pesca [WT-COOK].
  - **6 recetas de Favor: todas «smoothies» de Espíritu** (Venomous, Slimy, «Mrrggl Smrrthle», Calcified, Spicy, Wicked) [WP-FAV].
  - **Receta nueva «Savory Whimsyfin Delight»: te transforma en múrloc o en ogro** [WT-COOK]; el pez nuevo **Whimsyfin** aparece en [WHF-MAP] solo en Montañas Crestagrana (27 bancos, ~67, 70).
  - **Objetos de campamento:** la hoguera es el 1.º; **Festín de Cocinitas** (140; comida de aguante para todo el campamento; plano de **Cocinitas** en Las Minas de la Muerte) → **Horno de hierro** (300; recetas más avanzadas; plano del Intendente Zigris, Cumbre de Roca Negra inferior) [WP-CAMP].
  - Hotfixes: Especias suaves al vendedor 1 c (5-nov); Nyalah Brightfire (Valanaar) vende más suministros (13-nov); Sopa de aleta de múrloc y platos de almeja corregidos (23-nov) [OFI-HF].
  - Objeto: **Cookie's Stirring Rod** (Cocinitas, Las Minas de la Muerte): +25 % de velocidad al cocinar [WT-COOK].
- **Lugar/mapa:** Dirge Hojágil, Tanaris 52.6, 28.0 · Gikkix, Tanaris 66.6, 22.0 · Wulan, Desolace 26.2, 69.8 · Shandrina, Vallefresno 49.4, 67.0 · Whimsyfin, Crestagrana 67.1, 69.9 (mediana de 27 bancos) · Ortak Lomgok (cocinero y posadero de la Horda en Flora Antigua, Hyjal 13.0, 52.8) [WHF-MAP].
- **En pantalla:** **Hoguera básica / Basic Campfire Kit (279981)** · Hoguera de oficial (279961) · Hoguera de experto (279974) · Madera simple (4470) · Libro de cocina para expertos (16072) · Huevo gigante (12207) · Carne de almeja sabrosa (7974) · Queso curado de Alterac (8932) · Receta: sopa de pargo nocturno (13945) · Plano: Festín de Cocinitas (273102) · Plano: horno de hierro (273115). YouTube: «WoW Forever cooking 1-300» · «WoW Forever Savory Whimsyfin Delight» · «WoW Forever campfire kit».
- **Curioso:** en Forever la Cocina no empieza con una receta: empieza con **una hoguera que llevas en la mochila**. Y hay un plato nuevo que te convierte en múrloc… o en ogro.
- **Fuente:** [WP-COOK] · [WT-COOK] · [WP-FAV] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [WHF-TT]
- **Confianza:** OFICIAL (hotfixes) · DATOS (Whimsyfin, objetos) · GUÍAS (ruta; efecto múrloc/ogro sin id de receta).

### Parada 11 · PESCA (secundaria; no ocupa hueco)
- **Explicación por tramo** [WP-FISH; ORO #4, #14, #15]:
  - **1-75:** Caña de pescar + **Adorno lustroso** en cualquier zona inicial; todos los entrenadores de zona inicial están junto al agua (Lago Toro de Piedra en Mulgore, Lago de Cristal en Elwynn 52.4, 62.4, Lago Aguasclaras en Tirisfal, Lago Glacial en Dun Morogh, Poblado Sen'jin, Rut'theran).
  - **75-150 (Oficial, nivel 10):** en las capitales o en Los Baldíos, Costa Oscura, Forjaz, Loch Modan, Argénteos, Páramos (Reptadores nocturnos si se escapan).
  - **150-225 (Experto = libro «Pesca para expertos: La lubina y tú» del Viejo Heming, Bahía del Botín 27.4, 77.0; nivel 20, Pesca 125):** **Adornos brillantes** y a pescar en **Marjal Revolcafango** (allí empieza el Artesano).
  - **225-300 (Artesano = «Nat Pagle, Angler Extreme», nivel 35, Pesca 225; Nat Pagle en Cala Furiamarea, Marjal 58.4, 60.0):** 4 peces en 4 zonas: Latipinia azul de La Costa Salvaje (costa oeste de Tuercespina), Artillero Sar'theris (costa de Desolace), Mahi mahi Juncobruma (costa este del Pantano de las Penas) y Ahi de Feralas (Río Verdantis 63.2, 52.2, con Adornos brillantes). Luego Frondavil, Feralas, Tierras del Interior, Tanaris, Un'Goro o Peste del Oeste.
- **Alianza vs Horda:** neutral (Viejo Heming y Nat Pagle atienden a los dos); en Desolace la Alianza puede pescar junto a la torre de la costa norte [WP-FISH].
- **Lo nuevo de Forever** [WT-FISH; WP-CAMP; OFI-HF; WIKI-FISH en ORO]:
  - **Objetos de campamento:** **Cuenco de pescado** (20; **+8 % a todas las estadísticas**, como Bendición de reyes, que da 10 %) → **Expositor de pesca** (140; peces poco comunes 1 h y **señuelos para todos** — hotfix 16-nov —; plano de Gelihast, Cavernas de Brazanegra) → **Cabaña de pesca** (300; peces raros y señuelos; plano de Jammal'an el Profeta, Templo Sumergido) [WP-CAMP; OFI-HF].
  - **Peces poco comunes y raros nuevos** con esos buffs; **Chef's Knife** (273636) para preparar peces únicos; menú nuevo «Bait and Tackle» [WT-FISH].
  - **Concurso de Tuercespina:** desde el **13-nov** gana **mucha más gente por conjunto de reglas** [OFI-HF]; premio Caña de pescar de arcanita (+35) y Extravagant Extravaganza Coin; **Surfer Shoes** que caminan sobre el agua [WT-FISH; ORO].
  - Cofres en mar abierto sin habilidad, bancos y restos flotantes con baúles [ORO #15, #4]; Caña de pescar de hierro grande en las trampas de Desolace [ORO #14].
  - Legado **Luremaster** [WT-LEG].
- **Lugar/mapa:** Viejo Heming 27.4, 77.0 · Nat Pagle 58.4, 60.0 · Río Verdantis 63.2, 52.2 · Aldea Cazasombras 25.3, 70.4 · Krix (Claros del Río 79.2, 54.8) · bancos de **Almeja bocazas** y **Langosta garraoscura**: **Azshara** (226 y 132 bancos; 58.3, 56.3 / 61.4, 57.4) [WHF-MAP].
- **En pantalla:** Caña de pescar (6256) · Adorno lustroso / Shiny Bauble (6529) · **Adornos brillantes / Bright Baubles (6532)** · Pesca para expertos: La lubina y tú (16083) · Latipinia azul de La Costa Salvaje (16969) · Artillero Sar'theris (16968) · Mahi mahi Juncobruma (16970) · Ahi de Feralas (16967) · Cuenco de pescado (receta 1229745) · Plano: expositor de pesca (273141) · Plano: cabaña de pesca (273119). YouTube: «WoW Forever fishing 1-300» · «WoW Forever Fish Bowl camp buff» · «WoW Forever Nat Pagle artisan fishing» · «WoW Forever fishing tournament Surfer Shoes».
- **Curioso:** el objeto de campamento de la Pesca es una **pecera** que da +8 % a todas las estadísticas: casi una Bendición de reyes… hecha con un pececito y un vial vacío.
- **Fuente:** [WP-FISH] · [WT-FISH] · [WP-CAMP] · [OFI-HF] · [WHF-MAP] · [ORO #4 #14 #15]
- **Confianza:** OFICIAL (concurso, señuelos) · DATOS · GUÍAS (ruta; misión de Nat Pagle = la de Classic, confirmada por la guía de Forever).

### Parada 12 · PRIMEROS AUXILIOS (secundaria; ahora hace POCIONES) [3060 #13]
- **Explicación por tramo** [WP-FA]:
  - **1-75:** dos caminos: vendas (50 Venda de lino + 47 Venda de lino gruesa) o **86 Poción de sanación menor** (Flor de paz + Especias suaves + Vial vacío).
  - **75-150 (Oficial, mismo entrenador):** vendas de lana, o **Cataplasma simple** (receta nueva: Icor de araña + Especias suaves + Botella de Dalaran Noir) de 90 a 125 y **31 Poción de sanación** (Hierba cardenal + Especias picantes + Vial emplomado) de 125 a 150.
  - **150-225 (Experto = libro «Primeros auxilios para expertos: Entre vendas», 1 o; Deneb Camino en Arathi 27.0, 58.8 — Alianza — o Balai Lok'Wein en Marjal 36.4, 30.4 — Horda; sin nivel, Primeros auxilios 125):** 44 Venda de seda, 44 de seda gruesa, 19 de tejido mágico.
  - **225-300 (Artesano = «Atenciones médicas» / Triage, Primeros auxilios 225 y nivel 35):** **Doctor Gregory Victor** en **Sentencia**, Arathi 73.4, 36.8 (Horda) o **Doctor Gustaf VanHowzen** en Theramore, Marjal 67.6, 48.8 (Alianza): salvar 15 heridos, críticos primero, y **entregarla en cuanto llegas a 15** (el autor la falló por esperar). Luego vendas de tejido mágico, de tejido mágico grueso, de paño rúnico; **alternativa nueva: de 275 a 300, 30 Pociones de sanación sublimes** (Sansam dorado + Especias calmantes + Vial de cristal) con el **Manual: Poción de sanación sublime** (255729), que vende **Pexmit en Monte Hyjal por 8 o** o da a la Horda la misión «A Rest Without Pain» de Ortak Lomgok (Flora Antigua). Cierra 290-300 con Venda de paño rúnico gruesa.
  - Materiales: 1-225 ≈ 144 lino, 142 lana, 132 seda, 19 tejido mágico; 225-300 ≈ 86 tejido mágico + 68 paño rúnico.
- **Alianza vs Horda:** libros y doctores distintos (Arathi/Marjal), ver arriba. El autor de [WP-FA] avisa que Victor «a veces no ofrece la misión si otro la está haciendo».
- **Lo nuevo de Forever** [WP-FA; WT-FA; WT-ALCH; WP-CAMP]:
  - **Las pociones de sanación pasaron de Alquimia a Primeros auxilios**: Poción de sanación menor, inferior, normal y **sublime** — «everyone can craft them» [WT-ALCH; WT-FA; WP-FA]. Recetario en 3 pestañas: Vendas, Pociones de sanación, Curativos.
  - **Curativos nuevos:** Cataplasma simple, **Torniquete de lana** (sangrados) y recetas contra enfermedad (no usables en combate) [WT-FA].
  - **Objetos de campamento:** **Equipo de primeros auxilios** (20; Aguante, no se acumula con Palabra de poder: entereza) → **Estudio de toxinas** (140; pociones y contraveneno; plano del Comandante Vallefont, Castillo de Colmillo Oscuro) → **Laboratorio de médico de la peste** (300; pociones y cataplasmas; plano del Doctor Theolen Krastinov, Scholomance) [WP-CAMP].
  - Legado «Field Medicine» (acorta Recently Bandaged fuera de mazmorras) [WT-FA].
- **Lugar/mapa:** Sentencia (Arathi 73.9, 35.8) y Doctor Gregory Victor 73.4, 36.8 · Theramore (Marjal 65.0, 47.1) y VanHowzen 67.6, 48.8 · Deneb Camino 27.0, 58.8 · Balai Lok'Wein 36.4, 30.4 · **Pexmit, Monte Hyjal 48.2, 33.6** · Ortak Lomgok, Hyjal 13.0, 52.8 [WHF-MAP].
- **En pantalla:** Venda de lino (1251) · Poción de sanación menor (receta 1244431) · Poción de sanación (receta 1244433) · **Poción de sanación sublime / Major Healing Potion (receta 1244436; objeto 13446)** · **Manual: Poción de sanación sublime (255729)** · **Cataplasma simple (receta 1259342)** · Primeros auxilios para expertos: Entre vendas (16084) · Venda de paño rúnico gruesa (14530) · Plano: laboratorio de médico de la peste (273118). YouTube: «WoW Forever first aid healing potions» · «WoW Forever Triage quest Hammerfall» · «WoW Forever Major Healing Potion manual Pexmit».
- **Curioso:** en Forever **cualquier personaje** puede fabricar Pociones de sanación sublimes sin gastar un hueco de profesión: la receta ya no es del alquimista, sino del que sabe poner vendas.
- **Fuente:** [WP-FA] · [WT-FA] · [WT-ALCH] · [WP-CAMP] · [WHF-MAP] · [WHF-TT] · [3060 #13]
- **Confianza:** GUÍAS (dos guías de Forever coinciden en el traslado de pociones) · DATOS (recetas 1244431/1244433/1244436 existen en el cliente con esos nombres). El autor de [WP-FA] no probó todo Triage en el cliente en vivo ([3060]).

---

## PROPUESTA DE ORDEN (cómo contar la historia)
Lógica: **recolección primero** (alimenta todo), luego la fabricación por **cadena de materiales** (lo que pica el minero va al herrero y al ingeniero; lo que recoge el herbolario va al alquimista; lo que desuella el desollador va al peletero; la tela va al sastre y lo que cose se desencanta), y al final **las 3 secundarias que todo el mundo puede llevar**, cerrando con el dato más fuerte.

1. **Minería** — abre con la mena nueva (torio pesado, que exige campamento) y el contexto de entrenadores júnior.
2. **Herrería** — gasta el mineral (508-1220 barras de torio en el último tramo).
3. **Ingeniería** — el otro destino del mineral; gnomo sin +15, bombas SAF-T, parapente.
4. **Herboristería** — semillas e invernadero; hierbas de Hyjal.
5. **Alquimia** — pierde las pociones de sanación (deja el gancho para el final), gana el laboratorio portátil y los tintes.
6. **Desuello** — una vez por criatura; materiales prístinos.
7. **Peletería** — la Tienda de campamento (descanso) y los Zapatos de gamuza azul.
8. **Sastrería** — bolsas de componentes (enlaza con los tintes de Alquimia) y la trampa del Telar.
9. **Encantamiento** — desencanta lo que cose el sastre; collares por Favor; Annora.
10. **Cocina** — la hoguera en la mochila: aquí se explica el campamento entero (28,7 millones de objetos de campamento en la semana 1).
11. **Pesca** — la pecera del +8 %; concurso con más ganadores.
12. **Primeros auxilios** — **cierre**: «la poción que ya no es del alquimista»: cualquiera fabrica Pociones de sanación sublimes; el manual lo vende un PNJ difícil de encontrar en Monte Hyjal.

Bloque de contexto (costes, límite de 2, capitales, Legado, Favor y combinaciones) entre el gancho y la parada 1, o partido: costes y límite al inicio; Favor después de Herrería (primera vez que aparecen recetas de Favor de equipo); Legado después de Encantamiento (cierre de las 6 que dan puntos).

## 3 IDEAS DE GANCHO
1. «En WoW Forever, el alquimista ya no hace pociones de sanación. Ahora las hace… cualquiera. Y no es el único cambio: hay una mena que no se puede fundir en ninguna forja de Azeroth.»
2. «12 profesiones, 4 tramos cada una, Alianza y Horda: esta es la ruta del 1 al 300 de WoW Forever, con dónde entrenar, dónde recoger y lo que la guía de siempre no sabe.»
3. «En la primera semana de WoW Forever los jugadores pusieron más de 28 millones de objetos de campamento. Si subes tus profesiones sin campamento, te faltan las estaciones para fabricar media lista de recetas.»

## Comprobar antes de grabar
- Nombres es-MX en el cliente: «Cajón arrebatado», «Libranza del artesano», «Señor Grafo», «Anodín» (Grungle), «Tres Caminos», «Hojapesadilla», «Salvia demoníaca», «Poción de sanación sublime», «Kayleena Encantaflores» (Wowhead mx escribe «Kayleena»; el inglés es «Kaylaena»).
- Costes de entrenamiento en el cliente (las tablas son de la guía).
- Si el Aprendiz de fabricación pide nivel 5 o ninguno.
- Shurome (Frondavil) enseñando Artesano sin 200: puede corregirse.
- Que el Telar y la Máquina de coser sigan exigiendo 300 para colocarlos.
- Hotfixes posteriores al 23-nov.
- Coordenadas: pintarlas sobre el mapa de zona de Forever (rejilla del canal) antes del render; las de Ventormenta, sobre el **mapa de ciudad de Forever**.

## Descartados
- **Joyería, Inscripción, Arqueología:** no existen en Forever (ninguna fuente las lista).
- **Forzar cerraduras** (wow-professions tiene guía): es una habilidad del pícaro, no profesión.
- **Precios de subasta actuales** de cada material: cambian cada día y no hay fuente fechada por profesión; para cifras sueltas usar [ORO] con su fecha.
- **Tier de artesano de banda** como «meta» de Herrería/Peletería/Sastrería: roza «prometer botín de banda» (regla del patrocinador); solo mencionarlo como requisito de 300 [E60 C13], sin listar piezas.
- **Truco de cambiar de capa para vetas** (Teddys en [ORO #2]): él mismo lo llama exploit.
- **«Mining is good for raw gold / skip leveling»** y frases tipo «leveling Skinning is boring» de las guías: chocan con el brief.
- **Wowhead «Tried & Tested» / «Easiest» guides** de Forever: la página carga por JavaScript y no se pudo leer (solo autor «Nodge», actualizado 21-nov, parche 1.60.1).
- **Icy Veins** (403), **Method, RankedBoost, Gfinity, MeinMMO** de combinaciones: titulan «best»; se usó solo la lógica de pares material→fabricación, que coincide con [WP] y [WT].
- **Coordenadas de Classic de Ventormenta** (43, 73): no valen para el mapa de Forever.
- **Hierro espectral** como ruta de Minería: es mena de misión de Shen'dralas, no sube la profesión (sin dato de habilidad).
- **«Lotus Claw»** (encantamiento que deja sacar Loto de la muerte): sin id ni receta encontrada.
- **Recompensa de los Cajones de Artesano:** «Not known yet» en [WP-FAV].
