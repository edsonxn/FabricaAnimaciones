# -*- coding: utf-8 -*-
"""Registro de la coreografía: cada escena añade aquí cámara, territorios, actores, rutas, rótulos y sonidos."""
import math

import numpy as np

import boceto as B
import mapa as M
from core import (Act, CamPath, Fractura, Territorio, banda, contornos_tinta, estampar, kf, linea_punteada, punto_en, recortar,
                  rotulo, suavizar)
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from core import INI, FIN
from escena_base import TL


class Reg:
    def __init__(self):
        self.actores = []
        self.terr = []
        self.frac = []
        self.cam = []
        self.anios = []
        self.sellos = []
        self.fondo = []          # funciones f(img, cam, t, fs)
        self.frente = []         # funciones f(h, cam, t, fs, te)
        self.sonidos = []
        self.tinta_terr = True
        self.trans = []          # cambios de escena procedurales (trans.Transicion)
        ids = [e["id"] for e in TL["escenas"]]
        self.tcs = [(FIN(a) + INI(b)) / 2 for a, b in zip(ids, ids[1:])]      # instante de máxima cobertura de cada cambio de escena

    def fin_de(self, t0):
        """Primer cambio de escena posterior a t0: lo de una escena desaparece cuando la pintura del barrido la tapa del todo."""
        for tc in self.tcs:
            if tc > t0 + 0.15:
                return tc
        return 1e9

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

    # ---- cámara, territorio
    def camara(self, t, lon, lat, z, rot=0.0):
        self.cam.append((t, lon, lat, z, rot))

    def terreno(self, t, campo, color, dur=1.3):
        self.terr.append(dict(t=t, campo=campo, color=color, dur=dur))

    def romper(self, celdas, t0, t1, t2, t3, colores=None, **kw):
        f = Fractura(celdas, t0, t1, t2, t3, colores, semilla=len(self.frac) + 1, **kw)
        self.frac.append(f)
        return f

    def anio(self, t, valor):
        self.anios.append((t, valor))

    def sello(self, t, ch, nombre, color=(198, 52, 52)):
        self.sellos.append(dict(t=t, ch=ch, nombre=nombre, color=color))
        self.snd(t, "sello", 0.9)

    # ---- rótulos manuscritos
    def texto(self, t0, t1, txt, pos, px=72, d=0.5, geo=None, off=(0, 0), v=255, dur_sale=0.3):
        """Rótulo que se escribe en t0 y se borra en t1. pos = (x, y) de pantalla o geo = (lon, lat) con desplazamiento off."""
        def f(h, cam, t, fs, te):
            if t < t0 or t > t1 + dur_sale:
                return
            if geo is not None:
                x, y = cam.pant(*geo)
                x, y = x + off[0], y + off[1]
            else:
                x, y = pos
            u = prog(t, t0, t0 + d)
            vv = int(v * (1 - prog(t, t1, t1 + dur_sale)))
            rotulo(h, txt, x, y, px, u, fs, vv, te)
        self.frente.append(self._acot(f, t0))
        return f

    # ---- rutas y trazos sobre el mapa
    def rio(self, pts, t0, dur, color, ancho=26, tinta=True, t1=None):
        """Pincelada de guache + línea de tinta que avanza sobre un camino geográfico (lon, lat)."""
        P = suavizar(np.asarray(pts, float), 8)

        def u_de(t):
            if t1 is not None and t > t1:
                return 1 - prog(t, t1, t1 + 0.4)
            return e_inout(prog(t, t0, t0 + dur))

        def f(img, cam, t, fs):
            if t < t0 or (t1 is not None and t > t1 + 0.4):
                return
            banda(img, recortar(cam.pant_pts(P), u_de(t)), color, max(3.0, ancho * cam.z ** 0.6))
        self.fondo.append(self._acot(f, t0))
        if tinta:
            def g(h, cam, t, fs, te):
                if t < t0 or (t1 is not None and t > t1 + 0.4):
                    return
                h.trazo(recortar(cam.pant_pts(P), u_de(t)), 4.0, 11, fs, 1.0, amp=1.2)
            self.frente.append(self._acot(g, t0))
        return P

    def ruta(self, pts, t0, dur, ancho=5.0, dash=30, hueco=22, t1=None, color=None):
        P = suavizar(np.asarray(pts, float), 8)

        def g(h, cam, t, fs, te):
            if t < t0 or (t1 is not None and t > t1 + 0.4):
                return
            u = e_inout(prog(t, t0, t0 + dur))
            if t1 is not None and t > t1:
                u = 1 - prog(t, t1, t1 + 0.4)
            S = cam.pant_pts(P)
            linea_punteada(h, S, t, dash, hueco, ancho, 23, fs, u)
        self.frente.append(self._acot(g, t0))
        return P

    def camino_pos(self, P, t0, dur, ease=e_inout):
        """Función t -> (lon, lat, rumbo) de un punto que recorre el camino geográfico P."""
        Pa = np.asarray(P, float)

        def f(t):
            u = ease(prog(t, t0, t0 + dur))
            (lon, lat), ang = punto_en(Pa, max(u, 1e-4))
            return lon, lat
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

    def sello_libre(self, t0, t1, ch, x, y, px=130, rot=-0.07, color=(198, 52, 52)):
        def f(h, cam, t, fs, te):
            if t0 <= t < t1:
                from core import estampar
                v = prog(t, t0, t0 + 0.25)
                if v > 0:
                    estampar(h, ch, x, y, px * (1.5 - 0.5 * e_out(v)), rot, color, 0.05, 1)
        self.frente.append(self._acot(f, t0))
        self.snd(t0, "sello", 0.8)

    def contador(self, t0, t1, desde, hasta, pos, px=96, formato="{:,}", d=None):
        """Número que sube de `desde` a `hasta` entre t0 y t1 (rótulo manuscrito con recorte de papel)."""
        def f(h, cam, t, fs, te):
            if t < t0 - 0.2 or t > t1 + 1.6:
                return
            v = lerp(desde, hasta, e_out(prog(t, t0, t1)))
            txt = formato.format(int(v)).replace(",", ".")
            u = prog(t, t0 - 0.2, t0 + 0.2)
            vv = int(255 * (1 - prog(t, t1 + 1.0, t1 + 1.6)))
            rotulo(h, txt, pos[0], pos[1], px, u, fs, vv, te)
        self.frente.append(self._acot(f, t0))
