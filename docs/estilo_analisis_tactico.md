# Estilo ANÁLISIS TÁCTICO — una jugada explicada «como en la NFL» (esports / deportes)

Creado el 26-oct-2026 como prueba sin canal (`videos/lol_worlds_tl_al/`: el Barón de Team Liquid en la Worlds 2026 de
League of Legends). Pedido del usuario: «analice jugadas, repeticiones, como esos análisis de la NFL con efectos 3D,
flechas… haciendo pausas, dibujando flechas, rutas, elementos, mapa, todo para entender la jugada».

## Receta
1. **Elegir la jugada con datos**: resumen de YouTube → hojas de contacto (1 cuadro/15 s) → la secuencia decisiva.
   Los resúmenes SE SALTAN tramos (40:28 → 41:42 en el ejemplo): la jugada se corta del **VOD completo**. Con el reloj
   del juego en pantalla se saca el desfase (segundo del VOD = reloj + N) y se baja UN tramo de 2-3 min en 1080p
   (`ffmpeg -ss` sobre la URL de `yt-dlp -g`, video + audio) a `medios/_fuente/jugada.mp4`.
2. **Entender la jugada**: transcripción de la transmisión (`get_video_transcript` del VOD) para lo que pasa fuera de
   cámara + marcador (oro, asesinatos, torres) + minimapa (`previews/minimapas.png`: recorte del minimapa en cada momento).
   Los picks, de la descripción del VOD. Cero datos inventados: todo dato del guion sale de la transmisión.
3. **Guion** ~2 min: gancho con el final de la jugada → «vamos a rebobinar» → contexto (marcador en el tablero) →
   pausas con telestrador → tablero con el «por qué» (rotaciones, oleadas, visión) → desenlace en cámara lenta →
   la lección + pregunta. Voz ElevenLabs con corchetes (ejemplo: JC «Energetic News Broadcaster»).
4. **Montaje con UN solo clip** (motor SECUENCIA YT): `beats` normal, `medios/scene-NNN.jpg` de relleno, y TODO el
   cuadro lo pone el FX `video` del clip fuente: `vel=1` juega, `vel=0` congela (pausa), `vel<0` rebobina, `vel<1`
   cámara lenta. Helper `J(de, a, desde, vel)` en `efectos.py`.
5. **Kit `nucleo/mg_tactica.py`** (tiempos ABSOLUTOS de la voz):
   - `pizarra(de, elementos, "PAUSA", "40:16")` sobre el cuadro congelado: `anillo` en el suelo bajo cada jugador (borde
     que se traza + onda + etiqueta con línea guía), `flecha` que se dibuja sola (Catmull-Rom, discontinua para
     «llega tarde»/intención), `zona`, `texto`, `foco` (oscurece todo menos los anillos). Chip «❚❚ PAUSA · reloj».
     Posiciones: cuadro con rejilla (`previews/cuadros/g<t>.jpg`), el anillo va a los PIES, no a la barra de vida.
   - `tablero(de, mapa, elementos, camara, titulo, reloj, hud, iconos)`: mapa oficial (Data Dragon `map11.png`) en un
     plano girado 40° con cámara (zoom/paneo por fases), `ficha` con el icono REAL del campeón que sigue una ruta
     con tiempos, `oleada`, `tp` (arco punteado + remolino), `ward` (ojo + visión), `niebla`, `num` (pasos 1-2-3),
     HUD de píldoras con fin opcional.
   - `chip(...)` (píldora suelta: «REPETICIÓN», «-2 DESTELLO» con icono del hechizo) y `rebobinar()` (rayas de cinta).
6. Sonido: música de la biblioteca (`biblioteca sugerir`), SFX de la biblioteca (`biblioteca sfx usar`): golpe + clic en
   cada pausa, rebobinado, swoosh al entrar al tablero, pop en cada etiqueta, subida antes del momento clave.

## Voz: pronunciación de nombres en inglés (el usuario, 26-oct-2026)
- En la prueba la voz dijo «Liquid» a la española; se pronuncia **«Lícuid»**. En TODO video de este estilo, `FONETICA` en
  `guion.py` con los nombres de equipos y jugadores en inglés: config.py la aplica también a ElevenLabs (`FRASES_TTS`) y el
  guion conserva la grafía real para el .srt. Punto de partida (revisar oyendo): `"Team Liquid": "Tim Lícuid"`,
  `"Liquid": "Lícuid"`, `"Anyone's Legend": "Éniuans Léyend"`, `"Gen.G": "Yen yi"`, `"Dplus KIA": "Di plus Kía"`,
  `"Bilibili Gaming": "Bilibili Guéiming"`, `"Top Esports": "Top I spórts"`, `"Movistar KOI": "Movistar Koi"`,
  `"Hanwha Life": "Janjua Laif"`, `"Karmine Corp": "Karmin Corp"`, `"Cloud9": "Claud náin"`, `"Worlds": "Uórlds"`.
  Whisper sigue comparando contra la grafía real: sube `CER_MAX_POR_FRASE` donde haga falta tras leer la transcripción.

## Velocidad de render (optimizado el 26-oct-2026)
- Primera versión: ~0,9 s/cuadro (pausas ~0,8 s, tableros ~1,2 s, niebla 2,5 s): 2 min de video ≈ 40 min en un proceso.
- Ahora: **~60 ms/cuadro de media** (tableros 50-100 ms, pausas 70-110 ms, clip solo 12 ms). Claves: `_sobre` y el `_pegar`
  del motor trabajan solo en el recuadro con alfa (`cv2.boundingRect`), copia directa si la capa es opaca y `cv2.blendLinear`
  en vez de numpy; el mapa se deforma sobre el fondo con `BORDER_TRANSPARENT` (sin máscara); niebla a 1/4 de resolución;
  centinelas en parche local; el foco es la capa de ABAJO de la pizarra (antes apagaba también las flechas).
- Regla: nada de capas de 1920×1080 por elemento; dibuja en un parche del tamaño del elemento.
- Videos largos (18 min ≈ 32 000 cuadros ≈ 30 min a 60 ms): además, render en tramos paralelos
  (`fab.py <v> video --tramo a-b --salida salida/par_k.mp4` ×6 + `ffmpeg -f concat -c copy` → `salida/video_sin_audio.mp4`
  → `final`). El script de la prueba: 6 procesos subieron la CPU de 23 % a 97 %.

## Errores a no repetir (primera prueba)
- `tv`, `zoom`, `oscurecer`, `desaturar` del motor se aplican ANTES del FX `video`: con el clip a cuadro entero NO se ven.
  Por eso el foco y el rebobinado viven en el kit.
- Tablero amontonado: con fichas grandes y 10 nombres no se lee nada. Fichas chicas, nombre SOLO de quien nombra la voz,
  zoom de cámara en cada fase, y todo elemento con `sale` cuando ya no se habla de él (también las píldoras del HUD).
- Etiquetas en capa aparte encima de las fichas (si no, las fichas las tapan).
- La flecha de una intención (flanco) se dibuja ANTES de que las fichas se muevan.
- Whisper rechaza tomas buenas por los nombres («varón» por Barón, «John» por Yeon): `CER_MAX_POR_FRASE` tras leer la transcripción.

## Gráficos de transmisión: `nucleo/mg_lol.py` (el usuario, 27-oct-2026, `lol_worlds_2026`)
- Las píldoras `mg_tactica.chip` sobre el gameplay «se ven muy básicas, poco impresionantes»: en este estilo NO se usan solas.
  Se edita como Warcraft/Tamriel/Runa (docs/estilo_secuencia_yt.md § PEGATINAS y § MOTION GRAPHICS NUEVOS): pegatina real casi en
  cada frase (fotos oficiales de jugadores y arte de campeones), MG propios del guion que entran por partes con la voz, nada
  quieto > 2 s, y el gancho (primeros 30-45 s) cargado de MG.
- Kit `mg_lol`: `tarjeta` (tercio inferior de vidrio con filo dorado, logo, barrido, giro 3D que respira), `pegatina`,
  `resultados`, `caida`, `eliminado`, `apertura`, `versus`, `menu`, `suiza`. Hoja de prueba: `videos/lol_worlds_2026/_prueba_mg_lol.py`.
- Recursos oficiales: logos y fotos de jugadores con la API pública de LoL Esports (`esports-api.lolesports.com/persisted/gw/
  getTeams`, clave pública de la web; las URL `http://static.lolesports.com` redirigen: bajarlas por HTTPS o salen HTML);
  arte de campeones de Data Dragon (`cdn/img/champion/splash/<C>_0.jpg` y `loading/<C>_0.jpg`).

- **Durante el análisis de una jugada (el usuario, 27-oct-2026):** flechas, rutas y zoom; tarjetas y pegatinas CHICAS y en los bordes
  (esquinas o sobre el marcador de abajo) para no tapar la jugada. Fuera del análisis (gancho, resúmenes) sí van grandes.

- **MG nuevos (27-oct-2026, tramo 3 de `lol_worlds_2026`)**: `ficha_jugador(foto, nombre, logo, n, stats)` (top de jugadores:
  foto que sube, «N.º k», barras de estadística que se llenan con la voz), `ranking(titulo, filas)` (puestos en rombo dorado),
  `tabla(titulo, columnas)` (equipos por récord: 2-0 | 0-2), `calendario(titulo, hitos)` (línea de fechas, la final con halo),
  `barras(titulo, items, total)` (picks: «12 de 29») y `resultados` con ganador None = cruce por jugar («VS» o la fecha).
  Hoja: `videos/lol_worlds_2026/_prueba_mg_nuevos.py` → previews/mg_lol_nuevos.jpg.

## Zoom en la pausa y en la cámara lenta (27-oct-2026)
- El FX `video` acepta `zoom=(z, cx, cy)` (centro en fracción del cuadro fuente), `zoom0` (inicio; por defecto sin zoom),
  `zoom_en` y `zoom_dur`: acercamiento animado, también con el clip congelado o en cámara lenta. Para mantenerlo en el
  siguiente tramo, `zoom0 = zoom`; para salir, `zoom0 = (z, cx, cy)` y `zoom = (1, .5, .5)`.
- La pizarra NO se transforma: si una pausa lleva zoom, mide anillos y flechas sobre el cuadro ya acercado (rejilla con el mismo
  recorte). En el resumen de la Worlds el zoom se usó en las cámaras lentas (1,28-1,45) y las pausas quedaron a cuadro entero.

## Verificar cada frase con el MARCADOR y el VOD, no con el resumen (27-oct-2026)
- Los resúmenes oficiales PEGAN momentos distintos y la narración se monta encima: en DK-T1 el «Goodbye Lucid» era del 37:08
  y la pelea del Anciano del 40:25 (Lucid vivo). El guion decía «con uno menos»: falso. Antes de analizar una jugada, lee el
  RELOJ del juego en cada cuadro de la hoja de contacto (un salto de reloj = corte del resumen) y los subtítulos del VOD completo.
- El marcador dice más que los narradores: la fila de dragones (de qué lado están) desmintió «Hanwha aseguró el alma»
  (eran los 4 dragones de IG); la diferencia de oro a lo largo de la partida desmintió «KOI acababa de ganar una pelea».
- Corregir una frase sin mover el resto: regenerar solo esa frase (`voz` detecta el texto cambiado), `seleccionar`, `tiempo`,
  y si la escena pierde/gana un compás, `"post": s` en esa escena del guion para que conserve sus compases.
- El FX `cierra` sin `a` deja el video en NEGRO hasta el final: entre secciones, `cierra` con `a` + `abre`.

## Pendiente
- Zoom con la pizarra transformada (hoy la pizarra se mide sobre el cuadro ya acercado).
- Audio de los comentaristas/estadio bajo la voz en los tramos que juegan (FX `video` no lleva audio a la mezcla).
- Tablero de otros juegos/deportes: solo cambia el mapa (cancha, campo) y los iconos.
