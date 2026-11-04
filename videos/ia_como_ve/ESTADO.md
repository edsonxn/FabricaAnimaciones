# ¿Cómo VE una Inteligencia Artificial? — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: kuriox (LARGO horizontal 1920x1080, ~9,5 min) · hueco: Kuriox ATRASADO desde el 31-oct → el siguiente hueco libre
- estilo: ACUARELA PINTADA A MANO POR CÓDIGO → docs/estilo_acuarela_pincel.md · kit copiado de videos/arenas_movedizas/ (adaptar de vertical a horizontal)
- etapa: voz ✅ (69 frases CER 0, 10:36, timeline.json) · planos a (gancho 0-35,5) y b (píxeles 35,5-95,5) PROBADOS en hoja · c (gato) y d (neurona) escritos SIN probar
- siguiente: SFX sintetizados + Lyria (biblioteca primero) + mezcla de 0-95 s → vista previa `video --hasta 95` con audio completo → tele; luego probar plano_c/plano_d con `_hoja.py`

## Sesiones (plan de tramos · «continúa el video ia» retoma aquí · protocolo docs/sesiones.md)
- alias: ia_como_ve, ia, cómo ve la IA, el video de la IA que ve imágenes
- vista previa: SÍ, el primer 1,5 min con audio completo (el usuario, 4-nov) · TODO SEGUIDO en una sesión (el usuario, 4-nov; si salta el corte de tokens, sesión nueva por el hook)
- leer al empezar: este ESTADO.md · `guion.py` (datos y frases) · docs/estilo_acuarela_pincel.md
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | guion + voz + tiempo + kit + planos a, b (c, d escritos) | ◐ parcial | 4-nov: voz CER 0; Whisper dio OOM/bad allocation intermitente: reintentar `seleccionar` basta |
| 2 | kit horizontal + planos c-k + música biblioteca + SFX + mezcla + render + subida | ✅ 4-nov | Todo seguido en una sesión (tramos 3-6 absorbidos); Lyria API sin saldo → biblioteca |
| 3 | planos neurona, capas (2:10-4:10) | ✅ 4-nov | dentro de la sesión 2 |
| 4 | planos aprender, ImageNet, parches (4:10-7:00) | ✅ 4-nov | dentro de la sesión 2 |
| 5 | planos palabras, trucos, cierre (7:00-9:30) | ✅ 4-nov | dentro de la sesión 2 |
| 6 | cierre: SFX sintetizados → Lyria (biblioteca primero) → mezcla → render → final → verificar → miniatura Flow → subir | ✅ 4-nov | dentro de la sesión 2 |

## ✅ CERRADO 4-nov-2026 · subido y programado
- MASTER `salida/ia_como_ve_MASTER.mp4` (10:36, 1080p, 460 MB) · `verificar`: CER 0,0005, desfase 0 ms · hoja `previews/master_hoja.jpg` sin bloqueos · enviado a la tele
- YouTube Kuriox: https://youtu.be/9brG5SuaYII privado, se publica **jue 5-nov 14:00 CDMX**, miniatura Flow aplicada; registrado en `canales/kuriox.json` y BITACORA
- Pendiente en Studio: subir el `.srt` a mano

## Lecciones
- Render largo con poca RAM (~3,6 GB libres): OpenCV OOM con 3 procesos → `video --procs 2` en bucle de reintentos (reaprovecha segmentos) terminó en 70 min
- `acuarela.rotulo` con `esc` diminuto daba tamaño 0 de fuente y tumbaba el render: tamaño mínimo 2
- `pegar`/recortes por cuadro: 35 piezas con `forma` = 4,4 s/cuadro; recortar y pegar en numpy = 0,9 s
- Datos reales en gráficas (ILSVRC top-5 2010-2015 y línea humana 5,1 %) y mapas de convolución reales con cv2 sobre la foto del gato
- Débil: la radiografía de la mano (dedos cortos) en `personajes_ia.radiografia`

## Historial del tramo (checkpoint 4-nov tarde)
- HECHO 2.ª sesión: Lyria API = 402 sin saldo → música de la BIBLIOTECA (guion.py: 5 tramos ≤175 s; arana_techo_1, cinco_bichos_2, arana_amarilla_2, sin_medicina_4, telarana_rota_1; ninguna oída en Kuriox) → audio/musica.wav 636 s · `sonidos_ia.py` (SFX sintetizados 0-95 s, 53 eventos; `sfx_proc.py` ya importa sonidos_ia) · `mezcla` ✅ (−14,3 LUFS, voz +14,9 dB) · arreglo en acuarela.rotulo (px mínimo 2: tumbaba el render)
- plano_c (cerebro real de acuarela, registro en tira aparte, pirámide + cerebro del gato que se enciende, Nobel) y plano_d (Kuri + calculadora diminuta con lupa, foto con el cuadrito antes del 3×3, «red de filtros» antes de LeCun) PROBADOS y corregidos en hoja
- `iconos_ia.py` NUEVO: torre(), piezas (esquina, curva, rayado, ojo, oreja, nariz, bigotes, cara_gato, rueda, alto), perillas, tostadora, perro/lobo/husky, panda, gpu, trofeo, personita, estrella, marca_x, palomita, volcan, bici, foto_cosa(nombre)
- plano_e (capas: apilar → torre con ventana redonda por piso → niña con lupa → «nadie le programó» con cara de gato y oreja marcada → ¿CÓMO?) PROBADO en hoja_e
- plano_f (aprender) PROBADO y corregido (hoja_f, hoja_f2) · SFX de c-f en `sonidos_ia_cf.py` (fx.wav: 195 eventos)
- AVANCE 0-94 s con audio completo: salida/ia_como_ve_AVANCE.mp4 → enviado a la tele (~14:00) con pregunta «¿Sigo así?» (respuesta en previews/_log_tele.txt)
- Tele: el usuario respondió «Sí, sigue» al avance (4-nov ~14:15) · plano_g (ImageNet), plano_h (parches y atención) , plano_i (palabras), plano_j (trucos: husky/lobo, panda/gibón) y plano_k (cierre, suscríbete) PROBADOS — TODOS LOS PLANOS HECHOS
- SFX g-k en `sonidos_ia_gk.py` (fx.wav 363 eventos) · `mezcla` final ✅ (−14,3 LUFS, voz +13,8 dB)
- 1.er render completo cayó por RAM (OpenCV OOM, segmento 34); 2.º también (seg 88, 92 de 170 hechos; solo ~3,6 GB libres); relanzado ~16:45 en bucle de hasta 8 reintentos con `video --procs 2` + `final` + `verificar` → log previews/_log_render.txt
- MINIATURA FLOW ✅ `salida/ia_como_ve_mini_flow.jpg` (prompt_miniatura.md) · youtube.json ✅ (capítulos, fuentes, créditos de fotos)
- FALTA en orden: revisar MASTER (hoja 2×3) → avisar/tele → `canales --actualizar` → `yt subir ia_como_ve kuriox private --publicar <hueco>` → registrar → cierre (docs, biblioteca catalogar, commit)
- Lyria: avisar al usuario que la API está sin saldo (402) — se usó biblioteca
- Detalle débil a mejorar: la radiografía de la mano (dedos cortos) en `personajes_ia.radiografia`

## Idea visual (voz → imagen)
- Kuri (el robot de Kuriox) ES la IA. Una niña chibi le enseña la foto de un gato; el viaje es POR DENTRO de la cabeza de Kuri.
- píxeles: zoom a la foto → cuadritos → cada uno con 3 números R/G/B; cascada de números; «36 000 000»; gato movido = números distintos
- gato 1959: Hubel y Wiesel (retrato REAL pasado a acuarela) + pantalla con una línea que gira y la neurona que «suena» solo en un ángulo
- neurona = calculadora con perillas; filtro 3×3 = lupa que barre la foto y deja el mapa de bordes; LeCun + cheque
- capas = TORRE de pisos dentro de la cabeza de Kuri: piso 1 bordes, 2 texturas, 3 partes (ojo, oreja, bigote), arriba «GATO»
- aprender: «¿TOSTADORA?» → error que baja por la torre y gira perillas (frío/caliente) → «¿PERRO?» → «¿GATO… CREO?»
- ImageNet: Fei-Fei Li (retrato real) + montaña de fotos + 49 000 personas en un mapa · podio 2012: 15 % vs 26 % · gráfica 2010-2015 cruzando la línea humana
- parches: la foto se corta en rompecabezas; hilos de atención entre piezas (pelo ↔ oreja ↔ bigote; tecla ↔ gato)
- palabras: mapa de estrellas con fotos y palabras que se acercan (gato junto a «gato», perro cerca, volcán lejos); el modelo lee piezas como palabras
- trucos: husky/lobo con la nieve iluminada · panda + ruido = «GIBÓN 99 %» · cierre: la torre de abajo arriba y Kuri guiña

## Comentarios
- `yt comentarios kuriox` (4-nov): 3 nuevos, sin quejas ni sugerencias; todos positivos («me gusta cuando se frotan las manos», «buen dato»). Pocos para ≥ 4 agradecimientos; ver al final si caben con fecha ≤ 10 días.

## Hecho
- `nuevo` + kit copiado (acuarela, comun, _hoja, sfx_proc, personajes, utileria) · `canales --actualizar` (Kuriox ATRASADO, −4 d)
- guion.py con 11 escenas, ~9,1 min de voz + pausas; DOI verificados en Crossref (Hubel-Wiesel, Fukushima, LeCun, Rumelhart, ImageNet, AlexNet, Zeiler-Fergus, ResNet)

## Falta
- [x] todo; solo el .srt en Studio

- tele: 04-Nov 14:01 «¿Sigo así con el video de la IA?» → **Sí, sigue** (contestado en la tele)
