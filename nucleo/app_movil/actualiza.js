// Aviso de actualización (28-oct-2026, pedido del usuario: «cuando haya actualización de la app me aparezca al entrar»).
// Lee /v2/app/version.json (público) al abrir el panel, la Aldea o la Fábrica 3D:
//  - si la app Android instalada (agente «FabricaApp/… v=<código>») es más vieja que el APK publicado → «Descargar la nueva»;
//  - si las novedades de la web cambiaron desde la última visita en este teléfono → «¡Actualización!» con la lista.
(function () {
  "use strict";
  var CLAVE = "fab_ver_web";
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function leer(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function poner(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function mostrar(V, apkVieja) {
    var css = document.createElement("style");
    css.textContent = "#fabupd{position:fixed;inset:0;z-index:9999;display:grid;place-items:center;padding:20px;background:rgba(4,5,10,.72);font:15px/1.45 system-ui,-apple-system,'Segoe UI',sans-serif;color:#eef0f7;animation:fabupdF .3s}" +
      "@keyframes fabupdF{from{opacity:0}}@keyframes fabupdS{from{transform:translateY(30px) scale(.94);opacity:0}}" +
      "#fabupd .c{width:min(420px,100%);max-height:86vh;overflow:auto;background:linear-gradient(160deg,#1d1a33,#12141e);border:1px solid #3a3560;border-radius:22px;padding:22px 20px 18px;box-shadow:0 30px 80px rgba(0,0,0,.6);animation:fabupdS .45s cubic-bezier(.2,1.3,.4,1)}" +
      "#fabupd .e{font-size:44px;text-align:center}#fabupd h2{margin:4px 0 2px;text-align:center;font-size:22px}#fabupd .v{text-align:center;color:#9aa0b8;font-size:12.5px;margin-bottom:12px}" +
      "#fabupd ul{margin:0;padding:0 0 0 4px;list-style:none}#fabupd li{padding:7px 0 7px 2px;border-bottom:1px solid #26294a;font-size:14px}#fabupd li:last-child{border:0}" +
      "#fabupd .b{display:flex;align-items:center;justify-content:center;height:48px;border-radius:14px;margin-top:12px;font-weight:700;text-decoration:none;color:#fff;background:linear-gradient(135deg,#7a62ff,#ff5fa8);border:0;width:100%;font-size:15px;cursor:pointer}" +
      "#fabupd .b2{background:#262a40;color:#cfd3e6}#fabupd .apk{background:linear-gradient(135deg,#ffb547,#ff6b3d);color:#1b1004}";
    document.head.appendChild(css);
    var notas = (apkVieja ? V.apk.notas || [] : []).concat(V.web.notas || []);
    var d = document.createElement("div");
    d.id = "fabupd";
    d.innerHTML = '<div class="c"><div class="e">' + (apkVieja ? "📲" : "🆕") + "</div><h2>" + (apkVieja ? "Hay una app nueva" : "¡Actualización!") + "</h2>" +
      '<div class="v">' + esc(apkVieja ? "Versión " + V.apk.nombre : (V.web.fecha || V.web.version)) + "</div><ul>" +
      notas.map(function (n) { return "<li>" + esc(n) + "</li>"; }).join("") + "</ul>" +
      (apkVieja ? '<a class="b apk" href="' + esc(V.apk.url) + '">⬇ Descargar la app nueva</a><div style="font-size:12px;color:#9aa0b8;text-align:center;margin-top:6px">Ábrela al terminar y toca «Actualizar»: se instala encima, sin perder nada.</div>' : "") +
      '<button class="b' + (apkVieja ? " b2" : "") + '" id="fabupd-ok">' + (apkVieja ? "Después" : "¡Genial!") + "</button></div>";
    document.body.appendChild(d);
    function cerrar() { poner(CLAVE, V.web.version); d.remove(); }
    document.getElementById("fabupd-ok").onclick = cerrar;
    d.addEventListener("click", function (e) { if (e.target === d) cerrar(); });
  }
  function revisar() {
    fetch("/v2/app/version.json", { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (V) {
      if (!V || !V.web) return;
      var ua = navigator.userAgent, enApp = /FabricaApp\//.test(ua), m = ua.match(/\bv=(\d+)/);
      var apkVieja = !!(enApp && V.apk && V.apk.codigo && (!m || +m[1] < V.apk.codigo));
      var webNueva = leer(CLAVE) !== V.web.version;
      if (apkVieja || webNueva) mostrar(V, apkVieja);
    }).catch(function () {});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { setTimeout(revisar, 1200); });
  else setTimeout(revisar, 1200);
})();
