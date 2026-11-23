# -*- coding: utf-8 -*-
"""GUION — «Los 15 enemigos ocultos de Fallout» (Radio Yermo, 3.er video del canal, 23-nov-2026).
Motor SECUENCIA YT (docs/estilo_secuencia_yt.md § REGLA DE ORO y § Radio Yermo); receta y voz de `videos/fo_nunca_f4/guion.py`.
Datos: Fallout Wiki EN/ES leída por la API → `_investigacion_A.md` (FO3+FNV) y `_investigacion_B.md` (FO4), con URL;
comprobados a mano el 23-nov: Gabe se vuelve atómico al morir, sanguinario mítico suelta un cigarrillo, Hundebarcos 4 000 de
resistencia física. La voz NO cita fuentes. Referencia: Wastelander «Hidden Fallout NV/3/4 Enemies» ×7,3/×6,5/×3,4 (lista propia).
Reparto: FO3 = 15, 12, 9, 5 · FNV = 14, 11, 8, 6, 3, 1 · FO4 = 13, 10, 7, 4, 2. Clips SOLO del juego de cada puesto (regla 3).
Nombres en la voz: los de la versión en español (sanguinario, tochomosca, mutascorpio, hombre pinza, necrófago, Megatón,
Viejo Longfellow); lo que no tiene nombre oficial en español se dice en inglés (Red Death, Wild Wasteland, Big MT).
Sin sonidos nombrados (23-nov: el silbido del OVNI se quitó: ningún clip trae el choque con su audio; se ve con e7_cayendo).
Canal sin comentarios (0 en 21 d): sin agradecimientos ni críticas; suscripción sin cifra.
"""

TITULO = "15 ENEMIGOS ocultos de Fallout que casi nadie vio"
ARCHIVO = "fo_enemigos_ocultos"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 96
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
# ElevenLabs dice el inglés nativo: aquí solo lo que se oiga mal (oírlo antes de añadir)
FONETICA = {}
CER_MAX_POR_FRASE = {'p15_1': 0.067, 'p12_0': 0.14, 'p12_1': 0.024, 'p12_2': 0.027, 'p12_3': 0.018, 'p11_1': 0.017, 'p10_2': 0.028, 'p9_0': 0.075, 'p8_1': 0.089, 'p6_1': 0.024, 'p2_0': 0.034, 'p3_0': 0.038, 'p3_4': 0.031, 'subs_0': 0.033, 'p4_5': 0.015}   # 23-nov: solo nombres (Whisper: Rusca/Yaowai/Hicks/Greenwich/BDMT/Borus/Kuri/RAR/Dleason/Deadwind/Repcon/Nucacona)
TAIL_MAX_POR_FRASE = {'p1_4': 1.15, 'p2_3': 1.15, 'p13_3': 1.15}   # ElevenLabs: cola 1,03-1,10, toma completa

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="Fallout", min_s=40, max_min=240, alto=1080,
            evitar_canales=["AdayCanarioWTF", "chrom3rat", "Lone Wolfhound"]),   # webcam fija · Tale of Two Wastelands · mods
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = None   # canal de videojuego: OST oficial del juego de cada puesto (armar_musica_ost.py)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[deadpan] Buenos días, Yermo. Aquí Radio Yermo, transmitiendo desde una cueva que no sale en el mapa.",
        "Hoy, los quince enemigos ocultos de Fallout tres, New Vegas y Fallout cuatro. Los que casi nadie llegó a ver.",
        "Una osa de circo que sigue jugando con su pelota roja. Un perro gigante que al morir se vuelve atómico.",
        "Un monstruo marino legendario que resulta medir menos que una mosca. Y un alienígena herido, escondido en una cueva.",
        "[deadpan] Todo comprobado en el juego. Y el número uno es el enemigo más fuerte de todo New Vegas, y resulta que es una mosca.",
    ]},
    {"id": "p15", "frases": [
        "Número quince. El Quinteto de la Reina, en Fallout tres.",
        "Bajo la estación de metro Marigold, junto a Grayditch, un científico, el doctor Lesko, le inyectó un mutágeno a una reina de hormigas para que sus crías fueran más pequeñas.",
        "Le salió al revés. Las hormigas nacieron más grandes y escupiendo fuego, y la reina quedó custodiada por cinco guardianes únicos.",
        "Solo existen esos cinco en todo el juego. Cada uno con doscientos veinticinco puntos de vida y un ochenta y cinco por ciento de resistencia al fuego.",
        "Detrás está la reina de Marigold, con mil puntos de vida. Ella no escupe fuego: el experimento solo afectó a sus huevos.",
        "[sarcastic] Quería hormigas más pequeñas. Consiguió lanzallamas con patas. Ciencia de antes de la guerra.",
    ]},
    {"id": "p14", "frases": [
        "Número catorce. El cazador legendario, en New Vegas.",
        "En la mina de Silver Peak, al oeste de la carretera ciento cincuenta y siete, en el camino a Jacobstown, hay una mina llena de cazadores. Ya eso es mala idea.",
        "Pero al fondo, desde un túnel del segundo piso, sale el único cazador legendario del juego.",
        "Nivel veinticinco, cuatrocientos puntos de vida, el doble que un cazador adulto, y un veneno que te quita ocho puntos por segundo durante treinta segundos.",
        "En esa mina murió un soldado del Enclave que había huido de Navarro. Escapó de la RNC entera, y fue a esconderse justo aquí.",
        "[deadpan] En el Mojave hay dos formas de morir. Por un cazador, o por el cazador.",
    ]},
    {"id": "p13", "frases": [
        "Número trece. El Red Death, en Far Harbor.",
        "Los pescadores de Far Harbor llevan años hablando de un monstruo marino que hunde barcos en la costa. Lo llaman Red Death, la muerte roja.",
        "Solo lo ves si haces la gran cacería con una vieja capitana del puerto, que quiere matarlo como última aventura antes de morir.",
        "Llegas a una isla sin marcador, al suroeste de la Isla, rodeada de barcos hundidos. Y ahí está: un hombre pinza diminuto, más pequeño que una tochomosca, con los ojos rojos brillantes. Ni siquiera es hostil.",
        "Sus ojos brillan a través de la Niebla. Los capitanes se acercaban a mirar, y encallaban en las rocas.",
        "[sarcastic] Años de leyenda, y el monstruo cabe en una cubeta. Igual tienes que matarlo para terminar la misión.",
    ]},
    {"id": "p12", "frases": [
        "Número doce. Ruzka, la osa del circo, en la expansión Point Lookout de Fallout tres.",
        "En el rincón noroeste de Point Lookout, en una guarida sin marcador, vive el único yao guai de toda la expansión.",
        "Antes de la guerra era Ruzka, la osa maravilla, la estrella del circo de Point Lookout, famosa por bailar sobre una pelota. Todavía quedan sus carteles.",
        "Doscientos años después sigue ahí, salvaje, veinte por ciento más grande que un yao guai normal, rodeada de esqueletos y jugando con una enorme pelota roja.",
        "Y con las tripas de los pantaneros. Si no tienes la ventaja de amigo de los animales, tú eres el siguiente juguete.",
        "[deadpan] El espectáculo continúa. Solo cambió el público.",
    ]},
    {"id": "p11", "frases": [
        "Número once. Stripe, un sanguinario de bolsillo escondido en la expansión Old World Blues.",
        "Solo aparece si elegiste el rasgo Wild Wasteland. En Higgs Village, detrás de la casa ciento tres, hay una caseta de perro con un plato y una pata de pollo delante.",
        "Te acercas, y sale un sanguinario macho alfa reducido al tamaño de un perro.",
        "Pequeño, sí. Pero tiene ochocientos cincuenta puntos de vida y pega doscientos cincuenta por zarpazo. Te persigue hasta la fuente del pueblo, y ahí se da la vuelta.",
        "Es un homenaje a Stripe, el líder de los Gremlins, que en la película muere en una fuente.",
        "[sarcastic] No lo mojes. Y no le des de comer después de medianoche. Aunque en Big MT nadie sabe qué hora es.",
    ]},
    {"id": "p10", "frases": [
        "Número diez. La reina Nukalurk, en Nuka-World.",
        "Detrás de la planta embotelladora de Nuka-Cola hay un estanque. Y en ese estanque hay una reina de los hombres pinza única, azul y brillante.",
        "Brilla por el estroncio de la Nuka-Cola Quantum, el mismo isótopo que le da su color al refresco.",
        "Nivel sesenta y cuatro, mil quinientos puntos de vida, inmune a la radiación y al veneno. Y el techo y el estanque están llenos de nukalurks.",
        "No sale en la historia, así que muchísima gente termina Nuka-World sin verla. Si la matas, suelta cinco piezas de carne de reina, un ingrediente que no existe en ningún otro lado.",
        "[deadpan] Brilla en la oscuridad, sabe a refresco y te mata. El sueño de cualquier departamento de marketing.",
    ]},
    {"id": "p9", "frases": [
        "Número nueve. Madre Curie tercera, en Fallout tres.",
        "En el monasterio de la Luz Sagrada, la Madre Curie predica la fe en el Átomo, la sabiduría por encima de la violencia. Si la amenazas, ni se defiende.",
        "Pero con Broken Steel instalado hay una condición: si empiezas su misión y después haces estallar la bomba de Megatón, ella estaba predicando allí.",
        "Y vuelve. Como necrófago salvaje de la peor clase: mil cien puntos de vida, y se arranca pedazos radiactivos del cuerpo para lanzártelos y que exploten. El hermano Gerard también se transforma.",
        "Casi nadie la ve así, porque casi nadie vuela Megatón a mitad de una misión.",
        "[sarcastic] Predicaba la paz del Átomo. El Átomo le respondió en persona.",
    ]},
    {"id": "p8", "frases": [
        "Número ocho. Gabe, el perro gigante de la expansión Old World Blues.",
        "En la instalación de pruebas del X-ocho, en Big MT, el doctor Borous tenía una mascota. Un ciberperro.",
        "Tantos estimulantes le dieron, que Gabe creció hasta ser gigante. Nivel treinta y cinco, trescientos setenta y cinco puntos de vida y un ladrido sónico.",
        "Pero tiene cero de percepción. Puedes pasar a su lado en sigilo y no se entera.",
        "Y si lo matas, el cuerpo se vuelve atómico y detona, con una cuenta atrás que ni siquiera es exacta. Lo único sensato es correr lo más lejos posible.",
        "Gabe se llama así por el perro de una diseñadora del juego, que murió mientras lo hacían. Así que también puedes salvarlo. No te dan nada, pero puedes.",
    ]},
    {"id": "p7a", "frases": [
        "Número siete. El alienígena del OVNI estrellado, en Fallout cuatro.",
        "Cuando pasas del nivel veinte, viajando por la Commonwealth, a veces ves pasar algo muy raro por el cielo.",
    ]},
    {"id": "p7", "frases": [
        "Es una nave, que cruza echando humo y se estrella entre los árboles.",
        "Al este de la estación Oberland queda el OVNI medio enterrado en una colina, con los árboles ardiendo, y un rastro de sangre verde que baja a una cueva sin marcar.",
        "Ahí dentro está el único alienígena del juego base, herido, con una pierna lisiada. Te dispara en cuanto te ve: cincuenta puntos de vida y una pistola blaster.",
        "Lo matas, y la pistola alienígena es tuya, con cientos de balas alienígenas.",
        "[deadpan] Cruzó la galaxia para llegar a Boston. Ese fue su primer error.",
    ]},
    {"id": "p6", "frases": [
        "Número seis. El sanguinario legendario, en New Vegas.",
        "La caverna Dead Wind, cerca del paso de Primm y al sur del centro de pruebas de REPCONN, está llena de sanguinarios.",
        "Y en el rincón más profundo, escoltado por otros dos, espera el sanguinario legendario. El único de la cueva que no vuelve a aparecer.",
        "Nivel treinta, mil puntos de vida y doscientos cincuenta de daño por zarpazo, el doble que un sanguinario común.",
        "A su lado hay un soldado muerto de la Hermandad de Acero, con un arma única en la mano, que se llama Mercy, que quiere decir misericordia.",
        "[deadpan] El soldado llevó la misericordia. El sanguinario, no.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. El mutascorpio albino, en Fallout tres.",
        "Solo existe con Broken Steel, y solo cuando ya tienes un nivel alto. Aparece donde salen los mutascorpios gigantes, como la granja junto al cuartel de los Reguladores.",
        "Mil quinientos puntos de vida. En todo Fallout tres solo lo superan el supermutante behemoth y el general Jingwei.",
        "Pega cien por pinchazo, te envenena, es más rápido que un mutascorpio normal, y a los jugadores de nivel alto les salen más albinos que normales.",
        "Y lo mejor: se cura poco a poco con la luz del sol.",
        "[sarcastic] Un albino que se cura al sol. La radiación también tiene sentido del humor.",
    ]},
    {"id": "subs", "frases": [
        "[deadpan] Una pausa en la transmisión. Radio Yermo sigue subiendo la antena, y cada suscripción es un watt más de señal en el Yermo.",
        "Si te está sirviendo, suscríbete y activa la campana, porque quedan cuatro, y el número uno no es lo que esperas.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Los sanguinarios camaleón y mítico, en Fallout cuatro.",
        "Están en el juego desde el principio, pero casi nadie los ve, porque solo aparecen cuando tu personaje tiene un nivel altísimo.",
        "El sanguinario camaleón sale a partir del nivel ochenta y uno. Durante el combate su piel cambia de color: gris, verde ácido, rojo, naranja, turquesa. Y el cadáver se queda con el último.",
        "El mítico, a partir del nivel noventa y uno. Mil trescientos sesenta puntos de vida o más, y un golpe fuerte de trescientos cincuenta. Los sanguinarios no legendarios más fuertes del juego.",
        "Y cuando por fin matas al mítico, entre su botín hay un cigarrillo.",
        "[deadpan] Noventa y un niveles de esfuerzo, y la recompensa es un cigarrillo. Al menos el Yermo es honesto.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. Rawr, en Lonesome Road.",
        "En la Divisoria, pasando la azotea del hotel Boxwood, hay una cueva. Entras, se derrumba la salida, y te quedas encerrado con él.",
        "Rawr es un sanguinario único. Nivel cuarenta y cinco, novecientos puntos de vida y trescientos cincuenta de daño por zarpazo. No se le puede derribar.",
        "Y sus atributos rozan el máximo: diez en casi todo, menos un siete en carisma y un cinco en inteligencia.",
        "Su última víctima, un soldado de la RNC llamado Gleeson, dejó una baliza de socorro. Ahí está la pista: Rawr huye de las bengalas.",
        "[sarcastic] Un sanguinario más listo que la mitad de la RNC. Y aun así le tiene miedo a una bengala.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Hundebarcos, en Far Harbor.",
        "Mientras exploras la Isla, a veces tu Pip-Boy capta una frecuencia de radio rara, una señal que interfiere con las demás. Es ella.",
        "Un reptador de la Niebla legendario y único, de nivel setenta y cinco o más, que hunde barcos por deporte. El Viejo Longfellow lleva años cazándola.",
        "Tiene como mínimo dos mil doscientos puntos de vida, y cuatro mil puntos de resistencia al daño físico. Cuatro mil.",
        "Solo aparece en esa misión, y si la señal se pierde, la puedes perder a ella. Si la matas, Longfellow te da un arpón único.",
        "[sighs] Longfellow dice que preferiría morir entre sus garras que de cualquier otra forma. En el Yermo, eso es romántico.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. La tochomosca legendaria, en Old World Blues.",
        "En el noreste de Big MT, cerca del túnel norte, hay una cueva misteriosa que no pertenece a ninguna misión. A la izquierda de la entrada, en una cámara, espera ella.",
        "Es la criatura más poderosa de todo New Vegas. Más que cualquier sanguinario.",
        "Nivel cincuenta. Dos mil puntos de vida. Cuatrocientos cincuenta de daño cuerpo a cuerpo, y dispara plasma por el abdomen, a trescientos por disparo. Vuela alto, brilla en verde, y al morir explota como una granada de plasma.",
        "Si la matas, suelta cincuenta pedazos de carne de tochomosca, veinte Psycho y veinte Buffout. Y nació de una broma: un jugador la pidió en un foro, y los desarrolladores la hicieron de verdad.",
        "[deadpan] Sanguinarios, cazadores, un oso de circo y un alienígena. Y el rey del Mojave es una mosca.",
    ]},
    {"id": "cierre", "frases": [
        "Esos son los quince. Ahora dime en los comentarios cuántos encontraste tú, porque alguien vio a Stripe y no se lo contó a nadie.",
        "Todos los comentarios se leen, y los mejores salen en la próxima transmisión.",
        "Y si te gusta Skyrim, el canal hermano es Crónicas de Tamriel. Misma receta, otro fin del mundo.",
        "[deadpan] Esto fue Radio Yermo. Suscríbete, no entres a una cueva sin marcador, y recuerda: en el Yermo, lo que no sale en el mapa, también muerde.",
    ]},
]

# ------------------------------------------------------------------ filtro de radio (modo B, nucleo/voz_fx.py → mezcla)
VOZ_FX_DEFECTO = "tinte"                     # los datos: narrador cerca del micrófono con un toque de radio
VOZ_FX = {"intro_0": "radio+sintonia", "subs_0": "radio+sintonia", "subs_1": "radio",
          "cierre_3": "radio+sintonia"}
for _e in ESCENAS:                            # el remate de cada puesto sale por la radio del Yermo
    if _e["id"].startswith("p") and not _e["id"].endswith("a"):
        VOZ_FX[f"{_e['id']}_{len(_e['frases']) - 1}"] = "radio"
