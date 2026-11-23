# -*- coding: utf-8 -*-
"""PRUEBA del kit de 4 estilos de Crónicas de Warcraft (nucleo/mg_wow_estilos.py, 22-nov-2026) con el MOTOR real:
cada pieza se compone sobre gameplay de wow_errores_60 con secuencia_fx.Capa.aplicar (lo mismo que hacen `fx hoja` y el
render), con su envolvente entra/sale y sus marcas.

  python prueba.py            hoja_mezcla.jpg (filas = pieza, columnas = estilo; cada pieza en su cuadro FINAL, como
                              FAB_FX_FINAL=1 fx hoja) + hoja_mezcla_anim.jpg (las mismas a media animación)
  python prueba.py --clip     clip_mezcla.mp4 (~40 s): una secuencia con el REPARTO automático (estilo=None)
"""
import os
import subprocess
import sys

import cv2
import numpy as np

NUCLEO = r"C:\FabricaAnimaciones\nucleo"
sys.path.insert(0, NUCLEO)
import mg_wow_estilos as E   # noqa: E402
import secuencia_fx as SF    # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\FabricaAnimaciones\videos\wow_errores_60"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
W, H, FPS = 1920, 1080, 30
PEG = lambda s: os.path.join(SRC, "pegatinas", s + ".png")
MAPA = lambda s: os.path.join(SRC, "mapas", s + ".jpg")
CRIST = [PEG("o_cristal_" + c) for c in ("rojo", "amarillo", "azul", "verde")]
PUNTOS_UNGORO = [E.P(43.6, 23.9, "Refugio de los Mariscales", None, PEG("refugio_mariscales")),
                 E.P(47.3, 10.8, "Bancal del Creador", "mazmorra · 58-60", PEG("bancal_creador"))]
PUNTOS_HYJAL = [E.P(68.6, 44.0, "Vuelo", "Fayran Elthas"), E.P(78.5, 36.9, "Cima de la Eternidad", "junto a Nordrassil"),
                E.P(70.6, 51.2, "Rhylin Espinapiedra", "intendente · 10 de oro", PEG("monte_hyjal"))]


class Clip:
    def __init__(self, escena, desde=0.0):
        self.cap = cv2.VideoCapture(os.path.join(SRC, "medios", escena + ".mp4"))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.desde, self.idx, self.ult = desde, -1, None

    def cuadro(self, t):
        i = min(self.n - 1, int((self.desde + max(0.0, t)) * self.fps))
        if self.ult is None or i < self.idx or i > self.idx + 60:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            self.idx = i - 1
        while self.idx < i:
            ok, f = self.cap.read()
            if not ok:
                break
            self.ult, self.idx = f, self.idx + 1
        return cv2.resize(self.ult, (W, H), interpolation=cv2.INTER_AREA)


def capa(fx):
    """Capa del motor sin video: solo lo que usa aplicar() con FX mg/pantalla de tiempos numéricos."""
    c = object.__new__(SF.Capa)
    c.fx, c.rot, c.camaras = [], [], {}
    c.paleta, c._img_cache, c._vids, c._mallas, c._rot_cache = dict(SF.PALETA), {}, {}, None, {}
    for d in fx:
        d = dict(d)
        d["de"] = float(d.pop("en", d.get("de", 0.0)))
        d["a"] = d["de"] + float(d.pop("dur")) if "dur" in d else float(d["a"])
        d["_marcas"] = [m - d["de"] for m in d.get("marcas", [])]
        c.fx.append(d)
    c.fx.sort(key=lambda d: SF.ORDEN.index(d["tipo"]))
    return c


def piezas(estilo):
    """Las 5 piezas de un estilo, cada una en su ventana de 0 a dur (marcas en s desde 0)."""
    return dict(
        mapa=[E.mapa_e(MAPA("ungoro_norte"), PUNTOS_UNGORO, 0.0, 8.0, [1.4, 3.6], "CRÁTER DE UN'GORO", "al norte del cráter",
                       estilo=estilo)],
        mapa3=[E.mapa_e(MAPA("hyjal"), PUNTOS_HYJAL, 0.0, 10.0, [1.2, 3.4, 5.6], "MONTE HYJAL", "Guardianes de Hyjal",
                        estilo=estilo)],
        ficha=[E.ficha_e("N.º 15 · Sin los 60 cristales", CRIST, 0.0, 8.0, [1.6, 2.3, 3.0, 3.7], cuentas=[15] * 4,
                         estilo=estilo)],
        tarjeta=[E.tarjeta_e(0.0, PEG("bancal_creador"), "JEFA FINAL: NANAYA", "cambia de elemento cada 25 %", dur=6.0,
                             estilo=estilo)],
        rotulo=[E.rotulo_e(0.0, "Sin cristales: solo 5 jefes", sello="5", dur=5.0, estilo=estilo)],
        pegatina=[E.peg_e(0.0, PEG("onyxia"), "Onyxia · fase 3", dur=5.0, x=.24, y=.52, estilo=estilo),
                  E.peg_e(0.3, PEG("o_cristal_rojo"), "Cristal rojo", dur=4.7, x=.78, y=.55, tam=300, estilo=estilo)],
    )


FONDO = dict(mapa=None, mapa3=None, ficha=("scene-089", 2.0), tarjeta=("scene-093", 1.0), rotulo=("scene-091", 3.0),
             pegatina=("scene-093", 6.0))
FILAS = ("mapa", "mapa3", "ficha", "tarjeta", "rotulo", "pegatina")


def cuadro(fx, t, fondo):
    c = capa(fx)
    f = np.zeros((H, W, 3), np.uint8) if fondo is None else Clip(*fondo).cuadro(t)
    return c.aplicar(f, t)


def hoja():
    mw, mh = 480, 270
    for nombre, cuando in (("hoja_mezcla.jpg", "final"), ("hoja_mezcla_anim.jpg", "anim")):
        filas = []
        for fila in FILAS:
            celdas = []
            for est in E.ESTILOS_WOW:
                c = capa(piezas(est)[fila])
                fin = max(d["a"] for d in c.fx)
                t = fin - .75 if cuando == "final" else {"mapa": 2.6, "mapa3": 4.4}.get(fila, 1.2)
                fo = FONDO[fila]
                f = c.aplicar(np.zeros((H, W, 3), np.uint8) if fo is None else Clip(*fo).cuadro(t), t)
                cv2.imwrite(os.path.join(AQUI, "cuadros", f"{fila}_{est}_{cuando}.jpg"), f, [cv2.IMWRITE_JPEG_QUALITY, 88])
                m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
                cv2.rectangle(m, (0, mh - 24), (mw, mh), (20, 18, 18), -1)
                cv2.putText(m, f"{fila} · {est} · {t:.1f}s".encode("ascii", "replace").decode(), (6, mh - 7),
                            cv2.FONT_HERSHEY_SIMPLEX, .55, (90, 214, 255), 1, cv2.LINE_AA)
                celdas.append(m)
                print(nombre, fila, est, round(t, 2), flush=True)
            filas.append(np.hstack(celdas))
        cv2.imwrite(os.path.join(AQUI, nombre), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(os.path.join(AQUI, nombre))


def clip():
    """~40 s con el REPARTO automático: dos rondas de mapa · ficha · tarjeta + rótulo · pegatinas."""
    E.reinicia()
    fx, fondos = [], []
    t = 0.0
    for ronda in range(2):
        m = E.mapa_e(MAPA("ungoro_norte" if ronda == 0 else "hyjal"), PUNTOS_UNGORO if ronda == 0 else PUNTOS_HYJAL,
                     t, t + 7.0, [t + 1.2, t + 3.2, t + 5.0], "CRÁTER DE UN'GORO" if ronda == 0 else "MONTE HYJAL", None)
        fx.append(m)
        fondos.append((t, t + 7.0, None))
        t += 7.0
        fx.append(E.ficha_e("N.º 15 · Sin los 60 cristales", CRIST, t, t + 6.0, [t + 1.4, t + 2.0, t + 2.6, t + 3.2],
                            cuentas=[15] * 4))
        fondos.append((t, t + 6.0, ("scene-089", 1.0 + ronda * 4)))
        t += 6.0
        fx.append(E.tarjeta_e(t, PEG("bancal_creador"), "JEFA FINAL: NANAYA", "cambia de elemento cada 25 %", dur=5.0))
        fx.append(E.rotulo_e(t + .8, "Sin cristales: solo 5 jefes", sello="5", dur=4.0))
        fondos.append((t, t + 5.0, ("scene-093", 1.0 + ronda * 3)))
        t += 5.0
        fx.append(E.peg_e(t, PEG("onyxia" if ronda == 0 else "cima_hyjal"), "Onyxia" if ronda == 0 else "Cima Hyjal", dur=3.5,
                          x=.25, y=.52))
        fx.append(E.peg_e(t + .4, PEG("o_cristal_azul"), "Cristal azul", dur=3.1, x=.76, y=.55, tam=300))
        fondos.append((t, t + 3.5, ("scene-091", 2.0 + ronda * 3)))
        t += 3.5
    print("reparto:", [(d["nombre"]) for d in fx])
    c = capa(fx)
    clips = {}
    salida = os.path.join(AQUI, "clip_mezcla.mp4")
    cmd = [FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-threads", "4", salida]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(t * FPS)
    for i in range(n):
        tt = i / FPS
        a, b, fo = next(x for x in fondos if x[0] <= tt < x[1])
        if fo is None:
            f = np.zeros((H, W, 3), np.uint8)
        else:
            if fo not in clips:
                clips[fo] = Clip(*fo)
            f = clips[fo].cuadro(tt - a)
        p.stdin.write(np.ascontiguousarray(c.aplicar(f, tt)).tobytes())
        if i % 150 == 0:
            print(f"cuadro {i}/{n}", flush=True)
    p.stdin.close()
    p.wait()
    print(salida)


if __name__ == "__main__":
    os.makedirs(os.path.join(AQUI, "cuadros"), exist_ok=True)
    clip() if "--clip" in sys.argv else hoja()
