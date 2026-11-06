# ¿Qué pasó con los DWEMER? Los 20 secretos de su desaparición que Skyrim esconde — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_tamriel · meta: hueco tras el 14-nov-2026 (canales --actualizar del 4-nov: Tamriel BIEN, 3 programados)
- estilo: secuencia_yt (gameplay Skyrim/ESO/Morrowind por beat + MG `nucleo/mg_tes.py` + pegatinas + mapas tema `tes`) · SIETE voces ElevenLabs que compiten (fórmula de `tes_sentinel_teaser`) + el Humano tras el Telón · OST oficial → doc: docs/estilo_secuencia_yt.md § Tamriel + § REGLA DE ORO
- etapa: SUBIDO privado https://youtu.be/b0iLKv6r2Tw · programado dom 15-nov 12:08 (2026-11-15T18:08:00Z; el 14 chocaba con la separación de 96 h)
- siguiente: revisión del usuario · Studio: monetización + video relacionado de Shorts · biblioteca catalogar · medir a 7 días (campaña de subs)

## Sesiones (plan de tramos · «continúa el video tes_dwemer_desaparicion» retoma aquí · protocolo docs/sesiones.md)
- alias: dwemer, desaparición de los dwemer, enanos · vista previa: ninguna (el usuario se fue: «terminalo hasta master»)
- leer al empezar: docs/estilo_secuencia_yt.md § REGLA DE ORO y § Crónicas de Tamriel; docs/voz.md § VARIAS VOCES; videos/tes_sentinel_teaser/ (guion.py, efectos.py, _bordes.py, _remapear.py)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | TODO en una sesión (el usuario, 4-nov): UESP + guion + voz + beats + clips + pegatinas + MG + mapas + OST + mezcla + render MASTER | ✅ 4-nov | s3 (4-nov noche): MASTER 27:43 + subido y programado 15-nov ·: voz arreglada 27:24, efectos, música, clips en curso; cortada por contexto · s1 cortada al lanzar la investigación; s2 (4-nov noche): investigación, guion, voz, pegatinas, mapas, OST, efectos.py; cortada por contexto con la voz en 18:00 |

## Decisiones del episodio (4-nov-2026, el usuario)
- **24 minutos** · **varias voces como el último** («a la gente le gustó») · tema lo elige Claude · 1 sesión · hasta MASTER (sin revisión previa).
- Tema: los Dwemer (lo pidió @chuymoreno6820 en Sentinel; @EnriqueJVidal-ei1nk elogia Arniel y la Forja del Aeterio; lore largo rompe la media fuera: Qewvr ×7).
- Votos reales en Sentinel (4-nov, 33 comentarios): el Profeta 4 · MariCarmen 2 · Hope 2 · Johnny 2 · Edoardo, José y Mario 0 → «ronda 2»: los de 0 votos se juegan el puesto.
- Comentarios: QUEJA justa ♥7 «Oblivión con acento agudo» (+ «jarl» pronunciado como se escribe) → FONETICA y decirlo en el video. Agradecimientos: Miguel_Salvatierra, MelVal54, ShadowPriestBear, MoonrakerYo79, minecrafttv2081. Críticas con burla: «Que ridícula la voz femenina» (GalinaVenegas), «se nota que kyrim no es lo tuyo» (jhonfeddiszabalamoreno9056) — comprobar ≤ 10 días.
- Campaña de suscripción ~75 % (cifra de `yt metricas`, meta 10 000).

## En curso (checkpoint s3, 4-nov ~20:25, corte por contexto)
- HECHO s3: voz 181/181 (27:24) · beats 191 · busquedas.json (`_busquedas.py`) · efectos.py corregido + relleno (299 FX, 4 huecos chicos) · sfx/ del juego · audio/musica.wav (OST, 17 secciones) · pegatinas extra.
- ~23:40 MASTER HECHO (salida/tes_dwemer_desaparicion_MASTER.mp4, 27:43, 1,6 GB) + verificar OK + final_hoja revisada → `yt subir … --publicar 2026-11-14T18:08:00Z` LANZADO (log _subir.log). Falta: registrar id en canales/cronicas_tamriel.json + BITACORA, avisar (tele), cerrar sesión en ESTADO, `biblioteca`/lecciones, commit.
- youtube.json HECHO (`_youtube.py`, 4 846 bytes) · hueco = 2026-11-14T18:08:00Z (sáb 12:08 local) → `yt subir tes_dwemer_desaparicion cronicas_tamriel private --publicar 2026-11-14T18:08:00Z`.
- ~22:30: _bordes 0 encimados (`_desencimar.py` → _ajustes.json, aplicado al final de efectos.py; firmas de cadena/receta/ruleta arregladas), fx hoja revisada → `video` LANZADO (log _video.log) → luego `final`, `verificar`, subir.
- ~21:30: clips 191/191 REVISADOS y limpios (39 rehechos; 10 por --url de videos buenos) · ambiente/sfx/mezcla HECHOS (-14,1 LUFS) · chequeo: +23 fichas (relleno mis→ficha) + grito en Fuerza Implacable · arreglando firma de T.cadena en efectos.py (pasos con ruta de imagen) → _bordes → fx hoja → video → final.
- bajar TERMINADO (191/191, 040-042 y 037 con --q). Hojas revisadas: 29 malos → `_rehacer.sh` (log _rehacer.log) lanzado ~20:50; luego mirar medios otra vez.
- (viejo) `fab.py tes_dwemer_desaparicion bajar -j 4` lanzado ~20:00 (log `_bajar.log`, iba ~75/191). Si se cortó, relanzarlo (salta los ya bajados).
- MINIATURA HECHA: salida/miniatura.jpg (Flow, 2.ª variante, centurión en ceniza; original salida/_mini_flow.png). (antes: enviada a Flow (proyecto https://flow.google.com/project/cb6bc047-df5c-47f7-957e-c54c8595ec4c, x2, prompt en prompt_miniatura.md): elegir la mejor, comprobar tildes «¿QUÉ LES PASÓ?», bajarla (URL firmada de batchexecute ogiZ0b, docs/publicacion.md) a salida/miniatura.jpg 1280x720.
- FALTA en orden: (1) terminar bajar → `medios` y MIRAR hojas (rehacer clips malos con `bajar N --rehacer`/`--q`) → (2) `ambiente_por` donde convenga (centurión, Vulthuryol, resonadores) + `ambiente` → `sfx` → `mezcla` (musica.wav YA está; si cambias ambiente_por, rehaz `python armar_musica_ost.py`) → (3) `fx hoja` (mirar) → `chequeo` → `python _bordes.py` (0 encimados) → `video` → `final` → `verificar` → (4) `canales --actualizar` → `yt subir tes_dwemer_desaparicion cronicas_tamriel private --publicar <hueco tras 14-nov>` → registrar en canales/cronicas_tamriel.json + BITACORA → `fab.py tele`/`avisar`. Duración 27:24 (el usuario pidió 24; decírselo).
- s3 CORRECCIÓN: la voz NO medía 18:00: 67 tomas buenas estaban rechazadas por Whisper (nombres) y no contaban. Con CER_MAX_POR_FRASE/TAIL_MAX_POR_FRASE en guion.py → 181/181 válidas, 1 542 s de voz, línea de tiempo 1 643,75 s (27:24). Las 48 frases nuevas se QUITARON (guion = el de la s2); sus tomas quedan en voz/cands sin uso (1 294 créditos). voces_5 rehecha (s2).
- s3: anclas ambiguas arregladas en efectos.py (votación del cierre duraba 0 s: «Leído de una nota#2»), +60 FX de relleno al final (`_huecos.py` 54 → 4 huecos), sfx/ del juego copiados de Sentinel, armar_musica_ost.py reescrito (17 secciones) y musica.wav armado. Pegatinas nuevas: vyrthur, nimhe, kagrenzel, almalexia, espectro, radac, gnisis, lexicon, deep_folk (sin uso tras quitar las frases).
- (anulado) s3: guion.py +48 frases al FINAL de escenas (p20,p19,p18,p17,p15,p14,p13,p12,p11,p10,p9,p7,p4,p2) + escena nueva `teorias` (Profeta) tras p3; `voz` lanzada (log _voz2.log). Backup del guion previo en el scratchpad de la s3.
## (checkpoint s2)
- HECHO: voz ElevenLabs de las 181 frases (4 287 créditos, cuenta 2 queda ≈ 22 619) + `seleccionar` → **Voz total 1 080 s = 18:00: FALTAN ~6 min para los 24 que pidió el usuario**.
- SIGUIENTE, en orden:
  1. Ampliar guion.py ~45-50 frases (~6 000 caracteres) SIN tocar las frases ya generadas (las tomas se reusan por texto): más lore verificado de `_investigacion.md` (Tonal Architecture/Gnisis de ESO, Deep Folk Crossing → Bthar-zel, Kagrenzel y su jaula, Dwarven Spectres y Radac Stungnthumz de Morrowind, Mzulft en ESO, Gelebor, Dahrk Mezalf, teorías b-g de Lore:Dwemer, Ancient Tales «un niño de ocho años crea un gólem», Fal'Zhardum Din = Blackreach en ESO) repartido entre las voces (frases nuevas al final de escenas existentes o escenas nuevas `pXb`); quizá un secreto «extra» por voz. Luego `voz` (solo genera las nuevas) → `seleccionar` → `tiempo`.
  2. `beats` → `busquedas` (escribir busquedas.json: inglés, 2-4 palabras, «Skyrim … no commentary»; Morrowind/ESO donde toque) → `bajar -j 4` → `medios` (MIRAR hojas).
  3. efectos.py YA ESCRITO (≈ 230 FX, anclas = texto del guion): `fx --seco` (arreglar anclas que no casen y firmas de T.cadena/receta/ruleta/balanza/lecturas), `_huecos.py` (cambiar 1161/19.35 por la duración real), `fx hoja` y mirarla; añadir FX para las frases nuevas.
  4. `armar_musica_ost.py`: reescribir SECCIONES con las 20 pistas de audio/ost/_ids.json (Morrowind y Skyrim de Soule, ESO Greymoor de Derrick: blackreach_rising, skyrims_dark_secret, darkened_depths…) con T("pX") → `ambiente` → `sfx` → `mezcla`.
  5. `chequeo` → `python _bordes.py` → `video` → `final` → `verificar` → miniatura Flow → `yt subir … private --publicar <hueco tras 14-nov>` → avisar (`fab.py tele`/`avisar`).
- Archivos tocados: guion.py, efectos.py, pegatinas/ (75 + 15 com_*; mosaico previews/pegatinas.jpg), mapas/skyrim.jpg + morrowind.jpg (coords en efectos.py), audio/ost/ (20 pistas), nucleo/mg_tes.py (MG nuevo `destello`, al final).
## Hecho
- `_investigacion.md` (UESP, 36 URLs) · guion.py (20 secretos, 7 voces + Humano narra el 6)
- `nuevo --yt`, candado, `canales --actualizar`, comentarios leídos (34 nuevos)

## Falta
- [ ] guion · voz · beats · busquedas · bajar · pegatinas · efectos.py (MG, mapas, fichas de quién narra) · OST · sfx · mezcla · chequeo · _bordes · video · final · verificar · miniatura Flow · subir y programar

## Lecciones (cierre, 4-nov-2026)
- Duración real de la voz = mirar `voz/regenerar.json` antes de creer «Voz total» (67 tomas buenas rechazadas por nombres) → CER/TAIL por frase.
- Anclas ambiguas (1.ª aparición) y firmas de cadena/receta/ruleta: probarlas por script antes de `_bordes`; `_desencimar.py` deja 0 encimados.
- 20 % de clips rehechos (memes, VTuber, menús): 2.ª vuelta con `--url` de videos limpios ya bajados.
- Studio: monetización «Activada» y cuestionario enviado (Violencia 1.ª, Desagradable 1.ª); queda «Comprobando» hasta que YouTube procese la SD. Video relacionado de Shorts: no aplica (es un largo).
- Comentarios para contestar: pendiente de borrador si el usuario lo pide.
- (5-nov, el usuario) Se repitió la crítica «kyrim» (@jhonfeddiszabalamoreno9056, ya contestada en `tes_secretos_40`) y un agradecimiento (`UgwNcSsvmI…`, ya en `tes_cosas_nunca`). No se corrige este video; regla nueva: ningún comentario se enseña dos veces (`docs/estilo_secuencia_yt.md` § COMENTARIOS; `yt comentario` lo rechaza).
