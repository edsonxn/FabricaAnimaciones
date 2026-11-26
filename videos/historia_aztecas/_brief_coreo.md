# Brief para escribir un tramo de coreografía (historia_aztecas, Cronopapel, 23-nov-2026)

Video «Toda la historia de los AZTECAS» (18:20), estilo BOCETO + GUACHE en plano secuencia sobre un mapa con relieve real (Valle de México
con los LAGOS de 1519 + centro de México); los dibujos son PEGATINAS DE FLOW ya recortadas y hay FOTOS REALES como pegatinas de foto.
Es la primera prueba del formato LARGO «historia COMPLETA» con un PERSONAJE FIJO: **Xolo**, un xoloitzcuintle gris con pañuelo rojo
que acompaña toda la historia (chiste que se repite: siempre a un paso de terminar en el menú). **Xolo sale en CADA escena tuya al menos
una vez** (pequeño, en una esquina del encuadre o junto a la acción, reaccionando: asustado, escondido, olfateando, saltando), y
grande cuando la voz lo nombra.

Lee ANTES (en este orden):
1. `C:\FabricaAnimaciones\docs\estilo_boceto_guache_mapa.md` (por secciones: «Versión 2.1», «Dibujos en Flow», «historia_aguascalientes»,
   «REGLA del usuario… MÁS FOTOS REALES», «Ubicación en México»): MUCHOS elementos, un dibujo por frase, NADA de mapa solo > 1,5 s, cada escena
   empieza con una pegatina en i0, personas en el mapa s ≥ 0,5, ≥ 3 fotos reales por minuto.
2. EJEMPLO a imitar: `C:\FabricaAnimaciones\videos\historia_aguascalientes\coreo_1.py` y `coreo_3.py` (API: ga, pa, titulo, lugar, ciudad,
   R.camara, R.terreno, R.texto, R.snd, R.anio, R.sello, R.ruta, R.contador, R.mar, andar_ciclo, grupo_ciclo, ciclo_pant, T/INI/FIN).
   `T(e, "palabra")` busca la palabra SIN acentos en la escena (usa `frase=` si la palabra se repite o es común: «que», «el», «mil»…).
3. Aquí: `guion.py` (frases de tus escenas; la voz ya está y `timeline.json` tiene los tiempos), `_mapa_notas.md` (claves de CIUDADES,
   RUTAS, campos/territorios y encuadres z recomendados), `fotos/creditos.json` (cada clave con `"que"` = qué se ve) y `fotos/_indice.jpg`
   (MÍRALO), `fotos/LEEME.md` (FotoPeg), `piezas/<hoja>/_indice.jpg` de cada hoja que uses (MÍRALOS: la numeración NN no siempre es 0-7;
   algunas hojas tienen 9-14 piezas porque un dibujo salió en dos), `_hechos.md` (datos; nada de inventar), `sellos.py`, `obj_c.py`.
4. Hojas (en `piezas/`): 01_xolo_hoja, 01b_xolo_hoja, 01c_xolo_hoja, 24_xolo_salta (poses de Xolo), 18_mictlan_hoja (Xolo guía de almas,
   perro de Colima, criadora, Xolo con patos/olla/penacho/adiós), 02_migracion_hoja, 03_chapultepec_hoja, 04_fundacion_hoja, 05_chinampas_hoja,
   06_alianza_hoja, 07_moctezuma1_hoja, 08_vida_hoja, 09_mercado_hoja, 10_tributo_hoja, 11_axayacatl_hoja, 12_ahuizotl_hoja,
   13_moctezuma2_hoja, 14_cortes_hoja, 15_caida_hoja, 16_legado_hoja, 17_ruta_hoja. Ciclos: 19_xolo_corre (8), 20_mexica_camina (8),
   21_canoa_ciclo (6), 22_caballo_galope (6), 23_guerrero_corre (8). Los prompts que describen cada dibujo están en `flow/prompts.py`.

## Reglas de trabajo en paralelo (IMPORTANTE)
- Escribe SOLO tu archivo `coreo_N.py` (funciones `cortes(R)` y `construir(R)`). NO toques escenas.py, guion.py, core.py, mapa.py,
  coreo_peg.py, foto_peg.py, ni los demás coreo_*.py. Atajos de hojas AL PRINCIPIO de tu archivo, p. ej.
  `from pegflow import P, ciclo` · `XO = lambda n, **k: P("01_xolo_hoja", n, **k)` · `C_XOLO = ciclo("19_xolo_corre")`.
- Fotos: `import foto_peg as FP` → `pa(R, FP.F("<clave>"), x, y, FP.s_para(0.46), t0, t0 + 4.5, entra="pluma")`. Toda persona, lugar,
  objeto o códice que la voz nombre y tenga foto en `fotos/` sale en su frase (~4-5 s, a un lado, sin tapar el rótulo; el mapa y otras
  pegatinas siguen vivos alrededor). Una misma foto no se repite en dos tramos (el tuyo usa las de sus escenas).
- PROMESAS VISUALES: lo que dice la voz SE VE en ese momento (víboras, el águila con el pájaro, la serpiente de la bandera, los libros
  quemándose, el humo de chile, los perritos en el mercado, la Piedra del Sol, el tzompantli, el penacho, los bergantines…).
- Rótulos de LUGARES PARA VISITAR: cuando la frase dice que algo se puede visitar hoy, un rótulo corto («HOY: MUSEO DEL TEMPLO MAYOR»,
  «SE PUEDE VISITAR») con pin en el mapa. Fechas grandes con `R.anio`. La fuente NO tiene «→ ←» ni «≈» (salen cuadros).
- `sem` (semilla de temblor): usa SOLO tu rango (abajo). Capas de `R.terreno`: limpia las tuyas al salir.
- Cámara: tu primer `R.camara` en INI(e) − 0,2 de tu primera escena; el último en FIN − 0,25 de tu última (NUNCA FIN + 0,4: pisa al siguiente).
  Claves cada ~2 s en escenas de ciudad (CamPath añade vaivén). Movimiento continuo y suave, nunca quieto > 2 s. Usa los z de `_mapa_notas.md`.
- SFX: nombres de `guion.SFX_ELEVEN` (pop, whoosh, escribir, golpe_suave, crece, pasos, papel, tambor, caracol, flauta, pluck, brillo, impacto,
  sello, ladrido, gemido_perro, aullido, agua_lago, remo, aguila, cascabel, fuego, multitud, guajolote, flecha, batalla, canonazo, galope, ola,
  trueno, viento_frio, inundacion, cometa, llanto, tos, monedas, piedra, cincel, ciudad, campana, fanfarria, trajinera). Si necesitas uno nuevo,
  úsalo y apúntalo en tu respuesta final (nombre, prompt en inglés, segundos). No el mismo SFX en cada pegatina. Xolo con `ladrido`/`gemido_perro`
  de vez en cuando (no siempre).
- PROBAR: `./run.sh _prueba.py t1 t2 … --out=<tuyo>` (hoja en `previews/<tuyo>.jpg`; `--full` además a 1920). Mira un cuadro cada ~3 s de tus
  escenas y corrige: nada vacío > 1,5 s, pegatinas no diminutas ni cortadas por el borde, textos que no choquen ni se salgan, fotos legibles.
  `python -m py_compile coreo_N.py` antes de cada prueba; si escenas.py imprime «⚠ coreo_N …», el error es tuyo. Al final, hoja de revisión de
  TODO tu tramo cada 3 s (`./run.sh _hojas.py 3 <t0> <t1>` escribe previews/rev_NN.jpg — renómbralas EN SEGUIDA a `previews/rev_<tuyo>_NN.jpg`)
  y MÍRALAS. Corre también `./run.sh _qa_choques.py <t0> <t1>` si existe para tu rango.
- Responde (≤ 15 líneas): qué hiciste por escena, fotos usadas, SFX nuevos que pides, problemas del kit que viste.

## Reparto
| archivo | escenas | tiempo | semillas |
|---|---|---|---|
| coreo_1.py | gancho, aztlan, chapultepec, fundacion | 0-295,7 s | 1-299 |
| coreo_2.py | chinampas, alianza, moctezuma1, vida | 295,7-576,4 s | 300-599 |
| coreo_3.py | tributo, axayacatl, ahuizotl, moctezuma2 | 576,4-807,9 s | 600-899 |
| coreo_4.py | cortes, caida, legado, ruta, cierre | 807,9-1099,8 s | 900-1199 |
coreo_1 abre con `R.ubic.apertura(0.0, …)` (México entero → zoom al Valle de México) y presenta a Xolo grande en «Él es Xolo».
