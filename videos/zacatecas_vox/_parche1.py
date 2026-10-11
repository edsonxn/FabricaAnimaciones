# -*- coding: utf-8 -*-
import re
p = 'locales.py'
s = open(p, encoding='utf-8').read()

# --- colinas de fondo angulosas (papel recortado)
a = s.index("def colinas_fondo")
b = s.index("def montaña_bufa")
nuevo = '''def colinas_fondo(lz, cam_x, prof, base, alt, seed, color, x0=-1800, x1=1800, alfa=1.0, capa=0, cam_y=0.0, paso=150.0):
    """Capa de cerros lejanos ANGULOSOS (recortes) con paralaje: prof 0..1 (1 = se mueve con el mundo)."""
    dx = cam_x * (1 - prof)
    dy = cam_y * (1 - prof)
    xs = np.arange(x0, x1 + paso, paso)
    hs = np.array([0.25 + 0.75 * h01(int(seed * 10), i) ** 1.3 for i in range(len(xs))])
    ys = base - alt * hs
    P = np.vstack([np.stack([xs + dx, ys + dy], 1), [[x1 + dx, base + 900 + dy], [x0 + dx, base + 900 + dy]]])
    lz.relleno(P, color, temblor=0.0, capa=capa, alfa=alfa)


BUFA = np.array([(430, 20), (500, -60), (548, -150), (600, -200), (640, -330), (700, -360), (742, -470), (800, -520),
                 (838, -640), (900, -700), (940, -780), (972, -720), (1012, -742), (1060, -660), (1090, -560),
                 (1150, -480), (1190, -360), (1250, -300), (1310, -180), (1380, -110), (1450, 20)], float)
BUFA_SOMBRA = np.array([(940, -780), (972, -720), (1012, -742), (1060, -660), (1090, -560), (1150, -480), (1190, -360),
                        (1250, -300), (1310, -180), (1380, -110), (1450, 20), (1120, 20), (1060, -200), (1000, -460)], float)
BUFA_CRESTA = np.array([(900, -700), (940, -780), (972, -720), (1012, -742), (1030, -690), (980, -672), (930, -676)], float)
GRILLO = np.array([(-1500, 20), (-1430, -90), (-1380, -160), (-1320, -250), (-1260, -300), (-1200, -400), (-1130, -430),
                   (-1090, -360), (-1040, -330), (-980, -240), (-930, -190), (-880, -120), (-820, -70), (-760, 20)], float)
GRILLO_SOMBRA = np.array([(-1130, -430), (-1090, -360), (-1040, -330), (-980, -240), (-930, -190), (-880, -120), (-820, -70),
                          (-760, 20), (-1040, 20), (-1100, -180)], float)


def mesa(lz, x, ancho, alto, seed, alfa=1.0, claro=ROJIZO, capa=1):
    """Mesa/cerro suelto de bordes rectos (para el paisaje del camino)."""
    w = ancho / 2
    P = np.array([[x - w * 1.3, 20], [x - w, -alto * 0.55], [x - w * 0.55, -alto], [x + w * 0.4, -alto * 0.94],
                  [x + w * 0.9, -alto * 0.5], [x + w * 1.3, 20]])
    P = V.corte(P, seed, 6.0, 2)
    lz.relleno(P, claro, temblor=0.0, capa=capa, alfa=alfa)
    lz.relleno(np.array([[x + w * 0.4, -alto * 0.94], [x + w * 0.9, -alto * 0.5], [x + w * 1.3, 20], [x + w * 0.1, 20],
                         [x + w * 0.05, -alto * 0.5]]), ROJIZO_OSC, temblor=0.0, capa=capa, alfa=alfa)


def subsuelo_base(lz, alfa=1.0):
    """Tierra oscura bajo el mundo (y > 420)."""
    lz.relleno(np.array([[-9000, 420], [12000, 420], [12000, 9000], [-9000, 9000]]), (74, 56, 56), temblor=0.0, capa=1, alfa=alfa)


'''
s = s[:a] + nuevo + s[b:]

# --- montaña_bufa: siluetas angulosas
a = s.index("def montaña_bufa")
b = s.index("def suelo")
nuevo2 = '''def montaña_bufa(lz, alfa=1.0, capa=1, detalle=1.0):
    """Bufa y cerro del Grillo como recortes angulosos de papel (telón de fondo del valle)."""
    for P, sombra, c_luz, c_som in ((GRILLO, GRILLO_SOMBRA, (206, 142, 104), (170, 108, 82)),
                                    (BUFA, BUFA_SOMBRA, (204, 134, 96), (160, 96, 72))):
        lz.relleno(V.corte(P, 5, 2.5, 2), c_luz, temblor=0.0, capa=capa, alfa=alfa, seed=5)
        lz.relleno(sombra, c_som, temblor=0.0, capa=capa, alfa=alfa)
        if detalle > 0.5:
            V.semitono(lz, sombra, (128, 74, 58), esp=30, r=4.2, ang=0.5, capa=capa)
    lz.relleno(BUFA_CRESTA, (226, 176, 136), temblor=0.0, capa=capa, alfa=alfa)
    lz.relleno(np.array([[972, -720], [1012, -742], [1030, -690], [1000, -684]]), (150, 90, 68), temblor=0.0, capa=capa, alfa=alfa)
    for i in range(60):
        x = -2400 + i * 90 + 40 * h01(4, i)
        lz.relleno(V.elipse_pts(x, 10, 22, 11), (150, 158, 96), temblor=0.0, capa=capa, alfa=alfa * 0.9)


'''
s = s[:a] + nuevo2 + s[b:]
s = s.replace('lz.relleno(np.array([[x0, grosor - 2], [x1, grosor - 2], [x1, 420], [x0, 420]]), (168, 106, 80), temblor=0.0, capa=1, alfa=alfa)',
              'lz.relleno(np.array([[x0, grosor - 2], [x1, grosor - 2], [x1, 424], [x0, 424]]), (168, 106, 80), temblor=0.0, capa=1, alfa=alfa)')
open(p, 'w', encoding='utf-8').write(s)

# --- estratos con más contraste (subsuelo.py)
p = 'subsuelo.py'
s = open(p, encoding='utf-8').read()
a = s.index("ESTRATOS = [")
b = s.index("POZO_X")
s = s[:a] + '''ESTRATOS = [(0, (176, 112, 84)), (230, (216, 172, 122)), (620, (150, 124, 120)), (1150, (124, 102, 118)),
            (1750, (98, 86, 110)), (2400, (72, 66, 94)), (3100, (54, 50, 76))]
''' + s[b:]
open(p, 'w', encoding='utf-8').write(s)

# --- cielo como fondo de pantalla (barato)
p = 'C:/FabricaAnimaciones/nucleo/fondos.py'
s = open(p, encoding='utf-8').read()
if "def cielo_fondo" not in s:
    s = s.replace('\n\nFONDOS["papel"] = papel', '''

def cielo_fondo(colores, alfa=1.0, papel_img=None):
    """Degradado vertical (arriba, abajo) a pantalla completa; se mezcla con el papel según alfa."""
    a = np.array(colores[0], np.float32) / 255
    b = np.array(colores[1], np.float32) / 255
    v = np.clip(np.linspace(0, 1, H, dtype=np.float32) / 0.72, 0, 1)[:, None, None]
    col = a * (1 - v) + b * v
    img = np.broadcast_to(col, (H, W, 3))
    if papel_img is not None:
        return papel_img * (1 - alfa) + img * alfa
    return np.ascontiguousarray(img)


FONDOS["papel"] = papel''')
    open(p, 'w', encoding='utf-8').write(s)

# --- cap_local.base_local sin cielo pesado
p = 'cap_local.py'
s = open(p, encoding='utf-8').read()
a = s.index("def base_local")
b = s.index("# ------------------------------------------------------------------ casas del campamento")
s = s[:a] + '''def base_local(lz, t, cam_l, hora, alfa=1.0, sol_pos=(-300, -720)):
    """Sol + nubes + cerros lejanos + sierra de la Bufa + suelo (el degradado del cielo va en el fondo de pantalla)."""
    if alfa <= 0.01:
        return
    if isinstance(hora, str) and hora != "noche":
        L.sol(lz, sol_pos[0] + cam_l[0] * 0.05, sol_pos[1] + cam_l[1] * 0.05, 74, t, alfa=alfa)
    for i, (nx, ny, s) in enumerate([(-500, -1000, 1.2), (250, -1180, 0.9), (700, -900, 1.0), (-900, -820, 0.8)]):
        L.nube(lz, nx + (26 * t * 0.3) % 1200 - 200 + cam_l[0] * 0.08, ny + cam_l[1] * 0.08, s * 1.4, alfa=alfa, capa=0,
               color=(252, 248, 240))
    L.colinas_fondo(lz, cam_l[0], 0.3, -180, 520, 1.0, (222, 176, 150), -4200, 4200, alfa=alfa, cam_y=cam_l[1], paso=170)
    L.colinas_fondo(lz, cam_l[0], 0.6, -40, 360, 3.0, (204, 150, 118), -4200, 4200, alfa=alfa, cam_y=cam_l[1], paso=130)
    L.subsuelo_base(lz, alfa)
    L.montaña_bufa(lz, alfa=alfa)
    L.suelo(lz, -3400, 6400, SUR, alfa=alfa)


''' + s[b:]
open(p, 'w', encoding='utf-8').write(s)

# --- escenas: fondo con cielo, cámaras
p = 'escenas.py'
s = open(p, encoding='utf-8').read()
s = s.replace('''        osc = 0.0
        return F.papel(t, oscuro=osc, dx=cx * z * 0.05, dy=cy * z * 0.05)''', '''        pap = F.papel(t, dx=cx * z * 0.05, dy=cy * z * 0.05)
        al = CL.alfa_local(z)
        if al > 0.01:
            return F.cielo_fondo(hora_dia(t), al, pap)
        return pap''')
s = s.replace('KL(A_C["arma"] + 0.8, 90, -40, 1.5)', 'KL(A_C["arma"] + 0.8, 520, -60, 1.5)')
open(p, 'w', encoding='utf-8').write(s)
print("ok")
