# RevisiÃ³n de las 6 jugadas analizadas (27-oct-2026) â€” CORREGIR EN OTRA SESIÃ“N

El usuario (27-oct): Â«revisa todas las demÃ¡s jugadas, deben ser perfectas y no inventar nadaÂ». El video ya estÃ¡ subido en
PRIVADO (https://youtu.be/lcGGYgWwZEg, sin publicar). Corregir â†’ regenerar solo las frases (voz â†’ seleccionar â†’ tiempo;
si la escena cambia de compases, `"post"` en esa escena) â†’ efectos.py â†’ re-render de los tramos afectados (6 en paralelo,
scratchpad de la sesiÃ³n 3: render_par.py) â†’ final â†’ verificar â†’ subir de nuevo en privado por la pestaÃ±a de Studio
(monetizaciÃ³n activada, Â«Nada de lo anteriorÂ» en idoneidad, miniatura/elegida.jpg). El video viejo lo borra el usuario.

MÃ‰TODO (lo que fallÃ³): no fiarse de la narraciÃ³n ni de los subtÃ­tulos automÃ¡ticos (cambian nombres: Â«KeriaÂ», Â«CuzzÂ»).
Cada dato se comprueba en los CUADROS: kill feed, banners, etiquetas de nombre y, sobre todo, los RETRATOS DEL HUD de abajo
(el que muere se pone gris con su contador: orden real de las muertes). Herramientas en el scratchpad de la sesiÃ³n 3
(copiar a videos/lol_worlds_2026/ si hace falta): rejilla.py (cuadros con rejilla y zoom), contacto.py, cuadros_fx.py.
Recorte de HUD: f[930:1080, 440:1440] de jN.mp4 (orden de retratos: top, jungla, medio, tirador, soporte; izq. = azul).

## Jugada 2 Â· DK vs T1 (j2.mp4 = H2 Fbxau2uQc_E desde 1960 s) â€” âŒ ERROR CONFIRMADO
- jugada2_3 dice Â«Career, con Renata, se lanza con Destello al centro de T1Â». FALSO. Cuadros 78.0-79.6 (40:28-40:30): quien
  entra con Destello es KERIA (T1, Neeko) con la definitiva de Neeko sobre DK (cÃ­rculo en 78.0; en 78.8 ya estÃ¡ en la lÃ­nea
  de atrÃ¡s de DK; en 79.6 Â«STUNNED/SILENCEDÂ» sobre DK). VOD 47:08: Â«Keria flashes forward. [Fate's call] will pull out the
  Renata, Smash gets the knockupâ€¦ The ultimate will take overÂ». Smash usa la definitiva de Kalista para SACAR a Career de ahÃ­
  y lanzarlo; Career responde con la definitiva de Renata (Hostile Takeover).
- Propuesta: Â«Keria se lanza con Destello y la definitiva de Neeko sobre DK. Pero Smash usa la definitiva de Kalista para
  sacar a Career de ahÃ­â€¦ y Career responde con la definitiva de Renata.Â» (~10,7 s como la actual).
- efectos.py 453-464: tarjeta Â«Destello al centro Â· CareerÂ», pegatina Renata Â«Career Â· DestelloÂ» â†’ cambiar; aÃ±adir anillo y
  flecha de la entrada de Keria (medir en 78.0 con zoom 1,35 .45,.55) y pegatina de Neeko (Keria) gris/roja.
- Revisar tambiÃ©n: Â«T1 sale volandoÂ» (Â¿se ve el derribo de Kalista? confirmar en cuadros 79-81).

## Jugada 1 Â· KC vs AL (j1.mp4 = H1 _9iVitbeCio desde 1000 s) â€” narraciÃ³n y anillos OK, 1 dato falso
- âœ… Orden confirmado por la narraciÃ³n oficial (H1 17:56): Pop Blossom (Neeko) y Bullet Time (MF) de AL â†’ Hostile Takeover
  (Busio) â†’ onda de choque (kyeahoo) â†’ Cataclismo (Yike) â†’ cae Nocturne â†’ Â«quadra for the Jaxâ€¦ a one-fourÂ». Kill feed 297 s:
  Â«AL Hope has slain KC YikeÂ» (la 1 muerte de KC). Anillos de la pausa 24:36 sobre los jugadores correctos; Â«KC A CIEGASÂ»
  cuadra (KC con Â«NEARSIGHTEDÂ» = definitiva de Nocturne).
- âŒ jugada1_5: Â«el cuarto nexo chino que cae en las CUATRO PRIMERAS PARTIDAS DEL MUNDIALÂ». Falso: el Mundial empezÃ³ con el
  play-in (15-oct). La narraciÃ³n dice Â«the fourth LPL nexus OF THE DAY and there's only been four gamesÂ» â†’ Â«â€¦en las cuatro
  primeras partidas de la fase suizaÂ» (o Â«del dÃ­aÂ»).
- âš  Interpretaciones no dichas por nadie (quitar o confirmar en cuadros): flecha discontinua Â«KC CIERRA EL PASOÂ» (pizarra
  280.4), Â«Jax Â· Por detrÃ¡sÂ» (pegatina 295.6) y Â«Con Jax, POR DETRÃSÂ» en jugada1_3 (la narraciÃ³n dice Â«going ballistic in the
  back lineÂ»: Â«directo a la lÃ­nea de atrÃ¡sÂ» sÃ­ vale).

## Jugada 3 Â· DK vs KOI G1, penta de Smash (j3.mp4 = H3 Oix7cBcGmgM desde 830 s) â€” âŒ ERRORES CONFIRMADOS (HUD)
- HUD de KOI (rev_j3_hud.jpg): 64.2 cae MYRWN (Jayce, top) â€” primera muerte â€”; 69.6 cae SUPA (Ezreal); 72.8 cae ALVARO
  (Karma); 79.2 caen ELYOYA (Trundle) y JOJOPYUN (Anivia) = el penta. AdemÃ¡s DK pierde a CAREER (Nautilus: contador 14 en
  64.2). NarraciÃ³n H3 14:49: Â«the anchor connect onto the bird and they take out the [Jayce]â€¦ Supa taken out by Smash, the
  exhaust means absolutely nothingâ€¦ triple, quad, pentaÂ».
- âŒ jugada3_2 Â«El ancla conecta. Anivia cae primeroÂ» â†’ FALSO: el ancla atrapa a la Anivia, pero el primero que cae es el Jayce
  de Myrwn; Anivia cae la ÃšLTIMA. Tarjeta Â«Anivia, la primera Â· JojopyunÂ» (624.3) â†’ falsa.
- âš  jugada3_3 Â«Su Kai'Sa espera a que KOI gaste todoâ€¦ y entonces entraÂ»: interpretaciÃ³n, nadie lo dice; comprobar en cuadros o
  quitar. Â«Supa cae. El Agotamientoâ€¦ no sirve de nadaÂ» âœ… (narraciÃ³n). Tarjeta Â«Espera a que KOI gaste todoÂ» (631.1) idem.
- âš  No se dice que Career muriÃ³ en la pelea (no es falso omitirlo).
- âœ… jugada3_0 (corregida: +0,8K en 32:30), pausa 38:23 (Jojopyun adelantado, Career encima), Â«primer y Ãºnico pentakillÂ»
  (gol.gg), Â«DK 2-0, primer clasificadoÂ».

## Jugada 4 Â· LYON vs GEN G1 (j4.mp4 = H3 desde 1230 s) â€” PENDIENTE de revisar en cuadros; ya visto:
- âŒ Montaje engaÃ±oso: la voz dice Â«LYON acaba de quedarse con el BarÃ³nâ€¦ Y ahora mira a InspiredÂ» como si fuera seguido, pero el
  BarÃ³n es en el 20:24 y la entrada de Inspired en el 34:41 (14 minutos despuÃ©s). Decirlo (Â«catorce minutos despuÃ©sâ€¦Â») o
  usar la pelea que viene justo tras el BarÃ³n (narraciÃ³n H3 20:59-21:29: Â«Cash in from Inspiredâ€¦ THE BERSERKER IS STILL
  STANDING. LION! WHAT A PLAYÂ»).
- âŒ/âš  Pizarra 20:24: flechas Â«GEN.G LLEGA TARDEÂ» y anillo Â«LYONÂ» = inventados/no medidos: verificar posiciones y quitar la
  interpretaciÃ³n si no se ve.
- âš  Â«Busca a uno solo: ChovyÂ» / Â«Â¡Chovy cae!Â»: el kill feed dice Â«LYON Dhokla has slain GEN ChovyÂ» (34:48): lo mata Dhokla
  (Olaf), no Inspired. La narraciÃ³n: Â«Inspired! he jumped into the center of the teamâ€¦ Chovy is killedÂ». Decir que Inspired
  abre y Chovy cae, sin atribuirle la muerte a Inspired; revisar HUD para el orden de muertes y Â«LYON gana la peleaÂ».
- âœ… Kalista de Berserker en el BarÃ³n (Â«the Rend is too muchÂ»), Â«dragon stacking was the planÂ», GEN gana 2-1 y queda 3-0.

## Jugada 5 Â· IG vs HLE (j5.mp4 = H3 desde 215 s) â€” PENDIENTE de revisar en cuadros (HUD); ya visto:
- âœ… jugada5_0 corregida (alma del Infernal y +3,7K de IG). Rookie detrÃ¡s en la pausa 24:25 âœ… (posiciÃ³n).
- âš  Â«esperando a que Hanwha gaste sus herramientasÂ» y el texto Â«QUE HANWHA GASTE SUS HABILIDADESÂ»: interpretaciÃ³n.
- Por comprobar con el HUD/kill feed: Gumayusi muere a manos de Rookie (narraciÃ³n: Â«Rookie kill creditÂ»), Â«tres contra tresÂ»,
  polimorfo de Lulu al Olaf, orden triple â†’ cuÃ¡druple (banners Â«TRIPLE KILLÂ» 89, Â«QUADRA KILLÂ» 92).

## Jugada 6 Â· TLAW vs AL G2, el BarÃ³n (prueba lol_worlds_tl_al) â€” PENDIENTE
- Viene de la prueba (verificada entonces con la transcripciÃ³n del VOD). Revisar igual: marcador 11-17 âœ… (cuadro 1009 s),
  Â«+3 000 de oroÂ» (el cuadro dice 77,4K vs 73,9K = +3,5K), Â«6-2 en torresÂ», tercer dragÃ³n/alma, oleada + TP de Morgan, Â«Liquid
  se queda con toda la visiÃ³nÂ» y las fichas del tablero (posiciones aproximadas sacadas del minimapa: decirlo o medirlas).

