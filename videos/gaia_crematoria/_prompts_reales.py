# -*- coding: utf-8 -*-
"""Hojas del acto 1 regeneradas en Flow con la FOTO REAL del juego como ingrediente (pedido n.º 3 del usuario, 29-oct).
Escribe prompts_reales.json: clave → {prompt, ingredientes [slugs de piezas/reales/]}. Mismas poses y MISMO ORDEN que prompts.json
(los códigos de plan.py = número de pieza). Salida de Flow → hojas_reales/<clave>_a|b.jpg (no pisa hojas/ hasta el visto bueno)."""
import json

P = json.load(open("prompts.json", encoding="utf-8"))
REF = ("Use the attached reference image(s), screenshots of the real character(s) from the game World of Warcraft, for the face, "
       "hair, beard, skin colour, armor or clothing design, emblems and colours: keep that exact look, redrawn in the art style "
       "above. ")
CAMBIOS = {   # clave → (ingredientes, [(texto viejo, texto nuevo)] para no contradecir a la foto real)
    "h01_alexandros_hoja": (["alexandros_vivo"], [("heavy ornate silver and gold plate armor of the Silver Hand with a white tabard "
                            "bearing a golden hand emblem, a long blue cape", "his armor and tabard exactly as in the reference image")]),
    "h03_renault_hoja": (["renault_comandante"], [("with slick black hair, a thin moustache and a cold proud face, in a silver paladin "
                         "breastplate and a dark grey cloak", "with the hair, beard and face of the reference image, a cold proud look, "
                         "in the armor and tabard of the reference image")]),
    "h08_tirion_joven": (["tirion"], [("Tirion Fordring in his forties: brown hair and a short brown beard, kind strong face",
                         "Tirion Fordring in his forties (younger than in the reference): the face of the reference image with brown "
                         "hair and a short brown beard, kind strong face")]),
    "h11_taelan_hoja": (["taelan"], []),
    "h13_eitrigg_hoja": (["eitrigg"], [("green skin, long white hair in a topknot, a white braided beard, tusks, a scarred face, heavy "
                         "orcish leather and iron armor", "skin, hair, beard, tusks and red spiked armor exactly as in the reference image")]),
    "h14_isillien_hoja": (["isillien_joven"], [("an old bald human with a cruel thin face and a white goatee, crimson and white "
                          "inquisitor robes with gold trim, a red mantle, a golden staff", "a human paladin with the face, red hair "
                          "and the blue, white and purple tabard of the reference image, a cruel thin look, a golden staff")]),
    "h15_villanos_hoja": (["kelthuzad", "dathrohan", "balnazzar"], []),
    "h16_consejo_hoja": (["uther", "barthilas"], [("a sly human lieutenant with black hair and a pointed beard in a grey uniform",
                         "a sly human with black hair and beard in the blue vest and white shirt of the reference image")]),
    "h17_magni_hoja": (["magni"], []),
}
out = {}
for k, (ing, cambios) in CAMBIOS.items():
    p = P[k]
    for a, b in cambios:
        assert a in p, (k, a)
        p = p.replace(a, b)
    i = p.find("Character")
    out[k] = {"prompt": p[:i] + REF + p[i:], "ingredientes": ing}
json.dump(out, open("prompts_reales.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "hojas")
