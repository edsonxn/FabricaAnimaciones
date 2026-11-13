# Estilo «LÍNEA 3D» — transmisión de lanzamiento en alambre blanco sobre negro

Creado el 13-nov-2026 para `videos/cohete_crs30/` (prueba SIN CANAL para un canal nuevo de cohetería y exploración espacial).
Referencia: las animaciones de trayectoria de las transmisiones de SpaceX: todo es 3D real de líneas blancas, monocromo, con un
HUD de misión (reloj T+, arco de eventos, estado de motores). Nada de colores, nada de texturas, nada plano.

## Kit
- `nucleo/linea3d.py`: `Cam(pos, mira, arriba, fov, cerca, centro=)` (perspectiva real; `centro=(x, y)` coloca el punto mirado
  fuera del centro de pantalla: así se deja sitio para tablas y rótulos sin descentrar el mundo), `L3` (lienzo 2× con
  rellenos negros que ocultan lo de atrás, texto Bahnschrift tipo DIN, `final(t)` = brillo, viñeta y grano), `globo` (rejilla +
  costas mundiales con shapely, cacheadas en `nucleo/datos/costas_mundo_*.npz`, limbo exacto), `Sitio` (lat/lon → marco
  ENU en km; `gran_circulo` para trayectorias por rumbo), `cuerpo_revolucion`, `chorro` (pluma de partículas), `rejilla_suelo`,
  `circulo3d`, `etiqueta3d` (rótulo con guía hacia un punto 3D), `curva_suave` (tablas de trayectoria suavizadas).
- `nucleo/linea3d_cohetes.py`: Falcon 9 por partes en metros (etapa 1 con 9 motores, aletas de rejilla y patas; etapa 2 con MVac;
  Dragon con morro), Estación Espacial, torre, zona de aterrizaje. `Z_S2`, `Z_DRAGON` para piezas sueltas.
- Mundo en KM con el centro de la Tierra en el origen; el cohete en metros × 0,001.

## Cómo se arma un video (copiar de `videos/cohete_crs30/`)
- `escenas.py` dibuja el cuadro entero en función del tiempo global (`cuadro(t)`), con planos (`PLANOS`) encadenados por fundidos
  de 0,3 s; `Mundo(Escena)` solo envuelve `cuadro`. `TRANSICIONES = [("continua", 0.5)] * (n-1)`, `ESTILO_VISUAL = "documental"`.
- **Reloj de misión** anclado a la voz: tabla `RELOJ` (segundo de video ↔ segundo de misión, con `ww(escena, frase, palabra)`);
  `mision(t)` interpola. Todo (posición, motores, etiquetas, HUD) depende del tiempo de MISIÓN, así el reloj T+ y la imagen
  nunca se contradicen. Los tiempos de los eventos, de la fuente oficial (NASA para CRS-30, en el docstring de `guion.py`).
- Trayectorias ESQUEMÁTICAS (forma plausible, sin cifras de altura/velocidad en pantalla); geografía real (costa OSM del Cabo,
  coordenadas OSM de SLC-40 y LZ-1, distancia comprobada).
- `_hoja.py t1 t2 … --out x [-f]` en la carpeta del video: hoja de cuadros 640×360 (~1 s/cuadro). Revisar CADA plano así.
- SFX: `eventos_sfx()` en escenas.py (lista de tiempos anclados a la voz) + `SFX_ELEVEN` en guion.py; `Mundo.preparar` emite
  los eventos de su escena. Música de la biblioteca (`mods_ia_fusion__lyria_1` = sintetizador tipo webcast).

## Errores encontrados y cómo no repetirlos (13-nov-2026)
1. **Cámara que se aleja con el foco moviéndose linealmente** (regreso, aterrizaje, cierre): a media subida el foco ya está lejos
   y la distancia aún es corta → el objeto sale del cuadro o la cámara queda BAJO TIERRA (cuadros negros 64-66 s). Regla: en un
   viaje logarítmico de distancia, el foco se mueve AL RITMO DE LA DISTANCIA: `kf = (dist - d0) / (d1 - d0)`.
2. **Curva suavizada que no llega al destino**: `curva_suave` promedia la tabla y el cohete «aterrizaba» a 10 m de altura y 40 m
   de la plataforma (flotaba). Para el final de una trayectoria que debe tocar un punto exacto, mezclar con un perfil analítico
   (`h = h0·q²`, `q = (t_fin - m)/Δ`).
3. **Objeto que cae desde km de altura con la cámara fija en el suelo**: cuadros vacíos con solo el rótulo. La cámara ACOMPAÑA al
   objeto desde arriba y el suelo (rejilla grande + mapa) sube a su encuentro; el lado del que mira la cámara importa: desde el
   mar hacia tierra se ve la costa detrás; al revés, solo negro.
4. **Foco de la pila mal calculado** (órbita): `p + a·(Z_S2+12)` dejaba la etapa 2 cortada en el borde; centrar en el centro de la
   pila real. Y un error de paréntesis en una mezcla `p + x·(1-k) + y·k` mandó la cámara a 4900 km (cuadros vacíos).
5. **Rótulos**: el ancla de un rótulo que baja con el objeto acaba encima del HUD (MECO); poner el rótulo con `dy` grande hacia
   arriba o del lado contrario a donde se mueve el objeto. Tablas a la derecha → objeto a la izquierda con `Cam(centro=)`.
6. **Capa vista de canto**: un plano (aire denso) con la cámara a su altura es invisible; subir la cámara para verlo como plano.

## Promesas visuales
`videos/cohete_crs30/promesas.md`: 22 frases con su segundo y la hoja `previews/promesas_a/b.jpg`. Todo lo que dice la voz se ve
(9 motores con vista inferior, Max Q con conos de choque y gráfica, MECO, separación, media vuelta con flecha de giro, cae de cola,
capa de aire denso, aterrizaje con patas y polvo, 9 KM en el mapa, SECO, Dragon que se suelta, Estación, 5 vuelos del B1080).
