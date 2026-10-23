# ¿Por Qué Te DESPIERTAS a las 3 de la Mañana? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cuerpo_en_neon (Cuerpo en Neón, @cuerpoenneon) · hueco mar 27-oct-2026 14:05 CDMX (20:05 UTC)
- estilo: secuencia Flow + efectos (línea blanca sobre negro + un elemento en neón amarillo) → doc: docs/estilo_linea_neon.md
- etapa: SUBIDO y PROGRAMADO mar 27-oct-2026 14:05 CDMX (20:05 UTC) https://youtu.be/xnRw-_gBtMs (privado; miniatura A + .srt)
- siguiente: Studio > prueba A/B de miniatura (B en salida/miniatura_b.jpg) · métricas a 7 días (3-nov) en canales/formula/cuerpo_en_neon.md · `limpiar` al aprobar

## Sesiones (plan de tramos · «continúa el video despertar_3am» retoma aquí · protocolo docs/sesiones.md)
- alias: 3 de la mañana, despertar, 2.º de la fórmula nueva de Cuerpo en Neón
- vista previa: no (elegido por el usuario el 23-oct: 1 sesión, directo al MASTER, como duelo_cuerpo)
- leer al empezar: docs/estilo_linea_neon.md · fórmula: canales/formula/cuerpo_en_neon.md § «Revisión 22-oct» · modelo de archivos: videos/duelo_cuerpo/
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion → voz → beats → prompts → Flow → efectos → SFX → música → mezcla → render → final → rigor → subir y programar + Short | ✅ 23-oct-2026 | render 2006 s (33 min); tramo 93-101 rehecho y empalmado; Short `despertar_3am_short` en la misma sesión |

## Decisiones del episodio (23-oct-2026)
- el usuario eligió este tema en lugar de `corazon_roto` (n.º 2 de la tanda): el takotsubo ya sale en duelo_cuerpo y su Short (28-oct)
- validación vidIQ 23-oct: drkhoob Spanish «¿Te despiertas a las 3 AM?…» 4,4 M (63 K subs); llorar y abrazo 20 s sin señal; soledad: Fan de Ciencia 914 K
- escalera de la noche (11 · 1 · 3 · 3:15) + qué lo empeora + primer/segundo sueño (Ekirch) + 3 cosas + pregunta a comentarios
- protagonista nueva «el señor» (pijama a rayas, bigote); neón = su despertador interno (reloj sin números a las 3) u órgano que se nombra

## En curso
- nada

## Hecho
- MASTER 1080p 5:36,7, desfase 0, CER 0,0056 (solo «La 1 / Uno: / Dos: / Ekirch» → falsos positivos) · rigor: previews/rigor_1-5.jpg (112 cuadros cada 3 s), sin negros ni quietos > 2 s
- rigor encontró el despertador de scene-011 hecho mancha por el halo del FX neón → neón .25 (radio 4) entre 97,0 y 99,4 s, `video --tramo 93-101` + `_empalmar_tramos.py` (10 100 cuadros OK) + `final`
- subido privado y programado 27-oct 20:05 UTC (xnRw-_gBtMs), registrado en canales/cuerpo_en_neon.json y BITACORA
- voz ElevenLabs 301,4 s (1 930 créditos, cuenta 3; la 2 ya en 0) · tiempo 336,7 s · 70 beats (9 clips + 61 imágenes)
- Flow (proyecto «oct 23 - 07:49»): 61/61 imágenes Nano Banana 2.1 x1 a la primera (0 puntos) + 9 clips Omni 360p→1080 (63 puntos + 2 reenvíos: clip 6 rechazado por política de menores, clip 1 atascado en 99 %)
- efectos.py: 23 rótulos, 21 FX, 31 sonidos (27 SFX nuevos, 840 créditos) · `fx hoja` detectó el cierre anclado en el gancho (todo negro desde 0:39) y 9 rótulos sobre el neón
- música biblioteca: polilla_foco__lyria_tramo1 + wow_darrowshire__lyria_tramo7 + tes_misiones_nunca__lyria_tramo6 · mezcla −14,3 LUFS, voz 14,3 dB
- miniaturas Flow: A «NO ES INSOMNIO» (subida), B «3:00 AM» (salida/miniatura_b.jpg)
- guion.py: 45 frases, 856 palabras; 8 DOI verificados en Crossref (Weitzman 1971, Ohayon 2008, Ohayon 2004, Ebrahim 2013, Tubbs 2022, Tang 2007, Scullin 2018, Ekirch 2001)

## Falta
- [ ] prueba A/B de miniatura en Studio · [ ] medir a 7 días (3-nov) · [ ] `limpiar` al aprobar

## Lecciones de este video (solo lo no obvio)
- Un despertador de neón GRUESO (contorno ancho) se vuelve mancha con el FX `neon` a .9: revisar a tamaño completo los cuadros con objetos de neón grueso y bajar el neón por tramo (`de`/`a` en segundos).
- Ancla del cierre repetida en el gancho = todo negro desde ahí: `#2`. Lo vio `fx hoja` antes del render.
- Prompt de clip con «small sleeping figure floating» → rechazo de Flow por «menores de edad».
