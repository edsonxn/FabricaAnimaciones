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


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    """Acercamiento lento de cámara sobre el clip (3-nov-2026: más animación en los tramos sin apoyo)."""
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def vid(n, de, a, desde=0.0, recorte=0.0):
    """Corte rápido con OTRO clip ya bajado del video (medios/scene-NNN.mp4) a cuadro entero, para que el gancho cambie de
    plano cada 1-3 s sin renumerar los beats (3-nov-2026). Van PRIMERO en FX: se dibujan debajo de MG y pegatinas."""
    return dict(tipo="video", ruta=os.path.join(_AQUI, "medios", f"scene-{n:03d}.mp4"), de=de, a=a, desde=desde,
                recorte=recorte, entra=.12, sale=.12, nombre=f"corte clip {n:03d}")


FX = [
    # ---------------- gancho (MG desde el primer segundo)
    # 3-nov-2026 (el usuario: «el gancho se siente vacío»): un elemento nuevo cada 2-3 s; cortes rápidos con clips del video
    zoom(0.0, ("Un pato", -.1), 1.14),
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Clasificación", 2.6, "sello", x=.33, y=.42),
    leg("c_mw4", "EXPEDIENTE 141", ["Asunto: Modern Warfare 4", "Infinity Ward · 2026", "Clasificación: secreto"],
        de="Asunto", a=("Un pato", -.15), x=.78, y=.50, ancho=470),
    rel("Un pato de goma", "pato_goma", "Pato de goma", "Armado con un cuchillo · DMZ", dur=2.4, x=.74, y=.50, tam=480),
    cam("Un bol de fideos", "dunn", "Cabo Dunn", dur=2.2, x=.16, y=.66, foco=(.5, .3, 1.6)),
    peg("el sentido arácnido", "spiderman", "Sentido arácnido", dur=1.5, x=.80, y=.58, tam=330, giro=6),
    mg_en(C.marcador("Impresora 3D", 25, "Cachette · multijugador"), "Y una impresora", 3.0, "marcador impresora", x=.40, y=.34),
    mg_en(C.marcador("Retrato del Líder", 8), "Le disparas", 1.5, "marcador retrato", x=.52, y=.26),
    cam("Líder Supremo", "lider", "El Líder Supremo", dur=2.4, x=.84, y=.64, foco=(.5, .3, 1.5)),
    peg("en Corea del Norte", "corea_norte_mapa", "Corea del Norte", dur=2.2, x=.17, y=.66, tam=300, giro=-4),
    # «te ejecuta»: el clip ya enseña la pantalla de muerte REAL en coreano; solo temblor + cod_fallida
    dict(tipo="temblor", en="te ejecuta", amp=26, dur=.5),
    zoom("Te asomas a una tele", ("Sí. Antes", 0), 1.22),
    cam("en Nueva York", "nueva_york", "Nueva York", dur=2.2, x=.16, y=.66, foco=(.5, .5, 1.2)),
    rel("jugando GTA seis", "gta6", "GTA VI", "Antes que tú", dur=3.0, x=.78, y=.50, tam=470),
    aba([("price", "Price"), ("ghost", "Ghost"), ("gaz", "Gaz"), ("soap", "Soap")], de="Price, Ghost", a=("todos esconden", -.1),
        marcas=["Price", "Ghost", "Gaz", "Soap"], nombre="cuatro", x=.68, y=.58, tam=280),
    mg_en(C.marcador("Chapas de Gaz", 6), "todos esconden algo", 2.0, "marcador chapas", x=.42, y=.30),
    peg("Infinity Ward lo metió", "infinity_ward_placa", "El estudio", dur=2.2, x=.24, y=.70, tam=480),
    aba([("c_cod4", "2007"), ("c_mw2019", "2019"), ("c_mw4", "2026")], de="el último capítulo", a=("Veinticinco secretos", -.2),
        marcas=["último", "saga", "salió"], nombre="saga", x=.70, y=.60, tam=300),
    ficha("salió el veintitrés", "Modern Warfare 4", "Infinity Ward · salió el *23 de octubre de 2026* · campaña en Corea.",
          "INTEL / LANZAMIENTO", dur=2.2, x=.27, y=.28, ancho=760),
    mg_en(C.contador(25, "SECRETOS", "Expediente 141"), "Veinticinco secretos", 1.5, "contador 25", y=.50),
    ficha("Todos comprobados", "25 secretos", "Todos *comprobados*. Las fuentes, en la descripción.", "EXPEDIENTE 141 / ÍNDICE",
          dur=3.4),
    mg_en(C.radio("Expediente 01", "No se ve. Se oye.", "CANAL CIFRADO"), "Se oye", 1.6, "radio se oye", y=.30),
    mg_en(C.objetivo("Quédate hasta el final", "El número uno: post-créditos"), "Así que quédate", 3.0, "objetivo final", x=.30, y=.18),
    puesto("Número veinticinco", 25, "La tele que nadie mira", "MISIÓN 02 / NUEVA YORK"),
    leg("m_nuevayork", "OUT IN THE COLD", ["Misión 02", "Nueva York", "Persecución de Makarov"], de="En la segunda misión",
        a=("Y en una pantalla", -.2), x=.25, y=.50, ancho=500),
    sil("persigues a Makarov", "makarov", "Makarov", "El terrorista que persigues", lado="der", dur=3.8),
    mg_en(C.marcador("Guía de TV", 10), "en una pantalla está", 2.8, "marcador guia", x=.5, y=.30),
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
    cam("Price persigue al Arquero", "price", "Capitán Price", dur=3.6, x=.16, y=.66, foco=(.5, .25, 1.8)),
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
    dict(texto="NO SE VE", en="el número uno no se ve", tam=150, color="amarillo", y=.22, dur=1.6),
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

# ======================================================================================================================
# 3-nov-2026 — RELLENO de los tramos vacíos (el usuario: «le faltan más animaciones y pegatinas, hay momentos que se sienten
# vacíos»): ningún tramo de > ~4 s con el clip solo. Estilos variados (silueta, reliquia, banda, camafeo, legajo, abanico) +
# MG nuevos del kit (objetivo, marcador, contador) + acercamientos de cámara.
FX += [
    # ---- 25
    ficha("una pizzería de parodia", "Joe's Pizza House", "Pizzería de *parodia* al final de la misión.", "INTEL / MISIÓN 02",
          dur=3.6, x=.27, y=.28, ancho=700),
    mg_en(C.contador(0.5, "S", "Lo que tarda en verse", desde=9.0, decimales=1), "ves medio segundo", 2.4, "contador medio segundo"),
    cam("Mientras persigues a un terrorista", "makarov", "Makarov", dur=2.6, x=.16, y=.66, foco=(.5, .3, 1.5)),
    # ---- 24
    leg("m_atrapados", "ATRAPADOS", ["Norte nevado", "Corea del Norte", "El refugio"], de="En la misión Atrapados",
        a=("Cuando vuelves", -.2), x=.77, y=.52, ancho=480),
    cam("el soldado Chow", "chow", "Soldado Chow", dur=3.4, x=.16, y=.66, foco=(.5, .32, 1.5)),
    mg_en(C.objetivo("Despídete del soldado Chow", "Pulsa E"), "Y el juego te deja", 3.6, "objetivo chow", x=.30, y=.18),
    zoom("Solo que esta vez nadie", ("Número veintitrés", -.1), 1.12),
    # ---- 23
    ban("En DMZ, dentro", "dmz", "DMZ", "Hajan River Heights", foco=(.5, .35, 1.5), dur=3.2, y=.64, lado="izq"),
    rel("hasta los patos van armados", "pato_goma", "Pato armado", "No le des la espalda", dur=3.6, x=.76, y=.52, tam=480),
    # ---- 22
    peg("una granada de humo", "humo", "Granada de humo", dur=3.4, x=.18, y=.64, tam=340, giro=-6),
    mg_en(C.objetivo("Mira los detalles", "Casi nadie se detiene"), "Son detalles que la saga", 3.6, "objetivo detalles", x=.30, y=.82),
    # ---- 21
    cam("En la misión de Bombay, el Patriot", "mumbai", "Bombay", dur=2.2, x=.16, y=.66, foco=(.5, .5, 1.2)),
    rel("el Patriot XMR", "patriot", "Patriot XMR", "La versión del ACR", dur=2.8, x=.76, y=.54, tam=500),
    peg("el AK setenta", "ak74u", "AK-74u · cinta blanca", dur=3.0, x=.78, y=.56, tam=380, giro=5),
    peg("Como la FAMAS", "famas", "FAMAS · MW2 2009", dur=3.4, x=.22, y=.62, tam=380, giro=-4),
    # ---- 20
    mg_en(C.objetivo("Inspecciona el arma", "Con las manos vacías"), "Si haces la animación", 3.6, "objetivo inspeccion", x=.30, y=.18),
    rel("como en Matrix", "matrix", "The Matrix", "1999", dur=3.4, x=.77, y=.52, tam=470),
    # ---- 19
    leg("m_ordenes", "CUMPLIENDO ÓRDENES", ["Following Orders", "Corea del Norte", "Juegas como norcoreano"],
        de="En la misión Cumpliendo órdenes juegas", a=("Y bajo los pies", -.2), x=.77, y=.52, ancho=500),
    mg_en(C.marcador("Periódico", 6, "Bajo la familia"), "Y bajo los pies", 2.8, "marcador periodico", x=.5, y=.40),
    cam("la de Infinite Warfare", "c_iw", "Infinite Warfare · 2016", dur=3.0, x=.16, y=.66, foco=(.5, .4, 1.3)),
    mg(C.balanza("Zombies en Modern Warfare 4", [("Modo Zombies", False, "no existe"), ("El periódico de la aldea", True, "sí")]),
       de="Modern Warfare 4 no tiene modo Zombies", a=("En el dieciocho", -.2), marcas=["no tiene modo Zombies", "periódico de la aldea"],
       nombre="balanza zombies", x=.5, y=.50),
    # ---- 18
    rel("persigue al Arquero", "arquero", "El Arquero", "Mads Mikkelsen", dur=3.2, x=.77, y=.50, tam=470),
    mg_en(C.objetivo("No te tumbes", "Price recibe daño"), "Si te tiras al suelo", 3.0, "objetivo tumbarse", x=.30, y=.82),
    cam("Alguien en Infinity Ward", "infinity_ward", "Infinity Ward", dur=3.2, x=.16, y=.66, foco=(.5, .5, 1.0)),
    # ---- 17
    ficha("encuentras lo prohibido", "Contrabando", "Novela occidental · reproductor con *música de fuera* · medicina del corazón.",
          "INTEL / REGISTRO", dur=6.0, x=.27, y=.28, ancho=760),
    peg("Son los mismos objetos", "pyongyang", "Corea del Norte · real", dur=3.6, x=.79, y=.58, tam=420, giro=4),
    # ---- 16
    mg_en(C.marcador("Camioneta", 12, "Desaparece"), "una camioneta que tapaba", 3.0, "marcador camioneta", x=.5, y=.40),
    mg_en(C.objetivo("Rescata a los rehenes", "Si dejas de mirarlos, se esfuman"), "En la misión del tren", 3.8, "objetivo rehenes",
          x=.30, y=.18),
    mg_en(C.marcador("Granada", 2), "te aparecen granadas", 2.4, "marcador granada", x=.5, y=.62),
    # ---- 15
    mg(C.linea("Wallcroft y Griffin", [(2007, "CoD 4", "Griffin, entrenamiento"), (2011, "MW3", "Metro de Londres"),
                                       (2026, "MW4", "Bombay, con Gaz")]),
       de="Personajes de la saga original", a=("Y siguen sin ascenso", -.2), marcas=["saga original", "reboot", "otra línea temporal"],
       nombre="linea sas", y=.52),
    # ---- 14
    leg("m_hiredgun", "HIRED GUN", ["Shadow Company", "Helicóptero derribado"], de="En la misión Hired Gun",
        a=("Y Graves te suplica", -.3), x=.25, y=.52, ancho=480),
    ficha("No hay botón para perdonarlo", "Perdonarlo", "*No hay botón*. Si dudas, Graves te mata.", "DECISIÓN / HIRED GUN",
          dur=3.6, x=.27, y=.28, ancho=700),
    # ---- 13
    rel("una estatua gigante", "lider", "Líder Supremo", "La estatua gigante", dur=3.2, x=.77, y=.52, tam=470),
    mg_en(C.objetivo("Escala la estatua", "Arriba: suministros y una nota"), "Y se puede escalar", 4.2, "objetivo estatua", x=.30, y=.18),
    cam("Acuérdate de esta estatua", "lider", "El Líder", dur=3.6, x=.16, y=.66, foco=(.5, .3, 1.5)),
    # ---- 12
    peg("Primera misión, una tienda", "hajin_logo", "Hajin · Corea del Sur", dur=3.0, x=.78, y=.56, tam=400, giro=4),
    sil("el cabo Dunn", "dunn", "Cabo Dunn", "Te lanza el bol", lado="izq", dur=4.0),
    peg("un bol de fideos instantáneos", "fideos", "Fideos instantáneos", dur=3.0, x=.80, y=.62, tam=340, giro=5),
    cam("se te activó el sentido", "spiderman", "Spider-Man", dur=3.6, x=.16, y=.66, foco=(.5, .3, 1.4)),
    mg_en(C.objetivo("Recoge los fideos", "El cabo Dunn insiste"), "Diálogo distinto", 3.4, "objetivo fideos", x=.30, y=.82),
    # ---- 11
    mg_en(C.marcador("Grafiti SOAP", 9), "Un grafiti con una pastilla", 3.0, "marcador grafiti", x=.58, y=.30),
    mg_en(C.sello("EXPEDIENTE 141", "ESTE CANAL"), "Y el de este canal", 2.4, "sello canal", x=.5, y=.48),
    # ---- 10
    ban("Pasamos al multijugador", "cachette", "Cachette", "Mapa multijugador", foco=(.5, .5, 1.1), dur=3.6, y=.62, lado="der"),
    mg_en(C.marcador("Impresora 3D", 18, "Armería · piso de arriba"), "hay una impresora 3D", 3.2, "marcador impresora 2",
          x=.36, y=.32),
    ficha("La descubrió un usuario", "muggs1213", "Usuario de *Reddit*: lo descubrió él.", "FUENTE / REDDIT", dur=3.4,
          x=.27, y=.28, ancho=640),
    rel("una mecánica de DMZ", "dmz", "DMZ", "Colada en el multijugador", dur=3.6, x=.77, y=.52, tam=470),
    # ---- 9
    leg("m_contraataque", "CONTRAATAQUE", ["Costa de Hajin", "Indicativos de 2007"], de="En el contraataque",
        a=("War Pig", -.2), x=.77, y=.52, ancho=480),
    peg("el tanque atascado", "war_pig_tanque", "War Pig · CoD 4", dur=3.0, x=.79, y=.62, tam=400, giro=4),
    cam("El mismo helicóptero de Jackson", "jackson", "Jackson · CoD 4", dur=3.4, x=.16, y=.66, foco=(.5, .35, 1.3)),
    # ---- 8
    leg("m_huida", "HUIDA", ["Escape", "Price y Ghost, capturados"], de="En la misión Huida ves", a=("Si te quedas mirando", -.3),
        x=.77, y=.52, ancho=480),
    mg_en(C.objetivo("Entra y rescata a Ghost", "No te quedes mirando"), "Si te quedas mirando", 2.6, "objetivo ghost", x=.30, y=.18),
    # ---- 7
    sil("la comandante Ri", "ri", "Comandante Ri", "Hermana del Líder", lado="der", dur=4.6),
    ficha("Si escondes a la familia", "La familia del sótano", "Si mientes, Ri lo descubre: *otra soga*.",
          "DECISIÓN / CUMPLIENDO ÓRDENES", dur=5.0, x=.27, y=.28, ancho=720),
    # ---- 6
    leg("m_trafico", "TRÁFICO", ["París", "Mosaicos de pixel art"], de="En la misión Tráfico", a=("Price con su sombrero", -.2),
        x=.25, y=.52, ancho=480),
    cam("de los edificios de París", "paris", "París", dur=2.6, x=.84, y=.30, foco=(.5, .5, 1.2)),
    # ---- 5
    ban("unos perros atacan", "price", "Price y Ghost", "Atacados por perros", foco=(.5, .25, 1.8), dur=3.6, y=.62, lado="izq"),
    rel("los de Prípiat", "pripyat", "Prípiat", "Ucrania", dur=3.6, x=.26, y=.50, tam=480),
    mg_en(C.contador(1996, "", "Price joven en Prípiat", desde=2026), "en mil novecientos noventa", 2.6, "contador 1996", x=.30, y=.50),
    mg_en(C.sello("CANON", "ALL GHILLIED UP"), "sigue siendo canon", 2.6, "sello canon", x=.5, y=.46),
    # ---- 4
    cam("persigues a Makarov por las azoteas", "makarov", "Makarov", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg_en(C.marcador("La tele", 8), "y miras la tele", 2.6, "marcador tele", x=.5, y=.30),
    rel("idéntico a GTA seis", "gta6", "GTA VI", "En una tele de MW4", dur=3.4, x=.77, y=.52, tam=470),
    peg("con guiños a Pitfall", "pitfall", "Pitfall! · Activision", dur=3.4, x=.80, y=.62, tam=360, giro=5),
    # ---- 3
    ban("En Cumpliendo órdenes buscas", "m_ordenes", "Cumpliendo órdenes", "Casa por casa", foco=(.5, .5, 1.1), dur=3.0, y=.62,
        lado="izq"),
    peg("Y no es del todo un chiste", "corea_norte_mapa", "Corea del Norte · real", dur=3.6, x=.79, y=.60, tam=360, giro=4),
    ficha("dañar un retrato del líder es", "Delito político", "En Corea del Norte, dañar un retrato del líder *es delito real*.",
          "INTEL / MUNDO REAL", dur=3.6, x=.27, y=.28, ancho=720),
    # ---- spoilers
    mg_en(C.objetivo("Termina la campaña", "Si no, retírate ahora"), "Si no lo has terminado", 3.4, "objetivo spoilers", x=.30, y=.82),
    # ---- 2
    leg("m_bombay", "GONE DARK", ["Bombay", "Gaz caza a Price"], de="En Bombay, Gaz, ya capitán", a=("Y dice esto", -.1), x=.25, y=.52,
        ancho=470),
    peg("Es la frase de Price en el tráiler", "c_mw2019", "Tráiler · 2019", dur=3.4, x=.80, y=.60, tam=380, giro=5),
    cam("para cazar al hombre", "price", "Price", dur=2.6, x=.16, y=.66, foco=(.5, .25, 1.8)),
    ficha("cortamos cabezas de serpiente", "Frases de Price", "*Cortamos cabezas de serpiente*, no nos unimos al nido.",
          "DIÁLOGO / GAZ", dur=4.0, x=.27, y=.28, ancho=760),
    mg_en(C.marcador("Caja fuerte", 14), "una nota dice que lo confiscado", 3.0, "marcador caja", x=.5, y=.34),
    rel("Dentro están las chapas", "chapas", "Chapas de Gaz", "La caja fuerte", dur=3.4, x=.77, y=.50, tam=440),
    cam("seguir creyendo que Gaz", "gaz", "Gaz", dur=3.6, x=.16, y=.66, foco=(.5, .25, 1.6)),
    # ---- 1
    leg("m_final", "GREATER GOOD", ["Misión final", "Un lago helado"], de="La saga termina", a=("Price mata", -.2), x=.77, y=.52,
        ancho=470),
    aba([("price", "Price"), ("ghost", "Ghost")], de="Price mata al Arquero", a=("Pero no acaba", -.2), marcas=["Price mata", "Ghost"],
        nombre="price ghost", x=.30, y=.62, tam=300),
    mg_en(C.radio("Post-créditos", "Escucha.", "AUDIO / MW4"), "Y de fondo suena esto", 7.0, "radio postcreditos", y=.80),
    rel("la música del final de CoD 4", "ost_cod4", "CoD 4", "Banda sonora · 2007", dur=3.6, x=.77, y=.52, tam=440),
    cam("acaba de matar a Zakhaev", "zakhaev", "Zakhaev", dur=2.8, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg_en(C.radio("CoD 4 · 2007", "El final del puente.", "AUDIO / 2007"), "Así sonaba en dos mil siete", 7.0, "radio cod4", y=.80),
    aba([("c_cod4", "2007"), ("c_mw4", "2026")], de="La saga empieza y termina", a=("Expediente cerrado", -.2),
        marcas=["empieza", "termina"], nombre="empieza termina", x=.70, y=.60, tam=320),
    rel("Yo apuesto por el pato", "pato_goma", "El pato", "Mi favorito", dur=3.2, x=.77, y=.52, tam=440),
]
ROTULOS = [r for r in ROTULOS if r["texto"] != "PULSA E"] + [
    dict(texto="ANTES QUE TÚ", en="Antes que tú", tam=130, color="amarillo", y=.22),
    dict(texto="PRESS F", en="Press F to pay", tam=150, color="amarillo", y=.22),
    dict(texto="NO LE DES LA ESPALDA", en="no le des la espalda", tam=110, color="amarillo", y=.22),
    dict(texto="MUY VIEJOS", en="Y nosotros, muy viejos", tam=140, color="amarillo", y=.22),
    dict(texto="PIEDRA, PAPEL O TIJERA", en="piedra, papel o tijera", tam=110, color="amarillo", y=.22),
    dict(texto="UN POCO", en="Un poco. Número diecisiete", tam=140, color="amarillo", y=.22),
    dict(texto="NO DEBÍAS VERLO", en="se ve un mapa abierto", tam=120, color="amarillo", y=.22),
    dict(texto="LA PIEDAD ES UNA TRAMPA", en="Y es una trampa", tam=110, color="amarillo", y=.22),
    dict(texto="IMPOSIBLE", en="Imposible, admite", tam=150, color="amarillo", y=.22),
    dict(texto="TE DUELE LA ESPALDA", en="para que te duela la espalda", tam=110, color="amarillo", y=.22),
    dict(texto="NI CON LA MIRADA", en="Ni con la mirada", tam=130, color="amarillo", y=.22),
    dict(texto="PRIORIDADES, SOLDADO", en="Prioridades, soldado", tam=120, color="amarillo", y=.22),
    dict(texto="NI LO MIRES FEO", en="ni lo mires feo", tam=130, color="amarillo", y=.22),
    dict(texto="BRAVO 6, GOING DARK", en="Bravo seis, going dark", tam=110, color="amarillo", y=.22),
    dict(texto="EL ROTO ES PRICE", en="El roto, ahora, es Price", tam=120, color="amarillo", y=.22),
    dict(texto="SIN ROSTRO", en="nunca le vemos la cara", tam=140, color="amarillo", y=.22),
]
# Cortes rápidos del gancho con clips ya bajados (debajo de todo lo demás)
VIDEOS = [
    vid(14, "Un pato de goma", ("Un bol", -.05), desde=4.6),               # el departamento de DMZ (el clip del tráiler va a negro)
    vid(53, ("Un bol", -.05), ("Y una impresora", -.05), desde=1.2),       # el bol en el suelo de la tienda de Hajin
    vid(61, ("Y una impresora", -.05), ("Le disparas", -.12), desde=0.0),  # la impresora 3D de Cachette
    vid(2, ("Le disparas", -.12), ("Te asomas", -.12), desde=1.7),         # los retratos → pantalla de muerte con «te ejecuta»
    vid(112, ("Ghost,", -.05), ("Gaz,", -.05), desde=0.4),                 # Ghost
    vid(57, ("hasta Soap", -.05), ("todos esconden", -.05), desde=1.8),    # el grafiti de SOAP
    vid(69, ("todos esconden", -.05), ("Infinity Ward lo metió", -.12), desde=0.1),   # la caja con las chapas de Gaz
    vid(85, ("Veinticinco secretos", -.05), ("Veinticinco secretos", 1.0), desde=4.0),
    vid(106, ("Veinticinco secretos", 1.0), ("Todos comprobados", .4), desde=2.4),
    vid(95, ("Todos comprobados", .4), ("Todos comprobados", 1.5), desde=3.0),
    vid(29, ("Todos comprobados", 1.5), ("con sus fuentes", .6), desde=0.3),
    vid(107, ("Y el número uno no se ve", -.05), ("Número veinticinco", -.12), desde=0.5, recorte=.125),   # Laswell, post-créditos
    vid(7, ("La tele que nadie", -.05), "scene-006", desde=1.5, recorte=.25),   # la guía de TV (sin el «#3» del creador)
]
FX = VIDEOS + FX

# ---- 2.ª pasada de relleno (3-nov-2026): los huecos de 4-14 s que quedaban
FX += [
    peg("Y Excessive Cakes", "c_mw4", "Programación inventada", dur=3.0, x=.80, y=.60, tam=340, giro=5),
    zoom("Y Excessive Cakes", ("Y al final de la misión", -.1), 1.15),
    mg_en(C.marcador("Arma", 3, "Barro y sangre"), "Agáchate a disparar", 3.4, "marcador barro", x=.62, y=.55),
    cam("Y si te disparan, se mancha", "c_mw4", "MW4 · 2026", dur=2.6, x=.16, y=.66, foco=(.5, .4, 1.2)),
    mg_en(C.contador(2009, "", "Hace diecisiete años", desde=2026), "Si eso no te dice nada", 2.8, "contador 2009", x=.30, y=.50),
    mg_en(C.marcador("Tu soldado", 1, "Se inventa otra cosa"), "a veces el personaje", 2.6, "marcador soldado", x=.5, y=.40),
    peg("Él solo. Número", "c_mw2r", "MW2 Remastered", dur=2.2, x=.20, y=.62, tam=320, giro=-5),
    mg_en(C.sello("CASTIGADO", "INFINITY WARD"), "Y decidió castigarlo", 2.2, "sello castigado", x=.5, y=.46),
    mg_en(C.marcador("Medicina", 4, "La necesita para vivir"), "Y la medicina del corazón", 3.0, "marcador medicina", x=.5, y=.40),
    mg_en(C.fallida("Confiscado", "Morirá de todos modos"), "Y la respuesta es que morirá", 2.0, "fallida medicina"),
    mg_en(C.objetivo("Sigue al equipo", "Tras el apagón"), "tras el apagón", 3.2, "objetivo apagon", x=.30, y=.82),
    mg_en(C.marcador("Mapa abierto", 30, "No debías verlo"), "y de pronto se ve", 2.6, "marcador mapa", x=.62, y=.40),
    mg_en(C.sello("INVISIBLE", "CASTIGO"), "Tiene castigos invisibles", 2.4, "sello invisible", x=.33, y=.46),
    rel("la piedad es una mecánica", "graves", "Graves", "Pide piedad", dur=3.4, x=.77, y=.52, tam=440),
    mg_en(C.contador(1, "CONTRA UN BATALLÓN", "La leyenda del Líder"), "japonés entero", 2.6, "contador batallon", x=.30, y=.50),
    ficha("Pero ahí se habrían bebido", "La leyenda", "Se habrían *bebido la tierra como agua* si él lo decía.",
          "INTEL / NORTE NEVADO", dur=3.6, x=.27, y=.28, ancho=720),
    rel("un juego de guerra", "fideos", "Fideos", "En un juego de guerra", dur=2.2, x=.77, y=.52, tam=400),
    peg("con un símbolo radiactivo", "soap", "SOAP · grafiti", dur=3.0, x=.80, y=.60, tam=340, giro=5),
    ficha("Y un letrero digital", "Letrero digital", "Ciudad nevada: *KR-SOAP* · y junto a él, *141*.", "INTEL / CAMPAÑA",
          dur=4.0, x=.27, y=.28, ancho=700),
    mg_en(C.contador(141, "", "Task Force", desde=100), "El número de la Task Force", 2.4, "contador 141", x=.30, y=.50),
    mg_en(C.contador(5, "ACCESORIOS", "Arma impresa"), "Cambia en cada partida", 2.6, "contador accesorios", x=.30, y=.50),
    leg("m_decap", "DECAPITATION", ["Helicóptero", "Indicativo Outlaw 2-5"], de="Y en Decapitation", a=("indicativo Outlaw", -.1),
        x=.77, y=.52, ancho=470),
    mg_en(C.radio("Canal abierto", "Solo se oyen por radio.", "RADIO / 2007"), "Solo se oyen por radio", 3.4, "radio solo", y=.28),
    sil("El personaje más querido", "ghost", "Ghost", "El más querido", lado="der", dur=3.6),
    mg_en(C.marcador("Comandante Ri", 15, "No le apuntes"), "Si le apuntas demasiado", 2.6, "marcador ri", x=.5, y=.30),
    ficha("ella y sus soldados", "Comandante Ri", "Si le apuntas demasiado, *te disparan*.", "PELIGRO / CUMPLIENDO ÓRDENES",
          dur=3.0, x=.27, y=.28, ancho=680),
    mg_en(C.objetivo("Ahorca al desertor", "Si te niegas, Ri te ejecuta"), "Y si al final te niegas", 3.0, "objetivo desertor", x=.30, y=.82),
    cam("El juego no te deja ser el bueno", "ri", "Comandante Ri", dur=3.4, x=.16, y=.66, foco=(.5, .3, 1.5)),
    rel("Riley no sale en esta saga", "riley_perro", "Riley", "Ghosts · 2013", dur=3.6, x=.77, y=.52, tam=440),
    mg(C.espejo("Price recuerda", (1996, "CoD 4", ["All Ghillied Up", "Perros en Prípiat"]), (2026, "MW4", ["Huida", "«No son nada»"]),
                "Canon"), de="El reboot es otra", a=("sigue siendo canon", -.2), marcas=["El reboot", "Price se acuerda"],
       nombre="espejo pripiat", y=.50),
    mg_en(C.marcador("El pasillo", 6, "Detente antes"), "Si te detienes antes", 2.4, "marcador pasillo", x=.5, y=.40),
    cam("tienes que dejar que Makarov", "makarov", "Makarov", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    rel("La estatua la puedes escalar", "lider", "El Líder", "Escala la estatua, no el cuadro", dur=3.4, x=.77, y=.52, tam=440),
    mg_en(C.contador(23, "PUESTOS VISTOS", "Quedan 2", desde=1), "Los que se quedan", 2.6, "contador quedan", x=.5, y=.50),
    mg_en(C.radio("Gaz", "Bravo seis, going dark.", "RADIO / BOMBAY"), "cazar a Price", 3.4, "radio gaz", y=.80),
    aba([("gaz", "Gaz"), ("price", "Price")], de="El roto, ahora", a=("cortamos cabezas", -.2), marcas=["Price", "Gaz se lo echa"],
        nombre="gaz price", x=.70, y=.60, tam=300),
    mg_en(C.marcador("Recepción", 20, "Cruzas desarmado"), "Otra nota, en una recepción", 2.8, "marcador recepcion", x=.5, y=.40),
    cam("a la que nunca le vemos", "laswell", "Laswell", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
]

for _r in ROTULOS:            # sin dur, un rótulo dura hasta el final del beat y tapa lo que viene (3-nov-2026)
    _r.setdefault("dur", 2.2)
