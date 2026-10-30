# Pausas medidas — CFO vs KC, PARTIDA 1 (telestrador: anillos en los PIES, flechas, zonas)
Medido el 29-oct-2026 sobre las fuentes 1080p `medios/_fuente/g1_j*.mp4`. Coordenadas = fracción del cuadro COMPLETO (x, y de 0 a 1),
leídas en UN cuadro (recortes a 1280-1500 px con rejilla cada 0,01: `previews/cuadros/z_<fuente>_<t>.jpg`, más las `r_`/`h_`).
Se miden los PIES (base del modelo), no la placa. y > 0,76 = bajo el HUD → SIN anillo. «duda» = no lleva anillo (solo texto suelto).
Las RUTAS son coordenadas de PANTALLA en cada t, todas dentro de la misma toma (sin `null` en `cam_*.json` entre sus t);
la cámara se mueve entre puntos: `ruta()` debe compensar con `cam_*.json`. HUD = t + K (K de `datos_g1.md`).

## Cortes de cámara (`investigacion/cam_g1_j*.json`) y repeticiones
| Fuente | cortes (t con `null`) | tomas útiles para las pausas | repetición |
|---|---|---|---|
| g1_j1 | 26.0-26.1, 34.8 | 34.8 → fin (pausa 1) · paneo rápido 52.6-53.1 | no vista en 34.8-57 |
| g1_j2 | 16.4, 43.1-43.5, 46.7 | 16.4 → 43.1 (pausa 2) · paneos rápidos 18.5-20.4, 28.8-29.6, 31.3-32.1 | no vista |
| g1_j3 | 12.6, 45.2 | 12.6 → 45.2 (pausa 3) · paneos 18.5-19.4, 22.7-23.9 | no vista |
| g1_j4 | 26.1-26.2, 27.3, 53.4, 64.0-64.6 | 0 → 26.1 (pausa 4) · 27.3 → 53.4 (pausas 5 y 6) | **desde t ≈ 74** (datos_g1); los cortes 53.4 y 64.x pueden ser cámaras/repetición: no usar tras 53.4 sin mirar |
| g1_j5 | 11.7, 25.0-25.6, 27.9-28.0, 30.8-31.0, 33.3-33.4 | **28.0 → 30.8** (pausa 7; tomas muy cortas: el observador salta) | no vista |
| g1_j6 | 2.4, 9.6-9.7, 17.3, 34.2, 41.9, 71.8, 111.1-111.4, 149.7-150.9, 161.6, 178.3, 179.6, 186.1-186.9, 195.7-198.1, 212.2 | 41.9 → 71.8 (pausa 8) · 111.4 → 149.7 (pausa 9) | no vista en los tramos medidos |
| g1_j7 | 2.5-2.6, 9.9, 10.4, 15.6-17.4, 29.2-30.6, 40.0, 62.9-64.1, 89.4 | 30.6 → 40.0 (pausa 10) | **desde t ≈ 66** (datos_g1; cortes 62.9-64.1) |
| g1_j8 | 2.1, 18.5, 20.1-20.3, 83.2-83.4, 85.0, 88.1, 89.2, 92.7, 94.3 | (no se pausa) | — |

---
## 1 · g1_j1 · t = 51.0 (HUD 05:47) — POUT sin Destello, Busio va al arbusto
Cuadro limpio (juego en vivo, sin repetición). Yike NO se ve: está en el arbusto de abajo (aparece en t 52.2 con la placa en (0.69, 0.71) → pies bajo el HUD).
- POUT (Syndra, CFO): **0.554, 0.327** — alta
- kyeahoo (Cassiopeia, KC): **0.366, 0.476** — alta
- Busio (Nautilus, KC): **0.653, 0.608** — alta
- Yike (Wukong, KC): no visible (arbusto / bajo el HUD) — sin anillo
- Shad0w, Kino: no visibles (se retiraron tras el dragón, como dice la voz)
(a) Rutas (toma 34.8 → fin):
  - POUT: [(49.5, 0.568, 0.367), (51.0, 0.554, 0.327)]
  - kyeahoo: [(49.5, 0.365, 0.500), (51.0, 0.366, 0.476)]
  - Busio después de la pausa (si se continúa el clip): [(51.0, 0.653, 0.608), (52.2, 0.590, 0.474)] — en 52.2 POUT ya está AIRBORNE (gancho/derribo de Busio)
(b) Flecha de intención Busio → POUT: de (0.653, 0.608) a (0.554, 0.327). Zona «arbusto»: no la delimito con seguridad (abajo a la derecha, donde sale Yike: hacia (0.69, 0.78), bajo el HUD).
(c) POUT con barras llenas, nivel 5; efecto verde-azulado en (0.48-0.51, 0.31-0.38) (posible barrido/visión: duda). El Destello de POUT no se lee en el cuadro (usar la voz).

## 2 · g1_j2 · t = 26.0 (HUD 07:42) — Busio solo en el río
Cuadro limpio. Kino no aparece hasta t ≈ 31 (borde derecho).
- Busio (Nautilus, KC): **0.395, 0.569** — alta
- POUT (Syndra, CFO): **0.414, 0.320** — alta
- Shad0w (Jarvan IV, CFO): **0.557, 0.371** — alta
- Kino: no visible en 26
Cuadro secundario **t = 31.0 (HUD 07:47)**, misma toma (16.4 → 43.1), Kino llegando:
- POUT: **0.587, 0.510** — alta
- Kino (Alistar, CFO): **0.920, 0.430** — media (en el borde derecho)
- Shad0w (Jarvan IV, ROOTED, nivel 6): 0.404, 0.734 — duda (amontonado con Busio y efectos)
- Busio: placa en (0.398, 0.485), modelo no separable — duda
(a) Ruta POUT: [(26.0, 0.414, 0.320), (31.0, 0.587, 0.510)] — OJO: la cámara recorre ~610 px entre 26 y 31 (paneos rápidos 28.8-29.6): sin corte, pero compensar con cam.
(b) Flecha de intención Shad0w → Busio: de (0.557, 0.371) a (0.395, 0.569) (t 26).
(c) Busio está cerca de una planta/crustáceo del río (0.567, 0.62, no es campeón). Sin centinela visible cerca de Busio (coincide con «no hay un centinela»).

## 3 · g1_j3 · t = 25.0 (HUD 09:41) — Busio y Caliste encima de Kino (nivel 5)
Cuadro limpio. Kino ROOTED (raíz/ancla de Nautilus).
- Kino (Alistar, CFO): **0.468, 0.486** — alta
- Busio (Nautilus, KC): **0.416, 0.620** — alta
- Caliste (Tristana, KC): **0.433, 0.704** — alta
- Doggo (Kai'Sa, CFO): placa en (0.429, 0.237), modelo poco visible junto a la torre — duda
(a) Rutas (toma 12.6 → 45.2):
  - Kino: [(24.2, 0.458, 0.502), (25.0, 0.468, 0.486)]
  - Caliste: [(24.2, 0.415, 0.725), (25.0, 0.433, 0.704)]
  - Busio: [(23.2, 0.475, 0.431), (24.2, 0.408, 0.609), (25.0, 0.416, 0.620)] — en 23.2 Busio y Kino están juntos (AIRBORNE ambos); la cámara baja mucho entre 23.2 y 24.2 (paneo 22.7-23.9): casi todo el cambio es cámara.
  - Después: t 27.0 Busio (0.386, 0.542), Caliste (0.434, 0.734), Doggo (0.398, 0.398) — media.
(b) Flecha de intención Busio/Caliste → Kino: de (0.416, 0.620) a (0.468, 0.486). Torre de CFO (estandartes) arriba a la izquierda, ≈ (0.40, 0.17) — duda.
(c) Placas: Kino nivel 5, Busio 6, Caliste 7, Doggo 7 (confirma «Kino es nivel 5»).

## 4 · g1_j4 · t = 25.0 (HUD 11:21) — el foso del dragón Químico
Cuadro limpio; última imagen antes del corte de 26.1. El foso está arriba a la izquierda (barra del dragón «2717» sobre Yike).
- Yike (Wukong, KC, en el foso): **0.247, 0.313** — media
- Busio (Nautilus, KC): **0.273, 0.692** — alta
- Caliste (Tristana, KC): **0.423, 0.698** — alta
- Kino (Alistar, CFO, llegando): **0.747, 0.437** — alta
- Shad0w y Doggo (CFO): placas en (0.647, 0.696) y (0.717, 0.675) → pies bajo el HUD — sin anillo
- kyeahoo: posible figura en (0.43, 0.53) sin placa legible — duda; Canna no visible
(a) Rutas (toma 0 → 26.1):
  - Yike: [(23.0, 0.113, 0.194), (25.0, 0.247, 0.313)]
  - Kino: [(23.0, 0.667, 0.396), (25.0, 0.747, 0.437)]
  - Caliste: [(23.0, 0.373, 0.669), (25.0, 0.423, 0.698)]
  - Shad0w en 23.0 (aún sobre el HUD): (0.623, 0.621) — media
  - OJO: cámara de (-122, -34) a (-353, -96) entre 23 y 25 (paneo, sin corte).
(b) Zona FOSO (aprox.): centro ≈ (0.25, 0.24), radio ≈ 0.09 — duda (bordes del foso poco claros en este cuadro). Barra del dragón: (0.237, 0.141).
(c) Guardia de KC: barra azul corta en **(0.512, 0.153)** — media (encaja con «centinelas cubriendo el área»). Otra posible en (0.217, 0.168) — duda.

## 5 · g1_j4 · t = 30.0 (HUD 11:26) — Kino, Shad0w y Doggo entran; + t = 32.0 para Rest
Cuadro limpio; toma 27.3 → 53.4 (paneos 31.4-31.8 y 32.9-33).
- Kino (Alistar, CFO): **0.553, 0.218** — media
- Shad0w (Jarvan IV, CFO): **0.537, 0.372** — media
- Doggo (Kai'Sa, CFO): **0.600, 0.408** — media
- Dragón (barra «1664»): centro ≈ (0.433, 0.205); Yike: placa en el borde superior (0.363, 0.07) → sin anillo
- Busio: placa (0.433, 0.663) → pies ≈ (0.433, 0.775) bajo el HUD — sin anillo
Cuadro **t = 32.0 (HUD 11:28)** — Rest tras la Teleportación, ya enganchado (ROOTED, nivel 10) entre Busio y Caliste:
- Rest (Rumble, CFO): **0.453, 0.586** — alta
- Busio (Nautilus, KC): **0.397, 0.455** — media
- Caliste (Tristana, KC): **0.320, 0.408** — media
(a) Rutas:
  - Shad0w salta el risco: [(30.0, 0.537, 0.372), (31.0, 0.433, 0.182)] — sube 0,19 en 1 s con la cámara casi quieta (cam (-62,-176) → (-47,-173)): el salto es real
  - Doggo: [(30.0, 0.600, 0.408), (31.0, 0.510, 0.194)]
  - Rest: [(31.0, 0.503, 0.728) AIRBORNE, (32.0, 0.453, 0.586)] (paneo 31.4-31.8)
(b) Flecha de intención CFO → dragón: de (0.537, 0.372) a (0.433, 0.205). «Posición comprometida» de Rest: anillo rojo en (0.453, 0.586) con Busio/Caliste al lado.
(c) Definitiva de Kino: no se distingue en el cuadro (usar la voz). En 34.0 sale «Blue team has slain the Chemtech Drake!» (dragón para KC ≈ t 34, HUD 11:30). Rest de t 34 a t 38 tiene los pies bajo el HUD; vuelve a verse en **t 39: (0.57, 0.61)** — media.

## 6 · g1_j4 · t = 36.5 (HUD 11:32) — Canna (Galio) cae sobre CFO
Cuadro limpio (rótulo «CHEMTECH DRAKE» arriba). Galio aterriza con la definitiva: círculo morado alrededor.
- Canna (Galio, KC): **0.406, 0.258** — media (centro del aterrizaje ≈ (0.406, 0.229))
- Shad0w (Jarvan IV, CFO, AIRBORNE nivel 8): **0.370, 0.355** — media (está en el aire: anillo en su sombra)
- Kino (Alistar, CFO): **0.485, 0.320** — media
- Doggo (Kai'Sa, CFO): placa (0.482, 0.211), modelo detrás de Kino — duda
- Yike (barra azul nivel 8 bajo la de Shad0w): en el mismo círculo que Shad0w — duda
(a) Rutas: Shad0w [(31.0, 0.433, 0.182), (36.5, 0.370, 0.355)] (misma toma 27.3 → 53.4; la cámara baja ~35 px). Canna no tiene ruta medible (llega volando con la definitiva).
(b) Zona FOSO en este cuadro: centro ≈ (0.365, 0.25), semiejes ≈ (0.09, 0.13) — media. Flecha de intención de Canna: desde arriba (fuera del cuadro) a (0.406, 0.229) — no medida, solo dirección.
(c) t 37.5: Shad0w AIRBORNE otra vez y «CLONE» de Wukong en (0.396, 0.205); t 39: «The Inferno blazes!», Shad0w TAUNTED y otro CFO AIRBORNE (provocación de Galio), Yike (0.29, 0.50 aprox., duda). Kill de Canna a Shad0w t ≈ 45.

## 7 · g1_j5 · t = 28.3 (HUD 14:44) — Kino bajo la torre de kyeahoo
Toma corta 28.0 → 30.8 (el observador corta a menudo en esta fuente). Cuadro limpio.
- kyeahoo (Cassiopeia, KC, AIRBORNE): **0.450, 0.534** — media
- Kino (Alistar, CFO): **0.522, 0.648** — media
- Shad0w (Jarvan IV, CFO): **0.373, 0.610** — media
- POUT (Syndra, CFO): **0.549, 0.325** — media
(a) Rutas (28.0 → 30.8):
  - POUT: [(28.3, 0.549, 0.325), (29.5, 0.456, 0.392)]
  - Kino: [(28.3, 0.522, 0.648), (29.5, 0.522, 0.629)]
  - kyeahoo: [(28.3, 0.450, 0.534), (29.5, 0.405, 0.648) STUNNED]
(b) Zona TORRE de KC (cristales azules, en parte fuera del cuadro por la izquierda): centro ≈ (0.07, 0.62), radio ≈ 0.07 — duda. Flecha de intención POUT → kyeahoo: de (0.549, 0.325) a (0.450, 0.534).
(c) kyeahoo AIRBORNE (cabezazo/pulverizar de Alistar); orbes de Syndra en el suelo. El kill de POUT a kyeahoo sale hacia t 32-33 (otra toma: cortes 30.8-31.0).

## 8 · g1_j6 · t = 47.5 (HUD 17:13) — Rest entra con TP y definitiva; Canna canaliza la provocación
Toma 41.9 → 71.8. Cuadro limpio. Escena muy amontonada: los de CFO están dentro del escudo de Galio.
- Rest (Rumble, CFO, ROOTED, nivel 13): **0.398, 0.472** — media
- Canna (Galio, KC, «CHANNELING»): centro del escudo **0.574, 0.443**, pies ≈ **0.575, 0.47** — media
- kyeahoo (Cassiopeia, KC): **0.268, 0.369** — media
- Caliste (Tristana, KC): **0.216, 0.551** — media
- Yike (Wukong, KC): **0.345, 0.718** — media
- Busio: placa (0.326, 0.349), modelo no separable — duda
- POUT (Syndra): ≈ (0.572, 0.271) — duda · Shad0w, Kino, Doggo: dentro/junto al escudo de Galio (placas en (0.55, 0.38), (0.55, 0.28), (0.61, 0.18)) — duda
(a) Rutas:
  - Rest (entra tras la TP): [(45.0, 0.519, 0.325), (46.5, 0.447, 0.452), (47.5, 0.398, 0.472)] — media (cámara (56,-112) → (290,-142))
  - Caliste: [(45.0, 0.263, 0.487), (46.5, 0.218, 0.570), (47.5, 0.216, 0.551)]
  - Yike: [(45.0, 0.334, 0.678), (46.5, 0.326, 0.698), (47.5, 0.345, 0.718)]
(b) Zona del escudo/provocación de Galio: centro (0.574, 0.443), radio ≈ 0.07 en x. Flecha de intención de Rest: de (0.519, 0.325) a (0.398, 0.472).
(c) En t 48 (HUD 17:14) ya salen tres «TAUNTED» en CFO (niveles 12, 7 y 11) y Rest AIRBORNE: la provocación entra. En t 45 Rest aparece al lado de Kino (TP recién usada).

## 9 · g1_j6 · t = 124.0 (HUD 18:30) — justo antes de la 2.ª pelea 3 por 0
Toma 111.4 → 149.7. Cuadro limpio (rótulo «Objective Bounties are available soon»).
- Rest (Rumble, CFO): **0.542, 0.606** — alta
- Canna (Galio, KC): **0.251, 0.446** — media
- Caliste (Tristana, KC): **0.332, 0.622** — media
- kyeahoo (Cassiopeia, KC): **0.596, 0.724** — media (cerca del borde del HUD)
- POUT (Syndra, CFO): **0.299, 0.222** — media
- Yike (Wukong, KC): ≈ (0.41, 0.665) — duda (hay un «CLONE» de Wukong al lado)
- Shad0w, Doggo, Kino, Busio: un solo montón en (0.39-0.48, 0.33-0.53) (placas: Shad0w (0.474, 0.33), Doggo (0.469, 0.398), Kino (0.389, 0.449), Busio (0.452, 0.366)) — duda, sin anillos
(a) Rutas:
  - Canna: [(119.0, 0.260, 0.398), (122.5, 0.269, 0.398), (124.0, 0.251, 0.446)]
  - Caliste: [(119.0, 0.230, 0.745), (122.5, 0.326, 0.665), (124.0, 0.332, 0.622)]
(b) Barra «3721» en (0.25, 0.25) = estructura de CFO (en t 119 «Red turret destroyed!»): zona de torre ≈ (0.25, 0.30) — duda.
(c) En t 119 Canna canaliza (nivel 13) y cae la torre roja; las muertes vienen en t 125-130 (Doggo, Kino, Shad0w).

## 10 · g1_j7 · t = 33.6 (HUD 24:29) — la provocación de Canna sobre Shad0w
Toma 30.6 → 40.0. Cuadro limpio. Foso del Barón a la izquierda (barra «10813»).
**OJO: el anuncio «KC Yike is on a killing spree!» sale en t 34.3 (HUD 24:30): la muerte de Shad0w es en t ≈ 34, no en t 36 (el feed va ±2 s).**
- Shad0w (Jarvan IV, CFO, ROOTED, nivel 12): **0.443, 0.707** — media
- Canna (Galio, KC): **0.308, 0.675** — media
- Kino (Alistar, CFO): **0.458, 0.387** — media
- Rest (Rumble, CFO): ≈ (0.491, 0.525) — duda · POUT (Syndra): ≈ (0.512, 0.456) — duda (los dos juntos en el fuego de Rumble)
- Doggo (Kai'Sa, CFO): ≈ (0.578, 0.323) — duda · kyeahoo (KC): placa (0.242, 0.181), pies ≈ (0.254, 0.285) — duda
- Yike (placa (0.413, 0.72)), Busio y Caliste (AIRBORNE, niveles 9 y 14): pies bajo el HUD — sin anillo
(a) Rutas:
  - Canna: [(32.8, 0.350, 0.744), (33.6, 0.308, 0.675)]
  - Kino: [(32.8, 0.437, 0.510), (33.6, 0.458, 0.387)] (la cámara sube ~110 px entre 32.5 y 33.5: casi todo es cámara)
  - Shad0w en 32.8: placa en y 0.76 → pies bajo el HUD, sin punto de ruta.
(b) Zona Barón: centro ≈ (0.31, 0.62) — media. Flecha de intención Canna → Shad0w: de (0.308, 0.675) a (0.443, 0.707).
(c) Rest (0.515, 0.616) y POUT (0.509, 0.494) en t 32.8 — media.

---
## Resumen de calidad
- Bien medidas (anillos de alta/media para los protagonistas): 1, 2, 3, 4, 5 (+ t 32 para Rest), 7.
- Parciales: 6 (Canna, Shad0w, Kino ok; Doggo/Yike duda), 8 (Rest, Canna, KC ok; CFO dentro del escudo = duda),
  9 (Rest, Canna, Caliste, kyeahoo, POUT ok; el montón central = duda), 10 (Shad0w, Canna, Kino ok; Yike bajo el HUD; muerte en t ≈ 34).
