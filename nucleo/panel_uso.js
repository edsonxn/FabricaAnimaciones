/* Registro de uso del panel (bitácora de interacción). Lo sirve panel.py en /uso.js y lo guarda en /api/uso
   -> nucleo/datos/uso_panel/AAAA-MM-DD.jsonl (privado, fuera de git). Lo lee `python nucleo/uso_panel.py resumen`
   y el skill «analizar-uso-panel». Solo registra QUÉ controles se tocan, dónde, cuánto se mira cada pestaña y qué
   filtros se usan; NUNCA el texto que se teclea (salvo el buscador «q» y los filtros, que son la señal). Sin red externa. */
(function () {
  "use strict";
  const UI = (document.querySelector('meta[name="ui-version"]') || {}).content || "v1";
  const SES = Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  const cola = [];
  let pest = "proy", ultimaAccion = Date.now(), inventariados = new Set();

  const nd = (n) => Math.round(n * 100) / 100;
  const recorta = (s, n) => (s || "").replace(/\s+/g, " ").trim().slice(0, n);
  function reg(e, datos) { cola.push(Object.assign({ t: Date.now(), s: SES, ui: UI, e: e, p: pest }, datos || {})); }

  // ---------- identificar un control de forma estable (sin el nombre del video, que cambia)
  const INTERACTIVO = "button,a,select,input,textarea,summary,[data-f],[data-pest],[data-abrir],[data-prev],[data-ver],[data-ev],[data-master],[data-muestra],[data-play],[data-copiar],[data-voz],[data-ocultar],[data-mu-img],[role=button],[onclick]";
  function clave(el) {
    if (el.id) return "#" + el.id;
    for (const a of el.attributes) if (a.name.startsWith("data-")) return "[" + a.name + "]";
    const c = (typeof el.className === "string" ? el.className : "").split(/\s+/).filter(Boolean)[0];
    return el.tagName.toLowerCase() + (c ? "." + c : "");
  }
  function valorData(el) {
    // valores que describen la ELECCIÓN (filtro, pestaña, acción), no un nombre de video
    for (const a of ["data-f", "data-pest", "data-voz", "data-valor"]) if (el.hasAttribute && el.hasAttribute(a)) return el.getAttribute(a);
    return undefined;
  }
  function tarjeta(el) {
    const c = el.closest && el.closest(".card[data-n]");
    return c ? { vid: c.dataset.n, canal: c.dataset.canal } : {};
  }
  function seccion(el) {
    const v = el.closest && el.closest("[id^=vista-],.vp-caja,.mu-caja,#ev,header,nav,.barra,.filtros");
    return v ? (v.id || (typeof v.className === "string" ? v.className.split(/\s+/)[0] : v.tagName.toLowerCase())) : "";
  }

  // ---------- clics (incluye «clic muerto»: nada interactivo bajo el cursor)
  function alClic(e, ventana) {
    ultimaAccion = Date.now();
    const t = e.target.nodeType === 1 ? e.target : e.target.parentElement;
    if (!t) return;
    const c = t.closest(INTERACTIVO);
    const w = ventana.innerWidth || 1, h = ventana.innerHeight || 1;
    const base = { x: nd(e.clientX / w), y: nd(e.clientY / h) };
    if (!c) {
      const tarj = tarjeta(t);
      reg("clk", Object.assign(base, tarj, { dead: 1, k: clave(t), txt: recorta(t.textContent, 24), sec: seccion(t) }));
      return;
    }
    const v = valorData(c);
    reg("clk", Object.assign(base, tarjeta(c), { k: clave(c), txt: recorta(/^(select|textarea)$/i.test(c.tagName) ? (c.title || c.id) : (c.textContent || c.title || c.value), 30), sec: seccion(c) }, v !== undefined ? { v: v } : {}));
  }

  // ---------- cambios de filtros / selects / buscador
  function alCambio(e) {
    ultimaAccion = Date.now();
    const t = e.target;
    if (!t || !t.tagName) return;
    const tag = t.tagName.toLowerCase();
    if (tag === "select") reg("chg", { k: clave(t), v: recorta(t.value, 40) });
    else if (t.type === "checkbox" || t.type === "radio") reg("chg", { k: clave(t), v: t.checked ? 1 : 0 });
    else if (t.type === "range") reg("chg", { k: clave(t) });
    else if (t.type === "search" || t.id === "q") reg("chg", { k: clave(t), v: recorta(t.value, 40) });
  }
  let tBusca = 0;
  function alTecleo(e) {
    ultimaAccion = Date.now();
    const t = e.target;
    if (t && (t.type === "search" || t.id === "q")) {          // buscador: registra lo escrito al terminar de teclear
      clearTimeout(tBusca);
      tBusca = setTimeout(() => reg("chg", { k: clave(t), v: recorta(t.value, 40) }), 1200);
    }
  }
  function alTecla(e) {
    ultimaAccion = Date.now();
    const t = e.target, escribiendo = t && /^(input|textarea|select)$/i.test(t.tagName);
    const atajo = e.ctrlKey || e.metaKey || e.altKey;
    if (escribiendo && !["Escape", "Enter"].includes(e.key)) return;
    if (!atajo && !["Escape", "Enter", "ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", " ", "/", "PageDown", "PageUp", "Home", "End"].includes(e.key)) return;
    reg("key", { key: (atajo ? "ctrl+" : "") + e.key });          // nunca letras sueltas
  }

  // ---------- scroll (por contenedor, al quedar quieto) + qué tarjetas se ven
  const scrolls = new Map();
  function alScroll(e, ventana) {
    ultimaAccion = Date.now();
    const d = ventana.document;
    const t = e.target === d ? d.scrollingElement : e.target;
    if (!t || !t.tagName) return;
    const id = t === d.scrollingElement ? "pagina" : (t.id ? "#" + t.id : clave(t));
    let r = scrolls.get(id);
    if (!r) { r = { ini: t.scrollTop, y0: t.scrollTop, max: t.scrollTop, tm: 0 }; scrolls.set(id, r); }
    r.max = Math.max(r.max, t.scrollTop);
    clearTimeout(r.tm);
    r.tm = setTimeout(() => {
      const vh = t === d.scrollingElement ? ventana.innerHeight : t.clientHeight;
      const alto = t.scrollHeight || 1;
      const vis = [];
      d.querySelectorAll(".card[data-n]").forEach((c) => {
        const b = c.getBoundingClientRect();
        if (b.bottom > 60 && b.top < ventana.innerHeight - 60 && vis.length < 10) vis.push(c.dataset.n);
      });
      reg("scr", { k: id, y: Math.round(t.scrollTop), de: Math.round(r.y0), alto: alto, vh: Math.round(vh), prof: nd((t.scrollTop + vh) / alto), vis: vis });
      scrolls.delete(id);
    }, 600);
  }

  // ---------- pestañas del panel (proy / est / can) y tiempo activo
  function cambiaPest(nueva) {
    if (nueva === pest) return;
    reg("pest", { de: pest, a: nueva });
    pest = nueva;
    setTimeout(inventario, 1500);
  }
  function vigilaPest() {
    document.addEventListener("click", (e) => {
      const b = e.target.closest && e.target.closest("[data-pest]");
      if (b) cambiaPest(b.dataset.pest);
    }, true);
    try { const g = localStorage.getItem("pest"); if (["est", "can"].includes(g)) pest = g; } catch (_) {}
  }
  setInterval(() => {                                           // 15 s de ATENCIÓN real: ventana visible y acción en los últimos 40 s
    if (document.visibilityState === "visible" && Date.now() - ultimaAccion < 40000) reg("act", { seg: 15 });
  }, 15000);
  document.addEventListener("mousemove", () => { ultimaAccion = Date.now(); }, { passive: true });

  // ---------- inventario de controles (para saber cuáles NUNCA se tocan)
  function inventario() {
    const lista = {};
    const raiz = pest === "can" ? ((document.getElementById("can-frame") || {}).contentDocument || document) : document;
    raiz.querySelectorAll(INTERACTIVO).forEach((el) => {
      if (el.closest(".card[data-n] .det, .vp-caja .cuadros")) { /* detalle interno: se cuenta por clave igual */ }
      const b = el.getBoundingClientRect ? el.getBoundingClientRect() : { width: 1, height: 1 };
      const k = clave(el), v = valorData(el);
      const kk = v !== undefined ? k + "=" + v : k;
      if (!lista[kk]) lista[kk] = { k: kk, txt: recorta(/^(select|textarea)$/i.test(el.tagName) ? (el.title || el.id) : (el.textContent || el.title || el.placeholder), 30), vis: b.width > 0 && b.height > 0 ? 1 : 0, n: 0 };
      lista[kk].n++;
    });
    const filas = Object.values(lista).slice(0, 150);
    const firma = pest + "|" + filas.map((f) => f.k + f.n).join(",");
    if (inventariados.has(firma)) return;
    inventariados.add(firma);
    reg("inv", { ctl: filas });
  }

  // ---------- envío
  function enviar(final) {
    if (!cola.length) return;
    const lote = cola.splice(0, cola.length);
    const cuerpo = JSON.stringify({ eventos: lote });
    try {
      if (final && navigator.sendBeacon) { navigator.sendBeacon("/api/uso", new Blob([cuerpo], { type: "application/json" })); return; }
      fetch("/api/uso", { method: "POST", headers: { "Content-Type": "application/json" }, body: cuerpo, keepalive: true }).catch(() => { cola.unshift.apply(cola, lote.slice(-300)); });
    } catch (_) { /* el panel sigue funcionando aunque no se pueda registrar */ }
  }
  setInterval(() => enviar(false), 10000);
  document.addEventListener("visibilitychange", () => { reg("vis", { v: document.visibilityState }); if (document.visibilityState === "hidden") enviar(true); });
  window.addEventListener("pagehide", () => { reg("fin"); enviar(true); });

  // ---------- instalar en la ventana principal y en el iframe «Canales» (mismo origen)
  function instalar(ventana) {
    const d = ventana.document;
    d.addEventListener("click", (e) => alClic(e, ventana), true);
    d.addEventListener("change", alCambio, true);
    d.addEventListener("input", alTecleo, true);
    d.addEventListener("keydown", alTecla, true);
    ventana.addEventListener("scroll", (e) => alScroll(e, ventana), true);
  }
  function vigilaIframe() {
    const f = document.getElementById("can-frame");
    if (!f) return;
    const poner = () => { try { if (f.contentDocument && !f.contentDocument.__uso) { f.contentDocument.__uso = 1; instalar(f.contentWindow); } } catch (_) {} setTimeout(inventario, 1500); };
    f.addEventListener("load", poner);
    poner();
  }

  instalar(window);          // primero el registro de clics (atribuye el clic a la pestaña de origen) y después el cambio de pestaña
  vigilaPest();
  reg("ses", { w: window.innerWidth, h: window.innerHeight, dpr: window.devicePixelRatio || 1, hora: new Date().getHours(), dia: new Date().getDay(), filtros: (function () { try { return { f: localStorage.getItem("f"), fc: localStorage.getItem("fc"), fe: localStorage.getItem("fe") }; } catch (_) { return {}; } })() });
  setTimeout(vigilaIframe, 0);
  setTimeout(inventario, 3000);
  window.__usoPanel = { reg: reg, enviar: enviar, inventario: inventario };      // para que una versión nueva del panel pueda registrar eventos propios
})();
