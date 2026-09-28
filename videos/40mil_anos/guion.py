# -*- coding: utf-8 -*-
"""Guion: 10 cosas que hacían los humanos hace 40 mil años y seguimos repitiendo.

Cada escena tiene frases cortas (Chatterbox rinde mejor con < ~200 caracteres),
números escritos en palabras, y metadatos para pantalla (título, dato, fuente).
"""

TITULO = "10 cosas que hacías hace 40.000 años (y sigues haciendo)"
ARCHIVO = "10_cosas_hace_40000_anos"        # nombre base de los archivos de salida
ESTILO_VISUAL = "doodle_psicodelico"      # ver nucleo/estilos.py
DURACION = 180.0                          # segundos exactos; None = duración natural
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
# una transición por cada cambio de escena: (tipo, duración en s) — ver efectos.TRANSICIONES
TRANSICIONES = [
    ("garabato", 1.0), ("mancha", 0.8), ("espiral", 0.85), ("glitch", 0.7), ("zoom", 0.9),
    ("persianas", 0.8), ("derretir", 1.0), ("ola", 0.85), ("burbujas", 0.9), ("iris", 1.0),
    ("caleido", 0.95),
]
# música por escena: bombo (patrón), modo, raíz MIDI y sabor (ver musica.PROG / config.SABORES)
MUSICA = {
    "intro":     dict(bombo="4x4", modo="dorico", raiz=45, sabor="build"),
    "manos":     dict(bombo="4x4", modo="dorico", raiz=45, sabor="acid"),
    "comida":    dict(bombo="break", modo="mixolidio", raiz=43, sabor="funk"),
    "musica":    dict(bombo="4x4", modo="frigio", raiz=45, sabor="flauta"),
    "heroes":    dict(bombo="medio", modo="menor", raiz=40, sabor="epico"),
    "joyas":     dict(bombo="4x4", modo="lidio", raiz=41, sabor="brillo"),
    "moda":      dict(bombo="4x4", modo="dorico", raiz=43, sabor="disco"),
    "cuenta":    dict(bombo="4x4", modo="menor", raiz=45, sabor="reloj"),
    "pesca":     dict(bombo="break", modo="mixolidio", raiz=40, sabor="dub"),
    "ligar":     dict(bombo="latido", modo="dorico", raiz=41, sabor="lounge"),
    "despedida": dict(bombo="nada", modo="menor", raiz=40, sabor="ambiente"),
    "outro":     dict(bombo="4x4", modo="dorico", raiz=45, sabor="final"),
}

ESCENAS = [
    {
        "id": "intro",
        "frases": [
            "Hace cuarenta mil años no había internet, ni ciudades, ni agricultura.",
            "Pero ya había cerebros como el tuyo, haciendo casi lo mismo que tú.",
            "Estas son diez cosas que hacían los humanos de la Edad de Hielo, y que tú sigues repitiendo.",
        ],
    },
    {
        "id": "manos", "num": 1, "titulo": "DEJAR TU HUELLA",
        "antes": "manos en la roca", "ahora": "selfies",
        "dato": "Sulawesi (Indonesia) y El Castillo (España): ~40.000 años",
        "fuente": "Aubert et al. 2014, Nature · Pike et al. 2012, Science",
        "frases": [
            "Número uno: dejar tu huella.",
            "En cuevas de Indonesia y de España, alguien apoyaba la mano en la roca y soplaba pintura encima.",
            "Hoy lo llamamos selfie. El mensaje es el mismo: yo estuve aquí.",
        ],
    },
    {
        "id": "comida", "num": 2, "titulo": "PRESUMIR LA COMIDA",
        "antes": "pintar cerdos", "ahora": "foto del plato",
        "dato": "Cerdo de Leang Tedongnge, Sulawesi: +45.500 años",
        "fuente": "Brumm et al. 2021, Science Advances",
        "frases": [
            "Número dos: presumir la comida.",
            "Las pinturas de animales más antiguas que conocemos, en la isla de Sulawesi, son de cerdos salvajes.",
            "Cuarenta y cinco mil años después, seguimos fotografiando lo que vamos a comer.",
        ],
    },
    {
        "id": "musica", "num": 3, "titulo": "PONER MÚSICA",
        "antes": "flauta de hueso", "ahora": "playlist",
        "dato": "Flautas de Geissenklösterle (Alemania): 42.000 años",
        "fuente": "Higham et al. 2012, J. Human Evolution",
        "frases": [
            "Número tres: poner música.",
            "En cuevas de Alemania aparecieron flautas de hueso de ave y de marfil de mamut, de más de cuarenta mil años.",
            "Antes de inventar la agricultura, ya teníamos playlist.",
        ],
    },
    {
        "id": "heroes", "num": 4, "titulo": "INVENTAR SUPERHÉROES",
        "antes": "Hombre León", "ahora": "Hombre Araña",
        "dato": "Löwenmensch de Hohlenstein-Stadel: ~40.000 años",
        "fuente": "Museo de Ulm · Kind et al. 2014",
        "frases": [
            "Número cuatro: inventar superhéroes.",
            "El Hombre León es una figura de marfil de unos cuarenta mil años, con cuerpo humano y cabeza de león.",
            "Es una de las pruebas más antiguas de imaginación. El Hombre Araña es su tataranieto.",
        ],
    },
    {
        "id": "joyas", "num": 5, "titulo": "PONERSE JOYAS",
        "antes": "collar de conchas", "ahora": "accesorios",
        "dato": "Cuentas de cáscara de avestruz, conchas y dientes",
        "fuente": "Miller & Wang 2022, Nature",
        "frases": [
            "Número cinco: ponerse joyas.",
            "Collares de cáscara de huevo de avestruz, conchas y dientes perforados. Nadie los necesitaba para sobrevivir.",
            "Probablemente decían quién eras y a qué grupo pertenecías. Igual que tus accesorios.",
        ],
    },
    {
        "id": "moda", "num": 6, "titulo": "SEGUIR LA MODA",
        "antes": "aguja de hueso", "ahora": "ropa con estilo",
        "dato": "Primeras agujas con ojo, Siberia: ~40.000 años",
        "fuente": "Gilligan et al. 2024, Science Advances",
        "frases": [
            "Número seis: seguir la moda.",
            "Las primeras agujas con ojo aparecen en Siberia hace unos cuarenta mil años.",
            "Y los arqueólogos creen que no solo eran para abrigarse, sino para decorar la ropa y lucirla.",
        ],
    },
    {
        "id": "cuenta", "num": 7, "titulo": "LLEVAR LA CUENTA",
        "antes": "29 muescas", "ahora": "una app",
        "dato": "Hueso de Lebombo (sur de África): ~43.000 años",
        "fuente": "d'Errico et al. 2012, PNAS",
        "frases": [
            "Número siete: llevar la cuenta.",
            "El hueso de Lebombo, en el sur de África, tiene veintinueve muescas talladas a propósito, y más de cuarenta mil años.",
            "No sabemos qué contaba. Tú haces lo mismo, pero con una app.",
        ],
    },
    {
        "id": "pesca", "num": 8, "titulo": "COMER PESCADO DE ALTA MAR",
        "antes": "atún en Timor", "ahora": "sushi",
        "dato": "Jerimalai, Timor Oriental: atunes de ~42.000 años",
        "fuente": "O'Connor et al. 2011, Science",
        "frases": [
            "Número ocho: comer pescado de alta mar.",
            "En Timor, hace unos cuarenta y dos mil años, ya se pescaban atunes.",
            "Eso implica salir al mar abierto, con técnica y planificación. Tu antojo de sushi viene de lejos.",
        ],
    },
    {
        "id": "ligar", "num": 9, "titulo": "LIGAR CON DESCONOCIDOS",
        "antes": "neandertales", "ahora": "apps de citas",
        "dato": "Mezcla con neandertales: hace ~47.000 años",
        "fuente": "Sümer et al. 2024, Nature · Iasi et al. 2024, Science",
        "frases": [
            "Número nueve: ligar con desconocidos.",
            "Hace unos cuarenta y siete mil años, nuestros ancestros tuvieron hijos con los neandertales.",
            "Por eso, casi todas las personas con ancestros fuera de África llevan entre uno y dos por ciento de herencia genética neandertal.",
        ],
    },
    {
        "id": "despedida", "num": 10, "titulo": "DESPEDIR A QUIENES AMAMOS",
        "antes": "ocre rojo", "ahora": "flores",
        "dato": "Lago Mungo, Australia: cremación de ~40.000 años",
        "fuente": "Bowler et al. 2003, Nature",
        "frases": [
            "Número diez: despedir a quienes amamos.",
            "En el lago Mungo, en Australia, una mujer fue cremada hace unos cuarenta mil años. Es la cremación más antigua conocida.",
            "Cerca, un hombre fue enterrado cubierto de ocre rojo. Honrar a los muertos es profundamente humano.",
        ],
    },
    {
        "id": "outro",
        "frases": [
            "Cuarenta mil años después, cambiamos las cuevas por pantallas.",
            "Pero el cerebro es prácticamente el mismo: mismo hardware, aplicaciones nuevas.",
            "Así que la próxima vez que te tomes una selfie, recuerda: sigues siendo un humano de las cavernas. Solo que con wifi.",
        ],
    },
]


def todas_las_frases():
    """[(escena_id, idx, texto)] en orden."""
    out = []
    for e in ESCENAS:
        for i, f in enumerate(e["frases"]):
            out.append((e["id"], i, f))
    return out


if __name__ == "__main__":
    fr = todas_las_frases()
    palabras = sum(len(t.split()) for _, _, t in fr)
    print(len(fr), "frases,", palabras, "palabras,", max(len(t) for _, _, t in fr), "caracteres max")
