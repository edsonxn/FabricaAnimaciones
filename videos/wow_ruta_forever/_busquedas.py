# -*- coding: utf-8 -*-
"""Escribe busquedas.json: cada beat toma la fuente de SU escena ({"url","desde"}), de los candidatos de `_candidatos.txt`
(yt-dlp ytsearch, 19-nov-2026; capítulos comprobados con `yt-dlp --print "%(duration)s %(chapters)s"`). Copiado de
wow_oro_forever/_busquedas.py. `desde` nunca pasa de la duración real (de `_candidatos.json`). Un cuadro de cada fuente se miró
en hojas (1 s con --download-sections, sin bajar el video): fuera webcams (Nekrage, Raxamelius, Shindigg, Cassidy Darkstar,
Gloria, Xesol con avatar, StorisForever), rótulos fijos de otro canal (Dandylion «Let's Play Druid», logo de Blizzplanet beta)
y retail moderno. Fuentes principales, todas sin narrar: fwengli (serie «protection warrior pve leveling 1-60», Alianza, 99 partes
con la zona en el título), DankeyKong («Full Dungeon Clear - Longplay no Commentary»), Loopy Longplays (capítulos por subzona),
ambientes de Forever sin interfaz (Azeroth Ambience, NFGames, Wanderer's Hearth, BigChunkyTV) y, solo para zonas viejas sin
cambios (Arathi, Silithus, Peste del Este, Cuna, Un'Goro, Desolace, Tierras Inhóspitas, Mil Agujas), Meisio «Vanilla …» (Classic).
`python _busquedas.py --check` = solo comprueba SRC (escenas cubiertas, ids sin duración, offsets fuera)."""
import json
import os
import re
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
import guion  # noqa: E402


def Y(i):
    return "https://www.youtube.com/watch?v=" + i


def L(*pares):
    return [(Y(i), d) for i, d in pares]


# Relleno: dos longplays de Forever sin comentarios (Loopy Longplays). dlGeYLM0RI8 = brujo no-muerto (11 h; capítulos: 5772 Rémol,
# 15207 Entrañas, 30820 El Sepulcro, 36862 zepelín, 36947 Orgrimmar); sdAXLJUlags = sacerdote humano (8,8 h; 99 Villanorte,
# 3482 posada de Villadorada, 24214 Páramos, 27964 Colina del Centinela, 28225 Granja Alexston, 31195 pesca).
PAL = ("dlGeYLM0RI8", "sdAXLJUlags")
SRC = {
    # Ruta de Classic de memoria, zona nueva (Claros del Río), Hyjal, Alianza/Horda, posada y vuelo.
    "intro": L(("Ak0z7iSgH38", 300), ("N1oab1U4vcE", 1200), ("eK06h9XuCvI", 300), ("ZDOvf5r8TC0", 300), ("dlGeYLM0RI8", 4700),
               ("Ak0z7iSgH38", 1500), ("sdAXLJUlags", 3500), ("8aBwVTAnZLI", 26300), ("UMh80-64QLc", 600)),
    # Valles iniciales (Villanorte, Villadorada, Kharanos), Durotar, Isla Zephras, Elwynn, Fuerte de Bandarion (Tirisfal), Hogger.
    "p01": L(("sdAXLJUlags", 200), ("sdAXLJUlags", 3560), ("8aBwVTAnZLI", 3950), ("CpsfPD8JOZg", 1500), ("rL6_4K8_x5A", 3000),
             ("AAymw7k7jR4", 3000), ("sdAXLJUlags", 5400), ("R86WtDgehJY", 1200), ("sdAXLJUlags", 22300), ("QAGqdbWCmBM", 1500)),
    # Páramos (Colina del Centinela), Thelsamar, Costa Oscura, Los Baldíos, El Sepulcro, Salón de Señores Feudales (Hall of Thanes,
    # bajo Forjaz), Ruinas de Lordaeron, Granja Alexston (bolsa de dormir).
    "p02": L(("sdAXLJUlags", 24300), ("sdAXLJUlags", 27970), ("8aBwVTAnZLI", 24400), ("iSmlVgquXcU", 1500), ("3KISbNT5vNM", 1500),
             ("dlGeYLM0RI8", 30900), ("CSv7bEPMW0U", 300), ("UPt60kl1YGY", 300), ("HIxQ8uciSUc", 1500), ("sdAXLJUlags", 28240)),
    # Crestagrana (Villa del Lago), Vallefresno, Sierra Espolón, Minas de la Muerte, Cuevas de los Lamentos.
    "p03": L(("KGVdQ9qrp8c", 600), ("qtNLHvY926Q", 1500), ("niUqkQa8JnE", 1500), ("-6DqrXkNAHc", 1500), ("0GquZRuYXSc", 1500),
             ("KGVdQ9qrp8c", 1800), ("-rAOOKGNwgw", 1500), ("xgPyJ9lGKaQ", 2500), ("Nzq3dPw0i1k", 600), ("qDaLs8oeIOo", 1500)),
    "burla0": L(("sdAXLJUlags", 3600), ("8aBwVTAnZLI", 26600), ("pepk2VjNNbo", 3000)),
    # Bosque del Ocaso, Los Humedales (misiones nuevas), Vallefresno, Laderas de Trabalomas, zepelín Tirisfal-Orgrimmar, Colmillo
    # Oscuro, Cavernas de Brazanegra.
    "p04": L(("YB6wy2QdtAw", 1500), ("YBfzO8D8UeY", 2000), ("lvKtYowar-M", 1500), ("niUqkQa8JnE", 2500), ("YTJHwf1GZd8", 600),
             ("dlGeYLM0RI8", 38100), ("dlGeYLM0RI8", 36880), ("w-XXzLGrDw0", 1500), ("C5T25m4AIDY", 600), ("xvcEWz8LUsY", 600)),
    # Las Mil Agujas, Desierto de Sal, Sitio de Excavación de Los Humedales (raptores), Horado Rajacieno, Gnomeregan.
    "p05": L(("CRQ6kDVJBzc", 600), ("0fyfJX1_7yA", 600), ("K0mxgeVrWH0", 1500), ("iszBTrTEn4I", 600), ("StrO37BK9ec", 1500),
             ("6IwHjdVhctM", 700), ("Q53WW36_kBs", 1500), ("58BBfrSSpa8", 1500), ("6IwHjdVhctM", 1200)),
    # Arathi (Classic, sin cambios), Laderas/Alterac, Dalaran sobre Alterac y su mazmorra, Desolace, Monasterio Escarlata.
    "p06": L(("jOJC-qG3v9g", 300), ("jOJC-qG3v9g", 1500), ("jOJC-qG3v9g", 2700), ("YTJHwf1GZd8", 2000), ("bQXbsVQotFc", 1500),
             ("kqan4pO91m8", 2000), ("UZ7tLg_H-6c", 300), ("agf2NHPHn0I", 2500), ("RKcqwk8Ivtg", 14200), ("GMal7M01l84", 300)),
    # Vega de Tuercespina (Rebeldes, Nesingwary, Bahía del Botín), Marjal Revolcafango, Tierras Inhóspitas, La Ciudad Anegada, Uldaman.
    "p07": L(("5DInpqWarTY", 1500), ("nel13bjFTtY", 1500), ("6H5hypjnLE8", 1500), ("t7M5yl2Y78A", 1500), ("2EG0tAiPpT8", 4000),
             ("bWr3nnslZGw", 1500), ("dRYYoKJJUkg", 600), ("1kFLDwY0FAs", 1500), ("dRYYoKJJUkg", 2000), ("nZkVwoqAuwE", 1200)),
    "burla1": L(("dlGeYLM0RI8", 36960), ("7GLjcxgoUuk", 300), ("CpsfPD8JOZg", 4000)),
    # Claros del Río (Riverglades): llegada a pie, Fortaleza de Farholde, barco de Tanaris, Rog'mar, vuelos, Bastión de Krol'dok, lagos.
    "p08": L(("N1oab1U4vcE", 600), ("TNI8WYnd04E", 600), ("ZDOvf5r8TC0", 1500), ("ZDOvf5r8TC0", 200), ("ouHkhET8sCQ", 1500),
             ("w29Fkd50C9c", 100), ("yJavcEqLTt8", 5), ("c-UUA1ri5e4", 5), ("gYYw3oDi6vQ", 1500), ("57dre4k97Ho", 300),
             ("57dre4k97Ho", 1500), ("g4shdXqgqp8", 3000), ("Jx13kl7zgQ8", 1500), ("xcsMXfjZUYA", 2000)),
    "gracias1": L(("sdAXLJUlags", 3520), ("N1oab1U4vcE", 5000), ("sdAXLJUlags", 31250), ("N1oab1U4vcE", 9000)),
    # Shen'dralas: Valle de los Huesos, campamentos, centauros y shen'dralar; Aldea Cazasombras; Maraudon.
    # 1ZBGXQP49Js (capítulos): 0 Valley of Bones, 636 Outcast Hideaway, 1043 Shen'dralas, 1498 Magram Front, 1557 Forlorn Gardens.
    "p09": L(("a53qlTS-H3I", 200), ("1ZBGXQP49Js", 60), ("Y_y6GYs7pAk", 300), ("1ZBGXQP49Js", 1100), ("1ZBGXQP49Js", 700),
             ("1ZBGXQP49Js", 1510), ("1ZBGXQP49Js", 1570), ("RKcqwk8Ivtg", 13000), ("kzsTv_MrJ3M", 600), ("a53qlTS-H3I", 600)),
    "burla2": L(("1ZBGXQP49Js", 1700), ("1ZBGXQP49Js", 1200), ("Y_y6GYs7pAk", 450)),
    # Tanaris (Gadgetzan), equitación al 40, Feralas, Tierras del Interior, Zul'Farrak, Dalaran, muelle goblin.
    "p10": L(("tVj0XCwcc38", 100), ("HmsBzSMGlKM", 40), ("RKcqwk8Ivtg", 1400), ("9nZzTkK2Up8", 1500), ("7W2i__XIZm4", 1500),
             ("mRNqMdyJ-Wk", 1500), ("Of7K9stJBhA", 1200), ("kqan4pO91m8", 4000), ("kBA79xWzLAw", 1200), ("N3QOQegDvf4", 1500)),
    # Un'Goro, Azshara renovada, Prisión de Alcaz, La Garganta de Fuego, Tierras Devastadas, Templo de Atal'Hakkar.
    "p11": L(("mlzkgjTETX4", 600), ("aXR9GdyHcX4", 1500), ("2YUFXSPh5Lw", 30), ("2YUFXSPh5Lw", 120), ("omVtE6GLogk", 60),
             ("1Lxs5e_kPSc", 1500), ("omVtE6GLogk", 700), ("IO8iKuChHoc", 1500), ("A9dzFCjg2Bo", 1500), ("Wlc4VpUjnTE", 1500)),
    # Las Estepas Ardientes, vuelo de Farholde, Tierras de la Peste del Oeste, Profundidades de Roca Negra.
    "p12": L(("CtXjiVLxo6w", 2000), ("zf7qveNtYy0", 1500), ("c-UUA1ri5e4", 5), ("-cmE-w8Uyao", 1500), ("t-no7r8BR7M", 300),
             ("WWUxcpmAexg", 600), ("OkN6453Wjh8", 3000), ("rcUsDHO7QMc", 1500), ("zf7qveNtYy0", 2500)),
    "gracias2": L(("sdAXLJUlags", 16200), ("UMh80-64QLc", 4500), ("qtNLHvY926Q", 2500)),
    # Cuna del Invierno, Silithus, Peste del Este (Capilla), Bastión Faucenegra (Azshara).
    "p13": L(("63Kdh9JTEoQ", 1500), ("RBleypaLOPo", 1500), ("C25iVLryY3k", 1500), ("6UPvyboCIf8", 640), ("g_bDII8Gofc", 1500),
             ("9ocjLryl4II", 25), ("FIUHDfx1lmY", 600), ("FIUHDfx1lmY", 1500), ("FIUHDfx1lmY", 3500), ("8ckHY-hmCQw", 1500)),
    # Monte Hyjal de Forever (Laderas Maculadas, Santuario de Aviana, Nordrassil) y El Bancal del Creador (Shaper's Terrace).
    # QVin8qs0h4A (capítulos): 184 Tainted Foothills, 1423 Summit of Eternity, 1522 Hyjal Summit Raid Entrance.
    "p14": L(("eK06h9XuCvI", 300), ("xMu-ntOsDpw", 300), ("Og-F93kmgbI", 900), ("QVin8qs0h4A", 190), ("55HBXBVUhn0", 300),
             ("QVin8qs0h4A", 1480), ("cQrWYBvskro", 1500), ("JVEwH22Ra3A", 1500), ("JVEwH22Ra3A", 3500), ("QVin8qs0h4A", 1530)),
    "cierre": L(("N1oab1U4vcE", 10000), ("ZDOvf5r8TC0", 2700), ("1ZBGXQP49Js", 1000), ("eK06h9XuCvI", 1100), ("Ak0z7iSgH38", 2500),
                ("UMh80-64QLc", 6800)),
}
RELLENO = L((PAL[0], 9000), (PAL[1], 12000))


# FIJADO A MANO por beat (revisión de las hojas de `medios`): gana sobre SRC al regenerar. Vacío hasta la primera revisión.
FIJO = {   # ronda 1 (19-nov-2026, hojas de 3 cuadros por clip): motivo en _rehacer.txt
    "scene-013": ("8aBwVTAnZLI", 3957), "scene-014": ("QAGqdbWCmBM", 600), "scene-019": ("sdAXLJUlags", 22306),
    "scene-020": ("CpsfPD8JOZg", 1500), "scene-025": ("CSv7bEPMW0U", 300), "scene-026": ("UPt60kl1YGY", 300),
    "scene-027": ("3KISbNT5vNM", 1500), "scene-028": ("sdAXLJUlags", 28240), "scene-032": ("-6DqrXkNAHc", 1500),
    "scene-033": ("KGVdQ9qrp8c", 1200), "scene-036": ("xgPyJ9lGKaQ", 2500), "scene-037": ("Nzq3dPw0i1k", 600),
    "scene-038": ("-rAOOKGNwgw", 1500), "scene-049": ("w-XXzLGrDw0", 1530), "scene-050": ("UPt60kl1YGY", 900),
    "scene-052": ("xvcEWz8LUsY", 600), "scene-058": ("Q53WW36_kBs", 1500),
    "scene-059": ("58BBfrSSpa8", 1500), "scene-060": ("6IwHjdVhctM", 700), "scene-069": ("agf2NHPHn0I", 1200),
    "scene-070": ("GMal7M01l84", 300), "scene-078": ("bWr3nnslZGw", 2000), "scene-087": ("ouHkhET8sCQ", 1800),
    "scene-088": ("w29Fkd50C9c", 100), "scene-091": ("g4shdXqgqp8", 3000), "scene-093": ("57dre4k97Ho", 2500),
    "scene-094": ("57dre4k97Ho", 900), "scene-096": ("g4shdXqgqp8", 6000), "scene-099": ("N1oab1U4vcE", 3000),
    "scene-109": ("kzsTv_MrJ3M", 600), "scene-110": ("a53qlTS-H3I", 700), "scene-113": ("Y_y6GYs7pAk", 470),
    "scene-114": ("Ngpi1TkXOJA", 600), "scene-116": ("_ciyszkqp8U", 2300), "scene-118": ("mRNqMdyJ-Wk", 1500),
    "scene-119": ("mRNqMdyJ-Wk", 2600), "scene-121": ("BMPzO8CNuf8", 1500), "scene-129": ("IO8iKuChHoc", 600),
    "scene-133": ("zf7qveNtYy0", 600), "scene-135": ("-cmE-w8Uyao", 2000), "scene-145": ("RBleypaLOPo", 2200),
    "scene-148": ("FIUHDfx1lmY", 1500), "scene-151": ("g_bDII8Gofc", 1500), "scene-153": ("bUUN-RVAgZM", 2600),
    "scene-154": ("bUUN-RVAgZM", 3100), "scene-155": ("bUUN-RVAgZM", 1800), "scene-158": ("JVEwH22Ra3A", 700),
    "scene-161": ("N1oab1U4vcE", 7000), "scene-006": ("N1oab1U4vcE", 4000), "scene-029": ("3KISbNT5vNM", 2500), "scene-084": ("N1oab1U4vcE", 8000),
    "scene-051": ("dlGeYLM0RI8", 31380),
}


def _duraciones():
    """id -> segundos, de _candidatos.json (yt-dlp ya los midió)."""
    d = {}
    try:
        c = json.load(open("_candidatos.json", encoding="utf-8"))
    except Exception:
        return d
    for qs in c.values():
        for lst in qs.values():
            for x in lst:
                try:
                    d[x[0]] = float(x[1])
                except (TypeError, ValueError, IndexError):
                    pass
    return d


DUR = _duraciones()


def _id(url):
    return url.rsplit("=", 1)[-1]


def desde_seguro(url, desde):
    """Nunca más allá de la duración (deja 15 s de margen); si se pasa, da la vuelta."""
    dur = DUR.get(_id(url))
    if not dur:
        return float(desde)
    tope = max(1.0, dur - 15)
    return float(desde % tope) if desde > tope else float(desde)


def _norm(s):
    s = re.sub(r"\[[^\]]+\]", " ", s)
    return re.sub(r"[^a-záéíóúñü0-9]+", " ", s.lower()).strip()


FRASES = [(e["id"], _norm(f)) for e in guion.ESCENAS for f in e["frases"]]


def escena_de(texto):
    t = _norm(texto)
    for eid, f in FRASES:
        if f[:40] and f[:40] in t:
            return eid
    for eid, f in FRASES:
        if t[:30] and t[:30] in f:
            return eid
    return None


def comprobar():
    ids = [e["id"] for e in guion.ESCENAS]
    faltan = [i for i in ids if i not in SRC]
    sobran = [k for k in SRC if k not in ids]
    malos, sin = [], set()
    for k, lst in list(SRC.items()) + [("RELLENO", RELLENO)]:
        for url, d in lst:
            dur = DUR.get(_id(url))
            if dur is None:
                sin.add(_id(url))
            elif d > dur - 15:
                malos.append(f"{k}:{_id(url)}@{d}>{dur:.0f}")
    print(f"{len(ids)} escenas · faltan {faltan or '-'} · sobran {sobran or '-'}")
    print("sin duración:", sorted(sin) or "-")
    print("offset fuera (se corrige solo):", malos or "-")
    print("fuentes por escena:", ", ".join(f"{k}:{len(v)}" for k, v in SRC.items()))
    return not faltan


if __name__ == "__main__":
    if "--check" in sys.argv or not os.path.exists("beats.json"):
        if not os.path.exists("beats.json"):
            print("(aún no hay beats.json: solo compruebo SRC)")
        sys.exit(0 if comprobar() else 1)
    b = json.load(open("beats.json", encoding="utf-8"))
    out, cuenta, prev = {}, {}, "intro"
    for x in b:
        eid = escena_de(x.get("texto", "")) or prev
        prev = eid
        x["_esc"] = eid
        lst = SRC.get(eid) or RELLENO
        n = cuenta.get(eid, 0)
        cuenta[eid] = n + 1
        e = lst[n % len(lst)]
        if isinstance(e, tuple):
            url, desde = e
            out[x["id"]] = {"url": url, "desde": desde_seguro(url, desde + 25 * (n // len(lst)))}
        else:
            out[x["id"]] = e
    for k, (i, d) in FIJO.items():
        if k in out:
            out[k] = {"url": Y(i), "desde": float(d)}
    json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({x["id"]: x["_esc"] for x in b}, open("_beat_escena.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(out), "beats ·", ", ".join(f"{k}:{v}" for k, v in cuenta.items()))
