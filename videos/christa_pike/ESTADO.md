# Christa Pike: la ejecución que no terminó (documental serio, 8:15) — ESTADO
- canal: edsonxn · PUBLICADO (público) 3-oct-2026 ~19:00 CDMX (PGF2sbmC0po)
- estilo: documental → docs/estilo_documental.md (§ «Documental de NOTICIA / crimen real») · ejemplo: videos/voynich/ · voz Faraon · música Lyria · SIN subtítulos quemados
- etapa: publicado (verificado en YouTube 6-oct-2026) · MASTER 8:15, CER 0,0009, −14 LUFS · miniatura IA · .srt
- siguiente: ver retención a las 48 h; si hay novedades del caso, nota fijada o actualizar descripción. Al aprobar: `python fab.py christa_pike limpiar`

## Hecho
- Hechos verificados con texto completo en `fuentes/*.txt` (AP, Newsweek, CBS, Fox 9, Al Jazeera, ABC, NBC, Wikipedia). Discrepancias vistas y NO usadas: Al Jazeera dice 18 años al condenar (eran 20); un resumen dio 1-oct como fecha del intento (fue 30-sep).
- Pronunciación: nombres ingleses fonéticos en la narración (`PRON`) + `ALIAS_QA`. «treinta y un» NO pasa el QA: reescrito.
- Material: fotos Commons (`imagenes/creditos.json`), mapa de relieve real (`hacer_mapa.py`, `mapa_lugares.py`), clips de noticias con yt-dlp (`bajar_clips.py`, `cortes.py`), stock Pexels/Pixabay (`bajar_stock.py`), 5 mapas de profundidad (parallax).
- Música: `_lyria_segmentos.py` (3 tramos, prompt neutro, reintentos) → `audio/musica.wav`. NO correr `fab.py ... musica` (procedural la pisaría).
- Revisadas a tamaño medio hojas de cuadros de toda la línea de tiempo real (0-495 s) y corregidos: etiquetas sobre rostros, créditos cortados, tomas negras, letras ilegibles, mapa con nombres.

## Falta
- [ ] AVISAR al usuario: material de noticias con derechos (WBIR/Tegna, France 24, NBC, ABC, NewsChannel 5) → mirar «Derechos de autor» en Studio antes de publicar; la historia sigue abierta, revisar noticias del día de subida

## Cómo retomar (comandos)
```
python fab.py estado christa_pike
python fab.py christa_pike final
python fab.py christa_pike verificar
cd videos/christa_pike ; $env:PYTHONPATH="C:\FabricaAnimaciones\videos\christa_pike;C:\FabricaAnimaciones\nucleo" ; python _hoja.py 10 20 30   (cuadros de prueba -> previews/hoja.jpg)
```

## Archivos clave
- `guion.py` (datos con fuente, PRON, ALIAS_QA, LYRIA), `kit_cp.py` (anclas por palabra, fondos, MAPA, RELOJ, LINEA_ANOS, CRONO, F_vena, F_ventana_piedra, CRED), `tomas_a.py`, `tomas_b.py`, `escenas.py` (solo `Mundo`), `_ronda.py` (voz con reintentos), `_lyria_segmentos.py`, `hacer_youtube.py`, `revisar_master.py`
- `_tl_falso.py` = timeline provisional con el ritmo medido de Faraon (2,37 palabras/s)

## Lecciones de este video (solo lo no obvio)
- Faraon: 2,37 palabras/s. 8 min ≈ 1.100 palabras en 72 frases (incluye 11 s de créditos al final y una escena de contexto añadida tras ver el timeline real).
- Lyria bloquea al azar y por palabras sensibles; una pieza dura ≤ ~3 min → hay que pedirla en tramos (ver docs/estilo_documental.md).
- Los clips de noticias traen cortes duros y rótulos inferiores: `banner=` y `fin=` con `cortes.py`. Las etiquetas (`TAG`) no deben tapar rostros.
- El render de 8 min con este kit tarda ~80 min (2,2 s/cuadro/proceso con 8 procesos).

- v2 (3-oct): escenas DIBUJADAS propias (`mg.py`, `mg_obj.py`, `mg_esc*.py`) sustituyen al stock reciclado por feedback del usuario; `tomas_a_v1.py`/`tomas_b_v1.py` = versión anterior con stock.
