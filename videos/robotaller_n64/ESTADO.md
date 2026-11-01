# Así se hace por dentro: un video de 24 min en 4 horas (Edsonxn, 2.º video) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: edsonxn · PROGRAMADO sáb 7-nov-2026 10:00 CDMX: https://youtu.be/ALhXMUAc_RI
- estilo: Jefe de Robots: grabaciones reales con cámara + Token de acento + El Jefe → doc: docs/estilo_jefe_robots.md (copiar de videos/robotaller_mes1/)
- etapa: SUBIDO en privado y programado (1-nov), registrado en canales/edsonxn.json y BITACORA
- siguiente: comprobar en Studio «Contenido alterado» = Sí; medir a 7 días (retención, suscriptores, comentarios)

## En curso (1-nov-2026, 2.ª sesión — manda sobre lo de abajo)
2.ª sesión: las 19 grabaciones hechas y miradas (montaje.mp4 negro hasta 4 s → desde 5). `toma.py` escrito (69 planos, `python toma.py revisar` limpio). Token grabado (medios/token.mp4). efectos.py + 15 SFX nuevos (93 créditos) + sfx/ost_yoshi.mp3 hechos; descripcion.txt escrito; filtro limpio.
**PRIVACIDAD (1-nov):** `robotaller._USUARIO` tenía caracteres de retroceso en vez de la marca de límite de palabra y NO tapaba el usuario de Windows (se veía en voz_eleven). Arreglado en nucleo/robotaller.py; regrabando las 19 tomas del panel (`_cap5.log`). Ojo: el piloto robotaller_mes1 se grabó con el fallo: revisar. chequeo_yt.py:39-40 tiene el mismo problema (sin tocar).
Tomas del panel regrabadas y comprobadas (API tapada: 0 apariciones del usuario en las 3 sesiones). medios/toma.mp4 (69 planos) + partir hechos; fx (72 sonidos, OST Tetris 64 en «canciones» y Yoshi Valley en «Escucha») y mezcla (−14,08 LUFS) hechos.
**MASTER LISTO (1-nov):** `salida/robotaller_n64_MASTER.mp4` (5:00, 1080p) + `.srt`; verificar OK (CER 0,09 %, desfase 0); filtro limpio; hoja cada 10 s revisada (`previews/_master_10s.jpg`). 2.ª pasada: junta_0 = m_iwata (el Montaje del panel se regrabó en blanco), planos de investiga acercados al texto. Aviso por voz dado.
**VISTO BUENO DEL USUARIO (1-nov, vía la sesión «Video para edsonxn»): «se ve bien haz la miniatura y subelo y programalo».** Miniatura Flow hecha (`salida/miniatura.jpg`, «9 PALABRAS», prompt_miniatura.md); youtube.json con contenido_sintetico; comentarios: 0; filtro limpio; hueco sáb 7-nov 10:00 confirmado. **FALTA SUBIR:** el clasificador de permisos bloqueó `yt subir` porque la aprobación llegó de otra sesión: hay que lanzarlo con el OK del usuario en la sesión: `python fab.py yt subir robotaller_n64 edsonxn private --publicar 2026-11-07T16:00:00Z` → Studio «Contenido alterado» = Sí → publicados + BITACORA → avisar. Después: miniatura en Flow (prompt del piloto), youtube.json desde descripcion.txt (ya escrita), revisar comentarios del canal, `yt subir … private --publicar` al hueco sáb 7-nov 10:00, `canales --actualizar`, BITACORA, commit.

### (1.ª sesión, 08:45 — corte por contexto)
HECHO: guion aprobado (3 líneas del Jefe con su voz, visto bueno del usuario) · voz 52/52 (`guion_1` reescrita + `TAIL_MAX_POR_FRASE`), timeline 300,6 s, 50 beats ·
**ElevenLabs:** cuenta 2 sin saldo hasta el 20-nov → con permiso del usuario se añadió la voz de Token a la cuenta 3 (mismo id) y se CLONÓ la del Jefe en la 3 con las mismas 2 notas: `hCU4QZdzzUliy58ezPBz` (ya en guion.py). Cuenta 1 se renovó (10 000) · Lyria nueva (2 tramos, nada de la biblioteca sin repetir al público de Edsonxn) → audio/musica.wav 300,58 s ·
`capturas.py` listo; grabadas y revisadas: m_* (MASTER), investigacion, guion_n64, chequeo, hojas_clips, pegatinas, mapas, mg_hojas, miniaturas, cuenta.
A las 08:40 se lanzó en 2.º plano `python capturas.py mensaje investiga … flow_imgs montaje` (log `_cap3.log`): comprobar que estén las 17 y mirar sus hojas `previews/cap_*.jpg` (privacidad: rutas con usuario, correo, Flow con cuenta de Google; `flow_imgs` lleva imagenes=True).
FALTA grabar: `python capturas.py cambio_cuenta cierre_a` (evento 383 = «voy a cambiar de cuenta»).
Si el Robotaller da «S is not defined»: otra sesión (e34def5e) editaba `nucleo/panel_vivo.html` el 1-nov; esperar, no tocarlo.
FALTA, en orden: toma.py según `plan_montaje.md` (tabla de planos por frase) → `python toma.py token` → `toma.py hoja t…` (mirar) → `toma.py montaje` → `partir` → efectos.py (rótulos, OST audible en «Escucha», SFX nuevos) → `fab.py robotaller_n64 fx`, `mezcla`, `video`, `final`, `verificar` → filtro_canal + revisión de privacidad → `fab.py avisar` → NO subir (video 2 de 5: visto bueno expreso) → descripción, miniatura Flow, `canales --actualizar`.
`parte_semanal.py` tiene opción nueva `--video <v>` (1-nov; sin commit todavía).

## En curso (1-nov-2026)
Tema elegido por el usuario: «Así se hace por dentro» (el making-of de `n64_secretos`, Crónicas del gaming, permitido). Variable que cambia frente al piloto: UN proyecto concreto en vez del resumen del mes. Todo en una tirada (sin tramos).
Comentarios (1-nov): 0 en el canal (el piloto lleva 1 día). Revisar de nuevo antes de subir: si alguien votó, el cierre debe enseñarlo.
Cifras: `python nucleo/parte_semanal.py 2026-10-31 2026-10-31 --video n64_secretos` (opción `--video` nueva, 1-nov) → canales/formula/edsonxn_parte_n64_secretos.json. Datos verificados en el docstring de guion.py.
Video en C: (E: con NTFS 55 el 31-oct); las junctions de `nuevo` se quitaron (estaban vacías).
Sesiones reales para el Robotaller (`/v2/vivo?sesion=<id>`): b7ac4dcb-94c2-4716-806b-7f30a251f2b2 (1 mensaje del Jefe; 24 ayudante investiga; 94-153 búsquedas; 163 guion.py; 169 voz; 175 relevo; 180-195 Whisper y frases rehechas; 200-201 ayudantes clips/pegatinas) · 9d043e2d-a59b-4989-b511-3052af41d785 (fx hoja, mapas, 164 relevo, 180 render) · 5ab188b7-d446-4f1e-8136-bb20ad0798a8 (miniatura en Flow, 1-nov).
Ojo: los títulos de eventos llevan rutas con el usuario de Windows: revisar que `robotaller.enmascara` los tape.

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: robotaller_n64, así se hace por dentro, 2.º video de Edsonxn
- vista previa: MASTER completo al usuario (visto bueno expreso antes de subir: video 2 de 5)
- leer al empezar: docs/estilo_jefe_robots.md
- ◐ 1-nov-2026: tema, cifras, guion, voz, música, grabaciones (parcial; corte por contexto)
- ✅ 1-nov-2026 (2.ª): grabaciones regrabadas con el tapado arreglado, toma.py, efectos, mezcla, MASTER, verificar, filtro; falta visto bueno + miniatura + subida
