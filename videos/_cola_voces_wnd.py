# -*- coding: utf-8 -*-
"""Cola de voces de la tanda de Wild Next Door (22-oct-2026): corre el _ronda.py de cada video, uno tras otro, en la GPU.
Uso: python videos/_cola_voces_wnd.py [video ...]   Log por video en videos/<v>/_ronda.log; resumen en videos/_cola_voces_wnd.log."""
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
COLA = sys.argv[1:] or ["arana_escusado_short", "mariquitas_casa", "mariquitas_casa_short", "chinche_invierno",
                        "chinche_invierno_short", "hormigas_cocina", "hormigas_cocina_short", "telarana_rota",
                        "telarana_rota_short", "polilla_foco", "polilla_foco_short", "arana_crias", "arana_crias_short"]
LOG = os.path.join(AQUI, "_cola_voces_wnd.log")

for v in COLA:
    t0 = time.time()
    r = subprocess.run([sys.executable, "_ronda.py"], cwd=os.path.join(AQUI, v))
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M')} {v}: código {r.returncode} en {(time.time() - t0) / 60:.0f} min\n")
