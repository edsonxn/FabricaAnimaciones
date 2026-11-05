# Render de solo los segmentos 121-123 (363-372 s) con el código actual, en _parche/
import json, sys, time

if __name__ == "__main__":
    sys.argv = ["render", "video"]
    import render as R
    tam = 90
    json.dump(dict(nframes=R.NFRAMES, fps=R.FPS, tam=tam, w=R.W, h=R.H, preset="medium"),
              open("segmentos/info.json", "w", encoding="utf-8"))   # info.json había quedado vacío
    tareas = [(i * tam, min((i + 1) * tam, R.NFRAMES), f"_parche/seg_{i:04d}.mp4", "medium") for i in (121, 122, 123)]
    R._repartir(tareas, 3, 3, time.time())
    print("ok parche", flush=True)
