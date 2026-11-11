# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «20 SECRETOS ESCONDIDOS de los primeros niveles de WoW Forever» (SECUENCIA YT, Crónicas de Warcraft,
10-nov-2026, lista v3). Modelo: videos/wow_addons_forever/efectos.py.
- Cada puesto: reliquia/pegatina real al decir «Número N» + MAPA REAL con ruta (zamimg Classic, 1 % = coordenada del juego;
  Zephras = mapa del juego de Forever) + MG nuevos de este guion (chat del /rude y del «Eekum Bokum», paradero de Zendraas,
  reloj del servidor de Piroleña, cadena del Dawn Waker, carta Sully → Sullivan, línea de vida de Michel Koiter).
- Gaia al inicio: el beat del post lleva el MASTER de la Crematoria con su audio (_gaia.py + PISTA oye_crematoria).
- Comentarios en pantalla (≤ 10 días, ninguno repetido): Sayho, Pausa (gaia2) · Ricochet, Galaxy, Bajel (gracias1) · Chino,
  Klb (gracias2) · Alfredo (burla1). Gustavo y Vikussss (22-oct) solo por voz.
  python fab.py wow_secretos_primeros_niveles fx --seco | fx hoja | fx
"""
import os

import mg_tes as T
import mg_wow as M
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("Usa el código CRONICAS10", 0.9)
TEMA_PEG = "wow"
AMAR, ROJO, VERDE, BLANCO, NAR = (255, 255, 160), (255, 70, 60), (40, 210, 90), (240, 240, 240), (255, 150, 60)
V, GR, RJ = "verde", "gris", "#ff3b3b"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(F(slug), titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6):
    xs = (.14, .32, .50, .68, .86)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="comentario " + id_, ver=1.0)


def rel(en, slug, nombre=None, sub=None, dur=4.2, x=.76, y=.52, tam=500):
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.4)):
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def ban(en, slug, nombre, sub=None, dur=4.0, x=.5, y=.78, tam=420):
    return dict(tipo="mg", fn=PE.banda(F(slug), nombre, sub, alto=tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def sil(en, slug, nombre, sub=None, dur=4.4, lado="izq", alto=820):
    return dict(tipo="mg", fn=PE.silueta(F(slug), nombre, sub, alto=alto, lado=lado, tema="wow"), en=en, dur=dur,
                x=(.24 if lado == "izq" else .76), y=.54, sale=.3, nombre="silueta " + slug, ver=1.0)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(F(s), e) for s, e in fotos], tam, tema="wow"), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="abanico " + nombre, ver=1.2)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.5, zmin=1.0):
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin, objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.60, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel([(F(s), n) for s, n in fotos], tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus((F(a_[0]), a_[1]), (F(b_[0]), b_[1]), ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def P(x, y, rot, sub=None, foto=None):
    return (x, y, rot, sub, F(foto) if foto else None)


CAMARA = {}
FUNDIDO = {}
FX = [
    # =========================================================== gancho: MG desde el primer segundo
    mg(M.ocultos("SECRETOS DE LOS PRIMEROS NIVELES", [("Apagados en la beta", 0, ROJO), ("Desenterrados en una semana", 20, VERDE)],
                 ["inv_misc_questionmark", "inv_misc_map_01", "inv_misc_book_09", "spell_fire_fire"], "MUY BIEN ENTERRADOS", "20 SECRETOS"),
       ("Durante la beta de World of Warcraft", -.2), ("ya empezó a desenterrarlas|fin", .5),
       ["apagó los secretos", "Y en una semana", "hay cosas muy bien enterradas", "ya empezó a desenterrarlas"], "gancho ocultos", y=.55),
    carr([("terminator_t2", "Un brazo de Terminator"), ("ruinas_lordaeron", "Una estatua de ojos rojos"), ("o_antorcha", "Un guardia muerto"),
          ("moonrage", "Un pueblo que cambia"), ("sullivan", "Una carta de 1861"), ("ezra", "Una historia real")],
         "Un brazo de Terminator sobre un pedestal", ("casi nadie conoce|fin", .4),
         ["Una estatua con los ojos rojos", "Un guardia muerto", "Un pueblo entero", "Una carta real", "esconden una historia real"],
         titulo="HOY, LO QUE NADIE TE INDICA"),
    dict(tipo="mg", fn=PE.banda(F("o_carta"), "20 SECRETOS", "del 20 al 1 · con fuente y mapa", alto=380, tema="wow"),
         en=("Veinte secretos de los primeros niveles", -.2), dur=4.0, x=.5, y=.80, sale=.3, nombre="banda 20", ver=1.0),
    # =========================================================== Gaia Eterna
    rel("Se llama Gaia Eterna", "gaia_mini", "Gaia Eterna", "la historia de la Crematoria", dur=5.6, x=.72, y=.46, tam=640),
    filav("Alexandros, Renault, Darion, Tirion y Taelan", [("tirion", "Tirion", "Tirion y Taelan")], y=.66, tam=320, dur=3.6),
    com("Sayho escribió que le emocionaba", "UgwUAxVPSmsB1YOwyY54AaABAg", dur=4.4, x=.30, y=.30),
    com("y Pausa, que estaba buenísimo", "UgzrwqOhXZiG9GB95lh4AaABAg", dur=4.4, x=.66, y=.34),
    # =========================================================== 20 Zendraas
    rel("Número veinte. El vendedor", "zendraas", "Brother Zendraas", "el vendedor que desapareció"),
    mapa("zephras", [P(42.8, 23.5, "Thendal"), P(57.8, 52.0, "Santuario de Akir", "Zendraas · 58, 52")],
         ("En la Isla Zephras, la zona nueva", -.2), ("si sabías que existía|fin", .4),
         ["En la Isla Zephras", "Estaba más o menos en cincuenta y ocho"], "ISLA ZEPHRAS", "zona nueva de Forever"),
    dict(tipo="mg", fn=M.paradero("¿DÓNDE ESTÁ ZENDRAAS?", [(F("zendraas"), "Brother Zendraas", None)], ("SIN RASTRO", 1)),
         de=("Después del lanzamiento, los jugadores", -.2), a=("a ciertas horas|fin", .6),
         marcas=["y no estaba", "Unos dicen que lo quitaron"], x=.5, y=.62, sale=.4, nombre="MG paradero zendraas", ver=5.0),
    # =========================================================== 19 Pebblebitty
    pv("Número diecinueve. La enana", "pebblebitty", "Montañera Pebblebitty · Valle de los Reyes", dur=4.4, x=.76, y=.50, tam=470),
    mapa("loch_modan", [P(34, 47, "Thelsamar"), P(18.1, 83.8, "Pebblebitty", "18, 84 · túnel a la Garganta de Fuego", "pebblebitty")],
         ("En el extremo sur de Loch Modan", -.2), ("solo a nivel cuarenta y tantos|fin", .3),
         ["En el extremo sur", "Vigila el túnel"], "LOCH MODAN", "Valle de los Reyes"),
    mg(M.chat([("Sigue así y te enseño modales a golpes.", BLANCO), ("Estás tentando a la suerte.", BLANCO),
               ("No me obligues a ponerme medieval contigo.", AMAR)], "/rude"),
       ("si le haces el gesto de grosero", -.2), ("Una enana de Loch Modan citando|fin", .3),
       ["si le haces el gesto de grosero", "A veces escribe", "Otras: estás tentando", "Y la mejor"], "chat rude", y=.62, x=.30),
    # =========================================================== 18 Bom'bay
    rel("Número dieciocho. El médico brujo", "bombay_npc", "Bom'bay", "aprendiz de médico brujo"),
    mapa("durotar", [P(56, 75, "Poblado Sen'jin", "Bom'bay · 56, 75", "bombay_npc"), P(65, 85, "Islas del Eco", "Zalazane", "zalazane")],
         ("En Durotar, en el Poblado Sen'jin", -.2), ("de las Islas del Eco|fin", .5),
         ["En Durotar", "la misión de Zalazane"], "DUROTAR", "Poblado Sen'jin"),
    pv("Es el aprendiz del maestro Gadrin", "gadrin", "Maestro Gadrin", dur=3.4, x=.82, y=.60, tam=320),
    mg(M.chat([("Bom'bay: Eekum Bokum!", NAR)], "/hablar"),
       ("a veces escribe en el chat: Eekum Bokum", -.6), ("Eekum Bokum|fin", 2.4), ["mientras te transforma", "Eekum Bokum"], "chat bokum", y=.62, x=.30),
    vs(("mumbo", "Mumbo Jumbo · Banjo-Kazooie"), ("bombay_npc", "Bom'bay · Sen'jin"), ("Es el conjuro de Mumbo Jumbo", -.2),
       ("el brujo de la serie Hechizada|fin", .4), ["Es el conjuro de Mumbo Jumbo", "Y su nombre viene"], titulo="EL MISMO CONJURO"),
    # =========================================================== 17 Coldrasp
    pv("Número diecisiete. Coldrasp", "coldrasp", "Coldrasp · lobo espíritu · nivel 12", dur=4.4, x=.76, y=.50, tam=470),
    mapa("tirisfal", [P(31, 63, "Camposanto", "donde despiertan los no-muertos"), P(19.8, 65, "Coldrasp", "19, 65 · Bosque Susurrante")],
         ("Está al oeste de los Claros", -.2), ("diecinueve, sesenta y cinco|fin", .6),
         ["Está al oeste de los Claros", "Las coordenadas que comparten"], "CLAROS DE TIRISFAL", "solo en Forever"),
    # =========================================================== Overgear (hacia el minuto 4) + fondo de marca SIEMPRE
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="tú eliges, y pagas", a=("Número diecinueve. La enana", -.1),
         entra=.3, nombre="og fondo marca"),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True,
         de="Este video lo patrocina Overgear", a="El enlace está en la descripción, y por el lanzamiento", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="un profesional verificado", dur=4.0, sale=.25, nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="Talentos, rotación", dur=4.0, sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="tú eliges, y pagas", dur=4.0, sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción, y por el lanzamiento",
         a=CODIGO, entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a=("Número diecinueve. La enana", -.1), entra=.15, nombre="og CODIGO", ver=3.0),
    # =========================================================== 16 Mystmane
    mapa("zephras", [P(60.0, 33.5, "Mystmane", "60, 33"), P(59.3, 37.3, "hacia el sur", "59, 37")],
         ("Empieza en sesenta, treinta y tres", -.2), ("cincuenta y nueve, treinta y siete|fin", .6),
         ["Empieza en sesenta", "hasta cincuenta y nueve"], "ISLA ZEPHRAS", "oso raro · nivel 13"),
    mg(M.tiempos("VELOCIDAD DE ATAQUE", [("MYSTMANE · 1,6 s", 16, VERDE), ("OTROS OSOS · 2,0 s", 20, (110, 110, 130))], "+ Zarpazo: hasta 3 enemigos"),
       ("golpea cada un segundo y medio", -.6), ("hasta a tres enemigos a la vez|fin", .4),
       ["golpea cada un segundo y medio", "en vez de cada dos", "Y además conoce Zarpazo"], "velocidad oso", y=.62),
    # =========================================================== 15 Plata de las olas
    pv("Número quince. Plata de las olas", "o_munequera", "Plata de las olas · misión oculta", dur=4.4, x=.76, y=.50, tam=470),
    mapa("loch_modan", [P(45.6, 43.4, "Caja de pesca hundida", "45, 43 · bajo el agua")],
         ("La caja está en las coordenadas", -.2), ("Y no la vas a ver desde la orilla", .2),
         ["La caja está en las coordenadas"], "LOCH MODAN", "Plata de las olas", objeto="inv_misc_coin_17"),
    dict(tipo="mg", fn=PE.legajo(F("o_munequera"), "Pasador de plata", ["Iniciales grabadas: K.D.", "Empieza una misión"], ("OCULTA", 1), tema="wow"),
         en=("Dentro hay un pasador de pelo", -.2), dur=5.0, x=.76, y=.52, sale=.3, nombre="legajo pasador", ver=1.0),
    pv("te da una muñequera con intelecto", "o_munequera", "Muñequera · +2 Int +2 Esp", dur=4.0, x=.80, y=.60, tam=340),
    # =========================================================== gracias 1
    com("Ricochet escribió", "UgxlD-yqFaKQ8Tl40d94AaABAg", dur=4.0, x=.30, y=.30),
    com("Y Galaxy, con muchos signos", "UgzhzSe6o8IOFnL10-l4AaABAg", dur=4.0, x=.66, y=.34),
    com("Y Bajel dice que la voz de siempre", "UgzePOSYbB9-vgAYfEV4AaABAg", dur=5.6, x=.32, y=.32),
    # =========================================================== 14 Mankrik
    rel("Número catorce. ¿Dónde está", "olgra", "La esposa de Mankrik", "Perdidos en la batalla"),
    mapa("baldios", [P(52.0, 31.4, "El Cruce", "Mankrik"), P(49.3, 50.4, "La esposa de Mankrik", "al sur, cruzando el puente", "olgra")],
         ("Tienes que bajar al sur del Cruce", -.3), ("mirar frente a unas chozas|fin", .3),
         ["Tienes que bajar al sur", "Y lo que encuentras no se llama Olgra"], "LOS BALDÍOS", "nivel 14+"),
    mg(M.chat([("[General] ¿Dónde está la esposa de Mankrik?", AMAR), ("[General] ¿alguien sabe dónde está la esposa de Mankrik?", AMAR),
               ("[General] ¿DÓNDE ESTÁ LA ESPOSA DE MANKRIK?", ROJO)], "/1"),
       ("En el chat de Los Baldíos, todo el mundo", -.4), ("solo para molestar|fin", .3),
       ["todo el mundo preguntaba", "así que cada personaje", "Y muchos la hacían"], "chat mankrik", y=.62, x=.30),
    pv("Incluso salió en Hearthstone", "mankrik", "Mankrik · Hearthstone", dur=3.6, x=.80, y=.56, tam=420),
    # =========================================================== 13 Eitrigg
    pv("Número trece. Un orco", "eitrigg", "Eitrigg · consejero de Thrall", dur=4.4, x=.76, y=.50, tam=470),
    mapa("orgrimmar", [P(38, 37, "Bastión de Grommash", "Eitrigg, junto a Thrall", "eitrigg")],
         ("En Orgrimmar, dentro del Bastión", -.2), ("hay un orco viejo: Eitrigg|fin", .8),
         ["En Orgrimmar"], "ORGRIMMAR", "desde nivel 1"),
    cam("Ese paladín era Tirion", "tirion", "Tirion", dur=3.6, x=.18, y=.62),
    # =========================================================== 12 Piroleña
    rel("Número doce. El pueblo que cambia", "pyre_vigia", "Aldea Piroleña", "humanos de día"),
    mg(M.relojes("ALDEA PIROLEÑA", [("Hora del servidor", 21, 0, "los vecinos cambian")]),
       ("marca las nueve de la noche", -.6), ("haz la cuenta|fin", .3), ["marca las nueve de la noche"], "reloj pirolena", y=.60),
    vs(("pyre_vigia", "Vigía de Piroleña · de día"), ("moonrage", "Vigía Moonrage · de noche"), ("El anciano, el centinela", -.2),
       ("sea de la facción que sea|fin", .4), ["El anciano, el centinela", "se convierten en huargen"], ganador=1, titulo="21:00"),
    mapa("argenteos", [P(43, 41, "El Sepulcro", "Faerleia", "faerleia"), P(45, 67, "Colmillo Oscuro", "Arugal", "arugal"),
                       P(46, 72, "Aldea Piroleña", "nivel 15 · Horda", "morrison")],
         ("La culpa es del archimago Arugal", -.2), ("y a su alcalde, Morrison|fin", .5),
         ["La culpa es del archimago", "Y la Horda tiene misiones", "a su alcalde, Morrison"], "BOSQUE DE ARGÉNTEOS", "la maldición de Arugal"),
    # =========================================================== 11 Gilneas
    pv("Número once. Un reino entero", "muro", "Muro de Cringris · Gilneas, sellada", dur=4.4, x=.76, y=.50, tam=470),
    mapa("argenteos", [P(46, 72, "Piroleña"), P(50, 88, "Muro de Cringris", "detrás: Gilneas", "muro")],
         ("Al sur del Bosque de Argénteos", -.2), ("el Muro de Cringris|fin", .3),
         ["Al sur del Bosque", "hay un muro gigantesco"], "BOSQUE DE ARGÉNTEOS", "nivel 10-20"),
    cam("Genn Cringris, el rey", "genn", "Genn Cringris", dur=3.6, x=.82, y=.62),
    # =========================================================== burla 1
    com("Alfredo escribió", "UgzTnIrBYWqn820b1YB4AaABAg", dur=7.0, x=.32, y=.32),
    # =========================================================== 10 Sully Balloo
    rel("Número diez. Una carta", "o_carta", "La carta de Sully Balloo", "bajo el Puente de Thandol"),
    mapa("humedales", [P(49, 18, "Dun Modr"), P(51, 6, "Puente de Thandol", "el cadáver, bajo el agua", "thandol")],
         ("Entre Los Humedales y las Tierras Altas", -.2), ("Y con él, un sobre empapado|fin", .4),
         ["Entre Los Humedales", "Si te tiras al agua"], "LOS HUMEDALES", "nivel 20+"),
    pv("para su esposa, Sara Balloo", "sara", "Sara Balloo · Forjaz", dur=3.8, x=.80, y=.58, tam=380),
    dict(tipo="mg", fn=PE.legajo(F("o_carta"), "Mi querida Sara…", ["No me llores muerto.", "Piensa que me fui, y espérame:", "nos volveremos a ver."],
                                 None, tema="wow"),
         en=("La carta empieza así", -.2), dur=7.0, x=.70, y=.50, sale=.3, nombre="legajo carta", ver=1.0),
    sil("Sullivan Ballou, le escribió a su esposa", "sullivan", "Sullivan Ballou", "Ejército de la Unión · 1861", dur=6.0, lado="izq"),
    mg(M.cadena("LA CARTA REAL", [(F("sullivan"), "Sullivan Ballou", "14 de julio de 1861", False),
                                  (F("sullivan"), "Bull Run", "muere en la batalla", True),
                                  (F("o_carta"), "Sully Balloo", "bajo el Puente de Thandol", False)]),
       ("Fue una semana antes de la primera batalla", -.2), ("bajo un puente|fin", .4),
       ["Fue una semana antes", "Y Sullivan murió", "Y Blizzard la convirtió"], "cadena carta", y=.60),
    # =========================================================== 9 Terminator
    rel("Número nueve. El brazo de Terminator", "terminator", "El brazo de Terminator", "¿dónde está de verdad?"),
    mapa("humedales", [P(51, 6, "Puente de Thandol", "lo que dicen las listas", "thandol"), P(49, 18, "Dun Modr", "la misión del enano desaparecido", "dun_modr")],
         ("Muchas listas dicen que está dentro", -.2), ("a buscar a un enano desaparecido|fin", .4),
         ["Muchas listas dicen", "una misión de Dun Modr"], "PUENTE DE THANDOL", "¿el brazo está aquí?"),
    pant("terminator_wow", ("En la parte baja de la Cumbre", -.2), ("un brazo mecánico de metal|fin", .6), zoom=(1.0, 1.18), pan=(0, 0, -.04, -.02)),
    vs(("terminator", "En World of Warcraft"), ("terminator_t2", "En Terminator 2"), ("Es el brazo del primer Terminator", -.1),
       ("acaba creando a Skynet|fin", .5), ["Es el brazo del primer Terminator", "En Terminator dos"], titulo="EL MISMO BRAZO"),
    pv("Es el único de esta lista que no es de nivel bajo", "terminator", "Cumbre de Roca Negra inferior · nivel 56-60", dur=5.0, x=.76, y=.52, tam=640),
    # =========================================================== 8 Viktor (chimenea)
    rel("Número ocho. La chimenea", "ruinas_lordaeron", "Viktor el Vil", "jefe secreto"),
    mapa("tirisfal", [P(61, 72, "Ruinas de Lordaeron", "niveles 15-20", "ruinas_lordaeron")],
         ("una de ellas está sobre Entrañas", -.4), ("para los niveles quince a veinte|fin", .6),
         ["una de ellas está sobre Entrañas"], "CLAROS DE TIRISFAL", "mazmorra nueva de Forever"),
    mg(M.ocultos("RUINAS DE LORDAERON", [("Jefes que se ven", 0, BLANCO), ("Jefes secretos", 2, ROJO)],
                 ["inv_misc_questionmark", "spell_fire_fire", "spell_shadow_summonvoidwalker"], "VIKTOR EL VIL", None),
       ("escondidos en sus ruinas hay dos jefes", -.4), ("si no los buscas|fin", .4),
       ["escondidos en sus ruinas", "hay dos jefes"], "ocultos lordaeron", y=.60),
    mg(M.tiempos("LA CHIMENEA", [("Leña tibia: clic", 4, NAR), ("5 oleadas", 10, ROJO), ("VIKTOR EL VIL", 6, AMAR)], "Ruinas de Lordaeron · Forever"),
       ("Le haces clic, y empiezan las oleadas", -.3), ("aparece Viktor el Vil", -.15),
       ["Le haces clic", "Son cinco oleadas"], "oleadas viktor", y=.62),
    # =========================================================== 7 El Abandonado (estatua)
    pv("Número siete. La estatua", "s07_abandonado", "El Abandonado · la estatua de ojos rojos", dur=4.4, x=.76, y=.50, tam=470),
    mg(M.tiempos("LA ESTATUA", [("Te acercas", 3, NAR), ("3 oleadas", 9, ROJO), ("EL ABANDONADO", 6, AMAR)], "jefe secreto"),
       ("Si te acercas, llegan tres oleadas", -.3), ("el jefe secreto: El Abandonado|fin", .6),
       ["Si te acercas", "llegan tres oleadas", "Y después, aparece", "El Abandonado"], "oleadas abandonado", y=.62),
    # =========================================================== gracias 2
    com("Chino, que apenas empieza", "UgyYRdnI3UmDpDJdS8R4AaABAg", dur=5.6, x=.32, y=.32),
    com("Y Klb nos cuenta que Favorcraft", "UgwpComl30V1ZchiMFd4AaABAg", dur=6.0, x=.66, y=.34),
    # =========================================================== 6 Michel Koiter
    rel("Número seis. El santuario", "santuario", "Santuario del Guerrero Caído", "al oeste del Cruce"),
    mapa("baldios", [P(52, 31.4, "El Cruce"), P(47.5, 30, "Santuario del Guerrero Caído", "una loma al oeste", "santuario")],
         ("en una loma al oeste del Cruce", -.4), ("dos letras grabadas: M K|fin", .4),
         ["en una loma al oeste", "Se sube por la ladera"], "LOS BALDÍOS", "sin misión que te lleve"),
    mg(M.tiempos("MICHEL KOITER", [("1984 · nace", 20, (110, 110, 130)), ("MARZO 2004 · muere, 19 años", 4, ROJO),
                                   ("NOV 2004 · sale World of Warcraft", 3, AMAR)], "Twincruiser · con su gemelo René"),
       ("Murió en marzo de dos mil cuatro", -.4), ("todavía no había salido|fin", .5),
       ["Murió en marzo", "Tenía diecinueve años", "World of Warcraft todavía no"], "vida koiter", y=.60),
    # =========================================================== 5 Kyle
    pv("Número cinco. Kyle ha desaparecido", "kyle", "Kyle · el perro de Ahab", dur=4.4, x=.76, y=.50, tam=470),
    mapa("mulgore", [P(47, 59, "Poblado Pezuña de Sangre", "Ahab Wheathoof", "ahab")],
         ("En Mulgore, en el Poblado Pezuña de Sangre", -.2), ("perdió a su perro, Kyle|fin", .6),
         ["En Mulgore"], "MULGORE", "desde nivel 5"),
    pv("La misión te pide carne tierna", "o_carne", "Carne tierna de zancudo", dur=3.6, x=.18, y=.62, tam=320),
    sil("un niño de trece años, Ezra Chatterton", "ezra", "Ezra Chatterton", "Make-A-Wish · 2007", dur=6.0, lado="der"),
    # =========================================================== 4 ¡CLOC!
    rel("Número cuatro. El huevo de gallina", "pollo", "¡CLOC!", "el secreto con el que empezó todo"),
    mg(M.chat([("Haces cloc cloc al pollo.", NAR), ("El pollo te mira raro…", BLANCO), ("Misión: ¡CLOC!", AMAR)], "/chicken"),
       ("hazle el gesto de la gallina", -.4), ("te ofrece una misión|fin", 1.2),
       ["hazle el gesto de la gallina", "Una vez, y otra", "Hasta que el pollo te mira raro", "te ofrece una misión"], "chat chicken", y=.62, x=.30),
    mapa("poniente", [P(56, 31, "Granja de los Saldean", "pienso especial para pollos", "saldean")],
         ("La forma más fácil es en la granja", -.2), ("lo vende el mismo granjero|fin", .5),
         ["La forma más fácil"], "PÁRAMOS DE PONIENTE", "nivel 1"),
    filav("necesitas pienso especial para pollos", [("o_pienso", "Pienso especial para pollos", None),
                                                    ("o_huevo", "Huevo de pollo", "te deja un huevo"),
                                                    ("pollo", "Pollo de los Páramos", "un pollo de los Páramos")], y=.66, tam=300, dur=6.0),
    # =========================================================== 3 anillo
    pv("Número tres. El anillo heredado", "o_anillo", "Ancient Heirloom · Dawn Waker · parte 1", dur=4.4, x=.76, y=.50, tam=470),
    mg(M.cadena("EL DAWN WAKER", [(F("o_anillo"), "1 · El anillo", "Thendal · Zephras", False),
                                  (F("o_antorcha"), "2 · La antorcha", "Bosque del Ocaso", False),
                                  (F("o_eluviana"), "3 · Eluvi'ana", "Ruinas de Ban'aethal", True)], ("SIN RESOLVER", 3)),
       ("Los tres primeros puestos son", -.2), ("Y todavía nadie lo ha resuelto|fin", .6),
       ["Los tres primeros puestos", "el mismo secreto", "el primer gran secreto", "Y todavía nadie"], "cadena dawn waker", y=.58),
    mapa("zephras", [P(42.83, 23.45, "Thendal", "Ailee Farheart · 42, 23"), P(41.7, 23.4, "Rorian", "el anillo · o el piso de arriba", "o_anillo")],
         ("Empieza en la Isla Zephras", -.2), ("mira arriba|fin", .4),
         ["Empieza en la Isla Zephras", "La entregas a Rorian"], "ISLA ZEPHRAS", "La mayoría de edad", objeto="inv_jewelry_ring_03"),
    # =========================================================== 2 antorcha
    rel("Número dos. La antorcha", "o_antorcha", "Night Watchman's Torch", "Un final desafortunado"),
    mapa("ocaso", [P(21, 32, "Colina del Cuervo", "la cima del cementerio"), P(20.9, 34.4, "20, 34"), P(17, 54, "17, 54"),
                   P(30.0, 67.4, "30, 67"), P(45.9, 78.3, "45, 78"), P(47.8, 59.4, "47, 59", None, "o_antorcha")],
         ("El cuerpo no está siempre en el mismo sitio", -.2), ("en otros cinco lugares del bosque|fin", 2.4),
         ["El cuerpo no está siempre", "Lo han encontrado en la cima", "y en otros cinco", "otros cinco lugares", "del bosque#3",
          "en otros cinco lugares del bosque"], "BOSQUE DEL OCASO", "el guardia muerto · 6 sitios"),
    pv("Le quitas de la mano una antorcha", "o_antorcha", "Antorcha del vigilante nocturno", dur=4.0, x=.80, y=.58, tam=380),
    # =========================================================== 1 Eluvi'ana
    rel("Número uno. Eluvi'ana", "o_eluviana", "Eluvi'ana", "la espada del Dawn Waker", tam=560),
    mapa("zephras", [P(58.13, 24.06, "Ruinas de Ban'aethal", "la antorcha revela la empuñadura", "o_empunadura"),
                     P(65.94, 74.37, "Ealaane", "busca la hoja"), P(48.94, 72.68, "hoja · sitio 1"), P(50.4, 44.3, "hoja · sitio 2"),
                     P(66.25, 43.15, "hoja · sitio 3"), P(59.9, 82.2, "hoja · sitio 4", None, "o_hoja")],
         ("vuelves a la Isla Zephras, a las Ruinas", -.3), ("hay que recorrer Zephras con calma|fin", .4),
         ["a las Ruinas de Ban'aethal", "Se la llevas a Ealaane", "No tiene un lugar fijo", "en cuatro puntos distintos",
          "hay que recorrer", "con calma"], "ISLA ZEPHRAS", "Dawn Waker · parte 1", objeto="inv_sword_draenei_05"),
    mg(M.cadena("LA CADENA SIGUE", [(F("o_eluviana"), "Zephras", "nivel 1-12", False), (F("o_hoja"), "Costa Oscura y Brazanegra", "nivel ~22", False),
                                    (F("shendralar"), "Feralas · La Masacre", "nivel 40+", False),
                                    (F("tortheldrin"), "Eluvi'ana y Eluvi'tor", "Tortheldrin", True)], ("NADIE LO HA TERMINADO", 4)),
       ("Pero no termina ahí", -.2), ("Puede que sea la primera pieza|fin", .4),
       ["Pero no termina ahí", "La segunda parte llega", "Wowhead calcula", "habla de dos espadas", "Nadie ha terminado"], "cadena sigue", y=.58),
    # =========================================================== cierre
    carr([("terminator", "Brazo de Terminator"), ("sullivan", "Carta de 1861"), ("ezra", "Ezra"), ("santuario", "Michel Koiter")],
         "Un brazo de Terminator, una carta", ("su santuario en Los Baldíos|fin", .3),
         ["Un brazo de Terminator#2", "una carta de la Guerra", "un niño que le puso voz", "y un artista"], titulo="LO QUE NADIE TE INDICA"),
    rel("no olvides pasar por Gaia Eterna", "gaia_mini", "Gaia Eterna", "la Crematoria · enlace abajo", dur=5.0, x=.72, y=.46, tam=600),
    # ---- pegatinas añadidas tras el chequeo (densidad del canal 1,7/min)
    pv("en el Valle de los Reyes, hay una enana", "valle_reyes", "Valle de los Reyes", dur=3.8, x=0.18, y=.60, tam=340),
    pv("en el Poblado Sen'jin, vive", "senjin", "Poblado Sen'jin", dur=3.8, x=0.82, y=.60, tam=340),
    pv("encontrar a su esposa, Olgra", "olgra", "Olgra", dur=3.8, x=0.82, y=.60, tam=340),
    pv("está el Puente de Thandol, un puente enano", "thandol", "Puente de Thandol", dur=3.8, x=0.82, y=.60, tam=340),
    pv("un tauren llamado Ahab Wheathoof", "ahab", "Ahab Wheathoof", dur=3.8, x=0.82, y=.60, tam=340),
    pv("Le das la carne, Kyle se calma", "kyle", "Kyle", dur=3.8, x=0.18, y=.60, tam=340),
    pv("solo lo vende el granjero Saldean", "saldean", "Granjero Saldean", dur=3.8, x=0.82, y=.60, tam=340),
    pv("la cima del cementerio de la Colina del Cuervo", "colina_cuervo", "Colina del Cuervo", dur=3.8, x=0.18, y=.60, tam=340),
    pv("aparece una empuñadura antigua", "o_empunadura", "Ancient Hilt", dur=3.8, x=0.82, y=.60, tam=340),
    pv("te pide encontrar la hoja", "o_hoja", "Ancient Skyborne Blade", dur=3.8, x=0.18, y=.60, tam=340),
    pv("el príncipe Tortheldrin, en La Masacre", "tortheldrin", "Príncipe Tortheldrin", dur=3.8, x=0.82, y=.60, tam=340),
    pv("honorable con los Shen'dralar", "shendralar", "Shen'dralar", dur=3.8, x=0.18, y=.60, tam=340),
]
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]

# ============ 10-nov (sesión 4): TODO LO NOMBRADO SE MUESTRA — imágenes reales por puesto (propuestas A/B/C/D)
FX += [d for x in [
    # --- grupo A
    pant("s20_zendraas_vendedor", ("vendía equipo de nivel bajo", -.1), ("la moneda que se junta|fin", .2)),
    pant("s20_zendraas_dialogo", ("Un sectario que no te ataca", -.1), ("lo vieron en la beta lo recuerdan|fin", .2)),
    pant("s19_reja_llave", ("En Classic, ese paso tenía", -.1), ("a nivel cuarenta y tantos|fin", .2)),
    pant("s19_pebblebitty_reja", ("se quedaron mirando una puerta cerrada", -.1), ("se quedaron mirando una puerta cerrada|fin", .2)),
    pant("s17_coldrasp_doma", ("aparece un lobo espíritu raro", -.1), ("aparece un lobo espíritu raro|fin", .3)),
    pant("s17_coldrasp_translucido", ("Es azul, translúcido, como un", -.1), ("como un fantasma|fin", .3)),
    pant("s17_coldrasp_mascota", ("no lo mates: dómalo", -.1), ("no lo mates: dómalo|fin", .5)),
    pv("Número dieciséis. Mystmane, el oso", "s16_mystmane_ficha", "Mystmane · oso raro, nivel 13", dur=4.6, x=.26, y=.52, tam=640),
    vs(("s16_mystmane_nombre", "Mystmane"), ("s16_dendralass_nombre", "Den'dralass"), ("Hay otro oso idéntico en", -.1),
       ("antes de domarlo|fin", .3), ["Hay otro oso idéntico"], titulo="MISMO OSO, OTRO NOMBRE"),
    pant("s16_mystmane_doma", ("Y Mystmane derriba", -.1), ("te corta la doma|fin", .3)),
    # --- grupo B
    pv("con dos iniciales grabadas", "s15_mision_plata", "Silver of the Waves · «K.D.»", dur=5.2, x=.72, y=.50, tam=680),
    pant("s15_khara_orilla", ("Esas iniciales son de Khara", -.1), ("Esas iniciales son de Khara|fin", .4)),
    pant("s14_mankrik_choza", ("En el Cruce, en Los Baldíos", -.1), ("hay un orco que no descansa", .9)),
    pv("Así nació el primer gran meme", "s14_there", "Wowhead · «THERE»", dur=5.0, x=.72, y=.50, tam=680),
    pv("Mankrik acabó enterrando a su esposa", "s14_olgra_tumba", "La tumba de Olgra", dur=5.0, x=.72, y=.50, tam=640),
    pv("está la Aldea Piroleña, un pueblo", "s12_pirolena_dia", "Aldea Piroleña · de día", dur=5.0, x=.30, y=.50, tam=750),
    pv("Desde el castillo que domina el pueblo", "s12_colmillo_castillo", "Castillo de Colmillo Oscuro", dur=5.0, x=.74, y=.50, tam=640),
    pant("s12_huargen_flow", ("un pueblo lleno de huargen", -.3), ("un pueblo lleno de huargen|fin", .6)),
    pant("s07_estatua_flow", ("hay una estatua con los ojos rojos", -.4), ("hay una estatua con los ojos rojos|fin", .6), zoom=(1.0, 1.2)),
    pant("s01_empunadura_flow", ("Usas la antorcha, y aparece una empuñadura antigua", -.1), ("que antes no estaba ahí", .4)),
    pant("s01_altonato_flow", ("en la Playa de Zoram aparece", -.1), ("Y en Feralas hay una bóveda", -.1), zoom=(1.0, 1.15)),
    pv("encontraron una fila de campo de batalla", "s11_bg_gilneas", "Campo de batalla de Gilneas", dur=5.0, x=.26, y=.50, tam=620),
    pant("s11_muro_frente", ("a nivel quince ya puedes plantarte frente al muro", -.1), ("en lo que viene|fin", .3)),
    # --- grupo C
    pant("s10_cadaver", ("encuentras un cadáver", -.2), ("Y con él, un sobre empapado", -.1)),
    pant("s10_sobre_empapado", ("Y con él, un sobre empapado", -.1), ("Y con él, un sobre empapado|fin", .4)),
    pv("Y empieza una misión: llevársela", "s10_carta_mision", "Sully Balloo's Letter", dur=4.8, x=.72, y=.50, tam=660),
    pant("s08_lena_tibia", ("Dentro, en la chimenea, hay leña tibia", -.1), ("Le haces clic, y empiezan las oleadas", -.35)),
    pant("s08_viktor_aparece", ("aparece Viktor el Vil", -.1), ("aparece Viktor el Vil|fin", .5)),
    pv("abandonado por todos los grupos", "s07_abandonado", "El Abandonado · jefe secreto", dur=4.6, x=.74, y=.52, tam=660),
    carr([("s08_viktor", "Viktor el Vil"), ("s07_abandonado", "El Abandonado")], ("Dos jefes ocultos en una mazmorra", -.2),
         ("Dos jefes ocultos en una mazmorra|fin", .3), ["Dos jefes ocultos"], titulo="LOS DOS JEFES OCULTOS"),
    pant("s06_koiter_sanador", ("un sanador espiritual, que se llama Koiter", -.2), ("un sanador espiritual, que se llama Koiter|fin", .4)),
    sil("Michel Koiter era uno de los artistas", "s06_michel_koiter", "Michel Koiter", "artista de Blizzard · 1984-2004", dur=5.0, lado="izq"),
    pant("s06_estatua_orco", ("La estatua de ese orco es una copia exacta", -.1), ("La estatua de ese orco es una copia exacta|fin", .3)),
    pant("s06_koiter_sanador", ("quien te devuelve a la vida es Koiter", -.2), ("quien te devuelve a la vida es Koiter|fin", .4)),
    pv("Raynor recoge la placa de un marine caído", "s06_placa_koiter", "StarCraft II · «M. KOITER»", dur=4.8, x=.72, y=.50, tam=620),
    # --- grupo D
    pv("Ezra murió poco después", "s05_ezra_memorial", "Blizzard · In Memory of Ezra", dur=5.0, x=.70, y=.50, tam=680),
    pant("s04_cloc_mision", ("una misión: ¡Cloc!", -.3), ("una misión: ¡Cloc!|fin", .8)),
    pant("s04_huevo_gigante", ("Le das el pienso al pollo", -.1), ("sale tu mascota|fin", .3)),
    pv("el Ancient Heirloom", "s03_anillo_tooltip", "Ancient Heirloom", dur=5.0, x=.26, y=.50, tam=640),
    pant("s02_antorcha_mision", ("Le quitas de la mano una antorcha", -.1), ("lo que esconde la oscuridad|fin", .3)),
    pv("Es un objeto de nivel uno", "s02_antorcha_tooltip", "Antorcha del Vigía Nocturno", dur=5.0, x=.26, y=.50, tam=620),
    pv("Alrededor hay necrófagos", "s02_necrofago", "Necrófago · nivel 25", dur=4.4, x=.24, y=.56, tam=520),
] for d in (x if isinstance(x, list) else [x])]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="RECREACIÓN", en="un pueblo lleno de huargen", dur=3.0, tam=54, color="blanco", y=.93),
    dict(texto="RECREACIÓN", en="hay una estatua con los ojos rojos", dur=3.0, tam=54, color="blanco", y=.93),
    dict(texto="RECREACIÓN", en="Usas la antorcha, y aparece una empuñadura antigua", dur=3.0, tam=54, color="blanco", y=.93),
    dict(texto="RECREACIÓN", en="en la Playa de Zoram aparece", dur=2.8, tam=54, color="blanco", y=.93),
    dict(texto="APAGARON LOS SECRETOS", en="apagó los secretos", dur=2.6, tam=120, color="rojo", y=.2),
    dict(texto="/rude", en="barra rude", dur=2.2, tam=160, color="amarillo", y=.2),
    dict(texto="EEKUM BOKUM", en="Eekum Bokum", dur=2.4, tam=140, color="amarillo", y=.2),
    dict(texto="1,6 s", en="golpea cada un segundo y medio", dur=2.2, tam=160, color="amarillo", y=.2),
    dict(texto="K.D.", en="K punto D punto", dur=2.4, tam=170, color="amarillo", y=.2),
    dict(texto="21:00", en="las nueve de la noche", dur=2.4, tam=170, color="rojo", y=.2),
    dict(texto="1861", en="mil ochocientos sesenta y uno", dur=2.4, tam=170, color="amarillo", y=.2),
    dict(texto="M K", en="dos letras grabadas: M K", dur=2.6, tam=170, color="amarillo", y=.2),
    dict(texto="19 AÑOS", en="Tenía diecinueve años", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="/chicken", en="barra chicken", dur=2.2, tam=160, color="amarillo", y=.2),
    dict(texto="¿MITO?", en="Pero recorrí esas salas de punta a punta", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="NIVEL 40+", en="nivel cuarenta o más", dur=2.4, tam=140, color="amarillo", y=.2),
]
SFX = {}
# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/wow/, copiado a sfx/), solo en momentos clave
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.28) for e in ("Número veinte.", "Número quince", "Número diez", "Número cinco")]
PISTAS += [dict(sfx="mision_completada", en=e, vol=.22) for e in ("te ofrece una misión: ¡Cloc!", "te dan Eluvi'ana")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Veinte secretos de los primeros niveles", "Número uno. Eluvi'ana")]
# SI LA VOZ NOMBRA UN SONIDO, SE OYE (31-oct): «Escucha un pedazo» = la Crematoria con su audio (voz=True agacha la música)
PISTAS += [dict(sfx="oye_crematoria", en=("Escucha un pedazo|fin", .15), vol=1.0, voz=True)]

# APOYOS: tarjetas SOLO con datos del guion (fuentes en videos/_investigacion_wow_secretos_primeros_niveles.md)
APOYOS = [
    dict(en="vendía equipo de nivel bajo", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Brother Zendraas", calidad="amarillo",
         icono="inv_misc_coin_01", lineas=["Vendía equipo de nivel bajo", dict(t="Pago: piedras de viento", c=V)])),
    dict(en="Pero su ayuda es un maleficio al azar", dur=6.0, x=.72, size=.50, tarjeta=dict(titulo="Maleficios de Bom'bay", calidad="morado",
         icono="spell_shadow_summonvoidwalker", lineas=["Bicho · Borracho · Fantasma", "Gigante 5 min", dict(t="Lanzado: ¡ve con la vida llena!", c=RJ)])),
    dict(en="Se llama Coldrasp. Y no estaba", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Coldrasp", calidad="azul",
         icono="spell_shadow_summonvoidwalker", lineas=["Lobo espíritu raro · nivel 12", dict(t="Domable · solo en Forever", c=V)])),
    dict(en="Ahora, la trampa", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Mira el nombre", calidad=RJ, icono="inv_misc_questionmark",
         lineas=["Mystmane: el rápido", dict(t="Den'dralass: idéntico", c=RJ)])),
    dict(en="Para llegar hay que bucear", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="Ojo bajo el agua", calidad=RJ, icono="inv_misc_note_01",
         lineas=["Trillones jóvenes de más nivel", dict(t="Entra rápido, sal más rápido", c=V)])),
    dict(en="Su misión se recoge desde nivel catorce", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Perdidos en la batalla", calidad="amarillo",
         icono="inv_misc_map_01", lineas=["Requiere nivel 14", "Sin flecha ni marca", dict(t="Sigue en Forever", c=V)])),
    dict(en="Blizzard quitó todo esto en Cataclysm", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Piroleña", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Quitado en Cataclysm", dict(t="En Forever, la maldición sigue", c=V)])),
    dict(en="Y no está vacía", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Gilneas en los archivos", calidad="morado",
         icono="inv_misc_questionmark", lineas=["Zona sellada", dict(t="Fila de campo de batalla · 10 jugadores", c=V)])),
    dict(en="los Hierro Negro y los de Forjaz", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Dos guerras civiles", calidad="amarillo",
         icono="inv_misc_note_02", lineas=["Estados Unidos · 1861", dict(t="Forjaz vs Hierro Negro · 200 años", c=GR)])),
    dict(en="Y cuando le hice clic para cogerlo", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Brazo de Terminator", calidad="naranja",
         icono="trade_engineering", lineas=["Clic para cogerlo: desaparece", dict(t="Nunca llega a tu bolsa", c=RJ)])),
    dict(en="Blizzard lo volvió a recordar en StarCraft", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="StarCraft II", calidad="azul",
         icono="inv_misc_note_02", lineas=["Raynor recoge una placa", dict(t="«M. Koiter»", c=V)])),
    dict(en="Kaivax, de Blizzard, contestó", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Kyle vuelve", calidad="verde",
         icono="inv_misc_note_01", lineas=["Era de Burning Crusade", "Los jugadores lo pidieron", dict(t="Vuelve en la beta · nivel 5", c=V)])),
    dict(en="Ojo: la misión del pollo dura poco", dur=4.6, x=.72, size=.50, tarjeta=dict(titulo="¡CLOC!", calidad=RJ, icono="inv_misc_note_01",
         lineas=["La misión dura poco", dict(t="Acéptala rápido", c=V)])),
    dict(en="Es un objeto de nivel uno, tiene treinta segundos", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Night Watchman's Torch", calidad="verde",
         icono="spell_fire_fire", lineas=["Nivel 1 · 30 s de reutilización", "Ocupa hueco en la bolsa", dict(t="No funciona en posadas ni capitales", c=RJ)])),
    dict(en="Algunos creen que al final pide reputación", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Sin confirmar", calidad=RJ,
         icono="inv_misc_questionmark", lineas=["Honorable con los Shen'dralar", dict(t="Nadie lo ha comprobado", c=GR)])),
]
