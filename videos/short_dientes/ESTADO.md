# ¿Tus dientes se están tocando ahora mismo? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cuerpo_en_neon (Cuerpo en Neón) · Short vertical derivado de `estres_cuerpo` (https://youtu.be/rdzUobc1UAM)
- estilo: línea blanca + neón, imágenes del largo reencuadradas a 9:16 → doc: docs/estilo_linea_neon.md § «Shorts derivados»
- etapa: PROGRAMADO sáb 24-oct-2026 19:00 CDMX (2026-10-25T01:00:00Z) · https://youtu.be/za1GvddkcL8 (privado hasta la fecha)
- ✅ **PÚBLICO** desde el sáb 24-oct 19:00 CDMX · https://youtu.be/za1GvddkcL8 (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
- siguiente: poner «Video relacionado» = estres_cuerpo en Studio cuando el largo sea PÚBLICO (sale mié 21-oct 14:02 CDMX; antes Studio no lo ofrece); luego `limpiar` al aprobar

## Sesiones
- alias: short de posición de descanso de la quijada
- vista previa: el usuario revisó el 🎞 Montaje el 21-oct-2026 («se ven bien»)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo (pedido del usuario el 21-oct-2026: un Short por largo, una técnica, ~45 s, con video relacionado) | ✅ 21-oct-2026 | MASTER 59,6 s, verificar CER 0, rigor sin bloqueos, subido y programado; falta solo el video relacionado en Studio |

## En curso
- nada

## Lecciones
- el primer render murió en el cuadro 1254/1789 al cortarse la sesión anterior: `video` se relanza entero (no reanuda), 4,5 min
- Shorts entre sí: 48 h (`separacion_min_horas`); frente a largo, 12 h → franja 19:00 CDMX en días sin largo

## Decisiones
- técnica: posición de descanso de la quijada · 59,6 s · 19 beats de imagen, todas del largo (`medios_del_largo.py` + nucleo/vertical_desde_largo.py)
- voz: tomas del largo reutilizadas (copiadas a voz/cands) + frases nuevas de gancho/cierre con ElevenLabs Alejandro Durán
- SFX copiados de `estres_cuerpo/sfx`; Lyria nueva de 1 tramo; BPM 160 solo para que la línea de tiempo no meta silencios de 3 s
- «video relacionado» (enlace al largo): la API no lo pone; se pone en Studio (o con el navegador integrado si hay sesión)
