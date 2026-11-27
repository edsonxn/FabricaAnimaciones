# -*- coding: utf-8 -*-
"""Grupos de aparición (WN de _coords.md): tooltip de PNJ de Wowhead Forever (campo map) → casillas de 5 % con más puntos y su media.
    python _apariciones.py → imprime y guarda _apariciones.json (25-nov-2026)"""
import json,urllib.request,collections,sys
UA={"User-Agent":"Mozilla/5.0"}
npcs={4640:"retador",4641:"cazavientos",4643:"corremanadas",4662:"zarposea",4376:"arana",4378:"ermitana",1108:"gorila",1557:"gorila_anciano",1514:"mokk",1449:"unbagwa",4142:"tortuga",4143:"mordedor",4399:"cavapozos",255901:"reptador",2544:"reptador_sur",259962:"fimbo",2725:"cria",747:"murloc",750:"vomitatintas",751:"comecarnes",752:"oraculo",5426:"hiena_llagapata",5429:"roc_fuego",5428:"roc",5262:"tronador",5274:"patriarca",5260:"simio",5268:"oso",767:"jaguar",259055:"cazadora",2735:"elem_inf",92:"elem",2736:"elem_sup",259267:"coyote",259263:"merodeador",258522:"sootfur",258317:"benjy",2252:"ogro",2253:"tosco",2254:"aplastador",2255:"mago",2684:"rizz",2453:"logrosh",5982:"destripador",5988:"scorpok",5984:"risitas",7506:"lynnore",7505:"drazial"}
out={}
for i,n in npcs.items():
    d=json.loads(urllib.request.urlopen(urllib.request.Request(f"https://nether.wowhead.com/forever/tooltip/npc/{i}?locale=0",headers=UA)).read())
    m=d.get("map") or {}
    pts=[p for v in (m.get("coords") or {}).values() for p in v]
    c=collections.defaultdict(list)
    for x,y in pts: c[(int(x//5),int(y//5))].append((x,y))
    top=sorted(c.values(),key=len,reverse=True)[:4]
    cl=[(round(sum(p[0] for p in g)/len(g),1),round(sum(p[1] for p in g)/len(g),1),len(g)) for g in top]
    out[n]=dict(npc=i,zone=m.get("zone"),n=len(pts),cl=cl)
    print(n,i,"zona",m.get("zone"),"n",len(pts),cl)
json.dump(out,open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),"_apariciones.json"),"w"),indent=1)
