# -*- coding: utf-8 -*-
"""Un día en la vida hace 30 000 años — estilo doodle (sin psicodelia), ~4:00, voz de Dan, canal Sapiens con Wifi.
Siete momentos del día (amanecer → noche) sobre el Paleolítico superior de Europa (cazadores-recolectores gravetienses).
Datos verificados; las fuentes aparecen en pantalla y en la descripción. Números de la narración en palabras.

Notas de rigor (lo que sí se sabe y lo que es reconstrucción):
  - Agujas de hueso con ojo: usadas desde hace más de 40 000 años (Smithsonian, Human Origins).
  - Dieta: isótopos de huesos de Dolní Věstonice y Pavlov (Chequia) muestran mucho mamut; otros sitios, pescado (Richards et al. 2001, PNAS).
  - Flautas de hueso de buitre y de marfil de mamut de Hohle Fels y Geissenklösterle (Alemania), ~40 000 años (Conard et al. 2009, Nature).
  - Cerámica más antigua conocida: figurillas de arcilla cocida de Dolní Věstonice, ~29 000-25 000 años (Museo de Moravia, Brno).
  - Cueva Chauvet (Francia): pinturas de ~36 000 años (UNESCO). Hombre león de Hohlenstein-Stadel: ~40 000 años (UNESCO, Cuevas de la Jura de Suabia).
  - Sungir (Rusia): entierros de dos niños con miles de cuentas de marfil, ~34 000 años (Nalawade-Chavan et al. 2014, PLOS ONE).
  - Tamaño de las bandas: entre veinte y cincuenta personas (antropología de cazadores-recolectores). Era glacial: clima mucho más frío que el actual.
"""

TITULO = "Un día en la vida hace 30.000 años"
ARCHIVO = "un_dia_hace_30000_anos"
ESTILO_VISUAL = "doodle"
DURACION = None
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.0)
TRANSICIONES = [("persianas", 0.8), ("paneo", 1.1), ("ola", 0.85), ("bajada", 1.1),
                ("iris", 1.0), ("zoom_suave", 1.1), ("burbujas", 0.9), ("paneo", 1.1)]
MUSICA = {
    "intro": dict(sabor="build"), "amanecer": dict(sabor="flauta"), "desayuno": dict(sabor="lounge"),
    "caza": dict(sabor="epico"), "mediodia": dict(sabor="brillo"), "tarde": dict(sabor="funk"),
    "atardecer": dict(sabor="dub"), "noche": dict(sabor="reloj"), "cierre": dict(sabor="final"),
}

ESCENAS = [
    {
        "id": "intro",
        "frases": [
            "Imagina despertar hace treinta mil años. Sin reloj, sin calles y sin nadie que te diga qué hacer.",
            "Tu cerebro es igual de grande que el tuyo de hoy. Lo que cambia es todo lo demás.",
            "Este es un día completo en la vida de un humano de la era de hielo.",
        ],
    },
    {
        "id": "amanecer", "num": 1, "titulo": "EL AMANECER", "fase_b": 3, "etiqueta_numero": "MOMENTO",
        "sello": "HACE ~30.000 AÑOS", "icono": "fuego", "icono_hoy": "aguja",
        "dato": "Agujas de hueso con ojo: más de 40.000 años",
        "fuente": "Smithsonian, Human Origins",
        "frases": [
            "Momento uno: el amanecer.",
            "Hace un frío terrible, y lo más valioso del campamento son las brasas de anoche.",
            "Si se apagan, hay que encender fuego de nuevo, golpeando piedras, y eso puede llevar un buen rato.",
            "Te pones ropa de pieles, cosida con agujas de hueso, que ya existían desde hace más de cuarenta mil años.",
            "Y compartes el fuego con tu grupo, unas treinta personas, casi todas familiares.",
        ],
    },
    {
        "id": "desayuno", "num": 2, "titulo": "EL DESAYUNO", "fase_b": 3, "etiqueta_numero": "MOMENTO",
        "sello": None, "icono": "hueso", "icono_hoy": "hamburguesa",
        "dato": "Isótopos de Dolní Věstonice (Chequia): dieta con mucho mamut",
        "fuente": "Richards et al. 2001, PNAS",
        "frases": [
            "Momento dos: el desayuno.",
            "No hay tienda ni refrigerador. Comes lo que recolectaste ayer: frutos secos, raíces y carne seca.",
            "Todos ayudan en la tarea: niños, adultos y abuelos.",
            "Los huesos de esa época demuestran que algunos grupos comían muchísimo mamut.",
            "Y otros, sobre todo pescado de río. Tú pides un desayuno. Ellos tenían que conseguirlo.",
        ],
    },
    {
        "id": "caza", "num": 3, "titulo": "LA CAZA", "fase_b": 3, "etiqueta_numero": "MOMENTO",
        "sello": None, "icono": "mamut", "icono_hoy": "cavernicola",
        "dato": "Cabañas hechas con huesos de mamut en Europa central",
        "fuente": "Museo de Moravia, Brno",
        "frases": [
            "Momento tres: la caza.",
            "Los animales de la era de hielo son gigantes: mamuts, rinocerontes lanudos, bisontes y caballos salvajes.",
            "Cazan en grupo, con lanzas de punta de piedra, y a veces los acorralan en un barranco.",
            "Un solo mamut alimenta a todos durante semanas, pero es un trabajo muy peligroso.",
            "Y con sus huesos y colmillos, algunos grupos construían cabañas enteras.",
        ],
    },
    {
        "id": "mediodia", "num": 4, "titulo": "EL MEDIODÍA", "fase_b": 3, "etiqueta_numero": "MOMENTO",
        "sello": "HACE ~40.000 AÑOS", "icono": "flauta", "icono_hoy": "nota",
        "dato": "Flautas de hueso de buitre y marfil de mamut: ~40.000 años",
        "fuente": "Conard et al. 2009, Nature",
        "frases": [
            "Momento cuatro: el mediodía.",
            "Mientras unos cazan, en el campamento se talla piedra.",
            "Con un buen trozo de sílex sacas láminas casi tan afiladas como un bisturí.",
            "También fabrican agujas, collares, y figuras de marfil.",
            "Y alguien toma un hueso de buitre, le hace agujeros, y se escucha una flauta. Sí, hace treinta mil años ya había música.",
        ],
    },
    {
        "id": "tarde", "num": 5, "titulo": "LA TARDE", "fase_b": 3, "etiqueta_numero": "MOMENTO",
        "sello": "HACE ~29.000 AÑOS", "icono": "bebe", "icono_hoy": "vasija",
        "dato": "Figurillas de arcilla cocida de Dolní Věstonice (Chequia)",
        "fuente": "Museo de Moravia, Brno",
        "frases": [
            "Momento cinco: la tarde.",
            "Los niños no van a la escuela, pero aprenden todo el tiempo: imitan la caza, tallan piedras y escuchan historias.",
            "En algunos sitios modelaban animales y figuras con arcilla.",
            "Las cocían en hornos de tierra, y esas figurillas son la cerámica más antigua que se conoce.",
            "Miles de años antes de fabricar vasijas, ya trabajaban el barro.",
        ],
    },
    {
        "id": "atardecer", "num": 6, "titulo": "EL ATARDECER", "fase_b": 3, "etiqueta_numero": "MOMENTO",
        "sello": None, "icono": "dia_noche", "icono_hoy": "pan",
        "dato": "Grupos de entre veinte y cincuenta personas compartían la comida",
        "fuente": "Antropología de cazadores-recolectores",
        "frases": [
            "Momento seis: el atardecer.",
            "Regresan los cazadores, cargados de carne, y empieza la cena.",
            "Asan la carne sobre las brasas, y cocinan en hoyos con piedras calientes.",
            "Y si la caza fue buena, se comparte todo con todos.",
            "Compartir la comida era la mejor forma de sobrevivir al invierno.",
        ],
    },
    {
        "id": "noche", "num": 7, "titulo": "LA NOCHE", "fase_b": 4, "etiqueta_numero": "MOMENTO",
        "sello": "HACE ~36.000 AÑOS", "icono": "hombre_leon", "icono_hoy": "estrella",
        "dato": "Cueva Chauvet (Francia): pinturas de hace más de 30.000 años",
        "fuente": "UNESCO, Patrimonio Mundial",
        "frases": [
            "Momento siete: la noche.",
            "Alrededor del fuego llega lo mejor del día: las historias.",
            "En la cueva de Chauvet, en Francia, alguien pintó leones, caballos y rinocerontes con carbón, a la luz de una antorcha.",
            "En Alemania, otro artista talló en marfil a un hombre con cabeza de león.",
            "Y en Rusia, dos niños fueron enterrados con miles de cuentas de marfil cosidas a su ropa.",
            "Como ves, no eran brutos: eran artistas, y se quedaban despiertos hasta tarde.",
        ],
    },
    {
        "id": "cierre", "cierre": "¿HABRÍAS SOBREVIVIDO?",
        "frases": [
            "Un día duro, frío y sin comodidades. Pero con fuego, música, arte y familia.",
            "Tú tienes teléfono y wifi. Ellos tenían algo que tú también tienes: las mismas ganas de contar historias.",
            "¿Habrías sobrevivido un día así? Cuéntalo en los comentarios.",
        ],
    },
]
