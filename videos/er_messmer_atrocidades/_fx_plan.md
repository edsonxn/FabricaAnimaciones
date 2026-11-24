# Plan de efectos — er_messmer_atrocidades (24-nov-2026)

Regla de oro (docs/estilo_secuencia_yt.md): las capas SUMAN; ningún tramo > ~4 s sin pegatina/MG/ficha/pantalla salvo que
suene un sonido nombrado (PISTA) o el clip enseñe justo lo que se dice; meta ≥ 4 MG y ≥ 4 pegatinas/min, fichas ≥ 1,3/min,
mapas ≥ mitad de los puestos. Cada objeto/personaje/lugar NOMBRADO se ve en ese momento. Anclas ÚNICAS (mira `_anclas.py`).
Fichas `descripcion` = SOLO citas en español verificadas (dossier § 3, tal cual el guion las lee). Lo parafraseado (Anciana,
Cornamentado, Leda, Queelign, almas, Bendición de Márika) = rótulo `puesto` arriba (y=.10) o MG, nunca ficha entre comillas.

## PISTAS voz=True (sonidos nombrados; tramo = el `post` de la escena, voz callada; rótulo con lo que se oye)
- intro → sfx/s_despojados.mp3 (11,44 s) · rótulo «Messmer: Those stripped of the Grace of Gold shall all meet death…»
- p2b → sfx/s_cornamentado.mp3 (7,84 s) · rótulo «El Cornamentado: Messmer, foe of my beloved people…»
- p1b → sfx/s_madre_sanciona.mp3 (8,54 s) · rótulo «Messmer: Mother, wouldst thou truly Lordship sanction…»
- cierre → sfx/s_maldicion.mp3 (7,73 s) · rótulo «Messmer: Mother… Marika… A curse upon thee»
(Molde de cómo se declaran: PISTAS en videos/er_rykard_atrocidades/efectos.py.) Durante cada tramo: clip/pantalla de Messmer
(o del Cornamentado) hablando, nada que tape su cara.

## MG NUEVOS de este guion (nucleo/mg_er.py; prueba en previews/mg_prueba_hoja.jpg)
- `E.medalla(_G("insignia"), …)` 5 marcas: p1 (nombre «Insignia de cruzada» → efecto «Aumenta la potencia…» → bajas al
  decir «empalar y quemar» → cita al decir «estimulados por los gritos» → sello «Tú la llevabas puesta» en p1b «Léelo otra vez»).
  Puede repetirse corto en introb («una medalla… Sale en el número uno», sin sello: remate=None y 4 marcas tempranas).
- `E.empalados()` 6 marcas: p3 «destripadas y colgadas en las lanzas de Messmer» (5 lanzas una por palabra clave) + fuego
  en «calcinadas en sus llamas»; remate «Una pira funeraria para la propia torre».
- `E.tumba()` 5 marcas: p5b Andreas (marca 0 en «Andreas»), Huw (1 en «Su hijo Huw»), motivo (2 en «naturaleza reptiliana»
  de la 1.ª aparición… ojo ancla única), lágrima (3 en «Messmer lloró»), remate (4 en «Pero no lo sacó»). Si «naturaleza
  reptiliana» va antes de Huw en la voz, reordena marcas a mano para que cada una caiga en su palabra.
- `E.sopa(icono=_G("potaje"))` 3 marcas: p2 «Potaje de escorpión» → «Al haberse enfriado» → «No le hace falta» (remate
  «Nadie llegó a comérsela»); vuelve corto en p2c «Aun así, la sopa se enfrió» y en el cierre «Una sopa que se enfrió».
- `E.despojados(remate="Una cruzada que existía para matarte")` n+2 marcas: p1c (cita en «quienes se ven despojados» de
  p1c_0 → cornamentados, bestias divinas, Caballeros Negros → «Tú, Sinluz» en «la definición exacta» → remate en «para matarte»).
  Versión corta sin tachar en introb al decir «En español: quienes se ven despojados…».
## MG reusados (mg_er): `puesto` en cada «Número N» (títulos ≤ 22 letras: «Su gente, a la tumba», «El sabio incendiario»,
«Dioses en sus lanzas», «La sopa fría», «La medalla colgada»); `descripcion` (fichas); `cien` en subs (9 encendidos de 100:
«de cada cien vistas, menos de nueve»; remate «Meta: 2 000»); `linaje` o `hilos` en p5 («Márika → Messmer»: madre que le
arranca el ojo); `expediente` como hilo del video (acusado «Messmer el Empalador», un cargo por puesto: «Encerró a los suyos
en una tumba», «Su sabio quemó más que nadie», «Colgó a sus dioses», «Enfrió la sopa de una familia», «Te puso la medalla»
con sello CULPABLE en el cierre); `balanza` en p2c (Leda: «nunca fueron santos» vs «quemados en paz»; remate «Aun así, la
sopa se enfrió»); `cadena` o `estandarte_caido` en p5 (Caballeros de Fuego expulsados de sus casas); `muerte_suelta` NO.
Más: `ecos` en cierre (las líneas de Messmer en ES verificadas: «Madre... Márika... Una maldición caerá sobre ti»).

## MAPAS (mapas/sombras.jpg; coordenadas MEDIDAS del dossier § 4; helper `mapa()` del molde, TEMA_MAPA "er")
- introb: Reino de las Sombras entero → Fortaleza sombría (0,49 0,43) con foto pantallas/fortaleza_sombria_exterior.
- p4: Fortaleza sombría (0,49 0,43) → Antiguas ruinas de Rauh (0,283 0,490) con foto rauh_wiki (ruta: «la llama llegó»).
- p3: Belurat (0,245 0,60) y la torre / Enir-Ilim (0,225 0,555) con foto belurat_plaza_fuente.
- p2: Llanura de las Tumbas (0,40 0,68) → Ruinas calcinadas (0,390 0,693) con foto ruinas_calcinadas, y Belurat.
- p1: Belurat (Queelign invade) → Fortaleza sombría (sala de Messmer): ruta «la medalla viene de aquí».
NO usar lugares NO MEDIDOS (Aldea ósea, Fuerte de la reprimenda, Grieta Neblinosa, Iglesia de la Cruzada, gracia de entrada).

## COMENTARIOS (com(en, id) — tarjetas en pegatinas/; ≤ 2 a la vez, separadas en x/y)
- introb: Stormy UgxHbdhbvsllIKdpd-Z4AaABAg · Sergio UgyS_O2n-x-GKqkxjtl4AaABAg · Luis UgzTki3VLPQeOEt1BKF4AaABAg ·
  Rick UgxRBIoWmEnn48Wv8DB4AaABAg · Rico (crítica) UgzQ8NGWpzIzJX7yDax4AaABAg
- p4b: David UgxdHxlNVRMXvaRRqad4AaABAg · Quixilero UgzbX3DCRGfAJ_JaDGJ4AaABAg
- p3: Quaerens UgzgImyRyHKjdjBkCQx4AaABAg · p3c: Pascual (crítica) Ugxz7Dc9NCilg0P8Lmt4AaABAg
- subs: Shiro UgzTQ0w2ZJwz6Nh3Pgh4AaABAg · Ulises UgwOrheEVgtPhGGmRbN4AaABAg · Daniel UgzyUmjrE2l-sir6F9d4AaABAg
- p1c: Retos (crítica) UgyPJ2Ulc5FuS9MJVAx4AaABAg · cierreb: Santiago Ugz7NLq2H8saxbXlFO14AaABAg
- NO usar com_UgwJSlXBno3eEYwuI_x4AaABAg (reserva descartada).

## PEGATINAS por momento (pegatinas/*.png; hoja previews/pegatinas_hoja.jpg; `cornamentado_2` NO, es la misma)
intro: messmer (silueta o banda de su cara), lanza_empalador, yesca · introb: reino_sombras (pant), cornamentado, leon,
potaje (avance), insignia (avance) · p5: caballero_fuego, casco_fuego, armadura_fuego, recuerdo_empalador, casco_messmer,
escudo_serpiente, marika · p5b: caballero_negro, cenizas_andreas, cenizas_huw, cenizas_soldado, armadura_soldado, casco_negro ·
p4: capucha_salza, lluvia_fuego, chispa_aromatica, grasa_messmer, botella_perfume, rauh_wiki (pant), yesca · p4b: hilde,
almacen_wiki / almacen_especimenes_interior (pant), romina, hoja_brote, recuerdo_brote, iglesia_brote (pant) · p3: leon,
tornado_bestia, trailer_criatura_atravesada_lanzas (pant, rótulo «Tráiler oficial»), belurat_wiki · p3b: recuerdo_leon,
anciana, cabeza_bestia, marika · p2: anciana (silueta/legajo), potaje, belurat_plaza_fuente · p2b/p2c: cornamentado,
miquella (camafeo: «el grupo de Miquella»), leda, mayal, tunica_cordon, ruinas_calcinadas (pant) · p1: queelign,
espadon_queelign, iris_gracia, insignia · p1b/p1c: messmer_jefe/messmer_serpiente, runa_marika, armadura_messmer ·
cierre: bendicion_marika, recuerdo_empalador, marika · cierreb: messmer_serpiente; abanico de próximos (bayle, rennala,
maliketh, parches, zampaheces, gideon); abanico de la colección (marika, radagon, miquella, malenia, ranni, melina, radahn,
morgott, mohg, godrick, godfrey, rykard).
Pantallas del tráiler (trailer_*) llevan franjas negras: zoom ≥ 1.35 para taparlas o banda.
«Bendición de Márika»: rótulo «En inglés y en japonés: hizo varias… y nunca más», no ficha.
