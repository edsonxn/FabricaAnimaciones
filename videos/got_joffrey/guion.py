# -*- coding: utf-8 -*-
"""¿Quién envenenó al rey? La Boda Púrpura de Game of Thrones contada como pesquisa (noir feudal, ~3 min, 16:9). Sin canal (prueba).
Estilo `noir_feudal` (docs/estilo_noir_color.md § Variante FEUDAL; kit nucleo/noir_color.py + noir_feudal.py + noir_corte.py):
cine negro en tinta y aguada con color oscuro y apagado (antorcha/vela contra luna, UN acento: el morado del veneno).
El pesquisidor encapuchado narra el caso. Voz ElevenLabs «David» con eleven_v4 y CORCHETES de actuación. Sin subtítulos quemados.

Hechos (libro «Tormenta de espadas» y serie T4E2 «El león y la rosa»; confesión en T7E3):
  - Joffrey Baratheon muere en el banquete de su boda con Margaery Tyrell en Desembarco del Rey («la Boda Púrpura»).
  - Banquete de 77 platos (libro); Joffrey parte con la espada una empanada gigante y salen palomas vivas.
  - Joffrey humilla a Tyrion y lo obliga a ser su copero; bebe del gran cáliz de boda, tose, se ahoga, la cara se le pone morada;
    Tyrion recoge el cáliz y Cersei lo acusa.
  - Veneno: «el Estrangulador», cristales morados de las tierras del mar de Jade/Asshai; se disuelven en el vino y cierran la garganta.
  - El cristal iba escondido en la joya de Sansa (collar en la serie, redecilla en el libro), regalo de Ser Dontos; Olenna Tyrell se
    la acomoda durante la boda y toma una piedra. Lo planeó con Petyr Baelish (Meñique).
  - Dontos saca a Sansa durante el caos hasta un barco en la niebla; Meñique lo hace matar con ballesta.
  - Motivo de Olenna: proteger a su nieta del rey cruel. En T7 Olenna, tras beber el veneno que le da Jaime, confiesa: que Cersei
    sepa que fue ella.
Pronunciación (voz) → pantalla/.srt: «Yófrey» → Joffrey, «Tirion» → Tyrion, «Sérsei» → Cersei, «Olena» → Olenna.
Sin logos, escudos ni personajes con el aspecto de los actores de HBO: todo dibujado, emblemas propios.
"""

TITULO = "¿Quién envenenó al rey? La Boda Púrpura"
ARCHIVO = "got_joffrey"
ESTILO_VISUAL = "noir_feudal"
DURACION = None
BPM = 84
SUBTITULOS = False
MEZCLA = dict(musica=-21.0, sfx=-24.0, fx=-17)
VOZ = dict(motor="elevenlabs", voice_id="0hh7H4ZVAtaGpm1VZyEN", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/got_joffrey/ref_david.mp3",
           tomas=1, stability=0.5)

ESCENAS = [
    {
        "id": "gancho",
        "pre": 1.6,
        "post": 0.9,
        "frases": [
            "[thoughtful] He visto morir a muchos hombres. [short pause] Nunca a un rey, en su propia boda, delante de mil invitados.",
            "[serious] Todos lo vieron caer. [short pause] Nadie vio quién lo mató.",
            "Lo llamaron la Boda Púrpura. [short pause] Yo lo llamo por su nombre: envenenamiento.",
        ],
    },
    {
        "id": "victima",
        "pre": 0.6,
        "post": 0.9,
        "frases": [
            "[serious] La víctima: Yófrey, rey de los Siete Reinos. Un muchacho con una corona demasiado grande para su crueldad.",
            "[sighs] Con tantos enemigos, [short pause] la lista de sospechosos era medio reino.",
        ],
    },
    {
        "id": "banquete",
        "pre": 0.6,
        "post": 0.9,
        "frases": [
            "[thoughtful] El banquete duró horas. Setenta y siete platos, músicos y vino del sur.",
            "El rey partió con su espada una empanada gigante. [short pause] De dentro salieron volando palomas vivas.",
            "Y para humillar a su tío Tirion, el enano, lo obligó a servirle la copa.",
        ],
    },
    {
        "id": "muerte",
        "pre": 0.6,
        "post": 0.9,
        "frases": [
            "[serious] Bebió de su gran cáliz de oro. Tosió. [short pause] Y ya no pudo tragar.",
            "[whispers] Se llevó las manos al cuello. La cara se le puso morada.",
            "Su madre, la reina Sérsei, señaló al hombre que sostenía la copa: [short pause] Tirion.",
        ],
    },
    {
        "id": "acusado",
        "pre": 0.6,
        "post": 0.9,
        "frases": [
            "[curious] El sospechoso perfecto: odiaba al rey, y tenía el arma en la mano.",
            "[thoughtful] Pero en mi oficio se aprende algo. [short pause] Cuando te sirven al culpable en bandeja de oro, desconfía de quien puso la bandeja.",
        ],
    },
    {
        "id": "veneno",
        "pre": 0.6,
        "post": 0.9,
        "frases": [
            "[serious] El veneno tiene nombre: el Estrangulador. Cristales morados, traídos de más allá del mar.",
            "Se deshacen en el vino sin dejar rastro, y cierran la garganta como un puño.",
            "Un veneno así no se lleva en el bolsillo. [short pause] Se esconde a la vista de todos.",
        ],
    },
    {
        "id": "collar",
        "pre": 0.6,
        "post": 0.9,
        "frases": [
            "[curious] Esa noche, Sansa Stark llevaba un collar de piedras oscuras. Regalo de un caballero borracho, Ser Dontos.",
            "Durante la boda, una anciana se le acercó para acomodárselo.",
            "[whispers] Al terminar la fiesta, al collar le faltaba una piedra.",
        ],
    },
    {
        "id": "culpables",
        "pre": 0.6,
        "post": 0.9,
        "frases": [
            "[serious] La anciana era Olena Tyrell, la Reina de las Espinas. Su nieta acababa de casarse con el monstruo.",
            "Su socio en la sombra: Meñique, el hombre que sabía cobrar todas las deudas.",
            "En el caos, Dontos llevó a Sansa hasta un barco en la niebla. [short pause] Meñique le pagó con una saeta en el pecho.",
        ],
    },
    {
        "id": "cierre",
        "pre": 0.6,
        "post": 3.2,
        "frases": [
            "[thoughtful] Años después, la anciana lo confesó, con su propia copa de veneno en la mano.",
            "[serious] Quería que la reina lo supiera. [short pause] Que había sido ella.",
            "[whispers] En la corte, el veneno no va en la copa. [short pause] Va en la mano amable que te acomoda el collar.",
            "[sighs] Caso cerrado.",
        ],
    },
]

TRANSICIONES = [("continua", 0.1)] * (len(ESCENAS) - 1)
MUSICA = {k["id"]: dict(sabor="tension", raiz=38) for k in ESCENAS}   # respaldo procedural (va Lyria)
GAP = 0.5
# nombres de fantasía que Whisper escribe distinto (Yófrey/Joffrey, Tirion/Tyrion, Sérsei/Cersei, Olena/Olenna, Dontos)
CER_MAX_POR_FRASE = {"victima_0": 0.06, "banquete_2": 0.05, "muerte_2": 0.06, "collar_0": 0.06, "culpables_0": 0.06,
                     "culpables_2": 0.04}
