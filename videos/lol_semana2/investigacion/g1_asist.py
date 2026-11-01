# Quién mató, quién murió y quién asistió en cada cambio del feed (diferencia de K/D/A por jugador entre frames de 10 s).
# python g1_asist.py <gameId>   (usa feed_<gid>.json de g1_feed.py). Reloj = feed; HUD = feed - 4 s (medido en el VOD).
import json, sys, datetime as dt
gid = sys.argv[1]
D = json.load(open(f"feed_{gid}.json", encoding="utf-8"))
def iso(s): return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
meta = D["meta"]
nom = {}
for side in ("blue", "red"):
    for pm in meta[side + "TeamMetadata"]["participantMetadata"]:
        nom[pm["participantId"]] = f"{pm['summonerName']}({pm['championId']})"
fr = [f for f in D["frames"] if f["gameState"] in ("in_game", "finished")]
ini = iso(fr[0]["rfc460Timestamp"])
def ps(f): return {p["participantId"]: p for k in ("blueTeam", "redTeam") for p in f[k]["participants"]}
prev = None
for f in fr:
    if prev:
        a, b = ps(prev), ps(f)
        K = [f"{nom[i]}+{b[i]['kills']-a[i]['kills']}" for i in b if b[i]["kills"] > a[i]["kills"]]
        Dd = [nom[i] for i in b if b[i]["deaths"] > a[i]["deaths"]]
        A = [nom[i] for i in b if b[i]["assists"] > a[i]["assists"]]
        if K or Dd:
            s = (iso(f["rfc460Timestamp"]) - ini).total_seconds(); h = s - 4
            print(f"feed {int(s//60):02d}:{int(s%60):02d} (HUD~{int(h//60):02d}:{int(h%60):02d}) MUEREN {Dd} | MATAN {K} | ASISTEN {A}")
    prev = f
