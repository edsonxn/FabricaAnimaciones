# Historia de Estados Unidos en 6 minutos — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronopapel · SUBIDO y PROGRAMADO vie 30-oct-2026 14:00 CDMX (dGkN7MnhxoA; publishAt 2026-10-30T20:00:00Z) con miniatura y .srt
- estilo: boceto + guache con mapa ETOPO1 → doc de estilo: docs/estilo_boceto_guache_mapa.md (§ v2.2 sale de este video) · ejemplo: este video y videos/historia_mexico/
- etapa: TERMINADO (MASTER 6:01, CER 0,0006, −14 LUFS, revisado cada 3 s) · subido y registrado (canales/cronopapel.json, BITACORA)
- siguiente: ver retención tras publicarse; `python fab.py historia_eeuu limpiar` cuando el usuario lo apruebe (segmentos/ 516 MB)

## Sesiones (plan de tramos · protocolo docs/sesiones.md)
- alias: historia de Estados Unidos, historia_eeuu, EEUU, Estados Unidos en 6 minutos
- formato: `historia_pais_5m` · variable probada: país no hispano de enorme búsqueda en español (EEUU) a 6 min
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz + tiempo + mapa ETOPO1 (campos_us) | ✅ 17-oct | cortado al 81 % de la ventana; el resto pasó al tramo 2 |
| 2 | dibujos + escenas 0-6 min + audio + render + final + verificar + miniatura + youtube.json + subir | ✅ 22-oct | el usuario pidió terminarlo en una sesión: dibujos en 3 subagentes en paralelo mientras se escribía la coreografía |

## Hecho
- guion.py: 54 frases, 14 escenas, FONETICA para Dan, ALIAS_QA, LYRIA por escena; datos con fuentes (DOI White Sands verificado en Crossref)
- mapa.py «us» (relieve NOAA ETOPO1, 33 campos, 48 estados para la fractura) · `pal_us.py` (paleta)
- dibujos propios: `obj_us1.py` (65 personajes), `obj_us2.py` (54 objetos/animales/barcos hasta 1890), `obj_us3.py` (52 de 1860 a hoy) · sellos: 12 emblemas en `sellos._dibujar_us`
- `coreo_1..4.py` (todas las escenas), cámara por paradas (`para`/`foco`), 13 transiciones procedurales
- música Lyria en 3 partes (candidatos 2·1·2 por correlación de energía) → `audio/musica.wav`; 181 SFX; mezcla −14 LUFS, voz 13 dB sobre música+sfx
- render 26 min con 8 procesos (convivió con la voz de otra sesión) · `miniaturas.py` (variantes eeuu y superpotencia; se subió «eeuu») · `youtube.json` con 13 capítulos y fuentes

## Lecciones (no obvias)
- Con claves de cámara sueltas la cámara nunca llega al lugar: usar paradas (`para`/`foco`). Y la última clave de una escena puede caer después de la primera de la siguiente: `escenas._sin_solapes` lo arregla (si no, la cámara cruza el país de ida y vuelta).
- `core.Fractura` con `"estados"` daba 0 celdas (n salía de CELDAS_SEMILLAS): n = 49 con `fijas=(0,)`.
- `_lyria_partes.py` ahora nombra los candidatos `audio/lyria_ly<P>_<k>.mp3`: sin «lyria» en el nombre la biblioteca de música no los veía (México sigue con `ly*.mp3` sin catalogar).
- El sello grande va a (1720, 400): a 760 chocaba con el personaje de la derecha.

## Cómo retomar (comandos)
```
python fab.py estado historia_eeuu
cd videos/historia_eeuu ; ./run.sh _prueba.py 30 120 ; ./run.sh _hojas.py 3 ; ./run.sh _qa_choques.py 0.25
```
