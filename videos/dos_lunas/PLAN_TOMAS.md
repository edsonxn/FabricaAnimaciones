# Plan de tomas — «¿Qué pasaría si la Tierra tuviera DOS Lunas?» (plano secuencia, ~6 min)

Tiempos REALES (`fab.py dos_lunas tiempo`, 12-oct-2026; voz 309,6 s, video 5:50, 68 frases con CER 0).
Cada toma es una transformación continua de la anterior (sin cortes). `Mundo` único; Tierra en el origen del mundo.
Sesión 2 = tomas 1–5 (0:00–2:44, con render parcial `--hasta 90`); sesión 3 = tomas 6–10 (2:44–5:50).

| # | escena | ~tiempo | toma (qué pasa en pantalla, de qué a qué) | kit / SFX clave |
|---|---|---|---|---|
| 1 | `intro` | 0:00–0:22 | Plano cerrado de la Luna (cráteres, gira con `rot`), Kuri flotando que la mira → la cámara se aleja y aparece la Tierra → **segunda Luna** entra con destello + `?` (pop). «Mareas» = una ola dibujada sube y baja un instante; «ya tuvimos dos» = silueta de dos lunas con `?`. | `cuerpo_rocoso`, `destello`, `kuri`, `tierra` |
| 2 | `hoy` | 0:22–0:41 | Tierra–Luna con `regla` «384 400 km»; **81 lunitas** se apilan hasta formar el disco de la Tierra («1/81»); la Luna tira y el agua se abulta (`tierra_marea` una luna + `flechas_marea`, lado cercano más fuerte). | `regla`, `tierra_marea`, `flechas_marea` |
| 3 | `origen` | 0:41–1:23 | 3 mini-actos en el mismo espacio: (a) **captura**: asteroides pasan de largo y uno se curva y se queda; recuadro de Neptuno con Tritón (`planeta_gas` hielo); (b) **mini-luna 2024 PT5**: roca de 11 m da 1 lazo (rótulo «29 sep – 25 nov 2024») y se va; (c) **choque gigante**: un cuerpo golpea la Tierra joven, escombros → anillo → se juntan en la Luna y un 2.º grumo. | `roca`, `orbita`, `estela`, `anillo_escombros`, `planeta_gas` |
| 4 | `orbita` | 1:23–2:13 | Zoom-out enorme: `esfera_hill` de 1,5 M km con el Sol empujando desde un lado; órbita estable (< ½); **dos lunas en órbitas parecidas** se estorban y chocan/una sale disparada; recuadro de Saturno con **Jano y Epimeteo** intercambiando órbita; final: `triangulo_equilibrio` y la 2.ª luna en **L4** persiguiendo a la Luna (guardar ESTE encuadre: reaparece en la toma 9). | `esfera_hill`, `orbita`, `punto_lagrange`, `triangulo_equilibrio` |
| 5 | `cielo` | 2:13–2:44 | Inmersión en la Tierra (`Sup`): cielo de noche con **dos lunas** separadas ~6 puños (Kuri levanta el puño como regla); dos iconos de fase con ~5 días de desfase; corales/animales que dudan; al final la 2.ª luna **se acerca** y crece (transición a la toma 6). | `cuerpo_rocoso(fase=)`, `Sup`, `kuri` |
| 6 | `mareas` | 2:44–3:23 | Vuelta al espacio con la 2.ª luna a 192 000 km (`regla`, «×8» con curva 1/d³ dibujándose); la Tierra con `tierra_marea` enorme; inmersión a una costa: el mar sube metros, regla de **16 m (Fundy)** junto a la ola; las dos lunas se alinean y el agua se suma. | `tierra_marea`, `regla`, olas 2D |
| 7 | `calor` | 3:23–3:49 | Corte de la Tierra: el manto se estira y se frota (calor naranja); recuadro de **Ío** con plumas de volcanes (`cuerpo_rocoso volcanica`); la Tierra con volcanes que se encienden. | `fumarola`, `cuerpo_rocoso` |
| 8 | `caida` | 3:49–4:41 | Flechas de deriva: la Luna **se aleja** 3,8 cm/año; luna retrógrada/rápida **cae**; recuadro de Fobos (1,8 m por siglo); círculo del **límite de Roche** (9 500–18 400 km del centro); `luna_rota` se estira → se parte → `anillo_escombros` + `lluvia_rocas` sobre la Tierra. | `luna_rota`, `anillo_escombros`, `lluvia_rocas`, `regla` |
| 9 | `choque` | 4:41–5:32 | Dos lunas chocan; cámara a la Luna real: **cara visible lisa vs. cara oculta con montañas** (giro con `rot`); reconstrucción: la luna de 1 200 km en L4 (reutiliza el encuadre de la toma 4) se desestabiliza y se aplasta como panqueque en la cara oculta (impacto lento, sin cráter); rótulo «hipótesis». | `cuerpo_rocoso(rot=)`, `roca`, `punto_lagrange` |
| 10 | `cierre` | 5:32–5:50 | La Luna sola, tranquila, mareas suaves; Kuri se sienta a mirarla; cielo de noche con estrellas; «es la única que nos quedó» → fundido final. | `kuri`, `F.estrellas` |

## Estado del código (13-oct-2026, sesión 2: tomas 1–5 dibujadas y probadas con `escena <id> t…` y `_cuadro.py`; tomas 6–10 más abajo)
Módulos: `mundo_comun.py` (anclas `T()`, `kf`/`cam_claves`, `Cam`, `Sup`, `pop`, `ventana`), `anclas.py` (130 palabras ancladas de las
tomas 1–5; **añade las de 6–10 aquí**), `mundo_espacio.py` (constantes ER=100, RL=700, MR=52, HILL=2680; `ang_luna`/`luna_mundo`/`radio_luna1`;
`cam_espacio` con claves hasta t=133; toma 1–2; helpers `fantasma`, `marca_x`, `bez2`, `kepler`, `trail`, `chip`, `fondo_comun`, `kuri_ui`),
`mundo_origen.py` (toma 3), `mundo_orbita.py` (toma 4; `toma_L4(lz,t,cam,E,r_m,fade)` es el encuadre de L4 **para reutilizar en la toma 9**),
`mundo_tierra.py` (toma 5: `cam_inmersion`, `paisaje`, `corales_y_vida`, `cielo_dos_lunas`), `escenas.py` (`render_mundo` despacha por tiempo
+ `registrar_sfx` de las tomas 1–5: 96 eventos).
- **Empalme con la toma 6 (2:44):** la toma 5 termina con el cielo de la costa (superficie plana, `Sup(960, 700, 1, 0)`), Kuri en la playa
  (X=-790) y la 2.ª luna enorme en pantalla (centro ≈ (1440, 440), radio ≈ 295 px, `MT.pos_luna2(t)`). La toma 6 sale de ahí: cámara que
  se aleja (inverso de `MT.cam_inmersion`) hasta el espacio, con la 2.ª luna ya a 192 000 km (radio de órbita ≈ 350 en el mundo).
- La luna 2 «de verdad» en el espacio es `MO.luna_joven_2` hasta el 84 s y luego fantasma; en L4 es `ang_luna(t)+π/3` a radio 700.
- Kuri es overlay con posición por claves (`kuri_ui`): en cada toma nueva hay que empalmar su posición con la de la toma anterior.
- Coste medido por cuadro (1080p, 1 proceso): tomas 1–3 ≈ 0,6 s; toma 4 y la caída ≈ 1,1–1,9 s; superficie ≈ 0,5 s.

### Tomas 6–10 (sesión 3, 13-oct-2026; probadas con `escena <id> t…` y los empalmes 5→6, 6→7, 7→8, 8→9; hojas en `previews/esc_*.jpg`)
- `mundo_mareas.py` (toma 6, `toma_6`): salida de la playa → espacio con cotas «192 000 km / 384 400 km» y curva 1/d³ «×8» → inmersión a
  la costa con medidor y récord de Fundy (16 m) → suma de las dos lunas (`CLAVES_M` = nivel del mar por claves, hasta 26 m) → salida al espacio
  (`T_SAL`, `T_INM`, `T_SAL2`). `mundo_calor.py` (toma 7, `toma_7`): Tierra en corte con cuña de manto que se estira/frota, termómetro, inset de
  Ío con plumas, volcanes. `mundo_caida.py` (toma 8, `toma_8`): deriva de la Luna, luna retrógrada que cae, Fobos, límite de Roche
  (`R_IN`/`R_OUT`), luna que se estira y parte, anillo y lluvia de rocas (empalma con la toma 9). `mundo_choque.py` (toma 9 `toma_9` y toma 10
  `toma_10`; `toma_9_10` las despacha y aplica el fundido final): choque de las dos lunas, caras de la Luna (giro con `rot`), hipótesis de 2011,
  L4 (`escena_L4`), panqueque, cierre en la playa con UNA luna y tres tarjetas.
- `escenas.py`: `render_mundo` despacha por tiempo a las 10 tomas; `registrar_sfx` = 196 eventos (96 de las tomas 1–5 + 100 de 6–10).
- Fondos por toma (cada una con su tinte): NEB6 azul/verde, NEB7 rojo/magenta, NEB8 azul/rosa, NEB9 violeta/naranja.
- Coste por cuadro (1080p, 1 proceso): tomas 6–8 ≈ 0,8–1,8 s; 9–10 ≈ 0,55–1,3 s. Render completo estimado 1–1,5 h con 8–12 procesos.
- Cuidado con rótulos/tarjetas sobre el foco: en el cierre las tarjetas tapaban la Luna (M_C = (1180, 300), r 118); se movieron a x = 560 / 900 / 1620.

## Notas de producción
- Las tomas 4 y 9 comparten el encuadre de L4 (promesa y desenlace): dibujar una sola vez como función `escena_L4(lz, t, u)`.
- Reparto de sesión 2: intro, hoy, origen, orbita, cielo (hasta 2:44).
- Comprobar cada toma con `escena <id> t1 t2 ...` y la hoja 2×3 (1 cuadro/3 s) del MASTER antes de dar nada por bueno.
- SFX: un `ev(...)` por concepto nuevo (pop, ding, whoosh, impacto, zap) sin repetir el mismo sonido por cada pieza (memoria «sfx-repetidos-no»).
