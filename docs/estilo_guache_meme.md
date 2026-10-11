# Estilo guache y videos de meme por rondas

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

## Estilo `guache` (libro infantil en gouache) y videos de meme por rondas (ejemplo: `videos/pelea_meme/`, 65 s, 16:9)
- Referencia: post de @e_page «Economía de la isla» (X, 27-sep-2026): ilustración de libro infantil, paleta apagada y cálida (azul verdoso,
  crema, arena, terracota), formas planas SIN contorno con media luna de sombra, personajes de cabeza redonda con ojos de punto y mejillas
  rosadas, grano y fibra de papel. `ESTILO_VISUAL = "guache"` (entrada en `estilos.py`: `papel=0.55` activa la textura de papel en
  `efectos.acabado`). Kit en `nucleo/guache.py` (todo en px de 1080p, coordenadas de mundo dentro de `lz.grupo`):
  - **Personajes:** `hombre` (Don Beto: tirantes, bigote, chanclas; poses por ángulos de brazo `(hombro, antebrazo)`, `cara=` normal|brava|asombro|
    grito|ko|sonrisa|miedo|esfuerzo|victoria, `agach`, `inc`, `casco`, `arma_f/arma_b`; devuelve la posición de las manos), `escorpion`, `trex`,
    `tiburon`, `platillo`, `dragon` (todos nativos mirando a la derecha; `mirar=-1` los voltea). **Armas:** `chancla`, `sarten`, `pez_espada`,
    `extintor`, `tapa_olla`. **Efectos:** `explosion`, `ono` (onomatopeya), `polvo`, `spray`, `fuego`, `salpicadura`, `brillo`, `estrellitas`,
    `lineas_vel`. **Interfaz:** `barra` (vida), `rotulo`, `pastilla`.
  - `sombreado(lz, pts, color)`: forma oscura + la misma forma menor y corrida hacia la luz (la media luna de sombra). Formas largas y finas:
    usa el lado corto (ya lo hace) o dibuja a mano.
  - **Mundo continuo:** `fondo_mundo(X0, t)` mezcla el bioma actual con el siguiente con un borde de pincel; 5 biomas (desierto, selva, océano,
    Luna, volcán) de `BIOMA_W = 1920` px cada uno. El héroe va fijo en pantalla (x = HX) y la cámara corre `X0(t)` de una ronda a la
    siguiente (carrera de 1,9 s con `paso`/`ph` según X0); los props de cada bioma solo se dibujan si están cerca de la pantalla.
    Cuidado con lo que sobresale del bioma (hojas, muelle, olas): se ve en el vecino; el muelle/ola llega exacto a los bordes.
  - **Coreografía anclada a la voz:** `T(id, palabra, frase=)` en escenas.py da el tiempo de cada golpe; `kf(t, [(t0, v0), ...])` interpola
    claves, `bal(t, t0, t1, p0, p1, alto)` da trayectorias parabólicas (criatura lanzada, chancla, pez). Marcadores de ronda / ¡PELEA! / ¡NOCAUT!,
    barras de vida y medallas de las criaturas (tachadas al vencerlas) se dibujan en `ui()` (coordenadas de pantalla, sin cámara).
  - **Voz:** Chatterbox dice «nocaut» a la inglesa y Whisper lo escribe «knockout»: `qa.normaliza` lo iguala. Frases cortas del tipo
    «X. Nocaut.» pueden fallar por la pausa; si ocurre, cambiar la puntuación o el orden.
  - **Sonidos nuevos** (`sfx.py`): `chancla`, `bonk`, `gong`, `ko`, `estrellitas`, `bocinazo`. `BIB` se calcula al entrar a `main()` para
    incluir los efectos definidos al final del archivo.
  - Prueba rápida sin render: `videos/pelea_meme/_prueba.py <nombre> t1 t2 ...` (hoja de contacto en `previews/`) y `_kit_test.py` (todos los dibujos).
