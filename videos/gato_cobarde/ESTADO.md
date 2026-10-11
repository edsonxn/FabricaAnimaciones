# Mostacho y el ruido de la cocina — ESTADO
- canal: sin canal · prueba del estilo nuevo «cartoon90» (Coraje / dibujo animado de los 90, tinta redibujada cada cuadro)
- estilo: cartoon90 vertical, sin voz → docs/estilo_cartoon90.md · kit nucleo/toon*.py
- etapa: escenas 6/6 listas, música + SFX + mezcla hechos (−14 LUFS, pico −1,09 dBTP), `comprobar` pasa. NO se renderizó el video: el usuario renderiza escena por escena desde el panel
- siguiente: abrir el panel (`python fab.py panel --abrir`) → gato_cobarde → ▶ Vista previa → «Renderizar esta escena» (exterior, sala, pasillo, cocina, cosa, final); luego `python fab.py gato_cobarde final` y `verificar`

## Hecho
- Historia (personajes originales): gato flaco Mostacho duerme, un ruido lo despierta, cruza el pasillo con linterna y cascabel (retratos que lo siguen, sombra con cuernos), abre el refri (ojo gigante), GRITA y salta al techo; sale «la Cosa» (monstruo hambriento y asustado), grito a coro, la tarta cae en su boca, se hacen amigos; cenan y cae la sombra de verdad: grito, iris y cierre desde afuera de la casa (cierra el círculo con la primera toma).
- 6 escenas (7,5 / 7,5 / 10 / 12,5 / 12,5 / 10 s a 96 BPM), 216 efectos de sonido (40 sintetizados nuevos en `nucleo/sfx_toon.py`), música sintética `musica` (sabores tensión/vacío/épico/lounge).
- Vista previa del panel verificada (worker, cuadros, audio). ~0,4 s/cuadro, ~1 GB por proceso.

## Falta / ideas
- [ ] Escuchar la música (genérica) y decidir si se cambia por Lyria (`LYRIA` en guion.py, `python lyria.py --n 1 && --usar 1`, luego `mezcla`).
- [ ] Revisar el MASTER a tamaño completo (un cuadro cada ~3 s) cuando el usuario lo renderice; retocar tramos con `video --rehacer a-b`.
- [ ] Asignar canal, miniatura y título si gusta (no hay `youtube.json`).

## Archivos clave
- `guion.py` (SIN_VOZ, 24 compases a 96 BPM), `escenas.py` (CLASES), `esc_exterior|sala|pasillo|cocina|cosa|final.py`, `basec.py`, `mundos*.py`, `props.py`, `props2.py`, `_prueba.py`.

## Lecciones de este video (solo lo no obvio)
- Cámara aplicada dos veces en el rig (T incluía `h.tf` y `forma` también): con zoom 1 no se nota; con zoom las formas se desplazan. `T` devuelve MUNDO; `relleno/anillo` piden `h.tf(...)`.
- Con SEGS de caminata el pie apoyado no patina si la velocidad es 4·zancada·s/T (tabla de distancia acumulada, no `x = v·t`).
- Los fondos grandes (3 600 px de pasillo) pesan ~100 MB cada uno: LRU de 2 en `mundos.cacheado`.
