# Estilo «rayos X tecno» — animación por código + video real (vertical)

_Nació en `videos/mods_ia_fusion/` (7-oct-2026, 112 s, 1080x1920, sin canal). Pedido: «animación pulida, dinámica, adictiva, que combine con videos reales»._

**Idea:** fondo oscuro, neón y estética de interfaz. El video real NUNCA va suelto: vive dentro de una **ventana de programa**. Lo real es «lo que se ve en pantalla»; la animación es «lo que pasa por debajo» (procesos, memoria, datos, código). Sirve para explicar tecnología, software, juegos, IA, internet.

## Archivos a copiar
- `pix.py` — pintor `P` a resolución completa (texto nítido) con `cam` / `grupo` / `pivote` / `clip`; formas (`poly`, `rect`, `rrect`, `elip`, `circ`, `polilinea`, `glow`, `texto`, `imagen`); `fondo_tecno` (nebulosas, rejilla, motas en 3 planos); `acabado` (bloom global, aberración cromática, barrido, viñeta, `golpe` = temblor, `glitch`, `flash`); `Clip.cuadro(nombre, seg)` (extractos de `clips/*.mp4`); anclas por PALABRA `ww(escena, frase, "palabra")`, `INI`, `FIN`.
- `comp.py` — `slam` (rótulo de golpe), `chip` (cápsula con icono), `tecleo`, iconos, `ventana` (marco de proceso; `fantasma=` = proceso oculto), `clip_en`, `mundo_bloques` + `figura_bloques` (diorama isométrico ORIGINAL), `memoria`, `paquete`, `pista`.
- `escenas.py` — una sola clase `Mundo(Escena)` cuyo `render` devuelve `cuadro(t)`; `guion.TRANSICIONES = [("continua", 0.5)] * n` para que el núcleo no meta sus transiciones.
- `fx_audio.py` — SFX de ElevenLabs para videos por código: `SFX` (prompt + segundos) y `PISTAS` (sonido, segundo, volumen) con las MISMAS anclas que la animación → `audio/fx.wav`.
- `_hoja.py` — `python _hoja.py 1.2 3.4 10:20:2 [-f] --out nombre` → hoja de cuadros en `previews/` (`-f` = tamaño completo).

## Reglas del estilo
- **Plano secuencia:** una pieza de una escena sigue viva en la siguiente (la ventana del gancho es la ventana de «Skyrim» del diagrama). Cambios de sección con glitch, destello o cámara que atraviesa un objeto; nunca corte seco.
- **Cada frase, un dibujo que la explica** y entra en su palabra (`pop`/`slam` + `golpe` de cámara + SFX). Nada quieto más de ~2 s: el fondo, los indicadores y los datos siempre se mueven.
- **Zona segura de Shorts:** lo importante entre y≈170 y y≈1640; nada clave en x>940 de la mitad inferior (iconos) ni bajo y≈1650 (título).
- **Video real:** extractos cortos con `yt-dlp` (≤720p) en `clips/`, siempre dentro de una ventana, con «GAMEPLAY REAL» y crédito del autor en pantalla; avisar al usuario del riesgo de derechos. Elegir el tramo con una hoja de contacto de ffmpeg antes de usarlo.
- **Personajes y mundos de franquicias: no se dibujan.** Se usan diseños originales (el explorador-robot de bloques, el investigador) y, para lo real, el extracto de video.
- Colores con significado fijo durante todo el video (aquí: lila = juego A, verde = juego B, amarillo = memoria, cian/magenta = leer/escribir, rojo = límite o aviso).

## Flujo y cifras
`guion.py` (FORMATO="vertical", GAP=0.16, VOZ ElevenLabs) → `voz` → `seleccionar` → `tiempo` → escenas con `_hoja.py` → `python fx_audio.py` → Lyria (`LYRIA` en guion; ver CLAUDE.md «Arranque rápido») → `mezcla` → `video` → `final` → `verificar`.
- Un cuadro tarda 0,5–1,1 s (lo más caro: muchos textos pequeños, p. ej. la lluvia de bytes).
- Mezcla: con `MEZCLA = dict(musica=-24, sfx=-24, fx=-17)` la voz queda ~11 dB sobre el fondo; con `fx=-7` los efectos la tapaban (2,3 dB).
- Coste de ElevenLabs en este video: voz ~700 créditos, 12 efectos ~200.
