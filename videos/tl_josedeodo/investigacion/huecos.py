# -*- coding: utf-8 -*-
"""Jugadas SIN cortes (el usuario, 25-nov-2026): el VOD corre seguido a x1 y la VOZ se espacia. Para cada cadena de anclas
(momento de la voz → segundo de la fuente) calcula el silencio que falta ANTES de cada ancla para que llegue a x1 justo cuando la voz
la nombra: hueco = Δfuente − Δvoz (si Δvoz es mayor, el video PAUSA ahí: no hace falta nada). Lee timeline.json (tiempos actuales,
que ya incluyen los ESPACIOS_VOZ aplicados) y suma lo nuevo a lo que ya hay en guion.ESPACIOS_VOZ.
Las CADENAS de aquí son las mismas que usa fx_jugadas.py (CADENAS[...]): una sola fuente de verdad.
python videos/tl_josedeodo/investigacion/huecos.py            → imprime el ESPACIOS_VOZ nuevo"""
import json
import os
import re
import sys
import unicodedata

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, D)

# ancla = (tipo, frase|escena, palabra, n, segundo_fuente)   tipo: "esc" inicio de escena · "ini" inicio de frase · "w" palabra
# src None en la 1.ª ancla = «lo que haya»: el tramo anterior corre libre a x1 desde el inicio de la escena (VIVO desde VIVO0)
CADENAS = {      # 2.ª versión (25-nov): con PLAN 3D (pausa) y ÓRBITAS (pausa) = dos anclas al MISMO segundo de la fuente
    "gancho": [("esc", "gancho", None, 0, 22.0), ("w", "gancho_0", "Zest", 0, 32.6), ("w", "gancho_0", "y", 0, 35.6)],
    "blg_a": [("w", "blg_0", "Xun", 0, 15.0), ("w", "blg_0", "y", 2, 21.7), ("w", "blg_0", "roba", 0, 23.0)],                 # plan 3D en t 15 antes de «Xun»
    "blg_b": [("w", "blg_1", "minuto", 0, 30.0), ("w", "blg_1", "el", 3, 35.7), ("ini", "blg_2", None, 0, 38.0)],
    "al1_a": [("ini", "al1_1", None, 0, ("libre", "al1", 0.0)), ("w", "al1_1", "Morgan", 0, 21.2), ("w", "al1_1", "flanco", 0, 23.5)],
    "al1_b": [("w", "al1_1", "atrapa", 0, 23.5), ("w", "al1_1", "Josedeodo", 1, 26.4)],
    "al1_c": [("w", "al1_2", "Yeon", 0, 34.4), ("w", "al1_2", "triple", 0, 35.0), ("w", "al1_2", "CoreJJ", 0, 39.0),
              ("w", "al1_2", "pero", 0, 44.8), ("w", "al1_2", "Breathe", 0, 46.0), ("ini", "al1_3", None, 0, 47.0)],               # órbita en 26,4: «Josedeodo»(1) → «Yeon»
    "al1_d": [("ini", "al1_3", None, 0, 69.5), ("w", "al1_3", "alma", 0, 72.0)],                       # salto ROTULADO ACE → alma (26 s después)
    "cfo_a": [("ini", "cfo_1", None, 0, 56.0), ("ini", "cfo_2", None, 0, 56.0), ("w", "cfo_2", "Pero", 0, 61.2), ("w", "cfo_2", "Kino", 0, 61.5),
              ("w", "cfo_2", "remata", 0, 64.3)],                                                  # plan 3D en t 56 durante cfo_1
    "cfo_b": [("w", "cfo_2", "Baron", 0, 114.0), ("w", "cfo_2", "Liquid", 0, 116.0)],                  # salto ROTULADO: el Barón, 35:16
    "los2_a": [("ini", "los2_0", None, 0, 24.0), ("w", "los2_0", "Heraldo", 0, 27.0)],
    "los2_b": [("ini", "los2_1", None, 0, 27.0), ("w", "los2_1", "entra", 0, 35.0), ("w", "los2_1", "definitiva", 0, 35.5), ("w", "los2_1", "Duduhh", 0, 36.5)],
    "los2_c": [("w", "los2_1", "Y", 1, 36.5), ("w", "los2_1", "persigue", 0, 44.0), ("w", "los2_1", "y", 2, 48.9), ("w", "los2_1", "mata", 1, 49.7), ("ini", "los2_2", None, 0, 51.0)],
    "los2_d": [("ini", "los2_3", None, 0, 29.0), ("w", "los2_3", "Cataclismo", 0, 34.0), ("w", "los2_3", "cae", 0, 35.7),
               ("w", "los2_3", "Josedeodo", 0, 42.0), ("w", "los2_3", "Feisty", 0, 43.0), ("w", "los2_3", "y", 2, 62.8), ("w", "los2_3", "ancestral", 0, 64.0), ("ini", "los2_4", None, 0, 66.0)],
    "los3_a": [("ini", "los3_0", None, 0, ("libre", "los3", 0.0)), ("ini", "los3_1", None, 0, 10.0), ("w", "los3_1", "Y", 0, 14.7), ("w", "los3_1", "Josedeodo", 0, 15.0),
               ("ini", "los3_2", None, 0, 17.0)],
    "los3_b": [("ini", "los3_3", None, 0, 18.3), ("w", "los3_3", "Ackerman", 0, 21.3), ("w", "los3_3", "Zest", 0, 23.5),
               ("w", "los3_3", "doble", 0, 27.5), ("w", "los3_3", "triple", 0, 29.0), ("ini", "los3_4", None, 0, 30.5)],
}


def _n(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def cargar():
    tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
    fr = {f["key"]: f for e in tl["escenas"] for f in e["frases"]}
    es = {e["id"]: e for e in tl["escenas"]}
    return fr, es


def tiempo(a, fr, es):
    tipo, k, pal, n, _ = a
    if tipo == "esc":
        return es[k]["t0"]
    if tipo == "ini":
        return fr[k]["t0"]
    hits = [w for w in fr[k]["words"] if _n(w["w"]).startswith(_n(pal))]
    return hits[n]["s"]


def fuente_de(a, fr, es):
    s = a[4]
    if isinstance(s, tuple):            # ("libre", escena, s0): corre a x1 desde el inicio de la escena
        return s[2] + tiempo(a, fr, es) - es[s[1]]["t0"]
    return s


def huecos():
    fr, es = cargar()
    out = {}
    for nom, cad in CADENAS.items():
        for a, b in zip(cad, cad[1:]):
            dv = tiempo(b, fr, es) - tiempo(a, fr, es)
            ds = fuente_de(b, fr, es) - fuente_de(a, fr, es)
            h = round(ds - dv, 2)
            if h > .25:
                clave = b[1]
                pal = "$ini" if b[0] == "ini" else b[2]
                out.setdefault(clave, []).append((pal, b[3], h, nom))
    return out


if __name__ == "__main__":
    import guion
    act = {k: list(v) for k, v in getattr(guion, "ESPACIOS_VOZ", {}).items()}
    nuevos = huecos()
    for k, lst in nuevos.items():
        for pal, n, h, nom in lst:
            print(f"{nom:8s} {k:12s} antes de «{pal}»({n}) +{h:.2f} s")
            prev = next((i for i, x in enumerate(act.get(k, [])) if x[0] == pal and x[1] == n), None)
            if prev is None:
                act.setdefault(k, []).append((pal, n, h))
            else:
                x = act[k][prev]
                act[k][prev] = (pal, n, round(x[2] + h, 2), *x[3:])
    print("ESPACIOS_VOZ = {")
    for k in sorted(act, key=lambda k: list(guion.ESCENAS.__iter__()).index(next(e for e in guion.ESCENAS if k.rsplit('_', 1)[0] == e['id']))):
        print(f'    "{k}": {act[k]},')
    print("}")
