# -*- coding: utf-8 -*-
"""_wowhead_ids.json de «15 FARMEOS de ORO del 30 al 50» (regla 5 de los CAMBIOS DEL KIT del 25-nov-2026: TOOLTIP REAL de Wowhead junto
a cada objeto). slug o_* → forever/<id> COMPROBADO en nether.wowhead.com/forever/tooltip (nombre inglés locale=0 y es-MX locale=11;
si Forever no trae el es-MX —sale entre corchetes— se anota el de Wowhead Classic). Toma los ids de ICONOS y EQUIPADO de _pegatinas.py.
    python _wowhead_ids.py"""
import json
import os
import re
import urllib.request

import _pegatinas as P

D = os.path.dirname(os.path.abspath(__file__))


def tt(tipo, i, loc, env="forever"):
    return json.loads(P.get(f"https://nether.wowhead.com/{env}/tooltip/{tipo}/{i}?locale={loc}"))


def main():
    out = {}
    for slug, (tipo, i, que, esc) in P.ICONOS.items():
        en, mx = tt(tipo, i, 0), tt(tipo, i, 11)
        nom = mx.get("name") or ""
        d = dict(ref=f"forever/{i}", tipo=tipo, nombre_tooltip=nom, nombre_en=en.get("name"),
                 tooltip_url=f"https://nether.wowhead.com/forever/mx/tooltip/{tipo}/{i}", icono=en.get("icon"),
                 equipado=None, fuente_equipado=None, escena=esc)
        if nom.startswith("["):
            cl = tt(tipo, i, 11, "classic").get("name")
            d["nota"] = f"Forever no trae el nombre es-MX (tooltip «{nom}»); es-MX de Wowhead Classic: «{cl}»."
        txt = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", mx.get("tooltip", "")))
        m = re.search(r"Precio de venta: ([\d ]+)", txt)
        if m:
            d["precio_venta_tooltip"] = m.group(1).strip()
        if slug in P.EQUIPADO:
            did, nota = P.EQUIPADO[slug]
            d.update(equipado=f"pegatinas/eq_{slug}.jpg",
                     fuente_equipado=f"https://wow.zamimg.com/modelviewer/classicplus/webthumbs/item/{did % 256}/{did}.png",
                     nota_equipado="visor 3D de Wowhead Forever: " + nota)
        out[slug] = d
        print(slug, d["ref"], nom, "|", d.get("precio_venta_tooltip", "-"))
    json.dump(out, open(os.path.join(D, "_wowhead_ids.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "ids")


if __name__ == "__main__":
    main()
