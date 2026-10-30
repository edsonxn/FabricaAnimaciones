import json, sys
sys.path.insert(0, ".")
from api import get
d = get("getLive")["data"]["schedule"]["events"] or []
for e in d:
    print(json.dumps({k: e.get(k) for k in ("id","startTime","state","type","league")}, ensure_ascii=False)[:300])
    m = e.get("match") or {}
    for t in m.get("teams", []): print("  ", t.get("code"), t.get("result"))
    for s in e.get("streams") or []: print("   stream", s.get("provider"), s.get("parameter"), s.get("locale"))
