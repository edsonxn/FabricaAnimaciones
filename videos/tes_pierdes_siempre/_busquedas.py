# -*- coding: utf-8 -*-
"""Escribe busquedas.json de «Las 15 cosas de Skyrim que PIERDES para siempre» (26-nov-2026): una lista de búsquedas por FRASE
del guion (en inglés, 2-5 palabras, con lo que la voz describe en ese segundo: regla «lo que dice la voz SE VE») + respaldo
genérico. Búsquedas de investigacion.md § «Búsquedas YouTube (vanilla)». Los beats se casan por TEXTO con la frase original."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guion  # noqa: E402

G = "Skyrim gameplay no commentary"


def q(*s):
    return list(s) + [G]


L = [
 # intro
 q('Skyrim Nahkriin staff skuldafn portal seal'),
 q('Skyrim Fort Dawnguard armored troll', 'Skyrim Dawnguard Isran fort'),
 q('Skyrim storm call shout full power'),
 q('Skyrim landscape 4k no HUD'),
 q('Skyrim Skuldafn temple Odahviing flight'),
 # p15
 q('Skyrim Goldenglow Estate'),
 q('Skyrim Loud and Clear Brynjolf quest'),
 q('Skyrim Maven Black-Briar Riften'),
 q('Skyrim loud and clear goldenglow burn hives'),
 q('Skyrim goldenglow burn too many hives no reward'),
 q('Skyrim fire breath shout burning'),
 q('Skyrim Maven Black-Briar quest reward gold'),
 q('Skyrim Goldenglow burn only three hives', 'Skyrim Goldenglow beehive fire'),
 q('Skyrim Goldenglow fire hives burning'),
 # cr1
 q('Skyrim bard tavern no HUD'),
 q('Skyrim Goldenglow island burning'),
 # p14
 q('Skyrim Thalmor Embassy'),
 q('Skyrim Diplomatic Immunity party Elenwen'),
 q('Skyrim Thalmor Embassy courtyard barracks'),
 q('Skyrim Thalmor Embassy loot'),
 q('Skyrim Thalmor Embassy return glitch horse', 'Skyrim get back into Thalmor Embassy'),
 q("Skyrim Elenwen's Solar"),
 q('Skyrim Malborn Diplomatic Immunity'),
 q('Skyrim Malborn Windhelm Cornerclub'),
 # p13
 q('Skyrim Sven Faendal letter Camilla'),
 q('Skyrim Riverwood Camilla Valerius'),
 q('Skyrim Faendal letter quest Riverwood'),
 q('Skyrim Faendal follower'),
 q('Skyrim Faendal archery trainer', 'Skyrim Faendal bow'),
 q('Skyrim Faendal Sven letter choice', 'Skyrim Camilla Valerius letter'),
 q('Skyrim Sven bard Riverwood'),
 # p12
 q('Skyrim Thirsk Mead Hall Dragonborn'),
 q('Skyrim Thirsk rieklings Hall of Glory'),
 q('Skyrim Thirsk Mead Hall Nords quest'),
 q('Skyrim riekling follower Thirsk'),
 q('Skyrim Thirsk riekling chief quest', 'Skyrim Thirsk Mead Hall rieklings'),
 q('Skyrim riekling Solstheim'),
 # ag1
 q('Skyrim landscape relaxing no HUD'),
 q('Skyrim Whiterun no HUD'),
 q('Skyrim Riverwood night no HUD'),
 q('Skyrim aurora no HUD'),
 # p11
 q('Skyrim Season Unending High Hrothgar'),
 q('Skyrim Season Unending negotiation table Ulfric Tullius'),
 q('Skyrim Season Unending give the Reach'),
 q('Skyrim battle for Fort Sungard', 'Skyrim battle for Fort Greenwall'),
 q('Skyrim Ondolemar Markarth'),
 q('Skyrim Call Dragon shout Odahviing'),
 q('Skyrim Fort Greenwall battle', 'Skyrim Fort Sungard battle'),
 q('Skyrim High Hrothgar'),
 # p10
 q('Skyrim Hall of the Vigilant'),
 q('Skyrim Keeper Carcette Vigilant of Stendarr'),
 q('Skyrim Hall of the Vigilant destroyed'),
 q('Skyrim Hall of the Vigilant ruins vampires'),
 q('Skyrim Hall of the Vigilant interior chests', 'Skyrim Keeper Carcette'),
 q('Skyrim Hall of the Vigilant exterior', 'Skyrim Hall of the Vigilant intact'),
 q('Skyrim Dawnstar road The Pale'),
 q('Skyrim Keeper Carcette training restoration'),
 q('Skyrim Vigilant of Stendarr'),
 # p9
 q('Skyrim civil war jarl exiled'),
 q('Skyrim civil war map holds'),
 q('Skyrim Jarl Igmund Markarth', 'Skyrim Jarl Korir Winterhold'),
 q('Skyrim Brunwulf Free-Winter jarl', 'Skyrim Dengeir of Stuhn'),
 q('Skyrim Morthal Idgrod the Younger', 'Skyrim Morthal Gorm'),
 q('Skyrim battle for whiterun imperial severio pelagia', 'Skyrim battle for solitude captain aldis'),
 q('Skyrim jarl bounty quest'),
 q('Skyrim civil war battle'),
 # cr2
 q('Skyrim crying npc'),
 q('Skyrim Dawnguard choice Harkon'),
 # p8
 q('Skyrim stalhrim armor crafting'),
 q('Skyrim stalhrim ore Solstheim'),
 q('Skyrim a new source of stalhrim deor'),
 q('Skyrim Skaal Village Solstheim'),
 q('Skyrim Skaal Village follower axe', 'Skyrim Skaal Village Deor Woodcutter'),
 q('Skyrim Skaal Village Solstheim', 'Skyrim Skaal Village walk'),
 q('Skyrim stalhrim armor showcase'),
 q('Skyrim unrelenting force shout ragdoll'),
 # p7
 q('Skyrim jagged crown korvanjund'),
 q('Skyrim Korvanjund sarcophagus'),
 q('Skyrim Korvanjund word wall', 'Skyrim word wall learn shout'),
 q('Skyrim Jagged Crown showcase'),
 q('Skyrim jagged crown give to tullius', 'Skyrim jagged crown Ulfric'),
 q('Skyrim General Tullius Castle Dour'),
 q('Skyrim Jagged Crown quest'),
 q('Skyrim Hadvar Korvanjund'),
 q('Skyrim Jagged Crown worn'),
 # p6
 q('Skyrim Serana'),
 q('Skyrim serana cured human eyes falion'),
 q("Skyrim serana bloodcursed arrows auriel's bow"),
 q('Skyrim Serana cure Falion vampire', 'Skyrim vampire lord player Serana'),
 q('Skyrim Serana Elder Scroll Fort Dawnguard'),
 q('Skyrim Serana talking cure dialogue'),
 q('Skyrim Serana bloodcursed arrows', 'Skyrim Serana conversation'),
 q('Skyrim Serana Dawnguard ending'),
 # cr3
 q('Skyrim library books no HUD'),
 q('Skyrim Goldenglow hives burning'),
 # p5
 q('Skyrim Guild Master armor'),
 q('Skyrim Erikur Solitude'),
 q('Skyrim the dainty sload erikur'),
 q('Skyrim Delvin Mallory Ragged Flagon'),
 q('Skyrim under new management guild master armor'),
 q('Skyrim Thieves Guild achievement', 'Skyrim Thieves Guild Ragged Flagon'),
 q('Skyrim The Delicate Sload Erikur', 'Skyrim Erikur Solitude'),
 q('Skyrim Erikur'),
 # p4
 q('Skyrim werewolf transformation'),
 q('Skyrim beast form werewolf fight'),
 q('Skyrim aela restore lycanthropy dawnguard'),
 q('Skyrim Purity glenmoril witch head cure'),
 q('Skyrim become Vampire Lord Serana bite', 'Skyrim Serana turns you vampire lord'),
 q('Skyrim totems of hircine howl'),
 q('Skyrim Totems of Hircine quest', 'Skyrim werewolf totem Hircine'),
 q('Skyrim Aela the Huntress'),
 # campana
 q('Skyrim landscape 4k no HUD'),
 q('Skyrim sunrise no HUD'),
 # p3
 q('Skyrim Fort Dawnguard'),
 q('Skyrim dawnguard vs vampire choice harkon'),
 q('Skyrim dwarven crossbow exploding bolts'),
 q('Skyrim Dawnguard trainers Sorine Isran Gunmar Florentius'),
 q('Skyrim armored troll dawnguard'),
 q('Skyrim Dawnguard followers Agmaer Beleval', 'Skyrim Dawnguard recruits Ingjard Durak'),
 q('Skyrim Bloodstone Chalice'),
 q('Skyrim Dawnguard choice Isran Harkon', 'Skyrim Fort Dawnguard'),
 q('Skyrim Destroying the Dawnguard Isran'),
 # p2
 q('Skyrim storm call word wall skuldafn'),
 q('Skyrim storm call shout full power'),
 q('Skyrim storm call shout lightning', 'Skyrim storm call one word'),
 q('Skyrim storm call cooldown', 'Skyrim storm call shout'),
 q('Skyrim Forelhost storm call word wall'),
 q('Skyrim Odahviing fly to Skuldafn'),
 q('Skyrim Skuldafn word wall'),
 q('Skyrim Skuldafn temple explore', 'Skyrim Skuldafn word wall'),
 q('Skyrim storm call hits allies'),
 q('Skyrim Sovngarde'),
 # p1
 q('Skyrim Nahkriin staff'),
 q('Skyrim Nahkriin boss fight Skuldafn'),
 q('Skyrim nahkriin staff skuldafn portal seal'),
 q('Skyrim Skuldafn temple'),
 q('Skyrim keep nahkriin staff skuldafn'),
 q('Skyrim Skuldafn portal open run', 'Skyrim Skuldafn portal Sovngarde'),
 q('Skyrim Skuldafn portal Sovngarde'),
 # gema
 q('Skyrim Skuldafn temple'),
 q('Skyrim Nahkriin mask Konahrik'),
 q('Skyrim Odahviing ride'),
 q('Skyrim Thalmor Embassy', 'Skyrim Aela the Huntress'),
 q('Skyrim landscape 4k no HUD'),
 # cierre
 q('Skyrim Goldenglow Estate', 'Skyrim Nahkriin staff'),
 q('Skyrim tavern no HUD'),
 q('Skyrim sunset no HUD'),
 q('Skyrim bard lute song'),
]

FR = [re.sub(r"\[[^\]]*\]\s*", "", f) for e in guion.ESCENAS for f in e["frases"]]
N = len(FR)
assert len(L) == N, (len(L), N)
B = {i + 1: v for i, v in enumerate(L)}
S = {i + 1: " ".join(f.split()[:5]) for i, f in enumerate(FR)}

# frase que la voz dice DENTRO del beat → búsqueda (manda sobre la casada por inicio)
FORZAR = [
 ("Severo Pelagia", q("Skyrim battle for whiterun imperial severio pelagia")), ("Malborn", B[23]),
 ("Bran y Sceolang", q("Skyrim Dawnguard dogs Bran Sceolang")), ("trols con armadura", B[118]),
 ("Fus Ro Dah", B[76]), ("Ondolemar", B[46]),
]


def toks(t):
    return [w for w in (re.sub(r"[\W_]+", "", x.lower()) for x in t.split()) if w]


def busca(h, a):
    for i in range(len(h) - len(a) + 1):
        if h[i:i + len(a)] == a:
            return i
    return -1


AQUI = os.path.dirname(os.path.abspath(__file__))
beats = json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8"))
beats = beats if isinstance(beats, list) else beats["beats"]
out, ultimo, usados = {}, 0, {}
for b in beats:
    h = toks(b["texto"])
    hall = sorted((p, k) for k in range(ultimo + 1, min(ultimo + 9, N + 1)) for p in [busca(h, toks(S[k]))] if p >= 0)
    # la cola del beat original anterior solo compite si ese beat aún no tiene clip (lo nuevo que dice la voz gana)
    trozos = ([(hall[0][0] if hall else len(h), ultimo)] if ultimo and (ultimo not in usados or not hall) else []) + \
             [((hall[j + 1][0] if j + 1 < len(hall) else len(h)) - p, k) for j, (p, k) in enumerate(hall)]
    orden = sorted(trozos, reverse=True)
    k = next((kk for _, kk in orden if kk not in usados), orden[0][1]) if orden else 1
    if hall:
        ultimo = hall[-1][1]
    qs = list(B[k])
    usados[k] = usados.get(k, 0) + 1
    forz = next((list(fq) for fs, fq in FORZAR if busca(h, toks(fs)) >= 0), None)
    if forz:
        qs = forz
        for kk, v in B.items():
            if v == forz:
                usados[kk] = usados.get(kk, 0)
    elif usados[k] > 1:                       # el mismo beat original en dos beats nuevos: otra búsqueda primero (otro clip)
        qs = (qs[1:-1] + [qs[0] + " 4k"] + qs[-1:]) if len(qs) > 2 else ([qs[0] + " 4k"] + qs[1:])
    out[b["id"]] = qs
    print(b["id"], "<-", k, "|", qs[0], "|", b["texto"][:50])
json.dump(out, open(os.path.join(AQUI, "busquedas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("busquedas.json:", len(out), "beats · búsquedas originales sin usar:", [k for k in B if k not in usados])
