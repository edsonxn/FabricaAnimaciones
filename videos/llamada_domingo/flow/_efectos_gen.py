# genera efectos.py: ambiente continuo por lugar + radio/canario (sesión 2, 6-nov-2026)
import json, guion as g
b = json.load(open("beats.json", encoding="utf-8"))
AMB = {
 "taller": ("Room tone of an old watch repair workshop: dozens of antique wall clocks ticking softly out of sync, a faint street outside, no music, no voices", 22),
 "oficina": ("Quiet glass office high above a city at night: low air conditioning hum, distant muffled traffic far below, no music, no voices", 22),
 "depto": ("Modern apartment at night: soft steady rain against a window, a faint refrigerator hum, no music, no voices", 22),
 "plaza": ("Small Mexican neighborhood plaza on a Sunday afternoon: birds in big trees, distant children, a far street vendor bell, soft breeze, no music", 22),
 "cocina": ("Old small kitchen at night: a round wall clock ticking, a faint old refrigerator hum, crickets outside, no music, no voices", 22),
 "porche": ("Porch of an old house at dusk: crickets, a distant dog, a soft breeze in potted plants, a metal rocking chair creaking softly, no music", 20),
 "auto_lucia": ("Inside a parked small car in the evening, windows closed: muffled street traffic passing outside, no music, no voices", 20),
 "taxi": ("Back seat of a taxi driving in a city at night in the rain: engine hum, tires on wet asphalt, rain on the roof, no music", 20),
 "pasillo": ("Hospital corridor at night: fluorescent light hum, distant soft monitor beeps, far footsteps, no music, no voices", 22),
 "hospital": ("Hospital room at night: a slow steady heart monitor beep, an oxygen concentrator hiss, faint corridor hum, no music", 22),
 "carretera": ("Inside a modern car on a highway: steady smooth road noise, soft wind, no music, no voices", 20),
 "puerta": ("Quiet old Mexican street at dusk in December: distant firecrackers far away, a dog barking far, soft wind, no music", 20),
 "puerta_dia": ("Old Mexican street on a sunny Sunday morning: birds, a distant church bell, a car passing far away, no music", 20),
 "hospital_ext": ("City street outside a hospital at night: wet asphalt, a distant ambulance siren fading, light traffic, no music", 12),
}
SFX = dict(AMB)
SFX["radio_bolero"] = ("An old wooden AM radio playing a soft romantic Mexican bolero with a guitar trio, lo-fi warm radio sound with faint static, instrumental", 22)
SFX["radio_perilla"] = ("Turning the knob of an old wooden radio: static sweeping, then a faint bolero tuning in, lo-fi", 6)
SFX["canario"] = ("A single canary singing a long sweet melodic song indoors, close, no other sounds", 12)
# tramos seguidos del mismo lugar (las llamadas y las piezas ui no rompen ni suman)
runs, cur = [], None
for x, p in zip(b, g.PLANOS):
    e = p.get("esc") if p["tipo"] in ("clip", "img") else None
    if p["tipo"] == "img" and not e:
        e = {"ext_relojeria": "puerta_dia", "plaza": "plaza", "cocina": "cocina", "ext_hospital": "hospital_ext",
             "puerta": "puerta"}.get(p["img"])
    if p["tipo"] == "llamada":
        if cur: cur[2] = x["t1"]
        continue
    if p["tipo"] == "ui" or e not in AMB:
        cur = None; continue
    if cur and cur[0] == e and abs(cur[2] - x["t0"]) < 0.05:
        cur[2] = x["t1"]
    else:
        cur = [e, x["t0"], x["t1"]]; runs.append(cur)
t = {x["id"]: x for x in b}
L = ['# -*- coding: utf-8 -*-', '"""Efectos de «Llamada de domingo» (generado por flow/_efectos_gen.py, sesión 2): ambiente continuo por lugar',
     'para que los cortes entre clips no salten de sonido; el bolero y el canario donde el guion los nombra."""',
     'CAMARA = {}', 'FUNDIDO = {}', 'FX = [dict(tipo="abre", en=0, dur=1.2)]', 'ROTULOS = []', 'SFX = {']
for k, v in SFX.items():
    L.append(f'    {k!r}: ({v[0]!r}, {v[1]}),')
L.append('}'); L.append('PISTAS = [')
for e, a, z in runs:
    L.append(f'    dict(sfx={e!r}, de={a:.1f}, a={z:.1f}, vol=.20),')
s7, s81 = t["scene-007"], t["scene-081"]
L.append(f'    dict(sfx="radio_perilla", en={s7["t0"] + 0.8:.1f}, vol=.35),          # Ramón gira la perilla')
L.append(f'    dict(sfx="radio_bolero", de={s81["t0"] + 2.5:.1f}, a={s81["t1"]:.1f}, vol=.45),   # Daniel prende el radio')
L.append(f'    dict(sfx="canario", de={s81["t0"] + 4.5:.1f}, a={s81["t1"]:.1f}, vol=.40),        # y el canario canta')
L.append(']')
open("efectos.py", "w", encoding="utf-8").write("\n".join(L) + "\n")
print(len(runs), "tramos de ambiente")
