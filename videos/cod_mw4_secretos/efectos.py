# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 25 SECRETOS que Modern Warfare 4 te escondió» (SECUENCIA YT, Expediente 141, 2-nov-2026).
Kit de interfaz de Call of Duty: Modern Warfare por código (nucleo/mg_cod.py), anclado a palabras de la voz.
REGLA DE ORO (tes_secretos_40): las capas SUMAN; lo que dice la voz se ve; ningún clip ni imagen de otro juego; MG desde el gancho;
pegatinas variadas (peg_estilos con tema «cod»: silueta, reliquia, banda, camafeo, legajo, abanico); `chequeo` antes de `video`.
- Puestos: entrada de misión `C.puesto` (EXPEDIENTE NN/25), abajo.
- Fichas tácticas (`C.ficha`) arriba a la derecha; pegatinas reales (pegatinas/, `bajar_pegatinas.py`) abajo a la izquierda.
- MG propios de este guion: sello CLASIFICADO, misión fallida (retrato, Graves, Ghost, Ri), logro «Jamás te olvidaremos»,
  radio (War Pig / Gold Eagle / Outlaw 2-5), código 8410 y 214, línea «¿Estás roto?», espejo «Dos sagas, un compositor»,
  balanza «Lo que el juego castiga».
- SFX del JUEGO (regla 29-oct-2026): banco nucleo/datos/sfx_juego/cod/ copiado a sfx/.
  python fab.py cod_mw4_secretos fx --seco   tiempos      python fab.py cod_mw4_secretos fx hoja   previews/fx_NN.jpg
"""
import os

import mg_cod as C
import mg_wow as W
import peg_estilos as PE

TEMA = "cod"
CAMARA = {}
FUNDIDO = {}

_FX, _FY = .75, .30            # fichas: arriba a la derecha
_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_MAPA = "gaming"


def P(slug):
    for e in (".png", ".jpg", ".webp"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    return os.path.join(_PEG, slug + ".png")


def ficha(en, titulo, texto, tipo=None, dur=5.0, x=_FX, y=_FY, ancho=880):
    return dict(tipo="mg", fn=C.ficha(titulo, texto, tipo, ancho=ancho), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + titulo, ver=1.2)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, giro=-5.0):
    """Pegatina con la imagen REAL de lo que nombra la voz: abajo a la izquierda."""
    return dict(tipo="mg", fn=C.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.5, x=.27, tam=640):
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.5, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.78, y=.52, ancho=500, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.64, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="pegatina " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=W.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5,
                nombre="pantalla " + slug, ver=2.0)


def puesto(en, n, titulo, sub, dur=4.5):
    return dict(tipo="mg", fn=C.puesto(n, titulo, sub), en=en, dur=dur, x=.5, y=.80, sale=.4, nombre=f"puesto {n}", ver=1.4)


def mg(fn, de, a, marcas, nombre, x=.5, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


FX = [
    # ---------------- gancho (MG desde el primer segundo)
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Clasificación", 2.6, "sello", x=.33, y=.42),
    leg("c_mw4", "EXPEDIENTE 141", ["Asunto: Modern Warfare 4", "Infinity Ward · 2026", "Clasificación: secreto"],
        de="Asunto", a=("Le disparas", -.2), x=.78, y=.50, ancho=470),
    mg_en(C.fallida("Misión fallida", "Deshonraste a tu país dañando un retrato del Líder Supremo"), "te ejecuta", 1.45, "fallida retrato"),
    peg("Te asomas a una tele", "tele_gta", "Nueva York · misión 2", dur=4.0, x=.74, y=.50, tam=620, giro=4.0),
    peg("Infinity Ward escondió", "infinity_ward_placa", "El estudio", dur=3.6, x=.24, y=.70, tam=520),
    aba([("c_cod4", "2007"), ("c_mw2019", "2019"), ("c_mw4", "2026")], de="el último capítulo", a=("Hoy abrimos", -.2),
        marcas=["último", "saga", "salió"], nombre="saga", x=.70, y=.60, tam=300),
    ficha("hace apenas unas semanas", "Modern Warfare 4", "Infinity Ward · salió el *23 de octubre de 2026* · campaña en Corea.",
          "INTEL / LANZAMIENTO", dur=3.4, x=.27, y=.28, ancho=760),
    ficha("Todos comprobados", "25 secretos", "Todos *comprobados*. Las fuentes, en la descripción.", "EXPEDIENTE 141 / ÍNDICE",
          dur=4.6),
    mg_en(C.radio("Expediente 01", "No se ve. Se oye.", "CANAL CIFRADO"), "Se oye", 3.2, "radio se oye", y=.30),
    puesto("Número veinticinco", 25, "La tele que nadie mira", "MISIÓN 02 / NUEVA YORK"),
    sil("persigues a Makarov", "makarov", "Makarov", "El terrorista que persigues", lado="der", dur=4.8),
    ficha("La programación es inventada", "Guía de TV",
          "Princess Starfish 2: el regreso al trono · *Operation Saber 3* · Excessive Cakes.", "INTEL / MISIÓN 02", dur=6.0,
          x=.30, y=.74, ancho=820),
]

# ---------------- puestos 24 → 4
FX += [
    puesto("En el veinticuatro, pulsa E", 24, "Pulsa E para despedirte", "MISIÓN / ATRAPADOS / NORTE NEVADO"),
    peg("el famoso Press F", "c_aw", "Advanced Warfare · 2014", dur=4.4, x=.80, y=.55, tam=420, giro=5),
    puesto("Número veintitrés", 23, "El pato armado", "DMZ / HAJAN RIVER HEIGHTS"),
    ficha("hay un patito de goma", "Patito de goma", "Un pato de goma... con *un cuchillo*. Nadie lo explica.", "INTEL / DMZ", dur=5.0),
    puesto("En el veintidós", 22, "La física que nunca tuvimos", "CAMPAÑA / MULTIJUGADOR"),
    ficha("Dispara a través de una granada", "Detalles nuevos", "Túneles de bala en el *humo* · barro que salpica el arma · "
          "sangre en el arma si te disparan.", "INTEL / FÍSICA", dur=7.0),
    puesto("Número veintiuno", 21, "Armas que se acuerdan de 2009", "MISIÓN / BOMBAY"),
    aba([("c_mw2_2009", "2009"), ("c_mw4", "2026")], de="recarga casi igual", a=("Si eso no te dice", -.2),
        marcas=["recarga", "misión final"], nombre="mw2 vs mw4", x=.72, y=.58, tam=320),
    ficha("el Patriot XMR", "Patriot XMR", "La versión del ACR en este juego: recarga casi igual que en *MW2 (2009)*.", "ARSENAL / BOMBAY",
          dur=4.4, x=.28, y=.28, ancho=760),
    puesto("En el veinte", 20, "Tu soldado hace de Neo", "INSPECCIÓN DE ARMA / MANOS VACÍAS"),
    peg("Es la tradición de Modern Warfare dos", "c_mw2r", "MW2 Remastered", dur=4.4, x=.80, y=.55, tam=400, giro=4),
    puesto("Número diecinueve", 19, "Un periódico con la caja mágica", "MISIÓN / CUMPLIENDO ÓRDENES"),
    rel("En la foto sale la caja mágica", "mystery_box", "Caja mágica", "Zombies · Infinite Warfare 2016", dur=5.0, x=.74, y=.50),
    puesto("En el dieciocho", 18, "No te tumbes", "MISIÓN FINAL"),
    sil("Price persigue al Arquero", "price", "Capitán Price", "Herido en el estómago", lado="izq", dur=5.0),
    ficha("Lo probaron en dificultad Realismo", "Dificultad Realismo", "Tirarte al suelo *daña a Price*. Duele, pero no mata.",
          "PRUEBA / FINAL", dur=5.0),
    puesto("Número diecisiete", 17, "El contrabando de Occidente", "MISIÓN / CUMPLIENDO ÓRDENES"),
    mg(C.codigo("214", "Caja de herramientas", "Nota para un logro"), de="código dos, uno, cuatro", a=("guarda otro más", 2.5),
       marcas=["dos", "uno", "cuatro"], nombre="codigo 214", x=.72, y=.50),
    puesto("En el dieciséis", 16, "Los trucos de los desarrolladores", "MISIÓN 1 / MISIÓN DEL TREN"),
    ficha("te teletransportan", "Teletransporte", "Tras el apagón te mueven a una *copia destruida* del barrio.",
          "INTEL / DESARROLLO", dur=5.0),
    peg("como los morteros invisibles", "c_cod4", "Morteros invisibles · CoD 4", dur=4.0, x=.80, y=.55, tam=380, giro=4),
    puesto("Número quince", 15, "Dos de relleno que no lo son", "MISIÓN / BOMBAY"),
    aba([("wallcroft", "Wallcroft"), ("griffin", "Griffin")], de="Wallcroft y Griffin", a=("Personajes de la saga original", -.2),
        marcas=["Wallcroft", "Griffin"], nombre="sas", x=.30, y=.62, tam=330),
    peg("en Modern Warfare 3, de dos mil once", "c_mw3_2011", "MW3 · 2011", dur=4.0, x=.80, y=.55, tam=380, giro=5),
    puesto("En el catorce", 14, "No puedes perdonar a Graves", "MISIÓN / HIRED GUN"),
    sil("Phillip Graves", "graves", "Phillip Graves", "Shadow Company", lado="der", dur=5.0),
    mg_en(C.fallida("Misión fallida", "Graves aprovechó tu duda"), "y te mata", 2.2, "fallida graves"),
    puesto("Número trece", 13, "La estatua que puedes escalar", "NORTE NEVADO"),
    mg_en(C.radio("Leyenda local", "Derrotó él solo a un batallón japonés.", "MARCA POR RADIO"), "alguien te cuenta su leyenda", 4.5,
          "radio estatua", y=.28),
    puesto("En el doce", 12, "El fideo de Spider-Man", "MISIÓN 1 / HAJIN, COREA DEL SUR"),
    ficha("Si lo atrapas", "Cabo Dunn", "Atrapa el bol: *«se te activó el sentido arácnido»*.", "DIÁLOGO / MISIÓN 1", dur=4.0),
    ficha("Si lo dejas caer", "Cabo Dunn", "Si lo tiras, te regaña. Si tardas en recogerlo, *te lo reclama otra vez*.",
          "DIÁLOGO / MISIÓN 1", dur=5.0),
    puesto("Número once", 11, "Soap no sale en el juego", "GRAFITI / LETRERO DIGITAL"),
    ban("Soap MacTavish, el de siempre", "soap", "Soap MacTavish", "No aparece en la campaña", foco=(.5, .32, 1.8), dur=4.5, y=.62),
    puesto("En el diez", 10, "La impresora 3D de Cachette", "MULTIJUGADOR / CACHETTE"),
    ficha("si en vez de usarla la golpeas", "Impresora 3D", "Golpéala: se rompe la pantalla y sale un arma con *5 accesorios*. "
          "Cambia en cada partida.", "INTEL / MULTIJUGADOR", dur=6.0),
    puesto("Número nueve", 9, "La radio de 2007", "CONTRAATAQUE / COSTA DE HAJIN"),
    mg_en(C.radio("War Pig", "El tanque atascado en el pantano de CoD 4"), "War Pig, el tanque", 3.6, "radio war pig", y=.28),
    mg_en(C.radio("Gold Eagle", "El indicativo del general Shepherd"), "Y Gold Eagle", 3.4, "radio gold eagle", y=.28),
    cam("el indicativo del general Shepherd", "shepherd", "Gral. Shepherd", dur=3.4, x=.16, y=.66, foco=(.5, .4, 1.6)),
    mg_en(C.radio("Outlaw 2-5", "El helicóptero de Jackson en CoD 4"), "indicativo Outlaw dos cinco", 4.0, "radio outlaw", y=.28),
    puesto("En el ocho", 8, "Ghost muere si eres curioso", "MISIÓN / HUIDA"),
    sil("golpean a Ghost", "ghost", "Ghost", "Prisionero", lado="izq", dur=4.6),
    mg_en(C.fallida("Misión fallida", "Ghost ha muerto"), "la misión fracasa al instante", 2.4, "fallida ghost"),
    puesto("Número siete", 7, "La comandante Ri no perdona", "MISIÓN / CUMPLIENDO ÓRDENES"),
    mg_en(C.fallida("Misión fallida", "Traición: te negaste a cumplir la orden"), "Ri te ejecuta por traidor", 2.6, "fallida ri"),
    puesto("En el seis", 6, "Pixel art en París", "MISIÓN / TRÁFICO"),
    aba([("price", "Price"), ("ghost", "Ghost"), ("riley_perro", "Riley")], de="Price con su sombrero", a=("Es un homenaje", -.2),
        marcas=["Price", "Ghost", "pastor alemán"], nombre="pixel art", x=.70, y=.60, tam=300),
    peg("el perro de Call of Duty Ghosts", "c_ghosts", "Ghosts · 2013", dur=3.6, x=.18, y=.62, tam=360),
    cam("Es un homenaje a Invader", "invader", "Invader", dur=4.0, x=.16, y=.66, foco=(.5, .35, 1.4)),
    puesto("Número cinco", 5, "Los perros de Prípiat", "MISIÓN / HUIDA"),
    leg("macmillan", "ALL GHILLIED UP", ["CoD 4 · 2007", "Price y MacMillan", "Prípiat · 1996"], de="Es la misión All Ghillied Up",
        a=("El reboot es otra", -.2), x=.76, y=.52),
    puesto("En el cuatro, GTA seis", 4, "GTA 6 salió primero", "MISIÓN 2 / NUEVA YORK"),
    ficha("En una consola falsa", "Consola falsa", "De Activision, con guiños a *Pitfall*. Para verla, deja que Makarov se aleje.",
          "INTEL / MISIÓN 02", dur=5.0),
]

# ---------------- puesto 3, spoilers, 2, 1 y cierre
FX += [
    puesto("Número tres. Dispárale", 3, "Dispárale al retrato del Líder", "MISIÓN / CUMPLIENDO ÓRDENES"),
    mg(C.balanza("Lo que el juego castiga", [("Tiro de advertencia a civiles", True, "nada"),
                                             ("Disparar al retrato del Líder", False, "ejecución"),
                                             ("Mentir por la familia", False, "otra soga")]),
       de="Puedes disparar tiros de advertencia", a=("Y la pantalla de muerte", -.2),
       marcas=["no pasa nada", "retrato del Líder Supremo colgado", "te elimina"], nombre="balanza", x=.5, y=.50),
    # «la pantalla de muerte lo explica»: el clip ya enseña la pantalla REAL (2-nov: el MG la tapaba); solo suena cod_fallida
    mg_en(C.sello("SPOILERS", "FINAL DE LA CAMPAÑA"), "Alto ahí", 3.0, "sello spoilers", x=.5, y=.45),
    puesto("Número dos. La caída", 2, "La caída de Gaz", "MISIÓN / BOMBAY"),
    sil("Gaz, ya capitán", "gaz", "Gaz", "Capitán de la 141", lado="der", dur=5.0),
    mg(C.linea("¿Estás roto?", [(2019, "MW", "Price a Gaz"), (2022, "MW2", "Se repite"), (2023, "MW3", "Otra vez"),
                                (2026, "MW4", "Gaz a Price")]),
       de="Price conoció a Gaz", a=("El roto, ahora", -.2), marcas=["dos mil diecinueve", "las dos entregas", "siguientes", "Gaz quien"],
       nombre="linea estas roto", y=.50),
    ban("el villano de Mads Mikkelsen", "mads", "El Arquero", "Mads Mikkelsen", foco=(.5, .3, 1.8), dur=4.4, y=.62),
    cam("Igual que Zakhaev", "zakhaev", "Zakhaev · 2007", dur=4.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg(C.codigo("8410", "Caja fuerte / prisión", "Chapas de Gaz"), de="da el código", a=("Dentro están las chapas", 1.0),
       marcas=["ocho", "cuatro", "uno", "cero"], nombre="codigo 8410", x=.72, y=.50),
    mg_en(C.logro("Jamás te olvidaremos", "Recupera las chapas de Gaz"), "Y el logro se llama", 4.5, "logro gaz", y=.84),
    puesto("Y el número uno#2", 1, "El secreto que no se ve", "POST-CRÉDITOS"),
    sil("Kate Laswell borra", "laswell", "Kate Laswell", "Borra la Task Force 141", lado="izq", dur=5.0),
    mg(C.espejo("Dos sagas, un compositor", (2007, "CoD 4", ["Final del puente", "Price mata a Zakhaev"]),
                (2026, "MW4", ["Post-créditos", "Laswell borra la 141"]), "Stephen Barton"),
       de="La música de CoD 4 la escribió", a=("Y el último detalle", -.2), marcas=["CoD 4", "Modern Warfare 4", "La misma persona"],
       nombre="espejo compositor", y=.50),
    cam("junto a Harry Gregson-Williams", "gregson_williams", "H. Gregson-Williams", dur=3.6, x=.16, y=.70, foco=(.5, .3, 1.5)),
    mg_en(C.radio("Watcher 6", "Bienvenida al programa Watcher.", "INDICATIVO / 2019"), "Laswell usaba el indicativo", 5.0,
          "radio watcher", y=.28),
    mg_en(C.sello("EXPEDIENTE CERRADO", "POR AHORA"), "Expediente cerrado", 3.0, "sello cierre", x=.5, y=.45),
    ficha("Si quieres el siguiente", "Expediente 141", "Los archivos de Call of Duty que nadie te contó, *en español*. "
          "Suscríbete para el siguiente.", "CANAL / RECLUTAMIENTO", dur=6.0),
    ficha("Y dime en los comentarios", "¿Cuál no conocías?", "Déjalo en los *comentarios*. Yo apuesto por el pato.",
          "INFORME / COMENTARIOS", dur=5.0),
]
ROTULOS = [
    dict(texto="NO SE VE", en="el número uno no se ve", tam=150, color="amarillo", y=.22),
    dict(texto="PASTELES EXCESIVOS", en="Pasteles excesivos", tam=120, color="amarillo", y=.20),
    dict(texto="PULSA E", en="pulsar E para despedirte", tam=150, color="amarillo", y=.22),
    dict(texto="CASTIGOS INVISIBLES", en="Tiene castigos invisibles", tam=120, color="amarillo", y=.22),
    dict(texto="19 AÑOS SIN ASCENSO", en="Y siguen sin ascenso", tam=120, color="amarillo", y=.22),
    dict(texto="KR-SOAP · 141", en="ciento cuarenta y uno. El número", tam=130, color="amarillo", y=.22),
    dict(texto="MUÉVETE, SOLDADO", en="Muévete, soldado", tam=130, color="amarillo", y=.22),
    dict(texto="MANTÉN LA LÍNEA", en="mantén la línea", tam=130, color="amarillo", y=.22),
]
SFX = {}
# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/cod/ → sfx/<n>.mp3), solo en momentos clave
PISTAS = [
    dict(sfx="cod_sello", en="Clasificación", vol=.30),
    dict(sfx="cod_fallida", en="te ejecuta", vol=.30),
    dict(sfx="cod_radio", en="Se oye", vol=.26),
    dict(sfx="cod_puesto", en="Número veinticinco", vol=.24),
    dict(sfx="cod_puesto", en="En el veinte", vol=.22),
    dict(sfx="cod_sello", en="Número quince", vol=.24),
    dict(sfx="cod_puesto", en="En el diez", vol=.22),
    dict(sfx="cod_sello", en="Número cinco", vol=.24),
    dict(sfx="cod_fallida", en="y te mata", vol=.30),
    dict(sfx="cod_fallida", en="la misión fracasa al instante", vol=.30),
    dict(sfx="cod_fallida", en="Ri te ejecuta por traidor", vol=.30),
    dict(sfx="cod_fallida", en="la pantalla de muerte lo explica", vol=.30),
    dict(sfx="cod_radio", en="War Pig, el tanque", vol=.24),
    dict(sfx="cod_radio", en="Laswell usaba el indicativo", vol=.24),
    dict(sfx="cod_sello", en="Alto ahí", vol=.28),
    dict(sfx="cod_logro", en="Y el logro se llama", vol=.30),
    dict(sfx="cod_puesto", en="Y el número uno#2", vol=.26),
    dict(sfx="cod_sello", en="Expediente cerrado", vol=.28),
    # ---- SONIDOS NOMBRADOS (regla 31-oct-2026): la voz los anuncia y se oyen en el hueco, a nivel de voz (fx_voz.wav)
    dict(sfx="s_spidey", en="se te activó el sentido arácnido|fin", vol=1.0, voz=True),
    dict(sfx="s_warpig", en="Escucha la radio|fin", vol=1.0, voz=True),
    dict(sfx="s_bravo6", en="Y dice esto|fin", vol=1.0, voz=True),
    dict(sfx="s_broken", en="es Gaz quien se la grita a Price|fin", vol=1.0, voz=True),
    dict(sfx="s_postcreditos", en="Y de fondo suena esto|fin", vol=1.0, voz=True),
    dict(sfx="s_cod4", en="Así sonaba en dos mil siete|fin", vol=1.0, voz=True),
    dict(sfx="s_watcher", en="bienvenida al programa Watcher|fin", vol=1.0, voz=True),
]
