# -*- coding: utf-8 -*-
"""Añade a efectos.py los 13 mapas con ruta pedidos por el usuario (29-oct-2026: «al menos la mitad de las misiones con mapa de
donde inician y sus objetivos, con sus rutas») y quita las pegatinas/fichas que duplicaban la foto de los puntos del mapa.
Coordenadas REALES: base de datos del mapa de UESP calibrada sobre el mapa de papel (_coords_uesp.py). Se ejecuta una vez."""
import os

F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "efectos.py")
t = open(F, encoding="utf-8").read()


def cambia(viejo, nuevo):
    global t
    assert t.count(viejo) == 1, viejo[:70]
    t = t.replace(viejo, nuevo)


def quita(linea_ini):
    """Quita el efecto (una o dos líneas) que empieza por linea_ini."""
    global t
    i = t.index(linea_ini)
    j = t.index("\n", i)
    while t[j + 1:j + 11].startswith("          ") or t[j + 1:].startswith("       "):
        j = t.index("\n", j + 1)
    t = t[:i] + t[j + 1:]


M = 'titulo="Skyrim", '
# --- 25 · Riften → Avanchnzel
quita('    grande("aparece una argoniana"')
quita('    peg("Te pide que lleves un léxico"')
cambia('    peg("Breya muere junto a un centurión"',
       '    mapa("skyrim", [(.89, .78, "Riften · muelles", "inicio", P("fathoms")), (.84, .82),\n'
       '                    (.774, .814, "Avanchnzel", "meta", P("lexicon"))],\n'
       '         de="en los muelles de Riften", a=("en las montañas de Jerall|fin", .8),\n'
       '         marcas=["en los muelles de Riften", "lleves un léxico a Avanchnzel"], ' + M + 'sub="Simas insondables", ajuste=.6),\n'
       '    peg("Breya muere junto a un centurión"')
# --- 23 · Límite Sombrío (Alftand) → granja Sarethi
quita('    ficha("Juntar treinta raíces"')
quita('    peg("Avrusa Sarethi"')
cambia('    ficha("El premio es Descubrimiento"',
       '    mapa("skyrim", [(.663, .281, "Límite Sombrío · entrada de Alftand", "inicio", P("nirn_carmesi")), (.70, .45), (.72, .60),\n'
       '                    (.750, .709, "Granja Sarethi · Avrusa", "meta", P("avrusa"))],\n'
       '         de="Juntar treinta raíces", a=("a su granja cerca de Riften|fin", .8),\n'
       '         marcas=["Juntar treinta raíces", "Avrusa Sarethi"], ' + M + 'sub="Vuelta a las raíces", ajuste=.6),\n'
       '    ficha("El premio es Descubrimiento"')
# --- 22 · Kyne: Choza de Froki real (UESP)
cambia('(.68, .73, "Choza de Froki", "inicio", P("froki")), (.62, .62)', '(.715, .798, "Choza de Froki", "inicio", P("froki")), (.64, .66)')
# --- 21 · Soledad → Respiro del Muerto
quita('    peg("Viarmo te manda"')
cambia('    grande("Olaf Ojo Único ejecutó"',
       '    mapa("skyrim", [(.33, .20, "Soledad · Colegio de Bardos", "inicio", P("viarmo")), (.35, .28),\n'
       '                    (.341, .351, "Respiro del Muerto · el verso", "meta", P("olaf"))],\n'
       '         de="Para entrar en el Colegio", a=("en el Respiro del Muerto|fin", 1.8),\n'
       '         marcas=["Colegio de Bardos de Soledad", "en el Respiro del Muerto"], ' + M + 'sub="Que no se apaguen las llamas", ajuste=.6),\n'
       '    grande("Olaf Ojo Único ejecutó"')
# --- 20 · Carrera Blanca → Guarida de los Timadores
quita('    ficha("Pagas la multa"')
cambia('    ficha("se puede cobrar a los dos"',
       '    mapa("skyrim", [(.545, .49, "Carrera Blanca · Saadia", "inicio", P("saadia")), (.47, .50),\n'
       '                    (.392, .498, "Guarida de los Timadores · Kematu", "peligro", P("kematu"))],\n'
       '         de="Para hablar con su jefe", a=("El guarda pierde las llaves|fin", .5),\n'
       '         marcas=["Para hablar con su jefe", "Pagas la multa"], ' + M + 'sub="En tiempos de necesidad", ajuste=.6),\n'
       '    ficha("se puede cobrar a los dos"')
# --- 18 · Ventalia → Cueva abandonada
quita('    peg("custodiado por un draugr"')
cambia('    peg("Su aprendiz Quinto Navale"',
       '    mapa("skyrim", [(.78, .42, "Ventalia · Nurelion", "inicio", P("nurelion")), (.73, .38),\n'
       '                    (.684, .359, "Cueva abandonada · Curalmil", "meta", P("vial"))],\n'
       '         de="Lo encuentras en la Cueva", a=("Y está roto|fin", .8),\n'
       '         marcas=["Lo encuentras en la Cueva", "custodiado por un draugr"], ' + M + 'sub="El Vial Blanco", ajuste=.6),\n'
       '    peg("Su aprendiz Quinto Navale"')
# --- 17 · Carrera Blanca → Bastión de la Guardia del Norte
cambia('    peg("convenciendo a Idolaf"',
       '    mapa("skyrim", [(.545, .49, "Carrera Blanca · Fralia", "inicio", P("fralia")), (.42, .40), (.30, .29), (.22, .21),\n'
       '                    (.165, .165, "Bastión de la Guardia del Norte · Thorald", "meta", P("thorald"))],\n'
       '         de="Lo tienen preso los thalmor", a=("en el Bastión de la Guardia del Norte|fin", 2.0),\n'
       '         marcas=["Lo tienen preso los thalmor", "en el Bastión de la Guardia del Norte"], ' + M
       + 'sub="Desaparecido en acto de servicio", ajuste=.5, traza=99),\n'
       '    peg("convenciendo a Idolaf"')
# --- 16 · Reducto del Águila Roja → Torres Hendidas → túmulo
quita('    peg("Recuperas la espada"')
cambia('    ficha("Diez de fuego y los no muertos"',
       '    mapa("skyrim", [(.214, .459, "Reducto del Águila Roja", "inicio", P("aguila_roja")),\n'
       '                    (.230, .423, "Torres Hendidas · la espada", "paso", P("furia_aguila")),\n'
       '                    (.249, .437, "Túmulo del Rebelde", "meta", None)],\n'
       '         de=("Recuperas la espada", -.4), a=("y la llevas a su túmulo|fin", 2.0),\n'
       '         marcas=["Recuperas la espada", "en las Torres Hendidas", "y la llevas a su túmulo"], ' + M
       + 'sub="La leyenda de Águila Roja", ajuste=.5),\n'
       '    ficha("Diez de fuego y los no muertos"')
# --- 8 · Forja del Cielo → Tumba de Ysgramor
quita('    peg("con el hacha Wuuthrad"')
cambia('    peg("una cabeza de bruja de Glenmoril"',
       '    mapa("skyrim", [(.545, .49, "Carrera Blanca · Forja del Cielo", "inicio", P("kodlak")), (.62, .38), (.68, .26),\n'
       '                    (.696, .156, "Tumba de Ysgramor", "meta", P("wuuthrad"))],\n'
       '         de="Para liberarla vas a la Tumba", a=("en la Forja del Cielo|fin", 1.0),\n'
       '         marcas=["Para liberarla vas", "a la Tumba de Ysgramor"], ' + M + 'sub="La gloria de los muertos", ajuste=.5, traza=99),\n'
       '    peg("una cabeza de bruja de Glenmoril"')
# --- 7 · estatua de Meridia → Ruinas de Kilkreath
quita('    grande("Y Meridia te eleva"')
quita('    peg("un nigromante Malkoran"')
cambia('    ficha("cuarenta y tres cadáveres"',
       '    mapa("skyrim", [(.278, .218, "Monte Kilkreath · estatua de Meridia", "inicio", P("meridia")),\n'
       '                    (.292, .211, "Ruinas de Kilkreath · Malkoran", "meta", P("malkoran"))],\n'
       '         de="Te lleva al Monte Kilkreath", a=("de pedestal en pedestal|fin", .8),\n'
       '         marcas=["Te lleva al Monte Kilkreath", "Te manda limpiar su templo"], ' + M + 'sub="Al alba", ajuste=.4),\n'
       '    ficha("cuarenta y tres cadáveres"')
# --- 6 · Soledad → Cueva Cráneo de Lobo
quita('    peg("Falk Barba de Fuego"')
cambia('    grande("resucitar a Potema"',
       '    mapa("skyrim", [(.33, .20, "Soledad · Falk Barba de Fuego", "inicio", P("falk")),\n'
       '                    (.270, .194, "Cueva Cráneo de Lobo", "peligro", P("potema"))],\n'
       '         de="En Soledad Falk Barba", a=("Parece una falsa alarma|fin", 1.0),\n'
       '         marcas=["En Soledad Falk Barba", "en la Cueva Cráneo de Lobo"], ' + M + 'sub="El despertar de la Reina Loba", ajuste=.4),\n'
       '    grande("resucitar a Potema"')
# --- 5 · Riften → Última Vigilia
cambia('    ficha("dos mil setenta y uno"',
       '    mapa("skyrim", [(.89, .78, "Riften", "inicio", None),\n'
       '                    (.934, .719, "Última Vigilia", "peligro", P("guerrero_ebano"))],\n'
       '         de="Te espera en la Última Vigilia", a=("hasta que le pegas tú|fin", .6),\n'
       '         marcas=["Te espera en la Última Vigilia", ("Te espera en la Última Vigilia", 1.2)], ' + M
       + 'sub="El guerrero de ébano", ajuste=.4),\n'
       '    ficha("dos mil setenta y uno"')
# --- 4 · Puesto de Séptimo Signo → Alftand (bajada al Límite Sombrío)
cambia('    grande("El Oghma Infinium"',
       '    mapa("skyrim", [(.740, .097, "Puesto de Séptimo Signo", "inicio", P("septimo")), (.70, .19),\n'
       '                    (.663, .281, "Alftand · bajada al Límite Sombrío", "meta", None)],\n'
       '         de="Te manda al Límite Sombrío", a=("a leer un Pergamino antiguo|fin", 1.0),\n'
       '         marcas=["Te manda al Límite Sombrío", "a la Torre de Mzark"], ' + M + 'sub="Descifrar lo transmundano", ajuste=.5),\n'
       '    grande("El Oghma Infinium"')
# --- 3 · Gauldur: coordenadas reales (UESP)
cambia('(.38, .27, "Folgunthur · Mikrul", "inicio", P("mikrul")), (.50, .24), (.62, .22),',
       '(.381, .240, "Folgunthur · Mikrul", "inicio", P("mikrul")), (.50, .23), (.62, .22),')
cambia('(.72, .22, "Saarthal · Jyrik", "paso", P("jyrik")), (.74, .40), (.72, .58),',
       '(.692, .239, "Saarthal · Jyrik", "paso", P("jyrik")), (.74, .40), (.72, .58),')
cambia('(.70, .69, "Sala de Geirmund · Sigdis", "paso", P("sigdis")), (.55, .64), (.35, .60), (.22, .56),',
       '(.698, .691, "Sala de Geirmund · Sigdis", "paso", P("sigdis")), (.55, .64), (.35, .60), (.22, .55),')
cambia('(.16, .55, "Roca de la Cuenca · Gauldur", "meta", P("gauldur"))',
       '(.182, .514, "Roca de la Cuenca · Gauldur", "meta", P("gauldur"))')
# --- 2 · Cueva de Sima Negra (ventana)
quita('    peg("un caballero Gelebor"')
cambia('    grande("el Archicoadjutor Vyrthur"',
       '    mapa("skyrim", [(.146, .294, "Cueva de Sima Negra · Gelebor", "meta", P("gelebor"))],\n'
       '         de=("Con Serana llegas", .8), a=("te abre un pasaje|fin", .8), marcas=["la Cueva de Sima Negra"], ' + M
       + 'sub="Tocando el cielo", ventana=True),\n'
       '    grande("el Archicoadjutor Vyrthur"')

t = t.replace("- Mapas reales (tema tes) con FOTO de cada paso: las cacerías de Kyne (22) y los tres hijos de Gauldur (3).",
              "- Mapas reales (tema tes) con FOTO de cada paso y ruta, en 15 de las 25 misiones (el usuario, 29-oct-2026: «al menos la\n"
              "  mitad, con donde inician y sus objetivos»): 25, 23, 22, 21, 20, 18, 17, 16, 8, 7, 6, 5, 4, 3 y 2 (ventana).\n"
              "  Coordenadas reales de la base de datos del mapa de UESP calibradas sobre el mapa de papel (`_coords_uesp.py`).")
open(F, "w", encoding="utf-8").write(t)
print("ok:", t.count('mapa("skyrim"'), "mapas")
