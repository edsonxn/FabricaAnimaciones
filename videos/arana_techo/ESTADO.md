# Never Kill the Spider in Your Ceiling Corner — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: wild_next_door (EN INGLÉS) · meta: dom 18-oct-2026 16:00 UTC (hueco siguiente a `bichos_invierno`, 15-oct)
- estilo: secuencia_flow (dibujo animado de Flow: 8 clips al inicio + imágenes) → docs/manual_wild_next_door.md · ejemplo: videos/ciempies_casa/
- etapa: PROGRAMADO dom 18-oct-2026 16:00 UTC (https://youtu.be/gG2REwAK54Q, privado hasta la fecha, con miniatura); aprobado por el usuario el 11-oct
- siguiente: el 25-oct medir (`yt videos` + `yt metricas wild_next_door 90`) y llenar su fila en `canales/formula/wild_next_door.md`; `python fab.py arana_techo limpiar`

## Decisiones del episodio (del usuario, 11-oct-2026)
- Tema elegido con datos: formato «Never Kill» (el ciempiés es el ganador del canal) + la cellar spider que caza viudas
  negras (×382 / ×32 / ×30 en 3 canales chicos). Análisis: `canales/formula/wild_next_door.md`.
- Duración 9 min pedida → 8:51 reales (1 388 palabras, 106 frases, 15 bloques).
- Video: los 55 puntos = 7 clips de 10 s + 1 de 8 s (78 s, 360p con descarga «720p mejorada», 2 escenas por clip).
- Mascota: cellar spider con gorra azul de vigilante nocturno; villana: viuda negra con cejas de enojo (FICHA).

## Hecho
- Guion con ficha de hechos, voz 106/106 (`widow_7` y `mother_1` aceptadas: homófonos), 110 beats, 110 prompts.
- Clips 8/8 (proyecto Flow «oct 11 - 08:48»): 1-5 por flowscrap; 6-8 a mano (flowscrap saltaba a 720p). Verificados por
  huella contra `Descargas/flow-arana_techo/`. `recorte_por`: marcos en 1, 3, 4, 5, 7 y 8; números de estatura en el 6.
- Imágenes 102/102 (proyecto «oct 11 - 09:24»); 11 rehechas en una 2.ª ronda (rótulos, marcos, cara del conductor de TV;
  las viejas en `medios/_ronda1/`).
- Música Lyria en 4 tramos (tramo 4 rehecho; silencios de las uniones recortados; respaldos `_con_silencio`/`_largo`).
- MASTER 1080p 8:51, −14,03 LUFS, pico −1,28 dBTP, voz/fondo 12,9 dB, CER 0,001 (`hook_0` = falso positivo: «2» con cifra),
  sin desfase. Revisado con la vista: un cuadro cada 3 s + arranques de clips a tamaño completo. `.srt` hecho.
- Miniatura `salida/miniatura.jpg` («NEVER KILL IT»; alternativa `miniatura_alt_902.jpg`), `youtube.json` con fuentes.

## Falta
- [ ] Que el usuario vea el MASTER; luego subir en privado programado para el 18-oct 16:00 UTC y anotarlo en
      `canales/wild_next_door.json` (`"formato": "never_kill"`, `"prueba": "9 min + 78 s de clips"`) y en BITACORA
- [ ] A los 7 días (25-oct): llenar su fila en `canales/formula/wild_next_door.md`
- [ ] Tras aprobar: `python fab.py arana_techo limpiar`; borrar `salida/tramo_0_188.mp4` y `vista_previa_0_188.mp4`

## Cómo retomar (comandos)
```
python fab.py estado arana_techo
python fab.py yt videos wild_next_door
python fab.py yt subir arana_techo wild_next_door private --publicar 2026-10-18T16:00:00Z
```

## Archivos clave
- `guion.py` (narración + FICHA + LYRIA + clips_s), `hacer_prompts.py`, `_miniatura.py`, `_voz_previa.py`, `beats.json`, `medios/`

## Lecciones de este video (solo lo no obvio; también en docs/manual_wild_next_door.md)
- Para gastar TODO el saldo de Flow conviene mezclar duraciones (`clips_s`): el clip de 10 s rinde más por punto.
- NO reiniciar `servir` en medio de un lote de clips: los clips quedaron corridos una posición (código ya corregido).
- El modelo de VIDEO dibuja la telaraña en espiral aunque se pida «no spiral»; el de imagen sí obedece.
- `final` falla con «Acceso denegado» si el MASTER está abierto en un reproductor: cerrarlo o mover el `.tmp.mp4`.
