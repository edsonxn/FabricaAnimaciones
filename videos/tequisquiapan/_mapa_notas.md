# Mapa de Tequisquiapan (mapa.py, VERTICAL 1080x1920, 22-oct-2026)
- Caja (rejilla "mx", Mercator): lon -101.05..-98.85, lat 22.45..19.05 (Celaya → Tula/Zimapán; sur de SLP/Río Verde → CDMX y
  Toluca). Más ALTA que ancha (≈ 0,6:1) para la pantalla vertical, con ~90 px de margen de cámara a los lados en la toma entera.
- 700 px/° → FW×FH = 1540×2546 (≈ 4 Mpx, como Ags). Relieve a ≈ 159 m/px de rejilla (= Terrarium z10, ≈ 143 m).
- Zoom mínimo sin salir de la caja: z 0,754. Encuadres probados (lon, lat, z):
  · caja entera (-99.95, 20.76, 0,77) · estado de Querétaro entero (-99.81, 20.80, 0,98-1,0; a 1,02 ya roza los bordes E/O)
  · estado + protagonista (centro/sur) 1,3-1,7 · Sierra Gorda (-99.62, 21.05, 1,9) · zona Tequis-San Juan-Bernal (-99.92, 20.57, 3,2;
  rango 2,5-4) · pueblo de Tequisquiapan (-99.889, 20.53, 5-7). A z 7-8 el relieve se ablanda (rejilla ≈ 159 m): aguanta bien
  hasta z ≈ 6; más cerca, que manden las pegatinas/fotos. Para el pueblo de verdad (3 km) haría falta z ≈ 50: no es trabajo del mapa.
- `core.ZREF` recomendado = 1,0 (aquí z 1,0 = el estado entero llenando el ancho, el mismo papel que z 1,7 en Ags). De cerca las
  pegatinas crecen (z/1,0)^0,3: zona z 3,2 → ×1,42; pueblo z 6 → ×1,71 (tope ×2).
- Umbral recomendado en escenas.fondo (líneas con `(cam.z - 2.2) / 3.3`): `(cam.z - 1.8) / 3.7` → el estado (z ≤ 1,8) conserva
  el color pleno, la zona (z 3,2) queda a medio aclarar y el pueblo (z ≥ 5,5) ya es casi solo paisaje.
- Relieve: AWS Terrain Tiles Terrarium z10 (`datos/relieve_qro_terrarium_z10.npz`, 96 teselas en `datos/_teselas_z10/`) para el
  sombreado, los valles, la presa Zimapán y los RÍOS; SRTM15+ (ERDDAP `srtm15plus`, `datos/relieve_qro_srtm15.nc`) solo de respaldo.
  Color de altitud desde `ALT_BASE` 1 150 m, rango 2 400 m (cañones de la Sierra Gorda = tierra baja; altiplano medio; > 2 900 m blanco:
  Nevado de Toluca y cumbres de la Sierra Gorda). Terrarium trae unos px negativos en la Huasteca: se recorta a 0.
- Ríos calculados del relieve (relleno + D8 + acumulación) sobre el Terrarium remuestreado a 7,5" (`RIO_PASO`): con las celdas de
  15" del SRTM15+ el cañón del San Juan quedaba tapado y el río salía hacia Ezequiel Montes. Las «cuencas» hondas (> 30 m,
  `RIO_SUMIDERO_MAX`) son cañones tapados, no sumideros. Resultado: San Juan de San Juan del Río → presa Centenario → Tequis → ENE
  hacia Zimapán; Moctezuma, Tula, Santa María, Extoraz, Lerma, Laja, Querétaro... Natural Earth solo trae Lerma/Moctezuma/Verde.
- Presas: Zimapán = Terrarium inundado hasta 1 570 m (superficie que vio el SRTM) desde una semilla, caja (-99.80..-99.44, 20.45..20.70);
  Centenario = polígono de INEGI (al SO del pueblo, ≈ 3,8 km); Solís y Tepuxtepec (Lerma) = lagos de Natural Earth.
- Municipio de Tequisquiapan, su zona urbana, la presa Centenario y el tramo de vía junto al pueblo: digitalizados del
  «Compendio de información geográfica municipal 2010» de INEGI (PDF 22017; mapa georreferenciado con sus 4 cruces; ≈ 374 km²,
  INEGI dice 3,16 % del estado ✓; copia del mapa en `previews/_inegi_mun.png`). El borde E se recorta a la raya de Natural Earth.
- Estados: Natural Earth 10 m (`datos/estados_mx.geojson`). La CDMX cabe en la caja (abajo a la derecha).

## Claves
- CIUDADES: tequisquiapan, plaza_tequis, centro_geografico*, presa_centenario, bordo_blanco, san_nicolas, la_fuente, fuentezuelas,
  rio_san_juan (punto para rotular), san_juan_rio, ezequiel_montes, bernal, pena_bernal (la roca; cumbre del relieve), cadereyta,
  colon, pedro_escobedo, queretaro, corregidora, la_canada, cerro_campanas, huimilpan, amealco, toliman, penamiller, san_joaquin,
  pinal_amoles, jalpan, landa, arroyo_seco, sierra_gorda / semidesierto (puntos para rotular), presa_zimapan; vecinos: celaya, apaseo,
  san_miguel_allende, huichapan, tula, zimapan, ixmiquilpan, aculco, polotitlan, jilotepec, toluca, acambaro, rio_verde, xichu;
  mexico = mexico_real = ciudad_mexico (DENTRO de la caja), mexico_borde (borde SE, para flechas que salen de cuadro). (* = aprox.)
- RUTAS: camino_real (México → Cuautitlán → Huehuetoca → Tepeji → Aculco → San Juan del Río → Querétaro → Apaseo → Celaya → borde O),
  tren (México → Tula → Nopala → pasa al S de Tequis y por San Nicolás [INEGI] → San Juan del Río → Querétaro → Celaya; fuera del
  municipio, aprox.), ruta_turista (San Juan del Río → Tequis → Ezequiel Montes → Bernal), tequis_sjr, tequis_bernal,
  ruta_queso_vino (SJR → Tequis → Ezequiel Montes → Cadereyta → Bernal → Colón), ruta_sierra (Ezequiel Montes → Cadereyta →
  Pinal de Amoles → Jalpan).
- Campos: edo_queretaro (= territorio = queretaro_edo), edo_guanajuato, edo_hidalgo, edo_mexico, edo_cdmx, edo_san_luis_potosi
  (= edo_slp), edo_michoacan, resto_mx, mexico_mod, nueva_espana (= todo México), municipio_tequis (INEGI), mancha_tequis (INEGI),
  metro (zona metropolitana de Querétaro, aprox.), valle, sierra_gorda*, semidesierto*, otomies*, chichimecas* (= pames + jonaces +
  norte), pames*, jonaces*, purepechas*, mexicas*, insurgentes* (Bajío 1810), presas (toda el agua), presa_zimapan,
  presa_centenario, tierra. Colores en `M.COL[clave]`. (* = zona aproximada a mano; los pueblos tiemblan con el mismo `AMP_PUEBLOS`
  para que sus rayas compartidas coincidan.)
- Celdas: municipios (18, centros APROXIMADOS → Voronoi, no son los límites oficiales; orden en el comentario de `CELDAS_SEMILLAS`),
  regiones (4: Sierra Gorda, Semidesierto, Valles, Sur), pueblos (6, genéricas).

## Ver / rehacer (desde esta carpeta)
- Relieve (una vez, datos abiertos sin clave): `python _bajar_relieve.py` (Terrarium z10 + SRTM15+, ≈ 12 MB).
- Campos: `./run.sh mapa.py` (bash) o `$env:PYTHONPATH="C:\FabricaAnimaciones\videos\tequisquiapan;C:\FabricaAnimaciones\nucleo"; python mapa.py`
  (≈ 20 s) → `datos/campos_mx.npz`.
- Prueba: `./run.sh _mapa_test.py [--puntos]` → previews/mapa_t1_caja, t2_estado, t3_zona, t4_pueblo, t5_pueblos, t6_sierra
  (`_puntos` con ciudades y rutas) y las hojas previews/mapa_test.jpg / mapa_test_puntos.jpg. Fuerza FORMATO vertical aunque
  guion.py aún no lo diga, y solo usa mapa.py.
- OJO: mapa.py toma W/H de `motor`, que los saca de `guion.FORMATO`: el guion.py de este video DEBE decir `FORMATO = "vertical"`.
