# -*- coding: utf-8 -*-
"""FÁBRICA 3D (Mil por Minuto, 24-nov-2026): escena 3D procedural en Blender de una línea de embotellado (banda de entrada →
llenadora rotativa de 25 válvulas → tapadora → etiquetadora → banda de salida) con CÁMARA ORBITAL. Cinco estilos de la misma escena
para elegir (el usuario, 24-nov-2026: «construye 5 estilos diferentes y muestra en 1 video»).

  "C:/Program Files/Blender Foundation/Blender 4.2/blender.exe" -b --factory-startup --python nucleo/fabrica3d.py -- \
        --estilo realista --salida <carpeta> [--seg 6] [--ancho 1920] [--alto 1080] [--muestras 32]
  python nucleo/fabrica3d.py --comparar <carpeta>      (sin Blender: lanza los 5 y arma comparar.mp4 con rótulos)

Estilos: realista · plano (plano técnico azul del canal, líneas cian) · arcilla (maqueta mate, cámara ortográfica) ·
         comic (cel-shading con contorno negro) · rayosx (máquina de cristal, líquido que brilla, fondo negro).
"""
import math
import os
import sys

ESTILOS = ["realista", "plano", "arcilla", "comic", "rayosx"]
NOMBRES = {"realista": "1 · REALISTA INDUSTRIAL", "plano": "2 · PLANO TÉCNICO (HOLOGRAMA)", "arcilla": "3 · MAQUETA DE ARCILLA",
           "comic": "4 · CÓMIC CON CONTORNO", "rayosx": "5 · RAYOS X / CRISTAL"}
BLENDER = r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"

# geometría de la línea (unidades ≈ metros ×2: botella de 0,5)
R = 25 * 0.4 / (2 * math.pi)     # radio de la llenadora: 25 válvulas a 0,4 exactas → cada botella cae bajo su válvula
PASO = 0.4
LIN = 8.0                         # tramo recto de entrada hasta el punto tangente
ARCO = math.pi * R
Z0 = 0.8                          # altura de la banda
V = 1.0                           # velocidad de la línea (unidades/s)
S_TAPA = LIN + ARCO + 2.4
S_ETIQ = LIN + ARCO + 4.6


def ruta(s):
    """Posición (x, y) de una botella a la distancia s de la línea."""
    if s <= LIN:
        return -LIN + s, -R
    if s <= LIN + ARCO:
        a = -math.pi / 2 + (s - LIN) / R
        return R * math.cos(a), R * math.sin(a)
    return -(s - LIN - ARCO), R


def _cl(u):
    return max(0.0, min(1.0, u))


def _suave(u):
    u = _cl(u)
    return u * u * (3 - 2 * u)


# ====================================================================================================== lado Blender
def _blender(args):
    import bpy
    from mathutils import Vector

    estilo = args.get("estilo", "realista")
    toma = args.get("toma", "general")
    seg = float(args.get("seg", 6))
    fps = 30
    nfr = int(seg * fps)
    sc = bpy.context.scene
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)

    opaco = estilo in ("arcilla", "comic", "plano")

    # ---------------------------------------------------------------- materiales por estilo
    def nodos(m):
        m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        return nt, out

    def principled(nombre, color, metal=0.0, rugoso=.5, trans=0.0, ior=1.45, emis=None, emis_f=0.0, alfa=1.0, capa=0.0):
        m = bpy.data.materials.new(nombre)
        nt, out = nodos(m)
        b = nt.nodes.new("ShaderNodeBsdfPrincipled")
        b.inputs["Base Color"].default_value = (*color, 1)
        b.inputs["Metallic"].default_value = metal
        b.inputs["Roughness"].default_value = rugoso
        b.inputs["Transmission Weight"].default_value = trans
        b.inputs["IOR"].default_value = ior
        b.inputs["Alpha"].default_value = alfa
        b.inputs["Coat Weight"].default_value = capa
        if emis:
            b.inputs["Emission Color"].default_value = (*emis, 1)
            b.inputs["Emission Strength"].default_value = emis_f
        nt.links.new(b.outputs[0], out.inputs[0])
        if trans > 0 or alfa < 1:
            m.surface_render_method = "BLENDED" if alfa < 1 else "DITHERED"
        return m

    def emision(nombre, color, f=1.0):
        m = bpy.data.materials.new(nombre)
        nt, out = nodos(m)
        e = nt.nodes.new("ShaderNodeEmission")
        e.inputs[0].default_value = (*color, 1)
        e.inputs[1].default_value = f
        nt.links.new(e.outputs[0], out.inputs[0])
        return m

    def toon(nombre, color, alfa=1.0):
        """Cel-shading: difuso → Shader to RGB → rampa de 3 escalones."""
        m = bpy.data.materials.new(nombre)
        nt, out = nodos(m)
        dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
        dif.inputs[0].default_value = (1, 1, 1, 1)
        s2r = nt.nodes.new("ShaderNodeShaderToRGB")
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        cr = ramp.color_ramp
        cr.interpolation = "CONSTANT"
        cr.elements[0].position = 0.0
        cr.elements[0].color = (*[c * .42 for c in color], 1)
        cr.elements[1].position = 0.62
        cr.elements[1].color = (*[min(1, c * 1.08 + .04) for c in color], 1)
        mid = cr.elements.new(0.22)
        mid.color = (*[c * .78 for c in color], 1)
        em = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(dif.outputs[0], s2r.inputs[0])
        nt.links.new(s2r.outputs[0], ramp.inputs[0])
        nt.links.new(ramp.outputs[0], em.inputs[0])
        if alfa < 1:
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            mx = nt.nodes.new("ShaderNodeMixShader")
            mx.inputs[0].default_value = alfa
            nt.links.new(tr.outputs[0], mx.inputs[1])
            nt.links.new(em.outputs[0], mx.inputs[2])
            nt.links.new(mx.outputs[0], out.inputs[0])
            m.surface_render_method = "BLENDED"
        else:
            nt.links.new(em.outputs[0], out.inputs[0])
        return m

    def borde(nombre, cuerpo, filo, f_cuerpo=1.0, f_filo=3.0, transparente=False, mezcla=.35):
        """Emisión con filo brillante (fresnel): holograma y rayos X."""
        m = bpy.data.materials.new(nombre)
        nt, out = nodos(m)
        lw = nt.nodes.new("ShaderNodeLayerWeight")
        lw.inputs[0].default_value = mezcla
        e1 = nt.nodes.new("ShaderNodeEmission")
        e1.inputs[0].default_value = (*cuerpo, 1)
        e1.inputs[1].default_value = f_cuerpo
        e2 = nt.nodes.new("ShaderNodeEmission")
        e2.inputs[0].default_value = (*filo, 1)
        e2.inputs[1].default_value = f_filo
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lw.outputs["Facing"], mx.inputs[0])
        if transparente:
            tr = nt.nodes.new("ShaderNodeBsdfTransparent")
            add = nt.nodes.new("ShaderNodeAddShader")
            nt.links.new(tr.outputs[0], mx.inputs[1])
            nt.links.new(e2.outputs[0], mx.inputs[2])
            nt.links.new(mx.outputs[0], add.inputs[0])
            nt.links.new(e1.outputs[0], add.inputs[1])
            nt.links.new(add.outputs[0], out.inputs[0])
            m.surface_render_method = "BLENDED"
        else:
            nt.links.new(e1.outputs[0], mx.inputs[1])
            nt.links.new(e2.outputs[0], mx.inputs[2])
            nt.links.new(mx.outputs[0], out.inputs[0])
        return m

    def piso_rejilla(nombre, fondo, linea, f=1.0, paso=1.0, grosor=.025):
        m = bpy.data.materials.new(nombre)
        nt, out = nodos(m)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs[0])
        masc = None
        for eje in ("X", "Y"):
            mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 1 / paso
            nt.links.new(sep.outputs[eje], mul.inputs[0])
            fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"
            nt.links.new(mul.outputs[0], fr.inputs[0])
            lt = nt.nodes.new("ShaderNodeMath"); lt.operation = "LESS_THAN"; lt.inputs[1].default_value = grosor / paso
            nt.links.new(fr.outputs[0], lt.inputs[0])
            if masc is None:
                masc = lt
            else:
                mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
                nt.links.new(masc.outputs[0], mx.inputs[0]); nt.links.new(lt.outputs[0], mx.inputs[1])
                masc = mx
        mixc = nt.nodes.new("ShaderNodeMix"); mixc.data_type = "RGBA"
        mixc.inputs[6].default_value = (*fondo, 1)
        mixc.inputs[7].default_value = (*linea, 1)
        nt.links.new(masc.outputs[0], mixc.inputs[0])
        e = nt.nodes.new("ShaderNodeEmission"); e.inputs[1].default_value = f
        nt.links.new(mixc.outputs[2], e.inputs[0])
        nt.links.new(e.outputs[0], out.inputs[0])
        return m

    P = {}
    if estilo == "realista":
        P["acero"] = principled("acero", (.80, .81, .83), metal=1, rugoso=.38)
        P["acero_osc"] = principled("acero_osc", (.42, .44, .47), metal=.6, rugoso=.45)
        P["banda"] = principled("banda", (.035, .035, .04), rugoso=.75)
        P["botella"] = principled("pet", (.70, .78, .78), rugoso=.04, alfa=.13, capa=.5)
        P["liquido"] = principled("cola", (.05, .014, .004), rugoso=.06, capa=.6)
        P["tapa"] = principled("tapa", (.62, .02, .02), rugoso=.35)
        P["etiqueta"] = principled("etiqueta", (.68, .02, .03), rugoso=.4)
        P["acento"] = principled("amarillo", (.95, .62, .02), rugoso=.45)
        P["piso"] = principled("concreto", (.16, .16, .155), rugoso=.6)
        P["muro"] = principled("muro", (.16, .17, .18), rugoso=.8)
        P["valvula"] = P["acero"]
        P["molde"] = principled("molde", (.75, .78, .80), metal=.3, rugoso=.2, alfa=.32)
        mundo, mundo_f = (.025, .028, .032), 1.0
    elif estilo == "plano":
        cuerpo, cian, naranja = (.012, .05, .09), (.25, .85, 1.0), (1.0, .28, .04)
        P["acero"] = borde("holo", cuerpo, cian, 1.0, 1.6)
        P["acero_osc"] = P["acero"]
        P["banda"] = borde("holo_banda", (.01, .03, .06), cian, 1.0, 1.0)
        P["botella"] = toon("holo_bot", (.12, .42, .58), alfa=.5)
        P["liquido"] = emision("holo_liq", naranja, 2.2)
        P["tapa"] = emision("holo_tapa", (1.0, .75, .1), 2.0)
        P["etiqueta"] = emision("holo_etq", (1.0, .45, .08), 1.6)
        P["acento"] = emision("holo_acento", (1.0, .75, .1), 1.5)
        P["piso"] = piso_rejilla("holo_piso", (.008, .03, .055), (.06, .30, .45), 1.0, paso=1.0)
        P["muro"] = P["piso"]
        P["valvula"] = borde("holo_valv", cuerpo, (1.0, .75, .1), 1.0, 2.0)
        P["molde"] = borde("holo_molde", cuerpo, cian, .4, 1.4, transparente=True, mezcla=.3)
        mundo, mundo_f = (.004, .016, .03), 1.0
    elif estilo == "arcilla":
        def mate(n, c):
            return principled(n, c, rugoso=1.0)
        P["acero"] = mate("crema", (.86, .80, .70))
        P["acero_osc"] = mate("verde_agua", (.38, .62, .60))
        P["banda"] = mate("menta", (.55, .76, .66))
        P["botella"] = mate("bot_clara", (.80, .88, .90))
        P["liquido"] = mate("cafe", (.36, .14, .07))
        P["tapa"] = mate("coral", (.90, .30, .26))
        P["etiqueta"] = mate("rojo_suave", (.86, .22, .22))
        P["acento"] = mate("mostaza", (.95, .74, .30))
        P["piso"] = mate("arena", (.93, .86, .74))
        P["muro"] = P["piso"]
        P["valvula"] = mate("terracota", (.86, .52, .36))
        P["molde"] = principled("molde", (.86, .80, .70), rugoso=1.0, alfa=.4)
        mundo, mundo_f = (.92, .88, .82), .9
    elif estilo == "comic":
        P["acero"] = toon("t_gris", (.62, .70, .78))
        P["acero_osc"] = toon("t_azul", (.16, .38, .72))
        P["banda"] = toon("t_banda", (.18, .20, .24))
        P["botella"] = toon("t_bot", (.70, .92, 1.0))
        P["liquido"] = toon("t_cola", (.30, .08, .03))
        P["tapa"] = toon("t_tapa", (.95, .10, .08))
        P["etiqueta"] = toon("t_etq", (.95, .12, .10))
        P["acento"] = toon("t_amarillo", (1.0, .82, .10))
        P["piso"] = toon("t_piso", (.98, .93, .78))
        P["muro"] = P["piso"]
        P["valvula"] = toon("t_valv", (.98, .55, .10))
        P["molde"] = toon("t_molde", (.62, .70, .78), alfa=.4)
        mundo, mundo_f = (1.0, .95, .80), 1.0
    else:   # rayosx
        P["acero"] = borde("rx", (.0, .02, .04), (.15, .75, 1.0), .6, 2.2, transparente=True, mezcla=.25)
        P["acero_osc"] = P["acero"]
        P["banda"] = borde("rx_banda", (.0, .015, .03), (.15, .6, .9), .5, 1.6, transparente=True, mezcla=.25)
        P["botella"] = borde("rx_bot", (.0, .0, .0), (.85, .95, 1.0), .0, 1.6, transparente=True, mezcla=.18)
        P["liquido"] = emision("rx_liq", (1.0, .22, .04), 3.5)
        P["tapa"] = emision("rx_tapa", (1.0, .85, .3), 3.0)
        P["etiqueta"] = emision("rx_etq", (1.0, .1, .25), 2.2)
        P["acento"] = emision("rx_acento", (.9, .2, 1.0), 2.0)
        P["piso"] = piso_rejilla("rx_piso", (.0, .0, .004), (.10, .05, .22), 1.0, paso=1.0, grosor=.02)
        P["muro"] = P["piso"]
        P["valvula"] = borde("rx_valv", (.04, .0, .06), (.9, .3, 1.0), .5, 2.5, transparente=True, mezcla=.3)
        P["molde"] = P["acero"]
        mundo, mundo_f = (0, 0, .004), 1.0

    # ---------------------------------------------------------------- geometría
    def malla(nombre, verts, caras, mat, suave=True):
        me = bpy.data.meshes.new(nombre)
        me.from_pydata(verts, [], caras)
        me.update()
        if suave:
            for p in me.polygons:
                p.use_smooth = True
        me.materials.append(mat)
        return me

    def torno(nombre, perfil, mat, seg=40):
        """Sólido de revolución: perfil = [(r, z)] de abajo arriba."""
        verts, caras = [], []
        for r, z in perfil:
            for k in range(seg):
                a = 2 * math.pi * k / seg
                verts.append((r * math.cos(a), r * math.sin(a), z))
        n = len(perfil)
        for i in range(n - 1):
            for k in range(seg):
                a, b = i * seg + k, i * seg + (k + 1) % seg
                caras.append((a, b, b + seg, a + seg))
        verts.append((0, 0, perfil[0][1])); c0 = len(verts) - 1
        verts.append((0, 0, perfil[-1][1])); c1 = len(verts) - 1
        for k in range(seg):
            caras.append((c0, (k + 1) % seg, k))
            caras.append((c1, (n - 1) * seg + k, (n - 1) * seg + (k + 1) % seg))
        return malla(nombre, verts, caras, mat)

    def obj(nombre, me, loc=(0, 0, 0), padre=None):
        o = bpy.data.objects.new(nombre, me)
        sc.collection.objects.link(o)
        o.location = loc
        if padre:
            o.parent = padre
        return o

    def caja(nombre, x0, y0, z0, x1, y1, z1, mat, padre=None):
        v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        return obj(nombre, malla(nombre, v, f, mat, suave=False), padre=padre)

    def cil(nombre, r, z0, z1, mat, loc=(0, 0, 0), seg=40, padre=None):
        return obj(nombre, torno(nombre, [(r, z0), (r, z1)], mat, seg), loc, padre)

    def tubo(nombre, p0, p1, r, mat, seg=12):
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0
        o = cil(nombre, r, 0, d.length, mat, seg=seg)
        o.location = p0
        o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
        return o

    # piso y nave
    piso = obj("piso", malla("piso", [(-60, -60, 0), (60, -60, 0), (60, 60, 0), (-60, 60, 0)], [(0, 1, 2, 3)], P["piso"], False))
    if estilo == "realista":
        for x in range(-24, 13, 6):
            for y in (-9, 9):
                caja(f"pilar{x}{y}", x - .3, y - .3, 0, x + .3, y + .3, 9, P["muro"])
        caja("muro_fondo", -30, 11, 0, 14, 11.4, 9, P["muro"])
        caja("muro_lado", 14, -12, 0, 14.4, 12, 9, P["muro"])
    # líneas de seguridad alrededor de la llenadora
    for (x0, y0, x1, y1) in [(-3.0, -3.2, 3.2, -3.08), (-3.0, 3.08, 3.2, 3.2), (3.08, -3.2, 3.2, 3.2)]:
        caja("linea", x0, y0, .002, x1, y1, .006, P["acento"])

    if toma != "soplado":
        # bandas (entrada y = -R, salida y = +R) con patas y guías
        for yb in (-R, R):
            caja("banda", -26, yb - .17, Z0 - .08, 0, yb + .17, Z0, P["banda"])
            caja("chasis", -26, yb - .2, Z0 - .2, 0, yb + .2, Z0 - .08, P["acero"])
            for x in range(-25, 0, 2):
                caja("pata", x - .04, yb - .16, 0, x + .04, yb - .12, Z0 - .2, P["acero_osc"])
                caja("pata", x - .04, yb + .12, 0, x + .04, yb + .16, Z0 - .2, P["acero_osc"])
            for dy in (-.15, .15):
                tubo("guia", (-26, yb + dy, Z0 + .2), (0, yb + dy, Z0 + .2), .012, P["acero"])

        # llenadora rotativa
        cil("base", R + .35, 0, Z0 - .05, P["acero_osc"])
        cil("mesa", R + .25, Z0 - .05, Z0, P["acero"])
        cil("columna", .22, Z0, 2.35, P["acero"])
        gira = bpy.data.objects.new("gira", None)
        sc.collection.objects.link(gira)
        cil("corona", R + .12, 1.72, 1.80, P["acero"], padre=gira)
        tanque = obj("tanque", torno("tanque", [(.0, 2.35), (.95, 2.35), (1.0, 2.45), (1.0, 2.85), (.7, 3.05), (.25, 3.12), (0, 3.13)],
                                      P["acero"]), padre=gira)
        nval = 25
        for j in range(nval):
            a = -math.pi / 2 + j * 2 * math.pi / nval
            x, y = R * math.cos(a), R * math.sin(a)
            cil(f"valv{j}", .055, 1.45, 1.72, P["valvula"], loc=(x, y, 0), seg=16, padre=gira)
            obj(f"boq{j}", torno(f"boq{j}", [(.0, 1.33), (.02, 1.33), (.045, 1.45)], P["valvula"], 16), (x, y, 0), gira)
            tubo(f"tub{j}", (x * .6, y * .6, 2.40), (x, y, 1.80), .012, P["acero"])
        # los tubos van con la corona
        for o in sc.objects:
            if o.name.startswith("tub"):
                o.parent = gira

        # tapadora sobre la banda de salida
        xt = -2.4
        caja("tapadora_col", xt - .2, R + .45, 0, xt + .2, R + .8, 2.1, P["acero_osc"])
        caja("tapadora_brazo", xt - .18, R - .15, 1.85, xt + .18, R + .8, 2.05, P["acero_osc"])
        cabeza = cil("tapadora_cab", .1, 1.36, 1.85, P["valvula"], loc=(xt, R, 0), seg=20)
        obj("tolva_tapas", torno("tolva_tapas", [(.12, 2.1), (.32, 2.45), (.32, 2.6)], P["acento"], 24), (xt, R + .62, 0))
        # etiquetadora
        xe = -4.6
        caja("etiq_base", xe - .45, R - 1.15, 0, xe + .45, R - .35, Z0 + .05, P["acero_osc"])
        tambor = cil("etiq_tambor", .28, Z0 + .05, Z0 + .55, P["etiqueta"], loc=(xe, R - .7, 0), seg=40)
        rollo = cil("etiq_rollo", .22, Z0 + .05, Z0 + .45, P["etiqueta"], loc=(xe - .3, R - .95, 0), seg=32)

        # botellas
        perfil = [(.0, 0), (.085, 0), (.1, .02), (.1, .11), (.088, .16), (.1, .21), (.1, .30), (.085, .34), (.045, .42),
                  (.032, .45), (.032, .5)]
        me_bot = torno("botella", perfil, P["botella"], 32)
        k_liq = .9 if not opaco else 1.012
        perfil_l = [(r * k_liq, z) for r, z in perfil if z <= .42]
        perfil_l = [(0, .008)] + [(r, max(z, .008)) for r, z in perfil_l[1:]]
        me_liq = torno("liquido", perfil_l, P["liquido"], 32)
        me_tapa = torno("tapa", [(.0, .495), (.038, .495), (.038, .53), (.03, .535)], P["tapa"], 24)
        me_etq = torno("etiqueta", [(.104, 0), (.104, .09)], P["etiqueta"], 32)

        pivotes = []
        for k in range(-60, 36):
            s0 = LIN + PASO * k
            piv = bpy.data.objects.new(f"b{k}", None)
            sc.collection.objects.link(piv)
            obj(f"bot{k}", me_bot, padre=piv)
            liq = obj(f"liq{k}", me_liq, padre=piv)
            tapa = obj(f"tapa{k}", me_tapa, padre=piv)
            etq = obj(f"etq{k}", me_etq, (0, 0, .205), piv)
            pivotes.append((s0, piv, liq, tapa, etq))

        # ---------------------------------------------------------------- animación (clave por cuadro)
        sc.render.fps = fps
        sc.frame_start, sc.frame_end = 1, nfr
        t_extra = 0.0
        for f in range(1, nfr + 1):
            t = (f - 1) / fps + t_extra
            gira.rotation_euler = (0, 0, V * t / R)
            gira.keyframe_insert("rotation_euler", frame=f)
            cabeza.rotation_euler = (0, 0, t * 9)
            cabeza.keyframe_insert("rotation_euler", frame=f)
            tambor.rotation_euler = (0, 0, -t * 3)
            tambor.keyframe_insert("rotation_euler", frame=f)
            rollo.rotation_euler = (0, 0, t * 2)
            rollo.keyframe_insert("rotation_euler", frame=f)
            for s0, piv, liq, tapa, etq in pivotes:
                s = s0 + V * t
                x, y = ruta(s)
                vis = -22 < x < 6
                piv.location = (x, y, Z0) if vis else (x, y, -5)
                piv.rotation_euler = (0, 0, s * 1.3)
                piv.keyframe_insert("location", frame=f)
                piv.keyframe_insert("rotation_euler", frame=f)
                llen = _suave((s - LIN - .25) / (ARCO - .5))
                liq.scale = (1, 1, llen) if llen > 0 else (.001, .001, .001)
                liq.keyframe_insert("scale", frame=f)
                kt = _cl((s - S_TAPA + .3) / .3)
                tapa.scale = (1, 1, 1) if s >= S_TAPA - .3 else (.001, .001, .001)
                tapa.location = (0, 0, .16 * (1 - _suave(kt)))
                tapa.keyframe_insert("scale", frame=f)
                tapa.keyframe_insert("location", frame=f)
                ke = _suave((s - S_ETIQ + .35) / .35)
                etq.scale = (1, 1, ke) if ke > 0 else (.001, .001, .001)
                etq.keyframe_insert("scale", frame=f)

        # interpolación lineal en todo (movimiento continuo)
        for o in sc.objects:
            ad = o.animation_data
            if ad and ad.action:
                for fc in ad.action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"

    else:
        _soplado(bpy, sc, P, obj, torno, caja, cil, nfr, fps)

    # ---------------------------------------------------------------- cámara orbital
    objetivo = bpy.data.objects.new("objetivo", None)
    sc.collection.objects.link(objetivo)
    # tomas (24-nov-2026): (objetivo, r0, r1, z0, z1, th0, th1, lente)
    xt_, xe_ = -2.4, -4.6
    a_ll = math.radians(-25)
    TOMAS = {
        "general": ((-1.9, 0, 1.0), 9.6, 7.6, 4.4, 3.0, -118, -22, 28),
        "valvulas": ((R * math.cos(a_ll), R * math.sin(a_ll), 1.25), 3.0, 2.3, 1.9, 1.55, -70, -10, 35),
        "tapadora": ((xt_, R, 1.3), 3.2, 2.6, 2.0, 1.6, -125, -60, 35),
        "etiquetadora": ((xe_, R - .25, 1.1), 3.6, 2.9, 2.1, 1.6, -115, -55, 35),
        "soplado": ((0, 0, 1.42), 3.5, 2.8, 1.95, 1.55, -130, -50, 40),
    }
    tgt, r0, r1, z0, z1, th0, th1, lente = TOMAS[toma]
    objetivo.location = tgt
    cam_d = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    tr = cam.constraints.new("TRACK_TO")
    tr.target = objetivo
    tr.track_axis, tr.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    if estilo == "arcilla" and toma == "general":
        cam_d.type = "ORTHO"
        cam_d.ortho_scale = 8.5
        r0, r1, z0, z1 = 14, 14, 9.5, 9.0
        th0, th1 = th0 - 7, th1 - 13
    else:
        cam_d.lens = lente
        if estilo == "realista":
            cam_d.dof.use_dof = True
            cam_d.dof.focus_object = objetivo
            cam_d.dof.aperture_fstop = 4.0
    cam_d.clip_end = 200
    for f in range(1, nfr + 1):
        u = _suave((f - 1) / max(1, nfr - 1)) * .85 + (f - 1) / max(1, nfr - 1) * .15
        th = math.radians(th0 + (th1 - th0) * u)
        rr = r0 + (r1 - r0) * u
        cam.location = (objetivo.location.x + rr * math.cos(th), objetivo.location.y + rr * math.sin(th), z0 + (z1 - z0) * u)
        cam.keyframe_insert("location", frame=f)

    # ---------------------------------------------------------------- luz y mundo
    w = bpy.data.worlds.new("mundo")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (*mundo, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = mundo_f

    def luz(nombre, tipo, loc, energia, color=(1, 1, 1), tam=1.0, rot=None, sombra=True):
        ld = bpy.data.lights.new(nombre, tipo)
        ld.energy = energia
        ld.color = color
        if tipo == "AREA":
            ld.size = tam
        if tipo == "SUN":
            ld.angle = math.radians(tam)
        ld.use_shadow = sombra
        o = bpy.data.objects.new(nombre, ld)
        sc.collection.objects.link(o)
        o.location = loc
        if rot:
            o.rotation_euler = [math.radians(a) for a in rot]
        else:
            c = o.constraints.new("TRACK_TO")
            c.target = objetivo
            c.track_axis, c.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
        return o

    if estilo == "realista":
        luz("clave", "AREA", (6, -5, 7), 900, (1, .95, .88), 4)
        luz("relleno", "AREA", (-6, -6, 4), 500, (.75, .85, 1), 6)
        luz("contra", "AREA", (-2, 7, 6), 1200, (1, 1, 1), 3)
        for x in range(-20, 10, 5):
            luz(f"techo{x}", "AREA", (x, 0, 8.5), 220, (1, .97, .92), 3, rot=(0, 0, 0))
    elif estilo == "arcilla":
        luz("sol", "SUN", (5, -5, 10), 3.2, (1, .96, .9), 18, rot=(40, 10, 35))
    elif estilo == "comic":
        luz("sol", "SUN", (5, -5, 10), 4.0, (1, 1, 1), 2, rot=(45, 0, 30))
    # plano y rayos X: todo es emisión

    # ---------------------------------------------------------------- render
    r = sc.render
    r.engine = "BLENDER_EEVEE_NEXT"
    r.resolution_x = int(args.get("ancho", 1920))
    r.resolution_y = int(args.get("alto", 1080))
    r.resolution_percentage = 100
    ee = sc.eevee
    ee.taa_render_samples = int(args.get("muestras", 32))
    for attr, val in (("use_raytracing", estilo in ("realista", "arcilla")), ("use_shadows", True),
                      ("use_gtao", estilo in ("arcilla", "realista"))):
        try:
            setattr(ee, attr, val)
        except Exception:
            pass
    try:
        sc.view_settings.view_transform = "AgX" if estilo in ("realista", "arcilla") else "Standard"
        if estilo == "realista":
            sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    if estilo in ("plano", "comic"):
        r.use_freestyle = True
        r.line_thickness_mode = "ABSOLUTE"
        r.line_thickness = 1.4 if estilo == "plano" else 2.6
        vl = sc.view_layers[0]
        vl.use_freestyle = True
        fs = vl.freestyle_settings
        fs.crease_angle = math.radians(140)
        ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("lineas")
        ls.select_by_visibility = True
        ls.select_silhouette = ls.select_border = ls.select_crease = True
        ls.linestyle.color = (.35, .9, 1.0) if estilo == "plano" else (0, 0, 0)
        ls.linestyle.thickness = 1.4 if estilo == "plano" else 2.6
    if estilo in ("plano", "rayosx", "realista"):
        sc.use_nodes = True
        nt = sc.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        rl = nt.nodes.new("CompositorNodeRLayers")
        gl = nt.nodes.new("CompositorNodeGlare")
        gl.glare_type = "FOG_GLOW"
        gl.quality = "HIGH"
        gl.threshold = .9 if estilo != "realista" else 3.0
        gl.size = 8 if estilo != "realista" else 6
        gl.mix = 0.0 if estilo != "realista" else -.6
        co = nt.nodes.new("CompositorNodeComposite")
        nt.links.new(rl.outputs[0], gl.inputs[0])
        nt.links.new(gl.outputs[0], co.inputs[0])
    salida = args["salida"]
    os.makedirs(salida, exist_ok=True)
    r.image_settings.file_format = "PNG"
    r.filepath = os.path.join(salida, "f_")
    if args.get("blend"):
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(salida, f"escena_{estilo}.blend"))
    if args.get("cuadro"):
        sc.frame_set(int(args["cuadro"]))
        r.filepath = os.path.join(salida, f"cuadro_{int(args['cuadro']):04d}.png")
        bpy.ops.render.render(write_still=True)
    else:
        if args.get("desde"):                 # retomar un render cortado sin rehacer lo ya guardado
            sc.frame_start = int(args["desde"])
        bpy.ops.render.render(animation=True)


def _soplado(bpy, sc, P, obj, torno, caja, cil, nfr, fps):
    """Estación de soplado: la preforma se calienta, el molde se cierra, la varilla la estira y el aire la infla (24-nov-2026).
    Molde de material translúcido («vista en corte») para que se vea la botella crecer."""
    Z = 0.9
    caja("mesa_sopl", -.9, -.6, 0, .9, .6, Z - .02, P["acero_osc"])
    perfil_b = [(.0, 0), (.085, 0), (.1, .02), (.1, .11), (.088, .16), (.1, .21), (.1, .30), (.085, .34), (.045, .42),
                (.032, .45), (.032, .5)]
    perfil_e = [(.0, .02), (.03, .02), (.034, .04), (.034, .11), (.034, .16), (.034, .21), (.034, .30), (.034, .34), (.034, .42),
                (.032, .45), (.032, .5)]          # estirada: ya del largo de la botella, todavía delgada
    perfil_p = [(.0, .24), (.026, .24), (.032, .255), (.034, .29), (.034, .32), (.034, .35), (.034, .38), (.034, .41), (.034, .43),
                (.032, .45), (.032, .5)]          # preforma
    escala = 2.0
    me = torno("preforma3d", [(r * escala, z * escala) for r, z in perfil_p], P["botella"], 40)
    pre = obj("preforma3d", me, (0, 0, Z))
    pre.shape_key_add(name="base")
    for nombre, perfil in (("estira", perfil_e), ("infla", perfil_b)):
        k = pre.shape_key_add(name=nombre, from_mix=False)
        seg = 40
        pts = []
        for r, z in perfil:
            for j in range(seg):
                a = 2 * math.pi * j / seg
                pts.append((r * escala * math.cos(a), r * escala * math.sin(a), z * escala))
        pts.append((0, 0, perfil[0][1] * escala))
        pts.append((0, 0, perfil[-1][1] * escala))
        for v, c in zip(k.data, pts):
            v.co = c
    liq = torno("rosca3d", [(.036 * escala, .455 * escala), (.036 * escala, .5 * escala)], P["tapa"], 40)
    obj("rosca3d", liq, (0, 0, Z))
    # horno: dos filas de lámparas que brillan
    lamparas = []
    horno = bpy.data.objects.new("horno", None)
    sc.collection.objects.link(horno)
    for lado in (-1, 1):
        for k in range(4):
            o = cil(f"lampara{lado}{k}", .03, 0, .05, P["acento"], loc=(lado * .32, 0, Z + .5 + k * .12), seg=12)
            o.rotation_euler = (0, math.pi / 2, 0)
            o.parent = horno
            lamparas.append(o)
    ld = bpy.data.lights.new("calor", "POINT")
    ld.energy, ld.color = 0, (1, .45, .1)
    calor = bpy.data.objects.new("calor", ld)
    sc.collection.objects.link(calor)
    calor.location = (0, -.25, Z + .7)
    # molde: dos mitades que se cierran (translúcido)
    m = P.get("molde") or P["acero"]
    izq = caja("molde_izq", -.42, -.22, Z - .02, -.005, .22, Z + 1.02, m)
    der = caja("molde_der", .005, -.22, Z - .02, .42, .22, Z + 1.02, m)
    varilla = cil("varilla", .012, 0, 1.2, P["acero_osc"], loc=(0, 0, Z + 1.05), seg=12)
    sc.render.fps = fps
    sc.frame_start, sc.frame_end = 1, nfr
    T = nfr / fps

    def tramo(t, a, b):
        return _suave((t - a) / max(1e-6, b - a))
    for f in range(1, nfr + 1):
        t = (f - 1) / fps * (14.0 / max(T, 1e-6))          # guion de 14 s aunque el clip dure otra cosa
        calor_k = tramo(t, .2, 2.2) * (1 - tramo(t, 3.0, 3.6))
        ld.energy = 120 * calor_k
        ld.keyframe_insert("energy", frame=f)
        horno.location = (0, 1.1 * tramo(t, 2.4, 3.1), 0)          # el horno se aparta antes de que cierre el molde
        horno.keyframe_insert("location", frame=f)
        cierre = tramo(t, 3.2, 4.4) * (1 - tramo(t, 9.2, 10.4))
        izq.location = (-.55 * (1 - cierre), 0, 0)
        der.location = (.55 * (1 - cierre), 0, 0)
        izq.keyframe_insert("location", frame=f)
        der.keyframe_insert("location", frame=f)
        baja = tramo(t, 4.5, 6.0) * (1 - tramo(t, 7.6, 8.8))
        varilla.location = (0, 0, Z + 1.05 - .98 * baja)
        varilla.keyframe_insert("location", frame=f)
        kb = pre.data.shape_keys.key_blocks
        kb["estira"].value = tramo(t, 4.5, 6.0)
        kb["infla"].value = tramo(t, 6.0, 7.4)
        kb["estira"].keyframe_insert("value", frame=f)
        kb["infla"].keyframe_insert("value", frame=f)
        pre.rotation_euler = (0, 0, t * .8)
        pre.keyframe_insert("rotation_euler", frame=f)


def _args(lista):
    out, i = {}, 0
    while i < len(lista):
        if lista[i].startswith("--"):
            k = lista[i][2:]
            if i + 1 < len(lista) and not lista[i + 1].startswith("--"):
                out[k] = lista[i + 1]; i += 2
            else:
                out[k] = True; i += 1
        else:
            i += 1
    return out


# ====================================================================================================== lado Python normal
def comparar(carpeta, seg=6, muestras=32, estilos=ESTILOS, ancho=1920, alto=1080):
    """Renderiza los 5 estilos (uno a la vez: GPU de 8 GB) y arma comparar.mp4 con el rótulo de cada uno.
    Retoma: si un estilo ya tiene cuadros, sigue desde el primero que falte. Medido 24-nov: realista 1080p/24 muestras ≈ 15 s/cuadro."""
    import subprocess
    import time
    aqui = os.path.abspath(__file__)
    partes = []
    for e in estilos:
        d = os.path.join(carpeta, e)
        t0 = time.time()
        nfr = int(seg * 30)
        falta = next((f for f in range(1, nfr + 1) if not os.path.exists(os.path.join(d, f"f_{f:04d}.png"))), None)
        if falta:
            subprocess.run([BLENDER, "-b", "--factory-startup", "--python", aqui, "--", "--estilo", e, "--salida", d,
                            "--seg", str(seg), "--muestras", str(muestras), "--ancho", str(ancho), "--alto", str(alto),
                            "--desde", str(max(1, falta - 1))], check=True,
                           stdout=open(os.path.join(carpeta, f"_{e}.log"), "w"), stderr=subprocess.STDOUT)
        print(f"{e}: {time.time() - t0:.0f} s", flush=True)
        mp4 = os.path.join(carpeta, f"{e}.mp4")
        rot = NOMBRES[e].replace(":", r"\:")
        dt = (f"scale=1920:1080:flags=lanczos,drawbox=x=40:y=40:w=iw*0.42:h=78:color=0x0F1216@0.78:t=fill,"
              f"drawtext=fontfile='C\\:/Windows/Fonts/bahnschrift.ttf':text='{rot}':fontcolor=0xFFC400:fontsize=44:x=62:y=58")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", "30", "-i", os.path.join(d, "f_%04d.png"), "-vf", dt,
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", mp4], check=True)
        partes.append(mp4)
    lst = os.path.join(carpeta, "_lista.txt")
    with open(lst, "w", encoding="utf-8") as fh:
        for p in partes:
            fh.write(f"file '{p}'\n")
    final = os.path.join(carpeta, "comparar_estilos3d.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", final], check=True)
    print("listo:", final)
    return final


def tomas(salida, estilo, lista, muestras=24, ancho=1920, alto=1080):
    """Renderiza las tomas de un video en un estilo: lista = [(toma, segundos)] → <salida>/<toma>.mp4 (retoma si se corta)."""
    import subprocess
    import time
    aqui = os.path.abspath(__file__)
    os.makedirs(salida, exist_ok=True)
    for toma, seg in lista:
        d = os.path.join(salida, "_cuadros", toma)
        nfr = int(seg * 30)
        t0 = time.time()
        falta = next((f for f in range(1, nfr + 1) if not os.path.exists(os.path.join(d, f"f_{f:04d}.png"))), None)
        if falta:
            subprocess.run([BLENDER, "-b", "--factory-startup", "--python", aqui, "--", "--estilo", estilo, "--toma", toma,
                            "--salida", d, "--seg", str(seg), "--muestras", str(muestras), "--ancho", str(ancho), "--alto", str(alto),
                            "--desde", str(max(1, falta - 1))], check=True,
                           stdout=open(os.path.join(salida, f"_{toma}.log"), "w"), stderr=subprocess.STDOUT)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", "30", "-i", os.path.join(d, "f_%04d.png"),
                        "-vf", "scale=1920:1080:flags=lanczos", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                        os.path.join(salida, f"{toma}.mp4")], check=True)
        print(f"{toma}: {seg} s en {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    if "bpy" in sys.modules or "--" in sys.argv and any("blender" in a.lower() for a in sys.argv[:1]):
        _blender(_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []))
    else:
        a = _args(sys.argv[1:])
        if a.get("tomas"):
            lista = [(x.split(":")[0], float(x.split(":")[1])) for x in a["lista"].split(",")]
            tomas(a["tomas"], a["estilo"], lista, int(a.get("muestras", 24)), int(a.get("ancho", 1920)), int(a.get("alto", 1080)))
        elif a.get("comparar"):
            comparar(a["comparar"], float(a.get("seg", 6)), int(a.get("muestras", 32)),
                     a["estilos"].split(",") if a.get("estilos") else ESTILOS, int(a.get("ancho", 1920)), int(a.get("alto", 1080)))
