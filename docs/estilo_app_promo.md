# Estilo «anuncio de app» (UI de la app dibujada por código)

Para anunciar una app o producto **del usuario** usando SU propia interfaz: la pantalla, las tarjetas, los colores y la fuente
de la app, animados por código en plano secuencia. Primer video: `videos/duo_promo/` (Dúo · Misiones en pareja, 13-oct-2026,
vertical, 46,6 s, voces Lina + Eric de ElevenLabs, Lyria, 55 SFX de ElevenLabs). Kit: `videos/duo_promo/duo.py`.

## 1. Sacar el estilo de la app (sin leerla entera)
- `manifest.json` + cabecera de `index.html`: nombre, lema, `theme_color`, fuente (`fonts.googleapis.com/css2?family=…`).
- `:root{…}` y su `@media (prefers-color-scheme:dark)`: TODOS los colores (fondo, tarjeta, línea, texto, apagado, acentos, degradado).
- CSS de cada componente (`.card`, `.btn`, `.pill`, `.tag`, barras, listas, navegación, toast, overlay) → mismos radios, rellenos y
  sombras, en **px CSS**; se dibujan dentro de `p.grupo(x, y, k)` y el pintor escala (k ≈ 1,9 para un teléfono que llena el vertical).
- Textos REALES de la app (misiones, preguntas, mensajes): grep de los arreglos de datos. Nada inventado si la app ya lo dice.
- Fuente: el CSS de Google Fonts con un User-Agent viejo (`curl -A "Mozilla/4.0" …`) devuelve URLs `.ttf` estáticas por peso →
  `videos/<v>/fuentes/`. Revisar glifos con fontTools: Plus Jakarta Sans NO trae «✓» ni «♥» (se dibujan: `palomita`, `_corazon`).
- Emojis de color: PIL 12 con `C:/Windows/Fonts/seguiemj.ttf` (tamaño nativo 109) y `embedded_color=True` (`P.emoji`). Nunca
  meter emojis dentro de `p.texto` (salen como cajitas). «📲» y «💪» se ven raros en Fluent: mejor un ícono dibujado.

## 2. Kit (`duo.py`) — qué trae y qué reutilizar
- Pintor `P` (primitivas de `mods_ia_fusion/pix.py`) + degradado horizontal de marca `hg=(xa, xb[, paradas, fase])` en
  poly/rrect/elip/texto (con `fase` corre como `background-position` animado), `sombra()` difusa (box-shadow, a 1/4 si es grande),
  `trazo()` para palomitas que se dibujan, `oscurecer()` para el velo de los overlays.
- Fondo: las manchas difusas de la app calculadas a 1/4 de resolución (`_manchas`) + plano medio de orbes/corazones/destellos
  con paralaje (`fondo_duo`) → los 3 planos de profundidad de la regla de rigor sin tapar la UI.
- `telefono(p, cx, cy, k, t, contenido)`: cuerpo, isla, barra de estado, pantalla recortada y `_esquinas` (tapa lo que sale
  de las esquinas redondeadas; ojo con el barrido de 90°: el primer intento barría 270° y tapaba «9:41»).
- Componentes con nombre de la clase CSS: `tarjeta`, `pill`, `tag`, `avatar`, `check`, `mision`, `barra_xp`, `anillo_dia`,
  `tarjeta_xp`, `calendario`, `pestanas`, `boton`, `toast`, `logo`, `burst` (confeti con los colores de la app), `orbe`, `float_xp`.
  Para otra app: copiar el pintor y el fondo; los componentes se rehacen con el CSS de esa app (no reciclar escenas).

## 3. Estructura que funcionó (45 s vertical)
gancho con un problema cotidiano (chat de pareja que nunca concreta) → el logo nace de los dos personajes → teléfono con la
pantalla principal y una acción por frase (palomita + «+25 XP» + orbes que vuelan a la barra) → zoom a la barra que se llena →
overlay de festejo con confeti → segundo teléfono (cámara que viaja en un «mundo» con los dos) → toma de los dos teléfonos
sincronizados → cuestionario → «Creando sus misiones…» → cierre con logo, lema palabra por palabra y botón de descarga.
- Cámara: `Cam(z, cx, cy)` con `kf()` (claves por tiempo) y `css_a()` para llevar px CSS de un teléfono a pantalla: así la
  utilería grande del plano delantero (emojis 150 px, avatares que alimentan la barra, corazón que viaja) cae justo en su tarjeta.
- Cada frase cambia algo en pantalla, anclado con `ww(escena, frase, palabra)`; utilería grande al decir la palabra, palomita al
  final de la frase.

## 4. Audio
- Diálogo de dos voces ElevenLabs `eleven_v4`: narradora en `VOZ`, la otra en `VOZ_POR_FRASE` (su `sim` sale baja: normal).
- Duración: el núcleo cuantiza escenas a compases. Con Lyria (no usa el BPM) poner `BPM = 480` cuantiza a 0,5 s y márgenes
  `pre/post` cortos: 56 s → 46,6 s sin tocar la voz.
- SFX de ElevenLabs suaves de interfaz (pop, ding, chime, swish), con variantes de los frecuentes (`check_1/2/3`, `xp_1/2`,
  `burbuja_a/b`) y contados con `--seco` (regla «SFX repetidos no»). `MEZCLA = dict(musica=-22, sfx=-24, fx=-17)` → voz 15 dB arriba.
- Lyria: sin oírla, elegir el candidato cuya curva de dB por segundo se parezca al arco de intensidades (y que el cierre no caiga).

## 5. Cierre / llamada a la acción
- **No mostrar URLs provisionales** (el usuario, 13-oct-2026): Dúo saldrá en tiendas; el cierre es botón «Descarga Dúo» +
  insignias genéricas «Descárgala en App Store / Google Play» SIN los logos oficiales (Apple y Google exigen su arte oficial:
  cuando la app esté publicada, se pueden sobreponer las insignias oficiales). Preguntar el CTA antes de animarlo.

## 6. Segundo anuncio: 60 s con varias funciones (`videos/duo_promo_60/`, 21-oct-2026)
**El primer anuncio (duo_promo) fue solo una PRUEBA (el usuario, 21-oct)**: el de 60 s es el primer comercial real, así que el
gancho presenta la app desde cero (nunca «ya llevamos semanas con…»).
- Antes de escribir: `CHANGES` de index.html (qué trae cada versión) + capturas `guia/*.webp` en una hoja de contacto (PIL, 300 px
  por captura). Ahí salen la barra de pestañas vigente, los nombres de la demo (Ana y Beto) y textos que no están en arreglos.
- Una función por escena y un módulo por escena (`e_intro`, `e_medida`, `e_juegos`, `e_hogar`, `e_ciclo`), todos con tiempo
  global; `escenas.cuadro` elige la cámara por tramo. Cada módulo deja su último estado igual al primero del siguiente
  (p. ej. `e_juegos` arranca con el `home()` de `e_medida`).
- Pantallas que cambian dentro del teléfono: lista `PANTALLAS = [(t, función)]` y deslizamiento de 400 px CSS en 0,32 s.
- Cuando el teléfono queda chico (dos teléfonos, respuestas al lado), mover la cámara para dejar una columna libre (z 0,72) y
  poner allí tarjetas grandes del plano delantero; nunca encima de lo que se está explicando.
- Mundos que no son pantalla (la casa 3D de la app): isométrico propio con `iso()`/`caja()` (3 caras con 0,72/0,88 de luz), HUD
  y dock de la app en pantalla encima, y la cámara cerca (1,3 casa, 2,3 huerto); día-noche = sol/luna en arco + tinte azul.
- Cierre con insignias: `duo.insignia(p, x, y, "apple"|"google", alto)` = genéricas (bolsa / triángulo con el degradado), sin
  arte oficial. Órbita de íconos de las funciones alrededor del logo (detrás/delante según sen(ángulo)).
- Audio: 63 SFX de ElevenLabs (≈ 500 créditos) con `tts_eleven.post` (salta solo a la cuenta de respaldo); Lyria: el candidato
  más corto (58,8 s) se apagaba antes del cierre → elegir el que mantiene volumen en los últimos 3 s aunque dure más.
