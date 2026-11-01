// /v2/vivo en el teléfono (30-oct-2026): todo en una pantalla, sin desplazar la página. Arriba el taller; abajo tres pestañas
// (Ahora = el monitor, Historial, Plan); los controles van al pie y lo que no cabe, en «⋯». El CSS está en panel_vivo.html.
(()=>{
  const ANGOSTO=matchMedia("(max-width:900px),(max-height:500px)");
  const cab=$("cab"),pie=$("pie"),linea=$("linea");
  const SIEMPRE=["btPausa","btVivo"].map($);
  const MENU=[...cab.querySelectorAll(".cas"),$("btVel"),$("btEstreno"),$("btResumen")].filter(Boolean);
  const CTL=[...MENU.slice(0,2),...[$("btPausa"),$("btVel"),$("btEstreno"),$("btResumen"),$("btVivo")].filter(Boolean)];   // orden de la cabecera

  cab.querySelector('a.bt[href="/v2"]').href=REMOTO?"/v2/movil":"/v2";   // por el túnel se vuelve al panel del teléfono

  const tabs=document.createElement("nav");
  tabs.id="tabsM";tabs.setAttribute("aria-label","Secciones");
  tabs.innerHTML=[["ahora","🖥 Ahora"],["hist","📜 Historial"],["plan","☑ Plan"]].map(([k,t])=>`<button class="tabM" data-t="${k}">${t}</button>`).join("");
  $("cuerpo").before(tabs);
  const tab=k=>{document.body.dataset.tab=k;for(const b of tabs.children)b.classList.toggle("on",b.dataset.t===k);};
  tabs.onclick=e=>{const b=e.target.closest(".tabM");if(b)tab(b.dataset.t);};
  tab("ahora");
  $("feed").addEventListener("click",e=>{if(e.target.closest(".ev"))tab("ahora");});   // tocar algo del historial lo enseña en el monitor

  const menu=document.createElement("div"),mas=document.createElement("button");
  menu.id="menuM";mas.id="btMas";mas.className="bt";mas.textContent="⋯";mas.title="Más controles";
  const cierra=()=>menu.classList.remove("abierto");
  mas.onclick=e=>{e.stopPropagation();menu.classList.toggle("abierto");};
  addEventListener("pointerdown",e=>{if(!menu.contains(e.target)&&e.target!==mas)cierra();});
  document.body.append(menu);

  let chico=null;
  function acomoda(){
    if(ANGOSTO.matches===chico)return;
    chico=ANGOSTO.matches;
    if(chico){linea.before(...SIEMPRE);linea.after(mas);menu.append(...MENU);}
    else{cierra();cab.append(...CTL);}
  }
  ANGOSTO.addEventListener("change",acomoda);
  addEventListener("resize",acomoda);
  acomoda();

  if(REMOTO){                            // la cookie dura 30 días: al vencerse se vuelve a entrar en vez de quedarse en «Sin sesiones»
    const f=window.fetch;
    window.fetch=async(...a)=>{const r=await f(...a);if(r.status===401)location.href="/entrar?ir="+encodeURIComponent(location.pathname+location.search);return r;};
  }
})();
