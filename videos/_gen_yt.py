# -*- coding: utf-8 -*-
"""Escribe youtube.json de los 5 Shorts de ciencia."""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
V = {
    "platano_radiactivo": dict(
        titulo="Tu plátano es radiactivo #Shorts",
        alt=["¿Por qué los plátanos son radiactivos? #Shorts", "Comer un plátano es comer radiación #Shorts"],
        desc="Hay algo radiactivo en tu cocina, y seguro lo has comido: un plátano. Tiene potasio, y una pequeñísima parte de ese potasio (potasio-40) es radiactiva: unos quince átomos se desintegran cada segundo en un plátano. Una radiografía dental equivale a comer unos cincuenta plátanos, y tu propio cuerpo emite unas cuatro mil desintegraciones por segundo. Tranquilo: el plátano es inocente.\n\n📚 FUENTES\n• Potasio-40 (0,0117 % del potasio natural) y actividad de un plátano (~15 Bq): Health Physics Society · Oak Ridge Associated Universities (ORAU)\n• «Dosis equivalente de plátano» (~0,1 µSv) y radiografía dental (~5 µSv): ORAU · EPA\n• Cuerpo humano (~4 000 Bq de K-40): Health Physics Society\n\nAnimación original en boceto y guache. Las cifras son órdenes de magnitud.\n\n#Shorts #Ciencia #Radiactividad",
        tags=["platano radiactivo", "potasio 40", "radiactividad", "dosis equivalente de platano", "ciencia en 1 minuto", "datos curiosos", "fisica", "shorts de ciencia", "ciencia animada", "radiacion natural", "banana equivalent dose"]),
    "luna_se_aleja": dict(
        titulo="La Luna se está yendo #Shorts",
        alt=["La Luna se aleja 4 cm cada año #Shorts", "Los días se alargan por la Luna #Shorts"],
        desc="La Luna se está alejando de la Tierra unos cuatro centímetros por año, lo mismo que crecen tus uñas. Lo sabemos porque los astronautas dejaron espejos en su superficie y desde la Tierra les disparamos láseres. Las mareas empujan a la Luna hacia afuera y frenan a la Tierra: los días se alargan unos milisegundos por siglo. Hace 400 millones de años un día duraba unas 22 horas. Y dentro de unos 600 millones de años ya no habrá eclipses totales de Sol.\n\n📚 FUENTES\n• Recesión lunar (~3,8 cm/año), medidas láser a los retrorreflectores de Apolo: NASA · Observatoire de la Côte d'Azur (LLR)\n• Alargamiento del día (~1,7 ms por siglo) y días de ~22 h hace ~400 millones de años (corales y ritmitas fósiles): Britannica · Williams, 2000\n• Fin de los eclipses totales (~600 millones de años): NASA\n\nAnimación original en boceto y guache.\n\n#Shorts #Luna #Astronomía",
        tags=["la luna se aleja", "luna se aleja de la tierra", "dias mas largos", "eclipse total", "retrorreflectores apolo", "mareas", "astronomia", "ciencia en 1 minuto", "shorts de ciencia", "datos curiosos", "ciencia animada"]),
    "peso_nube": dict(
        titulo="¿Cuánto pesa una nube? #Shorts",
        alt=["Una nube pesa como 80 elefantes #Shorts", "¿Por qué las nubes no se caen? #Shorts"],
        desc="Una nube pesa lo mismo que ochenta elefantes, y aun así flota. Una nube normal de verano tiene unas quinientas toneladas de agua (medio millón de litros), repartida en miles de millones de gotitas tan pequeñas que caen a menos de un centímetro por segundo. Además, el aire caliente que sube desde el suelo las sostiene. Cuando las gotas se juntan y se hacen grandes, pesan demasiado y llueve.\n\n📚 FUENTES\n• Masa de un cúmulo (~500 toneladas): Margaret LeMone, NCAR/UCAR\n• Tamaño y velocidad de caída de las gotas de nube: NOAA · Britannica\n• Corrientes ascendentes (térmicas) y formación de lluvia: NOAA National Weather Service\n• Elefante africano ~6 toneladas.\n\nAnimación original en boceto y guache.\n\n#Shorts #Nubes #Ciencia",
        tags=["cuanto pesa una nube", "peso de una nube", "por que flotan las nubes", "nubes", "lluvia", "80 elefantes", "ciencia en 1 minuto", "datos curiosos", "meteorologia", "shorts de ciencia", "ciencia animada"]),
    "dedos_arrugados": dict(
        titulo="¿Por qué se arrugan los dedos en el agua? #Shorts",
        alt=["Tus dedos se arrugan A PROPÓSITO #Shorts", "El truco antideslizante de tus dedos #Shorts"],
        desc="Tus dedos se arrugan en el agua, y no es porque se empapen: lo ordena tu sistema nervioso, que contrae los vasos sanguíneos de la yema. Las arrugas funcionan como las ranuras de un neumático: canalizan el agua y mejoran el agarre. En experimentos, la gente con dedos arrugados manipulaba objetos mojados más rápido; con objetos secos no había diferencia.\n\n📚 FUENTES\n• Arrugas por vasoconstricción (sistema nervioso simpático): Wilder-Smith, 2004 · Changizi et al., 2011\n• Mejor agarre de objetos mojados con dedos arrugados: Kareklas, Nettle y Smulders, 2013, Biology Letters\n\nAnimación original en boceto y guache. La explicación evolutiva sigue siendo una hipótesis.\n\n#Shorts #Ciencia #CuerpoHumano",
        tags=["por que se arrugan los dedos", "dedos arrugados", "dedos arrugados en el agua", "sistema nervioso", "neumatico", "cuerpo humano", "ciencia en 1 minuto", "datos curiosos", "biologia", "shorts de ciencia", "ciencia animada"]),
    "cielo_azul": dict(
        titulo="¿Por qué el cielo es azul? #Shorts",
        alt=["El cielo no es azul, es violeta #Shorts", "¿Por qué los atardeceres son rojos? #Shorts"],
        desc="El cielo no es azul: en realidad deberías verlo violeta. La luz del Sol lleva todos los colores mezclados; al chocar con el aire, los colores de onda corta (azul y violeta) se dispersan por todo el cielo y el rojo casi pasa de largo. El violeta se dispersa más, pero el Sol emite menos violeta, la atmósfera absorbe parte y nuestros ojos lo ven peor: gana el azul. Al atardecer la luz atraviesa mucho más aire y el azul se pierde por el camino. En Marte es al revés: el cielo es rojizo de día y azul al atardecer.\n\n📚 FUENTES\n• Dispersión de Rayleigh (proporcional a 1/λ⁴): NASA · Britannica\n• Sensibilidad del ojo al violeta y emisión solar: NASA\n• Cielo de Marte (rojizo de día, azulado al atardecer): NASA/JPL (rovers)\n\nAnimación original en boceto y guache.\n\n#Shorts #Ciencia #Cielo",
        tags=["por que el cielo es azul", "cielo azul", "cielo violeta", "dispersion de rayleigh", "atardecer rojo", "cielo de marte", "ciencia en 1 minuto", "datos curiosos", "fisica", "shorts de ciencia", "ciencia animada"]),
}
for nombre, d in V.items():
    j = dict(titulo=d["titulo"], titulos_alternativos=d["alt"], descripcion=d["desc"], etiquetas=d["tags"], categoria=27, idioma="es", idioma_audio="es",
             para_ninos=False)
    arch = json.load(open(os.path.join(AQUI, nombre, "guion.py"), encoding="utf-8").read() and open(os.path.join(AQUI, nombre, "timeline.json"), encoding="utf-8")) and None
    import importlib.util
    spec = importlib.util.spec_from_file_location("g_" + nombre, os.path.join(AQUI, nombre, "guion.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    j["subtitulos"] = f"salida/{g.ARCHIVO}.srt"
    json.dump(j, open(os.path.join(AQUI, nombre, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(nombre, len(d["titulo"]), j["subtitulos"])
