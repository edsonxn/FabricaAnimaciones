# T1 vs KOI: las mejores jugadas analizadas (Worlds 2026, ~16 min) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Crónicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; subida por Studio en el navegador, NO está en la API) · publicar HOY mié 28-oct-2026 20:00 CDMX (pedido del usuario, aunque IG-LYON salió hoy 10:00)
- estilo: análisis táctico como `cfo_kc_worlds` (secuencia_yt + VOD + telestrador `mg_tactica` + `mg_lol` + mesas/capas 3D) → doc: docs/estilo_analisis_tactico.md
- etapa: ✅ SUBIDO por Studio y PROGRAMADO mié 28-oct-2026 20:00 CDMX · https://youtu.be/HsS0c8clYUs (MASTER 15:27, 833 MB) con miniatura «LA PELEA CLAVE», 14 etiquetas, «no para niños», IA «No», anuncios + mid-roll, idoneidad «Nada de lo anterior», .srt español PUBLICADO
- siguiente: al aprobarlo el usuario: `python fab.py t1_koi_worlds limpiar` (la música es de la biblioteca: no hay nada que catalogar)

## Sesiones (plan de tramos · «continúa el video t1_koi_worlds» retoma aquí · protocolo docs/sesiones.md)
- alias: T1 vs KOI, T1 KOI, análisis de T1, partido de T1 de hoy
- vista previa: NO (el usuario, 28-oct: «directo al MASTER»); todo seguido en una sesión (plan MAX)
- leer al empezar: este ESTADO, docs/estilo_analisis_tactico.md (§ «Errores corregidos» 28-oct), guion.py (docstring = datos)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + jugadas + render + subida (todo hoy) | ✅ 28-oct | 16:00 → 17:40: MASTER 15:27 y subida https://youtu.be/HsS0c8clYUs programada 20:00 CDMX |

## Decisiones (el usuario, 28-oct-2026)
- «video del partido de hoy de las 2 pm de T1, 16 minutos analizando las mejores jugadas». T1 2-0 MKOI (Bo3, ronda 4) → T1 a cuartos.
- todo seguido hoy; sin vista previa; publicar hoy ~20:00 hora de México.
- SIN SPOILER (el usuario, 28-oct): ni miniatura ni título ni gancho dicen quién ganó; el resultado se descubre partida a partida.

## En curso (checkpoint 28-oct ~17:15)
- ✅ MASTER salida/t1_koi_worlds_MASTER.mp4 (15:27, 833,5 MB, −14,61 LUFS, voz +10 dB, desfase 0 ms; CER alto solo en nombres),
  hoja previews/final_hoja.jpg sin bloqueos. Avisado por voz. Studio abierto en el diálogo de subida: falta que el usuario elija el archivo.

## Checkpoint (17:00)
- ✅ voz 79/79 (umbrales por nombres: investigacion/umbrales.py), tiempo 926,73 s (15:27), beats 108, busquedas (hacer_busquedas.py)
  y bajar 108/108 (101-107 rehechos: apuntaban más allá del fin del VOD; gancho 1-3 rehechos sin spoiler).
- ✅ Música: Lyria dio 429 «monthly spending cap» → biblioteca (lol_worlds_2026 tramos 1,5,4,3,7,8 + ig_lyon tramo 3). AVISAR.
- ✅ efectos.py (281 FX, 218 sonidos), 4 capas 3D (j2a, j4a, j4b, j6a) renderizadas, revisado en previews/rev_a..e.jpg.
- ▶ render_par.py lanzado (6 tramos → %TEMP%/t1_koi_par → salida/video_sin_audio.mp4). Después: `python videos/t1_koi_worlds/vivos_audio.py`
  (DESPUÉS de video: escribe audio/ambiente.wav con la narración original) → `fab.py t1_koi_worlds mezcla` → `final` → `verificar`.

- Subida: como IG-LYON/CFO-KC: Studio del canal en el navegador integrado (studio.youtube.com/channel/UCXU8DV4QJ24yhwXmrR_eLhw/videos/upload),
  el USUARIO pulsa «Seleccionar archivos» y elige salida/t1_koi_worlds_MASTER.mp4; el resto lo rellena Claude con youtube_texto.md
  (descripción con execCommand('insertText'); Escape en etiquetas cierra el diálogo). Programar 28-oct 20:00 CDMX.

## Checkpoint (16:40)
- ✅ datos_g1.md / datos_g2.md (agentes): VOD en ESPAÑOL (LoL Esports Latinoamérica). g1: VOD = HUD + 426; g2: VOD = HUD + 376,1.
  Fuentes medios/_fuente/g1_j1..j5 y g2_j1..j3 (HUD = t + K en la tabla de cada datos_g*.md); narración en g*_narr.txt.
- ✅ guion completo (76 frases, ~1 700 palabras, ~15:40 estimado); miniatura SIN spoiler miniatura/elegida.jpg («LA PELEA CLAVE»).
- ▶ `voz` lanzada 16:40 (voz.log). Luego: seleccionar → tiempo → beats → hacer_busquedas → bajar → efectos jugadas.
- Mapa jugada → fuente: jugada1 = g1_j1 (1.ª sangre) + g1_j2 (doble Elyoya, vivo) · jugada2 = g1_j3 · jugada3 = g1_j4 ·
  jugada4 = g1_j5 · jugada5 = g2_j1 · jugada6 = g2_j2 (t73-100 repetición sin HUD) · jugada7 = g2_j3.

## Checkpoint anterior (16:20)
- Video creado (`nuevo --yt`); recursos.py (logos, fotos de T1 y MKOI — slug API de MKOI = «mad-lions» —, arte Data Dragon 16.21.1).
- Copiados de cfo_kc_worlds: ver.py, rejilla2.py, render_par.py, mesas_3d.py, hacer_busquedas.py, escenas.py, tiempos_mesas.py.
- investigacion/muertes.txt (feed oficial de las 2 partidas). VOD: g1 rTVyiDIg-n8 (47:17), g2 irsYoLi62_U (32:36).

## Lecciones de este video (solo lo no obvio)
- En la API de LoL Esports, Movistar KOI sigue con el slug «mad-lions» (código MKOI); «movistar-koi» devuelve otra plantilla.
- Lyria: HTTP 429 «monthly spending cap» el 28-oct → música de la biblioteca (lol_worlds_2026 + ig_lyon). Avisado al usuario.
- Los apoyos de `busquedas` no pueden pasar del final del VOD (G1 = 2837 s, G2 = 1956 s): yt-dlp deja un mp4 de 261 bytes sin error.
- Tramos EN VIVO: video con FX `video` de la fuente local y audio con vivos_audio.py → audio/ambiente.wav (48 kHz; DESPUÉS de `video`, que lo borra).
- Studio en el navegador integrado sin cuadros de Windows: miniatura = fetch de la URL de Flow + canvas 1280×720 + DataTransfer en
  input#file-loader; .srt = interceptar HTMLInputElement.prototype.click (captura el input) + File desde base64. Al pasar el base64 a
  mano se coló una errata (una línea con «/�¦»): comprobar SIEMPRE con suma de control por línea contra el .srt local.

## Cierre (regla del 12-oct-2026)
- [ ] subido por Studio y PROGRAMADO 28-oct 20:00, miniatura, .srt, monetización
- [ ] HALLAZGOS documentados en docs/estilo_analisis_tactico.md
