# Coordenadas y mapas — wow_oro_30_50 (25-nov-2026; modelo: wow_ruta_profesiones/_coords.md)

**Fuentes de las coordenadas** (nada de memoria): INV = `videos/_investigacion_wow_oro_30_50.md` · **WN** = puntos de aparición del tooltip de PNJ
de **Wowhead Forever** (`nether.wowhead.com/forever/tooltip/npc/<id>`, campo `map`; centro = media de los puntos de la casilla de 5 % con más
apariciones; recalculado el 25-nov y sale igual que la investigación) · **WL** = rótulo de subzona/pueblo del mapa mundial de Wowhead Forever
(`nether.wowhead.com/forever/data/world-map`, campo `places`; nombres es-MX de `/forever/mx/data/world-map`) pasado a % de la zona con el `rect`
de la zona · **WP** = pin de PNJ del mismo archivo (`pois`: vendedores y maestros de vuelo; `side` 1 = Alianza, 2 = Horda, 0 = los dos) ·
**WM** = nodos de recolección/pesca del mismo archivo (`nodes`: vetas, bancos de peces).

**Mapas** (`mapas/`, origen en `mapas/_fuentes.txt`, se rehacen con `python _mapas.py [nombre…]`). **SIEMPRE EL ORIGINAL A TODO COLOR**
(cambio del usuario al kit, 25-nov): `E.mapa_e` rota original → oro → madera → original v1 → v2, nunca sepia ni azul.
- Zona (1 % de la imagen = 1 de coordenada): `wow.zamimg.com/images/wow/classicplus/maps/<eses|enus>/original/<id>.jpg` (Forever en Wowhead):
  desolace 405 · marjal 15 · tuercespina 33 · mil_agujas 400 · **riverglades 16591 (solo enus: rótulos en inglés)** · inhospitas 3 · pantano 8 ·
  tanaris 440 · feralas 357 · alterac 36 · **devastadas 4** (Las Tierras Devastadas; mirado: es la zona, no un continente).
- `mundo` = teselas del mapa mundial de Wowhead Forever (sin rótulos, zoom 4, 3200x1799, 16:9): Kalimdor + Reinos del Este de Feralas a Claros
  del Río y de Alterac a Bahía del Botín. Coordenada de zona → lienzo → % del recorte con `M()` de `_coords_check.py` (rect en `mapas/_rects.json`).
- Los x, y de la tabla son **% de la imagen** = lo que va a `P(x, y, rótulo, sub, foto)` de `mapa(...)` en efectos.py.
- **5.º campo (ícono) OBLIGATORIO y lleno en los 127 puntos**: `o_*` = pegatina del objeto que se farmea ahí (`pegatinas/`), slug de criatura/PNJ
  = su CARA (`Fc(slug)` → `caras/`), `ico:<ícono>` = ícono de Wowhead (vuelos: `ability_mount_gryphon_01` Alianza, `ability_mount_wyvern_01`
  Horda). Columna **Alt.** = otra imagen real para el mismo punto (la cara de la criatura o la foto del lugar) por si efectos prefiere esa.
  Regla aplicada: en puntos de farmeo el ícono es LO QUE SE FARMEA (paño, cola, molleja…) y la cara de la criatura va en Alt.; en PNJ, su cara.

**Comprobación visual:** `python _coords_check.py` → `previews/_coords_check_1..5.jpg` (18 vistas: 11 zonas + 7 sobre `mundo`, con el ícono pegado
a cada punto), MIRADAS a mano el 25-nov: todo punto en tierra y en su zona (los bancos de anguila, en el agua de la costa oeste, como deben).
`python _coords_check.py` también avisa si falta la imagen de algún 5.º campo (0 faltan). `python _coords_check.py md` imprime la tabla.

## Qué mapa para qué escena (propuesta; ≥ 1 por puesto)
| Escena | Mapas |
|---|---|
| intro | `devastadas` (el cráter del buitre) · `alterac` (la cueva de los 5 minerales y Rizz en su jaula) · `mundo:intro15` (los 15 puestos numerados) |
| reglas | — (sin geografía) |
| p15 Centauros | `desolace` (Poblado Magram, 3 grupos, hienas Zarpósea; venta: Campamento del Espíritu Errante H / Punta de Nijel A) |
| p14 Arañas | `marjal` (Cueva Niebla Negra, arañas dentro y fuera; Poblado Murohelecho H / Isla Theramore A) |
| p13 Gorilas | `tuercespina` (gorilas junto al Lago Nazferiti, ancianos al sur, Unbagwa y Mokk; Grom'Gol H / Asentamiento Rebelde A / Bahía del Botín) |
| p12 Tortugas | `mil_agujas` (tortugas y mordedores, Cráter de la Comadreja, Circuito del Espejismo) · `marjal` (cavapozos Fangorroca, la alternativa del 42) |
| p11 Cangrejos | `riverglades` (reptadores al sur del Puerto Polvomecha, Fimbo / Sabores de mar) · `tuercespina` (reptadores del sur, cerca de Bahía del Botín) |
| p10 Crías | `inhospitas` (crías en el este, Barranco Lethlor con élites en el centro, vetas de mitril) |
| p09 Múrlocs | `pantano` (playa del sureste, Puesto Juncobruma, oráculos hacia la Cueva Stagalbog, Rocal) |
| p08 Hienas | `tanaris` (Arenas Abisales: hienas y rocs de fuego; Gadgetzan) |
| p07 Feralas | `feralas` (tronadores y patriarcas en Los Dos Colosos; simios y osos del centro; Mojache H / Plumaluna A) |
| p06 Jaguares | `pantano` (jaguares, Rocal) · `riverglades` (plan B: cazadoras al sur de Rog'mar) |
| p05 Elementales | `inhospitas` (3 franjas: inferiores junto a Kargath, normales en la Explanada del Espejismo, superiores al suroeste) |
| p04 Coyotes | `riverglades` (coyotes al sur del Cortijo de Wheeler, Sootfur, Benjy) · `mundo:p04` (de Claros del Río a Tierras Inhóspitas) |
| p03 Pesca | `tuercespina` (ruta Grom'Gol → costa oeste → Bahía del Botín por los bancos de anguila escama pétrea) |
| p02 Alterac | `alterac` (fortaleza, Cuenca de la Matanza = cueva norte, 38 vetas, ogros del sur, Rizz, Lo'Grosh, élites) |
| p01 Buitres | `devastadas` (4 grupos de destripadores, Alto de los Rapiñadores, Serpiente Enroscada, Lynnore y Drazial, scorpok, hienas, Nethergarde) · `mundo:p01` (vuelos: Nethergarde A / Rocal H) |
| resumen | `mundo:r30` · `mundo:r35` · `mundo:r40` · `mundo:r45` (la ruta del oro por nivel, una vista por tramo) |
| cierre | `mundo:intro15` (otra vez, del 15 al 1) |

## Puntos (127)
| Mapa | Escena | x, y (% del mapa) | Rótulo | Subrótulo | Ícono (5.º campo) | Alt. | Frase del guion | Tipo | Fuente | Confianza |
|---|---|---|---|---|---|---|---|---|---|---|
| `desolace` | p15 | 70.8, 76.8 | Poblado Magram | 33-38 · reaparecen más rápido | `o_pano_seda` | `poblado_magram` | «Los centauros del Poblado Magram, en Desolace» | C | WL | ALTA |
| `desolace` | p15 | 67.6, 72.5 | Cazavientos y retadores | 33-34 | `o_pano_seda` | `cazavientos_magram` | «con retadores, cazavientos y corremanadas» | R | WN | ALTA (22 de 78 y 17 de 72 apariciones) |
| `desolace` | p15 | 72.5, 67.6 | Retadores y cazavientos | segundo grupo | `o_pano_seda` | `retador_magram` | «repartidos en varios grupos al sureste de la zona» | R | WN | ALTA (10 + 10) |
| `desolace` | p15 | 72.0, 76.7 | Corremanadas Magram | 34-35 | `o_tejido_magico` | `corremanadas_magram` | «hacia el treinta y cinco empieza a caer el tejido mágico» | R | WN | ALTA (10 de 51) |
| `desolace` | p15 | 67.8, 76.7 | Zarpósea Magram | hienas 37-38 | `zarposea_magram` | `zarposea_magram` | «Ojo con sus hienas, las Zarpósea» | X | WN | ALTA (solo 18 apariciones, mezcladas con los centauros) |
| `desolace` | p15 | 55.5, 55.9 | Campamento del Espíritu Errante | vende la Horda | `o_oro` | — | «cuando la bolsa se llena, sales a vender» | V | WL | ALTA (vendedor Muuran, side 2) |
| `desolace` | p15 | 65.1, 8.3 | Punta de Nijel | vende y vuela la Alianza | `o_oro` | — | «cuando la bolsa se llena, sales a vender» | V | WL | ALTA (5 vendedores + vuelo, side 1) |
| `marjal` | p14 | 33.3, 22.8 | Cueva Niebla Negra | 35-38 | `o_seda_sombras` | `cueva_niebla_negra` | «Las arañas de la Cueva Niebla Negra» | C | WL | ALTA |
| `marjal` | p14 | 35.4, 22.3 | Arañas y ermitañas | 35-37 | `o_seda_arana_espesa` | `arana_niebla_negra` | «arañas Niebla Negra y ermitañas Niebla Negra» | R | WN | ALTA (7 + 7; el grupo grande, 34.0, 21.8, está pegado al rótulo de la cueva) |
| `marjal` | p14 | 34.5, 25.4 | Arañas Niebla Negra | fuera de la cueva | `o_mandibula_arana` | `ermitana_niebla_negra` | «Están fuera y dentro de la cueva, al norte del marjal» | R | WN | ALTA (4 + 3) |
| `marjal` | p14 | 36.3, 31.4 | Poblado Murohelecho | vende la Horda | `o_oro` | `poblado_murohelecho` | «La Horda vende al lado, en el Poblado Murohelecho» | V | WL | ALTA (6 vendedores + vuelo, side 2) |
| `marjal` | p14 | 65.0, 47.1 | Isla Theramore | vende la Alianza | `o_oro` | `theramore` | «La Alianza, en la Isla Theramore» | V | WL | ALTA (13 vendedores + vuelo, side 1) |
| `marjal` | p12 | 58.4, 61.7 | Cavapozos Fangorroca | 42-43 | `o_almeja_boca_grande` | `cavapozos_fangorroca` | «los cavapozos Fangorroca del Marjal Revolcafango» | R | WN | ALTA (13 de 45) |
| `tuercespina` | p13 | 37.7, 17.1 | Gorilas Velo de Bruma | 32-33 · 14 apariciones | `o_colmillo_gorila` | `gorila_velo_bruma` | «Los jóvenes viven al oeste del Lago Nazferiti» | R | WN | ALTA (13 de 14) |
| `tuercespina` | p13 | 40.8, 16.0 | Lago Nazferiti |  | `o_pelo_gorila_burdo` | `lago_nazferiti` | «al oeste del Lago Nazferiti, en el norte de la selva» | C | WL | ALTA |
| `tuercespina` | p13 | 32.5, 66.8 | Gorilas ancianos | 40-41 · Valle del Velo de Bruma | `o_colmillo_gorila` | `gorila_velo_bruma_anciano` | «Los ancianos, en el Valle del Velo de Bruma, más al sur» | R | WN | ALTA (18 de 36; rótulo del valle 33.0, 66.2) |
| `tuercespina` | p13 | 35.2, 60.5 | Médico brujo Unbagwa | La fiebre de Tuercespina | `unbagwa` | — | «una misión, La fiebre de Tuercespina, pide colmillos» | P | WN | ALTA |
| `tuercespina` | p13 | 34.6, 62.2 | Mokk el Salvaje | 44 · sale en oleadas | `mokk` | — | «para invocar a Mokk el Salvaje en oleadas» | P | WN | ALTA (4 de 5 apariciones) |
| `tuercespina` | p13 p03 | 31.9, 28.4 | Campamento Grom'Gol | vende la Horda · buzón | `o_valija_mitril` | `gromgol` | «sales del Campamento Grom'Gol» | V | WL | ALTA (8 vendedores + vuelo, side 2) |
| `tuercespina` | p13 | 38.2, 3.5 | Asentamiento Rebelde | vende la Alianza | `o_oro` | — | (venta de la Alianza en el norte) | V | WL | MEDIA (1 vendedor, side 1) |
| `tuercespina` | p11 | 33.6, 76.3 | Reptadores de las arenas del sur | 40-41 · almejas | `o_almeja_boca_grande` | `reptador_arenas_sur` | «los reptadores del sur de Tuercespina, cerca de Bahía del Botín» | R | WN | MEDIA (solo 12 apariciones, en grupos de 2-3) |
| `tuercespina` | p03 | 27.1, 42.9 | Anguila escama pétrea | 5 bancos | `o_anguila_petrea` | — | «también de los bancos de anguila escama pétrea» | R | WM | ALTA |
| `tuercespina` | p03 | 23.3, 57.2 | Anguila escama pétrea | 5 bancos | `o_anguila_petrea` | — | «bajas por toda la costa oeste» | R | WM | ALTA |
| `tuercespina` | p03 | 27.4, 83.4 | Anguila escama pétrea | 8 bancos | `o_valija_mitril` | — | «hasta Bahía del Botín, y vuelves» | R | WM | ALTA |
| `tuercespina` | p03 p11 | 27.2, 75.6 | Bahía del Botín | vende (neutral) | `o_oro` | `bahia_botin` | «bajas por toda la costa oeste hasta Bahía del Botín» | V | WL | ALTA (23 vendedores neutrales + vuelos) |
| `mil_agujas` | p12 | 70.8, 76.7 | El Desierto de Sal |  | `o_fragmento_caparazon` | `desierto_sal` | «Las tortugas brillavalva del Desierto de Sal» | C | WL | ALTA |
| `mil_agujas` | p12 | 73.2, 57.3 | Tortugas brillavalva | 30-31 · 71 apariciones | `o_carne_tortuga` | `tortuga_brillavalva` | «Son lentas, no pegan fuerte» | R | WN | ALTA (15 de 71) |
| `mil_agujas` | p12 | 82.7, 56.2 | Mordedores brillavalva | 34-35 · 64 apariciones | `o_fragmento_caparazon` | `mordedor_brillavalva` | «Los mordedores brillavalva están al este de las salinas» | R | WN | ALTA (11 de 64) |
| `mil_agujas` | p12 | 78.8, 62.5 | Cráter de la Comadreja |  | `o_cola_escamosa` | — | «junto al Cráter de la Comadreja» | C | WL | ALTA |
| `mil_agujas` | p12 | 80.4, 77.5 | Circuito del Espejismo | vende (neutral) | `o_oro` | `circuito_espejismo` | «Y para vender, el Circuito del Espejismo, ahí mismo» | V | WL | ALTA (7 vendedores, side 0) |
| `riverglades` | p11 | 71.6, 67.5 | Reptadores de arena | 36-37 · 85 apariciones | `o_carne_cangrejo` | `reptador_arena` | «Son los cangrejos de la costa, al sur del Puerto Polvomecha» | R | WN | ALTA (14 de 85) |
| `riverglades` | p11 | 76.8, 61.9 | Reptadores de arena |  | `o_carne_cangrejo` | `reptador_arena` | «sueltan carne de cangrejo tierna en cuatro de cada diez muertes» | R | WN | ALTA (9) |
| `riverglades` | p11 | 78.9, 55.2 | Puerto Polvomecha | vende (neutral) | `o_oro` | `puerto_polvomecha` | «al sur del Puerto Polvomecha» | V | WL | ALTA (12 vendedores, side 0) |
| `riverglades` | p11 | 79.0, 54.2 | Fimbo Grasapuños | Sabores de mar | `fimbo` | — | «en el mismo puerto hay una misión con estos cangrejos, Sabores de mar» | P | WN | ALTA (a 1 % del rótulo del puerto: usar uno u otro) |
| `riverglades` | p06 | 58.7, 52.8 | Cazadoras llanagreste | 38-39 | `o_cola_blanda` | `cazadora_llanagreste` | «las cazadoras llanagreste, al sur de Rog'mar» | R | WN | ALTA (10 de 26) |
| `riverglades` | p06 | 59.6, 45.9 | Rog'mar | vende y vuela la Horda | `o_oro` | — | «al sur de Rog'mar» | V | WL | ALTA (side 2) |
| `riverglades` | p04 | 54.8, 75.8 | Cortijo de Wheeler | Benjy Wheeler | `benjy_wheeler` | `cortijo_wheeler` | «Están al sur del Cortijo de Wheeler, en la zona nueva» | C | WL | ALTA (Benjy en 54.8, 73.0) |
| `riverglades` | p04 | 54.5, 86.9 | Coyotes de las llanuras | 36-37 · siempre ~4 vivos | `o_cola_tupida` | `coyote_llanuras` | «Y reaparecen a lo loco» | R | WN | ALTA (9 de 14; 5 más en 54.1, 83.5) |
| `riverglades` | p04 | 54.4, 67.6 | Merodeadores coyote | 36-37 | `o_melena_espesa` | `merodeador_coyote` | «Sueltan la cola tupida suave» | R | WN | ALTA, pero quedan al NORTE del cortijo (67.6 < 75.8), no al sur |
| `riverglades` | p04 | 54.2, 84.0 | Sootfur | 38 · misión de Benjy | `sootfur` | — | «Hay un coyote con nombre, Sootfur» | P | WN | ALTA (2 de 8; las otras 6 en 54.5, 86.2, encima del grupo de coyotes) |
| `riverglades` | p04 | 64.4, 83.0 | Fortaleza de Farholde | vende y vuela (neutral) | `o_oro` | — | (venta más cercana a los coyotes) | V | WL | ALTA (11 vendedores + vuelo, side 0; el guion no la nombra) |
| `inhospitas` | p10 | 82.5, 32.2 | Crías del Barranco Lethlor | 41-43 · 110 apariciones | `o_glandula_llamas` | `cria_lethlor` | «al este de la zona, alrededor del barranco» | R | WN | ALTA (21 de 110) |
| `inhospitas` | p10 | 77.7, 62.8 | Crías del Barranco Lethlor |  | `o_vastago_oscuro` | `cria_lethlor` | «Y sueltan una mascota, el Vástago oscuro» | R | WN | ALTA (10) |
| `inhospitas` | p10 | 79.2, 53.9 | Barranco Lethlor | élites en el centro: por los bordes | `o_glandula_llamas` | `barranco_lethlor` | «Cuidado con los élites en el centro del barranco» | C | WL | ALTA |
| `inhospitas` | p10 | 78.2, 46.2 | Vetas de mitril | 16 puntos en el este | `o_mena_mitril` | — | «con vetas de mitril alrededor» | R | WM | ALTA (78.0, 48.4 · 78.3, 43.9 · 78.4, 46.2) |
| `inhospitas` | p05 | 17.6, 41.9 | Elementales inferiores | 37-39 · más desde el 13-nov | `o_piedra_inerte` | `elemental_roca_inferior` | «Los inferiores, del treinta y siete al treinta y nueve, junto a Kargath» | R | WN | ALTA (16 de 58) |
| `inhospitas` | p05 | 4.3, 47.4 | Kargath | vende y vuela la Horda | `o_oro` | `kargath` | «junto a Kargath» | V | WL | ALTA (side 2) |
| `inhospitas` | p05 | 25.8, 45.0 | Lotwil Veriatus | vendedor de los dos bandos | `o_oro` | — | (venta junto a los inferiores) | V | WP | ALTA (pin de vendedor, side 0; el guion no lo nombra) |
| `inhospitas` | p05 | 43.1, 82.4 | Elementales de roca | 39-40 | `o_tierra_elemental` | `elemental_roca` | «Los normales, al sur, junto a la Explanada del Espejismo» | R | WN | ALTA (17 de 90) |
| `inhospitas` | p05 | 37.7, 72.0 | Explanada del Espejismo |  | `o_piedra_lisa` | `explanada_espejismo` | «junto a la Explanada del Espejismo» | C | WL | ALTA |
| `inhospitas` | p05 | 2.8, 82.0 | Elementales superiores | 42-44 | `o_sal_roca` | `elemental_roca_superior` | «Y los superiores, del cuarenta y dos, al suroeste» | R | WN | ALTA (18 de 83) |
| `inhospitas` | p05 | 42.4, 52.6 | Jazzrik | vende la Alianza | `o_oro` | — | (venta de la Alianza en el centro) | V | WP | ALTA (pin de vendedor, side 1, Valle de los Colmillos) |
| `pantano` | p09 | 82.4, 92.1 | Múrlocs de marisma | 41-42 · playa | `o_almeja_boca_grande` | `murloc_marisma` | «Hay cuatro tipos en la mitad sur de la playa» | R | WN | ALTA (22 de 71) |
| `pantano` | p09 | 86.4, 82.1 | Múrlocs y vomitatintas | 41-43 | `o_perla_oro` | `vomitatintas_marisma` | «a veces, una perla» | R | WN | ALTA (16 + 16) |
| `pantano` | p09 | 81.5, 80.7 | Puesto Juncobruma | empieza aquí al 40 | `o_carne_almeja` | `puesto_juncobruma` | «Empieza por la playa al cuarenta, junto al Puesto Juncobruma» | C | WL | ALTA |
| `pantano` | p09 | 62.7, 87.2 | Oráculos y comecarnes | 43-45 · té soleado | `o_receta_te_soleado` | `oraculo_marisma` | «un grupo grande hacia la Cueva Stagalbog» | R | WN | ALTA (19 + 19) |
| `pantano` | p09 | 66.1, 77.3 | Cueva Stagalbog | demasiados juntos | `o_perla_negra` | `cueva_stagalbog` | «La parte de la cueva, mejor más tarde» | C | WL | ALTA |
| `pantano` | p06 | 42.2, 42.4 | Jaguares del pantano | 36-37 · 184 apariciones | `o_cola_blanda` | `jaguar_pantano` | «Los jaguares del Pantano de las Penas» | R | WN | ALTA (20 de 184) |
| `pantano` | p06 | 22.2, 42.4 | Jaguares del pantano | oeste | `o_bigote_cerdas` | `jaguar_pantano` | «Sueltan colas y bigotes de felino» | R | WN | ALTA (10) |
| `pantano` | p06 p09 p01 | 46.0, 53.8 | Rocal | vende y vuela la Horda | `o_oro` | `rocal` | «La Horda vende en Rocal, en medio del pantano» | V | WL | ALTA (10 vendedores + vuelo, side 2) |
| `pantano` | p06 | 26.4, 31.6 | El Puerto | vendedor de los dos bandos | `o_oro` | — | «un aviso para la Alianza» | V | WP | MEDIA (Masat T'andr, side 0; el guion no lo nombra) |
| `tanaris` | p08 | 44.4, 38.7 | Hienas Llagapata | 44-45 | `o_melena_espesa` | `hiena_llagapata` | «Sueltan la melena espesa» | R | WN | ALTA (7 de 60; hay más al este, 63.1, 43.1, fuera de las Arenas) |
| `tanaris` | p08 | 48.5, 43.1 | Hienas Llagapata |  | `o_pata_trofeo` | `hiena_llagapata` | «y la pata de trofeo grande» | R | WN | ALTA (6) |
| `tanaris` | p08 | 47.5, 36.9 | Rocs de fuego | 43-45 · huevos gigantes | `o_huevo_gigante` | `roc_fuego` | «Y si pasa un roc, mátalo también» | R | WN | ALTA (8 de 48; el grupo mayor, 48.6, 43.1, está encima de las hienas) |
| `tanaris` | p08 | 45.4, 42.9 | Arenas Abisales | triángulo de esqueletos | `o_carne_lobo_tierna` | `arenas_abisales` | «las hienas Llagapata de las Arenas Abisales» | C | WL | ALTA |
| `tanaris` | p08 | 51.2, 27.5 | Gadgetzan | vende (neutral) | `o_oro` | `gadgetzan` | «Para vender, Gadgetzan, al norte de las dunas» | V | WL | ALTA |
| `feralas` | p07 | 42.1, 21.9 | Tronadores Groddoc | 49-50 | `o_mechon_gorila` | `tronador_groddoc` | «Tronadores Groddoc y patriarcas Cueracero» | R | WN | ALTA (7 de 29) |
| `feralas` | p07 | 47.8, 27.3 | Patriarcas Cueracero | 48-49 | `o_hueso_oso` | `patriarca_cueracero` | «El hueso de oso grande, casi quince platas» | R | WN | ALTA (9 de 44; el grupo mayor, 42.9, 22.1, está encima de los tronadores) |
| `feralas` | p07 | 45.0, 22.7 | Los Dos Colosos |  | `o_mandibula_oso` | `dos_colosos` | «alrededor de Los Dos Colosos» | C | WL | ALTA |
| `feralas` | p07 | 45.0, 25.4 | Gregan Brewspewer | vendedor de los dos bandos | `o_oro` | — | (venta junto a los gorilas) | V | WP | ALTA (pin, side 0; el guion no lo nombra) |
| `feralas` | p07 | 57.0, 53.9 | Simios Groddoc | 42-43 · solo 9 | `o_pelo_gorila_burdo` | `simio_groddoc` | «los simios Groddoc y los osos Cueracero del centro de la zona» | R | WN | MEDIA (4 de 9 apariciones) |
| `feralas` | p07 | 57.8, 56.8 | Osos Cueracero | 41-42 | `o_garra_oso` | `oso_cueracero` | «sueltan casi lo mismo, a menos nivel» | R | WN | ALTA (13 de 109) |
| `feralas` | p07 | 75.2, 43.8 | Campamento Mojache | vende la Horda | `o_oro` | `campamento_mojache` | «La Horda vende en el Campamento Mojache» | V | WL | ALTA (side 2) |
| `feralas` | p07 | 31.1, 44.6 | Bastión Plumaluna | vende la Alianza | `o_oro` | `bastion_plumaluna` | «y la Alianza en el Bastión Plumaluna» | V | WL | ALTA (side 1) |
| `alterac` | p02 | 51.2, 42.0 | Dominios de los Aplastacresta | fortaleza | `o_pano_seda` | `dominios_aplastacresta` | «Junto a los Dominios de los Aplastacresta, la fortaleza de los ogros» | C | WL | ALTA |
| `alterac` | p02 | 47.9, 34.2 | Cuenca de la Matanza | cueva norte · 27 vetas | `o_mena_mitril` | `ogro_aplastacresta` | «dos cuevas, una al norte y otra al sur» | R | WL | ALTA (rótulo es-MX; 27 vetas en 48.0, 33.2) |
| `alterac` | p02 | 52.8, 47.1 | 38 vetas | oro · hierro · plata · mitril · veraplata | `o_mena_oro` | — | «En un solo rincón del mapa hay treinta y ocho vetas» | R | WM | ALTA (11 oro · 8 hierro · 7 plata · 6 mitril · 6 veraplata); SIN rótulo de cueva |
| `alterac` | p02 | 47.4, 61.6 | Ogros Aplastacresta | 34-35 · sur | `o_pano_seda` | `ogro_aplastacresta` | «Los ogros sueltan plata, paño de seda, grises y verdes» | R | WN | ALTA (17 de 111) |
| `alterac` | p02 | 47.3, 35.3 | Rizz Tornillosuelto | vendedor en una jaula | `rizz` | — | «cerca de la cueva del norte hay un vendedor gnomo» | P | WN | ALTA (side 0) |
| `alterac` | p02 | 52.7, 47.3 | Lo'Grosh | raro 39 · El pacificador | `lo_grosh` | `o_pacificador` | «en la misma zona de las vetas ronda un raro, Lo'Grosh» | P | WN | ALTA (19 de 30; las otras 6 en 47.8, 33.4) — MISMO sitio que «38 vetas» |
| `alterac` | p02 | 46.3, 47.1 | Aplastadores y magos | élite · no te acerques | `aplastador_aplastacresta` | `mago_aplastacresta` | «cerca de la fortaleza están los aplastadores y los magos» | X | WN | ALTA (aplastador 13 de 42 aquí y 18 en 42.1, 47.2, junto a las Ruinas de Alterac; magos 41.0, 43.0 y 45.7, 46.7) |
| `devastadas` | p01 | 56.2, 36.5 | Destripadores negros | 46-48 · 32 apariciones | `o_molleja_buitre` | `destripador_negro` | «entre el Alto de los Rapiñadores y la Serpiente Enroscada» | R | WN | ALTA (8 de 32) |
| `devastadas` | p01 | 62.4, 26.8 | Destripadores negros |  | `o_molleja_buitre` | `destripador_negro` | «hay competencia, y gana quien está encima» | R | WN | ALTA (5) |
| `devastadas` | p01 | 55.0, 44.0 | Destripadores negros |  | `o_molleja_buitre` | `destripador_negro` | «Solo hay unos treinta y dos puntos de aparición» | R | WN | ALTA (5: 54.4-55.8, 43.4-44.6) |
| `devastadas` | p01 | 46.5, 19.1 | Destripadores negros |  | `o_molleja_buitre` | `destripador_negro` | «Solo hay unos treinta y dos puntos de aparición» | R | WN | ALTA (4; +4 en 50.3, 17.1) |
| `devastadas` | p01 | 48.0, 29.1 | Alto de los Rapiñadores |  | `o_molleja_buitre` | `alto_rapinadores` | «entre el Alto de los Rapiñadores» | C | WL | ALTA |
| `devastadas` | p01 | 63.9, 33.6 | Serpiente Enroscada |  | `o_molleja_buitre` | — | «y la Serpiente Enroscada» | C | WL | ALTA (sin foto: la de la wiki es de Cataclysm) |
| `devastadas` | p01 | 50.6, 14.4 | Lynnore y Drazial | El vigor del buitre · El golpe decisivo | `lynnore` | `drazial` | «la piden dos misiones de la misma zona» | P | WN | ALTA (Drazial en 50.5, 14.2) |
| `devastadas` | p01 | 47.8, 18.1 | Aguijoneros Scorpok | 50-51 · desuello | `o_pinza_scorpok` | `aguijonero_scorpok` | «puedes desollar a los aguijoneros Scorpok» | R | WN | ALTA (24 de 78) |
| `devastadas` | p01 | 47.5, 22.2 | Hienas risitas famélicas | 45-46 · desuello | `o_papada_hiena` | `hiena_risitas` | «y a las hienas risitas famélicas de la zona» | R | WN | ALTA (23 de 78; comparten sitio con los scorpok) |
| `devastadas` | p01 | 65.9, 18.7 | Castillo de Nethergarde | vuelo y venta de la Alianza | `ico:ability_mount_gryphon_01` | `castillo_nethergarde` | «La Alianza llega volando al Castillo de Nethergarde» | V | WL | ALTA (3 vendedores + vuelo, side 1) |
| `mundo:intro15` | intro cierre | 14.5, 35.7 | 15 | Centauros · Desolace | `o_pano_seda` | `retador_magram` | «Hoy van quince farmeos de oro del treinta al cincuenta» | C | WL | ALTA |
| `mundo:intro15` | intro cierre | 25.1, 40.6 | 14 | Arañas · Marjal | `o_seda_arana_espesa` | `arana_niebla_negra` | — | C | WL | ALTA |
| `mundo:intro15` | intro cierre | 79.4, 75.1 | 13 | Gorilas · Tuercespina | `o_colmillo_gorila` | `gorila_velo_bruma` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 27.8, 54.6 | 12 | Tortugas · Mil Agujas | `o_fragmento_caparazon` | `tortuga_brillavalva` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 93.9, 58.9 | 11 | Cangrejos · Claros del Río | `o_carne_cangrejo` | `reptador_arena` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 90.5, 47.8 | 10 | Crías · Tierras Inhóspitas | `o_glandula_llamas` | `cria_lethlor` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 90.4, 70.8 | 9 | Múrlocs · Pantano | `o_perla_oro` | `murloc_marisma` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 26.7, 64.6 | 8 | Hienas · Tanaris | `o_melena_espesa` | `hiena_llagapata` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 10.4, 43.3 | 7 | Gorilas y osos · Feralas | `o_hueso_oso` | `tronador_groddoc` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 87.8, 67.0 | 6 | Jaguares · Pantano | `o_cola_blanda` | `jaguar_pantano` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 85.9, 48.6 | 5 | Elementales · Tierras Inhóspitas | `o_tierra_elemental` | `elemental_roca_inferior` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 91.6, 62.1 | 4 | Coyotes · Claros del Río | `o_cola_tupida` | `coyote_llanuras` | — | R | WN | ALTA |
| `mundo:intro15` | intro cierre | 77.6, 89.2 | 3 | Valijas · costa de Tuercespina | `o_valija_mitril` | — | — | R | WM | ALTA |
| `mundo:intro15` | intro cierre | 80.8, 12.7 | 2 | Ogros y vetas · Alterac | `o_mena_oro` | `ogro_aplastacresta` | — | R | WM | ALTA |
| `mundo:intro15` | intro cierre | 87.6, 72.6 | 1 | Buitres · Tierras Devastadas | `o_molleja_buitre` | `destripador_negro` | — | R | WN | ALTA |
| `mundo:r30` | resumen | 27.8, 54.6 | Tortugas · Desierto de Sal | 30-36 | `o_fragmento_caparazon` | `tortuga_brillavalva` | «las tortugas del Desierto de Sal» | R | WN | ALTA |
| `mundo:r30` | resumen | 79.4, 75.1 | Gorilas · Tuercespina | 32-35 | `o_colmillo_gorila` | `gorila_velo_bruma` | «los gorilas de Tuercespina» | R | WN | ALTA |
| `mundo:r30` | resumen | 14.5, 35.7 | Centauros · Desolace | 33-38 | `o_pano_seda` | `retador_magram` | «y los centauros de Desolace» | C | WL | ALTA |
| `mundo:r35` | resumen | 25.1, 40.6 | Arañas · Marjal | 35-38 | `o_seda_arana_espesa` | `arana_niebla_negra` | «las arañas del marjal» | C | WL | ALTA |
| `mundo:r35` | resumen | 80.8, 12.7 | Cuevas · Alterac | 34-38 | `o_mena_oro` | `ogro_aplastacresta` | «las cuevas de Alterac» | R | WM | ALTA |
| `mundo:r35` | resumen | 87.8, 67.0 | Jaguares · Pantano | 36-39 | `o_cola_blanda` | `jaguar_pantano` | «los jaguares del pantano» | R | WN | ALTA |
| `mundo:r35` | resumen | 91.6, 62.1 | Coyotes · Claros del Río | 36-40 | `o_cola_tupida` | `coyote_llanuras` | «los coyotes de Claros del Río» | R | WN | ALTA |
| `mundo:r35` | resumen | 85.9, 48.6 | Elementales inferiores | 37-39 | `o_piedra_inerte` | `elemental_roca_inferior` | «y los primeros elementales de roca» | R | WN | ALTA |
| `mundo:r40` | resumen | 90.5, 47.8 | Crías · Barranco Lethlor | 40-44 | `o_glandula_llamas` | `cria_lethlor` | «las crías del Barranco Lethlor» | R | WN | ALTA |
| `mundo:r40` | resumen | 84.9, 52.0 | Elementales superiores | 42-44 | `o_tierra_elemental` | `elemental_roca_superior` | «los elementales superiores» | R | WN | ALTA |
| `mundo:r40` | resumen | 78.7, 87.7 | Cangrejos · sur de Tuercespina | 40-41 | `o_almeja_boca_grande` | `reptador_arenas_sur` | «los cangrejos del sur de Tuercespina» | R | WN | ALTA |
| `mundo:r40` | resumen | 90.4, 70.8 | Múrlocs · Pantano | 41-45 | `o_perla_oro` | `murloc_marisma` | «y los múrlocs del Pantano de las Penas» | R | WN | ALTA |
| `mundo:r45` | resumen | 26.7, 64.6 | Hienas · Tanaris | 44-46 | `o_melena_espesa` | `hiena_llagapata` | «las hienas de Tanaris» | R | WN | ALTA |
| `mundo:r45` | resumen | 10.4, 43.3 | Gorilas y osos · Feralas | 47-50 | `o_hueso_oso` | `tronador_groddoc` | «los gorilas y osos de Feralas» | R | WN | ALTA |
| `mundo:r45` | resumen | 87.6, 72.6 | Buitres · Tierras Devastadas | 46-50 | `o_molleja_buitre` | `destripador_negro` | «y los buitres de Las Tierras Devastadas» | R | WN | ALTA |
| `mundo:r45` | resumen | 77.6, 89.2 | Pesca de valijas | cualquier nivel | `o_valija_mitril` | — | «La pesca de valijas, en cualquier momento» | R | WM | ALTA |
| `mundo:p04` | p04 | 91.6, 62.1 | Coyotes · Claros del Río | 36-40 | `o_cola_tupida` | `coyote_llanuras` | «Y desde ahí pasas directo a Tierras Inhóspitas» | R | WN | ALTA |
| `mundo:p04` | p04 | 85.9, 48.6 | Elementales · Tierras Inhóspitas | 37-39 | `o_piedra_inerte` | `elemental_roca_inferior` | «a los elementales del número cinco» | R | WN | ALTA |
| `mundo:p01` | p01 | 88.1, 68.0 | Rocal (vuelo de la Horda) | Pantano de las Penas | `ico:ability_mount_wyvern_01` | `rocal` | «Y la Horda, desde el vuelo del Pantano de las Penas» | V | WP | ALTA (maestro de vuelo Breyk) |
| `mundo:p01` | p01 | 88.6, 70.6 | Castillo de Nethergarde | vuelo de la Alianza | `ico:ability_mount_gryphon_01` | `castillo_nethergarde` | «La Alianza llega volando al Castillo de Nethergarde» | V | WL | ALTA |
| `mundo:p01` | p01 | 87.6, 72.6 | Destripadores negros | 46-48 | `o_molleja_buitre` | `destripador_negro` | «Los destripadores negros de Las Tierras Devastadas» | R | WN | ALTA |

## Puntos de venta por facción (WP/WL; para la FICHA DEL FARMEO)
| Puesto | Horda | Alianza | Los dos (neutral) |
|---|---|---|---|
| p15 Desolace | Campamento del Espíritu Errante 55.5, 55.9 (Muuran) | Punta de Nijel 65.1, 8.3 (+ vuelo) | — |
| p14 Marjal | Poblado Murohelecho 36.3, 31.4 (+ vuelo) | Isla Theramore 65.0, 47.1 (+ vuelo) | — |
| p13 / p03 Tuercespina | Campamento Grom'Gol 31.9, 28.4 (+ vuelo, buzón) | Asentamiento Rebelde 38.2, 3.5 (1 vendedor) | Bahía del Botín 27.2, 75.6 (23 + vuelos de los dos) |
| p12 Mil Agujas | — | — | Circuito del Espejismo 80.4, 77.5 (7) |
| p11 / p06 / p04 Claros del Río | Rog'mar 59.6, 45.9 (+ vuelo) | — | Puerto Polvomecha 78.9, 55.2 (12) · Fortaleza de Farholde 64.4, 83.0 (11 + vuelo) |
| p10 / p05 Tierras Inhóspitas | Kargath 4.3, 47.4 (+ vuelo) | Jazzrik 42.4, 52.6 (Valle de los Colmillos) | Lotwil Veriatus 25.8, 45.0 (Terraseca, junto a los inferiores) |
| p09 / p06 Pantano | Rocal 46.0, 53.8 (+ vuelo, Breyk 46.0, 54.6) | — (ninguno en la zona) | El Puerto 26.4, 31.6 (Masat T'andr) |
| p08 Tanaris | — | — | Gadgetzan 51.2, 27.5 (+ vuelos de los dos) |
| p07 Feralas | Campamento Mojache 75.2, 43.8 | Bastión Plumaluna 31.1, 44.6 | Gregan Brewspewer 45.0, 25.4 (junto a Los Dos Colosos) |
| p02 Alterac | — | — | Rizz Tornillosuelto 47.3, 35.3 (en la jaula, Cuenca de la Matanza) |
| p01 Tierras Devastadas | (vuelo desde Rocal) | Castillo de Nethergarde 65.9, 18.7 (3 vendedores + vuelo) | — |

## FALTA → Flow (no hay imagen real; NO generado)
- **Restos flotantes** de Tuercespina (el banco de pesca de las valijas): Wowhead no los tiene en el mapa y la wiki no tiene foto (las «Stranglethorn
  wreckage» son un barco HUNDIDO bajo el agua, no el banco flotante). → clip de pesca o Flow «corcho junto a restos flotantes en la costa de Tuercespina».
- **Cuatro valijas en el botín de un solo lance** (anécdota del p03): sin captura. → clip del jugador o Flow con la ventana de botín.
- **Cueva sur de los ogros** de Alterac y la **jaula de Rizz**: sin foto (Rizz sale como modelo 3D sin jaula). → clip de Alterac o Flow.
- **Serpiente Enroscada** (Las Tierras Devastadas): la única foto de la wiki es de Cataclysm (resumen del archivo: «cata»): descartada.
- **Los tres esqueletos de dinosaurio** de las Arenas Abisales (la ruta en triángulo): sin coordenada ni foto propia (la de Arenas Abisales enseña uno).
- **Doble especialización** (intro): no hay hechizo/ícono de Forever en el buscador de Wowhead (solo la noticia). La equitación sí: `o_equitacion`.
- **Bolsas de catorce casillas** de las valijas: no se sabe cuál es → sin pegatina por identidad.
- Fotos chicas (600 px, capturas antiguas): Valle del Velo de Bruma, Puesto Juncobruma, Cueva Stagalbog, Arenas Abisales, Los Dos Colosos, Kargath,
  Explanada del Espejismo, Campamento Mojache, Bastión Plumaluna, Barranco Lethlor, Alto de los Rapiñadores: sirven de pegatina, no de pantalla completa.
- No se hizo (el encargo dice que no hace falta): las botas épicas de los múrlocs.

## Dudas para el guion / efectos
- **Lo'Grosh suelta «El pacificador»** (The Pacifier, item 6327): maza a dos manos azul, velocidad 4,00, nivel 36 en Forever (era 32), botín propio
  3 de 104 en Wowhead Forever (tooltip: 2,88 %). Encaja con «una maza que en la subasta vale mucho». Forever no trae su nombre es-MX; Wowhead Classic:
  «El pacificador». Pegatina `o_pacificador` + foto `eq_o_pacificador.jpg`. Sus otros botines propios: Black Ogre Kickers (botas) y Boulder Pads (hombreras).
- **Coyotes y Cortijo de Wheeler:** los Coyotes de las llanuras (54.5, 86.9) y Sootfur sí están AL SUR del cortijo (rótulo 54.8, 75.8), pero los
  **Merodeadores coyote (54.4, 67.6) están al NORTE**. «Están al sur del Cortijo de Wheeler» vale para el grupo grande.
- **Élites de Alterac:** aplastadores y magos están entre las **Ruinas de Alterac (42.1, 47.2)** y la fortaleza (46.3, 47.1): el punto va en 46.3, 47.1
  («cerca de la fortaleza» es correcto).
- **«38 vetas» y Lo'Grosh** caen en la MISMA casilla (52.8, 47.1 y 52.7, 47.3): en un mismo mapa los marcadores se tapan → sacarlos en momentos
  distintos o en dos mapas. Ese rincón **no tiene rótulo de cueva**; la cueva con nombre es la del norte (**Cuenca de la Matanza**, 47.9, 34.2, donde
  está Rizz). Hay otra concentración de vetas en la **Caverna Estrecha** (37.6, 67.1: 6 de oro, 6 de hierro, 6 de plata).
- **Luremaster** tiene nombre es-MX en Wowhead Forever: **«Maestro del cebo»** (hechizo 1225455: «50 % de probabilidad de pescar un pez más» con cebo).
- **Ojo de múrloc** de «Sabores de mar»: es-MX «Ojo de múrloc marino».
- **Pantano, Alianza:** no hay vendedor de la Alianza en el Pantano de las Penas; el más cercano a los jaguares del oeste es un neutral (El Puerto, 26.4, 31.6).
- **Mismos modelos:** Coyote de las llanuras = Merodeador coyote (displayId 161); los tres elementales de roca y los dos rocs se ven casi iguales.
  **Mismo ícono:** carne de almeja = carne de cangrejo (`inv_misc_food_51`); pelo de gorila burdo = bigote de cerdas; tierra elemental = mena de hierro.
- **Fotos de confianza MEDIA** (en `_creditos.json`): `theramore` (cielo rojizo del atardecer), `lago_nazferiti` (detalle moderno, puede ser retail).
