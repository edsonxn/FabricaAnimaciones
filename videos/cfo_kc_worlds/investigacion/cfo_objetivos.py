# Objetivos (dragones, barones, torres, inhibidores) con reloj aprox. del feed oficial: python cfo_objetivos.py <gameId>
import json, sys, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor
def get(gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/window/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
def iso(s): return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
for gid in sys.argv[1:]:
    d0 = get(gid); t0 = iso(d0["frames"][0]["rfc460Timestamp"]); t0 = t0.replace(second=t0.second // 10 * 10)
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda t: get(gid, t), [t0 + dt.timedelta(seconds=10 * k) for k in range(360)]))
    fr = {}
    for r in res:
        if r:
            for f in r["frames"]: fr[f["rfc460Timestamp"]] = f
    fr = [f for f in sorted(fr.values(), key=lambda f: f["rfc460Timestamp"]) if f["gameState"] in ("in_game", "finished")]
    ini = iso(fr[0]["rfc460Timestamp"]); prev = None
    print("==", gid)
    for f in fr:
        if prev:
            s = (iso(f["rfc460Timestamp"]) - ini).total_seconds(); ev = []
            for side, k in (("AZUL", "blueTeam"), ("ROJO", "redTeam")):
                a, b = prev[k], f[k]
                if len(b["dragons"]) > len(a["dragons"]): ev.append(f"{side} dragón {b['dragons'][-1]} ({len(b['dragons'])})")
                if b["barons"] > a["barons"]: ev.append(f"{side} BARÓN")
                if b["towers"] > a["towers"]: ev.append(f"{side} torre ({b['towers']})")
                if b["inhibitors"] > a["inhibitors"]: ev.append(f"{side} inhibidor")
            if ev:
                print(f"{int(s//60):02d}:{int(s%60):02d} oro az-ro {f['blueTeam']['totalGold']-f['redTeam']['totalGold']:+d} kills {f['blueTeam']['totalKills']}-{f['redTeam']['totalKills']} | " + "; ".join(ev))
        prev = f
