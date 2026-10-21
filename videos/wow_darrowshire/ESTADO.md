# Darrowshire: la niña que sigue esperando — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · SUBIDO y PROGRAMADO jue 22-oct-2026 09:00 CDMX (publishAt 2026-10-22T15:00:00Z) · https://youtu.be/paQ5FISMZzU
- estilo: FORMATO NUEVO = pegatina Flow (docs/estilo_pegatina_flow.md) en clave de terror + pegatinas REALES de WoW + clips yt-dlp de apoyo · ejemplo: videos/asteroide_invisible/
- etapa: TODO ✅ · MASTER 13:49 (con pantalla final) · verificar CER 0,0023 · rigor ✅ · subido con miniatura + .srt · registrado (canal, BITACORA)
- siguiente: cierre de hallazgos (docs/estilo_pegatina_flow.md + canales/formula/cronicas_warcraft.md) · medir el 29-oct (7 días) contra la mediana del canal · `limpiar` cuando el usuario lo apruebe

## Sesiones (plan de tramos · «continúa el video wow_darrowshire» retoma aquí · protocolo docs/sesiones.md)
- alias: wow_darrowshire, el de Darrowshire, el de la niña fantasma, el de lore oscuro de Warcraft, el formato nuevo de Warcraft
- vista previa: 🎞 Montaje del panel con audio completo (voz + Lyria + SFX del juego + mezcla) conforme salen las escenas
- leer al empezar: este ESTADO.md, docs/estilo_pegatina_flow.md y el ESTADO.md de videos/asteroide_invisible/ (fusión que funcionó)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Investigación con fuentes + guion ~12 min (CTA del formato a la mitad y al final) + voz ElevenLabs + seleccionar + tiempo | ✅ 20-oct | guion ✅; voz 114/114 (1 549 + 2 550 créditos; la cuenta 1 se agotó y siguió sola la cuenta 2 de respaldo), `seleccionar` sin fallos, `tiempo` 809,1 s (13:29) |
| 2 | Prompts + Flow (escenarios + hojas con ciclos + utilería) + recorte + profundidad + pegatinas reales de WoW + clips yt + SFX del juego + Lyria | ✅ 20-oct | tanda 1 (0-3:06) + tanda 2 (horgus…cierre) y Lyria 1-7 (ver «En curso») |
| 3 | Escenas 0:00-2:30 + sfx + mezcla + montaje | ✅ 20-oct | 27 tomas 0-186 s + sfx + fx del juego + mezcla (-14,3 LUFS) + `video --hasta 180` → AVANCE revisado (cuadro cada ~10 s y hojas de rigor cada ~3 s) |
| 4-7 | Escenas 3:06-13:29 + montaje completo | ✅ 20-oct | ~85 tomas de la tanda 2 en una sola sesión (el usuario: «termínalo todo en esta sesión») |
| 8 | Render → revisión MASTER → miniatura → youtube.json → subir → cierre | ✅ 21-oct | MASTER rehecho 2 veces (3 bloqueos del rigor + fondos pisados en 0:47-2:40); subido paQ5FISMZzU, programado jue 22-oct 09:00 CDMX |

## En curso (sesión 3, 20-oct ~21:00) — el usuario: «termínalo todo en esta sesión»
- Lyria 4-7 ✅ (`musica`, 0,32 US$; tramo 4 bloqueado 1 vez por el filtro y pasó al reintento; sin huecos de silencio).
- Flow tanda 2 ✅ (proyecto «oct 20 - 21:02», 44 prompts `T2_*` de `_prompts.py`, `_bundle_t2.js`; 86 imágenes + monstruos
  reintentada: «Flow está recibiendo un gran número de solicitudes» en 1 prompt). Recorte ✅ (davil 6, horgus 5, marduk 5, galope b→a 6,
  rutagrana 5, cromi 6, aventurero 6, pamela_corre 8, reencuentro 6, utileria2 18, monstruos 7), profundidad ✅ (66 + 9 variantes b).
- Reales nuevos: cromi, cromi_dragon, medallones davil/horgus, iconos Wowhead (muñeca y piezas, anillo, Anales). SFX del juego nuevos
  con `_bajar_sonidos.py` (luz sagrada, DK, reloj de arena, cofre, susurros, mundo de los espíritus…).
- Escenas 186 s → 809 s ESCRITAS en escenas.py (tanda 2, ~85 tomas) y revisadas en hojas 640x360 cada ~5 s. Falta: sfx → fx → mezcla →
  revisión cada 3 s → render completo (conservar 0-180 s) → final → verificar → MASTER → miniatura → youtube.json → subir.
- Conciliado 20-oct 22:15 (la sesión se cortó sin anotarlo): sfx + fx + mezcla ✅ (21:40, `audio/final.wav`) · `youtube.json` ✅
  (21:42) · `salida/miniatura.jpg` ✅ (21:44, `_miniatura.py`) · render completo LANZADO y CORTADO a las 22:12 sin procesos vivos:
  109/270 segmentos (0-5:27); `seg_0109…0120.mp4.tmp.mp4` son restos a medias. Falta: reanudar render (161 seg., ~50 min) →
  final → verificar → rigor del MASTER → subir y programar (hueco de Halloween) → registrar → cierre.
- 20/21-oct (sesión 4): render reanudado ✅ (161 seg. en 2 654 s) · final ✅ (MASTER 13:49 con pantalla final, 3,4 GB) · verificar ✅
  (CER 0,0023; 3 frases >2 % son nombres que Whisper oye mal: «Viladaro», «Brutagrana», «Pilla barro») · RIGOR del MASTER cada 3 s
  (3:01-13:49) → 3 bloqueos ARREGLADOS en escenas.py: mu2 aventurero duplicado (paseo sin `hasta_despues=False` + quieto),
  r6 título «LA PARTE MÁS CRUEL» chocaba con el rastreador (ahora sale en t_liberar-0,6), b1 bolsa tapaba la cara (W*0,70 → W*0,36).
  `conservar(range(0,270))` + `video --rehacer 432.5-441 588.5-593.5 599.5-603` → final → verificar EN MARCHA.
  Hueco elegido: jue 22-oct-2026 09:00 CDMX (15:00 UTC; panel: Warcraft sin video desde el 22-oct, nada programado tras el 19-oct).
- ⚠ 21-oct ~07:40 (sesión «Video Wow Darrowshire»): el usuario vio en 1:55 el lago de los fantasmas en vez del mapa. CAUSA: la tanda 2
  redefinía nombres de módulo que leían tomas viejas → R1-R6 (planos de la Plaga q1-q6), t_lago (p1), t_antes (a4), t_asi (q6).
  Renombrados (RQ1-RQ7, t_lagoR, t_antesT, t_asiZ; comprobación AST: 0 duplicados). EL MASTER ACTUAL NO SE SUBE. En marcha
  (`scratchpad/rehacer.sh`, espera a que acabe el `final` ajeno): conservar 0-269 → `video --rehacer 46.8-56.4 90.4-127.7
  150.7-156.1` → final → verificar → revisar 0:47-2:40 → subir.
- 21-oct 08:03 (sesión «Video Darrowshire»): `rehacer.sh` ✅ (20 seg. en 441 s; final 13:49 + verificar CER 0,0023, los mismos 3
  nombres). Revisión: 0:00-3:00 del MASTER IDÉNTICO al AVANCE aprobado (180 cuadros a 1 fps, dif. media 0,0; la misma prueba entre
  dos instantes distintos da 39) · 1:55 ya enseña el mapa de la Plaga · mu2, r6 y b1 arreglados · unión 3:00 y pantalla final ✅.
  La sesión «Video Wow Darrowshire» se despertó al acabar su script y SUBIÓ (paQ5FISMZzU, publishAt ✅) pero se cortó antes de
  miniatura/.srt/registro → `yt aplicar` (miniatura + .srt «Español») y registro en canales/cronicas_warcraft.json + BITACORA.

## Decisiones con el usuario (20-oct-2026)
- Formato NUEVO para Warcraft: el del asteroide (Flow pinta, el código anima pegatinas) con pegatinas de Warcraft, imágenes de Flow,
  clips de YouTube si hace falta, SFX DEL PROPIO JUEGO y Lyria de terror. Historia de lore oscura y poco contada.
- Stalvan descartado: el canal ya lo contó (nov-2025, fCKVPqG7Yxc, ×0,67). Elegido Darrowshire (Pamela Redpath). Referencia de datos:
  «El Secreto Oscuro de Desolace: ¡Una Tragedia Familiar!» (×2,1, 11 420).
- Voz ElevenLabs, «la misma del último video de terror» = voz 11 del asteroide (`HNSF1CTQmub252yhXROX`), SUPUESTO dicho al usuario.
  El usuario recarga saldo. Duración: 12 min MÍNIMO. Sin Overgear (campaña en pausa, como en wow_tres_noches).
- CTA del formato nuevo (pedido del usuario): a la mitad y al final, «si te gusta este estilo, comparte y comenta para seguir con más
  lore e historias oscuras así».

## Sesión 2 (20-oct-2026) — resumen
- Voz Lily completa el 20-oct (`PARCIAL_HASTA = None`). `tiempo` 809,1 s: gancho 0-47,3 · pueblo -90,9 · plaga -127,3 · asedio
  -170,9 · horgus -225,5 · marduk -283,6 · cta_mitad -312,7 · despues -363,6 · pamela -421,8 · muneca -461,8 · anillo -501,8 · cromi
  -538,2 · reliquias -600,0 · batalla -680,0 · te -730,9 · cierre -809,1 (0-225,5 igual que en el AVANCE: sigue valiendo).
- Flow tanda 1 = `_prompts.py` (proyecto «oct 20 - 17:29»); intercambiadas a↔b: casa_rutagrana, villa_calle, esqueleto_camina,
  plaga_hoja. Render 0-180 s: 60 segmentos en 1 125 s con 12 procesos (~2,3 s/cuadro por proceso).

## Plan visual (para el tramo 2; wiki.gg bloquea curl → mirar los modelos reales con el navegador integrado en Wowhead)
- Fondos de Flow (~45, uno por lugar/hora; nada repetido entre escenas): posada del camino a Stratholme (noche, vela) · Peste del Este
  · ruinas de Villa Darrow (anochecer, noche, alba, final) · Villa Darrow viva junto al lago Darrowmere · casa Rutagrana (día /
  noche-escondite / ruina / té) · plaza (día / duelo / ruinas-noche / alba) · graneros de Andorhal · casa del enfermo · mapa pintado de
  Lordaeron (mancha de tinta por código) · Stratholme ardiendo · barricadas · colinas de noche · puerta del pueblo · campo de humo ·
  pueblo ardiendo · escritorio con vela y los Anales (CTA) · camino de la Plaga · granero de Gahrron · casa de Marlene (fuera/dentro) ·
  ruinas por dentro x2 · cementerio de Andorhal + monumento · posada en ruinas de Andorhal · ayuntamiento · Capilla de la Esperanza
  de la Luz · lago de los fantasmas · Vega del Amparo · bosque apestado · Vista Eterna (nieve).
- Hojas: pamela (6 poses) + pamela_corre (ciclo 8) · joseph (6) · rutagrana_corrompido (4) · marlene (4) · familia (Carlin, Jessica)
  · davil (5) · horgus (4) · marduk (4) + caballo esquelético galope (6) · cromi (5) + dragón de bronce · defensores (6) ·
  necrofagos (6) + necrofago_corre (8) · esqueletos (6) + esqueleto_camina (8) · aldeanos (6) · cuervos aleteo (6) · utileria x2
  (muñeca entera + cabeza + lado izq. + lado der., alianza, Anales, Fardo de reliquias, tetera y taza, llave, cofre, escudo, tratado,
  espada rota, cráneo, cama con dosel, sacos de grano, caldero de peste, lápida, barricada) · fuego/humo/niebla verde.
- FANTASMAS por código (no en Flow): la pieza viva teñida azul-verde, translúcida, con halo y temblor (Pamela, Joseph, Marlene,
  defensores) → misma cara viva y muerta.
- Pegatinas REALES de WoW (regla del canal): modelos de Pamela, Joseph, Rutagrana el Corrompido, Marduk, Horgus, Davil, Cromi,
  Carlin, Marlene + iconos de Wowhead (muñeca, alianza, Anales, Té con azúcar, Fardo de reliquias) con `mg_wow.icono`.
- Clips yt-dlp (dentro de un marco con profundidad, nunca pantalla plana): posada de La Matanza de Stratholme con la familia,
  ruinas de Villa Darrow en Classic, el evento de la Batalla de Villa Darrow, Pamela entregando la misión.
- SFX del juego: aceptar/completar misión, fantasmas, necrófagos, campanas, Cromi (arena del tiempo); de wow.zamimg.com / clips.
- MG NUEVOS propuestos (regla del 19-oct): (1) ventana de misión Classic en pergamino con el texto en español y la recompensa
  («La muñeca de Pamela», «Té con azúcar»); (2) árbol de la familia Rutagrana con quién sobrevivió (vuelve al final); (3) mapa de la
  cadena de misiones (Andorhal → Capilla → lago → Vega del Amparo → granero → Villa Darrow) en tinta; (4) dos líneas del tiempo de
  Cromi (original / reescrita: «lo que ya pasó tiene que volver a pasar»); (5) bolsa de WoW que se llena con las reliquias hasta
  formar el Fardo.

## Piezas (mapa número → pose, tanda 1)
- pamela_hoja 00 sentada jugando/01 abraza muñeca/02 saluda/03 agachada con miedo/04 de pie triste/05 camina · joseph_hoja 00 dormido
  /01 de pie/02 de rodillas con niño/03 espada en alto/04 señala/05 camina · familia 00 Jessica/01 Marlene/02 Marlene de rodillas/
  03 Carlin espada/04 Jessica saluda/05 Carlin brazos cruzados · aldeanos 00 saco/01 cesta/02 herrero/03 anciano/04 niño corre/
  05 carretilla · defensores 00 soldado lanza/01 paladín martillo/02 miliciano horca/03 arquero/04 dos con tablón/05 antorcha ·
  plaga 00 enfermo en cama/01 se levanta/02 zombi/03 saco verde/04 carro/05 rata · esqueletos 00 espada/01 hacha/02 arquero/03 se
  arrastra/04 se deshace/05 estandarte · utileria 00 muñeca/01 vela/02 barricada/03-04 saco/05 escudo/06 espada/07 horca/08 antorcha/
  09 libro/10 farol/11 estandarte/12 brasero/13 cubo/14 rueda/15 caballito/16 flechas · fx 00-02 fuego/03-04 humo/05 niebla verde/
  06 bruma azul/07 brasas/08 icor · ciclos: esqueleto_camina 8, necrofago_corre 8, jinete_galope 6, cuervos_aleteo 6.

## Hecho
- `nuevo` + `canales --actualizar` (20-oct): Warcraft URGENTE desde jue 22-oct; el que se queda antes sin video es Edsonxn (hoy).
- Lore verificado con fuentes (docstring de guion.py; IDs de misión y nombres es-ES de la API de tooltips de Wowhead:
  `https://nether.wowhead.com/classic/tooltip/quest/<id>?locale=6`, también `/npc/<id>`).

## Lecciones de este video (solo lo no obvio)
- Lily (eleven_v4) ≈ 0,43 créditos/carácter con corchetes; 41 frases (0-4:42) = 1 549 créditos. Whisper oye «Villadarro»,
  «Josef/Josep», «Jorgos», «Lordoran», «Darumir», «Ruta verana», «Orgus», «Chromie», «Villa Barrow/Villavarro» → ALIAS_QA (ya en guion.py).
- Lily NO dice «gnoma» (salió «ñoma», «manioma» con 2 semillas) → «Tiene forma de gnomo». «encuentres su» funde las eses → CER_MAX_POR_FRASE.
- SFX reales del juego desde Wowhead (`/sounds/name:<texto>`, curl sin bloqueo) y fantasma por código: ver docs/estilo_pegatina_flow.md §8.
- El ciclo `esqueleto_camina` salió con figuras pegadas (cortes rectos): en a2 van títeres de `esqueletos_hoja`.

## Cierre (regla del 12-oct-2026)
- [x] subido, miniatura, programado y registrado (`canales/cronicas_warcraft.json` con `formato`, BITACORA) — 21-oct
- [x] HALLAZGOS documentados (docs/estilo_pegatina_flow.md § 8: nombres únicos por tanda, `paseo`+`quieto`, choques de interfaz,
  comparación AVANCE↔MASTER; canales/formula/cronicas_warcraft.md: conclusión del 20-oct y qué medir el 29-oct) — 21-oct
- [ ] Medir el 29-oct-2026 (7 días): vistas vs mediana 5 239 y % visto · `python fab.py wow_darrowshire limpiar` al aprobarlo (3,4 GB de segmentos)
