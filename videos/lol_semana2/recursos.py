# -*- coding: utf-8 -*-
"""Recursos oficiales del video: fotos de jugadores y logos (API pública de LoL Esports, getTeams) y arte de campeones
(Data Dragon). Lo que ya bajó videos/lol_worlds_2026 se copia de ahí. python videos/lol_semana2/recursos.py"""
import json, os, shutil, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
VIEJO = os.path.join(D, "..", "lol_worlds_2026")
KEY = "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"
EQUIPOS = {"ctbc-flying-oyster": "CFO", "karmine-corp": "KC", "team-liquid": "TLAW", "t1": "T1", "mad-lions": "MKOI",
           "lyon-gaming": "LYON", "team-secret-whales": "TSW", "invictus-gaming": "IG", "bilibili-gaming": "BLG", "top-esports": "TES",
           "los": "LOS", "g2-esports": "G2", "hanwha-life-esports": "HLE", "gen-g-esports": "GEN", "dplus-kia": "DK", "anyones-legend": "AL"}
CAMPEONES = ['Aatrox', 'Akali', 'Alistar', 'Ambessa', 'Anivia', 'Annie', 'Ashe', 'Aurora', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 'Ezreal', 'Galio', 'Gnar', 'Gwen', 'JarvanIV', 'Jayce', 'Jhin', 'KSante', 'Kaisa', 'Kalista', 'Karma', 'Leblanc', 'LeeSin', 'Locke', 'Lucian', 'Lulu', 'Lux', 'Maokai', 'Milio', 'MonkeyKing', 'Nami', 'Nautilus', 'Nocturne', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Qiyana', 'Rakan', 'Renata', 'Renekton', 'Rumble', 'Ryze', 'Sejuani', 'Seraphine', 'Sivir', 'Swain', 'Sylas', 'Syndra', 'Taliyah', 'Tristana', 'Trundle', 'Vi', 'Viktor', 'Xayah', 'XinZhao', 'Yone', 'Yunara', 'Yuumi', 'Zaahen', 'Zeri', 'Ziggs']  # picks de investigacion/datos_*.md


def bajar(url, dst, cab=None):
    if os.path.exists(dst):
        return
    req = urllib.request.Request(url.replace("http://", "https://"), headers=dict({"User-Agent": "Mozilla/5.0"}, **(cab or {})))
    try:
        dat = urllib.request.urlopen(req, timeout=30).read()
    except Exception as e:  # noqa: BLE001
        print("FALLA", url, e)
        return
    if dat[:15].lower().startswith((b"<!doctype", b"<html")):
        print("HTML en vez de imagen", url)
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(dat)


def main():
    jug = os.path.join(D, "pegatinas", "jugadores")
    eq = os.path.join(D, "iconos", "equipos")
    os.makedirs(jug, exist_ok=True)
    os.makedirs(eq, exist_ok=True)
    u = "https://esports-api.lolesports.com/persisted/gw/getTeams?hl=es-MX&id=" + ",".join(EQUIPOS)
    datos = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"x-api-key": KEY})))
    for t in datos["data"]["teams"]:
        cod = EQUIPOS.get(t["slug"])
        if not cod:
            continue
        bajar(t["image"], os.path.join(eq, cod + ".png"))
        for p in t.get("players", []):
            if p.get("image"):
                bajar(p["image"], os.path.join(jug, p["summonerName"] + ".png"))
            print(cod, p["summonerName"], p.get("role"))
    for c in ("T1", "MKOI", "KC", "TES", "FNC", "EDG", "C9", "TLAW", "JDG", "AL", "BLG", "DK", "GEN", "IG", "HLE", "LYON", "TSW"):
        v = os.path.join(VIEJO, "iconos", "equipos", c + ".png")
        if os.path.exists(v) and not os.path.exists(os.path.join(eq, c + ".png")):
            shutil.copy(v, eq)
    for n in ():
        v = os.path.join(VIEJO, "pegatinas", "jugadores", n + ".png")
        if os.path.exists(v):
            shutil.copy(v, jug)
    ver = json.load(urllib.request.urlopen("https://ddragon.leagueoflegends.com/api/versions.json"))[0]
    for c in CAMPEONES:
        bajar(f"https://ddragon.leagueoflegends.com/cdn/{ver}/img/champion/{c}.png", os.path.join(D, "iconos", c + ".png"))
        bajar(f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{c}_0.jpg", os.path.join(D, "splash", c + "_carga.jpg"))
        bajar(f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{c}_0.jpg", os.path.join(D, "splash", c + ".jpg"))
    for s in ("SummonerFlash", "SummonerTeleport", "SummonerSmite"):
        bajar(f"https://ddragon.leagueoflegends.com/cdn/{ver}/img/spell/{s}.png", os.path.join(D, "iconos", s + ".png"))
    print("Data Dragon", ver)


if __name__ == "__main__":
    main()
