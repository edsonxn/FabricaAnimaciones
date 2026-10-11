# -*- coding: utf-8 -*-
"""Descarga candidatos (miniaturas de 700 px de ancho, dominio público de Wikimedia Commons) a retratos/cand/. Con pausas para no saturar el servidor."""
import os, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "FabricaAnimaciones/1.0 (proyecto educativo de videos de historia)"}
C = {
 "hidalgo": ["Generalísimo Miguel Hidalgo y Costilla.png", "Miguel Hidalgo.jpg", "Miguel Hidalgo con estandarte.jpg"],
 "morelos": ["José María Morelos, siglo XIX.png", "Retrato de Morelos, 1813.png", "Mexico.JoseMariaMorelos.01.jpg"],
 "allende": ["Ignacio Allende.jpg", "Ignacio Allende by Jose Ines Tovilla.jpg"],
 "aldama": ["Juan Aldama.png"],
 "josefa": ["Josefa Ortiz, óleo sobre tela.jpg", "La Ilustre Corregidora María Josefa Ortiz de Domínguez.jpg"],
 "leona": ["Leona Vicario Mayor.PNG"],
 "iturbide": ["Iturbide Emperador by Josephus Arias Huerta.jpg", "Agustin de Iturbide.jpg"],
 "calleja": ["Virrey Félix María Calleja.jpg"],
 "napoleon": ["Napoleon I of France by Andrea Appiani.jpg", "Henri Félix Emmanuel Philippoteaux - Portrait of Napoleon Bonaparte.jpg", "Bonaparte premier Consul Gérard Chantilly.jpg"],
 "virrey": ["Viceroy José de Iturrigaray.jpg"],
 "guerrero": ["Vicente Guerrero.png", "Vicente Ramón Guerrero Saldaña.jpg"],
 "victoria": ["Le general Guadalupe Victoria (BM 1952,0517.38).jpg", "Guadalupe Victoria, 29-9-1786 - 21-3-1843 (1825).jpg"],
 "matamoros": ["Mariano Matamoros.png"],
 "galeana": ["Hermenegildo Galeana.jpg"],
 "fernando": ["Goya - Fernando VII.jpg", "Retrato de Fernando VII, Francisco de Goya.jpg"],
 "carlos": ["Carlos IV por Goya (Academia de la Historia).jpg"],
 "jose": ["Joseph-Bonaparte.jpg"],
 "mina": ["Portret van de Mexicaanse guerillaleider Francisco Javier Mina, RP-P-1905-1228.jpg", "Mina, PA03450.jpg"],
 "odonoju": ["Juan O'Donoju.jpg", "JuanODonoju.jpg"],
 "porfirio": ["Porfirio Diaz civilian.jpg", "Portrait of Porfirio Díaz.jpg"],
 "yermo": ["Gabriel J. de Yermo.PNG"],
 "garibay": ["Pedro de Garibay.jpg"],
}
sel = sys.argv[1:] or list(C)
for k in sel:
    for i, nombre in enumerate(C[k]):
        dst = f"retratos/cand/{k}_{i}.jpg"
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
