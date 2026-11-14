"use strict";

const $ = (s) => document.querySelector(s);
// Fuera de la app (navegador normal) se usa un anfitrión de demostración para ver la interfaz
const host = window.chrome?.webview || demoHost();
const send = (m) => host.postMessage(m);

const S = { style: "info", presets: [], online: false, hist: new Map() };
const LABELS = { info: "AVISO", importante: "IMPORTANTE", urgente: "URGENTE", listo: "LISTO" };
const BADGE = { info: "i", importante: "!", urgente: "!", listo: "✓" };
const COLORS = { info: "var(--violet)", importante: "var(--amber)", urgente: "var(--red)", listo: "var(--green)" };
const svg = (p) => `<svg viewBox="0 0 24 24">${p}</svg>`;

// ------------------------------------------------------------ redactar y vista previa

const titulo = $("#titulo"), mensaje = $("#mensaje");
function refreshMini() {
  const mini = $("#mini");
  mini.dataset.s = S.style;
  $("#miniLabel").textContent = LABELS[S.style];
  $(".mini-badge").textContent = BADGE[S.style];
  $("#miniTitle").textContent = titulo.value.trim() || "La comida está lista";
  $("#miniMsg").textContent = mensaje.value.trim() || (titulo.value.trim() ? "" : "Ya pueden bajar a comer.");
  // Reinicia la animación de entrada para que se sienta vivo
  const card = $(".mini-card");
  card.style.animation = "none";
  void card.offsetWidth;
  card.style.animation = "";
}
let miniTimer;
[titulo, mensaje].forEach((el) => el.addEventListener("input", () => {
  clearTimeout(miniTimer);
  $("#miniTitle").textContent = titulo.value.trim() || "La comida está lista";
  $("#miniMsg").textContent = mensaje.value.trim() || (titulo.value.trim() ? "" : "Ya pueden bajar a comer.");
}));

$("#styles").addEventListener("click", (e) => {
  const b = e.target.closest("button");
  if (!b) return;
  document.querySelectorAll("#styles button").forEach((x) => x.classList.toggle("on", x === b));
  S.style = b.dataset.s;
  refreshMini();
});

["voz", "pausar", "encender"].forEach((k) => $("#" + k).addEventListener("change", (e) => send({ t: "settings", [k]: e.target.checked })));
$("#voice").addEventListener("change", (e) => {
  const o = e.target.selectedOptions[0];
  send({ t: "settings", voiceId: o.value, voiceName: o.textContent });
});

function payload() {
  return {
    titulo: titulo.value.trim(), mensaje: mensaje.value.trim(), estilo: S.style,
    voz: $("#voz").checked, pausar: $("#pausar").checked, encender: $("#encender").checked,
    voiceId: $("#voice").value,
  };
}

$("#send").addEventListener("click", () => {
  const p = payload();
  if (!p.titulo && !p.mensaje) { titulo.focus(); return toast("Escribe un título o un mensaje", true); }
  send({ t: "aviso", ...p });
  const b = $("#send");
  b.classList.add("busy");
  setTimeout(() => b.classList.remove("busy"), 1200);
});
[titulo, mensaje].forEach((el) => el.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.ctrlKey) $("#send").click(); }));

$("#preview").addEventListener("click", () => {
  const p = payload();
  if (!p.titulo && !p.mensaje) return toast("Escribe algo para escucharlo", true);
  $("#preview").classList.add("busy");
  send({ t: "preview", titulo: p.titulo, mensaje: p.mensaje, voiceId: p.voiceId });
});

// ------------------------------------------------------------ rápidos

function renderPresets() {
  const box = $("#presets");
  box.innerHTML = "";
  S.presets.forEach((p, i) => {
    const b = document.createElement("button");
    b.className = "preset";
    b.style.setProperty("--c", COLORS[p.estilo] || COLORS.info);
    b.innerHTML = `<b></b><span></span><span class="x" title="Quitar">${svg('<path d="M6 6l12 12M18 6 6 18"/>')}</span>`;
    b.querySelector("b").textContent = p.titulo || p.mensaje;
    b.querySelectorAll("span")[0].textContent = p.mensaje;
    b.addEventListener("click", (e) => {
      if (e.target.closest(".x")) {
        S.presets.splice(i, 1);
        send({ t: "presets", list: S.presets });
        renderPresets();
        return;
      }
      b.classList.remove("fire"); void b.offsetWidth; b.classList.add("fire");
      send({ t: "aviso", ...p, voz: $("#voz").checked, pausar: $("#pausar").checked, encender: $("#encender").checked, voiceId: $("#voice").value });
    });
    b.addEventListener("contextmenu", (e) => {
      e.preventDefault();
      titulo.value = p.titulo; mensaje.value = p.mensaje;
      document.querySelector(`#styles [data-s="${p.estilo}"]`)?.click();
      refreshMini();
    });
    box.append(b);
  });
}

$("#savePreset").addEventListener("click", () => {
  const p = payload();
  if (!p.titulo && !p.mensaje) return toast("Escribe el aviso primero", true);
  S.presets.unshift({ titulo: p.titulo, mensaje: p.mensaje, estilo: p.estilo });
  send({ t: "presets", list: S.presets });
  renderPresets();
  toast("Guardado en Rápidos");
});

// ------------------------------------------------------------ video e imagen

const mediaOpts = () => ({ pausar: $("#pausar").checked, segundos: Math.max(3, +$("#seg").value || 10), titulo: $("#imgTitle").value.trim() });
$("#pick").addEventListener("click", (e) => { e.preventDefault(); send({ t: "pick", ...mediaOpts() }); });
$("#sendUrl").addEventListener("click", () => {
  const u = $("#url").value.trim();
  if (!/^https?:\/\//.test(u)) return toast("Pega un enlace que empiece con http", true);
  send({ t: "url", url: u, pausar: $("#pausar").checked });
});

let depth = 0;
const hasFiles = (e) => [...(e.dataTransfer?.types || [])].includes("Files");
addEventListener("dragenter", (e) => { if (!hasFiles(e)) return; e.preventDefault(); depth++; document.body.classList.add("dragging"); });
addEventListener("dragover", (e) => { if (hasFiles(e)) { e.preventDefault(); e.dataTransfer.dropEffect = "copy"; } });
addEventListener("dragleave", () => { if (--depth <= 0) { depth = 0; document.body.classList.remove("dragging"); } });
addEventListener("drop", (e) => {
  e.preventDefault();
  depth = 0;
  document.body.classList.remove("dragging");
  const files = e.dataTransfer?.files;
  if (files?.length && host.postMessageWithAdditionalObjects) host.postMessageWithAdditionalObjects({ t: "drop", ...mediaOpts() }, files);
});

// ------------------------------------------------------------ controles de la TV

document.querySelectorAll("[data-ctl]").forEach((b) => b.addEventListener("click", () => send({ t: "control", path: b.dataset.ctl })));

function renderTv(m) {
  S.online = m.online;
  $("#tvcard").dataset.online = m.online ? "1" : "0";
  $("#tvName").textContent = m.online ? (m.name || "Google TV") : m.ip ? `${m.name || "Google TV"} · sin respuesta` : "Buscando tu Google TV…";
  const now = $("#tvNow");
  if (!m.online) now.textContent = m.ip ? "¿Está prendida? Abre Puente TV en la tele una vez" : "Instala Puente TV en la tele y ábrela una vez";
  else if (m.showing) now.innerHTML = "<b>Mostrando un aviso</b> ahora mismo";
  else if (m.app) { now.innerHTML = ""; const b = document.createElement("b"); b.textContent = m.app; now.append("Ahora: ", b, m.info ? ` · ${m.info}` : ""); }
  else now.textContent = "Lista para recibir avisos";
  const set = (id, ok, txtOk, txtNo) => { const el = $(id); el.className = "pill" + (ok ? " ok" : ""); el.textContent = ok ? txtOk : txtNo; };
  set("#pillOverlay", m.overlay, "✓ Mostrar encima", "✗ Falta mostrar encima");
  set("#pillControl", m.control, "✓ Pausa apps", "Pausa básica");
  $("#pillIp").textContent = m.ip ? `${m.ip}:8730` : "—";
  if (m.version) $("#tvVersion").textContent = `App de la TV: versión ${m.version}`;
  document.querySelectorAll("[data-ctl]").forEach((b) => (b.disabled = !m.online));
}

// ------------------------------------------------------------ historial

const KIND = {
  aviso: svg('<path d="M4 10v4h3l5 4V6L7 10z"/><path d="M16 9a4 4 0 0 1 0 6"/>'),
  video: svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m10 9 5 3-5 3z"/>'),
  imagen: svg('<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>'),
  archivo: svg('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/>'),
};
const STATUS = { generando: "Generando voz…", enviando: "Enviando…", mostrado: "En la TV ✓", error: "Falló" };

function renderHist(m) {
  const box = $("#hist");
  box.querySelector(".empty")?.remove();
  let el = S.hist.get(m.id);
  if (!el) {
    el = document.createElement("div");
    el.className = "h";
    el.innerHTML = `<span class="ic"></span><div><b></b><small></small><div class="prog" hidden><i></i></div></div><span class="st"></span>`;
    S.hist.set(m.id, el);
    box.prepend(el);
  }
  el.style.setProperty("--c", m.style ? COLORS[m.style] : m.kind === "video" ? "var(--pink)" : "var(--orange)");
  el.querySelector(".ic").innerHTML = KIND[m.kind] || KIND.archivo;
  el.querySelector("b").textContent = m.title;
  const sm = el.querySelector("small");
  sm.textContent = m.detail || m.time;
  sm.className = m.status === "error" ? "bad" : "";
  const st = el.querySelector(".st");
  st.textContent = m.progress != null && m.status === "enviando" ? `${Math.round(m.progress * 100)}%` : STATUS[m.status] || m.status;
  st.className = "st" + (m.status === "mostrado" ? " ok" : m.status === "error" ? " err" : "");
  const prog = el.querySelector(".prog");
  prog.hidden = !(m.status === "enviando" && m.progress != null);
  prog.querySelector("i").style.width = `${(m.progress || 0) * 100}%`;
  if (m.status === "mostrado") toast(m.kind === "aviso" ? "Aviso en la TV" : `${m.title} en la TV`);
}

// ------------------------------------------------------------ ajustes

const drawer = $("#drawer");
$("#openSettings").addEventListener("click", () => { drawer.classList.add("open"); send({ t: "credits" }); });
$("#closeSettings").addEventListener("click", () => drawer.classList.remove("open"));
drawer.addEventListener("click", (e) => { if (e.target === drawer) drawer.classList.remove("open"); });
$("#saveIp").addEventListener("click", () => { send({ t: "settings", tvIp: $("#tvIp").value }); toast("Guardado"); });
$("#saveKey").addEventListener("click", () => { send({ t: "settings", customKey: $("#customKey").value }); $("#customKey").value = ""; toast("Clave guardada (cifrada)"); });
$("#updateTv").addEventListener("click", () => send({ t: "updateTv" }));
$("#autostart").addEventListener("change", (e) => send({ t: "settings", autostart: e.target.checked }));
addEventListener("keydown", (e) => { if (e.key === "Escape") drawer.classList.remove("open"); });

function toast(text, bad) {
  const t = document.createElement("div");
  t.className = "toast" + (bad ? " bad" : "");
  t.textContent = text;
  $("#toasts").append(t);
  setTimeout(() => { t.classList.add("out"); setTimeout(() => t.remove(), 300); }, 2800);
}

// ------------------------------------------------------------ mensajes de la app

host.addEventListener("message", (e) => {
  const m = e.data;
  switch (m.t) {
    case "settings":
      if (m.voz != null) $("#voz").checked = m.voz;
      if (m.pausar != null) $("#pausar").checked = m.pausar;
      if (m.encender != null) $("#encender").checked = m.encender;
      if (m.autostart != null) $("#autostart").checked = m.autostart;
      if (m.tvIp !== undefined) $("#tvIp").value = m.tvIp || "";
      if (m.keys != null) $("#keysInfo").textContent = m.keys ? `${m.keys} cuenta(s) lista(s) · las de la Fábrica de Animaciones${m.customKey ? " + clave propia" : ""}` : "Sin clave: hablará la voz de la TV";
      if (m.presets) { S.presets = m.presets; renderPresets(); }
      if (m.api) $("#apiInfo").textContent = `POST ${m.api}/aviso\n{"titulo":"…","mensaje":"…","estilo":"urgente"}\n\nPuenteTV.exe --aviso "texto" --estilo listo`;
      if (m.voiceId && !$("#voice").dataset.loaded) $("#voice").innerHTML = `<option value="${m.voiceId}"></option>`, $("#voice").options[0].textContent = m.voiceName;
      break;
    case "voices": {
      if (!m.list?.length) break;
      const sel = $("#voice");
      sel.innerHTML = "";
      sel.dataset.loaded = "1";
      [...m.list].sort((a, b) => (a.cat === "cloned" ? -1 : 0) - (b.cat === "cloned" ? -1 : 0) || a.name.localeCompare(b.name)).forEach((v) => {
        const o = document.createElement("option");
        o.value = v.id;
        o.textContent = v.name + (v.cat === "cloned" ? " · clonada" : "");
        sel.append(o);
      });
      if (![...sel.options].some((o) => o.value === m.selected)) {
        const o = document.createElement("option");
        o.value = m.selected; o.textContent = "Alberto Rodríguez";
        sel.prepend(o);
      }
      sel.value = m.selected;
      break;
    }
    case "tv": renderTv(m); break;
    case "history": renderHist(m); break;
    case "toast": toast(m.text, m.bad); break;
    case "previewAudio": {
      $("#preview").classList.remove("busy");
      const a = $("#player");
      a.src = "data:audio/mpeg;base64," + m.b64;
      a.play();
      break;
    }
    case "credits": {
      $("#preview").classList.remove("busy");
      $("#credits").innerHTML = "";
      m.list.forEach((c) => {
        const d = document.createElement("div");
        d.innerHTML = "<span></span>: <b></b>";
        d.querySelector("span").textContent = c.name;
        d.querySelector("b").textContent = c.left == null ? "sin respuesta" : `${Number(c.left).toLocaleString("es-MX")} créditos`;
        $("#credits").append(d);
      });
      break;
    }
  }
});

send({ t: "ready" });
refreshMini();

function demoHost() {
  const ls = [];
  const emit = (m) => ls.forEach((f) => f({ data: m }));
  setTimeout(() => {
    emit({ t: "settings", voz: true, pausar: true, encender: false, autostart: true, tvIp: "red de la casa", keys: 3, api: "",
      voiceId: "l1zE9xgNpUTaQCZzpNJa", voiceName: "Alberto Rodríguez",
      presets: [
        { titulo: "La comida está lista", mensaje: "Ya pueden bajar a comer.", estilo: "listo" },
        { titulo: "Tocan a la puerta", mensaje: "Alguien está en la entrada.", estilo: "importante" },
        { titulo: "Hora de dormir", mensaje: "Es hora de apagar la tele e ir a la cama.", estilo: "info" },
        { titulo: "Necesito ayuda", mensaje: "Por favor ven a la computadora en cuanto puedas.", estilo: "urgente" },
      ] });
    emit({ t: "tv", online: true, name: "Google TV Streamer", ip: "red de la casa", overlay: true, control: true, app: "YouTube", info: "reproduciendo" });
    emit({ t: "history", id: "a", kind: "aviso", title: "La comida está lista", status: "mostrado", style: "listo", time: "12:35" });
    emit({ t: "history", id: "b", kind: "aviso", title: "¡Puente TV listo!", status: "mostrado", style: "listo", time: "12:56" });
  }, 200);
  return { postMessage: (m) => console.log("→", m), addEventListener: (_, f) => ls.push(f) };
}
