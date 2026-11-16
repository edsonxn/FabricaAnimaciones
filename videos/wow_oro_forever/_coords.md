# Coordenadas, mapas e íconos — wow_oro_forever (15-nov-2026)

Fuente principal: base de datos de **Wowhead Forever** (`nether.wowhead.com/forever/tooltip/<npc|object>/<id>` → campo `map`,
y `g_mapperData` de la página `wowhead.com/forever/...` cuando el PNJ está en varias zonas). Coordenadas del juego 0-100 de la zona.
Mapas: `wow.zamimg.com/images/wow/classicplus/maps/eses/original/<zona>.jpg` = mapas de **Forever** en Wowhead
(«classicplus»); para todas las zonas de abajo son **idénticos píxel a píxel** a los de Classic que ya teníamos (diferencia media 0,0),
salvo Arathi (misma geografía, mejor calidad: `mapas/arathi.jpg` es ya el de Forever). 1 % de la imagen = 1 de coordenada.
Comprobación visual: `python _coords_check.py` → `previews/_coords_check_1.jpg` y `_2.jpg` (cada punto dibujado en su mapa; revisados:
ninguno en el mar salvo los que DEBEN estar bajo el agua, trampas y almejas).

## Tabla
| Lugar | Zona (mapa) | x, y | Fuente | Confianza |
|---|---|---|---|---|
| Randal Hunter (instructor de equitación) | Bosque de Elwynn (`elwynn`) | **84.2, 65.0** | https://www.wowhead.com/forever/npc=4732 | ALTA (wiki: 84.3, 65.0) |
| Kildar (instructor de lobos) | Orgrimmar (`orgrimmar`) | **69.2, 13.2** (rango 69.0-69.6, 12.4-13.8) | https://www.wowhead.com/forever/npc=4752 | ALTA. ⚠ Está en el **Valle del Honor**, no en el «Valle de la Sabiduría» (guion.py l. 87) |
| Strahad Farsan | Los Baldíos, Trinquete (`baldios`) | **62.6, 35.5** | https://www.wowhead.com/forever/npc=6251 | ALTA |
| Chol'aruk (élite, Colina Espinosa) | Los Baldíos (`baldios`) | **57.5, 27.2** | https://www.wowhead.com/forever/npc=267307 | ALTA (wiki 57.6, 27.4; el [58, 25.5] es la boca de la cueva; Wowhead trae un 3.er punto suelto en 25.8, 23.8 = dato erróneo, ignorado) |
| Gelvas Grimegate — Feria en Villadorada | Bosque de Elwynn (`elwynn`) | **41.5, 68.9** | https://www.wowhead.com/forever/npc=14828 | ALTA |
| Gelvas Grimegate — Feria en Mulgore | Mulgore (`mulgore`) | **37.2, 37.8** | https://www.wowhead.com/forever/npc=14828 (g_mapperData zona 215) | ALTA |
| Trampas de marisco (Shellfish Trap, obj. 176582) | Desolace (`desolace`) | **20.0, 80.7** (24 trampas en 18-24.3, 75-86.5; otras 3 en 20.0, 71.3) | https://www.wowhead.com/forever/object=176582 | ALTA (bajo el agua, al oeste de Aldea Cazasombras) |
| Supervendedor 680 (caravana de Gizelton) | Desolace (`desolace`) | **40.5, 79.2** (parada; la caravana se mueve) | https://www.wowhead.com/forever/npc=12246 | ALTA (wiki 40, 79) |
| Exiliados ardientes (Burning Exile) | Tierras Altas de Arathi (`arathi`) | **25.2, 30.6** (noroeste, Círculo de Vínculo Oeste) | https://www.wowhead.com/forever/npc=2760 | ALTA |
| Exiliados del trueno (Thundering Exile) | Arathi (`arathi`) | **51.4, 50.6** (centro, Círculo de Vínculo Exterior) | https://www.wowhead.com/forever/npc=2762 | ALTA |
| Exiliados blasonados (Cresting Exile) | Arathi (`arathi`) | **66.6, 29.8** (noreste, Círculo de Vínculo Este) | https://www.wowhead.com/forever/npc=2761 | ALTA |
| Almejas gigantes (Giant Clam, obj. 2744) — Arrecife | Vega de Tuercespina (`tuercespina`) | **25.9, 26.6** (44 almejas en 23.6-28, 22.4-30.8) | https://www.wowhead.com/forever/object=2744 | ALTA. Al OESTE de Grom'gol (32.5, 29). ⚠ En el mapa es-ES el arrecife se llama **«El Arrecife Mortal»**, no «Arrecife Vil» |
| Dirge Hojágil (Dirge Quikcleave) | Tanaris, Gadgetzan (`tanaris_eses`) | **52.6, 28.0** | https://www.wowhead.com/forever/npc=8125 | ALTA |
| Rocs de Tanaris («Roc», npc 5428) | Tanaris (`tanaris_eses`) | **50.1, 30.6** (28 de 36 en 47.5-57, 25-37: alrededor de Gadgetzan); 2.º grupo 58.0, 25.8 | https://www.wowhead.com/forever/npc=5428 | ALTA |
| Rocs de fuego (Fire Roc, npc 5429) | Tanaris (`tanaris_eses`) | **46.6, 41.4** (al sur de Gadgetzan) | https://www.wowhead.com/forever/npc=5429 | ALTA (también Searing Roc 39.4, 64.8) |
| Grifos Frayfeather (son **hipogrifos**: Skystormer/Stagwing/Hippogryph) | Feralas (`feralas_eses`) | **55.3, 68.0** (53.4-58.6, 60-75; Altas Tierras Salvajes, sur) | https://www.wowhead.com/forever/npc=5305 · npc=5304 · npc=5300 | ALTA. ⚠ El guion dice «grifos»; en el juego son hipogrifos (es-ES: «Hipogrifo Plumavieja») |
| Planeadores de oleaje (Surf Glider) — costa sur | Tanaris (`tanaris_eses`) | **54.1, 93.1** (44 de 80, 48.6-59.2, 88-97: playa del sur) | https://www.wowhead.com/forever/npc=5431 | ALTA (coincide con «costa sur» del guion) |
| Planeadores de oleaje — costa este (Costa Rompesur) | Tanaris (`tanaris_eses`) | **68.5, 57.2** (18 de 80); 3.er grupo 60.2, 85.0 | https://www.wowhead.com/forever/npc=5431 | ALTA |
| Marcy Baker (Three Corners) | Montañas Crestagrana (`crestagrana`) | **9.5, 71.0** | https://www.wowhead.com/forever/npc=256390 | ALTA (wiki 9.7, 70.9; el «[10, 73]» era el campamento en general) |
| **Dokimi** (al oeste del Cruce) | Los Baldíos (`baldios`) | **50.0, 29.2** | https://www.wowhead.com/forever/npc=256386 | ALTA — **contradicción resuelta:** la página de la wiki (npc 214096, [39, 53] / el «[42, 34]») es la Dokimi de *Season of Discovery* en Cima del Trueno; la de Forever es otro PNJ (id 256386) y está pegada al Cruce, con Gishah (49.4, 29.4), Jornah y los kodos de carga |
| Viejo Heming | Vega de Tuercespina, Bahía del Botín (`tuercespina`) | **27.4, 77.0** | https://www.wowhead.com/forever/npc=2626 | ALTA |
| Nat Pagle | Marjal Revolcafango (`marjal_eses`) | **58.5, 60.0** (su islote, al sur de Theramore) | https://www.wowhead.com/forever/npc=12919 | ALTA |
| Sátiros Jadefire — Claro Jadefire (sur) | Frondavil (`frondavil_eses`) | **41.7, 85.0** (38-44, 80-89) | https://www.wowhead.com/forever/npc=7105 · npc=7109 | ALTA |
| Sátiros Jadefire — Bastión de las Sombras | Frondavil (`frondavil_eses`) | **35.8, 66.6** (Felsworn/Shadowstalker/Rogue) | https://www.wowhead.com/forever/npc=7109 · npc=7110 | ALTA |
| Sátiros Jadefire — Paso Jadefire (norte) | Frondavil (`frondavil_eses`) | **42.4, 17.4** (Betrayer/Trickster/Hellcaller) | https://www.wowhead.com/forever/npc=7108 | ALTA |
| Sátiros Legashi | Azshara (`azshara`) | **56.4, 20.6** (grupo principal 50.4-62.6, 17.4-26.8); 2.º grupo **66.0, 17.5** | https://www.wowhead.com/forever/npc=6200 · npc=6201 | ALTA (wiki daba 48.5, 17.5 = borde oeste del campamento) |
| Vetas de torio ricas (obj. 175404) | Las Estepas Ardientes (`estepas`) | 33 puntos en Forever; para el mapa: **47.3, 33.4 · 30.3, 58.6 · 54.4, 60.1 · 61.0, 38.5 · 72.4, 29.8** | https://www.wowhead.com/forever/object=175404 (g_mapperData zona 46) | ALTA (aparecen al azar entre esos puntos) |
| Mister Graphed (mercado negro) — extra | Riverglades (zona 16591) | 78.2, 51.8 | https://www.wowhead.com/forever/npc=263384 | ALTA el dato; **SIN mapa** de Riverglades en zamimg (404) |
| Monte Hyjal | Monte Hyjal (`hyjal`, zona 616 de Forever) | zona entera; sin punto (el guion no nombra un lugar). Torio rico allí: 52.7, 72.7 / 56.9, 72.2 | zona: https://www.wowhead.com/forever/object=175404 (zona 616) · https://warcraft.wiki.gg/wiki/Mount_Hyjal_(Forever) | ALTA que es zona de Forever (nivel 60, «Forever only») |

## Mapas en `mapas/`
Copiados de `wow_forever_experiencia/mapas/`: elwynn, orgrimmar, baldios, mulgore, desolace, tuercespina, tanaris_eses, feralas_eses,
crestagrana, marjal_eses, frondavil_eses, azshara, estepas, kalimdor, kalimdor_zonas.
Nuevos: `arathi.jpg` = zamimg classicplus/eses/45 (Forever); `hyjal.jpg` = mapa del juego de Forever (warcraft.wiki.gg
`File:WorldMap-Hyjal-forever.jpg`, 1002×668, rótulos en INGLÉS: Felwood, Winterspring, Dae'gun, Shrine of Aviana…; el de zamimg
classicplus/616 es un borrador casi sin rasgos y se descartó). Falta: Riverglades (no existe en zamimg).

## Nombres es-ES del juego (Wowhead, locale 6) que NO coinciden con el guion/investigación (para rótulos de MG)
- Bolsa de tejido mágico roja → **Bolsa de paño mágico roja** · Venda de seda gruesa → **Venda de seda pesada**
- Receta: filete de lobo magro → **Receta: chuleta de lobo magro** · Cardopresto → **Cardoveloz** · Fuego elemental → **Elemental de Fuego**
- Tela vil → **Tela de inferi** · Mena de torio → **Torio** · Veta de torio rica → **Filón de torio enriquecido**
- Planeador de oleaje → **Planoleador** · sátiros Jadefire → **Sátiro Fuego de Jade** · Trampa de marisco → **Concha trampa**
- Exiliado del trueno → **Exiliado tronador** · Randal Hunter → Randal Predatio · Gelvas Grimegate → Gelvas Roñas (la voz usa los ingleses)

## Íconos de Wowhead (nombre de ícono para los MG; id comprobado por nombre en el tooltip de Forever)
| Objeto (voz) | Nombre en el juego (en / es-ES) | id | ícono | pegatina |
|---|---|---|---|---|
| Bolsa de tejido mágico roja | Red Mageweave Bag / Bolsa de paño mágico roja | 10051 | `inv_misc_bag_10_red` | o_bolsa_roja |
| Caja de la Feria (Darkmoon Storage Box) | Darkmoon Storage Box / Caja para guardar de la Luna Negra | 19291 | `inv_box_04` | o_caja_feria |
| Paño de seda | Silk Cloth / Paño de seda | 4306 | `inv_fabric_silk_01` | o_seda |
| Paño de tejido mágico | Mageweave Cloth / Tela de paño mágico | 4338 | `inv_fabric_mageweave_01` | o_tejido_magico |
| Venda de seda gruesa | Heavy Silk Bandage / Venda de seda pesada | 6451 | `inv_misc_bandage_02` | o_venda |
| Página de Las verdes colinas | Green Hills of Stranglethorn - Page 1 / Las verdes colinas de Tuercespina: Página 1 | 2725 | `inv_misc_note_06` | o_pagina |
| Caña de pescar de hierro grande | Big Iron Fishing Pole / Caña de pescar de hierro grande | 6367 | `inv_fishingpole_01` | o_cana_hierro |
| Receta: filete de lobo magro | Recipe: Lean Wolf Steak / Receta: chuleta de lobo magro | 12227 | `inv_scroll_03` | o_receta_lobo |
| Filete de lobo magro | Lean Wolf Steak / Chuleta de lobo magro | 12209 | `inv_misc_food_47` | o_filete |
| Talismán ardiente | Burning Charm / Talismán ardiente | 4479 | `inv_jewelry_talisman_01` | o_tal_ardiente |
| Talismán del trueno | Thundering Charm / Talismán del trueno | 4480 | `inv_jewelry_talisman_02` | o_tal_trueno |
| Talismán blasonado | Cresting Charm / Talismán blasonado | 4481 | `inv_jewelry_talisman_05` | o_tal_blasonado |
| Perla azul | Blue Pearl / Perla azul | 4611 | `inv_ore_arcanite_02` | o_perla_azul |
| Huevo gigante | Giant Egg / Huevo gigante | 12207 | `inv_egg_03` | o_huevo |
| Pico afilado | Razor-sharp Beak / Pico afilado | 5829 | `inv_misc_birdbeck_01` | o_pico |
| Hueso de ala | Hollow Wing Bone / Hueso hueco de ala | 11418 | `inv_misc_bone_01` | o_hueso |
| Perla de oro | Golden Pearl / Perla de oro | 13926 | `inv_misc_gem_pearl_04` | o_perla_oro |
| Carne de tortuga | Turtle Meat / Carne de tortuga | 3712 | `inv_misc_food_70` | o_tortuga |
| Cardopresto | Swiftthistle / Cardoveloz | 2452 | `inv_misc_herb_04` | o_cardopresto |
| Fuego elemental | Elemental Fire / Elemental de Fuego | 7068 | `spell_fire_fire` | o_fuego |
| Adornos brillantes | Bright Baubles / Adornos brillante | 6532 | `inv_misc_gem_variety_02` | o_adornos |
| Paño rúnico | Runecloth / Paño rúnico | 14047 | `inv_fabric_purplefire_01` | o_runico |
| Tela vil | Felcloth / Tela de inferi | 14256 | `inv_fabric_felrag` | o_vil |
| Cristal Arcano | Arcane Crystal / Cristal Arcano | 12363 | `inv_misc_gem_topaz_01` | o_cristal |
| Mena de torio | Thorium Ore / Torio | 10620 | `inv_ore_thorium_02` | o_torio |
| Loto negro | Black Lotus / Loto negro | 13468 | `inv_misc_herb_blacklotus` | o_loto |
| Cuero ligero | Light Leather / Cuero ligero | 2318 | `inv_misc_leatherscrap_03` | o_cuero_ligero |
| Cuero medio | Medium Leather / Cuero medio | 2319 | `inv_misc_leatherscrap_05` | o_cuero_medio |

## Pegatinas de PNJ, criaturas y lugares (`pegatinas/`, registro en `pegatinas/_fuentes.txt`)
strahad, randal, kildar, cholaruk, gelvas (modelo viejo), supervendedor, dirge, heming, nat_pagle, frayfeather, planeador, almeja,
satiro_jadefire, satiro_legashi, exiliado_ardiente, exiliado_blasonado, exiliado_trueno_wiki, onyxia_guarida, hyjal = warcraft.wiki.gg.
roc, onyxia, exiliado_trueno, mister_graphed = modelo 3D de Wowhead **Forever** (webthumb classicplus, fondo transparente, 300 px).
roc_fuego, veta_torio = capturas de usuarios en Wowhead Classic (páginas del Fire Roc y del objeto 175404); `pantallas/veta_torio_mina.jpg`
= captura del mismo objeto con un minero. auctionator_logo/_vender/_compras/_tooltip = página oficial del add-on en CurseForge
(capturas «classic» del autor). Descartados: «Roc» de la wiki (= Irewing, otro roc), Onyxia y Nat Pagle de Hearthstone,
la foto del edificio de Trinquete que la wiki usa para Strahad.
