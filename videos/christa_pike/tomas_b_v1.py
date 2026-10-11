# -*- coding: utf-8 -*-
"""Tomas del documental, segunda mitad: debate, camino, noche, despues, precedente, cierre."""
from kit_cp import *  # noqa: F401,F403
from tomas_a import A, NEG, SEP, C_W, C_F, C_N, C_5, C_A

FRIO = (0.55, 0.57, 0.66)

# ============================================================== DEBATE
Dd = "debate"
shot(INI(Dd, 0), F_clip("stock/balanza_0", ini=1.0, z0=1.0, z1=1.18, c0=(0.55, 0.55), c1=(0.5, 0.5), tono=(0.78, 0.78, 0.82)),
     [], [], ent=("tinta", 0.7), grado=dict(vineta=0.8))
_lista = [("Su", "edad", 330), ("Abuso", "abuso", 470), ("Enfermedades", "enfermedades", 610), ("Daño", "dano", 750)]
shot(INI(Dd, 1), F_pozo(0.35, 0.5, 0.95, (0.15, 0.12, 0.10)),
     [R(pk(Dd, 1, "nunca", "historia"), 1330, 190, 62, lineas=(3,)),
      S([("Su", A(Dd, 1, "edad", -0.3)), ("Edad", A(Dd, 1, "edad"))], 1330, 380, 80),
      S([("Abuso", A(Dd, 1, "abuso")), ("Sexual", A(Dd, 1, "abuso", 0.3)), ("Infantil", A(Dd, 1, "sufrio", 0.0))], 1330, 520, 80),
      S([("Enfermedades", A(Dd, 1, "enfermedades")), ("Mentales", A(Dd, 1, "mentales"))], 1330, 660, 80),
      S([("Daño", A(Dd, 1, "dano")), ("Cerebral", A(Dd, 1, "cerebral")), ("Congénito", A(Dd, 1, "congenito"))], 1330, 800, 80)],
     [FRAME_CLIP("wbir_asesinato_1995", 560, 520, 700, 26.2, INI(Dd, 1) + 0.15, rot=-2, x_cont=(0.125, 0.875), fin=27.9),
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
     [N("30 · 09 · 2025", 560, 230, 120, A(Ca, 0, "treinta")), N("30 · 09 · 2026", 1360, 230, 120, A(Ca, 0, "ano"))],
     [TAG("Corte Suprema de Tennessee", 960, 900, A(Ca, 0, "corte"), 46), CRED("Foto: Jon698 · Wikimedia Commons (CC BY-SA 4.0)", INI(Ca, 0) + 0.3, FIN(Ca, 0))],
     ent=("tinta", 0.7))
shot(INI(Ca, 1), F_clip("newschannel5_hospital", ini=285.2, fin=288.4, z0=1.0, z1=1.12, banner=0.17, tono=FRIO),
     [S([("Mayo", A(Ca, 1, "mayo")), ("De", A(Ca, 1, "mayo", 0.3)), ("2026", A(Ca, 1, "mayo", 0.6))], 560, 240, 120),
      R(pk(Ca, 1, "mas", "hora"), W / 2, 890, 82)], [CRED(C_5, INI(Ca, 1) + 0.3, FIN(Ca, 1))], ent=("fundido", 0.6))
shot(INI(Ca, 2), F_clip("stock/hospital_0", ini=1.0, z0=1.0, z1=1.15, tono=FRIO),
     [R(pk(Ca, 2, "historial", "medico"), W / 2, 860, 90)], [], ent=("fundido", 0.6), grado=dict(vineta=0.8))


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
shot(INI(N_, 0), F_clip("newschannel5_hospital", ini=73.7, fin=74.9, z0=1.0, z1=1.12, banner=0.17, tono=(0.34, 0.37, 0.52)),
     [], [RELOJ("6:41 p. m.", 1400, 420, 210, A(N_, 0, "seis")),
          TAG("Riverbend Maximum Security Institution", 700, 900, A(N_, 0, "prision"), 44),
          CRED(C_5, INI(N_, 0) + 0.3, FIN(N_, 0))], ent=("tinta", 0.8), grado=G_)
shot(INI(N_, 1), F_clip("france24", ini=9.0, fin=13.2, z0=1.0, z1=1.08, tono=(0.85, 0.85, 0.95)),
     [], [PERSIANAS(INI(N_, 1) - 2.0, A(N_, 1, "abrieron", -0.15), 1.0), RELOJ("7:26 p. m.", 1450, 330, 210, A(N_, 1, "siete")),
          CRED(C_F, INI(N_, 1) + 1.0, FIN(N_, 1))], ent=("fundido", 0.5), grado=G_)
snd(A(N_, 1, "abrieron", -0.1), "persianas", 0.6)
shot(INI(N_, 2), F_clip("stock/lluvia_ventana_2", ini=1.0, z0=1.0, z1=1.18, tono=(0.8, 0.82, 0.9)),
     [R([("«I'm", A(N_, 2, "amor", -0.6)), ("at", A(N_, 2, "amor", -0.45)), ("peace", A(N_, 2, "paz")), ("and", A(N_, 2, "paz", 0.3)),
         ("I'm", A(N_, 2, "paz", 0.45)), ("ready", A(N_, 2, "paz", 0.6)), ("to", A(N_, 2, "paz", 0.75)), ("go»", A(N_, 2, "paz", 0.9))], W / 2, 500, 78, lineas=(4,))],
     [TAG("Christa Pike · últimas palabras", 1400, 880, A(N_, 2, "amor", -0.6), 44)], ent=("fundido", 0.7), grado=G_)
shot(INI(N_, 3), F_clip("france24", ini=10.0, fin=13.0, z0=1.5, z1=1.7, c0=(0.42, 0.72), c1=(0.44, 0.72), tono=(0.75, 0.55, 0.55)),
     [R([("«The", A(N_, 3, "vena", -0.4)), ("vein", A(N_, 3, "vena")), ("in", A(N_, 3, "vena", 0.2)), ("my", A(N_, 3, "brazo", -0.3)), ("arm", A(N_, 3, "brazo")),
         ("feels", A(N_, 3, "brazo", 0.3)), ("like", A(N_, 3, "estaba", 0.0)), ("it's", A(N_, 3, "estaba", 0.3)), ("about", A(N_, 3, "punto", 0.0)),
         ("to", A(N_, 3, "punto", 0.3)), ("bust.»", A(N_, 3, "reventar"))], W / 2, 860, 62, lineas=(5,))],
     [RELOJ("7:34 p. m.", 1500, 250, 190, A(N_, 3, "treinta")), TAG("Christa Pike", 480, 250, A(N_, 3, "se", 0.0), 44), CRED(C_F, INI(N_, 3) + 0.3, FIN(N_, 3))],
     ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 4), F_ventana_piedra(A(N_, 4, "piedra", 0.05)),
     [], [RELOJ("7:41 p. m.", 470, 330, 190, A(N_, 4, "siete")), CRED("Recreación gráfica del detalle que describieron los testigos · no es una imagen real", INI(N_, 4) + 0.5, A(N_, 4, "pentobarbital") - 0.6)],
     ent=("tinta", 0.7), grado=G_)
shot(A(N_, 4, "pentobarbital", -0.8), F_clip("newschannel5_hospital", ini=288.8, fin=292.0, z0=1.0, z1=1.12, banner=0.17, tono=(0.85, 0.8, 0.8)),
     [S([("Pentobarbital", A(N_, 4, "pentobarbital"))], W / 2, 250, 120)], [CRED(C_5, A(N_, 4, "pentobarbital") - 0.8, FIN(N_, 4))], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 5), F_clip("france24", ini=9.5, fin=13.5, z0=1.0, z1=1.1, tono=(0.8, 0.8, 0.9)),
     [], [PERSIANAS(A(N_, 5, "cerraron", -0.1), A(N_, 5, "abrieron", 0.1), 0.8), RELOJ("7:46 p. m.", 1450, 330, 210, INI(N_, 5)),
          CRED(C_F, INI(N_, 5) + 0.3, FIN(N_, 5))], ent=("fundido", 0.4), grado=G_)
snd(A(N_, 5, "cerraron"), "persianas", 0.55)
snd(A(N_, 5, "abrieron", 0.1), "persianas", 0.5)
shot(INI(N_, 6), F_clip("stock/reloj_2", ini=2.0, z0=1.0, z1=1.2, tono=(0.58, 0.6, 0.7)),
     [R(pk(N_, 6, "segunda", "dosis"), W / 2, 890, 90)],
     [TEMPORIZADOR(A(N_, 6, "cinco", -0.1), A(N_, 6, "viva", 0.2), 520, 420, 230)], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 7), F_clip("france24", ini=12.9, fin=16.4, z0=1.0, z1=1.05, tono=(0.8, 0.8, 0.9)),
     [R([("Roncaba", A(N_, 7, "roncaba"))], 960, 880, 100)], [RELOJ("8:05 p. m.", 1450, 330, 210, INI(N_, 7))], ent=("fundido", 0.5), grado=G_)
shot(A(N_, 7, "periodistas", -0.3), F_clip("nbc_ventilador", ini=41.0, fin=44.6, z0=1.0, z1=1.1, banner=0.2, tono=(0.7, 0.72, 0.85)),
     [R([("Roncaba", A(N_, 7, "roncaba"))], W / 2, 890, 100)], [CRED(C_N, A(N_, 7, "periodistas") - 0.3, FIN(N_, 7))], ent=("fundido", 0.5), grado=G_)
shot(INI(N_, 8), F_clip("stock/pasillo_oscuro_0", ini=2.0, z0=1.0, z1=1.2, tono=(0.7, 0.72, 0.82)),
     [R(pk(N_, 8, "protocolo", "hacer"), W / 2, 540, 92, lineas=(3,))], [], ent=("fundido", 0.6), grado=G_)
shot(INI(N_, 9), F_clip("nbc_ventilador", ini=45.0, fin=49.4, z0=1.0, z1=1.1, banner=0.2, tono=(0.8, 0.8, 0.9)),
     [], [CRED(C_N, INI(N_, 9) + 0.2, FIN(N_, 9))], ent=("fundido", 0.5), grado=G_)

# ============================================================== DESPUES
De = "despues"
shot(INI(De, 0), F_clip("stock/hospital_1", ini=1.0, z0=1.0, z1=1.18, tono=FRIO),
     [R(pk(De, 0, "estado", "critico"), W / 2, 860, 92)], [TAG("1 de octubre", 1560, 230, INI(De, 0) + 0.3, 48)], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(INI(De, 1), F_clip("stock/monitor_cardiaco_1", ini=1.0, z0=1.0, z1=1.15, tono=(0.7, 0.76, 0.8)),
     [R([("Inconsciente", A(De, 1, "inconsciente"))], 560, 270, 88), R([("Respirador", A(De, 1, "respirador"))], 1360, 820, 88)],
     [TAG("2 de octubre · escrito judicial", 1470, 230, INI(De, 1) + 0.3, 42)], ent=("fundido", 0.6), grado=dict(vineta=0.85))
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
shot(INI(De, 5), F_clip("stock/documento_1", ini=1.0, z0=1.0, z1=1.12, tono=(0.5, 0.5, 0.55), sat=0.6),
     [R([("«Actuó", A(De, 5, "actuo")), ("conforme", A(De, 5, "conforme")), ("al", A(De, 5, "al")), ("protocolo»", A(De, 5, "protocolo"))], W / 2, 500, 96, lineas=(2,))],
     [TAG("Frank Strada", 1460, 800, A(De, 5, "actuo"), 46)], ent=("fundido", 0.5), grado=dict(vineta=0.9))
shot(INI(De, 6), F_clip("stock/pasillo_oscuro_3", ini=2.0, z0=1.0, z1=1.12, tono=(0.55, 0.57, 0.66)),
     [R([("«Una", A(De, 6, "falla")), ("falla", A(De, 6, "falla")), ("sistémica»", A(De, 6, "sistemica"))], W / 2, 400, 110),
      R(pk(De, 6, "que", "persona"), W / 2, 620, 62, lineas=(5,))],
     [TAG("Abogados de Christa Pike", 1400, 900, A(De, 6, "falla"), 46)], ent=("fundido", 0.5), grado=dict(vineta=0.9))
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
shot(INI(Hs, 1), F_clip("stock/alambre_1", ini=3.0, z0=1.0, z1=1.12, tono=(0.5, 0.52, 0.6)), [], [_lh], ent=("fundido", 0.7), grado=dict(vineta=0.9))
shot(INI(Hs, 3), F_clip("stock/pasillo_oscuro_3", ini=3.0, z0=1.0, z1=1.12, tono=(0.55, 0.57, 0.66)),
     [N("4", 1560, 200, 230, A(Hs, 3, "cuatro")), R(pk(Hs, 3, "personas"), 1560, 380, 62)], [_lh], ent=("fundido", 0.6), grado=dict(vineta=0.9))
shot(INI(Hs, 4), F_clip("stock/documento_1", ini=2.0, z0=1.0, z1=1.12, tono=(0.5, 0.5, 0.56), sat=0.6),
     [R(pk(Hs, 4, "segunda", "fallida"), W / 2, 170, 78, lineas=(2,))], [_lh],
     ent=("fundido", 0.6), grado=dict(vineta=0.9))
shot(INI(Hs, 5), F_clip("newschannel5_hospital", ini=288.8, fin=292.1, z0=1.0, z1=1.12, banner=0.17, tono=(0.8, 0.78, 0.78)),
     [S([("Pentobarbital", A(Hs, 5, "pentobarbital"))], W / 2, 250, 118)],
     [TAG("Frank Strada · desde enero de 2023", 560, 900, A(Hs, 5, "frank"), 46), CRED(C_5, INI(Hs, 5) + 0.3, FIN(Hs, 5))], ent=("fundido", 0.6), grado=dict(vineta=0.85))

# ============================================================== PRECEDENTE
P = "precedente"
shot(INI(P, 0), F_clip("stock/documento_2", ini=3.0, z0=1.0, z1=1.15, tono=(0.62, 0.62, 0.66), sat=0.7),
     [R(pk(P, 0, "no", "igual"), W / 2, 860, 84, lineas=(3,))], [], ent=("tinta", 0.7), grado=dict(vineta=0.85))
shot(INI(P, 1), F_borroso("willie1", 0.30),
     [N("1946", 1400, 440, 320, A(P, 1, "mil"))],
     [HERO("willie1", 600, 530, -3, alto=820, t_in=INI(P, 1) + 0.1, desde=(-800, 0)), TAG("Luisiana", 1400, 700, A(P, 1, "luisiana"), 54),
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
shot(INI(P, 5), F_clip("stock/mazo_2", ini=1.0, z0=1.0, z1=1.15, tono=(1.5, 1.45, 1.4)),
     [R([("Impugnarlo", A(P, 5, "impugnarlo"))], W / 2, 870, 100)], [], ent=("fundido", 0.5), grado=dict(vineta=0.85))

# ============================================================== CIERRE
Ci = "cierre"
shot(INI(Ci, 0), F_clip("stock/ciudad_noche_0", ini=1.0, z0=1.0, z1=1.15, tono=(1.5, 1.5, 1.8)),
     [N("3 · 10 · 2026", W / 2, 260, 170, A(Ci, 0, "tres"))], [], ent=("tinta", 0.8), grado=dict(vineta=0.85))
shot(INI(Ci, 1), F_clip("stock/pasillo_oscuro_2", ini=1.0, z0=1.0, z1=1.15, tono=(0.7, 0.72, 0.82)),
     [Q([[("Qué", A(Ci, 1, "que")), ("Falló", A(Ci, 1, "fallo"))], [("Esa", A(Ci, 1, "esa")), ("Noche", A(Ci, 1, "noche"))]], A(Ci, 1, "que") - 0.2, W / 2, 560, 96)],
     [], ent=("fundido", 0.6), grado=dict(vineta=0.9))
shot(INI(Ci, 2), F_clip("stock/carretera_noche_0", ini=1.0, z0=1.0, z1=1.12, tono=(1.3, 1.3, 1.5)),
     [], [], ent=("fundido", 0.8), grado=dict(vineta=0.9))
_fin_voz = FIN(Ci, 3)
shot(INI(Ci, 3), F_clip("stock/vela_3", ini=1.0, z0=1.4, z1=1.4, c0=(0.40, 0.5), c1=(0.40, 0.5), tono=(0.9, 0.85, 0.8)),
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
                "Video de apoyo: Pexels · Música: Lyria",
                "Información al 3 de octubre de 2026. El caso sigue abierto."], _fin_voz + 1.6)], ent=("negro", 0.9))
construir()
