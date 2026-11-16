# -*- coding: utf-8 -*-
"""Escribe busquedas.json: cada beat toma la fuente de SU escena ({"url","desde"}), de los candidatos de `_candidatos.txt`
(yt-dlp ytsearch, 15-nov-2026; capítulos comprobados con `yt-dlp --print "%(duration)s %(chapters)s"`). Copiado de
wow_forever_experiencia/_busquedas.py. Añadido: `desde` nunca pasa de la duración real (de `_candidatos.json`), para no bajar
archivos vacíos. Mirar las hojas de `medios` y rehacer webcams, caras, rótulos de otros canales o webs.
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


# Relleno: dos longplays de Forever sin comentarios. dlGeYLM0RI8 = brujo no-muerto (11 h, capítulos: 5944 Taberna de Brill,
# 15207 Entrañas, 34532 murciélago, 36862 zepelín, 36947 Orgrimmar); UMh80-64QLc = paladín humano (2 h, Elwynn).
PAL = ("dlGeYLM0RI8", "UMh80-64QLc")
SRC = {
    # Nivel 40, instructor de equitación, bolsa vacía, doble especialización, épica de 1000.
    "intro": L(("HmsBzSMGlKM", 10), ("s0UgqWRk-mM", 45), ("knrbouuAzJk", 60), ("HmsBzSMGlKM", 50), ("s0UgqWRk-mM", 250),
               ("RY0zM-aAJkY", 120), ("UMh80-64QLc", 600), ("dlGeYLM0RI8", 36947)),
    # Instructor de clase (ventana con la lista de hechizos y precios).
    "c30": L(("TRYuJ04wdRE", 5), ("kKvaZd7YK_A", 5), ("vexDAo_msDk", 3), ("m1LZbpM3PpM", 60), ("uBj0YuizXsA", 5),
             ("MWxG1eUxy8w", 20), ("9G0HvNepm_A", 8), ("-qFAfVNWIXU", 30)),
    # Montura de clase: corcel vil (Strahad Farsan, Trinquete) y caballo de paladín.
    "c29": L(("jNe_U7WNtdU", 800), ("1lg9vQb9nh0", 10), ("CnpbBmAFXHg", 5), ("tgYT9cTFJLI", 520), ("IeJRcRrgc2o", 20),
             ("jNe_U7WNtdU", 130), ("z261xIcXq_Y", 20), ("EbkIW4xzlPU", 5)),
    # Instructor de equitación (Randal Hunter / Orgrimmar), reputación Honorable.
    "c28": L(("h0kzmlHRJW8", 20), ("e-1lrIIoY6c", 30), ("CHN2qD_OnIo", 20), ("2XbrlM-J8nA", 5), ("ZaVydajljH0", 50),
             ("s0UgqWRk-mM", 60), ("knrbouuAzJk", 200)),
    "burla0": L(("loJCGO2MTjc", 1200), ("7sWSTsZu50c", 300), ("SoBYCMXkjfs", 2000), ("5ArXTkfbt_0", 900)),
    # Ventana de Legado (Frequent Flier, Regateo, Reforzar = árbol Resourcefulness).
    "c27": L(("lM6AHmF0SAo", 300), ("00zjeevQXeo", 520), ("YhMY0pahLIM", 210), ("G2GeV-6a250", 230), ("GuvTVObAWGE", 40),
             ("cTgwYAtrcm0", 60), ("EoOuPZKl_Rs", 530), ("00zjeevQXeo", 300)),
    # Talentos / doble especialización / reespecializar con el instructor.
    "c26": L(("pqMweoyfzP4", 40), ("r94J2rjwNKU", 10), ("E8HuGKoiZ6k", 20), ("k1yCOd2N-1A", 20), ("IuAQ1Brg6NA", 20),
             ("lrxDUQzxdVc", 120), ("pqMweoyfzP4", 150)),
    # Casa de subastas con equipo verde.
    "c25": L(("yORZsDUltek", 810), ("yj-FpwFGBM0", 10), ("vwa_fCCHJOU", 10), ("yORZsDUltek", 116), ("wZWBPvezGNs", 2),
             ("WPwyz37A3IQ", 60), ("dj_9AWtpfqs", 100), ("LStkmcnFTCg", 60)),
    # Desuello / minería / herboristería mientras se sube.
    "c24": L(("Xpb0uVUPS04", 120), ("kLywz7PJxPk", 160), ("lt-cdpNDvow", 60), ("Pu356oge3t0", 60), ("fiNNeEqK3N0", 40),
             ("Xpb0uVUPS04", 220), ("dl8UiC1sBos", 60), ("kLywz7PJxPk", 230)),
    # Auctionator: escaneo completo, tooltip con dos precios, pestaña vender.
    "c23": L(("Wp_ghkuDU5E", 10), ("yORZsDUltek", 600), ("f4Qy4KZaX2E", 65), ("13JMw14SMIs", 30), ("yORZsDUltek", 710),
             ("CFHlqeoMJFk", 120), ("2CP44i3pe0E", 120)),
    # Publicar: duración y depósito; subastas neutrales (Gadgetzan, Bahía del Botín).
    "c22": L(("nrKEdHSJufM", 20), ("yORZsDUltek", 142), ("4_K-z45ujcE", 5), ("4VqtRbOlj2M", 10), ("Du_t4zxS4wY", 150),
             ("V_EzxrJuaCk", 5), ("CB3XTvNHCx4", 200), ("W4tLdtyZfXo", 60)),
    # Comprar por debajo del vendedor y vender al PNJ.
    "c21": L(("wRqxzNDqqh4", 30), ("HjBs8wEp6v4", 100), ("sB_OeR2pL2E", 100), ("VmsjGA3MlA0", 60), ("ndWzTAd9h38", 120),
             ("DHRRmR1GRbI", 60), ("2CP44i3pe0E", 300)),
    "gracias1": L(("MsO2tHZtGdY", 3000), ("Rbs_9GcWDDs", 1500), ("RtQiT1aSAPU", 800), ("UMh80-64QLc", 4500)),
    # Personaje banco junto al buzón y la subasta, desencantar.
    "c20": L(("JR0u0xdknrs", 40), ("j21MYHOtqTI", 60), ("gJgTmMyETS8", 185), ("1LP9tzreRMc", 10), ("JR0u0xdknrs", 215),
             ("JTwhOFmwLkQ", 60), ("mNYFXUN6_TQ", 80), ("83V_-NR_TN0", 20)),
    # Chol'aruk (élite jabaespín, Los Baldíos) e Isla Zephras.
    "c19": L(("C0Li5yHiZKw", 3), ("m9RW9BjEHME", 10), ("Ag2v_WLPNJ4", 700), ("m9RW9BjEHME", 60), ("Ag2v_WLPNJ4", 1100),
             ("5E725_ldT54", 230), ("ZcL2qAXRSPg", 100), ("rL6_4K8_x5A", 1200)),
    # Bolsas: Bolsa de tejido mágico roja (14) y Darkmoon Storage Box; Feria de la Luna Negra.
    "c18": L(("JBmvXda1b40", 50), ("tNcihXIyf70", 380), ("FRmsHpiU0_c", 60), ("tNcihXIyf70", 480), ("sXkQ09MZUzI", 220),
             ("d9etc6FqhCQ", 205), ("JBmvXda1b40", 555), ("oFxp54SCBA8", 60)),
    # Tela de humanoides, vendas de seda (Primeros auxilios).
    "c17": L(("yNIOcN0FChQ", 10), ("hMmT8L7XYI0", 10), ("EF9SR5bxOrk", 40), ("xzw78zoYkdQ", 5), ("QKd7nKit2NU", 100),
             ("dLqfn_mTnAs", 20), ("iPfK21nz7C8", 5)),
    "burla1": L(("wTOp82SGS-w", 300), ("kNIoC-QWaEg", 1500), ("orZKldgYCAw", 900), ("UMh80-64QLc", 5000)),
    # Las verdes colinas de Tuercespina: páginas y capítulos.
    "c16": L(("F0pJ7c2xWCQ", 5), ("ptmO1ZZuArA", 20), ("U4i_thwB0nE", 10), ("PiFrs3XkUoY", 60), ("bGQWLxO36iA", 30),
             ("LwxLwxPcr3M", 10), ("DLYBsDYP6Xw", 10), ("CocRRyd-mis", 900)),
    # Pesca en mar abierto y baúles.
    "c15": L(("BAs3fi51LR8", 590), ("lDni4r02lkE", 10), ("2dqcV8xmsCg", 600), ("BAs3fi51LR8", 680), ("RBNIiy3vdr4", 60),
             ("pEise4LPe2Y", 100), ("kyNSAiPvK-w", 30), ("2dqcV8xmsCg", 1500)),
    # Caña de pescar de hierro grande y trampas de marisco de Desolace.
    "c14": L(("AsFG17jcoCQ", 5), ("mPgzwBLLS8Y", 30), ("ZZlcVMO9Ntc", 60), ("BlV0vVmQWCI", 40), ("-kBqtFIn5yk", 30),
             ("vOOnPOf_tTQ", 60), ("qG9ZDPVXIr8", 20), ("ftVv67Yu8-o", 60)),
    # Supervendedor 680 con la caravana de Gizelton; receta de filete de lobo magro.
    "c13": L(("bqSipMJh46s", 5), ("jpF6MBXOJnc", 62), ("dVPhOoyr99Q", 5), ("jpF6MBXOJnc", 5), ("v1HdOknErOw", 60),
             ("teqLBWXkzow", 10), ("xkYys8EpBs8", 100), ("G_Z3toDv6iA", 30)),
    # Talismanes de los exiliados de Arathi; Hacha de torbellino.
    "c12": L(("w1WXYfN6fps", 15), ("_PMu4S9-74w", 10), ("igHxERi6idE", 570), ("hl1UKzCA8-I", 600), ("jOJC-qG3v9g", 1200),
             ("igHxERi6idE", 740), ("hl1UKzCA8-I", 2000), ("w82aEH84ssk", 60)),
    # Almejas gigantes bajo el agua (Arrecife Vil) y perlas; misión de las Tierras Inhóspitas.
    "c11": L(("77jCWn5pN-Y", 840), ("-KVRrRno70A", 30), ("pf936y1hc9Q", 30), ("j54EXgmJvmU", 600), ("GDzvpbmvByo", 300),
             ("77jCWn5pN-Y", 900), ("xwQNbp4kibc", 200), ("j54EXgmJvmU", 3000)),
    "gracias2": L(("yipNuUNGupk", 1200), ("FgsvhJmJpQA", 1500), ("g42Lo8IXAzk", 3000)),
    # Huevos gigantes: rocs de Tanaris, lechúcicos, Clamlette Surprise (Gadgetzan).
    "c10": L(("YW6SNBBT3MA", 20), ("WzVbdJH62gw", 100), ("YW6SNBBT3MA", 150), ("ZKeKtuAbrfo", 10), ("Xs0Ch-ecOOc", 1800),
             ("YW6SNBBT3MA", 300), ("28v2LOOG68w", 30), ("xFRgrqJt8Sc", 1200)),
    # Grises caros: grifos de Feralas, granjeros de Trabalomas (horcas).
    "c09": L(("dSz-qa1iBJY", 1200), ("2_S04f0USJw", 5), ("XbVkci_8oVk", 1500), ("Wz_zHsP7N78", 40), ("3ec-C3i3tjY", 60),
             ("dSz-qa1iBJY", 2400), ("ANA932N3edk", 100), ("kZnOXnZvqhM", 60)),
    # Tortugas de Tanaris (Planeadores de oleaje), almejas y perlas.
    "c08": L(("hGa3Q0bGd7s", 130), ("IBOqcRt39pY", 190), ("Y8jnaxp5XG4", 60), ("eK9ZaMQxLGA", 5), ("hGa3Q0bGd7s", 490),
             ("IBOqcRt39pY", 370), ("hGa3Q0bGd7s", 780), ("Xs0Ch-ecOOc", 2500)),
    # Waylaid Crates, Shipping Label, campamento de comerciantes.
    "c07": L(("pdA15s50Hjc", 60), ("K1-JjQauk-Y", 5), ("ivAmLe-KcBI", 10), ("ZJ5WFDkLmrI", 260), ("HFyD0XxW9Ls", 3),
             ("VK4UwbL85_w", 50), ("avfQmYaNApA", 60), ("teUQwIPbuk0", 100)),
    # Recetas nuevas que se compran con Favor; fórmula de encantar collar.
    "c06": L(("aKBaJ7-N8js", 5), ("WJGRdu2vjVs", 65), ("uBQZE-5Dk_U", 5), ("LhnBvLK_ZgE", 5), ("WJGRdu2vjVs", 240),
             ("Gdj-5mpq6hI", 5), ("VK4UwbL85_w", 240), ("rXTzqJjDu0Q", 5)),
    "burla2": L(("Kw1SZYipZUc", 200), ("Js78sTFOii8", 1200), ("GjQZ9Pjlr58", 100)),
    # Invertir para las bandas: Onyxia, cardopresto, fuego elemental, pociones de resistencia al fuego.
    "c05": L(("jR7bRkAdi6A", 20), ("xFGcTAOoAcM", 5), ("RMIMsfpa2nk", 140), ("zUJ7B8igRk8", 10), ("buRZA_NMkf8", 200),
             ("pbf59qftoHg", 40), ("pwWw_0IL-l8", 30), ("RMIMsfpa2nk", 330)),
    # Adornos brillantes, restos flotantes, Viejo Heming (Bahía del Botín).
    "c04": L(("vz31HMRlWl8", 10), ("kyNSAiPvK-w", 50), ("9N5AJamxhjY", 60), ("qEsyoclnExw", 10), ("tCkL4m9fSds", 100),
             ("0cq9AaKI0Dw", 30), ("Z9qh6SM42Po", 3), ("g2cM0IrZgBE", 3000)),
    # Sátiros Jadefire (Frondavil) y Legashi (Azshara): paño rúnico y tela vil.
    "c03": L(("4LiU968WpjA", 60), ("8Cb1CGY8W7U", 35), ("uDnixLCpQyo", 70), ("yzH6PW_cvyw", 10), ("zveEB8e-8f4", 60),
             ("huvCbLz6nLk", 40), ("uDnixLCpQyo", 485), ("8Cb1CGY8W7U", 380)),
    # Vetas de torio ricas (Las Estepas Ardientes), Cristal Arcano, mercado negro de Riverglades.
    "c02": L(("Fpn7WB0xwhU", 20), ("t7mGg5DPH-A", 870), ("y1Bl2EE7nIU", 20), ("t7mGg5DPH-A", 1060), ("RmVmKoBRfqA", 30),
             ("zSU-8Jy0s1E", 5), ("5tLSKOmhSXI", 20), ("N1oab1U4vcE", 2000)),
    # Misiones 48+ con oro, nota del hotfix, Monte Hyjal.
    "c01": L(("xMu-ntOsDpw", 300), ("v_8K17c2qc0", 30), ("YB1bXPZ3-OE", 600), ("84Nyu57rqCc", 40), ("_r_TqtE2XlI", 40),
             ("ujf50gVZoRY", 60), ("xMu-ntOsDpw", 900), ("WgjAayGBY2Q", 4000)),
    "cierre": L(("UMh80-64QLc", 6800), ("53ETqBtcafk", 6000), ("BNS8BDdQLhA", 2000), ("wTOp82SGS-w", 400),
                ("1rB82LPbgH0", 1500), ("8aBwVTAnZLI", 20000)),
}
RELLENO = L((PAL[0], 9000), (PAL[1], 3500))


# FIJADO A MANO por beat (revisión de las hojas de `medios`, 15-nov-2026): gana sobre SRC al regenerar.
# Motivo de cada uno en _rehacer.txt (webcam, rótulos/diapositivas de otro canal, web, caricatura, formato no disponible).
FIJO = {
    "scene-099": ("YFyyslnV8gw", 120),
    "scene-006": ("s0UgqWRk-mM", 150), "scene-016": ("1lg9vQb9nh0", 50), "scene-029": ("UMh80-64QLc", 1500),
    "scene-030": ("YhMY0pahLIM", 100), "scene-031": ("dlGeYLM0RI8", 34560), "scene-035": ("GuvTVObAWGE", 110),
    "scene-036": ("IuAQ1Brg6NA", 60), "scene-038": ("uBj0YuizXsA", 20), "scene-041": ("IuAQ1Brg6NA", 100),
    "scene-042": ("13JMw14SMIs", 90), "scene-044": ("Du_t4zxS4wY", 34), "scene-045": ("j54EXgmJvmU", 650),
    "scene-047": ("lt-cdpNDvow", 150), "scene-048": ("fiNNeEqK3N0", 100), "scene-049": ("fiNNeEqK3N0", 180),
    "scene-051": ("13JMw14SMIs", 150), "scene-053": ("Du_t4zxS4wY", 210), "scene-055": ("ndWzTAd9h38", 250),
    "scene-056": ("13JMw14SMIs", 210), "scene-059": ("13JMw14SMIs", 173), "scene-060": ("ndWzTAd9h38", 550),
    "scene-061": ("4VqtRbOlj2M", 45), "scene-062": ("Du_t4zxS4wY", 136), "scene-067": ("Du_t4zxS4wY", 100),
    "scene-068": ("ivAmLe-KcBI", 50), "scene-070": ("JTwhOFmwLkQ", 120), "scene-072": ("ivAmLe-KcBI", 90),
    "scene-076": ("dlGeYLM0RI8", 37600), "scene-077": ("gJgTmMyETS8", 60), "scene-080": ("dlGeYLM0RI8", 37200),
    "scene-084": ("C0Li5yHiZKw", 25), "scene-086": ("m9RW9BjEHME", 100), "scene-087": ("JTwhOFmwLkQ", 10),
    "scene-088": ("sXkQ09MZUzI", 100), "scene-089": ("sXkQ09MZUzI", 200), "scene-090": ("YFyyslnV8gw", 59),
    "scene-093": ("JTwhOFmwLkQ", 220), "scene-094": ("JTwhOFmwLkQ", 280), "scene-107": ("PiFrs3XkUoY", 200),
    "scene-108": ("lDni4r02lkE", 50), "scene-111": ("kyNSAiPvK-w", 84), "scene-125": ("_PMu4S9-74w", 50),
    "scene-128": ("hl1UKzCA8-I", 1500), "scene-135": ("RtQiT1aSAPU", 1700), "scene-142": ("WzVbdJH62gw", 300),
    "scene-147": ("XbVkci_8oVk", 2000), "scene-149": ("hGa3Q0bGd7s", 200), "scene-153": ("eK9ZaMQxLGA", 18),
    "scene-155": ("HFyD0XxW9Ls", 15), "scene-157": ("VK4UwbL85_w", 120), "scene-162": ("aKBaJ7-N8js", 25),
    "scene-165": ("LhnBvLK_ZgE", 30), "scene-168": ("RtQiT1aSAPU", 2500), "scene-169": ("pwWw_0IL-l8", 60),
    "scene-171": ("zUJ7B8igRk8", 40), "scene-173": ("pbf59qftoHg", 150), "scene-177": ("vz31HMRlWl8", 60),
    "scene-179": ("qEsyoclnExw", 45), "scene-187": ("t7mGg5DPH-A", 1500), "scene-192": ("y1Bl2EE7nIU", 80),
    "scene-194": ("xMu-ntOsDpw", 1100), "scene-195": ("xMu-ntOsDpw", 600), "scene-069": ("YFyyslnV8gw", 66),
    # Ronda 4 (15-nov-2026, revisión del usuario): voz ↔ imagen y rótulos quemados.
    "scene-050": ("zcsAQCNgS5M", 596), "scene-110": ("kyNSAiPvK-w", 114), "scene-144": ("jDyl3g6etsY", 45),
    "scene-145": ("2_S04f0USJw", 1), "scene-201": ("8aBwVTAnZLI", 34000), "scene-057": ("13JMw14SMIs", 106),
    "scene-112": ("pEise4LPe2Y", 100),
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
    """Nunca más allá de la duración (deja 12 s de margen); si se pasa, da la vuelta."""
    dur = DUR.get(_id(url))
    if not dur:
        return float(desde)
    tope = max(1.0, dur - 12)
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
    for k, lst in SRC.items():
        for url, d in lst:
            dur = DUR.get(_id(url))
            if dur is None:
                sin.add(_id(url))
            elif d > dur - 12:
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
