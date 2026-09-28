# -*- coding: utf-8 -*-
"""Genera API.md: referencia compacta de lo reutilizable (firmas + primera línea de docstring).
Se ejecuta desde la raíz con:  python fab.py api
Lee el código fuente con ast (no importa módulos que necesiten un timeline)."""
import ast
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUC = os.path.join(RAIZ, "nucleo")


def firma(fn):
    a = fn.args
    partes = []
    defs = [None] * (len(a.args) - len(a.defaults)) + list(a.defaults)
    for arg, d in zip(a.args, defs):
        if arg.arg == "self":
            continue
        partes.append(arg.arg if d is None else f"{arg.arg}={ast.unparse(d)}")
    if a.vararg:
        partes.append("*" + a.vararg.arg)
    for arg, d in zip(a.kwonlyargs, a.kw_defaults):
        partes.append(arg.arg if d is None else f"{arg.arg}={ast.unparse(d)}")
    if a.kwarg:
        partes.append("**" + a.kwarg.arg)
    return f"{fn.name}({', '.join(partes)})"


def doc1(n):
    d = ast.get_docstring(n)
    return (" — " + d.strip().split("\n")[0]) if d else ""


def modulo(nombre, solo=None, clases=True):
    arbol = ast.parse(open(os.path.join(NUC, nombre + ".py"), encoding="utf-8").read())
    out = [f"\n## {nombre}.py{doc1(arbol)}\n"]
    for n in arbol.body:
        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_") and (solo is None or n.name in solo):
            out.append(f"- `{firma(n)}`{doc1(n)}")
        elif clases and isinstance(n, ast.ClassDef) and not n.name.startswith("_"):
            out.append(f"- **class {n.name}**{doc1(n)}")
            for m in n.body:
                if isinstance(m, ast.FunctionDef) and not m.name.startswith("_"):
                    out.append(f"    - `{firma(m)}`{doc1(m)}")
    return out


def claves_dict(nombre, var):
    arbol = ast.parse(open(os.path.join(NUC, nombre + ".py"), encoding="utf-8").read())
    for n in arbol.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", None) == var for t in n.targets):
            v = n.value
            if isinstance(v, ast.Dict):
                return [ast.literal_eval(k) for k in v.keys]
            if isinstance(v, ast.Call) and getattr(v.func, "id", "") == "dict":
                return [k.arg for k in v.keywords]
    return []


def main():
    L = ["# API de la Fábrica de Animaciones (generado con `python fab.py api` — no editar a mano)",
         "", "Consulta esto en vez de leer el código completo. Detalles: `grep -n \"def nombre\" nucleo/*.py`."]
    L.append("\n## Catálogos")
    L.append(f"- **Estilos visuales** (`estilos.ESTILOS`): {', '.join(claves_dict('estilos', 'ESTILOS'))}")
    L.append(f"- **Íconos** (`escena_base.ICONOS`, usar con `dibujar_icono(lz, nombre, x, y, s, t)`): "
             f"{', '.join(claves_dict('escena_base', 'ICONOS'))}")
    L.append(f"- **Fondos** (`fondos.FONDOS`): {', '.join(claves_dict('fondos', 'FONDOS'))}")
    L.append(f"- **Transiciones** (`efectos.TRANSICIONES`): {', '.join(claves_dict('efectos', 'TRANSICIONES'))}")
    L.append(f"- **Paletas** (`fondos.PALETAS`): {', '.join(claves_dict('fondos', 'PALETAS'))}")
    L.append(f"- **Sabores musicales** (`config.SABORES`): {', '.join(claves_dict('config', 'SABORES'))}")
    L.append(f"- **Patrones de bombo** (`ritmo.PATRONES`): {', '.join(claves_dict('ritmo', 'PATRONES'))}")
    arbol = ast.parse(open(os.path.join(NUC, "sfx.py"), encoding="utf-8").read())
    sfx = [n.name[2:] for n in arbol.body if isinstance(n, ast.FunctionDef) and n.name.startswith("s_")]
    L.append(f"- **Efectos de sonido** (`self.ev(t, nombre, vol, pan, tono=, dur=)`): {', '.join(sfx)}")
    L.append(f"- **Modos** (`musica.MODOS`): {', '.join(claves_dict('musica', 'MODOS'))}")
    L += modulo("escena_base")
    L += modulo("motor")
    L += modulo("dibujos")
    L += modulo("plano")
    L += modulo("fondos")
    L += modulo("efectos")
    L += modulo("estilos")
    L += modulo("sinte", clases=False)
    open(os.path.join(RAIZ, "API.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("API.md:", len(L), "líneas")


if __name__ == "__main__":
    main()
