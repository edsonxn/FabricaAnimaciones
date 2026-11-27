# 5 atrocidades de Maliketh que el juego te ESCONDIÓ — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: runa_caida · hueco dom 29-nov-2026 12:00 CDMX (2026-11-29T18:00:00Z = Messmer 26-nov 18:00Z + ciclo 3 d; runa_caida.json)
- estilo: secuencia_yt (gameplay por beat + pegatinas + MG `nucleo/mg_er.py` + mapas tema `er`, OST oficial, SIN Overgear) → doc: docs/estilo_secuencia_yt.md § «Runa Caída»
- etapa: SUBIDO y PROGRAMADO 27-nov → https://youtu.be/bwpSvLHDhlE (private, sale dom 29-nov 12:00 CDMX) · anuncios ACTIVADOS + cuestionario
- siguiente: Studio cuando termine el procesado SD → casilla MID-ROLL + pantalla final (importar de Messmer) + «Probar y comparar» (salida/miniatura.jpg vs miniatura_B.jpg) → `fab.py yt monetizado bwpSvLHDhlE` · medir ≈ 2-dic

## Sesiones (UNA SESIÓN DIRECTO AL MASTER, regla 5-nov)
- alias: «Maliketh», «las atrocidades de Maliketh», «er_maliketh»
- leer al empezar: este ESTADO.md · plantilla `videos/er_messmer_atrocidades/` (herramientas copiadas aquí; su ESTADO tiene el orden exacto de pasos) · docs/estilo_secuencia_yt.md § Runa Caída / REGLA DE ORO / COMENTARIOS / CAMPAÑA · canales/formula/runa_caida.md § «FÓRMULA VIGENTE 27-nov» y § «PLANTILLA NUEVA de empaque»

## Decisiones del episodio (27-nov-2026)
- Investigación R45 hecha hoy (FÓRMULA VIGENTE en canales/formula/runa_caida.md): Maliketh = señal fuera (EldenBR ×8,07) + 3 pedidos dentro; semidiós de primera fila.
- EMPAQUE NUEVO (plantilla 26-nov): título «5 atrocidades de Maliketh que el juego te ESCONDIÓ» (50 car.; NO «QUE IGNORASTE»: Messmer ya lo llevó) · miniatura Flow escena del juego con la cara, 2-3 palabras de UN puesto, color BLANCO-GRIS/NEGRO + dorado (Messmer fue cálido) · 2 variantes + «Probar y comparar» al estreno.
- Duración ≈ 25 min. Voz el Profeta `HNSF1CTQmub252yhXROX` PLANA, `eleven_v4_turbo`; FONETICA Miquella→Miquéla (+ lo que pida el dossier). OST oficial (bajar_ost.py). Sin Overgear. Promo al final: Crónicas de Tamriel (promo_canal).
- R46: cada puesto = algo que el jugador normal NO sabía (texto escondido, diálogo opcional, DLC, beta).
- Comentarios (leídos 27-nov: 55 nuevos; tarjetas en pegatinas/com_*.png, 12):
  · PEDIDO Maliketh: @bautivenier9997 UgxoCYU4dtPLXve5bl14AaABAg («maliked tiene mucha pinta») · @AylanWar12 UgySmUGdjRfjJxkBcX94AaABAg («lo espero con muchas ansias», 17-nov) · @yoPisoPapas UgzBDd9Lo8N3FkUbdBd4AaABAg («yeeiiii maliketh vamoooo»)
  · AGRADECIMIENTOS: @xxe0511 UgxPfvjIQIZU-ZQM8_94AaABAg (novia que no juega; se suscribió) · @albertoisaiasflorescruz4012 UgypNy1lYYyWaXbJoit4AaABAg · @jonatandominguez6094 UgzctI4k2oDTuBdFzuR4AaABAg (rueda de Ghiza) · @Bryan-yu6ij UgyIXFYc9OQgyjwcpfB4AaABAg · @LissomStreik UgwqsA6iIqCgJqVSd754AaABAg («ya me suscribí») · @astoraperochikito5067 UgzGKL5gZgOIwF1SwsN4AaABAg («atrocidades de estos enfermos»)
  · CRÍTICAS con contraburla: @diegocuesta9289 Ugyq6VrXBUyp9nIRFVx4AaABAg («su único pecado fue servir a una tirana» → el video entero lo desmiente) · @EdgarFelipe-d9y UgyB1EoWLW8OFtGeOMh4AaABAg («habla latino… y me puedes saludar»; NO afirmar nombres latinos sin fuente; @oswaldovaca2620 descartado: ya citado en Sinluz) · respuesta: @DarkShooter942 UgwSM-kZWs4crUYmDih4AaABAg (Gurranq «nos suplicaba que guardáramos el arma»; comprobar contra el guion de Sinluz)

## En curso (checkpoint 27-nov, tarde)
- ✅ `nuevo` · herramientas de Messmer copiadas (ADAPTAR: armar_musica_ost SECCIONES, _render_tramos.sh V/T, _promesas, _peg_check, _plan) · mapas · 12 tarjetas com_*
- ✅ dossier `_investigacion/dossier.md` (+19 pantallas) · ✅ guion (3 172 palabras, 20 escenas) · ✅ 5 sfx de diálogo en sfx/ (Whisper OK) · ✅ OST 24 pistas · ✅ 46 pegatinas
- ✅ 6 MG nuevos en nucleo/mg_er.py (retal, recambio, nombre_bestia, jaula_orden, pruebas, dos_muertes; hoja previews/mg_prueba_hoja.jpg revisada)
- ✅ voz 108/108 (≈ 4 300 créditos, saldo cuenta 4 ≈ 39 500) · 25+5 falsas alarmas por nombres con umbrales por frase · reescritas y regeneradas: introb_0/p1c_0 («En español:» se lo comía → «Y lo que dice es esto:»), introb_3/p2_3/cierrec_1 (Maliketh a final de frase), y 10 oraciones cortas por idioma_voz → «OK todas en es» (OJO: leer el log ENTERO, no `tail`)
- ✅ tiempo 1 455 s (24:15) · 169 beats · youtube.json (50 car., 14 capítulos, promo Tamriel) · ✅ miniaturas Flow A «ELLA LO TRAICIONÓ» + B «ERAS TÚ» en salida/ (ver prompt_miniatura.md)
- ✅ plan_frases.json (subagente: 263 opciones, 35 fuentes, 0 avisos) → asignar_clips → `bajar -j 4` 169/169 (020 reintentado) · medir_brillo: rehechos 069 (intro 170), 088, 110, 117, 119, 125 (Catacumbas del Cuchillo Negro 500), 144, 164 · recorte_por .13 en las escenas del tráiler TRN
- ✅ efectos.py (subagente): 301 FX, anclas 0 malas, huecos 0; 2.ª tarjeta de Diego → rótulo (R46) · `yt repetidos` OK · audio/musica.wav OST 1 455 s
- ✅ clips revisados (subagente): 25 rehechos (avisos de objeto, «YOU DIED», menús, planos fijos seguidos, solapes) · dedupe 0 · 35 avisos OCR = subtítulos del juego aceptados · recorte_por: 137 tráiler .13; 014/021/029/032 (0,0,.14,0) marca «Khonziel» · 156 = xaXLX1UOl8A@73 sincronizado con s_perdon
- ✅ FX revisados (subagente): `FAB_FX_FINAL=1 fx hoja` 16 hojas ×3 pasadas MIRADAS (expediente con ritmo/tmin en mg_er; sin vitral sobre caras) · promesas.md 130 + escenas.md 21 · pegatinas_check 175 OK (radagon_cara, mohg_cara, ave_muerte_cerca nuevas) · chequeo OK
- ✅ fx → mezcla −14,06 LUFS, pico −1,05 dBTP, voz/fondo 13,7 dB · REGLA 10 en la mezcla: las 5 citas OK con Whisper (−17 a −19 LUFS) → repetir en el MASTER
- ✅ render por tramos (6) → `final` (pantalla final runa_caida) → MASTER 1 475 s, 1 595 MB · `verificar` desfase 21 ms, blackdetect 0, final_hoja OK
- ✅ REGLA 10 en el MASTER: las 5 citas se oyen (−16,8 a −19,4 LUFS) y Whisper las reconoce · previews/citas_audio.mp3
- ✅ `yt subir … --publicar 2026-11-29T18:00:00Z` → bwpSvLHDhlE (miniatura A + .srt) · runa_caida.json publicados + BITACORA · panel /api/v2/obra OK
- ✅ Studio: Anuncios «Activada» + cuestionario (Violencia y Desagradable = 1.ª opción → «Adecuado para anuncios») GUARDADO
- ◐ MID-ROLL, pantalla final y Probar y comparar: bloqueados por «primero se debe procesar la versión SD»; sigue en canales/monetizacion_pendiente.json

## Sesiones
- 27-nov (UNA sesión, «buenos días»): investigación R45 → dossier → guion → voz → clips → FX → mezcla → MASTER → subido y programado → anuncios. Para seguir: «continúa el video maliketh» (solo falta lo de Studio que espera el procesado).

## Lecciones (27-nov)
- «En español:» antes de una cita lo traga la voz → «Y lo que dice es esto:». Nombres propios al final de frase disparan idioma_voz: moverlos al centro.
- idioma_voz: leer el log ENTERO (las « X »), no `tail`; la medición es estable entre pasadas.
- flow_thumb puede decir FALLO y sí haber generado: bajar las imágenes por CDP (playwright, 9222).
- Clips de canales con marca de agua (Khonziel): recorte_por con tupla (0,0,.14,0).
- Studio tras subir 1,6 GB: el mid-roll y la pantalla final no se pueden poner hasta que termina la versión SD; dejarlo anotado y volver.

## Falta
- [ ] MID-ROLL + pantalla final + Probar y comparar (tras el procesado SD) · `yt monetizado bwpSvLHDhlE` · medir ≈ 2-dic
