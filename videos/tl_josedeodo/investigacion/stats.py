# python stats.py gid ... -> marcador final por jugador (feed oficial window + details), JSON en stats_<gid>.json
import json, sys, urllib.request, datetime as dt
def get(kind, gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/{kind}/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
def iso(s): return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
for gid in sys.argv[1:]:
    d0 = get("window", gid); meta = d0["gameMetadata"]
    t0 = iso(d0["frames"][0]["rfc460Timestamp"]); t0 = t0.replace(second=t0.second // 10 * 10)
    last = None; k = 20
    while k < 80:
        r = get("window", gid, t0 + dt.timedelta(minutes=k))
        if r and r["frames"]:
            last = r["frames"][-1]
            if last["gameState"] == "finished": break
        k += 1
    rd = get("details", gid, iso(last["rfc460Timestamp"]).replace(second=iso(last["rfc460Timestamp"]).second // 10 * 10))
    det = {p["participantId"]: p for p in rd["frames"][-1]["participants"]} if rd and rd.get("frames") else {}
    out = {"gid": gid, "end": last["rfc460Timestamp"], "teams": {}}
    for side, key in (("blue", "blueTeam"), ("red", "redTeam")):
        md = meta[side + "TeamMetadata"]; tm = last[key]
        out["teams"][side] = {"esportsTeamId": md["esportsTeamId"], "kills": tm["totalKills"], "gold": tm["totalGold"],
                              "towers": tm["towers"], "barons": tm["barons"], "dragons": tm["dragons"], "players": []}
        for pm, p in zip(md["participantMetadata"], tm["participants"]):
            dd = det.get(pm["participantId"], {})
            out["teams"][side]["players"].append({"name": pm["summonerName"], "champ": pm["championId"], "role": pm["role"],
                "k": p["kills"], "d": p["deaths"], "a": p["assists"], "cs": p["creepScore"], "gold": p["totalGold"],
                "dmgShare": dd.get("championDamageShare"), "kp": dd.get("killParticipation"), "wards": dd.get("wardsPlaced")})
    json.dump(out, open(f"stats_{gid}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(gid, out["end"], {s: (v["kills"], v["gold"], v["towers"], v["barons"], len(v["dragons"])) for s, v in out["teams"].items()})
