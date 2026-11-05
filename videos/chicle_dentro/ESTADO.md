# ¿Qué pasa DENTRO de tu cuerpo si te tragas un chicle? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: kuriox (LARGO horizontal 1920x1080, ~6 min) · hueco: lun 9-nov 14:00 CDMX (`canales --actualizar` del 5-nov)
- estilo: ACUARELA PINTADA A MANO POR CÓDIGO → docs/estilo_acuarela_pincel.md · kit copiado de videos/ia_como_ve/ (mismo formato: Kuri + la niña)
- etapa: guion ✅ · voz en marcha · kit copiado · fotos reales ✅ (Santa Anna, Thomas Adams, chiclero)
- siguiente: planos a-g (gancho, origen, bajada, estómago, intestino, peligro, cierre) con `_hoja.py` → SFX → música biblioteca → mezcla → render → MASTER → subir

## Sesiones (plan de tramos · «continúa el video chicle» retoma aquí · protocolo docs/sesiones.md)
- alias: chicle_dentro, chicle, el video del chicle, el chicle de los 7 años
- vista previa: NO; «hazlo completo hasta master» (el usuario, 5-nov). Todo seguido; si salta el corte de tokens, sesión nueva por el hook
- leer al empezar: este ESTADO.md · `guion.py` (datos y frases) · docs/estilo_acuarela_pincel.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz + kit + planos a-g + SFX + música + mezcla + render + subida | ✅ 5-nov | MASTER 6:05 (98 segmentos en 20 min con 4 procesos), subido privado y PROGRAMADO lun 9-nov 14:00 CDMX: https://youtu.be/Kfo-P8LgrPg (miniatura Flow aplicada) |

## Etapa
- ✅ CERRADO 5-nov: subido y programado (lun 9-nov 14:00 CDMX). Pendiente solo `python fab.py chicle_dentro limpiar` cuando el usuario lo apruebe.
- Música: corn_flakes__lyria_tramo1 (Plastitube), polilla_foco__lyria_tramo1 (WND), sin_medicina__lyria_tramo2 (Sapiens): públicos distintos al de Kuriox.

## Datos y fuentes
- En el docstring de `guion.py` (Pediatrics 1998 doi:10.1542/peds.102.2.e22 verificado en Crossref). Comentarios del canal: 0 nuevos (5-nov), nada que enseñar.

## Lecciones
- Planos escritos sin probar: todos tenían personajes demasiado pequeños para 1920x1080 (Kuri 0,3-0,8, bolita r 30-70): la LUPA (círculo de
  papel con Kuri sentado en la bolita en grande + hilo hasta la bolita diminuta) resuelve los planos de mapa/corte anatómico.
- `pop()`/otros SFX de duración fija sumados a un ruido de otra duración revientan con broadcast: sumar por recorte (`x[:len(p)] += p`).
- Whisper escribe «sictli» y «Santa Ana»: `CER_MAX_POR_FRASE` en guion.py en vez de regenerar (las tomas ya estaban pagadas).
- `python fab.py nuevo --help` CREA un video llamado «--help» (se borró): no pasar --help a `nuevo`.
