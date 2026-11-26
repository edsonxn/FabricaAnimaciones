# Coordenadas y mapas — wow_ruta_profesiones (25-nov-2026; modelo: wow_errores_60/_coords.md)

**Fuentes de las coordenadas:** INV = `videos/_investigacion_wow_ruta_profesiones.md` (coordenadas de Wowhead Forever: pines del mapa mundial
[WHF-MAP] y `/way` de los entrenadores [WP-TR], comprobadas entre sí); WHF = pin de mazmorra del mapa mundial de **Wowhead Forever**
(`nether.wowhead.com/forever/data/world-map`, leído el 25-nov); WHF-lugar = rótulo de pueblo/subzona del mismo archivo (campo `places`) pasado a
% de la zona con el `rect` de la zona (sale igual que la investigación: Theramore 65.0, 47.1 · Gadgetzan 51.2, 27.5 · Vega Cicatriz Feral 54.6, 56.5 ·
Refugio Roca del Sol 47.8, 60.8 · Torre de Azora 65.8, 68.1 · Sentencia 73.9, 35.8). Nada de memoria.

**Mapas** (`mapas/`, origen en `mapas/_fuentes.txt`, se rehacen con `python _mapas.py [nombre…]`):
- Zona (1 % de la imagen = 1 de coordenada): `wow.zamimg.com/images/wow/classicplus/maps/<eses|enus>/original/<id>.jpg` (Forever en Wowhead):
  durotar 14 · mulgore 215 · teldrassil 141 · elwynn 12 · humedales 11 · argenteos 130 · laderas 267 · arathi 45 · mil_agujas 400 ·
  **riverglades 16591 (enus)** · interior 47 · tanaris 440 · ungoro 490 · frondavil 361 · cuna_invierno 618 · estepas 46 · tuercespina 33 ·
  baldios 17 · crestagrana 44 · alterac 36 · feralas 357 · pantano 8 · sierra_espolon 406 · inhospitas 3 · desolace 405 · vallefresno 331 ·
  marjal 15 · azshara 16 · **shendralas 16651 (enus)** · loch_modan 38 · bosque_ocaso 10 · paramos 40 · **forjaz 1537** (ciudad).
- `hyjal` = `File:WorldMap-Hyjal-forever.jpg` de warcraft.wiki.gg (mapa del juego de **Forever**, rótulos en inglés; el 616 de zamimg es un borrador).
  Claros del Río y Monte Hyjal son zonas de Forever: sus mapas son los de Forever.
- Teselas del mapa mundial de Wowhead Forever (sin rótulos; rect en `mapas/_rects.json`):
  `ventormenta` y `orgrimmar` = rect EXACTO de la capital (1 % = 1 coordenada del **mapa de ciudad de Forever**; Ventormenta de Forever no es la de
  Classic: Georgio Bolero 53.3, 81.5 cae junto al Barrio de los Magos) · `peste_este` = rect EXACTO de la zona (el 139 de zamimg tiene el encuadre de
  Classic) · `mundo` = Kalimdor + Zephras + Reinos del Este en 16:9 (coordenada de zona → lienzo → % del recorte con `M()` de `_coords_check.py`).
- Los x, y de la tabla son **% de la imagen** = lo que va a `P(x, y, rótulo, sub, foto)` de `mapa(...)` en efectos.py. «foto» = slug de `pegatinas/`.

**Comprobación visual:** `python _coords_check.py` → `previews/_coords_check_1..12.jpg` (46 vistas: 38 mapas + 8 rutas sobre `mundo`), revisadas a mano
el 25-nov (cada punto en tierra y en su pueblo/zona; los de pesca de Azshara, en el agua de la bahía, como deben). `python _coords_check.py md` imprime la tabla.

## Qué mapa para qué escena (propuesta; ≥ 1 por parada, 2+ en las de recolección)
| Escena | Mapas |
|---|---|
| intro | `hyjal` (vetas de torio pesado, la mena nueva) |
| reglas | `durotar` / `elwynn` (entrenadores júnior Norzsh, Kelsey Fargo) |
| p01 Minería | `mundo:p01` (ruta por tramos) · `durotar`/`elwynn`/`mulgore`/`teldrassil` (1-65) · `humedales`/`argenteos`/`laderas` (65-125) · `arathi`/`mil_agujas` (125-175) · `riverglades` (133 vetas de hierro) · `interior`/`tanaris` (175-245) · `ungoro`/`frondavil`/`cuna_invierno`/`peste_este`/`estepas` (torio) · `hyjal` (torio rico y pesado) · `estepas` (Montaña Roca Negra: Latifuego) |
| p02 Herrería | `orgrimmar` (Saru) · `forjaz` (Bengus) · `alterac` (Alard, Dalaran) · `tuercespina` (Brikk) · `tanaris` (Derotain) · `baldios` + `crestagrana` + `mundo:p02` (campamentos de Favor) · `paramos` (Gilnid) · `estepas` (Argelmach) |
| p03 Ingeniería | `orgrimmar` (Roxxik) · `forjaz` (Springspindle) · `tanaris` (Buzzek) · `hyjal` (Kayleena) · `riverglades` (Kor'gar) · `cuna_invierno` (Vista Eterna) · `paramos` (Sneed) · `peste_este` (Stratholme: Ezra Grimm) |
| p04 Herboristería | `mundo:p04` (ruta) · `durotar`/`elwynn` · `argenteos`/`loch_modan` · `laderas`/`sierra_espolon` · `tuercespina`/`arathi` · `tanaris` · `interior` · `frondavil` · `hyjal` (3 hierbas nuevas) · `humedales` (Shadetooth) |
| p05 Alquimia | `mundo:p05` (Rogvar · Kylanna · Shurome) · `frondavil` (Shurome, Santuario Esmeralda) · `pantano` (Rogvar) · `feralas` (Kylanna) |
| p06 Desuello | `mundo:p06` (ruta) · `durotar`/`elwynn` · `baldios` (Fuerte del Norte) · `loch_modan`/`humedales` · `alterac` (cueva de yetis) / `laderas` / `bosque_ocaso` · `feralas` (Vega Cicatriz Feral) · `ungoro` · `riverglades` · `hyjal` |
| p07 Peletería | `mundo:p07` (Hahrana · Drakk) · `feralas` (Hahrana) · `interior` (Drakk) · `shendralas` (Jarael) |
| p08 Sastrería | `ventormenta` (Georgio Bolero) · `laderas` (Daryl Stack, Molino Tarren) · `marjal` (Timothy, Theramore) · `hyjal` (Pexmit, Kal'tinzan) · `alterac` (Charles Worth, Ciudad de Dalaran) · `shendralas` (Melanori) · `peste_este` (Stratholme: Anastari) |
| p09 Encantamiento | `mundo:p09` · `sierra_espolon` (Hgarth) · `elwynn` (Kitta, Torre de Azora) · `alterac` (Vanessa, Ciudad de Dalaran) · `inhospitas` (Uldaman: Annora) |
| p10 Cocina | `desolace` (Wulan) · `vallefresno` (Shandrina, Lago Mystral) · `tanaris` (Dirge) · `crestagrana` (Whimsyfin) · `paramos` (Cocinitas) |
| p11 Pesca | `mundo:p11` (Heming → Nat Pagle → costas) · `tuercespina` (Heming) · `marjal` (Nat Pagle) · `feralas` (Río Verdantis) · `desolace` · `vallefresno` (Brazanegra: Gelihast) · `pantano` (Templo: Jammal'an) · `azshara` (bancos) · `elwynn` (Lago de Cristal) |
| p12 Primeros auxilios | `mundo:p12` · `arathi` (Deneb, Sentencia/Victor) · `marjal` (Balai, Theramore/VanHowzen) · `hyjal` (Pexmit, Ortak) |

## Correcciones y puntos dudosos
1. **Profundidades de Roca Negra:** el pin de mazmorra de WHF (Estepas 22.6, 7.5) es el portal interior y cae en la franja de La Garganta de Fuego.
   En pantalla: el rótulo de subzona **Montaña Roca Negra 27.9, 40.2** (WHF-lugar), junto a la montaña dibujada.
2. **Templo Sumergido:** el pin (Pantano 77.3, 35.9) cae en la orilla; se usa el rótulo **70.0, 52.9** (el templo en el lago), como en wow_ruta_forever.
3. **Forjaz:** en las teselas la ciudad es solo la nieve de la montaña (está bajo tierra) → mapa de ciudad de zamimg (1537); la investigación dice que
   en las 5 capitales que no son Ventormenta el mapa coincide. Bengus cae en la Gran Fundición y Springspindle en Ciudad Manitas.
4. **Cueva de cobre de Mulgore:** la investigación da la casilla más densa (56.7, 53.4; n=33), no la boca de la cueva. MEDIA.
5. **Cueva de yetis:** Wowhead la asigna a Alterac (36.5, 85.9), en el borde con Laderas: se marca en `alterac` (y en `mundo:p06`). La voz dice
   «de Laderas de Trabalomas»: la entrada es desde Laderas, pero el mapa que la muestra es el de Alterac.
6. **Sin coordenada en la investigación:** Xizzer Fizzbolt (Cuna del Invierno: se marca Vista Eterna, MEDIA) · los vendedores de la receta de
   protección contra la naturaleza (Bronk/Logannas, Glyx) · las arpías Wormwing de Hyjal (peto bendecido) · la costa de Tuercespina, Desolace y
   el Pantano para la misión de Nat Pagle (solo el Río Verdantis tiene punto; Desolace = Aldea Cazasombras, MEDIA) · la misión del cuchillo de la
   Horda en Los Baldíos · el Bancal del Creador (Nanaya): el pin cae fuera del mapa de Un'Goro (ver `wow_errores_60/mapas/ungoro_norte.jpg`).
7. **Gadgetzan:** Derotain (51.4, 28.6), Buzzek (52.2, 27.6), Dirge (52.6, 28.0) y Pestlezugg (51.2, 27.5) caen en el mismo pueblo: un solo punto con subrótulo.

## Tabla (`python _coords_check.py md`)
| Mapa | Escena | x, y (% del mapa) | Rótulo | Subrótulo | Foto (pegatina) | Frase del guion | Tipo | Fuente | Confianza |
|---|---|---|---|---|---|---|---|---|---|
| `durotar` | reglas p01 | 40.5, 68.1 | Norzsh | entrenador júnior de minería | `norzsh` | «un entrenador júnior en cada uno» | P | INV | ALTA |
| `durotar` | p01 | 43.8, 64.7 | Vetas de cobre pobres | Valle de los Retos | `o_mena_cobre` | «vetas de cobre pobres en los valles de inicio» | R | INV | ALTA (densidad n=25) |
| `durotar` | p01 | 53.1, 25.5 | Cobre | 1-65 | `o_mena_cobre` | «Del uno al sesenta y cinco, cobre, en cualquier zona inicial» | R | INV | ALTA (n=17) |
| `durotar` | p04 | 44.3, 65.2 | Flor de paz marchita | 1-70 | `o_flor_paz` | «versiones marchitas y atrofiadas» | R | INV | ALTA (n=27) |
| `durotar` | p06 | 42.9, 23.2 | Jabalíes moteados | desuello 1-75 | `o_prof_desuello` | «jabalíes en Durotar» | R | INV | ALTA |
| `elwynn` | reglas p01 | 47.2, 32.2 | Kelsey Fargo | entrenadora júnior de minería | `kelsey_fargo` | «un entrenador júnior en cada uno» | P | INV | ALTA |
| `elwynn` | p01 | 42.0, 76.8 | Cobre | 1-65 | `o_mena_cobre` | «Del uno al sesenta y cinco, cobre» | R | INV | ALTA (n=13) |
| `elwynn` | p04 | 54.2, 44.5 | Hojaplata atrofiada | 1-70 | `o_hojaplata` | «versiones marchitas y atrofiadas» | R | INV | ALTA (n=19) |
| `elwynn` | p06 | 44.1, 71.1 | Jabalíes y lobos | desuello 1-75 | `o_prof_desuello` | «o lobos en el Bosque de Elwynn» | R | INV | ALTA |
| `elwynn` | p09 | 64.8, 70.6 | Kitta Vientofuego | encantamiento experto (A) | `kitta` | «Kitta Vientofuego, en lo alto de la Torre de Azora» | P | INV | ALTA |
| `elwynn` | p09 | 65.8, 68.1 | Torre de Azora |  | `torre_azora` | «en lo alto de la Torre de Azora» | C | WHF-lugar | ALTA |
| `elwynn` | p11 | 52.4, 62.4 | Lago de Cristal | pesca 1-75 | `o_cana_pescar` | «Todos los entrenadores de inicio están junto al agua» | R | INV | ALTA |
| `mulgore` | p01 | 56.7, 53.4 | Cueva de cobre | 5 vetas, reaparición rápida | `o_mena_cobre` | «En Mulgore hay una cueva con cinco vetas de cobre» | R | INV | MEDIA (casilla más densa n=33; la cueva exacta no tiene pin) |
| `mulgore` | p01 | 34.6, 53.2 | Excavación de Bael'dun | forja | — | «La forja más cerca está en la Excavación de Bael'dun» | C | WHF-lugar | ALTA |
| `teldrassil` | p01 | 56.9, 27.6 | Fragmentos de ámbar |  | `o_mena_cobre` | «ahora pican fragmentos de ámbar» | R | INV | ALTA (n=17) |
| `teldrassil` | p01 | 53.0, 51.1 | Fragmentos de ámbar grandes |  | `o_mena_cobre` | «ahora pican fragmentos de ámbar» | R | INV | ALTA |
| `teldrassil` | p01 | 58.2, 41.5 | Fanorran Stilloak | entrenador júnior de minería | — | «un entrenador júnior en cada uno» | P | INV | ALTA |
| `humedales` | p01 | 47.3, 62.2 | Cueva de estaño | Alianza · 65-125 | `o_mena_estano` | «La Alianza, en una cueva de Los Humedales llena de estaño» | R | INV | ALTA (14 vetas de incendicita en la casilla) |
| `humedales` | p04 | 38.5, 60.5 | Sitio de Excavación | plano del invernadero (Shadetooth) | `excavacion_humedales` | «el plano del invernadero lo suelta Shadetooth, en Los Humedales» | M | WHF | ALTA (pin de mazmorra) |
| `humedales` | p06 | 34.5, 49.7 | Excavación de Whelgar | desuello 130-150 (A) | `o_prof_desuello` | «La Alianza, a Loch Modan y luego a Los Humedales» | R | WHF-lugar | ALTA |
| `argenteos` | p01 | 58.1, 72.8 | Cueva de estaño | Horda · 65-125 | `o_mena_estano` | «la Horda, en el Bosque de Argénteos» | R | INV | ALTA (n=13) |
| `argenteos` | p04 | 54.5, 76.6 | Brezospina | 70-115 | `o_brezospina` | «marregal y brezospina en el Bosque de Argénteos» | R | INV | ALTA (n=12) |
| `argenteos` | p04 | 54.6, 27.0 | Marregal | 70-115 | `o_marregal` | «marregal y brezospina en el Bosque de Argénteos» | R | INV | ALTA |
| `laderas` | p01 | 28.3, 55.7 | Estaño | Horda · 65-125 | `o_mena_estano` | «o en Laderas de Trabalomas» | R | INV | ALTA |
| `laderas` | p04 | 36.5, 56.1 | Sangrerregia | 115-170 | `o_sangrerregia` | «Laderas de Trabalomas o Sierra Espolón» | R | INV | ALTA |
| `laderas` | p06 | 57.8, 27.4 | Osos y leones | desuello 150-160 | `o_prof_desuello` | «la cueva de yetis de Laderas de Trabalomas» | R | INV | ALTA |
| `laderas` | p08 | 63.7, 20.8 | Daryl Stack | sastrería artesano (H) | `daryl_stack` | «Daryl Stack, en el Molino Tarren de Laderas» | P | INV | ALTA |
| `laderas` | p08 | 61.5, 20.0 | Molino Tarren |  | `molino_tarren` | «en el Molino Tarren de Laderas» | C | WHF-lugar | ALTA |
| `alterac` | p06 | 36.5, 85.9 | Cueva de yetis | desuello 150-225 | `o_prof_desuello` | «la cueva de yetis de Laderas de Trabalomas» | R | INV | ALTA (Wowhead la pone en Alterac, en el borde con Laderas) |
| `alterac` | p02 | 19.7, 63.4 | Alard Schmied | herrería 1-225 (A) | — | «Alard Schmied, en Dalaran, enseña hasta el doscientos veinticinco» | P | INV | ALTA |
| `alterac` | p08 | 17.7, 60.4 | Charles Worth | sastrería 1-225 (A) | — | «la Alianza tiene además a Charles Worth en Dalaran» | P | INV | ALTA |
| `alterac` | p09 | 16.8, 62.3 | Vanessa Sellers | encantamiento 1-225 (A) | — | «La Alianza tiene además a Vanessa Sellers, en Dalaran» | P | INV | ALTA |
| `alterac` | p08 p09 | 16.7, 68.8 | Ciudad de Dalaran | rueca · recuperador arcano | `ciudad_dalaran` | «un centinela inestable, en la Ciudad de Dalaran» | M | WHF | ALTA (pin de mazmorra) |
| `arathi` | p01 | 54.4, 76.0 | Hierro | 125-175 | `o_mena_hierro` | «hierro y oro, en las Tierras Altas de Arathi» | R | INV | ALTA |
| `arathi` | p01 | 33.2, 44.7 | Hierro | 125-175 | `o_mena_hierro` | «hierro y oro, en las Tierras Altas de Arathi» | R | INV | ALTA |
| `arathi` | p01 | 84.5, 32.8 | Oro | 155-175 | `o_mena_oro` | «hierro y oro, en las Tierras Altas de Arathi» | R | INV | ALTA |
| `arathi` | p04 | 56.6, 35.1 | Mostacho de Khadgar | 170-205 | `o_mostacho_khadgar` | «la Vega de Tuercespina o Arathi» | R | INV | ALTA |
| `arathi` | p12 | 27.0, 58.8 | Deneb Camino | libro de experto (A) | `deneb` | «lo vende Deneb Camino en Arathi para la Alianza» | P | INV | ALTA |
| `arathi` | p12 | 73.4, 36.8 | Doctor Gregory Victor | Atenciones médicas (H) | `gregory_victor` | «el doctor Gregory Victor en Sentencia, en Arathi» | P | INV | ALTA |
| `arathi` | p12 | 73.9, 35.8 | Sentencia |  | — | «en Sentencia, en Arathi» | C | WHF-lugar | ALTA |
| `mil_agujas` | p01 | 12.7, 34.8 | Hierro | 125-175 | `o_mena_hierro` | «o en Las Mil Agujas» | R | INV | ALTA |
| `mil_agujas` | p01 | 43.3, 35.5 | Hierro | 125-175 | `o_mena_hierro` | «o en Las Mil Agujas» | R | INV | ALTA |
| `riverglades` | p01 | 55.5, 44.7 | Hierro: 133 vetas | la zona con más hierro | `o_mena_hierro` | «más vetas de hierro que ninguna otra zona del mapa» | R | INV | ALTA (casilla más densa) |
| `riverglades` | p01 | 77.8, 52.0 | Grungle | entrenador de minería | — | «(entrenador de la zona nueva; no lo nombra la voz)» | P | INV | ALTA |
| `riverglades` | p03 | 77.6, 50.8 | Kor'gar | esquema del tubo de torio | — | «o con Kor'gar, en Claros del Río» | P | INV | ALTA |
| `riverglades` | p06 | 65.2, 53.1 | Cuero pesado | bestias de las llanuras | `o_cuero_pesado` | «tiene bestias que dan mucho cuero pesado» | R | INV | ALTA |
| `riverglades` | p06 | 58.4, 55.6 | Cuero pesado |  | `o_cuero_pesado` | «tiene bestias que dan mucho cuero pesado» | R | INV | ALTA |
| `interior` | p01 | 56.7, 43.9 | Mitril y veraplata | 175-245 | `o_mena_mitril` | «mitril y veraplata, en Tierras del Interior» | R | INV | ALTA (n=11 de cada) |
| `interior` | p04 | 57.6, 42.6 | Champiñón fantasma | cueva · 230-270 | `o_champinon_fantasma` | «Tierras del Interior con solea y champiñón fantasma» | R | INV | ALTA (n=9) |
| `interior` | p04 | 65.4, 47.4 | Solea | 230-270 | `o_solea` | «Tierras del Interior con solea» | R | INV | ALTA |
| `interior` | p07 | 13.4, 43.3 | Drakk Stonehand | peletería artesano (A) | `drakk` | «Drakk Stonehand, en Tierras del Interior» | P | INV | ALTA |
| `tanaris` | p01 | 33.5, 44.6 | Mitril y veraplata | 175-245 | `o_mena_mitril` | «o en Tanaris» | R | INV | ALTA |
| `tanaris` | p01 | 55.1, 74.6 | Mitril y veraplata | 175-245 | `o_mena_mitril` | «o en Tanaris» | R | INV | ALTA |
| `tanaris` | p02 p03 p10 | 51.2, 27.5 | Gadgetzan | Derotain · Buzzek · Dirge | `gadgetzan` | «Buzzek Giracorchete, en Gadgetzan» | C | WHF-lugar | ALTA (Derotain 51.4, 28.6 · Buzzek 52.2, 27.6 · Dirge 52.6, 28.0: el mismo pueblo) |
| `tanaris` | p04 | 44.9, 34.7 | Flor de fuego | 205-230 | — | «Tanaris o La Garganta de Fuego» | R | INV | ALTA |
| `tanaris` | p04 | 46.9, 65.5 | Loto cárdeno | 205-230 | — | «Tanaris o La Garganta de Fuego» | R | INV | ALTA |
| `ungoro` | p01 | 67.3, 15.9 | Torio pequeño | 245-275 | `o_mena_torio` | «torio pequeño en Un'Goro» | R | INV | ALTA (n=12) |
| `ungoro` | p06 | 36.0, 35.2 | Diemetradones y pterrordáctilos | desuello 280-300 | `o_cuero_basto` | «los diemetradones y pterrordáctilos de Un'Goro» | R | INV | ALTA |
| `ungoro` | p06 | 35.5, 46.0 | Diemetradones |  | `o_cuero_basto` | «los diemetradones y pterrordáctilos de Un'Goro» | R | INV | ALTA |
| `ungoro` | p06 | 43.6, 7.2 | Refugio de los Mariscales |  | — | «(punto de partida de la guía)» | C | WHF-lugar | ALTA (referencia) |
| `frondavil` | p01 | 36.2, 54.6 | Torio pequeño | 245-275 | `o_mena_torio` | «o en Frondavil» | R | INV | ALTA |
| `frondavil` | p04 | 53.6, 14.9 | Hojasueño | 270-300 | `o_hojasueno` | «Frondavil, con hojasueño» | R | INV | ALTA |
| `frondavil` | p04 | 42.9, 43.6 | Flor de plaga | 270-300 | — | «y flor de plaga, hasta el trescientos» | R | INV | ALTA |
| `frondavil` | p04 | 44.8, 85.0 | Gromsanguina | 270-300 | — | «(no la nombra la voz)» | R | INV | ALTA |
| `frondavil` | p05 | 51.5, 82.0 | Maestro micólogo Shurome | alquimia 1-300 (los dos bandos) | `shurome` | «Shurome, en el Santuario Esmeralda de Frondavil» | P | INV | ALTA |
| `frondavil` | p05 | 50.9, 81.3 | Santuario Esmeralda |  | — | «en el Santuario Esmeralda de Frondavil» | C | WHF-lugar | ALTA |
| `cuna_invierno` | p01 | 55.9, 85.8 | Torio rico | 275-300 | `o_mena_torio` | «torio rico en Cuna del Invierno» | R | INV | ALTA (n=9) |
| `cuna_invierno` | p03 | 61.2, 38.2 | Vista Eterna | esquema del tubo de torio | — | «El esquema del tubo se compra en Cuna del Invierno» | C | WHF-lugar | MEDIA (Xizzer Fizzbolt sin coordenada: se marca el pueblo) |
| `peste_este` | p01 | 47.1, 54.6 | Torio rico | 275-300 | `o_mena_torio` | «en la Peste del Este» | R | INV | ALTA |
| `peste_este` | p03 p08 | 26.1, 10.4 | Stratholme | Ezra Grimm · Baronesa Anastari | `stratholme` | «suelta Ezra Grimm en Stratholme» | M | WHF | ALTA (pin de mazmorra) |
| `estepas` | p01 | 65.4, 35.8 | Torio rico | 275-300 | `o_mena_torio` | «o en Las Estepas Ardientes» | R | INV | ALTA |
| `estepas` | p01 p02 | 27.9, 40.2 | Montaña Roca Negra | Profundidades: Latifuego · Argelmach | `profundidades_roca_negra` | «el Embajador Latifuego, en Profundidades de Roca Negra» | M | WHF-lugar | ALTA el rótulo de subzona (el pin de mazmorra 22.6, 7.5 es el portal interior y cae en la franja de La Garganta de Fuego) |
| `hyjal` | p01 | 63.6, 86.7 | Torio rico | más de 100 vetas | `o_mena_torio` | «Monte Hyjal tiene, además, más de cien vetas de torio rico» | R | INV | ALTA (casilla densa) |
| `hyjal` | p01 | 76.3, 75.4 | Torio rico |  | `o_mena_torio` | «más de cien vetas de torio rico» | R | INV | ALTA |
| `hyjal` | intro p01 | 35.6, 83.3 | Torio pesado | la mena nueva | `o_mena_torio_pesada` | «la mena de torio pesada, en unas ciento veinte vetas» | R | INV | ALTA |
| `hyjal` | intro p01 | 35.8, 47.6 | Torio pesado |  | `o_mena_torio_pesada` | «la mena de torio pesada» | R | INV | ALTA |
| `hyjal` | intro p01 | 64.5, 86.0 | Torio pesado |  | `o_mena_torio_pesada` | «la mena de torio pesada» | R | INV | ALTA |
| `hyjal` | p03 | 60.2, 61.4 | Kayleena Encantaflores | ingeniería artesano | `kayleena` | «Kayleena Encantaflores, en Monte Hyjal» | P | INV | ALTA |
| `hyjal` | p04 | 44.3, 75.2 | Hojapesadilla | hierba nueva | `o_hojapesadilla` | «la hojapesadilla, la salvia demoníaca y el loto de la muerte» | R | INV | ALTA (n=11) |
| `hyjal` | p04 | 45.2, 86.8 | Salvia demoníaca | hierba nueva | `o_salvia_demoniaca` | «la salvia demoníaca» | R | INV | ALTA (n=13) |
| `hyjal` | p04 | 62.6, 33.8 | Salvia demoníaca |  | `o_salvia_demoniaca` | «la salvia demoníaca» | R | INV | ALTA |
| `hyjal` | p06 | 74.3, 36.6 | Cuero basto |  | `o_cuero_basto` | «Y en Monte Hyjal, cuero basto» | R | INV | ALTA |
| `hyjal` | p08 p12 | 48.2, 33.6 | Pexmit | difícil de encontrar | `pexmit` | «Lo vende Pexmit, en Monte Hyjal» | P | INV | ALTA (pin de PNJ raro) |
| `hyjal` | p12 | 13.0, 52.8 | Ortak Lomgok | Flora Antigua (H) | `ortak` | «una misión de Ortak Lomgok, en Flora Antigua» | P | INV | ALTA |
| `hyjal` | p08 | 13.6, 53.0 | Kal'tinzan | misión de los puños (H) | — | «o la Horda lo saca con una misión» | P | INV | ALTA |
| `tuercespina` | p02 | 29.0, 75.4 | Brikk Finoficio | herrería artesano | `brikk` | «Brikk Finoficio, en Bahía del Botín, a los dos bandos» | P | INV | ALTA |
| `tuercespina` | p11 | 27.4, 77.0 | Viejo Heming | libro de pesca de experto | `viejo_heming` | «un libro que vende el Viejo Heming, en Bahía del Botín» | P | INV | ALTA |
| `tuercespina` | p04 | 35.1, 15.2 | Mostacho de Khadgar | 170-205 | `o_mostacho_khadgar` | «la Vega de Tuercespina» | R | INV | ALTA (n=14) |
| `tuercespina` | p04 | 45.7, 35.9 | Espina de oro | 170-205 | — | «pálida, espina de oro y mostacho de Khadgar» | R | INV | ALTA |
| `baldios` | p02 | 49.8, 29.4 | Campamento de Favor (H) | Logística y suministros de Durotar | `o_cajon_arrebatado` | «La Horda lo tiene al oeste de El Cruce, en Los Baldíos» | C | INV | ALTA (vendedores 49.4-49.8, 28.8-30.0) |
| `baldios` | p02 | 52.1, 30.6 | El Cruce |  | — | «al oeste de El Cruce» | C | WHF-lugar | ALTA (referencia) |
| `baldios` | p06 | 61.2, 54.7 | Fuerte del Norte | raptores: desuello 75-150 (H) | `o_prof_desuello` | «a los raptores y zancudos al oeste de Fuerte del Norte» | R | INV | ALTA |
| `baldios` | p06 | 60.2, 33.8 | Zhevras y zancudos |  | `o_prof_desuello` | «a los raptores y zancudos» | R | INV | ALTA |
| `crestagrana` | p02 | 10.8, 72.4 | Campamento de Favor (A) | Autoridad Comercial de Azeroth | `o_cajon_arrebatado` | «la Alianza en Tres Caminos, al oeste de Crestagrana» | C | INV | ALTA (Nina Fuegocertero; vendedores 8.4-11.2, 71.0-74.6) |
| `crestagrana` | p10 | 67.1, 69.9 | Whimsyfin | pez nuevo (27 bancos) | `o_whimsyfin` | «el Whimsyfin, que solo se pesca en Crestagrana» | R | INV | ALTA (mediana de 27 bancos) |
| `orgrimmar` | p02 | 82.3, 23.0 | Saru Steelfury | herrería experto | `saru_steelfury` | «Saru Steelfury en Orgrimmar» | P | INV | ALTA |
| `orgrimmar` | p03 | 76.0, 25.1 | Roxxik | ingeniería experto | `roxxik` | «con Roxxik en Orgrimmar» | P | INV | ALTA |
| `forjaz` | p02 | 52.4, 41.2 | Bengus Deepforge | herrería experto | `bengus_deepforge` | «o Bengus Deepforge en Forjaz» | P | INV | ALTA |
| `forjaz` | p03 | 68.5, 43.5 | Springspindle | ingeniería experto | `springspindle` | «o con Springspindle en Forjaz» | P | INV | ALTA |
| `ventormenta` | p08 | 53.3, 81.5 | Georgio Bolero | sastrería experto | `georgio_bolero` | «Georgio Bolero en Ventormenta» | P | INV | ALTA (mapa de ciudad de Forever; WP-TR y WHF coinciden) |
| `feralas` | p05 | 32.6, 43.8 | Kylanna | alquimia artesano (A) | `kylanna` | «y Kylanna, en Feralas, para la Alianza» | P | INV | ALTA |
| `feralas` | p05 | 31.1, 44.6 | Bastión Plumaluna |  | — | «» | C | WHF-lugar | ALTA (referencia) |
| `feralas` | p06 | 54.6, 56.5 | Vega Cicatriz Feral | yetis: desuello 225-280 | `o_cuero_grueso` | «los yetis de la Vega Cicatriz Feral, en Feralas» | R | WHF-lugar | ALTA |
| `feralas` | p07 | 74.4, 43.1 | Hahrana Pielférrea | peletería artesano (H) | `hahrana` | «Hahrana Pielférrea, en Feralas, para la Horda» | P | INV | ALTA |
| `feralas` | p07 | 75.2, 43.8 | Campamento Mojache |  | — | «» | C | WHF-lugar | ALTA (referencia) |
| `feralas` | p11 | 63.2, 52.2 | Río Verdantis | Ahi de Feralas | — | «y el Río Verdantis, en Feralas» | R | INV | ALTA |
| `pantano` | p05 | 48.5, 55.8 | Rogvar | alquimia artesano (H) | `rogvar` | «Rogvar, en el Pantano de las Penas, para la Horda» | P | INV | ALTA |
| `pantano` | p11 | 70.0, 52.9 | Templo de Atal'Hakkar | cabaña de pesca (Jammal'an) | `templo_sumergido` | «el profeta Jammal'an, en el Templo Sumergido» | M | WHF-lugar | ALTA el rótulo (el pin de mazmorra 77.3, 35.9 cae en la orilla) |
| `sierra_espolon` | p09 | 49.2, 57.2 | Hgarth | encantamiento experto (H) | `hgarth` | «Hgarth, en un risco sobre el Refugio Roca del Sol» | P | INV | ALTA |
| `sierra_espolon` | p09 | 47.8, 60.8 | Refugio Roca del Sol |  | `refugio_roca_sol` | «sobre el Refugio Roca del Sol» | C | WHF-lugar | ALTA |
| `sierra_espolon` | p04 | 35.0, 64.2 | Hierba cardenal | 115-170 | — | «Laderas de Trabalomas o Sierra Espolón» | R | INV | ALTA |
| `inhospitas` | p09 | 44.2, 12.2 | Uldaman | Annora: encantamiento artesano | `annora` | «solo lo enseña Annora, en Uldaman» | M | WHF-lugar | ALTA (rótulo de Uldaman; Annora en la entrada trasera) |
| `desolace` | p10 | 26.2, 69.8 | Wulan | libro de cocina de experto (H) | `wulan` | «Wulan en Aldea Cazasombras, en Desolace» | P | INV | ALTA |
| `desolace` | p10 p11 | 25.3, 70.4 | Aldea Cazasombras |  | — | «en Aldea Cazasombras» | C | WHF-lugar | ALTA |
| `vallefresno` | p10 | 49.4, 67.0 | Shandrina | libro de cocina de experto (A) | `shandrina` | «Shandrina en el Lago Mystral, en Vallefresno» | P | INV | ALTA |
| `vallefresno` | p10 | 51.7, 73.4 | Lago Mystral |  | — | «en el Lago Mystral» | C | WHF-lugar | ALTA |
| `vallefresno` | p11 | 16.5, 11.0 | Cavernas de Brazanegra | expositor de pesca (Gelihast) | `brazanegra` | «Gelihast, en las Cavernas de Brazanegra» | M | WHF | ALTA (pin de mazmorra) |
| `marjal` | p11 | 58.4, 60.0 | Nat Pagle | pesca artesano | `nat_pagle` | «la misión de Nat Pagle, en el Marjal» | P | INV | ALTA |
| `marjal` | p08 | 66.2, 51.8 | Timothy Worthington | sastrería artesano (A) | `timothy_worthington` | «Timothy Worthington, en Theramore» | P | INV | ALTA |
| `marjal` | p12 | 67.6, 48.8 | Doctor Gustaf VanHowzen | Atenciones médicas (A) | `vanhowzen` | «el doctor Gustaf VanHowzen, en Theramore» | P | INV | ALTA |
| `marjal` | p08 p12 | 65.0, 47.1 | Theramore |  | — | «en Theramore» | C | WHF-lugar | ALTA |
| `marjal` | p12 | 36.4, 30.4 | Balai Lok'Wein | libro de experto (H) | `balai` | «Balai Lok'Wein en el Marjal para la Horda» | P | INV | ALTA |
| `azshara` | p11 | 58.3, 56.3 | Almeja bocazas | 226 bancos | `o_almeja_bocazas` | «más de trescientos cincuenta bancos de almejas bocazas y de langostas» | R | INV | ALTA (mediana) |
| `azshara` | p11 | 61.4, 57.4 | Langosta garraoscura | 132 bancos | `o_langosta_garraoscura` | «y de langostas» | R | INV | ALTA (mediana) |
| `shendralas` | p07 | 42.6, 78.1 | Jarael | peletería 1-225 | — | «o Jarael en Shen'dralas» | P | INV | ALTA |
| `shendralas` | p08 | 43.4, 77.8 | Melanori | sastrería 1-225 | — | «y en Shen'dralas está Melanori» | P | INV | ALTA |
| `loch_modan` | p06 | 63.2, 40.8 | Cocodrilos, osos y jabalíes | desuello 75-130 (A) | `o_prof_desuello` | «La Alianza, a Loch Modan» | R | INV | ALTA |
| `loch_modan` | p04 | 65.5, 42.9 | Brezospina | 70-115 | `o_brezospina` | «o en Loch Modan» | R | INV | ALTA |
| `bosque_ocaso` | p06 | 62.8, 68.2 | Huargos Nightbane | desuello 150-225 | `o_prof_desuello` | «O los huargos del Bosque del Ocaso» | R | INV | ALTA |
| `bosque_ocaso` | p06 | 64.6, 35.6 | Huargos Nightbane |  | `o_prof_desuello` | «O los huargos del Bosque del Ocaso» | R | INV | ALTA |
| `paramos` | p02 p03 p10 | 38.2, 77.5 | Las Minas de la Muerte | Gilnid · Sneed · Cocinitas | `minas_muerte` | «lo suelta Gilnid, en Las Minas de la Muerte» | M | WHF | ALTA (pin de mazmorra) |
| `mundo:p01` | p01 | 34.3, 44.1 | Durotar | cobre 1-65 (H) | `o_mena_cobre` | «Del uno al sesenta y cinco, cobre» | R | INV | ALTA |
| `mundo:p01` | p01 | 71.8, 77.3 | Elwynn | cobre 1-65 (A) | `o_mena_cobre` | «Del uno al sesenta y cinco, cobre» | R | INV | ALTA |
| `mundo:p01` | p01 | 77.1, 54.4 | Los Humedales | estaño 65-125 (A) | `o_mena_estano` | «una cueva de Los Humedales llena de estaño» | R | INV | ALTA |
| `mundo:p01` | p01 | 69.7, 40.7 | Argénteos | estaño 65-125 (H) | `o_mena_estano` | «en el Bosque de Argénteos» | R | INV | ALTA |
| `mundo:p01` | p01 | 78.2, 47.0 | Arathi | hierro y oro 125-175 | `o_mena_hierro` | «en las Tierras Altas de Arathi» | R | INV | ALTA |
| `mundo:p01` | p01 | 29.0, 67.2 | Las Mil Agujas | hierro 125-175 | `o_mena_hierro` | «o en Las Mil Agujas» | R | INV | ALTA |
| `mundo:p01` | p01 | 82.1, 70.3 | Claros del Río | 133 vetas de hierro | `o_mena_hierro` | «más vetas de hierro que ninguna otra zona» | R | INV | ALTA |
| `mundo:p01` | p01 | 80.2, 38.0 | Tierras del Interior | mitril 175-245 | `o_mena_mitril` | «en Tierras del Interior» | R | INV | ALTA |
| `mundo:p01` | p01 | 29.4, 78.7 | Tanaris | mitril 175-245 | `o_mena_mitril` | «o en Tanaris» | R | INV | ALTA |
| `mundo:p01` | p01 | 28.1, 72.5 | Un'Goro | torio 245-300 | `o_mena_torio` | «torio pequeño en Un'Goro» | R | INV | ALTA |
| `mundo:p01` | p01 | 30.7, 30.8 | Monte Hyjal | torio rico y pesado | `o_mena_torio_pesada` | «Monte Hyjal tiene, además, más de cien vetas de torio rico» | R | INV | ALTA |
| `mundo:p04` | p04 | 33.3, 49.6 | Durotar | 1-70 | `o_flor_paz` | «flor de paz y hojaplata en cualquier zona inicial» | R | INV | ALTA |
| `mundo:p04` | p04 | 72.7, 74.4 | Elwynn | 1-70 | `o_hojaplata` | «flor de paz y hojaplata» | R | INV | ALTA |
| `mundo:p04` | p04 | 69.4, 41.2 | Argénteos | 70-115 | `o_brezospina` | «en el Bosque de Argénteos» | R | INV | ALTA |
| `mundo:p04` | p04 | 72.2, 42.4 | Laderas | 115-170 | `o_sangrerregia` | «Laderas de Trabalomas» | R | INV | ALTA |
| `mundo:p04` | p04 | 72.0, 85.5 | Tuercespina | 170-205 | `o_mostacho_khadgar` | «la Vega de Tuercespina» | R | INV | ALTA |
| `mundo:p04` | p04 | 31.4, 82.4 | Tanaris | 205-230 | — | «Tanaris o La Garganta de Fuego» | R | INV | ALTA |
| `mundo:p04` | p04 | 80.3, 37.8 | Tierras del Interior | 230-270 | `o_champinon_fantasma` | «Tierras del Interior» | R | INV | ALTA |
| `mundo:p04` | p04 | 27.0, 22.0 | Frondavil | 270-300 | `o_hojasueno` | «y Frondavil» | R | INV | ALTA |
| `mundo:p04` | p04 | 29.2, 29.8 | Monte Hyjal | 3 hierbas nuevas | `o_hojapesadilla` | «en Monte Hyjal hay tres hierbas nuevas» | R | INV | ALTA |
| `mundo:p06` | p06 | 33.1, 43.8 | Durotar | 1-75 (H) | `o_prof_desuello` | «jabalíes en Durotar» | R | INV | ALTA |
| `mundo:p06` | p06 | 72.0, 76.8 | Elwynn | 1-75 (A) | `o_prof_desuello` | «lobos en el Bosque de Elwynn» | R | INV | ALTA |
| `mundo:p06` | p06 | 31.7, 55.8 | Los Baldíos | 75-150 (H) | `o_prof_desuello` | «la Horda va a Los Baldíos» | R | INV | ALTA |
| `mundo:p06` | p06 | 80.2, 59.8 | Loch Modan | 75-130 (A) | `o_prof_desuello` | «La Alianza, a Loch Modan» | R | INV | ALTA |
| `mundo:p06` | p06 | 76.0, 53.1 | Los Humedales | 130-150 (A) | `o_prof_desuello` | «y luego a Los Humedales» | R | INV | ALTA |
| `mundo:p06` | p06 | 72.5, 39.7 | Cueva de yetis | 150-225 | `o_prof_desuello` | «la cueva de yetis de Laderas de Trabalomas» | R | INV | ALTA |
| `mundo:p06` | p06 | 20.2, 67.2 | Vega Cicatriz Feral | 225-280 | `o_cuero_grueso` | «los yetis de la Vega Cicatriz Feral» | R | INV | ALTA |
| `mundo:p06` | p06 | 25.6, 74.4 | Un'Goro | 280-300 | `o_cuero_basto` | «los diemetradones y pterrordáctilos de Un'Goro» | R | INV | ALTA |
| `mundo:p02` | p02 | 29.2, 49.1 | Campamento de Favor (H) | Los Baldíos | `o_cajon_arrebatado` | «al oeste de El Cruce, en Los Baldíos» | C | INV | ALTA |
| `mundo:p02` | p02 | 76.2, 77.0 | Campamento de Favor (A) | Tres Caminos | `o_cajon_arrebatado` | «la Alianza en Tres Caminos» | C | INV | ALTA |
| `mundo:p02` | p02 | 71.1, 95.6 | Brikk Finoficio | herrería artesano | `brikk` | «Brikk Finoficio, en Bahía del Botín» | P | INV | ALTA |
| `mundo:p02` | p02 | 32.1, 75.8 | Derotain Sorbelodo | piezas imperiales | `derotain` | «en Tanaris, Derotain Sorbelodo» | P | INV | ALTA |
| `mundo:p05` | p05 | 79.3, 80.3 | Rogvar | artesano (H) | `rogvar` | «Rogvar, en el Pantano de las Penas» | P | INV | ALTA |
| `mundo:p05` | p05 | 16.8, 64.8 | Kylanna | artesano (A) | `kylanna` | «Kylanna, en Feralas» | P | INV | ALTA |
| `mundo:p05` | p05 | 26.7, 32.0 | Shurome | 1-300, los dos bandos | `shurome` | «Shurome, en el Santuario Esmeralda de Frondavil» | P | INV | ALTA |
| `mundo:p07` | p07 | 23.2, 64.7 | Hahrana Pielférrea | artesano (H) | `hahrana` | «Hahrana Pielférrea, en Feralas» | P | INV | ALTA |
| `mundo:p07` | p07 | 76.6, 37.9 | Drakk Stonehand | artesano (A) | `drakk` | «Drakk Stonehand, en Tierras del Interior» | P | INV | ALTA |
| `mundo:p09` | p09 | 22.0, 43.5 | Hgarth | experto (H) | `hgarth` | «Hgarth, en Sierra Espolón» | P | INV | ALTA |
| `mundo:p09` | p09 | 73.5, 76.8 | Kitta Vientofuego | experto (A) | `kitta` | «Kitta Vientofuego, en la Torre de Azora» | P | INV | ALTA |
| `mundo:p09` | p09 | 79.0, 63.1 | Annora · Uldaman | artesano | `annora` | «solo lo enseña Annora, en Uldaman» | M | WHF-lugar | ALTA |
| `mundo:p11` | p11 | 70.9, 95.8 | Viejo Heming | Bahía del Botín | `viejo_heming` | «el Viejo Heming, en Bahía del Botín» | P | INV | ALTA |
| `mundo:p11` | p11 | 32.7, 63.8 | Nat Pagle | Marjal | `nat_pagle` | «la misión de Nat Pagle, en el Marjal» | P | INV | ALTA |
| `mundo:p11` | p11 | 21.5, 66.4 | Río Verdantis | Feralas | — | «y el Río Verdantis, en Feralas» | R | INV | ALTA |
| `mundo:p11` | p11 | 17.0, 54.1 | Costa de Desolace | Aldea Cazasombras | — | «Desolace» | R | WHF-lugar | MEDIA (la guía no da el punto de la costa: se marca el pueblo) |
| `mundo:p12` | p12 | 79.7, 43.2 | Sentencia | Doctor Gregory Victor (H) | `gregory_victor` | «el doctor Gregory Victor en Sentencia» | C | WHF-lugar | ALTA |
| `mundo:p12` | p12 | 33.5, 62.1 | Theramore | Doctor Gustaf VanHowzen (A) | `vanhowzen` | «el doctor Gustaf VanHowzen, en Theramore» | C | WHF-lugar | ALTA |
| `mundo:p12` | p12 | 29.5, 26.0 | Pexmit | Monte Hyjal | `pexmit` | «El manual lo vende Pexmit, en Monte Hyjal» | P | INV | ALTA |
