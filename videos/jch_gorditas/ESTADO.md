# Viniste por la carrera… vas a volver por las gorditas (reel vertical) — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. -->
- canal: ninguno · Facebook (Juchipila; lo publica Edson o «Que pasa en Juchipila» SOLO con su aprobación) · antes del sáb 14-nov-2026
- estilo: SECUENCIA YT en VERTICAL como `jch_carrera_moyahua` (clips reales por beat con crédito, recorte 9:16) + `kit_jch.py` · tipo COMERCIAL / invitación
- etapa: ✅ MASTER v4 con la VOZ DE EDSON (opción A, plana) · 12-nov 12:19 · salida/jch_gorditas_MASTER.mp4 4:06 1080x1920 −14 LUFS A/V 0 ms · enviado por Rayo (WiFi) · sin tele · cambios 1-4 incluidos (v3 con Enrique: respaldos _v3 / _voz_enrique_v3)
- siguiente: Edson lo revisa en el celular → si aprueba, lo sube a Facebook con salida/post_facebook.md (NUNCA sin su OK) → `fab.py jch_gorditas limpiar`

## En curso
- sesión 1 (12-nov) cortada por contexto tras escribir busquedas.json. NO se lanzó `bajar` ni nada en segundo plano.
- `bajar` hecho (12-nov): 45/47; 017 y 041 (N1V642u57-4 no baja) cambiados a CZKb0xKPyIU 122/569 y re-bajados.
- Falta, en orden: (1) mirar hojas de medios (rehacer `desde` que no enseñe su frase); (2) fotos_redes/*.jpg → pegatinas/<slug>.png y pantallas/<slug>.jpg; churros (1VxwdPaFuoo 133) y pan (qKrXhC-Y2k8, no revisado) como cuadro 1080p para pegatina; (3) efectos.py según el PLAN; TEMA_PEG cálido (ver peg_estilos.TEMAS); credito() por clip como `jch_carrera_moyahua/efectos.py` (_creditos con CANAL) + «Foto: Gorditas Doña Chenda/Doña Yolis (Facebook)»; (4) promesas.md + `FAB_FX_FINAL=1 fx hoja` mirando TODAS las fx_NN; (5) música: `biblioteca sugerir` (Lyria sin saldo; no repetir jalpa/apozol/juchipila ni los 2 tramos del reel de la carrera); (6) video → mezcla → final → verificar → `tele video jch_gorditas master` → avisar. NO publicar en Facebook sin OK de Edson (salida/post_facebook.md listo).
- Un render a la vez: revisar antes que ninguna otra sesión corra `secuencia video`.
- sesión 2 (12-nov, tras apagón): medios revisados (009→b8ADq8B7kqo 236, 014→myMD6B4wx8A 7, 045→b8ADq8B7kqo 150 + CAMARA 1.2 tapa subtítulo); pegatinas/ (fotos FB, churros, pan de jQeYTvvCQRw «Emiliano JUCHIPILA» 108 s, letras de 5bNZspnZTIE 386 s) y pantallas/; efectos.py escrito (fx --seco OK); promesas.md; música biblioteca: tramo1 duo_promo__lyria_2, tramo2 lego_carpintero__lyria_tramo5 → audio/musica.wav ✅. Falta: fx (SFX) → fx hoja FINAL → chequeo → video → mezcla → final → verificar → tele.
- sesión 2, más tarde (12-nov ~09:50): fx ✅ (SFX nuevos en sfx/, audio/fx.wav); `FAB_FX_FINAL=1 fx hoja` revisada ENTERA y corregida (pizarra en 6 renglones, pegatinas ×1.5, letras = pegatinas/letras.png «JUCH/IPILA» marco clásico, MAYO 2027 como rótulo, 028 desde 5 sin logo, medios 043/045 recortados al 84 % por arriba con ffmpeg para quitar subtítulos quemados del dron — NO hacer `bajar --rehacer` de 043/045 sin repetir el recorte); últimos cambios menores sin re-hoja: churros dur 2.6 y «LLÉVATE FRUTA» y=.15. `chequeo` ✅ (idioma OK; «sin apoyo» cubiertos por rótulos/mapa/cartel; «escucha bien» no es un sonido). **fx ✅ re-armado 09:58. `video` en cola en 2.º plano (espera a que acabe el render de er_godrick_atrocidades; log en previews/_render.log). Siguiente: comprobar que nadie corra `secuencia video` → `video` → `mezcla` → `final` → `verificar` → `tele video jch_gorditas master` en 2.º plano → `avisar`.**

## PLAN de efectos (beat → MG; kit_gor = G, kit_jch = K)
- 001-004: dict abre; G.cartel("BIENVENIDOS A","JUCHIPILA","ZACATECAS") en 001-002 (y≈.30); K.ficha("CAIN ROAD RACE MÉXICO 2026",[evento 13-15 nov, carrera dom 15]) en 002-003; ambiente_por 001/002 (motos); rótulo «VEN CON MUCHA HAMBRE» en 004
- 005-008: pantalla G.mapa_paso() de scene-005 a scene-008:fin, marcas ["diecisiete","Apozol"]
- 010 rótulo «LO IMPORTANTE» · 011 pant chenda_02 + G.sello("IMPRESCINDIBLE") marca «sin probar» · 012 SFX chisporroteo
- 013-014: G.pizarra("GORDITAS DE JUCHIPILA",["De lomo","De rajas","De queso","De chorizo","+ salsa verde, queso y cebolla"]) marcas lomo/rajas/queso/chorizo/salsa
- 015-016 rótulo «RECIÉN HECHA, AHÍ SENTADO» + pv yolis_02 (friéndose) · 017 pv chenda_03 en «Una no alcanza» + rótulo «CALLEJÓN DE LOS JAMBADOS» · 018 K.cifra(40,"AÑOS",sub="friéndolas") · 019 pant yolis_03 · 020 fila horchata/café/chocolate (rótulos)
- 021-024: G.tacometro() de «advertimos» a scene-023:fin, marca «volver por las gorditas»; 024 pv chenda_01 + rótulo «¿A QUÉ HORA ABREN?»
- 026 rótulo «BIRRIA TATEMADA» · 027 pv churros + pv pan · 028 K.cifra o rótulo «GUAYABA DEL CAÑÓN» · 032 rótulo «TEMPLO DE SAN FRANCISCO» · 034 rótulo «📸 LAS LETRAS»
- 035-036 rótulo «SIN CURVAS… PERO CON SABOR» · 037 K.ficha("SI VAS A LA CARRERA",[Llega antes de las 10, Almuerza en Juchipila, Trae efectivo]) marcas · 041 rótulo «SE QUEDA EN JUCHIPILA» · 042 ficha «MAYO 2027» · 044 pant yolis_00 · 045 G.cartel("","JUCHIPILA","TE ESPERAMOS") · 047 rótulo «¿LOMO, RAJAS O CHORIZO?» + dict cierra
- Zona segura Reels: nada importante bajo y≈.78 ni pegado a la derecha en la mitad baja.

## Sesiones
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | investigación, guion, voz, tiempo, beats, kit_gor, fotos, busquedas | ◐ parcial 12-nov | corte por contexto a 180 mil |
| 2 | medios, pegatinas, efectos, SFX, música, hoja FINAL, chequeo, render, MASTER | ✅ 12-nov | verificar sin problemas; música biblioteca duo_promo__lyria_2 + lego_carpintero__lyria_tramo5 |
| 3 | cambios 1-4 de Edson: guion+voz (6 frases), beats 57, clips y efectos v3, MG pizarra CÓMO PEDIRLAS, búsqueda de mapa y comentario, MASTER v3, Rayo | ✅ 12-nov | verificar sin problemas; música rearmada a 248,65 s (tramo 1 en bucle con cruce) |
| 4 | portada del reel en Flow (Nano Banana 2.1, ingredientes reales chenda_02 + motos scene-001 + letras; prompt_miniatura.md): salida/portada_reel.jpg (9:16, A1) + portada_reel_cuadrada.jpg (1:1) + portada_reel_alt.jpg (9:16 compacta); descripción con horarios/recomendaciones de la CAIN (salida/descripcion_reel.md; no hay comunicado oficial de noviembre en internet: horarios de organizadores vía B15/Imagen/NTR); todo por Rayo (WiFi). Nada en Facebook | ✅ 12-nov | |
| 4 | voz de Edson (opción A: GUEeiSJYQQdbv0NJ86Im, stability 1.0, sin corchetes), beats 56, clips/efectos v4, MASTER, Rayo | ✅ 12-nov | verificar OK; umbrales de voz por frase en guion.py |

## Decisiones (Edson, 12-nov-2026)
- secuela del reel de la carrera (tuvo muchas vistas): invitación a bikers Y público de la CAIN Road Race (13-15 nov) a entrar a Juchipila a consumir lo local; que desde el inicio se sepa que es de Juchipila y del evento
- las GORDITAS fritas (con lomo encima) = IMPRESCINDIBLES, comidas ahí sentados, recién hechas; broma: «vienes por la carrera, vas a volver por las gorditas»
- vertical, ~3 min; narrador Enrique M. Nieto (mismo del reel anterior)

## Clips candidatos (yt-dlp, revisar en hojas)
- gorditas: 0j2qOJ2IJgM (14 s «GORDITAS IN JUCHIPILA») · myMD6B4wx8A · He0krFDCFRY (Uribe «El Chino») · 4imj8PW1eFo (churros, gorditas, calles) · sVCAp39CRPQ / CUd91cvqCWI / WXV7MyWhKi0 (Erika Ulloa, receta en casa: solo proceso, rótulo «estilo Juchipila»)
- callejón de los Jambados: 1VxwdPaFuoo (Caxcán Online) · N1V642u57-4 · birria: tVovSCNRmuE (don Alex) · -YPDUKO67KQ · CZKb0xKPyIU · jrSSfmw6LKs
- antojos: 5A-tV6-F0zI (chicharrones) · qKrXhC-Y2k8 (pan) · z7J_0u82xaY · S15emaCOPBI (gastronomía)
- pueblo: J6vZRk1-f9M · 0owcStKDbB0 / DEBbViEU7sE (4K walking) · b8ADq8B7kqo (dron 4K) · 5bNZspnZTIE / x0kdsfkhYmo (plaza) · QPEXkJxTw94 · 5u-hb0uTu1k (jardín Madero)
- motos: los del reel anterior (9nQiFRaa_Bs, HOanpy2EGo8, d-OqU-t6pME Juchipila llena de motos 200-340)

## Fotos de redes (Edson 12-nov: «busca fotos de gorditas en redes»; crédito «Foto: <página> (Facebook)» en cada una)
- fotos_redes/chenda_01 (collage con logo), chenda_02, chenda_03 (gorditas de lomo con queso, cebolla y chile) = Gorditas Doña Chenda (facebook.com/Gorditaschenda, Juchipila)
- fotos_redes/yolis_00 (tacos dorados + gorditas), yolis_02 (gorditas FRIÉNDOSE en el cazo), yolis_03 (plato) = Gorditas Doña Yolis (Facebook, tel. lada 467)
- receptor para bajarlas: scratchpad receptor.py (:8799) — FB bloquea fetch a localhost por CSP; se navega a 127.0.0.1:8799/get#lista
## Clips elegidos (segundos)
- 1VxwdPaFuoo Caxcán Online (EL MEJOR): templo 7-13, callejón 37-49, carne/lomo 55-61 y 103, gorditas inflándose en el aceite 73-91, churros 115-139, gordita con lomo encima 157-175
- myMD6B4wx8A Daniel RC (anuncio «Gorditas Juchi estilo Juchipila»): fritura 5-7, lomo+queso 8-11, platos 13-20 (solo cerca, sin su logo)
- tVovSCNRmuE (VERTICAL) birria don Alex en el callejón: 7, 79, 115, 157-163, 205 · CZKb0xKPyIU Rosy Rosy: jardín 1-21, callejón 82-183, birria 691, 1138
- 5A-tV6-F0zI chicharrones: cazo 49-55, 121, 235-241 · N1V642u57-4 callejón 1-187, plaza/templo 205-211, dulces 217-229
- 5bNZspnZTIE Vicky (2026): LETRAS JUCHIPILA 391-411, jardín 165-206, 832-843 · J6vZRk1-f9M Bien Chulo: torre 33, jardín 17/83/855, callejón 99, mercado 395-411, plaza 805-822
- b8ADq8B7kqo dron: pueblo 141-171, templo de noche 181, valle 221-241 · pu6amlAuHvk guayaba en el árbol 1, huerta 932
- motos (reel anterior): 9nQiFRaa_Bs onboard 62+, HOanpy2EGo8 grupo 200-320, d-OqU-t6pME Juchipila llena de motos 200-340

## En curso — CAMBIOS DE EDSON (12-nov, tras ver el MASTER v1)
1. Tramo de gorditas FRITAS: solo fritas planas con lomo ENCIMA (myMD6B4wx8A 5-20, fotos chenda_02/03, yolis_00/02/03, He0krFDCFRY ~274). Fuera las RELLENAS (1VxwdPaFuoo 73-91 / 157-175) de ese tramo; van aparte en una frase nueva «Y si te gustan rellenas, también las hay…».
2. Acompañamiento: + COCA DE VIDRIO bien fría como «el combo perfecto» (myMD6B4wx8A ~22-23 trae la botella) + rótulo/sello EL COMBO PERFECTO.
Pasos: guion → voz (solo nuevas) → seleccionar → idioma_voz → tiempo → beats → remapear busquedas/efectos → bajar → fx hoja FINAL → fx → video → mezcla → final → verificar → Rayo (NO tele, NO Facebook) → avisar a la sesión madre.
- v2 hecho hasta aquí: guion (gorditas_9 rellenas, _10 horchata+coca, _11 combo), voz+seleccionar+idioma ✅, tiempo+beats ✅ (52 beats, 3:46), busquedas.json v2 escrito a mano (fritas = myMD6B4wx8A 5-23 + fotos; rellenas solo en 020-021; coca/combo = myMD 21-24 pantalla partida), pegatinas coca.png/combo.png. Copias v1: _beats_v1.json, _busquedas_v1.json, _efectos_v1.py. Falta: bajar --todos --rehacer → recortar 048 y 050 (dron con subtítulo, ffmpeg crop 84 % arriba) → efectos.py v2 (scene-ids nuevos) → hoja FINAL → fx → video → mezcla → final → verificar → Rayo.
- CAMBIOS 3 y 4 de Edson (mismo render): (3) salsa ROJA (picante, de jitomate que no pica, o las dos) + queso, cebolla y chile verde frito aparte; mini tutorial «sírvamela como se acostumbra» + MG «CÓMO PEDIRLAS»; fuera todo «salsa verde». (4a) tras el Callejón: «si está lleno… Google Maps o alrededor del centro» + MG búsqueda de Maps con pines (sin nombres). (4b) cierre: invitar a los de Juchipila a dejar su puesto/negocio en comentarios + MG comentario genérico «Tu negocio aquí 👇»; cierre ≤ ~10 s; línea en salida/post_facebook.md antes de los hashtags.
- v3 (cambios 1-4 juntos): guion + voz ✅ (43 frases, idioma OK), tiempo + beats ✅ (57 beats, 4:09), busquedas.json v3 ✅ (copias _beats_v2.json/_busquedas_v2.json). Dron con subtítulo ahora en 055 y 056 (recortar tras bajar). Falta: bajar → recorte 055/056 → efectos.py v3 (tutorial CÓMO PEDIRLAS, MG Maps, MG comentario) → hoja FINAL → fx → video → mezcla → final → verificar → Rayo + post_facebook.md.
- v3: bajar ✅ (57; 055/056 recortados), kit_gor + busqueda_mapa() y comentario(), pizarra encoge renglones; efectos.py v3 ✅ (copia _efectos_v2.py); hoja FINAL revisada ✅ (arreglados: rótulos sobre créditos de foto, «varios puestos» bajo la barra, 030 sin logo → desde 17.8); post_facebook.md con invitación a negocios ✅. En marcha (11:0x): bajar 30 → fx → esperar render libre → video → mezcla → final → verificar (log previews/_v3.log). Luego: Rayo ("D:/Rayo/pc/publish/Rayo.exe" <MASTER>, confirmar en %APPDATA%\Rayo\log.txt) + avisar a la sesión madre. NO tele, NO Facebook.
- PEDIDO NUEVO (Edson, 12-nov ~11:50): rehacer el MASTER v3 con SU VOZ NUEVA «opción A», PLANA (sin emoción), en vez de Enrique M. Nieto, y mandarlo por Rayo. La «opción A» no está registrada en el disco: la eligió en la sesión «Video promocional Juchipila gastronomía» (local_ca77b58f-30ce-4bef-9d99-e0bc75dec52b) → pedirle ahí el voice_id. Todo lo demás (guion v3, beats, clips, efectos) se queda; tras la voz nueva: seleccionar → idioma_voz → tiempo → beats → reasignar busquedas/efectos si cambian los cortes → video → mezcla → final → verificar → Rayo.
- VOZ DE EDSON (12-nov ~12:00, la pidió él): opción A = GUEeiSJYQQdbv0NJ86Im (cuenta 3: hCU4QZdzzUliy58ezPBz), stability 1.0, style 0, sin corchetes de emoción. Muestra aprobada: audio/prueba_voz_edson_A_plana.mp3. Respaldo de la versión con Enrique: _voz_enrique_v3/, _guion_enrique_v3.py, _beats_v3.json, _busquedas_v3.json, _efectos_v3.py. Falta: voz → seleccionar → idioma → tiempo → beats → reasignar → bajar → hoja → fx → video → mezcla → final → verificar → Rayo.
- v4 (voz de Edson): voz ✅ 43/43 (umbrales por frase en guion.py; cierre_0 = «Aquí te estamos esperando»), idioma OK, tiempo + beats ✅ (56 beats, 4:06), busquedas.json + efectos.py v4 ✅ (respaldos _v3). En marcha: bajar → recorte 054/055 → medios → fx hoja. Luego: música usar+armar → fx → video → mezcla → final → verificar → Rayo.
