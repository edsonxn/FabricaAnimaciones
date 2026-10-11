# -*- coding: utf-8 -*-
"""Escribe prompts.json (un prompt por beat) con la FICHA de guion.py. Correr desde la carpeta del video.
Cada prompt = estilo + luz -> sujeto y acción -> escenario -> cierre. Personas por oficio, nunca por nombre."""
import json

import guion

F = guion.FICHA
Q = F["personajes"]["quimico"]
A = F["personajes"]["ayudante"]
I = F["personajes"]["ingeniero"]
S = F["personajes"]["esposa"]
CIL = F["objeto"]
LAB = ("en un laboratorio químico industrial de mil novecientos treinta y ocho, con mesas de madera oscura, matraces y "
       "tubos de vidrio, y lámparas colgantes de metal")
POLVO = "un polvo blanco y ceroso, como nieve apelmazada"
COCINA50 = ("en una cocina francesa de los años cincuenta, con azulejos crema, estufa de gas esmaltada blanca y cacerolas "
            "de cobre colgadas")
TALLER = ("en un pequeño taller casero francés de los años cincuenta, con banco de madera, herramientas colgadas y una "
          "ventana con luz de tarde")

# (luz, escena)
P = {
    1: ("luz cálida de lámpara de laboratorio", f"Primer plano de la mano de {Q} girando la válvula de latón de {CIL}, sujeto en un soporte de hierro sobre una mesa de madera, {LAB}."),
    2: ("luz cálida de lámpara de laboratorio", f"{Q} acerca la oreja a la válvula abierta de {CIL} con cara de desconcierto, sin que salga nada de la válvula, {LAB}."),
    3: ("luz lateral dramática", f"Plano detalle de {CIL} acostado sobre el platillo de una báscula antigua de hierro negro con pesas de latón en el otro platillo, los dos platillos perfectamente equilibrados, sobre una mesa de madera oscura."),
    4: ("luz tenue con sombras largas", f"{Q} sostiene con las dos manos {CIL} frente a su cara y lo mira fijamente con el ceño fruncido, fondo de laboratorio oscuro con matraces de vidrio desenfocados."),
    5: ("luz de estudio sobre fondo azul oscuro", "Tres objetos de plastilina en fila sobre una mesa: a la izquierda una nube de humo anaranjada en forma de hongo en miniatura, en el centro una luna gris con cráteres y una pequeña bandera, a la derecha una sartén negra con un huevo frito."),
    6: ("luz fría de mañana", f"Vista desde arriba de una mesa de laboratorio de madera llena de matraces, tubos de vidrio y cuadernos cerrados, y en una esquina olvidada {CIL}, {LAB}."),
    7: ("luz dorada dramática", "Un pequeño montón de polvo blanco y ceroso sobre un platillo de vidrio, colocado sobre un cojín de terciopelo rojo dentro de una vitrina de cristal, como si fuera una joya, con monedas de oro apiladas al lado."),
    8: ("luz cálida de cocina", "Primer plano de una sartén negra de plastilina sobre una estufa con un huevo frito de yema amarilla brillante que resbala hacia el borde, con vapor suave."),
    9: ("luz fría de taller", f"Un bote de basura metálico gris y abollado en un rincón de laboratorio, y la mano de {Q} detenida en el aire sosteniendo sobre el bote {CIL} sin soltarlo."),
    10: ("luz de mañana de primavera", "Plano general de un complejo industrial de ladrillo rojo con chimeneas altas y tanques a la orilla de un río ancho, con árboles en flor y automóviles negros redondeados de los años treinta estacionados afuera."),
    11: ("luz cálida de ventana", f"Retrato de medio cuerpo de {Q} de pie y sonriente con una carpeta bajo el brazo, {LAB}."),
    12: ("luz cálida de lámpara", f"{Q} sentado en un banco alto escribe en un cuaderno frente a una hilera de matraces con líquidos transparentes, con gesto de rutina aburrida, {LAB}."),
    13: ("luz de cocina de los años treinta", "Un refrigerador antiguo blanco de esquinas redondeadas con un compresor cilíndrico encima, puerta entreabierta con botellas de leche de vidrio dentro, en una cocina de los años treinta con piso de cuadros blancos y negros."),
    14: ("luz gris de tarde nublada", "Familias de plastilina con ropa de los años treinta saliendo apuradas por la puerta de un edificio de departamentos de ladrillo, tapándose la nariz con pañuelos, mientras un humo verdoso sale por una ventana de la planta baja."),
    15: ("luz de oficina cálida", "Tres hombres de negocios de plastilina con trajes oscuros de los años treinta, cada uno abrazando con recelo un refrigerador blanco pequeño distinto y mirando de reojo a los otros dos, en una sala de juntas de madera."),
    16: ("luz cálida de laboratorio", f"{Q} con gafas protectoras redondas ajusta una llave en un aparato de tubos y serpentines de vidrio conectados a un matraz redondo vacío y transparente, {LAB}."),
    17: ("luz suave", f"{Q} frente a un pizarrón verde cubierto de garabatos de tiza ilegibles y enredados como un nudo, rascándose la cabeza con una tiza en la mano."),
    18: ("luz cálida de taller", f"Una mesa larga de madera con dos filas ordenadas de cilindros pequeños de acero gris con válvula de latón, todos idénticos y sin etiquetas, y {A} colocando el último de la fila."),
    19: ("luz azulada fría", "Una caja de madera abierta llena de bloques de hielo seco blanco de los que sale una niebla blanca que se derrama por los bordes, con las puntas de varios cilindros pequeños de acero gris con válvula de latón asomando entre el hielo."),
    20: ("luz clara de mañana entrando por ventanales altos", f"{A} camina por el laboratorio cargando en brazos {CIL} cubierto de escarcha, {LAB}."),
    21: ("luz clara de mañana", f"Las manos de {A} conectan con una llave inglesa una manguera de caucho negro a la válvula de {CIL}, junto a un aparato de vidrio."),
    22: ("luz tenue y silenciosa", f"{Q} y {A} inclinados a cada lado de {CIL} que está sobre la mesa, mirando la válvula abierta de la que no sale nada, con caras de extrañeza, {LAB}."),
    23: ("luz de detalle muy cercana", f"Plano detalle de unos dedos de plastilina metiendo un alambre delgado de cobre por el orificio de la válvula de latón de {CIL}."),
    24: ("luz lateral cálida", f"{A} coloca {CIL} sobre el platillo de una báscula antigua de hierro negro mientras {Q} observa la aguja agachado, {LAB}."),
    25: ("luz fría de pasillo", "Un rincón de bodega industrial con una pila de cilindros pequeños de acero gris abollados y desechados, y un obrero de plastilina con overol azul y gorra alejándose de espaldas con otro cilindro igual en la mano."),
    26: ("luz de lámpara de escritorio", f"{Q} sentado ante un escritorio de madera se sujeta la cabeza con una mano mientras mira un cuaderno abierto lleno de rayas y garabatos ilegibles, con una regla de cálculo de madera al lado, ante una pared de ladrillo desnuda sin carteles, sin tablas ni láminas colgadas, y frascos de vidrio sin etiquetas."),
    27: ("luz dramática de un solo foco", f"{CIL} de pie y solo en el centro de una mesa de madera vacía, con una sombra larga, y al fondo en penumbra las siluetas de dos hombres mirándolo."),
    28: ("luz cálida de laboratorio", f"{Q} sostiene boca abajo con las dos manos {CIL} sin su válvula y lo sacude con fuerza sobre la mesa, {LAB}."),
    29: ("luz de detalle muy cercana", "Plano detalle de una mesa de madera oscura con unas pocas escamas blancas y cerosas recién caídas, y arriba la boca abierta de un cilindro pequeño de acero gris del que cae otra escama."),
    30: ("luz cálida de taller", f"{A} sujeta en un tornillo de banco de hierro {CIL} y apoya sobre él una sierra de arco para metal, mientras {Q} observa a un lado con los brazos cruzados."),
    31: ("luz de taller con chispas", f"Primer plano de una sierra de arco para metal cortando por la mitad un cilindro pequeño de acero gris sujeto en un tornillo de banco, con virutas de metal y chispas pequeñas, y al fondo {Q} retrocediendo un paso con los ojos entrecerrados."),
    32: ("luz cálida que entra en el metal", "Dos mitades de un cilindro pequeño de acero gris recién cortado, separadas sobre un banco de trabajo de madera, mostrando su interior hueco cubierto de una capa blanca."),
    33: ("luz de detalle muy cercana", f"Plano detalle del interior de medio cilindro de acero gris cortado, con las paredes completamente cubiertas por {POLVO}."),
    34: ("luz cálida de laboratorio", f"Primer plano de la mano de {Q} intentando tomar una pizca de {POLVO} que se le resbala entre los dedos y cae de nuevo."),
    35: ("luz conceptual sobre fondo azul oscuro", "Dentro de un cilindro de acero transparentado en corte, a la izquierda una nube de bolitas verdes sueltas flotando como gas, y a la derecha las mismas bolitas ya apretadas formando un bloque blanco sólido."),
    36: ("luz conceptual sobre fondo azul oscuro", "Decenas de bolitas de plastilina verdes y amarillas enganchadas unas con otras formando cadenas larguísimas que serpentean por todo el encuadre como collares de cuentas."),
    37: ("luz anaranjada cálida", "Corte de la pared de hierro gris de un cilindro, de la que salen pequeñas chispas anaranjadas que tocan a unas bolitas verdes y las hacen engancharse en cadena."),
    38: ("luz gris apagada", f"{Q} de pie y desanimado frente a un aparato de vidrio de laboratorio apagado y vacío, con los hombros caídos, {LAB}."),
    39: ("luz de detalle triste", f"Primer plano de la palma abierta de {Q} con un pequeño puñado de {POLVO}, y al fondo desenfocado un calendario de pared con las hojas arrancadas en el suelo."),
    40: ("luz cálida esperanzadora", f"{Q} aparta con el brazo una escoba y un recogedor apoyados en la mesa y se inclina con una lupa de mango de madera sobre un platillo de vidrio con {POLVO}, {LAB}."),
    41: ("luz cálida de laboratorio", f"{Q} se pone unas gafas protectoras redondas y alinea sobre la mesa una fila de tubos de ensayo en una gradilla de madera, cada uno con un poco de polvo blanco, {LAB}."),
    42: ("luz verdosa de vapores", f"{Q} con gafas protectoras vierte con una pipeta de vidrio un ácido humeante amarillo sobre {POLVO} en un platillo de vidrio; al lado, otro platillo con un clavo de hierro que se deshace en burbujas."),
    43: ("luz azul y naranja de llama", "Un mechero de laboratorio de metal con llama azul calentando una cápsula de porcelana blanca con un trozo de material blanco y ceroso que sigue intacto, y al lado otra cápsula con un plástico ámbar derretido en un charco."),
    44: ("luz cálida de estantería", f"Una fila de seis frascos de vidrio con líquidos de distintos colores, y en el fondo de cada uno el mismo grumo blanco intacto, mientras {Q} levanta uno de los frascos a contraluz."),
    45: ("luz de detalle", f"Una placa inclinada cubierta de material blanco y ceroso por la que resbala a toda velocidad un pequeño cubo de metal, y el dedo de {Q} resbalando en el borde."),
    46: ("luz de estudio limpia", "Una placa blanca y cerosa sobre la que hay una gota de agua perfectamente redonda, una gota de aceite dorado redonda y un tubo de pegamento antiguo de metal cuya tira de pegamento ámbar no se adhiere y se enrosca en el aire."),
    47: ("luz de lámpara de escritorio verde", f"{Q} sentado ante un escritorio de madera escribe con pluma fuente en un cuaderno de laboratorio de tapas negras, con trazos de tinta ilegibles, tranquilo, con un platillo de polvo blanco junto al tintero."),
    48: ("luz nocturna de ventana", f"{Q} sale del laboratorio apagando la luz, de espaldas en la puerta, mientras sobre la mesa en primer plano brilla suavemente un platillo de vidrio con {POLVO}."),
    49: ("luz dorada milagrosa", "Un bloque blanco y ceroso sobre un pedestal de madera con rayos de luz dorada alrededor, y sobre él, proyectada, la sombra enorme y oscura de una balanza de platillos."),
    50: ("luz fría industrial", "Una fábrica química de los años cuarenta con un reactor de acero enorme lleno de tuberías, del que sale por una pequeña bandeja apenas un puñado de polvo blanco, mientras un contador de plastilina con visera verde apila torres de monedas de oro junto a la bandeja."),
    51: ("luz de taller", "Un obrero de plastilina con overol y guantes gruesos intenta meter un bloque blanco y ceroso en un molde metálico de hierro con una prensa manual, y el bloque se desmorona en grumos sin tomar forma."),
    52: ("luz de oficina de los años cuarenta", "Un escritorio de madera con un documento oficial de varias hojas con sello de lacre rojo y cinta azul, lleno de líneas de tinta ilegibles, junto a un frasco de vidrio tapado con corcho lleno de polvo blanco."),
    53: ("luz polvorienta de bodega", "Un estante de madera en una bodega con un frasco de vidrio tapado con corcho lleno de polvo blanco, cubierto de polvo y con una telaraña en la esquina, entre cajas de cartón viejas."),
    54: ("luz de tienda vacía", "Un vendedor de plastilina con traje gris y sombrero de los años cuarenta sentado solo tras un mostrador de madera con un único frasco de polvo blanco a la venta, apoyando la cara en la mano, en una tienda sin clientes."),
    55: ("luz nocturna de reflectores", "Una ciudad industrial secreta de los años cuarenta en un valle boscoso de noche, con barracas de madera, una cerca de alambre, una torre de vigilancia con reflector y un soldado de plastilina con casco en la entrada."),
    56: ("luz verdosa de laboratorio militar", "Tres científicos de plastilina con batas blancas y gafas alrededor de una mesa con un trozo de mineral amarillo verdoso brillante dentro de una caja de plomo gris, en un laboratorio de los años cuarenta con medidores de aguja."),
    57: ("luz amarillenta tóxica", "Una tubería gruesa de acero con una mirilla de vidrio por la que se ve circular un gas amarillo verdoso denso, con gotas corrosivas que humean en una unión de la tubería."),
    58: ("luz amarillenta tóxica de detalle", "Plano detalle de una válvula industrial de hierro y una junta de goma negra totalmente corroídas, agrietadas y deshaciéndose en migajas, con un hilo de vapor amarillo escapando."),
    59: ("luz fría de banco de pruebas", "Una mesa metálica con una fila de anillos de sellado de distintos materiales, de goma negra, cuero marrón, cobre y corcho, todos derretidos, agujereados o rotos, y un ingeniero militar de plastilina con bata tachando una lista con gesto frustrado."),
    60: ("luz cálida de revelación", "Un científico de plastilina de bata blanca y bigote canoso con un dedo levantado y cara de haber recordado algo, y en su otra mano un frasco de vidrio tapado con corcho lleno de polvo blanco, en una oficina de los años cuarenta."),
    61: ("luz dura de oficina militar", "Un frasco de vidrio lleno de polvo blanco dentro de una caja fuerte de acero abierta, y un oficial militar de plastilina con uniforme verde oliva y gorra cerrando la pesada puerta con las dos manos."),
    62: ("luz industrial inmensa", "Interior de una nave industrial gigantesca de los años cuarenta con filas interminables de tuberías, tanques y válvulas que se pierden a lo lejos, y obreros de plastilina diminutos con casco caminando por una pasarela."),
    63: ("luz cálida de calle", "Una calle de un pueblo estadounidense de los años cuarenta con gente de plastilina paseando y un niño repartiendo periódicos sin letras, y al fondo, tras una colina con cerca de alambre, el resplandor de una fábrica escondida."),
    64: ("luz festiva de día", "Una calle de ciudad de mil novecientos cuarenta y cinco con gente de plastilina celebrando, serpentinas y confeti de colores en el aire, y en primer plano una caja de cartón abierta con un bloque blanco y ceroso que sale a la luz."),
    65: ("luz fría de fábrica", "Un rollo grande de cable eléctrico con forro blanco y ceroso, una junta blanca en una tubería de acero y un vaso de precipitados de vidrio con tapa blanca, agrupados sobre una mesa de fábrica de los años cuarenta."),
    66: ("luz cálida de cocina vacía", "Una cocina de los años cincuenta vacía y silenciosa, con una sartén de hierro negro común con comida quemada y pegada en el fondo, abandonada sobre la estufa."),
    67: ("luz dorada de amanecer en el río", f"{I} de pie a la orilla de un río francés tranquilo con sauces, sosteniendo una caña de pescar de bambú, con una cesta de mimbre a sus pies."),
    68: ("luz cálida de tarde", f"{I} sentado frente a un banco de madera pasa con cuidado un hilo de pescar por un pequeño recipiente con una pasta blanca, con un carrete de caña de pescar al lado, {TALLER}."),
    69: ("luz cálida de tarde", f"{S} apoyada en el marco de la puerta con los brazos cruzados y una ceja levantada observa a un hombre que trabaja de espaldas en un banco con una caña de pescar, {TALLER}."),
    70: ("luz cálida de tarde", f"{S} señala con el dedo un hilo de pescar blanco y liso que cuelga sin enredarse entre las manos de {I}, que la mira sorprendido, {TALLER}."),
    71: ("luz cálida de cocina", f"{S} levanta con una mano una sartén de aluminio con restos de comida quemada y pegada y la muestra con gesto de reclamo divertido, {COCINA50}."),
    72: ("luz de detalle", "Una sartén de aluminio plateado boca arriba sobre un banco de madera, y encima una lámina blanca y cerosa que resbala y cae hacia un lado sin quedarse pegada, con una espátula y un bote de pegamento volcados al lado."),
    73: ("luz verdosa de taller", f"{I} con guantes de goma gruesos y gafas protectoras sumerge con unas pinzas una sartén de aluminio en una cubeta de vidrio con ácido burbujeante, {TALLER}."),
    74: ("luz conceptual de detalle extremo", "Corte ampliado de una superficie de aluminio plateado llena de poros y cráteres diminutos, con una capa blanca y cerosa que rellena esos poros y queda anclada como raíces."),
    75: ("luz cálida de cocina", f"{S} sonríe asombrada inclinando una sartén de interior oscuro y liso, de la que un huevo frito de yema amarilla se desliza entero hacia un plato blanco, {COCINA50}."),
    76: ("luz de mañana en la calle", f"{I} y {S} de pie y orgullosos frente a un pequeño local de fábrica francés de los años cincuenta con persiana de madera, con una mesa en la acera llena de sartenes de interior oscuro apiladas."),
    77: ("luz industrial cálida", "Una cinta transportadora de fábrica de los años cincuenta con una fila interminable de sartenes idénticas de interior oscuro, y obreras de plastilina con pañuelo en la cabeza empacándolas en cajas de cartón."),
    78: ("luz dura del espacio", "Un astronauta de plastilina con traje espacial blanco abultado y casco de visor dorado caminando sobre la superficie gris de la Luna llena de cráteres, con la Tierra azul en el cielo negro."),
    79: ("luz gris de lluvia", "Un excursionista de plastilina con chaqueta impermeable roja con capucha caminando sonriente bajo una lluvia fuerte en un sendero de montaña, con las gotas de agua rebotando en la tela."),
    80: ("luz blanca de quirófano", "Un cirujano de plastilina con bata, gorro y cubrebocas verdes sosteniendo en alto con unas pinzas, a la altura de sus ojos, un tubo blanco delgado, flexible y corrugado del tamaño de un dedo, bajo una lámpara redonda de quirófano, con una bandeja de acero limpia y vacía delante; quirófano vacío, sin paciente, sin camilla, sin sangre, sin órganos."),
    81: ("luz de atardecer sobre el puerto", "Una gran estatua verde de cobre de una mujer con túnica, corona de puntas y una antorcha en alto, sobre un pedestal de piedra en una isla, rodeada de andamios de restauración."),
    82: ("luz interior dorada", "Interior hueco de una estatua gigante: una pared curva de láminas de cobre vista por dentro y una estructura de barras de metal gris, con una tira blanca delgada colocada entre el cobre y cada barra, y un obrero de plastilina con casco revisándola."),
    83: ("luz cálida de laboratorio", f"{Q} sonríe con calma sosteniendo en una mano medio cilindro de acero gris cortado con el interior blanco, junto a un bote de basura metálico vacío, {LAB}."),
    84: ("luz de salón elegante", "Un químico de plastilina de unos cuarenta años, de pelo castaño oscuro peinado de lado, con traje oscuro y corbata granate, recibe una medalla dorada con cinta azul de manos de un hombre mayor con toga, en un salón de ceremonias con cortinas rojas."),
    85: ("luz de salón elegante", "Invitados de plastilina con trajes y vestidos de los años cincuenta sentados en mesas redondas de banquete, cada uno sosteniendo con sorpresa un molde metálico para panecillos de seis huecos con interior oscuro y liso."),
    86: ("luz cálida de mañana en la cocina", "Una cocina actual y sencilla con una mano de plastilina inclinando una sartén negra de la que un huevo frito de yema amarilla se desliza hacia un plato, con una ventana soleada al fondo."),
    87: ("luz dramática de un solo foco", f"{Q} de pie con una sierra de arco para metal en la mano y mirada decidida, frente a {CIL} sujeto en un tornillo de banco de hierro."),
    88: ("luz cálida de estudio", "Una repisa de madera con una fila de inventos de plastilina en miniatura: una sartén negra, un cilindro pequeño de acero gris, un foco de luz, un engrane dorado y un matraz de vidrio."),
    89: ("luz cálida de mesa de trabajo", "Dos manos de plastilina amasando una bola de plastilina naranja sobre una mesa de madera, rodeadas de barras de plastilina de colores y pequeñas herramientas de modelar de madera."),
}

beats = json.load(open("beats.json", encoding="utf-8"))
beats = beats["beats"] if isinstance(beats, dict) else beats
assert len(beats) == len(P), (len(beats), len(P))
out = {}
for i, b in enumerate(beats, 1):
    luz, esc = P[i]
    out[b["id"]] = f"{F['estilo']}, {luz}. {esc} {F['cierre']}"
json.dump(out, open("prompts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "prompts; largo máximo", max(map(len, out.values())))
