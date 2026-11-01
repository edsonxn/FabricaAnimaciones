# Los 30 SECRETOS de la Nintendo 64 QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_gaming · hueco mar 17-nov-2026 18:00 CDMX (ciclo 3 d; confirmar con `canales --actualizar`)
- estilo: secuencia_yt (Crónicas del gaming) → doc: docs/estilo_secuencia_yt.md § «REGLA DE ORO», § «Crónicas del gaming», § SONIDO ORIGINAL y § MAPAS REALES
- etapa: ✅ SUBIDO privado y PROGRAMADO mar 17-nov-2026 18:00 CDMX (https://youtu.be/mw2-4rNFs50) con miniatura de Flow «REPARTIÓ GUANTES» (1-nov) y .srt; registrado y documentado
- siguiente: al aprobarlo, `python fab.py n64_secretos limpiar`


## Sesiones (plan de tramos · «continúa el video n64_secretos» retoma aquí · protocolo docs/sesiones.md)
- alias: n64_secretos, 30 secretos de la N64, secretos de la Nintendo 64, video de 23 minutos de Crónicas del gaming
- vista previa: NO; el usuario eligió directo al MASTER (encadenar tramos y avisar al terminar)
- leer al empezar: este ESTADO, docs/estilo_secuencia_yt.md § REGLA DE ORO y § Crónicas del gaming; investigacion.md solo por grep
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación, kit, mapas, OST, SFX, guion | ✅ 31-oct | investigación, guion, kit, mapas VGMaps, OST por secreto (audio/ost, musica.wav) y SFX del juego |
| 2 | voz, tiempo, beats, plan de clips, bajar, medios | ✅ 31-oct | voz, beats, 170 clips (36 rehechos), 18 MG nuevos, 76 pegatinas, efectos.py revisado con fx hoja |
| 3 | efectos, música, sfx, ambiente, mezcla | ✅ 31-oct | 220 FX; -14,3 LUFS; voz 12 dB sobre el resto |
| 4 | render, final, verificar, miniatura, subir, programar, avisar, documentar | ✅ 31-oct | MASTER 24:19 verificado; subido + programado 17-nov 18:00 (mw2-4rNFs50) con .srt; lecciones en estilo_secuencia_yt.md |

## Decisiones del episodio (el usuario, 31-oct-2026)
- 23 minutos. Elegido entre 3: «30 secretos de la N64» (no DK64 ni «lo que Nintendo borró»). Formato: `historia_y_30_secretos_multijuego_secuencia_yt`.
- Variable que cambia: de UN juego a TODA la consola; misma fórmula que spyro2/mario64_secretos.
- Referencias: alejoRet «10 SECRETOS de JUEGOS RETRO» ×83,6 (16 800 subs, 210 k), NintenNOW «Secretos de Super Mario 64» ×8,7 (803 subs).
- Voz Hope (eleven_v4_turbo): ~4 100 créditos por 24 min; saldo 10 353, alcanza.
- Comentarios (31-oct): 2 nuevos en Majora (@riuma77, @antilopezmexicanos), ♥0, sin quejas ni sugerencias; 3 en 21 días, no llega a 4 agradecimientos.
- REGLA DE ORO: leer docs/estilo_secuencia_yt.md § REGLA DE ORO antes de `efectos.py`; `fab.py n64_secretos chequeo` antes de renderizar. Cada secreto con clip, OST y SFX de SU juego.
- Disco (31-oct): C: 0,8 GB, E: 74,6 GB. Todo lo pesado en E: (`medios/` debe ser junction antes de `bajar`).

## Hecho
- `nuevo n64_secretos --yt`, candado, `canales --actualizar`, `ideas --actualizar`, comentarios.
- Tramos 1-4 completos (31-oct): ver la tabla de Sesiones.

## Falta
- [x] Miniatura de Flow aplicada el 1-nov (`prompt_miniatura.md`; la de código queda en `salida/miniatura_codigo.jpg`).

## Cómo retomar (comandos)
```
python fab.py estado n64_secretos
python fab.py n64_secretos voz
python fab.py n64_secretos bajar           baja lo que falte (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py n64_secretos medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `investigacion.md`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- (pendiente)

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO en el hueco del canal sin preguntar (regla 20-oct), miniatura y registrado (`canales/cronicas_gaming.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados en el manual/estilo (ver CLAUDE.md «CIERRE DE VIDEO»)
- Nota: `youtube.json` no traía `"subtitulos"` (la plantilla de spyro2 tampoco): el .srt se cargó después con `yt aplicar`. Revisar que los próximos lo traigan.
