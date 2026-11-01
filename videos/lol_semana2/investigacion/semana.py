# python semana.py [--sumar]  -> stats_<gid>.json de cada partida jugada del 28 al 31-oct (rondas 4 y 5) y semana.json por jugador
import json, os, subprocess, sys
import api
os.chdir(os.path.dirname(os.path.abspath(__file__)))
evs = []; tok = None
for _ in range(4):
    d = api.get("getSchedule", leagueId=98767975604431411, **({"pageToken": tok} if tok else {}))["data"]["schedule"]
    evs = d["events"] + evs; tok = d["pages"].get("older")
    if not tok: break
gids = []
for e in evs:
    if e["startTime"] < "2026-10-28" or e["startTime"] > "2026-11-01" or e["type"] != "match" or e["state"] != "completed": continue
    m = api.get("getEventDetails", id=e["match"]["id"])["data"]["event"]["match"]
    eq = "-".join(t["code"] for t in m["teams"])
    for g in m["games"]:
        if g["state"] == "completed":
            gids.append((eq, g["id"]))
print(len(gids), "partidas")
if "--sumar" not in sys.argv:
    falta = [g for _, g in gids if not os.path.exists(f"stats_{g}.json")]
    if falta:
        subprocess.run([sys.executable, "stats.py", *falta], check=True)
J = {}
for eq, g in gids:
    s = json.load(open(f"stats_{g}.json", encoding="utf-8"))
    for side, t in s["teams"].items():
        for p in t["players"]:
            j = J.setdefault(p["name"], dict(serie=set(), juegos=0, k=0, d=0, a=0, champs=[], role=p["role"], dmg=[]))
            j["serie"].add(eq); j["juegos"] += 1; j["k"] += p["k"]; j["d"] += p["d"]; j["a"] += p["a"]; j["champs"].append(p["champ"])
            if p.get("dmgShare") is not None: j["dmg"].append(p["dmgShare"])
for n, j in J.items():
    j["serie"] = sorted(j["serie"]); j["kda"] = round((j["k"] + j["a"]) / max(1, j["d"]), 2)
    j["dmg"] = round(sum(j["dmg"]) / len(j["dmg"]), 3) if j["dmg"] else None
json.dump(J, open("semana.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for n, j in sorted(J.items(), key=lambda x: -x[1]["kda"])[:25]:
    print(f"{n:16} {j['role']:8} {j['juegos']}p {j['k']}/{j['d']}/{j['a']} KDA {j['kda']} dmg {j['dmg']} {j['serie']}")
