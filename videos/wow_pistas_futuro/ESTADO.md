# Las 8 pistas que Blizzard YA dejó sobre lo que viene después de WoW Forever — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · meta: dom 18-oct-2026 09:00 CDMX (hueco tras `wow_clases_ocultas` del 15-oct)
- estilo: secuencia_yt (gameplay de YouTube por beat + apoyos + 3 MG + Overgear) → doc: docs/estilo_secuencia_yt.md
- etapa: SUBIDO en privado y PROGRAMADO dom 18-oct-2026 09:00 CDMX (https://youtu.be/vODv9Gm0tjQ) con miniatura y .srt
- siguiente: nada; versión «Forever ya salió» SUBIDA en privado SIN fecha el 27-oct (https://youtu.be/ZinI3H8kleI); la publica el usuario después del 4-nov. Pendiente en Studio: monetización. La vieja (vODv9Gm0tjQ) sigue en privado. Antes: (26-oct) cambiando el segmento a la campaña 2 de Overgear (ver fila ◐): render en curso → final → verificar → avisar al usuario → subir la versión nueva en PRIVADO sin fecha (es de reserva: la publica él) → registrar el id nuevo


## Sesiones (plan de tramos · «continúa el video <alias>» retoma aquí · protocolo docs/sesiones.md)
- alias: pistas, pistas del futuro, lo que viene, video de warcraft nuevo
- vista previa: el usuario la ve en la vista «Montaje» del panel mientras baja `bajar` (13-oct); sin render parcial, directo al MASTER
- leer al empezar: este ESTADO.md + `docs/estilo_secuencia_yt.md` + `docs/migracion_googleimagenes.md` (§ Overgear)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación + guion + voz Applio + tiempo + beats | ✅ 13-oct-2026 | tema elegido por el usuario con datos (Uncas ×6,8); 8 pistas, ~1 980 palabras; voz 103/103 (p(es) ≥ 0,997); 665,6 s; 77 beats. Pendiente del usuario: oír nombres propios y aprobar `overgear` (vía bandas) |
| 2 | `busquedas.json` + `bajar` + revisar hojas `medios` | ✅ 13-oct-2026 | 77/77 clips; 25 rehechos tras mirar hojas (webcams, logos, «Baby Shark» en el beat del tiburón); scene-029 = captura overgear (.png); `recorte_por` en 021/057/061 |
| 3 | Apoyos + 3 MG + Overgear + Lyria → mezcla → render → final → verificar → miniatura → subir privado | ✅ 13-oct-2026 | 37 apoyos, 3 MG (hoja de ruta, Cavernas, Gilneas), Overgear con código en nuestra voz; mezcla A (el usuario eligió B para los siguientes); revisión del MASTER cazó 3 clips; subido vODv9Gm0tjQ programado 18-oct 15:00 UTC |
| 4 | Campaña 2 de Overgear (coaching de WoW Forever, 10 % CRONICAS10): texto nuevo del segmento, voz Applio de las frases cambiadas, `reajustar`, recorrido por overgear.com/games/wow-forever/coaching como medio, insignias en pares, descripción de YouTube → mezcla → render → final → verificar → subir en privado (versión nueva) | ✅ 26-oct-2026 (absorbido por la fila del 27-oct) | segmento 42,5 → 45 s (total 668,1 s; capítulos +2,5 s tras el anuncio); rehechos 028, 032 y 030 (Midnight → Molten Core de «The raid encounter»); Lyria re-armada sin pedir nada nuevo |
| 5 | Adaptar a «Forever YA SALIÓ» (el usuario, 27-oct: se publica después del 4-nov): frases reescritas con el MISMO índice (intro, overgear, cierre…) + youtube.json → voz Applio → seleccionar → tiempo → reajustar → bajar beats que crecen → fx → Lyria armar → mezcla → render → final → verificar → avisar → subir privado SIN fecha | ✅ 27-oct-2026 | guion, youtube.json, voz (todas CER≈0), reajustar, clips que crecían rebajados con la misma url/desde, efectos (anclas y tarjeta «Salió el 4 de noviembre»), Lyria armada, mezcla ✅; MASTER 27-oct (11:35 con pantalla final; verificar OK, solo nombres propios con CER>2 % como antes; hoja de cambios revisada) → subido en privado SIN fecha ZinI3H8kleI (con miniatura y .srt); originales en _respaldo_prelanzamiento/ |

## Decisiones del episodio (preguntadas al usuario al empezar)
- duración total: ~11 min (como `wow_clases_ocultas`) · puestos de la lista: 8 (si la investigación no da 8 sólidas, bajar el número) · Overgear: SÍ lleva promoción (el usuario, 13-oct), código CRONICAS10 con nuestra voz; vía: por decidir

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (nada en curso; video subido y programado)

## Hecho
- Guion (fuentes y avisos en el docstring de `guion.py`), voz, `tiempo`, `beats` (77). `LYRIA.tramos` ya cabe: 167,5 / 165 / 137,5 / 67,5 / 128,1 s.

## Falta
- [ ] oído del usuario: Whisper transcribió raro Azshara, Alexstrasza, Uncas, huargen, Hyjal («Jiyal»), Stormwraith, Grim Batol («Green Battle» en p2_0) → `CER_MAX_POR_FRASE` subido SIN oírlas; si alguna suena mal, cambiar `FONETICA`
- [x] `medios/_overgear/` copiado · el texto `overgear` lo dio por bueno el usuario al pedir subir y programar
- [x] tramos 2 y 3

## Cómo retomar (comandos)
```
python fab.py estado <video>
python fab.py <video> bajar           baja lo que falte (rehacer: bajar 12,15 --rehacer | --q "otra búsqueda")
python fab.py <video> medios          hojas previews/medios_NN.jpg (MÍRALAS)
```

## Archivos clave
- `guion.py`, `beats.json`, `busquedas.json`, `fuentes.json` (de dónde sale cada clip), `medios/`, `salida/creditos.txt`

## Lecciones de este video (solo lo no obvio)
- Hojas `medios`: 25/77 clips rehechos (webcams, logos, Wowhead, «Baby Shark» en el beat del tiburón, cinemática IA en Karazhan); la hoja del MASTER cazó 3 más (texto «SOLO: 225 rep/hour», tramo casi negro, pillarbox de Warcraft I). Detalle en `docs/estilo_secuencia_yt.md` § «Lecciones de wow_pistas_futuro».
- Applio pronuncia mal «jugable» (Whisper oyó «Yaghebel» 3 veces): se cambió a «zona nueva». Icy Veins y Wowhead dan 403 a WebFetch: el legendario se documentó con resúmenes de búsqueda (guided.news, mmoexp), no con el artículo original.

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado y registrado (`canales/<alias>.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados: `docs/estilo_secuencia_yt.md` § «Lecciones de wow_pistas_futuro», `docs/voz.md` (cadena suave Applio), filtro de títulos en `nucleo/secuencia_yt.py`, imágenes locales en `nucleo/apoyos.py`

- **28-oct-2026 · kit Overgear «WoW - Forever (nov)» aplicado en efectos.py** (logo de esquina, par, tarjeta de coaching, reseñas con croma rojo, packshot «PLAY BETTER FOREVER»; revisado en hoja). SIN re-render: esperar el código y el creativo nuevos de Alice → cambiar CREATIVO/CREATIVO_DESDE + voz overgear_5/6 (decir «descuento mayor que el habitual, solo un mes») → fx → mezcla → render → final → verificar → subir la versión nueva en privado.

28-oct-2026 ✅ creativo del código de Alice (`medios/_overgear/CRONICAS10_forever.mp4`, -10 % CRONICAS10, rótulo en verde con croma; entra 2,5 s antes de «CRONICAS10») + kit Forever → fx, mezcla, render, final, verificar (CER como el 27-oct) → subido en privado SIN fecha: https://youtu.be/Hx0eAoY4szk. La voz no cambió: ya decía «diez por ciento». Fechas de Overgear: 1, 4, 5, 7 y 9-nov.
