# -*- coding: utf-8 -*-
"""El video entero (robotaller_4apps): grabaciones reales con cámara (nucleo/montaje_real.py), Token de streamer y El Jefe, anclado a las palabras de la voz.
Estructura copiada de videos/robotaller_n64/toma.py; planos según plan_montaje.md.
  python toma.py token            graba al robot (medios/token.mp4); solo hace falta si cambia la voz o su plan
  python toma.py montaje [a b]    arma medios/toma.mp4 (o solo del segundo a al b, para probar: medios/prueba.mp4)
  python toma.py partir           corta toma.mp4 por beats
  python toma.py hoja t1 t2 ...   cuadros sueltos en previews/toma_hoja.jpg, sin renderizar
"""
import itertools
import json
import os
import subprocess
import sys
import unicodedata

sys.path.insert(0, "../../nucleo")
import guion
import robotaller as R
from jefe_canadiense import Jefe
from montaje_real import Montaje, plano

FF = R.FFMPEG
tl = json.load(open("timeline.json", encoding="utf-8"))
FRASES = {f["key"]: f for e in tl["escenas"] for f in e["frases"]}
TOTAL = tl["total"]
TOKEN = "medios/token.mp4"
FIN_VOZ = max(w["e"] for w in FRASES["junta_2"]["words"])


def _llano(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn").strip(".,:;¿?¡!-")


def T(clave, palabra=None, mas=0.0):
    """Segundo de una frase, o de una de sus palabras."""
    f = FRASES[clave]
    if palabra:
        for w in f["words"]:
            if _llano(w["w"]) == _llano(palabra):
                return w["s"] + mas
        raise KeyError(f"{clave}: {palabra}")
    return f["t0"] + mas


# ---- Token: una toma entera del taller
def pose(t, nombre):
    if nombre == "senala":
        return dict(t=t, js="Taller.actividad('senala','¡Mira!',60000)")
    return dict(t=t, pose=nombre)


def js(t, codigo):
    return dict(t=t, js=codigo)


def minis(t, tipos):
    lista = [dict(id=f"m{i}", tipo=x, desc="", activo=True) for i, x in enumerate(tipos)]
    return js(t, f"Taller.sync({json.dumps(lista)},null)")


def pc(t, **k):
    return js(t, f"Taller.datosPC({json.dumps(R.muestra_pc(**k))})")


CARAS = itertools.cycle(("explicar", "preguntar", "leer", "explicar", "pensar", "palomita"))
GESTO = {
    "gancho_0": "explicar", "gancho_1": "fiesta", "gancho_2": "senala", "contraste_0": "selfie", "contraste_1": "leer", "altima_0": "explicar",
    "altima_3": "palomita", "altima_4": "pensar", "altima_5": "leer", "altima_6": "preguntar", "altima_7": "leer", "altima_9": "fiesta",
    "micwifi_0": "explicar", "micwifi_3": "escuchar", "micwifi_4": "fallo", "micwifi_6": "fiesta", "rayo_0": "preguntar", "rayo_4": "selfie",
    "puente_0": "explicar", "puente_2": "dormir", "puente_3": "escuchar", "tele_0": "tapa", "tele_3": "palomita", "tele_5": "selfie",
    "cuenta_0": "pensar", "cuenta_1": "leer", "cuenta_2": "explicar", "cuenta_4": "senala", "junta_1": "explicar", "junta_2": "tapa",
}
PLAN = [
    minis(.2, []), pc(.3, cpu=64, gpu=88, temp=69, ram=71, red=7),
    *[pose(f["t0"], GESTO.get(k) or next(CARAS)) for k, f in FRASES.items()],
    pose(T("altima_3", "no"), "fallo"),
    pose(T("altima_6", "ya"), "preguntar"),
    minis(T("altima_7"), ["obrero"]), pc(T("altima_7"), cpu=91, gpu=40, temp=74, ram=80, red=3), minis(T("altima_9"), []),
    minis(T("micwifi_2"), ["obrero", "inspector"]), minis(T("micwifi_5"), []),
    pc(T("micwifi_6"), cpu=48, gpu=30, temp=60, ram=62, red=9),
    minis(T("rayo_2"), ["explorador"]), minis(T("rayo_4"), []),
    pose(T("cuenta_1", "durmio"), "dormir"),
    minis(T("cuenta_1"), ["investigador", "explorador", "obrero", "inspector"]), js(T("cuenta_1", "acciones"), "Extras.prueba('logro')"), minis(T("cuenta_2"), []),
    pose(T("junta_2", "jefe"), "fallo"),
]


# ---- cámara: A(inicio, clip, z0, (cx0, cy0), z1, (cx1, cy1)); cada plano termina donde empieza el siguiente
TRANS = itertools.cycle([("latigo", .34), ("corte", 0), ("zoom", .42), ("deslizar", .3), ("glitch", .22), ("latigo", .3), ("destello", .3), ("zoom", .36), ("corte", 0), ("deslizar", .28), ("glitch", .2)])
_lista = []
QUIETOS = set()


def A(ini, clip, z0=1.0, c0=(.5, .5), z1=None, c1=None, desde=0.0, vel=1.0, tr=None, ventana=True):
    _lista.append(dict(ini=ini, clip=clip, z0=z0, c0=c0, z1=z1 or z0, c1=c1 or c0, desde=desde, vel=vel, tr=tr, ventana=ventana and clip != TOKEN))


def C(n):
    return f"capturas/{n}.mp4"


def tok(ini, z0=1.0, c0=(.5, .5), z1=None, c1=None, tr=None):
    A(ini, TOKEN, z0, c0, z1, c1, tr=tr)


FICHA = (.13, .55)          # dónde queda Token en la toma del taller
MSJ = (.5, .77)             # el globo del mensaje en las tomas del Robotaller
MSJ_J = (.6, .77)           # corrido: con El Jefe a la derecha, el globo queda a la izquierda
CODIGO = (.3, .22)          # arriba a la izquierda: las líneas de código y de consola
ESCUCHA = FRASES["puente_3"]["words"][-1]["e"] + .08    # «Escucha:» → suena la tele real (efectos.py) y el robot sale a la vez (s 3,4 de tele_aviso)
ROBOT = 3.4

# gancho: cuatro apps, una por aparato
tok(0, 1.45, (.18, .5), 1.25, (.2, .5), tr=("corte", 0))
A(T("gancho_0", "carro"), C("alt_pide"), 1.5, MSJ, 1.8, MSJ, desde=1, vel=.6, tr=("latigo", .34))
A(T("gancho_0", "telefono"), C("mic_pide"), 1.5, MSJ, 1.8, MSJ, desde=1, vel=.6, tr=("corte", 0))
A(T("gancho_0", "computadora"), C("rayo_pc"), 1.0, (.5, .5), 1.25, (.5, .4), desde=2, tr=("zoom", .36))
A(T("gancho_0", "tele"), C("tele_aviso"), 1.0, (.5, .5), 1.15, (.5, .45), desde=0, tr=("deslizar", .3))
A(T("gancho_1"), C("alt_funciona"), 1.6, MSJ, 1.9, MSJ, desde=1, tr=("glitch", .22))
A(T("gancho_1", "las"), C("mic_jala"), 2.0, MSJ, 2.4, MSJ, desde=.5, tr=("corte", 0))
A(T("gancho_1", "funcionaban"), C("tele_aviso"), 1.0, (.5, .5), 1.2, (.5, .42), desde=4, tr=("destello", .3))
A(T("gancho_2"), C("alt_codigo"), 1.0, (.5, .5), 1.4, CODIGO, desde=0, vel=2.4, tr=("latigo", .3))
A(T("gancho_2", "conversaciones"), C("alt_versiones"), 1.5, MSJ, 1.9, MSJ, desde=1, tr=("zoom", .36))
# contraste
tok(T("contraste_0"), 1.0, (.5, .5), 1.5, FICHA, tr=("destello", .28))
A(T("contraste_0", "cuadritos"), C("mic_firewall"), 1.5, (.3, .2), 1.8, (.25, .15), desde=7.5, vel=.6, tr=("glitch", .2))
A(T("contraste_1"), C("rayo_codigo"), 1.0, (.5, .5), 1.4, CODIGO, desde=0, tr=("deslizar", .28))
A(T("contraste_1", "necesitaba", -.5), C("ideas_pide"), 1.3, (.5, .65), 1.7, MSJ, desde=0, vel=.7, tr=("corte", 0))
# 1: el escáner del carro (sin modelo ni año: pedido del usuario, 5-nov)
tok(T("altima_0"), 1.0, (.5, .5), 1.4, FICHA, tr=("latigo", .3))
A(T("altima_0", "tres"), C("alt_pide"), 1.2, (.5, .6), 1.7, MSJ, desde=0, vel=.5, tr=("zoom", .36))
A(T("altima_2"), C("alt_pide"), 1.7, (.45, .76), 1.8, (.55, .76), desde=4.5, vel=.3, tr=("corte", 0))
A(T("altima_2", "graficas"), C("alt_codigo"), 1.0, (.5, .5), 1.4, CODIGO, desde=6, tr=("glitch", .22))
A(T("altima_3"), C("alt_versiones"), 1.0, (.5, .5), 1.4, (.5, .65), desde=0, tr=("deslizar", .3))
A(T("altima_3", "no"), C("alt_falla"), 1.6, MSJ, 2.2, MSJ, desde=0, vel=.7, tr=("glitch", .2))
A(T("altima_4"), C("alt_falla"), 2.0, MSJ, 2.3, MSJ, desde=3, vel=.6, tr=("corte", 0))
A(T("altima_5"), C("alt_registro"), 1.7, (.32, .77), 1.9, (.68, .77), desde=0, tr=("latigo", .3))
A(T("altima_6"), C("alt_versiones"), 1.4, (.5, .7), 1.7, (.48, .76), desde=8, vel=.9, tr=("zoom", .36))
tok(T("altima_6", "ya"), 1.5, FICHA, 1.2, (.25, .55), tr=("destello", .28))
A(T("altima_7"), C("alt_versiones"), 1.0, (.5, .5), 1.3, (.5, .4), desde=0, vel=2, tr=("deslizar", .28))
A(T("altima_7", "escribio"), C("alt_funciona"), 1.4, (1.0, .77), 1.5, (1.0, .77), desde=.5, vel=.6, tr=("corte", 0), ventana=False)   # sin Token: el mensaje del Jefe a la izquierda
A(T("altima_9"), C("alt_alertas"), 1.4, (.5, .6), 2.0, MSJ, desde=1, tr=("glitch", .22))
# 2: MicWiFi
tok(T("micwifi_0"), 1.0, (.5, .5), 1.4, FICHA, tr=("latigo", .3))
A(T("micwifi_0", "nueve"), C("mic_pide"), 1.2, (.5, .6), 1.7, MSJ, desde=0, vel=.7, tr=("zoom", .36))
A(T("micwifi_2"), C("mic_codigo"), 1.0, (.5, .5), 1.4, CODIGO, desde=0, vel=1.2, tr=("deslizar", .3))
tok(T("micwifi_3"), 1.2, (.3, .6), 1.6, FICHA, tr=("glitch", .2))
A(T("micwifi_3", "deformaba"), C("mic_firewall"), 1.4, (.5, .72), 1.7, MSJ, desde=2, vel=.8, tr=("corte", 0))
A(T("micwifi_4"), C("mic_codigo"), 1.0, (.5, .5), 1.4, CODIGO, desde=8, vel=.8, tr=("latigo", .3))
A(T("micwifi_4", "dieciocho"), C("mic_jala"), 1.4, (.5, .6), 2.4, MSJ_J, desde=0, vel=.5, tr=("zoom", .4))
tok(T("micwifi_6"), 1.0, (.5, .5), 1.3, (.3, .55), tr=("destello", .28))
# 3: Rayo
A(T("rayo_0"), C("rayo_pide"), 1.3, (.5, .65), 1.7, MSJ, desde=0, vel=.6, tr=("latigo", .3))
A(T("rayo_1", "sin"), C("rayo_codigo"), 1.0, (.5, .5), 1.35, CODIGO, desde=0, tr=("glitch", .22))
A(T("rayo_2"), C("rayo_pc"), 1.0, (.5, .5), 1.35, (.5, .3), desde=0, tr=("deslizar", .28))
A(T("rayo_3"), C("rayo_pc"), 1.8, (.3, .7), 2.0, (.72, .65), desde=7.5, vel=.8, tr=("zoom", .36))
A(T("rayo_4"), C("auto_rayo"), 1.4, (.5, .7), 1.7, (.5, .76), desde=0, tr=("glitch", .2))
A(T("rayo_4", "ahora"), C("rayo_pc"), 1.6, (.66, .74), 2.2, (.66, .8), desde=3, vel=.6, tr=("latigo", .3))
# 4: Puente TV
tok(T("puente_0"), 1.0, (.5, .5), 1.4, FICHA, tr=("destello", .28))
A(T("puente_0", "puente"), C("tv_pide"), 1.3, (.5, .6), 1.7, MSJ, desde=0, vel=.7, tr=("corte", 0))
A(T("puente_1", "la"), C("tele_aviso"), 1.0, (.5, .5), 1.2, (.5, .45), desde=1.5, tr=("zoom", .36))
A(T("puente_2"), C("tv_codigo"), 1.0, (.5, .5), 1.4, (.35, .3), desde=0, tr=("deslizar", .3))
A(T("puente_3"), C("tv_prueba"), 1.4, (.3, .2), 1.6, (.3, .18), desde=7, tr=("glitch", .22))
A(ESCUCHA - ROBOT, C("tele_aviso"), 1.0, (.5, .5), 1.2, (.5, .42), desde=0, tr=("destello", .3))
tok(T("tele_0", "historia"), 1.0, (.5, .5), 1.5, FICHA, tr=("latigo", .3))
A(T("tele_1"), C("ideas_pide"), 1.3, (.5, .6), 1.7, MSJ, desde=0, vel=.9, tr=("zoom", .36))
tok(T("tele_1", "varias"), 1.0, (.5, .5), 1.4, FICHA, tr=("corte", 0))
A(T("tele_1", "contesto"), C("ideas_no"), 1.4, (.62, .74), 1.7, (.66, .73), desde=0, vel=.7, tr=("glitch", .2), ventana=False)
tok(T("tele_3"), 1.0, (.5, .5), 1.4, FICHA, tr=("deslizar", .28))
A(T("tele_4"), C("tele_revision"), 1.0, (.5, .5), 1.3, (.6, .45), desde=0, tr=("latigo", .3))
A(T("tele_5"), C("tele_protector"), 1.0, (.5, .5), 1.25, (.5, .45), desde=0, tr=("zoom", .36))
tok(T("tele_5", "ese"), 1.0, (.5, .5), 1.5, FICHA, tr=("corte", 0))
# la cuenta
A(T("cuenta_0"), C("puente_pc"), 1.0, (.5, .5), 1.25, (.45, .5), desde=0, tr=("destello", .28))
A(T("cuenta_0", "primer"), C("alt_pide"), 1.5, (.5, .65), 1.7, MSJ, desde=0, vel=.5, tr=("glitch", .22))
A(T("cuenta_0", "manual"), C("rayo_pc"), 1.6, (.66, .72), 2.0, (.66, .76), desde=9, vel=.6, tr=("latigo", .3))
A(T("cuenta_1"), C("alt_codigo"), 1.2, CODIGO, 1.4, CODIGO, desde=10, vel=1.5, tr=("corte", 0))
A(T("cuenta_1", "aplicaciones"), C("mic_codigo"), 1.2, CODIGO, 1.4, CODIGO, desde=4, vel=1.5, tr=("zoom", .3))
A(T("cuenta_1", "ochocientas"), C("rayo_codigo"), 1.2, CODIGO, 1.4, CODIGO, desde=5, vel=1.5, tr=("corte", 0))
A(T("cuenta_1", "acciones"), C("tv_codigo"), 1.2, CODIGO, 1.4, CODIGO, desde=6, vel=1.5, tr=("glitch", .2))
tok(T("cuenta_1", "en"), 1.0, (.5, .5), 1.5, FICHA, tr=("deslizar", .28))
A(T("cuenta_2"), C("rayo_pc"), 1.0, (.5, .5), 1.3, (.5, .45), desde=2, tr=("latigo", .3))
A(T("cuenta_2", "vender", -.8), C("tele_protector"), 1.0, (.5, .5), 1.3, (.5, .45), desde=2, tr=("corte", 0))
tok(T("cuenta_2", "las"), 1.0, (.5, .5), 1.4, FICHA, tr=("destello", .3))
A(T("cuenta_3", "saber", -.6), C("alt_pide"), 1.6, MSJ, 1.8, MSJ, desde=2, vel=.5, tr=("zoom", .36))
A(T("cuenta_3", "pedirlo"), C("mic_pide"), 1.6, MSJ, 1.8, MSJ, desde=2, vel=.5, tr=("glitch", .22))
tok(T("cuenta_4"), 1.0, (.5, .5), 1.5, FICHA, tr=("latigo", .3))
# la junta directiva
A(T("junta_0"), C("puente_pc"), 1.0, (.5, .5), 1.3, (.5, .45), desde=4, tr=("deslizar", .28))
A(T("junta_0", "cambio"), C("alt_versiones"), 1.5, (.5, .7), 1.7, MSJ, desde=8, tr=("corte", 0))
A(T("junta_0", "conversaciones"), C("tv_pide"), 1.5, MSJ, 1.7, MSJ, desde=3, vel=.6, tr=("glitch", .2))
tok(T("junta_1"), 1.0, (.5, .5), 1.5, FICHA, tr=("destello", .28))
A(T("junta_2"), C("mic_jala"), 2.0, MSJ, 3.4, MSJ, desde=0, vel=.5, tr=("zoom", .4))


JEFE_FRASES = guion.JEFE


def _dur(ruta):
    import cv2
    c = cv2.VideoCapture(ruta)
    n, f = c.get(cv2.CAP_PROP_FRAME_COUNT), c.get(cv2.CAP_PROP_FPS) or 30
    c.release()
    return n / f


def quietos(m):
    """Planos que se comen el final de su grabación (se quedaría congelada)."""
    malo = []
    for p in m.planos:
        if p["reloj"] or p["clip"] in QUIETOS:
            continue
        sobra = p["desde"] + (p["a"] - p["de"]) * p["vel"] - _dur(p["clip"])
        if sobra > 1.0:
            malo.append(f"quieto {sobra:.1f} s al final de {p['clip']} en {p['de']:.1f}")
    return malo


def armar():
    m = Montaje("medios/toma.mp4", TOTAL)
    for a, b in zip(_lista, _lista[1:] + [dict(ini=TOTAL)]):
        fin = b["ini"]
        m.planos.append(plano(a["clip"], a["ini"], fin, desde=a["desde"], vel=a["vel"], cam=[(a["ini"], a["z0"], *a["c0"]), (fin, a["z1"], *a["c1"])],
                              tr=a["tr"] or next(TRANS), reloj=a["clip"] == TOKEN))
        m.planos[-1]["ventana"] = a["ventana"]
    trozos = []
    for p in m.planos:
        if p["ventana"]:
            if trozos and abs(trozos[-1][1] - p["de"]) < .05:
                trozos[-1][1] = p["a"]
            else:
                trozos.append([p["de"], p["a"]])
    for de, a in trozos:
        m.camara(de + .15, a - .1, "bi", caja=(0, .3, .34, .52), ancho=400)
    m._jefe = Jefe("propios/jefe_limpio.png", boca_y=.523 / .75, bisagra_x=.33, frente_x=.57, corte=.75)
    for k in JEFE_FRASES:
        f = FRASES[k]
        m.jefe(f["t0"] - .22, f["t1"] + .24, f"voz/final/{k}.wav", "i" if k == "tele_2" else "d", alto=620)   # tele_2: su mensaje queda a la derecha
    return m


def golpes(m):
    """Segundos de cada transición y entrada del Jefe, para sus SFX (efectos.py)."""
    out = [[p["tr"][0], p["de"]] for p in m.planos if p["tr"][1]] + [["jefe", d["de"]] for d in m.jefes]
    json.dump(out, open("medios/golpes.json", "w", encoding="utf-8"))


def partir():
    for b in json.load(open("beats.json", encoding="utf-8")):
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(b["t0"]), "-i", "medios/toma.mp4", "-t", str(round(b["t1"] - b["t0"], 3)), "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-an", f"medios/{b['id']}.mp4"], check=True)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    os.makedirs("medios", exist_ok=True)
    if arg == "token":
        R.grabar(TOKEN, TOTAL, PLAN, pc=R.muestra_pc(cpu=64, gpu=88, temp=69, ram=71, red=7), crf=23, hasta=float(sys.argv[2]) if len(sys.argv) > 2 else None)
        print("ok", TOKEN)
    elif arg == "revisar":
        m = armar()
        print("\n".join(m.revisar() + quietos(m)) or "planos sin huecos ni congelados")
    elif arg == "montaje":
        m = armar()
        print("\n".join(m.revisar() + quietos(m)) or "planos sin huecos ni congelados")
        golpes(m)
        if len(sys.argv) > 2:
            m.salida = "medios/prueba.mp4"
            print(m.render(float(sys.argv[2]), float(sys.argv[3])))
        else:
            print(m.render())
    elif arg == "partir":
        partir()
    elif arg == "hoja":
        import cv2
        import numpy as np
        m = armar()
        ts = [float(x) for x in sys.argv[2:]]
        cs = [cv2.resize(m.cuadro(t), (640, 360), interpolation=cv2.INTER_AREA) for t in ts]
        for c, t in zip(cs, ts):
            cv2.putText(c, f"{t:.1f}", (8, 24), 0, .7, (0, 255, 255), 2)
        while len(cs) % 3:
            cs.append(np.zeros((360, 640, 3), np.uint8))
        cv2.imwrite("previews/toma_hoja.jpg", np.vstack([np.hstack(cs[i:i + 3]) for i in range(0, len(cs), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
        print("previews/toma_hoja.jpg")
