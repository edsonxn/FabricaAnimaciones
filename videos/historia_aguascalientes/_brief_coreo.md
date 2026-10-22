# Brief para escribir un tramo de coreografía (historia_aguascalientes, Cronopapel, 22-oct-2026)

Video «La historia de Aguascalientes» (13:05), estilo BOCETO + GUACHE en plano secuencia sobre un mapa con relieve real; los dibujos
son PEGATINAS DE FLOW ya recortadas y hay FOTOS REALES como pegatinas de foto. Lee ANTES (en este orden):
1. `docs/estilo_boceto_guache_mapa.md` (grep/por secciones: «Reglas», «SFX», «Dibujos en Flow»: ajustes de historia_jalisco) — reglas del canal:
   MUCHOS elementos, un dibujo por frase, NADA de mapa solo > 1,5 s, cada escena empieza con una pegatina en i0, personas en el mapa s ≥ 0,5.
2. `videos/historia_jalisco/coreo_1.py` y `coreo_3.py` = EJEMPLO a imitar (API: ga, pa, titulo, lugar, ciudad, R.camara, R.terreno, R.texto,
   R.snd, R.anio, R.sello, R.ruta, R.contador, R.mar, andar_ciclo, grupo_ciclo, ciclo_pant, kf, T/INI/FIN). `T(e, "palabra")` busca la palabra
   SIN acentos en la escena (usa `frase=` si la palabra se repite o es común: «que», «el», «mil»…).
3. Aquí: `guion.py` (frases de tus escenas, `FOTOS` con la clave de cada foto), `_mapa_notas.md` (claves de CIUDADES, RUTAS y campos de
   `R.terreno`), `coreo_peg.py` (ATAJOS de hojas: HAY QUE ACTUALIZARLO, ver abajo), `fotos/LEEME.md` (FotoPeg), `ESTADO.md` (lista de piezas NN de
   cada hoja: «Piezas (NN)»), `piezas/<hoja>/_indice.jpg` (míralos), `sellos.py` (emblemas: aguila, aguila_nopal, balanza, campana, columnas,
   corona, espadas, gorro, libro, locomotora, maiz, olmeca, piramide_mx, sombrero_rev, torre_petroleo), `obj_c.py` (cronometro, campana…).

## Reglas de trabajo en paralelo (IMPORTANTE)
- Escribe SOLO tu archivo `coreo_N.py` (funciones `cortes(R)` y `construir(R)`, como en Jalisco). NO toques escenas.py, guion.py, core.py,
  mapa.py, coreo_peg.py, foto_peg.py, ni los demás coreo_*.py. Los atajos de hojas: defínelos AL PRINCIPIO de tu archivo, p. ej.
  `from pegflow import P, ciclo` · `CH = lambda n, **k: P("01_chichimecas_hoja", n, **k)` … y los ciclos `ciclo("11_chichimeca_corre")`.
  Hojas: 01_chichimecas_hoja, 02_plata_hoja, 03_fundacion_hoja, 04_colonia_hoja, 05_xix_hoja, 06_arte_hoja, 07_porfiriato_hoja,
  08_revolucion_hoja, 09_sigloxx_hoja, 10_turismo_hoja; ciclos 11_chichimeca_corre, 12_soldado_marcha, 13_carreta_camina, 14_villa_galope.
  `andar_ciclo`/`grupo_ciclo`/`ciclo_pant` se importan de coreo_peg (funcionan con cualquier lista de cuadros).
- Fotos: `import foto_peg as FP` → `pa(R, FP.F("convencion_9"), x, y, FP.s_para(0.48), t0, t0 + 4.5, entra="pluma")`. Pon CADA foto de
  `guion.FOTOS` de tus escenas en su frase (~4-5 s, a un lado, sin tapar el rótulo; el mapa y otras pegatinas siguen vivos alrededor).
- Rótulos de LUGARES PARA VISITAR (el usuario lo pidió): cuando la frase dice que algo se puede visitar hoy, un rótulo corto tipo
  «HOY: MUSEO JOSÉ GUADALUPE POSADA» o «SE PUEDE VISITAR» con un pin/flecha en el mapa (`ciudad`/`lugar`). Fechas grandes con `R.anio`.
- `sem` (semilla de temblor): usa SOLO tu rango (te lo doy abajo). Capas de `R.terreno`: limpia las tuyas al salir (como Jalisco).
- Cámara: tu primer `R.camara` en INI(e) - 0,2 de tu primera escena; el último en FIN + 0,4 de tu última. Zooms útiles: caja z 0,74,
  estado z 1,7-1,8, región 2,5-3,5, capital 4-6,5 (no más). Movimiento continuo y suave (plano secuencia), nunca quieto > 2 s.
- SFX: usa nombres del sintetizador del kit (pop, whoosh, escribir, campana, galope, tambor, fuego, crujido, pluck, sello, fanfarria,
  impacto, canonazo, monedas, papel, pasos, ola, crece, golpe_suave…) y/o los de `guion.SFX_ELEVEN` (flecha, tren, agua_termal, beso,
  multitud, feria). Si necesitas uno nuevo, úsalo con un nombre nuevo y apúntalo en tu respuesta final con un prompt en inglés y segundos
  (yo lo añado a SFX_ELEVEN). No repitas el mismo SFX en cada pegatina (regla «SFX repetidos, no»).
- PROBAR: `./run.sh _prueba.py t1 t2 … --out=<tuyo>` (hoja en `previews/<tuyo>.jpg`, 960x540; `--full` además a 1920). Mira un cuadro cada
  ~3 s de tus escenas y corrige: nada vacío > 1,5 s, pegatinas no diminutas ni cortadas por el borde, textos que no choquen ni se salgan,
  fotos legibles. `python -m py_compile coreo_N.py` antes de cada prueba; si escenas.py imprime «⚠ coreo_N …», el error es tuyo.
  Al final, una hoja de revisión de TODO tu tramo cada 3 s (`./run.sh _hojas.py 3 <t0> <t1>` escribe previews/rev_NN.jpg — renómbralas a
  `previews/rev_<tuyo>_NN.jpg` en seguida porque otros usan el mismo nombre) y MÍRALAS.
- Responde (≤ 15 líneas): qué hiciste por escena, SFX nuevos que pides (nombre, prompt, segundos), problemas del kit que viste.
