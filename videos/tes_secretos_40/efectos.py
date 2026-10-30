# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 40 SECRETOS de Skyrim que nadie te contó» (SECUENCIA YT, Crónicas de Tamriel, 30-oct-2026).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 41 avisos (título del top + uno por puesto), arriba al centro.
- Fichas estilo inventario SOLO con cifras verificadas en UESP (`_investigacion_*.md`), arriba a la derecha.
- Pegatinas con la imagen REAL (Fandom/UESP) de cada personaje u objeto que se nombra; los clave, GRANDES.
- Comentarios REALES (reglas 27/28-oct-2026): gancho @ericmarticorena3842, corrección @stazmadness3910 (29), n.º 1 @Knox8386 y
  agradecimientos @Senpai.13 (30), @AnormalProject (20), @OFSUAREZL + @daybengamers8298 (10), @franciscobarqueromunoz1218 (cierre).
- MG NUEVOS de este guion (regla 19-oct-2026): aguante (sopa, 31) · informe thalmor (7 y 6) · cordura (Cicerón, 2) · nombre
  (Paar-Thur-Nax, 1).
- Mapas reales (tema tes) con FOTO y ruta en 14 puestos: 40, 35, 29, 28, 23, 21, 18, 17, 16, 10, 9, 7, 4 y 3. Coordenadas de la
  base de datos del mapa de UESP calibradas sobre el mapa de papel (`_coords_uesp.py`).
  python fab.py tes_secretos_40 fx --seco   tiempos      python fab.py tes_secretos_40 fx hoja   previews/fx_NN.jpg
"""
import os

import mg_tes as T

CAMARA = {}
FUNDIDO = {}

_FX, _FY = .76, .30            # fichas: arriba a la derecha (no tapan el centro del clip)
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")   # imágenes reales de la wiki
_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapas")
TEMA_MAPA = "tes"


def P(slug):
    return os.path.join(_PEG, slug + ".png")


def ficha(en, nombre, efecto, origen=None, dur=5.0, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    """Pegatina con la imagen REAL de lo que nombra la voz (regla de canal): abajo a la izquierda."""
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.5, x=.25, tam=640):
    """Pegatina GRANDE (media pantalla): los personajes y objetos clave."""
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


def com(en, cid, dur=6.0, x=.30, y=.30):
    """Comentario REAL del canal (tarjeta de `fab.py yt comentario`)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760)


def aviso(en, n, titulo, dur=3.6):
    return dict(tipo="mg", fn=T.mision(f"Secreto · número {n}", titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mapa(puntos, de, a, marcas, sub, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, "skyrim.jpg"), puntos, TEMA_MAPA, titulo="Skyrim", sub=sub,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + sub, ver=4.0)


# ---- los MG nuevos (solo datos del guion)
def _aguante():
    return T.aguante("Ataques sin fin", (P("sopa"), "Sopa de verduras"), 12, remate=("Por 5 monedas", 1))


def _informe_esbern():
    return T.informe("Informe thalmor · Esbern", (P("esbern"), "Esbern"),
                     [("Dragones", "No entienden por qué han vuelto", 0),
                      ("Rango", "Nunca fue un simple archivero", 1),
                      ("Funcionario que lo descartó", "Enviado a Alinor a ser reeducado", 2)])


def _informe_ulfric():
    return T.informe("Informe thalmor · Ulfric", (P("ulfric"), "Ulfric"),
                     [("Interrogado por", "Elenwen, en la Gran Guerra", 0),
                      ("Le hicieron creer", "Que su confesión entregó la ciudad", 1),
                      ("En realidad", "La ciudad ya había caído", 2)],
                     sello=("Recurso", 3))


def _cordura():
    return T.cordura("Diario de Cicerón", P("cicero"),
                     [("Asesino cuerdo y metódico", 0), ("Guardián de la Madre Noche", 1), ("Último trabajo: matar a un bufón", 2),
                      ("Lava el cadáver cada semana", 3), ("Ella nunca le habla", 4), ("Oye la risa de aquel bufón", 5)],
                     final=("Cicerón el hombre ha muerto", 6))


def _nombre():
    return T.nombre("Lo que significa su nombre", P("paarthurnax"),
                    [("Paar", "Ambición", 0), ("Thur", "Señor supremo", 1), ("Nax", "Crueldad", 2)])


FX = [
    # ---- gancho
    com("nos dejó este comentario", "UgxVZpFHGH6mmk1_9kd4AaABAg", dur=7.0),
    peg("mejorar un amuleto de Talos", "amuleto_talos", "", dur=3.0, x=.78, y=.62, tam=330),
    peg("Un vendedor de Riften", "brand_shei", "", dur=2.4, x=.17, tam=340),
    peg("una sopa de cinco monedas", "sopa", "", dur=3.2, x=.78, y=.62, tam=340),
    aviso("cuarenta secretos", "40", "Secretos que nadie te contó", dur=4.5),
    grande("alguien en quien confías", "paarthurnax", "", dur=4.0, x=.75, tam=620),

    # ---- 40
    aviso("Número cuarenta", 40, "La poción del arquero"),
    ficha("sube el daño de todas", "Reforzar arquería", "Sube *todas* las armas, y los *puños.*", origen="Error del juego", rojo=True, dur=6.0),
    mapa([(.56, .21, "Lucero del Alba", "inicio", None), (.554, .326, "Fuerte Dunstad · la letrina", "meta", P("pocion_arqueria"))],
         de="Y en una letrina", a=("sobre apuntar bien|fin", .5), marcas=["Y en una letrina", "del Fuerte Dunstad"], sub="La poción del arquero", ajuste=.6),

    # ---- 39
    aviso("En el treinta y nueve", 39, "Las vacas del más allá"),
    peg("catorce cascarones plantados", "cascaron", "Cascarón de alma", dur=4.5),
    grande("dos almas de vaca", "vaca", "", dur=4.0, x=.75, tam=480),

    # ---- 38
    aviso("Número treinta y ocho", 38, "Tu raza decide lo rápido que corres"),
    ficha("Los altos elfos son los más rápidos", "Velocidad por raza", "Altos elfos *1,08* · Orcos *1,045* · Nórdicos *1,03* · Bretonas y khajiit *0,95*",
          origen="Datos del juego", dur=8.0),

    # ---- 37
    aviso("En el treinta y siete", 37, "Castlevania"),
    peg("una garra", "garra", "", dur=2.6, x=.12, tam=280),
    peg("un ojo", "ojo_sable", "", dur=2.2, x=.29, tam=280),
    peg("un corazón", "corazon_daedra", "", dur=1.8, x=.46, tam=280),
    grande("Son las partes de Drácula", "castlevania2", "Castlevania II", dur=5.5, x=.75, tam=560),

    # ---- 36
    aviso("Número treinta y seis", 36, "Los guardias te leen la mochila"),
    peg("Con la Estrella de Azura", "estrella_azura", "Estrella de Azura", dur=4.0),
    peg("Con el Anillo de Namira", "anillo_namira", "Anillo de Namira", dur=3.5, x=.78, y=.62, tam=340),

    # ---- 35
    aviso("En el treinta y cinco", 35, "El mamut congelado"),
    mapa([(.73, .20, "Hibernalia", "inicio", None), (.692, .239, "Saarthal", "paso", None), (.665, .235, "El mamut congelado", "meta", P("mamut"))],
         de="Al oeste de Saarthal", a=("un virote de balista dwemer|fin", .3), marcas=["Al oeste de Saarthal", "hay un mamut atrapado"], sub="El mamut congelado", ajuste=.6),
    peg("Lleva clavadas cinco flechas", "flecha_enana", "Flecha enana", dur=4.0, x=.17),

    # ---- 34
    aviso("Número treinta y cuatro", 34, "Rezar a Arkay te puede matar"),
    ficha("Son veinticinco de salud", "Bendición de Arkay", "*+25* de salud · *8* horas. Si te queda menos al acabar, mueres.", origen="Santuario de Arkay", rojo=True, dur=7.0),

    # ---- 33
    aviso("En el treinta y tres", 33, "El gigante que pudo ser tu aliado"),
    grande("un gigante, Goldar", "gigante", "Goldar · misión cortada", dur=4.5, x=.25, tam=560),
    peg("una vaca pintada", "vaca", "Vaca pintada", dur=3.5, x=.78, y=.62, tam=340),
    ficha("fabricantes de leche débil", "Goldar", "Las vacas son *fabricantes de leche débil.*", origen="Diálogo cortado", dur=4.5),

    # ---- 32
    aviso("Número treinta y dos", 32, "La turista de Markarth"),
    peg("contra Margret", "margret", "Margret", dur=5.0, x=.17),
    grande("agente del general Tullius", "tullius", "General Tullius", dur=4.5, x=.75, tam=480),

    # ---- 31
    aviso("En el treinta y uno", 31, "La sopa de verduras"),
    mg(_aguante(), ("La sopa de verduras te devuelve", -.2), ("Por cinco monedas|fin", .6), ["La sopa de verduras te devuelve", "Por cinco monedas"], "aguante sopa"),

    # ---- 30
    com("nos dijo que el video le pareció", "Ugx90MHBC389cXU7AoF4AaABAg", dur=7.5),
    aviso("Hacerte vampiro te cambia", 30, "Hacerte vampiro te cambia de raza"),
    peg("Bolund, en Falkreath", "bolund", "Bolund", dur=4.0, x=.17),
    peg("Y Galathil", "galathil", "Galathil", dur=4.5, x=.17),

    # ---- 29
    aviso("En el veintinueve", 29, "Un error nuestro"),
    ficha("velocidad cero coma seis", "Corrección", "Dijimos *0,6* para todos los martillos. No es verdad.", origen="Video de las armas", rojo=True, dur=6.0),
    mapa([(.105, .49, "Markarth", "inicio", None), (.239, .357, "Retiro del Mentiroso", "meta", P("martillo_largo"))],
         de="En el Retiro del Mentiroso", a=("Velocidad cero coma ocho|fin", .2), marcas=["En el Retiro del Mentiroso", "un cadáver sujeta"], sub="El Martillo largo", ajuste=.6),
    ficha("A herrería máxima", "Martillo largo", "*24,8* de daño por segundo · Volendrung *24,5*", origen="A herrería máxima", dur=5.0),
    com("nos dijo que Clarividencia", "UgyQPJkz1TMvyu2as4l4AaABAg", dur=7.5),
    peg("la brújula no dice", "clarividencia", "Clarividencia", dur=3.5, x=.78, y=.66, tam=320),

    # ---- 28
    aviso("Número veintiocho", 28, "El hombre que sigue esperando un barco"),
    mapa([(.73, .20, "Hibernalia", "inicio", None), (.671, .185, "Campamento de Trius", "paso", None), (.671, .165, "Zanja del Peregrino", "meta", None)],
         de="En la costa de Hibernalia", a=("de la Zanja del Peregrino|fin", .5), marcas=["En la costa de Hibernalia", "bajo el agua"], sub="Para Shelly", ajuste=.6),

    # ---- 27
    aviso("En el veintisiete", 27, "Tu seguidor es mejor ladrón que tú"),
    grande("Si le mandas abrir", "lydia", "", dur=5.0, x=.75, tam=560),
    ficha("un arco de caza", "Inventario oculto", "Arco de caza y *12* flechas de hierro.", origen="No sale en su inventario", dur=4.5),

    # ---- 26
    aviso("Número veintiséis", 26, "La maga de la corte de Soledad"),
    peg("Sybille Stentor dice", "sybille", "Sybille Stentor", dur=6.0, x=.17),
    peg("El verdugo cuenta", "ahtar", "Ahtar", dur=4.0, x=.78, y=.62, tam=340),

    # ---- 25
    aviso("En el veinticinco", 25, "La nave de los rieklings"),
    peg("los rieklings acampan", "riekling", "Riekling", dur=5.0, x=.17),

    # ---- 24
    aviso("Número veinticuatro", 24, "La semana libre que creó las expansiones"),
    peg("De ahí salieron los rieklings", "riekling", "", dur=2.2, x=.12, tam=280),
    peg("Arvak", "arvak", "", dur=2.2, x=.29, tam=280),
    peg("el Señor de los vampiros", "senor_vampiro", "", dur=2.4, x=.46, tam=280),

    # ---- 23
    aviso("En el veintitrés", 23, "La capilla que aparece sola"),
    mapa([(.241, .523, "Viejo Hroldan", "inicio", None), (.226, .50, "El campamento · capilla de Mara", "meta", P("capilla_mara"))],
         de="Cerca del Viejo Hroldan", a=("con el diario de Karan al lado|fin", .4), marcas=["Cerca del Viejo Hroldan", "el campamento desaparece"], sub="Karan y Talvur", ajuste=.8),

    # ---- 22
    aviso("Número veintidós", 22, "El Pergamino Antiguo esconde nuestras estrellas"),
    peg("Su fondo no es inventado", "pergamino", "Pergamino Antiguo", dur=6.0, x=.30, y=.70, tam=640),
    peg("con el Arco de Auriel", "auriel", "Arco de Auriel", dur=3.5, x=.78, y=.62, tam=340),

    # ---- 21
    aviso("En el veintiuno", 21, "Desde Skyrim se ve Morrowind"),
    mapa([(.744, .183, "Colegio de Hibernalia · azotea", "inicio", None), (.86, .23), (.96, .28, "Morrowind", "meta", None)],
         de="Desde la azotea", a=("se ve Morrowind|fin", .4), marcas=["Desde la azotea", "más allá de la frontera"], sub="Mirar fuera del mapa", ajuste=.6),

    # ---- 20
    com("nos dijo que a veces la música", "UgwjxU2XdFokls27Pnp4AaABAg", dur=7.5),
    aviso("Número veinte", 20, "Neloth ya era un cretino en Morrowind"),
    grande("Es el mismo personaje", "neloth", "Neloth", dur=5.0, x=.75, tam=520),

    # ---- 19
    aviso("En el diecinueve", 19, "El capitán que no se quedó muerto"),
    peg("está Falx Cario", "falx", "Falx Cario", dur=6.0, x=.17),
    peg("Ildari lo reanimó", "ildari", "Ildari", dur=4.0, x=.78, y=.62, tam=340),

    # ---- 18
    aviso("Número dieciocho", 18, "El local de skooma que es una granja de sangre"),
    mapa([(.89, .78, "Riften", "inicio", None), (.802, .723, "Guarida de Aguas Rojas", "meta", P("skooma"))],
         de="La Guarida de Aguas Rojas", a=("te venden skooma|fin", .3), marcas=["La Guarida de Aguas Rojas", "Bajo una trampilla"], sub="Aguas Rojas", ajuste=.6),

    # ---- 17
    aviso("En el diecisiete", 17, "Los cuatro aprendices que nadie buscó"),
    peg("Phinis Gestor menciona", "phinis", "Phinis Gestor", dur=4.0, x=.17),
    mapa([(.744, .183, "Colegio de Hibernalia", "inicio", P("phinis")), (.62, .20, "Yisra · la playa", "peligro", None),
          (.79, .225, "Rundi · runas de escarcha", "peligro", None), (.783, .273, "Borvir · Rincón del viajero", "peligro", None),
          (.718, .127, "Ilas-Tei · capilla de Talos", "meta", None)],
         de="repartidos por la comarca", a=("con un pergamino de Furia al lado|fin", .4),
         marcas=["repartidos por la comarca", "Yisra está calcinada", "Rundi yace", "Borvir, con tres", "E Ilas-Tei aparece"], sub="Los cuatro aprendices", ajuste=.9),

    # ---- 16
    aviso("Número dieciséis", 16, "El héroe del libro es el jefe que mataste"),
    peg("Sangre inmortal es un libro", "sangre_inmortal", "Sangre inmortal", dur=5.0, x=.20, y=.66, tam=480),
    mapa([(.42, .31, "Morthal", "inicio", None), (.418, .281, "Guarida de Movarth", "meta", P("movarth"))],
         de="Y el señor vampiro", a=("ese mismo Movarth|fin", .5), marcas=["Y el señor vampiro", "de la cueva de Morthal"], sub="Movarth Piquine", ajuste=.5),

    # ---- 15
    aviso("En el quince", 15, "La arena de Ventalia"),
    ficha("Si te encerraban", "La cárcel de la arena", "Peleabas ante el público. Si *ganabas*, salías *libre.*", origen="Contenido cortado", dur=6.0),

    # ---- 14
    aviso("Número catorce", 14, "El gran maestro tiene ficha de novato"),
    ficha("Paarthurnax es nivel diez", "Paarthurnax", "Nivel *10* · *905* de salud. Igual que el dragón más básico.", origen="Datos del juego", dur=6.5),
    grande("Acuérdate de este dragón", "paarthurnax", "", dur=3.5, x=.25, tam=560),

    # ---- 13
    aviso("En el trece", 13, "Los libros que nadie lee"),
    peg("cuatro libros en alfabeto falmer", "tomo_falmer", "Libro falmer", dur=4.0, x=.17),
    peg("Urag gro-Shub", "urag", "Urag gro-Shub", dur=4.5, x=.78, y=.62, tam=340),

    # ---- 12
    aviso("Número doce", 12, "Nunca absorbiste el alma de Alduin"),
    grande("Al matarlo no absorbes", "alduin", "Alduin", dur=4.0, x=.75, tam=560),
    peg("Arngeir te explica", "arngeir", "Arngeir", dur=5.0, x=.17),

    # ---- 11
    aviso("En el once", 11, "El cura de Falkreath"),
    peg("Runil, el anciano sacerdote", "runil", "Runil", dur=5.5, x=.17),

    # ---- 10
    com("tremendo video", "UgyyK-18w979imO7POB4AaABAg", dur=4.0, x=.30, y=.24),
    com("le encantan estos videos", "Ugz_K8Ode87ZNHZb7FR4AaABAg", dur=3.6, x=.30, y=.42),
    aviso("Número diez", 10, "El pozo de la Hueste de Forel"),
    peg("Las tropas de Skorm", "diario_skorm", "Diario de Skorm", dur=4.5, x=.17, tam=340),
    mapa([(.89, .78, "Riften", "inicio", None), (.913, .832, "Hueste de Forel · el pozo", "meta", None)],
         de="Al día siguiente, cuarenta", a=("tienes que bajar|fin", .4), marcas=["Al día siguiente, cuarenta", "Y ese pozo"], sub="La Hueste de Forel", ajuste=.5),

    # ---- 9
    aviso("En el nueve", 9, "El faro que se tragó a una familia"),
    mapa([(.56, .21, "Lucero del Alba", "inicio", None), (.631, .248, "Faro del Flujo Helado", "meta", None)],
         de="Una familia redguard", a=("un agujero en el sótano|fin", .3), marcas=["Una familia redguard", "el Faro del Flujo Helado"], sub="El faro", ajuste=.5),
    peg("Y los restos del padre", "segador", "Segador de chaurus", dur=4.0, x=.17),
    peg("Si los subes al brasero", "restos_habd", "Restos de Habd", dur=3.5, x=.78, y=.62, tam=340),

    # ---- 8
    aviso("Número ocho", 8, "Los Barbas Grises nacieron de una humillación"),
    peg("Jurgen Llamador del Viento", "jurgen", "Jurgen Llamador del Viento", dur=6.0, x=.17),
    ficha("diecisiete lo atacaron", "Jurgen contra todos", "*17* contra *1* · *3* días tragándose sus gritos.", origen="Tablillas de Alto Hrothgar", dur=6.0, x=.84),

    # ---- 7
    aviso("En el siete", 7, "Lo que dicen los archivos thalmor"),
    mg(_informe_esbern(), ("En su informe sobre Esbern", -.2), ("a ser reeducado|fin", .7),
       ["que no entienden la vuelta", "nunca fue un simple archivero", "Al funcionario que lo descartó"], "informe esbern"),
    grande("Y el informe de Delphine", "delphine", "Delphine", dur=6.0, x=.75, tam=520),

    # ---- 6
    aviso("Número seis", 6, "Ulfric cree que entregó la Ciudad Imperial"),
    mg(_informe_ulfric(), ("Los thalmor lo capturaron", -.2), ("figura como un recurso|fin", .9),
       ["Los thalmor lo capturaron", "le hicieron creer", "La ciudad ya había caído", "figura como un recurso"], "informe ulfric"),

    # ---- 5 (sin sarcasmo: solo lo necesario)
    aviso("Erik el Asesino existió", 5, "Erik el Asesino existió", dur=4.5),
    grande("El granjero de Paraje de Rorik", "erik", "Erik el Asesino", dur=6.0, x=.75, tam=560),

    # ---- 4
    aviso("Número cuatro", 4, "El vendedor de Riften"),
    grande("Brand-Shei es un elfo oscuro", "brand_shei", "Brand-Shei", dur=5.0, x=.75, tam=560),
    mapa([(.89, .78, "Riften · Brand-Shei", "inicio", P("brand_shei")), (.84, .45), (.793, .195, "Naufragio del Orgullo de Tel Vos", "meta", None)],
         de="En el naufragio del Orgullo", a=("Lo llama su único heredero|fin", .4), marcas=["En el naufragio del Orgullo", "un diario de su padre"], sub="El vendedor de Riften", ajuste=.7),
    peg("tú le metes un anillo", "anillo_madesi", "Anillo de plata de Madesi", dur=4.5, x=.17, tam=340),

    # ---- 3
    aviso("En el tres", 3, "El ataúd del carro"),
    peg("la Madre Noche estaba", "madre_noche", "Madre Noche", dur=5.0, x=.17),
    mapa([(.565, .429, "Granja de Loreio · el carro", "inicio", P("madre_noche")), (.50, .60), (.409, .745, "Santuario de Falkreath", "meta", P("cicero"))],
         de="Es el mismo ataúd", a=("la caída de la Hermandad|fin", .5), marcas=["Es el mismo ataúd", "Trece años huyendo"], sub="El ataúd del carro", ajuste=.5),

    # ---- 2
    aviso("Número dos", 2, "Cicerón no nació loco"),
    mg(_cordura(), ("Sus diarios empiezan", -.2), ("es su última víctima|fin", .8),
       ["Sus diarios empiezan", "Lo nombran Guardián", "Matar a un bufón", "Lava el cadáver", "Ella nunca le habla", "empieza a oír la risa", "Cicerón el hombre ha muerto"],
       "cordura cicerón"),

    # ---- 1
    aviso("Y llegamos al número uno", 1, "El que te enseñó a confiar", dur=3.0),
    com("nos escribió que tras muchísimos", "UgzXyBrJs7uH5lwToEV4AaABAg", dur=8.5),
    mg(_nombre(), ("Su nombre se separa", -.2), ("Crueldad|fin", 2.0), ["Paar, Thur", "Señor supremo", "Crueldad"], "nombre paarthurnax"),
    peg("la mano derecha de Alduin", "alduin", "Alduin", dur=4.5, x=.78, y=.62, tam=380),
    grande("Y lo más fuerte lo dice él", "paarthurnax", "Paarthurnax", dur=9.0, x=.25, tam=640),

    # ---- cierre
    com("nos dio las gracias", "UgzGF3olyXy2g-JageF4AaABAg", dur=6.0),
    ficha("Cuántos de estos cuarenta", "¿Cuántos sabías?", "Déjalo en los *comentarios.*", dur=5.0),
]


# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave para no repetirlos (regla de SFX)
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in ("Número cuarenta", "Hacerte vampiro te cambia", "Número veinte", "Número diez", "En el tres", "Número dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.20) for e in ("repartidos por la comarca", "Al día siguiente, cuarenta", "En su informe sobre Esbern", "En el naufragio del Orgullo")]
PISTAS += [dict(sfx="monedas", en=e, vol=.30) for e in ("Por cinco monedas", "paga mil monedas", "un anillo en el bolsillo")]
PISTAS += [dict(sfx="subir_nivel", en="Y llegamos al número uno", vol=.24), dict(sfx="subir_nivel", en="Hoy te traigo cuarenta secretos", vol=.18),
           dict(sfx="mision_completada", en="Esa es mi lista", vol=.22)]
