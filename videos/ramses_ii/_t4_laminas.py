

# ================================================================== TRAMO 4 (120-576 s): láminas del túnel, una por idea; cada una con su firma
import os as _os


def fs(key):
    return _FR[key]["words"][0]["s"]


def fe(key):
    return _FR[key]["words"][-1]["e"]


def IMGX(nombre):
    """Ruta de un archivo de imagenes/ si existe (el material de Commons puede faltar): None si no."""
    p = IMG + nombre
    return p if _os.path.exists(p) else None


def cine(nombre, t, ta, tb, z0=1.04, z1=1.16, c0=(0.5, 0.5), c1=(0.5, 0.5)):
    return toma("cine_" + nombre, t, ta, tb, z0=z0, z1=z1, c0=c0, c1=c1, par=(0, 0))


def foto(nombre, t, ta, tb, z0=1.04, z1=1.14, c0=(0.5, 0.5), c1=(0.5, 0.5), oscuro=0.75):
    if not IMGX(nombre):
        return negro()
    lz = toma(nombre, t, ta, tb, z0=z0, z1=z1, c0=c0, c1=c1, par=(0, 0))
    return lz * oscuro


def lonlat(lon, lat):
    """Punto del mapa_medit (pantalla completa, sin cámara): medido con Chipre y el mar Muerto en previews/_mapa_rejilla.jpg."""
    return 1505 + (lon - 34.58) * 132.0, 102 + (35.70 - lat) * 163.0


def centrar(img, z, px, py, rot=0.0):
    """Cámara que deja el punto (px, py) del cuadro en el centro con zoom z."""
    return _cam_punto(img, z, -(px - W / 2) * z, -(py - H / 2) * z, rot)


_HATTI = [(1080, 0), (1920, 0), (1920, 300), (1790, 318), (1730, 300), (1690, 250), (1665, 140), (1600, 60), (1450, 28), (1290, 12)]
_CANAAN = [(1480, 800), (1520, 700), (1560, 560), (1600, 460), (1646, 360), (1690, 312), (1780, 330), (1800, 450), (1760, 600), (1720, 790), (1640, 880)]


# ------------------------------------------------------------------ cap. 2: KADESH
A.firma("k_mapa", "mapa satelital con zoom al levante + egipto rojo y canaán que se llenan + imperio hitita gris acero que baja desde anatolia + "
        "kadesh con anillo que late entre los dos + ruta punteada desde el delta + rótulo 1274 a. c.")


def k_mapa(t, ta, tb):
    lz = toma("mapa_medit", t, ta, tb, z0=1.0, z1=1.0, par=(0, 0)) * 0.80
    humo(lz, t, sem=31, v=(-30, 6), color=(0.9, 0.9, 0.92), op=0.16)
    A.territorio(lz, _EGIPTO, (1050, 1060), e_out(prog(t, ta, ta + 1.4)), t, op=0.42, sem=3)
    A.territorio(lz, _CANAAN, (1500, 780), e_out(prog(t, ta + 0.6, ta + 2.6)), t, op=0.34, sem=5)
    t_hi = T("kadesh_1", "imperio")
    A.territorio(lz, _HATTI, (1500, 0), e_out(prog(t, t_hi - 0.3, t_hi + 2.4)), t, color=(0.55, 0.62, 0.70), op=0.50, sem=8)
    kx, ky = lonlat(36.51, 34.56)
    u = e_inout(prog(t, ta + 1.2, ta + 3.4))
    D.linea_punteada(lz, [(1060, 830), (1300, 820), (1490, 760), (1600, 520), (kx, ky)], u, grosor=4, color=(1.0, 0.86, 0.6))
    if t > ta + 3.0:
        r = 22 + 8 * math.sin(t * 4)
        cv2.circle(lz, (int(kx), int(ky)), int(r), (1.0, 0.25, 0.2), 3, cv2.LINE_AA)
    A.etiqueta(lz, "Kadesh", kx + 30, ky - 6, t, ta + 3.0, px=34)
    A.etiqueta(lz, "Hatti", 1500, 150, t, t_hi + 0.8, px=32, color=(0.85, 0.9, 1.0))
    A.rotulo_serif(lz, [("KADESH · ", A.BLANCO), ("1274 a. C.", A.ROJO)], W * 0.5, H * 0.10, t, ta + 0.6, px=48)
    z = lerp(1.0, 1.55, e_inout(prog(t, ta + 0.8, ta + 4.5)))
    return centrar(lz, z, lerp(W / 2, 1520, e_inout(prog(t, ta + 0.8, ta + 4.5))), lerp(H / 2, 420, e_inout(prog(t, ta + 0.8, ta + 4.5))))


A.firma("k_divisiones", "suelo de rejilla oscuro + cuatro estandartes de las divisiones (amón, ra, ptah, set) que entran uno por dios con su nombre + "
        "columnas de puntos que marchan al norte + flecha norte + campamento de flow muy oscuro detrás")


def k_divisiones(t, ta, tb):
    lz = cine("kadesh_campamento", t, ta, tb, 1.15, 1.25, (0.45, 0.5), (0.55, 0.5))
    lz[:] = cv2.GaussianBlur(lz, (0, 0), 6) * 0.35
    A.rejilla(lz, t, horizonte=0.52, op=0.30, vel=0.5)
    dioses = [("amon", "AMÓN"), ("ra", "RA"), ("ptah", "PTAH"), ("set", "SET")]
    for i, (pal, nom) in enumerate(dioses):
        try:
            t_d = T("kadesh_2", pal)
        except IndexError:
            t_d = fs("kadesh_2") + 4 + i
        x = W * (0.2 + 0.2 * i)
        u = e_out(prog(t, t_d - 0.3, t_d + 0.5))
        if u <= 0:
            continue
        y0 = H * 0.30 + (1 - u) * 160
        cv2.line(lz, (int(x), int(y0)), (int(x), int(H * 0.80)), (0.75 * u, 0.62 * u, 0.40 * u), 4, cv2.LINE_AA)
        cv2.rectangle(lz, (int(x - 48), int(y0)), (int(x + 48), int(y0 + 70)), (0.55 * u, 0.06 * u, 0.06 * u), -1)
        cv2.rectangle(lz, (int(x - 48), int(y0)), (int(x + 48), int(y0 + 70)), (0.95 * u, 0.80 * u, 0.5 * u), 2, cv2.LINE_AA)
        A.rotulo_serif(lz, [(nom, A.BLANCO)], x, y0 + 35, t, t_d - 0.1, px=30, vel=0.02)
        for k in range(14):                                          # soldados (puntos) que marchan al norte
            yy = H * 0.95 - ((t - t_d) * 60 + k * 26) % (H * 0.55)
            xx = x + ((k * 37) % 5 - 2) * 10
            cv2.circle(lz, (int(xx), int(yy)), 4, (0.95 * u, 0.85 * u, 0.6 * u), -1, cv2.LINE_AA)
    A.texto_mixto(lz, [("Cuatro divisiones,", A.BLANCO), ("cada una con el nombre de un dios", A.GRIS)], W * 0.07, H * 0.12, t, T("kadesh_2", "cuatro"), px=36)
    A.polvo(lz, t, n=50, sem=32, op=0.35)
    return camara(lz, t, ta, tb, 1.0, 1.06, dx=(0, -30))


A.firma("k_espias", "dos nómadas de rodillas ante guardias con antorchas que laten + humo bajo + texto de lo que juran + alepo lejos con flecha que se estira + "
        "foco que se cierra sobre sus caras")


def k_espias(t, ta, tb):
    lz = cine("espias", t, ta, tb, 1.05, 1.22, (0.5, 0.5), (0.40, 0.55))
    lz *= np.float32(0.88 + 0.12 * math.sin(t * 8.3) * math.sin(t * 2.9))
    humo(lz, t, sem=33, v=(14, -8), color=(0.7, 0.62, 0.5), op=0.22, zona_y=(0.5, 1.0))
    particulas(lz, t, sem=34, n=70, v=(5, -90), tam=(1, 2.2), color=(1.0, 0.6, 0.2), op=0.7, parpadeo=0.6, zona=(int(W * 0.5), 0, W, H))
    t_j = T("kadesh_3", "juraron")
    A.texto_mixto(lz, [("«Los hititas", A.BLANCO), ("están lejos, en Alepo»", A.GRIS)], W * 0.06, H * 0.80, t, t_j, px=40)
    t_al = T("kadesh_3", "alepo")
    u = e_inout(prog(t, t_al - 0.2, t_al + 1.0))
    if u > 0:
        A.arco_luz(lz, (W * 0.42, H * 0.20), (W * 0.92, H * 0.12), -20, u * 1.2, color=(0.95, 0.85, 0.6))
        A.etiqueta(lz, "Alepo · 150 km al norte", W * 0.70, H * 0.08, t, t_al + 0.4, px=28)
    v = smooth(prog(t, t_j, tb))
    yy, xx = np.ogrid[0:H, 0:W]
    lz *= (1 - 0.55 * v * np.clip(((xx - W * 0.38) ** 2 + (yy - H * 0.55) ** 2) / (W * 0.40) ** 2, 0, 1)).astype(np.float32)[..., None]
    return lz


A.firma("k_mentira", "neón rojo mentían que parpadea y se estabiliza + franja de carros hititas de flow que asoma desde detrás de la ciudad al fondo + "
        "texto eran espías + silueta de la ciudad que tiembla")


def k_mentira(t, ta, tb):
    lz = negro()
    fondo = cine("carros_hititas", t, ta, tb, 1.20, 1.05, (0.5, 0.35), (0.5, 0.45))
    rev = smooth(prog(t, T("kadesh_4", "muwatalli") - 0.3 if _tiene("kadesh_4", "muwatalli") else fs("kadesh_4") + 3, fe("kadesh_4")))
    lz += fondo * (0.15 + 0.55 * rev)
    A.polvo(lz, t, n=80, sem=35, op=0.4)
    A.neon(lz, "MENTÍAN", W * 0.5, H * 0.40, t, fs("kadesh_4") - 0.1, px=110)
    A.cursiva_luz(lz, "ERAN ESPÍAS", W * 0.5, H * 0.58, t, T("kadesh_4", "eran"), px=48)
    A.texto_mixto(lz, [("Muwatalli:", A.BLANCO), ("escondido detrás de la ciudad", A.GRIS)], W * 0.5, H * 0.86, t, T("kadesh_4", "esperaba") - 0.2,
                  px=36, alinear="centro")
    return camara(lz, t, ta, tb, 1.0, 1.08, temblor=1.4 * rev)


def _tiene(key, pal):
    try:
        T(key, pal)
        return True
    except IndexError:
        return False


A.firma("k_carga", "carros hititas de flow a la carga con temblor fuerte + arena que vuela de lado con estela + diagrama encima: bloque de la división de ra "
        "que recibe una flecha roja gruesa + campamento de amón casi solo marcado + destellos")


def k_carga(t, ta, tb):
    lz = cine("carros_hititas", t, ta, tb, 1.08, 1.30, (0.5, 0.5), (0.5, 0.6))
    particulas(lz, t, sem=36, n=260, v=(-900, 40), tam=(1, 2.4), color=(0.9, 0.75, 0.55), op=0.35, estela=0.06)
    humo(lz, t, sem=37, v=(-140, 0), color=(0.8, 0.66, 0.5), op=0.30, zona_y=(0.4, 1.0))
    lz *= 0.85
    t_am = T("kadesh_5", "amon")
    cv2.rectangle(lz, (int(W * 0.08), int(H * 0.10)), (int(W * 0.30), int(H * 0.22)), (0.9, 0.85, 0.7), 2, cv2.LINE_AA)
    A.rotulo_serif(lz, [("CAMPAMENTO DE ", A.BLANCO), ("AMÓN", A.ROJO)], W * 0.19, H * 0.16, t, t_am - 0.2, px=26)
    t_ra = T("kadesh_5", "ra", n=0) if _tiene("kadesh_5", "ra") else fs("kadesh_5") + 5
    u = e_out(prog(t, t_ra - 0.6, t_ra + 0.3))
    if u > 0:
        x0, y0 = W * 0.62, H * 0.28
        cv2.rectangle(lz, (int(x0), int(y0)), (int(x0 + 300), int(y0 + 90)), (0.9, 0.85, 0.7), 2, cv2.LINE_AA)
        A.rotulo_serif(lz, [("DIVISIÓN DE ", A.BLANCO), ("RA", A.ROJO)], x0 + 150, y0 + 45, t, t_ra - 0.4, px=28)
        p = (int(lerp(W * 0.98, x0 + 300, u)), int(y0 + 45))
        cv2.arrowedLine(lz, (int(W * 1.02), int(y0 + 45)), p, (0.95, 0.12, 0.10), 14, cv2.LINE_AA, tipLength=0.25)
    flashes(lz, t, t_ra, tb, sem=38, n=5)
    return camara(lz, t, ta, tb, 1.0, 1.04, temblor=3.0)


A.firma("k_cinco_mil", "contador gigante de carros hasta 5 000 + rejilla de siluetas de carro (del carro real recortado) que se llena en filas desde los dos lados "
        "en dos colores + rótulo la mayor batalla de carros + polvo")


def k_cinco_mil(t, ta, tb):
    lz = negro()
    A.rejilla(lz, t, horizonte=0.62, op=0.22, vel=0.2)
    png = IMGX("carro_tut_rec.png")
    t_c = T("kadesh_6", "carros")
    n = int(120 * e_out(prog(t, t_c - 0.5, fe("kadesh_6"))))
    if png and n > 0:
        spr = A._sprite_png(png, 46)
        for k in range(n):
            lado = k % 2
            fila, col = divmod(k // 2, 12)
            x = (W * 0.06 + col * 64) if lado == 0 else (W * 0.94 - col * 64)
            y = H * 0.50 + fila * 46
            M = D.poner(spr.w, spr.h, x, y, 1.0)
            capa = np.zeros_like(lz)
            D.pegar(capa, spr, M, 1.0)
            tono = np.float32((0.85, 0.75, 0.55)) if lado == 0 else np.float32((0.60, 0.68, 0.80))
            lz += capa.max(-1, keepdims=True) * tono * 0.9 if k == n - 1 else 0
            if k == n - 1:
                break
        lz2 = np.zeros_like(lz)
        for k in range(n):
            lado = k % 2
            fila, col = divmod(k // 2, 12)
            x = (W * 0.06 + col * 64) if lado == 0 else (W * 0.94 - col * 64)
            y = H * 0.50 + fila * 46
            cv2.rectangle(lz2, (int(x - 22), int(y - 12)), (int(x + 22), int(y + 12)), (0.85, 0.72, 0.5) if lado == 0 else (0.55, 0.65, 0.78), -1)
        lz += cv2.GaussianBlur(lz2, (0, 0), 1.2) * 0.55
    contador(lz, t, fs("kadesh_6") + 1.5, 4.5, 0, 5000, W * 0.5, H * 0.24, px=120, sufijo=" carros", color=A.ROJO_HALO)
    A.rotulo_serif(lz, [("LA MAYOR BATALLA DE ", A.BLANCO), ("CARROS", A.ROJO)], W * 0.5, H * 0.40, t, T("kadesh_6", "mayor"), px=40)
    A.etiqueta(lz, "Egipto", W * 0.10, H * 0.46, t, t_c, px=26)
    A.etiqueta(lz, "Hatti", W * 0.84, H * 0.46, t, t_c, px=26, color=(0.8, 0.88, 1.0))
    particulas(lz, t, sem=39, n=120, v=(0, -20), tam=(1, 2), color=(0.9, 0.8, 0.6), op=0.4)
    return camara(lz, t, ta, tb, 1.0, 1.07, rot=(-0.4, 0.4))


A.firma("k_solo", "faraón en su carro de flow rodeado con empuje lento + cita amarilla del poema de kadesh «estaba solo» + polvo dorado que gira + "
        "barrido de luz cuando llegan los refuerzos + rótulo refuerzos")


def k_solo(t, ta, tb):
    lz = cine("faraon_solo", t, ta, tb, 1.02, 1.28, (0.35, 0.5), (0.30, 0.45))
    humo(lz, t, sem=40, v=(-50, -10), color=(0.85, 0.7, 0.5), op=0.25)
    particulas(lz, t, sem=41, n=160, v=(-300, 60), tam=(1, 2.5), color=(1.0, 0.82, 0.5), op=0.45, estela=0.04)
    lz *= 0.82
    A.cita(lz, ["«Estaba solo,", "ninguno conmigo»"], W * 0.72, H * 0.32, t, T("kadesh_7", "relato"), px=46, fuente_txt="Poema de Kadesh (relato del propio faraón)",
           salida=T("kadesh_7", "cierto") - 0.3)
    t_r = T("kadesh_7", "refuerzos")
    barrido_luz(lz, t, t_r - 0.4, dur=1.4, op=0.35)
    A.rotulo_serif(lz, [("RESISTIÓ HASTA LOS ", A.BLANCO), ("REFUERZOS", A.ROJO)], W * 0.66, H * 0.84, t, T("kadesh_7", "resistio"), px=40)
    return lz


A.firma("k_empate", "balanza de bronce dibujada que oscila y queda nivelada (egipto contra hatti) + kadesh que cambia a gris hitita + neón nadie ganó + "
        "egipto que vuelve con flecha punteada hacia el sur")


def k_empate(t, ta, tb):
    lz = A.piedra(sem=41) * 0.7
    A.polvo(lz, t, n=60, sem=42, op=0.35)
    cx, cy = W * 0.5, H * 0.52
    ang = 18 * math.exp(-max(0.0, t - ta - 0.5) * 0.9) * math.sin((t - ta) * 3.2)
    a = math.radians(ang)
    dx, dy = 360 * math.cos(a), 360 * math.sin(a)
    oro = (0.85, 0.66, 0.32)
    cv2.line(lz, (int(cx), int(cy - 220)), (int(cx), int(cy + 230)), oro, 6, cv2.LINE_AA)
    cv2.line(lz, (int(cx - dx), int(cy - 200 - dy)), (int(cx + dx), int(cy - 200 + dy)), oro, 6, cv2.LINE_AA)
    for s, nom, col in ((-1, "EGIPTO", A.ROJO), (1, "HATTI", (0.6, 0.68, 0.8))):
        px_, py_ = cx + s * dx, cy - 200 + s * dy
        cv2.line(lz, (int(px_), int(py_)), (int(px_ - 70), int(py_ + 150)), oro, 2, cv2.LINE_AA)
        cv2.line(lz, (int(px_), int(py_)), (int(px_ + 70), int(py_ + 150)), oro, 2, cv2.LINE_AA)
        cv2.ellipse(lz, (int(px_), int(py_ + 150)), (90, 22), 0, 0, 180, oro, 5, cv2.LINE_AA)
        A.rotulo_serif(lz, [(nom, col)], px_, py_ + 200, t, ta + 0.3, px=34)
    A.neon(lz, "NADIE GANÓ", W * 0.5, H * 0.12, t, T("kadesh_8", "nadie"), px=72, barras=False)
    A.texto_mixto(lz, [("Kadesh:", A.BLANCO), ("se quedó hitita", A.GRIS)], W * 0.06, H * 0.88, t, T("kadesh_8", "hititas"), px=36)
    A.texto_mixto(lz, [("Egipto:", A.BLANCO), ("a casa sin la ciudad", A.GRIS)], W * 0.62, H * 0.88, t, T("kadesh_8", "egipto"), px=36)
    return camara(lz, t, ta, tb, 1.04, 1.0)


A.firma("k_historia", "escultores tallando el muro por antorchas con empuje + chispas de cincel que saltan en ráfagas + neón una historia + "
        "cinco templos que se encienden en fila a lo largo de una línea del nilo, de abydos a abu simbel")


def k_historia(t, ta, tb):
    lz = cine("escultores", t, ta, tb, 1.05, 1.20, (0.55, 0.45), (0.45, 0.45))
    lz *= np.float32(0.85 + 0.1 * math.sin(t * 7.1))
    for k in range(4):
        tk = ta + 1.0 + k * 1.7
        if tk < t < tk + 0.6:
            particulas(lz, t - tk, sem=43 + k, n=40, v=(120 * (1 if k % 2 else -1), -180), tam=(1, 2), color=(1, 0.85, 0.5), op=0.9,
                       zona=(int(W * (0.3 + 0.12 * k)), int(H * 0.3), int(W * (0.36 + 0.12 * k)), int(H * 0.5)))
    A.neon(lz, "UNA HISTORIA", W * 0.5, H * 0.14, t, T("kadesh_9", "historia") - 0.2, px=70, salida=fs("kadesh_10") + 0.5)
    t_c = T("kadesh_10", "cinco")
    if t > t_c - 0.3:
        lz *= 1 - 0.45 * smooth(prog(t, t_c - 0.3, t_c + 0.4))
        temp = ["Abydos", "Karnak", "Luxor", "Rameseo", "Abu Simbel"]
        y = H * 0.72
        u = e_inout(prog(t, t_c, t_c + 0.8))
        cv2.line(lz, (int(W * 0.10), int(y)), (int(lerp(W * 0.10, W * 0.90, u)), int(y)), (0.6, 0.5, 0.35), 3, cv2.LINE_AA)
        for i, nom in enumerate(temp):
            ti = t_c + 0.35 + 0.45 * i
            x = W * (0.12 + 0.19 * i)
            k = smooth(prog(t, ti, ti + 0.3))
            if k > 0:
                cv2.circle(lz, (int(x), int(y)), int(14 + 3 * math.sin(t * 5 + i)), (1.0 * k, 0.75 * k, 0.3 * k), -1, cv2.LINE_AA)
                A.etiqueta(lz, nom, x - 40, y + 50, t, ti, px=28, punto=False)
        A.rotulo_serif(lz, [("CINCO ", A.ROJO), ("TEMPLOS", A.BLANCO)], W * 0.5, H * 0.58, t, t_c, px=46)
    return lz


A.firma("k_propaganda", "relieve real de kadesh en el rameseo que corre como friso arriba y abajo + empate tachado con trazo rojo a mano y victoria eterna que "
        "se escribe encima + neón propaganda + sello rojo que cae")


def k_propaganda(t, ta, tb):
    lz = negro()
    banda_relieve(lz, IMG + "kadesh_rameseo.jpg", H * 0.12, 220, t, ta, vel=55, color=(0.85, 0.7, 0.5), op=0.35)
    banda_relieve(lz, IMG + "kadesh_rameseo.jpg", H * 0.90, 220, t, ta, vel=-45, color=(0.85, 0.7, 0.5), op=0.30, invertir=True)
    A.polvo(lz, t, n=50, sem=48, op=0.35)
    A.rotulo_serif(lz, [("EMPATE", A.BLANCO)], W * 0.5, H * 0.36, t, fs("kadesh_11"), px=70)
    t_v = T("kadesh_11", "victoria")
    D.marcador_mano(lz, "tachado", W * 0.5, H * 0.36, 360, 70, e_out(prog(t, t_v - 0.6, t_v - 0.1)))
    A.cursiva_luz(lz, "VICTORIA ETERNA", W * 0.5, H * 0.50, t, t_v, px=64, color=A.ROJO_HALO)
    t_p = T("kadesh_11", "propaganda")
    A.neon(lz, "PROPAGANDA", W * 0.5, H * 0.68, t, t_p - 0.2, px=84)
    D.estampa(lz, "1274 a. C.", W * 0.80, H * 0.76, t, t_p + 0.8, px=40)
    return camara(lz, t, ta, tb, 1.0, 1.08, rot=(0.6, -0.6))


# ------------------------------------------------------------------ cap. 3: EL TRATADO
A.firma("t_frontera", "mapa del levante con la frontera egipto-hatti que chisporrotea (choques) en 15 destellos + contador de años 0 a 15 + "
        "dos territorios que dejan de latir + rótulo 1259 a. c. la paz")


def t_frontera(t, ta, tb):
    lz = toma("mapa_medit", t, ta, tb, z0=1.0, z1=1.0, par=(0, 0)) * 0.70
    A.territorio(lz, _CANAAN, (1500, 780), 1.0, t, op=0.30, sem=5)
    A.territorio(lz, _HATTI, (1500, 0), 1.0, t, color=(0.55, 0.62, 0.70), op=0.42, sem=8)
    frontera = [(1646, 360), (1690, 312), (1780, 330), (1860, 330)]
    t_q = T("tratado_1", "quince")
    t_p = T("tratado_1", "paz")
    calma = smooth(prog(t, t_p - 0.4, t_p + 1.0))
    for i in range(15):
        tk = t_q - 0.6 + i * 0.25
        if tk < t < tk + 0.5 and calma < 0.5:
            px_, py_ = frontera[i % 4]
            r = int(30 * (1 - (t - tk) / 0.5))
            cv2.circle(lz, (int(px_ + (i * 13) % 40 - 20), int(py_)), max(1, r), (1.0, 0.6, 0.2), 2, cv2.LINE_AA)
    col = (lerp(1.0, 0.95, calma), lerp(0.3, 0.92, calma), lerp(0.2, 0.85, calma))
    cv2.polylines(lz, [np.int32(frontera)], False, col, 5, cv2.LINE_AA)
    contador(lz, t, t_q - 0.4, 3.0, 0, 15, W * 0.5, H * 0.20, px=90, sufijo=" años de choques", color=A.ROJO_HALO, salida=t_p - 0.2)
    A.rotulo_serif(lz, [("1259 a. C. · ", A.BLANCO), ("LA PAZ", A.ROJO)], W * 0.5, H * 0.20, t, t_p, px=56)
    lz = centrar(lz, 1.35, 1620, 420)
    return lz


A.firma("t_pacto", "enviados de flow intercambiando la tablilla con empuje lento + tres cláusulas que entran como lista con marca de visto + "
        "luz de lámparas que respira + rótulo hattusili iii")


def t_pacto(t, ta, tb):
    lz = cine("tratado_firma", t, ta, tb, 1.02, 1.18, (0.5, 0.5), (0.55, 0.45))
    lz *= np.float32(0.80 + 0.08 * math.sin(t * 2.3))
    humo(lz, t, sem=50, v=(8, -14), color=(0.8, 0.7, 0.55), op=0.18)
    clausulas = [("atacarse", "No atacarse"), ("ayudarse", "Ayudarse contra cualquier enemigo"), ("devolverse", "Devolverse a los fugitivos")]
    for i, (pal, txt) in enumerate(clausulas):
        tc = T("tratado_2", pal) if _tiene("tratado_2", pal) else fs("tratado_2") + 4 + 1.5 * i
        y = H * (0.60 + 0.09 * i)
        k = e_out(prog(t, tc - 0.2, tc + 0.3))
        if k > 0:
            cv2.rectangle(lz, (int(W * 0.06), int(y - 20)), (int(W * 0.06 + 40), int(y + 20)), (0.95 * k, 0.9 * k, 0.8 * k), 2, cv2.LINE_AA)
            if t > tc + 0.3:
                cv2.polylines(lz, [np.int32([(W * 0.06 + 8, y), (W * 0.06 + 18, y + 12), (W * 0.06 + 36, y - 16)])], False, (0.95, 0.15, 0.12), 5, cv2.LINE_AA)
            A.texto_mixto(lz, [(txt, A.BLANCO)], W * 0.06 + 64, y, t, tc - 0.1, px=34)
    A.rotulo_serif(lz, [("RAMSÉS II ", A.BLANCO), ("+", A.ROJO), (" HATTUSILI III", A.BLANCO)], W * 0.5, H * 0.10, t, T("tratado_2", "nuevo"), px=42)
    return lz


A.firma("t_doble", "pantalla partida: muro de karnak a la izquierda con paneo vertical y tablilla de arcilla real que sube y gira sobre piedra a la derecha + "
        "línea de luz que las une + etiquetas karnak y estambul + rótulo el tratado de paz más antiguo")


def t_doble(t, ta, tb):
    lz = A.piedra(sem=52) * 0.8
    izq = foto("tratado_karnak.jpg", t, ta, tb, 1.25, 1.35, (0.5, 0.3), (0.5, 0.7), oscuro=0.8) if IMGX("tratado_karnak.jpg") else \
        foto("kadesh_rameseo.jpg", t, ta, tb, 1.3, 1.4, (0.3, 0.4), (0.4, 0.6))
    m = int(W * 0.48)
    u = e_out(prog(t, ta, ta + 0.8))
    lz[:, :int(m * u)] = izq[:, W // 2 - int(m * u) // 2: W // 2 - int(m * u) // 2 + int(m * u)]
    cv2.line(lz, (int(m * u), 0), (int(m * u), H), (0.9, 0.85, 0.75), 3, cv2.LINE_AA)
    png = IMGX("tratado_tablilla_rec.png")
    t_es = T("tratado_4", "estambul") if _tiene("tratado_4", "estambul") else fs("tratado_4") + 2
    if png:
        A.artefacto(lz, png, W * 0.74, H * 0.50, 620, t, fs("tratado_4") - 0.3, giro=10.0)
    else:
        A.camafeo(lz, IMG + "tratado_estambul.jpg", W * 0.74, H * 0.48, 230, t, fs("tratado_4") - 0.3, foco=(0.5, 0.5), zoom=1.2)
    A.etiqueta(lz, "Karnak · jeroglíficos", W * 0.05, H * 0.92, t, T("tratado_3", "karnak"), px=28)
    A.etiqueta(lz, "Estambul · arcilla hitita", W * 0.58, H * 0.92, t, t_es, px=28)
    A.rotulo_serif(lz, [("EL TRATADO DE PAZ ", A.BLANCO), ("MÁS ANTIGUO", A.ROJO)], W * 0.5, H * 0.08, t, T("tratado_3", "antiguo") - 0.2, px=44)
    A.cursiva_luz(lz, "POR PARTIDA DOBLE", W * 0.74, H * 0.18, t, T("tratado_3", "doble") - 0.2, px=40)
    return camara(lz, t, ta, tb, 1.0, 1.05)


A.firma("t_onu", "réplica de cobre en la onu con paneo y destello metálico que la recorre + contador 1970 + bandera en etiqueta + rótulo onu nueva york + "
        "marco de luz azul de la sala")


def t_onu(t, ta, tb):
    n = "tratado_onu.jpg" if IMGX("tratado_onu.jpg") else "tratado_estambul.jpg"
    lz = foto(n, t, ta, tb, 1.05, 1.22, (0.5, 0.45), (0.5, 0.55), oscuro=0.72)
    lz += np.float32((0.0, 0.02, 0.05))
    barrido_luz(lz, t, ta + 1.2, dur=2.0, color=(1.0, 0.75, 0.5), op=0.35)
    contador(lz, t, T("tratado_5", "1970") - 0.6 if _tiene("tratado_5", "1970") else ta + 2, 1.0, 1259, 1970, W * 0.80, H * 0.20, px=70, color=A.BLANCO)
    A.rotulo_serif(lz, [("ONU · ", A.BLANCO), ("NUEVA YORK", A.ROJO)], W * 0.5, H * 0.88, t, T("tratado_5", "onu") - 0.1, px=48)
    A.etiqueta(lz, "Réplica en cobre · regalo de Turquía", W * 0.05, H * 0.10, t, T("tratado_5", "cobre"), px=28)
    return lz


A.firma("t_boda", "caravana de la princesa hitita de flow con paneo lateral largo + pétalos/polvo dorado que cae + aros entrelazados de luz (egipto y hatti) + "
        "rótulo boda diplomática")


def t_boda(t, ta, tb):
    lz = cine("princesa", t, ta, tb, 1.18, 1.18, (0.38, 0.5), (0.62, 0.5))
    particulas(lz, t, sem=55, n=90, v=(30, 50), tam=(1.5, 3), color=(1.0, 0.85, 0.45), op=0.6, parpadeo=0.4)
    t_c = T("tratado_6", "caso")
    u = e_out(prog(t, t_c - 0.2, t_c + 0.8))
    if u > 0:
        capa = np.zeros((H, W), np.float32)
        cv2.circle(capa, (int(W * 0.46), int(H * 0.24)), int(70 * u), 1.0, 3, cv2.LINE_AA)
        cv2.circle(capa, (int(W * 0.54), int(H * 0.24)), int(70 * u), 1.0, 3, cv2.LINE_AA)
        lz += (capa + cv2.GaussianBlur(capa, (0, 0), 8) * 1.4)[..., None] * np.float32((1.0, 0.8, 0.45)) * 0.9
    A.rotulo_serif(lz, [("BODA ", A.BLANCO), ("DIPLOMÁTICA", A.ROJO)], W * 0.5, H * 0.86, t, T("tratado_6", "princesa") - 0.2, px=46)
    A.texto_mixto(lz, [("El pacto", A.BLANCO), ("se sella con una boda", A.GRIS)], W * 0.06, H * 0.10, t, T("tratado_6", "pacto"), px=34)
    return lz


# ------------------------------------------------------------------ cap. 4: EL CONSTRUCTOR
A.firma("c_nombre", "cartucho de ramsés real sobre piedra con luz rasante que lo recorre + el nombre ramsés que se talla letra a letra con chispas + "
        "texto escribir su nombre en piedra + polvo de piedra que cae")


def c_nombre(t, ta, tb):
    lz = A.piedra(sem=60, tono=(0.14, 0.13, 0.12))
    if IMGX("cartucho_ramses.jpg"):
        A.camafeo(lz, IMG + "cartucho_ramses.jpg", W * 0.30, H * 0.50, 300, t, ta + 0.2, foco=(0.5, 0.5), zoom=1.0)
    t_n = T("constructor_0", "nombre")
    A.rotulo_serif(lz, [("RAMSÉS", A.ROJO)], W * 0.68, H * 0.46, t, t_n - 0.4, px=110, vel=0.12)
    for k in range(6):
        tk = t_n - 0.4 + 0.12 * k
        if tk < t < tk + 0.5:
            particulas(lz, t - tk, sem=61 + k, n=25, v=(80, -120), tam=(1, 2), color=(1, 0.85, 0.5), op=0.9,
                       zona=(int(W * (0.52 + 0.055 * k)), int(H * 0.42), int(W * (0.56 + 0.055 * k)), int(H * 0.5)))
    A.texto_mixto(lz, [("Lo que mejor sabía hacer:", A.GRIS), ("escribir su nombre en piedra", A.BLANCO)], W * 0.5, H * 0.82, t,
                  T("constructor_0", "escribir") - 0.3, px=38, alinear="centro")
    A.polvo(lz, t, n=70, sem=66, op=0.4)
    yy = (np.arange(W, dtype=np.float32)[None, :] - lerp(-400, W + 400, prog(t, ta, tb)))
    lz *= (1 + 0.35 * np.exp(-(yy / 260.0) ** 2))[..., None]
    return camara(lz, t, ta, tb, 1.02, 1.0)


A.firma("c_piramses", "vista aérea de pi-ramsés de flow con vuelo lento hacia el delta + barcos (puntos de luz) que navegan los canales + "
        "punto del delta en minimapa que late + rótulo la casa de ramsés")


def c_piramses(t, ta, tb):
    lz = cine("piramses", t, ta, tb, 1.0, 1.25, (0.5, 0.6), (0.55, 0.45))
    for k in range(10):
        x = (W * 0.2 + (t - ta) * (20 + k * 4) + k * 170) % W
        y = H * (0.55 + 0.03 * math.sin(k * 1.7))
        cv2.circle(lz, (int(x), int(y)), 3, (1.0, 0.85, 0.55), -1, cv2.LINE_AA)
    mini = cv2.resize(toma("mapa_medit", 0, 0, 1, z0=1.0, z1=1.0, par=(0, 0)), (W // 5, H // 5), interpolation=cv2.INTER_AREA) * 0.85
    x0, y0 = int(W * 0.77), int(H * 0.06)
    k = smooth(prog(t, ta + 0.6, ta + 1.3))
    lz[y0:y0 + mini.shape[0], x0:x0 + mini.shape[1]] = lz[y0:y0 + mini.shape[0], x0:x0 + mini.shape[1]] * (1 - k) + mini * k
    cv2.rectangle(lz, (x0, y0), (x0 + mini.shape[1], y0 + mini.shape[0]), (0.9 * k, 0.85 * k, 0.75 * k), 2)
    px_, py_ = x0 + 1060 / 5, y0 + 820 / 5
    cv2.circle(lz, (int(px_), int(py_)), int(6 + 3 * math.sin(t * 5)), (1.0 * k, 0.2 * k, 0.15 * k), -1, cv2.LINE_AA)
    A.rotulo_serif(lz, [("PI-RAMSÉS · ", A.BLANCO), ("LA CASA DE RAMSÉS", A.ROJO)], W * 0.42, H * 0.88, t, T("constructor_1", "pi") - 0.1 if _tiene("constructor_1", "pi") else ta + 2, px=44)
    return lz


A.firma("c_rameseo", "rameseo real con paneo + regla vertical de escala que sube hasta 20 m junto a una silueta humana diminuta + contador de metros + "
        "texto su templo funerario")


def c_rameseo(t, ta, tb):
    n = "rameseo_vista.jpg" if IMGX("rameseo_vista.jpg") else "rameseo_coloso.jpg"
    lz = foto(n, t, ta, tb, 1.08, 1.22, (0.45, 0.5), (0.55, 0.45), oscuro=0.70)
    t_v = T("constructor_2", "veinte") if _tiene("constructor_2", "veinte") else fs("constructor_2") + 5
    u = e_inout(prog(t, t_v - 1.0, t_v + 0.4))
    x, yb = W * 0.86, H * 0.86
    ytop = yb - u * H * 0.66
    cv2.line(lz, (int(x), int(yb)), (int(x), int(ytop)), (0.95, 0.9, 0.8), 3, cv2.LINE_AA)
    for k in range(11):
        yy = yb - k * H * 0.066
        if yy >= ytop:
            cv2.line(lz, (int(x - 12), int(yy)), (int(x + 12), int(yy)), (0.95, 0.9, 0.8), 2, cv2.LINE_AA)
    cv2.ellipse(lz, (int(x - 40), int(yb - 22)), (5, 5), 0, 0, 360, (0.95, 0.9, 0.8), -1)
    cv2.line(lz, (int(x - 40), int(yb - 16)), (int(x - 40), int(yb)), (0.95, 0.9, 0.8), 3)
    contador(lz, t, t_v - 1.0, 1.4, 0, 19, x - 70, ytop - 40, px=54, sufijo=" m", color=A.ROJO_HALO)
    A.texto_mixto(lz, [("El Rameseo:", A.BLANCO), ("su templo funerario en Tebas", A.GRIS)], W * 0.06, H * 0.10, t, T("constructor_2", "tebas") - 0.4, px=36)
    return lz


A.firma("c_abusimbel", "fachada real de abu simbel con empuje + cuatro aros de luz que se posan uno a uno sobre las caras de los colosos + x4 + "
        "contador más de 3 000 años + montaña tallada con rótulo nubia")


def c_abusimbel(t, ta, tb):
    lz = foto("Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", t, ta, tb, 1.02, 1.10, (0.5, 0.45), (0.5, 0.42), oscuro=0.78)
    t_m = T("constructor_3", "montana") if _tiene("constructor_3", "montana") else fs("constructor_3") + 3
    A.rotulo_serif(lz, [("NUBIA · ", A.BLANCO), ("ABU SIMBEL", A.ROJO)], W * 0.5, H * 0.08, t, t_m, px=48, salida=fs("constructor_4") + 2)
    t_c = T("constructor_4", "colosos") if _tiene("constructor_4", "colosos") else fs("constructor_4") + 0.6
    for i, fx in enumerate((0.20, 0.38, 0.62, 0.80)):
        aro(lz, W * fx, H * 0.36, 70, t, t_c + 0.25 * i, color=A.ORO, op=0.8)
    A.rotulo_serif(lz, [("×4 · ", A.ROJO), ("TODOS CON SU CARA", A.BLANCO)], W * 0.5, H * 0.08, t, T("constructor_4", "cara") - 0.2 if _tiene("constructor_4", "cara") else t_c + 2, px=44)
    contador(lz, t, T("constructor_4", "tres") - 0.3 if _tiene("constructor_4", "tres") else t_c + 3, 1.2, 0, 3000, W * 0.5, H * 0.86, px=64,
             sufijo=" años vigilando el río", color=A.BLANCO)
    return lz


A.firma("c_sol", "pasillo del santuario de flow en penumbra + rayo de sol que avanza por el pasillo y enciende las cuatro estatuas + motas en el rayo + "
        "calendario 22 de febrero y 22 de octubre que se marca con círculo rojo")


def c_sol(t, ta, tb):
    lz = cine("sol_santuario", t, ta, tb, 1.10, 1.30, (0.55, 0.5), (0.62, 0.5))
    t_s = T("constructor_5", "sol") if _tiene("constructor_5", "sol") else fs("constructor_5") + 5
    luz = smooth(prog(t, t_s - 0.5, t_s + 2.5))
    lz *= 0.45 + 0.55 * luz
    rayos(lz, t, W * 0.95, H * 0.18, op=0.35 * luz, color=(1.0, 0.8, 0.45), n=10, sem=70)
    particulas(lz, t, sem=71, n=120, v=(-30, 12), tam=(1, 2.2), color=(1.0, 0.9, 0.6), op=0.6 * luz, zona=(int(W * 0.4), 0, W, int(H * 0.7)))
    for i, (pal, txt) in enumerate((("febrero", "22 FEB"), ("octubre", "22 OCT"))):
        tc = T("constructor_5", pal) if _tiene("constructor_5", pal) else fs("constructor_5") + 2 + 2 * i
        x, y = W * (0.10 + 0.17 * i), H * 0.16
        k = e_out(prog(t, tc - 0.2, tc + 0.3))
        if k > 0:
            cv2.rectangle(lz, (int(x - 70), int(y - 50)), (int(x + 70), int(y + 50)), (0.92 * k, 0.88 * k, 0.8 * k), 2, cv2.LINE_AA)
            A.rotulo_serif(lz, [(txt, A.BLANCO)], x, y, t, tc - 0.1, px=36)
            D.marcador_mano(lz, "circulo", x, y, 170, 120, e_out(prog(t, tc + 0.3, tc + 0.9)), semilla=i)
    A.texto_mixto(lz, [("El sol del amanecer", A.BLANCO), ("alumbra su estatua", A.GRIS)], W * 0.06, H * 0.86, t, T("constructor_5", "alumbra") - 0.2 if _tiene("constructor_5", "alumbra") else t_s, px=36)
    return lz


A.firma("c_borrar", "manos de flow con el cincel que borra un cartucho + chispas de piedra en ráfagas + nombre viejo en gris tachado y ramsés en rojo que se escribe "
        "encima + pantalla que se llena de cartuchos rojos (su nombre por todo egipto)")


def c_borrar(t, ta, tb):
    lz = cine("cincel", t, ta, tb, 1.05, 1.25, (0.45, 0.5), (0.4, 0.5))
    for k in range(5):
        tk = ta + 0.5 + k * 1.3
        if tk < t < tk + 0.5:
            particulas(lz, t - tk, sem=75 + k, n=40, v=(160, -140), tam=(1, 2.4), color=(1, 0.85, 0.55), op=0.9,
                       zona=(int(W * 0.40), int(H * 0.40), int(W * 0.48), int(H * 0.50)))
    t_b = T("constructor_6", "borrar")
    A.rotulo_serif(lz, [("NOMBRE ANTERIOR", A.GRIS)], W * 0.76, H * 0.30, t, t_b - 0.2, px=40)
    D.marcador_mano(lz, "tachado", W * 0.76, H * 0.30, 420, 60, e_out(prog(t, t_b + 0.6, t_b + 1.2)), semilla=2)
    A.rotulo_serif(lz, [("RAMSÉS", A.ROJO)], W * 0.76, H * 0.42, t, T("constructor_6", "suyo") - 0.2 if _tiene("constructor_6", "suyo") else t_b + 2, px=70)
    t_t = T("constructor_7", "todo")
    n = int(28 * e_out(prog(t, t_t - 0.3, t_t + 2.0)))
    rng = np.random.default_rng(77)
    pts = rng.random((28, 2))
    for k in range(n):
        x, y = W * (0.05 + 0.9 * pts[k, 0]), H * (0.08 + 0.84 * pts[k, 1])
        cv2.ellipse(lz, (int(x), int(y)), (46, 18), 0, 0, 360, (0.9, 0.12, 0.1), 2, cv2.LINE_AA)
        cv2.line(lz, (int(x + 46), int(y - 14)), (int(x + 46), int(y + 14)), (0.9, 0.12, 0.1), 2, cv2.LINE_AA)
    A.cursiva_luz(lz, "SOBRE OBRAS QUE NO ERAN SUYAS", W * 0.5, H * 0.88, t, T("constructor_7", "obras") - 0.2, px=40, color=A.ROJO_HALO)
    return lz


# ------------------------------------------------------------------ cap. 5: LA FAMILIA
A.firma("f_nefertari", "reina de flow que camina por el pasillo con paneo que la acompaña + pétalos de luz + camafeo de la tumba qv66 real que flota + "
        "rótulo gran esposa real + aura dorada")


def f_nefertari(t, ta, tb):
    lz = cine("nefertari_reina", t, ta, tb, 1.15, 1.15, (0.42, 0.5), (0.58, 0.5))
    lz *= np.float32(0.86 + 0.06 * math.sin(t * 3.1))
    particulas(lz, t, sem=80, n=70, v=(10, -25), tam=(1, 2.5), color=(1.0, 0.85, 0.55), op=0.55, parpadeo=0.5)
    A.rotulo_serif(lz, [("NEFERTARI", A.ROJO)], W * 0.24, H * 0.16, t, T("familia_0", "nefertari") - 0.1, px=62)
    A.cursiva_luz(lz, "GRAN ESPOSA REAL", W * 0.24, H * 0.27, t, T("familia_0", "esposa"), px=34)
    A.camafeo(lz, IMG + "nefertari_qv66.jpg", W * 0.80, H * 0.60, 170, t, T("familia_0", "tumba") - 0.2, foco=(0.5, 0.35), zoom=1.4)
    A.etiqueta(lz, "Tumba QV66 · Valle de las Reinas", W * 0.66, H * 0.86, t, T("familia_0", "valle") - 0.2 if _tiene("familia_0", "valle") else ta + 6, px=26)
    return lz


A.firma("f_esposas", "árbol genealógico de luz sobre negro: ramsés en el centro, esposas reales como nodos dorados y decenas de esposas menores como "
        "constelación de puntos que aparecen + líneas que se trazan")


def f_esposas(t, ta, tb):
    lz = negro()
    A.polvo(lz, t, n=60, sem=81, op=0.3)
    cx, cy = W * 0.5, H * 0.52
    A.camafeo(lz, IMG + "luxor_ramses.jpg", cx, cy, 110, t, ta, foco=(0.5, 0.25), zoom=2.2)
    t_v = T("familia_1", "varias")
    for i in range(7):
        ang = -math.pi / 2 + i * 2 * math.pi / 7
        x, y = cx + 300 * math.cos(ang), cy + 260 * math.sin(ang)
        k = e_out(prog(t, t_v + 0.15 * i, t_v + 0.15 * i + 0.4))
        if k > 0:
            cv2.line(lz, (int(cx), int(cy)), (int(lerp(cx, x, k)), int(lerp(cy, y, k))), (0.8 * k, 0.65 * k, 0.35 * k), 2, cv2.LINE_AA)
            cv2.circle(lz, (int(x), int(y)), 18, (1.0 * k, 0.78 * k, 0.35 * k), -1, cv2.LINE_AA)
    t_d = T("familia_1", "decenas")
    rng = np.random.default_rng(82)
    pts = rng.random((60, 2))
    n = int(60 * e_out(prog(t, t_d - 0.2, t_d + 1.8)))
    for k in range(n):
        ang = pts[k, 0] * 2 * math.pi
        r = 420 + 160 * pts[k, 1]
        x, y = cx + r * math.cos(ang) * 1.5, cy + r * math.sin(ang) * 0.85
        cv2.circle(lz, (int(x), int(y)), 5, (0.75, 0.75, 0.8), -1, cv2.LINE_AA)
    A.texto_mixto(lz, [("Varias esposas reales", A.BLANCO), ("y decenas de esposas menores", A.GRIS)], W * 0.5, H * 0.92, t, t_v, px=34, alinear="centro")
    A.rotulo_serif(lz, [("NO FUE LA ", A.BLANCO), ("ÚNICA", A.ROJO)], W * 0.5, H * 0.08, t, fs("familia_1"), px=44)
    return camara(lz, t, ta, tb, 1.08, 1.0, rot=(-0.6, 0.6))


A.firma("f_hijos", "cien figuras de hijos e hijas (dos colores) que se encienden en una cuadrícula al ritmo del contador + friso real de la procesión de hijos "
        "que corre abajo + rótulo muchos")


def f_hijos(t, ta, tb):
    lz = negro()
    if IMGX("hijos_procesion.jpg"):
        banda_relieve(lz, IMG + "hijos_procesion.jpg", H * 0.88, 200, t, ta, vel=40, color=(0.85, 0.72, 0.5), op=0.35)
    A.neon(lz, "MUCHOS", W * 0.5, H * 0.12, t, T("familia_2", "muchos") - 0.1, px=80, barras=False)
    t_l = T("familia_2", "cincuenta") if _tiene("familia_2", "cincuenta") else fs("familia_2") + 3
    n = int(100 * e_out(prog(t, t_l - 0.6, fe("familia_2"))))
    for k in range(n):
        fila, col = divmod(k, 20)
        x, y = W * 0.18 + col * 62, H * 0.30 + fila * 82
        c = (0.95, 0.78, 0.40) if k < 50 else (0.95, 0.35, 0.30)
        cv2.circle(lz, (int(x), int(y - 18)), 9, c, -1, cv2.LINE_AA)
        cv2.ellipse(lz, (int(x), int(y + 10)), (12, 20), 0, 180, 360, c, -1, cv2.LINE_AA)
    contador(lz, t, t_l - 0.6, 2.2, 0, 50, W * 0.30, H * 0.76, px=54, sufijo=" hijos", color=(0.95, 0.78, 0.4))
    contador(lz, t, t_l + 0.8, 1.6, 0, 50, W * 0.70, H * 0.76, px=54, sufijo=" hijas", color=A.ROJO_HALO)
    return camara(lz, t, ta, tb, 1.0, 1.05)


A.firma("f_kv5", "arqueólogo de flow que se arrastra con linterna (haz que barre) + plano de la kv5 que se dibuja con trazo de luz pasillo a pasillo + "
        "contador más de 100 cámaras + rótulo kv5 1995")


def f_kv5(t, ta, tb):
    lz = cine("kv5_pasillo", t, ta, tb, 1.05, 1.30, (0.5, 0.5), (0.5, 0.45))
    lz *= np.float32(0.75 + 0.1 * math.sin(t * 5.3) * math.sin(t * 1.7))
    A.rotulo_serif(lz, [("KV5 · ", A.ROJO), ("1995", A.BLANCO)], W * 0.18, H * 0.10, t, T("familia_3", "1995") if _tiene("familia_3", "1995") else ta + 0.5, px=50)
    A.etiqueta(lz, "Kent Weeks, egiptólogo", W * 0.05, H * 0.20, t, T("familia_3", "weeks") - 0.3 if _tiene("familia_3", "weeks") else ta + 2, px=28)
    t_p = T("familia_4", "pasillos") if _tiene("familia_4", "pasillos") else fs("familia_4") + 2
    u = e_inout(prog(t, t_p - 0.8, fe("familia_4") - 2))
    if u > 0:
        lz *= 1 - 0.4 * u
        x0, y0 = W * 0.62, H * 0.18
        traz = [(0, 0), (0, 160), (-180, 160), (180, 160), (0, 160), (0, 420), (-220, 420), (220, 420), (0, 420), (0, 520), (-140, 620), (140, 620)]
        segs = [(traz[i], traz[i + 1]) for i in range(len(traz) - 1)]
        m = int(len(segs) * u)
        for (a, b) in segs[:m]:
            cv2.line(lz, (int(x0 + a[0]), int(y0 + a[1])), (int(x0 + b[0]), int(y0 + b[1])), (0.95, 0.9, 0.75), 4, cv2.LINE_AA)
        for k in range(int(40 * u)):
            sx = x0 + ((k * 53) % 440) - 220
            sy = y0 + 160 + (k // 9) * 100
            cv2.rectangle(lz, (int(sx - 10), int(sy - 8)), (int(sx + 10), int(sy + 8)), (0.95, 0.9, 0.75), 1, cv2.LINE_AA)
    contador(lz, t, T("familia_4", "cien") - 0.6 if _tiene("familia_4", "cien") else t_p + 2, 1.2, 0, 100, W * 0.24, H * 0.78, px=72, sufijo="+ cámaras", color=A.ROJO_HALO)
    A.cursiva_luz(lz, "LA TUMBA DE SUS HIJOS", W * 0.30, H * 0.90, t, T("familia_4", "tumba") - 0.2 if _tiene("familia_4", "tumba") else fe("familia_4") - 3, px=36)
    return lz


A.firma("f_herederos", "doce velas en fila sobre piedra que se apagan una a una con humo (los doce herederos) + contador de herederos enterrados + "
        "cursiva el precio de su leyenda")


def f_herederos(t, ta, tb):
    lz = A.piedra(sem=85, tono=(0.09, 0.09, 0.1))
    t_d = T("familia_5", "doce")
    A.cursiva_luz(lz, "EL PRECIO DE SU LEYENDA", W * 0.5, H * 0.14, t, T("familia_5", "precio") - 0.2, px=50)
    for i in range(12):
        x = W * (0.12 + 0.07 * i)
        y = H * 0.62
        apag = t > t_d - 0.8 + 0.18 * i
        cv2.rectangle(lz, (int(x - 12), int(y)), (int(x + 12), int(y + 120)), (0.78, 0.74, 0.66), -1)
        if not apag:
            fl = 1 + 0.12 * math.sin(t * 13 + i)
            cv2.ellipse(lz, (int(x), int(y - 16)), (int(7 * fl), int(16 * fl)), 0, 0, 360, (1.0, 0.75, 0.3), -1, cv2.LINE_AA)
            g = np.zeros((H, W), np.float32)
            cv2.circle(g, (int(x), int(y - 16)), 40, 1.0, -1)
            lz += cv2.GaussianBlur(g, (0, 0), 30)[..., None] * np.float32((0.5, 0.3, 0.1)) * 0.6
        else:
            ts = t - (t_d - 0.8 + 0.18 * i)
            if ts < 1.5:
                cv2.circle(lz, (int(x + 6 * math.sin(ts * 4)), int(y - 20 - ts * 50)), int(6 + ts * 10), (0.45, 0.45, 0.45), -1, cv2.LINE_AA)
    contador(lz, t, t_d - 0.8, 2.2, 0, 12, W * 0.5, H * 0.40, px=90, sufijo=" herederos", color=A.ROJO_HALO)
    return camara(lz, t, ta, tb, 1.0, 1.06)


A.firma("f_muerte", "cara real de la momia muy cerca con luz de quirófano que la recorre + flechas finas de diagnóstico (artritis, dientes) que se trazan + "
        "contadores 66 años de reinado y 90 años + fechas 1279-1213 a. c.")


def f_muerte(t, ta, tb):
    lz = foto("momia_cara.JPG", t, ta, tb, 1.20, 1.38, (0.5, 0.40), (0.5, 0.46), oscuro=0.70)
    barrido_luz(lz, t, ta + 0.5, dur=3.0, color=(0.85, 0.9, 1.0), op=0.25, ang=1.2)
    contador(lz, t, fs("familia_6"), 1.5, 0, 66, W * 0.16, H * 0.16, px=80, sufijo=" años", color=A.ROJO_HALO)
    A.etiqueta(lz, "de reinado · 1279-1213 a. C.", W * 0.05, H * 0.26, t, fs("familia_6") + 0.8, px=26)
    t_n = T("familia_6", "noventa") if _tiene("familia_6", "noventa") else fs("familia_6") + 6
    contador(lz, t, t_n - 0.5, 1.0, 0, 90, W * 0.84, H * 0.16, px=80, sufijo=" años", color=A.BLANCO)
    for i, (pal, txt, p0, p1) in enumerate((("artritico", "artritis", (W * 0.70, H * 0.62), (W * 0.86, H * 0.74)),
                                             ("dientes", "abscesos en los dientes", (W * 0.50, H * 0.70), (W * 0.20, H * 0.82)))):
        tc = T("familia_6", pal) if _tiene("familia_6", pal) else fe("familia_6") - 2 + i
        u = e_out(prog(t, tc - 0.2, tc + 0.5))
        if u > 0:
            cv2.line(lz, (int(p0[0]), int(p0[1])), (int(lerp(p0[0], p1[0], u)), int(lerp(p0[1], p1[1], u))), (0.95, 0.95, 0.95), 2, cv2.LINE_AA)
            cv2.circle(lz, (int(p0[0]), int(p0[1])), 8, (0.95, 0.2, 0.15), -1, cv2.LINE_AA)
            A.etiqueta(lz, txt, p1[0] - (0 if p1[0] > W / 2 else 150), p1[1] + 34, t, tc + 0.3, px=26, punto=False)
    return lz


A.firma("f_merenptah", "estatua real de merenptah que sube y gira sobre pizarra con franja de luz + número 13 gigante detrás en contorno + "
        "corona que pasa de un camafeo de ramsés a él con arco de luz + texto otro faraón")


def f_merenptah(t, ta, tb):
    lz = A.piedra(sem=88) * 0.85
    A.rotulo_serif(lz, [("13", (0.30, 0.30, 0.32))], W * 0.68, H * 0.48, t, ta, px=420, vel=0.0, glow=0.0)
    png = IMGX("merenptah_rec.png")
    if png:
        A.artefacto(lz, png, W * 0.66, H * 0.54, 760, t, T("familia_7", "merenptah") - 0.4 if _tiene("familia_7", "merenptah") else ta + 1, giro=9.0)
    A.camafeo(lz, IMG + "joven_memnon.jpg", W * 0.20, H * 0.32, 120, t, ta + 0.2, foco=(0.5, 0.3), zoom=1.6)
    u = e_inout(prog(t, ta + 1.0, ta + 2.4))
    A.arco_luz(lz, (W * 0.26, H * 0.32), (W * 0.56, H * 0.22), -60, u * 1.2)
    A.rotulo_serif(lz, [("MERENPTAH · ", A.BLANCO), ("HIJO N.º 13", A.ROJO)], W * 0.30, H * 0.70, t, T("familia_7", "hijo") - 0.2 if _tiene("familia_7", "hijo") else ta + 2, px=40)
    A.texto_mixto(lz, [("La mayoría no había conocido", A.GRIS), ("otro faraón", A.BLANCO)], W * 0.06, H * 0.86, t, T("familia_7", "mayoria") - 0.2, px=34)
    return camara(lz, t, ta, tb, 1.0, 1.05)


# ------------------------------------------------------------------ cap. 6: EL ESCONDITE
A.firma("e_viaje", "sacerdotes de flow con antorchas que llevan las momias por el acantilado + antorchas que laten + ruta punteada valle de los reyes → "
        "deir el-bahari sobre el acantilado + rótulo otro viaje + brasas")


def e_viaje(t, ta, tb):
    lz = cine("sacerdotes_momias", t, ta, tb, 1.06, 1.24, (0.45, 0.5), (0.60, 0.5))
    lz *= np.float32(0.82 + 0.1 * math.sin(t * 6.7) * math.sin(t * 2.3))
    particulas(lz, t, sem=90, n=80, v=(10, -100), tam=(1, 2.4), color=(1.0, 0.6, 0.2), op=0.7, parpadeo=0.6)
    A.cursiva_luz(lz, "OTRO VIAJE", W * 0.5, H * 0.12, t, T("escondite_0", "viaje") - 0.3, px=56, salida=fs("escondite_1") + 1)
    t_l = T("escondite_1", "ladrones")
    A.estampa(lz, "SAQUEADA", W * 0.78, H * 0.20, t, t_l + 0.3, px=46) if hasattr(A, "estampa") else D.estampa(lz, "SAQUEADA", W * 0.78, H * 0.20, t, t_l + 0.3, px=46)
    t_d = T("escondite_1", "deir") if _tiene("escondite_1", "deir") else fe("escondite_1") - 2
    u = e_inout(prog(t, t_d - 1.5, t_d + 0.5))
    D.linea_punteada(lz, [(W * 0.10, H * 0.78), (W * 0.30, H * 0.70), (W * 0.50, H * 0.74), (W * 0.70, H * 0.66)], u, grosor=4, color=(1.0, 0.86, 0.6))
    A.etiqueta(lz, "Valle de los Reyes", W * 0.04, H * 0.86, t, t_d - 1.5, px=26)
    A.etiqueta(lz, "Deir el-Bahari", W * 0.66, H * 0.60, t, t_d, px=28)
    return lz


A.firma("e_1881", "ataúdes que salen del pozo (flow) con cuerdas + tono sepia de foto de época con rayas de película + contador casi 3 000 años + "
        "sello 1881 que cae + pieza por pieza: siluetas de objetos que se van")


def e_1881(t, ta, tb):
    lz = cine("ataudes_1881", t, ta, tb, 1.05, 1.20, (0.5, 0.45), (0.5, 0.55))
    g = lz.mean(-1, keepdims=True)
    sep = smooth(prog(t, T("escondite_2", "familia") if _tiene("escondite_2", "familia") else ta + 3, fe("escondite_2") - 3))
    lz[:] = lz * (1 - sep) + g * np.float32((1.05, 0.9, 0.7)) * sep
    rng = np.random.default_rng(int(t * 24))
    for _ in range(3):
        x = int(rng.random() * W)
        cv2.line(lz, (x, 0), (x, H), (0.8, 0.75, 0.65), 1)
    contador(lz, t, fs("escondite_2"), 1.6, 0, 3000, W * 0.5, H * 0.14, px=74, sufijo=" años dormido", color=A.BLANCO, salida=fs("escondite_2") + 4)
    A.texto_mixto(lz, [("Pieza", A.BLANCO), ("por pieza", A.GRIS)], W * 0.06, H * 0.86, t, T("escondite_2", "pieza") - 0.2 if _tiene("escondite_2", "pieza") else ta + 6, px=40)
    D.estampa(lz, "1881", W * 0.78, H * 0.22, t, T("escondite_2", "1881") - 0.2 if _tiene("escondite_2", "1881") else fe("escondite_2") - 3, px=70)
    return lz


# ------------------------------------------------------------------ cap. 7: OZYMANDIAS
A.firma("o_belzoni", "cientos de hombres de flow arrastrando el busto con calima que ondula + polvo lateral + ruta punteada tebas → londres sobre un mini mapa + "
        "contador 1816 + rótulo rumbo a londres")


def o_belzoni(t, ta, tb):
    lz = cine("belzoni_arrastre", t, ta, tb, 1.18, 1.18, (0.40, 0.5), (0.58, 0.48))
    off = (np.sin(np.arange(H, dtype=np.float32)[:, None] * 0.05 + t * 6) * 2).astype(np.float32)
    lz[:] = cv2.remap(lz, (np.arange(W, dtype=np.float32)[None, :] + off), np.repeat(np.arange(H, dtype=np.float32)[:, None], W, 1), cv2.INTER_LINEAR)
    particulas(lz, t, sem=95, n=150, v=(160, -10), tam=(1, 2), color=(0.95, 0.82, 0.6), op=0.35, estela=0.03)
    contador(lz, t, ta + 0.4, 1.0, 1700, 1816, W * 0.14, H * 0.12, px=74, color=A.BLANCO)
    A.etiqueta(lz, "Giovanni Belzoni", W * 0.05, H * 0.22, t, T("ozymandias_0", "belzoni") - 0.2 if _tiene("ozymandias_0", "belzoni") else ta + 3, px=28)
    A.rotulo_serif(lz, [("TEBAS → ", A.BLANCO), ("LONDRES", A.ROJO)], W * 0.70, H * 0.88, t, T("ozymandias_0", "londres") - 0.4 if _tiene("ozymandias_0", "londres") else fe("ozymandias_0") - 1, px=46)
    return lz


A.firma("o_shelley", "poeta de flow escribiendo a la luz de vela con llama que tiembla + lluvia en la ventana + letras del título ozymandias que se escriben en "
        "cursiva luminosa + ecuación ozymandias = ramsés con camafeo")


def o_shelley(t, ta, tb):
    lz = cine("poeta", t, ta, tb, 1.05, 1.22, (0.45, 0.55), (0.40, 0.5))
    lz *= np.float32(0.82 + 0.10 * math.sin(t * 9.3) * math.sin(t * 3.1))
    particulas(lz, t, sem=96, n=90, v=(-20, 380), tam=(1, 1.5), color=(0.7, 0.8, 0.9), op=0.35, estela=0.05, zona=(int(W * 0.55), 0, W, int(H * 0.55)))
    A.texto_mixto(lz, [("Percy Shelley,", A.BLANCO), ("1818", A.GRIS)], W * 0.06, H * 0.10, t, T("ozymandias_1", "shelley") - 0.2 if _tiene("ozymandias_1", "shelley") else ta + 2, px=36)
    t_o = T("ozymandias_1", "ozymandias") if _tiene("ozymandias_1", "ozymandias") else (T("ozymandias_1", "osimandias") if _tiene("ozymandias_1", "osimandias") else fs("ozymandias_1") + 7)
    A.cursiva_luz(lz, "OZYMANDIAS", W * 0.5, H * 0.46, t, t_o - 0.2, px=96)
    t_g = T("ozymandias_1", "griegos") if _tiene("ozymandias_1", "griegos") else t_o + 1.5
    A.rotulo_serif(lz, [("= ", A.GRIS), ("RAMSÉS", A.ROJO)], W * 0.5, H * 0.60, t, t_g, px=56)
    return lz


A.firma("o_poema", "piernas de piedra en el desierto de flow + arena que barre en ráfagas cada vez más fuerte + cita amarilla de los versos del soneto + "
        "neón nada que se apaga + la arena cubre todo al final")


def o_poema(t, ta, tb):
    lz = cine("ozymandias_desierto", t, ta, tb, 1.04, 1.22, (0.5, 0.5), (0.5, 0.42))
    fuerza = 0.3 + 0.7 * smooth(prog(t, fs("ozymandias_4"), fe("ozymandias_4")))
    particulas(lz, t, sem=97, n=int(160 + 300 * fuerza), v=(-500 * fuerza - 200, 25), tam=(1, 2.2), color=(0.95, 0.8, 0.6), op=0.4, estela=0.06)
    humo(lz, t, sem=98, v=(-220, 0), color=(0.85, 0.72, 0.55), op=0.20 + 0.25 * fuerza, zona_y=(0.5, 1.0))
    A.cita(lz, ["«Mi nombre es Ozymandias, rey de reyes:", "¡mirad mis obras, poderosos, y desesperad!»"], W * 0.5, H * 0.24, t, fs("ozymandias_3") - 0.2,
           px=42, fuente_txt="Percy B. Shelley, «Ozymandias» (1818)", vel=2.5, salida=fs("ozymandias_4") - 0.2)
    A.neon(lz, "NADA", W * 0.5, H * 0.30, t, T("ozymandias_4", "nada") - 0.1, px=110, barras=False)
    cubre = smooth(prog(t, T("ozymandias_4", "arena") - 0.3, tb))
    lz[:] = lz * (1 - 0.8 * cubre) + np.float32((0.55, 0.42, 0.28)) * 0.8 * cubre
    return lz


A.firma("o_presa", "presa real de asuán con paneo + agua azul que sube desde abajo de la pantalla (líquido del kit en azul) hacia abu simbel en camafeo + "
        "contador de nivel + rótulo para siempre")


def o_presa(t, ta, tb):
    n = "presa_asuan.jpg" if IMGX("presa_asuan.jpg") else "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg"
    lz = foto(n, t, ta, tb, 1.05, 1.18, (0.5, 0.5), (0.45, 0.5), oscuro=0.70)
    A.camafeo(lz, IMG + "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", W * 0.74, H * 0.40, 170, t, T("ozymandias_5", "abu") - 0.2 if _tiene("ozymandias_5", "abu") else ta + 3, foco=(0.5, 0.45), zoom=1.3)
    t_i = T("ozymandias_5", "inundar") if _tiene("ozymandias_5", "inundar") else ta + 3
    u = smooth(prog(t, t_i - 0.5, tb))
    A.liquido(lz, 0, H * (1 - 0.55 * u), W, H, 1.0, t, color=(0.10, 0.28, 0.45), sem=9, op=0.75)
    A.rotulo_serif(lz, [("PRESA DE ", A.BLANCO), ("ASUÁN", A.ROJO)], W * 0.30, H * 0.10, t, T("ozymandias_5", "presa") - 0.2 if _tiene("ozymandias_5", "presa") else ta + 1, px=48)
    A.cursiva_luz(lz, "PARA SIEMPRE", W * 0.74, H * 0.66, t, T("ozymandias_5", "siempre") - 0.3 if _tiene("ozymandias_5", "siempre") else fe("ozymandias_5") - 1, px=40)
    return lz


A.firma("o_traslado", "corte de la unesco de flow con grúa que sube la cara + rejilla de bloques numerados que se superpone y se separa + contador 1 000 bloques + "
        "flecha que sube 65 m con regla + años 1964-1968")


def o_traslado(t, ta, tb):
    lz = cine("unesco_corte", t, ta, tb, 1.05, 1.18, (0.5, 0.5), (0.55, 0.42))
    t_c = T("ozymandias_6", "corto") if _tiene("ozymandias_6", "corto") else fs("ozymandias_6") + 1
    u = smooth(prog(t, t_c - 0.2, t_c + 1.5))
    if u > 0:
        paso = 96
        sep = 6 * smooth(prog(t, t_c + 1.0, t_c + 3.0))
        for x in range(0, W, paso):
            cv2.line(lz, (x, 0), (x, H), (0.9 * u, 0.85 * u, 0.7 * u), 1 + int(sep > 2))
        for y in range(0, H, paso):
            cv2.line(lz, (0, y), (W, y), (0.9 * u, 0.85 * u, 0.7 * u), 1 + int(sep > 2))
    contador(lz, t, t_c, 1.5, 0, 1000, W * 0.22, H * 0.12, px=70, sufijo="+ bloques", color=A.ROJO_HALO)
    t_s = T("ozymandias_6", "sesenta") if _tiene("ozymandias_6", "sesenta") else fe("ozymandias_6") - 3
    v = e_inout(prog(t, t_s - 0.5, t_s + 1.0))
    if v > 0:
        x, yb = W * 0.90, H * 0.85
        cv2.arrowedLine(lz, (int(x), int(yb)), (int(x), int(yb - v * H * 0.6)), (0.95, 0.9, 0.8), 6, cv2.LINE_AA, tipLength=0.08)
        contador(lz, t, t_s - 0.5, 1.5, 0, 65, x - 100, yb - v * H * 0.6 - 30, px=56, sufijo=" m", color=A.BLANCO)
    A.etiqueta(lz, "UNESCO · 1964-1968", W * 0.05, H * 0.90, t, T("ozymandias_6", "1964") - 0.2 if _tiene("ozymandias_6", "1964") else ta + 4, px=30)
    return lz


A.firma("o_paris", "laboratorio de parís de flow con luz fría que parpadea + esporas del hongo (puntos verdes) que flotan y se apagan con el destello de la radiación + "
        "símbolo de radiación que gira + rótulo rayos gamma + vuelta a casa")


def o_paris(t, ta, tb):
    lz = cine("paris_lab", t, ta, tb, 1.04, 1.22, (0.5, 0.55), (0.5, 0.48))
    t_h = T("ozymandias_7", "hongo") if _tiene("ozymandias_7", "hongo") else fs("ozymandias_7") + 3
    t_r = T("ozymandias_7", "radiacion") if _tiene("ozymandias_7", "radiacion") else fe("ozymandias_7") - 3
    esporas = smooth(prog(t, t_h - 0.4, t_h + 0.6)) * (1 - smooth(prog(t, t_r, t_r + 0.8)))
    particulas(lz, t, sem=99, n=120, v=(6, -8), tam=(1.5, 3.5), color=(0.5, 0.95, 0.4), op=0.7 * esporas, parpadeo=0.5)
    fl = math.exp(-max(0.0, t - t_r) * 2.0) if t > t_r else 0.0
    lz += np.float32((0.6, 0.8, 1.0)) * 0.6 * fl
    if t > t_r - 0.3:
        c = (int(W * 0.84), int(H * 0.22))
        for k in range(3):
            a0 = math.degrees((t - t_r) * 1.5) + k * 120
            cv2.ellipse(lz, c, (70, 70), 0, a0, a0 + 60, (1.0, 0.85, 0.2), -1, cv2.LINE_AA)
        cv2.circle(lz, c, 16, (1.0, 0.85, 0.2), -1, cv2.LINE_AA)
    A.rotulo_serif(lz, [("PARÍS · ", A.BLANCO), ("1976", A.ROJO)], W * 0.20, H * 0.10, t, T("ozymandias_7", "paris") - 0.2 if _tiene("ozymandias_7", "paris") else ta + 3, px=48)
    A.cursiva_luz(lz, "RAYOS GAMMA", W * 0.70, H * 0.86, t, t_r, px=44)
    return lz


# ------------------------------------------------------------------ cap. 8: CIERRE
A.firma("z_desfile", "desfile dorado de flow de noche con fuegos que destellan + carrozas que avanzan (paneo) + contador 22 reyes y reinas + "
        "rótulo el cairo 2021 + confeti de luz")


def z_desfile(t, ta, tb):
    lz = cine("desfile", t, ta, tb, 1.15, 1.15, (0.40, 0.5), (0.60, 0.5))
    for k in range(4):
        tk = ta + 0.8 + k * 1.9
        if t > tk:
            r = (t - tk) * 260
            g = np.zeros((H, W), np.float32)
            cv2.circle(g, (int(W * (0.2 + 0.2 * k)), int(H * 0.18)), int(r), 1.0, 3, cv2.LINE_AA)
            lz += cv2.GaussianBlur(g, (0, 0), 4)[..., None] * np.float32((1.0, 0.8, 0.4)) * max(0.0, 1 - (t - tk) / 1.2)
    particulas(lz, t, sem=100, n=120, v=(0, 60), tam=(1, 2.5), color=(1.0, 0.85, 0.4), op=0.5, parpadeo=0.6)
    A.rotulo_serif(lz, [("EL CAIRO · ", A.BLANCO), ("2021", A.ROJO)], W * 0.5, H * 0.10, t, ta + 0.5, px=50)
    contador(lz, t, T("cierre_0", "veintiun") - 0.4 if _tiene("cierre_0", "veintiun") else ta + 4, 1.2, 0, 22, W * 0.5, H * 0.86, px=64,
             sufijo=" reyes y reinas", color=A.BLANCO)
    return lz


A.firma("z_balance", "tres recuerdos del video que vuelven como láminas pequeñas que se apilan (cartucho tachado, relieve de kadesh, colosos) + "
        "tres verbos borró, talló, convirtió que se encienden uno por uno + negro con rejilla")


def z_balance(t, ta, tb):
    lz = negro()
    A.rejilla(lz, t, horizonte=0.70, op=0.22, vel=0.3)
    A.cursiva_luz(lz, "QUERÍA QUE NADIE LO OLVIDARA", W * 0.5, H * 0.12, t, fs("cierre_1") - 0.1, px=46)
    recs = [("borro", "BORRÓ", "estatua_usurpada.jpg", "cartucho_ramses.jpg"), ("tallo", "TALLÓ", "kadesh_rameseo.jpg", None),
            ("convirtio", "CONVIRTIÓ", "Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", None)]
    for i, (pal, txt, n1, n2) in enumerate(recs):
        tc = T("cierre_1", pal) if _tiene("cierre_1", pal) else fs("cierre_1") + 2 + 2 * i
        n = n1 if IMGX(n1) else (n2 if n2 and IMGX(n2) else "kadesh_rameseo.jpg")
        x = W * (0.2 + 0.3 * i)
        A.camafeo(lz, IMG + n, x, H * 0.48, 150, t, tc - 0.2, foco=(0.5, 0.45), zoom=1.2)
        A.rotulo_serif(lz, [(txt, A.ROJO)], x, H * 0.74, t, tc - 0.1, px=46)
    return camara(lz, t, ta, tb, 1.0, 1.06)


A.firma("z_pasaporte", "vuelve el pasaporte del principio con la profesión rey y el sello rojo fallecido que cae + cara real de la momia en la foto + "
        "rótulo 3 000 años después + polvo")


def z_pasaporte(t, ta, tb):
    lz = negro()
    A.polvo(lz, t, n=80, sem=101, op=0.4)
    tj = _tarjeta()
    u = e_out(prog(t, ta, ta + 1.0))
    if u > 0:
        sp = D.Sprite(tj[..., :3], tj[..., 3]) if tj.shape[-1] == 4 else None
    A.rotulo_serif(lz, [("3 000 AÑOS ", A.BLANCO), ("DESPUÉS", A.ROJO)], W * 0.5, H * 0.10, t, T("cierre_2", "tres") - 0.2 if _tiene("cierre_2", "tres") else ta, px=46)
    A.texto_mixto(lz, [("Profesión:", A.GRIS), ("rey", A.BLANCO)], W * 0.5, H * 0.46, t, T("cierre_2", "profesion") - 0.3 if _tiene("cierre_2", "profesion") else ta + 4,
                  px=64, alinear="centro")
    D.estampa(lz, "FALLECIDO", W * 0.5, H * 0.66, t, T("cierre_2", "fallecido") - 0.1 if _tiene("cierre_2", "fallecido") else fe("cierre_2") - 0.6, px=90)
    A.camafeo(lz, IMG + "momia_frontal.JPG", W * 0.16, H * 0.56, 140, t, ta + 0.6, foco=(0.5, 0.32), zoom=1.7)
    return camara(lz, t, ta, tb, 1.0, 1.05)


A.firma("z_final", "rótulo bitácora perdida en versales con línea roja que se traza + pregunta ¿a quién seguimos? en cursiva + siluetas de colosos al fondo "
        "que se funden a negro + polvo")


def z_final(t, ta, tb):
    lz = foto("Abu_Simbel_Ramesses_Temple_front_Egypt_Oct_2004.jpg", t, ta, tb, 1.10, 1.0, (0.5, 0.4), (0.5, 0.45), oscuro=0.22)
    A.polvo(lz, t, n=70, sem=102, op=0.4)
    A.rotulo_serif(lz, [("BITÁCORA ", A.BLANCO), ("PERDIDA", A.ROJO)], W * 0.5, H * 0.40, t, ta + 0.3, px=84)
    u = e_inout(prog(t, ta + 1.0, ta + 2.2))
    cv2.line(lz, (int(W * 0.5 - 380 * u), int(H * 0.50)), (int(W * 0.5 + 380 * u), int(H * 0.50)), (0.9, 0.12, 0.1), 3, cv2.LINE_AA)
    A.cursiva_luz(lz, "¿A QUIÉN SEGUIMOS?", W * 0.5, H * 0.62, t, T("cierre_3", "quien") - 0.3 if _tiene("cierre_3", "quien") else ta + 4, px=50)
    return lz
