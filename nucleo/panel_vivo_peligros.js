"use strict";
// Los peligros del edificio «En vivo» (5-nov-2026, el usuario: «que los monitos se enfrenten a obstáculos todo el tiempo mientras hacen sus tareas…
// puentes, acantilados… aprovechar el ragdoll… enemigos que los estén atacando, que sean pegatinas del video en el que están trabajando… que se tengan
// que defender… que sea aleatorio, que no se repita»).
// Cada piso tiene su escenografía (foso de aceite, barranco de papeles, foso de pintura, grieta de película, hueco entre azoteas) con PUENTES que a veces
// se rompen y ACANTILADOS que se brincan (a veces no llegan). Cada pocos segundos, un obstáculo al azar donde haya un robot (mejor si se ve): cáscara,
// barril, caja que cae, resorte, ráfaga. Y siempre hay ENEMIGOS: pegatinas del video en curso (`/api/v2/vivo/mundo` → piezas) que vuelan, apuntan y embisten;
// el robot se planta con lo que tenga a mano (llave, escoba, chancla…) y batea, esquiva, falla o caen los dos. La física es la de panel_vivo_ragdoll.js.
// Es teatro: no cambia la acción real ni los letreros. Solo en el edificio, nunca en EN_VIDEO.
// Probar en la consola: Peligros.prueba("resbala"|"rueda"|"cae"|"resorte"|"viento"|"puente"|"brinco"|"enemigo"); Peligros.cada(3000, 7000); Peligros.estado()
window.Peligros=(()=>{
  if(typeof Taller==="undefined"||!Taller.entidades||window.EN_VIDEO||!window.Trapo||!Taller.mundo().EDIF)return null;
  const {g,caja,marco,circ,aro,elip,raya,letra,TINTA,ROJO,AMAR,AZUL,VERDE,ROSA,LILA}=Taller.prim;
  const Cap=Taller.Cap,M=Taller.mundo,T_=window.Trapo;
  const cl=(v,a=0,b=1)=>Math.max(a,Math.min(b,v)),azar=(a,b)=>a+Math.random()*(b-a),elige=L=>L[Math.floor(Math.random()*L.length)];
  const suena=(n,f)=>{try{if(typeof Son!=="undefined")Son.mini(n,f);}catch(e){}};
  const K_=["maq","pb","p1","p2","p3","az"];
  let ya=0;

  // ---- la escenografía: cada piso con sus hoyos (fracciones del ancho), su puente y sus cosas. «brinco» = acantilado sin puente: se salta
  const ESC={
    maq:{n:"Foso de aceite",fondo:["#141a18","#0b0f0e"],roca:"#3c4250",puente:"rejilla",cont:"aceite",resbala:"aceite",rueda:"barril",cae:"engrane",viento:"vapor",
      hoyos:[{a:.30,b:.355,t:"puente"},{a:.56,b:.59,t:"brinco"}]},
    pb:{n:"Planta baja",resbala:"platano",rueda:"pelota",cae:"caja",viento:null,hoyos:[]},
    p1:{n:"Barranco de papeles",fondo:["#5b4a3a","#2a2119"],roca:"#7d6a55",puente:"cuerdas",cont:"papeles",resbala:"hoja",rueda:"bola",cae:"libro",viento:"ventilador",
      hoyos:[{a:.355,b:.41,t:"puente"},{a:.565,b:.60,t:"brinco"},{a:.725,b:.775,t:"puente"}]},
    p2:{n:"Foso de pintura",fondo:["#3a2f4a","#1c1626"],roca:"#6b5a7a",puente:"tablon",cont:"pintura",resbala:"pintura",rueda:"bote",cae:"cubeta",viento:null,
      hoyos:[{a:.19,b:.225,t:"brinco"},{a:.40,b:.47,t:"puente"},{a:.70,b:.735,t:"brinco"}]},
    p3:{n:"Grieta de película",fondo:["#2a2f3d","#11141c"],roca:"#4d5468",puente:"pelicula",cont:"pelicula",resbala:"cinta",rueda:"rollo",cae:"claqueta",viento:null,
      hoyos:[{a:.355,b:.41,t:"puente"},{a:.505,b:.535,t:"brinco"},{a:.745,b:.785,t:"puente"}]},
    az:{n:"Hueco entre azoteas",fondo:["#1d2a4a","#070b18"],roca:"#5d6b78",puente:"tablon",cont:"cielo",resbala:"charco",rueda:"barril",cae:"maceta",viento:"viento",
      hoyos:[{a:.27,b:.31,t:"brinco"},{a:.62,b:.69,t:"puente"}]},
  };
  const HOY=K_.map(k=>ESC[k].hoyos.map(h=>({...h,roto:false,rotoT:-1e9,repara:0,ang:0,va:0,carga:[]})));
  const prof=()=>{const m=M();return Math.max(20,m.H-6-(m.sue+3*m.K));};
  const lim=()=>{const W=M().W;return [.03*W,.97*.88*W];};
  const abierto=h=>h.t==="brinco"||h.roto;
  const hoyoEn=(p,x)=>{const L=HOY[p];if(!L)return null;const W=M().W;for(const h of L){if(!abierto(h))continue;const a=h.a*W,b=h.b*W;if(x>a&&x<b)return {a,b,d:prof()};}return null;};
  T_.ponHoyo(hoyoEn);
  const sueloObj=(p,x)=>{const m=M(),F=m.sue+3*m.K,h=hoyoEn(p,x);return h?F+h.d:F;};

  // ---- textos que saltan (los de los enemigos y obstáculos; los de los robots los pone el muñeco)
  const txts=[];
  const pop=(p,x,y,txt,col=AMAR,dur=900,grande=true)=>txts.push({p,x,y,txt,col,t0:ya,dur,grande});
  const parts=[];   // confeti y pedazos

  // ---- los robots que se pueden meter en problemas
  const calma=new WeakMap(),CALMA_MS=4500;   // tras cada tumbo, unos segundos de paz: que se le vea trabajar entre golpe y golpe
  function robots(){
    const m=M();
    return Taller.entidades().filter(i=>T_.libre(i)&&!salto.has(i.E)&&ya-(calma.get(i.E)??-1e9)>CALMA_MS).map(i=>{const u=m.ubica(i.E);return {i,u,vis:m.visto?m.visto(u.px,u.oy+m.sue-30*m.K,-30):true};}).filter(r=>isFinite(r.u.px));
  }
  function eligeR(L,f){
    const c=f?L.filter(f):L;if(!c.length)return null;
    let tot=0;const w=c.map(r=>{const x=r.vis?6:1;tot+=x;return x;});let q=Math.random()*tot;
    for(let k=0;k<c.length;k++){q-=w[k];if(q<=0)return c[k];}return c[0];
  }
  const dentroHoyo=(p,x,m=0)=>{const W=M().W;return (HOY[p]||[]).some(h=>x>h.a*W-m&&x<h.b*W+m);};

  // ---- andar sobre la escenografía: los puentes se doblan, los acantilados se brincan (o no) y un puente roto no se ve a tiempo
  const salto=new Map();let tablas=[];
  function caerHoyo(info,d,txt,alto=0){
    info.E.oy=null;
    T_.golpe(info,{vx:d*azar(50,120),vy:-azar(0,90),alto,reflejo:"aletea",sale:d,dice:txt,que:"¡al hoyo!",giro:.6,lejos:.4,cool:5000});
  }
  function romper(h,p,quien,d){
    const W=M().W,a=h.a*W,b=h.b*W;
    h.roto=true;h.rotoT=ya;h.ang=0;h.va=0;h.repara=0;suena("crack");pop(p,(a+b)/2,M().sue-60*M().K,"¡CRACK!",ROJO,1100);
    for(const r of robots())if(r.u.piso===p&&r.u.px>a&&r.u.px<b)caerHoyo(r.i,r.i.E.dir<0?-1:1,elige(["¡Nooo!","¿Y el piso?","¡Ayudaaa!"]));
    if(quien&&!quien.E.trapo)caerHoyo(quien,d,elige(["¡CRAAACK!","¡Esto no estaba en el plan!","¡Mamááá!","Ups…"]));
  }
  function andar(){
    const m=M(),W=m.W,K=m.K,vistos=new Set();
    tablas=[];for(const L of HOY)for(const h of L)h.carga=[];
    for(const info of Taller.entidades()){
      const E=info.E;if(E.via||E.trapo||T_.ocupado(E))continue;
      const u=m.ubica(E),hs=HOY[u.piso];if(!hs||!hs.length)continue;
      const px=u.px,d=E.dir<0?-1:1,mg=18*K;
      const h=hs.find(q=>px>q.a*W-mg&&px<q.b*W+mg);if(!h)continue;
      const a=h.a*W,b=h.b*W,base=m.pisoY(u.piso),q=(px-a)/(b-a);
      vistos.add(E);
      let st=salto.get(E);if(!st||st.h!==h){st={h,falla:Math.random()<.24,rompe:Math.random()<.16,q0:azar(.3,.7),alto:(b-a)*.6+22*K*info.esc};salto.set(E,st);}
      if(!abierto(h)){                  // puente entero: se dobla bajo el que pasa y a veces truena
        if(q>0&&q<1){
          const sag=(h.t==="puente"?(ESC[K_[u.piso]].puente==="cuerdas"?9:ESC[K_[u.piso]].puente==="pelicula"?5:2.5):0)*K*Math.sin(q*Math.PI);
          E.oy=base+sag;h.carga.push(px);
          if(info.anda&&st.rompe&&q>st.q0&&ya-h.rotoT>20000&&T_.cupo()){salto.delete(E);E.oy=null;romper(h,u.piso,info,d);}
        }else E.oy=null;
        continue;
      }
      if(!info.anda){E.oy=null;if(q>0&&q<1)tablas.push({p:u.piso,x:px,s:info.esc});continue;}   // parado justo encima del hoyo: un tablón improvisado
      if(h.t!=="brinco"){if(q>.06&&q<.94&&T_.cupo()){salto.delete(E);caerHoyo(info,d,elige(["¿Y el puente?","¡Nadie me avisó!","¿Quién quitó…?"]));}else E.oy=null;continue;}
      const f=cl((px-(a-mg))/(b-a+2*mg)),hop=Math.sin(f*Math.PI)*st.alto*(st.falla?.5:1);
      if(st.falla&&q>.3&&q<.7&&T_.cupo()){salto.delete(E);caerHoyo(info,d,elige(["¡No llego!","¡Muy corto!","¡Aaaah!","Calculé mal…"]),hop);continue;}
      if(!st.dijo&&f>.05){st.dijo=true;if(Math.random()<.3)pop(u.piso,px,m.sue-70*K,elige(["¡Hop!","¡Salto!","¡Yiiijaa!"]),"#fff",800,false);}
      E.oy=base-hop;
    }
    for(const [E,s] of salto)if(!vistos.has(E)){if(!E.via&&!E.trapo)E.oy=null;salto.delete(E);}
    for(let p=0;p<HOY.length;p++)for(const h of HOY[p]){   // los puentes rotos se balancean y, cuando ya nadie está abajo, se reponen
      if(!h.roto)continue;
      h.va+=(1.25-h.ang)*.02-h.va*.06;h.ang+=h.va;
      if(!h.repara&&ya-h.rotoT>7500&&!T_.enHoyo(p,h.a*W,h.b*W))h.repara=ya;
      if(h.repara&&ya-h.repara>700){h.roto=false;h.repara=0;suena("upa",1300);pop(p,(h.a+h.b)/2*W,M().sue-50*K,elige(["Puente nuevo","¡Reparado!","Ahora sí aguanta"]),VERDE,1000,false);}
    }
  }

  // ---- los obstáculos sueltos: cáscara, barril, caja, resorte y ráfaga
  const obs=[];
  const OB={
    resbala(r){                          // aparece delante del que camina; el primero que la pisa se va de espaldas
      const m=M(),d=r.i.E.dir<0?-1:1,[lo,hi]=lim();let x=cl(r.u.px+d*azar(55,120)*m.K,lo+20,hi-20);
      if(dentroHoyo(r.u.piso,x,20*m.K))return false;
      obs.push({tipo:"resbala",p:r.u.piso,x,y:m.sue+3*m.K,t0:ya,dur:14000,k:ESC[K_[r.u.piso]].resbala,vx:0,vy:0,rot:0,vivo:true});return true;
    },
    rueda(r){                            // rueda desde la pared más lejana hacia el robot
      const m=M(),[lo,hi]=lim(),de=r.u.px-lo>hi-r.u.px?-1:1,x=de<0?hi-10:lo+10,d=-de;
      obs.push({tipo:"rueda",p:r.u.piso,x,y:m.sue+3*m.K,vx:d*azar(230,330)*m.K,vy:0,rot:0,R:14*m.K,t0:ya,dur:12000,k:ESC[K_[r.u.piso]].rueda,ya:new Set(),dec:new Map(),vivo:true,toques:0});
      suena("rueda");return true;
    },
    cae(r){                              // del techo: primero la sombra y un «!», luego cae
      const m=M(),d=r.i.anda?(r.i.E.dir<0?-1:1):0;
      obs.push({tipo:"cae",p:r.u.piso,x:r.u.px+d*55*m.K,y:m.PCH+6,vx:0,vy:0,rot:azar(-.2,.2),vr:0,t0:ya,dur:9000,aviso:700,k:ESC[K_[r.u.piso]].cae,blanco:r.i,esq:Math.random()<.3,vivo:true,suelo:false});
      return true;
    },
    resorte(r){
      const m=M(),d=r.i.anda?(r.i.E.dir<0?-1:1):0,[lo,hi]=lim();let x=cl(r.u.px+d*azar(40,90)*m.K,lo+20,hi-20);
      if(dentroHoyo(r.u.piso,x,14*m.K))return false;
      obs.push({tipo:"resorte",p:r.u.piso,x,y:m.sue+3*m.K,t0:ya,dur:9000,sube:0,usado:0,vivo:true});suena("salto",500);return true;
    },
    viento(r){
      const k=ESC[K_[r.u.piso]].viento;if(!k)return false;
      const [lo,hi]=lim(),de=r.u.px-lo<hi-r.u.px?-1:1;
      obs.push({tipo:"viento",p:r.u.piso,x:de<0?lo:hi,dir:-de,t0:ya,dur:2600,k,golpeo:false,vivo:true});suena("zas");return true;
    },
  };
  function pasaObs(dt){
    const m=M(),K=m.K,s=dt/1000,[lo,hi]=lim(),F=m.sue+3*K;
    for(const o of obs){
      const e=ya-o.t0;if(e>o.dur){o.vivo=false;continue;}
      if(o.tipo==="resbala"){
        if(o.vuela){o.x+=o.vx*s;o.y+=o.vy*s;o.vy+=900*K*s;o.rot+=o.vr*s;if(o.y>m.H+40)o.vivo=false;continue;}
        for(const r of robots())if(r.u.piso===o.p&&r.i.anda&&Math.abs(r.u.px-o.x)<7*K*r.i.esc+4){
          const d=r.i.E.dir<0?-1:1;
          if(T_.golpe(r.i,{modo:"resbalon",vx:d,dice:Math.random()<.5?elige(["¡Uaaa!","¿¡Quién dejó eso!?","¡Nooo!"]):null,que:"se resbaló",lejos:.35})){
            o.vuela=true;o.vx=-d*azar(120,260)*K;o.vy=-azar(250,420)*K;o.vr=azar(-14,14);suena("plaf");break;}
        }
      }
      else if(o.tipo==="rueda"){
        o.vy+=1400*K*s;o.x+=o.vx*s;o.y+=o.vy*s;o.rot+=o.vx*s/o.R;
        const fl=sueloObj(o.p,o.x);
        if(o.y>fl){if(o.vy>220*K&&o.y-o.vy*s<=fl+1)suena("rueda");o.y=fl;o.vy=-o.vy*.25;if(Math.abs(o.vy)<40*K)o.vy=0;}
        if(fl>F+2&&o.y>F+o.R)o.vx*=.94;                 // cayó al hoyo: ahí se queda
        if(o.x<lo+o.R||o.x>hi-o.R){o.x=cl(o.x,lo+o.R,hi-o.R);o.vx=-o.vx*.55;o.toques++;suena("bonk");if(o.toques>1)o.dur=Math.min(o.dur,e+1200);}
        if(o.y>F+o.R)continue;
        for(const r of robots()){
          if(r.u.piso!==o.p||o.ya.has(r.i.E))continue;
          const dx=r.u.px-o.x,hacia=Math.sign(dx)===Math.sign(o.vx),ad=Math.abs(dx),sc=r.i.esc;
          if(!hacia||ad>110*K)continue;
          let dec=o.dec.get(r.i.E);if(!dec){dec=Math.random();o.dec.set(r.i.E,dec);}
          if(dec<.32&&ad<52*K&&Math.abs(o.vx)>80*K){o.ya.add(r.i.E);T_.salta(r.i,{h:(46+azar(0,22))*K*sc,dx:0,dur:.6,titulo:"brinca el barril"});continue;}
          if(dec>.82&&ad<95*K&&!o.guard){             // a veces lo regresa de un golpe
            const G=T_.guardia(r.i,{d:-Math.sign(o.vx),arma:elige(["escoba","sarten","martillo"])});
            if(G){o.guard=G;o.gE=r.i.E;o.ya.add(r.i.E);}continue;
          }
          if(ad<o.R+8*K*sc){o.ya.add(r.i.E);T_.golpe(r.i,{vx:Math.sign(o.vx)*azar(260,400),vy:-azar(280,420),txt:elige(["¡PUM!","¡CATAPLÁN!","¡BOLOS!"]),reflejo:"aletea",que:"lo atropelló un barril"});o.vx*=.7;suena("plaf");}
        }
        if(o.guard){
          const G=o.guard,gx=G.rd.P[2].x,ad=Math.abs(gx-o.x);
          if(!G.vivo())o.guard=null;
          else if(!o.bateo&&ad<52*K){o.bateo=ya;G.batea("listo");}
          else if(o.bateo&&ya-o.bateo>90&&!o.devuelto){o.devuelto=true;o.vx=-o.vx*1.25;o.vy=-azar(300,480)*K;pop(o.p,o.x,o.y-50*K,elige(["¡HOME RUN!","¡De regreso!","¡TOMA!"]),AMAR);suena("bonk");setTimeout(()=>G.fin(elige(["Siguiente.","¡Fuera de mi taller!","Fácil."])),500);}
        }
      }
      else if(o.tipo==="cae"){
        if(e<o.aviso){const r=o.blanco&&T_.libre(o.blanco)?M().ubica(o.blanco.E):null;if(r&&!o.blanco.anda)o.x=r.px;continue;}
        if(o.esq&&!o.esquivo&&o.blanco&&T_.libre(o.blanco)){o.esquivo=true;const sc=o.blanco.esc,dd=Math.random()<.5?-1:1;T_.salta(o.blanco,{h:22*K*sc,dx:dd*48*K*sc,dur:.45,titulo:"esquiva la caja"});}
        if(!o.suelo){
          o.vy+=1500*K*s;o.y+=o.vy*s;o.rot+=o.vr*s;
          if(!o.pego)for(const r of robots()){
            if(r.u.piso!==o.p)continue;const sc=r.i.esc*K,cabeza=F-68*sc;
            if(Math.abs(r.u.px-o.x)<20*sc+10*K&&o.y+14*K>cabeza&&o.y<F){
              o.pego=true;T_.golpe(r.i,{vx:azar(-90,90),vy:260,aplasta:true,reflejo:"suelo",txt:"¡BONK!",que:"le cayó algo encima",dice:Math.random()<.35?elige(["Auch.","¿Quién tiró eso?","Veo estrellitas…"]):null});
              suena("bonk");o.vy=-azar(220,320)*K;o.vx=azar(-120,120)*K;o.vr=azar(-8,8);break;
            }
          }
          o.x+=(o.vx||0)*s;
          const fl=sueloObj(o.p,o.x);
          if(o.y+12*K>fl){o.y=fl-12*K;if(Math.abs(o.vy)>200*K){o.vy=-o.vy*.3;suena("plaf");}else{o.suelo=true;o.vy=0;o.vx=0;o.dur=Math.min(o.dur,e+5000);}}
        }
      }
      else if(o.tipo==="resorte"){
        o.sube=cl(e/450);
        if(o.sube<1||o.usado)continue;
        for(const r of robots())if(r.u.piso===o.p&&Math.abs(r.u.px-o.x)<9*K*r.i.esc+5){
          const dd=Math.random()<.5?-1:1;
          if(T_.golpe(r.i,{vx:dd*azar(40,240),vy:-azar(560,880),reflejo:"aletea",txt:"¡BOING!",col:VERDE,que:"salió volando de un resorte",giro:azar(.3,1.4),lejos:.5})){o.usado=ya;o.dur=Math.min(o.dur,e+1800);suena("boing");break;}
        }
      }
      else if(o.tipo==="viento"){
        if(o.golpeo||e<500)continue;o.golpeo=true;
        let n=0;
        for(const r of robots()){
          if(r.u.piso!==o.p||n>=3)continue;
          const ad=Math.abs(r.u.px-o.x);if(ad>520*K)continue;
          const f=1-ad/(560*K);
          if(Math.random()<.25){pop(o.p,r.u.px,F-80*K*r.i.esc,elige(["¡Qué aireee!","Aguanto…","¡Mi antena!"]),"#fff",900,false);continue;}
          if(T_.golpe(r.i,{vx:o.dir*azar(260,480)*f+o.dir*80,vy:-azar(60,220),reflejo:"aletea",giro:1.2,que:"se lo llevó el aire",lejos:.3}))n++;
        }
      }
    }
    for(let i=obs.length-1;i>=0;i--)if(!obs[i].vivo){const o=obs[i];if(o.guard&&o.guard.vivo())o.guard.fin();obs.splice(i,1);}
  }

  // ---- los enemigos: pegatinas del video en curso que se rebelaron
  const IM=new Map();
  function imagen(u){if(!u)return null;let im=IM.get(u);if(!im){im=new Image();im.decoding="async";im.src=u;IM.set(u,im);}return im.complete&&im.naturalWidth?im:null;}
  const url=(v,rel,w=180)=>v&&rel?`/v2/mini/${encodeURIComponent(v)}/${rel.split("/").map(encodeURIComponent).join("/")}?w=${w}`:null;
  function fuentes(){
    const X=window.Extras&&Extras.M,w=X&&X.mundo;if(!w)return [];
    const v=X.vFijo||X.video,L=[];
    if(v)for(const r of w.piezas||[]){const u=url(v,r);if(u){L.push(u);if(r.startsWith("pegatinas/"))L.push(u,u);}}   // las pegatinas pesan el triple
    if(L.length<3)for(const o of w.trofeos||[])if(o.video&&o.rel)L.push(url(o.video,o.rel));
    return L;
  }
  const NOMBRES=["¡Una pegatina rebelde!","¡Se escapó del video!","¡Esa no estaba en el guion!","¡Pegatina salvaje!","¡Viene por ti!","¡Material sin licencia!","¡El recorte se soltó!"];
  const enem=[];let vencidas=0,proxE=0;
  function nuevoEnemigo(forzado){
    const L=robots();if(!L.length)return false;
    const r=forzado||eligeR(L,x=>x.u.piso!==1||Math.random()<.6);if(!r)return false;
    const m=M(),K=m.K,[lo,hi]=lim(),de=Math.random()<.5?-1:1,x=cl(r.u.px+de*azar(260,480)*K,lo+40,hi-40),F=m.sue+3*K;
    const fu=fuentes(),u=fu.length?elige(fu):null;
    const e={p:r.u.piso,x,y:F-azar(95,135)*K,by:0,vx:0,vy:0,rot:0,vr:0,st:"entra",t0:ya,url:u,hp:1+Math.floor(Math.random()*2.6),tam:azar(.85,1.25),
      fase:Math.random()*6,col:elige([ROJO,AMAR,AZUL,VERDE,ROSA,LILA]),wx:x,wy:0,blanco:null,G:null,plan:null,cara:"malo",ronda:azar(1400,3600)};
    e.by=e.y;e.wy=e.y;
    enem.push(e);suena("grr",700);
    pop(e.p,x,e.y-46*K,elige(NOMBRES),ROJO,1400);
    return true;
  }
  function apunta(e){
    const L=robots().filter(r=>r.u.piso===e.p);if(!L.length)return false;
    L.sort((a,b)=>Math.abs(a.u.px-e.x)-Math.abs(b.u.px-e.x));
    const r=Math.random()<.7?L[0]:elige(L);
    e.blanco=r.i;e.st="apunta";e.t0=ya;suena("grr",520+Math.random()*300);
    const d=e.x>=r.u.px?1:-1;
    if(Math.random()<.78){e.G=T_.guardia(r.i,{d,mira:()=>e.x,titulo:`${r.i.nom==="Token"?"Token":r.i.nom[0].toUpperCase()+r.i.nom.slice(1)} contra una pegatina`});}
    const q=Math.random();
    e.plan=e.G?(q<.42?"batea":q<.62?"esquiva":q<.84?"falla":"ambos"):"sorpresa";
    return true;
  }
  function blancoXY(e){                  // a dónde va: la cara del robot (el que se agacha la esquiva)
    const m=M(),K=m.K,F=m.sue+3*K;
    if(e.G&&e.G.vivo()){const c=e.G.rd.P[0];return {x:c.x,y:e.yFijo??c.y+4*K};}
    if(!e.blanco||!T_.libre(e.blanco))return null;
    const u=m.ubica(e.blanco.E);return {x:u.px,y:e.yFijo??F-40*K*e.blanco.esc};
  }
  function lanzado(e,vx,vy){e.st="lanzado";e.t0=ya;e.vx=vx;e.vy=vy;e.vr=azar(10,18)*(Math.random()<.5?-1:1);e.hp--;e.G=null;e.blanco=null;}
  function revienta(e){
    const K=M().K;e.st="fin";vencidas++;suena("pop");
    pop(e.p,e.x,e.y-30*K,elige(["¡POP!","¡FUERA!","¡AL RECICLAJE!","¡DESPEGADA!"]),AMAR,1100);
    for(let i=0;i<26;i++)parts.push({p:e.p,x:e.x,y:e.y,vx:azar(-260,260)*K,vy:azar(-420,-60)*K,c:elige([ROJO,AMAR,AZUL,VERDE,ROSA,LILA,"#fff"]),t0:ya,dur:azar(900,1500),r:azar(0,6),vr:azar(-12,12),w:azar(3,6)*K});
    for(let i=0;i<4;i++)parts.push({p:e.p,x:e.x,y:e.y,vx:azar(-180,180)*K,vy:azar(-360,-120)*K,url:e.url,q:i,t0:ya,dur:1300,r:0,vr:azar(-9,9),w:22*K*e.tam,trozo:true});
  }
  function pasaEnem(dt){
    const m=M(),K=m.K,s=dt/1000,[lo,hi]=lim(),F=m.sue+3*K,techo=m.PCH+20;
    if(!proxE)proxE=ya+4000;
    const vivos=enem.filter(e=>e.st!=="fin").length;
    if(ya>=proxE&&vivos<3){proxE=ya+azar(7000,14000);nuevoEnemigo();}
    for(const e of enem){
      const f=(ya-e.t0)/1000;
      if(e.G&&!e.G.vivo()&&["apunta","carga"].includes(e.st)){e.G=null;e.st="ronda";e.t0=ya;}
      if(e.st==="entra"){if(f>.5){e.st="ronda";e.t0=ya;}}
      else if(e.st==="ronda"){
        if(Math.abs(e.wx-e.x)<10*K||f<.05){e.wx=cl(e.x+azar(-260,260)*K,lo+40,hi-40);e.wy=F-azar(80,150)*K;}
        e.x+=cl(e.wx-e.x,-90*K*s,90*K*s);e.by+=(e.wy-e.by)*Math.min(1,s*1.5);e.y=e.by+Math.sin(ya/300+e.fase)*6*K;
        e.rot=Math.sin(ya/400+e.fase)*.18;
        if(ya-e.t0>e.ronda&&T_.cupo())if(!apunta(e))e.t0=ya;
      }
      else if(e.st==="apunta"){
        const b=blancoXY(e);if(!b){e.st="ronda";e.t0=ya;continue;}
        e.rot=Math.sin(ya/30)*.12;e.y=e.by+Math.sin(ya/90)*2*K;
        if(f>.75){e.st="carga";e.t0=ya;e.yFijo=e.plan==="esquiva"?b.y:null;suena("zas");}
      }
      else if(e.st==="carga"){
        const b=blancoXY(e);if(!b||(e.plan!=="sorpresa"&&!e.G)){e.st="ronda";e.t0=ya;if(e.G)e.G.fin();e.G=null;continue;}
        const dx=b.x-e.x,dy=b.y-e.y,d=Math.hypot(dx,dy)||1,v=(e.plan==="esquiva"?430:380)*K;
        e.vx=dx/d*v;e.vy=dy/d*v;
        if(e.plan==="esquiva"&&d<90*K&&!e.agacho){e.agacho=true;e.G.esquiva();e.yFijo=b.y;}
        if(e.plan==="esquiva"&&e.agacho){e.x+=e.vx*s;if((e.vx>0&&e.x>b.x+40*K)||(e.vx<0&&e.x<b.x-40*K)){e.st="pasa";e.t0=ya;e.vx=Math.sign(e.vx)*v;e.G.dice(elige(["¡Olé!","¡Fallaste!","Muy lento.","¡Matrix!"]));}continue;}
        e.x+=e.vx*s;e.y+=e.vy*s;e.rot=Math.atan2(e.vy,e.vx)*.15;
        const dir=Math.sign(dx)||1;
        if(e.plan==="batea"||e.plan==="ambos"){
          if(!e.swing&&d<62*K){e.swing=ya;e.G.batea("guardia");}
          if(e.swing&&ya-e.swing>85){
            e.G.lento();suena("bonk");
            pop(e.p,e.x,e.y-20*K,elige(["¡ZAS!","¡PLAF!","¡HOME RUN!","¡TOMA!"]),AMAR);
            const G=e.G0=e.G;             // antes de lanzado(), que suelta e.G
            lanzado(e,-dir*azar(320,500)*K,-azar(300,480)*K);
            if(e.plan==="ambos"){setTimeout(()=>{if(G.vivo())G.recibe(dir*azar(320,460),-azar(200,340),"¡PAF!");},30);}
            else setTimeout(()=>{if(G.vivo())G.fin(elige(["¡Y no vuelvas!","Siguiente.","¡Al reciclaje!","Ni sudé.","¿Quién sigue?"]));},700);
          }
        }else if(e.plan==="falla"){
          if(!e.swing&&d<150*K){e.swing=ya;e.G.batea("guardia");}
          if(d<18*K){const G=e.G;G.recibe(dir*azar(360,560),-azar(220,400),elige(["¡PAF!","¡ZUM!","¡PUM!"]));e.st="rebota";e.t0=ya;e.vx=-dir*240*K;e.vy=-260*K;e.G=null;suena("plaf");pop(e.p,e.x,e.y-34*K,elige(["¡JA, JA!","¡Muy lento!","¡Te gané!"]),ROJO,1100,false);}
        }else{                          // por la espalda: no la vio venir
          if(d<18*K){T_.golpe(e.blanco,{vx:dir*azar(380,560),vy:-azar(220,380),txt:"¡PAF!",dice:elige(["¿¡Qué fue eso!?","¡Por la espalda no!","¡Tramposa!"]),reflejo:"aletea",que:"una pegatina lo tumbó"});e.st="rebota";e.t0=ya;e.vx=-dir*240*K;e.vy=-260*K;e.blanco=null;suena("plaf");}
        }
        if(f>4){e.st="ronda";e.t0=ya;if(e.G)e.G.fin();e.G=null;}
      }
      else if(e.st==="pasa"){            // la esquivaron: sigue de largo y se estampa contra la pared
        e.x+=e.vx*s;e.rot+=.02;
        if(e.x<lo+18*K||e.x>hi-18*K){e.x=cl(e.x,lo+18*K,hi-18*K);suena("bonk");pop(e.p,e.x,e.y-30*K,"¡PLOF!",AMAR);e.st="mareado";e.t0=ya;e.vy=0;e.vx=0;
          const G=e.G;e.G=null;if(G)setTimeout(()=>{if(G.vivo())G.fin(elige(["¡Ja! Contra la pared.","Eso dolió… a ti.","Siguiente."]));},400);}
        if(f>3){e.st="ronda";e.t0=ya;if(e.G)e.G.fin();e.G=null;}
      }
      else if(e.st==="lanzado"||e.st==="cae"){
        e.vy+=900*K*s;e.x+=e.vx*s;e.y+=e.vy*s;e.rot+=e.vr*s;
        const r=18*K*e.tam,fl=sueloObj(e.p,e.x)-r;
        if(e.x<lo+r||e.x>hi-r){e.x=cl(e.x,lo+r,hi-r);e.vx=-e.vx*.5;suena("bonk");if(e.hp<=0&&f>.2){revienta(e);continue;}}
        if(e.y<techo){e.y=techo;e.vy=Math.abs(e.vy)*.4;suena("bonk");pop(e.p,e.x,e.y+30*K,"¡BONK!",AMAR,700,false);}
        if(e.y>fl){
          e.y=fl;if(e.hp<=0){revienta(e);continue;}
          if(Math.abs(e.vy)>160*K){e.vy=-e.vy*.4;e.vx*=.6;}else{e.st="mareado";e.t0=ya;e.vx=e.vy=0;}
        }
        if(f>2.5&&e.hp<=0)revienta(e);
      }
      else if(e.st==="mareado"){
        e.vy+=900*K*s;e.y+=e.vy*s;const fl=sueloObj(e.p,e.x)-18*K*e.tam;if(e.y>fl){e.y=fl;e.vy=0;}
        e.rot=Math.sin(ya/120)*.3;
        if(f>2){e.st="ronda";e.t0=ya;e.by=e.y;e.ronda=azar(1200,3000);pop(e.p,e.x,e.y-36*K,elige(["¡GRRR!","¡Esto no se acaba!","Otra vez…"]),ROJO,900,false);suena("grr",600);}
      }
      else if(e.st==="rebota"){
        e.vy+=500*K*s;e.x+=e.vx*s;e.y+=e.vy*s;e.vx*=.98;e.rot+=.05;
        if(f>.7){e.st="ronda";e.t0=ya;e.by=e.y;e.ronda=azar(1800,3800);}
      }
      if(!["fin"].includes(e.st)&&e.st!=="lanzado"){e.x=cl(e.x,lo+10,hi-10);e.y=cl(e.y,techo,F-14*K);}
      e.swing=e.st==="carga"?e.swing:0;e.agacho=e.st==="carga"?e.agacho:false;
    }
    for(let i=enem.length-1;i>=0;i--)if(enem[i].st==="fin")enem.splice(i,1);
    for(let i=parts.length-1;i>=0;i--){const q=parts[i];if(ya-q.t0>q.dur){parts.splice(i,1);continue;}q.vy+=900*K*s;q.x+=q.vx*s;q.y+=q.vy*s;q.r+=q.vr*s;q.vx*=.99;}
    for(let i=txts.length-1;i>=0;i--)if(ya-txts[i].t0>txts[i].dur)txts.splice(i,1);
  }

  // ---- quién dispara qué: siempre pasa algo, mejor donde se ve
  let prox=0,cadaMs=[4000,8000];
  const PESOS=[["resbala",3,r=>r.i.anda],["rueda",3,()=>true],["cae",3,()=>true],["resorte",2,()=>true],["viento",1.4,r=>!!ESC[K_[r.u.piso]].viento]];
  function dispara(tipo,forz){
    const L=robots();if(!L.length)return false;
    if(tipo==="enemigo")return nuevoEnemigo(forz?eligeR(L):null);
    const ops=[];
    for(const [k,w,f] of PESOS){if(tipo&&k!==tipo)continue;const c=L.filter(f);if(c.length)ops.push([k,w,c]);}
    if(!ops.length)return false;
    let tot=ops.reduce((a,o)=>a+o[1],0),q=Math.random()*tot,o=ops[0];
    for(const x of ops){q-=x[1];if(q<=0){o=x;break;}}
    const r=eligeR(o[2]);return r?OB[o[0]](r):false;
  }

  // ---- el dibujo: la escenografía va con el piso (debajo de los robots); lo que vuela, encima
  function dibujaHoyo(p,h,i,t){
    const m=M(),W=m.W,K=m.K,E=ESC[K_[p]],a=h.a*W,b=h.b*W,top=m.sue,bot=m.H-2,T=t/1000,w=b-a;
    const gr=g.createLinearGradient(0,top,0,bot);gr.addColorStop(0,E.fondo[0]);gr.addColorStop(1,E.fondo[1]);g.fillStyle=gr;g.fillRect(a,top,w,bot-top);
    if(E.cont==="cielo"){                // el hueco entre azoteas: la calle allá abajo, con ventanas encendidas
      for(let k=0;k<10;k++){const x=a+((k*37.3+i*13)%1)*w,y=top+12+((k*53.1)%1)*(bot-top-16);caja(x,y,3,3,0,k%3?"#ffd98a":"#8fb4ff");}
      g.globalAlpha=.35;for(let k=0;k<3;k++)raya(a+4,top+20+k*14+Math.sin(T*2+k)*3,b-4,top+26+k*14+Math.sin(T*2+k)*3,"#c9d6ff",1.2);g.globalAlpha=1;
    }else if(E.cont==="aceite"){
      const ly=bot-16*K;g.fillStyle="#1f3a2a";g.beginPath();g.moveTo(a,bot);for(let x=0;x<=w;x+=6)g.lineTo(a+x,ly+Math.sin(T*2+x*.08)*2);g.lineTo(b,bot);g.closePath();g.fill();
      for(let k=0;k<4;k++){const f=(T*.6+k*.27)%1;g.globalAlpha=1-f;aro(a+w*((k*.31+.15)%1),ly+8-f*20,2+f*3,"#5fe0a0",1.2);g.globalAlpha=1;}
    }else if(E.cont==="papeles"){
      for(let k=0;k<9;k++){const x=a+8+((k*41.7+i*7)%1)*(w-16),y=bot-6-((k*3)%3)*9*K,r=(6+(k%3)*2)*K;circ(x,y,r,"#f2efe4");aro(x,y,r,"#b9b29c",1);raya(x-r*.5,y-1,x+r*.4,y+2,"#b9b29c",.8);}
    }else if(E.cont==="pintura"){
      const ly=bot-18*K,cs=[ROSA,AZUL,AMAR,VERDE];
      for(let c=0;c<4;c++){g.fillStyle=cs[c];g.beginPath();g.moveTo(a,bot);for(let x=0;x<=w;x+=5)g.lineTo(a+x,ly+c*4*K+Math.sin(T*1.6+x*.07+c*1.7)*3);g.lineTo(b,bot);g.closePath();g.fill();}
    }else if(E.cont==="pelicula"){
      for(let k=0;k<3;k++){const y=bot-10*K-k*12*K;g.save();g.translate(a+w/2,y);g.rotate(Math.sin(T+k)*.08+(k-1)*.12);caja(-w*.45,-4*K,w*.9,8*K,1,"#1b2030");for(let x=-w*.42;x<w*.42;x+=7*K)caja(x,-3*K,3*K,1.6*K,.3,"#d7dbe6");g.restore();}
    }
    g.fillStyle=E.roca;                  // paredes de roca dentadas: acantilado, no zanja
    for(const [x0,sg] of [[a,1],[b,-1]]){g.beginPath();g.moveTo(x0,top-1);for(let y=top;y<=bot;y+=7){const n=((y*7.13+i*31+(sg>0?0:17))%1);g.lineTo(x0+sg*(3+n*7)*K*.7,y);}g.lineTo(x0,bot);g.closePath();g.fill();}
    for(const x0 of [a,b]){caja(x0-3,top-2,6,5,1,"#20242f");}
    caja(a-2,top-1,w+4,2,0,"rgba(0,0,0,.25)");
    for(const [x0,sg] of [[a,-1],[b,1]]){                       // franjas de peligro en el borde
      for(let k=0;k<3;k++){g.save();g.beginPath();g.rect(x0+(sg<0?-26*K:0),top,26*K,5*K);g.clip();g.fillStyle=k%2?"#20242f":"#ffd166";for(let q=-2;q<8;q++){g.beginPath();g.moveTo(x0+(sg<0?-26*K:0)+q*7*K,top);g.lineTo(x0+(sg<0?-26*K:0)+q*7*K+5*K,top);g.lineTo(x0+(sg<0?-26*K:0)+q*7*K,top+5*K);g.closePath();g.fill();}g.restore();break;}
    }
  }
  function dibujaPuente(p,h,t){
    const m=M(),W=m.W,K=m.K,E=ESC[K_[p]],a=h.a*W,b=h.b*W,y=m.sue,w=b-a,tipo=E.puente;
    const sag=x=>{let s=0;for(const c of h.carga){const q=1-Math.min(1,Math.abs(x-c)/(w*.6));s=Math.max(s,q);}return (tipo==="cuerdas"?9:tipo==="pelicula"?5:2.5)*K*s*Math.sin((x-a)/w*Math.PI);};
    const tramo=(x0,y0,x1,y1)=>{
      if(tipo==="rejilla"){g.save();g.translate(x0,y0);g.rotate(Math.atan2(y1-y0,x1-x0));const L=Math.hypot(x1-x0,y1-y0);caja(0,-1,L,6*K,1,"#596480");for(let k=4;k<L;k+=8)raya(k,0,k,5*K,"#3a4259",1.2);g.restore();}
      else if(tipo==="pelicula"){g.save();g.translate(x0,y0);g.rotate(Math.atan2(y1-y0,x1-x0));const L=Math.hypot(x1-x0,y1-y0);caja(0,-1,L,8*K,1,"#1b2030");for(let k=3;k<L-3;k+=7*K){caja(k,0,3*K,1.6*K,.3,"#d7dbe6");caja(k,5*K,3*K,1.6*K,.3,"#d7dbe6");}g.restore();}
      else if(tipo==="cuerdas"){const n=Math.max(2,Math.round(Math.hypot(x1-x0,y1-y0)/(9*K)));for(let k=0;k<n;k++){const f=(k+.5)/n,x=x0+(x1-x0)*f,yy=y0+(y1-y0)*f;caja(x-3.6*K,yy-1,7.2*K,4*K,1,k%2?"#a97a4f":"#b98a5c");}}
      else{g.save();g.translate(x0,y0);g.rotate(Math.atan2(y1-y0,x1-x0));const L=Math.hypot(x1-x0,y1-y0);caja(0,-1,L,6*K,2,"#a97a4f");raya(2,2*K,L-2,2*K,"#7f5a38",1);if(K_[p]==="p2")for(let k=0;k<4;k++){const x=L*(.15+k*.22);elip(x,5*K,2.2*K,1.4*K,[ROSA,AZUL,AMAR,VERDE][k]);caja(x-.8*K,5*K,1.6*K,(4+((k*7)%5))*K,.8,[ROSA,AZUL,AMAR,VERDE][k]);}g.restore();}
    };
    if(tipo==="cuerdas"){for(const x of [a-6*K,b+6*K]){caja(x-2*K,y-30*K,4*K,30*K,1,"#7f5a38");circ(x,y-30*K,2.6*K,"#5e4229");}}
    if(!h.roto){
      const n=10;let px=a,py=y+sag(a);
      for(let k=1;k<=n;k++){const x=a+w*k/n,yy=y+sag(x);tramo(px,py,x,yy);px=x;py=yy;}
      if(tipo==="cuerdas"){g.strokeStyle="#c9a26b";g.lineWidth=1.6;g.beginPath();g.moveTo(a-6*K,y-28*K);for(let k=0;k<=n;k++){const x=a+w*k/n;g.lineTo(x,y-22*K+sag(x)*.6+Math.sin(k/n*Math.PI)*6*K);}g.lineTo(b+6*K,y-28*K);g.stroke();for(let k=1;k<n;k++){const x=a+w*k/n;raya(x,y-22*K+sag(x)*.6+Math.sin(k/n*Math.PI)*6*K,x,y+sag(x),"#c9a26b",.9);}}
    }else{                               // roto: dos mitades colgando que se balancean; si lo están reponiendo, una tabla nueva baja del techo
      const L=w*.5,an=h.ang+Math.sin(ya/260)*.05;
      tramo(a,y,a+Math.cos(an)*L,y+Math.sin(an)*L);
      tramo(b,y,b-Math.cos(an)*L,y+Math.sin(an)*L);
      if(h.repara){const f=cl((ya-h.repara)/700),yy=y-90*K*(1-f*f);tramo(a,yy,b,yy);}
    }
  }
  function letrero(p,h,t){                // un letrero por hoyo: la escenografía con nombre
    const m=M(),W=m.W,K=m.K,E=ESC[K_[p]],x=h.a*W-34*K,y=m.sue;
    raya(x,y,x,y-34*K,"#6f7892",2.4);
    g.beginPath();g.moveTo(x,y-58*K);g.lineTo(x+13*K,y-35*K);g.lineTo(x-13*K,y-35*K);g.closePath();g.fillStyle=AMAR;g.fill();g.strokeStyle=TINTA;g.lineWidth=1.4;g.stroke();
    letra("!",x,y-42*K,13*K,TINTA);
    g.font=`700 ${Math.max(8,9*K)}px "Segoe UI",system-ui,sans-serif`;g.textAlign="center";g.fillStyle="rgba(255,255,255,.75)";
    g.fillText(h.t==="brinco"?"¡SALTA!":E.n,(h.a+h.b)/2*W,y+(m.H-m.sue)*.55);
  }
  function tablon(o){const m=M(),K=m.K;caja(o.x-22*K*o.s,m.sue-1,44*K*o.s,5*K,1.5,"#a97a4f");raya(o.x-20*K*o.s,m.sue+1.4*K,o.x+20*K*o.s,m.sue+1.4*K,"#7f5a38",1);}
  function dibujaSuelo(o){
    const K=M().K,T=ya/1000;
    if(o.tipo==="resbala"){
      g.save();g.translate(o.x,o.y);g.rotate(o.rot||0);const a=o.vuela?1:cl((ya-o.t0)/300)*cl((o.dur-(ya-o.t0))/600);g.globalAlpha=a;
      if(o.k==="platano"){g.beginPath();g.moveTo(-9*K,-1);g.quadraticCurveTo(0,-9*K,9*K,-1);g.quadraticCurveTo(0,-4*K,-9*K,-1);g.fillStyle="#ffd84a";g.fill();g.strokeStyle="#9b7a2a";g.lineWidth=1;g.stroke();for(const s of [-1,1])elip(s*7*K,-2*K,4*K,1.6*K,"#f2c23a",s*.6);}
      else if(o.k==="hoja"){g.rotate(-.1);caja(-9*K,-2*K,18*K,3*K,.5,"#f2efe4");for(let k=0;k<3;k++)raya(-6*K,-1.4*K+k,6*K,-1.4*K+k,"#b9b29c",.5);}
      else if(o.k==="cinta"){circ(0,-4*K,5*K,"#1b2030");circ(0,-4*K,1.6*K,"#d7dbe6");raya(4*K,-1,14*K,-1,"#1b2030",2*K);}
      else{const c={aceite:"#1f3a2a",pintura:elige([ROSA,AZUL,AMAR]),charco:"#7fb6e6"}[o.k]||"#7fb6e6";o.c=o.c||c;elip(0,-.5,12*K,2.4*K,o.c);g.globalAlpha*=.6;elip(-3*K,-1.2*K,4*K,.8*K,"#fff");}
      g.restore();
    }
    else if(o.tipo==="resorte"){
      const h=(o.sube*14+(o.usado?Math.max(0,1-(ya-o.usado)/200)*26:0))*K,b=o.y;
      caja(o.x-11*K,b-3*K,22*K,4*K,1.5,"#3a4259");
      g.strokeStyle="#c9cedb";g.lineWidth=2;g.beginPath();g.moveTo(o.x,b-3*K);for(let k=1;k<=6;k++)g.lineTo(o.x+(k%2?-6:6)*K,b-3*K-h*k/6);g.stroke();
      caja(o.x-12*K,b-6*K-h,24*K,4*K,2,ROJO);
      if(o.sube<1&&Math.sin(T*30)>0)letra("!",o.x,b-24*K,12*K,ROJO);
    }
    else if(o.tipo==="cae"&&ya-o.t0<o.aviso){
      const f=(ya-o.t0)/o.aviso,m=M();g.globalAlpha=.25+f*.3;elip(o.x,m.sue+3*K,(10+f*10)*K,2.4*K,"#000");g.globalAlpha=1;
      if(Math.sin(T*24)>0)letra("!",o.x,m.sue-90*K,16*K,ROJO);
      caja(o.x-16*K,m.PCH,32*K,4*K,1,"#20242f");      // la trampilla del techo
    }
  }
  function cosa(k,x,y,rot,K){            // lo que rueda y lo que cae, según el piso
    g.save();g.translate(x,y);g.rotate(rot);
    if(k==="barril"){caja(-12*K,-14*K,24*K,28*K,4*K,"#8d5a34");for(const yy of [-8,0,8])raya(-12*K,yy*K,12*K,yy*K,"#5e3a20",2);circ(0,0,3*K,"#c9cedb");}
    else if(k==="pelota"){circ(0,0,14*K,ROJO);g.beginPath();g.arc(0,0,14*K,-.6,.6);g.lineTo(0,0);g.closePath();g.fillStyle="#fff";g.fill();aro(0,0,14*K,TINTA,1.2);}
    else if(k==="bola"){circ(0,0,14*K,"#f2efe4");aro(0,0,14*K,"#b9b29c",1.2);for(let q=0;q<4;q++)raya(-8*K+q*4*K,-6*K,-2*K+q*3*K,5*K,"#b9b29c",1);}
    else if(k==="bote"){caja(-11*K,-13*K,22*K,26*K,3*K,"#d7dbe6");caja(-11*K,-4*K,22*K,10*K,1,ROSA);aro(0,-13*K,9*K,"#7f89a6",1.5,Math.PI,0);}
    else if(k==="rollo"){circ(0,0,14*K,"#232838");for(let q=0;q<6;q++){const u=q*1.047;circ(Math.cos(u)*8*K,Math.sin(u)*8*K,2.6*K,"#7f89a6");}circ(0,0,3*K,"#d7dbe6");}
    else if(k==="engrane"){for(let q=0;q<8;q++){g.save();g.rotate(q*.785);caja(-3*K,-15*K,6*K,6*K,1,"#9aa3b8");g.restore();}circ(0,0,11*K,"#9aa3b8");circ(0,0,4*K,"#3a4259");}
    else if(k==="libro"){caja(-14*K,-10*K,28*K,20*K,2,"#c9434f");caja(-12*K,-8*K,3*K,16*K,1,"#fffaf0");letra("?",3*K,0,12*K,"#fffaf0");}
    else if(k==="cubeta"){g.beginPath();g.moveTo(-12*K,-12*K);g.lineTo(12*K,-12*K);g.lineTo(9*K,12*K);g.lineTo(-9*K,12*K);g.closePath();g.fillStyle="#7f89a6";g.fill();caja(-12*K,-12*K,24*K,5*K,1,AZUL);aro(0,-12*K,12*K,TINTA,1.2,Math.PI,0);}
    else if(k==="claqueta"){caja(-14*K,-6*K,28*K,18*K,2,"#20242f");g.save();g.translate(-14*K,-6*K);g.rotate(-.35);caja(0,-6*K,28*K,6*K,1,"#fff");for(let q=0;q<4;q++)caja(q*7*K+2*K,-6*K,3.5*K,6*K,0,"#20242f");g.restore();}
    else if(k==="maceta"){g.beginPath();g.moveTo(-11*K,-4*K);g.lineTo(11*K,-4*K);g.lineTo(8*K,12*K);g.lineTo(-8*K,12*K);g.closePath();g.fillStyle="#c96f4a";g.fill();circ(-4*K,-9*K,6*K,VERDE);circ(4*K,-11*K,7*K,"#3f8a5a");}
    else{caja(-14*K,-12*K,28*K,24*K,2,"#c99a62");raya(-14*K,-2*K,14*K,-2*K,"#9b7448",1.6);letra("FRÁGIL",0,6*K,6*K,"#7a3b2a");}
    g.restore();
  }
  function dibujaAire(o){
    const K=M().K;
    if(o.tipo==="rueda"){const a=cl((o.dur-(ya-o.t0))/500);g.globalAlpha=a;elip(o.x,sueloObj(o.p,o.x)+1,o.R,2.5*K,"rgba(0,0,0,.2)");cosa(o.k,o.x,o.y-o.R,o.rot,K);g.globalAlpha=1;}
    else if(o.tipo==="cae"&&ya-o.t0>=o.aviso){const a=cl((o.dur-(ya-o.t0))/500);g.globalAlpha=a;cosa(o.k,o.x,o.y,o.rot,K);g.globalAlpha=1;}
    else if(o.tipo==="viento"){
      const m=M(),e=(ya-o.t0)/o.dur,F=m.sue,src=o.x;
      if(o.k==="vapor"){caja(src-(o.dir>0?0:20*K),F-52*K,20*K,14*K,2,"#596480");}
      else if(o.k==="ventilador"){const cx=src+o.dir*12*K,cy=F-60*K;circ(cx,cy,26*K,"#3a4259");for(let q=0;q<3;q++){g.save();g.translate(cx,cy);g.rotate(ya/40+q*2.09);elip(14*K,0,13*K,5*K,"#c9cedb");g.restore();}raya(cx,cy+26*K,cx,F,"#3a4259",4*K);}
      if(e>.18&&e<.9){
        g.globalAlpha=.55*Math.sin((e-.18)/.72*Math.PI);
        for(let q=0;q<9;q++){const f=((ya/600)+q*.13)%1,x=src+o.dir*f*560*K,y=F-(10+((q*29)%90))*K;raya(x,y,x+o.dir*46*K,y+Math.sin(q)*3,o.k==="vapor"?"#e8ecf5":"#cfe2ff",2.2);}
        g.globalAlpha=1;
      }
    }
  }
  function dibujaEnemigo(e,t){
    const K=M().K,s=K*e.tam,w=40*s,h=40*s,T=t/1000,ent=e.st==="entra"?cl((ya-e.t0)/500):1;
    if(e.st==="entra"){g.globalAlpha=1-ent;aro(e.x,e.y,(10+ent*40)*K,LILA,3);aro(e.x,e.y,(6+ent*26)*K,ROSA,2);g.globalAlpha=1;}
    g.save();g.translate(e.x,e.y);g.rotate(e.rot);g.scale(ent,ent);
    const al=Math.sin(T*22+e.fase)*.6;                        // alas de papel
    for(const sg of [-1,1]){g.save();g.translate(sg*w*.42,-h*.1);g.rotate(sg*(.5+al));elip(sg*12*s,-4*s,14*s,6*s,"rgba(255,255,255,.92)");g.strokeStyle="rgba(43,48,72,.5)";g.lineWidth=1;g.stroke();g.restore();}
    g.fillStyle="rgba(0,0,0,.25)";g.beginPath();g.roundRect(-w/2-3+2*s,-h/2-3+3*s,w+6,h+6,8*s);g.fill();
    caja(-w/2-3,-h/2-3,w+6,h+6,8*s,"#fff");
    const im=imagen(e.url);
    g.save();g.beginPath();g.roundRect(-w/2,-h/2,w,h,6*s);g.clip();
    if(im){const r=Math.max(w/im.naturalWidth,h/im.naturalHeight),iw=w/r,ih=h/r;g.drawImage(im,(im.naturalWidth-iw)/2,(im.naturalHeight-ih)/2,iw,ih,-w/2,-h/2,w,h);}
    else{g.fillStyle=e.col;g.fillRect(-w/2,-h/2,w,h);letra("?",0,-2*s,22*s,"#fff");}
    g.restore();
    const b=blancoXY(e),mx=b?cl((b.x-e.x)/80,-1,1):Math.sin(T+e.fase)*.5,enoj=["apunta","carga"].includes(e.st),mare=e.st==="mareado";
    for(const sg of [-1,1]){                                   // ojos de pegatina enojada
      const ox=sg*9*s,oy=h*.18;
      elip(ox,oy,6.4*s,7*s,"#fff");aro(ox,oy,6.4*s,TINTA,1.3);
      if(mare){raya(ox-3*s,oy-3*s,ox+3*s,oy+3*s,TINTA,1.6);raya(ox-3*s,oy+3*s,ox+3*s,oy-3*s,TINTA,1.6);}
      else circ(ox+mx*2.4*s,oy+1.2*s,3*s,enoj?ROJO:TINTA);
      raya(ox-6*s*sg*-1,oy-8.5*s-(sg>0?0:0),ox+6*s*sg*-1,oy-6*s+(enoj?-2*s:0),TINTA,2.2*s);
    }
    if(enoj){g.beginPath();g.moveTo(-7*s,h*.42);for(let q=0;q<=6;q++)g.lineTo(-7*s+q*14*s/6,h*.42+(q%2?3*s:-1*s));g.strokeStyle=TINTA;g.lineWidth=1.6;g.stroke();}
    else aro(0,h*.48,4*s,TINTA,1.5,Math.PI+.4,-.4);
    g.restore();
    for(let q=0;q<Math.max(0,e.hp);q++)letra("♥",e.x+(q-(e.hp-1)/2)*9*K,e.y-h/2-12*K,8*K,ROJO);   // las vidas que le quedan
    if(mare)for(let q=0;q<3;q++){const a=T*5+q*2.1;letra("✦",e.x+Math.cos(a)*18*K,e.y-h/2-6*K+Math.sin(a)*4*K,8*K,AMAR);}
  }
  function dibujaParts(p){
    const K=M().K;
    for(const q of parts){if(q.p!==p)continue;const a=1-cl((ya-q.t0)/q.dur);g.globalAlpha=a;g.save();g.translate(q.x,q.y);g.rotate(q.r);
      if(q.trozo){const im=imagen(q.url);g.beginPath();const w=q.w;if(q.q===0){g.moveTo(-w/2,-w/2);g.lineTo(w/2,-w/2);g.lineTo(0,0);}else if(q.q===1){g.moveTo(w/2,-w/2);g.lineTo(w/2,w/2);g.lineTo(0,0);}else if(q.q===2){g.moveTo(w/2,w/2);g.lineTo(-w/2,w/2);g.lineTo(0,0);}else{g.moveTo(-w/2,w/2);g.lineTo(-w/2,-w/2);g.lineTo(0,0);}g.closePath();g.fillStyle="#fff";g.fill();if(im){g.save();g.clip();const r=Math.max(w/im.naturalWidth,w/im.naturalHeight),iw=w/r,ih=w/r;g.drawImage(im,(im.naturalWidth-iw)/2,(im.naturalHeight-ih)/2,iw,ih,-w/2,-w/2,w,w);g.restore();}}
      else caja(-q.w/2,-q.w/4,q.w,q.w/2,1,q.c);
      g.restore();g.globalAlpha=1;}
    for(const x of txts){
      if(x.p!==p)continue;const e=cl((ya-x.t0)/x.dur),pp=x.grande?1+.5*Math.pow(1-cl(e*4),2):1,px=(x.grande?15:10.5)*K*pp,y=x.y-e*10*K;
      g.globalAlpha=e>.75?1-(e-.75)/.25:1;g.font=`${x.grande?900:700} ${px}px "Segoe UI",system-ui,sans-serif`;g.textAlign="center";g.textBaseline="middle";g.lineJoin="round";
      g.lineWidth=(x.grande?4.5:3.5)*K;g.strokeStyle="rgba(16,19,27,.92)";g.strokeText(x.txt,x.x,y);g.fillStyle=x.col;g.fillText(x.txt,x.x,y);g.textBaseline="alphabetic";g.globalAlpha=1;
    }
  }

  // ---- los ganchos del taller
  const prevPaso=Cap.trapoPaso,prevPiso=Cap.enPiso,prevSobre=Cap.sobre;
  Cap.trapoPaso=(t,dt)=>{
    ya=t;const d=Math.min(dt||16,50);
    try{
      for(const i of Taller.entidades())if(i.E.trapo)calma.set(i.E,t);
      andar();pasaObs(d);pasaEnem(d);
      if(!prox)prox=t+2500;
      if(t>=prox){prox=t+azar(...cadaMs);if(T_.cupo())dispara();}
    }catch(e){console.warn("peligros",e);}
    prevPaso&&prevPaso(t,dt);
  };
  Cap.enPiso=(k,t)=>{
    prevPiso&&prevPiso(k,t);
    const p=K_.indexOf(k);if(p<0)return;
    try{
      for(let i=0;i<HOY[p].length;i++){const h=HOY[p][i];dibujaHoyo(p,h,i,t);letrero(p,h,t);if(h.t==="puente")dibujaPuente(p,h,t);}
      for(const o of tablas)if(o.p===p)tablon(o);
      for(const o of obs)if(o.p===p)dibujaSuelo(o);
    }catch(e){console.warn("peligros",e);}
  };
  Cap.sobre=(k,p,t,dt)=>{
    prevSobre&&prevSobre(k,p,t,dt);
    try{
      for(const o of obs)if(o.p===p)dibujaAire(o);
      for(const e of enem)if(e.p===p)dibujaEnemigo(e,t);
      dibujaParts(p);
    }catch(e){console.warn("peligros",e);}
  };

  return {
    prueba(tipo){
      if(!M().W)return "el taller aún no se ha medido (¿pestaña oculta?)";
      if(tipo==="puente"||tipo==="brinco"){   // lleva a un robot libre a la orilla del hoyo y le pasa lo suyo
        const L=robots();let r=eligeR(L,x=>HOY[x.u.piso]&&HOY[x.u.piso].some(h=>h.t===tipo)),p;
        if(r)p=r.u.piso;else{   // nadie en un piso con ese hoyo: se lleva a uno libre al piso que lo tenga
          r=eligeR(L);if(!r)return "nadie libre";
          const ps=HOY.map((L,i)=>L.some(h=>h.t===tipo)?i:-1).filter(i=>i>=0);if(!ps.length)return "no hay "+tipo+" en este edificio";
          p=ps[Math.floor(Math.random()*ps.length)];
        }
        const h=HOY[p].find(h=>h.t===tipo),W=M().W;
        if(p!==r.u.piso){r.i.E.via=null;r.i.E.oy=null;}
        Taller.ponX(r.i.E,(h.a+h.b)/2*W,p,1);
        if(tipo==="puente"){h.rotoT=-1e9;romper(h,p,r.i,1);}else caerHoyo(r.i,1,"¡Aaaah!");
        return tipo+" en "+ESC[K_[p]].n;
      }
      return dispara(tipo,true)?tipo:"no se pudo (¿nadie libre?)";
    },
    cada:(a,b)=>{cadaMs=[a,b??a];prox=ya+a;return cadaMs;},
    estado:()=>({obstaculos:obs.map(o=>o.tipo+"@"+K_[o.p]),enemigos:enem.map(e=>`${K_[e.p]}:${e.st}:${e.plan||"-"}:${e.hp}♥`),vencidas,saltando:salto.size,rotos:HOY.flat().filter(h=>h.roto).length,escenas:T_.estado()}),
    ESC,HOY,
  };
})();
