# -*- coding: utf-8 -*-
"""El video entero: grabaciones reales con cámara (nucleo/montaje_real.py), Token de streamer y El Jefe, anclado a las palabras de la voz y partido por beats en medios/.
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

sys.path.insert(0, "../../nucleo")
import guion
import montaje_real as MR
import robotaller as R
from jefe_canadiense import Jefe
from montaje_real import Montaje, plano

FF = R.FFMPEG
tl = json.load(open("timeline.json", encoding="utf-8"))
FRASES = {f["key"]: f for e in tl["escenas"] for f in e["frases"]}
TOTAL = tl["total"]
TOKEN = "medios/token.mp4"
FIN_VOZ = max(w["e"] for w in FRASES["junta_7"]["words"])


def T(clave, palabra=None, mas=0.0):
    """Segundo de una frase, o de una de sus palabras."""
    f = FRASES[clave]
    if palabra:
        for w in f["words"]:
            if w["w"].lower().strip(".,:;¿?¡!-") == palabra.lower():
                return w["s"] + mas
        raise KeyError(f"{clave}: {palabra}")
    return f["t0"] + mas


# ---- Token: una toma entera del taller; poses que no van a estación, para que no se salga de su ventanita
LLAVES_JS = r"""
window.Llaves=(()=>{
  const g=document.getElementById('taller').getContext('2d'),M={ini:-1e9,ahora:0};
  const llave=(x,y,rot,c)=>{g.save();g.translate(x,y);g.rotate(rot);g.fillStyle=c;g.strokeStyle="#7a5a12";g.lineWidth=5;
    g.beginPath();g.arc(0,-46,26,0,7);g.arc(0,-46,11,0,7,true);g.fill("evenodd");g.stroke();
    g.beginPath();g.roundRect(-8,-22,16,92,4);g.fill();g.stroke();
    for(const [yy,ll] of [[42,26],[60,18]]){g.beginPath();g.roundRect(6,yy,ll,10,2);g.fill();g.stroke();}
    g.restore();};
  function pinta(t){
    const u=(t-M.ini)/1000;if(u<0||u>30)return;
    const W=g.canvas.width,H=g.canvas.height,k=W/1920,cab=Taller.estado().x*W,golpe=.42;
    let x,y,rot;
    if(u<golpe){const p=u/golpe;x=cab;y=-220*k+(H*.44+220*k)*p*p;rot=p*2.4;}
    else{const q=Math.min(1,(u-golpe)/1.05),b=Math.abs(Math.cos(q*Math.PI*2.5))*(1-q)**1.4;x=cab+(330*q)*k;y=H*.74-(H*.3)*b;rot=2.4+q*9*(1-q*.35);}
    g.save();g.translate(x,y);g.scale(k*1.25,k*1.25);g.translate(-x,-y);
    g.lineWidth=7;g.strokeStyle="#c9a227";g.beginPath();g.ellipse(x,y,46,46,0,0,7);g.stroke();
    llave(x-20,y+6,rot,"#ffd166");llave(x+22,y+2,rot+.8,"#f4b942");llave(x,y+16,rot-.7,"#ffe29a");
    g.save();g.translate(x+46,y+30);g.rotate(rot*.5);g.fillStyle="#ff5d73";g.strokeStyle="#7a1f2e";g.lineWidth=4;g.beginPath();g.roundRect(0,0,130,50,10);g.fill();g.stroke();
    g.fillStyle="#fff";g.font="800 28px 'Segoe UI'";g.textBaseline="middle";g.fillText("CANAL",16,26);g.restore();
    g.restore();
    if(u>golpe&&u<3.4){const n=5,hy=H*.44;for(let i=0;i<n;i++){const a=u*5+i*6.283/n,rx=100*k,ry=30*k;g.fillStyle="#ffd166";g.font=`${40*k}px serif`;g.fillText("★",cab-14*k+Math.cos(a)*rx,hy-46*k+Math.sin(a)*ry);}}
  }
  const prev=Taller.Cap.encima;
  Taller.Cap.encima=(t,dt)=>{if(prev)prev(t,dt);M.ahora=t;pinta(t);};
  return {cae(){M.ini=M.ahora;}};
})();
"""


def pose(t, nombre):
    if nombre == "senala":                     # pose propia del video: el taller no le conoce letrero
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
    "gancho_0": "explicar", "gancho_1": "fallo", "gancho_2": "explicar", "contraste_0": "gritar", "contraste_1": "escuchar", "contraste_2": "fiesta",
    "quien_0": "selfie", "quien_3": "tapa", "archivo_6": "fallo", "archivo_7": "selfie", "creado_1": "esconde", "creado_4": "esconde", "como_2": "escuchar", "como_6": "fallo",
    "como_8": "selfie", "como_11": "escuchar", "como_12": "escuchar", "version_1": "tapa", "version_2": "dormir", "fallos_0": "esconde", "fallos_2": "fallo", "fallos_3": "extintor",
    "fallos_4": "chocar", "fallos_5": "pensar", "fallos_7": "escuchar", "fallos_9": "escuchar", "fallos_10": "fiesta", "relevo_0": "fallo", "relevo_2": "dormir", "relevo_4": "selfie",
    "junta_2": "fiesta", "junta_4": "fallo", "junta_7": "correr",
}
PLAN = [
    minis(.2, ["obrero", "investigador"]), pc(.3, cpu=82, gpu=91, temp=71, ram=74, red=9),
    *[pose(f["t0"], GESTO.get(k) or next(CARAS)) for k, f in FRASES.items()],
    # las llaves del canal: le caen en la cabeza justo en «llaves»
    minis(T("gancho_2"), []), js(T("gancho_2", "llaves", -.42), "Llaves.cae()"), pose(T("gancho_2", "llaves"), "chocar"), pose(T("gancho_2", "llaves", .5), "fallo"),
    pose(T("gancho_3"), "pensar"), pose(T("gancho_3", "entiendo"), "preguntar"),
    pose(T("archivo_7", "hola"), "palomita"),
    pose(T("fallos_4", "desconectó"), "dormir"), pose(T("fallos_4", "conectar"), "chocar"), pc(T("fallos_4", "desconectó"), cpu=0, gpu=0, temp=30, ram=0, e=99, red=0),
    pc(T("fallos_4", "conectar"), cpu=25, gpu=10, temp=50, ram=60, e=88),
    minis(T("junta_2"), ["investigador", "explorador", "obrero", "inspector", "cantor"]), js(T("junta_2", "junta"), "Extras.prueba('logro')"), minis(T("junta_3"), []),
    js(T("junta_7", mas=.8), "Extras.prueba('relevo')"), pose(T("junta_7", "mil"), "dormir"),
]


# ---- cámara: A(inicio, clip, z0, (cx0, cy0), z1, (cx1, cy1)); cada plano termina donde empieza el siguiente
TRANS = itertools.cycle([("latigo", .34), ("corte", 0), ("zoom", .42), ("deslizar", .3), ("glitch", .22), ("latigo", .3), ("destello", .3), ("zoom", .36), ("corte", 0), ("deslizar", .28), ("glitch", .2)])
_lista = []


def A(ini, clip, z0=1.0, c0=(.5, .5), z1=None, c1=None, desde=0.0, vel=1.0, tr=None, ventana=True):
    _lista.append(dict(ini=ini, clip=clip, z0=z0, c0=c0, z1=z1 or z0, c1=c1 or c0, desde=desde, vel=vel, tr=tr, ventana=ventana and clip != TOKEN))


def C(n):
    return f"capturas/{n}.mp4"


def tok(ini, z0=1.0, c0=(.5, .5), z1=None, c1=None, tr=None):
    A(ini, TOKEN, z0, c0, z1, c1, tr=tr)


FICHA = (.13, .55)     # dónde queda Token en la toma del taller
# gancho: arranca con Token, entra rápido a lo real
tok(0, 1.45, (.18, .5), 1.25, (.2, .5), tr=("corte", 0))
A(T("gancho_0", "treinta"), C("vivo"), 3.2, (.87, .585), 1.0, (.5, .5), desde=2, tr=("latigo", .34))
A(T("gancho_1"), C("mira"), 3.4, (.76, .19), 2.6, (.76, .19), desde=3, tr=("glitch", .22))
tok(T("gancho_2"), 1.3, (.2, .6), 1.55, FICHA, tr=("destello", .3))
# contraste
A(T("contraste_0"), C("lienzo"), 1.3, (.56, .55), 1.3, (.56, .5), desde=2.7, vel=.5, tr=("zoom", .42))
A(T("contraste_1"), C("clasico"), 2.4, (.2, .42), 2.4, (.42, .42), desde=4, vel=.3, tr=("deslizar", .3))
A(T("contraste_2"), C("clasico"), 2.4, (.42, .42), 1.1, (.5, .5), desde=7, vel=.3, tr=("corte", 0))
# quién es
A(T("quien_0"), C("vivo"), 4.2, (.06, .39), 2.2, (.1, .39), desde=2, tr=("latigo", .3), ventana=False)
A(T("quien_1"), C("vivo"), 2.2, (.1, .39), 1.0, (.5, .5), desde=6, tr=("corte", 0), ventana=False)
A(T("quien_2"), C("escribe"), 1.0, (.5, .5), 1.5, (.42, .4), desde=1, tr=("destello", .3))
A(T("quien_3"), C("escribe"), 2.4, (.3, .6), 6.0, (.14, .655), desde=3.2, vel=.02, tr=("zoom", .36))
A(T("quien_3", "él"), C("vivo"), 1.6, (.5, .75), 2.8, (.86, .585), desde=8, tr=("glitch", .2))
# la trayectoria, con fragmentos reales
A(T("archivo_0"), C("arch_tutorial"), 1.0, (.5, .5), 1.5, (.5, .35), vel=.8, tr=("deslizar", .3))
A(T("archivo_1", "muñecos"), C("arch_ragdoll"), 1.15, (.4, .5), 1.0, (.5, .5), vel=.9, tr=("latigo", .3))
A(T("archivo_2"), C("arch_toro"), 1.25, (.5, .5), 1.0, (.5, .5), vel=.8, tr=("glitch", .2))
A(T("archivo_3"), C("arch_slime_16x9"), 1.0, (.5, .5), 1.3, (.5, .45), tr=("zoom", .36))
A(T("archivo_4"), C("arch_vr_16x9"), 1.3, (.5, .5), 1.0, (.5, .5), tr=("destello", .28))
A(T("archivo_5"), C("arch_iajuego"), 1.0, (.5, .5), 1.9, (.5, .28), vel=.7, tr=("deslizar", .28))
A(T("archivo_6"), C("arch_iajuego"), 1.9, (.5, .28), 3.0, (.5, .2), desde=4, vel=.5, tr=("corte", 0))
tok(T("archivo_7"), 1.2, (.3, .6), 1.7, FICHA, tr=("latigo", .3))
A(T("archivo_8"), C("arch_doc"), 1.0, (.5, .5), 1.25, (.5, .5), tr=("glitch", .2))
A(T("archivo_8", "desde"), C("vivo"), 1.0, (.5, .5), 2.6, (.25, .05), desde=4, tr=("zoom", .36))
# lo creado
A(T("creado_0"), C("clasico"), 1.0, (.5, .4), 1.2, (.5, .5), desde=2.5, vel=.6, tr=("latigo", .3))
A(T("creado_1"), C("vivo"), 1.0, (.5, .5), 1.7, (.42, .3), desde=8, tr=("corte", 0))
A(T("creado_2"), C("aldea"), 2.3, (.55, .42), 1.1, (.5, .5), desde=6, tr=("deslizar", .3))
A(T("creado_3"), C("fabrica3d"), 1.0, (.5, .55), 1.6, (.5, .4), desde=3.5, tr=("zoom", .36))
A(T("creado_4"), C("movil_16x9"), 1.0, (.5, .5), 1.45, (.5, .4), desde=3, tr=("latigo", .3))
A(T("creado_5"), C("montaje"), 1.0, (.5, .5), 1.5, (.5, .88), desde=1, tr=("glitch", .2))
A(T("creado_5", "cronopapel"), C("arch_crono"), 1.15, (.5, .5), 1.0, (.5, .5), tr=("deslizar", .28))
A(T("creado_5", "bitácora"), C("arch_bita"), 1.0, (.5, .5), 1.25, (.5, .5), tr=("corte", 0))
A(T("creado_5", "crónicas"), C("arch_gaming"), 1.0, (.5, .5), 1.2, (.5, .4), desde=1, vel=.8, tr=("latigo", .28))
A(T("creado_6"), C("canales"), 1.0, (.5, .5), 1.8, (.5, .42), desde=7, tr=("zoom", .36))
# cómo se hace, paso por paso sobre la sesión real
A(T("como_0"), C("vivo"), 1.0, (.5, .5), 1.7, (.4, .78), desde=4, tr=("destello", .28))
A(T("como_1"), C("mensaje"), 1.2, (.5, .7), 2.6, (.5, .77), desde=2, vel=.3, tr=("deslizar", .28))
A(T("como_2"), C("mensaje"), 2.6, (.5, .77), 3.6, (.56, .77), desde=3, vel=.3, tr=("corte", 0))
A(T("como_4"), C("como"), .78, (.5, .5), 1.0, (.5, .5), desde=1, vel=3, tr=("zoom", .36))
A(T("como_5"), C("plan"), 1.4, (.42, .6), 1.75, (.42, .62), desde=2, vel=.6, tr=("glitch", .2))
A(T("como_6"), C("como"), 1.0, (.5, .4), 1.5, (.38, .25), desde=2.2, vel=1.4, tr=("latigo", .3))
A(T("como_7"), C("escribe"), 1.0, (.5, .5), 1.6, (.28, .4), desde=3, tr=("deslizar", .28))
A(T("como_8"), C("mira"), 1.0, (.5, .5), 1.5, (.5, .5), desde=1, tr=("zoom", .36))
A(T("como_9"), C("codigo"), 1.2, (.5, .4), 1.9, (.3, .35), desde=1, vel=1.4, tr=("glitch", .2))
A(T("como_10"), C("como"), 1.0, (.5, .5), 1.0, (.5, .5), desde=20, vel=5, tr=("latigo", .3))
A(T("como_11"), C("clasico"), 2.2, (.2, .42), 2.2, (.52, .42), desde=4, vel=.3, tr=("destello", .28))
A(T("como_13"), C("lienzo"), 1.5, (.56, .5), 1.2, (.56, .5), desde=9.6, vel=.6, tr=("zoom", .36))
A(T("como_14"), C("vivo"), 1.0, (.5, .5), 1.0, (.5, .5), desde=2, vel=1.5, tr=("deslizar", .28))
# la versión dos
A(T("version_0"), C("v1"), 1.0, (.5, .5), 1.15, (.4, .5), desde=0, vel=.8, tr=("glitch", .2), ventana=False)
A(T("version_1"), C("v1"), 1.15, (.4, .5), .72, (.5, .5), desde=2.2, vel=.8, tr=("corte", 0), ventana=False)
tok(T("version_3"), 1.2, (.25, .6), 1.6, FICHA, tr=("latigo", .3))
# los errores
A(T("fallos_0"), C("mira"), 3.0, (.76, .19), 1.4, (.6, .35), desde=3, vel=.4, tr=("zoom", .36))
A(T("fallos_1"), C("mira"), 1.4, (.6, .35), 3.2, (.76, .45), desde=4, vel=.3, tr=("corte", 0))
A(T("fallos_2"), C("vivo"), 2.0, (.7, .22), 5.0, (.75, .21), desde=4, vel=.5, tr=("glitch", .2))
tok(T("fallos_3"), 1.0, (.5, .5), 1.5, FICHA, tr=("latigo", .3))
tok(T("fallos_5"), 1.5, FICHA, 1.15, (.3, .55), tr=("corte", 0))
A(T("fallos_6"), C("canales"), 1.4, (.5, .55), 1.1, (.5, .5), desde=7.5, tr=("deslizar", .28))
A(T("fallos_8"), C("clasico"), 1.1, (.5, .5), 1.5, (.5, .4), desde=5, vel=.5, tr=("zoom", .36))
A(T("fallos_10"), C("vivo"), 1.8, (.4, .75), 1.2, (.5, .55), desde=9, tr=("destello", .28))
# el relevo
A(T("relevo_0"), C("relevo"), 1.2, (.42, .75), 1.75, (.42, .78), desde=.8, vel=.5, tr=("glitch", .2))
A(T("relevo_1"), C("relevo"), 1.0, (.5, .5), 1.4, (.5, .4), desde=9.3, vel=.6, tr=("corte", 0))
A(T("relevo_2"), C("vivo"), 2.8, (.86, .585), 1.3, (.7, .6), desde=9, tr=("zoom", .36))
A(T("relevo_3"), C("relevo"), 1.0, (.5, .5), 1.7, (.42, .78), desde=11, vel=.6, tr=("latigo", .3))
tok(T("relevo_4"), 1.3, (.25, .6), 1.8, FICHA, tr=("deslizar", .28))
# la junta directiva y el corte
A(T("junta_0"), C("lienzo"), 1.25, (.56, .5), 1.7, (.56, .45), desde=10.5, vel=.5, tr=("zoom", .36))
A(T("junta_2"), C("organigrama"), 1.5, (.5, .25), 1.2, (.5, .3), tr=("destello", .28))
A(T("junta_3"), C("clasico"), 1.2, (.5, .5), 2.0, (.3, .5), desde=2, vel=.4, tr=("glitch", .2))
A(T("junta_4", "disco"), C("vivo"), 3.0, (.75, .21), 4.4, (.75, .21), desde=4, vel=.5, tr=("corte", 0))
A(T("junta_5"), C("organigrama"), 1.0, (.5, .55), 1.9, (.5, .28), tr=("latigo", .3))
A(T("junta_6"), C("vivo"), 1.0, (.5, .5), 1.7, (.86, .585), desde=2, vel=1.5, tr=("deslizar", .28))
tok(T("junta_7"), 1.0, (.5, .5), 1.6, FICHA, tr=("zoom", .36))


JEFE_FRASES = guion.JEFE


def armar():
    m = Montaje("medios/toma.mp4", TOTAL)
    for a, b in zip(_lista, _lista[1:] + [dict(ini=TOTAL)]):
        fin = b["ini"]
        m.planos.append(plano(a["clip"], a["ini"], fin, desde=a["desde"], vel=a["vel"], cam=[(a["ini"], a["z0"], *a["c0"]), (fin, a["z1"], *a["c1"])],
                              tr=a["tr"] or next(TRANS), reloj=a["clip"] == TOKEN))
        m.planos[-1]["ventana"] = a["ventana"]
    # Token en su ventanita mientras no esté a pantalla completa
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
    # el corte final: negro desde que se acaba la voz (lo pone efectos.py); y las capas por encima, si las hay
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
    if arg == "token":
        R.grabar(TOKEN, TOTAL, PLAN, pc=R.muestra_pc(cpu=82, gpu=91, temp=71, ram=74, red=9), crf=23, hasta=float(sys.argv[2]) if len(sys.argv) > 2 else None, previo=LLAVES_JS)
        print("ok", TOKEN)
    elif arg == "montaje":
        m = armar()
        print("\n".join(m.revisar()) or "planos sin huecos")
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
        while len(cs) % 3:
            cs.append(np.zeros((360, 640, 3), np.uint8))
        cv2.imwrite("previews/toma_hoja.jpg", np.vstack([np.hstack(cs[i:i + 3]) for i in range(0, len(cs), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
        print("previews/toma_hoja.jpg")
