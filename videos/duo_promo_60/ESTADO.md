# Dúo · Misiones en pareja — lo nuevo (anuncio 60 s) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: sin canal (anuncio de la app del usuario, E:\CalendarioPareja v24; App Store y Google Play) · sin fecha
- estilo: anuncio de app (UI de Dúo dibujada por código) → doc: docs/estilo_app_promo.md · ejemplo: videos/duo_promo/ (kit `duo.py` copiado)
- etapa: verificado (MASTER entregado 21-oct, espera revisión del usuario)
- siguiente: cambios que pida el usuario (`video --rehacer t0-t1` + `final`); al aprobar: `python fab.py duo_promo_60 limpiar`

## Sesiones (plan de tramos · «continúa el video duo 60» retoma aquí · protocolo docs/sesiones.md)
- alias: duo 60, anuncio nuevo de Dúo, comercial de 60 s de la app de pareja
- es el PRIMER comercial (duo_promo fue solo prueba, 21-oct): no dar por hecho que conocen Dúo
- decisiones del usuario (21-oct): vertical 9:16 · Lina (ella) + Eric (él) en diálogo · las 4 funciones nuevas (misiones a la medida
  + distancia, juegos, Nuestro hogar + huerto, ciclo/guía/embarazo) · cierre logo + «Descarga Dúo» + insignias App Store/Google Play, sin URL
- vista previa: borradores por escena en el 🎞 Montaje del panel (`fab.py duo_promo_60 montaje`), no la vista previa
- leer al empezar: este ESTADO.md, cabecera de guion.py, docs/estilo_app_promo.md; capturas reales en E:\CalendarioPareja\guia\*.webp
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion | ✅ 21-oct | 6 escenas; gancho reescrito como presentación (primer comercial); aprobado |
| 2 | voz, tiempo, componentes nuevos del kit, escenas, montaje | ✅ 21-oct | voz 54,4 s CER 0 (320 cr, cuenta 2); tiempo 60,0 s; 6 escenas revisadas en hojas (previews/h_*.jpg); montaje 109 s |
| 3 | fx, SFX, Lyria, mezcla, render, final, verificar | ✅ 21-oct | 104 SFX (499 cr); Lyria cand. 2; −14,0 LUFS, voz +14,9 dB; render 546 s; CER 0; rigor cada 3 s sin bloqueos |

## Hecho
- audio: fx_audio.py (104 SFX ElevenLabs, cuenta 2), Lyria candidato 2 (el 1 se apagaba antes del cierre), mezcla −14,04 LUFS / −1,19 dBTP
- voz ElevenLabs 14 frases, CER 0, 54,4 s; `medida` post 0.3 (con 0.1 la transición caía antes del fin de la voz); total 60,0 s
- carpeta creada; copiados de duo_promo: duo.py (kit), fuentes/, _hoja.py, ref_lina.mp3, ref_eric.mp3

## Falta
- [ ] visto bueno del usuario al MASTER (y, al salir en tiendas, sobreponer las insignias oficiales de Apple/Google)

## Archivos clave
- `guion.py` (VOZ_POR_FRASE: frases de Eric), `duo.py` (kit: + `interruptor`, `insignia`, pestañas de la v24), `comun.py`, `escenas.py`
- `e_intro.py` gancho · `e_medida.py` misiones a la medida/distancia (+ `home()`) · `e_juegos.py` 5 juegos · `e_hogar.py` casa isométrica + huerto · `e_ciclo.py` ciclo/guía/embarazo + cierre
- prueba: `python _hoja.py 18 20.5 23 --out h` → previews/h.jpg

## Lecciones de este video (solo lo no obvio)
- La v24 tiene 5 pestañas (Misiones · Juegos · Ciclo · Nosotros · 💬): a 14 px no caben en 400 px CSS → 13 px y relleno 11.
- La pareja de la demo de la app es Ana y Beto (capturas de guia/*.webp, en modo claro); el anuncio usa el modo oscuro del kit.
- `ww()` normaliza acentos pero NO la ñ: «acompañarla» se ancla con «acompa».
- Emojis de Fluent que salen como mancha a tamaño grande: 🍽️ y 📹 (usar 📵, o una pill dibujada).
- Isométrico propio (`iso()`/`caja()` en e_hogar.py): a cámara 1 la isla de 10 casillas se ve chica; 1,3 en la casa y 2,3 en el huerto.

## Cierre (regla del 12-oct-2026)
- [x] entregado MASTER + .srt (salida/duo_promo_60_MASTER.mp4, 21,2 MB)
- [x] HALLAZGOS documentados en docs/estilo_app_promo.md § 6; arreglo del núcleo: sfx.py ya no escribe NaN sin eventos
