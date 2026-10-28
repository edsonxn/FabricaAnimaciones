# Escanea el feed oficial (livestats window) cada 10 s y lista las muertes con el reloj aproximado de la partida.
import json, sys, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor

def get(gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/window/{gid}"
    if t:
        u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try:
            return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception:
            pass
    return None

def iso(s):
    return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")

for gid in sys.argv[1:]:
    d0 = get(gid)
    meta = d0["gameMetadata"]
    nombres = {p["participantId"]: (p["summonerName"], p["championId"]) for side in ("blueTeamMetadata", "redTeamMetadata")
               for p in meta[side]["participantMetadata"]}
    t0 = iso(d0["frames"][0]["rfc460Timestamp"])
    t0 = t0.replace(second=t0.second // 10 * 10)
    ts = [t0 + dt.timedelta(seconds=10 * k) for k in range(0, 6 * 60)]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda t: get(gid, t), ts))
    frames = {}
    for r in res:
        if not r:
            continue
        for f in r["frames"]:
            frames[f["rfc460Timestamp"]] = f
    fr = sorted(frames.values(), key=lambda f: f["rfc460Timestamp"])
    fr = [f for f in fr if f["gameState"] in ("in_game", "finished")]
    ini = iso(fr[0]["rfc460Timestamp"])
    prev = None
    print(f"== {gid} {meta['blueTeamMetadata']['participantMetadata'][0]['summonerName']} (azul) vs "
          f"{meta['redTeamMetadata']['participantMetadata'][0]['summonerName']} (rojo); inicio feed {ini}")
    for f in fr:
        ps = {p["participantId"]: p for p in f["blueTeam"]["participants"] + f["redTeam"]["participants"]}
        if prev:
            seg = (iso(f["rfc460Timestamp"]) - ini).total_seconds()
            ev = []
            for i, p in ps.items():
                q = prev[i]
                if p["deaths"] > q["deaths"]:
                    ev.append("†" + nombres[i][0] + "/" + nombres[i][1])
                if p["kills"] > q["kills"]:
                    ev.append("K " + nombres[i][0] + "x" + str(p["kills"] - q["kills"]))
            if ev:
                b, r = f["blueTeam"], f["redTeam"]
                print(f"{int(seg//60):02d}:{int(seg%60):02d}  {b['totalKills']}-{r['totalKills']} oro {b['totalGold']-r['totalGold']:+d} "
                      f"dr {len(b['dragons'])}-{len(r['dragons'])} bar {b['barons']}-{r['barons']} | " + ", ".join(ev))
        prev = ps
        last = f
    print("final", last["blueTeam"]["totalKills"], last["redTeam"]["totalKills"], last["gameState"])
