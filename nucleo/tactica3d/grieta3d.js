// Mapa táctico 3D de la Grieta del Invocador (nucleo/tactica3d, 27-oct-2026).
// Lee ?escena=<json> (ver docs/estilo_analisis_tactico.md § «Jugada en 3D»), dibuja el cuadro del instante t con
// window.cuadro(t) (JPEG en dataURL, lo usa render3d.py) y, con ?vivo=1, lo reproduce en tiempo real en el navegador.
// Coordenadas: u, v = fracción del minimapa (0,0 arriba-izquierda; base azul abajo-izquierda). Tiempos: segundos del video;
// las pistas de los campeones van en segundos de JUEGO y E.reloj = [[t_video, t_juego], ...] los relaciona.
import * as THREE from 'three';

const Q = new URLSearchParams(location.search);
const W = +(Q.get('w') || 1920), H = +(Q.get('h') || 1080);
const MAPA = 100, ALTO = 3.4;
const COL = { azul: '#46a5ff', rojo: '#ff4452', amarillo: '#ffd60a', blanco: '#ffffff', morado: '#b46bff', verde: '#3ddc84',
              oro: '#f4c542' };
const hex = c => COL[c] || c;
const clamp = (x, a = 0, b = 1) => Math.min(Math.max(x, a), b);
const suave = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const EQUIPO_COLOR = {};

let E, renderer, scene, camera, salida, octx, capa, ctx, alturas, AN;
const fichas = {}, dinamicos = [];
let arbolesMat, nieblaTex, nieblaCtx, nieblaU, aguaMat;

// ------------------------------------------------------------------ utilidades
const cargar = url => new Promise((ok, mal) => {
  const im = new Image(); im.crossOrigin = 'anonymous';
  im.onload = () => ok(im); im.onerror = () => mal(new Error('no carga ' + url)); im.src = url;
});

function alturaUV(u, v) {
  const x = clamp(u) * (AN - 1), y = clamp(v) * (AN - 1);
  const x0 = Math.floor(x), y0 = Math.floor(y), x1 = Math.min(x0 + 1, AN - 1), y1 = Math.min(y0 + 1, AN - 1);
  const fx = x - x0, fy = y - y0, A = alturas;
  return ((A[y0 * AN + x0] * (1 - fx) + A[y0 * AN + x1] * fx) * (1 - fy) +
          (A[y1 * AN + x0] * (1 - fx) + A[y1 * AN + x1] * fx) * fy) * ALTO;
}
// suelo «de camino»: los campeones no se suben a los muros aunque la medida caiga en el borde
const suelo = (u, v) => Math.min(alturaUV(u, v), .62);
// MODO «SOBRE VIDEO» (E.modo = "video", 27-oct-2026): capa transparente encima de un cuadro del VOD. u, v son entonces x, y
// de la PANTALLA (fracción): cada punto se proyecta sobre el suelo de una cámara fija inclinada como la del juego, así los
// anillos salen en perspectiva, las flechas se levantan en arco y todo proyecta sombra sobre el cuadro real.
// MODO «MESA» (E.modo = "mesa"): el cuadro congelado (E.fondo) se proyecta sobre el suelo desde esa misma cámara del juego y
// la cámara de render (E.camara = [[t, giro°, inclinación°, distancia, x, y]…]) parte del encuadre original —el corte con el
// video es invisible—, se inclina/gira para ver la jugada en 3D y vuelve. Las posiciones siguen siendo x, y del cuadro.
let VIDEO = false, MESA = false, camG = null;
const _rayo = new THREE.Raycaster(), _plano = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
function sobreVideo(x, y, dy = 0) {
  _rayo.setFromCamera(new THREE.Vector2(x * 2 - 1, 1 - y * 2), camG);
  const p = new THREE.Vector3(); _rayo.ray.intersectPlane(_plano, p); p.y += dy; return p;
}
const P = (u, v, dy = 0) => VIDEO ? sobreVideo(u, v, dy) : new THREE.Vector3((u - .5) * MAPA, suelo(u, v) + dy, (v - .5) * MAPA);
// radio en fracción del mapa → unidades (en modo video: fracción del ANCHO de la pantalla, medida a media altura)
const R = r => VIDEO ? sobreVideo(.5, .55).distanceTo(sobreVideo(.5 + r, .55)) : r * MAPA;

function lineal(keys, t) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [a, va] = keys[i], [b, vb] = keys[i + 1];
    if (t <= b) return va + (vb - va) * (b > a ? (t - a) / (b - a) : 1);
  }
  return keys[keys.length - 1][1];
}
const juego = t => lineal(E.reloj, t);
const reloj = g => { const s = Math.max(0, g); return `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`; };

function catmull(p0, p1, p2, p3, s) {
  const s2 = s * s, s3 = s2 * s;
  return .5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s2 + (-p0 + 3 * p1 - 3 * p2 + p3) * s3);
}

// posición (u, v) de una pista en el segundo de juego g. Un punto con 4.º elemento 'salto' = aparece ahí de golpe (TP, regreso)
function posicion(pts, g) {
  if (g <= pts[0][0]) return [pts[0][1], pts[0][2]];
  const n = pts.length;
  if (g >= pts[n - 1][0]) return [pts[n - 1][1], pts[n - 1][2]];
  let i = 0;
  while (i < n - 2 && g > pts[i + 1][0]) i++;
  const b = pts[i], c = pts[i + 1];
  if (c[3] === 'salto') return [b[1], b[2]];
  const a = (i > 0 && b[3] !== 'salto') ? pts[i - 1] : b;
  const d = (i + 2 < n && pts[i + 2][3] !== 'salto') ? pts[i + 2] : c;
  const s = (g - b[0]) / (c[0] - b[0]);
  return [catmull(a[1], b[1], c[1], d[1], s), catmull(a[2], b[2], c[2], d[2], s)];
}

function textura(canvas) {
  const t = new THREE.CanvasTexture(canvas); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

function brillo(color, tam = 128) {
  const c = document.createElement('canvas'); c.width = c.height = tam; const x = c.getContext('2d');
  const g = x.createRadialGradient(tam / 2, tam / 2, 0, tam / 2, tam / 2, tam / 2);
  const col = new THREE.Color(hex(color));
  const rgb = `${Math.round(col.r * 255)},${Math.round(col.g * 255)},${Math.round(col.b * 255)}`;
  g.addColorStop(0, `rgba(255,255,255,1)`); g.addColorStop(.18, `rgba(${rgb},.9)`); g.addColorStop(1, `rgba(${rgb},0)`);
  x.fillStyle = g; x.fillRect(0, 0, tam, tam);
  return textura(c);
}

function medallon(img, color, tam = 256) {
  const c = document.createElement('canvas'); c.width = c.height = tam; const x = c.getContext('2d'), r = tam / 2;
  x.beginPath(); x.arc(r, r, r - 3, 0, 7); x.fillStyle = '#0b0f17'; x.fill();
  if (img) {
    x.save(); x.beginPath(); x.arc(r, r, r - 22, 0, 7); x.clip();
    const lado = Math.min(img.width, img.height), z = (tam - 40) / (lado * .86);
    const w = img.width * z, h = img.height * z;
    x.drawImage(img, r - w / 2, r - h / 2, w, h); x.restore();
  }
  x.lineWidth = 16; x.strokeStyle = hex(color); x.beginPath(); x.arc(r, r, r - 13, 0, 7); x.stroke();
  x.lineWidth = 3; x.strokeStyle = 'rgba(255,255,255,.9)'; x.beginPath(); x.arc(r, r, r - 23, 0, 7); x.stroke();
  x.lineWidth = 3; x.strokeStyle = 'rgba(0,0,0,.8)'; x.beginPath(); x.arc(r, r, r - 3, 0, 7); x.stroke();
  return textura(c);
}

// ------------------------------------------------------------------ escenario
async function terreno() {
  const raiz = E.assets || '/nucleo/tactica3d/assets/';
  const [imAlt, imCol] = await Promise.all([cargar(raiz + 'grieta_altura.png'), cargar(raiz + 'grieta_color.png')]);
  const cv = document.createElement('canvas'); AN = imAlt.width; cv.width = cv.height = AN;
  const cx = cv.getContext('2d'); cx.drawImage(imAlt, 0, 0);
  const px = cx.getImageData(0, 0, AN, AN).data; alturas = new Float32Array(AN * AN);
  for (let i = 0; i < AN * AN; i++) alturas[i] = px[i * 4] / 255;

  const geo = new THREE.PlaneGeometry(MAPA, MAPA, 384, 384); geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) {
    const u = pos.getX(i) / MAPA + .5, v = pos.getZ(i) / MAPA + .5; pos.setY(i, alturaUV(u, v));
  }
  geo.computeVertexNormals();
  const tex = new THREE.Texture(imCol); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 16; tex.needsUpdate = true;
  const suelo3d = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, roughness: .92, metalness: 0 }));
  suelo3d.receiveShadow = true; suelo3d.castShadow = true; scene.add(suelo3d);

  // agua del río: plano a ras que solo asoma donde el terreno está más bajo
  const agua = new THREE.Mesh(new THREE.PlaneGeometry(MAPA, MAPA), new THREE.MeshStandardMaterial({
    color: 0x2aa6c9, transparent: true, opacity: .62, roughness: .12, metalness: .2, emissive: 0x0b3b4a, emissiveIntensity: .5 }));
  agua.rotateX(-Math.PI / 2); agua.position.y = .2; agua.receiveShadow = true; scene.add(agua);

  // fuera del mapa
  const fuera = new THREE.Mesh(new THREE.PlaneGeometry(800, 800), new THREE.MeshStandardMaterial({ color: 0x0c1712, roughness: 1 }));
  fuera.rotateX(-Math.PI / 2); fuera.position.y = -.3; fuera.receiveShadow = true; scene.add(fuera);

  // árboles sobre los muros (dos conos por árbol)
  const arb = await (await fetch(raiz + 'arboles.json')).json();
  arbolesMat = new THREE.MeshStandardMaterial({ roughness: .85, flatShading: true });
  const g1 = new THREE.ConeGeometry(.95, 2.2, 7), g2 = new THREE.ConeGeometry(.7, 1.7, 7);
  const m1 = new THREE.InstancedMesh(g1, arbolesMat, arb.length), m2 = new THREE.InstancedMesh(g2, arbolesMat, arb.length);
  const o = new THREE.Object3D(), c = new THREE.Color();
  arb.forEach(([u, v, s], i) => {
    const y = alturaUV(u, v);
    o.position.set((u - .5) * MAPA, y + 1.0 * s, (v - .5) * MAPA); o.scale.setScalar(s); o.rotation.y = i; o.updateMatrix();
    m1.setMatrixAt(i, o.matrix);
    o.position.y = y + 2.1 * s; o.updateMatrix(); m2.setMatrixAt(i, o.matrix);
    c.setHSL(.27 + .07 * Math.sin(i * 12.9898), .45, .2 + .07 * Math.sin(i * 78.233)); m1.setColorAt(i, c);
    c.offsetHSL(0, 0, .05); m2.setColorAt(i, c);
  });
  for (const m of [m1, m2]) { m.castShadow = true; m.receiveShadow = true; scene.add(m); }

  // niebla de guerra: el sombreador del terreno oscurece según un lienzo pintado cada cuadro (blanco = sin visión)
  const nc = document.createElement('canvas'); nc.width = nc.height = 512; nieblaCtx = nc.getContext('2d');
  nieblaTex = new THREE.CanvasTexture(nc);
  nieblaU = { nieblaMapa: { value: nieblaTex }, nieblaK: { value: 0 } };
  suelo3d.material.onBeforeCompile = sh => {
    Object.assign(sh.uniforms, nieblaU);
    sh.fragmentShader = 'uniform sampler2D nieblaMapa;\nuniform float nieblaK;\n' + sh.fragmentShader.replace('#include <opaque_fragment>',
      'outgoingLight *= 1.0 - nieblaK * texture2D(nieblaMapa, vMapUv).r * 0.9;\noutgoingLight += vec3(0.0, 0.01, 0.03) * nieblaK * texture2D(nieblaMapa, vMapUv).r;\n#include <opaque_fragment>');
  };
  aguaMat = agua.material;
}

function estructura(d) {
  const g = new THREE.Group(), col = new THREE.Color(hex(EQUIPO_COLOR[d.equipo] || d.color || 'blanco'));
  const piedra = new THREE.MeshStandardMaterial({ color: 0x77808c, roughness: .7, metalness: .1 });
  const cristal = new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: 1.1, roughness: .2 });
  if (d.tipo === 'torre') {
    const t = new THREE.Mesh(new THREE.CylinderGeometry(.75, 1.15, 3.8, 10), piedra); t.position.y = 1.9;
    const k = new THREE.Mesh(new THREE.OctahedronGeometry(.75), cristal); k.position.y = 4.5; k.name = 'gira';
    const b = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.8, .4, 14), piedra); b.position.y = .2;
    g.add(t, k, b);
  } else if (d.tipo === 'inhibidor') {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(1.6, 1.9, .5, 16), piedra); b.position.y = .25;
    const r = new THREE.Mesh(new THREE.TorusGeometry(1.25, .22, 8, 28), cristal); r.rotation.x = Math.PI / 2; r.position.y = .9;
    const k = new THREE.Mesh(new THREE.OctahedronGeometry(.95), cristal); k.position.y = 2.6; k.name = 'gira';
    g.add(b, r, k);
  } else {   // nexo
    const b = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 3.2, 1.0, 18), piedra); b.position.y = .5;
    const k = new THREE.Mesh(new THREE.OctahedronGeometry(2.0), cristal); k.position.y = 3.8; k.name = 'gira';
    g.add(b, k);
  }
  g.traverse(m => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });
  g.position.copy(P(d.u, d.v)); scene.add(g);
  const polvo = [];
  if (d.cae != null) {
    const mat = new THREE.SpriteMaterial({ map: brillo('#b9b2a5'), transparent: true, depthWrite: false, opacity: 0 });
    for (let i = 0; i < 16; i++) { const s = new THREE.Sprite(mat.clone()); s.visible = false; scene.add(s); polvo.push(s); }
  }
  dinamicos.push(t => {
    const gira = g.getObjectByName('gira'); if (gira) { gira.rotation.y = t * 1.3; gira.position.y += Math.sin(t * 2) * .004; }
    if (d.cae == null) return;
    const k = clamp((t - d.cae) / .9);
    g.position.y = P(d.u, d.v).y - 5 * suave(k); g.rotation.z = .5 * k; g.visible = k < 1;
    polvo.forEach((s, i) => {
      const q = clamp((t - d.cae) / 1.8); const a = i / polvo.length * Math.PI * 2;
      s.visible = q > 0 && q < 1;
      s.position.copy(P(d.u, d.v, .8 + q * 2.5 * (.5 + (i % 3) * .3))).add(new THREE.Vector3(Math.cos(a), 0, Math.sin(a)).multiplyScalar(q * 4.5));
      s.scale.setScalar(2 + q * 4); s.material.opacity = .55 * (1 - q);
    });
  });
}

function objetivo(d, img) {
  const g = new THREE.Group(); g.position.copy(P(d.u, d.v)); scene.add(g);
  const col = hex(d.color || 'morado');
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: brillo(col), transparent: true, depthWrite: false,
    blending: THREE.AdditiveBlending, opacity: .55 }));
  halo.scale.setScalar(11); halo.position.y = 6.2; g.add(halo);
  const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: medallon(img, col, 384), transparent: true }));
  sp.scale.setScalar(5.4); sp.position.y = 6.4; g.add(sp);
  const anillo = new THREE.Mesh(new THREE.RingGeometry(R(d.r || .03) * .85, R(d.r || .03), 64),
    new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: .7, side: THREE.DoubleSide, depthWrite: false }));
  anillo.rotation.x = -Math.PI / 2; anillo.position.y = .35; g.add(anillo);
  const poste = new THREE.Mesh(new THREE.CylinderGeometry(.12, .12, 3.6), new THREE.MeshStandardMaterial({ color: 0xdddddd }));
  poste.position.y = 1.9; g.add(poste);
  const obj = { d, g, sp };
  dinamicos.push(t => {
    sp.position.y = 6.4 + Math.sin(t * 2.2) * .25;
    const m = d.muere != null ? clamp((t - d.muere) / .8) : 0;
    sp.scale.setScalar(5.4 * (1 + .6 * m)); sp.material.opacity = 1 - m;
    halo.material.opacity = (.45 + .15 * Math.sin(t * 3)) * (1 - m) + (m > 0 && m < 1 ? .8 * (1 - m) : 0);
    if (m > 0 && d.gana) halo.material.color.set(hex(d.gana));
    anillo.material.opacity = .7 * (1 - m);
  });
  return obj;
}

// ------------------------------------------------------------------ fichas de campeón
class Ficha {
  constructor(id, d, img) {
    this.id = id; this.d = d; const col = new THREE.Color(hex(EQUIPO_COLOR[d.equipo] || d.color || 'blanco'));
    this.g = new THREE.Group(); scene.add(this.g);
    const disco = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.2, .35, 36),
      new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: .45, roughness: .35 }));
    disco.position.y = .18; disco.castShadow = true;
    this.aro = new THREE.Mesh(new THREE.RingGeometry(1.35, 1.75, 40), new THREE.MeshBasicMaterial({
      color: col, transparent: true, opacity: .6, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
    this.aro.rotation.x = -Math.PI / 2; this.aro.position.y = .12;
    this.foco = new THREE.Mesh(new THREE.RingGeometry(2.2, 2.6, 48), new THREE.MeshBasicMaterial({
      color: new THREE.Color(hex('amarillo')), transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false }));
    this.foco.rotation.x = -Math.PI / 2; this.foco.position.y = .16;
    const poste = new THREE.Mesh(new THREE.CylinderGeometry(.08, .08, 2.8), new THREE.MeshStandardMaterial({ color: 0xe8edf3 }));
    poste.position.y = 1.6; poste.castShadow = true;
    this.sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: medallon(img, col.getStyle()), transparent: true }));
    this.sp.scale.setScalar(2.9); this.sp.position.y = 4.2;
    disco.material.transparent = poste.material.transparent = true;
    this.disco = disco; this.poste = poste;
    this.g.add(disco, this.aro, this.foco, poste, this.sp);
    this.rastro = null; this.u = .5; this.v = .5;
  }
  donde(g) { return posicion(this.d.puntos, g); }
  actualizar(t, g) {
    const [u, v] = this.donde(g); this.u = u; this.v = v;
    this.g.position.copy(P(u, v));
    // entra levantándose y sale hundiéndose (en la «mesa» el último cuadro vuelve a ser el del video, sin fichas)
    const kin = this.d.de != null ? suave((t - this.d.de) / .5) : 1, kout = this.d.sale != null ? 1 - suave((t - this.d.sale) / .45) : 1;
    const ke = Math.min(kin, kout);
    this.g.visible = ke > .01; this.g.position.y -= (1 - ke) * 6; this.ke = ke;
    // foco (resaltar a un jugador)
    let f = 0;
    for (const e of E.focos || []) if (e.quien === this.id) f = Math.max(f, clamp((t - e.de) / .3) * (1 - clamp((t - e.a) / .3)));
    this.foco.material.opacity = f * (.65 + .35 * Math.sin(t * 9));
    this.foco.scale.setScalar(1 + .15 * Math.sin(t * 6));
    this.sp.scale.setScalar(2.9 * (1 + .4 * f));
    this.aro.scale.setScalar(1 + .12 * Math.sin(t * 4 + this.u * 20));
    // niebla: el equipo que no se ve queda como fantasma
    const n = nieblaActiva(t);
    const fantasma = n && n.oculta === this.d.equipo ? n.k : 0;
    this.sp.material.opacity = (1 - .72 * fantasma) * ke;
    this.disco.material.opacity = this.poste.material.opacity = (1 - .7 * fantasma) * ke;
  }
}

function nieblaActiva(t) {
  for (const n of E.niebla || []) {
    if (t >= n.de && t <= n.a + .5) return { ...n, k: suave((t - n.de) / (n.dur || 1.2)) * (1 - suave((t - n.a) / .5)) };
  }
  return null;
}

// ------------------------------------------------------------------ rastros, flechas, anillos, TP, oleadas, proyectiles
function tubo(puntos, radio, mat, segs) {
  if (puntos.length < 2) return null;
  const curva = new THREE.CatmullRomCurve3(puntos, false, 'centripetal');
  return new THREE.Mesh(new THREE.TubeGeometry(curva, segs || Math.max(8, puntos.length * 3), radio, 7, false), mat);
}

function rastros(t, g) {
  for (const r of E.rastros || []) {
    const f = fichas[r.quien]; if (!f) continue;
    if (f.rastro) { scene.remove(f.rastro); f.rastro.geometry.dispose(); f.rastro = null; }
    if (t < r.de || t > r.a + .4) continue;
    const g0 = Math.max(juego(r.de), g - (r.ventana || 99)), n = 36, pts = [];
    for (let i = 0; i <= n; i++) {
      const gg = g0 + (g - g0) * i / n, [u, v] = f.donde(gg);
      const p = P(u, v, .35);
      if (pts.length && pts[pts.length - 1].distanceTo(p) > 9) pts.length = 0;   // salto (TP, regreso): corta el rastro
      if (!pts.length || pts[pts.length - 1].distanceTo(p) > .15) pts.push(p);
    }
    const op = .78 * (1 - clamp((t - r.a) / .4));
    if (!r._mat) r._mat = new THREE.MeshBasicMaterial({ color: new THREE.Color(hex(EQUIPO_COLOR[f.d.equipo] || r.color)),
      transparent: true, depthWrite: false });
    r._mat.opacity = op;
    const m = tubo(pts, .32, r._mat); if (m) { m.renderOrder = 3; scene.add(m); f.rastro = m; }
  }
}

function flechaCurva(d) {
  const base = d.pts.map(([u, v]) => P(u, v, .6));
  const c0 = new THREE.CatmullRomCurve3(base, false, 'centripetal');
  const N = 160, muestras = [];
  for (let i = 0; i <= N; i++) {
    const s = i / N, p = c0.getPointAt(s); p.y += Math.sin(Math.PI * s) * (d.alto ?? 2.2); muestras.push(p);
  }
  return muestras;
}

function crearFlecha(d) {
  const col = new THREE.Color(hex(d.color)), muestras = flechaCurva(d);
  const mat = new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: .8, transparent: true, roughness: .3,
    depthWrite: false });
  const punta = new THREE.Mesh(new THREE.ConeGeometry(1.0 * (d.grosor || 1), 2.4 * (d.grosor || 1), 16), mat);
  scene.add(punta);
  let cuerpo = null;
  d._ancla = muestras[muestras.length - 1];
  dinamicos.push(t => {
    if (cuerpo) { scene.remove(cuerpo); cuerpo.traverse(m => m.geometry && m.geometry.dispose()); cuerpo = null; }
    const k = suave((t - d.en) / (d.dur || .8));
    const fuera = d.sale != null ? clamp((t - d.sale) / .35) : 0;
    const vis = t >= d.en && fuera < 1;
    punta.visible = vis && k > .02; if (!vis) return;
    mat.opacity = (1 - fuera) * .95;
    const fin = Math.max(2, Math.round(k * (muestras.length - 1)));
    const pts = muestras.slice(0, fin + 1);
    if (d.guion) {
      const grupo = new THREE.Group(), largo = 9, hueco = 6;
      for (let i = 0; i < pts.length - 1; i += largo + hueco) {
        const seg = pts.slice(i, Math.min(i + largo + 1, pts.length));
        const m = tubo(seg, .34 * (d.grosor || 1), mat, 6); if (m) grupo.add(m);
      }
      cuerpo = grupo;
    } else cuerpo = tubo(pts, .36 * (d.grosor || 1), mat, pts.length);
    if (cuerpo) { cuerpo.renderOrder = 4; scene.add(cuerpo); }
    const a = pts[pts.length - 2], b = pts[pts.length - 1];
    const dir = b.clone().sub(a).normalize();
    punta.position.copy(b); punta.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    d._ancla = b;
  });
}

function crearAnillo(d) {
  const col = new THREE.Color(hex(d.color)), r = R(d.r || .03);
  const mat = new THREE.MeshBasicMaterial({ color: col, transparent: true, side: THREE.DoubleSide, depthWrite: false });
  const m = new THREE.Mesh(new THREE.RingGeometry(r * .84, r, 64), mat);
  const mat2 = mat.clone(); const eco = new THREE.Mesh(new THREE.RingGeometry(r * .94, r, 64), mat2);
  for (const x of [m, eco]) { x.rotation.x = -Math.PI / 2; x.renderOrder = 5; scene.add(x); }
  const p = P(d.u, d.v, .5); m.position.copy(p); eco.position.copy(p);
  dinamicos.push(t => {
    const k = suave((t - d.en) / .35), fuera = d.sale != null ? clamp((t - d.sale) / .35) : 0;
    const vis = t >= d.en && fuera < 1; m.visible = eco.visible = vis; if (!vis) return;
    m.scale.setScalar(.4 + .6 * k); mat.opacity = .95 * (1 - fuera);
    const q = ((t - d.en) % 1.3) / 1.3; eco.scale.setScalar(1 + q * .7); mat2.opacity = .7 * (1 - q) * (1 - fuera) * k;
  });
}

function crearTP(d) {
  const col = new THREE.Color(hex(d.color));
  const haz = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.6, 16, 24, 1, true), new THREE.MeshBasicMaterial({
    color: col, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false }));
  const dest = P(d.a[0], d.a[1]); haz.position.copy(dest); haz.position.y += 8; scene.add(haz);
  const rem = new THREE.Mesh(new THREE.RingGeometry(1.6, 2.6, 6), new THREE.MeshBasicMaterial({ color: col, transparent: true,
    side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
  rem.rotation.x = -Math.PI / 2; rem.position.copy(dest); rem.position.y += .5; scene.add(rem);
  const arco = { pts: [d.desde, [(d.desde[0] + d.a[0]) / 2, (d.desde[1] + d.a[1]) / 2], d.a], color: d.color, en: d.en,
                 dur: (d.llega - d.en) * .6, sale: d.llega + .8, guion: true, alto: d.alto ?? 9, grosor: .7 };
  crearFlecha(arco);
  dinamicos.push(t => {
    const k = clamp((t - d.en) / (d.llega - d.en)), post = clamp((t - d.llega) / .8);
    const vis = t >= d.en && post < 1; haz.visible = rem.visible = vis; if (!vis) return;
    haz.material.opacity = (t < d.llega ? .25 + .35 * k + .1 * Math.sin(t * 20) : .9 * (1 - post));
    haz.scale.set(1 + post * 1.5, .3 + .7 * k, 1 + post * 1.5);
    rem.rotation.z = t * 4; rem.material.opacity = .8 * (1 - post); rem.scale.setScalar(1 + .3 * Math.sin(t * 8));
  });
}

function crearOleada(d) {
  const col = new THREE.Color(hex(d.color)), n = d.n || 6;
  const mat = new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: .7, roughness: .4 });
  const ms = [];
  for (let i = 0; i < n; i++) { const m = new THREE.Mesh(new THREE.SphereGeometry(.42, 10, 8), mat); m.castShadow = true; scene.add(m); ms.push(m); }
  const ruta = d.ruta.map(([u, v]) => new THREE.Vector2(u, v));
  const largos = [0]; for (let i = 1; i < ruta.length; i++) largos.push(largos[i - 1] + ruta[i].distanceTo(ruta[i - 1]));
  const total = largos[largos.length - 1];
  const en = s => { s = clamp(s) * total; let i = 1; while (i < largos.length - 1 && s > largos[i]) i++;
    const q = (s - largos[i - 1]) / (largos[i] - largos[i - 1] || 1); return ruta[i - 1].clone().lerp(ruta[i], q); };
  dinamicos.push(t => {
    const vis = t >= d.de && (d.sale == null || t < d.sale);
    ms.forEach((m, i) => {
      m.visible = vis; if (!vis) return;
      const k = clamp((t - d.de) / (d.a - d.de)) - i * .035;
      const p = en(k), lado = ((i % 2) ? 1 : -1) * .006;
      m.position.copy(P(p.x + lado, p.y - lado, .45 + (k >= 1 - i * .035 ? Math.abs(Math.sin(t * 9 + i)) * .5 : Math.abs(Math.sin(t * 7 + i)) * .18)));
    });
  });
}

function crearProyectil(d) {
  const col = hex(d.color);
  const bola = new THREE.Sprite(new THREE.SpriteMaterial({ map: brillo(col), transparent: true, blending: THREE.AdditiveBlending,
    depthWrite: false })); bola.scale.setScalar(4.5); scene.add(bola);
  const mat = new THREE.MeshBasicMaterial({ color: new THREE.Color(col), transparent: true, blending: THREE.AdditiveBlending,
    depthWrite: false });
  let estela = null;
  const camino = s => {
    const a = d.desde, b = d.a;
    const u = a[0] + (b[0] - a[0]) * s, v = a[1] + (b[1] - a[1]) * s;
    const p = P(u, v, 3.2 + Math.sin(Math.PI * s) * (d.alto ?? 3)); return p;
  };
  dinamicos.push(t => {
    if (estela) { scene.remove(estela); estela.geometry.dispose(); estela = null; }
    const k = clamp((t - d.de) / (d.llega - d.de)), post = clamp((t - d.llega) / .5);
    const vis = t >= d.de && post < 1; bola.visible = vis; if (!vis) return;
    bola.position.copy(camino(k)); bola.scale.setScalar(4.5 * (1 + 2 * post)); bola.material.opacity = 1 - post;
    const pts = []; for (let i = 0; i <= 20; i++) pts.push(camino(Math.max(0, k - .35 + .35 * i / 20)));
    mat.opacity = .75 * (1 - post);
    estela = tubo(pts, .45, mat, 30); if (estela) scene.add(estela);
  });
}

// columna de luz sobre un jugador o un punto (sobre todo en modo video: marca a alguien en el cuadro real)
function crearPilar(d) {
  const col = new THREE.Color(hex(d.color)), alto = d.alto ?? 9, r = R(d.r ?? .018);
  const haz = new THREE.Mesh(new THREE.CylinderGeometry(r * .55, r, alto, 28, 1, true), new THREE.MeshBasicMaterial({
    color: col, transparent: true, opacity: 0, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false }));
  const base = new THREE.Mesh(new THREE.CircleGeometry(r * 1.25, 40), new THREE.MeshBasicMaterial({ color: col, transparent: true,
    opacity: 0, blending: THREE.AdditiveBlending, depthWrite: false }));
  base.rotation.x = -Math.PI / 2;
  const p = P(d.u, d.v); haz.position.copy(p); haz.position.y += alto / 2; base.position.copy(p); base.position.y += .05;
  scene.add(haz, base);
  dinamicos.push(t => {
    const k = suave((t - d.en) / .35), fuera = d.sale != null ? clamp((t - d.sale) / .35) : 0;
    const vis = t >= d.en && fuera < 1; haz.visible = base.visible = vis; if (!vis) return;
    haz.scale.set(1, k, 1); haz.position.y = p.y + alto * k / 2;
    haz.material.opacity = (.32 + .08 * Math.sin(t * 6)) * (1 - fuera);
    base.material.opacity = (.45 + .15 * Math.sin(t * 6)) * (1 - fuera) * k;
  });
}

// zona: polígono en el suelo con borde levantado (muro de luz bajo)
function crearZona(d) {
  const col = new THREE.Color(hex(d.color)), pts = d.pts.map(([u, v]) => P(u, v, .06));
  const forma = new THREE.Shape(pts.map(p => new THREE.Vector2(p.x, -p.z)));
  const piso = new THREE.Mesh(new THREE.ShapeGeometry(forma), new THREE.MeshBasicMaterial({ color: col, transparent: true,
    opacity: 0, depthWrite: false, side: THREE.DoubleSide }));
  piso.rotation.x = -Math.PI / 2; piso.position.y = pts[0].y; scene.add(piso);
  const cerr = [...pts, pts[0]], alto = d.alto ?? 1.6, pos = [];
  for (let i = 0; i < cerr.length - 1; i++) {
    const a = cerr[i], b = cerr[i + 1];
    pos.push(a.x, a.y, a.z, b.x, b.y, b.z, b.x, b.y + alto, b.z, a.x, a.y, a.z, b.x, b.y + alto, b.z, a.x, a.y + alto, a.z);
  }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  const muro = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, side: THREE.DoubleSide,
    blending: THREE.AdditiveBlending, depthWrite: false }));
  scene.add(muro);
  dinamicos.push(t => {
    const k = suave((t - d.en) / .4), fuera = d.sale != null ? clamp((t - d.sale) / .35) : 0;
    const vis = t >= d.en && fuera < 1; piso.visible = muro.visible = vis; if (!vis) return;
    piso.material.opacity = (d.alfa ?? .2) * k * (1 - fuera); muro.material.opacity = .28 * k * (1 - fuera);
    muro.scale.y = 1;
  });
}

// ------------------------------------------------------------------ capa 2D (rótulos de transmisión)
function pildora(x, y, texto, sub, color, tam = 34, alinear = 'izq', alfa = 1) {
  ctx.save(); ctx.globalAlpha = alfa;
  ctx.font = `${tam}px PopBlack`; const w1 = ctx.measureText(texto).width;
  let w2 = 0; const ts = Math.round(tam * .6);
  if (sub) { ctx.font = `${ts}px PopSemi`; w2 = ctx.measureText(sub).width; }
  const pad = tam * .48, barra = tam * .2, w = Math.max(w1, w2) + pad * 2 + barra, h = sub ? tam * 2.0 : tam * 1.42;
  const x0 = alinear === 'centro' ? x - w / 2 : alinear === 'der' ? x - w : x;
  ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 4;
  ctx.fillStyle = 'rgba(9,13,21,.88)'; ctx.beginPath(); ctx.roundRect(x0, y, w, h, tam * .26); ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.fillStyle = hex(color); ctx.beginPath(); ctx.roundRect(x0, y, barra + 4, h, [tam * .26, 0, 0, tam * .26]); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = `${tam}px PopBlack`; ctx.textBaseline = 'alphabetic';
  ctx.fillText(texto, x0 + barra + pad, y + tam * 1.06);
  if (sub) { ctx.fillStyle = hex(color); ctx.font = `${ts}px PopSemi`; ctx.fillText(sub, x0 + barra + pad, y + tam * 1.72); }
  ctx.restore();
  return { x0, y, w, h };
}

function pantalla(v3) {
  const p = v3.clone().project(camera);
  return [(p.x + 1) / 2 * W, (1 - p.y) / 2 * H, p.z < 1];
}

const imgs = {};
function capa2d(t, g) {
  ctx.clearRect(0, 0, W, H);
  // viñeta
  if (!VIDEO) {
    const vg = ctx.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * .95);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.55)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  }
  // oscurecer el cuadro real (foco de la pausa)
  for (const o of E.oscurecer || []) {
    if (t < o.de || t > o.a + .3) continue;
    ctx.fillStyle = `rgba(0,0,0,${(o.k ?? .4) * suave((t - o.de) / .3) * (1 - suave((t - o.a) / .3))})`; ctx.fillRect(0, 0, W, H);
  }

  // nombres bajo las fichas
  if (E.nombres !== false) {
    for (const f of Object.values(fichas)) {
      if (!f.g.visible) continue;
      const [x, y, ok] = pantalla(f.g.position.clone().add(new THREE.Vector3(0, 2.2, 0))); if (!ok) continue;
      const n = nieblaActiva(t), a = n && n.oculta === f.d.equipo ? 1 - .75 * n.k : 1;
      ctx.save(); ctx.globalAlpha = a; ctx.font = '22px PopXB'; ctx.textAlign = 'center';
      ctx.lineWidth = 6; ctx.strokeStyle = 'rgba(0,0,0,.85)'; ctx.strokeText(f.d.jugador || f.id, x, y + 30);
      ctx.fillStyle = hex(EQUIPO_COLOR[f.d.equipo] || 'blanco'); ctx.fillText(f.d.jugador || f.id, x, y + 30); ctx.restore();
    }
  }

  // barras de vida de los objetivos
  for (const o of E._objetivos || []) {
    const d = o.d; if (!d.vida) continue;
    const muerto = d.muere != null && t >= d.muere;
    const hp = lineal(d.vida, t), max = d.vida_max || d.vida[0][1];
    if (t < d.vida[0][0] - .3 || (muerto && t > d.muere + .6)) continue;
    const [x, y, ok] = pantalla(o.sp.getWorldPosition(new THREE.Vector3()).add(new THREE.Vector3(0, 4.4, 0))); if (!ok) continue;
    const w = 230, h = 22, x0 = x - w / 2, y0 = y - 30;
    ctx.fillStyle = 'rgba(8,10,16,.9)'; ctx.beginPath(); ctx.roundRect(x0 - 4, y0 - 4, w + 8, h + 8, 8); ctx.fill();
    ctx.fillStyle = '#5a1f2a'; ctx.fillRect(x0, y0, w, h);
    ctx.fillStyle = hex(d.color_vida || 'rojo'); ctx.fillRect(x0, y0, w * clamp(hp / max), h);
    if (d.vida_numeros !== false && t >= (d.numeros_desde ?? -1e9)) {
      ctx.font = '24px PopXB'; ctx.textAlign = 'center'; ctx.lineWidth = 5; ctx.strokeStyle = '#000';
      const s = Math.round(hp).toLocaleString('es-MX'); ctx.strokeText(s, x, y0 - 10); ctx.fillStyle = '#fff'; ctx.fillText(s, x, y0 - 10);
    }
    ctx.textAlign = 'start';
  }

  // rótulos anclados a puntos del mapa o a jugadores
  for (const e of E.etiquetas || []) {
    if (t < e.de || t > e.a + .3) continue;
    const k = suave((t - e.de) / .25) * (1 - suave((t - e.a) / .3));
    let ancla;
    if (e.quien && fichas[e.quien]) ancla = fichas[e.quien].g.position.clone().add(new THREE.Vector3(0, e.alto ?? 6.6, 0));
    else if (e.flecha && E._flechas[e.flecha]) ancla = E._flechas[e.flecha]._ancla.clone();
    else ancla = P(e.u, e.v, e.alto ?? 1);
    const [x, y, ok] = pantalla(ancla); if (!ok) continue;
    const dx = e.dx ?? 0, dy = e.dy ?? -70;
    ctx.save(); ctx.globalAlpha = k; ctx.strokeStyle = hex(e.color); ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + dx, y + dy); ctx.stroke();
    ctx.fillStyle = hex(e.color); ctx.beginPath(); ctx.arc(x, y, 6, 0, 7); ctx.fill(); ctx.restore();
    const tam = e.tam || 30, alin = e.alinear || (dx < -10 ? 'der' : dx > 10 ? 'izq' : 'centro');
    const hp = (e.sub ? tam * 2 : tam * 1.42);
    const r = pildora(x + dx, y + dy - (dy < 0 ? hp : 0), e.texto, e.sub, e.color, tam, alin, k);
    const im = e.icono && imgs['ico_' + e.icono];
    if (im) {   // retrato redondo pegado al rótulo
      const rad = r.h * .62, cx = r.x0 - rad - 6, cy = r.y + r.h / 2;
      ctx.save(); ctx.globalAlpha = k; ctx.beginPath(); ctx.arc(cx, cy, rad, 0, 7); ctx.fillStyle = '#0b0f17'; ctx.fill(); ctx.clip();
      const z = rad * 2 / (Math.min(im.width, im.height) * .86);
      ctx.drawImage(im, cx - im.width * z / 2, cy - im.height * z / 2, im.width * z, im.height * z); ctx.restore();
      ctx.save(); ctx.globalAlpha = k; ctx.lineWidth = 5; ctx.strokeStyle = hex(e.color); ctx.beginPath(); ctx.arc(cx, cy, rad, 0, 7);
      ctx.stroke(); ctx.restore();
    }
  }

  // marcador de reloj (arriba al centro): logo · reloj · logo
  const yR = 34, ka = VIDEO ? 0 : suave((t - E.de) / .4);
  ctx.save(); ctx.globalAlpha = ka;
  ctx.fillStyle = 'rgba(9,13,21,.9)'; ctx.beginPath(); ctx.roundRect(W / 2 - 250, yR, 500, 84, 16); ctx.fill();
  ctx.fillStyle = hex(EQUIPO_COLOR[E.equipos?.[0]?.id] || 'azul'); ctx.fillRect(W / 2 - 250, yR + 78, 250, 6);
  ctx.fillStyle = hex(EQUIPO_COLOR[E.equipos?.[1]?.id] || 'rojo'); ctx.fillRect(W / 2, yR + 78, 250, 6);
  (E.equipos || []).forEach((q, i) => {
    const im = imgs['logo_' + q.id]; if (!im) return;
    const s = 60 / Math.max(im.width, im.height);
    ctx.drawImage(im, i ? W / 2 + 175 - im.width * s / 2 : W / 2 - 175 - im.width * s / 2, yR + 12 + (60 - im.height * s) / 2,
                  im.width * s, im.height * s);
  });
  ctx.font = '48px PopBlack'; ctx.textAlign = 'center'; ctx.fillStyle = '#fff'; ctx.fillText(reloj(g), W / 2, yR + 60);
  ctx.font = '17px PopSemi'; ctx.fillStyle = hex('amarillo'); ctx.fillText(E.titulo || 'MAPA TÁCTICO 3D', W / 2, yR + 112 + 6);
  ctx.restore(); ctx.textAlign = 'start';

  // datos del marcador (columna izquierda, como el tablero 2D)
  let yh = 150;
  for (const c of E.hud || []) {
    if (t < c.de || t > c.a + .3) continue;
    const k = suave((t - c.de) / .3) * (1 - suave((t - c.a) / .3));
    const r = pildora(60 - (1 - k) * 40, yh, c.texto, c.sub, c.color, c.tam || 34, 'izq', k); yh += r.h + 14;
  }

  // carteles grandes (PAUSA, salto de tiempo…)
  for (const c of E.carteles || []) {
    if (t < c.de || t > c.a + .3) continue;
    const k = suave((t - c.de) / .25) * (1 - suave((t - c.a) / .3));
    pildora(W / 2, c.y ?? 160, c.texto, c.sub, c.color, c.tam || 54, 'centro', k);
  }

  // destellos (salto de tiempo, impacto)
  for (const d of E.destellos || []) {
    const q = (t - d) / .45; if (q < 0 || q > 1) continue;
    ctx.fillStyle = `rgba(255,255,255,${.85 * (1 - q) * Math.min(1, q * 6)})`; ctx.fillRect(0, 0, W, H);
  }

  // fundido de entrada
  const fi = VIDEO ? 0 : 1 - clamp((t - E.de) / (E.fundido ?? .35));
  if (fi > 0) { ctx.fillStyle = `rgba(0,0,0,${fi})`; ctx.fillRect(0, 0, W, H); }
}

// ------------------------------------------------------------------ cámara
function camaraEn(t) {
  const K = E.camara; let i = 0;
  if (t <= K[0][0]) i = 0; else if (t >= K[K.length - 1][0]) i = K.length - 2;
  else while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const a = K[Math.max(i - 1, 0)], b = K[i], c = K[Math.min(i + 1, K.length - 1)], d = K[Math.min(i + 2, K.length - 1)];
  const q = c[0] > b[0] ? clamp((t - b[0]) / (c[0] - b[0])) : 0;   // Catmull-Rom: velocidad continua entre llaves
  const val = j => catmull(a[j], b[j], c[j], d[j], q);
  const u = val(1), v = val(2), dist = val(3), pitch = val(4) * Math.PI / 180, yaw = val(5) * Math.PI / 180;
  const obj = new THREE.Vector3((u - .5) * MAPA, 0, (v - .5) * MAPA);
  camera.position.set(obj.x + dist * Math.cos(pitch) * Math.sin(yaw), dist * Math.sin(pitch),
                      obj.z + dist * Math.cos(pitch) * Math.cos(yaw));
  camera.lookAt(obj); camera.fov = val(6) || 38; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
}

const G_PITCH = Math.atan2(52, 35) * 180 / Math.PI, G_DIST = Math.hypot(52, 35);   // pose de la cámara del juego
function camaraMesa(t) {
  const K = (E.camara && E.camara.length) ? E.camara : [[E.de, 0, G_PITCH, G_DIST, .5, .5]];
  let i = 0;
  if (t >= K[K.length - 1][0]) i = Math.max(K.length - 2, 0); else while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const a = K[Math.max(i - 1, 0)], b = K[i], c = K[Math.min(i + 1, K.length - 1)], d = K[Math.min(i + 2, K.length - 1)];
  const q = c[0] > b[0] ? suave(clamp((t - b[0]) / (c[0] - b[0]))) : 0;
  const val = j => catmull(a[j], b[j], c[j], d[j], q);
  const yaw = val(1) * Math.PI / 180, pitch = val(2) * Math.PI / 180, dist = val(3);
  const obj = sobreVideo(val(4), val(5));
  camera.position.set(obj.x + dist * Math.cos(pitch) * Math.sin(yaw), dist * Math.sin(pitch), obj.z + dist * Math.cos(pitch) * Math.cos(yaw));
  camera.lookAt(obj); camera.fov = 40; camera.updateProjectionMatrix(); camera.updateMatrixWorld();
}

// el cuadro del VOD proyectado sobre el suelo (sin el marcador de arriba ni el HUD de abajo, con borde difuminado)
async function mesa() {
  const im = await cargar(E.fondo);
  const tex = new THREE.Texture(im); tex.colorSpace = THREE.SRGBColorSpace; tex.needsUpdate = true;
  const mc = document.createElement('canvas'); mc.width = 512; mc.height = 288; const m = mc.getContext('2d');
  const [y0, y1] = E.mesa_y || [.1, .77];
  m.fillStyle = '#000'; m.fillRect(0, 0, 512, 288);
  m.filter = 'blur(10px)'; m.fillStyle = '#fff'; m.fillRect(14, y0 * 288 + 8, 484, (y1 - y0) * 288 - 16); m.filter = 'none';
  const mascara = new THREE.CanvasTexture(mc);
  const geo = new THREE.PlaneGeometry(260, 260, 160, 160); geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position, uv = geo.attributes.uv, v = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) {
    v.set(pos.getX(i), 0, pos.getZ(i)).project(camG);
    uv.setXY(i, (v.x + 1) / 2, (v.y + 1) / 2);
  }
  uv.needsUpdate = true;
  tex.wrapS = tex.wrapT = mascara.wrapS = mascara.wrapT = THREE.ClampToEdgeWrapping;
  const suelo = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: tex, alphaMap: mascara, transparent: true, depthWrite: false,
    toneMapped: false, fog: false }));
  fondoIm = im;
  suelo.renderOrder = -1; scene.add(suelo);
  // rejilla táctica tenue sobre el suelo para que se lea la profundidad
  const rej = new THREE.GridHelper(160, 32, 0x46a5ff, 0x46a5ff); rej.material.transparent = true; rej.material.opacity = .08;
  rej.position.y = .03; scene.add(rej);
  E._rejilla = rej;
}

// ------------------------------------------------------------------ cuadro
function dibujar(t) {
  const g = E.reloj ? juego(t) : t;
  if (MESA) camaraMesa(t); else if (!VIDEO) camaraEn(t);
  for (const f of Object.values(fichas)) f.actualizar(t, g);
  dinamicos.forEach(fn => fn(t, g));
  rastros(t, g);
  // niebla de guerra
  const n = VIDEO ? null : nieblaActiva(t), nk = n ? n.k * (n.fuerza ?? .8) : 0;
  if (VIDEO) { capa2d(t, g); return; }
  nieblaU.nieblaK.value = nk;
  arbolesMat.color.setScalar(1 - .6 * nk);
  aguaMat.color.set(0x2aa6c9).multiplyScalar(1 - .7 * nk); aguaMat.emissiveIntensity = .5 * (1 - nk);
  if (n) {
    const c = nieblaCtx; c.clearRect(0, 0, 512, 512);
    c.fillStyle = '#fff'; c.fillRect(0, 0, 512, 512);
    const agujero = (u, v, r) => {
      const gr = c.createRadialGradient(u * 512, v * 512, 0, u * 512, v * 512, r * 512);
      gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(.65, 'rgba(0,0,0,.9)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
      c.fillStyle = gr; c.beginPath(); c.arc(u * 512, v * 512, r * 512, 0, 7); c.fill();
    };
    for (const f of Object.values(fichas)) if (f.d.equipo === n.ve && f.g.visible) agujero(f.u, f.v, n.radio || .07);
    for (const [u, v, r] of n.extra || []) agujero(u, v, r);
    nieblaTex.needsUpdate = true;
  }
  capa2d(t, g);
}

let fondoIm = null;   // ?fondo=1: el cuadro del VOD debajo (solo para revisar el modo video)
window.cuadro = t => {
  dibujar(t); renderer.render(scene, camera);
  octx.clearRect(0, 0, W, H);
  if (fondoIm && !MESA) octx.drawImage(fondoIm, 0, 0, W, H);
  octx.drawImage(renderer.domElement, 0, 0);
  if (MESA) {   // al empezar y al terminar, el cuadro real entero encima: el corte con el VOD no se ve
    const k = 1 - Math.min(suave((t - E.de - .1) / .5), 1 - suave((t - (E.a - .75)) / .5));
    if (k > 0) { octx.globalAlpha = k; octx.drawImage(fondoIm, 0, 0, W, H); octx.globalAlpha = 1; }
  }
  octx.drawImage(capa, 0, 0);
  return Q.get('png') ? salida.toDataURL('image/png') : salida.toDataURL('image/jpeg', +(Q.get('calidad') || .93));
};

// ------------------------------------------------------------------ arranque
async function iniciar() {
  E = await (await fetch(Q.get('escena'))).json();
  for (const q of E.equipos || []) EQUIPO_COLOR[q.id] = q.color;
  MESA = E.modo === 'mesa'; VIDEO = E.modo === 'video' || MESA;
  renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true, alpha: VIDEO && !MESA });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.08; renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  scene = new THREE.Scene();
  if (VIDEO && !MESA) renderer.setClearColor(0x000000, 0);
  else { scene.background = new THREE.Color(0x070b14); scene.fog = new THREE.Fog(0x070b14, MESA ? 120 : 140, MESA ? 260 : 300); }
  camera = new THREE.PerspectiveCamera(38, W / H, .5, 800);
  if (VIDEO) {   // cámara fija inclinada ~56°, como la del juego (la «mesa» la usa para proyectar; renderiza con otra)
    camG = new THREE.PerspectiveCamera(40, W / H, .5, 800);
    camG.position.set(0, 52, 35); camG.lookAt(0, 0, 0); camG.updateProjectionMatrix(); camG.updateMatrixWorld();
    if (!MESA) camera = camG;
  }
  scene.add(new THREE.HemisphereLight(0xcfe3ff, 0x2a2417, 1.05));
  const sol = new THREE.DirectionalLight(0xfff0d8, 2.4); sol.position.set(-45, 80, 35); sol.castShadow = true;
  sol.shadow.mapSize.set(4096, 4096); const sc = sol.shadow.camera; sc.left = sc.bottom = -62; sc.right = sc.top = 62;
  sc.near = 10; sc.far = 220; sol.shadow.bias = -.0006; sol.shadow.normalBias = .04; scene.add(sol);

  await Promise.all([document.fonts.load('40px PopBlack'), document.fonts.load('40px PopXB'), document.fonts.load('40px PopSemi')]);
  if (VIDEO) {   // suelo invisible que solo recibe sombras
    const sombra = new THREE.Mesh(new THREE.PlaneGeometry(600, 600), new THREE.ShadowMaterial({ opacity: .42 }));
    sombra.rotation.x = -Math.PI / 2; sombra.receiveShadow = true; scene.add(sombra);
    if (MESA) await mesa();
    else if (Q.get('fondo') && E.fondo) fondoIm = await cargar(E.fondo);
  } else await terreno();
  for (const e of E.etiquetas || []) if (e.icono && !imgs['ico_' + e.icono]) imgs['ico_' + e.icono] = await cargar(e.icono);
  for (const q of E.equipos || []) if (q.logo) imgs['logo_' + q.id] = await cargar(q.logo);
  for (const s of E.estructuras || []) estructura(s);
  E._objetivos = [];
  for (const o of E.objetivos || []) E._objetivos.push(objetivo(o, o.img ? await cargar(o.img) : null));
  for (const [id, d] of Object.entries(E.fichas || {})) fichas[id] = new Ficha(id, d, d.icono ? await cargar(d.icono) : null);
  E._flechas = {};
  for (const f of E.flechas || []) { crearFlecha(f); if (f.id) E._flechas[f.id] = f; }
  for (const a of E.anillos || []) crearAnillo(a);
  for (const p of E.tps || []) crearTP(p);
  for (const o of E.oleadas || []) crearOleada(o);
  for (const p of E.proyectiles || []) crearProyectil(p);
  for (const p of E.pilares || []) crearPilar(p);
  for (const z of E.zonas || []) crearZona(z);

  salida = document.createElement('canvas'); salida.id = 'salida'; salida.width = W; salida.height = H;
  octx = salida.getContext('2d'); document.body.appendChild(salida);
  capa = document.createElement('canvas'); capa.width = W; capa.height = H; ctx = capa.getContext('2d');
  window.LISTO = true;

  if (Q.get('vivo')) {
    const t0 = +(Q.get('t') || E.de), inicio = performance.now();
    const paso = () => {
      let t = t0 + (performance.now() - inicio) / 1000; if (t > E.a) t = E.de + ((t - E.de) % (E.a - E.de));
      dibujar(t); renderer.render(scene, camera); octx.drawImage(renderer.domElement, 0, 0); octx.drawImage(capa, 0, 0);
      requestAnimationFrame(paso);
    };
    paso();
  } else if (Q.get('t')) window.cuadro(+Q.get('t'));
}
iniciar().catch(e => { console.error(e); window.ERROR = String(e); });
