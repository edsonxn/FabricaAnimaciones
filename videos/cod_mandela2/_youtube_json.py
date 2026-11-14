# -*- coding: utf-8 -*-
"""Genera youtube.json de cod_mandela2 (capítulos del timeline real, créditos de fuentes.json)."""
import json
T = json.load(open("timeline.json", encoding="utf-8"))
t0 = {e["id"]: e["t0"] + e.get("pre", 0) for e in T["escenas"]}
CAP = [("intro", "Expediente 141: tu memoria, otra vez"), ("p20", "#20 La bomba que nunca desactivaste"),
       ("p19", "#19 La mira de la Intervention"), ("p18", "#18 El uniforme de Richtofen"), ("p17", "#17 El césped de Nuketown"),
       ("p16", "#16 Double Tap, segunda parte"), ("p15", "#15 La montaña que nunca volvió"), ("p14", "#14 La cámara del Pack-a-Punch"),
       ("p13", "#13 Devolver la granada"), ("p12", "#12 Los perros de World at War"), ("p11", "#11 El armario de Nacht der Untoten"),
       ("p10", "#10 La canción que no era de Kino"), ("p09", "#9 La Wunderwaffe"), ("p08", "#8 ¿Cuándo salió Black Ops?"),
       ("p07", "#7 El reencuentro de Mason y Woods"), ("p06", "#6 La perk de Moon, otra vez"), ("p05", "#5 La M1911 de Alcatraz"),
       ("p04", "#4 El director Hoover"), ("p03", "#3 La AUG en la granja"), ("p02", "#2 El ojo de Weaver"),
       ("p01", "#1 La frase de Gaz"), ("cierre", "Expediente cerrado")]
def mmss(s):
    s = int(s); return f"{s // 60}:{s % 60:02d}"
caps = "\n".join(f"{'0:00' if k == 'intro' else mmss(t0[k])} {n}" for k, n in CAP)
F = json.load(open("fuentes.json", encoding="utf-8"))
vids = []
for k in sorted(F):
    v = F[k].get("video")
    if v and v not in vids: vids.append(v)
gameplay = " · ".join("https://youtu.be/" + v for v in vids)
desc = ("¿Gaz dijo «sidearm» o «pistol»? ¿Kravchenko le apagó un puro en el ojo a Weaver? ¿Richtofen iba de verde? La parte 1 la armaron ustedes "
        "en los comentarios y aquí está la parte 2: 20 efectos Mandela de Call of Duty, y cuatro me los mandaron ustedes. Lo que "
        "recuerdas contra lo que de verdad hay en el juego, comprobado en pantalla.\n\nCAPÍTULOS\n" + caps +
        "\n\nFUENTES:\nWiki de Call of Duty (transcripciones de F.N.G., Semper Fi, Executive Order y Pyrrhic Victory; Farm, Ascension, "
        "Downhill, Kino der Toten, Nacht der Untoten, Wunderwaffe DG-2, Mob of the Dead, Random Perk Bottle, Call of Duty: Black Ops) — "
        "https://callofduty.fandom.com\nThe Cutting Room Floor: Black Ops II — https://tcrf.net/Call_of_Duty:_Black_Ops_II\n"
        "Hilos de r/CODZombies, r/CallOfDuty y r/MandelaEffect con los recuerdos de la comunidad — https://www.reddit.com\n"
        "Fellow — https://youtu.be/MUHIbSFqEyg · https://youtu.be/8pSie2MKLoM\nDrrpy — https://youtu.be/g8n6YhAzlRs\n\n"
        "MÚSICA Y SONIDO: bandas sonoras oficiales de Call of Duty: Jack Wall («Black Ops 6», «Pyrrhic Victory», «Exit Amerika», "
        "«I Live»), Hans Zimmer («Contingency»), Sean Murray («Russian Theme», «Vorkuta») y Kevin Sherwood («Turn To Ashes»; «115» "
        "y «Lullaby of a Dead Man» con Elena Siegman). Audio del juego: Infinity Ward, Treyarch / Activision.\n\n"
        "GAMEPLAY DE: " + gameplay + " y más creadores. Gracias a todos.\n\n#callofduty #efectomandela #codzombies")
Y = {"titulo": "Los 20 EFECTOS MANDELA de Call of Duty que TÚ recordaste (parte 2)",
     "titulos_alternativos": ["20 cosas de Call of Duty que recuerdas MAL (parte 2)", "Efecto Mandela en Call of Duty: lo que TÚ recordaste"],
     "descripcion": desc,
     "etiquetas": ["call of duty", "efecto mandela", "efecto mandela call of duty", "cod zombies", "gaz pistol sidearm", "weaver ojo",
                   "richtofen", "nacht der untoten", "kino der toten", "wunderwaffe", "black ops", "modern warfare", "call of duty en español",
                   "expediente 141"],
     "categoria": 20, "idioma": "es", "idioma_audio": "es", "miniatura": "salida/miniatura.jpg",
     "subtitulos": "salida/Los_20_EFECTOS_MANDELA_de_Call_of_Duty_que_TU_recordaste_par.srt"}
json.dump(Y, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(desc), "caracteres;", len(vids), "videos de gameplay"); print(caps)
