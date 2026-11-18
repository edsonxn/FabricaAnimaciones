# La VERDADERA razón por la que cayó T1 (BLG 3-1 T1, semifinal Worlds 2026) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: Crónicas de ligoleyen (UCXU8DV4QJ24yhwXmrR_eLhw; subida por Studio en el navegador, NO está en la API) · publicar en cuanto esté (≥ 1 día después del de fichajes KmoTBym9d_o del 17-nov)
- estilo: análisis táctico (secuencia_yt + VOD + mg_tactica + mg_lol + mg_lol_pelea + 3D) → doc: docs/estilo_analisis_tactico.md · copiar de `videos/lol_final_previa/` (mismas partidas) y `videos/t1_koi_worlds/`
- etapa: ✅ SUBIDO por Studio y PROGRAMADO jue 19-nov-2026 10:00 CDMX · https://youtu.be/D5j-GQ5zbgc (MASTER 11:31, 640,6 MB, desfase 0) · miniatura «T1 CAYÓ / ¿CULPA DE DORAN?», 19 etiquetas, no para niños, IA «No», anuncios + mid-roll, idoneidad «Nada de lo anterior», .srt es-419 publicado
- siguiente: nada de producción. Medir a 48 h (CTR, retención) en Studio. MASTER NO mandado a la tele (regla 17-nov: solo si él lo pide).

## Sesiones
- alias: «la caída de T1», «t1 blg», «la verdadera razón de T1»
- vista previa: NO (directo al MASTER, regla 5-nov); a la tele el MASTER
- leer al empezar: este ESTADO + docs/estilo_analisis_tactico.md § GUÍA RÁPIDA + investigacion/datos_*.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación + guion + voz + jugadas + render + subida | ✅ 18-nov (sesión 1: investigación + guion v1; sesión 2: datos de agentes, guion v2, voz, fx, render; sesión 3: idioma_voz arreglado (g3_3, g4_3, cierre_1), 3D y medios rehechos, render 2 (tramos 4-5 relanzados por MemoryError), Studio: el usuario eligió el MASTER en el cuadro de Windows; miniatura y .srt por túnel cloudflared + fetch) | tema elegido por el usuario entre 3 (T1 / New Dawn 2027 / top 10 jugadas) |

## Decisiones
- Duración ~15 min (el usuario). Sin spoiler NO aplica: la caída de T1 ya es sabida (título, miniatura y gancho la usan).
- Por qué este tema (datos 17-nov): «La VERDADERA razón por la que T1 perdió contra BLG» (GGN) 422 mil vistas en 6 días; embeejay «se acabó la era de T1» 45 mil, reacción de Faker 38 mil. En el canal: resumen general 58 mil, semis 5,5 mil.
- NO reciclar las jugadas de `lol_final_previa` tal cual (su público vio la previa): se reutilizan DATOS y fuentes cortadas, pero con otro enfoque (el «porqué»), otras pausas y el 3D re-renderizado con otra cámara.

## TESIS (todo del feed oficial `investigacion/stats_g*.json`, feed_12x.txt)
1. **El chivo expiatorio, Doran: tiene parte de razón.** Perdió su línea en LAS 4 partidas (oro vs Bin a los 20 min: −1 166 G1 Rumble/K'Sante, −647 G2 Olaf/Camille, −1 842 G3 Ambessa/Gnar, −1 536 G4 Vayne/Renekton). 22 muertes en 4 partidas (0/5/3, 7/5/9, 1/7/4, 2/5/3 = 10/22/19); el que más murió de la serie. Oner 16, Peyz 14, Keria 11, Faker 5.
2. **T1 fue por detrás de oro al minuto ~15-17 en LAS 4 partidas**, también en la que ganó (G2: −2,7K al 17:13).
3. **El equipo con más dragones ganó las 4 partidas**: G1 BLG 3-1 (+Barón 21:06) · G2 T1 4-0 → alma del Océano (robo 23:15) + Anciano 30:30 + 2 Barones · G3 BLG 4-2 → alma infernal 32:59 + 2 Barones · G4 BLG 4-2 → alma de montaña 34:55 + Barón 35:54.
4. **Faker NO fue el problema**: 14/5/21 en la serie (4/2/2, 4/0/13, 3/2/2, 3/1/4). Knight 18/7/30 (G1 Orianna 8/0/9), Viper 23/11/27, Bin 13/9/26.
5. G4: T1 remonta de 3-10 (−3,6K) con la pelea 28:02-28:27 (Faker 3, Doran 2), toma el Barón 29:25… y pierde la pelea 32:23-32:32 con el Barón a punto de acabar → alma de BLG → fin (37:42).

## Material ya verificado (copiado de lol_final_previa/investigacion)
- `datos_j4.md` (G2 cierre, VOD r9-avVeme5o, K=448; robo del alma 23:15 = j4b) · `datos_j5.md` (G3 pelea del alma 31:44-34:14, VOD Tq2FdhgReuI, K=451) · `datos_j6.md` + `pistas_j6.json` (G4 32:04-32:28, VOD n616F3asGf0, K=481) · `datos_relleno.md` § r_t1g1 (G1 29:18-30:04, VOD bt2sO3ioJJ4).
- Fuentes 1080p en `videos/lol_final_previa/medios/_fuente/` (j4, j4b, j5, j6, j6_baron, j6_fin, r_t1g1, mesa_j5a…).
- Agentes (17-nov): `datos_g1.md` (G1: pelea 15:43, Barón 21:06, pelea 24:02-24:40) y `datos_g4a.md` (G4: draft Vayne, 08:31-09:01, Doran 10:57, 17:38-17:46).

## Lecciones (cerrado 18-nov)
- Pasadas a docs/estilo_analisis_tactico.md § «Rehacer la voz de un análisis ya montado»: frases cortas de solo nombres fallan idioma_voz; tail_ratio por frase; re-voz = 3D + medios + render completo; render_par copiado con nombre fijo; MemoryError con otra sesión; final que une el video viejo.
- Studio en el navegador integrado: localhost bloqueado (acceso a red local); el MASTER lo elige el usuario en «Seleccionar archivos»; archivos chicos (miniatura, .srt) por túnel cloudflared con clave + fetch + DataTransfer (docs/estilo_analisis_tactico.md).
