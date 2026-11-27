"""Receptor local mínimo para bajar clips de Flow sin ventanas de guardado.
La página de Flow (Chrome) hace fetch del blob/URL firmada y lo manda con POST /medio/<nombre> a http://127.0.0.1:18792.
Solo acepta el origen https://flow.google.com. Guarda en clips/. Se apaga tras 40 min sin novedad.
"""
import os, re, sys, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "clips")
os.makedirs(DEST, exist_ok=True)
ORIGEN = "https://flow.google.com"
ultimo = [time.time()]


class M(BaseHTTPRequestHandler):
    def _cors(self):
        if self.headers.get("Origin") == ORIGEN:
            self.send_header("Access-Control-Allow-Origin", ORIGEN)
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "content-type")
            self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        if self.headers.get("Origin") != ORIGEN:
            self.send_response(403); self.end_headers(); return
        m = re.match(r"^/medio/([A-Za-z0-9_.-]+)$", self.path)
        if not m:
            self.send_response(404); self._cors(); self.end_headers(); return
        n = int(self.headers.get("Content-Length", 0))
        datos = self.rfile.read(n)
        ruta = os.path.join(DEST, m.group(1))
        with open(ruta, "wb") as f:
            f.write(datos)
        ultimo[0] = time.time()
        print(f"recibido {m.group(1)} ({len(datos)/1e6:.1f} MB)", flush=True)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b"ok")

    def log_message(self, *a):
        pass


srv = HTTPServer(("127.0.0.1", 18792), M)


def vigila():
    while time.time() - ultimo[0] < 40 * 60:
        time.sleep(20)
    srv.shutdown()


threading.Thread(target=vigila, daemon=True).start()
print("receptor en http://127.0.0.1:18792", flush=True)
srv.serve_forever()
