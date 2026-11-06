# Estilo «Disección en vivo» (vertical; 5-nov-2026, nació en `videos/euphoria_robots/`, canal Edsonxn)

**Para qué:** explicar CÓMO FUNCIONA algo que de verdad existe (un motor, una herramienta, un sistema) en un video vertical.
Pedido del usuario: «parecido a Kuriox pero con un estilo nuevo que lo explique mejor», combinado con las grabaciones reales que
exige el canal Edsonxn. Kit: `nucleo/diseccion.py`. Primer video: `videos/euphoria_robots/` (el motor tipo Euphoria del Robotaller).

## La idea en una línea
La grabación REAL vive en un monitor flotante y el código la **abre como en rayos X** (un barrido la vuelve radiografía);
debajo, lo mismo que se ve en la grabación corre **simulado de verdad** en Python, en plano tipo Kurzgesagt, con su
anatomía a la vista (puntos, huesos, fuerzas, centro de masa). Lo que explica la voz no es una animación dibujada: es la cosa funcionando.

## Composición vertical (1080x1920), de arriba abajo
| zona | y | qué va |
|---|---|---|
| kicker | ≈250 | pastilla de color del paso: «PASO 1», «ERROR REAL · 5-NOV» (`D.kicker`) |
| titular | ≈380 | UNA palabra clave gigante, Poppins, entra con rebote (`D.titular`, px 130-150) |
| monitor | 520-1030 | grabación real (`pip()` en escenas.py → `D.monitor`), etiqueta «● GRABACIÓN REAL», bisel de 2 tonos, sombra, flota |
| escenario | 1050-1560 | el muñeco/objeto simulado (`D.muneco`), flechas de fuerza, centro de masa, plomada, base de apoyo |
| piso + pie | 1560-1850 | losa de 2 tonos con líneas de fuga; una pastilla con el estado («dentro: de pie» / «fuera: ¡un paso!») o un deslizador |
El gancho invierte el peso: monitor grande arriba (960x860) con la caída real, titular en medio y el muñeco chico abajo.
Momentos sin grabación: una **tarjeta de fórmula** (`tarjeta()`: fondo oscuro, barra amarilla, líneas que entran una a una) ocupa el centro.

## Piezas del kit (`nucleo/diseccion.py`)
- `fondo(t, tono)` degradado azul-violeta + rejilla de laboratorio que deriva; `manchas(lz, t, tono)` 3 halos grandes a distinta profundidad.
- `monitor(lz, frame_bgr, cx, cy, w, h, t, rayos=, barrido=)` radiografía = luminancia invertida teñida de turquesa + bordes Canny + líneas de barrido;
  `barrido` 0..1 pasa una barra de luz y deja la radiografía a su izquierda.
- `Sim` = **el mismo modelo que `nucleo/panel_vivo_ragdoll.js`**: 7 puntos (cabeza, pecho, cadera, 2 manos, 2 pies) con sus masas y radios,
  huesos con largo mínimo y máximo, Verlet a 180 Hz, gravedad 820, músculos (resorte a una pose, `k` 0 = trapo, 1 = animación),
  equilibrio por punto de captura (centro de masa + velocidad × √(altura/g)) con paso del pie, torso al revés, brazos abiertos, y reflejo
  de cubrirse la cabeza al caer. `escenario("trapo"|"rigido"|"leve"|"fuerte"|"vuela"|"arreglado")` = experimentos fijos y deterministas
  (se calculan una vez; el render en paralelo da lo mismo en cada proceso). «vuela» reproduce el error real del 5-nov (manos a 32 sobre el pecho
  con un brazo de 21: la meta viaja con el cuerpo y lo saca volando); «arreglado» = el arreglo real (≤ 18), cae al hoyo.
- `muneco(lz, P, ox, oy, s, rayos=, etiquetas=, cara="x")` el robot en plano (cápsulas de 2 tonos, cabeza-pantalla con ojos, antena con luz);
  `rayos` aclara el cuerpo y enciende el esqueleto (huesos blancos, puntos amarillos con halo); `etiquetas` nombra los 7 puntos con llamadas.
- `flecha` (fuerza plana con brillo en un borde), `centro_masa` (círculo en cuartos), `base` (verde dentro / coral fuera), `punteada`, `titular`, `kicker`.
- Paleta: fondo (16,12,44)→(46,26,96); turquesa del taller (125,243,225); amarillo fuerza; coral error; lila; verde «estable». Cada bloque tiene su par de tonos (`TONOS`).

## Reglas
- **El `Sim` es una versión de diagrama:** misma anatomía, masas, huesos, 180 Hz y gravedad; el controlador de equilibrio es más simple que el real (con los 0,2 s y 170 ms exactos del motor, sin sus límites de pasos ni la subida de músculos, se vuelve inestable). La voz cita las cifras del motor real, no las del diagrama.
- **Lo que se simula es lo que existe.** Las constantes del `Sim` se copian del código real; si el motor cambia, se copian otra vez. Nunca una cifra inventada.
- **Cada paso lleva grabación real en el centro** (Edsonxn: la grabación es la base). Mientras no exista, `clip()` falla salvo `FAB_RESPALDO=1` (solo hojas).
- Nada quieto: monitor que flota, rejilla que deriva, manchas que se mueven, el muñeco siempre simulando.
- Una palabra clave por bloque; nada de párrafos en pantalla. Sin subtítulos quemados.
- Hoja de prueba sin renderizar: `python _pruebas/hoja_estilo.py momento:u …` → `previews/hoja_estilo.jpg` (mírala antes del render).
- Coste medido: ~2 s por cuadro de hoja con SS=2 en un proceso (incluye cargar el clip).

## Pendiente / ideas
- Esqueleto REAL sobre la grabación: exportar `Trapo.estado()` cuadro a cuadro al grabar con `robotaller.grabar` y dibujar los 7 puntos encima del barrido.
- Transición propia entre pasos: el esqueleto «salta» del monitor al escenario de abajo.
