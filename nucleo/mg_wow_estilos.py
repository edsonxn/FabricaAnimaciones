# -*- coding: utf-8 -*-
"""KIT DE 4 ESTILOS de Crónicas de Warcraft (22-nov-2026, decisión del usuario): cada video de Warcraft COMBINA el estilo
original del kit (mg_wow / peg_estilos / peg_anim, azul noche y oro) con tres estilos nuevos, repartidos por el video:
  original   lo de siempre: mg_wow.ruta (mapa), panel azul noche y borde dorado (ficha y rótulo), peg_estilos.reliquia
             (tarjeta), peg_anim.variado (pegatina)
  pergamino  CARTÓGRAFO DE PERGAMINO: pergamino quemado, tinta sepia, Corsiva, sellos de lacre, ruta de pluma, fotos pegadas
  oro        RELIQUIA DE ORO Y PIEDRA: piedra tallada, molduras de oro, gemas engastadas, cadena de runas, polvo dorado
  madera     MADERA Y PERGAMINO (25-nov; sustituye al holograma arcano): mismas animaciones con madera, pergamino y oro
Demos de 30 s y hojas: videos/_kit_wow_estilos/estilo_1 (pergamino), estilo_2 (oro), estilo_3 (holograma); prueba de la
mezcla: videos/_kit_wow_estilos/prueba_mezcla/ (hoja_mezcla.jpg). Motores: nucleo/wow_estilos/. Doc: docs/estilo_secuencia_yt.md
§ «KIT DE 4 ESTILOS (22-nov-2026)».

PIEZAS (todas devuelven fn(dt, dur, marcas) -> BGRA, la firma de los FX `mg`/`pantalla` de nucleo/secuencia_fx.py):
  mapa(estilo, imagen_mapa, puntos, titulo=None, sub=None, zmin=1.0, zmax=1.5, objeto=None)
        cuadro entero (FX `pantalla`). puntos = [(x %, y %, rótulo, subrótulo|None, foto|None), ...] como mg_wow.ruta y
        `_coords.md`; el paso k entra en la marca k y la ruta va del paso k-1 al k; la cámara encuadra los pasos vistos;
        la foto de cada paso se va cuando entra el siguiente (la del último se queda). objeto = ícono de Wowhead del premio.
  ficha(estilo, titulo, iconos, cuentas=None, total=None, etiquetas=None, colores=None)
        cuadro sobre el gameplay: el ícono k entra en la marca k con su etiqueta («×15» por defecto si hay cuentas) y el
        contador sube con el acumulado hasta `total`. iconos = rutas, slugs de pegatina, «ico:<Wowhead>» o nombre Wowhead.
  tarjeta(estilo, imagen, titulo, subtitulo=None, tam=500, **extra)
        tarjeta de jefe/objeto/personaje (holograma: pie=, fases=N barra de vida; oro: elementos=[colores]; pergamino: letra=)
  rotulo(estilo, texto, sello=None)        rótulo inferior; sello = cifra o letra corta («5», «!») o None
  pegatina(estilo, imagen, titulo=None, tam=400, **anim)
        marco para pegatinas sueltas: original = peg_anim.variado (anim = entrada/estancia/salida/marco); pergamino = foto
        pegada con lacre; oro = relicario de oro; holograma = ficha de cristal translúcido con borde de neón.

CAMBIO DEL USUARIO (25-nov-2026, wow_ruta_profesiones): el «holograma» arcano (azul-violeta, neón) se salía del estilo
visual → ahora es «madera» (wow_estilos/madera.py: el MISMO motor y animaciones con piel de madera, pergamino y oro;
«holo», «holograma» y «arcano» llevan ahí). Los MAPAS van SIEMPRE con el mapa original sin teñir (ver mapa_e).
REPARTO (no pensarlo puesto a puesto): ESTILOS_WOW = ("original", "pergamino", "oro", "madera"). Con estilo=None cada
helper toma el SIGUIENTE estilo de su pieza en rotación (dos mapas seguidos nunca repiten estilo; cada pieza arranca
desfasada para que mapa, ficha, tarjeta y rótulo del mismo puesto no coincidan). estilo_para(indice_o_id, pieza) da el
estilo fijo de un puesto (int = número de puesto; str = id, en orden de aparición). El contador se reinicia solo cada vez
que el motor vuelve a cargar efectos.py (es determinista: mismo efectos.py = mismos estilos = el montaje no se rehace).

PLANTILLA (videos/<v>/efectos.py; los helpers buscan mapas/<nom>.jpg y pegatinas/<slug>.png junto a efectos.py):
    import mg_wow_estilos as E
    FX = [
        E.peg_e("Número quince. Entrar al Bancal", "bancal_creador", "Bancal del Creador"),          # pegatina
        E.mapa_e("ungoro_norte", [E.P(43.6, 23.9, "Refugio de los Mariscales", None, "refugio_mariscales"),
                                  E.P(47.3, 10.8, "Bancal del Creador", "mazmorra · 58-60", "bancal_creador")],
                 ("Es la otra mazmorra nueva", -.2), ("subiendo desde el Refugio|fin", .5),
                 ["un lugar de los titanes", "subiendo desde el Refugio"], "CRÁTER DE UN'GORO", "al norte del cráter"),
        E.ficha_e("N.º 15 · SIN LOS 60 CRISTALES", ["o_cristal_rojo", "o_cristal_amarillo", "o_cristal_azul",
                  "o_cristal_verde"], "Dentro hay cuatro consolas", ("te quedas en cinco jefes|fin", .6),
                  ["Rojo para Cinder", "Amarillo para Bolt", "Azul para Snowtalon", "Y el verde"], cuentas=[15] * 4),
        E.tarjeta_e("despierta la jefa final, Nanaya", "bancal_creador", "JEFA FINAL: NANAYA", "cambia de elemento cada 25 %"),
        E.rotulo_e("Sin los cristales", "Sin cristales: solo 5 jefes", sello="5"),
    ]
  Fijar un estilo: estilo="oro" (o estilo=E.estilo_para(15, "mapa")). Revisar SIEMPRE: FAB_FX_FINAL=1 python fab.py <v> fx hoja.
"""
import inspect
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from wow_estilos import comun as C

ESTILOS_WOW = ("original", "pergamino", "oro", "madera")
NUEVOS = ESTILOS_WOW[1:]
PIEZAS = ("mapa", "ficha", "tarjeta", "rotulo", "pegatina")
_DESFASE = dict(mapa=0, ficha=1, tarjeta=2, rotulo=3, pegatina=1)
_ALIAS = {"perg": "pergamino", "pergamino": "pergamino", "cartografo": "pergamino", "oro": "oro", "reliquia": "oro",
          "piedra": "oro", "holo": "madera", "holograma": "madera", "arcano": "madera", "madera": "madera", "original": "original",
          "clasico": "original"}


def _est(estilo):
    e = _ALIAS.get(str(estilo).lower())
    if e is None:
        raise ValueError(f"mg_wow_estilos: estilo «{estilo}» no existe; hay: {', '.join(ESTILOS_WOW)}")
    return e


def _motor(estilo):
    import importlib
    return importlib.import_module("wow_estilos." + estilo)


# ============================================================================ REPARTO
_rep = dict(dueno=None, cuenta={}, ids={})


def reinicia():
    """Vuelve a empezar la rotación (se hace solo al recargar efectos.py)."""
    _rep["cuenta"], _rep["ids"] = {}, {}


def _llamador():
    """Frame del primer llamador fuera de este módulo (efectos.py)."""
    f = inspect.currentframe()
    aqui = os.path.abspath(__file__)
    while f is not None and os.path.abspath(f.f_code.co_filename) == aqui:
        f = f.f_back
    return f


def _vigilar_dueno():
    f = _llamador()
    dueno = id(f.f_globals) if f is not None else None
    if dueno != _rep["dueno"]:                 # otro efectos.py (o el mismo recargado): reparto desde cero
        _rep["dueno"] = dueno
        reinicia()


def estilo_para(indice_o_id, pieza="mapa"):
    """Estilo fijo de un puesto: int = número de puesto (rota por los 4 con el desfase de la pieza); str = id (se le
    asigna el siguiente índice libre en orden de aparición)."""
    if pieza not in _DESFASE:
        raise ValueError(f"mg_wow_estilos: pieza «{pieza}»; hay: {', '.join(PIEZAS)}")
    if isinstance(indice_o_id, int):
        i = indice_o_id
    else:
        ids = _rep["ids"].setdefault(pieza, {})
        i = ids.setdefault(str(indice_o_id), len(ids))
    return ESTILOS_WOW[(i + _DESFASE[pieza]) % len(ESTILOS_WOW)]


def siguiente(pieza):
    """El siguiente estilo de esa pieza en la rotación equilibrada (nunca repite el de la anterior de la misma pieza)."""
    _vigilar_dueno()
    k = _rep["cuenta"].get(pieza, 0)
    _rep["cuenta"][pieza] = k + 1
    return estilo_para(k, pieza)


def resumen():
    """Cuántas piezas lleva cada pieza en la rotación (para el chequeo)."""
    return dict(_rep["cuenta"])


# ============================================================================ ORIGINAL (kit de siempre)
def _ficha_original(titulo, iconos, etiquetas, valores, total=None):
    """Panel azul noche con borde dorado (mg_wow._base), casillas de inventario con los íconos (marca k) y el contador
    que corre; el total sale en verde."""
    import mg_wow as M
    import mg_wow60 as W6
    n = len(iconos)
    t_cas, gap = 124, 46
    fnum = M.fuente("negra", 78)
    final = total if total is not None else sum(valores)
    dd = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    w_num = dd.textlength(f"= {final}", font=fnum) + 40
    ancho = int(max(dd.textlength(titulo, font=M.fuente("serif", 40)) + 360, n * (t_cas + gap) - gap + 120 + w_num + 40))
    h = 330 if any(etiquetas) else 290
    srcs = [s[4:] if str(s).startswith("ico:") else s for s in iconos]

    def fn(dt, dur, marcas):
        tk = C.tiempos(marcas, n, ini=.7, paso=.8, minimo=.3)
        im, Mg = M._base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0, y0 = Mg + 60, Mg + 96
        cuenta = 0.0
        for i in range(n):
            x = x0 + i * (t_cas + gap)
            u = dt - tk[i]
            d.rounded_rectangle((x, y0, x + t_cas, y0 + t_cas), 9, fill=(4, 6, 18, 235), outline=(95, 82, 45, 255), width=2)
            if u <= 0:
                continue
            M._pegar(im, W6._img(srcs[i], t_cas - 12), x + t_cas / 2, y0 + t_cas / 2, M._pop(u, .3))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((x, y0, x + t_cas, y0 + t_cas), 9, outline=M.ORO + (255,), width=3)
            if etiquetas[i]:
                M._texto(d, (x + t_cas / 2, y0 + t_cas + 30), etiquetas[i], M.fuente("negra", 30), M.BLANCO, "mm", 255 * M._eo(u / .3))
            cuenta += valores[i] * M._eo((u - .1) / .5)
        cuenta *= final / max(1e-6, sum(valores))
        tfin = tk[n - 1] + .6
        a = M._eo((dt - min(tk[0], 1.0)) / .3)
        col = M.VERDE if dt >= tfin else M.BLANCO
        M._texto(d, (Mg + ancho - 50, y0 + t_cas / 2), f"= {int(round(cuenta))}", fnum, col, "rm", 255 * a)
        return M._salida(im, dt)
    fn.ancho = ancho
    return fn


def _rotulo_original(texto, sello=None):
    """Rótulo inferior con el panel de mg_wow: azul noche, doble borde dorado, serif oro; sello de goma si hay cifra."""
    import mg_wow as M
    f = M.fuente("serif", 48)
    tw = ImageDraw.Draw(Image.new("RGBA", (8, 8))).textlength(texto, font=f)
    xs = 130 if sello else 0
    w, h, Mg = int(tw + 76 + xs), 100, 30
    base = Image.new("RGBA", (w + 2 * Mg, h + 2 * Mg + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((Mg + 6, Mg + 12, Mg + w + 4, Mg + h + 10), 14, fill=(0, 0, 0, 190))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle((Mg, Mg, Mg + w, Mg + h), 14, fill=(14, 19, 50, 240), outline=M.ORO + (255,), width=4)
    d.rounded_rectangle((Mg + 8, Mg + 8, Mg + w - 8, Mg + h - 8), 9, outline=M.ORO + (70,), width=1)
    M._texto(d, (Mg + 38 + xs, Mg + h / 2), texto, f, M.ORO_T, "lm")

    def fn(dt, dur, marcas):
        u = M._eo(dt / .45)
        if u <= 0:
            return C.VACIO
        im = Image.new("RGBA", base.size, (0, 0, 0, 0))
        vis = base.crop((0, 0, max(2, int(base.width * u)), base.height))
        im.alpha_composite(vis, (0, 0))
        if sello:
            M._sello(im, str(sello), Mg + 70, Mg + h / 2, dt - .25, (235, 60, 50), 44, ang=-8)
        sal = M._eo((dur - dt) / .35)
        if sal < 1:
            im.putalpha(im.getchannel("A").point(lambda v: int(v * sal)))
        return np.array(im)[..., [2, 1, 0, 3]].copy()
    fn.ancho, fn.izq = base.width, Mg
    return fn


# ============================================================================ PIEZAS (las 4 versiones)
def _firmar(fn, *datos):
    """Envuelve fn para que la firma del montaje (secuencia_fx._sig: lee las variables del closure) incluya los DATOS de la
    pieza (rutas con su fecha, textos, puntos): si cambian, su tramo se rehace; si no, se reutiliza."""
    def pieza(dt, dur, marcas):
        _ = datos                    # en el closure: _sig lo lee
        return fn(dt, dur, marcas)
    pieza.ancho, pieza.izq = getattr(fn, "ancho", None), getattr(fn, "izq", 0)
    pieza.datos = datos
    return pieza


def mapa(estilo, imagen_mapa, puntos, titulo=None, sub=None, zmin=1.0, zmax=1.5, objeto=None, variante=0):
    return _firmar(_mapa(estilo, imagen_mapa, puntos, titulo, sub, zmin, zmax, objeto, variante),
                   "mapa", _est(estilo), imagen_mapa, list(puntos), titulo, sub, zmin, zmax, objeto, variante)


def _mapa(estilo, imagen_mapa, puntos, titulo, sub, zmin, zmax, objeto, variante=0):
    e = _est(estilo)
    if e == "original":
        import mg_wow as M
        return M.ruta(imagen_mapa, puntos, titulo, sub, zmax=zmax, zmin=zmin, objeto=objeto, variante=variante)
    return _motor(e).Mapa(imagen_mapa, puntos, titulo, sub, zmin=zmin, zmax=zmax, objeto=objeto).fn()


def _norm_icono(s):
    """Ruta existente, «ico:<nombre>» o nombre de ícono de Wowhead (sin extensión) -> forma que entienden los motores."""
    s = str(s)
    if s.startswith("ico:") or os.path.exists(s):
        return s
    return "ico:" + s


def ficha(estilo, titulo, iconos, cuentas=None, total=None, etiquetas=None, colores=None):
    return _firmar(_ficha(estilo, titulo, iconos, cuentas, total, etiquetas, colores),
                   "ficha", _est(estilo), titulo, list(iconos), cuentas, total, etiquetas, colores)


def _ficha(estilo, titulo, iconos, cuentas, total, etiquetas, colores):
    e = _est(estilo)
    iconos = [_norm_icono(i) for i in iconos]
    n = len(iconos)
    valores = list(cuentas) if cuentas else [1] * n
    if etiquetas is None:
        etiquetas = [f"×{v}" for v in valores] if cuentas else [None] * n
    if e == "original":
        return _ficha_original(titulo, iconos, etiquetas, valores, total)
    m = _motor(e)
    if e == "pergamino":
        return m.Ficha(titulo, iconos, etiquetas, valores, total).fn()
    return m.Ficha(titulo, iconos, etiquetas, valores, total, colores=colores).fn()


def tarjeta(estilo, imagen, titulo, subtitulo=None, tam=500, **extra):
    return _firmar(_tarjeta(estilo, imagen, titulo, subtitulo, tam, **extra),
                   "tarjeta", _est(estilo), imagen, titulo, subtitulo, tam, extra)


def _tarjeta(estilo, imagen, titulo, subtitulo, tam, **extra):
    e = _est(estilo)
    if e == "original":
        import peg_estilos as PE
        if C.es_icono(imagen):
            tam = min(tam, 340)
        return PE.reliquia(imagen, titulo, subtitulo, tam, tema="wow")
    m = _motor(e)
    if e == "pergamino":
        return m.Tarjeta(imagen, titulo, subtitulo, letra=extra.get("letra"), ancho=extra.get("ancho", 600)).fn()
    if e == "oro":
        return m.Tarjeta(imagen, titulo, subtitulo, elementos=extra.get("elementos")).fn()
    return m.Tarjeta(imagen, titulo, subtitulo, pie=extra.get("pie"), fases=extra.get("fases"), ancho=extra.get("ancho", 640)).fn()


def rotulo(estilo, texto, sello=None):
    return _firmar(_rotulo(estilo, texto, sello), "rotulo", _est(estilo), texto, sello)


def _rotulo(estilo, texto, sello):
    e = _est(estilo)
    if e == "original":
        return _rotulo_original(texto, sello)
    m = _motor(e)
    if e == "pergamino":
        r = m.Rotulo(texto, sello)
        fn = r.fn()
        fn.ancho, fn.izq = r.w + 2 * r.MG, (r.MG - 4 if sello else r.MG)
    elif e == "oro":
        r = m.Rotulo(texto, sello)
        fn = r.fn()
        fn.ancho, fn.izq = r.CW, r.pos[0] - 86
    else:
        r = m.Rotulo(texto, sello)
        fn = r.fn()
        fn.ancho, fn.izq = r.CW, r.x
    return fn


_MARCOS_ICONO = ("polaroid", "carta", "estampilla", "naipe", "museo", "clasico")


def pegatina(estilo, imagen, titulo=None, tam=400, **anim):
    e = _est(estilo)
    if e == "original":            # peg_anim ya firma con sus propios datos (y el rotador del video)
        return _pegatina(e, imagen, titulo, tam, **anim)
    return _firmar(_pegatina(e, imagen, titulo, tam, **anim), "pegatina", e, imagen, titulo, tam)


def _pegatina(estilo, imagen, titulo, tam, **anim):
    e = _est(estilo)
    if C.es_icono(imagen):
        tam = min(tam, 340)
    if e == "original":
        import peg_anim as PA
        if C.es_icono(imagen) and "marco" not in anim:   # el «vitral» parte el ícono (hoja fx 22-nov): otro marco
            marcos = [m for m in _MARCOS_ICONO if m in PA.MARCOS] or ["polaroid"]
            anim["marco"] = marcos[sum(map(ord, os.path.basename(str(imagen)))) % len(marcos)]
        return PA.variado(imagen, titulo, tam, tema="wow", **anim)
    m = _motor(e)
    if e == "pergamino":
        return m.Pegatina(imagen, titulo, tam, seed=C.hash_semilla(imagen, titulo) % 9973).fn()
    if e == "oro":
        return m.Pegatina(imagen, titulo, tam, seed=C.hash_semilla(imagen, titulo) % 97).fn()
    return m.Pegatina(imagen, titulo, tam).fn()


# ============================================================================ HELPERS para efectos.py (FX listos)
def _dir():
    f = _llamador()
    archivo = f.f_globals.get("__file__") if f is not None else None
    return os.path.dirname(os.path.abspath(archivo)) if archivo else os.getcwd()


def _ruta(nombre, carpeta, ext):
    """Ruta tal cual si existe; si no, <carpeta junto a efectos.py>/<nombre><ext>."""
    if nombre is None or str(nombre).startswith("ico:") or os.path.exists(str(nombre)):
        return nombre
    r = os.path.join(_dir(), carpeta, str(nombre) + ("" if str(nombre).lower().endswith(ext) else ext))
    if os.path.exists(r):
        return r
    raise SystemExit(f"mg_wow_estilos: no encuentro {nombre} (ni {r})")


def P(x, y, rot, sub=None, foto=None):
    """Paso de un mapa: (x %, y %, rótulo, subrótulo, foto); foto = slug de pegatinas/ o ruta."""
    return (x, y, rot, sub, _ruta(foto, "pegatinas", ".png") if foto else None)


def _icono_e(s):
    if str(s).startswith("ico:") or os.path.exists(str(s)):
        return s
    r = os.path.join(_dir(), "pegatinas", str(s) + ".png")
    return r if os.path.exists(r) else "ico:" + str(s)


def mapa_e(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.5, zmin=1.0, estilo=None):
    """FX `pantalla` con el mapa (mapas/<nom>.jpg). Mismos argumentos que mapa() de efectos.py + estilo."""
    # REGLA DEL USUARIO (25-nov-2026, `wow_ruta_profesiones`): los MAPAS van SIEMPRE con el mapa ORIGINAL a todo color
    # («no me convence ese cambio radical de estilo… mejor mostrar siempre el mapa original igual, solo tal vez cambiando
    # los trazos y líneas, pero siempre el mapa original mostrando el ícono del material, personaje, etc. en el mapa»).
    # Pergamino y holograma ya NO se usan en mapas (tiñen el mapa de sepia o de azul). Sí el ORO («esa sí me gusta: el
    # mapa original con ese estilo nuevo de íconos y trazos»: marco de oro y piedra, gemas de pin, placas). Rotación:
    # original → oro → original variante 1 (línea continua, rombo, placa negra) → original variante 2 (puntos, sello de
    # tinta, etiqueta de pergamino) y «madera» = la animación del viejo holograma (haz que cae, anillos rúnicos, ruta con
    # chispas, título que se descifra) en oro cálido SOBRE EL MAPA ORIGINAL sin filtro ni rejilla. Rotación de 5:
    # original → oro → madera → original v1 → original v2. Cada paso lleva su foto o ícono (material, personaje, lugar).
    # `estilo` fija uno de los tres motores ("original"/"oro"/"madera"); pergamino se ignora a propósito.
    _vigilar_dueno()
    k = _rep["cuenta"].get("mapa", 0)
    _rep["cuenta"]["mapa"] = k + 1
    est, var = (("original", 0), ("oro", 0), ("madera", 0), ("original", 1), ("original", 2))[k % 5]
    if estilo and _est(estilo) in ("original", "oro", "madera"):
        est = _est(estilo)
        var = 0 if est == "oro" else var
    return dict(tipo="pantalla", fn=mapa(est, _ruta(nom, "mapas", ".jpg"), puntos, titulo, sub, zmin, zmax, objeto,
                                         variante=var),
                de=de, a=a, marcas=list(marcas), entra=.5, sale=.5, nombre=f"mapa {est} v{var} {titulo}", ver=1.0)


def ficha_e(titulo, iconos, de, a, marcas, cuentas=None, total=None, etiquetas=None, x=.5, y=.55, estilo=None):
    """FX `mg` con la ficha; iconos = slugs de pegatinas/, rutas, «ico:…» o nombres de Wowhead; ícono k en la marca k."""
    est = _est(estilo) if estilo else siguiente("ficha")
    return dict(tipo="mg", fn=ficha(est, titulo, [_icono_e(i) for i in iconos], cuentas, total, etiquetas), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.4 if est == "original" else .08, nombre=f"ficha {est} {titulo}", ver=1.0)


def tarjeta_e(en, imagen, titulo, sub=None, dur=5.0, x=.76, y=.52, tam=500, estilo=None, **extra):
    """FX `mg` con la tarjeta de jefe/objeto/personaje (imagen = slug de pegatinas/ o ruta)."""
    est = _est(estilo) if estilo else siguiente("tarjeta")
    ruta = _ruta(imagen, "pegatinas", ".png")
    return dict(tipo="mg", fn=tarjeta(est, ruta, titulo, sub, tam, **extra), en=en, dur=dur, x=x, y=y,
                sale=.35 if est == "original" else .06, nombre=f"tarjeta {est} {os.path.basename(str(ruta))}", ver=1.2)


def rotulo_e(en, texto, sello=None, dur=4.5, x=None, y=.86, izq=110, estilo=None):
    """FX `mg` con el rótulo inferior; sin x, su borde izquierdo queda a `izq` px."""
    est = _est(estilo) if estilo else siguiente("rotulo")
    fn = rotulo(est, texto, sello)
    if x is None:
        x = (izq - fn.izq + fn.ancho / 2) / C.W
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre=f"rótulo {est} {texto[:24]}", ver=1.2)


def peg_e(en, imagen, titulo=None, dur=4.0, x=.17, y=.62, tam=400, estilo=None, **anim):
    """FX `mg` con una pegatina suelta en el marco de su estilo (imagen = slug de pegatinas/ o ruta)."""
    est = _est(estilo) if estilo else siguiente("pegatina")
    ruta = _ruta(imagen, "pegatinas", ".png")
    return dict(tipo="mg", fn=pegatina(est, ruta, titulo, tam, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre=f"pegatina {est} {os.path.basename(str(ruta))}", ver=1.0)
