# La historia de Egipto en 5 minutos — ESTADO
- canal: cronopapel · v2 SUBIDA y PROGRAMADA jue 22-oct-2026 14:00 CDMX (R1LQTkRiwzI; publishAt 2026-10-22T20:00:00Z, verificado en YouTube el 17-oct); la v1 (3V_C7ZEj5is) la borra el usuario en Studio
- estilo: boceto + guache con mapa → docs/estilo_boceto_guache_mapa.md (§ Versión 2 y § Versión 2.1 = este video)
- etapa: v2 rehecha entera en lo visual (11/12-oct-2026); voz: 2 frases corregidas; render y subida en curso (ver «siguiente»)
- siguiente: esperar la publicación del 22-oct; al aprobar: `python fab.py historia_egipto limpiar`.

## Qué se corrigió (pedido del usuario: «tiene errores… muy pobre en elementos»)
- v1 (1-oct): mapa sin relieve con un Egipto en forma de «plátano», territorios de bordes rectos (rectángulos sobre el Levante), contornos
  descolocados, rótulos encimados y cortados, franjas vacías a los lados del cuadro y tramos largos con el mapa solo.
- v2: kit v2 de `historia_espana` con una rejilla "eg" (Mercator, lon 18-50, lat 8-42, 60 px/°): relieve NOAA ETOPO1, valle verde del Nilo,
  ríos reales de Natural Earth (Nilo, brazos de Rosetta y Damieta, Éufrates, Tigris, Jordán), lagos, el lago Nasser que se llena en 1970,
  ~40 territorios históricos (Alto/Bajo Egipto, hicsos, Reino Nuevo hasta el Éufrates, hititas, Kush, Asiria, Persia, Alejandro, Ptolomeos,
  Roma, Bizancio, califato, fatimíes, ayubíes y cruzados, mamelucos y mongoles, otomanos, Francia, Mehmet Alí, protectorado, Egipto actual).
- ~150 dibujos nuevos (obj_eg1-3): 60 personajes de todas las épocas, dioses con cabeza animal, monumentos, carros, barcos, animales.
- 14 sellos con emblemas egipcios (corona doble, pirámide, anj, ojo de Horus, Atón, cartucho, disco alado, faro, laurel, minarete,
  castillo, espadas, ancla, águila). Sin «pop» en cada pegatina: 190 SFX variados.
- Datos de la narración corregidos (voz regenerada solo en esas dos frases, CER 0): la República se proclamó en **1953** (no 1952) y los
  jeroglíficos callaron **casi mil quinientos años** (394 → 1822), no «mil».

## Archivos clave
- `guion.py` (guion, fuentes, LYRIA) · `mapa.py` (`python mapa.py` recalcula `datos/campos_eg.npz`; relieve en `datos/relieve_eg_etopo1.nc`)
- `core.py` / `reg.py` / `escenas.py` / `trans.py` / `sellos.py` / `coreo_util.py` (kit v2; aquí `BIG=320`, territorios translúcidos de cerca)
- `coreo_1.py` (gancho → hicsos) · `coreo_2.py` (Reino Nuevo → persas) · `coreo_3.py` (Alejandro → mamelucos) · `coreo_4.py` (Napoleón → cierre + transiciones)
- `obj_eg1.py` personajes y tocados · `obj_eg2.py` monumentos, objetos, dioses · `obj_eg3.py` animales, carros, barcos · `_v1/` = código de la v1
- Pruebas: `./run.sh _prueba.py t1 t2 …` · `./run.sh _hojas.py 3 1.5` · `./run.sh _qa_choques.py 0.25` · `./run.sh _hoja_dib.py obj_eg1` · `./run.sh _mapa_test.py`
- Audio: `audio/musica.wav` = Lyria (respaldo `musica_lyria_respaldo.wav`). **No correr `fab.py … musica`** (la reemplaza por música procedural):
  tras cambiar la coreografía basta `sfx` + `mezcla`.

## Lecciones
- Anclas `T()` por PREFIJO: «corona» casaba con «coronan» (Ptolomeo se coronaba 15 s antes); «cinco» con «ciento cinco». Usa `frase=`.
- Franjas finas (el valle ±0,5°) no «crecían» con `BIG=1600` de España: aparecían de golpe al final → `BIG=320`.
- De cerca (z > 4) el territorio opaco tapaba el paisaje: alfa y contorno bajan con el zoom (escenas.fondo).
- Rótulos de mapa girados se recortaban (salían letras sueltas): `mapa._mascara_rot` agranda el lienzo antes de girar.
- Pela (40,8° N) está a 1,2° del borde de la rejilla: en vistas amplias queda fuera; para verla hay que acercar la cámara.
- Ríos del desierto: los calculados del relieve (D8) inventan uadis; aquí se usan los de Natural Earth.

_Comprobar archivos reales: `python fab.py estado historia_egipto`. Historial completo del proyecto: `docs/historial.md`._
