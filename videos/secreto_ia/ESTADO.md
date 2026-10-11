# ¿Puede una IA guardar un secreto? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: logia · SIN FECHA (no subido; el usuario decide; hueco sugerido: el siguiente libre según `python fab.py yt videos logia`)
- estilo: noir → doc de estilo: docs/estilo_noir.md · ejemplo a copiar: videos/informante_2027/ (kit) + utilería y mundos propios de este video (mundos_secreto.py)
- etapa: MASTER HECHO y verificado (180 s, 1920x1080, −14 LUFS, CER 0, sin desfase) · música = RESPALDO PROCEDURAL (Lyria 403) · NO SUBIDO
- siguiente: cuando Lyria responda: `python _lyria_segmentos.py todo` (en esta carpeta) → `python fab.py secreto_ia mezcla` → `final` (sin re-render). Antes: revisar las dos tomas quietas de abajo y decidir con el usuario.

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
