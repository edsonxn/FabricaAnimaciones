# 5 viajeros en el tiempo: de dónde salió realmente cada caso — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: edsonxn · meta: mar 20-oct-2026 14:00 CDMX (20:00 UTC; ciclo 6 d tras `polybius` 14-oct) · hipótesis: título NUMERADO con promesa de veredicto (`canales/formula/edsonxn.md`)
- estilo: documental → docs/estilo_documental.md § «Tablero de detective VIVO» · ejemplo copiado: videos/polybius/ (kit `tablero.py`, `piezas.py`, `portal_base.py`, `mg*.py`, `coreo_comun.py`, `kit.py`) · voz Faraon · Lyria · SIN subtítulos
- etapa: voz ✓ (51/51, 351 s) · tiempo ✓ (389,4 s = 6:29, 8 escenas) · comprobar ✓ · kit copiado · escenas 0/8 (tramo 2 siguiente)
- siguiente: tramo 2 → escribir `escenas.py` + `coreo_*.py` + `portales.py` (gancho, carlssin, fentz) y render parcial `python fab.py viajeros_tiempo video --hasta 60`

## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: viajeros en el tiempo, viajeros_tiempo, los viajeros
- vista previa: tras el primer minuto (`python fab.py viajeros_tiempo video --hasta 60`); esperar el visto bueno del usuario antes de seguir
- leer al empezar: este ESTADO, `canales/formula/edsonxn.md`, `videos/polybius/ESTADO.md` (lecciones del tablero), `videos/polybius/escenas.py` y `coreo_a.py` (patrón)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion verificado + voz + tiempo + kit copiado de polybius | ✅ 12-oct-2026 | 5 casos (Carlssin, Fentz, Chaplin, Titor, Goddard) con veredicto y origen; hechos con fuente en el docstring de `guion.py` |
| 2 | escenas del tablero: gancho + carlssin + fentz (0:00-2:27) + render parcial `--hasta 60` | ⏳ siguiente | el usuario ve el primer minuto antes de seguir |
| 3 | escenas chaplin, titor, goddard, patron, cierre (2:27-6:29) + música Lyria | pendiente | portales NUEVOS por caso (nada reciclado de polybius/satoshi) |
| 4 | cierre: sfx → mezcla → render → final → verificar → hoja del MASTER → miniatura → youtube.json → subida PRIVADA | pendiente | programar mar 20-oct 14:00 CDMX solo si el usuario lo pide |

## Tiempos por escena (s): gancho 0-32,5 · carlssin -82,5 · fentz -147,5 · chaplin -200 · titor -262,5 · goddard -327,5 · patron -357,5 · cierre -389,4
Ideas de portales (una ventana dibujada por caso, estilo polybius): carlssin = pantalla de bolsa con cifras que suben + tabloide;
fentz = Times Square 1950 con taxi y hombre de época + revista Collier's 1951; chaplin = cola de estreno 1928 con la mujer y el audífono
(recreación rotulada); titor = monitor de foro 2000 + IBM 5100; goddard = cabina del biplano en tormenta → aeródromo con aviones amarillos.
Fotos reales posibles (Commons, con crédito): IBM 5100, Times Square 1950, Drem airfield, portada de revista. Nada de «foto del viajero».

## Hecho
- Datos y fórmula: `canales/formula/edsonxn.md`. Guion de 51 frases / 956 palabras. Voz Faraon: 351 s, todas CER ≤ 0,012.

## Falta
- [ ] Tramos 2-4 (arriba)

## Cómo retomar (comandos)
```
python fab.py continuar viajeros
python fab.py estado viajeros_tiempo
cd videos/viajeros_tiempo ; $env:PYTHONPATH="C:\FabricaAnimaciones\videos\viajeros_tiempo;C:\FabricaAnimaciones\nucleo"
python _hoja_rec.py a      (cuadros clave del recorrido)     python _hoja_portal.py nombre:1,5   (portales sueltos)
```

## Archivos clave
- `guion.py` (PRON/ALIAS_QA/TAIL_MAX_POR_FRASE), `escenas.py` (aún la plantilla), kit copiado de `videos/polybius/`.

## Lecciones de este video (solo lo no obvio)
- Un `( a && b ) &` en segundo plano MUERE cuando termina la herramienta: lanzar `voz && seleccionar` como UNA tarea de fondo (`run_in_background`), sin `&`.
- `seleccionar` rechazó frases con CER 0 por la COLA (`tail_ratio` > 0,35: frases largas que hablan hasta el final): `TAIL_MAX_POR_FRASE = {"fentz_1": 0.7, ...}` tras mirar que la transcripción termina bien.
- Whisper escribe los nombres ingleses a su manera («Andrew Carlson», «Times Square», «Goddard») y «DVD» salió «Dede»/«D.O.D»: alias en `ALIAS_QA` y quitar siglas ambiguas de la narración («el disco de la película»).
- `tomas=1`: tras cambiar el texto de una frase solo queda una toma; hay que mirar `voz/eval.json` antes de gastar más semillas.

## Cierre (regla del 12-oct-2026)
- [ ] subido, miniatura, programado y registrado (`canales/edsonxn.json` con `"formato"`/`"prueba"`, BITACORA)
- [ ] HALLAZGOS y mejoras documentados en `docs/estilo_documental.md` (ver CLAUDE.md «CIERRE DE VIDEO»)
