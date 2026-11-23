# Coordenadas y mapas â€” wow_errores_60 (22-nov-2026; modelo: wow_ruta_forever/_coords.md)

**Fuentes de las coordenadas:** WHF = mapa mundial de **Wowhead Forever** (`nether.wowhead.com/forever/data/world-map`, leÃ­do el 22-nov:
pines de PNJ, mazmorra y banda); WHF-lugar = rÃ³tulo de subzona del mismo archivo (campo `places`) pasado a % de la zona con el `rect` de la
zona; INV = `videos/_investigacion_wow_errores_60.md` (guÃ­as de Forever, sobre todo Conquest Capped).

**Mapas** (`mapas/`, origen en `mapas/_fuentes.txt`, se rehacen con `python _mapas.py [nombreâ€¦]`):
- Zona (1 % de la imagen = 1 de coordenada): `estepas` (46), `marjal` (15), `cuna_invierno` (618), `azshara` (16), `ungoro` (490), `tanaris` (440)
  = `wow.zamimg.com/images/wow/classicplus/maps/eses/original/<id>.jpg` (Forever en Wowhead). `hyjal` = `File:WorldMap-Hyjal-forever.jpg`
  de warcraft.wiki.gg (el 616 de zamimg es un borrador).
- Teselas del mapa mundial de Wowhead Forever (sin rÃ³tulos; rect del lienzo en `mapas/_rects.json`; coordenada de zona â†’ lienzo â†’ % del recorte):
  `ungoro_norte` (Un'Goro + 22 % al norte), `peste_forever` (Peste del Oeste + del Este), `cavernas_puertas` (Hyjal + Cuna + norte de Azshara),
  `kalimdor_bandas` (norte/este de Kalimdor 16:9), `mundo_bandas` (mundo entero 16:9).
- Los x, y de la tabla son **% de la imagen** = lo que va a `P(x, y, rÃ³tulo, sub, foto)` de `mapa(...)` en efectos.py.

**ComprobaciÃ³n visual:** `python _coords_check.py` â†’ `previews/_coords_check_1..3.jpg`, revisadas a mano el 22-nov.

## QuÃ© mapa para quÃ© escena (propuesta)
| Escena | Mapa | Puntos |
|---|---|---|
| c23 Â· c10 Â· c09 | `marjal` | Guarida de Onyxia (+ Theramore / Murohelecho de referencia) |
| c21 | `marjal` | Islas Lanza Negra: **sin coordenada** (ver dudas) â†’ solo la costa del Marjal |
| c18 | `hyjal` (o `cavernas_puertas`) | vuelo Fayran â†’ Cima de la Eternidad â†’ portal de la Cima Hyjal |
| c17 | `cavernas_puertas` (+ `hyjal`, `azshara`) | puerta de Hyjal Â· puerta del BastiÃ³n Faucenegra Â· Cuna del Invierno (zona) |
| c16 Â· c12 | `azshara` | Valormok / Punta Talrendis â†’ Ruinas de Eldarath â†’ Ursolan â†’ BastiÃ³n (piedra de encuentro, portal) |
| c15 | `ungoro_norte` | Refugio de los Mariscales / Gryfe â†’ Bancal del Creador (pin WHF, la estructura al norte del crÃ¡ter) |
| c11 Â· c04 | `estepas` + `marjal` | Cumbre de Roca Negra Â· Brasaliza (CiÃ©naga de Fuego) |
| c08 | `kalimdor_bandas` | Cima Hyjal Â· Cavernas (Hyjal y BastiÃ³n) Â· Guarida de Onyxia |
| c06 | `hyjal` | Tiala Â· Rhylin Espinapiedra Â· Cima de la Eternidad |
| c05 | `peste_forever` | Stratholme Â· Scholomance |
| c01 | `mundo_bandas` (+ `tanaris`, `peste_forever`, `estepas`) | Forjaz/Orgrimmar â†’ Mux â†’ Stratholme â†’ La Masacre â†’ Bodley â†’ Asharell â†’ Cumbre |

## Correcciones y puntos dudosos
1. **Cima Hyjal y Cavernas del TÃºmulo:** WHF tiene **un solo pin genÃ©rico** para las dos bandas (Hyjal 58.4, 57.1, cerca del Santuario de
   Aviana). Se usan las de la investigaciÃ³n: portal de la Cima **~85, 33** y entrada de las Cavernas **~70, 62** (MEDIA: Â«segÃºn los archivosÂ»).
   En el mapa caen en las montaÃ±as al este de la Cima de la Eternidad y al sureste del Santuario: plausible, sin comprobar en el cliente.
2. **Bancal del Creador:** la guÃ­a da 48.1, 6.1 de Un'Goro (en el mapa de zamimg cae en el borde de arriba, junto al Refugio); el **pin de
   mazmorra de WHF** cae 8,8 % **por encima** del mapa de Un'Goro (Mil Agujas 17.8, 60.8). En `ungoro_norte` el pin cae justo sobre la
   estructura titÃ¡nica al norte del crÃ¡ter â†’ usar el pin; 48.1, 6.1 parece el inicio de la subida desde el Refugio.
3. **BastiÃ³n Faucenegra:** guÃ­a 38.4, 32.6 (piedra de encuentro) y 35.0, 23.4 (portal); el rÃ³tulo WHF es 39.6, 32.3. En `cuna_invierno` el
   rÃ³tulo cae fuera de la zona dibujada (esquina sureste, 70.0, 90.5).
4. **Cuna del Invierno como tercera puerta de las Cavernas:** ninguna fuente da la coordenada â†’ se marca la ZONA (Vista Eterna), rÃ³tulo
   Â«puerta sin coordenadaÂ». No ponerla como puerta exacta.
5. **Ejecutor Asharell** (~74, 66 de Las Estepas): solo la guÃ­a; WHF no tiene pin. MEDIA.
6. **Islas Lanza Negra:** ni WHF ni la wiki dan su ubicaciÃ³n (la pÃ¡gina del campo de batalla no tiene geografÃ­a). No hay punto.
7. **Pix Xizzix** estÃ¡ en BahÃ­a del BotÃ­n segÃºn WHF (Tuercespina 28.4, 75.8), no en Minahonda como decÃ­a la investigaciÃ³n (el guion no dice dÃ³nde).

## Tabla (`python _coords_check.py md`)
| Mapa | Escena | Punto | Tipo | x, y (% del mapa) | Fuente | Confianza |
|---|---|---|---|---|---|---|
| `estepas` | c11 c04 | Cumbre de Roca Negra (entrada) | M | 33.0, 25.2 | WHF | ALTA (pin de mazmorra) |
| `estepas` | c01 | Bodley (fantasma, cadena 0.5) | P | 32.2, 25.8 | WHF | ALTA |
| `estepas` | c01 | Ejecutor Asharell (~74, 66) | P | 74.0, 66.0 | INV | MEDIA (guía; «sur de Las Estepas»; sin pin en WHF) |
| `estepas` | c01 | Vigilia de Morgan | C | 85.9, 67.6 | WHF-lugar | ALTA (referencia) |
| `marjal` | c23 c10 c09 c08 | Guarida de Onyxia | M | 52.9, 77.7 | WHF | ALTA (pin de banda) |
| `marjal` | c04 | Brasaliza (Ciénaga de Fuego) | P | 56.6, 87.6 | WHF | ALTA |
| `marjal` | c21 c08 | Isla Theramore | C | 65.0, 47.1 | WHF-lugar | ALTA (referencia) |
| `marjal` | c21 c08 | Poblado Murohelecho | C | 36.3, 31.4 | WHF-lugar | ALTA (referencia) |
| `hyjal` | c18 c06 | Cima de la Eternidad | R | 78.5, 36.9 | WHF-lugar | ALTA |
| `hyjal` | c18 | vuelo (Fayran Elthas) | C | 68.6, 44.0 | WHF | ALTA |
| `hyjal` | c06 | Tiala Melenablanca | P | 68.8, 50.4 | WHF | ALTA |
| `hyjal` | c06 | Rhylin Espinapiedra (intendente) | P | 70.6, 51.2 | WHF | ALTA |
| `hyjal` | c18 c08 | portal de la Cima Hyjal (~85, 33) | M | 85.0, 33.0 | INV | MEDIA (investigación; WHF no tiene pin propio) |
| `hyjal` | c17 c08 | Cavernas del Túmulo, entrada (~70, 62) | M | 70.0, 62.0 | INV | MEDIA (investigación «según los archivos») |
| `hyjal` | — | pin WHF de las 2 bandas (genérico) | P | 58.4, 57.1 | WHF | BAJA: el mismo pin para Cima y Cavernas; NO usar en pantalla |
| `hyjal` | c18 | Laderas Maculadas | R | 59.3, 74.3 | WHF-lugar | ALTA (referencia) |
| `cuna_invierno` | c17 | Vista Eterna | C | 61.2, 38.2 | WHF-lugar | ALTA |
| `cuna_invierno` | c17 | Garganta Negro Rumor (a Hyjal) | R | 58.2, 85.6 | WHF-lugar | ALTA |
| `cuna_invierno` | c17 c16 | Bastión Faucenegra (lado de Cuna) | M | 70.0, 90.5 | WHF-lugar | ALTA (rótulo de subzona) |
| `azshara` | c16 c12 c17 | Bastión Faucenegra: piedra de encuentro | M | 38.4, 32.6 | INV | ALTA (guía; WHF 39.6, 32.3) |
| `azshara` | c17 c16 | Bastión Faucenegra: portal | M | 35.0, 23.4 | INV | ALTA (guía; junto a Cuna del Invierno) |
| `azshara` | c16 | Valormok (vuelo H) | C | 21.8, 50.0 | WHF-lugar | ALTA |
| `azshara` | c16 | Punta Talrendis (vuelo A) | C | 11.7, 77.9 | WHF-lugar | ALTA |
| `azshara` | c16 | Ursolan | R | 47.5, 26.4 | WHF-lugar | ALTA |
| `azshara` | c16 | Ruinas de Eldarath | R | 33.6, 56.9 | WHF-lugar | ALTA |
| `ungoro` | c15 | Refugio de los Mariscales | C | 43.6, 7.2 | WHF-lugar | ALTA |
| `ungoro` | c15 | vuelo (Gryfe) | C | 45.2, 5.8 | WHF | ALTA |
| `ungoro` | c15 | Bancal del Creador (guía) | M | 48.1, 6.1 | INV | MEDIA: guía 48.1, 6.1; el pin WHF cae 8,8 % por ENCIMA del mapa |
| `ungoro_norte` | c15 | Refugio de los Mariscales | C | 43.6, 23.9 | WHF-lugar | ALTA |
| `ungoro_norte` | c15 | vuelo (Gryfe) | C | 45.2, 22.8 | WHF | ALTA |
| `ungoro_norte` | c15 | Bancal del Creador (guía 48.1, 6.1) | M | 48.1, 23.0 | INV | MEDIA |
| `ungoro_norte` | c15 | Bancal del Creador (pin WHF) | M | 47.3, 10.8 | WHF | ALTA el dato (pin de mazmorra) |
| `tanaris` | c01 | Mux Malamaná (Gadgetzan) | P | 52.4, 27.2 | WHF | ALTA |
| `tanaris` | c01 | Gadgetzan | C | 51.2, 27.5 | WHF-lugar | ALTA |
| `peste_forever` | c05 c01 | Stratholme (entrada) | M | 56.7, 24.1 | WHF | ALTA (pin) |
| `peste_forever` | c01 | Anthion Harmon | P | 53.9, 21.2 | WHF | ALTA |
| `peste_forever` | c05 c01 | Scholomance (entrada) | M | 44.4, 79.7 | WHF | ALTA (pin) |
| `peste_forever` | c05 c01 | Castel Darrow | R | 44.3, 81.2 | WHF-lugar | ALTA |
| `peste_forever` | c01 | Capilla Esperanza de la Luz (Alba Argenta) | C | 86.2, 53.2 | WHF-lugar | ALTA |
| `kalimdor_bandas` | c17 c08 | Cavernas del Túmulo · puerta de Hyjal | M | 51.2, 28.5 | INV | MEDIA |
| `kalimdor_bandas` | c18 c08 | Cima Hyjal | M | 53.1, 24.1 | INV | MEDIA |
| `kalimdor_bandas` | c17 c08 | Cavernas · puerta del Bastión Faucenegra | M | 57.6, 30.7 | INV | ALTA |
| `kalimdor_bandas` | c17 c08 | Cuna del Invierno (puerta sin coordenada) | R | 56.1, 16.2 | WHF-lugar | BAJA: marca la ZONA (Vista Eterna), no la puerta |
| `kalimdor_bandas` | c08 c23 | Guarida de Onyxia | M | 52.7, 92.7 | WHF | ALTA (pin) |
| `cavernas_puertas` | c17 | Cavernas · puerta del Monte Hyjal (~70, 62) | M | 36.1, 64.2 | INV | MEDIA |
| `cavernas_puertas` | c17 | Cavernas · puerta del Bastión Faucenegra | M | 57.8, 71.5 | INV | ALTA |
| `cavernas_puertas` | c17 c16 | Bastión Faucenegra (entrada) | M | 60.0, 78.6 | INV | ALTA |
| `cavernas_puertas` | c17 | Cuna del Invierno · Vista Eterna (puerta sin coordenada) | R | 52.8, 22.0 | WHF-lugar | BAJA: zona, no puerta |
| `cavernas_puertas` | c18 | Cima Hyjal (~85, 33) | M | 42.7, 49.0 | INV | MEDIA |
| `cavernas_puertas` | c18 c06 | Cima de la Eternidad | R | 39.8, 51.0 | WHF-lugar | ALTA |
| `mundo_bandas` | c01 | Forjaz · Deliana (A) | P | 72.4, 67.7 | WHF | ALTA |
| `mundo_bandas` | c01 | Orgrimmar · Mokvar (H) | P | 29.5, 48.9 | WHF | ALTA |
| `mundo_bandas` | c01 | Tanaris · Mux | P | 28.7, 85.6 | WHF | ALTA |
| `mundo_bandas` | c01 | Stratholme | M | 77.7, 34.2 | WHF | ALTA |
| `mundo_bandas` | c01 | La Masacre | M | 17.4, 72.5 | WHF | ALTA |
| `mundo_bandas` | c01 | Roca Negra · Bodley | P | 72.7, 78.6 | WHF | ALTA |
| `mundo_bandas` | c01 | Estepas · Ejecutor Asharell | P | 75.5, 81.8 | INV | MEDIA |
| `mundo_bandas` | c01 | Cumbre superior · Valthalak | M | 72.8, 78.6 | WHF | ALTA (pin de Cumbre de Roca Negra) |
