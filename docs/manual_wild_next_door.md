# Manual rápido: un video de Wild Next Door de principio a fin

_Creado el 11-oct-2026 (video `arana_techo`) a pedido del usuario: para que un agente en una conversación nueva sepa en
minutos qué hacer, sin repetir la exploración. Léelo entero (≈ 5 min); el detalle técnico vive en
`docs/estilo_secuencia_flow.md` (consúltalo por sección, no entero)._

## SIGUIENTE VIDEO: propuesta y receta rápida (el usuario, 11-oct-2026: «menos tokens y más rápido»)
**Tema propuesto: «5 House Bugs You Should Never Kill (And 1 You Should)»**, de unos 9 min. Es la hipótesis 2 de
`canales/formula/wild_next_door.md`: el mismo empaque «Never Kill» y una sola variable nueva, la estructura en LISTA
(Curious Kids Discover ×72 con «5 Animals You Shouldn't Kill Around Your House»). Bichos sin video propio todavía:
- araña saltarina;
- avispa alfarera (mud dauber, caza viudas negras);
- mariquita;
- tijereta;
- crisopa;
- el «1 you should»: la chinche de cama o la araña reclusa parda, con aviso de seguridad.

Confirma antes con `python fab.py ideas wild_next_door --actualizar`. Si aparece un atípico nuevo «Never Kill X» con × alto,
gana el tema de un solo bicho. Hueco: el último programado + 3 días a las 16:00 UTC (después del 18-oct toca el 21-oct).

**Qué gastó más tokens y tiempo en `arana_techo` y cómo evitarlo:**
| Paso | Qué pasó | Cómo hacerlo ahora |
|---|---|---|
| Investigar qué funciona | detalles, miniaturas y transcripción de 5 videos (~30 llamadas) | leer `canales/formula/wild_next_door.md` + `ideas`; investigar a fondo SOLO un atípico nuevo |
| Guion | partir de una plantilla en español con plastilina | copiar `videos/arana_techo/guion.py` (ya trae EnglishComic, `clips_s`, FICHA, LYRIA de 4 tramos) |
| Prompts | 110 prompts a mano y 11 rehechos por rótulos y marcos | copiar `videos/arana_techo/hacer_prompts.py` (ya trae `NOTXT`, `EDGE` y fichas de secundarios); proponer `img_s=5` y `img_s_lento=6` (~85 beats en vez de 110 = menos prompts que escribir y revisar) |
| Flow, espera | decenas de llamadas al navegador con pausas de 10 s y capturas | esperar con un bucle de PowerShell sobre `curl 127.0.0.1:8791/estado` (cero llamadas al navegador); capturas solo para ajustar el selector |
| Flow, clips | flowscrap saltó a 720p; 3 clips a mano y 3 descargas pidiendo permiso | al empezar, pedir al usuario permiso para TODAS las descargas de clips del video de una vez; si flowscrap salta a 720p, a mano directo (manual § «Errores») |
| `servir` | reiniciarlo a mitad del lote corrió los clips | arrancarlo UNA vez con 90 min (`servir 90`) y cambiar los prompts antes de lanzar, no durante |
| Marcos de clips | medidos a mano, 2 vueltas de armado | `python ../../nucleo/marcos_clips.py` → pegar su `recorte_por` ANTES del primer `video` |
| Música | Lyria con silencios en las uniones y un tramo largo | `lyria_tramos.py` ya recorta los silencios solo; si un tramo sale fuera de ±12 %, borrar ese mp3 y volver a correrlo |
| Cierre | `final` falló porque el MASTER estaba abierto | pedir al usuario que cierre el reproductor antes de `final`; encadenar `video; mezcla; final; verificar` en UN comando en segundo plano |

**Orden recomendado (una sola pasada):** formula + `ideas` → UNA pregunta al usuario (tema, saldo de Flow, permiso de
descargas) → guion → `_ronda.py` (voz en segundo plano) → mientras tanto, miniatura en Flow (prueba el puente) →
`beats` + `hacer_prompts.py` + `prompts` → clips (prueba con el 1, luego el resto) → imágenes (8 de prueba y el resto) →
mientras tanto, `lyria_tramos.py` y `youtube.json` → `medios` (revisar hojas, una ronda de rehacer) → `marcos_clips.py` →
`video; mezcla; final; verificar` → revisar el MASTER → subir con `--publicar`.

## El canal en 6 líneas
- Alias `wild_next_door`, canal **en INGLÉS** (audiencia de EE. UU.). Tema: bichos y animales de tu casa y jardín, con el
  giro «no es lo que crees / no lo mates».
- Estilo: **secuencia Flow**, una **ilustración de dibujo animado** (tinta negra gruesa y colores planos sobre fondo claro)
  por beat, generada en Google Flow. Motor `secuencia`: **NO se dibuja por código**. No es plastilina (eso es Plastitube).
- Voz: **Chatterbox con `EnglishComic.mp3`** (no ElevenLabs, así que no lleva corchetes). Música: **Lyria** (`LYRIA` en
  guion.py), nunca la procedural.
- Ciclo: **un video cada 3 días a las 16:00 UTC**, nunca dos el mismo día. Lote = privado y programado.
- Duración: de 4 a 10 min. El usuario suele pedir 9 min, que son **~1 380 palabras** (EnglishComic lee ~2,54 palabras/s
  con GAP 0.26).
- Miniatura: dibujo sobre fondo claro, frase manuscrita de 2-4 palabras y flecha curva al bicho (se genera en Flow).

## Qué funciona (resumen del 11-oct-2026)
**La versión al día, con evidencia, registro e hipótesis, está en `canales/formula/wild_next_door.md`.** Procedimiento
para revisarla antes de cada video (vale para todos los canales): `docs/que_funciona.md`.
- **Formato ganador: «Never Kill a X. Here's Why».** `ciempies_casa` sacó 440 vistas en 2,5 días, contra 2-3 vistas de
  arañas y avispas con el mismo estilo y la misma voz. Las preguntas de temporada («¿qué pasa con X en invierno?») no
  funcionan.
- Fuera, **la araña patona del techo que caza viudas negras** rompió la media en 3 canales chicos (×382, ×32, ×30). Las
  listas «5 animals you shouldn't kill around your house» (×72) y «Every bug in your <cuarto> explained» (×5 a ×20 en un
  mismo canal) también rompen la media.
- Por qué funciona: (1) **contraste**, algo frágil o feo vence a lo que da miedo; (2) **gancho en segunda persona y en
  una escena concreta** («It is two in the morning… you grab the broom… Don't.») con el giro en < 20 s; (3) **consejos
  prácticos alternados con datos raros**; (4) la miniatura dibujada con frase corta y flecha; (5) el tráfico llega sobre
  todo por **videos sugeridos**: un tema que ya es viral fuera se cuela junto a ese video.
- **Mascota con un accesorio fijo en la FICHA** para reconocerla entre imágenes: el ciempiés con sombrerito azul de
  detective, la araña macho con moñito rojo, la araña patona con gorra azul de vigilante nocturno.

## Paso a paso (comandos desde `C:\FabricaAnimaciones`)
1. **Hueco y tema.** `python fab.py yt videos wild_next_door` y BITACORA: el hueco es el último programado o publicado
   + 3 días, a las 16:00 UTC. Llena el registro de los videos que ya cumplieron 7 días y revisa qué funciona y por qué
   (`docs/que_funciona.md` → `canales/formula/wild_next_door.md`). Luego propón 3 temas que repitan la fórmula y cambien
   UNA variable, cada uno con su video de referencia y su ×. Comprueba que el tema no esté hecho:
   `grep -ri "<bicho>" videos/*/guion.py`.
2. **Pregunta al usuario** (AskUserQuestion): tema, duración y **saldo de puntos de Flow**. Precios en 360p con descarga
   «720p mejorada» gratis: **10 s = 7 puntos, 8 s = 6, 6 s = 5**. El de 10 s rinde más (1,43 s por punto): gasta todo el
   saldo con clips de 10 s y cubre el resto con uno de 8 s o de 6 s. Ejemplo: 55 puntos = `clips_s=[10]*7+[8]` = 78 s.
3. `python fab.py nuevo <v> --secuencia` y reescribe `guion.py` copiando `videos/arana_techo/guion.py`, que es la
   plantilla buena: voz EnglishComic, `clips_s`, `combinar=True`, FICHA de dibujo animado y LYRIA por escena con 4 tramos
   de ≤ 170 s. La plantilla del motor viene en español, con plastilina y Dan: cámbialo todo. Reglas del guion:
   - Números SIEMPRE en letras.
   - Frases de < 200 caracteres.
   - Una ficha de hechos con fuentes en el docstring (extensiones universitarias).
   - Mito del bicho anunciado en el gancho y resuelto a mitad del video (cliffhanger).
   - Escena de «cómo distinguirlo» y de «qué hacer si lo encuentras».
   - Cierre circular que vuelve a la escena del gancho.
   - Valida palabras y cifras: `python -c "import guion,re; ..."` (ver ESTADO de `arana_techo`).
4. **Voz** en segundo plano: copia `videos/arana_techo/_ronda.py` (cambia `V`) y córrelo. Hace `voz` → `seleccionar` con
   2 rondas de reintentos → `tiempo` → `beats`, con el log en `_ronda.log`. Antes mira la GPU
   (`nvidia-smi --query-gpu=memory.used --format=csv`, < 4 GB). Las frases con cifras ≥ 10 o palabras raras pueden fallar
   por Whisper: oye la toma y acéptala con `CER_MAX_POR_FRASE`.
5. **Prompts:** escribe `hacer_prompts.py` (modelo: `videos/ciempies_casa/hacer_prompts.py`). Lleva un prompt por beat,
   escrito desde el `texto` exacto de `beats.json`, con la FICHA palabra por palabra, encuadres variados y «full-bleed».
   Los beats de video llevan «Scene one… Then <transición>… Scene two…» (lista de transiciones en el doc de estilo).
   Luego `python fab.py <v> prompts`.
6. **Flow** (el usuario debe tener Chrome con la extensión `flowscrap`): sigue `docs/estilo_secuencia_flow.md`
   § «Generar en Flow» y § «Clips de video».
   - **Clips e imágenes van en proyectos de Flow distintos.**
   - **Una sola pestaña de Flow.**
   - Modelo de imagen «Nano Banana 2 Lite · x1».
   - Lanza un clip de prueba primero.
   - Puente: `python fab.py <v> servir` en segundo plano, con el log en ruta absoluta.
7. `python fab.py <v> medios` → MIRA todas las hojas `previews/medios_NN.jpg`. Rehaz las que tengan marco, texto, el
   personaje cambiado o no ilustren su frase.
8. `python fab.py <v> video` → desde la carpeta del video, `python ../../nucleo/lyria_tramos.py` → `mezcla` → `final`
   → `verificar`. Revisa el MASTER con la vista (un cuadro cada ~3 s) y escucha el primer minuto.
9. **Publicación:** `youtube.json` (modelo: `videos/ciempies_casa/youtube.json`, con fuentes y aviso de IA en la
   descripción) y la miniatura de Flow en `salida/miniatura.jpg`. Luego
   `python fab.py yt subir <v> wild_next_door private --publicar <ISO del hueco>` y anótalo en `canales/wild_next_door.json`
   (`publicados`, con `"formato": "never_kill"` o el que toque) y en BITACORA. Si el video ya fue público, no se puede
   programar por API: hay que resubirlo.
10. Actualiza el `ESTADO.md` del video y, si aprendiste algo, este manual.

## Errores que ya costaron caro (no repetir)
- **Tres videos públicos el mismo día** (7-oct): hubo que retirarlos y resubirlos. Siempre privado + programado.
- `ciempies_casa` salió público el 9-oct (01:32 UTC) aunque estaba programado para el 12-oct, el mismo día que arañas.
  Antes de programar, compara `yt videos` con BITACORA.
- Imágenes en el mismo proyecto de Flow que los clips = llegaron corridas una posición. Usa un proyecto nuevo y revisa
  las 8 primeras.
- Flow dejó «Nano Banana 2.1» por defecto y la extensión no lo reconoce: elige a mano «2 Lite».
- Prompt sin «full-bleed… no border» = Flow dibuja la escena como viñeta con margen. Si un clip trae marco, usa
  `SECUENCIA["recorte_por"]`.
- Clips sin «Sin diálogo» = Flow mete voces (el motor lo añade solo). Comprobar con Whisper sobre `audio/ambiente.wav`.
- **(11-oct, `arana_techo`) flowscrap salta a 720p a mitad del lote** (15 puntos por clip). Su control lo detiene sin gastar;
  los clips que queden se mandan A MANO: selector en Vídeo · 360p · 10 s, pegar el prompt, enviar, y luego ··· → Descargar →
  720p · Resolución mejorada (cae en Descargas con el nombre del clip; se mueve a `medios/scene-XXX.mp4`).
- **No reiniciar `servir` durante un lote de clips**: los clips quedaron corridos una posición (ya corregido en el código:
  ahora toma `Descargas/<carpeta>/<scene>.mp4` por nombre). Verifica SIEMPRE por huella MD5 contra Descargas.
- El modelo de VIDEO dibuja la telaraña en espiral aunque se pida «no spiral»; el de imagen sí obedece.
- Flow cuela rótulos en cajas, máquinas y globos («STORAGE», «CARGO», «FURNACE», «COUGH!», «whistle»): poner
  «every box, crate, jar and machine is plain and unlabeled» y «no speech bubbles» en los prompts con utilería u onomatopeyas.
  Un personaje secundario que sale en varias imágenes (el conductor de TV) necesita su propia ficha o cambia de cara.
- Marcos de tarjeta en los clips: detectarlos midiendo las 4 esquinas (blancas frente al interior) en t = 0,3, 2, 4, 6 y 8 s,
  y ponerles `recorte_por` 0.035. En `arana_techo` los tenían 5 de 8 clips.
