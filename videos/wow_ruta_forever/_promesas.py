# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026): cuadro real (clip + capa de efectos) en el segundo en que la voz dice cada frase.
previews/promesas_NN.jpg (12 por hoja). Las frases y lo que debería verse: PROMESAS de abajo (copiadas a promesas.md).
Copiado de wow_oro_forever/_promesas.py (19-nov-2026).
    python _promesas.py            (desde la carpeta del video)   ·   python _promesas.py --md   (reescribe promesas.md)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py

PROMESAS = [   # (frase ancla, + s, qué debería verse)
    # gancho
    ("Una zona nueva con ciento cincuenta y una", 1.0, "banda Claros del Río"),
    ("Un Monte Hyjal que no empieza", 1.5, "pegatina Monte Hyjal"),
    ("Unos llegan a la zona nueva caminando", 1.0, "MG bifurcación A/H"),
    ("Llegar al sesenta pide cuatro millones", 2.5, "MG curva XP"),
    ("El primer sesenta de Forever lo hizo", 1.5, "grupo de 5 / primer 60"),
    ("Por eso hoy te traigo la ruta completa", 4.0, "mapa mundo 14 paradas"),
    ("un consejo de un espectador", 2.0, "comentario consejo"),
    # P1
    ("Parada uno. Del nivel uno al diez", 1.5, "tarjeta parada 1"),
    ("Cada raza empieza en su valle", 2.0, "mapa Elwynn Villanorte"),
    ("Los humanos bajan a Villadorada", 1.0, "Villadorada"),
    ("Los elfos de la noche, a Dolanaar", 1.2, "pegatina Dolanaar"),
    ("a Kharanos, entre la nieve", 0.8, "pegatina Kharanos"),
    ("bajan del Valle de los Retos a Cerrotajo", 1.0, "pegatina Cerrotajo"),
    ("al Poblado Pezuña de Sangre", 1.0, "pegatina Pezuña de Sangre"),
    ("Y los renegados, a Rémol", 0.8, "pegatina Rémol"),
    ("la Isla Zephras, donde empiezan", 1.5, "mapa Zephras"),
    ("los de la Alianza a Dalaran", 0.8, "mapa Zephras dirigibles"),
    ("Elwynn, contando Ventormenta", 1.5, "MG misiones nuevas"),
    ("el Fuerte de Bandarion", 1.0, "mapa Tirisfal Bandarion"),
    ("con Shari Stilwell, en Rémol", 0.8, "Shari Stilwell"),
    ("Hogger sigue siendo nivel once", 1.0, "reliquia Hogger"),
    # P2
    ("Parada dos. Del diez al quince", 1.5, "tarjeta parada 2"),
    ("con centro en la Colina del Centinela", 1.0, "mapa Páramos"),
    ("Los enanos y gnomos van a Loch Modan", 1.5, "mapa Loch Modan"),
    ("con centro en Auberdine", 0.8, "mapa Costa Oscura"),
    ("en Los Baldíos, en El Cruce", 1.0, "mapa Baldíos"),
    ("al Bosque de Argénteos, a El Sepulcro", 1.0, "mapa Argénteos"),
    ("El Salón de Señores Feudales", 1.5, "pegatina Salón"),
    ("las Ruinas de Lordaeron, del quince", 1.5, "pegatina Ruinas"),
    ("sube de El Cruce hacia Trinquete", 1.0, "Baldíos / Trinquete"),
    ("de la Colina al Arroyo de la Luna", 1.0, "mapa Páramos ruta"),
    ("la Bolsa de dormir acogedora", 1.0, "bolsa de dormir"),
    ("o en una torre quemada de Los Baldíos", 1.0, "torre quemada"),
    # P3
    ("Parada tres. Del quince al veinte", 1.5, "tarjeta parada 3"),
    ("con centro en Villa del Lago, junto al lago", 1.0, "pegatina Villa del Lago"),
    ("al Campamento Taurajo", 1.0, "mapa Baldíos Taurajo"),
    ("al Refugio Roca del Sol", 0.5, "Roca del Sol"),
    ("al Molino de Alther", 1.0, "mapa Crestagrana"),
    ("ahí está la Avanzada del Sur", 1.0, "mapa Avanzada del Sur"),
    ("son las Minas de la Muerte", 1.0, "pegatina Minas"),
    ("Para la Horda son las Cuevas de los Lamentos", 1.5, "pegatina Cuevas"),
    ("tu primera recompensa de Legado", 1.5, "juguete de Legado"),
    ("Vito nos escribió esto", 2.0, "comentario Vito"),
    # P4
    ("Parada cuatro. Del veinte", 1.5, "tarjeta parada 4"),
    ("con centro en Villa Oscura", 0.8, "Villa Oscura"),
    ("con centro en el Puerto de Menethil", 0.8, "Puerto de Menethil"),
    ("como el Refugio Faucedraco", 0.8, "mapa Humedales Faucedraco"),
    ("con centro en Astranaar", 0.8, "mapa Vallefresno"),
    ("un barco nuevo de Menethil a Costasur", 1.5, "barco Menethil"),
    ("con centro en el Molino Tarren", 0.8, "Molino Tarren"),
    ("al Puesto del Hachazo", 0.8, "mapa Hachazo"),
    ("alexafm nos escribió", 2.0, "comentario alexafm"),
    ("sal de Argénteos hacia el Molino Tarren", 1.5, "mapa Laderas"),
    ("el Castillo de Colmillo Oscuro", 1.0, "pegatina Colmillo"),
    ("y las Cavernas de Brazanegra", 0.8, "pegatina Brazanegra"),
    # P5
    ("Parada cinco. Del veinticinco", 1.5, "tarjeta parada 5"),
    ("con centro en el Poblado Viento Libre", 1.0, "pegatina Viento Libre"),
    ("puede entrar por Thalanaar", 1.0, "Thalanaar"),
    ("hacia los centauros del oeste", 0.5, "mapa Mil Agujas"),
    ("y termina en el Desierto de Sal", 0.8, "mapa Desierto de Sal"),
    ("el Sitio de Excavación de Los Humedales", 1.0, "mapa excavación"),
    ("raptores escondidos en la hierba alta", 1.0, "pegatina raptores"),
    ("el Horado Rajacieno, en el sur", 0.8, "clip Horado"),
    ("y Gnomeregan, en Dun Morogh", 0.8, "clip Gnomeregan"),
    ("Blizzard la subió un cincuenta", 1.0, "MG XP mazmorras"),
    # P6
    ("Parada seis. Del treinta al", 1.5, "tarjeta parada 6"),
    ("el Refugio de la Zaga en el centro", 1.0, "mapa Arathi"),
    ("y el Castillo de Stromgarde", 0.8, "mapa Stromgarde"),
    ("Rubén nos escribió que le encanta", 2.0, "comentario Rubén"),
    ("Dalaran vuelve a su sitio", 1.0, "pegatina Dalaran"),
    ("Y tiene mazmorra nueva: la Ciudad de Dalaran", 1.5, "mapa Alterac"),
    ("En Kalimdor, toca Desolace", 1.0, "mapa Desolace"),
    ("y la Horda en Aldea Cazasombras", 1.0, "mapa Cazasombras"),
    ("el Cementerio de Kodos", 0.8, "mapa Kodos"),
    ("el Monasterio Escarlata", 1.2, "mapa Monasterio"),
    # P7
    ("Parada siete. Del treinta y cinco", 1.5, "tarjeta parada 7"),
    ("entra por el Asentamiento Rebelde", 1.0, "mapa Tuercespina"),
    ("la Expedición de Nesingwary", 0.8, "mapa Nesingwary"),
    ("y la Arena Gurubashi", 0.8, "mapa Arena"),
    ("la Alianza tiene la Isla Theramore", 1.0, "pegatina Theramore"),
    ("la Horda tiene Kargath", 0.8, "pegatina Kargath"),
    ("Y en el Pantano de las Penas, Rocal", 1.0, "Rocal"),
    ("La Ciudad Anegada, del treinta y cinco", 1.0, "mapa Ciudad Anegada"),
    ("Tiene ocho misiones: la Horda las recoge", 1.5, "pegatina Ciudad Anegada"),
    ("se separa de la de Classic", 0.5, "MG bifurcación 38"),
    ("Y si vas a Uldaman", 1.0, "Uldaman"),
    ("SolidNano nos escribió", 2.0, "comentario SolidNano"),
    # P8
    ("Parada ocho. Del treinta y seis", 1.5, "tarjeta parada 8"),
    ("En inglés se llama Riverglades", 0.8, "banda Claros del Río"),
    ("Tiene ciento cincuenta y una misiones nuevas", 1.5, "MG contadores Claros"),
    ("La Alianza entra a pie", 0.6, "mapa Crestagrana salida"),
    ("cruza las Colinas Espinosas", 0.8, "mapa Colinas Espinosas"),
    ("hasta la Fortaleza de Farholde", 1.0, "mapa Farholde"),
    ("desde un muelle al este de Gadgetzan", 1.0, "mapa Tanaris muelle"),
    ("hasta el Puerto Polvomecha", 1.0, "mapa Polvomecha"),
    ("corre por la carretera hasta Rog'mar", 1.2, "mapa Rog'mar"),
    ("Desde Rog'mar vuelas a Rocal", 1.5, "vuelos de Rog'mar"),
    ("La ruta va por la Avanzada de Terral", 1.0, "mapa ruta Terral"),
    ("y Pedreg'ok, el pueblo de los ogros", 0.8, "mapa Pedreg'ok"),
    ("el Bastión de Krol'dok, del cuarenta", 1.0, "mapa Krol'dok"),
    ("Hazla una vez", 1.0, "pegatina Krol'dok"),
    ("Krol'dok iba a ser una mazmorra de gnolls", 1.0, "ogros"),
    ("tres lagos en forma de herradura", 1.0, "lagos herradura"),
    ("Sakaan nos escribió", 2.0, "comentario Sakaan"),
    ("Y Mateo, que lleva dieciocho", 2.0, "comentario Mateo"),
    # P9
    ("Parada nueve. Del treinta y ocho", 1.5, "tarjeta parada 9"),
    ("por el Valle de los Huesos, al sur", 1.0, "mapa Desolace Valle"),
    ("con Orgrul", 0.6, "mapa Orgrul"),
    ("al Mirador de Sombrapar", 0.8, "mapa Shen ruta"),
    ("Mordent Evenshade te espera", 1.0, "mapa Mordent"),
    ("deja tu piedra de hogar en Aldea Cazasombras", 1.5, "Cazasombras / Shen'dralas"),
    ("y Maraudon, en Desolace", 0.5, "clip Maraudon"),
    ("José Juan nos escribió", 2.0, "comentario José Juan"),
    # P10
    ("Parada diez. Del cuarenta al cuarenta y ocho", 1.5, "tarjeta parada 10"),
    ("la equitación, unos cien de oro", 1.0, "MG compras del 40"),
    ("comparten Gadgetzan", 1.0, "mapa Tanaris Gadgetzan"),
    ("en el Bastión Plumaluna", 1.0, "mapa Feralas"),
    ("sube a Pico Nidal", 1.0, "mapa Interior"),
    ("La ruta acaba en Jintha'Alor", 1.0, "mapa Jintha'Alor"),
    ("La mazmorra estrella es Zul'Farrak", 1.2, "mapa Zul'Farrak"),
    ("en Dalaran hay dos archimagos", 1.0, "carrusel Dalaran/Cima"),
    ("Pasa por ahí antes de cada mazmorra", 1.0, "Cima del Trueno"),
    ("misiones nuevas en el muelle de los goblins", 0.5, "muelle goblin Tanaris"),
    # P11
    ("Seguimos con la siguiente parada", 1.5, "tarjeta parada 11"),
    ("el famoso muro de los cincuenta", 1.0, "muro de los 50"),
    ("La primera es Azshara renovada", 1.0, "mapa Azshara"),
    ("un campamento de vanguardia thalassiano", 1.0, "mapa thalassiano"),
    ("La segunda es la Prisión de Alcaz", 1.0, "mapa Alcaz"),
    ("Y el Cráter de Un'Goro, al cuarenta y ocho", 1.0, "mapa Un'Goro"),
    ("también tienes La Garganta de Fuego", 1.0, "Garganta/Frondavil/Devastadas"),
    ("Y El Templo de Atal'Hakkar", 1.0, "mapa Atal'Hakkar"),
    # P12
    ("Parada doce. Del cincuenta", 1.5, "tarjeta parada 12"),
    ("la Alianza en la Vigilia de Morgan", 1.0, "mapa Estepas"),
    ("vuela directo a la Vigilia de Morgan", 0.5, "vuelo Farholde → Morgan"),
    ("en el Campamento del Orvallo", 0.8, "mapa Peste Oeste"),
    ("Profundidades de Roca Negra, del cincuenta", 1.0, "mapa Roca Negra"),
    ("Franclorn Forjador, sobre su tumba", 1.0, "mapa Franclorn"),
    ("la mayoría de las misiones ya dan oro", 1.0, "MG oro"),
    ("el Oso espectral", 1.0, "reliquia Oso espectral"),
    ("Lololulu dice que somos", 2.0, "comentario Lololulu"),
    ("Massimo nos contó", 2.0, "comentario Massimo"),
    ("Y Alexander, que con su vida", 2.0, "comentario Alexander"),
    ("Y al sargento Sevilla", 2.0, "comentario Sevilla"),
    # P13
    ("Parada trece. Del cincuenta y tres", 1.5, "tarjeta parada 13"),
    ("el centro es Vista Eterna", 1.0, "mapa Cuna"),
    ("a la Aldea Estrella Fugaz", 1.0, "mapa Estrella Fugaz"),
    ("el centro es el Fuerte Cenarion", 1.0, "pegatina Fuerte Cenarion"),
    ("la Capilla de la Esperanza de la Luz, con vuelo", 1.0, "pegatina Capilla"),
    ("es el Bastión Faucenegra, del cincuenta y cinco", 1.0, "mapa Faucenegra"),
    ("el Bastión Fauces de Madera", 1.0, "Fauces de Madera"),
    ("entradas a las Cavernas del Túmulo", 1.0, "pegatina Túmulo"),
    ("En la Capilla tienes, además", 1.5, "mapa Peste del Este"),
    # P14
    ("Parada catorce, la última", 1.5, "tarjeta parada 14"),
    ("Sus ciento cuarenta y tres misiones", 1.5, "MG Hyjal"),
    ("por la Garganta Negro Rumor. Y desde", 0.6, "mapa Cuna → Hyjal"),
    ("como Aviana, de vuelta", 0.5, "pegatina Hyjal"),
    ("al Santuario de Aviana", 0.8, "mapa Hyjal"),
    ("El Bancal del Creador, del cincuenta", 1.0, "pegatina Bancal"),
    ("y la Guarida de Onyxia", 0.8, "carrusel bandas"),
    ("Y esa es la ruta completa", 3.0, "mapa mundo cierre"),
]


def md():
    with open("promesas.md", "w", encoding="utf-8") as f:
        f.write("# Promesas visuales — wow_ruta_forever\n\n| frase | +s | cómo se ve |\n|---|---|---|\n")
        for fr, dt, q in PROMESAS:
            f.write(f"| {fr} | {dt} | {q} |\n")


def main():
    import secuencia_fx as SF
    capa = SF.cargar()
    S = capa.S
    minis = []
    mw, mh = 480, 270
    filas = []
    for frase, dt, que in PROMESAS:
        try:
            t = capa.ancla(frase) + dt
        except BaseException as e:
            print("NO ENCONTRADA:", frase, e)
            continue
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{len(minis) + 1} {int(t // 60)}:{t % 60:04.1f} {b['id'][6:]} {que}"
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, .5, (90, 214, 255), 1,
                    cv2.LINE_AA)
        minis.append(m)
        filas.append((frase, t, b["id"], que))
    cols, n = 4, 12
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/promesas_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)
    for i, (frase, t, bid, que) in enumerate(filas):
        print(f"{i + 1}\t{int(t // 60)}:{t % 60:04.1f}\t{bid}\t{frase}\t{que}")


if __name__ == "__main__":
    if "--md" in sys.argv:
        md()
    else:
        main()
