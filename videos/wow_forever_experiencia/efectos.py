# -*- coding: utf-8 -*-
"""EFECTOS de «30 cosas para vivir la experiencia REAL de WoW Forever» (12-nov-2026; helpers de wow_errores_30_60).
Pegatinas (pv/rel/cam/ban/sil), comentarios (com), mapas con ruta (mapa), MG de mg_wow (mg). SIN Overgear (el usuario, 12-nov-2026).
python fab.py wow_forever_experiencia fx --seco · FAB_FX_FINAL=1 python fab.py wow_forever_experiencia fx hoja"""
import os

import mg_tes as T
import mg_wow as M
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
TEMA_PEG = "wow"
AMAR, ROJO, VERDE, BLANCO, NAR = (255, 255, 160), (255, 70, 60), (40, 210, 90), (240, 240, 240), (255, 150, 60)
V, GR, RJ = "verde", "gris", "#ff3b3b"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    if slug.startswith("o_"):
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PA.variado(F(slug), titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6):
    xs = (.14, .32, .50, .68, .86)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="comentario " + id_, ver=1.0)


def rel(en, slug, nombre=None, sub=None, dur=4.2, x=.76, y=.52, tam=500):
    if slug.startswith("o_"):   # íconos de 56 px: más chicos, que no se vean borrosos (regla 10-nov)
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.4)):
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def ban(en, slug, nombre, sub=None, dur=4.0, x=.5, y=.78, tam=420):
    return dict(tipo="mg", fn=PE.banda(F(slug), nombre, sub, alto=tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def sil(en, slug, nombre, sub=None, dur=4.4, lado="izq", alto=820, marco="museo"):
    # PERSONAS REALES = OPACAS (el usuario, 10-nov-2026): PE.silueta recortaba con rembg y la foto de Michel Koiter salía
    # translúcida, fundida con el gameplay. Ahora retrato con marco opaco a media pantalla (antes PE.silueta).
    return pv(en, slug, nombre, dur=dur, x=(.25 if lado == "izq" else .75), y=.50, tam=640,
              marco=marco, estancia="kenburns")


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
EXP = "inv_misc_book_11"   # ícono de experiencia


FX = [
    # =========================================================== gancho: Alberto + dos formas de jugar
    com("Hace unos días, Alberto nos escribió", "Ugzmf-vgaHwmGz-F4_J4AaABAg", dur=7.0, x=.32, y=.30),
    pv("Nadie te está esperando en el nivel sesenta", "villa_lago", "Villa del Lago · Montes Crestagrana", dur=4.2, x=.74, y=.55, tam=560),
    mg(M.calendario("UNA SEMANA DE WOW FOREVER", 4, 3, 9, [(0, 0, "Lanzamiento", AMAR), (1, 4, "Rutas óptimas · listas de errores", ROJO),
                                                       (5, 8, "Ya hay gente en el 60", ROJO)], hoy=8),
       ("World of Warcraft Forever salió el cuatro", -.2), ("Y hoy vamos a hacer justo lo contrario|fin", .2),
       ["salió el cuatro de noviembre", "rutas óptimas", "ya llegó al sesenta"], "semana de Forever", y=.56),
    mg(M.tiempos("EL TECHO DE FOREVER", [("Nivel 1 → 60", 60, VERDE), ("60 · para siempre", 40, AMAR)], "Lo nuevo crece hacia los lados"),
       ("Y aquí está lo curioso: Forever", -.2), ("el leveleo no es el trámite: es el juego|fin", .3),
       ["El nivel máximo es sesenta", "Lo nuevo va a crecer hacia los lados"], "techo 60", y=.56),
    dict(tipo="mg", fn=PE.banda(F("hogger"), "30 COSAS PARA VIVIR FOREVER", "del 30 al 1 · sin correr al 60", alto=380, tema="wow"),
         en=("Hoy te traigo treinta cosas", -.2), dur=5.0, x=.5, y=.80, sale=.3, nombre="banda 30", ver=1.0),
    # =========================================================== fricción (análisis)
    mg(M.contadores("FRICCIÓN: LO QUE EL JUEGO TE PONE EN MEDIO", [("ability_tracking", "Caminar", 10, 0, 1), ("ability_warrior_challange", "Misión de élite", 1, 1, 2),
                                                                 ("inv_ammo_arrow_02", "Flechas que se acaban", 200, 2, 3), ("inv_letter_15", "Preguntar en el chat", 1, 3, 4)],
                    ("Y POR ESO TODO PESA", 4)),
       ("Fricción es todo lo que el juego te pone en medio", -.2), ("Pero esa fricción era la que hacía que todo pesara|fin", .3),
       ["caminar diez minutos", "no poder hacer una misión solo", "quedarte sin flechas", "tener que preguntar", "Pero esa fricción"], "fricción", y=.56),
    mg(M.tiempos("CÓMO MIDE LA MEMORIA UN VIAJE", [("Mazmorra rápida", 32, ROJO), ("Los Baldíos · 10 lugares", 68, VERDE)],
                 "Un recuerdo por lugar, no por minuto"),
       ("Y hay un truco de la memoria", -.2), ("la primera vez que cruzaron Los Baldíos|fin", .4),
       ["no medimos el tiempo en minutos", "Un viaje con diez lugares", "la primera vez que cruzaron"], "memoria", y=.56),
    # =========================================================== 30 apellido
    mg(M.reglas("ELIGE TU CONJUNTO DE REGLAS", [("achievement_bg_winwsg", "Normal"), ("ability_dualwield", "JcJ"), ("inv_misc_book_09", "Juego de rol"),
                                                ("inv_misc_book_11", "Rol JcJ")], 2, "NO SE CAMBIA LIBREMENTE"),
       ("Parece una tontería, pero empieza en la pantalla", -.2), ("Un enano que se llama Brogan", -.9),
       ["Normal, JcJ", "Juego de rol y Juego de rol JcJ", "Y en los de rol"], "reglas", y=.56),
    mg(M.nombre("NOMBRE Y APELLIDO", [("xXmatadorXx", "", False, "nadie se imagina nada"), ("Brogan", "Barbapétrea", True, "una familia, una mina, una deuda")]),
       ("Un enano que se llama Brogan", -.6), ("se imagine algo|fin", .3), ["Un enano que se llama", "una deuda en la taberna"], "nombre", y=.56),
    # =========================================================== 29 español
    mg(M.chat([("[1. General] Thorin: ¿dónde está el entrenador de pesca?", (255, 192, 160)),
               ("[1. General] Lúmina: junto al lago, sigue el camino", (255, 192, 160)),
               ("[1. General] Kebabero: vendo agua, 1 de plata", (255, 192, 160)),
               ("[1. General] Grumok: jajaja", (255, 192, 160))], "Hola a todos, ¿alguien para Hogger?"),
       ("Y ese chat es medio juego", -.3), ("y tres respondiéndole|fin", .4), ["Gente preguntando", "otro vendiendo agua", "otro contando un chiste", "y tres respondiéndole"],
       "chat general", x=.30, y=.60),
    dict(tipo="mg", fn=PE.legajo(F("h_conjurar_agua"), "IDIOMA PREFERIDO", ["Opciones → Idiomas y redes sociales", "Toda la cuenta", "Enfriamiento: 24 h"],
                                  sello=("ESPAÑOL", 2), tema="wow"), en=("En Forever no hay reinos fijos", .2), dur=6.0, x=.72, y=.50, sale=.3, nombre="legajo idioma", ver=1.0),
    # =========================================================== 28 clase por fantasía
    filav("El mago se hace su propia comida", [("o_agua", "Mago: comida y agua gratis", None), ("o_flecha", "Cazador: compra flechas", "El cazador tiene que comprar"),
                                               ("o_fragmento", "Brujo: fragmentos de alma", "Y el brujo carga")], y=.64, tam=320, dur=5.4),
    filav("Pero el brujo también puede invocar", [("h_invocar", "Ritual de invocación", None), ("h_gato", "Druida: forma felina", "Y el druida se convierte en gato")],
          y=.64, tam=320, dur=5.0),
    mapa("azeroth_eses", [P(48, 62, "Dun Morogh", "enanos y gnomos"), P(43, 13, "Teldrassil", "elfos de la noche")],
         ("Y la raza también cuenta", -.2), ("aunque juegues la misma clase|fin", .2), ["nieve de Dun Morogh", "en Teldrassil"], "AZEROTH", "dónde empieza cada raza"),
    # =========================================================== burla0 (Arnold)
    com("Arnold escribió: deja a Marcos", "UgzPrV6Ty2-aLcalmSF4AaABAg", dur=6.4, x=.32, y=.30),
    # =========================================================== 27 leer misiones + add-on
    mapa("ocaso", [P(75, 45, "Villa Oscura", "una viuda", None)], ("Una viuda en el Bosque del Ocaso", -.2), ("Una viuda en el Bosque del Ocaso", 2.6),
         [], "BOSQUE DEL OCASO", "cada misión, una historia"),
    mapa("poniente", [P(56, 31, "Granja Saldean", "un granjero que lo perdió todo")], ("un granjero de los Páramos de Poniente", -.4),
         ("un orco en Durotar", -.2), [], "PÁRAMOS DE PONIENTE", "cada misión, una historia"),
    mg(M.hecho_en_casa("LO HICIMOS NOSOTROS", [("inv_misc_book_09", "Voces en español", "Misiones con voz", "una voz por personaje")], "GRATIS"),
       ("nosotros hicimos un add-on gratis", -.3), ("Escucha a tu primer PNJ|fin", .1), ["que le pone voz en español", "Se llama Voces en español"], "add-on Voces", y=.56),
    # add-on Voces: la GRABACIÓN de OBS del usuario (g1, Willem habla desde el seg. 8,1 = sfx oye_willem); sincronizada con la PISTA
    dict(tipo="video", ruta="D:/wowForeverVoces/grabaciones_obs/2026-11-07 11-35-43.mp4", desde=4.25,
         de=("Escucha a tu primer PNJ|fin", -3.85), a=("Escucha a tu primer PNJ|fin", 5.5), entra=.3, sale=.3, nombre="OBS add-on Voces", ver=2.0),
    # =========================================================== burla1 (Fetixe)
    com("Fetixe escribió: fomentando addons", "Ugw5eSQe9hTLTc9QKAF4AaABAg", dur=6.6, x=.32, y=.30),
    mg(M.enlaces("EN LA DESCRIPCIÓN", [("inv_misc_book_09", "Voces en español", "CurseForge · gratis"), ("inv_misc_coin_03", "Donación voluntaria", "para doblar más misiones")],
                 "Gratis para siempre"),
       ("Lo único que pedimos es una donación", -.2), ("Lo estamos intentando hacer hablar|fin", .3), ["Lo único que pedimos", "Igual que el mendigo"], "enlaces", y=.56),
    # =========================================================== 26 sin flechas
    rel("Número veintiséis. Apaga las flechas", "o_garra", "Sin flechas en el mapa", "lee, mira el mapa, pregunta"),
    mapa("elwynn", [P(42, 65, "Villadorada"), P(32, 50, "Mina de los Ecos", "campamento de gnolls")], ("Lee dónde dice el texto", -.2), ("sigue los postes del camino|fin", .3),
         ["mira el mapa", "y sigue los postes"], "BOSQUE DE ELWYNN", "guíate por el texto y los postes"),
    # =========================================================== 25 Hogger
    sil("Hogger, el gnoll de élite", "hogger", "Hogger · élite nivel 11", "veinte años humillando humanos", dur=5.0, lado="der"),
    mapa("elwynn", [P(42, 65, "Villadorada", "tres desconocidos"), P(27, 86, "Hogger", "el gnoll de élite", "hogger")], ("Si vas solo, Hogger te destroza", -.2),
         ("No hace falta decir mucho|fin", .3), ["Pero cuando ves a tres jugadores"], "BOSQUE DE ELWYNN", "Hogger, al suroeste", zmax=1.7),
    mg(M.grupos("EL GRUPO DE HOGGER", [(1, "ability_warrior_defensivestance", "tanque", AMAR), (1, "spell_holy_flashheal", "sanador", VERDE),
                                       (1, "ability_rogue_sprint", "cebo", ROJO)]),
       ("Y pasa algo muy curioso", -.2), ("el más valiente le hace de cebo|fin", .4), ["uno pone el cuerpo", "otro cura", "el más valiente"], "grupo de Hogger", y=.60),
    # =========================================================== 24 a pie
    mapa("elwynn", [P(42, 65, "Villadorada"), P(30, 62, "puente"), P(24, 72, "granja"), P(10, 72, "hacia los Páramos")], ("Vas a pasar por un puente", -.3),
         ("se te queda en la memoria|fin", .3), ["un puente", "una granja", "una torre en ruinas", "un río con múrlocs"], "A PIE", "cada lugar, un recuerdo"),
    rel("Y cuando por fin llegas a un maestro de vuelo", "grifo", "Maestro de vuelo", "solo si descubriste la parada", x=.74),
    # =========================================================== 23 zepelín y barco
    mapa("azeroth_eses", [P(71, 45, "Orgrimmar"), P(44, 35, "Entrañas"), P(48, 83, "Grom'gol", "Vega de Tuercespina")],
         ("Entre Orgrimmar, Entrañas y la Vega", -.2), ("navegan los barcos", -1.6), ["Entrañas", "y la Vega de Tuercespina"], "ZEPELINES DE LOS GOBLINS", "Horda"),
    mapa("azeroth_eses", [P(47, 52, "Menethil"), P(66, 62, "Theramore"), P(25, 26, "Auberdine")],
         ("Y entre Menethil, Theramore y Auberdine", -.2), ("ir por un café|fin", .2), ["Theramore", "y Auberdine"], "BARCOS", "Alianza"),
    # =========================================================== 22 campamento
    mg(M.experiencia("EL CAMPAMENTO DE FOREVER", [("spell_fire_fire", "Hoguera · Cocina"), ("inv_misc_bag_10", "Tienda · Peletería"),
                                                   ("inv_banner_01", "Estandarte · Sastrería"), ("inv_misc_fish_02", "Pecera · Pesca")],
                     ("SIÉNTATE UN RATO JUNTO AL FUEGO", 4)),
       ("Un cocinero enciende la hoguera", -.2), ("y si hay más gente, mejor|fin", .4),
       ["una tienda de campamento", "un estandarte", "una vela, hasta una pecera", "hay que quedarse sentado"], "campamento", y=.56),
    rel("Número veintidós. Enciende el campamento", "h_fogata", "Hoguera", "la nueva posada", x=.76),
    # =========================================================== 21 pesca
    rel("Número veintiuno. Sube la pesca", "o_cana", "Caña de pescar", "un rato de calma"),
    carr([("ventormenta", "Ventormenta"), ("villa_lago", "Villa del Lago")], ("Te sientas en un muelle", -.2), ("Villa del Lago, Alberto|fin", .3),
         ["En Ventormenta", "en el lago de Villa del Lago"], titulo="DÓNDE PESCAR"),
    mapa("tuercespina", [P(27, 77, "Bahía del Botín", "concurso de pesca · domingos")], ("Y el concurso de pesca de los domingos", -.2), ("se cambia en Bahía del Botín|fin", .3),
         [], "VEGA DE TUERCESPINA", "concurso de pesca · ganan los primeros 50"),
    # =========================================================== gracias1
    com("Yorsh escribió que sigue el canal", "UgzR5v08f7FdbdXZmMV4AaABAg", dur=7.0, x=.32, y=.30),
    com("Y Pablo escribió algo", "UgxbKVvAKhKBLZttjG94AaABAg", dur=6.0, x=.66, y=.34),
    # =========================================================== 20 comerciante
    mg(M.subasta("LA TIENDA DE LA POSADA", [("inv_misc_fish_02", "Pescado asado", "1 de plata", AMAR), ("inv_drink_18", "Agua fresca", "1 de plata", AMAR),
                                           ("inv_misc_bag_10", "Bolsa de lino", "regalo", VERDE)], "HECHO POR TI", cab=("PRODUCTO", "PRECIO")),
       ("Cocina pescado y véndelo", -.2), ("y la gente hace fila para comprarles|fin", .3), ["Fabrica bolsas", "Abre una tienda", "Hay jugadores que se hicieron"], "tienda", y=.56),
    mapa("crestagrana", [P(18, 64, "Three Corners", "Autoridad Comercial de Azeroth")], ("La Alianza tiene a la Autoridad", -.2),
         ("La Alianza tiene a la Autoridad", 3.4), [], "MONTES CRESTAGRANA", "Alianza · Favor de comerciante"),
    mapa("baldios", [P(50.0, 29.2, "Dokimi", "Logística y suministros de Durotar")], ("y la Horda, Logística y suministros", -.2),
         ("también es negocio|fin", .2), [], "LOS BALDÍOS", "Horda · Favor de comerciante"),
    # =========================================================== 19 mazmorra a pie
    mapa("poniente", [P(56, 47, "Colina del Centinela"), P(42, 72, "Arroyoplata", "entrada", "minas")], ("Las Minas de la Muerte, en los Páramos", -.2),
         ("Las Cuevas de los Lamentos", -.2), [], "MINAS DE LA MUERTE", "Páramos de Poniente"),
    mapa("baldios", [P(52, 30, "El Cruce"), P(46, 36, "Oasis", "entrada", "lamentos")], ("Las Cuevas de los Lamentos", -.2), ("antes de la primera pelea|fin", .3),
         [], "CUEVAS DE LOS LAMENTOS", "Los Baldíos"),
    mg(M.chat([("[Buscar grupo] Thalia: ¡yo voy de tanque!", (255, 192, 160)), ("[Grupo] Thalia: nos vemos en la Colina del Centinela", (170, 170, 255)),
               ("[Grupo] Brogan: llevo comida para todos", (170, 170, 255))], "Busco tanque para las Minas de la Muerte"),
       ("Escribes en el chat que buscas tanque", -.2), ("ya están charlando|fin", .3), ["Alguien contesta", "Se juntan en el pueblo"], "buscar grupo", x=.30, y=.60),
    # =========================================================== 18 hermandad
    mg(M.capas("CAPAS DE FOREVER", "inv_shirt_guildtabard_01", "spell_holy_prayerofspirit", "TU HERMANDAD, EN TU CAPA"),
       ("Y en Forever esto tiene premio extra", -.2), ("es la gente que te vas a ir cruzando|fin", .3),
       ["El sistema de capas", "siempre se vean en el mundo", "Y quien agrupó contigo"], "capas hermandad", y=.56),
    # =========================================================== 17 posada
    rel("Número diecisiete. Descansa en la posada", "o_hogar", "Piedra de hogar", "átala a tu posada"),
    mg(M.experiencia("EL DESCANSO DE LA POSADA", [("spell_nature_sleep", "Bien descansado"), ("inv_misc_rune_01", "Desconectado en la posada")],
                     ("×2 POR CADA ENEMIGO", 2)),
       ("Cuando te desconectas en una posada", -.2), ("literalmente|fin", .3), ["acumulas descanso", "Y al volver", "Así que el juego te premia"], "descanso", y=.56),
    # =========================================================== 16 misiones de clase
    carr([("h_diablillo", "Brujo · su primer diablillo"), ("h_sucubo", "Brujo · súcubo")],
         ("El brujo empieza sin demonio", -.2), ("y más adelante ata a su súcubo", 1.2),
         ["y más adelante ata a su súcubo"], titulo="MISIONES DE CLASE"),
    rel("El chamán recorre el mundo buscando", "h_totem", "Tótems del chamán", "tierra · fuego · agua · aire", x=.76),
    filav("El druida aprende a convertirse en oso", [("espiritu_oso", "Gran Espíritu del Oso", None), ("h_oso", "Forma de oso", None),
                                                     ("h_gato", "Forma felina · nivel 20", "gana la forma felina")], y=.64, tam=320, dur=6.0),
    # =========================================================== 15 cazador
    rel("Número quince. Si eres cazador", "h_domesticar", "Domesticar bestia", "y ponle nombre"),
    mg(M.nombre("NOMBRE DE TU MASCOTA", [("Lobo", "", False, "así no"), ("Galleta", "", True, "60 niveles contigo")]),
       ("Ponle el nombre de tu perro", -.3), ("Que se lo gane|fin", .3), ["Ponle el nombre", "Esa bestia te va a acompañar"], "mascota", y=.56),
    # =========================================================== 14 Defias
    mg(M.cadena("LA HERMANDAD DEFIAS", [(F("defias"), "Ladrones", "de pañuelo rojo", False), (F("ventormenta"), "Albañiles", "de Ventormenta", False),
                                        (F("vancleef"), "Edwin VanCleef", "Minas de la Muerte", True)], ("¿QUIÉN ERA EL LADRÓN?", 3)),
       ("En los Páramos de Poniente, los granjeros", -.2), ("los nobles que no les pagaron|fin", .3),
       ["eran los albañiles", "su líder, Edwin VanCleef", "quién era el verdadero ladrón"], "cadena Defias", y=.56),
    mapa("poniente", [P(56, 47, "Colina del Centinela", "la cadena empieza"), P(42, 72, "Arroyoplata", "Minas de la Muerte", "vancleef")],
         ("La historia te lleva por toda la zona", -.2), ("un barco pirata escondido bajo tierra|fin", .3), ["hasta el corazón"], "PÁRAMOS DE PONIENTE", "la Hermandad Defias"),
    # =========================================================== 13 Bosque del Ocaso
    mapa("ocaso", [P(75, 45, "Villa Oscura"), P(20, 50, "Colina del Cuervo", "cementerio", "colina_cuervo")], ("Un pueblo llamado Villa Oscura", -.2),
         ("Siempre es de noche|fin", .3), ["un cementerio lleno de neblina"], "BOSQUE DEL OCASO", "siempre es de noche"),
    sil("la de Stalvan Mantoniebla", "stalvan", "Stalvan Mantoniebla", "La leyenda de Stalvan", dur=5.2, lado="der"),
    pant("colina_cuervo", ("Y hay un no-muerto de élite, Mor'Ladim", -.2), ("Para esa, mejor ve en grupo de tres|fin", .2)),   # su imagen de la wiki no es la del juego
    # =========================================================== 12 raros
    mg(M.duplica("ENEMIGO NORMAL CONTRA RARO", "inv_misc_head_dragon_01", ("Normal", "siempre"), ("Plateado", "a veces"),
                 "RARO", "normal", "ATACA CON CUIDADO"),
       ("En cada zona hay enemigos especiales", -.2), ("a veces sueltan algo bueno|fin", .3), ["con un dragón plateado", "Aparecen pocas veces", "a veces sueltan"], "raro", y=.56),
    # =========================================================== 11 explorar
    mapa("azeroth_eses", [P(48, 56, "Dun Morogh", "picos donde nadie debería subir"), P(62, 30, "ruinas"), P(30, 75, "islas")],
         ("World of Warcraft tiene rincones", -.2), ("Lo que encuentres, lo encontraste tú|fin", .3), ["ruinas, cuevas, islas", "Y en Forever hay zonas"],
         "SIN MISIONES", "elige una montaña y ve"),
    # =========================================================== gracias2
    com("Alexander escribió que no se pierde", "UgyvBJ9JPFjgLoNWZHZ4AaABAg", dur=5.6, x=.27, y=.25, tam=620),
    com("Y el sargento Sevilla", "Ugwt3ef0C43WJWZhAjp4AaABAg", dur=5.4, x=.73, y=.64, tam=620),
    # =========================================================== 10 cruzar el mundo
    mapa("azeroth_eses", [P(71, 45, "Orgrimmar", "zepelín"), P(48, 83, "Grom'gol", "Vega de Tuercespina"), P(48, 70, "Bosque del Ocaso", "todo te mata"),
                          P(44, 66, "Bosque de Elwynn", "llegaste", "hogger")],
         ("Vas a tener que subir al zepelín", -.3), ("llegar se siente como una hazaña|fin", .3),
         ["cruzar zonas donde todo te mata", "esconderte, morir", "Es una tontería"], "DE DUROTAR A ELWYNN", "con un personaje de nivel bajo", zmax=1.4),
    # =========================================================== 09 morir bien
    rel("Número nueve. Aprende a morir bien", "angel", "Ángel de la resurrección", "debilidad y reparaciones"),
    rel("Y si tu clase puede resucitar", "h_resurreccion", "Resurrección", "hazlo por otros", x=.24),
    # =========================================================== 08 naufragio
    mapa("poniente", [P(30, 85, "naufragio", "Alianza · nivel 14")], ("Hacia el nivel catorce, en un barco hundido", -.2),
         ("Hacia el nivel catorce, en un barco hundido", 4.2), [], "PÁRAMOS DE PONIENTE", "la búsqueda del tesoro"),
    mapa("baldios", [P(63, 46, "naufragio", "Horda · nivel 14")], ("o de Los Baldíos si eres Horda", -.2), ("pistas que te llevan por varias zonas", .2),
         [], "LOS BALDÍOS", "la búsqueda del tesoro"),
    mapa("loch_modan", [P(47, 15, "la presa", "una pista en la cornisa")], ("hasta la presa de Loch Modan", -.6), ("hasta la presa de Loch Modan|fin", .2),
         [], "LOCH MODAN", "la pista de la presa"),
    mg(M.experiencia("BOLSA DE DORMIR ACOGEDORA", [("inv_misc_bag_10", "+1 % XP"), ("spell_holy_resurrection", "No se pierde"),
                                            ("spell_nature_sleep", "Descanso")], ("HASTA +3 %", 3)),
       ("Al final te espera la Bolsa de dormir", -.2), ("cuenta como zona de descanso|fin", .5), ["no se pierde al morir", "y cuenta como zona"], "bolsa de dormir", y=.56),
    # =========================================================== 07 libros
    rel("Número siete. Ve a la Feria de la Luna Negra", "o_boleto", "Feria de la Luna Negra", "una semana y se va", x=.76),
    mapa("azeroth_eses", [P(44, 66, "Bosque de Elwynn", "la primera · 9 al 15 nov"), P(36, 60, "Mulgore", "7 de diciembre")],
         ("La primera de Forever se instaló", -.2), ("dos días antes de que abran las bandas", -.7), ["Y la próxima llega"],
         "FERIA DE LA LUNA NEGRA", "va cambiando de lugar", zmax=1.3),
    pv("La primera de Forever se instaló", "silas", "Silas Luna Negra · el dueño de la feria", dur=4.4, x=.80, y=.36, tam=360),
    mg(M.calendario("LA FERIA DE LA LUNA NEGRA", 7, 1, 7, [(0, 0, "Llega a Mulgore", AMAR), (2, 2, "Abren las bandas", ROJO)], hoy=None),
       ("dos días antes de que abran las bandas", -.5), ("Ahí está Sayge", -.3),
       ["dos días antes", "de que abran las bandas"], "feria diciembre", y=.56),
    # =========================================================== 06 guerra
    mapa("trabalomas", [P(62, 20, "Molino Tarren", "Horda"), P(51, 55, "Costasur", "Alianza")], ("Como el Molino Tarren y Costasur", -.4),
         ("dos pueblos frente a frente|fin", .4), ["y Costasur"], "LADERAS DE TRABALOMAS", "la guerra de siempre"),
    mapa("tuercespina", [P(35.6, 10.6, "Expedición de Nesingwary", "emboscadas")], ("O la Vega de Tuercespina", -.2), ("tan viejas como el juego|fin", .3),
         [], "VEGA DE TUERCESPINA", "emboscadas"),
    # =========================================================== burla2 (Alberto)
    com("volvamos con Alberto", "Ugzmf-vgaHwmGz-F4_J4AaABAg", dur=5.6, x=.32, y=.30),
    mapa("crestagrana", [P(29, 46, "Villa del Lago", "Alberto, quédate aquí")], ("Así que quédate ahí", -.2), ("no se va a ir a ningún lado|fin", .3),
         ["Pesca en el lago", "cruza el puente"], "MONTES CRESTAGRANA", "Villa del Lago"),
    # =========================================================== 05 Baldíos
    mg(M.chat([("[1. General] Grokk: ¿dónde está la esposa de Mankrik?", (255, 192, 160)), ("[1. General] Zul: ¿dónde está la esposa de Mankrik?", (255, 192, 160)),
               ("[1. General] Thrak: con Chuck Norris", (255, 192, 160)), ("[1. General] Moa: ¿dónde está la esposa de Mankrik?", (255, 192, 160))],
              "¿Dónde está la esposa de Mankrik?"),
       ("Ahí nació la pregunta más famosa", -.2), ("todavía se cuentan|fin", .3),
       ["La misión se llama Perdida", "Durante años, la gente preguntaba", "Y alrededor de esa pregunta"], "chat de los Baldíos", x=.30, y=.60),
    sil("La misión se llama Perdida en la batalla", "mankrik", "Mankrik", "el Cruce · Los Baldíos", dur=5.0, lado="der"),
    mapa("baldios", [P(52, 30, "El Cruce", "Mankrik", "mankrik"), P(49, 61, "la esposa de Mankrik")], ("En Forever, Los Baldíos vuelven", -.2),
         ("Es una tradición|fin", .3), ["Así que pregunta"], "LOS BALDÍOS", "¿dónde está?"),
    # =========================================================== 04 capital
    carr([("ventormenta", "Ventormenta"), ("forjaz", "Forjaz"), ("cima_trueno", "Cima del Trueno"), ("darnassus", "Darnassus")],
         ("Ventormenta, Forjaz, Orgrimmar", -.2), ("Cada una se siente completamente distinta|fin", .3), ["Forjaz", "Cima del Trueno", "Darnassus"], titulo="CADA CAPITAL, UN MUNDO"),
    # =========================================================== 03 ayudar
    mg(M.contadores("LO QUE TE CUESTA AYUDAR", [("inv_misc_coin_03", "Unas monedas de plata", 5, 0, 1), ("inv_misc_bag_10", "Una bolsa que te sobra", 1, 1, 2)],
                    ("PARA ÉL: MEDIO DÍA DE JUEGO", 2)),
       ("Ve y ayúdalo", -.2), ("para él es medio día de juego|fin", .4), ["Dale unas monedas", "o una bolsa", "A ti no te cuesta nada"], "ayudar", y=.56),
    # =========================================================== 02 mirar
    mg(M.tiempos("UN DÍA EN AZEROTH", [("Amanecer · Elwynn", 30, AMAR), ("Tormenta · Páramos", 30, (120, 140, 200)), ("Nieve · Dun Morogh", 40, BLANCO)],
                 "Detente, y mira"),
       ("Y el mundo tiene día y noche", -.2), ("la nieve cayendo en Dun Morogh|fin", .4), ["la tormenta en los Páramos", "la nieve cayendo"], "día y noche", y=.56),
    # =========================================================== 01 calma
    mg(M.calendario("LAS BANDAS NO SE VAN", 9, 3, 10, [(0, 0, "9 dic · abren", AMAR), (1, 9, "y siguen ahí", VERDE)], hoy=None),
       ("Las bandas abren el nueve de diciembre", -.2), ("no se va a mover de su sitio|fin", .3), ["y van a seguir ahí en enero"], "bandas", y=.56),
    mg(M.consola("TU DIARIO DE FOREVER", [("Hoy pesqué en Villa del Lago", "RECUERDO", VERDE, 0), ("Hoy mi grupo mató a Hogger", "RECUERDO", VERDE, 1),
                                          ("Hoy me perdí en el Bosque del Ocaso", "RECUERDO", VERDE, 2)], sellos=[("NIVELES: DA IGUAL", AMAR, 3)]),
       ("Así que no midas tus sesiones en niveles", -.2), ("Hoy me perdí en el Bosque del Ocaso|fin", 1.2),
       ["Hoy pesqué", "Hoy mi grupo", "Hoy me perdí", "Hoy me perdí en el Bosque del Ocaso|fin"], "diario", y=.56),
    # =========================================================== cierre
    dict(tipo="mg", fn=PE.banda(F("hogger"), "30 COSAS · CERO PRISA", "vívelo, no lo corras", alto=380, tema="wow"),
         en=("Y esas son las treinta cosas", -.2), dur=5.0, x=.5, y=.80, sale=.3, nombre="banda cierre", ver=1.0),
]
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]

# --- más pegatinas (chequeo 12-nov: densidad 0,8/min vs 1,9 del canal) ---
FX += [
    pv("Te sientas en un muelle, lanzas la caña", "h_pesca", "Pesca", dur=3.6, x=.80, y=.62, tam=300),
    cam("Cocina pescado y véndelo", "o_pez", "Pescado", dur=3.4, x=.89, y=.20, tam=240),
    cam("Fabrica bolsas con sastrería", "o_bolsa", "Bolsa de lino", dur=3.4, x=.11, y=.20, tam=240),
    rel("En Forjaz, todo el mundo está frente al banco", "forjaz", "Forjaz", "todos frente al banco", x=.76, dur=3.8),
    pv("En Cima del Trueno hay ascensores", "cima_trueno", "Cima del Trueno · los ascensores", dur=3.6, x=.24, y=.60, tam=440),
    pv("Cuando por fin cae Hogger", "hogger", "Hogger · derrotado", dur=4.0, x=.80, y=.55, tam=420),
    cam("hasta una pecera", "o_pez", "Pecera · Pesca", dur=3.2, x=.89, y=.20, tam=240),
    pv("Pesca en el lago, haz amigos en la posada", "h_pesca", "Pesca en Villa del Lago", dur=3.6, x=.22, y=.62, tam=320),
    pv("a juntar boletos", "o_boleto", "Boletos de la feria", dur=3.4, x=.20, y=.60, tam=300),
]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="NIVEL 60 · PARA SIEMPRE", en="se queda en sesenta para siempre", dur=2.6, tam=120, color="amarillo", y=.2),
    dict(texto="FRICCIÓN", en="La palabra es fricción", dur=2.4, tam=170, color="amarillo", y=.2),
    dict(texto="×2", en="te da el doble de experiencia", dur=2.2, tam=180, color="amarillo", y=.2),
    dict(texto="GRATIS", en="Gratis de verdad", dur=2.2, tam=170, color="amarillo", y=.2),
    dict(texto="VÍVELO", en="Así que no lo corras, mejor vívelo", dur=2.6, tam=170, color="amarillo", y=.2),
]
SFX = {}
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.28) for e in ("Número treinta.", "Número veinticinco", "Número veinte.", "Número quince",
                                                                "Número diez", "Número cinco")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Hoy te traigo treinta cosas", "Número uno. Tómatelo con calma")]
PISTAS += [dict(sfx="oye_willem", en=("Escucha a tu primer PNJ|fin", .15), vol=1.0, voz=True)]   # add-on Voces (OBS 8-nov, Willem, 4,9 s)

APOYOS = [
    dict(en="Y en Forever el comercio tiene su propio sistema", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Favor de comerciante", calidad="amarillo",
         icono="inv_misc_coin_03", lineas=["Cajas de materiales", "al campamento de tu facción", dict(t="+600 recetas nuevas", c=V)])),
    dict(en="Ojo, que el ajuste es de toda la cuenta", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Idioma preferido en línea", calidad="amarillo",
         icono="inv_letter_15", lineas=["De toda la cuenta", dict(t="Enfriamiento: 24 horas", c=RJ)])),
]

APOYOS += [
    dict(en="Hasta hay un desafío de legado", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Desafío de legado", calidad="morado",
         icono="inv_misc_map_01", lineas=["Explora todo el mapa del mundo", "con el mismo personaje"])),
    dict(en="En Forever, Hogger no se adapta", dur=5.6, x=.72, size=.50, tarjeta=dict(titulo="Hogger", calidad="amarillo",
         icono="ability_warrior_challange", lineas=["Élite · nivel 11", dict(t="No se adapta a tu nivel", c=RJ), "Objetos de misión: por turnos"])),
    dict(en="Ahí está Sayge, un adivino", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Sayge", calidad="morado",
         icono="inv_misc_orb_02", lineas=["Te hace preguntas sobre ti", dict(t="Beneficio de 2 horas", c=V), "Sin respuesta correcta"])),
    dict(en="Se desbloquea muy al principio", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Hoguera básica", calidad="verde",
         icono="spell_fire_fire", lineas=["Misión hacia el nivel 5", "3 objetos · uno por jugador", dict(t="Siéntate ≥ 1 minuto", c=V)])),
]
