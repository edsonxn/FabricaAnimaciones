# Feed oficial completo de una partida -> feed_<gid>.json + objetivos (dragones, barones, torres, inhibidores),
# muertes con asesino/asistentes y curva de oro por minuto. python al_feed.py <gameId>
# Reloj = feed (segundos desde el primer frame in_game). HUD = feed - desfase (medirlo en cuadros del VOD).
import json, sys, os, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
def get(kind, gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/{kind}/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(4):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
def iso(s): return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
gid = sys.argv[1]
cache = f"feed_{gid}.json"
if os.path.exists(cache):
    D = json.load(open(cache, encoding="utf-8"))
else:
    d0 = get("window", gid); t0 = iso(d0["frames"][0]["rfc460Timestamp"]); t0 = t0.replace(second=t0.second // 10 * 10)
    ts = [t0 + dt.timedelta(seconds=10 * k) for k in range(300)]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda t: get("window", gid, t), ts))
    fr = {}
    for r in res:
        if r:
            for f in r["frames"]: fr[f["rfc460Timestamp"]] = f
    D = {"meta": d0["gameMetadata"], "frames": sorted(fr.values(), key=lambda f: f["rfc460Timestamp"])}
    json.dump(D, open(cache, "w", encoding="utf-8"))
meta = D["meta"]
nom = {}
for side in ("blue", "red"):
    for pm in meta[side + "TeamMetadata"]["participantMetadata"]:
        nom[pm["participantId"]] = f"{pm['summonerName']}({pm['championId']})"
fr = [f for f in D["frames"] if f["gameState"] in ("in_game", "finished")]
ini = iso(fr[0]["rfc460Timestamp"])
print("frames", len(fr), "inicio", ini, "fin", fr[-1]["rfc460Timestamp"], fr[-1]["gameState"])
def ps(f): return {p["participantId"]: p for k in ("blueTeam", "redTeam") for p in f[k]["participants"]}
def mmss(s): return f"{int(s//60):02d}:{int(s%60):02d}"
prev = None; ultmin = -1
for f in fr:
    s = (iso(f["rfc460Timestamp"]) - ini).total_seconds()
    b, r = f["blueTeam"], f["redTeam"]
    if int(s // 60) != ultmin:
        ultmin = int(s // 60)
        print(f"  [min {ultmin:02d}] oro az-ro {b['totalGold']-r['totalGold']:+d}  kills {b['totalKills']}-{r['totalKills']}  torres {b['towers']}-{r['towers']}")
    if prev:
        ev = []
        for side, k in (("AZUL(AL)", "blueTeam"), ("ROJO(TL)", "redTeam")):
            a, c = prev[k], f[k]
            if len(c["dragons"]) > len(a["dragons"]): ev.append(f"{side} DRAGÓN {c['dragons'][-1]} ({len(c['dragons'])})")
            if c["barons"] > a["barons"]: ev.append(f"{side} BARÓN")
            if c["towers"] > a["towers"]: ev.append(f"{side} torre ({c['towers']})")
            if c["inhibitors"] > a["inhibitors"]: ev.append(f"{side} inhibidor")
        A, B = ps(prev), ps(f)
        K = [f"{nom[i]}+{B[i]['kills']-A[i]['kills']}" for i in B if B[i]["kills"] > A[i]["kills"]]
        Dd = [nom[i] for i in B if B[i]["deaths"] > A[i]["deaths"]]
        As = [nom[i] for i in B if B[i]["assists"] > A[i]["assists"]]
        if K or Dd: ev.append(f"MUERE {Dd} | MATA {K} | ASISTE {As}")
        if ev:
            print(f"feed {mmss(s)} oro {b['totalGold']-r['totalGold']:+d} k {b['totalKills']}-{r['totalKills']} | " + "; ".join(ev))
    prev = f
