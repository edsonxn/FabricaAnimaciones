"use strict";
// El muñeco de trapo del taller «En vivo» (3-nov-2026, el usuario: «que se caigan los robots a veces y la cámara los enfoque… tipo Euphoria,
// kinemático con ragdoll, que se tomen de las manos o pies»). Cuando le toca, un robot deja de ser dibujo con pose y pasa a ser un muñeco de Verlet
// de 7 puntos (cabeza, pecho, cadera, 2 manos, 2 pies) con MÚSCULOS: resortes hacia una pose objetivo cuya fuerza va de 0 (trapo) a 1 (animación).
// Reflejos como Euphoria: al caer mete las manos; se agarra de quien tenga cerca (lo salva o se lo lleva); otro va y le da la mano para levantarlo,
// o el del suelo le agarra el pie y lo tumba; dos que están sin hacer nada se toman de las manos y bailan. Se levanta en dos tiempos (rodillas, de pie).
// 5-nov-2026 (el usuario: «que se enfrenten a obstáculos todo el tiempo… puentes, acantilados… enemigos… que se tengan que defender»): varias escenas
// a la vez (la cámara solo sigue una), hoyos con paredes de los que se sale trepando, techo con «¡BONK!», guardia con arma, golpe, esquiva y salto.
// Los peligros los pone panel_vivo_peligros.js con Trapo.golpe / Trapo.guardia / Trapo.salta / Trapo.ponHoyo.
// Es teatro: no cambia la acción real, el letrero ni la estación; al acabar, el robot sigue desde donde quedó. Solo en el edificio, nunca en EN_VIDEO.
// Probar en la consola: Trapo.prueba("tropiezo"|"resbalon"|"desmayo"|"cadena"|"domino"|"ayuda"|"pie"|"manos"); Trapo.cada(30000, 70000) = cada cuánto.
window.Trapo=(()=>{
  if(typeof Taller==="undefined"||!Taller.entidades||window.EN_VIDEO)return null;
  const {g,caja,marco,circ,aro,elip,raya,letra,corazon,ojos,gorro,TINTA,CABEZA,VISOR,ROSA,ROJO,AMAR,AZUL,VERDE}=Taller.prim;
  const Cap=Taller.Cap,M=Taller.mundo;
  const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),suave=q=>{q=cl(q);return q*q*(3-2*q);},azar=(a,b)=>a+Math.random()*(b-a),elige=L=>L[Math.floor(Math.random()*L.length)];
  const suena=(n,f)=>{try{if(typeof Son!=="undefined")Son.mini(n,f);}catch(e){}};

  // ---- el esqueleto, en unidades de figura(): pies en y = 0, y negativa hacia arriba, x hacia delante del robot
  const CAB=0,PEC=1,CAD=2,MI=3,MD=4,PI=5,PD=6;          // MI y PI = la mano y el pie de atrás; MD y PD = los de delante
  const RAD=[16,11,9,3.4,3.4,2.6,2.6],MASA=[3,4,4,.6,.6,.8,.8];
  const PARADO=[[0,-45],[0,-25],[0,-11],[-15,-14],[15,-14],[-6,-2.6],[6,-2.6]];
  const RODILLAS=[[9,-31],[4,-18],[-3,-9],[13,-3.4],[18,-3.4],[-12,-2.6],[-5,-2.6]];
  const AGACHA=[[8,-38],[4,-22],[0,-11],[-13,-16],[24,-7],[-6,-2.6],[6,-2.6]];
  const JALA=[[-7,-43],[-3,-25],[0,-11],[-15,-17],[21,-21],[-8,-2.6],[5,-2.6]];
  const GUARDIA=[[-3,-44],[-2,-25],[0,-11],[8,-30],[16,-34],[-7,-2.6],[6,-2.6]];   // puños arriba, el peso atrás, el arma lista
  const DUCK=[[14,-36],[4,-19],[-2,-6],[16,-12],[20,-16],[-9,-2.6],[7,-2.6]];         // se agacha: la cabeza baja todo lo que dejan los huesos
  const TREPA=[[0,-45],[0,-25],[0,-11],[-10,-58],[10,-60],[-6,-2.6],[6,-2.6]];        // los brazos arriba, agarrado del borde
  const HUESOS=[[CAB,PEC,20,20],[PEC,CAD,14,14],[CAB,CAD,30,34.5],[PEC,MI,7,21],[PEC,MD,7,21],[CAD,PI,6,11],[CAD,PD,6,11],[PI,PD,3,20]];
  const HZ=180,H=1/HZ;                   // paso fijo de la física: igual en una PC lenta que en una rápida
  const GRAV=820;                        // unidades/s²: un robot mide ~70 unidades, así que cae como de dibujo animado
  const GOLPES=["¡PLAF!","¡PUM!","¡PAF!","¡BONK!","¡CATAPLÁN!","¡ZAS!"];
  const ARMAS=["llave","escoba","chancla","periodico","sarten","martillo"];

  let Shs=[],prox=0,cadaMs=[18000,40000],ya=0,ultFoco=-1e9,hoyo=null,cols=null;
  const MAX_ESC=4;
  const enUso=E=>Shs.some(sh=>sh.rds.some(rd=>rd.E===E));
  // ---- los muebles (5-nov-2026): colisionadores por piso que pone panel_vivo_peligros.js con Trapo.ponCols(piso → lista), en px del piso.
  // plat = plataforma de un solo sentido (también inclinada = rampa: mesas, repisas, escalera); seg = tubo o barandal sólido (r = grosor);
  // circ = lámpara (c.on(vx,vy) la columpia); caja = caja sólida. asa:true = se puede agarrar; f:"asa" = solo para agarrarse (pasamanos).
  const colsDe=p=>{try{return cols?cols(p)||[]:[];}catch(e){return [];}};
  const NOCOL=new Set(["camina","baila","trepa","salta"]);   // lo que va con guion (caminar a otro, bailar, trepar, brincar) no choca con muebles
  function bbC(c){if(!c.bb){const r=c.r||0;c.bb=c.f==="circ"?[c.x-r,c.y-r,c.x+r,c.y+r]:[Math.min(c.x0,c.x1)-r,Math.min(c.y0,c.y1)-r,Math.max(c.x0,c.x1)+r,Math.max(c.y0,c.y1)+r];}return c.bb;}
  function encima(rd,c){                 // ¿el cuerpo toca la caja del mueble? (al nacer: lo que ya tenía encima no lo expulsa de golpe)
    const b=c.f==="circ"?[c.x-c.r,c.y-c.r,c.x+c.r,c.y+c.r]:bbC(c);
    for(const p of rd.P)if(p.x+p.r>b[0]-3&&p.x-p.r<b[2]+3&&p.y+p.r>b[1]-3&&p.y-p.r<b[3]+3)return true;
    return false;
  }
  const ignora=rd=>new Set(colsDe(rd.piso).filter(c=>c.f!=="asa"&&encima(rd,c)).map(c=>c.id));
  function contacto(rd,i,p,nx,ny,pen,c){ // empuja fuera del mueble; rebote y rozamiento según el mueble, golpe si venía rápido
    p.x+=nx*pen;p.y+=ny*pen;
    let vx=p.x-p.px,vy=p.y-p.py;const vn=vx*nx+vy*ny;
    if(vn>=0)return;
    const sp=-vn/H;
    if(i<=CAD&&sp>230*rd.s&&rd.k[i]<.5)golpe(rd,p.x,sp,p.y+p.r+(ny<-.5?0:30*rd.s),c.txt);
    if(c.on&&sp>40*rd.s)c.on(-vn*nx/H*MASA[i]/4,-vn*ny/H*MASA[i]/4);
    const rb=c.rb??.15,fr=rd.k[i]>.5?.5:(c.fr??.12);
    const tx=(vx-vn*nx)*(1-fr),ty=(vy-vn*ny)*(1-fr);
    vx=tx-vn*rb*nx;vy=ty-vn*rb*ny;p.px=p.x-vx;p.py=p.y-vy;
  }
  function choca(rd,i,p,C){
    for(const c of C){
      if(c.f==="asa"||(rd.ign&&rd.ign.has(c.id)))continue;
      const b=bbC(c);if(p.x+p.r<b[0]||p.x-p.r>b[2]||p.y+p.r<b[1]||p.y-p.r>b[3])continue;
      if(c.f==="plat"){                  // un solo sentido: solo si venía por encima de la línea
        const dx=c.x1-c.x0,dy=c.y1-c.y0,L2=dx*dx+dy*dy,t=((p.x-c.x0)*dx+(p.y-c.y0)*dy)/L2;if(t<0||t>1)continue;
        const L=Math.sqrt(L2);let nx=dy/L,ny=-dx/L;if(ny>0){nx=-nx;ny=-ny;}
        const sd=(p.x-c.x0)*nx+(p.y-c.y0)*ny,sp=(p.px-c.x0)*nx+(p.py-c.y0)*ny;
        if(sd<p.r&&sp>=p.r-2.2)contacto(rd,i,p,nx,ny,p.r-sd,c);
      }else if(c.f==="caja"){
        const l=p.x+p.r-c.x0,r=c.x1-(p.x-p.r),u=p.y+p.r-c.y0,d=c.y1-(p.y-p.r),m=Math.min(l,r,u,d);if(m<=0)continue;
        if(m===u)contacto(rd,i,p,0,-1,u,c);else if(m===l)contacto(rd,i,p,-1,0,l,c);else if(m===r)contacto(rd,i,p,1,0,r,c);else contacto(rd,i,p,0,1,d,c);
      }else{                             // seg y circ: cápsula
        let qx=c.x,qy=c.y;
        if(c.f==="seg"){const dx=c.x1-c.x0,dy=c.y1-c.y0,t=cl(((p.x-c.x0)*dx+(p.y-c.y0)*dy)/(dx*dx+dy*dy||1));qx=c.x0+dx*t;qy=c.y0+dy*t;}
        const ex=p.x-qx,ey=p.y-qy,d=Math.hypot(ex,ey),R=p.r+(c.r||0);if(d>=R)continue;
        const nx=d>1e-6?ex/d:0,ny=d>1e-6?ey/d:-1;contacto(rd,i,p,nx,ny,R-d,c);
      }
    }
  }
  function soporte(rd,x,y){              // la plataforma más alta que hay bajo (x, y): para levantarse encima de la mesa y no en el piso
    let best=null;
    for(const c of colsDe(rd.piso)){
      if(c.f!=="plat"&&c.f!=="caja"&&!(c.f==="seg"&&Math.abs(c.y1-c.y0)<2))continue;   // también un tubo horizontal: se pone de pie encima
      const x0=Math.min(c.x0,c.x1),x1=Math.max(c.x0,c.x1);if(x<x0+4*rd.s||x>x1-4*rd.s)continue;
      const yy=c.f==="caja"?c.y0:c.f==="seg"?c.y0-(c.r||0):c.y0+(c.y1-c.y0)*(x-c.x0)/(c.x1-c.x0);
      if(yy>=y-6*rd.s&&yy<rd.F-6*rd.s&&(best===null||yy<best))best=yy;
    }
    return best;
  }
  function puntoAsa(c,x,y){              // el punto del mueble más cercano a la mano
    if(c.f==="circ"){const dx=x-c.x,dy=y-c.y,d=Math.hypot(dx,dy)||1;return {x:c.x+dx/d*c.r,y:c.y+dy/d*c.r};}
    const y0=c.f==="caja"?c.y0:c.y0,y1=c.f==="caja"?c.y0:c.y1,dx=c.x1-c.x0,dy=y1-y0,t=cl(((x-c.x0)*dx+(y-y0)*dy)/(dx*dx+dy*dy||1));
    return {x:c.x0+dx*t,y:y0+dy*t-(c.f==="seg"?c.r||0:0)};
  }
  function buscaAsa(rd){                 // lo más cercano que se puede agarrar al caer: un mueble, un barandal u otro robot de otra escena
    let best=null;const S=rd.s,R=40*S;
    for(const i of [MI,MD]){
      const h=rd.P[i];
      for(const c of colsDe(rd.piso)){
        if(!c.asa&&c.f!=="asa")continue;const b=bbC(c);if(h.x<b[0]-R||h.x>b[2]+R||h.y<b[1]-R||h.y>b[3]+R)continue;
        const q=puntoAsa(c,h.x,h.y),d=Math.hypot(q.x-h.x,q.y-h.y);
        if(d<R&&(!best||d<best.d))best={i,d,x:q.x,y:q.y,c};
      }
      for(const sh of Shs)if(sh!==rd.show)for(const o of sh.rds){
        if(o.piso!==rd.piso)continue;
        for(const j of [MI,MD,PEC]){const q=o.P[j],d=Math.hypot(q.x-h.x,q.y-h.y);if(d<R&&(!best||d<best.d))best={i,d,x:q.x,y:q.y,o,j};}
      }
    }
    return best;
  }
  function agarra(rd,q){
    const S=rd.s;
    if(q.o)rd.fijo={i:q.i,o:q.o,j:q.j,L:2.5*S,hasta:ya+azar(500,1300)};
    else{const c=q.c,ox=q.x-(c.x??0),oy=q.y-(c.y??0);rd.fijo={i:q.i,c,pt:c.f==="circ"?()=>({x:c.x+ox,y:c.y+oy}):()=>({x:q.x,y:q.y}),L:1.5*S,hasta:ya+azar(450,1600)};}
    rd.agarrar=false;
    if(Math.random()<.45)dice(rd.show,rd,q.o?elige(["¡No me sueltes!","¡Agárrame!","¡Tú vienes conmigo!"]):elige(["¡Me agarro!","¡Aguanta, aguanta!","¡Te tengo, mueble!","¡No me suelto!"]));
  }

  // ---- un muñeco: nace con la pose de parado donde está el robot y con el control que tenía
  function nace(info,show,alto=0){
    const {E}=info,m=M(),u=m.ubica(E),s=m.K*info.esc,d=E.dir<0?-1:1,F=m.sue+3*m.K;
    const P=PARADO.map(([x,y],i)=>({x:u.px+x*s*d,y:F+y*s-alto,px:u.px+x*s*d,py:F+y*s-alto,r:RAD[i]*s,w:1/MASA[i]}));
    if(!(s>0&&isFinite(u.px)&&isFinite(F)&&isFinite(u.oy)))return null;   // el taller aún no se ha medido
    const rd={E,info,s,d,F,P,x0:u.px,piso:u.piso,oy:u.oy,lo:u.lo,hi:u.hi,techo:m.PCH?m.PCH+1:-1e9,AX:u.px,AY:0,k:new Array(7).fill(1),T:PARADO.map(()=>[0,0]),
      cara:"normal",boca:0,st:"quieto",st0:ya,show,golpeT:-1e9,fase:Math.random()*6,paso:0,bu:0,dSuelo:azar(900,1700),arma:null};
    E.trapo=rd;show.rds.push(rd);pose(rd,PARADO);rd.ign=ignora(rd);rd.ignT=ya;rd.fijo=null;rd.bal=null;
    if(info.anda)for(const p of P)p.px-=d*150*s*H;   // venía caminando: lleva su impulso
    return rd;
  }
  const ir=(rd,st)=>{rd.st=st;rd.st0=ya;};
  function encara(rd,d){                 // que mire al otro: el muñeco se refleja sobre su sitio y conserva su impulso
    if(d!==rd.d)for(const p of rd.P){const vx=p.x-p.px;p.x=2*rd.AX-p.x;p.px=p.x-vx;}
    rd.d=d;pose(rd,PARADO);
  }
  function pose(rd,L,hop=0){for(let i=0;i<7;i++){rd.T[i][0]=rd.AX+L[i][0]*rd.s*rd.d;rd.T[i][1]=rd.F+(L[i][1]+hop)*rd.s+rd.AY;}}
  function empuja(rd,i,vx,vy){const p=rd.P[i];p.px=p.x-vx*rd.s*H;p.py=p.y-vy*rd.s*H;}
  const empujaTodo=(rd,L)=>L.forEach(([vx,vy],i)=>empuja(rd,i,vx,vy));
  const quieto=rd=>rd.P.reduce((a,p)=>a+Math.abs(p.x-p.px)+Math.abs(p.y-p.py),0)<.05*rd.s;
  const dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
  const manoCerca=(rd,q)=>dist(rd.P[MI],q)<dist(rd.P[MD],q)?MI:MD;
  const liga=(sh,a,i,b,j,L)=>{sh.links.push({a,i,b,j,L});};
  const hoyoEn=(rd,x)=>hoyo?hoyo(rd.piso,x):null;          // {a, b, d}: un hoyo abierto en ese piso, en px del piso
  const sueloEn=(rd,x)=>{const h=hoyoEn(rd,x);return rd.F+(h?(h.trampa?60*rd.s:h.d):0);};   // la trampilla no tiene fondo: para la sombra y los reflejos, un suelo cercano
  const enPozo=rd=>{const h=hoyoEn(rd,rd.P[CAD].x);return h&&rd.P[CAD].y>rd.F+4*rd.s?h:null;};

  // ---- efectos: golpes con onomatopeya, polvo, estrellitas, corazones y lo que dicen
  function fx(sh,o){sh.fx.push({t0:ya,dur:700,...o});}
  function dice(sh,rd,txt){const h=rd.P[CAB],y=h.y-30*rd.s;fx(sh,{tipo:"dice",x:h.x,y:rd.info.token?Math.min(y,rd.F-112*M().K):y,txt,dur:1300});}   // Token lleva su letrero a 92 sobre el suelo: lo que dice va encima, no tapado
  function golpe(rd,x,v,y,txt){
    if(ya-rd.golpeT<380)return;
    rd.golpeT=ya;const sh=rd.show,fuerte=v>420*rd.s;
    suena(txt==="¡BONK!"?"bonk":"plaf",rd.info.tono);
    if(txt==="¡CLANG!")suena("clang");
    if(fuerte||!sh.unGolpe||txt){fx(sh,{tipo:"txt",x,y:(y??rd.F)-38*rd.s,txt:txt||elige(GOLPES),dur:900});sh.unGolpe=true;sh.sac=ya;}
    const yp=y??rd.F;
    for(let i=0;i<5;i++)fx(sh,{tipo:"polvo",x:x+azar(-10,10)*rd.s,y:yp-2*rd.s,vx:azar(-40,40)*rd.s,vy:azar(-30,-8)*rd.s,dur:azar(450,800)});
  }

  // ---- lo que hace cada muñeco: estado → objetivo y fuerza de los músculos
  function vive(rd){
    const s=(ya-rd.st0)/1000,st=rd.st,S=rd.s;
    rd.boca=0;
    if(st==="quieto"){pose(rd,PARADO);rd.k.fill(1);rd.cara="normal";}
    else if(st==="desmaya"){            // se apaga poco a poco: los músculos sueltan y la gravedad hace el resto
      pose(rd,PARADO);rd.k.fill(1-suave(s/.9));rd.cara="dormido";
      if(s>.35&&!rd.empujon){rd.empujon=true;empuja(rd,CAB,rd.d*40,0);}
      if(s>.9){rd.reflejo=null;ir(rd,"cae");}
    }
    else if(st==="cae"){
      rd.k.fill(0);rd.cara=rd.dormido?"dormido":"wow";rd.boca=rd.dormido?0:.8;
      const h=rd.P[CAD],dd=rd.caeDir||rd.d,fl=sueloEn(rd,h.x);
      if(rd.alcanza){const q=rd.alcanza();rd.T[MD]=[q.x,q.y];rd.T[MI]=[q.x,q.y];rd.k[MD]=.45;rd.k[MI]=.2;}
      else if(rd.reflejo==="suelo"&&s<1){rd.T[MI]=[h.x+dd*20*S,fl-3*S];rd.T[MD]=[h.x+dd*27*S,fl-3*S];rd.k[MI]=rd.k[MD]=.16;}
      else if(rd.reflejo==="aletea"&&s<1.4){const c=rd.P[PEC];rd.T[MI]=[c.x-(12+Math.sin(s*31)*5)*S,c.y-(13+Math.sin(s*23)*4)*S];rd.T[MD]=[c.x+(12+Math.sin(s*27+1)*5)*S,c.y-(13+Math.sin(s*29+2)*4)*S];rd.k[MI]=rd.k[MD]=.12;}   // manos arriba al alcance del brazo (≤ 21 desde el pecho): un blanco fuera de alcance lo impulsaba solo hacia arriba
      else if(rd.reflejo==="cabeza"&&s<1.8){const c=rd.P[CAB],a=Math.atan2(c.y-rd.P[PEC].y,c.x-rd.P[PEC].x);   // se protege la cabeza: una mano a cada lado del casco
        rd.T[MI]=[c.x+Math.cos(a+1.6)*13*S,c.y+Math.sin(a+1.6)*13*S];rd.T[MD]=[c.x+Math.cos(a-1.6)*13*S,c.y+Math.sin(a-1.6)*13*S];rd.k[MI]=rd.k[MD]=.3;rd.cara="apretado";rd.boca=0;}
      if(rd.agarrar===undefined)rd.agarrar=Math.random()<.6;   // Euphoria: al caer busca de qué agarrarse (mueble, barandal, otro robot)
      if(rd.fijo){
        const F0=rd.fijo,hm=rd.P[F0.i],q=F0.o?F0.o.P[F0.j]:F0.pt();
        if(ya>F0.hasta||Math.hypot(q.x-hm.x,q.y-hm.y)>9*S||(F0.o&&!Shs.includes(F0.o.show))){rd.fijo=null;rd.soltoT=ya;if(Math.random()<.35)dice(rd.show,rd,elige(["¡Me resbalo!","¡Uy!","Ya no aguanto…","¡Adióóós!"]));}
        else{rd.cara="apretado";rd.boca=0;}
      }else if(rd.agarrar&&!rd.alcanza&&s>.08&&s<1.7&&ya-(rd.soltoT||-1e9)>900){
        const q=buscaAsa(rd);
        if(q){if(q.d<6*S)agarra(rd,q);else if(q.d<28*S){rd.T[q.i]=[q.x,q.y];rd.k[q.i]=.2;}}
      }
      if(!rd.fijo&&((s>.6&&quieto(rd))||s>2.6))ir(rd,"suelo");
    }
    else if(st==="suelo"){
      rd.k.fill(0);rd.cara=rd.dormido?"dormido":s<.7?"apretado":"triste";
      if(rd.estira){const q=rd.estira(),i=manoCerca(rd,q);rd.T[i]=[q.x,q.y];rd.k[i]=.25;}
      const P0=enPozo(rd);
      if(P0&&P0.trampa){for(const p of rd.P){p.px-=cl((P0.a+P0.b)/2-p.x,-1,1)*40*S*H;}ir(rd,"cae");}   // atorado en el borde de la trampilla: se escurre hacia el hueco
      else if(!rd.espera&&s*1000>rd.dSuelo*(rd.dormido?1.6:1))levanta(rd);
    }
    else if(st==="rodillas"){
      pose(rd,RODILLAS);rd.k.fill(.04+.42*suave(s/.5));rd.cara="enfocado";
      if(s>.55)ir(rd,"arriba");
    }
    else if(st==="arriba"){
      pose(rd,PARADO);rd.k.fill(.46+.54*suave(s/.55));rd.cara="enfocado";
      if(s>.6)ir(rd,rd.pozo?"trepa":"listo");
    }
    else if(st==="trepa"){             // en el hoyo: brinca, se agarra del borde y sale hacia donde iba
      const P0=rd.pozo,sal=rd.sale||rd.d,bx=sal>0?P0.b+14*S:P0.a-14*S;
      if(s<.5){const q=suave(s/.5);rd.AY=P0.d*(1-q)-8*S*Math.sin(q*Math.PI);rd.d=sal;pose(rd,s<.25?TREPA:PARADO);rd.cara="apretado";if(!rd.upa){rd.upa=true;suena("upa",rd.info.tono);}}
      else{const q=suave((s-.5)/.35);rd.AX=rd.AX0+(bx-rd.AX0)*q;rd.AY=-10*S*Math.sin(q*Math.PI);pose(rd,PARADO,-Math.abs(Math.sin(q*Math.PI))*4);rd.cara="enfocado";}
      if(s<.5)rd.AX0=rd.AX;
      rd.k.fill(1);
      if(s>.88){rd.AY=0;rd.AX=bx;rd.pozo=null;ir(rd,"listo");if(Math.random()<.6){rd.dijo=true;dice(rd.show,rd,elige(["¡Salí!","Uf…","¿Quién puso eso ahí?","Otra vez no.","Sigo vivo."]));}}
    }
    else if(st==="listo"){             // se sacude y sigue como si nada
      pose(rd,PARADO);const a=Math.sin(s*20)*3.5*S*(1-cl(s/.7));rd.T[CAB][0]+=a;rd.k.fill(1);rd.cara=s<.35?"normal":"feliz";
      if(!rd.dijo&&s>.15){rd.dijo=true;if(Math.random()<.5)dice(rd.show,rd,elige(["No pasó nada.","Lo planeé.","¡Estoy bien!","Ups.","Nadie vio eso."]));}
      if(s>.75){
        if(rd.AY<-4*S){                // quedó encima de un mueble: se baja de un brinco por la orilla más cercana
          const c=colsDe(rd.piso).filter(c=>(c.f==="plat"||c.f==="caja"||c.f==="seg")&&rd.AX>=Math.min(c.x0,c.x1)-2&&rd.AX<=Math.max(c.x0,c.x1)+2),
            x0=c.length?Math.min(...c.map(c=>Math.min(c.x0,c.x1))):rd.AX,x1=c.length?Math.max(...c.map(c=>Math.max(c.x0,c.x1))):rd.AX,
            dd=rd.AX-x0<x1-rd.AX?-1:1,ob=(dd<0?x0-14*S:x1+14*S);
          rd.salto={h:16*S,dx:cl(ob,rd.lo+10*S,rd.hi-10*S)-rd.AX,dur:.5,x0:rd.AX,y0:rd.AY};rd.d=dd;rd.dijo=true;suena("salto",rd.info.tono);ir(rd,"salta");
          if(Math.random()<.4)dice(rd.show,rd,elige(["¡Abajo!","Con permiso.","¿Quién me subió aquí?","Bajando…"]));
        }else rd.fin=true;
      }
    }
    else if(st==="camina"){            // va a pie hacia rd.meta, con su paso de muñeco: piernas alternas y un saltito
      const dx=rd.meta-rd.AX,v=230*M().K*H*rd.ticks;
      rd.d=dx>0?1:dx<0?-1:rd.d;rd.AX+=Math.sign(dx)*Math.min(Math.abs(dx),v);rd.paso+=rd.ticks*H*16;
      const a=Math.sin(rd.paso)*7;pose(rd,PARADO,-Math.abs(Math.sin(rd.paso))*1.6);rd.T[PI][0]+=a*S*rd.d;rd.T[PD][0]-=a*S*rd.d;rd.T[MI][0]-=a*.6*S*rd.d;rd.T[MD][0]+=a*.6*S*rd.d;
      rd.k.fill(.95);rd.cara="normal";rd.llego=Math.abs(dx)<1;
    }
    else if(st==="agacha"||st==="sostiene"){   // le tiende la mano a otro: la mano de delante va a la suya
      pose(rd,st==="agacha"?AGACHA:PARADO);rd.k.fill(1);rd.cara="enfocado";
      if(rd.agarra){const q=rd.agarra();rd.T[MD]=[q.x,q.y];rd.k[MD]=.7;if(st==="sostiene")rd.T[CAB][0]+=rd.d*5*S;}
    }
    else if(st==="jala"){
      rd.AX=rd.AX0-rd.d*9*S*suave(s/.6);pose(rd,JALA);rd.k.fill(1);rd.cara="apretado";
      if(rd.agarra){const q=rd.agarra();rd.T[MD]=[q.x,q.y];rd.k[MD]=.3;}
    }
    else if(st==="baila"){
      const t=(ya-rd.show.bT)/1000,sw=Math.sin(t*3.6);
      rd.AX=rd.AX0+sw*6*S;pose(rd,PARADO,-Math.abs(Math.sin(t*7.2))*5);
      const o=rd.show.rds.find(x=>x!==rd),mx=(rd.P[MD].x+o.P[MD].x)/2;
      rd.T[MD]=[mx+sw*8*S,rd.F-(27+Math.sin(t*7.2)*4)*S];rd.T[MI]=[rd.AX-rd.d*12*S,rd.F-(44+Math.sin(t*9+rd.fase)*5)*S];rd.T[CAB][0]+=sw*4*S;
      rd.k.fill(.8);rd.cara="feliz";rd.boca=.3+.3*Math.abs(Math.sin(t*5));
    }
    else if(st==="guardia"){           // se planta: puños arriba, rebotando como boxeador, mirando al enemigo
      if(rd.mira)rd.d=rd.mira()>=rd.AX?1:-1;
      pose(rd,GUARDIA,-Math.abs(Math.sin(s*7+rd.fase))*1.6);rd.k.fill(1);rd.cara="apretado";
    }
    else if(st==="batea"){             // el golpe: la mano del arma barre de atrás-arriba a delante-abajo
      const q=suave(s/.17),a=-2.2+2.9*q;pose(rd,GUARDIA);const c=rd.T[PEC];
      rd.T[MD]=[c[0]+Math.cos(a)*21*S*rd.d,c[1]+Math.sin(a)*21*S];rd.T[CAB][0]+=rd.d*5*S*q;rd.T[CAD][0]+=rd.d*2*S*q;
      rd.k.fill(1);rd.k[MD]=.9;rd.cara="apretado";rd.boca=.6*(1-q);
      if(!rd.zas&&s>.05){rd.zas=true;suena("zas");}
      if(s>.5){rd.zas=false;ir(rd,rd.tras||"guardia");}
    }
    else if(st==="esquiva"){
      pose(rd,DUCK);rd.k.fill(1);rd.cara="wow";rd.boca=.7;
      if(s>.65)ir(rd,rd.tras||"guardia");
    }
    else if(st==="tambalea"){          // Euphoria: equilibrio activo. El centro de masa contra la base de los pies; si se sale, paso de recuperación
      const B=rd.bal,P=rd.P;               // hacia donde se cae, el torso se inclina al revés y los brazos se abren; si no alcanza, se cae
      let mx=0,vx=0,mt=0;for(let i=0;i<7;i++){mx+=P[i].x*MASA[i];vx+=(P[i].x-P[i].px)*MASA[i];mt+=MASA[i];}
      mx/=mt;vx=vx/mt/H;
      const c=mx-rd.AX,cap=c+vx*.2,base=7*S,fuera=Math.abs(cap)/base;   // «capture point»: dónde quedaría el peso si no hace nada
      if(B.paso){const q=cl((ya-B.paso.t0)/170);rd.AX=B.paso.x0+B.paso.dx*suave(q);if(q>=1){B.paso=null;suena("paso",rd.info.tono);}}
      else if(fuera>1&&B.pasos<B.max&&s>.05){B.paso={t0:ya,x0:rd.AX,dx:cl(cap*1.1,-24*S,24*S),pie:Math.sign(cap)===rd.d?PD:PI,quedo:null};B.pasos++;
        const j=B.paso.pie===PI?PD:PI;B.paso.quedo=[P[j].x,rd.F+PARADO[j][1]*S+rd.AY];}
      pose(rd,PARADO);
      if(B.paso){const q=cl((ya-B.paso.t0)/170);rd.T[B.paso.pie][1]-=8*S*Math.sin(q*Math.PI);rd.T[B.paso.pie===PI?PD:PI]=B.paso.quedo;}
      const lean=cl(-cap/(2.5*base),-1,1),pc=rd.T[PEC],w=s*(12+rd.fase),amp=cl(fuera,0,1.4);
      rd.T[CAB][0]+=lean*8*S;rd.T[PEC][0]+=lean*3.5*S;rd.T[CAD][0]-=lean*2*S;
      rd.T[MI]=[pc[0]-(14+3*amp)*S+Math.sin(w)*4*S*amp,pc[1]-(3+9*amp)*S-Math.cos(w*1.3)*5*S*amp];   // los brazos abiertos, como molinos si va muy mal
      rd.T[MD]=[pc[0]+(14+3*amp)*S+Math.sin(w+2)*4*S*amp,pc[1]-(3+9*amp)*S-Math.cos(w*1.3+1.4)*5*S*amp];
      const gan=suave(s/1.2);rd.k.fill(.025+.6*gan);rd.k[PI]=rd.k[PD]=.9;rd.k[MI]=rd.k[MD]=.3;if(B.paso)rd.k[B.paso.pie]=.55;
      rd.cara=fuera>.8?"wow":"apretado";rd.boca=fuera>.8?.55:0;
      if(Math.abs(c)>3.2*base||(B.pasos>=B.max&&!B.paso&&fuera>1.5)||s>3.2||hoyoEn(rd,rd.AX)){   // no alcanzó: ahora sí se cae, hacia donde iba el peso
        const dd=Math.sign(cap)||rd.d;rd.caeDir=dd;rd.k.fill(0);rd.reflejo=elige(["suelo","suelo","cabeza","aletea"]);
        empuja(rd,CAB,dd*120+(P[CAB].x-P[CAB].px)/H/S,(P[CAB].y-P[CAB].py)/H/S);empuja(rd,PEC,dd*80+(P[PEC].x-P[PEC].px)/H/S,0);
        if(!rd.dormido)suena("uy",rd.info.tono);rd.bal=null;ir(rd,"cae");
      }
      else if(!B.paso&&fuera<.55&&s>.35){B.ok+=rd.ticks*H;if(B.ok>.3){rd.bal=null;rd.dijo=Math.random()<.65;if(rd.dijo)dice(rd.show,rd,elige(["¡Uf, casi!","Equilibrio perfecto.","No me caí. Nadie diga nada.","Todo bajo control.","¡Ni me moví!","Ups… ¡pero no!"]));ir(rd,"listo");}}
      else B.ok=0;
    }
    else if(st==="salta"){             // brinco de verdad (barril, caja, acantilado corto): sube, encoge las piernas y cae de pie
      const J=rd.salto,q=cl(s/J.dur);
      rd.AX=J.x0+J.dx*q;rd.AY=(J.y0||0)*(1-q*q)-J.h*Math.sin(q*Math.PI);
      pose(rd,PARADO);const enc=Math.sin(q*Math.PI);rd.T[PI][1]-=8*S*enc;rd.T[PD][1]-=10*S*enc;rd.T[PI][0]-=3*S*rd.d*enc;rd.T[MI][1]-=14*S*enc;rd.T[MD][1]-=18*S*enc;
      rd.k.fill(1);rd.cara=q<.5?"wow":"feliz";
      if(q>=1){rd.AY=0;ir(rd,"listo");if(!rd.dijo&&Math.random()<.55){rd.dijo=true;dice(rd.show,rd,elige(["¡Ja!","Fácil.","¡Hop!","¿Eso es todo?","Ni me tocó."]));}}
    }
  }
  function levanta(rd){                  // se levanta hacia donde quedó la cabeza: primero de rodillas, luego de pie. En un hoyo, después trepa
    const h=rd.P[CAD],c=rd.P[CAB],P0x=enPozo(rd),P0=P0x&&!P0x.trampa?P0x:null;
    rd.d=c.x>=h.x?1:-1;rd.alcanza=rd.estira=null;rd.dormido=false;rd.fijo=null;rd.bal=null;
    const sp=P0?null:soporte(rd,h.x,h.y);  // cayó encima de una mesa, una caja o la rampa: se levanta ahí arriba
    if(P0){rd.pozo=P0;rd.AY=P0.d;rd.AX=cl(h.x,P0.a+10*rd.s,P0.b-10*rd.s);rd.sale=rd.sale||rd.caeDir||rd.d;}
    else{rd.pozo=null;rd.AY=sp!==null&&rd.F-sp<150*rd.s?sp-rd.F:0;rd.AX=cl(h.x,rd.lo+10*rd.s,rd.hi-10*rd.s);}
    suena("upa",rd.info.tono);ir(rd,"rodillas");
  }
  function tambalea(rd,vx,o={}){         // un golpe leve: no se cae de una vez, primero pelea por el equilibrio (y a veces gana)
    const dd=Math.sign(vx)||rd.d;
    rd.bal={pasos:0,ok:0,paso:null,max:o.pasos??elige([1,2,2,3,3,4])};rd.fijo=null;rd.caeDir=dd;
    rd.k.fill(.025);rd.k[PI]=rd.k[PD]=.9;
    empujaTodo(rd,[[vx*1.15,-25],[vx,-12],[vx*.5,0],[vx*1.2,-30],[vx*1.2,-30],[0,0],[0,0]]);
    suena("uy",(rd.info.tono||900)*1.3);ir(rd,"tambalea");
  }
  const dePie=rd=>["quieto","listo","guardia","batea","esquiva","tambalea","camina","sostiene","agacha","jala"].includes(rd.st);
  function cae(rd,modo,dd=rd.d){         // el tropiezo de verdad: músculos a cero y un empujón según cómo se cae
    if(modo==="tropiezo"&&!rd.trip&&Math.random()<.45&&dePie(rd)){rd.trip=true;tambalea(rd,dd*azar(170,260),{pasos:elige([1,2,3])});return;}   // tropezar no siempre es caer: unos pasitos y a veces se salva
    rd.caeDir=dd;rd.k.fill(0);rd.bal=null;
    if(modo==="tropiezo"){rd.reflejo="suelo";empujaTodo(rd,[[dd*240,-110],[dd*175,-90],[dd*60,-60],[dd*210,-150],[dd*210,-150],[-dd*90,-40],[-dd*90,-40]]);}
    else if(modo==="resbalon"){rd.reflejo="aletea";empujaTodo(rd,[[-dd*130,-20],[-dd*40,-40],[dd*90,-170],[-dd*60,-260],[dd*60,-260],[dd*330,-270],[dd*300,-250]]);}
    else if(modo==="suave"){rd.reflejo="suelo";empujaTodo(rd,[[dd*120,-40],[dd*80,-30],[dd*20,-10],[dd*90,-40],[dd*90,-40],[0,0],[0,0]]);}
    if(modo==="desmayo"){rd.dormido=true;ir(rd,"desmaya");return;}
    if(!rd.dormido)suena("uy",rd.info.tono);
    ir(rd,"cae");
  }
  function lanzaRd(rd,vx,vy,o={}){       // un golpe con dirección (barril, enemigo, resorte, viento): lo de arriba sale más rápido, así da la vuelta
    if(!o.aplasta&&o.aguanta!==0&&Math.abs(vx)<380&&vy>-300&&dePie(rd)&&rd.st!=="tambalea"&&Math.random()<(o.aguanta??.6)){tambalea(rd,vx*.8);return;}   // un golpe leve se aguanta
    rd.caeDir=Math.sign(vx)||rd.d;rd.k.fill(0);rd.bal=null;rd.fijo=null;rd.agarrar=undefined;rd.reflejo=o.reflejo!==undefined?o.reflejo:elige(["suelo","aletea","aletea","cabeza",null]);
    const giro=o.giro??1;
    rd.P.forEach((p,i)=>{const hf=-PARADO[i][1]/45;empuja(rd,i,vx*(1+giro*(hf-.5)*.9)*azar(.85,1.15),vy*azar(.88,1.12)*(i>=PI?.82:1)+(o.aplasta&&i===CAB?vy*.4:0));});
    if(!rd.dormido)suena("uy",rd.info.tono);
    rd.pozo=null;rd.AY=0;rd.dijo=false;rd.fin=false;rd.alcanza=rd.estira=null;
    ir(rd,"cae");
  }

  // ---- las escenas: quién participa, cómo empieza y qué pasa entre ellos
  const TXT={tropiezo:n=>`${n} se tropezó`,resbalon:n=>`${n} se resbaló`,desmayo:n=>`${n} se quedó dormido de pie`,
    tambalea:n=>`${n} pierde el equilibrio`,choque:(n,o)=>`${n} chocó con ${o}`,cadena:(n,o)=>`${o} atrapó a ${n}`,domino:(n,o)=>`${n} se llevó a ${o}`,ayuda:(n,o)=>`${o} ayuda a ${n}`,pie:(n,o)=>`${n} le agarró el pie a ${o}`,manos:(n,o)=>`${n} y ${o} · a bailar`};
  const Nom=x=>x.nom[0].toUpperCase()+x.nom.slice(1);
  const nuevaSh=(tipo,o={})=>({tipo,rds:[],links:[],fx:[],ini:ya,sac:-1e9,foco:false,zoom:o.zoom||1.85,bT:0,acc:0,lento:1,lentoT:-1e9,max:o.max||16000,quiet:!!o.quiet});
  function activa(sh,txt,o={}){           // la escena entra al taller; la cámara solo la sigue si no hay otra y se ve o toca
    Shs.push(sh);
    const c=centro(sh),vis=c&&M().visto?M().visto(c.x,c.y,-60):true;
    if(o.foco!==false&&!Shs.some(x=>x.foco)&&ya-ultFoco>(o.cool??7000)&&(vis||Math.random()<(o.lejos??.3))){
      sh.foco=true;ultFoco=ya;
      if(Taller.dirActivo()){const z=M().zSigue;Taller.hecho(o.k||"trapo",7,{suj:()=>centro(sh)||{x:0,y:0},z0:z*sh.zoom*.85,z1:z*sh.zoom,min:2600,dur:o.dur||9000,cool:o.dirCool||5000,sac:o.sac??1,rot:o.rot??.025,piso:sh.rds[0].piso,txt,vive:()=>Shs.includes(sh)});}
    }
    if(sh.foco&&o.lento!==false){sh.lento=.38;sh.lentoT=ya;}
  }
  function escena(tipo,a,b){
    const sh=nuevaSh(tipo,{zoom:tipo==="manos"?1.6:1.85});
    const A=nace(a,sh),B=b?nace(b,sh):null;
    if(!A||(b&&!B)){for(const rd of sh.rds)rd.E.trapo=null;return null;}
    if(B){const dd=A.P[CAD].x<=B.P[CAD].x?1:-1;encara(A,dd);encara(B,-dd);}
    if(tipo==="tropiezo"||tipo==="resbalon"||tipo==="desmayo")cae(A,tipo);
    else if(tipo==="tambalea")tambalea(A,(Math.random()<.5?-1:1)*azar(160,340));
    else if(tipo==="choque"){A.meta=B.AX;ir(A,"camina");A.prisa=true;}
    else if(tipo==="cadena"||tipo==="domino"){
      cae(A,"tropiezo",A.d);A.reflejo=null;A.alcanza=()=>B.P[MD];
      B.agarra=()=>A.P[MD];ir(B,"sostiene");
    }
    else if(tipo==="ayuda"||tipo==="pie"){cae(A,Math.random()<.5?"tropiezo":"resbalon");A.espera=true;ir(B,"quieto");}
    else if(tipo==="manos"){
      const mx=(A.AX+B.AX)/2;A.meta=mx-A.d*14*A.s;B.meta=mx+A.d*14*B.s;ir(A,"camina");ir(B,"camina");
    }
    activa(sh,TXT[tipo](Nom(a),b?Nom(b):""),{sac:tipo==="manos"?0:1,rot:tipo==="manos"?0:.025,k:tipo==="manos"?"manos":"trapo",lento:tipo!=="manos"});
    return sh;
  }
  function dirige(sh){                   // lo que une a los dos de cada escena
    const [A,B]=sh.rds,f=(ya-sh.ini)/1000;
    if(sh.tipo==="cadena"||sh.tipo==="domino"){
      if(!sh.agarre){
        if(dist(A.P[MD],B.P[MD])<8*A.s){sh.agarre=ya;liga(sh,A,MD,B,MD,2*A.s);A.alcanza=null;B.agarra=null;
          if(sh.foco){sh.lento=.4;sh.lentoT=ya;}
          if(sh.tipo==="cadena"){dice(sh,B,elige(["¡Te tengo!","¡Cuidado!","¡Upa!"]));levanta(A);A.st="arriba";B.AX0=B.AX;ir(B,"jala");}
          else dice(sh,B,elige(["¡Nooo!","¡Suelta!","¡Ay, ay, ay!"]));}
        else if(f>.75&&A.st==="cae"){A.alcanza=null;A.reflejo="suelo";B.agarra=null;ir(B,"listo");B.dijo=true;dice(sh,B,"Casi…");sh.tipo="tropiezo";}
      }else if(sh.tipo==="domino"){
        if(B.st==="sostiene"&&ya-sh.agarre>260){B.agarra=null;cae(B,"suave",B.d);}
        if(A.st==="suelo"&&B.st==="suelo")sh.links=[];
      }else{
        if(A.st==="listo"&&B.st==="jala"){sh.links=[];ir(B,"listo");B.dijo=true;fx(sh,{tipo:"corazon",x:(A.P[CAB].x+B.P[CAB].x)/2,y:A.P[CAB].y-24*A.s,dur:1400});}
      }
    }
    else if(sh.tipo==="ayuda"||sh.tipo==="pie"){
      if(A.st==="suelo"&&!sh.va){       // el otro va hacia el caído
        sh.va=true;B.d=A.P[CAD].x>B.AX?1:-1;
        B.meta=sh.tipo==="pie"?A.P[CAD].x+B.d*48*A.s:A.P[CAD].x-B.d*24*B.s;B.meta=cl(B.meta,B.lo+12*B.s,B.hi-12*B.s);ir(B,"camina");
        if(sh.tipo==="ayuda")dice(sh,B,elige(["¡Voy!","¿Estás bien?","Aguanta…"]));
      }
      if(sh.tipo==="pie"&&B.st==="camina"&&!sh.agarre){
        const i=manoCerca(A,B.P[PI]);
        if(Math.abs(A.P[i].x-B.P[PI].x)<12*A.s){sh.agarre=ya;liga(sh,A,i,B,PI,3*A.s);dice(sh,A,elige(["¡Je je!","¡Te tengo!","Tú también."]));cae(B,"tropiezo",B.d);B.reflejo="suelo";}
        else if(B.llego){sh.agarre=ya;cae(B,"tropiezo",B.d);}
      }
      if(sh.tipo==="pie"&&sh.agarre&&ya-sh.agarre>450){sh.links=[];A.espera=false;}
      if(sh.tipo==="ayuda"&&B.st==="camina"&&B.llego){B.agarra=()=>A.P[manoCerca(A,B.P[MD])];A.estira=()=>B.P[MD];ir(B,"agacha");}
      if(sh.tipo==="ayuda"&&B.st==="agacha"&&!sh.agarre){
        const i=manoCerca(A,B.P[MD]);
        if(dist(A.P[i],B.P[MD])<8*A.s){sh.agarre=ya;liga(sh,A,i,B,MD,2*A.s);A.espera=false;A.estira=null;levanta(A);A.d=-B.d;B.agarra=null;B.AX0=B.AX;ir(B,"jala");}
        else if(ya-B.st0>1500){A.espera=false;A.estira=null;ir(B,"listo");}
      }
      if(sh.tipo==="ayuda"&&A.st==="listo"&&B.st==="jala"){sh.links=[];ir(B,"listo");B.dijo=true;fx(sh,{tipo:"corazon",x:(A.P[CAB].x+B.P[CAB].x)/2,y:A.P[CAB].y-24*A.s,dur:1400});}
      if(B.st==="quieto"&&f>6)A.espera=false;
    }
    else if(sh.tipo==="choque"){        // va distraído y se estrella con el otro: los dos pelean por el equilibrio
      if(A.st==="camina"&&Math.abs(A.AX-B.AX)<24*A.s){
        const d=Math.sign(B.AX-A.AX)||A.d;golpe(B,(A.AX+B.AX)/2,300*A.s,B.F,"¡PUM!");
        tambalea(B,d*azar(230,380));tambalea(A,-d*azar(120,220));
        if(Math.random()<.6)dice(sh,B,elige(["¡Fíjate!","¿¡Y tú de dónde saliste!?","¡Mi café!","¡Oye!"]));
      }
      else if(A.st==="camina"&&f>6){ir(A,"listo");ir(B,"listo");}
      if(A.st==="quieto"&&B.st==="quieto"&&f>1){A.fin=B.fin=true;}
    }
    else if(sh.tipo==="manos"){
      if(A.st==="camina"&&B.st==="camina"&&A.llego&&B.llego){
        A.d=B.AX>=A.AX?1:-1;B.d=-A.d;A.AX0=A.AX;B.AX0=B.AX;sh.bT=ya;liga(sh,A,MD,B,MD,3*A.s);ir(A,"baila");ir(B,"baila");suena("baile",1100);
      }
      if(f>4&&(A.st!=="baila"||B.st!=="baila")&&!sh.bT){A.meta=A.AX;B.meta=B.AX;}   // atorados: que bailen donde estén
      if(A.st==="baila"){
        const t=(ya-sh.bT)/1000;
        if(Math.random()<.04)fx(sh,{tipo:"corazon",x:(A.P[CAB].x+B.P[CAB].x)/2+azar(-14,14)*A.s,y:A.P[CAB].y-20*A.s,dur:1200});
        if(t>4.2){
          if(Math.random()<.3){dice(sh,A,"¡Uy!");cae(A,"suave",A.d);cae(B,"suave",B.d);}   // a veces se enredan y caen juntos
          else{sh.links=[];ir(A,"listo");ir(B,"listo");A.dijo=B.dijo=true;}
        }
      }
      if(A.st==="suelo"&&B.st==="suelo")sh.links=[];
    }
  }
  const centro=sh=>{
    if(!sh.rds.length)return null;
    let x=0,y=0;for(const rd of sh.rds){x+=rd.P[CAD].x;y+=rd.oy+rd.P[CAD].y-14*rd.s;}
    return {x:x/sh.rds.length,y:y/sh.rds.length};
  };
  function termina(sh){                  // el robot vuelve a ser dibujo: desde donde quedó y mirando hacia donde quedó
    for(const rd of sh.rds){
      rd.E.trapo=null;
      let x=rd.P[CAD].x;x=isFinite(x)?x:rd.x0;
      const P0=hoyoEn(rd,x);if(P0)x=(rd.sale||rd.d)>0?P0.b+14*rd.s:P0.a-14*rd.s;   // nunca se queda flotando sobre un hoyo
      Taller.ponX(rd.E,cl(x,rd.lo,rd.hi),rd.piso,rd.d);
      if(rd.alQuitar)try{rd.alQuitar();}catch(e){}
    }
    const i=Shs.indexOf(sh);if(i>=0)Shs.splice(i,1);
    if(sh.foco)ultFoco=ya;
  }

  // ---- la física: Verlet a paso fijo con músculos, huesos, agarres, suelo con hoyos, paredes y techo
  function fisica(sh,n){
    const L=sh.rds,Mm=M();
    let C=L.map(rd=>colsDe(rd.piso));
    for(let it=0;it<n;it++){
      for(const rd of L){
        const G=GRAV*rd.s*H*H;
        for(const p of rd.P){const vx=(p.x-p.px)*.996,vy=(p.y-p.py)*.996;p.px=p.x;p.py=p.y;p.x+=vx;p.y+=vy+G;}
        for(let i=0;i<7;i++){const k=rd.k[i];if(!k)continue;const p=rd.P[i],[tx,ty]=rd.T[i],c=1-Math.exp(-H*42*k);p.x+=(tx-p.x)*c;p.y+=(ty-p.y)*c;p.px+=(p.x-p.px)*k*.28;p.py+=(p.y-p.py)*k*.28;}
      }
      for(let r=0;r<4;r++){
        for(const rd of L)for(const [a,b,lo,hi] of HUESOS)hueso(rd.P[a],rd.P[b],lo*rd.s,hi*rd.s);
        for(const l of sh.links)hueso(l.a.P[l.i],l.b.P[l.j],0,l.L);
        for(const rd of L)if(rd.fijo){    // agarrado: de un mueble (punto fijo, pesa infinito) o de otro robot (se reparten el tirón)
          const F0=rd.fijo,hm=rd.P[F0.i];
          if(F0.o)hueso(hm,F0.o.P[F0.j],0,F0.L);
          else{const q=F0.pt(),dx=q.x-hm.x,dy=q.y-hm.y,d=Math.hypot(dx,dy);if(d>F0.L){const f=1-F0.L/d;hm.x+=dx*f;hm.y+=dy*f;if(F0.c.on&&r===3)F0.c.on((hm.x-hm.px)/H*.3,(hm.y-hm.py)/H*.3);}}
        }
      }
      for(let ri=0;ri<L.length;ri++)for(let i=0;i<7;i++){
        const rd=L[ri],p=rd.P[i];
        const P0=hoyo?hoyo(rd.piso,p.px):null,dentro=P0&&p.py+p.r>rd.F+1;   // venía por debajo del suelo: está en el hoyo, sus paredes lo detienen
        if(dentro){
          if(p.x-p.r<P0.a){if(i<=CAD&&Math.abs(p.x-p.px)/H>260*rd.s)golpe(rd,P0.a,Math.abs(p.x-p.px)/H,p.y);p.x=P0.a+p.r;p.px=p.x;}
          if(p.x+p.r>P0.b){if(i<=CAD&&Math.abs(p.x-p.px)/H>260*rd.s)golpe(rd,P0.b,Math.abs(p.x-p.px)/H,p.y);p.x=P0.b-p.r;p.px=p.x;}
        }
        const Px=dentro?P0:hoyo?hoyo(rd.piso,p.x):null,fl=rd.F+(Px&&p.x>Px.a&&p.x<Px.b?Px.d:0);
        if(p.y+p.r>fl){
          const v=(p.y-p.py)/H;
          if(i<=CAD&&v>230*rd.s&&rd.k[i]<.5)golpe(rd,p.x,v,fl);
          p.y=fl-p.r;p.py=p.y+Math.max(0,v)*H*.18;   // casi sin rebote
          p.px+=(p.x-p.px)*(rd.k[i]>.5?.5:.14);                         // rozamiento: los pies parados no patinan
        }
        if(p.y-p.r<rd.techo&&!(rd.sinTecho&&ya<rd.sinTecho.hasta&&p.x>rd.sinTecho.a&&p.x<rd.sinTecho.b)){   // el techo: el que sale volando se da en la cabeza (salvo por la trampilla por la que acaba de caer)
          const v=(p.y-p.py)/H;
          if(i<=CAD&&v<-260*rd.s)golpe(rd,p.x,-v,rd.techo+46*rd.s,"¡BONK!");
          p.y=rd.techo+p.r;p.py=p.y+v*.3*H;
        }
        if(p.x-p.r<rd.lo){if(i<=CAD&&(p.px-p.x)/H>320*rd.s)golpe(rd,rd.lo,(p.px-p.x)/H,p.y);p.x=rd.lo+p.r;p.px=p.x;}
        if(p.x+p.r>rd.hi){if(i<=CAD&&(p.x-p.px)/H>320*rd.s)golpe(rd,rd.hi,(p.x-p.px)/H,p.y);p.x=rd.hi-p.r;p.px=p.x;}
        if(C[ri].length&&!NOCOL.has(rd.st))choca(rd,i,p,C[ri]);
      }
      for(let ri=0;ri<L.length;ri++)if(L[ri].P[CAD].y>Mm.H&&bajaPiso(L[ri],Mm))C[ri]=colsDe(L[ri].piso);
    }
  }
  function bajaPiso(rd,m){               // cayó por la trampilla: pasa al piso de abajo (sus 7 puntos cambian de marco) y ahí sigue rebotando
    const p=rd.piso;if(p<=0)return false;
    const paso=m.pisoY(p-1)-m.pisoY(p);if(!(rd.P[CAD].y>paso+m.PCH+10*rd.s))return false;
    const P0=hoyo?hoyo(p,rd.P[CAD].x):null,a=P0?P0.a:rd.P[CAD].x-30*rd.s,b=P0?P0.b:rd.P[CAD].x+30*rd.s;
    for(const q of rd.P){q.y-=paso;q.py-=paso;}
    for(const t of rd.T)t[1]-=paso;
    rd.piso=p-1;rd.oy=m.pisoY(p-1);rd.sinTecho={a:a-10*rd.s,b:b+10*rd.s,hasta:ya+1600};rd.st0=ya;rd.ign=new Set();rd.fijo=null;rd.pozo=null;rd.AY=0;
    rd.bajo=(rd.bajo||0)+1;
    const sh=rd.show;sh.links=sh.links.filter(l=>l.a!==rd&&l.b!==rd);sh.max=Math.max(sh.max,ya-sh.ini+14000);
    Taller.ponX(rd.E,rd.P[CAD].x,rd.piso,rd.d);rd.E.oy=null;
    if(rd.st!=="cae"){rd.k.fill(0);ir(rd,"cae");}
    if(Math.random()<.55)dice(sh,rd,elige(["¡Piso de abajo!","¿¡Por qué hay una trampilla!?","¡Aaaaah!","¡Atajo!","¡Ahí voy!"]));
    return true;
  }
  function hueso(a,b,lo,hi){
    const dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1e-6,L=d<lo?lo:d>hi?hi:d;
    if(L===d)return;
    const f=(d-L)/d/(a.w+b.w);a.x+=dx*f*a.w;a.y+=dy*f*a.w;b.x-=dx*f*b.w;b.y-=dy*f*b.w;
  }

  // ---- cada cuadro: decidir si alguien se cae, mover las escenas y la física
  const libre=x=>!x.E.via&&!x.E.trapo&&!enUso(x.E);
  function candidatos(L,tipo){
    const m=M(),ok=L.filter(libre),u=new Map(ok.map(x=>[x,m.ubica(x.E)]));
    const pares=[];for(const a of ok)for(const b of ok)if(a!==b&&u.get(a).piso===u.get(b).piso){const d=Math.abs(u.get(a).px-u.get(b).px);pares.push({a,b,d});}
    const op=[],cerca=pares.filter(p=>p.d>18*m.K&&p.d<70*m.K),medio=pares.filter(p=>p.d>40*m.K&&p.d<360*m.K),quietos=pares.filter(p=>!p.a.anda&&!p.b.anda&&p.d>30*m.K&&p.d<300*m.K);
    const andan=ok.filter(x=>x.anda);
    if(andan.length){op.push(["tropiezo",3,()=>[elige(andan)]]);op.push(["resbalon",2,()=>[elige(andan)]]);}
    if(ok.length)op.push(["tambalea",3,()=>[elige(ok)]]);
    if(medio.length)op.push(["choque",2,()=>{const p=elige(medio);return [p.a,p.b];}]);
    if(ok.length)op.push(["desmayo",1,()=>[elige(ok.filter(x=>!x.anda).length?ok.filter(x=>!x.anda):ok)]]);
    if(cerca.length){op.push(["cadena",3,()=>{const p=elige(cerca);return [p.a,p.b];}]);op.push(["domino",2,()=>{const p=elige(cerca);return [p.a,p.b];}]);}
    if(medio.length){op.push(["ayuda",3,()=>{const p=elige(medio);return [p.a,p.b];}]);op.push(["pie",2,()=>{const p=elige(medio);return [p.a,p.b];}]);}
    if(quietos.length)op.push(["manos",3,()=>{const p=elige(quietos);return [p.a,p.b];}]);
    if(!ok.length)return null;
    if(tipo){                           // a prueba: si no hay pareja cerca, la que se pueda
      const o=op.find(x=>x[0]===tipo);if(o)return [o[0],...o[2]()];
      if(["tropiezo","resbalon","desmayo","tambalea"].includes(tipo))return [tipo,elige(ok)];
      if(ok.length>1){const a=ok[0],b=ok.find(x=>x!==a&&u.get(x).piso===u.get(a).piso);if(b)return [tipo,a,b];}
      return ["tropiezo",elige(ok)];
    }
    let tot=op.reduce((s,o)=>s+o[1],0),r=Math.random()*tot;
    for(const o of op){r-=o[1];if(r<=0)return [o[0],...o[2]()];}
    return null;
  }
  function lanza(L,tipo){const c=candidatos(L,tipo);return !!(c&&escena(c[0],c[1],c[2]));}

  Cap.trapoPaso=(t,dt)=>{
    ya=t;
    const L=Taller.entidades(),vivos=new Set(L.map(x=>x.E));
    for(const sh of [...Shs])if(sh.rds.some(rd=>!vivos.has(rd.E))||ya-sh.ini>sh.max)termina(sh);   // alguien se fue (o algo se atoró): vuelven a la normalidad
    if(!prox)prox=t+azar(14000,26000);
    if(Shs.length<2&&t>=prox){prox=t+azar(...cadaMs);if(!lanza(L))prox=t+5000;}
    for(const sh of [...Shs]){
      const q=(ya-sh.lentoT)/1000;sh.lento=q<.5?Math.min(sh.lento,.4):q<.8?.4+.6*(q-.5)/.3:1;
      sh.acc+=Math.min(dt,50)/1000*sh.lento;
      const n=Math.min(9,Math.floor(sh.acc*HZ));sh.acc-=n*H;
      for(const rd of sh.rds){rd.ticks=n;vive(rd);}
      if(sh.dirige)sh.dirige(sh);else dirige(sh);
      if(n)fisica(sh,n);
      for(const rd of sh.rds)if(rd.P.some(p=>!isFinite(p.x+p.y+p.px+p.py))){rd.AX=rd.x0;rd.AY=0;rd.pozo=null;pose(rd,PARADO);rd.P.forEach((p,i)=>{p.x=p.px=rd.T[i][0];p.y=p.py=rd.T[i][1];});rd.fin=true;}   // si la física se rompe: de pie en su sitio y fuera
      for(const rd of sh.rds){const c=rd.P[CAB];rd.bu+=((cl(-(c.x-c.px)/H/rd.s*.012,-4,4))-rd.bu)*.2;
        if(rd.ign&&rd.ign.size&&ya-rd.ignT>250){rd.ignT=ya;const C=colsDe(rd.piso);for(const id of [...rd.ign]){const c=C.find(c=>c.id===id);if(!c||!encima(rd,c))rd.ign.delete(id);}}}   // lo que tenía encima al nacer vuelve a chocar en cuanto se separa
      sh.fx=sh.fx.filter(f=>ya-f.t0<f.dur);
      if(sh.rds.every(rd=>rd.fin))termina(sh);
    }
    try{cruza();atropella(L);}catch(e){console.warn("trapo",e);}
  };
  // ---- Euphoria entre escenas: los muñecos de escenas distintas chocan entre sí, y el que sale volando tumba (o hace tambalear) al que está de pie
  const GRANDES=[CAB,PEC,CAD];
  function cruza(){
    if(Shs.length<2)return;
    const R=[];for(const sh of Shs)for(const rd of sh.rds)R.push(rd);
    for(let a=0;a<R.length;a++)for(let b=a+1;b<R.length;b++){
      const A=R[a],B=R[b];if(A.show===B.show||A.piso!==B.piso||Math.abs(A.P[CAD].x-B.P[CAD].x)>80*A.s)continue;
      let fuerte=0,nx0=0;
      for(const i of GRANDES)for(const j of GRANDES){
        const p=A.P[i],q=B.P[j],dx=q.x-p.x,dy=q.y-p.y,d=Math.hypot(dx,dy),R0=p.r+q.r;
        if(d>=R0||d<1e-6)continue;
        const nx=dx/d,ny=dy/d,pen=R0-d,wa=p.w/(p.w+q.w),wb=1-wa;
        p.x-=nx*pen*wa;p.y-=ny*pen*wa;q.x+=nx*pen*wb;q.y+=ny*pen*wb;
        const rv=((q.x-q.px)-(p.x-p.px))*nx+((q.y-q.py)-(p.y-p.py))*ny;
        if(rv<0){const J=-rv*1.3;p.px+=nx*J*wa;p.py+=ny*J*wa;q.px-=nx*J*wb;q.py-=ny*J*wb;const v=-rv/H;if(v>fuerte){fuerte=v;nx0=nx;}}
      }
      if(fuerte>170*A.s){
        golpe(A,(A.P[PEC].x+B.P[PEC].x)/2,fuerte,Math.min(A.P[PEC].y,B.P[PEC].y)+30*A.s,fuerte>380*A.s?"¡CHOCAN!":null);
        for(const [X,sg] of [[A,-1],[B,1]])if(dePie(X)&&X.st!=="tambalea"&&ya-X.st0>200){
          if(fuerte<420*X.s&&Math.random()<.7)tambalea(X,sg*nx0*fuerte*.55/X.s);else lanzaRd(X,sg*nx0*fuerte*.7/X.s,-azar(120,240),{aguanta:0});
        }
      }
    }
  }
  function atropella(L){                 // uno que vuela contra uno que trabaja (sin escena): lo empuja y entra al juego
    if(Shs.length>=MAX_ESC)return;
    for(const sh of Shs)for(const rd of sh.rds){
      if(rd.st!=="cae"||ya-(rd.atropT||-1e9)<600)continue;
      const h=rd.P[CAD],vx=(h.x-h.px)/H;if(Math.abs(vx)<200*rd.s)continue;
      for(const info of L){
        if(!libre(info))continue;const u=M().ubica(info.E);
        if(u.piso!==rd.piso||Math.abs(u.px-h.x)>(16+12*info.esc)*rd.s||h.y<rd.F-70*info.esc*M().K)continue;
        rd.atropT=ya;
        const o={vx:Math.sign(vx)*azar(170,330),que:"lo atropelló un compañero",foco:false,dice:Math.random()<.5?elige(["¡Oye!","¡Fíjate!","¿¡De dónde saliste!?","¡Cuidado!"]):null};
        if(Math.random()<.7)o.modo="tambalea";else{o.vy=-azar(150,260);o.aguanta=0;}
        if(golpeAPI(info,o)){for(const p of rd.P){p.px+=(p.x-p.px)*.4;}golpe(rd,h.x,Math.abs(vx),h.y+30*rd.s,"¡PUM!");}
        return;
      }
    }
  }
  Cap.foco=()=>{                         // la cámara (si va siguiendo) se queda con la caída que tiene el foco; con el director, lo lleva su plano
    const sh=Shs.find(x=>x.foco);if(!sh)return null;
    const c=centro(sh);if(!c)return null;
    const z=M().zSigue*sh.zoom,q=(ya-sh.sac)/450;
    if(q<1){const a=(1-q)*(1-q)*12/z;c.x+=Math.sin(ya*.09)*a;c.y+=Math.cos(ya*.12)*a;}
    return isFinite(c.x)&&isFinite(c.y)&&isFinite(z)&&z>0?{x:c.x,y:c.y,z}:null;   // un número roto nunca llega a la cámara
  };
  Cap.toqueTrapo=(x,y)=>{               // tocar al muñeco: brinca y, si se estaba levantando, se vuelve a caer
    for(const sh of Shs){
      const rd=sh.rds.find(r=>Math.hypot(r.P[CAD].x-x,r.oy+r.P[CAD].y-y-10*r.s)<40*r.s);if(!rd)continue;
      const dd=Math.random()<.5?-1:1;
      for(let i=0;i<7;i++)empuja(rd,i,dd*azar(60,160),-azar(260,380));
      if(["rodillas","arriba","listo","cae","suelo","trepa","guardia","salta"].includes(rd.st)){rd.fin=false;rd.dijo=false;rd.alcanza=rd.estira=null;rd.k.fill(0);rd.dSuelo=azar(700,1200);rd.AY=0;suena("uy",rd.info.tono);ir(rd,"cae");}
      return true;
    }
    return false;
  };

  // ---- el dibujo: el mismo robot de figura(), pero cada pieza donde la física la dejó
  const rot=(x,y,a)=>[x*Math.cos(a)-y*Math.sin(a),x*Math.sin(a)+y*Math.cos(a)];
  function brazo(sx,sy,m,s,U){
    g.beginPath();g.moveTo(sx,sy);g.quadraticCurveTo((sx+m.x)/2,Math.max(sy,m.y)+3*s,m.x,m.y);g.strokeStyle=U?.manga||TINTA;g.lineWidth=3*s;g.lineCap="round";g.stroke();
    const r=(U?.mano||3.4)*s;circ(m.x,m.y,r,CABEZA);aro(m.x,m.y,r,TINTA,1.2*s);
  }
  function arma(rd){                     // lo que agarró para defenderse, en la mano de delante y apuntando hacia fuera del pecho
    const m=rd.P[MD],c=rd.P[PEC],s=rd.s,a=Math.atan2(m.y-c.y,m.x-c.x);
    g.save();g.translate(m.x,m.y);g.rotate(a);g.scale(s,s*(rd.d||1));
    const k=rd.arma;
    if(k==="llave"){caja(-2,-2,26,4,2,"#9aa3b8");circ(26,0,6,"#9aa3b8");caja(26,-2.2,8,4.4,0,"#2b3048");marco(-2,-2,26,4,2,TINTA,1);}
    else if(k==="escoba"){raya(-4,0,30,0,"#b27c50",3);g.beginPath();g.moveTo(30,-3);g.lineTo(42,-9);g.lineTo(42,9);g.lineTo(30,3);g.closePath();g.fillStyle="#e8c15a";g.fill();g.strokeStyle="#9b7a2a";g.lineWidth=1;g.stroke();}
    else if(k==="chancla"){g.save();g.translate(14,0);g.rotate(.15);elip(0,0,14,6,"#4fb3ff");elip(0,0,10,3.4,"#2f86c9");g.restore();}
    else if(k==="periodico"){caja(-2,-4,30,8,3,"#f2efe4");marco(-2,-4,30,8,3,"#8a8576",1);for(let i=0;i<4;i++)raya(4+i*6,-3,4+i*6,3,"#8a8576",.8);}
    else if(k==="sarten"){raya(-3,0,16,0,"#2b3048",3.4);circ(26,0,10,"#3a4259");circ(26,0,7.5,"#596480");}
    else{raya(-3,0,22,0,"#b27c50",3.2);caja(18,-6,9,12,1.5,"#7f89a6");marco(18,-6,9,12,1.5,TINTA,1);}
    g.restore();
  }
  function dibuja(rd,T){
    const P=rd.P,s=rd.s,d=rd.d,info=rd.info,U=info.uni&&Cap.uni?Cap.uni(info.uni):null;
    const pie=U?.pierna||TINTA,zap=U?.zapato||TINTA,cuerpo=U?U.c:info.cuerpo;
    const k=P[CAB],c=P[PEC],h=P[CAD];
    const aT=Math.atan2(-(h.x-c.x),h.y-c.y),aH=Math.atan2(k.x-c.x,-(k.y-c.y));
    const sp=soporte(rd,h.x,h.y),fl=sp??sueloEn(rd,h.x),alto=cl((fl-h.y)/(30*s),0,1.5);   // la sombra cae en la mesa si está encima
    g.fillStyle=`rgba(0,0,0,${.2-alto*.08})`;g.beginPath();g.ellipse(h.x,fl+1*s,(16+6*(1-cl(alto)))*s,3.6*s,0,0,7);g.fill();
    for(const [i,ox] of [[PI,-6],[PD,6]]){            // piernas y zapatos
      const [lx,ly]=rot(ox*s*d,0,aT),f=P[i];
      raya(h.x+lx,h.y+ly,f.x,f.y,pie,3.6*s);caja(f.x+(d>0?-4:-6)*s,f.y-1.9*s,10*s,4.5*s,2.2*s,zap);
    }
    const hombro=sx=>{const [x,y]=rot(sx*s*d,0,aT);return [c.x+x,c.y+y];};
    {const [x,y]=hombro(-11);brazo(x,y,P[MI],s,U);}
    g.save();g.translate(c.x,c.y);g.rotate(aT);g.scale(s*d,s);g.translate(0,25);
    caja(-13.5,-32,27,23,10,cuerpo);
    if(U)U.t(T);else corazon(0,-21,3.4+Math.sin(T*3)*.4,"rgba(255,255,255,.85)");
    g.restore();
    g.save();g.translate(c.x,c.y);g.rotate(aH);g.scale(s*d,s);g.translate(0,25);
    const bu=rd.bu;
    raya(0,-61,1.5+bu,-69,TINTA,1.8);
    circ(1.5+bu*1.3,-70,3,rd.st==="suelo"&&Math.sin(T*9)>0?ROJO:VERDE);
    caja(-22,-52,4.5,11,2,TINTA);caja(17.5,-52,4.5,11,2,TINTA);
    caja(-19.5,-61,39,32,13,CABEZA);marco(-19.5,-61,39,32,13,TINTA,1.5);
    caja(-15,-57,30,19,8,VISOR);
    ojos(rd.cara,T,1.5);
    const rub=rd.st==="baila"||rd.st==="listo";
    circ(-13.5,-34.5,rub?4.5:2.8,ROSA+(rub?"ee":"99"));circ(13.5,-34.5,rub?4.5:2.8,ROSA+(rub?"ee":"99"));
    if(rd.boca)elip(0,-33.5,3.2,1.3+2.6*rd.boca,"#d94a6a");
    else if(rd.cara==="triste")aro(0,-31.5,2.6,TINTA,1.4,Math.PI+.35,-.35);
    else aro(0,-35.5,2.6,TINTA,1.4,.35,Math.PI-.35);
    if(info.gorro)gorro(info.gorro);else if(U?.k)U.k(T);
    g.restore();
    if(rd.arma)arma(rd);
    {const [x,y]=hombro(11);brazo(x,y,P[MD],s,U);}
    if(rd.st==="suelo"&&!rd.dormido)for(let i=0;i<3;i++){const a=T*5+i*2.1;letra("✦",k.x+Math.cos(a)*15*s,k.y-20*s+Math.sin(a)*4*s,8*s,AMAR);}
    if(rd.dormido&&(rd.st==="suelo"||rd.st==="cae"||rd.st==="desmaya"))for(let i=0;i<2;i++){const f=(T*.5+i/2)%1;g.globalAlpha=1-f;letra("z",k.x+(8+f*10)*s,k.y-(18+f*16)*s,(7+f*5)*s,"#8fa0ff");g.globalAlpha=1;}
  }
  function efectos(sh){
    const K=M().K;
    for(const f of sh.fx){
      const e=cl((ya-f.t0)/f.dur);
      if(f.tipo==="polvo"){const q=e;g.globalAlpha=.55*(1-q);circ(f.x+f.vx*q*.6,f.y+f.vy*q*.6,(3+q*7)*K,"#c9cedb");g.globalAlpha=1;}
      else if(f.tipo==="corazon"){g.globalAlpha=1-e*e;corazon(f.x+Math.sin(e*9)*4*K,f.y-e*28*K,(4+e*2)*K,ROSA);g.globalAlpha=1;}
      else if(f.tipo==="txt"||f.tipo==="dice"){
        const pop=f.tipo==="txt"?1+.6*Math.pow(1-cl(e*4),2):1,px=(f.tipo==="txt"?15:10.5)*K*pop,y=f.y-(f.tipo==="txt"?e*10:e*6)*K;
        g.globalAlpha=e>.75?1-(e-.75)/.25:1;
        g.font=`${f.tipo==="txt"?900:700} ${px}px "Segoe UI",system-ui,sans-serif`;g.textAlign="center";g.textBaseline="middle";g.lineJoin="round";
        g.lineWidth=(f.tipo==="txt"?4.5:3.5)*K;g.strokeStyle="rgba(16,19,27,.92)";g.strokeText(f.txt,f.x,y);
        g.fillStyle=f.tipo==="txt"?(f.col||AMAR):"#fff";g.fillText(f.txt,f.x,y);g.textBaseline="alphabetic";g.globalAlpha=1;
      }
    }
  }
  Cap.trapo=(E,t)=>{const rd=E.trapo;if(!rd)return;dibuja(rd,t/1000+rd.fase);if(rd.show.rds[rd.show.rds.length-1]===rd)efectos(rd.show);};

  // ---- lo que usan los peligros (panel_vivo_peligros.js): un robot, una escena propia; la escena sabe cuándo se acaba
  function solo(info,tipo,o={}){
    if(!info||!libre(info)||Shs.length>=MAX_ESC)return null;
    const sh=nuevaSh(tipo,{zoom:o.zoom||1.7,max:o.max||20000});
    const rd=nace(info,sh,o.alto||0);if(!rd)return null;
    if(o.d)encara(rd,o.d);
    sh.dirige=()=>{};
    return {sh,rd};
  }
  function abre(r,o,txt){activa(r.sh,txt,{k:o.k||"peligro",cool:o.cool??8000,lejos:o.lejos??.25,dirCool:9000,dur:o.dur||7000,lento:o.lento,foco:o.foco});}
  function golpeAPI(info,o={}){          // un golpe: vx, vy en unidades/s (se escalan con el tamaño del robot)
    const r=solo(info,"golpe",o);if(!r)return null;
    const {sh,rd}=r;
    if(o.txt)fx(sh,{tipo:"txt",x:rd.P[CAB].x,y:rd.P[CAB].y-12*rd.s,txt:o.txt,dur:1000,col:o.col});
    if(o.dice)dice(sh,rd,o.dice);
    if(o.sale)rd.sale=o.sale;
    if(o.modo==='tambalea')tambalea(rd,o.vx||0,o);else if(o.modo)cae(rd,o.modo,Math.sign(o.vx||0)||rd.d);else lanzaRd(rd,o.vx||0,o.vy||0,o);
    if(o.alQuitar)rd.alQuitar=o.alQuitar;
    abre(r,o,o.titulo||`${Nom(info)} · ${o.que||"¡golpe!"}`);
    return {rd,sh};
  }
  function saltaAPI(info,o={}){          // brinca: h en px, dx en px, dur en s
    const r=solo(info,"salto",{...o,zoom:1.5});if(!r)return null;
    const {rd}=r;rd.salto={h:o.h||40*rd.s,dx:o.dx||0,dur:o.dur||.55,x0:rd.AX};rd.d=o.dx?Math.sign(o.dx):rd.d;
    if(o.alQuitar)rd.alQuitar=o.alQuitar;
    suena("salto",rd.info.tono);ir(rd,"salta");
    abre(r,{...o,lento:false,lejos:o.lejos??.1},o.titulo||`${Nom(info)} brinca`);
    return {rd,sh:r.sh};
  }
  function guardiaAPI(info,o={}){        // se planta a pelear; devuelve los mandos para el que lo ataca
    const r=solo(info,"pelea",{...o,max:o.max||26000,zoom:1.55});if(!r)return null;
    const {sh,rd}=r;
    rd.arma=o.arma||elige(ARMAS);rd.mira=o.mira||null;rd.d=o.d||rd.d;
    ir(rd,"guardia");if(Math.random()<.6)dice(sh,rd,elige(["¡Ven acá!","¡Atrás!","Aquí te espero.","¡No en mi turno!","¿Me hablas a mí?","¡Fuera de mi taller!"]));
    if(o.alQuitar)rd.alQuitar=o.alQuitar;
    sh.dirige=()=>{if(rd.st==="guardia"&&ya-rd.st0>7000){rd.dijo=true;dice(sh,rd,elige(["¿Ya se fue?","Eso pensé.","Cobarde."]));ir(rd,"listo");}};   // el enemigo se fue a otra cosa: no se queda en guardia para siempre
    abre(r,{...o,lento:false,k:"pelea",lejos:.45},o.titulo||`${Nom(info)} se defiende`);
    return {
      rd,sh,
      batea(tras){if(rd.st==="guardia"||rd.st==="listo"){rd.tras=tras||"guardia";ir(rd,"batea");}},
      esquiva(){if(rd.st==="guardia"){rd.tras="guardia";ir(rd,"esquiva");}},
      recibe(vx,vy,txt){if(["guardia","batea","esquiva","listo"].includes(rd.st)){if(txt)fx(sh,{tipo:"txt",x:rd.P[CAB].x,y:rd.P[CAB].y-12*rd.s,txt,dur:1000});rd.arma=Math.random()<.5?null:rd.arma;lanzaRd(rd,vx,vy,{reflejo:"aletea"});if(sh.foco){sh.lento=.35;sh.lentoT=ya;}}},
      dice:t=>dice(sh,rd,t),
      fx:o2=>fx(sh,o2),
      lento(){if(sh.foco){sh.lento=.35;sh.lentoT=ya;}},
      fin(txt){if(["guardia","batea","esquiva"].includes(rd.st)){rd.dijo=!!txt;if(txt)dice(sh,rd,txt);ir(rd,"listo");}else if(rd.st==="quieto")rd.fin=true;},
      vivo:()=>Shs.includes(sh),
    };
  }

  return {
    prueba:tipo=>{for(const sh of [...Shs])termina(sh);return lanza(Taller.entidades(),tipo||"tropiezo")?Shs[Shs.length-1].tipo:"nadie libre";},
    cada:(a,b)=>{cadaMs=[a,b??a];prox=ya+a;return cadaMs;},
    estado:()=>Shs.map(sh=>({tipo:sh.tipo,foco:sh.foco,quien:sh.rds.map(r=>`${r.info.nom}:${r.st}`),agarres:sh.links.length})),
    libre,ocupado:E=>!!E.trapo||enUso(E),cupo:()=>Shs.length<MAX_ESC,
    golpe:golpeAPI,salta:saltaAPI,guardia:guardiaAPI,
    ponHoyo:f=>{hoyo=f;},
    ponCols:f=>{cols=f;},soporte:(piso,x,y)=>soporte({piso,s:M().K,F:M().sue+3*M().K},x,y),
    enHoyo:(piso,a,b)=>Shs.some(sh=>sh.rds.some(rd=>rd.piso===piso&&rd.P.some(p=>p.x>a-4&&p.x<b+4&&p.y+p.r>rd.F+1))),   // alguien está dentro: el puente no se repone
    escenas:()=>Shs,
  };
})();
