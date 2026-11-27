# fo_shorts — Shorts de arranque de Radio Yermo recortados de los largos — ESTADO
<!-- Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: radio_yermo · 3 Shorts verticales (#Shorts, no cuentan para el hueco) · carpetas `videos/fo_short_gary|ruzka|cura81/`
- estilo: recorte de un puesto del MASTER largo, 1080x1920: fondo = el mismo video desenfocado, gancho Pip-Boy arriba, 16:9 en medio, «video completo» abajo; sin voz nueva, sin subtítulos quemados
- etapa: ✅ SUBIDOS y PROGRAMADOS 26-nov: Gary Mim1FgNOLcI (vie 27-nov 19:00 CDMX) · Ruzka dBmlWMwYNwg (lun 30-nov 19:00) · cura81 pnqZ8Sd5itk (jue 3-dic 19:00)
- siguiente: al salir cada uno PÚBLICO → Studio «Vídeo relacionado» = su largo (Gary → XU_OkLlxV7o · Ruzka → f2zKynItV6U · cura81 → z_YrsxSbIFg); medir a 48 h impresiones/vistas del Short y si mueven al largo (fuente «Shorts»)

## Por qué (26-nov-2026)
- Radio Yermo: 63 impresiones en 28 días con CTR 6,4 % → YouTube no lo muestra (sin semilla). En español el público de Fallout vive en Shorts («Crónicas del Yermo», 57 mil subs, solo Shorts). El usuario aprobó 2-3 Shorts de arranque.

## Cómo está armado
- `hacer.py [gary|ruzka|cura81]`: tramos en `SHORTS` (t0/t1 del largo), capa PNG (bahnschrift + consolab, verde de `mg_fo`), ffmpeg (split → fondo desenfocado + 16:9 + capa), .srt recortado y `youtube.json` en cada carpeta.
- Arranque SIN «Número X»: cortado en el silencio tras el número (silencedetect sobre `voz/final/<frase>.wav`), porque el primer segundo del puesto aún trae la cola visual del puesto anterior (transición). Comprobado con Whisper: arrancan en «Refugio 108», «Ruzka», «Quedarte la cura».
- −14 LUFS (hereda la mezcla del MASTER). Separación Short-Short = la del canal (72 h); Short-largo 12 h.

## Lecciones
- Al recortar un puesto de una Secuencia YT, los primeros ~1,5-2 s son la transición desde el puesto anterior (otro juego/tema): empezar después del número o mirar el cuadro 0.
- Consolas no trae «▶»: dibujar el triángulo.
