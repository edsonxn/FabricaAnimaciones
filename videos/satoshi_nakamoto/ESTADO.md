# ¿Quién es Satoshi Nakamoto? (documental serio, ~14 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: edsonxn · PUBLICADO (público) 6-oct-2026 ~08:48 CDMX (amA4bPr0aAY)
- estilo: documental → docs/estilo_documental.md (§ «Tablero de detective vivo») · ejemplo: videos/christa_pike/ + kit nuevo tablero.py · voz Faraon · Lyria · SIN subtítulos
- etapa: publicado (verificado en YouTube 6-oct-2026) · MASTER 14:45, CER 0,14 %, .srt, miniatura Flow A2
- siguiente: ver retención a las 48 h. Al aprobar: `python fab.py satoshi_nakamoto limpiar`

## Hecho
- Guion final: 16 escenas, 130 frases, 2.138 palabras (Faraon lee ~2,9 palabras/s → ~13:45). Hechos con fuente en el docstring de `guion.py` y texto en `fuentes/*.txt`.
- Datos REALES propios: `datos/forum_posts.json` (543 mensajes de Satoshi, Nakamoto Institute) → `datos/horas_utc.json` (solo 7 entre 5 y 12 UTC);
  código de Bitcoin v0.1 (`datos/v01_main.cpp`, MIT; línea 1456 = titular de The Times); hex del bloque génesis y firma del bloque 170 verificados en blockstream.info.
- 26 fotos de Commons con licencia en `imagenes/creditos.json`. OJO: «peter_todd.jpg» NO es el Peter Todd de Bitcoin (es el de HEC París): no usar. Craig Wright, Dorian y Todd: tarjeta de silueta «SIN FOTO LIBRE».
- KIT NUEVO `tablero.py`: corcho infinito + cámara 3D que nunca se para (Hermite, látigos con desenfoque, inclinación), `Pieza` (cae y se clava, portal),
  `Hilo` (catenaria, vaivén, corte), `Marca` (rotulador), `Punteada` (paquetes de datos), `Cinta`, `Lupa` (aumento real), `Linterna`, sellos, relleno de fondo.
  Fábricas en `piezas.py`/`piezas2.py`; 30 escenas dibujadas dentro de polaroids en `portales.py` (`_hoja_portal.py` para probarlas).
- Coreografía anclada a palabras: `coreo_a.py` (origen→perfil), `coreo_b.py` (Dorian→cierre), `coreo_c.py` (Le Roux, archivo, espejo, gancho a oscuras con linterna).
- Núcleo: `qa.normaliza` ahora convierte «1.100.000» y millones (antes `num_es` devolvía cifras).

## Falta
- [x] voz, tiempo, revisión de encuadres con la voz real (hojas a..e corregidas), Lyria (5 tramos, 1.er intento), sfx (366 eventos), mezcla, youtube.json (`hacer_youtube.py`)
- [ ] render → final → verificar → revisar MASTER (un cuadro cada ~3 s) → miniatura IA (`prompt_miniatura.md`) → subir privado
- [x] Docs: § «Tablero de detective VIVO» en docs/estilo_documental.md y fila de Edsonxn en CLAUDE.md

## Cómo retomar (comandos)
```
python fab.py estado satoshi_nakamoto
cd videos/satoshi_nakamoto ; $env:PYTHONPATH="C:\FabricaAnimaciones\videos\satoshi_nakamoto;C:\FabricaAnimaciones\nucleo"
python _hoja_rec.py a        (a..e: hoja de cuadros del recorrido -> previews/rec_a.jpg)
python _hoja_portal.py tribunal:0.3,1 carrera:2   (portales sueltos)
python _demo_tablero.py      (demo mínima del kit)
```

## Archivos clave
- `guion.py`, `kit.py` (anclas + textos del estilo), `tablero.py`, `piezas.py`, `piezas2.py`, `portales.py`, `coreo_*.py`, `escenas.py` (solo Mundo), `_ronda.py`, `_lyria_segmentos.py`

## Lecciones de este video (solo lo no obvio)
- Faraon fue más rápido que en Christa (2,9 vs 2,37 palabras/s): medir con la 1.ª ronda antes de dar la duración; se añadieron 3 escenas NUEVAS al final de bloques (no se desplazan claves).
- `pk(esc, fr, a, b, nth, nthb)`: el 4.º argumento es el nth de `a`; para la 2.ª aparición de `b` hay que pasar nthb. «di» casa con «día»: usar palabras únicas.
- La fuente Special Elite no tiene «→»: escribir con palabras. Los comandos > ~8 KB fallan en este Windows: escribir módulos con Write.
- Render: ~1,1 s/cuadro. Las láminas se guardan en 8 bits (`tablero.Lam`): con float32 cada proceso usaba 2,9 GB (470 papeles de fondo) y el render se quedó sin memoria; ahora ~1 GB.
- Memoria de compromiso de Windows casi llena (C: lleno, el archivo de paginación no crece): con 8 procesos falló, con 5 va. Cerrar Applio/app.py antes de voz/Whisper (vuelven a abrirse).
- Disco: MASTER de Christa a CRF 18 = 49 Mbps; aquí `FAB_CRF=21` (núcleo) para que quepa.
- El 1.er render se «colgó»: el PC se SUSPENDIÓ (00:34→08:08). `_render_despierto.py` pide a Windows no suspender mientras dura.
- Barrido `_barrido.py 3` (un cuadro cada 3 s, ~7 min): encontró nombres fonéticos en pantalla («DÓRIAN», «BAK» → `kit.REAL`), textos sobre caras, piezas encimadas y que faltaban créditos.
