# Publicación y canales (protocolo de video nuevo, horario, miniaturas IA, subida a YouTube)

_Extraído de CLAUDE.md (1-oct-2026). Se lee solo cuando el video lo necesita._

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
   **Y siempre `python fab.py ideas <alias>`** (8-oct-2026, `nucleo/ideas.py`): lo tuyo contra la mediana del canal
   + los videos del nicho que rompieron la media DE SU CANAL en los últimos 60 días (`--actualizar` si el informe
   tiene más de ~1 semana; ~350 de cuota). El tema sale de ahí: formato que se repite en varios canales chicos
   + lo que a ti te retuvo. Ajusta `ideas.busquedas`/`competidores`/`filtro` de `canales/<alias>.json` si sale ruido.
   **Después, el porqué:** `docs/que_funciona.md` → actualizar `canales/formula/<alias>.md` (fórmula, evitar,
   hipótesis, registro a 7 días) ANTES de proponer temas.
   Al subir el video, anota `"formato": "<nombre corto>"` en su entrada de `publicados`: el informe agrupa por formato
   y así se ve qué apuesta ganó.
3. **Preguntas** (AskUserQuestion, con tu recomendación primero): tema (3 ideas sacadas del informe de `ideas`,
   cada una con el video de referencia y su × mediana), estilo visual, duración, formato (largo o Short vertical), voz (Dan por defecto) y cuándo
   publicar (por defecto el siguiente hueco del horario del canal, abajo). Nunca versiones para WhatsApp.
4. **Producir** (flujo de abajo) → miniatura (2-3 variantes) → `youtube.json` (título ≤ 50 caracteres con
   la palabra clave al inicio; descripción con capítulos reales del timeline, fuentes, enlace a otro video
   del canal y 3 hashtags; 15-25 etiquetas ≤ 450 caracteres) → `yt subir ... --publicar <ISO>`.
   Publicar o hacer público = confirmarlo con el usuario (programar lo que él pidió está bien).

## REGLA: NUNCA varios videos del mismo canal el mismo día (el usuario, 7-oct-2026)
Origen: el 7-oct-2026 se hicieron públicos de golpe 3 videos de Wild Next Door (arañas, ciempiés, bichos en
invierno) un día después del de avispas. Hubo que retirarlos a privado. **No se repite.**
- **Un video por canal a la vez, espaciados.** Separación mínima entre dos videos públicos o programados del
  mismo canal: `horario.separacion_min_horas` de `canales/<alias>.json` (48 h por defecto). Wild Next Door:
  uno cada 2-3 días.
- **Si hay varios videos listos (lote):** todos se suben en PRIVADO y se programan (`--publicar <ISO UTC>`)
  en huecos sucesivos del calendario; antes se le enseña el calendario al usuario. «Súbelos» o «publícalos»
  dicho sobre un lote NO significa «todos hoy».
- **Antes de publicar o programar:** `python fab.py yt videos <canal>` + BITACORA para ver qué hay público o
  programado cerca de esa fecha.
- **El código lo impide:** `yt publicar ... public`, `yt publicar ... --programar` y `yt subir ... public /
  --publicar` se detienen (`comprobar_separacion` en `nucleo/youtube.py`) si chocan con otro video del canal.
  `--forzar` solo cuando el usuario pidió expresamente esa excepción para ese video, nunca por iniciativa propia.
- **Un video que ya fue público no se puede volver a programar por API** (HTTP 400): por eso hacer público es
  difícil de deshacer; ante la duda, privado + programado.

## Horario de publicación (investigado 2026-09-28; revisar con métricas propias)
- Audiencia objetivo: México/Latinoamérica (+ España). Videos largos: **miércoles a viernes 14:00 CDMX
  (20:00 UTC)** = 15:00 Bogotá/Lima, 17:00 Buenos Aires, 22:00 Madrid; alternativa sábado/domingo 10:00 CDMX
  (16:00 UTC). Regla: publicar 1-2 h antes del pico de la audiencia. Shorts: 18:00-21:00 locales.
- Constancia > hora exacta: 1-2 videos por semana el mismo día/hora. Programa con `--publicar` (UTC).
- Cuando el canal tenga datos, pide al usuario la gráfica "Cuándo están conectados tus usuarios" de
  YouTube Studio > Estadísticas > Audiencia (no está en la API) y ajusta `horario` en `canales/<alias>.json`.

8. Miniatura: `videos/<nombre>/miniaturas.py` con `VARIANTES = {nombre: fn(lz) -> fondo}` (ejemplo en
   `videos/40mil_anos/miniaturas.py`) → `python fab.py <nombre> miniatura` → `salida/*_mini_<variante>.jpg`
   (1280x720) y `previews/miniaturas.jpg` (MÍRALA: incluye la vista a tamaño de celular). En el nicho funciona:
   personaje grande con cara de sorpresa, 1-3 palabras enormes amarillas con contorno negro, alto contraste.
   Usa `ojos="abiertos"` (a un T fijo el parpadeo automático puede cerrar los ojos).
   Metadatos de YouTube del video en `videos/<nombre>/youtube.json`; datos del canal en `canales/*.json`.
8b. **Miniaturas con IA (Nano Banana 2) — flujo vigente desde el 30-sep-2026.** El usuario genera la imagen en Nano Banana 2 (soporta texto) con un prompt que escribe Claude;
   luego avisa, y Claude la reduce a 1280x720 (<2 MB) y la sube. Ejemplo ganador con su prompt completo: `videos/tesoro_moctezuma/prompt_miniatura.md` («ORO PERDIDO», salió muy bien a la primera).
   Receta del prompt (en inglés, texto en español entre comillas): (1) primera línea = formato + estilo (*flat vector illustration like modern animated explainers* para que coincida con el video);
   (2) SCENE = UN solo momento dramático con sujeto grande y emoción extrema (pánico/sorpresa), el elemento valioso cayendo/brillando y fondo con contexto (ciudad en llamas, canoas);
   (3) LIGHTING AND COLOR: fondo muy oscuro y UN elemento brillante (oro) + luz de contraluz naranja/azul; (4) TEXT: «exact, Spanish, render perfectly, no extra words», 1-3 palabras en 2 líneas (blanco + amarillo #FFE21E),
   mayúsculas gruesas condensadas con contorno negro y sombra, en el tercio superior-izquierdo SIN tapar cara ni objeto clave; (5) COMPOSITION: regla de tercios, espacio oscuro limpio para el texto;
   (6) NEGATIVE: sin marca de agua, sin texto extra, sin faltas, sin rostros reales, sin desenfoque en el texto. Dar 2 variantes (misterio «¿DÓNDE ESTÁ?» y consecuencia «NUNCA APARECIÓ»).
   Si un acento sale mal: pedir corregir solo el texto conservando todo lo demás. Comprobar a tamaño de celular (~170 px de ancho): deben leerse el texto y la cara.
   Las miniaturas hechas por código (`miniaturas.py` / `hacer_miniaturas.py`) quedan como respaldo; la de IA es mucho más llamativa.
8c. **Publicación (flujo acordado con el usuario):** Claude sube el video con `python fab.py yt subir <video> <canal> private` (sube video, aplica `youtube.json`, miniatura `miniatura` y subtítulos .srt), anota el
   id en `canales/<canal>.json` (`publicados`) y en BITACORA.md; **el usuario lo publica él mismo desde Studio** (o pide programarlo con `yt publicar <canal> <id> public --programar <ISO UTC>`).
   Antes de subir: cerrar VLC u otro reproductor que tenga el MASTER abierto (si no, `final` falla con PermissionError), correr `verificar` y abrir la hoja `previews/final_hoja.jpg`.
9. YouTube (`nucleo/youtube.py`, portado de RemoGravity; cliente OAuth en `canales/youtube_client_secrets.json`,
   tokens en `canales/tokens/`): `python fab.py yt ayuda`. Canal por alias = nombre de `canales/<alias>.json`
   (p. ej. `sapiens_con_wifi`). `yt videos <canal>`, `yt metricas <canal> [dias]`, `yt aplicar <video> <canal> <id>` (metadatos + miniatura +
   .srt a un video ya subido, sin cambiar su visibilidad), `yt subir <video> <canal> [private|unlisted|public]
   [--publicar ISO]`, `yt publicar <canal> <id> [public|unlisted|private] [--programar ISO]`, `yt canal <alias>` (descripción, palabras clave, idioma, país, banner). Nombre y foto de
   perfil del canal NO se pueden cambiar por API (Studio). Publicar o hacer público = preguntar antes.
   Arte del canal: `python canales/arte_canal.py "NOMBRE" "lema"` → `canales/arte/` (revisar `*_revision.jpg`).
