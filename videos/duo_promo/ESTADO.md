# Dúo · Misiones en pareja (anuncio 45 s) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: sin canal (anuncio de la app del usuario, E:\CalendarioPareja; saldrá en App Store y Google Play) · sin fecha
- estilo: el de la app Dúo (modo oscuro, manchas coral/violeta, tarjetas, degradado, Plus Jakarta Sans), dibujado por código → kit `duo.py` · ejemplo de motor: videos/mods_ia_fusion/
- etapa: verificado (MASTER entregado 13-oct, espera revisión del usuario)
- siguiente: cambios que pida el usuario (`video --rehacer t0-t1` + `final`); al aprobar: `python fab.py duo_promo limpiar`

## Sesiones (plan de tramos · «continúa el video duo» retoma aquí · protocolo docs/sesiones.md)
- alias: duo, anuncio de Dúo, video de la app de pareja
- vista previa: el usuario eligió «completo directo» (13-oct): MASTER completo en una sesión, sin preview parcial
- decisiones del usuario (13-oct): vertical 9:16 · voces Lina (ella) + Eric (él) en diálogo · cierre logo + «Descarga Dúo» + insignias App Store/Google Play
  (a media sesión pidió QUITAR el URL clicknbusiness: es provisional, la app será de tiendas)
- leer al empezar: este ESTADO.md y la cabecera de guion.py
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion, voz, tiempo, kit, escenas, fx, Lyria, mezcla, render, final | ✅ 13-oct | MASTER 46,6 s, CER 0, −14 LUFS; revisado cada 3 s y corregido |

## Hecho
- guion 12 frases (Eric = VOZ_POR_FRASE), voz 41,6 s, CER 0; total 46,6 s (BPM 480 = cuantización a 0,5 s)
- ElevenLabs: voz ~295 cr + SFX 257 cr; Lyria candidato 2 (energía sube justo en la barra)

## Falta
- [ ] visto bueno del usuario (y, si sale en tiendas, insignias oficiales de Apple/Google sobrepuestas)

## Archivos clave
- `guion.py` (VOZ_POR_FRASE: frases de Eric), `duo.py` (kit), `escenas.py`, `fx_audio.py`, `_hoja.py`, `fuentes/`

## Lecciones de este video (solo lo no obvio)
- PIL 12 pinta emojis de color con `C:/Windows/Fonts/seguiemj.ttf` y `embedded_color=True` (tamaño 109 nativo); 📲 y 💪 se ven raros.
- Con Lyria, `BPM = 480` cuantiza las escenas a 0,5 s: 56 s → 46,6 s sin tocar la voz.
- `_esquinas` del teléfono: el barrido debe ser de 90° (el primero barría 270° y tapaba la barra de estado).
- Revisión del MASTER: «Faltan 0 XP» un instante antes de llenarse y «quedan 5 días» fijo → umbral 449,5 y días según `hoy`.

## Cierre (regla del 12-oct-2026)
- [x] entregado MASTER + .srt (salida/duo_promo_MASTER.mp4)
- [x] HALLAZGOS documentados: docs/estilo_app_promo.md (nuevo), CLAUDE.md «Otros estilos», galeria.json
