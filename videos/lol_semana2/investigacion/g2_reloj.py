# Reloj de JUEGO (sin pausas) de un feed con pausas: python g2_reloj.py <gameId> -> pausas, objetivos y muertes con reloj de juego
# (el reloj de g1_feed.py es tiempo de pared desde el inicio: en la G2 hubo pausas largas y ese reloj no coincide con el HUD).
import json, sys, datetime as dt
gid = sys.argv[1]
D = json.load(open(f"feed_{gid}.json", encoding="utf-8"))
def iso(s): return dt.datetime.fromisoformat(s.rstrip("Z")[:23])
fr = [f for f in D["frames"] if f["gameState"] in ("in_game", "paused", "finished")]
nom = {}
for side in ("blue", "red"):
    for pm in D["meta"][side + "TeamMetadata"]["participantMetadata"]:
        nom[pm["participantId"]] = f"{pm['summonerName'].split(' ')[-1]}({pm['championId']})"
g = 0.0; prev = None; pausa = None
def mmss(s): return f"{int(s//60):02d}:{int(s%60):02d}"
def ps(f): return {p["participantId"]: p for k in ("blueTeam", "redTeam") for p in f[k]["participants"]}
for f in fr:
    t = iso(f["rfc460Timestamp"])
    if prev:
        dtt = (t - iso(prev["rfc460Timestamp"])).total_seconds()
        if prev["gameState"] == "in_game": g += dtt
        if f["gameState"] == "paused" and pausa is None: pausa = (t, g)
        if f["gameState"] != "paused" and pausa:
            print(f"PAUSA juego {mmss(pausa[1])}  pared {pausa[0]:%H:%M:%S}Z -> {t:%H:%M:%S}Z ({(t - pausa[0]).total_seconds()/60:.1f} min)")
            pausa = None
        a, b = ps(prev), ps(f)
        K = [f"{nom[i]}+{b[i]['kills']-a[i]['kills']}" for i in b if b[i]["kills"] > a[i]["kills"]]
        Dd = [nom[i] for i in b if b[i]["deaths"] > a[i]["deaths"]]
        A = [nom[i] for i in b if b[i]["assists"] > a[i]["assists"]]
        ob = []
        for s, lab in (("blueTeam", "CFO"), ("redTeam", "KC")):
            x, y = prev[s], f[s]
            if y["towers"] > x["towers"]: ob.append(f"{lab} torre {y['towers']}")
            if y["inhibitors"] > x["inhibitors"]: ob.append(f"{lab} inhib {y['inhibitors']}")
            if y["barons"] > x["barons"]: ob.append(f"{lab} BARON")
            if len(y["dragons"]) > len(x["dragons"]): ob.append(f"{lab} dragon {y['dragons'][-1]}")
        if K or Dd or ob:
            og = f["blueTeam"]["totalGold"] - f["redTeam"]["totalGold"]
            print(f"{mmss(g)} [{t:%H:%M:%S}Z] oro CFO{og:+d} k {f['blueTeam']['totalKills']}-{f['redTeam']['totalKills']} | "
                  f"{' '.join(ob)} | mata {K} muere {Dd} asist {A}")
    prev = f
print("FIN juego", mmss(g), prev["rfc460Timestamp"])
