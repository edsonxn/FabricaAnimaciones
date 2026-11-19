# -*- coding: utf-8 -*-
"""Escribe busquedas.json de cod_mandela3 (19-nov-2026). Cada beat va a la lista de SU escena (se busca su texto en guion.py);
«ID@s» = url + desde (si la escena usa el mismo ID varias veces, cada beat avanza 9 s). CITAS: el beat que CONTIENE el fin de la voz de una escena con
«post» lleva el clip de la cita alineado: desde = s_cita − (fin de la voz − t0 del beat) (CITAS abajo, segundos de investigacion.md).
VIOLENCIA: Menéndez, No Russian y Ghost cortan ANTES del disparo (No Russian: solo el ascensor).
"""
import importlib.util
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

E = {
    "intro": ["HiyklPTA7QE@40", "EMHd0VYb2pg@190", "Black Ops Nuketown 2010 gameplay", "Black Ops 2 Judgment Day no commentary"],
    "intro_b": ["4r-YtrYGAIQ@150", "G7vBol8wud0@80", "SDfcmo0hlqE@48", "Black Ops 7 campaign Menendez"],
    "p20": ["Modern Warfare 2 2009 intro cutscene", "Call of Duty 4 Game Over bridge no commentary",
            "Modern Warfare 2019 Kyle Garrick Gaz", "Call of Duty 4 Remastered Game Over ending"],
    "p19": ["Kino der Toten Black Ops zombies gameplay", "Max Ammo power up Black Ops zombies", "Black Ops 4 zombies Max Ammo",
            "Der Riese World at War zombies gameplay"],
    "p18": ["Modern Warfare 2 tactical nuke gameplay", "Call of Duty 4 multiplayer Crash gameplay", "Call of Duty 4 Shock and Awe nuke no commentary",
            "Call of Duty 4 multiplayer helicopter killstreak"],
    "p17": ["tc_O7NlHmZE@5", "Black Ops 1 main menu", "Black Ops main menu interrogation room"],
    "jesus": ["Modern Warfare 2 Loose Ends no commentary", "Modern Warfare 2 Endgame Shepherd no commentary"],
    "p16": ["TranZit Farm Black Ops 2 zombies gameplay", "Black Ops 2 Farm survival zombies", "TranZit bus Black Ops 2 zombies",
            "Double Tap TranZit farm barn"],
    "p15": ["KgaSo84nZLc@5", "aZj37c7ZJMM@5", "Black Ops 2 Grief zombies gameplay"],
    "p14": ["YSSDG-Cyyi8@60", "Call of Duty Ghosts Extinction gameplay", "Extinction Point of Contact Ghosts"],
    "p13": ["World at War Vendetta Stalingrad no commentary"],
    "p13b": ["World at War Their Land Their Blood no commentary"],
    "p13c": ["World at War Downfall Reichstag no commentary", "World at War Their Land Their Blood no commentary"],
    "p12": ["Black Ops One in the Chamber wager match", "Black Ops 2010 wager match gameplay"],
    "p11": ["Modern Warfare 2 Cliffhanger Ghost no commentary", "Modern Warfare 2 Takedown Ghost no commentary"],
    "p10": ["Call of Duty 2003 Captain Price campaign", "ZvfhyaBxoiY@0", "Call of Duty 2 Captain Price no commentary",
            "Call of Duty 4 Crew Expendable no commentary", "-uptI7C5Zhw@60"],
    "p09": ["lv90arMX8KU@60", "Modern Warfare 2019 Piccadilly gameplay", "bSO0CWrmWpg@30"],
    "p08": ["Nacht der Untoten World at War gameplay", "3Frj5cEjhrw@20", "Nacht der Untoten Black Ops gameplay"],
    "p07": ["Call of Duty 4 All Ghillied Up no commentary", "Call of Duty 4 Remastered All Ghillied Up"],
    "p07b": ["Call of Duty 4 main menu"],
    "p07c": ["Call of Duty 4 All Ghillied Up Pripyat no commentary", "Modern Warfare 2 Endgame Shepherd no commentary"],
    "p06": ["MP_KSkShPuk@110", "Cold War Outbreak Golova gameplay", "Black Ops Cold War Outbreak gameplay"],
    "p05": ["Ray Gun Mark II Buried gameplay", "SDfcmo0hlqE@45", "Black Ops 2 Buried zombies gameplay"],
    "p04": ["G7vBol8wud0@70"],
    "p04b": ["G7vBol8wud0@80"],
    "p04c": ["Modern Warfare 2 Remastered Takedown"],
    "p03": ["Call of Duty 4 Shock and Awe no commentary", "jB-n_8zq9Qo@40"],
    "p03b": ["4r-YtrYGAIQ@150", "Call of Duty 4 Remastered Shock and Awe"],
    "p02": ["Black Ops Nuketown 2010 gameplay", "Black Ops Nuketown mannequin easter egg", "HiyklPTA7QE@40", "ltRbTs8Hi8M@30",
            "fcWwAgqO0kg@300", "Alpha Omega Black Ops 4 zombies gameplay"],
    "p01": ["Black Ops 2 Judgment Day no commentary", "EMHd0VYb2pg@110", "EMHd0VYb2pg@190", "bVEbYbYd2ZE@622",
            "Black Ops 7 Menendez", "Black Ops 7 campaign no commentary"],
    "cierre": ["Call of Duty 4 Remastered campaign no commentary", "Black Ops zombies Kino der Toten gameplay",
               "Modern Warfare 2 Remastered campaign no commentary"],
}
# CITAS (escena con post → (ID, segundo en que EMPIEZA lo que se oye))
CITAS = {   # segundos MEDIDOS con _citas.py (Whisper, palabras con tiempo, 19-nov)
    "p13": ("2UAvWQgRRXQ", 27.7), "p13b": ("cnpYaxw8Q9A", 163.7), "p07": ("RRYmVb33VU0", 0.0), "p07b": ("pESIUgBES4Y", 0.0),
    "p04": ("G7vBol8wud0", 95.6), "p04b": ("x7vvJm9jRVU", 11.1), "p03": ("jB-n_8zq9Qo", 56.0),
}


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
