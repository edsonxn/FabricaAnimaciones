# -*- coding: utf-8 -*-
"""Coreografía (4/4): Jalisco hoy (8,3 millones, tercer estado más poblado; mariachi, paisaje agavero y Hospicio Cabañas como
patrimonio; el Mundial de 2026 en Guadalajara, México 1-0 Corea) y cierre (música, bebida y orgullo; pregunta a la audiencia), más los
cambios de escena procedurales."""
import obj_c as C
from core import FIN, INI, T
from coreo_peg import BALON, CO, HO, SI, XX
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo
import mapa as M
from trans import SFX, Transicion


def cortes(R):
    pass


def construir(R):
    _actualidad(R)
    _cierre(R)
    _transiciones(R)


def _actualidad(R):
    e = "actualidad"
    i0 = INI(e)
    t_hoy, t_och, t_hab, t_ter, t_pob = T(e, "hoy"), T(e, "ocho"), T(e, "habitantes"), T(e, "tercer"), T(e, "poblado")
    t_mar, t_pai, t_teq, t_hos, t_pat = T(e, "mariachi"), T(e, "paisajes"), T(e, "tequila"), T(e, "hospicio"), T(e, "patrimonio")
    t_dos, t_mun, t_gdl, t_mex, t_gan, t_cor = (T(e, "dos"), T(e, "mundial"), T(e, "guadalajara", frase=2), T(e, "mexico", frase=2),
                                                T(e, "gano"), T(e, "corea"))

    R.camara(i0 - 0.2, -103.6, 20.75, 1.15)
    R.camara(t_mar - 0.1, -103.6, 20.8, 1.3)
    R.camara(t_dos - 0.1, -103.45, 20.68, 3.6)
    R.camara(FIN(e) + 0.4, -103.45, 20.68, 3.8)

    R.anio(i0, 2026)
    R.terreno(i0, "jalisco", COL["jalisco"], 0.8)
    R.contador(t_och - 0.2, t_hab + 0.2, 0, 8348151, (960, 196), px=84, formato="{:,} HABITANTES", hasta_t=t_mar - 0.2)
    R.snd(t_och - 0.2, "reloj_rapido", 0.35, dur=0.9)
    for k, (dib, x, s) in enumerate(((HO(11), 300, 1.0), (SI(3), 620, 1.0), (SI(5), 1300, 0.95), (HO(8), 1620, 1.0))):
        pa(R, dib, x, 1010, s, t_hoy + 0.25 * k, t_mar - 0.1, sem=300 + k, flip=k >= 2)
    R.texto(t_ter - 0.1, t_mar - 0.2, "3.er ESTADO MÁS POBLADO", (960, 300), px=56, d=0.5)

    pa(R, XX(4), 320, 1010, 1.0, t_mar - 0.15, t_dos - 0.1, sem=305, extra=[(0.05, "fanfarria", 0.35)])
    ga(R, HO(9), CI["tequila"], t_pai - 0.1, t_dos - 0.1, s=0.6, off=(0, 150), sem=306, zs=0.4, z=2, entra="sube", dy=260)
    lugar(R, t_teq, t_dos - 0.1, "PAISAJE AGAVERO", CI["tequila"], off=(0, 200), px=42)
    pa(R, CO(1), 1580, 1010, 0.85, t_hos - 0.15, t_dos - 0.1, sem=307, entra="sube", dy=320)
    titulo(R, t_pat - 0.1, t_dos - 0.2, "PATRIMONIO DE LA HUMANIDAD", px=74, snd=True)

    ga(R, XX(7), CI["estadio"], t_mun - 0.15, FIN(e) + 0.3, s=0.6, off=(0, 30), sem=308, zs=0.4, z=2, extra=[(0.05, "fanfarria", 0.35)])
    lugar(R, t_gdl, FIN(e) + 0.2, "ESTADIO GUADALAJARA", CI["estadio"], off=(0, 70), px=40)
    titulo(R, t_mun - 0.1, t_mex - 0.1, "MUNDIAL 2026", px=86)
    pa(R, HO(7), 330, 1010, 1.05, t_mun, FIN(e) + 0.3, sem=309, extra=[(0.05, "impacto", 0.35)])
    R.act(BALON, pos=lambda t: (520 + 900 * min(1.0, max(0.0, (t - t_gan) / 0.8)), 960 - 260 * __import__("math").sin(
        3.14159 * min(1.0, max(0.0, (t - t_gan) / 0.8))), 0.35), t_in=t_mex, d_in=0.2, entra="pop", sem=310, z=4)
    pa(R, HO(8), 1610, 1010, 1.0, t_gan - 0.1, FIN(e) + 0.3, sem=311, flip=True, extra=[(0.3, "fanfarria", 0.4)])
    R.texto(t_cor - 0.1, FIN(e) + 0.3, "MÉXICO 1 · COREA 0", (960, 196), px=86, d=0.6)


def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_tie, t_are, t_mus, t_beb, t_org = T(e, "tierra"), T(e, "arena"), T(e, "musica"), T(e, "bebida"), T(e, "orgullo")
    t_que, t_est, t_cin, t_dim = T(e, "que", frase=1), T(e, "estado"), T(e, "cinco"), T(e, "dimelo")

    R.camara(i0 - 0.2, -103.6, 20.75, 1.3)
    R.camara(t_que - 0.1, -103.4, 20.8, 1.05)
    R.camara(FIN(e) + 1.2, -103.3, 20.8, 1.0)

    R.terreno(i0 - 0.1, "jalisco", COL["jalisco"], 0.6)
    ga(R, CO(0), CI["guadalajara"], i0, FIN(e) + 1.2, s=0.5, off=(0, 0), sem=320, zs=0.4, z=2)
    ga(R, HO(10), CI["zapopan"], i0 + 0.2, FIN(e) + 1.2, s=0.36, off=(-120, 10), sem=321, zs=0.4, z=2)
    R.texto(t_are - 0.1, t_que - 0.2, "«sobre la arena»", (960, 196), px=74, d=0.6)
    pa(R, XX(3), 330, 1010, 1.0, i0 - 0.1, t_que - 0.1, sem=322, extra=[(0.05, "fanfarria", 0.3)])
    pa(R, SI(1), 960, 1010, 0.9, t_beb - 0.15, t_que - 0.1, sem=323)
    pa(R, SI(0), 1600, 1010, 0.75, t_org - 0.15, t_que - 0.1, sem=324, entra="cae", dy=600)
    for k, (campo, nombre) in enumerate((("edo_nayarit", "Nayarit"), ("edo_zacatecas", "Zacatecas"), ("edo_aguascalientes", "Aguascalientes"),
                                         ("edo_guanajuato", "Guanajuato"), ("edo_michoacan", "Michoacán"), ("edo_colima", "Colima"))):
        R.terreno(t_est - 0.2 + 0.12 * k, campo, M.COL_ESTADOS[nombre], 0.5, capa=1 + k)
    titulo(R, t_que, FIN(e) + 1.2, "¿QUÉ ESTADO SIGUE?", px=82)
    R.texto(t_dim, FIN(e) + 1.1, "¡DÍMELO ABAJO!", (1520, 320), px=56, d=0.4)
    pa(R, HO(11), 330, 1010, 1.0, t_que, FIN(e) + 1.2, sem=325)
    pa(R, C.campana(), 1050, 315, 0.82, t_dim - 0.2, FIN(e) + 1.2, sem=326, extra=[(0.08, "campana", 0.5)])


def _transiciones(R):
    tipos = ["tinta", "pincel", "papel", "portal", "rollo", "puntos", "ola", "pincel", "tinta", "papel", "persianas", "portal"]
    colores = [(196, 120, 62), (176, 52, 48), (214, 156, 58), (74, 146, 98), (204, 72, 58), (74, 138, 104), (196, 146, 68),
               (198, 70, 60), (56, 138, 84), (204, 92, 66), (236, 186, 58), (204, 92, 66)]
    ids = [e["id"] for e in __import__("escena_base").TL["escenas"]]
    centros = [(FIN(a) + INI(b)) / 2 for a, b in zip(ids, ids[1:])]
    for k, tc in enumerate(centros):
        tipo, color = tipos[k % len(tipos)], colores[k % len(colores)]
        R.trans.append(Transicion(tc, tipo, color, (960, 540), (960, 540), dur=0.8, seed=k + 1))
        R.snd(tc - 0.4, SFX[tipo], 0.45, dur=0.8)
