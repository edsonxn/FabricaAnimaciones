# -*- coding: utf-8 -*-
"""El caso de la Víbora Roja: Oberyn Martell vs. Gregor Clegane (investigación noir, ~3 min, 16:9).
Estilo `noir` (nucleo/noir*.py; basen.py): cine negro en tinta y aguada, SOLO B/N;
el detective narra el caso como una investigación criminal.
Voz ElevenLabs «Edoardo» (YqZLNYWZm98oKaaLZkUA) con eleven_v4 y CORCHETES de actuación.
Sin subtítulos quemados.
GAP = 0.55 para el dramatismo.

MEDIOS REALES:
  - Fichas de retrato en tinta (R.retrato_noir):
      * Pedro Pascal como Oberyn Martell ("OBERYN MARTELL · La Víbora Roja")
      * Hafþór Júlíus Björnsson como Gregor Clegane ("GREGOR CLEGANE · La Montaña que Cabalga")
      * Charles Dance como Tywin Lannister ("TYWIN LANNISTER · Mano del Rey")
      * Peter Dinklage como Tyrion Lannister ("TYRION LANNISTER · El Acusado")
  - Video real entintado (N.clip_noir / R.clip_real):
      * Fragmentos transformados a tinta de alta fricción (≤ 8 s, crédito en pantalla)
"""

TITULO = "El caso de la Víbora Roja"
ARCHIVO = "caso_oberyn"
ESTILO_VISUAL = "noir"
DURACION = None
BPM = 84
GAP = 0.55
SUBTITULOS = False
CER_MAX_POR_FRASE = {"sospechoso_0": 0.03, "motivo_0": 0.03}
MEZCLA = dict(musica=-22.0, sfx=-24.0, fx=-17)
MUSICA = {
    "gancho": dict(sabor="tension", raiz=38, modo="menor"),
    "testigos": dict(sabor="tension", raiz=38, modo="frigio"),
    "sospechoso": dict(sabor="tension", raiz=36, modo="menor"),
    "motivo": dict(sabor="vacio", raiz=38, modo="frigio"),
    "pruebas": dict(sabor="tension", raiz=40, modo="frigio"),
    "desenlace": dict(sabor="tension", raiz=36, modo="menor"),
    "caso_abierto": dict(sabor="vacio", raiz=38, modo="menor"),
}
VOZ = dict(motor="elevenlabs", voice_id="YqZLNYWZm98oKaaLZkUA", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/caso_oberyn/ref_edoardo.mp3",
           tomas=1, stability=0.5)

ESCENAS = [
    {
        "id": "gancho",
        "pre": 1.6,
        "post": 1.1,
        "frases": [
            "[thoughtful] Desembarco del Rey huele a muchas cosas: [short pause] a pescado podrido, a humo de leña y a miedo.",
            "Pero ese verano, el aire trajo un hedor distinto. [short pause] La sangre vieja que nadie se atrevió a limpiar.",
            "[serious] Un príncipe del sur cruzó las puertas de la capital. No venía a rendir pleitesía. Venía a abrir un expediente que llevaba dieciséis años congelado.",
        ],
    },
    {
        "id": "testigos",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[curious] El escenario no podía ser más sucio. Un juicio por combate. El enano de la casa dorada, acusado de matar al rey.",
            "Nadie quería poner el cuerpo por él. Todos sabían que la sentencia ya estaba escrita antes de empezar.",
            "[whispers] Hasta que la Víbora Roja dio un paso al frente. [short pause] No para salvar a un inocente. Sino para elegir a su propio verdugo.",
        ],
    },
    {
        "id": "sospechoso",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] El sospechoso oficial tenía nombre propio: Ser Gregor Clegane. La Montaña que Cabalga.",
            "Ciento ochenta kilos de músculo y acero. Un animal entrenado para quebrar hombres por la mitad.",
            "[thoughtful] Pero en mi oficio aprendes a mirar más allá del arma. [short pause] La bestia solo empujaba la espada; la mano que firmó la orden vestía seda y miraba desde el palco: Tywin Lannister.",
        ],
    },
    {
        "id": "motivo",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[sad] El móvil del crimen era una deuda sin pagar. Elia Martell.",
            "La hermana violada, sus hijos degollados en el saqueo de la ciudad. El cadáver cubierto por una capa carmesí para tapar la vergüenza.",
            "[serious] Durante casi dos décadas, los señores del reino fingieron que fue un accidente de guerra. [short pause] Oberyn guardó el rencor en silencio, esperando el tribunal perfecto.",
        ],
    },
    {
        "id": "pruebas",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[curious] La mañana del duelo, el dorniense no eligió una espada pesada. Eligió una lanza de fresno.",
            "Ligera. Rápida. Y con un detalle que no figuraba en las actas oficiales: [short pause] la punta untada en veneno de mantícora.",
            "[thoughtful] No iba a ser un combate entre caballeros. Iba a ser una disección quirúrgica para arrancarle una confesión al gigante ante toda la corte.",
        ],
    },
    {
        "id": "desenlace",
        "pre": 0.7,
        "post": 1.1,
        "frases": [
            "[serious] Y la trampa funcionó. [short pause] El coloso cayó de rodillas, con las tripas abiertas y el veneno quemándole las venas.",
            "Bastaba un paso atrás. Dejarlo morir en el polvo y cobrar la victoria.",
            "[sighs] Pero el detective de la venganza cometió el error fatal de todos los obsesionados: [short pause] necesitó que el monstruo admitiera la culpa en voz alta.",
            "[whispers] Un tropiezo. Una mano de hierro alrededor del cuello. Y dos pulgares que apagaron la luz para siempre.",
        ],
    },
    {
        "id": "caso_abierto",
        "pre": 0.7,
        "post": 1.2,
        "frases": [
            "[thoughtful] La justicia en este mundo es una palabra que se inventaron los débiles para poder dormir tranquilos.",
            "La Montaña murió semanas después, pudriéndose en los sótanos entre aullidos que despertaron al castillo.",
            "[sighs] Pero para entonces, la Víbora ya era ceniza bajo tierra. [short pause] Caso cerrado. Y en Desembarco del Rey, como siempre... nadie ganó.",
        ],
    },
]
