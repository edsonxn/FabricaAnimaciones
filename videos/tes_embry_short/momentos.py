# -*- coding: utf-8 -*-
"""Los momentos del short, en orden. Cada uno es una lista de TROZOS (cortes en seco entre trozos) que se ubican por
frase en la transcripción palabra por palabra de YouTube (segmentos/clips/<clave>.yt.json):
    (desde_aprox, "primeras palabras", "últimas palabras")
y los datos de edición:
    quien   nombre del que dice el remate (placa estilo Skyrim)
    yo      pregunta/setup en burbuja corta («YO: …»), solo contexto; nada de subtítulo completo
    remate  texto de énfasis que revienta en pantalla en el remate (palabras clave, no la frase entera)
    golpe   palabra del remate donde entra el zoom a la cara + SFX
    bips    palabras a censurar con bip (groserías fuertes)
    meme    adorno: "skull" | "boom" | "risas" | "bruh" | "ding" | "scratch" | "congela"
    ego     cuánto baja la barra de EGO de Edson (estilo barra de vida de Skyrim)
Uso: python momentos.py  → imprime tiempos resueltos y la duración total; momentos.json
"""
import json, os, re, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "segmentos", "clips")

M = [
    dict(c="computadora", trozos=[(21.0, "oye", "cual computadora gey")], quien="EMBRY",
         yo="(configurando el mod a media partida…)", remate="¿QUÉ HACES CON ESA COMPUTADORA?", golpe="computadora",
         bips=[], meme="scratch", ego=4),
    dict(c="hijas", trozos=[(26.0, "oye lem", "tus hijas"), (34.5, "buena suerte", "desastre y problema")], quien="LEMKIL",
         yo="¿Cómo se llaman tus hijas?", remate="DESASTRE Y PROBLEMA", golpe="desastre", bips=[], meme="boom", ego=6),
    dict(c="parientes", trozos=[(16.0, "le aseguro", "oro o parientes")], quien="EL «INSPECTOR»",
         yo="(cobrando un impuesto inventado)", remate="EN ORO… O PARIENTES", golpe="parientes", bips=[], meme="ding", ego=0),
    dict(c="orca", trozos=[(18.0, "es una orca", "que la chingada"), (28.5, "soy orco", "así es la vida")], quien="LA ORCA",
         yo="", remate="SI SOY FEA, NI MODO", golpe="fea", bips=["chingada"], meme="bruh", ego=6),
    dict(c="pan", trozos=[(25.0, "aquí tienes", "tu propia existencia")], quien="MAVEN BLACK-BRIAR",
         yo="Dale algo de comer a Snilf", remate="UNA CORTEZA DE PAN", golpe="existencia", bips=[], meme="skull", ego=5),
    dict(c="alcohol", trozos=[(12.5, "vamos a ir a conseguirte", "pareja"), (19.5, "una pareja", "y mis problemas")],
         quien="EMBRY", yo="", remate="YA TENGO EL ALCOHOL", golpe="alcohol", bips=[], meme="ding", ego=4),
    dict(c="potencial", trozos=[(27.0, "chinguen", "el potencial que")], quien="EMBRY",
         yo="(nadie quiere salir con Embry)", remate="EL POTENCIAL QUE TENGO", golpe="potencial",
         bips=["chinguen", "madre"], meme="boom", ego=0),
    dict(c="sombrero", trozos=[(25.5, "cabrones", "loco con sombrero")], quien="HULDA",
         yo="(inspección «sanitaria» en la Yegua Abanderada)", remate="UN BORRACHO, UN CRÍO Y UN LOCO",
         golpe="sombrero", bips=[], meme="skull", ego=7),
    dict(c="yelmo", trozos=[(10.5, "a desinfectar", "quedar calvo"), (25.0, "y que encima", "en la cabeza")],
         quien="GUARDIA", yo="", remate="¿MEADO EN LA CABEZA?", golpe="meado", bips=[], meme="risas", ego=0),
    dict(c="dorthe", trozos=[(28.0, "padre tu necesidad", "evolutivo lamentable")], quien="DORTHE (8 AÑOS)",
         yo="(a su papá, Alvor)", remate="UN LASTRE EVOLUTIVO", golpe="lastre", bips=[], meme="boom", ego=0),
    dict(c="dormir", trozos=[(19.0, "venimos a dormir", "madrugar"), (27.0, "dormir en", "de tomar")], quien="EMBRY",
         yo="", remate="¿DORMIR EN LUGAR DE TOMAR?", golpe="tomar", bips=[], meme="bruh", ego=3),
    dict(c="roniosos", trozos=[(34.5, "de veras", "pinches roñosos")], quien="MENDIGO",
         yo="Toma todo el pan que quieras", remate="NO TODOS SON ROÑOSOS", golpe="roñosos", bips=["pinches"],
         meme="ding", ego=0),
    dict(c="diego", trozos=[(32.0, "y pues te mando", "decirle algo"), (40.5, "le voy a decir", "no brilla el sol")],
         quien="FRODNAR (NIÑO)", yo="", remate="POR DONDE NO BRILLA EL SOL", golpe="sol", bips=[], meme="skull", ego=5),
    dict(c="trio", trozos=[(28.0, "bueno aquí estamos", "de la desgracia")], quien="FRODNAR",
         yo="", remate="EL TRÍO DINÁMICO DE LA DESGRACIA", golpe="desgracia", bips=[], meme="risas", ego=8),
    dict(c="fracaso", trozos=[(44.0, "este desgraciado", "y a fracaso")], quien="ELFA OSCURA",
         yo="(Embry «revisa» sus plantas)", remate="APESTA A FRACASO", golpe="fracaso", bips=[], meme="skull", ego=8),
    dict(c="autografo", trozos=[(34.5, "le vas a pedir", "qué ridículo")], quien="MIS COMPAÑEROS",
         yo="(interrogo a un bandido)", remate="¿LE PEDIRÁS UN AUTÓGRAFO?", golpe="autógrafo", bips=[], meme="bruh", ego=10),
    dict(c="caldo", trozos=[(28.0, "calma niño", "caldo con él")], quien="EMBRY", yo="(el perro de Frodnar murió)",
         remate="UN BUEN CALDO", golpe="caldo", bips=[], meme="congela", ego=0),
    dict(c="tiktok", trozos=[(39.5, "qué más tienes", "de la batalla o qué"), (46.0, "qué es tiktok", "existe esa madre")],
         quien="TULIO", yo="¡Matamos al dragón de Carrera Blanca!", remate="¿UN VIDEO DE TIKTOK?", golpe="tiktok", golpe_i=0,
         bips=["madre"], meme="scratch", ego=24),
]


# fuera por duración (111 s → ~90 s): los más flojos o casi todo bip
FUERA = {"potencial", "roniosos", "computadora", "parientes", "caldo"}   # los 3 últimos: no se ve la cara de quien habla
M = [m for m in M if m["c"] not in FUERA]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9ñ ]", "", s.replace("ñ", "n")).strip()


def palabras(c):
    ws = json.load(open(os.path.join(D, c + ".yt.json"), encoding="utf-8"))
    out = []
    for t, w in ws:
        for p in w.replace("[ __ ]", " __ ").split():
            n = "bip" if p == "__" else norm(p)
            if n:
                out.append((t, n, "[bip]" if n == "bip" else p))
    return out


def buscar(ws, frase, desde):
    """Busca la frase saltándose los [ __ ] (bip); devuelve índices en la lista completa."""
    fr = norm(frase).split()
    idx = [i for i, w in enumerate(ws) if w[1] != "bip"]
    for k in range(len(idx) - len(fr) + 1):
        if ws[idx[k]][0] < desde - 0.5:
            continue
        if [ws[idx[k + j]][1] for j in range(len(fr))] == fr:
            return idx[k], idx[k + len(fr) - 1]
    raise SystemExit("no encontré «%s» desde %.1f" % (frase, desde))


def resolver():
    res = []
    for m in M:
        ws = palabras(m["c"])
        tz, palabras_m = [], []
        for desde, ini, fin in m["trozos"]:
            i0, _ = buscar(ws, ini, desde)
            _, i1 = buscar(ws, fin, ws[i0][0])
            a = ws[i0][0] - 0.12
            b = ws[i1 + 1][0] + 0.05 if i1 + 1 < len(ws) else ws[i1][0] + 0.6
            b = min(b, ws[i1][0] + 0.9)
            tz.append([round(a, 2), round(b, 2)])
            palabras_m += [(round(t, 2), p) for t, _, p in ws[i0:i1 + 1]]
        g = [t for t, p in palabras_m if norm(p) == norm(m["golpe"])]
        bips = [t for t, p in palabras_m if p == "[bip]" or norm(p) in {norm(b) for b in m["bips"]}]
        r = dict(m, trozos=tz, palabras=palabras_m, t_golpe=g[m.get("golpe_i", -1)] if g else tz[-1][1] - 1.0, t_bips=bips,
                 dur=round(sum(b - a for a, b in tz), 2))
        res.append(r)
    return res


if __name__ == "__main__":
    R = resolver()
    tot = 0
    for r in R:
        tot += r["dur"]
        print("%-12s %5.2f s  trozos=%s  golpe=%.2f  bips=%s" % (r["c"], r["dur"], r["trozos"], r["t_golpe"], r["t_bips"]))
        print("             " + " ".join(p for _, p in r["palabras"]))
    print("TOTAL clips %.1f s (%d momentos)" % (tot, len(R)))
    json.dump(R, open(os.path.join(AQUI, "momentos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
