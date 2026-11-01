# Jalpa: el pueblo que echó a su encomendero — ESTADO
- canal: bitacora_perdida · hueco del canal: sáb 24-oct-2026 14:00 (si la prueba gusta y se completa el video)
- estilo: pegatina_flow (NUEVO, 20-oct-2026) → doc: docs/estilo_pegatina_flow.md · kit: nucleo/pegaflow.py · ejemplo: este video
- etapa: MASTER TERMINADO (20-oct): `salida/jalpa_MASTER.mp4` 1080p 3:23 (203,4 s), CER 0,07 %, desfase 0; revisados 68 cuadros
- ✅ **PÚBLICO** desde el sáb 24-oct 14:00 CDMX · https://youtu.be/Ae7B03_QMDw (verificado en YouTube el 28-oct-2026; registrado en canales y BITACORA). Siguiente paso: nada de producción; tras 7 días, `python fab.py yt metricas <alias> 90` para ver cómo rindió.
  (previews/rev/), 3 arreglos (rumbo de 6 pegatinas, mula encima del arriero, máscara sobre el tastoán). Miniatura
  `salida/jalpa_mini_flowA.jpg` (Flow, «JALPA / ¡FUERA, ENCOMENDERO!») y `youtube.json` con capítulos y fuentes.
- youtube: Ae7B03_QMDw · privado, PROGRAMADO sáb 24-oct-2026 14:00 CDMX (2026-10-24T20:00:00Z) · miniatura + .srt subidos;
  registrado en canales/bitacora_perdida.json y BITACORA (20-oct).
- siguiente: nada de producción. Al aprobarlo el usuario: `python fab.py jalpa limpiar` (segmentos/ = 927 MB). Tras publicarse:
  métricas a los 7 días para decidir si la fórmula «pegatina Flow + un suceso con personajes» sigue en la serie de la carretera 54.

## Sesiones (plan de tramos · «continúa el video jalpa» retoma aquí · protocolo docs/sesiones.md)
- alias: jalpa, el de Jalpa, prueba de pegatinas Flow
- vista previa: la prueba de 1 min ES la vista previa (con audio completo: voz + Lyria + SFX + mezcla)
- leer al empezar: este ESTADO.md y docs/estilo_pegatina_flow.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | Prueba 1 min: guion, voz, Flow (escenarios + hojas con ciclos), kit pegaflow, escenas, audio, render | ✅ 20-oct | 54 s; MASTER 1080p verificado (CER 0, desfase 0); APROBADO. Cerrado con la ventana de 5 h al 92 % |
| 2 | Investigación + guion de las escenas 5-10 + voz + Flow (escenarios y hojas nuevas) + recorte | ✅ 20-oct | 545 palabras, voz 173 s, video 203,4 s; 28 prompts → 12 escenarios + 16 hojas; fuentes en el docstring de guion.py |
| 3 | Escenas 5-10 en escenas.py + montaje vivo con audio (Lyria 2 tramos, sfx, mezcla) | ✅ 20-oct | 37 tomas nuevas, retratos reales (Alvarado, Mendoza, Hidalgo); montaje_vivo.mp4 con audio mandado; ventana 5 h al ~70 % |
| 4 | Render completo → revisión MASTER → miniatura Flow → youtube.json → subir privado (preguntar) → cierre | ✅ 20-oct | render 21 min; 3 arreglos tras revisar 68 cuadros; miniatura Flow; subido privado Ae7B03_QMDw, programado sáb 24-oct 14:00 |

## Plan del video completo (~3:50; las 4 escenas de la prueba quedan como están, 0:00-0:54)
- 5 `mixton` (~35 s): Tenamaxtli y los peñoles; Pedro de Alvarado muere (1541); el virrey Mendoza con un ejército enorme; el peñol cae
  (1541-1542). Giro con cuidado: según Ernesto Juárez Frías (nuestrosranchos.org/node/23306), en nov-1541 Petacatl dejó a los sitiados
  del peñol de Nochistlán (UNA fuente: decirlo como «según el historiador…»). Coherente con videos/juchipila y videos/apozol.
- 6 `santiago` (~30 s): tras la guerra, Santiago de Xalpa (1542, escudo: crwflags), primeras iglesias desde 1542 (Wikivoyage), bajo la
  jurisdicción de Juchipila (tesis UNAM 1939), mestizaje.
- 7 `mineral` (~30 s): minas La Leonera y Monroy, «Jalpa Mineral»; la jalpaíta (mineral de plata y cobre) lleva el nombre de Jalpa
  (verificar en mindat/AZoMining).
- 8 `hidalgo` (~25 s): Hidalgo pasa por Jalpa el 18-ene-1811 tras la derrota de Puente de Calderón (Wikipedia EN: VERIFICAR con otra
  fuente; si no se confirma, «en su huida hacia el norte»). Retrato REAL de Hidalgo como pegatina (dominio público).
- 9 `franceses` (~20 s): 1864, unos 300 soldados franceses ocupan la plaza (Intervención; verificar).
- 10 `hoy` (~35 s): Señor de Jalpa y parroquia de San Antonio, tastoanes del 25 de julio, rollos de guayaba, la carretera 54, ~15 mil
  habitantes en la cabecera (censo 2020: 15 291 según Wikipedia ES; confirmar si es cabecera o municipio). NO afirmar Pueblo Mágico sin
  el catálogo de Sectur. Cierre: «Esto fue Bitácora Perdida» + «¿qué pueblo sigue?» con el mapa de la 54.
- Flow nuevo (misma FICHA): escenarios peñol con asedio / campamento del virrey / iglesia en obra 1542 / bocamina con malacate /
  camino al anochecer con la columna insurgente / plaza de 1864 / Jalpa hoy (plaza y templo) / fiesta de tastoanes. Hojas: Tenamaxtli,
  Alvarado, Mendoza, soldados y aliados (ciclo de marcha), fraile, mineros (ciclo con carretilla), insurgentes a caballo, soldados
  franceses (ciclo de marcha), gente de hoy, tastoanes (ciclo de danza), utilería (guayabas, rollo de guayaba, pico, mineral, campana).
- Lyria: 2 tramos (0:00-~2:00 y ~2:00-fin) por API (0,16 US$); la prueba usó 1 tramo de 54 s (rehacer con el guion completo).

## En curso (checkpoint por si la cuenta se agota: docs/sesiones.md §6; bórralo al cerrar el tramo)
- (vacío: tramo 4 cerrado el 20-oct)

## Decisiones con el usuario (20-oct-2026)
- Siguiente pueblo de la serie: Jalpa. Duración del video completo: ~4 min. Vista previa con audio completo: sí.
- «Quiero probar nuevo formato, nuevo estilo y fórmula»: Flow crea escenarios + hojas de personajes/elementos (Nano Banana 2.1); a cada
  personaje, su secuencia de cuadros (caminar o la acción que haga falta) EN LA MISMA IMAGEN; el código los anima como pegatinas.
- «Quiero ver el montaje mientras vas armando»: `_vivo.py` → previews/montaje_vivo.mp4 (mandado n.º 1 mudo y n.º 2 con audio).
- 2K de Flow: abre «Guardar como» por imagen y el usuario no quiere aceptarlas → se queda en 1K (las 11 que ya guardó, en `hd/`).
- Música: Lyria 3.5 por API (el usuario recargó crédito el 20-oct; 0,08 US$ por pieza; Clip 30 s = 0,04 US$).

## Hecho
- Flow (proyecto «oct 20 - 10:09», Nano Banana 2.1 · 16:9 · x2 = 0 puntos): 13 prompts (`prompts.json`) → `imagenes/` (5 escenarios) y
  `hojas/` (8 hojas); variantes `_a`; 2K de 11 en `hd/`. Piezas en `piezas/<hoja>/` (cuantas.json), profundidades en imagenes/depth.
- Voz Dan (Chatterbox): 11 frases CER 0, 54,0 s. Lyria 3.5: `audio/lyria_tramo1.mp3` → musica.wav. SFX 40 eventos. Mezcla −14 LUFS,
  voz/fondo 11,5 dB. 11 tomas en `escenas.py`; revisión de 18 cuadros (1/3 s) sin defectos bloqueantes.

## Material del video completo (tramo 2, 20-oct) → para escenas.py en el tramo 3
- Escenarios nuevos (`imagenes/<x>_a.jpg`): penoles_dia, campamento (mixton) · iglesia_obra, santiago_xalpa (santiago) · mina_dia
  (mineral) · mina_tarde = la MISMA tienda de raya con balcón al anochecer, camino_tarde (hidalgo) · gabinete (alemán 1858), plaza_1864
  (franceses) · jalpa_hoy (la b de Flow, torres desiguales como el templo real), fiesta_calle, canon_hoy (agave + carretera; cierre).
  Ya existía `penol` (atardecer rojo, prueba). Referencia real del templo: Commons «Templo del Señor de Jalpa.png».
- Piezas (`piezas/<hoja>/NN.png`): alvarado_hoja 00 espada en alto · 01 señala · 02 trepa · 03 caído · 04 a caballo |
  mendoza_hoja 00 calma · 01 ordena · 02 mapa · 03 alto · 04 a caballo | tenamaxtli_hoja 00 guardia · 01 grita puño · 02 arco ·
  03 lanza piedra · 04 tras escudo | colonia_hoja 00 fraile · 01 albañil con adobe · 02 colono azada · 03 madre mestiza · 04 mujer
  con maíz · 05 niño campana | mineros_hoja 00 pico · 01 costal · 02 capataz libreta · 03 tortillera · 04 arriero · 05 niño farol |
  hidalgo_hoja 00 cansado · 01 arenga brazo en alto (balcón) · 02 señala norte · 03 bastón · 04 a caballo | insurgentes_hoja
  00 bandera · 01 herido · 02 soldadera · 03 jinete lanza · 04 honda · 05 niño tambor | siglo19_hoja 00 mineralogista lupa ·
  01 mineralogista escribe · 02 oficial francés · 03 mujer rebozo · 04 hombre brazos cruzados · 05 niña tras barril | gente_hoy
  00 abuela dulces · 01 vaquero · 02 chica teléfono · 03 niño bici · 04 peregrina vela · 05 Santiago a caballo (tastoanes) |
  utileria_2 00 jalpaíta · 01 barra de plata · 02 pico · 03 farol · 04 lupa · 05 roca · 06 costal · 07 vagoneta · 08-09 campanas ·
  10 cañón · 11 quepí · 12 fusil · 13 cruz · 14 rollos de guayaba · 15 guayabas · 16 agave · 17 máscara de tastoán.
- Ciclos (`ciclo_NN.png`): soldado_marcha 8 · aliado_marcha 8 · insurgente_camina 8 · frances_marcha 8 (la b de Flow) ·
  tastoan_danza 8 (la b; saltos: altura variable) · mula_camina 6.

## Lecciones de este video (solo lo no obvio)
- `python fab.py nuevo --help` NO muestra ayuda: crea un video llamado «--help» (borrado; quitar junctions con `cmd /c rmdir`).
- Chatterbox NO aplicaba FONETICA (tts_gen.py usaba la grafía real) → arreglado en el núcleo; afectaba a Tamriel y Runa Caída.
- «Petacatl»: Chatterbox pone vocal de apoyo en la «tl» final (Petacatel/Petacatil) → ALIAS_QA; «Petacati» (sin ele) = mala.
- Whisper escribe «Halpa» por «Jalpa» (jota suave): ALIAS_QA. «pagarla» → Whisper «pagar la»: reescribir sin clítico.
- La mezcla final es `audio/final.wav` (no mezcla.wav).
- AI Studio web ya NO da Lyria gratis (403, icono key_off): hace falta crédito en la API.
- Tenamaxtli: Whisper oye «Tenamasti / Tenamastí / Tenamaxtile / Tenamazli» → ALIAS_QA (la toma elegida dice «Tenamazli»).
- Para otras épocas con la MISMA FICHA (que dice «1540»): «Same art style, but this picture is set in <año>: <qué>.» tras la ficha
  funcionó en todos (1800, 1811, 1858, 1864, hoy) sin perder el trazo.
- Flow puso un ciclo de 16 en 2 filas (frances_marcha_a) y una línea de suelo bajo la danza (tastoan_danza_a): elegir la b.
- Hidalgo en Jalpa: el dato fino (balcón de la tienda de raya de La Leonera, Portal Quemado) es de la compilación de cronistas del
  cañón (La Jornada Zacatecas, 2021); da para enlazar mina → Hidalgo → jalpaíta en la misma escena-lugar.
- Lyria puede devolver una pieza MÁS LARGA con un hueco de silencio dentro (tramo 2: 144 s = 94 s de música + 26 s de silencio + 24 s):
  mirar el perfil de volumen antes de `armar`; aquí bastó usar los primeros 95 s (ya traían su cierre) como `lyria_tramo2.wav`.
- `PF.T(…, "un")` casa también con «uno»: anclar con n=1 o con la palabra siguiente; «san» casa con «santuario».
- Baskervville no tiene «→» (sale un cuadro): rótulos sin flechas. Sus cifras son de estilo antiguo («45o»): aceptado (ya en la prueba).
- Ciclos (`ciclo_NN.png`) van en lienzo común con margen: el personaje sale ~25 % más chico que `frac` → subir el factor (tastoanes ×1,7).
- Montaje (usuario, 20-oct): «se ve perfecto», salvo 6 pegatinas que caminaban de espaldas a su rumbo (Hidalgo a caballo ×2 y a pie,
  Mendoza a caballo ×2, Santiago) → `MIRA` + `rumbo()` en escenas.py; comprobado en previews/rumbo.jpg.
- Retratos reales como pegatina: `_retratos.py` los enmarca (madera + filete dorado) en piezas/retratos/; `pega()` en pantalla.

