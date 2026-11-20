# Carrera de motos en el cañón: horarios y mejores curvas (reel vertical 3D) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: ninguno · Facebook de Edson (lo sube él) · URGENTE: la carrera es el dom 15-nov-2026, el video debe salir HOY sáb 14
- estilo: 3D propio (relieve Terrarium/SRTM + satélite Esri, three.js en Edge sin ventana, cámara orbital) + clips reales del reconocimiento oficial que se vuelven tarjeta clavada en el 3D + rótulos por código · vertical 1080x1920 · voz = clon de Edson
- etapa: ✅ MASTER ENTREGADO 14-nov-2026 13:20: `salida/jch_carrera_donde_verla_MASTER.mp4` (175 s, 1080x1920, 429 MB, −14 LUFS, verificado) + copia ligera `salida/jch_carrera_donde_verla_FACEBOOK.mp4` (247 MB) mandada al celular por Rayo (Edson: «a la tele no, por Rayo») · ✅ PUBLICADO 14-nov-2026 14:13 en el PERFIL PERSONAL de Facebook de Edson (público, como reel de 2:55): https://www.facebook.com/reel/1870559407448987/
- siguiente: nada pendiente de publicar (solo el perfil personal; NO se subió a la página «Que pasa en Juchipila» ni a YouTube). La etiqueta de IA de Facebook quedó apagada (valor por defecto; la voz es la clonada de Edson: si la quiere, se activa editando la publicación). Si pide cambios: `python render3d_jch.py --rango a b --rehacer` (si cambia `plan3d.py`) + `python fab.py jch_carrera_donde_verla video --rehacer a-b` + `final`; al aprobar: `python fab.py jch_carrera_donde_verla limpiar`

## Sesiones
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación, geometría medida, guion, voz, tiempo, visor 3D (sin probar) | ✅ cerrado 20-nov (el video ya está subido) | corte por contexto a 180 mil |
| 2 | terreno y visor probados, `plan3d.py`, `render3d_jch.py`, render 3D completo, clips + fx.wav, `escenas.py` escrito | ✅ cerrado 20-nov (el video ya está subido) | corte por contexto a 180 mil |
| 3 | (mismo hilo de relevo) escenas probadas y pulidas, promesas, música, mezcla, `salida/post_facebook.md`, cadena de render en espera | ✅ 14-nov | MASTER verificado (render 13:12-13:17 tras pausar Edson `tes_reina_loba`), hoja del MASTER revisada, enviado por Rayo, aviso por voz |
| 4 | publicación en el perfil personal de Facebook (Chrome, sesión de Edson) | ✅ 14-nov 14:13 | https://www.facebook.com/reel/1870559407448987/ · video idéntico al `_FACEBOOK.mp4` (SHA-256 comprobado en la página) y texto idéntico a `post_facebook.md`; público, 175 s. Cómo: `file_upload` de la extensión solo admite 10 MB por llamada → 27 trozos de 9 MB a `<input type=file>` temporales, unidos en la página con `new File` + `DataTransfer` sobre el input del cuadro «Crear publicación»; texto pegado con un evento `paste` sintético. Facebook lo trata como reel aunque dure 2:55 (ya no recorta a 90 s) |

## Decisiones (Edson, 14-nov-2026)
- horarios + dónde verla; 3 min vertical; SU VOZ CLONADA (ya generada); «escenas 3D y cámara orbital sobre satélite»; cada punto abre con su clip REAL (3 s con su sonido), se congela y el cuadro vuela como TARJETA hasta clavarse en su curva del 3D
- NO se toma postura sobre el cierre; no se dice el número de la carretera

## Datos comprobados (fuentes en el docstring de guion.py; NO cambiar de memoria)
- dom 15: control vehicular 10:00 · carrera 12:00, salidas cada 30 s · circulación normal a más tardar 13:30 · gratis · llegar antes de las 10 · 27.5 km, 97 curvas, 100 pilotos, ~50 marshals
- km de carretera = 78 + km del trazo. La Herradura km 82 (144° der, 140° izq) · Las Palmas km 87 (153° der) · Tráiler Quemado km 92 (142° der + 117° y 121°; a 12.3 km de Los Burritos) · Santa Rosa km 94 (puente 1 143 m; cima 1 630 m en km 5.9) · meta Los Burritos km 105
- clips (`_clips.py`, tabla `CL`): Alice Reyes 97 `_2HqpvYxpQ0` (720p; `salida.mp4` trae el rótulo «Practica Ruta CAIN ROAD RACE 2026») y dron de Los Burritos `QlVO3wmW0co` = DD On The Road, rodada de ene-2025 (NO es la carrera: solo se usa como «Los Burritos desde el aire» en el punto 5; trae música → va con el sonido de `meta.mp4`). Los clips a bordo no traen música (espectrograma revisado)

## En curso
- Nada pendiente de producción. No se sube a YouTube. Música: `mods_ia_fusion__lyria_1` + `cfo_kc_worlds__lyria_tramo1` (biblioteca). `audio/fx.wav` a 48 kHz (`_clips.py`). Segmentos conservados para arreglos por tramos.
- Niveles medidos en el MASTER: motor de los clips −14/−15 dB medios, voz con música −16.5 dB (si Edson siente fuerte el motor: `MEZCLA fx=-12` y `mezcla` + `final`).

## Cómo está armado (para no releer código)
- `terreno3d.html`: capas lejos/valle/corr_s/corr_n + 6 parches z18; las gruesas se HUNDEN bajo las finas (`hundido`), todas escriben profundidad; cinta y motos con sesgo de profundidad en metros (`cinta.sesgo`), pegadas al asfalto; `bandas` sin prueba de profundidad. `_terreno.py` iguala el color de `lejos.jpg` al valle.
- `plan3d.py`: `ww()`/`T0()`; `CLIPS` (cuándo el clip tapa el 3D), `TRAMOS` de claves `K(t, centro, az, el, d, fov)` (az 0 = cámara al sur mirando al norte) interpolados con PCHIP; la cámara nunca baja del relieve; `plan(t)` (cinta/hi/motos/haces/zona por sección); `ANCLAS` (puntos con nombre + zA, zE, x1, x2, xm, km12, gdl, cima, km0, m00…m49).
- `escenas.py`: `cuadro(t)` = `fondo3d` + `clip_punto`/`cabecera` + sección + crédito + `barrido` (franja negra/amarilla en `BARRIDOS`). Sprites cacheados `s_txt`, `s_chip` (paralelogramo), `s_pin`, `s_fila`, `s_regla`, `s_icono`; `pega()`, `chip()`, `texto()`, `rotulo()` (etiqueta unida a un ancla 3D), `perfil()`.

## Lecciones de este video
- Trazo: medir sobre el eje de la carretera en OSM y comprobar inicio y fin en el satélite (el OSRM del reel anterior empezaba dentro de Jesús María).
- Whisper escribe «1.» por «Uno:» y «Moyagua»: CER_MAX_POR_FRASE tras leer `voz/eval.json`. `cv2.remap` no admite mapas de más de 32 767 columnas. Esri World Imagery llega a z18 en el cañón.
- Terreno por capas en three.js: si las capas finas no escriben profundidad, los cerros no se tapan bien; si la escriben, la malla gruesa asoma («lagunas» cafés) → hundir la gruesa bajo la fina con la misma rampa del difuminado. La cinta levantada se despega del asfalto: mejor 3 m + sesgo de profundidad en metros.
- Cámara «a bordo» a menos de ~500 m del suelo: la textura z18 se ve borrosa y la malla quebrada; mínimo el 20-27°, d ≥ 540 m.
- Cadena de espera de render: invocarla SIEMPRE con la ruta que lleve el nombre del video (`bash videos/<v>/_cadena.sh`); lanzada como `bash _cadena.sh` su filtro «otro render» se cuenta a sí misma y se espera para siempre.
- Rótulos sobre un 3D que orbita: reservar zonas fijas (cabecera arriba, etiqueta secundaria a la izquierda bajo el km, tarjeta a la derecha, perfil abajo) y dar a las etiquetas ancladas un tope `ymax`; el perfil se quita antes de que entren los ángulos.
