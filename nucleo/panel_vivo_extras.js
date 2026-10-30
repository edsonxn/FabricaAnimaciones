"use strict";
// La vista «En vivo» con mundo propio (30-oct-2026): lo teatral se dispara con datos reales y cada letrero dice la cifra real. Lo que aquí se dibuja entra por `Taller.Cap`.
// Probar: Extras.prueba("bug"|"jefe"|"relevo"|"usuario"|"pregunta"|"carta"|"loteria"|"logro"|"estreno"|"resumen"), ?canal=<alias>, ?fiesta=muertos|navidad, ?dorado=1
window.Extras=(()=>{
  const {g,caja,marco,circ,aro,elip,raya,letra,corazon,camino,figura,MADERA,TINTA,ROSA,ROJO,AMAR,AZUL,VERDE,LILA,COLORES}=Taller.prim;
  const Cap=Taller.Cap,D=Taller.dim;
  const CEMPA="#ff9a1f",CEMPA2="#ffc23d";
  const ahoraS=()=>Date.now()/1000;
  const guarda=(k,v)=>{try{localStorage.setItem(k,v);}catch(e){}};
  const lee=k=>{try{return localStorage.getItem(k);}catch(e){return null;}};
  const hash=s=>{let h=7;for(const c of String(s))h=(h*31+c.charCodeAt(0))>>>0;return h;};
  const M={mundo:null,canal:"",r:null,ctx:null,preg:"",pregT:0,video:"",pedidoT:-1e9,clima:0,boton:{}};
  const Son_=(f)=>{try{f();}catch(e){}};

  // ---- imágenes: de una en una, nunca más de dos a la vez (no estorbar a un render)
  const IMG=new Map();let cargando=0;const cola=[];
  function sigueImg(){while(cargando<2&&cola.length){const [u,im]=cola.shift();cargando++;im.onload=im.onerror=()=>{cargando--;sigueImg();};im.src=u;}}
  function img(u){
    if(!u)return null;
    let im=IMG.get(u);
    if(!im){im=new Image();IMG.set(u,im);cola.push([u,im]);sigueImg();}
    return im.complete&&im.naturalWidth?im:null;
  }
  const url=(v,rel,w=200)=>v&&rel?`/v2/mini/${encodeURIComponent(v)}/${rel.split("/").map(encodeURIComponent).join("/")}?w=${w}`:null;
  const cubre=(im,x,y,w,h)=>{const r=Math.max(w/im.naturalWidth,h/im.naturalHeight),iw=w/r,ih=h/r;g.drawImage(im,(im.naturalWidth-iw)/2,(im.naturalHeight-ih)/2,iw,ih,x,y,w,h);};
  function lineas(txt,ancho,n){
    const fila=[];let l="";
    for(const p of String(txt||"").replace(/\s+/g," ").split(" ")){
      const c=l?l+" "+p:p;
      if(g.measureText(c).width>ancho&&l){fila.push(l);l=p;if(fila.length===n)break;}else l=c;
    }
    if(fila.length<n&&l)fila.push(l);
    else if(fila.length===n)fila[n-1]=fila[n-1].replace(/\s*\S*$/,"")+"…";
    return fila;
  }
  function pastilla(txt,x,y,d,c){
    g.font=`650 ${Math.max(10,11*d.K)}px "Segoe UI",system-ui,sans-serif`;
    const w=g.measureText(txt).width+18,h=Math.max(19,19*d.K),px=Math.max(d.m,Math.min(d.W-w-d.m,x-w/2));
    caja(px,y,w,h,h/2,d.pal["--panel"]);marco(px,y,w,h,h/2,c||d.pal["--faint"],1.2);
    g.fillStyle=d.pal["--txt"];g.textAlign="left";g.textBaseline="middle";g.fillText(txt,px+9,y+h/2+.5);g.textBaseline="alphabetic";
  }

  // ---- el taller de cada canal: paleta, pared y lo que lleva puesto el robot
  const pl=(muro,muro2,suelo,mesa,acc,ex={})=>({"--muro":muro,"--muro2":muro2,"--suelo":suelo,"--mesa":mesa,"--acc":acc,"--txt":"#f2f3f8","--mut":"#aeb4c4","--faint":"#6f7688","--panel":"#14161d",...ex});
  const claro={"--txt":"#33261a","--mut":"#6c5a48","--faint":"#94836f","--panel":"#fff6e8"};
  const antorcha=(x,y,T,K)=>{caja(x-2*K,y,4*K,16*K,1,"#5b4330");const f=Math.sin(T*9+x)*1.6*K;elip(x+f*.4,y-5*K,4.6*K,8*K,"#ff8a2a");elip(x+f*.2,y-3*K,2.5*K,5*K,"#ffd166");};
  const nieve=(d,t,n,c="#ffffff")=>{g.fillStyle=c;for(let i=0;i<n;i++){const s=i*37.7,x=(s*13+Math.sin(t/900+i)*14)%d.W,y=d.PCH+((t*.018+s*9)%(d.sue-d.PCH));g.globalAlpha=.25+.5*((i%3)/3);g.beginPath();g.arc(x,y,1.1+(i%3)*.6,0,7);g.fill();}g.globalAlpha=1;};
  const TEMAS={
    cronicas_warcraft:{pal:pl("#1f2430","#2a3040","#3a2f25","#5b4330","#e0a93a"),pared(d,t){
      g.strokeStyle="#2c3344";g.lineWidth=1;for(let f=0;f<4;f++){const y=d.PCH+f*(d.sue-d.PCH)/4;for(let c=-1;c<16;c++){g.strokeRect(c*d.W/15+(f%2)*d.W/30,y,d.W/15,(d.sue-d.PCH)/4);}}
      for(const k of [.2,.5,.8]){const x=k*d.W*d.AN;g.fillStyle="#7a1f2b";g.beginPath();g.moveTo(x-9*d.K,d.PCH);g.lineTo(x+9*d.K,d.PCH);g.lineTo(x+9*d.K,d.PCH+30*d.K);g.lineTo(x,d.PCH+36*d.K);g.lineTo(x-9*d.K,d.PCH+30*d.K);g.closePath();g.fill();}
      for(const k of [.08,.35,.65,.92])antorcha(k*d.W*d.AN,d.PCH+44*d.K,t/1000,d.K);},
      cabeza(P){if(P.gorro)return;g.beginPath();g.arc(0,-59,20,Math.PI,0);g.fillStyle="#9a6f2e";g.fill();caja(-22,-61,44,4,2,"#6d4c1e");for(const s of [-1,1]){g.beginPath();g.moveTo(s*17,-66);g.quadraticCurveTo(s*31,-68,s*30,-82);g.quadraticCurveTo(s*23,-72,s*12,-72);g.closePath();g.fillStyle="#efe4cf";g.fill();}}},
    cronicas_tamriel:{pal:pl("#232a30","#2e373e","#39424a","#4f5a63","#8fb7c9"),pared(d,t){
      g.fillStyle="#2e373e";g.beginPath();g.moveTo(0,d.sue);for(let i=0;i<=12;i++)g.lineTo(i/12*d.W,d.sue-(30+((i*73)%46))*d.K);g.lineTo(d.W,d.sue);g.closePath();g.fill();nieve(d,t,46);},
      cabeza(P){if(P.gorro)return;g.beginPath();g.arc(0,-59,20,Math.PI,0);g.fillStyle="#7f8a93";g.fill();caja(-22,-61,44,4,2,"#596269");for(const s of [-1,1]){g.beginPath();g.moveTo(s*16,-68);g.lineTo(s*27,-90);g.lineTo(s*9,-76);g.closePath();g.fillStyle="#d8d2c2";g.fill();}}},
    runa_caida:{pal:pl("#17140f","#231d14","#2c2418","#4a3c24","#e6c05a"),pared(d,t){
      const x=d.W*d.AN*.5,y=d.PCH+30*d.K,gr=g.createRadialGradient(x,y,4,x,y,150*d.K);gr.addColorStop(0,"rgba(255,206,90,.34)");gr.addColorStop(1,"rgba(255,206,90,0)");g.fillStyle=gr;g.fillRect(0,d.PCH,d.W,d.sue-d.PCH);
      g.strokeStyle="#c9a648";g.lineWidth=2.4;for(let i=-4;i<=4;i++){g.beginPath();g.moveTo(x+i*5*d.K,d.sue);g.quadraticCurveTo(x+i*9*d.K,y+40*d.K,x+i*38*d.K,y-10*d.K);g.stroke();}
      g.fillStyle="#ffd97a";for(let i=0;i<22;i++){const f=(t/7000+i*.137)%1;g.globalAlpha=.8*(1-f);g.beginPath();g.arc((i*.0477%1)*d.W,d.sue-f*(d.sue-d.PCH),1.5,0,7);g.fill();}g.globalAlpha=1;},
      cabeza(P){if(P.gorro)return;g.beginPath();g.moveTo(-24,-30);g.quadraticCurveTo(-26,-70,0,-72);g.quadraticCurveTo(26,-70,24,-30);g.lineTo(18,-30);g.quadraticCurveTo(21,-62,0,-63);g.quadraticCurveTo(-21,-62,-18,-30);g.closePath();g.fillStyle="#6b5a35";g.fill();}},
    cronicas_gaming:{pal:pl("#241a4d","#33256b","#2f2a66","#4b3f9e","#ff5d73"),pared(d,t){
      g.fillStyle="#33256b";for(let x=0;x<d.W;x+=16*d.K)for(let y=d.PCH;y<d.sue;y+=16*d.K)if(((x+y)/(16*d.K))%5<1)g.fillRect(x,y,4,4);
      for(let i=0;i<7;i++){const x=(i+.5)/7*d.W*d.AN,y=d.PCH+22*d.K+Math.sin(t/500+i)*4*d.K,a=Math.abs(Math.cos(t/400+i));elip(x,y,6*d.K*Math.max(.15,a),7*d.K,AMAR);}},
      cabeza(P){if(P.gorro)return;g.beginPath();g.arc(0,-59,18,Math.PI,0);g.fillStyle=ROJO;g.fill();caja(4,-61,24,3.6,1.6,"#c23a4e");circ(0,-68,5,"#fff");letra("★",0,-68,7,ROJO);}},
    pieza_oculta:{pal:pl("#f2c58a","#eab06c","#c98a52","#a86a3c","#e2553d",claro),cuerpo:"#e2653d",pared(d){
      g.strokeStyle="rgba(120,70,30,.16)";g.lineWidth=1.3;for(let i=0;i<7;i++){const x=(i+.5)/7*d.W,y=d.PCH+(i%2?34:60)*d.K;for(let r=4;r<34;r+=5){g.beginPath();g.ellipse(x,y,r*d.K*.8,r*d.K,.3,.2,5.6);g.stroke();}}},
      cabeza(){g.strokeStyle="rgba(90,50,20,.3)";g.lineWidth=.8;for(const r of [6,10]){g.beginPath();g.arc(-9,-33,r,3.4,4.4);g.stroke();}}},
    cronopapel:{pal:pl("#efe6d2","#e4d8bf","#d6c7a8","#a78f6b","#b5532c",claro),filtro:"sepia(.22)",pared(d){
      g.strokeStyle="rgba(90,74,50,.14)";g.lineWidth=1;for(let x=-d.H;x<d.W;x+=11*d.K){g.beginPath();g.moveTo(x,d.sue);g.lineTo(x+(d.sue-d.PCH)*.7,d.PCH);g.stroke();}},
      cabeza(P){if(!P.gorro){g.save();g.translate(18,-60);g.rotate(.6);caja(-2,-13,4,22,1,AMAR);g.beginPath();g.moveTo(-2,9);g.lineTo(2,9);g.lineTo(0,14);g.closePath();g.fillStyle="#3b3226";g.fill();g.restore();}}},
    logia:{pal:pl("#161616","#222222","#2c2c2c","#444444","#bbbbbb",{"--panel":"#1c1c1c"}),filtro:"grayscale(1) contrast(1.12)",pared(d,t){
      g.fillStyle="rgba(255,255,255,.05)";for(let i=0;i<7;i++)g.fillRect(d.W*.12,d.PCH+i*14*d.K,d.W*.26,6*d.K);
      g.strokeStyle="rgba(255,255,255,.2)";g.lineWidth=1;for(let i=0;i<34;i++){const x=(i*71.3+t*.05)%d.W,y=d.PCH+((i*53+t*.5)%(d.sue-d.PCH));g.beginPath();g.moveTo(x,y);g.lineTo(x-3,y+12);g.stroke();}},
      cabeza(P){if(P.gorro)return;caja(-24,-63,48,4,2,"#2a2a2a");caja(-15,-77,30,15,6,"#333333");caja(-15,-67,30,3,0,"#111111");}},
    cuerpo_en_neon:{pal:pl("#050507","#0c0c10","#0a0a0e","#26262c","#ffe600",{"--mut":"#b5b5bb","--faint":"#5c5c64","--panel":"#0f0f13"}),cuerpo:"#16161a",pared(d,t){
      g.strokeStyle="rgba(255,255,255,.5)";g.lineWidth=1.2;for(let i=0;i<5;i++){g.beginPath();g.moveTo(0,d.PCH+(14+i*15)*d.K);for(let x=0;x<=d.W;x+=d.W/28)g.lineTo(x,d.PCH+(14+i*15)*d.K+Math.sin(x/70+i)*5*d.K);g.stroke();}
      const a=.7+.3*Math.sin(t/330);g.shadowColor="#ffe600";g.shadowBlur=18;g.globalAlpha=a;corazon(d.W*d.AN*.5,d.PCH+36*d.K,16*d.K,"#ffe600");g.shadowBlur=0;g.globalAlpha=1;},
      cabeza(P,T){if(!P.gorro){g.shadowColor="#ffe600";g.shadowBlur=9;aro(0,-75,14,"#ffe600",2,0,7);g.shadowBlur=0;}}},
    bitacora_perdida:{pal:pl("#1d2b3a","#25384b","#33465a","#50637a","#e8a33d"),pared(d){
      g.strokeStyle="rgba(232,163,61,.2)";g.lineWidth=1;for(let i=1;i<12;i++){g.beginPath();g.moveTo(i/12*d.W,d.PCH);g.lineTo(i/12*d.W+22*d.K,d.sue);g.stroke();}for(let i=1;i<5;i++){g.beginPath();g.moveTo(0,d.PCH+i*22*d.K);g.quadraticCurveTo(d.W/2,d.PCH+i*16*d.K,d.W,d.PCH+i*22*d.K);g.stroke();}
      const x=d.W*d.AN*.5,y=d.PCH+34*d.K;aro(x,y,17*d.K,"#e8a33d",1.5);raya(x,y-22*d.K,x,y+22*d.K,"#e8a33d",1.2);raya(x-22*d.K,y,x+22*d.K,y,"#e8a33d",1.2);},
      cabeza(P){if(P.gorro)return;elip(0,-60,27,5,"#c9b184");g.beginPath();g.arc(0,-60,16,Math.PI,0);g.fillStyle="#d8c394";g.fill();}},
    kuriox:{pal:pl("#0e1638","#18235a","#222c6e","#3b47a0","#ff7a59"),pared(d,t){
      g.fillStyle="#fff";for(let i=0;i<60;i++){g.globalAlpha=.3+.6*Math.abs(Math.sin(t/900+i));g.fillRect((i*97.3)%d.W,d.PCH+(i*41.7)%(d.sue-d.PCH),1.6,1.6);}g.globalAlpha=1;
      const x=d.W*d.AN*.72,y=d.PCH+34*d.K;circ(x,y,20*d.K,"#ff7a59");elip(x,y,34*d.K,6*d.K,"#ffd166",-.25);circ(x-6*d.K,y-6*d.K,4*d.K,"#ffa98a");},
      cabeza(P){if(!P.gorro){g.globalAlpha=.35;circ(0,-46,29,"#bfe6ff");g.globalAlpha=1;aro(0,-46,29,"#dff3ff",1.6);}}},
    sapiens_con_wifi:{pal:pl("#4a3a2e","#5a4738","#3c2f26","#6d5643","#f2a541"),pared(d){
      g.strokeStyle="#c9713a";g.lineWidth=2.6;g.lineCap="round";for(let i=0;i<5;i++){const x=(i+.5)/5*d.W*d.AN,y=d.PCH+30*d.K,e=d.K;g.beginPath();g.ellipse(x,y,16*e,8*e,0,0,7);g.moveTo(x+14*e,y-4*e);g.lineTo(x+24*e,y-10*e);for(const s of [-9,-4,5,10]){g.moveTo(x+s*e,y+7*e);g.lineTo(x+s*e,y+16*e);}g.stroke();}},
      cabeza(P){if(!P.gorro){g.save();g.translate(0,-64);g.rotate(.35);caja(-13,-2,26,4,2,"#efe4cf");circ(-13,-1,3.4,"#efe4cf");circ(13,1,3.4,"#efe4cf");g.restore();}}},
    wild_next_door:{pal:pl("#20352a","#2a4636","#3a4a2a","#5d6b3a","#a8e05f"),pared(d,t){
      for(let i=0;i<9;i++){const x=(i+.5)/9*d.W,y=d.sue;caja(x-3*d.K,y-48*d.K,6*d.K,48*d.K,1,"#2a2018");circ(x,y-58*d.K,24*d.K,"#2f5a3f");circ(x-14*d.K,y-46*d.K,16*d.K,"#2a4f38");}
      for(let i=0;i<10;i++){const f=(t/9000+i*.1)%1,x=(i*.137%1)*d.W+Math.sin(t/800+i)*14;elip(x,d.PCH+f*(d.sue-d.PCH),3*d.K,1.6*d.K,"#a8e05f",t/700+i);}},
      cabeza(P){if(P.gorro)return;elip(0,-60,28,4.6,"#8a6a3a");g.beginPath();g.moveTo(-15,-60);g.lineTo(-10,-74);g.lineTo(10,-74);g.lineTo(15,-60);g.closePath();g.fillStyle="#a07c46";g.fill();caja(-15,-64,30,3,0,"#5b4326");}},
    gaia_eterna:{pal:pl("#1c2e35","#244049","#2a3a38","#40625f","#7fd8be"),pared(d,t){
      for(let i=0;i<4;i++){g.globalAlpha=.16;g.strokeStyle=["#7fd8be","#b388ff","#5bc0ff","#7fd8be"][i];g.lineWidth=16*d.K;g.beginPath();g.moveTo(0,d.PCH+(18+i*12)*d.K);for(let x=0;x<=d.W;x+=d.W/24)g.lineTo(x,d.PCH+(18+i*12)*d.K+Math.sin(x/120+t/1700+i)*9*d.K);g.stroke();}g.globalAlpha=1;},
      cabeza(P){if(P.gorro)return;g.beginPath();g.moveTo(-23,-34);g.quadraticCurveTo(-24,-72,1,-74);g.quadraticCurveTo(25,-72,23,-34);g.lineTo(18,-34);g.quadraticCurveTo(20,-63,0,-64);g.quadraticCurveTo(-20,-63,-18,-34);g.closePath();g.fillStyle="#2f6b5e";g.fill();elip(10,-71,6,3,VERDE,-.5);}},
  };
  const ALIAS={cronicas_de_warcraft:"cronicas_warcraft",cronicas_de_tamriel:"cronicas_tamriel"};
  const tema=()=>TEMAS[M.canal];
  function ponCanal(alias){
    alias=M.forzado||Q.get("canal")||ALIAS[alias]||alias||"";
    if(alias===M.canal)return;
    M.canal=alias;const t=TEMAS[alias];
    Taller.tema(t?t.pal:null);
    $("taller").style.filter=t?.filtro||"";
  }

  // ---- la fiesta del día: sale sola por fecha
  const fiesta=()=>{
    const q=Q.get("fiesta");if(q!=null)return q;
    const f=new Date(),m=f.getMonth()+1,n=f.getDate();
    return (m===10&&n>=28)||(m===11&&n<=3)?"muertos":(m===12&&n>=12)||(m===1&&n<=6)?"navidad":"";
  };
  const flor=(x,y,r)=>{for(let i=0;i<7;i++)circ(x+Math.cos(i*.9)*r*.62,y+Math.sin(i*.9)*r*.62,r*.5,i%2?CEMPA:CEMPA2);circ(x,y,r*.42,"#e87a10");};
  function papelPicado(d,t){
    const n=Math.max(6,Math.round(d.W/(52*d.K))),w=d.W/n,y=d.PCH+2,col=[ROSA,CEMPA,LILA,VERDE,AZUL,ROJO];
    g.strokeStyle=d.pal["--mut"];g.lineWidth=1;g.beginPath();g.moveTo(0,y);for(let i=0;i<=n;i++)g.quadraticCurveTo(i*w-w/2,y+5*d.K,i*w,y);g.stroke();
    for(let i=0;i<n;i++){
      const x=i*w+w*.1,fw=w*.8,fh=19*d.K,ox=Math.sin(t/900+i)*2*d.K,hy=y+3*d.K;
      g.beginPath();g.moveTo(x,hy);g.lineTo(x+fw,hy);g.lineTo(x+fw+ox,hy+fh);
      for(let k=5;k>0;k--){const a=x+ox+fw*k/5,b=x+ox+fw*(k-.5)/5;g.quadraticCurveTo(b,hy+fh+4*d.K,a-fw/5,hy+fh);}
      g.closePath();g.fillStyle=col[i%6];g.globalAlpha=.92;g.fill();g.globalAlpha=1;
      g.fillStyle=d.pal["--muro"];const cx=x+fw/2+ox/2,cy=hy+fh*.48;      // el calado: una calavera recortada
      circ(cx,cy,fh*.2,d.pal["--muro"]);caja(cx-fh*.1,cy+fh*.13,fh*.2,fh*.11,1,d.pal["--muro"]);
      for(const s of [-1,1]){circ(cx+s*fw*.32,cy,fh*.07,d.pal["--muro"]);circ(cx+s*fw*.32,cy-fh*.24,fh*.05,d.pal["--muro"]);}
      circ(cx-fh*.07,cy-fh*.02,fh*.05,col[i%6]);circ(cx+fh*.07,cy-fh*.02,fh*.05,col[i%6]);
    }
  }
  function ofrenda(d,t,x,y,w,h){         // cada foto es un video que se retiró de verdad; las velas parpadean, el resto no finge nada
    const pisos=[[0,1],[.12,.76],[.25,.5]],ph=h/3.1;
    pisos.forEach(([m,a],i)=>{const by=y+h-ph*i-ph*.3;caja(x+w*m,by,w*a,ph*.3,1.5,i%2?"#8a2f6a":"#c2317a");caja(x+w*m,by,w*a,3,1,"#f7d6e6");});
    const items=M.mundo?.ofrenda||[];const cx=x+w/2,top=y+h-ph*2-ph*.3;
    const fw=ph*1.15,fh=ph*.85;items.slice(0,3).forEach((o,i)=>{
      const px=cx+(i-(Math.min(items.length,3)-1)/2)*(fw+3)-fw/2,py=top-fh;
      caja(px-1.5,py-1.5,fw+3,fh+3,1,"#3b2a18");caja(px,py,fw,fh,1,"#20150c");
      const im=img(url(o.video,o.rel,200));if(im)cubre(im,px,py,fw,fh);else letra("🕯",px+fw/2,py+fh/2,fh*.6,CEMPA2);
      M.boton["of"+i]={x:px,y:py,w:fw,h:fh,txt:`En memoria de «${o.titulo}»`};
    });
    for(let i=0;i<5;i++){               // velas y flores en los pisos
      const px=x+w*(.08+i*.21),py=y+h-ph*.3;
      if(i%2){caja(px-1.6,py-9*d.K,3.2,9*d.K,.5,"#f6efe0");const f=Math.sin(t/120+i*2)*.6;elip(px+f,py-11.5*d.K,1.8,3.4,CEMPA2);}
      else flor(px,py-3.4*d.K,4.2*d.K);
    }
    const lx=x+w*.84;flor(lx,top-1,3.6*d.K);flor(x+w*.16,top-1,3.6*d.K);
    circ(x+w*.5,y+h-ph*.3-5*d.K,4.2*d.K,"#c9853a");raya(x+w*.46,y+h-ph*.3-6*d.K,x+w*.54,y+h-ph*.3-6*d.K,"#a56a2a",1.2);    // pan de muerto
  }
  function suelosMuertos(d,t){
    for(let x=14*d.K;x<d.W*d.AN;x+=44*d.K){flor(x,d.sue+11*d.K,4.4*d.K);if(d.W>700)flor(x+15*d.K,d.sue+16*d.K,3*d.K);}
    for(let i=0;i<12;i++){const f=(t/8000+i*.083)%1;g.globalAlpha=.75*(1-f*.6);elip((i*.0837%1)*d.W*d.AN+Math.sin(t/900+i)*18,d.PCH+f*(d.sue-d.PCH),2.6*d.K,1.3*d.K,CEMPA,t/500+i);}
    g.globalAlpha=1;
  }

  // ---- la pared: ventana con la hora real, radio, trofeos, noticiero y buzón
  function ventana(d,t,x,y,w,h){
    const f=new Date(),hr=f.getHours()+f.getMinutes()/60,dia=hr>=6&&hr<20,k=(hr-6)/14;
    const c=!dia?["#0b1030","#1b2350"]:hr<8?["#f5a25d","#7aa7d9"]:hr<18?["#6bb8f0","#cfeaff"]:["#ff8a5c","#4b3a7a"];
    g.save();camino(x,y,w,h,3);g.clip();
    const gr=g.createLinearGradient(0,y,0,y+h);gr.addColorStop(0,c[1]);gr.addColorStop(1,c[0]);g.fillStyle=gr;g.fillRect(x,y,w,h);
    if(dia)circ(x+w*k,y+h*(.85-Math.sin(k*Math.PI)*.62),h*.15,"#fff3a8");
    else{circ(x+w*.68,y+h*.3,h*.13,"#eef2ff");circ(x+w*.73,y+h*.26,h*.11,c[1]);g.fillStyle="#fff";for(let i=0;i<9;i++)g.fillRect(x+(i*.37%1)*w,y+(i*.23%.7)*h,1.2,1.2);}
    if(M.clima>=1){for(let i=0;i<3;i++){const nx=x+((t/9000+i*.37)%1.3-.15)*w;elip(nx,y+h*.24,w*.2,h*.13,M.clima>=3?"#7b8296":"#e8ecf5");}}
    if(M.clima>=3){g.strokeStyle="#bcd4ff";g.lineWidth=1;for(let i=0;i<14;i++){const px=x+(i*.173+t/1600)%1*w,py=y+(i*.29+t/500)%1*h;g.beginPath();g.moveTo(px,py);g.lineTo(px-1.5,py+5);g.stroke();}}
    g.restore();
    marco(x,y,w,h,3,MADERA,3);raya(x+w/2,y,x+w/2,y+h,MADERA,2);raya(x,y+h/2,x+w,y+h/2,MADERA,2);
  }
  const FMT=n=>n>=1e6?(n/1e6).toFixed(1).replace(".0","")+" M":n>=1e3?(n/1e3).toFixed(n>=1e4?0:1).replace(".0","")+" mil":String(n);
  function trofeos(d,t,x0,x1,y,h){
    const lista=(M.mundo?.trofeos||[]).filter(o=>!o.short),w=h*16/9,paso=w+9*d.K,n=Math.min(lista.length,Math.floor((x1-x0)/paso));
    for(let i=0;i<n;i++){
      const o=lista[i],x=x1-(i+1)*paso,im=img(url(o.video,o.rel,240));
      caja(x-2,y-2,w+4,h+4,2,MADERA);caja(x,y,w,h,1,"#20242f");
      if(im)cubre(im,x,y,w,h);else letra("🎬",x+w/2,y+h/2,h*.5,AMAR);
      const et=o.programado?`📅 ${o.programado}`:o.vistas!=null?`▶ ${FMT(o.vistas)}`:"";
      if(et){g.font=`650 ${Math.max(8.5,7.5*d.K)}px "Segoe UI",sans-serif`;const tw=g.measureText(et).width+7;caja(x+w-tw-1,y+h-Math.max(12,10*d.K)-1,tw,Math.max(12,10*d.K),2,"rgba(0,0,0,.76)");g.fillStyle="#fff";g.textAlign="left";g.textBaseline="middle";g.fillText(et,x+w-tw+2.5,y+h-Math.max(12,10*d.K)/2-.5);g.textBaseline="alphabetic";}
      M.boton["tr"+i]={x,y,w,h,txt:`«${o.titulo}»${o.programado?` · se estrena el ${o.programado}`:o.vistas!=null?` · ${FMT(o.vistas)} vistas`:""}`};
    }
  }
  function tele(d,t,x,y,w,h){
    const nv=M.mundo?.noticias||[];if(!nv.length)return;
    caja(x,y,w,h,3,"#10131c");marco(x,y,w,h,3,"#3a4256",1.5);
    caja(x+2,y+2,w-4,Math.max(10,8.5*d.K),2,ROJO);
    g.fillStyle="#fff";g.font=`800 ${Math.max(7.5,6.5*d.K)}px "Segoe UI",sans-serif`;g.textAlign="left";g.textBaseline="middle";g.fillText("NOTICIAS",x+6,y+2+Math.max(10,8.5*d.K)/2);
    const txt=nv[Math.floor(t/9000)%nv.length];
    g.font=`600 ${Math.max(10,9*d.K)}px "Segoe UI",sans-serif`;
    const av=g.measureText(txt).width,iz=x+6,an=w-12,f=(t%9000)/9000,yy=y+h*.66;
    g.save();camino(iz,y,an,h,1);g.clip();g.fillStyle="#e8ecf6";g.fillText(txt,av<=an?iz:iz+an-(av+an)*f+an*.0,yy);g.restore();g.textBaseline="alphabetic";
  }
  function radio(d,t,x,y,e){
    const son=M.sonando&&!M.sonando.paused;
    caja(x-13*e,y-16*e,26*e,16*e,3,"#6a4a2e");marco(x-13*e,y-16*e,26*e,16*e,3,"#3b2a18",1);
    circ(x-5*e,y-8*e,4.5*e,"#2a2018");for(let i=0;i<3;i++)raya(x+3*e,y-12*e+i*4*e,x+10*e,y-12*e+i*4*e,"#d7c29a",1);
    raya(x+9*e,y-16*e,x+15*e,y-28*e,"#aeb4c4",1.3);
    if(son){for(let i=0;i<3;i++){const f=(t/900+i/3)%1;g.globalAlpha=1-f;letra("♪",x-9*e+i*7*e,y-20*e-f*22*e,9*e,AMAR);}g.globalAlpha=1;}
    M.boton.radio={x:x-14*e,y:y-30*e,w:30*e,h:32*e,radio:true};
  }
  function buzon(d,t,x,y,e){
    const n=(M.mundo?.comentarios||[]).length;if(!n)return;
    caja(x-1.5*e,y+13*e,3*e,16*e,1,"#5b4330");
    caja(x-13*e,y,26*e,14*e,6*e,"#4f7fa8");marco(x-13*e,y,26*e,14*e,6*e,"#2c4a63",1.2);
    caja(x+10*e,y-3*e,2.4*e,10*e,1,ROJO);caja(x+10*e,y-3*e,7*e,5*e,1,ROJO);
    raya(x-9*e,y+5*e,x+6*e,y+5*e,"#2c4a63",1.4);
    M.boton.buzon={x:x-16*e,y:y-5*e,w:34*e,h:36*e,buzon:true};
  }
  function banda(d,t){                   // la banda lleva lo que de verdad se ha producido
    const v=M.video,lista=(M.mundo?.piezas||[]);
    Cap.sinCajas=lista.length>0;
    if(!lista.length)return;
    const h=Math.max(10,Math.min(24*d.K,d.by-d.sue-19*d.K)),w=h*1.5,paso=w*1.9,total=lista.length*paso;
    lista.forEach((r,i)=>{
      const x=((t*.03+i*paso)%Math.max(total,d.W+paso))-paso;
      if(x>d.W||x<-w)return;
      const im=img(url(v,r,160));
      caja(x-1.5,d.by-h-1.5,w+3,h+3,2,"#fff");
      if(im)cubre(im,x,d.by-h,w,h);else caja(x,d.by-h,w,h,1,d.pal["--acc"]);
    });
  }
  function pared(t){
    const d=D();M.boton={};
    const T=tema();if(T?.pared)T.pared(d,t);
    const fi=fiesta();
    const y=d.PCH+(fi==="muertos"?25:6)*d.K,h=Math.min(27*d.K,(d.sue-d.PCH)*.32),vw=h*1.25;
    let x=d.m;
    ventana(d,t,x,y,vw,h);x+=vw+10*d.K;
    radio(d,t,x+12*d.K,y+h,Math.min(1.25,d.K*.8));x+=30*d.K;
    if(fi==="muertos"&&d.W>=700){const w=88*d.K,oy=d.PCH+22*d.K;ofrenda(d,t,x,oy,w,(d.sue-oy)*.72);x+=w+8*d.K;}
    if(d.W>=900){
      const tw=Math.min(190*d.K,d.W*.17),fin=d.W*d.AN-34*d.K;
      tele(d,t,fin-tw,y,tw,h);
      buzon(d,t,fin+16*d.K,y,Math.min(1.2,d.K*.8));
      trofeos(d,t,x,fin-tw-6*d.K,y,h);
    }
    if(fi==="muertos")papelPicado(d,t);
    if(fi==="navidad"){nieve(d,t,40);for(let i=0;i<24;i++)circ((i+.5)/24*d.W,d.PCH+6*d.K+Math.sin(i*1.4)*3*d.K,2.4*d.K,COLORES[i%6]+(Math.floor(t/500+i)%2?"ff":"66"));}
    banda(d,t);
  }

  // ---- bichos y el jefe del render: sus vidas son datos reales
  const bichos=[];let vencidos=0;
  const Bo={vivo:false,p:0,muere:0,et:""};
  function nuevoBug(){
    const b=bichos.find(x=>!x.muere);
    if(b){b.n=Math.min(5,b.n+1);return b;}
    bichos.push({x:D().AN*.98,n:1,muere:0,fase:Math.random()*6});
  }
  function vence(){
    const b=bichos.find(x=>!x.muere);if(!b)return;
    b.muere=D().ahora;vencidos++;anuncia(b.n>1?`¡Bug vencido al ${b.n}.º intento!`:"¡Bug vencido!",VERDE);
    Son_(()=>Son.accion("fiesta"));
  }
  function dibujaBug(d,b,t){
    const e=d.K*(1+(b.n-1)*.3),x=b.x*d.W,y=d.sue+3*d.K,pat=Math.sin(t/70+b.fase)*2*e,muere=b.muere?(t-b.muere)/700:0;
    if(muere>=1)return;
    g.save();g.translate(x,y);g.scale(1+muere*1.6,1-muere);g.globalAlpha=1-muere;
    for(const s of [-8,0,8]){raya(s*e,-5*e,(s-3)*e+pat*(s%2?1:-1),2*e,TINTA,1.8*e);raya(s*e,-5*e,(s+3)*e-pat,2*e,TINTA,1.8*e);}
    elip(0,-8*e,13*e,8.5*e,ROJO);raya(0,-16*e,0,-.5*e,"#a02a3c",1.5*e);
    circ(-12*e,-11*e,6*e,"#a02a3c");circ(-14*e,-13*e,1.8*e,"#fff");circ(-10*e,-13*e,1.8*e,"#fff");circ(-14.4*e,-12.6*e,.9*e,TINTA);circ(-10.4*e,-12.6*e,.9*e,TINTA);
    raya(-14*e,-16*e,-19*e,-22*e,TINTA,1.2*e);raya(-10*e,-16*e,-7*e,-23*e,TINTA,1.2*e);
    g.restore();
    if(!b.muere&&b.n>1)letra(`×${b.n}`,x,y-26*e,10*d.K,ROJO);
  }
  function dibujaJefe(d,t){
    const muerto=Bo.muere?(t-Bo.muere)/1400:0;
    if((!Bo.vivo&&!Bo.muere)||muerto>=1)return;
    const e=d.K*.95,x=d.W*d.AN*.74,y=d.PCH+70*d.K+Math.sin(t/620)*3*d.K,hp=Math.max(0,100-Bo.p);
    g.save();g.translate(x,y);g.rotate(muerto*1.5);g.scale(1+muerto,1+muerto);g.globalAlpha=1-muerto;
    g.save();g.rotate(t/1400);g.fillStyle="#5c6478";for(let i=0;i<10;i++){g.rotate(.628);g.fillRect(-4*e,-29*e,8*e,8*e);}g.restore();
    circ(0,0,23*e,"#6f7892");aro(0,0,23*e,TINTA,1.6*e);
    for(const s of [-1,1]){circ(s*8*e,-3*e,4.2*e,"#fff");circ(s*7*e,-2*e,2*e,ROJO);raya(s*13*e,-11*e,s*3*e,-7*e,TINTA,2.6*e);}
    g.beginPath();g.moveTo(-11*e,9*e);for(let i=0;i<7;i++)g.lineTo(-11*e+i*3.66*e,(i%2?13:8)*e);g.strokeStyle=TINTA;g.lineWidth=2*e;g.stroke();
    g.restore();
    if(!Bo.muere){
      const bw=62*d.K,bh=Math.max(6,5*d.K),bx=x-bw/2,by=y-40*d.K;
      caja(bx,by,bw,bh,2,"#2a2f3f");caja(bx+1,by+1,(bw-2)*hp/100,bh-2,1.5,hp>50?VERDE:hp>20?AMAR:ROJO);
      g.font=`700 ${Math.max(9,8*d.K)}px "Segoe UI",sans-serif`;g.textAlign="center";g.fillStyle=d.pal["--txt"];g.fillText(`Jefe Render · falta ${Math.round(hp)} %`,x,by-3);
    }else if(muerto<.5)for(let i=0;i<8;i++)letra("✦",x+Math.cos(i*.79)*muerto*150*d.K,y+Math.sin(i*.79)*muerto*150*d.K,12*d.K,AMAR);
  }
  function medio(t,dt){
    const d=D();
    dibujaJefe(d,t);
    for(let i=bichos.length-1;i>=0;i--){
      const b=bichos[i];
      if(b.muere&&t-b.muere>800){bichos.splice(i,1);continue;}
      if(!b.muere){const m=d.robotX+.075;if(b.x>m)b.x-=dt*.000085;}
      dibujaBug(d,b,t);
    }
  }

  // ---- lo que va encima: anuncios, confeti, el Jefe, la carta y el relevo
  const avisos=[];let confeti=[];
  function anuncia(txt,c=AMAR,ms=3400){avisos.push({txt,c,ms,ini:0});}
  function lluvia(n=70){const d=D();for(let i=0;i<n;i++)confeti.push({x:Math.random()*d.W,y:d.PCH-Math.random()*60,vy:50+Math.random()*90,vx:(Math.random()-.5)*40,r:Math.random()*6,c:COLORES[i%6],v:1});}
  function dibujaAviso(d,t){
    const a=avisos[0];if(!a)return;
    if(!a.ini)a.ini=t;
    const f=(t-a.ini)/a.ms;if(f>=1){avisos.shift();return;}
    const e=Math.min(1,f*9),s=Math.min(1,(1-f)*9);
    g.font=`800 ${Math.max(14,14*d.K)}px "Segoe UI",system-ui,sans-serif`;
    const w=g.measureText(a.txt).width+34,h=Math.max(32,26*d.K),x=d.W*d.AN/2-w/2,y=d.PCH+(J.ini?84:6)*d.K+(1-e)*-30;
    g.globalAlpha=Math.min(e,s);caja(x,y,w,h,h/2,TINTA);marco(x,y,w,h,h/2,a.c,2.2);
    g.fillStyle=a.c;g.textAlign="center";g.textBaseline="middle";g.fillText(a.txt,x+w/2,y+h/2+1);g.textBaseline="alphabetic";g.globalAlpha=1;
  }
  const J={ini:0,txt:""};
  function dibujaJefeHumano(d,t){        // el usuario: baja una pantalla colgada con su sombrero y lo que escribió
    if(!J.ini)return;
    const s=(t-J.ini)/1000,dur=7;if(s>dur){J.ini=0;return;}
    const k=Math.min(1,s*3,(dur-s)*3),w=Math.min(300*d.K,d.W*.7),h=70*d.K,x=d.W*d.AN/2-w/2,y=d.PCH-h+(h+8*d.K)*k;
    raya(x+24,d.PCH,x+24,y,d.pal["--mut"],2);raya(x+w-24,d.PCH,x+w-24,y,d.pal["--mut"],2);
    caja(x,y,w,h,8,"#10131c");marco(x,y,w,h,8,AMAR,2);
    const cx=x+h*.5,cy=y+h*.58,b=Math.sin(t/90)>.1?1:.3;
    circ(cx,cy,h*.2,"#e9c7a4");elip(cx,cy-h*.17,h*.42,h*.08,"#7a5a3e");caja(cx-h*.19,cy-h*.36,h*.38,h*.2,h*.08,"#8d6a4a");
    for(const s2 of [-1,1])circ(cx+s2*h*.08,cy-h*.02,h*.022,TINTA);
    elip(cx,cy+h*.09,h*.06,h*.02+h*.03*b,"#b0413e");
    g.font=`700 ${Math.max(9,8.5*d.K)}px "Segoe UI",sans-serif`;g.fillStyle=AMAR;g.textAlign="left";g.fillText("EL JEFE DICE",x+h,y+15*d.K);
    g.font=`500 ${Math.max(10.5,10*d.K)}px "Segoe UI",sans-serif`;g.fillStyle="#f0f2f8";
    lineas(J.txt,w-h-12,3).forEach((l,i)=>g.fillText(l,x+h,y+(30+i*14)*d.K));
  }
  let tocT=-1e9;
  function dibujaPregunta(d,t){          // te está esperando: toca el vidrio
    if(!M.preg||ahoraS()-M.pregT>7200)return;
    const x=d.robotX*d.W+34*d.K,y=d.sue-62*d.K,go=Math.floor(t/340)%3;
    circ(x+(go===0?-3:0)*d.K,y,7*d.K,"#f5f7ff");aro(x+(go===0?-3:0)*d.K,y,7*d.K,TINTA,1.3);
    if(go===0){letra("toc",x+18*d.K,y-12*d.K,11*d.K,AMAR);letra("toc",x+30*d.K,y+2*d.K,9*d.K,AMAR);}
    pastilla(`🔔 Te espero: ${M.preg}`,d.W*d.AN/2,d.PCH+5*d.K,d,AMAR);
    if(t-tocT>30000){tocT=t;Son_(()=>Son.rx("pcFan"));}
  }
  const C={ini:0,c:null};
  function dibujaCarta(d,t){
    if(!C.ini)return;
    const s=(t-C.ini)/1000,dur=8.5;if(s>dur){C.ini=0;return;}
    const k=Math.min(1,s*2.5,(dur-s)*3),w=Math.min(330*d.K,d.W*.78),h=78*d.K,x=d.W*d.AN/2-w/2,y=d.sue-h-8*d.K+(1-k)*60*d.K;
    g.globalAlpha=k;g.save();g.translate(x+w/2,y+h/2);g.rotate(-.012);g.translate(-x-w/2,-y-h/2);
    caja(x,y,w,h,3,"#fff8e6");marco(x,y,w,h,3,"#c9b184",1.2);
    g.fillStyle="#6b5a48";g.textAlign="left";g.font=`700 ${Math.max(9,8.5*d.K)}px "Segoe UI",sans-serif`;
    g.fillText(`${C.c.autor}${C.c.likes?`  ♥ ${C.c.likes}`:""}`,x+12,y+15*d.K);
    g.font=`500 ${Math.max(10.5,10*d.K)}px "Segoe UI",sans-serif`;g.fillStyle="#2c2418";
    lineas(C.c.texto,w-24,3).forEach((l,i)=>g.fillText(l,x+12,y+(31+i*14)*d.K));
    g.font=`500 ${Math.max(8,7.5*d.K)}px "Segoe UI",sans-serif`;g.fillStyle="#8a7a62";g.fillText(`en «${C.c.video}»`,x+12,y+h-5);
    g.restore();g.globalAlpha=1;
    if(C.c.likes&&s<dur-1&&Math.random()<.05)Taller.suelta(x+w-18,y+h-10,"♥",ROSA,-40);
  }
  function leeCarta(forzar){
    const l=M.mundo?.comentarios||[];if(!l.length||C.ini)return false;
    const i=(M.nCarta=(M.nCarta||0)+1);C.c=l[i%l.length];C.ini=D().ahora;
    if(Taller.libre()||forzar)Taller.actividad(C.c.queja?"lupa":"leer",C.c.queja?"Revisa una queja del público":"Lee un comentario del público",8000);
    return true;
  }
  const R={ini:0,dur:7200};
  function relevo(){if(!R.ini){R.ini=D().ahora;Cap.oculto=true;}}
  function dibujaRelevo(d,t){
    if(!R.ini)return;
    const s=(t-R.ini)/1000,T=t/1000;
    if(s>7.2){R.ini=0;Cap.oculto=false;anuncia("Sesión nueva: sigue donde se quedó",VERDE);return;}
    const y=d.sue+3*d.K,xa=(s<4.6?.42:.42-(s-4.6)*.16)*d.W*d.AN,xb=(s<1.6?1.05:s<3?1.05-(s-1.6)/1.4*.49:.56)*d.W*d.AN,cb=COLORES[hash(S.sesion)%6];
    const rob=(x,c,yo)=>{g.fillStyle="rgba(0,0,0,.2)";g.beginPath();g.ellipse(x,d.sue+4*d.K,17*d.K,4*d.K,0,0,7);g.fill();g.save();g.translate(x,y);g.scale(d.K*(yo?1:-1),d.K);
      figura({cuerpo:c,cara:s>3&&s<4.6?"feliz":"normal",pies:[Math.sin(T*9)*4,-Math.sin(T*9)*4],brD:s<3?[24,-30]:[22,-34]},T);g.restore();};
    if(xa>-40)rob(xa,Cap.cuerpoR||d.pal["--acc"],true);
    rob(xb,cb,false);
    const cx=d.W*d.AN*.49,cy=d.sue-2*d.K;                  // la caja con lo que se lleva la siguiente
    caja(cx-16*d.K,cy-18*d.K,32*d.K,22*d.K,2,"#a97a4f");marco(cx-16*d.K,cy-18*d.K,32*d.K,22*d.K,2,"#7f5a38",1.2);
    letra("ESTADO.md",cx,cy-7*d.K,6.5*d.K,"#fff");
    const p=Math.max(0,Math.min(1,(s-2.8)/1.2)),bx=xa+24*d.K+(xb-24*d.K-xa-24*d.K)*p,by=y-33*d.K-Math.sin(p*Math.PI)*34*d.K;
    g.save();g.translate(bx,by);g.rotate(p*Math.PI*3);caja(-11*d.K,-2.2*d.K,22*d.K,4.4*d.K,2,AMAR);g.restore();
    pastilla(s<2.8?"Guarda todo en ESTADO.md":s<4.6?"¡Relevo!":"Hasta aquí llegó esta sesión",d.W*d.AN/2,d.sue-96*d.K,d,AMAR);
  }
  function hud(d,t){                     // la batería del contexto: arriba de 180 mil de trabajo toca relevo
    const c=M.ctx;if(!c||d.W<520)return;
    const f=Math.min(1.25,c.trabajo/c.umbral),w=Math.max(66,58*d.K),h=Math.max(13,11*d.K),x=d.W*d.AN-w-10,y=d.by-h-6;
    caja(x,y,w,h,3,"#10131c");marco(x,y,w,h,3,d.pal["--faint"],1);caja(x+w,y+h*.28,3,h*.44,1,d.pal["--faint"]);
    caja(x+1.5,y+1.5,(w-3)*Math.min(1,f),h-3,2,f<.7?VERDE:f<.9?AMAR:ROJO);
    g.font=`700 ${Math.max(8.5,7.5*d.K)}px "Segoe UI",sans-serif`;g.fillStyle="#fff";g.textAlign="center";g.textBaseline="middle";g.fillText(`${Math.round(c.trabajo/1000)} / ${Math.round(c.umbral/1000)} mil`,x+w/2,y+h/2+.5);g.textBaseline="alphabetic";
    if(f>=.8&&Math.floor(t/1400)!==M.gota){M.gota=Math.floor(t/1400);Taller.suelta(d.robotX*d.W+14*d.K,d.sue-58*d.K,"💧",AZUL,-12);}
  }
  function encima(t,dt){
    const d=D();
    if(M.flash&&t<M.flash){g.fillStyle=`rgba(230,240,255,${(M.flash-t)/900*.28})`;g.fillRect(0,d.PCH,d.W,d.H-d.PCH);}
    dibujaRelevo(d,t);dibujaJefeHumano(d,t);dibujaCarta(d,t);dibujaPregunta(d,t);hud(d,t);dibujaAviso(d,t);
    confeti=confeti.filter(c=>c.y<d.H&&c.v>0);
    for(const c of confeti){c.y+=c.vy*dt/1000;c.x+=c.vx*dt/1000;c.r+=dt*.008;g.save();g.translate(c.x,c.y);g.rotate(c.r);g.fillStyle=c.c;g.fillRect(-3.5,-2,7,4);g.restore();}
    if(Date.now()>(M.cartaEn||0)&&!C.ini&&!R.ini&&Taller.libre()&&(M.mundo?.comentarios||[]).length){M.cartaEn=Date.now()+75000+Math.random()*30000;if(M.cartaYa)leeCarta();M.cartaYa=true;}
  }

  // ---- lo que lleva puesto: el traje del nivel, el del canal y el de la fiesta
  const dorado=()=>Q.get("dorado")!=null||(S.sesion&&hash(S.sesion)%64===0);
  Cap.atras=(P,T)=>{
    if(M.nivel>=6){g.beginPath();g.moveTo(-12,-31);g.quadraticCurveTo(-26+Math.sin(T*3)*3,-10,-20,-2);g.lineTo(20,-2);g.quadraticCurveTo(26-Math.sin(T*3)*3,-10,12,-31);g.closePath();g.fillStyle=M.nivel>=10?"#7a1f6b":"#2f6bff";g.fill();}
    if(dorado()||M.nivel>=15)for(let i=0;i<4;i++){const f=(T*.5+i*.25)%1;letra("✦",Math.sin(i*2.3+T)*30,-16-f*62,7,AMAR);}
  };
  Cap.cuerpo=(P,T)=>{
    tema()?.cuerpo2?.(P,T);
    if(M.nivel>=3&&!P.gorro){caja(-14,-33,28,5,2.5,ROJO);caja(5,-30,6,12,2,ROJO);}
  };
  Cap.cabeza=(P,T)=>{
    const fi=fiesta();
    if(fi==="muertos"){                  // catrina: corona de cempasúchil y dientes cosidos
      for(let i=-3;i<=3;i++)flor(i*5.7,-61+Math.abs(i)*1.2,4.2);
      for(let i=-2;i<=2;i++)raya(i*2.4,-37,i*2.4,-32.5,TINTA,.9);
      raya(-7,-34.7,7,-34.7,TINTA,1);
      return;
    }
    if(fi==="navidad"&&!P.gorro){g.beginPath();g.moveTo(-18,-60);g.quadraticCurveTo(2,-84,24,-68);g.lineTo(16,-60);g.closePath();g.fillStyle=ROJO;g.fill();caja(-20,-62,40,5,2.5,"#fff");circ(25,-67,3,"#fff");return;}
    if(tema()?.cabeza)return tema().cabeza(P,T);
    if(M.nivel>=10&&!P.gorro){g.beginPath();g.moveTo(-13,-60);g.lineTo(-13,-71);g.lineTo(-6,-65);g.lineTo(0,-73);g.lineTo(6,-65);g.lineTo(13,-71);g.lineTo(13,-60);g.closePath();g.fillStyle=AMAR;g.fill();circ(0,-66,1.6,ROJO);}
  };
  Cap.fondo=pared;Cap.medio=medio;Cap.encima=encima;
  Cap.clic=(x,y)=>{
    for(const b of Object.values(M.boton)){
      if(x<b.x||x>b.x+b.w||y<b.y||y>b.y+b.h)continue;
      if(b.radio)tocaVoz(true);
      else if(b.buzon)leeCarta(true);
      else Taller.actividad("leer",b.txt,5000);
      return true;
    }
    return false;
  };

  // ---- la radio: un trozo real de la voz del video
  function tocaVoz(forzar){
    const l=M.mundo?.voz||[];if(!l.length||!M.video)return;
    if(!forzar&&!$("chkSon").checked)return;
    try{if(M.sonando)M.sonando.pause();}catch(e){}
    const r=l[Math.floor(Math.random()*l.length)],a=new Audio(`/v2/oir/${encodeURIComponent(M.video)}/${r.split("/").map(encodeURIComponent).join("/")}`);
    a.volume=.8;a.play().catch(()=>{});M.sonando=a;setTimeout(()=>a.pause(),9000);
  }

  // ---- la lotería de la sesión: nueve cartas, cada una se marca con un evento real
  const CARTAS=[["🎬","El Render",e=>e.en==="render"&&e.tipo==="comando"],["🎙","El Micrófono",e=>e.en==="voz"],["🎛","La Bocina",e=>e.en==="sonido"],["🎨","El Pincel",e=>e.en==="imagenes"],["🎞","La Claqueta",e=>e.en==="clips"],
    ["🚀","El Cohete",e=>e.en==="subida"],["🐛","El Bicho",e=>e.fallo],["🤖","El Mini",e=>e.tipo==="ayudante"||!!e.de],["🌍","El Mundo",e=>e.tipo==="busqueda"],["📖","El Libro",e=>e.tipo==="pagina"],["🔍","La Lupa",e=>e.tipo==="imagen"],
    ["✎","El Lápiz",e=>e.tipo==="codigo"],["❯","La Terminal",e=>e.tipo==="comando"],["🔦","La Linterna",e=>e.tipo==="buscar"],["🏁","La Bandera",e=>e.tipo==="cierre"],["🧑","El Jefe",e=>e.tipo==="usuario"],["🌐","El Navegador",e=>e.tipo==="navegador"],["🏃","La Estafeta",e=>e.tipo==="relevo"]];
  const LINEAS=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  function carton(ses){
    const b=CARTAS.map((c,i)=>i);let h=hash(ses);
    for(let i=b.length-1;i>0;i--){h=(h*1103515245+12345)>>>0;const j=h%(i+1);[b[i],b[j]]=[b[j],b[i]];}
    return b.slice(0,9).map(i=>CARTAS[i]);
  }
  let cartonDe="",cart=[],marcas="";
  function pintaLoteria(){
    if(!S.sesion)return;
    if(cartonDe!==S.sesion){cartonDe=S.sesion;cart=carton(S.sesion);marcas="";}
    const on=cart.map(c=>S.ev.some(c[2]));
    const firma=on.map(Number).join("");if(firma===marcas)return;
    const nuevaCarga=!marcas;marcas=firma;
    const gana=LINEAS.filter(l=>l.every(i=>on[i]));
    $("lotCartas").innerHTML=cart.map((c,i)=>`<div class="lc ${on[i]?"on":""} ${gana.some(l=>l.includes(i))?"gana":""}" title="${esc(c[1])}"><i>${c[0]}</i><span>${esc(c[1])}</span></div>`).join("");
    const k=`vivo_lot_${S.sesion}`,ya=+(lee(k)||0);
    if(gana.length>ya){guarda(k,gana.length);if(!nuevaCarga){anuncia("¡LOTERÍA!",AMAR,4200);lluvia(90);Son_(()=>Son.accion("fiesta"));}}
  }

  // ---- experiencia y logros: lo acumulado que manda el servidor
  const LOGROS=[["🎬","Primer render",p=>p.render>=1],["🚀","Primera subida",p=>p.subida>=1],["🎙","20 tandas de voz",p=>p.voz>=20],["⌨️","500 comandos",p=>p.comando>=500],["⌨️","5 000 comandos",p=>p.comando>=5000],
    ["✍️","500 archivos tocados",p=>p.codigo>=500],["🌍","200 búsquedas web",p=>p.busqueda>=200],["🔍","1 000 imágenes revisadas",p=>p.imagen>=1000],["🤖","50 ayudantes",p=>p.ayudante>=50],["🐛","100 bugs",p=>p.fallos>=100],
    ["🏃","10 relevos",p=>p.relevo>=10],["🏆","5 000 acciones",p=>p.acciones>=5000],["🏆","50 000 acciones",p=>p.acciones>=50000],["📅","50 sesiones",p=>p.sesiones>=50]];
  const xpDe=p=>(p.acciones||0)+(p.render||0)*50+(p.subida||0)*100;
  const nivelDe=xp=>Math.floor(Math.sqrt(xp/60))+1;
  function pintaProgreso(p){
    if(!p)return;
    const xp=xpDe(p),n=nivelDe(xp),ini=60*(n-1)**2,fin=60*n**2;
    M.nivel=n;
    Cap.cuerpoR=dorado()?"#e8b923":tema()?.cuerpo||null;
    $("lotNivel").innerHTML=`<b>Nv. ${n}</b><u><i style="width:${Math.round((xp-ini)/(fin-ini)*100)}%"></i></u>`;
    const hechos=LOGROS.filter(l=>l[2](p)),vistos=(lee("vivo_logros")||"").split("|");
    $("lotNivel").title=`${xp} de experiencia · faltan ${fin-xp} para el nivel ${n+1}\n${hechos.length} de ${LOGROS.length} logros: ${hechos.map(l=>l[0]+" "+l[1]).join(" · ")||"ninguno"}\nTraje: bufanda Nv. 3 · capa Nv. 6 · corona Nv. 10 · aura Nv. 15`;
    if(lee("vivo_logros")!=null)for(const l of hechos)if(!vistos.includes(l[1])){anuncia(`🏅 Logro: ${l[1]}`,LILA,4000);lluvia(40);}
    guarda("vivo_logros",hechos.map(l=>l[1]).join("|"));
    if(lee("vivo_nivel")&&+lee("vivo_nivel")<n){anuncia(`⬆ ¡Nivel ${n}!`,VERDE,4000);lluvia(60);}
    guarda("vivo_nivel",n);
  }

  // ---- el estreno: se apaga el taller y salen los primeros segundos del MASTER
  function estreno(){
    const m=M.mundo?.master;if(!m||!M.video||$("cine"))return;
    const el=document.createElement("div");el.id="cine";
    el.innerHTML=`<div class="tel iz"></div><div class="tel de"></div><div class="pcine"><video playsinline autoplay ${$("chkSon").checked?"":"muted"} src="/v2/archivo/${encodeURIComponent(M.video)}/${m.rel.split("/").map(encodeURIComponent).join("/")}"></video></div>
      <div class="fila">${["🍿🤖","🤖","🍿🤖","🤖🍿","🤖"].map(x=>`<span>${x}</span>`).join("")}</div><div class="cartel">Estreno · ${esc(M.r?.proyecto?.titulo||M.video)}</div><button class="bt" title="Cerrar">✕</button>`;
    document.body.appendChild(el);
    const fin=()=>{clearTimeout(tm);el.remove();anuncia("👏 Aplausos en el taller",VERDE);lluvia(80);};
    const tm=setTimeout(fin,17000);
    el.querySelector("button").onclick=fin;
    requestAnimationFrame(()=>requestAnimationFrame(()=>el.classList.add("abre")));
    guarda(`vivo_estreno_${M.video}`,m.t);
  }

  // ---- el resumen: los momentos de la sesión en un minuto, y se puede guardar
  function momentos(){
    const ev=S.ev.filter(e=>!e.de),sel=new Set(),par=(l,n)=>{for(let i=0;i<Math.min(n,l.length);i++)sel.add(l[Math.floor(i*l.length/Math.min(n,l.length))]);};
    const u=ev.find(e=>e.tipo==="usuario");if(u)sel.add(u);
    par(ev.filter(e=>e.tipo==="imagen"&&e.img),6);par(ev.filter(e=>e.tipo==="paso"),3);par(ev.filter(e=>e.fallo),2);
    const c=ev.filter(e=>e.tipo==="cierre").at(-1);if(c)sel.add(c);
    return [...sel].sort((a,b)=>a.seq-b.seq).slice(0,13);
  }
  function resumen(){
    if($("resu")||!S.ev.length)return;
    const el=document.createElement("div");el.id="resu";
    el.innerHTML=`<canvas width="1280" height="720"></canvas><div><button class="bt" id="reGrabar">⏺ Guardar video</button><button class="bt" id="reCerrar">✕ Cerrar</button></div>`;
    document.body.appendChild(el);
    const cv=el.querySelector("canvas"),c=cv.getContext("2d"),ev=S.ev.filter(e=>!e.de);
    const ms=momentos(),titulo=M.r?.proyecto?.titulo||M.r?.titulo||"Sesión",cnt=k=>ev.filter(k).length;
    const dur=(ev.at(-1).t-ev[0].t)/60,cifras=[["acciones",ev.length],["comandos",cnt(e=>e.tipo==="comando")],["archivos",cnt(e=>e.tipo==="codigo")],["imágenes vistas",cnt(e=>e.tipo==="imagen")],["búsquedas",cnt(e=>e.tipo==="busqueda")],["bugs",cnt(e=>e.fallo)]];
    for(const e of ms)if(e.img){e._im=new Image();e._im.src=`/v2/vivo/img/${S.sesion}/${e.img}`;}
    const SL=[{d:3800,f:p=>{c.fillStyle="#fff";c.textAlign="center";c.font="800 62px Segoe UI";linea(titulo,640,290,1120,70,2);c.font="500 30px Segoe UI";c.fillStyle="#b9c1d6";c.fillText(`Lo que hizo el robot en ${dur>=90?(dur/60).toFixed(1).replace(".",",")+" h":Math.round(dur)+" min"}`,640,470);}},
      ...ms.map(e=>({d:e._im?4200:3200,f:p=>{
        const t=TIPOS[e.tipo]||TIPOS.habla,txt=e.tipo==="usuario"||e.tipo==="cierre"?e.detalle:e.titulo;
        if(e._im?.naturalWidth){const z=1+p*.08,w=1280*z,h=w*e._im.naturalHeight/e._im.naturalWidth;c.drawImage(e._im,640-w/2,360-h/2,w,h);c.fillStyle="rgba(8,10,18,.62)";c.fillRect(0,560,1280,160);c.fillStyle="#fff";c.textAlign="left";c.font="700 34px Segoe UI";linea(`${t.ic} ${txt}`,60,626,1160,44,2);}
        else{c.fillStyle="#fff";c.textAlign="center";c.font="800 96px Segoe UI Emoji,Segoe UI";c.fillText(e.fallo?"🐛":t.ic,640,270);c.font="600 40px Segoe UI";linea(e.fallo?`Se atoró: ${txt}`:txt,640,370,1100,54,4);}
        c.textAlign="right";c.font="500 22px Segoe UI";c.fillStyle="#b9c1d6";c.fillText(hora(e.t).slice(0,5),1240,44);}})),
      {d:4800,f:p=>{c.textAlign="center";cifras.forEach(([n,v],i)=>{const x=250+(i%3)*390,y=270+Math.floor(i/3)*230;c.fillStyle="#fff";c.font="800 86px Segoe UI";c.fillText(String(Math.round(v*Math.min(1,p*2.2))),x,y);c.font="500 28px Segoe UI";c.fillStyle="#b9c1d6";c.fillText(n,x,y+46);});}}];
    function linea(t,x,y,w,lh,n){const f=[];let l="";for(const p of String(t||"").replace(/\s+/g," ").split(" ")){const k=l?l+" "+p:p;if(c.measureText(k).width>w&&l){f.push(l);l=p;}else l=k;}if(l)f.push(l);f.slice(0,n).forEach((s,i)=>c.fillText(i===n-1&&f.length>n?s+"…":s,x,y+i*lh));}
    const total=SL.reduce((a,s)=>a+s.d,0);let ini=0,vivo=true,rec=null,trozos=[];
    function cuadro(t){
      if(!vivo)return;
      if(!ini)ini=t;
      let q=t-ini;
      if(q>=total){if(rec){rec.stop();rec=null;$("reGrabar").textContent="⏺ Guardar video";}ini=t;q=0;}
      let s=SL[0],a=0;for(const x of SL){if(q<a+x.d){s=x;break;}a+=x.d;}
      const p=(q-a)/s.d;
      const gr=c.createLinearGradient(0,0,1280,720);gr.addColorStop(0,"#141a33");gr.addColorStop(1,"#2b1d4d");c.fillStyle=gr;c.fillRect(0,0,1280,720);
      c.globalAlpha=Math.min(1,p*7,(1-p)*7);s.f(p);c.globalAlpha=1;
      c.fillStyle="#6b4dff";c.fillRect(0,714,1280*q/total,6);
      requestAnimationFrame(cuadro);
    }
    requestAnimationFrame(cuadro);
    $("reCerrar").onclick=()=>{vivo=false;try{rec?.stop();}catch(e){}el.remove();};
    $("reGrabar").onclick=e=>{
      if(rec)return;
      trozos=[];rec=new MediaRecorder(cv.captureStream(30),{mimeType:MediaRecorder.isTypeSupported("video/webm;codecs=vp9")?"video/webm;codecs=vp9":"video/webm",videoBitsPerSecond:6e6});
      rec.ondataavailable=x=>trozos.push(x.data);
      rec.onstop=()=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob(trozos,{type:"video/webm"}));a.download=`resumen_${M.video||"sesion"}.webm`;a.click();};
      ini=0;rec.start();e.target.textContent="⏺ Grabando…";
    };
  }

  // ---- los eventos: cada uno se mira una vez, ya con su resultado
  const CON_RES=new Set(["comando","codigo","leer","buscar","imagen","navegador","busqueda","pagina","ayudante"]);
  let visto=new Set(),cargado=false;
  function revisaEventos(){
    const ya=ahoraS();let nuevos=0;
    for(const e of S.ev){
      if(visto.has(e.seq))continue;
      if(CON_RES.has(e.tipo)&&!e.listo&&ya-e.t<120)continue;
      visto.add(e.seq);nuevos++;
      if(!cargado||ya-e.t>90||e.de)continue;
      if(e.fallo)nuevoBug();
      else if(e.tipo==="comando")vence();
      if(e.tipo==="usuario"&&e.detalle){J.ini=D().ahora;J.txt=e.detalle;Son_(()=>Son.rx("rxUf"));}
      if(e.tipo==="relevo")relevo();
      if(e.tipo==="comando"&&e.en==="voz"&&!e.fallo&&ya-(M.vozT||0)>60){M.vozT=ya;tocaVoz();}
    }
    cargado=true;
    if(nuevos){
      const f=S.ev.filter(e=>!e.de).slice(-15).filter(e=>e.fallo).length;
      if(f>=5&&M.clima<5){M.flash=D().ahora+900;}
      M.clima=f>=3?f:f?1:0;
    }
    pintaLoteria();
  }
  function revisaJefe(r){
    if(Bo.prueba)return;
    const et=S.etapaViva,en=et==="video"||et==="final";
    if(en){let p=(r.proyecto?.etapas||[]).find(x=>x.id===et)?.progreso||0;if(p<=1)p*=100;Bo.vivo=true;Bo.p=p;Bo.et=et;Bo.muere=0;}
    else if(Bo.vivo){Bo.vivo=false;Bo.muere=D().ahora;anuncia("¡Jefe Render vencido!",AMAR,4200);lluvia(70);Son_(()=>Son.accion("fiesta"));M.pedidoT=-1e9;}
    if(Bo.muere&&D().ahora-Bo.muere>1500)Bo.muere=0;
  }
  async function pideMundo(){
    if(document.hidden)return;
    M.pedidoT=performance.now();
    try{
      const u=new URLSearchParams({video:M.video||"",canal:M.canal||""});
      const w=await (await fetch("/api/v2/vivo/mundo?"+u)).json();
      M.mundo=w;pintaProgreso(w.progreso);
      const m=w.master;$("btEstreno").style.display=m?"":"none";
      if(m&&ahoraS()-m.t<1800&&lee(`vivo_estreno_${M.video}`)!==String(m.t)&&D().W>=900&&!document.hidden)estreno();
    }catch(e){}
  }
  function datos(r){
    M.r=r;M.ctx=r.contexto||null;M.preg=M.fijaPreg||r.pregunta||"";M.pregT=M.fijaPreg?ahoraS():r.pregunta_t||0;
    const antes=M.video;M.video=r.video||"";
    ponCanal(r.proyecto?.canal);
    document.title=(M.preg?"🔔 ":"")+"En vivo";
    if(antes!==M.video||performance.now()-M.pedidoT>30000)pideMundo();
    revisaJefe(r);revisaEventos();
  }

  // ---- el marco de la página: tablero de la lotería, botones y las dos salas
  const est=document.createElement("style");
  est.textContent=`#juego{flex:none}#juego h3{display:flex;align-items:center;gap:8px;cursor:pointer;margin-bottom:5px;user-select:none}#lotNivel{margin-left:auto;display:flex;align-items:center;gap:6px;text-transform:none;letter-spacing:0;color:var(--txt);font-size:11px}#lotNivel u{display:block;width:62px;height:6px;border-radius:3px;background:var(--line);overflow:hidden;text-decoration:none}#lotNivel i{display:block;height:100%;background:var(--acc)}
#lotCartas{display:grid;grid-template-columns:repeat(3,1fr);gap:4px}.lc{display:flex;align-items:center;gap:4px;padding:3px 5px;border:1px solid var(--line);border-radius:6px;font-size:10.5px;color:var(--mut);background:var(--panel2);min-width:0;opacity:.72}.lc i{font-style:normal;font-size:12px}.lc span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.lc.on{opacity:1;color:var(--txt);border-color:var(--warn);box-shadow:inset 0 0 0 1px var(--warn)}.lc.gana{background:var(--warn);color:#201405;border-color:var(--warn)}
#juego.corto #lotCartas{display:none}#juego.corto h3{margin:0}
#cine,#resu{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;background:rgba(3,4,8,.93)}#cine .pcine{width:min(74vw,128vh);aspect-ratio:16/9;background:#000;box-shadow:0 0 90px rgba(255,220,150,.3)}#cine video{width:100%;height:100%;display:block}
#cine .tel{position:absolute;top:0;bottom:0;width:50%;background:repeating-linear-gradient(90deg,#7c1420 0 26px,#a11d2d 26px 52px);transition:transform 1.8s ease-in;z-index:2}#cine .tel.iz{left:0}#cine .tel.de{right:0}#cine.abre .tel.iz{transform:translateX(-96%)}#cine.abre .tel.de{transform:translateX(96%)}
#cine .fila{position:absolute;bottom:2vh;left:0;right:0;display:flex;justify-content:center;gap:5vw;font-size:clamp(24px,5vh,44px);z-index:3}#cine .cartel{position:absolute;top:2.5vh;left:0;right:0;text-align:center;color:#ffd166;font-weight:800;font-size:clamp(15px,2.6vh,24px);z-index:3}#cine button,#resu button{z-index:4}#cine>button{position:absolute;top:14px;right:14px}
#resu{flex-direction:column;gap:12px}#resu canvas{width:min(84vw,136vh);border-radius:10px;box-shadow:0 0 60px rgba(107,77,255,.4)}#resu>div{display:flex;gap:8px}@media (max-width:900px){#btResumen .txt,#btEstreno .txt{display:none}}`;
  document.head.appendChild(est);
  const caja_=document.createElement("div");caja_.className="caja";caja_.id="juego";
  caja_.innerHTML=`<h3><span>Lotería de la sesión</span><span id="lotNivel"></span></h3><div id="lotCartas"></div>`;
  $("filtro").before(caja_);
  caja_.querySelector("h3").onclick=()=>{caja_.classList.toggle("corto");guarda("vivo_lot_corto",caja_.classList.contains("corto")?"1":"0");};
  if(lee("vivo_lot_corto")==="1")caja_.classList.add("corto");
  $("btVivo").insertAdjacentHTML("beforebegin",`<button class="bt" id="btEstreno" style="display:none" title="Los primeros segundos del MASTER en el taller">🎬 <span class="txt">Estreno</span></button><button class="bt" id="btResumen" title="La sesión en un minuto; se puede guardar en video">🎞 <span class="txt">Resumen</span></button>`);
  $("btEstreno").onclick=estreno;$("btResumen").onclick=resumen;

  function prueba(q){
    const d=D();
    if(q.startsWith("canal:")){M.forzado=q.slice(6);return ponCanal("");}
    ({bug(){nuevoBug();setTimeout(nuevoBug,1500);setTimeout(vence,6000);},jefe(){Bo.prueba=true;Bo.vivo=true;Bo.p=62;setTimeout(()=>{Bo.prueba=false;},12000);},relevo,
      usuario(){J.ini=d.ahora;J.txt="aplica todo me gusta";},pregunta(){M.fijaPreg="¿Cuál hago primero?";M.preg=M.fijaPreg;M.pregT=ahoraS();setTimeout(()=>{M.fijaPreg="";},12000);},carta(){leeCarta(true);},loteria(){anuncia("¡LOTERÍA!",AMAR,4200);lluvia(90);},logro(){anuncia("🏅 Logro: 500 comandos",LILA,4000);lluvia(40);},estreno,resumen,lluvia:()=>{M.clima=3;},tormenta:()=>{M.clima=5;M.flash=d.ahora+900;}})[q]?.();
  }
  return {C,datos,cambioSesion:()=>{relevo();visto=new Set();cargado=false;marcas="";},prueba,M,momentos};
})();
