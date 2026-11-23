# -*- coding: utf-8 -*-
"""Clips rehechos tras MIRAR las hojas medios_01-06 (19-nov-2026, sesión 2). Aplica sobre busquedas.json y lista los beats:
    python _rehechos.py  ->  python fab.py cod_mandela3 bajar <lista> --rehacer -j 2
Motivo de cada uno al lado: marca de agua de canal, facecam, texto quemado, negro, menú en vez de juego, clip que no cuenta la frase."""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
YT = "https://youtu.be/"
R = {
    "scene-006": ["Black Ops 2 Nuketown 2025 gameplay"],                      # negro (intro de No Russian)
    "scene-008": ["Modern Warfare 2019 Clean House no commentary", "Modern Warfare 2019 campaign Price Gaz"],          # créditos en texto
    "scene-014": ["Black Ops 4 zombies IX gameplay"],                         # título quemado «WW2 Zombies Max Ammo»
    "scene-015": ["Call of Duty 4 multiplayer Crash no commentary"],          # zombis, la frase es la nuke de CoD 4
    "scene-016": ["Call of Duty 4 multiplayer Overgrown no commentary"],      # cronómetro de speedrun
    "scene-019": {"url": YT + "XVa5ocWlB5o", "desde": 160.0},         # marca BETA
    "scene-024": ["Modern Warfare 2 Endgame no commentary"],                  # logo de canal
    "scene-026": ["TranZit Black Ops 2 zombies no commentary"],               # logo de canal
    "scene-042": ["World at War Their Land Their Blood gameplay"],            # marca EPICSARCHIVE
    "scene-043": ["World at War Downfall Reichstag gameplay"],                # marca UKGAMEPLAY
    "scene-051": ["Call of Duty 2003 Pegasus Bridge Captain Price"],          # Price de MW2, la frase es el de CoD 1
    "scene-052": ["Call of Duty 1 Tirpitz mission gameplay"],                 # título quemado
    "scene-054": ["Call of Duty 1 Tirpitz battleship no commentary"],         # marca EPICSARCHIVE
    "scene-056": ["Modern Warfare 2019 Piccadilly multiplayer gameplay"],     # menú
    "scene-059": ["Modern Warfare 2019 Piccadilly gameplay no commentary"],   # menú
    "scene-061": ["Nacht der Untoten Black Ops gameplay no commentary"],      # negro
    "scene-068": {"url": YT + "XxemwEJDFi0", "desde": 0.0},                   # facecam del streamer (cita de la misión)
    "scene-069": ["Call of Duty 4 Remastered All Ghillied Up Pripyat"],      # otro juego/escena
    "scene-077": ["Buried Black Ops 2 zombies no commentary"],                # negro
    "scene-081": {"url": YT + "x7vvJm9jRVU", "desde": 8.5},                  # negro; el ascensor ANTES del tiroteo (98 s)
    "scene-086": {"url": YT + "jB-n_8zq9Qo", "desde": 40.0},            # marca EPICSARCHIVE
    "scene-089": {"url": YT + "4r-YtrYGAIQ", "desde": 158.0},                 # «ahí Jackson sí estira el brazo» = REMASTER
    "scene-094": ["Alpha Omega Black Ops 4 zombies no commentary"],           # texto quemado «1 ROUND AFTER…»
    "scene-102": {"url": YT + "EMHd0VYb2pg", "desde": 200.0},                 # la frase es la celda
    "scene-103": {"url": YT + "bVEbYbYd2ZE", "desde": 622.0},                 # la frase es la línea de tiempo (y marca GameClips)
    "scene-104": ["Black Ops 7 campaign no commentary"],                      # marca de canal
    # 2.ª vuelta tras texto_clips: marcas de canal y overlays (CINEMATIC GAMING, Subscribe, FPS, JMP PRODUCTIONS, GPU)
    "scene-004": ["Black Ops 2 Nuketown Zombies no commentary"],
    "scene-006": ["Black Ops 2 Nuketown 2025 multiplayer no commentary"],
    "scene-021": {"url": "https://youtu.be/h_6X1qv50Ww", "desde": 80.0},
    "scene-030": ["Black Ops 2 Grief zombies no commentary"],
    "scene-075": ["Black Ops Cold War Outbreak no commentary"],
    "scene-105": ["Black Ops 7 campaign Menendez no commentary"],
    "scene-076": {"url": YT + "SDfcmo0hlqE", "desde": 45.0},   # Blackout (BO4), la frase es la de Black Ops 2
    "scene-079": {"url": YT + "1Gvn9DCw0rU", "desde": 600.0},  # Blackout
    # 3.ª vuelta tras fx hoja (sesión 3, 19-nov): texto quemado, marca TGN + entrevista, negro inicial
    "scene-029": ["TranZit Farm Black Ops 2 zombies no commentary"],          # rótulo quemado «Song Easter Egg» + esfera oscura
    "scene-076": ["Ray Gun Mark II Black Ops 2 zombies gameplay no commentary"],  # marca TGN, entrevista y negro
    "scene-066": {"url": YT + "RRYmVb33VU0", "desde": 2.0},                   # 2 s de negro al inicio del menú
}
if __name__ == "__main__":
    p = os.path.join(AQUI, "busquedas.json")
    q = json.load(open(p, encoding="utf-8"))
    q.update(R)
    json.dump(q, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(",".join(str(int(k.split("-")[1])) for k in R))
