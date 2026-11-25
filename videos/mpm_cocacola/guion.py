# -*- coding: utf-8 -*-
"""GUION — Mil por Minuto, 2.º video: cómo se fabrica la COCA-COLA en México + el negocio (24-nov-2026).
Motor SECUENCIA YT (docs/estilo_secuencia_yt.md) + kit nucleo/mg_planta.py + escenas 3D orbitales (nucleo/fabrica3d.py, estilo a elegir).
Datos: investigacion.md (cada cifra con su fuente; lo «NC» no se dice como hecho: el proceso genérico va como «así funciona una línea»).
Contador: SOLO Coca-Cola FEMSA en México (9,553.8 M botellas o latas en 2025 ≈ 303 por segundo); nunca «todo México».
Voz: Brian C de ElevenLabs (cálido, sin prisa, de quien recorrió la planta), eleven_v4_turbo, sin [whispers]/[excited]/[shouts]. La voz no cita fuentes.
"""

TITULO = "Así se FABRICA la Coca-Cola en México"
ARCHIVO = "mpm_cocacola"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 92
VOZ = dict(motor="elevenlabs", voice_id="Czw3Dn181ypdrCOnPfif", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit"),
           referencia=r"C:\FabricaAnimaciones\videos\_muestras_voz_fallout\04_brian.mp3")
FONETICA = {}
# Whisper escribe las cifras con dígitos («$3.08», «2,200», «1,5%») y «Apisaco»: la voz las dice bien (transcripción revisada el 24-nov-2026)
CER_MAX_POR_FRASE = {"intro_2": 0.08, "mitos_7": 0.22, "mitos_10": 0.05, "mapa_4": 0.03}
TAIL_MAX_POR_FRASE = {k: 1.3 for k in ("proceso_3", "proceso_15", "trivia_1", "mitos_8", "cierre_2")}   # terminan en palabra corta o pregunta

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=7.5,             # canal de fábricas: cortes algo más rápidos que los de juegos
    transicion="slideleft",
    fundido=0.30,
    ambiente=0.0,
    ambiente_por={},
    yt=dict(sufijo="", min_s=60, max_min=240, alto=1080, evitar_canales=[]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(
    estilo="Modern documentary underscore about factories and big business: pulsing muted synth arpeggios, light mechanical "
           "percussion like conveyor clanks, warm bass, curious and confident, instrumental only, no vocals, unobtrusive under narration.",
    escenas={
        "intro": ("curious and punchy, building momentum", 4),
        "origen": ("warm nostalgic Americana turning into Mexican family business, soft vintage texture over pulse", 3),
        "suscripcion": ("light and friendly, the pulse keeps going", 3),
        "proceso": ("precise mechanical rhythm, steady and fascinating, fizzy ticking percussion", 4),
        "trivia": ("playful quiz pulse, light ticking", 3),
        "proceso_2": ("precise mechanical rhythm continues, brighter, high-speed bottling energy", 4),
        "negocio": ("ambitious and rising, corporate growth, bigger drums", 4),
        "mitos": ("investigative and calm, slightly tense", 3),
        "mapa": ("expansive, travelling, wide", 3),
        "cierre": ("resolved and warm, gentle outro", 2),
    },
    tramos=[(["intro"], "Begin with a punchy hit. Keep a steady pulse to the end."),
            (["origen", "suscripcion"], "Warm and nostalgic, then friendly. End on a held tone."),
            (["proceso"], "Mechanical and precise from the start. Keep the pulse; end flowing."),
            (["trivia", "proceso_2"], "Playful quiz first, then high-speed bottling energy."),
            (["negocio"], "Ambitious and rising throughout; end on a strong held chord."),
            (["mitos"], "Calm investigative tension throughout."),
            (["mapa"], "Wide and travelling, a sense of scale."),
            (["cierre"], "Resolved and warm, ending softly in the last seconds.")],
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "[curious] Una botella con cintura. Una etiqueta roja. Y ese chasquido del gas cuando le quitas la tapa.",
        "En mayo de 1886, en una farmacia de Atlanta, esta bebida se vendía a cinco centavos el vaso. [short pause] Y en todo su primer año, el promedio fue de nueve vasos al día.",
        "Nueve. [short pause] Hoy, en el mundo, se sirven más de dos mil doscientos millones de bebidas de esta compañía cada día.",
        "Y aquí viene lo raro: la empresa dueña de Coca-Cola casi no embotella Coca-Cola. Vende un concentrado. El trabajo pesado lo hacen otras empresas.",
        "La más grande de todas es mexicana. [short pause] Y solo en México, en 2025, vendió nueve mil quinientos cincuenta y tres millones de botellas y latas.",
        "Para llegar a cada una, hay una bóveda con una fórmula secreta, agua de pozo que se limpia una y otra vez, una preforma que se infla como globo, gas a presión y una máquina que llena botellas sin parar.",
        "[thoughtful] Así que hoy entramos a la planta. ¿Cómo se fabrica realmente una Coca-Cola?",
        "Mira la esquina de tu pantalla: ese contador va sumando las botellas y latas que vende Coca-Cola FEMSA en México desde que empezó este video. Son unas trescientas por segundo. Al final te digo cuántas juntó.",
    ]},
    {"id": "origen", "frases": [
        "Todo empezó con un farmacéutico de Atlanta: John Pemberton. Preparó un jarabe y lo llevó a la Farmacia Jacobs, en el centro de la ciudad.",
        "El nombre no fue idea suya. Fue de su socio y contador, Frank Robinson, que además escribió el logo a mano, con su propia letra.",
        "Pemberton murió en 1888 sin ver el negocio crecer. Y el que se quedó con todo fue un empresario llamado Asa Candler.",
        "[amused] ¿Cuánto pagó por quedarse con todo? En total, dos mil trescientos dólares.",
        "En 1892 fundó The Coca-Cola Company. Y dos años después, en Vicksburg, Mississippi, Joseph Biedenharn hizo algo nuevo: la metió en botellas.",
        "Y aquí viene la decisión que todavía mueve el negocio. En 1899, dos empresarios de Chattanooga, Tennessee, le pidieron a Candler los derechos para embotellarla en casi todo Estados Unidos.",
        "[short pause] Y Candler les vendió esos derechos por un dólar.",
        "Un dólar. Con el tiempo, la compañía tuvo que volver a comprar esos derechos. Pero de ese trato nació el modelo que hoy usa en todo el mundo: Coca-Cola hace el concentrado, y los embotelladores hacen todo lo demás.",
        "En 1915 se patentó la botella con cintura. [short pause] Y su inspiración no fue la hoja de coca: fue una vaina de cacao.",
        "Y en 1926 la Coca-Cola llegó a México. Las primeras concesiones para embotellarla fueron para Manuel Barragán en Monterrey, y para Herman Fleishman en Tampico.",
        "De la planta de Barragán, la de Topo Chico, nació con los años Arca Continental, hoy el segundo embotellador de Coca-Cola más grande de las Américas.",
        "Y en Monterrey había otra empresa, una cervecería fundada en 1890: la Cervecería Cuauhtémoc. En 1979 compró embotelladoras de refresco en la Ciudad de México. [short pause] De ahí salió Coca-Cola FEMSA.",
        "Hoy FEMSA es el embotellador de Coca-Cola más grande del mundo por volumen. [short pause] Una cervecería de Monterrey terminó siendo la mano más grande de la marca más famosa del planeta.",
    ]},
    {"id": "suscripcion", "frases": [
        "[short pause] Antes de entrar a la planta: en Mil por Minuto desarmamos, pieza por pieza, cómo se fabrican las marcas que compras todos los días.",
        "Si te gusta saber qué hay detrás de las cosas, suscríbete. Es gratis, y la mayoría de quienes ven estos videos todavía no lo está.",
    ]},
    {"id": "proceso", "frases": [
        "Ahora sí. [short pause] Estación uno: el concentrado.",
        "La embotelladora no puede comprarle el concentrado a nadie más. Se lo vende The Coca-Cola Company, y la fórmula no sale de sus manos.",
        "Esa fórmula pasó ochenta y seis años guardada en la bóveda de un banco. En 1919 sirvió de garantía para un préstamo, y en 2011 se mudó a una bóveda dentro del museo de la marca, en Atlanta.",
        "[amused] La compañía dice que solo dos personas conocen la receta completa y que nunca viajan juntas. Puede ser leyenda. Pero la leyenda también vende.",
        "Estación dos: el agua. Y es más importante de lo que parece, porque una Coca-Cola es casi toda agua.",
        "En México, las embotelladoras la sacan sobre todo de pozos propios, con permiso del gobierno. Y antes de usarla, se trata: se filtra, se pule, y en las plantas nuevas pasa por ósmosis inversa.",
        "¿Por qué tanto? [short pause] Porque una Coca de Toluca tiene que saber igual que una de Mérida. El agua de cada pozo es distinta. La bebida no puede serlo.",
        "Hoy Coca-Cola FEMSA usa un litro con treinta y cinco de agua por cada litro de bebida. En 2018 usaba casi quince por ciento más.",
        "Estación tres: el jarabe. Primero se disuelve el azúcar en agua tratada: eso es el jarabe simple. Luego se le agrega el concentrado, y queda el jarabe terminado.",
        "Ese jarabe se mezcla con agua tratada en una proporción exacta. Siempre la misma. Ahí está la Coca-Cola, todavía sin gas.",
        "Estación cuatro: la botella. Y aquí hay un truco que casi nadie conoce. [short pause] La botella de plástico no llega a la planta como botella.",
        "Llega como esto: una preforma, un tubito grueso del tamaño de un dedo, con la rosca ya hecha.",
        "La preforma se calienta, una varilla la estira hacia abajo, y aire a presión la infla contra un molde. En una fracción de segundo, el tubito se vuelve botella.",
        "Al estirarse en dos direcciones, el plástico se acomoda y se vuelve más resistente. Por eso una botella tan delgada aguanta la presión del gas.",
        "En la planta de Toluca, una sola máquina por línea sopla la botella, la llena y la etiqueta.",
        "Estación cinco: las retornables. Las botellas de vidrio y de plástico grueso que regresas a la tienda vuelven a la planta, se lavan por dentro y por fuera, y se revisan una por una.",
        "Una de plástico retornable se usa de veinte a veinticinco veces. Una de vidrio, de treinta y cinco a cincuenta.",
    ]},
    {"id": "trivia", "frases": [
        "Vamos con una pregunta, y la respuesta te la doy al final.",
        "¿Qué es más ácido? ¿A, la Coca-Cola? ¿B, el jugo de limón? ¿O C, son igual de ácidos? [short pause] Déjalo en los comentarios.",
    ]},
    {"id": "proceso_2", "frases": [
        "Estación seis: el gas. La bebida se enfría antes de recibir el dióxido de carbono.",
        "¿Por qué fría? [short pause] Porque el agua fría atrapa mucho más gas. Si estuviera tibia, el gas se escaparía y la botella saldría llena de espuma.",
        "Estación siete: el llenado. Y esta es la máquina más impresionante de toda la planta.",
        "Es un carrusel. Las botellas entran por una banda, se suben a una rueda que gira sin parar, y cada una queda debajo de su propia válvula.",
        "Antes de que caiga una sola gota, la válvula llena la botella con gas a presión. Se llama llenado a contrapresión.",
        "Así, cuando el refresco entra, no encuentra diferencia de presión, el gas no se escapa, y la botella se llena sin espuma. [short pause] Todo eso pasa mientras la rueda da media vuelta.",
        "En Toluca, una sola línea llena cuarenta mil botellas por hora. Y la de latas, mil ochocientas por minuto.",
        "Estación ocho: la tapa. Apenas sale del carrusel, una tapadora le enrosca la tapa a cada botella, antes de que el gas tenga tiempo de escapar.",
        "Estación nueve: la revisión y la etiqueta. Se revisa el nivel, la tapa y el código del lote. La botella que sale mal, se va de la línea.",
        "Y no solo revisan máquinas. En el laboratorio de Toluca hay cuarenta catadores por turno probando que la Coca sepa como debe saber.",
        "Estación diez: las tarimas y los camiones. Las botellas se agrupan en paquetes, los paquetes en tarimas, y las tarimas suben a los camiones.",
        "Toluca, una de las plantas más grandes de todo el sistema Coca-Cola en el mundo, saca unas setecientas mil cajas al día.",
    ]},
    {"id": "negocio", "frases": [
        "Ahora, el negocio. Porque fabricar una Coca es una cosa. Venderla en cada esquina es otra.",
        "¿Recuerdas el concentrado? Su precio no es fijo. La compañía lo cobra como un porcentaje de lo que pagas tú en la tienda.",
        "Si la Coca sube de precio en la tiendita, el concentrado también. [short pause] Y en México, ese porcentaje subió en 2021 y otra vez en 2022.",
        "Es un negocio muy elegante: la compañía cuida la marca y la fórmula. Las fábricas, los camiones, los pozos y los refrigeradores los pone el embotellador.",
        "En México hay ocho grupos embotelladores, setenta y tres plantas y más de trece mil rutas de reparto.",
        "Y su terreno no es el supermercado. Es la tiendita. Coca-Cola FEMSA vende en México sobre todo por el canal tradicional, el de la tienda de la esquina.",
        "El sistema dice llegar a más de un millón doscientos mil pequeños comercios en todo el país.",
        "En 2025, solo el negocio de Coca-Cola FEMSA en México facturó ciento treinta y seis mil millones de pesos.",
        "Y México pesa: es más del cuarenta por ciento de todo lo que la compañía vende en América Latina.",
        "Tanto, que en febrero de 2026 se anunció una inversión de seis mil millones de dólares de The Coca-Cola Company en México.",
        "Pero ojo: en 2025, Coca-Cola FEMSA vendió en México cinco por ciento menos que el año anterior. [short pause] Y para 2026 le esperaba otro golpe: los impuestos.",
    ]},
    {"id": "mitos", "frases": [
        "Con una bebida tan famosa, también llegaron los mitos y las polémicas. Vamos a separarlos con datos.",
        "Primero: ¿la Coca-Cola lleva cocaína? [short pause] Hoy no. La receta original usaba un extracto de hoja de coca. A partir de 1903 se usó hoja sin cocaína, y hacia 1929 ya no quedaba ni rastro.",
        "Segundo: ¿la Coca-Cola era verde? [short pause] No. Siempre fue café. Lo verde era el vidrio de las botellas.",
        "Tercero: ¿disuelve un clavo? [short pause] No. El ácido fosfórico le quita el óxido, y el clavo queda brillante. Pero entero.",
        "Cuarto: ¿la Coca mexicana es de azúcar de caña? [short pause] La que se vende en México lleva las dos cosas: azúcar y jarabe de alta fructosa. Lo dice la etiqueta.",
        "La famosa Coca mexicana de vidrio que se vende en Estados Unidos, esa sí va con caña. Y en 2025, después de un mensaje del presidente Trump, la compañía anunció allá una versión extra con azúcar de caña.",
        "Quinto, los impuestos. En 2014, México le puso un peso por litro a las bebidas azucaradas. Ese año, las compras bajaron seis por ciento en promedio, y en los hogares de menos ingresos, nueve.",
        "En 2026, el impuesto casi se duplicó: pasó a tres pesos con ocho centavos por litro.",
        "Y desde octubre de 2020, la botella lleva los sellos negros de advertencia. [short pause] Uno dice: contiene cafeína, evitar en niños.",
        "Y sexto, el agua. En San Cristóbal de las Casas, en Chiapas, hay una planta embotelladora desde 1994, y vecinos que reciben agua unas horas cada dos días.",
        "La autoridad del agua dice que la planta tiene permiso para menos del uno y medio por ciento del agua disponible de su acuífero, y que el problema está en la red de la ciudad.",
        "Los críticos acusan que saca más de lo que dice el permiso. [short pause] Las dos versiones siguen ahí, y la planta, también.",
    ]},
    {"id": "mapa", "frases": [
        "Hagamos el mapa completo.",
        "En Nuevo León, Monterrey: la concesión de 1926 y la cervecería de 1890. El lugar donde empezaron los dos gigantes.",
        "En Tamaulipas, Tampico y Altamira, donde sigue la planta La Pureza.",
        "En el Estado de México, Toluca: la planta gigante, y a su lado, la que se considera la recicladora de botellas de plástico para uso alimenticio más grande del mundo. Procesa más de ciento veinte mil toneladas al año.",
        "En Tlaxcala, Apizaco. En Guanajuato, León. En Michoacán, Morelia.",
        "En Chiapas, San Cristóbal de las Casas, la planta de la polémica.",
        "Y en Yucatán, Valladolid: una planta inaugurada en septiembre de 2026, la primera planta nueva de refrescos con gas en México en más de veinte años. Solo para botellas retornables.",
        "De un pozo en Toluca a una tiendita en cualquier esquina del país.",
    ]},
    {"id": "cierre", "frases": [
        "Así que la próxima vez que le quites la tapa a una Coca, piensa en todo lo que pasó para llegar ahí.",
        "Una fórmula en una bóveda. Agua de pozo tratada. Una preforma que se infló en una fracción de segundo. Gas que solo entra si está frío. Y un carrusel que no se detiene.",
        "La respuesta de la trivia: [short pause] la B. El jugo de limón es un poquito más ácido que la Coca-Cola. Así que, si la Coca disolviera un clavo, el limón también lo haría.",
        "Y el contador de la esquina: mientras veías este video, Coca-Cola FEMSA vendió en México más de doscientas cincuenta mil botellas y latas.",
        "Si quieres que entremos a la fábrica de otra marca, dime cuál en los comentarios. Y suscríbete a Mil por Minuto: aquí desarmamos lo que compras todos los días.",
    ]},
]
