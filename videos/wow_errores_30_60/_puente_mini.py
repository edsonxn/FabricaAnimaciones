# -*- coding: utf-8 -*-
"""Puente local con CORS para la miniatura en Flow (11-nov-2026): GET /<archivo> sirve miniatura_ing/, POST /guardar/<nombre>
guarda el cuerpo en miniatura_ing/opciones/<nombre>. python _puente_mini.py  (puerto 8799)"""
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "miniatura_ing")
os.makedirs(os.path.join(D, "opciones"), exist_ok=True)


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        p = os.path.join(D, os.path.basename(self.path.split("?")[0]))
        if not os.path.isfile(p):
            self.send_response(404)
            self._cors()
            self.end_headers()
            return
        b = open(p, "rb").read()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "image/png" if p.endswith(".png") else "image/jpeg")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        n = os.path.basename(self.path)
        b = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        open(os.path.join(D, "opciones", n), "wb").write(b)
        self.send_response(200)
        self._cors()
        self.end_headers()
        self.wfile.write(b"ok")


ThreadingHTTPServer(("127.0.0.1", 8799), H).serve_forever()
