# -*- coding: utf-8 -*-
"""Parche 3 del mapa: clima y relieve global de dirección de arte para los continentes sin datos de relieve; crestas de ola menos densas."""
p = 'kz_mapa.py'
s = open(p, encoding='utf-8').read()

if "def _clima_global" not in s:
    s = s.replace("class Mapa:", '''def _clima_global(lon, lat):
    """(humedad 0..1, altitud extra en m) para tierra SIN datos de relieve: dirección de arte, no un dato climático. Sahara seco, trópicos verdes, hielo en Groenlandia,
    Andes, Rocosas y Alpes elevados."""
    hum = np.full_like(lon, 0.45)
    alt = np.zeros_like(lon)

    def g(lo, la, sx, sy):
        return np.exp(-(((lon - lo) / sx) ** 2 + ((lat - la) / sy) ** 2))
    hum += 0.45 * g(-60, -3, 22, 9) + 0.40 * g(18, 0, 16, 9) + 0.35 * g(-80, 6, 6, 5) + 0.30 * g(100, 0, 1, 1)
    hum -= 0.60 * g(8, 24, 28, 7) + 0.40 * g(-69, -22, 7, 8) + 0.35 * g(-105, 34, 14, 7) + 0.40 * g(38, 28, 12, 7) + 0.25 * g(-68, -42, 6, 10)
    hum += 0.15 * g(10, 50, 22, 8)
    hum -= 0.30 * g(-100, 62, 40, 10)
    alt += 3400 * g(-76, -10, 6, 20) + 2600 * g(-110, 44, 7, 12) + 2800 * g(9, 46.5, 7, 2.2) + 2000 * g(-5, 31, 6, 3) + 1500 * g(-3, 42.5, 3, 1.0) + 2400 * g(-45, 72, 24, 9) * (lat > 60)
    alt += 1400 * g(30, 8, 9, 8) + 1300 * g(16, -22, 8, 8) + 1100 * g(-52, -15, 9, 9) + 900 * g(25, 60, 14, 6)
    return np.clip(hum, 0.0, 1.0).astype(np.float32), alt.astype(np.float32)


class Mapa:''', 1)

# usar el clima global en `base()` para los vecinos y las vistas lejanas
s = s.replace("""        vecino = (tierra_h > 0.5) & (mx_h < 0.5)                  # los países vecinos no llevan relieve de datos (así no se ve el recuadro de la ventana)
        elev = np.where(vecino, gen, elev)
        hum = np.where(vecino, 0.25, hum)
        if lod > 0.0:
            elev = np.where(tierra_h > 0.5, elev * (1 - lod) + gen * lod, elev * (1 - lod) - 2600.0 * lod)
            hum = hum * (1 - lod) + 0.30 * lod""",
"""        vecino = (tierra_h > 0.5) & (mx_h < 0.5)                  # los países vecinos no llevan relieve de datos (así no se ve el recuadro de la ventana)
        lon_h = cam[0] + (self.xx2 * 2 - 960) / (cam[2] * K * KX)
        lat_h = cam[1] - (self.yy2 * 2 - 540) / (cam[2] * K)
        hum_g, alt_g = _clima_global(lon_h, lat_h)
        gen_g = np.maximum(120.0, gen * 0.75 + alt_g)
        elev = np.where(vecino, gen_g, elev)
        hum = np.where(vecino, hum_g, hum)
        if lod > 0.0:
            elev = np.where(tierra_h > 0.5, elev * (1 - lod) + gen_g * lod, elev * (1 - lod) - 2600.0 * lod)
            hum = np.where(tierra_h > 0.5, hum * (1 - lod) + hum_g * lod, hum)""")
# los vecinos conservan color más vivo (no tan gris)
s = s.replace("        col = col * mxk + (col * 0.50 + gris * 0.50) * 0.84 * (1 - mxk)", "        col = col * mxk + (col * 0.72 + gris * 0.28) * 0.90 * (1 - mxk)")
open(p, 'w', encoding='utf-8').write(s)

# crestas de ola menos densas y más tenues
q = 'kz_mapa_dib.py'
m = open(q, encoding='utf-8').read()
m = m.replace("            if hh > 0.62:\n                continue", "            if hh > 0.30:\n                continue")
m = m.replace("            al = 0.22 + 0.22 * (0.5 + 0.5 * math.sin(t * 1.6 + i * 1.3 + j * 0.7))", "            al = 0.10 + 0.16 * (0.5 + 0.5 * math.sin(t * 1.6 + i * 1.3 + j * 0.7))")
m = m.replace("            if tipo > 0.985 and fauna and z > 0.18:", "            if tipo > 0.955 and fauna and z > 0.18:")
m = m.replace("            if tipo > 0.96 and barcos and z > 0.18:                      # barco lejano que navega\n                d = 1 if tipo > 0.975 else -1", "            if tipo > 0.915 and barcos and z > 0.18:                      # barco lejano que navega\n                d = 1 if tipo > 0.935 else -1")
open(q, 'w', encoding='utf-8').write(m)
print('ok')
