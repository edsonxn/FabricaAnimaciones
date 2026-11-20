# Coordenadas y mapas — wow_ruta_forever (19-nov-2026; modelo: wow_oro_forever/_coords.md)

**Fuente de todas las coordenadas:** mapa mundial de **Wowhead Forever** (`nether.wowhead.com/forever/data/world-map`), vía
`videos/_investigacion_wow_ruta_forever.md` (= WHF). «WHF-lugar» = rótulo de subzona del mismo mapa (campo `places`), pasado a % de la
zona con el `rect` de la zona en el lienzo (mismo método que la investigación; comprobado: Theramore 65.0, 47.1 · Gadgetzan 51.2, 27.5 · Refugio de la
Zaga 46.1, 46.6 salen idénticos). Las entradas de mazmorra son los pines `category: dungeon/raid` del mismo archivo.

**Mapas** (`mapas/`, origen en `mapas/_fuentes.txt`): `wow.zamimg.com/images/wow/classicplus/maps/<eses|enus>/original/<id de zona>.jpg`
= mapas de **Forever** en Wowhead («classicplus»); el nombre del archivo es el **id de zona** (Elwynn 12, Dun Morogh 1…), no el nombre.
Todos en **eses** salvo los tres nuevos, que solo existen en **enus**: Isla Zephras (16593), **Claros del Río / Riverglades (16591)** y
**Shen'dralas (16651)** (ya existen: el video del oro decía que Riverglades daba 404; ahora está). Monte Hyjal: el de zamimg (616) sigue siendo
un borrador sin rasgos → `hyjal.jpg` = `File:WorldMap-Hyjal-forever.jpg` de warcraft.wiki.gg (mapa del juego, rótulos en inglés; cuadra:
Santuario de Aviana, Dae'gun y Flora Antigua caen en su rótulo). 1 % de la imagen = 1 de coordenada del juego.
Continentes: `azeroth_eses.jpg` (-1, **no trae la Isla Zephras**), `reinos_este_eses.jpg` (-3, con fronteras), `kalimdor_enus.jpg` (-6; no hay eses).
**Vista general de las 14 paradas = `mundo_forever.jpg`** (4080×3187): teselas del mapa mundial interactivo de Wowhead Forever cosidas por
`_mapa_mundo.py` (Kalimdor + Zephras + Reinos del Este en su sitio real, con Claros del Río y Shen'dralas; sin rótulos, los ponemos nosotros;
tiene alguna raya fina de unión entre teselas en el mar). Sus puntos NO están medidos a ojo: salen del `rect` de cada zona (`mundo_px()` en
`_coords_check.py`) y se comprobaron en `previews/_coords_mundo.jpg`: los 23 caen en tierra y en su zona.

**Comprobación visual:** `python _coords_check.py` → `previews/_coords_check_1..11.jpg` (todos los puntos con su nombre y coordenada) +
`previews/_coords_mundo.jpg`. Revisadas a mano el 19-nov: los puntos caen en tierra y junto al rótulo de su lugar, salvo lo listado abajo.
`python _coords_check.py md` imprime la tabla de abajo. Tipos: **C** centro (pueblo/posada/vuelo) · **R** ruta · **M** mazmorra/banda · **P** PNJ/referencia.

## Correcciones y puntos dudosos (lo que NO cuadraba)
1. **Tierras de la Peste del Este: el mapa de zamimg (139) tiene el encuadre de Classic y las coordenadas de Forever NO caen en su sitio**
   (Khaelyn, vuelo de la Capilla: Classic 81.6, 59.2 → Forever 71.8, 49.5; Mano de Tyr y Cruce de Corin desplazados ~10 %). Solución:
   `mapas/peste_este_forever.jpg` = teselas de Forever recortadas con el rect de la zona (`python _mapa_mundo.py recortes`): ahí la Capilla, la
   Mano de Tyr, el Cruce de Corin y el Bosque de la Peste caen bien. `peste_este.jpg` (zamimg) se queda solo como referencia de rótulos: **no poner en él estas coordenadas**.
2. **La Ciudad Anegada** (x −15.6 de la Vega) cae fuera del mapa de zona. En las teselas de Forever **se ve la isla**: una ciudad trol en
   ruinas mar adentro, a la altura de la Arena (≈ −8.4, 50.6 de la Vega). Propuesta: `mapas/tuercespina_oeste.jpg` (la Vega con un 30 % más de
   mar al oeste; X = (x+30)/1.3) con el marcador sobre la isla y una ruta punteada desde Grom'Gol, y después zoom a `mapas/ciudad_anegada_isla.jpg`
   (la isla de cerca, zoom 7). El pin de WHF (−15.6, 58.3; valores redondos = colocado a mano) cae en el agua al suroeste de la isla: marcar la isla, no el pin.
3. **Prisión de Alcaz:** en el mapa del Marjal (dibujo de Classic) la isla es pequeña y el Sargento Ulka (70.3, 19.1) cae en el agua. En Forever la
   isla creció (jungla, prisión, muelle): `mapas/alcaz_isla.jpg` (teselas; X = (x−64)/0.22, Y = (y−8)/0.22) → Ulka en el muelle oeste y la entrada
   en la isla. Usar ese para la parada 11.
4. **Templo de Atal'Hakkar:** el pin de mazmorra de WHF (77.3, 35.9) cae en la orilla noreste del Pantano, lejos del templo dibujado. En
   pantalla usar el rótulo de WHF **70.0, 52.9** (el templo hundido en el centro del lago).
5. **Profundidades de Roca Negra:** el pin (22.6, 7.5 de Las Estepas) es el portal interior y cae en la franja de La Garganta de Fuego. En
   pantalla: el icono de la **Montaña Roca Negra, 29.5, 36.0** (medido en el mapa). Franclorn (29.0, 29.0) está dentro de la montaña.
6. **Avanzada del Sur** (93.8, 21.3 de Crestagrana) cae en el borde mismo del mapa de Crestagrana (dibujo de Classic, sin nada). Mejor mostrarla
   en el mapa de Claros del Río: **37.6, 74.7** (WHF-lugar «Southern Watch»), que además enseña que es la puerta a la zona nueva.
7. **El Bancal del Creador:** la entrada (17.8, 60.8 de Las Mil Agujas) cae en el borde oeste del mapa de Las Mil Agujas, al norte del cráter
   (8,8 % por encima del mapa de Un'Goro). En tierra, sin nada dibujado. Confianza MEDIA (no comprobado en el cliente).
8. **Gnomeregan** 17.7, 39.2 es el pin del portal (al fondo del valle oeste); el rótulo/puerta exterior está en 26.1, 39.8. **Hogger** 25.0, 92.9
   (games.gg) cae en la orilla del río del sur de Elwynn: es zona de patrulla, confianza MEDIA.
9. Rótulos algo separados del punto (no es error, el rótulo del mapa no está encima del sitio): Claro Soleado (47.3, 47.9; rótulo
   «Sunnyglade» ~45, 58), Laderas Maculadas de Hyjal (59.3, 74.3; rótulo «Tainted Foothills» ~68, 69), Refugio de Marshal (43.6, 7.2 en el
   acantilado; rótulo ~50, 16), Cañada Umbría (56.9, 32.8; rótulo ~59, 43). Ningún punto cae en el mar salvo los que deben (Brazanegra, en la
   ensenada de Zoram; la Ciudad Anegada).
10. Otros mapas que siguen siendo dibujo de Classic aunque la zona cambió: Tirisfal (el Fuerte de Bandarion, Bosque Susurrante y Vallesombra caen
   en montaña, sin dibujo), Los Humedales (Refugio Faucedraco y el Sitio de Excavación sin dibujo), Azshara sí trae lo nuevo. Alterac **sí** trae
   Dalaran dibujada como ciudad.
11. Nombres: el mapa de Claros del Río (enus) dice **Bolder'ok** = Pedreg'ok (es-MX), **Powderfuse Port** = Puerto Polvomecha, **Farholde Keep**,
   **Rog'mar**, **Sunnyglade**, **Twilight's Shroud**, **Wheeler's Grange**. Shen'dralas: **Valley of Bones**, **Evenshade's Overlook**,
   **Magram Front**, **Forlorn Gardens**, **Outcast Hideaway**, **Bristleback Retreat**. Rótulos de MG en español, como dice el guion.

## Tabla por parada
| Parada | Mapa | Punto | Tipo | x, y | Fuente | Confianza |
|---|---|---|---|---|---|---|
| 1 | `alterac` | muelle dirigible (cielonatos A) | C | 12.8, 51.2 | WHF | ALTA |
| 1 | `dun_morogh` | Valle de Crestanevada | R | 24.1, 74.3 | WHF | ALTA |
| 1 | `dun_morogh` | Kharanos | C | 46.4, 52.0 | WHF | ALTA |
| 1 | `dun_morogh` | posada (Belm) | C | 47.4, 52.4 | WHF | ALTA |
| 1 | `durotar` | Valle de los Retos | R | 43.9, 62.2 | WHF | ALTA |
| 1 | `durotar` | Cerrotajo | C | 52.6, 42.4 | WHF | ALTA |
| 1 | `durotar` | posada (Grosk) | C | 51.6, 41.6 | WHF | ALTA |
| 1 | `elwynn` | Abadía de Villanorte | R | 49.4, 41.3 | WHF | ALTA |
| 1 | `elwynn` | Villadorada | C | 42.4, 66.6 | WHF | ALTA |
| 1 | `elwynn` | posada (Farley) | C | 43.8, 65.8 | WHF | ALTA |
| 1 | `elwynn` | Aserradero Vega del Este | R | 84.1, 65.3 | WHF | ALTA |
| 1 | `elwynn` | Hogger (nv 11) | P | 25.0, 92.9 | games.gg | MEDIA (guía; zona de patrulla) |
| 1 | `elwynn` | vuelo Ventormenta (Dungar) | C | 30.1, 38.8 | WHF | ALTA |
| 1 | `mulgore` | Campamento Narache | R | 44.4, 77.4 | WHF | ALTA |
| 1 | `mulgore` | Pezuña de Sangre | C | 46.7, 63.2 | WHF | ALTA |
| 1 | `mulgore` | posada (Kauth) | C | 45.9, 64.1 | WHF | ALTA |
| 1 | `mulgore` | vuelo Cima del Trueno | C | 39.8, 35.7 | WHF | ALTA |
| 1 | `mulgore` | muelle dirigible (cielonatos H) | C | 34.3, 26.1 | WHF | ALTA |
| 1 | `teldrassil` | Cañada Umbría | R | 56.9, 32.8 | WHF | ALTA |
| 1 | `teldrassil` | Dolanaar | C | 56.3, 60.2 | WHF | ALTA |
| 1 | `teldrassil` | posada (Keldamyr) | C | 55.6, 59.8 | WHF | ALTA |
| 1 | `teldrassil` | vuelo Rut'theran | C | 58.4, 94.0 | WHF | ALTA |
| 1 | `tirisfal` | Camposanto | R | 32.0, 65.0 | WHF | ALTA |
| 1 | `tirisfal` | Rémol | C | 61.0, 52.7 | WHF | ALTA |
| 1 | `tirisfal` | posada (Renee) | C | 61.6, 52.0 | WHF | ALTA |
| 1 | `tirisfal` | Fuerte de Bandarion | R | 21.8, 46.1 | WHF | ALTA |
| 1 | `tirisfal` | Bosque Susurrante | R | 16.6, 58.2 | WHF | ALTA |
| 1 | `tirisfal` | Vallesombra | R | 12.2, 63.8 | WHF | ALTA |
| 1 | `zephras` | Poblado Thendal | R | 42.2, 23.5 | WHF | ALTA |
| 1 | `zephras` | Aldea Shen'dar | C | 43.4, 45.1 | WHF | ALTA |
| 1 | `zephras` | posada (Coriella) | C | 43.0, 43.2 | WHF | ALTA |
| 1 | `zephras` | Valanaar | C | 63.2, 77.5 | WHF | ALTA |
| 1 | `zephras` | posada (Donaal) | C | 62.2, 72.6 | WHF | ALTA |
| 1 | `zephras` | Muelles Celestiales | R | 63.2, 85.6 | WHF | ALTA |
| 1 | `zephras` | Elaadrin (a Dalaran) | P | 66.6, 79.8 | WHF | ALTA |
| 2 | `argenteos` | El Sepulcro | C | 43.6, 41.4 | WHF | ALTA |
| 2 | `argenteos` | vuelo (Karos) | C | 45.6, 42.4 | WHF | ALTA |
| 2 | `argenteos` | Aldea Piroleña | R | 46.8, 73.2 | WHF | ALTA |
| 2 | `baldios` | El Cruce | C | 52.1, 30.6 | WHF | ALTA |
| 2 | `baldios` | vuelo (Devrak) | C | 51.4, 30.2 | WHF | ALTA |
| 2 | `baldios` | Trinquete | R | 62.2, 37.9 | WHF | ALTA |
| 2 | `costa_oscura` | Auberdine | C | 38.6, 43.4 | WHF | ALTA |
| 2 | `costa_oscura` | vuelo (Caylais) | C | 36.4, 45.6 | WHF | ALTA |
| 2 | `costa_oscura` | posada | C | 37.0, 44.0 | WHF | ALTA |
| 2 | `dun_morogh` | Salón de Señores Feudales | M | 53.5, 34.8 | WHF | ALTA (bajo Forjaz) |
| 2 | `dun_morogh` | Earthseer Farsen | P | 64.8, 58.4 | WHF | ALTA |
| 2 | `loch_modan` | Thelsamar | C | 35.0, 46.8 | WHF | ALTA |
| 2 | `loch_modan` | vuelo (Thorgrum) | C | 33.8, 50.8 | WHF | ALTA |
| 2 | `loch_modan` | posada | C | 35.4, 48.4 | WHF | ALTA |
| 2 | `loch_modan` | Presa de las Tres Cabezas | R | 55.2, 14.3 | WHF | ALTA |
| 2 | `paramos` | Colina del Centinela | C | 56.8, 47.3 | WHF | ALTA |
| 2 | `paramos` | vuelo (Thor) | C | 56.4, 52.6 | WHF | ALTA |
| 2 | `paramos` | posada (Heather) | C | 52.8, 53.6 | WHF | ALTA |
| 2 | `paramos` | Arroyo de la Luna | R | 43.0, 69.3 | WHF | ALTA |
| 2 | `paramos` | Minas de la Muerte | M | 38.2, 77.5 | WHF | ALTA |
| 2 | `tirisfal` | Ruinas de Lordaeron | M | 61.6, 72.6 | WHF | ALTA (bajo Entrañas) |
| 3 | `baldios` | Cuevas de los Lamentos | M | 47.7, 35.0 | WHF | ALTA |
| 3 | `baldios` | Campamento Taurajo | C | 44.8, 58.7 | WHF | ALTA |
| 3 | `crestagrana` | Villa del Lago | C | 24.0, 45.1 | WHF | ALTA |
| 3 | `crestagrana` | posada (Brianna) | C | 26.8, 44.8 | WHF | ALTA |
| 3 | `crestagrana` | vuelo (Ariena) | C | 30.6, 59.4 | WHF | ALTA |
| 3 | `crestagrana` | Molino de Alther | R | 46.2, 39.7 | WHF | ALTA |
| 3 | `crestagrana` | Cascadas Petravista | R | 76.9, 62.7 | WHF | ALTA |
| 3 | `crestagrana` | Avanzada del Sur | R | 93.8, 21.3 | WHF | ALTA |
| 3 | `paramos` | Alba Fairmoon (misión nueva) | P | 52.4, 53.0 | WHF | ALTA |
| 3 | `sierra_espolon` | Refugio Roca del Sol | C | 47.8, 60.8 | WHF | ALTA |
| 3 | `sierra_espolon` | vuelo (Tharm) | C | 45.2, 59.8 | WHF | ALTA |
| 3 | `sierra_espolon` | posada (Jayka) | C | 47.4, 62.0 | WHF | ALTA |
| 4 | `argenteos` | Castillo de Colmillo Oscuro | M | 44.7, 67.8 | WHF | ALTA |
| 4 | `bosque_ocaso` | Villa Oscura | C | 74.2, 47.1 | WHF | ALTA |
| 4 | `bosque_ocaso` | vuelo (Felicia) | C | 77.4, 44.4 | WHF | ALTA |
| 4 | `bosque_ocaso` | Cementerio Jardín Sereno | R | 79.6, 72.2 | WHF | ALTA |
| 4 | `bosque_ocaso` | Cerro del Cuervo | R | 19.4, 57.5 | WHF | ALTA |
| 4 | `humedales` | Puerto de Menethil | C | 10.6, 55.3 | WHF | ALTA |
| 4 | `humedales` | vuelo (Shellei) | C | 9.4, 59.6 | WHF | ALTA |
| 4 | `humedales` | Excavación de Whelgar | R | 34.5, 49.7 | WHF | ALTA |
| 4 | `humedales` | Refugio Faucedraco | R | 66.8, 47.2 | WHF | ALTA |
| 4 | `humedales` | El Enano Borracho | R | 52.2, 79.9 | WHF | ALTA |
| 4 | `laderas` | Molino Tarren | C | 61.5, 20.0 | WHF | ALTA |
| 4 | `laderas` | vuelo (Zarise) | C | 60.2, 18.6 | WHF | ALTA |
| 4 | `laderas` | Campos de Trabalomas | R | 31.8, 36.7 | WHF | ALTA |
| 4 | `laderas` | Castillo de Durnholde | R | 81.8, 39.8 | WHF | ALTA |
| 4 | `vallefresno` | Astranaar | C | 36.1, 50.8 | WHF | ALTA |
| 4 | `vallefresno` | vuelo (Daelyshia) | C | 34.4, 48.0 | WHF | ALTA |
| 4 | `vallefresno` | Refugio de la Algaba | R | 61.0, 51.8 | WHF | ALTA |
| 4 | `vallefresno` | Puesto del Hachazo | C | 74.0, 62.1 | WHF | ALTA |
| 4 | `vallefresno` | Avanzada de Zoram'gar | C | 12.0, 34.1 | WHF-lugar | ALTA |
| 4 | `vallefresno` | Cavernas de Brazanegra | M | 16.5, 11.0 | WHF | ALTA |
| 5 | `baldios` | Horado Rajacieno | M | 42.3, 89.9 | WHF | ALTA |
| 5 | `dun_morogh` | Gnomeregan | M | 17.7, 39.2 | WHF | ALTA |
| 5 | `feralas` | Thalanaar | C | 89.5, 46.3 | WHF | ALTA |
| 5 | `humedales` | Sitio de Excavación (mazmorra) | M | 38.5, 60.5 | WHF | ALTA |
| 5 | `laderas` | Costasur | C | 50.0, 56.4 | WHF | ALTA |
| 5 | `mil_agujas` | Poblado Viento Libre | C | 45.7, 50.7 | WHF | ALTA |
| 5 | `mil_agujas` | vuelo (Nyse) | C | 45.0, 49.2 | WHF | ALTA |
| 5 | `mil_agujas` | Campamento E'thok | R | 18.6, 22.2 | WHF | ALTA |
| 5 | `mil_agujas` | El Desierto de Sal | R | 70.8, 76.7 | WHF | ALTA |
| 6 | `alterac` | Ciudad de Dalaran (mazmorra) | M | 16.7, 68.8 | WHF | ALTA |
| 6 | `alterac` | posaderos Dalaran | C | 17.8, 66.2 | WHF | MEDIA (bando sin comprobar) |
| 6 | `alterac` | Imagen de Modera | P | 7.7, 58.9 | WHF | ALTA |
| 6 | `arathi` | Refugio de la Zaga | C | 46.1, 46.6 | WHF | ALTA |
| 6 | `arathi` | vuelo (Cedrik) | C | 45.6, 46.2 | WHF | ALTA |
| 6 | `arathi` | Sentencia | C | 73.9, 35.8 | WHF | ALTA |
| 6 | `arathi` | vuelo (Urda) | C | 73.0, 32.6 | WHF | ALTA |
| 6 | `arathi` | Círculo de Vínculo Este | R | 68.1, 29.9 | WHF | ALTA |
| 6 | `arathi` | Poblado Secacorteza | R | 69.0, 70.1 | WHF | ALTA |
| 6 | `arathi` | Castillo de Stromgarde | R | 21.8, 64.6 | WHF | ALTA |
| 6 | `desolace` | Punta de Nijel | C | 65.1, 8.3 | WHF | ALTA |
| 6 | `desolace` | Fortaleza Hacha de Trueno | R | 55.2, 26.8 | WHF | ALTA |
| 6 | `desolace` | Cementerio de Kodos | R | 49.3, 60.1 | WHF | ALTA |
| 6 | `desolace` | Aldea Cazasombras | C | 25.3, 70.4 | WHF | ALTA |
| 6 | `tirisfal` | Monasterio Escarlata | M | 85.1, 31.4 | WHF | ALTA |
| 7 | `baldios` | Zahúrda Rajacieno | M | 50.9, 92.9 | WHF | ALTA |
| 7 | `ciudad_anegada_isla` | isla de la Ciudad Anegada | M | 50.0, 50.0 | medido en teselas WHF | ALTA |
| 7 | `ciudad_anegada_isla` | entrada [WHF] -15.6, 58.3 de la Vega | M | 18.5, 85.0 | WHF | MEDIA (pin redondo, en el agua) |
| 7 | `inhospitas` | Kargath | C | 4.3, 47.4 | WHF | ALTA |
| 7 | `inhospitas` | Uldaman | M | 35.2, 10.3 | WHF | ALTA |
| 7 | `marjal` | Isla Theramore | C | 65.0, 47.1 | WHF | ALTA |
| 7 | `marjal` | Colina de las Brujas | R | 56.7, 32.9 | WHF | ALTA |
| 7 | `marjal` | Ciénaga de Fuego | R | 52.9, 79.5 | WHF | ALTA |
| 7 | `marjal` | Poblado Murohelecho | C | 36.3, 31.4 | WHF | ALTA |
| 7 | `pantano` | Rocal | C | 46.0, 53.8 | WHF | ALTA |
| 7 | `tuercespina` | Asentamiento Rebelde | C | 38.2, 3.5 | WHF | ALTA |
| 7 | `tuercespina` | Expedición de Nesingwary | R | 36.1, 11.3 | WHF | ALTA |
| 7 | `tuercespina` | Base de Kurzen | R | 45.5, 9.0 | WHF | ALTA |
| 7 | `tuercespina` | Arena Gurubashi | R | 31.9, 50.5 | WHF | ALTA |
| 7 | `tuercespina` | Bahía del Botín | C | 27.2, 75.6 | WHF | ALTA |
| 7 | `tuercespina` | Campamento Grom'Gol | C | 31.9, 28.4 | WHF | ALTA |
| 7 | `tuercespina_oeste` | La Ciudad Anegada (mar adentro) | M | 11.1, 58.3 | WHF | MEDIA (entrada en el agua: comprobar) |
| 7 | `tuercespina_oeste` | Arena Gurubashi | R | 47.6, 50.5 | WHF | ALTA |
| 7 | `tuercespina_oeste` | Grom'Gol | C | 47.6, 28.4 | WHF | ALTA |
| 7 | `tuercespina_oeste` | Bahía del Botín | C | 44.0, 75.6 | WHF | ALTA |
| 7 | `tuercespina_oeste` | isla de la Ciudad Anegada (vista en las teselas) | M | 16.6, 50.6 | medido en teselas WHF | ALTA (isla con ruinas trol) |
| 8 | `riverglades` | Colinas Espinosas | R | 28.7, 62.4 | WHF | ALTA |
| 8 | `riverglades` | Fortaleza de Farholde | C | 64.4, 83.0 | WHF | ALTA |
| 8 | `riverglades` | vuelo (Gretchen) | C | 60.6, 81.4 | WHF | ALTA |
| 8 | `riverglades` | Cortijo de Wheeler | R | 54.8, 75.8 | WHF | ALTA |
| 8 | `riverglades` | Avanzada de Terral | R | 59.6, 64.4 | WHF | ALTA |
| 8 | `riverglades` | Claro Soleado | R | 47.3, 47.9 | WHF | ALTA |
| 8 | `riverglades` | Sudario Crepuscular | R | 28.7, 42.8 | WHF | ALTA |
| 8 | `riverglades` | Pedreg'ok | R | 65.1, 18.0 | WHF | ALTA |
| 8 | `riverglades` | Bastión de Krol'dok | M | 48.6, 26.3 | WHF | ALTA |
| 8 | `riverglades` | Rog'mar | C | 59.6, 45.9 | WHF | ALTA |
| 8 | `riverglades` | Puerto Polvomecha | C | 78.9, 55.2 | WHF | ALTA |
| 8 | `riverglades` | barco a Tanaris | C | 80.6, 54.6 | WHF | ALTA |
| 8 | `tanaris` | muelle barco a Claros del Río | C | 68.6, 23.0 | WHF | ALTA |
| 9 | `desolace` | Valle de los Huesos (a Shen'dralas) | R | 60.5, 90.2 | WHF | ALTA |
| 9 | `desolace` | Maraudon | M | 29.1, 62.9 | WHF | ALTA |
| 9 | `shendralas` | Valle de los Huesos | R | 24.9, 25.7 | WHF-lugar | ALTA |
| 9 | `shendralas` | Orgrul (H) | P | 35.8, 12.8 | WHF | ALTA |
| 9 | `shendralas` | Nerlokh (H) | P | 21.0, 22.6 | WHF | ALTA |
| 9 | `shendralas` | Mordent Evenshade | P | 35.0, 46.4 | WHF | ALTA |
| 9 | `shendralas` | Mirador de Sombrapar | R | 32.9, 45.1 | WHF | ALTA |
| 9 | `shendralas` | Escondite de Marginado | R | 36.2, 76.8 | WHF | ALTA |
| 9 | `shendralas` | Frente Magram | R | 62.2, 54.9 | WHF | ALTA |
| 9 | `shendralas` | Jardines Desolados | R | 70.3, 72.0 | WHF | ALTA |
| 9 | `shendralas` | Retirada Erizapúas | R | 72.0, 23.2 | WHF | ALTA |
| 10 | `feralas` | Bastión Plumaluna | C | 31.1, 44.6 | WHF | ALTA |
| 10 | `feralas` | vuelo (Fyldren) | C | 30.2, 43.2 | WHF | ALTA |
| 10 | `feralas` | Campamento Mojache | C | 75.2, 43.8 | WHF | ALTA |
| 10 | `feralas` | vuelo (Shyn) | C | 75.4, 44.2 | WHF | ALTA |
| 10 | `feralas` | Avanzada Gordunni | R | 75.7, 29.9 | WHF | ALTA |
| 10 | `feralas` | Los Dos Colosos | R | 45.0, 22.7 | WHF | ALTA |
| 10 | `interior` | Pico Nidal | C | 14.4, 48.0 | WHF | ALTA |
| 10 | `interior` | vuelo (Guthrum) | C | 11.0, 46.0 | WHF | ALTA |
| 10 | `interior` | Avanzada Quel'Danil | R | 32.3, 46.1 | WHF | ALTA |
| 10 | `interior` | Shadra'Alor | R | 34.0, 72.1 | WHF | ALTA |
| 10 | `interior` | Jintha'Alor | R | 62.6, 76.0 | WHF | ALTA |
| 10 | `interior` | Poblado Sañadiente | C | 78.3, 79.5 | WHF | ALTA |
| 10 | `tanaris` | Gadgetzan | C | 51.2, 27.5 | WHF | ALTA |
| 10 | `tanaris` | vuelo A (Bera) | C | 51.0, 29.2 | WHF | ALTA |
| 10 | `tanaris` | Campo del Manantial | R | 60.8, 41.5 | WHF | ALTA |
| 10 | `tanaris` | Base Machacaduna | R | 40.5, 56.7 | WHF | ALTA |
| 10 | `tanaris` | Zul'Farrak | M | 38.7, 19.9 | WHF | ALTA |
| 11 | `alcaz_isla` | Prisión de Alcaz (entrada) | M | 61.8, 43.6 | WHF | ALTA |
| 11 | `alcaz_isla` | Sargento Ulka (muelle) | P | 28.6, 50.5 | WHF | ALTA |
| 11 | `azshara` | Punta Talrendis | C | 11.7, 77.9 | WHF | ALTA |
| 11 | `azshara` | Valormok | C | 21.8, 50.0 | WHF | ALTA |
| 11 | `azshara` | Ruinas de Eldarath | R | 33.6, 56.9 | WHF | ALTA |
| 11 | `azshara` | Camp. Vanguardia Thalassiano | R | 70.5, 29.3 | WHF | ALTA |
| 11 | `azshara` | Fortaleza Legashi | R | 67.2, 15.5 | WHF | ALTA |
| 11 | `marjal` | Prisión de Alcaz | M | 77.6, 17.6 | WHF | ALTA |
| 11 | `marjal` | Sargento Ulka | P | 70.3, 19.1 | WHF | MEDIA: en este mapa cae en el agua; en Forever está en un muelle (ver alcaz_isla) |
| 11 | `pantano` | Templo de Atal'Hakkar | M | 70.0, 52.9 | WHF-lugar | ALTA (el templo dibujado en el mapa) |
| 11 | `pantano` | pin mazmorra WHF (Atal'Hakkar) | P | 77.3, 35.9 | WHF | BAJA: cae en la orilla NE, lejos del templo; NO usar |
| 11 | `ungoro` | Refugio de Marshal | C | 43.6, 7.2 | WHF | ALTA |
| 11 | `ungoro` | vuelo (Gryfe) | C | 45.2, 5.8 | WHF | ALTA |
| 11 | `ungoro` | Fosas Lakkari | R | 51.8, 20.9 | WHF | ALTA |
| 11 | `ungoro` | Cresta Penacho en Llamas | R | 49.1, 49.3 | WHF | ALTA |
| 11 | `ungoro` | Baños de Golakka | R | 30.2, 53.4 | WHF | ALTA |
| 12 | `baldios` | posada Wiley (Oso espectral) | P | 62.0, 39.4 | WHF | ALTA |
| 12 | `estepas` | Vigilia de Morgan | C | 85.9, 67.6 | WHF | ALTA |
| 12 | `estepas` | vuelo (Borgus) | C | 84.4, 68.2 | WHF | ALTA |
| 12 | `estepas` | Peñasco Llamarada | C | 65.5, 23.0 | WHF | ALTA |
| 12 | `estepas` | Roca Machacamiedo | R | 80.2, 38.5 | WHF | ALTA |
| 12 | `estepas` | Ruinas de Thaurissan | R | 60.9, 36.8 | WHF | ALTA |
| 12 | `estepas` | Cumbre de Roca Negra | R | 33.0, 25.2 | WHF | ALTA |
| 12 | `estepas` | pin Profundidades (portal interior) | P | 22.6, 7.5 | WHF | ALTA el dato, pero cae fuera de Las Estepas: NO usar en pantalla |
| 12 | `estepas` | Montaña Roca Negra (Profundidades) | M | 29.5, 36.0 | medido en el mapa | ALTA (icono de la montaña) |
| 12 | `estepas` | Franclorn Forjador | P | 29.0, 29.0 | WHF | ALTA |
| 12 | `peste_oeste` | Campamento del Orvallo | C | 42.7, 85.3 | WHF | ALTA |
| 12 | `peste_oeste` | El Baluarte | C | 26.4, 51.7 | WHF | ALTA |
| 12 | `peste_oeste` | Colina de las Penas | R | 48.1, 80.8 | WHF | ALTA |
| 12 | `peste_oeste` | Campo de Piedramácula | R | 38.8, 52.9 | WHF | ALTA |
| 13 | `azshara` | Bastión Faucenegra | M | 39.6, 32.3 | WHF | ALTA |
| 13 | `azshara` | Tradicionalista Nok | P | 41.4, 20.0 | WHF | ALTA |
| 13 | `cuna_invierno` | Vista Eterna | C | 61.2, 38.2 | WHF | ALTA |
| 13 | `cuna_invierno` | Aldea Estrella Fugaz | R | 51.2, 27.1 | WHF | ALTA |
| 13 | `cuna_invierno` | Roca Sable de Hielo | R | 51.6, 12.3 | WHF | ALTA |
| 13 | `cuna_invierno` | Mazthoril | R | 58.7, 51.8 | WHF | ALTA |
| 13 | `cuna_invierno` | Garganta Negro Rumor (a Hyjal) | R | 58.2, 85.6 | WHF | ALTA |
| 13 | `feralas` | La Masacre | M | 62.0, 33.3 | WHF | ALTA |
| 13 | `frondavil` | Bastión Fauces de Madera (túnel) | R | 68.5, 6.1 | WHF | ALTA |
| 13 | `peste_este_forever` | Capilla Esperanza de la Luz | C | 71.9, 49.1 | WHF | ALTA |
| 13 | `peste_este_forever` | Cruce de Corin | R | 53.3, 58.4 | WHF | ALTA |
| 13 | `peste_este_forever` | Mano de Tyr | R | 73.5, 70.1 | WHF | ALTA |
| 13 | `peste_este_forever` | Bosque de la Peste | R | 24.6, 29.4 | WHF | ALTA |
| 13 | `silithus` | Fuerte Cenarion | C | 52.2, 39.9 | WHF | ALTA |
| 13 | `silithus` | vuelo A | C | 50.6, 34.4 | WHF | ALTA |
| 13 | `silithus` | vuelo H | C | 48.8, 36.6 | WHF | ALTA |
| 14 | `hyjal` | Laderas Maculadas | R | 59.3, 74.3 | WHF | ALTA |
| 14 | `hyjal` | vuelo (Bluebell) | C | 55.0, 82.8 | WHF | ALTA |
| 14 | `hyjal` | Santuario de Aviana | R | 53.6, 58.5 | WHF | ALTA |
| 14 | `hyjal` | Flora Antigua | R | 13.3, 49.9 | WHF | ALTA |
| 14 | `hyjal` | campamento A (Sefira) | C | 15.6, 54.6 | WHF | ALTA |
| 14 | `hyjal` | campamento H (Zet'gan) | C | 14.0, 54.8 | WHF | ALTA |
| 14 | `hyjal` | Dae'gun | R | 58.4, 38.3 | WHF | ALTA |
| 14 | `hyjal` | Cima de la Eternidad | R | 78.5, 36.9 | WHF | ALTA |
| 14 | `hyjal` | vuelo Cima (Fayran) | C | 68.6, 44.2 | WHF | ALTA |
| 14 | `hyjal` | Cavernas del Túmulo + Cumbre Hyjal | M | 58.4, 57.1 | WHF | ALTA (bandas del 9-dic) |
| 14 | `marjal` | Guarida de Onyxia | M | 52.9, 77.7 | WHF | ALTA |
| 14 | `mil_agujas` | Bancal del Creador (entrada) | M | 17.8, 60.8 | WHF | MEDIA (sin comprobar en el cliente) |

## Vista general (mundo_forever.jpg): una marca por parada

| Parada | Lugar | Zona | x, y zona | píxel en mundo_forever.jpg (4080×3187) |
|---|---|---|---|---|
| 1 | Isla Zephras (inicio cielonato) | `zephras` | 43.4, 45.1 | 2082, 728 |
| 1 | Villadorada | `elwynn` | 42.4, 66.6 | 3188, 2388 |
| 1 | Kharanos | `dun_morogh` | 46.4, 52.0 | 3254, 1920 |
| 1 | Dolanaar | `teldrassil` | 56.3, 60.2 | 458, 331 |
| 1 | Cerrotajo | `durotar` | 52.6, 42.4 | 1141, 1468 |
| 1 | Pezuña de Sangre | `mulgore` | 46.7, 63.2 | 619, 1785 |
| 1 | Rémol | `tirisfal` | 61.0, 52.7 | 3163, 980 |
| 2 | P2 Colina del Centinela | `paramos` | 56.8, 47.3 | 3073, 2510 |
| 2 | P2 El Cruce | `baldios` | 52.1, 30.6 | 891, 1561 |
| 3 | P3 Villa del Lago | `crestagrana` | 24.0, 45.1 | 3460, 2357 |
| 4 | P4 Puerto de Menethil | `humedales` | 10.6, 55.3 | 3295, 1691 |
| 5 | P5 Viento Libre | `mil_agujas` | 45.7, 50.7 | 865, 2160 |
| 6 | P6 Arathi | `arathi` | 46.1, 46.6 | 3499, 1400 |
| 6 | P6 Dalaran | `alterac` | 16.7, 68.8 | 3158, 1224 |
| 7 | P7 Bahía del Botín | `tuercespina` | 27.2, 75.6 | 3138, 2976 |
| 8 | P8 Claros del Río | `riverglades` | 59.6, 45.9 | 3770, 2204 |
| 9 | P9 Shen'dralas | `shendralas` | 35.0, 46.4 | 415, 1810 |
| 10 | P10 Gadgetzan | `tanaris` | 51.2, 27.5 | 1022, 2363 |
| 11 | P11 Azshara | `azshara` | 21.8, 50.0 | 1098, 1068 |
| 11 | P11 Alcaz | `marjal` | 77.6, 17.6 | 1178, 1824 |
| 12 | P12 Las Estepas Ardientes | `estepas` | 85.9, 67.6 | 3530, 2252 |
| 13 | P13 Vista Eterna | `cuna_invierno` | 61.2, 38.2 | 1131, 699 |
| 14 | P14 Monte Hyjal | `hyjal` | 53.6, 58.5 | 906, 912 |
