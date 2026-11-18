# Utilidades API LoL Esports: python api.py sched <leagueId> [paginas]  -> sched_<id>.json con todos los eventos (paginando hacia atrás)
import json, sys, urllib.request
K = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
B = "https://esports-api.lolesports.com/persisted/gw/"
def get(op, **q):
    qs = "&".join(f"{k}={v}" for k, v in q.items())
    r = urllib.request.Request(f"{B}{op}?hl=en-US&{qs}", headers={"x-api-key": K})
    return json.load(urllib.request.urlopen(r, timeout=30))
if __name__ == "__main__":
    if sys.argv[1] == "sched":
        lid = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        evs = []; tok = None
        for _ in range(n):
            d = get("getSchedule", leagueId=lid, **({"pageToken": tok} if tok else {}))["data"]["schedule"]
            evs = d["events"] + evs
            tok = d["pages"].get("older")
            if not tok: break
        json.dump(evs, open(f"sched_{lid}.json", "w", encoding="utf-8"), ensure_ascii=False)
        print(len(evs), evs[0]["startTime"] if evs else None)
