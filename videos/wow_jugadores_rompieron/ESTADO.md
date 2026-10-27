# Los 10 jugadores REALES que ROMPIERON WoW Vanilla (y qué pasará en Forever) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · 13:34 · programado mar 3-nov-2026 09:00 CDMX (15:00 UTC), víspera de Forever
- estilo: secuencia_yt (gameplay por beat + apoyos + pegatinas + MG nuevos + mapas si hay ruta + Overgear campaña 2) → doc: docs/estilo_secuencia_yt.md
- etapa: ✅ SUBIDO y PROGRAMADO mar 3-nov-2026 09:00 CDMX (jBumLmFN600) · miniatura + .srt
- siguiente: (MASTER aprobado por el usuario el 27-oct, se queda programado) Studio: monetización + video relacionado; medir a los 7 días (10-nov) contra «12 Legendarios» (×2,54); luego `limpiar`

## Sesiones (plan de tramos · «continúa el video jugadores rompieron» retoma aquí · protocolo docs/sesiones.md)
- alias: jugadores rompieron, jugadores reales, jugadores que rompieron vanilla
- vista previa: NO (el usuario, 27-oct): solo el MASTER, aviso al terminar
- leer al empezar: este ESTADO.md + `docs/estilo_secuencia_yt.md` + `docs/migracion_googleimagenes.md` § «Campaña 2» + de modelo `videos/wow_clases_ocultas/` (segmento Overgear campaña 2) y `videos/wow_objetos_raros/`
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación + guion (10 jugadores, ~2 300 palabras, segmento Overgear coaching) | ✅ 27-oct | 2 272 palabras; 16 candidatos con fuentes en `videos/_investigacion_wow_jugadores.md`; Serenity Now descartado (ya en Halloween) |
| 2 | voz Applio + seleccionar + tiempo + beats + busquedas.json | ✅ 27-oct | 123/123 (43 con CER_MAX_POR_FRASE por nombres; «WoW» en FONETICA = «World of Warcraft»); 793,1 s + 20,6 final ≈ 13:34; 92 beats; 19 fijados con url (Onyxia Wipe, Kazzak en Ventormenta, Reckoning, gong de Medivh, RIdPEF, Joana); scene-008 con el audio real de Dives |
| 3 | bajar clips + revisar hojas `medios` | ✅ 27-oct | 92/92; 14 beats con metraje de ARCHIVO < 720p (Kazzak en Ventormenta, gong de Medivh, Hyjal, Joana, video original de Karmerr) hechos a mano como ventana con marco dorado sobre su propio fondo desenfocado (`medios/_archivo/`, NO `--rehacer`); 29 rehechos en la 1.ª vuelta + 5 en la 2.ª + 2 en la 3.ª; scene-031 = screencast de la web de coaching |
| 4 | apoyos + pegatinas + MG nuevos + Overgear (`fx hoja`) | ✅ 27-oct | efectos.py: 48 FX + 5 rótulos + 13 apoyos; MG nuevos `reckoning`, `inmortal`, `expediente` en nucleo/mg_wow.py; 3 mapas (RIdPEF, Kazzak, gong) |
| 5 | OST de WoW → mezcla → render → final → verificar → avisar → miniatura → subir y programar | ✅ 27-oct | OST: Orgrimmar, Forjaz, Cima del Trueno, Darnassus, Ahn'Qiraj, Entrañas (`musica_wow.py`; `aparta` −14 dB en scene-008) + música promo en Overgear; mezcla −14,09 LUFS, voz/música 14,3 dB; miniatura Flow v1 (Kazzak en Ventormenta, «10 LO ROMPIERON»); youtube.json listo; render 25 min; MASTER 13:34; blackdetect: 4 negros breves de origen (0:11 0,5 s · 8:09 0,23 s · 9:10 0,33 s · 10:37 0,4 s) + mapa del mundo abierto en el clip 042 (6:00), aceptados por el usuario (27-oct); subido jBumLmFN600 |

## Decisiones del episodio (el usuario, 27-oct-2026)
- tema elegido entre 3 propuestas con datos: jugadores REALES (eje más fuerte del canal: Kungen ×50, Angwe ×16,6, «12 Legendarios» ×2,54 con 53 % visto); variable que cambia respecto a «12 Legendarios»: ángulo «rompieron el juego» + gancho a Forever
- ~14 min · lista cuenta regresiva de 10 · Overgear campaña 2 (coaching self-play de Forever, CRONICAS10): vía PvE con pros de guilds world-first
- música ORIGINAL de WoW (no Lyria) · sin vista previa
- no repetir a los protagonistas de «12 Legendarios», «5 más épicos de BC», «Cuenta más vieja», Kungen, Angwe, Drakedog ni la Sangre Corrupta

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada en curso)

## Hecho
- `nuevo --yt` + `canales --actualizar` (27-oct)

## Pendiente del usuario
- % del descuento y creativo personalizado de la campaña 2: se usa CRONICAS10 al 10 % y el creativo viejo hasta que lleguen

## Cómo retomar (comandos)
```
python fab.py estado wow_jugadores_rompieron
python fab.py wow_jugadores_rompieron voz | seleccionar | tiempo | beats | busquedas
python fab.py wow_jugadores_rompieron bajar           (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py wow_jugadores_rompieron medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json`, `medios/`, `salida/creditos.txt`, `videos/_investigacion_wow_jugadores.md`

## Lecciones de este video (solo lo no obvio)
- Los videos de archivo de 2005-06 no pasan el filtro ≥ 720p de `bajar`: ventana enmarcada a mano (docs/estilo_secuencia_yt.md § METRAJE DE ARCHIVO).
- La animación del Onyxia Wipe trae fotos ajenas (una sugerente) y tacos en el audio tras «handle it»: revisar todos sus cuadros.
- `_barra_vida` de mg_wow fallaba con la barra casi vacía (PIL exige x1 >= x0): arreglado.

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO mar 3-nov 09:00 CDMX (jBumLmFN600), miniatura y .srt; registrado en `canales/cronicas_warcraft.json` y BITACORA
- [x] HALLAZGOS documentados en docs/estilo_secuencia_yt.md (MG reckoning/inmortal/expediente, § METRAJE DE ARCHIVO)
- [ ] Studio: monetización + video relacionado de Shorts
