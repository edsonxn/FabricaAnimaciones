# -*- coding: utf-8 -*-
"""Escribe busquedas.json: cada beat toma la fuente de SU escena ({"url","desde"}), en el ORDEN de sus beats (una entrada por beat,
pensada contra la frase de ese beat: lo que la voz nombra se ve). Copiado de wow_ruta_forever/_busquedas.py (22-nov-2026).
Candidatos: `_buscar_fuentes.py` → `_candidatos.txt` (yt-dlp ytsearch). Un cuadro de cada fuente nueva se miró antes en hojas
(1,5 s con --download-sections, sin bajar el video): fuera webcams (funkusz, Ahmpy, StorisForever, Kaghoegaming, Venruki, Payo,
Ksuper, Gillee, Xaryu, Davy JoneS), logos fijos (Railgan, Honeythief, LVLADEN, «Eternal», PitchNight, Gaap, Aspira), títulos
de guía encima (Nalowale, The Innkeeper, FUBAR, MySpaceGuide), mapas renderizados (ZWCOL) y diapositivas.
Fuentes principales, sin narrar: Grand Marshal Esshow («WoW Forever | <mazmorra> | Undead Paladin PoV»: Cumbre de Roca Negra
superior/inferior, Stratholme, Scholomance, La Masacre, Profundidades, Bastión Faucenegra, Bancal del Creador), Onyxia de Classic
(Hindenburg «Onyxia - No Commentary», Esshow TBC Anniversary nivel 60, Ripper Case 40 jugadores, Akadin 2019), JcJ de Forever
(Garganta Grito de Guerra, Cuenca de Arathi, campo nuevo de Zerocks) y Valle de Alterac de Classic, ambientes de Forever sin
interfaz (Wanderer's Hearth y NFGames en Hyjal, NFGames Cuna, Azeroth Ambience Ventormenta, Ambient AFK Orgrimmar/Forjaz,
Darnassus, NoloFaija Cima del Trueno), Meisio (Marjal, Azshara y Un'Goro de Classic), fwengli (Un'Goro, Frondavil, Cuna, Estepas)
y los longplays de Loopy Longplays / Checkpoint Storytime / Chernobyl Brotherhood para Overgear y las burlas.
`python _busquedas.py --check` = solo comprueba SRC (escenas cubiertas, nº de entradas = nº de beats, ids sin duración, offsets
fuera, tramos repetidos)."""
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


# Atajos de fuentes (id de YouTube). Esshow = WoW Forever, Undead Paladin PoV, sin narrar.
UBRS1, UBRS2 = "uLI9jgwjEpQ", "L0ogZWvleQE"                      # Cumbre de Roca Negra superior
LBRS, LBRSQ1, LBRSQ2 = "ckhwomooniY", "pyWxkRiNu8c", "CBZjbDj9xZE"  # Cumbre inferior
STRL, STRL2 = "aXx72ExidLE", "GmaLGLm8pJ8"                        # Stratholme lado vivo
STRU, STRU2, STRU3 = "i3gnRDz9mgw", "atT-5Io9LUo", "MSTuFhqp2go"  # Stratholme lado no-muerto
SCH, SCH2, SCH3 = "rsAN0MpTZcw", "kifKvOCaaj4", "WijSUV4Gtvo"     # Scholomance
DMW, DMN, DME = "OWG6_-QoGv0", "Or3wITeDgzQ", "1BpBQ_KMmcI"       # La Masacre
BRD1, BRD2, BRDL = "xlkl375-ic4", "rX3LNFZF74A", "vTFGIZXjts4"    # Profundidades de Roca Negra
BMH, BMH2, BMHE = "Tf5G9vUiVFI", "FIUHDfx1lmY", "9ocjLryl4II"     # Bastión Faucenegra (Esshow, Pootooroo, entrada)
SHT, SHT2 = "jbPm5SLQm9U", "JVEwH22Ra3A"                          # Bancal del Creador (Esshow, Pootooroo)
ONY1, ONY2, ONY3, ONY4 = "cULw3cMPvPs", "lKAXq32pd6Q", "pwWw_0IL-l8", "5bSGHYQTbQQ"   # Guarida de Onyxia (Classic)
ONYE, ONYA = "xFGcTAOoAcM", "TIuUjzYIdOM"                         # entrada (Forever) · cadena de sintonización (Classic)
HYJ, HYJ2, HYJ3, HYJ4, HYJ5 = "bUUN-RVAgZM", "cQrWYBvskro", "QVin8qs0h4A", "eK06h9XuCvI", "55HBXBVUhn0"   # Monte Hyjal
#   HYJ3 capítulos: 184 Tainted Foothills, 1423 Summit of Eternity, 1522 Hyjal Summit Raid Entrance
WS1, WS2, WS3 = "63Kdh9JTEoQ", "SMxWSKuB5_U", "RBleypaLOPo"       # Cuna del Invierno (Forever)
AZ1, AZ2 = "2YUFXSPh5Lw", "e0TSZHUcnsg"                           # Azshara (Forever 190 s · Meisio)
UG1, UG2 = "IO8iKuChHoc", "mlzkgjTETX4"                           # Un'Goro (Meisio · fwengli)
WSG1, WSG2, WSG3 = "bHAnJiRcTwg", "-zzEi33QWJ0", "nPkLk2PdcxE"    # Garganta Grito de Guerra (Forever)
AB, AV, NBG = "qj8EbB7C434", "wzDlD-h92Pk", "O2Pi1Are23w"         # Arathi (Forever) · Alterac (vanilla) · campo nuevo (Forever)
AH1, AH2 = "YIhM35KjtyA", "7GwYJB_SaPc"                           # casa de subastas (Forever)
RID, ENC = "HmsBzSMGlKM", "s5isRnNljQw"                           # entrenador de equitación · ventana de encantamiento
ORG, ORGL, SW, IF = "kZ79hHwLD7Q", "dlGeYLM0RI8", "M50FQ2tRfnc", "xbcv04EgQFk"   # Orgrimmar, Loopy (brujo), Ventormenta, Forjaz
TB, DAR, DW = "BMPzO8CNuf8", "vdpNu_Y1LqI", "_hW5xQMD0gY"         # Cima del Trueno, Darnassus, Marjal Revolcafango (Meisio)
BS1, BS2, TAN, FEL = "CtXjiVLxo6w", "zf7qveNtYy0", "_ciyszkqp8U", "ntdRpGZAgkY"   # Estepas, Tanaris, Frondavil
DRAK, EMB1, EMB2, BARON, STRC = "fyACirXi3gg", "kuTKldEedkQ", "6sk8tKH7Epw", "RcoHZFQPWwM", "9lVLX0SsXjI"   # Classic
PAL, LOOP2, CHK, CHB, RIV = "8aBwVTAnZLI", "sdAXLJUlags", "UMh80-64QLc", "u5bh7icrDCc", "N1oab1U4vcE"   # longplays Forever

SRC = {
    # 14 días para las bandas · 196 millones de muertes · reinicio semanal · trampas nuevas · más gente · 3.ª parte · 25 errores
    "intro": L((UBRS2, 600), (STRU, 900), (ONY4, 1500), (BMH, 600), (SW, 2000), (ORGL, 9000), (LBRS, 1200)),
    # (repetir mazmorras) anillo · dos anillos · Sortija · vendedor Pix Xizzix · estadísticas · sanador · arreglo
    "c25": L((SCH, 1500), (STRL, 600), (STRL2, 900), (SW, 6000), (SCH2, 1000), (SCH3, 1800), (ORG, 2500)),
    # tareas del Campo de honor · ruta de JcJ, duelos · 3 batallas en la Garganta · matar 25 · Legado · duelos en la capital
    "c24": L((WSG1, 300), (WSG1, 700), (WSG1, 1000), (WSG2, 1800), (WSG3, 2400), (ORGL, 36950)),
    # Overgear: gameplay de fondo (subir, combate, banda); resistencia al fuego para Onyxia en 026
    "overgear": L((PAL, 20000), (CHK, 3000), (CHB, 4000), (ORGL, 20000), (PAL, 30000), (ONY4, 2000), (UBRS1, 1200), (LBRS, 2200)),
    # Guarida (entrada) · 40, un jefe, vuela · coletazo · nidos/crías · bola de fuego, aliento · miedo, huevos · posiciones
    "c23": L((ONYE, 5), (ONY3, 60), (ONY1, 550), (ONY1, 700), (ONY2, 700), (ONY4, 3000), (ONY3, 120)),
    # honor: conjuntos JcJ · épico con lacre · rangos · error de venderla · guardarlas en el banco
    "c22": L((AV, 1500), (AV, 2500), (WSG2, 2600), (AB, 500), (SW, 9000)),
    # burla de Alejandro: gameplay de fondo
    "burla0": L((ORGL, 30000), (PAL, 12000), (CHK, 5000), (CHB, 10000)),
    # rango para siempre · vuelve al 1 · tope semanal · datos · Alterac 58 + Islas Lanza Negra · 15c15 frente al Marjal · equipo
    "c21": L((WSG1, 500), (AV, 3500), (WSG3, 1000), (AB, 1000), (AV, 600), (NBG, 200), (NBG, 900)),
    # consumibles/economía · todo sube · pociones, elixir, comida · comida con experiencia · fabrícalo tú
    "c20": L((AH1, 200), (AH2, 300), (AH1, 330), (ORG, 3000), (AH2, 500)),
    # sin oro para reparar · a ciegas, morir · 200 millones de muertes · armadura en rojo, reparto · apartar dinero
    "c19": L((BRD1, 1500), (BRDL, 600), (STRU2, 1200), (UBRS2, 1800), (SW, 4500)),
    # gracias: espectador nuevo · Torrikus · Arathi como Vietnam · cola de la Cumbre superior (+ Número 18)
    "gracias1": L((PAL, 5000), (ORGL, 15000), (AB, 800), (UBRS1, 300)),
    # Cima Hyjal de TBC (entrada) · 20 y 13 jefes, Nordrassil · guardián y tres caminos · nombres · arma inútil · tres noches
    "c18": L((HYJ3, 1530), (HYJ, 1800), (HYJ2, 1200), (HYJ, 2600), (HYJ4, 900), (HYJ5, 300)),
    # Cavernas del Túmulo bajo Kalimdor · tres entradas · norte de Azshara · medio grupo en Cuna · Well of Sorrow · piedra de hogar
    "c17": L((BMH, 1800), (WS1, 1500), (AZ1, 60), (WS2, 1500), (BMH, 2100), (WS3, 2200)),
    # Bastión sin misiones (entrada) · ciudad furbolg · 7 misiones · Cima del Trueno/Darnassus · un solo camino · túneles
    "c16": L((BMHE, 10), (BMH, 300), (BMH, 900), (TB, 1500), (BMH, 1500), (BMH2, 1500)),
    # (dos caminos) + burla de Jclothus: gameplay de fondo
    "burla1": L((BMH, 2200), (CHB, 14000), (PAL, 25000), (CHK, 6000), (ORGL, 25000)),
    # Bancal sin cristales · Un'Goro, Refugio · cristales, Cinder/Bolt · Snowtalon/Vitrix · Nanaya · consola con bichos · Un'Goro
    "c15": L((SHT, 200), (UG1, 600), (SHT, 900), (SHT, 1500), (SHT, 2500), (SHT2, 700), (UG2, 1500)),
    # equitación · mil de oro + montura · honorable · monturas raciales · cielonatos · 1391 de oro · juntar desde el 55
    "c14": L((RID, 40), (SW, 3000), (ORG, 1800), (DAR, 1800), (TB, 2500), (AH1, 100), (PAL, 33000)),
    # listas de botín · objetos ocultos · lista de la Cima Hyjal · primer conjunto · caja sorpresa · reparto
    "c13": L((ONY4, 4000), (LBRSQ1, 1500), (HYJ2, 2600), (ONY1, 400), (UBRS1, 1700), (STRL, 2400)),
    # fallo del Bastión · enemigos normales con botín de élite · economía bloqueada · vendedor, suspendidos · 10× oro · montura
    "c12": L((BMH, 1000), (BMH, 1300), (AH1, 250), (ORG, 700), (BMH, 1700), (SW, 7500)),
    # correcciones: Auctionator/TSM · brujo bajo el agua · JcJ sin durabilidad · bicho o guardia · Lacre de Ascensión
    "correc": L((AH1, 300), (AZ2, 2500), (WSG1, 900), (WSG3, 2800), (LBRS, 2000)),
    # Cumbre superior con cinco · única de diez · enemigos con menos vida · guías viejas · pilar rebelde · grupo de diez + lacre
    "c11": L((UBRS1, 200), (UBRS2, 900), (UBRS1, 800), (UBRS2, 1500), (UBRS1, 1400), (UBRS2, 2100)),
    # sintonización de Onyxia · ya te lo conté · amuleto en el banco · en la bolsa sí · cada alt · llévalo puesto · Número nueve
    "c10": L((ONYA, 1300), (ONYA, 2000), (IF, 1000), (ONYE, 30), (DW, 1200), (ONY3, 20), (ONY1, 150)),
    # resistencia al fuego · Amuleto 15 · Lacre 10 y conjunto 8 · Poción de protección · absorbe + Capa · escama · arreglo
    "c09": L((ONY2, 600), (ONY1, 300), (UBRS2, 300), (AH2, 200), (ONY4, 3500), (ONY3, 150), (ONY2, 850)),
    # gracias: Teniente con comida · Zargues sacerdote · vida del tanque · suscríbete, bandas
    "gracias2": L((ORG, 2200), (SCH2, 2000), (SCH, 2500), (HYJ2, 3000)),
    # banda que no llenas, Cavernas 10/8 · Hyjal 20/13, Onyxia 40 · sin tamaño flexible · grupo pequeño · Karazhan · alianzas
    "c08": L((BMH, 2300), (ONY3, 90), (STRL2, 1600), (SCH3, 3000), (UBRS1, 1000), (ONY4, 2500)),
    # profesiones < 300 (Gran Forja) · recetas del conjunto · planos de jefes · profesión en 240 · receta (encantador) · al 300
    "c07": L((IF, 2000), (IF, 3000), (DMW, 1500), (SW, 8000), (ENC, 300), (DME, 900)),
    # Guardianes de Hyjal · facción nueva · una pieza / Vaina · intendente en la Cima de la Eternidad · 21 000 · semilla · Tiala
    "c06": L((HYJ, 1200), (HYJ3, 300), (HYJ4, 600), (HYJ3, 1430), (HYJ2, 2000), (HYJ, 2200), (HYJ5, 700)),
    # burla de Rafael: ChatGPT · cristales del Bancal · puerta de Onyxia sin amuleto · top cinco
    "burla2": L((CHB, 16000), (SHT, 2000), (DW, 2000), (ORGL, 32000)),
    # tope de 5 por hora (Stratholme, Scholomance) · Roca Negra, Bancal · reiniciar · demasiadas estancias · alt de 45 · puntualidad
    "c05": L((STRU, 1500), (BRD1, 2500), (SCH, 600), (STRL, 1000), (STRU3, 800), (SCH3, 1200), (STRL2, 2000)),
    # Cumbre superior, Drakkisath · Rend, Valthalak · lacre sin adornar · 4 % · Brasaliza en el Marjal · resistencias · Vaelan
    "c04": L((DRAK, 60), (UBRS2, 2300), (LBRS, 800), (LBRSQ1, 2500), (EMB1, 200), (EMB2, 200), (LBRSQ2, 800)),
    # botín de banda al vendedor · Esencia maleable (desencantar) · Onyxia no cuenta · al vendedor · encantador
    "c03": L((ONY1, 750), (ENC, 400), (ONY2, 400), (AH2, 600), (ENC, 200)),
    # Número dos (capital) · Rend, Serenata (Frondavil), Masacre, Feria · brillando, no funcionan · cabeza en la ciudad ·
    # se apaga en la guarida · heraldos en Villadorada… · beneficio de Rend al subir · beneficios para alts (La Masacre)
    "c02": L((ORG, 900), (FEL, 1000), (ONY1, 500), (SW, 1500), (ONY2, 750), (LOOP2, 3600), (LOOP2, 24300), (DME, 1200)),
    # Número uno, conjunto de mazmorra · Scholo/Strat/Roca Negra · Gandling/Barón/Drakkisath · desencantar, 0.5 · entregas ·
    # casco y peto, Gandling otra vez · Tanaris… · 227 de oro, Alba Argenta · Ejecutor Asharell (Estepas) · versión por
    # especialización · Valthalak · punto de Legado
    "c01": L((SCH, 2000), (STRU2, 500), (BARON, 20), (STRL, 2700), (DMN, 1200), (SCH2, 2600), (TAN, 2300), (STRU3, 1600),
             (BS1, 2500), (BS2, 600), (UBRS1, 1800), (BRD2, 1500)),
    # 25 errores · dos semanas, puerta de la banda · comentarios · 39 amigos · próxima crónica
    "cierre": L((ONY1, 600), (HYJ3, 1580), (PAL, 36000), (ONY3, 40), (HYJ, 3300)),
}
RELLENO = L((PAL, 9000), (ORGL, 12000))


# FIJADO A MANO por beat (revisión de las hojas de `medios`): gana sobre SRC al regenerar. Vacío hasta la primera revisión.
FIJO = {   # rondas 1-2 (22-nov-2026, hojas medios_NN + _ultimos_NN): motivo en _rehacer.txt
    "scene-088": ("kZ79hHwLD7Q", 1200),   # ronda 3 (revisión visual 22-nov): rectángulos verdes de textura rota en Orgrimmar
    "scene-015": ("-lVDQz7oep0", 3000), "scene-016": ("eeHLcCzJ8O0", 60), "scene-017": ("eeHLcCzJ8O0", 530),
    "scene-018": ("eeHLcCzJ8O0", 380), "scene-019": ("eeHLcCzJ8O0", 260), "scene-029": ("cULw3cMPvPs", 30),
    "scene-038": ("-lVDQz7oep0", 4000), "scene-039": ("wzDlD-h92Pk", 1000), "scene-045": ("-lVDQz7oep0", 6000),
    "scene-047": ("-lVDQz7oep0", 9500), "scene-048": ("wzDlD-h92Pk", 4200), "scene-053": ("YIhM35KjtyA", 120),
    "scene-056": ("s5isRnNljQw", 100), "scene-064": ("jOJC-qG3v9g", 1500), "scene-101": ("M50FQ2tRfnc", 11000),
    "scene-102": ("M50FQ2tRfnc", 12000), "scene-103": ("cULw3cMPvPs", 100), "scene-107": ("L0ogZWvleQE", 1200),
    "scene-111": ("kZ79hHwLD7Q", 1500), "scene-117": ("-lVDQz7oep0", 2200), "scene-118": ("wzDlD-h92Pk", 3000),
    "scene-123": ("L0ogZWvleQE", 1560), "scene-136": ("vTFGIZXjts4", 1000), "scene-137": ("cULw3cMPvPs", 250),
    "scene-144": ("FIUHDfx1lmY", 2700), "scene-158": ("55HBXBVUhn0", 500), "scene-159": ("QVin8qs0h4A", 1440),
    "scene-166": ("8aBwVTAnZLI", 15000), "scene-178": ("I4rGe_s8Xqw", 150), "scene-179": ("I4rGe_s8Xqw", 60),
    "scene-184": ("YIhM35KjtyA", 50), "scene-185": ("s5isRnNljQw", 480), "scene-200": ("Ngpi1TkXOJA", 600),
    "scene-207": ("cQrWYBvskro", 500), "scene-208": ("UMh80-64QLc", 1500),
    "scene-167": ("i3gnRDz9mgw", 1550), "scene-180": ("CBZjbDj9xZE", 780), "scene-205": ("rX3LNFZF74A", 1480),
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


def asignar(b):
    out, cuenta, prev = [], {}, "intro"
    for x in b:
        eid = escena_de(x.get("texto", "")) or prev
        prev = eid
        n = cuenta.get(eid, 0)
        cuenta[eid] = n + 1
        out.append((x, eid, n))
    return out, cuenta


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
    if os.path.exists("beats.json"):
        _, cuenta = asignar(json.load(open("beats.json", encoding="utf-8")))
        dif = {k: (v, len(SRC.get(k, []))) for k, v in cuenta.items() if v != len(SRC.get(k, []))}
        print("beats ≠ entradas (beats, entradas):", dif or "-")
        usados, rep = [], []
        for k, lst in SRC.items():
            for url, d in lst:
                for k2, u2, d2 in usados:
                    if u2 == url and abs(d2 - d) < 15:
                        rep.append(f"{k2}/{k}:{_id(url)}@{d}")
                usados.append((k, url, d))
        print("tramos repetidos (< 15 s):", rep or "-")
    return not faltan


if __name__ == "__main__":
    if "--check" in sys.argv or not os.path.exists("beats.json"):
        if not os.path.exists("beats.json"):
            print("(aún no hay beats.json: solo compruebo SRC)")
        sys.exit(0 if comprobar() else 1)
    b = json.load(open("beats.json", encoding="utf-8"))
    out = {}
    lista, cuenta = asignar(b)
    for x, eid, n in lista:
        lst = SRC.get(eid) or RELLENO
        url, desde = lst[n % len(lst)]
        out[x["id"]] = {"url": url, "desde": desde_seguro(url, desde + 25 * (n // len(lst)))}
    for k, (i, d) in FIJO.items():
        if k in out:
            out[k] = {"url": Y(i), "desde": float(d)}
    json.dump(out, open("busquedas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({x["id"]: e for x, e, _ in lista}, open("_beat_escena.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(out), "beats ·", ", ".join(f"{k}:{v}" for k, v in cuenta.items()))
