import sys, os, json
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import imagenes_web as I
from PIL import Image, ImageDraw
from concurrent.futures import ThreadPoolExecutor
D = r"C:\FabricaAnimaciones\videos\voynich\imagenes\miniaturas"
res = {}
nums = list(range(1, 245))
for k in range(0, len(nums), 40):
    tit = "|".join(f"File:Voynich Manuscript ({n}).jpg" for n in nums[k:k+40])
    r = I._api(action="query", titles=tit, prop="imageinfo", iiprop="url|size", iiurlwidth=300)
    for p in r["query"]["pages"].values():
        if "imageinfo" in p:
            n = int(p["title"].split("(")[1].split(")")[0])
            res[n] = p["imageinfo"][0]
print("encontradas", len(res), "de", len(nums))
def bajar(n):
    ru = os.path.join(D, f"{n}.jpg")
    if not os.path.exists(ru):
        I.descargar(res[n]["thumburl"], ru, I.UA)
    return n
with ThreadPoolExecutor(6) as ex: list(ex.map(bajar, sorted(res)))
json.dump({n: (v["width"], v["height"]) for n, v in res.items()}, open(os.path.join(D, "tam.json"), "w"))
ks = sorted(res)
for s in range(0, len(ks), 48):
    grupo = ks[s:s+48]
    W, H = 200, 270
    hoja = Image.new("RGB", (W*8, H*6), (30, 30, 30))
    for i, n in enumerate(grupo):
        im = Image.open(os.path.join(D, f"{n}.jpg")).convert("RGB"); im.thumbnail((W-6, H-24))
        x, y = (i % 8)*W, (i//8)*H
        hoja.paste(im, (x+3, y+20)); ImageDraw.Draw(hoja).text((x+6, y+4), str(n), fill=(255, 255, 0))
    hoja.save(os.path.join(D, f"hoja_{s//48}.jpg"), quality=80)
print("hojas", (len(ks)+47)//48)
