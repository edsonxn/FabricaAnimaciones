import json,urllib.request,urllib.parse
B='https://eldenring.fandom.com/es/api.php?'
for s in ["Hacha de Godrick","Dragón injertado","Recuerdo de las crisálidas","Velo de imitador","Látigo","Espadón injertado","Icono de Godfrey","Margit","Castillo de Morne","Edgar","Irina","Varré","Gideon","Halcón de guerra","Escudo deteriorado","Cárcel eterna del linaje dorado","Kristoff","Leonino","Monumento","Espada recta ornamental","Cabaña en Colina Tormentosa","Fuerte de Haight","Caballero de Godrick","Soldado proscrito","Caballero proscrito","Lago de Agheel","Celda apartada","Torre de defensa"]:
    d=json.load(urllib.request.urlopen(urllib.request.Request(B+urllib.parse.urlencode({'action':'query','list':'search','srsearch':s,'format':'json','srlimit':5}),headers={'User-Agent':'Mozilla/5.0'})))
    print(s,'=>',[x['title'] for x in d['query']['search']])
