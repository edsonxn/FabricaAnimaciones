import os, sys, subprocess, glob, cv2, numpy as np
sys.path.insert(0, "../../nucleo")
import videos_stock as VS
import urllib.request
Q = [("gotas_vidrio","raindrops on glass night"),("humo","cigarette smoke dark"),("servidores","server room lights"),
("maquina","typewriter typing close up"),("multitud","crowd umbrellas rain night"),("interruptor","power switch off"),
("libros","flipping pages book"),("apreton","handshake dark"),("cafe","pouring coffee cup"),("codigo","computer code screen"),
("camara","security camera"),("poker","poker chips table"),("autos","car night rain headlights"),("fuego","house fire night"),
("robot","robotic arm factory"),("engranajes","clock gears"),("trafico","highway traffic night timelapse"),("hormigas","ants close up"),
("cables","power lines electricity"),("cerilla","match burning"),("imprenta","newspaper printing press"),("dados","dice rolling"),
("amanecer","city skyline fog sunrise"),("relampagos","lightning storm night")]
os.makedirs("clips/_m", exist_ok=True)
hojas=[]
for nom,q in Q:
    vs = VS.buscar(q, 6)[:6]
    fila=[]
    for i,v in enumerate(vs):
        p=f"clips/_m/{nom}_{i}_{v['fuente']}_{v['id']}.jpg"
        if not os.path.exists(p) and v.get("miniatura"):
            try: open(p,"wb").write(urllib.request.urlopen(urllib.request.Request(v["miniatura"],headers=VS.UA),timeout=30).read())
            except Exception as e: print("x",e)
        im=cv2.imread(p) if os.path.exists(p) else None
        im=np.zeros((135,240,3),np.uint8) if im is None else cv2.resize(im,(240,135))
        cv2.putText(im,f"{i} {v['fuente'][:2]}{v['id']} {v['dur']}s",(4,128),0,0.42,(0,255,255),1)
        fila.append(im)
    while len(fila)<6: fila.append(np.zeros((135,240,3),np.uint8))
    f=np.hstack(fila); lab=np.zeros((22,f.shape[1],3),np.uint8); cv2.putText(lab,nom,(4,16),0,0.55,(255,255,255),1)
    hojas.append(np.vstack([lab,f]))
for k in range(0,len(hojas),6):
    cv2.imwrite(f"previews/stock_{k//6}.jpg", np.vstack(hojas[k:k+6]))
print("ok")
