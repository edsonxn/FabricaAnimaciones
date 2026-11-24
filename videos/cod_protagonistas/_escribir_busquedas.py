# -*- coding: utf-8 -*-
"""Escribe busquedas.json de cod_protagonistas (24-nov-2026). Cada beat va a la lista de SU escena (se busca su texto en guion.py);
«ID@s» = url + desde (si la escena usa el mismo ID varias veces, cada beat avanza 9 s). CITAS: el beat que CONTIENE el fin de la voz de una escena con
«post» lleva el clip de la cita alineado: desde = s_cita − (fin de la voz − t0 del beat) (CITAS abajo, segundos de investigacion.md).
VIOLENCIA: Menéndez, No Russian y Ghost cortan ANTES del disparo (No Russian: solo el ascensor).
"""
import importlib.util
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

E = {
    "intro": ["ovN5k_l_MLA@12", "A_mZFP4484k@200", "tzhfsgRFMLw@20", "VpB_6nTB4qA@20", "zqg3F3K_dBw@2"],
    "intro_b": ["08lofXPcpPs@2860", "rMYWDBurwOY@20", "mv7Y5T2oq-Q@60", "Modern Warfare 4 campaign no commentary"],
    "p20": ["rMYWDBurwOY@0", "7kM9K8bNiF4@60", "Infinite Warfare Operation Blood Storm no commentary", "DJ84zMOAz0k@60"],
    "p19": ["4Ric1SLBmow@0", "l-c2ii3bov8@520", "Call of Duty Ghosts The Ghost Killer no commentary"],
    "p18": ["Xe7h68YkbUc@0", "ZPfkeaDO9OA@300", "Modern Warfare 2019 Into the Furnace no commentary"],
    "p17": ["_EcKJ5WEua4@0", "UTwHXnoNk1w@0", "Call of Duty 4 Aftermath no commentary"],
    "p16": ["Ajr_XayCA_w@20", "Call of Duty 4 The Coup no commentary"],
    "crit1": ["Modern Warfare 2 2022 campaign no commentary", "Modern Warfare II 2022 Alone mission no commentary"],
    "p15": ["Modern Warfare 2 Takedown no commentary", "Modern Warfare 2 Cliffhanger no commentary", "6-Kx-xxqjOI@0"],
    "p14": ["Modern Warfare 3 Blood Brothers no commentary", "sS_wS5uhynk@0", "y0yJU_hR8ZE@400"],
    "p13": ["m7-bmyuXduo@380", "n7hVACRHilc@420", "Black Ops 6 Checkmate no commentary"],
    "p12": ["VpB_6nTB4qA@0", "j4kFReFL2PQ@0", "gAN7QecQa9g@60", "Black Ops 7 campaign no commentary"],
    "p11": ["argiGmyg-_Y@60", "9SRL__ZJgsg@0", "Modern Warfare 2 Loose Ends no commentary"],
    "p11b": ["argiGmyg-_Y@300", "Modern Warfare 2 Loose Ends boneyard no commentary"],
    "p10": ["ovN5k_l_MLA@62", "A_mZFP4484k@220", "Modern Warfare 2 2022 Ghost Team no commentary", "iF-p-BaQBY4@0"],
    "p09": ["GeEEN0tuSn0@900", "zqg3F3K_dBw@0", "Black Ops Vorkuta no commentary"],
    "p09b": ["Black Ops Rebirth Reznov no commentary", "Black Ops Vietnam Reznov no commentary", "Black Ops Revelations Hudson Mason"],
    "p08": ["kA6qjpZjm7c@200", "Call of Duty 4 Game Over bridge no commentary", "6gFlUmjZb5U@150"],
    "p08b": ["6gFlUmjZb5U@245", "RmFHWr4iDY4@250"],
    "p07": ["Black Ops Payback Woods Kravchenko", "VpB_6nTB4qA@40", "gAN7QecQa9g@200", "Black Ops Cold War campaign no commentary"],
    "p06": ["8N7joopqLjI@0", "-UO3mDVwTl8@0", "Black Ops Cold War Final Countdown no commentary"],
    "p06b": ["TuaNtEAv6Z8@50", "Black Ops Cold War campaign no commentary"],
    "p05": ["NjQyih6O_5o@1300", "-fqjOgHRMRM@1400", "LzHkh3NJloQ@0", "Black Ops 2 Panama no commentary"],
    "p04": ["Black Ops 3 New World surgery cutscene", "KUHPa-vtJ6c@0", "08lofXPcpPs@2880", "Black Ops 3 campaign no commentary"],
    "crit2": ["mv7Y5T2oq-Q@30", "Modern Warfare 4 Archer cutscene"],
    "p03": ["tzhfsgRFMLw@15", "ak3a2kfdTb4@60"],
    "p03b": ["tzhfsgRFMLw@85", "Call of Duty 4 Game Over bridge no commentary", "ak3a2kfdTb4@200"],
    "p02": ["A_mZFP4484k@0", "qA2tBC5A7Xc@600", "1p18qB5xIh0@900"],
    "p02b": ["A_mZFP4484k@200", "vJLmI977rzU@60", "Modern Warfare 3 2023 Trojan Horse no commentary"],
    "p01": ["I-UWtfhJuYs@600", "mv7Y5T2oq-Q@0", "Modern Warfare 4 Greater Good no commentary"],
    "p01b": ["ovN5k_l_MLA@62", "4Xpc98CnSZI@0", "iF-p-BaQBY4@0", "Call of Duty 1 Battleship Tirpitz no commentary", "Call of Duty 4 Modern Warfare Price no commentary"],
    "cierre": ["Modern Warfare 4 campaign no commentary", "Black Ops campaign no commentary", "Modern Warfare 2 campaign no commentary"],
}
# CITAS (escena con post → (ID, segundo en que EMPIEZA lo que se oye)) — MEDIR con _citas.py antes de usar
CITAS = {"p11": ("0JEWoxV8ltE", 7.9), "p09": ("zqg3F3K_dBw", 17.9), "p08": ("6gFlUmjZb5U", 236.8), "p06": ("7kXDPU7LdnY", 52.0), "p03": ("tzhfsgRFMLw", 47.6), "p02": ("A_mZFP4484k", 193.7), "p01": ("ovN5k_l_MLA", 48.9)}   # medidas con _citas.py (Whisper medium) 24-nov


def main():
    spec = importlib.util.spec_from_file_location("g", os.path.join(AQUI, "guion.py"))
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
    tl = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
    fin_voz = {e["id"]: float(e["frases"][-1]["t1"]) for e in tl["escenas"]}   # fin real de la última frase
    textos = {e["id"]: " ".join(f.split("] ")[-1] for f in e["frases"]) for e in g.ESCENAS}

    def escena(t):
        cab = t.strip()[:40]
        for k, v in textos.items():
            if cab in v:
                return k
        return None

    out, usos, ult = {}, {}, {}
    actual = "intro"
    for b in beats:
        actual = escena(b["texto"]) or actual
        b["_esc"] = actual
        ult[actual] = b["id"]
    # el beat de la cita es el que CONTIENE el fin de la voz (el hueco «post»), no el último que empieza con su texto
    cbeat = {next(b["id"] for b in beats if float(b["t0"]) <= fin_voz[k] < float(b["t1"])): k for k in CITAS}
    for b in beats:
        k = b["_esc"]
        lista = E[k]
        n = usos.get(k, 0)
        usos[k] = n + 1
        v = lista[n % len(lista)]
        if b["id"] in cbeat:
            k = cbeat[b["id"]]
            vid, s = CITAS[k]
            desde = max(0.0, s - (fin_voz[k] - float(b["t0"])))
            out[b["id"]] = {"url": "https://youtu.be/" + vid, "desde": round(desde, 2)}
            print(f"cita {k}: {b['id']} t0={b['t0']:.2f} fin_voz={fin_voz[k]:.2f} -> {vid}@{desde:.2f}")
        elif "@" in v:
            vid, s = v.split("@")
            out[b["id"]] = {"url": "https://youtu.be/" + vid, "desde": float(s) + 9 * (n // len(lista))}
        else:
            out[b["id"]] = [v] + [x for x in lista if "@" not in x and x != v][:2]
    json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(out), "beats")


if __name__ == "__main__":
    main()
