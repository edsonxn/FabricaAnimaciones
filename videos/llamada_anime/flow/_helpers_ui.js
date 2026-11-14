// Helpers de Flow (7-nov, sesión 4) para editar imágenes VIEJAS del proyecto (originales fotorrealistas) a anime.
// Pegar con javascript_tool en la página del proyecto. La búsqueda de la galería busca por TEXTO DEL PROMPT.
// ⚠ NO usar el primer <input> de la página: es el NOMBRE DEL PROYECTO («Texto editable»). La búsqueda es input[aria-label="Buscar"].
// Envío: clic REAL por ref en «Iniciar generación» (el .click() por JS no envía) y comprobar __enviado() = ingr=0 txt=0.
// Patrón por imagen (browser_batch, 3 acciones): js `await __prep1(clave, frase_unica_del_prompt, 'd'|'r'|'')` →
//   computer left_click ref «Iniciar generación» → js `(await __enviado()).join(' ')`.
// __SIG = firmas 8x8 en gris de ../llamada_domingo/flow/bg/*.jpg (PIL resize BOX) para elegir la variante correcta.
window.__w = ms => new Promise(r => setTimeout(r, ms));
window.__ningr = () => { const ed = document.querySelector('.ProseMirror'); const box = ed.closest('form') || ed.parentElement.parentElement.parentElement; return box.querySelectorAll('img').length; };
window.__busca2 = async (txt) => {
  const inp = document.querySelector('input[aria-label="Buscar"]');
  inp.focus(); Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(inp, txt);
  inp.dispatchEvent(new Event('input', {bubbles: true}));
  inp.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}));
};
window.__sig8 = (img) => { const c = document.createElement('canvas'); c.width = 64; c.height = 64; const x = c.getContext('2d'); x.drawImage(img, 0, 0, 64, 64); const d = x.getImageData(0, 0, 64, 64).data; const o = []; for (let by = 0; by < 8; by++) for (let bx = 0; bx < 8; bx++) { let s = 0; for (let y = 0; y < 8; y++) for (let xx = 0; xx < 8; xx++) { const i = ((by * 8 + y) * 64 + bx * 8 + xx) * 4; s += 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]; } o.push(s / 64); } return o; };
// __elige(clave) = entre los resultados, el de firma más parecida a __SIG[clave]; __elige(null, 'uuidpref') = por uuid.
// Abre «Más opciones» del tile y pulsa el menuitem que CONTIENE «Añadir a la petición» (el texto lleva el icono «add_2»).
window.__elige = async (clave, idpref) => {
  await __w(2500);
  let ims = []; for (let i = 0; i < 20; i++) { ims = [...document.querySelectorAll('img[data-media-id]')].filter(im => im.complete && im.naturalWidth); if (ims.length && ims[0].dataset.mediaId !== window.__prevTop) break; await __w(500); }
  window.__prevTop = ims[0] && ims[0].dataset.mediaId;
  let best = null, bd = 1e9;
  for (const im of ims) { if (idpref) { if (im.dataset.mediaId.startsWith(idpref)) { best = im; bd = 0; } continue; }
    const s = __sig8(im), ref = __SIG[clave]; let dd = 0; for (let i = 0; i < 64; i++) dd += Math.abs(s[i] - ref[i]); dd /= 64; if (dd < bd) { bd = dd; best = im; } }
  if (!best) return ['nada'];
  let tile = best, b = null; for (let i = 0; i < 8 && tile && !b; i++) { tile = tile.parentElement; b = [...tile.querySelectorAll('button')].find(x => /Más opciones/.test(x.getAttribute('aria-label') || x.innerText)); }
  best.dispatchEvent(new MouseEvent('mouseover', {bubbles: true})); await __w(300); b.click(); await __w(800);
  const it = [...document.querySelectorAll('[role=menuitem]')].find(e => e.offsetParent && e.innerText.includes('Añadir a la petición'));
  if (!it) return ['sin menú']; it.click(); await __w(1500);
  return [clave || idpref, best.dataset.mediaId.slice(0, 8), 'd=' + bd.toFixed(1)];
};
// Retratos anime (fase A): Daniel da7e9068…, Ramón 5d8d84f6… (búsqueda: «Anime character design portrait of the person in
// the character reference, same face and identity: a 37-year-old» / «… a 71-year-old»).
window.__enviado = async () => { await __w(2500); return ['ingr=' + __ningr(), 'txt=' + document.querySelector('.ProseMirror').innerText.trim().length]; };
// Prompt usado (texto completo en ESTADO.md § sesión 4): base «Redraw the first image as a hand-drawn 2D anime feature film
// still… Keep EXACTLY the same composition…» + cláusula de Daniel/Ramón (segunda imagen) + «No text…».
