# -*- coding: utf-8 -*-
"""Escribe busquedas.json: cada beat toma la fuente de SU escena (video de guía de ESE secreto en Forever, o paseo sin
comentarios de ESA zona) con {"url","desde"}; si no hay, búsqueda. Fuentes buscadas el 10-nov-2026 (yt-dlp ytsearch).
v3 (10-nov, sesión 3): ids de la lista de 20; nuevos Pebblebitty, Bom'bay, Mankrik, Piroleña, Sully, Terminator (CESO63j0HYA 5:05), Koiter.
Descartadas: webcams (Viktor Dlonem, plata LostNiceland), «Benedict» CyKvLBPcoEU (era un tráiler), Hearthstone.
La escena `gaia` NO se baja: su clip es el MASTER de la Crematoria con su audio (_gaia.py)."""
import json
import os
import re
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
import guion  # noqa: E402


def Y(i):
    return "https://www.youtube.com/watch?v=" + i


G, NC = "WoW Forever gameplay", "WoW Forever no commentary"
TRAILER, LAUNCH, MUD = Y("uQuKE0KDgiM"), Y("n2Wg46fwmb0"), Y("5sBZlwAjAI8")
ZEPH, LLUVIA = Y("rL6_4K8_x5A"), Y("0LeB4u9Zexs")
ELW, WEST, MUL, TIR, BAR, LOCH, DUSK, SILV, DUR, ORG = (Y(i) for i in (
    "loJCGO2MTjc", "Rbs_9GcWDDs", "hJba3NVLtz8", "UPjeg-B2vQg", "gJD03H11xis", "BxkLMXXkmU4", "LW1veoIJasc", "x-QTq9cIV7Y",
    "yipNuUNGupk", "i4yBk436p0M"))
LORD1, LORD2, LORD3 = Y("6aksHieeWZ8"), Y("qlSdF_wFj-M"), Y("1_3JTiyAixI")

SRC = {
    "intro": [(Y("uQuKE0KDgiM"), 20), (Y("n2Wg46fwmb0"), 120), (Y("5sBZlwAjAI8"), 60), (Y("eyfyyP6hGkM"), 20), (Y("UYUQHJytluk"), 120), (Y("rL6_4K8_x5A"), 600), (Y("5sBZlwAjAI8"), 200), (Y("uQuKE0KDgiM"), 60), (Y("loJCGO2MTjc"), 300)],
    "gaia": [[G]],    # marcador: el clip lo pone _gaia.py
    "gaia2": [(Y("n2Wg46fwmb0"), 400), (Y("loJCGO2MTjc"), 900), (Y("uQuKE0KDgiM"), 100)],
    "s20": [(Y("S1VbE-sk6Vc"), 30), (Y("876c0cSzy04"), 2), (Y("YbV_Z_jTAaw"), 120), (Y("S1VbE-sk6Vc"), 100), (Y("rL6_4K8_x5A"), 3000), (Y("ZcL2qAXRSPg"), 200), (Y("YbV_Z_jTAaw"), 300)],
    "s19": [(Y("RjfX3-G6mm0"), 10), (Y("BxkLMXXkmU4"), 600), (Y("RjfX3-G6mm0"), 70), (Y("Hc1Y56lu5IM"), 300), (Y("RjfX3-G6mm0"), 140), (Y("BxkLMXXkmU4"), 1800), (Y("RjfX3-G6mm0"), 200), (Y("Hc1Y56lu5IM"), 1200), (Y("BxkLMXXkmU4"), 2500)],
    "s18": [(Y("GDdB28O5fVM"), 5), (Y("cqJRCzicnV4"), 20), (Y("GDdB28O5fVM"), 30), (Y("wyV7in63CgA"), 20), (Y("GDdB28O5fVM"), 55), (Y("wyV7in63CgA"), 80), (Y("GDdB28O5fVM"), 80), (Y("wyV7in63CgA"), 150), (Y("cqJRCzicnV4"), 120), (Y("wyV7in63CgA"), 240), (Y("yipNuUNGupk"), 900)],
    "s17": [(Y("PnvIrLh7Z3k"), 3), (Y("UPjeg-B2vQg"), 500), (Y("0rcZ-n6QGQk"), 60), (Y("PnvIrLh7Z3k"), 128), (Y("-9Pt-cTGBoI"), 10), (Y("0rcZ-n6QGQk"), 200), (Y("f9VcW-70t74"), 200), (Y("PnvIrLh7Z3k"), 84)],
    "overgear": [(Y("UYUQHJytluk"), 300), (Y("ohnJW6N0-wc"), 40), (Y("xG0Ry1lUtnE"), 200), (Y("UYUQHJytluk"), 500), (Y("qlSdF_wFj-M"), 60), (Y("f2uDy4QvEDs"), 300), (Y("xG0Ry1lUtnE"), 400)],
    "s16": [(Y("Qa-js9NB-r0"), 5), (Y("bbx4V_ZGyoI"), 10), (Y("Qa-js9NB-r0"), 30), (Y("s283CyGgpXU"), 15), (Y("bbx4V_ZGyoI"), 45), (Y("s283CyGgpXU"), 50), (Y("bbx4V_ZGyoI"), 80), (Y("Qa-js9NB-r0"), 52), (Y("rL6_4K8_x5A"), 1800)],
    "s15": [(Y("BxkLMXXkmU4"), 300), (Y("BxkLMXXkmU4"), 900), (Y("Z_Q1DMtaIZE"), 600), (Y("BxkLMXXkmU4"), 1500), (Y("Z_Q1DMtaIZE"), 1500), (Y("BxkLMXXkmU4"), 2200), (Y("yH2mm248cRs"), 900), (Y("BxkLMXXkmU4"), 2900)],
    "gracias1": [(Y("loJCGO2MTjc"), 1800), (Y("JXDA_FWvdl8"), 600), (Y("n2Wg46fwmb0"), 700), (Y("loJCGO2MTjc"), 2400)],
    "s14": [(Y("2JJIMKpKgVU"), 2), (Y("gJD03H11xis"), 300), (Y("9047fa1pUWA"), 3), (Y("2JJIMKpKgVU"), 20), (Y("VhcQvnBSUPs"), 5), (Y("9047fa1pUWA"), 20), (Y("qoA-h5j1Ed0"), 60), (Y("2JJIMKpKgVU"), 40), (Y("qoA-h5j1Ed0"), 200), (Y("VhcQvnBSUPs"), 25), (Y("gJD03H11xis"), 1200), (Y("qoA-h5j1Ed0"), 400)],
    "s13": [(Y("i4yBk436p0M"), 300), (Y("i4yBk436p0M"), 900), (Y("JG7vEn0LwNQ"), 600), (Y("i4yBk436p0M"), 1600), (Y("fVo7MoXGFGg"), 600), (Y("JG7vEn0LwNQ"), 2400), (Y("i4yBk436p0M"), 2400), (Y("JG7vEn0LwNQ"), 4000)],
    "s12": [(Y("x-QTq9cIV7Y"), 600), (Y("sL7X7f8yYbQ"), 10), (Y("Z6McskqeeYM"), 10), (Y("sL7X7f8yYbQ"), 60), (Y("ophzXhk_82M"), 60), (Y("Z6McskqeeYM"), 60), (Y("sL7X7f8yYbQ"), 120), (Y("ophzXhk_82M"), 180), (Y("Z6McskqeeYM"), 120), (Y("sL7X7f8yYbQ"), 180), (Y("x-QTq9cIV7Y"), 1500)],
    "s11": [(Y("x-QTq9cIV7Y"), 300), (Y("y3cElHEMtE0"), 40), (Y("HJ63Ez3nSF4"), 60), (Y("y3cElHEMtE0"), 120), (Y("KyWNp619jyg"), 200), (Y("HJ63Ez3nSF4"), 250), (Y("x-QTq9cIV7Y"), 1800), (Y("KyWNp619jyg"), 500)],
    "burla1": [(Y("JXDA_FWvdl8"), 1500), (Y("n2Wg46fwmb0"), 1000), (Y("loJCGO2MTjc"), 3000), (Y("1bNDaUuHhQ8"), 200)],
    "s10": [(Y("lv-X0xFiR7Q"), 20), (Y("bjY79b050l8"), 5), (Y("anq70c602oc"), 5), (Y("bjY79b050l8"), 40), (Y("BrLziiYU8g0"), 5), (Y("bjY79b050l8"), 80), (Y("anq70c602oc"), 40), (Y("bjY79b050l8"), 120), (Y("anq70c602oc"), 70), (Y("bjY79b050l8"), 160), (Y("BrLziiYU8g0"), 20)],
    "s09": [(Y("lv-X0xFiR7Q"), 20), (Y("lv-X0xFiR7Q"), 120), (Y("lv-X0xFiR7Q"), 201), (Y("QLn3FvJOQbY"), 20), (Y("QLn3FvJOQbY"), 140), (Y("QLn3FvJOQbY"), 60), (Y("QLn3FvJOQbY"), 100), (Y("QLn3FvJOQbY"), 150), (Y("yV29Y3CmNZE"), 3), (Y("QLn3FvJOQbY"), 120)],
    "s08": [(Y("6aksHieeWZ8"), 20), (Y("Xo-lxZBUWnM"), 30), (Y("qlSdF_wFj-M"), 30), (Y("6aksHieeWZ8"), 240), (Y("qlSdF_wFj-M"), 170), (Y("6aksHieeWZ8"), 270), (Y("1_3JTiyAixI"), 300), (Y("6aksHieeWZ8"), 300), (Y("9jS4d0p7D6w"), 1500), (Y("qlSdF_wFj-M"), 190)],
    "s07": [(Y("6aksHieeWZ8"), 20), (Y("Xo-lxZBUWnM"), 30), (Y("qlSdF_wFj-M"), 30), (Y("6aksHieeWZ8"), 120), (Y("6aksHieeWZ8"), 160), (Y("1_3JTiyAixI"), 250), (Y("qlSdF_wFj-M"), 150), (Y("6aksHieeWZ8"), 200)],
    "gracias2": [(Y("JXDA_FWvdl8"), 2500), (Y("loJCGO2MTjc"), 2000), (Y("n2Wg46fwmb0"), 1300), (Y("uQuKE0KDgiM"), 140)],
    "s06": [(Y("VGW9QAWNkyE"), 5), (Y("hSPkzpS-ZZk"), 10), (Y("VGW9QAWNkyE"), 45), (Y("_Zo51r_hntg"), 20), (Y("VGW9QAWNkyE"), 110), (Y("VGW9QAWNkyE"), 165), (Y("hSPkzpS-ZZk"), 50), (Y("VGW9QAWNkyE"), 225), (Y("VGW9QAWNkyE"), 290), (Y("e9sZ6bgkuZo"), 60), (Y("VGW9QAWNkyE"), 350)],
    "s05": [(Y("2BLJXAAX6o8"), 3), (Y("I5nXvze90AI"), 15), (Y("2BLJXAAX6o8"), 14), (Y("k19lB_y8b8s"), 40), (Y("I5nXvze90AI"), 50), (Y("hJba3NVLtz8"), 600), (Y("k19lB_y8b8s"), 120), (Y("2BLJXAAX6o8"), 30), (Y("I5nXvze90AI"), 90), (Y("hJba3NVLtz8"), 1500)],
    "s04": [(Y("ptBP1AAkmlE"), 20), (Y("qkI4VvJ5vxo"), 10), (Y("ptBP1AAkmlE"), 70), (Y("OtORJqHGE0w"), 22), (Y("piMgXlWydpI"), 60), (Y("qkI4VvJ5vxo"), 50), (Y("OtORJqHGE0w"), 45), (Y("RtQiT1aSAPU"), 600), (Y("ptBP1AAkmlE"), 150), (Y("piMgXlWydpI"), 120)],
    "s03": [(Y("rL6_4K8_x5A"), 200), (Y("5sBZlwAjAI8"), 300), (Y("ngpcCbJos0w"), 7), (Y("wEBvDza557g"), 10), (Y("ngpcCbJos0w"), 17), (Y("2-54bi2tLXI"), 10), (Y("ngpcCbJos0w"), 26), (Y("wEBvDza557g"), 35), (Y("rL6_4K8_x5A"), 1200), (Y("5sBZlwAjAI8"), 360)],
    "s02": [(Y("eyfyyP6hGkM"), 4), (Y("LW1veoIJasc"), 300), (Y("Qx9PpY1eN7o"), 40), (Y("eyfyyP6hGkM"), 28), (Y("eyfyyP6hGkM"), 60), (Y("TI6SB3UCEFI"), 80), (Y("-CLHbA9MO4A"), 20), (Y("eyfyyP6hGkM"), 44), (Y("Qx9PpY1eN7o"), 150)],
    "s01": [(Y("JekLW8trrMc"), 2), (Y("TzJ2JRfdXyw"), 300), (Y("5sBZlwAjAI8"), 400), (Y("KeU2GDOhOmM"), 1200), (Y("rL6_4K8_x5A"), 4000), (Y("5sBZlwAjAI8"), 460), (Y("JoNXFpRjmJg"), 600), (Y("dSz-qa1iBJY"), 600), (Y("NWbh6dNV6Vg"), 1200), (Y("TzJ2JRfdXyw"), 1500), (Y("rL6_4K8_x5A"), 6000), (Y("5sBZlwAjAI8"), 520), (Y("KeU2GDOhOmM"), 2600)],
    "cierre": [(Y("rL6_4K8_x5A"), 7000), (Y("0LeB4u9Zexs"), 3000), (Y("uQuKE0KDgiM"), 160), (Y("loJCGO2MTjc"), 3300), (Y("yY9_rF1LkHY"), 900)],
}


def _norm(s):
    s = re.sub(r"\[[^\]]+\]", " ", s)
    return re.sub(r"[^a-záéíóúñü0-9]+", " ", s.lower()).strip()


FRASES = [(e["id"], _norm(f)) for e in guion.ESCENAS for f in e["frases"]]


def escena_de(texto):
    t = _norm(texto)
    for eid, f in FRASES:
        if f[:40] and f[:40] in t:
            return eid
    for eid, f in FRASES:
        if t[:30] and t[:30] in f:
            return eid
    return None


if __name__ == "__main__":
    b = json.load(open("beats.json", encoding="utf-8"))
    out, cuenta, prev = {}, {}, "intro"
    for x in b:
        eid = escena_de(x.get("texto", "")) or prev
        prev = eid
        x["_esc"] = eid
        lst = SRC[eid]
        n = cuenta.get(eid, 0)
        cuenta[eid] = n + 1
        e = lst[n % len(lst)]
        if isinstance(e, tuple):
            url, desde = e
            out[x["id"]] = {"url": url, "desde": float(desde + 25 * (n // len(lst)))}
        else:
            out[x["id"]] = e
    json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({x["id"]: x["_esc"] for x in b}, open("_beat_escena.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(out), "beats ·", ", ".join(f"{k}:{v}" for k, v in cuenta.items()))
