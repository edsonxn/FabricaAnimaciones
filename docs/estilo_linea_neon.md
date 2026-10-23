# Estilo «LÍNEA BLANCA + NEÓN» (secuencia Flow con efectos; prueba sin canal)

_Creado el 16-oct-2026 con `videos/freno_enojo/` («Lo que pasa dentro de tu cuerpo cuando te callas el coraje»). Origen: reels
que le gustaron al usuario (Polymaths Unite / Deepstash: ratas mirando la luna desde un pozo, granjero con sombrero de neón
junto a un pozo, círculo de neón con gente peleando, rata cazando con una gallina de neón en el granero)._

Motor: SECUENCIA (`nuevo <v> --secuencia`) + capa de efectos (`docs/estilo_secuencia_fx.md`). Las imágenes y clips salen de
Google Flow; el brillo del neón, la cámara, las palabras clave y los SFX van por código.

## El look (lo que define el estilo)
1. **Fondo negro puro** y dibujo de **grabado en línea blanca fina** (como tiza o punta de plata): trazos delgados, sombreado
   con achurado suave, mucho detalle en el escenario (rocas, ladrillos, trigo, tablas) pero todo monocromo.
2. **UN solo elemento protagonista en neón amarillo** con halo dorado (el sombrero, la gallina, el anillo, el nervio, el
   corazón). A veces ojos rojos o amarillos que brillan. Nada más lleva color.
3. Personajes **monigote simpático**: cabeza redonda blanca, ojos de punto, cuerpo de línea; animales en grabado realista.
4. **Palabra gigante blanca al centro** (Poppins Black con sombra). En la referencia es karaoke palabra por palabra; en la
   Fábrica, por la regla «sin subtítulos quemados», **solo palabras clave** (decisión del usuario, 16-oct-2026): ~1 cada 10-15 s.
5. Cámara lenta y el neón **respirando** (FX `neon`): pulso lento + chisporroteo raro del tubo. Viñeta negra suave siempre.

## Prompt de estilo (FICHA["estilo"], en inglés, probado con Nano Banana 2 Lite y Omni 1.1 Flash)
Ver `videos/freno_enojo/guion.py` → `FICHA`. Claves: «white line-art illustration on a pure black background, like a fine
engraving drawn with thin white chalk-like lines», «ONE key element outlined in glowing bright yellow neon light», y en el
cierre «no color other than white lines and yellow neon». Nombrar en cada prompt QUÉ va en neón.

## Efectos por código (efectos.py)
- `dict(tipo="neon", de=0, a=99999, fuerza=.9)`: detecta lo saturado y brillante (sat > 90, val > 110 en HSV) y le suma un
  halo doble (radio 9 y 27 a 1/4 de resolución) que palpita. Parámetros: `fuerza`, `vel`, `radio`, `sat`, `val`.
- `vineta` negra 0,35 en todo el video; `latido` negro (no rojo) en la alarma; `tinte` azul en el frío.
- Rótulos: `dict(texto=..., en="palabras", dur=1.6, tam=140, color="blanco", y=.5)`.

## Voz
ElevenLabs `eleven_v4` con corchetes. Primera voz usada: **Alejandro Durán — Warm, Deep** (`sKgg4MPUDBy69X7iv3fA`, biblioteca
pública, latinoamericano grave con ronquera leve), tono de divulgación calmada.

## Miniatura (Flow, Nano Banana 2.1 con el texto dentro; 3 videos del canal)
- Fórmula fija: fondo negro, el monigote de línea blanca GRANDE en el 45 % izquierdo (cabeza negra con contorno blanco), UN
  motivo en neón amarillo sobre el cuerpo, y 2-3 palabras gigantes en 2 líneas a la derecha (mayúsculas condensadas blancas con
  halo amarillo). El texto dice lo que el título no dice («LLORAS DE CORAJE», «AGOTADO Y DESPIERTO», «ES EL ESTRÉS»).
- Navegador integrado → proyecto nuevo → chip por defecto Imagen · 16:9 · 2.1 · x2 (0 puntos) → 2 prompts = 4 imágenes en ~35 s.
  Deletrear la tilde (`E-S-T-R-É-S with an acute accent on the second E`): salió bien en 4 de 4. Prompt entero:
  `videos/estres_cuerpo/prompt_miniatura.md`. Recorte centrado 1376x768 → 16:9 → 1280x720; mirar a 320x180.
- Si el navegador integrado no tiene la sesión de Google (pasó el 20-oct tras cambiar de cuenta de Claude), pedir al usuario
  que inicie sesión en el panel del navegador; Claude no escribe contraseñas.

## Hallazgos de freno_enojo (16-oct-2026)
- **El estilo sale a la primera** con Nano Banana 2 Lite y Omni 1.1 Flash: 50 de 50 imágenes y 6 de 7 clips en estilo, con el
  monigote reconocible. Defectos: 1 niño con pelo en vez del monigote (pedir «bald round white head, no hair») y rótulos
  «V1 V2 V3» en el nervio trigémino aunque el prompt dijera «no labels» (2 veces: se borraron con `cv2.inpaint` NS en cajas
  ajustadas a cada rótulo; con cajas grandes quedaban manchas del halo).
- **Política de Flow (video):** «a glowing yellow neon knot tightens around his throat» se rechazó, y también la versión
  con lágrima + «inside the transparent body… chemical storm». No se cobra. Evitar garganta/cuello apretado, asfixia y
  cuerpos «por dentro» con personas tristes en los CLIPS; en imágenes sí pasaron (nudo de neón en la garganta en scene-012).
  Si un clip falla 2 veces: 2 imágenes del mismo beat + mp4 propio de 10 s (zoom + fundido a la mitad), como `scene-002`.
- **Clips en el navegador integrado (sin extensión):** chip Vídeo · 360p · 10 s · x1 (7 puntos), `__ins(i)` + Return real,
  igual que las imágenes. Para bajarlos: el `<video>` de cada tarjeta solo aparece al pasar el ratón (`hover`), y su `src`
  (`flow-content.google/video/<uuid>?Expires…&Signature…`) se baja con curl sin cookies. Salen a **640x360**: la descarga
  «720p mejorada» es una descarga del navegador (no hay URL). Se reescalaron a 1080 con
  `scale=1920:1080:flags=lanczos,unsharp=5:5:0.8` (originales en `medios/_360p/`): en línea blanca sobre negro + halo de
  neón el reescalado casi no se nota.
- El uuid de la imagen-póster de un clip es el mismo que el del video: sirve para cruzar tarjetas y escenas.
- `browser_batch` admite 25 acciones: 3 por prompt (`__ins` con espera de 3 s dentro, `wait 2`, `Return`) = 8 prompts por lote.
  `__ins` devuelve `pre=` (largo del editor ANTES de borrar): `pre=1` en todos = ningún envío perdido.
- La cuadrícula «Todo» va en 2 columnas de 602 px (con viewport 1500x800): orden de envío = invertir (y, x).

## Hallazgos de agotado_cortisol (17-oct-2026, 2.º video del canal Cuerpo en Neón)
- **66 de 66 medios a la primera** (7 clips Omni 1.1 Flash + 59 imágenes Nano Banana 2 Lite): el estilo es estable. Única
  imperfección: números diminutos en una esfera de reloj y «ON/OFF» en un apagador aunque el prompt diga «no numbers».
  Los voluntarios de laboratorio salen como personas realistas (no monigote) si el prompt dice «volunteers»: aceptable.
- **El banner «Te quedan pocos puntos» sale aunque haya ~50 puntos.** El saldo real se lee en el chip: con Vídeo · 360p ·
  10 s · x1 dice «La generación consumirá 7 puntos»; al acabarse aparece el botón «Advertencia de puntos insuficientes».
  Preguntar al usuario antes de pasar un video a «todo imagen» por el banner (aquí casi se pierde el inicio en clips).
- **Proyecto nuevo de Flow = ajustes por defecto (Nano Banana 2.1 x2; en Vídeo, «Ingredientes» y x2 = 14 puntos).** Con el
  viewport emulado (1500x800) los clics por coordenadas fallan: usar los `ref` de `find`/`read_page`; los radios del panel
  van en orden fijo (`[role=radio]`: 0 Imagen · 1 Vídeo · 4 16:9 · 6 360p · 11 10 s · 12 x1).
- **Bajar clips sin pasar el ratón uno a uno:** despachar `mouseover`/`pointerover` sintéticos sobre cada `<img>` póster y
  sus 4 padres hace que aparezcan TODOS los `<video>`; su `src` firmado se baja con curl. El orden del DOM es el inverso del
  envío (v1 = último clip): identificar con una hoja de 2 cuadros por clip (s 2 y s 8) antes de renombrar.
- `nuevo --secuencia` no crea `medios/`: crear la junction a E: antes de `flow_integrado.py bajar` (si falta, curl da
  «200 0 bytes» y el script marca FALLO).
- Reparto de beats cambiado a mitad (todo imagen → 7 clips): las imágenes ya hechas se renumeran con un desfase en
  `hacer_prompts.py` y en la página basta con rehacer `window.__I` (no hace falta volver a pegar el paquete).
- Voz: con `[tired]` delante, «Son las 11 de la noche» se tragó el «Son» en 3 semillas (Whisper: «A las…», «Soy a once…»);
  se arregló con «Las 11 de la noche.» (falsos positivos aparte: «Uno.» → «1.», «Zeigarnik» → «Seygarnik»).

## Hallazgos de estres_cuerpo (20-oct-2026, 3.er video, 13:22, recopilatorio de 5 zonas)
- **Rótulos: NO al centro cuando el personaje está al centro.** Con `y=.5, x=.5` (el valor por defecto) 12 de 38 rótulos
  taparon justo el neón que nombraban o la cara («1 EL PECHO» sobre el aro del pecho, «4 FUERA DEL CUERPO» sobre la cara). Se
  movieron al hueco lateral (`x≈.2`; partidos en 2 rótulos a `y=.43/.57` si son largos; `y=.09` arriba si la escena es ancha).
  Regla: al escribir `efectos.py`, todo rótulo que nombra lo que brilla va fuera del personaje. Revisar con
  `python videos/estres_cuerpo/_hoja_rotulos.py <carpeta_v> <salida.jpg> TEXTO…` (960x540 con la capa aplicada,
  sin render) o `fab.py <v> fx hoja` (todos, 480x270).
- **Corregir rótulos sin rehacer el render de 1 h:** en secuencia no hay `--rehacer` ni segmentos, y `final` borra
  `video_sin_audio.mp4`. Receta: pista de video del MASTER con `-c:v copy` → `video --tramo a-b` por cada rótulo (~15 s c/u) →
  empalme cuadro exacto (`videos/estres_cuerpo/_empalmar_tramos.py`: `trim`/`concat`, libx264 crf 18) → `final` + `verificar`. El tramo debe empezar ANTES del fundido entre
  beats: si empieza dentro, el motor no conoce el beat anterior y la costura salta (medir el salto entre cuadros en cada costura).
- 152 medios sin ningún fallo de estilo; 7 clips al inicio (0-70 s) + imágenes cada 4-5,5 s bastaron para 13 min sin quietos.

## Hallazgos de nervio_vago (21-oct-2026, 4.º largo, 9:53, un solo tema + historia + mitos + 5 técnicas)
- **120 de 120 medios** (7 clips + 113 imágenes) con UN fallo de imagen («surgeon's gloved hands holding a tiny implant» →
  rehecha como «implant resting in the open palm of a gloved hand») y UN rótulo inventado («airflow in» junto a una flecha:
  evitar flechas con «air flowing in»). Personaje nuevo «la chica» (bufanda + cárdigan) y un científico real (Loewi) en
  «realistic fine white engraving»: los dos consistentes en 20+ imágenes.
- **Anatomía en los CLIPS:** dibujarla en un busto clásico de mármol o en un maniquí de vidrio, nunca en una persona: 2 de 2
  pasaron (en estres_cuerpo la cabeza anatómica de una persona se rechazó).
- **Bajar clips:** los pósters `<img>` se vuelven `<video>` al despachar `mouseover`; añadir `/image/<uuid>` de los clips a
  `window.__seen` y filtrar `__col` por `/image/` (si no, los pósters cuentan como imágenes nuevas).
- **`fx hoja` antes del render (no después):** detectó 8 rótulos sobre el neón o cortados por el borde, y que «→» no existe en
  Poppins (sale un cuadro: usar «·»). Un rótulo de 2 palabras largas a x ≥ .8 se sale: partirlo en 2 líneas (y .43/.57).
- Render de 593 s con FX `neon` en todo el video: 6082 s (10x tiempo real) con otro render recién acabado; encolar con un bucle
  que espera el PID del otro render en vez de lanzar dos a la vez.

## Shorts derivados de un largo (21-oct-2026: `short_suspiro`, `short_pendientes`, `short_dientes`)
Pedido del usuario: el canal no tenía impresiones (1 suscriptor, nicho de salud); un Short por largo como motor de alcance.
- **Una técnica por Short**, ~50-60 s: gancho nuevo en pregunta (o la frase-prueba del largo si ya es pregunta: «¿Tus dientes
  se están tocando?») → la técnica con las tomas del largo → cierre nuevo «hay N más… en el video completo».
- **Voz sin gastar de más:** las frases idénticas al largo se copian de `<largo>/voz/final/<clave>.wav` a
  `voz/cands/<clave_nueva>_s1.wav` antes de `voz`; ElevenLabs solo pide gancho y cierre (~100 créditos por Short).
  Copiar también los `CER_MAX_POR_FRASE` de esas frases (Zeigarnik → «Seygarnik»).
- **`BPM = 160`** en guion.py: con 80 la línea de tiempo redondea cada escena a bloques de 3 s y metía hasta 3 s de silencio.
- **Imágenes:** las del largo (1376x768 originales) reencuadradas con `nucleo/vertical_desde_largo.py` desde
  `videos/<short>/medios_del_largo.py` (beat → medio, ancho visible .40-.50, foco x): banda centrada en y=.56 que se funde a
  negro; en este estilo no se nota el borde. Ancho visible < .30 amplía > 2,6x y se ablanda la línea: solo para acercamientos.
- **Rótulos** a `y=.15` (franja negra de arriba, fuera de la interfaz de Shorts), `tam` 90-170; nunca dos a la vez en la misma
  `y` (partir en `.12`/`.19` si son dos palabras). `fx hoja` ya dibuja minis 9:16 en videos verticales.
- SFX copiados de `<largo>/sfx` (no se vuelven a pedir) y Lyria nueva de 1 tramo con las escenas del Short.
- El 🎞 Montaje del panel ya muestra los verticales en 9:16 (antes la caja 16:9 los recortaba y parecían horizontales).
- «Video relacionado» del Short = el largo: la API no lo pone; Studio > Short > «Video relacionado».

## Hallazgos de duelo_cuerpo (22-oct-2026, 1.er largo de la fórmula nueva, 5:52, escalera de tiempo)
- **Flow cambió la barra del prompt:** hay un botón **«Agente»** junto al chip; un clic por `ref` equivocado lo ENCIENDE
  (`aria-pressed=true`) y el chip desaparece. Apagarlo antes de enviar nada. El chip ahora se llama «Activador de ajustes» y
  sus radios van: Imagen · 0 Imagen, 1 Vídeo, 2 16:9 … 7 x1; en Vídeo: 0 Imagen, 1 Vídeo, 2 Fotogramas, 3 Ingredientes,
  4 16:9, 5 9:16, 6 360p, 7 720p, 8-11 4/6/8/10 s, 12-15 x1-x4. Por defecto el Vídeo sale 720p · 8 s (12 puntos): pasar a
  360p · 10 s (7 puntos) con `find("360p")` y `find("10 s")`.
- **74 de 74 medios en estilo**, 0 rechazos de política (9 clips con la señora, el maniquí de vidrio, riñones y cerebro). 5
  imágenes rehechas por **figura diminuta sobre negro** (lámparas en una repisa, pastel, la señora sola de pie): pedir
  «close-up of …» o «medium close-up from the waist up of …» + un escenario concreto; si no, Nano Banana deja 70 % de negro.
- Los pósters de los clips aparecen como `<img>` nuevas DESPUÉS de que `__col` ya no las ve: antes del siguiente `__col`
  meter todas las `img` actuales en `window.__seen` (si no, devuelve los 9 pósters en lugar de las miniaturas).
- Clips identificados por orden: el DOM va del último enviado al primero (9 → 1), igual que en nervio_vago.
- Música con Lyria en 402: la biblioteca solo sugería piezas del MISMO canal (no se repite música ante el mismo público):
  `biblioteca sugerir <v> --excluir <videos del canal>` y `biblioteca buscar "<ánimo>"` encontraron piezas tiernas de
  Edsonxn (suspendido) y Crónicas del gaming.
- `_hoja_rotulos.py` hace `chdir` a la carpeta del video: pasarle la salida con ruta ABSOLUTA.
