# «La obra»: vista RTS de lo que se está produciendo (pedido del usuario, 19-nov-2026)

Pedido: al hacer clic en una obra de la ruleta «En producción» (pestaña «Canales», `nucleo/estadisticas.html`, tarjetas
`.tl-p`) se abre un pop-up en la misma ventana con una escena tipo estrategia en tiempo real (vista 3/4 isométrica, bosque):
aldeanos llevan recursos (madera, silicio, componentes de computadora, rollos de película) al edificio en obra, otros
martillan, la cámara se mueve sola como en un RTS y arriba del edificio se ven vistazos de lo que se genera del video
(como el monitor del robotaller). La misma escena reemplaza al robotaller en la tele (tablero de Puente TV).
**Arte y sonidos ORIGINALES** «en el espíritu de» los RTS medievales de fines de los 90: nada copiado de Age of Empires
(ni sprites, ni sonidos, ni nombre en pantalla). Ya se le dijo al usuario.

## Hecho (19-nov)
- `flow/*.jpg`: 8 dibujos de Flow (Nano Banana 2.1, 0 puntos, fondo magenta). Proyecto Flow «nov 19 - 12:54».
- `preparar_arte.py` → `img/*.png` (sprites al doble de su tamaño en pantalla, transparencia limpia) + `img/pasto.jpg`,
  `img/tierra.jpg` (512 px, repetibles) + `img/hoja.jpg` (revisión). Piezas: cimientos, armazon, taller (edificio por
  etapas); madera, silicio, componentes, pelicula (montones de recursos); roca, piedras, arbusto, arbusto_flor, tocon,
  barril, cajas, carretilla, costal, cerca; roble, pino, abedul, castano, pino_chico, arce.
- Pantalla pintada en el techo de `img/taller.png` (758x800): paralelogramo TL (416,172), TR (599,81), BL (416,314),
  BR (600,218). Para pintar ahí: `ctx.transform(183/w, -91/w, 0, 142/h, 416, 172)` en coordenadas del sprite.
- `sonido/*.mp3` (ElevenLabs, 332 créditos; NO va a git): martillo_1-3, hacha_1-2, pico_1-2, deposito_1-2, sierra,
  ambiente (20 s, en bucle), listo (fanfarria).
- Datos ya listos en `estadisticas.py`: `datos_panel()` → cada canal trae `prod` (video, titulo, progreso, etapa_n, mini,
  mini_final, sale, atrasado) y `libres` (huecos por llenar), `logo`, `color`.

## Falta (en orden)
1. **`nucleo/panel_obra.html`** servida en `/v2/obra` (`?video=<v>` enfoca esa obra; `?tele=1` = sin sonido, media
   resolución, menos aldeanos). Rutas en `panel_v2.py` → `get()` (se recarga solo, sin reiniciar el panel): `/v2/obra`,
   `/v2/obra/img/<n>`, `/v2/obra/sonido/<n>` (lista blanca de nombres), `/api/v2/obra`. En `panel_v2.py` el panel es `P`
   (`P.estado_cache()`), NO `import panel` (el panel corre como `__main__`): `estadisticas.datos_panel(P.estado_cache(30)["proyectos"])`.
   La API: obras [{video, titulo, canal, canal_nombre, color, progreso, etapa_n, sale, atrasado, vistazos: [/media/<v>/previews/*.jpg …]}],
   libres [{canal_nombre, logo, sale}].
2. Motor (canvas 2D): mundo 3200x1800; suelo pre-dibujado una vez (patrón de pasto, manchas, claro de tierra con máscara
   de degradados alrededor de cada obra, caminos de tierra a cada recurso); árboles de la orilla «horneados» en el suelo,
   los cercanos a la acción se dibujan cada cuadro ordenados por y; sombras elípticas.
   Obras: 1 → (1600,950); 2 → (1150,900),(2100,1000); 3 → (1000,1000),(1700,800),(2350,1100); 0 → taller terminado y
   letrero «Sin obras». Etapa por progreso: <0,3 cimientos · <0,7 armazón · ≥0,7 taller (+ andamio dibujado si <0,97);
   al cambiar de etapa, nube de polvo. Barra de construcción verde encima (estilo RTS). Vistazos cada 4 s: en la pantalla
   del techo del taller (transform de arriba) o, en etapas 1-2, en un letrero de obra flotante con cuerdas.
   Recursos: madera (bosque oeste ~500,900, un leñador talando), silicio (afloramiento norte ~1500,330), componentes
   (este ~2750,600), película (carreta sureste ~2600,1500). Huecos «por llenar»: terreno con estacas y letrero del canal.
   Aldeanos dibujados por código (~34 px de alto): piernas alternas, túnica del color del canal, cabeza, sombrero de paja
   en algunos, herramienta; recolectores: ir → trabajar 3-5 s (hacha/pico/recoger, con sonido) → volver cargando el
   recurso (sprite chico) → descargar (sonido) → repetir; constructores alrededor de la obra martillando.
   Cámara RTS: recorrido (obra de cerca, seguir a un aldeano 6 s, zona de recurso, vista general) con resorte suave; en el
   pop-up arrastrar/rueda la mueven a mano y a los 10 s vuelve al recorrido. HUD en HTML: barra de recursos arriba
   (cuenta entregas), minimapa abajo a la izquierda (obras, aldeanos, rectángulo de cámara), panel de la obra abajo
   (título, canal, % y etapa, «sale <fecha>»). Sonido WebAudio: ambiente en bucle 0,35; golpes con volumen y paneo por
   distancia a la cámara; botón 🔊; si el AudioContext queda suspendido, «Toca para sonido». `window.__pausa(si)` para la tele.
3. **Pop-up** en `estadisticas.html`: clic en `.tl-p` (no `.libre`) → capa fija con `<iframe src="/v2/obra?video=<v>" allow="autoplay">`,
   ✕ y Esc cierran; `cursor:pointer` en las obras. Ojo: el arrastre de la ruleta ya cancela clics (`TL.mov`).
4. **Tele**: `D:\PuenteTV\tablero\tv.html` línea ~476 `$("fVivo").src=conK("/v2/vivo")` → `/v2/obra?tele=1`; en
   `D:\PuenteTV\tablero\servidor.py` agregar a la lista blanca del proxy `/v2/obra`, `/api/v2/obra`, `^/v2/obra/(img|sonido)/…`
   y `/media/<v>/previews|salida/*.jpg`; reiniciar SOLO ese servidor (pythonw en el 8741; LEEME de esa carpeta). Medir
   fluidez con `bash D:/PuenteTV/tablero/medir_fps.sh "tv?vista=1"` (robotaller daba ~32 fps). Título del chip de la vista 1.
5. Probar en el panel (navegador integrado, `http://127.0.0.1:8765/canales` → clic en una obra) y en la tele; commit
   (sin `sonido/` ni `flow/`, ya en .gitignore); documentar en `docs/panel.md` y `docs/tele.md`.
