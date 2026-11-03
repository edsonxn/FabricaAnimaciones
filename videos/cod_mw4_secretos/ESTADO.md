# Los 25 secretos de Modern Warfare 4 — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_cod = «Expediente 141» (1.er video del canal) · meta: en cuanto esté (canal URGENTE, sin videos)
- estilo: secuencia_yt (gameplay de YouTube por beat + pegatinas + MG + mapas + sonido original + OST de MW4) → doc: docs/estilo_secuencia_yt.md
- etapa: REHECHO y SUBIDO (3-nov): https://youtu.be/T95SAXHHl10 privado, sale 3-nov 18:00 CDMX (2026-11-04T00:00Z); el viejo agTIwVlWD1I quedó privado sin fecha, NO borrado (espera el OK del usuario)
- siguiente: medir a 7 días (% visto ≥ 35, vistas/día); Shorts de 2-3 puestos; `limpiar` y `biblioteca sfx catalogar` al aprobar. Antes: beats → busquedas.json → bajar → medios (voz y tiempo HECHOS: 16:44) → piloto del 1.er minuto (el usuario: terminar TODO el video en esta sesión, pero antes enseñarle el 1.er minuto)

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: «secretos de MW4», «el video de Call of Duty», «cod_mw4_secretos»
- vista previa: SÍ, el primer minuto renderizado con audio completo (voz + OST + SFX + mezcla) antes del tramo 3; render: `python fab.py cod_mw4_secretos video --hasta 60`
- leer al empezar: este ESTADO.md, `canales/formula/cronicas_cod.md`, `docs/estilo_secuencia_yt.md` (grep por sección; § REGLA DE ORO entera)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación (fuentes + clips) + guion 25 puestos + 3 pruebas de voz → elegir → voz + tiempo | ✅ 2-nov (guion 2 332 palabras, voz Damián 125 frases, 16:44; kit `nucleo/mg_cod.py` hecho) | elegido por el usuario el 2-nov |
| 2 | beats, búsquedas, bajar clips, kit de interfaz CoD (`nucleo/mg_cod.py`), MG, pegatinas, mapas; vista previa del 1.er min | ✅ 2-nov (piloto aprobado: «Sí, sigue») | |
| 4 | REHACER con más MG/pegatinas (corrección del usuario 3-nov) | ✅ 3-nov (gancho reescrito y voz rehecha, 16:59; 44 pegatinas nuevas; MG objetivo/marcador/contador en mg_cod; cortes `vid()`; vacío 545 s → 45 s; densidad 5,5 MG + 5,8 pegatinas/min; subido T95SAXHHl10) | lección en docs/estilo_secuencia_yt.md § REGLA DE ORO «SIN TRAMOS VACÍOS» |
| 3 | sonido original + OST + SFX del juego → mezcla → render → final → verificar → miniatura Flow → subir y programar | ✅ 2-nov (hilo 4: 11 clips rehechos, recortes, 7 sonidos nombrados rehechos —los del hilo 3 estaban vacíos—, miniatura Flow; subido https://youtu.be/agTIwVlWD1I privado, sale 3-nov 18:00 CDMX) | |

## Decisiones del episodio (preguntadas al usuario al empezar, 2-nov-2026)
- duración total: ~20 min · puestos: 25 (cuenta regresiva) · Overgear: aún NO (canal nuevo; se ofrece cuando haya 5-10 mil vistas constantes)
- voz: **Damián** de ElevenLabs (`BPwS5yO6aXvwg8auqNwS`), tono de sargento; elegida por el usuario entre 9 pruebas (`canales/voces_prueba/cod_mw4/`); ya en guion.py
- 3 sesiones; vista previa del 1.er minuto
- Comentarios: canal nuevo, sin comentarios que leer (no aplica agradecimientos ni críticas en este video)
- REGLA DE ORO: leer docs/estilo_secuencia_yt.md § REGLA DE ORO antes de `efectos.py` (todas las capas suman); `fab.py <v> chequeo` antes de renderizar
- Datos: Shorts de detalles de MW4 rompen (TiHOME ×63, Vandal ×19,6 en español); nadie lo tiene en largo en español (`canales/metricas/ideas/cronicas_cod.md`)

## Hecho
- 2-nov: proyecto creado (`nuevo --yt`), decisiones tomadas; voz Damián en guion.py; investigación terminada (`investigacion.md`; MW4 = Infinity Ward, 23-oct-2026, Corea; OST Stephen Barton + Jason Graves, Lakeshore Records)

## Falta
- [x] investigación · [ ] guion · [ ] voz · [ ] beats/clips · [ ] kit CoD · [ ] vista previa · [ ] cierre y subida

## Cómo retomar (comandos)
```
python fab.py estado cod_mw4_secretos
python fab.py cod_mw4_secretos bajar           baja lo que falte (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py cod_mw4_secretos medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `investigacion.md`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`
