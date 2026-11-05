# Ramsés II (biografía, piloto del kit «documental de personaje antiguo») — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: bitacora_perdida · hueco: el canal está ATRASADO desde el 3-nov (prioridad alta)
- estilo: documental de personaje antiguo (kit `nucleo/docu_antiguo.py`) → docs/estilo_docu_antiguo.md · prueba: `_prueba_kit.py`
- etapa: SUBIDO ✅ https://youtu.be/6kPyIjnHOYk privado, se publica jue 5-nov 14:00 CDMX (miniatura + .srt aplicados; publicados + BITACORA registrados)
- siguiente: CERRADO. Facebook «Historias Perdidas de México» publicado 5-nov (fb_id 1211758334847804). Pendiente opcional: pasar `tunel.py` al kit si el usuario lo aprueba; medir a 7 días

## Sesiones (plan de tramos · «continúa el video ramses_ii» retoma aquí)
- alias: Ramsés, Ramsés II, el faraón, el piloto del kit nuevo
- vista previa: el usuario eligió 8-10 min; enseñarle el GANCHO renderizado (≈1 min, con voz+música+SFX+mezcla) antes de animar el resto
- leer al empezar: este ESTADO + docs/estilo_docu_antiguo.md (entera, es corta)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | kit nuevo + doc + esqueleto del guion | ✅ 4-nov | referencias analizadas; prueba del kit en previews/prueba_kit.jpg |
| 2 | guion completo + voz + tiempo | ✅ 4-nov | voz **Hugo M** `HIkzxzvsigFIynXHHKhU` (5 graves probadas en `prueba_voz/`; Ludovico/Salvatore son de Gaia); 1 184 palabras; 9:36; ~1 480 créditos (cuenta 2); datos verificados con fuentes en el docstring |
| 2b | material: Flow (cine) + Commons + yt-dlp | ◐ parcial 4-nov | Flow y Commons del gancho+cap.1 hechos; falta Desfile 2021 (yt-dlp) y Flow de Kadesh en adelante |
| 3 | escenas del gancho y cap. 1 (0-2 min) + vista previa al usuario | ✅ 4-nov (v2) | tras la crítica «muy lenta, parece secuencia de fotos»: `escenas.py` rehecho con capas (partículas, humo, recortes que cruzan, contadores, frisos reales que corren, flashes, rayos, cámara que se mueve); `_hoja_densidad.py` = 6 cuadros/0,5 s por toma; avance v2 en `salida/ramses_ii_AVANCE.mp4` + `previews/ramses_ii_AVANCE_720p.mp4` (21 MB) — el usuario: «mejoró mucho», pide v3 (abajo) |
| 4 | escenas 2-9:36 (Kadesh → cierre) + Flow de Kadesh, tratado, constructor, familia, escondite, París 1976 | ✅ 4-nov (40 láminas + 94 capas + 7 recorridos de túnel; hojas `previews/_h4*.jpg`) | cada escena con `A.firma(...)` única |
| 5 | cierre: sfx → mezcla → final → verificar → miniatura Flow → subir + Facebook Historias Perdidas | ✅ 5-nov (sfx ✅, mezcla ✅ −14,1 LUFS, miniatura ✅, MASTER ✅ + parche de 6:06 (hueco oscuro en `f_hijos`), firmas registradas, biblioteca catalogada, lecciones en el doc; subido 6kPyIjnHOYk, Facebook 1211758334847804 ✅) | `A.registrar_firmas("ramses_ii")` |

## En curso (4-nov, 20:30) — TRAMO 5: lo que falta, EN ORDEN
1. El render entero corre en segundo plano desde ~20:15 (`fab.py ramses_ii video --procs 4`, log `previews/_render_full.log`; ≈ 53 s por segmento →
   192 segmentos ≈ 2,8 h, termina hacia las 23:00). NO relanzarlo: mira la última línea del log; si se cortó, el mismo comando reanuda.
2. `python fab.py ramses_ii final` → `verificar` → mirar `previews/final_hoja.jpg` (sin rondas largas de rigor: el usuario revisa).
3. Copia 720p a la tele: `python fab.py tele video ramses_ii master --pregunta "¿Lo subo así?" --opciones "Sí, súbelo|Hay que cambiar algo" --esperar 900` (en segundo plano).
4. `python fab.py canales --actualizar` → hueco de Bitácora (ATRASADO desde el 3-nov) → `python fab.py yt subir ramses_ii bitacora_perdida private --publicar <ISO>`;
   registrar en `canales/bitacora_perdida.json` (publicados) + BITACORA.md. `youtube.json` listo (revisa que `subtitulos` apunte al .srt real que saque `final`).
5. Facebook «Historias Perdidas de México» al instante (`E:\PaginaFace\pagina.py --pagina historias_mx`, tipo video, `programar --ya`, copia < 1 GB; docs/publicacion.md § «Facebook»).
6. Cierre: `A.registrar_firmas("ramses_ii")`, `biblioteca catalogar` + `biblioteca sfx catalogar`, lecciones en docs/estilo_docu_antiguo.md
   (túnel en todo el video, rótulos sueltos que caducan a los 5 s, no repetir en capas el texto de la lámina), subir `tunel.py` al kit si el usuario lo aprueba, commit.
- Miniatura: Flow (Nano Banana 2.1, ingredientes reales: momia y busto de Commons), «PROFESIÓN: REY» + sello «FALLECIDO»: `salida/ramses_ii_mini_final.jpg` (alt `_mini_alt.jpg`; originales en `flow/mini/`).

## Tramo 4 (4-nov, noche) — TRAMO 4: el usuario aprobó el v4 («va bien, me gusta cómo manejas las capas; continúa con todo lo que falta»)
- Pidió: que los TEXTOS se vean aunque haya varias capas → HECHO: `escenas.con_texto` captura el texto de cada toma (`_TXT`, envolviendo
  rotulo_serif/neon/cursiva_luz/texto_mixto/cita/etiqueta/contador) y `tunel.Tunel.render` lo vuelve a pintar ENCIMA (con sombra) para la
  lámina que se narra; los rótulos sueltos (`spr_texto`) van siempre al final. Probado en `previews/_texto_fix.jpg`.
- Flow tramo 4 HECHO: 20 escenas (`flow/_prompts_t4.txt`, `flow/F7a…F26b.jpg`, elegidas → `imagenes/cine_<nombre>.jpg`: kadesh_campamento,
  espias, carros_hititas, faraon_solo, escultores, tratado_firma, princesa, piramses, sol_santuario, cincel, nefertari_reina, kv5_pasillo,
  sacerdotes_momias, ataudes_1881, belzoni_arrastre, poeta, ozymandias_desierto, unesco_corte, paris_lab, desfile). Hoja `previews/_flow_t4.jpg`.
- Commons tramo 4: un subagente baja ~31 imágenes reales + recortes rembg (`_bajar_commons2.py`, hoja `previews/_commons2.jpg`).
- ESCRITO (sin probar ni integrar): `_t4_laminas.py` = 37 láminas 120-576 s con su `A.firma` (k_mapa, k_divisiones, k_espias, k_mentira, k_carga,
  k_cinco_mil, k_solo, k_empate, k_historia, k_propaganda, t_frontera, t_pacto, t_doble, t_onu, t_boda, c_nombre, c_piramses, c_rameseo, c_abusimbel,
  c_sol, c_borrar, f_nefertari, f_esposas, f_hijos, f_kv5, f_herederos, f_muerte, f_merenptah, e_viaje, e_1881, o_belzoni, o_shelley, o_poema,
  o_presa, o_traslado, o_paris, z_desfile, z_balance, z_pasaporte, z_final) + helpers fs/fe/IMGX/cine/foto/lonlat/centrar/_tiene, polígonos
  `_HATTI`/`_CANAAN` (mapa_medit: x = 1505 + (lon-34.58)·132, y = 102 + (35.70-lat)·163). Limpiar: bucle sobrante en k_cinco_mil y `sp` sin usar en z_pasaporte.
- HECHO 4-nov (sesión 2): (1)-(6) integrados en `escenas.py` (respaldo `escenas_v4_bak.py`; `_t4_laminas.py` ya pegado, k_cinco_mil y z_pasaporte arreglados; `_T4` + `_pos_t4()` + `_capas_t4()` + SFX). Prueba rápida `_smoke_t4.py` = 40/40 sin error. (7) HECHO: hojas `previews/_h4a…f.jpg` + correcciones `_h4_fix.jpg` (rótulos repetidos fuera, rótulos sueltos caducan a los 5 s desde 119 s, mapa sin franjas), `verificar_firmas` limpio. (8) RENDER ENTERO lanzado 4-nov ~20:15 con `--procs 4` (segmentos del avance v4 apartados en `_segmentos_avance_v4/`, eran anteriores al arreglo de textos). Al terminar: sfx → mezcla → final → verificar → tele → miniatura → subir.
- FALTA, en orden: (1) pegar `_t4_laminas.py` en `escenas.py` ANTES de «# ---- lista de tomas»; (2) en `_tomas()` quitar la fila `None` y añadir
  las láminas (t0 = inicio de su frase − 0,3: k_mapa kadesh_0, k_divisiones kadesh_2, k_espias kadesh_3, k_mentira kadesh_4, k_carga kadesh_5,
  k_cinco_mil kadesh_6, k_solo kadesh_7, k_empate kadesh_8, k_historia kadesh_9, k_propaganda kadesh_11, t_frontera tratado_0, t_pacto tratado_2,
  t_doble tratado_3, t_onu tratado_5, t_boda tratado_6, c_nombre constructor_0, c_piramses _1, c_rameseo _2, c_abusimbel _3, c_sol _5, c_borrar _6,
  f_nefertari familia_0, f_esposas _1, f_hijos _2, f_kv5 _3, f_herederos _5, f_muerte _6, f_merenptah _7, e_viaje escondite_0, e_1881 _2,
  o_belzoni ozymandias_0, o_shelley _1, o_poema _2, o_presa _5, o_traslado _6, o_paris _7, z_desfile cierre_0, z_balance _1, z_pasaporte _2, z_final _3);
  (3) `_POS`: un recorrido distinto por capítulo (kadesh zigzag a la derecha bajando; tratado recto y hondo; constructor subiendo; familia a la
  izquierda; escondite bajando; ozymandias en espiral; cierre recto) + firmas `tunel_<cap>`; (4) `_capas()`: 2 por frase con el material nuevo
  (Commons `imagenes/*` del subagente + `*_rec.png`); (5) `render_mundo`: túnel en TODO el video y fundido a negro final (2 s); (6) SFX nuevos en
  `guion.py SFX_ELEVEN` (carros, cincel, tablilla, sierra, fuegos, pluma, agua, cuerdas) + lista `SFX`; (7) `python _hoja_t.py previews/x.jpg t…`
  por capítulo (MIRAR) + `A.verificar_firmas`; (8) render entero `fab.py ramses_ii video --procs 4` (los java ya no están) → sfx → mezcla → final →
  verificar → copia 720p a la tele (`fab.py tele video … --pregunta`) → miniatura Flow → subir/programar + Facebook.
- Commons HECHO (32 + recortes carro_tut, khopesh, tratado_tablilla, estatua_usurpada, merenptah, ataud_ramses `_rec.png`; hoja `previews/_commons2.jpg`).
  Falta `tratado_onu` (no hay en Commons: `t_onu` cae a tratado_estambul). Extras: qantir_azulejos, abusimbel_traslado2. Ojo: desfile_2021 = fotograma con
  marca «360» (recortar la esquina o usar solo `cine_desfile`); mapa_hititas con nombres en polaco; espias_shasu/db320/ozymandias_examiner pequeñas (≤ 700 px:
  usarlas pequeñas, en camafeo o foto con marco); carro_hitita es neohitita de Karkemish (decir «relieve hitita», no «de Kadesh»).

## Hecho en el tramo 3 (4-nov)
- Avance v2 (capas) renderizado en 29 min para 2 min (el v1 tardó 19). Render LENTO: 19-29 min para 2 min (≈ 9,5 s de render por segundo,
  12 procesos) → el video entero ≈ 1,5 h; lanzarlo en segundo plano y no vigilarlo.
- Lo que sigue sin animar (120-576 s) sale en negro: `TOMAS` en `escenas.py` termina con `(t0 de kadesh, None, …)`; ampliar la lista ahí.
- Kit: `territorio` recorta el polígono a la pantalla (antes fallaba si tocaba el borde).
- Lección: el mapa satelital necesita medir las coordenadas en un cuadro renderizado (la estimación desde una miniatura deformada falló); Egipto = delta + valle, no un rectángulo.

## Hecho en el tramo 2 (4-nov)
- Pasaporte: NO consta en ningún archivo (imagen viral = montaje) → el guion dice «se cuenta» y «nadie ha encontrado nunca ese documento». Honores militares en Le Bourget (26-sep-1976): sí.
- Réplica del tratado en la ONU: cobre, regalo de Turquía en 1970 (comunicado HQ/246). KV5: > 100 cámaras (Weeks 1995). Kadesh: ~5 000 carros «se calcula».
- Whisper escribe distinto los nombres (Muatali, Osimandias, Meremtá): `ALIAS_QA`; `kadesh_3` (cola) y `tratado_4` («arcilla y titas») aceptadas por frase tras ver la transcripción.
- «suena exactamente a él» → «encaja exactamente con él» (regla «si la voz nombra un sonido, se oye»).
- El usuario puede oír las 3 mejores pruebas de voz en `prueba_voz/` (hugo, ludovico, salvatore); si pide otra voz, rehacer `voz` entera (~1 400 créditos).

## Esqueleto del guion (ya redactado en guion.py; fuentes en su docstring)
- **Gancho:** 1974-1976: la momia se pudría por hongos; para volar a París le hicieron PASAPORTE egipcio, «Profesión: rey (fallecido)», y Francia lo recibió
  con honores militares. ⚠ lo del pasaporte es muy citado pero discutido: decirlo como «se cuenta que…» o verificar. «¿Quién era este hombre para que, 3 200 años
  después de morir, un país entero lo tratara como jefe de Estado?»
- **1. El nieto de un soldado:** la dinastía XIX no era de sangre real (Ramsés I, general de Horemheb); Seti I lo hace corregente de niño (~14 años). Rey 1279 a.C.
- **2. Kadesh (1274 a.C.):** emboscada de Muwatalli II (hititas), 2 espías beduinos, división Amón sola, ~5 000 carros (la mayor batalla de carros conocida); Ramsés
  resiste; empate táctico → él lo esculpe como victoria en 5 templos = **la primera propaganda de la historia** (relieves reales de Abu Simbel/Ramesseum).
- **3. El primer tratado de paz** (~1259 a.C., con Hattusili III): existe en dos versiones (jeroglífica en Karnak, tablilla de arcilla hitita en Estambul); una réplica
  cuelga en la sede de la ONU. Se casa con una princesa hitita.
- **4. El constructor:** Abu Simbel (el sol entra al santuario ~22-feb y ~22-oct), Ramesseum, Pi-Ramsés; borra nombres de otros faraones y pone el suyo.
- **5. Nefertari y los ~100 hijos** (≈ 50 hijos y 50 hijas; KV5, la tumba de sus hijos, la mayor del Valle); sobrevivió a 12 herederos; reinó 66 años, murió ~90.
- **6. Después:** su momia, robada y escondida por sacerdotes (escondite DB320, hallado en 1881); Belzoni arrastra el Joven Memnón al British Museum (1816-18) →
  Shelley escribe «Ozymandias» (1818): «Mirad mis obras, poderosos, y desesperad». 1964-68: la UNESCO corta Abu Simbel en ~1 000 bloques y lo sube 65 m.
  2021: Desfile Dorado de los Faraones en El Cairo. Cierre: vuelve el pasaporte.

## Material
- Ya en `imagenes/` (Commons, con `creditos.json`): `joven_memnon.jpg` + `_rec.png`, `momia_cara.JPG` (encuadre malo: buscar otra), `Abu_Simbel…jpg`.
- Falta: relieves de Kadesh, tratado (Estambul), Nefertari (tumba QV66), Ramesseum, mapa Egipto–Hatti, Shelley/Ozymandias, Desfile 2021 (yt-dlp ≤ 8 s con crédito).
- Flow (escenas de cine, oscuras): niño Ramsés con Seti, campamento en Kadesh de noche, carros, sacerdotes escondiendo momias, laboratorio de París 1976.

## Lecciones de este video
- El tilt-shift del filtro emborronaba los rótulos → `cine_antiguo` sin tilt. `rembg` deja margen: `artefacto` recorta al contenido.
