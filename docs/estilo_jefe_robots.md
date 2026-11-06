# Estilo «Jefe de Robots» (canal Edsonxn, desde el 30-oct-2026)

**Concepto (el usuario):** el tema es enseñar lo que se puede crear con IA y cómo se hace. **La IA es la narradora:** Token, el robot del panel, habla como lo que es. Edson es «mi jefe». El canal es el perfil de desarrollador de Edson y debe funcionar casi solo: Edson supervisa.

## Nombres
Robotaller = el panel `/v2/vivo` · Token = el robot principal · Torre = la PC · Jefe de Robots = eslogan del canal.

## Lo que pidió el usuario tras ver la v1 (30-oct)
1. Más divertido; que se sienta como la animación del Robotaller.
2. Capturas REALES de lo que se hace y de cómo se hace.
3. Jugar con el ego del espectador: que salga sintiéndose bien, motivado, superior.

## Elevar al espectador: la receta (INTERNA)
**Regla del usuario (30-oct): esto es entre Claude y él. JAMÁS se menciona en un video:** ni en voz, ni en rótulos, ni en descripción, ni en título. Se hace, no se dice: nada de «me pidieron hacerte sentir bien», ni adulación declarada, ni el estudio. El video tampoco dice que se cambió para gustarle al espectador.
Investigado el 30-oct. La evidencia es dispareja: el efecto de la adulación tiene estudios; lo demás son consejos de creadores, no experimentos. Medir en el canal.
- **El espectador es el protagonista.** Pasa de «¿esto funciona?» a «ya entendí»; la IA le habla de tú y va mostrando lo que él ya captó.
- **Darle un papel y poder real:** Token le dice «mi jefe me manda a mí, tú le mandas a él»: los suscriptores son **la junta directiva** y los comentarios deciden qué se construye. Tiene que ser verdad: cumplirlo y enseñar el comentario.
- **Tratarlo como colega listo:** no explicar de más, dejarle hacer la deducción, y dejar que llegue antes que Token a alguna conclusión («ya te diste cuenta, ¿verdad?»).
- **Token se hace menos para que él suba:** 1 293 fallos; el robot se equivoca y el espectador lo nota primero.
- **Contraste suave:** «mientras casi todos discuten si esto sirve, tú viniste a ver cómo se usa».
- **Motivar con algo cierto:** no hizo falta un equipo; hizo falta saber qué pedir, y eso se aprende mirando.
- **Límites:** nunca inventar cifras («solo el 1 % sabe…»), nunca prometer dinero, nunca burlarse de un grupo de personas. Cada elogio tiene que apoyarse en algo cierto, porque un elogio falso a la larga se vuelve en contra (Cialdini).

## Lo que pidió el usuario tras ver el guion v2 (30-oct)
«La animación se siente aburrida»: la recreación de robots no es lo principal. **Lo principal son las GRABACIONES REALES de la herramienta** (panel clásico, lienzo, En vivo, Montaje, canales, y lo demás), tal cual, con zoom in al detalle que nombra la voz, zoom out que revela la pantalla, paneos y transiciones variadas. Nada quieto ni repetitivo. Que se entienda cómo funciona la fábrica por dentro.

## El canal es archivo y currículum
El canal de Edson es el archivo de su carrera y funciona como su currículum: Token cuenta la trayectoria con fragmentos reales, su fecha y las herramientas de cada época. Fue su campo de pruebas; **desde ahora Claude lleva el control del canal, con supervisión del usuario**. Datos: `canales/formula/edsonxn_videos.json`. Solo se afirman fechas y herramientas verificables (títulos, descripciones); lo demás se pregunta. **El recorrido arranca en su etapa de desarrollo de juegos (primer video de Unity: febrero de 2017). Regla del usuario, 30-oct: nunca se menciona ni se enseña lo anterior, y menos la temporada de videos de virus: da pena.** Tampoco el año de creación del canal ni una cifra de años que dependa de esos videos. En la lista, esos videos llevan `no_usar`. La trayectoria completa da para una serie de documentales aparte; el piloto lleva el resumen fuerte.

## El Jefe
Edson sale como personaje: su foto recortada (`propios/jefe_foto.webp`, sin fondo) animada como los canadienses de South Park: la parte de arriba de la cabeza sube y baja como bisagra a la altura de la boca, cuerpo casi quieto, brinquitos. Es un recorte movido por código, no un deepfake. Habla con su voz clonada de ElevenLabs (por `VOZ_POR_FRASE`; nunca la de Gaia). Pocas líneas, como remate frente a Token, y solo frases suyas reales; una línea nueva con su voz se le enseña antes. Sustituye al personaje del sombrero del globo «El Jefe dice».

## Imagen
- Base: grabaciones reales a pantalla completa (`robotaller.grabar_real`, a 1600x900 ×1,5 para poder acercar) montadas con cámara: zoom, paneo y transiciones.
- Token: acento, no base. Narra desde una ventanita tipo cámara de streamer sobre la grabación, y a pantalla completa solo en chistes breves. Taller: `robotaller.grabar`, cuadro a cuadro.
- Rótulos en el piso (`y=.885`).
- **Montador (30-oct): `nucleo/montaje_real.py`**, reutilizable en cada video del canal. Planos anclados a las palabras (`toma.py` de `robotaller_mes1`, `T(frase, palabra)`), cámara por keyframes (z>1 acerca, z<1 la pantalla flota sobre fondo oscuro), transiciones `latigo`, `zoom`, `deslizar`, `glitch`, `destello`, `corte`, nunca dos seguidas iguales (`m.revisar()`). `m.camara()` = Token de streamer, `m.jefe()` = El Jefe. `python toma.py hoja t1 t2…` da cuadros sueltos sin renderizar: mirarlos ANTES del render largo.
- Fragmentos reales: `archivo_canal.py` (yt-dlp por secciones o MASTER local; un video privado o programado no baja, se corta del MASTER). Verticales con `vertical()`: el cuadro sobre su copia borrosa.

## Privacidad
`python nucleo/filtro_canal.py <v>` antes de la voz y antes de subir.
**PROTEGIDOS (el usuario, 30-oct; ni nombre, ni imagen, ni logo): Crónicas de Warcraft, Crónicas de Tamriel y Runa Caída.** También lo que los delata: alias `wow_*`, `tes_*`, `er_*`, títulos, miniaturas, pegatinas, gameplay o interfaz de WoW, Skyrim y Elden Ring, sus cifras de suscriptores, y el patrocinador con su código.
**PERMITIDOS: todos los demás.** Crónicas del gaming, Cronopapel y Bitácora Perdida se muestran y se mencionan; de Crónicas del gaming se dice que sus videos los hace la IA.
**Gaia Eterna tampoco sale en las grabaciones (30-oct): su arte es de WoW** (`gaia_crematoria`, en la lista roja). La pestaña Canales trae sus datos dentro del HTML (`const DATA`): `grabar_real` la limpia aparte. Los eventos 101-102 de la sesión d1b5e1a2 son búsquedas de adulación: fuera de cuadro.
**El carro del usuario, sin modelo ni año (el usuario, 5-nov-2026: «que no se muestra qué vehículo es, solamente que es para mi vehículo»):** ni en la voz, ni en rótulos, ni en pantalla (mensajes, nombres de paquete, APK). Se dice «su carro»; la app del escáner se llama «el escáner del carro». En `robotaller_4apps` el `PRIVADO` de `capturas.py` tapa modelo, año, «4 puertas», cilindrada y el nombre de la app.
Siempre tapados: dinero, claves, correo, dirección del panel remoto, Studio, y el usuario de Windows en las rutas. Las grabaciones pasan por `robotaller.enmascara`, que quita de la API lo protegido y bloquea sus imágenes, y aun así se revisan cuadro a cuadro.

## Lecciones del 3.er video (`robotaller_4apps`, 5-nov-2026)
- **`montaje_real` se quedaba sin memoria con 25 grabaciones de 2400 px** (cada `VideoCapture` abierto pesa): ahora deja abiertas 8 como máximo y cierra las menos recientes.
- Los globos largos del Robotaller no caben con z > 1,8; con El Jefe en pantalla, quitar la ventanita de Token de ese plano (`ventana=False`) o pasar al Jefe a la izquierda (`lado="i"`) si su frase queda a la derecha del globo.
- La cámara no puede subir el globo (está pegado abajo, `_encuadre` recorta dentro del cuadro): para esquivar al Jefe, correr el encuadre a la derecha (`c=(1.0, .77)`).

## Lecciones del 2.º video (`robotaller_n64`, 1-nov-2026)
- **El tapado del usuario estuvo roto** hasta el 1-nov: `robotaller._USUARIO` tenía retrocesos (\x08) en vez de `\b` y el usuario de Windows salía en las rutas. Arreglado; antes de montar, comprobar en la API ya tapada que no queda (`enmascara` sobre `/api/v2/agente?sesion=<id>&desde=0` y buscar el usuario, correo y la lista roja). Ojo: desde Bash, `\\` en heredocs y escrituras a `nucleo/` pueden fallar sin avisar; usar Write/Edit o PowerShell.
- **Con El Jefe en pantalla (va a la derecha) el globo del mensaje se corre a la izquierda** (`MSJ_J`), si no su cabeza tapa la frase (y la falta de ortografía).
- Las tomas del panel son casi todo fondo oscuro: acercar al texto (z 1,5-2,1 arriba a la izquierda), nunca a z 1 entero.
- El Montaje del panel (`/?embed=montaje`) puede grabarse en blanco: mirar su hoja; como respaldo, un fragmento del MASTER.
- Sonido nombrado: «canciones» y «Escucha» llevan su OST real como PISTA `voz=True` (la música Lyria se agacha); «la escucha» de Whisper es falso positivo del `chequeo`.

## Producción
Voz Token: ElevenLabs `I1n8B4pOly0qmOu46LFX`, turbo, corchetes (en las cuentas 2 y 3). Voz de El Jefe: cuenta 2 `GUEeiSJYQQdbv0NJ86Im` y, desde el 1-nov (cuenta 2 sin saldo hasta el 20-nov), cuenta 3 `hCU4QZdzzUliy58ezPBz`, clonada con las mismas 2 notas; solo por id. Los ids van en la línea `VOZ_POR_FRASE` de guion.py, nunca en comentarios (el filtro los marca). Cifras: `python nucleo/parte_semanal.py [desde] [hasta]`. Video en C:, no en E:. Revisión: primeros 5 videos con visto bueno expreso; no se sube sin él.

## Miniatura
Flow, Nano Banana 2.1, 16:9, x2, con Token y la foto de El Jefe como ingredientes. Cifra real gigante (lo que el título no dice), **escrita igual que la dice la voz** (el usuario pidió corregir «1,293» a «1,300»), El Jefe serio con los brazos cruzados a la izquierda y Token apenado a la derecha, en un taller oscuro con monitores. Salió bien a la primera, 2/2. Prompt: `videos/robotaller_mes1/prompt_miniatura.md`.
**Short vertical (5-nov-2026, `euphoria_robots`): 9:16 y UN solo ingrediente**: la miniatura ya publicada de `robotaller_mes1` (`i.ytimg.com/vi/TaNvpZ-wpao/maxresdefault.jpg`, CORS abierto: `fetch` → `File` → `paste`) trae a Token y a El Jefe con su diseño exacto; el prompt pide «use the reference only for the two characters, ignore its text and layout». Título arriba, nada de texto ni caras en el cuarto inferior (botones de Shorts). 2/2 bien; Flow da 768x1376 y se reescala a 1080x1920. Prompt: `videos/euphoria_robots/prompt_miniatura.md`.

## Subida
Canal con narrador IA y voz clonada: `"contenido_sintetico": true` en `youtube.json` y aviso en la descripción (narra una IA, voz clonada con permiso del dueño). `yt subir` lo manda en `status.containsSyntheticMedia`. **El GET de la API no devuelve ese campo: se comprueba en Studio, «Mostrar más» → «Contenido alterado» = Sí.** Desde nov-2026 la casilla se llama **«Uso de IA»** (Sí / No) y `yt subir` ya la deja en Sí: solo se mira, no hace falta guardar (comprobado con `euphoria_robots`). Primero `descripcion.txt` (la lee el filtro) y de ahí `youtube.json`.

## Rutina semanal (ciclo 7 días)
1. **Junta directiva:** `python fab.py yt comentarios edsonxn`. Lo más votado decide qué se construye; se cumple de verdad y el video enseña el comentario real.
2. **Cifras:** `python nucleo/parte_semanal.py <desde> <hasta>`, solo lo que salga de ahí.
3. **Tema:** `python fab.py ideas edsonxn` + `canales/formula/edsonxn.md`; propuesta de 3 temas al usuario. Reparto: lo que se construyó esa semana o un capítulo de la serie de la trayectoria.
4. **Producción:** `nuevo`, guion, filtro, voz, grabaciones reales (`grabar_real`), `toma.py`, sonido, `final`, `verificar`, filtro y revisión de privacidad cuadro a cuadro.
5. **Visto bueno:** `python fab.py avisar "..."`. Hasta el 5.º video no se sube sin él.
6. **Subida:** miniatura, descripción, hueco de `canales --actualizar`, privado y programado; casilla de Studio; registro en `publicados` y BITACORA.
7. **Medir a 7 días:** retención, suscriptores y comentarios; conclusión en `canales/formula/edsonxn.md`.

Fuentes: [AMA, resumen de Chan y Sengupta](https://www.ama.org/research-insights/research-insight-even-phony-flattery-helps-close-deals/) · [CNBC, Cialdini](https://www.cnbc.com/2020/07/14/how-donald-trump-charms-people.html) · [OverseerOS, espectador protagonista](https://www.overseeros.com/blog/YouTube-storytelling-techniques-6-ways-keep-viewers-watching-longer) · [Teleprompter, hablarle al espectador](https://www.teleprompter.com/blog/youtube-audience-retention)
