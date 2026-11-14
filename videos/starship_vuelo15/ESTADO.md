# Starship vuelo 15 explicado en 3D — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: T Menos Cero (`t_menos_cero`) · 1.er video del canal · al terminar: subir y programar (hueco de `canales --actualizar`: URGENTE, hoy)
- estilo: LÍNEA 3D (`nucleo/linea3d.py` + `linea3d_starship.py`) + video real de SpaceX con capas · ejemplo `videos/cohete_crs30/` · doc `docs/estilo_linea3d.md`
- etapa: MASTER hecho (10:10, verificar OK CER 0,15 %) · SUBIDO TJvawxDLQnE, programado sáb 14-nov 19:00 CDMX · en la tele
- siguiente: aplicar la miniatura que elija el usuario (`yt aplicar starship_vuelo15 t_menos_cero TJvawxDLQnE` tras cambiar `miniatura` en youtube.json) · al cerrar: `biblioteca sfx catalogar`, lecciones en docs/estilo_linea3d.md, `limpiar`, commit

## En curso (14-nov-2026 16:40 CDMX, sesión 1 cortada por contexto)
- Resultado comprobado: nave 42 ATRAPADA (T+22:32:28, 21:20 UTC) en la torre de la plataforma 2; B22 abortó la captura (automático), al golfo, se desintegró. Datos y fuentes: docstring de `guion.py`.
- Voz: 103 frases ElevenLabs Alberto, todas válidas (`CER_MAX_POR_FRASE` para 4 frases que Whisper escribe a su manera); `idioma_voz` OK. NO tocar el texto (las anclas `ww` dependen de él).
- Código: `comun.py` (anclas `ww/F0/F1/T0/T1`, `ap/vent`, RELOJ de misión monótono, EVENTOS, `motores_sh/nave`, HUD con panel de 33 motores (el n.º 21 = el que no reencendió, con X) y de 6, `real()` = clip a pantalla completa recortado y desaturado + capas, geografía `SB` (torre 2 OSM 25.99705,-97.15807) + costa OSM `datos/osm_costa.json`, trayectorias `p_asc`/`p_boo` esquemáticas, `orbita_eci`).
  `planos1.py` (gancho → separación, 16 planos) y `escenas.py` (montaje: lista PLANOS de planos1 + `P2.PLANOS` + `P3.PLANOS`; `sfx()` de cada módulo). Hoja: `python _hoja.py t1 t2 … --out x`.
- Hoja del gancho (`previews/h_gancho.jpg`) revisada: ARREGLAR (1) en los clips queda el rótulo «VIEWS BY STARLINK» de SpaceX arriba a la derecha encima de nuestro «VIDEO: SPACEX» → recortar más arriba (`cy`) o tapar con banda; (2) `g_captura3d` (18-24 s) la torre y la nave salen chiquitas: acercar la cámara a ~0,15 km; (3) `g_booster` (24-29 s) propulsor diminuto: acercar. El resto de planos1 SIN revisar en hoja.
- Clips (crédito SpaceX, vía VideoFromSpace): `clips/lanz_a.mp4` = seg 600-1240 de F0ltKM5qc7A (T+0 = seg 76,5 del clip; separación en caliente 217,5; vistas del propulsor en pantalla dividida 290-440);
  `clips/regreso_full.mp4` = KqGPHd7XAbs (seg = T+ − 80300; plasma 225-360; giro 838; CAPTURA 848; vista desde lo alto de la torre 849-853; dron con la nave en la torre 990-1080);
  `orb_1150.mp4` (T+8:06 en seg 0; SECO), `orb_4395.mp4` (Tierra, T+1:02), `orb_5790.mp4` (alerón sobre nubes, T+1:25). `lanz360.mp4` solo para localizar (T+0 = seg 675).
- OJO: el rótulo «VIEWS BY STARLINK» = video que viaja por la red Starlink, NO cámaras de los satélites (ya corregido en el guion).

- 14-nov 17:20: no se pudo abrir sesión de relevo (turno de aviso programado): seguí en el mismo hilo.

- Miniatura: el usuario elige entre `miniatura/propuestas/` (A1…D2 + la mía, la E) desde la sesión principal; si el render acaba antes, subir con `miniatura/miniatura.jpg` y cambiarla después con `yt aplicar`.

## Falta en orden (plan de planos2/planos3, anclas por frase del timeline)
- planos2: propulsor (3D media vuelta + panel con el motor que falla; cae de cola con 3 aletas; mapa OSM de Starbase con la ruta que se desvía al golfo + «ABORTO AUTOMÁTICO», cita Musk «BAJO RENDIMIENTO · POCO COMBUSTIBLE» / «SPACEX INVESTIGA»; se desintegra; torre vacía «CAPTURA DOBLE: PENDIENTE»),
  órbita (3D nave 6 motores 3+3; clip `o1150` en «los apaga» con SECO; globo con quema de inserción de 1 motor 20 s, anillo de órbita 275 km e inclinación 30,5°), starlink (compuerta + satélites saliendo con contador; rejilla de 60 con 26 llenos; 3 con cámara mirando el escudo; clip `o4395` «VIDEO EN DIRECTO VÍA STARLINK»),
  vueltas (globo con traza de 14 vueltas, reloj rápido, 3 puntos de control con ✓ «SÍ» ×3; sin decir que pasa sobre Hawái), reentrada (quema de 10 s, plasma alrededor de la nave de panza, losetas hexagonales, alerones; clip `reg` 225-360), llegada (mapa de Starbase, planeo de panza, giro, 3→2→1 motores en el panel, torre; clip `reg` desde 838,5 para que la captura 848 caiga en «atrapan»).
- planos3: lenta (3D a cámara lenta: brazos que se cierran, pernos bajo los alerones delanteros, «SIN PATAS»), importa (diagrama: transbordador planeando / etapas en el mar / S42 de pie ✓, B22 ✗; Luna), sigue (clip `reg` 990-1080 dron), cifras (tablero), cierre (suscripción como `cohete_crs30`).
- SFX: `sfx()` por módulo con los nombres de `SFX_ELEVEN`; música: `python fab.py biblioteca sugerir starship_vuelo15`.
- Luego promesas.md, FAB_FX no aplica; `chequeo` si existe para este motor; video → final → verificar → tele master → miniatura Flow → `yt subir … t_menos_cero private --publicar <hueco>`.

## Sesiones
- ✅ 14-nov-2026 (1, mismo hilo tras el corte): planos2/3, hojas, música, SFX, mezcla, render, final, miniatura Flow (E), subida programada.
- ◐ 14-nov-2026 (1a): resultado comprobado, `nuevo`, guion (1 286 palabras, 10:10), voz + timeline, clips, comun.py, planos1.py, escenas.py. Cortada por contexto.
