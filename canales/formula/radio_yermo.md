# Fórmula — Radio Yermo (`radio_yermo`, Fallout)

## Alta del 17-nov-2026 (canal nuevo, 0 subs; creado por Claude bajo la cuenta de Google de Edsonxn)
- **Pedido del usuario:** «similar al de Crónicas de Tamriel, pero de Fallout. Misma receta, todo igual… ponle un nombre
  interesante, no hay que repetirlo de "Crónicas de"». Promoción desde los próximos videos de Tamriel (`docs/estilo_secuencia_yt.md`
  § «CANAL HERMANO»; la línea de la descripción la pone `yt subir` sola con `promo_canal`). **18-nov-2026: la mención va AL FINAL
  de los videos de Tamriel (cierre + pantalla final «Canal») y solo desde que aquí haya ≥ 2 videos públicos; nunca a la mitad.**
  Lo que se mide aquí: subs el día de cada video de Tamriel y fuentes «pantallas finales» / «canales de YouTube» / sugeridos.
- **Nombre:** «Radio Yermo» (@RadioYermo, UClZr07HzwBSQbMgOvdSej_w). «El Yermo» es como los Fallout en español llaman a *the
  Wasteland*, y el canal es una radio que transmite desde el fin del mundo, como las radios de los propios juegos. Sin «Crónicas».
- **Por qué Fallout en español (NexLev, 17-nov):** los 15 canales que más se parecen a lo que haremos (listas, secretos, lore de
  Fallout) están TODOS en inglés: Echo (28 mil subs, outlier ×7,4), Explainatron (×3,8), Prizmere (×2,4), yaboiii (83 mil, ×2,0),
  SequentialGamer_Fallout, Calm Loremaster y Wasteland Sleep Protocol (lore largo «para dormir»). En español el hueco está libre.
  Público compartido con Tamriel (Bethesda, mismo motor de juego, mismo tipo de jugador): la promo cruzada tiene sentido.
- **Fórmula de arranque = la de Tamriel que ya funciona allí:** listas «NUNCA debes hacer» (Tamriel ×10-×13, el filón), «lo más
  ROTO/PODEROSO», «lo más INÚTIL», «secretos que te perdiste» de 12-20 min; luego lore largo «para dormir» (Calm Loremaster /
  Wasteland Sleep Protocol). Cambiar UNA variable cada video.
- **Frecuencia y hora (provisional):** ciclo 4 días, 17:00 CDMX; se ajusta con datos tras los primeros 3 videos.
  **17-nov-2026 (el usuario): desde el 2.º video, los MISMOS tiempos que Crónicas de Tamriel = ciclo 3 días, 09:15 CDMX.**
- **Voz (elegida por el usuario el 17-nov-2026): el Profeta con el filtro de radio del Yermo en modo B** (`nucleo/fx_radio.py`): idea
  suya, «que se escuche como la radio del juego, con esos filtros». Probó 6 locutores (Jose, Zabra, Juan Pablo, Brian C, Bardo, Carlos
  Pro) y dudó con Brian C en modo B. A vigilar: si en Tamriel se reconoce la voz (comentarios «es el mismo de Tamriel») y si el
  filtro cansa (quejas de audio); el modo C queda de respaldo.
- **Conectado (17-nov-2026):** el usuario lo verificó y lo conectó a la API; idioma es-419 puesto por API. `yt subir` ya puede publicar.
- **Falta (1.er video):** `python fab.py ideas radio_yermo` → 3 temas con video de referencia y ×; kit `nucleo/mg_fo.py` con capturas
  reales del Pip-Boy; ajustar el tema `fo` de `mg_mapa`.
- **A vigilar:** % visto ≥ 35 y vistas/día de los 3 primeros largos; subs que llegan desde Tamriel (fuente de tráfico).

## Conclusión del 17-nov-2026 (1.er video `fo_nunca_f4`)
- **Fuera (ideas 60 d):** Wastelander «Hidden Fallout NV/3/4 Enemies» ×6,5-×7,3 (canal de 13,8 mil); Oxhorn lore largo ×9,9; en Shorts
  SparkMark ×11-×14 y «Crónicas del Yermo» (57 mil subs, SOLO Shorts en español, ×3,4-×3,7: «El lugar más RADIOACTIVO», «La MEJOR
  Servoarmadura»): en español sí hay Shorts de Fallout, pero no listas largas.
- **Referencias del tema:** IGN «9 cosas que NO debes hacer en Fallout 4» 796 mil (español, 2 años); SmackerUnknown «10 Mistakes ALL Fallout 4
  Players Make» 99 mil en 1 mes y «10 Things You Should Do EARLY» 212 mil; Big Dan «69 Secrets ONLY Veteran Players Know» 389 mil.
- **Decisión (el usuario eligió entre 3):** «Las 15 cosas que NUNCA debes hacer en Fallout 4» = la fórmula ganadora de Tamriel (×10,7) con el
  juego de más público. Reserva: «Los 30 SECRETOS de Fallout 4» y «Las 10 armas más ROTAS de New Vegas».
- **Comentarios:** canal sin videos → este video va sin agradecimientos ni críticas; se pide suscripción sin cifra (0 subs).

## 2.º video `fo_refugios_25` (17-nov-2026, pedido directo del usuario)
- «Top 25 de los refugios más raros/malvados/hardcore de Fallout», ≥ 30 min, el n.º 1 = el peor refugio. Cambia DOS variables respecto al 1.º (largo y lore en vez de «NUNCA»): pedido del usuario, no elección por datos. Lo que no tenga imagen/video se recrea en Flow con gráficos de FO3/FO4 (marcado RECREACIÓN).
- Comentarios: el 1.er video aún no sale (18-nov) → 0 comentarios; este va sin agradecimientos ni críticas.

## 3.er video `fo_enemigos_ocultos` (23-nov-2026, Claude con datos; OK del usuario en «buenos días»)
- «15 ENEMIGOS ocultos de Fallout que casi nadie vio» (15:23, f2zKynItV6U, mié 25-nov 09:16): referencia Wastelander «Hidden Fallout NV/3/4 Enemies» ×7,3/×6,5/×3,4; vuelve a ~15 min y cambia el tema a «ocultos/secretos» en tres juegos.
- MAPAS: las coords salen del mapa interactivo de la wiki (`Map:FO3 World Map`, `Map:FNV World Map`, `Map:Fo4 Commonwealth`, y de DLC `Map:FO3PL…`, `Map:FNVOWB…`, `Map:FNVLR…` con su imagen base): misma textura que `mapas/<juego>.png` → sin template matching. Script: `videos/fo_enemigos_ocultos/mapas/_wiki/busca.py`. Nuka-World y la Isla: la imagen base de la wiki no está como archivo → sin mapa.
- A vigilar: % visto y vistas/día frente a los dos primeros; si «ocultos» rinde más que «NUNCA», repetir con FO76 o con la serie.
