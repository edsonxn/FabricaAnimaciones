# -*- coding: utf-8 -*-
"""¿Por qué se arrugan los dedos en el agua? — motor compartido nucleo/sh_motor.py + coreo.py + sonidos.py."""
import math

import sh_motor as M
from sh_motor import *  # noqa: F401,F403
from sh_motor import CLASES, _ORD  # noqa: F401

W_, H_ = M.W, M.H
M.CAMBIOS.update({
    "falso": ("pincel", 0.7, dict(ang=0.3)),
    "vasos": ("iris", 0.7, dict(cx=W_ / 2, cy=900)),
    "neumatico": ("pincel", 0.7, dict(ang=math.pi / 2)),
    "prueba": ("iris", 0.7, dict(cx=W_ / 2, cy=800)),
    "cierre": ("pincel", 0.7, dict(ang=-0.4)),
})
import coreo  # noqa: E402,F401
