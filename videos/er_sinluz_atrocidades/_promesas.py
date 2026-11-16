# -*- coding: utf-8 -*-
"""Escribe promesas.md (regla del 5-nov-2026): cada frase que promete algo que se VE, su segundo y cómo se ve.
    python _promesas.py
"""
import json

P = [
    ("p5_1", "la Torre de Seluvis en las Tres Hermanas, Seluvis", "pantalla tres_hermanas + silueta seluvis + clips de la torre"),
    ("p5_2", "el frasquito, su descripción y la orden", "reliquia pocion_seluvis + ficha + mensaje «Encuentra a Nepheli…»"),
    ("p5_3", "Nepheli, la Mesa Redonda y las 3 opciones", "pegatina grande nepheli + camafeo mesa_redonda + abanico Nepheli/Zampaheces/Gideon"),
    ("p5b_0", "sótano con figuras inmóviles y el mensaje «Marioneta de Seluvis. No tocar»", "clips del sótano + mensaje del suelo"),
    ("p5b_1", "las marionetas como cenizas de espíritu", "abanico de 4 marionetas reales + clips de invocación"),
    ("p5b_5", "marioneta de Sellen tras la pared falsa", "silueta sellen + clips del sótano"),
    ("p5b_6", "Ámbar de luz estelar, Brebaje ámbar, Ranni", "reliquia ambar_estelar + ficha + pegatina brebaje + MG marionetas (Ranni)"),
    ("p4_1", "Mansión del Volcán entre lava, Tanith con máscara", "mapa mundo (foto mansion_volcan) + silueta tanith + clips del recibidor"),
    ("p4_3", "Istvan, Rileigh, Juno Hoslow y sus lugares", "mapa mundo con las 3 fotos y ruta + clips de invasión"),
    ("p4_4", "los 3 pagos", "abanico disparo_magma / hoja_serpiente / camafeo"),
    ("p4b_1", "Rykard y el Rencor de Rykard", "silueta rykard + reliquia rencor_rykard + ficha + clips de la pelea"),
    ("p4b_2", "campeones a las fauces de la serpiente", "MG audiencia + pegatina serpiente + clips de la Serpiente devoradioses"),
    ("p4b_4", "Tanith comiéndose a Rykard", "pegatina tanith + clips 063-064 (Tanith junto al cadáver)"),
    ("p4b_6", "Varré y el Favor del Señor de la Sangre", "silueta varre + reliquia favor_sangre + ficha"),
    ("p4b_8", "doncella sentada en la Iglesia de la Inhibición", "pantalla iglesia_inhibicion + clips"),
    ("p3_3", "Rennala entre libros flotantes abrazando el huevo de ámbar", "mapa (foto academia) + pegatina rennala + clip 078 (huevo)"),
    ("p3_5", "Gran Runa de los Nonatos", "reliquia runa_nonatos + ficha"),
    ("p3b_0", "Radahn en Caelid y su corcel", "mapa Caelid + reliquia recuerdo_azote + ficha + clips 085-087 (Radahn a caballo)"),
    ("p3b_2", "las estrellas se mueven y una cae en Necrolimbo", "MG cielo_sujeto + mapa Caelid→Necrolimbo + clip 090 (estrella)"),
    ("p3b_4", "edificios enormes con patas: Mausoleos errantes", "clips 092-096 (mausoleo caminando) + rótulo"),
    ("p3c_0", "Gurranq, lobo enorme, en el Santuario de la bestia", "mapa Montedrago (foto santuario_bestia) + silueta gurranq + clips 099-106"),
    ("p3c_2", "le da la 4.ª raíz, se lanza contra ti, «basta»", "MG paciencia (sello «Basta») + clips 107-108 (ataque)"),
    ("p2_1", "Hyetta: ciega, misma cara y ropa que Irina", "abanico irina/hyetta + pegatina grande hyetta + clips 113-116"),
    ("p2_2", "la Uva Shabriri", "reliquia uva_shabriri + ficha con su descripción"),
    ("p2_4", "es un ojo", "MG uvas (las uvas giran y son ojos)"),
    ("p2_5", "Edgar el vengador te invade", "silueta edgar + clips de la invasión"),
    ("p2b_1", "Hyetta vomita", "banda hyetta + clips 127-128"),
    ("p2b_2", "Vyke y su ojo", "silueta vyke + ficha uva_dactilograma + clips"),
    ("p2b_3", "puerta sellada, te desnudas, dedos gigantes", "pantalla subsuelo + pegatina camara_frenetica + clips 133-135"),
    ("p2b_5", "se OYE a Hyetta ardiendo y dando las gracias", "PISTA s_hyetta (voz callada, 9,6 s) + clips 136-138"),
    ("p1_4", "último Gigante de fuego y la Forja", "pegatina gigante_fuego + clips de la Forja"),
    ("p1_5", "Melina ordena arder al Árbol; se OYE su despedida", "PISTA s_melina (9,4 s) + clips 148-150 (cinemática)"),
    ("p1b_0", "Melina se lanza al fuego", "MG arbol_arde + clips 158-160"),
    ("p1b_1", "Shabriri te lo restriega", "silueta shabriri + clips 162-164"),
    ("p1c_0", "Leyndell, capital cinérea, cenizas", "pantalla capital_cinerea + clips 172-174"),
    ("p1c_1", "el Zampaheces y las Maldiciones del semillero", "silueta zampaheces + reliquia maldicion_semillero + ficha runa reparadora"),
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
