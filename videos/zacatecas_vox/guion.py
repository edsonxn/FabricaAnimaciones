# -*- coding: utf-8 -*-
"""Zacatecas, 1546-1600: cómo se vivieron los primeros años de la ciudad de la plata.
Formato VERTICAL (1080x1920), estilo Vox (papel recortado, mapas, rotulación cinética, dibujo cuadro a cuadro),
PLANO SECUENCIA: sin cortes; todo es un único mundo continuo (escenas.py -> Mundo).

Datos verificados (fuentes):
  - 1546: indígenas de Tlaltenango informan a Juan de Tolosa de minerales al norte; campamento al pie de la Bufa
    (INAH / Catálogo Nacional de Bienes Culturales; Wikipedia: Juan de Tolosa).
  - 11 de junio de 1548: se descubre la veta de San Bernabé; luego Veta Grande, Pánuco y Albarrada.
  - 1549: ~300 habitantes (Scielo, "Abastecimiento de productos básicos a Zacatecas, siglos XVI y XVII").
  - 1550: 34 minas en operación. Las casas se agrupan sin orden junto a las minas, el arroyo y las laderas.
  - Beneficio de patio (amalgamación con mercurio): Bartolomé de Medina, Pachuca, ~1555; en Zacatecas desde 1557.
  - Falta de población indígena sedentaria para el repartimiento; población flotante atraída por parte del
    mineral; esclavos africanos: 230 en 1597 (Enciso Contreras; Historia económica general de México).
  - Guerra Chichimeca 1550-1590, la más larga y costosa de la Nueva España; presidios y escoltas;
    marzo de 1590: el virrey Luis de Velasco II encarga a Miguel Caldera la paz (comida, ropa, ganado).
  - Hospitales y hospicios en los años 1550; mercados y matadero regulados en los 1570-1580 (Scielo, abasto).
  - El mercurio (azogue) venía de España (Almadén).
  - Franciscanos: primer convento hacia 1558 (Gaceta UAZ). Título de ciudad: Felipe II, 1585; escudo 1588.
  - Centro histórico de Zacatecas: Patrimonio Mundial de la UNESCO (1993).
"""

TITULO = "Zacatecas: cómo se vivieron sus primeros años"
ARCHIVO = "zacatecas_primeros_anos"
ESTILO_VISUAL = "vox"
FORMATO = "vertical"
DURACION = 180.0
BPM = 96
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.0, sfx=-22.5)
TRANSICIONES = [("continua", 0.1)] * 8
MUSICA = {
    "mapa": dict(sabor="vacio"),
    "cerro": dict(sabor="espacio"),
    "campamento": dict(sabor="tension"),
    "mina": dict(sabor="tension", raiz=38),
    "camino": dict(sabor="vacio", raiz=40),
    "ciudad": dict(sabor="espacio", raiz=43),
    "plata": dict(sabor="esperanza"),
    "cierre": dict(sabor="esperanza", raiz=43),
}

ESCENAS = [
    {
        "id": "mapa",
        "frases": [
            "Mil quinientos cuarenta y seis.",
            "Al norte de la Nueva España no existe ninguna ciudad.",
            "Solo cerros secos, nopales, y pueblos nómadas que llevan siglos ahí.",
            "Zacatecos, huachichiles, y otros que los conquistadores llamarían chichimecas.",
        ],
    },
    {
        "id": "cerro",
        "frases": [
            "Ese año, unos indígenas le hablan al capitán Juan de Tolosa de unas piedras brillantes, más al norte.",
            "Tolosa llega al pie de un cerro que parece un odre de vino: la Bufa.",
            "Y ahí arma su campamento.",
            "En mil quinientos cuarenta y ocho aparece la veta de San Bernabé, y empieza la fiebre de la plata.",
            "Socios con dinero, como Oñate, Ibarra y Bañuelos, financian las primeras minas.",
        ],
    },
    {
        "id": "campamento",
        "frases": [
            "En mil quinientos cuarenta y nueve viven allí unas trescientas personas.",
            "Las casas se amontonan sin orden, pegadas a las minas, junto al arroyo y sobre las laderas.",
            "Todo se vende caro, porque el maíz y la carne llegan de rancherías lejanas.",
            "Aun así, en mil quinientos cincuenta ya funcionan treinta y cuatro minas.",
            "Por esos años se levantan también hospitales y hospicios, para tantos recién llegados.",
        ],
    },
    {
        "id": "mina",
        "frases": [
            "Bajo tierra, el trabajo es brutal.",
            "Los mineros cavan a golpe de barreta, con la luz de una vela.",
            "Y los cargadores suben el mineral a la espalda, por escalas de troncos.",
            "Casi no hay pueblos indígenas cercanos a los que obligar a trabajar.",
            "Así que llegan trabajadores atraídos por una parte del mineral.",
            "Y también hay indígenas y africanos esclavizados: en mil quinientos noventa y siete se cuentan unos doscientos treinta africanos.",
        ],
    },
    {
        "id": "patio",
        "frases": [
            "Hacia mil quinientos cincuenta y siete llega un truco nuevo: el beneficio de patio.",
            "Se muele el mineral, se mezcla con sal y mercurio, y las mulas lo pisan durante semanas.",
            "El mercurio atrapa la plata, y así se saca más de un mineral pobre.",
            "Ese mercurio viaja desde España, y sin él no hay plata.",
        ],
    },
    {
        "id": "camino",
        "frases": [
            "Pero la plata tiene que llegar a la Ciudad de México, y el camino cruza territorio en guerra.",
            "Desde mil quinientos cincuenta, los chichimecas atacan las caravanas: defienden tierras que otros invaden.",
            "Es el conflicto más largo y más caro de la Nueva España.",
            "Se levantan presidios y las caravanas viajan con escolta.",
            "Al final, la fuerza no basta.",
            "En mil quinientos noventa, Miguel Caldera negocia la paz: comida, ropa y ganado.",
        ],
    },
    {
        "id": "ciudad",
        "frases": [
            "Mientras tanto, la aldea se vuelve ciudad.",
            "Los franciscanos fundan su convento hacia mil quinientos cincuenta y ocho.",
            "En mil quinientos ochenta y cinco, el rey de España le da el título de ciudad.",
            "Y en mil quinientos ochenta y ocho, su escudo de armas.",
            "Para entonces ya tiene mercados, y hasta un matadero con reglas propias.",
        ],
    },
    {
        "id": "plata",
        "frases": [
            "La plata sale en mulas y carretas hacia la capital, cruza el mar hasta Sevilla, y llega mucho más lejos.",
            "Se convierte en monedas que pagan guerras, imperios y comercio en varios continentes.",
        ],
    },
    {
        "id": "cierre",
        "frases": [
            "Pero esa riqueza tuvo un costo, y lo pagaron sobre todo quienes cavaron en la oscuridad.",
            "Hoy, el centro histórico de Zacatecas es Patrimonio de la Humanidad.",
            "Cada calle empinada empezó con alguien que bajó a una mina.",
        ],
    },
]
