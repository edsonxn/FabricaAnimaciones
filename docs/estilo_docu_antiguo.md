# Estilo DOCUMENTAL DE PERSONAJE ANTIGUO (4-nov-2026)

Pedido del usuario: replicar cómo presentan los documentales **Detrás del Enigma** (@detrasdelenimga, 591 mil subs; Rasputín 1,9 M, Mona Lisa 3,8 M)
y **Homo Narrans** (@NarransHomo, 65 mil; el usuario lo llamó «Homo Sapiens»; Sargón 219 mil, Narmer 157 mil), «mismas fuentes, mismas animaciones»,
para biografías de **personajes muy antiguos y famosos (antes de Cristo)**. Canal: **Bitácora Perdida** (segunda línea de estilo, elegida por el usuario).
Kit: `nucleo/docu_antiguo.py` (encima de `docu.py`/`docu_fx.py`). Primer video: `videos/ramses_ii/`. Referencias bajadas: `E:\FabricaAnimaciones\_ref_docu\`
(rasputin, monalisa, narrans_sargon, narrans_narmer + `hojas/`).

## REGLA DEL KIT: cada escena, sus propias animaciones
«Cada animación es única, se recicla muy poco» (el usuario). El kit da PRIMITIVAS; cada escena compone algo nuevo para SU frase y lo declara:
`A.firma("kadesh_carros", "carros hititas en silueta cruzan el mapa + flecha que se parte + neón MENTIRA")`. `A.verificar_firmas(video)` (correr antes de
`video`) avisa si una receta se repite en el video o en otro video del kit; `A.registrar_firmas(video)` al cerrar (catálogo `nucleo/datos/docu_antiguo_firmas.json`).
Ni la misma toma de cine dos veces, ni el mismo artefacto con el mismo movimiento.

## Lo que se ve (medido cuadro a cuadro en las referencias)
**Detrás del Enigma 2026** — dos capas que alternan cada 2-6 s:
1. **Tomas de cine**: escenas recreadas fotorrealistas (película/IA), oscuras, gradación teal-ámbar, mucha viñeta, poca luz de ventana o vela. Aquí: **Flow**
   (imágenes Nano Banana con el código animando parallax/luz/partículas; clips Veo solo en momentos clave).
2. **Grafismos sobre negro** con motas de polvo: camafeos circulares con aro blanco luminoso (`camafeo`), sangre/líquido rojo que baja (`liquido`), rótulos serif en
   versales con la palabra clave en rojo, letra a letra (`rotulo_serif`), neón rojo que parpadea al encender con dos franjas grises encima (`neon`), cursiva
   Poppins con brillo (`cursiva_luz`, «Y LO CONSIGUEN»), texto Poppins blanco + gris que sube por palabras (`texto_mixto`, «Se acerca al cuadro»),
   suelo de rejilla 3D con personaje recortado y arco rojo de luz (`rejilla` + `arco_luz`), aura de color sobre una figura (`aura`), fotos de archivo
   como polaroids con hilo rojo (`docu.polaroid`/`hilo`), mapa de pergamino con ruta punteada (`docu.linea_punteada`), siluetas negras sobre rojo.
**Homo Narrans** — **objetos REALES recortados sobre pizarra oscura** (`piedra` + `artefacto`: sube, gira en Y, franja de luz), **citas de fuentes
antiguas en amarillo Arial Bold** centradas con la fuente debajo (`cita`), mapa satelital con el **territorio en rojo que crece** y nombres de pueblos
(`territorio` + `etiqueta`), relieves y pinturas reales a pantalla completa con paneo lento, diagramas planos sencillos (pirámide social).

## DENSIDAD: nunca secuencia de fotos (el usuario, 4-nov-2026, al ver el avance de ramses_ii)
«Se ve bien, aunque muy lenta en animación, poco dinámica, sin casi animaciones; no debe parecer secuencia de fotos: debe haber fotos pero con
elementos y múltiples capas de otros elementos.» Mínimo por toma:
- **≥ 4 capas que se mueven a velocidades distintas**: fondo (foto/Flow con parallax por profundidad o recorte en planos), 1-2 elementos recortados
  (estatua, carro, papiro, sello) que entran/giran/flotan, una capa de grafismo (camafeo, líquido, arco de luz, territorio, flechas, cifras que cuentan,
  rejilla) y una capa de primer plano (polvo, arena que vuela, humo, chispas, partículas de luz, siluetas desenfocadas que cruzan).
- **Algo nuevo entra cada 1-1,5 s** dentro de la toma (no solo cada corte); la cámara nunca quieta (empuje, paneo, giro leve, latigazo en cambios de tema).
- Fotos reales: nunca solas a pantalla completa más de ~1,5 s; recortarlas (rembg) y montarlas en un espacio con capas, marcos, sombras y luz que cambia.
- Transiciones con movimiento (barrido, zoom a través de un elemento, mancha de tinta/arena) además del fundido.
- Antes de renderizar: hoja de 6 cuadros por toma separados 0,5 s; si dos cuadros seguidos se ven casi iguales, a la toma le faltan capas.

### Segunda ronda (el usuario, 4-nov-2026, avance v2 de ramses_ii): «mejoró mucho, pero aún MÁS dinámico»
- **Casi cada frase invoca algo**: una animación, un movimiento de cámara, una capa nueva. La narración y su velocidad están bien; lo que debe sentirse más
  rápido es la IMAGEN.
- **Recursos de transición/espacio inventados, uno distinto por grupo de párrafos** (también cuentan para `A.firma`). Ejemplo del usuario: **túnel de capas**
  (el video avanza capa tras capa, las capas se apilan una sobre otra y la cámara se mueve a los lados). Inventar otros del mismo calibre: atravesar un
  relieve hasta la escena, páginas de papiro que pasan, arena que barre y deja la siguiente toma, zoom a través del ojo de una estatua, etc.
- **Errores que NO deben repetirse:**
  1. Parallax por mapa de profundidad sobre un PERSONAJE = contorno doble/fantasma (hombros y brazo «duplicados»). Personas: recortarlas (rembg) en su
     propia capa sobre el fondo rellenado, o mover la imagen entera sin deformarla; el warp de profundidad solo para paisaje/arquitectura.
  2. Un elemento añadido (luz que parpadea, chispa, marcador) debe ir ANCLADO a la imagen: aplicarle la misma cámara/transformación que a la foto; si el
     fondo se mueve y el elemento no, se ve pegado encima (luz roja del avión).
  3. Mapa: el territorio debe caer sobre la geografía real (Egipto = valle del Nilo, no un embudo sobre el mar); calcular el polígono en coordenadas
     lon/lat del mapa, no en píxeles de pantalla a ojo. Nada de franjas/paneles grises colgando del borde.
  4. Rótulos nunca cortados por el borde del cuadro (`REGENTE A LOS 14 AÑOS` se salía): medir el ancho y dejar margen ≥ 6 %.

### Tercera ronda (el usuario, 4-nov-2026, avance v3): «lo veo igual de estático»
- **NO** a los empujones de zoom/pulso cada pocos segundos (`golpe()` de ramses_ii): se sienten repetitivos. Ningún movimiento mecánico periódico.
- «Que cada oración evoque algo» = **una CAPA NUEVA con su propia animación**: un motion graphic nuevo, una pegatina nueva, una imagen nueva,
  un personaje, un texto. No un movimiento de cámara.
- **TÚNEL DE CAPAS (la idea central del usuario):** la escena empieza con unas capas; conforme el narrador cuenta más, se AGREGAN capas de lo que
  narra, cada una en su profundidad, y la cámara viaja por ese túnel: casi siempre hacia el fondo (hacia atrás), pero a veces hacia un lado, hacia
  arriba o hacia abajo. Es un espacio 3D continuo que se va llenando, no un fundido entre tomas. Nada repetitivo: cada capa distinta.

- Implementación (ramses_ii v4): `videos/ramses_ii/tunel.py` (`Tunel(laminas, capas, viaje)`, sprites `spr_png/spr_foto/spr_camafeo/spr_texto`);
  posiciones de capa en fracción de media pantalla vista desde su lámina; se recortan al cuadro salvo cuando la cámara las atraviesa.
  Si funciona, subirlo al kit (`nucleo/`). Render con `--procs 4` (más procesos = sin memoria).

## Tipografías (fijas)
| Uso | Fuente | Color |
|---|---|---|
| Rótulo / neón | Times New Roman Bold, VERSALES, tracking 0,06 | blanco + palabra clave roja `ROJO` |
| Frase de golpe | Poppins SemiBold Italic MAYÚSCULAS con brillo | blanco o rojo |
| Texto mixto | Poppins SemiBold | blanco + gris `GRIS` |
| Cita antigua | Arial Bold | amarillo `AMARILLO` (0,98, 0,80, 0,16) |
| Etiqueta de mapa | Poppins SemiBold con punto que late | blanco |

## Acabado y ritmo
- `A.cine_antiguo(img, t)`: filtro `docu_fx.cine` medido (viñeta 0,78, bloom 0,30, escaneo 0,05, sin tilt-shift: los rótulos van NÍTIDOS; `tilt=3.5` solo en
  fotos/tomas sin texto arriba).
- Poco texto: un rótulo cada 5-8 s, nunca subtítulos. Voz pausada (Detrás del Enigma no corre). Cortes por fundido a negro, empujes de cámara lentos.
- Lo que la voz nombra se ve (REGLA DE ORO): lugar → foto real o mapa; objeto → artefacto real recortado; persona antigua → estatua/relieve real (nunca
  un retrato inventado presentado como real; las recreaciones de Flow son «escena», no «retrato»).
- Material real: Commons (`imagenes_web.guardar_commons` → `creditos.json`), recortes con `rembg` (API Python: `from rembg import remove`; el
  `python -m rembg` no funciona), video real con yt-dlp ≤ 8 s con crédito.

## Lecciones de la prueba (`videos/ramses_ii/_prueba_kit.py`, 4-nov)
- `rembg` deja mucho margen transparente: `artefacto` recorta al contenido (si no, la estatua sale diminuta).
- El tilt-shift de `docu_fx.cine` emborronaba los rótulos de arriba → desactivado por defecto.
- El líquido con ondas de alta frecuencia parecía una cinta en zigzag: ondas largas (0,012-0,05) y borde suavizado 2,4.
- `liquido` va ANTES del `camafeo` (nace por debajo del aro).

## Lecciones del video completo (`videos/ramses_ii/`, 4/5-nov-2026)
- **Túnel de capas en TODO el video** (`videos/ramses_ii/tunel.py`, `Tunel(laminas, capas, viaje)`): cada capítulo con su RECORRIDO propio
  (zigzag, recto y hondo, subida, izquierda, caída, espiral…), registrado con `A.firma("tunel_<cap>")`; +0,6 de z extra al cambiar de capítulo.
  Fundido a negro de 2 s al final.
- **Rótulos sueltos de capa caducan a los 5 s** (`Tunel.txt_desde`/`txt_dura`): sin eso, en el minuto 6 se amontonan.
- **No repetir en una capa el texto que ya pinta la lámina** (en ramses se quitaron 24): la capa aporta material nuevo (foto, camafeo, recorte).
- **Lámina que empieza en negro = hueco oscuro de 2-3 s** tras la transición del túnel (pasó en `f_hijos`, 6:06): el fondo y el titular
  arrancan en `ta + 0,5`, aunque la palabra llegue después.
- **Corregir tras el render completo:** `video --rehacer` DESCARTA todos los segmentos si cambió el código (firma). Para un tramo corto,
  renderiza solo esos segmentos aparte (`render._repartir` con las 3 tareas, con `if __name__ == "__main__"`), parte el MASTER con
  `ffmpeg -f segment -segment_time 3 -c copy` (hay clave cada 3 s), cambia los trozos y vuelve a unir: 2 min en vez de 2,8 h.
  El concat con `inpoint/outpoint` sobre el MASTER mete 2 cuadros duplicados: no usarlo.
