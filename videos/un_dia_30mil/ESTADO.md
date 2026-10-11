# Un día en la vida hace 30.000 años — ESTADO
- canal: sapiens_con_wifi · **PROGRAMADO mié 14-oct-2026 14:00 CDMX** (https://youtu.be/MADQ6aemfZY; publishAt 2026-10-14T20:00:00Z, privado hasta la fecha, miniatura POR CÓDIGO `sobrevivir` y .srt)
- estilo: doodle → docs/flujo_produccion.md
- etapa: subido y programado el 6-oct. MASTER 3:30 (383 MB), CER 0,0000, −14,00 LUFS, desfase 0 ms; revisado con hojas de contacto (un cuadro cada 3 s) + blackdetect/freezedetect sin hallazgos; un parche por tramo (`--rehacer 102-109`: los cazadores de «unos cazan» reaparecían cruzando la pantalla en el cambio de fase)
- miniatura: **por código** `salida/*_mini_sobrevivir.jpg` (`miniaturas.py`; el usuario pidió cambiar la de Flow por la de código el 6-oct para que el canal se vea uniforme; aplicada con `yt aplicar`, publishAt intacto). Quedan sin usar las de Flow `_mini_ia_2.jpg` / `_mini_ia_1.jpg` (proyecto https://flow.google.com/project/aa72fd6d-82fc-43e5-9548-90c84b1ccc7b) y la de código `dia`
- siguiente: abrir una vez los enlaces de las fuentes de la descripción (PNAS, Nature, UNESCO: escritos de memoria; si alguno falla, corregir `youtube.json` y `python fab.py yt aplicar un_dia_30mil sapiens_con_wifi MADQ6aemfZY`); ver retención a las 48 h; al aprobar: `python fab.py un_dia_30mil limpiar` (segmentos, 374 MB)

## Lecciones (6-oct, revisión de las hojas de prueba antes del render)
- Las hojas con tiempos ABSOLUTOS (`escena caza 69 72 75 …`) destaparon: cuadros vacíos de 1-3 s al entrar a la fase B (el primer dibujo esperaba a una palabra tardía → ahora algo entra en `self.C + 0.1`), rótulos encimados, huesos a escala 1.4-1.6 cruzando toda la pantalla, personajes montados (arco de 6 personas con 170 px de separación) y uno dibujado dentro de la fogata.
- Los paneos de salida eran `-1500 px`: todo lo que estaba en x > 1500 se quedaba asomando en la fase siguiente. Ahora `-2400`.
- `D.hombre_leon`: origen en los pies, ~620 px de alto a escala 1 → con escala 1.7 la cabeza se sale del cuadro. `D.hueso` mide 560 px a escala 1. `D.estarcido` usa `capa=0` (queda DEBAJO de lo dibujado; pasar `capa=1`).
- Chauvet: la narración dice «leones, caballos y rinocerontes» y se dibujaban rino/caballo/bisonte → se añadió `tipo="leon"` a `animal()`.
- En fase A, la barra de dato+fuente ocupa y≈150-255: los rótulos van de y ≥ 320.

## Notas
- `_tl_prov.py` + `_hoja_b.py` permiten revisar las escenas antes de tener la voz.

_Comprobar archivos reales: `python fab.py estado un_dia_30mil`. Historial completo del proyecto: `docs/historial.md`._
