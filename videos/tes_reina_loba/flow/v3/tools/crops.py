from PIL import Image, ImageFilter
M='v3/muestras/'; L=M+'loc/'
C={ # nombre: (archivo, (x0,y0,x1,y1) fracciones)
 'ob_consejo':(M+'Npj94AyaLek_53.jpg',(0,0,1,.70)),
 'ob_martin':(M+'Npj94AyaLek_88.jpg',(.28,0,1,.74)),
 'ob_martin2':(M+'Npj94AyaLek_124.jpg',(.1,0,.9,.72)),
 'ob_uriel':(M+'O7M463t8Mi0_261.jpg',(.1,0,.9,.70)),
 'ob_ocato':(M+'Npj94AyaLek_338.jpg',(.15,0,.85,.72)),
 'ob_arriana':(M+'_gkpIchIESI_9.jpg',(.1,0,.9,.70)),
 'ob_mercator':(M+'5fxPsyJS3y4_114.jpg',(.1,0,.9,.74)),
 'ob_raminus':(M+'5fxPsyJS3y4_879.jpg',(.1,0,.9,.70)),
 'ob_calle_noche':(M+'Sq5qoGhxHQI_42.jpg',(.1,.05,1,.9)),
 'ob_ciudad':(M+'yd8WjcKrGJU_123.jpg',(0,0,1,1)),
 'ob_taberna':(M+'yd8WjcKrGJU_264.jpg',(0,0,1,1)),
 'ob_salon':(M+'yd8WjcKrGJU_405.jpg',(0,0,1,1)),
 'ob_aerea':(M+'JGhlg4JqvQw_88.jpg',(0,.12,1,.88)),
 'ob_templo':(M+'Npj94AyaLek_160.jpg',(.08,.06,.78,.86)),
 'ob_uriel_celda':(M+'O7M463t8Mi0_435.jpg',(.2,.05,1,.85)),
 'sk_palacio':(L+'s068_1.jpg',(.05,.07,.85,.88)),
 'sk_trono_elisif':(L+'s032_1.jpg',(.0,.05,1,.5)),
 'sk_taberna':(L+'s094_1.jpg',(0,.08,1,1)),
 'sk_dour_pasillo':(M+'eKmi4hmHl0Y_1035.jpg',(0,0,1,1)),
 'sk_dour_salon':(M+'eKmi4hmHl0Y_837.jpg',(0,0,1,1)),
 'sk_palacio_entrada':(M+'81FYBtKdWuY_1566.jpg',(0,.08,1,1)),
 'sk_jordis':(M+'3TklBWCm1Ec_333.jpg',(.22,.04,.63,1)),
 'sk_falk':(L+'s032_4.jpg',(.25,.0,.5,.55)),
 'sk_sheogorath_mesa':(M+'kIyLPCmQG-M_230.jpg',(.25,.1,1,1)),
}
for n,(f,(a,b,c,d)) in C.items():
    im=Image.open(f).convert('RGB'); W,H=im.size
    im=im.crop((int(a*W),int(b*H),int(c*W),int(d*H)))
    im.save(f'ingred/{n}.jpg',quality=92); print(n,im.size)
