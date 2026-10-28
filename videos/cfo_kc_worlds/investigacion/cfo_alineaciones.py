# Alineación de CFO en cada partido LCP 2026 (primer juego completado de cada serie), desde la API + feed oficial
import json, urllib.request, cfo_api
ev = json.load(open("sched_113476371197627891.json", encoding="utf-8"))
for e in ev:
    m = e.get("match") or {}
    if not e["startTime"].startswith("2026") or "CFO" not in [t["code"] for t in m.get("teams", [])]: continue
    d = cfo_api.get("getEventDetails", id=m["id"])["data"]["event"]
    gs = [g for g in d["match"]["games"] if g["state"] == "completed"]
    if not gs: continue
    try:
        w = json.load(urllib.request.urlopen(f"https://feed.lolesports.com/livestats/v1/window/{gs[0]['id']}", timeout=20))
        md = w["gameMetadata"]
        ps = [p for s in ("blueTeamMetadata", "redTeamMetadata") for p in md[s]["participantMetadata"] if p["summonerName"].startswith("CFO")]
        print(e["startTime"][:10], e.get("blockName"), " ".join(f"{p['role'][:3]}:{p['summonerName'][4:]}({p['championId']})" for p in ps))
    except Exception as ex:
        print(e["startTime"][:10], "sin feed", ex)
