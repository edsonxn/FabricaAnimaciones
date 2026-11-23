# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026) + ESCENAS IMPORTANTES (regla 18-nov-2026) de er_rykard_atrocidades.
Cuadro real (clip + capa de efectos) en el segundo en que la voz lo dice → previews/promesas_NN.jpg (12 por hoja),
y escribe promesas.md y escenas.md.      python _promesas.py            (desde la carpeta del video)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py
import secuencia_fx as SF  # noqa: E402

# (frase ancla, + s, qué debería verse, cómo se ve, escena importante)
PROMESAS = [
    ("Pretor Rykard", 1.0, "Rykard", "clip 001 + banda rykard", 0),
    ("Hijo de la reina Rennala", .6, "Rennala y Radagon, hijos", "MG linaje", 0),
    ("y dueño de la Mansión del Volcán", .8, "Mansión del Volcán", "pantalla mansion_exterior", 0),
    ("en lo alto del monte Gelmir", 1.0, "monte Gelmir", "mapa con foto mansion_wiki", 0),
    ("el semidiós que se dejó comer", 1.0, "la serpiente gigante", "pegatina serpiente + clip 003", 0),
    ("únete a la familia", .8, "Rykard grita «Únete a la familia»", "mensaje + clip 004 (pelea con Rykard)", 1),
    ("Antes de la serpiente fue juez", 1.0, "taller de tortura", "MG inquisicion", 0),
    ("Hay máquinas que secuestran", 1.0, "máquinas de secuestro", "MG red_secuestro", 0),
    ("Y dejó tirada la guerra", 1.0, "la guerra abandonada", "MG estandarte_caido", 0),
    ("contra uno de los jefes más difíciles", .6, "Maliketh", "camafeo maliketh + clip 007", 0),
    ("Era un pago", .8, "un pago", "MG recibo", 0),
    ("Héctor lleva siete intentos", 1.0, "comentario de Héctor", "tarjeta com_", 0),
    ("Otro usuario nos lleva la cuenta", 1.0, "comentario de uueee", "tarjeta com_", 0),
    ("Y Zohar nos pidió cerrar", 1.0, "comentario de Zohar", "tarjeta com_", 0),
    ("cerrar la trilogía", 1.2, "Ranni, Radahn, Rykard", "abanico", 0),
    ("los contratos de asesinato de Tanith", .6, "Tanith", "camafeo tanith", 0),
    ("En el video de Godfrey, alguien", 1.0, "comentario de m0h4xd", "tarjeta com_", 0),
    ("Messmer también exterminaba", .6, "Messmer", "camafeo messmer", 0),
    ("Los gigantes fueron cosa de Godfrey", .6, "Godfrey", "camafeo godfrey", 0),
    ("Lo dice su propia corona", 1.0, "Corona de Señor del Círculo", "reliquia + ficha", 0),
    ("Número cinco", 1.0, "puesto 5", "puesto", 0),
    ("Rykard era la ley", .6, "retrato de Rykard", "pegatina retrato_rykard_wiki (museo)", 0),
    ("En la Mesa Redonda, Gideon", .8, "Mesa Redonda", "camafeo mesa_redonda", 0),
    ("el Omnisciente, te lo describe", .6, "Gideon Ofnir", "pegatina gideon + clip 020", 0),
    ("El casco de sus caballeros de Gelmir", 1.0, "Casco de caballero de Gelmir", "reliquia + ficha + clip 022", 0),
    ("El rojo de Radagon", .8, "Radagon", "camafeo radagon", 0),
    ("La Mansión del Volcán parece un palacio", .8, "Mansión del Volcán por dentro", "pantalla mansion_wiki", 0),
    ("una anfitriona amable", .5, "Tanith", "camafeo tanith", 0),
    ("Uno se llama Iglesia", 1.0, "Iglesia de la ciudad de los penados", "pantalla iglesia_penados + banda", 0),
    ("Otro, Cámara subterránea", 1.0, "Cámara subterránea de la inquisición", "pantalla camara_inquisicion + banda", 0),
    ("lo cuenta todo. El Candelabro", 1.2, "Candelabro de inquisidor", "reliquia + ficha", 0),
    ("el inquisidor Ghiza, armado", .8, "Ghiza", "pegatina grande ghiza + clip 032", 1),
    ("La Rueda de Ghiza es un instrumento", 1.0, "Rueda de Ghiza", "reliquia + ficha + clip 033", 0),
    ("con la Máscara ensangrentada", .8, "Máscara ensangrentada", "pegatina + ficha", 0),
    ("Y su ropa es el Atuendo", .8, "Atuendo de oficial", "reliquia + ficha", 0),
    ("Número cuatro", 1.0, "puesto 4", "puesto", 0),
    ("en Liurnia, un personaje", 1.0, "Academia de Raya Lucaria", "mapa con foto raya_lucaria", 0),
    ("Es Parches, el mismo", .8, "Parches", "pegatina grande + clip 040", 0),
    ("Te habla de las vírgenes", .8, "virgen raptora", "pegatina + clip 041", 0),
    ("en el fondo de la gran noria", .8, "la noria de la Academia", "pantalla virgen_noria", 0),
    ("La virgen raptora abre el pecho", 1.0, "la virgen te atrapa", "banda + clip 045 (agarre)", 1),
    ("Y despiertas encerrado", 1.2, "despiertas en la cámara", "mapa Raya → Mansión + clip 046/047", 1),
    ("Sin poder salir y sin poder viajar", 1.0, "Cámara de la inquisición", "pantalla camara_wiki", 0),
    ("Una gira con ruedas dentadas", .8, "dos vírgenes raptoras", "clip 048 (pelea)", 1),
    ("te dejan su premio", .8, "Candelabro de inquisidor", "reliquia", 0),
    ("La descripción completa de la Rueda", 1.0, "Rueda de Ghiza", "reliquia + ficha", 0),
    ("en la Mansión de los Caria", .6, "red de vírgenes en el mapa", "mapa con 4 puntos", 0),
    ("En la cámara de la inquisición de Rykard", .4, "adónde van los pasajeros", "MG red_secuestro", 0),
    ("Y Parches lo sabía", .8, "Parches", "legajo parches + clip 056", 0),
    ("te empuja por un precipicio", .8, "Parches te empuja", "pantalla gelmir + clip 058", 1),
    ("Braulio dice que se volvió adicto", 1.0, "comentario de Braulio", "tarjeta com_", 0),
    ("Y Juan José dice que se han vuelto", 1.0, "comentario de Juan José", "tarjeta com_", 0),
    ("Número tres", 1.0, "puesto 3", "puesto", 0),
    ("el monte Gelmir, al oeste", 1.0, "Monte Gelmir en el mapa", "mapa Leyndell → Gelmir", 0),
    ("Junto al noveno campamento", 1.2, "monumento con espada", "pantalla monumento_asalto (zoom sin inglés)", 0),
    ("El asalto a la Mansión del Volcán", 1.0, "la inscripción del monumento", "mensaje del suelo", 0),
    ("La Gran Runa de Rykard lo cuenta", 1.0, "Gran Runa de Rykard", "reliquia + ficha", 0),
    ("se lo entregó a la boca", .6, "la serpiente traga a Rykard", "MG domino + clip 073", 1),
    ("En el camino que sube a la mansión", 1.0, "alma estancada del caballero", "pantalla almas_camino", 0),
    ("La Armadura de caballero de Gelmir lo deja", 1.0, "Armadura de caballero de Gelmir", "reliquia + ficha", 0),
    ("El Cazador de serpientes, una lanza", 1.0, "Cazador de serpientes", "reliquia + ficha", 0),
    ("Clavada en un montón de cadáveres", .8, "la lanza en los cadáveres", "pantalla cadaveres_cazador", 0),
    ("aparece el fantasma de un caballero", .8, "fantasma del caballero de Gelmir", "pegatina casco + clip 083", 1),
    ("Y cuando lo haces, en el sitio", 1.0, "arena de Rykard", "pantalla arena_rykard", 0),
    ("La Hoja blasfema, la espada", 1.0, "Hoja blasfema", "reliquia + ficha + clip 090", 0),
    ("con el Sobretodo ocular", .8, "Sobretodo ocular", "pegatina + ficha", 0),
    ("Y así es como Rykard te invita", 1.0, "Rykard", "banda rykard_jefe + clip 094", 0),
    ("en su propia voz. Escúchalo|fin", 3.0, "se OYE «Join the Serpent King»", "clip 095 + PISTA s_rykard + rótulo", 1),
    ("Yuzo nos preguntó", 1.0, "comentario de Yuzo", "tarjeta com_", 0),
    ("lo más artificial sigue siendo", .8, "Tanith", "pegatina grande tanith", 0),
    ("Número dos", 1.0, "puesto 2", "puesto", 0),
    ("los hombres serpiente, con látigos", .6, "hombre serpiente", "pegatina grande + clip 102", 0),
    ("Sus cenizas de espíritu cuentan", 1.0, "Cenizas de hombre serpiente", "reliquia + ficha", 0),
    ("El Disparo de magma dice", .8, "Disparo de magma", "reliquia + ficha", 0),
    ("De esa religión queda la Espada curva", 1.0, "Espada curva de dios serpiente", "reliquia + ficha", 0),
    ("Ahora entra en el Templo de Eiglay", 1.0, "Templo de Eiglay", "pantalla eiglay + banda", 0),
    ("Sobre el altar cuelga", 1.0, "piel de serpiente mudada", "pantalla altar_eiglay", 0),
    ("después de matar al Noble sacrodermo", .6, "Noble sacrodermo", "camafeo", 0),
    ("encuentras un objeto húmedo", .8, "Amnios de serpiente", "reliquia amnios", 0),
    ("Rya, la chica de Liurnia", .8, "Rya", "pegatina grande rya + clip 113", 0),
    ("Y cuando por fin se ve a sí misma", 1.0, "Rya en su forma de serpiente", "pantalla rya_serpiente + clip 117", 1),
    ("cuando le llevas el amnios", 1.0, "Rya reconoce el amnios", "reliquia + ficha + clip 119", 1),
    ("de ese cuerpo maldito. Escúchala|fin", 1.0, "se OYE «Kill me, please»", "clip 123 + PISTA s_rya + rótulo", 1),
    ("sus últimas palabras son para ti", .6, "muerte de Rya", "clip 124 + rótulo adalid", 1),
    ("te deja una carta", .8, "Carta de Zorayas", "reliquia + ficha", 0),
    ("Y la Ira de Gelmir, el hechizo", 1.0, "Ira de Gelmir", "reliquia + ficha", 0),
    ("el hechizo que te regala Bernahl", .5, "Bernahl", "camafeo bernahl", 0),
    ("Andrés escribió que Miquella", 1.0, "comentario de Andrés", "tarjeta com_", 0),
    ("ese es el encanto de Miquella", .5, "Miquella", "camafeo miquella", 0),
    ("Otro nos conoció con el video de Morgott", 1.0, "comentario de D424", "tarjeta com_", 0),
    ("Evil Ryu dice que este fue", 1.0, "comentario de Evil Ryu", "tarjeta com_", 0),
    ("Y Kanintor encontró el canal", 1.0, "comentario de Kanintor", "tarjeta com_", 0),
    ("Y Wsefsd celebró", 1.0, "comentario de Wsefsd", "tarjeta com_", 0),
    ("solo siete están suscritos", .3, "7 de cada 100", "MG cien", 0),
    ("Número uno#3", 1.0, "puesto 1", "puesto", 0),
    ("Al final del juego, en Farum Azula", 1.0, "Farum Azula", "mapa con foto farum_wiki", 0),
    ("suelta una losa con una garra grabada", .8, "Garra blasfema", "reliquia", 0),
    ("el combate contra Maliketh", .8, "Garra blasfema contra Maliketh", "pantalla garra_maliketh + camafeo", 1),
    ("Ranni recompensó con estos", .6, "Ranni", "camafeo ranni + ficha", 0),
    ("Rogier te lo contó hace mucho", .6, "Rogier", "pegatina grande + clip 148", 0),
    ("asesinó a Godwyn", .5, "Godwyn asesinado", "MG muerte_suelta + clip 149", 0),
    ("La garra termina así", 1.0, "Garra blasfema", "reliquia + ficha", 0),
    ("El Recuerdo del blasfemo lo resume", 1.0, "Recuerdo del blasfemo", "reliquia + ficha", 0),
    ("Bernahl, que cargaba la garra", .8, "Bernahl", "pegatina grande + clip 161", 0),
    ("la serpiente con la cara del pretor", 1.0, "Rykard vencido", "banda + clip 163", 1),
    ("una serpiente nunca muere. Escúchalo|fin", 3.0, "se OYE «A serpent never dies»", "clip 165 + PISTA s_serpiente + rótulo", 1),
    ("Parches lo resume mejor que nadie", .8, "Parches", "pegatina grande + clip 167", 0),
    ("Bnet nos escribió", 1.0, "comentario de Bnet", "tarjeta com_", 0),
    ("Esa es la lista", 1.0, "la lista", "MG estandartes", 0),
    ("Y Tanith, cuando lo matas", .8, "Tanith", "pegatina grande tanith + clip 174/175", 0),
    ("el Cetro de devorador, con forma", 1.0, "Cetro de devorador", "reliquia + ficha", 0),
    ("Ranni, Radahn y Rykard", .6, "trilogía de los hijos de Rennala", "MG linaje", 0),
    ("ya está apuntada la madre", 1.0, "Rennala, Zampaheces, Gideon, Messmer", "abanico", 0),
    ("En el canal tienes las atrocidades", 1.5, "los videos del canal", "abanico", 0),
    ("Crónicas de Tamriel, nuestro canal hermano", .8, "Crónicas de Tamriel", "rótulo", 0),
    ("A lo mejor tiene una rueda de Ghiza", .8, "Rueda de Ghiza", "reliquia", 0),
]


def main():
    capa = SF.cargar()
    S = capa.S
    minis, filas = [], []
    mw, mh = 480, 270
    for frase, dt, que, como, esc in PROMESAS:
        try:
            t = capa.ancla(frase) + dt
        except Exception as e:
            print("NO ENCONTRADA:", frase, e)
            continue
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{len(filas) + 1} {int(t // 60)}:{t % 60:04.1f} {b['id'][6:]} {'E ' if esc else ''}{que}"
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, .45, (90, 214, 255), 1,
                    cv2.LINE_AA)
        minis.append(m)
        filas.append((frase, t, b["id"], que, como, esc))
    cols, n = 4, 12
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/promesas_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)
    mm = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
    pm = ["# Promesas visuales — er_rykard_atrocidades (regla del 5-nov-2026)", "",
          "Hoja: previews/promesas_NN.jpg (cuadro real clip + capa de FX en ese segundo; «E» = escena importante).", "",
          "| n | segundo | beat | qué se nombra | cómo se ve |", "|---|---|---|---|---|"]
    es = ["# Escenas importantes — er_rykard_atrocidades (regla del 18-nov-2026)", "",
          "Cada una con el clip REAL de ese momento (sin Flow); la pegatina va encima o después.", "",
          "| segundo | beat | escena | cómo se ve |", "|---|---|---|---|"]
    for i, (frase, t, bid, que, como, esc) in enumerate(filas, 1):
        pm.append(f"| {i} | {mm(t)} | {bid[6:]} | {que} | {como} |")
        if esc:
            es.append(f"| {mm(t)} | {bid[6:]} | {que} | {como} |")
    open("promesas.md", "w", encoding="utf-8").write("\n".join(pm) + "\n")
    open("escenas.md", "w", encoding="utf-8").write("\n".join(es) + "\n")
    print(len(filas), "promesas;", sum(f[5] for f in filas), "escenas")


if __name__ == "__main__":
    main()
