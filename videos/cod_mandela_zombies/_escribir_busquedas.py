# -*- coding: utf-8 -*-
"""Escribe busquedas.json de cod_mandela_zombies (22-nov-2026). Cada beat va a la lista de SU escena (se busca su texto en guion.py);
«ID@s» = url + desde (si la escena usa el mismo ID varias veces, cada beat avanza 9 s). CITAS: el beat que CONTIENE el fin de la voz de una escena con
«post» lleva el clip de la cita alineado: desde = s_cita − (fin de la voz − t0 del beat) (CITAS abajo, segundos de investigacion.md).
VIOLENCIA: Menéndez, No Russian y Ghost cortan ANTES del disparo (No Russian: solo el ascensor).
"""
import importlib.util
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

E = {
    "intro": ["WDjR3vkOQeU@45", "kv3uNLemtvk@196", "4ojUEs--XSM@63", "Black Ops 2 Town zombies downed revive no commentary"],
    "intro_b": ["uFld4ZaGubk@60", "JX8P5vRC3_A@10", "WDjR3vkOQeU@60", "Black Ops zombies Kino der Toten gameplay no commentary"],
    "p20": ["iYkE5v8KzQw@38", "iYkE5v8KzQw@44", "Black Ops Five zombies gameplay no commentary"],
    "p20b": ["iYkE5v8KzQw@86", "Black Ops Five zombies Pentagon gameplay no commentary", "iYkE5v8KzQw@89"],
    "p19": ["UIibbSa2fLc@60", "Gorod Krovi Black Ops 3 zombies gameplay no commentary", "H-hHlX77ips@70"],
    "p19b": ["UIibbSa2fLc@100", "Gorod Krovi ending cutscene Black Ops 3"],
    "p18": ["CfvenJIR4IY@60", "OGBDdo67yn0@120", "Black Ops The Defector Hue no commentary", "Black Ops zombies map list all maps"],
    "p17": ["GbuuUuUnmsA@60", "Verruckt World at War zombies gameplay no commentary", "Verruckt dentist chair easter egg",
            "Verruckt zombies Black Ops gameplay"],
    "p16": ["s1P8DlZ09Xg@5", "Town Black Ops 2 zombies bank Speed Cola", "Remington 870 TranZit farm barn wall buy",
            "TranZit bus depot Remington wall weapon"],
    "crit1": ["Advanced Warfare press F to pay respects", "Call of Duty World at War campaign no commentary"],
    "p15": ["Quick Revive solo Black Ops zombies", "Kino der Toten solo Quick Revive", "Black Ops zombies Quick Revive machine disappears"],
    "p14": ["Type 100 Shi No Numa wall buy", "Shi No Numa World at War zombies gameplay no commentary", "Der Riese World at War zombies gameplay no commentary"],
    "p13": ["Origins zombie shield build Black Ops 2", "vd4UbrEFig8@60", "Origins Black Ops 2 zombies gameplay no commentary"],
    "p12": ["NeyIbejaePE@60", "Thundergun Kino der Toten Black Ops gameplay", "Thundergun Ascension gameplay no commentary"],
    "p11": ["JamjYnnlqJc@20", "Der Riese perk machine prone points", "Black Ops 3 prone perk machine 100 points"],
    "gracias1": ["Black Ops 2 zombies Origins gameplay no commentary", "Black Ops 2 Judgment Day no commentary"],
    "p10": ["NEGwfpVzQKc@30", "Juggernog perk machine Black Ops zombies", "Juggernog World at War Der Riese"],
    "p09": ["WbgOppGihWk@15", "WbgOppGihWk@60", "uoSdVmHJl8o@30", "Moon Black Ops zombies gameplay no commentary"],
    "p08": ["ESCEixYoqqM@0", "ESCEixYoqqM@12", "yLpwTMCm9J8@60", "Nacht der Untoten World at War gameplay no commentary"],
    "p07": ["y1jYcOon5fM@60", "no_XMUCjiW0@0", "no_XMUCjiW0@18", "no_XMUCjiW0@36", "Wk37MvzkOYA@60"],
    "crit2": ["Advanced Warfare Will Irons funeral press F", "Advanced Warfare campaign no commentary"],
    "p06": ["fXw6u6vOhEQ@3", "Town Black Ops 2 zombies Tombstone", "Black Ops 2 Town zombies gameplay no commentary"],
    "p05": ["JX8P5vRC3_A@10", "Blundergat Mob of the Dead gameplay no commentary", "Electric Cherry Blundergat",
            "Mob of the Dead Alcatraz zombies gameplay no commentary"],
    "p04": ["4ojUEs--XSM@9", "4ojUEs--XSM@63", "Black Ops 2 zombies bleed out downed no commentary"],
    "p03": ["kv3uNLemtvk@140", "kv3uNLemtvk@180", "kv3uNLemtvk@196", "fmJon_FYmWE@124", "Black Ops Numbers Kowloon no commentary"],
    "p02": ["uFld4ZaGubk@60", "gYvT_20XMy8@543", "TranZit bridge collapse bus Black Ops 2", "TranZit bus Black Ops 2 zombies gameplay"],
    "p01": ["WDjR3vkOQeU@40", "nMdC5BfC9Y4@30", "World at War Little Resistance no commentary"],
    "p01b": ["WDjR3vkOQeU@60", "WDjR3vkOQeU@70", "WDjR3vkOQeU@75", "nMdC5BfC9Y4@60"],
    "cierre": ["Black Ops zombies Kino der Toten gameplay no commentary", "World at War Nacht der Untoten gameplay no commentary",
               "Black Ops 2 Origins zombies gameplay no commentary"],
}
# CITAS (escena con post → (ID, segundo en que EMPIEZA lo que se oye)) — MEDIR con _citas.py antes de usar
CITAS = {"p20": ("iYkE5v8KzQw", 52.8), "p19": ("H-hHlX77ips", 93.7), "p01": ("WDjR3vkOQeU", 31.0)}   # medidas con _citas.py 22-nov (Nixon por volumen: «Oh my God» 52,8-56; Nikolai 93,9-99,5; voz al revés 31-34,5)


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
