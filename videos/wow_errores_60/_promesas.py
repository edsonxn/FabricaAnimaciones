# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026): cuadro real (clip + capa de efectos) en el segundo en que la voz dice cada frase.
previews/promesas_NN.jpg (12 por hoja). Las frases y lo que debería verse: PROMESAS de abajo (copiadas a promesas.md).
Copiado de wow_ruta_forever/_promesas.py (22-nov-2026).
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
    ("Faltan catorce días para que abran", 2.0, "MG cuenta atrás 14 días + 3 bandas"),
    ("En la primera semana de Forever hubo ciento", 3.0, "MG 196 millones de muertes"),
    ("Porque las tres bandas reinician", 1.5, "abanico 3 bandas + REINICIO SEMANAL"),
    ("beneficios que se apagan en la puerta", 0.8, "fila trampas: beneficios / tope / botín"),
    ("Blizzard dice que Forever tiene más gente", 1.5, "banda MÁS GENTE"),
    ("Ya hicimos los errores de los primeros niveles", 2.0, "MG saga 1-30 / 30-60 / 60"),
    ("Hoy te traigo veinticinco errores", 1.5, "banda 25 ERRORES"),
    ("Unos te cuestan oro", 1.5, "fila oro / semanas / repetir mazmorras"),
    # 25
    ("Número veinticinco. Cambiar un anillo", 1.5, "reliquia Anillo de canalizador"),
    ("Al Anillo de canalizador le quitó", 1.0, "ficha anillo - espíritu + poder"),
    ("Y a la Sortija de la Luz bendita", 1.0, "pegatina Sortija"),
    ("ese cambio se hace con un vendedor, Pix", 1.0, "pegatina Pix Xizzix"),
    ("El Anillo da intelecto, golpe", 1.5, "fichas anillo y sortija"),
    ("acaba de regalar su sanación", 0.5, "rótulo -SANACIÓN"),
    ("pon los dos anillos uno junto al otro", 1.0, "fila dos anillos"),
    # 24
    ("Número veinticuatro. Ignorar las tareas", 1.5, "reliquia tareas JcJ"),
    ("Cada temporada de JcJ trae una ruta", 1.5, "ficha tareas semanales"),
    ("Y la primera es casi un regalo", 1.5, "MG meta 3 tareas"),
    ("matar a veinticinco jugadores", 1.0, "MG meta: 25 jugadores"),
    ("Mucha gente al sesenta solo mira la banda", 0.8, "camafeo Onyxia solo la banda"),
    ("y deja pasar semanas de tareas", 0.8, "pegatina Garganta Grito de Guerra"),
    ("se pueden completar en temporadas futuras", 0.5, "rótulo TEMPORADAS FUTURAS"),
    ("Diez duelos en la puerta de tu capital", 1.0, "pegatina 10 duelos"),
    # overgear
    ("Y si estás llegando al sesenta, este es el momento", 2.0, "gameplay (antes del patrocinio)"),
    ("Este video lo patrocina Overgear", 1.5, "logo blanco Overgear"),
    ("Son sesiones individuales", 1.5, "tarjeta coaching Overgear"),
    ("Un coach mira tus talentos", 1.5, "pros Overgear"),
    ("Porque las guías no siempre van al día", 1.5, "talentos / guías"),
    ("Y si todavía vas camino del sesenta", 1.0, "logo + gameplay"),
    ("resistencia al fuego para la Guarida", 0.5, "captura página coaching"),
    ("Si reservas dos horas", 1.5, "reseñas sobre fondo morado"),
    ("y lo que aprendes se queda contigo", 0.5, "fondo morado"),
    ("El enlace está en la descripción, y hay", 1.5, "packshot sobre fondo morado"),
    ("Usa el código CRONICAS10", 2.5, "código CRONICAS10 sobre fondo morado"),
    # 23
    ("Número veintitrés. Entrar a la Guarida", 1.5, "reliquia Onyxia"),
    ("La banda más grande del nueve", 1.5, "mapa Marjal Guarida"),
    ("Blizzard confirma que la pelea tiene", 2.0, "MG 3 fases"),
    ("porque el coletazo te manda a volar", 0.8, "pegatina Barrido de cola"),
    ("de los huevos salen crías", 0.8, "pegatina cría de Onyxia"),
    ("El que recibe la bola de fuego", 1.0, "fila bola de fuego / aliento"),
    ("Y en la tercera llega el rugido", 1.0, "pegatina Onyxia fase 3"),
    ("El arreglo: que los cuarenta vean la pelea", 1.5, "ficha plan de Onyxia"),
    # 22
    ("Número veintidós. Gastar el honor", 1.5, "reliquia lacre envalentonado"),
    ("El honor de Forever compra dos conjuntos", 1.5, "ficha conjuntos JcJ"),
    ("Los de muñeca y cinturón piden rango ocho", 1.0, "MG rangos lacres"),
    ("venderla porque te cayó algo mejor", 0.8, "camafeo vendida"),
    ("Son la base de tu conjunto épico", 0.8, "pegatina lacre de cabeza"),
    # burla0
    ("Alejandro escribió: hay un poco", 1.5, "comentario Alejandro"),
    ("Y fíjate en las proporciones", 2.0, "MG proporciones"),
    ("no alcanzan ni para la banda de diez", 0.8, "camafeo banda de 10"),
    # 21
    ("Número veintiuno. Creer que tu rango", 1.5, "reliquia rango JcJ"),
    ("todo el mundo vuelve al rango uno", 0.6, "MG reinicio al rango 1"),
    ("ese tope empieza en el rango tres", 1.0, "MG tope por semana"),
    ("Y ojo con el Valle de Alterac", 1.0, "pegatina Valle de Alterac"),
    ("las Islas Lanza Negra, de quince", 0.5, "pantalla Islas Lanza Negra"),
    ("de quince contra quince", 0.5, "camafeo 15 contra 15"),
    ("el equipo que compras se queda contigo", 0.6, "camafeo se queda contigo"),
    # 20
    ("Número veinte. Comprar los consumibles", 1.5, "reliquia consumibles"),
    ("La economía de Forever empezó de cero", 2.0, "MG economía"),
    ("Pociones de protección de fuego para Onyxia", 3.0, "fila 5 consumibles"),
    ("Y un detalle gracioso: la comida", 1.5, "ficha comida +5 %"),
    ("si tienes alquimia o cocina", 0.6, "camafeo alquimia"),
    # 19
    ("Número diecinueve. Llegar al nueve", 1.5, "reliquia reparar"),
    ("de las dos bandas nuevas", 0.6, "fila Cima / Cavernas"),
    ("hubo casi doscientos millones de muertes", 0.8, "pegatina ángel de resurrección"),
    ("El que se gasta todo en la montura épica", 0.8, "camafeo montura"),
    ("si el grupo no acuerda antes", 0.6, "camafeo y el botín"),
    ("El arreglo: aparta un dinero solo para reparar", 1.5, "ficha primera semana"),
    # gracias1
    ("Un espectador nuevo nos escribió", 1.5, "comentario i.a.2.0.2.5"),
    ("Torrikus dice que siempre", 1.0, "comentario Torrikus"),
    ("Y Andrés, después del video", 1.5, "comentario Andrés"),
    ("todavía no has hecho cola para la Cumbre", 0.8, "pegatina Cumbre superior"),
    # 18
    ("Número dieciocho. Ir a la Cima Hyjal", 1.5, "reliquia Cima Hyjal"),
    ("era la banda de Archimonde", 0.6, "pegatina Archimonde"),
    ("Es de veinte jugadores, con trece jefes", 1.5, "mapa Hyjal"),
    ("junto a Nordrassil", 0.5, "mapa Hyjal: Nordrassil"),
    ("Empieza contra un guardián antiguo", 1.0, "pantalla Cima Hyjal"),
    ("Y luego se abren tres caminos", 1.5, "ficha Cima Hyjal 3 caminos"),
    ("En los datos del juego hay nombres", 2.5, "MG expediente archivos"),
    ("existe un arma que se llama", 1.5, "reliquia Arma inútil"),
    ("tres caminos, para un grupo nuevo", 0.6, "camafeo 3 caminos"),
    # 17
    ("Número diecisiete. No saber que las Cavernas", 1.5, "reliquia Cavernas"),
    ("La banda de diez está escondida", 1.0, "pantalla Cavernas / Illidan"),
    ("Y tiene tres entradas", 3.0, "mapa 3 entradas"),
    ("medio grupo esperando en Cuna", 0.8, "fila Cuna / Hyjal"),
    ("uno de los jefes es un pozo", 0.5, "rótulo WELL OF SORROW"),
    ("Y hay una moneda de oro de Sonya", 1.5, "reliquia moneda + ficha texto"),
    ("decidid la entrada antes del día", 0.5, "rótulo DECIDID LA ENTRADA + mapa Cuna del Invierno"),
    # 16
    ("Número dieciséis. Entrar al Bastión", 1.5, "reliquia Bastión"),
    ("Es la mazmorra nueva del cincuenta y cinco", 1.5, "mapa Azshara Bastión"),
    ("más grande que Profundidades de Roca Negra", 0.3, "camafeo Profundidades"),
    ("Cada bando tiene siete misiones", 1.5, "MG misiones Bastión"),
    ("La primera empieza con Nara", 1.0, "fila Nara / Mathrengyl"),
    ("Y otra misión pide un objeto de Withermaw", 1.5, "ficha dos caminos"),
    ("Y un detalle: el Bastión está", 1.5, "pantalla Bastión"),
    ("llevan a las Cavernas del Túmulo", 0.6, "camafeo Cavernas"),
    # burla1
    ("interrumpo el video para interactuar", 0.5, "rótulo INTERRUPCIÓN"),
    ("Jclothus escribió: deja de interrumpir", 1.5, "comentario Jclothus"),
    ("te leo a ti, que lo pediste", 0.5, "rótulo TE LEO A TI"),
    ("en paradas cortas", 1.0, "MG paradas"),
    # 15
    ("Número quince. Entrar al Bancal", 1.5, "reliquia Bancal"),
    ("Es la otra mazmorra nueva", 2.0, "mapa Un'Goro norte"),
    ("Dentro hay cuatro consolas titánicas", 1.5, "MG consolas"),
    ("Azul para Snowtalon", 0.8, "MG consolas azul"),
    ("despierta la jefa final, Nanaya", 0.8, "MG Nanaya"),
    ("no metas cristales en la consola", 0.5, "rótulo SIN BICHOS"),
    ("juntad quince de cada color", 0.8, "fila 4 cristales"),
    # 14
    ("Número catorce. Llegar al sesenta sin plan", 1.5, "reliquia montura épica"),
    ("La equitación del sesenta en Forever cuesta", 2.0, "MG factura montura"),
    ("las monturas raciales de vendedor se ligan", 1.0, "ficha monturas raciales"),
    ("los cielonatos no recibían el descuento", 0.5, "rótulo CIELONATOS"),
    ("Para que te hagas una idea", 2.5, "MG 1391 de oro"),
    ("empieza a juntar desde el cincuenta y cinco", 0.6, "camafeo desde el 55"),
    # 13
    ("Número trece. Planear la banda", 1.5, "reliquia botín oculto"),
    ("En Forever, el botín de las bandas", 2.0, "MG botín oculto"),
    ("esa lista se la inventó", 0.3, "MG lista inventada"),
    ("el primer conjunto se reparte entre las tres", 1.2, "abanico 3 bandas"),
    ("con nueve personas mirándote", 0.5, "camafeo banda de 10"),
    # 12
    ("Número doce. Farmear un fallo", 1.5, "reliquia fallo"),
    ("El fin de semana del catorce", 2.0, "mapa Azshara fallo"),
    ("Blizzard lo arregló el dieciséis", 2.0, "MG expediente fallo"),
    ("Eso sí, Blizzard aclaró que nadie", 1.5, "ficha aviso Blizzard"),
    ("si algo da diez veces más oro", 0.6, "camafeo el fallo"),
    # correcciones
    ("En el video del oro recomendé Auctionator", 1.5, "comentario Gespexp"),
    ("Aztero nos recordó que el brujo", 1.5, "comentario Aztero"),
    ("Sastakai nos corrigió que", 1.5, "comentario Sastakai"),
    ("en el video del treinta al sesenta dijimos", 1.5, "reliquia Lacre de Ascensión"),
    # 11
    ("Vamos con el número once", 1.5, "reliquia Cumbre superior"),
    ("La Cumbre superior es especial", 1.5, "mapa Estepas Cumbre"),
    ("Y en las dos primeras semanas de Forever estaba", 2.0, "MG cumbre rota"),
    ("arreglaron un pilar de piedra rebelde", 0.6, "camafeo pilar rebelde"),
    ("y alguien con el Lacre de Ascensión", 0.6, "camafeo Lacre"),
    # 10
    ("Número diez. Terminar la sintonización", 1.5, "reliquia amuleto"),
    ("Lo de empezar pronto la sintonización", 0.8, "camafeo sintonización"),
    ("te dan el Amuleto de Pirodraco", 0.6, "pegatina amuleto"),
    ("Pero para entrar a la Guarida", 1.5, "mapa puerta de Onyxia"),
    ("Y es personal: no se comparte", 1.0, "ficha amuleto personal"),
    ("Y en Forever, el amuleto da diez", 0.8, "camafeo +15 fuego"),
    ("para pelear contra la dueña de la casa", 0.5, "pegatina Onyxia"),
    # 9
    ("Número nueve. Entrar a Onyxia", 1.5, "reliquia poción fuego"),
    ("Blizzard lo escribió en su anuncio", 1.5, "banda RESISTENCIA AL FUEGO"),
    ("El Amuleto de Pirodraco da quince", 0.8, "MG resistencias"),
    ("Y está la Poción de protección de fuego", 1.5, "ficha poción"),
    ("Y la Capa de escamas de Onyxia", 1.0, "fila capa / escama"),
    ("lleva el amuleto encima y varias", 0.6, "camafeo encima"),
    # gracias2
    ("El Teniente Dandadan nos cuenta", 1.5, "comentario Teniente"),
    ("Y Zargues, con tres semanas", 1.5, "comentario Zargues"),
    ("así no te pierdes lo que viene", 0.6, "camafeo 9 de diciembre"),
    # 8
    ("Número ocho. Apuntar a una banda", 1.5, "reliquia Onyxia 40"),
    ("Las bandas de Forever son fijas", 3.0, "MG aforo"),
    ("Si tu hermandad son catorce", 1.0, "MG aforo hermandad 14"),
    ("se parecen más a Karazhan", 0.6, "pegatina Cavernas"),
    ("El arreglo: arma un grupo fijo de diez", 2.0, "mapa Kalimdor bandas"),
    # 7
    ("Dejar la herrería, la peletería", 1.0, "fila profesiones"),
    ("Las recetas del conjunto de artesano", 1.5, "ficha conjunto artesano"),
    ("da puntos de Legado a ciento cincuenta", 1.5, "MG legado profesiones"),
    ("con la profesión en doscientos cuarenta", 0.5, "rótulo 240 NO ES 300"),
    ("La receta te pide reputación", 2.5, "MG forja artesano"),
    ("busca un fabricante en tu hermandad", 0.6, "camafeo fabricante"),
    # 6
    ("Número seis. Ignorar a los Guardianes", 1.5, "reliquia tabardo"),
    ("Es una facción nueva de Forever, en el Monte", 1.0, "pegatina Monte Hyjal"),
    ("Del conjunto de artesano, el que se fabrica, solo", 1.5, "ficha artesano 1 pieza"),
    ("necesitas la Vaina de semilla", 0.8, "reliquia vaina"),
    ("Esa vaina la vende su intendente", 1.5, "mapa Rhylin"),
    ("Y reverenciado son veintiún mil", 2.0, "MG reputación"),
    ("una semilla caída de Nordrassil", 0.5, "pegatina Nordrassil"),
    ("haz ya la cadena de Tiala", 1.0, "mapa Hyjal: Tiala (foto) · El bastón de la montaña"),
    # burla2
    ("Rafael escribió: deja de hacer", 1.5, "comentario Rafael"),
    ("cuántos cristales pide el Bancal", 1.5, "fila cristales / lacre / poción"),
    ("lo que te dice la puerta de Onyxia", 0.5, "camafeo puerta Onyxia"),
    ("Quédate al top cinco", 0.5, "rótulo TOP 5"),
    # 5
    ("Número cinco. Farmear mazmorras", 1.5, "reliquia 5 por hora"),
    ("Al sesenta, todo el mundo farmea", 2.0, "mapa Peste Stratholme/Scholomance"),
    ("Y el veinte de noviembre, hace solo", 2.5, "MG tope por hora"),
    ("con el aviso de que ha entrado", 1.0, "MG DEMASIADAS ESTANCIAS"),
    ("Y otra regla: una mazmorra no da experiencia", 1.5, "ficha experiencia"),
    ("Blizzard pasó de diez a cinco", 0.5, "rótulo 10 a 5"),
    ("y alterna mazmorras", 0.6, "fila Stratholme / Scholomance"),
    # 4
    ("Número cuatro. Que nadie de tu grupo", 1.5, "reliquia Lacre de Ascensión"),
    ("Dentro está el general Drakkisath", 0.8, "carrusel Drakkisath"),
    ("y Lord Valthalak", 0.3, "carrusel Valthalak"),
    ("Y la puerta solo se abre", 1.0, "pantalla Cumbre superior"),
    ("y las tres gemas de sus generales", 1.5, "MG forja lacre"),
    ("Y al final tienes que forjarlo", 2.0, "mapa Brasaliza"),
    ("Y en Forever, el lacre da además", 1.0, "ficha lacre resistencias"),
    ("empiézalo con Vaelan", 0.6, "mapa Estepas: Cumbre (foto Vaelan)"),
    # 3
    ("Número tres. Vender al vendedor", 1.5, "reliquia esencia"),
    ("se fabrica con un material", 1.5, "MG forja esencias"),
    ("acaba en el vendedor por unas monedas", 0.6, "camafeo monedas"),
    ("Y si la banda va sin encantador", 0.8, "pegatina encantamiento"),
    ("lleva un encantador a cada banda", 0.6, "camafeo encantador"),
    ("que todo lo que sobre se desencante", 0.6, "camafeo desencantar"),
    # 2
    ("Número dos. Farmear beneficios", 1.5, "reliquia beneficios"),
    ("mata a Rend", 0.5, "carrusel Rend"),
    ("se come la Serenata Cantaflor", 0.6, "carrusel Serenata"),
    ("y por la Feria de la Luna Negra", 0.6, "carrusel Feria"),
    ("El texto del de la cabeza de Onyxia", 1.5, "ficha berrido"),
    ("puedes matar a Onyxia, colgar su cabeza", 0.8, "pegatina cabeza de Onyxia"),
    ("el Poderío de Ventormenta", 0.8, "fila Poderío / Bendición"),
    ("Lo bueno: Blizzard puso heraldos", 1.5, "ficha heraldos"),
    ("así que el beneficio de Rend te llega", 0.6, "camafeo cabeza de Rend"),
    ("Y el Reubicador cronológico", 1.0, "reliquia Reubicador"),
    # 1
    ("Número uno. Vender las piezas", 1.5, "reliquia Yelmo Forjaluz"),
    ("El casco lo suelta el Maestro", 0.6, "carrusel Gandling"),
    ("y el peto el general Drakkisath", 0.6, "carrusel Drakkisath"),
    ("Te cae un azul nuevo", 0.6, "camafeo pieza del conjunto"),
    ("Vas entregando brazales", 2.0, "MG entregas"),
    ("Si vendiste el casco", 0.8, "MG entregas: Gandling otra vez"),
    ("Y la cadena es una vuelta al mundo", 3.0, "mapa vuelta al mundo"),
    ("Y el brasero sagrado que necesitas", 1.0, "reliquia brasero"),
    ("el Ejecutor Asharell", 0.6, "mapa Estepas Asharell"),
    ("Y la novedad buena: en cada entrega", 1.5, "ficha 0.5 Forever"),
    ("si matas a Lord Valthalak", 0.6, "pegatina Valthalak"),
    ("guarda cada pieza del conjunto aunque", 1.0, "fila cierre del 1"),
    # cierre
    ("del anillo que no tiene vuelta atrás", 0.6, "fila anillo / conjunto"),
    ("Faltan dos semanas para el nueve", 2.0, "MG cuenta atrás 2 semanas"),
    ("Cuéntame en los comentarios en qué nivel vas", 1.0, "rótulo EN QUÉ NIVEL VAS"),
    ("treinta y nueve amigos más", 0.5, "MG 39 amigos"),
    ("Nos vemos en la próxima crónica", 1.0, "cierre"),
]


def md():
    with open("promesas.md", "w", encoding="utf-8") as f:
        f.write("# Promesas visuales — wow_errores_60\n\n| frase | +s | cómo se ve |\n|---|---|---|\n")
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
