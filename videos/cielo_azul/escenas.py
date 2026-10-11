# -*- coding: utf-8 -*-
"""¿Por qué el cielo es azul? — motor compartido nucleo/sh_motor.py + coreo.py + sonidos.py."""
import math

import sh_motor as M
from sh_motor import *  # noqa: F401,F403
from sh_motor import CLASES, _ORD  # noqa: F401

W_, H_ = M.W, M.H
M.CAMBIOS.update({
    "blanca": ("pincel", 0.7, dict(ang=0.3)),
    "dispersion": ("iris", 0.7, dict(cx=W_ / 2, cy=900)),
    "violeta": ("pincel", 0.7, dict(ang=math.pi / 2)),
    "atardecer": ("iris", 0.7, dict(cx=W_ / 2, cy=1100)),
    "marte": ("pincel", 0.7, dict(ang=-0.5)),
    "cierre": ("iris", 0.7, dict(cx=W_ / 2, cy=900)),
})
import coreo  # noqa: E402,F401
