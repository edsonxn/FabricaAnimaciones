# -*- coding: utf-8 -*-
"""Lista archivos de Wowpedia por prefijo (para elegir la pegatina buena):  python _buscar_img.py "Muradin" "Lich King" ..."""
import json
import sys
import urllib.parse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}
API = "https://wowpedia.fandom.com/api.php?"

for pref in sys.argv[1:]:
    q = dict(action="query", list="allimages", aiprefix=pref.replace(" ", "_"), ailimit=40, aiprop="size", format="json")
    r = json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(q), headers=UA), timeout=40))
    ims = [f"{i['name']}({i['width']}x{i['height']})" for i in r["query"]["allimages"] if i["width"] >= 250]
    print(f"== {pref}: " + " · ".join(ims[:28]))
