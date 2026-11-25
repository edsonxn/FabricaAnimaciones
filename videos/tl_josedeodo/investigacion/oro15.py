# Oro de Josedeodo vs el jungla rival al minuto 15 de juego (feed livestats window; inicio = primer frame in_game)
import json, sys, urllib.request, datetime as dt
def get(gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/window/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
def iso(s): return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
tot = 0
for g in sys.argv[1:]:
    d0 = get(g); meta = d0["gameMetadata"]
    t = iso(d0["frames"][0]["rfc460Timestamp"]); t = t.replace(second=t.second // 10 * 10)
    ini = None
    for k in range(0, 40):
        r = get(g, t + dt.timedelta(seconds=10 * k))
        if r and any(f["gameState"] == "in_game" for f in r["frames"]):
            ini = iso(next(f for f in r["frames"] if f["gameState"] == "in_game")["rfc460Timestamp"]); break
    tt = ini + dt.timedelta(minutes=15); tt = tt.replace(second=tt.second // 10 * 10)
    r = get(g, tt); f = r["frames"][-1]
    res = {}
    for side, key in (("blue", "blueTeam"), ("red", "redTeam")):
        md = meta[side + "TeamMetadata"]
        for pm, p in zip(md["participantMetadata"], f[key]["participants"]):
            if pm["role"] == "jungle": res[side] = (pm["summonerName"], p["totalGold"])
        res[side + "_team"] = f[key]["totalGold"]
    tl = "blue" if "Josedeodo" in res["blue"][0] else "red"; ot = "red" if tl == "blue" else "blue"
    dj = res[tl][1] - res[ot][1]; de = res[tl + "_team"] - res[ot + "_team"]; tot += dj
    print(g, ini, res[tl], res[ot], "dif jungla", dj, "dif equipo", de)
print("media dif jungla", tot / len(sys.argv[1:]))
