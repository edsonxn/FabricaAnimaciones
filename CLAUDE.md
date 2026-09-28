# Fábrica de Animaciones — guía para Claude Code

Pipeline propio (Python, todo local) que produce videos animados 2D procedurales con narración
(Chatterbox), subtítulos palabra por palabra, música y efectos de sonido sintetizados y sincronizados.
Ejemplo terminado: `videos/40mil_anos/` (3:00, estilo doodle psicodélico, 12 escenas a medida).

## Reglas para ahorrar tokens (IMPORTANTE)
- **No leas el núcleo completo.** Consulta `API.md` (catálogos + firmas). Si necesitas un detalle:
  `grep -n "def nombre" nucleo/*.py` y lee solo ese rango.
- Para una coreografía nueva, copia patrones de `videos/40mil_anos/escenas.py` buscando la clase
  parecida con grep (p. ej. `grep -n "class Cuenta" -A 60`), no el archivo entero.
- El usuario habla español: responde en español.
- Comandos largos (>~8 KB) fallan en este Windows: escribe archivos con Write/Edit, no con heredocs enormes.
- Usa rutas absolutas o `python fab.py ...` desde `C:\FabricaAnimaciones`.

## Cuando el usuario pide un video nuevo (PROTOCOLO — hazlo siempre, en este orden)
1. **Canal.** `python fab.py yt canales` y pregunta para qué canal es (hoy solo hay uno conectado:
   **Sapiens con Wifi**, alias `sapiens_con_wifi`, `canales/sapiens_con_wifi.json`). Canal nuevo:
   `python fab.py yt conectar` (el usuario inicia sesión en el navegador) + crear `canales/<alias>.json`.
2. **Métricas primero.** `python fab.py yt metricas <alias> 90` y analiza ANTES de proponer nada:
   % visto medio y curva de retención de cada video (¿dónde cae? → intro/gancho/duración), fuentes de tráfico
   (búsqueda vs sugeridos vs navegación), términos de búsqueda, países/edades, qué títulos/miniaturas rinden.
   Compara con el último `canales/metricas/*.json`. Da al usuario 2-4 recomendaciones concretas para el
   proceso y el canal (tema, duración, gancho, estilo, miniatura, frecuencia). Canal con pocos datos
   (<1.000 vistas en 28 días): dilo y apóyate en investigación del nicho (vidIQ/Nexlev si hay créditos).
3. **Preguntas** (AskUserQuestion, con tu recomendación primero): tema (3 ideas basadas en métricas y
   búsquedas), estilo visual, duración, formato (largo o Short vertical), voz (Dan por defecto) y cuándo
   publicar (por defecto el siguiente hueco del horario del canal, abajo). Nunca versiones para WhatsApp.
4. **Producir** (flujo de abajo) → miniatura (2-3 variantes) → `youtube.json` (título ≤ 50 caracteres con
   la palabra clave al inicio; descripción con capítulos reales del timeline, fuentes, enlace a otro video
   del canal y 3 hashtags; 15-25 etiquetas ≤ 450 caracteres) → `yt subir ... --publicar <ISO>`.
   Publicar o hacer público = confirmarlo con el usuario (programar lo que él pidió está bien).

## Horario de publicación (investigado 2026-09-28; revisar con métricas propias)
- Audiencia objetivo: México/Latinoamérica (+ España). Videos largos: **miércoles a viernes 14:00 CDMX
  (20:00 UTC)** = 15:00 Bogotá/Lima, 17:00 Buenos Aires, 22:00 Madrid; alternativa sábado/domingo 10:00 CDMX
  (16:00 UTC). Regla: publicar 1-2 h antes del pico de la audiencia. Shorts: 18:00-21:00 locales.
- Constancia > hora exacta: 1-2 videos por semana el mismo día/hora. Programa con `--publicar` (UTC).
- Cuando el canal tenga datos, pide al usuario la gráfica "Cuándo están conectados tus usuarios" de
  YouTube Studio > Estadísticas > Audiencia (no está en la API) y ajusta `horario` en `canales/<alias>.json`.

## Estructura
```
fab.py                  lanzador de todas las etapas (ver abajo)
API.md                  referencia generada (python fab.py api)
nucleo/                 motor reutilizable (NO específico de ningún video)
  config.py             lee guion.py del video + valores por defecto
  estilos.py            6 estilos visuales intercambiables
  motor.py              lienzo 2x supersampleado, trazos "boil", texto, composición (sticker/tiza/neón)
  dibujos.py            personajes (cave/tu/neander) y ~40 objetos dibujados por código
  fondos.py             15 fondos procedurales (psicodélicos, pizarra, kraft, plano, cueva, synthwave...)
  efectos.py            tomas raras (ojo_pez, caleido, warhol, droste, espejo, planeta...) + 12 transiciones
  escena_base.py        Escena, Item, helpers (chip, flecha...), ICONOS, escenas genéricas
  tts_gen.py / tts_select.py / qa.py      voz: generación, selección con Whisper+ECAPA, alineación
  linea_tiempo.py / ritmo.py              timeline.json (fuente única de verdad) y bombos compartidos
  sinte.py / musica.py / sfx.py / mezcla.py   síntesis, música por escena, efectos, mezcla y máster
  render.py / final.py                    render paralelo -> MASTER + WHATSAPP + .srt
videos/<nombre>/        un video = guion.py + escenas.py (+ datos generados)
  voz/ timeline.json audio/ segmentos/ previews/ salida/
videos/_plantilla/      punto de partida (escenas genéricas: funciona sin programar coreografía)
```

## Flujo para un video nuevo
1. `python fab.py nuevo <nombre>` → edita `videos/<nombre>/guion.py` (el docstring explica todos los campos).
   - Investiga y verifica los datos; pon `dato` y `fuente` reales. Números en PALABRAS en las frases.
   - Ítems de lista: `num`, `titulo` y 3 frases ("Número N: <titulo>", fase A, fase B).
   - Elige `ESTILO_VISUAL`, `DURACION` (o None), `TRANSICIONES`, `MUSICA` (opcionales).
2. `python fab.py <nombre> voz` → `python fab.py <nombre> seleccionar`
   (si imprime REGENERAR: `python fab.py <nombre> voz --seeds 5 6 7 8 --solo <keys>` y volver a seleccionar;
   si una frase falla siempre, reescríbela. `fab.py <nombre> todo` hace estas rondas solo.)
3. `python fab.py <nombre> tiempo` → timeline.json (BPM y escenas en tiempo fuerte).
4. Escenas: la plantilla ya genera todo con `ItemGenerico` etc. Para coreografía a medida, crea clases en
   `escenas.py` (heredan de `Item`/`Escena`) y regístralas en `PROPIAS`. Revisa con
   `python fab.py <nombre> escena <id> t1 t2 ...` y **mira la imagen** `previews/esc_<id>.jpg`.
5. `python fab.py <nombre> prueba t1 t2 ...` (cuadros finales con transiciones y subtítulos).
   Antes del render largo: `python fab.py <nombre> comprobar` (nombres sin definir, anclas, un cuadro por
   fase; tarda segundos y evita que un NameError tumbe el render a los 10 minutos).
6. `python fab.py <nombre> musica` → `sfx` → `mezcla` → `video` → `final`
   (o `python fab.py <nombre> todo` para todo en orden). Salida en `videos/<nombre>/salida/`.
7. `python fab.py <nombre> verificar`: Whisper frase por frase sobre la mezcla final (CER), duración y
   desfase A/V del MASTER y `previews/final_hoja.jpg` (MÍRALA). Reporta estos números al usuario.
8. Miniatura: `videos/<nombre>/miniaturas.py` con `VARIANTES = {nombre: fn(lz) -> fondo}` (ejemplo en
   `videos/40mil_anos/miniaturas.py`) → `python fab.py <nombre> miniatura` → `salida/*_mini_<variante>.jpg`
   (1280x720) y `previews/miniaturas.jpg` (MÍRALA: incluye la vista a tamaño de celular). En el nicho funciona:
   personaje grande con cara de sorpresa, 1-3 palabras enormes amarillas con contorno negro, alto contraste.
   Usa `ojos="abiertos"` (a un T fijo el parpadeo automático puede cerrar los ojos).
   Metadatos de YouTube del video en `videos/<nombre>/youtube.json`; datos del canal en `canales/*.json`.
9. YouTube (`nucleo/youtube.py`, portado de RemoGravity; cliente OAuth en `canales/youtube_client_secrets.json`,
   tokens en `canales/tokens/`): `python fab.py yt ayuda`. Canal por alias = nombre de `canales/<alias>.json`
   (p. ej. `sapiens_con_wifi`). `yt videos <canal>`, `yt metricas <canal> [dias]`, `yt aplicar <video> <canal> <id>` (metadatos + miniatura +
   .srt a un video ya subido, sin cambiar su visibilidad), `yt subir <video> <canal> [private|unlisted|public]
   [--publicar ISO]`, `yt publicar <canal> <id> [public|unlisted|private] [--programar ISO]`, `yt canal <alias>` (descripción, palabras clave, idioma, país, banner). Nombre y foto de
   perfil del canal NO se pueden cambiar por API (Studio). Publicar o hacer público = preguntar antes.
   Arte del canal: `python canales/arte_canal.py "NOMBRE" "lema"` → `canales/arte/` (revisar `*_revision.jpg`).
- Evita escenario vacío: el objeto principal de cada fase debe aparecer al empezar su frase
  (`self.B + 0.35` / `self.C + 0.15`); la palabra clave solo lo remarca (rebote, etiqueta).

Tiempos aprox. (RTX 4060): voz ~4 s por toma (x4 tomas por frase), selección ~2-3 min, música ~2.5 min
por 3 min de video, render ~20 min por 3 min (13 procesos). Si otro programa ocupa la GPU
(p. ej. un `chatterbox_server.py` del usuario), la voz puede ir 5-8x más lenta: no lo mates, avisa.

## Cómo se escribe una escena a medida (lo esencial)
- `preparar()` / `escena()` (en Item): calcula anclas con `self.w("palabra")` (tiempo en que se dice;
  `fin=True` = cuando termina; `frase=i`; `n=` enésima aparición; KeyError si no existe) y registra
  sonidos con `self.ev(t, "nombre_sfx", vol, pan, tono=, dur=)`.
- `dibujar(lz, t)` (Escena) o `antes(lz, t)` / `hoy(lz, t)` (Item, fases A/B). Todo es función del tiempo
  global `t`; usa `pop(t, t0)`, `sale(t, t0)`, `prog(t, a, b)`, `e_out/e_inout/e_back`.
- Fases de Item: `self.A` (título), `self.B` (inicio fase A), `self.C` (inicio fase B; `fase_b` en guion = índice
  de frase que la abre, para ítems de 4+ frases). `ANTES_PERSISTE = True`
  mantiene lo de la fase A dibujado durante la fase B.
- Cámara: `camara(t) -> (zoom, rot, dx, dy)`. Fondo: `fondo(t)` / `fondo_antes` / `fondo_hoy`
  (por defecto los del estilo: `fondo_estilo("antes", t, pal, pulso)`).
- Tomas raras: `self.post_fx(t_ini, t_fin, lambda img, t, u: E.caleido(img, 6, t, u))` (u = rampa 0..1).
- Capas del lienzo: 0 = pared (sin borde), 1 = stickers (defecto), 2 = encima (partículas, destellos).
  `with lz.grupo(x, y, s, rot):` transforma; `with lz.capa(2):` cambia de capa.
- Texto que no debe distorsionarse con un post-efecto (espejo, warhol): dibújalo en `ui(lz, t)`.
- Zona segura: encabezado arriba-izq (y≈62), sello arriba-der, tarjeta dato (y≈150-240), subtítulos
  abajo (y≈950-1040), barra de progreso arriba al centro. El escenario útil es y≈260-900.

## Estilos visuales (`ESTILO_VISUAL` en guion.py o `set FAB_ESTILO=...` para probar)
doodle_psicodelico · pizarra · cuaderno · neon · recortes (con stop-motion `fps_mov`=15 y fondo `cartulina`
por escena según `PAL`) · limpio. Un estilo cambia tinta, rellenos,
temblor, borde sticker, sombra, textura (tiza), brillo (neón), grano y fondos por defecto — sin tocar la
coreografía. Ver `python fab.py <video> estilos <t>` (mismo cuadro en todos) y `catalogo` (íconos).
Nuevo estilo: copiar una entrada de `nucleo/estilos.py` y ajustar. Nuevo fondo: función en `fondos.py`
+ registrar en `FONDOS`. Nueva transición: `tr_x(A, B, p, seed)` en `efectos.py` + `TRANSICIONES`.
Nuevo sonido: `s_x(**k)` en `sfx.py` (se registra solo). Nuevo sabor musical: rama en `musica.componer`
+ entrada en `musica.PROG` y `config.SABORES`.
Tras cambiar el núcleo: `python fab.py api` y re-verificar `videos/40mil_anos` (no debe cambiar).

## Estilo Kurzgesagt y plano secuencia (ejemplo: `videos/sol_apagado/`, 1:00)
- `ESTILO_VISUAL = "kurzgesagt"`: sin contornos (los trazos NEGRO no se dibujan; usa `plano.TINTA` si quieres
  una línea oscura), sin temblor, bloom de lo luminoso y saturado. Dibuja con `nucleo/plano.py`: `esfera`,
  `sol`, `tierra` (continentes que giran, `luz`, `ciudades`), `luna`, `pajaro`, `microbio`, `arbol`, `fumarola`,
  `termometro`, `onda` (frente de onda), `discontinua`, `rotulo`/`pastilla` (fuente `geo` = Poppins).
- Lienzo nuevo: `with lz.recorte(pts):` (clip), `lz.degradado(pts, c0, c1, p0, p1)`, `lz.halo(x, y, r, color)`.
- Fondos `espacio` (estrellas con paralaje dx/dy) y `degradado`; `F.estrellas(img, t, brillo)` sobre cualquier fondo.
- Sabores musicales documental: `espacio`, `tension`, `vacio`, `esperanza` (sin bombo; cierre suave).
- **Plano secuencia (sin cortes)**: `TRANSICIONES = [("continua", 0.1)] * n` y en escenas.py una sola clase
  (`Mundo`) para todos los ids que dibuja el mundo en función del t global; las escenas solo marcan narración y
  música. Anclas entre escenas con `T(id, palabra)`. Transformaciones usadas: zoom a la Tierra cuyo borde se
  aplana en horizonte (clase `Sup`: paisaje doblado con curvatura 1/radio), paneo continuo, brillo que llena la
  pantalla y se encoge convertido en otro objeto. Registra los sfx solo en la instancia `idx == 0`.
- `MEZCLA = dict(musica=-21.5, sfx=-22.5)` en guion.py baja el fondo cuando la narración es casi continua.

## Control de calidad (el usuario exige rigor)
- Voz: 36/36 frases con CER 0 en el ejemplo; mira `voz/eval.json`. Whisper escribe "Número seis" como
  "6." (ya normalizado); siglas pueden leerse mal ("ADN" → "Adán"): reescribir.
- Imagen: SIEMPRE revisar hojas de contacto (`escena`, `prueba`) buscando choques de texto, etiquetas
  fuera de cuadro al hacer zoom, dibujos ilegibles, escenario vacío. Corregir antes del render final.
- Audio: `mezcla` imprime LUFS (objetivo −14), pico verdadero (≤ −1 dBTP) y relación voz/fondo (≥ ~11 dB).
  Verificación extra: transcribir la mezcla final con Whisper (debe dar CER ≈ 0).
- Sin parpadeos rápidos a pantalla completa (fotosensibilidad): flashes solo locales.
- `render.py video` reanuda: borra `segmentos/seg_XXXX.mp4` afectados para re-renderizar solo esos.

## Modelos (no borrar)
- `~/.cache/huggingface/hub` guarda Chatterbox (~3 GB) y Whisper large-v3 (~3 GB). Si se borra (p. ej. al
  liberar espacio), la etapa `voz` los vuelve a bajar (~1.4 MB/s ≈ 40 min) y puede quedarse trabada:
  si un `.incomplete` no crece en 1-2 min, detén solo tus procesos (`tts_gen`) y relanza; HF retoma.
- `modelos/ecapa` (similitud de voz) son enlaces a esa caché: si están rotos, bórralos y se regeneran.

## Disco (C: suele estar casi lleno)
- Antes de producir, revisa espacio: `powershell -Command "[math]::Round((Get-PSDrive C).Free/1GB,2)"`.
  Un video de 3 min necesita ~1.5 GB temporales (segmentos ~470 MB + video sin audio ~470 MB + MASTER ~500 MB).
  Con < 2 GB libres, avisa al usuario antes de renderizar (un disco lleno corta la escritura: p. ej. un
  .wav de 80 bytes = toma rota; bórrala y reanuda).
- `final` borra solos `segmentos/` y `video_sin_audio.mp4` al terminar (FAB_CONSERVAR=1 para mantenerlos);
  si luego cambias solo el audio, `final` remuxa desde el MASTER existente.
- `musica` ya no guarda pistas separadas (FAB_STEMS=1 si se necesitan, ~300 MB).
- Nombre de los archivos de salida: `ARCHIVO = "..."` en guion.py (si no, se deriva del TITULO).

## Git / GitHub
- Repo privado (remoto `origin`). Se versiona solo código y configuración (ver `.gitignore`): núcleo, docs,
  `canales/*.json`, arte del canal y por video `guion.py`, `escenas.py`, `miniaturas.py`, `youtube.json`,
  `timeline.json`. NUNCA subir `canales/youtube_client_secrets.json`, `canales/tokens/`, métricas, respaldos,
  voz/audio/render ni `proyecto/`. Antes de cada commit: `git status` y revisa que no entre ningún secreto.
- Al terminar un cambio que funcione: commit en español describiendo qué y por qué; `git push`.
- Sesiones en la nube (claude.ai/code) sirven para guion, escenas, investigación y metadatos, pero NO tienen
  GPU, Chatterbox, voces, Whisper, ffmpeg ni fuentes: voz, música y render siempre en esta PC
  (`git pull` y luego `python fab.py <video> todo`).

## Entorno
Python 3.10 del sistema (torch cu124, numpy, opencv, PIL, librosa, numba, faster-whisper, speechbrain,
pyloudnorm). Chatterbox en `C:\chatterbox\repo` (Multilingual v3, `language_id="es"`).
Voces de referencia en `C:\chatterbox_voices` (Dan.mp3 = narrador usado). Whisper large-v3 y ECAPA
en caché de HuggingFace. ffmpeg en `C:\ffmpeg\bin`. Fuentes: Snap ITC (títulos), Segoe UI Black
(subtítulos), Segoe Print (notas). GPU RTX 4060 8 GB, 16 hilos, 34 GB RAM.
Entrega: `salida/*_MASTER.mp4` (1080p) + `.srt`. El usuario YA NO quiere versiones para WhatsApp
(no generarlas salvo que lo pida; existe FAB_WHATSAPP=1). SendUserFile solo llega al móvil si pesa < 30 MB.
