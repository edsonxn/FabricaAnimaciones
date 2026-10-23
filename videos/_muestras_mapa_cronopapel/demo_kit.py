# Demo del formato elegido (22-oct-2026) con el kit REAL de Cronopapel (escenas.py de historia_aguascalientes + nucleo/crono_ubicacion):
# apertura México entero -> zoom al estado (fronteras, vecinos, minimapa, cartela, escala) -> región con todos los estados.
# uso (desde videos/historia_aguascalientes):
#   PYTHONPATH="<esta carpeta>;<historia_aguascalientes>;C:\FabricaAnimaciones\nucleo" python ..\_muestras_mapa_cronopapel\demo_kit.py hoja|video
import os
import subprocess
import sys
from multiprocessing import Pool

import cv2
import numpy as np

SAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida")
DUR, FPS = 17.0, 30
_E = None


def kit():
    global _E
    if _E is None:
        import guion
        guion.UBICACION = {"prota": "MX-AGU", "subtitulo": "centro-norte de México"}
        import core
        import escenas as E
        E.ACTORES[:] = []
        E.SELLOS[:] = []
        E.R.anios[:] = []
        E.R.frente[:] = []
        E.R.fondo_tinta[:] = []
        E.R.fondo[:] = []
        E.R.trans[:] = []
        E.CAPAS.clear()
        E.CAM = core.CamPath([(0, -102.33, 22.0, 1.25), (6.0, -102.33, 22.0, 1.25), (10.8, -102.30, 21.98, 1.4),
                              (13.0, -102.0, 21.5, 0.40), (17.0, -101.95, 21.45, 0.38)])
        E.R.ubic.cam_fn = E.CAM.estado
        E.R.ubic.apertura(0.0, 6.0, quieto=2.0, fundido=0.01, estado=6.2)
        E.R.ubic.region(11.0, DUR + 1, extra=[("Guadalajara", -103.35, 20.67), ("León", -101.68, 21.12)])
        _E = (E, E.Mundo(E.TL["escenas"][0], 0))
    return _E


def cuadro(t):
    E, m = kit()
    im = m.render(None, t)
    return (np.clip(im, 0, 1)[..., ::-1] * 255).astype(np.uint8)


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "hoja"
    if modo == "hoja":
        ts = [0.5, 2.6, 3.6, 4.4, 5.2, 6.0, 8.5, 11.3, 12.2, 16.5]
        tiles = []
        for t in ts:
            s = cv2.resize(cuadro(t), (640, 360), interpolation=cv2.INTER_AREA)
            cv2.putText(s, f"{t:.1f}", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            tiles.append(s)
            if t in (8.5, 16.5, 3.6):
                cv2.imwrite(os.path.join(SAL, f"demo_{t:04.1f}.jpg"), cuadro(t), [cv2.IMWRITE_JPEG_QUALITY, 90])
        while len(tiles) % 3:
            tiles.append(np.zeros_like(tiles[0]))
        cv2.imwrite(os.path.join(SAL, "demo_hoja.jpg"), np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]))
    else:
        out = os.path.join(SAL, "demo_apertura_estado_region.mp4")
        ff = subprocess.Popen(["C:/ffmpeg/bin/ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080",
                               "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out], stdin=subprocess.PIPE)
        ts = [i / FPS for i in range(int(DUR * FPS))]
        with Pool(8) as p:
            for k, fr in enumerate(p.imap(cuadro, ts, chunksize=4)):
                ff.stdin.write(fr.tobytes())
                if k % 60 == 0:
                    print(k, flush=True)
        ff.stdin.close()
        ff.wait()
        print("ok", out)
