# Brief común para investigar una jugada (lol_final_previa, 10-nov-2026)
Video: previa de la FINAL de la Worlds 2026 (Gen.G vs BLG), estilo análisis táctico (docs/estilo_analisis_tactico.md).
Raíz: C:\FabricaAnimaciones\videos\lol_final_previa  (python 3.10, ffmpeg en C:\ffmpeg\bin, yt-dlp en PATH)

## Qué entregar por jugada <jN>
1. `medios/_fuente/<jN>.mp4`: tramo 1080p con audio del VOD es-MX de la partida (UNA partida = UN video de YouTube),
   ~150 s que empiece ~60 s ANTES de la pelea (contexto) y acabe ~30 s después. Con `python investigacion/cortar.py medios/_fuente <jN>:<vid>:<desde_s>:<dur_s>`.
2. `investigacion/datos_<jN>.md` con el formato de `../lol_semana2/investigacion/datos_blte.md` (léelo: tablas «Reloj», «paso a paso»):
   - VOD id, **K tal que segundo_VOD = HUD + K** MEDIDO leyendo el reloj del HUD (arriba al centro) en ≥ 2 cuadros
     (`python investigacion/hojas.py <archivo> a b paso prefijo` o ffmpeg -ss … -frames:v 1 a 1280 px; mira la imagen con Read).
     Ojo: el VOD tiene pausas técnicas a veces → mide cerca de la jugada. Da también feed − HUD.
   - **K_fuente**: HUD = t_en_<jN>.mp4 + K_fuente.
   - Marcador en la jugada (asesinatos, oro de cada equipo, torres, dragones), leído en el cuadro.
   - Tabla paso a paso cada 1-3 s durante la pelea: t (en <jN>.mp4), HUD, qué se ve (quién está dónde EN EL CUADRO, quién
     usa qué, rótulos del kill feed «X has slain Y», «DOUBLE/TRIPLE KILL», estados STUNNED/AIRBORNE).
   - **Cortes de cámara y repeticiones** dentro del tramo (t de cada corte; las repeticiones NO valen como acción en vivo)
     → lista «Tomas sin corte: a → b».
   - Narración: subtítulos automáticos es (`yt-dlp --skip-download --write-auto-subs --sub-langs es --sub-format vtt -o investigacion/subs/%(id)s <url>`;
     `investigacion/vtt.py` los pasa a texto) → 3-6 citas cortas con su segundo de VOD que expliquen la jugada.
   - Los campeones y K/D/A salen del feed (`investigacion/feed_<id>.txt`, ya hecho: «† jugador/campeón» = murió; reloj del feed ≈ HUD + pocos s).
   - Un párrafo «por qué se gana/pierde la pelea» SOLO con lo que se ve y lo que dicen los narradores. CERO datos inventados.
3. Hoja de contacto `previews/<jN>_hoja.jpg` (4×4 cuadros de la pelea) para que el editor la vea.
4. SOLO si la jugada es 3D (se indica): `investigacion/pistas_<jN>.json` con las posiciones de los 10 campeones en el MINIMAPA
   cada 2-4 s durante ~40 s (desde ~20 s antes de la pelea): {"jugador": {"campeon": "...", "equipo": "azul|rojo",
   "puntos": [[segundo_de_juego_HUD, u, v], ...]}} con u,v = fracción del minimapa (0,0 arriba-izquierda, base azul abajo-izquierda),
   recorte del minimapa en 1080p ≈ x 1640-1916, y 800-1076 (comprúebalo en un cuadro). Haz hojas del minimapa con rejilla de décimas
   (python + cv2) y MIDE A MANO (el rastreo automático falla cuando los iconos se enciman); usa la vista principal para saber quién es
   quién en los grupos. Precisión ±0,03. Donde no hay datos, no inventes. Ejemplo de formato/rigor: `../lol_worlds_2026/j6_3d.py` (docstring y TL).
   Añade objetivos (Barón/dragón con su vida leída), torres caídas y el instante de cada muerte (HUD).

## Reglas
- No toques nada fuera de `videos/lol_final_previa/` (ni nucleo/ ni otros videos). No hagas commit.
- Nombres de archivo exactamente como arriba. Al final responde con un resumen de ≤ 25 líneas por jugada: K, K_fuente,
  tramo de la pelea en <jN>.mp4, tomas sin corte, 3 frases clave de lo que pasa (con HUD) y cualquier duda.
