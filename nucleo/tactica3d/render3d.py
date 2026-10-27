# -*- coding: utf-8 -*-
"""Renderiza una jugada en 3D (nucleo/tactica3d/grieta3d.html + three.js) a MP4 o a cuadros sueltos (27-oct-2026).

El HTML se sirve desde la raíz del proyecto con un servidor local (los módulos ES no cargan desde file://) y se dibuja en
Microsoft Edge sin ventana con la GPU (ANGLE/D3D11; Playwright no trae navegadores instalados aquí: channel="msedge").

uso:
  python nucleo/tactica3d/render3d.py <escena.json> <salida.mp4> [--fps 30]
  python nucleo/tactica3d/render3d.py <escena.json> <carpeta> --cuadros 976 984.5 990   (JPEG sueltos para revisar)
  python nucleo/tactica3d/render3d.py <escena.json> --url                                (dirección para verlo en vivo)
"""
import base64
import functools
import http.server
import os
import subprocess
import sys
import threading

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"


class _Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def servidor(puerto=0):
    h = functools.partial(_Silencioso, directory=RAIZ)
    s = http.server.ThreadingHTTPServer(("127.0.0.1", puerto), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def url_de(escena, puerto, w=1920, h=1080, extra=""):
    rel = os.path.relpath(os.path.abspath(escena), RAIZ).replace("\\", "/")
    return f"http://127.0.0.1:{puerto}/nucleo/tactica3d/grieta3d.html?escena=/{rel}&w={w}&h={h}{extra}"


def abrir(p, url, w, h):
    b = p.chromium.launch(channel="msedge", args=["--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist",
                                                   "--disable-gpu-vsync", "--disable-frame-rate-limit"])
    pg = b.new_page(viewport={"width": w, "height": h})
    pg.on("console", lambda m: m.type in ("error", "warning") and print("[navegador]", m.type, m.text))
    pg.on("pageerror", lambda e: print("[navegador] error:", e))
    pg.goto(url)
    pg.wait_for_function("window.LISTO === true || window.ERROR", timeout=120000)
    err = pg.evaluate("window.ERROR || null")
    if err:
        raise SystemExit("la escena 3D falló: " + err)
    return b, pg


def main():
    import json
    from playwright.sync_api import sync_playwright
    a = sys.argv[1:]
    escena = a.pop(0)
    fps = 30
    if "--fps" in a:
        i = a.index("--fps"); fps = int(a[i + 1]); del a[i:i + 2]
    E = json.load(open(escena, encoding="utf-8"))
    w, h = E.get("ancho", 1920), E.get("alto", 1080)
    s = servidor()
    puerto = s.server_address[1]
    if a and a[0] == "--url":
        print(url_de(escena, puerto, w, h, "&vivo=1"))
        input("Servidor activo; Enter para cerrar.")
        return
    destino = a.pop(0)
    video = E.get("modo") == "video"
    with sync_playwright() as p:
        if a and a[0] == "--cuadros":   # revisión: en modo video, con el cuadro del VOD debajo
            b, pg = abrir(p, url_de(escena, puerto, w, h, "&fondo=1" if video else ""), w, h)
            os.makedirs(destino, exist_ok=True)
            for t in map(float, a[1:]):
                d = pg.evaluate("t => window.cuadro(t)", t)
                ruta = os.path.join(destino, f"c3d_{t:.2f}.jpg")
                open(ruta, "wb").write(base64.b64decode(d.split(",", 1)[1]))
                print(ruta)
        elif video:   # capa transparente: <destino>_color.mp4 + <destino>_alfa.mp4 (la lee nucleo/tactica3d/capa.py)
            import io
            import time
            import numpy as np
            from PIL import Image
            b, pg = abrir(p, url_de(escena, puerto, w, h, "&png=1"), w, h)
            base = destino[:-4] if destino.endswith(".mp4") else destino
            def ff(ruta, fmt):
                return subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", fmt, "-s", f"{w}x{h}",
                                         "-framerate", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "14",
                                         "-pix_fmt", "yuv420p", ruta], stdin=subprocess.PIPE)
            fc, fa = ff(base + "_color.mp4", "rgb24"), ff(base + "_alfa.mp4", "gray")
            de, hasta = E["de"], E["a"]
            n = int(round((hasta - de) * fps))
            t0 = time.time()
            for i in range(n):
                d = pg.evaluate("t => window.cuadro(t)", de + i / fps)
                im = np.asarray(Image.open(io.BytesIO(base64.b64decode(d.split(",", 1)[1]))).convert("RGBA"))
                fc.stdin.write(im[..., :3].tobytes()); fa.stdin.write(im[..., 3].tobytes())
            for x in (fc, fa):
                x.stdin.close(); x.wait()
            print(f"{base}_color/_alfa.mp4: {n} cuadros en {time.time() - t0:.0f} s")
        else:
            b, pg = abrir(p, url_de(escena, puerto, w, h), w, h)
            de, hasta = E["de"], E["a"]
            n = int(round((hasta - de) * fps))
            ff = subprocess.Popen([FFMPEG, "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg",
                                   "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
                                   "-movflags", "+faststart", destino], stdin=subprocess.PIPE)
            import time
            t0 = time.time()
            for i in range(n):
                d = pg.evaluate("t => window.cuadro(t)", de + i / fps)
                ff.stdin.write(base64.b64decode(d.split(",", 1)[1]))
                if i % 150 == 0:
                    print(f"  {i}/{n} cuadros ({time.time() - t0:.0f} s)", flush=True)
            ff.stdin.close(); ff.wait()
            print(f"{destino}: {n} cuadros, {n / fps:.2f} s, en {time.time() - t0:.0f} s")
        b.close()
    s.shutdown()


if __name__ == "__main__":
    main()
