# ¿Qué pasaría si el OXÍGENO desapareciera 5 segundos? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: kuriox · meta: lun 19-oct-2026 14:00 CDMX (hueco del canal; ciclo 4 d; los Shorts no cuentan) · video LARGO horizontal 16:9, 5:52
- estilo: kurzgesagt con la mascota Kuri → doc de estilo: docs/estilo_kurzgesagt.md · ejemplo a copiar: videos/sol_apagado_8min/ (largo, misma fórmula) y videos/historia_60/
- etapa: PROGRAMADO lun 19-oct-2026 14:00 CDMX · https://youtu.be/3SL2RsY7FMk (privado hasta entonces; miniatura «tierra» + .srt)
- siguiente: cerrado. Tras publicarse: métricas en 7 días; `python fab.py oxigeno_5s limpiar` cuando el usuario lo apruebe

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: oxígeno, oxigeno 5 segundos, video de kuriox, qué pasaría si el oxígeno
- vista previa: SÍ, el primer minuto con audio completo → hecha y enviada el 14-oct (`salida/oxigeno_5s_AVANCE.mp4`)
- cuenta: `cronicas.warcraft` (26 % semanal el 14-oct, reinicia mar 20-oct); `jairedson5` al 90 % → solo gestión
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion (~5 min) + voz + seleccionar + tiempo + LYRIA | ✅ 14-oct | 13 escenas, 72 frases CER 0 en 1.ª ronda; 5:52; Lyria 3 tramos (audio/musica.wav) |
| 2 | escenas 0:00–3:10 + sfx/mezcla + vista previa `--hasta 60` | ✅ 14-oct | el usuario pidió los tramos 2-4 en una sola sesión |
| 3 | escenas 3:10–5:52 (versión B + realidad + cierre) | ✅ 14-oct | |
| 4 | render → final → verificar → revisión 117 cuadros → miniatura → youtube.json → subir + programar | ✅ 14-oct | 3SL2RsY7FMk, --forzar pedido por el usuario |

## Hecho
- Plano secuencia en módulos: `escenas.py` (despacho por modo: paisaje / zoom al planeta / espacio / portal / cuerpo), `camara.py`,
  `mundo_paisaje.py`, `gente.py`, `mundo_espacio.py`, `mundo_cuerpo.py`, `estado.py`, `kit_oxi.py`, `kit_bio.py`, `ui_base.py`,
  `ui.py`, `ui2.py`, `sonido.py` (161 sfx). Pruebas: `cd videos/oxigeno_5s; $env:PYTHONPATH="C:\FabricaAnimaciones\nucleo";
  python _cuadro.py hoja t1 t2 ...`; revisión del MASTER: `python _revision_master.py` (hojas 4×3, un cuadro cada 3 s).
- Mezcla LUFS −14, pico −1,14 dBTP, voz/fondo 12,9 dB; verificar: CER 0,09 % (solo realidad_3 al 3,7 %: Whisper corta «Hoy,»).
- Miniatura por código, elegida «tierra» (`salida/oxigeno_5_segundos_mini_tierra.jpg`); fórmula del canal en `canales/formula/kuriox.md`.
- Tema con datos: referencia Ángel Hernández ×12,2 (Short) + nuestro «¿Qué pasaría si el Sol se apagara?» ×9,8 (44 % visto).

## Lecciones de este video (solo lo no obvio)
- Dan con GAP 0,35 leyó a 3,1 palabras/s (941 palabras = 303 s de voz → 5:52 de video): para N min con Dan ≈ N×60×2,7 palabras.
- Nombres propios y siglas fuera de la narración (aerolínea, ADN → «material genético»): 72/72 con CER 0 a la primera.
- El usuario vio un «cuadro de tierra» en el zoom al planeta: al doblar el paisaje sobre la Tierra se ve el corte del subsuelo.
  Arreglo: durante el zoom solo la piel de la superficie (`MP.dibujar(delgado=True)`) + planeta liso + continente en lente.
- Un SFX encima de las primeras palabras las tapa (Whisper oyó «Respirando»): la inspiración va DESPUÉS de «Respira hondo».
- Moléculas rojas que cruzan la copa de un árbol parecen frutas: los flujos de partículas van por cielo abierto.
- Render de 5:52 con 12 procesos: 22 min (0,3-1 s por cuadro). Si se edita código con un render en marcha, `--rehacer` esos tramos.

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado y registrado (`canales/kuriox.json` → `publicados` + `"formato"`, BITACORA)
- [x] HALLAZGOS documentados en `docs/estilo_kurzgesagt.md` (HALLAZGOS `oxigeno_5s`) y fórmula en `canales/formula/kuriox.md`
- [ ] `python fab.py oxigeno_5s limpiar` cuando esté aprobado (segmentos 299 MB)
