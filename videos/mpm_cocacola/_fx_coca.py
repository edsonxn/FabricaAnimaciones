

# ======================================================================================================================
# mpm_cocacola (24-nov-2026). Datos: investigacion.md (cada uno con fuente). Clips: metraje.md / fuentes.json.
# Coordenadas de los mapas: mapas/lugares.json (OpenStreetMap) → mapas/xy.json (con _mapa_base.ll).
# OJO: CAMARA solo mueve IMÁGENES, no clips de video. «→», «×», «−», «≈» no se usan en textos (Bahnschrift).
CAMARA = {}
FUNDIDO = {}

from PIL import Image as _Im, ImageDraw as _Dr
import json as _json

_AQUI = os.path.dirname(os.path.abspath(__file__))
_XY = _json.load(open(os.path.join(_AQUI, "mapas", "xy.json"), encoding="utf-8"))


def xy(lugar):
    return tuple(_XY[lugar][1:])


def plano(activa, de, a, marcas=(), sub=None):
    """FIRMA: plano de la línea a pantalla completa (estación activa o recorrido con marcas)."""
    return dict(tipo="pantalla", fn=P.plano(ESTACIONES, activa, "Así se embotella una Coca-Cola", sub=sub, pieza="botella"),
                de=de, a=a, marcas=list(marcas), entra=.4, sale=.4, nombre=f"plano {activa}", ver=3.0)


ESTACIONES = [("Concentrado", "caja"), ("Agua", "agua"), ("Jarabe", "tanque"), ("Botella", "soplado"), ("Retornables", "lavadora"),
              ("Gas", "co2"), ("Llenado", "llenadora"), ("Tapa", "tapa"), ("Revisión", "etiqueta"), ("Tarimas", "tarima")]


def pvr(en, ruta, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    """pv() con una imagen fuera de pegatinas/ (pantallas/, mapas…)."""
    import peg_anim as PA
    fn = PA.variado(ruta, titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + os.path.basename(ruta), ver=1.0)


def _placa(titulo, sub, color):
    """Placa chica abajo a la izquierda: de qué planta / archivo es el clip (regla del canal: cada imagen por identidad)."""
    f1, f2 = P.fuente("b", 26, "Bold Condensed"), P.fuente("b", 19, "SemiBold Condensed")
    w = max(300, min(560, int(16 * max(len(titulo), len(sub or "")) + 60)))
    h = 64 if sub else 46

    def fn(dt, dur, marcas):
        im = _Im.new("RGBA", (w, h), (0, 0, 0, 0))
        d = _Dr.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), 6, fill=(15, 18, 22, 190))
        if color == "ref":
            P._franjas(d, 6, 8, 22, h - 8, 255, paso=7)
            col = P.AMARILLO
        else:
            d.rectangle((6, 8, 22, h - 8), fill=P.NARANJA + (255,))
            col = P.NARANJA
        P._txt(d, (34, 22 if sub else h / 2), titulo, f1, col, "lm")
        if sub:
            P._txt(d, (34, 46), sub, f2, P.HUESO, "lm", 230)
        return P._bgra(im, min(P._eo(dt / .4), max(0.0, (dur - dt) / .4)))
    return fn


_PLACAS = {
    "zyrzswdZe2g": ("PLANTA TOLUCA · COCA-COLA FEMSA", "metraje de Forbes México", "real"),
    "wMctmMin9vM": ("PLANTA DE COCA-COLA · EE.UU.", "Baton Rouge, Luisiana", "real"),
    "IUMK2LY3pIs": ("PLANTA DE COCA-COLA · EE.UU.", "Marietta, Georgia", "real"),
    "fYW_-YRY5Ls": ("COCA-COLA EMBONOR · CHILE", None, "real"),
    "3VHBeoFd1FM": ("COCA-COLA HBC · NIGERIA", None, "real"),
    "u0rQ_7ymRo8": ("ARCA CONTINENTAL · ECUADOR", None, "real"),
    "jVDEicwgb4w": ("COCA-COLA FEMSA · BRASIL", None, "real"),
    "eDinB9pnzhg": ("BEPENSA · MÉRIDA", None, "real"),
    "NuteIxJeDUw": ("CORPORACIÓN RICA · PACHUCA", None, "real"),
    "GsCcOphYld4": ("PLANTA LEÓN · COCA-COLA FEMSA", None, "real"),
    "DWXVQwxj3Q4": ("COCA-COLA HBC · AUSTRIA", None, "real"),
    "yP4nzCHoVSE": ("COCA-COLA ANDINA · ARGENTINA", None, "real"),
    "n7-XU3fNhpM": ("COCA-COLA ANDINA", None, "real"),
    "bcatrD251VA": ("ARCHIVO · 1939", "«Refreshment Through the Years»", "real"),
    "7wFEz_z0XhY": ("ARCHIVO · AÑOS 40", None, "real"),
    "TcSgz8Ws_NE": ("EQUIPO DE REFERENCIA", "maquinaria del mismo tipo · sin marca", "ref"),
    "-hV5CkqvAcI": ("COCA-COLA ANDINA · CHILE", None, "real"),
    "1jGfv5ODsaI": ("EQUIPO DE REFERENCIA", "un pozo de agua · no es de Coca-Cola", "ref"),
}
_fu = _json.load(open(os.path.join(_AQUI, "fuentes.json"), encoding="utf-8"))
_SIN_PLACA = {"scene-049", "scene-050", "scene-061", "scene-062", "scene-063", "scene-064", "scene-065", "scene-067",
              "scene-068", "scene-069", "scene-104", "scene-105", "scene-106", "scene-107", "scene-108", "scene-109", "scene-110", "scene-111",
              "scene-024", "scene-025"}       # bajo mapas a pantalla completa
_REF = [dict(tipo="mg", fn=_placa(*_PLACAS[v["video"]]), de=k, a=k + ":fin", x=.17, y=.935, sale=.06, nombre="placa " + k, ver=1.0)
        for k, v in sorted(_fu.items()) if k.startswith("scene-") and v.get("video") in _PLACAS and k not in _SIN_PLACA]


def est(n, nombre, frase, porque, dur_plano=2.6, dur_card=3.6):
    """Estación N: PLANO de la línea (pantalla) al decir «Estación N» y luego la tarjeta con el porqué sobre el clip."""
    return [plano(n - 1, (frase, -.15), (frase, dur_plano), sub=f"Estación {n} de 10 · {nombre}"),
            mg(P.estacion(n, 10, nombre, porque), (frase, dur_plano), (frase, dur_plano + dur_card), x=.30, y=.80,
               nombre=f"estacion {n}")]


def et(texto, sub, de, dur=2.6, x=.50, y=.26):
    return mg(P.etiqueta(texto, sub), de, (de, dur), x=x, y=y, nombre="etiqueta " + texto.lower()[:18])


# ESCENAS 3D (el usuario, 24-nov-2026: «en escenas de proceso, escena 3d con cámara orbital»). nucleo/fabrica3d.py renderiza
# tres_d/<toma>.mp4 en el estilo elegido; mientras no exista el archivo, el FX no entra (el video se arma igual).
ESTILO_3D = None


def tres_d(toma, de, a, desde=0.0):
    ruta = os.path.join(_AQUI, "tres_d", f"{toma}.mp4")
    if not os.path.exists(ruta):
        return None
    return dict(tipo="video", ruta=ruta, de=de, a=a, desde=desde, recorte=0.0, entra=.25, sale=.25, nombre=f"3d {toma}")


def tarjeta(de, a):
    """Fondo que oscurece el clip (para cubrir una entrevista con una cifra a pantalla)."""
    return dict(tipo="fondo", de=de, a=a, entra=.3, sale=.3, nombre="fondo tarjeta")


ESTRELLA_CONTADOR = 9553.8e6 / (365 * 24 * 3600)      # ≈ 302.95 botellas o latas por segundo (KOF México 2025)

FX = [
    # ---------------------------------------------------------------- firma: contador de botellas (todo el video hasta el cierre)
    mg(P.contador_produccion(ESTRELLA_CONTADOR, "BOTELLAS Y LATAS", "VENDIDAS POR COCA-COLA FEMSA EN MÉXICO DESDE QUE EMPEZÓ ESTE VIDEO",
                             nota="9,553.8 millones en 2025 entre los segundos del año · reporte 4T25"),
       0, ("scene-117:fin", .4), x=.855, y=.085, nombre="contador botellas", ver=1.0),

    # ---------------------------------------------------------------- gancho
    pv("Una botella con cintura", "botella_contour", "La botella con cintura", dur=4.0, x=.80, y=.52, tam=480),
    et("5¢ EL VASO", "Atlanta · mayo de 1886", "se vendía a cinco centavos", dur=2.6, y=.24),
    mg(P.cifra(9, titulo="VASOS AL DÍA · PRIMER AÑO (1886)", texto="9 AL DÍA"), ("el promedio fue de nueve", -.1),
       ("nueve vasos al día|fin", 1.4), y=.46, nombre="cifra 9"),
    mg(P.cifra(2200, titulo="BEBIDAS DE LA COMPAÑÍA · CADA DÍA EN EL MUNDO", texto="2,200 MILLONES"), ("se sirven más de dos mil", -.1),
       ("de esta compañía cada día|fin", .6), y=.46, nombre="cifra 2200"),
    et("CASI NO EMBOTELLA", "vende un concentrado", "casi no embotella Coca-Cola", dur=2.8),
    pv("Vende un concentrado", "tccc_logo", "The Coca-Cola Company", dur=3.4, x=.20, y=.62),
    pv("La más grande de todas es mexicana", "kof_logo", "Coca-Cola FEMSA", dur=4.0, x=.78, y=.55, tam=440),
    mg(P.cifra(9553, titulo="BOTELLAS Y LATAS · COCA-COLA FEMSA EN MÉXICO · 2025", texto="9,553 MILLONES"),
       ("vendió nueve mil quinientos", -.1), ("de botellas y latas|fin", .8), y=.46, nombre="cifra 9553"),
    pant("boveda", ("hay una bóveda", -.1), ("agua de pozo que se limpia", -.05), zoom=(1.0, 1.10)),
    pv("una preforma que se infla", "preforma", "Una preforma", dur=3.2, x=.78, y=.55, tam=440),
    tres_d("general", ("una máquina que llena botellas", -.1), ("sin parar|fin", .2), desde=2.0),
    plano(None, ("Así que hoy entramos a la planta", -.1), ("realmente una Coca-Cola|fin", .2), sub="10 estaciones, del pozo al camión"),
    mg(P.etiqueta("MIRA LA ESQUINA", "botellas y latas de Coca-Cola FEMSA en México"), "Mira la esquina",
       ("Son unas trescientas por segundo", -.1), x=.55, y=.24, nombre="etiqueta esquina"),
    mg(P.cifra(303, titulo="POR SEGUNDO · SOLO COCA-COLA FEMSA EN MÉXICO", texto="~303 POR SEGUNDO"),
       ("Son unas trescientas por segundo", -.1), ("cuántas juntó|fin", .4), y=.46, nombre="cifra 303"),

    # ---------------------------------------------------------------- origen
    mapa("eeuu_sur", [xy("Atlanta") + ("Atlanta, Georgia · 1886", "meta", None)], "un farmacéutico de Atlanta",
         ("John Pemberton|fin", .2), ["un farmacéutico de Atlanta"], ventana=True, x=.30, y=.40),
    pv("John Pemberton", "pemberton", "John S. Pemberton", dur=4.6, x=.78, y=.52, tam=460),
    pv("la Farmacia Jacobs", "jacobs_pharmacy", "Farmacia Jacobs · pintura oficial", dur=4.6, x=.74, y=.50, tam=540),
    pv("Frank Robinson", "robinson", "Frank M. Robinson", dur=3.6, x=.80, y=.55, tam=420),
    pv("escribió el logo a mano", "coca_logo", "Su letra, su logo", dur=3.4, x=.30, y=.32, tam=520),
    et("1888", "muere Pemberton", "Pemberton murió en 1888", dur=2.6, x=.30),
    pv("el que se quedó con todo", "candler", "Asa G. Candler", dur=6.6, x=.78, y=.52, tam=460),
    mg(P.cifra(2300, "$", titulo="POR QUEDARSE CON TODO · 1891", texto="$2,300"), ("En total, dos mil trescientos", -.1),
       ("dos mil trescientos dólares|fin", 1.2), y=.46, nombre="cifra 2300"),
    mg(P.linea_tiempo("DE LA FARMACIA A LA BOTELLA", [("1886", "Pemberton, Atlanta"), ("1891", "Candler se queda con todo"),
                                                      ("1892", "The Coca-Cola Company"), ("1894", "La primera botella")]),
       ("En 1892 fundó", -.2), ("en Vicksburg, Mississippi", -.1), ["En 1892 fundó", "Y dos años después", ("Y dos años después", 1.2)],
       y=.30, nombre="linea origen"),
    mapa("eeuu_sur", [xy("Atlanta") + ("Atlanta", "inicio", None), xy("Vicksburg") + ("Vicksburg, Mississippi · 1894", "meta", None)],
         "en Vicksburg, Mississippi", ("la metió en botellas|fin", .2), ["en Vicksburg, Mississippi", "Joseph Biedenharn"],
         ventana=True, x=.72, y=.42, entrada="pliegue"),
    mapa("eeuu_sur", [xy("Atlanta") + ("Atlanta", "inicio", None), xy("Chattanooga") + ("Chattanooga, Tennessee · 1899", "meta", None)],
         "dos empresarios de Chattanooga", ("en casi todo Estados Unidos|fin", .2), ["dos empresarios de Chattanooga"],
         ventana=True, x=.72, y=.42, entrada="foco"),
    mg(P.cifra(1, "$", titulo="LOS DERECHOS DE EMBOTELLAR · 1899", texto="$1"), ("les vendió esos derechos por un dólar", -.1),
       ("Con el tiempo, la compañía", -.1), y=.46, nombre="cifra 1 dolar"),
    et("LOS TUVO QUE RECOMPRAR", None, "tuvo que volver a comprar", dur=2.8),
    mg(P.cuenta(["LA COMPAÑÍA: EL CONCENTRADO", "LOS EMBOTELLADORES: TODO LO DEMÁS"], "EL MODELO DESDE 1899", titulo="EL TRATO"),
       ("de ese trato nació el modelo", -.1), ("hacen todo lo demás|fin", 1.0), ["Coca-Cola hace el concentrado", "y los embotelladores"],
       x=.68, y=.40, nombre="cuenta trato"),
    pant("patente_1915", ("En 1915 se patentó", -.1), ("fue una vaina de cacao", -.1), zoom=(1.0, 1.12)),
    pv("fue una vaina de cacao", "vaina_cacao", "Vaina de cacao", dur=2.4, x=.76, y=.52, tam=460),
    mapa("mexico", [xy("Monterrey") + ("Monterrey · Manuel Barragán", "inicio", os.path.join(_PEG, "barragan.png")),
                    xy("Tampico") + ("Tampico · Herman Fleishman", "meta", None)],
         ("Y en 1926 la Coca-Cola llegó a México", -.1), ("y para Herman Fleishman en Tampico|fin", .5),
         ["Manuel Barragán en Monterrey", "Herman Fleishman en Tampico"], titulo="1926 · Llega a México",
         sub="Las primeras concesiones para embotellarla", ajuste=.8),
    pv("nació con los años Arca Continental", "arca_logo", "Arca Continental", dur=4.0, x=.78, y=.55, tam=440),
    et("N.º 2 DE LAS AMÉRICAS", "embotellador de Coca-Cola", "hoy el segundo embotellador", dur=3.0, x=.34),
    pv("la Cervecería Cuauhtémoc", "cerveceria_cuauhtemoc", "Cervecería Cuauhtémoc · grabado de época", dur=4.6, x=.74, y=.50, tam=540),
    et("1979", "compra embotelladoras en la CDMX", "En 1979 compró", dur=3.0, x=.30),
    pv("De ahí salió Coca-Cola FEMSA", "kof_logo", "Coca-Cola FEMSA", dur=3.6, x=.78, y=.55, tam=420),
    et("N.º 1 DEL MUNDO", "embotellador de Coca-Cola por volumen", "Hoy FEMSA es el embotellador", dur=3.4),
    pv("Una cervecería de Monterrey terminó", "femsa_logo", "FEMSA", dur=3.8, x=.20, y=.60),

    # ---------------------------------------------------------------- suscripción
    pv("en Mil por Minuto desarmamos", "logo_mpm", "Mil por Minuto", dur=4.4, x=.50, y=.50, tam=520),
    mg(P.etiqueta("SUSCRÍBETE", "es gratis"), "suscríbete. Es gratis", ("todavía no lo está|fin", .3), x=.50, y=.78,
       nombre="etiqueta suscribete"),

    # ---------------------------------------------------------------- la planta: 10 estaciones
    *est(1, "Concentrado", "Estación uno: el concentrado", "Lo hace la compañía; la fórmula no sale de sus manos"),
    pv("Se lo vende The Coca-Cola Company", "tccc_logo", "El único proveedor", dur=3.6, x=.78, y=.55),
    pant("boveda", ("ochenta y seis años guardada", -.2), ("dentro del museo de la marca|fin", .4), zoom=(1.0, 1.14), pan=(0, 0, .05, 0)),
    mg(P.linea_tiempo("LA FÓRMULA SECRETA", [("1919", "Garantía de un préstamo"), ("1925-2011", "Bóveda de un banco"),
                                             ("2011", "Bóveda del museo, Atlanta")]),
       ("En 1919 sirvió de garantía", -.1), ("dentro del museo de la marca|fin", .4),
       ["En 1919 sirvió de garantía", "y en 2011 se mudó", "dentro del museo de la marca"], y=.74, nombre="linea formula"),
    pv("dentro del museo de la marca", "world_of_coca_cola", "World of Coca-Cola · Atlanta", dur=3.6, x=.78, y=.40, tam=420),
    et("¿SOLO 2 PERSONAS?", "nunca viajan juntas", "solo dos personas conocen", dur=3.2),
    et("LA LEYENDA VENDE", None, "Pero la leyenda también vende", dur=2.2),
    *est(2, "Agua", "Estación dos: el agua", "Casi toda la bebida es agua"),
    et("POZOS PROPIOS", "con permiso del gobierno", "de pozos propios", dur=3.0),
    mg(P.cuenta(["FILTRAR", "PULIR", "ÓSMOSIS INVERSA (PLANTAS NUEVAS)"], "AGUA TRATADA", titulo="ANTES DE USARLA"),
       ("se filtra, se pule", -.2), ("pasa por ósmosis inversa|fin", .8), ["se filtra", "se pule", "pasa por ósmosis inversa"],
       x=.70, y=.40, nombre="cuenta agua"),
    mapa("mexico", [xy("Toluca") + ("Toluca", "inicio", None), xy("Mérida") + ("Mérida", "meta", None)],
         "una Coca de Toluca", ("La bebida no puede serlo|fin", .3), ["una Coca de Toluca", "una de Mérida"],
         ventana=True, x=.72, y=.40, entrada="mesa"),
    mg(P.cifra(1.35, "", " L", "DE AGUA POR LITRO DE BEBIDA · COCA-COLA FEMSA, 2025", decimales=2, texto="1.35 L"),
       ("un litro con treinta y cinco", -.2), ("En 2018 usaba casi", -.1), y=.46, nombre="cifra agua"),
    et("2018: CASI 15 % MÁS", None, "En 2018 usaba casi", dur=3.0),
    *est(3, "Jarabe", "Estación tres: el jarabe", "Azúcar, agua y concentrado, en ese orden"),
    mg(P.cuenta(["AZÚCAR + AGUA TRATADA = JARABE SIMPLE", "+ CONCENTRADO = JARABE TERMINADO", "+ AGUA TRATADA = COCA-COLA SIN GAS"],
                "SIEMPRE LA MISMA PROPORCIÓN", titulo="EL JARABE"),
       ("Primero se disuelve el azúcar", -.1), ("todavía sin gas|fin", .8),
       ["Primero se disuelve el azúcar", "Luego se le agrega el concentrado", "Ese jarabe se mezcla"], x=.66, y=.42, nombre="cuenta jarabe"),
    *est(4, "Botella", "Estación cuatro: la botella", "Llega como preforma: se sopla aquí"),
    et("UN TRUCO", "casi nadie lo conoce", "un truco que casi nadie conoce", dur=2.4),
    pv("una preforma, un tubito grueso", "preforma", "Preforma de PET", dur=4.6, x=.76, y=.50, tam=560),
    tres_d("soplado", ("La preforma se calienta", -.1), ("el tubito se vuelve botella|fin", .4)),
    mg(P.cuenta(["CALENTAR", "ESTIRAR CON UNA VARILLA", "INFLAR CONTRA EL MOLDE"], "UNA FRACCIÓN DE SEGUNDO", titulo="SOPLADO"),
       ("La preforma se calienta", -.1), ("el tubito se vuelve botella|fin", .4),
       ["La preforma se calienta", "una varilla la estira", "y aire a presión la infla"], x=.27, y=.28, nombre="cuenta soplado"),
    et("MÁS RESISTENTE", "plástico estirado en dos direcciones", "se vuelve más resistente", dur=3.0),
    et("TOLUCA: TODO EN UNA MÁQUINA", "sopla, llena y etiqueta", "En la planta de Toluca, una sola", dur=3.4),
    *est(5, "Retornables", "Estación cinco: las retornables", "Vuelven, se lavan y se revisan una por una"),
    pv("Una de plástico retornable", "retornable_pet", "Plástico: 20 a 25 usos", dur=6.0, x=.25, y=.55, tam=480),
    pv("Una de vidrio", "retornable_vidrio", "Vidrio: 35 a 50 usos", dur=4.0, x=.75, y=.55, tam=480),

    # ---------------------------------------------------------------- trivia
    mg(P.trivia("¿Qué es más ácido?", ["A · La Coca-Cola", "B · El jugo de limón", "C · Son igual de ácidos"]),
       ("¿Qué es más ácido", -.1), ("Déjalo en los comentarios|fin", .8),
       ["la Coca-Cola?", "el jugo de limón?", "son igual de ácidos?"], y=.48, nombre="trivia pregunta"),

    # ---------------------------------------------------------------- estaciones 6-10
    *est(6, "Gas", "Estación seis: el gas", "Primero se enfría, luego recibe el CO2"),
    et("FRÍA = MÁS GAS", "tibia = espuma", "Porque el agua fría atrapa", dur=3.6),
    *est(7, "Llenado", "Estación siete: el llenado", "La máquina más impresionante de la planta", dur_card=3.0),
    tres_d("general", ("Es un carrusel", -.1), ("su propia válvula|fin", .3)),
    tres_d("valvulas", ("Antes de que caiga una sola gota", -.1), ("la rueda da media vuelta|fin", .3)),
    et("CONTRAPRESIÓN", "gas a presión antes del líquido", "Se llama llenado a contrapresión", dur=3.0, y=.20),
    mg(P.cifra(40000, titulo="BOTELLAS POR HORA · UNA LÍNEA EN TOLUCA", texto="40,000 POR HORA"), ("una sola línea llena", -.1),
       ("Y la de latas", -.1), y=.46, nombre="cifra 40000"),
    mg(P.cifra(1800, titulo="LATAS POR MINUTO · TOLUCA", texto="1,800 POR MINUTO"), ("Y la de latas", -.1),
       ("mil ochocientas por minuto|fin", 1.0), y=.46, nombre="cifra 1800"),
    *est(8, "Tapa", "Estación ocho: la tapa", "Antes de que se escape el gas"),
    tres_d("tapadora", ("Apenas sale del carrusel", -.1), ("tiempo de escapar|fin", .3)),
    *est(9, "Revisión", "Estación nueve: la revisión", "Nivel, tapa, código y etiqueta"),
    tres_d("etiquetadora", ("Se revisa el nivel", -.1), ("se va de la línea|fin", .2)),
    mg(P.cuenta(["NIVEL", "TAPA", "CÓDIGO DEL LOTE"], "LA QUE SALE MAL, FUERA DE LA LÍNEA", titulo="REVISIÓN"),
       ("Se revisa el nivel", -.1), ("se va de la línea|fin", .4), ["Se revisa el nivel", "la tapa y", "el código del lote"],
       x=.27, y=.28, nombre="cuenta revision"),
    tarjeta(("En el laboratorio de Toluca", 2.6), "scene-070:fin"),
    mg(P.cifra(40, titulo="CATADORES POR TURNO · LABORATORIO DE TOLUCA", texto="40 CATADORES"), ("En el laboratorio de Toluca", -.1),
       ("como debe saber|fin", .3), y=.46, nombre="cifra catadores"),
    *est(10, "Tarimas", "Estación diez: las tarimas", "Paquetes, tarimas y camiones", dur_card=3.0),
    mg(P.cuenta(["BOTELLAS A PAQUETES", "PAQUETES A TARIMAS", "TARIMAS A LOS CAMIONES"], "TOLUCA: ~700,000 CAJAS AL DÍA",
                titulo="LA SALIDA"),
       ("Las botellas se agrupan en paquetes", -.1), ("setecientas mil cajas al día|fin", .8),
       ["se agrupan en paquetes", "los paquetes en tarimas", "y las tarimas suben", "setecientas mil cajas"],
       x=.70, y=.40, nombre="cuenta salida"),
    pv("Toluca, una de las plantas más grandes", "toluca_planta", "Planta Toluca · Coca-Cola FEMSA", dur=4.6, x=.26, y=.40, tam=520),

    # ---------------------------------------------------------------- el negocio
    mg(P.etiqueta("EL NEGOCIO"), "Ahora, el negocio", ("Venderla en cada esquina es otra|fin", .2), x=.50, y=.82, nombre="etiqueta negocio"),
    mg(P.cuenta(["LO QUE PAGAS EN LA TIENDA", "POR UN PORCENTAJE", "= PRECIO DEL CONCENTRADO"], "MÉXICO: SUBIÓ EN 2021 Y EN 2022",
                titulo="CÓMO SE COBRA EL CONCENTRADO"),
       ("Su precio no es fijo", -.1), ("otra vez en 2022|fin", .8),
       ["La compañía lo cobra", "Si la Coca sube de precio", "ese porcentaje subió"], x=.66, y=.40, nombre="cuenta concentrado"),
    mg(P.cuenta(["LA COMPAÑÍA: MARCA Y FÓRMULA", "EL EMBOTELLADOR: FÁBRICAS, CAMIONES, POZOS Y REFRIGERADORES"], "UN NEGOCIO MUY ELEGANTE",
                titulo="QUIÉN PONE QUÉ"),
       ("Es un negocio muy elegante", -.1), ("los pone el embotellador|fin", .6), ["la compañía cuida la marca", "Las fábricas, los camiones"],
       x=.62, y=.40, nombre="cuenta quien"),
    mg(P.cuenta(["8 GRUPOS EMBOTELLADORES", "73 PLANTAS", "+13,000 RUTAS DE REPARTO"], "INDUSTRIA MEXICANA DE COCA-COLA · 2026",
                titulo="EN MÉXICO"),
       ("En México hay ocho grupos", -.1), ("trece mil rutas de reparto|fin", .8),
       ["ocho grupos embotelladores", "setenta y tres plantas", "trece mil rutas"], x=.68, y=.40, nombre="cuenta mexico"),
    pv("Es la tiendita", "tiendita", "La tiendita", dur=4.0, x=.76, y=.52, tam=500),
    et("CANAL TRADICIONAL", "la tienda de la esquina", "por el canal tradicional", dur=3.0),
    mg(P.cifra(1200000, titulo="PEQUEÑOS COMERCIOS · SEGÚN EL SISTEMA", texto="+1.2 MILLONES"), ("más de un millón doscientos mil", -.2),
       ("pequeños comercios en todo el país|fin", .6), y=.46, nombre="cifra comercios"),
    mg(P.cifra(136193, "$", titulo="MILLONES DE PESOS · COCA-COLA FEMSA MÉXICO, 2025", texto="$136,193 MILLONES"),
       ("facturó ciento treinta y seis mil", -.2), ("Y México pesa", -.1), y=.46, nombre="cifra pesos"),
    mg(P.barras("VOLUMEN DE COCA-COLA EN AMÉRICA LATINA · 2025", [("México", 43), ("Resto de la región", 57)], "%", decimales=0),
       ("es más del cuarenta por ciento", -.1), ("Tanto, que en febrero", -.1), ["es más del cuarenta por ciento"], y=.46,
       nombre="barras latam"),
    mg(P.cifra(6000, "$", titulo="MILLONES DE DÓLARES · INVERSIÓN ANUNCIADA, FEB-2026", texto="$6,000 MILLONES"),
       ("una inversión de seis mil millones", -.2), ("Pero ojo", -.1), y=.46, nombre="cifra 6000"),
    mg(P.cifra(5.2, "-", "%", "VOLUMEN DE COCA-COLA FEMSA EN MÉXICO · 2025 CONTRA 2024", decimales=1, texto="-5.2 %"),
       ("vendió en México cinco por ciento menos", -.1), ("otro golpe", -.1), y=.46, nombre="cifra caida"),
    et("2026: IMPUESTOS", None, "le esperaba otro golpe", dur=3.0),

    # ---------------------------------------------------------------- mitos
    et("MITOS VS. DATOS", None, "llegaron los mitos y las polémicas", dur=3.4),
    et("MITO 1", "¿lleva cocaína?", "Primero: ¿la Coca-Cola lleva cocaína", dur=2.8, x=.30),
    pv("un extracto de hoja de coca", "hoja_coca", "Hoja de coca", dur=4.0, x=.78, y=.52, tam=440),
    mg(P.linea_tiempo("LA HOJA DE COCA", [("1886", "Extracto con cocaína"), ("1903", "Hoja sin cocaína"), ("HACIA 1929", "Ni rastro")]),
       ("La receta original usaba", -.1), ("ya no quedaba ni rastro|fin", .8),
       ["La receta original usaba", "A partir de 1903", "hacia 1929"], y=.30, nombre="linea coca"),
    et("MITO 2", "¿era verde?", "Segundo: ¿la Coca-Cola era verde", dur=2.8, x=.30),
    et("SIEMPRE FUE CAFÉ", "lo verde era el vidrio", "Siempre fue café", dur=3.4),
    et("MITO 3", "¿disuelve un clavo?", "Tercero: ¿disuelve un clavo", dur=2.8, x=.30),
    pv("le quita el óxido", "clavo_oxidado", "Ácido fosfórico: quita el óxido", dur=4.4, x=.74, y=.50, tam=580),
    et("ENTERO", "no lo disuelve", "Pero entero", dur=2.2),
    et("MITO 4", "¿azúcar de caña?", "Cuarto: ¿la Coca mexicana", dur=2.8, x=.30),
    mg(P.ingredientes(["Agua carbonatada", "Azúcares añadidos (azúcar y jarabe de alta fructosa)", "Caramelo clase IV", "Ácido fosfórico",
                       "Saborizantes", "Cafeína"], resalta=(1,), titulo="ETIQUETA · COCA-COLA MÉXICO"),
       ("La que se vende en México lleva", -.1), ("Lo dice la etiqueta", -.1), ["azúcar y jarabe de alta fructosa"],
       x=.50, y=.42, nombre="ingredientes"),
    pv("Lo dice la etiqueta", "etiqueta_mx", "Etiqueta de México", dur=3.8, x=.80, y=.50, tam=520),
    pv("La famosa Coca mexicana de vidrio", "mexican_coke", "«Mexican Coke» · EE.UU.", dur=4.6, x=.76, y=.52, tam=480),
    et("JULIO 2025", "versión extra con caña en EE.UU.", "la compañía anunció allá", dur=3.2),
    et("MITO 5", "los impuestos", "Quinto, los impuestos", dur=2.4, x=.30),
    mg(P.cifra(1, "$", titulo="POR LITRO · IMPUESTO A BEBIDAS AZUCARADAS, 2014", texto="$1 POR LITRO"),
       ("México le puso un peso por litro", -.2), ("las compras bajaron seis", -.2), y=.46, nombre="cifra impuesto 2014"),
    mg(P.barras("CAÍDA EN COMPRAS DE BEBIDAS CON IMPUESTO · 2014", [("Promedio", 6), ("Hogares de menos ingresos", 9)], "%",
                decimales=0, resalta=1),
       ("las compras bajaron seis", -.2), ("En 2026, el impuesto", -.1), ["las compras bajaron seis", "en los hogares de menos ingresos"],
       y=.46, nombre="barras impuesto"),
    mg(P.cifra(3.08, "$", titulo="POR LITRO · IMPUESTO 2026 (ANTES $1.65)", decimales=2, desde=1.65, texto="$3.08 POR LITRO"),
       ("el impuesto casi se duplicó", -.1), ("Y desde octubre de 2020", -.1), y=.46, nombre="cifra impuesto 2026"),
    pv("los sellos negros de advertencia", "sellos_600", "Coca-Cola 600 ml · México", dur=5.4, x=.76, y=.50, tam=560, marco="museo"),
    et("CONTIENE CAFEÍNA", "evitar en niños", "contiene cafeína, evitar en niños", dur=3.0, x=.34),
    et("MITO 6", "el agua", "Y sexto, el agua", dur=2.4, x=.30),
    mapa("mexico", [xy("San Cristóbal") + ("San Cristóbal de las Casas · desde 1994", "meta", None)],
         "En San Cristóbal de las Casas, en Chiapas", ("una planta embotelladora desde 1994|fin", .4),
         ["En San Cristóbal de las Casas"], ventana=True, x=.30, y=.40, entrada="foco"),
    et("AGUA UNAS HORAS CADA 2 DÍAS", "algunos vecinos", "reciben agua unas horas", dur=3.2),
    mg(P.cifra(1.23, "", " %", "DEL AGUA DISPONIBLE DEL ACUÍFERO · PERMISO DE LA PLANTA", decimales=2, texto="1.23 %"),
       ("menos del uno y medio por ciento", -.2), ("está en la red de la ciudad|fin", .4), y=.46, nombre="cifra acuifero"),
    mg(P.cuenta(["LA AUTORIDAD: PERMISO PARA EL 1.23 %; LA FALLA ES LA RED", "LOS CRÍTICOS: SACA MÁS DE LO PERMITIDO"], "LAS DOS VERSIONES SIGUEN",
                titulo="SAN CRISTÓBAL"),
       ("Los críticos acusan", -.1), ("y la planta, también|fin", .6), ["Los críticos acusan", "Las dos versiones"],
       x=.62, y=.40, nombre="cuenta versiones"),

    # ---------------------------------------------------------------- mapa completo
    mapa("mexico", [xy("Monterrey") + ("Monterrey · 1926 y 1890", "inicio", os.path.join(_PEG, "cerveceria_cuauhtemoc.png")),
                    xy("Tampico") + ("Tampico y Altamira · La Pureza", "paso", None),
                    xy("Toluca") + ("Toluca · planta y PetStar", "paso", os.path.join(_PEG, "petstar.png")),
                    xy("Apizaco") + ("Apizaco", "paso", None), xy("León") + ("León", "paso", None),
                    xy("Morelia") + ("Morelia", "paso", None), xy("San Cristóbal") + ("San Cristóbal", "paso", None),
                    xy("Valladolid") + ("Valladolid · 2026", "meta", os.path.join(_PEG, "valladolid.png"))],
         ("Hagamos el mapa completo", -.1), ("Solo para botellas retornables|fin", .5),
         ["En Nuevo León, Monterrey", "En Tamaulipas, Tampico", "En el Estado de México, Toluca", "En Tlaxcala, Apizaco",
          "En Guanajuato, León", "En Michoacán, Morelia", "En Chiapas, San Cristóbal", "Y en Yucatán, Valladolid"],
         titulo="Dónde se hace la Coca-Cola", sub="Algunas plantas del sistema en México", ajuste=.7, entrada="desenrolla"),
    mg(P.cifra(120000, titulo="TONELADAS DE PET AL AÑO · PETSTAR, TOLUCA", texto="+120,000 T", w=900, h=300),
       ("Procesa más de ciento veinte mil", -.1), ("toneladas al año|fin", .8), x=.26, y=.86, nombre="cifra petstar"),
    et("LA PRIMERA EN +20 AÑOS", "solo botellas retornables", "la primera planta nueva de refrescos", dur=3.6, x=.25, y=.88),
    pv("a una tiendita en cualquier esquina", "tiendita", "La tiendita", dur=3.6, x=.76, y=.52, tam=480),

    # ---------------------------------------------------------------- cierre
    plano(None, ("piensa en todo lo que pasó", -.1), ("Y un carrusel que no se detiene|fin", .5),
          marcas=["piensa en todo lo que pasó", "Una fórmula en una bóveda", "Agua de pozo tratada", ("Agua de pozo tratada", .7),
                  "Una preforma que se infló", ("Una preforma que se infló", 1.0), "Gas que solo entra", "Y un carrusel",
                  ("Y un carrusel", .7), ("Y un carrusel", 1.3)], sub="Del pozo al camión"),
    mg(P.trivia("¿Qué es más ácido?", ["A · La Coca-Cola", "B · El jugo de limón", "C · Son igual de ácidos"], correcta=1,
                cabecera="TRIVIA · LA RESPUESTA"),
       ("La respuesta de la trivia", -.1), ("El jugo de limón es un poquito", -.1),
       [("La respuesta de la trivia", 0), ("La respuesta de la trivia", .15), ("La respuesta de la trivia", .3), "la B."],
       y=.48, nombre="trivia respuesta"),
    mg(P.barras("pH: MÁS BAJO, MÁS ÁCIDO", [("Jugo de limón", 2.25), ("Coca-Cola", 2.37)], "", decimales=2, resalta=0),
       ("El jugo de limón es un poquito", -.1), ("el limón también lo haría|fin", .4), ["El jugo de limón es un poquito"],
       y=.46, nombre="barras ph"),
    pv("El jugo de limón es un poquito", "limon", "Limón", dur=3.6, x=.17, y=.62),
    mg(P.etiqueta("MÁS DE 250,000", "botellas y latas mientras veías"), "Y el contador de la esquina", ("scene-117:fin", .3),
       x=.62, y=.26, nombre="etiqueta contador final"),
    mg(P.etiqueta("¿QUÉ MARCA SIGUE?", "dímelo en los comentarios"), "dime cuál en los comentarios", ("scene-118:fin", .2),
       x=.50, y=.26, nombre="etiqueta siguiente"),
    pv("Y suscríbete a Mil por Minuto", "logo_mpm", "Suscríbete", dur=5.0, x=.50, y=.48, tam=520),

    # ---------------------------------------------------------------- huecos de > 4 s (fx --seco, 24-nov)
    pv("Una etiqueta roja", "coca_logo", "La etiqueta roja", dur=3.0, x=.22, y=.30, tam=460),
    et("MAYO DE 1886", "una farmacia de Atlanta", "En mayo de 1886", dur=3.6, x=.34, y=.24),
    et("LA DECISIÓN", "que todavía mueve el negocio", "la decisión que todavía mueve", dur=3.6),
    et("MONTERREY · 1890", "otra empresa", "Y en Monterrey había otra empresa", dur=3.6),
    pv("la marca más famosa del planeta", "coca_logo", "La marca más famosa", dur=3.8, x=.76, y=.50, tam=520),
    et("¿QUÉ HAY DETRÁS?", None, "Si te gusta saber", dur=3.0),
    et("CASI TODA AGUA", None, "una Coca-Cola es casi toda agua", dur=3.0),
    et("NO LLEGA COMO BOTELLA", None, "no llega a la planta como botella", dur=3.4),
    mg(P.cuenta(["VUELVEN A LA PLANTA", "SE LAVAN POR DENTRO Y POR FUERA", "SE REVISAN UNA POR UNA"], "BOTELLAS RETORNABLES",
                titulo="EL REGRESO"),
       ("que regresas a la tienda", -.1), ("se revisan una por una|fin", .8),
       ["vuelven a la planta", "se lavan por dentro", "se revisan una por una"], x=.68, y=.40, nombre="cuenta retornables"),
    et("TIBIA: ESPUMA", None, "Si estuviera tibia", dur=3.6, y=.78),
    pv("Con una bebida tan famosa", "botella_contour", "Coca-Cola", dur=3.6, x=.78, y=.52, tam=440),
    et("CON CAÑA", "la de vidrio que se vende en EE.UU.", "esa sí va con caña", dur=3.4),
    pv("la próxima vez que le quites", "botella_contour", "Coca-Cola", dur=3.8, x=.78, y=.52, tam=460),
] + _REF

FX = [f for f in FX if f]

ROTULOS = []
SFX = {
    "destapar": ("Opening a glass soda bottle: metal cap pops off, then a crisp carbonation fizz hiss, close and clean", 3),
    "golpe_metal": ("Heavy industrial metal clank, a factory press stamping once, short", 2),
    "maquina": ("Bottling plant ambience, glass bottles clinking on conveyor belts and machines humming, steady loop", 10),
    "gas": ("Soda being poured into a glass, fizzing carbonation bubbles, close", 4),
    "caja": ("Cash register ka-ching, bright and short", 2),
    "sello": ("Rubber stamp hitting paper hard, single thud", 1),
}
PISTAS = [dict(sfx="destapar", en="ese chasquido del gas", vol=.55), dict(sfx="destapar", en="le quites la tapa a una Coca", vol=.40)]
PISTAS += [dict(sfx="golpe_metal", en=f"Estación {n}", vol=.45) for n in
           ("uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez")]
PISTAS += [dict(sfx="maquina", de="Estación uno: el concentrado", a=("Vamos con una pregunta", -.3), vol=.10),
           dict(sfx="maquina", de="Estación seis: el gas", a=("Ahora, el negocio", -.3), vol=.10),
           dict(sfx="gas", en="La bebida se enfría antes de recibir", vol=.30),
           dict(sfx="caja", en="dos mil trescientos dólares", vol=.30), dict(sfx="caja", en="por un dólar", vol=.30),
           dict(sfx="caja", en="facturó ciento treinta y seis mil", vol=.28), dict(sfx="caja", en="una inversión de seis mil millones", vol=.28),
           dict(sfx="sello", en="Hoy no. La receta", vol=.40), dict(sfx="sello", en="Siempre fue café", vol=.40),
           dict(sfx="sello", en="Pero entero", vol=.40)]
