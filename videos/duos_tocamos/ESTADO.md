# Los Duos — «Así tocamos» (sin narrador) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: ninguno (cliente: grupo musical Los Duos) · para mandar por WhatsApp/Facebook a quien pida videos de cómo tocan
- estilo: mismo kit del anuncio `videos/duos_promo/` (pix.py + duos.py copiados): videos reales + marca negro/dorado → docs/estilo_app_promo.md § 7
- etapa: CERRADO — aprobado por el usuario el 22-oct-2026; segmentos limpiados; commit 1f9eaca
- siguiente: nada (entregables en salida/: MASTER + WHATSAPP)

## Sesiones («continúa el video duos_tocamos» retoma aquí)
- alias: así tocamos, video sin narrador de Los Duos, duos_tocamos
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion sin voz, clips, medley, cortes al pulso, escenas, SFX, mezcla, render (7 min), final, verificar | ✅ 22-oct | MASTER 2:01 242 MB + WHATSAPP 24 MB; rigor: se cambió la última toma de la balada (bocina y pared vacías) |

## Decisiones (el usuario, 22-oct-2026)
- SIN narrador: secuencia de sus videos con VARIAS de sus canciones; mismos elementos del anuncio
- 2:01 vertical (`SIN_VOZ`, `BPM = 480` → compás de 0,5 s): intro 3,5 s · 4 canciones de 26-28,5 s · cierre 8 s
- Canciones (frases ubicadas con Whisper; stems en duos_promo/audio/stems): La indita (A1 desde 27,3 «Chiquita y bonita…» +
  «Yo le di mi amor…») · Mis ojos me denuncian (A4 desde 27,5) · balada «Es tu amor» (A2 desde 89,6) · corrido de Teodora (A3 desde 17,0)
- Rótulos de canción = la primera frase cantada (no se sabe el título oficial); «EN VIVO · n DE 4»; cierre con WhatsApp, $1,200 por hora y Aguascalientes

## Archivos
- `guion.py` (CANCION, ESCENAS por compases) · `prep_clips.py` (los 4 videos enteros a 1080x1920 en clips/, E:)
- `musica_medley.py` → audio/musica.wav · `plan_cortes.py` → cortes.json (pulsos y cortes cada 6-8 pulsos) · `sfx_tocamos.py` → audio/fx.wav
- `escenas.py` (TOMAS por canción: (video, segundo)) · kit `duos.py` (ecualizador con rango propio por banda)

## Lecciones (solo lo no obvio)
- Ecualizador sobre canciones completas (muy comprimidas): normalizar cada banda entre sus percentiles 8 y 99, no con un umbral fijo.
- Anton no trae «»: los títulos van sin comillas, con notas dibujadas a los lados.
