# Curva de oro de la partida 2 (feed oficial window, cada 10 s): python g2_oro.py <gameId> [mm:ss ...]
# Guarda frames_<gid>.json (caché) y escribe la curva cada 2 min + los instantes pedidos.
import json, sys, os, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
def get(gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/window/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
def iso(s): return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
gid = sys.argv[1]; cache = f"frames_{gid}.json"
if os.path.exists(cache):
    fr = json.load(open(cache, encoding="utf-8"))
else:
    d0 = get(gid); t0 = iso(d0["frames"][0]["rfc460Timestamp"]); t0 = t0.replace(second=t0.second // 10 * 10)
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda t: get(gid, t), [t0 + dt.timedelta(seconds=10 * k) for k in range(200)]))
    m = {}
    for r in res:
        if r:
            for f in r["frames"]: m[f["rfc460Timestamp"]] = f
    fr = [f for f in sorted(m.values(), key=lambda f: f["rfc460Timestamp"]) if f["gameState"] in ("in_game", "finished")]
    json.dump(fr, open(cache, "w", encoding="utf-8"))
ini = iso(fr[0]["rfc460Timestamp"])
def at(s):
    best = None
    for f in fr:
        if (iso(f["rfc460Timestamp"]) - ini).total_seconds() <= s: best = f
    return best
def linea(s):
    f = at(s); b, r = f["blueTeam"], f["redTeam"]
    return (f"{int(s//60):02d}:{int(s%60):02d}  oro T1 {b['totalGold']} MKOI {r['totalGold']} dif {b['totalGold']-r['totalGold']:+d}  "
            f"kills {b['totalKills']}-{r['totalKills']}  torres {b['towers']}-{r['towers']}  dr {len(b['dragons'])}-{len(r['dragons'])}")
print("curva cada 2 min (reloj feed desde in_game)")
for s in range(0, 26 * 60, 120): print(" ", linea(s))
print(" ", linea(25 * 60 + 48))
for a in sys.argv[2:]:
    mm, ss = a.split(":"); print("pedido", linea(int(mm) * 60 + int(ss)))
