# Prompts y control en Google Flow (video Omni 1.2 / Veo 3.1 e imágenes) — guía para TODOS los proyectos

Alta: 27-nov-2026, pedida por el usuario («investiga cómo estructurar el prompt para aprovechar al máximo Flow… y aplícalo en
este y los demás proyectos»). Investigación con fuentes oficiales de Google + pruebas reales en `videos/campana_dc_superdaniel/`.
Marcas: **[OF]** fuente oficial · **[COM]** comunidad · **[PROBADO]** comprobado por nosotros en la interfaz.

## 0. Modelos y costos (nov-2026)
- **Omni 1.2 Flash** = el modelo de video por defecto. Veo 3.1 Fast/Quality y Omni 1.1 se retiran el **5-dic-2026** [OF]
  https://support.google.com/flow/answer/16352836
- Omni 1.2: **1 punto/s a 360p**, 3 puntos/s a 720p, hasta 10 s por toma; **reescalar a 1080p = 0 puntos** (hasta 10 s) [OF]
  https://support.google.com/flow/answer/16526234 → siempre **360p** y reescalar el que sirva [OF] (blog Labs).
- Ampliar (Extend) cuesta lo mismo por segundo añadido (10 s = 10 pts) [OF][PROBADO].
- Imágenes Nano Banana 2.1 = 0 puntos [PROBADO]. Probar barato (imagen o 360p) antes de gastar.

## 1. Ingredientes: subir, NOMBRAR y citar con @ [PROBADO]
1. Subir: pegar con Ctrl+V en el campo del prompt (Chrome) — cada imagen queda en el proyecto como «image.png».
2. **Renombrar cada recurso** (abrirlo → clic en su nombre arriba a la izquierda → escribir → Enter): `daniel_cervantes`,
   `daniel_traje`, `plaza_xochipilli`… Así las menciones dicen QUÉ es cada cosa.
3. En el prompt, escribir `@` → se abre el buscador de recursos → clic en la OPCIÓN (con find: `option "<nombre> Imagen"`)
   → queda una ficha `<span class="mention-chip" data-reference-type="media">nombre</span>` y la imagen se añade sola como
   ingrediente. A veces la primera opción ya está resaltada y hay que pulsar «Añadir a petición».
4. Decir con palabras el PAPEL de cada referencia: «@daniel_cervantes is the face…», «@daniel_traje is his exact armor…»,
   «@juchipila_aerea is the real town below». Nada de etiquetas tipo `<IMAGE_REF_0>` [OF] https://aistudio.google.com/docs/omni.md.txt
5. Límite Omni: **6 imágenes** por petición, hasta 3 por personaje y máx. 2 personajes [OF]. Ampliar acepta **3** [OF].
   Referencias sobre fondo liso funcionan mejor [OF] https://support.google.com/flow/answer/16894016
6. Personajes de Flow («Caracteres») se citan igual (`@Nombre`); voz fija con `@Voice: <nombre>` solo en Ingredientes,
   una por generación [OF]. Avatar propio = `@me`.
7. **Trampa de la interfaz [PROBADO]:** en el editor de un clip, un clic que cae fuera del buscador o del panel abierto
   SALE del modo Ampliar y vacía el prompt. Usar refs de `find` (opciones, «Añadir a petición», «Activador de ajustes»,
   «Iniciar generación») en vez de coordenadas, y verificar con JS las fichas:
   `[...document.querySelectorAll('.ProseMirror .mention-chip')].map(c=>c.textContent)`.

## 2. Plantilla de prompt (Omni 1.2, Ingredientes o Ampliar)
```
@personaje is the face (rasgos clave, lentes, etc.). @vestuario is his exact outfit. @lugar is the real location.
[0-3s] <plano y cámara>: <acción 1>.
[3-6s] <acción 2>; when <evento>, the camera <movimiento>.
[6-8s] <acción 3>.
[8-10s] <remate>. He says in Mexican Spanish, calm confident voice: "<frase corta>".
SFX: <sonidos>. Ambient noise: <ambiente>. No music.
Photorealistic, natural phone-video look. Do not add subtitles, captions, on-screen text or watermarks.
```
- Orden de Google: cámara + sujeto + acción + contexto + estilo; audio aparte [OF]
  https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- **Diálogo** entre comillas en su propia frase, con idioma y tono. El español «no está evaluado» oficialmente [OF]: revisar
  el lipsync y pasar Whisper siempre (en `campana_dc_superdaniel` salió exacto a la primera [PROBADO]).
- **Bloques `[0-3s]`** = formato oficial de Veo [OF]; en Omni son aproximados: ayudan los disparadores por evento [COM].
  Una acción por bloque de 2-3 s; 3-4 acciones caben en 10 s [PROBADO: plaza → frase → armadura → despegue].
- Un solo plano: «In a single continuous shot. No scene cuts.» (Omni corta solo si no se le dice) [OF].
- Sin campo de negativos: los «Do not…» van dentro del prompt [OF]. Pedir «No music» si no se quiere música [COM].
- Texto que no se define, el modelo lo inventa: si hay letreros, escribir qué dicen [COM]. Logos: darlos como ingrediente
  (el logo PAN salió legible en el pecho [PROBADO]).
- Cámara: «static/locked off», «push in», «dolly zoom», «oner», «over-the-shoulder», «natural smartphone zoom» [OF]
  https://deepmind.google/models/gemini-omni/prompt-guide/ · Evitar nombres de cámaras de marca (Flow quemó «ARRI ALEXA»
  en un clip de la novela, `docs/formato_novela_ia.md`).

## 3. CONSISTENCIA entre clips (prioridad del usuario)
| Para… | Usar | Por qué |
|---|---|---|
| Seguir la MISMA acción/plano | **Ampliar** (editor del clip → «+» al final de la línea de tiempo → Ampliar → 3-10 s) con las referencias del personaje en el prompt | Usa los últimos 10 s como contexto; continuidad total; el resultado es UN video más largo [OF][PROBADO] https://support.google.com/flow/answer/16935718 |
| Cortar a OTRO plano con empalme exacto | **Guardar cuadro** («Save frame») del clip → **Fotogramas** (primer cuadro) | Idea del usuario (27-nov): el último cuadro abre el plano siguiente. Elegir un cuadro nítido un poco antes del final, no el borroso [COM] |
| Una transformación controlada (vestirse, cambiar de lugar) | **Fotogramas** con primer Y último cuadro (3-10 s) | El modelo solo inventa el camino entre dos imágenes conocidas [OF] |
| La identidad en todo el video | Las MISMAS imágenes de referencia en cada clip (cara + vestuario), o un Carácter de Flow | Ancla la cara; re-anclar cada 3-4 clips porque el encadenado por cuadros acumula deriva [COM] |
- Al usar un cuadro inicial, no describir de nuevo lo que ya se ve: solo lo que CAMBIA [COM].
- Poner todas las referencias desde el primer turno; añadir una a mitad puede desestabilizar la escena [COM].
- **Lección [PROBADO 27-nov]: Fotogramas desde un cuadro donde la cara sale CHICA → al acercarse, la cara se inventa**
  (salió con perilla y más pelo). Y el modo editar («Describe cómo editar este vídeo» + `@cara`) casi no cambia la identidad.
  **Receta que funcionó:** 1) Nano Banana (0 pts) con `@cara` + `@vestuario` + `@cuadro_del_lugar` → imagen del plano que se
  quiere (primer plano, cara grande); si sale abierta, editarla «tight close-up… same person as `@cara`»; 2) comparar con la
  foto real; 3) Fotogramas con esa imagen como Inicio. La cara se mantiene los 5 s. Videos > 15 s no se editan, amplían ni
  mejoran en Flow: tramos largos se reescalan en local; los cortos se bajan con «720p Resolución mejorada» (gratis).
- Truco [PROBADO]: sacar del clip 1 un cuadro limpio del personaje ya transformado (`ffmpeg -ss 7 … c1_t7.png`), subirlo como
  ingrediente (`daniel_traje`) y citarlo en los clips siguientes: fija el vestuario que inventó el propio modelo.

## 4. Personas reales y políticas
- Omni bloquea fotos de ciertas personas reconocibles; hay falsos positivos frecuentes [OF][COM]. Una persona NO famosa con su
  permiso (Daniel Cervantes) pasó sin problema, con logo de partido incluido [PROBADO 27-nov].
- Si rechaza: no nombrar a la persona en el texto, describirla («the man from @ref»), o usar Avatar/Carácter.
- Contenido realista de personas reales en redes: rotular «Hecho con IA» (Meta/TikTok/YouTube lo piden).

## 5. Bajar sin ventanas (Chrome)
Gancho en `window.fetch` que guarda las URL `flow-content.google/video/<id>?…` + `HTMLAnchorElement.prototype.click` anulado →
el botón de descarga del recurso dispara la URL → `fetch(url)` en la página y POST a un receptor local (ej.
`videos/campana_dc_superdaniel/recibe.py`, puerto 18792 con `Access-Control-Allow-Private-Network`). El 8792 dio WinError 10013.
