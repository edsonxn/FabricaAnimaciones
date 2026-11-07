# -*- coding: utf-8 -*-
"""Lote de Flow del remake ANIME de «Llamada de domingo» (6-nov-2026).
  python flow_anime.py A          -> flow/_A.js (escenarios anime + retratos de personaje)  [ingredientes = los del original]
  python flow_anime.py B          -> flow/_B.js (un cuadro por plano/toma, ingredientes = anime de la fase A por uuid)
  python flow_anime.py E          -> flow/_E.js (ediciones boca/ojos de cada toma que habla, ingrediente = su base)
En la página: pegar el .js, luego por prompt `await __prep(k)` + clic REAL en «Iniciar generación».
uuids de lo generado: flow/uuids.json {clave: [uuid_a, uuid_b, nombre_flow]} (lo llena `python flow_anime.py reg <fase>` desde
flow/_reg.txt = líneas «clave uuid»)."""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, "..", "llamada_domingo")
LOTE = json.load(open(os.path.join(ORIG, "flow", "lote.json"), encoding="utf-8"))
UUIDS = os.path.join(AQUI, "flow", "uuids.json")

FICHA = ("Hand-drawn 2D anime feature film still, mature seinen drama: clean thin dark-brown line art, flat cel-shaded "
         "characters with crisp two-tone shadows and soft rim light, realistic adult proportions and expressive faces, richly "
         "hand-painted detailed backgrounds with painterly light, glowing atmosphere, cinematic composition with depth, "
         "theatrical anime movie quality. Guadalajara and Mexico City, Mexico, a few years in the future. ")
CIERRE = " No text, no letters, no subtitles, no logos, no watermark."

ESC_FLOW = dict(taller="Empty watch repair workshop", taller_perfecto="Watch repair workshop interior",
                oficina="Empty startup office at night", depto="Modern apartment interior at night",
                plaza="Empty plaza in Guadalajara", cocina="Empty kitchen at night", porche="Porch of colorful house dusk",
                auto_lucia="Hatchback parked on Guadalajara", taxi="Taxi interior at night", pasillo="Empty hospital corridor",
                hospital="Empty hospital room at night", carretera="Modern car driving to Guadalajara",
                puerta="Closed watch-repair shop facade", puerta_dia="Don Ramón watch-repair shop stor",
                hospital_ext="Hospital exterior at night", perfecto="Minimalist living room interior",
                auditorio="Crowd in modern dark auditorium")
PJ_FLOW = dict(ramon="Don Ramón", daniel="Daniel", lucia="Lucía", ines="Inés", carmen="Doña Carmen", chuy="Don Chuy",
               mariana="Mariana")
CORTO = dict(ramon="Don Ramón (the old man with white hair and a white mustache)",
             daniel="Daniel (the man with the short black beard)",
             lucia="Lucía (the woman with the low black ponytail)",
             ines="Inés (the woman with long straight dark-brown hair)",
             carmen="Doña Carmen (the old woman with grey permed hair and round glasses)",
             chuy="Don Chuy (the stout bald old man with a thick mustache)",
             mariana="Mariana (the woman with the chestnut bob)")


def _g():
    import importlib.util
    s = importlib.util.spec_from_file_location("g", os.path.join(ORIG, "guion.py"))
    g = importlib.util.module_from_spec(s)
    s.loader.exec_module(g)
    return g


def uu():
    return json.load(open(UUIDS, encoding="utf-8")) if os.path.exists(UUIDS) else {}


# ───────────────────────────── fase A ─────────────────────────────
def fase_a():
    g = _g()
    Q = []
    for k, desc in g.ESC.items():
        if k not in ESC_FLOW:
            continue
        Q.append(dict(id=f"esc_{k}", ing=[dict(q=ESC_FLOW[k], tipo="Imagen")],
                      p=FICHA + "Redraw the place in the reference image as an EMPTY anime background painting: same layout, "
                        "same furniture and objects, same time of day and light, rich painted detail, depth from foreground "
                        f"to background. The place: {desc}. No people, no animals except what is described." + CIERRE))
    for k, desc in g.FICHA["personajes"].items():
        if k not in PJ_FLOW:
            continue
        Q.append(dict(id=f"pj_{k}", ing=[dict(q=PJ_FLOW[k], tipo="Personaje")],
                      p=FICHA + "Anime character design portrait of the person in the character reference, same face and "
                        f"identity: {desc}. Medium shot from the waist up, three-quarter view toward the camera, calm natural "
                        "expression, mouth closed, eyes open, soft warm studio light, plain softly painted warm-grey "
                        "background." + CIERRE))
    return Q


# ───────────────────────────── fase B ─────────────────────────────
_DICE = re.compile(r"([A-ZÁÉÍÓÚÑ][\wáéíóúñ]*(?: [A-ZÁÉÍÓÚÑ][\wáéíóúñ]*)?) says in Mexican Spanish, ([^:]*): \"[^\"]*\"\.?")


def limpiar(p):
    p = re.sub(r"^Cinematic 16:9 frame.*?naturalistic acting\. ", "", p)
    p = p.replace("Continuing the same conversation from the previous shot, same moment, same lighting, same clothes, the "
                  "characters stay exactly where they were. ", "")
    p = _DICE.sub(lambda m: f"{m.group(1)} is mid-conversation, {m.group(2)} expression, mouth closed in this frame.", p)
    p = re.sub(r" No on-screen text.*$", "", p)
    p = p.replace("photorealistic", "").replace("Framed as the front camera of a video call",
                                                 "Framed like the front camera of a video call")
    return p.strip()


def ing_anime(e, U):
    out = []
    for i in e["ing"]:
        if i.startswith("ESC:"):
            k = "esc_" + i[4:]
        else:
            k = "pj_" + {v: kk for kk, v in PJ_FLOW.items()}[i]
        if k in U:
            out.append(dict(uuid=U[k][0], q=U[k][2] if len(U[k]) > 2 else ""))
    return out


# tomas extra (segundo hablante de un plano, o planos sin prompt propio)
EXTRA = {
    "scene-014b": ("scene-014", ["daniel", "esc_depto"],
                   "Night, the minimalist apartment: medium close-up of Daniel on the grey sofa, looking down at his laptop, "
                   "answering without looking up, evasive, a little ashamed, mouth closed in this frame."),
    "scene-032b": ("scene-032", ["ramon", "esc_taller"],
                   "Medium close-up of Don Ramón at his workbench, the phone in his hand, glancing up at his daughter off-screen "
                   "with an absent-minded smile, mouth closed in this frame."),
    "scene-069b": ("scene-069", ["daniel", "esc_puerta"],
                   "Dusk at the closed shop door with a black mourning bow: medium close-up of Daniel, confused and worried, "
                   "carrying a gift bag, mouth closed in this frame."),
}


def fase_b():
    g = _g()
    U = uu()
    Q = []
    for e in LOTE:
        if e["kind"] not in ("clip", "llamada", "img") or e.get("copia"):
            continue
        Q.append(dict(id=e["id"], ing=ing_anime(e, U), p=FICHA + limpiar(e["prompt"]) + CIERRE))
    for k, (base, ings, txt) in EXTRA.items():
        ing = []
        for i in ings:
            kk = i if i.startswith("esc_") else "pj_" + i
            if kk in U:
                ing.append(dict(uuid=U[kk][0], q=U[kk][2] if len(U[kk]) > 2 else ""))
        desc = g.FICHA["personajes"][ings[0]]
        Q.append(dict(id=k, ing=ing, p=FICHA + f"{txt} {PJ_FLOW[ings[0]]} is {desc}." + CIERRE))
    return Q


# ───────────────────────────── fase E (ediciones) ─────────────────────────────
def quien_habla():
    """{toma: personaje que habla en ella} para las tomas con diálogo."""
    g = _g()
    q = {}
    for i, p in enumerate(g.PLANOS):
        if p["tipo"] in ("clip", "llamada") and p["dialogo"]:
            q[f"scene-{i + 1:03d}"] = p["dialogo"][0][0]
    for k, (base, ings, _) in EXTRA.items():
        q[k] = ings[0]
    return q


def fase_e(solo=None):
    U = uu()
    Q = []
    for k, pj in quien_habla().items():
        if solo and k not in solo:
            continue
        if k not in U:
            continue
        b = dict(uuid=U[k][0], q=U[k][2] if len(U[k]) > 2 else "")
        quien = CORTO[pj]
        Q.append(dict(id=f"{k}_boca", ing=[b], p=(
            "Edit this exact image. Keep EVERYTHING identical: same drawing, same framing, same pose, same lines, same colors, "
            f"same background, same lighting. The ONLY change: {quien} has the mouth open in the middle of speaking a word, "
            "lips parted showing a dark open mouth and a hint of upper teeth, like an anime lip-sync frame. Nothing else "
            "changes.")))
        Q.append(dict(id=f"{k}_ojos", ing=[b], p=(
            "Edit this exact image. Keep EVERYTHING identical: same drawing, same framing, same pose, same lines, same colors, "
            f"same background, same lighting. The ONLY change: {quien} has the eyes fully closed in the middle of a blink, "
            "upper eyelids down, mouth closed exactly as before. Nothing else changes.")))
    return Q


def js(Q, nombre):
    Q = [dict(q, p=q["p"].replace(FICHA, "~F~").replace(CIERRE, "~C~")) for q in Q]
    s = "window.__F=" + json.dumps(FICHA) + ";window.__C=" + json.dumps(CIERRE) + ";\n"
    import collections
    cnt = collections.Counter(f for q in Q for f in re.split(r"(?<=[.;]) ", q["p"]) if len(f) > 50)
    D = [f for f, c in cnt.most_common() if c >= 2]
    idx = {f: i for i, f in enumerate(D)}
    Q = [dict(q, p=" ".join(f"~{idx[f]}~" if f in idx else f for f in re.split(r"(?<=[.;]) ", q["p"]))) for q in Q]
    s += "window.__D=" + json.dumps(D, ensure_ascii=False) + ";\n"
    s += "window.__Q=" + json.dumps(Q, ensure_ascii=False, separators=(",", ":")) + ";\n"
    s += ("window.__prep=async(k)=>{const e=__Q[k]; const r=[]; for(const i of e.ing){ r.push(i.uuid? await __ingU(i.uuid,i.q||'')"
          " : await __ing(i.q,i.tipo)); } const n=await __txt(e.p.replace(/~(\d+)~/g,(m,i)=>__D[+i]).replace('~F~',__F).replace('~C~',__C)); return [k,e.id,r.join(','),n,__ningr()];};\n")
    ruta = os.path.join(AQUI, "flow", f"_{nombre}.js")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    open(ruta, "w", encoding="utf-8").write(s)
    print(ruta, len(Q), "prompts", len(s), "bytes")


def registrar(txt):
    """líneas «clave uuid_a [uuid_b] [nombre…]» → flow/uuids.json"""
    U = uu()
    for ln in open(txt, encoding="utf-8-sig").read().splitlines():
        if not ln.strip():
            continue
        pz = ln.split("\t") if "\t" in ln else ln.split(" ", 3)
        U[pz[0]] = pz[1:]
    json.dump(U, open(UUIDS, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(U), "claves")


if __name__ == "__main__":
    f = sys.argv[1]
    if f == "A":
        js(fase_a(), "A")
    elif f == "B":
        js(fase_b(), "B")
    elif f == "E":
        js(fase_e(sys.argv[2:] or None), "E")
    elif f == "reg":
        registrar(sys.argv[2])
