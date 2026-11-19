# -*- coding: utf-8 -*-
"""Escribe busquedas.json de «Las 20 ARMADURAS más poderosas de Skyrim» (s2, 18-nov-2026): 194 beats, búsquedas en inglés de 2-5
palabras con lo que la voz describe en ese segundo (regla «lo que dice la voz SE VE») + respaldo genérico de Skyrim."""
import json
import os
import re

G ="Skyrim gameplay no commentary"


def q(*s):
    return list(s) + [G]


B = {
 # gancho
 1: q("Skyrim Konahrik dragon priest summon", "Skyrim Konahrik mask"), 2: q("Skyrim Boethiah sacrifice follower altar"),
 3: q("Skyrim Deathbrand treasure map chest", "Skyrim Miraak robes tentacles"), 4: q("Skyrim best armor showcase 4k"),
 5: q("Skyrim armor rating inventory"), 6: q("Skyrim iron armor legendary smithing"),
 # 20 Mzund
 7: q("Skyrim Visage of Mzund"), 8: q("Skyrim Visage of Mzund enchantment"), 9: q("Skyrim Breath of Nchuak steam"),
 10: q("Skyrim Breath of Nchuak ragdoll kill"), 11: q("Skyrim Fahlbtharz boiler puzzle"), 12: q("Skyrim Fahlbtharz Visage of Mzund location"),
 13: q("Skyrim dwemer elevator ride"),
 # 19 Clavicus
 14: q("Skyrim Masque of Clavicus Vile"), 15: q("Skyrim A Daedra's Best Friend quest"), 16: q("Skyrim Barbas talking dog Falkreath"),
 17: q("Skyrim Haemar's Shame Clavicus Vile shrine"), 18: q("Skyrim Barbas Clavicus Vile choice Rueful Axe"),
 19: q("Skyrim Clavicus Vile mask Ebony Mail invisible head"), 20: q("Skyrim headless character bug"),
 # 18 Ysgramor
 21: q("Skyrim Shield of Ysgramor"), 22: q("Skyrim Glory of the Dead Eorlund Wuuthrad"), 23: q("Skyrim Ysgramor's Tomb boss chest"),
 24: q("Skyrim Ysgramor's Tomb chest empty"), 25: q("Skyrim Shield of Ysgramor first person block"),
 # correo 1
 26: q("Skyrim courier letter"), 27: q("Skyrim tavern bard no HUD"), 28: q("Skyrim Whiterun night no HUD"),
 29: q("Skyrim landscape relaxing no HUD"),
 # 17 Piel del salvador
 30: q("Skyrim Savior's Hide"), 31: q("Skyrim Savior's Hide armor showcase"), 32: q("Skyrim Ill Met by Moonlight quest"),
 33: q("Skyrim Sinding Falkreath jail", "Skyrim White Stag Hircine"), 34: q("Skyrim Bloated Man's Grotto Sinding"),
 35: q("Skyrim Ring of Hircine"), 36: q("Skyrim Sinding werewolf hunters fight"), 37: q("Skyrim Ill Met by Moonlight both rewards"),
 # 16 Real de vampiro
 38: q("Skyrim Vampire Royal Armor"), 39: q("Skyrim Vampire Royal Armor showcase"), 40: q("Skyrim Castle Volkihar ruins Serana"),
 41: q("Skyrim Volkihar Ruins armoire royal armor"), 42: q("Skyrim Vampire Lord armor Harkon"), 43: q("Skyrim Castle Volkihar court"),
 # 15 Auriel
 44: q("Skyrim Auriel's Shield"), 45: q("Skyrim Auriel's Shield charged glow"), 46: q("Skyrim Auriel's Shield bash Unrelenting Force"),
 47: q("Skyrim Forgotten Vale Ruby Paragon frost giant", "Skyrim Falmer Warmonger"), 48: q("Skyrim Falmer Warmonger Auriel's Shield"),
 49: q("Skyrim brawl bounty"),
 # 14 Ahzidal
 50: q("Skyrim Ahzidal's armor"), 51: q("Skyrim Ahzidal's boots water walking"), 52: q("Skyrim Ahzidal mask"),
 53: q("Skyrim Ahzidal's Genius set bonus"), 54: q("Skyrim Unearthed Kolbjorn Barrow"), 55: q("Skyrim Ralis Sedarys Kolbjorn"),
 56: q("Skyrim Ahzidal boss fight"), 57: q("Skyrim catch fish by hand Dragonborn"),
 # agradecimientos
 58: q("Skyrim Arcanaeum library"), 59: q("Skyrim landscape 4k no HUD"), 60: q("Skyrim Riverwood no HUD"),
 61: q("Skyrim Solitude no HUD"), 62: q("Skyrim Breton Lord Stone"), 63: q("Skyrim dragon priest mask Konahrik"),
 64: q("Skyrim aurora no HUD"), 65: q("Skyrim Guild Master armor"),
 # 13 Maestre del gremio
 66: q("Skyrim Guild Master's Armor showcase"), 67: q("Skyrim Guild Master's Armor enchantments"), 68: q("Skyrim Tonilia Guild Master armor"),
 69: q("Skyrim Ratway Ragged Flagon Riften"), 70: q("Skyrim pickpocket house theft"), 71: q("Skyrim Mercer Frey armor"),
 # 12 Etérea antigua
 72: q("Skyrim Ancient Shrouded Armor"), 73: q("Skyrim Ancient Shrouded Armor showcase"), 74: q("Skyrim Ancient Shrouded Armor enchantments"),
 75: q("Skyrim Olava's Token Gabriella"), 76: q("Skyrim Olava the Feeble Hag's End lever"), 77: q("Skyrim Hag's End secret lever"),
 78: q("Skyrim Hag's End Deepwood Redoubt"),
 # correo 2
 79: q("Skyrim reverse pickpocket poison bounty"), 80: q("Skyrim pickpocket guard caught"), 81: q("Skyrim Thieves Guild Guild Master armor"),
 # 11 Spellbreaker
 82: q("Skyrim Spellbreaker shield"), 83: q("Skyrim Spellbreaker ward block"), 84: q("Skyrim The Only Cure Kesh Peryite shrine"),
 85: q("Skyrim Bthardamz Orchendor"), 86: q("Skyrim Spellbreaker ward concave"), 87: q("Skyrim Spellbreaker dragon breath block"),
 # menciones de honor
 88: q("Skyrim armor display mannequin"), 89: q("Skyrim Jagged Crown"), 90: q("Skyrim Jagged Crown dragon priest mask"),
 91: q("Skyrim Falmer heavy armor Dawnguard"), 92: q("Skyrim Falmer Hardened armor chaurus"),
 # 10 Archimago
 93: q("Skyrim Archmage's Robes"), 94: q("Skyrim Archmage's Robes enchantment"), 95: q("Skyrim Eye of Magnus College of Winterhold"),
 96: q("Skyrim Ancano boss Hall of the Elements"), 97: q("Skyrim Archmage robes with dragon priest mask"),
 98: q("Skyrim Sovngarde heroes"),
 # 9 Ruiseñor
 99: q("Skyrim Nightingale Armor"), 100: q("Skyrim Nightingale Armor showcase"), 101: q("Skyrim Nightingale Armor stats"),
 102: q("Skyrim Trinity Restored Nightingale Hall"), 103: q("Skyrim Karliah Brynjolf Nightingale oath"),
 104: q("Skyrim Nightingale Armor level scaling"), 105: q("Skyrim Nightingale armor level 32"),
 # 8 Konahrik
 106: q("Skyrim Konahrik mask"), 107: q("Skyrim Konahrik mask stats"), 108: q("Skyrim Konahrik low health flames"),
 109: q("Skyrim Konahrik fire cloak heal"), 110: q("Skyrim Konahrik spectral dragon priest"),
 111: q("Skyrim Bromjunaar Sanctuary Wooden Mask"), 112: q("Skyrim Skuldafn Nahkriin"), 113: q("Skyrim dragon priest masks shrine busts"),
 114: q("Skyrim selling dragon priest mask merchant"), 115: q("Skyrim dragon priest masks all eight"),
 116: q("Skyrim Bromjunaar Sanctuary"),
 # 7 Miraak
 117: q("Skyrim Miraak's Robes"), 118: q("Skyrim Miraak's Robes enchantment"), 119: q("Skyrim Miraak's Robes tentacle explosion"),
 120: q("Skyrim Miraak mask"), 121: q("Skyrim Miraak boss fight Summit of Apocrypha"), 122: q("Skyrim Sahrotaar Apocrypha summit"),
 123: q("Skyrim Atronach Stone"), 124: q("Skyrim 100% spell absorption"),
 # 6 Estigma Mortal
 125: q("Skyrim Deathbrand Armor"), 126: q("Skyrim Deathbrand Armor set bonus"), 127: q("Skyrim Deathbrand helm water breathing"),
 128: q("Skyrim Deathbrand treasure map"), 129: q("Skyrim Deathbrand Haknir's Shoal chest"), 130: q("Skyrim Deathbrand chest Tel Mithryn"),
 131: q("Skyrim Gyldenhul Barrow treasure"), 132: q("Skyrim Haknir Death-Brand cutlass"), 133: q("Skyrim Haknir's Shoal ghost"),
 134: q("Skyrim Ebony Mail"),
 # 5 Cota de ébano
 135: q("Skyrim Ebony Mail showcase"), 136: q("Skyrim daedric armor stats"), 137: q("Skyrim Ebony Mail poison cloak"),
 138: q("Skyrim Ebony Mail smoke"), 139: q("Skyrim Boethiah's Calling quest"), 140: q("Skyrim Boethiah Sacellum sacrifice follower Knifepoint"),
 141: q("Skyrim Boethiah cut content quest"), 142: q("Skyrim follower carrying items"),
 # campaña
 143: q("Skyrim Dragonborn shout no HUD"), 144: q("Skyrim mountains no HUD"), 145: q("Skyrim Stalhrim armor"),
 # 4 Stalhrim
 146: q("Skyrim stalhrim deposit"), 147: q("Skyrim Stalhrim heavy armor showcase"), 148: q("Skyrim Stalhrim light armor showcase"),
 149: q("Skyrim A New Source of Stalhrim"), 150: q("Skyrim Deor Woodcutter Skaal Village"), 151: q("Skyrim Deor Woodcutter"),
 152: q("Skyrim Solstheim stalhrim"), 153: q("Skyrim stalhrim mining"),
 # 3 Escamas de dragón
 154: q("Skyrim Dragonscale Armor"), 155: q("Skyrim Dragonscale Armor showcase"), 156: q("Skyrim smithing Dragon Armor perk"),
 157: q("Skyrim Dragonscale armor rating"), 158: q("Skyrim armor cap 567 light armor"), 159: q("Skyrim Shrine of Akatosh dragon scales"),
 160: q("Skyrim Akatosh shrine Rorikstead"), 161: q("Skyrim dragon scales"),
 # 2 Placas de dragón
 162: q("Skyrim Dragonplate Armor"), 163: q("Skyrim Dragonplate Armor showcase"), 164: q("Skyrim tempering dragonplate grindstone"),
 165: q("Skyrim armor rating 567"), 166: q("Skyrim Dragonplate legendary"), 167: q("Skyrim dragon bone Dawnguard"),
 168: q("Skyrim dragon skull helmet"),
 # 1 Daédrica
 169: q("Skyrim Daedric Armor"), 170: q("Skyrim Daedric Armor showcase"), 171: q("Skyrim Dremora daedra heart"),
 172: q("Skyrim daedra heart Jorrvaskr"), 173: q("Skyrim Atronach Forge College of Winterhold"), 174: q("Skyrim Atronach Forge daedric armor"),
 175: q("Skyrim Heavy Armor perk tree"), 176: q("Skyrim daedric armor rating"), 177: q("Skyrim daedric armor full set"),
 178: q("Skyrim Dremora Lord fight"), 179: q("Skyrim daedric boots bug glow"), 180: q("Skyrim daedric armor glitch"),
 # gema
 181: q("Skyrim iron armor"), 182: q("Skyrim armor rating explained"), 183: q("Skyrim armor rating cap"),
 184: q("Skyrim armor 567 cap"), 185: q("Skyrim iron armor legendary"), 186: q("Skyrim giant club smash"),
 187: q("Skyrim armor penetration"), 188: q("Skyrim Conditioning perk heavy armor"), 189: q("Skyrim daedric armor showcase 4k"),
 190: q("Skyrim iron armor showcase"),
 # cierre
 191: q("Skyrim Breath of Nchuak dwemer helmet", "Skyrim daedric armor full set"), 192: q("Skyrim armor collection mannequins"), 193: q("Skyrim bard lute song"),
 194: q("Skyrim sunset no HUD"),
}

# Cómo empezaba cada beat cuando se escribieron las búsquedas (194 beats). `beats` vuelve a cortar los beats cuando cambia la voz:
# cada beat nuevo se casa por TEXTO con el beat original que más texto le ocupa (no por número).
S = {
 1: "Una máscara que cuando", 2: "Una coraza que solo te dan", 3: "Un pirata que enterró", 4: "Hoy las veinte armaduras",
 5: "Con sus cifras dónde", 6: "Y quédate hasta el final", 7: "Número veinte El Semblante", 8: "sesenta de aguante que ya",
 9: "Una ráfaga de vapor", 10: "Y a veces los enemigos que mata", 11: "Está en el Gran Salón", 12: "Tras la reja el casco",
 13: "Los dwemer desaparecieron", 14: "Número diecinueve", 15: "más persuasión y la magia", 16: "desde el nivel diez En",
 17: "Barbas te lleva a", 18: "la máscara o matar al perro", 19: "no una tienda de descuentos", 20: "Precios mejores eso sí",
 21: "Número dieciocho", 22: "Llega al final de los Compañeros", 23: "la Forja del Cielo y la llevas", 24: "Y ojo si entras antes",
 25: "Y en primera persona al bloquear", 26: "Un momento que hay correo", 27: "algunas me dan hasta grima",
 28: "Y Lagartija Vaquera", 29: "Una sola de principio a fin", 30: "Ponte una de estas armaduras", 31: "Una coraza ligera de",
 32: "Quince por ciento de resistencia a la magia y la mitad", 33: "En la cárcel de", 34: "En la Gruta del Hombre",
 35: "Si lo perdonas el Anillo", 36: "Moda sostenible", 37: "termina la misión y recibe el anillo", 38: "Número dieciséis",
 39: "Treinta de armadura nueve de peso", 40: "Está en el Castillo", 41: "sobre un armario junto a", 42: "Si se te pierde vuelves",
 43: "Es para los que mandan", 44: "Número quince", 45: "A los cinco bloqueos", 46: "Y un golpe con escudo potente",
 47: "Le quitas el Modelo de perfección", 48: "Él lleva el escudo", 49: "cuenta como agresión", 50: "Número catorce",
 51: "un cinco por ciento de dejar paralizado", 52: "Los guanteletes absorben", 53: "Con cuatro reliquias puestas",
 54: "Un genio con problemas", 55: "Financias la excavación", 56: "Once mil de oro en total", 57: "Inversión segura",
 58: "Antes del top trece", 59: "zaarondarklord6196", 60: "Reyes3019 que encontró", 61: "Te damos la bienvenida",
 62: "Ahora ya sabes qué ponerte", 63: "bretón piedra del Señor", 64: "Y CarlosLopezx9j", 65: "Pero gracias por decirlo",
 66: "Cuatro piezas de cuero", 67: "La armadura más cincuenta", 68: "ganzúas Y la capucha", 69: "cuando te nombran maestre",
 70: "Es la única armadura del juego diseñada", 71: "Mercer Frey llevaba", 72: "Número doce", 73: "Setenta y dos de armadura",
 74: "Inmunidad total al veneno", 75: "doble daño en ataques furtivos", 76: "Olava la Débil te lee", 77: "Una palanca que solo existe",
 78: "En Escairim hasta la arquitectura", 79: "Tres treinta y tres", 80: "el veneno no es crimen", 81: "El del clip no era yo",
 82: "Número once", 83: "Y al bloquear crea una custodia", 84: "La misión es La única cura", 85: "te manda a la ruina",
 86: "la custodia es cóncava", 87: "la custodia se rompe", 88: "Antes del top diez", 89: "La Corona dentada",
 90: "así que la puedes llevar a la vez", 91: "Y la armadura falmer pesada", 92: "Mejor que la de ébano", 93: "Número diez",
 94: "Y aun así está en esta lista", 95: "y la magia se regenera el doble", 96: "Derrotas a", 97: "la túnica no ocupa la ranura",
 98: "A veces el juego te da dos", 99: "No se la puedes robar", 100: "Cuero negro y morado",
 101: "y más veinticinco de armadura con las cuatro", 102: "ganzúa y más daño a una mano", 103: "con Kárlia y Brynjolf",
 104: "Y aquí está la trampa que arruina", 105: "No al recibirla", 106: "Nocturnal diosa de la suerte",
 107: "Veinticuatro de armadura el casco", 108: "Y su encantamiento solo despierta", 109: "una capa de llamas",
 110: "aparece un sacerdote dragón espectral", 111: "En Laberintia te pones", 112: "Ahora las malas noticias",
 113: "Si no la recoges", 114: "Todo el trabajo de herrería", 115: "Un dios de la guerra que depende", 116: "Y un dato de los creadores",
 117: "Número siete", 118: "la magia de los hechizos y del aliento", 119: "Y cuando te golpean a veces brotan",
 120: "cien de daño de veneno", 121: "el casco más protector del juego", 122: "Lees los libros negros", 123: "Y con la túnica la piedra",
 124: "Inmune a los hechizos", 125: "La Armadura de Estigma Mortal Ligera", 126: "Y crece con cada pieza", 127: "respiras bajo el agua",
 128: "Desde el nivel treinta y seis", 129: "Y no hay marcadores", 130: "Otro junto a Tel", 131: "Y el último cofre trae la llave",
 132: "Con sus dos cimitarras", 133: "Dice la leyenda que el primero", 134: "Normal Yo también grito", 135: "Una coraza pesada de",
 136: "La daédrica protege solo tres", 137: "Te mueves en silencio", 138: "Y hasta funciona como radar",
 139: "El precio La llamada de", 140: "En el Próstilo de", 141: "Y en los archivos del juego", 142: "Tu seguidor te cargó la mochila",
 143: "Y a mí también para qué mentir", 144: "solo trece están suscritos", 145: "Número cuatro", 146: "es hielo nórdico encantado",
 147: "lo mismo que las placas de dragón con cinco", 148: "La ligera setenta y ocho", 149: "Para forjarla necesitas Herrería de ébano",
 150: "Tallador en la Aldea", 151: "Y la trampa si Déor", 152: "Ni una pieza Para siempre", 153: "Y el nombre tiene truco",
 154: "Número tres", 155: "Ochenta y dos de armadura", 156: "Se forja con escamas", 157: "Con Armadura ligera al máximo",
 158: "Un cincuenta y cinco por ciento", 159: "Y un secreto puedes forjarla", 160: "Y reaparece cada diez días",
 161: "Es la única suscripción", 162: "Número dos", 163: "Con escudo ciento treinta y seis", 164: "Y el templado con hueso",
 165: "quinientos veinticinco de armadura", 166: "Y una vez templada llega al tope", 167: "Y sus materiales son más fáciles",
 168: "Para forjar antes de que haya", 169: "Número uno", 170: "Negra con vetas rojas", 171: "La armadura pesada más fuerte",
 172: "y hay algunos fijos", 173: "Herrería noventa La otra vía", 174: "un núcleo dinamo", 175: "Y la razón del número uno",
 176: "con su escudo llega a quinientos sesenta", 177: "Es la única armadura del juego que llega al tope",
 178: "Y los drémora que van vestidos", 179: "La armadura no Y un fallo", 180: "Bethesda nos dio", 181: "Y ahora lo que prometí",
 182: "Cada punto de armadura reduce", 183: "Y el máximo del juego es un ochenta", 184: "Por eso con escudo al tope",
 185: "cualquier armadura pesada templada", 186: "El mismo ochenta por ciento", 187: "Solo cuenta contra las armas",
 188: "lo único que importa es el peso", 189: "A partir de ahí la armadura", 190: "Después hasta el hierro",
 191: "De un casco que escupe vapor", 192: "Cuál te pones tú", 193: "Y suscríbete que vamos", 194: "nuestro canal hermano",
}
assert sorted(S) == sorted(B) == list(range(1, 195))

# frase que la voz dice DENTRO del beat → búsqueda (manda sobre el casado por inicio; sobrevive a que `beats` vuelva a cortar)
FORZAR = [
 ("La Corona dentada", B[89]), ("Contra un mago muy fuerte", q("Skyrim Spellbreaker ward mage fight")),
 ("te quedas con la versión débil", q("Skyrim Nocturnal Twilight Sepulcher")), ("Número ocho Konájrik", B[106]),
 ("el casco con más armadura base", B[107]), ("Las botas y los guantes un cinco", q("Skyrim Miraak's Robes showcase")),
 ("la piedra del Atronach", B[123]), ("Número seis La Armadura", B[125]),
 ("seis mil cuatrocientas", q("Skyrim Haknir treasure gold pile")), ("el humo sale en cuanto", q("Skyrim Ebony Mail poison enemies")),
 ("El precio La llamada de", B[139]), ("Luego en la Cresta de Punta", B[140]), ("con cinco menos de peso", B[147]),
 ("Toda una isla de hielo", B[152]), ("La otra vía es la Fragua", B[173]),
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
    hall = sorted((p, k) for k in range(ultimo + 1, min(ultimo + 9, 195)) for p in [busca(h, toks(S[k]))] if p >= 0)
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
