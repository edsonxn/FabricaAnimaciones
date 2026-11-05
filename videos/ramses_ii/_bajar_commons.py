# -*- coding: utf-8 -*-
"""Descarga el material real de Commons a imagenes/ (con creditos.json) y hace una hoja previews/_commons.jpg."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import cv2, numpy as np
import imagenes_web as IW
L = {
 "momia_frente": "File:Mummy of Ramses II - Cairo Museum - front - TIMEA (n.d.) - front - timea.jpg",
 "momia_01": "File:Mummy of Ramesses II - 01-cropped.jpg",
 "momia_frontal": "File:Mummy of Ramesses II - 02 (front).JPG",
 "horemheb_amon": "File:Statue of king Horemheb with the god Amun, limestone - Museo Egizio Turin C 768 p01.jpg",
 "ramses1_relieve": "File:Relief on the South Wall of a Chapel of Ramesses I MET DP337514.jpg",
 "seti1_relieve": "File:Relief of Seti I.jpg",
 "seti1_momia": "File:Seti I mummy head profile.png",
 "kadesh_rameseo": "File:Battle scene from the Great Kadesh reliefs of Ramses II on the Walls of the Ramesseum.jpg",
 "tratado_estambul": "File:Kadesh Treaty, written in Akkadian. 1269 BCE. From Boğazköy, Turkey. Clay tablet. Museum o",
 "nefertari_qv66": "File:Maler der Grabkammer der Nefertari 004.jpg",
 "rameseo_coloso": "File:Osiride Court and Fallen Colossus, Ramesseum, Thebes (1890) - TIMEA.jpg",
 "luxor_ramses": "File:Ramses II in Luxor Temple.jpg",
 "mapa_satelite": "File:MiddleEast.A2003031.0820.250m.jpg",
}
os.makedirs("imagenes", exist_ok=True)
hoja = []
for nom, tit in L.items():
    try:
        if not tit.endswith(("jpg", "JPG", "png", "jpeg")):
            r = [x for x in IW.commons(tit.replace("File:", ""), n=3)][0]
        else:
            r = IW.info_archivo(tit)
        ruta = IW.guardar_commons(r, "imagenes", nom)
        im = cv2.imread(ruta)
        print(nom, ruta, None if im is None else im.shape, r["licencia"])
        if im is not None:
            t = cv2.resize(im, (320, 240)); cv2.putText(t, nom, (6, 20), 0, 0.55, (0, 255, 255), 2); hoja.append(t)
    except Exception as e:
        print(nom, "ERROR", e)
while len(hoja) % 4: hoja.append(np.zeros((240, 320, 3), np.uint8))
cv2.imwrite("previews/_commons.jpg", np.vstack([np.hstack(hoja[i:i + 4]) for i in range(0, len(hoja), 4)]))
