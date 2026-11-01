# El asteroide que NO vimos venir — ESTADO
- canal: kuriox · hueco: mar 27-oct-2026 14:00 (panel de canales del 20-oct)
- estilo: FUSIÓN Kuriox (Kurzgesagt espacial) + pegatina_flow → docs/estilo_pegatina_flow.md · ejemplo: videos/jalpa/ (+ sol_apagado_8min para MG)
- etapa: guion ✅ · voz ✅ (voz 11 `HNSF1CTQmub252yhXROX`, 50/50 CER 0) · tiempo ✅ (5:41) · Flow ✅ · recorte ✅ · profundidad ✅ · Lyria ✅ (3 tramos) · escenas 0-341 s ✅ (s1-s58) · sfx ✅ (188 eventos) · mezcla ✅ (−14,15 LUFS, voz +10,2 dB) · montaje ✅ completo · MASTER ✅ (CER 0, rigor OK) · subido ✅
- ✅ **PÚBLICO** desde el mar 27-oct 14:00 CDMX · https://youtu.be/KQdki-Rq-2w (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
- siguiente: NADA de producción. ✅ SUBIDO y PROGRAMADO mar 27-oct-2026 14:00 CDMX (KQdki-Rq-2w, https://youtu.be/KQdki-Rq-2w). Pendiente: tras el estreno, métricas (`yt metricas kuriox`) y `limpiar` cuando el usuario lo apruebe (segmentos/ 1,5 GB)

## Sesiones (plan de tramos · «continúa el video asteroide_invisible» retoma aquí · protocolo docs/sesiones.md)
- alias: asteroide_invisible, el del asteroide, el de terror de Kuriox, el meteorito
- vista previa: SÍ, el primer minuto renderizado con audio completo (voz + Lyria + SFX + mezcla) tras el tramo 2
- leer al empezar: este ESTADO.md y docs/estilo_pegatina_flow.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Guion + voz ElevenLabs + prompts y Flow (escenarios + hojas) + recorte | ✅ 20-oct | 50 frases CER 0, 5:29; 56 imágenes, 89 piezas, 17 profundidades |
| 2 | Escenas 0:00-2:30 + Lyria/SFX/mezcla → vista previa del 1.er minuto con audio | ✅ 20-oct | Lyria 3 tramos (0,24 US$); s1-s8 = 0-62 s (voz 11 aprobada); s9-s25 = 62-158 s (Cheliábinsk, observatorio, sala de crisis, ×100 bombas); hoja de rigor cada 3 s OK; montaje en el panel + `previews/montaje_0-2m38.mp4` con audio (enviado al usuario) |
| 4 | Notas del montaje 2:38-5:41 + render + MASTER + subida | ✅ 20-oct | s3 pulido; montaje 2 aprobado; render 1080p (35 min) + `final` + `verificar` (CER 0, desfase 0); rigor: 114 cuadros cada 3 s + hoja 2×3 OK, negros intencionales < 2 s (`blackdetect`); youtube.json + miniatura Flow «NADIE LO VIO»; DOI en Crossref; subido y PROGRAMADO 27-oct 14:00 CDMX sin preguntar (regla nueva del usuario, docs/publicacion.md) |
| 3 | Escenas 2:30-5:00 + montaje vivo con audio | ✅ 20-oct | montaje 0-2:38 aprobado («bien, sigue»); s26-s58 (alerta→cierre, 33 tomas) revisadas en hojas y corregidas; sfx+mezcla; 🎞 Montaje completo + `previews/montaje_2m38-5m41.mp4` enviado al usuario |

## Decisiones con el usuario (20-oct-2026)
- Kuriox con su estilo espacial FUSIONADO con pegatina Flow (jalpa). Hipótesis de impacto de un asteroide no detectado; el escenario
  más catastrófico REALISTA; varias perspectivas (astrónoma, agencias, persona normal). TERROR de verdad: miedo, pánico. ~5 min.
- 4 sesiones · vista previa del 1.er minuto · voz ElevenLabs con corchetes (BRAULIO, «brooding», es) · SIN Kuri (terror puro).

## Fusión de estilos (cómo)
- Flow (Nano Banana 2.1, 1K, x2) pinta con la FICHA de guion.py: explicador espacial tipo Kurzgesagt (geometría limpia, degradados,
  brillos) en clave de terror (navy/índigo/teal desaturado + UN acento rojo-naranja). Escenarios vacíos + hojas con ciclos.
- El código (pegaflow) anima las pegatinas y añade los motion graphics de Kuriox: órbitas, trayectoria, contador de horas, % de
  impacto, anillos de daño, onda expansiva, destello que quema la imagen, polvo y brasas. Ritmo Kuriox: nada quieto > 2 s.

## Plan de tomas (escenario elegido · pegatinas `hoja/NN` · motion graphics por código)
- gancho: `espacio_tierra_a` empuje lento; `asteroide_hoja/00-02` a la deriva con borde de luz del Sol; «miles de rocas» → enjambre
  de puntos-roca; «no sabemos dónde» → se apagan y solo parpadean contornos. «Todavía» = corte a negro + destello rojo.
- ciegos: `sistema_solar_a` + órbitas MG; contador 25 000 (> 140 m); 40 % hallados (teal) / 60 % fantasmas rojos; 2019 OK = trayectoria
  entre la Tierra y la Luna, rótulo «2019 OK · ~100 m · 1 día antes»; cono ROJO de la Tierra al Sol = «PUNTO CIEGO».
- cheliabinsk: `cheliabinsk_b`; bólido `asteroide_hoja/04` desde el Sol con estela de humo (`fuego_humo/04-06`), destello blanco;
  `gente_hoja` en ventanas; anillo de onda → `utileria/06` (ventana) revienta; rótulo «CHELIÁBINSK · 2013 · 20 m»; «imagina una de
  400» = barra de escala 20 m vs 400 m (silueta de rascacielos).
- punto: `observatorio_a` → `sala_observatorio_b`; `astronoma_hoja/00` ante los monitores con cielo MG y un punto que NO se mueve y
  crece; `/01` mano en la boca; rótulo «400 m»; cuenta atrás roja gigante 20:00:00.
- numeros: `sala_crisis_a`; pantalla con % MG 1→10→60→100 al ritmo de latido; `funcionarios_hoja/00,04,05`; barras «DART: 10 MESES»
  vs «20 HORAS» con `utileria/05` (cohete); «5 000 MEGATONES» + rejilla de 100 hongos.
- alerta: `recamara_a` 4 a. m., `utileria/00` (teléfono rojo) vibrando, `persona_hoja/00`; `ciudad_noche_a` con sirenas y anillo
  «90 km»; `autopista_b` con `vehiculos` atascados, `persona_corre` y `mujer_corre` por el arcén; → `sala_mediodia_a`.
- destello: `sala_mediodia_a`: el punto rojo crece → blanco total, segundo sol; `utileria/08` (tendedero) humea; `persona_hoja/04`
  contra la pared; sismo = sacudida fuerte; «nada» = polvo flotando, silencio.
- silencio: `calle_mediodia_a`: `gente_hoja` sale a mirar (adolescente grabando, mujer señalando, anciano); `aves_aleteo` huyen;
  reloj `utileria/14` con 4:30 MG; la onda = látigo a `calle_destruida_b` con escombros volando (`utileria/10,11`, vidrios).
- zona_cero: `zona_cero_a` con anillos MG «7 km» y «30 km»; `columna_a` con columna creciendo, `fuego_humo`, rocas encendidas cayendo;
  «fin de tu mundo» = `persona_hoja/02` agachado entre ruinas.
- peor: `sistema_exterior_a`, cometa `asteroide_hoja/05` entrando rápido; `marte_b` con el cometa rozando, rótulo «SIDING SPRING · 2013».
- cierre: `espacio_tierra_a` + telescopio `utileria/04` en L1 con su cono teal sobre el punto ciego → `atardecer_a`: `persona_hoja/01`
  en la colina; una mota oscura sale del disco del Sol y crece… negro.

## Referencia de piezas y fondos (sesión 4, 20-oct)
- Fondos extra (variantes b, con profundidad): cheliabinsk_a, observatorio_b, sala_observatorio_a, sala_crisis_b, columna_b (hongo de
  la Tsar Bomba en s25 → en zona_cero, `columna_a` con encuadre MUY distinto). Mapa de piezas: astronoma 00 sentada/01 mano en boca/
  02 teléfono/03 señala/04 cabeza en manos; funcionarios 00 general tel./01 científica tableta/02 operador consola/03 soldado asustada/
  04 traje manos en cabeza/05 obrero sentado; gente 00 madre+niña/01 anciano/02 adolescente graba/03 mujer señala/04 niño osito/
  05 hombre maletín; utileria 00 tel. alerta/01 observatorio/02 antena/03 rover/04 JWST/05 cohete/06 ventana rota/07 paraguas/
  08 tendedero/09 semáforo/10 lámina/11 árbol/12 meteoro/13 sirena/14 reloj/15 binoculares; asteroide 00-02 redondas/03 angular/
  04 bólido (roca abajo-dcha., cola arriba-izq.)/05 cometa; fuego_humo 00-03 llamas/04-06 humo/07-08 polvo café/09,11 roca ardiendo/10 brasas.

## Hecho
- Voz 11 (`HNSF1CTQmub252yhXROX`, sesión 3): al usuario le gustó MUCHO la animación del 1.er minuto pero NO la voz BRAULIO; 7 muestras
  (`previews/muestras_voz/`, 328 créditos); `voz` 1 641 créditos (saldo ≈ 2 709; BRAULIO en `voz_braulio/`), numeros_3 rehecha (semilla 2),
  `tiempo` 341,1 s. Aprobado: «me gusta, continúa con lo demás». OJO: los segmentos de un render normal se REUTILIZAN aunque cambie la voz → `--rehacer`.
- Voz ElevenLabs BRAULIO (`dQafQNlqLLJDepKplzjl`, eleven_v4): 1 792 créditos en total (saldo ≈ 5 334). 4 frases rehechas (semillas
  2-3): «Y no sabemos…» (Whisper se comía la «Y»), «100.» suelto (inestable → «100 por ciento.»), un final cortado y «Si cae» → «Que
  caes» / «Pipas acerca» con `[sad]` delante (→ «Cerca de una gran ciudad, serían millones…»). `tiempo`: 329,1 s.
- Flow (proyecto «oct 20 - 12:25»): escenarios elegidos = espacio_tierra_a, sistema_solar_a, cheliabinsk_b, observatorio_a,
  sala_observatorio_b, sala_crisis_a, ciudad_noche_a, recamara_a, autopista_b, sala_mediodia_a, calle_mediodia_a, calle_destruida_b,
  zona_cero_a, columna_a, sistema_exterior_a, marte_b, atardecer_a (con `imagenes/depth`). calle_mediodia salió con cielo oscuro y un
  orbe rojo (no «mediodía azul»): se queda, funciona como la roca acercándose. `utileria` sin la nave DART (salió un rover; la variante
  b trae satélites si hace falta: recortar `utileria_b`).
- Guion con fuentes en el docstring de guion.py (NASA dic-2025, 2019 OK, Chelyabinsk, DART, NEO Surveyor, Siding Spring; números
  del impacto calculados con Collins et al. 2005).

## Lecciones de este video (solo lo no obvio)
- FICHA «Kurzgesagt + terror» en Flow (navy/índigo/teal + UN acento rojo-naranja) da fondos y pegatinas coherentes al primer intento.
- ElevenLabs: frases de 1 palabra/número («100.») salen inestables; `[sad]` al inicio metió un sollozo que Whisper oyó como palabra.
- `pegaflow.py recortar <v> hoja=N …` con argumentos SOLO procesa las hojas nombradas: las demás hay que nombrarlas también.
- FUSIÓN que funcionó (s1-s8): fondos de Flow con `PF.Plano` + MG por código en `escenas.py` (`trazo` = máscara cv2 + halo
  aditivo; `texto` Poppins con halo en vez de `PF.rotulo` de papel; `corriente`/`enjambre` de rocas; conos teal/rojo;
  `linea_punteada`; Luna dibujada por código). Rótulos en zonas oscuras, lejos de las trayectorias. Las coordenadas de cada escenario
  están en `ET_A/ET_B/SS_A/SS_B`.
- Un enjambre en órbita alrededor de un Sol fuera de cuadro casi no se ve: para «miles de rocas junto a la Tierra», usar una corriente
  en pantalla (`corriente`).
- Lyria: un tramo > 175 s se rechaza, así que hay que partirlo (aquí quedaron 3). El filtro bloqueó una vez el tramo 3 (400) y pasó al reintento.
- Pendiente de pulir: s3 (14,9-17,4 s) muestra la Tierra sin la roca 2,5 s; adelantar la aparición de la roca o meter el enjambre lejano.
- (sesión 4) `pegaflow` buscaba la profundidad como `<fondo>_a.png`: con fondos ya nombrados «espacio_tierra_a» no la encontraba y
  s1-s8 salieron SIN parallax (arreglado en el núcleo; al re-renderizar 0-62 s cambian un poco: `--rehacer 0-62`).
- La orientación de una pieza se mira en el PNG, no en la miniatura de `_indice.jpg` (el bólido 04 parecía al revés).
- Objetos a escala real más grandes que la pantalla (la roca de 400 m = 13 bloques): dibujarlos por código (`roca_gigante`: borde con
  armónicos altos + textura + cráteres pequeños junto al canto); una pieza de Flow ampliada 20× es una mancha y un borde senoidal
  suave parece una nube o un techo.
- Pantalla diegética que desborda el cuadro al acercar la cámara (s22): colocar cifra y diagrama en la parte VISIBLE, no relativos a la pantalla.
- Rejilla de 100 iconos (hongos): con celdas apretadas se leen como collares; filas alternas desplazadas + icono al 66 % de la celda.
- (tramo 3) Sobreexposición con `caja` sobre el ventanal = recuadro plano («página web») → `quemar()`; calima de 3 px ondula los
  marcos → 1 px; «MILLONES» rojo sobre humo café no se lee → `sombra_txt()`. Detalle en docs/estilo_pegatina_flow.md §7.
- Coordenadas del tramo 3 medidas con rejilla 10×10 (scratch): PUNTO28 (0.713, 0.395) ciudad_noche_a, GLOW29 (0.352, 0.39), PUNTO31
  (0.70, 0.34) autopista_a, PUNTO32 (0.76, 0.355) sala_mediodia_a, CRATER (0.50, 0.555, 0.225, 0.115) zona_cero_b, Marte_b limbo x≈0.60.

## Cierre (regla del 12-oct-2026)
- Lección de núcleo: un video recién subido llega con duración 0 (procesando) y `estadisticas.py` lo tomaba por Short → el panel no
  contaba el programado. Arreglado (dur 0 = sin decidir, cuenta como largo).
- [x] subido, miniatura, programado (mar 27-oct 14:00 CDMX) y registrado (`canales/kuriox.json`, BITACORA)
- [x] HALLAZGOS y mejoras documentados (docs/estilo_pegatina_flow.md §7 «cierre»)
