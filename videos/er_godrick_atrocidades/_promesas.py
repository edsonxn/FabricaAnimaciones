# -*- coding: utf-8 -*-
"""Escribe promesas.md (regla del 5-nov-2026): cada frase que promete algo que se VE, su segundo y cómo se ve.
    python _promesas.py
"""
import json

P = [
    ("intro_0", "cara de niño, muchos brazos, escudo dorado (el Vástago)", "pantalla vastago_foto + clips 001-003 Vástago en la Capilla + reliquia escudo_bestia"),
    ("intro_3", "castillo con miembros colgados, trol crucificado, pila de cadáveres", "abanico (castillo, caballeros, recuerdo, dragón) sobre clips de Velo Tormentoso"),
    ("voto_2", "se OYE el narrador anterior", "PISTA s_faraon (voz callada) + MG votacion carta A con onda"),
    ("p5_3", "cofre con el Velo de imitador en la sala del Vástago", "clip yRzy2vEY2MQ cofre + reliquia velo_imitador + ficha"),
    ("p5_6", "estatua de Godfrey en la sala del trono", "clips Godrick/Godfrey + MG linaje (Godfrey)"),
    ("p5b_2", "monumento con una espada junto al Lago de Agheel", "mapa limgrave (Agheel con foto) + pantalla monumento"),
    ("p5b_3", "la inscripción legible", "mensaje del suelo con el texto + pantalla monumento"),
    ("p5b_6", "Radahn podrido en Caelid", "clips Radahn (039-041) + pegatina radahn + mapa mundo Caelid"),
    ("p4_1", "Castillo de Morne en la punta de la Península", "mapa limgrave (Morne con foto) + silueta Edgar"),
    ("p4_2", "Morne en llamas, Bastardos rebelados", "pantalla morne + clips Morne + pegatina leonino"),
    ("p4_3", "látigo en el suelo de la celda, ratas, Bastardo encerrado", "clip RVBWw-J2rA0 246 (látigo + aviso) + reliquia latigo"),
    ("p4_5", "Bastardo leonino", "silueta leonino + clips 054-056 de la pelea"),
    ("p4b_0", "Irina junto al Puente del Sacrificio", "silueta irina + mapa del puente + clips Irina viva"),
    ("p4b_1", "Irina muerta", "pantalla edgar_irina + clip IkesCV_PYwI 3080"),
    ("p4b_5", "comandante con Tajo sangriento y la Exultación", "silueta comandante_haight + reliquia exaltacion + clips del Fuerte"),
    ("p3_2", "dragón muerto atravesado sobre una estatua", "pantalla dragon_estatua + clips 075-078 + pegatina dragon_empalado"),
    ("p3_4", "se OYE «I command thee, kneel!»", "PISTA s_kneel + ficha con la frase original + clip 081 Godrick"),
    ("p3b_1", "se corta el brazo y se cose la cabeza del dragón", "clips 085-086 (Huip3TdEOdU 492-530) + pegatina brazo_dragon"),
    ("p3c_0", "cárcel eterna en Altus, otro hombre con la misma cara", "mapa mundo Altus + silueta godefroy + clips 092-098"),
    ("p3c_3", "deja caer el Icono de Godfrey", "reliquia icono_godfrey"),
    ("p2_1", "Roderika sentada en una cabaña junto al camino", "mapa de la Colina + silueta roderika + clips 102-103"),
    ("p2_5", "el Vástago injertado: muchas extremidades, rostro de joven", "pantalla vastago_foto + clips Vástago"),
    ("p2b_0", "pila de cadáveres y trol crucificado", "clips 114-115, 120 (vjgNUcwhopI 2743-2768) + mapa Velo"),
    ("p2b_1", "broche del Recuerdo de las crisálidas", "reliquia recuerdo_crisalidas + ficha + clip de la pila"),
    ("p2b_3", "halcones de guerra sin garras", "reliquia halcon (cenizas) + ficha; clip 122 halcón en el castillo"),
    ("p2b_5", "la capucha carmesí en la pila", "pegatina grande capucha + clip q_fz0HWb2yk 38 (capucha en la pila)"),
    ("p1_5", "se OYE el monólogo cortado de la cacería", "PISTA s_caceria + rótulo CONTENIDO CORTADO + mensaje con el texto inglés"),
    ("p1b_1", "Gostoc te encierra con un Caballero proscrito", "pantalla gostoc_foto + silueta gostoc + clips 139-143"),
    ("p1b_4", "se OYE a Gostoc cortado", "PISTA s_branch + rótulo CONTENIDO CORTADO + mensaje «A fine branch»"),
    ("p1c_3", "Capilla de la espera, la criatura que te mató", "pantalla vastago_foto + clips del Vástago"),
    ("cierre_8", "un Vástago injertado te mata", "pantalla vastago_foto + clip 172 BYSgy6UllRw"),
]
tl = json.load(open("timeline.json", encoding="utf-8"))
t0 = {f["key"]: f["t0"] for e in tl["escenas"] for f in e["frases"]}
out = ["# Promesas visuales — er_godrick_atrocidades (regla del 5-nov-2026)", "",
       "| frase | segundo | qué promete | cómo se ve |", "|---|---|---|---|"]
for k, que, como in P:
    t = t0[k]
    out.append(f"| {k} | {int(t // 60)}:{t % 60:04.1f} | {que} | {como} |")
out += ["", "Sin video real (cubierto con imagen fija): monumento legible, halcones, Icono de Godfrey, Cenizas de Kristoff, "
        "Exultación como objeto, capucha en Farum Azula (se dice que aparece en la misma pila: clip de la pila + pegatina)."]
open("promesas.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(P), "promesas")
