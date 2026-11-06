# -*- coding: utf-8 -*-
"""TELE SIMULADA (pedido del usuario, 5-nov: «la de la tele la simulas, haces una animación»): capturas/tele/tele.html.
Sala con profundidad (pared, repisa con planta, lámpara, tele con brillo en la pared, mueble, respaldo del sofá desenfocado delante).
Modos por hash: #aviso (video → pausa → robot de Puente TV que dice el aviso real de las 12:35 con la boca siguiendo SU volumen → sigue el video),
#revision (sala de revisión: capturas reales rev_1/rev_3 + clic del control), #protector (robotaller en la tele, captura real tablero_vivo_1).
El robot copia RobotView.kt (D:/PuenteTV/tv/…/RobotView.kt): cabeza #323855→#141727, visor negro, ojos en píldora, boca de barras, antena.
  python tele.py      (luego: python capturas.py tele_aviso tele_revision tele_protector)"""
import json
import os
import shutil
import subprocess

import numpy as np

FF = "C:/ffmpeg/bin/ffmpeg.exe"
DEST = "capturas/tele"
CAPS = "D:/PuenteTV/capturas"
T_ROBOT = 3.6          # segundo de la toma #aviso en que sale el robot y empieza la voz


def envolvente(mp3, fps=30):
    pcm = subprocess.run([FF, "-v", "error", "-i", mp3, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    n = 16000 // fps
    rms = np.array([np.sqrt(np.mean(x[i:i + n] ** 2)) for i in range(0, len(x) - n, n)])
    return [round(float(v), 3) for v in np.clip(rms / (rms.max() + 1e-6), 0, 1)]


HTML = r"""<!doctype html><meta charset=utf-8><style>
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#0b0d16;font-family:'Segoe UI',sans-serif}
#sala{position:absolute;inset:-4%;transform-origin:50% 45%;animation:deriva 14s ease-in-out infinite alternate}
@keyframes deriva{from{transform:scale(1.02) translate(0,0)}to{transform:scale(1.07) translate(-1.2%,.6%)}}
.pared{position:absolute;inset:0;background:radial-gradient(ellipse 60% 55% at 50% 42%,#2a2340 0%,#1a1628 45%,#0e0c18 100%)}
.zoc{position:absolute;left:0;right:0;top:71%;bottom:0;background:linear-gradient(#1b1622,#120f17)}
.zoc:before{content:"";position:absolute;left:0;right:0;top:0;height:6px;background:#2c2436}
#halo{position:absolute;left:50%;top:40%;width:1500px;height:900px;margin:-450px 0 0 -750px;border-radius:50%;filter:blur(60px);opacity:.55;background:radial-gradient(#6a5cff 0%,transparent 65%);transition:background .6s}
.repisa{position:absolute;left:7%;top:30%;width:15%;height:12px;background:#3a2e2a;border-radius:3px;box-shadow:0 14px 26px #000a}
.maceta{position:absolute;left:10%;top:21.5%;width:5%;height:8.6%;background:linear-gradient(#a8664a,#6e3e2c);border-radius:0 0 18px 18px}
.hoja{position:absolute;width:5%;height:9%;background:linear-gradient(#3f8a5a,#1f4d33);border-radius:0 100% 0 100%;transform-origin:0 100%}
.libro{position:absolute;top:24%;width:1.1%;height:6%;border-radius:2px}
.lampara{position:absolute;right:8%;top:24%;width:9%;height:13%;background:linear-gradient(#f3d9a8,#c9a46b);clip-path:polygon(18% 0,82% 0,100% 100%,0 100%);box-shadow:0 0 80px #f5c97a}
.cono{position:absolute;right:2%;top:36%;width:21%;height:40%;background:linear-gradient(#f5c97a44,transparent);clip-path:polygon(35% 0,65% 0,100% 100%,0 100%);filter:blur(6px)}
.pie{position:absolute;right:12.2%;top:37%;width:.7%;height:34%;background:#2a2230}
#tv{position:absolute;left:50%;top:40%;width:960px;height:560px;margin:-300px 0 0 -480px;background:#07080c;border-radius:14px;padding:16px;box-sizing:border-box;
 box-shadow:0 0 0 2px #23242c,0 30px 60px #000c,inset 0 0 0 1px #000}
#pant{position:relative;width:100%;height:100%;overflow:hidden;border-radius:4px;background:#000}
#pant canvas,#pant img{position:absolute;inset:0;width:100%;height:100%}
#brillo{position:absolute;inset:0;background:linear-gradient(115deg,#ffffff14 0%,#ffffff05 30%,transparent 31%);pointer-events:none}
.mueble{position:absolute;left:28%;right:28%;top:73.5%;height:9%;background:linear-gradient(#3b2f2b,#231b19);border-radius:6px;box-shadow:0 20px 40px #000c}
.barra{position:absolute;left:41%;right:41%;top:71.6%;height:1.6%;background:#15161c;border-radius:8px}
.pata{position:absolute;left:49.2%;width:1.6%;top:66%;height:6%;background:#121318}
.sofa{position:absolute;left:-6%;right:-6%;bottom:-15%;height:32%;background:radial-gradient(ellipse 60% 70% at 50% 100%,#2d2538,#151119);border-radius:50% 50% 0 0;filter:blur(7px)}
.sofa2{position:absolute;left:4%;bottom:6%;width:16%;height:16%;background:#3a2b3c;border-radius:40%;filter:blur(9px)}
#vel{position:absolute;inset:0;background:radial-gradient(ellipse at center,transparent 55%,#000a 100%);pointer-events:none}
.mando{position:absolute;right:16%;bottom:4%;width:90px;height:230px;background:linear-gradient(#e7e7ee,#b8b9c4);border-radius:45px;transform:rotate(-12deg);box-shadow:0 20px 40px #000c;opacity:0;transition:opacity .4s}
.mando i{position:absolute;left:50%;top:40px;width:46px;height:46px;margin-left:-23px;border-radius:50%;background:#2c2d36}
.mando b{position:absolute;left:50%;top:52px;width:22px;height:22px;margin-left:-11px;border-radius:50%;background:#6c6e7c;transition:background .1s}
.mando.on{opacity:1}.mando b.pulsa{background:#9aa0ff;box-shadow:0 0 18px #9aa0ff}
</style>
<div id=sala>
 <div class=pared></div><div id=halo></div><div class=zoc></div>
 <div class=repisa></div><div class=maceta></div>
 <div class=hoja style="left:12.4%;top:13.6%;transform:rotate(-30deg)"></div><div class=hoja style="left:12.6%;top:14.6%;transform:rotate(25deg) scaleX(-1)"></div>
 <div class=hoja style="left:12.5%;top:12.2%;transform:rotate(-2deg)"></div>
 <div class=libro style="left:17%;background:#5b6fa8"></div><div class=libro style="left:18.3%;background:#a85b62;height:5.4%;top:24.6%"></div><div class=libro style="left:19.6%;background:#c9a24f;transform:rotate(12deg)"></div>
 <div class=pie></div><div class=lampara></div><div class=cono></div>
 <div class=pata></div><div class=barra></div>
 <div id=tv><div id=pant><canvas id=c width=928 height=528></canvas><div id=brillo></div></div></div>
 <div class=mueble></div>
 <div class=sofa></div><div class=sofa2></div>
 <div class=mando id=mando><i></i><b id=boton></b></div>
</div><div id=vel></div>
<script>
const ENV=__ENV__, T_ROBOT=__TR__, TXT="La comida está lista. Ya pueden bajar a comer, se enfría.";
const modo=(location.hash||"#aviso").slice(1), c=document.getElementById("c"), g=c.getContext("2d"), W=c.width, H=c.height;
const img=(s)=>{const i=new Image();i.src=s;return i};
const REV1=img("rev_1_marcar.png"), REV3=img("rev_3_lista.png"), TAB=img("tablero_vivo_1.png");
const halo=document.getElementById("halo"); let t0=performance.now();
function rr(x,y,w,h,r){g.beginPath();g.roundRect(x,y,w,h,r)}
function video(t,pausa){ // «lo que estaba viendo»: un paisaje animado cualquiera con barra de reproducción
  const k=pausa?0:t; const sky=g.createLinearGradient(0,0,0,H);sky.addColorStop(0,"#4fa3e8");sky.addColorStop(1,"#bfe4ff");g.fillStyle=sky;g.fillRect(0,0,W,H);
  g.fillStyle="#ffe27a";g.beginPath();g.arc(W*.78,H*.25,46,0,7);g.fill();
  for(let i=0;i<4;i++){const x=((i*290+k*30)%(W+300))-150;g.fillStyle="#ffffffd0";g.beginPath();g.ellipse(x,90+i*28,80,24,0,0,7);g.ellipse(x+50,80+i*28,60,26,0,0,7);g.fill()}
  [["#5cb85c",.62,.10],["#3f9a4a",.72,.16],["#2f7a3a",.84,.24]].forEach(([col,y,s],j)=>{g.fillStyle=col;g.beginPath();g.moveTo(0,H);
    for(let x=0;x<=W;x+=16)g.lineTo(x,H*y+Math.sin(x*.01+j*2+k*s)*26);g.lineTo(W,H);g.fill()});
  g.fillStyle="#0009";g.fillRect(0,H-46,W,46);g.fillStyle="#fff4";g.fillRect(20,H-26,W-40,5);g.fillStyle="#ff3b3b";g.fillRect(20,H-26,(W-40)*(.31+k*.004),5);
  g.beginPath();g.arc(20+(W-40)*(.31+k*.004),H-23.5,8,0,7);g.fill();
  if(pausa){g.fillStyle="#0008";g.fillRect(0,0,W,H);g.fillStyle="#fff";rr(W/2-40,H/2-50,26,100,6);g.fill();rr(W/2+14,H/2-50,26,100,6);g.fill()}
}
function robot(t){ // RobotView.kt: la boca, los ojos y la antena siguen el volumen real de la voz
  const i=Math.floor(t*30), lv=t>=0&&i<ENV.length?ENV[i]:0, c1="#3ee08f", c2="#b9ffd9";
  const bg=g.createRadialGradient(W/2,H*.42,40,W/2,H*.42,W*.7);bg.addColorStop(0,"#1b2140");bg.addColorStop(1,"#070912");g.fillStyle=bg;g.fillRect(0,0,W,H);
  const cx=W/2, hw=250, hh=190, hx=cx-hw/2, hy=110;
  let gr=g.createRadialGradient(cx,hy+hh/2,20,cx,hy+hh/2,260);gr.addColorStop(0,`rgba(62,224,143,${.25+lv*.35})`);gr.addColorStop(1,"transparent");g.fillStyle=gr;g.fillRect(0,0,W,H);
  g.strokeStyle="#3A4060";g.lineWidth=7;g.beginPath();g.moveTo(cx,hy);g.lineTo(cx,hy-48);g.stroke();
  gr=g.createRadialGradient(cx,hy-54,2,cx,hy-54,30);gr.addColorStop(0,`rgba(62,224,143,${.5+lv*.5})`);gr.addColorStop(1,"transparent");g.fillStyle=gr;g.fillRect(cx-40,hy-94,80,80);
  g.fillStyle=c1;g.beginPath();g.arc(cx,hy-54,11,0,7);g.fill();
  [-1,1].forEach(s=>{const ex=cx+s*(hw/2+14);const l=g.createLinearGradient(ex-16,0,ex+16,0);l.addColorStop(0,"#2C3150");l.addColorStop(1,"#191C2E");g.fillStyle=l;rr(ex-16,hy+50,32,90,10);g.fill()});
  let l=g.createLinearGradient(0,hy,0,hy+hh);l.addColorStop(0,"#323855");l.addColorStop(1,"#141727");g.fillStyle=l;rr(hx,hy,hw,hh,40);g.fill();
  g.strokeStyle="#ffffff3c";g.lineWidth=2;g.stroke();
  const vx=hx+22,vy=hy+22,vw=hw-44,vh=hh-44;l=g.createLinearGradient(0,vy,0,vy+vh);l.addColorStop(0,"#070912");l.addColorStop(1,"#0B0E1C");g.fillStyle=l;rr(vx,vy,vw,vh,28);g.fill();
  const blink=(t%3.7)<.12?.15:1, ew=vw*.17, eh=vh*.30*blink, ey=vy+vh*.34;
  [-1,1].forEach(s=>{const ex=cx+s*vw*.2;l=g.createLinearGradient(0,ey-eh/2,0,ey+eh/2);l.addColorStop(0,c2);l.addColorStop(1,c1);g.fillStyle=l;rr(ex-ew/2,ey-eh/2,ew,eh,ew*.45);g.fill()});
  const my=vy+vh*.74, mw=vw*.56, bars=9, bw=mw/bars;
  for(let k=0;k<bars;k++){const ph=Math.sin(t*18+k*1.3)*.5+.5, bh=6+lv*48*(.35+.65*ph)*(1-Math.abs(k-4)/6);
    l=g.createLinearGradient(0,my-bh/2,0,my+bh/2);l.addColorStop(0,c2);l.addColorStop(1,c1);g.fillStyle=l;rr(cx-mw/2+k*bw+bw*.2,my-bh/2,bw*.6,bh,bw*.3);g.fill()}
  g.fillStyle="#3ee08f";rr(cx-46,342,92,30,15);g.fill();g.fillStyle="#06210f";g.font="800 16px Segoe UI";g.textAlign="center";g.fillText("LISTO",cx,363);
  const n=Math.max(0,Math.min(TXT.length,Math.floor(t/3.9*TXT.length)));
  g.fillStyle="#f2f5ff";g.font="700 30px Segoe UI";const s=TXT.slice(0,n),p=s.split(". ");
  g.fillText(p[0]+(p.length>1?".":""),cx,420);if(p.length>1)g.fillText(p.slice(1).join(". "),cx,460);
  g.strokeStyle="#3ee08f";g.lineWidth=3;g.beginPath();for(let x=0;x<=360;x+=4){const y=490+Math.sin(x*.09+t*14)*lv*12;x?g.lineTo(cx-180+x,y):g.moveTo(cx-180,y)}g.stroke();
}
function foto(im,t,dur,z0,z1){g.fillStyle="#000";g.fillRect(0,0,W,H);if(!im.complete)return;const k=Math.min(1,t/dur),z=z0+(z1-z0)*k,
  r=Math.max(W/im.width,H/im.height)*z,w=im.width*r,h=im.height*r;g.drawImage(im,(W-w)/2,(H-h)/2*(1+.2*k),w,h)}
const mando=document.getElementById("mando"),boton=document.getElementById("boton");
function pulsa(){boton.classList.add("pulsa");setTimeout(()=>boton.classList.remove("pulsa"),220)}
let pulsado={};
function cuadro(){
  const t=(performance.now()-t0)/1000;
  if(modo==="aviso"){
    if(t<T_ROBOT-.6){video(t,false);halo.style.background="radial-gradient(#79c2ff 0%,transparent 65%)"}
    else if(t<T_ROBOT){video(t,true)}
    else if(t<T_ROBOT+4.6){robot(t-T_ROBOT);halo.style.background="radial-gradient(#3ee08f 0%,transparent 65%)"}
    else{video(t-4.6-.6,false);halo.style.background="radial-gradient(#79c2ff 0%,transparent 65%)"}
  } else if(modo==="revision"){
    mando.classList.add("on");
    if(t<4){foto(REV1,t,4,1,1.08);if(t>1.2&&!pulsado.a){pulsado.a=1;pulsa()}}
    else{foto(REV3,t-4,5,1.08,1);if(!pulsado.b){pulsado.b=1;pulsa()}}
    halo.style.background="radial-gradient(#8a6cff 0%,transparent 65%)";
  } else {foto(TAB,t,8,1.0,1.15);halo.style.background="radial-gradient(#ffd36a 0%,transparent 65%)"}
  requestAnimationFrame(cuadro);
}
requestAnimationFrame(()=>{t0=performance.now();cuadro()});
</script>"""


if __name__ == "__main__":
    os.makedirs(DEST, exist_ok=True)
    for f in ("rev_1_marcar.png", "rev_3_lista.png", "tablero_vivo_1.png"):
        shutil.copy(f"{CAPS}/{f}", f"{DEST}/{f}")
    html = HTML.replace("__ENV__", json.dumps(envolvente("sfx/tele_1235.mp3"))).replace("__TR__", str(T_ROBOT))
    open(f"{DEST}/tele.html", "w", encoding="utf-8").write(html)
    print(f"{DEST}/tele.html")
