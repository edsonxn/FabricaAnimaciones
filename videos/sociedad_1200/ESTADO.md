# El caso de las 1.200 (agentes de OpenAI que asaltaron Hugging Face) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia · PROGRAMADO dom 18-oct-2026 14:00 CDMX (https://youtu.be/GMGBr5KkzTs; publishAt 2026-10-18T20:00:00Z, privado hasta la fecha, con miniatura B/N y .srt)
- estilo: noir_color (12-oct-2026: el usuario pidió REHACER TODAS LAS ESCENAS en NOIR A COLOR, más dinámicas) → docs/estilo_noir_color.md
- etapa: SUBIDO Y PROGRAMADO (12-oct). MASTER 15:47 verificado (CER 0,0003, desfase 0) y revisado con hoja 1 cuadro/3 s. Pendiente solo: `python fab.py sociedad_1200 limpiar` cuando el usuario lo apruebe, y hallazgos en docs/estilo_noir_color.md (cierre de video)
- vista previa: render parcial 0-9:21 (tramos 1-4) visto y aprobado por el usuario el 12-oct (`salida/sociedad_1200_AVANCE.mp4`). MASTER viejo (Gemini) apartado como `salida/sociedad_1200_viejo_gemini.mp4`.
- siguiente: cierre de video = escribir hallazgos en `docs/estilo_noir_color.md`; `limpiar` segmentos (4 GB en E:) al aprobar

## Sesiones (plan de tramos · «continúa el video de las 1200» retoma aquí · protocolo docs/sesiones.md)
- alias: las 1200, 1200, sociedad 1200
- leer al empezar: videos/sociedad_1200/GUIA_ESCENAS.md + la parte del tramo en PLAN_TOMAS.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1-4 | gancho … traicion (17 escenas) | ✅ 12-oct | mundos_1..4, esc_<id>.py; revisadas a la vista; preview 0-9:21 aprobado |
| 5 | sandbagging, evaluacion_falsa, mundo_exterior, taskrabbit, ciego, mentira_consciente | ✅ 12-oct | mundos_5.py (13 lugares); lotes revisados a la vista (cuadros a 30-90 %) |
| 6 | filosofia_peligro, dos_reglas, ironia_metr, tablero_final, cierre | ✅ 12-oct | mundos_6.py (7 lugares); Bostrom real; revisadas |
| 7 | sfx ✅ · Lyria (`nucleo/lyria_tramos.py`) · mezcla → video --procs 12 → final → verificar · hoja del MASTER | ✅ 12-oct | MASTER 15:47 verificado, subido y programado dom 18-oct (fila corregida el 13-oct: se había quedado en «en curso») |

## Decisiones (12-oct-2026)
- Escenas viejas de Gemini en `_viejo/` (no se usan). Paleta POR TOMA: `self.plano(t, fn, pal=...)`: laboratorio = medianoche; despacho/calle = sodio; Facebook 2017 = bourbon.
- Protagonista visual: LA COPIA (`reparto.py`): reo de overol con número y CABEZA DE MONITOR cuya pantalla es su cara. Ritmo: una toma nueva cada 3-5 s anclada a palabras, cámara siempre en movimiento.
- Medios reales: fichas de Sam Altman, Delangue, LeCun y Bostrom. Hecho verificado: informe METR/Redwood del 26-ago-2026. SFX: cada escena trae `sonidos()` (sfx_noir).
- Voz: «Once de la noche» salió «uans» (inglés) → ahora «11 de la noche» (y 8, 10, 11, 12 de julio, «1:30», «Alice»): ElevenLabs = escritura normal. Se regeneraron 5 frases; anclas de escena cambiadas a `w("8")`, `w("11")`, `w("10")`.
- Música procedural vieja guardada en `audio/musica_procedural.wav`; la nueva es Lyria adaptada al guion (regla global).

## Archivos
- `GUIA_ESCENAS.md` · `PLAN_TOMAS.md` · `basen.py` · `comun.py` · `reparto.py` · `props_s.py` · `mundos_base.py` · `mundos_1..6.py` · `esc_<id>.py` (`python _reg.py`)
- `_lote.py <escena> --fr 0.5,0.9 --procs 4` (cuadros por toma → previews/lote_0.jpg) · `_cuadro.py <escena> t1 t2` (cuadro completo) · `_ver_mundos.py mundos_N` · `_prueba.py` · `_mosaico.py`

## Cómo retomar (comandos)
```
python fab.py continuar las 1200
python fab.py sociedad_1200 mezcla ; python fab.py sociedad_1200 video --procs 12 ; python fab.py sociedad_1200 final ; python fab.py sociedad_1200 verificar
PYTHONPATH="<carpeta>;nucleo" python ../../nucleo/lyria_tramos.py todo      (música; no correr `musica`)
```

## Lecciones
- `NC.pegar(..., oscuro=k)`: k es GANANCIA (k>1 aclara, k<1 oscurece; Oxford con 0.35 salía negro). `h.c(v, rampa)` pide rampa válida (piedra, papel, madera, lacre, vino…; «verde»/«tinta» NO): para luz verde usa color 0-255 en `trazo(color=(150,255,190))`.
- Lugares con muros a tono ≤0.2 + `piedra` salen negros sobre las emisivas (parecen recortes): muros 0.25-0.35. Calle en perspectiva: copiar `mundos_5.calle_lluvia` (fachadas con ventanas + farolas + charcos).
- Conos de luz sobre papel lo queman (k≤0.7). `K.hoja` tono ~210; texto `N.texto_maquina` con `ancho_max` o líneas cortas (≤24 car. a 36 px en una hoja de 700 px).
- `P.mano(manga=…, largo_brazo=900)` dibuja una barra enorme: entra desde el borde (ang=π desde la derecha) y úsala solo con brazo corto (≤700). El `Detective` no levanta brazos: la mano que clava hilos va aparte o se omite.
- `Frontal.dibujar` ignora `manos`; `Figura` solo `brazo` 0..1. `K.caminante` tiene `d`, `andar`, `carga`; la fase por distancia evita patinar (`K.fase_paso(dist, s)`).
- Hojas de 2×N de lotes: un `Pool(4)` renderiza ~14 cuadros en 1-2 min. Las `banda` abajo tapan pies: en tomas de pies sube la banda (y=120).
- Mosaicos de cientos de cabezas: cerca ≤110 con `RP.cabeza_mini` y el resto con `C.rejilla_luces`. Evitar `·` en `texto_lienzo`; `P.TIZA`/`TIZA_B` para letra de pizarra; la fuente IMPACT no tiene «₿» (usar texto).
- Whisper lee «1:30» como «1 y 30»: `CER_MAX_POR_FRASE = {"redada_0": 0.05}`. Cambiar el TEXTO de un guion ya voceado → `fab.py <v> voz --solo <claves>` y luego `seleccionar` + `tiempo` (las escenas quantizadas por compás conservan sus límites).

- Lección 12-oct: miniatura = B/N como las anteriores de LogIA (el usuario rechazó la versión a color; guardada en salida/miniatura_color_descartada.jpg). Destello blanco de ~0,3 s en «mundo_exterior» (≈10:39) es intencional (flash al salir a la calle).