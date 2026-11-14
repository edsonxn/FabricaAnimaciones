"use strict";

const $ = (s) => document.querySelector(s);
// Fuera de la app (navegador normal) se usa un anfitrión de demostración para ver la interfaz
const host = window.chrome?.webview || demoHost();
const send = (msg) => host?.postMessage(msg);

function demoHost() {
  const listeners = [];
  const emit = (m) => listeners.forEach((f) => f({ data: m }));
  setTimeout(() => {
    emit({ t: "settings", pc: "TORRE", folder: "Descargas\\Rayo", autostart: true, port: 50520 });
    emit({ t: "device", connected: true, name: "Xiaomi 2412DPC0AG", ip: "red de la casa", battery: 76, charging: true });
    emit({ t: "transfer", id: "a", out: true, name: "Escaner-2.1.apk", size: 6.1e6, done: 6.1e6, status: "done", speed: 0, time: "20:17" });
    emit({ t: "transfer", id: "b", out: true, name: "Manual Puente TV.pdf", size: 1.8e6, done: 1.8e6, status: "done", speed: 0, time: "17:13" });
    emit({ t: "transfer", id: "c", out: false, text: "¿Ya llegó?", name: "Texto", size: 0, done: 0, status: "done", time: "09:42" });
    let done = 0;
    const size = 2.4e9;
    const tick = setInterval(() => {
      done = Math.min(size, done + 6.8e6);
      emit({ t: "transfer", id: "d", out: true, name: "robotaller_4apps_MASTER.mp4", size, done, status: done >= size ? "done" : "active", speed: 68e6, time: "09:45" });
      if (done >= size) clearInterval(tick);
    }, 100);
  }, 300);
  return { postMessage: (m) => console.log("→ host", m), addEventListener: (_, f) => listeners.push(f) };
}

const state = {
  connected: false,
  phone: null,
  items: new Map(), // id -> datos
  els: new Map(),   // id -> elemento
  filter: "all",
};

// ------------------------------------------------------------ formatos

function fmtBytes(b) {
  if (b < 1024) return `${b} B`;
  const u = ["KB", "MB", "GB", "TB"];
  let i = -1;
  do { b /= 1024; i++; } while (b >= 1024 && i < u.length - 1);
  return `${b.toFixed(b >= 100 ? 0 : 1)} ${u[i]}`;
}

function fmtEta(sec) {
  if (!isFinite(sec) || sec <= 0) return "";
  if (sec < 60) return `${Math.ceil(sec)} s`;
  const m = Math.floor(sec / 60);
  return m < 60 ? `${m} min ${Math.round(sec % 60)} s` : `${Math.floor(m / 60)} h ${m % 60} min`;
}

const ICONS = {
  image: ["#f472b6", '<rect x="3" y="4" width="18" height="16" rx="3"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-9 9"/>'],
  video: ["#a78bfa", '<rect x="3" y="5" width="13" height="14" rx="3"/><path d="m16 10 5-3v10l-5-3"/>'],
  audio: ["#fbbf24", '<path d="M9 18V6l11-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>'],
  archive: ["#fb923c", '<rect x="4" y="3" width="16" height="18" rx="3"/><path d="M12 3v4m0 2v2m0 2v2"/>'],
  apk: ["#34d399", '<rect x="6" y="2" width="12" height="20" rx="2.8"/><path d="M10.5 18.5h3"/>'],
  doc: ["#60a5fa", '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'],
  text: ["#22d3ee", '<path d="M4 6h16M4 11h16M4 16h10"/>'],
  file: ["#94a3b8", '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>'],
};

function kindOf(item) {
  if (item.text != null) return "text";
  const ext = (item.name.split(".").pop() || "").toLowerCase();
  if (/^(jpe?g|png|gif|webp|heic|heif|bmp|svg|avif)$/.test(ext)) return "image";
  if (/^(mp4|mkv|mov|avi|webm|3gp|m4v)$/.test(ext)) return "video";
  if (/^(mp3|wav|flac|m4a|ogg|opus|aac)$/.test(ext)) return "audio";
  if (/^(zip|rar|7z|tar|gz)$/.test(ext)) return "archive";
  if (ext === "apk") return "apk";
  if (/^(pdf|docx?|xlsx?|pptx?|txt|csv|md|rtf|odt)$/.test(ext)) return "doc";
  return "file";
}

const svg = (paths, extra = "") => `<svg viewBox="0 0 24 24" ${extra}>${paths}</svg>`;
const ARROW_UP = svg('<path d="M12 19V5m-6 6 6-6 6 6"/>');
const ARROW_DOWN = svg('<path d="M12 5v14m-6-6 6 6 6-6"/>');
const ACT = {
  cancel: ["Cancelar", svg('<path d="M6 6l12 12M18 6 6 18"/>')],
  retry: ["Reintentar", svg('<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>')],
  open: ["Abrir", svg('<path d="M14 4h6v6M20 4l-9 9"/><path d="M19 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h4"/>')],
  reveal: ["Mostrar en carpeta", svg('<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>')],
  copy: ["Copiar", svg('<rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/>')],
};
const CHECK = `<span class="check">${svg('<path d="m5 12 5 5 9-10"/>')}</span>`;

// ------------------------------------------------------------ lista de actividad

function renderItem(it) {
  let el = state.els.get(it.id);
  const kind = kindOf(it);
  if (!el) {
    el = document.createElement("div");
    el.className = "item";
    const [color, paths] = ICONS[kind];
    el.style.setProperty("--c", color);
    el.innerHTML = `
      <div class="ficon">${svg(paths)}<span class="dir">${it.out ? ARROW_UP : ARROW_DOWN}</span></div>
      <div class="meta"><div class="name"></div><div class="sub"></div><div class="bar"><i></i></div></div>
      <div class="actions"></div>`;
    el.querySelector(".ficon").title = it.out ? "Enviado al teléfono" : "Recibido del teléfono";
    el.querySelector(".actions").addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      const a = b.dataset.a;
      if (a === "copy") { send({ t: "copy", text: it.text }); toast("Copiado"); }
      else send({ t: a, id: it.id });
    });
    if (it.text == null) el.addEventListener("dblclick", () => it.status === "done" && send({ t: "open", id: it.id }));
    state.els.set(it.id, el);
    $("#list").prepend(el);
  }

  const name = el.querySelector(".name");
  const sub = el.querySelector(".sub");
  const acts = el.querySelector(".actions");
  el.classList.remove("queued", "active", "done", "error", "cancelled");
  el.classList.add(it.status);

  if (it.text != null) {
    name.textContent = it.text;
    name.classList.add("textual");
    sub.textContent = `${it.out ? "Enviado" : "Recibido · copiado al portapapeles"} · ${it.time}`;
    setActions(acts, ["copy"], it.status);
  } else {
    name.textContent = it.name;
    name.title = it.name;
    const pct = it.size ? Math.min(100, (it.done / it.size) * 100) : 0;
    el.querySelector(".bar i").style.width = pct + "%";
    let s;
    switch (it.status) {
      case "queued": s = `${fmtBytes(it.size)} · ${state.connected ? "en cola" : "se enviará al conectar el teléfono"}`; break;
      case "active": {
        const eta = it.speed ? fmtEta((it.size - it.done) / it.speed) : "";
        s = `${Math.floor(pct)}% · ${fmtBytes(it.done)} de ${fmtBytes(it.size)}${it.speed ? ` · ${fmtBytes(it.speed)}/s` : ""}${eta ? ` · ${eta}` : ""}`;
        break;
      }
      case "done": s = `<span class="ok">${it.out ? "Enviado" : "Recibido"}</span> · ${fmtBytes(it.size)} · ${it.time}`; break;
      case "error": s = `<span class="bad">Falló</span> · ${fmtBytes(it.size)}`; break;
      default: s = `Cancelado · ${fmtBytes(it.size)}`;
    }
    sub.innerHTML = s;
    const list = {
      queued: ["cancel"], active: ["cancel"],
      done: it.out ? ["reveal"] : ["open", "reveal"],
      error: it.out ? ["retry"] : [], cancelled: it.out ? ["retry"] : [],
    }[it.status];
    setActions(acts, list, it.status);
  }
  applyFilter(el, it);
}

function setActions(box, list, status) {
  const key = status + list.join();
  if (box.dataset.key === key) return;
  box.dataset.key = key;
  box.innerHTML = (status === "done" && box.closest(".item").dataset.wasActive ? CHECK : "") +
    list.map((a) => `<button data-a="${a}" title="${ACT[a][0]}">${ACT[a][1]}</button>`).join("");
}

function applyFilter(el, it) {
  const f = state.filter;
  el.classList.toggle("hidden", f !== "all" && (f === "out") !== it.out);
}

function refreshEmpty() {
  const visible = [...state.els.values()].some((e) => !e.classList.contains("hidden"));
  $("#empty").classList.toggle("gone", visible);
}

$("#filters").addEventListener("click", (e) => {
  const b = e.target.closest(".chip");
  if (!b) return;
  document.querySelectorAll(".chip").forEach((c) => c.classList.toggle("on", c === b));
  state.filter = b.dataset.f;
  state.items.forEach((it) => applyFilter(state.els.get(it.id), it));
  refreshEmpty();
});

$("#clear").addEventListener("click", () => send({ t: "clear" }));

// ------------------------------------------------------------ teléfono

function renderDevice(d) {
  state.connected = d.connected;
  state.phone = d.name || null;
  $("#phoneName").textContent = d.name || "Teléfono";
  $("#setPhone").textContent = d.name || "Ninguno";
  $("#forget").disabled = !d.name;
  const bat = $("#battery");
  if (d.connected && d.battery >= 0) {
    bat.textContent = `${d.charging ? "⚡ " : ""}${d.battery}%`;
    bat.className = "battery" + (d.charging ? " charging" : d.battery <= 15 ? " low" : "");
  } else bat.textContent = "";
  $("#linkStatus").textContent = d.connected
    ? `Conectado por WiFi · ${d.ip}`
    : d.name ? `Esperando a ${d.name}… (abre Rayo en el teléfono o conéctalo a tu WiFi)` : "Buscando tu teléfono… instala Rayo en él y ábrelo en la misma red";
  $("#overlayText").textContent = d.connected ? `Suelta para enviar a ${d.name}` : "Suelta y se enviará cuando el teléfono se conecte";
  updateLink();
  state.items.forEach((it) => it.status === "queued" && renderItem(it));
}

function updateLink() {
  const active = [...state.items.values()].filter((i) => i.status === "active");
  const speed = active.reduce((a, i) => a + (i.speed || 0), 0);
  const link = $("#link");
  link.dataset.state = !state.connected ? "off" : active.length ? "busy" : "on";
  beam.out = active.some((i) => i.out);
  beam.in = active.some((i) => !i.out);
  beam.rate = speed;
  if (active.length) {
    const mb = speed / 1048576;
    $("#speed").textContent = mb >= 10 ? mb.toFixed(0) : mb.toFixed(1);
    $("#speedMbps").textContent = `${Math.round((speed * 8) / 1e6)} Mbps`;
  }
}

// ------------------------------------------------------------ animación del haz

const beam = { out: false, in: false, rate: 0, parts: [] };
(function animateBeam() {
  const c = $("#beam");
  const ctx = c.getContext("2d");
  let w = 0, h = 0;
  const resize = () => {
    const r = c.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    w = r.width; h = r.height;
    c.width = w * dpr; c.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  new ResizeObserver(resize).observe(c);

  const point = (t) => {
    const x0 = 10, x1 = w - 10, y = h / 2, lift = h * 0.32;
    const x = x0 + (x1 - x0) * t;
    return [x, y - Math.sin(t * Math.PI) * lift * 0.5];
  };
  let last = performance.now();

  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    ctx.clearRect(0, 0, w, h);
    const st = $("#link").dataset.state;

    // línea base
    ctx.beginPath();
    for (let i = 0; i <= 40; i++) { const [x, y] = point(i / 40); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    const g = ctx.createLinearGradient(0, 0, w, 0);
    g.addColorStop(0, "rgba(139,92,246,.75)");
    g.addColorStop(1, "rgba(34,211,238,.75)");
    ctx.strokeStyle = st === "off" ? "rgba(255,255,255,.12)" : g;
    ctx.lineWidth = st === "busy" ? 2.5 : 1.5;
    ctx.setLineDash(st === "off" ? [4, 8] : []);
    ctx.lineDashOffset = -now / 60;
    ctx.stroke();
    ctx.setLineDash([]);

    // partículas: más y más rápidas cuanto mayor la velocidad
    if (st !== "off") {
      const busy = st === "busy";
      const target = busy ? 26 + Math.min(40, beam.rate / 2e6) : 6;
      if (beam.parts.length < target && Math.random() < (busy ? 0.6 : 0.08)) {
        const dirs = busy ? [beam.out && 1, beam.in && -1].filter(Boolean) : [1, -1];
        const d = dirs[Math.floor(Math.random() * dirs.length)] || 1;
        beam.parts.push({ t: d > 0 ? 0 : 1, d, v: busy ? 0.45 + Math.random() * 0.5 : 0.12 + Math.random() * 0.08, r: busy ? 1.5 + Math.random() * 2 : 1.4 });
      }
    }
    beam.parts = beam.parts.filter((p) => p.t >= 0 && p.t <= 1 && st !== "off");
    for (const p of beam.parts) {
      p.t += p.d * p.v * dt;
      const [x, y] = point(Math.max(0, Math.min(1, p.t)));
      const fade = Math.sin(Math.max(0, Math.min(1, p.t)) * Math.PI);
      ctx.beginPath();
      ctx.arc(x, y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = p.d > 0 ? `rgba(196,181,253,${fade})` : `rgba(103,232,249,${fade})`;
      ctx.shadowColor = p.d > 0 ? "#8b5cf6" : "#22d3ee";
      ctx.shadowBlur = 12;
      ctx.fill();
      ctx.shadowBlur = 0;
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();

// ------------------------------------------------------------ arrastrar y soltar

let dragDepth = 0;
const hasFiles = (e) => [...(e.dataTransfer?.types || [])].includes("Files");
window.addEventListener("dragenter", (e) => { if (!hasFiles(e)) return; e.preventDefault(); dragDepth++; document.body.classList.add("dragging"); });
window.addEventListener("dragover", (e) => { if (!hasFiles(e)) return; e.preventDefault(); e.dataTransfer.dropEffect = "copy"; });
window.addEventListener("dragleave", () => { if (--dragDepth <= 0) { dragDepth = 0; document.body.classList.remove("dragging"); } });
window.addEventListener("drop", (e) => {
  e.preventDefault();
  dragDepth = 0;
  document.body.classList.remove("dragging");
  const files = e.dataTransfer?.files;
  if (files?.length && host?.postMessageWithAdditionalObjects) {
    host.postMessageWithAdditionalObjects({ t: "drop" }, files);
    toast(files.length === 1 ? `Enviando ${files[0].name}` : `Enviando ${files.length} elementos`);
  }
});

$("#pickFiles").addEventListener("click", () => send({ t: "pickFiles" }));
$("#pickFolder").addEventListener("click", () => send({ t: "pickFolder" }));

// ------------------------------------------------------------ texto

const text = $("#text");
const sendBtn = $("#sendText");
text.addEventListener("input", () => (sendBtn.disabled = !text.value.trim() || !state.connected));
function sendText() {
  const v = text.value.trim();
  if (!v || !state.connected) return;
  send({ t: "text", text: v });
  text.value = "";
  sendBtn.disabled = true;
  toast("Texto enviado al teléfono");
}
sendBtn.addEventListener("click", sendText);
text.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.ctrlKey) { e.preventDefault(); sendText(); } });

// ------------------------------------------------------------ ajustes y emparejar

const drawer = $("#drawer");
$("#openSettings").addEventListener("click", () => drawer.classList.add("open"));
$("#closeSettings").addEventListener("click", () => drawer.classList.remove("open"));
drawer.addEventListener("click", (e) => { if (e.target === drawer) drawer.classList.remove("open"); });
$("#openFolder").addEventListener("click", () => send({ t: "openFolder" }));
$("#changeFolder").addEventListener("click", () => send({ t: "changeFolder" }));
$("#setAutostart").addEventListener("change", (e) => send({ t: "autostart", value: e.target.checked }));
$("#forget").addEventListener("click", () => { send({ t: "forget" }); toast("Teléfono olvidado"); });

let pairId = null;
const pairModal = $("#pairModal");
function answerPair(ok) {
  send({ t: "pairAnswer", id: pairId, accept: ok });
  pairModal.classList.remove("open");
  if (ok) toast("Teléfono emparejado");
}
$("#pairYes").addEventListener("click", () => answerPair(true));
$("#pairNo").addEventListener("click", () => answerPair(false));

function toast(msg) {
  const t = document.createElement("div");
  t.className = "toast";
  t.innerHTML = `${svg('<path d="m5 12 5 5 9-10"/>')}<span></span>`;
  t.querySelector("span").textContent = msg;
  $("#toasts").append(t);
  setTimeout(() => { t.classList.add("out"); setTimeout(() => t.remove(), 300); }, 2600);
}

window.addEventListener("keydown", (e) => {
  if (e.key === "Escape") { drawer.classList.remove("open"); }
  // Ctrl+V fuera del cuadro de texto: manda lo copiado
  if (e.key === "v" && e.ctrlKey && document.activeElement !== text) text.focus();
});

// ------------------------------------------------------------ mensajes desde la PC

host?.addEventListener("message", (e) => {
  const m = e.data;
  switch (m.t) {
    case "settings":
      if (m.pc) { $("#pcName").textContent = m.pc; $("#setPc").textContent = m.pc; }
      if (m.folder) $("#setFolder").textContent = m.folder;
      if (m.autostart != null) $("#setAutostart").checked = m.autostart;
      if (m.port) $("#setPort").textContent = `Puertos de red: TCP ${m.port} y UDP ${m.port + 1}`;
      break;
    case "device":
      renderDevice(m);
      break;
    case "transfer": {
      const prev = state.items.get(m.id);
      const el = state.els.get(m.id);
      if (el && prev?.status === "active") el.dataset.wasActive = "1";
      if (!prev && m.status === "active" && !m.out) toast(`Recibiendo ${m.name}`);
      if (prev && prev.status !== "done" && m.status === "done" && !m.out && m.text == null) toast(`Recibiste ${m.name}`);
      if (!prev && m.text != null && !m.out) toast("Texto recibido y copiado");
      state.items.set(m.id, m);
      renderItem(m);
      updateLink();
      refreshEmpty();
      break;
    }
    case "removed": {
      const el = state.els.get(m.id);
      state.items.delete(m.id);
      state.els.delete(m.id);
      if (el) { el.classList.add("leaving"); setTimeout(() => { el.remove(); refreshEmpty(); }, 300); }
      break;
    }
    case "toast":
      toast(m.text);
      break;
    case "pair":
      pairId = m.id;
      $("#pairName").textContent = m.name;
      pairModal.classList.add("open");
      break;
  }
});

send({ t: "ready" });
refreshEmpty();
