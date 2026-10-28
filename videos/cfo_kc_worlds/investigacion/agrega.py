import json, sys
sys.stdout.reconfigure(encoding="utf-8")
KC = "111692118851466302"
fases = {"Play-in": ["115660588583171787","115660588583171788","115660588583171789","116299649500204436","116299649500204437",
                      "115660588583171791","115660588583171792","115660588583171793","116299649498303885","116299649498303886","116299649498303887"],
         "Suiza": ["115660540726095010","115660540726095024","115660540726095052"]}
fases["Total"] = fases["Play-in"] + fases["Suiza"]
for f, gids in fases.items():
    agg = {}; tk = 0; wins = 0
    print(f"\n== {f} ({len(gids)} partidas)")
    for g in gids:
        s = json.load(open(f"stats_{g}.json", encoding="utf-8"))
        side = [k for k, v in s["teams"].items() if v["esportsTeamId"] == KC][0]
        opp = "red" if side == "blue" else "blue"
        t = s["teams"][side]; tk += t["kills"]
        if f != "Total":
            print(g, side, f"{t['kills']}-{s['teams'][opp]['kills']}", " | ".join(f"{p['name'].split()[-1]} {p['champ']} {p['k']}/{p['d']}/{p['a']} dmg{(p['dmgShare'] or 0)*100:.0f}%" for p in t["players"]))
        for p in t["players"]:
            n = p["name"].split()[-1]
            a = agg.setdefault(n, {"k":0,"d":0,"a":0,"ch":[],"cs":0,"dmg":[]})
            a["k"]+=p["k"]; a["d"]+=p["d"]; a["a"]+=p["a"]; a["ch"].append(p["champ"]); a["dmg"].append(p["dmgShare"] or 0)
    for n, a in agg.items():
        kda = (a["k"]+a["a"])/max(a["d"],1)
        print(f"{n:10s} {a['k']}/{a['d']}/{a['a']} KDA {kda:.2f} KP {100*(a['k']+a['a'])/tk:.0f}% dmg medio {100*sum(a['dmg'])/len(a['dmg']):.0f}% | {', '.join(a['ch'])}")
    print("asesinatos equipo", tk)
