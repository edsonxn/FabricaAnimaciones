# Objetivos del feed oficial (dragones, barones, torres, inhibidores) y oro cada minuto: python objetivos.py <gid>
import json, sys, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
def get(gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/window/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
iso = lambda s: dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
gid = sys.argv[1]
d0 = get(gid); t0 = iso(d0["frames"][0]["rfc460Timestamp"]); t0 = t0.replace(second=t0.second // 10 * 10)
ts = [t0 + dt.timedelta(seconds=10 * k) for k in range(0, 6 * 60)]
with ThreadPoolExecutor(12) as ex: res = list(ex.map(lambda t: get(gid, t), ts))
fr = {}
for r in res:
    if r:
        for f in r["frames"]: fr[f["rfc460Timestamp"]] = f
fr = [f for f in sorted(fr.values(), key=lambda f: f["rfc460Timestamp"]) if f["gameState"] in ("in_game", "finished")]
ini = iso(fr[0]["rfc460Timestamp"]); prev = None; ultmin = -1
for f in fr:
    s = (iso(f["rfc460Timestamp"]) - ini).total_seconds(); m = f"{int(s//60):02d}:{int(s%60):02d}"
    b, r = f["blueTeam"], f["redTeam"]
    if prev:
        for lado, x, y in (("AZUL TL", b, prev["blueTeam"]), ("ROJO BLG", r, prev["redTeam"])):
            if len(x["dragons"]) > len(y["dragons"]): print(m, lado, "dragón", x["dragons"][-1], x["dragons"])
            if x["barons"] > y["barons"]: print(m, lado, "BARÓN")
            if x["towers"] > y["towers"]: print(m, lado, "torre", x["towers"])
            if x["inhibitors"] > y["inhibitors"]: print(m, lado, "inhib", x["inhibitors"])
    if int(s // 60) != ultmin:
        ultmin = int(s // 60); print(m, f"   oro TL-BLG {b['totalGold']-r['totalGold']:+d}  kills {b['totalKills']}-{r['totalKills']}")
    prev = f
print("fin", m, f["gameState"])
