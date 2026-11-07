import sys, time; sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import anime_vivo as AV
P="flow/prueba/"
t=AV.Toma(P+"r1a.jpg", bocas=[P+"r1_boca2.jpg",P+"r1_boca1.jpg"], ojos=[P+"r1_ojos1.jpg"], mov="cabeceo",
          cam=dict(z0=1.0,z1=1.18,c0=(0.5,0.5),c1=(0.56,0.42)),
          fx=[("rayos",dict(origen=(0.95,-0.05),ang=125)),("polvo",dict(caja=(0.55,0.0,1.0,0.75)))])
a=r"..\llamada_domingo\medios\scene-005.mp4"
s=time.time(); t.preparar(); print("prep",time.time()-s)
AV.cuadros([(0,t)],10,[0.5,2.5,5,7.5],"previews/_hoja_prueba.jpg",audio=a)
s=time.time(); AV.render([(0,t)],10,"previews/prueba_005.mp4",audio=a,mux_audio=True); print("render",time.time()-s)
