# Marcador final de una partida desde el feed oficial: python stats.py <gameId> ...
import json, sys, urllib.request, datetime as dt
def get(gid, t=None, kind="window"):
    u = f"https://feed.lolesports.com/livestats/v1/{kind}/{gid}"
    if t: u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception: pass
def iso(s): return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
for gid in sys.argv[1:]:
    d0 = get(gid); meta = d0["gameMetadata"]
    nom = {p["participantId"]: (p["summonerName"], p["championId"], p["role"]) for s in ("blueTeamMetadata", "redTeamMetadata") for p in meta[s]["participantMetadata"]}
    t0 = iso(d0["frames"][0]["rfc460Timestamp"]); t0 = t0.replace(second=t0.second // 10 * 10)
    ini = fin = None; last = None
    for k in range(0, 75):
        r = get(gid, t0 + dt.timedelta(minutes=k))
        if not r: continue
        for f in r["frames"]:
            if f["gameState"] == "in_game" and ini is None: ini = iso(f["rfc460Timestamp"])
            if f["gameState"] in ("in_game", "finished"): last = f
        if last and last["gameState"] == "finished": break
    # el estado 'finished' llega en cuanto cae el nexo
    dur = (iso(last["rfc460Timestamp"]) - ini).total_seconds()
    print(f"== {gid}  patch {meta.get('patchVersion')}  inicio in_game {ini}  fin {last['rfc460Timestamp'][:19]}  duración feed ≈ {int(dur//60)}:{int(dur%60):02d}")
    for side, key in (("AZUL", "blueTeam"), ("ROJO", "redTeam")):
        T = last[key]
        print(f" {side}: kills {T['totalKills']} oro {T['totalGold']} torres {T['towers']} inhib {T['inhibitors']} barones {T['barons']} dragones {T['dragons']}")
        for p in T["participants"]:
            n = nom[p["participantId"]]
            print(f"   {n[2]:8s} {n[0]:16s} {n[1]:12s} {p['kills']}/{p['deaths']}/{p['assists']}  oro {p['totalGold']} cs {p['creepScore']} nivel {p['level']}")
    det = get(gid, iso(last["rfc460Timestamp"]).replace(second=last["rfc460Timestamp"] and int(last["rfc460Timestamp"][17:19]) // 10 * 10), kind="details")
    if det and det.get("frames"):
        f = det["frames"][-1]
        for p in f["participants"]:
            n = nom[p["participantId"]]
            print(f"   det {n[0]:16s} KP {p.get('killParticipation',0):.2f} dmg% {p.get('championDamageShare',0):.2f} wards {p.get('wardsPlaced')} items {p.get('items')}")
