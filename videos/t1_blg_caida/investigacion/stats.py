# Estadísticas de la serie BLG-T1 (semifinal Worlds 2026) desde el feed oficial livestats `window`.
# Por partida: oro/CS/nivel por jugador a los 10, 15, 20 min y al final; diferencias por posición; dragones (tipo y
# minuto), torres, barones e inhibidores en el tiempo. Salida: stats_g<n>.json + resumen en pantalla.
import json, sys, urllib.request, datetime as dt
from concurrent.futures import ThreadPoolExecutor

JUEGOS = {1: "115660540726095122", 2: "115660540726095123", 3: "115660540726095124", 4: "115660540726095125"}
ROLES = ["top", "jungla", "medio", "tirador", "apoyo"]

def get(gid, t=None):
    u = f"https://feed.lolesports.com/livestats/v1/window/{gid}"
    if t:
        u += "?startingTime=" + t.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(u, timeout=20))
        except Exception:
            pass
    return None

def iso(s):
    return dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")

def juego(n):
    gid = JUEGOS[n]
    d0 = get(gid)
    meta = d0["gameMetadata"]
    lados = {}
    nombres = {}
    for side, col in (("blueTeamMetadata", "azul"), ("redTeamMetadata", "rojo")):
        for k, p in enumerate(meta[side]["participantMetadata"]):
            nombres[p["participantId"]] = dict(nombre=p["summonerName"], campeon=p["championId"], lado=col, rol=ROLES[k])
    t0 = iso(d0["frames"][0]["rfc460Timestamp"])
    t0 = t0.replace(second=t0.second // 10 * 10)
    ts = [t0 + dt.timedelta(seconds=10 * k) for k in range(0, 6 * 50)]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(lambda t: get(gid, t), ts))
    frames = {}
    for r in res:
        if r:
            for f in r["frames"]:
                frames[f["rfc460Timestamp"]] = f
    fr = sorted(frames.values(), key=lambda f: f["rfc460Timestamp"])
    fr = [f for f in fr if f["gameState"] in ("in_game", "finished")]
    ini = iso(fr[0]["rfc460Timestamp"])
    def seg(f):
        return (iso(f["rfc460Timestamp"]) - ini).total_seconds()
    def en(minuto):
        mejor = min(fr, key=lambda f: abs(seg(f) - minuto * 60))
        return mejor
    def foto(f):
        ps = {p["participantId"]: p for p in f["blueTeam"]["participants"] + f["redTeam"]["participants"]}
        out = {}
        for i, p in ps.items():
            m = nombres[i]
            out[m["nombre"]] = dict(campeon=m["campeon"], lado=m["lado"], rol=m["rol"], oro=p["totalGold"], cs=p["creepScore"],
                                    nivel=p["level"], k=p["kills"], d=p["deaths"], a=p["assists"])
        eq = {}
        for col, t in (("azul", f["blueTeam"]), ("rojo", f["redTeam"])):
            eq[col] = dict(oro=t["totalGold"], kills=t["totalKills"], torres=t["towers"], inhib=t["inhibitors"],
                           barones=t["barons"], dragones=t["dragons"])
        return dict(t=round(seg(f)), jugadores=out, equipos=eq)
    # eventos de objetivos
    eventos = []
    prev = None
    for f in fr:
        if prev:
            for col, a, b in (("azul", prev["blueTeam"], f["blueTeam"]), ("rojo", prev["redTeam"], f["redTeam"])):
                if len(b["dragons"]) > len(a["dragons"]):
                    eventos.append((round(seg(f)), col, "dragon", b["dragons"][-1]))
                if b["towers"] > a["towers"]:
                    eventos.append((round(seg(f)), col, "torre", b["towers"]))
                if b["barons"] > a["barons"]:
                    eventos.append((round(seg(f)), col, "baron", b["barons"]))
                if b["inhibitors"] > a["inhibitors"]:
                    eventos.append((round(seg(f)), col, "inhib", b["inhibitors"]))
        prev = f
    azul = meta["blueTeamMetadata"]["participantMetadata"][0]["summonerName"]
    out = dict(n=n, gid=gid, inicio=str(ini), azul_top=azul, duracion=round(seg(fr[-1])),
               fotos={m: foto(en(m)) for m in (5, 10, 15, 20, 25)}, final=foto(fr[-1]), eventos=eventos,
               oro=[[round(seg(f)), f["blueTeam"]["totalGold"] - f["redTeam"]["totalGold"]] for f in fr[::3]])
    json.dump(out, open(f"stats_g{n}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out

def t1(nombre):
    return nombre.startswith("T1 ")

if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or [1, 2, 3, 4]
    with ThreadPoolExecutor(4) as ex:
        outs = list(ex.map(juego, ns))
    for o in outs:
        print(f"\n===== G{o['n']}  duración {o['duracion']//60}:{o['duracion']%60:02d}  azul = {'T1' if t1(o['azul_top']) else 'BLG'}")
        for m in (10, 15, 20):
            js = o["fotos"][m]["jugadores"]
            fila = []
            for rol in ROLES:
                a = [v | dict(n=k) for k, v in js.items() if v["rol"] == rol and t1(k)][0]
                b = [v | dict(n=k) for k, v in js.items() if v["rol"] == rol and not t1(k)][0]
                fila.append(f"{rol[:3]} {a['n']}({a['campeon']}) {a['oro']-b['oro']:+d}/{a['cs']-b['cs']:+d}cs vs {b['n']}({b['campeon']})")
            print(f" min {m} (t={o['fotos'][m]['t']}): " + " | ".join(fila))
        js = o["final"]["jugadores"]
        print(" final KDA: " + ", ".join(f"{k} {v['campeon']} {v['k']}/{v['d']}/{v['a']} cs{v['cs']}" for k, v in js.items()))
        print(" eventos:", "; ".join(f"{t//60}:{t%60:02d} {c} {e} {x}" for t, c, e, x in o["eventos"]))
