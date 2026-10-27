# Revisión de las 6 jugadas analizadas (27-oct-2026) — CORREGIR EN OTRA SESIÓN

El usuario (27-oct): «revisa todas las demás jugadas, deben ser perfectas y no inventar nada». El video ya está subido en
PRIVADO (https://youtu.be/lcGGYgWwZEg, sin publicar). Corregir → regenerar solo las frases (voz → seleccionar → tiempo;
si la escena cambia de compases, `"post"` en esa escena) → efectos.py → re-render de los tramos afectados (6 en paralelo,
scratchpad de la sesión 3: render_par.py) → final → verificar → subir de nuevo en privado por la pestaña de Studio
(monetización activada, «Nada de lo anterior» en idoneidad, miniatura/elegida.jpg). El video viejo lo borra el usuario.

MÉTODO (lo que falló): no fiarse de la narración ni de los subtítulos automáticos (cambian nombres: «Keria», «Cuzz»).
Cada dato se comprueba en los CUADROS: kill feed, banners, etiquetas de nombre y, sobre todo, los RETRATOS DEL HUD de abajo
(el que muere se pone gris con su contador: orden real de las muertes). Herramientas en el scratchpad de la sesión 3
(copiar a videos/lol_worlds_2026/ si hace falta): rejilla.py (cuadros con rejilla y zoom), contacto.py, cuadros_fx.py.
Recorte de HUD: f[930:1080, 440:1440] de jN.mp4 (orden de retratos: top, jungla, medio, tirador, soporte; izq. = azul).

## ESTADO 27-oct (sesión 5): TODAS REVISADAS
- Textos corregidos en guion.py: jugada1_3 (sin «por detrás»), jugada1_5 («de la fase suiza»), jugada2_3 (Destello de KERIA +
  definitiva de Neeko; Smash saca a Career con Kalista; Career responde con Renata), jugada3_2 (el ancla atrapa a la Anivia,
  cae primero el Jayce de Myrwn), jugada3_3 (sin «espera a que KOI gaste todo»), jugada4_0/1/2 (Barón en el 20, la pelea
  decisiva 14 min después; sin «busca a uno solo: Chovy»), jugada5_1 (sin «esperando a que Hanwha gaste…»), jugada6_2/3.
- j2: al final DK remata sola el Anciano (40:40, 1 814 PV, T1 con 4 muertos) ✓.
- j4 ✓ con cuadros: Barón 20:24 «Blue team has slain» (LYON azul, LCS #2; Gen.G LCK #1); la pizarra del Barón coincide con
  Kiin, Ruler y Chovy llegando. 34:42 AIRBORNE sobre 4 de Gen.G, 34:48 «LYON Dhokla has slain GEN Chovy», 6-4 → 8-4.
  Picks G1: Berserker Kalista, Inspired Xin Zhao, Dhokla Olaf, Chovy Anivia.
- j5 ✓ con HUD y kill feed: 24:27 «Rookie is on a killing spree», 24:40 «rampage» y Gumayusi muere (temporizador 37 a las
  24:43) → Rookie lo remata ✓; 3 contra 3 (IG: Wei, Rookie, Meiko · HLE: Zeus, Zeka, Delight) ✓; Rookie 3/1/8 → 7/1/8.
- j6: ver ESTADO.md (verificada con la narración del VOD y el minimapa; ahora en 3D, nucleo/tactica3d).

## Jugada 2 · DK vs T1 (j2.mp4 = H2 Fbxau2uQc_E desde 1960 s) — ❌ ERROR CONFIRMADO
- jugada2_3 dice «Career, con Renata, se lanza con Destello al centro de T1». FALSO. Cuadros 78.0-79.6 (40:28-40:30): quien
  entra con Destello es KERIA (T1, Neeko) con la definitiva de Neeko sobre DK (círculo en 78.0; en 78.8 ya está en la línea
  de atrás de DK; en 79.6 «STUNNED/SILENCED» sobre DK). VOD 47:08: «Keria flashes forward. [Fate's call] will pull out the
  Renata, Smash gets the knockup… The ultimate will take over». Smash usa la definitiva de Kalista para SACAR a Career de ahí
  y lanzarlo; Career responde con la definitiva de Renata (Hostile Takeover).
- Propuesta: «Keria se lanza con Destello y la definitiva de Neeko sobre DK. Pero Smash usa la definitiva de Kalista para
  sacar a Career de ahí… y Career responde con la definitiva de Renata.» (~10,7 s como la actual).
- efectos.py 453-464: tarjeta «Destello al centro · Career», pegatina Renata «Career · Destello» → cambiar; añadir anillo y
  flecha de la entrada de Keria (medir en 78.0 con zoom 1,35 .45,.55) y pegatina de Neeko (Keria) gris/roja.
- Revisar también: «T1 sale volando» (¿se ve el derribo de Kalista? confirmar en cuadros 79-81).

## Jugada 1 · KC vs AL (j1.mp4 = H1 _9iVitbeCio desde 1000 s) — narración y anillos OK, 1 dato falso
- ✅ Orden confirmado por la narración oficial (H1 17:56): Pop Blossom (Neeko) y Bullet Time (MF) de AL → Hostile Takeover
  (Busio) → onda de choque (kyeahoo) → Cataclismo (Yike) → cae Nocturne → «quadra for the Jax… a one-four». Kill feed 297 s:
  «AL Hope has slain KC Yike» (la 1 muerte de KC). Anillos de la pausa 24:36 sobre los jugadores correctos; «KC A CIEGAS»
  cuadra (KC con «NEARSIGHTED» = definitiva de Nocturne).
- ❌ jugada1_5: «el cuarto nexo chino que cae en las CUATRO PRIMERAS PARTIDAS DEL MUNDIAL». Falso: el Mundial empezó con el
  play-in (15-oct). La narración dice «the fourth LPL nexus OF THE DAY and there's only been four games» → «…en las cuatro
  primeras partidas de la fase suiza» (o «del día»).
- ⚠ Interpretaciones no dichas por nadie (quitar o confirmar en cuadros): flecha discontinua «KC CIERRA EL PASO» (pizarra
  280.4), «Jax · Por detrás» (pegatina 295.6) y «Con Jax, POR DETRÁS» en jugada1_3 (la narración dice «going ballistic in the
  back line»: «directo a la línea de atrás» sí vale).

## Jugada 3 · DK vs KOI G1, penta de Smash (j3.mp4 = H3 Oix7cBcGmgM desde 830 s) — ❌ ERRORES CONFIRMADOS (HUD)
- HUD de KOI (rev_j3_hud.jpg): 64.2 cae MYRWN (Jayce, top) — primera muerte —; 69.6 cae SUPA (Ezreal); 72.8 cae ALVARO
  (Karma); 79.2 caen ELYOYA (Trundle) y JOJOPYUN (Anivia) = el penta. Además DK pierde a CAREER (Nautilus: contador 14 en
  64.2). Narración H3 14:49: «the anchor connect onto the bird and they take out the [Jayce]… Supa taken out by Smash, the
  exhaust means absolutely nothing… triple, quad, penta».
- ❌ jugada3_2 «El ancla conecta. Anivia cae primero» → FALSO: el ancla atrapa a la Anivia, pero el primero que cae es el Jayce
  de Myrwn; Anivia cae la ÚLTIMA. Tarjeta «Anivia, la primera · Jojopyun» (624.3) → falsa.
- ⚠ jugada3_3 «Su Kai'Sa espera a que KOI gaste todo… y entonces entra»: interpretación, nadie lo dice; comprobar en cuadros o
  quitar. «Supa cae. El Agotamiento… no sirve de nada» ✅ (narración). Tarjeta «Espera a que KOI gaste todo» (631.1) idem.
- ⚠ No se dice que Career murió en la pelea (no es falso omitirlo).
- ✅ jugada3_0 (corregida: +0,8K en 32:30), pausa 38:23 (Jojopyun adelantado, Career encima), «primer y único pentakill»
  (gol.gg), «DK 2-0, primer clasificado».

## Jugada 4 · LYON vs GEN G1 (j4.mp4 = H3 desde 1230 s) — PENDIENTE de revisar en cuadros; ya visto:
- ❌ Montaje engañoso: la voz dice «LYON acaba de quedarse con el Barón… Y ahora mira a Inspired» como si fuera seguido, pero el
  Barón es en el 20:24 y la entrada de Inspired en el 34:41 (14 minutos después). Decirlo («catorce minutos después…») o
  usar la pelea que viene justo tras el Barón (narración H3 20:59-21:29: «Cash in from Inspired… THE BERSERKER IS STILL
  STANDING. LION! WHAT A PLAY»).
- ❌/⚠ Pizarra 20:24: flechas «GEN.G LLEGA TARDE» y anillo «LYON» = inventados/no medidos: verificar posiciones y quitar la
  interpretación si no se ve.
- ⚠ «Busca a uno solo: Chovy» / «¡Chovy cae!»: el kill feed dice «LYON Dhokla has slain GEN Chovy» (34:48): lo mata Dhokla
  (Olaf), no Inspired. La narración: «Inspired! he jumped into the center of the team… Chovy is killed». Decir que Inspired
  abre y Chovy cae, sin atribuirle la muerte a Inspired; revisar HUD para el orden de muertes y «LYON gana la pelea».
- ✅ Kalista de Berserker en el Barón («the Rend is too much»), «dragon stacking was the plan», GEN gana 2-1 y queda 3-0.

## Jugada 5 · IG vs HLE (j5.mp4 = H3 desde 215 s) — PENDIENTE de revisar en cuadros (HUD); ya visto:
- ✅ jugada5_0 corregida (alma del Infernal y +3,7K de IG). Rookie detrás en la pausa 24:25 ✅ (posición).
- ⚠ «esperando a que Hanwha gaste sus herramientas» y el texto «QUE HANWHA GASTE SUS HABILIDADES»: interpretación.
- Por comprobar con el HUD/kill feed: Gumayusi muere a manos de Rookie (narración: «Rookie kill credit»), «tres contra tres»,
  polimorfo de Lulu al Olaf, orden triple → cuádruple (banners «TRIPLE KILL» 89, «QUADRA KILL» 92).

## Jugada 6 · TLAW vs AL G2, el Barón (prueba lol_worlds_tl_al) — PENDIENTE
- Viene de la prueba (verificada entonces con la transcripción del VOD). Revisar igual: marcador 11-17 ✅ (cuadro 1009 s),
  «+3 000 de oro» (el cuadro dice 77,4K vs 73,9K = +3,5K), «6-2 en torres», tercer dragón/alma, oleada + TP de Morgan, «Liquid
  se queda con toda la visión» y las fichas del tablero (posiciones aproximadas sacadas del minimapa: decirlo o medirlas).


