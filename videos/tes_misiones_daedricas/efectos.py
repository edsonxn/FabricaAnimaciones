# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 8 misiones daédricas que NUNCA deberías hacer en Skyrim» (SECUENCIA YT, Crónicas de Tamriel).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 9 avisos de misión (título del top + uno por puesto), arriba al centro.
- Fichas de objeto/personaje (estilo inventario) SOLO con datos del guion, arriba a la derecha.
- 3 motion graphics (regla de canal heredada de Warcraft): Navaja 2 de 100, Hoja de Ébano 10 traiciones (10 -> 30) y
  el reloj de 5 minutos del Anillo de Namira.
  python fab.py tes_misiones_daedricas fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py tes_misiones_daedricas fx         audio/fx.wav
"""
import mg_tes as T

CAMARA = {}
FUNDIDO = {}

_FX = .76      # fichas: arriba a la derecha (no tapan el centro del clip)
_FY = .30


def ficha(en, nombre, efecto, origen=None, dur=5.0, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def aviso(en, arriba, titulo, dur=3.6):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


FX = [
    # ---- avisos de misión (uno por puesto)
    aviso("las ocho misiones daédricas que", "Top 8", "Misiones daédricas que nunca deberías hacer", dur=4.5),
    aviso("Número ocho. Empezamos", "Misión daédrica · número 8", "Clavicus Vile"),
    aviso("En el siete aparece", "Misión daédrica · número 7", "Mehrunes Dagon"),
    aviso("Número seis, y aquí", "Misión daédrica · número 6", "Hircine"),
    aviso("Bajando al cinco", "Misión daédrica · número 5", "Vaermina"),
    aviso("Ahora sí, entramos", "Misión daédrica · número 4", "Molag Bal"),
    aviso("Número tres. En el Salón", "Misión daédrica · número 3", "Namira"),
    aviso("Ya en el podio", "Misión daédrica · número 2", "Mephala"),
    aviso("Y llegamos al número uno", "Misión daédrica · número 1", "Boethiah"),

    # ---- 8 · Clavicus Vile
    ficha("Se llama Barbas", "Barbas", "Perro que habla. Gran parte del poder de su dueño vive dentro de él.",
          origen="Mascota de Clavicus Vile", dur=6.0),
    ficha("te llevas la Máscara", "Máscara de Clavicus Vile", "Precios un *20 %* mejores.", origen="Artefacto daédrico"),

    # ---- 7 · Mehrunes Dagon
    ficha("Te pide recuperar los tres fragmentos", "Navaja de Mehrunes", "Rota en *3* fragmentos.", origen="Artefacto daédrico"),
    ficha("te ofrece quinientas monedas", "Silus Vesuius", "Ofrece *500* monedas de oro por su vida.",
          origen="Dueño del museo del Alba Mítica"),
    dict(tipo="mg", fn=T.rejilla("Navaja de Mehrunes: muerte instantánea", 100, 2, remate=("2 de cada 100 golpes", 2)),
         de=("la navaja mata al instante", -.2), a=("como la impresora de la oficina|fin", .3),
         marcas=["la navaja mata al instante", "más o menos dos por ciento", "Dos golpes de cada cien"],
         y=.50, sale=.4, nombre="MG navaja", ver=5.0),

    # ---- 6 · Hircine
    ficha("En la cárcel de Falkreath", "Sinding", "Hombre lobo. Encerrado por matar a una niña de *9* años.",
          origen="Prisionero de Falkreath", dur=6.0),
    ficha("te llevas la Piel del Salvador", "Piel del Salvador", "Resistir magia *15*. Resistir veneno *50*.",
          origen="Recompensa de Hircine"),
    ficha("si te pones el anillo maldito", "Anillo de Hircine", "*1* posibilidad entre *10* cada hora de transformarte al "
          "aire libre. No te lo puedes quitar.", origen="Maldito", rojo=True, dur=6.5),

    # ---- 5 · Vaermina
    ficha("Un sacerdote de Mara llamado Erandur", "Erandur", "Sacerdote de Mara.", origen="Pide ayuda", dur=4.5),
    ficha("Erandur antes se llamaba Cassimir", "Cassimir", "Sacerdote de Vaermina. Huyó y dejó atrás a sus compañeros.",
          origen="El pasado de Erandur", rojo=True, dur=6.0),
    ficha("La calavera es un bastón", "Calavera de la Corrupción", "Daño *20*. Hasta *50* con sueños robados a alguien dormido.",
          origen="Artefacto daédrico", dur=6.0),

    # ---- 4 · Molag Bal
    ficha("te encarga liberar a Logrolf", "Logrolf", "Sacerdote de Boethiah, prisionero de los renegados.",
          origen="Encargo de Molag Bal", dur=5.0),
    ficha("el juego no la cuenta como asesinato", "Recompensa por tu cabeza", "*0* monedas. No cuenta como asesinato.",
          origen="Registro de crímenes", dur=4.5),
    ficha("El premio es la Maza de Molag Bal", "Maza de Molag Bal", "Por golpe: *25* de aguante y *25* de magia. "
          "Atrapa el alma *3* segundos.", origen="Artefacto daédrico", dur=6.5),

    # ---- 3 · Namira
    ficha("el hermano Verulus", "Hermano Verulus", "Sacerdote de Arkay. Guarda el Salón de los Muertos.", origen="Markarth"),
    ficha("Eola es encantadora", "Eola", "Encantadora. Caníbal.", origen="Culto de Namira", rojo=True, dur=4.0),
    ficha("La recompensa es el Anillo de Namira", "Anillo de Namira", "Aguante *+50*. Comer un cadáver: salud extra y "
          "regeneración durante *5* minutos.", origen="Artefacto daédrico", dur=6.0),
    dict(tipo="mg", fn=T.reloj("Anillo de Namira", 5, remate=("Precio: un sacerdote", 2)),
         de=("Cinco minutos. Te comiste", -.2), a=("Ni el peor menú del día te cobra tan caro|fin", .4),
         marcas=["Cinco minutos. Te comiste", ("Cinco minutos. Te comiste", 3.2), "Ni el peor menú"],   # 5:00 -> 0:00 en 3,2 s
         y=.50, sale=.4, nombre="MG reloj namira", ver=4.5),

    # ---- 2 · Mephala
    ficha("por su hijo menor, Nelkir", "Nelkir", "Oye una voz detrás de una puerta cerrada del sótano.",
          origen="Hijo menor del jarl Balgruuf", dur=6.0),
    ficha("te espera una espada", "Hoja de Ébano", "Absorbe *10* puntos de salud por golpe.", origen="Artefacto de Mephala"),
    dict(tipo="mg", fn=T.traiciones("Hoja de Ébano: traiciones", 10, 10, 4, 2),
         de=("Para que llegue a treinta", -.2), a=("como si narrara un partido|fin", .3),
         marcas=["Para que llegue a treinta", "Cada dos amigos asesinados", "En total son diez traiciones|fin"],
         y=.74, sale=.4, nombre="MG traiciones", ver=6.0),
    ficha("quedaron restos de un plan descartado", "Contenido descartado", "Los hijos de Balgruuf lo matan. "
          "Su hermano Hrongar se queda con el trono.", origen="Archivos del juego", dur=6.5),

    # ---- 1 · Boethiah
    ficha("El Sacellum de Boethiah", "Sacellum de Boethiah", "Nivel *30* para empezar.", origen="Noreste de Ventalia"),
    ficha("Los seguidores esenciales no activan", "Pilar del Sacrificio", "Los seguidores esenciales no lo activan.",
          origen="Regla de Boethiah", rojo=True, dur=5.5),
    ficha("te quedas con su cota de ébano", "Cota de ébano", "Pasos silenciosos. *5* de daño de veneno por segundo a quien "
          "se acerque.", origen="Artefacto de Boethiah", dur=7.5),
    ficha("sigue existiendo una segunda parte", "Contenido descartado", "Segunda parte: asesinar a Elisif la Bella, "
          "jarl de Soledad.", origen="Archivos del juego", rojo=True, dur=6.5),

    # ---- cierre: puente al video ya publicado
    ficha("tienes que ver el video", "Los 8 Príncipes Daédricos más poderosos de Skyrim", "Ya está en el canal.",
          origen="Video recomendado", dur=6.0, x=.5, y=.40),
]

SFX = {
    "mision_a": ("Deep nordic war drum hit with a short low horn swell, dark fantasy game quest notification", 3),
    "mision_b": ("Low ominous choir breath with a single deep drum hit, dark fantasy quest started sting", 3),
    "navaja": ("Sharp dagger unsheathing with a dark magical shimmer sting", 2),
    "reloj": ("Slow heavy clock ticking in a stone crypt, five ticks", 3),
    "caida": ("Muffled body falls onto a stone floor with a low thud", 1),
}
PISTAS = [
    dict(sfx="mision_a", en="las ocho misiones daédricas que", vol=.55),
    dict(sfx="mision_b", en="Número ocho. Empezamos", vol=.5),
    dict(sfx="mision_a", en="En el siete aparece", vol=.5),
    dict(sfx="mision_b", en="Número seis, y aquí", vol=.5),
    dict(sfx="mision_a", en="Bajando al cinco", vol=.5),
    dict(sfx="mision_b", en="Ahora sí, entramos", vol=.5),
    dict(sfx="mision_a", en="Número tres. En el Salón", vol=.5),
    dict(sfx="mision_b", en="Ya en el podio", vol=.5),
    dict(sfx="mision_a", en="Y llegamos al número uno", vol=.6),
    dict(sfx="navaja", en="más o menos dos por ciento", vol=.5),
    dict(sfx="reloj", en="Cinco minutos. Te comiste", vol=.45),
    dict(sfx="caida", en="Cada dos amigos asesinados", vol=.45),
]
