# El llamado del Mixtón — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Bitácora Perdida (`bitacora_perdida`; el usuario lo eligió el 21-oct tras verlo) · 18:00, 16:9
- estilo: pegatina_flow CINEMATOGRÁFICO → docs/estilo_pegatina_flow.md (§8b = hallazgos de este video) · ejemplos: videos/la_sena/, videos/jalpa/
- etapa: SUBIDO y PROGRAMADO ✅ https://youtu.be/H3B9BIiN33E · privado → público jue 29-oct-2026 14:00 CDMX (2026-10-29T20:00:00Z) · miniatura Flow «MAÑANA SUBEN» (`salida/caxcan_mixton_mini_flowA.jpg`; respaldo «SOY CAXCÁN» flowB) · .srt · 17 capítulos
- siguiente: tras publicarse, ver métricas (retención de un video de 18 min en un canal de ~3-8 min) · `fab.py caxcan_mixton limpiar` cuando ya no haya arreglos (libera 4 GB de segmentos en E:)

## Sesiones (plan de tramos · «continúa el video caxcan_mixton» retoma aquí · protocolo docs/sesiones.md)
- alias: caxcan_mixton, la novela del Mixtón, el padre caxcán, el llamado del Mixtón
- vista previa: SÍ, el acto I (0-222 s) con audio completo → visto bueno del usuario el 21-oct («continúa; el viento muy fuerte»)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en 1 sesión (pedido del usuario): guion + voz + Flow + recorte + escenas + audio + vista previa acto I + resto + render | ✅ 21-oct | 155 tomas, 18:00; viento procedural → ambientes grabados; 17 SFX ElevenLabs; 2K de hojas por otra sesión |
| 2 | Revisión del usuario → canal y publicación → miniatura | ✅ 21-oct | Bitácora Perdida; `youtube.json` (título 43 car., 20 etiquetas, fuentes con DOI); miniatura Flow (ojo: el chip había quedado en 9:16 → comprobar 16:9 antes de enviar) |

## Hecho (21-oct-2026)
- Voz: 154 frases ElevenLabs (20 voces, `eleven_v4`), seleccionar con CER/GAP/TAIL_MAX_POR_FRASE (Whisper oye mal los nombres).
- Flow: 89 prompts x2 = 178 imágenes 1K (navegador integrado, 0 errores) · hojas 2K en `hd/` (sesión aparte con Claude in Chrome).
  `_repartir.py` (orden ALFABÉTICO de clave), `_elegir.py` (11 hojas a la variante b), `_marcos.py`. Profundidad de los 96 escenarios.
- Recorte: 43 hojas (+ `c09_zopilote_aleteo`, `c11_tameme_camina`). `h18_ollin_viejo` en 2K: 00 sentado · 01 fogata · 02 de espaldas · 03 de pie con la piedra · 04 camina.
- escenas.py: 155 tomas (prólogo AP/NO, I AN/RI/FI/TE/NT, II LL/CH/HI/EN/CE, III DI/TL/LM/DE, IV PE/VI/CO/AL/GU/HE, V VR/CR/UL/CA,
  epílogo EP/VA/FN/CI), AST 0 repetidos, cada acto revisado con `_vivo.py hoja` (`_muestras.py t0 t1`, `_tiempos.py`, `_plan_actos.md`).
- Música: Lyria 19 tramos (≤ 69 s) → `audio/musica.wav`. Catalogada en la biblioteca (no repetir ante el mismo público).
- Sonido: ambientes grabados en bucle (`escenas.AMB` + `_fx_eventos.AMB2`) y 47 golpes (`_fx_eventos.UNA`); 17 SFX nuevos de
  ElevenLabs (`_sfx_eleven.py`, 1.000 créditos de la cuenta 3) + 3 de la biblioteca; 46 procedurales duplicados quitados.
  Mezcla −14,3 LUFS, −1,05 dBTP, voz 9,9 dB sobre el fondo. SFX catalogados.
- Render: 360 segmentos (~1 h 50 min con 12 procesos tras archivar 19 sesiones inactivas) · rigor del MASTER: un cuadro cada 3 s
  (`previews/_master_0N.jpg`), blackdetect (solo el fundido final 0,47 s) y freezedetect (nada quieto > 2 s). Dos planos sin
  personajes (Mixtón de hoy 1038-1044 s y plaza del cierre) → antepasados translúcidos → `conservar` + `video --rehacer` (9 segmentos).
- `verificar`: CER medio 0,0038; los 8 avisos son variantes de nombres (Olin, Kashkán, Nochislán, Itlalí).

## Para rehacer el AUDIO sin re-renderizar
`python videos/caxcan_mixton/_sfx_filtrado.py` → `python videos/caxcan_mixton/_fx_ambiente.py` → `fab.py caxcan_mixton mezcla` →
`fab.py caxcan_mixton final` (solo une `video_sin_audio` + `audio/final.wav`). NO usar `fab.py … sfx` (mete los procedurales quitados).

## Para arreglar un tramo de IMAGEN
Editar escenas.py → `cache_escenas.conservar(car, [segmentos buenos], firma_codigo(car, nucleo))` → `fab.py caxcan_mixton video
--rehacer t0-t1 …` → `final`. Segmentos de 3 s (k = t // 3). E: queda justo (~7 GB): el `final` necesita ~4,2 GB libres.

## Lecciones de este video (solo lo no obvio; el resto en docs/estilo_pegatina_flow.md §8b)
- Comandos de bash > 8 KB fallan en Windows también por la herramienta Bash: escribir con Write/Edit.
- Dos sesiones sobre el mismo video (una por Remote Control): se detectó por la cola de voz («espero mi turno») y cambios en
  guion.py a mitad de lectura. Antes de producir, `list_sessions` y mtimes del video.
- Con ~57 procesos de Claude abiertos (21 GB comprometidos) la memoria virtual baja a < 1 GB y el render cae a 3-6 procesos;
  archivar sesiones inactivas (con permiso del usuario) lo devolvió a 12.
- `final` con E: lleno falla con código −28 (ENOSPC) y deja `MASTER.mp4.tmp.mp4` a medias: borrar el temporal y el MASTER viejo antes.
- El log de `_render_todo.ps1` sale mezclado UTF-8/UTF-16: leerlo con `(Get-Content … -Raw) -replace "`0", ''`.
