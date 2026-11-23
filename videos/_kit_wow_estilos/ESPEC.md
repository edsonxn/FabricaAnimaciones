# 5 propuestas de estilo para el kit visual de Crónicas de Warcraft (22-nov-2026)

El usuario quiere MEJORAR el kit visual de Warcraft (cuadros/fichas, íconos y marcadores sobre los mapas, líneas de ruta, rótulos)
y elegir entre 5 estilos. Cada estilo = UN video de 30 s, 1920x1080, 30 fps, H.264 + AAC, que muestra el MISMO contenido para
poder compararlos. El kit actual (lo que se quiere superar) está en `nucleo/mg_wow.py`, `nucleo/mg_mapa.py`, `nucleo/peg_estilos.py`,
`nucleo/peg_anim.py`, `nucleo/mg_wow60.py`; míralo para no repetir su look (y para reutilizar utilidades si te sirven).
Animación POR CÓDIGO (Python: numpy/PIL/opencv + ffmpeg `C:\ffmpeg\bin\ffmpeg.exe`), cuadro a cuadro, con easing y movimiento
(nada de diapositivas estáticas). Todo original: no copiar el arte ni la interfaz de Blizzard ni de otro canal; los íconos e
imágenes del juego que ya tenemos sí se usan (son las «fotos» de lo que se nombra).

## Contenido común (idéntico en los 5)
Assets (en `C:\FabricaAnimaciones\videos\wow_errores_60\`):
- Mapa: `mapas/ungoro_norte.jpg` (coordenadas en % de la imagen: Refugio de los Mariscales 43.6,23.0 · Gryfe (vuelo) junto al Refugio ·
  Bancal del Creador 47.3,10.8 — ver `_coords.md`).
- Pegatinas: `pegatinas/bancal_creador.png`, `pegatinas/o_cristal_rojo.png`, `o_cristal_amarillo.png`, `o_cristal_azul.png`,
  `o_cristal_verde.png`, `pegatinas/ungoro.png`, `pegatinas/refugio_mariscales.png` (si existe).
- Gameplay de fondo: `medios/scene-089.mp4`, `scene-091.mp4`, `scene-093.mp4` (Bancal del Creador / Un'Goro).
- Música: `audio/wow/nlXOcybLHxc.wav` (Un'Goro, OST de WoW) a −18 dB con fundido de entrada y salida. Sin voz.

Guion visual (30 s):
1. **0-11 s · MAPA CON RUTA:** entra el mapa (con el tratamiento del estilo: marco, viñeta, color), rótulo de zona «CRÁTER DE UN'GORO»,
   aparece el marcador del Refugio de los Mariscales (con su nombre), la LÍNEA DE RUTA se dibuja hacia el Bancal del Creador
   (con el estilo de línea propio), cae el marcador final con la foto `bancal_creador.png` junto a él y rótulo «BANCAL DEL CREADOR · 58-60».
2. **11-21 s · FICHA SOBRE GAMEPLAY:** gameplay de fondo (scene-089/091) tratado según el estilo; una ficha/cuadro con título
   «N.º 15 · SIN LOS 60 CRISTALES», los 4 íconos de cristal entrando uno a uno con «×15» cada uno, y un contador que sube a «= 60».
3. **21-30 s · TARJETA DE JEFE + RÓTULO INFERIOR:** gameplay (scene-093); tarjeta/reliquia con `bancal_creador.png` y el texto
   «JEFA FINAL: NANAYA» / «cambia de elemento cada 25 %», más un rótulo inferior (lower third) «Sin cristales: solo 5 jefes»
   con un sello o acento del estilo; salida animada.
Esquina superior izquierda, discreto, todo el video: «ESTILO N · <NOMBRE DEL ESTILO>».
Texto en español, tipografías de `C:\Windows\Fonts` (o .ttf libres ya en el proyecto: búscalas con Glob `**/*.ttf`), legible a 1080p.

## Los 5 estilos
1. **Cartógrafo de pergamino:** mapa en sepia con bordes quemados, ruta de pluma punteada que se va entintando, marcadores = sellos de
   lacre que caen y se aplastan, fichas de pergamino enrollado que se despliegan, tinta que se esparce, letra caligráfica.
2. **Reliquia de oro y piedra:** marcos tallados de piedra oscura con filo dorado y gemas engastadas (originales, no la UI del juego),
   ruta = cadena de runas doradas que brillan al encenderse, marcadores = gemas facetadas que destellan, destellos y polvo dorado.
3. **Holograma arcano:** mapa proyectado azul-violeta con líneas de escaneo, rejilla y círculos rúnicos que giran, ruta = haz de energía con
   partículas, marcadores = anillos que pulsan, fichas de cristal translúcido con borde de neón, glitch suave en las entradas.
4. **Táctico plano (infografía):** diseño plano moderno, colores sólidos con acentos por facción, ruta = línea gruesa con flecha y
   distancia, marcadores = pines geométricos con número, fichas tipo tarjeta con sombra suave, contadores grandes, tipografía sans negrita.
5. **Cuaderno de explorador (acuarela y lápiz):** manchas de acuarela que se extienden, trazos de lápiz que dibujan el contorno de la ruta,
   notas manuscritas y flechas a mano, recortes pegados con cinta, fichas en papel de cuaderno con clip.

## Entrega
Carpeta `C:\FabricaAnimaciones\videos\_kit_wow_estilos\estilo_N\` con su script `estilo_N.py` (reutilizable: funciones `mapa_ruta`, `ficha`,
`tarjeta`, `rotulo` parametrizables, para pasarlas al kit si el usuario lo elige) y el video `estilo_N_<nombre>.mp4` (30,0 s).
Hoja de revisión `estilo_N/hoja.jpg` (12 cuadros, uno cada 2,5 s) que MIRES tú antes de dar por bueno el video: texto legible, nada
cortado, la ruta va del Refugio al Bancal, los íconos son los cristales, se nota el estilo. No uses `fab.py` ni toques otros videos;
no detengas el panel ni mates procesos python ajenos. Render con ffmpeg a `-preset medium -crf 20`, usando como mucho 4 hilos
(otros 4 estilos se hacen a la vez).
