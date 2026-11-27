# -*- coding: utf-8 -*-
"""campana_dc_topes (27-nov-2026): sátira de 30 s estilo PS1. Daniel Cervantes (la misma malla low poly de campana_dc_lowpoly v3)
en una calle empedrada de Juchipila llena de topes amarillos: un vocho rojo vuela, uno verde rebota en cada «tope» de la voz, se
le cae el mofle y una llanta, Daniel hace berrinche (cara roja, vapor, patada) y con un pisotón TODOS los topes salen volando.
Tiempos: plan.py (de voz/tiempos.json). Receta PS1: texturas de 64 px, render 270×480 sin suavizar, vértices a la rejilla.

  "C:/Program Files/Blender Foundation/Blender 4.2/blender.exe" -b --factory-startup --python topes3d.py -- [--cuadros 10,60] [--salida render]
Escribe render/f_####.png (15 cps) y eventos.json (golpes del carro rojo) para post.py."""
import json
import math
import os
import sys
import wave

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import plan as P  # noqa: E402

TEX = os.path.join(AQUI, "tex")
FPS, RX, RY = P.FPS, P.RX, P.RY


def _args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return {a[i].lstrip("-"): a[i + 1] for i in range(0, len(a), 2)}


def main():
    import bpy
    from mathutils import Vector

    A = _args()
    salida = os.path.abspath(A.get("salida", os.path.join(AQUI, "render")))
    os.makedirs(salida, exist_ok=True)
    nfr = int(round(P.SEG * FPS))
    F = lambda t: int(round(t * FPS)) + 1
    sc = bpy.context.scene
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    # ------------------------------------------------------------------ materiales (sin brillo, texturas «Closest»)
    def mat(nombre, color=None, img=None, emis=0.0):
        m = bpy.data.materials.new(nombre); m.use_nodes = True
        bs = m.node_tree.nodes["Principled BSDF"]
        bs.inputs["Roughness"].default_value = 1.0
        bs.inputs["Specular IOR Level"].default_value = 0.0
        if img:
            tx = m.node_tree.nodes.new("ShaderNodeTexImage")
            tx.image = bpy.data.images.load(os.path.join(TEX, img)); tx.interpolation = "Closest"
            m.node_tree.links.new(tx.outputs["Color"], bs.inputs["Base Color"])
            if emis:
                m.node_tree.links.new(tx.outputs["Color"], bs.inputs["Emission Color"]); bs.inputs["Emission Strength"].default_value = emis
        else:
            bs.inputs["Base Color"].default_value = (*color, 1)
            if emis:
                bs.inputs["Emission Color"].default_value = (*color, 1); bs.inputs["Emission Strength"].default_value = emis
        return m

    M = dict(cara=mat("cara", img="cara2_rel.png", emis=.15), piel=mat("piel", img="piel.png"), pelo=mat("pelo", img="pelo.png"),
             polo=mat("polo", img="polo.png"), jeans=mat("jeans", img="jeans.png"), zapato=mat("zapato", (.20, .09, .04)),
             cuello=mat("cuello", (.02, .16, .55)), sombra=mat("sombra", (.16, .10, .10)), interior=mat("interior", (.30, .32, .36)),
             vidrio=mat("vidrio", (.10, .18, .30)), llanta=mat("llanta", (.04, .04, .05)), empedrado=mat("empedrado", img="empedrado.png"),
             banqueta=mat("banqueta", img="banqueta.png"), tortilleria=mat("tortilleria", img="tortilleria.png", emis=.2),
             cantera_rosa=mat("cantera_rosa", img="cantera_rosa.png", emis=.15), cerro=mat("cerro", (.30, .36, .16)),
             tope=mat("tope", img="tope.png", emis=.25), puerta=mat("puerta", (.30, .16, .07)), faro=mat("faro", (1, .95, .6), emis=1.0),
             calavera=mat("calavera", (.8, .05, .05), emis=.6), rojo=mat("rojo", (.75, .04, .03)), verde=mat("verde", (.10, .45, .12)),
             blanco=mat("blanco", (.88, .88, .86)), onda=mat("onda", (1, .85, .1), emis=2.0), vapor=mat("vapor", (1, 1, 1), emis=1.2),
             polvo=mat("polvo", (.62, .56, .48)),
             **{f"fachada_{c}": mat(f"fachada_{c}", img=f"fachada_{c}.png", emis=.12) for c in ("rosa", "amarillo", "blanco", "terracota", "azulcasa")})

    def malla(nombre, verts, caras, mats, uvs=None, padre=None, loc=(0, 0, 0)):
        me = bpy.data.meshes.new(nombre)
        me.from_pydata(verts, [], [f for f, _ in caras])
        me.update()
        ob = bpy.data.objects.new(nombre, me); sc.collection.objects.link(ob)
        for m_ in mats:
            me.materials.append(M[m_])
        for p, (_, mi) in zip(me.polygons, caras):
            p.material_index = mi; p.use_smooth = False
        uv = me.uv_layers.new(name="uv")
        for p in me.polygons:
            for li in p.loop_indices:
                vi = me.loops[li].vertex_index
                uv.data[li].uv = uvs(me.vertices[vi].co, p) if uvs else (me.vertices[vi].co.x * .5 + me.vertices[vi].co.y * .5, me.vertices[vi].co.z * .5)
        ob.location = loc
        if padre:
            ob.parent = padre
        return ob

    def anillo(nombre, aros, n, mats_f, uvs=None, padre=None, loc=(0, 0, 0), rot0=0.0, tapas=True):
        """Prisma por aros [(z, rx, ry, dy)]; mats_f(i_lado, j_aro) → índice de material."""
        V, C = [], []
        for (z, rx, ry, dy) in aros:
            for i in range(n):
                a = rot0 + 2 * math.pi * i / n
                V.append((rx * math.sin(a), -ry * math.cos(a) + dy, z))
        for j in range(len(aros) - 1):
            for i in range(n):
                a, b = j * n + i, j * n + (i + 1) % n
                C.append(((a, b, b + n, a + n), mats_f(i, j)))
        if tapas:
            C.append((tuple(range(n))[::-1], mats_f(-1, -1)))
            C.append((tuple(range((len(aros) - 1) * n, len(aros) * n)), mats_f(-2, -2)))
        nm = max(mi for _, mi in C) + 1
        return V, C, nm

    def caja(nombre, cx, cy, cz, sx, sy, sz, m_, padre=None, escala_uv=1.0):
        V = [(cx + sx / 2 * x, cy + sy / 2 * y, cz + sz / 2 * z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
        Cs = [((0, 1, 3, 2), 0), ((4, 6, 7, 5), 0), ((0, 4, 5, 1), 0), ((2, 3, 7, 6), 0), ((0, 2, 6, 4), 0), ((1, 5, 7, 3), 0)]

        def uvc(co, p):
            nx, ny, nz = (abs(c) for c in p.normal)
            if nz > .5:
                return (co.x * escala_uv, co.y * escala_uv)
            if nx > .5:
                return (co.y * escala_uv, co.z * escala_uv)
            return (co.x * escala_uv, co.z * escala_uv)
        return malla(nombre, V, Cs, [m_], uvc, padre)

    def vacio(nombre, loc, padre=None):
        e = bpy.data.objects.new(nombre, None); sc.collection.objects.link(e)
        e.location = loc
        if padre:
            e.parent = padre
        return e

    # ------------------------------------------------------------------ DANIEL v2: UNA malla continua con piel por pesos
    # Las articulaciones son vacíos animados (mismas poses que la v1); cada vértice sigue a 1-2 de ellos, así no hay huecos en
    # hombros, codos ni cuello. La cabeza es redondeada (10 lados) con orejas y nariz, y la foto va proyectada DE FRENTE.
    raiz = vacio("raiz", (0, 0, 0))
    cadera = vacio("cadera", (0, 0, .92), raiz)
    torso = vacio("torso", (0, 0, 0), cadera)
    cuello = vacio("cuello", (0, 0, .60), torso)
    cab = vacio("cabeza", (0, 0, .04), cuello)
    brazos = {}
    for lado, x in (("I", -.25), ("D", .25)):
        h = vacio("hombro" + lado, (x, 0, .50), torso)
        co = vacio("codo" + lado, (0, 0, -.29), h)
        brazos[lado] = (h, co)
    for lado, x in (("I", -.1), ("D", .1)):
        vacio("pierna" + lado, (x, 0, 0), cadera)
    bpy.context.view_layer.update()
    J = ["raiz", "cadera", "torso", "cuello", "cabeza", "hombroI", "codoI", "hombroD", "codoD", "piernaI", "piernaD"]
    JO = [bpy.data.objects[n] for n in J]
    REST_INV = [o.matrix_world.inverted() for o in JO]

    V, WV, FC = [], [], []          # vértices (mundo, en reposo), pesos {articulación: w}, caras (índices, material)

    def anillo_v(c, rx, ry, n, w, rot0=0.0):
        idx = []
        for i in range(n):
            a = rot0 + 2 * math.pi * i / n
            idx.append(len(V)); V.append((c[0] + rx * math.sin(a), c[1] - ry * math.cos(a), c[2])); WV.append(w)
        return idx

    def puente(r0, r1, m):
        n = len(r0)
        for i in range(n):
            FC.append(((r0[i], r0[(i + 1) % n], r1[(i + 1) % n], r1[i]), m))

    def tapa(r, m, punta, w, arriba=True):
        k = len(V); V.append(punta); WV.append(w); n = len(r)
        for i in range(n):
            FC.append(((r[i], r[(i + 1) % n], k) if arriba else (r[(i + 1) % n], r[i], k), m))

    def caja_v(c, sx, sy, sz, w, m, punta_baja=0.0):
        o = len(V)
        for z in (-1, 1):
            for y in (-1, 1):
                for x in (-1, 1):
                    dz = -punta_baja if (z > 0 and y < 0) else 0.0
                    V.append((c[0] + sx / 2 * x, c[1] + sy / 2 * y, c[2] + sz / 2 * z + dz)); WV.append(w)
        for q in ((0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)):
            FC.append((tuple(o + i for i in q), m))

    T_, C_ = {"torso": 1.0}, {"cadera": 1.0}
    # piernas y zapatos
    for s in (-1, 1):
        P_ = {"pierna" + ("I" if s < 0 else "D"): 1.0}
        x = .1 * s
        rs = [anillo_v((x, 0, .93), .095, .10, 6, C_), anillo_v((x, 0, .80), .09, .095, 6, P_), anillo_v((x, -.005, .52), .068, .072, 6, P_),
              anillo_v((x, .005, .30), .062, .066, 6, P_), anillo_v((x, 0, .11), .05, .055, 6, P_)]
        for a, b in zip(rs, rs[1:]):
            puente(b, a, "jeans") if False else puente(a, b, "jeans")
        tapa(rs[-1], "jeans", (x, 0, .09), P_, arriba=False)
        caja_v((x, -.045, .05), .11, .27, .1, P_, "zapato", punta_baja=.035)
    # torso: jeans, cinturón, polo con panza, hombros y cuello del polo
    t = [anillo_v((0, 0, .84), .18, .12, 8, C_, math.pi / 8), anillo_v((0, 0, .93), .19, .125, 8, C_, math.pi / 8),
         anillo_v((0, 0, .975), .192, .127, 8, {"torso": .5, "cadera": .5}, math.pi / 8),
         anillo_v((0, -.005, 1.0), .196, .132, 8, T_, math.pi / 8), anillo_v((0, -.015, 1.15), .205, .145, 8, T_, math.pi / 8),
         anillo_v((0, -.005, 1.30), .212, .135, 8, T_, math.pi / 8), anillo_v((0, 0, 1.42), .20, .115, 8, T_, math.pi / 8),
         anillo_v((0, 0, 1.475), .125, .09, 8, T_, math.pi / 8), anillo_v((0, -.005, 1.515), .085, .075, 8, T_, math.pi / 8)]
    tapa(t[0], "jeans", (0, 0, .82), C_, arriba=False)
    for k, (a, b) in enumerate(zip(t, t[1:])):
        puente(a, b, ["jeans", "cinturon", "polo", "polo", "polo", "polo", "polo", "cuello"][k])
    cu0 = anillo_v((0, -.005, 1.515), .06, .055, 8, T_, math.pi / 8)
    puente(t[-1], cu0, "cuello")
    cu1 = anillo_v((0, -.005, 1.60), .056, .052, 8, {"cabeza": 1.0}, math.pi / 8)
    puente(cu0, cu1, "piel")
    # brazos: hombro redondo (tapa), manga, codo, muñeca y mano
    for s, lado in ((-1, "I"), (1, "D")):
        H, Co = {"hombro" + lado: 1.0}, {"codo" + lado: 1.0}
        # v3 (27-nov): el hombro nace DENTRO del torso y sigue al torso (75 %), así la manga nunca se despega del cuerpo;
        # el brazo cuelga más pegado (pivote en x=.25) y es más grueso
        x = .25 * s
        a0 = anillo_v((.20 * s, 0, 1.45), .085, .08, 6, {"torso": .75, "hombro" + lado: .25})
        tapa(a0, "polo", (.19 * s, 0, 1.515), T_)
        a1 = anillo_v((x, 0, 1.30), .078, .08, 6, H)
        a2 = anillo_v((x, 0, 1.29), .058, .06, 6, H)
        a3 = anillo_v((x, -.005, 1.13), .054, .056, 6, {"hombro" + lado: .5, "codo" + lado: .5})
        a4 = anillo_v((x, -.01, .90), .044, .046, 6, Co)
        a5 = anillo_v((x, -.015, .855), .033, .056, 6, Co)
        a6 = anillo_v((x, -.02, .78), .026, .046, 6, Co)
        puente(a0, a1, "polo"); puente(a1, a2, "polo"); puente(a2, a3, "piel"); puente(a3, a4, "piel")
        puente(a4, a5, "piel"); puente(a5, a6, "piel"); tapa(a6, "piel", (x, -.02, .76), Co, arriba=False)
        a0[:] = a0
    # cabeza (rígida): mentón, quijada, pómulos, ojos, frente, coronilla
    K_ = {"cabeza": 1.0}
    hs = [((0, -.02, 1.565), .055, .05), ((0, -.015, 1.60), .085, .085), ((0, -.005, 1.67), .108, .105), ((0, 0, 1.75), .115, .112),
          ((0, 0, 1.83), .113, .112), ((0, .005, 1.90), .098, .10), ((0, .01, 1.955), .065, .07)]
    hr = [anillo_v(c, rx, ry, 10, K_) for c, rx, ry in hs]
    tapa(hr[0], "piel", (0, -.01, 1.552), K_, arriba=False)
    for a, b in zip(hr, hr[1:]):
        puente(a, b, "auto")
    tapa(hr[-1], "pelo", (0, .015, 1.978), K_)
    for s in (-1, 1):
        caja_v((.112 * s, .012, 1.745), .022, .045, .07, K_, "piel")
    o = len(V)
    V += [(-.024, -.110, 1.712), (.024, -.110, 1.712), (0, -.113, 1.79), (0, -.148, 1.722)]; WV += [K_] * 4
    FC += [((o, o + 1, o + 3), "cara"), ((o + 1, o + 2, o + 3), "cara"), ((o + 2, o, o + 3), "cara")]

    # materiales automáticos de la cabeza y UV
    Va = np.array(V)

    def info(f):
        p = Va[list(f)]
        n_ = np.cross(p[1] - p[0], p[2] - p[0]); n_ /= (np.linalg.norm(n_) + 1e-9)
        return p.mean(0), n_
    FC2 = []
    for f, m in FC:
        if m == "auto":
            c, n_ = info(f)
            m = "cara" if n_[1] < .35 else ("pelo" if c[2] > 1.69 else "piel")
        FC2.append((f, m))
    FC = FC2
    M["cinturon"] = mat("cinturon", (.20, .11, .05))
    for nd in M["cara"].node_tree.nodes:
        if nd.type == "TEX_IMAGE":
            nd.extension = "EXTEND"
    MATS = ["cara", "piel", "pelo", "polo", "cuello", "jeans", "cinturon", "zapato"]
    dme = bpy.data.meshes.new("daniel"); dme.from_pydata(V, [], [f for f, _ in FC]); dme.update()
    dan_ob = bpy.data.objects.new("daniel", dme); sc.collection.objects.link(dan_ob)
    for m_ in MATS:
        dme.materials.append(M[m_])
    uvd = dme.uv_layers.new(name="uv")
    for p, (_, m_) in zip(dme.polygons, FC):
        p.material_index = MATS.index(m_); p.use_smooth = False
        for li in p.loop_indices:
            x, y, z = V[dme.loops[li].vertex_index]
            if m_ == "cara":
                uvd.data[li].uv = (.5 + x / (2 * .1415), (z - 1.535) / (1.99 - 1.535))
            else:
                uvd.data[li].uv = ((x + y) * 2.2, z * 2.2)
    TRIS_DANIEL = sum(len(f) - 2 for f, _ in FC)
    nj = len(J); nv = len(V)
    WM = np.zeros((nv, nj))
    for i, wd in enumerate(WV):
        for k, w in wd.items():
            WM[i, J.index(k)] = w
    WM /= WM.sum(1, keepdims=True)
    VH = np.c_[np.array(V), np.ones(nv)]

    def piel_daniel():
        S = np.array([np.array(o.matrix_world @ R) for o, R in zip(JO, REST_INV)])
        P = np.einsum("jab,vb->jva", S, VH)
        return np.einsum("vj,jva->va", WM, P)

    # ------------------------------------------------------------------ calle de Juchipila: empedrado, banquetas, casas, parroquia
    malla("calle", [(-3.2, -14, 0), (3.2, -14, 0), (3.2, 46, 0), (-3.2, 46, 0)], [((0, 1, 2, 3), 0)], ["empedrado"],
          uvs=lambda co, p: (co.x / 1.4, co.y / 1.4))
    for s in (-1, 1):
        caja("banqueta", s * 3.9, 16, .08, 1.4, 60, .16, "banqueta", escala_uv=.7)
    rnd = np.random.default_rng(5)
    colores = ["fachada_rosa", "fachada_amarillo", "fachada_blanco", "fachada_terracota", "fachada_azulcasa"]
    for s in (-1, 1):
        y = -14.0
        k = 0
        while y < 44:
            lg = float(rnd.uniform(3.6, 5.4)); h = float(rnd.uniform(3.0, 4.8))
            col = colores[(k * 2 + (s > 0)) % len(colores)]
            caja("casa", s * 6.1, y + lg / 2, h / 2, 3.0, lg - .04, h, col, escala_uv=.45)
            caja("pretil", s * 4.62, y + lg / 2, h + .08, .12, lg - .04, .16, "sombra")
            xf = s * 4.585
            caja("puerta", xf, y + lg * .3, .95, .06, 1.0, 1.9, "puerta")
            caja("ventana", xf, y + lg * .7, 1.6, .06, 1.0, 1.1, "vidrio")
            caja("reja", xf - s * .02, y + lg * .7, 1.6, .06, .06, 1.1, "sombra")
            if s > 0 and k == 4:
                y0_, y1_, z0_, z1_ = y + lg / 2 - 1.2, y + lg / 2 + 1.2, h - .85, h - .25
                malla("letrero", [(4.55, y0_, z0_), (4.55, y1_, z0_), (4.55, y1_, z1_), (4.55, y0_, z1_)], [((0, 3, 2, 1), 0)],
                      ["tortilleria"], uvs=lambda co, p, a_=y1_, b_=y0_, c_=z0_: ((a_ - co.y) / (a_ - b_), (co.z - c_) / .6))
            y += lg
            k += 1
    # parroquia al fondo de la calle (torre de cantera rosa) y cerros del cañón
    caja("templo", 0, 50, 4, 9, 6, 8, "cantera_rosa", escala_uv=.4)
    caja("torre", -2.6, 48, 7.5, 2.4, 2.4, 15, "cantera_rosa", escala_uv=.4)
    caja("campanario", -2.6, 48, 15.8, 1.9, 1.9, 1.8, "sombra")
    Vt = [(-2.6 - 1.0, 48 - 1.0, 16.7), (-2.6 + 1.0, 48 - 1.0, 16.7), (-2.6 + 1.0, 48 + 1.0, 16.7), (-2.6 - 1.0, 48 + 1.0, 16.7), (-2.6, 48, 19)]
    malla("cupula", Vt, [((0, 1, 4), 0), ((1, 2, 4), 0), ((2, 3, 4), 0), ((3, 0, 4), 0)], ["cantera_rosa"])
    for (x, y, r, h) in ((-30, 95, 26, 22), (10, 110, 32, 30), (42, 92, 22, 18), (-60, 70, 22, 16), (65, 70, 22, 17)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.0, location=(x, y, 0))
        ce = bpy.context.object; ce.scale = (r, r * .6, h); ce.data.materials.append(M["cerro"])

    # ------------------------------------------------------------------ topes amarillos (uno por objeto: luego salen volando)
    PERF = [(-.36, 0), (-.22, .13), (.22, .13), (.36, 0)]
    topes = []
    for k, ty in enumerate(P.TOPES_Y):
        Vt, Ct = [], []
        for x in (-3.15, 3.15):
            for (py, pz) in PERF:
                Vt.append((x, py, pz))
        for i in range(3):
            Ct.append(((i, i + 1, 5 + i, 4 + i), 0))
        Ct.append(((3, 2, 1, 0), 0)); Ct.append(((4, 5, 6, 7), 0))
        largo = [0, .26, .70, .96]
        ob = malla(f"tope{k}", Vt, Ct, ["tope"], uvs=lambda co, p: (co.x / .8, .5))
        uv = ob.data.uv_layers.active.data
        for p_ in ob.data.polygons:
            for li in p_.loop_indices:
                vi = ob.data.loops[li].vertex_index
                uv[li].uv = (ob.data.vertices[vi].co.x / .8, largo[vi % 4])
        ob.location = (0, ty, 0)
        topes.append(ob)

    # ------------------------------------------------------------------ vochos: rojo (A, vuela), verde (B, se desarma), blanco (C, pasa liso)
    def carro(nombre, color, sin_mofle=False, sin_llanta=False):
        r = vacio(nombre, (0, 0, 0))
        caja("cuerpo", 0, 0, .52, 1.36, 2.3, .5, color, padre=r)
        caja("cofre", 0, .78, .82, 1.22, .74, .12, color, padre=r)
        caja("cabina", 0, -.18, 1.03, 1.16, 1.25, .5, color, padre=r)
        caja("parabrisas", 0, .45, 1.03, 1.06, .02, .38, "vidrio", padre=r)
        caja("medallon", 0, -.81, 1.03, 1.0, .02, .32, "vidrio", padre=r)
        for s in (-1, 1):
            caja("ventanilla", s * .585, -.18, 1.05, .02, 1.0, .34, "vidrio", padre=r)
            caja("faro", s * .46, 1.155, .62, .22, .04, .16, "faro", padre=r)
            caja("calavera", s * .5, -1.155, .62, .2, .04, .12, "calavera", padre=r)
        caja("defensa", 0, 1.2, .38, 1.42, .08, .1, "interior", padre=r)
        caja("defensa2", 0, -1.2, .38, 1.42, .08, .1, "interior", padre=r)
        ruedas = []
        for x in (-.66, .66):
            for y in (-.78, .78):
                Vr, Cr, nm = anillo("ll", [(-.11, .29, .29, 0), (.11, .29, .29, 0)], 8, lambda i, j: 0)
                ll = malla("llanta", Vr, Cr, ["llanta"])
                if sin_llanta and x < 0 and y > 0:         # la delantera izquierda va suelta (se zafa)
                    ruedas.append(ll)
                    continue
                ll.parent = r; ll.location = (x, y, .29); ll.rotation_euler = (0, math.pi / 2, 0)
        mofle = None
        Vm, Cm, nm = anillo("mo", [(-.2, .06, .06, 0), (.2, .06, .06, 0)], 6, lambda i, j: 0)
        mofle = malla("mofle", Vm, Cm, ["interior"])
        if not sin_mofle:
            mofle.parent = r; mofle.location = (.35, -1.3, .26); mofle.rotation_euler = (math.pi / 2, 0, 0)
        return r, mofle, (ruedas[0] if ruedas else None)

    carA, _, _ = carro("carroA", "rojo")
    carB, mofleB, ruedaB = carro("carroB", "verde", sin_mofle=True, sin_llanta=True)
    carC, _, _ = carro("carroC", "blanco")
    mofleB.rotation_mode = "XYZ"; ruedaB.rotation_mode = "XYZ"
    # onda del pisotón (anillo plano) y vapor de coraje
    Vo, Co_ = [], []
    for i in range(16):
        a_ = 2 * math.pi * i / 16
        Vo += [(math.cos(a_), math.sin(a_), .03), (.82 * math.cos(a_), .82 * math.sin(a_), .03)]
    for i in range(16):
        j = (i + 1) % 16
        Co_.append(((2 * i, 2 * j, 2 * j + 1, 2 * i + 1), 0))
    onda = malla("onda", Vo, Co_, ["onda"])
    vapor = []
    for i in range(8):
        bpy.ops.mesh.primitive_cube_add(size=1.0); vp = bpy.context.object; vp.data.materials.append(M["vapor"]); vapor.append(vp)
    polvo = []
    for i in range(10):
        bpy.ops.mesh.primitive_cube_add(size=1.0); pv = bpy.context.object; pv.data.materials.append(M["polvo"]); polvo.append(pv)

    # ------------------------------------------------------------------ Daniel: poses RÁPIDAS con rebote (caricatura)
    def key(ob, attr, t, val):
        setattr(ob, attr, val); ob.keyframe_insert(attr, frame=F(t))

    R = math.radians
    POSES = {   # (hombroI, codoI, hombroD, codoD, cabeza, torso)
        "reposo": ((0, R(6), 0), (R(-10), 0, 0), (0, R(-6), 0), (R(-10), 0, 0), (0, 0, 0), (0, 0, 0)),
        "mira": ((0, R(10), 0), (R(-10), 0, 0), (0, R(-10), 0), (R(-10), 0, 0), (R(-4), 0, R(-35)), (0, 0, R(-12))),
        "susto": ((0, R(150), 0), (0, R(45), 0), (0, R(-150), 0), (0, R(-45), 0), (R(-14), 0, 0), (R(-10), 0, 0)),
        "puño": ((0, R(35), 0), (0, R(-75), 0), (0, R(-150), 0), (0, R(-70), 0), (R(-6), 0, R(25)), (0, 0, R(10))),
        "abajo": ((0, R(25), 0), (0, R(-60), 0), (R(-55), R(-20), 0), (R(-10), 0, 0), (R(22), 0, 0), (R(10), 0, 0)),
        "calle": ((0, R(10), 0), (R(-10), 0, 0), (R(55), R(-70), 0), (0, R(-10), 0), (0, 0, R(40)), (0, 0, R(18))),
        "abierto": ((R(-20), R(65), 0), (R(-30), 0, 0), (R(-20), R(-65), 0), (R(-30), 0, 0), (R(-8), 0, 0), (0, 0, 0)),
        "cabeza": ((0, R(150), 0), (0, R(115), 0), (0, R(-150), 0), (0, R(-115), 0), (R(8), 0, 0), (R(6), 0, 0)),
        "jarras": ((0, R(40), 0), (0, R(-95), 0), (0, R(-40), 0), (0, R(95), 0), (R(-4), 0, 0), (0, 0, 0)),
        "rabia": ((0, R(130), 0), (0, R(60), 0), (0, R(-130), 0), (0, R(-60), 0), (R(-10), 0, 0), (R(6), 0, 0)),
        "patada": ((0, R(70), 0), (0, R(20), 0), (0, R(-70), 0), (0, R(-20), 0), (R(10), 0, 0), (R(-14), 0, 0)),
        "pie": ((R(-30), R(30), 0), (R(-40), 0, 0), (R(-30), R(-30), 0), (R(-40), 0, 0), (R(20), 0, R(10)), (R(18), 0, 0)),
        "serio": ((R(-40), R(-8), 0), (R(-95), 0, R(55)), (R(-40), R(8), 0), (R(-95), 0, R(-55)), (R(4), 0, 0), (0, 0, 0)),
        "uno": ((0, R(40), 0), (0, R(-95), 0), (0, R(-172), 0), (0, 0, 0), (R(-8), 0, R(-8)), (0, 0, R(-4))),
        "pecho": ((0, R(40), 0), (0, R(-95), 0), (0, R(-40), 0), (0, R(95), 0), (R(-14), 0, 0), (R(-10), 0, 0)),
        "arriba": ((0, R(172), 0), (0, 0, 0), (0, R(-172), 0), (0, 0, 0), (R(-16), 0, 0), (R(-8), 0, 0)),
        "pisoton": ((R(-30), R(50), 0), (R(-40), 0, 0), (R(-30), R(-50), 0), (R(-40), 0, 0), (R(18), 0, 0), (R(22), 0, 0)),
        "baile1": ((0, R(165), 0), (0, R(20), 0), (0, R(-35), 0), (0, R(-80), 0), (0, 0, R(12)), (0, R(10), R(-10))),
        "baile2": ((0, R(35), 0), (0, R(80), 0), (0, R(-165), 0), (0, R(-20), 0), (0, 0, R(-12)), (0, R(-10), R(10))),
        "saludo": ((0, R(6), 0), (R(-10), 0, 0), (0, R(-100), 0), (0, R(-80), 0), (0, R(-6), 0), (0, R(-4), 0)),
    }
    (hI, cI), (hD, cD) = brazos["I"], brazos["D"]
    piezas = (hI, cI, hD, cD, cab, torso)
    pI, pD = bpy.data.objects["piernaI"], bpy.data.objects["piernaD"]
    for ob in piezas + (pI, pD, raiz, cadera):
        ob.rotation_mode = "XYZ"

    def mezcla_r(a, b, k):
        return tuple(x + (y - x) * k for x, y in zip(a, b))

    def pose(t, nombre, dur=.09):
        """Pose nueva en `dur` s con un rebote del 18 % (sube de más y se asienta): movimiento de caricatura."""
        prev = pose.ult
        for ob, r0, r1 in zip(piezas, POSES[prev], POSES[nombre]):
            key(ob, "rotation_euler", t, r0)
            key(ob, "rotation_euler", t + dur, mezcla_r(r0, r1, 1.18))
            key(ob, "rotation_euler", t + dur * 1.9, r1)
        pose.ult = nombre
    pose.ult = "reposo"
    for ob, r in zip(piezas, POSES["reposo"]):
        key(ob, "rotation_euler", 0, r)
    for ob in (pI, pD):
        key(ob, "rotation_euler", 0, (0, 0, 0))
    key(raiz, "location", 0, (P.DX, 0, 0)); key(raiz, "rotation_euler", 0, (0, 0, 0))

    def brinco(t, h, dur=.32, giro=0.0):
        key(raiz, "location", t, (P.DX, 0, 0))
        key(raiz, "location", t + dur * .45, (P.DX, 0, h))
        key(raiz, "location", t + dur, (P.DX, 0, -0.04))
        key(raiz, "location", t + dur + .06, (P.DX, 0, 0))
        if giro:
            key(raiz, "rotation_euler", t, (0, 0, 0)); key(raiz, "rotation_euler", t + dur, (0, 0, giro))

    def sacude(ob, t0, t1, eje, amp, paso=.07, base=None):
        """Vibración rápida alrededor de la rotación actual (puños, cabeza que dice que no)."""
        k = 0
        t = t0
        while t < t1:
            b = list(base if base is not None else ob.rotation_euler)
            b[eje] += amp * (1 if k % 2 == 0 else -1)
            key(ob, "rotation_euler", t, tuple(b))
            t += paso; k += 1

    FR = P.FRASES
    # 1 · el vocho rojo pasa, pega en el tope y vuela: susto y puño
    pose(.15, "mira", .12)
    pose(P.T_CHOQUE_A + .03, "susto", .07)
    brinco(P.T_CHOQUE_A + .03, .5, .36)
    pose(P.W(1, "cabrón") - .1, "puño")
    sacude(cD, P.W(1, "cabrón"), P.W(1, "pinche") - .1, 1, R(22), base=POSES["puño"][3])
    brinco(P.W(1, "pinche") - .05, .18, .22)
    pose(P.W(1, "tope") - .08, "abajo")
    # 2 · «más topes que calles» · «no mamen»
    pose(FR[1][0] - .05, "calle", .1)
    pose(P.W(2, "calles") - .1, "abierto")
    pose(P.W(2, "no") - .08, "cabeza")
    sacude(cab, P.W(2, "mamen"), FR[1][1] + .25, 2, R(14), base=POSES["cabeza"][4])
    # 3 · cada «tope»: brinquito y cabezazo
    pose(FR[2][0] - .05, "jarras", .1)
    for k, tt in enumerate(P.TOPES_L3):
        brinco(tt, .14, .2)
        key(cab, "rotation_euler", tt - .02, POSES["jarras"][4])
        key(cab, "rotation_euler", tt + .06, (R(18), 0, R(10 if k % 2 else -10)))
        key(cab, "rotation_euler", tt + .22, POSES["jarras"][4])
    pose(P.W(3, "misa") - .1, "abierto", .08)
    pose(P.TOPES_L3[2] + .05, "jarras", .08)
    # 4 · mofle, suspensión, susto
    pose(P.T_MOFLE + .05, "abajo")
    pose(P.T_SUSP - .05, "cabeza")
    sacude(cab, P.T_SUSP + .15, P.T_SUSTO - .1, 2, R(10), base=POSES["cabeza"][4])
    pose(P.T_SUSTO, "susto", .06)
    brinco(P.T_SUSTO, .75, .5)
    sacude(torso, P.T_SUSTO + .55, FR[3][1] + .2, 1, R(5), paso=.05, base=POSES["susto"][5])
    # 5 · coraje: puños, pisotón en «verga», patada en «putos», brinca agarrándose el pie
    pose(FR[4][0] - .1, "rabia", .08)
    sacude(cD, FR[4][0] + .1, P.T_PATADA - .1, 1, R(28), paso=.06, base=POSES["rabia"][3])
    sacude(cI, FR[4][0] + .13, P.T_PATADA - .1, 1, R(28), paso=.06, base=POSES["rabia"][1])
    brinco(P.T_VERGA5 - .05, .2, .2)
    pose(P.T_PATADA - .08, "patada", .06)
    key(pD, "rotation_euler", P.T_PATADA - .08, (0, 0, 0)); key(pD, "rotation_euler", P.T_PATADA + .02, (R(-80), 0, 0))
    key(pD, "rotation_euler", P.T_PATADA + .2, (R(-70), 0, 0))
    pose(P.T_PIE - .05, "pie", .07)
    key(pD, "rotation_euler", P.T_PIE, (R(55), 0, 0))
    t = P.T_PIE
    while t < FR[4][1] + .25:
        brinco(t, .2, .24, giro=0.0)
        key(raiz, "rotation_euler", t, (0, 0, R(12 if int((t - P.T_PIE) / .26) % 2 else -12)))
        t += .26
    key(raiz, "rotation_euler", FR[4][1] + .3, (0, 0, 0))
    key(pD, "rotation_euler", FR[4][1] + .3, (R(55), 0, 0)); key(pD, "rotation_euler", FR[4][1] + .42, (0, 0, 0))
    # 6 · «Por eso, mi primera orden como presidente...»
    pose(FR[5][0] - .05, "serio", .1)
    pose(P.W(6, "primera") - .08, "uno")
    pose(P.W(6, "presidente") - .08, "pecho", .12)
    # 7 · brinco enorme y PISOTÓN: los topes salen volando
    pose(P.T_TIRAR - .05, "arriba", .07)
    key(raiz, "location", P.T_TIRAR, (P.DX, 0, 0))
    key(raiz, "location", (P.T_TIRAR + P.T_PISOTON) / 2, (P.DX, 0, 1.1))
    key(raiz, "location", P.T_PISOTON, (P.DX, 0, -.1))
    key(raiz, "location", P.T_PISOTON + .12, (P.DX, 0, 0))
    pose(P.T_PISOTON - .03, "pisoton", .05)
    pose(P.T_PISOTON + .45, "arriba", .08)
    sacude(cD, P.T_PISOTON + .6, FR[6][1], 1, R(18), paso=.08, base=POSES["arriba"][3])
    sacude(cI, P.T_PISOTON + .64, FR[6][1], 1, R(18), paso=.08, base=POSES["arriba"][1])
    # 8 · baile de la victoria y saludo
    t = P.T_BAILE - .05
    k = 0
    while t < P.T_SOY - .2:
        pose(t, "baile1" if k % 2 == 0 else "baile2", .07)
        brinco(t, .12, .18)
        t += .27; k += 1
    pose(P.T_SOY - .1, "saludo", .1)
    for k in range(int((P.SEG - P.T_SOY) / .28)):
        key(cD, "rotation_euler", P.T_SOY + .25 + .28 * k, (0, R(-80 + (25 if k % 2 == 0 else -15)), 0))
    # respiración
    for k in range(0, int(P.SEG * 2) + 1):
        key(torso, "location", k * .5, (0, 0, .012 * (k % 2)))
    for ob in piezas + (pI, pD, raiz, torso):
        if ob.animation_data and ob.animation_data.action:
            for fc in ob.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "BEZIER" if ob is torso else "LINEAR"

    # ------------------------------------------------------------------ cara: gesto por cuadro (voz) + roja de coraje
    wf = wave.open(os.path.join(AQUI, "voz", "voz.wav"))
    sr = wf.getframerate(); nch = wf.getnchannels(); sw = wf.getsampwidth()
    raw = wf.readframes(wf.getnframes())
    y = np.frombuffer(raw, np.int16 if sw == 2 else np.int32).astype(np.float32)
    y = y.reshape(-1, nch).mean(1) / (32768 if sw == 2 else 2 ** 31)
    GL = ("rel", "a", "e", "o", "m", "f", "sonrisa", "parpadeo", "serio")
    GEST = {g: bpy.data.images.load(os.path.join(TEX, f"cara2_{g}.png")) for g in GL}
    GEST.update({g + "_rojo": bpy.data.images.load(os.path.join(TEX, f"cara2_{g}_rojo.png")) for g in GL})
    PIEL = {False: bpy.data.images.load(os.path.join(TEX, "piel.png")), True: bpy.data.images.load(os.path.join(TEX, "piel_rojo.png"))}
    nodo_cara = M["cara"].node_tree.nodes["Image Texture"]
    nodo_piel = M["piel"].node_tree.nodes["Image Texture"]
    O_PAL = {"tope", "topes", "otro", "no", "todos", "mofle", "eso", "orden", "como", "soy", "los"}
    VENT_O = [(a, b) for f_, w_, a, b in P.PALABRAS if w_ in O_PAL]
    ROJO = [(1.35, FR[0][1] + .1), (FR[4][0] - .1, FR[4][1] + .35), (P.T_TIRAR, FR[6][1] + .2)]
    SUSTO = [(P.T_CHOQUE_A, P.T_CHOQUE_A + .45), (P.T_SUSTO, P.T_SUSTO + .55)]
    PARPADEO = (4.0, 9.6, 15.2, 22.5, 28.9, 32.0)

    def gesto(t):
        tv = t - P.VOZ_OFF
        a = int(max(0, tv) * sr); b = int(max(0, tv + 1 / FPS) * sr)
        ab = min(1.0, float(np.sqrt(np.mean(y[a:b] ** 2))) / .08) if b > a and tv >= 0 and a < len(y) else 0.0
        if any(p <= t < p + .14 for p in PARPADEO):
            return "parpadeo"
        if any(x <= t < z for x, z in SUSTO) and ab < .3:
            return "o"
        if ab < .15:
            if t < .15 or t >= P.T_BAILE:
                return "sonrisa"
            return "serio"
        o = any(x <= t < z for x, z in VENT_O)
        if ab < .35:
            return "o" if o else "f"
        if ab < .65:
            return "o" if o else "e"
        return "o" if o else "a"

    def cara(t):
        rojo = any(x <= t < z for x, z in ROJO)
        g = gesto(t)
        nodo_cara.image = GEST[g + ("_rojo" if rojo else "")]
        nodo_piel.image = PIEL[rojo]
        return rojo

    # ------------------------------------------------------------------ física de caricatura, cuadro por cuadro
    def baches(t, golpes, dur=.36):
        """Altura y cabeceo por una lista de golpes [(t, altura)]."""
        z = 0.0; pitch = 0.0
        for tk, h in golpes:
            u = (t - tk) / dur
            if 0 <= u <= 1:
                z += h * 4 * u * (1 - u)
                pitch += .35 * h * math.sin(2 * math.pi * u) * (1 - u)
        return z, pitch

    ESC = lambda ob, s: setattr(ob, "scale", (s, s, s))
    # carro rojo (A): de detrás de la cámara hasta el tope de Daniel, voltereta y rebotes calle arriba
    Y0A = -1.5                                      # arranca ya en cuadro (no pegado a la cámara) y ACELERA hasta el tope
    ACA = 2 * (P.TOPES_Y[0] - Y0A) / P.T_CHOQUE_A ** 2
    DUR_V = 1.15
    VF, VL = 6.0, 9.0                               # avance en el aire y, ya aterrizado, calle arriba
    y_aterriza = P.TOPES_Y[0] + VF * DUR_V
    golpes_A = []
    for ty in P.TOPES_Y[1:]:
        if ty > y_aterriza:
            golpes_A.append((P.T_CHOQUE_A + DUR_V + (ty - y_aterriza) / VL, .45))

    def carro_a(t):
        if t < P.T_CHOQUE_A:
            y_ = Y0A + .5 * ACA * t * t
        elif t < P.T_CHOQUE_A + DUR_V:
            y_ = P.TOPES_Y[0] + VF * (t - P.T_CHOQUE_A)
        else:
            y_ = y_aterriza + VL * (t - P.T_CHOQUE_A - DUR_V)
        if y_ > 36:
            ESC(carA, 0); return
        ESC(carA, 1)
        z, pitch = baches(t, golpes_A)
        rollo = 0.0
        u = (t - P.T_CHOQUE_A) / DUR_V
        if 0 <= u <= 1:
            z = 2.8 * 4 * u * (1 - u)
            pitch = 2 * math.pi * (u ** .9)
            rollo = .5 * math.sin(math.pi * u)
        carA.location = (P.CARRIL, y_, z); carA.rotation_euler = (pitch, rollo, 0)

    # carro verde (B): viene hacia la cámara, un golpe por «tope», mofle, llanta, se hunde; en el pisotón sale volando
    T_B0 = P._B[0][0]
    T_VUELA_B = P.T_PISOTON + .35

    def carro_b(t):
        if t < T_B0 or t > T_VUELA_B + 1.6:
            ESC(carB, 0); return None
        ESC(carB, 1)
        y_ = P.carro_b_y(t)
        z, pitch = baches(t, P.GOLPES_B)
        rollo = 0.0
        if t >= P.T_SUSP:
            k = min(1.0, (t - P.T_SUSP) / .12)
            rollo = R(-9) * k + (R(3) * math.sin((t - P.T_SUSP) * 40) * math.exp(-(t - P.T_SUSP) * 6))
            z -= .14 * k; pitch -= R(4) * k
        loc = [P.CARRIL, y_, z]; rot = [pitch, rollo, math.pi]
        if t >= T_VUELA_B:
            u = t - T_VUELA_B
            loc = [P.CARRIL + 2 * u, y_ + 14 * u, z + 13 * u - 4.9 * u * u]
            rot = [pitch + 7 * u, rollo + 4 * u, math.pi + 3 * u]
        carB.location = loc; carB.rotation_euler = rot
        return True

    def pegado(raiz_, local):
        return raiz_.matrix_world @ Vector(local)

    def mofle_b(t):
        if t < T_B0 or t > T_VUELA_B + 1.6:
            ESC(mofleB, 0); return
        ESC(mofleB, 1)
        t_s = P.T_MOFLE + .22
        if t < t_s:
            mofleB.location = pegado(carB, (.35, -1.3, .26)); mofleB.rotation_euler = carB.rotation_euler.copy()
            mofleB.rotation_euler.x += math.pi / 2
            mofle_b.p0 = mofleB.location.copy()
            return
        if not hasattr(mofle_b, "p0"):
            carro_b(t_s); bpy.context.view_layer.update(); mofle_b.p0 = pegado(carB, (.35, -1.3, .26)); carro_b(t); bpy.context.view_layer.update()
        u = t - t_s
        p0 = mofle_b.p0
        z = max(.06, p0.z + 1.5 * u - 4.9 * u * u)
        if p0.z + 1.5 * u - 4.9 * u * u < .06:
            u2 = u - .45
            z = .06 + max(0, .35 * math.sin(min(math.pi, u2 * 9))) * math.exp(-u2 * 3)
        yy = p0.y + 1.2 * min(u, .9)
        if t >= T_VUELA_B:
            w = t - T_VUELA_B
            z += 11 * w - 4.9 * w * w; yy += 10 * w
        mofleB.location = (p0.x - .4 * min(u, .9), yy, z); mofleB.rotation_euler = (math.pi / 2 + 6 * min(u, 1.2), 0, R(30) * min(u, 1))

    def rueda_b(t):
        if t < T_B0 or t > P.T_SUSP + 2.6:
            ESC(ruedaB, 0); return
        ESC(ruedaB, 1)
        if t < P.T_SUSP:
            ruedaB.location = pegado(carB, (-.66, .78, .29))
            r_ = carB.rotation_euler
            ruedaB.rotation_euler = (r_.x, r_.y + math.pi / 2, r_.z)
            rueda_b.p0 = ruedaB.location.copy()
            return
        if not hasattr(rueda_b, "p0"):
            carro_b(P.T_SUSP - .01); bpy.context.view_layer.update(); rueda_b.p0 = pegado(carB, (-.66, .78, .29)); carro_b(t); bpy.context.view_layer.update()
        u = t - P.T_SUSP
        p0 = rueda_b.p0
        rebote = abs(math.sin(u * 5.5)) * 1.1 * math.exp(-u * 1.3)
        ruedaB.location = (p0.x - 1.1 * u, p0.y - 3.6 * u, .29 + rebote)
        ruedaB.rotation_euler = (-12 * u, math.pi / 2, R(25) * math.sin(u * 3))

    # carro blanco (C): pasa LISO por la calle sin topes
    T_C0 = P.T_BAILE - .2

    def carro_c(t):
        if t < T_C0:
            ESC(carC, 0); return
        ESC(carC, 1)
        carC.location = (P.CARRIL, -4.0 + 9.0 * (t - T_C0), 0); carC.rotation_euler = (0, 0, 0)

    def topes_vuelan(t):
        for k, ob in enumerate(topes):
            tv = P.T_VUELAN[k]
            if t < P.T_PISOTON:
                ob.location = (0, P.TOPES_Y[k], 0); ob.rotation_euler = (0, 0, 0); ESC(ob, 1)
            elif t < tv:
                ob.location = (0, P.TOPES_Y[k], .03 * math.sin(t * 90)); ob.rotation_euler = (0, R(2) * math.sin(t * 70), 0); ESC(ob, 1)
            else:
                u = t - tv
                if u > 2.2:
                    ESC(ob, 0); continue
                ob.location = (1.2 * u * (1 if k % 2 else -1), P.TOPES_Y[k] + 2.0 * u, 15 * u - 4.9 * u * u)
                ob.rotation_euler = (5 * u * (1 if k % 2 else -1), 2 * u, 3 * u)
                ESC(ob, max(0.0, 1 - max(0, u - 1.4) / .8))

    def onda_(t):
        u = t - P.T_PISOTON
        if 0 <= u < .7:
            ESC(onda, 1); onda.location = (P.DX, 0, 0)
            s = .5 + 14 * u
            onda.scale = (s, s, 1)
        else:
            ESC(onda, 0)

    rv = np.random.default_rng(9).uniform(-1, 1, (len(vapor), 3))

    def vapor_(t, activo):
        cabeza = cab.matrix_world.translation
        for i, vp in enumerate(vapor):
            if not activo:
                ESC(vp, 0); continue
            ph = (t * 1.8 + i / len(vapor)) % 1.0
            lado = -1 if i % 2 else 1
            vp.location = (cabeza.x + lado * (.12 + .25 * ph) + .04 * rv[i, 0], cabeza.y + .03 * rv[i, 1], cabeza.z + .28 + .7 * ph)
            ESC(vp, .09 * (1 - ph) + .03)
            vp.rotation_euler = (ph * 3, ph * 2, i)

    rp = np.random.default_rng(4).uniform(-1, 1, (len(polvo), 3))
    NUBES = [(P.T_CHOQUE_A, (P.CARRIL, P.TOPES_Y[0], .2)), (P.T_MOFLE, (P.CARRIL, P.TOPES_Y[0], .2)),
             (P.T_SUSP, (P.CARRIL - .7, -2.6, .15)), (P.T_PISOTON, (P.DX, 0, .1))]

    def polvo_(t):
        act = [(tk, c) for tk, c in NUBES if 0 <= t - tk < .7]
        for i, pv in enumerate(polvo):
            if not act:
                ESC(pv, 0); continue
            tk, c = act[-1]
            u = t - tk
            pv.location = (c[0] + rp[i, 0] * (.3 + 1.6 * u), c[1] + rp[i, 1] * (.3 + 1.2 * u), c[2] + abs(rp[i, 2]) * 1.2 * u)
            ESC(pv, .22 * (1 - u / .7) + .02)

    # ------------------------------------------------------------------ cámara: un plano por frase, cortes secos y sacudida en cada golpe
    PLANOS = [  # (t0, loc0, loc1, mira0, mira1)
        (0.0, (0.2, -4.7, 1.65), (0.1, -4.1, 1.6), (-.3, 2, 1.2), (-.5, 2.5, 1.25)),
        (FR[1][0] - .05, (-.2, -5.2, 1.7), (.9, -6.6, 5.6), (-1.0, 0, 1.3), (0, 13, .4)),
        (FR[2][0] - .1, (-.9, -4.4, 2.0), (-.8, -4.2, 1.95), (.2, 9, .7), (.3, 4, .8)),
        (FR[3][0] - .1, (-.2, -5.0, 1.9), (.1, -5.6, 1.95), (0, 0, .95), (0, -1.5, .95)),
        (FR[4][0] - .12, (-1.12, -3.1, 1.5), (-1.08, -2.5, 1.55), (-1.0, 0, 1.2), (-1.0, 0, 1.35)),
        (FR[5][0] - .12, (-1.0, -2.6, 1.75), (-1.0, -1.65, 1.78), (-1.0, 0, 1.62), (-1.0, 0, 1.72)),
        (FR[6][0] - .1, (-.3, -7.0, 2.6), (.3, -9.5, 4.6), (-.6, 3, 1.4), (0, 10, 3.2)),
        (P.T_BAILE - .15, (0.0, -4.3, 1.65), (-.3, -3.6, 1.6), (-.8, 2, 1.25), (-.95, 0, 1.35)),
        (P.SEG + 1, None, None, None, None),
    ]
    GOLPES_CAM = [(P.T_CHOQUE_A, .9), (P.T_CHOQUE_A + DUR_V, .5)] + [(tk, .35) for tk, _ in P.GOLPES_B] + \
                 [(P.T_SUSP, .6), (P.T_SUSTO + .5, .4), (P.T_VERGA5, .3), (P.T_PATADA, .4), (P.T_PISOTON, 1.4)]
    rs = np.random.default_rng(2)
    RS = rs.uniform(-1, 1, (int(P.SEG * FPS) + 10, 3))

    def camara(t, f):
        for (t0, l0, l1, m0, m1), (t1, *_) in zip(PLANOS, PLANOS[1:]):
            if t0 <= t < t1:
                u = (t - t0) / (t1 - t0)
                u = u * u * (3 - 2 * u)
                loc = Vector(l0).lerp(Vector(l1), u); mi = Vector(m0).lerp(Vector(m1), u)
                break
        amp = sum(a * math.exp(-(t - tk) * 7) for tk, a in GOLPES_CAM if t >= tk)
        sh = Vector(RS[f]) * .09 * min(amp, 1.6)
        loc = loc + sh
        cam.location = loc
        cam.rotation_euler = (mi - loc).to_track_quat("-Z", "Y").to_euler()

    bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
    cam.data.lens = 30; cam.data.sensor_fit = "AUTO"; cam.data.clip_end = 400

    # ------------------------------------------------------------------ luz y render diminuto
    w = bpy.data.worlds.new("cielo"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (.42, .66, .95, 1); w.node_tree.nodes["Background"].inputs[1].default_value = .7
    bpy.ops.object.light_add(type="SUN", rotation=(math.radians(50), math.radians(10), math.radians(215)))
    bpy.context.object.data.energy = 3.6; bpy.context.object.data.angle = 0.0
    sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.eevee.taa_render_samples = 1
    sc.eevee.use_shadows = True
    sc.render.filter_size = 0.0
    sc.render.resolution_x, sc.render.resolution_y = RX, RY
    sc.render.fps = FPS; sc.frame_start, sc.frame_end = 1, nfr
    sc.render.image_settings.file_format = "PNG"; sc.render.image_settings.color_mode = "RGB"
    sc.view_settings.view_transform = "Standard"
    json.dump(dict(triangulos_daniel=TRIS_DANIEL), open(os.path.join(salida, "info.json"), "w"))

    # ------------------------------------------------------------------ temblor PS1: vértices a la rejilla de píxeles
    mallas = [o for o in sc.objects if o.type == "MESH" and o.name != "daniel"]
    for o in mallas:
        if o.data.users > 1:
            o.data = o.data.copy()
    base = {o.name: [v.co.copy() for v in o.data.vertices] for o in mallas}

    def temblor():
        Kpx = (RY / 2) / (18.0 / cam.data.lens)
        Ci = cam.matrix_world.inverted(); Cw = cam.matrix_world
        for o in mallas:
            Mw = o.matrix_world
            if abs(Mw.determinant()) < 1e-9:
                continue
            Mi = Mw.inverted()
            for v, b in zip(o.data.vertices, base[o.name]):
                c = Ci @ (Mw @ b)
                if c.z < -.05:
                    k = -c.z
                    c = Vector((round(c.x / k * Kpx) / Kpx * k, round(c.y / k * Kpx) / Kpx * k, c.z))
                    v.co = Mi @ (Cw @ c)
                else:
                    v.co = b
            o.data.update()
        Pd = piel_daniel()
        c = (np.array(Ci) @ Pd.T).T
        k = -c[:, 2]; m = k > .05
        for ax in (0, 1):
            c[m, ax] = np.round(c[m, ax] / k[m] * Kpx) / Kpx * k[m]
        Pw = (np.array(Cw) @ c.T).T[:, :3]
        dme.vertices.foreach_set("co", Pw.astype(np.float32).ravel()); dme.update()

    cuadros = [int(x) for x in A["cuadros"].split(",")] if "cuadros" in A else range(1, nfr + 1)
    eventos = dict(golpes_A=golpes_A, aterriza_A=P.T_CHOQUE_A + DUR_V, vuela_B=T_VUELA_B, carro_C=T_C0)
    json.dump(eventos, open(os.path.join(AQUI, "eventos.json"), "w"))
    for f in cuadros:
        t = (f - 1) / FPS
        sc.frame_set(f)
        rojo = cara(t)
        carro_a(t); carro_b(t); carro_c(t); topes_vuelan(t); onda_(t)
        bpy.context.view_layer.update()
        mofle_b(t); rueda_b(t)
        vapor_(t, FR[4][0] <= t < FR[4][1] + .35)
        polvo_(t)
        camara(t, f)
        bpy.context.view_layer.update()
        temblor()
        sc.render.filepath = os.path.join(salida, f"f_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
    print("LISTO topes", salida)


if __name__ == "__main__":
    main()
