

# ---------------------------------------------------------------- TEORÍAS (100 - 112.5): tablero de evidencias
Te = "teorias"
KEYS = [(100.0, 1.0, C0[0], C0[1] - 40, 0.0), (101.5, 1.35, C0[0] - 480, C0[1] + 20, -1.0), (103.2, 1.3, C0[0], C0[1] + 90, 0.8),
        (105.4, 1.0, C0[0], C0[1] - 40, 0.0), (106.4, 1.35, C0[0] + 480, C0[1] + 10, 1.0), (108.6, 1.0, C0[0], C0[1] - 40, 0.0)]


def _cam_keys(t):
    """Cámara por claves: mantiene y se mueve con suavidad (0,9 s) entre encuadres."""
    for i in range(len(KEYS) - 1, -1, -1):
        if t >= KEYS[i][0]:
            k = KEYS[i]
            prev = KEYS[i - 1] if i > 0 else k
            u = e_inout(clamp01((t - k[0]) / 0.9))
            z, cx, cy, rot = [lerp(prev[j], k[j], u) for j in (1, 2, 3, 4)]
            z += 0.015 * (t - k[0]) / 2.0
            return D.camara(z, cx, cy, rot)
    return D.camara(1.0, KEYS[0][2], KEYS[0][3], 0.0)


def _tablero(lz, t):
    cam = _cam_keys(t)
    D.pegar(lz, corcho(), cam @ D.poner(3400, 2000, C0[0], C0[1]))
    cx, cy = C0
    ANC = 360
    ALT2 = 0.5 * ANC * (0.055 + 0.89 * 1.15 + 0.17)
    ti = (w_(Te, 0, 5) - 0.15, w_(Te, 0, 8) - 0.15, w_(Te, 1, 6) - 0.15)
    tarjetas = (("alberti", -520, 20, -5, ti[0], "Disco de cifrado"), ("f190", 0, 90, 3, ti[1], None), ("f110", 520, 10, -3, ti[2], "¿Fraude medieval?"))
    pins = []
    for k, (nom, dx, dy, r, t_in, ley) in enumerate(tarjetas):
        sp = pola(nom, ANC, 1.15, (0.5, 0.5) if nom != "f190" else (0.5, 0.35), ley)
        carta(lz, sp, cam, t, t_in, cx + dx, cy + dy, r, desde=(0, -420), fase=k * 1.3)
        if t > t_in + 0.25:
            pins.append((cx + dx, cy + dy - ALT2 + 22))
    if t > 100.1:
        q = spr("pregunta", lambda: D.Sprite(np.full((220, 360, 3), (240, 235, 220), np.uint8), None, sombra=True, sr=12))
        M = cam @ D.poner(q.w, q.h, cx, cy - 250, 1.0, 1.5)
        D.pegar(lz, q, M, smooth(prog(t, 100.1, 100.5)))
        pm, a_, m = D.palabra_img("¿Qué es?", "serif", 84, (0.72, 0.05, 0.05), stroke=0.02, glow=0.0)
        x, y = D.tf(M, q.w / 2, q.h / 2)
        D.mezclar_pm(lz, pm, a_, int(x - pm.shape[1] / 2), int(y - pm.shape[0] / 2), smooth(prog(t, 100.2, 100.6)))
    for k, p in enumerate(pins):
        D.hilo(lz, cam, (cx, cy - 350), p, smooth(prog(t, ti[k] + 0.2, ti[k] + 0.8)))
    if t > 100.1:
        D.pin(lz, cam, cx, cy - 350)
    for p in pins:
        D.pin(lz, cam, *p)
    for k, tt in enumerate((w_(Te, 2, 0), w_(Te, 2, 1), w_(Te, 2, 3))):
        dx, dy = tarjetas[k][1], tarjetas[k][2]
        x, y = D.tf(cam, cx + dx, cy + dy)
        z = float(np.sqrt(abs(np.linalg.det(cam[:2, :2]))))
        X.trazo_recto(lz, (x - ANC * 0.42 * z, y - ALT2 * 0.8 * z), (x + ANC * 0.42 * z, y + ALT2 * 0.8 * z), 0.0, e_out(prog(t, tt, tt + 0.4)), 22)
        X.trazo_recto(lz, (x + ANC * 0.42 * z, y - ALT2 * 0.8 * z), (x - ANC * 0.42 * z, y + ALT2 * 0.8 * z), 0.0, e_out(prog(t, tt + 0.15, tt + 0.55)), 22)
    D.estampa(lz, "SIN RESOLVER", W / 2, 640, t, w_(Te, 2, 6) + 0.1, 120, rot=-7)


shot(100.0, F_negro(),
     [R(pal_(Te, 0, 4, 6), W / 2, 1000, 66, sal=w_(Te, 0, 7) - 0.05), R(pal_(Te, 0, 7, 10), W / 2, 1000, 66, sal=w_(Te, 1, 5) - 0.05),
      R(pal_(Te, 1, 5, 10), W / 2, 1000, 66, sal=w_(Te, 2, 0) - 0.05), R(pal_(Te, 2, 0, 7), W / 2, 1000, 62, lineas=None)],
     [_tablero], ent=("tinta", 0.7))

# ---------------------------------------------------------------- CIERRE (112.5 - 131.25)
K = "cierre"
shot(112.50, F_clip("biblioteca", inicio=0.5, z0=1.0, z1=1.25, c0=(0.5, 0.5), c1=(0.5, 0.55), tono=(1.0, 0.9, 0.8), sat=0.7), [], ent=("tinta", 0.7))
shot(114.85, F_foto("beinecke_interior", z0=1.05, z1=1.24, c0=(0.5, 0.55), c1=(0.5, 0.42), par=(70, 14), tono=(0.95, 0.9, 0.85)), [],
     [lambda lz, t: D.tag_nombre(lz, "Biblioteca Beinecke", 470, 860, t, w_(K, 0, 6), 54)], ent=("fuga", 0.7))
shot(116.92, F_clip("paginas2", inicio=0.5, z0=1.05, z1=1.22, tono=(0.7, 0.62, 0.52)),
     [S(pal_(K, 0, 12, 15), 960, 880, 100, lineas=(1,))],
     [lambda lz, t: D.pegar(lz, X.sello_circular("Universidad", "YALE", "New Haven"), D.poner(420, 420, 1500, 430, 0.85, -10), 0.95 * smooth(prog(t, w_(K, 0, 14), w_(K, 0, 14) + 0.2))),
      lambda lz, t: carta(lz, X.estampilla("f003", "MS 408", 320), I3, t, 117.0, 380, 470, -6, desde=(-500, 0), dur=0.55)], ent=("fundido", 0.6))


def _internet(lz, t):
    tl = t - 119.15
    vent = spr("ventana", lambda: _ventana())
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.05, W / 2, H / 2 - 8, 0.0), 2.4, mano=0.5)(tl)
    D.pegar(lz, vent, cam @ D.poner(vent.w, vent.h, W / 2, 470, 1.0, 0.0), smooth(prog(t, 119.15, 119.5)))
    nomb = (4, 7, 10, 24, 32, 110, 111, 136, 141, 147, 175, 176)
    for k, n in enumerate(nomb):
        col, fila = k % 6, k // 6
        x = 405 + col * 222
        y = 385 + fila * 335 - 6 * math.sin(0.7 * t + k)
        sp = pola(f"f{n:03d}", 205, 1.36, (0.5, 0.45))
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, x, y, 1.0, (k % 3 - 1) * 1.5), smooth(prog(t, 119.4 + 0.07 * k, 119.8 + 0.07 * k)))


def _ventana():
    w, h = 1500, 760
    im = np.zeros((h, w, 3), np.uint8)
    im[:] = (26, 26, 28)
    cv2.rectangle(im, (0, 0), (w, 66), (44, 44, 48), -1)
    for k, c in enumerate(((70, 70, 220), (60, 190, 240), (80, 200, 90))):
        cv2.circle(im, (34 + k * 34, 33), 10, c[::-1], -1, cv2.LINE_AA)
    cv2.rectangle(im, (150, 14), (w - 60, 52), (20, 20, 22), -1)
    from PIL import Image, ImageDraw
    pil = Image.fromarray(im)
    ImageDraw.Draw(pil).text((176, 33), "collections.library.yale.edu", font=D.fuente("sans_l", 24), fill=(200, 200, 195), anchor="lm")
    return D.Sprite(np.asarray(pil), None, sombra=True, sr=26, off=(18, 26), sop=0.7)


shot(119.15, F_pozo(0.5, 0.5, 0.85, (0.17, 0.15, 0.13)), [], [_internet], ent=("tinta", 0.7))
shot(120.90, F_clip("proyector", inicio=4, z0=1.05, z1=1.25, c0=(0.5, 0.5), c1=(0.6, 0.5), tono=(0.7, 0.62, 0.55)),
     [R(pal_(K, 1, 5, 9), W / 2, 540, 92, lineas=(2,))], ent=("fundido", 0.6))
shot(122.85, F_foto("folios_hd/f003", z0=1.7, z1=2.1, c0=(0.4, 0.3), c1=(0.52, 0.5), par=(0, 0), lado=3800, tono=(0.72, 0.66, 0.56)),
     [R(pal_(K, 1, 9, 13), W / 2, 820, 92, lineas=(2,))], ent=("fuga", 0.7))
shot(125.38, F_foto("folios_hd/f190", z0=1.9, z1=2.3, c0=(0.25, 0.3), c1=(0.7, 0.6), par=(0, 0), lado=3800, tono=(0.5, 0.48, 0.45)),
     [Q([[(w, t) for w, t in pal_(K, 2, 0, 4)], [(w, t) for w, t in pal_(K, 2, 4, 8)]], w_(K, 2, 0) - 0.1, W / 2, 560, 84, sal=w_(K, 2, 8) - 0.1)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(127.12, F_clip("vela", inicio=6, z0=1.05, z1=1.3, tono=(1.0, 0.9, 0.8)),
     [Q([[(w, t) for w, t in pal_(K, 2, 8, 12)], [(w, t) for w, t in pal_(K, 2, 12, 15)]], w_(K, 2, 8) - 0.1, W / 2, 560, 84, sal=129.6)], ent=("fuga", 0.7))
FIN_VOZ = FIN("cierre")
shot(129.85, F_negro(),
     [S([("El", 130.1), ("Libro", 130.3), ("Que", 130.5), ("Nadie", 130.7), ("Puede", 130.9), ("Leer", 131.1)], 960, 470, 110, lineas=(3,)),
      R([("Escaneos", 130.9), ("del", 130.9), ("manuscrito:", 130.9), ("Beinecke", 130.9), ("Library,", 130.9), ("Yale", 130.9), ("(MS", 130.9), ("408)", 130.9)], 960, 700, 30, lineas=None),
      R([("Video:", 131.0), ("Pexels", 131.0), ("·", 131.0), ("Fotos:", 131.0), ("Wikimedia", 131.0), ("Commons", 131.0)], 960, 750, 30)], ent=("negro", 0.6))
_construir()


# ================================================================== Mundo
class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            self.sonidos()

    def sonidos(self):
        e = self.ev
        e(0.2, "latido", 0.7, dur=1.6)
        for t, n, v, kw in SND:
            e(t, n, v, **kw)
        e(w_("gancho", 2, 12) + 0.35, "sello", 0.8)
        e(w_("fecha", 0, 13), "ding", 0.35)
        e(w_("fecha", 2, 8) + 0.1, "garabato", 0.5, dur=0.4)
        for tt in (w_("teorias", 2, 0), w_("teorias", 2, 1), w_("teorias", 2, 3)):
            e(tt, "garabato", 0.5, dur=0.35)
        e(w_("teorias", 2, 6) + 0.1, "sello", 0.8)
        for tt in (8.7, 9.0, 43.9, 44.3, 92.4, 92.7):
            e(tt, "garabato", 0.4, dur=0.5)
        e(w_("cierre", 2, 8) - 0.05, "latido", 0.55, dur=1.2)
        e(130.1, "impacto", 0.6)

    def render(self, lz, t):
        i = 0
        for k, d in enumerate(SHOTS):
            if d["t0"] <= t:
                i = k
        d = SHOTS[i]
        img = np.zeros((H, W, 3), np.float32)
        _dibujar(d, img, t)
        tipo, dur = d["ent"]
        if i > 0 and t < d["t0"] + dur:
            A = np.zeros((H, W, 3), np.float32)
            _dibujar(SHOTS[i - 1], A, t)
            img = X.mezcla2(A, img, (t - d["t0"]) / dur, tipo, i)
        img = X.cine(img, t, **d["grado"])
        img *= smooth(prog(t, 0.0, 0.9))
        return np.clip(img, 0, 1).astype(np.float32)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
