# Fotos reales (FotoPeg) — historia_aguascalientes
`foto_peg.FotoPeg` = foto impresa con marco de papel cálido, 2 cintas, inclinación, sombra y crédito (de `creditos.json`). Misma interfaz que `pegflow.Peg` (pies en x, y; s = 1 → 400 px de alto TOTAL); va sobre el mapa y bajo crayón/tinta (rótulos encima).
```python
import foto_peg as FP
t0 = T("convencion", "El teatro sigue en pie")
pa(R, FP.F("convencion_9"), 1340, 930, FP.s_para(0.48), t0, t0 + 4.5, entra="pluma")   # «pluma» (u 0→1) = caída «pegar»; «pop» también vale
```
- Tamaño: `FP.s_para(f)` da la s para ocupar la fracción f del alto: 0,40 → s 1,08; 0,48 → 1,30; 0,55 → 1,49. Retratos (3:4) 0,50-0,55; paisajes (4:3) 0,42-0,48.
- Duración: ~4-5 s en pantalla. Entrada: `u` 0→1 (cae girando, la sombra aterriza, las cintas llegan al final). Salida: `u` 1→0 o `s`→0 con `sq` (pop).
- Opciones: `incl` (grados; por defecto ±1,6-3,2 según la clave), `calido` (0,35; 0 = color original), `cinta`, `credito` (texto propio). `rot` se suma a la inclinación; `flip` se ignora.
- `fondo` se modifica en sitio al componer (pegflow): en escenas.py ya es nuevo cada cuadro; en pruebas pasa `fondo.copy()`.
- Coste: ~0,2 s la primera vez por tamaño, ~0,05 s por variante de temblor, luego caché.
- Recortes: `recortes.json` ([cx, cy, alto, aspecto]) → `python foto_peg.py recortar [claves]` rehace `<clave>_rec.jpg`. Prueba: `_prueba_fotos.py` → `previews/fotos_prueba_*.jpg`.

## Claves (22, todas libres: CC BY / CC BY-SA / dominio público; detalle en creditos.json)
origenes_1 (El Ocote, recorte a los venados), origenes_7, colonia_1, colonia_3, colonia_5, aguas_4, feria_2, feria_3, beso_0, posada_0, posada_3 (recorte a la Catrina con el título), posada_6, porfiriato_3, porfiriato_5, porfiriato_8, porfiriato_9 (recorte al cuadro, sin marco), convencion_1, convencion_6, convencion_8, convencion_9, siglo20_3, siglo20_6.

**Sustituciones:** `colonia_1` → `Fachada_de_la_Catedral_de_Aguascalientes_01.jpg` (Luisalvaz, CC BY 4.0; la de guion.py era el interior) · `siglo20_3` → `El_Cristo_Roto,_San_José_de_Gracias,_Aguascalientes,_Ags..jpg` (Luisalvaz, CC BY-SA 3.0; la de guion.py era la placa). Hay que actualizar esas 2 entradas de `FOTOS` en guion.py (no lo toqué).
Fuentes pequeñas: posada_0 (370×500), convencion_6 (700×466), convencion_8 (500×325): úsalas a ≤ 0,45 del alto.
