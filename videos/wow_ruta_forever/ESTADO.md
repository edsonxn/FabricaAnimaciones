# La RUTA del 1 al 60 en WoW Forever, zona por zona — ESTADO
<!-- Máx. 60 líneas. Las 4 primeras viñetas las lee `python fab.py estado`. Actualízalo al terminar cada sesión. -->
- canal: cronicas_warcraft · lun 23-nov-2026 09:00 CDMX (2026-11-23T15:00:00Z), SIN Overgear (integraciones de la campaña 3: 25 y 29-nov)
- estilo: secuencia_yt (gameplay de YouTube por beat + apoyos + MG + mapas con ruta) → doc: docs/estilo_secuencia_yt.md · copiar de `videos/wow_oro_forever/`
- etapa: revisión visual hecha (19-nov) → falta render (musica_wow → musica → sfx → mezcla → video → final)
- siguiente: `python musica_wow.py` (≤ 175 s por tramo) → `musica` → `sfx` → `mezcla` → `video` → `final` → `verificar` (revisión visual ya hecha; ver «En curso»)

## Sesiones
- alias: «la ruta 1-60», «ruta de Forever», «warcraft del lunes»
- vista previa: ninguna (una sesión directo al MASTER, regla 5-nov)
- leer al empezar: este ESTADO.md, docs/estilo_secuencia_yt.md § REGLA DE ORO, videos/wow_oro_forever/ESTADO.md (lecciones de RAM/Applio)
| # | Tramo | Estado | Nota |
|---|---|---|---|
| 1 | todo hasta el MASTER y la subida | ✅ 19-nov: MASTER, subido, monetizado, registrado y commit 2d8c1e4 | tema elegido por el usuario el 19-nov: opción 2 de la conclusión del 15-nov |

## Decisiones del episodio
- tema: «La RUTA 1-60 de WoW Forever zona por zona» (el usuario, 19-nov; recomendado por Claude). Una variable sobre «20 errores del 30 al 60»: el formato (guía-ruta con mapa real en cada zona). Referencia: Blizzard «leveling past 30» ×2,2.
- duración: ~25 min (listas largas de Forever aguantan 42-47 % visto). Paradas por tramo de nivel, Alianza y Horda.
- voz: Remy (Applio) entero — los comentarios piden «la voz de siempre» (se le reporta al usuario, no se cambia).
- Overgear: NO. Nada contra comprar oro ni contra coaching.
- Comentarios (19-nov, 47 nuevos): corrección @sastakai «en JcJ no se pierde durabilidad al morir» (comprobar y, si es justa, corregir) · agradecimientos candidatos @rubenlopez9451 ♥5, @Sakaan07 ♥2, @mateogrisalescano2147, @lololulu-r5w, @sgto.sevilla6976, @massimoamoretti9086 · críticas con burla: @vito_232 «Parece el tilin usando IA», @Dk_EpYon91 (Maricarmen GPS), @josejuanandrade4439 · voz: siguen pidiendo «la voz de siempre» o la real.
- REGLA DE ORO: leer docs/estilo_secuencia_yt.md § REGLA DE ORO antes de `efectos.py`; `chequeo` antes de renderizar; FAB_FX_FINAL=1 fx hoja; citas de audio comprobadas en la mezcla final (regla 10).

## En curso (checkpoint)
- ✅ investigación (`videos/_investigacion_wow_ruta_forever.md`, 14 paradas, coords de Wowhead Forever; Riverglades = «Claros del Río» en es-MX).
- ✅ guion.py (157 frases, ~4 100 palabras, 14 paradas + 3 gracias/comentarios + 3 burlas + cierre). 12 tarjetas `com_*` hechas.
- `voz` LANZADA (`_voz.log`/`_voz.err`; avisos de «sonido nombrado» = falsos positivos: «así suena», «voces», «escuchando»).
- subagente 2 LANZADO: mapas de zona + `_coords.md` + `_coords_check.py` (previews/_coords_check_N.jpg) + pegatinas + `previews/pegatinas_check.jpg`.
- OST bajando (`_ost.log`, audio/wow/). Plan de temas por tramo: intro Legends of Azeroth (-ZD81cUBwHo) · p01 Dun Morogh (g2SZuqyjKtA) · p02 Westfall (R7FGebBI8JM) · p03+burla0 Elwynn Release (MDMa49NrQPM) · p04 Duskwood (l8AlVcEvLEE) · p05 Mil Agujas (k43reRbLrrM) · p06 Baldíos (Do5s0MQvF9s) · p07+burla1 Tuercespina (uRiQE-xvDyQ) · p08 Ashenvale (78xB_GqLwPY) · gracias1 Goldshire Tavern (siGaJvUTqGI) · p09+burla2 Feralas (SXImOlFUGYo) · p10 Tanaris (S1qEZ7uw0iw) · p11 Un'Goro (nlXOcybLHxc) · p12 Blackrock (_bWLsDaffMU) · gracias2 Tavern Orc (21sMUJMnkhc) · p13 Winterspring (S-hYpfNnlv0) · p14 Moonglade (MwJ65pIfamE) · cierre Legends of Azeroth.

## RELEVO 1 (19-nov ~15:30, corte a 180 mil) — qué falta EN ORDEN
- Corriendo al cortar: `voz` (Start-Process; `_voz.log`) · subagente de mapas/coords/pegatinas (escribe `mapas/`, `_coords.md`, `_coords_check.py`, `previews/_coords_check_N.jpg`, `pegatinas/`, `pegatinas/_creditos.json`, `previews/pegatinas_check.jpg`; su informe llega a la sesión vieja: COMPROBAR que existan esos archivos y MIRAR las hojas; si faltan, rehacer esa tarea con el mismo brief = modelo `videos/wow_oro_forever/_coords.md` + `_pegatinas.py`) · OST bajando (`_ost.log` → audio/wow/, 17 temas del plan de arriba).
- 1) ✅ voz 157 · seleccionar 1: 108/157 (resto = nombres propios → CER_MAX 0.06 en guion.py; reescritas p01_2, p14_1, gracias2_1 y fonética «Parada once»→«ónse», Dolanaar, Kharanos) → `voz` + `seleccionar` RELANZADOS (`_voz2.log`, `_sel2.log`, 19-nov ~16:10). Si quedan rechazadas, leer hyp en voz/eval.json. Luego: `fab.py wow_ruta_forever seleccionar` hasta 157/157 (Applio da siempre la misma toma: leer `hyp` en `voz/eval.json`; nombre propio → `CER_MAX_POR_FRASE`; otra cosa → reescribir frase) → `python nucleo/idioma_voz.py wow_ruta_forever` → `tiempo` → `beats`.
- 2) ✅ HECHO y probado (parada, curva_xp, bifurcacion; `python nucleo/mg_ruta.py` → %TEMP%/_mg_ruta_pruebaN.jpg, mirado). `nucleo/mg_ruta.py` NUEVO (MG nuevos, regla de oro 4), API como `nucleo/mg_oro.py` (helpers de mg_wow: _base, _eo, _mk, _pegar, _pop, _salida, _sello, _texto, fuente, icono): `parada(n, nivel_a, nivel_b, zona_titulo, zonas_alianza, zonas_horda)` tarjeta de capítulo con barra de niveles 1-60 que se llena y dos columnas Alianza (azul) / Horda (rojo), una por marca · `curva_xp(titulo, [(10,27600),(20,167200),(30,499000),(40,1154400),(50,2306100),(60,4084700)], sombra 30-60 «88 %»)` para el gancho · `bifurcacion(titulo, raiz, izq, der, remate)` = al 36-38 la ruta se parte: Alianza a pie (Villa del Lago → Colinas Espinosas → Farholde) / Horda en barco (muelle de Tanaris → Puerto Polvomecha → Rog'mar) · cifras de misiones con `M.contadores` (151 Claros del Río, 143 Hyjal, ~144 Zephras). Probar como `python nucleo/mg_oro.py` (imagen de prueba en %TEMP%) y mirarla.
- 3) ⏳ subagente 3 LANZADO (19-nov ~15:50) → `_busquedas.py` + `_candidatos.json` (comprobar `python _busquedas.py --check`). Luego: `_busquedas.py` (copiar de wow_oro_forever; búsquedas «WoW Forever <zona>», longplays sin narrar; Claros del Río = «WoW Forever Riverglades») → `bajar -j 4` → `python nucleo/texto_clips.py wow_ruta_forever -j 4` → hojas `medios` (mirar) → rehacer.
- 4) efectos.py (helpers de `../wow_oro_forever/efectos.py`: pv/rel/cam/ban/com/mapa/pant/carr): por parada `mg_ruta.parada` + `mapa()` de su zona con los puntos de `_coords.md` + pegatinas; 12 `com()` (ids en guion.py, cabecera); mapa general con las 14 paradas al final del gancho y en el cierre. Luego promesas.md + `_promesas.py` → pegatinas_check → `chequeo` → `FAB_FX_FINAL=1 fx hoja` (mirar todo).
- 5) ✅ `musica_wow.py` + `LYRIA.tramos` escritos y OST bajada (17 temas, audio/wow/); falta comprobar ≤ 175 s por tramo tras `tiempo` y correr `python musica_wow.py` (≤ 175 s por tramo) → `musica` → `sfx` → `mezcla` → `video` → `final` → `verificar` → (regla 10: no hay citas de audio).
- 6) miniatura Flow (que parezca el juego: mapa/ruta con «1→60», texto de Nano Banana) · youtube.json (copiar de wow_oro_forever; SIN Overgear, capítulos por parada, título «La RUTA del 1 al 60 en WoW Forever, zona por zona») · `yt subir wow_ruta_forever cronicas_warcraft private --publicar 2026-11-23T15:00:00Z` · monetización en Studio (R07) · publicados + BITACORA + `canales --actualizar` · commit (con nucleo/mg_ruta.py).

- ✅ 19-nov ~16:50: voz 157/157 (Voz total ~1324 s; tiempo 23:28 antes del arreglo de Gnomeregan) · reescritas p01_2, p11_0 («once» sonaba en inglés → «Seguimos con la siguiente parada»), p14_1, gracias2_1 · fonética Gnomeregan → `voz`+`seleccionar` 157/157 OK; `idioma_voz` relanzado (falta `tiempo` → `beats` otra vez).
- ✅ subagente mapas/pegatinas: 47 mapas (`mapas/_fuentes.txt`; Zephras/Riverglades/Shen'dralas en enus; Hyjal de la wiki; `mundo_forever.jpg` vista general cosida con `_mapa_mundo.py`), `_coords.md` por parada (hojas `previews/_coords_check_*.jpg` miradas), 87 pegatinas (`pegatinas/_creditos.json`, hoja `previews/pegatinas_check.jpg` mirada). OJO al montar: Peste del Este → `peste_este_forever.jpg`; Ciudad Anegada → `tuercespina_oeste.jpg` + zoom `ciudad_anegada_isla.jpg`; Alcaz → `alcaz_isla.jpg`; Atal'Hakkar 70.0,52.9; Roca Negra 29.5,36.0; Avanzada del Sur en el mapa de Claros del Río 37.6,74.7. Sin imagen: Shen'dar, Avanzada del Sur, Refugio Faucedraco, Rog'mar, lagos en herradura, Mordent, campamento thalassiano, Santuario de Aviana, Cima de la Eternidad → cubrir con mapa/clip o Flow «como captura real».

- ✅ idioma_voz OK (157) · tiempo 23:28 (1408 s) · beats 164 · subagente clips: `_busquedas.py` (173 fuentes, --check limpio; ojo ids RKcqwk8Ivtg/C5T25m4AIDY marca ROBOT89, R86WtDgehJY «XP: 28», Og-F93kmgbI/QVin8qs0h4A@190 mapa abierto, 8aBwVTAnZLI@3950 clan; p11 Azshara y p09 Shen'dralas flojas) · busquedas.json ✅ · `bajar -j 4` LANZADO 19-nov ~17:20 (`_bajar.log`). Siguiente: texto_clips → medios (mirar hojas) → rehacer → efectos.py.

- ✅ efectos.py ESCRITO (119 efectos, `fx --seco` OK sin efectos < 3 s): 14 tarjetas `R.parada`, ~35 mapas con ruta y fotos, bifurcaciones (gancho y nivel 38), curva_xp, contadores, 13 `com()`, pegatinas. OJO: el ancla «texto|fin» = fin de ESE texto; y un ancla repetida en el guion casa con la primera (usar trozos únicos). Siguiente: al acabar `bajar` → texto_clips + hojas medios + rehacer + promesas + chequeo + `FAB_FX_FINAL=1 fx hoja` (mirar) → render.

- ✅ bajar 156/164 · subagente 4 LANZADO (revisión visual: 8 fallidos, texto_clips, medios, promesas, pegatinas_check, chequeo, `FAB_FX_FINAL=1 fx hoja`) · ✅ OST armada (`python musica_wow.py` + `fab.py musica`, 18 tramos ≤ 130 s) · sfx corrido. Al acabar el subagente: `fx` → `mezcla` → `video` → `final` → verificar.

- REVISIÓN VISUAL (subagente, 19-nov):
  - ✅ 1 bajar 164/164 (8 fallos transitorios de ffmpeg reintentados).
  - ✅ 2 medios: hoja propia de 3 cuadros por clip mirada entera → 53 beats rehechos en 2 rondas (FIJO en _busquedas.py, motivos en _rehacer.txt: clip de otra zona/mazmorra, ROBOT89, rótulo «SHADOWFANG KEEP», mapas/ventanas abiertas, plano repetido). texto_clips relanzado (`_texto.log`).
  - ✅ 3 promesas: `_promesas.py` + `promesas.md` (168 frases) → previews/promesas_01..14 miradas. Añadidos al final de efectos.py 12 mapas (El Cruce→Trinquete, Roca del Sol, Villa Oscura, Molino Tarren, Hachazo/Zoram'gar, Thalanaar, Rocal, Uldaman, vuelos de Farholde, muelle goblin, Fauces de Madera) + pegatina barco de Menethil; corregidos: tiempos del mapa de Los Baldíos, carrusel Dalaran/Cima (su 2.ª marca casaba en el min 8), lagos ↔ pueblo de Claros, foto de Thunder Bluff quitada del punto de Zephras, Whelgar fuera (rótulo encimado), pegatinas que se quedaban sobre el mapa siguiente (Kargath→Rocal, Capilla→Faucenegra, filav del inicio). 3 clips más (029 051 084).
  - ✅ 4 pegatinas: `_peg_check.py` → previews/pegatinas_check_01..04 (79) miradas: identidad OK (fuentes en _creditos.json).
  - ✅ 5 chequeo: densidad mg 1,7 (canal 1,1) · mapas 2,5 (0,7) · pegatinas 1,9 (1,8) tras añadir 10 pegatinas + 1 MG; idioma OK; sonido = falsos positivos (así suena, voces, escuchando); OCR 102 clips = HUD del juego (misiones, nombres, chat), revisado.
  - ✅ 6 `FAB_FX_FINAL=1 fx hoja` (fx_01..08, 143 efectos) mirada 3 veces + cuadros sueltos: mapa de las 14 paradas ahora sobre `mapas/mundo_forever_ancho.jpg` (mar a los lados: antes se cortaban Zephras, Cuna y Bahía del Botín y se encimaban «13 · Cuna»/«14 · Hyjal»; marcas a 1,0 s y 0,65 s para leer cada rótulo), bandas de Claros con foco al sujeto, camafeo cielonato con foco a la cara, Jintha'Alor sacado del mapa a pegatina (su rótulo tapaba el pin de Sañadiente), rótulos rojos movidos (tapaban rótulos de mapa), tarjeta parada 2 / MG / comentarios recortados para no pisar el mapa siguiente, MG «HASTA EL NIVEL 20» (faltaba su 2.ª marca: tumbaba la hoja). `fx --seco` sin efectos < 3 s. LISTO PARA RENDER (no lanzado).
  - Dudoso para el usuario: 18:27 «La Garganta de Fuego, Frondavil y Las Tierras Devastadas» va sobre clip de Un'Goro (no hay clip ni pegatina de esas zonas) · «Bolsa de dormir acogedora» y «juguete de Legado» sin imagen del objeto (rótulo en el juguete) · Thalanaar y Avanzada del Sur caen en el borde de su mapa.

- ✅ subagente 4: revisión visual completa (59 clips rehechos en FIJO, `_rehacer.txt`; 12 mapas + 11 pegatinas + 1 MG + 4 rótulos añadidos; densidad MG 1,7 · mapas 2,5 · pegatinas 1,9/min; fx hoja limpia). Dudas para el usuario: 18:27 Garganta de Fuego/Frondavil/Devastadas sobre clip de Un'Goro; Bolsa de dormir y juguete de Legado sin imagen; Thalanaar y Avanzada del Sur en el borde de su mapa.
- RENDER LANZADO 19-nov (fx → mezcla → video → final; `_render_<etapa>.log`). Si `mezcla` cae por RAM: ver lecciones de wow_oro_forever (reiniciar). Luego: verificar → miniatura Flow → youtube.json → subir 2026-11-23T15:00:00Z → monetización → registro → commit.

- ✅ youtube.json (SIN Overgear, 16 capítulos) · ✅ miniatura Flow `salida/miniatura.jpg` (mapa-pergamino con ruta 1→60, medallones Claros/Hyjal, orco de espaldas; ojo: piel del orco amarillenta; receta y proyecto en `prompt_miniatura.md`).

- ✅ MASTER `salida/wow_ruta_forever_MASTER.mp4` (1051 MB, 1080p, 1428,7 s) + .srt · verificar ✅ · final_hoja mirada. Sin citas de audio (regla 10 no aplica).
- `yt subir … private --publicar 2026-11-23T15:00:00Z` LANZADO 19-nov ~20:55 (`_subir.log`). Luego: monetización en Studio (R07) → `yt monetizado <id>` → publicados (formato) + BITACORA + `canales --actualizar` → commit (incl. nucleo/mg_ruta.py).

## Hecho
- carpeta creada (`fab.py nuevo wow_ruta_forever --yt`), canales actualizados (hueco lun 23-nov 09:00 libre).

## Falta
- [ ] guion → voz → seleccionar → idioma_voz → tiempo → beats → busquedas → bajar → medios → efectos/mapas/pegatinas → promesas → chequeo → fx hoja → OST → sfx → mezcla → video → final → verificar → citas audio → miniatura Flow → youtube.json → subir 2026-11-23T15:00:00Z → monetización en Studio → registro + commit

## Lecciones de este video (solo lo no obvio)
- ...

## Cierre (regla del 12-oct-2026)
- [x] subido y PROGRAMADO (Rcu_3ztFANk, 23-nov 15:00Z), monetización activada (mid-roll + cuestionario), registrado (`canales/cronicas_warcraft.json`, BITACORA), commit 2d8c1e4
- [ ] HALLAZGOS documentados en el manual/estilo
