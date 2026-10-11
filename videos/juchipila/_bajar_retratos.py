# -*- coding: utf-8 -*-
"""Candidatos de retratos reales para Juchipila (dominio público / CC0, Wikimedia Commons) -> videos/independencia_mx/retratos/cand/
(allí los recorta nucleo/preparar_retratos.py). Con pausas para no saturar Commons."""
import os, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "FabricaAnimaciones/1.0 (proyecto educativo de videos de historia)"}
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "independencia_mx", "retratos", "cand")
C = {
 "alvarado": ["Pedro de Alvarado.JPG"],
 "mendoza": ["Retrato de Antonio de Mendoza Primer Virrey de la Nueva España en el Museo Nacional del Virreinato.jpg"],
 "lascasas": ["Bartolomé de las Casas.jpg", "Bartolomé de Las Casas.png"],
 "madero": ["Francisco I Madero-retouched.jpg", "Francisco Madero.jpg"],
 "natera": ["Panfilo Natera.jpg"],
 "villa": ["Pancho Villa bandolier (cropped).jpg", "Portrait of \"Pancho\" Villa.jpg"],
}
for k in sys.argv[1:] or list(C):
    for i, nombre in enumerate(C[k]):
        dst = os.path.join(DST, f"{k}_{i}.jpg")
        if os.path.exists(dst) and os.path.getsize(dst) > 5000:
            continue
        u = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(nombre.replace(" ", "_")) + "?width=700"
        for intento in range(5):
            try:
                data = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
                open(dst, "wb").write(data)
                print("ok", dst, len(data) // 1024, "KB", flush=True)
                break
            except Exception as e:
                print("reintento", dst, str(e)[:60], flush=True)
                time.sleep(6 * (intento + 1))
        time.sleep(2.5)
