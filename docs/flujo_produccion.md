# Flujo de producción, estructura del núcleo y cómo se escribe una escena a medida

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

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

- Evita escenario vacío: el objeto principal de cada fase debe aparecer al empezar su frase
  (`self.B + 0.35` / `self.C + 0.15`); la palabra clave solo lo remarca (rebote, etiqueta).

Tiempos aprox. (RTX 4060): voz ~4 s por toma (x4 tomas por frase), selección ~2-3 min, música ~2.5 min
por 3 min de video, render ~20 min por 3 min (13 procesos; antes de la optimización del 2026-10-04, ver «Velocidad
del render»; cierra `chatterbox_server.py`/`app.py` antes de renderizar para que quepan 12 procesos). Si otro programa ocupa la GPU
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

## Velocidad del render (medido 2026-09-29)
- `boceto.componer` y `motor.a_uint8` usan kernels numba (`FAB_SIN_NUMBA=1` vuelve a numpy). En `gota_bucle` (estilo
  boceto): 145 -> 55 ms/cuadro y render 106 -> 43 s; salida igual (máx. 1 nivel en ~31 px por 75 M).
- Probado y DESCARTADO: fusionar el "over" del `Lienzo` con numba (no gana a OpenCV) y pasar la composición a la GPU
  (la rasterización sigue en CPU; la copia CPU->GPU cuesta lo mismo).
- Lo que sí acelera en escenas del `Lienzo`: no usar `lz.degradado` a pantalla completa (usa bandas: `mundo.degradado_v`),
  evitar `lz.recorte` y rellenos con `alfa<1` en bucles (cada uno compone una región grande), y dibujar solo lo visible.
- Un cuadro de Teotihuacán tarda ~0,3 s con el CPU libre; con 12 procesos, ~5-10 min por 6 min de video.

### Optimización del 2026-10-04 (medida en independencia_mx, 1 hilo por proceso)
- Render real de los mismos 8 segmentos (con su codificación): 1215 s -> 614 s. Memoria medida: 2,14 GB por proceso + su ffmpeg.
- 1229 -> ~650 ms/cuadro (−47 %), salida igual (máx. 1 nivel salvo ~20 píxeles sueltos; 40mil_anos, historia_iran y
  sol_apagado_8min idénticos bit a bit). Kernels numba (FAB_SIN_NUMBA=1 los apaga todos):
  `motor.componer` («over» de cada capa), `kz_ui.gradacion` (0,24 s -> ~16 ms) y grano+viñeta de `efectos.acabado`.
- Mapas: `kz_mapa.base` iba TODO en float64 (por `XY`), lo que mandaba el posproceso a la vía lenta; ahora float32.
  `_clima_global_rejilla`: las gaussianas son separables (cámara sin rotación) -> matmul, 150 ms -> 7 ms por cuadro.
- x264 `slow` -> `medium` (FAB_PRESET): misma calidad medida (SSIM ±0,0003), ~38 % menos CPU de codificación, ~5 % más peso.
  NVENC DESCARTADO: el driver (616) admite ~12 sesiones simultáneas y con 12+ procesos fallaban. Los segmentos guardan su
  preset en `segmentos/info.json`: un render reanudado sigue con el mismo (el concat sin recomprimir no admite mezclas).
- El cuello real era la MEMORIA VIRTUAL de Windows (commit), no el CPU: cada proceso de render + su ffmpeg reserva ~2 GB,
  y `chatterbox_server.py` (~8 GB) y `app.py` (~8 GB) se la comían -> solo cabían 6 procesos (ArrayMemoryError con 8).
  `procesos_seguros` ahora mide el commit libre y lista qué cerrar. Por defecto 12 procesos (Ryzen 7 5700X, 8 núcleos/16 hilos).
  **Procesos dinámicos (6-oct-2026, `render._repartir`)**: arranca con los procesos que caben y cada ~30 s, si se libera memoria
  (otro render o app terminó), agrega uno hasta `--procs`. Si un proceso se queda sin memoria, su segmento vuelve a la cola y baja
  un proceso (antes tumbaba todo el render). Cambiar `render.py` cambia la firma del código: tras tocarlo, `conservar` en el panel.
- El render evita que Windows se suspenda mientras corre (`SetThreadExecutionState`; no cambia la configuración de
  energía). El render v3 de independencia_mx perdió ~13 h con la PC dormida (6 tramos de 48 000 s a la vez en el log).
- Probado y descartado: `FAB_SS=1` (solo −21 % y líneas peores).
- Pendiente posible: `kz_mapa.base` aún cuesta ~0,25 s por cuadro de mapa (muchas operaciones numpy a media resolución;
  candidato a un kernel numba) y `efectos.bloom` ~40 ms.

## Control de calidad (el usuario exige rigor)
- Voz: 36/36 frases con CER 0 en el ejemplo; mira `voz/eval.json`. Whisper escribe "Número seis" como
  "6." (ya normalizado); siglas pueden leerse mal ("ADN" → "Adán"): reescribir.
- Imagen: SIEMPRE revisar hojas de contacto (`escena`, `prueba`) buscando choques de texto, etiquetas
  fuera de cuadro al hacer zoom, dibujos ilegibles, escenario vacío. Corregir antes del render final.
- Audio: `mezcla` imprime LUFS (objetivo −14), pico verdadero (≤ −1 dBTP) y relación voz/fondo (≥ ~11 dB).
  Verificación extra: transcribir la mezcla final con Whisper (debe dar CER ≈ 0).
- Sin parpadeos rápidos a pantalla completa (fotosensibilidad): flashes solo locales.
- `render.py video` reanuda: salta los `segmentos/seg_XXXX.mp4` ya hechos. Para arreglar una toma tras revisar el
  MASTER: `python fab.py <v> video --rehacer 270-280 545-550` (borra y re-renderiza solo los trozos de 3 s que tocan
  esos segundos) y luego `final`. Si cambió el timeline, `segmentos/info.json` lo detecta y borra todos (no sirven).
  Si cambiaste el código de una escena, usa `--rehacer` con su rango: el render no detecta cambios de código.
  **Excepción: escenas hechas con «Escena fluida» de la vista previa del panel** (`docs/panel.md`): sus segmentos
  quedan en `segmentos/` anotados en `segmentos/preview_origen.json` con la firma del código; `render.video` los
  reutiliza si la firma coincide y los borra (se rehacen) si el código cambió (`nucleo/cache_escenas.py`).

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
- `final` borra `video_sin_audio.mp4` pero CONSERVA `segmentos/` (desde 2026-10-04) para arreglar tomas por tramos
  (`video --rehacer t0-t1`). Cuando el video esté aprobado/subido: `python fab.py <v> limpiar` (borra segmentos;
  `--previews` también previews/). FAB_LIMPIAR=1 en `final` los borra de inmediato. Si luego cambias solo el audio,
  `final` remuxa desde el MASTER existente.
- Cuando el video ya es PÚBLICO en YouTube (22-oct-2026): `python fab.py limpiar --publicados` simula y
  `--borrar` borra en todos los públicos los videos (MASTER, segmentos, medios/clips bajados, previews .mp4) y las
  mezclas .wav de audio/. Conserva el proyecto (código, guion, ESTADO, imágenes, .srt, Lyria .mp3, voz .wav);
  registro en `E:\FabricaAnimaciones\_limpieza_publicados.txt`. Los programados a futuro no se tocan.
- **Mover lo pesado a otro disco (4-oct-2026)**: `python nucleo/mover_pesados.py` (simula) / `--aplicar` mueve `videos/<v>/salida*/` a
  `E:\FabricaAnimaciones\videos\<v>\` (FAB_PESADOS cambia el destino; E: = HDD USB «Edson Externo») y deja un **junction** en la ruta
  original, así `fab.py`, el panel y el render no notan nada. Verifica tamaños antes de borrar el original y no mueve lo que esté en
  uso. `--subs segmentos,previews,audio` otras carpetas; `--deshacer salida <video>` lo trae de vuelta. Al producir un video nuevo
  que vaya a ser grande: `python nucleo/mover_pesados.py --aplicar <video>` antes de renderizar. **E: debe estar conectado** o esas
  rutas fallan (un junction roto hace que `os.makedirs("salida", exist_ok=True)` falle). E: es mecánico: no pongas ahí lo que se
  escribe/lee mucho durante la producción (segmentos/ mientras se renderiza, voz/), solo salidas y archivos terminados.
- **5-oct-2026 (C: llegó a 0 GB, el usuario pidió producir en E:)**: se movieron 12,6 GB (`--subs audio,voz,previews,segmentos,clips,salida*`
  de todos los videos; `datos/` e `imagenes/` se quedan en C:). Desde ahora **`fab.py nuevo` crea `salida, segmentos, audio, voz, previews`
  directamente en E:** (junctions; `pesados_a_e` en fab.py). Queda superada la nota de arriba de no poner segmentos/voz en E:: el usuario
  prefiere E: aunque sea mecánico. El Estudio guarda proyectos y vistas en `E:\FabricaAnimaciones\estudio` (`proyecto.DATOS`).
  Si C: se vuelve a llenar, mira también `C:\pagefile.sys` (llegó a 46,8 GB con `app.py`/`chatterbox_server.py` abiertos).
- `musica` ya no guarda pistas separadas (FAB_STEMS=1 si se necesitan, ~300 MB).
- Nombre de los archivos de salida: `ARCHIVO = "..."` en guion.py (si no, se deriva del TITULO).

## Entorno
Python 3.10 del sistema (torch cu124, numpy, opencv, PIL, librosa, numba, faster-whisper, speechbrain,
pyloudnorm). Chatterbox en `C:\chatterbox\repo` (Multilingual v3, `language_id="es"`).
Voces de referencia en `C:\chatterbox_voices` (Dan.mp3 = narrador usado). Whisper large-v3 y ECAPA
en caché de HuggingFace. ffmpeg en `C:\ffmpeg\bin`. Fuentes: Snap ITC (títulos), Segoe UI Black
(subtítulos), Segoe Print (notas). GPU RTX 4060 8 GB, 16 hilos, 34 GB RAM.
Entrega: `salida/*_MASTER.mp4` (1080p, x264 `-crf 18 -preset medium`; crf antes 15, cambiado el 2026-09-29; preset antes slow, cambiado el 2026-10-04) + `.srt`. El usuario YA NO quiere versiones para WhatsApp
(no generarlas salvo que lo pida; existe FAB_WHATSAPP=1). SendUserFile solo llega al móvil si pesa < 30 MB.
