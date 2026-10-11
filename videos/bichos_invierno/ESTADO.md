# Where Do All the Bugs Go in Winter? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: wild_next_door (EN INGLÉS) · PROGRAMADO jue 15-oct-2026 16:00 UTC (https://youtu.be/AYmaIJedCPc, privado hasta la fecha)
- estilo: secuencia_flow (ilustración dibujada; 7 clips de video al inicio + imágenes de Google Flow) → docs/estilo_secuencia_flow.md · ejemplo: videos/avispas_invierno/
- etapa: resubido y programado el 7-oct-2026 (la subida vieja mqHB3cK7RF8 fue pública por error y quedó en privado: el usuario la borra en Studio)
- siguiente: nada; opcional `python fab.py bichos_invierno limpiar`

## Decisiones del episodio (del usuario, 7-oct-2026)
- duración total: 9 min (1320 palabras, 111 frases) · video inicial: los clips que alcancen con 55 puntos = 7 clips de 10 s (70 s) · 360p reescalado gratis al descargar · dos escenas por clip con transición dibujada (`combinar=True`)

## Hecho
- Guion (17 bloques), voz 111/111 (4 frases aceptadas con `CER_MAX_POR_FRASE`: cifras y «mourning»), 8:39, 108 beats, prompts, youtube.json, 7 clips

## Falta
- nada. Máster 8:39, −14,21 LUFS, pico −1,05 dBTP, ambiente de los 7 clips al 50 %, CER medio 0,0043 (4 frases marcadas son falsos positivos: cifras y «Wooly»)

## Cómo retomar (comandos)
```
python fab.py estado bichos_invierno
python fab.py bichos_invierno servir
python fab.py bichos_invierno medios
```

## Archivos clave
- `guion.py` (narración + FICHA), `_ronda.py`, `beats.json`, `prompts.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- Clips 360p + descarga mejorada y dos escenas por clip: funcionan (7 puntos c/u). El clip 4 trae un marco fino en su primera escena: usar `recorte_por` si se nota.
- flowscrap falló en los clips 6-7: con DOS pestañas de Flow abiertas (una congelada) leía el chip de la otra y cambiaba a 720p (15 puntos); su control «Flow no confirmó 360p» evitó el gasto. Se enviaron a mano (chip en 360p, pegar prompt, ··· → Descargar → 720p Resolución mejorada). Tener UNA sola pestaña de Flow.
- NO generar imágenes en el mismo proyecto de Flow donde hay clips: la extensión toma el mosaico equivocado y las imágenes llegan corridas una posición (y Flow sacó 2 por prompt). Proyecto NUEVO y vacío para el lote de imágenes, y comprobar las 8 primeras contra su texto.
- `servir` en segundo plano: redirigir el log con ruta absoluta (con ruta relativa falló dos veces al arrancar).
