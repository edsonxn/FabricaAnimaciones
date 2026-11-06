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

  let Shs=[],prox=0,cadaMs=[18000,40000],ya=0,ultFoco=-1e9,hoyo=null;
  const MAX_ESC=4;
  const enUso=E=>Shs.some(sh=>sh.rds.some(rd=>rd.E===E));

  // ---- un muñeco: nace con la pose de parado donde está el robot y con el control que tenía
  function nace(info,show,alto=0){
    const {E}=info,m=M(),u=m.ubica(E),s=m.K*info.esc,d=E.dir<0?-1:1,F=m.sue+3*m.K;
    const P=PARADO.map(([x,y],i)=>({x:u.px+x*s*d,y:F+y*s-alto,px:u.px+x*s*d,py:F+y*s-alto,r:RAD[i]*s,w:1/MASA[i]}));
    if(!(s>0&&isFinite(u.px)&&isFinite(F)&&isFinite(u.oy)))return null;   // el taller aún no se ha medido
    const rd={E,info,s,d,F,P,x0:u.px,piso:u.piso,oy:u.oy,lo:u.lo,hi:u.hi,techo:m.PCH?m.PCH+1:-1e9,AX:u.px,AY:0,k:new Array(7).fill(1),T:PARADO.map(()=>[0,0]),
      cara:"normal",boca:0,st:"quieto",st0:ya,show,golpeT:-1e9,fase:Math.random()*6,paso:0,bu:0,dSuelo:azar(900,1700),arma:null};
    E.trapo=rd;show.rds.push(rd);pose(rd,PARADO);
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
  const sueloEn=(rd,x)=>{const h=hoyoEn(rd,x);return rd.F+(h?h.d:0);};
  const enPozo=rd=>{const h=hoyoEn(rd,rd.P[CAD].x);return h&&rd.P[CAD].y>rd.F+4*rd.s?h:null;};

  // ---- efectos: golpes con onomatopeya, polvo, estrellitas, corazones y lo que dicen
  function fx(sh,o){sh.fx.push({t0:ya,dur:700,...o});}
  function dice(sh,rd,txt){const h=rd.P[CAB],y=h.y-30*rd.s;fx(sh,{tipo:"dice",x:h.x,y:rd.info.token?Math.min(y,rd.F-112*M().K):y,txt,dur:1300});}   // Token lleva su letrero a 92 sobre el suelo: lo que dice va encima, no tapado
  function golpe(rd,x,v,y,txt){
    if(ya-rd.golpeT<380)return;
    rd.golpeT=ya;const sh=rd.show,fuerte=v>420*rd.s;
    suena(txt==="¡BONK!"?"bonk":"plaf",rd.info.tono);
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
      if((s>.6&&quieto(rd))||s>2.6)ir(rd,"suelo");
    }
    else if(st==="suelo"){
      rd.k.fill(0);rd.cara=rd.dormido?"dormido":s<.7?"apretado":"triste";
      if(rd.estira){const q=rd.estira(),i=manoCerca(rd,q);rd.T[i]=[q.x,q.y];rd.k[i]=.25;}
      if(!rd.espera&&s*1000>rd.dSuelo*(rd.dormido?1.6:1))levanta(rd);
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
      if(s>.75)rd.fin=true;
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
    else if(st==="salta"){             // brinco de verdad (barril, caja, acantilado corto): sube, encoge las piernas y cae de pie
      const J=rd.salto,q=cl(s/J.dur);
      rd.AX=J.x0+J.dx*q;rd.AY=-J.h*Math.sin(q*Math.PI);
      pose(rd,PARADO);const enc=Math.sin(q*Math.PI);rd.T[PI][1]-=8*S*enc;rd.T[PD][1]-=10*S*enc;rd.T[PI][0]-=3*S*rd.d*enc;rd.T[MI][1]-=14*S*enc;rd.T[MD][1]-=18*S*enc;
      rd.k.fill(1);rd.cara=q<.5?"wow":"feliz";
      if(q>=1){rd.AY=0;ir(rd,"listo");if(!rd.dijo&&Math.random()<.55){rd.dijo=true;dice(rd.show,rd,elige(["¡Ja!","Fácil.","¡Hop!","¿Eso es todo?","Ni me tocó."]));}}
    }
  }
  function levanta(rd){                  // se levanta hacia donde quedó la cabeza: primero de rodillas, luego de pie. En un hoyo, después trepa
    const h=rd.P[CAD],c=rd.P[CAB],P0=enPozo(rd);
    rd.d=c.x>=h.x?1:-1;rd.alcanza=rd.estira=null;rd.dormido=false;
    if(P0){rd.pozo=P0;rd.AY=P0.d;rd.AX=cl(h.x,P0.a+10*rd.s,P0.b-10*rd.s);rd.sale=rd.sale||rd.caeDir||rd.d;}
    else{rd.pozo=null;rd.AY=0;rd.AX=cl(h.x,rd.lo+10*rd.s,rd.hi-10*rd.s);}
    suena("upa",rd.info.tono);ir(rd,"rodillas");
  }
  function cae(rd,modo,dd=rd.d){         // el tropiezo de verdad: músculos a cero y un empujón según cómo se cae
    rd.caeDir=dd;rd.k.fill(0);
    if(modo==="tropiezo"){rd.reflejo="suelo";empujaTodo(rd,[[dd*240,-110],[dd*175,-90],[dd*60,-60],[dd*210,-150],[dd*210,-150],[-dd*90,-40],[-dd*90,-40]]);}
    else if(modo==="resbalon"){rd.reflejo="aletea";empujaTodo(rd,[[-dd*130,-20],[-dd*40,-40],[dd*90,-170],[-dd*60,-260],[dd*60,-260],[dd*330,-270],[dd*300,-250]]);}
    else if(modo==="suave"){rd.reflejo="suelo";empujaTodo(rd,[[dd*120,-40],[dd*80,-30],[dd*20,-10],[dd*90,-40],[dd*90,-40],[0,0],[0,0]]);}
    if(modo==="desmayo"){rd.dormido=true;ir(rd,"desmaya");return;}
    if(!rd.dormido)suena("uy",rd.info.tono);
    ir(rd,"cae");
  }
  function lanzaRd(rd,vx,vy,o={}){       // un golpe con dirección (barril, enemigo, resorte, viento): lo de arriba sale más rápido, así da la vuelta
    rd.caeDir=Math.sign(vx)||rd.d;rd.k.fill(0);rd.reflejo=o.reflejo!==undefined?o.reflejo:elige(["suelo","aletea","aletea",null]);
    const giro=o.giro??1;
    rd.P.forEach((p,i)=>{const hf=-PARADO[i][1]/45;empuja(rd,i,vx*(1+giro*(hf-.5)*.9)*azar(.85,1.15),vy*azar(.88,1.12)*(i>=PI?.82:1)+(o.aplasta&&i===CAB?vy*.4:0));});
    if(!rd.dormido)suena("uy",rd.info.tono);
    rd.pozo=null;rd.AY=0;rd.dijo=false;rd.fin=false;rd.alcanza=rd.estira=null;
    ir(rd,"cae");
  }

  // ---- las escenas: quién participa, cómo empieza y qué pasa entre ellos
  const TXT={tropiezo:n=>`${n} se tropezó`,resbalon:n=>`${n} se resbaló`,desmayo:n=>`${n} se quedó dormido de pie`,
    cadena:(n,o)=>`${o} atrapó a ${n}`,domino:(n,o)=>`${n} se llevó a ${o}`,ayuda:(n,o)=>`${o} ayuda a ${n}`,pie:(n,o)=>`${n} le agarró el pie a ${o}`,manos:(n,o)=>`${n} y ${o} · a bailar`};
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
    const L=sh.rds;
    for(let it=0;it<n;it++){
      for(const rd of L){
        const G=GRAV*rd.s*H*H;
        for(const p of rd.P){const vx=(p.x-p.px)*.996,vy=(p.y-p.py)*.996;p.px=p.x;p.py=p.y;p.x+=vx;p.y+=vy+G;}
        for(let i=0;i<7;i++){const k=rd.k[i];if(!k)continue;const p=rd.P[i],[tx,ty]=rd.T[i],c=1-Math.exp(-H*42*k);p.x+=(tx-p.x)*c;p.y+=(ty-p.y)*c;p.px+=(p.x-p.px)*k*.28;p.py+=(p.y-p.py)*k*.28;}
      }
      for(let r=0;r<4;r++){
        for(const rd of L)for(const [a,b,lo,hi] of HUESOS)hueso(rd.P[a],rd.P[b],lo*rd.s,hi*rd.s);
        for(const l of sh.links)hueso(l.a.P[l.i],l.b.P[l.j],0,l.L);
      }
      for(const rd of L)for(let i=0;i<7;i++){
        const p=rd.P[i];
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
        if(p.y-p.r<rd.techo){             // el techo: el que sale volando se da en la cabeza
          const v=(p.y-p.py)/H;
          if(i<=CAD&&v<-260*rd.s)golpe(rd,p.x,-v,rd.techo+46*rd.s,"¡BONK!");
          p.y=rd.techo+p.r;p.py=p.y+v*.3*H;
        }
        if(p.x-p.r<rd.lo){if(i<=CAD&&(p.px-p.x)/H>320*rd.s)golpe(rd,rd.lo,(p.px-p.x)/H,p.y);p.x=rd.lo+p.r;p.px=p.x;}
        if(p.x+p.r>rd.hi){if(i<=CAD&&(p.x-p.px)/H>320*rd.s)golpe(rd,rd.hi,(p.x-p.px)/H,p.y);p.x=rd.hi-p.r;p.px=p.x;}
      }
    }
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
    if(ok.length)op.push(["desmayo",1,()=>[elige(ok.filter(x=>!x.anda).length?ok.filter(x=>!x.anda):ok)]]);
    if(cerca.length){op.push(["cadena",3,()=>{const p=elige(cerca);return [p.a,p.b];}]);op.push(["domino",2,()=>{const p=elige(cerca);return [p.a,p.b];}]);}
    if(medio.length){op.push(["ayuda",3,()=>{const p=elige(medio);return [p.a,p.b];}]);op.push(["pie",2,()=>{const p=elige(medio);return [p.a,p.b];}]);}
    if(quietos.length)op.push(["manos",3,()=>{const p=elige(quietos);return [p.a,p.b];}]);
    if(!ok.length)return null;
    if(tipo){                           // a prueba: si no hay pareja cerca, la que se pueda
      const o=op.find(x=>x[0]===tipo);if(o)return [o[0],...o[2]()];
      if(["tropiezo","resbalon","desmayo"].includes(tipo))return [tipo,elige(ok)];
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
      for(const rd of sh.rds){const c=rd.P[CAB];rd.bu+=((cl(-(c.x-c.px)/H/rd.s*.012,-4,4))-rd.bu)*.2;}
      sh.fx=sh.fx.filter(f=>ya-f.t0<f.dur);
      if(sh.rds.every(rd=>rd.fin))termina(sh);
    }
  };
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
    const fl=sueloEn(rd,h.x),alto=cl((fl-h.y)/(30*s),0,1.5);
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
    if(o.modo)cae(rd,o.modo,Math.sign(o.vx||0)||rd.d);else lanzaRd(rd,o.vx||0,o.vy||0,o);
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
    enHoyo:(piso,a,b)=>Shs.some(sh=>sh.rds.some(rd=>rd.piso===piso&&rd.P.some(p=>p.x>a-4&&p.x<b+4&&p.y+p.r>rd.F+1))),   // alguien está dentro: el puente no se repone
    escenas:()=>Shs,
  };
})();
