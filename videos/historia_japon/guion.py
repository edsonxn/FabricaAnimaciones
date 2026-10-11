# -*- coding: utf-8 -*-
"""La historia de Japón en 5 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa que se une, se parte y se une).

Canal Cronopapel, tercer video de la serie «historia en minutos» (mismo motor que `videos/historia_iran/` y `historia_china/`).
Hilo narrativo: un archipiélago que se cierra, se abre y se transforma; el poder real pasa de los emperadores a los shogunes,
pero el emperador nunca desaparece.

Datos y fuentes (Britannica, Cambridge History of Japan, Museo Nacional de Tokio, UNESCO):
  - Periodo Jomon (desde ~14 000 a. C.): una de las cerámicas más antiguas del mundo (~16 000 años). Yayoi (~300 a. C.): arroz irrigado y metal.
  - Kofun (siglos III-VI): tumbas en forma de ojo de cerradura; la del emperador Nintoku (Osaka) mide unos 486 m (UNESCO, 2019).
  - Según la tradición, el primer emperador, Jimmu, funda Japón en 660 a. C. (mito; el linaje documentado es de ~1 500 años). La casa imperial es la
    monarquía hereditaria continua más antigua del mundo.
  - Príncipe Shotoku (~604): Constitución de diecisiete artículos; el budismo llega de Corea (~538/552). Nara capital en 710; Kioto (Heian) en 794.
  - Genji Monogatari (~1010), de Murasaki Shikibu: considerada la primera novela de la historia.
  - Minamoto no Yoritomo: primer shogun (1192), gobierno militar en Kamakura. Invasiones mongolas 1274 y 1281, derrotadas en parte por tifones (kamikaze).
  - Era Sengoku (desde la guerra de Onin, 1467, hasta 1600). Arcabuces portugueses llegan en 1543 (Tanegashima). Nobunaga, Hideyoshi y Ieyasu; Sekigahara (1600);
    Ieyasu shogun en 1603 (Edo); Japón cierra sus puertas en los años 1630 (solo Dejima, holandeses y chinos). ~250 años de paz (periodo Edo, 1603-1868).
  - Comodoro Matthew Perry llega en 1853 («barcos negros»); Tratado de Kanagawa (1854). Restauración Meiji (1868): el emperador Meiji (15 años) recupera el poder;
    en 1872 abre el primer ferrocarril Tokio-Yokohama; 1876 se prohíbe a los samuráis llevar espada. Guerra ruso-japonesa 1904-1905: primera vez que una potencia asiática
    vence a una europea en la era moderna. Corea anexada en 1910.
  - 1931 Manchuria; 1937 guerra con China; 7-dic-1941 Pearl Harbor; 6 y 9-ago-1945 Hiroshima y Nagasaki; rendición 15-ago (anuncio) / 2-sep-1945 (firma).
    Constitución de 1947, artículo 9: renuncia a la guerra. Juegos Olímpicos de Tokio y primer tren bala (Shinkansen), octubre de 1964.
  - Población ~124 millones (2023), una de las más envejecidas del mundo.
"""

TITULO = "La historia de Japón en 5 minutos"
ARCHIVO = "historia_japon_5min"
ESTILO_VISUAL = "boceto"
DURACION = None                  # None = duración natural (~353s); antes 330
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)
ALIAS_QA = {"shotoku": "shotoku", "shotoko": "shotoku", "minamoto": "minamoto", "yoritomo": "yoritomo",
            "nobunaga": "nobunaga", "hideyoshi": "hideyoshi", "ieyasu": "ieyasu", "tokugawa": "tokugawa", "meiji": "meiji",
            "kamakura": "kamakura", "kioto": "kioto", "kyoto": "kioto", "tokyo": "tokio", "shogun": "shogun", "shoguns": "shogunes",
            "sekigahara": "sekigahara", "genji": "genji", "kamikaze": "kamikaze", "edo": "edo", "dejima": "dejima", "perry": "perry",
            "homon": "jomon", "khan": "kan"}
SUBTITULOS = False
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Un archipiélago donde los samuráis gobernaron durante siglos, y donde un emperador jamás perdió su trono.",
        "Cerró sus puertas al mundo, y las abrió de golpe con una revolución.",
        "Esta es la historia de Japón, en cinco minutos.",
    ]},
    {"id": "origenes", "frases": [
        "Todo empieza en islas cubiertas de volcanes y bosques, hace más de dieciséis mil años.",
        "Allí, el pueblo jomon fabrica algunas de las cerámicas más antiguas del mundo.",
        "Hacia trescientos antes de Cristo, llegan el arroz y el metal, y aparecen pueblos de agricultores.",
        "Los jefes más poderosos se entierran en enormes tumbas con forma de ojo de cerradura, más grandes que un estadio.",
        "Según la leyenda, en seiscientos sesenta antes de Cristo, el emperador Jimmu funda Japón, y es descendiente de la diosa del sol.",
    ]},
    {"id": "imperio", "frases": [
        "Con el tiempo, el clan Yamato unifica las islas, y sus jefes se convierten en emperadores.",
        "Desde Corea y China llegan la escritura, el budismo y la forma de gobernar.",
        "En el año seiscientos cuatro, el príncipe Shotoku escribe una constitución de diecisiete artículos.",
        "La capital se traslada a Nara, y después, en el año setecientos noventa y cuatro, a Kioto.",
    ]},
    {"id": "heian", "frases": [
        "Empieza la edad de oro de la corte imperial: poetas, pintores y nobles refinados.",
        "Hacia el año mil, una dama llamada Murasaki Shikibu escribe la historia de un príncipe, el Genji.",
        "Muchos la consideran la primera novela de la historia.",
        "Pero mientras la corte escribe poemas, en las provincias crecen los guerreros.",
    ]},
    {"id": "shogun", "frases": [
        "Son los samuráis, y sus clanes se disputan el poder.",
        "En mil ciento noventa y dos, Minamoto Yoritomo vence, y el emperador le da un título nuevo: shogun, general supremo.",
        "Desde entonces, el shogun manda de verdad, y el emperador reina, pero no gobierna.",
        "Y los samuráis imponen su código: honor, lealtad y disciplina.",
    ]},
    {"id": "mongoles", "frases": [
        "En mil doscientos setenta y cuatro, llega una flota gigante desde China: los mongoles de Kublai Kan.",
        "Los samuráis resisten. Siete años después, regresan con miles de barcos.",
        "Pero una tormenta hunde gran parte de la flota, y los japoneses la llaman kamikaze: el viento divino.",
    ]},
    {"id": "sengoku", "frases": [
        "Sin embargo, el poder del shogun se debilita, y en mil cuatrocientos sesenta y siete, estalla una guerra civil.",
        "Comienza el periodo de los países en guerra. Durante más de cien años, cada señor feudal lucha contra todos.",
        "En mil quinientos cuarenta y tres, unos comerciantes portugueses llegan a una isla y traen armas de fuego.",
        "Los japoneses aprenden a fabricarlas en pocos años.",
        "Y un señor ambicioso, Oda Nobunaga, las usa para aplastar a sus enemigos.",
    ]},
    {"id": "unificacion", "frases": [
        "Nobunaga muere traicionado, y su general, Hideyoshi, un campesino que llegó a lo más alto, continúa su obra.",
        "Hideyoshi unifica casi todo el país. Pero a su muerte, sus rivales vuelven a pelear.",
        "En mil seiscientos, en la batalla de Sekigahara, triunfa Tokugawa Ieyasu.",
        "Tres años después, se convierte en shogun, y funda su capital en una pequeña aldea de pescadores llamada Edo.",
        "Hoy ese lugar se llama Tokio.",
    ]},
    {"id": "edo", "frases": [
        "Los Tokugawa gobiernan durante más de doscientos cincuenta años de paz.",
        "Los samuráis dejan la guerra, y se convierten en funcionarios. Florecen el teatro kabuki, los grabados y los artistas.",
        "Pero temen que los europeos, y sus misioneros, traigan problemas.",
        "Así que Japón cierra sus puertas: expulsa a los extranjeros, y prohíbe salir del país.",
        "Solo unos pocos comerciantes holandeses y chinos pueden entrar, en una pequeña isla artificial.",
    ]},
    {"id": "perry", "frases": [
        "Hasta que, en mil ochocientos cincuenta y tres, aparecen en la bahía cuatro buques de guerra negros, con cañones.",
        "Son los de Estados Unidos, y su comodoro exige abrir el país al comercio.",
        "Los samuráis no pueden competir con los cañones de vapor, y el shogun cede.",
        "Muchos japoneses se indignan. Y una idea se extiende: el shogun ha fallado. El emperador debe volver a gobernar.",
    ]},
    {"id": "meiji", "frases": [
        "En mil ochocientos sesenta y ocho, samuráis rebeldes derrocan al shogun, y colocan en el trono a un emperador de quince años: Meiji.",
        "Y comienza una modernización a una velocidad asombrosa.",
        "Japón estudia a Occidente: trenes, fábricas, escuelas, un ejército moderno y una constitución.",
        "Los samuráis pierden sus privilegios, y se les prohíbe llevar espada.",
        "En solo treinta años, pasa de país aislado a potencia.",
    ]},
    {"id": "imperialismo", "frases": [
        "Y, como las potencias europeas, Japón se lanza a conquistar.",
        "En mil novecientos cinco, derrota a Rusia, algo que ningún país asiático había logrado frente a uno europeo.",
        "Anexa Corea, e invade Manchuria, y en mil novecientos treinta y siete, China.",
        "En mil novecientos cuarenta y uno, ataca la base estadounidense de Pearl Harbor, y entra de lleno en la Segunda Guerra Mundial.",
    ]},
    {"id": "guerra", "frases": [
        "Al principio, conquista medio Pacífico. Pero Estados Unidos contraataca, isla por isla.",
        "Las ciudades japonesas son bombardeadas.",
        "Y en agosto de mil novecientos cuarenta y cinco, dos bombas atómicas destruyen Hiroshima y Nagasaki.",
        "El emperador habla por radio por primera vez, y anuncia la rendición.",
        "Japón queda arrasado, y ocupado por los estadounidenses.",
    ]},
    {"id": "moderna", "frases": [
        "Pero se levanta de nuevo.",
        "En mil novecientos cuarenta y siete, aprueba una constitución que renuncia para siempre a hacer la guerra.",
        "En mil novecientos sesenta y cuatro, organiza los Juegos Olímpicos de Tokio, y estrena el primer tren bala del mundo.",
        "En pocas décadas, se convierte en una de las mayores economías del planeta.",
        "Hoy viven en Japón unos ciento veinticuatro millones de personas, una de las poblaciones más envejecidas del mundo.",
        "Y sus cerezos florecen cada primavera, como hace mil años.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Un país que se aisló, se abrió, cayó y se reinventó, sin perder su identidad.",
        "¿Qué país quieres ver en cinco minutos? Dímelo en los comentarios.",
    ]},
]
TRANSICIONES = [("continua", 0.1)] * len(ESCENAS)


# Música con Lyria (nucleo/lyria.py): estilo japonés moderno y juguetón, con hueco para la voz; un bloque por escena
LYRIA = dict(
    estilo=("Playful yet epic animated-history documentary score blending traditional Japanese instruments (shakuhachi flute, koto, shamisen, "
            "taiko drums) with a light modern pulse, in the feel of a fast-moving illustrated history explainer. Bright, rhythmic, "
            "constantly evolving, with short stingers at scene changes. Melodies kept low so a narrator can speak over it."),
    escenas={
        "gancho": ("Hook: plucked koto motif over a light ticking pulse, curiosity building, a cheeky rise and a bright taiko hit at the end.", 5),
        "origenes": ("Misty volcanic islands at dawn: shakuhachi and soft koto arpeggios, gentle pulse, then a rising tribal taiko.", 5),
        "imperio": ("Court and continent: stately koto and flute, slow dignified pulse, travelers arriving, building to a bright chord.", 5),
        "heian": ("Refined imperial court: elegant koto and gagaku-inspired strings, graceful and calm, a hint of tension underneath.", 5),
        "shogun": ("Warrior rise: low taiko pounding, shamisen riffs, a proud heroic march, a bold final hit.", 5),
        "mongoles": ("Sea storm: dark rumbling drums, urgent strings, a huge crashing climax, then a hush.", 5),
        "sengoku": ("Civil war: fast shamisen and taiko, chaotic galloping energy, a sudden gunshot stinger and a wild rising pulse.", 6),
        "unificacion": ("Unification: heroic climbing melody, bold brass-like strings, a dramatic drop then a triumphant return.", 6),
        "edo": ("Peaceful era: light playful shamisen, kabuki-inspired percussion, then a slow closing-door atmosphere.", 6),
        "perry": ("Giant black ships: ominous deep drums and horns, a tense silence, then a heavy cannon hit.", 5),
        "meiji": ("Rapid modernization: upbeat accelerating rhythm, marching snare mixed with koto, bright and energetic like a montage.", 6),
        "imperialismo": ("Expansion and war: martial drums, rising tension, dissonant strings, dark and ominous.", 5),
        "guerra": ("Destruction: heavy low drums, a deep rumble, a long haunting silence, mournful shakuhachi.", 6),
        "moderna": ("Rebirth: a tender hopeful theme on koto and piano, then a bright modern groove for the Olympics, then soft cherry-blossom bells.", 7),
        "cierre": ("Playful resolving outro: the main koto theme returns brightly, light percussion, friendly and inviting, a final warm chord and fade.", 5),
    },
)
