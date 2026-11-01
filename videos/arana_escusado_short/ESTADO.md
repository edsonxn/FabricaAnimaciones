# <Título del video> — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: pieza_oculta · <fecha meta de publicación>
- estilo: secuencia_flow (plastilina, clips e imágenes de Google Flow) → doc de estilo: docs/estilo_secuencia_flow.md
- etapa: <guion | voz | beats | prompts n/N | flow n/N | armado | música | verificado | subido | publicado>
- ✅ **PÚBLICO** desde el lun 26-oct 22:05 CDMX · https://youtu.be/EjcARSU5Kwc (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
- siguiente: <el paso exacto que sigue, con comando>


## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: <frases con las que el usuario nombra este video>
- vista previa: <¿ver el principio antes de seguir? p. ej. «tras el min 1», «cada tramo», «solo al final»; render: `python fab.py <v> video --hasta <s>`>
- leer al empezar: <archivos además de este ESTADO.md: guía del kit, plan de tomas…>
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | <guion, voz, tiempo + kit + escenas …> | ⏳ siguiente | <plan propuesto al usuario y elegido por él> |
| 2 | <cierre: sfx → mezcla → render → final → verificar → miniatura → youtube.json> | pendiente | |

## Decisiones del episodio (preguntadas al usuario al empezar)
- duración total: · minutos iniciales en video: · duración de clip: · resolución de clip:

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (qué estás haciendo · archivos que tocas · qué falta · comando largo lanzado y hora)

## Hecho
- (guion, voz, beats, prompts, medios de Flow, armado... con cifras)

## Falta
- [ ] ...

## Cómo retomar (comandos)
```
python fab.py estado <video>
python fab.py <video> medios          hojas previews/medios_NN.jpg (qué llegó de Flow y qué falta)
python fab.py <video> ingesta --espera 900
```

## Archivos clave
- `guion.py` (narración + FICHA visual), `beats.json`, `prompts.json`, `flow/escenas.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- ...

## Cierre (regla del 12-oct-2026)
- [ ] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [ ] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
