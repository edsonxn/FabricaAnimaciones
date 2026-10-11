# What Happens to Wasps When Winter Comes? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: wild_next_door (EN INGLÉS) · sin fecha
- estilo: secuencia_flow (ilustración dibujada, tinta y color plano; clips e imágenes de Google Flow) → docs/estilo_secuencia_flow.md
- etapa: publicado el 6-oct-2026 en público: https://youtu.be/sHqcDnMrQTU
- siguiente: mirar métricas en unos días (`python fab.py yt metricas wild_next_door 28`); probar la miniatura B si el CTR sale bajo

## Decisiones del episodio (del usuario, 6-oct-2026)
- 6 minutos · 1 minuto inicial en video (clips de 8 s) · voz EnglishComic · estilo ilustración dibujada sobre fondo claro
- Tema elegido por investigación de nicho: ola de videos de avispas (Zyka, 821 mil vistas en 10 días con 1,5 mil subs)

## Hecho
- Guion en inglés: 73 frases, 830 palabras, 12 bloques. Voz EnglishComic: 73/73 con CER 0 (una frase reescrita: «waists» no pasaba)
- 74 beats: 4 clips de video de Flow (beats 1-4) + 70 imágenes. Los beats 5-8 iban a ser video pero se acabaron los puntos de Flow
- MASTER `salida/wasps_winter_MASTER.mp4`: 5:31, 1080p, -14,0 LUFS, pico -1,36 dBTP, voz/fondo 11,6 dB, CER 0 sobre la mezcla, desfase 0 ms
- Revisión visual: 4 hojas de medios completas, cuadros de los 4 clips, 9 cuadros del primer minuto y `final_hoja.jpg`
- Miniatura `salida/miniatura.jpg` («THE ONLY SURVIVOR», dibujada, fondo claro); alternativa `miniatura_b.jpg` («WHERE DID THEY GO?»)
- `youtube.json` en inglés con capítulos y fuentes

## Falta

## Cómo retomar (comandos)
```
python fab.py estado avispas_invierno
python fab.py avispas_invierno servir        (puente con Flow; pasos en docs/estilo_secuencia_flow.md «Generar en Flow»)
python fab.py avispas_invierno medios
```

## Archivos clave
- `guion.py` (narración + FICHA visual), `_ronda.py`/`_ronda.log`, `beats.json`, `prompts.json`, `flow/escenas.json`, `medios/`

## Lecciones de este video (solo lo no obvio)
- La extensión flowscrap necesita el chip de Flow en «Nano Banana 2 Lite · x1» y estar recargada (versión 0.14.5).
- Chrome guardó las descargas con nombre uuid: usar el puente (`servir` + recolector), no `ingesta`.
- Flow se quedó sin puntos al 5.º clip («No tienes saldo suficiente»): la extensión no lo detectó y se quedó esperando; hubo
  que detener, pasar el chip a Imagen a mano y refrescar la pestaña para que la cola volviera a andar.
- La etapa `sfx` sin eventos escribía un sfx.wav con NaN que dejaba la mezcla muda (Whisper oía «Thank you»): corregido en mezcla.py.
- Tres clips salieron con marco de viñeta: `recorte_por` en SECUENCIA los recorta.
