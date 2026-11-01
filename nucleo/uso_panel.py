# -*- coding: utf-8 -*-
"""Bitácora de uso del panel: guarda cómo interactúa el usuario con el panel y la resume para rediseñarlo.

  guardar(eventos)                       lo llama panel.py en POST /api/uso (eventos de nucleo/panel_uso.js)
  python nucleo/uso_panel.py resumen [--dias 14] [--ui v2] [--json]   informe de comportamiento (lo lee el skill analizar-uso-panel)
  python nucleo/uso_panel.py estado                         cuántos eventos hay y desde cuándo
  python nucleo/uso_panel.py borrar --antes AAAA-MM-DD      limpia archivos viejos

Datos: nucleo/datos/uso_panel/AAAA-MM-DD.jsonl (una línea por evento; fuera de git; `FAB_USO_DIR` lo cambia para pruebas).
Eventos (campo `e`): ses · clk · chg · key · scr · pest · act · inv · vis · fin. Ver la cabecera de panel_uso.js.
"""
import argparse
import collections
import datetime as dt
import glob
import json
import os
import sys
import threading

DIR = os.environ.get("FAB_USO_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos", "uso_panel")
_LOCK = threading.Lock()
CAMPOS = ("t", "s", "ui", "e", "p", "k", "txt", "v", "x", "y", "dead", "sec", "vid", "canal", "key", "de", "a", "seg",
          "alto", "vh", "prof", "vis", "ctl", "w", "h", "dpr", "hora", "dia", "filtros")
MAX_LOTE = 400


def _limpio(ev):
    if not isinstance(ev, dict) or "e" not in ev:
        return None
    return {k: ev[k] for k in CAMPOS if k in ev}


def guardar(eventos):
    """Añade los eventos al archivo del día (por la hora del evento). Devuelve cuántos guardó."""
    n = 0
    por_dia = collections.defaultdict(list)
    for ev in (eventos or [])[:MAX_LOTE]:
        ev = _limpio(ev)
        if not ev:
            continue
        t = ev.get("t")
        d = dt.datetime.fromtimestamp(t / 1000.0) if isinstance(t, (int, float)) else dt.datetime.now()
        por_dia[d.strftime("%Y-%m-%d")].append(json.dumps(ev, ensure_ascii=False, separators=(",", ":")))
    if not por_dia:
        return 0
    with _LOCK:
        os.makedirs(DIR, exist_ok=True)
        for dia, lineas in por_dia.items():
            with open(os.path.join(DIR, dia + ".jsonl"), "a", encoding="utf-8") as f:
                f.write("\n".join(lineas) + "\n")
            n += len(lineas)
    return n


def leer(dias=14):
    """Eventos de los últimos `dias` días, en orden de tiempo."""
    desde = (dt.date.today() - dt.timedelta(days=dias - 1)).strftime("%Y-%m-%d")
    out = []
    for ruta in sorted(glob.glob(os.path.join(DIR, "*.jsonl"))):
        if os.path.basename(ruta)[:10] < desde:
            continue
        with open(ruta, encoding="utf-8") as f:
            for lin in f:
                try:
                    out.append(json.loads(lin))
                except ValueError:
                    pass
    out.sort(key=lambda e: e.get("t", 0))
    return out


# ============================================================================ análisis
def _top(c, n=12):
    return [[k, v] for k, v in c.most_common(n)]


def resumen(dias=14, ui=None):
    ev = leer(dias)
    if ui:
        ev = [e for e in ev if e.get("ui", "v1") == ui]
    R = dict(dias=dias, eventos=len(ev))
    if not ev:
        return R
    R["desde"] = dt.datetime.fromtimestamp(ev[0]["t"] / 1000).strftime("%Y-%m-%d %H:%M")
    R["hasta"] = dt.datetime.fromtimestamp(ev[-1]["t"] / 1000).strftime("%Y-%m-%d %H:%M")
    R["versiones_ui"] = _top(collections.Counter(e.get("ui", "?") for e in ev))

    # ---- sesiones y tiempo de atención por pestaña (cada `act` = 15 s de atención real)
    ses = [e for e in ev if e["e"] == "ses"]
    R["sesiones"] = len(ses)
    R["dias_con_uso"] = len({dt.datetime.fromtimestamp(e["t"] / 1000).strftime("%Y-%m-%d") for e in ev})
    R["horas_del_dia"] = sorted(collections.Counter(e.get("hora") for e in ses if e.get("hora") is not None).items())
    R["pantalla"] = _top(collections.Counter("%sx%s" % (e.get("w"), e.get("h")) for e in ses), 4)
    atencion = collections.Counter()
    for e in ev:
        if e["e"] == "act":
            atencion[e.get("p", "?")] += e.get("seg", 15)
    R["atencion_min_por_pestana"] = {k: round(v / 60, 1) for k, v in atencion.most_common()}
    R["atencion_total_min"] = round(sum(atencion.values()) / 60, 1)
    R["cambios_de_pestana"] = _top(collections.Counter("%s→%s" % (e.get("de"), e.get("a")) for e in ev if e["e"] == "pest"))

    # ---- clics
    clk = [e for e in ev if e["e"] == "clk"]
    vivos = [e for e in clk if not e.get("dead")]
    R["clics"] = len(clk)
    R["clics_muertos"] = len(clk) - len(vivos)
    R["clics_por_pestana"] = _top(collections.Counter(e.get("p") for e in clk))
    ctl = collections.Counter(((e.get("k") or "?") + ("=" + str(e["v"]) if "v" in e else "")) for e in vivos)
    R["controles_mas_usados"] = _top(ctl, 25)
    txt = {}
    for e in vivos:
        txt.setdefault((e.get("k") or "?") + ("=" + str(e["v"]) if "v" in e else ""), e.get("txt", ""))
    R["etiquetas"] = {k: txt[k] for k, _ in ctl.most_common(25)}
    R["clics_muertos_donde"] = _top(collections.Counter("%s %s «%s»" % (e.get("p"), e.get("k"), e.get("txt", "")) for e in clk if e.get("dead")), 12)
    # clics repetidos en el mismo control en < 2 s (impaciencia o control que no responde)
    rep = collections.Counter()
    prev = {}
    for e in clk:
        k = e.get("k")
        if k in prev and e["t"] - prev[k] < 2000:
            rep[k] += 1
        prev[k] = e["t"]
    R["clics_repetidos_rapido"] = _top(rep, 8)
    # mapa de calor grueso (4 columnas × 4 filas) por pestaña
    calor = collections.defaultdict(lambda: [[0] * 4 for _ in range(4)])
    for e in clk:
        if "x" in e and "y" in e:
            calor[e.get("p", "?")][min(3, int(e["y"] * 4))][min(3, int(e["x"] * 4))] += 1
    R["mapa_calor_4x4"] = {p: m for p, m in calor.items()}
    R["videos_mas_tocados"] = _top(collections.Counter(e["vid"] for e in clk if e.get("vid")), 12)
    R["canales_mas_tocados"] = _top(collections.Counter(e["canal"] for e in clk if e.get("canal")), 8)

    # ---- filtros y búsquedas
    chg = [e for e in ev if e["e"] == "chg"]
    R["filtros"] = _top(collections.Counter("%s=%s" % (e.get("k"), e.get("v")) for e in chg if e.get("k") != "#q"), 20)
    R["busquedas"] = _top(collections.Counter(e.get("v") for e in chg if e.get("k") == "#q" and e.get("v")), 15)
    sec_filtro = collections.Counter(e["v"] for e in clk if e.get("k") == "[data-f]" and "v" in e)
    R["chips_de_filtro_clics"] = _top(sec_filtro)
    R["filtros_al_abrir"] = _top(collections.Counter(json.dumps(e.get("filtros"), sort_keys=True) for e in ses), 5)

    # ---- teclado
    R["atajos_teclado"] = _top(collections.Counter(e.get("key") for e in ev if e["e"] == "key"))

    # ---- scroll: profundidad y cuánto se scrollea sin llegar a nada
    scr = [e for e in ev if e["e"] == "scr"]
    prof = collections.defaultdict(list)
    for e in scr:
        prof[(e.get("p"), e.get("k"))].append(e.get("prof", 0))
    R["scroll"] = [dict(pestana=p, contenedor=k, veces=len(v), profundidad_media=round(sum(v) / len(v), 2), profundidad_max=round(max(v), 2))
                   for (p, k), v in sorted(prof.items(), key=lambda kv: -len(kv[1]))[:10]]
    R["alto_pagina_px"] = {str(p): max(e.get("alto", 0) for e in scr if e.get("p") == p) for p in {e.get("p") for e in scr}}
    vis = collections.Counter(v for e in scr for v in (e.get("vis") or []))
    R["tarjetas_que_mas_se_miran"] = _top(vis, 12)
    # scroll de ida y vuelta (sube y baja sobre lo mismo) = buscar algo que no está a mano
    vai = 0
    for a, b in zip(scr, scr[1:]):
        if a.get("k") == b.get("k") and (a.get("y", 0) - a.get("de", 0)) * (b.get("y", 0) - b.get("de", 0)) < 0 and b["t"] - a["t"] < 8000:
            vai += 1
    R["scroll_ida_y_vuelta"] = vai

    # ---- controles que existen pero nunca se tocan (último inventario por pestaña vs. clics)
    vistos = set(ctl)
    inv = {}
    for e in ev:
        if e["e"] == "inv":
            for c in e.get("ctl", []):
                inv.setdefault((e.get("p"), c["k"]), c)
    nunca = [dict(pestana=p, control=k, texto=c.get("txt", ""), copias=c.get("n", 1)) for (p, k), c in inv.items()
             if k not in vistos and c.get("vis", 1)]
    R["controles_nunca_tocados"] = nunca[:40]
    R["controles_inventariados"] = len(inv)
    return R


def informe(R):
    L = []
    P = L.append
    if not R.get("eventos"):
        return "Sin datos todavía: abre el panel (reiniciado, con panel_uso.js) y úsalo unos días."
    P("USO DEL PANEL · %s → %s · %d días con uso · %d sesiones · %d eventos · UI %s" % (
        R["desde"], R["hasta"], R["dias_con_uso"], R["sesiones"], R["eventos"], ", ".join("%s(%d)" % tuple(x) for x in R["versiones_ui"])))
    P("Atención real: %s min en total · por pestaña %s" % (R["atencion_total_min"], R["atencion_min_por_pestana"]))
    P("Horas de apertura (hora, sesiones): %s · pantallas: %s" % (R["horas_del_dia"], R["pantalla"]))
    P("Cambios de pestaña: %s" % R["cambios_de_pestana"])
    P("\nCLICS: %d (muertos = sin nada interactivo: %d). Por pestaña: %s" % (R["clics"], R["clics_muertos"], R["clics_por_pestana"]))
    P("Controles más usados:")
    for k, n in R["controles_mas_usados"]:
        P("  %4d  %-28s %s" % (n, k, R["etiquetas"].get(k, "")))
    P("Videos más tocados: %s" % R["videos_mas_tocados"])
    P("Canales más tocados: %s" % R["canales_mas_tocados"])
    P("Clics muertos (dónde): %s" % R["clics_muertos_donde"])
    P("Clics repetidos en < 2 s: %s" % R["clics_repetidos_rapido"])
    P("\nFILTROS: %s" % R["filtros"])
    P("Chips de filtro: %s · al abrir: %s" % (R["chips_de_filtro_clics"], R["filtros_al_abrir"]))
    P("Búsquedas: %s" % R["busquedas"])
    P("Atajos de teclado: %s" % R["atajos_teclado"])
    P("\nSCROLL: ida y vuelta %d veces · alto de página %s" % (R["scroll_ida_y_vuelta"], R["alto_pagina_px"]))
    for s in R["scroll"]:
        P("  %s %s: %d veces, profundidad media %s, máx %s" % (s["pestana"], s["contenedor"], s["veces"], s["profundidad_media"], s["profundidad_max"]))
    P("Tarjetas que más se ven al detenerse: %s" % R["tarjetas_que_mas_se_miran"])
    P("\nMAPA DE CALOR (filas = arriba→abajo, columnas = izq→der):")
    for p, m in R["mapa_calor_4x4"].items():
        P("  %s" % p)
        for fila in m:
            P("    " + " ".join("%4d" % c for c in fila))
    P("\nCONTROLES QUE EXISTEN Y NUNCA SE TOCAN (%d inventariados):" % R["controles_inventariados"])
    for c in R["controles_nunca_tocados"]:
        P("  [%s] %s  «%s» ×%d" % (c["pestana"], c["control"], c["texto"], c["copias"]))
    return "\n".join(L)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("accion", choices=["resumen", "estado", "borrar"])
    ap.add_argument("--dias", type=int, default=14)
    ap.add_argument("--ui", help="solo los eventos de esa versión de la interfaz (v1, v2…) para comparar antes/después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--antes", help="AAAA-MM-DD (con borrar)")
    a = ap.parse_args()
    if a.accion == "resumen":
        R = resumen(a.dias, a.ui)
        print(json.dumps(R, ensure_ascii=False, indent=1) if a.json else informe(R))
    elif a.accion == "estado":
        arch = sorted(glob.glob(os.path.join(DIR, "*.jsonl")))
        n = sum(sum(1 for _ in open(r, encoding="utf-8")) for r in arch)
        print("%d archivos, %d eventos, %s → %s  (%s)" % (len(arch), n, os.path.basename(arch[0])[:10] if arch else "-",
                                                          os.path.basename(arch[-1])[:10] if arch else "-", DIR))
    elif a.accion == "borrar":
        if not a.antes:
            sys.exit("falta --antes AAAA-MM-DD")
        for r in glob.glob(os.path.join(DIR, "*.jsonl")):
            if os.path.basename(r)[:10] < a.antes:
                os.remove(r)
                print("borrado", r)


if __name__ == "__main__":
    main()
