# <Título del video> — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: <alias> · <fecha meta de publicación>
- estilo: secuencia_yt (gameplay de YouTube por beat + apoyos + 3 MG + Overgear) → doc: docs/estilo_secuencia_yt.md
- etapa: <guion | voz | beats | busquedas | bajar n/N | armado | música | verificado | subido | publicado>
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
- duración total: · puestos de la lista: · vía de Overgear (M+/raids/PvP/leveling):
- Runa/Tamriel: campaña de suscripción en el guion (cifra real, meta, ~75 %): docs/estilo_secuencia_yt.md § CAMPAÑA
- REGLA DE ORO: leer docs/estilo_secuencia_yt.md § REGLA DE ORO antes de `efectos.py` (todas las capas suman); `fab.py <v> chequeo` antes de renderizar

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (qué estás haciendo · archivos que tocas · qué falta · comando largo lanzado y hora)

## Hecho
- (guion, voz, beats, busquedas, clips bajados, armado... con cifras)

## Falta
- [ ] ...

## Cómo retomar (comandos)
```
python fab.py estado <video>
python fab.py <video> bajar           baja lo que falte (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py <video> medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json` (de dónde sale cada clip), `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- ...

## Cierre (regla del 12-oct-2026)
- [ ] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/<alias>.json`, BITACORA)
- [ ] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
