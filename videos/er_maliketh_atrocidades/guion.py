# -*- coding: utf-8 -*-
"""Runa Caída — «5 atrocidades de Maliketh que el juego te ESCONDIÓ» (27-nov-2026).
Motor SECUENCIA YT (gameplay de Elden Ring por beat + pegatinas + pantallas + MG de mg_er; docs/estilo_secuencia_yt.md).
Elegido por el usuario en el «buenos días» (de Zampaheces y Parches); investigación R45 en canales/formula/runa_caida.md.
Pedido ≤ 10 días por Aylan, Bauti y Piso Papas (tarjetas com_*). ≈ 25 min. Voz «el Profeta» de ElevenLabs, PLANA. Sin
patrocinio. OST oficial (bajar_ost.py). EMPAQUE NUEVO (título sin «QUE IGNORASTE»).
Investigación: _investigacion/dossier.md. Citas textuales = descripciones de objeto en español ([EG]); las líneas de Maliketh,
Gurranq y D solo existen verificadas en inglés → PARAFRASEADAS y se OYEN en inglés (salvo «Oh, Muerte…», [ES-wiki]).
NO decir: «Maliketh robó la Muerte» (errata ES de su espada), «muerte destinada» (es Muerte Escrita), «Noche de los Cuchillos
Negros» (es de los Puñales Negros; las asesinas sí son «de los Cuchillos Negros»), que Márika ordenó el robo (PREGUNTA, nunca
hecho), que mató a la Reina del Ojo Velado (sucumbió/derrota), Nokron, Messmer o el DLC.
Críticas con contraburla: @diegocuesta9289 (intro + p1d), @EdgarFelipe-d9y (p3c). Respuesta: @DarkShooter942 (p4c).
Agradecimientos: Jonatan, xxe0511 (p4c) · Bryan, Alberto, Astora, Lissom (subs).
Sonidos nombrados = tramo audible con `post` (regla 31-oct / regla 10), dossier § 5:
intro S1 «O, Death. Become my blade, once more.» (xaXLX1UOl8A 18,6-23,2) · p1b S9 Gurranq al morir (v-Csk29Jx50 127,3-142,5) ·
p1c S14 diálogo RECORTADO (GczQrVgIUis 41,5-55,3) · cierre S3 «Witless Tarnished…» (xaXLX1UOl8A 33,3-41,2) ·
cierreb S6 «Forgive me, Marika…» (xaXLX1UOl8A 75,9-87,2).
"""

TITULO = "5 atrocidades de Maliketh que el juego te ESCONDIÓ"
ARCHIVO = "er_maliketh_atrocidades"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_yt"
DURACION = None
BPM = 80
# el Profeta (ElevenLabs God - Deep, Powerful). Corchetes SOBRIOS: nada de risas ni alegría (el usuario, 11-nov-2026).
VOZ = dict(motor="elevenlabs", voice_id="HNSF1CTQmub252yhXROX", modelo="eleven_v4_turbo", idioma="es", tomas=1, stability=0.5,
           sin_etiquetas=("whisper", "excit", "laugh", "amused", "chuckl", "cheer", "happy", "mischiev", "giggl", "joy"),
           referencia=r"C:\FabricaAnimaciones\canales\muestras_voz\runa_profeta\B_profeta.mp3")
FONETICA = {"Miquella": "Miquéla", "Messmer": "Mésmer", "Maliketh": "Málikez", "Gurranq": "Gúrank", "Farum Azula": "Fárum Azúla"}

SECUENCIA = dict(
    fuente="yt",
    video_s=99999,
    clip_s=8.6,
    transicion="slideleft",
    fundido=0.35,
    ambiente=0.0,
    ambiente_por={},
    # tráiler de la historia (TRN, K_03kFqWfqs) con franjas negras y subtítulos en ellas: solo 137 (110/112/117 ya no son
    # del tráiler: vhmkUYSyMfE y W4K4iaLfcug, sin franjas, 27-nov). Marca de agua «Khonziel» abajo a la derecha (x ≥ 88 %) en
    # fQjCJnVTrY4 y HaJOgAg90AY (014/021/029/032): se recorta 14 % por la derecha (izq, arriba, der, abajo).
    recorte_por={**{s: .13 for s in ('scene-137',)},
                 **{s: (0.0, 0.0, .14, 0.0) for s in ('scene-014', 'scene-021', 'scene-029', 'scene-032')}},
    yt=dict(sufijo="Elden Ring", min_s=45, max_min=1500, alto=1080,
            evitar_canales=["Fextralife", "Lance McDonald", "IGN", "ConCon", "PowerPyx", "FP Good Game", "Erudur Gaming", "GAMER ZONE",
                            "Horizon Gaming", "Zullie the Witch", "Winter Valis", "Mage Infa", "Nate Sandhart", "Shaded Grin", "cad5150",
                            "Taveris the Red", "Cravotato", "NeoJetty", "VaatiVidya", "Ambient Souls", "Gamerpillar", "Shirrako", "pgp"]),
)

TRANSICIONES = [("continua", 0.1)] * 40
LYRIA = dict(   # sin uso: la música es la OST oficial (regla del 23-oct-2026, audio/ost/ + armar_musica_ost.py)
    estilo="Dark gothic fantasy orchestral underscore, instrumental only.",
    escenas={},
)

ESCENAS = [
    {"id": "intro", "pre": 0.3, "post": 5.6, "frases": [
        "Maliketh, la Hoja Negra. La sombra de la reina Márika, el guardián de la Runa de la Muerte, y el jefe que te espera al final de Farum Azula, la ciudad en ruinas, con una espada hecha de muerte cosida a su propia carne.",
        "A mitad del combate, levanta esa espada y le habla. No te habla a ti, le habla a la muerte. Escúchalo.",
    ]},
    {"id": "introb", "frases": [
        "Y lo que dice es esto: Oh, Muerte. Conviértete en mi espada una vez más.",
        "Casi todo el mundo cree que Maliketh es la víctima de esta historia. El perro fiel de Márika, al que le robaron la muerte, y que acabó escondido en una iglesia comiendo raíces. Y algo de eso es verdad.",
        "Pero el juego esconde otra cosa. Unos guardias remendados con grasa de muertos. Un cazador que hacía el trabajo sucio antes que tú. Un nombre que hacía temblar a los semidioses. Una reina que acunaba recién nacidos. [short pause] Y en el número uno, una frase que FromSoftware grabó, y luego quitó del juego.",
        "Este video lo pidieron ustedes. Aylan escribió que lo esperaba con muchas ansias. Bauti, que este semidiós tiene mucha pinta. Y Piso Papas ya gritaba vamos, Maliketh, antes de que existiera.",
        "Y luego está Diego, que defendió al acusado antes del juicio. Escribió: Maliketh, la Hoja Negra, su único pecado fue servir a una tirana.",
        "Diego, la defensa ya habló. Ahora le toca a la fiscalía. [short pause] Y la fiscalía trae cinco pruebas.",
    ]},
    {"id": "p5", "frases": [
        "Número cinco. [short pause] Guardias hechos de campeones muertos.",
        "Antes de conocer a Gurranq, el clérigo bestia, tienes que cruzar Montedrago, al norte de Caelid. Su refugio es el Santuario de la bestia, un edificio de piedra en la punta de la península, rodeado de cadáveres de hombres bestia.",
        "Y en la puerta te espera un guardia. Una gárgola enorme, negra, con alas de piedra. El juego la llama el Fiel de la Hoja Negra.",
        "Casi todo el mundo la mata, recoge su arma y sigue. El arma se llama Hoja negra de gárgola. Y su descripción dice esto.",
        "Espadón de bronce que portaban las gárgolas denodadas, arreglada con adipocira ennegrecida. Esa es la marca de quienes sirven a Maliketh, la Hoja Negra.",
        "Y adipocira es una palabra que casi nadie se detiene a buscar. [short pause] En la vida real es la grasa de los cadáveres, que se convierte en cera bajo tierra. Cera de muerto.",
        "Y el propio juego te dice de dónde sale. En otra arma de gárgola, el Espadón de gárgola, se lee: tal y como le pasaba a su portador, las piezas que faltan fueron arregladas con adipocira, el retal de los campeones.",
    ]},
    {"id": "p5b", "frases": [
        "El retal de los campeones. Las gárgolas se rompen en combate, y se remiendan con lo que queda de los guerreros que cayeron. Un parche hecho de héroes muertos.",
        "Las gárgolas normales llevan esa cera. Las de esta bestia la llevan ennegrecida. Esa es su marca. Sus guardianes llevan encima, teñidos de negro, a los campeones de otros.",
        "Y el casco de Maliketh tiene una frase que, después de leer eso, ya no suena igual. Los campeones sabían lo que estaba en juego y, por eso mismo, eran campeones.",
        "Ojo: unir esas dos frases es cosa nuestra. El juego no dice de quién era cada pedazo. Solo pone la cera de los campeones en sus guardias, y el miedo de los campeones en su casco.",
        "Y no es la única. Hay otra gárgola igual en las Tierras prohibidas, el camino que sube a las Cumbres de los gigantes, con la misma marca negra y la misma cera de muerto.",
        "Así que el perro fiel de Márika tenía la puerta vigilada por estatuas remendadas con muertos. [short pause] Y eso es lo más suave de la lista.",
    ]},
    {"id": "p4", "frases": [
        "Número cuatro. [short pause] El cazador que trabajaba para él.",
        "Si has pasado por el santuario, ya sabes lo que pide Gurranq: raíces mortuorias. Tú se las llevas, él se las come, y a cambio te paga. En el video de tus atrocidades ya contamos cómo acaba esa historia. Hoy va el porqué.",
        "¿Qué es una raíz mortuoria? Su descripción empieza así: una fuente que despierta a quienes viven en la muerte. Los muertos que caminan. Los esqueletos que se levantan una y otra vez.",
        "Y termina con esto. En la noche del complot, la Runa de la Muerte robada permitió la primera muerte de un semidiós. Posteriormente, la Runa de la Muerte se extendió por las Tierras Intermedias a través de las raíces subterráneas del gran árbol, emergiendo en forma de raíz mortuoria.",
        "Léelo despacio. La muerte que le robaron a Maliketh, la Hoja Negra, se coló por las raíces del Árbol Áureo. Y por donde salía, los muertos dejaban de estar muertos.",
        "Cada esqueleto que se te ha levantado del suelo, cada tumba que vuelve a abrirse, es el fallo de un solo guardián. [short pause] Y su forma de arreglarlo fue comérselo.",
    ]},
    {"id": "p4b", "frases": [
        "Pero no lo arreglaba él solo. En Necrolimbo te cruzas con un caballero de armadura dorada que se presenta así: me conocen como D. Cazo a quienes viven en la muerte, y arranco sus raíces.",
        "Y cuando le hablas de las raíces, te pasa el encargo. Te dice que la propia bestia quiere que alguien ocupe su lugar.",
        "La bestia es Gurranq. D trabajaba para él: recorría el mundo arrancando la muerte que su guardián había dejado escapar, para llevársela a la boca. Y cuando D ya no bastaba, la bestia buscó un recambio.",
        "El recambio eras tú.",
        "Con la cuarta raíz nota algo raro. Dice que hay algo más, algo mezclado. Y aun así, la muerte le sigue calmando el hambre. El juego nunca explica qué llevaba esa raíz. [short pause] Y tú se la diste igual.",
        "Y Gurranq sabía lo que comía. Con la quinta raíz dice que la muerte es su pecado, y que no debería tocarla la mano del hombre. [short pause] Pero la tocaba la tuya. Él mismo te la pedía.",
        "Su Ojo de bestia, el objeto que tiembla cerca de las raíces, lleva grabada su voz: no estoy saciado. Aliméntame. Con más Muerte.",
    ]},
    {"id": "p4c", "frases": [
        "Y aquí va una respuesta. Dark Shooter nos corrigió lo del video del Sinluz: lo que Gurranq nos suplicaba era que guardáramos el arma, y que dejáramos de atacarle.",
        "Tienes razón, Dark. Después de lanzarse contra ti, Gurranq te pide que guardes el arma, que no volverá a olvidar su apetito, y por favor, que basta. Ese basta era para tu espada, no para las raíces.",
        "Anotado. [short pause] Aunque la quinta raíz se la llevaste igual.",
        "Y dos comentarios más. Jonatan escribe que estos videos valen oro: que se pasó media partida con la rueda de Ghiza sin pensarlo tanto como ahora, aunque sigue siendo su favorita.",
        "Jonatan, la rueda no te juzga; el que te juzga es Rykard. [short pause] Y un suscriptor nuevo nos cuenta que hasta su novia, que no juega, se queda viendo los videos. Saludos a ella: ya sabe más de Elden Ring que la mitad de los que lo juegan.",
    ]},
    {"id": "p3", "frases": [
        "Número tres. [short pause] El nombre que asustaba a los dioses.",
        "Gurranq no siempre fue un clérigo. Y su nombre no siempre fue solo un nombre.",
        "Debajo de su santuario hay una daga, la Cinquedea. Su descripción dice que se cedía a los clérigos de alta jerarquía de Farum Azula, y que su diseño rinde homenaje a los cinco dedos de una bestia, símbolo de la inteligencia que se otorgó antaño a los suyos.",
        "Una ciudad de bestias con clérigos. Y entre ellas, una que no rezaba precisamente.",
        "Cuando le llevas la sexta raíz, te regala un milagro: la Piedra de Gurranq. Y su descripción dice: antaño, Gurranq era una bestia tan terroríficamente feroz que su nombre significaba Muerte de los Semidioses.",
        "Muerte de los Semidioses. [short pause] Ese era su nombre. Mucho antes de que nadie robara nada, antes de la Devastación, ya había una bestia que se llamaba así.",
        "Y su casco lo confirma. Maliketh, fiel hermanastro de la Reina Márika, empuñaba un filo bañado en Muerte Escrita. No había ni un solo semidiós que no lo temiese.",
        "Ni uno. [short pause] Todos los semidioses que han pasado por este canal le tenían miedo al mismo perro.",
        "Y los milagros que te enseña lo dejan ver por debajo del disfraz. La Garra de la bestia Gurranq habla de su furia, una vez recuperada su naturaleza de bestia. Y de su desasosiego. [short pause] Un clérigo que, cuando se quita la túnica, vuelve a ser lo que era.",
    ]},
    {"id": "p3b", "frases": [
        "Y ahora la parte que casi nadie conecta. La Muerte Escrita, la que llevaba en la espada, es la propia Runa de la Muerte. Márika la sacó del Círculo de Elden, y se la dio a guardar a su sombra.",
        "Y la Runa reparadora del Príncipe de la Muerte lo dice sin rodeos: la Orden Dorada se creó tras confinar a la Muerte Escrita.",
        "La Orden Dorada. La edad de oro, el Árbol Áureo brillando, los semidioses que no envejecen. Todo se levantó encima de una jaula. Y el carcelero era él.",
        "Para que nadie pudiera volver a robarla, vinculó la espada a su propia carne. Y en la cinemática de Farum Azula lo ves: la hoja le sale del cuerpo.",
        "Mientras él guardó esa jaula, la muerte de verdad no existió en las Tierras Intermedias. Lo decidió Márika. [short pause] Y lo hizo cumplir la bestia que daba miedo a todos.",
    ]},
    {"id": "p3c", "frases": [
        "Y antes del número dos, un comentario. Edgar nos pidió que habláramos latino, porque a veces se confunde con los nombres. Y al final añadió: y me puedes saludar.",
        "Hola, Edgar. [short pause] Y para que hoy no te confundas: en Latinoamérica, a este semidiós le llaman la Espada Negra. Aquí le decimos la Hoja Negra. Mismo perro, distinta correa.",
        "Lo de hablar latino lo dejamos para otro día. El Profeta solo tiene un acento: el de las profecías.",
    ]},
    {"id": "p2", "frases": [
        "Número dos. [short pause] La reina que acunaba a los recién nacidos.",
        "Antes de ser carcelero, Maliketh fue otra cosa: el arma de Márika contra una rival.",
        "En Montedrago, cerca del santuario, hay una torre redonda en un islote: la Torre Sagrada de Caelid. Arriba, después de pelear contra un apóstol sacrodermo, encuentras un espadón enorme, el Espadón del exterminador de dioses.",
        "Su descripción: espada sagrada de la Reina del Ojo Velado, que controlaba a los apóstoles sacrodermos antes de sucumbir ante Maliketh, la Hoja Negra.",
        "En el video de Melina la nombramos de pasada. Hoy toca contarla desde el otro lado. El Ritual de la llama negra dice que la Reina del Ojo Velado dirigió a los apóstoles. Y que se dice que era una empírea elegida por los Dedos.",
        "Una empírea. Lo mismo que Márika: el propio Recuerdo de esta bestia llama a la reina su empírea. Una candidata a diosa, elegida por los mismos Dedos. [short pause] Y la sombra de Márika la quitó de en medio.",
    ]},
    {"id": "p2b", "frases": [
        "¿Y quiénes eran sus apóstoles? Gente que empuñaba la llama negra, la que mataba dioses. La Llama negra rastreadora lo cuenta: hace un tiempo la llama negra era capaz de matar dioses. Sin embargo, cuando Maliketh selló la Muerte Escrita, el verdadero poder de la llama negra se perdió.",
        "Y la túnica de los apóstoles lo remata: tras su derrota ante Maliketh, la Hoja Negra, la fuente de su poder fue sellada.",
        "Pero el objeto que casi nadie lee es un talismán pequeño, la Empañadura sacroderma. La Reina del Ojo Velado acuna a los apóstoles recién nacidos envueltos en este paño. Pronto crecerán y se convertirán en la fatalidad de los dioses.",
        "Una reina acunando recién nacidos en un paño. Y la Hoja Negra, que llega y sella el poder con el que nacían. [short pause] Esos niños crecieron sin lo único que los hacía peligrosos.",
        "Ojo, que aquí tampoco hay santos. Sacrodermo quiere decir piel de dios. Los apóstoles desollaban dioses, y llevan esa piel encima. Y el juego dice que la reina sucumbió y fue derrotada. No dice que la matara.",
        "Pero sí deja claro quién ganó. En la torre queda su espada. [short pause] Y en tu inventario se queda el paño de los recién nacidos.",
    ]},
    {"id": "subs", "frases": [
        "Antes del número uno, varios comentarios que se ganaron su sitio. Bryan dice que ha visto muchos videos de lore de Elden Ring, pero que pocos lo entretienen y le enseñan tanto. Y Alberto, que son de las mejores explicaciones que ha visto.",
        "Astora lo resume mejor que nadie: este canal tiene encanto para contar las atrocidades de estos enfermos.",
        "Y Lissom escribió: toca pasarse el juego otra vez. Ya me suscribí. [short pause] Gracias, Lissom. Eso es exactamente lo que pedimos.",
        "A día de hoy somos mil trescientos ochenta suscriptores. Aun así, de cada cien vistas de estos videos, menos de nueve son de gente suscrita. El siguiente objetivo son dos mil.",
        "A Maliketh le hizo falta coserse la muerte a la carne para que nadie se la llevara. Aquí, en cambio, basta con apretar un botón. [short pause] Y todos los comentarios se leen, uno por uno: con ellos se decide lo que viene.",
    ]},
    {"id": "p1", "frases": [
        "Número uno. [short pause] La noche que dejó robar la Muerte.",
        "Esta es la parte que todo el mundo cree conocer. Rogier te la cuenta en la Mesa Redonda, y Ranni la narra en el tráiler: en una noche de niebla invernal, alguien robó la Runa de la Muerte. Y los semidioses empezaron a caer. El primero, Godwyn, el Dorado.",
        "Esa noche tiene nombre oficial: la Noche de los Puñales Negros. Y pasó porque el guardián falló. Por eso se cosió la espada a la carne. Por eso acabó escondido, comiendo raíces.",
        "Y la asesina que lo hizo tiene nombre. Tiche, la Cuchillo Negro. Su ceniza de espíritu dice que, durante la noche del complot, imbuyó su puñal negro en la Runa de la Muerte para dar muerte a Godwyn, el Dorado. [short pause] Y esa ceniza la invocas tú, para que pelee a tu lado.",
        "El Sello maldito de la Muerte añade el detalle que casi nadie recuerda: aquella noche, dos semidioses murieron al mismo tiempo. Ranni fue la primera en ver cómo moría su carne. Y en el caso del Príncipe de la Muerte, Godwyn, solo murió su alma.",
        "Hasta aquí, la versión de siempre. Ahora, lo que el juego esconde en tres objetos que están en tres sitios distintos.",
        "El primero es el Aojo de puñal negro, en unas catacumbas de Liurnia. Durante la Noche de los Puñales Negros, alguien robó un fragmento de la Runa de la Muerte a Maliketh, la Hoja Negra, e imbuyó las dagas de los asesinos con su poder. Esta marca es una prueba del ritual, y oculta la verdad de la conspiración.",
        "Oculta la verdad. El juego te dice, con esas palabras, que lo que te han contado no es todo.",
        "El segundo, la armadura de las asesinas. Las asesinas que llevaron a cabo las hazañas de la Noche de los Puñales Negros eran todas mujeres y, según los rumores, eran númenes estrechamente vinculadas a la propia Márika.",
        "Las asesinas eran de la gente de Márika. [short pause] Y el tercer objeto es el que lo une todo.",
    ]},
    {"id": "p1b", "post": 15.6, "frases": [
        "Es el Recuerdo de la Hoja Negra, el que te llevas cuando lo vences. Maliketh era una bestia ligada a la sombra de su empírea. El ansia de Márika por disponer de su sombra actuaba como un baluarte contra la Muerte Escrita. Aun así, ella lo traicionó.",
        "En inglés y en japonés es todavía más duro: Márika solo lo quería como recipiente para encerrar la muerte. [short pause] Y aun así, lo traicionó.",
        "Así que la pregunta es esta, y ojo, que el juego no la contesta: ¿le robaron la Muerte a Maliketh, o se la hizo robar su propia reina?",
        "Hay alguien que parece tener la respuesta. El propio Maliketh. Pero solo la dice si haces algo que casi nadie hace: atacar a Gurranq en su santuario hasta matarlo.",
        "Si lo matas, el clérigo bestia no habla de raíces. Sus últimas palabras son para ella. Escúchalo.",
    ]},
    {"id": "p1c", "post": 14.2, "frases": [
        "Y lo que dice es esto: ¿por qué me engañaste, Márika? ¿Por qué lo rompiste?",
        "En japonés el verbo es justo ese: romper. El guardián de la muerte, muriendo, acusa a su reina de engañarlo. Y de romper algo. [short pause] El Círculo de Elden se rompió. Y el que lo pregunta es su sombra.",
        "Y todavía hay más. FromSoftware grabó un diálogo entero para el final del combate contra Maliketh, la Hoja Negra. Lo quitó del juego, pero sigue en los archivos. Y es la confesión que le faltaba a esta historia. Escúchalo.",
    ]},
    {"id": "p1d", "frases": [
        "Oh, Márika. ¿Qué pasó? ¿Fui yo el necio? ¿O fuiste tú la que me engañó?",
        "En ese mismo diálogo recortado, la bestia promete muerte a los ladrones de la Muerte. Y te dice que, armado con la muerte, puedes elegir el trono que desees.",
        "Fíjate en lo que no hace: no la acusa a ella sin más. Se pregunta si el necio fue él. [short pause] Y FromSoftware decidió que esa pregunta no la oyera nadie.",
        "Así que volvamos con Diego, que lo defendía: su único pecado fue servir a una tirana. [short pause] Puede que la tirana existiera, Diego. Pero antes de servirla, su nombre significaba Muerte de los Semidioses. Y después, mandaba a otros a arrancar raíces por él.",
    ]},
    {"id": "cierre", "post": 8.3, "frases": [
        "Esa es la lista. Guardias remendados con la grasa de campeones muertos. Un cazador que arrancaba raíces para él, y el recambio que iba a ocupar su lugar, que eras tú. Un nombre que significaba Muerte de los Semidioses. Una reina que acunaba recién nacidos. Y una noche en la que el guardián de la muerte se preguntó si lo habían engañado.",
        "Y queda una última cosa que casi nadie sabe de esta pelea: Maliketh tiene dos formas de morir, y cada jugador solo oyó una.",
        "Si nunca le llevaste raíces a Gurranq, cuando cae te desprecia. Escúchalo.",
    ]},
    {"id": "cierreb", "post": 11.7, "frases": [
        "Sinluz necio. ¿Para qué codicias la Muerte Escrita? ¿Para matar a quién?",
        "Pero si terminaste su misión, si le diste de comer hasta el final, su último aliento cambia. Escúchalo.",
    ]},
    {"id": "cierrec", "frases": [
        "Perdóname, Márika. La Orden Dorada ya no puede restaurarse.",
        "Al que nunca le dio de comer, lo desprecia. Al que le dio de comer, no le dice nada: le pide perdón a ella. [short pause] Hasta el último aliento, Maliketh le habló a Márika, y a nadie más.",
        "Hasta su entrada cambia. Si le diste de comer, cuando llegas a su arena no te recibe como a un ladrón. Te pregunta por qué. Duda. Y luego jura que la Muerte Escrita no volverá a ser robada.",
        "Y entonces lo vences. La Runa de la Muerte queda libre, y la capital del reino acaba en ceniza. [short pause] El carcelero cae, y la muerte sale de la jaula. Y la que abrió la puerta esta vez no fue ninguna asesina de Márika. Fuiste tú.",
        "En los comentarios siguen pidiendo a Bayle el Temible, a Rennala y a Rellana, a Parches, y al Zampaheces con Gideon. Dinos cuál quieres.",
        "En el canal tienes las atrocidades de Márika y Radagon, de Miquella, Malenia, Ranni, Melina, Radahn, Morgott, Mohg, Godrick, Godfrey, Rykard, Messmer, y las tuyas. Suscríbete, que vamos por los dos mil.",
        "Y si te gustan los mundos donde hasta los dioses tienen las manos sucias, Crónicas de Tamriel, nuestro canal hermano, cuenta los secretos de Skyrim. Te lo dejo aquí al final.",
        "Y la próxima vez que una bestia te pida que le traigas la muerte, pregúntate primero quién la dejó escapar. [long pause] A lo mejor la bestia ya lo sabe.",
    ]},
]

# Falsas alarmas revisadas con _revisar_voz.py (27-nov): nombres (Málikez→«maliques», Márika→«marica», Gúrank→«gurang»),
# [short pause], «dos mil»→2000, «dos semidioses»→«doce midioses» (Whisper junta las sílabas).
CER_MAX_POR_FRASE = {'introb_1': 0.015, 'introb_4': 0.03, 'p5_4': 0.034, 'p5b_2': 0.034, 'p4_4': 0.025, 'p4b_0': 0.022, 'p4c_0': 0.018, 'p4c_3': 0.023, 'p4c_4': 0.02, 'p3_1': 0.019, 'p3_6': 0.033, 'p2_1': 0.033, 'p2b_1': 0.034, 'p1_1': 0.017, 'p1_4': 0.018, 'p1_6': 0.018, 'p1_9': 0.018, 'p1b_2': 0.022, 'p1d_0': 0.022, 'cierre_1': 0.014, 'cierre_2': 0.019, 'cierreb_0': 0.002, 'cierrec_0': 0.023, 'cierrec_4': 0.039, 'cierrec_5': 0.06, 'introb_3': 0.022, 'p2_3': 0.027, 'p1c_0': 0.02, 'cierrec_1': 0.033}
GAP_MAX_POR_FRASE = {'introb_1': 0.58, 'introb_4': 0.5, 'p5_4': 0.58, 'p5b_2': 0.91, 'p4_4': 0.67, 'p4b_0': 0.59, 'p4c_0': 0.56, 'p4c_3': 0.45, 'p4c_4': 1.05, 'p3_1': 0.41, 'p3_6': 0.51, 'p2_1': 0.53, 'p2b_1': 0.56, 'p1_1': 0.61, 'p1_4': 0.61, 'p1_6': 0.59, 'p1_9': 0.97, 'p1b_2': 0.75, 'p1d_0': 0.46, 'cierre_1': 0.58, 'cierre_2': 0.49, 'cierreb_0': 0.57, 'cierrec_0': 0.46, 'cierrec_4': 0.42, 'cierrec_5': 0.2, 'introb_3': 0.46, 'p2_3': 0.43, 'p1c_0': 0.55, 'cierrec_1': 1.09}
TAIL_MAX_POR_FRASE = {'introb_1': 1.01, 'introb_4': 0.7, 'p5_4': 0.75, 'p5b_2': 0.67, 'p4_4': 0.66, 'p4b_0': 0.64, 'p4c_0': 0.61, 'p4c_3': 0.79, 'p4c_4': 0.9, 'p3_1': 0.34, 'p3_6': 0.66, 'p2_1': 0.53, 'p2b_1': 0.56, 'p1_1': 0.59, 'p1_4': 0.92, 'p1_6': 0.82, 'p1_9': 0.53, 'p1b_2': 0.68, 'p1d_0': 0.59, 'cierre_1': 0.77, 'cierre_2': 0.24, 'cierreb_0': 1.05, 'cierrec_0': 0.33, 'cierrec_4': 0.54, 'cierrec_5': 1.03, 'introb_3': 0.83, 'p2_3': 0.67, 'p1c_0': 0.55, 'cierrec_1': 0.87}
