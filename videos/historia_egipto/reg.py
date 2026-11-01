# -*- coding: utf-8 -*-
"""Registro de la coreografía (copia de historia_espana; Egipto usa una sola rejilla, "eg"): cada escena añade aquí cámara, territorios (por capas y por rejilla), actores, rutas, rótulos y sonidos.
Novedades respecto a Japón: capas de territorio simultáneas (Reconquista), dos rejillas ("eu" y "am") con fundido entre ellas,
ciudades con punto de tinta, rótulos de mar pintados y registro de cajas de texto para el control de choques (_qa_choques.py)."""
import math

import numpy as np

import boceto as B
import mapa as M
from core import (Act, CamPath, Fractura, Territorio, banda, contornos_tinta, estampar, kf, linea_punteada, punto_en, recortar,
                  rotulo, suavizar, _mascara_texto)
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from core import INI, FIN
from escena_base import TL


class Reg:
    def __init__(self):
        self.actores = []
        self.terr = {}           # (rejilla, capa) -> [claves]
        self.frac = []
        self.cam = []
        self.anios = []
        self.sellos = []
        self.fondo = []          # (rejilla o None, f(img, cam, t, fs))
        self.frente = []         # funciones f(h, cam, t, fs, te)  (encima de todo: rótulos, puntos de ciudad)
        self.fondo_tinta = []    # funciones f(h, cam, t, fs, te) de tinta del mapa (rutas): debajo de las pegatinas
        self.sonidos = []
        self.tinta_terr = True
        self.trans = []          # cambios de escena procedurales (trans.Transicion)
        self.rej_claves = []     # (t, dur, peso de la rejilla "am": 0 = Europa, 1 = América)
        self.cajas = []          # (t0, t1, f(t, cam) -> (x0, y0, x1, y1), etiqueta) para el control de choques
        self.mares = {"eg": []}
        ids = [e["id"] for e in TL["escenas"]]
        self.tcs = [(FIN(a) + INI(b)) / 2 for a, b in zip(ids, ids[1:])]      # instante de máxima cobertura de cada cambio de escena

    def fin_de(self, t0):
        """Primer cambio de escena posterior a t0: lo de una escena desaparece cuando la pintura del barrido la tapa del todo."""
        for tc in sorted(self.tcs):
            if tc > t0 + 0.15:
                return tc
        return 1e9

    def corte_extra(self, t):
        """Barrido dentro de una escena (p. ej. al cambiar de rejilla): también hace desaparecer lo anterior."""
        self.tcs.append(t)

    def _acot(self, f, t0):
        tf = self.fin_de(t0)

        def g(*a):
            if a[2] >= tf:
                return
            return f(*a)
        return g

    # ---- actores y sonido
    def act(self, dib, **k):
        pers = k.pop("persistente", False)
        a = Act(dib, **k)
        a.tfin = None if pers else self.fin_de(a.t_in)
        self.actores.append(a)
        return a

    def snd(self, t, nombre, vol=1.0, pan=0.0, **kw):
        self.sonidos.append((t, nombre, vol, pan, kw))

    # ---- cámara, rejilla, territorio
    def camara(self, t, lon, lat, z, rot=0.0):
        self.cam.append((t, lon, lat, z, rot))

    def rejilla(self, t, nombre, dur=0.7):
        """Desde t (fundido de dur s; 0 = de golpe, para cambiar bajo un barrido) se pinta la rejilla `nombre` ("eu" o "am")."""
        self.rej_claves.append((t, max(dur, 1e-3), 1.0 if nombre == "am" else 0.0))

    def peso_am(self, t):
        w = 0.0
        for ts, d, v in sorted(self.rej_claves):
            if t >= ts + d:
                w = v
            elif t >= ts:
                return lerp(w, v, e_inout(prog(t, ts, ts + d)))
            else:
                break
        return w

    def terreno(self, t, campo, color, dur=1.3, capa=0, rej="eu"):
        self.terr.setdefault((rej, capa), []).append(dict(t=t, campo=campo, color=color, dur=dur))

    def romper(self, celdas, t0, t1, t2, t3, colores=None, capa=0, rej="eu", **kw):
        f = Fractura(celdas, t0, t1, t2, t3, colores, semilla=len(self.frac) + 1, capa=capa, rej=rej, **kw)
        self.frac.append(f)
        return f

    def anio(self, t, valor):
        self.anios.append((t, valor))

    def sello(self, t, emblema, nombre, color=(198, 52, 52)):
        self.sellos.append(dict(t=t, ch=emblema, nombre=nombre, color=color))
        self.snd(t, "sello", 0.9)

    def mar(self, rej, txt, lon, lat, px=40, alfa=0.40, rot=0.0, color=(70, 96, 120)):
        """Nombre de mar, desierto o región pintado en el mapa (siempre visible, debajo de todo)."""
        self.mares["eg"].append((txt, lon, lat, px, alfa, rot, color))

    # ---- rótulos manuscritos
    def texto(self, t0, t1, txt, pos, px=72, d=0.5, geo=None, off=(0, 0), v=255, dur_sale=0.3, choque=True):
        """Rótulo que se escribe en t0 y se borra en t1. pos = (x, y) de pantalla o geo = (lon, lat) con desplazamiento off."""
        mw = _mascara_texto(txt, px).shape[1]
        mh = px * 1.15

        def donde(cam):
            if geo is not None:
                x, y = cam.pant(*geo)
                return x + off[0], y + off[1]
            return pos

        def f(h, cam, t, fs, te):
            if t < t0 or t > t1 + dur_sale:
                return
            x, y = donde(cam)
            u = prog(t, t0, t0 + d)
            vv = int(v * (1 - prog(t, t1, t1 + dur_sale)))
            rotulo(h, txt, x, y, px, u, fs, vv, te)
        self.frente.append(self._acot(f, t0))
        if choque:
            tf = min(t1, self.fin_de(t0))

            def caja(t, cam):
                x, y = donde(cam)
                return (x - mw / 2, y - mh / 2, x + mw / 2, y + mh / 2)
            self.cajas.append((t0 + d, tf, caja, txt))
        return f

    def ciudad(self, t0, t1, nombre, geo, txt=None, lado="arriba", px=46, d=0.45, sfx=False):
        """Punto de tinta en la ciudad (lon, lat) + su nombre manuscrito al lado."""
        lon, lat = geo

        def f(h, cam, t, fs, te):
            if t < t0 or t > t1 + 0.3:
                return
            x, y = cam.pant(lon, lat)
            u = e_back(prog(t, t0, t0 + 0.35), 2.0)
            v = int(255 * (1 - prog(t, t1, t1 + 0.3)))
            if u <= 0.02 or v <= 0:
                return
            r = 11 * u
            h.silueta(B.circ(x, y, r + 7, n=24))
            h.relleno(B.circ(x, y, r, n=20), (200, 60, 50), 3, fs, 1.0, sp=4)
            h.trazo(B.circ(x, y, r, n=24), 4.0, 5, fs, 1.0, amp=0.8, v=v)
        self.frente.append(self._acot(f, t0))
        if sfx:
            self.snd(t0, "pop", 0.35, tono=1.3)
        if txt:
            dx, dy = {"arriba": (0, -50), "abajo": (0, 52), "der": (24 + _mascara_texto(txt, px).shape[1] / 2, 0),
                      "izq": (-24 - _mascara_texto(txt, px).shape[1] / 2, 0)}[lado]
            self.texto(t0 + 0.1, t1, txt, None, px=px, d=d, geo=geo, off=(dx, dy))

    # ---- rutas y trazos sobre el mapa
    def rio(self, pts, t0, dur, color, ancho=26, tinta=True, t1=None, rej="eu"):
        """Pincelada de guache + línea de tinta que avanza sobre un camino geográfico (lon, lat)."""
        P = suavizar(np.asarray(pts, float), 8)

        def u_de(t):
            if t1 is not None and t > t1:
                return 1 - prog(t, t1, t1 + 0.4)
            return e_inout(prog(t, t0, t0 + dur))

        def f(img, cam, t, fs):
            if t < t0 or (t1 is not None and t > t1 + 0.4):
                return
            banda(img, recortar(cam.pant_pts(P), u_de(t)), color, max(3.0, ancho * (cam.z / 2.5) ** 0.6))
        self.fondo.append((rej, self._acot(f, t0)))
        if tinta:
            def g(h, cam, t, fs, te):
                if t < t0 or (t1 is not None and t > t1 + 0.4):
                    return
                h.trazo(recortar(cam.pant_pts(P), u_de(t)), 4.0, 11, fs, 1.0, amp=1.2)
            self.fondo_tinta.append(self._acot(g, t0))
        return P

    def ruta(self, pts, t0, dur, ancho=5.0, dash=30, hueco=22, t1=None, color=None, flecha=False):
        P = suavizar(np.asarray(pts, float), 8)

        def g(h, cam, t, fs, te):
            if t < t0 or (t1 is not None and t > t1 + 0.4):
                return
            u = e_inout(prog(t, t0, t0 + dur))
            if t1 is not None and t > t1:
                u = 1 - prog(t, t1, t1 + 0.4)
            S = cam.pant_pts(P)
            linea_punteada(h, S, t, dash, hueco, ancho, 23, fs, u)
            if flecha and u > 0.05:
                (x, y), ang = punto_en(S, u)
                for s_ in (-1, 1):
                    a = ang + math.pi + s_ * 0.5
                    h.trazo(np.array([(x, y), (x + 26 * math.cos(a), y + 26 * math.sin(a))]), ancho + 1, 31 + s_, fs, 1.0, amp=0.8)
        self.fondo_tinta.append(self._acot(g, t0))
        return P

    def camino_pos(self, P, t0, dur, ease=e_inout):
        """Función t -> (lon, lat) de un punto que recorre el camino geográfico P (interpolado en longitud desenvuelta)."""
        Pa = np.asarray(P, float).copy()
        Pa[:, 0] = M.U(Pa[:, 0])

        def f(t):
            u = ease(prog(t, t0, t0 + dur))
            (lu, lat), ang = punto_en(Pa, max(u, 1e-4))
            return float(M.desU(lu)), lat
        return f

    def rumbo(self, P, t0, dur, ease=e_inout):
        """Función t -> True si el punto que recorre P va hacia la izquierda (para voltear barcos y jinetes)."""
        Pa = np.asarray(P, float).copy()
        Pa[:, 0] = M.U(Pa[:, 0])

        def f(t):
            u = ease(prog(t, t0, t0 + dur))
            _, ang = punto_en(Pa, max(u, 1e-3))
            return math.cos(ang) < 0
        return f

    # ---- transformación de un dibujo en otro (contorno que se deforma, crayón que se disuelve) sobre la pantalla
    def morf(self, dibA, dibB, t0, dur, pos, sem=0, sfx=True, salida=None, t_a=None):
        """dibA se convierte en dibB entre t0 y t0+dur, en pos=(x, y, s). Devuelve el actor de dibB (entra en t0+dur)."""
        a = Act(dibA, pos=pos, t_in=(t0 - 1.0 if t_a is None else t_a), d_in=0.45, entra="pop", t_out=t0, d_out=0.01, sale="cortar", sem=sem, sfx=[(0, "pop", 0.6)])
        b = Act(dibB, pos=pos, t_in=t0 + dur, d_in=0.01, entra="fija", sem=sem + 1, t_out=salida, sale="encoger")
        a.tfin = b.tfin = self.fin_de(t0)
        self.actores += [a, b]

        def f(h, cam, t, fs, te):
            if t0 <= t < t0 + dur:
                p = {"x": pos[0], "y": pos[1], "s": pos[2]}
                B.morfosis(h, dibA, p, dibB, p, (t - t0) / dur, fs, sem, te)
        self.frente.append(self._acot(f, t0))
        if sfx:
            self.snd(t0, "morph", 0.8)
            self.snd(t0 + 0.05, "garabato", 0.5, dur=0.45)
            self.snd(t0 + dur, "pop", 0.5, tono=1.2)
        return b

    def contador(self, t0, t1, desde, hasta, pos, px=96, formato="{:,}", d=None, hasta_t=None):
        """Número que sube de `desde` a `hasta` entre t0 y t1 (rótulo manuscrito con recorte de papel)."""
        fin = t1 + 1.6 if hasta_t is None else hasta_t

        def f(h, cam, t, fs, te):
            if t < t0 - 0.2 or t > fin:
                return
            v = lerp(desde, hasta, e_out(prog(t, t0, t1)))
            txt = formato.format(int(v)).replace(",", ".")
            u = prog(t, t0 - 0.2, t0 + 0.2)
            vv = int(255 * (1 - prog(t, fin - 0.6, fin)))
            rotulo(h, txt, pos[0], pos[1], px, u, fs, vv, te)
        self.frente.append(self._acot(f, t0))
        mw = _mascara_texto(formato.format(int(hasta)).replace(",", "."), px).shape[1]
        self.cajas.append((t0, min(fin - 0.6, self.fin_de(t0)), lambda t, cam: (pos[0] - mw / 2, pos[1] - px * 0.6, pos[0] + mw / 2, pos[1] + px * 0.6), "contador"))
