# -*- coding: utf-8 -*-
"""Parche: más países en el mapa (toda América, Europa, norte de África), máscara de mar y `mar_vivo`; clamp correcto en llamada; cuello corto en retratos."""
import os

# ---------------------------------------------------------------- 1) ampliar países
p = 'kz_mapa_datos.py'
s = open(p, encoding='utf-8').read()
a = s.index("def paises():")
b = s.index("def lagos():")
nuevo = '''def paises():
    """Todos los países con alguna parte entre lon -135..50 y lat -58..75 (América, Europa y el norte de África). México y los vecinos cercanos conservan el detalle completo;
    el resto se simplifica a ~0,02° para que el archivo no crezca."""
    import cv2
    g = json.load(open(PAISES, encoding="utf-8"))
    detalle = {"Mexico", "United States of America", "Guatemala", "Belize", "Honduras", "El Salvador", "Nicaragua", "Cuba", "Spain", "Costa Rica", "Panama", "Jamaica", "Haiti", "Dominican Republic", "Bahamas"}
    out = {}
    for ft in g["features"]:
        nom = ft["properties"].get("NAME") or ft["properties"].get("ADMIN")
        polys = []
        for poly in _anillos(ft["geometry"]):
            ext = np.array(poly[0], np.float32)
            if len(ext) < 4:
                continue
            if not (ext[:, 0].max() > -135 and ext[:, 0].min() < 50 and ext[:, 1].max() > -58 and ext[:, 1].min() < 75):
                continue
            if nom not in detalle:
                ext = simplificar(ext, 0.02)
            polys.append(ext.tolist())
        if polys:
            out[nom] = polys
    return out


'''
s = s[:a] + nuevo + s[b:]
open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- 2) máscara de mar + mar_vivo en kz_mapa
p = 'kz_mapa.py'
s = open(p, encoding='utf-8').read()
if "def es_tierra" not in s:
    s = s.replace("    # ------------------------------------------------------------------ geometría\n    @staticmethod\n    def proy(cam, lon, lat):",
'''    # ------------------------------------------------------------------ máscara de tierra (para colocar cosas solo en el mar)
    def _mascara_tierra(self):
        if getattr(self, "_mt", None) is not None:
            return
        self._cargar()
        res = 10.0                                              # celdas por grado
        self._mt0 = (-135.0, -58.0)
        w, h = int(200 * res), int(135 * res)
        m = np.zeros((h, w), np.uint8)
        for pols in self.paises.values():
            for p in pols:
                q = np.stack([(p[:, 0] - self._mt0[0]) * res, (p[:, 1] - self._mt0[1]) * res], 1)
                cv2.fillPoly(m, [np.round(q).astype(np.int32)], 255)
        self._mt = m
        self._mt_res = res

    def es_tierra(self, lon, lat):
        """True donde hay tierra (según los polígonos de países), vectorizado."""
        self._mascara_tierra()
        i = np.clip(((np.asarray(lat) - self._mt0[1]) * self._mt_res).astype(int), 0, self._mt.shape[0] - 1)
        j = np.clip(((np.asarray(lon) - self._mt0[0]) * self._mt_res).astype(int), 0, self._mt.shape[1] - 1)
        return self._mt[i, j] > 0

    # ------------------------------------------------------------------ geometría
    @staticmethod
    def proy(cam, lon, lat):''', 1)
open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- 3) clamp correcto en llamada
p = 'kz_ui.py'
s = open(p, encoding='utf-8').read()
s = s.replace('''    if clamp:
        mx = w / 2 * k + 24
        x = min(max(x, mx), W - mx)
        y = min(max(y, h * k + px * 0.4 + 70), H - 40)''', '''    if clamp:
        nt_ = px * 0.34
        if cola in ("izq", "der"):
            mx = (w + nt_) * k + 24
            x = min(max(x, 24 if cola == "izq" else mx), (W - mx) if cola == "izq" else W - 24)
            y = min(max(y, h / 2 * k + 24), H - h / 2 * k - 24)
        else:
            mx = w / 2 * k + 24
            x = min(max(x, mx), W - mx)
            if cola == "abajo":
                y = min(max(y, (h + nt_) * k + 24), H - 24)
            elif cola == "arriba":
                y = min(max(y, 24), H - (h + nt_) * k - 24)
            else:
                y = min(max(y, h / 2 * k + 24), H - h / 2 * k - 24)''')
open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- 4) cuello corto en retratos
p = 'kz_retrato.py'
s = open(p, encoding='utf-8').read()
s = s.replace("    _poly(lz, [(-0.40, -0.9), (0.40, -0.9), (0.46, 0.5), (-0.46, 0.5)], x, y, s, sombra, flip, A)\n    _poly(lz, [(-0.40, -0.9), (0.28, -0.9), (0.34, 0.5), (-0.46, 0.5)], x, y, s, P.mezcla(piel, sombra, 0.45), flip, A)",
              "    _poly(lz, [(-0.52, -0.9), (0.52, -0.9), (0.60, 0.5), (-0.60, 0.5)], x, y, s, sombra, flip, A)\n    _poly(lz, [(-0.52, -0.9), (0.36, -0.9), (0.44, 0.5), (-0.60, 0.5)], x, y, s, P.mezcla(piel, sombra, 0.45), flip, A)")
# torso más arriba (hombros pegados a la barbilla)
s = s.replace("    forma = [(-0.45, 0.2), (-1.6, 0.55), (-2.4, 1.25), (-2.9, 3.4), (2.9, 3.4), (2.4, 1.25), (1.6, 0.55), (0.45, 0.2)]",
              "    forma = [(-0.55, -0.12), (-1.6, 0.20), (-2.4, 0.95), (-2.9, 3.4), (2.9, 3.4), (2.4, 0.95), (1.6, 0.20), (0.55, -0.12)]")
s = s.replace("    forma2 = [(-0.45, 0.2), (-1.6, 0.55), (-2.4, 1.25), (-2.9, 3.4), (1.0, 3.4), (1.0, 1.0), (0.45, 0.2)]",
              "    forma2 = [(-0.55, -0.12), (-1.6, 0.20), (-2.4, 0.95), (-2.9, 3.4), (1.0, 3.4), (1.0, 0.8), (0.55, -0.12)]")
open(p, 'w', encoding='utf-8').write(s)
print('parches 1-4 ok')
