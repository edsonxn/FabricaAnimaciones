# Las 5 peores atrocidades de Mohg QUE IGNORASTE — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · meta: hueco del canal (URGENTE: sin video desde mié 11-11 10:00 CDMX; ciclo 3 d) → mirar `canales --actualizar`
- estilo: secuencia_yt (gameplay de Elden Ring por beat + PEGATINAS + pant() + MG NUEVOS `nucleo/mg_er.py` + mapas; sin patrocinio) · voz Chatterbox Faraon → doc: docs/estilo_secuencia_yt.md § Runa Caída
- etapa: ✅ SUBIDO y PROGRAMADO mié 11-nov-2026 10:00 CDMX: https://youtu.be/G6C2R0X_oCo (privado + publishAt, miniatura Flow + .srt por API)
- siguiente: visto bueno del usuario (revisión r1110131958 en la tele: `tele revisar-resultado r1110131958 er_mohg_atrocidades`) · Studio: monetización + video relacionado · medir la suscripción a 7 días · `limpiar` al aprobar

## Sesiones (UNA sesión directo al MASTER, regla 5-nov; avance y MASTER a la tele sin preguntar)
- alias: mohg, atrocidades de mohg
- leer al empezar: este ESTADO + docs/estilo_secuencia_yt.md § Runa Caída (líneas ~912-1042); plantilla de TODO el resto: videos/er_morgott_atrocidades/ (efectos.py, asignar_clips.py, bajar_ost.py, armar_musica_ost.py, _anclas.py, medir_brillo.py, _revisar_voz.py, youtube.json, prompt_miniatura.md)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | datos + tema + investigación + guion | ✅ 10-nov | sesión 1 (cortada por contexto a los 180 mil) |
| 2 | voz (lanzada) + OST + sonidos + plan de clips | ◐ parcial 10-nov | sesión 2 (corte por contexto): ver «En curso» |
| 3 | seleccionar + tiempo + beats + clips + pegatinas + MG + mapas + mezcla + chequeo + render + tele + miniatura + subir | ✅ 10-nov | MASTER 24:12, verificar CER 0,010; tele con copia 720p (el de 1,8 GB cortó la conexión al 40 %); subido G6C2R0X_oCo |

## Decisiones del episodio (10-nov-2026)
- tema: MOHG (elegido por el usuario de 3: Mohg, Rykard, Godfrey/Godwyn); duración: **23 min** (pedido del usuario)
- **NUEVA REGLA del usuario (10-nov): «hay que pedir suscripciones antes del minuto 5»** → hecho en p5b (frase 8, ~3:30), ADEMÁS del
  tramo de campaña hacia el 75 % (final de p2b, cifra 30 d: 3 045 de 76 050 vistas = 4 % suscritos; 651 subs → meta 1 000).
  PENDIENTE: apuntarla en docs/estilo_secuencia_yt.md § CAMPAÑA, canales/formula/runa_caida.md y memoria (¿solo Runa o todos? preguntar al cerrar).
- Comentarios: token sin force-ssl (403) → leídos con yt-dlp (`_investigacion/*.info.json`, Morgott fMBEJI5FjaY y Radahn Uuj8Bw45-fs).
  Gancho: @zoharysakiyamablue471 ♥5 (9-nov, «mi patrón MOHG… NIHIL»), @JustinRivera-c9l ×2. Agradecimientos (5): @dany00g1 ♥5,
  @isaackbradleyfreega (p4c), @joseluisdelavegaest, @davidponsmedina7224, @Eternalack (cierre). Corrección: @jonathanvillamil985
  («rey augurio», p3b). Crítica con burla disfrazada: @Nikova14 (Radahn, «¿atrocidad a alguien que perdió la cordura?», p2b).
  Broma: @escuadronnf (Torrentera, cierre). Piden: Rykard (@franko637, @hectorsocarras3030), Godwyn (@carlramonescch), Maliketh
  (@JustinRivera-c9l, @Ronn3773), Godrick, Mésmer, Rellana → canales/formula. Tarjetas: `yt comentario er_mohg_atrocidades runa_caida <id>` (pegatinas/com_<id>.png).
- Voz IA: quejas siguen (no nuevas fuertes); @isaackbradley la acepta → reportar al usuario al avisar del MASTER.

## En curso (checkpoint 10-nov, sesión 2, cortada por contexto a los 180 mil)
- LANZADO ~07:25: `fab.py er_mohg_atrocidades voz --seeds 1 2` en segundo plano (log `_voz.log`; iba en 107/224 a las ~08:10). Si
  `voz/cands` tiene 224 tomas y no hay python con chatterbox vivo, terminó. NO relanzar.
- HECHO en guion.py: posts medidos con Whisper = p5 6.0 · p4b 6.0 · p2 10.0 · p1 11.0 · p1b 3.5; p4b_2 cambió «Sí, oíste bien» →
  «Escúchalo de su boca» (el sonido va DESPUÉS): REGENERAR esa frase: borrar voz/cands/p4b_2_* y `voz --seeds 1 2 --solo p4b_2`.
- HECHO sfx/ (PISTAS voz=True, −18 LUFS, verificados con Whisper): s_maidenless (5,75 s, Stratek Varré 11,0-16,75),
  s_scream (5,6 s, 625,9), s_welcome (10,1 s, Leomega 97,8), s_nihil (11,4 s, Leomega 163,2-174,6), s_mohgwyn (2,8 s, 336,2).
  En efectos.py: `PISTAS = [dict(sfx="s_maidenless", en="Así suena en inglés|fin", vol=1.0, voz=True), dict(sfx="s_scream",
  en="Escúchalo de su boca|fin", …), dict(sfx="s_welcome", en="Así lo dice él|fin", …), dict(sfx="s_nihil", en="Escúchalo|fin"
  (p1_8), …), dict(sfx="s_mohgwyn", en="el nombre de su casa|fin", …)]`; tras `tiempo`, alinear el clip del beat del post a esos
  segundos (Stratek Yp6mfzUQlfM / Leomega 3h5IIdRbqGc) para que la boca cuadre; medir volumedetect de audio/fx_voz.wav ahí.
- HECHO OST: bajar_ost.py (omen, godskin, astel + copias) → audio/ost/; armar_musica_ost.py con SECCIONES de Mohg (correr tras `tiempo`).
- HECHO plan de clips: `_plan.py` → plan_frases.json (112/112 frases, fuentes vistas en hojas: Leomega sin HUD de Mohg, SS91
  Parts 40-43/5/1/49, Stratek Varré/Yura/Gideon/Ansbach, Leomega Okina/Vyke/Eleonora, etc.). OJO: recorte_por .09 en los beats
  de D_iqjI2p7F4 (SHIRRAKO, Malenia); NE (HhNFpTSOs3I) con rótulos 30-140 s; el video de Ríos vs Malenia sin HUD (dntKHh8R2bQ)
  DESCARTADO (jugador desnudo).
- HECHO (sesión 2, tras el corte): pegatinas/pantallas bajadas y revisadas (previews/pegatinas_check.jpg; descartadas en
  pegatinas/_descartes: albinaurico_rojo2 = esqueleto, torrentera = dibujo B/N, varre_invasion dudosa; caras «Character Face»
  recortadas sin la etiqueta de interfaz) · 11 tarjetas com_<id> con `_tarjetas.py` (hechas antes de la reconexión del 10-nov; ya vale `yt comentario`) · 3 MG nuevos en mg_er
  (`cuenta_atras`, `reclutamiento`, `dinastia`; prueba previews/mg_todos.jpg) · mapas/ (mundo, limgrave) · efectos.py COMPLETO
  (175 FX + PISTAS de los 5 sonidos) con 0 anclas malas en `_anclas.py`.
- Copiados de Morgott: _revisar_voz.py, medir_brillo.py, asignar_clips.py, _anclas.py. Nombres de archivo de pegatinas en la wiki:
  `_investigacion/pegatinas_wiki.txt`.
- HECHO voz: 7 frases regeneradas con semillas 3-6 por «Moj/Mock/Barlet» (elegidas a mano: «Mog», «Barré»); tomas malas en
  voz/_descartes; umbrales *_MAX_POR_FRASE en guion.py; `tiempo` + `beats` hechos (167 beats, 1 432,5 s). asignar_clips hecho;
  beats de los sonidos fijados a mano (`_mano`): 015 Stratek@6, 055 @624, 107 Leomega@93.6, 108 @97, 135 @162, 151 @331;
  recorte_por scene-098 (Shirrako). armar_musica_ost ✅. Miniatura: Chrome de Flow abierto (puerto 9222) y
  `flow_thumb.py --file miniatura_ing/prompt_linea.txt --variantes 2` lanzado → miniatura_ing/flow/.
- HECHO tras beats: bajar 167 clips + 11 rehechos (BonfireVN oscuro, noble Hacx7 negro, mapa) · medir_brillo limpio · fx hoja
  revisada (2 siluetas cambiadas a pegatina) · PISTA de Nihil corregida (`Escúchalo.#2`; se había ido a la de Varré) · mezcla
  −14,1 LUFS, los 5 sonidos a −19/−22 dB · chequeo (avisos de sonido = falsos positivos de PISTAS voz=True). Selector de Flow
  arreglado en C:\googleimagenes\scripts (texto nuevo «Subir archivos multimedia»).
- FALTA, en orden: (voz) → seleccionar → tiempo → beats → asignar_clips → bajar -j 4 → medir_brillo → hojas → rehacer →
  armar_musica_ost → bajar_pegatinas + `yt comentario … <id>` de los 10 comentarios (ids en _investigacion/*.info.json) →
  MG NUEVOS en mg_er (`cuenta_atras`, `reclutamiento`, `dinastia`) → efectos.py (copiar estructura de Morgott) → _anclas →
  fx hoja → promesas.md + pegatinas_check → mezcla → chequeo → video → final → tele master → verificar → miniatura Flow →
  yt subir private --publicar <hueco> → registrar + BITACORA + canales --actualizar → cierre (regla «suscripción antes del
  min 5» en docs) + commit.

## Lecciones de este video (solo lo no obvio)
- Un MASTER de ~1,8 GB corta la subida a la tele (ConnectionReset al 40 %): mandar una copia 720p NVENC cq 28 con `tele revisar <v> --archivo`.
- Regla «suscripción antes del min 5» apuntada en docs/estilo_secuencia_yt.md § CAMPAÑA y canales/formula/runa_caida.md; falta que el usuario diga si vale para todos los canales.
- Runa Caída se reconectó con force-ssl el 10-nov: `yt comentarios runa_caida` y `yt comentario <v> runa_caida <id>` ya funcionan (el 403 era del token viejo); el .srt también sube por API (`yt aplicar`). Las 11 tarjetas de este video se hicieron antes con `_tarjetas.py` (desde yt-dlp), con los mismos datos reales.
