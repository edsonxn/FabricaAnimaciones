# -*- coding: utf-8 -*-
def rep(s, old, new):
    assert old in s, "NO ENCONTRADO: " + old[:100]
    return s.replace(old, new, 1)


k = open('kit_cp.py', encoding='utf-8').read()
i0 = k.index("def F_ventana_piedra(")
i1 = k.index("def F_vena(")
nuevo = '''def F_ventana_piedra(t_piedra, base=(0.075, 0.08, 0.095)):
    """Muro de bloques con una ventana en la pared (luz fría detrás del vidrio); una piedra blanca aparece en ella: el detalle de las 7:41 p. m.
    que contaron los testigos. Gráfico de recreación (se rotula como tal)."""
    def f(lz, tl, t, dur, ext):
        if "muro" not in _C:
            rng = np.random.default_rng(3)
            ruido = cv2.GaussianBlur(rng.random((H // 6, W // 6)).astype(np.float32), (0, 0), 1.0)
            _C["muro"] = cv2.resize(ruido, (W, H), interpolation=cv2.INTER_CUBIC)
            bl = np.ones((H, W), np.float32)
            for yy in range(0, H, 72):
                bl[yy:yy + 3] *= 0.45
                for xx in range((yy // 72 % 2) * 120, W, 240):
                    bl[yy:yy + 72, xx:xx + 3] *= 0.5
            _C["bloques"] = bl
        muro, bloques = _C["muro"], _C["bloques"]
        cam = 1.0 + 0.05 * (tl / max(dur, 1))
        cx, cy = 1180, 520
        ww_, hh_ = int(640 * cam), int(460 * cam)
        x0, y0 = int(cx - ww_ / 2), int(cy - hh_ / 2)
        # muro iluminado desde la ventana (halo frío)
        Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((X - cx) / 1100.0) ** 2 + ((Y - cy) / 760.0) ** 2)
        luz = np.clip(1.0 - d, 0, 1) ** 1.6
        lz[:] = (np.array(base, np.float32) * (0.75 + 0.5 * muro[..., None]) * bloques[..., None]) + luz[..., None] * np.array([0.10, 0.13, 0.17], np.float32)
        # marco y vidrio
        cv2.rectangle(lz, (x0 - 22, y0 - 22), (x0 + ww_ + 22, y0 + hh_ + 22), (0.20, 0.21, 0.23), -1)
        cv2.rectangle(lz, (x0 - 22, y0 - 22), (x0 + ww_ + 22, y0 + hh_ + 22), (0.34, 0.35, 0.38), 4)
        vid = np.linspace(0.55, 0.22, hh_)[:, None, None] * np.array([0.72, 0.86, 1.0], np.float32)
        lz[y0:y0 + hh_, x0:x0 + ww_] = vid
        refl = np.zeros((hh_, ww_), np.float32)
        cv2.fillConvexPoly(refl, np.array([[0, hh_ * 0.05], [ww_ * 0.42, 0], [ww_ * 0.62, 0], [0, hh_ * 0.75]], np.int32), 0.13)
        lz[y0:y0 + hh_, x0:x0 + ww_] += refl[..., None]
        cv2.line(lz, (x0 + ww_ // 2, y0), (x0 + ww_ // 2, y0 + hh_), (0.20, 0.21, 0.23), 8)          # travesaño
        # alféizar con su sombra
        cv2.rectangle(lz, (x0 - 40, y0 + hh_ + 22), (x0 + ww_ + 40, y0 + hh_ + 52), (0.30, 0.31, 0.33), -1)
        cv2.rectangle(lz, (x0 - 40, y0 + hh_ + 52), (x0 + ww_ + 40, y0 + hh_ + 80), (0.05, 0.05, 0.06), -1)
        # polvo en suspensión frente a la luz
        for i in range(36):
            px_ = (X[0, int((i * 197 + t * (8 + i % 5) * 4) % W)])
            py_ = (i * 83 + t * (6 + i % 4) * 5) % (H * 0.9)
            cv2.circle(lz, (int(px_), int(py_)), 2 + i % 2, (0.5, 0.55, 0.62), -1, cv2.LINE_AA)
        # piedra: cae dentro del vidrio y rebota una vez
        if t >= t_piedra:
            u = clamp01((t - t_piedra) / 0.6)
            yb = y0 + hh_ - 34
            ya = y0 + 34
            yy_ = lerp(ya, yb, u * u) - (math.sin(clamp01((t - t_piedra - 0.6) / 0.35) * math.pi) * 22 if t > t_piedra + 0.6 else 0)
            xx_ = x0 + ww_ * 0.62
            gl = np.zeros((H, W), np.float32)
            cv2.ellipse(gl, (int(xx_), int(yy_)), (38, 28), 14, 0, 360, 1.0, -1, cv2.LINE_AA)
            halo = cv2.GaussianBlur(gl, (0, 0), 44) * 0.7
            lz += halo[..., None] * np.array([1.0, 0.98, 0.92], np.float32)
            lz *= (1 - gl[..., None] * 0.97)
            lz += gl[..., None] * np.array([0.95, 0.94, 0.90], np.float32) * 0.97
    return f


'''
k = k[:i0] + nuevo + k[i1:]
open('kit_cp.py', 'w', encoding='utf-8').write(k)

b = open('tomas_b.py', encoding='utf-8').read()
b = rep(b, 'F_clip("france24", ini=15.4, fin=16.4, z0=1.0, z1=1.05, tono=(0.7, 0.7, 0.8))', 'F_clip("france24", ini=12.9, fin=16.4, z0=1.0, z1=1.05, tono=(0.8, 0.8, 0.9))')
open('tomas_b.py', 'w', encoding='utf-8').write(b)
print('ok')
