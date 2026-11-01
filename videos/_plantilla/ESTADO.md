# <Título del video> — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: <alias> · <fecha meta de publicación>
- estilo: <ESTILO_VISUAL> → doc de estilo: docs/<...>.md · ejemplo a copiar: videos/<...>/
- etapa: <guion | voz | tiempo | escenas n/N | música | render | verificado | subido | publicado>
- siguiente: <el paso exacto que sigue, con comando>


## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: <frases con las que el usuario nombra este video>
- vista previa: <¿ver el principio antes de seguir? p. ej. «tras el min 1», «cada tramo», «solo al final»; render: `python fab.py <v> video --hasta <s>`>
- leer al empezar: <archivos además de este ESTADO.md: guía del kit, plan de tomas…>
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | <guion, voz, tiempo + kit + escenas …> | ⏳ siguiente | <plan propuesto al usuario y elegido por él> |
| 2 | <cierre: sfx → mezcla → render → final → verificar → miniatura → youtube.json> | pendiente | |

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (qué estás haciendo · archivos que tocas · qué falta · comando largo lanzado y hora)

## Hecho
- (guion, voz, escenas, música... con cifras: duración, CER, LUFS)

## Falta
- [ ] ...

## Cómo retomar (comandos)
```
python fab.py estado <video>
./run.sh _prueba.py nombre t1 t2 ...      (si el video tiene run.sh / hoja de prueba)
```

## Archivos clave
- `guion.py`, `escenas.py` ...

## Lecciones de este video (solo lo no obvio)
- ...

## Cierre (regla del 12-oct-2026)
- [ ] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [ ] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
