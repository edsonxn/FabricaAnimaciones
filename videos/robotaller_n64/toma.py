# -*- coding: utf-8 -*-
"""El video entero: grabaciones reales con cámara (nucleo/montaje_real.py), Token de streamer y El Jefe, anclado a las palabras de la voz y partido por beats en medios/.
Estructura copiada de videos/robotaller_mes1/toma.py; planos según plan_montaje.md.
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
    "gancho_0": "explicar", "gancho_1": "tapa", "gancho_2": "fiesta", "gancho_4": "senala", "contraste_0": "pensar", "contraste_1": "gritar", "contraste_2": "selfie",
    "investiga_0": "leer", "investiga_3": "preguntar", "investiga_4": "palomita", "guion_1": "leer", "voz_1": "escuchar", "voz_2": "fallo", "voz_3": "fallo",
    "clips_0": "extintor", "clips_2": "fallo", "clips_4": "palomita", "capas_2": "fiesta", "sonido_2": "escuchar", "relevo_0": "dormir", "relevo_1": "preguntar",
    "relevo_2": "escuchar", "relevo_3": "leer", "relevo_4": "selfie", "revisa_1": "fallo", "revisa_2": "fiesta", "revisa_4": "escuchar", "miniatura_0": "esconde",
    "miniatura_2": "escuchar", "miniatura_3": "fiesta", "cuenta_2": "pensar", "junta_1": "explicar", "junta_2": "tapa",
}
PLAN = [
    minis(.2, []), pc(.3, cpu=64, gpu=88, temp=69, ram=71, red=7),
    *[pose(f["t0"], GESTO.get(k) or next(CARAS)) for k, f in FRASES.items()],
    pose(T("gancho_0", "falta"), "fallo"),
    minis(T("investiga_1", "ayudante"), ["investigador"]), minis(T("investiga_3"), []),
    minis(T("clips_2", "ayudante"), ["inspector"]), minis(T("clips_3"), []),
    pose(T("voz_3", "si"), "explicar"),
    pose(T("revisa_4", "no"), "palomita"),
    minis(T("relevo_4", "cinco"), ["investigador", "explorador", "obrero", "inspector", "cantor"]), js(T("relevo_4", "cinco"), "Extras.prueba('logro')"), minis(T("revisa_0"), []),
    pc(T("revisa_2"), cpu=97, gpu=99, temp=78, ram=83, red=2), pc(T("miniatura_0"), cpu=40, gpu=55, temp=62, ram=60, red=6),
    pose(T("cuenta_2", "el"), "palomita"),
    pose(T("junta_2", "jefe"), "fallo"),
]


# ---- cámara: A(inicio, clip, z0, (cx0, cy0), z1, (cx1, cy1)); cada plano termina donde empieza el siguiente
TRANS = itertools.cycle([("latigo", .34), ("corte", 0), ("zoom", .42), ("deslizar", .3), ("glitch", .22), ("latigo", .3), ("destello", .3), ("zoom", .36), ("corte", 0), ("deslizar", .28), ("glitch", .2)])
_lista = []
QUIETOS = {"capturas/cuenta.mp4", "capturas/miniaturas.mp4", "capturas/mapas.mp4"}   # páginas fijas: la cámara les da el movimiento


def A(ini, clip, z0=1.0, c0=(.5, .5), z1=None, c1=None, desde=0.0, vel=1.0, tr=None, ventana=True):
    _lista.append(dict(ini=ini, clip=clip, z0=z0, c0=c0, z1=z1 or z0, c1=c1 or c0, desde=desde, vel=vel, tr=tr, ventana=ventana and clip != TOKEN))


def C(n):
    return f"capturas/{n}.mp4"


def tok(ini, z0=1.0, c0=(.5, .5), z1=None, c1=None, tr=None):
    A(ini, TOKEN, z0, c0, z1, c1, tr=tr)


FICHA = (.13, .55)          # dónde queda Token en la toma del taller
MSJ = (.5, .77)             # el globo del mensaje en vivo
MSJ_J = (.6, .77)           # el globo corrido a la izquierda cuando habla El Jefe (él va a la derecha)
FALTA = (.48, .78)          # «croncias» dentro del globo
FALTA_J = (.56, .78)        # igual, pero corrida: con El Jefe a la derecha, «croncias» queda a la izquierda

# gancho: las nueve palabras, con su falta
tok(0, 1.45, (.18, .5), 1.25, (.2, .5), tr=("corte", 0))
A(T("gancho_0", "nueve"), C("mensaje"), 1.2, MSJ, 2.6, MSJ, desde=.3, vel=.5, tr=("latigo", .34))
A(T("gancho_1"), C("mensaje"), 2.6, MSJ, 3.4, FALTA_J, desde=2.4, vel=.3, tr=("corte", 0))
A(T("gancho_2"), C("m_intro"), 1.0, (.5, .5), 1.15, (.5, .45), desde=.5, tr=("destello", .3))
A(T("gancho_3"), C("hojas_clips"), 1.0, (.5, .5), 1.3, (.5, .4), desde=1, vel=1.4, tr=("glitch", .22))
A(T("gancho_3", "noventa"), C("pegatinas"), 1.0, (.5, .5), 1.4, (.5, .45), desde=1, vel=1.5, tr=("latigo", .3))
A(T("gancho_3", "mapas"), C("m_yoshi"), 1.1, (.5, .5), 1.0, (.5, .5), desde=6.5, tr=("corte", 0))
A(T("gancho_3", "treinta"), C("m_tetris"), 1.0, (.5, .5), 1.3, (.5, .45), desde=5.2, tr=("deslizar", .3))
A(T("gancho_4"), C("investiga"), 1.6, (.4, .2), 2.1, (.33, .14), desde=3, tr=("zoom", .4))
# contraste
tok(T("contraste_0"), 1.0, (.5, .5), 1.5, FICHA, tr=("destello", .28))
A(T("contraste_1"), C("investiga"), .82, (.5, .5), 1.15, (.5, .5), desde=8, vel=3, tr=("glitch", .2))
tok(T("contraste_2"), 1.6, FICHA, 1.25, (.22, .55), tr=("latigo", .3))
A(T("contraste_2", "cuadritos"), C("voz_eleven"), 1.4, (.3, .3), 2.6, (.2, .12), desde=3, vel=.5, tr=("zoom", .36))
A(T("contraste_2", "real"), C("fx_hojas"), 1.0, (.5, .5), 1.25, (.5, .5), desde=2, vel=1.2, tr=("corte", 0))
# paso 1: investigar
A(T("investiga_0"), C("investiga"), 1.5, (.4, .22), 2.0, (.33, .15), desde=4, vel=2, tr=("deslizar", .28))
A(T("investiga_1"), C("ayudante"), 1.6, (.5, .5), 1.1, (.5, .5), desde=.5, vel=.8, tr=("glitch", .22))
A(T("investiga_1", "revise"), C("investiga"), 1.5, (.4, .25), 1.9, (.33, .16), desde=12, tr=("latigo", .3))
A(T("investiga_2"), C("investigacion"), 1.0, (.5, .5), 1.5, (.4, .3), desde=1, tr=("zoom", .36))
A(T("investiga_3"), C("m_guantes"), 1.0, (.5, .5), 1.2, (.5, .5), desde=2, tr=("destello", .3))
A(T("investiga_4"), C("m_intro"), 1.25, (.6, .4), 1.0, (.5, .5), desde=1, tr=("corte", 0))
# paso 2: el guion
A(T("guion_0"), C("escribe_guion"), 1.0, (.5, .5), 1.5, (.35, .3), desde=.5, tr=("latigo", .3))
A(T("guion_0", "contados"), C("m_yoshi"), 1.5, (.82, .15), 1.0, (.5, .5), desde=0, tr=("glitch", .2))
A(T("guion_1"), C("guion_n64"), 1.0, (.5, .5), 1.6, (.4, .3), desde=0, tr=("deslizar", .3))
A(T("guion_1", "susurrando"), C("guion_n64"), 2.4, (.2, .14), 2.4, (.3, .14), desde=1.5, vel=.3, tr=("corte", 0))
A(T("guion_2"), C("guion_n64"), 1.0, (.5, .5), .8, (.5, .5), desde=6, vel=1.5, tr=("zoom", .36))
# paso 3: la voz
A(T("voz_0"), C("voz_eleven"), 1.0, (.5, .5), 1.5, (.3, .3), desde=0, tr=("latigo", .3))
A(T("voz_1"), C("whisper"), 1.3, (.35, .2), 1.8, (.3, .12), desde=1.2, vel=.4, tr=("glitch", .2))
A(T("voz_2"), C("whisper"), 1.6, (.25, .4), 1.9, (.22, .45), desde=6.3, vel=.3, tr=("destello", .28))
tok(T("voz_3"), 1.2, (.3, .6), 1.6, FICHA, tr=("deslizar", .28))
A(T("voz_3", "si"), C("whisper"), 1.2, (.4, .15), 1.6, (.35, .12), desde=13.5, vel=.6, tr=("zoom", .36))
# paso 4: las imágenes
A(T("clips_0"), C("ayudantes_clips"), 1.5, (.5, .5), 1.0, (.5, .5), desde=1, vel=.7, tr=("latigo", .3))
A(T("clips_1"), C("hojas_clips"), 1.0, (.5, .5), 2.2, (.3, .35), desde=0, vel=.7, tr=("corte", 0))
A(T("clips_2"), C("hojas_clips"), 1.4, (.6, .5), 1.0, (.5, .5), desde=6, vel=.8, tr=("glitch", .22))
A(T("clips_2", "treinta"), C("fx_hojas"), 1.0, (.5, .5), 1.4, (.5, .4), desde=4, tr=("deslizar", .3))
A(T("clips_3"), C("m_guantes"), 1.0, (.5, .5), 1.25, (.5, .45), desde=2, tr=("latigo", .3))
tok(T("clips_4"), 1.0, (.5, .5), 1.5, FICHA, tr=("destello", .28))
# las capas
A(T("capas_0"), C("m_intro"), 1.0, (.5, .5), 1.6, (.68, .35), desde=2, tr=("zoom", .36))
A(T("capas_0", "noventa"), C("pegatinas"), 1.2, (.5, .4), 1.0, (.5, .5), desde=4, vel=1.2, tr=("corte", 0))
A(T("capas_1"), C("m_yoshi"), 1.0, (.5, .5), 1.35, (.5, .55), desde=5, tr=("glitch", .2))
A(T("capas_2"), C("kit_mg"), 1.0, (.5, .5), 1.4, (.5, .45), desde=2, tr=("latigo", .3))
A(T("capas_2", "doscientos"), C("mg_hojas"), 1.0, (.5, .5), 1.5, (.5, .35), desde=1, vel=1.5, tr=("deslizar", .28))
# paso 5: el sonido (en «Escucha» suena la OST real, efectos.py)
A(T("sonido_0"), C("mapas_sesion"), 1.0, (.5, .5), 1.4, (.45, .45), desde=1, tr=("zoom", .36))
A(T("sonido_1"), C("m_tetris"), 1.0, (.5, .5), 1.2, (.5, .5), desde=0, vel=1.2, tr=("destello", .28))
A(T("sonido_2"), C("m_yoshi"), 1.25, (.5, .55), 1.0, (.5, .5), desde=1.2, tr=("corte", 0))
# el relevo
A(T("relevo_0"), C("relevo_a"), 1.0, (.5, .5), 1.5, (.45, .7), desde=1, vel=.8, tr=("latigo", .3))
tok(T("relevo_1"), 1.2, (.3, .6), 1.6, FICHA, tr=("glitch", .2))
A(T("relevo_2"), C("cambio_cuenta"), 1.6, MSJ, 2.6, MSJ_J, desde=1.5, vel=.5, tr=("zoom", .36))
A(T("relevo_3"), C("cierre_a"), 1.2, (.5, .6), 1.6, (.5, .7), desde=0, tr=("deslizar", .3))
A(T("relevo_3", "leyo"), C("relevo_b"), 1.0, (.5, .5), 1.5, (.45, .65), desde=2, tr=("corte", 0))
A(T("relevo_4"), C("ayudantes_clips"), 1.0, (.5, .5), 1.4, (.5, .55), desde=4, vel=.8, tr=("latigo", .3))
tok(T("relevo_4", "ninguna"), 1.5, FICHA, 1.15, (.3, .55), tr=("destello", .28))
# paso 6: revisar
A(T("revisa_0"), C("chequeo"), 1.0, (.5, .5), 1.5, (.4, .35), desde=0, tr=("glitch", .22))
A(T("revisa_1"), C("fx_hojas"), 1.3, (.5, .5), 1.0, (.5, .5), desde=8, tr=("zoom", .36))
A(T("revisa_2"), C("render"), 1.0, (.5, .5), 1.5, (.5, .7), desde=1, tr=("deslizar", .28))
A(T("revisa_3"), C("m_cierre"), 1.0, (.5, .5), 1.2, (.5, .5), desde=0, tr=("latigo", .3))
tok(T("revisa_4"), 1.0, (.5, .5), 1.5, FICHA, tr=("corte", 0))
# la miniatura
A(T("miniatura_0"), C("miniaturas"), 1.0, (.5, .5), 2.1, (.26, .3), desde=5, tr=("glitch", .2))
A(T("miniatura_1"), C("flow"), 1.0, (.5, .5), 1.4, (.5, .55), desde=0, tr=("destello", .28))
A(T("miniatura_2"), C("si_flow"), 1.6, MSJ, 2.6, MSJ_J, desde=1.5, vel=.5, tr=("zoom", .36))
A(T("miniatura_3"), C("miniaturas"), 1.0, (.5, .5), 2.1, (.74, .3), desde=5, tr=("latigo", .3))
A(T("miniatura_3", "desde"), C("flow_imgs"), 1.0, (.5, .5), 1.3, (.5, .45), desde=5.5, tr=("corte", 0))
# la cuenta
A(T("cuenta_0"), C("cuenta"), 1.0, (.5, .5), 1.6, (.27, .45), desde=2, tr=("deslizar", .3))
A(T("cuenta_1"), C("cuenta"), 1.6, (.27, .45), 1.6, (.73, .45), desde=2, tr=("corte", 0))
A(T("cuenta_2"), C("cuenta"), 1.6, (.73, .45), 1.0, (.5, .5), desde=2, tr=("corte", 0))
A(T("cuenta_2", "decidir"), C("mensaje"), 1.5, MSJ, 2.4, MSJ, desde=2.2, vel=.3, tr=("glitch", .22))
A(T("cuenta_3"), C("investiga"), 1.0, (.5, .5), .8, (.5, .5), desde=1, vel=3, tr=("zoom", .4))
# la junta directiva
A(T("junta_0"), C("m_iwata"), 1.0, (.5, .5), 1.25, (.5, .45), desde=0, tr=("latigo", .3))     # el Montaje del panel salió en blanco al regrabarlo
tok(T("junta_1"), 1.0, (.5, .5), 1.5, FICHA, tr=("deslizar", .28))
A(T("junta_2"), C("mensaje"), 2.4, MSJ, 3.4, FALTA, desde=2.4, vel=.3, tr=("glitch", .2))


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
        m.jefe(f["t0"] - .22, f["t1"] + .24, f"voz/final/{k}.wav", "d", alto=620)
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
