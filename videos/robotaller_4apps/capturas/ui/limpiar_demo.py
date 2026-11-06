# -*- coding: utf-8 -*-
"""Copias de las interfaces reales de Rayo y Puente TV con su anfitrión de demostración ajustado: sin IPs ni enlaces, con lo que pasó de verdad."""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
CAMBIOS = {
    "rayo/app.js": [
        (r'pc: "PC-DEMO", folder: "C:\Users\demo\Downloads\Rayo"', r'pc: "TORRE", folder: "Descargas\\Rayo"'),
        ('ip: "192.168.0.184"', 'ip: "red de la casa"'),
        ('name: "IMG_20261104_0931.jpg", size: 4.2e6, done: 4.2e6', 'name: "Escaner-2.1.apk", size: 6.1e6, done: 6.1e6'),
        ('name: "Presentación clientes.pdf", size: 18e6, done: 18e6, status: "done", speed: 0, time: "09:40"',
         'name: "Manual Puente TV.pdf", size: 1.8e6, done: 1.8e6, status: "done", speed: 0, time: "17:13"'),
        ('text: "https://clicknbusiness.com.mx/micwifi/", name: "Texto"', 'text: "¿Ya llegó?", name: "Texto"'),
        ('name: "Video boda 4K.mp4"', 'name: "robotaller_4apps_MASTER.mp4"'),
    ],
    "puente/app.js": [
        ('tvIp: "192.168.0.187"', 'tvIp: "red de la casa"'),
        ('ip: "192.168.0.187"', 'ip: "red de la casa"'),
        ('api: "http://127.0.0.1:8740"', 'api: ""'),
        ('title: "La comida está lista", status: "mostrado", style: "listo", time: "11:02"',
         'title: "La comida está lista", status: "mostrado", style: "listo", time: "12:35"'),
        ('kind: "video", title: "promo_noviembre.mp4", status: "enviando", progress: 0.62, time: "11:05"',
         'kind: "aviso", title: "¡Puente TV listo!", status: "mostrado", style: "listo", time: "12:56"'),
        ('info: "Lofi beats · reproduciendo"', 'info: "reproduciendo"'),
    ],
}
for arch, pares in CAMBIOS.items():
    ruta = os.path.join(AQUI, arch)
    s = open(ruta, encoding="utf-8").read()
    for a, b in pares:
        if a not in s:
            print("NO ESTÁ:", arch, a[:60])
        s = s.replace(a, b)
    open(ruta, "w", encoding="utf-8").write(s)
    print(arch, "192.168:", s.count("192.168"), "clicknbusiness:", s.count("clicknbusiness"))
