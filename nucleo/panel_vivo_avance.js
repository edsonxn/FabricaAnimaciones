"use strict";
// El avance de las tareas largas (3-nov-2026, el usuario): render, voz, selección… con su % REAL en una tarjeta del lienzo y UNA de 15 animaciones,
// elegida al azar por tarea. Lo hecho se ve construido y lo que falta como contorno punteado: de un vistazo, cuánto lleva y cuánto le falta.
// Probar: Avance.prueba(i, p) — i = 0..14 o parte del nombre; p = 0..1 fijo; sin p recorre de 0 a 100 % en 14 s. Avance.prueba() la apaga.
window.Avance=(()=>{
  const {g,caja,marco,circ,aro,elip,raya,letra,figura,MADERA,TINTA,ROSA,ROJO,AMAR,AZUL,VERDE,LILA,COLORES}=Taller.prim;
  const Cap=Taller.Cap,D=Taller.dim;
  const GH="rgba(255,255,255,.13)",GHL="rgba(255,255,255,.34)";
  const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),suave=q=>q*q*(3-2*q);
  const guarda=(k,v)=>{try{localStorage.setItem(k,v);}catch(e){}};
  const lee=k=>{try{return localStorage.getItem(k);}catch(e){return null;}};
  const punteado=f=>{g.setLineDash([3,3]);f();g.setLineDash([]);};
  const fantasma=(x,y,w,h,r=2)=>{caja(x,y,w,h,r,GH);punteado(()=>marco(x,y,w,h,r,GHL,1));};   // lo que falta: hueco con contorno
  const mini=(x,y,s,T,P={})=>{g.save();g.translate(x,y);g.scale(s*(P.izq?-1:1),s);figura({cuerpo:AZUL,cara:"feliz",...P},T);g.restore();};
  const anda=(T,v=10,a=5)=>[Math.sin(T*v)*a,-Math.sin(T*v)*a];
  const bez=(a,b,c,t)=>[(1-t)*(1-t)*a[0]+2*(1-t)*t*b[0]+t*t*c[0],(1-t)*(1-t)*a[1]+2*(1-t)*t*b[1]+t*t*c[1]];
  function linea(pts,c,lw,dash){g.beginPath();pts.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.strokeStyle=c;g.lineWidth=lw;g.lineCap="round";g.lineJoin="round";if(dash)g.setLineDash(dash);g.stroke();g.setLineDash([]);}
  function tramo(pts,p){                 // la polilínea cortada en la fracción p de su largo: [hecho, falta, punto]
    const L=[0];for(let i=1;i<pts.length;i++)L.push(L[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));
    const m=L[L.length-1]*cl(p);let i=1;while(i<pts.length-1&&L[i]<m)i++;
    const k=(m-L[i-1])/((L[i]-L[i-1])||1),q=[pts[i-1][0]+(pts[i][0]-pts[i-1][0])*k,pts[i-1][1]+(pts[i][1]-pts[i-1][1])*k];
    return [[...pts.slice(0,i),q],[q,...pts.slice(i)],q,Math.atan2(pts[i][1]-pts[i-1][1],pts[i][0]-pts[i-1][0])];
  }
  const piezas=(p,N)=>{const n=Math.min(N,Math.floor(p*N+1e-6));return [n,n<N?p*N-n:0];};   // cuántas enteras y cuánto de la que sigue

  // ---- las 15: cada una dibuja en (0,0)-(w,h) con p = 0..1; u = h/64 es la unidad de grosor
  const ANIM=[
    {n:"Apilando la torre",f(w,h,p,T,c,u){
      const N=8,bh=(h-8*u)/N,bw=Math.min(36*u,w*.18),cx=w*.58,b=h-3*u,[n,q]=piezas(p,N);
      raya(w*.3,b,w*.86,b,GHL,1.5);
      for(let i=0;i<N;i++){const y=b-(i+1)*bh,dx=Math.sin(i*1.7)*2*u;if(i<n){caja(cx-bw/2+dx,y,bw,bh-1,2,COLORES[i%6]);raya(cx-bw/2+dx+3,y+2,cx+bw/2+dx-3,y+2,"rgba(255,255,255,.35)",1);}else fantasma(cx-bw/2+dx,y,bw,bh-1);}
      if(n<N){const dx=Math.sin(n*1.7)*2*u,ty=b-(n+1)*bh,yy=-bh+(ty+bh)*suave(q),sw=Math.sin(T*2.2)*3*u*(1-q);
        raya(cx+dx+sw,0,cx+dx+sw,yy,"#9aa3bd",1.2);caja(cx-bw/2+dx+sw,yy,bw,bh-1,2,COLORES[n%6]);}
      mini(w*.2,b,h/150,T,{brD:[20,-44+Math.sin(T*4)*6]});
    }},
    {n:"Levantando la pared",f(w,h,p,T,c,u){
      const R=4,C=8,x0=w*.3,bw=w*.64/C,bh=(h-7*u)/R,b=h-3*u,[n,q]=piezas(p,R*C);let k=0,ya=null;
      for(let r=0;r<R;r++)for(let j=0;j<C;j++,k++){
        const jj=r%2?C-1-j:j,x=x0+jj*bw+(r%2?bw/2:0),y=b-(r+1)*bh;
        if(k<n){caja(x+.5,y+.5,bw-1.5,bh-1.5,1.5,"#c4603f");raya(x+2,y+2,x+bw-3,y+2,"rgba(255,220,190,.4)",1);}
        else if(k===n){ya=[x,y];g.globalAlpha=.35+.65*q;caja(x+.5,y+.5-(1-q)*10*u,bw-1.5,bh-1.5,1.5,"#c4603f");g.globalAlpha=1;fantasma(x+.5,y+.5,bw-1.5,bh-1.5,1.5);}
        else fantasma(x+.5,y+.5,bw-1.5,bh-1.5,1.5);
      }
      raya(x0-4*u,b,w*.98,b,GHL,1.5);
      mini(w*.15,b,h/150,T,{brD:[22,-30+Math.sin(T*7)*7]});
      if(ya)letra("·",ya[0]+bw/2,ya[1]-4*u+Math.sin(T*9)*2,12*u,"#e9ebf3");
    }},
    {n:"Cargando el tren",f(w,h,p,T,c,u){
      const N=6,y=h-9*u,ww=w*.72/N,lx=w*.78;
      raya(0,y+6*u,w,y+6*u,"#7f89a6",1.6);for(let x=2;x<w;x+=9*u)raya(x,y+5*u,x+4*u,y+8*u,"#5c6478",1.4);
      for(let i=0;i<N;i++){const x=w*.03+i*ww,f=cl(p*N-i),top=y-12*u;
        caja(x,top,ww-4*u,12*u,2,"#5c6478");circ(x+5*u,y+2*u,3*u,TINTA);circ(x+ww-9*u,y+2*u,3*u,TINTA);
        if(i<N-1)raya(x+ww-4*u,y-4*u,x+ww,y-4*u,"#7f89a6",1.4);
        const ch=14*u;fantasma(x+2*u,top-ch,ww-8*u,ch);
        if(f>0){g.save();g.beginPath();g.rect(x+2*u,top-ch*f,ww-8*u,ch*f);g.clip();for(let a=0;a<3;a++)for(let r=0;r<2;r++)caja(x+2*u+a*(ww-8*u)/3+.5,top-(r+1)*ch/2+.5,(ww-8*u)/3-1,ch/2-1,1.5,COLORES[(i+a+r)%6]);g.restore();}
      }
      caja(lx,y-20*u,w*.18,20*u,3,ROJO);caja(lx+w*.1,y-30*u,w*.08,11*u,2,"#c23a4e");caja(lx+4*u,y-28*u,6*u,9*u,1,"#3a4259");
      circ(lx+7*u,y+2*u,4*u,TINTA);circ(lx+w*.14,y+2*u,4*u,TINTA);
      if(p<1)Taller.prim.humito?.(lx+7*u,y-29*u,T,"#d7dbe6",3);
    }},
    {n:"Llenando el tanque",f(w,h,p,T,c,u){
      const tx=w*.38,tw=w*.4,ty=6*u,th=h-10*u,ly=ty+th*(1-p);
      raya(tx-w*.16,4*u,tx+8*u,4*u,"#7f89a6",4*u);raya(tx+8*u,4*u,tx+8*u,ty+2*u,"#7f89a6",4*u);
      if(p<1){g.setLineDash([4*u,3*u]);g.lineDashOffset=-T*40;raya(tx+8*u,ty+2*u,tx+8*u,ly,AZUL,2.4*u);g.setLineDash([]);g.lineDashOffset=0;}
      g.save();g.beginPath();g.roundRect(tx,ty,tw,th,5*u);g.clip();
      g.beginPath();g.moveTo(tx,ly);for(let x=0;x<=tw;x+=3)g.lineTo(tx+x,ly+Math.sin(x/9+T*4)*1.6*u);g.lineTo(tx+tw,ty+th);g.lineTo(tx,ty+th);g.closePath();g.fillStyle="rgba(77,166,255,.75)";g.fill();
      for(let i=0;i<6;i++){const f=(T*.4+i*.17)%1,by=ty+th-f*(ty+th-ly);if(by>ly+3)circ(tx+tw*(.15+.7*((i*.37)%1)),by,1.5*u,"rgba(255,255,255,.6)");}
      g.restore();
      marco(tx,ty,tw,th,5*u,"#cfd6e6",1.6);
      g.font=`600 ${7*u}px "Segoe UI",sans-serif`;g.textAlign="left";g.fillStyle="#aeb4c4";
      for(const k of [.25,.5,.75]){const y=ty+th*(1-k);raya(tx+tw,y,tx+tw+5*u,y,"#aeb4c4",1);g.fillText(Math.round(k*100),tx+tw+7*u,y+2.5*u);}
      mini(w*.17,h-2*u,h/150,T,{brD:[18+Math.cos(T*3)*6,-40+Math.sin(T*3)*6]});
    }},
    {n:"Horneando la pizza",f(w,h,p,T,c,u){
      const cx=w*.5,cy=h*.52,r=h*.45,a0=-Math.PI/2,a1=a0+p*Math.PI*2;
      punteado(()=>{aro(cx,cy,r,GHL,1.2);for(let i=0;i<8;i++){const a=a0+i*Math.PI/4;raya(cx,cy,cx+Math.cos(a)*r,cy+Math.sin(a)*r,GH,1);}});
      if(p>0){const sec=(rr,col)=>{g.beginPath();g.moveTo(cx,cy);g.arc(cx,cy,rr,a0,a1);g.closePath();g.fillStyle=col;g.fill();};
        sec(r,"#d9a35a");sec(r*.84,"#ffcf5a");
        [[.03,.5],[.1,.75],[.16,.35],[.24,.62],[.31,.82],[.38,.42],[.45,.68],[.52,.3],[.6,.78],[.67,.5],[.74,.7],[.81,.36],[.88,.62],[.95,.8]].forEach(([k,rr])=>{if(k<p){const a=a0+k*Math.PI*2;circ(cx+Math.cos(a)*r*rr,cy+Math.sin(a)*r*rr,3.4*u,"#c7372f");}});
        for(let i=1;i<8;i++)if(i/8<p){const a=a0+i*Math.PI/4;raya(cx,cy,cx+Math.cos(a)*r*.98,cy+Math.sin(a)*r*.98,"rgba(120,60,20,.5)",1);}}
      Taller.prim.humito?.(cx-8*u,cy-r*.3,T,"rgba(255,255,255,.7)",2);
      mini(w*.86,h-2*u,h/150,T,{izq:true,brD:[20,-38+Math.sin(T*5)*4]});
    }},
    {n:"Tendiendo el puente",f(w,h,p,T,c,u){
      const dy=h*.42,a=w*.15,bB=w*.85,N=10,pw=(bB-a)/N,[n,q]=piezas(p,N);
      g.fillStyle="#2b5f8a";g.fillRect(a,h*.8,bB-a,h*.2);for(let i=0;i<6;i++){const x=a+((i*.19+T*.05)%1)*(bB-a);raya(x,h*.86,x+8*u,h*.86,"rgba(255,255,255,.4)",1);}
      caja(0,dy,a,h-dy,0,"#6b5a45");caja(bB,dy,w-bB,h-dy,0,"#6b5a45");caja(0,dy,a,3*u,0,"#5bbf6a");caja(bB,dy,w-bB,3*u,0,"#5bbf6a");
      for(let i=0;i<N;i++){const x=a+i*pw;if(i<n)caja(x+.5,dy,pw-1,4*u,1,MADERA);else if(i>n||!q)fantasma(x+.5,dy,pw-1,4*u,1);}
      if(n<N&&q>0){g.save();g.translate(a+n*pw,dy);g.rotate(-(1-suave(q))*1.3);caja(.5,0,pw-1,4*u,1,MADERA);g.restore();fantasma(a+n*pw+.5,dy,pw-1,4*u,1);}
      if(n)raya(a,dy-9*u,a+n*pw,dy-9*u,"#cfd6e6",1);
      mini(Math.max(a*.5,a+n*pw-6*u),dy,h/170,T,{pies:anda(T,6,3),brD:[16,-40]});
    }},
    {n:"Rumbo a la Luna",f(w,h,p,T,c,u){
      for(let i=0;i<14;i++){g.globalAlpha=.3+.6*Math.abs(Math.sin(T*1.3+i*2.1));circ((i*.137%1)*w,(i*.291%1)*h,1+(i%2)*.6,"#fff");}g.globalAlpha=1;
      const P0=[w*.07,h*.92],P1=[w*.3,-h*.1],P2=[w*.84,h*.22],pts=[];for(let i=0;i<=40;i++)pts.push(bez(P0,P1,P2,i/40));
      const [hecho,falta,q]=tramo(pts,p);
      linea(falta,GHL,1.3,[3,4]);linea(hecho,AMAR,2.2*u);
      for(const k of [.25,.5,.75]){const [x,y]=bez(P0,P1,P2,k);circ(x,y,2*u,k<=p?AMAR:"#5c6478");}
      circ(P2[0],P2[1],10*u,"#eef2ff");circ(P2[0]-3*u,P2[1]-2*u,2.4*u,"#c9cfe0");circ(P2[0]+4*u,P2[1]+3*u,1.6*u,"#c9cfe0");
      const [ax,ay]=bez(P0,P1,P2,Math.min(1,p+.01)),ang=Math.atan2(ay-q[1],ax-q[0])||-.6;
      g.save();g.translate(q[0],q[1]);g.rotate(ang);const s=u;
      elip(-13*s,0,(6+Math.sin(T*30)*2)*s,2.6*s,"#ff8a2a");elip(-11*s,0,3*s,1.5*s,"#ffd166");
      elip(0,0,10*s,4.2*s,"#f2f3f8");g.beginPath();g.moveTo(9*s,-3.4*s);g.quadraticCurveTo(15*s,0,9*s,3.4*s);g.closePath();g.fillStyle=ROJO;g.fill();
      circ(2*s,0,1.8*s,AZUL);for(const v of [-1,1]){g.beginPath();g.moveTo(-6*s,v*3*s);g.lineTo(-10*s,v*7*s);g.lineTo(-3*s,v*3*s);g.closePath();g.fillStyle=ROJO;g.fill();}
      g.restore();
    }},
    {n:"La carrera",f(w,h,p,T,c,u){
      const y=h*.78,x0=w*.06,x1=w*.9,x=x0+(x1-x0)*p;
      caja(0,y,w,h-y,0,"#8a4b3a");raya(0,y+5*u,w,y+5*u,"rgba(255,255,255,.35)",1);
      linea([[x,y-1],[x1,y-1]],GHL,1.2,[3,4]);raya(x0,y-1,x,y-1,VERDE,2.4*u);
      g.font=`700 ${7*u}px "Segoe UI",sans-serif`;g.textAlign="center";
      for(const k of [0,.25,.5,.75]){const mx=x0+(x1-x0)*k;raya(mx,y-4*u,mx,y+3*u,"#e9ebf3",1);g.fillStyle=k<=p?"#e9ebf3":"#6f7688";g.fillText(Math.round(k*100),mx,y+12*u);}
      raya(x1,y,x1,y-40*u,"#cfd6e6",1.6);for(let r=0;r<3;r++)for(let k=0;k<4;k++)caja(x1+k*4*u,y-40*u+r*4*u+Math.sin(T*6+k)*u,4*u,4*u,0,(r+k)%2?"#fff":TINTA);
      for(let i=0;i<3;i++){const f=(T*2+i/3)%1;g.globalAlpha=.5*(1-f);circ(x-8*u-f*14*u,y-3*u-f*6*u,2*u+f*3*u,"#d7dbe6");}g.globalAlpha=1;
      mini(x,y-1,h/150,T,{pies:anda(T,16,7),incl:.12,brD:[16,-20+Math.sin(T*16)*6],brI:[-16,-20-Math.sin(T*16)*6]});
    }},
    {n:"Haciendo crecer la planta",f(w,h,p,T,c,u){
      const cx=w*.42,b=h-3*u,py=b-12*u,Hs=h*.74,top=py-Hs*p,sw=Math.sin(T*1.5)*2*u;
      punteado(()=>raya(cx+12*u,py,cx+12*u,py-Hs,GHL,1));caja(cx+12*u,py-Hs-1,9*u,5*u,1,"#6f7688");
      g.beginPath();g.moveTo(cx,py);g.quadraticCurveTo(cx-4*u,py-Hs*p*.5,cx+sw,top);g.strokeStyle="#4caf50";g.lineWidth=2.4*u;g.stroke();
      for(let i=0;i<6;i++){const k=(i+1)/7,e=cl((p-k)*8);if(e<=0)continue;const ly=py-Hs*k,s=i%2?1:-1;g.save();g.translate(cx+sw*k,ly);g.rotate(s*.6);elip(s*6*u*e,0,7*u*e,3*u*e,"#5bbf6a");g.restore();}
      const fl=cl((p-.86)/.14);if(fl>0){for(let i=0;i<5;i++){const a=i*1.257+T*.5;circ(cx+sw+Math.cos(a)*5*u*fl,top+Math.sin(a)*5*u*fl,4*u*fl,ROSA);}circ(cx+sw,top,3*u*fl,AMAR);}
      else circ(cx+sw,top,2.4*u,"#7cd67f");
      g.beginPath();g.moveTo(cx-13*u,py);g.lineTo(cx+13*u,py);g.lineTo(cx+10*u,b);g.lineTo(cx-10*u,b);g.closePath();g.fillStyle="#c96f45";g.fill();caja(cx-14*u,py-3*u,28*u,4*u,1,"#b35d38");
      const rx=w*.75;mini(rx,b,h/150,T,{izq:true,brD:[24,-36]});
      g.save();g.translate(rx-15*u,b-30*u);g.rotate(-.5+Math.sin(T*2)*.08);caja(-7*u,-4*u,12*u,8*u,2,"#7f89a6");raya(-7*u,-1,-14*u,-4*u,"#7f89a6",2*u);g.restore();
      for(let i=0;i<4;i++){const f=(T*1.4+i/4)%1;circ(rx-31*u-f*6*u,b-32*u+f*18*u,1.3*u,AZUL);}
    }},
    {n:"Armando el rompecabezas",f(w,h,p,T,c,u){
      const C=5,R=3,ord=[7,2,11,0,13,5,9,3,14,1,8,12,4,10,6],cs=Math.min((h-8*u)/R,w*.6/C),x0=w*.5-C*cs/2,y0=(h-R*cs)/2,[n,q]=piezas(p,15);
      const color=(i)=>{const r=Math.floor(i/C),k=i%C;return r===0?(k===3?AMAR:"#7fc8f8"):r===1?(k===1||k===2?"#8d99ae":"#9fd6ff"):(k===4?"#3f8a5a":"#5bbf6a");};
      marco(x0-3*u,y0-3*u,C*cs+6*u,R*cs+6*u,3,MADERA,2.4);
      for(let i=0;i<15;i++){const x=x0+(i%C)*cs,y=y0+Math.floor(i/C)*cs;fantasma(x+1,y+1,cs-2,cs-2,2);}
      for(let k=0;k<n;k++){const i=ord[k],x=x0+(i%C)*cs,y=y0+Math.floor(i/C)*cs;caja(x+.5,y+.5,cs-1,cs-1,2,color(i));circ(x+cs,y+cs/2,cs*.12,color(i));}
      if(n<15){const i=ord[n],x=x0+(i%C)*cs,y=y0+Math.floor(i/C)*cs-(1-suave(q))*12*u+Math.sin(T*3)*u;g.globalAlpha=.45+.55*q;caja(x+.5,y+.5,cs-1,cs-1,2,color(i));marco(x+.5,y+.5,cs-1,cs-1,2,"#fff",1.2);g.globalAlpha=1;}
      mini(w*.1,h-2*u,h/160,T,{brD:[22,-44+Math.sin(T*3)*5]});
    }},
    {n:"Pintando la cerca",f(w,h,p,T,c,u){
      const N=10,x0=w*.06,pw=(w*.88)/N,b=h-4*u,ph=h*.66,[n,q]=piezas(p,N),col=c||AMAR;
      caja(0,b,w,4*u,0,"#4f9a68");raya(x0,b-ph*.3,x0+N*pw,b-ph*.3,"#6a4f36",2.4*u);raya(x0,b-ph*.75,x0+N*pw,b-ph*.75,"#6a4f36",2.4*u);
      const tabla=(x,y0,y1,colr)=>{g.beginPath();g.moveTo(x,y1);g.lineTo(x,y0+4*u);g.lineTo(x+pw*.35,y0);g.lineTo(x+pw*.7,y0+4*u);g.lineTo(x+pw*.7,y1);g.closePath();g.fillStyle=colr;g.fill();};
      for(let i=0;i<N;i++){const x=x0+i*pw+pw*.15;tabla(x,b-ph,b,"#8a6a4a");if(i<n)tabla(x,b-ph,b,col);
        else if(i===n&&q>0){g.save();g.beginPath();g.rect(x-1,b-ph*q,pw,ph*q);g.clip();tabla(x,b-ph,b,col);g.restore();}}
      if(n<N){const rx=x0+n*pw+pw*.5,ry=b-ph*q;caja(rx-5*u,ry-2*u,10*u,4*u,2,"#f2f3f8");mini(rx+pw*.65,b,h/165,T,{izq:true,brD:[22,-26-Math.sin(T*5)*10]});}
    }},
    {n:"Escalando la montaña",f(w,h,p,T,c,u){
      const pk=[w*.6,h*.1];
      g.beginPath();g.moveTo(w*.1,h);g.lineTo(pk[0],pk[1]);g.lineTo(w*.98,h);g.closePath();g.fillStyle="#5c6478";g.fill();
      g.beginPath();g.moveTo(pk[0]-9*u,pk[1]+13*u);g.lineTo(pk[0],pk[1]);g.lineTo(pk[0]+8*u,pk[1]+11*u);g.lineTo(pk[0]+2*u,pk[1]+9*u);g.closePath();g.fillStyle="#eef2ff";g.fill();
      const cx=((T*.03)%1)*w*1.3-w*.15;elip(cx,h*.25,14*u,4*u,"rgba(255,255,255,.5)");
      const ruta=[[w*.2,h*.96],[w*.62,h*.82],[w*.36,h*.64],[w*.66,h*.47],[w*.47,h*.32],[pk[0],pk[1]+2*u]];
      const [hecho,falta,q]=tramo(ruta,p);linea(falta,GHL,1.2,[3,3]);linea(hecho,AMAR,2*u);
      raya(pk[0],pk[1],pk[0],pk[1]-14*u,"#cfd6e6",1.4);g.beginPath();g.moveTo(pk[0],pk[1]-14*u);g.lineTo(pk[0]+(9+Math.sin(T*5))*u,pk[1]-11*u);g.lineTo(pk[0],pk[1]-8*u);g.closePath();g.fillStyle=c||ROJO;g.fill();
      mini(q[0],q[1],h/230,T,{pies:anda(T,8,4),brD:[16,-46]});
    }},
    {n:"Tirando el dominó",f(w,h,p,T,c,u){
      const N=14,x0=w*.07,sp=w*.84/N,b=h-4*u,dh=h*.5,dw=4.5*u,[n,q]=piezas(p,N),cae=1.12;
      raya(0,b,w,b,GHL,1.2);
      for(let i=N-1;i>=0;i--){const x=x0+i*sp,a=i<n?cae:i===n?cae*suave(q)*q:0;
        g.save();g.translate(x+dw,b);g.rotate(a);
        if(i<n||i===n&&q>0){caja(-dw,-dh,dw,dh,1.5,COLORES[i%6]);circ(-dw/2,-dh*.3,1*u,TINTA);circ(-dw/2,-dh*.7,1*u,TINTA);}
        else{caja(-dw,-dh,dw,dh,1.5,"#e9ebf3");g.globalAlpha=.6;raya(-dw,-dh/2,0,-dh/2,TINTA,1);g.globalAlpha=1;}
        g.restore();}
      mini(w*.035,b,h/190,T,{brD:[22,-34]});
      if(p>=1)letra("✦",x0+N*sp+4*u,b-dh-4*u+Math.sin(T*6)*2,10*u,AMAR);
    }},
    {n:"Cargando el camión",f(w,h,p,T,c,u){
      const C=5,R=3,cx=w*.4,cw=w*.44,cy=h*.14,chh=h*.62,bw=cw/C,bh=chh/R,b=cy+chh,[n,q]=piezas(p,C*R);
      marco(cx,cy,cw,chh,3,"#cfd6e6",1.8);caja(cx+cw,cy+chh*.35,w*.13,chh*.65,4,ROJO);caja(cx+cw+3*u,cy+chh*.42,w*.07,chh*.2,2,"#9fd6ff");
      circ(cx+cw*.2,b+5*u,5*u,TINTA);circ(cx+cw*.8,b+5*u,5*u,TINTA);circ(cx+cw+w*.08,b+5*u,5*u,TINTA);raya(cx,b+1,cx+cw+w*.13,b+1,"#7f89a6",2*u);
      const lugar=k=>{const col=C-1-Math.floor(k/R),row=R-1-k%R;return [cx+col*bw,cy+row*bh];};
      for(let k=0;k<C*R;k++){const [x,y]=lugar(k);if(k<n){caja(x+1,y+1,bw-2,bh-2,1.5,"#c8935a");raya(x+bw/2,y+1,x+bw/2,y+bh-1,"#a5743f",1.2);}else fantasma(x+1.5,y+1.5,bw-3,bh-3,1.5);}
      if(n<C*R){const rx=w*.05+(cx-w*.1)*suave(q),by=h-2*u;mini(rx,by,h/165,T,{pies:anda(T,10,4),brD:[10,-74],brI:[-10,-74]});caja(rx-bw*.4,by-h/165*90,bw*.8,bh*.7,1.5,"#c8935a");}
    }},
    {n:"Pasa la arena",f(w,h,p,T,c,u){
      const cx=w*.5,t0=5*u,b=h-5*u,m=(t0+b)/2,a=h*.24,nk=1.6*u;
      const bulbo=()=>{g.beginPath();g.moveTo(cx-a,t0);g.lineTo(cx+a,t0);g.quadraticCurveTo(cx+a,m-6*u,cx+nk,m);g.quadraticCurveTo(cx+a,m+6*u,cx+a,b);g.lineTo(cx-a,b);g.quadraticCurveTo(cx-a,m+6*u,cx-nk,m);g.quadraticCurveTo(cx-a,m-6*u,cx-a,t0);g.closePath();};
      g.save();bulbo();g.clip();g.fillStyle="#f0c674";
      const sup=m-(m-t0)*.9*Math.sqrt(1-p);if(p<1)g.fillRect(cx-a,sup,a*2,m-sup);
      const alto=(b-m)*.9*Math.sqrt(p),cima=b-alto;g.beginPath();g.moveTo(cx-a,b);g.lineTo(cx-a,cima+alto*.35);g.quadraticCurveTo(cx,cima-alto*.15,cx+a,cima+alto*.35);g.lineTo(cx+a,b);g.closePath();g.fill();
      if(p<1){g.setLineDash([2*u,2*u]);g.lineDashOffset=-T*30;raya(cx,m,cx,cima,"#f0c674",1.4*u);g.setLineDash([]);g.lineDashOffset=0;}
      g.restore();bulbo();g.strokeStyle="#cfd6e6";g.lineWidth=1.4;g.stroke();
      caja(cx-a-5*u,t0-4*u,a*2+10*u,4*u,2,MADERA);caja(cx-a-5*u,b,a*2+10*u,4*u,2,MADERA);
      mini(w*.2,h-1,h/150,T,{brD:[24,-50],cara:p>.9?"feliz":"normal"});
      g.font=`700 ${8*u}px "Segoe UI",sans-serif`;g.textAlign="left";g.fillStyle="#aeb4c4";g.fillText("falta",cx+a+8*u,t0+10*u);g.fillStyle="#f0c674";g.fillText("lleva",cx+a+8*u,b-4*u);
    }},
  ];

  // ---- la tarea en curso: sale de las etapas reales del video (r.proyecto) y se suaviza, porque el panel la recalcula cada ~20 s
  const A={on:false,key:"",i:0,p:0,v:0,ini:0,fin:0,listo:false,nombre:"",det:"",prueba:null};
  function elige(key){
    const k=lee("vivo_avance_k");if(k&&k.startsWith(key+"|"))return +k.slice(key.length+1)%ANIM.length;   // al recargar, la misma de esa tarea
    const ult=+(lee("vivo_avance_ult")||-1);let i;do{i=Math.floor(Math.random()*ANIM.length);}while(i===ult&&ANIM.length>1);
    guarda("vivo_avance_ult",String(i));guarda("vivo_avance_k",key+"|"+i);return i;
  }
  function datos(r){
    if(A.prueba)return;
    const pr=r&&r.proyecto,et=pr&&(pr.etapas||[]),act=et&&(et.find(e=>e.id===pr.etapa_actual)||et.find(e=>e.estado==="en_curso"));
    const p=act?+act.progreso||0:0,con=act&&act.estado==="en_curso"&&p<.999&&(p>0||/\d+\s*\/\s*\d+/.test(act.detalle||""));
    if(con){
      const key=`${r.video||pr.titulo||""}|${act.id}`;
      if(key!==A.key||!A.on){A.key=key;A.i=elige(key);A.ini=D().ahora;A.v=p;}
      Object.assign(A,{on:true,fin:0,p,nombre:act.nombre||act.id,det:act.detalle||"",listo:false});
    }else if(A.on){
      const e=et&&et.find(x=>`${r.video||pr.titulo||""}|${x.id}`===A.key);
      A.on=false;A.fin=D().ahora;A.listo=!!e&&(e.estado==="listo"||e.estado==="lista"||(+e.progreso||0)>=.999)||A.p>=.97;
      if(A.listo)A.p=1;
    }
  }
  function corto(det){                   // del detalle del panel, lo que dice cuánto falta en tiempo
    const s=String(det||""),r=s.match(/~?\d+:\d{2}(:\d{2})?\s*restantes/),f=s.match(/termina \d{1,2}:\d{2}/),n=s.match(/\d+\s*\/\s*\d+\s*[^\s·(]*/);
    return [r&&r[0],f&&f[0]].filter(Boolean).join(" · ")||(n?n[0]:"");
  }
  const recorta=(s,ancho)=>{if(g.measureText(s).width<=ancho)return s;while(s&&g.measureText(s+"…").width>ancho)s=s.slice(0,-1);return s+"…";};
  function tarjeta(t,dt){
    if(A.prueba){const q=A.prueba;if(q.p==null){const k=(t-q.ini)/14000;A.p=cl(k);if(k>1.25){A.prueba=null;A.on=false;A.fin=t;A.listo=true;A.p=1;}}else A.p=q.p;}
    if(!A.on&&!A.fin)return;
    const sale=A.fin?(t-A.fin)/1000:0;if(sale>4.2){A.fin=0;return;}
    if(A.p<A.v-.15)A.v=A.p;else A.v+=(A.p-A.v)*(1-Math.exp(-(dt||16)/900));
    const d=D(),T=t/1000,c=A.listo&&A.fin?VERDE:(d.pal["--acc"]||LILA);
    const w=Math.round(cl(d.W*.24,205,290)*(window.EN_VIDEO?1.5:1)),s=w/250,h=150*s,x=d.piso===null?d.W-w-(matchMedia("(pointer:coarse)").matches?54:50):d.W*(d.AN||1)-w-10*s,y=(d.PCH||0)+10*s;   // en el edificio, a la izquierda de la columna de zoom
    const al=Math.min(1,(t-A.ini)/450,sale?(4.2-sale)/.6:1);g.save();g.globalAlpha=cl(al);
    g.translate(0,(1-cl(al))*-12*s);
    caja(x,y,w,h,10*s,"rgba(14,16,24,.94)");marco(x,y,w,h,10*s,c,1.6);
    const an=ANIM[A.i];
    g.textBaseline="alphabetic";g.font=`750 ${12*s}px "Segoe UI",system-ui,sans-serif`;g.textAlign="left";g.fillStyle="#f2f3f8";
    const nom=recorta(A.nombre,w*.45);g.fillText(nom,x+12*s,y+19*s);
    g.font=`600 ${9.5*s}px "Segoe UI",system-ui,sans-serif`;g.textAlign="right";g.fillStyle="#aeb4c4";g.fillText(recorta(an.n,w-g.measureText(nom).width-40*s),x+w-12*s,y+19*s);
    const sw=w-20*s,sh=66*s;
    g.save();g.translate(x+10*s,y+26*s);g.beginPath();g.rect(0,0,sw,sh);g.clip();caja(0,0,sw,sh,6*s,"rgba(255,255,255,.04)");
    try{an.f(sw,sh,A.listo&&A.fin?1:cl(A.v),T,c,sh/64);}catch(e){}
    g.restore();
    const bx=x+12*s,by=y+100*s,bw=w-24*s,bh=9*s,v=A.listo&&A.fin?1:cl(A.v);
    caja(bx,by,bw,bh,bh/2,"#262b3a");if(v>0)caja(bx,by,Math.max(bh,bw*v),bh,bh/2,c);
    for(let i=1;i<10;i++)raya(bx+bw*i/10,by+2,bx+bw*i/10,by+bh-2,"rgba(0,0,0,.28)",1);
    if(v<1){const lx=bx+bw*v,br=.5+.5*Math.sin(T*5);circ(lx,by+bh/2,bh*.42,`rgba(255,255,255,${.5+.4*br})`);}
    const pct=A.listo&&A.fin?100:Math.min(99,Math.floor(v*100));
    g.font=`850 ${24*s}px "Segoe UI",system-ui,sans-serif`;g.textAlign="left";g.fillStyle=c;g.fillText(`${pct} %`,bx,y+136*s);
    g.font=`600 ${9*s}px "Segoe UI",system-ui,sans-serif`;g.fillStyle="#aeb4c4";g.fillText("lleva",bx+1,y+146*s);
    g.textAlign="right";
    if(A.fin){g.font=`800 ${15*s}px "Segoe UI",system-ui,sans-serif`;g.fillStyle=A.listo?VERDE:"#aeb4c4";g.fillText(A.listo?"¡Listo!":"Se detuvo",bx+bw,y+128*s);}
    else{g.font=`800 ${14*s}px "Segoe UI",system-ui,sans-serif`;g.fillStyle=AMAR;g.fillText(`falta ${100-pct} %`,bx+bw,y+126*s);
      const q=corto(A.det);if(q){g.font=`500 ${9.5*s}px "Segoe UI",system-ui,sans-serif`;g.fillStyle="#aeb4c4";g.fillText(recorta(q,bw*.62),bx+bw,y+142*s);}}
    if(A.fin&&A.listo)for(let i=0;i<9;i++){const k=(sale*.9+i/9)%1;letra("✦",x+w*((i*.37+.1)%1),y+h*(.95-k*.9),(8+(i%3)*3)*s,COLORES[i%6]);}
    g.restore();
  }
  const antesE=Cap.encima;Cap.encima=(t,dt)=>{if(antesE)antesE(t,dt);tarjeta(t,dt);};
  const antesD=window.Extras&&Extras.datos;if(window.Extras)Extras.datos=r=>{if(antesD)antesD(r);datos(r);};
  function prueba(i,p){
    if(i==null){A.prueba=null;A.on=false;A.fin=0;return;}
    const k=typeof i==="number"?i:ANIM.findIndex(a=>a.n.toLowerCase().includes(String(i).toLowerCase()));
    A.i=((k%ANIM.length)+ANIM.length)%ANIM.length;A.prueba={ini:D().ahora,p};A.on=true;A.fin=0;A.listo=false;A.ini=D().ahora;A.v=p??0;A.p=p??0;A.nombre="Render (prueba)";A.det="12/40 segmentos · ~3:20 restantes · termina 15:42";
    return ANIM[A.i].n;
  }
  return {datos,prueba,ANIM,A};
})();
