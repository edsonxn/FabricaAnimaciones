# -*- coding: utf-8 -*-
"""Lote de Flow de «Llamada de domingo» (6-nov-2026): compone flow/lote.json con TODO lo que se pide en Flow.
  python videos/llamada_domingo/flow_lote.py        -> flow/lote.json + resumen
Entradas: kind = esc (imagen de escenario, ingrediente de los clips) · img (beat de imagen) · bg (fondo para ui.py) ·
clip / llamada (video con diálogo). `ing` = ingredientes por nombre en Flow (personajes) + «ESC:<lugar>» (imagen de escenario).
Cada entrada lleva `out`: dónde se guarda (medios/scene-NNN.jpg|mp4, flow/esc/<lugar>.jpg, flow/bg/<id>.jpg)."""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import guion as g  # noqa: E402

F = g.FICHA
NOM = F["nombres"]
SIN_TEXTO = "No on-screen text, no subtitles, no captions, no logos, no watermark."

# Beats de imagen: lo que se ve (en inglés) · «=esc» = se usa la imagen del escenario tal cual
IMG = {
    "ext_relojeria": "=puerta_dia",
    "ramon_radio": "Medium shot: Don Ramón turns the knob of the old wooden radio on the shelf with a hopeful face, looking "
                   "at the silent yellow canary in its white wire cage by the window.",
    "ext_auditorio": "The glass facade of a huge modern convention center in Mexico City at night, a crowd entering, a giant "
                     "warm glowing abstract circular light sculpture above the entrance, wet pavement reflecting the lights.",
    "daniel_laptop": "Late night, wide shot: Daniel sits alone on the grey sofa lit only by the cold glow of the laptop on his "
                     "knees; behind him, out of focus, Inés sleeps on the other end of the sofa under a blanket.",
    "plaza": "=plaza",
    "carmen_duda": "Medium close-up: Doña Carmen sits at the dominoes table in the plaza looking down at the phone in her "
                   "hand; her smile is slowly fading into doubt.",
    "lucia_llega": "Lucía, in her nurse scrubs and open grey cardigan, arrives at the open door of the watch-repair shop "
                   "carrying two grocery bags and a weekly plastic pill organizer, tired but smiling.",
    "cocina": "=cocina",
    "carmen_sola": "Night. Doña Carmen sits alone at the kitchen table under the single hanging lamp, her glasses in her "
                   "hand, the phone lying face down next to the sugar bowl, the round wall clock behind her.",
    "ramon_duda": "Night, only the magnifying lamp is on: Don Ramón sits at his workbench holding the phone in both hands, "
                  "looking at the dark screen, doubtful and worried.",
    "ext_hospital": "=hospital_ext",
    "cama_vacia": "Dawn light: the hospital bed is empty, the sheets pulled back, the heart monitor turned off; on the "
                  "bedside table the old gold pocket watch lies open, stopped.",
    "puerta": "=puerta",
    "daniel_roto": "Close-up at dusk at the shop door: Daniel's face crumbles, eyes full of tears, mouth half open, the "
                   "black mourning bow out of focus behind him.",
    "reloj_grabado": "Extreme close-up on the wooden workbench: the old gold pocket watch with its lid open, polished and "
                     "repaired, ticking; the inside of the lid is engraved in elegant cursive with the words «Para el que "
                     "viene».",
}

# Fondos fotográficos para las piezas por código (ui.py)
VALERIA = ("Valeria Roca, an elegant 45-year-old Mexican woman with a sleek black low bun, a white minimalist suit and a "
           "thin headset microphone")
BG = {
    "key_sala": ("auditorio", f"Wide shot from the back of a dark huge auditorium at a tech launch: thousands of people "
                 f"in silhouette, a giant blank warm-white LED screen above the stage, and {VALERIA} small on the stage in a "
                 "spotlight. The giant screen is completely blank."),
    "key_valeria": ("auditorio", f"Medium shot from the side of the stage: {VALERIA}, walking calmly on the stage in a "
                    "soft spotlight, gesturing with one open hand toward the audience, seen in profile, mouth closed."),
    "key_publico": ("auditorio", "Close shot of the audience in a dark auditorium: faces of people of different ages lit "
                    "by the warm light of a giant screen, some moved, a woman touching her chest."),
    "key_valeria2": ("auditorio", f"Wide shot of the stage from the audience: {VALERIA} stands alone in the center in a "
                     "golden spotlight, arms open, a standing ovation in silhouette in the foreground, confetti of light."),
    "anu_1": (None, "A bright warm commercial: a 75-year-old Mexican grandmother laughs with joy at a video call on a "
              "tablet in her sunny kitchen with colorful talavera tiles."),
    "anu_2": (None, "A bright warm commercial: a 35-year-old Mexican man in a business suit walks fast through an airport "
              "terminal with a carry-on, relieved and smiling at his phone."),
    "anu_3": (None, "A bright warm commercial: an elderly Mexican man on a sunny porch with a straw hat smiles proudly "
              "while talking to his phone held at arm's length for a video call."),
    "anu_4": (None, "A bright warm commercial: a young Mexican woman in a modern office leans back in her chair and "
              "closes her eyes peacefully, a cup of coffee in her hand, the city behind the glass."),
    "mon_1": ("taller", "Morning: Don Ramón eats breakfast at a small table in a corner of his workshop, the phone propped "
              "against a coffee cup for a video call, laughing with his mouth open."),
    "mon_2": ("plaza", "Afternoon in the plaza: Don Ramón proudly shows his phone screen to two neighbors at the dominoes "
              "table, beaming."),
    "mon_3": ("taller", "Don Ramón waters potted plants by the window of his workshop while talking happily into the "
              "phone held in his other hand, sunlight on his face."),
    "mon_4": (None, "Night: Don Ramón lies in his old wooden bed in a simple bedroom with a crucifix on the wall, the phone "
              "glowing in his hands for a video call, smiling tenderly, a bedside lamp."),
    "mon_5": ("taller", "Don Ramón at his workbench polishes the old gold pocket watch, the phone propped in front of him "
              "on a video call, talking and gesturing with the tiny screwdriver, very happy."),
    "noti_1": (None, "A crowded Mexico City metro car: many passengers of all ages look at their phones, some smiling at "
               "video calls, cold fluorescent light."),
    "noti_2": (None, "A sunny residential home for the elderly in Mexico: several elderly people in armchairs each talk to "
               "a tablet with a video call, smiling, a nurse walks by."),
    "noti_3": (None, "The plenary hall of the Mexican Senate in session, senators voting, a big electronic voting board "
               "glowing green, wide shot."),
    "noti_estudio": (None, "An empty modern TV news studio set with a sleek desk, blue and white light, a huge video wall "
                     "behind the desk that is completely blank, no people."),
    "fiesta": ("oficina", "Night, an office party in the glass startup office: colleagues laugh with drinks and balloons; "
               "in the center Daniel, smiling, holds a glass in one hand and glances at his phone in the other."),
    "oficina_dia": ("oficina", "Daytime: Daniel sits alone at his desk in the glass office, sunlight, the city behind the "
                    "glass, looking down at the phone in his hand with an empty, faint smile."),
    "telefono_puerta": ("puerta", "Close-up at dusk at the shop door: Daniel's trembling hand holds the thin glass phone, "
                        "the screen glowing with an incoming call, his blurred tearful face behind it."),
    "dos_telefonos": ("taller", "Night, the workshop is dark: on the wooden workbench two thin glass phones lie face up "
                      "side by side, both screens glowing with video calls, the birdcage with the sleeping yellow canary behind them, the clocks on "
                      "the green wall in shadow."),
    "mesa_junta": ("oficina", "Close-up on the long white meeting table at night: a thin glass phone lies face down next "
                   "to a laptop, vibrating, Daniel's tired hand resting near it."),
    "laptop_noche": ("depto", "Over-the-shoulder close-up from behind the grey sofa at night: Daniel's hands on a laptop "
                     "keyboard, the screen glowing white and blank, rain on the window beyond."),
}

LUGAR_AUDITORIO = ("a huge modern dark auditorium in Mexico City at a tech product launch: tiered seats full of people, a "
                   "giant LED screen above a minimalist stage, warm spotlights")


def personajes_en(texto):
    out = []
    for k, n in NOM.items():
        if n in texto and k not in out:
            out.append(k)
    return out


def chars(keys):
    return "; ".join(f"{NOM[k]} is {F['personajes'][k]}" for k in keys)


def lote():
    L = []
    for lugar, desc in g.ESC.items():
        L.append(dict(id=f"esc_{lugar}", kind="esc", out=f"flow/esc/{lugar}.jpg", ing=[],
                      prompt=f"{F['estilo']}. Empty establishing shot, no people: {desc}. {SIN_TEXTO}"))
    L.append(dict(id="esc_auditorio", kind="esc", out="flow/esc/auditorio.jpg", ing=[],
                  prompt=f"{F['estilo']}. Empty establishing shot, no people: {LUGAR_AUDITORIO}. {SIN_TEXTO}"))
    for k, pl in enumerate(g.PLANOS):
        sid = f"scene-{k + 1:03d}"
        if pl["tipo"] == "img":
            txt = IMG[pl["img"]]
            if txt.startswith("="):
                L.append(dict(id=sid, kind="img", out=f"medios/{sid}.jpg", copia=f"flow/esc/{txt[1:]}.jpg", ing=[]))
                continue
            esc = pl.get("esc")
            quien = [q for q in personajes_en(txt)]
            partes = [F["estilo"] + ".", f"Setting: {g.ESC[esc]}." if esc else "",
                      f"Characters: {chars(quien)}." if quien else "", txt]
            for o, d in F["objetos"].items():
                if {"reloj": "pocket watch", "canario": "canary", "telefono": "phone"}[o] in txt:
                    partes.append(d + ".")
            partes.append(SIN_TEXTO if pl["img"] != "reloj_grabado" else "No other text, no logos, no watermark.")
            L.append(dict(id=sid, kind="img", out=f"medios/{sid}.jpg", ing=[NOM[q] for q in quien] + ([f"ESC:{esc}"] if esc else []),
                          prompt=" ".join(p for p in partes if p)))
        elif pl["tipo"] in ("clip", "llamada"):
            quien = pl["personajes"]
            partes = [F["estilo"] + ".", f"Setting: {pl['escenario']}.", f"Characters: {chars(quien)}."]
            for o in pl.get("objetos", []):
                partes.append(F["objetos"][o].rstrip(".") + ".")
            if len(quien) >= 2:
                partes.append(" ".join(f"{NOM[q]} looks exactly like the {NOM[q]} character reference." for q in quien))
            partes.append(pl["a"])
            if pl["dialogo"]:
                for q, tono, linea in pl["dialogo"]:
                    partes.append(f'{NOM[q]} says in Mexican Spanish, {tono}: "{linea}"')
            else:
                partes.append("Nobody speaks: lips closed, no dialogue, no voice-over.")
            partes.append(F["cierre"])
            L.append(dict(id=sid, kind=pl["tipo"], d=pl["d"], out=f"medios/{sid}.mp4",
                          ing=[NOM[q] for q in quien] + [f"ESC:{pl['esc']}"], prompt=" ".join(partes)))
    for bid, (esc, txt) in BG.items():
        quien = personajes_en(txt)
        lugar = LUGAR_AUDITORIO if esc == "auditorio" else (g.ESC[esc] if esc else "")
        partes = [F["estilo"] + ".", f"Setting: {lugar}." if lugar else "", f"Characters: {chars(quien)}." if quien else "",
                  txt]
        if "phone" in txt:
            partes.append(F["objetos"]["telefono"] + ".")
        partes.append(SIN_TEXTO)
        L.append(dict(id=f"bg_{bid}", kind="bg", out=f"flow/bg/{bid}.jpg",
                      ing=[NOM[q] for q in quien] + ([f"ESC:{esc}"] if esc else []), prompt=" ".join(p for p in partes if p)))
    return L


if __name__ == "__main__":
    os.chdir(AQUI)
    os.makedirs("flow/esc", exist_ok=True)
    os.makedirs("flow/bg", exist_ok=True)
    os.makedirs("medios", exist_ok=True)
    L = lote()
    json.dump(L, open("flow/lote.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    c = Counter(x["kind"] for x in L)
    pts = sum((6 if x["d"] == 8 else 7) for x in L if x["kind"] in ("clip", "llamada"))
    print(dict(c), f"· clips ≈ {pts} pts")
    print(max(len(x.get("prompt", "")) for x in L), "caracteres el prompt más largo")
