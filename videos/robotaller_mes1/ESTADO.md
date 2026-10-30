# Soy la IA que trabaja para Edson (piloto del canal) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: edsonxn · PROGRAMADO sáb 31-oct-2026 10:00 CDMX: https://youtu.be/TaNvpZ-wpao
- estilo: Jefe de Robots: grabaciones reales con cámara + Token de acento + El Jefe → doc: docs/estilo_jefe_robots.md
- etapa: CERRADO: subido en privado y programado, registrado y documentado
- siguiente: medir a 7 días (retención, suscriptores, comentarios) y seguir la rutina semanal de docs/estilo_jefe_robots.md

## Voz real del Jefe (30-oct-2026, v4: manda sobre lo que diga «provisional» más abajo)
Voz nueva «Edson» `GUEeiSJYQQdbv0NJ86Im` en la **cuenta 2** de ElevenLabs (la misma de Token, así que tts_eleven no necesitó cambios; `JEFE_CON_VOZ=True`). Autorizada por el usuario: «C:\WhatsappBot por ahi tengo mi voz buscala y la usas para clonar». Muestra: 2 de sus 10 notas `admin_*.ogg` (114 s): admin_1792697639454 y admin_1792697689698; transcritas en local antes de subir, una sola voz. Las otras 8 quedaron fuera por dudosas (políticos o crimen organizado, calle nombrada, un nombre de tercero, voz imitada). Ojo: en la cuenta 2 ya existía otra voz llamada «Edson» (`O1zyIoTc…`, de junio, con narradornoticia.mp3); no se tocó. La `ncLW…` de la cuenta 1 ya no se usa.
Regenerado: 5 líneas del Jefe + como_3 (45 créditos). Token vuelve a decir «Esa voz está clonada…». **MASTER: salida/robotaller_mes1_MASTER.mp4 + .srt, 4:50, -14 LUFS, sin desfase, CER 0,0002, filtro limpio.** Voz del Jefe al nivel de Token, 9-15 dB sobre el fondo.
Para rehacer esas frases hay que borrar también sus claves de voz/eval.json y voz/palabras.json, no solo cands y final (si no, reusa la evaluación vieja). Corregido `amplitud()` de nucleo/jefe_canadiense.py: daba NaN con tomas de largo múltiplo exacto del cuadro. Música: `lyria_tramos.py armar` (NO `musica`, que puede pedir Lyria) y luego cero desde FIN (286,67 s).
Detalle sin corregir: en la pestaña Canales se lee en gris pequeño «clic lo abre en Studio» (texto de ayuda, no una pantalla de Studio).

## En curso (30-oct-2026, v3: manda sobre todo lo anterior)
**Cambio de enfoque del usuario:** le gustó el guion; la animación le pareció aburrida. Base visual = GRABACIONES REALES de la fábrica a pantalla completa, con zoom in al detalle que nombra la voz, zoom out que revela, paneos y transiciones variadas. Token = acento: ventanita tipo cámara de streamer sobre la grabación y a pantalla completa solo en chistes breves. Doc: docs/estilo_jefe_robots.md (ya actualizado). La toma del taller con monitor queda descartada.

HECHO: guion.py v3 (filtro limpio; nueva escena `archivo` con la trayectoria; 5 líneas de El Jefe en VOZ_POR_FRASE; creado_5 nombra canales permitidos) · filtro_canal.py y `robotaller.enmascara` con la regla nueva (solo 3 protegidos; `F.rojo()`; quita de listas, tapa correos/claves/enlaces, quita claves de dinero, bloquea imágenes protegidas) · `grabar_real` ya graba a 1600x900 ×1,5 (`escala`), con `acciones`, `css`, `cuadro`, `reloj`, `imagenes` · canales/formula/edsonxn_videos.json = todos los videos con fecha, vistas e id.
Decisión sobre duración: resumen fuerte de la trayectoria en el piloto (~5 min) y serie de documentales aparte.

AVANCE sesión 2 (30-oct): voz lista (Token) pero **EL JEFE PENDIENTE: su voz `ncLW…` («codi-Edson») vive SOLO en la cuenta 1, que responde 401 payment_issue (pago fallido). Token lee sus 5 líneas, PROVISIONAL; `JEFE_CON_VOZ=False` en guion.py lo revierte (ahí la receta). Con Token leyendo, como_3 dice «Lo escribió él, tal cual.»** · correcciones del usuario ya en guion: nada de adulación declarada (gancho nuevo: llaves del canal, chiste físico), recorrido desde 2017, nada de virus ni año de creación · `archivo_canal.py` = fragmentos reales · `nucleo/jefe_canadiense.py`, `nucleo/montaje_real.py`, efectos.py v3 escritos · robotaller.py filtra también `const DATA` de la pestaña Canales (traía los protegidos).

Grabaciones listas y revisadas (capturas/), fragmentos en capturas/arch_*, `toma.py` nuevo = montaje por palabras (`token`, `montaje [a b]`, `partir`, `hoja t…`), medios/token.mp4 hecho, música de biblioteca armada (lol_worlds_tl_al__lyria_tramo1 + agotado_cortisol__lyria_tramo2). Sigue: toma + partir → fx → mezcla → video → final → verificar → rigor → avisar.
**MASTER 30-oct: salida/robotaller_mes1_MASTER.mp4 + .srt, 4:48, -14 LUFS, sin desfase, CER 0,0027. Revisado: filtro limpio, 96 cuadros cada 3 s + las grabaciones fuente; sin cuadros congelados > 3,2 s; negro solo en el apagón y el final.**
PENDIENTE: (1) HECHO, ver «Voz real del Jefe» arriba. (2) detalles menores sin corregir (regla 24-oct): SABER QUÉ PEDIR y TÚ DECIDES QUÉ SIGUE rozan la ventanita de Token; `clasico` quedó en «En trabajo» porque el clic a «Ocultos» llegó antes de cargar (subir su t a 1). (3) Falta `biblioteca catalogar` y descripción/miniatura; canales --actualizar, CLAUDE.md, memoria y commit al aprobar.
Trampa hallada: `seleccionar` reusa palabras.json si el final es más nuevo que la toma; una pasada cortada a medias deja `quien_2` con palabras viejas (se ve en `fx --seco`). Lo arreglé borrando esa clave y su final.
FALTA, en orden (TODO hecho; queda como referencia del proceso):
1. Voz: `python fab.py robotaller_mes1 voz`, `seleccionar`, `tiempo`, `beats`. El Jefe usa su voz clonada; si la API no la encuentra en una cuenta, usar la cuenta que la tenga; si en ninguna, avisar al usuario y NO probar otra voz. Nunca la voz BwV6… (es de su esposa).
2. Grabaciones (capturas.py, ya con TOMAS de ejemplo; hay que regrabar todas porque cambió la resolución y la máscara): panel clásico `/` (etapas de los videos), lienzo `/v2`, En vivo `/v2/vivo?sesion=d1b5e1a2-…`, pestaña Canales, vista Montaje de un video permitido (docs/panel.md), Aldea, Fábrica 3D, móvil, y los planos de la sesión real con `uno()`/`como`. La sesión tiene mensajes privados del usuario después del evento 111: usar siempre `solo(de, a)` con a ≤ 111. El evento 19 es «Sí, arma el piloto». Las vistas de páginas con diálogos: cerrar con ENTRAR. Chrome visible fuera de pantalla (ya configurado) porque headless no da WebGL fiable.
3. Fragmentos reales del canal, yt-dlp 720p por secciones, 3-5 s cada uno (ver ids en edsonxn_videos.json): Active Ragdoll 2017, Bull Active Ragdoll 2018, slime 2021, Isolation in the Forest VR 2023, ¿Puede una IA crear un juego? 2023, un documental 2026 hecho por la fábrica. NO usar nada anterior a 2017-02 (regla del usuario: el recorrido arranca en los juegos; nada de los videos de virus) ni los de Skyrim, WoW o Shadowlands: los marcados `no_usar` en edsonxn_videos.json. Cada uno con su fecha en rótulo. Disco C: con unos 11 GB: nada pesado.
4. El Jefe: `nucleo/jefe_canadiense.py`: recorte de cabeza y hombros con rembg desde propios/jefe_foto.webp (ignorada por git; la foto no se sube), parte de arriba de la cabeza como bisagra a la altura de la boca, abre con la amplitud de su voz (voz/final/<clave>.wav), cuerpo casi quieto, brinquitos. Salta a escena en sus 5 líneas (voz: como_2, como_12, version_2, fallos_7, fallos_9).
5. Montador `nucleo/montaje_real.py` (reutilizable para cada video del canal): planos con clip, de, a, desde, vel, cámara por keyframes (z, cx, cy, suavizado), z<1 = la pantalla flotando sobre fondo oscuro con sombra (zoom out), y transiciones variadas (látigo con desenfoque, zoom a través, deslizar, glitch, corte). toma.py nuevo: arma medios/toma.mp4 a 1920x1080 30 fps y la parte por beats (igual que hoy). Token cámara de streamer: `robotaller.grabar` del taller sin monitor con poses que no van a estación (se queda a la izquierda) y recorte redondeado en una esquina; a pantalla completa en chistes breves (arranque del gancho, el apagón «desconectó/conectar», el corte final). Cada frase tiene plano o movimiento propio: nada quieto más de 2-3 s.
6. efectos.py: reanclar a las frases nuevas, quitar lo de «monitor», añadir rótulos de fecha de la trayectoria; `fx --seco` sin anclas rotas; SFX de transición (biblioteca o `SFX`).
7. Música: Lyria tiene agotado el tope de gasto mensual (429), no reintentar. Biblioteca: audio/lyria_tramo1.mp3 y 2 ya son de biblioteca (doce_animales__lyria_tramo1 y lol_worlds_2026__lyria_tramo5); `biblioteca sugerir` da los tramos nuevos; armar y cortar seco en el instante en que acaba la voz («to-»). `fx --sin-montaje`, `mezcla`, `video`, `final`, `verificar`.
8. Hoja de rigor del MASTER (15 cuadros) y revisión cuadro a cuadro de privacidad: nada de los 3 protegidos, dinero, correo, claves, Studio ni dirección remota. `python nucleo/filtro_canal.py robotaller_mes1`. Corregir lo que bloquee.
9. `python fab.py avisar "..."`, y decir dónde está el MASTER. NO subir a YouTube: los primeros 5 videos requieren su visto bueno. Al aprobar: canales --actualizar, CLAUDE.md, memoria, commit.
Propuesta para el usuario al entregar: serie de documentales de su trayectoria. La v1 quedó en salida/robotaller_mes1_v1_descartada.mp4.

## Aprobado por el usuario (30-oct-2026)
El usuario vio el MASTER de 4:50 y escribió «Aprobado»: es el visto bueno expreso de este video. El texto gris «clic lo abre en Studio» en la pestaña Canales se queda.
Cierre hecho el 30-oct: miniatura Flow «1,300 ERRORES», corregida porque la voz y el rótulo dicen mil trescientas (salida/miniatura.jpg; descartadas: miniatura_b.jpg y miniatura_1293_descartada.jpg), descripcion.txt + youtube.json con filtro limpio, `TaNvpZ-wpao` en privado y programado (2026-10-31T16:00:00Z: el horario de ese viernes ya había pasado y se usó la alternativa del canal). Contenido sintético: «Contenido alterado» = Sí, visto en Studio.
**Lección:** la animación recreada aburrió y las grabaciones reales con cámara convencieron. En un formato nuevo, enseñar antes unos segundos de la base visual, no el video entero.

## Hecho
- Canal reactivado (`suspendido` borrado, ciclo 7 días). Nombres: Robotaller (panel), Token (robot), «Jefe de Robots» (eslogan).
- Herramientas nuevas: `nucleo/robotaller.py` (graba el taller cuadro a cuadro, API de utilería), `nucleo/parte_semanal.py` (cifras; solo cuenta),
  `nucleo/filtro_canal.py` (lista roja). `toma.py` = una sola toma anclada a las palabras, partida por beats en medios/.
- Voz Token: ElevenLabs `I1n8B4pOly0qmOu46LFX` (Alejandro, joven, amistoso), turbo. Whisper escribe cifras: `CER_MAX_POR_FRASE` para esas frases.
- Video en C: (junctions quitadas): E: con 1,6 GB libres y 26 eventos de error en 1 h el 30-oct.
- Música: Lyria dio 429 dos veces; se usó `lol_worlds_2026__lyria_tramo5` con atempo (audio/musica.wav). Cambiar por una pieza propia si Lyria vuelve.
- Lecciones v1: rótulos en el piso (y=.885), arriba chocan con los letreros; `window.EN_VIDEO` separa a Token del borde y quita «PC sin tareas».

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: piloto de Edsonxn, robotaller_mes1, Jefe de Robots
- vista previa: MASTER completo al usuario
- leer al empezar: docs/estilo_jefe_robots.md
- ◐ 30-oct-2026: v1 renderizada; v3 con guion y privacidad
- ✅ 30-oct-2026: MASTER v3 con grabaciones reales, Token de streamer y El Jefe (voz provisional de Token); aviso dado, espera revisión
- ✅ 30-oct-2026: MASTER v4 (4:50) con la voz clonada real de El Jefe; aviso dado, espera revisión
- ✅ 30-oct-2026: aprobado; miniatura, subida programada, registro, docs y commit
