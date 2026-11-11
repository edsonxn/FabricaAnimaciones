# Propuesta de imágenes — grupo D (s05 Kyle/Ezra · s04 ¡CLOC! · s03 anillo · s02 antorcha · s01 Eluvi'ana)

Revisé los 45 beats (scene-149 a scene-193) con hojas de 3 cuadros (`_dl/img_D/hojas/`) y lo que ya pone `efectos.py`.
Las imágenes nuevas están en `pegatinas/` y `pantallas/`, revisadas a 640 px y apuntadas en `pegatinas/_fuentes.txt`.

## ERRORES QUE BLOQUEAN (identidad y rótulos de otros youtubers)
- **`pegatinas/kyle.png` es un NIÑO HUMANO llamado Kyle (homónimo), no el perro.** Se usa en `pv("Número cinco. Kyle ha desaparecido"…)` y en `pv("Le das la carne, Kyle se calma"…)`. Hay que cambiarlo en los dos por **`s05_kyle_perro`** (Kyle the Frenzied, el perro de Ahab, wowpedia).
- **`o_hoja.png` y `o_eluviana.png` son la MISMA imagen** (el mismo icono de cimitarra). Salen las dos en `pv("te pide encontrar la hoja")`, en la `M.cadena` y en el `rel` del n.º 1. No pude comprobar en Wowhead cuál es la buena porque bloquea las descargas (403). Hay que revisarlo, o usar la hoja solo en el mapa.
- **Clips de OTROS secretos con rótulos del youtuber** (5sBZlwAjAI8, con su logo de taza y sus cartelas):
  - scene-167: «ALCHEMY HERB / Grave Moss» y «Rockslicer».
  - scene-184: «THE CHAIN», que es la cadena de Delgren y Mannoroth, otro secreto.
  - scene-187: «KHARA DEEPWATER», que es la caja de pesca.
  - scene-193: «Thoradin's Wall» y «Spawn of Grubthor».
  - Los cuatro se cambian (filas abajo).
- **Más rótulos o marcas de agua de youtubers:**
  - scene-149: cartela «Kyle's Gone Missing! Solo - Mulgore» al empezar.
  - scene-150: «Farm 1 Tender Strider Meat».
  - scene-153: subtítulo «When you see the dog, click on the Strider Meat».
  - scene-160 y scene-163: cartela «Prairie Chicken / Westfall».
  - scene-161: logo «M» del canal.
  - scene-176: logo de YouTube y «xScarlife Gaming».
  - scene-180: retrato de la marca de la guía abajo a la izquierda desde el segundo ~3.
- scene-179 (Colina del Cuervo) enseña la cubierta de un barco y scene-175 un Skeletal Mage: ninguno de los dos es lo que dice la voz. El mapa con `colina_cuervo` lo tapa en parte, pero el clip sigue sin venir al caso.

## Cambios
| frase | empieza en | hasta | tipo | slug / url + desde | qué se ve |
|---|---|---|---|---|---|
| s05_0 | Número cinco. Kyle ha desaparecido | (pv actual) | pegatina grande | `s05_kyle_perro` (en lugar de `kyle`) | Kyle, el perro (lobo rubio) de Mulgore |
| s05_0-1 | Número cinco. Kyle ha desaparecido | perdió a su perro, Kyle | clip nuevo scene-149 | https://www.youtube.com/watch?v=k19lB_y8b8s desde 14 | 4K: Poblado Pezuña de Sangre con tiendas; el tauren con el perro al lado; sin cartela |
| s05_2 | La misión te pide carne tierna | corriendo por las praderas | clip nuevo scene-150 | https://www.youtube.com/watch?v=I5nXvze90AI desde 17 | el mismo clip de ahora pero 2 s más tarde, ya sin «Farm 1 Tender Strider Meat»: caza de zancudos |
| s05_3 | Le das la carne, Kyle se calma | (pv actual) | pegatina | `s05_kyle_perro` (en lugar de `kyle`) | el perro |
| s05_5 | Ezra tenía cáncer cerebral | le puso su propia voz a Ahab | clip nuevo scene-153 | https://www.youtube.com/watch?v=k19lB_y8b8s desde 84 | 4K de día: Kyle siguiendo al tauren por las praderas; sin subtítulos del youtuber |
| s05_6 | Ezra murió poco después de su | también en Forever | pegatina grande (legajo/banda) | `s05_ezra_memorial` | el post OFICIAL de Blizzard «In Memory of Ezra Chatterton (1996-2008)», 28-10-08, «Strength and honor, Ezra.» |
| s04_0 (cola de scene-157) | Número cuatro. El huevo de gallina | Este es el secreto con el que | clip nuevo scene-157 | https://www.youtube.com/watch?v=ptBP1AAkmlE desde 84 | pollos en el campo de los Páramos (ahora se ve el vendedor Saldean antes de que la voz lo nombre) |
| s04_3 | Una vez, y otra, y otra | te ofrece una misión: ¡Cloc! | clip nuevo scene-160 | https://www.youtube.com/watch?v=ptBP1AAkmlE desde 109 | el pollo junto al jugador y, en el segundo ~6, la ventana «CLUCK! Cluck... BACAW!»; sin cartela |
| s04_3 (respaldo) | te ofrece una misión: ¡Cloc! | 2,5 s | pant | `s04_cloc_mision` | la ventana real de la misión CLUCK! que ofrece el pollo |
| s04_4 | Para cumplirla necesitas pienso especial | ahí mismo, en su granja | clip nuevo scene-161 | https://www.youtube.com/watch?v=ptBP1AAkmlE desde 20 | el granjero Saldean con su ventana de venta y el tooltip «Special Chicken Feed»; sin el logo «M» |
| s04_6 | Le das el pienso al pollo | Y del huevo sale tu mascota | pant | `s04_huevo_gigante` | el Chicken Egg gigante que deja el pollo en el campo |
| s04_6-7 | un pollo de los Páramos | antes que su primera espada decente | clip nuevo scene-163 | https://www.youtube.com/watch?v=qkI4VvJ5vxo desde 87 | ficha de la mascota «Westfall Chicken» y, después, la mascota «Westfall Chicken <…'s Companion>»; sin cartela |
| s03_1-2 (cola de scene-167) | el Dawn Waker. Lo encontró | Wowhead lo publicó esta semana | clip nuevo scene-167 | https://www.youtube.com/watch?v=KeU2GDOhOmM desde 300 | 4K de Zephras (estatua y explanada) en vez del clip de hierbas y del hacha Rockslicer |
| s03_6 | y te da un anillo | una reliquia de familia | clip nuevo scene-171 | https://www.youtube.com/watch?v=_oYca7_FdYw desde 24 | entrega a Rorian the Dayseeker → panel de personaje con el tooltip del Ancient Heirloom (desde el segundo ~3) |
| s03_6 (+ o en lugar del clip) | el Ancient Heirloom, una reliquia | una reliquia de familia | pegatina grande o pant | `s03_anillo_tooltip` (png, tooltip ×3) / `pantallas/s03_anillo_tooltip.jpg` | tooltip real: «Ancient Heirloom · Soulbound · Finger · …'With love always, KG'» |
| s02_3 | Le quitas de la mano una antorcha | lo que esconde la oscuridad | pant | `s02_antorcha_mision` | ventana «An Unfortunate End» (el texto de «pry it from his stiff fingers… reveal things hidden by darkness»), el guardia muerto «Night Watch Guard» y el tooltip de la antorcha |
| s02_2-3 | Requiere nivel uno, es para | El texto dice que te | clip nuevo scene-176 | https://www.youtube.com/watch?v=eyfyyP6hGkM desde 18 | camino del Bosque del Ocaso hasta el guardia con «?» y su ventana (s. 26); sin la marca «xScarlife Gaming» |
| s02_4 | Es un objeto de nivel uno | ocupa un hueco en la bolsa | pegatina grande (cambia o acompaña la tarjeta de APOYOS) | `s02_antorcha_tooltip` | tooltip real: «Item Level 1 · Unique · Use: Light the Night Watchman's Torch (30 Sec Cooldown)» |
| s02_7 | Alrededor hay necrófagos de nivel veinticinco | entra con cuidado | pegatina | `s02_necrofago` | Flesh Eater, el necrófago de la Colina del Cuervo (wowpedia) |
| s02_7 | Alrededor hay necrófagos | muy cerca | clip nuevo scene-180 | https://www.youtube.com/watch?v=LW1veoIJasc desde 2590 | Bosque del Ocaso de noche en 4K, cementerio con lápidas, sin marca de la guía (el nombre del enemigo no se distingue en mi muestra: mirarlo al bajarlo) |
| s01_3 | Se la llevas a Ealaane | No tiene un lugar fijo | clip nuevo scene-184 | https://www.youtube.com/watch?v=On6ShRFYsco desde 12 | Ealaane Nimbuswalker <Ban'aethal Refugee> junto a la hoguera del campamento (coordenadas 65.9, 74.5 = las del guion), con su nombre en grande |
| s01_5 | te dan Eluvi'ana, una espada | de calidad poco común | pegatina grande | `o_eluviana` (una vez aclarado que no es la hoja) | el icono de la espada en el momento de la recompensa |
| s01_6-7 (cola de scene-187) | La cadena sigue por Costa Oscura | La segunda parte llega | clip nuevo scene-187 | https://www.youtube.com/watch?v=JoNXFpRjmJg desde 1200 | Costa Oscura Classic en 4K: ruinas élficas, sin la cartela de Khara Deepwater |
| s01_12 | Nadie ha terminado el Dawn Waker | algo enorme | clip nuevo scene-193 | https://www.youtube.com/watch?v=JekLW8trrMc desde 18 | las Ruinas de Ban'aethal con su estatua (comprobado en la guía, 18-27 s); fuera Thoradin y Grubthor |

## Falta (no hay material real)
- **s01_2 «Usas la antorcha, y aparece una empuñadura antigua»**: ningún video enseña la empuñadura apareciendo (busqué Dawn Waker, Ancient Hilt, Eluvi'ana, Ban'aethal torch). Hay que hacerla en **Flow** como captura del juego. Ingredientes:
  - `_dl/img_D/flow_banaethal_ing.jpg`: Ruinas de Ban'aethal a 2560x1440, JekLW8trrMc s. 26.
  - `pantallas/s02_antorcha_mision.jpg`: la antorcha encendida.
  - `o_empunadura`: el icono.
  - Prompt: personaje con la antorcha encendida en las ruinas y una empuñadura antigua que brilla en el suelo. Va con rótulo pequeño «RECREACIÓN».
- **s01_7 globo de agua corrupto, nagas de Costa Oscura y Barón Aquanis**: no encontré cuadros comprobados. La imagen del Barón Aquanis de wowpedia es un render moderno, así que la descarté. Falta Flow, o una captura de Brazanegra (Cavernas de Brazanegra / Blackfathom Deeps) Classic.
- **s01_8 espíritu altonato en la Playa de Zoram y bóveda de Feralas que solo se ve con el anillo**: no hay material. Falta Flow con ingredientes de Costa Oscura y Feralas Classic, marcado como recreación.
- **s05_7-8 respuesta de Kaivax en el foro**: no la capturé; haría falta el navegador. La tarjeta «Kyle vuelve» de APOYOS ya lo cubre.
- **s01_10 Tortheldrin**: en mi muestra de NWbh6dNV6Vg (La Masacre Oeste) no apareció; se queda la pegatina `tortheldrin`, que es correcta. scene-191 (ruinas como bajo el agua de TzJ2JRfdXyw) no es La Masacre: si se encuentra a Tortheldrin en NWbh6dNV6Vg (es el último jefe, hacia el s. 5900-6060), se pone ese tramo.

## Ya bien (no tocar)
- **s05:** scene-151, 152, 155 y 156 (Kyle y el tauren en Mulgore, la entrega). El mapa de Mulgore con Ahab, `o_carne` y `ahab`. Lo de Ezra (`sil` con `ezra`) se queda, pero la foto es de 135 px: ponerla pequeña o en camafeo, no a media pantalla.
- **s04:**
  - scene-158: el pollo con «Chicken», que sirve para el /chicken.
  - scene-159: la granja de los Saldean.
  - scene-162: la ventana de William Saldean en la parte de la Horda.
  - scene-164 y scene-165: el pollo con «!» y el registro de misiones CLUCK!.
  - Lo de efectos.py: chat /chicken, mapa de los Páramos y `filav` del pienso, el huevo y el pollo.
- **s03:**
  - scene-166: Zephras.
  - scene-168, 169 y 170: Ailee Farheart con su misión y la entrada.
  - scene-172: Rorian the Dayseeker.
  - scene-173: rampa al piso de arriba.
  - La cadena del Dawn Waker y el mapa de Thendal.
- **s02:**
  - scene-174 y scene-181: personaje con la antorcha encendida.
  - scene-177: el guardia con «?».
  - scene-178: Bosque del Ocaso.
  - El mapa de 6 sitios, el `rel` y el `pv` de la antorcha.
- **s01:**
  - scene-182: «Ruins of Ban'aethal» y el mapa de Zephras.
  - scene-183 y scene-186: ruinas y paisaje.
  - scene-189: Feralas (ogros Gordunni).
  - scene-190: mazmorra con nivel 40+.
  - El mapa con los 4 sitios de la hoja y la `M.cadena`.
  - scene-185 (combate oscuro) y scene-188 (Costa Oscura) valen como relleno, pero es mejor tapar 188 con lo de Flow cuando esté.
