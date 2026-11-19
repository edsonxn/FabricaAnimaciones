# -*- coding: utf-8 -*-
"""PROMESAS VISUALES (regla 5-nov-2026) + ESCENAS IMPORTANTES (regla 18-nov-2026) de er_godfrey_atrocidades.
Cuadro real (clip + capa de efectos) en el segundo en que la voz lo dice → previews/promesas_NN.jpg (12 por hoja),
y escribe promesas.md y escenas.md.      python _promesas.py            (desde la carpeta del video)"""
import os
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)   # el efectos.py del video, no nucleo/efectos.py
import secuencia_fx as SF  # noqa: E402

# (frase ancla, + s, qué debería verse, cómo se ve, escena importante)
PROMESAS = [
    ("Primer Señor del Círculo", 1.5, "Godfrey", "clip 001 (Godfrey en su cinemática) + silueta godfrey", 0),
    ("Marido de la reina Márika", .5, "Márika", "camafeo marika", 0),
    ("padre de Godwyn", .4, "Godwyn", "camafeo godwyn", 0),
    ("esquivando el hacha", .3, "el hacha de Godfrey", "camafeo hacha_godfrey + clip 006", 0),
    ("Ryans lo pidió en un comentario", 1.0, "comentario de Ryans", "tarjeta com_", 0),
    ("la mejor waifu del gaming", .4, "Miquella", "camafeo miquella + clip 010 (capullo de Miquella)", 0),
    ("se acuerda de Godrick", .4, "Godrick", "camafeo godrick", 0),
    ("en el Castillo de Velo Tormentoso", 1.0, "Velo Tormentoso", "mapa con foto + clips 012-014 del castillo", 0),
    ("La corona de Godfrey lo cuenta", .8, "Corona de Señor del Círculo", "reliquia + ficha", 0),
    ("todavía cuelga un retrato enorme", 1.2, "el retrato de Godfrey con Serosh", "pantalla retrato_velo", 0),
    ("Hasta los halcones lo recuerdan", .8, "Cenizas del halcón", "reliquia cenizas_halcon_rey", 0),
    ("Al sur, el Castillo de Morne", .6, "Castillo de Morne", "mapa con foto morne", 0),
    ("Su inscripción dice así", .8, "monumento de Morne con su inscripción", "pantalla monumento_morne + ficha (clip 024)", 0),
    ("en la espada más famosa de Morne", .8, "Espadón de hoja injertada", "reliquia + ficha", 0),
    ("la empuña el Bastardo leonino", .8, "Bastardo leonino", "silueta + clip 030 (pelea con el espadón)", 0),
    ("Un monumento en la frontera de Caelid", 4.2, "monumento de espada de Caelid", "pantalla monumento_caelid_espada", 0),
    ("llevaban en la frente la Cinta de campeón", .6, "Cinta de campeón", "reliquia + ficha", 0),
    ("su líder, Hoarah Loux", .4, "Hoarah Loux", "camafeo hoarah_loux + clip 036", 0),
    ("en la Tercera iglesia de Márika", .8, "Tercera iglesia de Márika", "mapa con foto + clip 041", 0),
    ("Melina te deja oír un eco", .8, "Melina y el eco", "silueta melina + clip 041 (Melina en la gracia)", 1),
    ("Mi señor. Os despojo", .6, "el eco de Márika", "MG ecos + clip 042/043 (Márika)", 1),
    ("El Recuerdo de Hoarah Loux lo confirma", .8, "Recuerdo de Hoarah Loux", "reliquia + ficha", 0),
    ("El Talismán con hacha cuenta", .8, "Talismán con hacha", "pegatina + ficha", 0),
    ("En la Iglesia de la peregrinación", .8, "Iglesia de la peregrinación", "mapa con foto + clip 049 (rótulo)", 0),
    ("Tras vuestra muerte", .6, "eco de la promesa", "MG ecos + clip 050 (Melina en la gracia)", 1),
    ("Hasta el Ancla oxidada guarda", .8, "Ancla oxidada", "reliquia + ficha", 0),
    ("Su hacha se rompió en la batalla", .6, "Hacha de Godfrey", "pegatina + ficha", 0),
    ("la intro lo nombra entre los muertos", .6, "la intro", "pantalla intro_hoarah", 0),
    ("Hoarah Loux, el caudillo", .8, "Hoarah Loux en la intro del juego", "clip 057 (intro, Hoarah Loux)", 1),
    ("Alzaos, Sinluz", .8, "«Alzaos, Sinluz» (intro)", "mensaje del suelo + clip 057/058", 0),
    ("Antonio escribió que está suscrito", 1.0, "comentario de Antonio", "tarjeta com_", 0),
    ("Godwyn el Dorado", .4, "Godwyn, Morgott y Mohg", "MG linaje", 0),
    ("Un muñeco que encuentras en el Subsuelo", 1.0, "Subsuelo de los marginados + Párvulo maldito", "pantalla subsuelo + reliquia parvulo", 0),
    ("el Párvulo maldito de la realeza", .6, "Párvulo maldito de la realeza", "reliquia + ficha", 0),
    ("Y el Grillete de Mohg dice", .8, "Grillete de Mohg", "pegatina + MG cadena", 0),
    ("Morgott salió de ahí abajo", .6, "Morgott", "silueta morgott + clip 077 (Morgott)", 0),
    ("Su recuerdo lo dice: jamás", .6, "Recuerdo del rey de los Augurios", "reliquia + ficha", 0),
    ("Su gemelo Mohg tomó el otro camino", .6, "Mohg", "silueta mohg + clip 079-081 (Mohg)", 0),
    ("Su Gran Runa lo dice", .8, "Gran Runa de Mohg", "reliquia + ficha", 0),
    ("Morgott ya está muerto", .4, "Godfrey llega al trono con Morgott muerto", "clip 082 (llegada al trono) + camafeo morgott", 1),
    ("Es para su hijo. Escúchalo", 2.5, "Godfrey ante Morgott muerto (se OYE «It's been a long while, Morgott»)", "clip 084 (cinemática, arrodillado junto a Morgott) + PISTA s_morgott", 1),
    ("también está la Llama Frenética", .8, "la Llama Frenética (rótulo)", "rótulo + clip 086 (cloacas)", 0),
    ("no se puede cancelar el final", .5, "la Llama Frenética de los Tres Dedos", "clip 087 (cinemática de los Tres Dedos, sin el jugador)", 0),
    ("Moreno nos corrigió", 1.0, "comentario de Moreno", "tarjeta com_", 0),
    ("La Aguja de Miquella solo funciona", .8, "Aguja de Miquella en Farum Azula", "reliquia + clip 089 (Farum Azula)", 0),
    ("en los Picos de los gigantes", .8, "Picos de los gigantes", "pantalla picos + clips 091-092", 0),
    ("En la Primera iglesia de Márika", .8, "Primera iglesia de Márika", "mapa con foto + clip 093", 0),
    ("Recuérdalo, mi señor Godfrey", .8, "el eco de la orden", "MG ecos + clip 094 (eco con Melina)", 1),
    ("Su corona lo resume en una línea", .6, "Corona de Señor del Círculo", "reliquia + ficha", 0),
    ("El Medallón de rugido dice", .6, "Medallón de rugido", "reliquia + ficha", 0),
    ("Y el Aplastagigantes, un martillo", .6, "Aplastagigantes", "pegatina + ficha", 0),
    ("Los caballeros de Zamor fueron", .8, "caballeros de Zamor", "reliquia armadura_zamor + clips 100-102 (Antiguo héroe de Zamor)", 0),
    ("hasta un escudo con un rostro espantoso", .8, "Escudo de rostro", "reliquia + ficha", 0),
    ("atravesados por estacas", .3, "gigantes empalados", "pantalla gigantes_empalados + clip 103", 1),
    ("El Gigante de fuego, el jefe", .8, "Gigante de fuego", "pegatina grande + clip 105", 1),
    ("Oh, insignificante gigante", .6, "la maldición de Márika", "mensaje + clip 107 (Gigante de fuego)", 0),
    ("y usas su llama para quemar", .5, "la Forja / el Árbol en llamas", "MG domino + clip 109 (el Árbol arde)", 1),
    ("un monumento con espada la resume", .8, "monumento de la guerra contra los gigantes", "pantalla monumento_gigantes", 0),
    ("Los troles descienden de los gigantes", .6, "un trol", "silueta troll + clip 112", 0),
    ("la Espada dorada de trol", .4, "Espada dorada de trol", "reliquia + ficha", 0),
    ("Marcelo escribió que estos videos", 1.0, "comentario de Marcelo", "tarjeta com_", 0),
    ("solo seis están suscritos", .3, "6 de cada 100", "MG cien", 0),
    ("contra el único que lo aguantó", .6, "Serosh", "camafeo serosh + clip 125", 0),
    ("El león que Godfrey lleva", .6, "Godfrey con Serosh", "pegatina grande + clip 126 (Serosh en la cinemática)", 0),
    ("El Icono de Godfrey lo explica", .8, "Icono de Godfrey", "reliquia + ficha", 0),
    ("Y ese icono lo guarda Godefroy", .8, "Godefroy en su prisión eterna", "silueta + mapa + clips 130-131", 0),
    ("el que te da Gurranq", .4, "Gurranq + Gran martillo de garras", "camafeo gurranq + reliquia + clip 132", 0),
    ("Y un escudo con su blasón", .8, "Escudo apuntado con blasón de bestia", "reliquia + ficha", 0),
    ("La Armadura leonina de Radahn", .6, "Armadura leonina de Radahn", "reliquia + ficha + clips 134-135 (Radahn)", 0),
    ("en la capital hecha ceniza", .8, "Leyndell, capital cinérea", "mapa + pantalla leyndell_ceniza", 0),
    ("Godfrey vuelve con Serosh a la espalda", 1.0, "Godfrey vuelve con Serosh", "clip 139 (cinemática) + silueta", 1),
    ("Por desgracia, aquí estoy", 1.5, "Godfrey habla", "clip 140 (Godfrey se levanta con el hacha) + mensaje", 1),
    ("Serosh empieza a cambiar", 1.0, "Serosh se vuelve de carne", "clip 142 (Serosh se materializa) + banda serosh_carne", 1),
    ("Le agarra la cabeza", .5, "Godfrey agarra la cabeza de Serosh", "clip 143 (cinemática)", 1),
    ("Me has servido bien, Serosh", .5, "«Me has servido bien, Serosh»", "clip 144 (cinemática)", 1),
    ("Y le rompe el cuello", .6, "Godfrey le rompe el cuello a Serosh", "clip 145 (Serosh ensangrentado, la sangre)", 1),
    ("Bañado en la sangre de su regente", 1.0, "Godfrey bañado en sangre", "clip 147 + banda hoarah_loux", 1),
    ("antes de ser rey. Escúchalo", 3.5, "el grito «Now I fight as Hoarah Loux! Warrior!» se OYE", "clip 148 (cinemática sincronizada con PISTA s_hoarah)", 1),
    ("Ahora pelea como Hoarah Loux", 1.0, "Hoarah Loux peleando", "clip 149 (2.ª fase) + MG contencion", 1),
    ("Los guerreros de los altiplanos, su gente", .6, "Atuendo de los altiplanos", "reliquia + ficha", 0),
    ("Nibald nos escribió", 1.0, "comentario de Nibald", "tarjeta com_", 0),
    ("digna de una corona", .4, "la muerte de Godfrey («digna de una corona»)", "clip 156 (Hoarah Loux cae y se deshace)", 1),
    ("El Hacha de Godfrey ya lo había", .8, "Hacha de Godfrey", "reliquia + ficha", 0),
    ("Que acabó en Godrick", .5, "Godrick cosiéndose brazos", "MG linaje + clip 162 (Godrick)", 0),
    ("y le pregunta a Godfrey si lo ha visto", .3, "Godrick", "silueta godrick + clip 163", 0),
    ("con un talismán en la Fortaleza sombría", .8, "Fortaleza sombría + Talismán de la dádiva", "pantalla + reliquia", 0),
    ("Ya están apuntados Rykard", 1.0, "Rykard, Zampaheces, Gideon, Rennala, Messmer", "abanico", 0),
    ("En el canal tienes las atrocidades", 1.5, "los videos del canal", "abanico", 0),
    ("Crónicas de Tamriel, nuestro canal hermano", .8, "Crónicas de Tamriel", "rótulo", 0),
    ("fíjate en el león", .4, "Serosh", "camafeo + clip 172", 0),
]


def main():
    capa = SF.cargar()
    S = capa.S
    minis, filas = [], []
    mw, mh = 480, 270
    for frase, dt, que, como, esc in PROMESAS:
        try:
            t = capa.ancla(frase) + dt
        except Exception as e:
            print("NO ENCONTRADA:", frase, e)
            continue
        k = next((i for i, b in enumerate(capa.bs) if b["t0"] <= t < b["t1"]), len(capa.bs) - 1)
        b = capa.bs[k]
        f = capa.aplicar(capa.envolver(S._fuente(b, k, True, capa), b).cuadro(t), t)
        m = cv2.resize(f, (mw, mh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(m, (0, mh - 26), (mw, mh), (20, 18, 18), -1)
        txt = f"{len(filas) + 1} {int(t // 60)}:{t % 60:04.1f} {b['id'][6:]} {'E ' if esc else ''}{que}"
        cv2.putText(m, txt.encode("ascii", "replace").decode(), (6, mh - 7), cv2.FONT_HERSHEY_SIMPLEX, .45, (90, 214, 255), 1,
                    cv2.LINE_AA)
        minis.append(m)
        filas.append((frase, t, b["id"], que, como, esc))
    cols, n = 4, 12
    for h in range(0, len(minis), n):
        g = minis[h:h + n] + [np.zeros_like(minis[0])] * (-len(minis[h:h + n]) % cols)
        ruta = f"previews/promesas_{h // n + 1:02d}.jpg"
        cv2.imwrite(ruta, np.vstack([np.hstack(g[i:i + cols]) for i in range(0, len(g), cols)]))
        print(ruta)
    mm = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"
    pm = ["# Promesas visuales — er_godfrey_atrocidades (regla del 5-nov-2026)", "",
          "Hoja: previews/promesas_NN.jpg (cuadro real clip + capa de FX en ese segundo; «E» = escena importante).", "",
          "| n | segundo | beat | qué se nombra | cómo se ve |", "|---|---|---|---|---|"]
    es = ["# Escenas importantes — er_godfrey_atrocidades (regla del 18-nov-2026)", "",
          "Cada una con el clip REAL de ese momento (sin Flow); la pegatina va encima o después.", "",
          "| segundo | beat | escena | cómo se ve |", "|---|---|---|---|"]
    for i, (frase, t, bid, que, como, esc) in enumerate(filas, 1):
        pm.append(f"| {i} | {mm(t)} | {bid[6:]} | {que} | {como} |")
        if esc:
            es.append(f"| {mm(t)} | {bid[6:]} | {que} | {como} |")
    open("promesas.md", "w", encoding="utf-8").write("\n".join(pm) + "\n")
    open("escenas.md", "w", encoding="utf-8").write("\n".join(es) + "\n")
    print(len(filas), "promesas;", sum(f[5] for f in filas), "escenas")


if __name__ == "__main__":
    main()
