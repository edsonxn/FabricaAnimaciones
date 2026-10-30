# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 8 mundos de Banjo-Tooie del PEOR al MEJOR» (SECUENCIA YT, Crónicas del gaming, 30-oct-2026).
Kit TRANSLÚCIDO nucleo/mg_banjo.py (humo chocolate, filetes miel, Cooper Black + Arial Rounded) + PEGATINAS reales de la wiki.
- `puesto` = el Jiggy REAL que gira + `ficha_mundo` (jefe y transformación) + `cuatro_listas` (dónde lo puso cada lista).
- `egg` = contador de los 31 Easter eggs del video, en la esquina, cada uno con su palabra.
- MG NUEVOS de ESTE guion: `ruleta` (1 de cada 1000, el baño), `codigos` (la pared: SGGE, KCABYENOH, ESRA) y `conexiones` (cierre).
- MAPAS REALES de la Guía oficial de Nintendo (2000) con ruta y fotos en los 8 puestos (mapas/_coordenadas.md); tema `gaming`.
- Todo clip de la versión de Xbox lleva su rótulo: `xbox()`. Citas del juego leídas en pantalla (verificacion_clips.md).
- SFX DEL JUEGO (regla del 29-oct): sfx/bt_*.mp3.
  python fab.py bt_mundos_ranking fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py bt_mundos_ranking fx         audio/fx.wav
"""
import os

import mg_banjo as B
import mg_mapa as MP
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .42     # fichas: a la derecha (el rótulo de puesto va arriba)
JIGGY = os.path.join(_PEG, "jiggy.png")

CAMARA = {}
FUNDIDO = {}


def _p(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400):
    return dict(tipo="mg", fn=T.pegatina(_p(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.54, tam=tam)


def fila(items, y=.66, tam=290, dur=5.0):
    """Pegatinas en fila; items = [(ancla, slug, titulo)], cada una entra con su palabra."""
    xs = (.11, .29, .47, .65, .83)
    return [peg(a, s, t, dur=dur - .9 * i, x=xs[i], y=y, tam=tam) for i, (a, s, t) in enumerate(items)]


def ficha(en, titulo, texto, sub=None, dur=6.0, a=None, x=_FX, y=_FY):
    d = dict(tipo="mg", fn=B.ficha(titulo, texto, sub), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def xbox(en, dur=5.0):
    return dict(tipo="mg", fn=B.ficha("Xbox 360", "Versión de 2009", ancho=430), en=en, dur=dur, x=.86, y=.15, sale=.3,
                nombre="rótulo Xbox", ver=1.0)


def egg(en, num, titulo, dur=5.0, y=.11):
    return dict(tipo="mg", fn=B.egg(num, titulo), en=en, dur=dur, x=.19, y=y, sale=.35, nombre=f"egg {num}", ver=1.0)


def puesto(en, num, titulo, jefe, transf, dur=4.0):
    return [dict(tipo="mg", fn=B.puesto(num, titulo, JIGGY, etiqueta="PUESTO"), en=en, dur=dur, x=.5, y=.17, sale=.45,
                 nombre=f"puesto {num}", ver=1.4),
            dict(tipo="mg", fn=B.ficha_mundo([(_p(jefe[0]), "Jefe", jefe[1]), (_p(transf[0]), "Transformación", transf[1])]),
                 en=(en, 1.0), dur=4.6, x=.5, y=.86, sale=.35, nombre=f"mundo {num}", ver=1.3)]


def listas(en, mr, vb, tg, sj, media, dur=7.0):
    n8 = list("12345678")
    filas = [("MrDrBoi", n8, mr - 1), ("Virtual Bastion", n8, vb - 1), ("TheGamer", n8, tg - 1),
             ("Super Joe Bros", list("SABCDE"), "SABCDE".index(sj))]
    return dict(tipo="mg", fn=B.cuatro_listas("Las cuatro listas", filas, "Media: " + media), en=en, dur=dur, x=.5, y=.52,
                sale=.4, nombre="listas " + media, ver=4.0)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, recorte=None, **kw):
    """Mapa REAL con ruta (tema gaming). `puntos` en fracciones de la imagen ENTERA; con `recorte` se pasan solos al recorte."""
    ruta = os.path.join(_MAP, slug + ".jpg")
    if recorte:
        x0, y0, x1, y1 = recorte
        puntos = [((p[0] - x0) / (x1 - x0), (p[1] - y0) / (y1 - y0)) + tuple(p[2:]) for p in puntos]
    puntos = [p[:4] + ((_p(p[4]) if len(p) > 4 and p[4] else None),) if len(p) > 4 else p for p in puntos]
    fn = MP.mapa(ruta, puntos, "gaming", titulo=titulo, sub=sub, recorte=recorte, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


_TIT = {k: _p("titulo_" + k) for k in ("mt", "ggm", "ww", "jrl", "tdl", "gi", "hfp", "ccl")}
_NODOS = {"ggm": (_TIT["ggm"], .15, .16), "hfp": (_TIT["hfp"], .58, .14), "mt": (_TIT["mt"], .22, .54), "tdl": (_TIT["tdl"], .76, .54),
          "ww": (_TIT["ww"], .50, .88), "ccl": (_TIT["ccl"], .87, .14)}
_ENLACES = [("mt", "ggm", "la cueva de Dilberta"), ("mt", "tdl", "la reliquia de Targitzan"), ("ggm", "hfp", "el pasadizo helado"),
            ("ww", "tdl", "comida chatarra"), ("ccl", "tdl", "la piscina de Dippy")]

FX = [
    # ================================================================ GANCHO
    *fila([("Hay un cartón de leche", "tooty", "Tooty"), ("Una constelación escondida", "mr_pants", "Mr. Pants"),
           ("Y un pirata borracho", "blackeye", "Capitán Blackeye")], dur=8.0),
    xbox("Hay un cartón de leche", dur=4.0),
    peg("Hoy vamos a recorrer los ocho mundos", "caja_bt", "Banjo-Tooie (2000)", tam=460, x=.78, y=.56, dur=6.0),

    # ================================================================ CONTEXTO
    ficha("Crucé cuatro listas", "Cuatro listas", "MrDrBoi, Virtual Bastion, *TheGamer* y Super Joe Bros.", sub="La media decide el orden",
          a=("y saqué la media|fin", .8)),
    ficha("Los de Rare lo contaron", "El documental de Rare", "¿Cuántos *dobles sentidos* podían colar?", sub="Rare Revealed",
          a=("para que no se los cortaran|fin", .6), x=.27),
    peg("Este video también sale de un comentario", "com_Ugw_CCIkctKMyqDDO9l4AaABAg", "Riuma", tam=760, x=.5, y=.40, dur=8.0),
    peg("Son ocho mundos, con diez Jiggies", "jiggy", "10 Jiggies por mundo", tam=340, x=.20, y=.60, dur=4.6),
    peg("casi todos conectados entre sí", "chuffy", "Chuffy", tam=380, x=.80, y=.60, dur=4.4),

    # ================================================================ 8. GRUNTY INDUSTRIES
    *puesto("Puesto número ocho", 8, "Grunty Industries", ("weldar", "Weldar"), ("washer", "Lavadora")),
    peg("Ahora fabrica ropa interior", "gruntilda_bt", "Gruntilda", tam=420, x=.20, y=.58, dur=4.0),
    mapa("gi", [(.235, .83, "Inicio", "inicio"), (.30, .76), (.39, .63, "Puerta cerrada", "paso"), (.47, .72),
                (.55, .72, "La estación", "paso", "chuffy"), (.54, .58, "Grunty Industries", "meta")],
         de=("Y el mundo te recibe con una broma pesada", -.1), a=("y volver dentro de él|fin", .6),
         marcas=["Y el mundo te recibe", "La puerta está cerrada", "subirse al tren", "volver dentro de él"],
         titulo="Grunty Industries", sub="Guía oficial de Nintendo"),
    listas("¿Por qué está en el último lugar?", 8, 4, 7, "D", "6,5"),
    egg("Primer piso, cuartos de los trabajadores", 1, "La luz del baño", dur=11.0),
    mg(B.ruleta(), ("Steve Malpass, diseñador de Rare", -.1), ("sale luz por debajo|fin", 1.4), ["sale luz por debajo"], "ruleta"),
    egg("hay un refrigerador lleno de pegatinas", 2, "El refri de Rare", dur=7.0),
    xbox("Cuando el juego salió en Xbox", dur=5.0),
    ficha("Una letra, y problema resuelto", "DK o BK", "Nintendo 64: *DK*. Xbox 360: *BK*.", sub="El refrigerador", dur=4.6),
    egg("Una dice: entregar en Twycross", 3, "Twycross, Inglaterra"),
    xbox("Y otra, pegada a ella", dur=4.0),
    egg("Otra caja dice BIG-O PANTS", 4, "BIG-O PANTS"),
    peg("la mascota de la web de Rare", "mr_pants", "Mr. Pants", tam=380, x=.80, y=.58, dur=4.4),
    egg("En el baño de hombres regresa Loggo", 5, "Loggo"),
    peg("En el baño de hombres regresa Loggo", "loggo", "Loggo", tam=400, x=.80, y=.58, dur=5.0),
    egg("Y la transformación de Humba Wumba", 6, "La lavadora"),
    *fila([("Mumbo podía convertirte en lavadora", "mumbo", "Mumbo"), ("Aquí lo convierten en poder", "washer", "Lavadora")], tam=320, dur=6.0),
    grande("Cierro con el jefe", "weldar", "Weldar", lado="der", dur=6.6, tam=560),
    ficha("Su moraleja es muy buena", "La moraleja", "No tires nada: otro puede ver *lo que tú no viste*.", dur=5.0),

    # ================================================================ 7. JOLLY ROGER'S LAGOON
    *puesto("Puesto número siete", 7, "Jolly Roger's Lagoon", ("woo_fak_fak", "Lord Woo Fak Fak"), ("submarino", "Submarino")),
    mapa("jrl", [(.32, .04, "Inicio", "inicio"), (.35, .18), (.27, .31, "Jolly's", "paso", "jolly"), (.40, .42), (.50, .52),
                 (.57, .77, "Fondo del mar", "meta")],
         de=("Parece un pueblito pesquero", -.1), a=("hasta la Atlántida|fin", .4), marcas=["Parece un pueblito", "con un bar", "debajo hay un mar"],
         titulo="Jolly Roger's Lagoon", sub="Guía oficial de Nintendo"),
    listas("Collider lo llama el mundo", 7, 5, 8, "B", "6,3"),
    egg("El Easter egg más triste del juego", 7, "El pirata y el oso", dur=11.0),
    grande("En una habitación de Jolly's", "blackeye", "Capitán Blackeye", lado="der", dur=5.0, tam=520),
    ficha("Te dice que un oso le robó su gloria", "Capitán Blackeye", "«A bear stole me *glory*… looked a bit like you, 'e did!»",
          sub="Lo que dice en el juego", dur=6.0, x=.27),
    peg("Y Banjo salió de un personaje secundario", "banjo", "Banjo", tam=420, x=.80, y=.58, dur=4.6),
    egg("Bajo el agua hay un OVNI", 8, "Elvis y E.T.", dur=8.0),
    ficha("les pregunta si alguno se llama Elvis", "Kazooie", "«Are any of you called *Elvis*?»", sub="El texto del juego", dur=3.6, x=.27),
    ficha("si necesitan llamar a casa", "Kazooie", "«Let me guess, you need to *phone home*…»", sub="El texto del juego", dur=4.0, x=.27),
    egg("En el fondo del mar está el casillero", 9, "Los casilleros de Rare", dur=8.0),
    ficha("G. Kirkhope, el compositor", "Las placas", "*G. Kirkhope*, *G. Mayles*, S. Fileccia, D. Pashute y D. Jones.", sub="Casilleros", dur=5.6, x=.27),
    egg("En la tienda de empeños de Pawno", 10, "La caja B-K"),
    peg("En la tienda de empeños de Pawno", "pawno", "Pawno", tam=360, x=.80, y=.58, dur=4.4),
    egg("Y en este pueblo vive Merry Maggie", 11, "Merry Maggie Malpass"),
    ficha("aunque eso no está confirmado", "Sin confirmar", "El nombre vendría de *Steve Malpass*.", dur=3.6, x=.27),
    peg("Otro nombre con historia es el del jefe", "woo_fak_fak", "Lord Woo Fak Fak", tam=460, x=.78, y=.56, dur=6.0),
    ficha("Mumbo tiene un hechizo que se llama Sunlight", "Sunlight", "Efecto: *Oxygenated Water*.", sub="Hechizo de Mumbo", dur=6.0, x=.27),
    ficha("Un truco para este mundo", "Código", "*CHEATO* + *XOBEKUJ*", sub="Jukebox, al revés", dur=6.0),
    peg("otra te la vende Pawno", "cheato_page", "Página de Cheato", tam=340, x=.20, y=.60, dur=4.0),

    # ================================================================ 6. TERRYDACTYLAND
    *[dict(tipo="mg", fn=B.puesto(6, "Terrydactyland", JIGGY, etiqueta="PUESTO"), en="Puesto número seis", dur=4.0, x=.5, y=.17,
           sale=.45, nombre="puesto 6", ver=1.4),
      dict(tipo="mg", fn=B.ficha_mundo([(_p("terry"), "Jefa", "Terry")]), en=("Puesto número seis", 1.0), dur=4.6, x=.5, y=.86,
           sale=.35, nombre="mundo 6", ver=1.3)],
    listas("Otro mundo que parte a los fans", 6, 3, 4, "E", "5,3"),
    egg("El mejor engaño está en Chompa", 12, "La barriga de Chompa", dur=8.0),
    peg("El mejor engaño está en Chompa", "chompa", "Chompa", tam=440, x=.80, y=.58, dur=5.0),
    egg("Del Stomponadon, un dinosaurio gigantesco", 13, "El pie del Stomponadon", dur=7.0),
    peg("Del Stomponadon, un dinosaurio gigantesco", "stomponadon", "Stomponadon", tam=460, x=.78, y=.56, dur=5.4),
    peg("Terry, la jefa del mundo", "terry", "Terry", tam=460, x=.78, y=.56, dur=5.4),
    mapa("tdl", [(.665, .77, "Inicio", "inicio"), (.61, .62), (.59, .45), (.52, .41, "Unga Bunga", "paso", "unga_bunga"), (.585, .43),
                 (.645, .40, "Oogle Boogle", "paso"), (.56, .40), (.42, .36), (.28, .30), (.16, .28, "Dippy", "meta", "dippy")],
         de=("Lo mejor de Terrydactyland son sus conexiones", -.1), a=("y el agua cae hasta aquí|fin", .6),
         marcas=["Lo mejor de Terrydactyland", "La cueva de Unga Bunga", "La cueva de Oogle Boogle", "la piscina de Dippy"],
         titulo="Terrydactyland", sub="Guía oficial de Nintendo", recorte=(.06, .10, .76, .84)),

    # ================================================================ 5. MAYAHEM TEMPLE
    *puesto("Puesto número cinco", 5, "Mayahem Temple", ("targitzan", "Targitzan"), ("stony", "Stony")),
    listas("Para Super Joe Bros es el mejor arranque", 5, 8, 5, "A", "5,3"),
    peg("por primera vez en la saga, controlas a Mumbo", "mumbo", "Mumbo", tam=420, x=.80, y=.58, dur=4.6),
    ficha("La segunda es Kazooie como arma", "GoldenEye", "Casi todas las *horas de comida*, durante un par de años.",
          sub="Chris Sutherland, Rare", a=("durante un par de años|fin", .6), x=.27),
    mapa("mt", [(.255, .91, "Inicio", "inicio"), (.245, .72), (.31, .50), (.39, .35), (.50, .27), (.60, .33), (.66, .50), (.665, .70),
                (.56, .69), (.52, .60, "Templo de Targitzan", "meta", "targitzan")],
         de=("Y eso se coló en el juego", -.1), a=("en el templo de Targitzan|fin", .8), marcas=["Y eso se coló", "en el templo de Targitzan"],
         titulo="Mayahem Temple", sub="Guía oficial de Nintendo"),
    peg("apuntando con su mejor amiga", "blaster", "Breegull Blaster", tam=420, x=.20, y=.60, dur=4.4),
    peg("Targitzan, por cierto, es el dios maya", "targitzan", "Targitzan", tam=460, x=.78, y=.56, dur=5.6),
    egg("Ahora el Easter egg que más gente", 14, "La Cámara de Códigos", dur=8.0),
    peg("Una sala con la pared llena de letras", "cheato", "Cheato", tam=360, x=.80, y=.60, dur=4.4),
    mg(B.codigos([("SGGE", "EGGS", "doble de huevos"), ("KCABYENOH", "HONEY BACK", "la salud se recupera")]),
       ("Todos los códigos empiezan con CHEATO", -.1), ("honey back|fin", .8), ["CHEATO SGGE", "CHEATO KCABYENOH"], "codigos"),
    egg("Y mira la primera fila de la pared", 15, "E S R A", dur=7.0),
    mg(B.codigos([("ESRA", "ARSE", "culo, en inglés británico")]), ("Empieza con E, S, R, A", -.1), ("Que en el inglés británico|fin", 1.0),
       ["Empieza con"], "arse", y=.70),
    egg("Y hay más chistes en los nombres", 16, "Las cámaras sagradas", dur=8.0),
    peg("Viene de un tema descartado", "bk_1998", "Banjo-Kazooie (1998)", tam=420, x=.20, y=.58, dur=4.6),

    # ================================================================ 4. GLITTER GULCH MINE
    *puesto("Puesto número cuatro", 4, "Glitter Gulch Mine", ("old_king_coal", "Old King Coal"), ("detonator", "Detonator")),
    listas("A MrDrBoi le encanta", 4, 6, 6, "B", "5,0"),
    ficha("Lo curioso es que este mundo", "Retro Gamer", "Idea de *Banjo-Kazooie*, aplazada por falta de tiempo.", sub="Chris Sutherland",
          a=("por falta de tiempo|fin", .6), x=.27),
    egg("Canary Mary, la de las carreras", 17, "Canary Mary", dur=8.0),
    grande("Canary Mary, la de las carreras", "canary_mary", "Canary Mary", lado="der", dur=6.0, tam=540),
    egg("El jefe es Old King Coal", 18, "Old King Coal", dur=7.0),
    grande("El jefe es Old King Coal", "old_king_coal", "Old King Coal", lado="der", dur=6.0, tam=560),
    *fila([("Bullion Bill, el minero", "bullion_bill", "Bullion Bill"), ("Y su socia es Dilberta", "dilberta", "Dilberta")], tam=330, dur=7.0),
    mapa("ggm", [(.10, .83, "Inicio", "inicio"), (.30, .70), (.37, .42), (.41, .30, "Crushing Shed", "meta")],
         de=("Y mira la Crushing Shed", -.1), a=("y de ahí sale tu Jiggy|fin", .6), marcas=["Y mira la Crushing Shed", "Una roca con una veta"],
         titulo="Crushing Shed", ventana=True),
    egg("Ahora el secreto grande", 19, "Bottles' Revenge", dur=8.0),
    peg("¿Recuerdas Bottles' Revenge", "devil_bottles", "Bottles' Revenge", tam=440, x=.80, y=.58, dur=5.4),
    mapa("ggm", [(.10, .83, "Inicio", "inicio"), (.30, .70), (.37, .42), (.50, .50), (.53, .57, "Flooded Caves", "meta")],
         de=("Y otro más. Bajo el agua", -.1), a=("al lado helado de Hailfire Peaks|fin", .6), marcas=["Y otro más", "Bajo el agua hay una roca"],
         titulo="Glitter Gulch Mine", sub="Guía oficial de Nintendo"),
    peg("Allí, una llave de hielo", "mega_glowbo", "Mega Glowbo", tam=400, x=.80, y=.58, dur=5.6),

    # ================================================================ 3. CLOUD CUCKOOLAND
    *puesto("Puesto número tres", 3, "Cloud Cuckooland", ("mingy_jongo", "Mingy Jongo"), ("bee_banjo", "Abeja")),
    listas("Un mundo que flota sobre la isla", 3, 7, 2, "C", "4,5"),
    egg("Ahora el Easter egg más famoso", 20, "Missing: Tooty", dur=11.0, y=.27),
    peg("Lo primero que haces al llegar", "george", "George Ice Cube", tam=400, x=.80, y=.58, dur=6.0),
    mapa("ccl", [(.80, .65, "Inicio", "inicio"), (.69, .61), (.60, .56), (.42, .50), (.24, .70), (.11, .80, "Bote de basura", "meta", "tooty")],
         de=("Ahora el Easter egg más famoso", -.1), a=("Vista por última vez en Banjo-Kazooie|fin", .4),
         marcas=["Ahora el Easter egg", "Dentro del bote de basura"], titulo="Cloud Cuckooland", sub="Guía oficial de Nintendo"),
    ficha("Y el chiste terminó siendo verdad", "Tooty", "*Nunca* volvió a aparecer.", sub="Banjo-Kazooie, 1998", dur=4.4, x=.27),
    egg("El nombre del mundo es uno de los guiños", 21, "Aristófanes", dur=8.0),
    ficha("Cloud cuckoo land viene de Aristófanes", "Las aves", "Aristófanes, *414 a. C.*", sub="Comedia griega", dur=6.0),
    egg("En este mundo hay una caja fuerte", 22, "Superstash", dur=8.0),
    xbox("Se abre con cuatro números", dur=5.0),
    ficha("Se abre con cuatro números", "Superstash", "*1 / 9 / 8 / 4*", dur=5.0, x=.27, y=.74),
    ficha("Rare se fundó en mil novecientos", "Teoría", "Rare: *1985*. Sabre Wulf, de Ultimate: *1984*.", dur=6.6),
    peg("Mingy Jongo, un doble robot", "mingy_jongo", "Mingy Jongo", tam=460, x=.78, y=.56, dur=5.4),
    peg("aquí también está la segunda carrera", "canary_mary", "Canary Mary", tam=380, x=.20, y=.60, dur=5.0),

    # ================================================================ 2. WITCHYWORLD
    *puesto("Puesto número dos", 2, "Witchyworld", ("mr_patch", "Mr. Patch"), ("van", "La Van")),
    listas("Virtual Bastion lo pone primero", 2, 1, 3, "S", "1,9"),
    egg("Y aquí está la constelación del principio", 23, "Mr. Pants en el cielo", dur=11.0, y=.27),
    mapa("ww", [(.82, .58, "Inicio", "inicio"), (.68, .50), (.48, .45, "La carpa", "paso"), (.50, .68), (.62, .84, "Dodgem Dome", "meta", "dodgem")],
         de=("Y aquí está la constelación del principio", -.1), a=("Entra al vestíbulo del Dodgem Dome|fin", .4),
         marcas=["Y aquí está", "la constelación del principio", "Entra al vestíbulo"], titulo="Witchyworld", sub="Guía oficial de Nintendo"),
    xbox("Las estrellas forman la figura", dur=7.0),
    peg("Mister Pants era la mascota", "mr_pants", "Mr. Pants", tam=440, x=.80, y=.58, dur=6.0),
    egg("El mejor chiste del parque está en un letrero", 24, "El letrero de los sobornos", dur=8.0),
    ficha("Avisa que Witchyworld está cerrado", "Mr. Patch", "«*Appalling safety record*… once the authorities have been *bribed*…»",
          sub="El letrero del parque", dur=7.0, x=.27),
    egg("La comida también tiene su humor", 25, "Cien por ciento roedor", dur=9.0),
    *fila([("El letrero de Big Al", "big_al", "Big Al"), ("Y el de las papas de Salty Joe", "salty_joe", "Salty Joe")], tam=340, dur=8.0),
    egg("La música tiene un secreto", 26, "Chase, de Project Dream", dur=7.0),
    peg("Pero hay algo que nadie olvida", "van", "La Van", tam=480, x=.78, y=.56, dur=6.0),

    # ================================================================ 1. HAILFIRE PEAKS
    *[dict(tipo="mg", fn=B.puesto(1, "Hailfire Peaks", JIGGY, etiqueta="PUESTO"), en="Y llegamos al número uno", dur=4.4, x=.5, y=.17,
           sale=.45, nombre="puesto 1", ver=1.4),
      dict(tipo="mg", fn=B.ficha_mundo([(_p("chilli_billi"), "Jefe", "Chilli Billi"), (_p("chilly_willy"), "Jefe", "Chilly Willy"),
                                        (_p("snowball"), "Transformación", "Bola de nieve")]),
           en=("Y llegamos al número uno", 1.0), dur=5.0, x=.5, y=.86, sale=.35, nombre="mundo 1", ver=1.3)],
    listas("Las cuatro listas lo ponen arriba", 1, 2, 1, "S", "1,4"),
    ficha("Y tiene historia", "Mount Fire Eyes", "Nivel *cortado* de Banjo-Kazooie.", dur=5.0),
    peg("Gobi, el camello del primer juego", "gobi", "Gobi", tam=460, x=.78, y=.56, dur=6.0),
    peg("Con esa agua enfrías la caldera", "chuffy", "Chuffy", tam=400, x=.20, y=.60, dur=4.4),
    egg("El Easter egg más viejo de todos", 27, "Sabreman", dur=8.0, y=.27),
    mapa("hfp_hielo", [(.40, .92, "Lado de lava", "inicio"), (.45, .72), (.52, .60), (.63, .50), (.64, .38), (.62, .20), (.79, .115, "Sabreman", "meta", "sabreman")],
         de=("El Easter egg más viejo de todos", -.1), a=("llevarlo hasta su tienda|fin", .4), marcas=["El Easter egg más viejo", "está atrapado en el hielo"],
         titulo="Hailfire Peaks", sub="Lado de hielo"),
    mapa("hfp_hielo", [(.68, .28, "Los Boggy", "meta", "boggy_tooie")], de=("Y ahora, la casa de Boggy", -.1), a=("y tiene tele|fin", .6),
         marcas=["Y ahora, la casa de Boggy"], titulo="El iglú", ventana=True, recorte=(.46, .06, .90, .50)),
    egg("¿Y qué sale en la tele?", 28, "La tele de Boggy", dur=5.0),
    peg("¿Y qué sale en la tele?", "mr_pants", "Mr. Pants", tam=380, x=.20, y=.60, dur=4.4),
    egg("Boggy te invita a quedarte", 29, "Bear Babes", dur=9.0),
    ficha("Boggy te invita a quedarte", "Boggy", "«Bear Babes DVD: should be *hot stuff*.»", sub="El texto del juego", dur=8.0, x=.27),
    egg("En el cuarto de los niños Boggy", 30, "Muñeco de nieve", dur=7.0),
    egg("¿Recuerdas a George Ice Cube", 31, "George y Mildred", dur=9.0),
    *fila([("Y su pareja es Mildred Ice Cube", "george", "George Ice Cube"), ("Y su pareja es Mildred Ice Cube", "mildred", "Mildred Ice Cube")], tam=330, dur=8.0),
    xbox("Son George y Mildred Roper", dur=5.0),
    ficha("Son George y Mildred Roper", "George y Mildred", "*Comedia británica* de los años setenta.", dur=6.0),
    mapa("hfp", [(.49, .85, "Inicio", "inicio"), (.49, .62), (.47, .49), (.30, .48), (.175, .44, "La calavera de Mumbo", "paso", "mumbo"),
                 (.15, .30), (.15, .20, "Hacia el wigwam de Humba", "meta", "humba")],
         de=("Mumbo y Humba, los rivales", -.1), a=("al wigwam en el hielo|fin", .6), marcas=["Mumbo y Humba", "de la calavera en la lava", "al wigwam en el hielo"],
         titulo="Hailfire Peaks", sub="Lado de lava"),
    peg("La caja de hielo de Glitter Gulch", "dragon_kazooie", "Kazooie dragón", tam=480, x=.78, y=.56, dur=6.0),

    # ================================================================ CIERRE
    mg(B.conexiones(_NODOS, _ENLACES), ("Mayahem conecta con Glitter Gulch", -.1), ("le llena la piscina a Dippy|fin", 1.0),
       ["Mayahem conecta", "y con Terrydactyland", "Glitter Gulch, con Hailfire", "Witchyworld, con Terrydactyland", "le llena la piscina"], "conexiones"),
    ficha("¿Tú cuál pones en el número uno?", "Tu turno", "¿Viste *la luz del baño*? Cuéntamelo en los comentarios.", dur=7.0),
]
ROTULOS = []
SFX = {}
# SONIDOS DEL PROPIO JUEGO (regla del 29-oct-2026): sfx/bt_*.mp3
_EGGS = ["Primer piso, cuartos de los trabajadores", "hay un refrigerador lleno de pegatinas", "Una dice: entregar en Twycross",
         "Otra caja dice BIG-O PANTS", "En el baño de hombres regresa Loggo", "Y la transformación de Humba Wumba",
         "El Easter egg más triste del juego", "Bajo el agua hay un OVNI", "En el fondo del mar está el casillero",
         "En la tienda de empeños de Pawno", "Y en este pueblo vive Merry Maggie", "El mejor engaño está en Chompa",
         "Del Stomponadon, un dinosaurio gigantesco", "Ahora el Easter egg que más gente", "Y mira la primera fila de la pared",
         "Y hay más chistes en los nombres", "Canary Mary, la de las carreras", "El jefe es Old King Coal", "Ahora el secreto grande",
         "Ahora el Easter egg más famoso", "El nombre del mundo es uno de los guiños", "En este mundo hay una caja fuerte",
         "Y aquí está la constelación del principio", "El mejor chiste del parque está en un letrero", "La comida también tiene su humor",
         "La música tiene un secreto", "El Easter egg más viejo de todos", "¿Y qué sale en la tele?", "Boggy te invita a quedarte",
         "En el cuarto de los niños Boggy", "¿Recuerdas a George Ice Cube"]
_ROTA = ["bt_nota", "bt_pluma", "bt_panal", "bt_nota", "bt_correcto", "bt_pluma"]
PISTAS = [dict(sfx=_ROTA[i % len(_ROTA)], en=e, vol=.5) for i, e in enumerate(_EGGS)] + [
    dict(sfx="bt_jiggy", en=f"Puesto número {n}", vol=.5) for n in ("ocho", "siete", "seis", "cinco", "cuatro", "tres", "dos")] + [
    dict(sfx="bt_jiggy", en="Y llegamos al número uno", vol=.55),
    dict(sfx="bt_panal_skill", en="sale luz por debajo", vol=.5),
    dict(sfx="bt_jinjo", en="Hoy vamos a recorrer los ocho mundos", vol=.5),
    dict(sfx="bt_guhuh", en="Nos vemos en la próxima crónica", vol=.55),
]
