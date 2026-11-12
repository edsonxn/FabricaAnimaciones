import json,urllib.request,urllib.parse
B='https://eldenring.fandom.com/api.php?'
def q(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(B+urllib.parse.urlencode(p),headers={'User-Agent':'Mozilla/5.0'}),timeout=30))
titles=["Godrick the Grafted","Godefroy the Grafted","Grafted Scion","Axe of Godrick","Grafted Dragon","Godrick's Great Rune","Remembrance of the Grafted","Margit, the Fell Omen","Nepheli Loux, Warrior","Kenneth Haight","Gatekeeper Gostoc","Castellan Edgar","Irina of Morne","Roderika, Spirit Tuner","Chrysalids' Memento","White Mask Varré","Sorcerer Rogier","Finger Reader Enia","Leonine Misbegotten","Warhawk Ashes","Whip","Grafted Blade Greatsword","Ancient Dragon Knight Kristoff Ashes","Mimic's Veil","Godfrey Icon","Malenia, Blade of Miquella","Godfrey, First Elden Lord","Ornamental Straight Sword","Golden Beast Crest Shield","Godrick Soldier Ashes","Marred Leather Shield","Stormveil Castle","Castle Morne","Sir Gideon Ofnir, the All-Knowing","Godrick Knight","Exile Soldier","Banished Knight","Commoner"]
out={}
for i in range(0,len(titles),20):
    d=q({'action':'query','prop':'pageimages','piprop':'original|name','titles':'|'.join(titles[i:i+20]),'format':'json','redirects':1})
    for p in d['query']['pages'].values():
        out[p['title']]=(p.get('pageimage'),p.get('original',{}).get('source'))
for t,v in out.items(): print(t,'|',v[0],'|',v[1])
print('----- allimages')
for pre in ['ER NPC','ER Render Godrick','ER Render Grafted','Godrick','ER Godrick','ER Godefroy','ER Icon Key Item Great Rune Godrick','ER Character Face','ER Gostoc','ER NPC Closeup','ER Icon weapon Grafted','ER Icon weapon Axe of Godrick','ER Icon Remembrance of the Grafted','ER Icon Key Item Chrysalid','ER Blood Obsessed','Elden ring gostoc','Eldenringkenneth','ER Irina','ER Edgar','ER Nepheli','Nepheli','ER Roderika','ER Varr','Grafted','ER Godrick\'s Dragon','ER Render Impaled']:
    d=q({'action':'query','list':'allimages','aiprefix':pre,'ailimit':50,'format':'json'})
    names=[x['name'] for x in d['query']['allimages']]
    if pre=='ER NPC': names=[n for n in names if any(k in n for k in ['Godrick','Gostoc','Kenneth','Nepheli','Edgar','Irina','Roderika','Varr','Rogier','Enia','Margit','Godefroy','Gideon'])]
    print(pre,'=>',names[:40])
