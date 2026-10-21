# -*- coding: utf-8 -*-
"""Anuncio de Dúo (60 s, vertical): la interfaz de la app dibujada por código (kit duo.py), en plano secuencia.
Todas las escenas del guion usan `Mundo`, que dibuja el cuadro completo en función del tiempo global:
  e_intro.py   gancho (la sala de noche, cada quien en su celular) -> logo
  e_medida.py  misiones a la medida + «Estamos a distancia» + videollamada
  e_juegos.py  pestaña Juegos: turnos, ¿Qué tanto me conoces?, Dibújalo, Torre al cielo, 4 en línea, Asalto al cochinito
  e_hogar.py   Nuestro hogar (casa isométrica que se decora con monedas) + huerto que crece y se riega
  e_ciclo.py   Mi ciclo / Ciclo de Ana (guía para acompañar, embarazo) + cierre con logo, botón e insignias
Los sonidos (SFX de ElevenLabs) NO pasan por `ev`: los ancla `fx_audio.py` a las mismas palabras y los deja en audio/fx.wav."""
import e_ciclo as EC
import e_hogar as EH
import e_intro as EI
import e_juegos as EJ
import e_medida as EM
from duo import TOTAL, P, acabado, fondo_duo, golpe, pr, smooth
from escena_base import Escena


def camara(t):
    if t < EM.T1:
        return EM.camara(t)
    if t < EJ.T1:
        return EJ.camara(t)
    if t < EH.T1:
        return EH.camara(t)
    return EC.camara(t)


def cuadro(t):
    p = P()
    cam = camara(t)
    noche = 1 - smooth(pr(t, EI.h_duo - 0.2, EI.h_duo + 0.5))
    fondo_duo(p, t, dx=-(cam.cx - 540) * 0.30 * cam.z, dy=-(cam.cy - 960) * 0.25 * cam.z, fuerza=1 - 0.45 * noche,
              motas=1 - 0.7 * noche, calida=smooth(pr(t, EC.T_CI - 0.4, EC.T_CI + 0.6)))
    EI.intro(p, t)
    EM.telefonos(p, t)
    EM.frente(p, t)
    EJ.dibujar(p, t)
    EH.dibujar(p, t)
    EC.dibujar(p, t)
    flash = (0.10 * golpe(t, EI.h_duo, 0.45) + 0.08 * golpe(t, EJ.r_coch + 0.1, 0.4) + 0.06 * golpe(t, EJ.c_lin + 0.2, 0.4)
             + 0.08 * golpe(t, EC.c_duo - 0.05, 0.45))
    img = acabado(p.im, t, flash=flash, sacudida=0.6 * golpe(t, EJ.r_coch + 0.1, 0.4))
    img *= smooth(pr(t, 0.0, 0.3))
    img *= 1.0 - smooth(pr(t, TOTAL - 0.35, TOTAL))
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


from escena_base import TL  # noqa: E402

CLASES = {e["id"]: Mundo for e in TL["escenas"]}
