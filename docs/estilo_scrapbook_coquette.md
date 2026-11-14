# Estilo SCRAPBOOK COQUETTE — canal «Amaya Vibes» (`canal_amaya`)

Alta 10-nov-2026. Ejemplo completo: `videos/amaya_navidad/` (8:56, 15 mejores y 10 peores cosas que pedir en Navidad).
Referencias que eligió Amaya: `canales/referencias/amaya/` (ref1 plantilla «Welcome to my vlog», ref2 TikTok de stickers,
ref3-5 = SUS propios videos: «Amaya Vibe / Hello», avatar, stickers, «HAPPY WATCHING!!»).

## Qué es
Lista para preadolescentes (11-15 años, México) dibujada por código en UN plano secuencia (`escenas.cuadro(t)`), con:
- Fondos `vichy_amaya` (vichy rosa-rojo sobre crema), `rayas` pastel y `rayas_gris` (los PEORES): `coquette.fondo()`.
- Letras recortadas de revista en PASTEL que caen una a una (`rotulo_recorte`), papel rasgado + periódico en las esquinas (`esquinas`).
- Stickers de productos de FLOW (contorno blanco, sombreado suave) + stickers dibujados por código en el mismo lenguaje
  (`videos/amaya_navidad/stickers_codigo.py`: aguacate, fresa, martillo, celular, jabón, esponja, gel, bloqueador, dados, pulseras,
  nube, copo, nota musical, pilas, lata, claqueta, tienda, globo, pulgar). **No lo llames `dibujos.py`: choca con `nucleo/dibujos`.**
- SU AVATAR (`propios/amaya_avatar.png` + `_cierra` para parpadear) que sube desde abajo, salta de gusto con el sello verde y niega
  con el rojo (`avatar()` en escenas.py), con rayitas azules de «¡pop!» junto a la cabeza.
- Sellos `golpe_sello("si"|"no")` con temblor de cámara, etiquetas `cuelga_etiqueta(1..3)` ($/$$/$$$), cinta washi con el nombre,
  notitas adhesivas (`pega_nota`, Ink Free) ancladas a palabras, destellos y corazones.
- Transiciones: papel `rasgado` entre ítems; barras de `tv` al pasar a un PEOR.

## Plantilla de ítem (escenas.py)
`LAY[id]` = sticker principal · `NOTAS[id]` = notitas `(frase, palabra, texto, x, y, rosa[, fin])` · `SEC[id]` = piezas secundarias
`(frase, palabra, sticker, alto, x, y, rot, fin, opciones)` — **cada cosa que la voz nombra sale en ese segundo** (regla de oro y
promesas visuales) · `MOD[id]` = gancho propio (aplastar/estirar, crecer/encoger, luz de lámpara `halo`, spray, grietas, lágrimas,
charms que se columpian, flash de cámara…). Los sonidos se anotan en `EV` con las MISMAS anclas → `sonidos_navidad.py` + `sfx_proc.py`.
Huecos fijos: título arriba a la izquierda, sticker al centro-derecha (1180, ~530), notitas en (430, 520) y en la columna derecha
(1660-1700, 380/540/700; con ≥ 150 px entre ellas), etiqueta (1530, 250), sello (560, 770), avatar abajo a la izquierda.

## Final de suscripción (como el de Amaya)
Fondo rosa liso, botón de play rojo GENÉRICO (nunca el logo de YouTube), píldora roja «SUSCRÍBETE» → la mano (su sticker `mano`)
entra y da clic → «✓ SUSCRITO» gris + campana que se columpia + destellos; fila de sus stickers abajo; el avatar a la izquierda.
Cierre: repaso de todos los stickers, globo de comentarios con la pregunta, like + suscríbete, «Soy Amaya» en recortes y pantalla
final con dos cajas de video + listón «¡GRACIAS POR VER!» (≥ 5 s para los elementos finales de YouTube).

## Voz, música y SFX
Voz ElevenLabs Regina `9Godp7dNohUvXk6qp0gS` (cuenta 2), narra Amaya en 1.ª persona. Música Lyria coquette (piano suave, cajita de
música, pizzicato, cascabeles) en tramos ≤ 175 s; si Lyria da 402, biblioteca con piezas de cajita/juguetonas (nada oscuro).
SFX sintetizados (pop, cae, sello, nota, clic, campana, flash, spray, crujido, lata, claqueta, cajita…), nunca repetidos en seco.

## Fotos reales + stickers (el usuario, 10-nov-2026)
Objeto por objeto: **solo sticker** lo genérico o chistoso (calcetines, canasta, diario, paleta, tarjeta); **ambos** = el sticker
presenta el puesto y luego entra la foto real a un lado (cámara, audífonos, termo, peluche, squishy…); **solo foto** lo que no se
entiende sin verlo real (maquillaje cargado, pirata contra original, juego de mesa). Fotos de Wikimedia Commons con licencia libre
(`fotos_buscar.py`, API sin clave, con pausas porque da 429), enmarcadas en `foto_prep.py`: polaroid con washi, recorte con borde
blanco o recorte de revista; crédito en `fuentes.json`. NUNCA personas reconocibles ni logos grandes (por eso tintes y bloqueador se
quedaron con sticker). Identidad comprobada en `previews/pegatinas_check.jpg` (cada foto con su segundo) antes del render.
Lista escrita por Amaya: sus puestos llevan la insignia «elegido por Amaya ♡» (`CREDITO` en escenas.py) y la voz lo dice.

## Errores a no repetir (amaya_navidad)
- Al insertar entradas por texto en `NOTAS`/`SEC`, las claves se repiten en los dos dicts: corta el archivo en `SEC = {` antes de
  reemplazar, o caerá en el dict equivocado.
- Stickers de Flow con **contorno fantasma** de una pieza vecina (bálsamo, sérum, audífonos pirata, agenda): hacer `*_solo` con el
  componente más grande antes de usarlos.
- La luz proyectada (`halo`) tiene que verse en la pared: radio ~900 y opacidad ~0,85, si no, no se nota.
- Lágrimas/efectos sobre un sticker: medir la cara en la hoja; la primera estimación cayó en el pecho.
- Humor: pocos chistes y de observación; nada de memes del año pasado.
