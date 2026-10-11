# -*- coding: utf-8 -*-
"""Estilos visuales intercambiables. Un estilo cambia tinta, rellenos, temblor, bordes, texturas,
brillo y fondos por defecto SIN tocar la coreografía de las escenas.

Uso: en guion.py -> ESTILO_VISUAL = "pizarra"   (o variable de entorno FAB_ESTILO para probar)
Para crear uno nuevo: copiar una entrada de ESTILOS y ajustar valores.
"""

ESTILOS = {
    "doodle_psicodelico": dict(
        descripcion="Marcador doodle con stickers (borde blanco + sombra) sobre fondos psicodélicos.",
        tinta=None, relleno=None, wob=2.0, sticker=True, borde_sticker=(255, 251, 242), grosor_sticker=13,
        sombra=0.38, textura_trazo=0.0, brillo_neon=0.0, grano=0.035, vineta=True,
        fondos=dict(titulo=("rayos", dict(n=14, vel=0.05)), antes=("cueva", dict(tinte=0.5)),
                    hoy=("rejilla", {}), libre=("plasma", {}))),
    "doodle": dict(
        descripcion="Marcador doodle con stickers (borde blanco + sombra) sobre fondos naturales y calmados: "
                    "roca de cueva sin brillos de color, ocre plano y azul suave. Sin efectos psicodélicos.",
        tinta=None, relleno=None, wob=2.0, sticker=True, borde_sticker=(255, 251, 242), grosor_sticker=13,
        sombra=0.38, textura_trazo=0.0, brillo_neon=0.0, grano=0.035, vineta=True,
        hue_rango=(0.02, 0.14),     # los colores que recorren el arcoíris se quedan en naranja-amarillo
        camiseta_tu=(84, 150, 216),  # el personaje 'tu' lleva camiseta lisa (no arcoíris con espiral)
        fondos=dict(titulo=("plano", dict(pal="ocre")), antes=("cueva", dict(tinte=0.0)),
                    hoy=("plano", dict(pal="oceano")), libre=("plano", dict(pal="ocre")))),
    "pizarra": dict(
        descripcion="Tiza blanca sobre pizarra verde: trazos granulados, rellenos pastel, sin stickers.",
        tinta=(238, 238, 228), relleno="pastel", wob=1.4, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.36, brillo_neon=0.0, grano=0.05, vineta=True,
        fondos=dict(titulo=("pizarra", dict(tono=0)), antes=("pizarra", dict(tono=0)),
                    hoy=("pizarra", dict(tono=1)), libre=("pizarra", dict(tono=0)))),
    "cuaderno": dict(
        descripcion="Bolígrafo azul en cuaderno rayado, rellenos tipo acuarela clara.",
        tinta=(28, 48, 130), relleno="acuarela", wob=2.4, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.12, textura_trazo=0.15, brillo_neon=0.0, grano=0.03, vineta=True,
        fondos=dict(titulo=("liso", {}), antes=("liso", {}), hoy=("liso", dict(color=(0.93, 0.96, 0.99))),
                    libre=("liso", {}))),
    "neon": dict(
        descripcion="Contornos de neón brillantes sobre fondos oscuros tipo synthwave.",
        tinta=(90, 240, 255), relleno="oscuro", wob=1.2, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.9, grano=0.02, vineta=True,
        fondos=dict(titulo=("tunel", dict(pal="neon", vel=0.6)), antes=("cosmos", {}), hoy=("rejilla", {}),
                    libre=("cosmos", {}))),
    "recortes": dict(
        descripcion="Papel recortado: borde blanco grueso, sombra marcada, poco temblor, fondo kraft.",
        tinta=(45, 35, 30), relleno="mate", wob=0.8, sticker=True, borde_sticker=(250, 246, 236), grosor_sticker=21,
        sombra=0.55, textura_trazo=0.0, brillo_neon=0.0, grano=0.05, vineta=True, fps_mov=15,
        fondos=dict(titulo=("cartulina", {}), antes=("kraft", {}), hoy=("cartulina", dict(claro=1)),
                    libre=("kraft", {}))),
    "limpio": dict(
        descripcion="Vector plano y limpio: sin temblor, sin grano, colores planos (explicativo/corporativo).",
        tinta=(40, 40, 52), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.18, textura_trazo=0.0, brillo_neon=0.0, grano=0.0, vineta=False,
        fondos=dict(titulo=("plano", dict(pal="arcoiris")), antes=("plano", dict(pal="oceano")),
                    hoy=("plano", dict(pal="chicle")), libre=("plano", {}))),
    "vox": dict(
        descripcion="Explicativo tipo Vox: papel recortado sobre mesa de papel, sombras marcadas, movimiento en dos "
                    "(12 cuadros/s), mapas, rotulación gruesa y marcador amarillo (usar con nucleo/vox.py).",
        tinta=(40, 30, 26), relleno=None, wob=0.6, sticker=True, borde_sticker=(247, 241, 228), grosor_sticker=9,
        sombra=0.5, textura_trazo=0.0, brillo_neon=0.0, grano=0.045, vineta=True, fps_mov=12,
        texto_fijo=True,
        fondos=dict(titulo=("papel", {}), antes=("papel", {}), hoy=("papel", {}), libre=("papel", {}))),
    "boceto": dict(
        descripcion="Boceto a mano sobre papel crema: cada elemento se dibuja trazo a trazo (tinta que hierve a 12 cuadros/s) "
                    "y se colorea con crayón desfasado; los objetos se borran o caen para dar paso al siguiente; letra "
                    "manuscrita palabra por palabra (usar con nucleo/boceto.py). Pensado para bucles.",
        tinta=(28, 26, 30), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.0, grano=0.0, vineta=False, fps_mov=12,
        texto_fijo=True, subs_propios=True,
        fondos=dict(titulo=("liso", {}), antes=("liso", {}), hoy=("liso", {}), libre=("liso", {}))),
    "documental": dict(
        descripcion="Documental de misterio tipo 'Detrás del Enigma': fotos y escaneos con parallax 2.5D, polaroids, tablero "
                    "de evidencias, mapas, texto serif amarillo/blanco sincronizado con la voz, viñeta y grano "
                    "(usar con nucleo/docu.py; la clase Mundo devuelve el cuadro completo).",
        tinta=(20, 16, 14), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.0, grano=0.0, vineta=False,
        texto_fijo=True, subs_propios=True,
        fondos=dict(titulo=("liso", {}), antes=("liso", {}), hoy=("liso", {}), libre=("liso", {}))),
    "kurzgesagt": dict(
        descripcion="Vector plano tipo Kurzgesagt: sin contornos ni temblor, colores vivos, degradados y halos "
                    "sobre fondos espaciales oscuros (usar con nucleo/plano.py).",
        tinta=(26, 24, 52), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.0, grano=0.016, vineta=True,
        sin_contorno=True,     # los trazos de tinta (NEGRO) no se dibujan: solo rellenos
        texto_fijo=True,       # el texto no tiembla
        bloom=0.32,            # resplandor suave de lo muy luminoso (en efectos.acabado)
        fondos=dict(titulo=("espacio", {}), antes=("espacio", dict(tono=1)), hoy=("degradado", {}),
                    libre=("espacio", {}))),
    "cartoon90": dict(
        descripcion="Dibujo animado de los 90 (ref. «Coraje el perro cobarde»): tinta gruesa de grosor variable que se vuelve a "
                    "trazar a 12 dibujos/s, formas elásticas cuadro a cuadro (squash/stretch, smears, acción superpuesta), "
                    "relleno de celda con sombra de 2 tonos, fondos pintados, luz dramática y grano (usar con nucleo/toon.py; "
                    "la clase Mundo devuelve el cuadro completo).",
        tinta=(24, 18, 26), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.0, grano=0.0, vineta=False,
        texto_fijo=True, subs_propios=True,
        fondos=dict(titulo=("liso", {}), antes=("liso", {}), hoy=("liso", {}), libre=("liso", {}))),
    "noir": dict(
        descripcion="Cine negro en tinta y aguada (novela gráfica vintage): SOLO blanco y negro de alto contraste, claroscuro, "
                    "lluvia, niebla, humo, sombras de persiana; tinta que se redibuja a 12 dibujos/s sobre papel (usar con "
                    "nucleo/noir.py sobre nucleo/toon.py; cada escena devuelve el cuadro completo).",
        tinta=(12, 12, 12), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.0, grano=0.0, vineta=False,
        texto_fijo=True, subs_propios=True,
        fondos=dict(titulo=("liso", {}), antes=("liso", {}), hoy=("liso", {}), libre=("liso", {}))),
    "noir_feudal": dict(
        descripcion="Noir a color en época feudal (docs/estilo_noir_color.md § Variante FEUDAL): tinta y aguada con color oscuro "
                    "y apagado (antorcha/vela contra luna, un acento), pesquisidor encapuchado y corte medieval (usar con "
                    "nucleo/noir_color.py + noir_feudal.py + noir_corte.py; cada escena devuelve el cuadro completo).",
        tinta=(12, 12, 12), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.0, grano=0.0, vineta=False,
        texto_fijo=True, subs_propios=True,
        fondos=dict(titulo=("liso", {}), antes=("liso", {}), hoy=("liso", {}), libre=("liso", {}))),
    "guache": dict(
        descripcion="Ilustración de libro infantil en gouache (ref. «Economía de la isla»): paleta apagada y cálida, sin "
                    "contornos ni temblor, personajes de cabeza redonda con ojos de punto, grano y fibra de papel (usar con "
                    "nucleo/guache.py).",
        tinta=(62, 48, 52), relleno=None, wob=0.0, sticker=False, borde_sticker=None, grosor_sticker=13,
        sombra=0.0, textura_trazo=0.0, brillo_neon=0.0, grano=0.022, vineta=True,
        sin_contorno=True, texto_fijo=True,
        papel=0.55,            # textura de papel de acuarela/gouache + tinte cálido (en efectos.acabado)
        fondos=dict(titulo=("liso", dict(color=(0.93, 0.89, 0.79))), antes=("liso", dict(color=(0.93, 0.89, 0.79))),
                    hoy=("liso", dict(color=(0.93, 0.89, 0.79))), libre=("liso", dict(color=(0.93, 0.89, 0.79))))),
}

ACTUAL = ESTILOS["doodle_psicodelico"]
NOMBRE = "doodle_psicodelico"


def activar(nombre):
    global ACTUAL, NOMBRE
    if nombre not in ESTILOS:
        raise KeyError(f"Estilo '{nombre}' no existe. Opciones: {', '.join(ESTILOS)}")
    ACTUAL = ESTILOS[nombre]
    NOMBRE = nombre
    return ACTUAL


def transformar_relleno(rgb):
    """Transforma un color de relleno según el estilo activo (la tinta se trata aparte)."""
    modo = ACTUAL["relleno"]
    r, g, b = rgb
    if modo is None:
        return rgb
    if modo == "pastel":
        return (int(0.55 * r + 0.45 * 225), int(0.55 * g + 0.45 * 225), int(0.55 * b + 0.45 * 215))
    if modo == "acuarela":
        return (int(0.5 * r + 0.5 * 250), int(0.5 * g + 0.5 * 248), int(0.5 * b + 0.5 * 240))
    if modo == "oscuro":
        return (int(0.3 * r + 8), int(0.3 * g + 6), int(0.3 * b + 18))
    if modo == "mate":
        gris = (r + g + b) / 3
        return (int(0.8 * r + 0.2 * gris), int(0.8 * g + 0.2 * gris), int(0.8 * b + 0.2 * gris))
    return rgb
