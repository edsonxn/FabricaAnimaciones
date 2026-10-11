import sys, numpy as np, cv2
import boceto as B, mapa as M
import obj_a as A, obj_b as Bb, obj_c as C
from obj_base import *
M.cargar()
cam=M.Cam(108,35,1.25)
def hoja_de(lista, nombre, cols=6, esc=0.55, cell=(300, 340)):
    img=M.fondo_base(); M.pintar_tierra(img,cam,0)
    S=cam.proyectar(M.CAMPOS['tang']); M.pintar(img,S,M.COL['tang'],1.0,0)
    h=B.Hoja(); h.limpiar(); h.fondo=img
    for i,(n,d,s) in enumerate(lista):
        x=110+(i%cols)*cell[0]+80; y=110+(i//cols)*cell[1]+200
        d.dibujar(h,x,y,s*esc,0,False,1.0,0,i+3,peg=True)
    out=np.clip(h.componer(),0,1)
    cv2.imwrite(f'previews/{nombre}.jpg',(out[...,::-1]*255).astype(np.uint8))
a=[('casa',A.casa(),1.1),('arrozal',A.arrozal(),1),('mijo',A.mijo_planta(),1),('ding',A.ding(),1),('trono',A.trono(),1),('hueso',A.hueso(),1),('grietas',A.grietas_hueso(),1),('llama',A.llama(1),1),
   ('nube',A.nube_cielo(),1),('sol',A.sol_brillo(),1),('pulgar',A.pulgar(True),1),('rayo',A.rayo(),1),('espadas',A.espadas(),1),('moneda',A.moneda(),1),('rueda',A.rueda(),1),('rollo',A.rollo_escritura(),1),
   ('torre',A.torre_muralla(),1),('barro',A.soldado_barro(),1),('reloj',A.arena_reloj(),1),('puerta',A.puerta(0.0),0.8),('camello',A.camello(0),0.9),('seda',A.rollo_seda(),1),('papel',A.papel_hoja(),1),('pagoda',A.pagoda(),0.8),
   ('multitud',A.multitud(),1),('horq',A.horquilla(),1),('bolsa',A.bolsa_dinero(),1),('corona',A.cetro_corona(),1),('pregunta',A.signo_pregunta(),1),('estallido',A.estallido(),1)]
hoja_de(a,'_o_a')
b=[('barca',Bb.barca_arroz(),1),('poeta',Bb.poeta(),1),('bailarina',Bb.bailarina(0),1),('alquimista',Bb.alquimista(),1),('frasco',Bb.frasco_burbujas(),1),('cohete',Bb.cohete(),1),('chispas',Bb.chispas(),1),
   ('billete',Bb.billete(),1),('tipo',Bb.tipo_movil(),1),('brujula',Bb.brujula(0.5),1),('junco',Bb.junco(),0.8),('carabela',Bb.carabela(),0.8),('caballo',Bb.caballo(1),0.9),('jinete',Bb.jinete(0),0.8),
   ('flecha',Bb.flecha(),1),('tormenta',Bb.tormenta(),1),('yurta',Bb.yurta(),1),('huerfano',Bb.huerfano(),1),('emperador',Bb.emperador(),1),('palacio',Bb.palacio(),0.8),('nave',Bb.nave_tesoro(),0.6),('puertaC',Bb.gran_puerta_cerrada(1.0),0.7),('ladrillo',Bb.ladrillo_muro(),1)]
hoja_de(b,'_o_b')
c=[('manchu',C.jinete_manchu(),0.8),('ptaciudad',C.puerta_ciudad(),0.9),('canon',C.canon(),1),('vapor',C.vapor(0),0.7),('te',C.caja_te(),1),('opio',C.caja_opio(),1),('func',C.funcionario_opio(),1),('ingles',C.ingles(),1),
   ('isla',C.isla_trozo(),1),('nino',C.nino_emperador(),1),('coronaG',C.corona_grande(),1),('soldado',C.soldado_fusil(),1),('avion',C.avion(),1),('lider',C.lider(),1),('lider2',C.lider_nuevo(),1),('tribuna',C.tribuna(),0.9),
   ('bandera',C.bandera(),0.9),('horno',C.horno_patio(),1),('humo',C.humo(0),1),('cuenco',C.cuenco_vacio(),1),('trigo',C.trigo(0),1),('trigo2',C.trigo(1),1),('gatoB',C.gato('blanco'),1),('gatoN',C.gato('negro'),1),
   ('raton',C.raton(),1),('vela',C.vela(),1),('rasca',C.rascacielos(),0.9),('fabrica',C.fabrica(),0.9),('podio',C.podio(),1),('tren',C.tren_bala(),0.7),('crono',C.cronometro(0.6),1),('dialogo',C.globo_dialogo(),1),('boton',C.boton_suscribir(),0.8),('campana',C.campana(),1)]
hoja_de(c,'_o_c')
print('ok')
