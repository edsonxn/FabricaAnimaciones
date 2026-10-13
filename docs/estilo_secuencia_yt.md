# Estilo SECUENCIA YT — gameplay de YouTube por beat (Crónicas de Warcraft; luego Tamriel y Runa Caída)

Creado el 13-oct-2026 en la mudanza desde `C:\googleimagenes` (`docs/migracion_googleimagenes.md`).
Motor: `nucleo/secuencia_yt.py` (fuente de medios) + `nucleo/secuencia.py` (beats y armado de siempre).

## Flujo
```
python fab.py nuevo <v> --yt          plantilla videos/_plantilla_yt (VOZ Applio Remy, SECUENCIA fuente="yt", LYRIA épica)
python fab.py <v> voz | seleccionar | tiempo
python fab.py <v> beats               cortes en pausas reales, ~8,6 s (clip_s)
python fab.py <v> busquedas           crea busquedas.json vacío y lista los beats; Claude escribe una búsqueda por beat; repetir valida
python fab.py <v> bajar [-j 4]        busca (ytsearch), elige tramo, baja SOLO ese tramo (≤1080p, ≥720p) y lo corta a medios/scene-NNN.mp4
python fab.py <v> medios              hojas previews/medios_NN.jpg — MIRARLAS
python fab.py <v> bajar 12,15-17 --rehacer        otro tramo/candidato
python fab.py <v> bajar 12 --q "Thunder Bluff"    otra búsqueda solo para ese beat
python fab.py <v> bajar 12 --url https://youtu.be/ID --desde 312   video y segundo exactos
python fab.py <v> fuentes             beat → video/canal/segundo; salida/creditos.txt para la descripción
python fab.py <v> video [--tramo a-b]  arma con transición slideleft (0,35 s)
```
Velocidad medida: 4 clips en 37 s con `-j 4` (≈ 100 clips de un video de 15 min ≈ 15 min).

## Cómo escribir busquedas.json (lecciones heredadas del sistema viejo)
- **2-4 palabras, en INGLÉS, nombre propio primero**: «Thunder Bluff», «Thrall Orgrimmar», «Kith'ix raid».
- **Nunca varios nombres propios juntos**: YouTube devuelve CERO (probado: «Ratchet centaur chase Barrens»).
- Lista = respaldos en orden: `["Kith'ix raid", "Unbinding of Kithix", "WoW raid boss fight"]`. Lo recién salido
  (parche de esta semana) tiene pocos videos: pon siempre un respaldo genérico.
- El sufijo `World of Warcraft` se añade solo (salvo que la búsqueda ya diga WoW).
- `{"url", "desde"}` para lo que hay que enseñar sí o sí (la captura del tema, un jefe concreto).
- Búsquedas iguales en beats seguidos: el motor toma otro tramo, pero mejor variar el plano.

## Filtros automáticos (`_apto`, `_juzgar`)
- Duración del video 90 s – 240 min; fuera títulos con reaction/podcast/tier list/news/shorts; `evitar_canales`.
- Tramo dentro del 12 %–88 % del video (sin intros ni outros), sin repetir tramo del mismo video (±L+20 s) y los
  videos de beats cercanos pasan al final de la cola.
- Rechaza clip **oscuro** (luz media < 0,07), **quieto** (menús, pantallas de carga) y **webcam de streamer**: cara
  Haar que se queda fija (±12 px) en ≥ 3 de 4 cuadros fuera del centro. El tono de piel NO sirve (la madera tauren da
  94 % «piel», probado 13-oct); lo que distingue la webcam es que no se mueve con la cámara del juego.
- Sin audio: se baja solo la imagen (`ambiente=0`).

## Lo que la revisión de la hoja tiene que cazar (los filtros no lo ven)
Otro juego u otra expansión que no toca, texto/logos de otro canal encima, fan-art estático de videos de lore,
interfaz recargada que tape el sujeto, el sujeto equivocado (otra raza/zona). Se rehace con `--rehacer` o `--q`.

## Pendiente del estilo
Apoyos (tooltips Wowhead, tarjetas), 3 motion graphics por video, segmento Overgear y la vista «Montaje» del panel.
