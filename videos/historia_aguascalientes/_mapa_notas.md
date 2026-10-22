# Mapa de Aguascalientes (mapa.py, 22-oct-2026)
- Caja (rejilla "mx", Mercator): lon -104.20..-100.10, lat 23.05..20.85 (Jerez/Juchipila → SLP, Zacatecas → León/Silao). Ancha a
  propósito: con z 0,74 cabe casi toda en 16:9 (con la caja pedida, 2,4°, el zoom mínimo dejaba fuera Zacatecas o Lagos).
- 640 px/° → FW×FH = 2624×1518. Encuadres: caja entera z 0,74 · estado entero z 1,7-1,8 (con margen 1,5) · región del estado 2,5-3,5
  · capital z 4-6,5 (más allá se ablanda: la rejilla es de ~160 m/px).
- `core.ZREF = 1.7` se conserva: en Jalisco (260 px/°) z 1,7 era «la región protagonista llenando la pantalla»; aquí z 1,7 es el estado
  entero con margen → mismo tamaño relativo de pegatinas. De cerca crecen (z/1,7)^0,3 (z 6 → ×1,46).
- Umbrales de escenas.fondo (líneas 76 y 172, `(cam.z - 1.8) / 2.7`): NO los toqué (escenas.py es de otro). Recomendado
  `(cam.z - 2.2) / 3.3` para que el estado a z 1,5-2,2 conserve el color pleno y se aclare al entrar a la capital (z 5,5).
- Relieve: sombreado y valles con AWS Terrain Tiles (Terrarium z10 ≈ 140 m, `datos/relieve_ags_terrarium_z10.npz`, datos abiertos);
  ríos y Presa Calles con SRTM15+ (ERDDAP `srtm15plus`, `datos/relieve_ags_srtm15.nc`). Altitud en color desde 1 500 m (`ALT_BASE`).
- Ríos calculados del relieve (relleno + D8 + acumulación, cuencas cerradas > 10 m y > 80 km² = sumidero): San Pedro-Verde, Chicalote,
  Juchipila, Calvillo, Santiago-Pabellón... Natural Earth no trae nada útil aquí. Presa Calles = relieve inundado (75 celdas de 15").
- Estados: Natural Earth 10 m (`datos/estados_mx.geojson`, copiado de historia_jalisco). Ags solo toca Zacatecas y Jalisco (correcto).
## Claves
- CIUDADES: aguascalientes, plaza_patria, san_marcos, encino, estacion, ojocaliente, cerro_muerto (cumbre 2 380 m), el_ocote*,
  real_asientos, calvillo, san_jose_gracia, presa_calles, cristo_roto, rincon_romos, pabellon_hidalgo, pabellon_arteaga, jesus_maria,
  san_francisco_romo, tepezala, cosio, el_llano, cienega_grande, bocas_gallardo*, palmillas*, zacatecas, guadalupe_zac, jerez,
  lagos_moreno, encarnacion, teocaltiche, juchipila, ojuelos, san_luis_potosi, leon, silao, san_juan_lagos; en el BORDE (para flechas):
  guadalajara, ciudad_mexico, queretaro (la real en `*_real`). (* = sitio aproximado, sin coordenada fiable)
- RUTAS: camino_plata y tren (recortadas a la caja desde `RUTAS_COMPLETAS`: México→Querétaro→León→Lagos→Ags→Zacatecas), ruta_turista
  (Plaza de la Patria→Calvillo→San José de Gracia→Pabellón de Hidalgo→Real de Asientos), paseo_capital, santa_anna (Zacatecas→Ags).
- Campos: aguascalientes (= territorio = edo_aguascalientes), edo_zacatecas, edo_jalisco, edo_san_luis_potosi, edo_guanajuato,
  resto_mx, mexico_mod, guachichiles, guamares, zacatecos, caxcanes, tecuexes, chichimecas (los 5), nueva_galicia, nueva_espana,
  zacatecas_dep (Ags + Zac), insurgentes, metro, valle, presa_calles, tierra. Colores en `M.COL[clave]`. Celdas: municipios (11), pueblos.

## Ver / rehacer (desde esta carpeta; ojo: run.sh apunta a historia_jalisco)
- `PYTHONPATH="C:\FabricaAnimaciones\videos\historia_aguascalientes;C:\FabricaAnimaciones\nucleo" python mapa.py` (≈ 12 s)
- igual con `python _mapa_test.py [--puntos]` → previews/mapa_t1_caja.jpg, mapa_t2_estado.jpg, mapa_t3_capital.jpg,
  mapa_t4_chichimecas.jpg y la hoja previews/mapa_test.jpg (`--puntos` dibuja ciudades y rutas para comprobar posiciones).
