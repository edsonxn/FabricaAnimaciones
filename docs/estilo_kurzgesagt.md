# Estilo Kurzgesagt (plano secuencia, sin voz, portales) + **Kurzgesagt ISOMÉTRICO con mapas de relieve** (Bitácora Perdida)

_Primera parte nueva (1-oct-2026): receta del estilo isométrico de `videos/independencia_mx/`, el estándar de calidad del canal Bitácora Perdida. Debajo, lo anterior (extraído de CLAUDE.md)._

## A. KURZGESAGT ISOMÉTRICO + MAPAS CON RELIEVE REAL (historia; ejemplo `videos/independencia_mx/`, t01…t0N.py)
**Cuándo usarlo:** videos de historia/geografía de más de 3 min para Bitácora Perdida (y cualquier canal Kurzgesagt que cuente lugares y épocas). Se compone de: mapa con relieve real + dioramas isométricos de cada lugar + interiores en corte + retratos de personajes + etiquetas de cápsula + cámara siempre viva. Calidad objetivo: Kurzgesagt (detalle denso, personajes expresivos, movimiento continuo).

**Kit reutilizable (en `nucleo/`, NO específico de un video)** — catálogo con firmas en `docs/api_kz.md` (se regenera con `python nucleo/api_kz.py`; consúltalo con grep, no lo leas entero):
- `kz_iso.py` motor isométrico (`Iso`, `Mundo`, `caja`, `habitacion`, `isla`, techos, cúpulas, suelos); `kz_iso_arq.py`/`kz_iso_arq2.py` arquitectura colonial (casas, iglesia, haciendas, alhóndiga, palacio, catedral, mina, puente, acueducto, tiendas, cañón, barco); `kz_iso_obj.py`/`kz_iso_obj2.py` objetos (árboles, nopal, maguey, fuego, humo, banderas, carretas, estandarte guadalupano, lingotes, pergaminos, trincheras…); `kz_iso_int.py` interiores (cortinas, ventanas, escudos, chimenea, araña…); `kz_iso_deco.py` densidad automática (bosque, campos, hierba, aves, polvo, acequia).
- `kz_gente_iso.py` personas (`persona(..., tipo=, accion=, cara=)`, tipos en `G.TIPOS`, `Multitud` con `camina/ronda/quieto`, caballos, burros, ovejas).
- `kz_retrato.py` bustos grandes expresivos (`RT.QUIEN`: Hidalgo, Allende, Morelos, Iturbide, Calleja, Napoleón…). `kz_ui.py` etiquetas `llamada`/`globo`, `pop/repop/salida`, `fecha_lugar`, `contador`, `bokeh`, `haces_luz`, `ondas_sonoras`, `gradacion`, `pergamino_grande`.
- `kz_mapa.py` (relieve ETOPO1 + países Natural Earth: `MAPA.base(cam, t, exag, rios_umbral)`, `proy`), `kz_mapa_dib.py` (sobre el mapa: `ciudad`, `ejercito`, `ruta`, `pais`, `mar_vivo`, `montes`, `medallon`, `insignia_batalla`, `etiqueta`; 37 lugares nombrados en `CIUDADES`, o una tupla (lon, lat)). Datos en `nucleo/datos/` (y `videos/<v>/datos/`). **Fotos en el mapa (regla global, 23-oct-2026):** cuando la voz nombra una ciudad/personaje/objeto sobre el mapa, su retrato o foto REAL (`kz_retrato_real`) sale junto a su punto y se va al pasar al siguiente.

**Esqueleto de un video nuevo (copiar de `independencia_mx`):** `reg.py` (registro de tomas `@shot` y sonidos `snd`), `escenas.py` (ensambla las tomas y las transiciones; una clase `Mundo` para todas las escenas), `util.py` (anclas de la voz `T()`, claves de cámara `K/Klog`, fondos), `_prueba.py`/`_cuadro.py`/`_clip.py`/`_pal.py`/`run.sh`/`_esc.sh` (herramientas de revisión), y por escena `tNN.py` + mundos propios `mundos_X.py`. Orden de trabajo: guion y voz primero (`fab.py voz/seleccionar/tiempo`), luego una escena a la vez con revisión visual, al final música (Lyria), SFX (`snd`), mezcla, render con `--procs 8`, `final`, `verificar`.

**Receta de una toma (≈ 3-8 s; un cambio visual cada ~4 s):**
1. Anclas con `T(escena, "palabra", frase=i)` (prefijo, sin acentos, `n` base 0) → tiempos de entrada de rótulos, personajes y efectos.
2. Cámara con `K(t, [(t, (cx, cy, cz, zoom)), ...])` (iso) o `Klog` (mapa, zoom logarítmico). La cámara NUNCA está quieta; acércate a la acción narrada.
3. Mundo: `suelo(lz, iso, t)` + `objetos(t)` (estático cacheado + dinámico por cuadro) con densidad (bosque, campos, casas de colores, 40-100 personas en tomas de masas).
4. Actores con `G.persona`/`Multitud` (ritmo propio de cada uno); la acción narrada la hacen ellos.
5. Rótulos: `U.pop(t, t0) * U.salida(t, t1)` (ojo: `salida` vale 1 ANTES de t1). Máx. ~6 palabras por rótulo; que no se encimen (cada uno se apaga antes de que entre el siguiente; los de una lista duran ~1 s).
6. Sonidos con `snd(t, nombre, vol)` en el pulso de cada aparición.

**Composiciones que funcionan (catálogo):** mapa con relieve + ciudades que «saltan» (pop) + ruta/flecha; diorama isométrico de un lugar con multitud; interior en corte con personajes; **pantalla dividida con muesca** (dos lugares a la vez, p. ej. celda/trono, Josefa/alcaide) — un corte de casa de dos pisos NO sirve (el piso de arriba tapa al de abajo); retrato en medallón + globo de diálogo; burbujas de pensamiento con iconos 2D; calendario; vista 2D de paisaje con «mar de gente» de espaldas (`mundos_h.vista_capital`, `multitud_espalda`); **flechas gruesas de pantalla** para movimientos locales de tropas (en distancias cortas los íconos de ciudad/ejército de tamaño fijo se encimaban); contadores que suben; cerros con casitas de fondo (`mundos_g.cerros`) para ciudades de ladera.

**Más composiciones validadas (escenas 6-18 de la Independencia):** cerros con casitas de fondo para ciudades de ladera; mapa del Atlántico a `z=0.18` centrado en (-52, 29) para escenas México–España (a `z=0.55` solo se ve el océano); flechas gruesas de guerra y círculos que se encogen para cercos; polígono de territorio que crece/se encoge (`SUR_POLI` en t10/t12); infografías 2D rápidas y baratas (cadena que se rompe, escalera de castas que se aplana, barras de poder con tijeras, velas que se consumen, línea de tiempo con hitos, bolsa vacía + flechas divergentes, escudo con cofre/iglesia/espada, calendario/tarjetas de fecha, pergamino con sello); mar de gente de espaldas (`multitud_espalda`); fuegos artificiales radiales (`t16._cohete`); retratos en fila con crespón negro para memoriales; globos de pensamiento con iconos 2D (`t07._nube`).
**Violencia y muerte (decisión de tono):** paleta gris-violeta (`GRIS` = gradación con saturación 0,6-0,7), fondo `bg` oscuro, sin mostrar el momento: soldados en fila con fusiles en alto, destello local sobre el lugar, una paloma que sube; crespón negro diagonal sobre el retrato; jaulas colgadas como silueta. Rótulo con la fecha y el nombre.
**Coste real del video de 11 min:** 18 escenas, ~170 tomas, ~480 efectos de sonido; unas 3-4 horas de escritura/revisión por escena en iteraciones de «hoja de prueba → mirar → corregir».

**Reglas y trampas (aprendidas, 1-oct-2026):**
- Relieve del mapa: `exag=12-13, rios_umbral=0.7` y zoom ≤ ~4; por encima se ve borroso (ETOPO1). Para acercarte pasa a un diorama isométrico. Los íconos de `MD.ciudad` y `MD.ejercito` tienen tamaño fijo en píxeles (no dependen del zoom).
- Nunca mapas de «manchas»: siempre relieve + ríos + costa + ciudades en su coordenada real con etiqueta.
- Cada escena con su mundo visual propio (no repetir el mismo decorado en escenas distintas; el mismo lugar se varía con hora del día, luz y cámara). Pueblo dormido = `objetos(t, gente=0)`.
- Personajes: tipos y retratos existentes (no hay `criollo`; usa noble/regidor/comerciante/escribano/dama). Violencia sin sangre: humo, fuego, objetos que vuelan, personas que huyen; la matanza se sugiere con rótulo y color, no se dibuja.
- Texto en pantalla solo de énfasis (regla global); nunca subtítulos corridos.
- Al terminar cada escena: hoja con `_prueba.py` (3 columnas), MIRARLA, corregir (rótulos encimados, escenario vacío, personajes diminutos, mapas con íconos amontonados) y anotar en `ESTADO.md` del video.
**Correcciones del usuario (2-oct-2026) → ya están en el kit; úsalas así:**
- **Mar sin «paralaje raro»:** `MD.mar_vivo` ancla olas, barcos y delfines a rejillas de lon/lat de tamaño fijo por NIVEL (2**n grados) y funde un nivel en otro al hacer zoom (`_niveles`/`_celdas`); las crestas son polígonos con alfa real (`_cresta`). El sombreado del agua en `Mapa.base` usa coordenadas del mundo (se mueve con el mapa, no con la pantalla). NUNCA dibujar olas con celdas de tamaño que cambie con el zoom ni brillo del agua en coordenadas de pantalla.
- **Íconos de ciudad en mapas lejanos:** `MD.ciudad` se achica con el zoom (`(z/0.7)**0.75`, 0,3-1) y esconde (encoge) los que se encimarían con otro del mismo cuadro (`lz.ocupado`); reaparecen al acercar la cámara.
- **Orden de dibujo isométrico:** `Mundo.topo = True` ordena por GEOMETRÍA (`_orden_topologico`: i detrás de j si su caja está a menor x o y y se tocan en pantalla; empates por clave). Úsalo en mundos con muelles, barcos, gente y casas largas. Requiere cajas reales en `m.add(x0,y0,x1,y1,h,fn)` (no `(0,0,4,4)` falsas con `clave=`). Ya activo en `RutaPlata` y `PuebloRuina`; para otros mundos activarlo escena por escena y revisar (los `add` con caja falsa se desordenan).
- **Etiquetas sin cola (`U.llamada(..., cola=None)`) que no se encimen:** con `lz.diferir = True` (se pone en `escenas._toma`) se dibujan al FINAL del cuadro (`U.vaciar_diferidos`) y se mueven lo mínimo para esquivar la fecha de esquina (`U.fecha_lugar` registra su zona), los marcos de retrato y otras etiquetas (`lz.zonas_rot`, `U._registrar`). Rótulos sueltos grandes (años con `P.rotulo`) deben llamar a `U._registrar(lz, cx, cy, w, h)`.
- **Transición `tinta`** nunca deja el cuadro negro (revela B con borde de tinta, `docu_fx.mezcla2`).
- **Retratos de personajes históricos: REALES, no dibujados.** `nucleo/kz_retrato_real.py` + recortes en `nucleo/datos/retratos/*.jpg` (pinturas, grabados y fotos de dominio público de Wikimedia Commons; créditos en `CREDITOS.md`). `RT.retrato(...)` y `MD.medallon(...)` delegan solos si `quien` tiene retrato (hidalgo, morelos, allende, aldama, jimenez, josefa, leona, iturbide, calleja, napoleon, virrey, guerrero, victoria, matamoros, galeana, fernando, mina, odonoju, porfirio, yermo, garibay); el resto (campesino, criollo, peninsular, esclavo…) sigue dibujado. Integración: cuadro dentro de marco dorado con molduras y bisel, sombra, viñeta, mapa de color hacia la paleta morado/crema (`_grad_map`), flotación suave, brillo que cruza el cristal y esquiva de etiquetas; medallón redondo con anillo dorado para mapas. Para añadir uno: descargar de Commons (`_buscar_retratos.py`, `_bajar_retratos.py` en `videos/independencia_mx/`; con pausas, Wikimedia da 429 si se pide rápido), añadir caja de la cara en `videos/independencia_mx/retratos/_config.py` y correr `python nucleo/preparar_retratos.py`. En fila, cada marco mide ≈ 2,8·s px de ancho (s = tamaño del retrato): deja ≥ 3·s entre centros.
- Coste: ≈ 0,7-1,5 s por cuadro; un video de 11 min ≈ 19 500 cuadros → render largo con 8 procesos (no lo lances junto con la voz).

**Lecciones de `videos/juchipila/` (11-oct-2026; personajes 2D `kz_pers2d` + conceptos `kz_abstracto` sobre el isométrico):**
- **Orden de capas (defecto que vio el usuario):** en paisajes 2D el río va ANTES que el pueblo y las casas se reparten en las dos orillas (`paisajes.rio_borde`, `aldea(rio_h=...)`); lo que está «en las crestas» (guerreros) se dibuja entre sierras y pueblo, nunca encima de los techos. Los bustos/cuerpos de `kz_pers2d` se dibujan en la capa 1: el fondo de un medallón o de un papel que los contiene debe ir en `capa=1` (en `capa=2` los tapa y la cara sale oscura o vacía). El caballo 2D con jinete va en la misma capa que el jinete (`mundos_h.caballo2d`, capa 1) y el jinete a ≈1,2·s con `cara="minima"`.
- **Mapas de lugares muy juntos** (pueblos a < 60 km): ETOPO1 se ve borroso por encima de zoom ≈ 5,5 y los ríos se escalonan; no se separan. Solución: la acción en una escena 2D propia (p. ej. emisarios con antorchas de aldea en aldea) + **recuadro con el mapa real** en la esquina donde se encienden los pueblos (`mundos_g.inset_mapa`, post-proceso numpy cacheado).
- **Recursos nuevos reutilizables del video** (copiar si hace falta, no reciclar escenas): peñol isométrico escalonado con cornisas, defensores, lluvia de piedras y cerco que se cierra (`mundos_h.PenolIso`, `mundos_i.cerco`); peñol 2D de perfil con gente que sube (`mundos_g.penol`); olla tapada que hierve + termómetro (tensión); pueblo que se construye casa por casa con muros de adobe y andamio hasta el templo (`mundos_k.PuebloNuevo`); mina en corte; Lecumberri radial; tablero de «reparto» de pueblos.
- **Retratos reales añadidos** (`nucleo/datos/retratos/`, config en `videos/independencia_mx/retratos/_config.py`, descarga `videos/juchipila/_bajar_retratos.py`): alvarado, mendoza (virrey Antonio de Mendoza), lascasas, madero, natera, villa. Sin retrato de época (van dibujados): Nuño de Guzmán, Cristóbal de Oñate, Tenamaxtli, Crispín Robles, los frailes Segovia y Bolonia.
- `kz_pers2d`: máscara de **tastoán** rehecha (madera rosada, nariz larga, ojos saltones, dientes, cuernitos, cabellera de ixtle).
- Revisión: `_humo.py <paso>` (en el video) recorre TODO el video renderizando un cuadro cada `paso` s y reporta excepciones, cuadros negros y cuadros lentos; correrlo antes de entregar.

**Lecciones de `videos/apozol/` (11-oct-2026; 4 min, 7 escenas, kurzgesagt isométrico + mapa; todo escrito en una sesión):**
- **Estructura que funciona para 4 min:** 7 escenas de 30-50 s, 4-9 tomas cada una (~40 tomas); cada escena con su propio mundo (`mundos_N.py`) y las tomas 2D de apoyo (infografía, medallón, línea de tiempo) entre dioramas isométricos.
- **Línea de tiempo provisional para desarrollar sin voz:** `_tl_prov.py` (copiar de independencia_mx; 3,3 palabras/s para Dan, `unidad=4`, `BPM=108`) → las anclas `T(escena, "palabra", frase=i)` buscan por PREFIJO en las palabras del GUION (no en Whisper): cualquier palabra escrita en la frase sirve; `fab.py <v> tiempo` la sustituye.
- **Isométrico sin «isla vacía»:** una isla de 600×600 u a zoom ≤ 1 deja 60 % de la pantalla morada; zoom 1,3-2,2 con la acción centrada y relleno automático (`DC.bosque` en el borde exterior, `O.agua` en una orilla, camino, tiendas/fogatas, rocas). Para ruinas o interiores: zoom 1,9-2,2 y utilería (alfombra, reloj, maceta, mapa de pared, haz de luz de la ventana).
- **Interiores (`I.habitacion`):** las paredes de fondo son las caras `"yi"` (plano y mínimo, a a lo largo de +x) y `"xi"` (plano x mínimo); usar `"y"`/`"x"` coloca el objeto en el plano delantero, invisible o flotando.
- **No inventar cifras en pantalla** (un contador «4 000» donde la narración dice «miles»): rótulo «MILES». Contadores de año solo entre hitos que el guion nombra.
- `lz.trazo` no tiene `alfa=`: pasar color RGBA `(r, g, b, a)`. Medallones con busto `K2` → fondo en `capa=1`. Banderas/telas llevadas por figuras 2D: asta propia pegada al cuerpo (no rectángulos flotando sobre la cabeza).
- `post_fundido_negro` solo al FINAL del video: entre escenas deja un cuadro negro (`_humo.py` lo marca).

### ERRORES A NO REPETIR (revisión de 166 cuadros del MASTER de Juchipila, 11-oct-2026; detalle con tiempos: `videos/juchipila/REVISION_MASTER.md`)
El video se subió así por decisión del usuario, pero estos fallos NO deben llegar a un video nuevo. **Antes del render largo, repasa esta lista con la hoja de cuadros y márcala:**
1. **Transición de «manchas» (`tinta`/máscara de ruido) con contorno negro:** se ve sucia y tapa texto. Usa barrido/iris/continua limpios; si usas `tinta`, sin contorno oscuro y SIN texto importante en pantalla durante la transición (reubica o retrasa la etiqueta).
2. **Escenas 2D con «suelo plano»:** una franja verde/oscura lisa + cielo vacío no es escenario. Toda escena 2D lleva ≥ 3 planos, textura de suelo (hierba, piedras, polvo), detalle del lugar y animación ambiente; si no hay presupuesto, hazla isométrica (`kz_iso*`). Cuidado con 2/3 de la pantalla vacíos con una fila de figuras abajo.
3. **Figuras clonadas en fila** (misma pose, mismo tamaño): varía pose, altura, atuendo y fase de animación; multitudes con ritmo propio. Bailarines/figuras con `kz_pers2d` en primer plano: boca, manos unidas al brazo; **nada de flores/objetos pegados encima del cuerpo** (van en el suelo o en las manos).
4. **Etiquetas:** tamaño mínimo ≈ 28 px a 1080p; ninguna entra o sale a escala mínima visible (la animación de salida debe desvanecer, no encoger a ilegible). Ninguna etiqueta, calendario, listón, flecha o letrero cubre una cara, otra etiqueta o el punto que señala (comprueba también `Juchipila`/`Guadalajara` y similares a < 60 km: separa con cola o `U._registrar`).
5. **Contraste:** texto blanco sobre fondo claro (mapa beige, sol, amarillo, naranja) SIEMPRE con cápsula oscura o sombra; números grandes no van delante del sol.
6. **Retratos reales:** revisar a tamaño completo cada marco (rayas de estiramiento en el borde superior, imagen casi negra tras `_grad_map`, relieve del mapa u otros íconos encima de la cara). Si la pintura es muy oscura, subir exposición al preparar el recorte (`preparar_retratos.py`).
7. **Mapas:** no ampliar el relieve más allá de zoom ≈ 5,5 (se ve borroso): usa recuadro/inset o escena propia. Mapas del Atlántico/mundo con el MISMO estilo de relieve que los demás (no el plano de color liso). Etiquetas de lugar no cubiertas por barcos, flechas ni puntos de ruta; las flechas terminan junto al destino, no encima.
8. **Línea de tiempo con escala proporcional** (o marcas honestas): 1541→1550 no puede medir lo mismo que 1550→1552. Contadores de año: el año mostrado coincide con la escena que se ve.
9. **Cartas/pergaminos/documentos:** nada de renglones de relleno en un pergamino enorme vacío; ajusta el tamaño al contenido o añade contenido real (texto corto, sello, firma). Check/íconos no pisan el texto.
10. **Personajes que flotan** (jinetes sin asiento, caminantes sobre ladera oscura sin suelo): siempre contacto con suelo y sombra; el jinete se sienta (`mundos_h.caballo2d`).
11. **Escenas con tarjetas planas** (icono blanco sobre fondo liso) ocupan el cuadro con contexto: fondo ilustrado detrás y animación (no dos tarjetas quietas).
12. **Etapa de revisión obligatoria:** hoja de 6 cuadros por pantalla (2×3, 800×450, un cuadro cada 3 s) sobre el MASTER antes de dar el video por bueno, y tamaño completo para tomas con texto, retratos o mapas. Anotar defectos con el tiempo en `videos/<v>/REVISION_MASTER.md`.

---
# (Anterior) Estilo Kurzgesagt plano, plano secuencia, videos sin voz y portales

## BAÚL ESPACIAL `nucleo/kz_espacio.py` (12-oct-2026, Kuriox; nació en `videos/dos_lunas/`)
Piezas reutilizables para cualquier video de espacio (catálogo con firmas: `grep -n "def cuerpo_rocoso" docs/api_kz.md`):
- `cuerpo_rocoso(tipo=luna|ceniza|rojiza|hielo|volcanica|mercurio|oscura, seed, rot, fase=)` lunas con mares y cráteres que giran con
  foreshortening (`fase` 0..1 = fase lunar limpia); `roca` (asteroide/Fobos); `luna_rota(estira, rompe)` (límite de Roche: se estira, se
  agrieta con lava y se parte); `planeta_gas(paleta)`; `anillo` (continuo, `mitad=0` antes del planeta y `mitad=1` después) y
  `anillo_escombros` (rocas con Kepler); `lluvia_rocas`.
- Órbitas y zonas: `orbita` (discontinua que corre o se traza), `pos_orbita`, `estela`, `esfera_hill`, `punto_lagrange`, `triangulo_equilibrio`.
- Mareas: `tierra_marea(lunas=[(ang, fuerza)])` (el agua se deforma; con dos lunas a 90° los tirones semidiurnos se anulan, a 0°/180° se suman)
  y `flechas_marea`. Diagrama: `flecha`, `regla`, `etiqueta`, `destello`, `nebulosa`, `fondo_espacio`.
- Prueba visual: `videos/dos_lunas/_hoja_kit.py` (→ `previews/kit_hoja.jpg`). Convención: `ang_luz` apunta HACIA la luz; `seed` fija los detalles.
- Lección: dos tonos de `esfera` (terminador doble) ensucian las fases lunares → por eso `fase=` dibuja el cuerpo a plena luz y sobrepone UN terminador elíptico.
- (13-oct) `luna_dos_caras(rot, panqueque)` (cara visible lisa con mares / oculta con cráteres) y utilidades de trayectoria: `fantasma`
  (cuerpo hipotético punteado), `marca_x`, `bez2` + `kepler(a, e, w, M)` (aproximación y elipse de un asteroide capturado), `trail(f, t)`
  (estela; `f` debe valer para tiempos anteriores). Cámara de plano secuencia: `cam_claves` de `videos/dos_lunas/mundo_comun.py` (zoom log).
- HALLAZGOS `dos_lunas` (13-oct): (1) un cierre «quieto» de > 10 s con solo animación ambiente (peces, reflejos) se nota estático:
  mueve algo grande (la Luna sube y crece despacio, `luna_c`) además del ambiente. (2) Rótulos y tarjetas se comprueban contra el
  rectángulo del foco (la tarjeta tapaba la Luna). (3) Mitad del cuadro vacía en un primer plano (Luna a la izquierda) → llénala con
  un recuadro que explique (la otra cara, corteza, año del estudio) en vez de dejar cielo. (4) `fab.py <v> musica` era la PROCEDURAL
  y pisaba la Lyria: desde el 13-oct, si guion.py tiene `LYRIA` con `tramos`, `musica` corre `nucleo/lyria_tramos.py todo` (sin `tramos`
  avisa y no hace nada; la procedural solo con `--procedural`).

- HALLAZGOS `oxigeno_5s` (14-oct, 5:52, plano secuencia en módulos; copiar de ahí):
  (1) `mundo_comun.Sup(hx, hy, k, kappa, X0)` se dobla alrededor de X0 y `S.par(f)` da capas lejanas con paralaje (Sol 0,04,
  nubes 0,3, cordillera 0,2, cerros 0,42, lomas 0,68, skyline 0,86). (2) Zoom paisaje <-> planeta (`camara.zoom_global`): k = rs/RW
  con RW = 1e5; si solo se dobla el paisaje se ve un «bloque» con el corte del subsuelo (el usuario lo vio: «aparece ese cuadro de
  tierra»): durante el zoom dibuja SOLO la piel de la superficie (`MP.dibujar(delgado=True)`: suelo de 70 u, mar de 70 u, montaña
  rellena), encima un planeta liso + continente en forma de lente (`escenas._tapa_planeta`), y `P.tierra` solo con rs < 3200 y girada
  un poco (con rs grande su casquete polar ocupa media pantalla). (3) Mundo interior por PORTAL: círculo que se abre en el pecho
  (`mundo_cuerpo.portal`, el cuerpo se dibuja recortado con su fondo como polígono) y se cierra en la cabeza al salir.
  (4) Poppins no trae «₂», «✓», «→», «⚠»: `ui_base.texto_q/pildora` dibujan O2/H2O con subíndice y `check`/`cruz`/`prohibido`
  son vectores. (5) La visión de túnel se hace en el posproceso: los rótulos de ese momento van al centro (si no, se oscurecen).
  (6) Contador «SEGUNDO n» + insignia «VERSIÓN A/B» ordenan un experimento mental largo. Hoja rápida: `_cuadro.py hoja t...`.

## Estilo Kurzgesagt y plano secuencia (ejemplo: `videos/sol_apagado/`, 1:00)
- `ESTILO_VISUAL = "kurzgesagt"`: sin contornos (los trazos NEGRO no se dibujan; usa `plano.TINTA` si quieres
  una línea oscura), sin temblor, bloom de lo luminoso y saturado. Dibuja con `nucleo/plano.py`: `esfera`,
  `sol`, `tierra` (continentes que giran, `luz`, `ciudades`), `luna`, `pajaro`, `microbio`, `arbol`, `fumarola`,
  `termometro`, `onda` (frente de onda), `discontinua`, `rotulo`/`pastilla` (fuente `geo` = Poppins).
- Lienzo nuevo: `with lz.recorte(pts):` (clip), `lz.degradado(pts, c0, c1, p0, p1)`, `lz.halo(x, y, r, color)`.
- Fondos `espacio` (estrellas con paralaje dx/dy) y `degradado`; `F.estrellas(img, t, brillo)` sobre cualquier fondo.
- Sabores musicales documental: `espacio`, `tension`, `vacio`, `esperanza` (sin bombo; cierre suave).
- **Plano secuencia (sin cortes)**: `TRANSICIONES = [("continua", 0.1)] * n` y en escenas.py una sola clase
  (`Mundo`) para todos los ids que dibuja el mundo en función del t global; las escenas solo marcan narración y
  música. Anclas entre escenas con `T(id, palabra)`. Transformaciones usadas: zoom a la Tierra cuyo borde se
  aplana en horizonte (clase `Sup`: paisaje doblado con curvatura 1/radio), paneo continuo, brillo que llena la
  pantalla y se encoge convertido en otro objeto. Registra los sfx solo en la instancia `idx == 0`.
- `MEZCLA = dict(musica=-21.5, sfx=-22.5)` en guion.py baja el fondo cuando la narración es casi continua.

## Estilo Kurzgesagt — ACTUALIZACIÓN (29-sep, `videos/historia_60/`: vertical, 19 épocas, portales)
Receta visual que ya funciona (mirar `previews/final_hoja.jpg` del video como referencia):
- **Forma:** solo rellenos planos, sin contornos ni temblor; volumen con 2 tonos (`oscurecer(c, 0.2-0.4)` en la cara de sombra y
  `aclarar` en el borde de luz), nunca negro puro (sombras azul-violeta, `plano.SOMBRA`). Personas y animales son cápsulas
  (`kit.capsula`) + círculos; ojo = un punto, nariz = círculo pegado a la cabeza, cejas finas para dar expresión.
- **Color:** cada época tiene su propio degradado de cielo (`kit.degradado_img(arriba, abajo, mid=, ym=)`, atardeceres morado→naranja,
  cielos azules claros de día, noche azul-violeta con `F.estrellas`), colinas en 2-3 capas con paralaje (`kit.colinas(..., dx=t*v)`), suelo oscuro
  al pie para que entren título y contador. Luz de antorcha/bombilla/sol = `lz.halo` cálido en capa 2 encima de todo (no hay iluminación real).
- **Movimiento (regla del canal: nada se queda quieto):** todo es función del tiempo: caminata con fase `ph=t*ω` (ω≈6,5 rad/s con suelo a
  ≈385 px/s para que los pies no resbalen), parallax de fondo, humo/polvo/partículas periódicas (`kit.particulas`), ruedas y engranajes girando,
  brazos con IK (`kit.ik`) para que la mano siga un punto (pincel, azada). Cada objeto principal entra con `e_back` (rebote) y su sfx en el pulso.
- **Personaje:** `kit.persona(lz, x, y, s, t, ph=, paso=, mirar=±1, piel=, pelo_t=, ropa=, falda=, sombrero=fn, brazos=(4 ángulos), obj_d/obj_i=fn,
  fijo_i/fijo_d=, inc=, salto=, extra_torso=fn, barba=)`; `kit.PIEL` (5 tonos). Objeto en mano: su +y va a lo largo del antebrazo (`fijo_*` lo deja vertical).
- **Vertical 1080x1920, zonas:** contador de años arriba (y≈262, halo oscuro detrás), escenario y≈450-1400, título de época abajo (y≈1462/1532),
  riel de progreso en x=48 (y 470-1290). Suelos/polígonos deben llegar a H+60 (la cámara hace zoom).
- **Transiciones procedurales entre épocas** (`escenas.py`, imágenes A/B): `portal` (círculo que crece desde un objeto de A con anillo de luz;
  A hace zoom-in y B llega desde 0,42x), `reloj`, `puntos` (media tinta), `bajada`/`subida`, `ola` diagonal, y `E.tr_glitch`/`E.tr_pixeles`.
  El objeto-origen se declara en `Era.salida(t)`, su color en `COL_SALIDA`. Cada 750 ms (`D_TR`), termina justo en el pulso de la nueva época.
- **Sonido:** cada época registra sus sfx en `sfx(ev)`; las transiciones usan iris/reloj_rapido/burbujas/ola/glitch. ~300 eventos; `MEZCLA` sfx ≈ -23.
- **Coste:** 0,2-0,5 s por cuadro normal y 0,6-1,3 s durante transiciones (dos épocas a la vez); 60 s completos ≈ 400 s con 12 procesos.
- **Voz anclada sin tocar la imagen:** `VOZ_ANCLADA = True` + `"anclas": [pulso,...]` por frase en cada escena del guion (ver `videos/historia_60/guion.py`);
  `SUBTITULOS = False` evita dibujar subtítulos encima (el `.srt` se genera igual). Generar voz cambia solo el audio: basta `voz`, `seleccionar`,
  `tiempo`, `mezcla`, `final` (el MASTER conserva el video).

## Videos SIN VOZ y "épocas" con portales (ejemplo: `videos/historia_60/`, 60 s vertical, 19 épocas)
- `SIN_VOZ = True` en guion.py: cada escena es una sección musical con `"compases": N, "frases": []`; `tiempo` usa
  `nucleo/linea_tiempo_mudo.py` (60 s a 128 BPM = 32 compases). `mezcla`/`verificar` no exigen voz; `todo` salta voz/seleccionar.
  La música termina con su golpe final en `fin_musica` (TOTAL - 3 pulsos). El pico verdadero se recorta a ≤ -1 dBTP.
- Estructura: `kit.py` (persona de perfil con ciclo de caminata, IK del brazo `ik()`, colinas, nubes, partículas),
  `era.py` (tabla de épocas en pulsos, clase `Era`, `img_era`), `epocas1..4.py` (una clase por época con `fondo/cam/dibujar/sfx/salida`),
  `escenas.py` (transiciones procedurales portal/reloj/puntos/bajada/ola/glitch, contador de años, riel, `Mundo`).
  Cada época se dibuja también ANTES de su inicio (durante el portal): sus animaciones deben arrancar en `a(-1.6)`.
- OJO `lz.grupo(x, y, s)` TRASLADA y luego escala: para escalar alrededor de un punto anida `grupo(x,y,s)` + `grupo(-x,-y)`.
- Prueba una época sola: `videos/historia_60/run.sh _era_test.py <id> <pulsos...>`; hoja de cuadros en `previews/`.
