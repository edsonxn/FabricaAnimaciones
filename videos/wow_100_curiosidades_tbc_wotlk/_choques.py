"""Choques en la capa de efectos: pares de FX que se pisan en tiempo y espacio (cajas aproximadas en fracciÃ³n del cuadro)."""
import os, sys
os.chdir(r"C:\FabricaAnimaciones\videos\wow_100_curiosidades_tbc_wotlk")
sys.path[:0] = [os.getcwd(), r"C:\FabricaAnimaciones\nucleo"]
import secuencia_fx as F
c = F.cargar()
cajas = []
for d in c.fx:
    n = d.get("nombre", d["tipo"])
    if d["tipo"] == "pantalla":
        cajas.append((d["de"], d["a"], n, None)); continue
    x, y = d.get("x", .5), d.get("y", .5)
    if n.startswith("pegatina"):
        w, h = .22, .38
        if y == .50: w, h = .33, .58
    elif n.startswith("mapa"):
        w, h = .52, .60
    elif n.startswith("MG"):
        w, h = .80, .50
    elif d["tipo"] == "imagen":                  # tarjetas/apoyos (26-oct: también entran)
        w, h = d.get("ancho", .44), .30
        n = "tarjeta %d" % d.get("apoyo", 0) if d.get("apoyo") else n
    else:
        w, h = .3, .3
    cajas.append((d["de"], d["a"], n, (x - w / 2, y - h / 2, x + w / 2, y + h / 2)))
cajas.sort()
for i, (a0, a1, n, b) in enumerate(cajas):
    for (c0, c1, m, e) in cajas[i + 1:]:
        if c0 >= a1 - .3:
            break
        if b is None or e is None:
            continue
        if b[0] < e[2] and e[0] < b[2] and b[1] < e[3] and e[1] < b[3]:
            print(f"{a0:7.1f}-{a1:6.1f} {n:28s} Ã— {c0:7.1f}-{c1:6.1f} {m}")
print(len(cajas), "cajas;", sum(1 for k in cajas if k[3] is None), "pantallas"); print([ (round(k[0]),k[2]) for k in cajas[:6]])


