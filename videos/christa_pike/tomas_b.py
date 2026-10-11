# -*- coding: utf-8 -*-
"""Tomas del documental, segunda mitad: debate, camino, noche, despues, precedente, cierre."""
from kit_cp import *  # noqa: F401,F403
from tomas_a import A, NEG, SEP, C_W, C_F, C_N, C_5, C_A
from mg_esc import F_mg, OV  # noqa: F401
from mg_esc2 import OV_calendario  # noqa: F401
from mg_obj import cerebro, check  # noqa: F401
from mg import pr as _pr  # noqa: F401

FRIO = (0.55, 0.57, 0.66)

# ============================================================== DEBATE
Dd = "debate"
shot(INI(Dd, 0), F_mg("d_balanza"), [], [], ent=("tinta", 0.7))
_lista = [("Su", "edad", 330), ("Abuso", "abuso", 470), ("Enfermedades", "enfermedades", 610), ("Daño", "dano", 750)]
shot(INI(Dd, 1), F_pozo(0.35, 0.5, 0.95, (0.15, 0.12, 0.10)),
     [R(pk(Dd, 1, "nunca", "historia"), 1330, 190, 62, lineas=(3,)),
      S([("Su", A(Dd, 1, "edad", -0.3)), ("Edad", A(Dd, 1, "edad"))], 1330, 380, 80),
      S([("Abuso", A(Dd, 1, "abuso")), ("Sexual", A(Dd, 1, "abuso", 0.3)), ("Infantil", A(Dd, 1, "sufrio", 0.0))], 1330, 520, 80),
      S([("Enfermedades", A(Dd, 1, "enfermedades")), ("Mentales", A(Dd, 1, "mentales"))], 1330, 660, 80),
      S([("Daño", A(Dd, 1, "dano")), ("Cerebral", A(Dd, 1, "cerebral")), ("Congénito", A(Dd, 1, "congenito"))], 1330, 800, 80)],
     [OV(lambda p, t: cerebro(p, 1700, 800, 110, grieta=_pr(t, A(Dd, 1, "cerebral"), A(Dd, 1, "congenito", 0.8)), t=t) if t > A(Dd, 1, "enfermedades") else None),
      FRAME_CLIP("wbir_asesinato_1995", 560, 520, 700, 26.2, INI(Dd, 1) + 0.15, rot=-2, x_cont=(0.125, 0.875), fin=27.9),
      TAG("Según sus abogados", 560, 880, INI(Dd, 1) + 0.6, 44), CRED(C_W, INI(Dd, 1) + 0.3, FIN(Dd, 1))], ent=("fundido", 0.6))
shot(INI(Dd, 2), F_clip("wbir_cronologia", ini=13.9, fin=20.4, z0=1.0, z1=1.1, tono=(0.9, 0.9, 0.95)),
     [], [TAG("Amnistía Internacional", 560, 900, A(Dd, 2, "amnistia"), 46), TAG("Expertos de la ONU", 1400, 240, A(Dd, 2, "onu"), 46),
          CRED(C_W, INI(Dd, 2) + 0.3, FIN(Dd, 2))], ent=("fundido", 0.6))
shot(INI(Dd, 3), F_clip("nbc_ventilador", ini=60.0, fin=64.4, z0=1.0, z1=1.1, banner=0.2, tono=(0.9, 0.9, 0.95)),
     [R(pk(Dd, 3, "pagar"), W / 2, 880, 70)], [TAG("Familia de Colleen Slemmer", 1450, 120, A(Dd, 3, "familia"), 46), CRED(C_N, INI(Dd, 3) + 0.3, FIN(Dd, 3))],
     ent=("fundido", 0.7))
shot(INI(Dd, 4), F_clip("france24", ini=42.0, fin=45.8, z0=1.3, z1=1.22, c0=(0.56, 0.5), c1=(0.56, 0.5), tono=(0.85, 0.85, 0.9), sat=0.7),
     [], [CRED(C_F, INI(Dd, 4) + 0.3, FIN(Dd, 4))], ent=("fundido", 0.8), grado=dict(vineta=0.85))

# ============================================================== CAMINO
Ca = "camino"
shot(INI(Ca, 0), F_foto("tn_supreme", z0=1.05, z1=1.2, c0=(0.5, 0.55), c1=(0.5, 0.45), tono=(0.85, 0.85, 0.92)),
     [],
     [OV_calendario(A(Ca, 0, "fijo", 0.0), FIN(Ca, 0) - 0.4, 420, 560), TAG("Corte Suprema de Tennessee", 1300, 900, A(Ca, 0, "corte"), 46), CRED("Foto: Jon698 · Wikimedia Commons (CC BY-SA 4.0)", INI(Ca, 0) + 0.3, FIN(Ca, 0))],
     ent=("tinta", 0.7))
shot(INI(Ca, 1), F_mg("ca_intentos"),
     [S([("Mayo", A(Ca, 1, "mayo")), ("De", A(Ca, 1, "mayo", 0.3)), ("2026", A(Ca, 1, "mayo", 0.6))], 560, 230, 120),
      R(pk(Ca, 1, "mas", "hora"), W / 2, 1010, 70)], [], ent=("fundido", 0.6))
shot(INI(Ca, 2), F_mg("ca_sangre"), [], [], ent=("fundido", 0.6))


def _cartas_ca3(lz, t):
    t_l = INI(Ca, 3)
    carta(lz, pola("bill_lee3", 520, 1.22, (0.5, 0.35), "Gobernador Bill Lee"), I3, t, t_l, 520, 560, -4, desde=(-700, 0), dur=0.6)
    carta(lz, pola("scotus", 760, 0.74, (0.5, 0.5), "Corte Suprema"), I3, t, A(Ca, 3, "corte") - 0.1, 1330, 520, 3, desde=(700, 0), dur=0.6, fase=1.7)


shot(INI(Ca, 3), F_pozo(0.5, 0.5, 0.9, (0.14, 0.12, 0.11)),
     [N("28 · 09", 520, 190, 120, A(Ca, 3, "veintiocho")), N("29 · 09", 1330, 190, 120, A(Ca, 3, "dia", 0.0, 0))],
     [_cartas_ca3, SELLO("Clemencia negada", 520, 720, A(Ca, 3, "nego"), 54, -9), SELLO("Rechazado", 1330, 540, A(Ca, 3, "rechazo"), 66, -8),
      CRED("Fotos: Lynn Freeny (dominio público) · Kjetil Ree (CC BY-SA 3.0) · Wikimedia Commons", INI(Ca, 3) + 0.4, FIN(Ca, 3))], ent=("fundido", 0.6))
shot(INI(Ca, 4), F_borroso("sexto_circuito", 0.30),
     [N("30 · 09", W / 2, 150, 120, INI(Ca, 4) + 0.2)],
     [HERO("sexto_circuito", 610, 540, -3, alto=760, t_in=INI(Ca, 4) + 0.1, desde=(-900, 0)),
      HERO("scotus_ocaso", 1320, 540, 3, alto=620, t_in=A(Ca, 4, "horas") - 0.2, desde=(900, 0), ry=(8, 3)),
      SELLO("Suspendida", 610, 560, A(Ca, 4, "detuvo"), 62, -9), SELLO("Levantada", 1320, 560, A(Ca, 4, "levanto"), 62, -7),
      CRED("Fotos: Warren LeMay (CC0) · Joe Ravi (CC BY-SA 3.0) · Wikimedia Commons", INI(Ca, 4) + 0.4, FIN(Ca, 4))], ent=("fundido", 0.6))

# ============================================================== NOCHE
N_ = "noche"
G_ = dict(vineta=0.9)
shot(INI(N_, 0), F_mg("n_prision"),
     [], [RELOJ("6:41 p. m.", 1500, 300, 210, A(N_, 0, "seis")),
          TAG("Riverbend Maximum Security Institution", 700, 940, A(N_, 0, "prision"), 44)], ent=("tinta", 0.8), grado=G_)
shot(INI(N_, 1), F_mg("n_persianas"), [], [RELOJ("7:26 p. m.", 1700, 200, 150, A(N_, 1, "siete"))], ent=("fundido", 0.5), grado=G_)
snd(A(N_, 1, "persianas", -0.2), "persianas", 0.6)
shot(INI(N_, 2), F_mg("n_cancion"),
     [R([("«I'm", A(N_, 2, "amor", -0.6)), ("at", A(N_, 2, "amor", -0.45)), ("peace", A(N_, 2, "paz")), ("and", A(N_, 2, "paz", 0.3)),
         ("I'm", A(N_, 2, "paz", 0.45)), ("ready", A(N_, 2, "paz", 0.6)), ("to", A(N_, 2, "paz", 0.75)), ("go»", A(N_, 2, "paz", 0.9))], 600, 220, 66, lineas=(4,))],
     [TAG("Christa Pike · últimas palabras", 1400, 960, A(N_, 2, "amor", -0.6), 44)], ent=("fundido", 0.7), grado=G_)
shot(INI(N_, 3), F_mg("n_vena"),
     [R([("«The", A(N_, 3, "vena", -0.4)), ("vein", A(N_, 3, "vena")), ("in", A(N_, 3, "vena", 0.2)), ("my", A(N_, 3, "brazo", -0.3)), ("arm", A(N_, 3, "brazo")),
         ("feels", A(N_, 3, "brazo", 0.3)), ("like", A(N_, 3, "estaba", 0.0)), ("it's", A(N_, 3, "estaba", 0.3)), ("about", A(N_, 3, "punto", 0.0)),
         ("to", A(N_, 3, "punto", 0.3)), ("bust.»", A(N_, 3, "reventar"))], W / 2, 220, 62, lineas=(5,))],
     [RELOJ("7:34 p. m.", 1640, 1000, 130, A(N_, 3, "treinta")), TAG("Christa Pike", 480, 700, A(N_, 3, "se", 0.0), 44)],
     ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 4), F_ventana_piedra(A(N_, 4, "piedra", 0.05)),
     [], [RELOJ("7:41 p. m.", 470, 330, 190, A(N_, 4, "siete")), CRED("Recreación gráfica del detalle que describieron los testigos · no es una imagen real", INI(N_, 4) + 0.5, A(N_, 4, "pentobarbital") - 0.6)],
     ent=("tinta", 0.7), grado=G_)
shot(A(N_, 4, "pentobarbital", -0.8), F_mg("n_jeringa"), [], [], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 5), F_mg("n_reabre"), [], [RELOJ("7:46 p. m.", 1700, 200, 150, INI(N_, 5))], ent=("fundido", 0.4), grado=G_)
snd(A(N_, 5, "cerraron"), "persianas", 0.55)
snd(A(N_, 5, "abrieron", 0.1), "persianas", 0.5)
shot(INI(N_, 6), F_mg("n_cuenta"),
     [R(pk(N_, 6, "segunda", "dosis"), 1380, 960, 70)],
     [TEMPORIZADOR(A(N_, 6, "cinco", -0.1), A(N_, 6, "viva", 0.2), 1380, 250, 150)], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 7), F_mg("n_ronca"), [], [RELOJ("8:05 p. m.", 1620, 330, 170, INI(N_, 7))], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 8), F_mg("n_protocolo"), [], [], ent=("fundido", 0.6), grado=G_)
shot(INI(N_, 9), F_mg("n_ambulancia"), [], [], ent=("fundido", 0.5), grado=G_)

# ============================================================== DESPUES
De = "despues"
shot(INI(De, 0), F_mg("de_hospital"),
     [R(pk(De, 0, "estado", "critico"), W / 2, 960, 80)], [TAG("1 de octubre", 1560, 230, INI(De, 0) + 0.3, 48)], ent=("tinta", 0.7))
shot(INI(De, 1), F_mg("de_monitor"),
     [R([("Inconsciente", A(De, 1, "inconsciente"))], 560, 190, 80), R([("Respirador", A(De, 1, "respirador"))], 1400, 960, 80)],
     [TAG("2 de octubre · escrito judicial", 1470, 130, INI(De, 1) + 0.3, 42)], ent=("fundido", 0.6))
shot(INI(De, 2), F_vena(A(De, 2, "vias", -0.2)), [], [], ent=("tinta", 0.7))
shot(INI(De, 3), F_borroso("bill_lee3", 0.28),
     [S([("Profundamente", A(De, 3, "profundamente")), ("Perturbador", A(De, 3, "perturbador"))], 1330, 450, 98, lineas=(1,))],
     [HERO("bill_lee3", 600, 520, -3, alto=760, t_in=INI(De, 3) + 0.1, desde=(-800, 0)), TAG("Gobernador Bill Lee", 600, 960, INI(De, 3) + 0.5, 46),
      SELLO("Revisión independiente", 1330, 760, A(De, 3, "revision"), 60, -6),
      CRED("Foto: Lynn Freeny · Wikimedia Commons (dominio público)", INI(De, 3) + 0.4, FIN(De, 3))], ent=("fundido", 0.6))
shot(INI(De, 4), F_foto("capitolio_tn", z0=1.05, z1=1.2, c0=(0.5, 0.45), c1=(0.5, 0.4), par=(30, 0), tono=(0.85, 0.85, 0.92)),
     [N("3 · 10 · 2026", W / 2, 200, 150, A(De, 4, "sabado"))],
     [TAG("Frank Strada · Comisionado de Correcciones", 960, 900, A(De, 4, "frank"), 44), SELLO("Renuncia", 1450, 520, A(De, 4, "renuncia"), 70, -8),
      CRED("Foto: Kaldari · Wikimedia Commons (dominio público)", INI(De, 4) + 0.4, FIN(De, 4))], ent=("fundido", 0.6))
shot(INI(De, 5), F_mg("de_protocolo"),
     [R([("«Actuó", A(De, 5, "actuo")), ("conforme", A(De, 5, "conforme")), ("al", A(De, 5, "al")), ("protocolo»", A(De, 5, "protocolo"))], 1300, 220, 66, lineas=(2,))],
     [TAG("Frank Strada", 1460, 900, A(De, 5, "actuo"), 46)], ent=("fundido", 0.5))
shot(INI(De, 6), F_mg("de_sistema"),
     [R([("«Una", A(De, 6, "falla")), ("falla", A(De, 6, "falla")), ("sistémica»", A(De, 6, "sistemica"))], W / 2, 140, 80)],
     [TAG("Abogados de Christa Pike", 1560, 760, A(De, 6, "falla"), 46)], ent=("fundido", 0.5))
shot(INI(De, 7), F_clip("abc_ventilador", ini=72.9, fin=80.4, z0=1.0, z1=1.1, banner=0.22, tono=(0.9, 0.9, 0.94)),
     [], [TAG("May Martinez · madre de Colleen", 560, 900, INI(De, 7) + 0.4, 46), CRED(C_A, INI(De, 7) + 0.3, FIN(De, 7))], ent=("tinta", 0.7))
shot(INI(De, 8), F_clip("abc_ventilador", ini=64.2, fin=68.1, z0=1.0, z1=1.1, banner=0.22, tono=(0.8, 0.8, 0.84)),
     [R([("«Todo", A(De, 8, "queria", -0.5)), ("lo", A(De, 8, "queria", -0.35)), ("que", A(De, 8, "queria", -0.2)), ("quería", A(De, 8, "queria")),
         ("era", A(De, 8, "era")), ("justicia»", A(De, 8, "justicia"))], W / 2, 860, 62, lineas=(3,))],
     [CRED("Foto: AP · ABC News", INI(De, 8) + 0.3, FIN(De, 8))], ent=("fundido", 0.7), grado=dict(vineta=0.85))

# ============================================================== HISTORIAL (contexto: problemas previos de Tennessee con sus ejecuciones)
Hs = "historial"
_mh = [(2022.3, "Frena la ejecución de Oscar Smith", A(Hs, 1, "oscar"), (True, 120), "Abr. 2022"),
       (2025.0, "Se reanudan las ejecuciones", A(Hs, 2, "hasta"), (False, 120), "2025"),
       (2026.38, "Una ejecución se detiene: sin vía", A(Hs, 4, "segunda", -0.25), (True, 250), "May. 2026"),
       (2026.75, "Pike: dos dosis y sigue viva", A(Hs, 4, "fallida"), (False, 120), "30 sep. 2026")]
_lh = LINEA_ANOS(2021, 2027.2, 600, _mh, A(Hs, 1, "abril"), A(Hs, 2, "veinticinco", 0.2), 2022.3, 2025.0, x0=190, x1=1740,
                 etiqueta="Ejecuciones en Tennessee", paso=1, paso_lab=1)
shot(INI(Hs, 0), F_clip("newschannel5_hospital", ini=68.4, fin=73.4, z0=1.0, z1=1.12, banner=0.17, tono=(0.7, 0.72, 0.8)),
     [R([("Tennessee", A(Hs, 0, "tenesi")), ("ya", A(Hs, 0, "ya")), ("tenía", A(Hs, 0, "tenia"))], W / 2, 880, 80)],
     [CRED(C_5, INI(Hs, 0) + 0.3, FIN(Hs, 0))], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(INI(Hs, 1), F_mg("hs_prision"), [], [_lh], ent=("fundido", 0.7), grado=dict(vineta=0.9))
shot(INI(Hs, 3), F_mg("hs_cuatro"),
     [N("4", 1560, 200, 230, A(Hs, 3, "cuatro")), R(pk(Hs, 3, "personas"), 1560, 380, 62)], [_lh], ent=("fundido", 0.6), grado=dict(vineta=0.9))
shot(INI(Hs, 4), F_mg("hs_dos"), [R(pk(Hs, 4, "segunda", "fallida"), W / 2, 130, 78, lineas=(2,))], [], ent=("fundido", 0.6))
shot(INI(Hs, 5), F_mg("hs_vial"),
     [S([("Pentobarbital", A(Hs, 5, "pentobarbital"))], W / 2, 150, 118)],
     [TAG("Frank Strada · desde enero de 2023", 1330, 790, A(Hs, 5, "frank"), 46)], ent=("fundido", 0.6))

# ============================================================== PRECEDENTE
P = "precedente"
shot(INI(P, 0), F_mg("pr_busqueda"), [], [], ent=("tinta", 0.7))
shot(INI(P, 1), F_mg("pr_luisiana"),
     [N("1946", 420, 220, 260, A(P, 1, "mil"))],
     [lambda lz, t: carta(lz, pola("willie1", 520, 1.22, (0.5, 0.35), "Willie Francis"), I3, t, A(P, 1, "luisiana", 0.4), 1500, 560, 4, desde=(500, 0), dur=0.6),
      CRED("Foto: Bill Allen / AP · Wikimedia Commons (dominio público)", INI(P, 1) + 0.4, FIN(P, 1))], ent=("fundido", 0.6))
shot(INI(P, 2), F_borroso("willie2", 0.30),
     [S([("Sobrevivió", A(P, 2, "sobrevivio"))], 560, 880, 100)],
     [HERO("willie2", 1320, 520, 3, alto=840, t_in=INI(P, 2) + 0.1, desde=(800, 0)), TAG("Willie Francis · 17 años", 1320, 960, A(P, 2, "wili"), 46),
      CRED("Foto: International News Photos · Wikimedia Commons (dominio público)", INI(P, 2) + 0.4, FIN(P, 2))], ent=("fundido", 0.5))
shot(INI(P, 3), F_foto("scotus", z0=1.05, z1=1.18, c0=(0.5, 0.55), c1=(0.5, 0.45), par=(30, 0), tono=(0.85, 0.85, 0.92)),
     [N("1947", 1400, 240, 260, A(P, 3, "ano", 0.0))], [CRED("Foto: Kjetil Ree · Wikimedia Commons (CC BY-SA 3.0)", INI(P, 3) + 0.4, FIN(P, 3))], ent=("fundido", 0.6))
shot(INI(P, 4), F_foto("capitolio_tn", z0=1.05, z1=1.2, c0=(0.5, 0.5), c1=(0.5, 0.4), par=(30, 0), tono=(0.78, 0.78, 0.88)),
     [Q([[("Otro", A(P, 4, "otra", -0.2)), ("Intento", A(P, 4, "intentarlo"))]], A(P, 4, "otra") - 0.3, 1400, 560, 100)],
     [CRED("Foto: Kaldari · Wikimedia Commons (dominio público)", INI(P, 4) + 0.4, FIN(P, 4))], ent=("fundido", 0.6))
shot(INI(P, 5), F_mg("pr_abogados"), [R([("Impugnarlo", A(P, 5, "impugnarlo"))], W / 2, 980, 90)], [], ent=("fundido", 0.5))

# ============================================================== CIERRE
Ci = "cierre"
shot(INI(Ci, 0), F_mg("ci_ciudad"), [N("3 · 10 · 2026", 1300, 230, 170, A(Ci, 0, "tres"))], [], ent=("tinta", 0.8))
shot(INI(Ci, 1), F_mg("ci_sala"),
     [Q([[("Qué", A(Ci, 1, "que")), ("Falló", A(Ci, 1, "fallo"))], [("Esa", A(Ci, 1, "esa")), ("Noche", A(Ci, 1, "noche"))]], A(Ci, 1, "que") - 0.2, 1600, 520, 96)],
     [], ent=("fundido", 0.6))
shot(INI(Ci, 2), F_mg("ci_discuten"), [], [], ent=("fundido", 0.8))
_fin_voz = FIN(Ci, 3)
shot(INI(Ci, 3), F_mg("ci_vela"),
     [S([("Colleen", A(Ci, 3, "colin")), ("Slemmer", A(Ci, 3, "colin", 0.4))], 1610, 380, 96, lineas=(1,)),
      N("1975 – 1995", 1610, 600, 110, A(Ci, 3, "diecinueve", -0.3), color=BL)],
     [FRAME_CLIP("wbir_cronologia", 600, 520, 700, 301.3, INI(Ci, 3) + 0.3, rot=-2, fin=304.7), CRED(C_W, INI(Ci, 3) + 0.5, _fin_voz)], ent=("fundido", 1.0), grado=dict(vineta=0.9))
shot(_fin_voz + 1.0, F_negro(), [],
     [CREDITOS("Christa Pike: la ejecución que no terminó",
               ["Fuentes: Associated Press · CBS News · NBC News · ABC News · Newsweek · Al Jazeera · Fox 9 · Wikipedia",
                "Imágenes de archivo y noticias: WBIR (Knoxville) · France 24 · NBC News · ABC News · NewsChannel 5 · uso informativo",
                "Fotos (Wikimedia Commons): Kaldari, Cessna86, Jon698, Warren LeMay, Joe Ravi,",
                "Lynn Freeny, Quintin Soloviev, Bill Allen / AP",
                "Foto de ficha: Tennessee Department of Correction",
                "Animaciones y gráficos: producción propia · Música: Lyria",
                "Información al 3 de octubre de 2026. El caso sigue abierto."], _fin_voz + 1.6)], ent=("negro", 0.9))
construir()
