# Estilo Kurzgesagt REAL — lo observado y medido (30-sep-2026)

Referencia estudiada: «This Is What a Godlike Civilization Would Look Like» (Kurzgesagt, `QW_jlUn4gA8`, 14:12), descargada para estudio local en
`referencias/kurzgesagt_godlike_QW_jlUn4gA8.mp4` (1080p60; fuera de git por `*.mp4`; NO se redistribuye ni se copian sus personajes ni sus dibujos:
solo se replica el LENGUAJE visual y de movimiento con personajes y objetos originales). El usuario pidió replicar ese estilo con rigor
(«lleno de detalles y movimiento», «fluidez») y mostró como modelo la aldea isométrica con empalizada.
Revisados ~190 fotogramas (hojas cada 6 s), secuencias a 0,1-0,25 s, 12 transiciones y mediciones con ffmpeg/OpenCV.

## 1. Medido (datos, no opiniones)
- **60 fps reales**: 0 % de cuadros repetidos en casi todos los tramos (cada cuadro es distinto). Nuestro motor renderiza a 30; para igualar la fluidez hay que renderizar a 60 (render x2).
- **Cámara casi siempre en movimiento**: actividad (píxeles que cambian en 0,1 s): 2-72 %; escenas isométricas con cámara viajando 300-900 px/s (a 1920 de ancho) con aceleración
  progresiva (recorrido de ~3.000 px en 4,5 s); movimientos «de empuje» con campana de velocidad (pico ~1.150 px/s, 1,75 s, ease-in-out); derivas lentas de 40-180 px/s;
  frenados suaves (480 px/s -> 0 en ~1,5 s). Cuando la cámara no se mueve (ADN, bici) todo lo demás sí.
- **Aparición de un globo de texto** (medida cuadro a cuadro): crece de 9 % a 92 % de su tamaño en 9 cuadros (0,15 s, casi lineal, ~19 px/cuadro de ancho), llega a su sitio
  con rebote muy pequeño (+1,5 % ancho, +5 % alto) y se asienta en ~0,3 s. Se mueve hacia su posición final mientras crece (ancla en la «cola»). Después puede volver a «saltar» (re-pop) para enfatizar.
- **Ritmo de planos**: 102 cambios de escena en 852 s (mediana 5,5 s; 28 planos de ≤2 s; 28 de >10 s). Los planos largos NO están quietos: viaje de cámara + cosas que aparecen.
- **Transiciones**: casi todo son CORTES directos en el pulso de la narración; pantalla dividida con una **muesca de flecha** en el borde; zoom a través de un objeto; fundido a oscuro corto; fugas de luz.

## 2. Tipos de plano (cada escena es UNO de estos, con mundo propio)
1. **Diorama isométrico** (aldeas, ciudades, fuertes, campos): proyección isométrica de 30° (pendiente 0,57), mundo enorme por el que viaja la cámara, cientos de personas diminutas (~50-90 px de alto a 1080p), animales, cultivos en hileras, fogatas, humo, mercados, carretas, coches; casi cada objeto tiene su micro-animación.
2. **Plataformas isométricas flotantes** (baldosas de color con sombra «flotante» azul oscuro debajo, una cúpula/vaso de cristal o un objeto encima, cono de luz translúcido, rejilla isométrica tenue de fondo) con etiquetas.
3. **Primer plano de personaje** (busto grande): ojos con destello de estrella de 4 puntas + círculos de brillo, mejillas rubor, cejas gruesas, pelo con degradado de 2-3 tonos y borde de luz amarillo, boca que cambia de forma al hablar; fondo de **bokeh** (discos desenfocados), chispas «+» y **haces de luz**; empuje lento de cámara.
4. **Paisaje lateral ilustrado** (cañón, parque de diversiones, Egipto, biblioteca interior): 4-6 planos de profundidad, gradientes de cielo, nubes con sombra, vegetación en racimos, luz cálida/volumétrica, personajes pequeños en acción.
5. **Espacio/energía**: gradientes púrpura-azul, estrellas de 4 puntas, galaxias, brillos con bloom, partículas.
6. **Infografía**: etiquetas en cápsula de color sólido con **muesca** (morado, magenta, naranja, azul; texto blanco en negrita), números en círculos, globos de diálogo (blancos o de color), barras, contadores.

## 3. Modelado (cómo están hechas las cosas)
- **Sin contornos**. Cada forma = relleno plano con **degradado sutil** + **2-3 tonos por cara** (cara iluminada clara, cara en sombra más fría/violeta) + a veces filo de luz.
- **Cajas isométricas** con 3 caras (arriba clara, izquierda media, derecha oscura) y luz desde la izquierda; **techos de dos aguas**: dos faldones (claro/oscuro), cumbrera, borde de espesor (franja más oscura) y, en algunos, alero con festón; hileras REGULARES de ventanas (marrón/morado oscuro con marco claro, a veces postigos verdes), puertas marrón oscuro, zócalo/cornisa de color acento (azul-verde), toldos rosas, jardineras de ladrillo con arbustos, chimeneas cilíndricas con humo.
- **Suelo**: dos tonos de camino sobre otro tono de suelo, bordes redondeados, sombras de contacto (franja más oscura junto a los muros, hacia la derecha), cuadrícula de baldosas muy tenue (líneas claras), cultivos en hileras de pequeñas plantas, estanques con brillos, setos oscuros bordeando caminos.
- **Árboles**: racimos de círculos en 3 verdes (más claro arriba-izquierda), troncos cortos naranjas; cipreses = elipses alargadas verde claro con base naranja; palmeras sencillas; rocas facetadas con luz arriba-izquierda; tocones; troncos de empalizada = cilindros con punta redondeada, tono rojo-naranja con filo claro.
- **Personas pequeñas**: cabeza circular (tonos de piel variados), pelo oscuro, torso de color saturado, piernas oscuras, sombra elíptica suave debajo; sombreros de paja naranja, rojos; grupos (adulto + niño), parejas; caminan con balanceo y rebote; hacen gestos (saludar, trabajar, cargar).
- **Animales**: ovejas (blanco con cabeza oscura), cabras, gallinas moradas/rojas, cerdos rosas; pequeños saltos y giros de cabeza.
- **Paleta por escena**: pocas familias muy saturadas (carmesí+blanco+verde lima+teal; naranja+verde; azul+rosa) con un acento brillante; fondos de espacio púrpura-azul.
- **Efectos**: fuego en 3 capas que parpadea, humo = círculos que suben y se agrandan desvaneciéndose, destellos «+» de 4 puntas, bloom en lo luminoso, haces de luz, bokeh, sombra «flotante» desenfocada bajo plataformas, líneas de velocidad.

## 4. Movimiento (reglas que hay que replicar)
- Nada está quieto: **idle en todo** (respiración, balanceo senoidal ~2-3 s, parpadeo cada 3-6 s con 3 cuadros cerrados, fuego, humo, ondas de agua, banderas, hierba).
- Entradas: escala 0 -> 1 en ~0,15-0,3 s con ease-out y rebote pequeño (1-5 %), **escalonadas** (retardo 0,05-0,1 s por elemento); texto/etiquetas igual; refuerzo con «re-pop».
- Cámara: viaje continuo con aceleración suave (ease-in-out, cúbico), empuje de ~2-4 % de escala por segundo, o deriva lenta; planos largos con recorridos grandes.
- Seguimiento/secundario: cabello, colas, tentáculos, ropa se retrasan 2-4 cuadros (60 fps) respecto del cuerpo; squash & stretch en saltos/aterrizajes.
- Multitudes: clones con **desfase temporal aleatorio** (0,1-0,5 s) y velocidades distintas para que nunca vayan a la vez.

## 5. Qué NO copiar
Personajes, mascotas y dibujos concretos de Kurzgesagt (el pájaro, los alienígenas, la niña, etc.). Aquí solo se toma la técnica y se dibuja todo original (personajes históricos mexicanos, arquitectura colonial, flora y fauna de México).

## 6. Ejemplo 2 (4-oct-2026): «This Woman Cured Her Cancer with an Insane Method» (Kurzgesagt, `0NY2gAftzJE`, 15:14) — personajes 2D y conceptos abstractos
Estudiado con cuadros reales (0:18, 0:36, 1:15, 1:37, 2:30, 3:05, 3:26, 4:00, 4:35, 7:00, 8:31, 9:20, 10:22, 13:20; el cuadro de 5:06 es un patrocinio, no el video) y un análisis visual de IA (que se equivocó en detalles: dijo «sin cuello» y «gafas sin patillas», pero la captura del usuario muestra cuello y patillas; **fiarse de los cuadros, no del texto**). No se copian sus personajes ni dibujos: solo el lenguaje.
- **Personaje en primer plano (3/4 de perfil, cabeza grande):** cuello visible, pelo en bloque con 2 tonos, gafas gruesas magenta CON patillas, pendiente, ojos cerrados como arco con pestañas, cejas sueltas, mejillas de rubor, boca pequeña fruncida; torso lila con manga de degradado claro→oscuro; manos con dedos marcados; fondo degradado violeta oscuro casi negro con viñeta. Un punto negro con halo turquesa en el pecho = el concepto («el tumor») sin dibujar órganos.
- **Personajes pequeños/de cuerpo entero (multitud, 4:00):** SIN CARA (óvalo liso de color piel), pelo en bloque de color vivo (verde, lila, morado), ropa de 2-3 colores planos, piernas rectas, sombra elíptica; variedad de peinados y de tonos de piel en la misma fila; cada uno con su «globo cuadrado con muesca» que muestra el concepto (células distintas por persona).
- **Silueta duotono (2:30):** cabeza con gafas toda en violeta, fondo de bordes magenta y centro negro (efecto de radiografía/recuerdo).
- **Persona en acción dentro de un círculo de luz (3:05):** científica de espaldas ladeada mirando un microscopio, enorme sol amarillo detrás, siluetas oscuras de matraces, suelo marrón rojizo; contraluz fuerte.
- **Medallón + línea de tiempo (10:22):** retrato en círculo con borde amarillo (paciente con compresa de hielo y mejillas rojas = fiebre) sobre fondo azul-violeta, barra de «Semana 1…6» con jeringas que aparecen; título de tarjeta naranja arriba a la izquierda.
- **Concepto abstracto con formas, no con dibujos literales:** cáncer = masa de células con borde claro y núcleo rosa neón sobre fondo de «tejido» (células oscuras a baja alfa, bokeh); células inmunes = criaturas naranja con patitas y un «?» sobre la cabeza; virus = bolas verdes/rojas con espículas; cirugía = bisturí lila sobre un tajo magenta con tejido de fondo; «viroterapia» = tipografía gigante rellena con patrones de colores; tarjetas coleccionables (morado, con ilustración y rayas naranjas) para listar virus.
- **Infografía:** etiquetas de cápsula (verde, morado, naranja) con texto blanco en negrita; globos de cuadrados con muesca; números/medallones con listón.
- **Paisaje lateral minimalista (13:20):** degradado cielo celeste → crema, personajes enormes (aves moradas/rosas) de perfil con patas naranja delgadas, ojos como un trazo, boca blanca; con letterbox negro en escenas cinemáticas (9:20).
- **Pantalla de software** (0:17): ventana con barra de herramientas, íconos de apps y cursor, el personaje dentro: composición UI plana como «marco» de la escena.
- **Fondo:** siempre degradado (radial o lineal) + bokeh de discos oscuros/claros a baja alfa; paleta de pocas familias (violeta/magenta/turquesa; o amarillo-naranja de contraluz). Nunca negro puro en objetos (sí en radiografía/letterbox).
