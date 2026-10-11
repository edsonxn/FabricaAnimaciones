# La historia de España en 5 minutos — ESTADO
- canal: cronopapel · **PROGRAMADO mié 7-oct-2026 14:00 CDMX** (eSMFJWNy5IA; publishAt 2026-10-07T20:00:00Z, privado hasta la fecha, miniatura por código y .srt)
- estilo: boceto + guache con mapa → docs/estilo_boceto_guache_mapa.md (este video es el ejemplo v2: relieve real, dos rejillas, capas, fronteras reales)
- etapa: subido y programado (6-oct-2026). MASTER 312,87 s, CER medio 0,23 %, −14 LUFS, audio sin desfase; revisado con la vista cada 3 s sobre el MASTER.
- 6-oct: terminado el re-render por tramos que se cayó el 4-oct por memoria (faltaban 7 segmentos) y corregidos 4 choques hallados al revisar: Napoleón encimado con soldados y José (3:39), Goya sobre un madrileño (3:42), visigodos apilados en Toledo (1:10), rótulo de Covadonga cruzando a Pelayo (1:49), Isabel II sobre el título «Un siglo de caos» (4:02).
- video YouTube: https://youtu.be/eSMFJWNy5IA
- siguiente: ver retención a las 48 h; si el usuario quiere, cambiar la miniatura por la de IA (`prompt_miniatura.md`) con `python fab.py yt aplicar historia_espana cronopapel eSMFJWNy5IA`; al aprobar: `python fab.py historia_espana limpiar`.
- miniatura: `miniaturas.py` (fondo = hoja `hf` del propio video sin pegatinas + personajes grandes + texto Impact) → `python fab.py historia_espana miniatura`; la elegida se copia a `salida/historia_espana_mini_final.jpg`.

## Archivos clave
- `guion.py` (guion, fuentes, LYRIA), `mapa.py` (dos rejillas Mercator: "eu" con relieve ETOPO1 + ríos del relieve; "am" Pacífico-América-Iberia; `python mapa.py` recalcula `datos/campos_*.npz`)
- `core.py` (cámara con longitud desenvuelta, capas de territorio int16, fractura con celdas fijas y por fronteras reales, contornos sin raya en el borde)
- `reg.py` (capas, `rejilla()` con fundido, `ciudad()`, `mar()`, registro de cajas para choques), `escenas.py` (fundido entre rejillas, sellos con emblema)
- `sellos.py` (emblemas: laurel, corona votiva, arco, castillo, yugo, columnas, lis, libro, gorro frigio, urna)
- `obj_es1..4.py` (≈110 dibujos: personajes por época, Dama de Elche, bisonte, elefante, acueducto, mezquita, Alhambra, galeón, Quijote, Meninas, SEAT 600…)
- `coreo_1..4.py` (coreografía por escena) · `coreo_util.py` (atajos ga/pa/andar/titulo/lugar)
- Pruebas: `./run.sh _prueba.py t1 t2 …` (previews/hoja.jpg) · `./run.sh _hojas.py 3` (previews/rev_NN.jpg, todo el video) · `./run.sh _qa_choques.py` (choques de texto)

## Lecciones
- Las capas se pintan por número: los pueblos de fondo (íberos, celtas) van en capas NEGATIVAS para que Roma (capa 0) quede encima.
- Al terminar una escena en la rejilla "am" hay que volver a "eu" con `R.rejilla(t_corte, "eu", 0.0)` (si no, todo se pinta sobre la rejilla gruesa).
- Los personajes geo-anclados crecen con el zoom: comprobar con `_qa_choques.py` que no invadan la fila de sellos (arriba a la derecha) ni el contador.
- Frase con «le arrebata Cuba»: Whisper oye «a Cuba» siempre → reescrita («España pierde Cuba…»).
- **Fundido entre rejillas** (`escenas.cobertura`): la rejilla "eu" solo abarca 43° de longitud; si la cámara ya voló fuera de ella cuando el fundido apenas empieza, se veía el rectángulo de Europa sobre papel vacío. Ahora donde "eu" no tiene mapa manda "am" (borde que se desvanece ~80 px). Aun así, empieza el fundido ANTES de que la cámara salga de Europa.
- **Ríos en rejillas envueltas** (`mapa._cortar_costura`): un río que cruza la costura de longitud (60° E) se dibujaba como recta de lado a lado del mundo (se veía a 42,2° N sobre España). Se parte en la costura al cargar.
- **Voz: CER 0 no basta** — Whisper (con VAD/GPU) ignoraba un «oas» de 0,3 s antes de «Fenicios». `qa.silenciar_arranque` lo detecta y `seleccionar` lo silencia (conserva la duración). Respaldos: `voz/gancho_0_antes_arranque.wav`, `audio/final_antes_arranque.wav`.
- **Grupos que marchan juntos**: mismo camino Y mismo reloj que el líder, separados por un desplazamiento fijo en pantalla (`off`) hacia un lado libre; con salidas escalonadas el retraso en la ruta deshace la separación y se apilan. Deja libre el lado donde espera otro personaje.
- **Personajes anclados al mapa + cámara que se va**: sácalos antes de que la cámara empiece a moverse (Pelayo quedaba cortado arriba y tapaba la etiqueta de la ciudad); y si el título va arriba, las rutas no deben subir hasta esa franja.
- **Antes de `video --rehacer` tras editar código sin el panel abierto**: `cache_escenas.conservar(car, ks, firma)` con todos los segmentos anotados (si no, `depurar` los borra).

_Comprobar archivos reales: `python fab.py estado historia_espana`._
