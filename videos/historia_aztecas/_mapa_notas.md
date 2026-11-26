# Mapa de los aztecas (mapa.py, 23-nov-2026)
- **Dos rejillas Mercator, una sola cámara.** `"mx"` (la del kit): lon -103.00..-91.80, lat 22.00..14.30 (del Bajío/Michoacán al
  Soconusco, del Golfo al Pacífico), **300 px/° → FW×FH = 3360×2433**. `"cuenca"` (solo fondo + campos de la isla): lon -99.45..-98.45,
  lat 19.95..18.95 (Valle de México con Popocatépetl e Iztaccíhuatl), **2000 px/° → 2000×2121**. `pintar_base` funde la fina encima
  cuando la cámara se acerca (entra de z 1,6 a 2,4, con fundido en su borde): lago, isla y cerros nítidos hasta z ≈ 50.
  Por qué no una sola: el imperio con el Soconusco a 2000 px/° serían 22 400 px de ancho; a 480-640 px/° no cabe el Soconusco y la
  isla se ablanda igual. Con dos rejillas: ~360 MB de arreglos por proceso (+~50 MB con tepanecas/acolhuas) → con 12 procesos ≈ 5-6 GB.
  Si falta RAM, bajar a 8 procesos. `R.ubic.region` (mapa vectorial de `nucleo/crono_ubicacion.py`) ya no hace falta para el imperio.
- **Encuadres** (z = px de pantalla por px de "mx"; `Cam(lon, lat, z)`):
  caja entera = imperio 1519 con el Soconusco **z 0,575** (-97.40, 18.15) · imperio sin Soconusco z 0,8 (-97.70, 17.90) ·
  expansión/centro z 1,0-1,1 (-98.40, 18.70) · **centro de México / ruta de Cortés z 1,4-1,6** (-97.85, 19.32) · Tlaxcala-Cholula-volcanes
  z 3-4 (-98.45, 19.20) · **Valle entero con los 5 lagos z 6-6,5** (-99.02, 19.48) · isla con Chapultepec/Tlacopan/Tepeyac z 14-18
  (-99.14, 19.43) · **isla de cerca z 35-50** (-99.135, 19.435); más allá de ~60 se ablanda el relieve (el contorno sigue nítido).
- **`core.ZREF = 1.7` se conserva**: z 1,7 = 510 px/° ≈ el centro de México llenando la pantalla (Jalisco: 442 px/° a z 1,7).
- **Umbrales de `escenas.fondo`** (líneas 100 y 198, `(cam.z - 2.2) / 3.3`; NO los toqué): recomendado **`(cam.z - 3.0) / 7.0`** →
  territorios plenos en el centro de México (z ≤ 3), a media tinta en el Valle (z 6,5: alfa 0,63) y solo un tinte en la isla (z ≥ 10).
  Ruta (`R.ruta`): el ancho crece con (z/2,5)^0,6 → en la isla (z 40) usar `ancho` ~1/4 del normal.
- **Relieve**: AWS Terrain Tiles Terrarium z9 (≈ 300 m, con batimetría: el mar se oscurece con la profundidad;
  `datos/relieve_azt_terrarium_z9.npz`) y z12 para la cuenca (≈ 38 m, `datos/relieve_valle_terrarium_z12.npz`). Color por altitud:
  costa clara → altiplano 2 200 m ocre medio → sierras ocre → nieve desde ~4 000 m (Popo, Izta, Orizaba, Nevado de Toluca).
  Valles verdes (`campo valle`): cuenca, Puebla-Tlaxcala, Toluca, Morelos, Oaxaca, Pátzcuaro-Cuitzeo y llanura del Golfo (fondo de
  valle del relieve; de muy cerca, z > 10, se retira). Ríos: Natural Earth 10 m (Balsas, Lerma, Papaloapan, Moctezuma, Atoyac;
  peso 8,6-9,4) + los 26 ríos que bajan a los lagos del mapa de Sémhur (peso 7,0: se ven de z ≈ 2,7).
- **Lagos de 1519 = AGUA en las dos rejillas** (aunque hoy sean ciudad; el agua manda sobre el relieve) + Pátzcuaro y Cuitzeo
  (Natural Earth, solo `featurecla = Lake`: las presas modernas NO). Isla de Tenochtitlan-Tlatelolco = tierra. Calzadas y albarradón
  NO están en el fondo: `M.pintar_calzadas(img, cam, claves=(...), alfa, u=0..1)` (bandas claras con tinta + estacas del albarradón),
  p. ej. `R.fondo.append(("mx", lambda img, cam, t, fs: M.pintar_calzadas(img, cam, alfa=...)))`; o como rutas `R.RUTAS[...]`.
  Rótulos de los lagos: `M.LAGOS_ROT` («LAGO DE TEXCOCO»...: px 22-26 a z 6; a px 30 se pisan Xochimilco y Chalco).
- **Comprobado** (`./run.sh _mapa_test.py --puntos` → previews/mapa_t1_caja … t6_etapas.jpg y la hoja previews/mapa_test.jpg):
  Tenochtitlan en la isla dentro del lago, Chapultepec y Tlacopan en la orilla oeste, Texcoco en la orilla este, Iztapalapa y Culhuacán
  en la orilla sur, Xaltocan en su isla; el lago calza con la llanura < 2 245 m del relieve. Tlaxcala, Huexotzinco y Cholula caen
  dentro del enclave `tlaxcala`; Teotitlán en `teotitlan`; Tzintzuntzan en `purepecha`; Taxco, Tuxpan y Cuilápam en `imperio_1519`.

## Claves
- **CIUDADES** (lon, lat; `*` = aproximado): tenochtitlan (= templo_mayor = ciudad_mexico), tlatelolco, chapultepec, azcapotzalco,
  tlacopan, texcoco, culhuacan, tizapan*, iztapalapa, mexicaltzingo, xoloc*, coyoacan, xochimilco, chalco, tlahuac, ayotzingo, xaltocan,
  zumpango, citlaltepec, cuautitlan, tepotzotlan, los_remedios, tepeyac, tenayuca, atzacoalco, ecatepec, chimalhuacan*, coatlinchan,
  huexotla, acolman, teotihuacan, otumba, tula, amecameca, tlalmanalco, popocatepetl, iztaccihuatl, paso_cortes, tlaxcala, tizatlan,
  cholula, huexotzinco, hueyotlipan*, huamantla*, ixtacamaxtitlan*, zautla*, perote*, xico*, xalapa, cempoala, quiahuiztlan, villa_rica,
  veracruz, tepeaca, tehuacan, tzintzuntzan, cuauhnahuac, malinalco, toluca, xilotepec, huaxtepec, oaxaca, coyolapan, tochtepec,
  tochpan, cuetlaxtlan, tlachco, tlapan, teotitlan, metztitlan*, tututepec*, acapulco, tehuantepec*, soconusco*, **aztlan_flecha***
  (borde norte de la rejilla al NO de Tula: Aztlán es mítico, es solo el arranque de la flecha).
- **RUTAS**: migracion (aztlan_flecha → Tula → Tenayuca → Azcapotzalco → Chapultepec → Culhuacán → Tizapán → Tenochtitlan),
  cortes_ida (Villa Rica → Cempoala → Xalapa → Xico → Perote → Zautla → Ixtacamaxtitlan → Huamantla/Tecoac → Tlaxcala → Cholula →
  Paso de Cortés → Amecameca → Ayotzingo → Cuitláhuac → Iztapalapa → calzada → Tenochtitlan), noche_triste (calzada de Tlacopan →
  Los Remedios → Cuautitlán → Tepotzotlán → Citlaltepec → Zumpango → norte de los lagos → Teotihuacan → Otumba → Hueyotlipan →
  Tlaxcala), comercio_pochteca (Tenochtitlan → Chalco → Cholula → Tepeaca → Tehuacán → Tochtepec → Tehuantepec → Soconusco),
  calzada_tepeyac, calzada_tlacopan, calzada_iztapalapa (Tenochtitlan → Xoloc → Mexicaltzingo → Iztapalapa), calzada_coyoacan,
  calzada_tlahuac_n / _s, albarradon (Atzacoalco → Iztapalapa).
- **Campos "mx"** (`M.CAMPOS`, color `M.COL[clave]`): tierra, valle, lagos_1519, mexico_mod, edo_cdmx, imperio_1440, imperio_1469,
  imperio_1481, imperio_1486, imperio_1502, imperio_1519 (todas incluyen la isla), tlaxcala, teotitlan, yopitzinco, purepecha
  — **FALTAN tepanecas, acolhuas e imperio_1428** (ver Fuentes); mientras, el alias triple_alianza → imperio_1440. Alias: imperio/mexicas/territorio → imperio_1519, triple_alianza → imperio_1428, lagos → lagos_1519, isla → isla_1519.
- **Campos "cuenca"** (otro tamaño; `Cam.proyectar` los reconoce; un `Territorio` NO puede fundir uno de "cuenca" con uno de "mx"):
  isla_1519 (Tenochtitlan + Tlatelolco), isla_1325 (Tenochtitlan 1325-1377, 10 km²), islote_1325 (islote del Templo Mayor, 5 km²),
  islote_tlatelolco (1,5 km²), agua_isla_1325 (agua que tapa lo que la isla aún no era: capa de agua en `CAPAS_AGUA` que se encoge a
  None hacia 1519 = la isla crece), lagos_cuenca. Celdas (`R.romper`): triple_alianza (3), cuenca (18 altepetl), provincias (21 cabeceras).
- **Ubicación**: `UBICACION = {"prota": "MX-DIF", ...}` (clave de la CDMX en `nucleo/crono_ubicacion.py`: **MX-DIF**, no MX-CMX).

## Fuentes (todo en `datos/fuentes/`: scripts + descargas en `crudo/`)
- Lagos, islotes, calzadas, albarradón, ríos de la cuenca y rótulos: **«Basin of Mexico 1519 map-en.svg»** (Wikimedia Commons, Sémhur,
  CC BY-SA 4.0; de Niederberger 1987 *Paléo-paysages et archéologie pré-urbaine du Bassin de Mexico* y Coe, Snow & Benson 1986
  *Atlas of Ancient America*). Vectores leídos del SVG (`svgmini.py`) y georreferenciados con sus 26 pueblos + las islas de Xaltocan y
  Tláhuac: afín (error medio 1,7 km) + lámina delgada (error < 0,1 km); Ecatepec, Acolman e Ixtapaluca están a 5-7 km en el mapa y
  no deforman (`cuenca.py`). Comparado con OpenHistoricalMap (lagos ≤ 1635): misma forma, la orilla este de OHM queda 3-8 km al oeste
  de Texcoco; la de Sémhur calza con la llanura del relieve.
- Isla de 1519 y de 1325: **OpenHistoricalMap** (CC0), relaciones 2856555 «Mexico-Tenochtitlan 1473-1521» (parte de la isla) y
  2856558 «1325-1377». Islotes de 1325 y Tlatelolco: agujeros del lago de Sémhur (esquemáticos).
- Imperio 1519, enclaves de Tlaxcala, Teotitlan y Yopitzinco: **«Aztec Empire 1519 map-fr.svg»** (Commons, Sémhur/Yavidaxiu, CC BY-SA
  3.0; del *Atlas del México prehispánico*, Arqueología Mexicana 2000). Georreferenciado por su costa contra Natural Earth y corregido
  tierra adentro con 23 cabeceras (el mapa las pone 20-50 km al este: lámina delgada con la costa fija) (`georef_mapas.py`, `corregir.py`).
- Etapas 1440-1502 (conquistas de Itzcóatl, Moctezuma I, Axayácatl, Tízoc, Ahuízotl): **«Aztecexpansion.png»** (Commons, Maunus,
  dominio público), igual (costa + 5 lugares), acumuladas y recortadas al imperio de 1519 para que crezcan anidadas.
- Purépecha 1519: **«Michhuahcān 1519.svg»** (Commons, Yavidaxiu / Ricardo gs, CC BY-SA 3.0), georreferenciado por la costa (±10-20 km).
- **PENDIENTE: tepanecas (~1420), acolhuas e imperio_1428.** La fuente elegida es «Tepanecapan.png» (Commons, Akapochtli / El
  Comandante, CC BY-SA 3.0: territorio tepaneca original, fases 1222-1283 y 1283-1414 y lo añadido tras someter a los acolhuas de
  Texcoco en 1418), pero Wikimedia devolvió 429 (límite de descargas, 23-nov 15:17-15:36 UTC) y no quise dibujarlos a ojo. Para
  hacerlos: bajar el PNG, georreferenciarlo como los otros (`georef_mapas.py`: costa no sirve aquí → con los pueblos que marque y la
  lámina delgada de `cuenca.py`), exportar las claves tepanecas/acolhuas/imperio_1428 a `aztecas_territorios.geojson` y `./run.sh mapa.py`
  (mapa.py ya las lee si existen; COL ya tiene sus colores).
- Coordenadas: artículos de Wikipedia es/en (API `prop=coordinates`) y OpenStreetMap/Nominatim (barrios, pueblos y cabeceras); listas
  en `datos/fuentes/crudo/`. Relieve: AWS Terrain Tiles (Terrarium; Mapzen, datos abiertos). Costa, estados, lagos y ríos: Natural Earth 10 m.

## Ver / rehacer (desde esta carpeta)
- `./run.sh mapa.py` (≈ 20 s; lee datos/aztecas_*.geojson/json y los Terrarium → datos/campos_mx.npz)
- `./run.sh _mapa_test.py [--puntos] [--solo t3_valle,t4_isla]` → previews/mapa_t1_caja, t2_centro, t3_valle, t4_isla, t5_imperio,
  t6_etapas.jpg y la hoja previews/mapa_test.jpg (~0,2-0,3 s por cuadro).
- Rehacer las fuentes: `datos/fuentes/` (`cuenca.py` → `georef_mapas.py` → `corregir.py` con `DATOS_AZT=<datos>`; ver cabecera de cada uno).
