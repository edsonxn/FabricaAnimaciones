# Never Kill a House Centipede. Here's Why — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: wild_next_door (EN INGLÉS) · PROGRAMADO lun 12-oct-2026 16:00 UTC (https://youtu.be/8voZAKYUAkM, privado hasta la fecha)
- estilo: secuencia_flow (ilustración dibujada; imágenes de Google Flow, sin clips de video) → docs/estilo_secuencia_flow.md · ejemplo: videos/aranas_otono/
- etapa: resubido y programado el 7-oct-2026 (la subida vieja oFi5HDkClVE fue pública por error y quedó en privado: el usuario la borra en Studio)
- siguiente: nada; opcional `python fab.py ciempies_casa limpiar`

## Decisiones del episodio
- Tercer video del canal, pedido por el usuario («te pones a hacer el siguiente»); mismos ajustes que arañas: todo imagen porque Flow no tiene puntos de video
- ~4:40 (688 palabras, 58 frases), voz EnglishComic; el ciempiés lleva un sombrerito azul de detective (FICHA) para reconocerlo entre imágenes

## Hecho
- Guion, voz 58/58, 66 beats e imágenes (la 5 rehecha por marco), armado, mezcla −14,03 LUFS, verificado (CER medio 0,0023; `legs_1` es falso positivo: Whisper escribe «15»), miniatura, subida

## Falta
- nada

## Cómo retomar (comandos)
```
python fab.py estado ciempies_casa
python fab.py ciempies_casa servir      (puente con Flow; pasos en docs/estilo_secuencia_flow.md «Generar en Flow»)
python fab.py ciempies_casa medios
```

## Archivos clave
- `guion.py` (narración + FICHA), `_ronda.py`, `beats.json`, `prompts.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- Flow añadió el modelo «Nano Banana 2.1» y lo dejó por defecto: flowscrap falla con «no expuso el control accesible». Antes de lanzar, elegir a mano «Nano Banana 2 Lite · x1» en el chip.
- Frases con números ≥ 10 no pasan `seleccionar` (Whisper escribe cifras): usar `CER_MAX_POR_FRASE` en guion.py tras oír qué transcribe.
