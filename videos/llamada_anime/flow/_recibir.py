# Receptor local: la página de Flow hace POST de los bytes de cada imagen (fetch con sus cookies) y aquí se guardan.
# python flow/_recibir.py  → http://127.0.0.1:8798/guardar?f=b/scene-002_0.jpg
import http.server
import os
import urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))


class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Access-Control-Allow-Local-Network", "true")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"ok")

    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        f = q["f"][0].replace("..", "")
        dst = os.path.join(BASE, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        n = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(n)
        open(dst, "wb").write(data)
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(str(len(data)).encode())

    def log_message(self, *a):
        pass


http.server.ThreadingHTTPServer(("127.0.0.1", 8798), H).serve_forever()
