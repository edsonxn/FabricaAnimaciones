# Why Spiders "Invade" Your House Every Fall (They Don't) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: wild_next_door (EN INGLÉS) · PROGRAMADO vie 9-oct-2026 16:00 UTC (https://youtu.be/A0uq0XZgWmI, privado hasta la fecha)
- estilo: secuencia_flow (ilustración dibujada; imágenes de Google Flow, sin clips de video) → docs/estilo_secuencia_flow.md · ejemplo: videos/avispas_invierno/
- etapa: resubido y programado el 7-oct-2026 (la subida vieja 9E9j5ZWxZHo fue pública por error y quedó en privado: el usuario la borra en Studio)
- siguiente: nada; opcional `python fab.py aranas_otono limpiar`

## Decisiones del episodio
- Segundo video del canal, pedido por el usuario («te pones a hacer el siguiente»); mismos ajustes que avispas salvo video: todo imagen porque Flow quedó sin puntos
- 4:37 (699 palabras), voz EnglishComic; fuente principal: Rod Crawford, Burke Museum

## Hecho
- Armado, mezcla, final, verificar, miniatura (`salida/miniatura.jpg`) y subida
- Guion (58 frases, 11 bloques), voz 58/58 con CER 0 (una frase reescrita: «egg sacs» no pasaba), timeline, 69 beats, 69 prompts

## Falta
- nada. Máster 4:37, −14,03 LUFS, CER medio 0,0019 (la única frase marcada, `locals_7`, es falso positivo: Whisper escribe «5 out of every 100» con cifras)

## Cómo retomar (comandos)
```
python fab.py estado aranas_otono
python fab.py aranas_otono servir      (puente con Flow; pasos en docs/estilo_secuencia_flow.md «Generar en Flow»)
python fab.py aranas_otono medios
```

## Archivos clave
- `guion.py` (narración + FICHA), `hacer_prompts.py` → `prompts.json`, `beats.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- El macho lleva un moñito rojo en la FICHA para distinguirlo de la hembra y de las arañas genéricas entre imágenes.
