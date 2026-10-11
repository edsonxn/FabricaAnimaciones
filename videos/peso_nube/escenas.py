# -*- coding: utf-8 -*-
"""¿Cuánto pesa una nube? — motor compartido nucleo/sh_motor.py + coreo.py + sonidos.py."""
import math

import sh_motor as M
from sh_motor import *  # noqa: F401,F403
from sh_motor import CLASES, _ORD  # noqa: F401

W_, H_ = M.W, M.H
M.CAMBIOS.update({
    "peso": ("pincel", 0.7, dict(ang=0.3)),
    "gotas": ("iris", 0.7, dict(cx=W_ / 2, cy=700)),
    "aire": ("pincel", 0.7, dict(ang=math.pi / 2)),
    "lluvia": ("iris", 0.7, dict(cx=W_ / 2, cy=600)),
    "cierre": ("pincel", 0.7, dict(ang=-0.4)),
})
import coreo  # noqa: E402,F401
