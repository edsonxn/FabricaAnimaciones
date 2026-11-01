# ¿Qué pasaría si la Tierra tuviera DOS Lunas? — 6 min — ESTADO
- canal: kuriox · **PROGRAMADO jue 15-oct-2026 14:00 CDMX** (https://youtu.be/ix2tlWFWjqM, privado hasta la fecha, con miniatura y .srt)
- estilo: kurzgesagt PLANO SECUENCIA (una clase `Mundo`, sin cortes) → docs/estilo_kurzgesagt.md §A · ejemplo a copiar: `videos/sol_apagado_8min/` (`mundo_espacio.py`, `mundo_tierra.py`, `mundo_comun.py`)
- etapa: **PROGRAMADO jue 15-oct-2026 14:00 CDMX** (https://youtu.be/ix2tlWFWjqM; publishAt 2026-10-15T20:00:00Z, privado hasta la fecha; fecha aprobada por el usuario el 13-oct, `--forzar` por el Short `peso_nube` 20 h antes). MASTER 5:50 verificado y revisado cada 3 s, miniatura `mini_dos` y .srt; registrado en `canales/kuriox.json` y BITACORA
- siguiente: nada con YouTube; `python fab.py dos_lunas limpiar` cuando el usuario dé el visto bueno final; a las 48 h de publicado mirar retención (`python fab.py yt metricas kuriox 90`)

## Decisiones del usuario (12-oct-2026)
- Tema elegido de 3 propuestas con datos (`canales/metricas/ideas/kuriox.md`): «dos Lunas» (referencia: Ángel Hernández, «¿Qué pasaría SI la TIERRA tuviera DOS LUNAS?», ×9,7 de su mediana, 706 k vistas). Línea: «¿Qué pasaría si…?» del espacio, como el del Sol (128 vistas, 39 % visto, ×3,4 la mediana del canal).
- Mayormente escenas en el ESPACIO (planetas, lunas, órbitas, estrellas, fondos) con acercamientos ocasionales a la Tierra en 2D (mareas, costas, cielo con dos lunas).
- Objetivo secundario: dejar un BAÚL de recursos espaciales reutilizables (planetas, lunas con cráteres, anillos, órbitas, estrellas, nebulosas). Reciclar PRIMITIVAS, nunca escenas enteras: cada escena con efectos nuevos.
- Kuriox: pausas cortas (GAP≈0,35, post ≤ 1 s), mucho movimiento, mascota Kuri (nunca el pájaro). El del Sol se sintió lento.
- Sin subtítulos quemados. Música Lyria apegada al guion. Voz: la de Kuriox (ver `videos/sol_apagado_8min/guion.py` o `historia_60/`).

## Arco propuesto del guion (a afinar en la sesión 1)
1. Gancho: la Luna ya es rara (¿y si hubiera otra?). 2. ¿De dónde sale la 2.ª luna? (captura vs. formación). 3. Dónde puede vivir:
órbitas estables, Hill, resonancia. 4. Mareas: dos tirones, costas, mareas gigantes (2D). 5. Cielo: dos lunas, noches, eclipses dobles.
6. El final posible: se acercan, límite de Roche, anillo o choque. 7. Cierre/gancho al siguiente «qué pasaría si». Verificar cifras
(distancia, masa, Roche) con fuentes antes de escribir; DOI/enlaces con Crossref/NASA, nunca de memoria.

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: dos lunas, dos lunas kuriox, la tierra con dos lunas, kuriox dos lunas
- vista previa: tras el primer tramo de escenas (sesión 2): render parcial del primer minuto y medio con `python fab.py dos_lunas video --hasta 90`; esperar el visto bueno antes de seguir
- leer al empezar: `docs/estilo_kurzgesagt.md` §A, `docs/api_kz.md` (solo grep), `videos/sol_apagado_8min/mundo_espacio.py` y `mundo_comun.py` (grep), `GUIA_ESCENAS.md` y `PLAN_TOMAS.md` de este video (se crean en la sesión 1)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion, voz, tiempo + kit espacial (planetas, lunas, órbitas, estrellas) + GUIA_ESCENAS.md y PLAN_TOMAS.md | ✅ 12-oct | guion 1 007 palabras; voz Dan 309,6 s (CER 0 en las 68 frases; reescritas hoy_1 y calor_4); tiempo 5:50; `nucleo/kz_espacio.py`; guías |
| 2 | escenas primera mitad (0:00–2:44: intro, hoy, origen, orbita, cielo) + render parcial `--hasta 90` | ✅ 13-oct | `mundo_comun/anclas/mundo_espacio/mundo_origen/mundo_orbita/mundo_tierra.py` + `escenas.py` (96 SFX); render parcial hecho; el usuario lo vio y lo aprobó (13-oct) |
| 3 | escenas segunda mitad (2:44–5:50: mareas, calor, caida, choque, cierre) | ✅ 13-oct | `mundo_mareas/calor/caida/choque.py` + anclas 6–10 + despacho y 100 SFX nuevos en `escenas.py`; tomas 9–10 probadas, empalmes 5→6→7→8→9 revisados con hoja; cierre con tarjetas movidas para no tapar la Luna. La sesión se cortó por tokens y otra cuenta la terminó |
| 4 | cierre: hoja 3 s de la 2.ª mitad → sfx → Lyria → mezcla → render → final → verificar → hoja del MASTER → miniatura → youtube.json → subida en privado | ✅ 13-oct | subido en privado (ix2tlWFWjqM), falta solo la fecha. Hoja 2.ª mitad hecha (`previews/rev/h2_01–11.jpg`) + arreglo toma 9 (`fix_a/b`: mitad derecha rellena con la otra cara, corteza, 2011, ≈1 200 km); conciliado y compilado; cierre: Luna que sube/crece en 337–350 s (`luna_c`) para que la playa no quede quieta. Sigue: sfx → musica → mezcla → video |

## Registro del tramo 4 (cerrado)
- 13-oct ~13:10: MASTER HECHO y verificado (`salida/dos_lunas_MASTER.mp4`, 5:50, 1080p, 221 MB, CER 0,14 %, −14 LUFS, desfase 0). Hoja del MASTER cada 3 s (`previews/master/m_01–13.jpg`): 3 choques de texto arreglados y rehechos con `--rehacer 261-273 311-317 322-330` («18 400 km» sobre Kuri → ángulo 2,75; «el equilibrio se rompe» sobre «segunda luna»; «HIPÓTESIS/encaja» sobre la tarjeta del panqueque → arriba y salen antes de la tarjeta «1 + 1»); comprobado en `previews/master/fix.jpg`. Siguiente: subida en privado → pedir fecha (propuesta jue 15-oct 14:00 CDMX).
- 13-oct (cuenta nueva): tramo 4 — hoja 2.ª mitad ✓, arreglos ✓, `sfx` ✓ (196 eventos), música Lyria ✓ (`lyria_tramos.py todo`, 3 tramos ya generados 11:33; `fab.py musica` ahora usa Lyria si hay `LYRIA`, antes era la procedural), `mezcla` ✓ (−14 LUFS, voz/fondo 12,8 dB). RENDER COMPLETO lanzado ~11:45 (`previews/render_log.txt`; descartó los 30 segmentos del avance por código nuevo: 117 segmentos, ~270 s c/u con 12 procesos ≈ 45 min). Hechos ya durante el render: miniaturas por código (`miniaturas.py` → `salida/dos_lunas_mini_dos.jpg` principal, `_choque` alternativa), `youtube.json` (capítulos del timeline, fuentes del docstring), helpers promovidos a `nucleo/kz_espacio.py` + `docs/api_kz.md` regenerado + HALLAZGOS en `docs/estilo_kurzgesagt.md` § baúl espacial. Después: `final` → `verificar` → hoja del MASTER → miniatura → youtube.json → subida privada.

## Hecho
- Tema, duración, plan de sesiones y carpeta `videos/dos_lunas/` (plantilla).
- Guion final (`guion.py`): 10 escenas (intro, hoy, origen, orbita, cielo, mareas, calor, caida, choque, cierre), 68 frases, 1 007 palabras (≈ 5:45–6:10 con Dan). Docstring con las cifras y fuentes verificadas; DOI de Jutzi y Asphaug 2011 comprobado en Crossref. Gancho/remate: la 2.ª luna del final (hipótesis de Jutzi y Asphaug, luna de ~1 200 km en un punto troyano que se aplastó en la cara oculta) está sembrada en `intro` y en `orbita` (L4/L5).
- Kit `nucleo/kz_espacio.py` (+ `docs/estilo_kurzgesagt.md` § baúl espacial, `docs/api_kz.md` regenerado): cuerpos rocosos con fases, luna que se rompe, gigantes, anillos, órbitas, Hill, Lagrange, mareas, diagramas. Hoja de prueba: `_hoja_kit.py` → `previews/kit_hoja.jpg`.
- `GUIA_ESCENAS.md` y `PLAN_TOMAS.md` (10 tomas con tiempos estimados; «Estado del código» cubre las 10).
- Tomas 6–10 (2:44–5:50) dibujadas y probadas, 196 SFX registrados en `escenas.py` (13-oct-2026).

## Revisión del AVANCE (13-oct-2026, 30 cuadros a tamaño completo, uno cada 3 s)
Render parcial 0–90 s: 968 s con 8→12 procesos (RAM limitada por un `chatterbox_server.py` ajeno); `salida/dos_lunas_AVANCE.mp4`, 1920x1080, voz + SFX
provisionales (`sfx` + `mezcla` sin música: -14 LUFS). Sin defectos bloqueantes (sin texto fuera de cuadro, sin cuadros negros, cada toma con su propio tinte de fondo).
Mejoras candidatas (no hechas para no invalidar los segmentos ya dibujados; aplicar con `video --rehacer` si el usuario las pide o tras su feedback):
- 22–27 s (Luna que ya conocemos) y 60–62 s (antes de 2024 PT5) son las partes más quietas: empuje lento de cámara (`cam_claves` z 1,17→1,26 en 24–30,4; z 1,05→1,10 en 44,5–66,5).
- Barquito de la marea (31–36 s) y fila de años de Jano/Epimeteo son pequeños; subir su tamaño si se ven pobres en el MASTER.
- Toma 4 (Hill, 88–99 s) la Tierra queda de ~44 px; si se ve vacía añadir más elementos de la escala (Sol, otras órbitas).
- Pendiente de la toma 4–5 (83–164 s): se probó con hojas y `_cuadro.py`, **aún sin render** (se renderizan en el cierre).

## Falta
- [x] Visto bueno del usuario al AVANCE (90 s): aprobado el 13-oct, sin ajustes (las «mejoras candidatas» de arriba quedan opcionales).
- [ ] Antes del render largo: hoja 2×3 a tamaño completo, 1 cuadro/3 s, de 2:44–5:50 (rigor); vigilar toma 9 a 289–301 s (la mitad derecha del cuadro queda
  vacía con la Luna a la izquierda y rótulos arriba: añadir elementos de relleno si se ve pobre) y los 12 s de playa quieta del cierre (337–349 s).
- [ ] En el cierre: promover al kit (`nucleo/kz_espacio.py`) los helpers genéricos de `mundo_espacio.py` (`fantasma`, `marca_x`, `bez2`, `kepler`, `trail`) y regenerar `docs/api_kz.md` + `docs/estilo_kurzgesagt.md` (baúl espacial).
- [ ] Tramos 3-4 de la tabla de sesiones.

## Cómo retomar (comandos)
```
python fab.py continuar dos lunas
python fab.py estado dos_lunas
```

## Archivos clave
- `guion.py`, `GUIA_ESCENAS.md`, `PLAN_TOMAS.md` (con «Estado del código»), `_hoja_kit.py`, `_cuadro.py` (cuadro 1920x1080 de un t global); `escenas.py` + `mundo_*.py` (espacio, origen, orbita, tierra, mareas, calor, caida, choque) + `anclas.py` (tomas 1–10). Kit: `nucleo/kz_espacio.py`. Ideas con datos: `canales/metricas/ideas/kuriox.md`.

## Lecciones de este video (solo lo no obvio)
- «81 veces» → el normalizador de Whisper lo lee «ochenta y uno» (≠ «una»), «384 mil» sale como 384.000 y «Ío» se oye «ello/dio»: escribir «unas ochenta veces», «unos cuatrocientos mil» y evitar «Ío» en frases sueltas.
- La voz compite por la GPU con otros videos (12-oct: `viajeros_tiempo` generaba voz a la vez): mirar `nvidia-smi` y `tasklist` antes de lanzar `voz`.
- Nombres difíciles para Whisper en la narración: «Jano y Epimeteo», «Tritón», «Fobos», «Fundy», «Ío», «límite de Roche»; si una frase falla 4 tomas, reescribir (docs/voz.md).
- Hecho distinto al guion de referencia: a la órbita de una luna segunda a 192 000 km la marea NO la acerca (está por encima de la órbita síncrona, 42 164 km): por eso la caída del guion usa luna retrógrada (Tritón) o más rápida que el giro terrestre (Fobos).

- Plano secuencia con `Mundo` único: `cam_claves(t, [(t, ancla_mundo, punto_pantalla, zoom)])` (zoom en escala log, suavizado entre claves) es la forma
  barata de dirigir la cámara toma a toma; Kuri y los rótulos son overlays con posición por claves (`kf`) y hay que empalmarlos entre tomas.
- `P.pastilla`/`rotulo` (Poppins) NO tienen el glifo «→» (sale un cuadrado): usa «–» o palabras. `P.arbol` de noche dibuja un disco de brillo que parece una luna: en
  el cielo con dos lunas usa un árbol propio (`mundo_tierra.arbol_noche`). Recuadros con contenido recortado: `lz.capa(2)` + `lz.grupo(cx,cy,k)` + `lz.recorte(rect_red local)`.
- Trayectorias: Bézier cuadrática hasta el periapsis + `kepler(a, e, w, M)` para el asteroide capturado (queda una elipse que se dibuja punteada); estelas con
  `trail(lz, f, t)` (f = posición en pantalla en función del tiempo, también para tiempos anteriores: si no, salen líneas rectas raras).
- `fab.py <v> escena <id> t1 t2…` usa tiempos GLOBALES y en un plano secuencia todas las escenas son el mismo `Mundo`: el `<id>` solo da el nombre de la hoja
  (`previews/esc_<id>.jpg`); úsalo para repartir hojas por empalme (mareas/calor/caida/choque). Rótulos y tarjetas: comprobar su rectángulo contra el
  foco (la Luna del cierre quedaba tapada por la 2.ª tarjeta a x = 1260).
- Corte de sesión por tokens (13-oct): el código de las tomas 6–10 estaba escrito pero el ESTADO.md no; `fab.py continuar` ahora avisa de archivos más nuevos
  que el ESTADO.md (protocolo: `docs/sesiones.md` §6).
- Coste: el Hill + varias nebulosas suben a ~1,2–1,9 s por cuadro; el resto 0,5–0,7 s. Con 8 procesos (RAM limitada por `chatterbox_server.py` ajeno) 90 s tardan unos minutos.

## Cierre (regla del 12-oct-2026)
- [x] subido (privado), miniatura, .srt y registrado (`canales/kuriox.json`, BITACORA) — [x] programado jue 15-oct-2026 14:00 CDMX
- [x] HALLAZGOS y mejoras documentados en docs/estilo_kurzgesagt.md § baúl espacial; helpers `fantasma/marca_x/bez2/kepler/trail` promovidos a `nucleo/kz_espacio.py` (el video conserva sus copias locales) y `docs/api_kz.md` regenerado; `fab.py musica` ahora usa Lyria si el guion tiene `LYRIA`
