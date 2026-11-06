# -*- coding: utf-8 -*-
"""Runa Caída — «Las 5 peores atrocidades de Morgott QUE IGNORASTE» (5-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + imágenes a pantalla + MG de mg_er; docs/estilo_secuencia_yt.md)
con voz Chatterbox «Faraon». Sin patrocinio. Fórmula: canales/formula/runa_caida.md (formato largo; el usuario pidió AL MENOS
20 min el 5-nov-2026). Tema pedido en los comentarios (@ConkerLord22, 28-oct y 5-nov) y prometido en el video de Radahn.
Cada puesto va partido en dos escenas (pN / pNb), como Miquella, Malenia, Melina y Radahn.
Investigación: investigacion.md (wikitexto de eldenring.fandom.com en inglés, japonés y español, 5-nov-2026).
Nombres de la wiki es: Morgott, rey de los Augurios · Margit, el Augurio Caído · Subsuelo de los marginados · asesinos de augurios.
NO REPITE lo de Márika (el exilio de los gemelos) ni lo de Melina (invocarla contra él, quemar el Árbol): aquí desde el lado de Morgott.
TEORÍA / sin texto, dicho como pregunta: que permitiera a los asesinos de augurios. EVITAR: que hizo su propio grillete (FALSO), que
es el jefe que más mata (son INTENTOS, 2.º tras Malenia), que encerró a Mohg, Godwyn/Cuchillos Negros, que se cortó los cuernos,
que se vuelve anciano, que poseyó a un plebeyo (sin comprobar), Shanehaight (contenido cortado).
"""

TITULO = "Las 5 peores atrocidades de Morgott QUE IGNORASTE"
ARCHIVO = "er_morgott_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
VOZ = dict(referencia="C:/chatterbox_voices/Faraon.mp3", idioma="es",
           exaggeration=0.55, cfg_weight=0.3, temperature=0.75)

# Lo que lee Chatterbox (solo sabe español); el guion conserva la grafía del juego para .srt, apoyos y YouTube.
# Radahn (28-oct): «Mikuéla» SUENA «Micuela» (la burla) → «Mikéla»; Mohg «Móg» y siempre ANTE VOCAL (ante consonante = «mock»).
FONETICA = {
    "Miquella": "Mikéla", "Malenia": "Malénia", "Radahn": "Rádan", "Radagon": "Rádagon", "Godfrey": "Gódfri",
    "Mohg": "Móg", "Morgott": "Mórgot", "Margit": "Márguit", "Leyndell": "Léindel", "Rennala": "Renála",
    "Ranni": "Ráni", "Godrick": "Gódrik", "Godwyn": "Gódwin", "Rykard": "Ráikard", "Gideon": "Guídeon", "Enia": "Énia",
    "Kenneth Haight": "Kénet Jéit", "Elden Ring": "Élden Ring", "Elden": "Élden", "Altus": "Áltus", "Melina": "Melína",
    "Blaidd": "Bleid", "Bandai Namco": "Bandái Námco", "Conker": "Cónker", "Antithesis": "Antítesis", "Hunter": "Jánter",
}

# Umbrales de seleccionar = mejor toma de cada frase (5-nov-2026): falsas alarmas revisadas con _revisar_voz.py (Morgoth,
# Mog, Miquela, sin luz, cifras en número, colas). Real solo p1b_5 («Dradan, Drani»): reescrita.
CER_MAX_POR_FRASE = {'intro_0': 0.028, 'intro_2': 0.008, 'p5_1': 0.002, 'p5_2': 0.002, 'p5_3': 0.009, 'p5_4': 0.002, 'p5_5': 0.002, 'p5_7': 0.002, 'p5_8': 0.002, 'p5_9': 0.002, 'p5b_1': 0.002, 'p5b_3': 0.008, 'p5b_4': 0.017, 'p5b_5': 0.016, 'p5b_6': 0.002, 'p4_1': 0.009, 'p4_3': 0.002, 'p4_5': 0.002, 'p4_6': 0.017, 'p4_7': 0.002, 'p4b_0': 0.002, 'p4b_1': 0.008, 'p4b_2': 0.002, 'p4b_3': 0.002, 'p4b_4': 0.002, 'p4b_5': 0.002, 'p4b_6': 0.037, 'p4b_7': 0.008, 'p3_1': 0.002, 'p3_2': 0.01, 'p3_3': 0.002, 'p3_5': 0.002, 'p3_6': 0.014, 'p3_7': 0.002, 'p3b_0': 0.009, 'p3b_2': 0.009, 'p3b_3': 0.002, 'p3b_5': 0.002, 'p3b_6': 0.009, 'p3b_8': 0.017, 'p3b_10': 0.007, 'p2_2': 0.033, 'p2_4': 0.002, 'p2_5': 0.008, 'p2_6': 0.009, 'p2_7': 0.002, 'p2b_1': 0.002, 'p2b_3': 0.002, 'p2b_4': 0.007, 'p2b_5': 0.002, 'p2b_7': 0.002, 'p1_1': 0.002, 'p1_2': 0.002, 'p1_3': 0.002, 'p1_4': 0.002, 'p1_5': 0.008, 'p1_6': 0.015, 'p1_7': 0.002, 'p1_8': 0.002, 'p1b_0': 0.002, 'p1b_1': 0.002, 'p1b_2': 0.002, 'p1b_4': 0.009, 'p1b_6': 0.007, 'p1b_7': 0.002, 'p1b_8': 0.024, 'cierre_0': 0.002, 'cierre_1': 0.002, 'cierre_2': 0.002, 'cierre_4': 0.019, 'cierre_5': 0.016, 'cierre_6': 0.012, 'cierre_7': 0.015}
GAP_MAX_POR_FRASE = {'p1b_5': 0.67, 'intro_0': 0.44, 'intro_2': 0.28, 'p5_1': 0.32, 'p5_2': 0.51, 'p5_3': 0.43, 'p5_4': 0.51, 'p5_5': 0.7, 'p5_7': 0.57, 'p5_8': 0.65, 'p5_9': 0.5, 'p5b_1': 0.47, 'p5b_3': 0.57, 'p5b_4': 0.7, 'p5b_5': 0.56, 'p5b_6': 0.5, 'p4_1': 0.54, 'p4_3': 0.63, 'p4_5': 0.69, 'p4_6': 0.61, 'p4_7': 0.87, 'p4b_0': 0.46, 'p4b_1': 0.41, 'p4b_2': 0.76, 'p4b_3': 0.44, 'p4b_4': 0.27, 'p4b_5': 0.81, 'p4b_6': 0.49, 'p4b_7': 0.63, 'p3_1': 0.39, 'p3_2': 0.48, 'p3_3': 0.52, 'p3_5': 0.68, 'p3_6': 0.61, 'p3_7': 0.69, 'p3b_0': 0.6, 'p3b_2': 0.78, 'p3b_3': 0.63, 'p3b_5': 0.8, 'p3b_6': 0.6, 'p3b_8': 0.36, 'p3b_10': 0.38, 'p2_2': 0.64, 'p2_4': 0.75, 'p2_5': 0.76, 'p2_6': 0.69, 'p2_7': 0.51, 'p2b_1': 0.61, 'p2b_3': 0.69, 'p2b_4': 1.02, 'p2b_5': 0.85, 'p2b_7': 0.45, 'p1_1': 0.67, 'p1_2': 0.67, 'p1_3': 0.6, 'p1_4': 0.91, 'p1_5': 0.51, 'p1_6': 0.7, 'p1_7': 0.99, 'p1_8': 0.79, 'p1b_0': 0.71, 'p1b_1': 0.61, 'p1b_2': 0.91, 'p1b_4': 0.69, 'p1b_6': 0.67, 'p1b_7': 0.76, 'p1b_8': 0.67, 'cierre_0': 0.69, 'cierre_1': 0.62, 'cierre_2': 0.6, 'cierre_4': 0.54, 'cierre_5': 0.6, 'cierre_6': 0.72, 'cierre_7': 0.52}
TAIL_MAX_POR_FRASE = {'p1b_5': 0.53, 'intro_0': 0.48, 'intro_2': 0.43, 'p5_1': 0.61, 'p5_2': 0.67, 'p5_3': 0.56, 'p5_4': 0.42, 'p5_5': 0.34, 'p5_7': 0.37, 'p5_8': 0.46, 'p5_9': 0.44, 'p5b_1': 0.56, 'p5b_3': 0.63, 'p5b_4': 0.45, 'p5b_5': 0.53, 'p5b_6': 0.37, 'p4_1': 0.53, 'p4_3': 0.49, 'p4_5': 0.66, 'p4_6': 0.51, 'p4_7': 0.41, 'p4b_0': 0.53, 'p4b_1': 0.41, 'p4b_2': 0.56, 'p4b_3': 0.59, 'p4b_4': 0.42, 'p4b_5': 0.4, 'p4b_6': 0.42, 'p4b_7': 0.68, 'p3_1': 0.54, 'p3_2': 0.38, 'p3_3': 0.37, 'p3_5': 0.56, 'p3_6': 0.53, 'p3_7': 0.47, 'p3b_0': 0.45, 'p3b_2': 0.69, 'p3b_3': 0.78, 'p3b_5': 0.46, 'p3b_6': 0.52, 'p3b_8': 0.37, 'p3b_10': 0.73, 'p2_2': 0.63, 'p2_4': 0.4, 'p2_5': 0.41, 'p2_6': 0.29, 'p2_7': 0.39, 'p2b_1': 0.48, 'p2b_3': 0.63, 'p2b_4': 0.47, 'p2b_5': 0.51, 'p2b_7': 0.58, 'p1_1': 0.59, 'p1_2': 0.41, 'p1_3': 0.42, 'p1_4': 0.37, 'p1_5': 0.66, 'p1_6': 0.49, 'p1_7': 0.58, 'p1_8': 0.85, 'p1b_0': 0.37, 'p1b_1': 0.62, 'p1b_2': 0.48, 'p1b_4': 0.43, 'p1b_6': 0.52, 'p1b_7': 0.64, 'p1b_8': 0.02, 'cierre_0': 0.55, 'cierre_1': 0.39, 'cierre_2': 0.49, 'cierre_4': 0.66, 'cierre_5': 0.41, 'cierre_6': 0.21, 'cierre_7': 0.59}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,          # todo el video es gameplay
    clip_s=8.6,             # ~8,6 s por clip (ritmo heredado de Warcraft/Tamriel)
    transicion="slideleft", # el clip nuevo empuja al anterior
    fundido=0.35,
    ambiente=0.0,           # por defecto solo imagen; el audio del juego va donde conviene oírlo (regla del 26-oct-2026)
    ambiente_por={},
    recorte_por={},
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=240, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar"]),   # heredado de Radahn
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "frases": [
        "En el video de Radahn, Conker Lord nos dejó dos comentarios. En el primero pedía a Radahn y a Morgott, porque son sus favoritos. Y en el segundo, hace nada: estoy ansioso por el de Morgott. Así, sin más.",
        "Le dijimos que estaba en la lista. Pues aquí lo tienes, Conker. Ojalá siga siendo tu favorito cuando terminemos.",
        "Morgott es, probablemente, el jefe más trágico de Elden Ring. Un príncipe nacido con cuernos, escondido bajo la capital, que aun así decidió proteger el Árbol Áureo cuando todos sus hermanos se fueron a pelear por su cuenta.",
        "Su propio recuerdo lo dice: no amó porque lo amaran. Simplemente amó. Y media comunidad se pone triste cada vez que lo ve caer de rodillas en el Trono de Elden.",
        "Además, es el primer muro de casi todos los jugadores. Antes de saber su nombre, ya lo conoces. Es el viejo enorme del bastón que te espera en la puerta del primer castillo.",
        "Pero si juntas lo que dicen de él las armaduras, los monumentos, los muñecos del subsuelo y sus propias palabras, el guardián leal empieza a parecerse a otra cosa.",
        "Así que van las cinco peores atrocidades de Morgott que ignoraste. Y aviso: la número uno no es contra ti. Es contra los suyos.",
        "Ponte cómodo. Y la próxima vez que le compres un grillete a Parches, fíjate bien de quién era esa cadena.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. Te caza desde el primer día.",
        "Acabas de salir de la cueva del principio. No sabes ni dónde está el norte. Subes por la Colina Tormentosa, cruzas la Puerta Tormentosa camino del Castillo de Velo Tormentoso, y en medio del paso aparece él.",
        "Repugnante Sinluz. Tú que andas tras el Círculo de Elden. Envalentonado por las llamas de la ambición. Alguien debe extinguir tu llama. ¡Y ese será Margit, el Caído!",
        "Fíjate en lo que dice. No te para porque estés invadiendo su castillo. El castillo ni siquiera es suyo, es de Godrick. Te para por querer ser señor. Por tener ambición. Ese es tu delito.",
        "Y no es un guardia cualquiera. Según los datos que publicó Bandai Namco por el primer aniversario del juego, Margit fue el segundo jefe con más intentos de todo Elden Ring. Solo Malenia le ganaba.",
        "Si te mata, te deja un consejo: más te vale olvidar esa absurda ambición. Y si le ganas, no muere. Se deshace en luz dorada, y antes de irse te promete algo.",
        "Te recordaré, Sinluz. Ardiendo con tu miserable llama. Teme a la noche. Las manos del Augurio Caído no tendrán piedad contigo.",
        "Teme a la noche. Y en Necrolimbo, de noche, hay algo que seguramente ya te ha matado más de una vez: los jinetes negros que patrullan los caminos. La Caballería nocturna.",
        "Su casco lo explica: la Caballería nocturna, que ahora vaga por los caminos oscuros de la noche, antaño la dirigía el Augurio Caído. Y eran la muerte de grandes guerreros, caballeros y campeones.",
        "Y su armadura añade un detalle: negra como la brea, con una fina capa de sangre seca. Hoy vagan solos. Pero el escuadrón que te persigue por las noches desde el primer día lo dirigía Margit.",
    ]},
    {"id": "p5b", "frases": [
        "Y no se conforma con un intento. Cuando por fin llegas a la Meseta de Altus, a las afueras de la capital, vuelve a salirte al paso. Te encontré, Sinluz, te dice. Todavía ardiendo con esa miserable llama de ambición.",
        "Ese Margit ya no es el de la puerta. Tiene el doble de vida y pega mucho más fuerte. Es el señor de una capital saliendo de su ciudad, en persona, para matar a un recién llegado antes de que llame a la puerta.",
        "Y elige muy bien el sitio. Ese encuentro es junto a un monumento con espadas clavadas en el suelo. Guárdate ese monumento, que es la número cuatro.",
        "Ahora, un detalle que casi nadie sabe. Si consigues llegar al trono y matar a Morgott antes que a Margit, el Margit de la puerta ya no aparece. El viejo del paso desaparece del juego. Porque nunca fue un guardia. Era él.",
        "La Capa del Augurio Caído lo confirma: es la capa de pelo raído que llevaba Margit sobre el cuerpo. Y solo te la vende Enia, en la Mesa Redonda, cuando Morgott ya ha muerto.",
        "Y si juegas en japonés, la pista estaba desde el principio. Cuando Margit te mata, y cuando Morgott te mata, dicen exactamente la misma frase: más te vale olvidar tu absurda ambición.",
        "En inglés cambiaron una de las dos, pero las dobla el mismo actor. Así que el primer jefe difícil del juego es, en realidad, el último rey de las Tierras Intermedias, haciendo de portero en la otra punta del mapa.",
        "Piénsalo. Tú acabas de llegar, con tu espada oxidada y tu frasco de lágrimas. Y el rey de Leyndell ya te está esperando en el camino. Para que no llegues nunca.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. Apila los cadáveres de los héroes.",
        "Antes de que tú aparecieras en esta historia, Morgott ya tenía práctica. La introducción del juego lo enseña: un gigante con cuernos en las murallas de la capital, peleando contra Radahn.",
        "Sí, el mismo Radahn del video anterior. El que detenía las estrellas con las manos. Y aun así, la capital siguió en pie.",
        "Ahora vuelve al monumento de las afueras, junto a la gracia del Muro exterior del campo de batalla. Su texto dice esto: la Segunda Defensa de Leyndell. El Augurio Caído apila los cadáveres de los héroes. Pero el Árbol Áureo se mantiene inquebrantable.",
        "No dice que salvó la ciudad. Dice que apiló cadáveres. De héroes. Y lo dice el monumento que levantaron para celebrarlo.",
        "Mira alrededor de ese monumento. Los campamentos abandonados, las catapultas, los estandartes rotos de los que sitiaron la capital. Lo que cruzas camino de Leyndell es el campo de batalla tal como él lo dejó.",
        "Entre esos estandartes hay algunos del Castillo de Velo Tormentoso. Y Kenneth Haight, el noble de Necrolimbo, cuenta que Godrick huyó de la capital escondido entre las mujeres. El juego no dice quién lo echó. Pero ya sabes quién guardaba la puerta.",
        "Y la capa de Margit lo cuenta todavía más claro: tras masacrar a incontables campeones durante la Devastación, el Augurio Caído se ha convertido en el horror de quienes ambicionan el Árbol Áureo o el señorío.",
        "En japonés es aún más fuerte. Dice que es la pesadilla de todos los que desafían al Árbol con ambición de rey. Incontables campeones. Durante toda la guerra.",
    ]},
    {"id": "p4b", "frases": [
        "Ahora piensa en quiénes eran esos campeones. Cuando Márika rompió el Círculo de Elden, sus hijos se repartieron los pedazos. Y todos, de una forma u otra, miraban hacia el Árbol. Hacia el trono.",
        "Morgott no hizo la guerra para conquistar nada. La hizo para que nadie llegara. Ni sus hermanos, ni sus ejércitos, ni los Sinluz que vinieron después. Todo el que se acercaba con ambición acababa en la pila.",
        "Y aquí hay un detalle que da escalofríos. Cuando le ganas la primera fase, Margit casi te felicita: vaya, tienes cierta habilidad. Por tus venas debe correr sangre de guerrero, Sinluz.",
        "En japonés lo dice más claro todavía: así que los Sinluz sí son descendientes de guerreros. ¿Y de qué guerreros? De los que se fueron al exilio cuando perdieron la gracia, siguiendo al primer señor del Círculo. A Godfrey. Su padre.",
        "El monumento de Godfrey lo cuenta: sus ejércitos dorados, invictos y sin doblegarse, y aun así encuentran la gracia perdida, raída y apagada.",
        "O sea, el hijo se pasa la guerra apilando héroes en las murallas. Y cuando la guerra se acaba, se dedica a cazar a los descendientes del ejército de su propio padre.",
        "Antes del número tres, un par de comentarios que nos alegraron la semana. Mister Hunter escribió en el video de Radahn: se agradece que corrigieras la pronunciación de Miquella, se ve que lees los comentarios.",
        "Y Pablo, que en el video de Malenia se quejaba de la voz y de Micuela, volvió para decir: qué bueno, ya no dice Micuela. Pablo, aquí seguimos, puliendo nombre a nombre. Hoy el examen es Morgott, el rey de los augurios.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. El rey de una ciudad que mutila a los suyos.",
        "Para esta hay que bajar. Bajo Leyndell, la ciudad dorada, están las alcantarillas. Y debajo de las alcantarillas, un sitio que no aparece en ningún mapa del juego: el Subsuelo de los marginados.",
        "Ahí abajo viven los augurios. Gente nacida con cuernos, como él. Y hay un objeto que explica lo que les pasa: el Párvulo maldito, un muñequito que suelta uno de ellos.",
        "Su descripción es de las más duras del juego. A los bebés augurio les extirpan todos los cuernos, y la mayoría muere. Estos fetiches se hacen para recordarlos.",
        "Y el muñeco lleva una frase escrita. Por favor, no me odies ni me maldigas. Por favor.",
        "¿Y los que sobreviven? Para eso están los asesinos de augurios. Los de la máscara sonriente y el machete enorme. Fíjate de qué está hecho ese machete: su hoja es una hilera de cuernos de augurio amputados.",
        "Rollo, el asesino de augurios que puedes invocar como ceniza, tiene una descripción sin anestesia: se bebió una medicina para librarse de las emociones, y así poder hacer su trabajo de pesadilla. Cazar augurios.",
        "Y a los augurios que sí mandaban a la guerra les daban un machete con una maldición grabada en la hoja. El arma lo explica con toda la calma: al entregar un arma, hay que prepararse para quitarla.",
    ]},
    {"id": "p3b", "frases": [
        "Todo esto pasa en el reino de Morgott. Y aquí va la pregunta incómoda. Junto a la Iglesia inferior de la capital, dentro de Leyndell, en su propia ciudad, hay un asesino de augurios. Trabajando.",
        "El rey de los augurios gobernaba Leyndell. Gideon lo llama el monarca velado, el señor de Leyndell. Y en su capital, los cazadores de augurios seguían con su oficio.",
        "Ojo: ningún texto dice que Morgott lo ordenara, ni que lo permitiera. Pero tampoco hay uno solo que diga que lo impidió. Era el rey. ¿De verdad no sabía lo que pasaba debajo de su trono?",
        "Porque él sabía muy bien lo que hay ahí abajo. Su recuerdo te da otro muñeco, el Párvulo maldito de la realeza. Y dice: a los bebés augurio nacidos de la realeza no les extirpan los cuernos. Los guardan bajo tierra, sin que nadie lo sepa, encerrados para siempre.",
        "Sin que nadie lo sepa. Ese muñeco va en su recuerdo porque habla de él. Del príncipe con cuernos que su familia escondió en el subsuelo.",
        "Y cuando salió, y llegó a gobernar la capital, el subsuelo siguió igual. Lleno de augurios encerrados, aullando bajo la ciudad dorada. No consta que sacara a uno solo.",
        "Lo único que hizo ahí abajo fue poner un sello. En la Catedral de los Desamparados, detrás de un altar falso, hay un pasaje cerrado con este mensaje: sellado por Morgott, el agraciado.",
        "Detrás está la Llama Frenética, el fuego que lo quema todo. Ese sello sí lo puso. Para proteger el mundo de arriba. A los de abajo los dejó donde estaban.",
        "Por cierto, Barial nos pidió un video de la Llama Frenética, y queda apuntado. Ese sello se rompe en cuanto muere Morgott. Ya sabes por dónde empieza esa historia.",
        "Y Manuel nos dejó esto en el video de Malenia: qué mal que un buen video decaiga tanto por usar la IA.",
        "Gracias por lo de buen video, Manuel. Y sí, la voz es una IA, nunca lo hemos escondido, y la vamos afinando nombre a nombre. Pero si lo que te interesa es algo que decae de verdad, espera al número dos. Hay un árbol que lleva mil años decayendo, y nadie le escribe.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. Mata por un trono que sabe vacío.",
        "Cuando por fin llegas al Trono de Elden, Morgott te recibe con un discurso. Sinluz sin gracia. ¿Qué asunto te trae ante estos tronos?",
        "Y empieza a nombrar a sus hermanos, uno a uno. Godrick el Dorado. Los gemelos prodigio, Miquella y Malenia. El general Radahn. El pretor Rykard. La princesa de la Luna, Ranni. Traidores deliberados, todos ellos.",
        "Fíjate en la lista. Casi todos ya han pasado por este canal. Y en el video de Ranni vimos que, al menos con ella, no le faltaba razón.",
        "Pero falta uno. Su gemelo, Mohg, el que nació con él, con los mismos cuernos y la misma maldición. Nombra a todos los traidores menos a su hermano de sangre. Y el juego nunca explica por qué.",
        "Luego remata: sois todos de la misma calaña. Saqueadores, envalentonados por las llamas de la ambición. Que lo escriban en tu patética tumba: ¡derrotado por el rey Morgott! El último de todos los reyes.",
        "Según la wiki, en la primera versión del juego esa frase terminaba distinto: derrotado por el rey Morgott, ¡Señor del Círculo! Un parche la cambió por el último de todos los reyes.",
        "Y fíjate en cómo te llama: sin gracia. Su propio recuerdo dice que él nació como un augurio sin la gracia. La misma palabra, en inglés y en japonés. Te insulta con lo que él es.",
    ]},
    {"id": "p2b", "frases": [
        "Y ahora, lo peor. Cuando lo vences, cae de rodillas y te dice la verdad que había callado durante toda la guerra.",
        "Sinluz, no eres más que un necio. El Árbol Áureo rechaza a todo el que se le acerca. Estamos... todos estamos abandonados. Nadie puede reclamar el título de Señor del Círculo.",
        "Y si vuelves a hablarle, añade una cosa más: tus hazañas acabarán en fracaso. Igual que yo.",
        "Igual que yo. Él ya lo había intentado, y el Árbol ya lo había rechazado. Lo sabía mientras apilaba héroes en las murallas, mientras sus jinetes cazaban campeones de noche, mientras te esperaba en el paso de Necrolimbo.",
        "Y nada más morir, lo compruebas. La entrada del Árbol Áureo se cierra con un muro de espinas. Enia, en la Mesa Redonda, te lo confirma: el Árbol te ha rechazado. Y tendrán que pasar miles de lunas, si no decenas de miles, antes de que cambie.",
        "Así que piénsalo. Toda la Devastación, todos los campeones de la pila, todos los Sinluz a los que les apagó la llama, murieron por intentar llegar a un trono que él sabía que nadie iba a ocupar. Ni siquiera él.",
        "No defendía el trono de los usurpadores. Defendía una silla vacía. Y la defendía matando.",
        "Antes del número uno, un dato que duele un poco. De cada cien personas que ven este canal, menos de cuatro están suscritas. Estamos a nada de los quinientos, y la meta grande es mil.",
        "Morgott se pasó la vida defendiendo un trono que nunca iba a ser suyo. Tú no tienes que pelear con nadie. Solo pulsar un botón.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. El más leal.",
        "Volvamos al primer encuentro. Si Margit te parece imposible, en la Cueva de Agualóbrega hay un comerciante que te echa una mano. Parches, el estafador de siempre. Por cinco mil runas te vende un objeto: el Grillete de Margit.",
        "Lo usas en la pelea y Margit cae al suelo, inmovilizado, como si una cadena invisible tirara de él hacia abajo. Media comunidad lo descubrió así. Casi nadie leyó la descripción.",
        "Un fetiche bañado en magia dorada. Los grilletes se usaban para atar al pueblo maldito al que llaman augurios. Y estos se hicieron para mantener a un augurio concreto bajo el más estricto encierro.",
        "Aunque débiles, todavía conservan algo de poder. Lo bastante para atrapar en la tierra, aunque sea un momento, a Margit, que una vez estuvo encadenado.",
        "Ese grillete no es un arma contra Margit. Es la cadena con la que lo tuvieron preso. Por eso lo tumba: su cuerpo se acuerda. Y hay otro igual, el Grillete de Mohg, hecho para su gemelo. A los dos los encadenaron.",
        "Ahora fíjate en su espada. La Espada maldita de Morgott, la que esconde como si fuera un bastón. Su descripción dice: la sangre maldita que Morgott repudió y selló se transformó en esta hoja.",
        "Su propia sangre. La sangre de los augurios. La encerró dentro de un arma. Y cuando por fin la desenvaina, en la segunda fase, se le escapa esto: los tronos, manchados por mi maldición. Es una vergüenza que no puedo soportar.",
        "Vergüenza de sí mismo. Su gemelo hizo lo contrario. La Gran Runa de Mohg, en cambio, dice que está empapada en sangre maldita, por el amor devoto que sentía por el fango miserable donde nació. Uno abrazó lo que era. El otro lo encerró en una espada.",
    ]},
    {"id": "p1b", "frases": [
        "Y aquí está la atrocidad de verdad. ¿Quién convirtió a los augurios en una maldición? La Orden Dorada. La de Márika y Radagon, la que ya vimos en sus videos.",
        "Hay un talismán, la Pluma del Crisol, que lo cuenta: los rasgos del Crisol se consideraban en la antigüedad una señal de lo divino. Pero, a medida que avanzaba la civilización, se desprecian cada vez más como una impureza.",
        "Y otro muñeco, el Párvulo cornudo, dice que los cuernos enredados son un símbolo de espiritualidad. Antes, los cuernos eran sagrados. La Orden Dorada los convirtió en una condena.",
        "Esa Orden es la que les corta los cuernos a los bebés. La que encierra a los de la realeza para siempre. La que lo encadenó a él con ese grillete. La que le enseñó a avergonzarse de su propia sangre.",
        "Y Morgott se pasó toda la Devastación defendiéndola. Con el nombre de un monstruo, con una capa de pelo raído, matando a todo el que se acercara. Fue el mejor soldado del sistema que lo odiaba.",
        "Ninguno de sus hermanos la defendió como él. Ni los gemelos prodigio, ni Radahn, ni Ranni: todos se fueron por su lado. El único que se quedó a defender a la familia fue el hijo que la familia escondió en las cloacas.",
        "Su recuerdo lo dice así en la versión oficial en español: pese a haber nacido como un augurio más sin la Gracia, Morgott decidió convertirse en el protector del Árbol Áureo. Jamás recibió ninguna muestra de afecto por ello, pero aun así, él amó.",
        "Y la única muestra de afecto llega cuando ya es tarde. Al final del juego, con la capital hecha ceniza, aparece un guerrero dorado de rodillas junto a un cuerpo que se deshace en oro. Es Godfrey. Y le habla por su nombre.",
        "Ha pasado mucho tiempo, Morgott. Larga y dura fue tu lucha.",
        "Su padre. El que se fue al exilio cuando perdió la gracia. Lo primero bonito que le dice en toda su vida se lo dice a un cadáver. Y luego se levanta, y viene a por ti.",
    ]},
    {"id": "cierre", "frases": [
        "Esa es la lista. El viejo del primer castillo te caza desde el primer día, dirigía a los jinetes que matan campeones de noche, apiló héroes en las murallas, reinó sobre una ciudad que mutila a los suyos, mató durante toda una guerra por un trono que sabía vacío, y defendió hasta la muerte al sistema que lo encadenó.",
        "Y aun así, cuesta odiarlo. Porque de todos los hijos de Márika, fue el único que nunca la traicionó. Y ella nunca se lo agradeció.",
        "Antes de irme, gracias a los que nos escriben. Pachón dijo: qué buen video, y encima le resolvió una duda a otros en los comentarios. Luis nos contó que era el primer video nuestro que veía, y que le pareció buenísimo. Bienvenido, Luis.",
        "Juan Camilo nos pidió: sigue con estos videos, por favor. Y El Imputable lo resumió en tres palabras: esto es oro. Aquí seguimos.",
        "Y Antithesis nos corrigió algo del video de Radahn. Cuando Blaidd dice en inglés que Radahn pelea de una forma sick, no es asco. En inglés, sick también se usa para algo brutal, impresionante. Tiene razón, y gracias por el apunte.",
        "Los comentarios se leen todos, de verdad, y con ellos vamos mejorando el canal. Por eso Cristian ya tiene a Rennala apuntada, y John, a Godfrey y a Godwyn, que tienen mucho que contar.",
        "Ahora te toca a ti. ¿Morgott fue un héroe trágico, o el carcelero más fiel de su madre? Y Conker, espero que siga siendo tu favorito.",
        "Si te quedaste con ganas de más familia, en el canal tienes las atrocidades de Márika y Radagon, de Miquella, de Malenia, de Ranni, de Melina y de Radahn. Y si te suscribes, nos acercas a los quinientos.",
        "Y la próxima vez que le compres un grillete a Parches, acuérdate: antes de servirte a ti, sirvió para encadenar a Morgott, el rey de los augurios.",
    ]},
]
