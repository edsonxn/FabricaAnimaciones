# -*- coding: utf-8 -*-
"""Parche 2: base() con varias ventanas; ríos en toda la tierra con datos; picos de todas las ventanas."""
p = 'kz_mapa.py'
s = open(p, encoding='utf-8').read()

# quitar _afin_h de Mapa (ahora vive en Ventana)
a = s.index("    def _afin_h(self, cam, nivel):\n        \"\"\"Matriz 2x3: destino a media resolución (x, y) -> índices (j, i) del nivel de la pirámide (WARP_INVERSE_MAP).\"\"\"\n        lo, la, z = cam\n        e = self.escalas[nivel]")
b = s.index("    def _poly_px(self, cam, p):")
s = s[:a] + s[b:]

# bloque inicial de base()
a = s.index("        self._cargar()\n        ppg = K * cam[2]\n        nivel = int(np.clip(math.floor(math.log2(max(1.0, 60.0 / ppg))), 0, 3))\n        A = self._afin_h(cam, nivel)")
b = s.index("        elev_t = np.maximum(elev, 12.0)")
nuevo = '''        self._cargar()
        ppg = K * cam[2]
        nivel = int(np.clip(math.floor(math.log2(max(1.0, 60.0 / ppg))), 0, 3))
        lon_h = cam[0] + (self.xx2 * 2 - 960) / (cam[2] * K * KX)
        lat_h = cam[1] - (self.yy2 * 2 - 540) / (cam[2] * K)
        # ---- relieve de todas las ventanas que se ven (con mezcla suave en sus bordes)
        elev = np.full((HH, WH), -3000.0, np.float32)
        hum = np.full((HH, WH), 0.45, np.float32)
        w_dato = np.zeros((HH, WH), np.float32)
        for v in self.vent:
            if not v.toca(cam):
                continue
            A = v.afin_h(cam, nivel)
            e_i = cv2.warpAffine(v.pir[nivel], A, (WH, HH), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=NODATA)
            h_i = cv2.warpAffine(v.pir_h[nivel], A, (WH, HH), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)
            d = np.minimum(np.minimum(lon_h - v.lon_min, v.lon_max - lon_h), np.minimum(lat_h - v.lat_min, v.lat_max - lat_h))
            w_i = np.clip(d / 3.0, 0.0, 1.0)
            w_i = w_i * w_i * (3 - 2 * w_i)
            mejor = (e_i > -7000) & (w_i > w_dato)
            elev = np.where(mejor, e_i, elev)
            hum = np.where(mejor, h_i, hum)
            w_dato = np.where(mejor, w_i, w_dato)
        m_mx = self._mascara(cam, self.vec_mx)
        m_ot = self._mascara(cam, self.vec_otros)
        tierra = np.maximum(m_mx, m_ot)
        tierra_h = cv2.resize(tierra, (WH, HH), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        mx_h = cv2.resize(m_mx, (WH, HH), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        lod = float(_suave_np(np.float32(cam[2]), 0.40, 0.22))     # 1 = vista lejana (Atlántico): el relieve de datos se funde con el genérico
        gen = self._relieve_generico(cam)
        hum_g, alt_g = _clima_global(lon_h, lat_h)
        gen_g = np.maximum(120.0, gen * 0.75 + alt_g)
        # tierra que no es México: relieve real donde hay datos (EE. UU. del sur, Cuba, Iberia, Francia…) y genérico fuera de ellos (mezcla continua)
        vecino = (tierra_h > 0.5) & (mx_h < 0.5)
        elev = np.where(vecino, elev * w_dato + gen_g * (1 - w_dato), elev)
        hum = np.where(vecino, hum_g, hum)
        # el mar se funde hacia el azul profundo plano en los bordes de las ventanas de datos (sin costuras)
        elev = np.where(elev < 0, elev * w_dato + (-2600.0) * (1 - w_dato), elev)
        if lod > 0.0:
            elev = np.where(tierra_h > 0.5, elev * (1 - lod) + gen_g * lod, elev * (1 - lod) - 2600.0 * lod)
            hum = np.where(tierra_h > 0.5, hum * (1 - lod) + hum_g * lod, hum)
'''
s = s[:a] + nuevo + s[b:]

# ríos en toda la tierra
s = s.replace("        self._agua(img, cam, ppg, mostrar_rios and cam[2] >= 0.36, rios_umbral, m_mx, rio_color)", "        self._agua(img, cam, ppg, mostrar_rios and cam[2] >= 0.36, rios_umbral, tierra, rio_color)")

# picos de todas las ventanas
if "def picos(self)" not in s:
    s = s.replace("    # ------------------------------------------------------------------ geometría\n    @staticmethod\n    def proy(cam, lon, lat):", '''    def picos(self):
        """Máximos locales (> 2000 m) de todas las ventanas: array [lon, lat, altitud] ordenado de mayor a menor."""
        self._cargar()
        if getattr(self, "_picos", None) is None:
            L = []
            for v in self.vent:
                a = v.pir[1]
                k = 5
                mx = cv2.dilate(a, np.ones((2 * k + 1, 2 * k + 1), np.uint8))
                ys, xs = np.nonzero((a >= mx) & (a > 2000))
                lat = v.lat0 + (ys * 2 + 0.5) * v.paso
                lon = v.lon0 + (xs * 2 + 0.5) * v.paso
                L.append(np.stack([lon, lat, a[ys, xs]], 1))
            p = np.concatenate(L)
            self._picos = p[np.argsort(-p[:, 2])]
        return self._picos

    # ------------------------------------------------------------------ geometría
    @staticmethod
    def proy(cam, lon, lat):''', 1)
open(p, 'w', encoding='utf-8').write(s)

# montes() usa picos()
q = 'kz_mapa_dib.py'
m = open(q, encoding='utf-8').read()
a = m.index("    if not hasattr(M, \"_picos\"):")
b = m.index("    sel = p[p[:, 2] >= min_alt]")
m = m[:a] + "    p = M.picos()\n" + m[b:]
open(q, 'w', encoding='utf-8').write(m)
print('ok parte 2')
