# -*- coding: utf-8 -*-
"""Escribe busquedas.json: cada beat toma la fuente de SU escena ({"url","desde"}), de los candidatos de `_candidatos.txt`
(yt-dlp ytsearch, 12-nov-2026). Copiado de wow_secretos_primeros_niveles (vía `_busquedas_ref.py`). Mirar las hojas de `medios` y rehacer webcams,
caras, rótulos de otros canales o webs."""
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


# Relleno: dos longplays de Forever sin comentarios. dlGeYLM0RI8 = brujo no-muerto (11 h, capítulos: 5944 Taberna de Brill,
# 15207 Entrañas, 34532 murciélago, 36862 zepelín, 36947 Orgrimmar); UMh80-64QLc = paladín humano (2 h, Elwynn).
PAL = ("dlGeYLM0RI8", "UMh80-64QLc")
SRC = {
    "intro": L(("xmWBweJBqic", 600), ("NPbTAXZL_2A", 20), ("rJ6uG-u33GY", 400), ("r_FkSZMFgCc", 120), ("n2a7vzV7o-s", 60), ("loJCGO2MTjc", 900), ("xXaXYxcbA6A", 40)),
    "friccion": L(("gJD03H11xis", 1200), ("QGNb2s2sQkU", 2400), ("n2a7vzV7o-s", 200), ("7sWSTsZu50c", 300), ("8DslDEPpU0U", 1800), ("UMh80-64QLc", 2500)),
    "c30": L(("lwLQEhWiIiE", 160), ("BNS8BDdQLhA", 235), ("7ZmA4Jy6ixU", 30), ("hHxI1I35rkw", 90), ("demZZ0R-JCw", 60), ("lwLQEhWiIiE", 2310), ("2yse8T2UETM", 3200)),
    "c29": L(("0pCMcYoMeJg", 150), ("eJQBYuej3C4", 60), ("sZHmYgnT0fA", 20), ("jhFU9GRimbQ", 5), ("Uuhnwny2xT8", 900), ("dlGeYLM0RI8", 5800)),
    "c28": L(("Wsmzfhhf9PM", 715), ("fYS4Jt7QZR0", 3), ("EguKMRe0ZtU", 300), ("JdY-XOfn580", 10), ("mxKH8WJ3Ock", 2), ("dpAsOYlF4KU", 90), ("nP5uOou48k8", 600), ("DCSqtD9MfDg", 600)),
    "overgear": L(("dlGeYLM0RI8", 9000), ("UMh80-64QLc", 3500)),
    "burla0": L(("Kl36u5sujeg", 5), ("G9dyx6t7pwU", 5), ("dlGeYLM0RI8", 20000)),
    "c27": L(("rMTgC3Gt9zI", 620), ("gJtZyyJada0", 9000), ("G54Cq4QFxp4", 30), ("fzQSyDmnoAI", 5), ("wKo9Nyo32EE", 1500), ("g2u7XAmCvL0", 30)),
    "c27b": L(("BNS8BDdQLhA", 400), ("UMh80-64QLc", 300), ("rMTgC3Gt9zI", 900)),   # add-on Voces en español: tapar con captura propia
    "burla1": L(("r1PCoQk0t8o", 90), ("wTOp82SGS-w", 1050), ("UMh80-64QLc", 5000)),
    "c26": L(("LHlPJjIPIUE", 120), ("YGBfPfzxCf8", 40), ("loJCGO2MTjc", 1500), ("xMzWaSXAzYg", 120), ("ka1mtP4NeJ8", 300), ("ka1mtP4NeJ8", 900), ("UMh80-64QLc", 6000)),
    "c25": L(("y43dR8LdLJE", 10), ("TEqxbwyDZQc", 30), ("00X9g_G7X0A", 5), ("8yUhuAaHXwY", 10), ("19j3dDgmWnM", 400), ("mhsVvF8s2r4", 600), ("Noz_qCICxqs", 120)),
    "c24": L(("1rg10ueI5Vg", 5), ("FFar0-nA2bM", 60), ("Rbs_9GcWDDs", 600), ("QGNb2s2sQkU", 4000), ("1mB0BEMm7WE", 3), ("YER5Qnhfd0M", 10), ("G9IIA4sgV-8", 30)),
    "c23": L(("Zu-t67-ebL4", 30), ("dlGeYLM0RI8", 36870), ("9YGfJkhhhUg", 40), ("uTrG-K9Lgqs", 20), ("a2LFnBZwaLU", 40), ("hZHk98CniLk", 20), ("dlGeYLM0RI8", 37400)),
    "c22": L(("uGHD83yIg3w", 5), ("5n-t8iOWOQY", 15), ("dARGlaGpJ64", 230), ("33S82jVRJco", 150), ("XmofywfCCBI", 10), ("s2EvvISbrxE", 5), ("hiDFh4GB21k", 60)),
    "c21": L(("I2waqOFv3JI", 60), ("oH99ASPSARg", 120), ("Ag4snkiemOY", 60), ("BAs3fi51LR8", 280), ("b3qTfL9RHDA", 10), ("jhWJPCLFsdo", 120), ("sQVU81yKZIs", 150)),
    "gracias1": L(("Uuhnwny2xT8", 1500), ("2hufFGenEWg", 5), ("UMh80-64QLc", 4500)),
    "c20": L(("YIhM35KjtyA", 30), ("SxQ0akozRL4", 120), ("TPcpFs3nNAY", 5), ("ZJ5WFDkLmrI", 60), ("K1-JjQauk-Y", 5), ("pdA15s50Hjc", 90), ("VK4UwbL85_w", 120)),
    "c19": L(("9AlEQvn4dlc", 10), ("kQlAPtj8g1I", 60), ("TvLcpFXAID0", 260), ("7KzYue4AKnU", 60), ("s_iAWEzJlk8", 1200), ("8DslDEPpU0U", 900), ("epsdq5NycVc", 1500)),
    "c18": L(("EK0Vj6LigIA", 20), ("x6s0xovrd2c", 30), ("8wp7uIPD1K8", 20), ("o1BdQBCkwag", 60), ("54t1WT4bF2c", 60), ("gJtZyyJada0", 20000)),
    "c17": L(("IPFF3dbEqhk", 3), ("dlGeYLM0RI8", 5950), ("siGaJvUTqGI", 60), ("OdgUUoL5eys", 10), ("AfHAHa2PjFY", 30), ("i4_7V_PXDPg", 1200), ("LTCJWI9NtNY", 1500)),
    "c16": L(("vFeN_Nk6za8", 20), ("YftiAddJBgk", 20), ("d0_SDiINAGE", 20), ("yZ75kCyU--4", 20), ("z261xIcXq_Y", 10), ("1lg9vQb9nh0", 5), ("ZVoKCa0ut28", 60)),
    "c15": L(("hs0s4oGa6bg", 60), ("UOm1NIT1Djs", 225), ("0rcZ-n6QGQk", 40), ("G9N_IuRvWEM", 90), ("vYenK1CLCmI", 90), ("HzHk_atMyjg", 5), ("AdL1QZ3rp4Q", 2)),
    "c14": L(("Rbs_9GcWDDs", 1500), ("PtSADAfgVn0", 1200), ("OjMoqnTzTP8", 30), ("7vqX47_gBnU", 60), ("OjMoqnTzTP8", 1180), ("TvLcpFXAID0", 1800), ("4XmoW1ag0jQ", 150), ("m_qRGQo9lKw", 60)),
    "c13": L(("LW1veoIJasc", 600), ("gJtZyyJada0", 3000), ("LW1veoIJasc", 2400), ("IPTPsJpz5ZE", 3), ("Ta3mRzg9oM0", 300), ("OlfAv0PJy28", 10), ("q0EHhgh05f8", 10), ("7-W7DjmiyzQ", 120)),
    "c12": L(("YT-lEDJge2Q", 5), ("gELZS8minTw", 5), ("dEqRKj04ots", 60), ("7F-4IeZZXII", 120), ("Le87L0LocOU", 60), ("ULv7zylvbUc", 60), ("-TKf3fmvbWc", 5)),
    "c11": L(("ClioKSmb3aw", 60), ("r2P0OqqGCxo", 1630), ("uQ2THBTjRYo", 120), ("M54OOETkX9k", 1480), ("XVN82fnA4uI", 60), ("M54OOETkX9k", 1305), ("5kuJowGULAk", 300)),
    "gracias2": L(("wKo9Nyo32EE", 800), ("cekQL_cWDgg", 60), ("dlGeYLM0RI8", 25000)),
    "c10": L(("J3jjcGwvQMw", 60), ("6L1aWHKpRQY", 40), ("ipzdLbJG3DE", 60), ("9wtL-vIkOgM", 120), ("loJCGO2MTjc", 200), ("tE7JhgYhc-Q", 200), ("cekQL_cWDgg", 120)),
    "c09": L(("jN_UR1ipkbg", 60), ("Ciw0Qu74hPU", 5), ("6qhqW6eGNlI", 5), ("kGIbXBMOwWE", 3), ("P5RrW-YGt4k", 3), ("lkDzbPWVvDE", 300)),
    "c08": L(("1l-WVCn4E7k", 5), ("PBpdFI94vIM", 10), ("BCE2OEahm6k", 10), ("t3FClbeBIOc", 60), ("RsTh987_ZWI", 60), ("Pat1iPhQKCA", 120), ("qI5kw-RxDq8", 60)),
    "c07": L(("d9etc6FqhCQ", 60), ("sXkQ09MZUzI", 40), ("pSrVhIXh6-I", 50), ("xJ5JF7HAnjs", 30), ("4-ccDcesiBc", 60), ("NN2IbC6LSQA", 120), ("cPRZSZSbtSE", 100), ("bB76gr2jUvI", 150), ("UEH61UM9Uj4", 60), ("NN2IbC6LSQA", 500)),
    "c06": L(("71vNSwulB5w", 10), ("v6MpEscz3o8", 20), ("5hc4Ap50Zrg", 60), ("tUZC0GA1EOA", 3), ("bHSjP_fq9Lo", 120), ("mgfbB-bsR0Y", 60), ("QLnEHLfF_wU", 60)),
    "burla2": L(("xmWBweJBqic", 1800), ("gxHastTxBLk", 600), ("FFar0-nA2bM", 300)),
    "c05": L(("gJD03H11xis", 300), ("_Kq-mqFpsQk", 5), ("bJXClzo9JJk", 30), ("1Nd5BJ9n3Lk", 5), ("qoA-h5j1Ed0", 120), ("2JJIMKpKgVU", 5), ("gJD03H11xis", 2400)),
    "c04": L(("wTOp82SGS-w", 15), ("AMNb5wreFDc", 300), ("dlGeYLM0RI8", 36960), ("dlGeYLM0RI8", 15220), ("UEkgrypKvR4", 30), ("9Pp41mtchxE", 3), ("V8C3W1FuyYg", 3), ("wTOp82SGS-w", 1060)),
    "c03": L(("3E2gvZK1LaM", 3), ("Kl36u5sujeg", 5), ("HcJDMaKRuqo", 5), ("PlW8w2vhhK0", 60), ("xj1472f3Fg4", 300), ("UMh80-64QLc", 6600)),
    "c02": L(("udQhEKs_krg", 10), ("J3XxrQ_Grfo", 15), ("3CT6tfjdUAM", 10), ("WXrH74pQfUY", 600), ("M54OOETkX9k", 995), ("rg45jlTFtIU", 3), ("M54OOETkX9k", 632), ("4NnGqD8GtwA", 1200)),
    "c01": L(("eh6KpYQ08dM", 600), ("om7LTU-xWlk", 60), ("DMqrugPh9EU", 300), ("prF5YkgsOfQ", 1200), ("xmWBweJBqic", 2400), ("19j3dDgmWnM", 700), ("LW1veoIJasc", 1500), ("FO68us8GExM", 1500)),
    "cierre": L(("UMh80-64QLc", 6800), ("53ETqBtcafk", 6000), ("BNS8BDdQLhA", 2000), ("wTOp82SGS-w", 400), ("NPbTAXZL_2A", 120), ("xXaXYxcbA6A", 150)),
}


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


if __name__ == "__main__":
    b = json.load(open("beats.json", encoding="utf-8"))
    out, cuenta, prev = {}, {}, "intro"
    for x in b:
        eid = escena_de(x.get("texto", "")) or prev
        prev = eid
        x["_esc"] = eid
        lst = SRC[eid]
        n = cuenta.get(eid, 0)
        cuenta[eid] = n + 1
        e = lst[n % len(lst)]
        if isinstance(e, tuple):
            url, desde = e
            out[x["id"]] = {"url": url, "desde": float(desde + 25 * (n // len(lst)))}
        else:
            out[x["id"]] = e
    json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({x["id"]: x["_esc"] for x in b}, open("_beat_escena.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(out), "beats ·", ", ".join(f"{k}:{v}" for k, v in cuenta.items()))
