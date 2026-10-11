# -*- coding: utf-8 -*-
import sys, time, json
sys.path.insert(0, ".")
from _buscar_retratos import buscar
Q = {
 "leona": ["Leona Vicario", "Leona Vicario portrait"],
 "napoleon": ["Napoleon Bonaparte portrait", "Napoleon Ingres throne"],
 "virrey": ["José de Iturrigaray", "Iturrigaray virrey retrato"],
 "guerrero": ["Vicente Guerrero retrato", "Vicente Guerrero portrait"],
 "victoria": ["Guadalupe Victoria retrato", "Guadalupe Victoria portrait"],
 "matamoros": ["Mariano Matamoros", "Matamoros retrato insurgente"],
 "galeana": ["Hermenegildo Galeana", "Galeana retrato insurgente"],
 "fernando": ["Fernando VII Goya", "Fernando VII retrato"],
 "carlos": ["Carlos IV Goya"],
 "jose": ["José Bonaparte rey de España retrato", "Joseph Bonaparte portrait"],
 "mina": ["Francisco Xavier Mina retrato", "Francisco Javier Mina portrait"],
 "odonoju": ["Juan O'Donojú", "O'Donojú retrato"],
 "porfirio": ["Porfirio Díaz retrato", "Porfirio Diaz portrait"],
 "jimenez": ["Mariano Jiménez insurgente", "Mariano Jimenez retrato"],
 "abasolo": ["Mariano Abasolo retrato"],
 "yermo": ["Gabriel de Yermo"],
 "garibay": ["Pedro de Garibay virrey"],
 "dominguez": ["Miguel Domínguez corregidor retrato"],
}
res = {}
for k, qs in Q.items():
    res[k] = []
    for q in qs:
        for intento in range(4):
            try:
                r = buscar(q, 7)
                res[k] += r
                break
            except Exception as e:
                time.sleep(8 * (intento + 1))
        time.sleep(3.5)
    print("##", k)
    seen = set()
    for t, w, h, lic, u in res[k]:
        if t in seen: continue
        seen.add(t)
        print(f"  {t[:95]} | {w}x{h} | {lic}")
json.dump(res, open("retratos/_busqueda.json", "w", encoding="utf-8"), ensure_ascii=False)
