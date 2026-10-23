# -*- coding: utf-8 -*-
"""Copias ASCII de las fotos de Commons (cv2 no abre rutas con acentos en Windows) y creditos.json por clave.
El original de la investigación queda en creditos_commons.json. python fotos/_claves.py"""
import json
import os
import shutil

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
CL = {
    "codice_chich": "Guerreros_Chichimecas_(Códice_Chapa_de_Mota_-_Jilotepec,_1703).jpg",
    "pareja_chich": "ParejaChichimeca.jpg",
    "carranza": "Portrait_of_Venustiano_Carranza_(cropped).jpg",
    "centro_1": "Centro_geográfico_de_México,_Tequisquiapan.jpg",
    "centro_2": "Centro_geográfico_de_México_en_Tequisquiapan,_Querétaro_01.jpg",
    "centro_3": "Centro_geográfico_de_México_en_Tequisquiapan,_Querétaro_03.jpg",
    "pendulo": "Péndulo_de_Tequisquiapan.jpg",
    "parroquia_1": "Templo_Parroquial_Santa_María_de_la_Asunción_de_Tequisquiapan.jpg",
    "parroquia_2": "Parroquia_Santa_María_de_la_Asunción_en_Tequisquiapan.jpg",
    "tequis_noche": "TequisNoche.jpg",
    "cupula": "CupolaSantaMariaTequis.jpg",
    "altar": "MainAltarSantaMariaTequis.jpg",
    "iglesia_centro": "Iglesia_de_Tequisquiapan_centro.jpg",
    "magdalena": "Iglesia_barrio_de_la_Magdalena,_Tequisquiapan,_Querétaro.jpg",
    "kiosco": "Tequisquiapan_kiosco.jpg",
    "plaza": "La_Plaza_de_Tequisquiapan.jpg",
    "portales": "PortalesTequis.jpg",
    "calle": "Calle_Niños_Héroes,_Tequisquiapan.jpg",
    "callejon": "Callejón_del_Piojo.jpg",
    "relox": "El_Relox_Hotel_&_Spa_(hotel)_en_Tequisquiapan.jpg",
    "artesano": "Artesano_iniciando_una_canasta_de_vara.jpg",
    "cestos": "BasketsTequis.jpg",
    "mercado_1": "CraftsMarketTequis.jpg",
    "mercado_2": "Mercado_de_artesanías_de_Tequisquapan._-_panoramio.jpg",
    "bordado": "OtomiEmbroideryTequis.jpg",
    "feria_entrada": "EntranceFeriaVinoTequis.jpg",
    "feria_1": "FeriaQuesoVino01.jpg",
    "feria_2": "FeriaQuesoVino02.jpg",
    "feria_3": "FeriaQuesoVino10.jpg",
    "feria_queso": "Feria_del_queso.jpg",
    "tienda_vino": "WineCheeseShopVaquitaTequis.jpg",
    "opalo": "OpaleMexique.jpg",
    "mina_opalo": "Opal_Mine_Queretaro_2.jpg",
    "bernal_1": "Peña_de_Bernal_(Querétaro,_México).jpg",
    "bernal_2": "Peña_de_Bernal,_Querétaro_(México)_I.jpg",
    "bernal_3": "Una_vista_de_la_Peña_de_Bernal.jpg",
    "bernal_4": "Vista_de_la_peña_desde_el_sendero_de_acenso.jpg",
    "bernal_iglesia": "Vista_iglesia_peña.JPG",
    "danzantes": "Danzantes_chichimecas_(Bernal,_Querétaro).jpg",
    "vinedo_bernal": "VineyardPenaBernalEMontes.JPG",
    "freixenet": "VineyardBldgFreixnet.JPG",
    "la_redonda": "Viñedos_La_Redonda,_Querétaro-_La_Redonda_vineyards_(24459213651).jpg",
    "cadereyta": "Parroquia_de_San_Pedro_y_San_Pablo,_Cadereyta,_Querétaro.JPG",
}
src = os.path.join(D, "creditos_commons.json")
if not os.path.exists(src):
    shutil.copy(os.path.join(D, "creditos.json"), src)
orig = json.load(open(src, encoding="utf-8"))
out = {}
for k, f in CL.items():
    v = orig[f]
    Image.open(os.path.join(D, f)).convert("RGB").save(os.path.join(D, k + ".jpg"), quality=93)
    out[k] = dict(v, credito_corto=v["credito_corto"])
json.dump(out, open(os.path.join(D, "creditos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "fotos con clave")
