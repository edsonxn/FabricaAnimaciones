# -*- coding: utf-8 -*-
"""Escribe busquedas.json: cada beat toma la fuente de SU escena ({"url","desde"}), de los candidatos de `_candidatos.txt`
(yt-dlp ytsearch, 10-nov-2026). Copiado de wow_secretos_primeros_niveles. Mirar las hojas de `medios` y rehacer webcams,
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


PAL = ("u5bh7icrDCc",)   # Paladín 30-60 en Forever sin comentarios (5,8 h): relleno de gameplay real
SRC = {
    "intro": L(("u5bh7icrDCc", 600), ("r_FkSZMFgCc", 120), ("NPbTAXZL_2A", 20), ("74XUkU2RH_w", 200), ("u5bh7icrDCc", 3000), ("h-4cbrrMKWQ", 300), ("u5bh7icrDCc", 6000)),
    "c20": L(("F0pJ7c2xWCQ", 5), ("bGQWLxO36iA", 20), ("dwfROJLXHLA", 300), ("PiFrs3XkUoY", 60), ("sDBhP4jU1e0", 200), ("hD-ywJN2_Dk", 150), ("mP3eP-vMueM", 120)),
    "c19": L(("LHlPJjIPIUE", 120), ("1PnPAK4Ii1k", 200), ("_QnQe62WAOc", 600), ("grlv9T35znU", 900), ("zsJwlTl1TSk", 400), ("u5bh7icrDCc", 1500)),
    "overgear": L(("u5bh7icrDCc", 2200), ("r_FkSZMFgCc", 300)),
    "burla0": L(("u5bh7icrDCc", 2600), ("GvioT1zWgXY", 3000), ("u5bh7icrDCc", 7000)),
    "burla2": L(("u5bh7icrDCc", 10000), ("Jjv4k--Qvwk", 300), ("u5bh7icrDCc", 13000)),
    "c18": L(("zdzOeH9g2Q0", 600), ("KF5VK9e7ucM", 5), ("fvZuWMOLv50", 60), ("d-3Zz97TK3M", 300), ("QeVmTwBtph0", 3)),
    "c17": L(("XAH7oEDAnpE", 10), ("ycGaSqtuoho", 60), ("qa61dZmVeiA", 30), ("CL6IWiZxZQ8", 200), ("qkOfOvMp194", 10), ("pltWOTNRy74", 300)),
    "c16": L(("WyNNa9aX3Ew", 20), ("8qfJq1QuNEA", 60), ("ZcIjILTL078", 120), ("GvioT1zWgXY", 2000), ("ydX7567o-vU", 10), ("r90rwiohKhI", 5), ("pAQ2KFgyHvs", 120)),
    "c15": L(("NoLC1rBoBe0", 30), ("lW7ho5Xtfu4", 60), ("7l3RcYf8jOY", 120), ("WLR7_LzF-O4", 60), ("xgVCC9bk6JM", 20), ("VvkXpiGkoyo", 600)),
    "gracias1": L(("FJdgsycYDWA", 1200), ("KOP5MGBVdoo", 600)),
    "c14": L(("57Gq2A1km6o", 30), ("ALprdmEUPYI", 20), ("uwoRlp5uOb8", 5), ("CU75UnS-6g0", 60), ("MoqhpvfIeW8", 20), ("u5bh7icrDCc", 4000)),
    "c13": L(("46tci5H65b8", 20), ("_EzzFGYTthM", 40), ("0M3fA5TnBGw", 20), ("G5P-hcyv69s", 60), ("wuCrnwAFPzQ", 30), ("1sQpvRfcGjY", 300)),
    "c12": L(("E8HuGKoiZ6k", 120), ("KSE5CSMKWhg", 120), ("el0Thja5_S8", 60), ("0Av3zvIKN0E", 120), ("C-nY0i7Whx4", 600), ("IuAQ1Brg6NA", 20)),
    "c11": L(("tkOAMawttCE", 60), ("G4alWvGP118", 10), ("knrbouuAzJk", 100), ("wRqxzNDqqh4", 60), ("yORZsDUltek", 300), ("5RnQFmjx4Ho", 120), ("JJUUu3dx7ZQ", 120)),
    "burla1": L(("8oEvwddgqso", 120), ("u5bh7icrDCc", 8000), ("Q1Xr-sUaztk", 5)),
    "c10": L(("BcBkQ1m38W0", 60), ("MRv5Q9Wj0ts", 5), ("xAN9StV9eRs", 10), ("V7Nd5aT163M", 30), ("Pp4wTHQKEZY", 10), ("kDmdNVeGZqA", 900), ("LKV2KYofcEc", 120)),
    "c09": L(("ynkW2W30ezE", 30), ("yBmWpV_k9RU", 300), ("TOBQdrxw_aU", 10), ("de1fmWn9Umc", 30), ("zapsbc70dRM", 20), ("9A6RMp223_s", 60), ("u78k0SR1z8g", 60), ("SRBUzCyQbC0", 20)),
    "c08": L(("P8Z-vRs95ck", 20), ("_xcOFCzi5SM", 30), ("a7ejBQCnvE4", 120), ("r9hSoa_u-i0", 60), ("45GIKTF9Cu4", 60), ("cdTVc0d4XBw", 600), ("VpcP81zVTvM", 1800)),
    "c07": L(("enTMsUS3eKA", 30), ("dI9VSkG_m38", 5), ("JDygId9iaRw", 60), ("ZMq2fT88X8g", 120), ("C25iVLryY3k", 600), ("KnXuer7lY8Y", 900)),
    "gracias2": L(("xW1SFPMUwEk", 300), ("Z8LgcYaOi48", 600), ("u5bh7icrDCc", 12000)),
    "c06": L(("NRer4cwoF_I", 5), ("lh1MrYNU_5U", 60), ("Qw-C2eah23Q", 30), ("xU8Pn_rbnaU", 60), ("LJs4D-MEIEA", 5), ("KgLuu-mDZh8", 120), ("NDDICyzoaJ8", 600)),
    "c05": L(("a4KSuGLeK_U", 60), ("t1fFwdBlwGA", 60), ("IbSP9ZB10uM", 120), ("e0TSZHUcnsg", 600), ("OR11ie_disU", 60), ("inOAlrUqXIA", 200), ("csZL5b4IyIs", 60)),
    "c04": L(("_Q_BS8i-icY", 60), ("hnRIUMTjygU", 1200), ("L3EQ1BgqwcU", 1500), ("ohEMSwQmSjw", 10), ("Ap_1PMCLh7k", 10), ("DR0UEalOioc", 300), ("TQ7lSDvQnPs", 300)),
    "c03": L(("55TNsPDlUlo", 30), ("JIypJzisJsY", 20), ("BzIGt9K7BBc", 20), ("PXZwJ9Sdxi4", 10), ("FcoXtun1hDU", 600), ("SQhoL0aPwaM", 900)),
    "c02": L(("hNvrGjK-RWQ", 5), ("x6Pz2Ilyhms", 30), ("N1oab1U4vcE", 600), ("2JyfIgQJrnQ", 900), ("8fetPSKCc3A", 300), ("X2BteR-S-2E", 300), ("HjtxqKdg7pM", 300), ("hPt53BCb7fI", 600), ("a53qlTS-H3I", 120), ("Y_y6GYs7pAk", 200)),
    "c01": L(("laZZOZleHUE", 60), ("JB-4mtyKn_c", 60), ("jR7bRkAdi6A", 30), ("5DZFhW7IDLM", 30), ("YAPOmeaIC7s", 30), ("aeERNuApUic", 120), ("TIuUjzYIdOM", 600), ("u2cfEH4Tjm0", 30), ("fFSts4P228Y", 300)),
    "cierre": L(("639pYfDYE5w", 300), ("oDaueMwxEh8", 600), ("NPbTAXZL_2A", 60), ("u5bh7icrDCc", 15000), ("dvueCoFTkCk", 60)),
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
