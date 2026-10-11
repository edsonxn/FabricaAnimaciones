# -*- coding: utf-8 -*-
"""La Luna se está yendo — motor compartido nucleo/sh_motor.py + coreo.py + sonidos.py."""
import math

import sh_motor as M
from sh_motor import *  # noqa: F401,F403
from sh_motor import CLASES, _ORD  # noqa: F401

W_, H_ = M.W, M.H
M.CAMBIOS.update({
    "unas": ("pincel", 0.7, dict(ang=0.3)),
    "espejos": ("iris", 0.7, dict(cx=W_ / 2, cy=900)),
    "dias": ("pincel", 0.7, dict(ang=math.pi / 2 + 0.2)),
    "pasado": ("iris", 0.7, dict(cx=W_ / 2, cy=1000)),
    "futuro": ("pincel", 0.7, dict(ang=-0.5)),
    "cierre": ("iris", 0.7, dict(cx=W_ / 2, cy=800)),
})
import coreo  # noqa: E402,F401
