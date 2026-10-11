# -*- coding: utf-8 -*-
"""Tomas del documental, primera mitad: gancho, quien, colleen, crimen, juicio, corredor. Los tiempos salen de la voz (anclas por palabra)."""
from kit_cp import *  # noqa: F401,F403
from mg_esc import F_mg, OV, ecg_pulso  # noqa: F401
import mg_esc2, mg_esc3, mg_esc4  # noqa: F401  (registran las escenas dibujadas)
from mg_esc2 import OV_calendario  # noqa: F401
from mg_obj import reloj  # noqa: F401

NEG = (0.62, 0.64, 0.72)          # tono frío y oscuro para la noche
SEP = (0.95, 0.86, 0.72)          # tono de archivo cálido


def A(e, fr, k, off=0.0, nth=0):
    return ww(e, fr, k, nth, off)


C_W = "Imagen: WBIR (Knoxville)"
C_F = "Imagen: France 24"
C_N = "Imagen: NBC News"
C_5 = "Imagen: NewsChannel 5 (Nashville)"
C_A = "Imagen: ABC News"

# ============================================================== GANCHO
G = "gancho"
shot(0.0, F_foto("nashville_noche", z0=1.06, z1=1.2, c0=(0.5, 0.62), c1=(0.5, 0.5), par=(40, 0), tono=(0.88, 0.88, 1.0)),
     [S([("Nashville,", A(G, 0, "nashvil")), ("Tennessee", A(G, 0, "tenesi"))], W / 2, 270, 118),
      R([("Miércoles", A(G, 0, "miercoles")), ("30", A(G, 0, "treinta")), ("de", A(G, 0, "de")), ("septiembre", A(G, 0, "septiembre")),
         ("de", A(G, 0, "de", 0.0, 1)), ("2026", A(G, 0, "veintiseis"))], W / 2, 880, 80, lineas=(3,))],
     [CRED("Foto: Cessna86 · Wikimedia Commons (dominio público)", 0.9, 4.0)], ent=("fundido", 0.01))
shot(INI(G, 1), F_mg("g_camilla"),
     [N("50", 1480, 260, 230, A(G, 1, "cincuenta")), R([("años", A(G, 1, "anos"))], 1480, 440, 76)], [], ent=("fundido", 0.6))
shot(INI(G, 2), F_mg("g_testigos"), [], [], ent=("fundido", 0.6))
shot(INI(G, 3), F_mg("g_dosis"),
     [R(pk(G, 3, "una", "dosis"), W / 2, 100, 80, lineas=None)], [], ent=("fundido", 0.5))
shot(INI(G, 4), F_mg("g_nadie"),
     [Q([[("Nadie", A(G, 4, "nadie")), ("sabe", A(G, 4, "sabe"))], [("explicar", A(G, 4, "explicar"))]], A(G, 4, "nadie") - 0.1, 960, 560, 96)],
     [], ent=("fundido", 0.5))


def _ficha(lz, t):
    t_in = INI(G, 5)
    sp = pola("pike_ficha_usuario", 780, 0.78, (0.5, 0.45), lado=1200)
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.10, W / 2, H / 2 + 20, 0.0), 6.0, mano=0.6)(t - t_in)
    u = e_out(prog(t, t_in, t_in + 0.9))
    D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, W / 2, lerp(340, 450, u), lerp(1.2, 1.0, u), lerp(4, -1, u), lerp(-24, -3, u)), smooth(prog(t, t_in, t_in + 0.4)))


shot(INI(G, 5), F_pozo(0.5, 0.48, 0.9, (0.16, 0.13, 0.11)),
     [R(pk(G, 5, "sigue", "respirando"), W / 2, 960, 82)],
     [_ficha, OV(ecg_pulso), TAG("Christa Pike", 560, 250, A(G, 5, "crista"), 50, -4),
      CRED("Foto: Tennessee Department of Correction", INI(G, 5) + 0.5, FIN(G, 5) + 1.5)], ent=("fundido", 0.6), grado=dict(vineta=0.85))
snd(0.3, "latido", 0.55, dur=1.6)
snd(A(G, 5, "sigue", -0.1), "latido", 0.7, dur=1.4)

# ============================================================== QUIEN
Qn = "quien"
shot(INI(Qn, 0), F_mg("q_atras"), [R(pk(Qn, 0, "volver", "atras"), W / 2, 960, 70)], [], ent=("tinta", 0.7))
shot(INI(Qn, 1), F_mg("q_montanas"),
     [N("1976", 560, 330, 290, A(Qn, 1, "mil"))], [TAG("Christa Pike", 1380, 880, A(Qn, 1, "crista"), 52)], ent=("fundido", 0.6))
shot(A(Qn, 1, "virginia", -0.25), F_foto("beckley", z0=1.05, z1=1.2, c0=(0.5, 0.55), c1=(0.55, 0.45), par=(40, 0), tono=(0.9, 0.9, 0.96)),
     [S([("Virginia", A(Qn, 1, "virginia")), ("Occidental", A(Qn, 1, "occidental"))], 540, 870, 108)],
     [TAG("Beckley", 1500, 230, A(Qn, 1, "virginia"), 48), CRED("Foto: Quintin Soloviev · Wikimedia Commons (CC BY 4.0)", A(Qn, 1, "virginia"), FIN(Qn, 1))], ent=("fundido", 0.5))
_cl = [(INI(Qn, 2), 1.35, -81.6, 37.0), (A(Qn, 3, "mil", 0.3), 1.45, -82.3, 36.6), (FIN(Qn, 3), 1.55, -82.5, 36.4)]
shot(INI(Qn, 2),
     MAPA(_cl, marcas=[("Beckley", INI(Qn, 2)), ("Swannanoa", A(Qn, 2, "carolina")), ("Knoxville", A(Qn, 3, "mil", 0.9))],
          rutas=[("Beckley", "Swannanoa", A(Qn, 2, "centro"), A(Qn, 2, "centro", 1.7)), ("Swannanoa", "Knoxville", A(Qn, 3, "mil", 0.2), A(Qn, 3, "mil", 1.9))]),
     [N("1991", 1450, 260, 230, A(Qn, 2, "mil"), sal=A(Qn, 3, "mil", -0.2)),
      N("1993", 1450, 260, 230, A(Qn, 3, "mil"))],
     [CRED("Mapa: elevación AWS Terrain (dominio público) · límites Natural Earth", INI(Qn, 2) + 0.3, A(Qn, 3, "programa", -0.3))],
     ent=("fundido", 0.5), grado=dict(vineta=0.75))
shot(A(Qn, 3, "programa", -0.3), F_clip("wbir_2020", ini=63.6, fin=66.5, z0=1.0, z1=1.08, tono=SEP, sat=0.8),
     [], [TAG("Job Corps · Knoxville, Tennessee", 1330, 880, A(Qn, 3, "programa"), 46), CRED(C_W, A(Qn, 3, "programa"), A(Qn, 3, "programa") + 2.6)], ent=("fundido", 0.5))
shot(A(Qn, 3, "programa", 2.7), F_mg("q_campus"), [], [], ent=("fundido", 0.6))

# ============================================================== COLLEEN
Co = "colleen"
shot(INI(Co, 0), F_clip("wbir_2020", ini=70.7, fin=72.9, z0=1.0, z1=1.1, c0=(0.5, 0.45), c1=(0.5, 0.45), tono=(1.0, 0.95, 0.9)),
     [], [TAG("Colleen Slemmer", 1500, 880, A(Co, 0, "colin"), 54), CRED(C_W, INI(Co, 0) + 0.3, FIN(Co, 0))], ent=("tinta", 0.7))
shot(INI(Co, 1), F_arch("wbir_cronologia", ini=301.3, fin=304.7, x_cont=(0.0, 1.0), alto=800, z0=1.0, z1=1.07, dx=-230, bg=0.34),
     [N("19", 1500, 420, 330, A(Co, 1, "diecinueve")), R([("años", A(Co, 1, "diecinueve", 0.3))], 1500, 610, 74)],
     [CRED(C_W, INI(Co, 1) + 0.3, A(Co, 1, "florida", -0.5))], ent=("fundido", 0.6))
shot(A(Co, 1, "florida", -0.5), F_mg("c_florida"), [], [], ent=("fundido", 0.5))
shot(INI(Co, 2), F_mg("c_pc"), [R(pk(Co, 2, "computacion"), 1380, 830, 90)], [], ent=("fundido", 0.6))

# ============================================================== CRIMEN
Cr = "crimen"
shot(INI(Cr, 0), F_arch("wbir_asesinato_1995", ini=26.2, fin=27.9, tono=(0.95, 0.9, 0.9), alto=920),
     [], [TAG("Christa Pike · 18 años", 1520, 880, A(Cr, 0, "crista"), 50), CRED(C_W, INI(Cr, 0) + 0.3, A(Cr, 0, "novio") - 0.2)], ent=("tinta", 0.7))
shot(A(Cr, 0, "novio", -0.35), F_arch("wbir_asesinato_1995", ini=28.1, fin=32.3, tono=(0.95, 0.9, 0.9), alto=920),
     [], [TAG("Tadaryl Shipp · 17 años", 1520, 880, A(Cr, 0, "novio"), 50), CRED(C_W, A(Cr, 0, "novio") - 0.3, FIN(Cr, 0))], ent=("fundido", 0.45))
shot(INI(Cr, 1), F_mg("cr_bosque"), [], [], ent=("fundido", 0.6))
shot(A(Cr, 1, "junto", -0.2), F_arch("wbir_asesinato_1995", ini=59.5, fin=72.5, tono=(0.8, 0.8, 0.85), sat=0.7, alto=900),
     [S([("Planta", A(Cr, 1, "planta")), ("De", A(Cr, 1, "de")), ("Vapor", A(Cr, 1, "vapor")), ("Abandonada", A(Cr, 1, "abandonada"))], W / 2, 975, 92)],
     [CRED(C_W, A(Cr, 1, "junto"), FIN(Cr, 1))], ent=("fundido", 0.5))
shot(INI(Cr, 2), F_mg("cr_paz"), [], [], ent=("tinta", 0.7))
shot(INI(Cr, 3), F_mg("cr_reloj"),
     [N("30 min", 560, 430, 150, A(Cr, 3, "media", -0.1)), N("a 1 hora", 560, 620, 150, A(Cr, 3, "hora", -0.1, 1)),
      R(pk(Cr, 3, "segun", "tribunal"), W / 2, 900, 62)], [], ent=("fundido", 0.7))
shot(INI(Cr, 4), F_mg("cr_luto"), [], [], ent=("fundido", 0.9))
shot(INI(Cr, 5), F_arch("wbir_asesinato_1995", ini=47.95, fin=50.5, tono=(0.8, 0.8, 0.85), sat=0.7, alto=900),
     [], [TAG("Knoxville · enero de 1995", 1520, 880, INI(Cr, 5) + 0.3, 46), CRED(C_W, INI(Cr, 5) + 0.3, A(Cr, 5, "estaba") - 0.3)], ent=("tinta", 0.7))
shot(A(Cr, 5, "estaba", -0.3), F_arch("wbir_asesinato_1995", ini=50.8, fin=53.1, tono=(0.8, 0.8, 0.85), sat=0.7, alto=900),
     [], [CRED(C_W, A(Cr, 5, "estaba") - 0.3, A(Cr, 5, "principio") - 0.2)], ent=("fundido", 0.45))
shot(A(Cr, 5, "principio", -0.2), F_arch("wbir_asesinato_1995", ini=60.0, fin=72.0, tono=(0.7, 0.72, 0.78), sat=0.6, alto=900),
     [], [CRED(C_W, A(Cr, 5, "principio") - 0.2, FIN(Cr, 5))], ent=("fundido", 0.6), grado=dict(vineta=0.85))

# ============================================================== JUICIO
J = "juicio"
shot(INI(J, 0), F_mg("j_trato"), [], [CRED("Recreación gráfica · no es el documento real", INI(J, 0) + 0.3, FIN(J, 0))], ent=("tinta", 0.7))
shot(INI(J, 1), F_arch("wbir_asesinato_1995", ini=28.1, fin=32.3, tono=(0.95, 0.9, 0.9), alto=920),
     [], [TAG("Tadaryl Shipp · cadena perpetua", 1320, 880, A(J, 1, "novio"), 46), CRED(C_W, INI(J, 1) + 0.3, A(J, 1, "amiga") - 0.3)], ent=("fundido", 0.6))
shot(A(J, 1, "amiga", -0.3), F_mg("j_testigo"),
     [S([("Shadolla", A(J, 1, "amiga")), ("Peterson", A(J, 1, "amiga", 0.4))], 1380, 250, 100),
      R(pk(J, 1, "declaro", "contra"), 1380, 400, 52), R(pk(J, 1, "recibio", "carcel"), 1380, 520, 52)], [], ent=("fundido", 0.5))
shot(INI(J, 2), F_mg("j_tribunal"), [], [], ent=("fundido", 0.6))
shot(A(J, 2, "silla", -0.3), F_mg("j_silla"),
     [S([("Silla", A(J, 2, "silla")), ("Eléctrica", A(J, 2, "electrica"))], W / 2, 230, 124)], [], ent=("fundido", 0.4))
shot(INI(J, 3), F_clip("france24", ini=46.1, fin=49.8, z0=1.0, z1=1.1, tono=(0.9, 0.88, 0.85)),
     [], [TAG("1996 · 20 años", 560, 900, INI(J, 3) + 0.3, 48), CRED(C_F, INI(J, 3) + 0.3, FIN(J, 3))], ent=("fundido", 0.7), grado=dict(vineta=0.85))

# ============================================================== CORREDOR
Cd = "corredor"
shot(INI(Cd, 0), F_mg("co_anos"),
     [N("30", 520, 330, 360, A(Cd, 0, "treinta")), R([("años", A(Cd, 0, "treinta", 0.4))], 520, 540, 78),
      R(pk(Cd, 0, "unica", "mujer"), 1340, 830, 86), R([("Aislada", A(Cd, 0, "aislada"))], 520, 800, 90)], [], ent=("tinta", 0.7))
_marcas = [(2001, "Pide ser ejecutada", A(Cd, 1, "uno"), (True, 120)), (2002, "Lo pide otra vez", ww(Cd, 1, "dos", 2), (False, 120)),
           (2004, "Condena por atacar a otra presa", A(Cd, 2, "cuatro"), (True, 230)), (2022, "Demanda por igualdad", A(Cd, 3, "veintidos"), (False, 120)),
           (2024, "Acuerdo con el estado", A(Cd, 3, "veinticuatro"), (True, 120))]
_lin = LINEA_ANOS(1995, 2027, 600, _marcas, INI(Cd, 1), FIN(Cd, 3), 1996, 2026, etiqueta="Años en el corredor de la muerte")
shot(INI(Cd, 1), F_mg("co_pasillo"), [], [_lin], ent=("fundido", 0.7), grado=dict(vineta=0.9))
