# -*- coding: utf-8 -*-
"""Parche 4 de t03: golpe de Estado con personajes separados en el balcón, etiquetas escalonadas y título arriba."""
p = 't03.py'
s = open(p, encoding='utf-8').read()
a = s.index("def cam_golpe(t):")
b = s.index("def _cetro(lz, iso, x, y, z, t):")
nuevo = '''def cam_golpe(t):
    return K(t, [(T_GOLPE, (260, 110, 36, 3.0)), (t_dem, (260, 100, 40, 3.2)), (T_PODER, (260, 96, 42, 3.0)), (t_camb2, (260, 98, 44, 2.9)), (t_fuerza, (260, 100, 44, 2.6)), (T1(E3), (260, 110, 44, 2.3))])


XB = (170, 230, 290, 350)          # posiciones de los cuatro del relevo en el balcón (separados 60 unidades)


@shot(T_GOLPE, bg=lambda t: bg_grad((100, 30, 60), (44, 20, 80), mid=(70, 26, 80), ym=0.5), post=[GRAD], ent=("destello", 0.5))
def p_golpe(lz, t):
    sh = 0.0
    if t_golpe < t < t_golpe + 0.6:
        sh = 12 * (1 - (t - t_golpe) / 0.6)
    cx, cy, cz, zm = cam_golpe(t)
    with lz.grupo(sh * math.sin(t * 90), sh * math.cos(t * 77), 1.0):
        iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
        I.luz(mul=(1.0, 0.92, 0.92), mix=(120, 40, 60), k=0.14)
        U.haces_luz(lz, W / 2, 400, t, n=10, largo=1500, color=(255, 120, 130), alfa=0.10, ancho=0.07)
        PLZ.suelo(lz, iso, t)
        m = PLZ.objetos(t)
        # los soldados toman el balcón por los dos extremos
        entra = e_inout(prog(t, t_golpe, t_estado + 0.4))
        for i, (x, lado) in enumerate(((110, -1), (136, -1), (404, 1), (378, 1))):
            m.add(x - 4, 74, x + 4, 82, 40, (lambda x, i, lado: (lambda lz, iso: G.persona(lz, iso, lerp(x + lado * 90, x, entra), 84, t, "granadero", dir=(0, 1), vel=0.0 if entra > 0.98 else 1.0, seed=1500 + i, h=52, z=40, cara="enojo", accion="vitorea" if t > t_dem else None)))(x, i, lado), fijo=False, clave=x + 90)
        # el relevo del poder: Iturrigaray -> Yermo -> Garibay -> Calleja
        quienes = (("pijama", "miedo"), ("yermo", "enojo"), ("virrey", "serio"), ("dragon", "enojo"))
        tt = [t_pod2 - 0.1, t_camb2 + 0.1, t_manos - 0.2, t_fuerza + 0.4]
        for i, (tp_, emo) in enumerate(quienes):
            ki = 1.0 if i < 2 else e_back(prog(t, tt[i - 1] - 0.15, tt[i - 1] + 0.3))
            if ki > 0.01:
                x = XB[i]
                m.add(x - 4, 74, x + 4, 82, 40, (lambda tp_, x, emo, ki, i: (lambda lz, iso: G.persona(lz, iso, x, 84, t, tp_, dir=(0, 1), seed=1600 + i, h=56 * ki, z=40, cara=emo, accion="habla" if (i == 1 and t > t_camb2) else None)))(tp_, x, emo, ki, i), fijo=False, clave=x + 91)
        # cetro de mando con arcos y destellos entre las manos
        seg = 0
        while seg < 3 and t > tt[seg]:
            seg += 1
        a0 = XB[max(0, seg - 1)]
        a1 = XB[seg]
        u = prog(t, tt[max(0, seg - 1)], tt[max(0, seg - 1)] + 0.55) if seg > 0 else 0.0
        xs = lerp(a0, a1, e_inout(u)) if seg > 0 else XB[0]
        zs = 58 + 40 * math.sin(math.pi * u) if seg > 0 else 58
        m.add(xs - 3, 80, xs + 3, 88, 60, lambda lz, iso: _cetro(lz, iso, xs, 90, zs, t), fijo=False, clave=xs + 95)
        m.dibujar(lz, iso)
        bx, by = 262, 72
        k_b = e_inout(prog(t, t_estado, t_estado + 0.9))
        O.bandera(lz, iso, bx, by, h=110 * max(0.2, k_b), w=50, alto=32, color=(206, 56, 70), t=t, franjas=[((206, 56, 70), 0.25), ((250, 206, 90), 0.5), ((206, 56, 70), 0.25)])
        DC.aves(lz, t, n=8, seed=11, y0=60, y1=240)
        kg = U.pop(t, t_golpe - 0.1, 1.2) * U.salida(t, t_dem + 0.3, 0.3)
        if kg > 0.01:
            P.rotulo(lz, W / 2, 150, "GOLPE DE ESTADO", px=170, k=kg, color=(255, 255, 255))
        k = U.pop(t, t_fuerza - 0.2)
        if k > 0.01:
            U.llamada(lz, W / 2, 980, "por la fuerza", color=U.COL["rojo"], px=84, k=k * U.repop(t, t_fuerza + 0.3), cola=None)
        for i, (lab, col) in enumerate((("Iturrigaray", U.COL["rojo"]), ("Yermo", U.COL["morado"]), ("Garibay", U.COL["azul"]), ("Calleja", U.COL["naranja"]))):
            t0 = t_pod2 - 0.1 if i < 2 else tt[i - 1] + 0.1
            kk = U.pop(t, t0 + (0.0 if i == 0 else 0.25)) * U.salida(t, T1(E3) - 0.2, 0.2)
            if kk > 0.01:
                qx, qy = iso.P(XB[i], 84, 112)
                U.llamada(lz, float(qx), float(qy) - 10 - 66 * (i % 2), lab, color=col, px=34, k=kk, cola="abajo")


'''
s = s[:a] + nuevo + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('ok')
