# ¿Puede una IA guardar un secreto? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia · ✅ SUBIDO y PROGRAMADO sáb 24-oct-2026 14:00 CDMX (2026-10-24T20:00:00Z) · https://youtu.be/_OCS1atQpQA (private, miniatura + .srt)
- estilo: noir con PEGATINA FLOW (`ESTILO_VISUAL = "pegatina_flow"`) → docs/estilo_pegatina_flow.md §7a + docs/estilo_noir.md § «ERRORES A NO REPETIR — secreto_ia»
- etapa: ✅ TERMINADO 21-oct (montaje aprobado por el usuario; rigor del MASTER: 60 cuadros cada 3 s + hoja 2×3 + blackdetect solo en el fundido final 0,33 s; CER 0, desfase 0; 3 encuadres corregidos que reflejaban el borde inferior del fondo) · registrado en canales/logia.json («formato»), BITACORA, panel
- ✅ **PÚBLICO** desde el sáb 24-oct 14:00 CDMX · https://youtu.be/_OCS1atQpQA (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
- siguiente: tras el estreno (24-oct) métricas `yt metricas logia` y `python fab.py secreto_ia limpiar` (segmentos/ 818 MB) cuando el usuario lo apruebe. El código de Gemini queda en `_gemini/`
## Historial del tramo (21-oct-2026, sesión de buenos días, cuenta jairedson5 / plan Max)
- FICHA noir en guion.py + LYRIA (3 tramos) · `_prompts.py` → prompts.json (16 escenarios + 8 hojas) · `_bundle.js`
- Flow en el CHROME del usuario (proyecto «oct 21 - 09:39», Nano Banana 2.1, 16:9, x2, 0 puntos): 24 prompts ✅ · escenarios 1K
  (`_ordenar_flow.py`: variante elegida = `_a`, marco de papel recortado; las otras en `imagenes/_flow1k/`) · hojas 2K ✅ (Chrome →
  Descargas → `hojas/`, comprobadas por correlación) · recorte ✅ · profundidad (en curso) · reales ✅ (`reales/`: 1.ª página de los
  3 papers de arXiv + Dario Amodei CC BY 2.0 TechCrunch, `creditos.json`) · escenas.py ✅ (31 tomas q01-q31, revisadas en 3 hojas
  de `_vivo.py hoja`) · SFX ✅ (53 procedurales + 19 propios → `_sfx_propios.py` → audio/fx.wav) · Lyria ✅ (3 tramos, 1.er intento,
  sin huecos) · mezcla ✅ (−14,0 LUFS, voz +12,6 dB) · 🎞 Montaje ✅ (10:40, aviso por voz al usuario) · miniatura Flow ✅
  (`salida/miniatura.jpg` «YA LO HACE», prompt en `prompt_miniatura.md`; la de Gemini en `_gemini/`) · youtube.json ✅ (créditos de reales)
- RENDER EN COLA (10:45): `_render_en_cola.ps1` (proceso aparte, log `previews/_render_en_cola.log`) espera a que acaben el render de
  `frio_extremo` y la voz de `nervio_vago` y hace video → final → verificar → aviso por voz. Si el log no dice «LISTO», relanzar:
  `$env:FAB_ESPERAR=""; powershell -File videos\secreto_ia\_render_en_cola.ps1`
- SIGUIENTE: notas del usuario sobre el Montaje (si hay: editar escenas.py y `video --rehacer t0-t1` + `final`) → rigor del MASTER
  (1 cuadro/3 s + hoja 2×3 + blackdetect) → `yt subir secreto_ia logia private --publicar <hueco de canales --actualizar>`
  (sáb 24-oct 14:00 CDMX) → registrar en `canales/logia.json` («formato»: "expediente noir pegatina flow"), BITACORA, panel
- Mapa de piezas: detective_hoja 00 lee carta/01 sentado en silla (mira dcha.)/02 fuma/03 señala/04 agachado levanta alfombra/05 de
  espaldas · detective_camina 8 (mira dcha.) · ia_hoja 00 sentada (mira dcha.)/01 de pie manos atrás/02 careta sonriente/03 mira
  por encima del hombro/04 escribe en libreta/05 agachada mete algo bajo la alfombra · ia_camina 8 (mira dcha.) · investigadores 00
  mujer portapapeles/01 hombre teclado (dcha.)/02 hombre café/03 mujer señala (dcha.)/04 viejo brazos cruzados/05 joven notas ·
  utileria 00 sobre/01 hoja/02 máquina/03 teléfono/04 lámpara/05 carpeta/06 lupa/07 cámara/08 palanca/09 llave/10 candado/11 careta/
  12 libreta/13 taza/14 cenicero/15 sombrero/16 reloj/17 rack · humo_papel 00-03 humo/04-05 vapor/06-08 hojas volando/09 montón/
  10-11 tinta · polilla_aleteo 6
- Avance: 🎞 Montaje del panel (`python fab.py secreto_ia montaje`) · objetivo: hueco de LogIA sáb 24-oct 14:00 CDMX
- siguiente: **21-oct-2026, el usuario: «está mal hecho, lo hizo un modelo básico y la animación está fea» → veredicto REHACER las escenas** (diagnóstico cuadro a cuadro en docs/estilo_noir.md § «ERRORES A NO REPETIR — secreto_ia»: escenarios vacíos de rectángulos, sin medios reales, IA infantil, fondo repetido 40 s, tomas quietas, texto cortado, música procedural). Guion y voz (David, CER 0) se pueden conservar si el usuario lo aprueba. NO subir. Antes (14-oct): NO PROGRAMAR, lo hizo Gemini y hay que corregir varias cosas → sesión propia: que el usuario diga qué falla (o revisión cada 3 s contra docs/estilo_noir.md) y corregir. Además, cuando Lyria responda: `python _lyria_segmentos.py todo` (en esta carpeta) → `python fab.py secreto_ia mezcla` → `final` (sin re-render). Antes: revisar las dos tomas quietas de abajo y decidir con el usuario.

## Hecho
- Tema con datos (`python fab.py ideas logia`, 08-oct-2026): en el nicho, la IA que engaña o esconde cosas es lo que más rompe la media («¿Puede una IA guardar un secreto?», Homosapiens ×3,3).
- Guion (5 escenas, 25 frases, 3:00): gancho, puerta, interrogatorio, fingir, cierre. Hechos y fuentes en el encabezado de `guion.py`: Anthropic (sleeper agents, ene-2024), Apollo Research (dic-2024), Anthropic + Redwood (alignment faking, dic-2024; 14 % del escenario de prueba).
- Voz: ElevenLabs «David» eleven_v4 con corchetes; 25/25 frases CER 0; 151,5 s de voz; ~250 créditos.
- Escenas con elementos PROPIOS (no reciclados de otros videos): pasillo de servidores con la puerta trasera, sala de interrogatorio con espejo, columna de cristal de la IA con careta, dos cuartos separados, alfombra que se levanta. Del kit solo primitivas (hoja, carpeta, medidor, barra, detective).
- SFX ElevenLabs propios (7 sonidos, 12 golpes): pulso, cerrojo, puerta, alarma suave, estática, cristal, sello de metal.
- Miniatura `salida/miniatura.jpg` (kit noir: columna + careta + rótulo). `youtube.json` (título 33 caracteres, capítulos, fuentes).
- Render completo rehecho tras correcciones (movimiento ambiental en los mundos, barras visibles, toma de la puerta más grande, oscurecimiento final más suave).

## Falta
- [ ] **Música**: Lyria devuelve 403 «Your project has been denied access» en los 14 intentos (cuenta/proyecto, no código). La mezcla usa música procedural de respaldo. Cambiar en cuanto responda Lyria; NO hace falta re-renderizar.
- [ ] **Tomas quietas** (regla: más de ~2 s sin movimiento): «fingir» (la sala con la columna y la careta, ~8–10 s casi igual) y el arranque del cierre (el detective casi quieto ~6 s). Añadir movimiento real (una figura, un objeto que se mueve, cámara con paralaje) y `video --rehacer t0-t1` en esos tramos.
- [ ] Cuadro borroso hacia el cierre (~165 s, transición): revisar a tamaño completo.
- [ ] Visto bueno del usuario; después subir EN PRIVADO y programar (preguntar antes): `python fab.py yt subir secreto_ia logia private`, y anotar `"formato": "expediente de caso real"` en `publicados`.

## Cómo retomar (comandos)
```
python fab.py estado secreto_ia
python fab.py secreto_ia verificar
python fab.py secreto_ia video --rehacer 0-180      (solo si cambió código de escenas; si no, sobra)
python fab.py secreto_ia mezcla
python fab.py secreto_ia final
python _miniatura.py                                (miniatura, sin render)
python _youtube.py                                  (youtube.json)
python _prueba.py <escena> u1 u2 ...                (cuadros a tamaño completo en previews/)
```

## Archivos clave
- `guion.py` (hechos y fuentes en el encabezado), `esc_gancho.py`, `esc_puerta.py`, `esc_interrogatorio.py`, `esc_fingir.py`, `esc_cierre.py`
- `mundos_secreto.py` (mundos y utilería propios: `columna_ia`, `careta`, `espejo_unidireccional`, `camara_vigilancia`, `burbuja`, `alfombra`)
- `_reg.py` (genera `escenas.py`), `_lyria_segmentos.py` (música por tramos, pendiente de Lyria), `fx_audio.py` (SFX propios), `_miniatura.py`, `_youtube.py`

## Lecciones de este video (solo lo no obvio)
- Zoom de cámara con texto: tope ~0,012·u por plano. Con más zoom, `texto_maquina` (encuadrar=True) se desplaza para quedar en pantalla y se sale de la hoja.
- Texto sobre hoja: NO poner `encuadrar=False`; dejar que se ajuste al soporte que declara `K.hoja`.
- El robot de `kit27` se ve de juguete: para la IA se usó `columna_ia` (columna de cristal con núcleo de luz y la careta encima).
- Globos de diálogo: sin luz propia salen grises sobre fondo oscuro; `h.luz_fija(rect, 1.3)` los hace legibles.
- Lyria «denied access» (403) no se arregla desde el código: revisar la cuenta de Google AI Studio.
