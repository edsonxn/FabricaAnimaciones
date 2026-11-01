# Así se hace por dentro: un video de 24 min en 4 horas (Edsonxn, 2.º video) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: edsonxn · hueco sáb 7-nov-2026 10:00 CDMX (ciclo 7 d)
- estilo: Jefe de Robots: grabaciones reales con cámara + Token de acento + El Jefe → doc: docs/estilo_jefe_robots.md (copiar de videos/robotaller_mes1/)
- etapa: voz + beats (5:00) + música Lyria + casi todas las grabaciones; falta toma.py, efectos, mezcla, render
- siguiente: terminar grabaciones → toma.py (plan_montaje.md) → efectos.py → fx, mezcla, video, final, verificar, filtro, avisar

## En curso (1-nov-2026, 2.ª sesión — manda sobre lo de abajo)
2.ª sesión: las 19 grabaciones hechas y miradas (montaje.mp4 negro hasta 4 s → desde 5). `toma.py` escrito (69 planos, `python toma.py revisar` limpio). Siguiente: `python toma.py token` (log `_token.log`) → hoja → montaje → partir → efectos.

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
