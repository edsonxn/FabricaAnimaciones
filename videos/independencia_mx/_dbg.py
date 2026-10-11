import estilos
estilos.activar("kurzgesagt")
import t07 as T
cam = T.cam_c(243.4)
print("cam", cam)
for nm, ll in (("mexico", (-99.13, 19.43)), ("toluca", (-99.66, 19.29)), ("cruces", (-99.35, 19.30)), ("retiro", (-100.0, 19.45))):
    print(nm, [float(v) for v in T.MP.proy(cam, ll[0], ll[1])])
import kz_mapa_dib as MD
print(MD.punto_ruta(cam, T.RUTA_AV, 0.5))
