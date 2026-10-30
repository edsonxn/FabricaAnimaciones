# Curva de oro de la G2 por MINUTO DE JUEGO (reloj sin pausas, como g2_reloj.py): python g2_curva.py <gameId>
import json, sys, datetime as dt
gid = sys.argv[1]
D = json.load(open(f"feed_{gid}.json", encoding="utf-8"))
def iso(s): return dt.datetime.fromisoformat(s.rstrip("Z")[:23])
fr = [f for f in D["frames"] if f["gameState"] in ("in_game", "paused", "finished")]
g = 0.0; prev = None; nxt = 0
for f in fr:
    if prev and prev["gameState"] == "in_game":
        g += (iso(f["rfc460Timestamp"]) - iso(prev["rfc460Timestamp"])).total_seconds()
    if g >= nxt and f["gameState"] != "paused":
        b, r = f["blueTeam"], f["redTeam"]
        print(f"{int(g//60):02d}:{int(g%60):02d} [{f['rfc460Timestamp'][11:19]}Z] CFO{b['totalGold']-r['totalGold']:+6d} k {b['totalKills']}-{r['totalKills']} "
              f"torres {b['towers']}-{r['towers']} dr {len(b['dragons'])}-{len(r['dragons'])} bar {b['barons']}-{r['barons']} inh {b['inhibitors']}-{r['inhibitors']}")
        nxt = (int(g // 60) + 1) * 60
    prev = f
b, r = prev["blueTeam"], prev["redTeam"]
print("FIN", f"{int(g//60):02d}:{int(g%60):02d}", f"CFO{b['totalGold']-r['totalGold']:+d}", b['totalKills'], r['totalKills'])
