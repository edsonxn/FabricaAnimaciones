# Muertes con asesino y asistentes, resolución ~1 s del feed: python asist.py <gid> <feed_menos_hud>
import json, sys, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
def get(gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/window/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
iso = lambda s: dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
gid, off = sys.argv[1], float(sys.argv[2])
d0 = get(gid); meta = d0["gameMetadata"]
nom = {p["participantId"]: f'{p["summonerName"]}({p["championId"]})' for s in ("blueTeamMetadata", "redTeamMetadata") for p in meta[s]["participantMetadata"]}
t0 = iso(d0["frames"][0]["rfc460Timestamp"]); t0 = t0.replace(second=t0.second // 10 * 10)
ts = [t0 + dt.timedelta(seconds=10 * k) for k in range(0, 6 * 60)]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda t: get(gid, t), ts))
fr = {}
for r in res:
    if r:
        for f in r["frames"]: fr[f["rfc460Timestamp"]] = f
fr = [f for f in sorted(fr.values(), key=lambda f: f["rfc460Timestamp"]) if f["gameState"] in ("in_game", "finished")]
ini = iso(fr[0]["rfc460Timestamp"]); prev = None
print("inicio in_game feed", fr[0]["rfc460Timestamp"], "fin", fr[-1]["rfc460Timestamp"])
for f in fr:
    ps = {p["participantId"]: p for p in f["blueTeam"]["participants"] + f["redTeam"]["participants"]}
    if prev:
        mu = [nom[i] for i, p in ps.items() if p["deaths"] > prev[i]["deaths"]]
        ma = [nom[i] + f"+{p['kills']-prev[i]['kills']}" for i, p in ps.items() if p["kills"] > prev[i]["kills"]]
        asi = [nom[i] for i, p in ps.items() if p["assists"] > prev[i]["assists"]]
        if mu or ma:
            s = (iso(f["rfc460Timestamp"]) - ini).total_seconds(); h = s - off
            print(f"feed {int(s//60):02d}:{int(s%60):02d} (HUD~{int(h//60):02d}:{int(h%60):02d}) MUEREN {mu} | MATAN {ma} | ASISTEN {asi}")
    prev = ps
