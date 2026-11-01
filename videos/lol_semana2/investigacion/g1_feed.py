# Feed oficial de una partida: python g1_feed.py <gameId>  -> feed_<gid>.json (frames cada 10 s) + resumen en pantalla
# (curva de oro cada minuto, objetivos con reloj del feed, marcador final por jugador con details)
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
    ts = [t0 + dt.timedelta(seconds=10 * k) for k in range(int(os.environ.get("NFR", "330")))]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda t: get("window", gid, t), ts))
        det = list(ex.map(lambda t: get("details", gid, t), ts[::6]))
    fr = {}
    for r in res:
        if r:
            for f in r["frames"]: fr[f["rfc460Timestamp"]] = f
    df = {}
    for r in det:
        if r and r.get("frames"):
            for f in r["frames"]: df[f["rfc460Timestamp"]] = f
    D = {"meta": d0["gameMetadata"], "frames": sorted(fr.values(), key=lambda f: f["rfc460Timestamp"]),
         "details": sorted(df.values(), key=lambda f: f["rfc460Timestamp"])}
    json.dump(D, open(cache, "w", encoding="utf-8"))
meta = D["meta"]
fr = [f for f in D["frames"] if f["gameState"] in ("in_game", "paused", "finished")]
ini = iso(fr[0]["rfc460Timestamp"])
print("inicio in_game feed", fr[0]["rfc460Timestamp"], "fin", fr[-1]["rfc460Timestamp"], fr[-1]["gameState"])
print("pausas:", [f["rfc460Timestamp"] for f in D["frames"] if f["gameState"] == "paused"][:5])
def clk(f): s = (iso(f["rfc460Timestamp"]) - ini).total_seconds(); return f"{int(s//60):02d}:{int(s%60):02d}"
for side in ("blue", "red"):
    md = meta[side + "TeamMetadata"]
    print(side, md["esportsTeamId"], [(p["summonerName"], p["championId"], p["role"]) for p in md["participantMetadata"]])
print("== curva de oro (azul - rojo), cada minuto")
nxt = 0
for f in fr:
    s = (iso(f["rfc460Timestamp"]) - ini).total_seconds()
    if s >= nxt:
        b, r = f["blueTeam"], f["redTeam"]
        print(f"{clk(f)} oro {b['totalGold']}-{r['totalGold']} ({b['totalGold']-r['totalGold']:+d}) kills {b['totalKills']}-{r['totalKills']} torres {b['towers']}-{r['towers']} dr {b['dragons']}|{r['dragons']} bar {b['barons']}-{r['barons']} inh {b['inhibitors']}-{r['inhibitors']}")
        nxt += 60
print("== objetivos")
prev = None
for f in fr:
    if prev:
        ev = []
        for side, k in (("AZUL", "blueTeam"), ("ROJO", "redTeam")):
            a, b = prev[k], f[k]
            if len(b["dragons"]) > len(a["dragons"]): ev.append(f"{side} dragón {b['dragons'][-1]} ({len(b['dragons'])})")
            if b["barons"] > a["barons"]: ev.append(f"{side} BARÓN")
            if b["towers"] > a["towers"]: ev.append(f"{side} torre ({b['towers']})")
            if b["inhibitors"] > a["inhibitors"]: ev.append(f"{side} inhibidor ({b['inhibitors']})")
        if ev:
            print(f"{clk(f)} oro {f['blueTeam']['totalGold']-f['redTeam']['totalGold']:+d} kills {f['blueTeam']['totalKills']}-{f['redTeam']['totalKills']} | " + "; ".join(ev))
    prev = f
last = fr[-1]
print("== final", last["rfc460Timestamp"], clk(last))
dl = D["details"][-1] if D["details"] else None
det = {p["participantId"]: p for p in dl["participants"]} if dl else {}
for side, key in (("blue", "blueTeam"), ("red", "redTeam")):
    md = meta[side + "TeamMetadata"]; tm = last[key]
    print(side, "kills", tm["totalKills"], "oro", tm["totalGold"], "torres", tm["towers"], "inh", tm["inhibitors"], "barones", tm["barons"], "dragones", tm["dragons"])
    for pm, p in zip(md["participantMetadata"], tm["participants"]):
        dd = det.get(pm["participantId"], {})
        print(f"   {pm['role']:8s} {pm['summonerName']:18s} {pm['championId']:12s} {p['kills']}/{p['deaths']}/{p['assists']} cs {p['creepScore']} oro {p['totalGold']} nivel {p['level']} dmg% {dd.get('championDamageShare')} kp {dd.get('killParticipation')} items {dd.get('items')}")
