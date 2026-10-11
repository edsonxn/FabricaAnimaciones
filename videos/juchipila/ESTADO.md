# Juchipila: el lugar de las flores nobles — ESTADO
- canal: bitacora_perdida · sin fecha (el usuario decide; ver `python fab.py canales --actualizar` para el hueco)
- estilo: kurzgesagt ISOMÉTRICO + personajes 2D (`kz_pers2d`) + conceptos abstractos (`kz_abstracto`) → docs/estilo_kurzgesagt.md §A (+ «Lecciones de videos/juchipila») · ejemplo: videos/independencia_mx/
- etapa (11-oct-2026): **las 13 escenas están escritas** (t01…t13 + mundos_a…n), revisadas con hojas de prueba y corregidas; prueba de humo de todo el video sin errores (`./run.sh _humo.py 2`). Voz y timeline listos (498,33 s).
- 11-oct (tarde): música Lyria en 4 tramos (`LYRIA["tramos"]`, `lyria_tramos.py todo`), `sfx` (151 eventos) y `mezcla` (-14 LUFS, voz/fondo 14,6 dB) HECHOS. El usuario pidió render completo: `python fab.py juchipila video` → `final` → `verificar`; él lo ve y decide si se sube (hueco del canal: jue 15-oct) o se corrige.
- 11-oct: MINIATURA hecha (Flow, Nano Banana 2 Lite, 0 puntos): «FLORES Y GUERRA» → `salida/juchipila_mini_flowA.jpg` (1280x720); prompts A/B en `prompt_miniatura.md`. Falta: revisar el MASTER a tamaño completo y listar correcciones.
- 11-oct (tarde): el usuario decidió NO corregir y subir con el render actual. SUBIDO en PRIVADO: https://youtu.be/UHZ9sXW0D1g (miniatura «FLORES Y GUERRA» + .srt + youtube.json). Defectos documentados en `REVISION_MASTER.md` y en `docs/estilo_kurzgesagt.md` § «ERRORES A NO REPETIR». PROGRAMADO jue 15-oct-2026 20:00 UTC (14:00 CDMX). (Ya no falta: elegir fecha (hueco sugerido jue 15-oct 14:00 CDMX = 20:00 UTC) con `yt publicar bitacora_perdida UHZ9sXW0D1g public --programar <ISO UTC>`.
- (antes) siguiente: si aprueba → miniatura Google Flow, `youtube.json`, subir privado y programar; si no → `video --rehacer <tramos>` + `final`.

## Acuerdos con el usuario (4-oct-2026)
- **NO renderizar el video completo: el usuario renderiza escena por escena desde el panel** (excepción 11-oct: pidió render completo). Yo escribo y reviso con hojas cortas (`./_esc.sh <escena> [n]`, `./run.sh _prueba.py nombre t1 t2…`, `./run.sh _cuadro.py t nombre` = 1 cuadro a tamaño completo).
- NO tocar los textos de `guion.py` (regenera voz).

## Escenas (archivo · mundos · qué se ve)
| id | archivo | qué hay |
|---|---|---|
| gancho, canon, ventanas, caxcanes, llegada | t01–t05 | ver docstrings; 11-oct: río antes del pueblo y casas en las orillas, guerreros en las crestas, «junio», tablero del reparto, pergamino fuera de la cara, medallones en capa 1 |
| hartazgo | t06 · mundos_g | tributo y templo derribado; encomendero vs. frailes; olla + termómetro; emisarios nocturnos con antorcha + recuadro del mapa real; 1540 en el mapa; memorial; peñol 2D |
| mixton | t07 · mundos_h | peñol isométrico y fracaso; Oñate pide ayuda; Alvarado (retrato real) + Templo Mayor; junio 1541; Tenamaxtli; caída del caballo; 10 días; confianza; Guadalajara |
| mendoza | t08 · mundos_i | Mendoza (retrato real) y el occidente; salida de México con volcanes; aliados convergentes; Nochistlán 9-nov-1541 y fuga; dos peñoles; cerco del Mixtón |
| castigo | t09 · mundos_j | gris-violeta: iconos duotono; mina en corte; ruinas y huida; ciudad fantasma y refugio; Consejo de Indias con lupa; encrucijada sierra/valle |
| refundacion | t10 · mundos_k | frailes; 6 000 bajan de paz; pueblo que se construye → convento y templo 1627; alcaldía mayor 1548-1786; 1810 insurgentes |
| tenamaxtli | t11 · mundos_l | linaje; guerrilla bajo la lluvia; SE BUSCA 1552; barco a España; Las Casas (retrato real); memorial; Consejo 1-jul-1555; ventana con lluvia 1556; línea de tiempo |
| revolucion | t12 · mundos_m | calle 1909 y «El Nuevo Mundo» + club; arresto y Lecumberri; Madero (real) 22-feb / alzamiento 15-abr-1913; caballería y Natera (real); Ocotlán 1914; Villa y Natera toman Zacatecas |
| cierre | t13 · mundos_n | Juchipila hoy (12 251 hab.); migración y remesas; junio en flores; tastoanes con Santiago; título; ¿qué pueblo sigue? |

## Falta
- [ ] El usuario renderiza las 13 escenas en el panel (las de t01–t05 quedaron en ámbar por los arreglos)
- [ ] Música Lyria (`$env:PYTHONPATH="<video>;C:\FabricaAnimaciones\nucleo"; python ..\..\nucleo\lyria.py --n 1` y `--usar 1`), `python fab.py juchipila sfx`, `mezcla`
- [ ] Revisión a tamaño completo sobre el MASTER (regla de rigor) · miniatura con Google Flow · metadatos y programar

## Lecciones de este video (solo lo no obvio)
- Los `snd()` de t01–t13 están DENTRO de las funciones de dibujo → `sfx` veía 0 eventos (y `sfx.wav` salía NaN). `escenas.Mundo.preparar` ahora dibuja cada toma una vez solo en la etapa `sfx` y quita duplicados.
- Lyria da ≤ ~3 min por pieza: con 8:18 hay que usar `LYRIA["tramos"]` + `lyria_tramos.py`, no `lyria.py`.
- Fuentes en conflicto (resueltas en `guion.py`): NO «Pueblo Mágico»; no se nombra dónde murió Alvarado; Mixtón «finales de 1541 / inicios de 1542»; fundación «hacia 1542-43».
- La narración dice «Cuando asesinaron a Madero, el quince de abril de 1913, Robles se levantó»: Madero murió el 22-feb-1913 y Robles se alzó el 15-abr. En pantalla van las DOS fechas separadas (t12 D) para que no se lea como fecha del asesinato.
- Whisper falla con nombres náhuatl: Xochipillan/Xúchitl solo en pantalla.
- Fondos de medallón con busto K2 dentro → `capa=1` (en capa 2 lo tapan). Pueblos a < 60 km no caben en el mapa ETOPO (zoom ≤ 5,5): escena 2D + `mundos_g.inset_mapa`.
- Retratos reales nuevos: alvarado, mendoza, lascasas, madero, natera, villa. Sin retrato (dibujados): Nuño, Oñate, Tenamaxtli, Robles, frailes.
