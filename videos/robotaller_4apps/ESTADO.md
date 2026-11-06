# 4 apps en menos de 24 horas (Edsonxn, 3.er video) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: edsonxn · PROGRAMADO sáb 14-nov-2026 10:00 CDMX: https://youtu.be/WLb3mCBM288
- estilo: Jefe de Robots: grabaciones reales con cámara + Token de acento + El Jefe → doc: docs/estilo_jefe_robots.md (copiar de videos/robotaller_n64/)
- etapa: SUBIDO en privado y programado (5-nov) con el visto bueno del usuario; registrado en canales/edsonxn.json y BITACORA
- siguiente: comprobar en Studio «Contenido alterado» = Sí; medir a 7 días (retención, suscriptores, comentarios); cumplir la junta directiva (app más votada)

## Pedido del usuario (5-nov-2026)
«Que se muestren más las cosas que yo hago y desarrollo y los cambios en las aplicaciones; toda mi interacción con Claude en ese canal.»
Tema elegido: «4 apps en un día» → título «Soy una IA: mi jefe me pidió 4 apps y las hice en menos de 24 horas». **Todo en 1 MASTER directo** (sin vista previa parcial).
Video 3 de 5: NO se sube sin su visto bueno expreso del MASTER.
Grabaciones (el usuario, 5-nov): las del CELULAR las graba él (pantalla, con las mejoras de cada app) y las manda por Rayo → `%USERPROFILE%\Downloads\Rayo\`;
las de ESCRITORIO se graban de la pantalla real (UI HTML de `D:\Rayo\pc\ui` y `D:\PuenteTV\pc\ui`, con anfitrión inyectado: sin IPs ni enlaces);
la TELE se SIMULA con una animación (tele dibujada + aviso con robot + sala de revisión + tablero; capturas reales en `D:\PuenteTV\capturas`).
Comentarios (5-nov): 0 en el canal.

## Datos (verificados en el docstring de guion.py)
Sesiones reales (`~/.claude/projects/D--Escaner/`): 30a418d2 (Altima, 3-nov) · fecd0d1d (MicWiFi, Rayo, Puente TV, 4-nov) · 5023f72b (ideas de la tele, sala de revisión, tablero) · bd7d4bbf (Altima conexión automática, APK por Rayo).
Scripts de consulta en el scratchpad de la sesión f7b7a9a5 (`mensajes.py`, `textos.py`): rehacer si hacen falta (leen el .jsonl, hora CDMX = UTC-6).
Sonido nombrado: `sfx/tele_1235.mp3` (1.ª frase real de la tele) suena tras `puente_3` con la voz callada (post 4,6 s).
PRIVADO a tapar: nombre de la wifi (apellido), IPs, nombre de la tele (nombres de la familia), código/puerto de vinculación ADB, dominio y enlaces de descarga.
El Robotaller (`nucleo/agente_vivo.py`) solo lee sesiones de `C--FabricaAnimaciones`: para repetir las de `D--Escaner` hay que buscarlas en las otras carpetas.

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: robotaller_4apps, 4 apps en 24 horas, 3.er video de Edsonxn
- vista previa: MASTER completo al usuario (en la tele: `fab.py tele video robotaller_4apps master --pregunta …`)
- leer al empezar: docs/estilo_jefe_robots.md
- ◐ 5-nov-2026: tema, datos, guion, voz, música, 25 grabaciones, tele simulada, plan de cámara (parcial; corte por contexto en toma.py)
- ✅ 5-nov-2026 (2.ª): toma.py, cambio del carro sin modelo ni año (voz, 22 tomas, Token, música), efectos + 19 SFX, montaje, mezcla −14 LUFS, MASTER, verificar, filtro y privacidad cuadro a cuadro; aviso por voz (tele apagada). Visto bueno dado («Sí, súbelo»); miniatura B de Flow, descripción y youtube.json hechos; falta solo la subida.

## En curso (5-nov-2026, 2.ª sesión — manda sobre lo de abajo)
**CAMBIO DEL USUARIO (5-nov, antes del MASTER): ni modelo ni año del carro.** `altima_1` reescrita («Mi jefe tiene un carro y uno de esos escáneres…», 16 créditos) → seleccionar/tiempo (275,2 s)/beats/música rearmada; `PRIVADO` de capturas.py tapa modelo, año, 4 puertas, 2.5L y nombre de la app; APK de la UI de Rayo = Escaner-2.1.apk; rótulo «1 · ESCÁNER DEL CARRO»; 22 tomas regrabadas y token regrabado. Regla en docs/estilo_jefe_robots.md § Privacidad.
toma.py escrito (planos de plan_montaje.md, `revisar` limpio; los `_*.py` borrados) · `beats` (46) · efectos.py (31 rótulos, tele_1235 voz=True en «Escucha:», 19 SFX nuevos, 230 créditos) · token grabado · planos afinados con hojas (mensajes largos z≤1,8; Jefe: mensaje sin Token, en tele_2 el Jefe a la izquierda; «ese de ahí soy yo» = Token) · filtro del guion limpio · fx (80 sonidos) + mezcla (−14 LUFS; tele_1235 al nivel de voz) HECHOS · montaje + partir HECHOS (1.er intento sin memoria a 181 s → `nucleo/montaje_real.py` ahora cierra grabaciones viejas, máx. 8 abiertas; sin commit) · fx/mezcla rehechos · MASTER salida/robotaller_4apps_MASTER.mp4 (81 MB, 275,2 s) · verificar OK · filtro limpio · privacidad revisada cuadro cada 4 s (todo ▒▒) · tele apagada → aviso por voz con la pregunta «¿listo para subir?».
Pendiente menor (si el usuario lo pide): el rótulo «22 MIN» tapa un renglón de la lista de Rayo y «4 VERSIONES · 36 MIN» arranca bajo la ventanita de Token.

## 1.ª sesión (5-nov-2026)
HECHO: guion (45 frases; Jefe = altima_8, micwifi_5, tele_2 con su voz clonada de la cuenta 3, frases literales de sus mensajes) · voz ElevenLabs 843 créditos (cuenta 2 ≈ 8 691) · `seleccionar` 45/45 · `tiempo` 277,5 s.
`nucleo/agente_vivo.py` (5-nov): `_sesion` busca el id también en las otras carpetas de ~/.claude/projects (repetir sesiones de D:\Escaner); sin commit todavía.
`eventos.py` = índice completo de eventos (la API solo manda 160) → capturas/eventos_*.txt. `capturas.py` usa ese índice en `solo()` y tapa wifi/tele/IPs/código/dominio (`PRIVADO`).
Escritorio: copias de las UI reales en `capturas/ui/{rayo,puente}` con la demo limpia (`limpiar_demo.py`): sin IPs ni enlaces; Rayo enseña AltimaScan-2.1.apk enviada 20:17.
Tele: las capturas de `D:\PuenteTV\capturas` con tablero de CNB traen CLIENTES y DINERO → fuera. Usables: rev_1_marcar, rev_3_lista, opciones_normal, tablero_vivo_1. La tele se SIMULA (pedido del usuario): HTML con tele + video → pausa → robot con boca y texto «La comida está lista…» sincronizado con `sfx/tele_1235.mp3` → sala de revisión → protector.
MÚSICA HECHA: Lyria 402 dos veces → el usuario eligió «reusa la del video anterior»: robotaller_n64 tramos 1 y 2 → audio/musica.wav (277,5 s).
GRABACIONES HECHAS: 25 tomas en capturas/ (Robotaller de las 4 sesiones, rayo_pc, puente_pc, tele_aviso/revision/protector); datos tapados comprobados (0 restos de usuario, wifi, tele, IPs, dominio). tv_codigo y tv_prueba regrabadas con la subred tapada.
Tele simulada = `tele.py` → capturas/tele/tele.html (robot de RobotView.kt, boca con la envolvente real de sfx/tele_1235.mp3; el robot sale en el s 3,6 de tele_aviso).
PLAN DE CÁMARA: `plan_montaje.md` (frase → toma).
CORTE POR CONTEXTO (5-nov, ~19:10): toma.py a medias. Hechos `_cabeza2.py` (cabecera reutilizable de n64: imports, T, pose, js, minis, pc) y
`_cola_toma.py` (de `JEFE_FRASES = guion.JEFE` al final: armar, golpes, partir, main). Falta escribir en medio: CARAS/GESTO/PLAN de Token, TRANS,
QUIETOS, A/C/tok, FICHA/MSJ y los planos de plan_montaje.md (copiar las líneas 63-107 de `_cabeza_toma.py` y cambiar los planos) → unir en toma.py y borrar los `_*.py`.
tele_aviso: el robot aparece en el s ≈ 3,4 del clip (3,6 de la página − 0,2 de espera): plano en FRASES["puente_3"]["t1"] − 3,4 con desde=0.
FALTA: videos del celular (aún no llegan; el montaje no espera: si llegan, entran en los planos que dice plan_montaje.md) · toma.py (copiar de robotaller_n64, `T(frase, palabra)`) · token (`toma.py token`) · efectos.py (sonido de la tele tras puente_3) · fx · mezcla · video · final · verificar · filtro + privacidad cuadro a cuadro · aviso a la tele (video 3 de 5: visto bueno antes de subir).
