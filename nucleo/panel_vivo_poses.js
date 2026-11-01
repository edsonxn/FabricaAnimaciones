"use strict";
// Kit de variantes del taller «En vivo» (1-nov-2026, el usuario: «se repite mucho lo mismo… un kit muy amplio de animaciones para cada acción, que den risa»).
// Cada acción de trabajo tiene aquí varias poses; el taller las baraja sin repetir hasta agotarlas y, si la acción dura, cambia cada 9 s.
// El letrero y el sonido siguen siendo los de la acción REAL: solo cambia el teatro. Coordenadas: x hacia delante del robot, y negativa hacia arriba,
// pies en y = 0, cabeza de -61 a -29; la utilería entre x -60 y +84. s = segundos desde que empezó la pose.
// Añadir una: pon("<acción>", {nombre(T,s){return {...};}}) → POSES["<acción>_<nombre>"]. Probar en la consola: Taller.prueba("boton_hamster").
(()=>{
  if(typeof Taller==="undefined"||!Taller.VARIAS)return;
  const {g,caja,marco,circ,aro,elip,raya,letra,camino,em,humito,MADERA,TINTA,CABEZA,ROSA,ROJO,AMAR,AZUL,VERDE,LILA,COLORES}=Taller.prim;
  const POSES=Taller.POSES,VARIAS=Taller.VARIAS;
  const pon=(acc,poses)=>{VARIAS[acc]=VARIAS[acc]||[];for(const [k,f] of Object.entries(poses)){const n=acc+"_"+k;POSES[n]=f;if(!VARIAS[acc].includes(n))VARIAS[acc].push(n);}};
  const ciclo=(s,d)=>((s%d)+d)%d/d;
  const ease=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x);};
  const mareo=(x,y,T)=>{for(let i=0;i<3;i++){const a=T*5+i*2.1;letra("✦",x+Math.cos(a)*14,y+Math.sin(a)*4,8,AMAR);}};

  // ---- correr un comando (la más frecuente)
  pon("boton",{
    palanca(T,s){
      const f=ciclo(s,2.4),k=f<.45?ease(f/.45):f<.75?1:1-ease((f-.75)/.25),a=-.7+k*1.7,hx=36+Math.sin(a)*24,hy=-30-Math.cos(a)*24,luz=k>.95;
      if(luz)em(500,46,-60,"⚡",AMAR);
      return {cara:f<.45?"apretado":luz?"wow":"enfocado",incl:.05+k*.1,mira:2,brD:[hx-1,hy+2],brI:[hx-5,hy+4],pies:[k*3,-k*2],
        atras(){caja(24,-30,26,30,3,"#6f7892");marco(24,-30,26,30,3,TINTA,1.3);for(let i=0;i<3;i++)raya(28,-22+i*6,46,-22+i*6,"#4a5270",1.4);raya(52,-30,52,-38,"#9aa3bb",1.6);if(luz)circ(52,-43,9,"#ffe98a55");circ(52,-43,5,luz?AMAR:"#4a5270");},
        frente(){raya(36,-30,hx,hy,"#9aa3bb",3);circ(36,-30,3,TINTA);circ(hx,hy,4.5,ROJO);}};
    },
    hamster(T){
      const r=T*9,b=Math.abs(Math.sin(T*18));em(900,66,-14,"💨","#d7dbe6",-10);
      return {cara:"feliz",boca:.4+.3*Math.sin(T*8),mira:2,sube:Math.abs(Math.sin(T*5))*3,brD:[22,-46+Math.sin(T*10)*5],brI:[-18,-42],
        atras(){raya(44,-21,34,0,"#79829b",2.6);raya(44,-21,54,0,"#79829b",2.6);g.save();g.translate(44,-21);g.rotate(r);for(let i=0;i<6;i++){g.rotate(Math.PI/3);raya(0,0,0,-18,"#9aa3bb88",1.2);}g.restore();aro(44,-21,18,"#9aa3bb",2.6);},
        frente(){const hy=-7-b*2;elip(44,hy,7,4.6,"#d9a066");elip(48,hy-2,3.2,3,"#d9a066");circ(49.5,hy-2.6,.9,TINTA);circ(46,hy-5.4,1.6,"#f3c5a0");for(const q of [-1,1])raya(44+q*3,hy+3,44+q*3+Math.sin(T*36)*q*2.5,hy+6,"#b07a46",1.4);circ(44,-21,2.6,TINTA);}};
    },
    patada(T,s){                         // la máquina no responde: patada, tiembla, ¡ding!
      const f=ciclo(s,3.4),pat=f>.5&&f<.6,tiembla=f>.5&&f<.7?Math.sin(T*60)*1.5:0,ok=f>.62;
      if(pat)em(400,30,-28,"💥",AMAR,-10);if(ok)em(800,44,-66,"✦",VERDE);
      return {cara:f<.35?"enfocado":f<.62?"apretado":"feliz",mira:2,incl:f>.4&&f<.6?-.12:0,pies:[-2,pat?17:f>.4&&f<.5?-6:0],brD:f<.35?[27,-36+(Math.sin(T*14)>0?2:0)]:[16,-18],brI:[-16,-20],
        atras(){g.save();g.translate(tiembla,0);caja(30,-62,30,62,4,"#c94b5e");marco(30,-62,30,62,4,TINTA,1.3);caja(34,-56,15,34,2,"#2b3048");for(let i=0;i<3;i++)for(let j=0;j<2;j++)circ(38+j*7,-50+i*10,2.4,COLORES[(i*2+j)%6]);caja(51,-54,6,4,1,ok?VERDE:"#3c4259");caja(51,-46,6,10,1,"#9aa3bb");caja(34,-14,22,8,2,"#1b1f2e");g.restore();},
        frente(){if(ok){const k=Math.min(1,(f-.62)/.12);caja(40,-24+k*12,7,6,1.5,AZUL);}}};
    },
    detonador(T,s){
      const f=ciclo(s,3),k=f<.3?0:f<.42?(f-.3)/.12:f<.8?1:1-(f-.8)/.2,bum=f>.42&&f<.75;
      if(bum){em(250,74+Math.random()*10-5,-30,"💥",AMAR,-30);em(300,66,-20,"✦",ROJO,-40);}
      return {cara:bum?"wow":"apretado",pelo:bum,mira:3,incl:bum?-.1:.08,sube:bum?Math.abs(Math.sin(T*20))*3:0,brD:[34,-34+k*10],brI:[24,-34+k*10],
        atras(){caja(24,-18,22,18,2,"#a0522d");marco(24,-18,22,18,2,TINTA,1.2);raya(46,-6,64,-2,"#3c4259",1.4);raya(64,-2,78,-4,"#3c4259",1.4);},
        frente(){raya(35,-18,35,-30+k*10,"#9aa3bb",2.4);caja(26,-33+k*10,18,4,2,TINTA);if(bum){const r=8+(f-.42)*40;circ(78,-14,r,"#ffffff44");circ(74,-18,r*.6,"#ffd16688");}}};
    },
    microondas(T,s){
      const f=ciclo(s,4),coc=f>.22&&f<.85,ding=f>=.85;
      if(ding)em(600,44,-52,"¡ding!",AMAR);
      return {cara:ding?"feliz":coc?"wow":"enfocado",mira:3,incl:coc?.12:0,dx:coc?3:0,brD:f<.22?[55,-28+(Math.sin(T*16)>0?2:0)]:[18,-20],brI:[-15,-16],
        atras(){caja(18,-14,48,14,2,MADERA);caja(20,-40,44,26,3,"#d7dbe6");marco(20,-40,44,26,3,TINTA,1.3);caja(24,-36,26,18,2,coc?"#ffe98a":"#3c4259");caja(52,-36,9,18,1.5,"#9aa3bb");for(let i=0;i<3;i++)circ(56.5,-32+i*5,1.3,TINTA);},
        frente(){if(coc){elip(37,-21,10,2.4,"#ffffff88");caja(37+Math.cos(T*4)*6-3,-27,6,5,1,ROJO);}}};
    },
    manivela(T){                         // la cinta perforada sale y se enrolla en el piso
      const a=T*5,hx=20+Math.cos(a)*8,hy=-26+Math.sin(a)*8,d=(T*14)%22;
      return {cara:"enfocado",mira:2,incl:.06,sube:Math.abs(Math.sin(a))*1.5,brD:[hx,hy],brI:[-14,-18],
        atras(){caja(22,-42,30,30,3,"#8791ad");marco(22,-42,30,30,3,TINTA,1.3);raya(26,-12,26,0,"#6f7892",2.4);raya(48,-12,48,0,"#6f7892",2.4);for(let i=0;i<3;i++)circ(28+i*8,-36,2,Math.sin(T*7+i*2)>0?AMAR:"#3c4259");
          g.beginPath();g.moveTo(52,-27);g.lineTo(70,-27);g.quadraticCurveTo(82,-20,72,-9);g.quadraticCurveTo(62,2,78,0);g.strokeStyle="#fffaf0";g.lineWidth=6;g.stroke();for(let i=0;i<4;i++)circ(54+((i*6+d)%18),-27,1,TINTA);},
        frente(){raya(20,-26,hx,hy,"#c7cede",2.4);circ(20,-26,2.6,TINTA);circ(hx,hy,2.4,ROJO);}};
    },
  });

  // ---- leer
  pon("leer",{
    pergamino(T,s){                      // se desenrolla hasta el piso y se va rodando
      const f=ciclo(s,4.5),L=Math.min(1,f/.7),fl=Math.max(0,(L-.4)/.6),yb=-44+Math.min(L,.4)/.4*42;
      return {cara:f>.7?"wow":"enfocado",mira:Math.sin(T*1.4)*2+1,incl:-.05+L*.12,brD:[26,-44],brI:[18,-44],
        frente(){caja(14,-48,18,4,2,"#c9a76b");caja(16,-44,14,yb+44,0,"#f6ecd2");for(let y=-40;y<yb-2;y+=5)raya(18,y,28,y,"#b9a27a",1);
          if(fl>0)caja(16,-4,14+fl*44,3.6,0,"#f6ecd2");const rx=23+fl*44;circ(rx,-4,4,"#e8d8b0");aro(rx,-4,4,"#c9a76b",1.2);}};
    },
    periodico(T,s){                      // detrás del periódico; lo baja para espiar
      const f=ciclo(s,3.2),baja=f>.6&&f<.85?Math.sin((f-.6)/.25*Math.PI)*15:0;
      if(baja>11)em(1200,10,-66,"👀","#fff");
      return {cara:"enfocado",mira:baja>5?4:2,incl:baja>5?.08:0,brD:[36,-38+baja],brI:[-2,-38+baja],
        frente(){const y=-64+baja;caja(-6,y,46,30,1,"#eceae2");marco(-6,y,46,30,1,"#8d93a8",1);raya(17,y,17,y+30,"#c9cedb",1);caja(-3,y+3,17,5,0,TINTA);for(let i=0;i<4;i++){raya(-3,y+11+i*4,14,y+11+i*4,"#9aa3bb",1);raya(20,y+4+i*6,37,y+4+i*6,"#9aa3bb",1);}caja(20,y+20,15,7,0,"#c9cedb");}};
    },
    lejos(T){                            // ni de cerca ni de lejos: no ve
      const k=(Math.sin(T*1.6)+1)/2,px=16+k*34;
      if(k>.9)em(1500,px,-60,"?",AMAR);
      return {cara:k<.25||k>.85?"apretado":"enfocado",mira:2,incl:k<.25?.14:-.06,brD:[px-2,-42],brI:[px-8,-40],
        frente(){caja(px-4,-52,12,16,1,"#fffaf0");marco(px-4,-52,12,16,1,"#c9b28f",1);for(let i=0;i<4;i++)raya(px-2,-48+i*3,px+6,-48+i*3,TINTA+"88",.8);}};
    },
    tablet(T,s){                         // desliza sin parar… hasta que algo le llama la atención
      const f=ciclo(s,2.6),par=f>=.7,sc=par?0:T*60;
      if(par)em(900,30,-60,"!",AMAR);
      return {cara:par?"wow":"enfocado",mira:2.5,incl:.1,brI:[22,-30],brD:[30,par?-34:-38+((T*6)%1)*8],
        frente(){caja(18,-46,20,28,3,"#2b3048");caja(20,-44,16,24,1.5,"#dfe9ff");g.save();camino(20,-44,16,24,1.5);g.clip();for(let i=0;i<8;i++){const y=-44+((i*7-sc)%56+56)%56-4;caja(22,y,i%3?12:8,2.4,1,i%3?"#9aa3bb":AZUL);}g.restore();}};
    },
    alreves(T,s){                        // lee el libro al revés… hasta que se da cuenta
      const f=ciclo(s,4),r=f<.55?Math.PI:f<.7?Math.PI*(1-(f-.55)/.15):0;
      if(f<.5)em(1400,12,-66,"?",AMAR);if(f>.7&&f<.8)em(600,30,-60,"💡",AMAR);
      return {cara:f<.55?"enfocado":"feliz",mira:2,incl:f<.55?Math.sin(T*1.3)*.15:.05,rubor:f>.7,brD:[26,-28],brI:[10,-28],
        frente(){g.save();g.translate(17,-24);g.rotate(r);caja(-15,-9,30,16,2,ROJO);caja(-13,-11,12.5,15,1,"#fffaf0");caja(.5,-11,12.5,15,1,"#fffaf0");caja(-11,-9,7,4,0,AZUL);for(let i=0;i<2;i++){raya(-11,-3+i*4,-3,-3+i*4,TINTA+"99",1);raya(3,-7+i*4,11,-7+i*4,TINTA+"99",1);}g.restore();}};
    },
  });

  // ---- programar
  pon("teclear",{
    furioso(T){                          // modo hacker: las teclas salen volando
      const a=Math.sin(T*40)*3,b=Math.cos(T*37)*3;
      em(150,30+Math.random()*16,-22,["■","▪","◆"][Math.floor(Math.random()*3)],"#dfe3ee",-60);em(700,42,-26,"💨","#c9cedb",-20);
      return {cara:"apretado",pelo:true,boca:.6,mira:2,incl:.12,brD:[34+a,-21+b],brI:[24-b,-21+a],sube:Math.abs(Math.sin(T*20))*1.5,
        atras(){caja(12,-14,44,14,2,MADERA);raya(16,0,16,-14,MADERA,2.4);raya(52,0,52,-14,MADERA,2.4);},
        frente(){caja(18,-18,32,4,1.5,"#9aa3bb");for(let i=0;i<4;i++)caja(20+i*7.4,-17.4,5.4,1.4,.5,Math.sin(T*30+i*2)>0?"#fff":"#dfe3ee");g.save();g.translate(50,-17);g.rotate(.18);caja(-3,-24,3,24,1,"#9aa3bb");caja(-2.6,-23,2,22,1,Math.sin(T*12)>0?"#ff5d7388":"#5bc0ff88");g.restore();}};
    },
    pulpo(T){                            // le salen cuatro brazos más: café, teléfono, dona y apuntes
      const M=[0,1,2,3].map(i=>[-4+i*4,-28+i,24+i*8+Math.sin(T*1.8+i)*3,-46+i*4+Math.sin(T*2.2+i*1.7)*3]);
      const cosas=[(x,y)=>{caja(x-3,y-8,6,7,1.5,"#fff");marco(x-3,y-8,6,7,1.5,TINTA,1);humito(x,y-9,T,"#d7dbe6",2);},(x,y)=>{caja(x-2.5,y-10,5,9,1.4,TINTA);caja(x-1.8,y-9,3.6,6,.6,AZUL);},(x,y)=>{aro(x,y-5,3.2,"#e7b15a",2.6);aro(x,y-5,3.2,ROSA,1.2,Math.PI,0);},(x,y)=>{caja(x-4,y-11,8,10,.6,"#fffaf0");for(let j=0;j<3;j++)raya(x-3,y-9+j*3,x+3,y-9+j*3,TINTA+"88",.8);}];
      return {cara:"feliz",mira:2,incl:.04,brD:[30,-20-(Math.sin(T*22)>0?2:0)],brI:[20,-20-(Math.sin(T*22+2)>0?2:0)],
        atras(){caja(12,-14,46,14,2,MADERA);for(const [ox,oy,hx,hy] of M){g.beginPath();g.moveTo(ox,oy);g.quadraticCurveTo(ox+6,hy-10,hx,hy);g.strokeStyle=TINTA;g.lineWidth=2.6;g.lineCap="round";g.stroke();}},
        frente(){caja(18,-18,30,3,1.5,"#9aa3bb");M.forEach(([,,hx,hy],i)=>{cosas[i](hx,hy);circ(hx,hy,2.8,CABEZA);aro(hx,hy,2.8,TINTA,1);});}};
    },
    undedo(T,s){                         // con un solo dedo, tecla por tecla, sudando
      const f=ciclo(s,1.3),k=f<.7?ease(f/.7):1-ease((f-.7)/.3),y=-21-k*30,x=30-k*4;
      if(f>.95||f<.04)em(600,30,-26,"✦",AMAR,-10);em(2600,-14,-58,"💧",AZUL,14);
      return {cara:"enfocado",boca:.25,mira:2+Math.sin(T*.8)*1.5,incl:.14,brD:[x,y],brI:[-14,-16],
        atras(){caja(12,-14,42,14,2,MADERA);},
        frente(){caja(18,-17,28,3,1.5,"#9aa3bb");for(let i=0;i<3;i++)caja(20+i*8,-16.6,6,1.2,.5,"#dfe3ee");raya(x,y,x+2,y+5,CABEZA,2.2);}};
    },
    piano(T){                            // teclea como concertista, con los ojos cerrados
      const sw=Math.sin(T*2.4);em(450,30+sw*10,-46,["♪","♫","♬"][Math.floor(T*3)%3],COLORES[Math.floor(T*2)%6],-30);
      return {cara:"dormido",rubor:true,boca:.2,incl:sw*.2,dx:sw*2,mira:1,brD:[36+Math.sin(T*9)*5,-22-(Math.sin(T*18)>0?3:0)],brI:[22+Math.sin(T*7)*4,-22-(Math.sin(T*18+1)>0?3:0)],
        atras(){caja(12,-16,48,16,2,TINTA);raya(18,0,18,-16,TINTA,3);raya(54,0,54,-16,TINTA,3);},
        frente(){caja(16,-20,40,5,1,"#fff");for(let i=0;i<8;i++)raya(16+i*5,-20,16+i*5,-15,"#c9cedb",.8);for(const i of [1,2,4,5,6])caja(15+i*5,-20,2.6,3,0,TINTA);}};
    },
    bloques(T,s){                        // apila bloques de código… y se le caen
      const f=ciclo(s,5.5),n=Math.min(6,1+Math.floor(f*8)),cae=f>.78?(f-.78)/.22:0;
      if(cae>0&&cae<.3)em(500,40,-50,"!",ROJO);
      return {cara:cae?"wow":"enfocado",pelo:cae>0&&cae<.5,mira:2,incl:.06,brD:cae?[16,-42]:[30,-14-n*8],brI:cae?[-16,-42]:[-14,-18],
        frente(){g.save();g.translate(40,0);g.rotate(cae*1.3);for(let i=0;i<n;i++)caja(-8+(i%2)*2,-8.4-i*8.4,16,8,1.5,COLORES[i%6]);g.restore();}};
    },
  });

  // ---- escribir el guion
  pon("escribir",{
    maquina(T,s){                        // máquina de escribir: ¡ding! y regresa el carro de golpe
      const f=ciclo(s,3),c=f<.85?f/.85:1-(f-.85)/.15,tec=f<.85&&Math.sin(T*26)>0;
      if(f>.85&&f<.9)em(500,48,-52,"¡ding!",AMAR);
      return {cara:f>.85?"feliz":"enfocado",mira:2,incl:.06,brD:f>.85?[44,-34]:[30,-24-(tec?2:0)],brI:[22,-24-(tec?0:2)],
        atras(){caja(12,-12,44,12,2,MADERA);},
        frente(){const ox=-c*12;caja(18,-26,30,12,3,"#3c4259");marco(18,-26,30,12,3,TINTA,1.2);caja(14+ox,-30,40,4,2,"#6f7892");caja(22+ox,-46,22,17,0,"#fffaf0");for(let i=0;i<3;i++)raya(24+ox,-43+i*4,24+ox+(i<2?18:18*c),-43+i*4,TINTA+"99",1);raya(54+ox,-30,58+ox,-36,"#9aa3bb",1.6);for(let i=0;i<4;i++)circ(23+i*7,-18,2,"#dfe3ee");}};
    },
    bolas(T,s){                          // no le gusta: hecha bola y para atrás; la pila crece
      const f=ciclo(s,3),n=Math.min(7,Math.floor(s/3)),tira=f>.65,k=tira?(f-.65)/.35:0,bx=24-k*70,by=-36-Math.sin(k*Math.PI)*40+k*32;
      const pila=()=>{for(let i=0;i<n;i++){const x=-38-(i%3)*8,y=-4-Math.floor(i/3)*7;circ(x,y,4,"#fffaf0");aro(x,y,4,"#c9cedb",1);}};
      return {cara:f<.5?"enfocado":f<.65?"apretado":"normal",mira:f<.65?2:-3,incl:tira?-.08:.05,brD:f<.5?[24+((T*20)%10),-30]:f<.65?[26,-34]:[24-k*8,-48],brI:[-14,-18],
        atras:pila,
        frente(){if(f<.5){caja(16,-36,22,14,1,"#fffaf0");for(let i=0;i<2;i++)raya(18,-32+i*5,18+((T*20)%18)*(i?1:.8),-32+i*5,TINTA+"99",1);}else if(!tira){circ(26,-34,5+Math.sin(T*30),"#fffaf0");aro(26,-34,5,"#c9cedb",1);}else{circ(bx,by,4,"#fffaf0");aro(bx,by,4,"#c9cedb",1);}}};
    },
    tintero(T,s){                        // pluma de ave… y la tinta le salpica la cara
      const f=ciclo(s,4),spl=f>.7,px=22+((T*18)%16);
      if(f>.7&&f<.74)em(500,8,-56,"¡splash!","#9aa3bb",-10);
      return {cara:spl?"apretado":"enfocado",mira:2,incl:spl?Math.sin(T*30)*.08:.06,brD:spl?[12,-46]:[px,-30],brI:[-14,-18],
        atras(){caja(12,-22,40,22,2,MADERA);caja(14,-26,30,5,1,"#f6ecd2");caja(44,-30,8,8,2,"#2b3048");},
        frente(){if(!spl){g.save();g.translate(px,-32);g.rotate(-.5);g.beginPath();g.moveTo(0,0);g.quadraticCurveTo(4,-12,1,-22);g.quadraticCurveTo(-5,-12,0,0);g.fillStyle="#fff";g.fill();g.restore();raya(16,-24,px,-24,TINTA+"aa",1);}
          else{elip(5,-48,7,5,"#1b1f2e");circ(-1,-43,2,"#1b1f2e");circ(12,-53,1.6,"#1b1f2e");}}};
    },
  });

  // ---- buscar
  pon("buscar",{
    cajon(T,s){                          // revuelve el cajón: calcetín, hueso, tuerca, plátano, llave…
      const k=ciclo(s,.9),o=Math.floor(s/.9)%5,it=["🧦","🦴","⚙","🍌","🔑"][o],x=30-k*84,y=-26-Math.sin(k*Math.PI)*48+k*20;
      return {cara:"enfocado",mira:2,incl:.25,dx:2,brD:[32+Math.sin(T*16)*4,-18],brI:[26,-20+Math.cos(T*14)*3],sube:-1,
        atras(){caja(20,-30,40,30,2,MADERA);marco(20,-30,40,30,2,"#7f5a38",1.2);caja(22,-28,36,12,1,"#8d6a4a");caja(16,-14,46,10,1,"#c9935f");circ(39,-9,1.8,TINTA);},
        frente(){if(k<.95)letra(it,x,y,11,"#fff");}};
    },
    detector(T){                         // detector de metales: ¡bip!
      const a=Math.sin(T*1.8),x=38+a*18,bip=Math.abs(a)<.22;
      if(bip)em(400,x,-12,"¡bip!",AMAR,-30);
      return {cara:bip?"wow":"enfocado",mira:3,incl:.18,brD:[22,-26],brI:[16,-26],
        frente(){raya(20,-26,x,-4,"#9aa3bb",2.2);elip(x,-3,8,2.4,"#3c4259");aro(x,-3,8,"#9aa3bb",1);caja(18,-31,7,6,1.5,TINTA);circ(21.5,-28,1.3,bip?ROJO:VERDE);if(bip)for(let i=1;i<3;i++)aro(x,-3,8+i*5+((T*10)%5),AMAR+"88",1.2,Math.PI,0);}};
    },
    binoculares(T,s){                    // de vez en cuando los agarra al revés
      const a=Math.sin(T*1.2),rev=ciclo(s,6)>.7;
      if(rev)em(1200,20,-66,"¿?",AMAR);
      return {cara:rev?"wow":"normal",mira:3,incl:a*.12,dx:a*3,brD:[22,-44],brI:[14,-44],
        frente(){g.save();g.translate(17,-48);g.rotate(a*.12);for(const y of [-4,4]){caja(rev?6:0,y-3.5,rev?8:13,7,2,"#6f7892");marco(rev?6:0,y-3.5,rev?8:13,7,2,TINTA,1);circ(rev?6:13,y,rev?1.8:4,"#9fd8ff");}g.restore();}};
    },
    perro(T){                            // un perrito robot olfatea y lo jala de la correa
      const tira=Math.sin(T*2)>.3,d=tira?6:0,px=46+d+Math.sin(T*8)*1.5,hb=Math.abs(Math.sin(T*10))*2;
      em(900,56,-10,"snif","#fff",-14);
      return {cara:tira?"wow":"feliz",mira:2,incl:tira?.14:0,pies:tira?[4,9]:[Math.sin(T*6)*3,-Math.sin(T*6)*3],brD:[20+d,-24],brI:[-14,-18],
        frente(){raya(20+d,-24,px-4,-14+hb,ROJO,1.2);caja(px-8,-16+hb,18,9,4,"#c7cede");marco(px-8,-16+hb,18,9,4,TINTA,1);caja(px+6,-14+hb*1.5,10,7,3,"#c7cede");circ(px+16,-9+hb*1.5,1.6,TINTA);circ(px+10,-12+hb*1.5,1,TINTA);raya(px+7,-14+hb,px+5,-19+Math.sin(T*16)*2,"#9aa3bb",1.6);for(const q of [-5,5])raya(px+q,-8+hb,px+q+Math.sin(T*12+q)*2,0,TINTA,2);raya(px-8,-13+hb,px-13,-18+Math.sin(T*20)*3,TINTA,1.6);}};
    },
  });

  // ---- investigar en la web
  pon("libros",{
    torre(T,s){                          // torre de libros que se tambalea; saca uno de en medio
      const f=ciclo(s,3),w=Math.sin(T*3)*(.04+(f>.4&&f<.7?.08:0)),saca=f>.4&&f<.7?(f-.4)/.3*14:f>=.7?14:0;
      if(f>.45&&f<.7)em(700,40,-80,"!",ROJO,-10);
      return {cara:f>.4&&f<.7?"apretado":"wow",mira:2,incl:-.05,brD:[30-saca*.6,-36],brI:[-14,-20],
        atras(){g.save();g.translate(42,0);g.rotate(w);for(let i=0;i<10;i++){const x=-12+Math.sin(i*2.1)*3+(i===4?-saca:0);caja(x,-7-i*7,24,6.4,1.5,COLORES[i%6]);}g.restore();},
        frente(){if(f>=.7)caja(6,-38,16,6,1.5,COLORES[4]);}};
    },
    lluvia(T,s){                         // le llueven libros en la cabeza
      const f=ciclo(s,1.4),y=-110+f*f*62,golpe=f>.9;
      if(golpe)em(500,0,-70,"¡toc!",AMAR,-20);
      return {cara:golpe?"apretado":"wow",mira:0,incl:-.15,sube:golpe?-2:0,brD:[12,-58],brI:[-12,-58],pies:[-3,3],
        atras(){const n=Math.min(6,Math.floor(s/1.4));for(let i=0;i<n;i++)caja(-44+(i%2)*4,-6-i*6,22,5.6,1.4,COLORES[(i+2)%6]);},
        frente(){if(!golpe){g.save();g.translate(2,y);g.rotate(f*4);caja(-10,-3,20,6,1.5,COLORES[Math.floor(s/1.4)%6]);g.restore();}}};
    },
    corcho(T){                           // tablero de conspiración con hilo rojo
      const p=Math.floor(T*1.5)%4,PT=[[32,-62],[58,-54],[40,-36],[62,-30]];
      return {cara:"wow",pelo:Math.sin(T*.7)>.6,boca:.4+.3*Math.sin(T*9),mira:3,brD:[PT[p][0]-6,PT[p][1]+4],brI:[-16,-22],incl:.06,
        atras(){caja(22,-72,50,52,2,"#c9935f");marco(22,-72,50,52,2,"#7f5a38",2);raya(30,-20,28,0,"#7f5a38",2.4);raya(64,-20,66,0,"#7f5a38",2.4);
          for(const [x,y] of PT)caja(x-5,y-5,10,8,1,"#fffaf0");g.beginPath();g.moveTo(...PT[0]);for(const q of [1,2,3,0,2])g.lineTo(...PT[q]);g.moveTo(...PT[1]);g.lineTo(...PT[3]);g.strokeStyle=ROJO;g.lineWidth=1.2;g.stroke();for(const [x,y] of PT)circ(x,y-4,1.8,ROJO);}};
    },
  });

  // ---- navegar
  pon("navegar",{
    barco(T){                            // barquito de papel con catalejo
      const o=Math.sin(T*2.2);em(1500,44,-60,"🏝","#fff",-6);
      return {cara:"enfocado",mira:3,sube:6+o*3,incl:o*.1,brD:[22,-48],brI:[16,-46],
        atras(){g.beginPath();g.moveTo(-60,4);for(let x=-60;x<=70;x+=4)g.lineTo(x,-Math.sin(x*.08+T*2.4)*3-4);g.lineTo(70,4);g.closePath();g.fillStyle=AZUL+"cc";g.fill();
          g.beginPath();g.moveTo(-8,-6+o*3);g.lineTo(-30,-6+o*3);g.lineTo(-8,-40+o*3);g.closePath();g.fillStyle="#fffaf0";g.fill();raya(-8,-6+o*3,-8,-42+o*3,"#c9cedb",1.4);},
        frente(){g.save();g.translate(0,3-o*3);g.rotate(o*.08);g.beginPath();g.moveTo(-30,-8);g.lineTo(30,-8);g.lineTo(20,4);g.lineTo(-20,4);g.closePath();g.fillStyle="#fffaf0";g.fill();g.strokeStyle="#c9cedb";g.lineWidth=1;g.stroke();g.restore();
          g.save();g.translate(18,-50);g.rotate(-.12);caja(0,-2.5,22,5,2,"#c9935f");caja(18,-3.5,6,7,1.5,"#7f5a38");g.restore();}};
    },
    liana(T){                            // a lo Tarzán
      const a=Math.sin(T*2.2)*.7,x=Math.sin(a)*42,y=(1-Math.cos(a))*42;
      em(1800,0,-64,"¡aaah!",AMAR,-8);
      return {cara:"wow",boca:.8,dx:x,sube:y,rota:a*.5,brD:[4,-58],brI:[-4,-58],pies:[-4,6],
        atras(){g.beginPath();g.moveTo(0,-130);g.quadraticCurveTo(x*.4,-90,x+2,-60-y);g.strokeStyle="#5f8f3a";g.lineWidth=2.4;g.stroke();for(let i=0;i<4;i++)elip(-20+i*14,-128+(i%2)*4,8,3,"#6fbf73",.3*i);}};
    },
    alfombra(T){                         // alfombra voladora
      const o=Math.sin(T*2.6),h=14+o*4,y0=-h-5;
      em(500,-30+Math.random()*60,-2,"✦",AMAR,10);
      return {cara:"feliz",sentado:true,mira:2,sube:h,incl:o*.06,brD:[18,-32],brI:[-16,-32],
        frente(){const ola=x=>Math.sin(x*.15+T*6)*2;g.beginPath();for(let x=-30;x<=30;x+=3){const y=y0+ola(x);x===-30?g.moveTo(x,y):g.lineTo(x,y);}for(let x=30;x>=-30;x-=3)g.lineTo(x,y0+5+ola(x));g.closePath();g.fillStyle=LILA;g.fill();for(let x=-30;x<=30;x+=6)raya(x,y0+5+ola(x),x,y0+8+ola(x),AMAR,1.2);}};
    },
  });

  // ---- revisar una imagen
  pon("lupa",{
    jurado(T,s){                         // jurado de concurso: alza su cartulina de estrellas
      const f=ciclo(s,3.5),alza=f>.55,n=1+Math.floor(s/3.5)%3;
      if(alza)em(1100,40,-60,"★".repeat(n),AMAR,-10);
      return {cara:alza?"feliz":"enfocado",mira:2,incl:alza?0:Math.sin(T*1.5)*.12,brD:alza?[28,-48]:[8,-32],brI:[-14,-18],
        atras(){caja(38,-42,26,22,1,"#fffaf0");marco(38,-42,26,22,1,MADERA,2);elip(48,-30,6,5,ROSA);elip(56,-33,5,4,AZUL);raya(51,-20,51,0,MADERA,2);},
        frente(){if(alza){raya(28,-48,28,-56,MADERA,1.8);caja(18,-74,20,18,2,"#fff");marco(18,-74,20,18,2,TINTA,1);for(let i=0;i<n;i++)letra("★",28+(i-(n-1)/2)*6,-65,7,AMAR);}}};
    },
    microscopio(T,s){
      const ok=ciclo(s,4)>.75;if(ok)em(800,30,-62,"✓",VERDE);
      return {cara:ok?"feliz":"apretado",mira:3,incl:.32,dx:3,brD:[34,-36+Math.sin(T*3)],brI:[24,-20],
        atras(){caja(20,-6,30,6,2,"#6f7892");raya(26,-6,26,-40,"#6f7892",4);g.save();g.translate(26,-42);g.rotate(.5);caja(-3,-2,8,22,2,"#9aa3bb");g.restore();caja(24,-24,22,3,1,"#3c4259");circ(36,-25,3,ok?VERDE:"#9fd8ff");circ(34,-36,3,TINTA);}};
    },
    torcido(T,s){                        // endereza el cuadro… y se vuelve a torcer
      const f=ciclo(s,3),r=f<.4?.35*(1-f/.4):f<.7?0:-(f-.7)/.3*.3;
      if(f>.75)em(1200,40,-70,"¬¬","#fff",-6);
      return {cara:f<.4?"enfocado":f<.72?"feliz":"apretado",mira:3,incl:f>.72?-.1:0,brD:f<.4?[30,-50]:[16,-16],brI:[-14,-18],
        atras(){g.save();g.translate(44,-64);g.rotate(r);raya(0,0,-8,10,"#7f5a38",1);raya(0,0,8,10,"#7f5a38",1);caja(-14,10,28,22,1,"#fffaf0");marco(-14,10,28,22,1,MADERA,2.4);elip(-3,22,6,5,VERDE);circ(6,17,3,AMAR);g.restore();circ(44,-64,1.6,TINTA);}};
    },
    foto(T,s){                           // fotógrafo de antes: ¡flash!
      const f=ciclo(s,2.6),fl=f>.8&&f<.88;
      return {cara:fl?"wow":"enfocado",mira:3,incl:.1,brD:[26,-40],brI:[16,-54],
        atras(){raya(30,0,36,-30,MADERA,2);raya(46,0,38,-30,MADERA,2);},
        frente(){caja(22,-46,22,16,2,"#2b3048");caja(42,-42,8,8,2,"#3c4259");circ(46,-38,3,"#9fd8ff");raya(16,-54,14,-60,"#9aa3bb",1.6);caja(8,-66,12,6,1,"#c7cede");if(fl){g.globalAlpha=.7;circ(14,-62,24,"#fff");g.globalAlpha=1;}}};
    },
  });

  // ---- pintar (imágenes)
  pon("pintar",{
    rodillo(T,s){
      const y=-50+(Math.sin(T*3)+1)*18,n=Math.min(5,Math.floor(s/1.2)+1);em(1600,24,-20,"•",ROSA,30);
      return {cara:"feliz",mira:2,brD:[24,y+6],brI:[18,y+10],
        atras(){caja(30,-64,34,62,1,"#fffaf0");for(let i=0;i<n;i++)caja(31+i*6.4,-64,6.4,62,0,COLORES[(i+1)%6]+"cc");caja(-36,-10,16,10,2,"#9aa3bb");elip(-28,-10,7,2,ROSA);},
        frente(){raya(24,y+6,30,y,"#6f7892",2);caja(28,y-8,6,18,3,COLORES[(n+1)%6]);}};
    },
    salpica(T,s){                        // a lo Pollock
      const f=ciclo(s,1),lanza=f<.3;
      return {cara:lanza?"apretado":"feliz",pelo:true,mira:2,incl:lanza?.15:-.05,brD:lanza?[34,-30]:[10,-52],brI:[-16,-30],
        atras(){caja(30,-58,34,56,1,"#fffaf0");for(let i=0;i<Math.min(24,Math.floor(s*4));i++){const x=34+((i*37)%28),y=-54+((i*53)%50);elip(x,y,2+(i%3),1.4+(i%2),COLORES[i%6],i);}},
        frente(){const hx=lanza?34:10,hy=lanza?-30:-52;caja(hx-4,hy-10,8,10,1.5,"#9aa3bb");if(lanza)for(let i=0;i<4;i++)circ(38+f*60+i*4,-34+f*20+i*2,1.8,COLORES[(i+Math.floor(s))%6]);}};
    },
    espray(T,s){                         // grafiti: dibuja un corazón con aerosol
      const k=Math.min(1,ciclo(s,4)/.8),a=k*Math.PI*2;
      return {cara:"enfocado",mira:2,brD:[28+Math.cos(a)*5,-40+Math.sin(a)*5],brI:[-14,-18],
        atras(){caja(32,-64,38,60,1,"#9aa3bb");for(let y=-56;y<-6;y+=8)raya(32,y,70,y,"#8791ad",1);g.save();g.beginPath();g.rect(32,-64,38,60);g.clip();const n=Math.floor(k*30);for(let i=0;i<n;i++){const t=i/30*Math.PI*2,x=51+15*Math.pow(Math.sin(t),3),y=-36-(13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t));circ(x,y,2.8,ROSA);}g.restore();},
        frente(){caja(26+Math.cos(a)*5,-46+Math.sin(a)*5,6,12,2,ROJO);circ(29+Math.cos(a)*5,-47+Math.sin(a)*5,1.5,"#fff");}};
    },
  });

  // ---- grabar la voz
  pon("grabar",{
    opera(T,s){                          // nota de ópera… y la copa se rompe
      const f=ciclo(s,5),cr=f>.7;
      if(cr&&f<.74)em(500,54,-34,"¡crash!","#9fd8ff",-10);
      return {cara:"dormido",boca:.6+.4*Math.abs(Math.sin(T*3)),rubor:true,incl:-.12,mira:1,brD:[30,-46],brI:[-18,-30],
        frente(){for(let i=1;i<=3;i++)aro(16,-35,6+i*6+((T*20)%6),AZUL+"66",1.4,-.6,.6);const sh=cr?0:Math.sin(T*50)*f*2;caja(46,-14,14,14,1,MADERA);
          if(!cr){g.save();g.translate(53+sh,-14);g.beginPath();g.moveTo(-5,-18);g.lineTo(5,-18);g.lineTo(2,-8);g.lineTo(2,-2);g.lineTo(-2,-2);g.lineTo(-2,-8);g.closePath();g.fillStyle="#dff4ff99";g.fill();g.strokeStyle="#9fd8ff";g.lineWidth=1;g.stroke();g.restore();}
          else for(let i=0;i<5;i++)caja(46+i*3.4,-16+(i%2)*2,2.6,2,0,"#9fd8ff");}};
    },
    rap(T){
      const b=Math.abs(Math.sin(T*6));em(800,-10,-60,["yo","¡eh!","♪"][Math.floor(T)%3],AMAR,-20);
      return {cara:"enfocado",boca:Math.abs(Math.sin(T*12))*.8,sube:b*3,incl:Math.sin(T*6)*.08,mira:2,brD:[16,-40],brI:[-22+Math.sin(T*6)*6,-36-b*8],pies:[b*3,-b*3],
        frente(){caja(13,-46,7,9,3,"#6f7892");marco(13,-46,7,9,3,TINTA,1);raya(16,-37,14,-28,"#6f7892",2);for(let i=0;i<3;i++)circ(15+i*1.5,-44+i*2,.8,"#9aa3bb");}};
    },
    ducha(T){                            // canta en la regadera, con patito
      em(900,14,-50,"♪",LILA);
      return {cara:"feliz",boca:.3+.4*Math.abs(Math.sin(T*5)),rubor:true,incl:Math.sin(T*2)*.1,brD:[18,-40],brI:[-20,-50],
        atras(){raya(-30,0,-30,-100,"#9aa3bb",2.4);raya(-30,-100,0,-100,"#9aa3bb",2.4);caja(-8,-104,16,6,3,"#c7cede");g.globalAlpha=.18;caja(-34,-96,70,96,4,AZUL);g.globalAlpha=1;},
        frente(){caja(15,-48,6,9,3,AMAR);elip(32,-5,6,4,AMAR);circ(36,-10,3,AMAR);raya(38.5,-10,41.5,-9,"#ff9a1f",1.6);circ(37,-11,.8,TINTA);for(let i=0;i<6;i++){const y=-96+((T*80+i*20)%92);elip(-8+i*3.2,y,1,2,AZUL);}}};
    },
  });

  // ---- mezclar sonido
  pon("dj",{
    maracas(T){
      const a=Math.sin(T*10),b=Math.abs(Math.sin(T*5));em(400,0,-60,"♪",COLORES[Math.floor(T*3)%6],-26);
      return {cara:"feliz",boca:.4,sube:b*4,incl:Math.sin(T*5)*.1,pies:[a*3,-a*3],brD:[20,-40+a*6],brI:[-20,-40-a*6],
        frente(){for(const [x,y,c] of [[20,-40+a*6,ROJO],[-20,-40-a*6,VERDE]]){raya(x,y,x,y-8,MADERA,2);elip(x,y-12,4.5,6,c);for(let i=0;i<3;i++)circ(x-3+i*3,y-12,1,AMAR);}}};
    },
    bateria(T){
      const a=Math.sin(T*12)>0,b=Math.sin(T*12+1.6)>0,pl=Math.sin(T*3)>.8;
      if(pl)em(300,52,-50,"¡tsss!",AMAR,-20);
      const hD=a?[30,-28]:[34,-40],hI=b?[18,-24]:[22,-34];
      return {cara:"apretado",pelo:pl,boca:.4,sentado:true,mira:2,sube:2,incl:.06+(a?.04:0),brD:hD,brI:hI,
        atras(){caja(-10,-12,14,10,2,"#6f7892");elip(54,-44,12,2.4,"#e7c56b");raya(54,-44,54,0,"#9aa3bb",1.4);},
        frente(){elip(32,-11,14,11,ROJO);elip(32,-11,10,8,"#fff");elip(20,-27,8,3,"#dfe3ee");raya(hD[0],hD[1],hD[0]+(a?-8:-4),hD[1]+(a?2:-6),MADERA,1.8);raya(hI[0],hI[1],hI[0]+(b?10:8),hI[1]+(b?-2:-6),MADERA,1.8);}};
    },
    eq(T){                               // baile robot frente al ecualizador gigante
      const b=Math.sin(T*8);
      return {cara:"feliz",boca:.3,sube:Math.abs(b)*3,incl:b*.12,brD:[18+b*4,-36-Math.abs(b)*10],brI:[-18,-36+Math.abs(b)*10],pies:[b*4,-b*4],
        atras(){for(let i=0;i<7;i++){const h=8+Math.abs(Math.sin(T*(5+i)+i*1.3))*44;for(let y=0;y<h;y+=5)caja(24+i*7,-y-4,5,3.4,.6,y>40?ROJO:y>28?AMAR:VERDE);}}};
    },
  });

  // ---- bajar clips
  pon("claqueta",{
    carrete(T,s){                        // pesca la película de un hoyo, como caña
      const a=T*6,n=Math.min(8,Math.floor(s*2));em(1200,58,-6,"✦",AZUL,-24);
      return {cara:"apretado",mira:3,incl:-.1,brD:[18+Math.cos(a)*5,-30+Math.sin(a)*5],brI:[10,-34],pies:[-3,4],
        atras(){for(let i=0;i<n;i++){caja(-38,-4-i*5,24,4.4,1,"#2b3048");for(let j=0;j<4;j++)caja(-36+j*6,-3-i*5,3.4,2.4,.4,"#fff");}},
        frente(){circ(18,-30,8,"#3c4259");aro(18,-30,8,TINTA,1.4);for(let i=0;i<4;i++){const u=a+i*1.57;circ(18+Math.cos(u)*4.5,-30+Math.sin(u)*4.5,1.6,"#9aa3bb");}
          g.beginPath();g.moveTo(18,-38);g.quadraticCurveTo(40,-52,58,-2);g.strokeStyle="#2b3048";g.lineWidth=5;g.stroke();elip(58,0,12,2.6,"#10131b");}};
    },
    palomitas(T){                        // ve el clip con palomitas
      const come=Math.sin(T*2.4)>.4;em(500,22,-34,"●","#fff4c0",-50);
      return {cara:"wow",mira:3,boca:come?.6:.15,brD:come?[8,-36]:[20,-24],brI:[16,-22],
        atras(){caja(38,-58,32,22,2,"#10131b");caja(40,-56,28,18,1,Math.sin(T*9)>0?"#5bc0ff":"#7fd1c0");raya(54,-36,54,0,"#3c4259",2);},
        frente(){g.beginPath();g.moveTo(12,-30);g.lineTo(28,-30);g.lineTo(25,-12);g.lineTo(15,-12);g.closePath();g.fillStyle="#fff";g.fill();for(let i=0;i<3;i++)caja(14.5+i*4.5,-30,2.4,18,0,ROJO);for(let i=0;i<5;i++)circ(13+i*3.6,-31-(i%2)*2,2.6,"#fff4c0");}};
    },
    cine(T){                             // cámara de manivela de los años 20
      const a=T*6;em(900,50,-30,"🎞","#fff",-20);
      return {cara:"enfocado",mira:2,brD:[30+Math.cos(a)*5,-36+Math.sin(a)*5],brI:[-14,-18],
        atras(){raya(30,0,36,-26,MADERA,2.2);raya(48,0,40,-26,MADERA,2.2);},
        frente(){caja(28,-44,22,18,2,"#3c4259");for(const x of [32,46]){circ(x,-50,6,"#2b3048");g.save();g.translate(x,-50);g.rotate(a);raya(-5,0,5,0,"#9aa3bb",1);raya(0,-5,0,5,"#9aa3bb",1);g.restore();}caja(50,-40,6,8,1,"#2b3048");circ(30,-36,2,"#9aa3bb");}};
    },
  });

  // ---- renderizar y esperar el render
  pon("rueda",{
    bici(T){                             // pedalea una bici fija que prende un foco
      const a=T*8,p=Math.sin(a)*6;em(900,-16,-58,"💧",AZUL,14);
      return {cara:"apretado",mira:2,incl:.18,sube:4,pies:[p,-p],brD:[24,-32],brI:[18,-32],
        atras(){raya(-2,-2,0,-20,"#79829b",3);caja(-6,-22,12,3,1.5,TINTA);raya(0,-20,24,-32,"#79829b",2.4);raya(-2,-2,32,-2,"#79829b",3);circ(32,-9,9,"#3c4259");g.save();g.translate(32,-9);g.rotate(a);raya(-8,0,8,0,"#9aa3bb",1);raya(0,-8,0,8,"#9aa3bb",1);g.restore();raya(32,-9,54,-16,"#3c4259",1.2);circ(58,-21,5,Math.sin(T*8)>0?AMAR:"#ffe98a88");caja(55,-17,6,4,1,"#9aa3bb");}};
    },
    horno(T,s){                          // hornea los cuadros como pan
      const f=ciclo(s,4),ab=f>.8;if(ab)em(500,44,-46,"🎞","#fff",-30);
      return {cara:ab?"feliz":"wow",gorro:"chef",mira:3,incl:ab?0:.2,dx:ab?0:3,brD:ab?[44,-30]:[18,-20],brI:[-14,-18],
        atras(){caja(24,-48,40,48,3,"#6f7892");marco(24,-48,40,48,3,TINTA,1.3);caja(28,-40,32,26,2,ab?"#2b3048":"#ff9a1f");for(let i=0;i<3;i++)circ(32+i*10,-44,1.8,TINTA);if(!ab)for(let i=0;i<3;i++)caja(31+i*10,-30,8,10,1,"#ffffff88");humito(44,-50,T);},
        frente(){if(ab){caja(26,-14,36,4,1,"#9aa3bb");for(let i=0;i<3;i++)caja(30+i*10,-22,8,8,1,"#fffaf0");}}};
    },
    remo(T){
      const k=(Math.sin(T*4)+1)/2,dx=-8+k*10,hx=30-k*20+dx;em(900,-16,-58,"💧",AZUL,14);
      return {cara:"apretado",sentado:true,dx,incl:-.15+k*.3,mira:2,brD:[30-k*20,-26],brI:[24-k*20,-26],sube:2,
        atras(){caja(-30,-4,90,4,2,"#79829b");caja(50,-16,8,14,2,"#3c4259");},
        frente(){raya(hx,-28,52,-12,"#9aa3bb",1.4);}};
    },
  });
  pon("prisa",{
    arena(T,s){                          // voltea el reloj de arena una y otra vez
      const f=ciclo(s,3),gira=f>.85?(f-.85)/.15*Math.PI:0,k=Math.min(1,f/.85);
      return {cara:f>.85?"apretado":"normal",mira:2,incl:.1,brD:[24,-36],brI:[18,-26],pies:[0,Math.sin(T*9)>0?-3:2],
        frente(){g.save();g.translate(26,-30);g.rotate(gira);caja(-7,-14,14,2.4,1,MADERA);caja(-7,11.6,14,2.4,1,MADERA);g.beginPath();g.moveTo(-6,-12);g.lineTo(6,-12);g.lineTo(1,0);g.lineTo(6,12);g.lineTo(-6,12);g.lineTo(-1,0);g.closePath();g.fillStyle="#dff4ff88";g.fill();g.strokeStyle="#9fd8ff";g.lineWidth=1;g.stroke();
          if(!gira){caja(-4,-10+8*k,8,10-8*k,1,AMAR);caja(-5,12-8*k,10,8*k,1,AMAR);raya(0,-1,0,11-8*k,AMAR,.8);}g.restore();}};
    },
    pasear(T){                           // camina de un lado a otro: ¿ya?
      const x=Math.sin(T*1.1)*22,v=Math.cos(T*1.1),a=Math.sin(T*8)*5;
      em(2500,x,-62,["¿ya?","…","¿cuánto falta?"][Math.floor(T/2.5)%3],"#fff",-8);
      return {cara:"enfocado",dx:x,mira:v>0?3:-3,pies:[a,-a],sube:Math.abs(Math.sin(T*8))*1.5,brD:[-6,-20],brI:[-10,-20],incl:.05};
    },
    globo(T,s){                          // infla un globo… ¡pum!
      const f=ciclo(s,4),r=f<.85?3+f/.85*20:0,pum=f>=.85;
      if(pum&&f<.9)em(500,24,-56,"¡PUM!",ROJO,-20);
      return {cara:pum?"wow":"apretado",pelo:pum,boca:pum?.8:.5,rubor:!pum,mira:2,incl:pum?-.15:0,brD:[16,-38],brI:[12,-34],
        frente(){if(!pum){elip(18+r*.9,-38-r*.2,r,r*1.1,ROJO);circ(18+r*.5,-38-r*.6,r*.18,"#ffffff88");}else{const d=8+(f-.85)*200;for(let i=0;i<6;i++){const a=i*1.05;caja(30+Math.cos(a)*d,-44+Math.sin(a)*d,3,2,0,ROJO);}}}};
    },
  });

  // ---- subir el video
  pon("subir",{
    paloma(T,s){                         // paloma mensajera con el video
      const f=ciclo(s,3.5),v=f>.4?(f-.4)/.6:0,px=26+v*56,py=-40-v*v*56,al=Math.sin(T*(v?20:3))*5;
      if(v>0&&v<.15)em(600,20,-60,"¡suerte!",AMAR,-10);
      return {cara:v?"feliz":"enfocado",mira:2,brD:v?[20,-52+Math.sin(T*10)*4]:[24,-36],brI:v?[-18,-48]:[-14,-18],sube:v?Math.abs(Math.sin(T*8))*3:0,
        frente(){g.save();g.translate(px,py);elip(0,0,8,5,"#c7cede");circ(7,-4,3.4,"#c7cede");circ(8,-5,.9,TINTA);g.beginPath();g.moveTo(10,-4);g.lineTo(13,-3);g.lineTo(10,-2);g.fillStyle=AMAR;g.fill();g.beginPath();g.moveTo(-2,-2);g.lineTo(-8,-6-al);g.lineTo(4,-3);g.closePath();g.fillStyle="#9aa3bb";g.fill();caja(-5,3,8,5,1,ROJO);g.restore();}};
    },
    resortera(T,s){                      // lo lanza con resortera
      const f=ciclo(s,3),tens=f<.5?f/.5:0,vu=f>=.5?(f-.5)/.5:0,bx=43-tens*14+vu*40,by=-36-vu*90+vu*vu*10;
      if(vu>0&&vu<.1)em(500,40,-40,"¡fiuuu!",AMAR,-30);
      return {cara:f<.5?"apretado":"wow",mira:3,incl:-.1+tens*.05,brD:f<.5?[bx-2,-36]:[28,-40],brI:[42,-28],
        atras(){raya(42,0,42,-24,MADERA,3);raya(42,-24,36,-40,MADERA,2.4);raya(42,-24,50,-40,MADERA,2.4);},
        frente(){const lx=f<.5?bx:43,ly=f<.5?by:-36;raya(36,-40,lx,ly,"#8d6a4a",1.4);raya(50,-40,lx,ly,"#8d6a4a",1.4);if(by>-120){caja(bx-6,by-5,12,10,2,ROJO);g.beginPath();g.moveTo(bx-2,by-3);g.lineTo(bx+3,by);g.lineTo(bx-2,by+3);g.fillStyle="#fff";g.fill();}}};
    },
    globos(T,s){                         // le amarra globos y se va flotando
      const f=ciclo(s,4.5),v=f>.45?(f-.45)/.55:0,by=-14-v*v*110;
      if(v>0&&v<.1)em(800,40,-60,"♥",ROSA);
      return {cara:v?"feliz":"enfocado",mira:2,brD:v?[18,-46+Math.sin(T*9)*3]:[30,-16],brI:v?[-18,-46]:[-14,-18],
        frente(){caja(30,by,20,12,2,ROJO);g.beginPath();g.moveTo(37,by+3);g.lineTo(43,by+6);g.lineTo(37,by+9);g.fillStyle="#fff";g.fill();for(const [dx,c] of [[-8,AMAR],[0,AZUL],[8,ROSA]]){raya(40,by,40+dx,by-24,"#c9cedb",.8);elip(40+dx,by-30,6,7.5,c);}}};
    },
  });

  // ---- explicar (cuando Claude te contesta)
  pon("explicar",{
    pizarra(T){
      const p=Math.floor(T*1.2)%3,pt=[[38,-56],[56,-48],[46,-30]][p];
      return {cara:"feliz",boca:Math.abs(Math.sin(T*10))*.6,mira:3,incl:-.05,brD:[22,-36],brI:[-16,-20],
        atras(){caja(28,-66,44,44,2,"#fff");marco(28,-66,44,44,2,"#9aa3bb",2);raya(34,-22,32,0,"#9aa3bb",2);raya(66,-22,68,0,"#9aa3bb",2);aro(38,-56,5,AZUL,1.4);aro(56,-48,5,ROJO,1.4);marco(41,-34,10,8,1,VERDE,1.4);raya(42,-53,52,-49,TINTA,1);raya(54,-44,48,-34,TINTA,1);},
        frente(){raya(22,-36,pt[0]-2,pt[1]+2,MADERA,1.6);circ(pt[0]-2,pt[1]+2,1.4,ROJO);}};
    },
    titere(T){                           // le explica un títere de calcetín
      const bo=Math.abs(Math.sin(T*9));em(1000,42,-58,"bla","#fff",-16);
      return {cara:"enfocado",mira:3,incl:.08,brD:[26,-40],brI:[-16,-20],
        frente(){g.save();g.translate(26,-40);caja(-4,0,8,10,3,LILA);elip(5,-4,11,6,LILA);g.beginPath();g.moveTo(-2,-2);g.lineTo(16,-2-bo*4);g.lineTo(16,-2+bo*2);g.closePath();g.fillStyle="#7a3d9c";g.fill();circ(4,-9,2.6,"#fff");circ(5,-9,1.3,TINTA);g.restore();}};
    },
    megafono(T){
      const v=Math.abs(Math.sin(T*8));em(1200,50,-50,"¡!",AMAR,-14);
      return {cara:"apretado",boca:.7,mira:2,incl:-.06,brD:[24,-44],brI:[14,-40],sube:v*1.5,
        frente(){g.beginPath();g.moveTo(16,-46);g.lineTo(34,-54);g.lineTo(34,-34);g.lineTo(16,-42);g.closePath();g.fillStyle=ROJO;g.fill();caja(12,-47,6,6,1,"#fff");for(let i=1;i<=3;i++)aro(36,-44,4+i*5+v*2,AMAR+"aa",1.6,-.6,.6);}};
    },
    grafica(T,s){                        // la gráfica que solo sube
      const k=Math.min(1,ciclo(s,4)/.7);if(k>=1)em(800,52,-70,"📈","#fff",-10);
      return {cara:k>=1?"feliz":"enfocado",boca:.3+.3*Math.sin(T*9),mira:3,brD:[26,-40+(1-k)*10],brI:[-16,-20],
        atras(){caja(28,-64,40,40,1,"#fffaf0");marco(28,-64,40,40,1,"#9aa3bb",1.6);raya(36,-24,38,0,"#6f7892",2);raya(60,-24,58,0,"#6f7892",2);for(let i=0;i<4;i++){const h=6+i*7,q=Math.min(1,Math.max(0,(k-i/4)*4));if(q)caja(33+i*8,-28-h*q,6,h*q,1,COLORES[i]);}
          const ex=33+k*30,ey=-32-k*24;raya(33,-32,ex,ey,ROJO,2.2);g.beginPath();g.moveTo(ex,ey-3);g.lineTo(ex+5,ey-4);g.lineTo(ex+2,ey+1);g.closePath();g.fillStyle=ROJO;g.fill();}};
    },
  });

  // ---- te escucha (mensaje del usuario)
  pon("escuchar",{
    corneta(T){                          // trompetilla de oreja de abuelo
      em(700,52,-46,"♥",ROSA,-10);
      return {cara:"wow",mira:3,incl:.18,dx:2,brD:[22,-44],brI:[-14,-18],
        frente(){g.beginPath();g.moveTo(16,-48);g.lineTo(44,-60);g.lineTo(44,-34);g.closePath();g.fillStyle="#e7c56b";g.fill();elip(44,-47,3,13,"#c9a24a");for(let i=1;i<=2;i++)aro(58,-47,4+i*5-((T*10)%5),"#ffffff99",1.2,Math.PI*.6,Math.PI*1.4);}};
    },
    notas(T){                            // apunta todo y asiente rapidísimo
      const n=Math.sin(T*8),p=(T*24)%8;em(1600,30,-56,"¡sí!","#fff",-12);
      return {cara:"enfocado",incl:.1+n*.08,mira:2,brD:[22+p,-26],brI:[16,-28],
        frente(){caja(14,-36,16,18,1.5,"#fffaf0");marco(14,-36,16,18,1.5,"#c9b28f",1);for(let i=0;i<4;i++)raya(16,-32+i*4,16+((T*3+i)%3)*4,-32+i*4,TINTA+"99",1);raya(22+p,-26,26+p,-34,ROSA,1.6);}};
    },
    saludo(T,s){                         // saludo militar
      const b=Math.min(1,s*3);if(Math.sin(T*1.5)>.6)em(1800,24,-60,"¡sí, jefe!",AMAR,-10);
      return {cara:"enfocado",rubor:true,mira:2,sube:b<1?b*4:0,brD:[9,-54],brI:[-13,-12],pies:[0,0]};
    },
  });

  // ---- paso listo
  pon("palomita",{
    sello(T,s){                          // ¡sellado!
      const f=ciclo(s,1.6),k=f<.35?f/.35:f<.5?1:1-(f-.5)/.5,y=-50+k*28,gol=f>.33&&f<.45;
      if(gol)em(500,30,-26,"¡pum!",AMAR,-30);
      return {cara:gol?"apretado":"feliz",mira:2,sube:gol?2:0,brD:[30,y-4],brI:[-14,-18],
        atras(){caja(14,-10,40,10,1,MADERA);caja(17,-13,32,4,1,"#fffaf0");if(f>.38||s>1.6){raya(25,-11.5,28,-10,VERDE,1.6);raya(28,-10,36,-13,VERDE,1.6);}},
        frente(){caja(26,y-14,8,8,2,MADERA);caja(22,y-6,16,6,1.5,ROJO);}};
    },
    floss(T){                            // bailecito de victoria
      const a=Math.sin(T*9),b=Math.sin(T*4.5);
      return {cara:"feliz",boca:.4,dx:b*2,incl:-b*.06,mira:2,brD:[a*16,-16],brI:[a*16-4,-14],pies:[-b*2,-b*2],sube:Math.abs(a)*1.5};
    },
    estrella(T,s){                       // se pega su propia estrellita dorada
      const f=ciclo(s,3),pega=f>.5;if(f>.5&&f<.55)em(600,0,-30,"✦",AMAR,-30);
      return {cara:pega?"feliz":"enfocado",rubor:pega,mira:pega?0:2,incl:pega?-.08:.15,brD:pega?[18,-44]:[10,-26],brI:[-14,-18],
        frente(){const sx=pega?2:10+(1-f/.5)*10,sy=pega?-20:-28;g.save();g.translate(sx,sy);g.beginPath();for(let i=0;i<10;i++){const r=i%2?2.2:5,a=i*Math.PI/5-Math.PI/2;g.lineTo(Math.cos(a)*r,Math.sin(a)*r);}g.closePath();g.fillStyle=AMAR;g.fill();g.restore();}};
    },
    pulgar(T){                           // pulgar arriba con destello
      const b=Math.sin(T*3)>.7;if(b)em(700,12,-50,"✦","#fff",-6);
      return {cara:"feliz",mira:3,incl:-.08,brD:[22,-36],brI:[-14,-18],
        frente(){caja(19,-44,7,9,2.5,CABEZA);marco(19,-44,7,9,2.5,TINTA,1);caja(20,-52,4,9,2,CABEZA);marco(20,-52,4,9,2,TINTA,1);}};
    },
  });

  // ---- tramo listo
  pon("fiesta",{
    pinata(T,s){                         // ¡dale, dale, dale!
      const f=ciclo(s,1.2),gol=f<.2,sw=Math.sin(T*3)*.3+(gol?.3:0),rota=s>6,px=44+Math.sin(sw)*30;
      if(gol)em(400,40,-56,"¡dale!",AMAR,-20);if(rota)em(160,40+Math.random()*20-10,-60,"●",COLORES[Math.floor(Math.random()*6)],40);
      const hx=gol?30:14,hy=gol?-30:-50;
      return {cara:gol?"apretado":"feliz",gorro:"fiesta",boca:.5,mira:3,brD:[hx,hy],brI:gol?[24,-30]:[8,-52],
        atras(){raya(44,-110,px,-72,"#c9cedb",1);g.save();g.translate(px,-62);g.rotate(sw);if(!rota){for(let i=0;i<5;i++){const a=i*1.256;g.beginPath();g.moveTo(0,0);g.lineTo(Math.cos(a)*16,Math.sin(a)*16);g.lineTo(Math.cos(a+.6)*6,Math.sin(a+.6)*6);g.closePath();g.fillStyle=COLORES[i];g.fill();}circ(0,0,8,AMAR);}else{circ(-6,8,4,AMAR);circ(6,10,3,ROSA);}g.restore();},
        frente(){raya(hx,hy,hx+(gol?22:-4),hy-(gol?28:22),MADERA,2.6);}};
    },
    matasuegras(T){                      // espantasuegras
      const k=(Math.sin(T*4)+1)/2;em(600,40,-44,"♪",AMAR,-20);
      return {cara:"feliz",gorro:"fiesta",rubor:true,mira:2,sube:Math.abs(Math.sin(T*8))*4,brD:[18,-36],brI:[-18,-48+Math.sin(T*8)*4],
        frente(){if(k>.3){raya(17,-35,17+k*24,-35,ROSA,4);for(let i=0;i<5;i++)raya(19+i*k*4.5,-37,19+i*k*4.5,-33,AMAR,1);}else aro(20,-35,3,ROSA,3);}};
    },
    fuegos(T,s){                         // cohetes
      const f=ciclo(s,1.5),x=30+((Math.floor(s/1.5)*23)%40),y=-40-f*60;
      return {cara:f>.6?"wow":"feliz",boca:.5,mira:3,incl:-.15,brD:[20,-48],brI:[-20,-48],sube:f>.6?Math.abs(Math.sin(T*10))*5:0,
        frente(){if(f<.6){circ(x,y,2,AMAR);raya(x,y,x,y+10,"#ffd16688",1.4);}else{const r=(f-.6)*60;for(let i=0;i<10;i++){const a=i*.628;circ(x+Math.cos(a)*r,-76+Math.sin(a)*r,1.8,COLORES[(i+Math.floor(s))%6]);}}}};
    },
  });

  // ---- algo privado
  pon("tapa",{
    cajacarton(T){                       // escondido en una caja de cartón con dos agujeros
      const x=Math.sin(T*.8)*10,m=Math.sin(T*2.2)>.6;if(m)em(1500,x,-50,"!",ROJO,-14);
      return {cara:"normal",dx:x,sube:-20,mira:3,brD:[10,-14],brI:[-10,-14],
        frente(){caja(x-24,-40,48,40,2,"#c9935f");marco(x-24,-40,48,40,2,"#8d6a4a",1.2);raya(x-24,-40,x-30,-48,"#c9935f",3);raya(x+24,-40,x+30,-48,"#c9935f",3);caja(x-2,-32,14,5,2,"#2b2018");circ(x+1+(m?3:0),-29.5,1.4,"#7df3e1");circ(x+8+(m?3:0),-29.5,1.4,"#7df3e1");}};
    },
    silbar(T){                           // silba como si nada, con la carpeta atrás
      em(700,-14,-50,"♪",LILA,-20);
      return {cara:"normal",mira:-4,boca:.2,rubor:true,incl:-.1+Math.sin(T*1.2)*.04,brD:[-8,-22],brI:[-12,-22],pies:[0,Math.sin(T*3)>0?-2:0],
        atras(){caja(-32,-32,16,12,1,AMAR);caja(-32,-34,7,3,1,AMAR);}};
    },
    biombo(T){                           // tras el biombo; solo asoma la antena… y a veces los ojos
      const asoma=Math.sin(T*1.4)>.7;
      return {cara:asoma?"wow":"normal",sube:asoma?14:0,mira:3,rubor:true,brD:[16,-30],brI:[-14,-18],
        frente(){for(let i=0;i<3;i++){const x=-24+i*20;g.beginPath();g.moveTo(x,-56+(i%2)*2);g.lineTo(x+20,-56+((i+1)%2)*2);g.lineTo(x+20,0);g.lineTo(x,0);g.closePath();g.fillStyle=i%2?"#f3d9b1":"#e8c896";g.fill();g.strokeStyle=MADERA;g.lineWidth=1.4;g.stroke();for(let j=0;j<3;j++)circ(x+10,-44+j*14,2,ROSA+"88");}}};
    },
  });

  // ---- llamó a un ayudante
  pon("amigo",{
    telefono(T){                         // teléfono de disco
      const r=Math.sin(T*3)*.6;em(1500,30,-60,"¿bueno?","#fff",-10);
      return {cara:"feliz",boca:Math.abs(Math.sin(T*9))*.5,mira:2,incl:.1,brD:[14,-46],brI:[30,-22],
        frente(){caja(24,-12,18,12,1,MADERA);caja(22,-24,22,12,3,ROJO);circ(33,-18,4.5,"#fff");g.save();g.translate(33,-18);g.rotate(r);for(let i=0;i<6;i++){const a=i*1.05;circ(Math.cos(a)*3,Math.sin(a)*3,.8,TINTA);}g.restore();caja(10,-52,6,14,3,ROJO);g.beginPath();g.moveTo(13,-38);g.bezierCurveTo(10,-20,30,-30,24,-22);g.strokeStyle=TINTA;g.lineWidth=1;g.stroke();}};
    },
    silbato(T){
      const s2=Math.sin(T*6)>0;em(500,30,-48,"¡fiu!",AMAR,-20);
      return {cara:"apretado",rubor:true,mira:2,brD:[14,-36],brI:[-20,-48+(s2?4:0)],sube:s2?1:0,
        frente(){caja(14,-38,10,5,2,"#c7cede");circ(22,-35,3,"#c7cede");for(let i=1;i<=3;i++)aro(26,-36,i*5,"#ffffff88",1.2,-.5,.5);}};
    },
    senal(T){                            // la señal en el cielo, con cara de robot
      const a=-1.1+Math.sin(T*.8)*.1,cx=28+Math.cos(a)*84,cy=-22+Math.sin(a)*84;
      return {cara:"enfocado",mira:3,incl:-.08,brD:[24,-26],brI:[18,-22],
        frente(){caja(18,-24,14,12,2,"#6f7892");g.save();g.translate(28,-22);g.rotate(a);g.beginPath();g.moveTo(0,-4);g.lineTo(90,-20);g.lineTo(90,20);g.lineTo(0,4);g.closePath();g.fillStyle="#ffe98a33";g.fill();g.restore();circ(cx,cy,12,"#ffe98a66");caja(cx-5,cy-5,10,8,3,"#2b3048");circ(cx-2,cy-1,1.2,"#ffe98a");circ(cx+2,cy-1,1.2,"#ffe98a");raya(cx,cy-5,cx,cy-8,"#2b3048",1);}};
    },
  });

  // ---- pensar
  pon("pensar",{
    foco(T,s){                           // ¡se le prende el foco!
      const f=ciclo(s,3),on=f>.6;if(on&&f<.65)em(600,0,-90,"✦",AMAR,-10);
      return {cara:on?"wow":"normal",mira:on?0:1.5,incl:on?0:-.08,brD:on?[16,-46]:[9,-32],brI:[-14,-20],luz:on?AMAR:undefined,
        frente(){const y=-86;if(on)circ(0,y,10,"#ffe98a55");circ(0,y,6,on?AMAR:"#c9cedb");caja(-3,y+5,6,4,1,"#9aa3bb");if(!on)for(let i=0;i<3;i++)circ(-10+i*10,-75-Math.sin(T*3+i)*2,1.4,"#fff");}};
    },
    humo(T){                             // piensa tanto que le sale humo
      return {cara:"apretado",mira:Math.sin(T*9),incl:Math.sin(T*25)*.03,brD:[16,-54],brI:[-16,-54],luz:ROJO,boca:.2,
        frente(){humito(-6,-64,T,"#c9cedb",3);humito(8,-64,T+.4,"#c9cedb",3);}};
    },
    rubik(T,s){
      const f=ciclo(s,6),ok=f>.85,r=Math.floor(T*2);if(ok)em(700,24,-56,"✦",AMAR);
      const C=[ROJO,VERDE,AZUL,AMAR,"#fff","#ff9a1f"];
      return {cara:ok?"feliz":"enfocado",mira:2,incl:.1,brD:[26,-32+(r%2)*2],brI:[16,-32],
        frente(){for(let i=0;i<3;i++)for(let j=0;j<3;j++)caja(14+i*4.4,-42+j*4.4,4,4,.8,ok?ROJO:C[(i*3+j*5+r)%6]);}};
    },
    pino(T){                             // piensa de cabeza
      const w=Math.sin(T*2)*.08;if(Math.sin(T*.9)>.7)em(1600,20,-40,"🤔","#fff",-10);
      return {cara:"enfocado",rota:Math.PI+w,sube:22,mira:1,brD:[14,-58],brI:[-14,-58],pies:[Math.sin(T*3)*3,-Math.sin(T*3)*3]};
    },
  });

  // ---- un fallo
  pon("fallo",{
    resbalon(T,s){                       // se resbala con una cáscara de plátano
      const f=ciclo(s,3.5),cae=f<.25?f/.25:1,aire=f<.25;
      return {cara:aire?"wow":"triste",sentado:!aire,rota:aire?-Math.sin(cae*Math.PI)*1.2:0,sube:aire?Math.sin(cae*Math.PI)*16:-4,pelo:f<.3,mira:0,brD:aire?[20,-46]:[14,-14],brI:aire?[-20,-46]:[-14,-14],
        frente(){g.save();g.translate(aire?20+cae*10:34,-2);g.rotate(aire?cae*3:0);g.beginPath();g.moveTo(-6,0);g.quadraticCurveTo(0,-8,6,0);g.quadraticCurveTo(0,-4,-6,0);g.fillStyle=AMAR;g.fill();g.restore();if(!aire)mareo(0,-70,T);}};
    },
    nubecita(T){                         // su propia nube de lluvia
      const x=Math.sin(T*.7)*3;if(Math.sin(T*1.3)>.95)em(400,x,-92,"⚡",AMAR,0);
      return {cara:"triste",incl:.12,mira:-1,brD:[13,-13],brI:[-13,-13],luz:"#8d93a8",
        frente(){for(const [dx,dy,r] of [[-10,0,8],[0,-4,10],[10,0,8]])circ(x+dx,-86+dy,r,"#8d93a8");for(let i=0;i<6;i++){const y=-80+((T*60+i*13)%74);raya(x-12+i*5,y,x-13+i*5,y+4,AZUL,1.2);}}};
    },
    pataleta(T){                         // berrinche
      const a=Math.sin(T*16);em(300,0,-66,"#!@$%&".charAt(Math.floor(T*5)%6),ROJO,-34);
      return {cara:"apretado",pelo:true,boca:.8,mira:0,incl:a*.06,pies:[a*4,-a*4],sube:Math.abs(a)*3,brD:[18,-44-a*6],brI:[-18,-44+a*6],luz:ROJO};
    },
    chispas(T){                          // cortocircuito
      const t=Math.sin(T*30)>.6;if(t)em(200,(Math.random()-.5)*30,-50,"⚡",AMAR,-30);
      return {cara:"apretado",mira:Math.random()*2,incl:Math.sin(T*40)*.04,dx:Math.sin(T*35),brD:[13,-13],brI:[-13,-13],luz:t?"#fff":"#333",
        frente(){humito(-4,-62,T,"#555d78",3);g.globalAlpha=.25;circ(4,-46,10,"#10131b");g.globalAlpha=1;}};
    },
  });

  // ---- dormir (sesión terminada)
  pon("dormir",{
    moco(T){                             // burbuja de moco
      const r=2+((Math.sin(T*1.2)+1)/2)*7;
      return {cara:"dormido",gorro:"noche",incl:.15,sube:-3,brD:[13,-14],brI:[-13,-14],pies:[3,-3],rubor:true,luz:"#555d78",
        frente(){circ(16+r*.7,-38,r,"#9fd8ff55");aro(16+r*.7,-38,r,"#9fd8ff",1);circ(16+r,-38-r*.4,r*.2,"#fff");}};
    },
    sonambulo(T){
      const a=Math.sin(T*3)*4,x=Math.sin(T*.4)*14;em(1300,x+16,-64,"z","#b388ff",-16);
      return {cara:"dormido",gorro:"noche",dx:x,brD:[30,-28],brI:[26,-30],pies:[a,-a],sube:Math.abs(Math.sin(T*3)),incl:.05};
    },
  });
})();
