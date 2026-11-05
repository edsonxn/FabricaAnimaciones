# -*- coding: utf-8 -*-
"""Segunda tanda de material real de Commons (min 2:00-9:36) a imagenes/ (con creditos.json).
No pisa archivos existentes. Recortes rembg con --rec; hoja previews/_commons2.jpg con --hoja."""
import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2, numpy as np
import imagenes_web as IW

L = {
 "muwatalli_relieve": "File:Sirkeli Hüyük 04 2004 hethitisches Felsrelief am Ceyhan.jpg",
 "hattusili_relieve": "File:Firaktin1.jpg",
 "abusimbel_kadesh": "File:Templo de Ramsés II, Abu Simbel, Egipto, 2022-04-02, DD 74-76 HDR.jpg",
 "espias_shasu": "File:Ancient carving - Shasu spies being beaten by Egyptians.png",
 "carro_hitita": "File:Ankara Anatolian Civilizations Carchemish orthostats Long Wall Chariot scene A in 2011 02.jpg",
 "carro_tut": "File:Chariot of Tutankhamun.jpg",
 "khopesh": "File:Khopesh sword dedicated to Ramasses II-E 25689-IMG 2660.JPG",
 "tratado_karnak": "File:Karnak Ägyptisch-Hethitischer Friedensvertrag 01.jpg",
 "qantir_pi_ramses": "File:Kolossalstatue Qantir.JPG",
 "qantir_azulejos": "File:Tiles from the railing of a throne dais of Ramesses II MET EG138.jpg",
 "rameseo_vista": "File:Ramesseum, Luxor, Egipto, 2022-04-03, DD 08.jpg",
 "abusimbel_santuario": "File:Großer Tempel (Abu Simbel) Sonnenwunder 05.jpg",
 "abusimbel_nefertari": "File:Templo de Nefertari, Abu Simbel, Egipto, 2022-04-02, DD 153.jpg",
 "estatua_usurpada": "File:Statue of Amenhotep II usurped by Ramesses II, granite - Museo Egizio Turin C 1381 p01.jpg",
 "cartucho_ramses": "File:Flickr - Gaspa - Tempio di Karnak, cartiglio di Ramesse II.jpg",
 "hijos_procesion": "File:Sons of Ramesses II.jpg",
 "kv5_plano": "File:KV5 sons of Rameses II Schematic.jpg",
 "kv5_entrada": "File:Entrance of Tomb KV5 of Ramesses II's sons.jpg",
 "merenptah": "File:Buste de Meremptah (la Villette, 2023) (cropped).jpg",
 "deir_el_bahari": "File:Cliffs of Deir el-Bahri.JPG",
 "db320_1881": "File:DB320 Mummies 1881.jpg",
 "ataud_ramses": "File:Coffin of Ramesses II 02.jpg",
 "belzoni_retrato": "File:Giovanni Battista Belzoni by William Brockedon.png",
 "belzoni_memnon": "File:Aglio - Belzoni - Memnon.jpg",
 "shelley_retrato": "File:Portrait of Percy Bysshe Shelley by Curran, 1819.jpg",
 "ozymandias_examiner": "File:Ozymandias The Examiner 1818.jpg",
 "abusimbel_traslado": "File:Dismantling of the statues of the Great Temple.jpg",
 "abusimbel_traslado2": "File:International cooperation, Abu Simbel - UNESCO - PHOTO0000003243 0001.tiff",
 "presa_asuan": "File:Aswan High Dam-1.jpg",
 "desfile_2021": "File:Royal mummies moved to Cairo museum in 'Golden Parade' - News 360 Tv.webm",
 "nmec": "File:National Museum of Egyptian Civilization 2022 01.jpg",
 "mapa_hititas": "File:Starożytny Bliski Wschód po bitwie pod Kadesz XIII w. p.n.e..jpg",
}
# recortes sin fondo: nombre de salida -> imagen de origen
REC = {"carro_tut": "carro_tut", "khopesh": "khopesh", "tratado_tablilla": "tratado_estambul",
       "estatua_usurpada": "estatua_usurpada", "merenptah": "merenptah", "ataud_ramses": "ataud_ramses"}


def existe(nom):
    return [f for f in glob.glob(os.path.join("imagenes", nom + ".*")) if not f.endswith("_rec.png")]


def bajar():
    for nom, tit in L.items():
        if existe(nom):
            print(nom, "ya existe, no se pisa"); continue
        try:
            r = IW.info_archivo(tit)
            if not r:
                print(nom, "NO ENCONTRADO", tit); continue
            ruta = IW.guardar_commons(r, "imagenes", nom)
            im = cv2.imread(ruta)
            print(nom, ruta, None if im is None else im.shape, r["licencia"])
        except Exception as e:
            print(nom, "ERROR", e)


def recortar():
    from rembg import remove
    from PIL import Image
    for sal, ori in REC.items():
        dst = os.path.join("imagenes", sal + "_rec.png")
        if os.path.exists(dst):
            print(dst, "ya existe"); continue
        f = existe(ori)
        if not f:
            print(sal, "sin original"); continue
        im = Image.open(f[0]).convert("RGB")
        out = remove(im)
        a = np.array(out)[:, :, 3]
        ys, xs = np.where(a > 10)
        if len(xs):
            out = out.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        out.save(dst)
        print(dst, out.size)


def hoja():
    cel = []
    for nom in list(L) + [s + "_rec" for s in REC]:
        f = existe(nom) if not nom.endswith("_rec") else glob.glob(os.path.join("imagenes", nom + ".png"))
        if not f:
            continue
        im = cv2.imread(f[0], cv2.IMREAD_UNCHANGED)
        if im is None:
            continue
        if im.ndim == 2:
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        if im.shape[2] == 4:
            a = im[:, :, 3:4].astype(np.float32) / 255
            im = (im[:, :, :3] * a + 128 * (1 - a)).astype(np.uint8)
        c = np.full((240, 320, 3), 128 if nom.endswith("_rec") else 30, np.uint8)
        h, w = im.shape[:2]; s = min(320 / w, 216 / h)
        t = cv2.resize(im, (max(1, int(w * s)), max(1, int(h * s))), interpolation=cv2.INTER_AREA)
        y0, x0 = 24 + (216 - t.shape[0]) // 2, (320 - t.shape[1]) // 2
        c[y0:y0 + t.shape[0], x0:x0 + t.shape[1]] = t
        cv2.putText(c, f"{nom} {w}x{h}", (4, 17), 0, 0.45, (0, 255, 255), 1)
        cel.append(c)
    while len(cel) % 4:
        cel.append(np.zeros((240, 320, 3), np.uint8))
    cv2.imwrite("previews/_commons2.jpg", np.vstack([np.hstack(cel[i:i + 4]) for i in range(0, len(cel), 4)]))
    print("previews/_commons2.jpg", len(cel))


if __name__ == "__main__":
    a = sys.argv[1:] or ["--bajar", "--rec", "--hoja"]
    if "--bajar" in a: bajar()
    if "--rec" in a: recortar()
    if "--hoja" in a: hoja()
