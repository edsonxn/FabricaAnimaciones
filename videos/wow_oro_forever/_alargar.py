# -*- coding: utf-8 -*-
"""Añade frases (comprobadas en _investigacion_wow_oro_forever.md) ANTES de la última frase de cada escena. Se corre una vez."""
import re
EXTRA = {
 "intro": ["Y nada de esto es teoría: todo sale del juego en vivo, de los precios reales de la subasta de estos días, y de lo que han hecho jugadores que ya llegaron al sesenta con la bolsa llena."],
 "c30": ["El entrenamiento completo, del uno al sesenta, cuesta lo mismo en todas las clases: unos doscientos siete de oro. Pero eso no significa que tengas que pagarlo todo de golpe.",
         "Algunos rangos los puedes comprar más tarde, cuando el oro sobre. Y otros, simplemente, nunca."],
 "c29": ["Y no es un atajo raro: es una misión de clase, con su historia y todo. El brujo se gana su corcel vil, y el paladín, su caballo de guerra."],
 "c28": ["Y el descuento también vale para los colores extra: cada montura de otro color baja de veinte a dieciocho de oro."],
 "c27": ["Y otra de las ventajas, Economía de componentes, hace que tus habilidades de clase ya no te pidan componentes de vendedor. Otro gasto que desaparece."],
 "c26": ["Y no somos los únicos que lo vimos tarde: hasta las guías escritas antes del lanzamiento decían diez. El juego en vivo dice cincuenta."],
 "c25": ["Hay jugadores que llegan al cuarenta con apenas cincuenta de oro, y casi siempre es por esto: pequeños caprichos de diez y veinte de oro que, juntos, son una montura."],
 "c24": ["Y no tienes que farmear aparte: recolectas mientras haces tus misiones. Cada hierba y cada veta del camino es dinero que ya estaba en tu ruta.",
         "Eso sí, mira los precios: el cuero prístino, que en la beta se vendía a más de un oro, ya bajó a unas cinco platas. Lo raro deja de ser raro cuando todos lo recogen."],
 "c23": ["Y lo mismo con la venta: en la pestaña de vender, haces clic en el objeto, le das a la barra espaciadora, y el add-on lo publica con el precio correcto. Uno tras otro."],
 "c22": ["Y una buena noticia: Blizzard anunció que va a bajar el depósito mínimo de una plata a un cobre. Así publicar cosas baratas deja de doler."],
 "c21": ["Y los add-ons de subasta te avisan si tú mismo estás a punto de publicar algo por debajo del vendedor. Para no ser tú el que regala monedas."],
 "c20": ["Y como está siempre junto al buzón, ese personaje también recoge el oro de tus ventas sin que tu principal tenga que volver a la ciudad."],
 "c19": ["Y Chol\'aruk es una élite de nivel veinte: no la vas a poder hacer solo. Así que es también la excusa perfecta para juntar un grupo en el chat."],
 "c18": ["Para conseguir esos boletos, la ruta más barata son cincuenta pelambres de oso rasgadas y cinco péndolas vibrantes. Unos tres de oro en total.",
         "Y los vendedores de la Isla Zephras ya venden bolsas de profesión de aprendiz, para que las hierbas y los minerales no te ocupen la bolsa normal."],
 "c17": ["Pero ojo con el Monasterio Escarlata: cuando medio servidor entre ahí, va a llover seda, y el precio va a bajar. Vende antes de esa ola."],
 "c16": ["Y aunque no hagas la misión, las páginas te caen igual matando en la Vega. Así que, para un jugador de nivel cuarenta, son monedas que caen solas."],
 "c15": ["Y si tu habilidad es muy baja, compra un señuelo brillante en el vendedor de pesca, y ya no se te escapa casi nada en las zonas iniciales."],
 "c14": ["Y como la caña pide cien de habilidad para usarla, el que la compra suele ser un pescador serio, que paga lo que haga falta."],
 "c13": ["Y no solo vende esa receta: también tiene chile aliento de dragón, costillas de lobo picantes y algunos esquemas de ingeniería, todo en cantidades limitadas."],
 "c12": ["Los del trueno caen en el centro de Arathi, los blasonados al noreste y los ardientes al noroeste. Así que puedes ir de un campamento a otro sin dar vueltas."],
 "c11": ["Y cada almeja es como un pequeño cofre: aunque el precio baje, el botín de una tarde de buceo se vende mucho mejor que lo que te daría el vendedor."],
 "c10": ["Y la misión también pide carne de almeja sabrosa y queso de Alterac. Así que cuando los huevos caen, a veces la almeja es la que sube."],
 "c09": ["Y como esos grifos son de misión, reaparecen muy rápido. Puedes quedarte en un mismo punto y no parar de llenar la bolsa."],
 "c08": ["Sin profesiones, él calcula unos veinte de oro por hora solo con lo que paga el vendedor. Con desuello y minería, mucho más.",
         "Y esa perla de oro el vendedor la paga a un oro, pero en la subasta llegó a valer cinco. Por eso Auctionator siempre va primero."],
 "c07": ["Y si no quieres hacer cuentas cada vez, una regla sencilla: llena la primera caja de cada personaje, por la Shipping Label, y vende las demás que no te salgan a cuenta."],
 "c06": ["Hay quien piensa que el primero en tener la fórmula de encantar un collar va a poder cobrar lo que quiera. Y en un servidor nuevo, probablemente tenga razón."],
 "c05": ["El fuego elemental es otro clásico: en Classic pasó de cuarenta platas a dos de oro cuando abrieron las bandas. Y la tierra elemental ya está subiendo poco a poco.",
         "Y el cardopresto sube por el té de cardo de los pícaros, y ahora también de los druidas felinos. Cada clase nueva que lo usa es un comprador más."],
 "c04": ["Y en la costa de Tanaris, con algo más de habilidad, los restos flotantes dan todavía más. Un jugador calculó que pescando ahí habría sacado diez o veinte de oro extra por hora."],
 "c03": ["Y la tela vil no es solo para sastres: los brujos y los encantadores la buscan, así que siempre tiene comprador."],
 "c02": ["Y en ese mismo mercado negro, el Loto negro también tiene su techo de cincuenta de oro. Así que los dos objetos más caros de la recolección ya tienen un precio máximo conocido."],
 "c01": ["Y la cantidad de oro no cambia aunque ya seas sesenta. Así que no hay ninguna ventaja en guardarlas: cobras lo mismo hoy que mañana."],
 "cierre": ["Y recuerda que la economía de Forever tiene apenas dos semanas: todo lo que hoy vale, mañana puede valer la mitad. Sigue mirando la subasta."],
}
src = open("guion.py", encoding="utf-8").read()
for eid, frases in EXTRA.items():
    m = re.search(r'\{"id": \'%s\'.*?"frases": \[\n(.*?)\n    \]\}' % eid, src, re.S)
    assert m, eid
    lineas = m.group(1).split("\n")
    nuevas = lineas[:-1] + ["        %r," % f for f in frases] + lineas[-1:]
    src = src[:m.start(1)] + "\n".join(nuevas) + src[m.end(1):]
open("guion.py", "w", encoding="utf-8").write(src)
